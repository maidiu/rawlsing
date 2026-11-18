#!/usr/bin/env python3
"""Independent one-f4 query on retained 10k estate, exact 68aa snapshot."""
from __future__ import annotations
import hashlib, json, sys, time
from pathlib import Path
OWNER=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/OWNER')
SNAP=OWNER/'WORKER_RETURNS/ANVIL_ENGINEERING_SCALE_G5_20261118/tmp/snapshot'
MP=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117')
EX=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118/EXECUTION')
sys.path[:0]=[str(SNAP),str(MP/'vendor'),str(MP)]
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from fixture_1006 import ShapeSpec, build_context
from query_1006 import build_query_bundle
from court_instrumentation import CourtInstrumentation
contract=json.loads((EX/'fixture_contract_10k.json').read_text())
shape=ShapeSpec('scale-10k',contract['respondents'],include_weights=True,tag=contract['tag'])
ctx=build_context(shape); bundle=build_query_bundle(ctx)
q,p=bundle.by_name('f4_three')
root=Path(contract['root']); grant={'ok':True}
adm=PreparedSavedC11Admission.open(root=root,exact_path=contract['exact_path'],independently_held_manifest_sha256=contract['manifest_sha256'],independently_held_i02=ExternalI02Roots(**contract['i02']),release_ref=exact_ref(contract['reconstructed_v1_release_ref']),runtime_catalog=bundle.catalog,current_authorizer=lambda _r:grant['ok'])
instr=CourtInstrumentation()
with instr.phase(forbid_c11_repository=True) as counters:
    t=time.monotonic()
    with adm.prepared_i03() as session:
        idx=time.monotonic()-t
        t2=time.monotonic(); res=session.execute_i03(query_ref=q.ref,predicate_ref=p.ref); wall=time.monotonic()-t2
        facts=list(res.facts)
assert len(facts)==1
f=facts[0]
def refs(name):
    return [exact_ref(r,name).key for r in getattr(f,name,())]
fields=f.semantic_fields
out={'schema':'ANVIL_SCALE_G5_ONE_F4@1','product_file':str(SNAP/'rawlsing_next/pre553_direct_estate_i03.py'),'product_sha256':hashlib.sha256((SNAP/'rawlsing_next/pre553_direct_estate_i03.py').read_bytes()).hexdigest(),'fixture_contract':str(EX/'fixture_contract_10k.json'),'estate_manifest_sha256':contract['manifest_sha256'],'query_ref':q.ref.key,'predicate_ref':p.ref.key,'index_seconds':idx,'operation_wall_seconds':wall,'fact_ref':f.ref.key,'typed_state':f.typed_state,'raw_denominator_support':f.raw_denominator_support,'weighted_denominator_support':getattr(f,'weighted_denominator_support',None),'risk_set_member_refs':refs('risk_set_member_refs'),'denominator_member_refs':refs('denominator_member_refs'),'replay_ref':exact_ref(f.replay_ref,'replay').key,'target_topology':fields.get('target_topology'),'semantic_projection':f.semantic_projection(),'counters':counters.material()}
OUT=OWNER/'WORKER_RETURNS/ANVIL_ENGINEERING_SCALE_G5_20261118/one-f4.json'
OUT.write_text(json.dumps(out,indent=2,default=str,sort_keys=True)+'\n')
print(json.dumps({'fact_ref':out['fact_ref'],'state':out['typed_state'],'raw_denominator_support':out['raw_denominator_support'],'risk_members':len(out['risk_set_member_refs']),'denom_members':len(out['denominator_member_refs']),'replay':out['replay_ref'],'counters':out['counters'],'index':idx,'wall':wall},indent=2,default=str))
raise SystemExit(0)
