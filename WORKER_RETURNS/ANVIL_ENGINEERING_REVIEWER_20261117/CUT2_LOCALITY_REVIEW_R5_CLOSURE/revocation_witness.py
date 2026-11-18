"""Independent closure witness: R4 RED vs R5 corrected adapter, sealed estate."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117')
R2 = ROOT/'R2_PILOT/fixture_contract_pilot.json'
R4 = ROOT/'R4_LOCALITY_EXPERIMENT/locality_adapter.py'
R5 = ROOT/'R5_LOCALITY_REVOCATION_REPAIR/locality_adapter.py'
sys.path.insert(0, str(ROOT.parents[1]))
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def estate(e,grant):
 return VerifiedDirectEstate(e['root'], exact_path=e['exact_path'], independently_held_manifest_sha256=e['manifest_sha256'], independently_held_i02=ExternalI02Roots(**e['i02']), current_authorizer=lambda _r: grant['ok'])
def adapter_case(mod,e,grant):
 original=mod.install()
 try:
  with DirectEstateI03Session(estate(e,grant)) as s:
   respondent=next(iter(s.respondents)); gen=s._respondent_family('RoutingEligibilityFact',respondent); first=next(gen); first_ref=first.ref.key; grant['ok']=False
   try:
    second=next(gen); second_ref=second.ref.key; error=None
   except Exception as exc:
    second_ref=None; error=f'{type(exc).__name__}: {exc}'
 finally:
  mod.restore(original)
 return {'first_ref':first_ref,'second_ref':second_ref,'error':error,'bypassed':error is None and second_ref is not None,'restored':DirectEstateI03Session._respondent_family is original}
def original_case(e,grant):
 with DirectEstateI03Session(estate(e,grant)) as s:
  respondent=next(iter(s.respondents)); gen=s._respondent_family('RoutingEligibilityFact',respondent); first=next(gen); first_ref=first.ref.key; grant['ok']=False
  try:
   second=next(gen); second_ref=second.ref.key; error=None
  except Exception as exc:
   second_ref=None; error=f'{type(exc).__name__}: {exc}'
 return {'first_ref':first_ref,'second_ref':second_ref,'error':error,'refused':error is not None}
def valid_order(mod,e,grant):
 grant['ok']=True
 with DirectEstateI03Session(estate(e,grant)) as s:
  respondent=next(iter(s.respondents)); original=[o.ref.key for o in s._respondent_family('RoutingEligibilityFact',respondent)]
 original_fn=mod.install()
 try:
  with DirectEstateI03Session(estate(e,grant)) as s:
   respondent=next(iter(s.respondents)); corrected=[o.ref.key for o in s._respondent_family('RoutingEligibilityFact',respondent)]
 finally:
  mod.restore(original_fn)
 return {'count':len(corrected),'canonical_sorted':corrected==sorted(corrected),'matches_original_order':corrected==original,'first_ref':corrected[0] if corrected else None,'last_ref':corrected[-1] if corrected else None,'restored':DirectEstateI03Session._respondent_family is original_fn}
def main(argv):
 proof=Path(argv[1]).resolve(); contract=json.loads(R2.read_text()); e=contract['estate']; grant={'ok':True}
 r4=load('r4_adapter',R4); r5=load('r5_adapter',R5)
 grant['ok']=True; red=adapter_case(r4,e,grant)
 grant['ok']=True; green=adapter_case(r5,e,grant)
 grant['ok']=True; original=original_case(e,grant)
 grant['ok']=True; order=valid_order(r5,e,grant)
 out={'schema':'ANVIL_CUT2_R5_CLOSURE_WITNESS@1','sealed_estate_manifest':e['manifest_sha256'],'family':'RoutingEligibilityFact','r4_red':red,'r5_green':green,'original_control':original,'valid_iteration_order':order,'red_expected':red['bypassed'] is True,'green_expected':green['bypassed'] is False and 'current source/operation authority refused' in (green['error'] or ''),'original_expected':original['refused'] is True,'order_expected':order['canonical_sorted'] and order['matches_original_order'] and order['count']>0,'all_expected':False}
 out['all_expected']=all((out['red_expected'],out['green_expected'],out['original_expected'],out['order_expected'],red['restored'],green['restored'],order['restored']))
 (proof/'r5_closure_witness.json').write_text(json.dumps(out,indent=2,sort_keys=True),encoding='utf-8'); print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out['all_expected'] else 2
if __name__=='__main__': raise SystemExit(main(__import__('sys').argv))
