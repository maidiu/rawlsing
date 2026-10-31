"""Same-consumer tests for CP-A5 multicontact life and read-only encounter."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from cp_a5.assertion import ASSERTION_NAME, run_a5_assertion
from cp_a5.encounter import EncounterReader, EncounterRefusal, render_encounter
from cp_a5.scenario import build_cp_life

RETURN = Path(__file__).resolve().parents[1]


def _env() -> dict:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_intact_multicontext_life_reaches_the_a5_assertion(intact, tmp_path):
    root = tmp_path / "life"
    _, trace = build_cp_life(root, intact)
    receipt = run_a5_assertion(root)
    assert receipt["status"] == "PASS"
    assert receipt["assertion"] == ASSERTION_NAME
    assert receipt["decision"] == "RETAIN_TOOL"
    assert receipt["evidence"]["inspection_count"] >= 3
    assert len(receipt["evidence"]["contexts"]) == 2
    assert receipt["material"]["b_cash"] == 58
    assert receipt["material"]["b_completed_units"] == 5
    assert receipt["material"]["a_material_remaining"] == 1
    assert receipt["material"]["a_completed_units"] == 5
    assert receipt["material"]["tool_available"] is True
    assert receipt["read_only"] is True
    assert receipt["encounter"]["tool"]["status"] == "OK"
    assert receipt["encounter"]["market"]["status"] == "UNKNOWN"
    with EncounterReader(root) as reader:
        events = reader.all_events()
        known_ids = set(reader.view()["known_event_ids"])
        assert "B_MARKET_COMMISSION" not in [
            event["kind"] for event in events
            if event["event_id"] in known_ids]
        assert "B_TAKE_TOOL" in [
            event["kind"] for event in events
            if event["event_id"] in known_ids]
        commission = next(event for event in events
                          if event["kind"] == "B_MARKET_COMMISSION")
        assert commission["body"]["material_delta"] == 0
        assert commission["body"]["cash_delta"] == 2
    assert trace["event_ids"]["B_MARKET_COMMISSION"]


def test_sever_b_independent_activity_reddens_then_exact_restore_greens(
        intact, tmp_path):
    intact_root = tmp_path / "intact"
    fault_root = tmp_path / "fault"
    build_cp_life(intact_root, intact)
    build_cp_life(fault_root, intact, include_b_activity=False)
    with pytest.raises(AssertionError) as error:
        run_a5_assertion(fault_root)
    assert "A4_B_INDEPENDENT_ACTIVITY_MISSING" in str(error.value)
    backup = tmp_path / "intact.sqlite"
    shutil.copy2(intact_root / "c12.sqlite", backup)
    shutil.copy2(backup, fault_root / "c12.sqlite")
    restored = run_a5_assertion(fault_root)
    assert restored["status"] == "PASS"


def test_removing_a_access_makes_the_tool_unknown(intact, tmp_path):
    root = tmp_path / "life"
    build_cp_life(root, intact, grant_a_access=False)
    with EncounterReader(root) as reader:
        view = reader.view()
        assert view["known_event_ids"]
        assert len(view["known_event_ids"]) < len(reader.all_events())
        tool = reader.ask("What happened to the workshop tool?")
        assert tool["status"] == "UNKNOWN"
        assert "who moved" in tool["answer"]
    with pytest.raises(AssertionError) as error:
        run_a5_assertion(root)
    assert "A5_A_TOOL_ACCESS_MISSING" in str(error.value)


def test_actor_or_branch_identity_swap_is_refused(intact, tmp_path):
    root = tmp_path / "life"
    build_cp_life(root, intact)
    with pytest.raises(EncounterRefusal) as error:
        EncounterReader(root, actor_id="B")
    assert error.value.code == "ENCOUNTER_ACTOR_SWAP_REFUSED"
    with pytest.raises(EncounterRefusal) as error:
        EncounterReader(root, branch_id="not-a-branch")
    assert error.value.code == "ENCOUNTER_BRANCH_REFUSED"


def test_renderer_output_change_does_not_mutate_canonical_state(intact, tmp_path):
    root = tmp_path / "life"
    build_cp_life(root, intact)
    with EncounterReader(root) as reader:
        before = reader.canonical_digest()
        before_changes = reader.total_changes()
        view = reader.view()
        plain = render_encounter(view, "plain")
        compact = render_encounter(view, "compact")
        after = reader.canonical_digest()
        after_changes = reader.total_changes()
        assert plain != compact
        assert before == after == view["canonical_digest"]
        assert before_changes == after_changes
        with pytest.raises(ValueError):
            render_encounter(view, "unknown")


def test_missing_custody_rule_emits_held_not_a_decision(intact, tmp_path):
    root = tmp_path / "life"
    _, trace = build_cp_life(root, intact, custody_rule=False)
    assert "A4_CUSTODY_DECISION" not in trace["event_ids"]
    assert trace["event_ids"]["A4_CUSTODY_HELD"]
    with EncounterReader(root) as reader:
        events = reader.all_events()
        held = [event for event in events
                if event["kind"] == "A4_CUSTODY_HELD"]
        assert held[-1]["body"]["state"] == "HELD"
        assert held[-1]["body"]["code"] == "MISSING_CUSTODY_RULE"
        assert not any(event["body"].get("decision") == "RETAIN_TOOL"
                       for event in events if event["kind"] == "A4_CUSTODY_HELD")
    with pytest.raises(AssertionError) as error:
        run_a5_assertion(root)
    assert "A4_CUSTODY_DECISION_MISSING" in str(error.value)


def test_single_context_inspection_is_insufficient(intact, tmp_path):
    root = tmp_path / "life"
    _, trace = build_cp_life(root, intact, context_profile="single_context")
    assert trace["inspection_evidence"]["qualified"] is False
    assert len(trace["inspection_evidence"]["contexts"]) == 1
    assert trace["event_ids"]["A4_CUSTODY_HELD"]
    with pytest.raises(AssertionError) as error:
        run_a5_assertion(root)
    assert "A3_CONTEXT_EVIDENCE_INSUFFICIENT" in str(error.value)


def test_fork_after_acquired_activity_preserves_parent(intact, tmp_path):
    from bp2p4.i1_product import GuardedJoinedProduct

    root = tmp_path / "life"
    build_cp_life(root, intact)
    with EncounterReader(root) as base:
        parent_digest = base.canonical_digest()
        parent = base.product
        fork = parent.fork("alt")
        assert fork["shared_root"]["equal"] is True
        parent.use("alt")
        base.branch_id = "alt"
        assert parent.inspect()["status"] == "NO_CHANGE"
        assert parent.say("child-only life")["status"] == "OK"
        assert parent.verify_c12()["ok"] is True
        child_digest = base.canonical_digest()
        assert child_digest != parent_digest
    restored = run_a5_assertion(root)
    assert restored["status"] == "PASS"
    with EncounterReader(root, branch_id="alt") as child:
        assert child.canonical_digest() == child_digest
    assert _sha(root / "c12.sqlite")


def test_cold_process_cli_loads_history_without_writing(intact, tmp_path):
    root = tmp_path / "cli"
    scenario = subprocess.run(
        [sys.executable, str(RETURN / "run_cp_a5.py"), "--root", str(root),
         "scenario"], capture_output=True, text=True, env=_env())
    assert scenario.returncode == 0, scenario.stderr
    trace = json.loads(scenario.stdout)
    assert trace["schema"] == "SOROK_CP_A5_SCENARIO_TRACE@1"
    database = root / "life" / "c12.sqlite"
    before = _sha(database)
    encounter = subprocess.run(
        [sys.executable, str(RETURN / "run_cp_a5.py"), "--root", str(root),
         "encounter", "What happened to the workshop tool?"],
        capture_output=True, text=True, env=_env())
    assert encounter.returncode == 0, encounter.stderr
    answer = json.loads(encounter.stdout)
    assert answer["status"] == "OK"
    assert answer["read_only"] is True
    assert _sha(database) == before
    assertion = subprocess.run(
        [sys.executable, str(RETURN / "run_cp_a5.py"), "--root", str(root),
         "assert"], capture_output=True, text=True, env=_env())
    assert assertion.returncode == 0, assertion.stderr
    assert json.loads(assertion.stdout)["status"] == "PASS"
    assert _sha(database) == before
