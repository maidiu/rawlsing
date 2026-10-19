"""Path bootstrap for the P41 test suite (works under any cwd/rootdir)."""
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

import bootstrap  # noqa: E402

bootstrap.install()
