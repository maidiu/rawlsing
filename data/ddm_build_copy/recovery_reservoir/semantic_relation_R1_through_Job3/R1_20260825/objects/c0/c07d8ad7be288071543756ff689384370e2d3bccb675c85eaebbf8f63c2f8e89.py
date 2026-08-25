import pandas as pd,json,hashlib,pathlib,sys
from collections import Counter
R=pathlib.Path(__file__).resolve().parent; O=R/'RETURN'; A=R/'AUTHORITY'
errs=[]; checks=[]
def ck(name,cond,detail=''):
    checks.append({'check':name,'pass':bool(cond),'detail':detail})
    if not cond: errs.append(name+(':'+detail if detail else ''))

def read(n): return pd.read_csv(O/n,dtype=str).fillna('')
base=pd.read_csv(A/'NORMALIZED_PRIOR_T06_IMPLEMENTATION_ACCOUNTING.csv',dtype=str).fillna('')
cal=pd.read_csv(A/'ASSIGNED_T06_CALIBRATION_SLICE.csv',dtype=str).fillna('')
acc=read('T15_PRACTICAL_SHORE_ACCOUNTING.csv'); pos=read('T15_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv'); cw=read('T15_CROSSWALK_REVIEW.csv'); ov=read('T15_T06_OVERLAP_AND_BOUNDARY.csv'); att=read('T15_WAVE_COMPLETENESS_ATTESTATION.csv'); defe=read('T15_SOURCE_COVERAGE_DEFECTS.csv'); bl=read('T15_BLOCKERS.csv')
parent=R/'PARENT_T06_RETURN/Rawlsing_R10K_S14_T06_SourceFirst_T06W04_Return_20260812.zip'
ck('parent_t06_sha256_immutable',hashlib.sha256(parent.read_bytes()).hexdigest()=='902c1b381445275e62604df2c9ddebb870cba54a109b5576aea1149a02412447')
ck('accounting_exact_base_ids',set(acc.question_implementation_id)==set(base.question_implementation_id) and len(acc)==len(base)==3052)
ck('all_prior_norm_search',all(acc.set_index('question_implementation_id').loc[i,'norm_to_praxis_search_completed'].upper()=='YES' for i in base.loc[base.baseline_t06_classification=='NORM_SHORE','question_implementation_id']))
ck('all_new_norm_search',all(x=='YES' for x in acc.loc[acc.t15_norm_candidate=='YES','norm_to_praxis_search_completed']))
ck('all_praxis_reverse_search',all(x=='YES' for x in acc.loc[acc.t15_praxis_candidate=='YES','praxis_to_norm_search_completed']))
# positive to crosswalk one-to-one
posids=set(pos.worker_relation_id); cpos=set(cw.loc[cw.disposition=='POSITIVE_T15','positive_relation_id'])
ck('positive_crosswalk_bijection',posids==cpos and len(posids)==len(cw[cw.disposition=='POSITIVE_T15']))
# strict overlap exact exclusion
strict=cal[cal.central_strict_t06_posture=='RETAIN_STRICT_T06']; boundary=cal[cal.central_strict_t06_posture=='BOUNDARY_TO_T15']
ck('strict_overlap_ledger_count',len(ov[ov.t15_overlap_disposition=='EXCLUDE_FROM_T15__STRICT_T06'])==len(strict)==24)
ck('boundary_recommendation_count',len(ov[ov.t15_overlap_disposition=='RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW'])==len(boundary)==11)
# all boundary parent IDs appear in positive overlap json
seen=set()
for _,r in pos.iterrows():
    try: arr=json.loads(r.overlap_with_existing_s14_rule_json or '[]')
    except: arr=[]
    for x in arr:
        if isinstance(x,dict) and x.get('worker_relation_id'): seen.add(x['worker_relation_id'])
ck('all_11_boundary_canaries_reconstructed',set(boundary.worker_relation_id)<=seen,f'missing={sorted(set(boundary.worker_relation_id)-seen)}')
# no strict parent id in positive overlap
strictids=set(strict.worker_relation_id)
ck('no_strict_t06_in_positive',not (strictids & seen),f'bad={sorted(strictids&seen)}')
# no peoptrbl positive
peop=base[(base.source_family=='GSS')&(base.wave=='2002')&(base.source_variable_code.str.lower()=='peoptrbl')].iloc[0].question_implementation_id
p_members=[]
for x in pos.member_implementation_ids_json:
    p_members+=json.loads(x)
ck('peoptrbl_central_reopen_not_positive',peop not in p_members)
# instrumental law
inst=pos[pos.manifestation_subtype=='INSTRUMENTAL_ENACTMENT']
ck('instrumental_count',len(inst)==3)
ck('instrumental_explicit_bridge_only',set(inst.bridge_basis_type)<= {'SOURCE_EXPLICIT_MEANS','GOVERNED_T04_BRIDGE','SOURCE_NATIVE_BATTERY_BRIDGE'})
ck('instrumental_has_basis_ids',all(len(json.loads(x or '[]'))>0 for x in inst.bridge_basis_ids_json))
# EVS zero support
for wave in ['2008','1990']:
    ck(f'EVS_{wave}_zero_positive',len(pos[(pos.source_family=='EVS')&(pos.wave==wave)])==0)
    a=att[(att.source_family=='EVS')&(att.wave==wave)].iloc[0]
    ck(f'EVS_{wave}_zero_attested',a.zero_positive_supportable.startswith('YES') and a.hostile_sparse_wave_qa=='YES')
# environmental condition mismatch must be negative, never positive
id126=base[(base.source_family=='EVS')&(base.wave=='1990')&(base.source_variable_code.str.lower()=='q126c')].iloc[0].question_implementation_id
id124=base[(base.source_family=='EVS')&(base.wave=='1990')&(base.source_variable_code.str.lower()=='q124a')].iloc[0].question_implementation_id
id125=base[(base.source_family=='EVS')&(base.wave=='1990')&(base.source_variable_code.str.lower()=='q125b')].iloc[0].question_implementation_id
ck('EVS1990_cost_conflict_not_positive',not any(id126 in json.loads(x) and (id124 in json.loads(x) or id125 in json.loads(x)) for x in pos.member_implementation_ids_json))
ck('EVS1990_cost_conflict_negative_ledgered',any(r.disposition=='NOT_T15_SOURCE_PROVEN_MISMATCH' and id126 in json.loads(r.norm_implementation_ids_json) and id124 in json.loads(r.praxis_implementation_ids_json) for _,r in cw.iterrows()))
# coverage defect claims: C33/C31a absent, c24/q98/Q551 implementations present but collapsed
base_codes={(r.source_family,r.wave,r.source_variable_code.lower()) for _,r in base.iterrows()}
ck('south_c33_absent_selected',('South Asia','W1','c33') not in base_codes)
ck('south_c31a_absent_selected',('South Asia','W1','c31a') not in base_codes)
for fam,w,c in [('South Asia','W1','c24'),('Asian Barometer','W5','q98'),('Arab Barometer','VIII','q551a'),('Arab Barometer','VIII','q551b')]: ck(f'collapsed_impl_present_{fam}_{c}',(fam,w,c) in base_codes)
ck('coverage_defect_count',len(defe)==6)
# accounting positive map consistency
for _,p in pos.iterrows():
    mem=json.loads(p.member_implementation_ids_json)
    for iid in mem:
        ar=acc[acc.question_implementation_id==iid].iloc[0]
        ids=json.loads(ar.positive_relation_ids_json or '[]')
        if p.worker_relation_id not in ids: errs.append(f'accounting_missing_positive:{p.worker_relation_id}:{iid}')
ck('accounting_positive_relation_backrefs',not any(e.startswith('accounting_missing_positive:') for e in errs))
# attestation counts exactly reproduce outputs
for _,a in att.iterrows():
    fam,w=a.source_family,a.wave
    ck(f'att_pos_{fam}_{w}',int(a.positive_t15_count)==len(pos[(pos.source_family==fam)&(pos.wave==w)]))
    ck(f'att_block_{fam}_{w}',int(a.blocked_count)==len(cw[(cw.source_family==fam)&(cw.wave==w)&(cw.disposition=='BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY')]))
    ck(f'att_neg_{fam}_{w}',int(a.source_proven_mismatch_count)==len(cw[(cw.source_family==fam)&(cw.wave==w)&(cw.disposition=='NOT_T15_SOURCE_PROVEN_MISMATCH')]))
    ck(f'att_def_{fam}_{w}',int(a.coverage_defect_count)==len(defe[(defe.source_family==fam)&(defe.wave==w)]))
# all 5 subtypes, expected stable counts
expected={'DIRECT_ENACTMENT':2,'RIGHT_OR_PERMISSION_EXERCISE':4,'PRACTICAL_VIOLATION':6,'INSTITUTIONAL_OR_SOCIAL_REALIZATION':19,'INSTRUMENTAL_ENACTMENT':3}
ck('subtype_counts_exact',pos.groupby('manifestation_subtype').size().to_dict()==expected,str(pos.groupby('manifestation_subtype').size().to_dict()))
expectedwaves={('GSS','2002'):2,('Arab Barometer','VIII'):18,('EVS','2008'):0,('EVS','1990'):0,('Asian Barometer','W5'):12,('South Asia','W1'):2}
actual={(f,w):len(pos[(pos.source_family==f)&(pos.wave==w)]) for f,w in expectedwaves}
ck('wave_counts_exact',actual==expectedwaves,str(actual))
# every block has blocker row and no block converted to positive
blockcw=cw[cw.disposition=='BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY']
ck('all_blocks_have_blocker',all(x in set(bl.blocker_id) for x in blockcw.blocker_id) and len(bl)==len(blockcw))
# no blank implementation member in positives
ck('all_positive_members_bound',all(all(i in set(base.question_implementation_id) for i in json.loads(x)) and len(json.loads(x))>=2 for x in pos.member_implementation_ids_json))
result={'status':'PASS' if not errs else 'FAIL','error_count':len(errs),'errors':errs,'check_count':len(checks),'checks':checks,'positive_count':len(pos),'block_count':len(bl),'coverage_defect_count':len(defe)}
(O/'HOSTILE_VALIDATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
sys.exit(0 if not errs else 1)
