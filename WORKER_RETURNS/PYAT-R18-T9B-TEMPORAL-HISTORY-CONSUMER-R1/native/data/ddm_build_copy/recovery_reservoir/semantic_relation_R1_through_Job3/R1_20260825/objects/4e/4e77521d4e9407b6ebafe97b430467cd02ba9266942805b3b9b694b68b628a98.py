import csv,json,sys,hashlib,zipfile
from pathlib import Path
ROOT=Path('/mnt/data/Rawlsing_S14_T06W05_SourceFirst_Authority_Reconstruction_20260812/T06W05')
REQ=['T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv','T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv','T06_SOURCE_FIRST_CROSSWALK_REVIEW.csv','T06_SOURCE_FIRST_UPSTREAM_REPAIRS.csv','T06_SOURCE_COVERAGE_DEFECTS.csv','T06_SOURCE_FIRST_BLOCKERS.csv','T06_WAVE_COMPLETENESS_ATTESTATION.csv','WORKER_REPORT.md']
EXPECTED={('GSS','2016'):1018,('GSS','1993'):752,('EVS','1999'):513,('Latinobarómetro','2011'):414,('Asian Barometer','W4'):289}
def read(name):
  with open(ROOT/name,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
checks=[]
def chk(name,ok,detail=''):
  checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail}); return ok
chk('required_files_present',all((ROOT/x).exists() for x in REQ))
a=read('T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv'); p=read('T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv'); x=read('T06_SOURCE_FIRST_CROSSWALK_REVIEW.csv'); r=read('T06_SOURCE_FIRST_UPSTREAM_REPAIRS.csv'); d=read('T06_SOURCE_COVERAGE_DEFECTS.csv'); b=read('T06_SOURCE_FIRST_BLOCKERS.csv'); t=read('T06_WAVE_COMPLETENESS_ATTESTATION.csv')
chk('accounting_total_2986',len(a)==2986,str(len(a)))
chk('accounting_ids_unique',len({z['question_implementation_id'] for z in a})==len(a))
for k,n in EXPECTED.items(): chk('wave_count_'+k[0]+'_'+k[1],sum(z['source_family']==k[0] and z['wave']==k[1] for z in a)==n)
validcls={'NORM_SHORE','CONDUCT_SHORE','OTHER','SOURCE_AMBIGUOUS'}
chk('accounting_classes_valid',all(z['t06_accounting_class'] in validcls for z in a))
chk('all_implementations_accounted',all(z['implementation_accounted']=='YES' for z in a))
chk('norm_search_complete',all(z['norm_to_conduct_search_completed']=='YES' for z in a if z['t06_accounting_class']=='NORM_SHORE'))
chk('conduct_search_complete',all(z['conduct_to_norm_search_completed']=='YES' for z in a if z['t06_accounting_class']=='CONDUCT_SHORE'))
ids={z['question_implementation_id'] for z in a}
allowed_roles={'RR_NORM','RR_STATED_OR_INTENDED_CONDUCT','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT'}
allpos=True
for z in p:
  try:
    mids=json.loads(z['member_implementation_ids_json']); roles=json.loads(z['role_assignments_json'])
    ok=z['rule_id']=='T06' and z['relation_type']=='NORM_CONDUCT' and len(mids)==2 and all(q in ids for q in mids) and {q['relation_role'] for q in roles}.issubset(allowed_roles) and sum(q['relation_role']=='RR_NORM' for q in roles)==1 and sum(q['relation_role']!='RR_NORM' for q in roles)==1
  except Exception: ok=False
  allpos &= ok
chk('positive_schema_roles_binding',allpos)
chk('positive_count_18',len(p)==18,str(len(p)))
chk('positive_exact_source_text_present',all(len(json.loads(z['source_texts_json']))==2 and all(str(q).strip() for q in json.loads(z['source_texts_json'])) for z in p))
chk('positive_native_page_evidence_present',all(all('flattened_native_page_evidence' in side for side in json.loads(z['source_provenance_json']).values()) for z in p))
allowed_disp={'POSITIVE_T06','BLOCKED_SOURCE_AMBIGUITY','NOT_T06_SOURCE_PROVEN_MISMATCH'}
chk('crosswalk_dispositions_valid',all(z['disposition'] in allowed_disp for z in x))
chk('crosswalk_bidirectional_flags',all(z['norm_to_conduct_search_completed']=='YES' and z['conduct_to_norm_search_completed']=='YES' for z in x))
px={z['crosswalk_id'] for z in x if z['disposition']=='POSITIVE_T06'}
chk('all_positives_have_positive_crosswalk',all(z['crosswalk_id'] in px for z in p) and len(px)==len(p))
chk('mismatches_have_dimension',all(z['source_proven_mismatch_dimension'] for z in x if z['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH'))
blocked={z['crosswalk_id'] for z in x if z['disposition']=='BLOCKED_SOURCE_AMBIGUITY'}
chk('blocker_table_exact',blocked=={z['crosswalk_id'] for z in b},f'{len(blocked)} vs {len(b)}')
chk('coverage_defects_zero',len(d)==0,str(len(d)))
chk('upstream_repairs_count_22',len(r)==22,str(len(r)))
chk('repair_targets_bound',all(z['question_implementation_id'] in ids for z in r))
chk('attestation_five_waves',len(t)==5)
att_ok=True
for z in t:
  k=(z['source_family'],z['wave']); expected=EXPECTED.get(k)
  att_ok &= expected is not None and int(z['total_implementations'])==expected and z['completion_attestation']=='COMPLETE_SOURCE_FIRST' and z['norm_to_conduct_bidirectional_search_complete']=='YES' and z['conduct_to_norm_bidirectional_search_complete']=='YES'
  if int(z['positive_T06_count'])==0: att_ok &= z['zero_T06_currently_supportable']=='YES' and z['hostile_QA_sparse_or_zero_wave']=='PASS'
chk('attestations_complete_and_zero_QA',att_ok)
chk('no_freeze_claim',all(not z.get('r16f_freeze_status') and not z.get('r16f_freeze_basis') for z in p))
result='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL'
out={'worker':'T06W05','validation_result':result,'checks':checks,'statistics':{'assigned_total':len(a),'positive_relations':len(p),'crosswalk_rows':len(x),'blockers':len(b),'source_proven_mismatches':sum(z['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH' for z in x),'source_coverage_defects':len(d),'upstream_repairs':len(r),'accounting_by_wave':{f'{f}::{w}':sum(z['source_family']==f and z['wave']==w for z in a) for f,w in EXPECTED},'shore_counts_by_wave':{f'{f}::{w}':{'norm':sum(z['source_family']==f and z['wave']==w and z['t06_accounting_class']=='NORM_SHORE' for z in a),'conduct':sum(z['source_family']==f and z['wave']==w and z['t06_accounting_class']=='CONDUCT_SHORE' for z in a),'other':sum(z['source_family']==f and z['wave']==w and z['t06_accounting_class']=='OTHER' for z in a),'ambiguous':sum(z['source_family']==f and z['wave']==w and z['t06_accounting_class']=='SOURCE_AMBIGUOUS' for z in a)} for f,w in EXPECTED}}}
(ROOT/'VALIDATION.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
sys.exit(0 if result=='PASS' else 1)
