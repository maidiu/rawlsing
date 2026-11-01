from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys

import pytest

EXT = Path(__file__).resolve().parents[1]
R2 = EXT.parent
REPO = Path(__file__).resolve().parents[5]

sys.path.insert(0, str(EXT))

from cp_a5_consumer import ask_cp_a5, run_cp_a5_consumer, view_cp_a5
from c9c12_consumer import read_r2_c12, read_r2_c9_snapshot


def _r2_state(tmp_path: Path) -> Path:
    state = tmp_path / "r2-state"
    code = (
        "from joined.session import JoinedSession\n"
        f"s=JoinedSession.start({str(state)!r}, perform='omit', attention='focused')\n"
        "s.close()\n"
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = str(R2) + os.pathsep + str(REPO)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    run = subprocess.run([sys.executable, "-B", "-c", code], cwd=str(REPO),
                         env=env, text=True, capture_output=True, timeout=120)
    assert run.returncode == 0, run.stderr[-3000:]
    return state


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_cp_a5_real_encounter_consumer_grounds_tool_and_keeps_market_unknown(tmp_path):
    root = tmp_path / "cp-a5"
    receipt = run_cp_a5_consumer(root)
    assert receipt["status"] == "PASS"
    assert receipt["assertion"] == "cp_a5.assertion.multicontext_encounter_assertion"
    assert receipt["decision"] == "RETAIN_TOOL"
    assert receipt["encounter"]["tool"]["status"] == "OK"
    assert receipt["encounter"]["market"]["status"] == "UNKNOWN"
    assert receipt["read_only"] is True
    view = view_cp_a5(root)
    assert view["observed_event_count"] > view["accessed_event_count"]
    assert view["unperceived_event_count"] > 0
    before = _sha(root / "c12.sqlite")
    answer = ask_cp_a5(root, "What did B do at the market?")
    assert answer["status"] == "UNKNOWN"
    assert answer["read_only"] is True
    assert _sha(root / "c12.sqlite") == before


def test_cp_a5_severed_b_activity_reddens_then_exact_restore_greens(tmp_path):
    intact = tmp_path / "intact"
    run_cp_a5_consumer(intact)
    backup = tmp_path / "intact-c12.sqlite"
    shutil.copy2(intact / "c12.sqlite", backup)
    fault = tmp_path / "fault"
    with pytest.raises(AssertionError, match="A4_B_INDEPENDENT_ACTIVITY_MISSING"):
        run_cp_a5_consumer(fault, include_b_activity=False)
    shutil.copy2(backup, fault / "c12.sqlite")
    from cp_a5.assertion import run_a5_assertion
    restored = run_a5_assertion(fault)
    assert restored["status"] == "PASS"


def test_cp_a5_same_root_r2_cut_conflict_is_exact(tmp_path):
    state = _r2_state(tmp_path)
    with pytest.raises(Exception) as exc:
        ask_cp_a5(state / "product", "What happened to the workshop tool?")
    text = str(exc.value)
    assert "ENCOUNTER_BRANCH_REFUSED" in text
    assert "BP2_ORIGIN_INVARIANT_MISMATCH" in text
    assert "TEST_ONLY_BP1_ACTOR_A" in text
    assert "TEST_ONLY_BP1_R26V_ACTOR_A" in text


def test_cp_a5_actor_swap_is_refused(tmp_path):
    from cp_a5.encounter import EncounterReader, EncounterRefusal
    root = tmp_path / "cp-a5"
    run_cp_a5_consumer(root)
    with pytest.raises(EncounterRefusal) as exc:
        EncounterReader(root, actor_id="B")
    assert exc.value.code == "ENCOUNTER_ACTOR_SWAP_REFUSED"


def test_c9c12_reader_really_reads_r2_root_c12(tmp_path):
    state = _r2_state(tmp_path)
    result = read_r2_c12(state / "product")
    assert result["status"] == "C12_COLD_READ_OK"
    assert result["ok"] is True
    assert result["content_ok"] is True
    assert result["schema_ok"] is True
    assert result["fork_status"] == "VERIFIED"
    assert result["counts"]["episode"] > 0
    assert result["anchor_status"]["code"] == "OWNER_ANCHOR_REQUIRED"
    assert result["consumer"] == "C9C12_R2_GUARDED_C12_COLD_READ_ON_RRIF_R2"


def test_c9c12_actor_snapshot_is_source_missing_on_r2_product(tmp_path):
    state = _r2_state(tmp_path)
    result = read_r2_c9_snapshot(state / "product")
    assert result["status"] == "C9_SOURCE_MISSING"
    assert "no such table: actor_meta" in result["reason"]


def test_c9c12_legacy_branch_is_held_not_green(tmp_path):
    state = _r2_state(tmp_path)
    result = read_r2_c12(state / "product", branch_id="first_session")
    assert result["status"] == "C12_HELD"
    assert result["fork_status"] == "LEGACY_HELD"
    assert any("legacy_root_unverified" in error for error in result["errors"])


def test_c9c12_tampered_episode_is_red_then_exact_restore_greens(tmp_path):
    state = _r2_state(tmp_path)
    c12 = state / "product" / "c12.sqlite"
    backup = tmp_path / "c12-clean.sqlite"
    shutil.copy2(c12, backup)
    db = sqlite3.connect(c12)
    try:
        row = db.execute("SELECT branch_id,seq,body FROM episode WHERE branch_id='root' ORDER BY seq LIMIT 1").fetchone()
        assert row is not None
        branch_id, seq, body = row
        parsed = json.loads(body)
        parsed["rrif_r3_tamper"] = True
        db.execute("DROP TRIGGER IF EXISTS episode_no_update")
        db.execute("UPDATE episode SET body=? WHERE branch_id=? AND seq=?",
                   (json.dumps(parsed, sort_keys=True, separators=(",", ":")), branch_id, seq))
        db.commit()
    finally:
        db.close()
    damaged = read_r2_c12(state / "product")
    assert damaged["ok"] is False
    assert any("body_hash_mismatch" in error or "C12" in error for error in damaged["errors"])
    shutil.copy2(backup, c12)
    restored = read_r2_c12(state / "product")
    assert restored["status"] == "C12_COLD_READ_OK"
    assert restored["fork_status"] == "VERIFIED"


def test_cp_a5_consumer_survives_r2_joined_import(tmp_path):
    from joined.session import JoinedSession
    state = tmp_path / "joined"
    session = JoinedSession.start(state, perform="omit", attention="focused")
    session.close()
    root = tmp_path / "cp-a5"
    receipt = run_cp_a5_consumer(root)
    assert receipt["status"] == "PASS"
    assert receipt["decision"] == "RETAIN_TOOL"
