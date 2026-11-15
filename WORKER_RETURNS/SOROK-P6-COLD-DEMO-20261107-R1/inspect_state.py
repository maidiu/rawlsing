#!/usr/bin/env python3
"""Read-only P6 house history evidence for the demo state."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
P6 = REPO / "WORKER_RETURNS" / "SOROK-P6-ONE-LIVING-HOUSE-R1"
sys.path.insert(0, str(P6))

from run_p6 import open_owner, read_house


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, type=Path)
    args = parser.parse_args()
    state = args.state.resolve()
    try:
        owner = open_owner(state / "actual-p2")
        try:
            _, house = read_house(owner.base_owner.fanin.session)
            payload = {
                "epoch": house["epoch"],
                "root": house["root"],
                "history": house["history"],
                "objects": house["objects"],
            }
        finally:
            owner.close()
    except Exception as exc:
        print(json.dumps({"status": "ERROR", "reason": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(payload, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
