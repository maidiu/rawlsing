"""Read-only actual frame/import observer; never replaces any owner callable."""
import sys,pathlib,json,hashlib,collections,os
NAMES={'ingest_c11_source_release','validate_c11_source_release','execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context'}
class Observer:
 def __init__(self,detailed=False):
  self.detailed=detailed;self.counts=collections.Counter();self.calls=[];self.compositions=[];self.f8=[];self.facts=[];self.ingests=[];self.held=[]
 def profile(self,frame,event,arg):
  name=frame.f_code.co_name;file=frame.f_code.co_filename
  if name not in NAMES or 'runtime_root' not in file:return
  if event=='call':
   self.counts[(file,frame.f_code.co_firstlineno,name)]+=1
   if self.detailed:self.calls.append(dict(function=name,file=file,line=frame.f_code.co_firstlineno))
   if self.detailed and name=='evaluate_positioned_subject_possibility':
    values=frame.f_locals.get('evidence',())
    if isinstance(values,(tuple,list)):
     self.held.extend(values);self.f8.append(dict(ids=[id(v) for v in values],refs=[v.evidence_ref.as_dict() for v in values],query_ref=frame.f_locals['query'].ref.as_dict()))
  elif event=='return' and arg is not None and self.detailed:
   if name=='compose_positioned_subject_possibility' and hasattr(arg,'possibility_slice_evidence_or_null'):
    e=arg.possibility_slice_evidence_or_null
    if e is not None:
     self.held.append(e);self.compositions.append(dict(id=id(e),evidence_ref=e.evidence_ref.as_dict(),fact_ref=arg.producer_fact_ref.as_dict(),query_ref=frame.f_locals['empirical_query'].ref.as_dict()))
   elif name=='execute_empirical_query' and hasattr(arg,'facts'):
    self.held.extend(arg.facts);self.facts.extend(dict(ref=f.ref.as_dict(),projection=f.semantic_projection()) for f in arg.facts)
   elif name=='ingest_c11_source_release' and hasattr(arg,'accepted'):
    c=frame.f_locals['candidate'];self.ingests.append(dict(accepted=arg.accepted,ref=arg.release_ref.as_dict() if arg.release_ref else None,source_events=[e.semantic_projection() for e in c.respondent_events]))
 def start(self):sys.setprofile(self.profile)
 def stop(self):sys.setprofile(None)
 def material(self):
  imports=[]
  for name,m in sorted(sys.modules.items()):
   f=getattr(m,'__file__',None)
   if f and 'runtime_root' in f and f.endswith('.py') and pathlib.Path(f).is_file():
    b=pathlib.Path(f).read_bytes();imports.append(dict(module=name,file=f,git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha256=hashlib.sha256(b).hexdigest()))
  return dict(pid=os.getpid(),imports=imports,counts=[dict(file=f,line=l,function=n,count=c) for (f,l,n),c in sorted(self.counts.items())],calls=self.calls,compositions=self.compositions,F8_actual_inputs=self.f8,I03_facts=self.facts,C11_ingests=self.ingests,method='sys.setprofile actual call/return frames; original owner functions unmodified')
