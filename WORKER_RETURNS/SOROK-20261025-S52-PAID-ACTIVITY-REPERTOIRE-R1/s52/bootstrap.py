"""Install S52 over the accepted S51/S49 and actual G18 sources."""
from __future__ import annotations

import sys
from pathlib import Path

from .source_registry import source_roots, verify_dependencies

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
S51 = REPO / "WORKER_RETURNS" / "SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1"
S49 = REPO / "WORKER_RETURNS" / "SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1"
CUTS = {
    "s51": "2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65",
    "s49": "6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43",
}
_INSTALLED = False


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    verify_dependencies(source_roots())
    for path in (str(RETURN), str(S51), str(S49)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)
    from s51.bootstrap import install as s51_install
    from s51.bootstrap import roots as s51_roots

    s51_install()
    s51_roots()
    import s51  # noqa: F401
    _INSTALLED = True


def roots() -> dict:
    install()
    from s51.bootstrap import roots as s51_roots

    value = s51_roots()
    value.update(
        {
            "s52_return": str(RETURN),
            "s51_return": str(S51),
            "s49_return": str(S49),
            "dependency_verified": True,
            "source_verified": True,
            "source_manifest": str(
                REPO / "WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/source_manifest.json"
            ),
        }
    )
    value["cuts"].update(CUTS)
    return value


__all__ = ["CUTS", "RETURN", "S49", "S51", "install", "roots"]
