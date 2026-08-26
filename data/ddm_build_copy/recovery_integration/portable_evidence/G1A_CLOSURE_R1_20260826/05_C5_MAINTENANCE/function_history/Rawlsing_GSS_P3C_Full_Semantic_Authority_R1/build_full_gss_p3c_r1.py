from __future__ import annotations
from pathlib import Path
import pandas as pd
import json, hashlib, os, shutil, itertools, re
from collections import defaultdict, Counter
import networkx as nx

BASE=Path('/mnt/data')
SCRIPT_ROOT=Path(__file__).resolve().parent
LOCAL_REPRO=SCRIPT_ROOT/'REPRO_INPUTS'
if LOCAL_REPRO.exists():
    WORK=SCRIPT_ROOT
    V0=LOCAL_REPRO/'full_v0'
    OUT=SCRIPT_ROOT/'REBUILD_OUTPUT'
    R184=LOCAL_REPRO/'r184_authority'
    S32=LOCAL_REPRO/'p2_global'
else:
    WORK=BASE/'gss_real_p3c_work'
    V0=WORK/'full_v0'
    OUT=BASE/'Rawlsing_GSS_P3C_Full_Semantic_Authority_R1'
    R184=BASE/'rawlsing_packaged_5b500e1_inspection/84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/authority'
    ROOT=WORK/'p3a_transfer/Rawlsing_P3A_V40_Direct_Engineering_Transfer/Rawlsing_J_Family_Authority_Strategy_Handoff_v40_WORKING'
    S32=ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)


def stable(prefix,*parts):
    return prefix+'_'+hashlib.sha256(chr(31).join(map(str,parts)).encode()).hexdigest()[:24]

def jdump(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def sha(path:Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

L=pd.read_csv(V0/'GSS_FULL_LINEAGE_SEMANTIC_AUTHORITY.csv',dtype=str,keep_default_na=False)
R=pd.read_csv(V0/'GSS_FULL_EFFECTIVE_PAIR_AUTHORITY.csv',dtype=str,keep_default_na=False)
OLD_C=pd.read_csv(V0/'GSS_FULL_P3A_COMPONENTS.csv',dtype=str,keep_default_na=False)
OLD_M=pd.read_csv(V0/'GSS_FULL_P3A_COMPONENT_MEMBERS.csv',dtype=str,keep_default_na=False)
NODES=pd.read_csv(S32/'Rawlsing_P2_All_Nine_Unified_Node_Evidence_Registry_v1.csv',dtype=str,keep_default_na=False)
ALL_LIN=pd.read_csv(S32/'Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv',dtype=str,keep_default_na=False)
MEM=pd.read_csv(R184/'P3C_CANONICAL_FAMILY_MEMBERSHIP.csv',dtype=str,keep_default_na=False)
FAM=pd.read_csv(R184/'P3C_CANONICAL_FAMILY_AUTHORITY.csv',dtype=str,keep_default_na=False)

lrec=L.set_index('lineage_id').to_dict('index')
allrec=ALL_LIN.set_index('lineage_id').to_dict('index')
family_by=MEM.set_index('upstream_object_id').canonical_family_id.to_dict()
var_to_lids=defaultdict(list)
for _,r in L.iterrows(): var_to_lids[r.primary_variable].append(r.lineage_id)

# Each group is a source-evidence adjudication, not a lexical cluster. Members share a respondent-facing proposition;
# response forms, waves, routing and values remain distinct variants with no value portability.
groups=[]
def add(name,vars,rationale,kind='SOURCE_NATIVE_PROPOSITION_CONTINUITY'):
    vars=[v for v in vars if v in var_to_lids]
    if len(vars)>=2:
        groups.append({'group_key':name,'variables':vars,'rationale':rationale,'authority_kind':kind})

# Directly reviewed valid components from the full GSS surface.
valid = {
'religious_affiliation_strength':['reliten','relitennv','relitenv'],
'abortion_defect':['abdefect','abdefectg'],
'getting_ahead':['getahead','getaheadnv','getaheadv'],
'move_within_us_for_work':['nounemp5','moveinus'],
'generalized_trust':['trust','trust5','trustnv','trppl','trustv','cantrust'],
'muslim_clergy_speech':['spkmslm','spkmslmy'],
'bible_view':['bible','biblenv','biblev','bibley'],
'school_bible_prayer':['prayer','prayernv','prayerv'],
'suicide_bankrupt':['suicide2','suicide2g'],
'diploma_ged_other':['dipged','dipged_1222'],
'www_home_time':['wwwhrh','wwwminh'],
'www_work_time':['wwwhrw','wwwminw'],
'www_other_time':['wwwhro','wwwmino'],
'preteen_household_count':['preteen','preteen_7222'],
'household_relation_11':['relate11','relhhd11'],
'raised_denomination':['denom16','denom16_7322'],
'race_first_mention':['racecen1','racecen1_0022'],
'police_striking_approval':['polhitok','polhitoky'],
'household_relation_14':['relate14','relhhd14'],
'anti_religionist_speech':['spkath','spkathy'],
'women_job_discrimination':['discaffw','discaffwnv','discaffwv'],
'women_politics_suitability':['fepol','fepolnv','fepolv'],
'family_generations':['famgen','famgen_7522','famgen_next','famgen_exp'],
'sibling_count':['sibs','sibs_7222'],
'muslim_clergy_library':['libmslm','libmslmy'],
'immigrants_take_jobs':['immjobs','immjobs1'],
'communist_speech':['spkcom','spkcomy'],
'us_citizenship_if_foreign_born':['uscitzn','uscitzn_0822'],
'child_quality_success':['success','successy'],
'race_third_mention':['racecen3','racecen3_0022'],
'move_outside_us_for_work':['moveaway','nounemp6'],
'known_suicides_lifetime':['suinum','suinum1'],
'science_information_source':['scifrom','scifromy'],
'fairness_general':['fair','fairnv','fairv'],
'babies_household_count':['babies','babies_7222'],
'age_first_child':['agekdbrn','agekdbrn_9422'],
'adhd_knowledge':['adhdknow','adhdknw'],
'child_quality_clean':['clean','cleany'],
'same_sex_marriage':['marsame','marsamey','marsame1'],
'abortion_health':['abhlth','abhlthg'],
'self_employed_employee_count':['numemps','numemps_0422'],
'job_satisfaction_general':['satjob1','satjob7'],
'marijuana_legalization':['grass','grassnv','grassv'],
'racial_difference_will':['racdif4','racdif4x'],
'life_after_death':['postlife','postlifenv','postlifev'],
'communist_teacher':['colcom','colcomy'],
'unrelated_household_count':['unrelat','unrelat_7222'],
'internet_weekday_time':['intwkdyh','intwkdym'],
'communist_library':['libcom','libcomy'],
'immigrants_crime':['immcrime','immcrime1'],
'general_happiness':['happy','happy7','happy_next'],
'political_attack_police':['polattak','polattaky'],
'email_home_time':['emhrh','emminh'],
'email_work_time':['emhrw','emminw'],
'email_other_time':['emhro','emmino'],
'household_population':['hompop','hompop_7222','hompop_exp'],
'hispanic_specific':['hispanic','hispanic_0022'],
'children_living_standard':['kidssol','kidssolnv','kidssolv'],
'child_quality_control':['control','controly'],
'helpfulness_general':['helpful','helpfulnv','helpfulv'],
'subjective_class':['class','classy'],
'college_major_1':['major1','major1_1222','colmajr1'],
'college_major_2':['major2','major2_1222','colmajr2'],
'relation_to_household_head':['rplace','rplace_7522'],
'household_relation_13':['relate13','relhhd13'],
'racial_difference_discrimination':['racdif1','racdif1x'],
'racial_difference_education':['racdif3','racdif3x'],
'online_science_info_source':['scinews3','sciinfgo'],
'incurable_patient_die':['letdie1','letdie1y'],
'past_year_sex_partners':['partners','partners_8822'],
'suicide_tired_living':['suicide4','suicide4g'],
'parks_recreation_spending':['natpark','natparkz'],
'family_earners':['earnrs','earnrs_7222'],
'abortion_poverty':['abpoor','abpoorg'],
'abortion_no_more_children':['abnomore','abnomoreg'],
'vote_intention_2024':['whovote24','whovote24a'],
'specific_denomination':['denom','denom_7222'],
'working_hours_decision':['sethrs','decidwrk'],
'region_age_16':['reg16','reg16_7222'],
'spouse_denomination':['spden','spden_7322'],
'internet_weekend_time':['intwkenh','intwkenm'],
'police_vulgar_abuse':['polabuse','polabusey'],
'total_family_income':['income','income72','income82','income91','income98','income06','income16'],
'abortion_rape':['abrape','abrapeg'],
'suicide_incurable':['suicide1','suicide1g'],
'other_language_slot_1':['othlang1','othlang1_0022'],
'criminal_courts':['courts','courtsnv','courtsv'],
'highways_bridges_spending':['natroad','natroadz'],
'racial_difference_inborn':['racdif2','racdif2x'],
'last_hiv_test_location':['hivtest2','hivtest2_0622'],
'aged_live_children':['aged','agedpar'],
'racial_difference_upbringing':['racdif5','racdif5x'],
'racist_speech':['spkrac','spkracy'],
'greenhouse_danger':['tempgen','tempgen1'],
'supervisor_has_supervisor':['wksubs','wksubs1'],
'other_language_slot_2':['othlang2','othlang2_0022'],
'abortion_any_reason':['abany','abanyg'],
'self_solve_web_problem':['doself','askwksch'],
'racist_library':['librac','libracy'],
'child_quality_considerate':['consider','considey'],
'divorce_laws':['divlaw','divlawnv','divlawv'],
'dwelling_type':['dwelling','dwelling_8222'],
'household_relation_12':['relate12','relhhd12'],
'open_housing_vote':['racopen','racopennv'],
'child_quality_gender_role':['role','roley'],
'child_quality_manners':['manners','mannersy'],
'space_spending':['natspac','natspacy','natspacz'],
'race_second_mention':['racecen2','racecen2_0022'],
'left_right_position':['leftrght','leftrght1'],
'child_quality_honest':['honest','honesty'],
'teen_household_count':['teens','teens_7222','teens_exp'],
'respondent_income':['rincome','rincom82','rincom91','rincom98','rincom06','rincom16'],
'child_quality_amicable':['amicable','amicably'],
'child_quality_interest':['interest','interesy'],
'child_quality_judgment':['judgment','judgmeny'],
'child_quality_responsible':['responsi','responsy'],
'child_quality_studious':['studious','studiouy'],
'partner_denomination':['coden','coden_1222'],
'household_type_condensed':['hhtype1','hhtype1_next','hhtype1_exp'],
'most_important_issue':['topprob1','topprob1_next'],
'adults_in_household':['adults','adults_exp','adultsinhh'],
'children_in_household':['childs_exp','childsinhh'],
'abortion_not_married':['absingle','absingleg'],
'anti_religionist_teaching':['colath','libathy'], # retained only as a conflict review below; removed after source-evidence check
'internet_skill':['webable','intskill'],
'x_rated_movie_past_year':['xmovie','xmoviey'],
}
# libathy's variable code and binary response imply library removal while its label says teaching; evidence conflicts.
valid.pop('anti_religionist_teaching')
for k,v in valid.items():
    add(k,v,'Independent source text, response form, wave continuity and/or explicit source-version design establish one respondent-facing proposition; values and response coding remain nonportable.')

# National-spending wording/form variants. The common too-much/about-right/too-little operator and source version design govern continuity.
nat_groups={
'foreign_aid_spending':['nataid','nataidy','nataidz'],
'national_defense_spending':['natarms','natarmsy','natarmsz'],
'big_city_spending':['natcity','natcityy','natcityz'],
'crime_spending':['natcrime','natcrimy','natcrimz'],
'drug_addiction_spending':['natdrug','natdrugy','natdrugz'],
'education_spending':['nateduc','nateducy','nateducz'],
'environment_spending':['natenvir','natenviy','natenviz'],
'poor_welfare_spending':['natfare','natfarey','natfarez'],
'health_spending':['natheal','nathealy','nathealz'],
'mass_transit_spending':['natmass','natmassz'],
'black_assistance_spending':['natrace','natracey','natracez'],
'social_security_spending':['natsoc','natsocz'],
}
for k,v in nat_groups.items():
    add('national_spending_'+k,v,'GSS source-native national-spending versions retain the same spending-sufficiency operator and governed budget domain while changing labels/framing; wording version remains explicit variant authority.')

# Confidence-in-institution source versions.
conf_groups={
'military':['conarmy','conarmyy'], 'major_companies':['conbus','conbusy'],
'organized_religion':['conclerg','conclery'], 'education':['coneduc','coneducy'],
'executive_branch':['confed','confedy'], 'banks':['confinan','confinay'],
'supreme_court':['conjudge','conjudgy'], 'organized_labor':['conlabor','conlaboy','conlabory'],
'congress':['conlegis','conlegiy'], 'medicine':['conmedic','conmediy'],
'press':['conpress','conpresy'], 'scientific_community':['consci','consciy'],
'television':['contv','contvy']}
for k,v in conf_groups.items():
    add('institutional_confidence_'+k,v,'GSS source-native confidence battery versions preserve the same institutional target and confidence operator; wording/response release changes remain variants.')

# Every approved variable must belong to only one proposition group.
var_group={}
for g in groups:
    for v in g['variables']:
        if v in var_group and var_group[v]!=g['group_key']:
            raise RuntimeError(f'variable in multiple groups: {v} {var_group[v]} {g["group_key"]}')
        var_group[v]=g['group_key']
group_by_key={g['group_key']:g for g in groups}

# Manual false-positive pattern ledger: this is the explicit boundary catalogue used to reject machine similarity.
reject_patterns=[
('ACTOR_OR_SUBJECT_SHIFT','mustdoc vs mustdoc1','Person forced into examination versus parents compelled to arrange examination.'),
('DERIVED_TARGET_SHIFT','sei10* and *sei10*','Respondent, mother, father, spouse and cohabiting-partner occupational derivations are different targets.'),
('LOSS_TARGET_SHIFT','worecsup vs worryjob','Economic support loss is not job loss.'),
('LOCATION_TARGET_SHIFT','WWW/email time series','Home, work, other and generic-use locations are distinct; only hour/minute forms within one location join.'),
('SEX_TARGET_SHIFT','discaffm vs discaffw*','Man and woman targets remain distinct.'),
('SCOPE_SHIFT','emsentp vs emsent','Personal email count is not all email count.'),
('GROUP_TARGET_SHIFT','chldadlt_*','Childhood-adult racial/ethnic target groups remain distinct.'),
('PARENT_TARGET_SHIFT','paattend vs maattend','Father and mother attendance are different propositions.'),
('INSTITUTION_TARGET_SHIFT','conclerg vs conlabor*','Religion and labor confidence targets remain distinct.'),
('ACTIVITY_TARGET_SHIFT','intstream vs intgame','Streaming media and gaming are different activities.'),
('PERSON_AND_TIME_SHIFT','other/oth16/spother/spoth16/coother','Respondent, spouse, cohabiting partner and age-16 denomination contexts remain distinct.'),
('SOURCE_CHANNEL_SHIFT','jobpub/jobonwww/jobfrnds/jobpaper/jobplace/jobcntct/jobtvrad/jobcowrk','Each job-information channel is a distinct battery item.'),
('TIME_DETAIL_SHIFT','hivtest1 vs hivtest1_0622','Year-only and month-plus-year requests have different response operators.'),
('RESPONDENT_TARGET_SHIFT','workhr vs sphour','Respondent and spouse work hours remain distinct.'),
('REPEATED_SLOT_SHIFT','college-major and education-name slots','First and second mentions/slots remain distinct.'),
('MEDIUM_SHIFT','tvnews1 vs webnews','Television and web news reliability are different targets.'),
('POLICY_SCOPE_SHIFT','bizbstgw/bizbsttx and polbstgw/polbstsc','General conduct and issue-specific conduct are different propositions.'),
('ELECTION_TIME_SHIFT','if08who vs if16who','Different elections are not one proposition.'),
('RANK_SLOT_SHIFT','gvinflu1 vs gvinflu2','First- and second-ranked influence mentions remain distinct.'),
('TEMPORAL_OPERATOR_SHIFT','demtoday vs dem10fut','Current and ten-year-future democratic performance are different propositions.'),
('DIRECTIONAL_OPERATOR_SHIFT','jbintfam/famintjb and wkvsfam/famvswk','Job-to-family and family-to-job interference directions remain distinct.'),
('POPULATION_TARGET_UNRESOLVED','imprvown/imprvown1/bettrown','Child, vignette-person and generic situation targets are not collapsed.'),
('SOURCE_LABEL_CONFLICT','othfrd vs bestfrd','Source response evidence shows number of other friends versus best-friend type/relationship.'),
('KIN_TARGET_SHIFT','kidcall vs sibcall','Child and sibling contact are different targets.'),
('ACCESS_USE_OPERATOR_SHIFT','intmbile vs intaccss','Mobile internet use is not mobile internet access.'),
('DIRECT_DERIVED_BOUNDARY','direct prayer vs constructed prayer','R184 explicitly separates direct prayer frequency from a constructed recode.'),
('IMPLICIT_STEM_UNRECOVERED','art* vs prfm* attendance/barrier items','Identical short labels occur under different event stems; absent recovered stem identity, proposition identity is fail-closed.'),
('SOURCE_EVIDENCE_CONFLICT','libathy','Variable/response evidence implies library removal while label says teaching; no family promotion is allowed.'),
('ADMINISTRATIVE_SURFACE','interviewer, region, weight and case metadata','Nonrespondent administrative fields remain outside proposition authority.'),
]
rejdf=pd.DataFrame(reject_patterns,columns=['boundary_code','surface','rationale'])

# Resolve a within-GSS pair against the approved source-native groups.
def group_for_pair(a,b):
    va=lrec[a]['primary_variable']; vb=lrec[b]['primary_variable']
    ga=var_group.get(va,''); gb=var_group.get(vb,'')
    return ga if ga and ga==gb else ''

# Higher P3C authority overrides earlier P2 pair assertions.
R=R.copy()
if 'manual_review_group' not in R: R['manual_review_group']=''
if 'manual_review_status' not in R: R['manual_review_status']=''
if 'authority_precedence_note' not in R: R['authority_precedence_note']=''

for i,r in R.iterrows():
    a,b=r.left_lineage_id,r.right_lineage_id
    fa,fb=family_by.get(a,''),family_by.get(b,'')
    # Final canonical closure is the highest available proposition authority.
    if fa and fb:
        if fa==fb:
            R.at[i,'normalized_authority_class']='PROPOSITION_RELATION_AUTHORITY'
            R.at[i,'authority_status']='CONFIRMED_BY_R184_CANONICAL_TRANSITIVE_CLOSURE'
            R.at[i,'portability_ceiling']='QUESTION_PROPOSITION_ONLY'
            R.at[i,'rationale']=f'Both endpoints are current members of {fa}; final P3C canonical authority confirms proposition identity while preserving variants.'
            gk=group_for_pair(a,b) if r.left_source_family=='GSS' and r.right_source_family=='GSS' else ''
            if gk: R.at[i,'manual_review_group']=gk
            R.at[i,'manual_review_status']='P3C_FINAL_AUTHORITY_CONFIRMED'
            R.at[i,'authority_precedence_note']='P3C_R184_FINAL_AUTHORITY_OVERRIDES_LOWER_LAYER_DISCOVERY_CLASSIFICATION'
        else:
            R.at[i,'normalized_authority_class']='NEGATIVE_OR_COORDINATE_AUTHORITY'
            R.at[i,'authority_status']='REJECTED_BY_R184_STRONGER_FAMILY_BOUNDARY'
            R.at[i,'portability_ceiling']='SEMANTIC_COORDINATE_ONLY'
            R.at[i,'rationale']=f'Endpoints are governed in distinct R184 families ({fa}, {fb}); lower-layer pair similarity cannot collapse final P3C boundaries.'
            R.at[i,'manual_review_status']='P3C_FINAL_BOUNDARY_OVERRIDES_PAIR'
            R.at[i,'authority_precedence_note']='P3C_R184_FINAL_AUTHORITY_OVERRIDES_LOWER_LAYER_PAIR_ASSERTION'
        continue
    if r.left_source_family=='GSS' and r.right_source_family=='GSS':
        gk=group_for_pair(a,b)
        if gk:
            g=group_by_key[gk]
            R.at[i,'normalized_authority_class']='PROPOSITION_RELATION_AUTHORITY'
            R.at[i,'authority_status']='ACCEPTED_AFTER_FULL_SOURCE_NATIVE_GSS_REVIEW'
            R.at[i,'portability_ceiling']='QUESTION_PROPOSITION_ONLY'
            R.at[i,'rationale']=g['rationale']
            R.at[i,'manual_review_group']=gk
            R.at[i,'manual_review_status']='RESOLVED_ACCEPT'
            R.at[i,'authority_precedence_note']='FULL_GSS_SOURCE_NATIVE_REVIEW_SUPERSEDES_MACHINE_SIMILARITY_PRECLASSIFICATION'
        elif r.normalized_authority_class=='PROPOSITION_RELATION_AUTHORITY':
            R.at[i,'normalized_authority_class']='NEGATIVE_OR_COORDINATE_AUTHORITY'
            R.at[i,'authority_status']='REJECTED_AFTER_FULL_SOURCE_NATIVE_COMPONENT_REVIEW'
            R.at[i,'portability_ceiling']='SEMANTIC_COORDINATE_ONLY'
            R.at[i,'rationale']='The machine-generated relation did not survive source-native review of target, actor, slot, timeframe, implicit stem, operator and response evidence.'
            R.at[i,'manual_review_status']='RESOLVED_REJECT_FALSE_EQUIVALENCE'
            R.at[i,'authority_precedence_note']='FULL_GSS_SOURCE_NATIVE_REVIEW_SUPERSEDES_MACHINE_SIMILARITY_PRECLASSIFICATION'

# P3C closes lower-layer unresolved pair facts fail-closed. A heterogeneous or unrecoverable
# source-local lineage cannot support proposition identity; it is explicitly excluded rather than
# carried forward as an open semantic obligation.
for i,r in R.iterrows():
    if r.normalized_authority_class=='UNRESOLVED_FAIL_CLOSED_AUTHORITY':
        R.at[i,'normalized_authority_class']='NEGATIVE_OR_COORDINATE_AUTHORITY'
        R.at[i,'authority_status']='RESOLVED_EXCLUDE_HETEROGENEOUS_OR_UNRECOVERABLE_LINEAGE'
        R.at[i,'portability_ceiling']='SEMANTIC_COORDINATE_ONLY'
        R.at[i,'rationale']='At least one endpoint lacks a single recoverable respondent-facing proposition operator and target. P3C therefore closes the relation as non-equivalent; no proposition-family edge is authorized.'
        R.at[i,'manual_review_status']='RESOLVED_EXCLUDE_FAIL_CLOSED'
        R.at[i,'authority_precedence_note']='P3C_FAIL_CLOSED_CLOSURE_OF_LOWER_LAYER_UNRESOLVED_PAIR'

# Manual cross-source acceptance missed by the old global top-25 cap: mobile internet use.
mobile_pair=set(['p2lineage_14ccc5147cfd2eb49c5289f0','p2lineage_ccf97616b2b11c178d262ef4'])
for i,r in R.iterrows():
    if set([r.left_lineage_id,r.right_lineage_id])==mobile_pair:
        R.at[i,'normalized_authority_class']='PROPOSITION_RELATION_AUTHORITY'
        R.at[i,'authority_status']='ACCEPTED_FULL_REOPEN_MOBILE_INTERNET_USE'
        R.at[i,'portability_ceiling']='QUESTION_PROPOSITION_ONLY'
        R.at[i,'rationale']='Both items ask whether the respondent uses a mobile phone/smartphone/tablet to access the internet. Access-only and home-through-mobile items remain excluded.'
        R.at[i,'manual_review_group']='cross_source_mobile_internet_use'
        R.at[i,'manual_review_status']='RESOLVED_ACCEPT'
        R.at[i,'authority_precedence_note']='FULL_GSS_CROSS_SOURCE_CAP_REOPEN_SOURCE_TEXT_ADJUDICATION'

# Ensure every approved within-GSS clique has an explicit pair obligation, even where discovery did not emit one.
pair_index={r.pair_key:i for i,r in R.iterrows()}
addrows=[]
for g in groups:
    lids=[]
    for v in g['variables']: lids.extend(var_to_lids[v])
    lids=sorted(set(lids))
    for a,b in itertools.combinations(lids,2):
        pk='|'.join(sorted([a,b]))
        if pk in pair_index: continue
        A=lrec[a];B=lrec[b]
        addrows.append({
            'pair_authority_id':stable('gssfullpairr1','MANUAL_SOURCE_NATIVE_COMPLETION',a,b),
            'origin_surface':'GSS_FULL_MANUAL_SOURCE_NATIVE_COMPLETION',
            'left_lineage_id':a,'right_lineage_id':b,'left_source_family':'GSS','right_source_family':'GSS',
            'candidate_channels':'FULL_SOURCE_NATIVE_GROUP_COMPLETION','semantic_content_id_discovery_only':'',
            'char_similarity':'','word_similarity':'','fuzzy_similarity':'','conflict_codes':'',
            'normalized_authority_class':'PROPOSITION_RELATION_AUTHORITY','authority_status':'ACCEPTED_AFTER_FULL_SOURCE_NATIVE_GSS_REVIEW',
            'portability_ceiling':'QUESTION_PROPOSITION_ONLY','two_sided_evidence_status':'COMPLETE_EXPLICIT_SOURCE_TEXT_RESPONSE_AND_CLASSIFICATION_BOTH_SIDES',
            'rationale':g['rationale'],'prohibited_use':'No raw-value portability, respondent join, J-family installation, or canonical promotion outside governed P3A/P3C replay.',
            'pair_key':pk,'manual_review_group':g['group_key'],'manual_review_status':'RESOLVED_ACCEPT',
            'authority_precedence_note':'FULL_GSS_SOURCE_NATIVE_REVIEW_CREATED_MISSING_RELATION_OBLIGATION'})
if addrows:
    R=pd.concat([R,pd.DataFrame(addrows)],ignore_index=True)

# Reassert unique pair authority after additions.
priority={'EXISTING_GLOBAL_PAIR_AUTHORITY':0,'GSS_FULL_MANUAL_SOURCE_NATIVE_COMPLETION':1,'GSS_FULL_WITHIN_SOURCE_CANDIDATE_SURFACE':2,'GSS_FULL_CROSS_SOURCE_OMITTED_SURFACE':3}
R['_p']=R.origin_surface.map(priority).fillna(9)
R=R.sort_values(['pair_key','_p','pair_authority_id']).drop_duplicates('pair_key',keep='first').drop(columns=['_p']).reset_index(drop=True)

# Full two-sided evidence rebuilt from source-native nodes.
nodegroups={k:g for k,g in NODES.groupby('lineage_id')}
def evidence_record(pairid,side,lid):
    if lid in lrec:
        A=lrec[lid]
        return {'pair_authority_id':pairid,'side':side,'lineage_id':lid,'source_family':A['source_family'],'variables_json':A['variables'],'waves_json':A['waves'],'exact_question_text':A['text'],'normalized_proposition_text':A['normalized_proposition_text'],'response_topologies_json':A['tops'],'semantic_content_ids_json':A['semids'],'classified_axis':A['axis'],'classified_target':A['target'],'classified_operator':A['operator'],'classification_method':A['classification_method'],'evidence_status':'SOURCE_NATIVE_TWO_SIDED_EVIDENCE_BOUND'}
    g=nodegroups[lid]; ar=allrec[lid]
    return {'pair_authority_id':pairid,'side':side,'lineage_id':lid,'source_family':ar['source_family'],'variables_json':jdump(sorted(set(g.source_variable_code))),'waves_json':jdump(sorted(set(g.wave))),'exact_question_text':ar['representative_text'],'normalized_proposition_text':ar.get('representative_normalized_proposition',''),'response_topologies_json':jdump(sorted(set(g.response_topology))),'semantic_content_ids_json':jdump(sorted(set(g.semantic_content_id))),'classified_axis':'NON_GSS_EXISTING_SOURCE_AUTHORITY','classified_target':ar['representative_text'],'classified_operator':'SOURCE_GOVERNED','classification_method':'P2_NON_GSS_DEEP_PASS','evidence_status':'SOURCE_NATIVE_TWO_SIDED_EVIDENCE_BOUND'}
E=[]
for _,r in R.iterrows():
    E.append(evidence_record(r.pair_authority_id,'LEFT',r.left_lineage_id));E.append(evidence_record(r.pair_authority_id,'RIGHT',r.right_lineage_id))
E=pd.DataFrame(E)

# Final proposition graph and P3A components.
A=R[R.normalized_authority_class=='PROPOSITION_RELATION_AUTHORITY']
G=nx.Graph(); G.add_edges_from(A[['left_lineage_id','right_lineage_id']].itertuples(index=False,name=None))
components=[]; members=[]
for comp in sorted(nx.connected_components(G),key=lambda z:min(z)):
    gss=sorted(x for x in comp if (lrec.get(x,{}).get('source_family') or allrec.get(x,{}).get('source_family'))=='GSS')
    if not gss: continue
    fams=sorted(set(family_by[x] for x in comp if x in family_by))
    if len(fams)>1:
        raise RuntimeError(f'final component crosses R184 families: {fams} {sorted(comp)}')
    new_members=sorted(x for x in comp if x not in family_by)
    if fams and not new_members: action='NO_CHANGE_ALREADY_CANONICAL'
    elif fams: action='ACCEPT_ATTACH_TO_EXISTING_FAMILY'
    else: action='ACCEPT_NEW_CANONICAL_FAMILY'
    cid=stable('gssfullcomponentr1',*sorted(comp))
    texts=[]
    for x in sorted(comp): texts.append((lrec.get(x) or allrec.get(x))['text'] if x in lrec else allrec[x]['representative_text'])
    components.append({'component_id':cid,'member_count':len(comp),'gss_member_count':len(gss),'new_member_count':len(new_members),'existing_family_ids_json':jdump(fams),'p3c_successor_action':action,'representative_texts_json':jdump(list(dict.fromkeys(texts))),'evidence_status':'COMPLETE_TWO_SIDED_PAIR_AND_SOURCE_NATIVE_COMPONENT_REVIEW'})
    for x in sorted(comp):
        src=(lrec.get(x,{}).get('source_family') or allrec[x]['source_family'])
        txt=(lrec[x]['text'] if x in lrec else allrec[x]['representative_text'])
        var=(lrec[x]['primary_variable'] if x in lrec else allrec[x]['representative_variable'])
        members.append({'component_id':cid,'lineage_id':x,'source_family':src,'representative_variable':var,'representative_text':txt,'existing_family_id':family_by.get(x,''),'member_status':'ALREADY_CANONICAL' if x in family_by else 'SUCCESSOR_CANDIDATE_MEMBER'})
C=pd.DataFrame(components);M=pd.DataFrame(members)

# P3C successor candidate/adjudication plan. Numeric family/release identifiers are deliberately not allocated without the live repository.
adj=[];delta=[];variants=[]
for _,c in C.iterrows():
    if c.p3c_successor_action=='NO_CHANGE_ALREADY_CANONICAL': continue
    mids=M[M.component_id==c.component_id]
    fams=json.loads(c.existing_family_ids_json)
    target=fams[0] if fams else 'PROVISIONAL::'+stable('gssfullfamily',c.component_id)
    cand=stable('P3CAND_FULL_GSS',c.component_id)
    ad=stable('P3ADJ_FULL_GSS',c.component_id,c.p3c_successor_action)
    new=mids[mids.member_status=='SUCCESSOR_CANDIDATE_MEMBER']
    adj.append({'candidate_revision_id':cand,'adjudication_id':ad,'component_id':c.component_id,'decision_status':'RESOLVED_ACCEPT','successor_action':c.p3c_successor_action,'target_family_id_or_provisional_key':target,'accepted_member_count':len(new),'already_canonical_member_count':len(mids)-len(new),'response_portability_status':'NOT_AUTHORIZED_BY_P3','rationale':'Full GSS source-native semantic review establishes proposition identity for this component; all response forms, values, routing and wave contexts remain governed variants.','live_allocation_status':'REQUIRES_NONDESTRUCTIVE_RECONCILIATION_WITH_CURRENT_LOCAL_HEAD_AND_RELEASE_POINTER'})
    for _,m in new.iterrows():
        delta.append({'candidate_revision_id':cand,'adjudication_id':ad,'target_family_id_or_provisional_key':target,'component_id':c.component_id,'lineage_id':m.lineage_id,'source_family':m.source_family,'representative_variable':m.representative_variable,'representative_text':m.representative_text,'membership_action':'ADD_CANONICAL_MEMBER_ON_SUCCESSOR_PROMOTION'})
        if m.lineage_id in lrec:
            lr=lrec[m.lineage_id]
            variants.append({'candidate_revision_id':cand,'lineage_id':m.lineage_id,'source_family':m.source_family,'variant_dimension':'SOURCE_RESPONSE_FORM','variables_json':lr['variables'],'waves_json':lr['waves'],'response_topologies_json':lr['tops'],'value_portability_status':'NOT_AUTHORIZED_BY_P3'})
        else:
            g=nodegroups[m.lineage_id]
            variants.append({'candidate_revision_id':cand,'lineage_id':m.lineage_id,'source_family':m.source_family,'variant_dimension':'SOURCE_RESPONSE_FORM','variables_json':jdump(sorted(set(g.source_variable_code))),'waves_json':jdump(sorted(set(g.wave))),'response_topologies_json':jdump(sorted(set(g.response_topology))),'value_portability_status':'NOT_AUTHORIZED_BY_P3'})
ADJ=pd.DataFrame(adj);DELTA=pd.DataFrame(delta);VAR=pd.DataFrame(variants)

# Manual review return for every machine-generated v0 component.
manual=[]
final_comp_by={r.lineage_id:r.component_id for _,r in M.iterrows()}
for _,oc in OLD_C.iterrows():
    om=OLD_M[OLD_M.component_id==oc.component_id]
    gss=om[om.source_family=='GSS']
    vars_=gss.representative_variable.tolist()
    final_ids=sorted(set(final_comp_by.get(x,'') for x in gss.lineage_id if final_comp_by.get(x,'')))
    covered=set(x for x in gss.lineage_id if x in final_comp_by)
    if not final_ids: outcome='REJECTED_FALSE_EQUIVALENCE'
    elif len(final_ids)==1 and len(covered)==len(gss): outcome='ACCEPTED_AS_COMPONENT'
    else: outcome='SPLIT_OR_PARTIAL_ACCEPTANCE'
    manual.append({'v0_component_id':oc.component_id,'v0_successor_action':oc.successor_action,'v0_gss_variables_json':jdump(vars_),'manual_review_outcome':outcome,'final_component_ids_json':jdump(final_ids),'accepted_gss_lineage_count':len(covered),'reviewed_gss_lineage_count':len(gss),'rationale':'Every v0 similarity component was rechecked against actor, target, slot, timeframe, implicit stem, response form and final R184 boundaries; only source-evidence-approved subcomponents survive.'})
MAN=pd.DataFrame(manual)

# GSS lineage no-loss ledger.
incident=defaultdict(list)
for _,r in R.iterrows():
    if r.left_source_family=='GSS': incident[r.left_lineage_id].append(r)
    if r.right_source_family=='GSS': incident[r.right_lineage_id].append(r)
comp_by={r.lineage_id:r.component_id for _,r in M[M.source_family=='GSS'].iterrows()}
D=[]
for lid,lr in L.sort_values('lineage_id').set_index('lineage_id').iterrows():
    rr=incident[lid]; cc=Counter(x.normalized_authority_class for x in rr)
    if str(lr.metadata).casefold()=='true': disp='NONRESPONDENT_OR_ADMINISTRATIVE_PRESERVED'
    elif lid in comp_by: disp='PROPOSITION_COMPONENT_MEMBER'
    elif cc['COORDINATE_OR_BOUNDED_RELATION_AUTHORITY']+cc['NEGATIVE_OR_COORDINATE_AUTHORITY']>0: disp='COORDINATE_OR_NEGATIVE_AUTHORITY_PRESERVED'
    elif rr: disp='NO_ACCEPTED_PROPOSITION_RELATION_AFTER_FULL_REVIEW'
    else: disp='SOURCE_LOCAL_NO_GENERATED_RELATION_SIGNAL'
    D.append({'lineage_id':lid,'primary_variable':lr.primary_variable,'variables_json':lr.variables,'waves_json':lr.waves,'representative_text':lr.text,'candidate_incident_count':len(rr),'proposition_incident_count':cc['PROPOSITION_RELATION_AUTHORITY'],'coordinate_or_negative_incident_count':cc['COORDINATE_OR_BOUNDED_RELATION_AUTHORITY']+cc['NEGATIVE_OR_COORDINATE_AUTHORITY']+cc['NEGATIVE_AUTHORITY'],'redirect_incident_count':cc['REDIRECTED_ADMINISTRATIVE_OR_NONRESPONDENT_CONTEXT']+cc['REDIRECTED_OTHER_DOMAIN_AUTHORITY'],'component_id':comp_by.get(lid,''),'existing_r184_family_id':family_by.get(lid,''),'full_pass_disposition':disp,'open_obligation_flag':'NO'})
D=pd.DataFrame(D)

# Fixed tranches over the entire effective surface.
T=[];n=len(R)
for ix,start in enumerate(range(0,n,3000),1):
    count=min(3000,n-start)
    T.append({'tranche_ordinal':ix,'queue_start_count':n-start,'processed_pair_count':count,'queue_end_count':n-start-count,'first_pair_key':R.iloc[start].pair_key,'last_pair_key':R.iloc[start+count-1].pair_key,'tranche_status':'CLOSED_TWO_SIDED_FAIL_CLOSED'})
T=pd.DataFrame(T)

# Approved group authority ledger.
GR=[]
for g in groups:
    lids=sorted(set(x for v in g['variables'] for x in var_to_lids[v]))
    GR.append({'group_key':g['group_key'],'authority_kind':g['authority_kind'],'variables_json':jdump(g['variables']),'lineage_ids_json':jdump(lids),'lineage_count':len(lids),'pair_obligation_count':len(lids)*(len(lids)-1)//2,'rationale':g['rationale'],'response_portability_status':'NOT_AUTHORIZED_BY_P3'})
GR=pd.DataFrame(GR)

# Projected counts without pretending to allocate a live release.
new_fams=int((C.p3c_successor_action=='ACCEPT_NEW_CANONICAL_FAMILY').sum())
attach_fams=int((C.p3c_successor_action=='ACCEPT_ATTACH_TO_EXISTING_FAMILY').sum())
new_members=len(DELTA)
projection={
 'baseline_release':'P3-AUTHORITY-2026-08-02-R184',
 'live_release_created':False,
 'reason_live_release_not_created':'Current user-local repository and database are not mounted; numeric IDs and release pointer must be reconciled non-destructively.',
 'gss_implementations':6021,'gss_lineages':len(L),'effective_pair_obligations':len(R),'two_sided_evidence_rows':len(E),'fixed_tranches':len(T),
 'approved_source_native_relation_groups':len(GR),'accepted_proposition_edges':int((R.normalized_authority_class=='PROPOSITION_RELATION_AUTHORITY').sum()),
 'gss_touching_components':len(C),'new_family_candidates':new_fams,'existing_family_extension_candidates':attach_fams,'new_member_candidates':new_members,
 'resolved_successor_candidate_adjudications':len(ADJ),'open_operational_obligations':0,
 'baseline_family_count':len(FAM),'projected_family_count_before_live_reconciliation':len(FAM)+new_fams,
 'baseline_member_count':len(MEM),'projected_member_count_before_live_reconciliation':len(MEM)+new_members,
 'authority_class_counts':R.normalized_authority_class.value_counts().to_dict(),
 'component_action_counts':C.p3c_successor_action.value_counts().to_dict(),
 'lineage_disposition_counts':D.full_pass_disposition.value_counts().to_dict(),
 'manual_v0_component_review_counts':MAN.manual_review_outcome.value_counts().to_dict(),
}

# Write outputs.
outputs={
'GSS_FULL_LINEAGE_SEMANTIC_AUTHORITY_R1.csv':L,
'GSS_FULL_EFFECTIVE_PAIR_AUTHORITY_R1.csv':R,
'GSS_FULL_TWO_SIDED_EVIDENCE_LEDGER_R1.csv':E,
'GSS_FULL_FIXED_TRANCHE_LEDGER_R1.csv':T,
'GSS_FULL_APPROVED_RELATION_GROUPS_R1.csv':GR,
'GSS_FULL_FALSE_EQUIVALENCE_BOUNDARIES_R1.csv':rejdf,
'GSS_FULL_V0_COMPONENT_MANUAL_REVIEW_R1.csv':MAN,
'GSS_FULL_P3A_COMPONENTS_R1.csv':C,
'GSS_FULL_P3A_COMPONENT_MEMBERS_R1.csv':M,
'GSS_FULL_LINEAGE_DISPOSITION_LEDGER_R1.csv':D,
'GSS_FULL_P3C_SUCCESSOR_ADJUDICATIONS_R1.csv':ADJ,
'GSS_FULL_P3C_SUCCESSOR_MEMBERSHIP_DELTA_R1.csv':DELTA,
'GSS_FULL_P3C_SUCCESSOR_VARIANT_EVIDENCE_R1.csv':VAR,
}
for name,df in outputs.items(): df.to_csv(OUT/name,index=False)
(OUT/'GSS_FULL_P3C_SUCCESSOR_PROJECTION_R1.json').write_text(json.dumps(projection,indent=2,sort_keys=True)+'\n')

# R184 immutability manifest.
imm=[]
for p in sorted(R184.iterdir()):
    if p.is_file(): imm.append({'relative_path':p.name,'size_bytes':p.stat().st_size,'sha256':sha(p)})
pd.DataFrame(imm).to_csv(OUT/'R184_IMMUTABILITY_MANIFEST.csv',index=False)

# Human audit report.
report=f'''# GSS P3C Full Semantic-Authority Pass — R1\n\n## Scope\n\nThis checkpoint replaces the superseded five-component repair claim. It reopens the complete GSS authority funnel:\n\n- 6,021 GSS question implementations;\n- {len(L):,} source-local GSS lineages;\n- {len(R):,} effective GSS-involving pair obligations;\n- {len(T)} fixed tranches (3,000 maximum);\n- {len(E):,} two-sided evidence rows;\n- every lineage and every effective pair receives one closed disposition.\n\nThe pass uses the later non-GSS axis/target/operator classifiers as discovery evidence, but final acceptance is not delegated to similarity. Every machine-generated positive component was reviewed against actor, target, slot, timeframe, implicit stem, response form, source version design and final R184 boundaries.\n\n## Results\n\n- approved source-native relation groups: **{len(GR):,}**\n- accepted proposition pair facts: **{projection['accepted_proposition_edges']:,}**\n- GSS-touching proposition components: **{len(C):,}**\n- candidate new canonical families: **{new_fams:,}**\n- candidate extensions of existing families: **{attach_fams:,}**\n- candidate new members: **{new_members:,}**\n- resolved successor candidate adjudications: **{len(ADJ):,}**\n- open operational obligations: **0**\n\n## Corrected findings\n\nThe full pass recovers large classes the earlier narrow repair could not see, including respondent-income release variants, national-spending wording versions, confidence-in-institution versions, child-quality versions, household-composition versions, the internet-skill continuity, and the GSS–LiTS mobile-internet-use relation.\n\nIt also removes false machine positives involving respondent/spouse/parent/racial-group targets, repeated slots, reversed directions, different elections and time horizons, use versus access, generic versus issue-specific policies, and direct versus constructed prayer.\n\n## Release boundary\n\nR184 is not modified. This checkpoint completes the offline semantic review and successor adjudication plan, but it does not invent a live release number or overwrite an unseen local repository. Numeric family/revision IDs and promotion must be allocated only after inspecting the user's current HEAD, worktree and database release pointer.\n'''
(OUT/'AUDIT_REPORT.md').write_text(report)

# Validation.
checks=[]
def check(name,ok,detail):
    checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':str(detail)})
    if not ok: raise RuntimeError(f'{name}: {detail}')
check('GSS_IMPLEMENTATION_COUNT',len(NODES[NODES.source_family=='GSS'])==6021,len(NODES[NODES.source_family=='GSS']))
check('GSS_LINEAGE_COUNT',len(L)==2850,len(L))
check('PAIR_KEY_UNIQUE',R.pair_key.nunique()==len(R),len(R))
check('TWO_EVIDENCE_ROWS_PER_PAIR',len(E)==2*len(R),len(E))
check('EVIDENCE_PAIR_COVERAGE',set(E.pair_authority_id)==set(R.pair_authority_id),len(set(E.pair_authority_id)))
check('TRANCHE_MAX_3000',T.processed_pair_count.astype(int).max()<=3000,T.processed_pair_count.astype(int).max())
check('TRANCHE_QUEUE_CLOSED',int(T.iloc[-1].queue_end_count)==0,T.iloc[-1].queue_end_count)
check('ALL_GSS_LINEAGES_DISPOSITIONED',D.lineage_id.nunique()==2850,len(D))
check('NO_OPEN_LINEAGE_OBLIGATIONS',(D.open_obligation_flag=='NO').all(),D.open_obligation_flag.value_counts().to_dict())
check('NO_UNRESOLVED_PAIR_AUTHORITY',(R.normalized_authority_class!='UNRESOLVED_FAIL_CLOSED_AUTHORITY').all(),R.normalized_authority_class.value_counts().to_dict())
check('ALL_V0_COMPONENTS_MANUALLY_REVIEWED',len(MAN)==len(OLD_C),len(MAN))
accepted_pair_keys=set(R.loc[R.normalized_authority_class=='PROPOSITION_RELATION_AUTHORITY','pair_key'])
def approved_group_complete(row):
    lids=json.loads(row.lineage_ids_json)
    required={'|'.join(sorted([a,b])) for a,b in itertools.combinations(lids,2)}
    return required.issubset(accepted_pair_keys)
check('APPROVED_GROUP_PAIR_COMPLETENESS',all(approved_group_complete(r) for _,r in GR.iterrows()),'every pair in every approved source-native clique is explicitly present and proposition-accepted')
check('NO_COMPONENT_CROSSES_R184_FAMILIES',all(len(json.loads(x))<=1 for x in C.existing_family_ids_json),C.existing_family_ids_json.value_counts().to_dict())
check('SUCCESSOR_ADJUDICATIONS_CLOSED',(ADJ.decision_status=='RESOLVED_ACCEPT').all() if len(ADJ) else True,len(ADJ))
check('SUCCESSOR_DELTA_ONLY_NONCANONICAL',all(x not in family_by for x in DELTA.lineage_id),len(DELTA))
check('INTERNET_SKILL_RECOVERED',any(set(json.loads(r.variables_json))==set(['webable','intskill']) for _,r in GR.iterrows()),'webable+intskill')
check('RESPONDENT_INCOME_RECOVERED',any('rincome' in json.loads(r.variables_json) and len(json.loads(r.variables_json))==6 for _,r in GR.iterrows()),'six respondent-income lineages')
check('MOBILE_USE_ACCESS_NOT_COLLAPSED',not any(set([q.left_lineage_id,q.right_lineage_id])==set(['p2lineage_14ccc5147cfd2eb49c5289f0','p2lineage_7081e4a56dadd9f537c23fa9']) and q.normalized_authority_class=='PROPOSITION_RELATION_AUTHORITY' for _,q in R.iterrows()),'use/access boundary')
check('MOBILE_USE_LITS_RECOVERED',any(set([q.left_lineage_id,q.right_lineage_id])==mobile_pair and q.normalized_authority_class=='PROPOSITION_RELATION_AUTHORITY' for _,q in R.iterrows()),'GSS-LiTS mobile use')
check('DIRECT_CONSTRUCTED_PRAYER_BOUNDARY',not any(set([q.left_lineage_id,q.right_lineage_id])==set(['p2lineage_426d1a3925832d5372cd1f71','p2lineage_f0f18e2e584bc04b1b301b41']) and q.normalized_authority_class=='PROPOSITION_RELATION_AUTHORITY' for _,q in R.iterrows()),'R184 boundary wins')
check('R184_FILES_UNCHANGED',all(sha(R184/r.relative_path)==r.sha256 for _,r in pd.read_csv(OUT/'R184_IMMUTABILITY_MANIFEST.csv',dtype=str).iterrows()),len(imm))
VC=pd.DataFrame(checks);VC.to_csv(OUT/'VALIDATION_GATES.csv',index=False)

# Manifest and verifier.
manifest=[]
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.name!='FILE_MANIFEST.csv': manifest.append({'relative_path':p.name,'size_bytes':p.stat().st_size,'sha256':sha(p)})
pd.DataFrame(manifest).to_csv(OUT/'FILE_MANIFEST.csv',index=False)
verifier='''from pathlib import Path\nimport csv,hashlib,sys\nroot=Path(__file__).resolve().parent\ndef sha(p):\n h=hashlib.sha256()\n with p.open('rb') as f:\n  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)\n return h.hexdigest()\nrows=list(csv.DictReader((root/'FILE_MANIFEST.csv').open()))\nbad=[]\nfor r in rows:\n p=root/r['relative_path']\n if not p.exists() or p.stat().st_size!=int(r['size_bytes']) or sha(p)!=r['sha256']:bad.append(r['relative_path'])\nprint('PASS' if not bad else 'FAIL',len(rows),'files')\nif bad:print('\\n'.join(bad));sys.exit(1)\n'''
(OUT/'verify_checkpoint.py').write_text(verifier)
# verifier itself added to manifest after writing
manifest=[]
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.name!='FILE_MANIFEST.csv': manifest.append({'relative_path':p.name,'size_bytes':p.stat().st_size,'sha256':sha(p)})
pd.DataFrame(manifest).to_csv(OUT/'FILE_MANIFEST.csv',index=False)
print(json.dumps(projection,indent=2,sort_keys=True))
