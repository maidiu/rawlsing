import sys
from pathlib import Path
_repro = Path(__file__).parent / "repro"
if str(_repro) not in sys.path:
    sys.path.insert(0, str(_repro))
_repo = Path(__file__).parent.parent.parent
if str(_repo) not in sys.path:
    sys.path.insert(0, str(_repo))
