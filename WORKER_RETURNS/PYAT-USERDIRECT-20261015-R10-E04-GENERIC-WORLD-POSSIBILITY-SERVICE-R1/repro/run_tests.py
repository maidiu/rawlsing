"""Actual pytest, source import hashes and portable execution receipts."""
from pathlib import Path
import sys,json,hashlib,time,os
RET=Path(__file__).resolve().parents[1];SOURCE=RET/'runtime_root/source'
sys.path[:0]=[str(RET),str(SOURCE),str(SOURCE/'rawlsing_next/tests')]
os.environ['PYTHONPATH']=str(SOURCE)+os.pathsep+str(SOURCE/'rawlsing_next/tests')
label=sys.argv[1];tag=sys.argv[2];out=RET/'outputs'/('tests_'+label+'_'+tag);out.mkdir(parents=True,exist_ok=False)
TESTS=['test_pre553_analytical_composition','test_pre553_analytical_composition_higher_order','test_pre553_empirical_possibility_provider','test_pre553_empirical_query','test_source_backed_positioned_subject_possibility','test_m4_v557_v558_publication_repository','test_m5_runtime_rsc_peer_prior','test_pre553_n9_n10w_progressive_candidate']
paths=[RET/'repro/test_product.py'] if label=='product' else [SOURCE/'rawlsing_next/tests'/(n+'.py') for n in TESTS]+[SOURCE/'tests/test_hq297_n9c_two_field_reader.py']
import pytest
start=time.time();args=['-q','--tb=short','--rootdir='+str(RET),'--confcutdir='+str(RET),*map(str,paths),'--junitxml='+str(out/'junit.xml')];code=pytest.main(args)
imports=[]
for name,mod in sorted(sys.modules.items()):
 f=getattr(mod,'__file__',None)
 if name.startswith(('rawlsing_next','product')) and f and Path(f).suffix=='.py':
  file=Path(f).resolve();b=file.read_bytes();imports.append(dict(module=name,file=str(file.relative_to(RET)),blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha256=hashlib.sha256(b).hexdigest()))
(out/'execution.json').write_text(json.dumps(dict(command=['python3','repro/run_tests.py',label,tag],pytest_args=[str(x).replace(str(RET),'RETURN_ROOT') for x in args],exit_code=int(code),seconds=time.time()-start,imports=imports),indent=2)+'\n');raise SystemExit(code)
