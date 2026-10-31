"""SOROK BP4 — sourcefree C10/C12 continuing person/world and A0-A3 alpha.

TEST_ONLY technical product. Not native C12, not C11, not an ADP/CAN issuer.
The package composes actual pinned sourcefree carriers:
  - BP1 per-actor historical ledgers / G18 material-action receipts
  - BP3 keyed exclusive C8 occurrence writer and verified C9 event ingress
  - C9R durable C9 target and later performed E2 consumer
  - current M6 actor-safe expression ingress
"""
from __future__ import annotations

import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
REPO = RET.parents[1]
for _path in (RET / "vendor", RET / "vendor" / "c9r", RET / "vendor" / "bp3", REPO):
    _text = str(_path)
    if _text not in sys.path:
        sys.path.insert(0, _text)

__all__ = ["RET", "REPO"]
