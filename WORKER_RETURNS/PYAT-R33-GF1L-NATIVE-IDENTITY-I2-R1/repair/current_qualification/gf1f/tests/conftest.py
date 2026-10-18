"""Seat current tests on the exact retained native GF1F source tree."""
import os
import sys
from pathlib import Path
FROZEN = Path(os.environ['GF1_CURRENT_FROZEN_GF1F']).resolve()
for path in (FROZEN/'repro',FROZEN/'candidate/court/repro',FROZEN/'candidate/court/runtime_root'):
    assert path.is_dir(),path
    sys.path.insert(0,str(path))
