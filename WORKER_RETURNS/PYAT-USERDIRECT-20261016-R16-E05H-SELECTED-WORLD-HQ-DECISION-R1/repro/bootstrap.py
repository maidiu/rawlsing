from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'inherited_e05a'
RT=A/'runtime'
sys.path[:0]=list(map(str,[RT,RT/'rawlsing_next/tests',RT/'rawlsing_next',A,A/'repro',ROOT]))
