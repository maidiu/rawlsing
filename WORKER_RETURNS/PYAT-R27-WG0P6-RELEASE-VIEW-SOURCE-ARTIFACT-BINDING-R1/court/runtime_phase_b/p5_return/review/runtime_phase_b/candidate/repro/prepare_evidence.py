"""Fresh original WG0J probe/numeric reconstruction and actual native cold court."""
import importlib.util,json,os,pathlib,runpy,subprocess,sys
from dataclasses import asdict
import common_v1 as common
from common_v1 import w,R,plan,execute,values,dump
sys.modules['common']=common;sys.modules['wg0p2_workload']=w
# These exact pinned probe and reconstruction bodies inspect genuine native owners.
runpy.run_path(str(R/'pinned/predecessors/j/repro/probe.py'),run_name='__main__')
runpy.run_path(str(R/'pinned/predecessors/j/repro/numerics.py'),run_name='__main__')
# Four real new interpreters: two full controls, one abrupt crash and one resume.
d=R/'runtime'/('cold-proof-'+w.secrets.token_hex(8))
if d.exists():raise RuntimeError('REFUSE_REUSE_OLD_COLD_EVIDENCE_DIRECTORY')
logs={}
for mode in ['crash','resume']:
    child=subprocess.run([sys.executable,str(R/'repro/cold_worker.py'),mode,str(d)],text=True,capture_output=True)
    logs[mode]={'exit':child.returncode,'stdout':child.stdout,'stderr':child.stderr}
    assert child.returncode==(23 if mode=='crash' else 0),logs[mode]
a=json.loads((d/'crash_proof.json').read_text());b=json.loads((d/'resume_proof.json').read_text())
assert a['pid']!=b['pid'] and a['manifest']==b['manifest'] and a['unit_count']==b['unit_count']==3
assert b['summary']['coverage_state']=='FULL_MANIFEST_COVERAGE' and b['remaining_executed']==2
assert sum(c['function']=='execute_empirical_query' for c in a['actual_calls'])==1
assert sum(c['function']=='execute_empirical_query' for c in b['actual_calls'])==2
assert a['receipts'][0] in b['receipts']
# Full deterministic controls run in independent interpreter processes too.
full=[]
code="from common_v1 import *; from dataclasses import asdict; p=plan();r,rs,e=execute(p);print(json.dumps({'receipts':[w.receipt_to_json(x) for x in rs],'values':values(e),'frontier':p.frontier_receipts,'manifest':p.manifest.manifest_hash}))"
for n in range(2):
    pr=subprocess.run([sys.executable,'-c',code],text=True,capture_output=True)
    assert pr.returncode==0,pr.stderr
    full.append(json.loads(pr.stdout));logs['full'+str(n+1)]={'exit':pr.returncode,'stdout':pr.stdout,'stderr':pr.stderr}
assert full[0]==full[1] and full[0]['receipts']==b['receipts'] and full[0]['values']==b['values']
dump('native_cold_crash.json',a);dump('native_cold_resume.json',b)
dump('cold_comparison.json',{'cold_identical_receipts':full[0]['receipts']==full[1]['receipts'],'cold_identical_values':full[0]['values']==full[1]['values'],'cold_frontier25':len(full[0]['frontier'])==25,'resume':b,'shard_combined_unit_keys_match_full':{x['unit_ref']['content_hash'] for x in a['receipts']}|{x['unit_ref']['content_hash'] for x in b['receipts'] if x not in a['receipts']}=={x['unit_ref']['content_hash'] for x in full[0]['receipts']},'shard_values_match_full':b['values']==full[0]['values'],'partition_scope':'Disjoint actual1+2 executed unit partitions of SAME original3-unit manifest; not separate reduced manifests.','processes':{'checkpoint':{'exit':logs['crash']['exit'],'pid':a['pid']},'resume':{'exit':logs['resume']['exit'],'pid':b['pid']},'full1':{'exit':logs['full1']['exit']},'full2':{'exit':logs['full2']['exit']}},'original_receipt_preimage_preserved':a['receipts'][0] in b['receipts'],'no_original_or_35_wave_claim':True})
dump('cold_processes.stdout.json',logs)
c=plan(joint=True);r,rs,e=execute(c);op='OP-WG0P4-JOINT-RT-GIVEN-WG0P4-JOINT-ORD'
assert e[op][0]['denominator']==2 and {x['cell']:x['n'] for x in e[op][0]['cells']}=={'yes':1,'no':1}
dump('ordinary_conditional.json',{'scope':'IMPLEMENTER_SOURCEFREE_ORDINARY_COMPILER_PATH_NOT_INDEPENDENT_ACCEPTANCE','frontier':c.frontier_receipts,'science_root':c.science_root,'manifest':c.manifest.semantic_projection(),'receipts':[w.receipt_to_json(x) for x in rs],'query':c.op_specs[op].query.semantic_projection(),'predicate':c.op_specs[op].predicate.semantic_projection(),'actual_consumer':e[op][0],'summary':asdict(r.summary())})
print('FRESH_NATIVE_COLD_ORIGINAL3_AND_ORDINARY_CONDITIONAL_PASS')
