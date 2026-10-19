"""P41 bootstrap: staged accepted E04L apparatus + injected E03 candidate.

Loads the exact staged E04L files (blob-pinned in runtime/PROVENANCE.json) and
registers the staged `pre553_n9_n10w_progressive_candidate` module under
`rawlsing_next.pre553_n9_n10w_progressive_candidate` exactly as the accepted
E04L bootstrap did.  No production install, no source read.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent
PACKET = RUNTIME.parent
REPO = PACKET.parents[1]

_INSTALLED = False


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    for path in (str(RUNTIME), str(RUNTIME / "vendor"), str(REPO)):
        if path not in sys.path:
            sys.path.insert(0, path)
    import rawlsing_next
    _STAGED_MODULES = (
        ("rawlsing_next.pre553_n9_n10w_progressive_candidate",
         RUNTIME / "vendor/aux/pre553_n9_n10w_progressive_candidate.py"),
        ("rawlsing_next.pre553_learned_product_lifecycle",
         RUNTIME / "staged_native/pre553_learned_product_lifecycle.py"),
    )
    for name, path in _STAGED_MODULES:
        if name in sys.modules:
            continue
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        setattr(rawlsing_next, name.rsplit(".", 1)[-1], module)
    _INSTALLED = True
