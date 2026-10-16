"""Read-only actual native entry/import observer, with sanitized path aliases."""
from pathlib import Path
import sys,hashlib,collections,json
from bootstrap import ROOT,RT
NAMES={'ingest_c11_source_release','execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context','read_historical_test_only','consume','evaluate','accept','serve'}
class Observer:
 def __init__(self):self.counts=collections.Counter();self.compositions=[];self.f8=[];self.held=[]
 def profile(self,frame,event,arg):
  n=frame.f_code.co_name;f=frame.f_code.co_filename
  if n not in NAMES or not f.startswith(str(RT)):return
  if event=='call':
   self.counts[(str(Path(f).relative_to(ROOT)),frame.f_code.co_firstlineno,n)]+=1
   if n=='evaluate_positioned_subject_possibility':
    es=frame.f_locals.get('evidence',())
    if isinstance(es,(tuple,list)):
     self.held.extend(es);self.f8.append(dict(ids=[id(e) for e in es],refs=[e.evidence_ref.as_dict() for e in es]))
  elif event=='return' and n=='compose_positioned_subject_possibility' and hasattr(arg,'possibility_slice_evidence_or_null'):
   e=arg.possibility_slice_evidence_or_null
   if e is not None:
    self.held.append(e);self.compositions.append(dict(id=id(e),ref=e.evidence_ref.as_dict()))
 def start(self):sys.setprofile(self.profile)
 def stop(self):sys.setprofile(None)
 def result(self):
  manifest=json.loads((ROOT/'source_manifest.json').read_text());bylocal={x['local']:x for x in manifest};modules=[]
  for name,m in sorted(sys.modules.items()):
   file=getattr(m,'__file__',None)
   if file and str(file).startswith(str(RT)) and str(file).endswith('.py'):
    p=Path(file);b=p.read_bytes();rel=str(p.relative_to(RT));entry=bylocal[rel]
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert blob==entry['git_blob']
    modules.append(dict(module=name,physical_module_file=str(p.relative_to(ROOT)),path_basis='RETURN_RELATIVE_ALIAS_OF_VERIFIED_MODULE___FILE__',source_commit=entry['commit'],source_path=entry['path'],git_blob=blob,sha256=hashlib.sha256(b).hexdigest(),actual_physical_path_verified=True))
  assert all(any(c['id'] in x['ids'] and c['ref'] in x['refs'] for x in self.f8) for c in self.compositions)
  return dict(imports=modules,actual_entries=[dict(file=f,line=l,function=n,count=c) for (f,l,n),c in sorted(self.counts.items())],same_concrete_C1_evidence_objects_into_F8=len(self.compositions),observer='sys.setprofile actual frames; no owner wrappers/doubles; absolute personal filesystem paths remain local')
