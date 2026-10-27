"""S51 over accepted S49 plus the actual G18 root history source."""
from __future__ import annotations

import sys
from pathlib import Path

from .source_binding import resolve_g18, verify_g18, verify_sources

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
S49 = REPO / "WORKER_RETURNS" / "SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1"
CUTS = {"s49": "6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43"}
_INSTALLED = False
G18: Path | None = None


def _g18() -> Path:
    global G18
    if G18 is None:
        G18 = resolve_g18(RETURN, REPO)
        verify_g18(G18)
    return G18


def install() -> None:
    global G18, _INSTALLED
    if _INSTALLED:
        return
    verification = verify_sources(check_cache=True)
    g18 = Path(verification["roots"]["g18"])
    G18 = g18
    verify_g18(g18)
    for path in (str(RETURN), str(S49), str(g18)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)
    from s49.bootstrap import install as s49_install

    s49_install()
    import s49  # noqa: F401
    import lab_sgi1.history  # noqa: F401
    _INSTALLED = True


def roots() -> dict:
    install()
    verification = verify_sources(check_cache=False)
    return {
        "s51_return": str(RETURN),
        "s49_return": str(S49),
        "g18_source": verification["roots"]["g18"],
        "g18_source_verified": True,
        "source_verified": True,
        "source_manifest": verification["manifest"],
        "source_count": verification["verified"],
        "cuts": dict(CUTS),
    }


__all__ = [
    "CUTS",
    "G18",
    "RETURN",
    "S49",
    "install",
    "roots",
]
