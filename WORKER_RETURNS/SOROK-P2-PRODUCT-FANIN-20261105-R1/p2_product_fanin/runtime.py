"""Load the accepted base plus the three exact P2 additive returns."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True

RETURN = Path(__file__).resolve().parents[1]
WORKER_RETURNS = RETURN.parent
WORKSPACE = WORKER_RETURNS.parent
LIFECYCLE_RETURN = WORKER_RETURNS / "SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1"
INTERVAL_RETURN = WORKER_RETURNS / "SOROK-P2-EXPLICIT-INTERVAL-FLOW-20261105-R1"
LATER_RETURN = WORKER_RETURNS / "SOROK-P2-LATER-EVENT-CONTINUATION-20261105-R1"
PACKAGE_RETURN = WORKER_RETURNS / "SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1"
PACKAGE_PRODUCT = PACKAGE_RETURN / "product"
PROJECTION_RETURN = WORKER_RETURNS / "SOROK-S45-S47-PROJECTION-20261105-R1"
TMP = RETURN / "logs" / "tmp"

_LOADED = False
_DEPS: dict | None = None


def load() -> dict:
    global _LOADED, _DEPS
    if _LOADED and _DEPS is not None:
        return _DEPS
    TMP.mkdir(parents=True, exist_ok=True)
    os.environ["TMPDIR"] = str(TMP)
    for path in (
        LATER_RETURN,
        INTERVAL_RETURN,
        LIFECYCLE_RETURN,
        PROJECTION_RETURN,
        PACKAGE_PRODUCT,
    ):
        if not path.is_dir():
            raise RuntimeError("SOROK_P2_FANIN_SOURCE_MISSING:" + str(path))
        text = str(path)
        if text in sys.path:
            sys.path.remove(text)
        sys.path.insert(0, text)

    from p2_continuation.bootstrap import load as later_load

    deps = later_load()
    from p2_explicit_interval_flow.bootstrap import install as interval_install
    from p2_explicit_interval_flow.continuation import (
        ALLOWED_MODES,
        INTERVAL_INPUT_SCHEMA,
        apply_explicit_interval,
    )
    from p2_continuation.continuation import P2Continuation
    from sorok_p2_lifecycle.lifecycle import LifecycleEncounter, LifecycleRefusal

    interval_info = interval_install(WORKSPACE)
    deps.update({
        "WORKSPACE": WORKSPACE,
        "fanin_return": RETURN,
        "lifecycle_return": LIFECYCLE_RETURN,
        "interval_return": INTERVAL_RETURN,
        "later_return": LATER_RETURN,
        "interval_info": interval_info,
        "ALLOWED_MODES": ALLOWED_MODES,
        "INTERVAL_INPUT_SCHEMA": INTERVAL_INPUT_SCHEMA,
        "interval_apply": apply_explicit_interval,
        "P2Continuation": P2Continuation,
        "LifecycleEncounter": LifecycleEncounter,
        "LifecycleRefusal": LifecycleRefusal,
    })
    _LOADED = True
    _DEPS = deps
    return deps


__all__ = [
    "INTERVAL_RETURN",
    "LATER_RETURN",
    "LIFECYCLE_RETURN",
    "PACKAGE_PRODUCT",
    "PACKAGE_RETURN",
    "PROJECTION_RETURN",
    "RETURN",
    "TMP",
    "WORKER_RETURNS",
    "WORKSPACE",
    "load",
]
