#!/usr/bin/env python3
"""Helpers for recording exact run invocation provenance."""

from __future__ import annotations

import json
import shlex
import sys
from pathlib import Path
from typing import Any, Mapping


def capture_run_provenance(
    *,
    input_documents: Mapping[str, Any] | None = None,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    argv = [str(arg) for arg in sys.argv]
    provenance: dict[str, Any] = {
        "invocation_command": shlex.join(argv),
        "invocation_argv": argv,
        "invocation_executable": sys.executable,
        "invocation_cwd": str(Path.cwd()),
        "invocation_script_path": str(Path(argv[0]).resolve()) if argv else "",
        "input_documents": dict(input_documents or {}),
    }
    if extra:
        provenance.update(dict(extra))
    return provenance


def provenance_json(provenance: Mapping[str, Any]) -> str:
    return json.dumps(dict(provenance), sort_keys=True, ensure_ascii=False)
