"""RRIF-E terminal repair: C12 verifier, self-exclusion, custody, compatibility."""
from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

R2 = Path(__file__).resolve().parents[1]
EXT = R2 / "rrif_r3_extension"
REPO = Path(__file__).resolve().parents[5]
for path in (str(R2), str(EXT), str(REPO)):
    if path not in sys.path:
        sys.path.insert(0, path)

from joined.c12_custody import coordinated_guard_report
from joined.c12_verify_repair import upstream_defect_is_reproducible, verify_branch_chain_repaired
from joined.c9c12_compat import INCOMPATIBLE, read_c9c12_compatibility
from joined.first_consumer import run_first_consumer
from joined.session import JoinedSession
from joined.source_identity import audit_candidate_preimage
from r26e.c12_integrity import QualifiedC12Store
from r30a.first_session import SessionRefusal


def _session(tmp_path: Path, name: str = "state") -> tuple[Path, Path]:
    state = tmp_path / name
    session = JoinedSession.start(state, perform="omit", attention="focused")
    product = session.product.root
    session.close()
    return state, product


def _episode(db_path: Path):
    db = sqlite3.connect(db_path)
    try:
        return db.execute(
            "SELECT branch_id,seq,episode_id,actor_id,kind,clock,body,hash "
            "FROM episode WHERE branch_id='root' ORDER BY seq LIMIT 1").fetchone()
    finally:
        db.close()


def _rewrite_episode(db_path: Path, body: str, body_hash: str, actor_id: str) -> None:
    db = sqlite3.connect(db_path)
    try:
        db.execute("DROP TRIGGER IF EXISTS episode_no_update")
        db.execute("UPDATE episode SET body=?, hash=?, actor_id=? "
                   "WHERE branch_id='root' AND seq=0", (body, body_hash, actor_id))
        db.execute("DROP TRIGGER IF EXISTS perception_no_update")
        db.execute("UPDATE perception SET actor_id='FORGED_ACTOR' "
                   "WHERE branch_id='root' AND seq=0")
        db.commit()
    finally:
        db.close()


def test_repaired_c12_verifier_intact_green_upstream_known_defect_tamper_red_restore(tmp_path):
    _state, product = _session(tmp_path)
    db_path = product / "c12.sqlite"
    qualified = QualifiedC12Store(db_path)
    try:
        report = upstream_defect_is_reproducible(qualified, "root")
        assert report["repaired_ok"] is True, report
        assert report["upstream_ok"] is False
        assert any("body_hash_mismatch" in error for error in report["upstream_errors"])
        assert qualified.verify("root")["ok"] is True
    finally:
        qualified.close()
    backup = tmp_path / "clean.sqlite"
    backup.write_bytes(db_path.read_bytes())
    branch, seq, episode_id, actor_id, kind, clock, body, body_hash = _episode(db_path)
    parsed = json.loads(body)
    parsed["rrif_e_tamper"] = True
    tampered = json.dumps(parsed, sort_keys=True, separators=(",", ":"))
    db = sqlite3.connect(db_path)
    try:
        db.execute("DROP TRIGGER IF EXISTS episode_no_update")
        db.execute("UPDATE episode SET body=? WHERE branch_id='root' AND seq=0", (tampered,))
        db.commit()
    finally:
        db.close()
    qualified = QualifiedC12Store(db_path)
    try:
        assert verify_branch_chain_repaired(qualified, "root")["ok"] is False
        assert any("body_hash_mismatch" in error for error in verify_branch_chain_repaired(qualified, "root")["errors"])
    finally:
        qualified.close()
    db_path.write_bytes(backup.read_bytes())
    qualified = QualifiedC12Store(db_path)
    try:
        restored = verify_branch_chain_repaired(qualified, "root")
        assert restored["ok"] is True, restored
    finally:
        qualified.close()


def test_source_preimage_excludes_itself_and_hashes_every_other_file():
    report = audit_candidate_preimage(R2)
    assert report["ok"] is True, report["errors"]
    assert report["files"] == 638
    assert report["self_excluded"] == "RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json"
    assert report["source_manifest_sha256"] == hashlib.sha256((R2 / "SOURCE_MANIFEST.json").read_bytes()).hexdigest()
    assert report["self_exclusion"]["content_addressed"] is False


def test_coordinated_column_branch_and_perception_tamper_is_guarded_red_then_restore(tmp_path):
    _state, product = _session(tmp_path)
    db_path = product / "c12.sqlite"
    backup = tmp_path / "clean.sqlite"
    backup.write_bytes(db_path.read_bytes())
    branch, seq, episode_id, actor_id, kind, clock, body, body_hash = _episode(db_path)
    parsed = json.loads(body)
    parsed["branch_id"] = "forged_origin"
    preimage = {key: value for key, value in parsed.items() if key not in {"hash", "episode_id"}}
    from bp1.canon import digest
    forged_hash = digest(preimage)
    parsed["hash"] = forged_hash
    forged_body = json.dumps(parsed, sort_keys=True, separators=(",", ":"))
    _rewrite_episode(db_path, forged_body, forged_hash, actor_id)
    report = coordinated_guard_report(db_path, branch_id="root")
    assert report["qualified"]["ok"] is True, report
    assert report["guarded"]["ok"] is False, report
    assert report["classification"] == "SELF_HASH_ONLY__TRUST_CUSTODY_HOLD"
    assert report["external_owner_anchor"] == "OWNER_ANCHOR_REQUIRED"
    assert report["authenticity_claimed"] is False
    assert any("branch_id_origin" in error or "actor_not_in_branch" in error
               for error in report["guarded"]["errors"])
    db_path.write_bytes(backup.read_bytes())
    restored = coordinated_guard_report(db_path, branch_id="root")
    assert restored["qualified"]["ok"] is True
    assert restored["guarded"]["ok"] is True
    assert restored["classification"].startswith("BOTH_GREEN")
    assert restored["external_owner_anchor"] == "OWNER_ANCHOR_REQUIRED"


def test_c9_c12_compatibility_is_exact_owner_held(tmp_path):
    _state, product = _session(tmp_path)
    report = read_c9c12_compatibility(product)
    assert report["status"] == INCOMPATIBLE
    assert report["c12_root"]["ok"] is True
    assert report["c9_actor"]["status"] == "C9_SOURCE_MISSING"
    assert "actor_meta" in report["c9_actor"]["reason"]
    assert report["legacy_first_session"]["fork_status"] == "LEGACY_HELD"
    assert report["cp_a5_same_root"]["code"] == "BP2_ORIGIN_INVARIANT_MISMATCH"
    assert report["owner_migration_required"] is True
    assert report["external_owner_anchor"] == "OWNER_ANCHOR_REQUIRED"
    assert report["native_person"] is False


def test_first_consumer_executes_same_root_and_separate_cp_a5(tmp_path):
    receipt = run_first_consumer(tmp_path / "consumer")
    assert receipt["status"].startswith("PASS_PARTIAL_SAME_ROOT_C9_C12")
    same = receipt["same_root"]
    assert same["cold_verify_ok"] is True
    assert same["c12"]["repaired_root"]["ok"] is True
    assert same["c12"]["repaired_alt"]["ok"] is True
    assert same["c12"]["upstream_defect_reproduced"]["upstream_ok"] is False
    assert same["c12"]["custody"]["classification"].startswith("BOTH_GREEN")
    assert same["c9c12_compatibility"]["status"] == INCOMPATIBLE
    assert receipt["cp_a5"]["assertion_status"] == "PASS"
    assert receipt["cp_a5"]["market_status"] == "UNKNOWN"
    assert receipt["cp_a5"]["ask_status"] == "UNKNOWN"
    assert receipt["cp_a5"]["same_root_with_r2"] is False
    assert receipt["authority"]["native_person"] is False
    assert receipt["authority"]["external_anchor"] == "OWNER_ANCHOR_REQUIRED"


def test_refusal_and_nochange_are_distinct(tmp_path):
    probe = JoinedSession.probe_refusal(tmp_path / "refusal")
    assert probe["status"] == "HOLD"
    assert probe["target_id"] == ""
    assert probe["c9"]["target_branch"] == "NO_CHANGE"
    assert probe["c9"]["target_reason"] == "NO_PROPOSAL"
    session = JoinedSession.start(tmp_path / "nochange", perform="omit")
    try:
        attended = session.attend()
        assert attended["status"] == "NO_CHANGE"
        assert session.verify()["ok"] is True
    finally:
        session.close()
