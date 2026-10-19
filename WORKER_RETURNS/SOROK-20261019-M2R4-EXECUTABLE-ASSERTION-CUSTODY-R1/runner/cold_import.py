#!/usr/bin/env python3
"""Fresh-process import receipt for one exact kernel run tree."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

run_dir = Path(sys.argv[1]).resolve()
return_root = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(run_dir))
import kernel  # noqa: E402

module_file = Path(kernel.__file__).resolve()
try:
    module_rel = module_file.relative_to(return_root).as_posix()
except ValueError:
    module_rel = "<outside-return>"
try:
    cwd_rel = Path.cwd().resolve().relative_to(return_root).as_posix()
except ValueError:
    cwd_rel = "<outside-return>"
sys_path_rel = []
for entry in sys.path[:3]:
    try:
        sys_path_rel.append(Path(entry).resolve().relative_to(return_root).as_posix())
    except (ValueError, OSError):
        sys_path_rel.append("<external>")
payload = dict(
    schema="SOROK_M2R4E_COLD_IMPORT@1",
    module="kernel",
    module_file=module_rel,
    module_sha256=hashlib.sha256(module_file.read_bytes()).hexdigest(),
    rule=kernel.RULE,
    rule_hash=kernel.RULE_HASH,
    python=sys.version.split()[0],
    implementer=sys.implementation.name,
    cwd=cwd_rel,
    sys_path_first=sys_path_rel,
    imported_kernel_is_exact_local_file=module_file.is_file(),
)
print(json.dumps(payload, sort_keys=True, indent=2))
