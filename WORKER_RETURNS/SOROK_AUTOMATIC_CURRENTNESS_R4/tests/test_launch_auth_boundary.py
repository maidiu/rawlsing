"""Focused R4 tests for launcher proof and actual-session binding."""
from __future__ import annotations
import json, shutil, sys
from pathlib import Path
import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROGRAMMA = ROOT / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK"
sys.path.insert(0, str(PROGRAMMA))
import operational_currentness_runtime_r1 as rt
import test_operational_currentness_runtime_r1 as t


def test_launcher_proof_requires_exact_path_hash_and_token(tmp_path):
    identity = rt._launcher_identity()
    spec = {"run_dir": str(tmp_path / "run"), "job_id": "x", "session": "s"}
    token = rt._launcher_token(spec)
    good = {"path": identity["path"], "sha256": identity["sha256"],
            "token": token}
    rt._verify_launcher_proof(spec, good)

    copy = tmp_path / "launch.py"
    shutil.copy2(identity["path"], copy)
    with pytest.raises(rt.CurrentnessError, match="LAUNCHER_PATH_MISMATCH"):
        rt._verify_launcher_proof(spec, {**good, "path": str(copy)})
    with pytest.raises(rt.CurrentnessError, match="LAUNCHER_HASH_MISMATCH"):
        rt._verify_launcher_proof(spec, {**good, "sha256": "0" * 64})
    with pytest.raises(rt.CurrentnessError, match="LAUNCHER_TOKEN_MISMATCH"):
        rt._verify_launcher_proof(spec, {**good, "token": "0" * 64})
    other = rt._launcher_token({**spec, "session": "different"})
    with pytest.raises(rt.CurrentnessError, match="LAUNCHER_TOKEN_MISMATCH"):
        rt._verify_launcher_proof(spec, {**good, "token": other})


def test_existing_enrollment_cannot_be_replayed(tmp_path):
    config = t.make_sandbox(tmp_path)
    run, _w, _art = t.make_controller_run(
        tmp_path / "repo", job_id="replay-enroll", role="IMPLEMENTER",
        task_id=rt.MECHANISM_ID)
    config = t.enroll_test_run(config, run)
    with pytest.raises(rt.CurrentnessError,
                       match="TRUSTED_LAUNCH_ALREADY_ENROLLED"):
        rt.enroll_existing_run(config, run, "test-enroll-1")
    with pytest.raises(rt.CurrentnessError,
                       match="TRUSTED_LAUNCH_ALREADY_MIGRATED"):
        rt.enroll_existing_run(config, run, "test-enroll-1",
                               migrate_existing=True)


def test_unsigned_operator_cannot_enroll(tmp_path):
    config = t.make_sandbox(tmp_path)
    run, _w, _art = t.make_controller_run(
        tmp_path / "repo", job_id="unsigned-enroll", role="IMPLEMENTER",
        task_id=rt.MECHANISM_ID)
    auth_path = Path(config["_state_root"]) / "unsigned_operator.json"
    auth = {
        "schema": rt.OPERATOR_AUTH_SCHEMA, "authorization_id": "unsigned",
        "role": "SOROK_HQ_OPERATOR", "owner": "test", "granted_by": "TEST_ONLY",
        "granted_at_utc": rt.now_utc(), "expires_at_utc": rt._utc_add(3600),
        "allowed_kinds": ["TRUSTED_LAUNCH_ENROLLMENT"],
        "allowed_scopes": ["TRUSTED_LAUNCH_ENROLLMENT"],
        "allowed_source_digests": [], "allowed_item_digests": [],
        "allowed_supersedes": [],
    }
    auth_path.write_text(json.dumps(auth) + "\n")
    cp = Path(config["_root"]) / "config.json"
    data = json.loads(cp.read_text()); data["trusted_operator_authorization"] = str(auth_path)
    cp.write_text(json.dumps(data) + "\n")
    config = rt.load_config(cp)
    with pytest.raises(rt.CurrentnessError,
                       match="OPERATOR_AUTHORIZATION_SIGNATURE_REQUIRED"):
        rt.enroll_existing_run(config, run, "unsigned")


def test_enrollment_rejects_actual_expected_session_mismatch(tmp_path):
    config = t.make_sandbox(tmp_path)
    receipt = json.loads((ROOT / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/"
                          "reviewer_original/REVIEW_RECEIPT.json").read_text())
    run, _w, _art = t.make_controller_run(
        tmp_path / "repo", job_id="fake-session-trust", role="REVIEWER",
        task_id=rt.MECHANISM_ID, return_schema=rt.REVIEW_RECEIPT_SCHEMA,
        return_payload=receipt, session="ses_FAKE_ATTEST",
        expected_session=receipt["reviewer_session"],
        expected_source_commit=receipt["implementation_commit"])
    with pytest.raises(rt.CurrentnessError,
                       match="TRUSTED_LAUNCH_ACTUAL_SESSION_MISMATCH"):
        t.enroll_test_run(config, run)


def test_review_expected_source_must_match_receipt(tmp_path):
    config = t.make_sandbox(tmp_path)
    receipt = json.loads((ROOT / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/"
                          "reviewer_original/REVIEW_RECEIPT.json").read_text())
    run, _w, _art = t.make_controller_run(
        tmp_path / "repo", job_id="fake-source-receipt", role="REVIEWER",
        task_id=rt.MECHANISM_ID, return_schema=rt.REVIEW_RECEIPT_SCHEMA,
        return_payload=receipt, session=receipt["reviewer_session"],
        expected_session=receipt["reviewer_session"],
        expected_source_commit="f" * 40)
    config = t.enroll_test_run(config, run)
    source = rt._make_return_event(config, run)["source"]
    source["trust"] = "REAL_LOCAL_SUPERVISED_REVIEW_RUN"
    source["review_run_dir"] = str(run)
    with pytest.raises(rt.CurrentnessError,
                       match="REVIEW_RUN_SOURCE_MISMATCH"):
        rt._validate_review_receipt(config, receipt, replay=False, source=source)


def test_review_receipt_session_must_match_actual_run(tmp_path):
    config = t.make_sandbox(tmp_path)
    receipt = json.loads((ROOT / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/"
                          "reviewer_original/REVIEW_RECEIPT.json").read_text())
    run, _w, _art = t.make_controller_run(
        tmp_path / "repo", job_id="fake-session-receipt", role="REVIEWER",
        task_id=rt.MECHANISM_ID, return_schema=rt.REVIEW_RECEIPT_SCHEMA,
        return_payload=receipt, session="ses_FAKE_ATTEST",
        expected_session="ses_FAKE_ATTEST",
        expected_source_commit=receipt["implementation_commit"])
    config = t.enroll_test_run(config, run)
    source = rt._make_return_event(config, run)["source"]
    source["trust"] = "REAL_LOCAL_SUPERVISED_REVIEW_RUN"
    source["review_run_dir"] = str(run)
    with pytest.raises(rt.CurrentnessError,
                       match="REVIEW_RUN_ACTUAL_SESSION_MISMATCH"):
        rt._validate_review_receipt(config, receipt, replay=False, source=source)
