#!/usr/bin/env python3
"""Cold-process readback for a SOROK V3CORE-R1 projection ledger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for path in (str(ROOT), str(ROOT / "vendor"), str(ROOT / "vendor" / "py3deps")):
    if path not in sys.path:
        sys.path.insert(0, path)

from v3core_adapter.ledger import HistoricalProjection  # noqa: E402
from v3core_adapter.quarantine import forbidden_default_reasons  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger")
    args = parser.parse_args(argv)
    projection = HistoricalProjection.load(args.ledger)
    payload = {
        "schema": "SOROK_V3CORE_R1_COLD_PROBE@1",
        "state_hash": projection.state_hash(),
        "years": len(projection.years),
        "applied_event_ids": list(projection.applied_event_ids),
        "cash": projection.state.capacity.money,
        "material_facts": dict(projection.material_facts),
        "forbidden_default_reasons": forbidden_default_reasons(projection.state),
        "canonical_c9_claimed": projection.canonical_c9_claimed,
        "rival_store_created": projection.rival_store_created,
        "authority": projection.authority,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
