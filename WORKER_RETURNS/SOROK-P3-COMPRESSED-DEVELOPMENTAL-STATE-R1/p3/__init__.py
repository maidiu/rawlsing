"""Sourcefree P3 additions over the received, unchanged recursion ABI."""
from pathlib import Path
import sys

_engine = Path(__file__).resolve().parents[2] / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
if str(_engine) not in sys.path:
    sys.path.insert(0, str(_engine))
