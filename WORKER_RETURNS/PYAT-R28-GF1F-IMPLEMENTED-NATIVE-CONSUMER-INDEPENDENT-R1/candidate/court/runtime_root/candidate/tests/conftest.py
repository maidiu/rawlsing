"""Shared path setup for the PV2 return.

The pinned accepted owners and the V2-chain candidates are staged from the
pinned runtime commit into PV2_RUNTIME_ROOT; the return's own sourcefree code
lives under repro/.
"""
import os
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
REPRO = RETURN / 'repro'
RUNTIME = os.environ.get('PV2_RUNTIME_ROOT')

for path in (REPRO, RUNTIME, Path(__file__).resolve().parent):
    if path is not None and str(path) not in sys.path:
        sys.path.insert(0, str(path))
