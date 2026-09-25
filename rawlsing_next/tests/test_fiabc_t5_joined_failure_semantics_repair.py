from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from rawlsing_next import ee_p2x_candidate_process_envelope as envelope
from rawlsing_next import ee_p2x_darwin_court_driver as driver
from rawlsing_next import fiabc_live_accounting_binding as t4
from rawlsing_next import fiabc_live_terminal_control as t5
from rawlsing_next.pre553_independent_parity_oracle import OracleMismatchError


REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json"

FAILURE_POSITIONS = {
    "S01": "S01_CANDIDATE_PREPARATION_BUILD",
    "BEFORE_S05": "S04_I03_EXECUTION",
    "AT_S05": "S05_I05_LEARNED_PRODUCTION",
    "AFTER_S05": "S10_SOURCE_RELEASE_INVALIDATION",
    "S16": "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS",
}
COMMON_POSITIONS = {
    "EARLY": "S01_CANDIDATE_PREPARATION_BUILD",
    "MIDDLE": "S08_WARM_REPEATED_RESEARCH",
    "LATE": "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS",
}


def _machine():
    return driver.load_current_execution_manifest(MANIFEST)


def _stage(machine, source: str, candidate: str, stage_id: str):
    return machine.get(f"{source}/{candidate}/{stage_id}")


def _all_stage_entries(machine, terminal="PASS"):
    return {
        f"{cell['source']}/{cell['candidate']}/{sid}": {
            "state": "TERMINAL",
            "terminal_disposition": terminal,
        }
        for cell in machine.document["cells"]
        for sid in machine.document["stage_catalog"]
    }


class _ReadLedger:
    def __init__(self, entries):
        self.entries = entries

    def stage_entry(self, address):
        return self.entries.get(address)

    def revalidate_terminal(self, address):
        return self.entries[address]


def _candidate_failure_entries(machine, source, candidate, failed_stage_id):
    entries = _all_stage_entries(machine)
    catalog = list(machine.document["stage_catalog"])
    start = catalog.index(failed_stage_id)
    for sid in catalog[start:]:
        entries[f"{source}/{candidate}/{sid}"]["terminal_disposition"] = (
            "CANDIDATE_LOCAL_FAILURE"
        )
    return entries


@pytest.mark.parametrize("source", ["LITS_I", "WVS7"])
@pytest.mark.parametrize("candidate", ["A", "B", "C"])
@pytest.mark.parametrize("position,stage_id", FAILURE_POSITIONS.items())
def test_candidate_failure_matrix_uses_actual_manifest_and_never_reaches_success_s17(
    source, candidate, position, stage_id, monkeypatch
):
    machine = _machine()
    stage = _stage(machine, source, candidate, stage_id)

    # The current manifest itself can make a requested failure origin impossible.
    # That is still a required matrix row: never invent execution on a preserved/skip stage.
    if stage.disposition != "READY__RUN_LOCALLY":
        assert (source, candidate, position) == ("LITS_I", "B", "S01")
        assert stage.disposition == "DONE__PRESERVE"
        return

    calls = []
    fake = SimpleNamespace(stage_entry=lambda address: None)

    def mechanical(_machine, _ledger, later, _head, _sha, kind, body, next_stage):
        calls.append((later.address, kind, next_stage, body["blocker_stage"]))
        return next_stage, "0" * 64

    monkeypatch.setattr(driver, "_mechanical_terminal", mechanical)
    driver._candidate_stop(
        machine,
        fake,
        source=source,
        candidate=candidate,
        head="f" * 40,
        source_sha=machine.document["sources"][source]["sha256"],
        blocker=stage.address,
    )
    catalog = list(machine.document["stage_catalog"])
    expected_later = catalog[catalog.index(stage_id) + 1 :]
    assert [row[0] for row in calls] == [
        f"{source}/{candidate}/{sid}" for sid in expected_later
    ]
    assert all(row[1] == "CANDIDATE_LOCAL_FAILURE" for row in calls)
    assert all(row[3] == stage.address for row in calls)

    entries = _candidate_failure_entries(machine, source, candidate, stage_id)
    with pytest.raises(driver.CandidateLocalFailure) as caught:
        driver._final_ready(machine, _ReadLedger(entries))
    assert f"{source}/{candidate}" in caught.value.receipt["candidate_failure_cells"]


@pytest.mark.parametrize("source", ["LITS_I", "WVS7"])
@pytest.mark.parametrize("position,stage_id", COMMON_POSITIONS.items())
def test_common_source_blocker_matrix_preserves_source_scope_and_later_source_eligibility(
    source, position, stage_id, monkeypatch
):
    machine = _machine()
    blocker = _stage(machine, source, "A", stage_id)
    ordered = [
        f"{cell['source']}/{cell['candidate']}/{sid}"
        for cell in machine.document["cells"]
        for sid in machine.document["stage_catalog"]
    ]
    blocker_i = ordered.index(blocker.address)
    prior = set(ordered[: blocker_i + 1])
    fake = SimpleNamespace(stage_entry=lambda address: {"terminal": True} if address in prior else None)
    calls = []

    def mechanical(_machine, _ledger, later, _head, _sha, kind, body, next_stage):
        calls.append((later.address, kind, next_stage, body["blocker_stage"]))
        return next_stage, "0" * 64

    monkeypatch.setattr(driver, "_mechanical_terminal", mechanical)
    next_stage = driver._source_stop(
        machine,
        fake,
        source=source,
        head="e" * 40,
        source_sha=machine.document["sources"][source]["sha256"],
        blocker=blocker.address,
    )
    assert calls
    assert all(row[1] == "BLOCKED_BY_COMMON_SOURCE_AUTHORITY" for row in calls)
    assert all(row[3] == blocker.address for row in calls)
    if source == "LITS_I":
        assert next_stage.startswith("WVS7/A/")
    else:
        assert next_stage == machine.final_stage_id

    entries = _all_stage_entries(machine)
    entries[blocker.address]["terminal_disposition"] = "BLOCKED_BY_COMMON_SOURCE_AUTHORITY"
    with pytest.raises(driver.CommonAuthorityBlocker) as caught:
        driver._final_ready(machine, _ReadLedger(entries))
    assert caught.value.scope == "SOURCE"
    assert blocker.address in caught.value.receipt["common_source_blockers"]


@pytest.mark.parametrize("source", ["LITS_I", "WVS7"])
@pytest.mark.parametrize("position,stage_id", COMMON_POSITIONS.items())
def test_common_court_blocker_matrix_remains_court_scope(source, position, stage_id):
    machine = _machine()
    blocker = _stage(machine, source, "A", stage_id)
    entries = _all_stage_entries(machine)
    entries[blocker.address]["terminal_disposition"] = "BLOCKED_BY_COMMON_COURT_AUTHORITY"
    with pytest.raises(driver.CommonAuthorityBlocker) as caught:
        driver._final_ready(machine, _ReadLedger(entries))
    assert caught.value.scope == "COURT"
    assert blocker.address in caught.value.receipt["common_court_blockers"]


def _observation(candidate):
    return {
        "schema": t5.OBSERVATION_SCHEMA,
        "candidate": candidate,
        "observation_identity": candidate.lower() * 64,
    }


@pytest.mark.parametrize("source", ["LITS_I", "WVS7"])
@pytest.mark.parametrize("missing_candidate", ["A", "B"])
@pytest.mark.parametrize("failure_position", ["BEFORE_S05", "AT_S05"])
def test_c_s05_missing_failed_peer_is_typed_source_parity_blocker(
    tmp_path, monkeypatch, source, missing_candidate, failure_position
):
    machine = _machine()
    stage = _stage(machine, source, "C", "S05_I05_LEARNED_PRODUCTION")
    roots = SimpleNamespace(receipts=tmp_path / "cells" / source / "C" / "receipts")
    roots.receipts.mkdir(parents=True)

    other_source = "WVS7" if source == "LITS_I" else "LITS_I"
    # Foreign-source observations must never satisfy C's source-local gate.
    for candidate in ("A", "B", "C"):
        p = t5._cell_receipts_root(tmp_path, other_source, candidate)
        p.mkdir(parents=True, exist_ok=True)
        t5._atomic(p / "fiabc_t5_candidate_observation.json", _observation(candidate))

    for candidate in ("A", "B"):
        if candidate == missing_candidate:
            continue
        p = t5._cell_receipts_root(tmp_path, source, candidate)
        p.mkdir(parents=True, exist_ok=True)
        t5._atomic(p / "fiabc_t5_candidate_observation.json", _observation(candidate))

    oracle = {"oracle_identity_sha256": "9" * 64}
    monkeypatch.setattr(
        t5,
        "load_frozen_source_oracle",
        lambda **kwargs: (oracle, {"workload_identities": {source: {}}}, "8" * 64),
    )
    monkeypatch.setattr(
        t5,
        "validate_candidate_observation",
        lambda _oracle, observation: {
            "status": "PASS__INDEPENDENT_ORACLE_MATCH",
            "candidate": observation["candidate"],
        },
    )
    three_way_called = False

    def forbidden_three_way(*args, **kwargs):
        nonlocal three_way_called
        three_way_called = True
        raise AssertionError("three-way validation may not run with a missing peer")

    monkeypatch.setattr(t5, "validate_three_way_parity", forbidden_three_way)

    result = t5.admit_post_i05_oracle_match(
        stage=stage,
        roots=roots,
        work_root=tmp_path,
        freeze_path=tmp_path / "synthetic-freeze.json",
        backend_receipt={"stage_payload": {"t5_candidate_observation": _observation("C")}},
    )
    assert result["status"] == "NON_PASS"
    assert result["terminal_disposition"] == "COMMON_SOURCE_BLOCKER"
    assert result["kind"] == "PARITY_ORACLE_FAILURE"
    assert result["blocking_scope"] == "SOURCE_ONLY"
    assert result["own_oracle_match_retained"] is True
    assert result["detail"]["missing_candidates"] == [missing_candidate]
    assert three_way_called is False
    assert not (tmp_path / "court" / "t5_oracle" / f"{source}.json").exists()
    assert (roots.receipts / "fiabc_t5_candidate_observation.json").is_file()
    assert (roots.receipts / "fiabc_t5_oracle_match.json").is_file()
    adjudication = json.loads(Path(result["adjudication_path"]).read_text())
    assert adjudication["three_way_parity_claimed"] is False
    assert adjudication["missing_observation_synthesized"] is False
    assert failure_position in {"BEFORE_S05", "AT_S05"}


@pytest.mark.parametrize("source", ["LITS_I", "WVS7"])
def test_c_s05_three_actual_passing_observations_preserve_pass_path(tmp_path, monkeypatch, source):
    machine = _machine()
    stage = _stage(machine, source, "C", "S05_I05_LEARNED_PRODUCTION")
    roots = SimpleNamespace(receipts=tmp_path / "cells" / source / "C" / "receipts")
    roots.receipts.mkdir(parents=True)
    for candidate in ("A", "B"):
        p = t5._cell_receipts_root(tmp_path, source, candidate)
        p.mkdir(parents=True, exist_ok=True)
        t5._atomic(p / "fiabc_t5_candidate_observation.json", _observation(candidate))

    oracle = {"oracle_identity_sha256": "7" * 64}
    monkeypatch.setattr(
        t5, "load_frozen_source_oracle",
        lambda **kwargs: (oracle, {"workload_identities": {source: {}}}, "6" * 64),
    )
    monkeypatch.setattr(
        t5, "validate_candidate_observation",
        lambda _oracle, observation: {"candidate": observation["candidate"], "status": "PASS"},
    )
    monkeypatch.setattr(
        t5, "validate_three_way_parity",
        lambda _oracle, observations: {
            "status": "PASS__A_B_C_MATCH_ONE_FROZEN_CANDIDATE_NEUTRAL_ORACLE",
            "candidates": sorted(observations),
        },
    )
    result = t5.admit_post_i05_oracle_match(
        stage=stage,
        roots=roots,
        work_root=tmp_path,
        freeze_path=tmp_path / "synthetic-freeze.json",
        backend_receipt={"stage_payload": {"t5_candidate_observation": _observation("C")}},
    )
    assert result["status"] == "PASS"
    assert set(result) == {
        "status", "match_receipt_path", "match_receipt_identity",
        "three_way_receipt_identity",
    }
    three = json.loads(
        (tmp_path / "court" / "t5_oracle" / f"{source}.json").read_text()
    )
    assert three["status"] == "PASS"
    assert three["candidates"] == ["A", "B", "C"]


@pytest.mark.parametrize("source", ["LITS_I", "WVS7"])
@pytest.mark.parametrize("candidate", ["A", "B", "C"])
def test_individual_s05_oracle_mismatch_is_candidate_local_typed_failure(
    tmp_path, monkeypatch, source, candidate
):
    machine = _machine()
    stage = _stage(machine, source, candidate, "S05_I05_LEARNED_PRODUCTION")
    roots = SimpleNamespace(receipts=tmp_path / "cells" / source / candidate / "receipts")
    roots.receipts.mkdir(parents=True)
    oracle = {"oracle_identity_sha256": "5" * 64}
    monkeypatch.setattr(
        t5, "load_frozen_source_oracle",
        lambda **kwargs: (oracle, {"workload_identities": {source: {}}}, "4" * 64),
    )

    def mismatch(*args, **kwargs):
        raise OracleMismatchError("frontier_manifest", "FAIL_CLOSED__FULL_FRONTIER_DRIFT")

    monkeypatch.setattr(t5, "validate_candidate_observation", mismatch)
    result = t5.admit_post_i05_oracle_match(
        stage=stage,
        roots=roots,
        work_root=tmp_path,
        freeze_path=tmp_path / "synthetic-freeze.json",
        backend_receipt={"stage_payload": {"t5_candidate_observation": _observation(candidate)}},
    )
    assert result["terminal_disposition"] == "CANDIDATE_LOCAL_FAILURE"
    assert result["kind"] == "PARITY_ORACLE_FAILURE"
    assert result["blocking_scope"] == "CANDIDATE_ONLY"
    assert result["own_oracle_match_retained"] is False
    assert not (roots.receipts / "fiabc_t5_oracle_match.json").exists()


def _accounting_pass(**kwargs):
    return {
        "schema": "FIABC_T4_LIVE_ACCOUNTING_BINDING@1.0.0",
        "semantic_state_modified": False,
        "candidate_neutral_c0_excluded": True,
    }


def _terminal_fixture(tmp_path, source="LITS_I", candidate="C", stage_id="S05_I05_LEARNED_PRODUCTION"):
    machine = _machine()
    repo = tmp_path / "repo"
    work = tmp_path / "work"
    repo.mkdir()
    work.mkdir()
    ledger = driver.StageLedger(work, machine, repo)
    stage = _stage(machine, source, candidate, stage_id)
    result = driver.BackendResult(
        "PASS",
        {
            "stage_payload": {},
            "evidence_artifacts": {},
        },
        {},
        True,
    )
    return machine, repo, work, ledger, stage, result


def test_driver_converts_c_s05_t5_source_nonpass_to_typed_ledger_and_failure_evidence(
    tmp_path, monkeypatch
):
    machine, repo, work, ledger, stage, result = _terminal_fixture(tmp_path)
    monkeypatch.setattr(t4, "admit_live_stage_accounting", _accounting_pass)
    monkeypatch.setenv(driver.FROZEN_UPSTREAM_ENV, str(tmp_path / "freeze.json"))
    monkeypatch.setattr(
        t5,
        "admit_post_i05_oracle_match",
        lambda **kwargs: {
            "status": "NON_PASS",
            "terminal_disposition": "COMMON_SOURCE_BLOCKER",
            "kind": "PARITY_ORACLE_FAILURE",
            "blocking_scope": "SOURCE_ONLY",
            "detail": {"missing_candidates": ["A"]},
            "adjudication_identity": "1" * 64,
            "adjudication_path": str(work / "court" / "adjudication.json"),
            "own_oracle_match_retained": True,
        },
    )
    next_stage, receipt_hash, disposition = driver._backend_terminal(
        machine, ledger, stage, "f" * 40,
        machine.document["sources"][stage.source]["sha256"], result,
    )
    assert disposition == "BLOCKED_BY_COMMON_SOURCE_AUTHORITY"
    assert next_stage == "__COMMON_SOURCE_BLOCKER__"
    entry = ledger.revalidate_terminal(stage.address)
    envelope_doc = json.loads((work / entry["receipt_path"]).read_text())
    assert envelope_doc["terminal_disposition"] == "COMMON_SOURCE_BLOCKER"
    evidence = envelope_doc["measured_payload"]["evidence_artifacts"]
    assert {"cell_receipt", "failure_receipt"} <= set(evidence)
    failure = json.loads((repo / evidence["failure_receipt"]).read_text())
    assert failure["kind"] == "PARITY_ORACLE_FAILURE"
    assert failure["blocking_scope"] == "SOURCE_ONLY"
    assert failure["candidate"] is None
    assert len(receipt_hash) == 64


def test_postbackend_t4_expected_failure_is_typed_common_court_not_untyped(
    tmp_path, monkeypatch
):
    machine, repo, work, ledger, stage, result = _terminal_fixture(
        tmp_path, stage_id="S06_PROVENANCE_AUDIT"
    )

    def accounting_failure(**kwargs):
        raise t4.LiveAccountingError("synthetic governed accounting gap")

    monkeypatch.setattr(t4, "admit_live_stage_accounting", accounting_failure)
    next_stage, _, disposition = driver._backend_terminal(
        machine, ledger, stage, "f" * 40,
        machine.document["sources"][stage.source]["sha256"], result,
    )
    assert disposition == "BLOCKED_BY_COMMON_COURT_AUTHORITY"
    assert next_stage == "__COMMON_COURT_BLOCKER__"
    entry = ledger.revalidate_terminal(stage.address)
    receipt = json.loads((work / entry["receipt_path"]).read_text())
    failure_rel = receipt["measured_payload"]["evidence_artifacts"]["failure_receipt"]
    failure = json.loads((repo / failure_rel).read_text())
    assert failure["kind"] == "COMMON_COURT_AUTHORITY_FAILURE"
    assert failure["blocking_scope"] == "COURT_UNTIL_RESUME"


def test_s16_terminal_qualification_expected_failure_is_candidate_local(
    tmp_path, monkeypatch
):
    machine, repo, work, ledger, stage, result = _terminal_fixture(
        tmp_path, stage_id="S16_TERMINAL_METRIC_VECTOR_COMPLETENESS"
    )
    monkeypatch.setattr(t4, "admit_live_stage_accounting", _accounting_pass)
    monkeypatch.setenv(driver.FROZEN_UPSTREAM_ENV, str(tmp_path / "freeze.json"))

    def seal_failure(**kwargs):
        raise t5.LiveTerminalControlError("synthetic cell-local terminal mismatch")

    monkeypatch.setattr(t5, "seal_live_cell_terminal", seal_failure)
    next_stage, _, disposition = driver._backend_terminal(
        machine, ledger, stage, "f" * 40,
        machine.document["sources"][stage.source]["sha256"], result,
    )
    assert disposition == "CANDIDATE_LOCAL_FAILURE"
    assert next_stage == stage.next_stage_on_candidate_local_failure
    entry = ledger.revalidate_terminal(stage.address)
    receipt = json.loads((work / entry["receipt_path"]).read_text())
    failure_rel = receipt["measured_payload"]["evidence_artifacts"]["failure_receipt"]
    failure = json.loads((repo / failure_rel).read_text())
    assert failure["kind"] == "CANDIDATE_LOCAL_CORRECTNESS_FAILURE"
    assert failure["blocking_scope"] == "CANDIDATE_ONLY"
    assert failure["candidate"] == stage.candidate


def test_unexpected_programming_error_in_post_i05_hook_still_escapes(tmp_path, monkeypatch):
    machine, repo, work, ledger, stage, result = _terminal_fixture(tmp_path)
    monkeypatch.setattr(t4, "admit_live_stage_accounting", _accounting_pass)
    monkeypatch.setenv(driver.FROZEN_UPSTREAM_ENV, str(tmp_path / "freeze.json"))

    def programming_error(**kwargs):
        raise ValueError("not a governed T5 failure class")

    monkeypatch.setattr(t5, "admit_post_i05_oracle_match", programming_error)
    with pytest.raises(ValueError, match="not a governed"):
        driver._backend_terminal(
            machine, ledger, stage, "f" * 40,
            machine.document["sources"][stage.source]["sha256"], result,
        )


def test_pass_s05_driver_envelope_shape_and_transition_remain_unchanged(tmp_path, monkeypatch):
    machine, repo, work, ledger, stage, result = _terminal_fixture(tmp_path)
    monkeypatch.setattr(t4, "admit_live_stage_accounting", _accounting_pass)
    monkeypatch.setenv(driver.FROZEN_UPSTREAM_ENV, str(tmp_path / "freeze.json"))
    pass_gate = {
        "status": "PASS",
        "match_receipt_path": "synthetic",
        "match_receipt_identity": "2" * 64,
        "three_way_receipt_identity": "3" * 64,
    }
    monkeypatch.setattr(t5, "admit_post_i05_oracle_match", lambda **kwargs: dict(pass_gate))
    next_stage, _, disposition = driver._backend_terminal(
        machine, ledger, stage, "f" * 40,
        machine.document["sources"][stage.source]["sha256"], result,
    )
    assert disposition == "PASS"
    assert next_stage == stage.next_stage_on_pass
    entry = ledger.revalidate_terminal(stage.address)
    receipt = json.loads((work / entry["receipt_path"]).read_text())
    assert receipt["terminal_disposition"] == "PASS"
    assert receipt["measured_payload"]["t5_oracle_match"] == pass_gate
    assert "postbackend_failure_adjudication" not in receipt["measured_payload"]


def test_outer_nonpass_gracefully_stops_retained_same_cell_process(monkeypatch):
    controller = object.__new__(envelope.ProcessIsolationController)
    controller._active = SimpleNamespace(cell_key="LITS_I/C")
    calls = []
    monkeypatch.setattr(controller, "_stop", lambda reason: calls.append(reason) or {"op": "STOPPED"})
    stopped = controller.stop_after_outer_nonpass(
        source="LITS_I", candidate="C", reason="T5_SOURCE_BLOCKER"
    )
    assert stopped == {"op": "STOPPED"}
    assert calls == ["T5_SOURCE_BLOCKER"]

    controller._active = SimpleNamespace(cell_key="LITS_I/A")
    with pytest.raises(envelope.CrossCandidateReuseError):
        controller.stop_after_outer_nonpass(
            source="LITS_I", candidate="C", reason="WRONG_CELL"
        )


def test_driver_requires_retained_s05_process_stop_after_outer_nonpass():
    stage = SimpleNamespace(
        stage_id="S05_I05_LEARNED_PRODUCTION",
        address="LITS_I/C/S05_I05_LEARNED_PRODUCTION",
    )

    class Good:
        def stop_after_outer_nonpass(self, stage, reason):
            return {"status": "STOPPED", "reason": reason}

    assert driver._stop_backend_after_posthook_nonpass(
        Good(), stage, "PASS", "BLOCKED_BY_COMMON_SOURCE_AUTHORITY"
    )["status"] == "STOPPED"

    class Bad:
        def stop_after_outer_nonpass(self, stage, reason):
            return None

    with pytest.raises(driver.StageExecutionError, match="expected a retained"):
        driver._stop_backend_after_posthook_nonpass(
            Bad(), stage, "PASS", "BLOCKED_BY_COMMON_SOURCE_AUTHORITY"
        )


def test_final_nonpass_receipt_never_fabricates_s17_success_or_terminal_bundle(tmp_path):
    machine = _machine()
    obj = object.__new__(driver.DarwinCourtDriver)
    obj.machine = machine
    obj.work_root = tmp_path
    obj.repo = SimpleNamespace(head="d" * 40)
    path = obj._write_final_nonpass(
        status="COURT_SEQUENCE_COMPLETE__CANDIDATE_LOCAL_FAILURES_RECORDED__S17_SUCCESS_VERIFIER_NOT_RUN",
        terminal_disposition="CANDIDATE_LOCAL_FAILURE",
        detail={"candidate_failure_cells": ["LITS_I/A"]},
        next_stage="__COURT_COMPLETE__",
    )
    receipt = json.loads(path.read_text())
    assert receipt["schema"] == "RAWLSING_FIABC_T5_LIVE_FINAL_NONPASS@1.0.0"
    assert receipt["s17_success_backend_invoked"] is False
    assert receipt["s17_success_claimed"] is False
    assert receipt["six_cell_pass_claimed"] is False
    assert receipt["terminal_bundle_fabricated"] is False
    assert receipt["missing_success_evidence_synthesized"] is False


def test_process_isolation_pass_law_is_not_weakened_by_outer_stop_hook():
    import inspect

    source = inspect.getsource(envelope.ProcessIsolationController.run_stage)
    assert 'must_stop = source == "COURT" or terminal != "PASS" or not same_cell_next' in source
    assert "warm_transition_authorized" in source
    assert "CrossCandidateReuseError" in inspect.getsource(
        envelope.ProcessIsolationController.stop_after_outer_nonpass
    )
