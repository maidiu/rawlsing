"""Reviewer interface transport. No author common/adapters are imported."""
import copy, hashlib, importlib, json, os, pathlib, sys
from dataclasses import fields
R=pathlib.Path(__file__).resolve().parents[1]
C=R/'runtime_phase_b/candidate'
sys.path[:0]=[str(C/'repro'),str(C/'pinned')]
import wg0p4_workload as w
O=json.loads((R/'01_FROZEN_EXPECTATIONS_BEFORE_WG0P4.json').read_text())
OP='OP-WG0P-ORD-01-MARGINAL'
JOP='OP-WG0P4-JOINT-RT-GIVEN-WG0P4-JOINT-ORD'
SECOND=json.loads((R/'observations/phase_b/reviewer_second_frontier_register.json').read_text())
def dump(path,value):
 path=pathlib.Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(value,indent=2,sort_keys=True,default=str)+'\n')
def items():
 names={x.name for x in fields(w.NativeItem)}
 return [w.NativeItem(**{k:tuple(v) if k in ('options','missing_codes') else v for k,v in row.items() if k in names}) for row in O['original_items']]
def joint_items():
 return [w.NativeItem(item_id='WG0P4-JOINT-'+suffix,form_id=form,source_id='WG0P-SRC-A',wave='W1',unit='respondent',response_kind=kind,options=domain,missing_codes=missing,route_evidence=route,grant='GRANTED_FIXTURE',version='v1') for suffix,form,kind,domain,missing,route in [('ORD','Q-ORD-A','ORDINAL',('0','1','2','3','9'),('9','997','998'),None),('RT','Q-RT-C','ROUTED',('yes','no'),('9',),'TESTONLY_R1_R6_JOINT_ROUTING')]]
class AdmissionRefused(Exception):
 def __init__(self,value):self.value=value;super().__init__(value)
def builder(its=None,joint=False):
 b=w.WorkloadBuilder()
 for i in items() if its is None else its:
  outcome=b.add_item(i)
  if outcome=='CONFLICTING_NATIVE_ITEM_IDENTITY':raise AdmissionRefused(outcome)
  if outcome!='OK':raise RuntimeError('unexpected reviewer admission return '+str(outcome))
 if joint:b.add_joint_risk_authority(w.joint_risk_authority())
 return b
def plan(its=None,joint=False,releases=None,ops=None):
 its=joint_items() if joint and its is None else items() if its is None else its
 b=builder(its,joint);freeze=b.freeze()
 return w.build_executable_plan(b.enumerate() if ops is None else ops,w.build_all_releases() if releases is None else releases,freeze_hash=freeze,items_by_id={i.item_id:i for i in its})
def execute(p):
 runner,rs=w.run_plan(p,w.make_executor(p));return runner,rs,w.consumer_effects(p,rs)
def rows(ops):return sorted([w.receipt_row(x) for x in ops],key=lambda x:x['op_id'])
def stripped(e):return {k:[{f:x[f] for f in ('typed_state','denominator','cells')} for x in v] for k,v in e.items()}
def profile_calls(calls):
 def trace(frame,event,arg):
  if event=='call' and ('runtime_phase_b/candidate/' in frame.f_code.co_filename):
   name=frame.f_code.co_name
   if name in ('__init__','enumerate','build_executable_plan','make_executor','run_plan','run','execute_empirical_query','consumer_effects','execute_positive_conditional','build_positive_conditional_frontier'):
    calls.append({'name':name,'file':frame.f_code.co_filename,'line':frame.f_code.co_firstlineno})
 return trace

def verified_modules():
 cut=json.loads((R/'observations/phase_b/candidate_read_cut.json').read_text())
 # Verify pinned staging independently, not just the candidate's own import loop.
 entries=cut['source_rows']
 if not entries:raise RuntimeError('candidate read cut missing file inventory')
 for row in entries:
  path=R/row['staged_path'];data=path.read_bytes()
  if hashlib.sha256(data).hexdigest()!=row['sha256']:raise RuntimeError('changed staged source '+str(path))
 mods={}
 for name in ('pre553_c11_repository','pre553_c11_ingest','pre553_empirical_query','pre553_batch_runner','pre553_empirical_objects','pre553_c11_integrity'):
  module=importlib.import_module('rawlsing_next.'+name);path=pathlib.Path(module.__file__).resolve()
  if not path.is_relative_to(C/'pinned/rawlsing_next'):raise RuntimeError('wrong physical owner '+str(path))
  mods[name]={'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 return mods
