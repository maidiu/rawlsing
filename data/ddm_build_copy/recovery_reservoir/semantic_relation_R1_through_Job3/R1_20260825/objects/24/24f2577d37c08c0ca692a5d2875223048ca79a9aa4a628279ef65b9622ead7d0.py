#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
scope=json.loads((ROOT/'WORKER_SCOPE.json').read_text())
out=ROOT/'RETURN'
errors=[]
required=[
'T15_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv','T15_PRACTICAL_SHORE_ACCOUNTING.csv',
'T15_CROSSWALK_REVIEW.csv','T15_T06_OVERLAP_AND_BOUNDARY.csv','T15_COMPOSITION_BRIDGE_LEDGER.csv',
'T15_UPSTREAM_REPAIRS.csv','T15_SOURCE_COVERAGE_DEFECTS.csv','T15_BLOCKERS.csv',
'T15_WAVE_COMPLETENESS_ATTESTATION.csv','WORKER_REPORT.md'
]
for fn in required:
    if not (out/fn).exists(): errors.append(f'missing:{fn}')

def rows(fn):
    p=out/fn
    if not p.exists(): return []
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

acc=rows('T15_PRACTICAL_SHORE_ACCOUNTING.csv')
if len(acc)!=scope['implementation_denominator']:
    errors.append(f'accounting_denominator:{len(acc)}!={scope["implementation_denominator"]}')
ids=[r.get('question_implementation_id','') for r in acc]
if len(ids)!=len(set(ids)): errors.append('duplicate_accounting_implementation_id')
waves={(r.get('source_family',''),r.get('wave','')) for r in acc}
expected={tuple(x) for x in scope['wave_keys']}
if waves!=expected: errors.append(f'wave_keys:{sorted(waves)} != {sorted(expected)}')

base=[]
with (ROOT/'AUTHORITY'/'NORMALIZED_PRIOR_T06_IMPLEMENTATION_ACCOUNTING.csv').open(encoding='utf-8-sig',newline='') as f:
    base=list(csv.DictReader(f))
base_norm={r['question_implementation_id'] for r in base if r.get('baseline_t06_classification')=='NORM_SHORE'}
acc_by={r.get('question_implementation_id'):r for r in acc}
missing=base_norm-set(acc_by)
if missing: errors.append(f'missing_prior_norm_rows:{len(missing)}')
def truth(v): return str(v).strip().upper() in {'YES','TRUE','1','PASS','COMPLETE'}
for iid in base_norm:
    r=acc_by.get(iid,{})
    if not truth(r.get('norm_to_praxis_search_completed','')):
        errors.append(f'prior_norm_search_incomplete:{iid}')
for r in acc:
    if str(r.get('t15_praxis_candidate','')).strip().upper()=='YES' and not truth(r.get('praxis_to_norm_search_completed','')):
        errors.append(f'praxis_reverse_search_incomplete:{r.get("question_implementation_id")}')

pos=rows('T15_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv')
allowed={'DIRECT_ENACTMENT','RIGHT_OR_PERMISSION_EXERCISE','PRACTICAL_VIOLATION','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTRUMENTAL_ENACTMENT'}
allowed_shores={'STATED_INTENDED_CONDUCT','REALIZED_SELF_CONDUCT','REALIZED_OTHER_CONDUCT','LIFE_STATE','INSTITUTIONAL_STATE','POLICY_APPLICATION','OTHER_SOURCE_PROVEN_REALIZATION'}
allowed_bridge={'DIRECT_SOURCE_ENTAILMENT','SOURCE_EXPLICIT_MEANS','GOVERNED_T04_BRIDGE','SOURCE_NATIVE_BATTERY_BRIDGE','SOURCE_EXPLICIT_VIOLATION','SOURCE_EXPLICIT_RIGHT_EXERCISE','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION'}
valid_ids=set(ids)
seen=set()
json_fields=['active_source_wave_set_json','member_semantic_unit_ids_json','member_implementation_ids_json','role_assignments_json','bridge_basis_ids_json','source_provenance_json','overlap_with_existing_s14_rule_json']
for r in pos:
    rid=r.get('worker_relation_id','')
    if not rid: errors.append('positive_blank_worker_relation_id')
    if rid in seen: errors.append(f'duplicate_positive_relation_id:{rid}')
    seen.add(rid)
    if r.get('rule_id')!='S14-T15': errors.append(f'wrong_rule:{rid}:{r.get("rule_id")}')
    if r.get('relation_type')!='NORM_PRACTICAL_REALIZATION': errors.append(f'wrong_type:{rid}')
    st=r.get('manifestation_subtype')
    if st not in allowed: errors.append(f'bad_subtype:{rid}:{st}')
    if r.get('praxis_shore_kind') not in allowed_shores: errors.append(f'bad_praxis_shore:{rid}')
    bb=r.get('bridge_basis_type')
    if bb not in allowed_bridge: errors.append(f'bad_bridge_basis:{rid}:{bb}')
    if st=='INSTRUMENTAL_ENACTMENT' and bb not in {'SOURCE_EXPLICIT_MEANS','GOVERNED_T04_BRIDGE','SOURCE_NATIVE_BATTERY_BRIDGE'}:
        errors.append(f'instrumental_without_explicit_bridge:{rid}')
    if r.get('t06_overlap_status')=='EXCLUDE_FROM_T15__STRICT_T06':
        errors.append(f'strict_t06_duplicate_in_positive:{rid}')
    for jf in json_fields:
        try:
            v=json.loads(r.get(jf,'') or '[]')
        except Exception:
            errors.append(f'bad_json:{rid}:{jf}'); continue
        if jf=='member_implementation_ids_json':
            vals=v if isinstance(v,list) else []
            for iid in vals:
                if isinstance(iid,dict): iid=iid.get('implementation_id') or iid.get('question_implementation_id')
                if iid and iid not in valid_ids: errors.append(f'unknown_member:{rid}:{iid}')

att=rows('T15_WAVE_COMPLETENESS_ATTESTATION.csv')
att_keys={(r.get('source_family',''),r.get('wave','')) for r in att}
if att_keys!=expected: errors.append('attestation_wave_keys')
for r in att:
    for k in ['norm_to_praxis_search_complete','praxis_to_norm_search_complete','direct_enactment_reviewed','right_exercise_reviewed','practical_violation_reviewed','institutional_social_realization_reviewed','instrumental_enactment_reviewed','hostile_sparse_wave_qa']:
        if not truth(r.get(k,'')): errors.append(f'attestation_incomplete:{r.get("source_family")}:{r.get("wave")}:{k}')

result={'status':'PASS' if not errors else 'FAIL','error_count':len(errors),'errors':errors,
        'worker_id':scope['worker_id'],'positive_count':len(pos),'accounting_rows':len(acc)}
(out/'VALIDATION.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
sys.exit(0 if not errors else 1)
