from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from rawlsing_next import ee_p2x_darwin_court_driver as d


@pytest.fixture(autouse=True)
def _banked_evidence_bytes(monkeypatch):
    monkeypatch.setattr(d, "_git_show_bytes", lambda *args, **kwargs: b"banked-evidence")

    # These are state-machine/driver fixtures, not T3/T4 integration fixtures.
    # The exact process-envelope/accounting seam is covered independently by
    # test_fiabc_t3_oracle_process_envelope.py and test_fiabc_t4_live_accounting.py.
    from rawlsing_next import fiabc_live_accounting_binding as t4

    monkeypatch.setattr(
        t4,
        "admit_live_stage_accounting",
        lambda **kwargs: {
            "schema": t4.LIVE_CONTRACT,
            "classification": "TEST_FIXTURE__DRIVER_MECHANICS_ONLY",
            "semantic_state_modified": False,
        },
    )


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fixture_map(source_sha: str) -> dict:
    evidence = {
        "PREFLIGHT": {"commit": "a" * 40, "path": "e/preflight.json"},
        "LITS_A_FIRST_BUILD": {"commit": "b" * 40, "path": "e/lits_a.json"},
        "LITS_B_CACHELESS_C11": {"commit": "c" * 40, "path": "e/lits_b.json"},
        "WVS_C_FAILURE": {"commit": "d" * 40, "path": "e/wvs_c.json"},
    }
    stop = {
        "PURE_B_NO_CACHE": "Candidate-B has no cache.",
        "WVS_C_PORTABILITY": "WVS-C has no executable fallback.",
    }
    order = [("LITS_I", "A"), ("LITS_I", "B"), ("LITS_I", "C"), ("WVS7", "A"), ("WVS7", "B")]
    next_cell = {
        pair: (
            f"{order[i + 1][0]}/{order[i + 1][1]}/S00_SOURCE_PREFLIGHT_IDENTITY"
            if i + 1 < len(order)
            else "WVS7/C/S01_CANDIDATE_PREPARATION_BUILD"
        )
        for i, pair in enumerate(order)
    }

    def cell(source: str, candidate: str, *, wvs_c: bool = False):
        if wvs_c:
            stages = {
                "S00_SOURCE_PREFLIGHT_IDENTITY": ["DONE__PRESERVE", "PREFLIGHT", False, False, "S01_CANDIDATE_PREPARATION_BUILD"],
                "S01_CANDIDATE_PREPARATION_BUILD": ["TERMINAL_CANDIDATE_LOCAL_FAILURE__PRESERVE", "WVS_C_FAILURE", False, False, "COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION"],
                "S02_C11_REACHABILITY": ["SKIP__NOT_APPLICABLE_BY_FROZEN_LAW", "WVS_C_PORTABILITY", False, False, "COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION"],
                "S03_PARITY_ORACLE_GATE": ["SKIP__NOT_APPLICABLE_BY_FROZEN_LAW", "WVS_C_PORTABILITY", False, False, "COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION"],
            }
            failure_next = "COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION"
        else:
            ev = (
                "LITS_A_FIRST_BUILD"
                if source == "LITS_I" and candidate == "A"
                else "LITS_B_CACHELESS_C11"
                if source == "LITS_I" and candidate == "B"
                else "PREFLIGHT"
            )
            pair = (source, candidate)
            after = next_cell[pair]
            stages = {
                "S00_SOURCE_PREFLIGHT_IDENTITY": ["DONE__PRESERVE", "PREFLIGHT", False, False, "S01_CANDIDATE_PREPARATION_BUILD"],
                "S01_CANDIDATE_PREPARATION_BUILD": ["DONE__PRESERVE", ev, False, False, "S02_C11_REACHABILITY"],
                "S02_C11_REACHABILITY": ["READY__RUN_LOCALLY", None, True, True, "S03_PARITY_ORACLE_GATE"],
                "S03_PARITY_ORACLE_GATE": ["READY__RUN_LOCALLY", None, False, False, after],
            }
            failure_next = after
        return {
            "source": source,
            "candidate": candidate,
            "prerequisite_ref": f"{source}_{candidate}",
            "expected_receipt": f"WORKER_RETURNS/EE-P2X/{source}_{candidate}.json",
            "candidate_local_failure_next": failure_next,
            "stages": stages,
        }

    return {
        "schema": d.CONTINUATION_MAP_SCHEMA,
        "authority": {
            "p2x_branch": d.P2X_BRANCH,
            "p2x_resume_head": d.P2X_RESUME_HEAD,
            "p2r1_pass": d.P2R1_PASS,
            "p2r1_seam_path": d.P2R1_SEAM_PATH,
            "p2r1_seam_blob": d.P2R1_SEAM_BLOB,
        },
        "source_order": ["LITS_I", "WVS7"],
        "candidate_order": ["A", "B", "C"],
        "sources": {
            "LITS_I": {"sha256": source_sha},
            "WVS7": {"sha256": source_sha},
        },
        "evidence": evidence,
        "stop_laws": stop,
        "stage_catalog": ["S00_SOURCE_PREFLIGHT_IDENTITY", "S01_CANDIDATE_PREPARATION_BUILD", "S02_C11_REACHABILITY", "S03_PARITY_ORACLE_GATE"],
        "cells": [
            cell("LITS_I", "A"),
            cell("LITS_I", "B"),
            cell("LITS_I", "C"),
            cell("WVS7", "A"),
            cell("WVS7", "B"),
            cell("WVS7", "C", wvs_c=True),
        ],
        "stage_tuple_schema": [
            "disposition",
            "evidence_or_stop_law_ref",
            "empirical_source_access_required",
            "physical_host_measurement_required",
            "next_stage_on_pass",
        ],
        "entry_guard": {"first_unfinished_court_stage": "LITS_I/A/S02_C11_REACHABILITY"},
        "final_stage": {
            "stage_id": "S17_FINAL_COMPLETENESS_AND_VERIFICATION",
            "expected_outputs": ["WORKER_RETURNS/EE-P2X/final.json"],
            "wake_on_pass": "HQ_MEASURED_SYNTHESIS",
        },
    }


def _machine(tmp_path: Path, data: bytes = b"source"):
    doc = _fixture_map(_sha(data))
    ident = d.MapIdentity(schema=d.CONTINUATION_MAP_SCHEMA, sha256="1" * 64, git_blob_sha1="2" * 40)
    return d.validate_state_machine(doc, ident)


def _host(**changes):
    values = dict(
        implementation="CPython",
        python="3.11.3",
        system="Darwin",
        machine="x86_64",
        dependency_versions={"pyreadstat": "1.3.6", "pyarrow": "25.0.1"},
        ru_maxrss_value=123,
    )
    values.update(changes)
    return d.HostFingerprint(**values)


def _repo():
    return d.RepoFingerprint(
        branch=d.P2X_BRANCH,
        head="f" * 40,
        resume_head_is_ancestor=True,
        p2r1_seam_blob=d.P2R1_SEAM_BLOB,
    )


class Backend:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def run_stage(self, context, services):
        self.calls.append(context.stage.address)
        if callable(self.result):
            return self.result(context)
        if isinstance(self.result, list):
            return self.result.pop(0)
        return self.result


def _driver(tmp_path: Path, machine: d.StateMachine, backend, source_bytes=b"source"):
    lits = tmp_path / "lits.bin"
    wvs = tmp_path / "wvs.bin"
    lits.write_bytes(source_bytes)
    wvs.write_bytes(source_bytes)
    return d.DarwinCourtDriver(
        machine=machine,
        work_root=tmp_path / "work",
        repo_root=tmp_path,
        source_paths={"LITS_I": lits, "WVS7": wvs},
        host=_host(),
        repo=_repo(),
        backend=backend,
    )


def test_runtime_gate_rejects_non_darwin_before_execution():
    with pytest.raises(d.RuntimeGateError, match="runtime gate drift"):
        d.verify_runtime_gate(_host(system="Linux"))


def test_runtime_gate_rejects_non_x86_64():
    with pytest.raises(d.RuntimeGateError, match="runtime gate drift"):
        d.verify_runtime_gate(_host(machine="arm64"))


def test_runtime_gate_rejects_wrong_python():
    with pytest.raises(d.RuntimeGateError, match="runtime gate drift"):
        d.verify_runtime_gate(_host(python="3.11.9"))


def test_runtime_gate_rejects_dependency_drift():
    with pytest.raises(d.RuntimeGateError, match="runtime gate drift"):
        d.verify_runtime_gate(_host(dependency_versions={"pyreadstat": "1.3.5", "pyarrow": "25.0.1"}))


def test_source_and_candidate_order_drift_rejects(tmp_path):
    doc = _fixture_map(_sha(b"source"))
    doc["source_order"] = ["WVS7", "LITS_I"]
    with pytest.raises(d.ContinuationMapError, match="source order drift"):
        d.validate_state_machine(doc, d.MapIdentity(d.CONTINUATION_MAP_SCHEMA, "1" * 64, "2" * 40))


def test_executable_done_preserve_rejects():
    with pytest.raises(d.ContinuationMapError, match="executable DONE__PRESERVE"):
        d._validate_stage_tuple(["DONE__PRESERVE", "PREFLIGHT", True, False, "S01"], address="X")


def test_executable_wvs_c_fallback_rejects(tmp_path):
    doc = _fixture_map(_sha(b"source"))
    doc["cells"][-1]["stages"]["S02_C11_REACHABILITY"] = ["READY__RUN_LOCALLY", None, True, True, "COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION"]
    with pytest.raises(d.ContinuationMapError, match="WVS-C fallback"):
        d.validate_state_machine(doc, d.MapIdentity(d.CONTINUATION_MAP_SCHEMA, "1" * 64, "2" * 40))


def test_source_sha_drift_rejects_before_backend_call(tmp_path):
    machine = _machine(tmp_path, b"authorized")
    backend = Backend(d.BackendResult("PASS", {"ok": True}, verifier_complete=True))
    driver = _driver(tmp_path, machine, backend, source_bytes=b"wrong")
    with pytest.raises(d.RuntimeGateError, match="source SHA drift"):
        driver.run(resume=False)
    assert backend.calls == []


def test_partial_output_without_verifier_remains_incomplete(tmp_path):
    machine = _machine(tmp_path)
    backend = Backend(d.BackendResult("PASS", {"not": "verified"}, verifier_complete=False))
    driver = _driver(tmp_path, machine, backend)
    with pytest.raises(d.StageStateError, match="verifier did not complete"):
        driver.run(resume=False)
    entry = driver.ledger.stage_entry(machine.first_unfinished)
    assert entry["state"] == "RUNNING"
    assert entry["terminal_disposition"] is None


def test_candidate_local_failure_records_and_advances(tmp_path):
    machine = _machine(tmp_path)

    def outcome(context):
        if context.stage.address == machine.first_unfinished:
            return d.BackendResult("CANDIDATE_LOCAL_FAILURE", {"reason": "typed"}, verifier_complete=True)
        return d.BackendResult("PASS", {"ok": True}, verifier_complete=True)

    backend = Backend(outcome)
    driver = _driver(tmp_path, machine, backend)
    result = driver.run(resume=False)
    assert result["status"] == "COURT_SEQUENCE_COMPLETE__S17_VERIFIED"
    entry = driver.ledger.revalidate_terminal(machine.first_unfinished)
    assert entry["terminal_disposition"] == "CANDIDATE_LOCAL_FAILURE"
    propagated = driver.ledger.revalidate_terminal("LITS_I/A/S03_PARITY_ORACLE_GATE")
    assert propagated["terminal_disposition"] == "CANDIDATE_LOCAL_FAILURE"
    assert machine.final_stage_id in backend.calls


def test_common_court_blocker_halts_exact_scope(tmp_path):
    machine = _machine(tmp_path)
    backend = Backend(d.BackendResult("COMMON_COURT_BLOCKER", {"reason": "common"}, verifier_complete=True))
    driver = _driver(tmp_path, machine, backend)
    result = driver.run(resume=False)
    assert result["status"] == "BLOCKED__COMMON_COURT_AUTHORITY"
    entry = driver.ledger.revalidate_terminal(machine.first_unfinished)
    assert entry["terminal_disposition"] == "BLOCKED_BY_COMMON_COURT_AUTHORITY"


def test_valid_completed_stage_resume_reverifies_and_skips(tmp_path):
    machine = _machine(tmp_path)
    backend = Backend(d.BackendResult("PASS", {"ok": True}, verifier_complete=True))
    driver = _driver(tmp_path, machine, backend)
    first = driver.run(resume=False)
    assert first["status"] == "COURT_SEQUENCE_COMPLETE__S17_VERIFIED"
    assert backend.calls[-1] == machine.final_stage_id

    backend2 = Backend(d.BackendResult("PASS", {"should": "not run"}, verifier_complete=True))
    driver2 = _driver(tmp_path, machine, backend2)
    resumed = driver2.run(resume=True)
    assert resumed["status"] == "COURT_SEQUENCE_COMPLETE__S17_VERIFIED"
    assert backend2.calls == []


def test_resume_rejects_receipt_hash_drift(tmp_path):
    machine = _machine(tmp_path)
    backend = Backend(d.BackendResult("PASS", {"ok": True}, verifier_complete=True))
    driver = _driver(tmp_path, machine, backend)
    driver.run(resume=False)
    entry = driver.ledger.stage_entry(machine.first_unfinished)
    receipt = driver.work_root / entry["receipt_path"]
    receipt.write_text("tampered\n", encoding="utf-8")
    driver2 = _driver(tmp_path, machine, Backend(d.BackendResult("PASS", {}, verifier_complete=True)))
    with pytest.raises(d.StageStateError, match="receipt hash drift"):
        driver2.run(resume=True)


def test_second_driver_instance_rejects(tmp_path):
    root = tmp_path / "work"
    with d.DriverInstanceLock(root):
        with pytest.raises(d.RuntimeGateError, match="second EE-P2X"):
            with d.DriverInstanceLock(root):
                pass


def test_exact_owner_deployment_rejects_blob_drift(tmp_path, monkeypatch):
    monkeypatch.setattr(d, "_git_show_bytes", lambda *args, **kwargs: b"not-the-accepted-owner")
    with pytest.raises(d.OwnerDeploymentError, match="owner blob drift"):
        d.load_exact_owner_module("A", repo_root=tmp_path, work_root=tmp_path / "work")


def test_common_source_blocker_propagates_without_executing_blocked_cells(tmp_path):
    machine = _machine(tmp_path)
    driver = _driver(tmp_path, machine, Backend(d.BackendResult("PASS", {}, verifier_complete=True)))
    source_sha = driver.ensure_source_verified("LITS_I")
    nxt = d._mark_source_blocked(
        machine,
        driver.ledger,
        source="LITS_I",
        observed_head=driver.repo.head,
        source_sha256=source_sha,
        blocker_stage="LITS_I/A/S02_C11_REACHABILITY",
    )
    assert nxt == "WVS7/A/S00_SOURCE_PREFLIGHT_IDENTITY"
    blocked = driver.ledger.revalidate_terminal("LITS_I/C/S02_C11_REACHABILITY")
    assert blocked["terminal_disposition"] == "BLOCKED_BY_COMMON_SOURCE_AUTHORITY"


def test_non_source_stage_does_not_receive_private_source_path(tmp_path):
    machine = _machine(tmp_path)
    seen = []

    def outcome(context):
        seen.append((context.stage.address, context.stage.empirical_source_access_required, context.source_path))
        return d.BackendResult("PASS", {"ok": True}, verifier_complete=True)

    driver = _driver(tmp_path, machine, Backend(outcome))
    driver.run(resume=False)
    assert all(path is None for _, needs_source, path in seen if not needs_source)
    assert all(path is not None for _, needs_source, path in seen if needs_source)


def test_wvs_c_preserved_failure_never_opens_source_for_candidate_c(tmp_path, monkeypatch):
    machine = _machine(tmp_path)
    opened = []
    original = d._source_hash_and_size

    def tracking(path):
        opened.append(path.name)
        return original(path)

    monkeypatch.setattr(d, "_source_hash_and_size", tracking)
    driver = _driver(tmp_path, machine, Backend(d.BackendResult("PASS", {"ok": True}, verifier_complete=True)))
    driver.run(resume=False)
    assert opened.count("wvs.bin") == 1
    c = driver.ledger.revalidate_terminal("WVS7/C/S01_CANDIDATE_PREPARATION_BUILD")
    assert c["terminal_disposition"] == "CANDIDATE_LOCAL_FAILURE"


def test_repo_root_output_artifact_is_bound_and_revalidated(tmp_path):
    machine = _machine(tmp_path)
    repo_artifact = tmp_path / "WORKER_RETURNS" / "EE-P2X" / "stage.json"
    repo_artifact.parent.mkdir(parents=True)
    repo_artifact.write_text("{}\n", encoding="utf-8")
    backend = Backend(d.BackendResult("PASS", {"ok": True}, {"stage": repo_artifact}, True))
    driver = _driver(tmp_path, machine, backend)
    driver.run(resume=False)
    entry = driver.ledger.revalidate_terminal(machine.first_unfinished)
    assert any(k.startswith("repo:") for k in entry["output_artifact_hashes"])
    repo_artifact.write_text("tamper\n", encoding="utf-8")
    with pytest.raises(d.StageStateError, match="output artifact hash drift"):
        driver.ledger.revalidate_terminal(machine.first_unfinished)
