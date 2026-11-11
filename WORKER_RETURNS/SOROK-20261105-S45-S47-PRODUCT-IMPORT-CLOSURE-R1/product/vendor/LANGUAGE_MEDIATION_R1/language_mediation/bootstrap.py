"""Import the unchanged prior JOIN-E return before any J/E module.

The language experiment does not vendor or edit the returned code.  The
accepted WORKER_RETURNS tree supplies the real ``JoinedSession``, C12 store and
R31E expression port; this module only places that tree on ``sys.path`` and
lets ``joined.imports`` install its documented J-first/E-second closure.
"""
from __future__ import annotations

import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
WORKER_ROOT = Path(__file__).resolve().parents[2]
RETURN_ROOT = (
    WORKER_ROOT / "WORKER_RETURNS" / "SOROK-20261022-SAME-PERSON-JOIN-R1"
)
_INSTALLED = False


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    for path in (str(PACKAGE_ROOT), str(RETURN_ROOT)):
        if path not in sys.path:
            sys.path.insert(0, path)
    import joined.session  # noqa: F401  # installs the documented J/E closure
    _INSTALLED = True


__all__ = ["install", "PACKAGE_ROOT", "RETURN_ROOT"]
