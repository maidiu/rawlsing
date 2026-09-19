from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import rawlsing_next.ee_p2x_darwin_court_driver as driver
import rawlsing_next.ee_p2x_darwin_stage_backend as backend


FINAL = "COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION"
EXPECTED_VERIFIER_BLOB = "da8f3434f791c9f6495238b28817de4b3e328ad3"


class FakeLedger:
    def __init__(self, work_root: Path, repo_root: Path, entries=None):
        self.work_root = work_root
        self.repo_root = repo_root
        self.entries = dict(entries or {})
        self.data = {"stages": self.entries}
        self.begin_calls = []
        self.complete_calls = []
        self.discard_calls = []

    def stage_entry(self, address):
        return self.entries.get(address)

    def begin(self, stage, ih):
        self.begin_calls.append(stage.address)
        self.entries[stage.address] = {
            "stage_id": stage.stage_id,
            "source": stage.source,
            "candidate": stage.candidate,
            "input_identity_hash": ih,
            "state": "RUNNING",
            "output_artifact_hashes": {},
            "receipt_path": None,
            "receipt_hash": None,
            "verifier_completion": False,
            "terminal_disposition": None,
            "next_stage": None,
        }

    def discard_empty_running_preterminal(self, stage):
        old = self.entries.get(stage.address)
        assert old is not None and old["state"] == "RUNNING"
        assert old["terminal_disposition"] is None
        assert old["receipt_path"] is None and old["receipt_hash"] is None
        assert old["output_artifact_hashes"] == {}
        self.discard_calls.append(stage.address)
        del self.entries[stage.address]

    def complete(self, stage, **kw):
        self.complete_calls.append(stage.address)
        self.entries[stage.address] = {
            "stage_id": stage.stage_id,
            "source": stage.source,
            "candidate": stage.candidate,
            "input_identity_hash": kw["input_identity_hash"],
            "state": "TERMINAL",
            "output_artifact_hashes": dict(kw["output_artifact_hashes"]),
            "receipt_path": str(kw["receipt_path"].relative_to(self.work_root)),
            "receipt_hash": driver._sha256_file(kw["receipt_path"]),
            "verifier_completion": kw["verifier_complete"],
            "terminal_disposition": kw["terminal_disposition"],
            "next_stage": kw["next_stage"],
        }

    def revalidate_terminal(self, address):
        e = self.entries[address]
        assert e["state"] == "TERMINAL"
        return e

    def hash(self):
        return "f" * 64


class FakeMachine:
    def __init__(self, stage: driver.StageSpec, *, final=FINAL, document=None):
        self.first_unfinished = stage.address
        self.final_stage_id = final
        self.identity = driver.MapIdentity("TEST", "a" * 64, "b" * 40)
        self.document = document or {"sources": {}}
        self._stages = {stage.address: stage}

    def get(self, address):
        return self._stages[address]


class InspectingBackend:
    def __init__(self, ledger: FakeLedger, address: str, *, expected_state):
        self.ledger = ledger
        self.address = address
        self.expected_state = expected_state
        self.observed = None

    def run_stage(self, context, services):
        entry = self.ledger.stage_entry(self.address)
        self.observed = None if entry is None else entry.get("state")
        assert self.observed == self.expected_state
        return driver.BackendResult(
            "PASS",
            {"schema": "TEST_BODY", "evidence_artifacts": {}, "ranking_or_selection": False},
            verifier_complete=True,
        )


def _bare_driver(tmp_path: Path, stage: driver.StageSpec, ledger: FakeLedger, runtime_backend, *, final=FINAL):
    d = object.__new__(driver.DarwinCourtDriver)
    d.machine = FakeMachine(stage, final=final)
    d.work_root = tmp_path / "work"
    d.repo_root = tmp_path
    d.source_paths = {}
    d.host = None
    d.repo = SimpleNamespace(head="1" * 40)
    d.backend = runtime_backend
    d.ledger = ledger
    d.services = driver.DriverServices(repo_root=tmp_path, work_root=d.work_root)
    d.verify_static_gates = lambda: None
    d.bind_initial_preserved_prefix = lambda: None
    d.source_sha_for_stage = lambda _stage: "2" * 64
    return d


def test_s17_backend_runs_with_no_s17_entry_then_driver_terminalizes(monkeypatch, tmp_path):
    stage = driver.StageSpec(
        "COURT", "ALL", "S17_FINAL_COMPLETENESS_AND_VERIFICATION",
        "READY__RUN_LOCALLY", None, False, False, "__COURT_COMPLETE__",
        "ALL_S00_S16_TERMINAL", "FINAL", "__FORBIDDEN__",
    )
    ledger = FakeLedger(tmp_path / "work", tmp_path)
    runtime_backend = InspectingBackend(ledger, FINAL, expected_state=None)
    d = _bare_driver(tmp_path, stage, ledger, runtime_backend)

    final_ready_calls = []
    monkeypatch.setattr(
        driver,
        "_final_ready",
        lambda machine, observed: (
            final_ready_calls.append(True),
            observed.stage_entry(FINAL) is None or pytest.fail("S17 existed before backend"),
        ),
    )

    result = d.run(resume=True)

    assert final_ready_calls == [True]
    assert runtime_backend.observed is None
    assert ledger.begin_calls == []
    assert ledger.complete_calls == [FINAL]
    assert ledger.stage_entry(FINAL)["state"] == "TERMINAL"
    assert ledger.stage_entry(FINAL)["terminal_disposition"] == "PASS"
    assert result["status"] == "COURT_SEQUENCE_COMPLETE__S17_VERIFIED"


def test_non_s17_ready_stage_still_begins_before_backend(tmp_path):
    stage = driver.StageSpec(
        "LITS_I", "A", "S04_I03_EXECUTION",
        "READY__RUN_LOCALLY", None, False, False, "__COURT_COMPLETE__",
        "READY", "I03", "__CANDIDATE_STOP__",
    )
    ledger = FakeLedger(tmp_path / "work", tmp_path)
    runtime_backend = InspectingBackend(ledger, stage.address, expected_state="RUNNING")
    d = _bare_driver(tmp_path, stage, ledger, runtime_backend, final=FINAL)

    result = d.run(resume=True)

    assert ledger.begin_calls == [stage.address]
    assert runtime_backend.observed == "RUNNING"
    assert ledger.complete_calls == [stage.address]
    assert result["status"] == "COURT_SEQUENCE_COMPLETE__S17_VERIFIED"


def test_only_empty_legacy_running_s17_placeholder_is_discardable(tmp_path):
    stage = driver.StageSpec(
        "COURT", "ALL", "S17_FINAL_COMPLETENESS_AND_VERIFICATION",
        "READY__RUN_LOCALLY", None, False, False, "__COURT_COMPLETE__",
        "READY", "FINAL", "__FORBIDDEN__",
    )
    ledger = object.__new__(driver.StageLedger)
    ledger.path = tmp_path / "ledger.json"
    ledger.data = {"stages": {
        FINAL: {
            "state": "RUNNING",
            "terminal_disposition": None,
            "receipt_path": None,
            "receipt_hash": None,
            "output_artifact_hashes": {},
        }
    }}

    ledger.discard_empty_running_preterminal(stage)
    assert FINAL not in ledger.data["stages"]

    ledger.data["stages"][FINAL] = {
        "state": "RUNNING",
        "terminal_disposition": None,
        "receipt_path": None,
        "receipt_hash": None,
        "output_artifact_hashes": {"work:evidence.json": "a" * 64},
    }
    with pytest.raises(driver.StageStateError, match="evidenced running stage"):
        ledger.discard_empty_running_preterminal(stage)


def test_final_ready_requires_every_reducer_stage_terminal_and_wvsc_failure():
    catalog = ("S00_SOURCE_PREFLIGHT_IDENTITY", "S01_CANDIDATE_PREPARATION_BUILD", "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS")
    cells = [
        {"source": "LITS_I", "candidate": "A"},
        {"source": "WVS7", "candidate": "C"},
    ]
    machine = SimpleNamespace(document={"cells": cells, "stage_catalog": catalog})
    entries = {}
    for cell in cells:
        for sid in catalog:
            address = f"{cell['source']}/{cell['candidate']}/{sid}"
            entries[address] = {
                "state": "TERMINAL",
                "terminal_disposition": "PASS",
                "verifier_completion": True,
            }
    entries["WVS7/C/S01_CANDIDATE_PREPARATION_BUILD"]["terminal_disposition"] = "CANDIDATE_LOCAL_FAILURE"

    ledger = SimpleNamespace(
        stage_entry=lambda a: entries.get(a),
        revalidate_terminal=lambda a: entries[a],
    )
    driver._final_ready(machine, ledger)

    missing = "LITS_I/A/S16_TERMINAL_METRIC_VECTOR_COMPLETENESS"
    saved = entries.pop(missing)
    with pytest.raises(driver.StageStateError, match="nonterminal reducer stage"):
        driver._final_ready(machine, ledger)
    entries[missing] = saved

    entries["WVS7/C/S01_CANDIDATE_PREPARATION_BUILD"]["terminal_disposition"] = "PASS"
    with pytest.raises(driver.StageStateError, match="WVS-C portability failure not bound"):
        driver._final_ready(machine, ledger)


def test_s17_common_court_failure_is_candidate_neutral_and_never_calls_cell_serializer(monkeypatch, tmp_path):
    stage = SimpleNamespace(
        source="COURT",
        candidate="ALL",
        stage_id="S17_FINAL_COMPLETENESS_AND_VERIFICATION",
        address=FINAL,
    )
    ctx = SimpleNamespace(stage=stage, input_identity_hash="3" * 64)
    services = SimpleNamespace(repo_root=tmp_path)

    monkeypatch.setattr(
        backend,
        "_write_cell",
        lambda *a, **k: pytest.fail("candidate-cell serializer invoked for COURT/ALL"),
    )

    result = backend._failure(
        ctx,
        services,
        {},
        backend.CourtAuthorityStop("final verifier blocked", {"terminal": "BLOCKER__TEST"}),
    )

    assert result["terminal_disposition"] == "COMMON_COURT_BLOCKER"
    assert set(result["receipt"]["evidence_artifacts"]) == {"cell_receipt", "failure_receipt"}
    court_path = tmp_path / result["receipt"]["evidence_artifacts"]["cell_receipt"]
    failure_path = tmp_path / result["receipt"]["evidence_artifacts"]["failure_receipt"]
    court = json.loads(court_path.read_text())
    failure = json.loads(failure_path.read_text())
    assert court["schema"] == "RAWLSING_EE_P2X_COMMON_COURT_SCOPE_RECEIPT@1.0.0"
    assert court["candidate"] is None and court["candidate_neutral"] is True
    assert failure["candidate"] is None
    assert failure["kind"] == "COMMON_COURT_AUTHORITY_FAILURE"
    assert failure["blocking_scope"] == "COURT_UNTIL_RESUME"
    assert "COURT/ALL" not in failure_path.as_posix()


def test_any_s17_backendstop_is_normalized_to_common_court_not_candidate_local(monkeypatch, tmp_path):
    roots = SimpleNamespace(durable=tmp_path / "durable", scratch=tmp_path / "scratch")
    stage = SimpleNamespace(
        source="COURT",
        candidate="ALL",
        stage_id="S17_FINAL_COMPLETENESS_AND_VERIFICATION",
        address=FINAL,
        disposition="READY__RUN_LOCALLY",
        empirical_source_access_required=False,
    )
    ctx = SimpleNamespace(
        contract=backend.BACKEND_CONTRACT,
        stage=stage,
        roots=roots,
        work_root=tmp_path / "work",
        source_path=None,
        source_sha256="4" * 64,
        input_identity_hash="5" * 64,
    )
    services = SimpleNamespace(repo_root=tmp_path)

    def fail_gate(_ctx):
        raise backend.BackendStop("synthetic candidate-style backend failure")

    monkeypatch.setattr(backend, "_gate", fail_gate)
    result = backend.run_stage(ctx, services)

    assert result["terminal_disposition"] == "COMMON_COURT_BLOCKER"
    failure = json.loads((tmp_path / result["receipt"]["evidence_artifacts"]["failure_receipt"]).read_text())
    assert failure["candidate"] is None
    assert failure["kind"] == "COMMON_COURT_AUTHORITY_FAILURE"


def test_external_verify_only_revalidates_terminal_s17(tmp_path):
    ledger = FakeLedger(tmp_path / "work", tmp_path, {
        FINAL: {
            "stage_id": "S17_FINAL_COMPLETENESS_AND_VERIFICATION",
            "source": "COURT",
            "candidate": "ALL",
            "state": "TERMINAL",
            "terminal_disposition": "PASS",
            "verifier_completion": True,
            "next_stage": "__COURT_COMPLETE__",
        }
    })
    seen = []
    ledger.revalidate_terminal = lambda address: seen.append(address) or ledger.entries[address]

    d = object.__new__(driver.DarwinCourtDriver)
    d.ledger = ledger
    d.next_stage = lambda: "__COURT_COMPLETE__"

    out = d.verify_only()
    assert seen == [FINAL]
    assert out["status"] == "PASS"
    assert out["terminal_stages_reverified"] == 1
    assert out["next_stage"] == "__COURT_COMPLETE__"


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def test_strict_driver_bound_verifier_is_unchanged_and_rebound_to_repaired_driver():
    repo = Path(__file__).resolve().parents[2]
    verifier_path = repo / "WORKER_RETURNS/EE-P2X/12A_verify_ee_p2x_driver_bound_local_court.py"
    driver_path = repo / "rawlsing_next/ee_p2x_darwin_court_driver.py"
    binding_path = repo / "WORKER_RETURNS/EE-P2X/10B_DARWIN_DRIVER_RECEIPT_BINDING.json"

    binding = json.loads(binding_path.read_text())
    verifier_source = verifier_path.read_text()

    assert _git_blob(verifier_path.read_bytes()) == EXPECTED_VERIFIER_BLOB
    assert binding["driver"]["git_blob_sha1"] == _git_blob(driver_path.read_bytes())
    assert binding["backend_measured_payload_bridge"]["required_roles"]["ANY_BACKEND_TERMINAL_FAILURE"] == [
        "cell_receipt", "failure_receipt"
    ]
    assert binding["common_scope_normalization"]["common_court"] == {
        "backend_disposition": "COMMON_COURT_BLOCKER",
        "permitted_failure_kinds": ["COMMON_COURT_AUTHORITY_FAILURE"],
        "blocking_scope": "COURT_UNTIL_RESUME",
        "candidate": None,
        "law": "A common-court authority failure is candidate-neutral and terminates the court until resume; the driver-bound verifier short-circuits before the legacy normalized verifier.",
    }
    assert "S17 may be absent while this verifier is itself running as the S17 backend." in verifier_source
    assert 'if address.startswith("COURT/"):' in verifier_source


def test_real_s17_handler_is_invoked_while_s17_absent_then_driver_terminalizes(monkeypatch, tmp_path):
    stage = driver.StageSpec(
        "COURT", "ALL", "S17_FINAL_COMPLETENESS_AND_VERIFICATION",
        "READY__RUN_LOCALLY", None, False, False, "__COURT_COMPLETE__",
        "ALL_S00_S16_TERMINAL", "FINAL", "__FORBIDDEN__",
    )
    work = tmp_path / "work"
    repo = Path(__file__).resolve().parents[2]
    ledger = FakeLedger(work, repo)
    subprocess_calls = []

    def fake_run(argv, **kwargs):
        assert ledger.stage_entry(FINAL) is None
        subprocess_calls.append(tuple(str(x) for x in argv))
        return SimpleNamespace(returncode=0, stdout="PASS__FINAL_TWO_SOURCE_P2_EVIDENCE_COMPLETE\n")

    monkeypatch.setattr(backend.subprocess, "run", fake_run)
    monkeypatch.setattr(
        driver,
        "_final_ready",
        lambda machine, observed: (
            observed.stage_entry(FINAL) is None
            or pytest.fail("S17 existed before the production verifier handler")
        ),
    )

    class ProductionS17Handler:
        def run_stage(self, context, services):
            payload = backend._s17(context, services, {})
            assert payload["terminal"] == "PASS__FINAL_TWO_SOURCE_P2_EVIDENCE_COMPLETE"
            return driver.BackendResult(
                "PASS",
                {"schema": "TEST_REAL_S17_HANDLER", "terminal": payload["terminal"], "evidence_artifacts": {}},
                verifier_complete=True,
            )

    d = object.__new__(driver.DarwinCourtDriver)
    d.machine = FakeMachine(stage)
    d.work_root = work
    d.repo_root = repo
    d.source_paths = {}
    d.host = None
    d.repo = SimpleNamespace(head="1" * 40)
    d.backend = ProductionS17Handler()
    d.ledger = ledger
    d.services = driver.DriverServices(repo_root=repo, work_root=work)
    d.verify_static_gates = lambda: None
    d.bind_initial_preserved_prefix = lambda: None
    d.source_sha_for_stage = lambda _stage: "2" * 64

    out = d.run(resume=True)

    assert len(subprocess_calls) == 1
    assert subprocess_calls[0][1].endswith("WORKER_RETURNS/EE-P2X/12A_verify_ee_p2x_driver_bound_local_court.py")
    assert "--driver-work-root" in subprocess_calls[0]
    assert ledger.begin_calls == []
    assert ledger.complete_calls == [FINAL]
    assert ledger.stage_entry(FINAL)["terminal_disposition"] == "PASS"
    assert out["status"] == "COURT_SEQUENCE_COMPLETE__S17_VERIFIED"
