#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
from scientific_native_input import build_all  # noqa: E402

def main(argv=None):
 p=argparse.ArgumentParser(); p.add_argument('--source-id',required=True); a=p.parse_args(argv)
 r=build_all()['records']
 if a.source_id not in r: raise SystemExit('unknown source')
 print(json.dumps(r[a.source_id],indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
