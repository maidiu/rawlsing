from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
RT=ROOT/'runtime'
sys.path[:0]=list(map(str,[ROOT,ROOT/'repro',RT/'owners',RT,RT/'rawlsing_next/tests',RT/'rawlsing_next']))
