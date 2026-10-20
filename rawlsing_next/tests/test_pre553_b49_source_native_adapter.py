"""B49 source-rule selection, native preimage and TEST_ONLY workload binding tests.

These tests execute the real current PRE553 owners (C11 facade, Route B, I03
dispatch, Batch) on a frozen source-authority corpus derived from the accepted
H48 evidence and a safe synthetic nonrespondent LiTS-I incidence. No raw
source bytes and no respondent records are read.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

import rawlsing_next.pre553_issued_workload as u43
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_inherited_source_rules import (
    EXCLUDED_NON_U,
    HELD_UNRESOLVED,
    SourceAuthorityCorpus,
    SourceRuleRefusal,
    U_CANDIDATE,
    all35_coverage_ledger,
    select_source_rules,
)
from rawlsing_next.pre553_native_workload_binding import (
    OperationFixture,
    TestOnlyDecisionResolver,
    WorkloadBindingRefusal,
    build_projection_catalog,
    build_test_only_workload,
    execute_test_only_workload,
)
from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence, PhysicalVariable
from rawlsing_next.pre553_source_native_preimage_adapter import (
    ADMINISTERED,
    HELD_NATIVE_ABSENT,
    InstrumentInventory,
    NativeInstrumentVariable,
    NativePreimageRefusal,
    build_authority_set,
    materialize_native_preimages,
)

RETURN = Path(__file__).resolve().parents[2] / "WORKER_RETURNS" / (
    "PYAT-R49-B49-REUSE-FIRST-AUTHORITY-NATIVE-ADAPTER-R1"
)
CORPUS_PATH = RETURN / "corpus" / "source_authority_corpus.json"

SYN_COLUMNS = ("q301_2", "q301_7", "country", "w1", "id")
SYN_ROWS = (
    (1, 2, "US", 1, "S1"),
    (3, 4, "US", 2, "S2"),
    (5, None, "US", 3, "S3"),
)


def _corpus() -> SourceAuthorityCorpus:
    return SourceAuthorityCorpus.from_document(json.loads(CORPUS_PATH.read_text()))


def _incidence(sha: str, rows=SYN_ROWS, columns=SYN_COLUMNS) -> PhysicalSourceIncidence:
    variables = tuple(
        PhysicalVariable(i, name, None, f"label-{name}", {}, (), {}, {})
        for i, name in enumerate(columns, 1)
    )
    return PhysicalSourceIncidence(
        source_sha256=sha,
        source_format="SYNTHETIC",
        row_count=len(rows),
        variables=variables,
        reader_configuration={"fixture": "b49-synthetic"},
        file_metadata={"fixture": "b49-synthetic"},
        _frame=pd.DataFrame(rows, columns=columns),
    )


def _inventory(sha: str, variables=SYN_COLUMNS, respondents: int = 3) -> InstrumentInventory:
    return InstrumentInventory(
        source_id="27",
        source_sha256=sha,
        variables=tuple(
            NativeInstrumentVariable(name, i, (), "TEST_ONLY_REPRESENTATION")
            for i, name in enumerate(variables, 1)
        ),
        respondent_count=respondents,
        id_variable="id",
        country_variable="country",
        weight_variable="w1",
        country_scope=("US",),
    )


def _bundle():
    corpus = _corpus()
    package = select_source_rules(
        corpus, family="LiTS", wave="I", as_of="2026-10-20"
    )
    authorities = build_authority_set(source=package.source, as_of="2026-10-20")
    incidence = _incidence(package.source.declared_sha256)
    bundle = materialize_native_preimages(
        package=package,
        inventory=_inventory(package.source.declared_sha256),
        incidence=incidence,
        authorities=authorities,
        as_of="2026-10-20",
    )
    return corpus, package, bundle, incidence


# ---------------------------------------------------------------------------
# T1 — source-rule selection
# ---------------------------------------------------------------------------

def test_corpus_is_the_exact_frozen_h48_authority_evidence():
    corpus = _corpus()
    assert corpus.source_count == 35
    assert len(corpus.unmatched_ids) == 26
    assert corpus.total_authority_items == 18276
    assert corpus.schema == "B49_SOURCE_AUTHORITY_CORPUS@1.0.0"


def test_all35_coverage_ledger_accounts_every_source_identity_once():
    ledger = all35_coverage_ledger(_corpus())
    assert len(ledger) == 35
    assert len({row["source_id"] for row in ledger}) == 35
    assert len({(row["family"], row["wave"]) for row in ledger}) == 35
    for row in ledger:
        assert row["declared_sha256"]
        assert row["identity_hash"]
        assert row["original_administered_measurement_u"] is None


def test_selected_package_is_deterministic_and_accounts_every_item():
    corpus = _corpus()
    first = select_source_rules(corpus, family="LiTS", wave="I", as_of="2026-10-20")
    second = select_source_rules(corpus, family="LiTS", wave="I", as_of="2026-10-20")
    assert first.package_hash == second.package_hash
    assert first.authority_object_identity == second.authority_object_identity
    items = corpus.items_for("LiTS", "I")
    assert len(first.accounted_item_ids) == len(items) == 1198
    assert len(set(first.accounted_item_ids)) == 1198


def test_q301_2_and_q301_7_are_selected_certified_directional():
    corpus = _corpus()
    package = select_source_rules(corpus, family="LiTS", wave="I", as_of="2026-10-20")
    by_code = {rule.source_variable_code: rule for rule in package.selected}
    for code in ("q301_2", "q301_7"):
        rule = by_code[code]
        assert rule.status == U_CANDIDATE
        assert rule.semantic_direction == "CERTIFIED_DIRECTIONAL"
        assert rule.routing_status == "UNCONDITIONAL_SOURCE_PROVEN"
        assert rule.response_binding_status == "bound"
        assert rule.authority_evidence_refs


def test_excluded_administrative_items_are_not_promoted_to_u():
    corpus = _corpus()
    package = select_source_rules(corpus, family="LiTS", wave="I", as_of="2026-10-20")
    assert package.excluded
    assert all(rule.status == EXCLUDED_NON_U for rule in package.excluded)
    assert not any(rule.disposition == "administrative_metadata" for rule in package.selected)


def test_unmatched_fqra_id_is_held_and_refused_when_promoted():
    corpus = _corpus()
    package = select_source_rules(corpus, family="Afrobarometer", wave="Round 1", as_of="2026-10-20")
    unmatched_held = {
        rule.implementation_id for rule in package.held
        if rule.reason == "FQRA_RELATION_ID_UNMATCHED__HELD_NOT_PROMOTED"
    }
    assert unmatched_held, "unmatched FQRA IDs must be held explicitly"
    assert unmatched_held <= set(corpus.unmatched_ids)
    with pytest.raises(SourceRuleRefusal) as exc:
        select_source_rules(
            corpus, family="Afrobarometer", wave="Round 1", as_of="2026-10-20",
            promote_unmatched=True,
        )
    assert exc.value.code == "UNMATCHED_FQRA_ID_CANNOT_BE_PROMOTED"


def test_synthetic_grant_is_refused():
    with pytest.raises(SourceRuleRefusal) as exc:
        select_source_rules(
            _corpus(), family="LiTS", wave="I", as_of="2026-10-20",
            synthetic_grant={"CURRENT_ACCEPTED": True},
        )
    assert exc.value.code == "SYNTHETIC_GRANT_REFUSED"


def test_wrong_edition_and_wrong_decoder_refuse():
    corpus = _corpus()
    with pytest.raises(SourceRuleRefusal) as exc:
        select_source_rules(
            corpus, family="LiTS", wave="I", as_of="2026-10-20",
            expected_source_sha256="0" * 64,
        )
    assert exc.value.code == "SCOPE_OR_EDITION_MISMATCH"
    with pytest.raises(SourceRuleRefusal) as exc:
        select_source_rules(
            corpus, family="LiTS", wave="I", as_of="2026-10-20",
            required_decoder_mode="UNSUPPORTED_DECODER",
        )
    assert exc.value.code == "DECODER_MODE_MISMATCH"


def test_superseded_ledger_refuses():
    with pytest.raises(SourceRuleRefusal) as exc:
        select_source_rules(
            _corpus(), family="LiTS", wave="I", as_of="2026-10-20",
            ledger_versions={"p2": "v1"},
            required_ledger_versions={"p2": "v2"},
        )
    assert exc.value.code == "SUPERSEDED_RULE_REQUIRES_CURRENT"


def test_duplicate_implementation_identity_refuses():
    corpus = _corpus()
    items = list(corpus.items)
    victim = next(i for i in items if i.source_family == "LiTS" and i.wave == "2006")
    forged = type(victim)(
        implementation_id=victim.implementation_id,
        source_family=victim.source_family,
        wave=victim.wave,
        source_variable_code="forged_alias",
        p2_row=victim.p2_row,
        p2_evidence_id=victim.p2_evidence_id,
        exact_identity_sha256="f" * 64,
        disposition=victim.disposition,
        binding_grade=victim.binding_grade,
        response_binding_status=victim.response_binding_status,
        directional_certification_status=victim.directional_certification_status,
        current_directional_atom_eligible=victim.current_directional_atom_eligible,
        routing_status=victim.routing_status,
        relation_evidence_id=victim.relation_evidence_id,
        relation_data_row=victim.relation_data_row,
    )
    from dataclasses import replace

    hostile = replace(corpus, items=tuple(items) + (forged,))
    with pytest.raises(SourceRuleRefusal) as exc:
        select_source_rules(hostile, family="LiTS", wave="I", as_of="2026-10-20")
    assert exc.value.code == "AMBIGUOUS_DUPLICATE_IMPLEMENTATION_IDENTITY"


def test_unknown_source_wave_refuses():
    with pytest.raises(SourceRuleRefusal) as exc:
        select_source_rules(_corpus(), family="NoSuchSurvey", wave="X", as_of="2026-10-20")
    assert exc.value.code == "UNKNOWN_OR_AMBIGUOUS_SOURCE_WAVE"


# ---------------------------------------------------------------------------
# T2 — native preimage materialization
# ---------------------------------------------------------------------------

def test_native_preimage_classifies_administered_u_and_holds_the_rest():
    _, _, bundle, _ = _bundle()
    assert {item.source_variable_code for item in bundle.administered} == {"q301_2", "q301_7"}
    assert all(item.classification == ADMINISTERED for item in bundle.administered)
    assert bundle.held
    assert all(
        item.classification in (HELD_NATIVE_ABSENT, "HELD_PACKAGE_UNRESOLVED")
        for item in bundle.held
    )
    assert bundle.excluded
    assert bundle.projection.expected_source_sha256 == bundle.source_sha256


def test_native_preimage_refuses_wrong_edition():
    _, package, _, incidence = _bundle()
    authorities = build_authority_set(source=package.source, as_of="2026-10-20")
    with pytest.raises(NativePreimageRefusal) as exc:
        materialize_native_preimages(
            package=package,
            inventory=_inventory("1" * 64),
            incidence=incidence,
            authorities=authorities,
            as_of="2026-10-20",
        )
    assert exc.value.code == "WRONG_SOURCE_EDITION"


def test_native_preimage_refuses_row_count_mismatch():
    _, package, _, incidence = _bundle()
    authorities = build_authority_set(source=package.source, as_of="2026-10-20")
    with pytest.raises(NativePreimageRefusal) as exc:
        materialize_native_preimages(
            package=package,
            inventory=_inventory(package.source.declared_sha256, respondents=4),
            incidence=incidence,
            authorities=authorities,
            as_of="2026-10-20",
        )
    assert exc.value.code == "INCIDENCE_ROW_COUNT_MISMATCH"


def test_native_preimage_holds_absent_variable_instead_of_inventing_it():
    _, package, _, incidence = _bundle()
    authorities = build_authority_set(source=package.source, as_of="2026-10-20")
    inventory = _inventory(
        package.source.declared_sha256,
        variables=("q301_2", "country", "w1", "id"),
    )
    bundle = materialize_native_preimages(
        package=package,
        inventory=inventory,
        incidence=incidence,
        authorities=authorities,
        as_of="2026-10-20",
    )
    assert [i.source_variable_code for i in bundle.administered] == ["q301_2"]
    held_codes = {i.source_variable_code for i in bundle.held}
    assert "q301_7" in held_codes


def test_native_preimage_refuses_incidence_edition_mismatch():
    _, package, _, _ = _bundle()
    authorities = build_authority_set(source=package.source, as_of="2026-10-20")
    with pytest.raises(NativePreimageRefusal) as exc:
        materialize_native_preimages(
            package=package,
            inventory=_inventory(package.source.declared_sha256),
            incidence=_incidence("2" * 64),
            authorities=authorities,
            as_of="2026-10-20",
        )
    assert exc.value.code == "INCIDENCE_SOURCE_EDITION_MISMATCH"


# ---------------------------------------------------------------------------
# T4 — TEST_ONLY native workload binding and real execution
# ---------------------------------------------------------------------------

def _issued(operation: OperationFixture | None = None):
    _, _, bundle, incidence = _bundle()
    op = operation or OperationFixture(
        fixture_id="B49-TEST-ONLY-1",
        target_variable_code="q301_2",
        response_value="1",
    )
    catalog, request = build_projection_catalog(bundle=bundle, operation=op, as_of="2026-10-20")
    issued = build_test_only_workload(
        bundle=bundle,
        projection=bundle.projection,
        catalog=catalog,
        request=request,
        operation=op,
        as_of="2026-10-20",
        host="local-b49",
        purpose="TEST_ONLY_SOURCEFREE",
    )
    return bundle, incidence, issued


def test_test_only_workload_executes_through_real_u43_c11_i03_batch():
    bundle, incidence, issued = _issued()
    result = execute_test_only_workload(
        issued=issued,
        source_factory=lambda ref: incidence,
        host="local-b49",
        purpose="TEST_ONLY_SOURCEFREE",
    )
    assert len(result.manifest.units) == 1
    assert len(result.receipts) == 1
    assert result.receipts[0].state == "COMPLETED"
    assert len(result.native_outputs) == 1
    assert len(result.output_refs) == 1
    assert result.scope == "TEST_ONLY_SOURCEFREE"
    assert result.original_wave_identity is None


def test_test_only_workload_envelope_is_deterministic():
    _, _, first = _issued()
    _, _, second = _issued()
    assert first.envelope_sha256 == second.envelope_sha256


def test_issuer_record_cannot_be_reused_for_a_different_host():
    _, incidence, issued = _issued()
    with pytest.raises(Exception) as exc:
        execute_test_only_workload(
            issued=issued,
            source_factory=lambda ref: incidence,
            host="other-host",
            purpose="TEST_ONLY_SOURCEFREE",
        )
    assert "HOST" in str(exc.value) or "PURPOSE" in str(exc.value)


def test_omitted_operation_job_is_refused():
    from dataclasses import replace

    _, incidence, issued = _issued()
    hostile_record = replace(issued.record, expected_jobs=())
    from rawlsing_next.pre553_native_workload_binding import TestOnlyIssuedWorkload

    hostile = TestOnlyIssuedWorkload(
        workload=issued.workload,
        record=hostile_record,
        descriptor=issued.descriptor,
        envelope_sha256=issued.envelope_sha256,
    )
    with pytest.raises(Exception) as exc:
        execute_test_only_workload(
            issued=hostile,
            source_factory=lambda ref: incidence,
            host="local-b49",
            purpose="TEST_ONLY_SOURCEFREE",
        )
    assert "EXPECTED_EXECUTED_OPERATION" in str(exc.value)


def test_counterfeit_descriptor_is_refused():
    from dataclasses import replace

    _, incidence, issued = _issued()
    forged_descriptor = json.dumps(
        dict(json.loads(issued.workload.descriptor), source_edition="9" * 64),
        sort_keys=True, separators=(",", ":"),
    ).encode()
    hostile = replace(issued.workload, descriptor=forged_descriptor)
    from rawlsing_next.pre553_native_workload_binding import TestOnlyIssuedWorkload

    with pytest.raises(Exception) as exc:
        execute_test_only_workload(
            issued=TestOnlyIssuedWorkload(
                workload=hostile,
                record=issued.record,
                descriptor=issued.descriptor,
                envelope_sha256=issued.envelope_sha256,
            ),
            source_factory=lambda ref: incidence,
            host="local-b49",
            purpose="TEST_ONLY_SOURCEFREE",
        )
    assert "DESCRIPTOR" in str(exc.value) or "ENVELOPE" in str(exc.value)


def test_wrong_source_edition_from_factory_is_refused():
    _, _, issued = _issued()
    wrong = _incidence("3" * 64)
    with pytest.raises(Exception) as exc:
        execute_test_only_workload(
            issued=issued,
            source_factory=lambda ref: wrong,
            host="local-b49",
            purpose="TEST_ONLY_SOURCEFREE",
        )
    assert "WRONG_EDITION" in str(exc.value) or "EDITION" in str(exc.value)


def test_revoked_record_is_refused():
    from dataclasses import replace

    _, incidence, issued = _issued()
    revoked = replace(issued.record, currentness="REVOKED")
    from rawlsing_next.pre553_native_workload_binding import TestOnlyIssuedWorkload

    with pytest.raises(Exception) as exc:
        execute_test_only_workload(
            issued=TestOnlyIssuedWorkload(
                workload=issued.workload,
                record=revoked,
                descriptor=issued.descriptor,
                envelope_sha256=issued.envelope_sha256,
            ),
            source_factory=lambda ref: incidence,
            host="local-b49",
            purpose="TEST_ONLY_SOURCEFREE",
        )
    assert "CURRENT" in str(exc.value) or "SCOPE" in str(exc.value)


def test_test_only_resolver_refuses_foreign_decision():
    _, _, issued = _issued()
    resolver = TestOnlyDecisionResolver(issued.record)
    foreign = ExactRef("TEST_ONLY_DECISION", "urn:rawlsing:b49:foreign", "a" * 64)
    with pytest.raises(WorkloadBindingRefusal) as exc:
        resolver.resolve_current(foreign)
    assert exc.value.code == "UNKNOWN_DECISION_REF"


def test_fixture_target_outside_administered_u_refuses():
    _, _, bundle, _ = _bundle()
    op = OperationFixture(
        fixture_id="B49-BAD-TARGET",
        target_variable_code="casenumb",
        response_value="1",
    )
    with pytest.raises(WorkloadBindingRefusal) as exc:
        build_projection_catalog(bundle=bundle, operation=op, as_of="2026-10-20")
    assert exc.value.code == "FIXTURE_TARGET_NOT_ADMINISTERED"


def test_evidence_source_value_change_reaches_downstream_assertion():
    """A changed synthetic source value changes the real downstream I03 fact."""
    _, first, issued_first = _issued()
    rows_changed = ((1, 2, "US", 1, "S1"), (1, 4, "US", 2, "S2"), (5, None, "US", 3, "S3"))
    changed = _incidence(issued_first.workload.projection.expected_source_sha256, rows=rows_changed)
    result_first = execute_test_only_workload(
        issued=issued_first,
        source_factory=lambda ref: first,
        host="local-b49",
        purpose="TEST_ONLY_SOURCEFREE",
    )
    _, _, bundle2, _ = _bundle()
    op = OperationFixture(
        fixture_id="B49-TEST-ONLY-1", target_variable_code="q301_2", response_value="1"
    )
    catalog2, request2 = build_projection_catalog(bundle=bundle2, operation=op, as_of="2026-10-20")
    issued_second = build_test_only_workload(
        bundle=bundle2, projection=bundle2.projection, catalog=catalog2, request=request2,
        operation=op, as_of="2026-10-20", host="local-b49", purpose="TEST_ONLY_SOURCEFREE",
    )
    result_second = execute_test_only_workload(
        issued=issued_second,
        source_factory=lambda ref: changed,
        host="local-b49",
        purpose="TEST_ONLY_SOURCEFREE",
    )
    fact_first = result_first.native_outputs[0].facts[0]
    fact_second = result_second.native_outputs[0].facts[0]
    first_fields = dict(fact_first.semantic_fields)
    second_fields = dict(fact_second.semantic_fields)
    assert fact_first.ref != fact_second.ref, (
        "a changed physical source value must change the real I03 fact identity"
    )
    assert first_fields["raw_numerator_support"] == 1
    assert second_fields["raw_numerator_support"] == 2
    assert first_fields["raw_denominator_support"] == 1
    assert second_fields["raw_denominator_support"] == 2


def test_warm_cold_bytes_are_stable():
    _, incidence, issued = _issued()
    first = execute_test_only_workload(
        issued=issued, source_factory=lambda ref: incidence,
        host="local-b49", purpose="TEST_ONLY_SOURCEFREE",
    )
    second = execute_test_only_workload(
        issued=issued, source_factory=lambda ref: incidence,
        host="local-b49", purpose="TEST_ONLY_SOURCEFREE",
    )
    assert [f.ref for f in first.native_outputs[0].facts] == [
        f.ref for f in second.native_outputs[0].facts
    ]
    assert first.envelope_sha256 == second.envelope_sha256
    assert first.summary == second.summary


def test_u43_module_is_byte_exact_staged():
    import subprocess

    path = Path(u43.__file__)
    blob = subprocess.run(
        ["git", "hash-object", str(path)], capture_output=True, text=True, check=True
    ).stdout.strip()
    assert blob == "31e84f49d624f5524906e9e7839d2873106f8249"


def test_cold_process_replay_is_byte_stable(tmp_path):
    """The full chain replayed in two fresh interpreters yields stable identities."""
    import os
    import subprocess
    import sys

    script = tmp_path / "cold_chain.py"
    script.write_text(
        "import json,hashlib\n"
        "from pathlib import Path\n"
        "import pandas as pd\n"
        "from rawlsing_next.pre553_inherited_source_rules import SourceAuthorityCorpus, select_source_rules\n"
        "from rawlsing_next.pre553_source_native_preimage_adapter import (\n"
        "    NativeInstrumentVariable, InstrumentInventory, build_authority_set,\n"
        "    materialize_native_preimages,\n"
        ")\n"
        "from rawlsing_next.pre553_native_workload_binding import (\n"
        "    OperationFixture, build_projection_catalog, build_test_only_workload,\n"
        "    execute_test_only_workload,\n"
        ")\n"
        "from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence, PhysicalVariable\n"
        f"doc = json.loads(Path({str(CORPUS_PATH)!r}).read_text())\n"
        "corpus = SourceAuthorityCorpus.from_document(doc)\n"
        "pkg = select_source_rules(corpus, family='LiTS', wave='I', as_of='2026-10-20')\n"
        "sha = pkg.source.declared_sha256\n"
        "cols = ('q301_2','q301_7','country','w1','id')\n"
        "rows = [(1,2,'US',1,'S1'),(3,4,'US',2,'S2'),(5,None,'US',3,'S3')]\n"
        "variables = tuple(PhysicalVariable(i,n,None,f'l-{n}',{},(),{},{}) for i,n in enumerate(cols,1))\n"
        "inc = PhysicalSourceIncidence(source_sha256=sha, source_format='SYNTHETIC', row_count=3, variables=variables, reader_configuration={}, file_metadata={}, _frame=pd.DataFrame(rows, columns=cols))\n"
        "inv = InstrumentInventory(source_id='27', source_sha256=sha, variables=tuple(NativeInstrumentVariable(n,i,(),'T') for i,n in enumerate(cols,1)), respondent_count=3, id_variable='id', country_variable='country', weight_variable='w1', country_scope=('US',))\n"
        "auths = build_authority_set(source=pkg.source, as_of='2026-10-20')\n"
        "b = materialize_native_preimages(package=pkg, inventory=inv, incidence=inc, authorities=auths, as_of='2026-10-20')\n"
        "op = OperationFixture(fixture_id='COLD', target_variable_code='q301_2', response_value='1')\n"
        "cat, req = build_projection_catalog(bundle=b, operation=op, as_of='2026-10-20')\n"
        "issued = build_test_only_workload(bundle=b, projection=b.projection, catalog=cat, request=req, operation=op, as_of='2026-10-20', host='h', purpose='p')\n"
        "r = execute_test_only_workload(issued=issued, source_factory=lambda ref: inc, host='h', purpose='p')\n"
        "print(json.dumps({'envelope': issued.envelope_sha256, 'refs': [f.ref.as_dict() for f in r.native_outputs[0].facts]}))\n",
        encoding="utf-8",
    )
    outputs = []
    for _ in range(2):
        env = dict(os.environ)
        env["PYTHONHASHSEED"] = "0"
        repo_root = str(Path(__file__).resolve().parents[2])
        env["PYTHONPATH"] = repo_root + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
        proc = subprocess.run(
            [sys.executable, "-B", str(script)],
            cwd=str(Path(__file__).resolve().parents[2]),
            capture_output=True, text=True, timeout=180, env=env, check=True,
        )
        outputs.append(json.loads(proc.stdout.strip()))
    assert outputs[0] == outputs[1], "cold-process replay must be byte-stable"
    assert outputs[0]["refs"], "cold replay must produce at least one native fact"
