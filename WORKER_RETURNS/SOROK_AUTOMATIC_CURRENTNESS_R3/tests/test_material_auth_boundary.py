"""Focused R3 tests for trusted material-event admission."""
from __future__ import annotations
import json, os, sys
from pathlib import Path
import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROGRAMMA = ROOT / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK"
sys.path.insert(0, str(PROGRAMMA))
import operational_currentness_runtime_r1 as rt
import test_operational_currentness_runtime_r1 as t


def operator_auth(config, *, kinds, scopes, aid="ops-control-1"):
    path = Path(config["_state_root"]) / "operator_control_authorization.json"
    path.write_text(json.dumps({
        "schema": rt.OPERATOR_AUTH_SCHEMA, "authorization_id": aid,
        "role": "SOROK_HQ_OPERATOR", "owner": "test HQ operator",
        "granted_by": "TEST_ONLY", "granted_at_utc": rt.now_utc(),
        "expires_at_utc": rt._utc_add(3600), "allowed_kinds": list(kinds),
        "allowed_scopes": list(scopes), "allowed_source_digests": [],
        "allowed_item_digests": [], "allowed_supersedes": []}) + "\n")
    cp = Path(config["_root"]) / "config.json"
    data = json.loads(cp.read_text()); data["trusted_operator_authorization"] = str(path)
    cp.write_text(json.dumps(data) + "\n")
    return rt.load_config(cp)


def test_public_material_events_are_denied_by_default(tmp_path):
    config = t.make_sandbox(tmp_path)
    cases = {
        "REJECTION": "UNTRUSTED_REJECTION_SOURCE",
        "PROTECTED_INTEGRATION": "UNTRUSTED_PROTECTED_INTEGRATION_SOURCE",
        "GITHUB_OBSERVATION": "LIVE_GITHUB_OBSERVATION_UNTRUSTED_SOURCE",
        "USER_STOP": "OPERATOR_AUTHORIZATION_UNAVAILABLE",
    }
    for kind, code in cases.items():
        with pytest.raises(rt.CurrentnessError, match=code):
            rt.intake_event(config, t.event(kind, payload={}))
    _whole, _md, state = rt.read_pair(config)
    assert state["authenticated_checkpoint"]["live_github"] is None
    assert not state["controls"]["stops"]


def test_attest_launch_requires_actual_controller_launcher(tmp_path):
    config = t.make_sandbox(tmp_path)
    run, _w, _art = t.make_controller_run(
        tmp_path / "repo", job_id="fake-attest", role="IMPLEMENTER",
        task_id=rt.MECHANISM_ID)
    with pytest.raises(rt.CurrentnessError,
                       match="TRUSTED_LAUNCH_CALLER_INVALID"):
        rt.attest_launch(config, run)


def test_state_maintenance_cli_requires_operator(tmp_path):
    config = t.make_sandbox(tmp_path)
    cp = Path(config["_root"]) / "config.json"
    proc = __import__("subprocess").run(
        [sys.executable, "-B", str(PROGRAMMA / "operational_currentness_runtime_r1.py"),
         "--config", str(cp), "migrate"],
        capture_output=True, text=True, cwd=str(ROOT))
    assert proc.returncode == 1
    assert "OPERATOR_AUTHORIZATION_UNAVAILABLE" in proc.stderr


def test_registry_tamper_and_untrusted_runpath_fail(tmp_path):
    config = t.make_sandbox(tmp_path)
    run, _w, _art = t.make_controller_run(
        tmp_path / "repo", job_id="registry-run", role="IMPLEMENTER",
        task_id=rt.MECHANISM_ID)
    config = t.enroll_test_run(config, run)
    registry = json.loads(rt._registry_path(config).read_text())
    entry = next(iter(registry["entries"].values()))
    entry["role"] = "REVIEWER"
    rt._registry_path(config).write_text(json.dumps(registry))
    with pytest.raises(rt.CurrentnessError,
                       match="LOCAL_CAPABILITY_SIGNATURE_MISMATCH"):
        rt._require_trusted_launch(config, run, rt.validate_controller_run(
            run, rt._make_return_event(config, run)["source"]), json.loads(
                (run / "binding.json").read_text()))

    outside = tmp_path / "repo" / "outside" / "controller-state" / "x"
    outside.mkdir(parents=True)
    with pytest.raises(rt.CurrentnessError, match="UNTRUSTED_RUN_PATH"):
        rt.attest_launch(config, outside)


def test_control_cli_cannot_mint_material_events(tmp_path):
    config = t.make_sandbox(tmp_path)
    for kind in ("REJECTION", "PROTECTED_INTEGRATION", "GITHUB_OBSERVATION",
                 "REVIEW_VERDICT", "WORKER_RETURN"):
        with pytest.raises(rt.CurrentnessError, match="PUBLIC_EVENT_INTAKE_DISABLED"):
            rt.intake_control_event(config, t.event(kind, payload={}))


def test_trusted_rejection_is_not_claim_ready(tmp_path):
    config = t.make_sandbox(tmp_path)
    run, _w, art = t.make_controller_run(
        tmp_path / "repo", job_id="trusted-reject", role="REJECTOR",
        task_id="B01", return_schema=rt.REJECTION_SCHEMA)
    art.write_text(json.dumps({
        "schema": rt.REJECTION_SCHEMA, "task_id": "B01", "role": "REJECTOR",
        "session": "ses_local_fixture_child",
        "implementation_commit": "a" * 40, "predecessor": "candidate-source",
        "reason": "qualified test rejection"}) + "\n")
    config = t.enroll_test_run(config, run)
    rt.intake_event(config, rt._make_return_event(config, run, return_path=str(art)),
                    trusted=True)
    _whole, _md, state = rt.read_pair(config)
    b01 = next(row for row in state["tasks"] if row["id"] == "B01")
    assert b01["sourcefree_state"] == "REJECTED"
    assert b01["readiness"] == "REJECTED"
    assert b01["claim_ready"] is False


def test_fake_merge_refused_and_real_merge_without_ci_is_pending(tmp_path):
    config = t.make_sandbox(tmp_path)
    run, _w, art = t.make_controller_run(
        tmp_path / "repo", job_id="fake-protect", role="PROTECTED_INTEGRATOR",
        task_id="B05", return_schema=rt.PROTECTED_INTEGRATION_SCHEMA)
    art.write_text(json.dumps({
        "schema": rt.PROTECTED_INTEGRATION_SCHEMA, "task_id": "B05",
        "source_commit": "cab1f2d6cdab6f6b653ed20e5b41afb90d9facbc",
        "merge_sha": "f" * 40, "ci_state": "PASS",
        "ci_observation_digest": "evil"}) + "\n")
    config = t.enroll_test_run(config, run)
    with pytest.raises(rt.CurrentnessError, match="PROTECTED_MERGE_LINEAGE_INVALID"):
        rt.intake_event(config, rt._make_return_event(config, run, return_path=str(art)),
                        trusted=True)
    _whole, _md, state = rt.read_pair(config)
    b05 = next(row for row in state["tasks"] if row["id"] == "B05")
    assert b05["protected_integration"] == "PENDING_PROTECTED_CI_AND_ADOPTION"

    run2, _w2, art2 = t.make_controller_run(
        tmp_path / "repo", job_id="pending-protect", role="PROTECTED_INTEGRATOR",
        task_id="P3", return_schema=rt.PROTECTED_INTEGRATION_SCHEMA)
    art2.write_text(json.dumps({
        "schema": rt.PROTECTED_INTEGRATION_SCHEMA, "task_id": "P3",
        "source_commit": "fe51de7979108df3e922e69ea3fd1d5159c5e293",
        "merge_sha": "034bf8b6927bcd9c7c0b88b36368c1282a8f1f14",
        "ci_state": "PASS", "ci_observation_digest": "not-observed"}) + "\n")
    config = t.enroll_test_run(config, run2)
    rt.intake_event(config, rt._make_return_event(config, run2, return_path=str(art2)),
                    trusted=True)
    _whole, _md, state = rt.read_pair(config)
    assert state["protected_foundations"]["P3"]["scope"] == "SOURCEFREE_PROTECTED"
    assert state["protected_integration_requests"][-1]["state"] == (
        "PENDING_PROTECTED_CI_AND_ADOPTION")


def test_fake_reviewer_run_and_prefix_verdict_refused(tmp_path):
    config = t.make_sandbox(tmp_path)
    receipt = json.loads((ROOT / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/"
                          "reviewer_original/REVIEW_RECEIPT.json").read_text())
    run, _w, _art = t.make_controller_run(
        tmp_path / "repo", job_id="fake-reviewer", role="REVIEWER",
        task_id=rt.MECHANISM_ID, return_schema=rt.REVIEW_RECEIPT_SCHEMA,
        return_payload=receipt)
    source = rt._make_return_event(config, run)["source"]
    source["trust"] = "REAL_LOCAL_SUPERVISED_REVIEW_RUN"
    source["review_run_dir"] = str(run)
    with pytest.raises(rt.CurrentnessError, match="UNTRUSTED_CONTROLLER_RUN"):
        rt._validate_review_receipt(config, receipt, replay=False, source=source)
    with pytest.raises(rt.CurrentnessError,
                       match="REVIEW_VERDICT_ARTIFACT_MISMATCH"):
        rt._verify_verdict_artifact(
            config, "f8006235266aa618963b186e5c357bf92be830b3",
            [{"path": "WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R2_G5/VERDICT.json",
              "git_blob": "1e3fe0ae4200f15451ffc7867ba8b6d23bb4114e"}],
            "REVISE")


def test_trusted_reviewer_run_is_accepted(tmp_path):
    config = t.make_sandbox(tmp_path)
    receipt = json.loads((ROOT / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/"
                          "reviewer_original/REVIEW_RECEIPT.json").read_text())
    run, _w, _art = t.make_controller_run(
        tmp_path / "repo", job_id="trusted-reviewer", role="REVIEWER",
        task_id=rt.MECHANISM_ID, return_schema=rt.REVIEW_RECEIPT_SCHEMA,
        return_payload=receipt, session=receipt["reviewer_session"],
        expected_source_commit=receipt["implementation_commit"])
    config = t.enroll_test_run(config, run)
    source = rt._make_return_event(config, run)["source"]
    source["trust"] = "REAL_LOCAL_SUPERVISED_REVIEW_RUN"
    source["review_run_dir"] = str(run)
    validated = rt._validate_review_receipt(
        config, receipt, replay=False, source=source)
    assert validated["review_run"]["role"] == "REVIEWER"
    assert validated["review_run"]["session"] == receipt["reviewer_session"]


def test_authorized_revocation_and_restoration(tmp_path):
    config = t.make_sandbox(tmp_path)
    config = operator_auth(config, kinds=["REVOCATION", "RESTORATION"],
                           scopes=["REVOCATION B03", "RESTORATION B03"])
    revoke = t.event("REVOCATION", payload={
        "scope": "B03", "authorization_id": "ops-control-1",
        "owner": "test HQ operator", "reason": "authorized revocation"})
    rt.intake_event(config, revoke, trusted=True)
    _whole, _md, state = rt.read_pair(config)
    b03 = next(r for r in state["tasks"] if r["id"] == "B03")
    b05 = next(r for r in state["tasks"] if r["id"] == "B05")
    assert b03["readiness"] == "REVOKED"
    assert b05["readiness"] == "BLOCKED_BY_DEPENDENCY"
    restore = t.event("RESTORATION", payload={
        "scope": "B03", "restores": revoke["event_id"],
        "authorization_id": "ops-control-1", "owner": "test HQ operator",
        "reason": "authorized restoration"})
    rt.intake_event(config, restore, trusted=True)
    _whole, _md, state = rt.read_pair(config)
    b03 = next(r for r in state["tasks"] if r["id"] == "B03")
    b05 = next(r for r in state["tasks"] if r["id"] == "B05")
    assert not state["controls"].get("revocations")
    assert state["controls"]["restorations"][-1]["restores"] == revoke["event_id"]
    assert b03["readiness"] != "REVOKED"
    assert b05["readiness"] != "BLOCKED_BY_DEPENDENCY"
