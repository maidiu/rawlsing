#!/usr/bin/env python3
"""Reusable pure residual check for response codes against declared labels.

No source access, wave launch, inventory, or implicit label inference.
Input is an aggregate code/count map plus the exact declared labels and
physical missing states. Output separates known labels, unlabeled observed
codes, and system/declared missing states.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def residual_check(codes, labels, missing_states=None):
    labels = {str(k): str(v) for k, v in (labels or {}).items()}
    missing_states = dict(missing_states or {})
    out = {"labeled": {}, "unlabeled_observed": {}, "system_missing": {}, "special_labeled": {}}
    for key, count in codes.items():
        value = None if key == "None" else float(key)
        if value is None:
            out["system_missing"][key] = count
        elif str(key) in labels:
            label = labels[str(key)]
            bucket = "labeled"
            if label.strip().lower() in {"not clear", "can't choose/don't know", "don't know", "decline to answer", "refused"}:
                bucket = "special_labeled"
            out[bucket][key] = {"count": count, "label": label}
        else:
            out["unlabeled_observed"][key] = count
    out["all_observed_accounted"] = (
        sum(codes.values())
        == sum(x["count"] for x in out["labeled"].values())
        + sum(x["count"] for x in out["special_labeled"].values())
        + sum(out["unlabeled_observed"].values())
        + sum(out["system_missing"].values())
    )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aggregate", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()
    d = json.loads(Path(args.aggregate).read_text())
    labels = d.get("config", {}).get("q217_labels", d.get("labels", {}))
    result = residual_check(d["q217"]["codes"], labels, d["q217"].get("missing_states"))
    payload = {"schema": "ANVIL_Q217_RESIDUAL_CHECK@1", **result}
    if args.out:
        Path(args.out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
