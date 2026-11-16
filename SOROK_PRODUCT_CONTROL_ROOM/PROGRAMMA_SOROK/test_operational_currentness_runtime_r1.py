"""Tests for the SOROK automatic operational-currentness runtime R2."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import operational_currentness_runtime_r1 as rt  # noqa: E402

PROGRAMMA = ROOT / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK"
FIXTURES = ROOT / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/fixtures/historical_reviews"
BASELINE = Path("/Users/matthewsmith/.local/state/rawlsing-controller/"
                "sorok-01a161c5/sorok-automatic-currentness-20261115/"
                "GITHUB_INTAKE_BASELINE.json")


def make_sandbox(tmp_path):
    root = tmp_path / "repo"
    room = root / "SOROK_PRODUCT_CONTROL_ROOM"
    frozen = room / "PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1"
    frozen.mkdir(parents=True)
    shutil.copy2(ROOT / "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json",
                 room / "CURRENT_PROGRESS.json")
    shutil.copy2(ROOT / "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md",
                 room / "CURRENT_PROGRESS.md")
    for path in PROGRAMMA.joinpath("CURRENTNESS_FROZEN_SOURCE_R1").glob("*.json"):
        shutil.copy2(path, frozen / path.name)
    baseline_path = root / "GITHUB_INTAKE_BASELINE.json"
    if BASELINE.is_file():
        shutil.copy2(BASELINE, baseline_path)
    config_path = root / "config.json"
    config_path.write_text(json.dumps({
        "schema": "SOROK_CURRENTNESS_RUNTIME_CONFIG_R1",
        "repo_root": str(root),
        "pair_json": "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json",
        "pair_md": "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md",
        "state_root": "state",
        "frozen_source_dir":
            "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1",
        "github_baseline": str(baseline_path) if baseline_path.is_file() else None,
        "controller_state_root": "controller-state",
        "github_live": {
            "remote": "https://github.com/maidiu/rawlsing.git",
            "api_repo": "maidiu/rawlsing",
            "ttl_seconds": 900,
            "cafile": "/etc/ssl/cert.pem",
            "watch_prs": [1062, 1066, 1089, 1091, 1095],
            "watch_branches": ["integration/pre-main-reconciliation-r1"],
        },
    }, indent=2) + "\n", encoding="utf-8")
    (root / "controller-state").mkdir()
    config = rt.load_config(config_path)
    whole = rt.read_json(config["_pair_json"])
    md = config["_pair_md"].read_text(encoding="utf-8")
    state = rt.initial_state(config, whole)
    state["source_freeze"]["frozen_md_block_sha256"] = rt.sha256_bytes(
        rt._extract_block(md, rt.FROZEN_START, rt.FROZEN_END).encode())
    rt.commit_state(config, whole, md, state)
    return config


def read_pair(config):
    return rt.read_pair(config)


def event(kind, **kwargs):
    payload = kwargs.pop("payload", {})
    source = kwargs.pop("source", {"trust": "TEST"})
    return {
        "schema": rt.EVENT_SCHEMA,
        "event_id": kwargs.pop("event_id", kind + ":" + rt.digest(payload)),
        "kind": kind,
        "recorded_utc": rt.now_utc(),
        "source": source,
        "payload": payload,
        **kwargs,
    }


def fake_live(config, *, refs=None, status_coverage="FULL",
              fetched_at=None, expires_at=None, evidence_digest=None):
    rows = rt._baseline_rows(config)
    live_refs = {}
    pulls, issues, comments = {}, {}, {}
    for row in rows:
        number = row.get("number")
        value = row.get("value") or {}
        if isinstance(value, dict) and "head" in value:
            live_refs[f"refs/pull/{number}/head"] = value.get("head_sha")
            live_refs[f"refs/pull/{number}/merge"] = value.get("merge_commit_sha")
            if value.get("head"):
                live_refs["refs/heads/" + str(value["head"]).removeprefix(
                    "refs/heads/")] = value.get("head_sha")
            pulls[str(number)] = {
                "state": value.get("state", "open"),
                "merged": value.get("merged", False),
                "draft": value.get("draft", True),
                "updated_at": value.get("updated_at"),
                "head_sha": value.get("head_sha"),
                "merge_commit_sha": value.get("merge_commit_sha"),
                "http_status": 200,
                "body_sha256": "0" * 64,
            }
        elif isinstance(value, dict) and "issue" in value:
            issue = value["issue"]
            issues[str(number)] = {
                "state": issue.get("state", "open"),
                "updated_at": issue.get("updated_at"),
                "comments": issue.get("comments"),
                "http_status": 200 if status_coverage == "FULL" else 403,
                "body_sha256": "0" * 64,
            }
        else:
            for comment in row.get("comments", []):
                if comment.get("id"):
                    comments[str(comment["id"])] = {
                        "body_sha256": hashlib.sha256(
                            comment.get("body", "").encode()).hexdigest(),
                        "updated_at": None,
                        "http_status": 200 if status_coverage == "FULL" else 403,
                    }
    live_refs.update(refs or {})
    live = {
        "schema": rt.LIVE_GITHUB_SCHEMA,
        "source_trust": "AUTHENTICATED_LIVE_GITHUB",
        "source_identity": "test-live",
        "transport": "test",
        "fetched_at_utc": fetched_at or rt.now_utc(),
        "expires_at_utc": expires_at or rt._utc_add(900),
        "ttl_seconds": 900,
        "refs": live_refs,
        "refs_digest": "0" * 64,
        "api": {"repo": {"http_status": 200}, "pulls": pulls,
                "issues": issues, "comments": comments, "commits": {},
                "token_available": True, "token_error": None},
        "status_coverage": status_coverage,
        "status_checks": len(pulls) + len(issues) + len(comments),
        "status_success": (len(pulls) + len(issues) + len(comments)
                           if status_coverage == "FULL" else 0),
        "credential_helper_used": True,
        "credential_error": None,
    }
    live["evidence_digest"] = evidence_digest or rt.digest({
        "source_identity": live["source_identity"],
        "fetched_at_utc": live["fetched_at_utc"],
        "refs": live["refs"], "refs_digest": live["refs_digest"],
        "api": live["api"], "status_coverage": live["status_coverage"],
    })
    return live


def test_init_preserves_frozen_projection_and_last_key(tmp_path):
    config = make_sandbox(tmp_path)
    whole, md, state = read_pair(config)
    assert list(whole)[-1] == rt.RUNTIME_KEY
    assert whole[rt.FROZEN_KEY]["adoption"] == "PENDING_INDEPENDENT_RECEIVING"
    assert state["generation"] == 1
    assert rt.validate_pair(whole, md) == []


def test_live_github_fresh_observation_is_recorded_with_time_and_expiry(
        tmp_path, monkeypatch):
    config = make_sandbox(tmp_path)
    live = fake_live(config)
    monkeypatch.setattr(rt, "fetch_live_github", lambda cfg: live)
    result = rt.startup(config, reconcile=True)
    _whole, _md, state = read_pair(config)
    stored = state["authenticated_checkpoint"]["live_github"]
    assert stored["source_trust"] == "AUTHENTICATED_LIVE_GITHUB"
    assert stored["fetched_at_utc"] == live["fetched_at_utc"]
    assert stored["expires_at_utc"] == live["expires_at_utc"]
    assert stored["evidence_digest"] == live["evidence_digest"]
    assert result["readout"]["authenticated_github_live"]["fresh"] is True


def test_tampered_local_baseline_head_is_detected_not_accepted(
        tmp_path, monkeypatch):
    config = make_sandbox(tmp_path)
    live = fake_live(config)
    data = json.loads(config["_baseline"].read_text())
    pr = next(row for row in data if row.get("number") == 1062)
    pr["value"]["head"] = "SIMULATED_LOCAL_BASELINE_ADVANCE"
    config["_baseline"].write_text(json.dumps(data) + "\n")
    monkeypatch.setattr(rt, "fetch_live_github", lambda cfg: live)
    items, _live = rt.reconciliation_items(config, read_pair(config)[2])
    assert any("LOCAL_GITHUB_BASELINE_BRANCH_UNAVAILABLE" in i["what_changed"]
               for i in items)
    assert all(i.get("source_kind") == "LIVE_GITHUB" for i in items)


def test_unchanged_stale_local_baseline_is_not_a_fresh_source(
        tmp_path, monkeypatch):
    config = make_sandbox(tmp_path)
    os.utime(config["_baseline"], (1577836800, 1577836800))
    live = fake_live(config, status_coverage="REF_SHA_ONLY")
    monkeypatch.setattr(rt, "fetch_live_github", lambda cfg: live)
    result = rt.startup(config, reconcile=True)
    _whole, _md, state = read_pair(config)
    live_store = state["authenticated_checkpoint"]["live_github"]
    assert live_store["fetched_at_utc"] == live["fetched_at_utc"]
    assert any("GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE" in i["what_changed"]
               for i in result["reconciliation_required"])
    assert result["readout"]["authenticated_github_live"]["fresh"] is True


def test_live_head_advanced_and_deleted_are_typed(tmp_path, monkeypatch):
    config = make_sandbox(tmp_path)
    live = fake_live(config)
    live["refs"]["refs/pull/1095/head"] = "f" * 40
    del live["refs"]["refs/pull/1089/head"]
    monkeypatch.setattr(rt, "fetch_live_github", lambda cfg: live)
    items, _live = rt.reconciliation_items(config, read_pair(config)[2])
    text = [item["what_changed"] for item in items]
    assert any(text_value.startswith("GITHUB_HEAD_ADVANCED pr:1095")
               for text_value in text)
    assert any(text_value.startswith("GITHUB_REF_DELETED pr:1089")
               for text_value in text)


def test_live_source_unavailable_is_typed_not_stale_ready(tmp_path, monkeypatch):
    config = make_sandbox(tmp_path)
    def unavailable(cfg):
        raise rt.CurrentnessError("LIVE_GITHUB_REF_FETCH_UNAVAILABLE", {"exit": 1})
    monkeypatch.setattr(rt, "fetch_live_github", unavailable)
    result = rt.startup(config, reconcile=True)
    assert any("LIVE_GITHUB_REF_FETCH_UNAVAILABLE" in item["what_changed"]
               for item in result["reconciliation_required"])
    _whole, _md, state = read_pair(config)
    assert state["authenticated_checkpoint"]["live_github"] is None


def test_mechanism_review_requires_supervised_review_run(tmp_path):
    config = make_sandbox(tmp_path)
    receipt = copy.deepcopy(json.loads(
        (ROOT / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/fixtures/"
         "historical_reviews/B05_1089/REPLAY_RECEIPT.json").read_text()))
    receipt.update({"task_id": rt.MECHANISM_ID, "verdict": "REVISE_EXACT_DEFECT",
                    "implementation_commit": "a" * 40,
                    "review_commit": "5c83a8321dce70fcc40c8f210af06a9edb1f8999",
                    "source_trust": "REAL_LOCAL_NONAUTHOR_REVIEW",
                    "source_documents": []})
    with pytest.raises(rt.CurrentnessError, match="REVIEW_SUPERVISED_RUN_REQUIRED"):
        rt._validate_review_receipt(config, receipt, replay=False, source=None)


def test_fake_task_review_is_refused(tmp_path):
    config = make_sandbox(tmp_path)
    receipt = copy.deepcopy(json.loads(
        (ROOT / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/fixtures/"
         "historical_reviews/B05_1089/REPLAY_RECEIPT.json").read_text()))
    receipt.update({"task_id": "C05", "reviewer_session": "ses_fake",
                    "author_session": "ses_other_fake",
                    "implementation_commit": "4b33b8be1127c2186931a66f23e3a2b05feaf0a6",
                    "review_commit": "5c83a8321dce70fcc40c8f210af06a9edb1f8999",
                    "source_trust": "REAL_LOCAL_NONAUTHOR_REVIEW",
                    "source_documents": []})
    with pytest.raises(rt.CurrentnessError, match="REVIEW_SUPERVISED_RUN_REQUIRED"):
        rt._validate_review_receipt(config, receipt, replay=False, source=None)


def test_control_events_require_authorization(tmp_path):
    config = make_sandbox(tmp_path)
    with pytest.raises(rt.CurrentnessError, match="OPERATOR_AUTHORIZATION_UNAVAILABLE"):
        rt.intake_event(config, event(
            "USER_STOP", payload={"scope": "B02", "owner": "fake",
                                  "reason": "fabricated"}), trusted=True)
    _whole, _md, state = read_pair(config)
    assert state["controls"]["stops"] == []


def test_authorized_stop_and_superseding_resume(tmp_path):
    config = make_sandbox(tmp_path)
    auth_path = tmp_path / "operator_authorization.json"
    auth = {
        "schema": rt.OPERATOR_AUTH_SCHEMA,
        "authorization_id": "ops-test-1",
        "role": "SOROK_HQ_OPERATOR",
        "owner": "test HQ operator",
        "granted_by": "TEST_ONLY",
        "granted_at_utc": rt.now_utc(),
        "expires_at_utc": rt._utc_add(3600),
        "allowed_kinds": ["USER_STOP", "USER_RESUME"],
        "allowed_scopes": ["USER_STOP B02", "USER_RESUME B02"],
        "allowed_item_digests": [],
        "allowed_source_digests": [],
        "allowed_supersedes": ["stop-b02"],
    }
    auth_path.write_text(json.dumps(auth))
    config_path = tmp_path / "repo/config.json"
    config_data = json.loads(config_path.read_text())
    config_data["trusted_operator_authorization"] = str(auth_path)
    config_path.write_text(json.dumps(config_data))
    config = rt.load_config(config_path)
    stop = event("USER_STOP", event_id="stop-b02",
                 payload={"scope": "B02", "authorization_id": "ops-test-1",
                          "reason": "authorized test stop"})
    rt.intake_event(config, stop, trusted=True)
    _whole, _md, state = read_pair(config)
    assert state["controls"]["stops"]
    resume = event("USER_RESUME", event_id="resume-b02",
                   payload={"scope": "B02", "authorization_id": "ops-test-1",
                            "supersedes": "stop-b02", "reason": "authorized test resume"})
    rt.intake_event(config, resume, trusted=True)
    _whole, _md, state = read_pair(config)
    assert not state["controls"]["stops"]
    assert state["controls"]["resumes"][-1]["supersedes"] == "stop-b02"


def test_unauthorized_resume_is_refused(tmp_path):
    config = make_sandbox(tmp_path)
    with pytest.raises(rt.CurrentnessError, match="OPERATOR_AUTHORIZATION_UNAVAILABLE"):
        rt.intake_event(config, event(
            "USER_RESUME", payload={"scope": "B02", "supersedes": "stop-b02",
                                    "authorization_id": "fake"}), trusted=True)


def test_resolution_requires_authenticated_evidence(tmp_path, monkeypatch):
    config = make_sandbox(tmp_path)
    live = fake_live(config, status_coverage="REF_SHA_ONLY")
    monkeypatch.setattr(rt, "fetch_live_github", lambda cfg: live)
    result = rt.startup(config, reconcile=True)
    item = next(i for i in result["reconciliation_required"]
                if i["source_kind"] == "LIVE_GITHUB")
    with pytest.raises(rt.CurrentnessError, match="RESOLUTION_AUTHENTICATION_REQUIRED"):
        # The public CLI no longer accepts arbitrary --evidence; direct event
        # with no digest/auth must also refuse.
        rt.intake_event(config, event(
            "RECONCILIATION_RESOLVED",
            payload={"what_changed": item["what_changed"],
                     "evidence": "arbitrary text"}), trusted=True)
    with pytest.raises(rt.CurrentnessError, match="RESOLUTION_FRESH_OBSERVATION_INVALID"):
        rt.intake_event(config, event(
            "RECONCILIATION_RESOLVED",
            payload={"what_changed": item["what_changed"],
                     "fresh_observation_digest": "0" * 64}), trusted=True)
    rt.intake_event(config, event(
        "RECONCILIATION_RESOLVED",
        payload={"what_changed": item["what_changed"],
                 "fresh_observation_digest": live["evidence_digest"]}),
        trusted=True)
    _whole, _md, state = read_pair(config)
    assert not any(row["what_changed"] == item["what_changed"]
                   for row in state["reconciliation_required"])


def test_legacy_arbitrary_resolution_is_reopened(tmp_path):
    config = make_sandbox(tmp_path)
    _whole, _md, state = read_pair(config)
    state["reconciliation_resolved"].append({
        "what_changed": "AUTHENTICATED_GITHUB_INTAKE_UNAVAILABLE",
        "evidence": "arbitrary legacy text", "owner": "fake-operator",
        "event_id": "legacy-resolution"})
    rt.recompute(state)
    rt.commit_state(config, _whole, _md, state)
    items, _live = rt.reconciliation_items(config, read_pair(config)[2])
    assert any("LEGACY_UNVERIFIED_RESOLUTION" in i["what_changed"] for i in items)


def test_duplicate_and_out_of_order_are_typed(tmp_path):
    config = make_sandbox(tmp_path)
    row = event("USER_STOP", payload={"scope": "OLD_FLEET"})
    # unauthorized first, but duplicate/order are checked after auth; use a
    # replay review event for idempotence instead.
    receipt = json.loads((ROOT / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/"
                          "fixtures/historical_reviews/B05_1089/REPLAY_RECEIPT.json").read_text())
    replay = {
        "schema": rt.EVENT_SCHEMA, "event_id": "replay-b05",
        "kind": "REVIEW_VERDICT", "recorded_utc": rt.now_utc(),
        "source": {"trust": "IMMUTABLE_HISTORICAL_INDEPENDENT_REVIEW_REPLAY"},
        "receipt": receipt, "payload": {"task_id": "B05"},
    }
    first = rt.intake_event(config, replay, trusted=True)
    second = rt.intake_event(config, replay, trusted=True)
    assert first["state"] == "EVENT_RECORDED"
    assert second["state"] == "DUPLICATE_EVENT"
    bad = copy.deepcopy(replay)
    bad["event_id"] = "replay-b05-out-of-order"
    bad["sequence"] = 99
    with pytest.raises(rt.CurrentnessError, match="OUT_OF_ORDER_EVENT"):
        rt.intake_event(config, bad, trusted=True)


def test_mixed_pair_and_crash_recovery(tmp_path, monkeypatch):
    config = make_sandbox(tmp_path)
    md = config["_pair_md"].read_text(encoding="utf-8")
    config["_pair_md"].write_text(
        md.replace("SOROK_RUNTIME_GENERATION: 1", "SOROK_RUNTIME_GENERATION: 99"),
        encoding="utf-8")
    with pytest.raises(rt.CurrentnessError, match="PAIRED_MD_JSON_MIXED_GENERATION"):
        read_pair(config)
    # restore and exercise roll-forward recovery
    config["_pair_md"].write_text(md, encoding="utf-8")
    whole, md, state = read_pair(config)
    state = copy.deepcopy(state)
    state["generation"] += 1
    state["updated_utc"] = rt.now_utc()
    rt.recompute(state)
    original = rt.write_text_atomic
    seen = {"md": 0}
    def flaky(path, text):
        if Path(path) == config["_pair_md"] and seen["md"] == 0:
            seen["md"] += 1
            return
        return original(path, text)
    monkeypatch.setattr(rt, "write_text_atomic", flaky)
    with pytest.raises(rt.CurrentnessError, match="COMMIT_PAIR_VALIDATION_FAILED"):
        rt.commit_state(config, copy.deepcopy(whole), md, state)
    monkeypatch.setattr(rt, "write_text_atomic", original)
    result = rt.recover(config)
    assert result["state"] == "RECOVERED"
    new_whole, new_md, new_state = read_pair(config)
    assert rt.validate_pair(new_whole, new_md) == []


def make_controller_run(root: Path, *, job_id="sorok-currentness-test-job",
                        role="IMPLEMENTER", task_id=rt.MECHANISM_ID,
                        return_schema=rt.RETURN_SCHEMA,
                        return_payload=None,
                        session="ses_local_fixture_child",
                        expected_source_commit=None):
    run = root / "controller-state" / job_id
    run.mkdir(parents=True)
    worktree = root / "child-worktree"
    worktree.mkdir(exist_ok=True)
    argv = ["/usr/bin/true"]
    job = {"job_id": job_id, "session": session,
           "grant_id": "g-local-fixture", "argv": argv}
    binding = {
        "schema": "LOCAL_COMPLETION_BINDING_V1",
        "recipient_thread": "00000000-0000-4000-8000-000000000000",
        "worktree": str(worktree), "session": job["session"],
        "state_root": str(root / "controller-state"), "codex_binary": "/usr/bin/true",
        "notify": False,
        "grant": {"id": job["grant_id"], "scope": "LOCAL_TEST",
                  "expires_utc": "2099-01-01T00:00:00+00:00",
                  "job_ids": [job_id],
                  "argv_sha256": rt.command_digest(argv)},
        "sorok_currentness": {"task_id": task_id, "role": role,
                              "expected_session": job["session"],
                              "return_filename": "return.json"},
    }
    if expected_source_commit:
        binding["sorok_currentness"]["expected_source_commit"] = expected_source_commit
    (run / "job.json").write_text(json.dumps(job), encoding="utf-8")
    (run / "binding.json").write_text(json.dumps(binding), encoding="utf-8")
    pid = os.getpid()
    (run / "launch.json").write_text(json.dumps({
        "job_id": job_id, "child_pid": pid, "supervisor_pid": pid - 1,
        "observer_pid": pid + 1, "run_dir": str(run),
        "launch_is_not_completion": True}), encoding="utf-8")
    (run / "process.json").write_text(json.dumps({
        "job_id": job_id, "session": job["session"], "grant_id": job["grant_id"],
        "pid": pid, "started_utc": rt.now_utc()}), encoding="utf-8")
    (run / "completion.json").write_text(json.dumps({
        "job_id": job_id, "session": job["session"], "grant_id": job["grant_id"],
        "pid": pid, "exit_code": 0, "finished_utc": rt.now_utc(),
        "scope": "LOCAL_TEST",
        "recipient_thread": binding["recipient_thread"]}), encoding="utf-8")
    artifact = worktree / "return.json"
    artifact.write_text(json.dumps(return_payload or {
        "schema": return_schema, "task_id": task_id, "role": role,
        "session": job["session"], "scope": "TEST",
        "artifact": {"message": "local fixture"}}), encoding="utf-8")
    return run, worktree, artifact


def enroll_test_run(config, run):
    auth_path = Path(config["_state_root"]) / "test_operator_authorization.json"
    job = json.loads((run / "job.json").read_text())
    process = json.loads((run / "process.json").read_text())
    source = rt.digest({
        "job_id": job["job_id"], "session": job["session"],
        "grant_id": job["grant_id"],
        "job_sha256": rt.sha256_file(run / "job.json"),
        "binding_sha256": rt.sha256_file(run / "binding.json"),
        "launch_sha256": rt.sha256_file(run / "launch.json"),
        "process_sha256": rt.sha256_file(run / "process.json"),
        "pid": process["pid"],
    })
    auth_path.write_text(json.dumps({
        "schema": rt.OPERATOR_AUTH_SCHEMA,
        "authorization_id": "test-enroll-1",
        "role": "SOROK_HQ_OPERATOR",
        "owner": "test operator",
        "granted_by": "TEST_ONLY",
        "granted_at_utc": rt.now_utc(),
        "expires_at_utc": rt._utc_add(3600),
        "allowed_kinds": ["TRUSTED_LAUNCH_ENROLLMENT", "USER_STOP",
                          "USER_RESUME", "REVOCATION", "RESTORATION",
                          "STATE_MAINTENANCE"],
        "allowed_scopes": ["TRUSTED_LAUNCH_ENROLLMENT", "USER_STOP",
                           "USER_RESUME", "REVOCATION", "RESTORATION",
                           "STATE_MAINTENANCE", "AUTOMATIC_CURRENTNESS_R1"],
        "allowed_source_digests": [source],
        "allowed_item_digests": [],
        "allowed_supersedes": [],
    }) + "\n")
    config_path = Path(config["_root"]) / "config.json"
    data = json.loads(config_path.read_text())
    data["trusted_operator_authorization"] = str(auth_path)
    config_path.write_text(json.dumps(data) + "\n")
    config = rt.load_config(config_path)
    rt.enroll_existing_run(config, run, "test-enroll-1")
    return config


def test_mechanism_worker_return_is_review_pending(tmp_path, monkeypatch):
    config = make_sandbox(tmp_path)
    run, _worktree, artifact = make_controller_run(tmp_path / "repo")
    payload = {
        "schema": rt.RETURN_SCHEMA, "task_id": rt.MECHANISM_ID,
        "role": "IMPLEMENTER", "session": "ses_local_fixture_child",
        "implementation_commit": "a" * 40,
        "runtime_blob": "b" * 40, "test_blob": "c" * 40,
        "return_paths": {}}
    artifact.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(rt, "_verify_mechanism_worker_return",
                        lambda cfg, p, b: None)
    config = enroll_test_run(config, run)
    event = rt._make_return_event(config, run, return_path=str(artifact))
    rt.intake_event(config, event, trusted=True)
    _whole, _md, state = read_pair(config)
    assert state["mechanism_worker_return"]["execution_state"] == "RETURNED_REVIEW_PENDING"
    assert state["mechanism_review"]["state"] == "PENDING_EXTERNAL_NONAUTHOR_REVIEW"


def test_readout_contains_live_source_and_holds(tmp_path, monkeypatch):
    config = make_sandbox(tmp_path)
    live = fake_live(config, status_coverage="REF_SHA_ONLY")
    monkeypatch.setattr(rt, "fetch_live_github", lambda cfg: live)
    rt.startup(config, reconcile=True)
    _whole, _md, state = read_pair(config)
    readout = rt.render_readout(state)
    assert readout["authenticated_github_live"]["fresh"] is True
    assert readout["authenticated_github_live"]["status_coverage"] == "REF_SHA_ONLY"
    assert readout["no_automatic_dispatch"] is True
    assert any(hold["kind"] == "MECHANISM_REVIEW" for hold in readout["holds"])
