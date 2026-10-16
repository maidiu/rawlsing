"""Explicit frozen-test import-path adapter; no changes to tests or owners."""
import pathlib,sys,os,json,importlib,runpy
R=pathlib.Path(__file__).resolve().parents[1];RT=R/'runtime_root';S=RT/'candidate/runtime_root/source'
variant=os.environ.get('E04S_VARIANT','repaired')
P=RT/'candidate' if variant=='original' else RT/'repaired' if variant=='e04r' else R
sys.path[:0]=list(map(str,[P,S,S/'rawlsing_next/tests',R/'repro']))
# Original author37 prepends its historic candidate to sys.path. Preimport
# EXACT selected six modules so that path change cannot replace the candidate.
for n in ['product','product.empirical','product.world','product.service','product.nonparent','product.scenario']:importlib.import_module(n)
from observer import Observer
obs=Observer();obs.start()
try:
 if sys.argv[1]=='--script':
  file=sys.argv[2];sys.argv=sys.argv[2:];runpy.run_path(file,run_name='__main__');code=0
 else:
  import pytest
  code=pytest.main(sys.argv[1:])
finally:
 obs.stop();path=pathlib.Path(os.environ['E04S_PROCESS_AUDIT']);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obs.material(),indent=2)+'\n')
sys.exit(code)
