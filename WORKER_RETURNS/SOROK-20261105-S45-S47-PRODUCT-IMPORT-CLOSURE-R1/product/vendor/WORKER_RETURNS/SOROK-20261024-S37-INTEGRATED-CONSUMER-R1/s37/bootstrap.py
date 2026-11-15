"""Exact read-only import roots for the S37 integrated consumer.

The S37 return vendors only the small pinned M35 producer surface.  The warm
JOIN-E closure, the accepted S36 return and the accepted language-mediation
checkout are used read-only.  After M35 installs its closure, the S36 candidate
is deliberately loaded at the front so the actual S36 pipeline (not the older
warm C9R copy) is the one consumed.
"""
from __future__ import annotations

import importlib
import importlib.util
import os
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
DEFAULT_M35 = RETURN / "vendor" / "m35"
DEFAULT_JOIN_E = Path(
    "/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/"
    "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1"
)
DEFAULT_LANGUAGE = Path(
    "/Users/matthewsmith/repos/rawlsing-controller/.worktrees/"
    "sorok-incumbent-attachment/.local-logs/sorok-attachment/"
    "language-consumer-r3/worker/LANGUAGE_MEDIATION_R1"
)
DEFAULT_S36 = (
    REPO / "WORKER_RETURNS" / "SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1"
)

M35_RETURN = Path(os.environ.get("S37_M35_RETURN", str(DEFAULT_M35))).resolve()
JOIN_E_RETURN = Path(
    os.environ.get("S37_JOIN_E_RETURN", str(DEFAULT_JOIN_E))
).resolve()
LANGUAGE_RETURN = Path(
    os.environ.get("S37_LANGUAGE_RETURN", str(DEFAULT_LANGUAGE))
).resolve()
S36_RETURN = Path(os.environ.get("S37_S36_RETURN", str(DEFAULT_S36))).resolve()

CUTS = {
    "m35": "4170fbf19a9d5a64bc728f5b22156bbffcec51e5",
    "s36": "8da78d8031a06a4bd7e1297fd713e573299c0860",
    "language": "8d2920da951f98cd8246d7c34cac777928e0c732",
    "join_e": "7bf2da302996491ddf34b9a039fea47ac982d135",
}

_ORIGINS: dict[str, str] = {}
_INSTALLED = False


def _require(path: Path, label: str) -> None:
    if not path.exists():
        raise ImportError(f"S37_{label}_ROOT_MISSING:{path}")


def _insert_front(path: Path) -> None:
    text = str(path)
    if text in sys.path:
        sys.path.remove(text)
    sys.path.insert(0, text)


def _forget_candidate() -> None:
    for name in list(sys.modules):
        if name == "candidate" or name.startswith("candidate."):
            del sys.modules[name]


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    _require(M35_RETURN, "M35")
    _require(JOIN_E_RETURN, "JOIN_E")
    _require(LANGUAGE_RETURN, "LANGUAGE")
    _require(S36_RETURN, "S36")
    os.environ.setdefault("M35_JOIN_E_RETURN", str(JOIN_E_RETURN))

    _insert_front(M35_RETURN)
    spec = importlib.util.spec_from_file_location(
        "_s37_m35_install", M35_RETURN / "install.py"
    )
    if spec is None or spec.loader is None:
        raise ImportError("S37_M35_INSTALL_UNLOADABLE")
    m35_install = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m35_install)
    m35_install.install()

    _forget_candidate()
    _insert_front(S36_RETURN)
    candidate = importlib.import_module("candidate")
    if not Path(candidate.__file__).resolve().is_relative_to(S36_RETURN):
        raise ImportError("S37_S36_CANDIDATE_NOT_LOADED:" + str(candidate.__file__))
    importlib.import_module("candidate.actor_access_response")

    _insert_front(LANGUAGE_RETURN)
    language_session = importlib.import_module("language_mediation.session")
    language_session.bootstrap.install()

    for name in (
        "candidate",
        "candidate.pipeline",
        "candidate.actor_access_response",
        "bp2_joined",
        "firstclass",
        "joined.session",
        "joined.refusal",
        "language_mediation.session",
        "r31j.build",
        "bp4.product",
        "r31e.expression",
        "r30a.first_session",
        "c8_readonly_consumer",
    ):
        module = sys.modules.get(name)
        if module is not None:
            _ORIGINS[name] = str(Path(getattr(module, "__file__", "")).resolve())
    _INSTALLED = True


def origins() -> dict:
    install()
    return dict(_ORIGINS)


def roots() -> dict:
    install()
    return {
        "m35_return": str(M35_RETURN),
        "join_e_return": str(JOIN_E_RETURN),
        "language_return": str(LANGUAGE_RETURN),
        "s36_return": str(S36_RETURN),
        "cuts": dict(CUTS),
        "origins": origins(),
    }


__all__ = [
    "CUTS",
    "JOIN_E_RETURN",
    "LANGUAGE_RETURN",
    "M35_RETURN",
    "RETURN",
    "S36_RETURN",
    "install",
    "origins",
    "roots",
]
