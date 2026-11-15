from argparse import Namespace
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path("/Users/matthewsmith/.codex/worktrees/sorok982-composite-g5/Rawlsing")
P6 = ROOT / "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1"
sys.path.insert(0, str(P6))

import run_p6
from house import read_house


def run(state, command, request_id, **kwargs):
    return run_p6.experience(state, Namespace(
        command=command, request_id=request_id, duration=None,
        situated_house=True, **kwargs))


def receipt(state):
    return json.loads((state / "p4_receipts.json").read_text())["turns"][-1]["receipt"]


with tempfile.TemporaryDirectory(dir=ROOT / ".local-logs/sorok982-composite-g5/tmp") as td:
    tmp = Path(td)
    base = tmp / "base"
    other = tmp / "other"
    # Same monkeypatch as the author's same-clock test.
    original = run_p6.establish_demo_conditions
    def establish_facing(session):
        original(session)
        world, house = read_house(session)
        house["situated_conditions"] = {
            **house["situated_conditions"], "bench_view": "facing_player",
        }
        session.product._checkpoint(session.branch_id, world.clock, world)
    run_p6.establish_demo_conditions = establish_facing
    run(base, "new", None)
    run(other, "new", None)
    run(base, "approach", "a")
    run(other, "orient", "b")
    a = receipt(base)
    b = receipt(other)
    keys = ("state_id", "receipt_hash", "episode_id", "domain_issuance_id",
            "start", "end", "root_hash", "branch_id", "actor_id")
    print("root_equal", a["interval"]["root_hash"] == b["interval"]["root_hash"])
    print("branch_equal", a["interval"]["branch_id"] == b["interval"]["branch_id"])
    print("start_end", a["interval"]["start"], a["interval"]["end"],
          b["interval"]["start"], b["interval"]["end"])
    for key in keys:
        print(key, a["interval"].get(key) == b["interval"].get(key),
              str(a["interval"].get(key))[:48], str(b["interval"].get(key))[:48])
    print("event_a", a["performed"]["event_id"])
    print("event_b", b["performed"]["event_id"])
    print("kind_a", a["performed"]["kind"], "kind_b", b["performed"]["kind"])
