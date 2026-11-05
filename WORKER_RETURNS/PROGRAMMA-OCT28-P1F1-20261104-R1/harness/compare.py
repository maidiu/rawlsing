"""Verify native and P41 parity before summarizing the paired runs."""
from hashlib import sha256
import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
labels = (
    "base-a", "compact-cold", "compact-warm", "base-b", "compact-corrupt", "compact-deleted",
)
runs = {label: json.loads((root / f"{label}.json").read_bytes()) for label in labels}
baseline = runs["base-a"]

def native(record):
    return {key: value for key, value in record["result"].items()
            if key not in ("wall_ns", "phases")}

def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

stats = {}
for label, record in runs.items():
    assert record["host"] == baseline["host"], label
    assert native(record) == native(baseline), label
    counts = record["p1"]["counts"]
    maxima = record["p1"]["maxima"]
    if label.startswith("compact"):
        assert maxima["compact_event_count"] > 0, label
        assert not maxima.get("eager_event_count", 0), label
        assert not counts.get("exact_event_reconstructions", 0), label
        if label == "compact-warm":
            assert counts["cache_hit"] == counts["compact_view_builds"], label
            assert not counts.get("cache_miss", 0), label
        else:
            assert counts["cache_miss"] > 0 and counts["cache_publications"] > 0, label
    stats[label] = {
        "wall_seconds": record["result"]["wall_ns"] / 1e9,
        "peak_rss_bytes": record["peak_rss"],
        "resources": record["p1"],
        "phases": record["result"]["phases"],
    }
material = native(baseline)
print(json.dumps({
    "host": baseline["host"],
    "native_material_sha256": digest(material),
    "p41_view_hash": material["runs"][0]["view_hash"],
    "checkpoint_lengths": material["checkpoint_bytes"],
    "runs": stats,
}, indent=2, sort_keys=True))
