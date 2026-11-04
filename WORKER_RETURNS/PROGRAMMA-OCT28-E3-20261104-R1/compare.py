"""Summarize exact baseline/E3 replay outputs using the E2 comparison."""
import hashlib
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()

def read(name):
    return json.loads((root / f"{name}.json").read_text())

def digest(value):
    wire = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(wire).hexdigest()

def joined_pair(baseline, candidate):
    base, changed = baseline["result"], candidate["result"]
    parity_keys = ("runs", "p41_consumer_values", "route_outputs", "decoder_roots",
                   "projection_and_authority_roots", "checkpoint_bytes", "source_sha256",
                   "source_bytes", "p41_runtime_scratch_bytes", "p41_commit")
    return {
        "equal": {key: base[key] == changed[key] for key in parity_keys},
        "roots": {key: [digest(base[key]), digest(changed[key])] for key in parity_keys},
        "host_equal": baseline["host"] == candidate["host"],
        "baseline_ms": base["wall_ns"] / 1e6,
        "candidate_ms": changed["wall_ns"] / 1e6,
        "baseline_rss_bytes": baseline["peak_rss"],
        "candidate_rss_bytes": candidate["peak_rss"],
        "phases": [base["phases"], changed["phases"]],
        "storage_bytes": {key: base[key] for key in (
            "checkpoint_bytes", "source_bytes", "p41_runtime_scratch_bytes")},
        "first_consumer": {key: base["runs"][0][key] for key in (
            "refused_reason", "revoked_code", "wrong_source_code", "view_hash")},
    }

summary = {"host": read("base-joined")["host"],
           "joined": [joined_pair(read("base-joined"), read("candidate-joined")),
                      joined_pair(read("base-joined-repeat"), read("candidate-joined-repeat"))],
           "queries": {}}
for rounds in (1, 8, 150):
    base = read(f"base-queries-{rounds}")["result"]
    changed = read(f"candidate-queries-{rounds}")["result"]
    assert set(base) == set(changed)
    summary["queries"][rounds] = {
        label: {"equal": item["results"] == changed[label]["results"],
                "baseline_result_sha256": digest(item["results"]),
                "candidate_result_sha256": digest(changed[label]["results"]),
                "baseline_ms": item["wall_ns"] / 1e6,
                "candidate_ms": changed[label]["wall_ns"] / 1e6,
                "baseline_builds": item["phases"]["index_build"]["calls"] if rounds != 150 else None,
                "candidate_builds": changed[label]["phases"]["index_build"]["calls"] if rounds != 150 else None}
        for label, item in base.items()
    }
print(json.dumps(summary, indent=2, sort_keys=True))
