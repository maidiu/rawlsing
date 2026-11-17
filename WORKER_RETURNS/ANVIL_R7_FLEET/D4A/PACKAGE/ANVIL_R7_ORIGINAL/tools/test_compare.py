#!/usr/bin/env python3
"""Paired full-set comparison adversarial unit cases; no scientific/runner authentication."""
import copy,json,hashlib
from compare_candidates import full_comparison
cases=['W-S','W-D','W-R','W-O','W-J','W-U','W-X']
frozen={'schema':'ANVIL_R5_FROZEN_MATERIAL_CELLS','cells':[{'id':'C'+str(i),'workload_case_id':c,'metric':'query_100_wall_s' if c in {'W-O','W-J','W-U'} else 'build_wall_s','input_identity':'same exact 100k sourcefree respondent event estate','runner_identity':'same physical host, monotonic clock and environment','negative_restore_oracle':'exact positive, negative and restored source qualified reader','decision_reversal_if_A':'A better at actual relevant whole physical workload','decision_reversal_if_B':'B better at actual relevant whole physical workload','required_claim_grade':'EXECUTED_SOURCEFREE_MATCHED','source_cut':'s0-synthetic-source-cut','source_grade':'SOURCEFREE_SYNTHETIC','fixture_id':'sourcefree_100k_same_fixture','runner_id':'host_fixture_real_same'} for i,c in enumerate(cases)],'exclusions':[]}
input={'schema':'ANVIL_R5_COMPARATOR_INPUT','candidate_ids':['A','B'],'frozen_sha256':hashlib.sha256(json.dumps(frozen,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),'hard_vetoes':{'A':[],'B':[]},'measurements':[{'cell_id':c['id'],'source_cut':c['source_cut'],'source_grade':c['source_grade'],'fixture_id':c['fixture_id'],'runner_id':c['runner_id'],'A':{'status':'MEASURED','value':10,'low':9,'high':11,'receipt_path':'a_'+c['id'],'receipt_sha256':'a'*64},'B':{'status':'MEASURED','value':20,'low':19,'high':21,'receipt_path':'b_'+c['id'],'receipt_sha256':'b'*64}} for c in frozen['cells']]}
r=full_comparison(input,frozen);assert r['status']=='A_DOMINATES_FULL_FROZEN_SET' and r['winner']=='A',r
results={'full_exact_matched_set':'A_DOMINATES_FULL_FROZEN_SET'}
def run(name, mutate, expected):
    x=copy.deepcopy(input);f=copy.deepcopy(frozen);mutate(x,f);res=full_comparison(x,f);assert res['status']==expected,(name,res);results[name]=res['status']
run('favorable_one_metric_no_broad_victory',lambda x,f:x['measurements'].__delitem__(slice(1,None)),'MISSING_DECISIVE_EVIDENCE')
run('B_unmeasured_decisive',lambda x,f:x['measurements'][2]['B'].update(status='UNRUN_HELD'),'MISSING_DECISIVE_EVIDENCE')
run('reported_one_cell_conflicts_scope',lambda x,f:x['measurements'][0].update(source_cut='wrong_source'),'RED')
run('late_inserted_measurement_cell',lambda x,f:x['measurements'].append({**x['measurements'][0],'cell_id':'LATE'}),'RED')
run('A_and_B_tradeoff',lambda x,f:x['measurements'][1].update(A={'status':'MEASURED','value':30,'low':29,'high':31,'receipt_path':'a','receipt_sha256':'a'*64},B={'status':'MEASURED','value':20,'low':19,'high':21,'receipt_path':'b','receipt_sha256':'b'*64}),'TRADEOFF')
run('same_uncertain_interval',lambda x,f:x['measurements'][0].update(A={'status':'MEASURED','value':20,'low':15,'high':25,'receipt_path':'a','receipt_sha256':'a'*64},B={'status':'MEASURED','value':20,'low':15,'high':25,'receipt_path':'b','receipt_sha256':'b'*64}),'PARETO_NONDECISIVE')
run('invalid_unit_or_unaccounted_census',lambda x,f:f['cells'].pop(),'RED')
run('false_hard_veto_without_second',lambda x,f:x.update(hard_vetoes={'A':['unknown']}),'RED')
print(json.dumps({'status':'PASS_NUMERICAL_SYNTHETIC_ONLY','cases':results,'count':len(results)},indent=2))
