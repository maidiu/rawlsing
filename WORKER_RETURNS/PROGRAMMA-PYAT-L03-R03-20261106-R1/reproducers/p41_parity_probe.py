"""Reviewer-only P41 grouped-vs-forced-unshared parity probe. No source edits."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve()
while not (ROOT / 'rawlsing_next').is_dir():
    if ROOT.parent == ROOT:
        raise RuntimeError('repository root not found')
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

import rawlsing_next.pre553_issued_workload as issued  # noqa: E402

_REAL = issued.I03GroupedExecutionScope


class _ClosedScope(_REAL):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.close()


def _run(runtime, source_path, forced_closed):
    issued.I03GroupedExecutionScope = _ClosedScope if forced_closed else _REAL
    from rawlsing_next.tests.test_universal_world_binding import _same_source_connected

    return _same_source_connected(runtime, source_path)


def main():
    from rawlsing_next.tests.test_universal_world_binding import (
        _materialize_p41_runtime,
    )

    source_path = ROOT / ".local-logs/pyat-l03-r03/tmp/p41-parity-source.sav"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    runtime, base = _materialize_p41_runtime()
    runtime = str(runtime)
    try:
        grouped = _run(runtime, source_path, False)
        unshared = _run(runtime, source_path, True)
    finally:
        shutil.rmtree(base, ignore_errors=True)
        issued.I03GroupedExecutionScope = _REAL
    grouped_hashes = json.dumps(grouped["hashes"], sort_keys=True)
    unshared_hashes = json.dumps(unshared["hashes"], sort_keys=True)
    payload = {
        "schema": "R03_P41_GROUPED_VS_UNSHARED_PARITY@1",
        "hashes_equal": grouped_hashes == unshared_hashes,
        "view_hash_equal": grouped["view"].view_hash == unshared["view"].view_hash,
        "view_state_equal": grouped["view"].state == unshared["view"].state,
        "consumer_values_equal": (
            grouped["view"].consumer_values_read == unshared["view"].consumer_values_read
        ),
        "grouped_hashes": grouped["hashes"],
        "unshared_hashes": unshared["hashes"],
    }
    out = ROOT / ".local-logs/pyat-l03-r03/evidence/p41_grouped_vs_unshared.json"
    out.write_text(json.dumps(payload, indent=1, sort_keys=True))
    print(json.dumps({k: v for k, v in payload.items() if k not in (
        "grouped_hashes", "unshared_hashes",
    )}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
