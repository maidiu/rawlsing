"""Replay driver: print the progressive receipt content hash (cold process)."""
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

import bootstrap  # noqa: E402

bootstrap.install()
from p41_service import P41Service  # noqa: E402

print(P41Service().progressive()["content_hash"])
