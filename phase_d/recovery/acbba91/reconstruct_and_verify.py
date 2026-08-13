#!/usr/bin/env python3
"""Reconstruct and verify the exact historical d49e55c -> acbba91 Git bundle."""
from __future__ import annotations

import base64
import hashlib
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
STEM = "Rawlsing_PreV553_Wiring_Contract_Repair_acbba91.bundle.b64.part"
OUT = HERE / "Rawlsing_PreV553_Wiring_Contract_Repair_acbba91.bundle"
EXPECTED_SHA256 = "7ed342080215ed605551b96c1d0e0ec2b90a83f53e0a913fc35a3d299eb528fa"
EXPECTED_BASE = "d49e55c9f2df86c5412be8759b9ad6ca86778262"
EXPECTED_TARGET = "acbba91de28b9cee20af05e81e4d8bfdaa876298"

parts = [HERE / f"{STEM}{i:02d}" for i in range(1, 9)]
missing = [str(p) for p in parts if not p.exists()]
if missing:
    raise SystemExit("missing recovery payload parts: " + ", ".join(missing))

encoded = "".join(p.read_text(encoding="ascii").strip() for p in parts)
try:
    raw = base64.b64decode(encoded, validate=True)
except Exception as exc:
    raise SystemExit(f"base64 reconstruction failed: {exc}")

sha = hashlib.sha256(raw).hexdigest()
if sha != EXPECTED_SHA256:
    raise SystemExit(f"SHA256 FAIL expected={EXPECTED_SHA256} actual={sha}")

OUT.write_bytes(raw)
print(f"PASS bundle={OUT}")
print(f"sha256={sha}")
print(f"required_base={EXPECTED_BASE}")
print(f"target={EXPECTED_TARGET}")
