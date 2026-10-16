"""Read-only per-process import/callee telemetry, opt-in. No owner patching."""
import os
if os.environ.get('PV2I_AUDIT_DIR'):
 import sys,atexit,json,hashlib
 from pathlib import Path
 calls={}
 names={'validate_c11_source_release','ingest_c11_source_release','execute_empirical_query','execute_exact_bounded_discovery','run_integrated','produce_exact_conditional_support_profile','run_sourcefree_with_register'}
 def profile(frame,event,arg):
  if event=='call' and frame.f_code.co_name in names:
   k=frame.f_code.co_filename+':'+str(frame.f_code.co_firstlineno)+':'+frame.f_code.co_name;calls[k]=calls.get(k,0)+1
 sys.setprofile(profile)
 def save():
  files=[]
  for n,m in sorted(sys.modules.items()):
   p=getattr(m,'__file__',None)
   if p and 'runtime_root' in p and p.endswith('.py') and Path(p).is_file():
    data=Path(p).read_bytes();files.append({'module':n,'physical_file':p,'sha256':hashlib.sha256(data).hexdigest(),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()})
  d=Path(os.environ['PV2I_AUDIT_DIR']);d.mkdir(parents=True,exist_ok=True);(d/f'process_{os.getpid()}.json').write_text(json.dumps({'pid':os.getpid(),'argv':sys.argv,'calls':calls,'imports':files},indent=2)+'\n')
 atexit.register(save)
