"""Read-only S49 person plus recovered historical V3 source import."""
from __future__ import annotations

import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
S49_RETURN = REPO / "WORKER_RETURNS" / "SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1"
SOURCE_ROOT = Path(
    "/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging"
)
IDENTITIES = Path(
    "/Users/matthewsmith/.codex/worktrees/10f2/Rawlsing/WORKER_COMMISSIONS/"
    "SOROK-20261025-S50-HISTORICAL-V3-ACTOR-RECOVERY-R1/"
    "01_SOURCE_IDENTITIES.json"
)
CUTS = {
    "s49": "6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43",
}
_INSTALLED = False


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    for path in (str(RETURN), str(S49_RETURN), str(SOURCE_ROOT)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)
    from s49.bootstrap import install as s49_install

    s49_install()
    import s49  # noqa: F401

    from .yaml_compat import install as yaml_install

    yaml_install()
    _INSTALLED = True


def roots() -> dict:
    install()
    value = {
        "s50_return": str(RETURN),
        "s49_return": str(S49_RETURN),
        "source_root": str(SOURCE_ROOT),
        "source_identities": str(IDENTITIES),
        "cuts": dict(CUTS),
    }
    return value


__all__ = ["CUTS", "IDENTITIES", "RETURN", "S49_RETURN", "SOURCE_ROOT", "install", "roots"]
