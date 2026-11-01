"""One-time import-closure installation for the J-first/E-second join.

The two vendored returns contain same-named packages. This module is imported
before any J/E package and deliberately clears any closure that was loaded by
an earlier E-first import, then installs the J closure and finally the E path.
It is idempotent so the first coherent installation is preserved.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
J = ROOT / 'vendor' / 'j'
E = ROOT / 'vendor' / 'e'
J_PATHS = (J, J/'r29m/source', J/'candidate', J/'candidate/vendor/bp2',
           J/'candidate/vendor/bp4', J/'r29p', J/'r26e', J/'n1')
CONFLICT_PREFIXES = (
    'bp1', 'bp2p4', 'bp2_joined', 'bp4', 'candidate', 'c8_exclusive_writer',
    'c8_readonly_consumer', 'c8o_trusted_outbox', 'c9_event_ingress',
    'historical_actor_producer', 'lab_sgi1', 'outbox_prototype', 'r26e',
    'r29p', 'r30a', 'r31e', 'r31j',
)
_INSTALLED = False


def _is_under(path, root: Path) -> bool:
    try:
        return Path(path).resolve().is_relative_to(root)
    except (OSError, ValueError):
        return False


def install() -> None:
    """Install the explicit J-first/E-second closure once."""
    global _INSTALLED
    if _INSTALLED:
        return
    e_root = E.resolve()
    sys.path[:] = [p for p in sys.path if not _is_under(p, e_root)]
    for name in list(sys.modules):
        if any(name == prefix or name.startswith(prefix + '.')
               for prefix in CONFLICT_PREFIXES):
            sys.modules.pop(name, None)
    for path in reversed(J_PATHS):
        sys.path.insert(0, str(path))
    import r31j.build  # noqa: F401  # loads the authoritative J closure
    sys.path.insert(0, str(E))
    _INSTALLED = True
