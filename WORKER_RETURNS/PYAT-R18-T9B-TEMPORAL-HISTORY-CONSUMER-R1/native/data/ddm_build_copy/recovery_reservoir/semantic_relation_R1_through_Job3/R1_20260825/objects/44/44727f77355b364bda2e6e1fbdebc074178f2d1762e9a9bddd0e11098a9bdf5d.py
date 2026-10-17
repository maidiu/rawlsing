#!/usr/bin/env python3
import csv,json,sys,pathlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]; R=ROOT/'RETURN'
def rd(name):
 with open(R/name,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
errors=[]; checks=[]
def ck(name,cond,detail):
 checks.append({'check':name,'pass':bool(cond),'detail':detail})
 if not cond: errors.append(f'{name}: {detail}')
acct=rd('T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv'); pos=rd('T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv'); rev=rd('T06_SOURCE_FIRST_CROSSWALK_REVIEW.csv'); rep=rd('T06_SOURCE_FIRST_UPSTREAM_REPAIRS.csv'); de=rd('T06_SOURCE_COVERAGE_DEFECTS.csv'); blk=rd('T06_SOURCE_FIRST_BLOCKERS.csv'); comp=rd('T06_WAVE_COMPLETENESS_ATTESTATION.csv')
expected={('GSS','2024'):980,('GSS','2010'):922,('Arab Barometer','II'):468,('GSS','1973'):339,('Latinobarómetro','2024'):195,('WVS','W1'):188}
ck('total_accounting_3092',len(acct)==3092,f'got={len(acct)} expected=3092')
ids=[x['question_implementation_id'] for x in acct]; ck('unique_accounting_ids',len(ids)==len(set(ids)),f'{len(ids)} rows/{len(set(ids))} unique')
by=collections.Counter((x['source_family'],x['wave']) for x in acct)
for k,n in expected.items(): ck('wave_count:'+str(k),by[k]==n,f'got={by[k]} expected={n}')
allowed_cls={'NORM_SHORE','CONDUCT_SHORE','OTHER','SOURCE_AMBIGUOUS'}
ck('allowed_accounting_classes',all(x['t06_reconstruction_class'] in allowed_cls for x in acct),'all rows classified')
ck('norm_forward_search',all(x['norm_to_conduct_search_completed']=='YES' for x in acct if x['t06_reconstruction_class']=='NORM_SHORE'),'all norm shores searched')
ck('conduct_reverse_search',all(x['conduct_to_norm_search_completed']=='YES' for x in acct if x['t06_reconstruction_class']=='CONDUCT_SHORE'),'all conduct shores reverse-searched')
allowed_disp={'POSITIVE_T06','BLOCKED_SOURCE_AMBIGUITY','NOT_T06_SOURCE_PROVEN_MISMATCH'}
ck('allowed_review_dispositions',all(x['disposition'] in allowed_disp for x in rev),'review ledger dispositions valid')
implset=set(ids); relids={x['worker_relation_id'] for x in pos}; blockids={x['blocker_id'] for x in blk}
ck('positive_count_9',len(pos)==9,f'got={len(pos)} expected=9')
ck('positive_rule',all(x['rule_id']=='T06' for x in pos),'all T06')
ck('no_freeze_claim',all(x['r16f_freeze_status']=='NOT_FROZEN_WORKER_SOURCE_FIRST' for x in pos),'worker positives explicitly not frozen')
roles={'RR_NORM','RR_STATED_OR_INTENDED_CONDUCT','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT'}
for x in pos:
 try:
  mids=json.loads(x['member_implementation_ids_json']); ras=json.loads(x['role_assignments_json'])
 except Exception as e:
  errors.append('json parse '+x.get('worker_relation_id','')+': '+repr(e)); continue
 ck('members_bound:'+x['worker_relation_id'],all(i in implset for i in mids),str(mids))
 ck('roles_exact:'+x['worker_relation_id'],all(a.get('relation_role') in roles for a in ras),str([a.get('relation_role') for a in ras]))
 ck('has_norm_and_conduct:'+x['worker_relation_id'],any(a.get('relation_role')=='RR_NORM' for a in ras) and any(a.get('relation_role') in {'RR_STATED_OR_INTENDED_CONDUCT','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT'} for a in ras),'role shores present')
for x in rev:
 if x['disposition']=='POSITIVE_T06': ck('review_positive_relation:'+x['review_id'],x['positive_relation_id'] in relids,x['positive_relation_id'])
 if x['disposition']=='BLOCKED_SOURCE_AMBIGUITY': ck('review_blocker:'+x['review_id'],x['blocker_id'] in blockids,x['blocker_id'])
ck('upstream_repair_count_2',len(rep)==2,f'got={len(rep)} expected=2')
ck('coverage_defects_zero',len(de)==0,f'got={len(de)}')
ck('completeness_six_rows',len(comp)==6,f'got={len(comp)}')
compkeys={(x['source_family'],x['wave']) for x in comp}; ck('completeness_wave_keys',compkeys==set(expected),str(compkeys))
for x in comp:
 k=(x['source_family'],x['wave']); ar=[a for a in acct if (a['source_family'],a['wave'])==k]; rr=[a for a in rev if (a['source_family'],a['wave'])==k]; pp=[a for a in pos if (a['source_family'],a['wave'])==k]
 ck('attest_total:'+str(k),int(x['total_implementations_accounted'])==len(ar),f'{x["total_implementations_accounted"]}/{len(ar)}')
 ck('attest_positive:'+str(k),int(x['positive_t06_count'])==len(pp),f'{x["positive_t06_count"]}/{len(pp)}')
 ck('attest_blocked:'+str(k),int(x['blocked_candidate_count'])==sum(a['disposition']=='BLOCKED_SOURCE_AMBIGUITY' for a in rr),x['blocked_candidate_count'])
 ck('attest_mismatch:'+str(k),int(x['source_proven_mismatch_count'])==sum(a['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH' for a in rr),x['source_proven_mismatch_count'])
 if x['zero_t06_currently_supportable']=='YES': ck('zero_gate:'+str(k),len(pp)==0 and int(x['blocked_candidate_count'])==0 and int(x['unresolved_source_count'])==0,'zero requires no positives/blocks/unresolved')
# Ensure source-first basis is not contaminated by old candidate verdict language.
contam=('r15atom','worker_recommend_reject','c4 verdict','old candidate pair')
texts=' '.join((x.get('central_basis','')+' '+x.get('source_first_adjudication_basis','')) for x in pos+rev).lower()
ck('recall_firewall',not any(t in texts for t in contam),'no inherited candidate/verdict tokens in adjudication basis')
status='PASS' if not errors else 'FAIL'
out={'worker_id':'T06W06','validation_status':status,'error_count':len(errors),'errors':errors,'checks':checks,'counts':{'accounting_rows':len(acct),'crosswalk_rows':len(rev),'positive_relations':len(pos),'blockers':len(blk),'upstream_repairs':len(rep),'source_coverage_defects':len(de)}}
(R/'VALIDATION.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'worker_id':'T06W06','validation_status':status,'error_count':len(errors),'counts':out['counts']},indent=2))
sys.exit(0 if status=='PASS' else 1)
