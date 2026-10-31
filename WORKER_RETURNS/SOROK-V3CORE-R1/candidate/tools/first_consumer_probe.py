#!/usr/bin/env python3
"""Execute the I1 -> historical material projection first consumer."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for path in (str(ROOT), str(ROOT / "vendor"), str(ROOT / "vendor" / "py3deps")):
    if path not in sys.path:
        sys.path.insert(0, path)

from v3core_adapter.i1_consumer import project_actual_market_event  # noqa: E402
from v3core_adapter.ledger import HistoricalProjection  # noqa: E402
from v3core_adapter.provenance import record_to_dict  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="v3core-i1-consumer-") as directory:
        base = Path(directory)
        ledger = base / "v3core-projection.json"
        result = project_actual_market_event(base / "i1", projection_path=ledger)
        loaded = HistoricalProjection.load(ledger)
        payload = {
            "schema": "SOROK_V3CORE_R1_FIRST_CONSUMER_PROBE@1",
            "status": result.status.value,
            "event_id": result.event_id,
            "observed_world_hash": result.observed_world_hash,
            "source_clock": result.source_clock,
            "source_clock_domain": result.source_clock_domain.value,
            "cash_before": result.cash_before,
            "cash_after": result.cash_after,
            "completed_units_before": result.completed_units_before,
            "completed_units_after": result.completed_units_after,
            "position_before": result.position_before,
            "position_after": result.position_after,
            "material_index_before": result.material_index_before,
            "material_index_after": result.material_index_after,
            "material_index_delta": result.material_index_delta,
            "state_hash_before": result.state_hash_before,
            "state_hash_after": result.state_hash_after,
            "projection_ledger_sha256": __import__("hashlib").sha256(ledger.read_bytes()).hexdigest(),
            "projection_reloaded_hash": loaded.state_hash(),
            "projection_cold_equal": loaded.state_hash() == result.state_hash_after,
            "projection_source_metadata": loaded.source_metadata,
            "c12_counts_before": result.c12_verify_before["counts"],
            "c12_counts_after": result.c12_verify_after["counts"],
            "c12_authenticity": result.c12_verify_after["authenticity"],
            "canonical_c9_claimed": result.canonical_c9_claimed,
            "rival_store_created": result.rival_store_created,
            "year_record": record_to_dict(result.year_record) if result.year_record else None,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
