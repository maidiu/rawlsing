from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from rawlsing_next import ee_p2x_darwin_court_driver as driver

REPO = Path(__file__).resolve().parents[2]
P2X = REPO / "WORKER_RETURNS" / "EE-P2X"
BINDING = json.loads((P2X / "10B_DARWIN_DRIVER_RECEIPT_BINDING.json").read_text(encoding="utf-8"))

spec = importlib.util.spec_from_file_location(
    "ee_p2x_driver_bound_verify",
    P2X / "12A_verify_ee_p2x_driver_bound_local_court.py",
)
bridge = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(bridge)


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _base_ledger():
    reducer = json.loads((REPO / BINDING["continuation_map"]["path"]).read_text(encoding="utf-8"))
    return {
        "schema": BINDING["driver"]["ledger_schema"],
        "continuation_map": {
            "schema": BINDING["continuation_map"]["schema"],
            "sha256": BINDING["continuation_map"]["sha256"],
            "git_blob_sha1": BINDING["continuation_map"]["git_blob_sha1"],
        },
        "p2x_branch": BINDING["hq_authority"]["p2x_branch"],
        "p2x_resume_head": reducer["authority"]["p2x_resume_head"],
        "source_order": reducer["source_order"],
        "candidate_order": reducer["candidate_order"],
        "source_identities": {},
        "stages": {},
    }


def _write_stage(work: Path, ledger: dict, *, address: str, ledger_disposition: str, receipt: dict):
    source, candidate, sid = address.split("/")
    rel = f"cells/{source}/{candidate}/receipts/{sid.lower()}.json"
    path = work / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(receipt, indent=2, sort_keys=True).encode() + b"\n"
    path.write_bytes(data)
    ledger["stages"][address] = {
        "stage_id": sid,
        "source": source,
        "candidate": candidate,
        "input_identity_hash": receipt["input_identity_hash"],
        "state": "TERMINAL",
        "output_artifact_hashes": {},
        "receipt_path": rel,
        "receipt_hash": hashlib.sha256(data).hexdigest(),
        "verifier_completion": True,
        "terminal_disposition": ledger_disposition,
        "next_stage": receipt.get("_next_stage", "LITS_I/A/S02_C11_REACHABILITY"),
    }
    receipt.pop("_next_stage", None)
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ledger["stages"][address]["receipt_hash"] = bridge.sha256_file(path)


def _write_ledger(work: Path, ledger: dict):
    work.mkdir(parents=True, exist_ok=True)
    (work / "ee_p2x_stage_ledger.json").write_text(
        json.dumps(ledger, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_original_compatible_proposal_blobs_are_preserved_exactly():
    expected = {
        "09_LOCAL_COURT_FROZEN_EXPECTATIONS.json": "1e336d0c7700997819876d6a5faa65389baf5dc3",
        "10_LOCAL_COURT_RECEIPT_CONTRACT.json": "7e729e6934fea270bf7d180faeeec33877e89fcf",
        "10A_COURT_RUN_MANIFEST_CONTRACT.json": "2d2293171167317338c39c57b848bec33e5f8aac",
        "11_seed_ee_p2x_local_receipts.py": "694d751fcb4cbaf59250532ce1261c25fcc4b9e1",
        "12_verify_ee_p2x_local_court.py": "4394bb61beba08259349cac3afbfa599f9f1a9aa",
        "13_WVS7_C_PRESERVED_PORTABILITY_FAILURE.json": "15cc59fe96c00a7178e0d9c318903e64c9e1d118",
    }
    assert {name: git_blob_sha1(P2X / name) for name in expected} == expected


def test_binding_is_exactly_the_qualified_driver_and_adopted_map():
    assert git_blob_sha1(REPO / BINDING["driver"]["path"]) == BINDING["driver"]["git_blob_sha1"]
    map_path = REPO / BINDING["continuation_map"]["path"]
    assert git_blob_sha1(map_path) == BINDING["continuation_map"]["git_blob_sha1"]
    assert bridge.sha256_file(map_path) == BINDING["continuation_map"]["sha256"]
    assert driver.LEDGER_SCHEMA == BINDING["driver"]["ledger_schema"]
    assert driver.BACKEND_CONTRACT == BINDING["driver"]["backend_contract"]
    assert driver.SUPERVISOR_TOKEN_SCHEMA == BINDING["driver"]["supervisor_token_schema"]


def test_binding_covers_every_actual_driver_cli_mode():
    parser = driver._parser()
    options = {x for action in parser._actions for x in action.option_strings}
    assert set(BINDING["driver"]["cli_modes"]) <= options
    assert {"--preflight", "--status", "--run", "--resume", "--verify-only"} <= options


def test_reducer_law_is_consumed_without_inventing_transitions():
    reducer, laws, physical, order = bridge._map_law(BINDING)
    assert reducer["entry_guard"]["first_unfinished_court_stage"] == BINDING["continuation_map"]["first_unfinished_stage"]
    assert order[-1] == BINDING["continuation_map"]["final_stage"]
    assert laws["LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD"] == "DONE__PRESERVE"
    assert laws["LITS_I/B/S02_C11_REACHABILITY"] == "DONE__PRESERVE"
    assert laws["WVS7/C/S01_CANDIDATE_PREPARATION_BUILD"] == "TERMINAL_CANDIDATE_LOCAL_FAILURE__PRESERVE"
    assert laws["WVS7/C/S02_C11_REACHABILITY"] == "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW"
    assert physical["WVS7/C/S01_CANDIDATE_PREPARATION_BUILD"] is False


def test_actual_preserved_receipt_schema_is_accepted_without_execution(tmp_path):
    work = tmp_path / "work"
    ledger = _base_ledger()
    address = "LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD"
    _write_stage(
        work,
        ledger,
        address=address,
        ledger_disposition="PRESERVED",
        receipt={
            "schema": BINDING["driver"]["stage_receipt_schemas"]["preserved_stage"],
            "stage": address,
            "input_identity_hash": "1" * 64,
            "evidence_ref": "LITS_A_FIRST_BUILD",
            "evidence": {"commit": "0" * 40, "path": "banked.json"},
            "evidence_sha256": "2" * 64,
            "evidence_git_blob_sha1": "3" * 40,
            "source_access_performed": False,
            "execution_performed": False,
            "measurement_performed": False,
        },
    )
    _write_ledger(work, ledger)
    _, _, _, info, _ = bridge.validate_driver_ledger(work, allow_incomplete=True)
    assert info[address]["kind"] == "preserved"


def test_backend_envelope_on_done_preserve_is_rejected(tmp_path):
    work = tmp_path / "work"
    ledger = _base_ledger()
    address = "LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD"
    _write_stage(
        work,
        ledger,
        address=address,
        ledger_disposition="PASS",
        receipt={
            "schema": BINDING["driver"]["stage_receipt_schemas"]["backend_envelope"],
            "stage": address,
            "backend_contract": BINDING["driver"]["backend_contract"],
            "terminal_disposition": "PASS",
            "input_identity_hash": "4" * 64,
            "measured_payload": {"evidence_artifacts": {}},
        },
    )
    _write_ledger(work, ledger)
    with pytest.raises(bridge.DriverBindingBlocker, match="BACKEND_EXECUTION_OF_NONEXECUTABLE_STAGE"):
        bridge.validate_driver_ledger(work, allow_incomplete=True)


def test_driver_specific_common_court_blocker_is_explicit_extension():
    ext = BINDING["driver_specific_failure_extension"]
    assert ext == {
        "kind": "COMMON_COURT_AUTHORITY_FAILURE",
        "driver_backend_disposition": "COMMON_COURT_BLOCKER",
        "ledger_disposition": "BLOCKED_BY_COMMON_COURT_AUTHORITY",
        "normalized_blocking_scope": "COURT_UNTIL_RESUME",
        "law": ext["law"],
    }
    assert BINDING["driver"]["backend_to_ledger_disposition"]["COMMON_COURT_BLOCKER"] == ext["ledger_disposition"]


def test_ready_stage_next_transition_is_exact_and_drift_rejects(tmp_path):
    work = tmp_path / "work"
    ledger = _base_ledger()
    address = "LITS_I/A/S03_PARITY_ORACLE_GATE"
    _write_stage(
        work,
        ledger,
        address=address,
        ledger_disposition="PASS",
        receipt={
            "schema": BINDING["driver"]["stage_receipt_schemas"]["backend_envelope"],
            "stage": address,
            "backend_contract": BINDING["driver"]["backend_contract"],
            "terminal_disposition": "PASS",
            "input_identity_hash": "5" * 64,
            "measured_payload": {"evidence_artifacts": {}},
            "_next_stage": "LITS_I/A/S04_I03_EXECUTION",
        },
    )
    _write_ledger(work, ledger)
    _, _, _, info, _ = bridge.validate_driver_ledger(work, allow_incomplete=True)
    assert info[address]["kind"] == "backend"

    ledger["stages"][address]["next_stage"] = "LITS_I/B/S00_SOURCE_PREFLIGHT_IDENTITY"
    _write_ledger(work, ledger)
    with pytest.raises(bridge.DriverBindingBlocker, match="NEXT_STAGE_DRIFT"):
        bridge.validate_driver_ledger(work, allow_incomplete=True)


def test_driver_payload_rejects_ranking_or_selection_surface(tmp_path):
    work = tmp_path / "work"
    ledger = _base_ledger()
    address = "LITS_I/A/S03_PARITY_ORACLE_GATE"
    _write_stage(
        work,
        ledger,
        address=address,
        ledger_disposition="PASS",
        receipt={
            "schema": BINDING["driver"]["stage_receipt_schemas"]["backend_envelope"],
            "stage": address,
            "backend_contract": BINDING["driver"]["backend_contract"],
            "terminal_disposition": "PASS",
            "input_identity_hash": "6" * 64,
            "measured_payload": {"evidence_artifacts": {}, "winner": "A"},
            "_next_stage": "LITS_I/A/S04_I03_EXECUTION",
        },
    )
    _write_ledger(work, ledger)
    with pytest.raises(bridge.DriverBindingBlocker, match="FORBIDDEN_DRIVER_OUTPUT_SURFACE"):
        bridge.validate_driver_ledger(work, allow_incomplete=True)


def test_common_scope_failures_are_candidate_neutral_for_reuse():
    source = BINDING["common_scope_normalization"]["common_source"]
    court = BINDING["common_scope_normalization"]["common_court"]
    assert source["candidate"] is None
    assert source["blocking_scope"] == "SOURCE_ONLY"
    assert set(source["permitted_failure_kinds"]) == {
        "COMMON_SOURCE_AUTHORITY_FAILURE",
        "PARITY_ORACLE_FAILURE",
    }
    assert court["candidate"] is None
    assert court["blocking_scope"] == "COURT_UNTIL_RESUME"
    assert court["permitted_failure_kinds"] == ["COMMON_COURT_AUTHORITY_FAILURE"]
