#!/usr/bin/env python3
"""Fresh-process actual import receipt for the corrected candidate runtime."""
from __future__ import annotations

import hashlib
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
RUNTIME = ROOT / "candidate" / "stage" / "runtime"
sys.path.insert(0, str(ROOT / "candidate"))
sys.path.insert(0, str(RUNTIME))
MODULES = [
    "product.nonparent", "product.scenario", "product.service", "product.world",
    "product.empirical",
    "rawlsing_next.m4_v557_v558_publication_repository",
    "rawlsing_next.m5_runtime_rsc_peer_prior",
    "rawlsing_next.pre553_empirical_possibility_provider",
    "rawlsing_next.pre553_analytical_composition",
    "rawlsing_next.source_backed_positioned_subject_possibility",
    "rawlsing_next.pre553_n9_n10w_progressive_candidate",
]
rows = []
for name in MODULES:
    module = importlib.import_module(name)
    path = Path(module.__file__).resolve()
    try:
        rel = path.relative_to(ROOT).as_posix()
    except ValueError:
        rel = "<outside-return>"
    rows.append(dict(module=name, file=rel,
                     sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                     bytes=path.stat().st_size))
print(json.dumps(dict(schema="SOROK_C0R3_ACTUAL_IMPORTS@1",
                      python=sys.version.split()[0], runtime="candidate/stage/runtime",
                      modules=rows), sort_keys=True, indent=2))
