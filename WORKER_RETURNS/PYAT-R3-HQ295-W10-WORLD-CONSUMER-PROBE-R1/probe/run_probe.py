#!/usr/bin/env python3
"""Execute the W10 world-consumer probe and write outputs/ artifacts.

Run from the repository root:
  python3 -m WORKER_RETURNS.PYAT-R3-HQ295-W10-WORLD-CONSUMER-PROBE-R1.probe.run_probe
or:
  python3 WORKER_RETURNS/PYAT-R3-HQ295-W10-WORLD-CONSUMER-PROBE-R1/probe/run_probe.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
PROBE_ROOT = Path(__file__).resolve().parents[1]
if str(PROBE_ROOT) not in sys.path:
    sys.path.insert(0, str(PROBE_ROOT))

from probe.e05_vertical_experiment import run_full_experiment  # noqa: E402


def main() -> int:
    result = run_full_experiment()
    out_dir = PROBE_ROOT / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "experiment_result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (out_dir / "consumer_receipt_A.json").write_text(
        json.dumps(result["receipt_a"], indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (out_dir / "consumer_receipt_B.json").write_text(
        json.dumps(result["receipt_b"], indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (out_dir / "hostile_oracle_results.json").write_text(
        json.dumps(
            {
                "positive_oracles": result["positive_oracles"],
                "hostile_oracles": result["hostile_oracles"],
                "typed_refusals": result["typed_refusals"],
                "replay_and_invalidation": result["replay_and_invalidation"],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    overall = result["overall"]
    lines = [
        f"experiment_id: {result['experiment_id']}",
        f"grade: {result['grade']}",
        f"positive_oracles_pass: {overall['positive_oracles_pass']}",
        f"hostile_oracles_pass: {overall['hostile_oracles_pass']}",
        f"typed_refusals_pass: {overall['typed_refusals_pass']}",
        f"replay_invalidation_pass: {overall['replay_invalidation_pass']}",
        f"sourcefree_interface_court_pass: {overall['sourcefree_interface_court_pass']}",
        f"integrated_n9_n10w_pass: {overall['integrated_n9_n10w_pass']}",
        f"receipt_a_replay_hash: {result['receipt_a_replay_hash']}",
        f"receipt_b_replay_hash: {result['receipt_b_replay_hash']}",
        f"n10e_lane_hash: {result['n10e_lane']['provider_receipt_hash']}",
        f"metrics: {json.dumps(result['metrics'], sort_keys=True)}",
    ]
    (out_dir / "run_log.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if overall["sourcefree_interface_court_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
