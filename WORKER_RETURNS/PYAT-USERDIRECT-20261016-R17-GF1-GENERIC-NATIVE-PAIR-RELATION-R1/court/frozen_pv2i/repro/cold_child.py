"""Instrument unmodified candidate cold script in a genuinely fresh process."""
from pathlib import Path
import sys,runpy,os,json,hashlib,atexit
R=Path(__file__).resolve().parents[1];RT=R/'runtime_root';root=Path(sys.argv[1]);mode=sys.argv[2];tag=sys.argv[3];calls=[];names={'validate_c11_source_release','ingest_c11_source_release','execute_empirical_query','execute_exact_bounded_discovery','produce_exact_conditional_support_profile','replay_exact_conditional_support_profile','run_integrated','execute_route_b_production'}
if mode=='current_read':
 import pv2_original_scope_register as V
 from dataclasses import replace
 report=json.loads((root/'observations/first.json').read_text());reg=V.author_sourcefree_original_scope_register();reg=replace(reg,fixture_use_grant=replace(reg.fixture_use_grant,issuer='PV2I-SELF-ISSUED-COLD',grant='FAKE_SIGNED_ORIGINAL_SOURCE',ceiling=('PRODUCTION',)))
 result=V.read_current_consumer_material(reg,report);(R/f'observations/{tag}.json').write_text(json.dumps({'pid':os.getpid(),'grant':reg.binding()['fixture_use_grant'],'committed_root':reg.committed_root,'servable':result['servable'],'links':len(result.get('links',[]))},indent=2)+'\n');sys.exit(0)
if mode=='missing_source':
 import rawlsing_next.tests.test_pre553_route_b_production as T
 def missing(*a,**k):raise FileNotFoundError('PV2I_INDEPENDENT_SOURCE_MISSING')
 T._fixture=missing;mode='replay'
if mode=='changed_edition':
 import rawlsing_next.tests.test_pre553_route_b_production as T
 from dataclasses import replace
 old=T._fixture
 def edition(*a,**k):
  fx=old(*a,**k);h=hashlib.sha256(b'PV2I-NEW-SOURCE-EDITION').hexdigest();fx['stream']=replace(fx['stream'],source_sha256=h);p=fx['projection'];fx['projection']=replace(p,expected_source_sha256=h,source_snapshot_retention_ref=replace(p.source_snapshot_retention_ref,content_hash=h));return fx
 T._fixture=edition;mode='replay'
def trace(frame,event,arg):
 if event=='call' and frame.f_code.co_name in names:
  calls.append({'function':frame.f_code.co_name,'physical_file':frame.f_code.co_filename,'expected_file_exists':(root/'observations/expected_before_production.json').exists()})
 return trace
def finish():
 imports=[]
 for n,m in sorted(sys.modules.items()):
  f=getattr(m,'__file__',None)
  if f and Path(f).is_file() and str(RT) in f and f.endswith('.py'):
   d=Path(f).read_bytes();imports.append({'module':n,'file':f,'git_blob_sha1':hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()})
 (R/f'observations/{tag}.audit.json').write_text(json.dumps({'pid':os.getpid(),'calls':calls,'imports':imports},indent=2)+'\n')
atexit.register(finish);sys.settrace(trace)
script=RT/'candidate/repro/pv2_cold_process.py';sys.argv=[str(script),str(RT/'candidate'),str(root),mode];runpy.run_path(str(script),run_name='__main__')
