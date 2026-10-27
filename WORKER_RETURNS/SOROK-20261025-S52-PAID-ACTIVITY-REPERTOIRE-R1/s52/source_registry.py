"""Portable F0-R2 source registry loaded before any S49/S51/G18 import.

This module intentionally does not import the S51 package: importing the package
would execute its ``__init__`` and session before custody verification.  The
standalone S51 ``source_binding.py`` file is loaded by path and verifies the
bounded source manifest under the new F0-R2-owned directory.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Mapping

REPO = Path(__file__).resolve().parents[3]
S51 = REPO / "WORKER_RETURNS" / "SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1"
BINDING = S51 / "s51" / "source_binding.py"


def _binding():
    existing = sys.modules.get("s51.source_binding")
    if existing is not None:
        return existing
    if not BINDING.is_file():
        raise RuntimeError(f"SOURCE_BINDING_MISSING: {BINDING}")
    spec = importlib.util.spec_from_file_location("_f0_r2_source_binding", BINDING)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"SOURCE_BINDING_UNLOADABLE: {BINDING}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_roots() -> dict[str, Any]:
    """Resolve the bounded F0 closure without importing its packages."""
    return _binding().source_roots(S51, REPO)


def verify_dependencies(roots: Mapping[str, Any] | None = None) -> bool:
    """Verify the complete bounded closure; raise before any managed import."""
    binding = _binding()
    value = roots if roots is not None else source_roots()
    binding.verify_sources(value)
    return True


__all__ = ["BINDING", "REPO", "S51", "source_roots", "verify_dependencies"]
