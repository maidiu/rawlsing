"""BP2P4J — one joined BP2 -> BP4 source-free person/product chain.

The package installs the exact staged upstream closures and verifies every
loaded module against pinned bytes. It adds no shadow C8/C9/C10 engine: the
joined producer calls BP2's actual ``JoinedProducer`` and the product calls
BP4's actual ``C10``/``C12``/``A0-A3`` implementation.

TEST_ONLY only. No native CAN/ADP/Pyat/C11/C12 authority is issued here.
"""
from __future__ import annotations

from . import bootstrap  # noqa: F401  (path setup)
from .bootstrap import (  # noqa: F401
    BP2_DIR,
    BP4_DIR,
    REPO,
    RETURN,
    VENDOR,
    SourceClosureDrift,
    install,
    verify_loaded_modules,
    verify_sources,
)

__all__ = [
    "BP2_DIR",
    "BP4_DIR",
    "REPO",
    "RETURN",
    "SourceClosureDrift",
    "VENDOR",
    "install",
    "verify_loaded_modules",
    "verify_sources",
]
