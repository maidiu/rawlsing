"""Generate a sourcefree P4 starting life from an actual I03 observed-sample target.

Invoke with PYTHONPATH=. python3 <this file>; optional --state keeps the selected
playable roots. Each calibration rehearsal uses an isolated disposable root.
"""
import argparse
import json
import os
from fractions import Fraction
from pathlib import Path
from random import Random
import subprocess
import sys
from tempfile import TemporaryDirectory

from history_conditioning import (
    Alternative, ConditionedHistories, PopulationConstraint, constrained_world_range,
    identified_range, raw_joint,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate, _build_source, _query, _query_authority, _registry, _run,
)

CLI = Path(__file__).resolve().parents[2] / "WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/run_p4.py"
HISTORY = {"recognized": "recognized_plan", "imposed": "imposed_plan", "no_record": ""}
# An explicit fictional proposal law, independent of release, actor and observation.
BASE = {
    "start": (Alternative("recognized", Fraction(1, 3)), Alternative("remaining", Fraction(2, 3))),
    "remaining": (Alternative("imposed", Fraction(1, 2)), Alternative("no_record", Fraction(1, 2))),
}


def call(root, *args):
    run = subprocess.run([sys.executable, str(CLI), "--state", str(root), *args],
                         env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), text=True,
                         capture_output=True, timeout=120)
    if run.returncode:
        raise RuntimeError(run.stdout + run.stderr)
    return json.loads(run.stdout)


def observe(root):
    """Read public instrument items. Private ledger verifies who acted; it supplies no answer."""
    response = call(root, "say", "May I look at that edge?", "--request-edge", "--request-id", "first")
    turn, = json.loads((root / "p4_receipts.json").read_text())["turns"]
    r = turn["receipt"]
    if not response["performed"] or r["uptake"]["status"] != "UPTAKE":
        raise ValueError("question not administered and taken up")
    public = response["observation"]
    if not public or public["event_id"] != r["expression"]["event_id"]:
        raise ValueError("actor expression lacked a matching observable event")
    view = call(root, "view")
    if view != response["next"]:
        raise ValueError("cold first consumer did not recover the interaction")
    invited = view["invitation"] == public["event_id"]
    if invited != ("INSPECT_EDGE" in view["choices"]):
        raise ValueError("public invitation and available operation disagree")
    return ("1", str(int(invited))), {
        "mode": r["uptake"]["mode"], "expression_hash": r["expression"]["hash"],
        "formation": json.loads((root / "p4_receipts.json").read_text())["antecedent"]["formation"],
        "readset": r["uptake"]["readset"], "invitation": view["invitation"],
    }


def generation(out, temp):
    observed, traces = {}, {}
    for name, history in HISTORY.items():
        root = temp / name
        call(root, "new", "--history", history)
        observed[name], traces[name] = observe(root)
    evidence = {"grade": "SOURCEFREE_RESEARCH", "observations": observed, "calibration": traces, "runs": []}
    for invitations in (1, 3):
        # Matched, explicitly fictional observation protocol on distinct respondents.
        tag = f"edge-protocol-{invitations}"
        source = _build_source(tag, [
            {"id": f"r{i}", "responses": {"replied": 1, "invited": int(i < invitations)}}
            for i in range(4)
        ])
        authority = _query_authority(tag)
        predicate = _branch_predicate(source, authority)
        query = _query(source, authority, predicate, ("replied", "invited"))
        fact, = _run(source, authority, predicate, query).facts
        cells = raw_joint(source["repo"], query, predicate, _registry(source, authority),
                          [source["release_ref"]], fact.ref)
        model = ConditionedHistories("start", BASE, observed, cells)
        path = model.draw(Random(7))
        selected = path[-1]
        root = out / tag
        call(root, "new", "--history", HISTORY[selected])
        # The live actor has not received the rehearsal question or its desired answer.
        if json.loads((root / "p4_receipts.json").read_text())["turns"]:
            raise ValueError("counterfactual calibration leaked into generated present")
        live_cell, live = observe(root)
        if live_cell != observed[selected]:
            raise ValueError("calibration did not transport to the fresh owner root")
        if live["invitation"]:
            inspection = call(root, "inspect-edge", live["invitation"], "--request-id", "second")
            if not inspection["performed"]:
                raise ValueError("selected first consumer failed to perform inspection")
            live["inspection_performed"] = True
        # Distinct question: how often will the actor explicitly request a private check?
        bounds = identified_range(cells, observed, {n: int(t["mode"] == "private_check")
                                                     for n, t in traces.items()})
        # One unit per current P4 fictional world. In a household library each
        # entry counts all eligible units within its whole, indivisible world.
        constraints = [PopulationConstraint(fact.ref.key, probability, tuple(
            (int(observed[name] == cell), 1) for name in HISTORY
        )) for cell, probability in cells.items()]
        outcome = tuple(int(traces[name]["mode"] == "private_check") for name in HISTORY)
        vertices = constrained_world_range(constraints, outcome, basis_budget=10)
        assert tuple(v for v, _ in vertices) == bounds
        # Independent hypothetical information about the frequency of imposed
        # histories must survive. Its incompatibility is an engineering result.
        fixed = PopulationConstraint("HYPOTHETICAL_HALF_IMPOSED", Fraction(1, 2),
                                     tuple((int(n == "imposed"), 1) for n in HISTORY))
        try:
            fixed_range = constrained_world_range(constraints + [fixed], outcome, basis_budget=10)
            fixed_result = [str(value) for value, _ in fixed_range]
        except ValueError as exc:
            if str(exc) != "incompatible constraints on supplied world library":
                raise
            fixed_result = str(exc)
        evidence["runs"].append({
            "release": source["release_ref"].as_dict(), "query": query.ref.as_dict(),
            "fact": fact.ref.as_dict(), "ordered_targets": ["replied", "invited"],
            "cell_mass": {"".join(k): str(v) for k, v in cells.items()},
            "history_mass": {k: str(v) for k, v in model.leaf_mass.items()},
            "private_check_sharp_bounds": list(map(str, bounds)), "draw_seed": 7,
            "extremal_whole_root_weights": [dict(zip(HISTORY, map(str, w))) for _, w in vertices],
            "also_requiring_half_imposed_hypothetically": fixed_result,
            "path": path, "live_cell": live_cell, "live": live,
        })
    return evidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path)
    args = parser.parse_args()
    with TemporaryDirectory() as temp:
        print(json.dumps(generation(args.state or Path(temp) / "selected", Path(temp)), indent=2))
