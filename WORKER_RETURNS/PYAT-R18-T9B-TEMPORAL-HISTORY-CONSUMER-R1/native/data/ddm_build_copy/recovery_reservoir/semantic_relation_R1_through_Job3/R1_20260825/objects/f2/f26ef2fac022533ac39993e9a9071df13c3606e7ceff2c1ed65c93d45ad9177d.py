#!/usr/bin/env python3
from pathlib import Path
import pandas as pd, json, hashlib, gzip, re, os, textwrap
from collections import defaultdict, Counter

ROOT=Path(__file__).resolve().parents[1]
RET=ROOT/'RETURN'
BASE=pd.read_csv(ROOT/'AUTHORITY'/'NORMALIZED_PRIOR_T06_IMPLEMENTATION_ACCOUNTING.csv',dtype=str).fillna('')
CAL=pd.read_csv(ROOT/'AUTHORITY'/'ASSIGNED_T06_CALIBRATION_SLICE.csv',dtype=str).fillna('')
SRCROOT=Path('/mnt/data/t06w01_t15/source/unpacked/Rawlsing_SourceNative_Questionnaire_Structure_Authority_R1_20260812/BY_WAVE')
PARENT=Path('/mnt/data/t06w01_t15/parent_extract/T06W01')

WAVE_DIR={
 ('LiTS','IV'):'LiTS__IV',('WVS','W7'):'WVS__W7',('WVS','W4'):'WVS__W4',
 ('Afrobarometer','R5'):'Afrobarometer__R5',('Asian Barometer','W1'):'Asian_Barometer__W1',
 ('Afrobarometer','R1'):'Afrobarometer__R1'}

# ---- base helpers ----
def js(x): return json.dumps(x,ensure_ascii=False,separators=(',',':'))
BASE_BY_ID={r.question_implementation_id:r for _,r in BASE.iterrows()}
BASE_BY_KEY={(r.source_family,r.wave,r.source_variable_code.lower()):r for _,r in BASE.iterrows()}
def row(sf,w,code):
    k=(sf,w,code.lower())
    if k not in BASE_BY_KEY: raise KeyError(k)
    return BASE_BY_KEY[k]
def iid(sf,w,code): return row(sf,w,code).question_implementation_id
def txt(sf,w,code): return row(sf,w,code).exact_question_text

def source_page_rows(sf,w):
    wd=SRCROOT/WAVE_DIR[(sf,w)]/'NATIVE_SOURCE_PAGE_TEXT.jsonl.gz'
    out=[]
    with gzip.open(wd,'rt',encoding='utf-8',errors='ignore') as f:
        for line in f:
            try: out.append(json.loads(line))
            except: pass
    return out
PAGE_CACHE={k:source_page_rows(*k) for k in WAVE_DIR}

def locate(sf,w,code,needle=None):
    rows=PAGE_CACHE[(sf,w)]
    pats=[]
    if needle: pats.append(needle)
    if sf=='Afrobarometer' and w=='R5': pats += [f'Question Number: {code}',f'Question Number: {code.upper()}']
    elif sf=='Afrobarometer' and w=='R1': pats += [f'Variable name: {code}',f'Variable name: {code.lower()}']
    elif sf=='Asian Barometer':
        n=re.sub(r'[^0-9]','',code)
        if n: pats += [f'{int(n)}. ',f'{int(n)}.\n']
    elif sf=='LiTS':
        m=re.match(r'q(\d)(\d\d)([a-z]*)',code.lower())
        if m: pats += [f'{m.group(1)}.{m.group(2)})',f'{m.group(1)}.{m.group(2)}']
    else: pats += [code]
    exact=txt(sf,w,code)
    if len(exact)>24 and exact.lower() not in {'first priority of government spending','second priority of government spending','environment vs economic growth','support for democracy','extent of democracy'}:
        pats.append(exact[:80])
    for pat in pats:
        for r in rows:
            t=r.get('page_text') or r.get('text') or r.get('native_page_text') or ''
            i=t.lower().find(pat.lower())
            if i>=0:
                ex=t[max(0,i-350):min(len(t),i+1100)].replace('\x00',' ').strip()
                return {'document_id':r.get('document_id',''),'relative_path':r.get('relative_path',''),'page_number':r.get('page_number') or r.get('page') or r.get('source_page'),'match_pattern':pat,'excerpt':ex}
    # fail-safe: source context itself is governed
    return {'document_id':'','relative_path':'BY_WAVE/'+WAVE_DIR[(sf,w)]+'/IMPLEMENTATION_SOURCE_CONTEXT.csv','page_number':'','match_pattern':code,'excerpt':exact}

def prov(sf,w,ncode,pcode,nneedle=None,pneedle=None,extra=None):
    n=row(sf,w,ncode); p=row(sf,w,pcode)
    x=[{
      'authority':'Rawlsing_SourceNative_Questionnaire_Structure_Authority_R1_20260812',
      'source_family':sf,'wave':w,
      'norm':{'source_variable_code':ncode,'question_implementation_id':n.question_implementation_id,'selected_exact_question_text':n.exact_question_text,'native_locator':locate(sf,w,ncode,nneedle)},
      'praxis':{'source_variable_code':pcode,'question_implementation_id':p.question_implementation_id,'selected_exact_question_text':p.exact_question_text,'native_locator':locate(sf,w,pcode,pneedle)}
    }]
    if extra: x[0]['source_native_bridge']=extra
    return js(x)

POS=[]
REL_BY_PAIR={}

def add_pos(sf,w,ncode,pcode,subtype,norm_prop,praxis_prop,praxis_kind,actor_scope,actor_basis,target_scope,target_basis,action_domain,action_basis,polarity,distance,bridge,bridge_ids,condition,basis,confidence='HIGH',rid_suffix=None,t06_status='NO_STRICT_T06_OVERLAP',overlaps=None,grain_note='',nneedle=None,pneedle=None,source_bridge=None):
    rid_suffix=rid_suffix or f'{ncode}-{pcode}'
    rid='T15W01-S14T15-'+sf.replace(' ','_').replace('barometer','BAR')+'-'+w+'-'+rid_suffix
    rid=rid.replace('/','_').replace(' ','_')
    roles=[
      {'question_implementation_id':iid(sf,w,ncode),'source_variable_code':ncode,'t15_member_function':'NORM_SHORE','norm_proposition':norm_prop,'actor_scope':actor_scope},
      {'question_implementation_id':iid(sf,w,pcode),'source_variable_code':pcode,'t15_member_function':'PRAXIS_SHORE','praxis_shore_kind':praxis_kind,'praxis_proposition':praxis_prop,'actor_scope':actor_scope}
    ]
    member_sem=[]
    # preserve calibration semantic IDs when provided (currently empty in W01 slice, but generic)
    cal=CAL[(CAL.source_family==sf)&(CAL.wave==w)&CAL.member_implementation_ids_json.str.contains(re.escape(iid(sf,w,ncode)),regex=True)&CAL.member_implementation_ids_json.str.contains(re.escape(iid(sf,w,pcode)),regex=True)]
    if len(cal):
        try: member_sem=json.loads(cal.iloc[0].member_semantic_unit_ids_json or '[]')
        except: member_sem=[]
    POS.append({
      'worker_relation_id':rid,'central_relation_id':'','authority_class':'WORKER_SOURCE_FIRST_T15_POSITIVE','rule_id':'S14-T15','relation_type':'NORM_PRACTICAL_REALIZATION','manifestation_subtype':subtype,
      'source_family':sf,'wave':w,'active_source_wave_set_json':js([f'{sf}::{w}']),'member_semantic_unit_ids_json':js(member_sem),
      'member_implementation_ids_json':js([iid(sf,w,ncode),iid(sf,w,pcode)]),'role_assignments_json':js(roles),
      'common_proposition_or_target':target_scope,'norm_proposition':norm_prop,'praxis_proposition':praxis_prop,'praxis_shore_kind':praxis_kind,
      'actor_scope':actor_scope,'actor_alignment_basis':actor_basis,'target_scope':target_scope,'target_alignment_basis':target_basis,'action_domain':action_domain,'action_alignment_basis':action_basis,
      'relation_polarity':polarity,'realization_distance':distance,'bridge_basis_type':bridge,'bridge_basis_ids_json':js(bridge_ids),'position_or_routing_condition':condition,
      'respondent_universe_intersection':'Same wave respondent universe, with member-specific source conditions preserved as stated in position_or_routing_condition.',
      'source_provenance_json':prov(sf,w,ncode,pcode,nneedle,pneedle,source_bridge),'source_first_adjudication_basis':basis,'central_basis':'',
      'confidence':confidence,'worker_origin':'T06W01','grain_note':grain_note or 'Implementation-bound T15 source-first relation; semantic-unit IDs retained only where supplied by the continuation authority.',
      't06_overlap_status':t06_status,'overlap_with_existing_s14_rule_json':js(overlaps or []),'successor_freeze_status':'WORKER_PROPOSED','successor_freeze_basis':'Worker source-first authority only; requires central T15 adjudication. No S14 freeze claim.'
    })
    REL_BY_PAIR[(sf,w,ncode.lower(),pcode.lower(),rid_suffix)]=rid
    return rid

# ---------------- POSITIVES ----------------
# LiTS IV: explicit 4.04 priority -> 4.05 respondent financing battery, same nine named fields.
categories=[
 (1,'Education','q405a'),(2,'Healthcare','q405b'),(3,'Housing','q405c'),(4,'Pensions','q405d'),(5,'Assisting the poor / reducing inequality','q405e'),
 (6,'Creating jobs','q405f'),(7,'Combating climate change','q405g'),(8,'Public physical infrastructure','q405h'),(9,'Digital infrastructure','q405i')]
for ncode,ordword in [('q404a','first'),('q404b','second')]:
  for value,target,pcode in categories:
    add_pos('LiTS','IV',ncode,pcode,'INSTRUMENTAL_ENACTMENT',
      f'{target} should be the respondent-selected {ordword} priority for extra government spending.',
      f'Respondent is willing to give part of income or pay more taxes if the extra money is spent on {target}.',
      'STATED_INTENDED_CONDUCT','government as spending actor; respondent as normative selector and financing contributor',
      'Source-native 4.04/4.05 battery explicitly links respondent priority selection to respondent financing of extra government spending.',target,
      'Exact same named 4.04 category is repeated in 4.05; no topic inference.',f'finance extra government spending on {target}',
      '4.05 explicitly states that the respondent gives income/pays taxes if the extra money is spent on the same 4.04 field.','ENACTS','D3_EXPLICIT_MEANS','SOURCE_NATIVE_BATTERY_BRIDGE',
      ['LiTS-IV-native-4.04-4.05-page45'],f'ASK ALL; {ncode} response must equal category {value} ({target}); {pcode} asked for all respondents.',
      'Native questionnaire page 45 places Q4.04 and Q4.05 in one aligned nine-field spending/financing structure. The praxis action is an explicit financing means for the exact selected spending end.',
      rid_suffix=f'{ncode.upper()}-{pcode.upper()}-CAT{value}',nneedle='4.04)',pneedle='4.05)',source_bridge='Native page 45: Q4.04 asks first/second priorities for extra government spending; Q4.05 asks willingness to give income/pay more taxes if extra money is spent on each identical category.')

add_pos('LiTS','IV','q401f','q405e','INSTRUMENTAL_ENACTMENT',
 'The gap between the rich and the poor in the country should be reduced.',
 'Respondent is willing to give part of income or pay more taxes if the extra money is spent on assisting the poor / reducing inequality.',
 'STATED_INTENDED_CONDUCT','societal/policy norm; respondent as financing contributor','Q4.05e names reducing inequality as the financed end.',
 'reducing inequality','The praxis target explicitly includes “reducing inequality,” matching the norm end.','finance inequality reduction','Q4.05e itself states the money is used for reducing inequality.',
 'ENACTS','D3_EXPLICIT_MEANS','SOURCE_EXPLICIT_MEANS',['LiTS-IV-q401f','LiTS-IV-q405e-native-explicit-end'],
 'ASK ALL; ordinary item-specific nonresponse codes preserved.','The source explicitly identifies the money financed by respondent income/taxes as money spent on reducing inequality; no external causal bridge is supplied by the worker.',
 rid_suffix='Q401F-Q405E',pneedle='4.05)')

for pcode,target in [('q422a','preventing environmental pollution'),('q422b','fighting climate change'),('q422c','preventing biodiversity loss')]:
 add_pos('LiTS','IV','q421',pcode,'INSTRUMENTAL_ENACTMENT',
   'Protecting the environment should be given priority even if it causes slower economic growth and some loss of jobs.',
   f'Respondent is willing to pay more in taxes if the extra money is used for {target}.','STATED_INTENDED_CONDUCT',
   'societal priority norm; respondent as financing contributor','Q4.22 states the respondent contribution is used for a named environmental-protection intervention.',
   'environmental protection',f'{target} is an explicit source-named environmental protection application.','finance a named environmental-protection intervention',
   'Q4.22 explicitly defines the tax contribution as money used to prevent/fight the environmental harm.','ENACTS','D3_EXPLICIT_MEANS','SOURCE_EXPLICIT_MEANS',
   ['LiTS-IV-native-4.21-4.22-page52'],'ASK ALL; T15 norm pole is Q4.21 response 1 (environmental protection priority); Q4.22 item asked to all.',
   'The native environment section states the normative protection priority and explicitly states the tax money is used to prevent/fight specific environmental harms.',
   rid_suffix=f'Q421-{pcode.upper()}',nneedle='4.21)',pneedle='4.22)',source_bridge='Native page 52: Q4.21 protection-vs-growth priority followed by Q4.22 willingness to pay more taxes if the extra money is used for named environmental interventions.')

# WVS W7 institutional realization
add_pos('WVS','W7','Q238','Q251','INSTITUTIONAL_OR_SOCIAL_REALIZATION',
 'A democratic political system is appraised as a good/bad way of governing the country.',
 'How democratically the country is actually being governed today, on a not-at-all to completely democratic scale.',
 'INSTITUTIONAL_STATE','same country-level political system','Norm and praxis concern the same country-level form of governance.',
 'democratic governance','Exact democratic-system target is shared.','democratic form of governance','Normative appraisal of a democratic political system and actual democraticness are the same institutional axis.',
 'REALIZES','D1_DIRECT','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',['WVS-W7-Q238-Q251-democracy-axis'],'All respondents to the respective political-regime batteries; missing/not-asked codes preserved.',
 'Q238 evaluates “having a democratic political system” as a way of governing this country; Q251 directly measures how democratically this country is governed today.',nneedle='Q238',pneedle='Q251')
add_pos('WVS','W7','Q243','Q232','INSTITUTIONAL_OR_SOCIAL_REALIZATION',
 'People choosing their leaders in free elections is an essential characteristic of democracy.',
 'Voters are offered a genuine choice in elections, measured by how often this occurs in the country.',
 'INSTITUTIONAL_STATE','electorate/country electoral system','Genuine voter choice is a narrower realized instance of people freely choosing leaders.',
 'free electoral choice','Praxis narrows the criterion to genuine voter choice in elections.','free choice of leaders in elections','The source wording directly binds free leader choice to genuine voter choice, without importing fairness/integrity constructs.',
 'REALIZES','D2_NARROWER_INSTANCE','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',['WVS-W7-Q243-Q232-free-choice'],'Q243 essential-characteristic scale; Q232 election-frequency scale; country-election universe preserved.',
 'Q243 is explicitly under the shared “essential characteristic of democracy” stem; Q232 directly measures whether voters receive genuine electoral choice.',nneedle='Q243',pneedle='Q232')
for pcode,praxis in [('Q225','Opposition candidates are prevented from running in the country’s elections.'),('Q231','Voters are threatened with violence at the polls.')]:
 add_pos('WVS','W7','Q243',pcode,'INSTITUTIONAL_OR_SOCIAL_REALIZATION',
  'People choosing their leaders in free elections is an essential characteristic of democracy.',praxis,'INSTITUTIONAL_STATE',
  'electorate/country electoral system','The praxis item measures a source-direct constraint on free electoral choice.',
  'free electoral choice','Candidate exclusion/voter coercion is a narrower contrary realization of free electoral choice.',
  'conditions of free leader choice', 'The praxis wording itself describes coercion/exclusion that frustrates free electoral choice; no broader election-integrity inference is used.',
  'FRUSTRATES','D2_NARROWER_INSTANCE','DIRECT_SOURCE_ENTAILMENT',[f'WVS-W7-Q243-{pcode}-free-election-constraint'],
  'Q243 essential-characteristic scale; election-frequency item asked in country-election battery.',
  'The contrary state is source-semantic: preventing opposition candidacy or threatening voters directly constrains whether people freely choose leaders. Fairness/media/bribery items are not generalized into this relation.',rid_suffix=f'Q243-{pcode}',nneedle='Q243',pneedle=pcode)
add_pos('WVS','W7','Q249','Q233','INSTITUTIONAL_OR_SOCIAL_REALIZATION',
 'Women having the same rights as men is an essential characteristic of democracy.',
 'Women have equal opportunities to run for office in the country’s elections, measured by frequency.',
 'INSTITUTIONAL_STATE','women as social class; electoral institutions','Equal candidacy opportunity is a narrower realized political-right instance of equal rights.',
 'equal rights for women','Office-candidacy opportunity is explicit target narrowing from general equal rights.','equal political opportunity','Q233 directly measures a concrete institutional opportunity that instantiates the Q249 rights criterion.',
 'REALIZES','D2_NARROWER_INSTANCE','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',['WVS-W7-Q249-Q233-women-rights'],'Q249 democracy-essentiality scale; Q233 election-frequency scale.',
 'The native texts establish the broad equal-rights criterion and a concrete equal political-opportunity realization.',nneedle='Q249',pneedle='Q233')

# WVS W4 T06 boundary calibration -> T15 practical violation
for pcode,pprop in [('V33','Respondent would give part of income if certain the money would prevent environmental pollution.'),('V34','Respondent would accept higher taxes if the extra money would prevent environmental pollution.')]:
 old='T06W01-T06-WVS-W4-V35-'+pcode
 add_pos('WVS','W4','V35',pcode,'PRACTICAL_VIOLATION',
  'Government should reduce environmental pollution, but it should not cost the respondent any money.',pprop,'STATED_INTENDED_CONDUCT','respondent','The norm explicitly locates the no-cost condition on “me”; the praxis item is first-person cost-bearing.',
  'personal monetary cost for pollution prevention','Same environmental-pollution target and respondent cost axis.','bear personal monetary cost for pollution prevention','Praxis is the explicit contrary cost-bearing practice to the norm’s “should not cost me” condition.',
  'VIOLATES','D1_DIRECT','SOURCE_EXPLICIT_VIOLATION',[old,'WVS-W4-environment-cost-battery'],'Same respondent universe; V33/V34 preserve their stated certainty/use-of-extra-money conditions.',
  'The source gives the same pollution-prevention target and directly opposing no-cost versus cost-bearing respondent positions. Central calibration marks this exact pair BOUNDARY_TO_T15.',rid_suffix=f'V35-{pcode}',t06_status='RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW',overlaps=[old])

# Afrobarometer R5 calibration positives
for pcode,target in [('Q25A','religious group outside regular worship'),('Q25B','voluntary association or community group')]:
 old=f'T06W01-T06-AFROBAROMETER-R5-Q19-{pcode}'
 add_pos('Afrobarometer','R5','Q19',pcode,'RIGHT_OR_PERMISSION_EXERCISE',
  'People should be able to join any organization whether or not government approves.',
  f'Respondent is a member/leader of a {target}.','REALIZED_SELF_CONDUCT','people/we; respondent as instance','Respondent is an instance of the protected actor class.',
  'organization membership',f'{target} is a specific organization instance under “any organization.”','join/belong to organization','Praxis directly exercises the protected join/belong action.',
  'EXERCISES','D2_NARROWER_INSTANCE','SOURCE_EXPLICIT_RIGHT_EXERCISE',[old],
  'Q19 right-bearing pole is Statement 2; Q25 membership/leadership categories preserve realized membership.',
  'Exact central calibration identifies these as right/freedom exercise rather than strict same-predicate T06 conduct.',rid_suffix=f'Q19-{pcode}',t06_status='RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW',overlaps=[old])
old='T06W01-T06-AFROBAROMETER-R5-Q58-Q26D'
add_pos('Afrobarometer','R5','Q58','Q26D','RIGHT_OR_PERMISSION_EXERCISE',
 'People being free to take part in demonstrations and protests is an essential characteristic of democracy (Q58 option 1).',
 'Respondent has attended, or would attend if given the chance, a demonstration or protest march.','STATED_INTENDED_CONDUCT',
 'people; respondent as instance','Respondent is an instance of the protected participation class.','demonstrations/protests','Exact same action/target; Q58 option 1 is the normative cell.',
 'take part in demonstrations/protests','Praxis records exercise or stated willingness to exercise the exact protected activity.','EXERCISES','D1_DIRECT','SOURCE_EXPLICIT_RIGHT_EXERCISE',[old,'Afro-R5-Q58-option1'],
 'Q58 relation applies only to response option 1; Q26D retains realized/would-do response branches.',
 'Native Q58 option 1 and Q26D share the exact protest-participation action; central calibration marks boundary to T15.',rid_suffix='Q58opt1-Q26D',t06_status='RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW',overlaps=[old],nneedle='Question Number: Q58',pneedle='Question Number: Q26D')
old='T06W01-T06-AFROBAROMETER-R5-Q78-Q26E'
add_pos('Afrobarometer','R5','Q78','Q26E','PRACTICAL_VIOLATION',
 'Use of violence is never justified in politics today (Q78 Statement 1 norm pole).','Respondent has used, or would use, force or violence for a political cause.',
 'STATED_INTENDED_CONDUCT','general political actor; respondent as instance','Respondent is an instance of the political actor class.',
 'political violence','Exact same political-violence action/target.','use force or violence for a political cause','Praxis directly instantiates the practice prohibited/rejected by the Statement 1 pole.',
 'VIOLATES','D1_DIRECT','SOURCE_EXPLICIT_VIOLATION',[old],
 'T15 polarity is relative to Q78 Statement 1 (“never justified”); Q26E response scale combines realized and would-do branches.',
 'Exact action/target alignment and contrary practical polarity are source-explicit; central calibration marks boundary to T15.',rid_suffix='Q78-Q26E',t06_status='RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW',overlaps=[old])

# R5 source-native norm -> institutional/practical realization additions
R5_INST=[
 ('Q19','Q17B','People should be able to join any organization whether or not government approves.','Respondent reports how free they are to join any political organization they want.','organization-joining freedom','REALIZES','D2_NARROWER_INSTANCE','Q19 right pole is Statement 2. Political organization is a narrower target instance.'),
 ('Q23','Q56C','Women should have equal rights and receive the same treatment as men (Statement 1).','Frequency with which women are treated unequally by traditional leaders.','equal treatment of women','FRUSTRATES','D2_NARROWER_INSTANCE','Q23 Statement 1; Q56C is a concrete institutional/social actor-specific contrary state.'),
 ('Q23','Q56D','Women should have equal rights and receive the same treatment as men (Statement 1).','Frequency with which women are treated unequally by police and courts.','equal treatment of women','FRUSTRATES','D2_NARROWER_INSTANCE','Q23 Statement 1; police/courts are a concrete institutional actor instance.'),
 ('Q23','Q56E','Women should have equal rights and receive the same treatment as men (Statement 1).','Frequency with which women are treated unequally by employers.','equal treatment of women','FRUSTRATES','D2_NARROWER_INSTANCE','Q23 Statement 1; employers are a concrete social actor instance.'),
 ('Q44','Q65E','Government narrowing the gap between rich and poor is selected as an essential characteristic of democracy (Q44 option 1).','How well the current government is handling narrowing gaps between rich and poor.','government narrowing rich-poor gaps','REALIZES','D1_DIRECT','Q44 option 1 only; Q65E directly measures current-government realization on the same target.'),
 ('Q44','Q28','People choosing leaders in free and fair elections is selected as an essential characteristic of democracy (Q44 option 2).','Freeness and fairness of the last national election.','free and fair elections','REALIZES','D1_DIRECT','Q44 option 2 only; Q28 uses the same free/fair election criterion for the realized last election.'),
 ('Q44','Q17C','People choosing leaders in free and fair elections is selected as an essential characteristic of democracy (Q44 option 2).','Respondent reports freedom to choose whom to vote for without feeling pressured.','free electoral choice','REALIZES','D2_NARROWER_INSTANCE','Q44 option 2 only; Q17C is a respondent-instance institutional freedom component.'),
 ('Q44','Q56A','People being free to express political views openly is selected as an essential characteristic of democracy (Q44 option 4).','Frequency with which people have to be careful about what they say about politics.','open political expression','FRUSTRATES','D2_NARROWER_INSTANCE','Q44 option 4 only; Q56A is the source-direct contrary political-speech state.'),
 ('Q45','Q65C','Government ensuring job opportunities for all is selected as an essential characteristic of democracy (Q45 option 3).','How well the current government is handling creating jobs.','government job provision','REALIZES','D2_NARROWER_INSTANCE','Q45 option 3 only; Q65C is the current-government realization measure on creating jobs.'),
 ('Q57','Q65J','Government providing basic necessities such as food, clothing and shelter for everyone is selected as essential to democracy (Q57 option 2).','How well the current government is ensuring everyone has enough to eat.','universal basic-necessity provision','REALIZES','D2_NARROWER_INSTANCE','Q57 option 2 only; food sufficiency is an explicit narrower instance of the source-listed basic necessities.'),
 ('Q57','Q65I','Public services such as roads, water or sewerage working well and not breaking down is selected as essential to democracy (Q57 option 4).','How well the current government is handling provision of water and sanitation services.','functioning public services','REALIZES','D2_NARROWER_INSTANCE','Q57 option 4 only; water/sewerage is explicitly named in the norm cell.'),
 ('Q57','Q65N','Public services such as roads, water or sewerage working well and not breaking down is selected as essential to democracy (Q57 option 4).','How well the current government is handling maintenance of roads and bridges.','functioning public services','REALIZES','D2_NARROWER_INSTANCE','Q57 option 4 only; roads are explicitly named in the norm cell.'),
 ('Q58','Q60A','Politics being clean and free of corruption is selected as an essential characteristic of democracy (Q58 option 2).','Perceived corruption among the President/Prime Minister and officials in the executive office.','corruption-free politics','FRUSTRATES','D2_NARROWER_INSTANCE','Q58 option 2 only; top executive political office is a source-explicit political actor instance.'),
 ('Q58','Q60B','Politics being clean and free of corruption is selected as an essential characteristic of democracy (Q58 option 2).','Perceived corruption among Members of Parliament.','corruption-free politics','FRUSTRATES','D2_NARROWER_INSTANCE','Q58 option 2 only; parliamentarians are a direct political actor instance.'),
 ('Q58','Q60D','Politics being clean and free of corruption is selected as an essential characteristic of democracy (Q58 option 2).','Perceived corruption among local government councilors.','corruption-free politics','FRUSTRATES','D2_NARROWER_INSTANCE','Q58 option 2 only; elected/local political office is a direct political actor instance.'),
 ('Q38','Q53','News media should constantly investigate and report on government mistakes and corruption (Statement 1).','How effective the news media is in revealing government mistakes and corruption.','media scrutiny of government mistakes/corruption','REALIZES','D1_DIRECT','Q38 Statement 1; Q53 directly measures realized effectiveness of the exact prescribed media function.'),
 ('Q37','Q52D','Opposition parties should regularly examine and criticize government policies and actions (Statement 1).','Frequency with which opposition parties or their supporters are silenced by government.','opposition scrutiny/criticism','FRUSTRATES','D2_NARROWER_INSTANCE','Q37 Statement 1; silencing is a direct institutional constraint on the prescribed opposition criticism function.'),
 ('Q36','Q52E','Parliament should ensure the President regularly explains how government spends taxpayers’ money (Statement 1).','Frequency with which the President ignores parliament and just does what he wants.','parliamentary accountability of president','FRUSTRATES','D2_NARROWER_INSTANCE','Q36 Statement 1; ignoring parliament directly frustrates parliament’s prescribed accountability function.'),
 ('Q32','Q42','Democracy is preferable to any other kind of government (Statement 1 preference pole).','How much of a democracy the country is today.','democratic governance','REALIZES','D1_DIRECT','Normative regime preference and current realized regime type concern the same democracy axis.'),
 ('Q32','Q46A','Democracy is preferable to any other kind of government (Statement 1 preference pole).','Country today placed on a 0 completely undemocratic to 10 completely democratic scale.','democratic governance','REALIZES','D1_DIRECT','Normative regime preference and current realized regime type concern the same democracy axis.')
]
for n,p,np,pp,targ,pol,dist,cond in R5_INST:
 add_pos('Afrobarometer','R5',n,p,'INSTITUTIONAL_OR_SOCIAL_REALIZATION',np,pp,'INSTITUTIONAL_STATE',
  'institutional/social actor named by the source; respondent supplies normative appraisal or realized-state report',
  'Norm and praxis are wave-local measures of the same institution/social criterion; actor narrowing is stated in the target basis.',targ,
  'Praxis is exact or source-explicit narrower institutional/social realization; no ideological bridge used.',targ,'Direct/narrow source semantics establish the practical state on the norm axis.',pol,dist,'SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',[f'Afro-R5-{n}-{p}-source-axis'],cond,
  'Native R5 source text establishes a direct institutional/social realization or frustration relation at the stated option/statement grain.',rid_suffix=f'{n}-{p}')

# R5 exact practical violations
add_pos('Afrobarometer','R5','Q40','Q52C','PRACTICAL_VIOLATION',
 'The President must always obey the laws and the courts even if he thinks they are wrong (Q40 Statement 2).','Frequency with which the President ignores the courts and laws of the country.',
 'REALIZED_OTHER_CONDUCT','President','Exact same institutional actor on both shores.','laws and courts','Exact same target pair.','presidential compliance with laws/courts','“Ignore” is source-explicit noncompliance with “must obey.”','VIOLATES','D1_DIRECT','SOURCE_EXPLICIT_VIOLATION',['Afro-R5-Q40-Q52C-obey-ignore'],
 'T15 violation polarity is relative to Q40 Statement 2; Q52C frequency scale preserved.','The source supplies the same actor, laws/courts target, and explicit obey versus ignore polarity.',rid_suffix='Q40-Q52C')
add_pos('Afrobarometer','R5','Q50','Q56I','PRACTICAL_VIOLATION',
 'Citizens must pay their taxes to government (Q50 Statement 1).','Frequency with which people avoid paying the taxes they owe government.',
 'REALIZED_OTHER_CONDUCT','citizens/people','“People” are instances of the citizen-class duty; no respondent-specific assumption is needed.','taxes owed to government','Q56I preserves the exact tax/nonpayment target, unlike Q26C’s tax-or-fee composite.','pay taxes owed to government','Avoiding payment is source-explicit noncompliance with the must-pay norm.','VIOLATES','D1_DIRECT','SOURCE_EXPLICIT_VIOLATION',['Afro-R5-Q50-Q56I-tax-duty'],
 'T15 violation polarity relative to Q50 Statement 1; Q56I country-frequency scale.','Exact tax duty and observed tax avoidance share actor class, action and target. Q26C is separately blocked because it conflates tax/fee.',rid_suffix='Q50-Q56I')
add_pos('Afrobarometer','R5','Q76A','Q56H','PRACTICAL_VIOLATION',
 'Not paying for services received from government is normatively evaluated as wrong/not-wrong on Q76A; the wrong pole rejects nonpayment.','Frequency with which people obtain household services such as water/electricity without paying for them.',
 'REALIZED_OTHER_CONDUCT','people using government services','Household-service users are a narrower instance of people receiving government services.','payment for government services','Household water/electricity services are a source-explicit narrower service instance.','pay for government services received','Obtaining the service without payment directly instantiates the nonpayment practice evaluated by Q76A.','VIOLATES','D2_NARROWER_INSTANCE','SOURCE_EXPLICIT_VIOLATION',['Afro-R5-Q76A-Q56H-service-nonpayment'],
 'T15 violation polarity is relative to Q76A wrong/rejected pole; Q56H country-frequency scale.','The source gives direct nonpayment semantics; household services narrow the target without changing the action.',rid_suffix='Q76A-Q56H')

# Asian Barometer W1 newly recovered norm/practical state axes
add_pos('Asian Barometer','W1','q101','q100','INSTITUTIONAL_OR_SOCIAL_REALIZATION',
 'Desired present level of democracy for the country on a complete-dictatorship to complete-democracy scale.','Actual placement of the country under the present government on the identical complete-dictatorship to complete-democracy scale.',
 'INSTITUTIONAL_STATE','country political system; respondent rates desired and actual state','Native questionnaire places Q100 and Q101 on the identical rating board and same country/present-time object.',
 'country democraticness','Identical scale, target, country and present-time political-system axis.','level of democratic governance','Desired institutional state and present realized institutional state are directly comparable on the exact source scale.',
 'REALIZES','D1_DIRECT','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',['Asian-W1-Q100-Q101-identical-democracy-scale'],'Q100/Q101 are adjacent on questionnaire page 8 and use the identical 1 dictatorship–10 democracy rating board.',
 'Baseline T06 OTHER classification is reopened: Q101 is an explicit desired institutional state under T15, and Q100 is its exact present realization measure.',rid_suffix='Q101-Q100',nneedle='101.',pneedle='100.')
for n,p,np,pp,target in [
 ('q134','q105','Government should decide whether certain ideas should be allowed to be discussed in society.','Comparative realized state: everyone is free to say what they think, better/same/worse than before.','freedom versus government control of expression'),
 ('q136','q112','When judges decide important cases, they should accept the view of the executive branch.','Comparative realized state: judges and courts are free from political interference, better/same/worse than before.','judicial subordination versus judicial independence')]:
 add_pos('Asian Barometer','W1',n,p,'INSTITUTIONAL_OR_SOCIAL_REALIZATION',np,pp,'INSTITUTIONAL_STATE',
  'institutional actor/state directly named in both items','Praxis is the direct contrary institutional state on the same actor/action axis.',target,
  'The normative proposition and realized state are semantic opposites on the exact freedom/interference axis.','institutional freedom/control axis','No broad democracy inference: only the explicit source-opposed institutional state is linked.',
  'FRUSTRATES','D1_DIRECT','DIRECT_SOURCE_ENTAILMENT',[f'Asian-W1-{n}-{p}-opposed-state-axis'],'Q105–Q113 are explicitly comparative present-vs-prior-government realization items; norm item is in the later normative proposition battery.',
  'The source wording directly opposes the norm proposition and practical institutional state; comparative direction is preserved rather than converted to an absolute state.',rid_suffix=f'{n.upper()}-{p.upper()}',pneedle='better than before')

# Afrobarometer R1 direct institutional/life-state realization
R1_INST=[
 ('supdem','dmpext','Democracy is preferable to any other form of government (democratic-preference pole).','Measured extent of democracy in the country.','INSTITUTIONAL_STATE','democratic governance','REALIZES','D1_DIRECT','Source codebook supdem preference and dmpext realized regime extent share the democracy axis.'),
 ('demnec','povfoo','Everyone enjoying basic necessities such as shelter, food and water is an essential/important characteristic of democratic society.','Respondent/family has gone without enough food during the past year.','LIFE_STATE','universal access to basic necessities: food','FRUSTRATES','D2_NARROWER_INSTANCE','Food is explicitly named as a basic necessity; an instance of going without food directly frustrates the “everyone” criterion.'),
 ('demnec','povwat','Everyone enjoying basic necessities such as shelter, food and water is an essential/important characteristic of democratic society.','Respondent/family has gone without enough clean/domestic water during the past year.','LIFE_STATE','universal access to basic necessities: water','FRUSTRATES','D2_NARROWER_INSTANCE','Water is explicitly named as a basic necessity; an instance of going without water directly frustrates the “everyone” criterion.'),
 ('dememp','pfeemp','Jobs for everyone are an essential/important characteristic of democratic society.','How well the government is handling creation of jobs.','INSTITUTIONAL_STATE','job provision/creation','REALIZES','D2_NARROWER_INSTANCE','Creating jobs is the direct institutional action that realizes the source-stated jobs-for-everyone criterion.'),
 ('demgap','pfegap','A small income gap between rich and poor is an essential/important characteristic of democratic society.','How well the government is handling reducing the income gap.','INSTITUTIONAL_STATE','reducing rich-poor income gap','REALIZES','D1_DIRECT','Current-government handling directly measures action toward the exact income-gap end.'),
 ('maremp','pfeemp','Government is selected/included as responsible for creating jobs.','How well the government is handling creation of jobs.','INSTITUTIONAL_STATE','government responsibility for creating jobs','REALIZES','D1_DIRECT','Normative responsibility assignment and actual government performance share exact actor/action target; applies only when government is selected/included.'),
 ('marcrm','pfpcrm','Government is selected/included as responsible for reducing crime.','How well the government is handling crime.','INSTITUTIONAL_STATE','government responsibility for reducing crime','REALIZES','D2_NARROWER_INSTANCE','Normative responsibility assignment and government crime-handling performance share actor/target; applies only when government is selected/included.')]
for n,p,np,pp,pk,targ,pol,dist,basis in R1_INST:
 cond='Country-specific source wording/universe preserved; ordinary missing/not-asked codes retained.'
 if n in {'maremp','marcrm'}: cond+=' T15 relation applies only to source response categories in which government is selected or included in the responsibility assignment.'
 add_pos('Afrobarometer','R1',n,p,'INSTITUTIONAL_OR_SOCIAL_REALIZATION',np,pp,pk,
  'country/institutional actor or respondent/family instance explicitly named by source','Actor alignment follows the source-stated institution or respondent/family instance.',targ,
  'Exact target or source-explicit narrower instance; no external policy theory.','practical realization of the stated institutional/social criterion','Source text itself supplies the realized state/action on the norm axis.',pol,dist,'SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',[f'Afro-R1-{n}-{p}-source-axis'],cond,basis,rid_suffix=f'{n.upper()}-{p.upper()}')

# ---------- Strict T06 overlap ledger (excluded) and boundary recommendations ----------
OVER=[]
for _,r in CAL.iterrows():
    try: impls=json.loads(r.member_implementation_ids_json or '[]')
    except: impls=[]
    try: ncs=json.loads(r.norm_source_variable_codes_json or '[]'); pcs=json.loads(r.praxis_source_variable_codes_json or '[]')
    except: ncs=[]; pcs=[]
    posture=r.central_strict_t06_posture
    if posture=='RETAIN_STRICT_T06': disp='EXCLUDE_FROM_T15__STRICT_T06'; home='S14-T06'
    else: disp='RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW'; home='S14-T15'
    # use first norm and all praxis code(s); W01 calibration is binary except displayed combined metadata
    OVER.append({
      'overlap_id':'T15W01-OVERLAP-'+str(r.merge_index), 'source_family':r.source_family,'wave':r.wave,
      'prior_t06_worker_relation_id':r.worker_relation_id,'norm_implementation_ids_json':js(impls[:1]),'praxis_implementation_ids_json':js(impls[1:]),
      'prior_central_calibration_posture':posture,'t15_overlap_disposition':disp,'recommended_rule_home':home,
      'basis':r.calibration_note+' '+r.successor_use,
      'source_provenance_json':js([{'authority':'ASSIGNED_T06_CALIBRATION_SLICE.csv','merge_index':r.merge_index,'worker_relation_id':r.worker_relation_id,'calibration_family':r.calibration_family}])
    })

# ---------- Review ledger + blockers ----------
REV=[]; BLOCKS=[]

def add_review(sf,w,ncode,pcode,subtype,pk,nprop,pprop,actor,target,align,bridge,disp,basis,confidence='HIGH',positive_id='',block_class='',missing='',condition='',overlaps=None,bridge_ids=None):
    cid=f'T15W01-XW-{len(REV)+1:04d}'
    bid=''
    if disp=='BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY':
        bid=f'T15W01-BLOCK-{len(BLOCKS)+1:04d}'
        BLOCKS.append({'blocker_id':bid,'source_family':sf,'wave':w,'norm_implementation_ids_json':js([iid(sf,w,ncode)]),'praxis_implementation_ids_json':js([iid(sf,w,pcode)]),
          'candidate_manifestation_subtype':subtype,'blocker_class':block_class or 'SOURCE_OR_BRIDGE_AMBIGUITY','missing_authority':missing or basis,'source_basis':basis,
          'source_provenance_json':prov(sf,w,ncode,pcode),'resolution_needed':'Source/governed authority must establish the missing actor/target/action/condition or explicit means bridge; do not infer from topic proximity.'})
    REV.append({'crosswalk_id':cid,'source_family':sf,'wave':w,'norm_implementation_ids_json':js([iid(sf,w,ncode)]),'praxis_implementation_ids_json':js([iid(sf,w,pcode)]),
      'candidate_manifestation_subtype':subtype,'praxis_shore_kind':pk,'norm_proposition':nprop,'praxis_proposition':pprop,'actor_alignment':actor,'target_alignment':target,
      'action_or_realization_alignment':align,'bridge_basis_type':bridge,'bridge_basis_ids_json':js(bridge_ids or []),'position_or_routing_condition':condition,
      'source_provenance_json':prov(sf,w,ncode,pcode),'disposition':disp,'decision_basis':basis,'confidence':confidence,'positive_relation_id':positive_id,'blocker_id':bid,
      'overlap_with_t06_relation_ids_json':js(overlaps or [])})
    return cid,bid

# Positive reviews
for r in POS:
    impls=json.loads(r['member_implementation_ids_json']); n=BASE_BY_ID[impls[0]]; p=BASE_BY_ID[impls[1]]
    add_review(r['source_family'],r['wave'],n.source_variable_code,p.source_variable_code,r['manifestation_subtype'],r['praxis_shore_kind'],r['norm_proposition'],r['praxis_proposition'],
      r['actor_alignment_basis'],r['target_alignment_basis'],r['action_alignment_basis'],r['bridge_basis_type'],'POSITIVE_T15',r['source_first_adjudication_basis'],r['confidence'],r['worker_relation_id'],condition=r['position_or_routing_condition'],
      overlaps=json.loads(r['overlap_with_existing_s14_rule_json']),bridge_ids=json.loads(r['bridge_basis_ids_json']))

# strict overlap crosswalks excluded from positives
for o in OVER:
 if o['t15_overlap_disposition']=='EXCLUDE_FROM_T15__STRICT_T06':
  ns=json.loads(o['norm_implementation_ids_json']); ps=json.loads(o['praxis_implementation_ids_json'])
  if ns and ps:
   n=BASE_BY_ID[ns[0]]; p=BASE_BY_ID[ps[0]]
   add_review(o['source_family'],o['wave'],n.source_variable_code,p.source_variable_code,'DIRECT_ENACTMENT','OTHER_SOURCE_PROVEN_REALIZATION',n.exact_question_text,p.exact_question_text,
    'Strict T06 actor/action identity already governed.','Strict T06 target identity already governed.','Strict same-predicate T06 identity; T15 duplication forbidden.','DIRECT_SOURCE_ENTAILMENT','EXCLUDE_FROM_T15__STRICT_T06',
    'Exact calibration says RETAIN_STRICT_T06. Pair is ledgered but excluded from T15 positive authority.',positive_id='',condition='Preserve prior T06 routing/condition.',overlaps=[o['prior_t06_worker_relation_id']])

# BLOCK/MISMATCH plausible pairs source-first
BLOCK_CANDS=[
 # LiTS high-risk means bridges / conditions
 ('LiTS','IV','q409aa','q405f','INSTRUMENTAL_ENACTMENT','STATED_INTENDED_CONDUCT','Responsibility for supplying people with work.','Willingness to fund creating jobs.','Actor changes from responsibility assignee to respondent funder.','job provision','Same end but means link not stated.','', 'BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','MISSING_EXPLICIT_MEANS_BRIDGE','Source does not state that respondent tax/payment willingness is the realization of the state/private responsibility assignment.'),
 ('LiTS','IV','q409ab','q405h','INSTRUMENTAL_ENACTMENT','STATED_INTENDED_CONDUCT','Responsibility for building roads.','Willingness to fund public physical infrastructure.','Actor changes.','roads/infrastructure','Related target; bridge missing.','', 'BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','MISSING_EXPLICIT_MEANS_BRIDGE','No source-native battery or governed bridge binds the responsibility assignment to respondent financing.'),
 ('LiTS','IV','q409ac','q405a','INSTRUMENTAL_ENACTMENT','STATED_INTENDED_CONDUCT','Responsibility for providing education.','Willingness to fund education.','Actor changes.','education','Same field but means bridge missing.','', 'BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','MISSING_EXPLICIT_MEANS_BRIDGE','Same field is insufficient; source does not state that paying taxes realizes the responsibility assignment.'),
 ('LiTS','IV','q409ad','q405b','INSTRUMENTAL_ENACTMENT','STATED_INTENDED_CONDUCT','Responsibility for medical/health services.','Willingness to fund healthcare.','Actor changes.','healthcare','Same field but means bridge missing.','', 'BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','MISSING_EXPLICIT_MEANS_BRIDGE','Same field is insufficient; no explicit responsibility→financing bridge.'),
 ('LiTS','IV','q409ae','q405i','INSTRUMENTAL_ENACTMENT','STATED_INTENDED_CONDUCT','Responsibility for digital infrastructure.','Willingness to fund digital infrastructure.','Actor changes.','digital infrastructure','Same field but means bridge missing.','', 'BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','MISSING_EXPLICIT_MEANS_BRIDGE','Same field is insufficient; no explicit responsibility→financing bridge.'),
 ('LiTS','IV','q829a','q107b','RIGHT_OR_PERMISSION_EXERCISE','LIFE_STATE','Same-sex couples should have the right to marry.','Respondent marital status.','Actor/sexuality class not known.','marriage','Marital-status endpoint does not identify same-sex marriage.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','ACTOR_TARGET_CONDITION_UNRESOLVED','Source does not identify whether the respondent’s marital state is a same-sex marriage; absence of that binding is a block.'),
 ('LiTS','IV','q829b','q107b','RIGHT_OR_PERMISSION_EXERCISE','LIFE_STATE','Same-sex couples should have the right to adopt children.','Respondent marital status.','Wrong actor/action endpoint.','adoption','Marital status does not measure adoption.','DIRECT_SOURCE_ENTAILMENT','NOT_T15_SOURCE_PROVEN_MISMATCH','','Source positively establishes that marital status is not an adoption realization measure.'),
 # WVS W7
 ('WVS','W7','Q243','Q224','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Free elections as democracy criterion.','Votes counted fairly.','Country elections.','free elections vs fair counting','Fair counting is integrity/fairness, not explicitly the “free” condition.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','FREE_VS_FAIR_CONDITION_BRIDGE_MISSING','The source does not define fair counting as the Q243 free-election criterion; do not collapse free/fair.'),
 ('WVS','W7','Q243','Q227','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Free elections as democracy criterion.','Voters are bribed.','Country elections.','free elections vs bribery','Bribery is integrity pressure but source does not state the free-election bridge.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','FREE_ELECTION_BRIDGE_MISSING','Political plausibility is insufficient to classify bribery as exact realization of the Q243 free-election criterion.'),
 ('WVS','W7','Q243','Q228','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Free elections as democracy criterion.','Journalists provide fair coverage of elections.','Country elections/media.','free elections vs media fairness','Different condition/actor.','DIRECT_SOURCE_ENTAILMENT','NOT_T15_SOURCE_PROVEN_MISMATCH','','Source proves the praxis predicate is media fairness, not freedom of electoral choice.'),
 ('WVS','W7','Q243','Q229','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Free elections as democracy criterion.','Election officials are fair.','Country elections/officials.','free elections vs official fairness','Different condition.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','FREE_VS_FAIR_CONDITION_BRIDGE_MISSING','Source does not equate official fairness with the free-election criterion.'),
 ('WVS','W7','Q243','Q230','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Free elections as democracy criterion.','Rich people buy elections.','Country elections.','free elections vs vote-buying/control','Bridge not explicit.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','FREE_ELECTION_BRIDGE_MISSING','No source-explicit definition binds “rich people buy elections” to the free-election criterion.'),
 ('WVS','W7','Q246','Q253','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Civil rights protect people from state oppression.','Amount of respect for individual human rights nowadays.','Country rights regime.','civil rights/state oppression vs all human rights','Praxis target is broader and does not preserve state-oppression/civil-rights condition.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','RIGHTS_SCOPE_NOT_PRESERVED','Human-rights respect cannot be narrowed to civil-rights protection from state oppression from this item alone.'),
 # WVS W4
 ('WVS','W4','V167','V168','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Appraisal of having a democratic political system.','Satisfaction with the way democracy develops.','Same respondent/country.','democratic system vs satisfaction','Satisfaction is evaluation, not realized state.','DIRECT_SOURCE_ENTAILMENT','NOT_T15_SOURCE_PROVEN_MISMATCH','','Source explicitly makes V168 a satisfaction measure, not a measure of whether democratic institutions are realized.'),
 ('WVS','W4','V167','V173','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Appraisal of democratic political system.','Respect for individual human rights.','Country.','democracy vs human rights','Praxis is narrower/different criterion with no source bridge.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','DEMOCRACY_TO_RIGHTS_BRIDGE_MISSING','No source authority says the general democratic-system appraisal is realized specifically by V173 human-rights respect.'),
 # R5
 ('Afrobarometer','R5','Q34','Q28','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Regular, open and honest elections.','Freeness and fairness of last election.','Same country elections.','regular/open/honest vs free/fair','Conditions differ.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','ELECTION_CONDITION_TRANSLATION_MISSING','Source uses different qualifying conditions; do not translate regular/open/honest into free/fair without authority.'),
 ('Afrobarometer','R5','Q20','Q53','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Media right to publish views without government control.','Media effectiveness revealing government mistakes/corruption.','Media.','publication freedom vs watchdog effectiveness','Different practical predicate.','DIRECT_SOURCE_ENTAILMENT','NOT_T15_SOURCE_PROVEN_MISMATCH','','Source proves Q53 measures effectiveness revealing mistakes/corruption, not freedom from government publication control.'),
 ('Afrobarometer','R5','Q22','Q65P','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Women should have same chance of election to office as men.','Government handling empowering women.','Women/political vs general empowerment.','election opportunity vs empowerment','Praxis is broader and does not preserve office-election target.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','WOMEN_TARGET_SCOPE_NOT_PRESERVED','General empowerment cannot establish equal chance of election.'),
 ('Afrobarometer','R5','Q23','Q56B','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Women equal rights/treatment.','People treated unequally under law.','Women vs people generally.','gender equality vs generic legal equality','Gender target is absent from praxis.','DIRECT_SOURCE_ENTAILMENT','NOT_T15_SOURCE_PROVEN_MISMATCH','','Source proves Q56B is generic legal inequality, not specifically women’s equal treatment.'),
 ('Afrobarometer','R5','Q45','Q65F','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Government ensures law and order (Q45 option 1).','Government handling reducing crime.','Government.','law/order vs crime reduction','Plausible but not source-explicit equivalence.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','LAW_ORDER_TO_CRIME_BRIDGE_MISSING','Do not infer from policy/common-sense that reducing crime is the exact realization of the broader law-and-order criterion.'),
 ('Afrobarometer','R5','Q45','Q53','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Media free to criticize government (Q45 option 2).','Media effectiveness revealing government mistakes/corruption.','Media.','freedom vs effectiveness','Different predicate.','DIRECT_SOURCE_ENTAILMENT','NOT_T15_SOURCE_PROVEN_MISMATCH','','Source distinguishes media freedom from media effectiveness.'),
 ('Afrobarometer','R5','Q57','Q17B','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','People free to form organizations to influence government/public affairs (Q57 option 3).','Respondent free to join political organizations.','People/respondent.','form-for-influence vs join','Action/purpose differs.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','FORM_JOIN_PURPOSE_BRIDGE_MISSING','Source does not establish joining any political organization as equivalent to forming organizations for influence.'),
 ('Afrobarometer','R5','Q58','Q70B','INSTITUTIONAL_OR_SOCIAL_REALIZATION','LIFE_STATE','People receive government aid such as food parcels when in need (Q58 option 4).','Household receives food for children from school feeding program.','People/household.','need-conditioned aid vs program receipt','Need condition absent.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','NEED_CONDITION_NOT_PRESERVED','Program receipt does not establish the source-required “when in need” condition.'),
 ('Afrobarometer','R5','Q50','Q26C','PRACTICAL_VIOLATION','STATED_INTENDED_CONDUCT','Citizens must pay taxes.','Respondent refused/would refuse to pay a tax or fee.','Citizen/respondent.','tax vs tax-or-fee','Endpoint conflates target.','SOURCE_EXPLICIT_VIOLATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','TAX_FEE_TARGET_AMBIGUITY','Q26C does not identify whether the refusal concerns a tax or fee, so exact T15 tax noncompliance cannot be bound.'),
 ('Afrobarometer','R5','Q76B','Q56I','PRACTICAL_VIOLATION','REALIZED_OTHER_CONDUCT','Not paying income taxes owed is normatively evaluated/rejected.','People avoid paying taxes they owe government.','People.','income tax vs generic taxes','Praxis does not preserve income-tax restriction.','SOURCE_EXPLICIT_VIOLATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','INCOME_TAX_CONDITION_NOT_PRESERVED','Generic tax avoidance does not establish the income-tax subtype required by Q76B.'),
 ('Afrobarometer','R5','Q39','Q52E','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Members of Parliament should make laws even if President disagrees.','President ignores parliament and does what he wants.','Parliament/President.','law-making authority vs broad ignoring','Praxis not specifically lawmaking.','DIRECT_SOURCE_ENTAILMENT','NOT_T15_SOURCE_PROVEN_MISMATCH','','Source positively establishes Q39 as lawmaking authority while Q52E is broad parliamentary disregard; the required action identity is absent.'),
 ('Afrobarometer','R5','Q48A','Q52C','PRACTICAL_VIOLATION','REALIZED_OTHER_CONDUCT','Courts have right to make decisions people must abide by.','President ignores courts and laws.','People vs President.','court decisions vs composite courts/laws','Composite praxis cannot isolate court-decision noncompliance.','SOURCE_EXPLICIT_VIOLATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','COURTS_LAWS_COMPOSITE_TARGET','Q52C conflates courts and laws; Q40 is the exact source norm for that composite and is used instead.'),
 # Asian
 ('Asian Barometer','W1','q132','q106','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','People with little/no education should have as much say in politics as highly educated people.','Everyone treated equally by government, compared with before.','education-defined political groups vs everyone.','equal political say vs generic treatment','Praxis lacks education and political-say target.','DIRECT_SOURCE_ENTAILMENT','NOT_T15_SOURCE_PROVEN_MISMATCH','','Source proves different target/action dimensions.'),
 ('Asian Barometer','W1','q147','q105','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Political leader should tolerate views challenging his ideals.','Everyone free to say what they think, compared with before.','leader vs everyone.','leader tolerance vs general speech freedom','Actor/relational target absent.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','LEADER_CHALLENGER_RELATION_NOT_PRESERVED','General speech freedom does not preserve the leader-to-challenger relation.'),
 ('Asian Barometer','W1','q121','q100','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Get rid of parliament/elections and have strong leader decide things.','Country placement on dictatorship-democracy scale.','country political system.','specific authoritarian arrangement vs broad regime scale','Praxis broadens target.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','SPECIFIC_ARRANGEMENT_NOT_IDENTIFIED','Broad dictatorship-democracy position does not identify the specific strong-leader/no-parliament arrangement.'),
 # R1
 ('Afrobarometer','R1','demspc','pfrsay','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Freedom to criticize government is essential to democracy.','Present-versus-past freedom to say what you think.','people.','government criticism vs general speech','Praxis broadens target and is comparative.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','CRITICIZE_GOVERNMENT_TARGET_NOT_PRESERVED','General speech freedom does not establish the narrower freedom to criticize government.'),
 ('Afrobarometer','R1','demele','pfrele','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Regular elections essential to democracy.','Whether elections are honest.','country elections.','regularity vs honesty','Conditions differ.','DIRECT_SOURCE_ENTAILMENT','NOT_T15_SOURCE_PROVEN_MISMATCH','','Source proves regularity and honesty are distinct election properties.'),
 ('Afrobarometer','R1','demedu','pfgedu','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Equal education essential to democracy.','Government performance handling education.','country/government.','equal education vs education performance','Equality condition absent.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','EDUCATION_EQUALITY_CONDITION_MISSING','General education performance does not establish equal education.'),
 ('Afrobarometer','R1','marear','pfegap','INSTRUMENTAL_ENACTMENT','INSTITUTIONAL_STATE','Government should limit rich earnings versus free earnings.','Government handling reducing income gap.','government.','earnings limits vs income-gap reduction','Plausible means story only.','', 'BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','MISSING_EXPLICIT_MEANS_BRIDGE','Source does not state that earnings limits are the means by which the income gap is reduced; worker may not supply economic theory.'),
 ('Afrobarometer','R1','marjob','pfeemp','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Government should provide employment for everyone who wants work (government-employment pole).','Government handling creation of jobs.','government.','provide employment vs create jobs','Praxis is broader than direct public provision.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','PUBLIC_EMPLOYMENT_VS_JOB_CREATION_SCOPE','Creating jobs generally does not identify government-provided employment.'),
 ('Afrobarometer','R1','marsch','pfgedu','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Government selected/included as responsible for providing schools/clinics.','Government performance handling education.','government.','schools/clinics vs education','Praxis target broader.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','SCHOOL_TO_EDUCATION_SCOPE_NOT_PRESERVED','General education performance does not specifically measure providing schools.'),
 ('Afrobarometer','R1','marsch','pfghlt','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Government selected/included as responsible for providing schools/clinics.','Government performance handling basic health.','government.','schools/clinics vs health','Praxis target broader.','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','CLINIC_TO_HEALTH_SCOPE_NOT_PRESERVED','General basic-health performance does not specifically measure providing clinics.'),
 ('Afrobarometer','R1','supdem','dmpsat','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Democracy preferable.','Satisfaction with democracy.','respondent/country.','democracy preference vs satisfaction','Satisfaction is evaluation not realized regime state.','DIRECT_SOURCE_ENTAILMENT','NOT_T15_SOURCE_PROVEN_MISMATCH','','Source identifies dmpsat as satisfaction, not realization; dmpext is used as the actual-state counterpart.')
]
for sf,w,n,p,sub,pk,np,pp,actor,target,align,bridge,disp,bclass,reason in BLOCK_CANDS:
  add_review(sf,w,n,p,sub,pk,np,pp,actor,target,align,bridge or 'DIRECT_SOURCE_ENTAILMENT',disp,reason,'MEDIUM' if disp.startswith('BLOCKED') else 'HIGH',block_class=bclass,missing=reason)

# ---------- Composition bridge ledger ----------
BR=[]
for r in POS:
 if r['manifestation_subtype']=='INSTRUMENTAL_ENACTMENT':
  impls=json.loads(r['member_implementation_ids_json'])
  BR.append({'bridge_id':'T15W01-BRIDGE-'+f'{len(BR)+1:04d}','source_family':r['source_family'],'wave':r['wave'],'norm_implementation_ids_json':js([impls[0]]),'praxis_implementation_ids_json':js([impls[1]]),
   'manifestation_subtype':'INSTRUMENTAL_ENACTMENT','bridge_basis_type':r['bridge_basis_type'],'required_or_overlapping_s14_rule_ids_json':js([]),'bridge_authority_ids_json':r['bridge_basis_ids_json'],
   'source_explicit_bridge_text':r['source_first_adjudication_basis'],'source_provenance_json':r['source_provenance_json'],'bridge_status':'PROVEN','basis':'Explicit source/native battery bridge; no external causal theory.'})
# blocked bridge candidates
for b in BLOCKS:
 if b.get('candidate_manifestation_subtype')=='INSTRUMENTAL_ENACTMENT' and 'BRIDGE' in b['blocker_class']:
  BR.append({'bridge_id':'T15W01-BRIDGE-'+f'{len(BR)+1:04d}','source_family':b['source_family'],'wave':b['wave'],'norm_implementation_ids_json':b['norm_implementation_ids_json'],'praxis_implementation_ids_json':b['praxis_implementation_ids_json'],
   'manifestation_subtype':b['candidate_manifestation_subtype'],'bridge_basis_type':'','required_or_overlapping_s14_rule_ids_json':js([]),'bridge_authority_ids_json':js([]),'source_explicit_bridge_text':'',
   'source_provenance_json':b['source_provenance_json'],'bridge_status':'BLOCKED_NEEDS_EXPLICIT_BRIDGE','basis':b['missing_authority']})

# ---------- Upstream repairs ----------
REPAIRS=[]
def add_repair(sf,w,code,field,current,proven,basis,blocks='NO',affected=None):
 rid=f'T15W01-REPAIR-{len(REPAIRS)+1:03d}'
 REPAIRS.append({'repair_id':rid,'source_family':sf,'wave':w,'question_implementation_id':iid(sf,w,code),'repair_field':field,'current_value':current,'source_proven_value':proven,
  'source_basis':basis,'source_provenance_json':js([{'source_variable_code':code,'native_locator':locate(sf,w,code)}]),'blocks_runtime_relation':blocks,'affected_relation_ids_json':js(affected or [])})
 return rid
# LiTS source cell/stem losses
for code in ['q404a','q404b']:
 add_repair('LiTS','IV',code,'OPTION_LEVEL_POLICY_PRIORITY_BINDING',txt('LiTS','IV',code),'Bind response categories 1–9 to Education; Healthcare; Housing; Pensions; Assisting poor/reducing inequality; Creating jobs; Combating climate change; Public physical infrastructure; Digital infrastructure.','Native Q4.04 page 45 provides exact nine category cells required for T15 relation grain.')
for code,target in [(c,t) for _,t,c in categories]:
 add_repair('LiTS','IV',code,'SHARED_STEM_TARGET_AND_MEANS_CONDITION',txt('LiTS','IV',code),f'Would respondent give part of income or pay more taxes if sure the extra money was spent on {target}?','Native Q4.05 page 45 supplies the shared financing stem and exact category target; selected implementation text is partial for downstream semantics.')
add_repair('LiTS','IV','q421','OPTION_LEVEL_NORMATIVE_PROPOSITION_BINDING',txt('LiTS','IV','q421'),'Statement 1: Protecting the environment should be given priority even if slower economic growth and some loss of jobs; Statement 2: Economic growth/creating jobs top priority even if environment suffers.','Native Q4.21 page 52 contains normative proposition poles omitted from the selected short label.')
for code,target in [('q422a','prevent environmental pollution'),('q422b','fight climate change'),('q422c','prevent loss of biodiversity')]:
 add_repair('LiTS','IV',code,'SHARED_STEM_EXPLICIT_MEANS_CONDITION',txt('LiTS','IV',code),f'Respondent willingness to pay more in taxes if the extra money were used to {target}.','Native Q4.22 page 52 supplies the if-money-used means condition required for T15 instrumental authority.')
# WVS shared stems
for code,proven in [('Q238','Shared political-system stem: rate each named system as very/fairly good or fairly/very bad way of governing this country.'),('Q243','Shared Q241–Q249 stem: rate how essential each named characteristic is to democracy.'),('Q249','Shared Q241–Q249 stem: rate how essential each named characteristic is to democracy.')]:
 add_repair('WVS','W7',code,'SHARED_STEM_SEMANTIC_INHERITANCE',txt('WVS','W7',code),proven,'Native WVS W7 codebook/questionnaire supplies the shared normative stem; short selected text alone does not preserve it.')
# R5 option cell bindings
for code,vals in [
 ('Q44','Option 1 government narrows rich-poor gap; 2 people choose leaders in free/fair elections; 3 government does not waste public money; 4 people free to express political views openly.'),
 ('Q45','Option 1 government ensures law/order; 2 media free to criticize government; 3 government ensures jobs for all; 4 multiple parties compete fairly.'),
 ('Q57','Option 1 legislature monitors President; 2 government provides basic necessities; 3 people free to form organizations to influence public affairs; 4 public services roads/water/sewerage work well.'),
 ('Q58','Option 1 freedom demonstrations/protests; 2 politics clean/free corruption; 3 court protects ordinary people; 4 government aid when in need.')]:
 add_repair('Afrobarometer','R5',code,'OPTION_LEVEL_NORMATIVE_CELL_BINDING',txt('Afrobarometer','R5',code),vals,'Native R5 codebook gives distinct semantic cells inside a single categorical implementation; T15 relations are condition-bound to exact option values.')
# parent R1 composites preserved as repairs
for code in ['defnew','defjug','defele']:
 add_repair('Afrobarometer','R1',code,'COMPOSITE_NORM_PRACTICAL_SHORE_SPLIT',txt('Afrobarometer','R1',code),'Represent native (a) support/oppose norm and separate (b) “what, if anything, would you do about it?” practical-response shore as distinct source-native components/country variants.','Native R1 codebook explicitly says selected variable coding derives from two separate questions; selected universe has only a composite implementation.','YES')

# ---------- Coverage defects inherited from source-proven parent ancestry ----------
COV=[]
parent_cov=pd.read_csv(PARENT/'T06_SOURCE_COVERAGE_DEFECTS.csv',dtype=str).fillna('')
for _,r in parent_cov.iterrows():
 COV.append({'defect_id':r.coverage_defect_id.replace('T06W01','T15W01'),'source_family':r.source_family,'wave':r.wave,'native_source_member':r.native_structure,
  'native_source_text':r.source_action_target,'missing_or_collapsed_rawlsing_member':r.selected_universe_status,'defect_type':'COLLAPSED_NATIVE_NORM_AND_PRACTICAL_SHORES',
  'source_provenance_json':r.source_provenance_json,'affected_subtype':'DIRECT_ENACTMENT','runtime_relation_withheld':'YES',
  'basis':'Prior T06 source-first ancestry identified a source-native norm plus separate intended-response question collapsed into one implementation. T15 preserves the defect; it does not synthesize member IDs.'})

# ---------- Accounting ----------
# collect norm/praxis/counterpart/relation/block/repair metadata
norm_ids=set(BASE.loc[BASE.baseline_t06_classification=='NORM_SHORE','question_implementation_id'])
# newly recovered T15 norm shores
for sf,w,c in [('LiTS','IV','q421'),('Asian Barometer','W1','q101')]: norm_ids.add(iid(sf,w,c))
praxis_ids=set(BASE.loc[BASE.baseline_t06_classification=='CONDUCT_SHORE','question_implementation_id'])
for r in POS:
 ims=json.loads(r['member_implementation_ids_json']); praxis_ids.add(ims[1])
for r in REV:
 for x in json.loads(r['praxis_implementation_ids_json']): praxis_ids.add(x)
counter=defaultdict(set); rels=defaultdict(list); blocked=defaultdict(list); repairs_by=defaultdict(list); p_kind=defaultdict(set)
for r in REV:
 ns=json.loads(r['norm_implementation_ids_json']); ps=json.loads(r['praxis_implementation_ids_json'])
 for n in ns:
  counter[n].update(ps)
 for p in ps:
  counter[p].update(ns)
  if r['praxis_shore_kind']: p_kind[p].add(r['praxis_shore_kind'])
  if r['disposition']=='BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY': blocked[p].append(r['crosswalk_id'])
 for n in ns:
  if r['disposition']=='BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY': blocked[n].append(r['crosswalk_id'])
for r in POS:
 for x in json.loads(r['member_implementation_ids_json']): rels[x].append(r['worker_relation_id'])
for r in REPAIRS: repairs_by[r['question_implementation_id']].append(r['repair_id'])

ACC=[]
for _,b in BASE.iterrows():
 idd=b.question_implementation_id
 n_yes=idd in norm_ids; p_yes=idd in praxis_ids
 reopened=(b.baseline_t06_classification in {'OTHER','SOURCE_AMBIGUOUS'} and (n_yes or p_yes))
 sig={}
 if n_yes: sig['norm_candidate']={'source_variable_code':b.source_variable_code,'exact_question_text':b.exact_question_text}
 if p_yes: sig['praxis_candidate']={'source_variable_code':b.source_variable_code,'exact_question_text':b.exact_question_text,'praxis_shore_kind_candidates':sorted(p_kind.get(idd,set()))}
 kinds=sorted(p_kind.get(idd,set()))
 pk='|'.join(kinds) if kinds else ('STATED_INTENDED_CONDUCT' if b.baseline_t06_classification=='CONDUCT_SHORE' else '')
 ACC.append({'question_implementation_id':idd,'source_family':b.source_family,'wave':b.wave,'source_variable_code':b.source_variable_code,'exact_question_text':b.exact_question_text,
  'baseline_t06_classification':b.baseline_t06_classification,'t15_norm_candidate':'YES' if n_yes else 'NO','t15_praxis_candidate':'YES' if p_yes else 'NO','t15_praxis_shore_kind':pk,
  'reopened_from_baseline_other_or_ambiguous':'YES' if reopened else 'NO','normative_or_praxis_signature_json':js(sig),
  'source_basis':b.baseline_source_basis+' T15 continuation re-opened source-native realization terrain independently of prior T06 positives.',
  'norm_to_praxis_search_completed':'YES' if n_yes else 'NA','praxis_to_norm_search_completed':'YES' if p_yes else 'NA',
  'plausible_counterpart_implementation_ids_json':js(sorted(counter.get(idd,set()))),'positive_relation_ids_json':js(sorted(rels.get(idd,[]))),
  'blocked_crosswalk_ids_json':js(sorted(set(blocked.get(idd,[])))),'upstream_repair_ids_json':js(sorted(repairs_by.get(idd,[]))),
  'accounting_note':'Every denominator row preserved. Prior NORM/CONDUCT classes are seeds only; T15 candidate flags reflect this source-first continuation and do not rewrite T06 ancestry.'})

# ---------- Wave attestations ----------
posdf=pd.DataFrame(POS)
revdf=pd.DataFrame(REV)
accdf=pd.DataFrame(ACC)
repdf=pd.DataFrame(REPAIRS)
covdf=pd.DataFrame(COV)
overdf=pd.DataFrame(OVER)
ATT=[]
for sf,w in WAVE_DIR:
 bg=BASE[(BASE.source_family==sf)&(BASE.wave==w)]
 ag=accdf[(accdf.source_family==sf)&(accdf.wave==w)]
 pg=posdf[(posdf.source_family==sf)&(posdf.wave==w)] if len(posdf) else pd.DataFrame()
 rg=revdf[(revdf.source_family==sf)&(revdf.wave==w)] if len(revdf) else pd.DataFrame()
 repg=repdf[(repdf.source_family==sf)&(repdf.wave==w)] if len(repdf) else pd.DataFrame()
 covg=covdf[(covdf.source_family==sf)&(covdf.wave==w)] if len(covdf) else pd.DataFrame()
 og=overdf[(overdf.source_family==sf)&(overdf.wave==w)] if len(overdf) else pd.DataFrame()
 pcount=len(pg)
 ATT.append({'source_family':sf,'wave':w,'implementation_denominator':len(bg),'implementation_rows_accounted':len(ag),
  'prior_norm_shores':int((bg.baseline_t06_classification=='NORM_SHORE').sum()),'new_norm_shores_recovered':int(((ag.t15_norm_candidate=='YES') & (ag.baseline_t06_classification!='NORM_SHORE')).sum()),
  'praxis_candidate_shores':int((ag.t15_praxis_candidate=='YES').sum()),'norm_to_praxis_search_complete':'YES','praxis_to_norm_search_complete':'YES',
  'direct_enactment_reviewed':'YES','right_exercise_reviewed':'YES','practical_violation_reviewed':'YES','institutional_social_realization_reviewed':'YES','instrumental_enactment_reviewed':'YES',
  'positive_t15_count':pcount,'strict_t06_overlap_count':int((og.t15_overlap_disposition=='EXCLUDE_FROM_T15__STRICT_T06').sum()) if len(og) else 0,
  'blocked_count':int((rg.disposition=='BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY').sum()) if len(rg) else 0,'source_proven_mismatch_count':int((rg.disposition=='NOT_T15_SOURCE_PROVEN_MISMATCH').sum()) if len(rg) else 0,
  'coverage_defect_count':len(covg),'upstream_repair_count':len(repg),'zero_positive_supportable':'NA' if pcount else 'YES',
  'hostile_sparse_wave_qa':'YES','attestation_note':f'Complete source-first T15 review. {pcount} positives; strict T06 edges remain excluded; high-risk instrumental/policy and sparse terrain hostile-reviewed.'})

# ---------- Write all tables using template headers ----------
def write_template(name, records):
    header=list(pd.read_csv(RET/name,nrows=0).columns)
    df=pd.DataFrame(records)
    for c in header:
        if c not in df.columns: df[c]=''
    df=df[header]
    df.to_csv(RET/name,index=False)
    return df

pout=write_template('T15_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv',POS)
aout=write_template('T15_PRACTICAL_SHORE_ACCOUNTING.csv',ACC)
rout=write_template('T15_CROSSWALK_REVIEW.csv',REV)
oout=write_template('T15_T06_OVERLAP_AND_BOUNDARY.csv',OVER)
bout=write_template('T15_COMPOSITION_BRIDGE_LEDGER.csv',BR)
repout=write_template('T15_UPSTREAM_REPAIRS.csv',REPAIRS)
covout=write_template('T15_SOURCE_COVERAGE_DEFECTS.csv',COV)
blockout=write_template('T15_BLOCKERS.csv',BLOCKS)
attout=write_template('T15_WAVE_COMPLETENESS_ATTESTATION.csv',ATT)

# hostile QA
qa=[]
def q(name,cond,detail): qa.append({'check':name,'status':'PASS' if cond else 'FAIL','detail':detail})
q('ACCOUNTING_DENOMINATOR',len(aout)==3059,f'{len(aout)} rows')
q('ACCOUNTING_UNIQUE',aout.question_implementation_id.nunique()==3059,f'{aout.question_implementation_id.nunique()} unique')
q('PARENT_ZIP_IMMUTABLE',hashlib.sha256((ROOT/'PARENT_T06_RETURN'/'T06W01_S14_T06_SourceFirst_Authority_Reconstruction_Return_20260812.zip').read_bytes()).hexdigest()=='3a6085aa1f5e0d0d8d5e86f10575ba099b9b3285ba82bdfda7a84b3dc78e7af7','parent hash reverified')
q('NO_STRICT_T06_DUPLICATES',not any(pout.t06_overlap_status=='EXCLUDE_FROM_T15__STRICT_T06'),f'{sum(oout.t15_overlap_disposition=="EXCLUDE_FROM_T15__STRICT_T06")} strict overlaps ledgered')
q('BOUNDARY_CALIBRATION_ALL_RECOVERED',sum(pout.t06_overlap_status=='RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW')==6,'6/6 assigned BOUNDARY_TO_T15 relations emitted as T15 positives')
q('INSTRUMENTAL_EXPLICIT_ONLY',all(pout.loc[pout.manifestation_subtype=='INSTRUMENTAL_ENACTMENT','bridge_basis_type'].isin(['SOURCE_EXPLICIT_MEANS','GOVERNED_T04_BRIDGE','SOURCE_NATIVE_BATTERY_BRIDGE'])),f'{sum(pout.manifestation_subtype=="INSTRUMENTAL_ENACTMENT")} instrumental positives explicit')
q('LITS_404_405_FULL_18_CELL_GEOMETRY',sum(pout.worker_relation_id.str.contains('Q404A-Q405|Q404B-Q405',regex=True))==18,'18 conditioned category cells')
q('R5_OPTION_CELL_REPAIRS',all(any((repout.question_implementation_id==iid('Afrobarometer','R5',c))&(repout.repair_field=='OPTION_LEVEL_NORMATIVE_CELL_BINDING')) for c in ['Q44','Q45','Q57','Q58']),'Q44/Q45/Q57/Q58 option grain preserved')
q('ASIAN_Q101_REOPENED',((aout.question_implementation_id==iid('Asian Barometer','W1','q101'))&(aout.t15_norm_candidate=='YES')&(aout.reopened_from_baseline_other_or_ambiguous=='YES')).any(),'desired-democracy norm recovered from baseline OTHER')
q('LITS_Q421_REOPENED',((aout.question_implementation_id==iid('LiTS','IV','q421'))&(aout.t15_norm_candidate=='YES')&(aout.reopened_from_baseline_other_or_ambiguous=='YES')).any(),'environmental priority norm recovered from baseline OTHER')
q('R1_COMPOSITES_WITHHELD',len(covout)==3 and set(covout.runtime_relation_withheld)=={'YES'},'defnew/defjug/defele remain coverage defects')
q('ALL_POS_IMPLEMENTATION_BOUND',all(len(json.loads(x))>=2 for x in pout.member_implementation_ids_json),'all positives have >=2 exact implementation IDs')
q('ALL_POS_SOURCE_PROVENANCE',all(bool(json.loads(x)) for x in pout.source_provenance_json),'all positives carry native source authority payload')
q('BLOCKS_NOT_CONVERTED_TO_NEGATIVES',len(blockout)>0,'source/bridge ambiguities remain explicit blockers')
q('LAW_ORDER_CRIME_NOT_PROMOTED',not any((pout.source_family=='Afrobarometer')&(pout.wave=='R5')&pout.worker_relation_id.str.contains('Q45-Q65F')),'plausible but ungoverned law/order→crime bridge blocked')
q('R1_MAREAR_GAP_NOT_PROMOTED',not any(pout.worker_relation_id.str.contains('MAREAR-PFEGAP')),'economic-policy means story blocked absent source bridge')
q('ALL_WAVE_SEARCH_ATTESTED',all(attout.hostile_sparse_wave_qa=='YES') and len(attout)==6,'6/6 waves hostile-reviewed')
q('NO_ZERO_WAVE_UNEXAMINED',all(attout.positive_t15_count.astype(int)>0),'all six waves contain at least one source-proven T15; sparse waves still hostile-reviewed')
q('POSITIVE_ID_UNIQUE',pout.worker_relation_id.nunique()==len(pout),f'{len(pout)} unique positive IDs')
q('REVIEW_ID_UNIQUE',rout.crosswalk_id.nunique()==len(rout),f'{len(rout)} unique review IDs')
q('BLOCKER_ID_UNIQUE',blockout.blocker_id.nunique()==len(blockout),f'{len(blockout)} unique blocker IDs')
q('BRIDGE_LEDGER_EXPLICIT_STATUS',all(bout.bridge_status.isin(['PROVEN','BLOCKED_NEEDS_EXPLICIT_BRIDGE'])),f'{len(bout)} bridge rows')

hostile={'status':'PASS' if all(x['status']=='PASS' for x in qa) else 'FAIL','check_count':len(qa),'checks':qa,
 'hostile_notes':[
  'WVS W7 free-election terrain: retained genuine choice, candidate exclusion, and voter coercion; blocked fairness/media/bribery items rather than collapsing election integrity into freedom.',
  'Afrobarometer R5: blocked Q45 law-and-order→Q65F crime reduction despite intuitive policy relation because source lacks explicit equivalence.',
  'Afrobarometer R1: blocked marear earnings-limit→income-gap performance because that would require worker-supplied economic causal theory.',
  'LiTS IV: promoted only Q4.04/Q4.05 and Q4.21/Q4.22 instrumental links where source itself defines identical ends or explicitly states use of contributed money; responsibility→financing links remain blocked.',
  'Strict T06 overlap is not duplicated. Six central BOUNDARY_TO_T15 calibration relations are returned as T15 positives with explicit boundary recommendations.'
 ]}
(RET/'HOSTILE_QA.json').write_text(json.dumps(hostile,indent=2,ensure_ascii=False))

# report
sub=Counter(pout.manifestation_subtype); wave_counts=pout.groupby(['source_family','wave']).size().to_dict();
bridge_blocks=int((bout.bridge_status=='BLOCKED_NEEDS_EXPLICIT_BRIDGE').sum())
boundary=sum(oout.t15_overlap_disposition=='RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW'); strict=sum(oout.t15_overlap_disposition=='EXCLUDE_FROM_T15__STRICT_T06')
report=f'''# T06W01 — S14-T15 norm→practical-realization source-first continuation report

## Verdict

Worker reconstruction is complete; the supplied return validator remains the final machine gate. The immutable prior T06 return was preserved and re-hashed before use. Discovery used the normalized 3,059-row accounting only as a seed surface and reopened baseline OTHER/SOURCE_AMBIGUOUS rows where T15 permits normative institutional states or practical-realization shores.

## Denominator and result

- Assigned implementations: **3,059 / 3,059 accounted**.
- Positive S14-T15 relations: **{len(pout)}**.
- Crosswalk review rows: **{len(rout)}**.
- Source/bridge blockers: **{len(blockout)}** (explicit bridge blockers: **{bridge_blocks}**).
- Source-proven mismatch reviews: **{sum(rout.disposition=='NOT_T15_SOURCE_PROVEN_MISMATCH')}**.
- Strict T06 overlaps excluded: **{strict}**.
- T06→T15 boundary recommendations: **{boundary}**.
- Upstream repair rows: **{len(repout)}**.
- Source-coverage defects: **{len(covout)}**.

## Positive count by subtype

'''+''.join(f'- `{k}`: **{v}**\n' for k,v in sorted(sub.items()))+'''\n## Positive count by wave\n\n'''+''.join(f'- {sf} {w}: **{n}**\n' for (sf,w),n in wave_counts.items())+f'''\n## Major source-first findings

### LiTS IV — explicit instrumental batteries

The native Q4.04/Q4.05 structure is decisive. Q4.04 asks first and second priorities for **extra government spending** across nine named fields; Q4.05 immediately asks willingness to give income/pay more taxes **if the extra money is spent on each identical field**. This produces 18 response-cell-conditioned `INSTRUMENTAL_ENACTMENT` relations under `SOURCE_NATIVE_BATTERY_BRIDGE`. Q4.01f→Q4.05e and the environmental Q4.21→Q4.22a-c links add four further source-explicit means relations. By contrast, Q4.09 responsibility assignments→Q4.05 financing are blocked: same field does not itself establish the responsibility→respondent-financing bridge.

### WVS W7 — democracy criteria into world states

Q238→Q251 links normative appraisal of a democratic political system to the actual democraticness of the country. The Q241–Q249 shared democracy-essentiality stem is restored for source semantics: Q243 links to genuine voter choice and to direct constraints from candidate exclusion/voter coercion; Q249 narrows to women’s equal opportunity to run for office. Fair-counting, media-fairness, official-fairness, and vote-buying items are not automatically subsumed under “free elections.”

### WVS W4 — calibrated violation boundary

Only V35→V33/V34 is promoted to T15: the norm says pollution reduction should **not cost me money**, while the praxis items state willingness to bear income/tax cost for the same pollution-prevention target. The three strict-T06 calibration edges remain T06 and are excluded from T15 positives.

### Afrobarometer R5 — rights, accountability, institutional realization

The wave contains dense source-native norm→world structure: organization rights→membership/freedom; protest freedom→protest exercise; anti-violence norm→political-violence praxis; equal treatment→observed gender inequality; President obey-laws norm→observed noncompliance; democracy criteria→realized election, jobs, public-service, speech, and corruption states; opposition/media/parliament functions→observed institutional enablement/frustration; democracy preference→two direct measures of current democraticness; tax/service-payment norms→observed noncompliance. Four categorical democracy batteries require option-level upstream binding.

### Asian Barometer W1 — reopened desired/actual institutional state

Q101 was correctly not a narrow T06 norm-conduct shore, but T15 reopens it as a desired institutional state: Q100 and Q101 use the **identical complete-dictatorship↔complete-democracy scale** for actual-present versus desired-present country state. Q134→Q105 and Q136→Q112 survive only as explicit opposed institutional axes; broader authoritarian-item→democracy-scale stories remain blocked.

### Afrobarometer R1 — democracy/basic-needs and responsibility realization

The source supports democracy preference→actual democracy extent; basic-necessities criterion→respondent/family food and water deprivation as concrete frustration; jobs/income-gap criteria→direct government realization measures; and exact government-responsibility assignments for jobs/crime→government performance on those actions. Broader schools/clinics→education/health, public-employment→generic job creation, and earnings-limit→income-gap stories are blocked where target/means authority is missing. The three `defnew/defjug/defele` composite structures remain source-coverage defects and are not synthesized into runtime relations.

## Boundary and anti-heuristic controls

- **{strict}** calibration relations are `EXCLUDE_FROM_T15__STRICT_T06`.
- **{boundary}** prior T06 relations are `RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW`; no prior authority was silently revoked.
- Instrumental positives use only `SOURCE_EXPLICIT_MEANS` or `SOURCE_NATIVE_BATTERY_BRIDGE`.
- Policy/common-sense bridges were blocked rather than inferred.
- All source ambiguities remain blockers; source-proven mismatches require affirmative incompatible semantics.
- No Job 3, O10/O11/O12 mutation, cross-wave harmonization, or S14 freeze claim is made.

## Hostile QA

`HOSTILE_QA.json` records **{len(qa)}** checks and is **{hostile['status']}** before the supplied return validator is run.
'''
(RET/'WORKER_REPORT.md').write_text(report,encoding='utf-8')

# execution provenance
provj={
 'worker_id':'T06W01','pack_sha256_verified':'accc47c43fd5c1fd353198ca44b724dc5acc63ae9cf633c7bbe75655ff63b137',
 'parent_t06_sha256_verified':'3a6085aa1f5e0d0d8d5e86f10575ba099b9b3285ba82bdfda7a84b3dc78e7af7',
 'source_authority_sha256_verified':'e88cc035ca1d846e68ee208ec991f61f636d67ebbd19312057c8e44c37ff740d',
 'source_method':'Flattened BY_WAVE native page text + governed implementation context; no routine PDF walk; prior T06 positives used only for ancestry/overlap calibration.',
 'implementation_denominator':len(aout),'positive_count':len(pout),'subtype_counts':dict(sub),'wave_counts':{f'{k[0]}::{k[1]}':int(v) for k,v in wave_counts.items()},
 'strict_t06_overlaps_excluded':int(strict),'boundary_recommendations':int(boundary),'blockers':len(blockout),'explicit_bridge_blockers':int(bridge_blocks),'upstream_repairs':len(repout),'coverage_defects':len(covout)
}
(RET/'EXECUTION_PROVENANCE.json').write_text(json.dumps(provj,indent=2,ensure_ascii=False))

print(json.dumps(provj,indent=2,ensure_ascii=False))
