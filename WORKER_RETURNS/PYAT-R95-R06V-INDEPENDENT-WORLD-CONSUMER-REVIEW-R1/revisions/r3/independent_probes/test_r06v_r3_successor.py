"""R95-R06V R3 independent successor controls (TEST_ONLY)."""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import sys
import shutil
import subprocess
import tarfile
import tempfile

import pytest

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, ExactRef, StructuralEmpiricalAdmission,
)
from rawlsing_next.pre553_universal_world_binding import (
    R05WorldField, select_joined_world_view, select_r05_world_view,
)
from rawlsing_next.tests.test_universal_world_binding import (
    P41_COMMIT, P41_PACKET, _actual_execution_for,
    _build_r05_learned_inprocess, _joined_request, _persistent_p41_runtime,
    _r05_request, _run_j42_build, _run_r05_p41,
)

REPO_ROOT = Path.cwd()


def _fixture():
    base = Path(tempfile.mkdtemp(prefix="r06v-r3-p41-"))
    archive = base / "p41.tar"
    subprocess.run(
        ["git", "archive", P41_COMMIT, P41_PACKET, "-o", str(archive)],
        cwd=str(REPO_ROOT), check=True, capture_output=True, timeout=180,
    )
    with tarfile.open(archive) as handle:
        handle.extractall(base)
    try:
        receipts = _run_r05_p41(str(base / P41_PACKET / "runtime"))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    return _build_r05_learned_inprocess(), receipts


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:r06v-r3:{tag}", "a" * 64)


def _authority(tag: str) -> AuthorityRef:
    return AuthorityRef(f"FORGED_AUTHORITY_{tag}", "1.0.0", "b" * 64)


def _forged_admission(field: R05WorldField, source_universe_ref: ExactRef):
    return StructuralEmpiricalAdmission(
        typed_state="ADMITTED_FOR_EXACT_STRUCTURAL_USE",
        authority_snapshot_refs=(_authority("snapshot"),),
        dependency_refs=(_ref("EmpiricalFact", "dependency"),),
        producer_replay_locator_or_reference_root=_ref("FORGED_ROOT", "root"),
        admission_decision_state="ADMITTED",
        decision_reason_code="FORGED_DECISION",
        empirical_query_spec_ref=_ref("EmpiricalQuerySpec", "query"),
        empirical_fact_ref=_ref("EmpiricalFact", "fact"),
        admission_authority_ref=_authority("admission"),
        source_universe_refs=(source_universe_ref,),
        native_scope_identity_refs=(_ref("SCOPE", "native"),),
        target_use="STRUCTURAL_MEDIATION_INPUT",
        target_use_permission_refs=(_ref("TARGET_USE_PERMISSION", "permission"),),
        focal_structural_proposition_ref=_ref("PROPOSITION", "focal"),
        structural_semantic_identity_refs=(field.field_ref,),
        effective_time_or_interval_refs_required_by_target_use=(
            _ref("TIME", "effective"),
        ),
        estimand_refs=(_ref("ESTIMAND", "estimand"),),
        measure_and_weight_authority_refs=(_authority("weight"),),
        support_uncertainty_state="SUPPORTED",
        support_uncertainty_refs=(_ref("SUPPORT", "uncertainty"),),
        applicable_negative_denial_noncomparability_refs=(),
        interpretation_critical_authority_refs=(_authority("interpretation"),),
        authority_closure_refs=(_authority("closure"),),
        structural_interpretation_payload={"role": "FORGED_STRUCTURAL_MEANING"},
    )


def _fake_runtime(tmp_path: Path, receipts: dict) -> str:
    root = tmp_path / "forged-runtime"
    (root / "product").mkdir(parents=True)
    (root / "bootstrap.py").write_text("def install():\n    return None\n")
    (root / "product" / "__init__.py").write_text("")
    (root / "product" / "world.py").write_text(
        "class SelectedWorldCatalog:\n"
        "    def __init__(self, empirical, structural_revision=True):\n"
        "        self.empirical = empirical\n"
        "    def select(self, **kwargs):\n"
        "        return {'forged': True}\n"
    )
    (root / "p41_service.py").write_text(
        "import json\n"
        f"RECEIPTS = json.loads({json.dumps(json.dumps(list(receipts.values()))) })\n"
        "_COUNT = [0]\n"
        "class P41Service:\n"
        "    def __init__(self, *args, **kwargs):\n"
        "        pass\n"
        "    def progressive(self, **kwargs):\n"
        "        receipt = RECEIPTS[_COUNT[0] % len(RECEIPTS)]\n"
        "        _COUNT[0] += 1\n"
        "        return receipt\n"
    )
    return str(root)


def test_S1_forged_runtime_cannot_mint_actual_execution(tmp_path):
    data, receipts = _fixture()
    fake = _fake_runtime(tmp_path, receipts)
    execution = _actual_execution_for(data, fake)
    view = select_r05_world_view(
        _r05_request(data, receipts, actual_execution=execution)
    )
    print("S1_REASON", view.state, view.reason_code)
    if fake in sys.path:
        sys.path.remove(fake)
    for name in tuple(sys.modules):
        if name in {"bootstrap", "p41_service"} or name.startswith("product"):
            del sys.modules[name]
    assert view.state == "REFUSED", (
        "a forged P41 runtime returning canned self-consistent receipts was "
        "accepted as authenticated actual execution"
    )


def test_S2_forged_real_type_ff_admission_cannot_authorize_context():
    data, _ = _fixture()
    execution = _actual_execution_for(data, _persistent_p41_runtime())
    fields = _r05_request(data).fields
    promoted = (
        fields[0],
        replace(
            fields[1], role="CONTEXT",
            field_ref=_ref("STRUCTURAL_SEMANTICS", "context-field"),
        ),
    )
    forged = _forged_admission(promoted[1], data["source_universe_ref"])
    view = select_r05_world_view(_r05_request(
        data, fields=promoted, actual_execution=execution,
        ff_structural_admission=forged,
    ))
    print("S2_REASON", view.state, view.reason_code)
    assert view.state == "REFUSED", (
        "an arbitrary real-type StructuralEmpiricalAdmission was accepted as "
        "competent FF structural authority"
    )


def test_S3_subject_selected_coordinator_original_cannot_mint_output():
    data, _ = _fixture()
    execution = replace(
        _actual_execution_for(data, _persistent_p41_runtime()),
        coordinator_original_ref=_ref("FORGED_COORDINATOR_ORIGINAL", "original"),
    )
    view = select_r05_world_view(_r05_request(data, actual_execution=execution))
    if view.state == "R05_WORLD_SELECTED_VIEW":
        assert view.consumer_values_read["coordinator_original_ref"] != (
            execution.coordinator_original_ref.as_dict()
        ), "subject-selected coordinator original was emitted as authenticated"


def test_S4_equal_actual_payload_with_distinct_clocks_refuses():
    data, _ = _fixture()
    execution = _actual_execution_for(
        data, _persistent_p41_runtime(), structural_revision=False,
    )
    fields = (
        R05WorldField(
            "training_access", True, "modeled policy eligibility boolean",
            temporal_expected_value=True,
        ),
        R05WorldField("civil_sanction", False, "modeled policy eligibility boolean"),
    )
    view = select_r05_world_view(_r05_request(
        data, fields=fields, actual_execution=execution,
    ))
    assert view.state == "REFUSED"
    assert view.reason_code == "R05_TEMPORAL_PAIR_NOT_CONSUMED"


def test_S5_genuine_positive_then_hostile_then_restore():
    data, receipts = _fixture()
    runtime = _persistent_p41_runtime()
    base = select_r05_world_view(
        _r05_request(data, actual_execution=_actual_execution_for(data, runtime))
    )
    assert base.state == "R05_WORLD_SELECTED_VIEW"
    assert base.temporal_changed is True
    assert base.consumer_values_read["t0_routes"]["training"] == "ELIGIBLE"
    assert base.consumer_values_read["t1_routes"]["training"] == (
        "BLOCKED_BY_MODELED_RULE"
    )
    hostile = select_r05_world_view(_r05_request(
        data, actual_execution=_actual_execution_for(data, runtime),
        consumer=lambda label: receipts[label],
    ))
    assert hostile.state == "REFUSED"
    assert hostile.reason_code == "CALLER_CALLBACK_NOT_ACCEPTED"
    restored = select_r05_world_view(
        _r05_request(data, actual_execution=_actual_execution_for(data, runtime))
    )
    assert restored.view_hash == base.view_hash


def test_S6_joined_wrapper_forged_real_type_ff_admission_is_not_authority():
    receipts = _run_j42_build()
    fields = _joined_request(receipts).fields
    forged = _forged_admission(
        R05WorldField(
            "civil_sanction", False, "modeled policy eligibility boolean",
            field_ref=_ref("STRUCTURAL_SEMANTICS", "joined-context-field"),
        ),
        _ref("EmpiricalUniverse", "joined-source"),
    )
    view = select_joined_world_view(_joined_request(
        receipts, fields=(fields[0], replace(fields[1], role="CONTEXT")),
        ff_structural_admission=forged,
    ))
    print("S6_REASON", view.state, view.reason_code)
    assert view.state == "REFUSED", (
        "joined wrapper accepted an arbitrary real-type FF admission as a "
        "competent CONTEXT-to-STRUCTURAL authority"
    )
