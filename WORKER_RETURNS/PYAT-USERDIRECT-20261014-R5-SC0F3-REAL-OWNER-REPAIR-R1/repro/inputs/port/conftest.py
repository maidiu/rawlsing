"""Namespace staging shim for the HQ298 SC0 sourcefree port court.

Appends the exact blob-verified staged modules (staging/ns) to the live
``rawlsing_next`` / ``rawlsing_next.tests`` namespace paths so that the pinned
N10E/C1/PE owners and their fixtures import as ``rawlsing_next.*`` WITHOUT any
owner file mutation.  Verified preimages: staging/staging_manifest.json.
"""
from __future__ import annotations

import sys
from pathlib import Path

_RETURN = Path(__file__).resolve().parent
_NS = _RETURN / "staging" / "ns"
_REPO_ROOT = _RETURN.parents[1]

# ensure the repository root is importable (live rawlsing_next namespace)
for _p in (
    str(_REPO_ROOT),
    str(_NS),
    str(_RETURN),
    str(_NS / "rawlsing_next" / "tests"),  # top-level test-helper imports
    str(_REPO_ROOT / "rawlsing_next" / "tests"),
):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# rawlsing_next is a namespace package (no __init__.py); adding staging/ns to
# sys.path extends the namespace with the blob-verified staged owners without
# shadowing any live module (staged set is disjoint from the live tree).
import rawlsing_next  # noqa: E402,F401
import rawlsing_next.tests  # noqa: E402,F401
