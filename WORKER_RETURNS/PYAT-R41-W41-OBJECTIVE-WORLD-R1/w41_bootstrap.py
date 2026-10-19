"""One isolated process, pinned native owners; no installed package changes."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
from reconstruct_owners import reconstruct
reconstruct()
for p in (ROOT/'owners/native', ROOT/'owners/wv1', ROOT/'owners/wv1/vendor', ROOT/'owners/native/rawlsing_next/tests', ROOT/'owners/f6p',ROOT/'owners/f6p/oracle',ROOT/'owners/f6p/tests',ROOT/'owners/ee1/runtime'):
    sys.path.insert(0,str(p))
import bootstrap
bootstrap.install()
# F6M/A/A0 are absent from the WV1 closure; use the exact separately pinned F6P namespace path.
import rawlsing_next
rawlsing_next.__path__.append(str(ROOT/'owners/f6p/native/rawlsing_next'))
