#!/usr/bin/env python3
"""Execute the frozen S-M-LAB1 trial plan and retain every run."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
if str(LAB_ROOT) not in sys.path:
    sys.path.insert(0, str(LAB_ROOT))

from lab.experiment import run_full_lab  # noqa: E402


def main() -> int:
    prereg_raw = (LAB_ROOT / "02_FROZEN_PREREGISTRATION.json").read_bytes()
    prereg_hash = hashlib.sha256(prereg_raw).hexdigest()
    result = run_full_lab(prereg_hash)

    out = LAB_ROOT / "outputs"
    (out / "runs").mkdir(parents=True, exist_ok=True)

    runs = result["runs"]
    for k_id in runs:
        for contrast in runs[k_id]:
            for baseline in runs[k_id][contrast]:
                for seed, receipt in runs[k_id][contrast][baseline].items():
                    path = out / "runs" / f"{k_id}__{contrast}__{baseline}__{seed}.json"
                    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")

    summary = {k: v for k, v in result.items() if k != "runs"}
    summary["preregistration_hash"] = prereg_hash
    (out / "primary_results.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )

    lines = [
        f"preregistration_hash: {prereg_hash}",
        f"trial_count: {result['trial_count']}",
        f"phase1_integrity: {result['integrity']['phase1_integrity']}",
        f"phase2_state: {result['integrity']['phase2_state']}",
        f"hard_invariants_pass: {result['integrity']['hard_invariants_pass']}",
        f"null_controls_all_pass: {result['null_controls']['all_pass']}",
        f"opacity_all_pass: {result['opacity']['all_pass']}",
        f"A_equals_B_equals_C: {result['comparison'].get('A_equals_B_equals_C_on_correctness')}",
        f"decision_law_branch: {result['comparison'].get('decision_law_branch')}",
        f"wall_seconds: {result['wall_seconds']}",
    ]
    for k_id, score in sorted(result["scores"].items()):
        frac = {
            b: score["per_baseline"][b]["fraction"] for b in ("A", "B", "C")
        }
        lines.append(f"score {k_id}: {frac}")
    (out / "run_log.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
