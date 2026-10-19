#!/usr/bin/env python3
"""Fresh-process import receipt for every Python module in one run tree."""
from __future__ import annotations

import hashlib
import importlib
import json
import sys
from pathlib import Path

run_dir = Path(sys.argv[1]).resolve()
return_root = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(run_dir))
rows = []
for path in sorted(run_dir.glob("*.py")):
    module_name = path.stem
    module = importlib.import_module(module_name)
    module_file = Path(module.__file__).resolve()
    try:
        rel = module_file.relative_to(return_root).as_posix()
    except ValueError:
        rel = "<outside-return>"
    rows.append(dict(module=module_name, file=rel,
                     sha256=hashlib.sha256(module_file.read_bytes()).hexdigest(),
                     bytes=module_file.stat().st_size))
print(json.dumps(dict(schema="SOROK_M2R4E_IMPORTED_MODULE_RECEIPT@1",
                      python=sys.version.split()[0],
                      run_dir=run_dir.relative_to(return_root).as_posix(),
                      modules=rows), sort_keys=True, indent=2))
