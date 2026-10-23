from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from dataclasses import replace
from pathlib import Path

import pytest

import rawlsing_next.pre553_universal_evidence_binding as binding
from rawlsing_next.pre553_empirical_objects import canonicalize
from rawlsing_next.pre553_universal_evidence_binding import (
    EvidenceAssociationError,
    EvidenceConsumerReader,
    EvidenceRequest,
    EvidenceRequestShapeError,
    EvidenceResolver,
    EvidenceResult,
    reduce_required_support,
)
from rawlsing_next.tests.n10e_empirical_slice_fixture import (
    at07_rows,
    build_provider_case,
)
from rawlsing_next.tests.test_universal_evidence_binding import (
    _binding,
    _condition,
    _ref,
    _request,
    _zero_case,
)


def _positive():
    case = build_provider_case("forward")
    request = _request(case, request_id="r08v-baseline-positive")
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, case))
    result = resolver.resolve(request)
    return case, request, resolver, result


def test_positive_actual_provider_arithmetic_and_real_evaluator_call(monkeypatch):
    rows = at07_rows()
    cohort = [row for row in rows if row["responses"]["POSITION"] == "P1"]
    expected = {
        "yes": sum(row["responses"]["ANSWER"] == "yes" for row in cohort),
        "no": sum(row["responses"]["ANSWER"] == "no" for row in cohort),
    }
    original = binding.evaluate_positioned_subject_possibility
    calls = []

    def witnessed(**kwargs):
        calls.append(kwargs)
        return original(**kwargs)

    monkeypatch.setattr(
        binding, "evaluate_positioned_subject_possibility", witnessed
    )
    _, request, _, result = _positive()

    assert len(cohort) == 60
    assert expected == {"yes": 54, "no": 6}
    assert result.result_state == "SUPPORTED"
    assert result.denominator == 60
    assert {cell["cell"]: cell["raw_numerator_support"] for cell in result.cells} == expected
    assert calls, "candidate did not invoke the actual unchanged evaluator"
    assert result.consumer_result_object is not None
    assert result.consumer_result_object.result_state == "EXACT_SUPPORTED"
    assert result.consumer_result_object.result_hash == result.consumer_result_hash
    replay = original(
        query=result.consumer_query_object,
        rule=result.model_rule_object,
        evidence=(result.evidence_object,),
    )
    assert replay.material() == result.consumer_result_object.material()
    read = EvidenceConsumerReader(request, result).read()
    assert read["denominator"] == 60
    assert read["consumer_result_hash"] == result.consumer_result_hash


def test_cold_process_cache_baseline(tmp_path):
    case = build_provider_case("forward")
    request = _request(case, request_id="r08v-baseline-cold")
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    cache_path = tmp_path / "cache.json"
    cache_path.write_text(json.dumps(resolver.export_cache()), encoding="utf-8")
    script = f"""
import json
from pathlib import Path
from rawlsing_next.tests.n10e_empirical_slice_fixture import build_provider_case
from rawlsing_next.tests.test_universal_evidence_binding import _request
from rawlsing_next.pre553_universal_evidence_binding import EvidenceConsumerReader, EvidenceResolver
case = build_provider_case("forward")
request = _request(case, request_id="r08v-baseline-cold")
cache = json.loads(Path({str(cache_path)!r}).read_text(encoding="utf-8"))
resolver = EvidenceResolver()
resolver.import_authenticated_cache(cache)
result = resolver.resolve(request)
values = EvidenceConsumerReader(request, result).read()
print(json.dumps({{"provenance": result.provenance, "state": result.result_state,
"denominator": result.denominator, "consumer_denominator": values["denominator"],
"consumer_hash": result.consumer_result_hash}}, sort_keys=True))
"""
    completed = subprocess.run(
        [sys.executable, "-c", script],
        cwd=Path(__file__).resolve().parents[3],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout.strip().splitlines()[-1])
    assert observed == {
        "provenance": "AUTHENTICATED_CACHE",
        "state": "SUPPORTED",
        "denominator": 60,
        "consumer_denominator": 60,
        "consumer_hash": produced.consumer_result_hash,
    }


def test_actual_zero_support_refuses_consumer_and_summary():
    case = build_provider_case("forward")
    zero = _zero_case(case)
    request = _request(
        zero,
        conditions=(_condition("POSITION", "P3", "P3", "position"),),
        direction="POSITION_P3_TO_ANSWER",
        request_id="r08v-baseline-zero",
    )
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, zero))
    result = resolver.resolve(request)
    assert result.result_state == "ZERO_SUPPORT"
    assert result.denominator == 0
    with pytest.raises(EvidenceAssociationError):
        EvidenceConsumerReader(request, result).read()
    summary = reduce_required_support([result])
    assert summary.exact_all_support is False
    assert summary.productive_all_required is False
    assert summary.positive_support_count == 0


def test_valid_null_control_is_not_all_support():
    valid_null = EvidenceResult(
        request_key="a" * 64,
        eligibility_state="ELIGIBLE",
        execution_state="COMPLETED",
        result_state="VALID_NULL",
        provenance="TYPED_REFUSAL",
        denominator=10,
    )
    summary = reduce_required_support([valid_null])
    assert summary.exact_all_support is False
    assert summary.positive_support_count == 0
    assert summary.result_counts["VALID_NULL"] == 1
    assert summary.productive_all_required is True


def test_severance_of_actual_evidence_refuses_same_consumer_assertion():
    _, request, _, result = _positive()
    changed = build_provider_case("forward", variant="CHANGED_SOURCE_LAW")
    changed_request = _request(changed, request_id="r08v-baseline-severed-source")
    changed_resolver = EvidenceResolver()
    changed_resolver.bind(_binding(changed_request, changed))
    changed_result = changed_resolver.resolve(changed_request)
    assert changed_result.result_state == "SUPPORTED"
    assert changed_result.denominator == 70
    severed = replace(result, evidence_object=changed_result.evidence_object)
    with pytest.raises(EvidenceAssociationError):
        EvidenceConsumerReader(request, severed).read()


def test_absent_condition_tuple_is_rejected_at_shape_boundary():
    case = build_provider_case("forward")
    request = _request(case, request_id="r08v-baseline-absent")
    with pytest.raises(EvidenceRequestShapeError):
        EvidenceRequest(**{**request.__dict__, "ordered_conditions": ()})


def test_request_clock_and_permission_changes_do_not_hit_cache():
    case = build_provider_case("forward")
    request = _request(case, request_id="r08v-baseline-clock")
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, case))
    assert resolver.resolve(request).result_state == "SUPPORTED"
    cache = resolver.export_cache()
    cold = EvidenceResolver()
    cold.import_authenticated_cache(cache)
    assert cold.resolve(request).result_state == "SUPPORTED"
    for mutated in (
        request.changed(as_of_clock="2027-01-01"),
        request.changed(
            permission_ref=_ref(
                "R61_PERMISSION", "other-permission", {"scope": "OTHER"}
            )
        ),
        request.changed(edition="2025-12"),
    ):
        assert cold.resolve(mutated).result_state == "UNKNOWN"
