"""E41 return bootstrap: repo-root sys.path setup for imports.

The E41 tranche code imports only accepted in-tree modules (``rawlsing_next``)
and modules from this return directory. Nothing here mutates accepted owners.
"""
from __future__ import annotations

import sys
from pathlib import Path

RETURN_DIR = Path(__file__).resolve().parent


def _repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "rawlsing_next").is_dir() and (candidate / "WORKER_RETURNS").is_dir():
            return candidate
    raise RuntimeError("repo root not found from E41 return bootstrap")


ROOT = _repo_root()


def ensure_paths() -> Path:
    for path in (str(ROOT), str(RETURN_DIR)):
        if path not in sys.path:
            sys.path.insert(0, path)
    # Accepted test-support material (frozen fixtures) is importable as
    # ``rawlsing_next.tests``; the flat-name helpers used by those modules need
    # the tests directory on the path as well (same convention as the accepted
    # fixture modules themselves use).
    tests_dir = str(ROOT / "rawlsing_next" / "tests")
    if tests_dir not in sys.path:
        sys.path.insert(0, tests_dir)
    return ROOT


ensure_paths()
