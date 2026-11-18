#!/usr/bin/env python3
"""One fresh prepared f4 operation on the 128R/600Q width estate."""
from __future__ import annotations
import gzip,hashlib,json,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2];MP=REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'
def main():
 contract=json.loads((HERE/'fixture_contract_width128.json').read_text());snap=Path((HERE/'SNAPSHOT_PATH.txt').read_text().strip());sys.path[:0]=[str(snap),str(MP),str(MP/'vendor')]
 from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
 from rawlsing_next.pre553_empirical_objects import exact_ref,canonical_json
 from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
 from fixture_1006 import ShapeSpec,build_context
 from query_1006 import build_query_bundle
 from court_instrumentation import CourtInstrumentation
 shape=ShapeSpec('width128',contract['respondents'],include_weights=True,tag=contract['tag']);ctx=build_context(shape);bundle=build_query_bundle(ctx);q,p=bundle.by_name('f4_three')
 adm=PreparedSavedC11Admission.open(root=Path(contract['root']),exact_path=contract['exact_path'],independently_held_manifest_sha256=contract['manifest_sha256'],independently_held_i02=ExternalI02Roots(**contract['i02']),release_ref=exact_ref(contract['reconstructed_v1_release_ref']),runtime_catalog=bundle.catalog,current_authorizer=lambda _r:True)
 t=time.monotonic(); instr=CourtInstrumentation()
 with adm.prepared_i03() as session:
  S=time.monotonic()-t;t2=time.monotonic()
  with instr.phase(forbid_c11_repository=True) as counters:
   res=session.execute_i03(query_ref=q.ref,predicate_ref=p.ref);Q=time.monotonic()-t2;f=res.facts[0];payload=f.as_dict();o=time.monotonic();ser=canonical_json(payload);O=time.monotonic()-o
 refs=lambda n:[exact_ref(r,n).key for r in getattr(f,n,())]
 replay_ref=exact_ref(f.replay_ref,'replay').key
 gz=HERE/'f4.payload.json.gz';gz.write_bytes(gzip.compress((json.dumps(payload,default=str,sort_keys=True)+'\n').encode()))
 # controlled base role truth: A1 & B1, target C; B missing at i%17==0
 N=contract['respondents'];elig=[];cells={}
 for i in range(N):
  if i%2==1 and i%17!=0 and ((i//3)%2)==1:
   elig.append(i);c=str((i%2)^((i//3)%2));cells[c]=cells.get(c,0)+1
 exp_cells=[{'cell':v,'cell_state':'OBSERVED_POSITIVE','raw_numerator_support':cells[v]} for v in sorted(cells)]
 allids=[ctx._respondent(i).ref.key for i in range(N)];expected={'denominator_count':len(elig),'risk_count':N,'cells':exp_cells,'denominator_members':[allids[i] for i in elig],'risk_members':allids}
 actual_cells=payload['semantic_fields']['target_topology']['complete_cell_semantic_projection'];norm=[{k:c[k] for k in ('cell','cell_state','raw_numerator_support')} for c in actual_cells]
 checks={'cells':norm==exp_cells,'risk_set':set(refs('risk_set_member_refs'))==set(expected['risk_members']),'denom_set':set(refs('denominator_member_refs'))==set(expected['denominator_members']),'raw_denominator':f.raw_denominator_support==len(elig),'state':f.typed_state=='SUPPORTED'}
 out={'schema':'ANVIL_WIDTH128_F4_RESULT@1','status':'WIDTH128_F4_COMPLETE','estate_manifest':contract['manifest_sha256'],'respondents':N,'questions':contract['questions'],'events':contract['family_counts']['RespondentEvent'],'routing':contract['family_counts']['RoutingEligibilityFact'],'weights':contract['family_counts']['WeightMeasureFact'],'S_seconds':S,'Q_seconds':Q,'O_seconds':O,'fact_ref':f.ref.key,'replay_ref':replay_ref,'raw_numerator_support':f.raw_numerator_support,'raw_denominator_support':f.raw_denominator_support,'risk_count':len(refs('risk_set_member_refs')),'denominator_count':len(refs('denominator_member_refs')),'checks':checks,'all_expected_match':all(checks.values()),'expected':expected,'payload_file':'f4.payload.json.gz','payload_sha256':hashlib.sha256(ser.encode()).hexdigest(),'counters':counters.material()}
 (HERE/'RESULT.json').write_text(json.dumps(out,indent=2,default=str,sort_keys=True)+'\n');print(json.dumps({'S':S,'Q':Q,'state':f.typed_state,'risk':out['risk_count'],'denom':out['denominator_count'],'all_expected':out['all_expected_match']},sort_keys=True))
if __name__=='__main__':main()
