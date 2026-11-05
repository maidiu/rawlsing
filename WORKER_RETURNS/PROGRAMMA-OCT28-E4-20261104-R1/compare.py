"""Assert parity and report timing differences from independent captures."""
from hashlib import sha256
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])

def read(label):
    return json.loads((root / (label + ".json")).read_bytes())

def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def compare_joined(labels):
    baseline = None
    results = {}
    for label in labels:
        run = read(label)
        result = run["result"]
        material = {k: v for k, v in result.items() if k not in ("wall_ns", "phases")}
        if baseline is None:
            baseline = material
        assert material == baseline, label
        results[label] = {
            "wall_seconds": result["wall_ns"] / 1e9,
            "peak_rss_bytes": run["peak_rss"],
            "phases": result["phases"],
        }
    return {"exact_material_sha256": digest(baseline),
            "checkpoint_lengths": baseline["checkpoint_bytes"],
            "p41_view_hash": baseline["runs"][0]["view_hash"],
            "results": results}

def compare_queries(labels):
    baseline = None
    results = {}
    for label in labels:
        run = read(label)
        material = {key: case["results"] for key, case in run["result"].items()}
        if baseline is None:
            baseline = material
        assert material == baseline, label
        results[label] = {
            "sum_case_wall_seconds": sum(case["wall_ns"] for case in run["result"].values()) / 1e9,
            "peak_rss_bytes": run["peak_rss"],
            "cases": {key: {k: v for k, v in case.items() if k != "results"}
                      for key, case in run["result"].items()},
        }
    return {"exact_case_sha256": {key: digest(value) for key, value in baseline.items()},
            "results": results}

joined = compare_joined(("joined-base-a", "joined-e3-a", "joined-e3-b", "joined-base-b"))
for suffix in ("a", "b"):
    b = joined["results"][f"joined-base-{suffix}"]
    e = joined["results"][f"joined-e3-{suffix}"]
    joined[f"wall_reduction_percent_{suffix}"] = 100 * (1 - e["wall_seconds"] / b["wall_seconds"])
queries = {
    str(rounds): compare_queries([f"queries-{cut}-{rounds}" for cut in ("base", "e1", "e3")])
    for rounds in (1, 8)
}
queries["150"] = compare_queries(("warm-e1-a", "warm-e3-a", "warm-e3-b",
                                  "warm-e1-b", "attestation"))
assert queries["1"]["exact_case_sha256"] == queries["8"]["exact_case_sha256"]
assert queries["8"]["exact_case_sha256"] == queries["150"]["exact_case_sha256"]
for suffix in ("a", "b"):
    results = queries["150"]["results"]
    old = results[f"warm-e1-{suffix}"]["sum_case_wall_seconds"]
    new = results[f"warm-e3-{suffix}"]["sum_case_wall_seconds"]
    queries["150"][f"e3_wall_delta_percent_{suffix}"] = 100 * (new / old - 1)
attestation = {}
for phase in ("index_attestation_match", "index_attestation_create"):
    samples = [case["phases"][phase] for case in queries["150"]["results"]["attestation"]["cases"].values()]
    calls = sum(sample["calls"] for sample in samples)
    ns = sum(sample["inclusive_ns"] for sample in samples)
    attestation[phase] = {"calls": calls, "total_ns": ns, "mean_ns": ns / calls}

native = {}
for path in sorted((root / "native-base").glob("*.json")):
    data = path.read_bytes()
    for cut in ("e1", "e3"):
        assert data == (root / f"native-{cut}" / path.name).read_bytes(), (cut, path.name)
    native[path.name] = {"bytes": len(data), "sha256": sha256(data).hexdigest()}
assert "native.json" in native and any(name.startswith("checkpoint-") for name in native)
assert native["checkpoint-0.json"]["bytes"] == joined["checkpoint_lengths"][0]
print(json.dumps({"host": read("joined-base-a")["host"],
                  "joined": joined, "queries": queries,
                  "attestation": attestation, "native_byte_parity": native},
                 sort_keys=True, indent=2))
