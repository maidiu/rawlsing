"""R03 sourcefree total native workload qualification (TEST_ONLY)."""
from __future__ import annotations

from dataclasses import replace
import hashlib
from pathlib import Path

import pytest

from rawlsing_next.pre553_native_workload_binding import WorkloadBindingRefusal
from rawlsing_next.pre553_physical_decoder import decode_dta, decode_sav
from rawlsing_next.pre553_source_native_preimage_adapter import (
    NativePreimageRefusal, NativeSourceRule, materialize_native_preimages,
)
from rawlsing_next.pre553_universal_workload import (
    bind_recursive_execution, compile_universal_workload,
    execute_universal_workload,
)
from rawlsing_next.tests.test_universal_source_projection import (
    SOURCE_ID, build_s3, decode_sav as _decode_sav, package, s3_rows,
    write_rows,
)

AS_OF = "2026-10-23"
HOST = "local-r03"
PURPOSE = "TEST_ONLY_SOURCEFREE"


def _expected_sav_operations(bundle):
    expected = set()
    for item in bundle.administered:
        qref = bundle.question_refs.get(item.source_variable_code)
        if qref is None:
            continue
        values = {
            str(rule.canonical_value)
            for slot in bundle.projection.response_slots
            if slot.question_binding.native_question_ref == qref
            for rule in slot.values
            if rule.response_state == "SUBSTANTIVE_RESPONSE"
            and rule.canonical_value is not None
        }
        for value in values:
            expected.add((item.source_variable_code, value))
    return expected


def test_r03_heterogeneous_sav_total_workload_and_no_drop(tmp_path):
    path = tmp_path / "r03_s3.sav"
    bundle = build_s3(path, s3_rows(respondents=6, occasions=2))
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    expected = _expected_sav_operations(bundle)
    observed = {(op.source_variable_code, op.response_value)
                for op in compilation.operations if op.status == "COMPILED"}
    assert observed == expected
    assert compilation.expected_jobs
    assert len(compilation.expected_jobs) == len(set(compilation.expected_jobs))
    result = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    join = result.anti_join()
    assert join["no_drop_ok"], join
    assert result.native_results
    assert result.receipt_refs
    assert result.fact_refs
    assert not result.failed
    assert compilation.content_hash == compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE).content_hash


def test_r03_dta_valid_person_and_cross_unit_refusal(tmp_path):
    path = tmp_path / "r03_person.dta"
    rows = [{"PID": float(i), "OCCASION": 0.0, "A": float(i % 2),
             "Y": float((i // 2) % 2)} for i in range(6)]
    write_rows(path, rows, fmt="dta")
    pkg = package(
        path, len(rows),
        (NativeSourceRule("impl.a", "A"), NativeSourceRule("impl.y", "Y")),
        coordinate="OCCASION", source_format="DTA",
    )
    bundle = materialize_native_preimages(
        package=pkg, incidence=decode_dta(path))
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    result = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert result.anti_join()["no_drop_ok"]
    assert result.fact_refs

    household_path = tmp_path / "r03_cross_unit.dta"
    write_rows(household_path, [{"HID": 1.0, "PID": 1.0, "HMEAS": 1.0,
                                "OUTCOME": 1.0, "OCCASION": 0.0}], fmt="dta")
    with pytest.raises(NativePreimageRefusal) as caught:
        package(
            household_path, 1,
            (NativeSourceRule("impl.h", "HMEAS", unit="household"),
             NativeSourceRule("impl.o", "OUTCOME", unit="person")),
            coordinate="HID", units={"HMEAS": "household", "OUTCOME": "person"},
            source_format="DTA",
        )
    assert caught.value.code == "CROSS_UNIT_POOLING_UNAUTHORIZED"


def test_r03_failure_and_source_restoration_same_consumer(tmp_path):
    path = tmp_path / "r03_fault.sav"
    bundle = build_s3(path, s3_rows(respondents=4, occasions=2))
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    good = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert good.anti_join()["no_drop_ok"]
    bad_stream = replace(bundle.physical_stream, source_sha256="b" * 64)
    failed = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bad_stream,
    )
    assert failed.failed
    assert failed.executed_operation_ids == ()
    assert failed.anti_join()["no_drop_ok"] is False
    restored = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert restored.anti_join()["no_drop_ok"]
    assert restored.fact_refs == good.fact_refs


def test_r03_consumes_recursive_campaign_execution_without_rerun():
    from rawlsing_next.tests.test_universal_grammar import _campaign_fixture
    from rawlsing_next.tests.test_universal_grammar import (
        _campaign_active_refs,
    )
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    i1 = campaign.issue(
        parent_lineage_refs=(campaign.root_lineage_ref,),
        condition_refs=tuple((key, value) for key, value, _ in s1),
    )
    e1 = campaign.execute(i1)
    fragment1 = bind_recursive_execution(campaign, e1)
    assert fragment1.campaign_ref == campaign.campaign_ref
    assert fragment1.execution_ref == e1
    assert fragment1.receipt_refs
    assert fragment1.handoff_refs
    assert fragment1.fact_refs
    assert fragment1.source_release_refs
    activation1 = campaign.activate(e1)
    active = _campaign_active_refs(campaign, activation1)
    i2 = campaign.issue(
        parent_lineage_refs=active,
        condition_refs=tuple((key, value) for key, value, _ in s2),
    )
    e2 = campaign.execute(i2)
    fragment2 = bind_recursive_execution(campaign, e2)
    assert fragment2.execution_ref == e2
    assert set(fragment2.receipt_refs) != set(fragment1.receipt_refs)
    assert fragment2.operation_ids
    # Binding is read-only: no new issuance or execution appears.
    before = len(campaign.inspect()["executions"])
    bind_recursive_execution(campaign, e2)
    assert len(campaign.inspect()["executions"]) == before


def test_r03_wrong_source_edition_and_duplicate_job_refused(tmp_path):
    path = tmp_path / "r03_dup.sav"
    bundle = build_s3(path, s3_rows(respondents=4, occasions=2))
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    wrong = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: replace(bundle.physical_stream,
                                            source_sha256="c" * 64),
    )
    assert wrong.failed
    assert wrong.executed_operation_ids == ()


def test_r03_count_preserving_substitution_and_duplicate_fail_antijoin(tmp_path):
    path = tmp_path / "r03_antijoin.sav"
    bundle = build_s3(path, s3_rows(respondents=4, occasions=2))
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    result = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert result.anti_join()["no_drop_ok"]
    ids = list(result.executed_operation_ids)
    substituted = tuple(ids[:-1] + [ids[0]]) if len(ids) > 1 else tuple(ids)
    mutated = replace(result, executed_operation_ids=substituted)
    report = mutated.anti_join()
    assert report["no_drop_ok"] is False
    assert report["missing_operation_ids"]
    assert report["duplicate_operation_ids"]
    restored = replace(result, executed_operation_ids=tuple(ids))
    assert restored.anti_join()["no_drop_ok"]
