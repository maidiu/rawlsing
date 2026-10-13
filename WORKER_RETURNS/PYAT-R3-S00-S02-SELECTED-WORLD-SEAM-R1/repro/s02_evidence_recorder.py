"""PYAT R3 S00-S02 — evidence recorder for the seam witness.

Executes the full S02 seam witness and records evidence as JSON.
Source-free/retained-source-conditioned: no raw data, no V3, no actor.
"""

from __future__ import annotations

import json
import pathlib
import time

import rawlsing_next.r3_s02_seam_witness as seam


def main() -> dict:
    started = time.time()
    result = seam.run_seam_witness()
    elapsed = time.time() - started

    return {
        "contract_version": seam.SEAM_CONTRACT_VERSION,
        "bundle_id": result["bundle"]["bundle_id"],
        "bundle_content_hash": result["bundle"]["content_hash"],
        "replay_verified": result["replay_verified"],
        "consumer_receipt": result["consumer_receipt"],
        "scenario_a": result["scenario_a"],
        "scenario_b": result["scenario_b"],
        "effects": result["effects"],
        "elapsed_seconds": round(elapsed, 3),
    }


if __name__ == "__main__":
    result = main()
    out = pathlib.Path(__file__).parent / "s02_evidence.json"
    out.write_text(json.dumps(result, indent=2, default=str))
    print(f"evidence written to {out}")
    print(f"replay_verified: {result['replay_verified']}")
    print(f"bundle_content_hash: {result['bundle_content_hash']}")
    print(f"elapsed: {result['elapsed_seconds']}s")
