"""Process-separated first-consumer court over three antecedent histories."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

CLI = Path(__file__).with_name("run_p4.py")
SEVER = """
import run_p4
from p3 import test_rules
test_rules.B1_PATH = test_rules.B1_PATH.with_name("missing-p4-court-source")
raise SystemExit(run_p4.main())
"""


def call(state, *args, sever=False):
    command = ([sys.executable, "-c", SEVER] if sever else
               [sys.executable, str(CLI)])
    process = subprocess.run(
        [*command, "--state", str(state), *args], cwd=CLI.parent,
        capture_output=True, text=True, timeout=90,
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
    )
    assert process.returncode == (2 if sever else 0), process.stderr or process.stdout
    assert not process.stderr, process.stderr
    return json.loads(process.stdout)


def receipts(state):
    return json.loads((state / "p4_receipts.json").read_text())


def footing(view):
    # S44 includes path-bound generated speech IDs in cold fixture roots.
    return {**view, "observations": [
        {k: v for k, v in row.items() if k != "event_id"}
        for row in view["observations"]
    ]}


def test_complete_cell_and_controls(tmp_path):
    root = tmp_path / "joint"
    opening = call(root, "new")
    original = receipts(root)
    assert original["turns"] == []
    assert original["antecedent"]["psychology_head"]["count"] == 1
    assert original["antecedent"]["formation"].startswith("P3_PSYCH:")
    assert opening["clock"] == original["antecedent"]["identity"]["clock"]
    assert any(e["kind"] == "ARRIVAL" for e in opening["observations"])
    assert all(e["kind"] != "SPEECH" for e in opening["observations"])
    assert opening["choices"] == ["SAY", "REQUEST_EDGE"]
    assert opening["invitation"] is None

    # Keep an exact cold checkpoint. S37 refuses relocated live state, so
    # replay it at its original path below.
    alternate = tmp_path / "alternate"
    shutil.copytree(root, alternate)
    text = "  I need a closer look at that edge.  "
    args = ("say", text, "--request-edge", "--request-id", "first")
    rejected = call(root, *args, sever=True)
    assert rejected["status"] == "REFUSED"
    assert rejected["reason"] == "P3_B1_SOURCE_SEVERED"
    assert receipts(root) == original

    first = call(root, *args)
    assert first["performed"] and first["admission"] == "ADMITTED"
    assert call(root, *args) == first
    first_turn = receipts(root)["turns"][0]
    assert first_turn["before"] == original["antecedent"]["identity"]
    speech = first_turn["receipt"]["speech"]
    event = speech["performed"]
    assert event["body"]["text"] == speech["attempt"]["text"] == text
    assert event["body"]["attempt_hash"] == speech["attempt"]["hash"]
    assert speech["actor_access"]["event_id"] == event["event_id"]
    assert event["hash"] in first_turn["receipt"]["uptake"]["readset"]
    # The invitation is the decision boundary, including on a cold reopen.
    assert first_turn["receipt"]["interval"] is None
    assert first["next"]["clock"] == first["observation"]["clock"] == opening["clock"]
    assert call(root, "view") == first["next"]
    from run_p4 import open_owner

    owner = open_owner(root / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        actor = first_turn["receipt"]["uptake"]["actor_alias"]
        assert session.world().actor_state[actor]["material_remaining"] == 1
        assert all(row["domain"]["mode"] != "ACTUAL" for row in session.read_interval_states())
    finally:
        owner.close()

    accepted_path = tmp_path / "accepted"
    root.rename(accepted_path)
    alternate.rename(root)
    try:
        assert receipts(root) == original
        changed = call(root, "say", "Do not invite me to inspect. I am leaving the edge.")
        changed_turn = receipts(root)["turns"][0]
    finally:
        root.rename(alternate)
        accepted_path.rename(root)
    other_event = changed_turn["receipt"]["speech"]["performed"]
    assert changed["performed"] and other_event["hash"] != event["hash"]
    assert changed["observation"] is None and changed["next"]["invitation"] is None
    assert changed_turn["receipt"]["uptake"]["status"] == "PERCEIVED_NO_INSPECTION_REQUEST"
    assert speech["attempt"]["request_edge"] is True
    assert changed_turn["receipt"]["speech"]["attempt"]["request_edge"] is False
    assert other_event["hash"] in changed_turn["receipt"]["uptake"]["readset"]
    assert event["hash"] not in changed_turn["receipt"]["uptake"]["readset"]

    invitation = first["next"]["invitation"]
    assert invitation == first["observation"]["event_id"]
    assert "INSPECT_EDGE" in first["next"]["choices"]
    blank = call(root, "say", "   ")
    assert blank["admission"] == "EMPTY_SPEECH" and not blank["performed"]
    assert blank["observation"] is None and blank["next"] == first["next"]
    blank_turn = receipts(root)["turns"][-1]
    assert blank_turn["receipt"]["speech"]["performed"] is None
    assert blank_turn["receipt"]["uptake"]["status"] == "NOT_PERFORMED"
    assert blank_turn["receipt"]["interval"] is None

    bad = call(root, "inspect-edge", "foreign-invitation", "--then-wait")
    assert not bad["performed"] and bad["next"]["invitation"] == invitation
    assert receipts(root)["turns"][-1]["receipt"]["interval"] is None
    second = call(root, "inspect-edge", invitation, "--then-wait")
    assert second["performed"] and second["observation"]["kind"] == "INSPECT"
    assert second["observation"]["body_public"]["changed"] is False
    assert second["observation"]["clock"] == first["next"]["clock"]
    assert second["next"]["clock"] == first["next"]["clock"] + 2
    assert second["next"]["choices"] == ["SAY", "REQUEST_EDGE"]
    assert call(root, "view") == second["next"]

    turns = receipts(root)["turns"]
    assert [turn["action"]["operation"] for turn in turns] == [
        "SAY", "SAY", "INSPECT_EDGE", "INSPECT_EDGE"]
    for previous, current in zip(turns, turns[1:]):
        assert previous["after"] == current["before"]
    for turn in turns:
        assert all(turn["after"][key] == first_turn["before"][key]
                   for key in ("root", "actor", "branch"))
    assert turns[-1]["receipt"]["invitation"] == invitation
    assert turns[-1]["action"]["then_wait"] is True
    interval = turns[-1]["receipt"]["interval"]
    material = interval["segments"][0]["world"]
    assert material["actual_action_event_id"] and material["actual_action_event_hash"]
    assert material["state_before"]["material_remaining"] == 1
    assert material["state_after"]["material_remaining"] == 0
    owner = open_owner(root / "actual-p2")
    try:
        events = owner.base_owner.fanin.session.events()
        event_ids = [row["event_id"] for row in events]
        assert event_ids.index(second["observation"]["event_id"]) < event_ids.index(
            material["actual_action_event_id"])
    finally:
        owner.close()
    assert turns[-1]["receipt"]["performed"]["event_id"] == second["observation"]["event_id"]

    imposed = tmp_path / "private"
    assert footing(call(imposed, "new", "--history", "imposed_plan")) == footing(opening)
    private = call(imposed, *args)
    assert private["observation"]["body_public"]["text"] != first["observation"]["body_public"]["text"]
    assert private["next"]["choices"] == ["SAY", "REQUEST_EDGE"]
    private_receipt = receipts(imposed)["turns"][0]["receipt"]
    assert private_receipt["speech"]["performed"]["body"]["text"] == text
    assert private_receipt["interval"]["segments"][0]["world"]["state_before"] == material["state_before"]

    empty = tmp_path / "empty"
    assert footing(call(empty, "new", "--history", "")) == footing(opening)
    assert receipts(empty)["antecedent"]["psychology_head"]["count"] == 0
    valid_empty = call(empty, *args)
    assert valid_empty["performed"] and valid_empty["next"]["choices"] == ["SAY", "REQUEST_EDGE"]
    assert valid_empty["observation"]["body_public"]["text"] != private["observation"]["body_public"]["text"]

    outputs = json.dumps([opening, first, blank, second, private, valid_empty])
    for private_token in ("V3MS_MEDIATOR", "recognized_plan", "imposed_plan",
                          "actor_access", "readset", "attempt_hash", "psyche",
                          "private_check", "joint_check"):
        assert private_token not in outputs
