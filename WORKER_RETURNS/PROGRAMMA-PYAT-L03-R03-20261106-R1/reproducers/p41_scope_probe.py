"""Reviewer-only instrumentation: verify the P41 issued path constructs and uses
the grouped scope. Does not modify implementation/source."""
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
_CREATED = []


class _SpyScope(_REAL):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _CREATED.append(self)


issued.I03GroupedExecutionScope = _SpyScope

from rawlsing_next.tests.test_universal_world_binding import (  # noqa: E402
    _materialize_p41_runtime,
    _same_source_connected,
)

runtime, base = _materialize_p41_runtime()
try:
    _same_source_connected(str(runtime))
finally:
    shutil.rmtree(base, ignore_errors=True)

receipts = [dict(scope.receipt()) for scope in _CREATED]
payload = {
    "scope_count": len(receipts),
    "scopes_with_builds": sum(1 for r in receipts if r["core_builds"] > 0),
    "scopes_with_hits": sum(1 for r in receipts if r["core_hits"] > 0),
    "total_builds": sum(r["core_builds"] for r in receipts),
    "total_hits": sum(r["core_hits"] for r in receipts),
    "total_fallbacks": sum(r["fallbacks"] for r in receipts),
    "total_capacity_fallbacks": sum(r["capacity_fallbacks"] for r in receipts),
    "receipts": receipts,
}
out = ROOT / ".local-logs/pyat-l03-r03/evidence/p41_scope_probe.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(payload, indent=1, sort_keys=True))
print(json.dumps(payload, indent=1, sort_keys=True))
