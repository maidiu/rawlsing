"""Assert exact cross-cut parity and report timings for completed local runs."""
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def load(stem):
    return json.loads((root / (stem + ".json")).read_text())

comparison = load("comparison")
assert all(all(pair["equal"].values()) and pair["host_equal"]
           for pair in comparison["joined"])
assert all(all(case["equal"] for case in cases.values())
           for cases in comparison["queries"].values())
for run in comparison["joined"]:
    before, after = run["phases"]
    assert before["index_build"]["calls"] == 1328
    assert after["index_build"]["calls"] == 6
    print("JOINED", json.dumps({
        "wall_ms": [run["baseline_ms"], run["candidate_ms"]],
        "improvement_percent": (1 - run["candidate_ms"] / run["baseline_ms"]) * 100,
        "rss_bytes": [run["baseline_rss_bytes"], run["candidate_rss_bytes"]],
        "index_build_calls": [p["index_build"]["calls"] for p in (before, after)],
        "index_build_ms": [p["index_build"]["inclusive_ns"] / 1e6 for p in (before, after)],
        "checkpoint": run["storage_bytes"]["checkpoint_bytes"],
        "first_consumer": run["first_consumer"],
    }, sort_keys=True))
by_case = []
for order in ("a", "b"):
    before, after = (load(cut + "-warm-" + order)["result"] for cut in ("e1", "e3"))
    assert set(before) == set(after)
    case_ms = {}
    for case in before:
        assert before[case]["results"] == after[case]["results"]
        case_ms[case] = [before[case]["wall_ns"] / 1e6, after[case]["wall_ns"] / 1e6]
    total_ms = [sum(v[n] for v in case_ms.values()) for n in (0, 1)]
    by_case.append(100 * (total_ms[1] / total_ms[0] - 1))
    print("WARM", json.dumps({
        "order": order, "e1_e3_total_ms": total_ms,
        "e3_change_percent": by_case[-1], "case_ms": case_ms,
    }, sort_keys=True))
instrumented = load("e3-attestation-queries")["result"]
warm = load("e3-warm-b")["result"]
assert all(warm[k]["results"] == v["results"] for k, v in instrumented.items())
for phase in ("index_attestation_match", "index_attestation_create"):
    count = sum(case["phases"][phase]["calls"] for case in instrumented.values())
    nanos = sum(case["phases"][phase]["inclusive_ns"] for case in instrumented.values())
    print("ATTESTATION", json.dumps({
        "phase": phase, "calls": count, "inclusive_ns": nanos,
        "inclusive_ns_per_call": nanos / count,
    }, sort_keys=True))
