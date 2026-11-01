"""Install the first-class BP2 source package over the warm JOIN-E closure.

The JOIN-E consumer and its C12/E code are reused unchanged. Only the BP2
occurrence producer is shadowed by this return's validated source intake, and
the two module-level builder names used by the existing JOIN-E sessions are
pointed at ``firstclass``. The closure audit is extended to recognize the
candidate BP2 root instead of pretending it is the old J vendor.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE_BP2 = (HERE / "candidate" / "vendor" / "bp2").resolve()
JOIN_E = Path(os.environ.get(
    "M35_JOIN_E_RETURN",
    "/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/"
    "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1",
)).resolve()
J = JOIN_E / "vendor" / "j"
E = JOIN_E / "vendor" / "e"
J_PATHS = (
    J,
    J / "r29m" / "source",
    J / "candidate",
    J / "candidate" / "vendor" / "bp2",
    J / "candidate" / "vendor" / "bp4",
    J / "r29p",
    J / "r26e",
    J / "n1",
)
CONFLICT_PREFIXES = (
    "bp1", "bp2p4", "bp2_joined", "bp4", "candidate", "c8_exclusive_writer",
    "c8_readonly_consumer", "c8o_trusted_outbox", "c9_event_ingress",
    "historical_actor_producer", "lab_sgi1", "outbox_prototype", "r26e",
    "r29p", "r30a", "r31e", "r31j",
)
_INSTALLED = False


def _forget_conflicts() -> None:
    for name in list(sys.modules):
        if any(name == prefix or name.startswith(prefix + ".")
               for prefix in CONFLICT_PREFIXES):
            sys.modules.pop(name, None)


def install() -> None:
    """Install the candidate BP2 closure once, before JOIN-E imports it."""
    global _INSTALLED
    if _INSTALLED:
        return
    for path in (E, JOIN_E, *reversed(J_PATHS), CANDIDATE_BP2):
        text = str(path)
        if text in sys.path:
            sys.path.remove(text)
    _forget_conflicts()
    sys.path.insert(0, str(E))
    for path in reversed(J_PATHS):
        sys.path.insert(0, str(path))
    sys.path.insert(0, str(JOIN_E))
    sys.path.insert(0, str(CANDIDATE_BP2))

    import joined.imports as imports
    imports._INSTALLED = True

    import bp2_joined
    if not Path(bp2_joined.__file__).resolve().is_relative_to(CANDIDATE_BP2):
        raise ImportError("M35_FIRSTCLASS_BP2_NOT_LOADED: " + str(bp2_joined.__file__))

    import joined.closure as closure
    closure.ROOT_BY_CLASS["CANDIDATE"] = CANDIDATE_BP2
    for name in list(closure.EXPECTED):
        if name == "bp2_joined" or name.startswith("bp2_joined."):
            closure.EXPECTED[name] = "CANDIDATE"

    import joined.session as session
    import joined.refusal as refusal
    import firstclass

    session.build_product = firstclass.build_product
    session.c9_only = firstclass.c9_only
    refusal.c9_only = firstclass.c9_only
    _INSTALLED = True


__all__ = ["CANDIDATE_BP2", "JOIN_E", "install"]
