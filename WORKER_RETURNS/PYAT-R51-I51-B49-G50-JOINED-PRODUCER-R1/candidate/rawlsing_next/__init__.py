"""R51 shadow package: B49 candidate modules plus the accepted rawlsing_next tree."""
from pathlib import Path
_REPO = Path(__file__).resolve().parents[4]
__path__ = [str(Path(__file__).resolve().parent), str(_REPO / "rawlsing_next")]
