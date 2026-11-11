"""Independent adverse probes for MII final checkpoint 49720bf."""

from argparse import Namespace
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
P6 = ROOT / "WORKER_RETURNS" / "SOROK-P6-ONE-LIVING-HOUSE-R1"
P5 = ROOT / "WORKER_RETURNS" / "SOROK-P5-CONTINUOUS-EXPERIENCE-R1"
P4 = ROOT / "WORKER_RETURNS" / "SOROK-P4-FIRST-FULL-MPC-R1"
P3 = ROOT / "WORKER_RETURNS" / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
for path in (P6, P5, P4, P3 / "tests"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from run_p6 import experience


def _run(state, command, **kwargs):
    kwargs.setdefault("request_id", None)
    return experience(state, Namespace(command=command, **kwargs))


def test_candidates_and_offered_are_distinct(tmp_path):
    state = tmp_path / "candidates"
    opening = _run(state, "new")
    profile = json.loads((state / "p6_gaze.json").read_text(encoding="utf8"))
    entry = profile["exposures"][-1]
    assert set(entry["candidates"]) == {"bench", "mug"}
    assert list(entry["offered"]) == [opening["mii_surface"]["optional"]["target"]]
    assert entry["candidates"]["mug"] != entry["offered"].get("mug")


def test_duplicate_look_does_not_double_count_adaptive_evidence(tmp_path):
    state = tmp_path / "duplicate"
    _run(state, "new")
    _run(state, "go", target="living room")
    _run(state, "mii-enable-learning")
    first = _run(state, "look", target="sandals", request_id="same-look")
    first_weight = json.loads((state / "p6_gaze.json").read_text(encoding="utf8"))[
        "hypotheses"]["sandals"]["weight"]
    _run(state, "look", target="sandals", request_id="same-look")
    second_weight = json.loads((state / "p6_gaze.json").read_text(encoding="utf8"))[
        "hypotheses"]["sandals"]["weight"]
    assert second_weight == first_weight, (first, second_weight)
