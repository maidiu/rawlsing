"""Same-world P6 gaze counterfactual through the real frozen entry points.

Run from the repository root with:
  /private/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q \
    WORKER_RETURNS/SOROK-P6-GAZE-PROOF-20261107-R1/test_gaze_proof.py

The two variants start from one byte-identical P6 state snapshot, at the same
state root path. Only the prior attention/exposure history is changed. The
actual user conduct sequence, objective world, clock and Nadia's episodes are
identical.
"""
from __future__ import annotations

from argparse import Namespace
import json
from pathlib import Path
import shutil
import sys

RETURNS = Path(__file__).resolve().parents[1]
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
sys.path.insert(0, str(P6))

from run_p6 import experience, open_owner, read_house  # noqa: E402


def _run(state, command, **kwargs):
    return experience(state.resolve(), Namespace(command=command, request_id=None, **kwargs))


def _seed_attention(state, target):
    (state / "p6_gaze.json").write_text(json.dumps({
        "history": [{
            "target": target,
            "turn": 0,
            "shown": False,
            "available": ["bench", "mug"],
        }],
        "exposure": {"room": "workshop", "detail": target},
    }))


def _observe(state):
    owner = open_owner(state.resolve() / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        _, house = read_house(session)
        return {
            "snapshot": owner.snapshot().document(),
            "ledger": json.loads((state / "p4_receipts.json").read_text()),
            "clock": session.world().clock,
            "positions": dict(session.world().positions),
            "house": house,
            "nadia_episodes": list(session.episodes("A")),
            "user_perceived_ids": list(session.user_perceived_ids()),
            "gaze": json.loads((state / "p6_gaze.json").read_text()),
        }
    finally:
        owner.close()


def _run_variant(state, initial, target):
    if state.exists():
        shutil.rmtree(state)
    shutil.copytree(initial, state)
    _seed_attention(state, target)
    first_view = _run(state, "view")
    for command, kwargs in (
        ("go", {"target": "living room"}),
        ("look", {"target": "sandals"}),
        ("go", {"target": "workshop"}),
    ):
        _run(state, command, **kwargs)
    return first_view, _observe(state)


def test_same_world_attention_counterfactual(tmp_path):
    state = tmp_path / "state"
    initial = tmp_path / "initial"

    opening = _run(state, "new")
    assert opening["clock"] == 248
    assert opening["room"] == "workshop"
    # One actual world snapshot is restored for each attention variant.
    shutil.copytree(state, initial)

    left_view, left_state = _run_variant(state, initial, "bench")
    right_view, right_state = _run_variant(state, initial, "mug")

    # Optional phenomenal detail differs through the real P6 selector.
    assert left_view["room"] == right_view["room"] == "workshop"
    assert left_view["available"] == right_view["available"] == ["bench", "mug"]
    assert left_view["detail"] == "The bench stands beside the doorway."
    assert right_view["detail"] == "A mug stands beside the bench."
    assert left_view["detail"] != right_view["detail"]
    assert left_view["clock"] == right_view["clock"]

    # Attention is not actual conduct: committed world, user conduct, clock and
    # Nadia's episodes remain identical.
    assert left_state["clock"] == right_state["clock"] == 253
    assert left_state["positions"] == right_state["positions"]
    assert left_state["snapshot"] == right_state["snapshot"]
    assert left_state["ledger"] == right_state["ledger"]
    assert left_state["house"] == right_state["house"]
    assert left_state["nadia_episodes"] == right_state["nadia_episodes"]
    assert left_state["user_perceived_ids"] == right_state["user_perceived_ids"]

    # The differing earlier attention remains confined to gaze history/detail.
    assert left_state["gaze"]["exposure"]["detail"] == "bench"
    assert right_state["gaze"]["exposure"]["detail"] == "mug"
    assert left_state["gaze"] != right_state["gaze"]
    assert all(left_state[key] == right_state[key] for key in (
        "snapshot", "ledger", "clock", "positions", "house",
        "nadia_episodes", "user_perceived_ids"))
