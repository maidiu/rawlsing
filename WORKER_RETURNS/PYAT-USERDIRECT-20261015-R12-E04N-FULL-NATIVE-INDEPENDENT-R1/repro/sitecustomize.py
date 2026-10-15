"""Opt-in read-only child import/callee observer. No semantic substitution."""
import os
if os.environ.get('E04N_AUDIT_DIR'):
 import sys,atexit,json,hashlib
 from pathlib import Path
 counts={};names={'ingest_c11_source_release','validate_c11_source_release','execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context'}
 def profile(frame,event,arg):
  if event=='call' and frame.f_code.co_name in names:
   k=frame.f_code.co_filename+':'+str(frame.f_code.co_firstlineno)+':'+frame.f_code.co_name;counts[k]=counts.get(k,0)+1
 sys.setprofile(profile)
 def save():
  imports=[]
  for n,m in sorted(sys.modules.items()):
   p=getattr(m,'__file__',None)
   if p and 'runtime_root' in p and p.endswith('.py') and Path(p).is_file():
    data=Path(p).read_bytes();imports.append({'module':n,'file':p,'git_blob_sha1':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),'sha256':hashlib.sha256(data).hexdigest()})
  d=Path(os.environ['E04N_AUDIT_DIR']);d.mkdir(parents=True,exist_ok=True);(d/f'process_{os.getpid()}.json').write_text(json.dumps({'pid':os.getpid(),'argv':sys.argv,'calls':counts,'imports':imports},indent=2)+'\n')
 atexit.register(save)
