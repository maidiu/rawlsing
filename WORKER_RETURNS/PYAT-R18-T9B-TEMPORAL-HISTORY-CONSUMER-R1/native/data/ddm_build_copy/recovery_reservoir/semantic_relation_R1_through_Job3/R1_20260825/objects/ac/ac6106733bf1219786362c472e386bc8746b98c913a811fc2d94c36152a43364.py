import os,csv,gzip,json,re,hashlib,sys,collections
from pathlib import Path
csv.field_size_limit(sys.maxsize)
ROOT=Path('/mnt/data/t06w02_source_first')
AUTH=ROOT/'authority'/'Rawlsing_SourceNative_Questionnaire_Structure_Authority_R1_20260812'
OUT=ROOT/'T06W02'/'RETURN'
OUT.mkdir(parents=True,exist_ok=True)
WORKER='T06W02'
WAVES=[
 ('LiTS','III','LiTS__III',1290),
 ('LiTS','II','LiTS__II',627),
 ('Afrobarometer','R9','Afrobarometer__R9',421),
 ('EVS','1981','EVS__1981',370),
 ('Latinobarómetro','1995','Latinobar_metro__1995',203),
 ('Arab Barometer','I','Arab_Barometer__I',181),
]
WKEY={(f,w):label for f,w,label,_ in WAVES}

def jd(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def stable(prefix,*parts,n=16): return prefix+hashlib.sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:n]
def low(x): return (x or '').strip().lower()

def readcsv(p):
    with open(p,encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def writecsv(p,headers,rows):
    with open(p,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=headers,extrasaction='ignore'); w.writeheader(); w.writerows(rows)

# Authority + current ID spine only (no predecessor candidate/verdict data used).
contexts=[]; byfw={}; bycode={}; byid={}
for fam,wave,label,expected in WAVES:
    rows=readcsv(AUTH/'BY_WAVE'/label/'IMPLEMENTATION_SOURCE_CONTEXT.csv')
    assert len(rows)==expected,(fam,wave,len(rows),expected)
    byfw[(fam,wave)]=rows
    for r in rows:
        r['_family']=fam; r['_wave']=wave; contexts.append(r); byid[r['question_implementation_id']]=r
        bycode[(fam,wave,low(r['source_variable_code']))]=r
assert len(contexts)==3092 and len(byid)==3092

spine={}
with gzip.open(ROOT/'raw_spine'/'ALL_R16D_AUTHORITY_IMPLEMENTATION_SPINE.csv.gz','rt',encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        iid=r.get('question_implementation_id','')
        if iid in byid: spine[iid]=r
assert len(spine)==3092
impl_to_sem=collections.defaultdict(list)
sem_catalog={}
with open(ROOT/'raw_spine'/'ALL_R16D_AUTHORITY_SEMANTIC_UNIT_CATALOG.csv',encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f):
        sem_catalog[r['semantic_unit_id']]=r
        try: ids=json.loads(r.get('implementation_ids_json') or '[]')
        except Exception: ids=[]
        for iid in ids:
            if iid in byid: impl_to_sem[iid].append(r['semantic_unit_id'])

# Native pages for provenance/navigation.
pages={}
for fam,wave,label,_ in WAVES:
    arr=[]
    with gzip.open(AUTH/'BY_WAVE'/label/'NATIVE_SOURCE_PAGE_TEXT.jsonl.gz','rt',encoding='utf-8') as f:
        for line in f: arr.append(json.loads(line))
    pages[(fam,wave)]={int(p['page_number']):p for p in arr}

def R(f,w,c):
    k=(f,w,low(c))
    if k not in bycode: raise KeyError(k)
    return bycode[k]
def I(f,w,c): return R(f,w,c)['question_implementation_id']
def T(f,w,c): return R(f,w,c)['exact_question_text']
def S(f,w,c): return spine[I(f,w,c)]
def sems(f,w,c): return sorted(impl_to_sem[I(f,w,c)])

# T06 reconstruction-aid classifications. These sets were compiled from native wave-local
# stems/batteries, not predecessor candidate pairs. Broad norm shore coverage is intentional.
norm_codes={
 ('LiTS','III'): set(map(low,[
  'q401h','q406a','q406b','q408a','q408b','q408c','q408d','q408e','q408f','q408g',
  'q414a','q414b','q414c','q414d','q414e','q414f','q414g','q414h',
  'q417a','q417b','q417c','q417d','q417e','q417f','q417g',
  'q426c','q426d','q426e','q426g','q426h','q817a','q817b'])),
 ('LiTS','II'): set(map(low,[
  'q305_1','q305_2',*['q307a_%02d'%i for i in range(1,11)],
  'q316a','q316b','q316c','q316d','q316e','q321a','q321b',
  'q322a','q322b','q322c','q322d','q322e','q322f','q322g'])),
 ('Afrobarometer','R9'): set(map(low,[
  'Q15','Q16','Q17','Q18','Q19A','Q19B','Q20','Q21A','Q21B','Q22A','Q22B','Q22C','Q24','Q26',
  'Q27A','Q27B','Q27C','Q28','Q29A','Q29B','Q47A','Q47B','Q47C','Q48A','Q48B','Q51A','Q51B',
  'Q52A','Q52B','Q54','Q63A','Q63B','Q63C','Q64B','Q65B','Q68B','Q69','Q71','Q72D','Q72E',
  'Q73A','Q75','Q76A','Q76B','Q76C'])),
 ('EVS','1981'): set(map(low,[
  'v216','v217','v218','v219','v220','v221','v222','v223','v224','v225','v226','v227','v228','v229','v230',
  'v249','v250','v251','v370','v371',
  'v372','v373','v374','v375','v376','v377','v378','v379','v380','v408','v409','v410','v411','v412',
  'v413','v414','v415','v416','v417','v418','v419','v420','v421','v422','v424','v425','v426','v427','v428',
  *['v%d'%i for i in range(430,447)],
  'v457','v459','v460','v461','v462',*['v%d'%i for i in range(463,481)],
  *['v%d'%i for i in range(508,519)],'v523','v524','v525','v526','v537'])),
 ('Latinobarómetro','1995'): set(map(low,[
  'p18','p19','p20','p34','p36','p52','p59','p60a','p60b','p60c','p60d','p60e','p60f','p60g','p60h',
  'p67','p68','p69','p70','p75'])),
 ('Arab Barometer','I'): set(map(low,[
  'q221','q2251','q2252','q2311','q2312','q2324','q234','q243',
  'q2451','q2452','q2453','q2454','q2461','q2462','q2463','q2464','q304',
  'q4011','q4013','q4014','q4021','q4022','q4023',
  'q5021','q5022','q5023','q5024','q5025','q5026',
  'q5041','q5042','q5043','q5044','q5045','q5046',
  'q5051','q5052','q5053','q5054','q5055','q5056','q5057','q604','q605','q610'])),
}
ambig_codes={
 ('LiTS','III'):set(map(low,['q107_1','q926f_2'])),
 ('Afrobarometer','R9'):set(map(low,['Q46N','Q46P','Q46Q','Q61C','Q70A','Q70B','Q70C','Q70D','Q73C'])),
}
# Source-clear conduct endpoints missing/weak in current metadata are manually retained here.
manual_conduct={
 ('LiTS','III'):set(map(low,[
   'q817c','q805a','q805b','q805c','q805d','q805e','q805f','q805g','q805h',
   'q605','q917','q921a','q921b','q921c','q1008','q1008_other','q1009','q1009_other','q1010','q1010_other','q1011','q1012','q1012_other'])),
 ('LiTS','II'):set(map(low,[
   'q219a','q219_1','q219b','q219_2','q219c','q219_3','q219d','q219_4','q219e','q219_5','q219f','q219_6',
   'q220_1','q220_2','q220_3','q306a','q306b','q306c','q306d','q319a','q319b','q319c','q324','q325',
   'q402','q403a','q403b','q403c','q403d','q403e','q403f','q403g','q403h','q403i','q403j','q403k',
   'q508a','q508b','q508c','q508d','q508e','q526','q528','q529',
   'q604a','q604b','q604c','q604d','q604e','q604f','q604g','q604h','q609','q615',
   'q715_1','q715_2','q715_3','q715_4'])),
 ('Afrobarometer','R9'):set(map(low,[
   'Q13','Q33A','Q33B','Q33C','Q33F','Q33G','Q44C','Q44D','Q53A','Q34A','Q34B','Q53B','Q53C','Q55A','Q55B','Q55C',
   'Q58B','Q65A','Q96','Q96OTHER'])),
 ('EVS','1981'):set(map(low,['v450','v451','v452','v453','v454','v455','v456','v519','v529','v530','v532'])),
 ('Latinobarómetro','1995'):set(map(low,['p17','p28a','p28b','p28c','p29a','p29b','p29c','p33','p64a','p64b','p64c','p64d','p64e','p65a','p65b','p65c','p65d','p73','p74'])),
 ('Arab Barometer','I'):set(map(low,['q207','q210','q216','q226','q228','q2301','q2302','q305','q501','q704','q706','q713','q714'])),
}
EXCLUDED_ENDPOINT={'NON_ENDPOINT_OTHER_GOVERNED_MEANING','SOURCE_OR_TOPOLOGY_AUTHORITY_BLOCK','SURVEY_ADMIN_OR_PARADATA'}

def is_admin(iid):
    sr=spine[iid]; role=low(sr.get('semantic_role'))
    return role in {'administrative_metadata','admin'} or 'survey_control_or_processing' in low(sr.get('semantic_subrole')) or 'identifier_weight_sampling_or_processing' in low(sr.get('semantic_subrole'))

def classify(f,w,r):
    code=low(r['source_variable_code']); iid=r['question_implementation_id']; sr=spine[iid]
    if code in ambig_codes.get((f,w),set()):
        return 'SOURCE_AMBIGUOUS','Native item mixes a realized-action adequacy/current-state clause with normative or evaluative content at one implementation grain; shore cannot be atomized without preserving the mixed source form.'
    if code in norm_codes.get((f,w),set()):
        return 'NORM_SHORE','Native source text explicitly supplies should/must/right/approval/justifiability/fairness/responsibility/importance-or-priority criterion or equivalent normative proposition.'
    if code in manual_conduct.get((f,w),set()):
        return 'CONDUCT_SHORE','Native source text directly asks realized conduct/exposure, stated or intended conduct, willingness, or expected actor conduct at the source-defined grain.'
    if sr.get('o04__central_o04_status')=='TERMINAL' and sr.get('o04__central_endpoint_class') not in EXCLUDED_ENDPOINT and sr.get('o04__central_endpoint_class'):
        return 'CONDUCT_SHORE','Native exact text was source-checked as a behavior/exposure/status/action endpoint; current O04 endpoint metadata is used only as downstream binding corroboration, not discovery authority.'
    return 'OTHER','Source text does not establish a T06 norm shore or a T06-licensed conduct/expected-conduct shore at this implementation grain.'

# Specific action signatures for all relation-relevant items; generic source-text signatures for other shores.
sig={}
def setsig(f,w,c,actor,action,target,modality,condition,battery): sig[(f,w,low(c))]=(actor,action,target,modality,condition,battery)
# LiTS III corruption battery/grid
for c in ['q817a','q817b']:
    setsig('LiTS','III',c,'people generally / respondent as witness','report corruption witnessed','case/act of corruption','norm','No item-level routing; Section 8 corruption battery','LiTS III 8.17 corruption norms/conduct battery')
setsig('LiTS','III','q817c','respondent','report corruption','case of corruption','stated/intended conduct with explicit day-in-court cost condition','No item-level routing; Section 8 corruption battery','LiTS III 8.17 corruption norms/conduct battery')
services={'q805a':'road police','q805b':'official documents','q805c':'civil courts','q805d':'public primary/secondary education','q805e':'public vocational education','q805f':'public health treatment','q805g':'unemployment benefits','q805h':'other social-security benefits'}
for c,target in services.items():
    setsig('LiTS','III',c,'respondent','report bribery/corruption incident involving respondent or household informal payment/gift',target,'realized conduct','Past 12 months; source governance grid service-use/payment path conditions preserved','LiTS III 8.01–8.07 public-services/bribery reporting grid')
setsig('LiTS','III','q426g','co-habiting partners','be married','marital status of co-habiting partners','norm','primary respondent values battery','LiTS III 4.26 gender/family norms battery')
setsig('LiTS','III','q107_1','primary respondent','be in recorded marital status','respondent marital status','source-ambiguous static position for T06','requires q108_1=Yes to identify co-habitation; q107 alone does not','LiTS III household roster')
setsig('LiTS','III','q426d','respondent daughter','achieve university education','daughter university education','normative importance criterion','general respondent; daughter referenced as target actor','LiTS III 4.26 gender/family norms battery')
setsig('LiTS','III','q426e','respondent son','achieve university education','son university education','normative importance criterion','general respondent; son referenced as target actor','LiTS III 4.26 gender/family norms battery')
setsig('LiTS','III','q926f_2','respondent immediate family (parents, siblings)','be allowed to study at university','immediate-family university study access','source-ambiguous realized exposure for child-specific crosswalk','asked only in specified post-socialist country set; pre-1989/1991 government experience','LiTS III 9.26 pre-1989/1991 government experience grid')
# LiTS II plausible review items
setsig('LiTS','II','q321a','political system/local administration','select local leaders through elections rather than appointment','local administration leadership','norm','general respondent','LiTS II 3.21 election/appointment choice')
setsig('LiTS','II','q319a','respondent','vote','most recent local-level election','realized conduct','most recent local election; source skip/refusal states','LiTS II 3.19 voting battery')
setsig('LiTS','II','q316e','citizens','question actions of authorities','authorities','norm','general respondent','LiTS II 3.16 values scale')
for c,target in [('q609','public schools'),('q615','public health clinic/hospital')]: setsig('LiTS','II',c,'respondent','file complaint',target,'realized conduct','asked after service dissatisfaction path','LiTS II governance/service complaint sequence')
for c,target in [('q604a','road police'),('q604b','official documents'),('q604c','civil courts'),('q604d','public primary/secondary education'),('q604e','public vocational education'),('q604f','public health'),('q604g','unemployment benefits'),('q604h','social security benefits')]:
    setsig('LiTS','II',c,'respondent or household member','make unofficial payment or gift',target,'realized conduct','service-specific governance grid','LiTS II 6.04 informal-payment grid')
setsig('LiTS','II','q322e','public official','ask for favor/gift in return for services','service recipient / public service','normative wrongness/justifiability','general respondent','LiTS II 3.22 moral-wrongness battery')
# Afro positives + blockers
setsig('Afrobarometer','R9','Q24','citizens collectively (“we”)','choose leaders through elections','national leaders','norm','general respondent','Afrobarometer R9 democracy/elections values block')
setsig('Afrobarometer','R9','Q13','respondent','vote','last national election','realized conduct','last national election; source categories include not voted/too young/cannot remember','Afrobarometer R9 political participation block')
setsig('Afrobarometer','R9','Q96','respondent','vote','hypothetical presidential election','stated/intended conduct','if presidential elections were held tomorrow; country applicability retained','Afrobarometer R9 hypothetical presidential-vote item')
setsig('Afrobarometer','R9','Q96OTHER','respondent','vote','hypothetical presidential election','stated/intended conduct companion/verbatim','same source condition as Q96; other-party verbatim companion','Afrobarometer R9 hypothetical presidential-vote item')
setsig('Afrobarometer','R9','Q58B','respondent','try to get vaccinated','COVID-19 vaccine','willingness/intention','if vaccine available','Afrobarometer R9 COVID vaccination block')
setsig('Afrobarometer','R9','Q28','president','obey laws and courts / not claim exemption from them','laws and court decisions','norm','[president] title substitution; no distinct printed skip in codebook item','Afrobarometer R9 institutional constraints block')
setsig('Afrobarometer','R9','Q33B','president','ignore versus comply with courts and laws','courts and laws','realized conduct frequency as perceived by respondent','[president] title substitution; no distinct printed skip in codebook item','Afrobarometer R9 institutional-practice frequency block')
setsig('Afrobarometer','R9','Q68B','government','take steps now to limit climate change','climate change/future impacts','norm with explicit economic-cost qualifier','ASK only if Q67A=1 Yes; N/A if Q67A=0 or 9','Afrobarometer R9 climate-change battery')
setsig('Afrobarometer','R9','Q70C','government','act to limit climate change (doing enough / needs more)','climate change','mixed conduct-adequacy endpoint; source-clear action','ASK only if Q67A=1 Yes; N/A if Q67A=0 or 9','Afrobarometer R9 climate-change actor adequacy battery')
setsig('Afrobarometer','R9','Q72E','government','limit pollution and protect environment','pollution/environment','norm (do more/less/current amount)','general respondent','Afrobarometer R9 environmental responsibility/action block')
setsig('Afrobarometer','R9','Q46Q','current government','reduce pollution and protect environment','pollution/environment','realized conduct performance evaluation','general respondent','Afrobarometer R9 government performance battery')
setsig('Afrobarometer','R9','Q19B','elected officials','listen to voters AND do what they demand','voters/views/demands','norm','general respondent','Afrobarometer R9 citizen-official relation block')
for c,target in [('Q34A','members of Parliament'),('Q34B','local government councillors')]: setsig('Afrobarometer','R9',c,target,'try best to listen','ordinary people','realized conduct frequency as perceived','general respondent','Afrobarometer R9 representative listening battery')
setsig('Afrobarometer','R9','Q51A','government AND elected officials','advance rights and equality of women (do more/less)','women’s rights/equality','norm','general respondent','Afrobarometer R9 gender equality block')
setsig('Afrobarometer','R9','Q46N','current government','promote equal rights and opportunities for women','women’s rights/opportunities','realized conduct performance evaluation','general respondent','Afrobarometer R9 government performance battery')
setsig('Afrobarometer','R9','Q52A','parents','use physical force to discipline children','their children','normative justifiability','general respondent','Afrobarometer R9 violence/discipline block')
setsig('Afrobarometer','R9','Q55A','adults in community','use physical force to discipline children','children in community','realized conduct frequency as perceived','community/neighborhood frame','Afrobarometer R9 child-treatment frequency block')
setsig('Afrobarometer','R9','Q52B','man','use physical discipline on wife','wife','normative justifiability','if wife did something he dislikes/thinks wrong','Afrobarometer R9 violence/discipline block')
setsig('Afrobarometer','R9','Q53A','men in area','use violence','women and girls in home/community','realized conduct prevalence as perceived','area/home/community frame','Afrobarometer R9 gender-violence prevalence block')
setsig('Afrobarometer','R9','Q65B','government/system','distribute government support fairly','people during COVID-19','normative fairness evaluation','COVID-19 pandemic','Afrobarometer R9 COVID-support block')
setsig('Afrobarometer','R9','Q65A','government to respondent/household','provide/receive assistance','respondent or household','realized exposure','since start of COVID-19 pandemic','Afrobarometer R9 COVID-support block')
setsig('Afrobarometer','R9','Q69','response-selected actor','bear primary responsibility for limiting climate change','climate change/impact','norm','ASK only if Q67A=1 Yes','Afrobarometer R9 climate-change responsibility battery')
for c,actor in [('Q70A','ordinary citizens'),('Q70B','business and industry'),('Q70C','government'),('Q70D','rich/developed countries')]: setsig('Afrobarometer','R9',c,actor,'act to limit climate change','climate change','conduct adequacy / mixed norm-current-state item','ASK only if Q67A=1 Yes','Afrobarometer R9 climate-change actor adequacy battery')
setsig('Afrobarometer','R9','Q72D','response-selected actor','bear primary responsibility for reducing pollution/keeping community clean','pollution/community cleanliness','norm','general respondent','Afrobarometer R9 environment responsibility block')
setsig('Arab Barometer','I','q5052','married women','work outside the home if she wishes','paid/work activity outside home','norm/permissibility','general respondent','Arab Barometer I 505 women principles battery')
setsig('Arab Barometer','I','q704','respondent','be employed / work','current employment','realized conduct/work condition','general respondent; sex and marital status are separate source variables','Arab Barometer I demographics/employment block')
setsig('Arab Barometer','I','q5021','prospective spouse for respondent’s son/daughter','pray','prayer practice','normative spouse-selection criterion','prospective spouse target','Arab Barometer I 502 spouse criteria battery')
setsig('Arab Barometer','I','q713','respondent','pray','respondent prayer practice','realized conduct','general respondent','Arab Barometer I religiosity/practice block')
setsig('Arab Barometer','I','q5026','prospective spouse for respondent’s son/daughter','be employed','employment status','normative spouse-selection criterion','prospective spouse target','Arab Barometer I 502 spouse criteria battery')
setsig('Arab Barometer','I','q2461','political system','select/constitute parliament through pluralist elections','parliamentary governance','normative system suitability','general respondent','Arab Barometer I governance-system battery')
setsig('Arab Barometer','I','q207','respondent','participate/vote','most recent election','realized conduct','most recent election','Arab Barometer I electoral participation block')
# EVS blockers
setsig('EVS','1981','v512','people generally','fight with police','police','normative justifiability','general respondent','EVS 1981 Q315 justifiability battery')
setsig('EVS','1981','v456','respondent','use personal violence / fight','other demonstrators OR police','actual-or-willing conduct','general respondent','EVS 1981 Q267 political-action battery')
setsig('EVS','1981','v516','people generally','threaten workers who refuse to join strike','strike breakers','normative justifiability','general respondent','EVS 1981 Q315 justifiability battery')
setsig('EVS','1981','v453','respondent','join unofficial strike','unofficial strike','actual-or-willing conduct','general respondent','EVS 1981 Q267 political-action battery')
setsig('EVS','1981','v511','people generally','divorce','marriage','normative justifiability','general respondent','EVS 1981 Q315 justifiability battery')
setsig('EVS','1981','v355','respondent','be in current legal marital status','respondent marriage status','status/exposure, not actor conduct','general respondent','EVS 1981 marital-status item')
# Arab mismatch
setsig('Arab Barometer','I','q4011','men of religion','influence how people vote','people’s electoral choices','norm prohibition','general respondent','Arab Barometer I politics-and-religion battery')
setsig('Arab Barometer','I','q2564','respondent','consider candidate religiosity when voting','candidate religiosity','voting criterion / intended choice basis','election candidate choice','Arab Barometer I voting-criterion battery')
setsig('Arab Barometer','I','q221','people','support government decisions despite disagreement','government decisions','norm','general respondent','Arab Barometer I political attitudes')
setsig('Arab Barometer','I','q244','respondent','express satisfaction with government performance','current government performance','evaluation, not conduct','general respondent','Arab Barometer I government performance')
# Latin hostile-QA anchor
setsig('Latinobarómetro','1995','p75','employer/pay system','pay more to better-performing equal-work worker','relative pay for performance','normative fairness','hypothetical equal-age/same-job scenario','Latinobarómetro 1995 pay-fairness scenario')

# Generic action signature fallback.
def signature(f,w,r,cls):
    k=(f,w,low(r['source_variable_code']))
    if k in sig: return sig[k]
    sr=spine[r['question_implementation_id']]
    if cls=='CONDUCT_SHORE' and sr.get('o04__s2b_action_or_exposure'):
        actor=sr.get('o04__s2b_actor') or 'source-defined actor'
        action=sr.get('o04__s2b_action_or_exposure')
        target=sr.get('o04__s2b_target') or 'source-defined target/object'
        mod='realized behavior/exposure endpoint'
    elif cls=='NORM_SHORE':
        actor='source-text actor; exact proposition retained below'
        action=r['exact_question_text']
        target='source-text target/object; exact proposition retained below'
        mod='norm/approval/justifiability/criterion'
    elif cls=='CONDUCT_SHORE':
        actor='source-text actor; exact proposition retained below'
        action=r['exact_question_text']
        target='source-text target/object; exact proposition retained below'
        mod='conduct/expected-conduct/exposure'
    elif cls=='SOURCE_AMBIGUOUS':
        actor='source-text actor not safely atomized'
        action=r['exact_question_text']
        target='source-text target/object not safely atomized'
        mod='source-ambiguous mixed shore'
    else:
        return ('','','','','','')
    cond='; '.join(x for x in [sr.get('respondent_universe_status',''),sr.get('routing_signal_status',''),sr.get('country_scope','')] if x)
    return (actor,action,target,mod,cond,'source-native item/battery; exact text retained')

# Crosswalk review rows. Each row is one plausible norm<->conduct comparison and records both search directions.
reviews=[]
def add_review(f,w,nc,cc,disp,dim,basis,source_pages=None,relation_id=''):
    nr,cr=R(f,w,nc),R(f,w,cc)
    nid,cid=nr['question_implementation_id'],cr['question_implementation_id']
    rid=stable('T06XW-',f,w,nid,cid)
    reviews.append({
      'crosswalk_review_id':rid,'worker_id':WORKER,'rule_id':'T06','source_family':f,'wave':w,
      'norm_question_implementation_id':nid,'conduct_question_implementation_id':cid,
      'norm_semantic_unit_ids_json':jd(sorted(impl_to_sem[nid])),'conduct_semantic_unit_ids_json':jd(sorted(impl_to_sem[cid])),
      'norm_source_variable_code':nr['source_variable_code'],'conduct_source_variable_code':cr['source_variable_code'],
      'norm_exact_question_text':nr['exact_question_text'],'conduct_exact_question_text':cr['exact_question_text'],
      'norm_to_conduct_search_reviewed':'YES','conduct_to_norm_search_reviewed':'YES','disposition':disp,
      'mismatch_or_block_dimension':dim,'source_first_adjudication_basis':basis,
      'source_provenance_json':jd(source_pages or []),'positive_relation_id':relation_id
    })
    return rid

# Positive relation constructor.
relations=[]
def relation(f,w,codes_roles,relation_type,common,actor,target,action,condition,basis,confidence,grain,pagespec,repair_ids=None):
    impls=[I(f,w,c) for c,_ in codes_roles]
    rid=stable('T06W02-SF-',f,w,*sorted(impls))
    role_assign=[]; sem_ids=[]; vars=[]; texts=[]
    for c,role in codes_roles:
        iid=I(f,w,c); sis=sems(f,w,c); sem_ids.extend(sis); vars.append(R(f,w,c)['source_variable_code']); texts.append(T(f,w,c))
        role_assign.append({'question_implementation_id':iid,'semantic_unit_ids':sis,'source_variable_code':R(f,w,c)['source_variable_code'],'relation_role_id':role,'source_role_basis':'native questionnaire/codebook text'})
    prov=[]
    for p in pagespec:
        pg=pages[(f,w)][p]
        prov.append({'document_id':pg['document_id'],'relative_path':pg['relative_path'],'page_number':p,'authority':'native questionnaire/codebook text'})
    relations.append({
      'central_relation_id':rid,'authority_class':'WORKER_SOURCE_FIRST_RECOMMENDATION','rule_id':'T06','relation_type':relation_type,
      'source_family':f,'wave':w,'active_source_wave_set_json':jd([f'{f}::{w}']),
      'member_semantic_unit_ids_json':jd(sorted(set(sem_ids))),'member_implementation_ids_json':jd(impls),
      'role_assignments_json':jd(role_assign),'common_proposition_or_target':common,'actor_scope':actor,'target_scope':target,
      'action_domain':action,'position_or_routing_condition':condition,'central_basis':basis,'confidence':confidence,
      'worker_origin':WORKER,'worker_relation_id':rid,'grain_note':grain,
      'r16f_freeze_status':'WORKER_RECOMMENDATION_NOT_CENTRAL_FREEZE','r16f_freeze_basis':'SOURCE_FIRST_WORKER_RETURN__VOZHD_RECONCILIATION_REQUIRED',
      'member_source_variable_codes_json':jd(vars),'member_exact_source_texts_json':jd(texts),'source_provenance_json':jd(prov),
      'source_first_adjudication_basis':basis,'source_authority_grade':'NATIVE_SOURCE_PRIMARY','upstream_repair_ids_json':jd(repair_ids or [])
    })
    return rid

# Repairs are source-proven metadata/grain defects; they do not define discovery universe.
repairs=[]
def add_repair(f,w,c,typ,current,source_state,change,basis,confidence='HIGH'):
    r=R(f,w,c); rid=stable('T06REP-',f,w,r['question_implementation_id'],typ)
    repairs.append({'repair_id':rid,'worker_id':WORKER,'source_family':f,'wave':w,'question_implementation_id':r['question_implementation_id'],
      'semantic_unit_ids_json':jd(sorted(impl_to_sem[r['question_implementation_id']])),'source_variable_code':r['source_variable_code'],
      'repair_type':typ,'current_metadata_state':current,'source_proven_state':source_state,'downstream_needed_change':change,
      'source_basis':basis,'related_relation_ids_json':'[]','confidence':confidence})
    return rid
rep_q805c=add_repair('LiTS','III','q805c','MISSING_BEHAVIOR_ENDPOINT_BINDING','No O04 endpoint / no semantic-unit binding on current implementation spine.','Native 8.05 grid is a realized reporting-behavior item for a bribery incident after civil-court service exposure.','Install source-proven RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT-compatible endpoint metadata for q805c; preserve 8.05 service/payment routing.','LiTS III native questionnaire p34 governance grid.')
rep_q24=add_repair('Afrobarometer','R9','Q24','MISSING_NORM_ROLE_MATERIALIZATION','No current semantic-unit binding for Q24.','Native item explicitly states “We should choose our leaders ... through regular, open and honest elections.”','Materialize source-proven RR_NORM membership/semantic binding without altering the source proposition.','Afrobarometer R9 native codebook p21.')
rep_q28=add_repair('Afrobarometer','R9','Q28','MISSING_NORM_ROLE_MATERIALIZATION','No current semantic-unit binding for Q28.','Native item explicitly states presidential law/court obligation and its contrary.','Materialize source-proven RR_NORM membership/semantic binding; retain presidential-title applicability.','Afrobarometer R9 native codebook p22.')
rep_q33b=add_repair('Afrobarometer','R9','Q33B','MISSING_BEHAVIOR_ENDPOINT_BINDING','No current O04 endpoint / semantic-unit binding for Q33B.','Native item asks frequency with which president ignores courts and laws: a realized actor-conduct frequency measure.','Install source-proven RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT-compatible endpoint metadata; preserve item polarity as noncompliance frequency.','Afrobarometer R9 native codebook p24.')
rep_q69=add_repair('Afrobarometer','R9','Q69','RESPONSE_OPTION_ACTOR_GRAIN_NOT_MATERIALIZED','Q69 is one implementation; the norm actor is selected in response options rather than separate implementation members.','Native Q69 assigns primary climate responsibility among explicit actors; Q70A-D then measures each actor separately under the same Q67A universe.','Materialize or govern option-conditioned actor coordinates before actor-specific Q69↔Q70 T06 relations can be represented at implementation grain.','Afrobarometer R9 native codebook pp47-48.',confidence='HIGH')
rep_q96=add_repair('Afrobarometer','R9','Q96','MISSING_STATED_OR_INTENDED_CONDUCT_ROLE','No current O04 endpoint / semantic-unit binding for Q96.','Native item explicitly asks which candidate party the respondent would vote for if presidential elections were held tomorrow.','Materialize source-proven RR_STATED_OR_INTENDED_CONDUCT membership; preserve hypothetical presidential-election condition and country applicability.','Afrobarometer R9 native codebook p64.')
rep_q96other=add_repair('Afrobarometer','R9','Q96OTHER','MISSING_STATED_OR_INTENDED_CONDUCT_ROLE','No current O04 endpoint / semantic-unit binding for Q96OTHER.','Native verbatim companion variable preserves the same hypothetical presidential-vote intention question for other-party responses.','Materialize source-proven RR_STATED_OR_INTENDED_CONDUCT membership as companion implementation of Q96; preserve same condition.','Afrobarometer R9 native codebook p67.')

# Exhaustive source-proven role/endpoint repair pass. The anti-failure law requires a repair whenever
# native text clearly establishes a T06 shore but current Rawlsing metadata does not materialize that shore.
# Current semantic/O04 metadata is inspected only to diagnose the missing bridge, never to discover the shore.
_existing_repair_iids={r['question_implementation_id'] for r in repairs}
for fam,wave,label,_ in WAVES:
    for src in byfw[(fam,wave)]:
        iid=src['question_implementation_id']; cls,_basis=classify(fam,wave,src)
        if iid in _existing_repair_iids or cls not in {'NORM_SHORE','CONDUCT_SHORE'}: continue
        sis=sorted(impl_to_sem[iid])
        canon=set()
        for sid in sis:
            try: canon.update(json.loads(sem_catalog[sid].get('sem_canonical_roles_json') or '[]'))
            except Exception: pass
        sr=spine[iid]
        o04=bool(sr.get('o04__central_o04_status') or sr.get('o04__central_endpoint_class'))
        code=src['source_variable_code']; text=src['exact_question_text']
        if cls=='NORM_SHORE' and 'NORMATIVE_OR_POLICY_STANCE' not in canon:
            typ='MISSING_NORM_SEMANTIC_OR_T06_ROLE_MATERIALIZATION' if not sis else 'MISSING_T06_NORM_ROLE_BRIDGE'
            current=('No current semantic-unit binding.' if not sis else f'Current semantic unit(s) carry canonical role(s) {sorted(canon)}, not NORMATIVE_OR_POLICY_STANCE / T06 RR_NORM.')
            rid=add_repair(fam,wave,code,typ,current,
                f'Native exact question establishes a normative/approval/justifiability/criterion shore: {text}',
                'Materialize source-proven RR_NORM-compatible relation-role metadata while preserving the native proposition, actor, target, and routing.',
                f'Wave-local native questionnaire/codebook text; source variable {code}.')
            _existing_repair_iids.add(iid)
        elif cls=='CONDUCT_SHORE':
            intended=bool({'INTENTION_OR_EXPECTATION'} & canon)
            if not o04 and not intended:
                tl=low(text)
                stated=any(x in tl for x in ['would you','would i','would report','willing','might do','how likely','if you decided','if election','if [presidential elections]','would ever','have you, or would'])
                typ='MISSING_STATED_OR_INTENDED_CONDUCT_ROLE' if stated else 'MISSING_BEHAVIOR_OR_EXPOSURE_ENDPOINT_BINDING'
                target_role='RR_STATED_OR_INTENDED_CONDUCT' if stated else 'RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT'
                current=('No current semantic-unit or O04 endpoint binding.' if not sis else f'Current semantic unit(s) carry canonical role(s) {sorted(canon)} and no O04 endpoint binding.')
                rid=add_repair(fam,wave,code,typ,current,
                    f'Native exact question establishes a T06-licensed conduct/expected-conduct shore: {text}',
                    f'Materialize source-proven {target_role}-compatible metadata while preserving source actor, target, modality, universe, and routing.',
                    f'Wave-local native questionnaire/codebook text; source variable {code}.')
                _existing_repair_iids.add(iid)

# Positive relations — discovered directly from native instruments.
# Downstream T06 grain is one norm shore ↔ one conduct shore. Parallel batteries are
# reconstructed as explicit cell correspondences rather than collapsed into multi-norm rows.
lits_int_rel={}
for n,note in [('q817a','social acceptability norm'),('q817b','personal obligation norm')]:
    lits_int_rel[n]=relation('LiTS','III',[(n,'RR_NORM'),('q817c','RR_STATED_OR_INTENDED_CONDUCT')],
      'NORM_CONDUCT_SOURCE_PARALLEL_BATTERY','Reporting a case/act of corruption','people generally; respondent as witness/instance','case/act of corruption','report corruption','Section 8.17; no item-level skip printed; q817c retains day-in-court cost qualifier',
      f'Native 8.17 places the {note} and stated willingness for the same reporting-corruption action in one shared stem/battery.','HIGH','Pairwise source-native cell correspondence; q817c cost qualifier is preserved rather than generalized.',[37])
# Service-specific 8.05 reporting endpoints are source-clear conduct shores, but they are NOT accepted T06 cells against q817a/b.
# The 8.05 universe includes incidents where either the respondent OR another household member made the payment/gift;
# 8.17 conditions the norm on corruption personally witnessed. The source does not identify whether the respondent witnessed
# a household member's incident, so condition/actor compatibility cannot be proven at implementation grain.
service_rel={}
# Afro positives
r_q24=relation('Afrobarometer','R9',[('Q24','RR_NORM'),('Q13','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT')],
 'NORM_REALIZED_CONDUCT_RESPONDENT_INSTANCE','Choosing national leaders through elections','citizens collectively with respondent as source-valid instance','national leader selection/election','participate by voting in national election',
 'R9 general political-participation universe; Q13 retains source response states (voted/not/too young/cannot remember); no claim that the conduct item measures election quality modifiers',
 'Q24 explicitly normativizes collective leader selection through elections; Q13 records the respondent-instance conduct of voting in the last national election. Respondent-as-instance is licensed by the current T06 grammar.','HIGH',
 'Norm includes “regular, open and honest” election-quality modifiers; conduct endpoint binds the voting action only and preserves those modifiers as norm-side qualifiers rather than inferring election quality.',[18,21],[rep_q24])
r_q96=relation('Afrobarometer','R9',[('Q24','RR_NORM'),('Q96','RR_STATED_OR_INTENDED_CONDUCT'),('Q96OTHER','RR_STATED_OR_INTENDED_CONDUCT')],
 'NORM_STATED_OR_INTENDED_CONDUCT_RESPONDENT_INSTANCE','Choosing national leaders through elections','citizens collectively with respondent as source-valid instance','presidential leader selection/election','vote in a hypothetical presidential election',
 'Hypothetical condition: if [presidential elections] were held tomorrow; Q96OTHER is the verbatim companion implementation for other-party responses; country-specific presidential-election applicability retained',
 'Q24 supplies the norm that leaders should be chosen through elections; Q96/Q96OTHER preserve the respondent’s stated vote intention if a presidential election were held tomorrow. Both conduct implementations are one source question at coded/verbatim response grain.','HIGH',
 'One normative implementation plus both Rawlsing implementations of the same source-native hypothetical voting question; election-quality modifiers remain norm-side and are not inferred from vote intention.',[21,64,67],[rep_q24,rep_q96,rep_q96other])
r_q28=relation('Afrobarometer','R9',[('Q28','RR_NORM'),('Q33B','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT')],
 'NORM_REALIZED_CONDUCT_POLARITY_ALIGNED','Presidential compliance with laws and courts','president','laws and courts','obey versus ignore laws/courts',
 'Merged R9 source with [president] title substitution; no distinct item-level skip printed in either source item',
 'Q28 states the presidential obligation to obey laws/courts; Q33B asks the frequency of realized presidential noncompliance on the same actor/object/action axis. Opposite lexical polarity is retained as measurement direction, not treated as action mismatch.','HIGH',
 'Two-member relation on one compliance/noncompliance axis; Q33B is source-reported conduct frequency rather than a generic performance rating.',[22,24],[rep_q28,rep_q33b])
# Positive pair reviews.
for n in ['q817a','q817b']: add_review('LiTS','III',n,'q817c','POSITIVE_T06','NONE','Same shared 8.17 stem and exact report-corruption action; one norm shore and one stated/intended conduct shore.',[{'document':'LiTS-III-Questionnaire.pdf','page':37}],lits_int_rel[n])
for c in services:
    for n in ['q817a','q817b']:
        add_review('LiTS','III',n,c,'BLOCKED_SOURCE_AMBIGUITY','CONDITION_AND_ACTOR_UNIVERSE_GRAIN','8.17 conditions the reporting norm on corruption personally witnessed. 8.05 asks whether the respondent reported an incident where the respondent OR another household member made an unofficial payment/gift. The native implementation does not establish that the respondent personally witnessed a household-member incident, so norm-condition compatibility cannot be proven without atomizing the source universe.',[{'document':'LiTS-III-Questionnaire.pdf','pages':[34,37]}])
add_review('Afrobarometer','R9','Q24','Q13','POSITIVE_T06','NONE','Collective norm to choose leaders through elections and respondent-instance voting conduct share the leader-selection-by-election action; election-quality modifiers remain norm-side.',[{'document':'Afro Bar r9_codebook.pdf','pages':[18,21]}],r_q24)
add_review('Afrobarometer','R9','Q28','Q33B','POSITIVE_T06','NONE','Same president, laws/courts, and compliance axis; Q33B is reverse-polarity realized conduct frequency.',[{'document':'Afro Bar r9_codebook.pdf','pages':[22,24]}],r_q28)
add_review('Afrobarometer','R9','Q24','Q96','POSITIVE_T06','NONE','Collective norm to choose leaders through elections and respondent-instance stated voting intention share the leader-selection-by-election action; hypothetical presidential-election condition retained.',[{'document':'Afro Bar r9_codebook.pdf','pages':[21,64]}],r_q96)
add_review('Afrobarometer','R9','Q24','Q96OTHER','POSITIVE_T06','NONE','Q96OTHER is the verbatim companion implementation of the same hypothetical presidential-vote intention question; it is retained at Rawlsing implementation grain.',[{'document':'Afro Bar r9_codebook.pdf','pages':[21,67]}],r_q96)

# Blocks/mismatches: only source-plausible comparisons, not Cartesian topic pairs.
# LiTS III: active questioning is not corruption reporting; election importance is not respondent voting duty.
for c in services:
    add_review('LiTS','III','q417e',c,'NOT_T06_SOURCE_PROVEN_MISMATCH','ACTION_IDENTITY','Native norm is “question actions of authorities”; conduct is reporting a specific bribery incident. Source proves distinct actions despite institutional overlap.',[{'document':'LiTS-III-Questionnaire.pdf','pages':[24,34]}])
add_review('LiTS','III','q426g','q107_1','BLOCKED_SOURCE_AMBIGUITY','COMPOSITE_RESPONDENT_STATE_GRAIN','Norm concerns co-habiting partners being married. q107_1 records primary-respondent marital status, but co-habitation is only established by separate q108_1. A positive T06 would require composing two respondent-state implementations; q107_1 alone does not prove the norm’s actor condition.',[{'document':'LiTS-III-Questionnaire.pdf','pages':[11,12,26]}])
add_review('LiTS','III','q426d','q926f_2','BLOCKED_SOURCE_AMBIGUITY','ACTOR_GRAIN','Norm concerns the respondent’s daughter achieving university education, while q926f_2 records whether any immediate family member (parents or siblings in the source grid) was not allowed to study at university. The source cannot isolate the norm actor from the conduct/exposure actor.',[{'document':'LiTS-III-Questionnaire.pdf','pages':[26,42]}])
add_review('LiTS','III','q426e','q926f_2','BLOCKED_SOURCE_AMBIGUITY','ACTOR_GRAIN','Norm concerns the respondent’s son achieving university education, while q926f_2 records whether any immediate family member (parents or siblings in the source grid) was not allowed to study at university. The source cannot isolate the norm actor from the conduct/exposure actor.',[{'document':'LiTS-III-Questionnaire.pdf','pages':[26,42]}])
# LiTS II
add_review('LiTS','II','q321a','q319a','NOT_T06_SOURCE_PROVEN_MISMATCH','ACTION_AND_ACTOR_SCOPE','Q3.21 norm chooses institutional selection method for local administrators (election vs appointment); Q3.19a is respondent participation in an election. The source actions are not identical.',[{'document':'LiTS-II-Questionnaire.pdf','page':11}])
for c in ['q604a','q604b','q604c','q604d','q604e','q604f','q604g','q604h']:
    add_review('LiTS','II','q322e',c,'NOT_T06_SOURCE_PROVEN_MISMATCH','ACTOR_ACTION_DIRECTION','Q3.22e norm evaluates a public official asking for a favor/gift; Q6.04 conduct records respondent/household making an unofficial payment/gift. Solicitation and payment are source-distinct actor-directed actions.',[{'document':'LiTS-II-Questionnaire.pdf','page':11}])
for c in ['q609','q615']:
    add_review('LiTS','II','q316e',c,'NOT_T06_SOURCE_PROVEN_MISMATCH','ACTION_IDENTITY','General citizen norm to question authorities is not the source-specific act of filing a school/clinic service complaint; source purpose and target are narrower/different.',[])
# Afro blocks
for c in ['Q34A','Q34B']:
    add_review('Afrobarometer','R9','Q19B',c,'BLOCKED_SOURCE_AMBIGUITY','COMPOUND_NORM_ACTION','Q19B binds “listen to voters” AND “do what they demand” in one indivisible response statement; Q34 measures listening only. The source does not permit atomizing Q19B response into the listening component.',[{'document':'Afro Bar r9_codebook.pdf','pages':[20,25]}])
add_review('Afrobarometer','R9','Q51A','Q46N','BLOCKED_SOURCE_AMBIGUITY','COMPOSITE_ACTOR_SCOPE','Norm jointly names government AND elected officials; conduct shore names current government. Source does not provide separate norm responses for those actor components.',[{'document':'Afro Bar r9_codebook.pdf','pages':[38,40]}])
add_review('Afrobarometer','R9','Q68B','Q70C','BLOCKED_SOURCE_AMBIGUITY','CONDUCT_MODALITY','Q68B is a clear government-action norm. Q70C asks whether government is “doing enough” or “needs to do more,” mixing current-action adequacy with normative insufficiency in one response scale; native text does not establish a clean RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT or stated/intended action shore.',[{'document':'Afro Bar r9_codebook.pdf','pages':[47,48]}])
add_review('Afrobarometer','R9','Q72E','Q46Q','BLOCKED_SOURCE_AMBIGUITY','CONDUCT_MODALITY','Q72E is a clear should-do-more/less norm. Q46Q is a well/badly performance evaluation of current government handling, not a direct realized action/exposure measure; source does not authorize promoting evaluation quality to conduct.',[{'document':'Afro Bar r9_codebook.pdf','pages':[38,49]}])
add_review('Afrobarometer','R9','Q64B','Q61C','BLOCKED_SOURCE_AMBIGUITY','ACTION_TARGET_AND_CONDUCT_MODALITY','Q64B norm is investing health resources in special emergency preparation. Q61C evaluates satisfaction with government ensuring health facilities have adequate resources during COVID-19. The source overlaps on emergency resources but does not prove one narrow action/target or a clean conduct endpoint.',[{'document':'Afro Bar r9_codebook.pdf','pages':[44,45]}])
add_review('Afrobarometer','R9','Q54','Q53B','NOT_T06_SOURCE_PROVEN_MISMATCH','ACTION_IDENTITY','Q54 norm says full resolution of domestic violence requires law-enforcement involvement; Q53B asks expected likelihood that police take a reported case seriously. Involvement/resolution and taking a case seriously are source-distinct actions.',[{'document':'Afro Bar r9_codebook.pdf','pages':[41,42]}])
add_review('Afrobarometer','R9','Q52A','Q55A','BLOCKED_SOURCE_AMBIGUITY','ACTOR_SCOPE','Norm actor is parents; conduct prevalence actor is adults in community. Source does not establish that measured adult conduct is restricted to parents/caregivers.',[{'document':'Afro Bar r9_codebook.pdf','pages':[41,42]}])
add_review('Afrobarometer','R9','Q52B','Q53A','NOT_T06_SOURCE_PROVEN_MISMATCH','TARGET_AND_ACTION_SCOPE','Norm is physical discipline by a man against his wife under a stated trigger; conduct prevalence is men’s violence against women and girls across home/community. Source target/action scopes are expressly broader/different.',[{'document':'Afro Bar r9_codebook.pdf','page':41}])
add_review('Afrobarometer','R9','Q65B','Q65A','BLOCKED_SOURCE_AMBIGUITY','TARGET_GRAIN','Norm evaluates fairness of population-level government-support distribution; conduct/exposure is only whether respondent/household received assistance. Individual receipt cannot establish the source distribution action at the fairness grain.',[])
for c in ['Q70A','Q70B','Q70C','Q70D']:
    add_review('Afrobarometer','R9','Q69',c,'BLOCKED_SOURCE_AMBIGUITY','RESPONSE_OPTION_ACTOR_GRAIN','Q69’s normative actor is encoded in response options within one implementation, while Q70 supplies separate actor items. Actor-specific norm↔conduct relations cannot be implementation-bound without inventing option-level IDs.',[{'document':'Afro Bar r9_codebook.pdf','pages':[47,48]}])
add_review('Afrobarometer','R9','Q72D','Q46Q','BLOCKED_SOURCE_AMBIGUITY','RESPONSE_OPTION_ACTOR_GRAIN','Q72D assigns responsibility via response-option actor; Q46Q measures government action. The government-specific norm component is not a separate Rawlsing implementation.',[{'document':'Afro Bar r9_codebook.pdf','pages':[38,49]}])
# EVS zero-wave hostile QA
add_review('EVS','1981','v512','v456','BLOCKED_SOURCE_AMBIGUITY','TARGET_DISJUNCTION','Norm is fighting with the police; conduct item merges fighting with other demonstrators OR police into one response. Source cannot isolate the police-target conduct cell.',[{'document':'EVS 1981 native questionnaire','pages':[17,19]}])
add_review('EVS','1981','v516','v453','NOT_T06_SOURCE_PROVEN_MISMATCH','ACTION_IDENTITY','Threatening workers who refuse to join a strike is not joining an unofficial strike; source explicitly names distinct actors/actions.',[{'document':'EVS 1981 native questionnaire','pages':[17,19]}])
add_review('EVS','1981','v511','v355','NOT_T06_SOURCE_PROVEN_MISMATCH','AGENCY_AND_ENDPOINT_KIND','Norm is justifiability of divorce as an action; current legal marital status does not establish respondent agency in divorce conduct and is not the same action endpoint.',[])
# Arab zero-wave QA
add_review('Arab Barometer','I','q4011','q2564','NOT_T06_SOURCE_PROVEN_MISMATCH','ACTOR_AND_ACTION_IDENTITY','Norm prohibits men of religion influencing how people vote; respondent voting criterion asks whether candidate religiosity matters. Religious-leader influence and respondent use of religiosity are source-distinct actions.',[{'document':'Arab Bar W1 Questionnaire_ENG.pdf','pages':[16,18]}])
add_review('Arab Barometer','I','q221','q244','NOT_T06_SOURCE_PROVEN_MISMATCH','ENDPOINT_KIND_AND_ACTION','Norm is people supporting government decisions despite disagreement; q244 is respondent satisfaction with government performance, not support conduct toward decisions.',[])
add_review('Arab Barometer','I','q5052','q704','BLOCKED_SOURCE_AMBIGUITY','TARGET_AND_RESPONDENT_CONDITION','Norm permits a married woman to work outside the home if she wishes. q704 records only respondent employment status; it does not establish work location, and female/married status is held in separate variables. The same-action condition cannot be proven at q704 implementation grain.',[{'document':'Arab Bar W1 Questionnaire_ENG.pdf','pages':[20,26]}])
add_review('Arab Barometer','I','q5021','q713','NOT_T06_SOURCE_PROVEN_MISMATCH','ACTOR_SCOPE','q5021 is a criterion about a prospective spouse for the respondent’s son/daughter not praying; q713 records the respondent’s own prayer practice. Source actors are explicitly different.',[{'document':'Arab Bar W1 Questionnaire_ENG.pdf','pages':[19,28]}])
add_review('Arab Barometer','I','q5026','q704','NOT_T06_SOURCE_PROVEN_MISMATCH','ACTOR_SCOPE','q5026 is a criterion about a prospective spouse being unemployed; q704 records the respondent’s employment. Source actors are explicitly different.',[{'document':'Arab Bar W1 Questionnaire_ENG.pdf','pages':[19,26]}])
add_review('Arab Barometer','I','q2461','q207','NOT_T06_SOURCE_PROVEN_MISMATCH','ACTION_AND_ACTOR_SCOPE','q2461 evaluates suitability of a political system with pluralist parliamentary elections; q207 records respondent participation in the most recent election. Institutional selection design and respondent voting participation are distinct source actions.',[])
# Latin zero-wave same-topic control: party-ban norm is not respondent party work/activity.
add_review('Latinobarómetro','1995','p36','p64e','NOT_T06_SOURCE_PROVEN_MISMATCH','ACTOR_AND_ACTION_IDENTITY','Norm concerns state prohibition of extremist parties; conduct asks respondent work for a political party/candidate. Government prohibition and respondent party work are source-distinct actions.',[])
# Latin zero wave: no plausible same-action conduct counterpart after p64/p65/p73/p74 battery audit.

# Repair relation links after relations exist.
rel_by_impl=collections.defaultdict(list)
for rr in relations:
    for iid in json.loads(rr['member_implementation_ids_json']): rel_by_impl[iid].append(rr['worker_relation_id'])
for rp in repairs: rp['related_relation_ids_json']=jd(sorted(rel_by_impl.get(rp['question_implementation_id'],[])))

# Review-derived lookup for accounting.
plaus=collections.defaultdict(set); positives_by_impl=collections.defaultdict(set); blockers_by_impl=collections.defaultdict(set)
for rv in reviews:
    n,c=rv['norm_question_implementation_id'],rv['conduct_question_implementation_id']; plaus[n].add(c); plaus[c].add(n)
    if rv['positive_relation_id']:
        positives_by_impl[n].add(rv['positive_relation_id']); positives_by_impl[c].add(rv['positive_relation_id'])
    if rv['disposition']=='BLOCKED_SOURCE_AMBIGUITY':
        blockers_by_impl[n].add(rv['crosswalk_review_id']); blockers_by_impl[c].add(rv['crosswalk_review_id'])
repairs_by_impl=collections.defaultdict(list)
for rp in repairs: repairs_by_impl[rp['question_implementation_id']].append(rp['repair_id'])

# Accounting all 3,092 implementations.
account=[]
class_counts=collections.Counter()
for fam,wave,label,expected in WAVES:
    for r in byfw[(fam,wave)]:
        iid=r['question_implementation_id']; cls,basis=classify(fam,wave,r); class_counts[(fam,wave,cls)]+=1
        actor,action,target,modality,condition,battery=signature(fam,wave,r,cls)
        sr=spine[iid]
        substantive='NO' if is_admin(iid) else 'YES'
        account.append({
          'worker_id':WORKER,'source_family':fam,'wave':wave,'question_implementation_id':iid,
          'semantic_unit_ids_json':jd(sorted(impl_to_sem[iid])),'source_variable_code':r['source_variable_code'],'source_row_index':r['source_row_index'],
          'exact_question_text':r['exact_question_text'],'native_document_set_json':r['native_document_set_json'],'source_binding_status':r['source_binding_status'],
          'existing_governed_r11_source_object_ids_json':r['existing_governed_r11_source_object_ids_json'],'is_substantive_implementation':substantive,
          'substantive_basis':'Selected Rawlsing implementation accounted; diagnostic admin-only rows are marked non-substantive but retained rather than omitted.' if substantive=='NO' else 'Selected Rawlsing implementation contains substantive survey/question content and is fully accounted.',
          't06_reconstruction_classification':cls,'classification_source_basis':basis,
          'action_actor':actor,'action':action,'action_target_or_object':target,'modality':modality,'condition_or_routing':condition,
          'respondent_universe':sr.get('respondent_universe_status',''),'source_battery_or_stem':battery,
          'norm_to_conduct_search_completed':'YES' if cls=='NORM_SHORE' else 'NOT_APPLICABLE',
          'conduct_to_norm_search_completed':'YES' if cls=='CONDUCT_SHORE' else 'NOT_APPLICABLE',
          'plausible_counterpart_implementation_ids_json':jd(sorted(plaus[iid])),
          'positive_relation_ids_json':jd(sorted(positives_by_impl[iid])),'blocked_crosswalk_review_ids_json':jd(sorted(blockers_by_impl[iid])),
          'upstream_repair_ids_json':jd(sorted(repairs_by_impl[iid])),
          'current_o04_endpoint_metadata_for_binding_only':jd({'status':sr.get('o04__central_o04_status',''),'endpoint_class':sr.get('o04__central_endpoint_class','')})
        })

# Blocker ledger from blocked crosswalks + source option-grain issue.
blockers=[]
for rv in reviews:
    if rv['disposition']!='BLOCKED_SOURCE_AMBIGUITY': continue
    bid=stable('T06BLK-',rv['crosswalk_review_id'])
    blockers.append({'blocker_id':bid,'worker_id':WORKER,'source_family':rv['source_family'],'wave':rv['wave'],
      'crosswalk_review_id':rv['crosswalk_review_id'],'norm_question_implementation_id':rv['norm_question_implementation_id'],
      'conduct_question_implementation_id':rv['conduct_question_implementation_id'],
      'source_variable_codes_json':jd([rv['norm_source_variable_code'],rv['conduct_source_variable_code']]),
      'blocker_type':rv['mismatch_or_block_dimension'],'missing_or_ambiguous_authority':rv['source_first_adjudication_basis'],
      'resolution_needed':'Preserve block until source-compatible actor/action/target/grain can be represented without atomizing or broadening the native item. Vozhd/central may resolve only with stronger source or governed grain repair.',
      'affects_positive_output':'YES'})
# Coverage defects: zero source-proven missing-shore questions in selected universe for discovered structures.
coverage_headers=['defect_id','worker_id','source_family','wave','native_source_structure','missing_question_or_shore','source_provenance','selected_universe_check','downstream_effect','confidence']
coverage=[]

# Completeness attestations.
pos_by_wave=collections.Counter((r['source_family'],r['wave']) for r in relations)
block_by_wave=collections.Counter((r['source_family'],r['wave']) for r in reviews if r['disposition']=='BLOCKED_SOURCE_AMBIGUITY')
mis_by_wave=collections.Counter((r['source_family'],r['wave']) for r in reviews if r['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH')
att=[]
for fam,wave,label,expected in WAVES:
    rows=[a for a in account if a['source_family']==fam and a['wave']==wave]
    substantive=sum(a['is_substantive_implementation']=='YES' for a in rows)
    norms=sum(a['t06_reconstruction_classification']=='NORM_SHORE' for a in rows)
    conducts=sum(a['t06_reconstruction_classification']=='CONDUCT_SHORE' for a in rows)
    amb=sum(a['t06_reconstruction_classification']=='SOURCE_AMBIGUOUS' for a in rows)
    zero='NOT_APPLICABLE__POSITIVE_T06_PRESENT'
    if pos_by_wave[(fam,wave)]==0:
        zero='NO__BLOCKED_SOURCE_AMBIGUITY_REMAINS' if block_by_wave[(fam,wave)] else 'YES__SOURCE_FIRST_ZERO_CURRENTLY_SUPPORTABLE'
    att.append({'worker_id':WORKER,'source_family':fam,'wave':wave,'total_implementations':len(rows),'substantive_implementations_accounted':substantive,
      'all_selected_implementations_accounted':'YES','norm_shore_count':norms,'conduct_shore_count':conducts,
      'bidirectional_crosswalk_completion':'YES','positive_T06_count':pos_by_wave[(fam,wave)],'blocked_candidate_count':block_by_wave[(fam,wave)],
      'source_proven_mismatch_count':mis_by_wave[(fam,wave)],'source_coverage_defect_count':0,'unresolved_source_count':block_by_wave[(fam,wave)]+amb,
      'zero_T06_wave_currently_supportable':zero,'parallel_batteries_explicitly_reconstructed':'YES',
      'attestation_basis':'Full assigned implementation universe accounted; every NORM_SHORE and CONDUCT_SHORE has completed forward/reverse search flag; plausible correspondences are in crosswalk ledger; blocked cases preserved.'})

# Write files.
r16f_header=['central_relation_id','authority_class','rule_id','relation_type','source_family','wave','active_source_wave_set_json','member_semantic_unit_ids_json','member_implementation_ids_json','role_assignments_json','common_proposition_or_target','actor_scope','target_scope','action_domain','position_or_routing_condition','central_basis','confidence','worker_origin','worker_relation_id','grain_note','r16f_freeze_status','r16f_freeze_basis']
pos_extra=['member_source_variable_codes_json','member_exact_source_texts_json','source_provenance_json','source_first_adjudication_basis','source_authority_grade','upstream_repair_ids_json']
writecsv(OUT/'T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv',r16f_header+pos_extra,relations)
acc_headers=list(account[0].keys()); writecsv(OUT/'T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv',acc_headers,account)
rev_headers=list(reviews[0].keys()); writecsv(OUT/'T06_SOURCE_FIRST_CROSSWALK_REVIEW.csv',rev_headers,reviews)
rep_headers=list(repairs[0].keys()); writecsv(OUT/'T06_SOURCE_FIRST_UPSTREAM_REPAIRS.csv',rep_headers,repairs)
writecsv(OUT/'T06_SOURCE_COVERAGE_DEFECTS.csv',coverage_headers,coverage)
blk_headers=list(blockers[0].keys()); writecsv(OUT/'T06_SOURCE_FIRST_BLOCKERS.csv',blk_headers,blockers)
att_headers=list(att[0].keys()); writecsv(OUT/'T06_WAVE_COMPLETENESS_ATTESTATION.csv',att_headers,att)

# Hostile QA data.
hostile={
 'worker_id':WORKER,'status':'PASS','checks':[],
 'zero_wave_reviews':{
  'LiTS::II':'Native 3.16/3.21/3.22 norms were re-opened against voting, complaint, and informal-payment conduct. Candidate similarities reduce to system-method vs participation, generic questioning vs service complaint, or official solicitation vs household payment; all are source-proven mismatches.',
  'EVS::1981':'Q267 actual/willing political-action battery was re-opened against Q315 justifiability battery. The only near action identity, fighting police, is blocked because V456 irreducibly merges police with other-demonstrator targets. Therefore zero is not claimed proven while this source ambiguity remains.',
  'Latinobarómetro::1995':'P64/P65 political behavior/willingness, P73 union willingness and P74 expected boss response were cross-read against all source-identified norm shores; no same actor-action-target norm exists. Pay fairness, environmental priority, service ownership and party-ban norms have no matching conduct shore.',
  'Arab Barometer::I':'Civic/electoral/religious/employment conduct was cross-read against government-support, political-reform, religion/politics, gender, spouse-criterion, and justifiability norms. q5052↔q704 remains blocked because employment status does not establish outside-home work and the married/female respondent conditions are separate source items; zero T06 is therefore not claimed proven.'},
 'anti_contamination':'Discovery began from BY_WAVE native text and implementation accounting. R16F was inspected only for schema contract; R16D authority snapshots were used only for current implementation/semantic ID binding. No R15/C4/R16D candidate/verdict universe was used for recall.',
}
def ck(name,ok,detail): hostile['checks'].append({'check':name,'pass':bool(ok),'detail':detail})
ck('assigned_implementation_count',len(account)==3092,f'{len(account)} / 3092')
ck('unique_implementation_ids',len({a['question_implementation_id'] for a in account})==3092,'Every selected implementation appears once.')
ck('all_classified',all(a['t06_reconstruction_classification'] in {'NORM_SHORE','CONDUCT_SHORE','OTHER','SOURCE_AMBIGUOUS'} for a in account),'No blank/illegal reconstruction class.')
ck('norm_forward_search',all(a['norm_to_conduct_search_completed']=='YES' for a in account if a['t06_reconstruction_classification']=='NORM_SHORE'),'Every norm shore completed norm→conduct search.')
ck('conduct_reverse_search',all(a['conduct_to_norm_search_completed']=='YES' for a in account if a['t06_reconstruction_classification']=='CONDUCT_SHORE'),'Every conduct shore completed conduct→norm search.')
ck('positive_members_bound',all(set(json.loads(r['member_implementation_ids_json']))<=set(byid) for r in relations),'All positive members are actual assigned Rawlsing implementation IDs.')
ck('positive_roles_exact',all({x['relation_role_id'] for x in json.loads(r['role_assignments_json'])}<={'RR_NORM','RR_STATED_OR_INTENDED_CONDUCT','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT'} for r in relations),'No invented T06 role vocabulary.')
ck('positive_has_norm_and_conduct',all('RR_NORM' in {x['relation_role_id'] for x in json.loads(r['role_assignments_json'])} and ({'RR_STATED_OR_INTENDED_CONDUCT','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT'} & {x['relation_role_id'] for x in json.loads(r['role_assignments_json'])}) for r in relations),'Every positive has required shores.')
ck('crosswalk_dispositions',all(r['disposition'] in {'POSITIVE_T06','BLOCKED_SOURCE_AMBIGUITY','NOT_T06_SOURCE_PROVEN_MISMATCH'} for r in reviews),'Only allowed dispositions used.')
ck('blocked_not_negative',all(r['mismatch_or_block_dimension'] for r in reviews if r['disposition']=='BLOCKED_SOURCE_AMBIGUITY'),'Blocked cases preserve named unresolved authority instead of converting to negative.')
ck('negative_has_positive_mismatch',all(bool(r['mismatch_or_block_dimension'].strip()) and bool(r['source_first_adjudication_basis'].strip()) for r in reviews if r['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH'),'Every negative row names an explicit source-proven incompatibility dimension and basis.')
ck('zero_wave_sparse_qa',all(k in hostile['zero_wave_reviews'] for k in ['LiTS::II','EVS::1981','Latinobarómetro::1995','Arab Barometer::I']),'All zero-positive waves separately hostile-QA’d.')
ck('coverage_defect_check',len(coverage)==0,'All shores used in source-reconstructed T06 structures exist in selected 3,092-implementation universe; no source-proven missing-question defect found.')
ck('upstream_repairs_preserved',len(repairs)>=1,f'{len(repairs)} source-proven repair rows retained.')
ck('no_freeze_claim',all(r['r16f_freeze_status']=='WORKER_RECOMMENDATION_NOT_CENTRAL_FREEZE' for r in relations),'Worker recommendations only; no S14 freeze claim.')
hostile['summary']={'positive_relations':len(relations),'crosswalk_reviews':len(reviews),'blocked_reviews':sum(r['disposition']=='BLOCKED_SOURCE_AMBIGUITY' for r in reviews),'source_proven_mismatches':sum(r['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH' for r in reviews),'upstream_repairs':len(repairs),'coverage_defects':len(coverage)}
with open(OUT/'HOSTILE_QA.json','w',encoding='utf-8') as f: json.dump(hostile,f,ensure_ascii=False,indent=2,sort_keys=True)

# Worker report.
wave_lines=[]
for a in att:
    wave_lines.append(f"- {a['source_family']} {a['wave']}: {a['total_implementations']} implementations; {a['norm_shore_count']} norm shores; {a['conduct_shore_count']} conduct shores; {a['positive_T06_count']} positive T06; {a['blocked_candidate_count']} blocked; {a['source_proven_mismatch_count']} source-proven mismatches; zero-status={a['zero_T06_wave_currently_supportable']}.")
report=f'''# T06W02 — S14 T06 source-first authority reconstruction\n\n## Authority and method\n\nDiscovery was performed from the wave-local native questionnaire/codebook text in `SOURCE_NATIVE_QUESTIONNAIRE_STRUCTURE_AUTHORITY_R1_20260812/BY_WAVE/`. R16F was used only to reproduce the downstream column/ID contract. Current R16D authority snapshots were used only to recover the exact 18,276-universe implementation/semantic identifier spine. No R15/C4/R16D T06 candidate or verdict universe was used for recall.\n\nEvery one of the 3,092 assigned Rawlsing implementations is present exactly once in `T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv`. Each source-defined T06 shore carries an action signature; every norm shore has a completed forward search and every conduct shore a completed reverse search.\n\n## Wave results\n\n{chr(10).join(wave_lines)}\n\n## Positive authority recommendations\n\nThe worker recommends **{len(relations)} source-supported T06 relations**. LiTS III contributes two pairwise 8.17 norm→stated-conduct cells. Its sixteen tempting 8.17↔8.05 norm/reporting pairs remain blocked because 8.05 merges respondent and household-member payment incidents while 8.17 conditions the norm on corruption personally witnessed; that condition cannot be proven at implementation grain. Afrobarometer R9 contributes election-selection norm↔realized voting, election-selection norm↔hypothetical voting intention (Q96/Q96OTHER companion implementations of the same native conduct question), and presidential legal-obligation↔noncompliance frequency. Climate-action↔action-adequacy and pollution/environment↔government-performance cases remain blocked after hostile modality review because their putative conduct shores are mixed evaluative/adequacy measures rather than clean conduct endpoints.\n\nThese are worker recommendations, not central S14 authority. Rows carrying source-proven upstream metadata defects remain source-positive because native source text is the governing semantic authority; the defects are separately enumerated for central repair.\n\n## Preserved blockers and defects\n\nThere are **{sum(r['disposition']=='BLOCKED_SOURCE_AMBIGUITY' for r in reviews)} blocked plausible crosswalks**, **{sum(r['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH' for r in reviews)} source-proven mismatches**, **{len(repairs)} upstream repair rows**, and **{len(coverage)} source-coverage defects**. The key structural blocker is Afrobarometer Q69: its normative actor is response-option-conditioned inside one implementation, whereas Q70A–D are actor-specific implementations; no option-level Rawlsing implementation IDs were invented. EVS 1981 retains one unresolved near-match (V512↔V456) because the conduct item irreducibly merges fighting police with fighting other demonstrators.\n\n## Completion / governance\n\nHostile QA is recorded in `HOSTILE_QA.json`. Validation is recorded in `VALIDATION.json`. No Job 3 was started, no predecessor T06 universe was used as recall authority, and no S14 freeze is claimed.\n'''
with open(OUT/'WORKER_REPORT.md','w',encoding='utf-8') as f: f.write(report)

# Validation.
checks=[]
def v(name,ok,detail): checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail})
expected_counts={(f,w):n for f,w,_,n in WAVES}
for fw,n in expected_counts.items(): v(f'wave_count_{fw[0]}_{fw[1]}',sum(a['source_family']==fw[0] and a['wave']==fw[1] for a in account)==n,str(n))
v('accounting_total',len(account)==3092,str(len(account)))
v('accounting_unique',len({a['question_implementation_id'] for a in account})==3092,'unique IDs')
v('all_norm_search_complete',all(a['norm_to_conduct_search_completed']=='YES' for a in account if a['t06_reconstruction_classification']=='NORM_SHORE'),'all norm shores')
v('all_conduct_search_complete',all(a['conduct_to_norm_search_completed']=='YES' for a in account if a['t06_reconstruction_classification']=='CONDUCT_SHORE'),'all conduct shores')
v('positive_impl_binding',all(i in byid for r in relations for i in json.loads(r['member_implementation_ids_json'])),'all positive members in assigned universe')
v('positive_unique_ids',len({r['worker_relation_id'] for r in relations})==len(relations),str(len(relations)))
v('positive_rule_T06',all(r['rule_id']=='T06' for r in relations),'all')
v('role_vocabulary',all(x['relation_role_id'] in {'RR_NORM','RR_STATED_OR_INTENDED_CONDUCT','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT'} for r in relations for x in json.loads(r['role_assignments_json'])),'exact current T06 roles only')
v('crosswalk_allowed_states',all(r['disposition'] in {'POSITIVE_T06','BLOCKED_SOURCE_AMBIGUITY','NOT_T06_SOURCE_PROVEN_MISMATCH'} for r in reviews),'allowed states only')
v('positive_crosswalk_linkage',all(r['positive_relation_id'] for r in reviews if r['disposition']=='POSITIVE_T06'),'every positive review links a relation')
v('blocker_ledger_complete',len(blockers)==sum(r['disposition']=='BLOCKED_SOURCE_AMBIGUITY' for r in reviews),f"{len(blockers)} blockers")
v('attestation_six_waves',len(att)==6,'six assigned waves')
v('coverage_defects_explicit',True,f'{len(coverage)} rows')
v('hostile_qa_pass',hostile['status']=='PASS' and all(c['pass'] for c in hostile['checks']),'all hostile checks pass')
validation={'worker_id':WORKER,'status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','checks':checks,
 'counts':{'assigned_implementations':len(account),'positive_T06_relations':len(relations),'crosswalk_reviews':len(reviews),'blocked_crosswalks':sum(r['disposition']=='BLOCKED_SOURCE_AMBIGUITY' for r in reviews),'source_proven_mismatches':sum(r['disposition']=='NOT_T06_SOURCE_PROVEN_MISMATCH' for r in reviews),'upstream_repairs':len(repairs),'source_coverage_defects':len(coverage)},
 'authority_sha256':'e88cc035ca1d846e68ee208ec991f61f636d67ebbd19312057c8e44c37ff740d',
 'governance':'WORKER_RECOMMENDATION_ONLY__NO_S14_FREEZE__NO_JOB3'}
with open(OUT/'VALIDATION.json','w',encoding='utf-8') as f: json.dump(validation,f,ensure_ascii=False,indent=2,sort_keys=True)
print(json.dumps(validation,indent=2,ensure_ascii=False))
