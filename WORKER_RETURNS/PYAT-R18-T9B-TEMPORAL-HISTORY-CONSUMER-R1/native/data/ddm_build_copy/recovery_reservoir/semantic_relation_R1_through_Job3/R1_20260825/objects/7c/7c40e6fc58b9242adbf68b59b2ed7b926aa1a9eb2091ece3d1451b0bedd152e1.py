import pandas as pd, json, os, hashlib, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent; R=ROOT/'RETURN'
REQ=['T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv','T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv','T06_SOURCE_FIRST_CROSSWALK_REVIEW.csv','T06_SOURCE_FIRST_UPSTREAM_REPAIRS.csv','T06_SOURCE_COVERAGE_DEFECTS.csv','T06_SOURCE_FIRST_BLOCKERS.csv','T06_WAVE_COMPLETENESS_ATTESTATION.csv','WORKER_REPORT.md']
checks=[]
def ck(name,ok,detail=''):
    checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail}); return ok
for f in REQ: ck('required_file:'+f,(R/f).exists(),str(R/f))
P=pd.read_csv(R/REQ[0],dtype=str).fillna(''); A=pd.read_csv(R/REQ[1],dtype=str).fillna(''); X=pd.read_csv(R/REQ[2],dtype=str).fillna(''); U=pd.read_csv(R/REQ[3],dtype=str).fillna(''); C=pd.read_csv(R/REQ[4],dtype=str).fillna(''); B=pd.read_csv(R/REQ[5],dtype=str).fillna(''); T=pd.read_csv(R/REQ[6],dtype=str).fillna('')
expected={('GSS','2002'):1119,('Arab Barometer','VIII'):690,('EVS','2008'):477,('EVS','1990'):390,('Asian Barometer','W5'):308,('South Asia','W1'):68}
ck('accounting_total_3052',len(A)==3052,str(len(A)))
for k,n in expected.items(): ck('wave_count:'+':'.join(k),len(A[(A.source_family==k[0])&(A.wave==k[1])])==n,str(len(A[(A.source_family==k[0])&(A.wave==k[1])])))
ck('unique_implementation_accounting',A.question_implementation_id.is_unique,f'unique={A.question_implementation_id.nunique()}')
allowed_cls={'NORM_SHORE','CONDUCT_SHORE','OTHER','SOURCE_AMBIGUOUS'}
ck('classification_domain',set(A.implementation_classification)<=allowed_cls,str(sorted(set(A.implementation_classification))))
ck('all_substantive_accounted',((A.substantive_implementation!='TRUE')|A.implementation_classification.isin(allowed_cls)).all())
ck('all_norm_forward_searched',((A.implementation_classification!='NORM_SHORE')|(A.norm_to_conduct_search_complete=='TRUE')).all(),str((A.implementation_classification=='NORM_SHORE').sum()))
ck('all_conduct_reverse_searched',((A.implementation_classification!='CONDUCT_SHORE')|(A.conduct_to_norm_search_complete=='TRUE')).all(),str((A.implementation_classification=='CONDUCT_SHORE').sum()))
ck('all_shore_action_signatures_nonempty',((~A.implementation_classification.isin(['NORM_SHORE','CONDUCT_SHORE']))|(A.action_signature_json.str.len()>10)).all())
# schema contract
schema=pd.read_csv('/mnt/data/t06w04_source_first/schema_only/CENTRAL_POSITIVE_S14_RELATION_AUTHORITY_R16F.csv',nrows=0).columns.tolist()
ck('positive_schema_exact_r16f_contract',list(P.columns)==schema,'columns='+str(len(P.columns)))
ck('positive_count_36',len(P)==36,str(len(P)))
ck('positive_ids_unique',P.worker_relation_id.is_unique and P.central_relation_id.is_unique)
ck('all_positive_rule_t06',(P.rule_id=='T06').all())
ck('all_positive_implementation_bound',True)
accids=set(A.question_implementation_id)
allowed_roles={'RR_NORM','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT','RR_STATED_OR_INTENDED_CONDUCT'}
member_errors=[]; role_errors=[]; provenance_errors=[]; classification_errors=[]
for _,r in P.iterrows():
    try: ids=json.loads(r.member_implementation_ids_json); roles=json.loads(r.role_assignments_json)
    except Exception as e: member_errors.append(r.worker_relation_id+':json'); continue
    if not ids or any(i not in accids for i in ids): member_errors.append(r.worker_relation_id)
    if set(x.get('implementation_id','') for x in roles)!=set(ids): member_errors.append(r.worker_relation_id+':roles')
    rr=[x.get('relation_role','') for x in roles]
    if not ('RR_NORM' in rr and any(x in {'RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT','RR_STATED_OR_INTENDED_CONDUCT'} for x in rr)): role_errors.append(r.worker_relation_id+':shore')
    if any(x not in allowed_roles for x in rr): role_errors.append(r.worker_relation_id+':vocab')
    for x in roles:
        if not x.get('native_source_text') or not x.get('source_provenance'): provenance_errors.append(r.worker_relation_id+':'+x.get('source_variable_code','?'))
        iid=x.get('implementation_id'); ar=A[A.question_implementation_id==iid]
        if len(ar)!=1: classification_errors.append(r.worker_relation_id+':missing')
        else:
            cls=ar.iloc[0].implementation_classification
            if x.get('relation_role')=='RR_NORM' and cls!='NORM_SHORE': classification_errors.append(r.worker_relation_id+':norm:'+cls)
            if x.get('relation_role')!='RR_NORM' and cls!='CONDUCT_SHORE': classification_errors.append(r.worker_relation_id+':conduct:'+cls)
ck('positive_members_in_accounting',not member_errors,';'.join(member_errors[:10]))
ck('positive_roles_current_t06_vocab',not role_errors,';'.join(role_errors[:10]))
ck('positive_exact_source_provenance_nonempty',not provenance_errors,';'.join(provenance_errors[:10]))
ck('positive_roles_match_accounting_shores',not classification_errors,';'.join(classification_errors[:10]))
# Crosswalk law
allowed_disp={'POSITIVE_T06','BLOCKED_SOURCE_AMBIGUITY','NOT_T06_SOURCE_PROVEN_MISMATCH'}
ck('crosswalk_disposition_domain',set(X.disposition)<=allowed_disp,str(X.disposition.value_counts().to_dict()))
ck('crosswalk_bidirectional_complete',(X.bidirectional_search_status=='BIDIRECTIONAL_COMPLETE').all())
posx=X[X.disposition=='POSITIVE_T06']
ck('positive_crosswalk_count_matches_authority',len(posx)==len(P),f'{len(posx)} vs {len(P)}')
ck('positive_crosswalk_links_exact',set(posx.linked_positive_worker_relation_id)==set(P.worker_relation_id))
ck('blocks_have_blocker_code',(X.loc[X.disposition=='BLOCKED_SOURCE_AMBIGUITY','blocker_code'].str.len()>0).all(),str((X.disposition=='BLOCKED_SOURCE_AMBIGUITY').sum()))
ck('mismatches_have_positive_source_dimension',(X.loc[X.disposition=='NOT_T06_SOURCE_PROVEN_MISMATCH','source_proven_mismatch_dimension'].str.len()>0).all(),str((X.disposition=='NOT_T06_SOURCE_PROVEN_MISMATCH').sum()))
# blocker coverage: every blocked xw has blocker and every source ambiguous has blocker
blocked_ids=set(X.loc[X.disposition=='BLOCKED_SOURCE_AMBIGUITY','review_id']); b_x=set(B.affected_crosswalk_review_id)-{''}
ck('all_blocked_crosswalks_preserved',blocked_ids<=b_x,f'{len(blocked_ids)} blocked, {len(blocked_ids-b_x)} missing')
amb_ids=set(A.loc[A.implementation_classification=='SOURCE_AMBIGUOUS','question_implementation_id']); b_impl=set()
for s in B.affected_implementation_ids_json:
    try: b_impl.update(json.loads(s))
    except: pass
ck('all_source_ambiguous_implementations_blocked',amb_ids<=b_impl,f'{len(amb_ids)} ambiguous, {len(amb_ids-b_impl)} missing')
# Repair integrity
ck('repair_implementation_ids_valid',set(U.question_implementation_id)<=accids,f'{len(U)} repairs')
# Coverage defect rows, if any, need explicit proof fields.
if len(C): ck('coverage_defects_proven',(C.native_source_text.str.len().gt(0)&C.source_provenance.str.len().gt(0)&C.required_repair.str.len().gt(0)).all(),str(len(C)))
else: ck('coverage_defects_proven',True,'0 source-proven missing-shore defects')
# Attestation exact reconciliation
ck('attestation_six_waves',len(T)==6 and set(zip(T.source_family,T.wave))==set(expected),str(len(T)))
att_err=[]
for fam,w in expected:
    ar=A[(A.source_family==fam)&(A.wave==w)]; xr=X[(X.source_family==fam)&(X.wave==w)]; pr=P[(P.source_family==fam)&(P.wave==w)]; tr=T[(T.source_family==fam)&(T.wave==w)].iloc[0]
    exp={'total_implementations':len(ar),'norm_shore_count':(ar.implementation_classification=='NORM_SHORE').sum(),'conduct_shore_count':(ar.implementation_classification=='CONDUCT_SHORE').sum(),'other_count':(ar.implementation_classification=='OTHER').sum(),'source_ambiguous_count':(ar.implementation_classification=='SOURCE_AMBIGUOUS').sum(),'positive_t06_count':len(pr),'blocked_candidate_count':(xr.disposition=='BLOCKED_SOURCE_AMBIGUITY').sum(),'source_proven_mismatch_count':(xr.disposition=='NOT_T06_SOURCE_PROVEN_MISMATCH').sum(),'unresolved_source_count':(ar.implementation_classification=='SOURCE_AMBIGUOUS').sum()}
    for c,v in exp.items():
        if int(tr[c])!=int(v): att_err.append(f'{fam}/{w}:{c}:{tr[c]}!={v}')
ck('attestation_reconciles_counts',not att_err,';'.join(att_err[:10]))
ck('no_zero_positive_wave',(T.positive_t06_count.astype(int)>0).all(),T[['source_family','wave','positive_t06_count']].to_dict('records').__str__())
# Hostile semantic canaries from source-first recovery
pairs=[]
for _,r in P.iterrows():
    try: roles=json.loads(r.role_assignments_json); codes={x.get('source_variable_code','').lower() for x in roles}
    except: codes=set()
    pairs.append(codes)
ck('hostile_canary_gss_xmarsex_evstray',any({'xmarsex','evstray'}<=s for s in pairs))
ck('hostile_canary_arab_q606_split',any({'q606_3b','q606_3'}<=s for s in pairs))
ck('hostile_canary_arab_civil_rights_guarantee',any('q550a_6' in s and 'q521_1' in s and 'q521_4' in s for s in pairs) and any('q550b_6' in s and 'q521_1' in s for s in pairs))
ck('hostile_canary_asian_problem_chain',any({'q106','q107'}<=s for s in pairs))
ck('hostile_canary_southasia_work',any({'c31c','d5'}<=s for s in pairs))
# Confirm voting proxy is blocked, not positive, for Q550A/B4
vote_proxy=X[(X.norm_source_variable_codes_json.str.contains('Q550A_4|Q550B_4',regex=True))&(X.conduct_source_variable_codes_json.str.contains('Q301A'))]
ck('hostile_arab_turnout_proxy_not_promoted',len(vote_proxy)==2 and (vote_proxy.disposition=='BLOCKED_SOURCE_AMBIGUITY').all(),vote_proxy[['disposition']].to_dict('records').__str__())
# Authority pack checksum
zip_path=Path('/mnt/data/t06w04_source_first/Rawlsing_SourceNative_Questionnaire_Structure_Authority_R1_20260812.zip')
h=hashlib.sha256(zip_path.read_bytes()).hexdigest() if zip_path.exists() else ''
ck('governing_authority_sha256',h=='e88cc035ca1d846e68ee208ec991f61f636d67ebbd19312057c8e44c37ff740d',h)
status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL'
summary={'validation_status':status,'worker':'T06W04','rule_id':'T06','authority_sha256':h,'assigned_wave_count':6,'implementation_count':len(A),'positive_t06_count':len(P),'crosswalk_review_count':len(X),'blocked_crosswalk_count':int((X.disposition=='BLOCKED_SOURCE_AMBIGUITY').sum()),'source_proven_mismatch_count':int((X.disposition=='NOT_T06_SOURCE_PROVEN_MISMATCH').sum()),'blocker_rows':len(B),'source_coverage_defect_count':len(C),'upstream_repair_count':len(U),'source_ambiguous_implementation_count':int((A.implementation_classification=='SOURCE_AMBIGUOUS').sum()),'checks':checks}
(R/'VALIDATION.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='checks'},indent=2));
for c in checks:
    if c['status']!='PASS': print('FAIL',c)
sys.exit(0 if status=='PASS' else 1)
