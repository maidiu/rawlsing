"""Read-only callee/identity probe, no owner wrappers or estimator doubles."""
from bootstrap import ROOT,RT
from pathlib import Path
from collections import Counter
import sys,json,hashlib,os
NAMES={'ingest_c11_source_release','execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context','_authorize_cached_use','_require_exact_i03_authority_fitness','require_positive_authority','consume','evaluate','serve','accept'}
class Observer:
 def __init__(self):self.counts=Counter();self.ingests=[];self.compositions=[];self.f8=[];self.facts=[];self.held=[];self.client_snapshots=[]
 def profile(self,f,event,arg):
  n=f.f_code.co_name;path=f.f_code.co_filename
  if not path.startswith(str(RT)) or n not in NAMES:return
  if event=='call':
   self.counts[(str(Path(path).relative_to(ROOT)),f.f_code.co_firstlineno,n)]+=1
   if n=='evaluate_positioned_subject_possibility':
    es=f.f_locals.get('evidence',());self.held.extend(es);self.f8.append(dict(ids=[id(e) for e in es],refs=[e.evidence_ref.as_dict() for e in es]))
   if n in ('consume','evaluate') and 'snapshot' in f.f_locals:
    x=f.f_locals['snapshot'];self.held.append(x);self.client_snapshots.append(dict(consumer=n,snapshot_object_id=id(x),snapshot_hash=x.snapshot_hash))
  elif event=='return' and arg is not None:
   if n=='compose_positioned_subject_possibility' and hasattr(arg,'possibility_slice_evidence_or_null'):
    e=arg.possibility_slice_evidence_or_null
    if e is not None:self.held.append(e);self.compositions.append(dict(id=id(e),evidence_ref=e.evidence_ref.as_dict(),fact_ref=arg.producer_fact_ref.as_dict(),query_ref=f.f_locals['empirical_query'].ref.as_dict()))
   elif n=='execute_empirical_query' and hasattr(arg,'facts'):
    self.held.extend(arg.facts);self.facts.extend(dict(ref=x.ref.as_dict(),projection=x.semantic_projection()) for x in arg.facts)
   elif n=='ingest_c11_source_release' and hasattr(arg,'accepted'):
    c=f.f_locals['candidate'];self.ingests.append(dict(accepted=arg.accepted,release_ref=arg.release_ref.as_dict() if arg.release_ref else None,events=[e.semantic_projection() for e in c.respondent_events]))
 def start(self):sys.setprofile(self.profile)
 def stop(self):sys.setprofile(None)
 def result(self):
  manifest={x['local']:x for x in json.loads((ROOT/'source_manifest.json').read_text())};imports=[]
  for name,m in sorted(sys.modules.items()):
   p=getattr(m,'__file__',None)
   if p and p.startswith(str(RT)) and p.endswith('.py'):
    p=Path(p);b=p.read_bytes();local=str(p.relative_to(ROOT));x=manifest[local];assert hashlib.sha256(b).hexdigest()==x['sha256'];imports.append(dict(module=name,physical_file=local,commit=x['commit'],source_path=x['path'],git_blob=x['git_blob'],sha256=x['sha256'],verified=True))
  assert all(any(c['id'] in f['ids'] and c['evidence_ref'] in f['refs'] for f in self.f8) for c in self.compositions)
  return dict(pid=os.getpid(),imports=imports,actual_frames=[dict(file=p,line=l,function=n,count=c) for (p,l,n),c in sorted(self.counts.items())],C11_ingests=self.ingests,I03_facts=self.facts,compositions=self.compositions,F8_inputs=self.f8,client_snapshots=self.client_snapshots,same_concrete_C1_evidence_into_F8=len(self.compositions),observer='sys.setprofile; actual original callees; no callable replacement')
