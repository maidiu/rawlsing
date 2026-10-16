from pathlib import Path
import sys,runpy
R=Path(__file__).resolve().parents[1]
import common as C
from pv2i_adapter import adapt_common
adapt_common(C,R)
exec(compile((R/'frozen_pv2i/repro/probe.py').read_text().replace('probe_ledger_v3','pv3_published_probe_final'),str(R/'frozen_pv2i/repro/probe.py'),'exec'))
