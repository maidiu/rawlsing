"""Path setup for the R11 E05 return.

The sealed E04 candidate product package and the pinned native owners are
staged into PV2_RUNTIME_ROOT (git-ignored scratch), so the return's own
sourcefree adapter is the only code authored here.
"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETURN = HERE.parent
RUNTIME = os.environ.get('PV2_RUNTIME_ROOT', '')

for path in (Path(RUNTIME) if RUNTIME else None, RETURN / 'repro'):
    if path is not None and path.is_dir() and str(path) not in sys.path:
        sys.path.insert(0, str(path))
