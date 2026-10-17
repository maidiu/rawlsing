from pathlib import Path
import common as C

R = Path(__file__).resolve().parents[1]
C.R = R / "historical"
C.RT = R / "runtime_root"
