import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

import install

install.install()
