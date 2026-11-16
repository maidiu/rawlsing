"""Tests for the SOROK automatic operational-currentness runtime R1."""
from __future__ import annotations

import copy
import hashlib
import json
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
FIXTURES = ROOT / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R1/fixtures/historical_reviews"
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
    config_path = root / "config.json"
    config_path.write_text(json.dumps({
        "schema": "SOROK_CURRENTNESS_RUNTIME_CONFIG_R1",
        "repo_root": str(root),
        "pair_json": "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json",
        "pair_md": "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md",
        "state_root": "state",
        "frozen_source_dir":
            "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1",
        "github_baseline": str(BASELINE) if BASELINE.is_file() else None,
        "controller_state_root": "controller-state",
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


def replay_receipt(name):
    return json.loads((FIXTURES / name / "REPLAY_RECEIPT.json").read_text())


def test_init_preserves_frozen_projection_and_last_key(tmp_path):
    config = make_sandbox(tmp_path)
    whole, md, state = read_pair(config)
    assert list(whole)[-1] == rt.RUNTIME_KEY
    assert whole[rt.FROZEN_KEY]["adoption"] == "PENDING_INDEPENDENT_RECEIVING"
    assert state["generation"] == 1
    assert rt._extract_block(md, rt.FROZEN_START, rt.FROZEN_END) == \
        rt._extract_block((ROOT / "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md")
                          .read_text(encoding="utf-8"), rt.FROZEN_START, rt.FROZEN_END)
    assert rt.validate_pair(whole, md) == []


def test_duplicate_event_is_idempotent(tmp_path):
    config = make_sandbox(tmp_path)
    row = event("USER_STOP", payload={"scope": "OLD_FLEET", "reason": "test"})
    first = rt.intake_event(config, row)
    whole, _md, state = read_pair(config)
    generation = state["generation"]
    second = rt.intake_event(config, row)
    assert first["state"] == "EVENT_RECORDED"
    assert second["state"] == "DUPLICATE_EVENT"
    _whole, _md, state = read_pair(config)
    assert state["generation"] == generation


def test_out_of_order_event_is_refused(tmp_path):
    config = make_sandbox(tmp_path)
    row = event("USER_STOP", payload={"scope": "OLD_FLEET"})
    row["sequence"] = 99
    with pytest.raises(rt.CurrentnessError, match="OUT_OF_ORDER_EVENT"):
        rt.intake_event(config, row)


def test_self_review_is_refused(tmp_path):
    config = make_sandbox(tmp_path)
    receipt = copy.deepcopy(replay_receipt("B05_1089"))
    receipt["reviewer_session"] = receipt["author_session"]
    with pytest.raises(rt.CurrentnessError, match="SELF_REVIEW_REFUSED"):
        rt._validate_review_receipt(config, receipt, replay=True)


def test_wrong_review_source_document_is_refused(tmp_path):
    config = make_sandbox(tmp_path)
    receipt = copy.deepcopy(replay_receipt("B05_1089"))
    receipt["source_documents"][0]["git_blob"] = "0" * 40
    with pytest.raises(rt.CurrentnessError, match="REVIEW_DOCUMENT_BLOB_MISMATCH"):
        rt._validate_review_receipt(config, receipt, replay=True)


def test_revocation_invalidates_dependents(tmp_path):
    config = make_sandbox(tmp_path)
    rt.intake_event(config, event(
        "REVOCATION", payload={"scope": "B02", "owner": "competent owner",
                               "reason": "test revocation"}))
    _whole, _md, state = read_pair(config)
    by_id = {task["id"]: task for task in state["tasks"]}
    assert by_id["B02"]["readiness"] == "REVOKED"
    assert by_id["B04"]["readiness"] == "BLOCKED_BY_DEPENDENCY"


def test_scope_inflation_is_refused(tmp_path):
    config = make_sandbox(tmp_path)
    receipt = copy.deepcopy(replay_receipt("B05_1089"))
    receipt["full_original_claim"] = "ACCEPT"
    with pytest.raises(rt.CurrentnessError, match="SCOPE_INFLATION_REFUSED"):
        rt._validate_review_receipt(config, receipt, replay=True)


def test_stale_r2_b05_review_cannot_regress_r3(tmp_path):
    config = make_sandbox(tmp_path)
    receipt = copy.deepcopy(replay_receipt("B05_1089"))
    receipt["implementation_commit"] = "270eb29cd4487b6865b61adc9d671952554d425d"
    row = {
        "schema": rt.EVENT_SCHEMA,
        "event_id": "stale-b05-r2",
        "kind": "REVIEW_VERDICT",
        "recorded_utc": rt.now_utc(),
        "source": {"trust": "IMMUTABLE_HISTORICAL_INDEPENDENT_REVIEW_REPLAY"},
        "receipt": receipt,
        "payload": {"task_id": "B05"},
    }
    with pytest.raises(rt.CurrentnessError, match="STALE_EVIDENCE"):
        rt.intake_event(config, row)
    _whole, _md, state = read_pair(config)
    task = next(t for t in state["tasks"] if t["id"] == "B05")
    assert task["code_sha"] == "cab1f2d6cdab6f6b653ed20e5b41afb90d9facbc"


def test_stop_invalidates_dependents_transitively(tmp_path):
    config = make_sandbox(tmp_path)
    rt.intake_event(config, event(
        "USER_STOP", payload={"scope": "B02", "owner": "user", "reason": "test STOP"}))
    _whole, _md, state = read_pair(config)
    by_id = {task["id"]: task for task in state["tasks"]}
    assert by_id["B02"]["readiness"] == "STOPPED_BY_USER"
    assert by_id["B04"]["readiness"] == "BLOCKED_BY_DEPENDENCY"
    assert by_id["B05"]["readiness"] == "BLOCKED_BY_DEPENDENCY"
    assert "B05" not in state["readiness"]["awaiting_independent_receiving"]


def test_authority_hold_invalidates_dependents(tmp_path):
    config = make_sandbox(tmp_path)
    rt.intake_event(config, event(
        "SOURCE_AUTHORITY_HOLD",
        payload={"scope": "C01", "owner": "C05/CAN/ADP issuer",
                 "reason": "actor knowledge HOLD"}))
    _whole, _md, state = read_pair(config)
    by_id = {task["id"]: task for task in state["tasks"]}
    assert by_id["C01"]["readiness"] == "HELD_SOURCE_AUTHORITY"
    assert by_id["C02"]["readiness"] == "BLOCKED_BY_DEPENDENCY"
    assert any(hold["kind"] == "SOURCE_AUTHORITY_HOLD"
               and hold["scope"] == "C01" for hold in state["holds"])


def test_mixed_pair_is_typed_red(tmp_path):
    config = make_sandbox(tmp_path)
    md = config["_pair_md"].read_text(encoding="utf-8")
    config["_pair_md"].write_text(
        md.replace("SOROK_RUNTIME_GENERATION: 1", "SOROK_RUNTIME_GENERATION: 99"),
        encoding="utf-8")
    with pytest.raises(rt.CurrentnessError,
                       match="PAIRED_MD_JSON_MIXED_GENERATION"):
        read_pair(config)


def test_crash_recovery_rolls_forward_pending_pair(tmp_path, monkeypatch):
    config = make_sandbox(tmp_path)
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
    assert new_state["generation"] == 2
    assert rt.validate_pair(new_whole, new_md) == []


def test_historical_replays_are_explicit_and_scoped(tmp_path):
    config = make_sandbox(tmp_path)
    for name in ("B05_1089", "C04_1062", "C05_1091"):
        receipt = replay_receipt(name)
        row = {
            "schema": rt.EVENT_SCHEMA,
            "event_id": "review:" + rt.digest(receipt),
            "kind": "REVIEW_VERDICT",
            "recorded_utc": rt.now_utc(),
            "source": {"trust": "IMMUTABLE_HISTORICAL_INDEPENDENT_REVIEW_REPLAY"},
            "receipt": receipt,
            "payload": {"task_id": receipt["task_id"]},
        }
        rt.intake_event(config, row)
    _whole, _md, state = read_pair(config)
    by_id = {task["id"]: task for task in state["tasks"]}
    assert by_id["B05"]["sourcefree_state"] == "SCOPED_RECEIVED_UNMERGED"
    assert by_id["C04"]["sourcefree_state"] == "SCOPED_RECEIVED_UNMERGED"
    assert by_id["C05"]["sourcefree_state"] == "SCOPED_RECEIVED_UNMERGED"
    assert all(row["replay_is_not_new_review"] for row in state["baseline_replay"])
    assert len(state["baseline_replay"]) == 3


def make_controller_run(root: Path, *, job_id="sorok-currentness-test-job"):
    run = root / "controller-state" / job_id
    run.mkdir(parents=True)
    worktree = root / "child-worktree"
    worktree.mkdir(exist_ok=True)
    argv = ["/usr/bin/true"]
    job = {"job_id": job_id, "session": "ses_local_fixture_child",
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
    }
    (run / "job.json").write_text(json.dumps(job), encoding="utf-8")
    (run / "binding.json").write_text(json.dumps(binding), encoding="utf-8")
    (run / "launch.json").write_text(json.dumps({
        "job_id": job_id, "child_pid": 4242, "supervisor_pid": 4241,
        "observer_pid": 4243, "run_dir": str(run),
        "launch_is_not_completion": True}), encoding="utf-8")
    (run / "process.json").write_text(json.dumps({
        "job_id": job_id, "session": job["session"], "grant_id": job["grant_id"],
        "pid": 4242, "started_utc": rt.now_utc()}), encoding="utf-8")
    (run / "completion.json").write_text(json.dumps({
        "job_id": job_id, "session": job["session"], "grant_id": job["grant_id"],
        "pid": 4242, "exit_code": 0, "finished_utc": rt.now_utc(),
        "scope": "LOCAL_TEST",
        "recipient_thread": binding["recipient_thread"]}), encoding="utf-8")
    artifact = worktree / "return.json"
    artifact.write_text(json.dumps({
        "schema": rt.RETURN_SCHEMA,
        "scope": "INFRASTRUCTURE_QUALIFICATION_NOT_ORIGINAL_SCIENCE",
        "artifact": {"message": "local fixture"}}), encoding="utf-8")
    return run, worktree, artifact


def test_real_controller_receipt_intake_is_review_pending(tmp_path):
    config = make_sandbox(tmp_path)
    run, _worktree, artifact = make_controller_run(tmp_path)
    row = rt._make_return_event(config, run, return_path=str(artifact))
    result = rt.intake_event(config, row)
    assert result["state"] == "EVENT_RECORDED"
    _whole, _md, state = read_pair(config)
    assert len(state["infrastructure_qualification"]) == 1
    infra = state["infrastructure_qualification"][0]
    assert infra["exit_code"] == 0
    assert infra["execution_state"] == "RETURNED_REVIEW_PENDING"
    assert infra["review_required"] is True
    assert state["controller_integration"]["hook_state"] == "REAL_LOCAL_RETURN_INTAKEN"


def test_startup_reconciles_baseline_and_reports_unseen_receipts(tmp_path):
    if not BASELINE.is_file():
        pytest.skip("authenticated GitHub baseline not available")
    config = make_sandbox(tmp_path)
    run, _worktree, _artifact = make_controller_run(tmp_path / "repo", job_id="unseen-job")
    result = rt.startup(config, reconcile=False)
    assert any("AUTHENTICATED_GITHUB_REF_NOT_YET_RECONCILED" in
               item["what_changed"] for item in result["reconciliation_required"])
    result = rt.startup(config, reconcile=True)
    assert not any("AUTHENTICATED_GITHUB_REF_NOT_YET_RECONCILED" in
                   item["what_changed"] for item in result["reconciliation_required"])
    assert any("UNSEEN_LOCAL_CONTROLLER_RECEIPT" in item["what_changed"]
               for item in result["reconciliation_required"])


def test_reconciliation_resolution_is_explicit_and_idempotent(tmp_path):
    config = make_sandbox(tmp_path)
    item = {"what_changed": "UNSEEN_LOCAL_CONTROLLER_RECEIPT test-job",
            "expected_evidence": "test", "owner": "test", "next_action": "test"}
    rt.intake_event(config, event("RECONCILIATION_REQUIRED", payload={"item": item}))
    _whole, _md, state = read_pair(config)
    assert state["reconciliation_required"] == [item]
    row = event("RECONCILIATION_RESOLVED", payload={
        "what_changed": item["what_changed"], "evidence": "run receipt inspected",
        "owner": "SOROK HQ", "reason": "explicit test resolution"})
    rt.intake_event(config, row)
    _whole, _md, state = read_pair(config)
    assert state["reconciliation_required"] == []
    assert state["reconciliation_resolved"][-1]["what_changed"] == item["what_changed"]
    duplicate = rt.intake_event(config, row)
    assert duplicate["state"] == "DUPLICATE_EVENT"


def test_readout_contains_ready_hold_owner_and_unmet_prereqs(tmp_path):
    config = make_sandbox(tmp_path)
    rt.intake_event(config, event(
        "USER_STOP", payload={"scope": "B02", "owner": "user", "reason": "test STOP"}))
    _whole, _md, state = read_pair(config)
    readout = rt.render_readout(state)
    assert readout["generation"] == state["generation"]
    assert readout["no_automatic_dispatch"] is True
    assert readout["mechanism_review"]["state"] == "PENDING_EXTERNAL_NONAUTHOR_REVIEW"
    assert any(row["id"] == "B02" and row["readiness"] == "STOPPED_BY_USER"
               for row in readout["task_readiness"])
    assert any(hold["kind"] == "USER_STOP" and hold["scope"] == "B02"
               for hold in readout["holds"])
    assert readout["recommended_next"]["owner"]
