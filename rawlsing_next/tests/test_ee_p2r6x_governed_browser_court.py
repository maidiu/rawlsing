from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


TOOL_PATH = (
    Path(__file__).resolve().parents[2]
    / "WORKER_RETURNS"
    / "EE-P2R6X"
    / "03_RECONCILE_LOCAL_P2X_INFRASTRUCTURE_STOPS.py"
)
SPEC = importlib.util.spec_from_file_location("ee_p2r6x_reconciler", TOOL_PATH)
assert SPEC is not None and SPEC.loader is not None
r6x = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r6x)


def _render(value) -> bytes:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False).encode() + b"\n"


def _write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_render(value))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _receipt_entry(
    work: Path,
    *,
    address: str,
    source: str,
    candidate: str,
    stage_id: str,
    next_stage: str,
    receipt,
):
    receipt_path = work / "cells" / source / candidate / "receipts" / (stage_id.lower() + ".json")
    _write_json(receipt_path, receipt)
    return {
        "stage_id": stage_id,
        "source": source,
        "candidate": candidate,
        "input_identity_hash": "synthetic-" + hashlib.sha256(address.encode()).hexdigest(),
        "state": "TERMINAL",
        "output_artifact_hashes": {},
        "receipt_path": receipt_path.relative_to(work).as_posix(),
        "receipt_hash": _sha(receipt_path),
        "verifier_completion": True,
        "terminal_disposition": "CANDIDATE_LOCAL_FAILURE",
        "next_stage": next_stage,
    }


def _preserved(stage_id: str, source: str, candidate: str, next_stage: str):
    return {
        "stage_id": stage_id,
        "source": source,
        "candidate": candidate,
        "input_identity_hash": "preserved-" + stage_id,
        "state": "TERMINAL",
        "output_artifact_hashes": {},
        "receipt_path": f"synthetic-preserved/{source}/{candidate}/{stage_id}.json",
        "receipt_hash": "a" * 64,
        "verifier_completion": True,
        "terminal_disposition": "PRESERVED",
        "next_stage": next_stage,
    }


def _failure_doc(spec):
    return {
        "schema": "RAWLSING_EE_P2X_FAILURE_STOP_RECEIPT@1.0.0",
        "source": spec["source"],
        "candidate": spec["candidate"],
        "kind": "CANDIDATE_LOCAL_CORRECTNESS_FAILURE",
        "blocking_scope": "CANDIDATE_ONLY",
        "disposition": (
            f"EE_P2X_{spec['source']}_{spec['candidate']}_{spec['stage_id']}"
            "__CANDIDATE_LOCAL_CORRECTNESS_FAILURE"
        ),
        "evidence_paths": [
            f"WORKER_RETURNS/EE-P2X/LOCAL_COURT/cells/{spec['source']}__{spec['candidate']}.json",
            spec["failure_path"],
        ],
        "later_lawful_cells_suppressed": False,
        "ranking_or_selection": False,
        "synthetic_fallback_used": False,
        "backend_detail": {
            "exception_type": spec["exception_type"],
            "exception": spec["exception"],
        },
    }


def _build_fixture(tmp_path: Path, monkeypatch):
    work = tmp_path / "work"
    repo = tmp_path / "repo"
    work.mkdir()
    repo.mkdir()

    stages = {}

    # Lawful prefix that must survive byte-for-byte.
    stages["LITS_I/A/S00_SOURCE_PREFLIGHT_IDENTITY"] = _preserved(
        "S00_SOURCE_PREFLIGHT_IDENTITY", "LITS_I", "A", "LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD"
    )
    stages["LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD"] = _preserved(
        "S01_CANDIDATE_PREPARATION_BUILD", "LITS_I", "A", "LITS_I/A/S02_C11_REACHABILITY"
    )
    for sid, nxt in (
        ("S00_SOURCE_PREFLIGHT_IDENTITY", "LITS_I/B/S01_CANDIDATE_PREPARATION_BUILD"),
        ("S01_CANDIDATE_PREPARATION_BUILD", "LITS_I/B/S02_C11_REACHABILITY"),
        ("S02_C11_REACHABILITY", "LITS_I/B/S03_PARITY_ORACLE_GATE"),
    ):
        stages[f"LITS_I/B/{sid}"] = _preserved(sid, "LITS_I", "B", nxt)

    # Legitimate C states are opaque to this repair and must be untouched.
    for source in ("LITS_I", "WVS7"):
        for sid in r6x.STAGE_CATALOG:
            stages[f"{source}/C/{sid}"] = {
                "stage_id": sid,
                "source": source,
                "candidate": "C",
                "state": "TERMINAL",
                "terminal_disposition": (
                    "CANDIDATE_LOCAL_FAILURE" if sid == "S01_CANDIDATE_PREPARATION_BUILD"
                    else "SKIPPED_BY_FROZEN_LAW"
                ),
                "verifier_completion": True,
                "receipt_path": f"c-preserved/{source}/{sid}.json",
                "receipt_hash": "c" * 64,
                "output_artifact_hashes": {},
                "next_stage": r6x.S17 if source == "WVS7" else "WVS7/A/S00_SOURCE_PREFLIGHT_IDENTITY",
                "input_identity_hash": "c-" + sid,
            }

    for spec in r6x.BLOCKERS:
        address = spec["address"]
        blocker_receipt = {
            "schema": "RAWLSING_EE_P2X_DARWIN_STAGE_RECEIPT_ENVELOPE@1.0.0",
            "stage": address,
            "terminal_disposition": "CANDIDATE_LOCAL_FAILURE",
            "input_identity_hash": "synthetic",
            "backend_contract": "RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0",
            "measured_payload": {
                "error": "synthetic governed infrastructure stop",
                "detail": {
                    "exception_type": spec["exception_type"],
                    "exception": spec["exception"],
                },
            },
        }
        stages[address] = _receipt_entry(
            work,
            address=address,
            source=spec["source"],
            candidate=spec["candidate"],
            stage_id=spec["stage_id"],
            next_stage=spec["next_stage"],
            receipt=blocker_receipt,
        )
        start = r6x.STAGE_CATALOG.index(spec["stage_id"]) + 1
        for sid in r6x.STAGE_CATALOG[start:]:
            later = f"{spec['source']}/{spec['candidate']}/{sid}"
            prop_receipt = {
                "schema": "RAWLSING_EE_P2X_CANDIDATE_LOCAL_STOP_PROPAGATION@1.0.0",
                "stage": later,
                "blocker_stage": address,
                "input_identity_hash": "synthetic",
                "execution_performed": False,
                "measurement_performed": False,
            }
            stages[later] = _receipt_entry(
                work,
                address=later,
                source=spec["source"],
                candidate=spec["candidate"],
                stage_id=sid,
                next_stage=spec["next_stage"],
                receipt=prop_receipt,
            )

    stages[r6x.S17] = {
        "stage_id": "S17_FINAL_COMPLETENESS_AND_VERIFICATION",
        "source": "COURT",
        "candidate": "ALL",
        "input_identity_hash": "synthetic-s17",
        "state": "RUNNING",
        "output_artifact_hashes": {},
        "receipt_path": None,
        "receipt_hash": None,
        "verifier_completion": False,
        "terminal_disposition": None,
        "next_stage": None,
    }

    ledger = {
        "schema": r6x.LEDGER_SCHEMA,
        "continuation_map": {
            "schema": r6x.CONTINUATION_MAP_SCHEMA,
            "sha256": r6x.CONTINUATION_MAP_SHA256,
            "git_blob_sha1": r6x.CONTINUATION_MAP_GIT_BLOB_SHA1,
        },
        "p2x_branch": "agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1",
        "p2x_resume_head": "a954e2d6676843da8427ef2439b5d1ef33478359",
        "source_order": ["LITS_I", "WVS7"],
        "candidate_order": ["A", "B", "C"],
        "source_identities": {
            "LITS_I": {"sha256": "lits-source", "size": 111},
            "WVS7": {"sha256": "wvs-source", "size": 222},
        },
        "stages": stages,
    }
    ledger_path = work / "ee_p2x_stage_ledger.json"
    _write_json(ledger_path, ledger)
    ledger_sha = _sha(ledger_path)
    monkeypatch.setattr(r6x, "EXPECTED_LEDGER_SHA256", ledger_sha)

    for spec in r6x.BLOCKERS:
        _write_json(repo / spec["failure_path"], _failure_doc(spec))

    _write_json(
        repo / r6x.FINAL_VERIFY_RECEIPT,
        {
            "schema": "RAWLSING_EE_P2X_DRIVER_BOUND_FINAL_VERIFICATION@1.0.0",
            "driver_ledger_sha256": ledger_sha,
            "terminal": "BLOCKER__DRIVER_STAGE_RUNNING__COURT__S17_FINAL_COMPLETENESS_AND_VERIFICATION",
        },
    )
    return_path = repo / r6x.P2X_RETURN
    return_path.parent.mkdir(parents=True, exist_ok=True)
    return_path.write_text(
        "driver-bound final verification failed\n"
        "ValueError: 'COURT/ALL' is not in list\n"
        "BLOCKER__DRIVER_STAGE_RUNNING__COURT__S17_FINAL_COMPLETENESS_AND_VERIFICATION\n",
        encoding="utf-8",
    )

    # Exact mutable cleanup roots. Durable carriers other than backend state are
    # deliberately present to prove they are not deleted.
    for source, candidate in [
        *((x["source"], x["candidate"]) for x in r6x.BLOCKERS),
        ("COURT", "ALL"),
    ]:
        root = work / "cells" / source / candidate
        _write_json(
            root / "durable" / "ee_p2x_backend_state.json",
            {
                "schema": r6x.BACKEND_STATE_SCHEMA,
                "source": source,
                "candidate": candidate,
                "source_sha256": "synthetic",
            },
        )
        (root / "durable" / "preserved_transformed_carrier.bin").write_bytes(b"KEEP-DURABLE")
        (root / "scratch").mkdir(parents=True, exist_ok=True)
        (root / "scratch" / "failed-attempt.tmp").write_bytes(b"DROP-SCRATCH")

    # C scratch and completely external carriers must survive.
    c_keep = work / "cells" / "LITS_I" / "C" / "scratch" / "keep.txt"
    c_keep.parent.mkdir(parents=True, exist_ok=True)
    c_keep.write_bytes(b"KEEP-C")
    source_carrier = tmp_path / "source-carrier-do-not-touch.bin"
    source_carrier.write_bytes(b"FROZEN-SOURCE-CARRIER")

    return {
        "work": work,
        "repo": repo,
        "ledger_path": ledger_path,
        "ledger_before": copy.deepcopy(ledger),
        "ledger_sha": ledger_sha,
        "c_keep": c_keep,
        "source_carrier": source_carrier,
        "source_carrier_sha": _sha(source_carrier),
    }


def _removed_addresses():
    removed = []
    for spec in r6x.BLOCKERS:
        removed.append(spec["address"])
        start = r6x.STAGE_CATALOG.index(spec["stage_id"]) + 1
        removed.extend(
            f"{spec['source']}/{spec['candidate']}/{sid}"
            for sid in r6x.STAGE_CATALOG[start:]
        )
    removed.append(r6x.S17)
    return removed


def test_exact_stopped_shape_rewinds_only_infrastructure_stops(tmp_path, monkeypatch):
    fx = _build_fixture(tmp_path, monkeypatch)
    before = fx["ledger_before"]
    removed = set(_removed_addresses())
    preserved_before = {
        a: json.dumps(e, sort_keys=True, separators=(",", ":"))
        for a, e in before["stages"].items()
        if a not in removed
    }
    c_before = {
        a: copy.deepcopy(e)
        for a, e in before["stages"].items()
        if a.startswith("LITS_I/C/") or a.startswith("WVS7/C/")
    }

    result = r6x.reconcile(fx["work"], fx["repo"])

    assert result["status"] == "RECONCILED"
    assert result["before_ledger_sha256"] == fx["ledger_sha"]
    assert result["next_stage_after_reconciliation"] == r6x.FIRST_REOPENED_STAGE
    assert set(result["removed_stage_addresses"]) == removed
    assert len(removed) == 62

    after = json.loads(fx["ledger_path"].read_text())
    assert after["source_identities"] == before["source_identities"]
    assert after["continuation_map"] == before["continuation_map"]
    for address in removed:
        assert address not in after["stages"]
    for address, encoded in preserved_before.items():
        assert json.dumps(after["stages"][address], sort_keys=True, separators=(",", ":")) == encoded
    assert {
        a: e for a, e in after["stages"].items()
        if a.startswith("LITS_I/C/") or a.startswith("WVS7/C/")
    } == c_before

    for source, candidate in [
        *((x["source"], x["candidate"]) for x in r6x.BLOCKERS),
        ("COURT", "ALL"),
    ]:
        root = fx["work"] / "cells" / source / candidate
        assert not (root / "durable" / "ee_p2x_backend_state.json").exists()
        assert not (root / "scratch").exists()
        assert (root / "durable" / "preserved_transformed_carrier.bin").read_bytes() == b"KEEP-DURABLE"

    assert fx["c_keep"].read_bytes() == b"KEEP-C"
    assert _sha(fx["source_carrier"]) == fx["source_carrier_sha"]
    assert (fx["work"] / r6x.RECONCILIATION_RECEIPT_NAME).is_file()


def test_unrelated_ledger_drift_fails_closed_before_mutation(tmp_path, monkeypatch):
    fx = _build_fixture(tmp_path, monkeypatch)
    doc = json.loads(fx["ledger_path"].read_text())
    doc["unrelated_drift"] = True
    _write_json(fx["ledger_path"], doc)
    state = fx["work"] / "cells" / "LITS_I" / "A" / "durable" / "ee_p2x_backend_state.json"

    with pytest.raises(r6x.ReconciliationError, match="pre-reconciliation ledger SHA-256 mismatch"):
        r6x.reconcile(fx["work"], fx["repo"])
    assert state.is_file()


def test_wrong_exception_identity_refuses_reconciliation(tmp_path, monkeypatch):
    fx = _build_fixture(tmp_path, monkeypatch)
    spec = r6x.BLOCKERS[0]
    failure_path = fx["repo"] / spec["failure_path"]
    doc = json.loads(failure_path.read_text())
    doc["backend_detail"]["exception"] = "different failure"
    _write_json(failure_path, doc)
    state = fx["work"] / "cells" / "LITS_I" / "A" / "durable" / "ee_p2x_backend_state.json"

    with pytest.raises(r6x.ReconciliationError, match="governed exception identity drift"):
        r6x.reconcile(fx["work"], fx["repo"])
    assert state.is_file()
    assert _sha(fx["ledger_path"]) == fx["ledger_sha"]


def test_orphan_s17_must_be_exact_running_shape(tmp_path, monkeypatch):
    fx = _build_fixture(tmp_path, monkeypatch)
    doc = json.loads(fx["ledger_path"].read_text())
    doc["stages"][r6x.S17]["state"] = "TERMINAL"
    _write_json(fx["ledger_path"], doc)
    monkeypatch.setattr(r6x, "EXPECTED_LEDGER_SHA256", _sha(fx["ledger_path"]))
    final = json.loads((fx["repo"] / r6x.FINAL_VERIFY_RECEIPT).read_text())
    final["driver_ledger_sha256"] = r6x.EXPECTED_LEDGER_SHA256
    _write_json(fx["repo"] / r6x.FINAL_VERIFY_RECEIPT, final)

    with pytest.raises(r6x.ReconciliationError, match="S17 orphan identity drift"):
        r6x.reconcile(fx["work"], fx["repo"])


def test_audit_only_on_stopped_ledger_is_non_mutating(tmp_path, monkeypatch):
    fx = _build_fixture(tmp_path, monkeypatch)
    ledger_bytes = fx["ledger_path"].read_bytes()
    state = fx["work"] / "cells" / "WVS7" / "A" / "durable" / "ee_p2x_backend_state.json"

    result = r6x.reconcile(fx["work"], fx["repo"], audit_only=True)

    assert result["status"] == "AUDIT_ONLY__READY"
    assert fx["ledger_path"].read_bytes() == ledger_bytes
    assert state.is_file()
    assert not (fx["work"] / r6x.RECONCILIATION_RECEIPT_NAME).exists()


def test_second_mutating_invocation_refuses_but_audit_only_accepts(tmp_path, monkeypatch):
    fx = _build_fixture(tmp_path, monkeypatch)
    first = r6x.reconcile(fx["work"], fx["repo"])
    assert first["status"] == "RECONCILED"

    with pytest.raises(r6x.ReconciliationError, match="pre-reconciliation ledger SHA-256 mismatch"):
        r6x.reconcile(fx["work"], fx["repo"])

    audited = r6x.reconcile(fx["work"], fx["repo"], audit_only=True)
    assert audited["status"] == "AUDIT_ONLY__ALREADY_RECONCILED"
    assert audited["ledger_sha256"] == first["after_ledger_sha256"]


def test_propagation_must_link_to_exact_blocker(tmp_path, monkeypatch):
    fx = _build_fixture(tmp_path, monkeypatch)
    spec = r6x.BLOCKERS[2]
    later = f"{spec['source']}/{spec['candidate']}/S02_C11_REACHABILITY"
    ledger = json.loads(fx["ledger_path"].read_text())
    entry = ledger["stages"][later]
    receipt = fx["work"] / entry["receipt_path"]
    receipt_doc = json.loads(receipt.read_text())
    receipt_doc["blocker_stage"] = "WVS7/A/WRONG_BLOCKER"
    _write_json(receipt, receipt_doc)
    entry["receipt_hash"] = _sha(receipt)
    _write_json(fx["ledger_path"], ledger)
    monkeypatch.setattr(r6x, "EXPECTED_LEDGER_SHA256", _sha(fx["ledger_path"]))
    final = json.loads((fx["repo"] / r6x.FINAL_VERIFY_RECEIPT).read_text())
    final["driver_ledger_sha256"] = r6x.EXPECTED_LEDGER_SHA256
    _write_json(fx["repo"] / r6x.FINAL_VERIFY_RECEIPT, final)

    with pytest.raises(r6x.ReconciliationError, match="does not link to exact blocker"):
        r6x.reconcile(fx["work"], fx["repo"])
