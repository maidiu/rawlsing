"""Execute the author controls and retain actual import and guard receipts."""
from pathlib import Path
import sys,time,json,hashlib,pytest
RET=Path(__file__).resolve().parents[1];tag=sys.argv[1]
sys.path[:0]=[str(RET),str(RET/'runtime_root/original')]
from rawlsing_next import v3_psepf_zero_positive_guard as g
before=Path(g.__file__).read_bytes();assert not g.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
out=RET/'evidence'/('repair_'+tag);out.mkdir(exist_ok=False)
start=time.time();code=pytest.main(['-q','--tb=short','--rootdir='+str(RET),'--confcutdir='+str(RET),str(RET/'repro/test_repair.py'),'--junitxml='+str(out/'junit.xml')])
assert Path(g.__file__).read_bytes()==before and not g.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
imports=[]
for name,mod in sorted(sys.modules.items()):
 f=getattr(mod,'__file__',None)
 if name.startswith(('candidate','rawlsing_next')) and f and Path(f).suffix=='.py':
  p=Path(f).resolve();b=p.read_bytes();imports.append(dict(module=name,file=str(p.relative_to(RET)),sha256=hashlib.sha256(b).hexdigest(),blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
(out/'execution.json').write_text(json.dumps(dict(command=['python3','repro/run_repair.py',tag],exit_code=int(code),seconds=time.time()-start,imports=imports,guard_blob='e0528d65215cb431196570c38bac4eae94217a1b',guard_empty_unchanged=True),indent=2)+'\n');raise SystemExit(code)
