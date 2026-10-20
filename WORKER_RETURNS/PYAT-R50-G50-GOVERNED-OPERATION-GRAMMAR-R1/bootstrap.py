"""R50 G50 bootstrap: repo-root and return-dir import paths."""
from __future__ import annotations

import sys
from pathlib import Path

RETURN_DIR = Path(__file__).resolve().parent


def _repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "rawlsing_next").is_dir() and (candidate / "WORKER_RETURNS").is_dir():
            return candidate
    raise RuntimeError("repo root not found from G50 return")


ROOT = _repo_root()


def ensure_paths() -> None:
    for path in (str(ROOT), str(RETURN_DIR)):
        if path not in sys.path:
            sys.path.insert(0, path)


ensure_paths()
