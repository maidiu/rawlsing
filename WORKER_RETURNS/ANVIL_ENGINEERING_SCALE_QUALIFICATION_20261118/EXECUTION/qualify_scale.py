#!/usr/bin/env python3
"""ONE fresh-process prepared 5-op scale qualification; PREP script, not run."""
from __future__ import annotations
import argparse, hashlib, json, sys, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
MEASURE=HERE.parents[2]/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'
VEND=MEASURE/'vendor'

def sha(b): return hashlib.sha256(b).hexdigest()
def j(v): return json.loads(__import__('rawlsing_next.pre553_empirical_objects',fromlist=['canonical_json']).canonical_json(v))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--snapshot',required=True);ap.add_argument('--contract',required=True);ap.add_argument('--out',required=True);ap.add_argument('--max-seconds',type=float,default=600);ap.add_argument('--max-rss-bytes',type=int,default=6*1024**3);ap.add_argument('--max-scratch-bytes',type=int,default=4*1024**3);a=ap.parse_args()
 snap=Path(a.snapshot).resolve();sys.path[:0]=[str(snap),str(VEND)]
 from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref, ExactRef
 from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
 from court_instrumentation import CourtInstrumentation, directory_bytes, process_tree_rss_bytes
 from fixture_1006 import ShapeSpec, build_context
 from query_1006 import build_query_bundle
 contract=json.loads(Path(a.contract).read_text()); root=Path(contract['root']); grant={'ok':True}
 shape=ShapeSpec('scale-10k',contract['respondents'],include_weights=True,tag=contract['tag']);ctx=build_context(shape);bundle=build_query_bundle(ctx)
 names=(('selected_weighted','weighted'),('f2_forward_raw','f2_forward'),('f2_reverse_raw','f2_reverse'),('f4_three_raw','f4_three'),('repeated_mr_raw','repeated'))
 ops=[]
 for label,key in names:
  q,p=bundle.by_name(key);ops.append((label,q,p))
 def estate_open():
  from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
  from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
  return VerifiedDirectEstate(root,exact_path=contract['exact_path'],independently_held_manifest_sha256=contract['manifest_sha256'],independently_held_i02=ExternalI02Roots(**contract['i02']),current_authorizer=lambda _r:grant['ok'])
 h0=time.monotonic(); adm=PreparedSavedC11Admission.open(root=root,exact_path=contract['exact_path'],independently_held_manifest_sha256=contract['manifest_sha256'],independently_held_i02=__import__('rawlsing_next._pre553_external_i02_certificate',fromlist=['ExternalI02Roots']).ExternalI02Roots(**contract['i02']),release_ref=exact_ref(contract['reconstructed_v1_release_ref']),runtime_catalog=bundle.catalog,current_authorizer=lambda _r:grant['ok']);h=time.monotonic()-h0
 rows=[];start=time.monotonic();instrument=CourtInstrumentation()
 with instrument.phase(forbid_c11_repository=True) as counters:
  entry=time.monotonic()
  with adm.prepared_i03() as session:
   index_seconds=time.monotonic()-entry
   for index,(label,q,p) in enumerate(ops):
    if time.monotonic()-start>a.max_seconds: raise SystemExit('ABORT_TOTAL_LIMIT')
    op0=time.monotonic();res=session.execute_i03(query_ref=q.ref,predicate_ref=p.ref);wall=time.monotonic()-op0
    facts=list(res.facts);sem=canonical_json([f.semantic_projection() for f in facts]);ident=canonical_json([f.as_dict() for f in facts]);refs=canonical_json([f.ref.as_dict() for f in facts]);replay=canonical_json([exact_ref(f.replay_ref,'replay').as_dict() for f in facts]);members=[]
    for f in facts:
     for key in ('risk_set_member_refs','denominator_member_refs'):
      members += [exact_ref(r,key).key for r in getattr(f,key,())]
    mem=canonical_json(sorted(set(members)))
    rows.append({'label':label,'operation_index':index,'wall_seconds':wall,'fact_count':len(facts),'typed_states':[getattr(f,'typed_state',None) for f in facts],'raw_denominator_support':[getattr(f,'raw_denominator_support',None) for f in facts],'semantic_sha256':sha(sem.encode()),'identity_sha256':sha(ident.encode()),'refs_sha256':sha(refs.encode()),'replay_sha256':sha(replay.encode()),'member_refs_sha256':sha(mem.encode()),'semantic_bytes':len(sem.encode()),'identity_bytes':len(ident.encode()),'output_bytes':len(ident.encode())+len(refs.encode())+len(replay.encode())+len(mem.encode())})
   receipt=session.receipt().as_dict()
 out={'schema':'ANVIL_SCALE_QUALIFICATION_RESULT@1','status':'COMPLETE','grade':'SOURCEFREE_TEST_ONLY_SURVEY_SCALE_QUALIFICATION','integrated_commit':'68aa7cac7cce7057fefd458ef4a06bec2dede1b2','fixture':contract,'operations':rows,'completed':len(rows),'admission_seconds':h,'index_build_seconds':index_seconds,'total_wall_seconds':time.monotonic()-start,'counters':counters.material(),'process_tree_rss_end':process_tree_rss_bytes(),'retained_bytes':contract['retained_bytes'],'session_receipt':receipt,'negative':'NOT_INCLUDED_TIMED_POSITIVE_ONLY','limits':['5 distinct ops only; no 100k/native/science/actor/CURRENT acceptance','one fresh process; OS cache uncontrolled']}
 Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'COMPLETE','completed':len(rows),'out':a.out},sort_keys=True))
if __name__=='__main__': main()
