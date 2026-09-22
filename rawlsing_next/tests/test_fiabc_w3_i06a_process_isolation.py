from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import types

import pytest

from rawlsing_next.ee_p2x_candidate_process_envelope import (
    BACKEND_CONTRACT,
    FREEZE_RECEIPT_SCHEMA,
    OWNER_MARKER,
    ColdStateViolation,
    CrossCandidateReuseError,
    ForeignCandidateStateError,
    PreStartContaminationError,
    ProcessIsolationController,
    WarmStatePolicyError,
)

REPO = Path(__file__).resolve().parents[2]
PROBE = Path(__file__).with_name("fiabc_i06a_process_probe_backend.py")
SOURCE_SHA = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"


def _freeze(tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "candidate-neutral-freeze.json"
    path.write_text(
        json.dumps(
            {
                "schema": FREEZE_RECEIPT_SCHEMA,
                "candidate_neutral": True,
                "frozen_before_candidate_execution": True,
                "candidate_outputs_seen": 0,
                "candidate_owned_roots_consulted": [],
                "candidate_owned_state_reused": False,
                "state": "FROZEN_READ_ONLY",
                "source_freezes": {
                    "LITS_I": {
                        "source_id": "LITS_I",
                        "canonical_source_sha256": SOURCE_SHA,
                        "source_identity_authority_ref": "HOSTILE_TEST_SOURCE_AUTHORITY",
                        "derivative_identity": None,
                        "derivative_to_source_provenance_ref": None,
                    }
                },
                "authority_identities": {"opaque": "authority-freeze-test"},
                "workload_identities": {"opaque": "workload-freeze-test"},
                "oracle_identities": {
                    "LITS_I": {
                        "oracle_identity_sha256": "5" * 64,
                        "oracle_freeze_authority_ref": "HOSTILE_TEST_ORACLE_FREEZE",
                    }
                },
                "freeze_order": {
                    "source_identity_freeze_sequence": 1,
                    "authority_workload_freeze_sequence": 2,
                    "oracle_materialize_freeze_sequence": 3,
                },
            },
            sort_keys=True,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    return path


def _roots(work: Path, source: str, candidate: str):
    root = work / "cells" / source / candidate
    values = {
        "root": root,
        "scratch": root / "scratch",
        "durable": root / "durable",
        "logs": root / "logs",
        "receipts": root / "receipts",
    }
    for path in values.values():
        path.mkdir(parents=True, exist_ok=True)
    return types.SimpleNamespace(**values)


def _context(
    work: Path,
    candidate: str,
    stage_id: str,
    *,
    next_stage: str,
    roots=None,
):
    roots = roots or _roots(work, "LITS_I", candidate)
    stage = types.SimpleNamespace(
        source="LITS_I",
        candidate=candidate,
        stage_id=stage_id,
        disposition="READY__RUN_LOCALLY",
        evidence_or_stop_law_ref=None,
        empirical_source_access_required=False,
        physical_host_measurement_required=True,
        next_stage_on_pass=next_stage,
        executable_prerequisite="HOSTILE_TEST",
        expected_output_receipt="HOSTILE_TEST",
        next_stage_on_candidate_local_failure="__TEST_STOP__",
        address=f"LITS_I/{candidate}/{stage_id}",
    )
    return types.SimpleNamespace(
        contract=BACKEND_CONTRACT,
        stage=stage,
        work_root=work,
        roots=roots,
        source_path=None,
        source_sha256=SOURCE_SHA,
        map_identity=types.SimpleNamespace(
            schema="HOSTILE_TEST_MAP",
            sha256="1" * 64,
            git_blob_sha1="2" * 40,
        ),
        p2x_branch="HOSTILE_TEST",
        observed_p2x_head="3" * 40,
        input_identity_hash="4" * 64,
    )


def _services(work: Path):
    return types.SimpleNamespace(repo_root=REPO, work_root=work)


def _controller(tmp_path: Path, *, resume_cells=(), warm_transitions=()):
    return ProcessIsolationController(
        backend_spec=str(PROBE),
        freeze_receipt_path=_freeze(tmp_path),
        resume_cells=resume_cells,
        warm_state_transitions=warm_transitions,
        context_mode="SIMPLE_TEST_ONLY",
    )


def _payload(result):
    return result.receipt["stage_payload"]


def test_candidate_a_session_process_and_rss_history_cannot_enter_candidate_b(tmp_path):
    work = tmp_path / "work"
    controller = _controller(
        tmp_path,
        warm_transitions={"PROBE_SET_SESSION>PROBE_ALLOCATE_RSS"},
    )
    services = _services(work)
    try:
        a1 = controller.run_stage(
            _context(work, "A", "PROBE_SET_SESSION", next_stage="LITS_I/A/PROBE_ALLOCATE_RSS"),
            services,
        )
        a2 = controller.run_stage(
            _context(work, "A", "PROBE_ALLOCATE_RSS", next_stage="LITS_I/B/PROBE_SET_SESSION"),
            services,
        )
        b = controller.run_stage(
            _context(work, "B", "PROBE_SET_SESSION", next_stage="LITS_I/C/PROBE_SET_SESSION"),
            services,
        )
    finally:
        controller.close()

    assert _payload(a1)["session_keys_before"] == []
    assert _payload(a2)["session_keys_before"] == ["LITS_I/A"]
    assert _payload(b)["session_keys_before"] == []
    assert _payload(a1)["pid"] == _payload(a2)["pid"]
    assert _payload(a1)["pid"] != _payload(b)["pid"]
    retention = a1.receipt["process_envelope"]["lifecycle_process_retention"]
    assert retention["authorization_token"] == "PROBE_SET_SESSION>PROBE_ALLOCATE_RSS"
    assert retention["authorized"] is True

    a_stop = a2.receipt["process_envelope"]["stop"]
    b_stop = b.receipt["process_envelope"]["stop"]
    assert a_stop["rss_scope"] == "RUSAGE_SELF__THIS_CELL_PROCESS_ONLY"
    assert b_stop["rss_scope"] == "RUSAGE_SELF__THIS_CELL_PROCESS_ONLY"
    assert a_stop["pid"] != b_stop["pid"]
    assert b.receipt["process_envelope"]["process"]["pre_backend_import_resource"]["peak_rss_bytes"] >= 0
    assert "prior_candidate_peak_rss_bytes" not in b.receipt["process_envelope"]


def test_live_candidate_process_cannot_be_reused_for_another_candidate(tmp_path):
    work = tmp_path / "work"
    controller = _controller(
        tmp_path,
        warm_transitions={"PROBE_SET_SESSION>PROBE_LIST_STATE"},
    )
    services = _services(work)
    try:
        controller.run_stage(
            _context(work, "A", "PROBE_SET_SESSION", next_stage="LITS_I/A/PROBE_LIST_STATE"),
            services,
        )
        with pytest.raises(CrossCandidateReuseError):
            controller.run_stage(
                _context(work, "B", "PROBE_SET_SESSION", next_stage="LITS_I/C/PROBE_SET_SESSION"),
                services,
            )
    finally:
        controller.close()




def test_same_cell_process_retention_requires_explicit_lifecycle_authorization(tmp_path):
    work = tmp_path / "work"
    controller = _controller(tmp_path)
    try:
        with pytest.raises(WarmStatePolicyError):
            controller.run_stage(
                _context(
                    work,
                    "A",
                    "PROBE_SET_SESSION",
                    next_stage="LITS_I/A/PROBE_LIST_STATE",
                ),
                _services(work),
            )
    finally:
        controller.close()


def test_scratch_and_durable_state_are_cell_local_and_foreign_marker_fails(tmp_path):
    work = tmp_path / "work"
    controller = _controller(tmp_path)
    services = _services(work)
    try:
        a = controller.run_stage(
            _context(work, "A", "PROBE_WRITE_STATE", next_stage="LITS_I/B/PROBE_LIST_STATE"),
            services,
        )
        b = controller.run_stage(
            _context(work, "B", "PROBE_LIST_STATE", next_stage="LITS_I/C/PROBE_LIST_STATE"),
            services,
        )
    finally:
        controller.close()

    assert "probe-from-A.txt" in _payload(a)["scratch_files_after"]
    assert "probe-from-A.txt" not in _payload(b)["scratch_files_before"]
    assert "probe-from-A.txt" not in _payload(b)["scratch_files_after"]

    c_roots = _roots(work, "LITS_I", "C")
    (c_roots.root / OWNER_MARKER).write_text(
        json.dumps({"cell_key": "LITS_I/A", "state": "STOPPED"}) + "\n",
        encoding="utf-8",
    )
    controller = _controller(tmp_path / "second")
    try:
        with pytest.raises(ForeignCandidateStateError):
            controller.run_stage(
                _context(
                    work,
                    "C",
                    "PROBE_LIST_STATE",
                    next_stage="__COURT_COMPLETE__",
                    roots=c_roots,
                ),
                services,
            )
    finally:
        controller.close()


def test_cold_run_fails_if_candidate_owned_warm_state_already_exists(tmp_path):
    work = tmp_path / "work"
    roots = _roots(work, "LITS_I", "A")
    (roots.durable / "warm-state.bin").write_bytes(b"already warm")
    controller = _controller(tmp_path)
    try:
        with pytest.raises(ColdStateViolation):
            controller.run_stage(
                _context(
                    work,
                    "A",
                    "PROBE_LIST_STATE",
                    next_stage="__COURT_COMPLETE__",
                    roots=roots,
                ),
                _services(work),
            )
    finally:
        controller.close()


def test_same_candidate_warm_state_requires_explicit_resume_hook(tmp_path):
    work = tmp_path / "work"
    roots = _roots(work, "LITS_I", "A")
    (roots.durable / "warm-state.bin").write_bytes(b"lawfully retained")
    (roots.root / OWNER_MARKER).write_text(
        json.dumps({"cell_key": "LITS_I/A", "state": "STOPPED"}) + "\n",
        encoding="utf-8",
    )
    controller = _controller(tmp_path, resume_cells={"LITS_I/A"})
    try:
        result = controller.run_stage(
            _context(
                work,
                "A",
                "PROBE_LIST_STATE",
                next_stage="__COURT_COMPLETE__",
                roots=roots,
            ),
            _services(work),
        )
    finally:
        controller.close()

    cold = result.receipt["process_envelope"]["cold_state_observation"]
    assert cold["start_mode"] == "SAME_CELL_RESUME_EXPLICIT"
    assert cold["candidate_owned_warm_state_present"] is True
    assert "warm-state.bin" in cold["durable_files_before_start"]


def test_candidate_specific_backend_import_before_measurement_start_is_detected(tmp_path):
    work = tmp_path / "work"
    name = "_fiabc_hostile_preimport_probe"
    spec = importlib.util.spec_from_file_location(name, PROBE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    controller = _controller(tmp_path)
    try:
        with pytest.raises(PreStartContaminationError):
            controller.run_stage(
                _context(work, "A", "PROBE_LIST_STATE", next_stage="__COURT_COMPLETE__"),
                _services(work),
            )
    finally:
        controller.close()
        sys.modules.pop(name, None)


def test_candidate_neutral_freeze_is_shared_without_becoming_candidate_state(tmp_path):
    work = tmp_path / "work"
    controller = _controller(tmp_path)
    services = _services(work)
    try:
        a = controller.run_stage(
            _context(work, "A", "PROBE_LIST_STATE", next_stage="LITS_I/B/PROBE_LIST_STATE"),
            services,
        )
        b = controller.run_stage(
            _context(work, "B", "PROBE_LIST_STATE", next_stage="LITS_I/C/PROBE_LIST_STATE"),
            services,
        )
    finally:
        controller.close()

    af = a.receipt["process_envelope"]["candidate_neutral_freeze"]
    bf = b.receipt["process_envelope"]["candidate_neutral_freeze"]
    assert af["receipt_sha256"] == bf["receipt_sha256"]
    assert af["classification"] == "C0_SHARED_UPSTREAM__NOT_CANDIDATE_PRODUCTION_COST"
    assert bf["classification"] == af["classification"]
    assert not Path(af["receipt_path"]).is_relative_to(work / "cells")


def test_descendant_child_process_is_attributable_to_exactly_one_candidate_cell(tmp_path):
    work = tmp_path / "work"
    controller = _controller(tmp_path)
    try:
        result = controller.run_stage(
            _context(work, "A", "PROBE_SPAWN_CHILD", next_stage="__COURT_COMPLETE__"),
            _services(work),
        )
    finally:
        controller.close()

    payload = _payload(result)
    child = payload["child"]
    assert child["cell_key"] == "LITS_I/A"
    assert child["source"] == "LITS_I"
    assert child["candidate"] == "A"
    assert child["ppid"] == payload["pid"]
    assert child["freeze"] == result.receipt["process_envelope"]["candidate_neutral_freeze"]["receipt_sha256"]
    assert result.receipt["process_envelope"]["stage_process_pid"] == payload["pid"]
