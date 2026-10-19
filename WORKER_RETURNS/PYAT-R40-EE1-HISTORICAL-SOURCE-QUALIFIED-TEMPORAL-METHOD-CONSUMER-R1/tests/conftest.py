"""Path bootstrap for the EE1 test suite (runs under any cwd/rootdir)."""
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

import ee1_paths  # noqa: E402

ee1_paths.install()
