#!/usr/bin/env python3
import csv,json,gzip,hashlib,sys,re
from pathlib import Path
from collections import Counter,defaultdict
csv.field_size_limit(sys.maxsize)
ROOT=Path(__file__).resolve().parents[1]
RET=ROOT/'RETURN'
BASE=Path('/mnt/data/t06w02_source_first')
AUTH=BASE/'authority'/'Rawlsing_SourceNative_Questionnaire_Structure_Authority_R1_20260812'
SRCZIP=BASE/'Rawlsing_SourceNative_Questionnaire_Structure_Authority_R1_20260812.zip'
EXPECTED_SHA='e88cc035ca1d846e68ee208ec991f61f636d67ebbd19312057c8e44c37ff740d'
WAVES={('LiTS','III'):'LiTS__III',('LiTS','II'):'LiTS__II',('Afrobarometer','R9'):'Afrobarometer__R9',('EVS','1981'):'EVS__1981',('Latinobarómetro','1995'):'Latinobar_metro__1995',('Arab Barometer','I'):'Arab_Barometer__I'}
EXPECTED={('LiTS','III'):1290,('LiTS','II'):627,('Afrobarometer','R9'):421,('EVS','1981'):370,('Latinobarómetro','1995'):203,('Arab Barometer','I'):181}

def readcsv(n):
    with open(RET/n,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
acc=readcsv('T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv')
pos=readcsv('T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv')
rev=readcsv('T06_SOURCE_FIRST_CROSSWALK_REVIEW.csv')
rep=readcsv('T06_SOURCE_FIRST_UPSTREAM_REPAIRS.csv')
defects=readcsv('T06_SOURCE_COVERAGE_DEFECTS.csv')
blocks=readcsv('T06_SOURCE_FIRST_BLOCKERS.csv')
att=readcsv('T06_WAVE_COMPLETENESS_ATTESTATION.csv')
bycode={(r['source_family'],r['wave'],r['source_variable_code'].lower()):r for r in acc}
checks=[]
def ck(name,ok,detail=''):
    checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':str(detail)})
def A(f,w,c):return bycode[(f,w,c.lower())]
def has_review(f,w,n,c,disp=None,dim=None):
    xs=[r for r in rev if r['source_family']==f and r['wave']==w and r['norm_source_variable_code'].lower()==n.lower() and r['conduct_source_variable_code'].lower()==c.lower()]
    if disp is not None: xs=[r for r in xs if r['disposition']==disp]
    if dim is not None: xs=[r for r in xs if r['mismatch_or_block_dimension']==dim]
    return bool(xs)
# Native page corpus for exact phrase checks.
page_text={}
for fw,label in WAVES.items():
    alltext=[]
    with gzip.open(AUTH/'BY_WAVE'/label/'NATIVE_SOURCE_PAGE_TEXT.jsonl.gz','rt',encoding='utf-8') as f:
        for line in f:
            r=json.loads(line); alltext.append(r.get('page_text',''))
    page_text[fw]='\n'.join(alltext)

def src_has(f,w,*phrases):
    t=page_text[(f,w)].lower()
    return all(p.lower() in t for p in phrases)
# Source authority + denominator.
h=hashlib.sha256(SRCZIP.read_bytes()).hexdigest() if SRCZIP.exists() else 'MISSING'
ck('source_authority_sha',h==EXPECTED_SHA,h)
ck('denominator_3092',len(acc)==3092,len(acc))
counts=Counter((r['source_family'],r['wave']) for r in acc)
ck('wave_counts_exact',all(counts[k]==v for k,v in EXPECTED.items()),dict(counts))
ck('all_impl_unique',len({r['question_implementation_id'] for r in acc})==3092,'')
ck('all_substantive_accounted',all(r['t06_reconstruction_classification'] in {'NORM_SHORE','CONDUCT_SHORE','OTHER','SOURCE_AMBIGUOUS'} for r in acc),'')
ck('all_norm_forward',all(r['norm_to_conduct_search_completed']=='YES' for r in acc if r['t06_reconstruction_classification']=='NORM_SHORE'),'')
ck('all_conduct_reverse',all(r['conduct_to_norm_search_completed']=='YES' for r in acc if r['t06_reconstruction_classification']=='CONDUCT_SHORE'),'')
# R16F successor schema contract: first canonical columns preserved exactly.
with open(BASE/'schema_only'/'CENTRAL_POSITIVE_S14_RELATION_AUTHORITY_R16F.csv',encoding='utf-8-sig',newline='') as f:r16f=csv.reader(f); r16fh=next(r16f)
with open(RET/'T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv',encoding='utf-8-sig',newline='') as f:outh=next(csv.reader(f))
ck('r16f_schema_prefix_exact',outh[:len(r16fh)]==r16fh,(len(r16fh),len(outh)))
# Source anchors discovered directly.
ck('native_lits_817_phrases',src_has('LiTS','III','generally acceptable for people to report a case of corruption','personally obliged to report','spend a day in court to give evidence'),'')
ck('native_lits_805_household_phrase',all(x in page_text[('LiTS','III')].lower() for x in ['report any','household','unofficial payment','gift']),'')
ck('native_afro_q24',src_has('Afrobarometer','R9','we should choose our leaders in this country through regular, open and honest elections'),'')
ck('native_afro_q13',src_has('Afrobarometer','R9','in the last national election held in','did you vote'),'')
ck('native_afro_q96',src_has('Afrobarometer','R9','if [presidential elections] were held tomorrow'),'')
ck('native_afro_q28_q33b',src_has('Afrobarometer','R9','must always obey the laws and the courts','ignore the courts and laws'),'')
_evs_norm=re.sub(r'\s+',' ',page_text[('EVS','1981')].lower()); ck('native_evs_violence_disjunction','fighting with other demonstrators or the police' in _evs_norm and 'fighting with the police' in _evs_norm,'')
_arab_norm=re.sub(r'\s+',' ',page_text[('Arab Barometer','I')].lower()); ck('native_arab_work_condition','a married woman can work outside the home' in _arab_norm and 'if she wishes' in _arab_norm and 'employment status' in _arab_norm,'')
# Key shore classifications after hostile recall audit.
expected_class=[
 ('LiTS','III','q817a','NORM_SHORE'),('LiTS','III','q817b','NORM_SHORE'),('LiTS','III','q817c','CONDUCT_SHORE'),
 ('LiTS','III','q406a','NORM_SHORE'),('LiTS','III','q406b','NORM_SHORE'),('LiTS','III','q605','CONDUCT_SHORE'),('LiTS','III','q917','CONDUCT_SHORE'),
 ('Afrobarometer','R9','Q24','NORM_SHORE'),('Afrobarometer','R9','Q96','CONDUCT_SHORE'),('Afrobarometer','R9','Q96OTHER','CONDUCT_SHORE'),
 ('Afrobarometer','R9','Q44C','CONDUCT_SHORE'),('Afrobarometer','R9','Q44D','CONDUCT_SHORE'),('Afrobarometer','R9','Q53A','CONDUCT_SHORE'),
 ('Latinobarómetro','1995','p19','NORM_SHORE'),('Arab Barometer','I','q5021','NORM_SHORE'),('Arab Barometer','I','q5026','NORM_SHORE')]
for f,w,c,cl in expected_class: ck('shore_'+f+'_'+w+'_'+c,A(f,w,c)['t06_reconstruction_classification']==cl,A(f,w,c)['t06_reconstruction_classification'])
# Exact positive set and binding.
pos_codes=[tuple(json.loads(r['member_source_variable_codes_json'])) for r in pos]
expected_pos={('q817a','q817c'),('q817b','q817c'),('Q24','Q13'),('Q24','Q96','Q96OTHER'),('Q28','Q33B')}
ck('positive_set_exact_5',set(pos_codes)==expected_pos,pos_codes)
ck('positive_all_impl_bound',all(all(i in {a['question_implementation_id'] for a in acc} for i in json.loads(r['member_implementation_ids_json'])) for r in pos),'')
ck('positive_roles_exact',all({x['relation_role_id'] for x in json.loads(r['role_assignments_json'])}<={'RR_NORM','RR_STATED_OR_INTENDED_CONDUCT','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT'} for r in pos),'')
ck('positive_native_provenance',all(all(x.get('authority')=='native questionnaire/codebook text' for x in json.loads(r['source_provenance_json'])) for r in pos),'')
ck('positive_q96_companion_grain',any(tuple(json.loads(r['member_source_variable_codes_json']))==('Q24','Q96','Q96OTHER') and any(k in (r['grain_note']+' '+r['source_first_adjudication_basis']).lower() for k in ['companion','same source-native','same source question']) for r in pos),'')
# Critical blocks: proof failure stays block, not negative/positive.
for n in ['q817a','q817b']:
    for c in ['q805a','q805b','q805c','q805d','q805e','q805f','q805g','q805h']:
        ck('lits805_block_'+n+'_'+c,has_review('LiTS','III',n,c,'BLOCKED_SOURCE_AMBIGUITY','CONDITION_AND_ACTOR_UNIVERSE_GRAIN'),'')
ck('lits_cohab_composite_block',has_review('LiTS','III','q426g','q107_1','BLOCKED_SOURCE_AMBIGUITY','COMPOSITE_RESPONDENT_STATE_GRAIN'),'')
ck('lits_daughter_university_actor_block',has_review('LiTS','III','q426d','q926f_2','BLOCKED_SOURCE_AMBIGUITY','ACTOR_GRAIN'),'')
ck('lits_son_university_actor_block',has_review('LiTS','III','q426e','q926f_2','BLOCKED_SOURCE_AMBIGUITY','ACTOR_GRAIN'),'')
ck('evs_police_disjunction_block',has_review('EVS','1981','v512','v456','BLOCKED_SOURCE_AMBIGUITY'),'')
ck('arab_married_woman_work_block',has_review('Arab Barometer','I','q5052','q704','BLOCKED_SOURCE_AMBIGUITY'),'')
ck('afro_climate_modality_block',has_review('Afrobarometer','R9','Q68B','Q70C','BLOCKED_SOURCE_AMBIGUITY'),'')
ck('afro_environment_modality_block',has_review('Afrobarometer','R9','Q72E','Q46Q','BLOCKED_SOURCE_AMBIGUITY'),'')
# Q69 option-conditioned actor grain must not be fabricated.
ck('q69_no_positive',not any('Q69' in json.loads(r['member_source_variable_codes_json']) for r in pos),'')
ck('q69_four_actor_blocks',sum(r['source_family']=='Afrobarometer' and r['wave']=='R9' and r['norm_source_variable_code']=='Q69' and r['disposition']=='BLOCKED_SOURCE_AMBIGUITY' for r in rev)==4,'')
ck('q69_upstream_grain_repair',any(r['source_family']=='Afrobarometer' and r['wave']=='R9' and r['source_variable_code']=='Q69' and r['repair_type']=='RESPONSE_OPTION_ACTOR_GRAIN_NOT_MATERIALIZED' for r in rep),'')
# Negative rows require positive mismatch basis, never missing-evidence language alone.
ck('negative_rows_named_mismatch',all(r['mismatch_or_block_dimension'].strip() and r['source_first_adjudication_basis'].strip() for r in rev if r['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH'),'')
ck('blocker_ledger_exact',{r['crosswalk_review_id'] for r in rev if r['disposition']=='BLOCKED_SOURCE_AMBIGUITY'}=={r['crosswalk_review_id'] for r in blocks},'')
# Zero-wave hostile QA.
am={(r['source_family'],r['wave']):r for r in att}
ck('litsII_zero_supportable',am[('LiTS','II')]['zero_T06_wave_currently_supportable'].startswith('YES'),am[('LiTS','II')]['zero_T06_wave_currently_supportable'])
ck('latin_zero_supportable',am[('Latinobarómetro','1995')]['zero_T06_wave_currently_supportable'].startswith('YES'),am[('Latinobarómetro','1995')]['zero_T06_wave_currently_supportable'])
ck('evs_zero_not_supportable',am[('EVS','1981')]['zero_T06_wave_currently_supportable'].startswith('NO'),am[('EVS','1981')]['zero_T06_wave_currently_supportable'])
ck('arab_zero_not_supportable',am[('Arab Barometer','I')]['zero_T06_wave_currently_supportable'].startswith('NO'),am[('Arab Barometer','I')]['zero_T06_wave_currently_supportable'])
# Exhaustive upstream-repair law: every source-clear shore lacking a current semantic/O04 role representation must be in repairs.
# This is checked from final accounting plus current catalog / implementation spine, not from predecessor T06 candidates.
rep_iids={r['question_implementation_id'] for r in rep}
semcat={}
with open(BASE/'raw_spine'/'ALL_R16D_AUTHORITY_SEMANTIC_UNIT_CATALOG.csv',encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):semcat[r['semantic_unit_id']]=r
missing=[]
for r in acc:
    cls=r['t06_reconstruction_classification']
    if cls not in {'NORM_SHORE','CONDUCT_SHORE'}:continue
    sis=json.loads(r['semantic_unit_ids_json']); canon=set()
    for sid in sis:
        try: canon.update(json.loads(semcat[sid].get('sem_canonical_roles_json') or '[]'))
        except: pass
    try:o04=json.loads(r['current_o04_endpoint_metadata_for_binding_only'])
    except:o04={}
    represented=(('NORMATIVE_OR_POLICY_STANCE' in canon) if cls=='NORM_SHORE' else (bool(o04.get('status') or o04.get('endpoint_class')) or 'INTENTION_OR_EXPECTATION' in canon))
    if not represented and r['question_implementation_id'] not in rep_iids:missing.append((r['source_family'],r['wave'],r['source_variable_code'],cls))
ck('upstream_repair_anti_failure_exhaustive',not missing,missing[:20])
ck('repairs_unique',len(rep_iids)==len(rep),len(rep))
ck('repairs_all_bound',all(r['question_implementation_id'] in {a['question_implementation_id'] for a in acc} for r in rep),'')
ck('repair_count_289',len(rep)==289,len(rep))
ck('coverage_defects_zero',len(defects)==0,len(defects))
# No predecessor candidate universe appears as an input dependency in executable worker code.
code='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in (ROOT/'CODE').glob('*.py'))
# References in comments/output-law are okay; fail only on opening/reading candidate/verdict artifacts.
ck('no_predecessor_candidate_file_dependency',not re.search(r"(?:open|readcsv|read_csv|gzip\.open)\([^\n]*(R15|C4|CANDIDATE|VERDICT)",code,re.I),'')
# Governance.
report=(RET/'WORKER_REPORT.md').read_text(encoding='utf-8')
ck('no_job3','No Job 3 was started' in report,'')
ck('no_freeze_claim','no S14 freeze is claimed' in report or 'no S14 freeze' in report,'')
status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL'
out={'worker_id':'T06W02','status':status,'hostile_qa':'CODE/hostile_qa_t06w02.py','check_count':len(checks),'checks':checks,
     'counts':{'assigned_implementations':len(acc),'positive_T06_relations':len(pos),'crosswalk_reviews':len(rev),'blocked_crosswalks':sum(r['disposition']=='BLOCKED_SOURCE_AMBIGUITY' for r in rev),'source_proven_mismatches':sum(r['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH' for r in rev),'upstream_repairs':len(rep),'source_coverage_defects':len(defects)},
     'authority_sha256':h,'governance':'WORKER_RECOMMENDATION_ONLY__NO_S14_FREEZE__NO_JOB3'}
(RET/'HOSTILE_QA.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':status,'check_count':len(checks),'failed':[c for c in checks if c['status']=='FAIL'],'counts':out['counts']},ensure_ascii=False,indent=2))
sys.exit(0 if status=='PASS' else 1)
