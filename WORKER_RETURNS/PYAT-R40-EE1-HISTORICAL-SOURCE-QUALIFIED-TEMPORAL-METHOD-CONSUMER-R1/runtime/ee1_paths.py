"""EE1 path bootstrap: repo sealed sources + staged accepted T35 world.

Import order discipline (this module is imported by tests/conftest.py before
any test module):
  * the worktree root is appended to sys.path so the sealed `data.*` and
    `rawlsing_next.*` modules resolve to this branch's exact bytes;
  * the staged accepted T35 runtime directory is inserted FIRST so the
    generic module names `bootstrap`, `product`, `two_epoch_world` and
    `e05_n9_selected_world_adapter` resolve to the staged upstream blobs.
"""
from __future__ import annotations

import sys
from pathlib import Path

PACKET = Path(__file__).resolve().parents[1]
RUNTIME = PACKET / "runtime"
STAGED_WORLD = RUNTIME / "selected_world"
REPO = PACKET.parents[1]

_INSTALLED = False


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    if str(REPO) not in sys.path:
        sys.path.append(str(REPO))
    if str(STAGED_WORLD) not in sys.path:
        sys.path.insert(0, str(STAGED_WORLD))
    _INSTALLED = True
