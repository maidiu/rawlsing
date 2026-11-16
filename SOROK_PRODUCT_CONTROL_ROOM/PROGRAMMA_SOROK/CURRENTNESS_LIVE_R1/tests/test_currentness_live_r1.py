"""Adversarial tests for SOROK live currentness intake R1.

These use the real frozen 27-packet state/MD and a fixture ref observer.  No
network is used; the live remote check is an explicit operator command.
"""
from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
LIVE = ROOT / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_LIVE_R1"
sys.path.insert(0, str(LIVE))
import currentness_live_r1 as engine_mod  # noqa: E402

REAL_PROGRESS = ROOT / "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json"
REAL_MARKDOWN = ROOT / "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md"
BOOTSTRAP = LIVE / "bootstrap.json"
NEW_REF = "refs/heads/codex/sorok-currentness-event-test-r1"
NEW_SHA = "c" * 40
PROTECTED_REF = "refs/heads/integration/pre-main-reconciliation-r1"


class FixtureObserver:
    def __init__(self, refs: dict[str, str]) -> None:
        self.refs = dict(refs)
        self.ancestors: set[tuple[str, str]] = set()
        self.parents: dict[str, tuple[str, ...]] = {}

    def heads(self) -> dict[str, str]:
        return {
            ref: sha for ref, sha in self.refs.items()
            if ref.startswith("refs/heads/")
        }

    def ref(self, refname: str) -> str | None:
        return self.refs.get(refname)

    def is_ancestor(self, ancestor: str, descendant: str) -> bool:
        return ancestor == descendant or (ancestor, descendant) in self.ancestors

    def merge_parents(self, sha: str) -> tuple[str, ...]:
        return self.parents.get(sha, ())


def baseline_refs() -> dict[str, str]:
    bootstrap = json.loads(BOOTSTRAP.read_text())
    return {ref: fact["sha"] for ref, fact in bootstrap["baseline_refs"].items()}


def make_engine(tmp_path: Path, observer: FixtureObserver | None = None):
    progress = tmp_path / "CURRENT_PROGRESS.json"
    markdown = tmp_path / "CURRENT_PROGRESS.md"
    shutil.copyfile(REAL_PROGRESS, progress)
    shutil.copyfile(REAL_MARKDOWN, markdown)
    receipts = tmp_path / "receipts"
    evidence = tmp_path / "evidence"
    receipts.mkdir()
    evidence.mkdir()
    observer = observer or FixtureObserver(baseline_refs())
    engine = engine_mod.CurrentnessEngine(
        progress_path=progress,
        markdown_path=markdown,
        receipts_dir=receipts,
        evidence_root=tmp_path,
        observer=observer,
    )
    engine.init(BOOTSTRAP, force=True)
    return engine, progress, markdown, observer


def check(engine) -> engine_mod.CheckResult:
    return engine.check(write=False)


def write_receipt(
    tmp_path: Path, *, ref: str, sha: str, event_id: str,
    grade: str = "ACCEPT_SCOPED_SOURCEFREE_ENGINEERING",
    scope: str = "SOURCEFREE_TEST_EVENT",
) -> Path:
    evidence = tmp_path / "evidence" / f"{event_id}.md"
    evidence.write_text(f"fixture evidence for {event_id} at {sha}\n")
    receipt = {
        "schema": engine_mod.RECEIPT_SCHEMA,
        "receipt_id": f"FIXTURE-{event_id}",
        "event_id": event_id,
        "event_kind": "ACCEPTED_CODE",
        "event_ref": ref,
        "event_sha": sha,
        "grade": grade,
        "scope": scope,
        "owner": "FIXTURE_OWNER",
        "accepted_at": "2026-11-16",
        "reviewer": "FIXTURE_REVIEWER",
        "evidence": [{
            "path": f"evidence/{evidence.name}",
            "sha256": hashlib.sha256(evidence.read_bytes()).hexdigest(),
        }],
        "attestation": "fixture only",
    }
    path = tmp_path / "receipts" / f"{event_id}.json"
    path.write_text(json.dumps(receipt, indent=2))
    return path


def test_live_check_passes_and_paired_blocks_are_intact(tmp_path):
    engine, progress, markdown, _observer = make_engine(tmp_path)
    result = check(engine)
    assert result.ok, result.holds
    text = markdown.read_text()
    assert text.startswith(engine_mod.START)
    assert text.count(engine_mod.START) == 1
    assert "<!-- SOROK_OPERATIONAL_CURRENT_START -->" in text
    data = json.loads(progress.read_text())
    assert data["operational_currentness_live_r1"]["last_check"]["status"] == "NOT_CHECKED"
    assert "operational_currentness_r1" in data


def test_new_accepted_event_not_in_old_snapshot_holds_then_reconciles(tmp_path):
    observer = FixtureObserver(baseline_refs())
    engine, progress, markdown, _ = make_engine(tmp_path, observer)
    old_progress = tmp_path / "old.json"
    old_markdown = tmp_path / "old.md"
    shutil.copyfile(progress, old_progress)
    shutil.copyfile(markdown, old_markdown)

    observer.refs[NEW_REF] = NEW_SHA
    held = check(engine)
    assert not held.ok
    assert any(NEW_REF in hold and NEW_SHA in hold for hold in held.holds), held.holds

    receipt = write_receipt(tmp_path, ref=NEW_REF, sha=NEW_SHA, event_id="NEW_EVENT")
    reconciled = engine.reconcile(receipt)
    assert reconciled.ok, reconciled.holds
    data = json.loads(progress.read_text())
    live = data["operational_currentness_live_r1"]
    assert [event["id"] for event in live["accepted_events"]] == ["NEW_EVENT"]
    assert any(row["action"] == "RECONCILED" for row in live["history"])

    old_engine = engine_mod.CurrentnessEngine(
        progress_path=old_progress, markdown_path=old_markdown,
        receipts_dir=tmp_path / "receipts", evidence_root=tmp_path,
        observer=observer,
    )
    old_result = old_engine.check(write=False)
    assert not old_result.ok
    assert any(NEW_REF in hold for hold in old_result.holds), old_result.holds


def test_unrelated_refs_do_not_block(tmp_path):
    observer = FixtureObserver(baseline_refs())
    observer.refs["refs/heads/voskres/unrelated-r1"] = "a" * 40
    observer.refs["refs/heads/implementation/pyat999-unrelated-r1"] = "b" * 40
    engine, _, _, _ = make_engine(tmp_path, observer)
    result = check(engine)
    assert result.ok, result.holds


def test_pinned_pr_head_drift_holds(tmp_path):
    observer = FixtureObserver(baseline_refs())
    observer.refs["refs/pull/1089/head"] = "d" * 40
    engine, _, _, _ = make_engine(tmp_path, observer)
    result = check(engine)
    assert not result.ok
    assert any("refs/pull/1089/head" in hold for hold in result.holds), result.holds


def test_protected_head_drift_holds_without_receipt(tmp_path):
    observer = FixtureObserver(baseline_refs())
    observer.refs[PROTECTED_REF] = "e" * 40
    engine, _, _, _ = make_engine(tmp_path, observer)
    result = check(engine)
    assert not result.ok
    assert any(hold.startswith("PROTECTED_HEAD_DRIFT") for hold in result.holds), result.holds


def test_receipt_evidence_tamper_is_red(tmp_path):
    observer = FixtureObserver(baseline_refs())
    observer.refs[NEW_REF] = NEW_SHA
    engine, _, _, _ = make_engine(tmp_path, observer)
    receipt_path = write_receipt(tmp_path, ref=NEW_REF, sha=NEW_SHA, event_id="TAMPER_EVENT")
    engine.reconcile(receipt_path)
    evidence = tmp_path / "evidence" / "TAMPER_EVENT.md"
    evidence.write_text("tampered")
    result = check(engine)
    assert not result.ok
    assert any("RECEIPT_INVALID" in hold for hold in result.holds), result.holds


def test_grade_ceiling_rejects_native_or_full_claim(tmp_path):
    observer = FixtureObserver(baseline_refs())
    observer.refs[NEW_REF] = NEW_SHA
    engine, _, _, _ = make_engine(tmp_path, observer)
    receipt = write_receipt(
        tmp_path, ref=NEW_REF, sha=NEW_SHA, event_id="NATIVE_EVENT",
        grade="FULL_NATIVE_ACCEPTED",
    )
    with pytest.raises(engine_mod.CurrentnessError, match="GRADE_CEILING_VIOLATION"):
        engine.reconcile(receipt)


def test_paired_live_md_drift_is_red(tmp_path):
    engine, _progress, markdown, _ = make_engine(tmp_path)
    check(engine)
    text = markdown.read_text()
    markdown.write_text(text.replace("**Status:** NOT_CHECKED", "**Status:** FORGED", 1))
    result = check(engine)
    assert not result.ok
    assert any("PAIRED_LIVE_MD_DRIFT" in hold for hold in result.holds), result.holds


def test_static_snapshot_tamper_is_red(tmp_path):
    engine, progress, _markdown, _ = make_engine(tmp_path)
    data = json.loads(progress.read_text())
    by_id = {row["id"]: row for row in data["operational_currentness_r1"]["tasks"]}
    by_id["B05"]["sourcefree_state"] = "CANDIDATE"
    progress.write_text(json.dumps(data, indent=2))
    result = engine.check(write=True)
    assert not result.ok
    assert any("STATIC_FROZEN" in hold or "STATIC_SNAPSHOT_DRIFT" in hold
               or "PAIRED_WRITE_REFUSED" in hold for hold in result.holds), result.holds


def test_offline_is_explicitly_not_current(tmp_path):
    engine, _, _, _ = make_engine(tmp_path)
    result = engine.check(write=False, offline=True)
    assert result.mode == "OFFLINE"
    assert result.status == "OFFLINE_NOT_CURRENT"
    assert "OFFLINE_NOT_CURRENT" in engine_mod.CurrentnessEngine.render_live_block(result.live)


def test_history_and_static_state_are_preserved_after_reconcile(tmp_path):
    observer = FixtureObserver(baseline_refs())
    observer.refs[NEW_REF] = NEW_SHA
    engine, progress, _markdown, _ = make_engine(tmp_path, observer)
    before = json.loads(progress.read_text())
    receipt = write_receipt(tmp_path, ref=NEW_REF, sha=NEW_SHA, event_id="PRESERVE_EVENT")
    engine.reconcile(receipt)
    after = json.loads(progress.read_text())
    assert after["operational_currentness_r1"] == before["operational_currentness_r1"]
    for key in before:
        if key not in ("operational_currentness_live_r1", "operational_currentness_r1"):
            assert after[key] == before[key]
    assert any(row["event_id"] == "PRESERVE_EVENT" for row in after["operational_currentness_live_r1"]["history"])


def test_stale_last_check_is_a_visible_hold(tmp_path):
    engine, progress, _markdown, _ = make_engine(tmp_path)
    engine.check(write=True)
    assert engine.status().ok
    data = json.loads(progress.read_text())
    data["operational_currentness_live_r1"]["last_check"]["at"] = "2020-01-01T00:00:00+00:00"
    progress.write_text(json.dumps(data, indent=2))
    result = engine.status()
    assert not result.ok
    assert any(hold.startswith("CHECK_STALE") for hold in result.holds), result.holds


def test_receipt_outside_inbox_is_refused(tmp_path):
    observer = FixtureObserver(baseline_refs())
    observer.refs[NEW_REF] = NEW_SHA
    engine, _progress, _markdown, _ = make_engine(tmp_path, observer)
    receipt = write_receipt(tmp_path, ref=NEW_REF, sha=NEW_SHA, event_id="OUTSIDE_EVENT")
    outside = tmp_path / "outside.json"
    outside.write_bytes(receipt.read_bytes())
    with pytest.raises(engine_mod.CurrentnessError, match="RECEIPT_OUTSIDE_INBOX"):
        engine.reconcile(outside)
