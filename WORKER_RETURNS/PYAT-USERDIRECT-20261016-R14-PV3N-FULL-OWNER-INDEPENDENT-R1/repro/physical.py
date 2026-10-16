"""Independent instrumentation of original calls; no patched owner results."""
import bootstrap
from bootstrap import R,C,RT,blob,reattest
from pathlib import Path
from collections import Counter
import sys,json,os,hashlib
from copy import deepcopy
from dataclasses import replace
from fixture_owner import FixtureOwnerControl
from pv3_candidate import RequestAPI,reconcile_journal
import pv2_sourcefree_fixture as F
from rawlsing_next.pre553_batch_runner import UnitExecutionReceipt

NAMES={'validate_c11_source_release','ingest_c11_source_release','execute_empirical_query','execute_exact_bounded_discovery','run_integrated','execute_route_b_production','produce_exact_conditional_support_profile','replay_exact_conditional_support_profile'}
class Trace:
 def __init__(self):self.durable_callbacks=[];self.calls=[];self.c11=[];self.facts=[];self.consumers=[];self.discovery=[]
 def profile(self,frame,event,arg):
  name=frame.f_code.co_name
  if event=='call' and name=='execute' and frame.f_code.co_filename==F.__file__:
   self.durable_callbacks.append(dict(file=frame.f_code.co_filename,line=frame.f_code.co_firstlineno,unit_ref=frame.f_locals['unit'].unit_ref.as_dict()))
  if name not in NAMES:return
  if event=='call':self.calls.append(dict(function=name,file=frame.f_code.co_filename,line=frame.f_code.co_firstlineno))
  if event=='return' and arg is not None:
   if name=='validate_c11_source_release' and hasattr(arg,'release_ref'):
    c=frame.f_locals['candidate'];self.c11.append(dict(class_name=type(arg).__module__+'.'+type(arg).__name__,release_ref=arg.release_ref.as_dict(),source_artifact_ref=arg.source_artifact_ref.as_dict(),public=[x.semantic_projection() for x in (*c.empirical_universes,*c.respondent_events,*c.routing_eligibility_facts_or_exact_rules)],respondents=[x.semantic_projection() for x in c.respondent_identities]))
   if name=='execute_empirical_query' and hasattr(arg,'facts'):
    self.facts.extend(dict(ref=f.ref.as_dict(),projection=f.semantic_projection(),query=frame.f_locals['query'].semantic_projection(),query_ref=frame.f_locals['query'].ref.as_dict()) for f in arg.facts)
   if name=='execute_exact_bounded_discovery' and hasattr(arg,'receipts'):
    self.discovery.append(dict(facts=[f.ref.as_dict() for f in arg.empirical_facts],receipts=[r.semantic_projection() for r in arg.receipts],receipt_refs=[r.ref.as_dict() for r in arg.receipts]))
   if name=='produce_exact_conditional_support_profile' and hasattr(arg,'as_dict'):self.consumers.append(dict(class_name=type(arg).__module__+'.'+type(arg).__name__,ref=arg.ref.as_dict(),material=arg.as_dict()))
 def __enter__(self):sys.setprofile(self.profile);return self
 def __exit__(self,*args):sys.setprofile(None)
 def data(self):return dict(pid=os.getpid(),actual_durable_executor_callbacks=self.durable_callbacks,call_counts=dict(Counter(x['function'] for x in self.calls)),calls=self.calls,C11=self.c11,I03=self.facts,I05=self.discovery,Field_Forge=self.consumers,imports=imports())
def imports():
 rows=[]
 for name,m in sorted(sys.modules.items()):
  f=getattr(m,'__file__',None)
  if f and Path(f).is_file() and Path(f).suffix=='.py' and (str(RT) in f or str(C/'repro') in f):
   b=Path(f).read_bytes();rows.append(dict(module=name,file=str(Path(f).resolve().relative_to(R)),blob_sha1=blob(b),sha256=hashlib.sha256(b).hexdigest()))
 return rows

def args(fx):return dict(expected=fx['expected'],selected_scopes=fx['plans'],register=fx['register'],scope_metadata=tuple(fx['meta']))
def prepare(root,profile='BASELINE',policy=None,provision=False):
 owner=FixtureOwnerControl(profile,policy_path=policy,provision=provision);api=RequestAPI(owner.client(),owner._attest)
 installation=dict(pid=os.getpid(),before_source_fixture=True,expected_root=owner.installation.expected_root,register_root=owner.installation.register_root,complete_expected=json.loads(owner.installation.expected_json),profile=profile)
 if profile=='BASELINE':
  oracle=json.loads((R/'01_FROZEN_ORIGINAL_EIGHT_OPS_AND_TRUSTED_OWNER.json').read_text())
  assert {x['expected_work_key']:x for x in installation['complete_expected']['records']}=={x['complete_exact_fixture_identity']['expected_work_key']:x['complete_exact_fixture_identity'] for x in oracle['inventory']}
  fx=F.pv2_sourcefree_fixture(root)
 else:
  # Original independent fixture creates real altered physical cells before owner validation.
  import common
  row,value=(2,'1') if profile=='R2_Y1' else (1,'0')
  fx=common.make_numeric_fixture(root,row=row,new_value=value)
 assert fx['expected'].payload_json==owner.installation.expected_json
 return owner,api,fx,installation

def receipts(fx):
 out=[]
 for scope in fx['plans']:
  s=scope.p01_kwargs['session'];cp=s.store.load(identity=s.identity);proof=reconcile_journal(s);rows=[]
  for rec in cp.records:
   receipt=rec.rehydrate_verified();assert isinstance(receipt,UnitExecutionReceipt)
   rows.append(dict(actual_class=type(receipt).__module__+'.'+type(receipt).__name__,hash=rec.receipt_hash,projection=receipt.projection(),unit_key=rec.unit_key))
  assert len(rows)==3;out.append(dict(identity=s.identity.projection(),records=rows,reconciliation=proof))
 return out

def profile(m):return {str(x['condition_state']):dict(denominator=x['condition_denominator_support'],targets={str(t['target_state']):t['joint_support_count'] for t in x['target_counts']}) for x in m['conditional_count_profile']}
def write(p,value):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w') as f:json.dump(value,f,indent=2,default=list);f.write('\n');f.flush();os.fsync(f.fileno())
