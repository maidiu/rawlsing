#!/usr/bin/env python3
"""Matched separate-process baseline/candidate runner for WIDTH128 f2 pair.

PREP ONLY: this file is executable but was not run by the return.
Each variant uses a distinct frozen code commit and a fresh process/session.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, os, shutil, signal, subprocess, sys, tempfile, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
MEASUREMENT_PREP=HERE.parents[2]
REPO=MEASUREMENT_PREP
MP=REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'
W=REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118'/'WIDTH128'
CONTRACT=W/'fixture_contract_width128.json';SHARED_GIT=Path('/Users/matthewsmith/s2b-work/rawlsing')
CAP=600.0;RSS=6*1024**3;SCRATCH=4*1024**3;TOTAL=900.0

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def child(variant,snapshot,out):
 sys.path[:0]=[str(snapshot),str(MP),str(MP/'vendor')]
 from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
 from rawlsing_next.pre553_empirical_objects import ExactRef,canonical_json,exact_ref
 from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
 from fixture_1006 import ShapeSpec,build_context
 from query_1006 import build_query_bundle
 from court_instrumentation import CourtInstrumentation,process_tree_rss_bytes,directory_bytes
 import rawlsing_next._pre553_query_eval as qeval
 import rawlsing_next.pre553_direct_estate_i03 as direct
 from rawlsing_next.pre553_empirical_objects import RoutingEligibilityFact
 rc={'setup':0,'query':0};phase={'name':'setup'}
 orig_obj=direct._object_from_row
 def obj_wrap(value):
  o=orig_obj(value)
  if type(o) is RoutingEligibilityFact:rc[phase['name']]+=1
  return o
 direct._object_from_row=obj_wrap
 c=json.loads(CONTRACT.read_text());root=Path(c['root']);tag=c['tag'];ctx=build_context(ShapeSpec('width128',c['respondents'],include_weights=True,tag=tag));bundle=build_query_bundle(ctx)
 def open_adm():
  return PreparedSavedC11Admission.open(root=root,exact_path=c['exact_path'],independently_held_manifest_sha256=c['manifest_sha256'],independently_held_i02=ExternalI02Roots(**c['i02']),release_ref=exact_ref(c['reconstructed_v1_release_ref']),runtime_catalog=bundle.catalog,current_authorizer=lambda _r:True)
 h0=time.monotonic();adm=open_adm();H=time.monotonic()-h0
 orig_lookup=qeval._routing_fact_for;lookup_calls={'n':0,'sec':0.0}
 def lookup(*a,**k):
  t=time.monotonic()
  try:return orig_lookup(*a,**k)
  finally:lookup_calls['n']+=1;lookup_calls['sec']+=time.monotonic()-t
 qeval._routing_fact_for=lookup
 try:
  instr_b=CourtInstrumentation()
  with instr_b.phase(forbid_c11_repository=True) as bc:
   t=time.monotonic();ctx_s=adm.prepared_i03();session=ctx_s.__enter__();S=time.monotonic()-t
  build_counters=bc.material();phase['name']='query'
  instr_q=CourtInstrumentation();rows=[]
  with instr_q.phase(forbid_c11_repository=True) as qc:
   for key in ('f2_forward','f2_reverse'):
    q,p=bundle.by_name(key);t0=time.monotonic();res=session.execute_i03(query_ref=q.ref,predicate_ref=p.ref);Q=time.monotonic()-t0
    f=res.facts[0];payload=f.as_dict();t1=time.monotonic();ser=canonical_json(payload);O=time.monotonic()-t1
    refs=lambda n:[exact_ref(r,n).key for r in getattr(f,n,())]
    rows.append({'label':key,'query_ref':q.ref.key,'predicate_ref':p.ref.key,'Q_seconds':Q,'O_seconds':O,'fact_ref':f.ref.key,'replay_ref':exact_ref(f.replay_ref,'replay').key,'typed_state':f.typed_state,'raw_numerator':f.raw_numerator_support,'raw_denominator':f.raw_denominator_support,'cells':payload['semantic_fields']['target_topology']['complete_cell_semantic_projection'],'risk_set_member_refs':refs('risk_set_member_refs'),'denominator_member_refs':refs('denominator_member_refs'),'provenance_refs':refs('source_empirical_provenance_refs'),'payload_sha256':hashlib.sha256(ser.encode()).hexdigest(),'payload':payload})
  qcounters=qc.material();ctx_s.__exit__(None,None,None);direct._object_from_row=orig_obj
  out.write_text(json.dumps({'schema':'ANVIL_ROUTING_MATCHED_VARIANT@1','variant':variant,'snapshot':str(snapshot),'product_sha256':sha(snapshot/'rawlsing_next/pre553_direct_estate_i03.py'),'estate_manifest':c['manifest_sha256'],'contract_sha256':sha(CONTRACT),'H_seconds':H,'S_seconds':S,'build_counters':build_counters,'query_counters':qcounters,'routing_objects_build':rc['setup'],'routing_objects_query':rc['query'],'routing_lookup_calls':lookup_calls['n'],'routing_lookup_seconds':lookup_calls['sec'],'operations':rows,'rss_end':process_tree_rss_bytes(),'limits':['one fresh process; two operations; no rebuild','OS cache uncontrolled']},indent=2,sort_keys=True)+'\n')
 finally:qeval._routing_fact_for=orig_lookup

def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def supervise(cmd,label,outdir):
 from court_instrumentation import process_tree_rss_bytes,directory_bytes
 contract=json.loads(CONTRACT.read_text());estate_root=Path(contract['root']);retained=int(contract['retained_bytes'])
 start=time.monotonic();p=subprocess.Popen(cmd,cwd=str(REPO),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);samples=[];abort=None
 while p.poll() is None:
  time.sleep(.25);e=time.monotonic()-start;r=process_tree_rss_bytes(p.pid);estate_bytes=directory_bytes(estate_root);scratch=max(0,estate_bytes-retained);owned=directory_bytes(outdir);samples.append({'e':e,'rss':r,'estate_scratch':scratch,'owned_outdir':owned})
  if e>CAP:abort='WALL_600S'
  elif r>RSS:abort='RSS_6GIB'
  elif s>SCRATCH:abort='SCRATCH_4GIB'
  if abort:break
 if abort:
  try:os.killpg(p.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  try:p.wait(timeout=3)
  except subprocess.TimeoutExpired:
   try:os.killpg(p.pid,signal.SIGKILL)
   except ProcessLookupError:pass
   p.wait(timeout=3)
 o,e=p.communicate(timeout=10);return {'exit':p.returncode,'abort':abort,'wall':time.monotonic()-start,'rss_peak':max((x['rss'] for x in samples),default=0),'scratch_peak':max((x['estate_scratch'] for x in samples),default=0),'owned_outdir_peak':max((x['owned_outdir'] for x in samples),default=0),'samples':len(samples),'stdout':o,'stderr':e}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--baseline-commit',required=True);ap.add_argument('--candidate-commit',required=True);ap.add_argument('--outdir',required=True);a=ap.parse_args();out=Path(a.outdir).resolve();out.mkdir(parents=True,exist_ok=True);base_snap=Path(tempfile.mkdtemp(prefix='anvil-routing-base-',dir='/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode'));cand_snap=Path(tempfile.mkdtemp(prefix='anvil-routing-cand-',dir='/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode'))
 for commit,snap in ((a.baseline_commit,base_snap),(a.candidate_commit,cand_snap)):
  archive=subprocess.check_output(['git','-C',str(SHARED_GIT),'archive',commit,'rawlsing_next']); subprocess.run(['tar','-x','-C',str(snap)],input=archive,check=True)
  if not (snap/'rawlsing_next/pre553_direct_estate_i03.py').exists():raise SystemExit('SNAPSHOT_MISSING')
 res={}
 for variant,snap in [('baseline',base_snap),('candidate',cand_snap)]:
  child_out=out/f'{variant}.json';cmd=[sys.executable,str(Path(__file__)),'--child',variant,'--snapshot',str(snap),'--out',str(child_out)]
  # Parent process executes child mode via re-entry below; use subprocess with an internal child entry.
  cmd=[sys.executable,str(Path(__file__)),'--child-run',variant,str(snap),str(child_out)]
  res[variant]=supervise(cmd,variant,out)
  res[variant]['file']=str(child_out)
  if res[variant]['exit'] != 0 or res[variant]['abort']:
   (out/'RUN_RESULT.json').write_text(json.dumps({'schema':'ANVIL_ROUTING_MATCHED_RUNNER@1','status':'CHILD_FAILED_OR_ABORTED','variant':variant,'variant_result':res[variant]},indent=2,sort_keys=True)+'\n')
   raise SystemExit(1)
  cumulative = res['baseline']['wall'] if variant=='baseline' else res['baseline']['wall']+res['candidate']['wall']
  if cumulative > TOTAL:
   (out/'RUN_RESULT.json').write_text(json.dumps({'schema':'ANVIL_ROUTING_MATCHED_RUNNER@1','status':'TOTAL_CAP_EXCEEDED','baseline':res['baseline'],'candidate':res.get('candidate')},indent=2,sort_keys=True)+'\n')
   raise SystemExit(1)
 (out/'RUN_RESULT.json').write_text(json.dumps({'schema':'ANVIL_ROUTING_MATCHED_RUNNER@1','baseline_commit':a.baseline_commit,'candidate_commit':a.candidate_commit,'contract':str(CONTRACT),'estate_manifest':json.loads(CONTRACT.read_text())['manifest_sha256'],'baseline':res['baseline'],'candidate':res['candidate'],'caps':{'per_child':CAP,'total':TOTAL,'rss':RSS,'scratch':SCRATCH},'note':'separate frozen snapshots and fresh sessions; no adapter disabled in one session'},indent=2,sort_keys=True)+'\n')
 # Separate exact-full-payload comparison and total-cost accounting.
 b=json.loads((out/'baseline.json').read_text());c=json.loads((out/'candidate.json').read_text())
 br={r['label']:r for r in b['operations']};cr={r['label']:r for r in c['operations']};expected={'f2_forward','f2_reverse'}
 if set(br)!=expected or set(cr)!=expected:
  (out/'COMPARISON.json').write_text(json.dumps({'schema':'ANVIL_ROUTING_MATCHED_COMPARISON@1','all_exact':False,'error':'EXPECTED_TWO_OPERATION_MISMATCH','baseline_labels':sorted(br),'candidate_labels':sorted(cr)},indent=2,sort_keys=True)+'\n');raise SystemExit(1)
 checks={}
 for label in sorted(br):
  checks[label]={'fact_ref':br[label]['fact_ref']==cr[label]['fact_ref'],'payload_sha':br[label]['payload_sha256']==cr[label]['payload_sha256'],'payload_exact':json.dumps(br[label]['payload'],sort_keys=True,separators=(',',':'),default=str)==json.dumps(cr[label]['payload'],sort_keys=True,separators=(',',':'),default=str),'risk_set':set(br[label]['risk_set_member_refs'])==set(cr[label]['risk_set_member_refs']),'denom_set':set(br[label]['denominator_member_refs'])==set(cr[label]['denominator_member_refs']),'provenance':set(br[label]['provenance_refs'])==set(cr[label]['provenance_refs']),'replay':br[label]['replay_ref']==cr[label]['replay_ref']}
 bs=b['H_seconds']+b['S_seconds'];cs=c['H_seconds']+c['S_seconds'];bq=sum(r['Q_seconds'] for r in b['operations']);cq=sum(r['Q_seconds'] for r in c['operations']);bo=sum(r['O_seconds'] for r in b['operations']);co=sum(r['O_seconds'] for r in c['operations'])
 comp={'schema':'ANVIL_ROUTING_MATCHED_COMPARISON@1','ops':checks,'all_exact':all(all(v.values()) for v in checks.values()),'setup':{'baseline_H_plus_S':bs,'candidate_H_plus_S':cs,'candidate_added_setup_seconds':cs-bs},'operation':{'baseline_Q':bq,'candidate_Q':cq,'delta_Q':cq-bq,'baseline_O':bo,'candidate_O':co},'end_to_end':{'baseline_H_S_Q_O':bs+bq+bo,'candidate_H_S_Q_O':cs+cq+co},'routing':{'baseline_lookup_calls':b['routing_lookup_calls'],'candidate_lookup_calls':c['routing_lookup_calls'],'baseline_setup_family_objects':b['build_counters']['family_object_materializations'],'candidate_setup_family_objects':c['build_counters']['family_object_materializations']},'external':{'baseline':res['baseline']['wall'],'candidate':res['candidate']['wall'],'total':res['baseline']['wall']+res['candidate']['wall']},'note':'one measured pair only; no extrapolation/speedup claim'}
 (out/'COMPARISON.json').write_text(json.dumps(comp,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='--child-run':
  _,_,variant,snap,out=sys.argv;child(variant,Path(snap),Path(out));raise SystemExit(0)
 if len(sys.argv)>1 and sys.argv[1]=='--child':
  raise SystemExit('use --child-run')
 main()
