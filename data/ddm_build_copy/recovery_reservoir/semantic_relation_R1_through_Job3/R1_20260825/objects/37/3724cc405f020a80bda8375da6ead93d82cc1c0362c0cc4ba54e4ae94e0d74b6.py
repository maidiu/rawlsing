#!/usr/bin/env python3
import csv, json, os, sys, hashlib
from collections import Counter, defaultdict
from pathlib import Path

WORKER='T06W02'
EXPECTED_SHA='e88cc035ca1d846e68ee208ec991f61f636d67ebbd19312057c8e44c37ff740d'
EXPECTED={('LiTS','III'):1290,('LiTS','II'):627,('Afrobarometer','R9'):421,('EVS','1981'):370,('Latinobarómetro','1995'):203,('Arab Barometer','I'):181}
ALLOWED_CLASS={'NORM_SHORE','CONDUCT_SHORE','OTHER','SOURCE_AMBIGUOUS'}
ALLOWED_DISP={'POSITIVE_T06','BLOCKED_SOURCE_AMBIGUITY','NOT_T06_SOURCE_PROVEN_MISMATCH'}
ALLOWED_ROLES={'RR_NORM','RR_STATED_OR_INTENDED_CONDUCT','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT'}
REQUIRED=[
'T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv','T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv',
'T06_SOURCE_FIRST_CROSSWALK_REVIEW.csv','T06_SOURCE_FIRST_UPSTREAM_REPAIRS.csv','T06_SOURCE_COVERAGE_DEFECTS.csv',
'T06_SOURCE_FIRST_BLOCKERS.csv','T06_WAVE_COMPLETENESS_ATTESTATION.csv','WORKER_REPORT.md','HOSTILE_QA.json','VALIDATION.json']
ROOT=Path(__file__).resolve().parents[1]
RET=ROOT/'RETURN'
SOURCE_ZIP=Path('/mnt/data/t06w02_source_first/Rawlsing_SourceNative_Questionnaire_Structure_Authority_R1_20260812.zip')
checks=[]
def ck(name,cond,detail=''):
    checks.append({'check':name,'status':'PASS' if cond else 'FAIL','detail':str(detail)})

def read_csv(name):
    with open(RET/name,newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))

# Presence (VALIDATION is overwritten by this script, so allow absent before write).
for n in REQUIRED[:-1]: ck('required_file_'+n,(RET/n).is_file(),str(RET/n))

acc=read_csv('T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv')
pos=read_csv('T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv')
rev=read_csv('T06_SOURCE_FIRST_CROSSWALK_REVIEW.csv')
rep=read_csv('T06_SOURCE_FIRST_UPSTREAM_REPAIRS.csv')
defects=read_csv('T06_SOURCE_COVERAGE_DEFECTS.csv')
blocks=read_csv('T06_SOURCE_FIRST_BLOCKERS.csv')
att=read_csv('T06_WAVE_COMPLETENESS_ATTESTATION.csv')

# Source authority hash.
if SOURCE_ZIP.exists():
    h=hashlib.sha256();
    with open(SOURCE_ZIP,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    got=h.hexdigest()
else: got='MISSING'
ck('source_authority_sha256',got==EXPECTED_SHA,got)

# Accounting exact denominator.
ck('accounting_total_3092',len(acc)==3092,len(acc))
ids=[r['question_implementation_id'] for r in acc]
ck('accounting_unique_implementation_ids',len(ids)==len(set(ids)),len(set(ids)))
counts=Counter((r['source_family'],r['wave']) for r in acc)
ck('assigned_wave_set_exact',set(counts)==set(EXPECTED),sorted(counts))
for k,n in EXPECTED.items(): ck('wave_count_'+k[0]+'_'+k[1],counts[k]==n,counts[k])
ck('accounting_classification_vocabulary',all(r['t06_reconstruction_classification'] in ALLOWED_CLASS for r in acc),Counter(r['t06_reconstruction_classification'] for r in acc))
ck('every_row_accounted',all(r['t06_reconstruction_classification'] for r in acc),'all classification nonblank')
ck('norm_forward_search_complete',all(r['norm_to_conduct_search_completed']=='YES' for r in acc if r['t06_reconstruction_classification']=='NORM_SHORE'),'')
ck('conduct_reverse_search_complete',all(r['conduct_to_norm_search_completed']=='YES' for r in acc if r['t06_reconstruction_classification']=='CONDUCT_SHORE'),'')

byid={r['question_implementation_id']:r for r in acc}
# Positives.
ck('positive_relation_ids_unique',len(pos)==len({r['worker_relation_id'] for r in pos}),len(pos))
ck('positive_all_T06',all(r['rule_id']=='T06' for r in pos),'')
ck('positive_worker_authority_only',all(r['authority_class']=='WORKER_SOURCE_FIRST_RECOMMENDATION' and 'NOT_CENTRAL_FREEZE' in r['r16f_freeze_status'] for r in pos),'')
ck('positive_required_basis_nonblank',all(r['source_first_adjudication_basis'].strip() and r['source_provenance_json'].strip() and r['grain_note'].strip() for r in pos),'')

posids={r['worker_relation_id'] for r in pos}
for r in pos:
    impls=json.loads(r['member_implementation_ids_json']); roles=json.loads(r['role_assignments_json'])
    role_impls=[]; role_names=[]
    for x in roles:
        iid=x.get('question_implementation_id') or x.get('implementation_id')
        rr=x.get('relation_role_id') or x.get('relation_role')
        role_impls.append(iid); role_names.append(rr)
    ck('positive_bound_'+r['worker_relation_id'],bool(impls) and all(i in byid for i in impls),impls)
    ck('positive_same_wave_'+r['worker_relation_id'],all((byid[i]['source_family'],byid[i]['wave'])==(r['source_family'],r['wave']) for i in impls),r['source_family']+'::'+r['wave'])
    ck('positive_role_member_match_'+r['worker_relation_id'],set(role_impls)==set(impls),role_impls)
    ck('positive_role_vocab_'+r['worker_relation_id'],all(x in ALLOWED_ROLES for x in role_names),role_names)
    ck('positive_has_norm_'+r['worker_relation_id'],'RR_NORM' in role_names,role_names)
    ck('positive_has_conduct_'+r['worker_relation_id'],any(x in {'RR_STATED_OR_INTENDED_CONDUCT','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT'} for x in role_names),role_names)
    # Exact downstream grain: one normative shore plus one conceptual conduct shore. A source-native conduct question may
    # have more than one Rawlsing implementation only when the companion/verbatim grain is explicitly preserved.
    norm_n=sum(x=='RR_NORM' for x in role_names); conduct_n=sum(x in {'RR_STATED_OR_INTENDED_CONDUCT','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT'} for x in role_names)
    ck('positive_one_norm_shore_'+r['worker_relation_id'],norm_n==1,norm_n)
    if len(impls)>2:
        g=(r.get('grain_note','')+' '+r.get('source_first_adjudication_basis','')).lower()
        ck('positive_multi_impl_conduct_companion_'+r['worker_relation_id'],conduct_n==len(impls)-1 and any(k in g for k in ['companion','same source question','same source-native']),g[:240])
    ck('positive_sources_texts_align_'+r['worker_relation_id'],len(json.loads(r['member_source_variable_codes_json']))==len(impls)==len(json.loads(r['member_exact_source_texts_json'])),r['member_source_variable_codes_json'])

# Review ledger.
ck('crosswalk_allowed_states',all(r['disposition'] in ALLOWED_DISP for r in rev),Counter(r['disposition'] for r in rev))
ck('crosswalk_both_directions',all(r['norm_to_conduct_search_reviewed']=='YES' and r['conduct_to_norm_search_reviewed']=='YES' for r in rev),'')
ck('crosswalk_members_bound',all(r['norm_question_implementation_id'] in byid and r['conduct_question_implementation_id'] in byid for r in rev),'')
ck('positive_reviews_link_valid_relation',all(r['positive_relation_id'] in posids for r in rev if r['disposition']=='POSITIVE_T06'),'')
linked=Counter(r['positive_relation_id'] for r in rev if r['disposition']=='POSITIVE_T06')
ck('every_positive_has_positive_review',all(linked[r['worker_relation_id']]>=1 for r in pos),linked)
ck('mismatches_have_positive_source_proof',all(r['mismatch_or_block_dimension'].strip() and r['source_first_adjudication_basis'].strip() for r in rev if r['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH'),'')
ck('blocks_name_missing_or_ambiguous_dimension',all(r['mismatch_or_block_dimension'].strip() and r['source_first_adjudication_basis'].strip() for r in rev if r['disposition']=='BLOCKED_SOURCE_AMBIGUITY'),'')

# Blocker ledger exact correspondence.
blocked_reviews={r['crosswalk_review_id'] for r in rev if r['disposition']=='BLOCKED_SOURCE_AMBIGUITY'}
ck('blocker_ledger_exact',blocked_reviews=={r['crosswalk_review_id'] for r in blocks},(len(blocked_reviews),len(blocks)))

# Repairs/defects.
ck('repair_ids_unique',len(rep)==len({r['repair_id'] for r in rep}),len(rep))
ck('repairs_bound_to_selected_implementations',all(r['question_implementation_id'] in byid for r in rep),'')
ck('repair_source_state_nonblank',all(r['source_proven_state'].strip() and r['source_basis'].strip() for r in rep),'')
ck('coverage_defects_explicit_file',defects is not None,len(defects))

# Attestations.
ck('attestation_six_rows',len(att)==6,len(att))
attmap={(r['source_family'],r['wave']):r for r in att}
ck('attestation_wave_set',set(attmap)==set(EXPECTED),sorted(attmap))
for k,n in EXPECTED.items():
    a=attmap[k]
    aw=[r for r in acc if (r['source_family'],r['wave'])==k]
    rw=[r for r in rev if (r['source_family'],r['wave'])==k]
    pw=[r for r in pos if (r['source_family'],r['wave'])==k]
    ck('att_total_'+k[0]+'_'+k[1],int(a['total_implementations'])==n,a['total_implementations'])
    ck('att_norm_'+k[0]+'_'+k[1],int(a['norm_shore_count'])==sum(r['t06_reconstruction_classification']=='NORM_SHORE' for r in aw),a['norm_shore_count'])
    ck('att_conduct_'+k[0]+'_'+k[1],int(a['conduct_shore_count'])==sum(r['t06_reconstruction_classification']=='CONDUCT_SHORE' for r in aw),a['conduct_shore_count'])
    ck('att_positive_'+k[0]+'_'+k[1],int(a['positive_T06_count'])==len(pw),a['positive_T06_count'])
    b=sum(r['disposition']=='BLOCKED_SOURCE_AMBIGUITY' for r in rw)
    m=sum(r['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH' for r in rw)
    ck('att_block_'+k[0]+'_'+k[1],int(a['blocked_candidate_count'])==b,a['blocked_candidate_count'])
    ck('att_mismatch_'+k[0]+'_'+k[1],int(a['source_proven_mismatch_count'])==m,a['source_proven_mismatch_count'])
    zero=a['zero_T06_wave_currently_supportable']
    if not pw and b: ck('zero_not_claimed_with_block_'+k[0]+'_'+k[1],not zero.startswith('YES'),zero)
    if not pw and not b: ck('zero_supportable_when_closed_'+k[0]+'_'+k[1],zero.startswith('YES'),zero)

# Known structural controls from this source-first run.
ck('litsIII_source_parallel_positive_count',sum((r['source_family'],r['wave'])==('LiTS','III') for r in pos)==2,'')
ck('afroR9_positive_count',sum((r['source_family'],r['wave'])==('Afrobarometer','R9') for r in pos)==3,'')
ck('other_waves_no_positive',all((r['source_family'],r['wave']) in {('LiTS','III'),('Afrobarometer','R9')} for r in pos),'')
ck('q69_not_accepted',not any('Q69' in json.loads(r['member_source_variable_codes_json']) for r in pos),'')
ck('q69_repair_present',any(r['source_variable_code']=='Q69' and r['repair_type']=='RESPONSE_OPTION_ACTOR_GRAIN_NOT_MATERIALIZED' for r in rep),'')
ck('evs_zero_not_final',attmap[('EVS','1981')]['zero_T06_wave_currently_supportable'].startswith('NO'),attmap[('EVS','1981')]['zero_T06_wave_currently_supportable'])
ck('arab_zero_not_final',attmap[('Arab Barometer','I')]['zero_T06_wave_currently_supportable'].startswith('NO'),attmap[('Arab Barometer','I')]['zero_T06_wave_currently_supportable'])
# The 8.05 service reporting grid remains blocked against 8.17 norms because witness-condition identity is not source-proven.
svc={'q805a','q805b','q805c','q805d','q805e','q805f','q805g','q805h'}
ck('lits_service_grid_not_accepted',not any(set(json.loads(r['member_source_variable_codes_json'])) & svc for r in pos),'')
ck('lits_service_grid_blocks_16',sum(r['source_family']=='LiTS' and r['wave']=='III' and r['conduct_source_variable_code'].lower() in svc and r['disposition']=='BLOCKED_SOURCE_AMBIGUITY' for r in rev)==16,'')
ck('positive_total_5',len(pos)==5,len(pos))
ck('source_proven_repairs_exhaustive_nontrivial',len(rep)>=250,len(rep))

# Independent hostile-QA must already be PASS.
try:
    hqa=json.loads((RET/'HOSTILE_QA.json').read_text(encoding='utf-8'))
    ck('independent_hostile_qa_pass',hqa.get('status')=='PASS' and int(hqa.get('check_count',0))>=70,(hqa.get('status'),hqa.get('check_count')))
except Exception as e:
    ck('independent_hostile_qa_pass',False,repr(e))

# Governance / report.
report=(RET/'WORKER_REPORT.md').read_text(encoding='utf-8')
ck('report_no_freeze_claim','no S14 freeze is claimed' in report or 'no S14 freeze' in report,'')
ck('report_no_job3','No Job 3 was started' in report,'')
ck('report_source_first','source-first' in report.lower(),'')

status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL'
out={'worker_id':WORKER,'status':status,'validator':'CODE/validate_t06w02_return.py','checks':checks,
     'counts':{'assigned_implementations':len(acc),'positive_T06_relations':len(pos),'crosswalk_reviews':len(rev),
               'blocked_crosswalks':len(blocked_reviews),'source_proven_mismatches':sum(r['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH' for r in rev),
               'upstream_repairs':len(rep),'source_coverage_defects':len(defects)},
     'authority_sha256':got,'governance':'WORKER_RECOMMENDATION_ONLY__NO_S14_FREEZE__NO_JOB3'}
(RET/'VALIDATION.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'status':status,'counts':out['counts'],'failed':[c for c in checks if c['status']=='FAIL']},indent=2))
sys.exit(0 if status=='PASS' else 1)
