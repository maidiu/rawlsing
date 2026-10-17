import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent            # .../PYAT-R27-GF1E-.../tests
RET = HERE.parent                                 # .../PYAT-R27-GF1E-...
WORKER_RETURNS = RET.parent                       # .../WORKER_RETURNS
GF1_COURT = WORKER_RETURNS / "PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1" / "court"
GF1_REPRO = GF1_COURT / "repro"
GF1_RT = GF1_COURT / "runtime_root"

for p in (str(RET / "repro"), str(GF1_REPRO), str(GF1_RT)):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

if not (GF1_RT / "gf1_pair_support_consumer.py").is_file():
    raise RuntimeError("gf1_pair_support_consumer.py not found under GF1 court runtime_root")
