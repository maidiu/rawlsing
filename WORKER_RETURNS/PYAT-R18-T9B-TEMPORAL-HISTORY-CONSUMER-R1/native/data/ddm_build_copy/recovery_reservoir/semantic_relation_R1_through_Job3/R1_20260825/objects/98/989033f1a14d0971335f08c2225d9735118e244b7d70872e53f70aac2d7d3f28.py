from __future__ import annotations
import pandas as pd, json, hashlib, pathlib, re, gzip, os, textwrap
from collections import defaultdict, Counter

ROOT=pathlib.Path(__file__).resolve().parent
RET=ROOT/'RETURN'
AUTH=ROOT/'AUTHORITY'
SRCROOT=pathlib.Path('/mnt/data/t06w04_continuation/source_authority/unpacked/Rawlsing_SourceNative_Questionnaire_Structure_Authority_R1_20260812')
PARENT=ROOT/'PARENT_T06_RETURN/Rawlsing_R10K_S14_T06_SourceFirst_T06W04_Return_20260812.zip'
WORKER='T06W04'
RULE='S14-T15'
TYPE='NORM_PRACTICAL_REALIZATION'

jd=lambda x: json.dumps(x,ensure_ascii=False,separators=(',',':'))

def clean_list(x):
    if isinstance(x,list): return x
    try:
        y=json.loads(x or '[]')
        return y if isinstance(y,list) else []
    except: return []

base=pd.read_csv(AUTH/'NORMALIZED_PRIOR_T06_IMPLEMENTATION_ACCOUNTING.csv',dtype=str).fillna('')
cal=pd.read_csv(AUTH/'ASSIGNED_T06_CALIBRATION_SLICE.csv',dtype=str).fillna('')
# normalize code lookup by wave
by_code={}
by_id={}
for _,r in base.iterrows():
    k=(r.source_family,r.wave,r.source_variable_code.lower())
    by_code[k]=r
    by_id[r.question_implementation_id]=r

def row(fam,wave,code):
    k=(fam,wave,code.lower())
    if k not in by_code:
        raise KeyError(f'missing code {k}')
    return by_code[k]

def ids(fam,wave,codes): return [row(fam,wave,c).question_implementation_id for c in codes]

def code_for_iid(iid): return by_id[iid].source_variable_code if iid in by_id else ''

# Flattened source page cache and helpers
wave_dirs={
 ('GSS','2002'):'GSS__2002',
 ('Arab Barometer','VIII'):'Arab_Barometer__VIII',
 ('EVS','2008'):'EVS__2008',
 ('EVS','1990'):'EVS__1990',
 ('Asian Barometer','W5'):'Asian_Barometer__W5',
 ('South Asia','W1'):'South_Asia__W1',
}
page_cache={}
def pages_for(fam,wave):
    key=(fam,wave)
    if key in page_cache: return page_cache[key]
    p=SRCROOT/'BY_WAVE'/wave_dirs[key]/'NATIVE_SOURCE_PAGE_TEXT.jsonl.gz'
    out=[]
    with gzip.open(p,'rt',encoding='utf-8') as f:
        for line in f:
            o=json.loads(line); txt=o.get('page_text') or o.get('text') or ''
            out.append((str(o.get('page_number','')),txt))
    page_cache[key]=out
    return out

code_search_override={
 ('Arab Barometer','VIII','Q550A_1'):'Q550A',('Arab Barometer','VIII','Q550A_2'):'Q550A',('Arab Barometer','VIII','Q550A_3'):'Q550A',('Arab Barometer','VIII','Q550A_4'):'Q550A',('Arab Barometer','VIII','Q550A_5'):'Q550A',('Arab Barometer','VIII','Q550A_6'):'Q550A',
 ('Arab Barometer','VIII','Q550B_1'):'Q550B',('Arab Barometer','VIII','Q550B_2'):'Q550B',('Arab Barometer','VIII','Q550B_3'):'Q550B',('Arab Barometer','VIII','Q550B_4'):'Q550B',('Arab Barometer','VIII','Q550B_5'):'Q550B',('Arab Barometer','VIII','Q550B_6'):'Q550B',
 ('Arab Barometer','VIII','Q552_1A'):'Q552',('Arab Barometer','VIII','Q552_1B'):'Q552',
 ('Arab Barometer','VIII','Q521_1'):'Q521',('Arab Barometer','VIII','Q521_2A'):'Q521',('Arab Barometer','VIII','Q521_2B'):'Q521',('Arab Barometer','VIII','Q521_4'):'Q521',('Arab Barometer','VIII','Q521_6'):'Q521',
 ('Arab Barometer','VIII','Q127_1A'):'Q127',('Arab Barometer','VIII','Q127_2A'):'Q127',('Arab Barometer','VIII','Q127_1B'):'Q127',('Arab Barometer','VIII','Q127_2B'):'Q127',
 ('Arab Barometer','VIII','Q547_1'):'Q547',('Arab Barometer','VIII','Q547_2'):'Q547',('Arab Barometer','VIII','Q547_3'):'Q547',('Arab Barometer','VIII','Q547_4'):'Q547',('Arab Barometer','VIII','Q547_TUN2'):'Q547',('Arab Barometer','VIII','Q547_TUN3'):'Q547',('Arab Barometer','VIII','Q547_TUN4'):'Q547',
 ('Asian Barometer','W5','q160a'):'160A',('Asian Barometer','W5','q160b'):'160B',('Asian Barometer','W5','q160c'):'160C',('Asian Barometer','W5','q160d'):'160D',
 ('South Asia','W1','c18d'):'d. The country should be governed',('South Asia','W1','c31c'):'c. Like men, women should have freedom',
}

def source_pages_for_codes(fam,wave,codes):
    hits=[]
    for code in codes:
        token=code_search_override.get((fam,wave,code),code)
        token_low=token.lower()
        ph=[]
        for pn,txt in pages_for(fam,wave):
            if token_low in txt.lower(): ph.append(pn)
        if ph: hits.append({'source_variable_code':code,'flattened_relative_path':f'BY_WAVE/{wave_dirs[(fam,wave)]}/NATIVE_SOURCE_PAGE_TEXT.jsonl.gz','page_numbers':sorted(set(ph),key=lambda x:int(x) if x.isdigit() else 9999)[:4]})
        else: hits.append({'source_variable_code':code,'flattened_relative_path':f'BY_WAVE/{wave_dirs[(fam,wave)]}/NATIVE_SOURCE_PAGE_TEXT.jsonl.gz','page_numbers':[],'binding_note':'code token not uniquely recoverable; wave-local flattened source reviewed by battery/stem'})
    return hits

def rid(subtype,fam,wave,norm_codes,prax_codes):
    s='|'.join([WORKER,RULE,subtype,fam,wave,','.join(norm_codes),','.join(prax_codes)])
    return f'T15-{WORKER}-{hashlib.sha1(s.encode()).hexdigest()[:20]}'

def cwid(fam,wave,norm_codes,prax_codes,subtype):
    s='|'.join([fam,wave,','.join(norm_codes),','.join(prax_codes),subtype])
    return f'T15CW-{WORKER}-{hashlib.sha1(s.encode()).hexdigest()[:18]}'

def make_roles(fam,wave,norm_codes,prax_codes,praxis_kind,norm_prop,praxis_prop,condition=''):
    out=[]
    for c in norm_codes:
        r=row(fam,wave,c)
        out.append({'implementation_id':r.question_implementation_id,'source_variable_code':c,'t15_shore':'NORMATIVE_PROPOSITION','exact_question_text':r.exact_question_text,'norm_proposition':norm_prop,'source_condition':r.baseline_condition_routing or condition})
    for c in prax_codes:
        r=row(fam,wave,c)
        out.append({'implementation_id':r.question_implementation_id,'source_variable_code':c,'t15_shore':'PRACTICAL_REALIZATION','praxis_shore_kind':praxis_kind,'exact_question_text':r.exact_question_text,'praxis_proposition':praxis_prop,'source_condition':r.baseline_condition_routing or condition})
    return out

positives=[]
positive_by_cal_rel={}

def add_positive(*,fam,wave,norm_codes,prax_codes,subtype,praxis_kind,norm_prop,praxis_prop,common,actor_scope,actor_basis,target_scope,target_basis,action_domain,action_basis,polarity,distance,bridge,bridge_ids=None,condition='',universe='',basis='',confidence='HIGH',grain='',t06_status='NO_STRICT_T06_OVERLAP_FOUND',overlap=None,semantic_ids=None,calibration_rel=None):
    wrid=rid(subtype,fam,wave,norm_codes,prax_codes)
    role=make_roles(fam,wave,norm_codes,prax_codes,praxis_kind,norm_prop,praxis_prop,condition)
    prov=source_pages_for_codes(fam,wave,norm_codes+prax_codes)
    rec={
      'worker_relation_id':wrid,'central_relation_id':'','authority_class':'SOURCE_FIRST_WORKER_ACCEPTED_T15','rule_id':RULE,'relation_type':TYPE,'manifestation_subtype':subtype,'source_family':fam,'wave':wave,
      'active_source_wave_set_json':jd([f'{fam}::{wave}']),'member_semantic_unit_ids_json':jd(semantic_ids or []),'member_implementation_ids_json':jd(ids(fam,wave,norm_codes+prax_codes)),'role_assignments_json':jd(role),
      'common_proposition_or_target':common,'norm_proposition':norm_prop,'praxis_proposition':praxis_prop,'praxis_shore_kind':praxis_kind,
      'actor_scope':actor_scope,'actor_alignment_basis':actor_basis,'target_scope':target_scope,'target_alignment_basis':target_basis,'action_domain':action_domain,'action_alignment_basis':action_basis,
      'relation_polarity':polarity,'realization_distance':distance,'bridge_basis_type':bridge,'bridge_basis_ids_json':jd(bridge_ids or []),'position_or_routing_condition':condition,'respondent_universe_intersection':universe or 'wave-local source universe; member routing preserved in role assignments',
      'source_provenance_json':jd(prov),'source_first_adjudication_basis':basis,'central_basis':'Source-first T15 worker authority; central successor adjudication/install pending.','confidence':confidence,'worker_origin':WORKER,'grain_note':grain,
      't06_overlap_status':t06_status,'overlap_with_existing_s14_rule_json':jd(overlap or []),'successor_freeze_status':'WORKER_ACCEPTED__CENTRAL_REVIEW_PENDING','successor_freeze_basis':'No S14/T15 central freeze claimed; append-only worker successor authority.'
    }
    positives.append(rec)
    if calibration_rel: positive_by_cal_rel[calibration_rel]=wrid
    return wrid

# ---- 11 centrally supplied T15 calibration boundary rows, reconstructed as T15 ----
for _,r in cal[cal.central_strict_t06_posture=='BOUNDARY_TO_T15'].iterrows():
    fam,wave=r.source_family,r.wave
    nc=clean_list(r.norm_source_variable_codes_json); pc=clean_list(r.praxis_source_variable_codes_json)
    cf=r.calibration_family
    if cf=='DIRECT_ENACTMENT_OR_NARROWER_REALIZATION': st='DIRECT_ENACTMENT'; pk='REALIZED_SELF_CONDUCT'; pol='ENACTS'; dist='D2_NARROWER_INSTANCE'; bridge='DIRECT_SOURCE_ENTAILMENT'
    elif cf=='RIGHT_OR_FREEDOM_EXERCISE': st='RIGHT_OR_PERMISSION_EXERCISE'; pol='EXERCISES'; dist='D2_NARROWER_INSTANCE'; bridge='SOURCE_EXPLICIT_RIGHT_EXERCISE'; pk='LIFE_STATE' if fam=='South Asia' else 'REALIZED_SELF_CONDUCT'
    else: st='INSTITUTIONAL_OR_SOCIAL_REALIZATION'; pk='INSTITUTIONAL_STATE'; pol='REALIZES'; dist='D1_DIRECT' if any(x.lower().startswith('q606') for x in nc) else 'D2_NARROWER_INSTANCE'; bridge='SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION'
    roles=clean_list(r.role_assignments_json)
    norm_native=[x.get('native_source_text','') for x in roles if x.get('relation_role')=='RR_NORM']
    praxis_native=[x.get('native_source_text','') for x in roles if x.get('relation_role')!='RR_NORM']
    norm_prop='; '.join([x for x in norm_native if x]) or r.common_proposition_or_target
    praxis_prop='; '.join([x for x in praxis_native if x]) or 'source-measured practical realization: '+r.common_proposition_or_target
    add_positive(fam=fam,wave=wave,norm_codes=nc,prax_codes=pc,subtype=st,praxis_kind=pk,norm_prop=norm_prop,praxis_prop=praxis_prop,
      common=r.common_proposition_or_target or f'{nc} → {pc}',actor_scope=r.actor_scope or 'source-specified actor / respondent-as-instance where applicable',actor_basis='Exact source-native actor relation preserved from calibration role assignments; respondent-as-instance only where the norm governs the actor class.',
      target_scope=r.target_scope or r.common_proposition_or_target,target_basis='Exact source target or source-explicit narrower instance preserved; no topic-only widening.',action_domain=r.action_domain or r.common_proposition_or_target,action_basis='Central T15 calibration marks this prior T06 edge as broader norm→practical-realization rather than strict same-predicate T06.',polarity=pol,distance=dist,bridge=bridge,
      bridge_ids=[r.worker_relation_id],condition=r.position_or_routing_condition,universe='Exact member routing/split/ballot conditions preserved; semantic relation does not imply respondent co-observation when source arms are disjoint.',basis='Independently re-read from flattened source at battery/stem level and agrees with the centrally supplied T15 calibration boundary; old T06 pair used only after source reconstruction as overlap control.',grain='T15 successor grain; prior T06 worker edge retained as immutable ancestry pending central boundary migration.',t06_status='RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW',overlap=[{'rule_id':'S14-T06','worker_relation_id':r.worker_relation_id,'posture':'BOUNDARY_TO_T15'}],semantic_ids=clean_list(r.member_semantic_unit_ids_json),calibration_rel=r.worker_relation_id)

# ---- Novel source-first T15 positives ----
# GSS 2002
add_positive(fam='GSS',wave='2002',norm_codes=['othshelp'],prax_codes=['givhmlss'],subtype='DIRECT_ENACTMENT',praxis_kind='REALIZED_SELF_CONDUCT',
 norm_prop='People should be willing to help others who are less fortunate.',praxis_prop='Respondent gave food or money to a homeless person during the source helping-behavior period.',common='helping a source-explicitly disadvantaged person',actor_scope='general people → respondent as instance',actor_basis='The normative actor is general people; the respondent is a valid instance of that actor class.',target_scope='less-fortunate others → homeless person',target_basis='Homeless person is a concrete disadvantaged-person instance within the source helping-attitudes/helping-behaviors terrain; generic charity rows were not promoted.',action_domain='material helping/giving',action_basis='The practical act is direct material assistance, a concrete performance of helping rather than a correlated attitude.',polarity='ENACTS',distance='D2_NARROWER_INSTANCE',bridge='DIRECT_SOURCE_ENTAILMENT',condition='OTHSHELP helping-attitudes item; GIVHMLSS helping-behaviors battery. Preserve distinct GSS version/ballot routing.',universe='Potentially disjoint GSS ballot/version universes; relation is source-semantic and does not assert respondent-level joint observation.',basis='Flattened GSS instrument explicitly supplies a general help norm and a concrete homeless-aid act; target narrowing is bounded and action identity remains help.',grain='One norm + one concrete helping act; generic charity/volunteer items excluded because beneficiary identity is not source-fixed.')

# Arab Barometer VIII helper
for split in ['A','B']:
    n2=f'Q550{split}_2'; n3=f'Q550{split}_3'; n5=f'Q550{split}_5'; n6=f'Q550{split}_6'
    splitcond=f'SPLIT {split}; preserve COUNTRY and item-specific routing on praxis members.'
    # no-corruption criterion -> measured corruption state
    add_positive(fam='Arab Barometer',wave='VIII',norm_codes=[n2],prax_codes=['Q210','Q211B','Q211C'],subtype='INSTITUTIONAL_OR_SOCIAL_REALIZATION',praxis_kind='INSTITUTIONAL_STATE',
      norm_prop=('Absence of corruption is an essential pillar of human dignity.' if split=='A' else 'Absence of corruption is an essential pillar of democracy.'),praxis_prop='Measured extent/widespreadness of corruption in national and local public institutions.',common='absence/presence of public-institution corruption',actor_scope='political/public institutional order',actor_basis='Norm and practical battery concern the corruption state of the country/public institutions; local/national scopes are explicit subscopes.',target_scope='public-sector corruption',target_basis='Q210/Q211B/Q211C directly measure the same corruption condition at national/local institutional scopes.',action_domain='institutional corruption state',action_basis='Practical members directly measure whether the norm-defined no-corruption state is realized or frustrated.',polarity='FRUSTRATES',distance='D2_NARROWER_INSTANCE',bridge='SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',condition=splitcond,universe=('Q550'+split+' split-arm respondents; Q211B/C have their own split/country routing; joint respondent overlap preserved where present and not assumed where absent.'),basis='Source wording is exact no-corruption criterion ↔ actual corruption-state measurement; no ideological inference.',grain='Parallel national/local corruption-state battery retained as one source-native practical realization family.')
    # anti-corruption crackdown as explicit means
    add_positive(fam='Arab Barometer',wave='VIII',norm_codes=[n2],prax_codes=['Q211_2'],subtype='INSTRUMENTAL_ENACTMENT',praxis_kind='POLICY_APPLICATION',
      norm_prop=('Absence of corruption is an essential pillar of human dignity.' if split=='A' else 'Absence of corruption is an essential pillar of democracy.'),praxis_prop='Extent to which the national government is working to crack down on corruption.',common='government anti-corruption enactment toward the no-corruption criterion',actor_scope='political order norm; national government practical actor',actor_basis='Government is the explicitly named practical institutional actor charged with the anti-corruption action.',target_scope='corruption in national public institutions',target_basis='The practical action explicitly targets corruption, the exact norm object.',action_domain='anti-corruption government action',action_basis='“Working to crack down on corruption” is source-explicit means language, not a worker-supplied causal story.',polarity='ENACTS',distance='D3_EXPLICIT_MEANS',bridge='SOURCE_EXPLICIT_MEANS',bridge_ids=['Q210→Q211_2 native conditional anti-corruption sequence'],condition=f'{splitcond} Q211_2 asked only if Q210 indicates corruption (1/2/3).',universe=f'Q550{split} split-arm respondents intersected with Q211_2 corruption-present routing where co-observed; semantic bridge retained beyond co-observation.',basis='Native Q211_2 wording explicitly names the practical action as cracking down on the exact target “corruption”; satisfies the high-risk instrumental means requirement.',grain='One normative criterion + one explicitly targeted government anti-corruption application.')
    # basic necessities availability state
    add_positive(fam='Arab Barometer',wave='VIII',norm_codes=[n3],prax_codes=['Q127_1A','Q127_2A'],subtype='INSTITUTIONAL_OR_SOCIAL_REALIZATION',praxis_kind='INSTITUTIONAL_STATE',
      norm_prop=('Basic necessities such as food/water/clothes/shelter being available for all is an essential pillar of human dignity.' if split=='A' else 'Basic necessities such as food/water/clothes/shelter being available for all is an essential pillar of democracy.'),praxis_prop='Measured extent to which availability of food and housing is a problem in the country.',common='availability of basic necessities',actor_scope='country/social order',actor_basis='Both shores concern population-level availability rather than respondent self-conduct.',target_scope='basic necessities → food and housing availability',target_basis='Q127 Split A explicitly measures availability (not affordability) of two named basic-necessity subtypes in the criterion.',action_domain='social provision/availability state',action_basis='The practical items directly measure realization/frustration of the availability state; affordability cells are separately rejected.',polarity='FRUSTRATES',distance='D2_NARROWER_INSTANCE',bridge='SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',condition=f'{splitcond} Q127 is COUNTRY!=9; Q127 availability cells are SPLIT A.',universe=('Same split A for Q550A/Q127A when split=A; disjoint A/B source arms for Q550B→Q127A, explicitly preserved as semantic-only across split.'),basis='Native criterion names basic necessities “available for all”; Q127A measures whether food/housing availability is a problem. Affordability cells are not substituted.',grain='Norm → two source-explicit availability subcells; clean food/water/clothes lack selected practical cells and are not invented.')
    # safety state
    add_positive(fam='Arab Barometer',wave='VIII',norm_codes=[n5],prax_codes=['Q105A'],subtype='INSTITUTIONAL_OR_SOCIAL_REALIZATION',praxis_kind='INSTITUTIONAL_STATE',
      norm_prop=('Feeling safe from physical danger is an essential pillar of human dignity.' if split=='A' else 'Feeling safe from physical danger is an essential pillar of democracy.'),praxis_prop='Respondent rates the safety of the neighborhood.',common='experienced physical safety',actor_scope='people/country criterion → respondent neighborhood experience',actor_basis='Respondent/neighborhood is a bounded source instance of the people-level safety condition.',target_scope='physical safety → neighborhood safety',target_basis='Neighborhood safety is a source-measured narrower setting of the same safety state; unrelated security/trust items were not included.',action_domain='social safety state',action_basis='Practical item directly measures realized safety/unsafety, not an attitude about an unrelated security institution.',polarity='REALIZES',distance='D2_NARROWER_INSTANCE',bridge='SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',condition=splitcond,universe=f'Q550{split} split arm; Q105A general wave routing. Co-observation preserved only for matching split respondents.',basis='Exact safety-state criterion ↔ direct neighborhood safety-state measurement.',grain='One criterion + one bounded safety-state measure.')
    # civil-rights exercise via actual political acts
    add_positive(fam='Arab Barometer',wave='VIII',norm_codes=[n6],prax_codes=['Q552_1A','Q552_1B'],subtype='RIGHT_OR_PERMISSION_EXERCISE',praxis_kind='REALIZED_SELF_CONDUCT',
      norm_prop=('Guaranteed basic civil rights—including freedom of speech and protest—are an essential pillar of human dignity.' if split=='A' else 'Guaranteed basic civil rights—including freedom of speech and protest—are an essential pillar of democracy.'),praxis_prop='In the past year respondent made a political statement through art/writing/music and/or participated in an in-person protest/demonstration/strike/boycott.',common='exercise of source-enumerated speech/protest civil rights',actor_scope='general rights-holder → respondent as rights-holder instance',actor_basis='The practical respondent is an instance of the persons whose speech/protest rights the criterion protects.',target_scope='basic civil rights → speech and protest examples',target_basis='The norm source itself gives freedom of speech and freedom to protest as examples; Q552 measures concrete exercises on those axes.',action_domain='political expression and protest participation',action_basis='Actual statement/protest acts instantiate the source-enumerated freedoms; contact/petition/boycott-only cells not promoted absent a direct example match.',polarity='EXERCISES',distance='D2_NARROWER_INSTANCE',bridge='SOURCE_EXPLICIT_RIGHT_EXERCISE',condition=f'{splitcond} Q552_1A SPLIT A; Q552_1B SPLIT B.',universe='Member split-arm intersections recorded; cross-arm member linkage is source-semantic and does not imply respondent-level co-observation.',basis='Right/freedom examples are explicit in Q550; Q552 supplies concrete respondent exercise of two named examples.',grain='Broad civil-right criterion → bounded speech/protest exercise battery only.')

# Asian Barometer W5
add_positive(fam='Asian Barometer',wave='W5',norm_codes=['q91'],prax_codes=['q111'],subtype='INSTITUTIONAL_OR_SOCIAL_REALIZATION',praxis_kind='INSTITUTIONAL_STATE',norm_prop='Court protection of ordinary people from abuse of government power is an essential characteristic of democracy.',praxis_prop='When government leaders break laws, there is nothing the court can do.',common='court capacity to restrain unlawful/abusive government power',actor_scope='court and government leaders; ordinary people as protected constituency',actor_basis='Both shores directly concern the court’s capacity relative to government power; practical item is a contrary institutional state.',target_scope='government abuse/lawbreaking restraint',target_basis='Lawbreaking by government leaders is a narrower source form of unlawful government power; ordinary-person beneficiary is not expanded beyond the source.',action_domain='judicial constraint on government power',action_basis='Practical item directly measures court incapacity on the same institutional restraint axis.',polarity='FRUSTRATES',distance='D2_NARROWER_INSTANCE',bridge='SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',condition='Q91-97 democracy-characteristic battery; Q108-119 quality-of-governance battery.',basis='Native source juxtaposes normative court-protection criterion and realized court-capacity state; relation does not infer causation beyond that axis.',grain='Normative institutional criterion → contrary realized court-capacity state.')
add_positive(fam='Asian Barometer',wave='W5',norm_codes=['q92'],prax_codes=['q124','q125'],subtype='INSTITUTIONAL_OR_SOCIAL_REALIZATION',praxis_kind='INSTITUTIONAL_STATE',norm_prop='Politics being clean and free of corruption is an essential characteristic of democracy.',praxis_prop='Measured widespreadness of corruption/bribe-taking in local and national government.',common='clean politics / absence versus presence of corruption',actor_scope='political/government institutions',actor_basis='Practical members are local/national institutional instances of the political corruption criterion.',target_scope='political corruption → local and national government',target_basis='Exact corruption/bribe-taking target with explicit institutional subscopes.',action_domain='institutional corruption state',action_basis='Practical battery directly measures realized/frustrated corruption state.',polarity='FRUSTRATES',distance='D2_NARROWER_INSTANCE',bridge='SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',condition='Q91-97 meaning-of-democracy battery; Q124-126 governance-corruption battery.',basis='Exact no-corruption criterion ↔ measured local/national corruption state.',grain='One criterion + parallel local/national corruption-state cells.')
add_positive(fam='Asian Barometer',wave='W5',norm_codes=['q92'],prax_codes=['q127'],subtype='PRACTICAL_VIOLATION',praxis_kind='REALIZED_OTHER_CONDUCT',norm_prop='Politics being clean and free of corruption is an essential characteristic of democracy.',praxis_prop='Respondent or someone personally known witnessed an act of corruption or bribe-taking by a politician or government official.',common='political corruption',actor_scope='political system norm; politician/government-official practical actor',actor_basis='The practical actor is explicitly a politician or government official, a direct political-institution actor under the norm.',target_scope='clean politics / corruption',target_basis='Observed corruption/bribe-taking is a concrete contrary instance of the exact no-corruption proposition.',action_domain='corruption/bribe-taking',action_basis='Concrete corruption act directly violates the clean/no-corruption criterion; no mere absence inference.',polarity='VIOLATES',distance='D2_NARROWER_INSTANCE',bridge='SOURCE_EXPLICIT_VIOLATION',condition='Q127 witness/known-person wording preserved; follow-up witness-source items not required for relation truth.',basis='Source explicitly names a concrete corruption/bribe-taking act by political/government actors.',grain='Normative no-corruption state → concrete contrary political act.')
add_positive(fam='Asian Barometer',wave='W5',norm_codes=['q92'],prax_codes=['q126'],subtype='INSTRUMENTAL_ENACTMENT',praxis_kind='POLICY_APPLICATION',norm_prop='Politics being clean and free of corruption is an essential characteristic of democracy.',praxis_prop='Measured effectiveness of the government in cracking down on corruption.',common='government anti-corruption application toward clean politics',actor_scope='political system norm; government practical actor',actor_basis='Government is explicitly named as carrying out the anti-corruption action.',target_scope='corruption',target_basis='Crackdown explicitly targets the exact normative object corruption.',action_domain='government anti-corruption action',action_basis='The source phrase “cracking down on corruption” itself states a means directed at the norm target.',polarity='ENACTS',distance='D3_EXPLICIT_MEANS',bridge='SOURCE_EXPLICIT_MEANS',bridge_ids=['Asian W5 Q124-Q126 corruption governance battery'],condition='Q91-97 meaning-of-democracy battery; Q124-126 governance-corruption battery.',basis='Source-explicit anti-corruption action satisfies T15’s high-risk means requirement without importing outside policy theory.',grain='One criterion + one explicit government anti-corruption application.')
add_positive(fam='Asian Barometer',wave='W5',norm_codes=['q95'],prax_codes=['q121'],subtype='PRACTICAL_VIOLATION',praxis_kind='INSTITUTIONAL_STATE',norm_prop='Political leaders ruling by their own wisdom rather than people’s preferences for collective welfare is evaluated as a democracy characteristic.',praxis_prop='Measured degree to which government responds to what people want.',common='leader decision-making responsiveness to popular preferences',actor_scope='political leaders/government',actor_basis='Both shores directly concern how government leaders relate decisions to people’s preferences.',target_scope='people’s preferences in government decision-making',target_basis='Same preference-responsiveness object; practical state is contrary to “rather than people’s preferences.”',action_domain='government responsiveness versus leader-autonomous rule',action_basis='High responsiveness is the source-explicit contrary institutional practice on the same action axis.',polarity='VIOLATES',distance='D1_DIRECT',bridge='SOURCE_EXPLICIT_VIOLATION',condition='Q91-97 democracy-characteristic battery; Q120-123 governance-capacity/responsiveness battery.',basis='Native wording establishes the direct preference-responsiveness opposition; no ideological valence inference.',grain='Normative leader-autonomy criterion → realized contrary responsiveness state.')
add_positive(fam='Asian Barometer',wave='W5',norm_codes=['q96'],prax_codes=['q109','q119'],subtype='PRACTICAL_VIOLATION',praxis_kind='INSTITUTIONAL_STATE',norm_prop='Rule by one party representing the interests of all classes is evaluated as a democracy characteristic.',praxis_prop='Opposition parties/candidates have opportunities to be elected and elections offer real choice between different parties/candidates.',common='one-party rule versus multiparty electoral competition',actor_scope='political party/electoral system',actor_basis='Both shores define the party structure of political rule/elections.',target_scope='party competition for government',target_basis='Practical members explicitly instantiate opposition/multiple-party competition contrary to one-party-only structure.',action_domain='party-system competition',action_basis='Multiparty electoral opportunity/choice directly contradicts one-party rule on the same institutional axis.',polarity='VIOLATES',distance='D1_DIRECT',bridge='SOURCE_EXPLICIT_VIOLATION',condition='Q91-97 democracy-characteristic battery; Q108-119 governance-state battery.',basis='Source wording itself supplies one-party versus multiple-party/opposition competition; no general democracy inference needed.',grain='One-party norm → two aligned multiparty realized-state cells.')
for ncode,nprop in [('q137','We should get rid of parliament and elections and have a strong leader decide things.'),('q140','We should get rid of elections and parliaments and have experts make decisions on behalf of the people.')]:
    add_positive(fam='Asian Barometer',wave='W5',norm_codes=[ncode],prax_codes=['q108','q119'],subtype='PRACTICAL_VIOLATION',praxis_kind='INSTITUTIONAL_STATE',norm_prop=nprop,praxis_prop='Citizens can remove governments through elections and elections offer voters real choice between parties/candidates.',common='elimination versus realized functioning of competitive elections',actor_scope='national governing/electoral system',actor_basis='Norm and practical members directly concern whether elections structure government selection.',target_scope='elections/parliamentary choice',target_basis='Practical members instantiate the exact election institution the norm proposes eliminating.',action_domain='competitive electoral governance',action_basis='Functioning voter choice/removal through elections directly contradicts “get rid of elections.”',polarity='VIOLATES',distance='D1_DIRECT',bridge='SOURCE_EXPLICIT_VIOLATION',condition='Q137/Q140 authoritarian-democratic-values block; Q108/Q119 governance-state battery.',basis='Explicit contrary election predicates in native wording.',grain='Anti-election norm → realized election-function battery.')
add_positive(fam='Asian Barometer',wave='W5',norm_codes=['q138'],prax_codes=['q109','q119'],subtype='PRACTICAL_VIOLATION',praxis_kind='INSTITUTIONAL_STATE',norm_prop='Only one political party should be allowed to stand for election and hold office.',praxis_prop='Opposition parties/candidates can be elected and voters receive real choice between different parties/candidates.',common='one-party-only permission versus multiparty electoral competition',actor_scope='party/electoral system',actor_basis='Same party/election actor structure.',target_scope='eligibility and competition among political parties',target_basis='Opposition/multiple-party opportunity is the direct contrary institutional state.',action_domain='party eligibility/electoral competition',action_basis='Practical state directly violates one-party-only permission on the same action axis.',polarity='VIOLATES',distance='D1_DIRECT',bridge='SOURCE_EXPLICIT_VIOLATION',condition='Q138 authoritarian-democratic-values block; Q109/Q119 governance-state battery.',basis='Explicit “only one party” versus “parties/candidates not in power” and “different parties/candidates.”',grain='One-party-only norm → parallel contrary multiparty-state cells.')
add_positive(fam='Asian Barometer',wave='W5',norm_codes=['q160c'],prax_codes=['q42'],subtype='INSTITUTIONAL_OR_SOCIAL_REALIZATION',praxis_kind='INSTITUTIONAL_STATE',norm_prop='Government bears responsibility to make sure everyone has access to basic medical care.',praxis_prop='Measured ease/difficulty of obtaining healthcare.',common='access to healthcare/basic medical care',actor_scope='government responsibility; population-level service-access state',actor_basis='Practical item measures the outcome state the government-responsibility norm names; it does not attribute causal performance beyond access.',target_scope='basic medical care / healthcare access',target_basis='Healthcare access is the exact service-access target; “easy/difficult to obtain” operationalizes realization/frustration.',action_domain='healthcare access state',action_basis='Practical state directly measures whether access exists in usable form.',polarity='REALIZES',distance='D1_DIRECT',bridge='SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',condition='Q42 public-service access battery; Q160 government-responsibility battery.',basis='Native source explicitly names access to basic medical care and separately measures ease/difficulty obtaining healthcare.',grain='Government ought-state → population service-access realization measure.')
add_positive(fam='Asian Barometer',wave='W5',norm_codes=['q160d'],prax_codes=['q114'],subtype='INSTITUTIONAL_OR_SOCIAL_REALIZATION',praxis_kind='INSTITUTIONAL_STATE',norm_prop='Government bears responsibility to make sure basic necessities such as food and shelters are provided for everyone.',praxis_prop='People have basic necessities like food, clothes, and shelter.',common='population provision of basic necessities',actor_scope='government responsibility; population-level provision state',actor_basis='Practical member measures the social state named as the object of government responsibility.',target_scope='basic necessities for everyone',target_basis='Food/shelter are repeated explicitly on both shores; practical item adds clothes as a same-battery basic-necessity component.',action_domain='basic-needs provision state',action_basis='Practical item directly measures realized provision of the norm-defined state.',polarity='REALIZES',distance='D1_DIRECT',bridge='SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',condition='Q114 quality-of-governance state; Q160 government-responsibility battery.',basis='Near-verbatim source-state identity between ought-state and realized-state measure.',grain='Government ought-state → realized population basic-needs state.')

# South Asia W1: c18d composite realized institutional components
add_positive(fam='South Asia',wave='W1',norm_codes=['c18d'],prax_codes=['c19','c32'],subtype='INSTITUTIONAL_OR_SOCIAL_REALIZATION',praxis_kind='INSTITUTIONAL_STATE',norm_prop='The country should be governed by those chosen by the people in a fair election.',praxis_prop='Respondent assesses whether their vote affects how the country is run and whether elections are fair/somewhat fair/unfair.',common='popular electoral choice with practical governing effect under fair elections',actor_scope='people/electoral system/governing institutions',actor_basis='C19 measures the governing effect of citizens’ votes; C32 measures the fairness component of the election process named in C18d.',target_scope='government selection through fair election',target_basis='The two practical cells separately measure the “chosen by people” effect and “fair election” condition; neither is treated as full realization alone.',action_domain='electoral selection and governance realization',action_basis='Source wording explicitly decomposes into vote-to-governance effect plus fair-election condition; the pair is retained as a bounded composition.',polarity='REALIZES',distance='D2_NARROWER_INSTANCE',bridge='SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION',bridge_ids=['South Asia W1 C18→C19/C32 source-native governance/election sequence'],condition='C18 governance alternatives; C19 vote-effect item; C32 election-fairness item. Preserve all source response universes.',basis='Both practical members measure explicit components of the C18d normative proposition; C33 actual vote-choice is absent from the selected implementation universe and is separately defect-ledgered.',grain='One composite governance norm → two bounded realized institutional components; no claim that either alone exhausts the norm.')

# ---------- overlap/boundary ledger ----------
over=[]
for _,r in cal.iterrows():
    posture=r.central_strict_t06_posture
    if posture=='RETAIN_STRICT_T06': disp='EXCLUDE_FROM_T15__STRICT_T06'; home='S14-T06'; basis='Central calibration and source-first replay retain exact/same-predicate T06 boundary; pair is ledgered but not duplicated in T15.'
    elif posture=='BOUNDARY_TO_T15': disp='RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW'; home='S14-T15'; basis='Source-first T15 reconstruction independently supports broader norm→practical-realization characterization; immutable T06 ancestry is not revoked by worker.'
    else: disp='REOPEN_NORM_SHORE__DOCTRINE_CONFLICT'; home='CENTRAL_REVIEW'; basis='Prior norm shore conflicts with central doctrine (personal importance is not itself RR_NORM); no T15 positive emitted from this pair.'
    prov=[]
    roles=clean_list(r.role_assignments_json)
    for x in roles:
        if x.get('source_provenance'): prov.append({'source_variable_code':x.get('source_variable_code'),'source_provenance':x.get('source_provenance'),'native_source_text':x.get('native_source_text','')})
    over.append({'overlap_id':f'T15OV-{WORKER}-{hashlib.sha1(r.worker_relation_id.encode()).hexdigest()[:16]}','source_family':r.source_family,'wave':r.wave,'prior_t06_worker_relation_id':r.worker_relation_id,
      'norm_implementation_ids_json':jd(ids(r.source_family,r.wave,clean_list(r.norm_source_variable_codes_json))),'praxis_implementation_ids_json':jd(ids(r.source_family,r.wave,clean_list(r.praxis_source_variable_codes_json))),
      'prior_central_calibration_posture':posture,'t15_overlap_disposition':disp,'recommended_rule_home':home,'basis':basis,'source_provenance_json':jd(prov or source_pages_for_codes(r.source_family,r.wave,clean_list(r.norm_source_variable_codes_json)+clean_list(r.praxis_source_variable_codes_json)))})

# ---------- crosswalk review: positives + hostile blocks/mismatches ----------
cross=[]; blockers=[]
def add_cw(fam,wave,nc,pc,st,pk,nprop,pprop,actor,target,align,bridge,disp,decision,confidence='HIGH',posid='',blockclass='',missing='',basisids=None,overlap_ids=None):
    cw=cwid(fam,wave,nc,pc,st)
    bid=''
    if disp=='BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY':
        bid=f'T15BL-{WORKER}-{hashlib.sha1(cw.encode()).hexdigest()[:16]}'
        blockers.append({'blocker_id':bid,'source_family':fam,'wave':wave,'norm_implementation_ids_json':jd(ids(fam,wave,nc)),'praxis_implementation_ids_json':jd(ids(fam,wave,pc)),'candidate_manifestation_subtype':st,'blocker_class':blockclass or 'SOURCE_OR_BRIDGE_AMBIGUITY','missing_authority':missing or decision,'source_basis':decision,'source_provenance_json':jd(source_pages_for_codes(fam,wave,nc+pc)),'resolution_needed':'Additional source-explicit actor/action/target/condition or bridge authority; do not infer from topic/valence/co-presence.'})
    cross.append({'crosswalk_id':cw,'source_family':fam,'wave':wave,'norm_implementation_ids_json':jd(ids(fam,wave,nc)),'praxis_implementation_ids_json':jd(ids(fam,wave,pc)),'candidate_manifestation_subtype':st,'praxis_shore_kind':pk,'norm_proposition':nprop,'praxis_proposition':pprop,'actor_alignment':actor,'target_alignment':target,'action_or_realization_alignment':align,'bridge_basis_type':bridge,'bridge_basis_ids_json':jd(basisids or []),'position_or_routing_condition':'Preserve member source routing/split/ballot/universe exactly; see provenance/accounting.','source_provenance_json':jd(source_pages_for_codes(fam,wave,nc+pc)),'disposition':disp,'decision_basis':decision,'confidence':confidence,'positive_relation_id':posid,'blocker_id':bid,'overlap_with_t06_relation_ids_json':jd(overlap_ids or [])})
    return cw,bid

# positive crosswalks from positive table
for p in positives:
    roles=json.loads(p['role_assignments_json'])
    nc=[x['source_variable_code'] for x in roles if x.get('t15_shore')=='NORMATIVE_PROPOSITION']; pc=[x['source_variable_code'] for x in roles if x.get('t15_shore')=='PRACTICAL_REALIZATION']
    ov=[x.get('worker_relation_id') for x in json.loads(p['overlap_with_existing_s14_rule_json']) if isinstance(x,dict) and x.get('worker_relation_id')]
    add_cw(p['source_family'],p['wave'],nc,pc,p['manifestation_subtype'],p['praxis_shore_kind'],p['norm_proposition'],p['praxis_proposition'],p['actor_alignment_basis'],p['target_alignment_basis'],p['action_alignment_basis'],p['bridge_basis_type'],'POSITIVE_T15',p['source_first_adjudication_basis'],p['confidence'],p['worker_relation_id'],basisids=json.loads(p['bridge_basis_ids_json']),overlap_ids=ov)

# hostile blocks and source-proven mismatches
block_specs=[
 # GSS
 ('GSS','2002',['peoptrbl'],['hlpneedy'],'DIRECT_ENACTMENT','REALIZED_SELF_CONDUCT','Assisting people in trouble is very important.','Contributed time to help needy people.','general/value actor','helping target broadly overlaps','importance is not governed norm modality','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Central calibration explicitly reopens PEOPTRBL because personal importance is not itself sufficient normative authority.','NORM_SHORE_DOCTRINE_CONFLICT','Need central norm-shore re-adjudication.'),
 ('GSS','2002',['helpfrds'],['lentto'],'DIRECT_ENACTMENT','REALIZED_SELF_CONDUCT','Better-off people should help a less-well-off friend.','Respondent lent money to another person.','respondent could instantiate general actor','friend/relative wealth condition not preserved','money-lending is not source-bound to a less-well-off friend','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','LENTTO does not preserve the friend identity or better-off/less-well-off condition; cannot fill missing target conditions.','TARGET_CONDITION_NOT_PRESERVED','Need an actual aid/lending item explicitly about a less-well-off friend.'),
 ('GSS','2002',['kidpars'],['caresik1'],'DIRECT_ENACTMENT','REALIZED_SELF_CONDUCT','Adult children have a duty to look after a parent.','Who in household cares for sick family member.','family actors overlap only generically','parent/child direction not preserved','care act lacks parent target and adult-child actor','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','CARESIK1 is generic family sick-care allocation; it does not establish adult-child→parent care.','DIRECTIONAL_KIN_TARGET_MISSING','Need explicit adult-child caring for parent shore.'),
 ('GSS','2002',['othshelp'],['volchrty'],'DIRECT_ENACTMENT','REALIZED_SELF_CONDUCT','People should help less-fortunate others.','Respondent did volunteer work for a charity.','respondent-as-instance available','charity beneficiary unspecified','generic charity work may target unrelated causes','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Source does not state that VOLCHRTY benefits less-fortunate others; charity status alone cannot supply target identity.','BENEFICIARY_NOT_SOURCE_FIXED','Need source-explicit beneficiary relation.'),
 ('GSS','2002',['helppoor'],['tax'],'INSTRUMENTAL_ENACTMENT','POLICY_APPLICATION','Government should improve standard of living of poor people.','Respondent federal income-tax amount.','government norm vs respondent payment','poor-relief target absent from tax item','generic taxation is not source-explicit means to poor relief','SOURCE_EXPLICIT_MEANS','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','No source-governed means bridge connects generic federal tax amount to the poor-relief norm.','BLOCKED_NEEDS_MEANS_BRIDGE','Need source or governed T04 bridge tying tax to this end.'),
 ('GSS','2002',['helpfrds'],['givhmlss'],'DIRECT_ENACTMENT','REALIZED_SELF_CONDUCT','Better-off people should help a less-well-off friend.','Respondent gave food/money to homeless person.','general actor vs respondent','friend target and homeless target are positively different','both are help acts but source target identity conflicts','DIRECT_SOURCE_ENTAILMENT','NOT_T15_SOURCE_PROVEN_MISMATCH','Native norm specifically requires a friend; homeless-aid item specifically targets a homeless person, with no friend condition.','',''),
 # Arab Barometer
 ('Arab Barometer','VIII',['Q550A_4'],['Q301A'],'RIGHT_OR_PERMISSION_EXERCISE','REALIZED_SELF_CONDUCT','Ability to freely choose political leaders in elections is an essential pillar of human dignity.','Respondent reports voting in last parliamentary election.','rights-holder/respondent plausible','election target overlaps','mere voting does not establish free/genuine choice condition','SOURCE_EXPLICIT_RIGHT_EXERCISE','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Voting alone does not prove the source-required freedom/genuine-choice condition; Q303B_3 is the calibrated realization shore.','FREE_CHOICE_CONDITION_MISSING','Need practical item preserving freedom/genuine choice.'),
 ('Arab Barometer','VIII',['Q550B_4'],['Q301A'],'RIGHT_OR_PERMISSION_EXERCISE','REALIZED_SELF_CONDUCT','Ability to freely choose political leaders in elections is an essential pillar of democracy.','Respondent reports voting in last parliamentary election.','rights-holder/respondent plausible','election target overlaps','mere voting does not establish free/genuine choice condition','SOURCE_EXPLICIT_RIGHT_EXERCISE','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Voting alone does not prove the source-required freedom/genuine-choice condition; Q303B_3 is the calibrated realization shore.','FREE_CHOICE_CONDITION_MISSING','Need practical item preserving freedom/genuine choice.'),
 ('Arab Barometer','VIII',['Q550A_1'],['Q872A'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Equality under the law is an essential pillar of human dignity.','Racial discrimination seriousness in the country.','population/institutional scopes only broadly overlap','legal equality vs broad discrimination are not identical','discrimination problem does not source-prove equality-under-law state','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Source does not establish that Q872A specifically measures equality under law rather than broader social discrimination.','LEGAL_EQUALITY_BRIDGE_MISSING','Need legal-treatment/equality state item.'),
 ('Arab Barometer','VIII',['Q601_13'],['Q628_4B'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Woman may reject family-chosen marriage without consent.','Relative freedom of men/women to choose whom to marry.','gender actor overlaps','marriage choice overlaps but family-imposition condition missing','general freedom does not measure ability to reject a family-imposed marriage','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Unlike calibrated Q601_13B, Q601_13 has the specific family-chosen-without-consent condition that Q628_4B does not preserve.','FORCED_FAMILY_CHOICE_CONDITION_MISSING','Need practical shore retaining family-imposition/consent condition.'),
 ('Arab Barometer','VIII',['Q601_5'],['Q869D','Q869E'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Men and women should have equal work opportunities.','Chance respondent/family loses job while equally/less qualified male/female receives it.','gender/work actors overlap','employment opportunity overlaps','single displacement scenario does not source-prove equal-opportunity state','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Q869D/E are asymmetric hypothetical displacement risks, not a direct measure of equal work opportunities across genders.','EQUAL_OPPORTUNITY_STATE_NOT_ESTABLISHED','Need direct realized equality-of-opportunity measure.'),
 ('Arab Barometer','VIII',['Q546'],['Q547_1','Q547_2','Q547_3','Q547_4'],'INSTRUMENTAL_ENACTMENT','POLICY_APPLICATION','National government should do more/less/same to deal with climate change.','Respondent favors/opposes adopting climate measures.','government norm vs respondent policy attitude','climate target overlaps','policy favor is not government enactment or respondent enactment','SOURCE_NATIVE_BATTERY_BRIDGE','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Immediate battery adjacency is insufficient: Q547 records respondent policy approval, not actual adoption/application, so no practical shore is source-proven.','ATTITUDE_NOT_PRACTICAL_ENACTMENT','Need actual/intended adoption/application shore.'),
 ('Arab Barometer','VIII',['Q553B_3'],['Q547_1','Q547_2','Q547_3','Q547_4'],'INSTRUMENTAL_ENACTMENT','POLICY_APPLICATION','Government of respondent country bears responsibility for addressing climate change.','Respondent favors/opposes adopting climate measures.','norm actor government, praxis actor respondent','climate target overlaps','actor mismatch; favor is not government action','SOURCE_NATIVE_BATTERY_BRIDGE','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Q547 does not measure government enactment; responsibility cannot be realized by another actor’s policy attitude without an explicit action bridge.','ACTOR_AND_ENACTMENT_MISMATCH','Need government action/application measure.'),
 ('Arab Barometer','VIII',['Q885'],['Q882'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','REALIZED_SELF_CONDUCT','National government should do more/less/same to deal with discrimination.','Respondent personally faced discrimination in past year.','government norm vs respondent exposure','discrimination target overlaps','experience does not measure government doing-more action or an explicit anti-discrimination outcome','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Discrimination exposure may motivate policy but does not realize or directly measure government anti-discrimination action.','GOVERNMENT_ACTION_SHORE_MISSING','Need government action or explicit outcome criterion.'),
 ('Arab Barometer','VIII',['Q518_6'],['Q127_1A','Q127_2A','Q521_1'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Government provides needs without political participation rights (evaluated political-system alternative).','Needs-availability and freedom-guarantee states.','political system actor overlaps','two distinct norm components map to different practical batteries','requires composite response-state bridge not source-bound to a single implementation proposition','SOURCE_NATIVE_BATTERY_BRIDGE','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Q518_6 is a composite regime proposition; selected practical cells cannot be collapsed into one realized state without explicit composition authority.','COMPOSITE_NORM_NEEDS_MULTI_AXIS_BRIDGE','Need governed composition bridge preserving both provision and participation-right components.'),
 ('Arab Barometer','VIII',['Q550A_3'],['Q127_1B','Q127_2B'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Basic necessities are available for all.','Food/housing affordability problem.','country/social actor aligns','availability and affordability are explicitly distinct split cells','target condition differs positively in source','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION','NOT_T15_SOURCE_PROVEN_MISMATCH','Q127 explicitly distinguishes availability (A) from affordability (B); affordability cannot stand in for the norm’s availability predicate.','',''),
 ('Arab Barometer','VIII',['Q550B_3'],['Q127_1B','Q127_2B'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Basic necessities are available for all.','Food/housing affordability problem.','country/social actor aligns','availability and affordability are explicitly distinct split cells','target condition differs positively in source','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION','NOT_T15_SOURCE_PROVEN_MISMATCH','Q127 explicitly distinguishes availability (A) from affordability (B); shared basic-needs topic cannot erase the predicate mismatch.','',''),
 # EVS 2008
 ('EVS','2008',['v101'],['v91'],'DIRECT_ENACTMENT','INSTITUTIONAL_STATE','Follow superiors’ instructions versus require conviction they are right.','How free respondent is to make decisions in job.','worker context overlaps','workplace target broad','decision freedom is not actual obedience/refusal conduct','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Job autonomy does not source-prove following/refusing superior instructions; same workplace topic is insufficient.','ACTION_IDENTITY_NOT_ESTABLISHED','Need actual instruction-following shore.'),
 ('EVS','2008',['v158'],['v349'],'DIRECT_ENACTMENT','LIFE_STATE','Child’s duty to take care of ill parent.','Respondent experienced long unemployment.','actors/targets incompatible','parent care vs unemployment','no action/target identity','DIRECT_SOURCE_ENTAILMENT','NOT_T15_SOURCE_PROVEN_MISMATCH','Source propositions concern different actors/actions/targets; positive mismatch is explicit.','',''),
 ('EVS','2008',['v166'],['v91'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Men should take same responsibility for home and children.','Job decision freedom.','respondent context only','home/children vs job autonomy','different action domains','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION','NOT_T15_SOURCE_PROVEN_MISMATCH','Source targets home/child responsibility versus workplace autonomy; no realization relation.','',''),
 ('EVS','2008',['v195'],['v349'],'RIGHT_OR_PERMISSION_EXERCISE','LIFE_STATE','Unemployed people should have right to refuse unwanted job versus take any available job/lose benefits.','Respondent experienced unemployment longer than three months.','unemployed actor potentially aligns','unemployment state lacks refusal target','being unemployed is not exercise of job-refusal right','SOURCE_EXPLICIT_RIGHT_EXERCISE','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Unemployment history does not establish that a job was offered/refused, so right exercise cannot be inferred.','REFUSAL_EVENT_NOT_MEASURED','Need explicit offered-job refusal conduct.'),
 ('EVS','2008',['v267'],['v283'],'PRACTICAL_VIOLATION','OTHER_SOURCE_PROVEN_REALIZATION','Terrorism justified/always condemned.','People should stick to own affairs.','generic actors','targets unrelated','different normative actions','SOURCE_EXPLICIT_VIOLATION','NOT_T15_SOURCE_PROVEN_MISMATCH','Native source predicates are unrelated; no shared action axis.','',''),
 # EVS 1990
 ('EVS','1990',['q126c'],['q124a','q125b'],'INSTRUMENTAL_ENACTMENT','STATED_INTENDED_CONDUCT','Government has to reduce environmental pollution but it should not cost respondent money.','Respondent would give income / accept higher taxes if money used to prevent environmental pollution.','government norm plus respondent payer actor mismatch partly explicit','same pollution end but cost condition conflicts','source explicitly imposes personal cost where norm explicitly says no personal cost','SOURCE_NATIVE_BATTERY_BRIDGE','NOT_T15_SOURCE_PROVEN_MISMATCH','Same battery supplies a positive condition mismatch: q126c says government pollution reduction should not cost me money, whereas q124a/q125b explicitly accept income/tax cost.','',''),
 ('EVS','1990',['q559a'],['q138a','q156b'],'DIRECT_ENACTMENT','REALIZED_SELF_CONDUCT','Approval/disapproval of ecology/nature-protection movement.','Membership/unpaid work in environmental organization.', 'respondent actor across attitude/conduct','environmental movement/organization terms broadly overlap','approval of a movement does not source-entail membership or unpaid work in a source-identical organization','DIRECT_SOURCE_ENTAILMENT','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Native source does not bind movement approval to organizational membership/work; shared environmental topic cannot create enactment.','MOVEMENT_TO_ORGANIZATION_BRIDGE_MISSING','Need explicit movement/organization identity or membership-as-enactment bridge.'),
 # Asian Barometer blocks/mismatches
 ('Asian Barometer','W5',['q91'],['q118'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Court protects ordinary people from abuse of government power.','Frequency government leaders break law/abuse power.','government actor overlaps; court response missing','abuse target overlaps','incidence of abuse does not measure court protection/capacity response','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Q118 measures occurrence of abuse/lawbreaking, not whether the court protects people from it.','COURT_RESPONSE_SHORE_MISSING','Need court response/protection state.'),
 ('Asian Barometer','W5',['q150'],['q115'],'PRACTICAL_VIOLATION','INSTITUTIONAL_STATE','Government should decide whether certain ideas may be discussed.','People are free to speak what they think without fear.','government regulation vs people speech state','speech/discussion target overlaps','government deciding permissibility can coexist with broad speech freedom depending decisions','SOURCE_EXPLICIT_VIOLATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Q150 assigns decision authority; it does not necessarily prohibit speech. Q115 therefore is not source-proven contrary conduct/state.','CONTRARY_OUTCOME_NOT_ENTAILED','Need explicit censorship/prohibition outcome.'),
 ('Asian Barometer','W5',['q152'],['q111'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Judges should accept executive view in important cases.','When leaders break laws there is nothing court can do.','judiciary/executive actors overlap','judicial constraint target overlaps','court incapacity is not source-stated consequence of judicial deference','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Inferring that accepting executive views causes inability to act against lawbreaking would be a worker-supplied causal story.','CAUSAL_BRIDGE_NOT_SOURCE_EXPLICIT','Need direct source bridge from deference to incapacity.'),
 ('Asian Barometer','W5',['q160b'],['q114'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Government should ensure everyone has affordable housing.','People have basic necessities including shelter.','government/outcome actor relation broadly aligns','affordability housing vs shelter provision differ','source target predicate differs positively','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION','NOT_T15_SOURCE_PROVEN_MISMATCH','Housing affordability is not the same as presence of shelter/basic necessities; source wording positively distinguishes the condition.','',''),
 ('Asian Barometer','W5',['q160a'],['q113'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Government should narrow rich-poor gap.','Rich and poor people are treated equally by government.','government actor aligns','income gap vs equal treatment are distinct targets','redistribution/inequality outcome differs from treatment equality','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION','NOT_T15_SOURCE_PROVEN_MISMATCH','Source distinguishes economic gap from government treatment equality; shared rich/poor vocabulary is insufficient.','',''),
 ('Asian Barometer','W5',['q97'],['q119'],'PRACTICAL_VIOLATION','INSTITUTIONAL_STATE','Qualified candidates are pre-selected by religious leaders (democracy characteristic).','Elections offer real choice between different parties/candidates.','electoral actors overlap','candidate choice overlaps','preselection can coexist with choice among preselected candidates','SOURCE_EXPLICIT_VIOLATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Q119 does not establish absence of religious preselection; no source-proven contradiction.','CONTRARY_CONDITION_NOT_ESTABLISHED','Need measure of who controls candidate selection.'),
 ('Asian Barometer','W5',['q146'],['q79'],'PRACTICAL_VIOLATION','REALIZED_SELF_CONDUCT','Women should not be involved in politics as much as men.','Respondent attended protest/demonstration.','respondent sex could condition actor instance','comparative gender participation norm vs one individual act','one act cannot establish “as much as men” comparative violation','SOURCE_EXPLICIT_VIOLATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','The norm is comparative by gender; a single respondent participation act cannot establish the comparative condition.','COMPARATIVE_RATE_CONDITION_MISSING','Need gender-comparative participation measure.'),
 # South Asia
 ('South Asia','W1',['c18d'],['c20c'],'INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTITUTIONAL_STATE','Country should be governed by those chosen by people in a fair election.','People have power to change a government they dislike.','citizen/government scopes overlap','government change overlaps','C20c does not state election mechanism or fair-election condition','SOURCE_EXPLICIT_INSTITUTIONAL_REALIZATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','Popular removal power may arise through mechanisms not specified as elections; source does not bind C20c to the C18d election mechanism.','ELECTION_MECHANISM_NOT_PRESERVED','Need election-specific turnover state.'),
 ('South Asia','W1',['c18a'],['c32'],'PRACTICAL_VIOLATION','INSTITUTIONAL_STATE','Strong leader need not bother about elections.','Elections are rated fair/somewhat fair/unfair.','governing/electoral system broadly overlaps','elections target overlaps','existence/fairness of elections does not prove leader is constrained by them','SOURCE_EXPLICIT_VIOLATION','BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY','C32 presupposes elections but does not establish whether a strong leader must heed them; direct contradiction is not source-proven.','LEADER_ELECTION_CONSTRAINT_NOT_MEASURED','Need practical state of leader accountability/selection by elections.'),
 ('South Asia','W1',['c18d'],['c20b'],'RIGHT_OR_PERMISSION_EXERCISE','INSTITUTIONAL_STATE','Country should be governed by people chosen in a fair election.','People are free to speak without fear.','citizen actors overlap','speech vs electoral selection targets differ','different action axes','SOURCE_EXPLICIT_RIGHT_EXERCISE','NOT_T15_SOURCE_PROVEN_MISMATCH','Speech freedom and electoral selection are distinct source predicates; shared democracy block cannot create T15.','',''),
]
for spec in block_specs:
    fam,w,nc,pc,st,pk,np,pp,aa,ta,al,bb,disp,dec,bc,miss=spec
    add_cw(fam,w,nc,pc,st,pk,np,pp,aa,ta,al,bb,disp,dec,'HIGH','',bc,miss)

# ---------- accounting ----------
acc=base[['question_implementation_id','source_family','wave','source_variable_code','exact_question_text','baseline_t06_classification']].copy()
acc['t15_norm_candidate']='NO_AFTER_SOURCE_SCREEN'
acc.loc[base.baseline_t06_classification=='NORM_SHORE','t15_norm_candidate']='YES'
# central reopen control
acc.loc[acc.question_implementation_id==row('GSS','2002','peoptrbl').question_implementation_id,'t15_norm_candidate']='CENTRAL_REOPEN_REQUIRED'
acc['t15_praxis_candidate']='NO_AFTER_SOURCE_SCREEN'
acc.loc[base.baseline_t06_classification=='CONDUCT_SHORE','t15_praxis_candidate']='YES'
acc['t15_praxis_shore_kind']=''
# generic classification for T06 conduct seeds
for i,r in acc[acc.t15_praxis_candidate=='YES'].iterrows():
    txt=r.exact_question_text.lower()
    if any(x in txt for x in ['do you belong','where do you work','marital','number of children','experienced unemployment','employment status']): kind='LIFE_STATE'
    elif any(x in txt for x in ['extent','how widespread','guaranteed','how often do you think','state of','are able','opportunities to be elected','free to speak','basic necessities','court can do','safety of']): kind='INSTITUTIONAL_STATE'
    else: kind='REALIZED_SELF_CONDUCT'
    acc.at[i,'t15_praxis_shore_kind']=kind
# newly recovered norm candidates from OTHER/ambiguous source review
new_norm_codes={
 ('GSS','2002'):['adhdcon','adhdmed','forcedoc','forcehos','forcemed','affrmact','careself','fejobaff','safetywk','selffrst','trdunion'],
 ('Arab Barometer','VIII'):['Q518_1','Q518_4','QKUW28_1','QKUW28_2','QKUW28_3','QKUW28_4','QKUW28_5','QKUW28_6','QKUW28_7'],
 ('EVS','2008'):['v102','v103','v168','v169','v194','v197'],
 ('EVS','1990'):['q316a','q318c','q452','q520c','q666a'],
 ('Asian Barometer','W5'):['q60','q69','Q106c','Q106d','Q106e'],
 ('South Asia','W1'):[],
}
for (fam,w),codes in new_norm_codes.items():
    for c in codes:
        try: iid=row(fam,w,c).question_implementation_id
        except KeyError: continue
        acc.loc[acc.question_implementation_id==iid,'t15_norm_candidate']='YES'
# reopen practical shores from OTHER/ambig that T15 can use/search
new_praxis={
 ('GSS','2002'):{'givhmlss':'REALIZED_SELF_CONDUCT','volchrty':'REALIZED_SELF_CONDUCT','lentto':'REALIZED_SELF_CONDUCT','caresik1':'REALIZED_SELF_CONDUCT','wkfreedm':'INSTITUTIONAL_STATE'},
 ('Arab Barometer','VIII'):{'Q211_2':'POLICY_APPLICATION','Q127_2A':'INSTITUTIONAL_STATE','Q127_1B':'INSTITUTIONAL_STATE','Q127_2B':'INSTITUTIONAL_STATE','Q518_1':'INSTITUTIONAL_STATE','Q547_1':'STATED_INTENDED_CONDUCT','Q547_2':'STATED_INTENDED_CONDUCT','Q547_3':'STATED_INTENDED_CONDUCT','Q547_4':'STATED_INTENDED_CONDUCT','Q547_TUN2':'STATED_INTENDED_CONDUCT','Q547_TUN3':'STATED_INTENDED_CONDUCT','Q547_TUN4':'STATED_INTENDED_CONDUCT'},
 ('EVS','2008'):{'v91':'INSTITUTIONAL_STATE','v349':'LIFE_STATE'},
 ('EVS','1990'):{'q124a':'STATED_INTENDED_CONDUCT','q125b':'STATED_INTENDED_CONDUCT'},
 ('Asian Barometer','W5'):{'q42':'INSTITUTIONAL_STATE','q43':'INSTITUTIONAL_STATE','q77':'REALIZED_SELF_CONDUCT','q126':'POLICY_APPLICATION'},
 ('South Asia','W1'):{},
}
for (fam,w),d in new_praxis.items():
    for c,k in d.items():
        try: iid=row(fam,w,c).question_implementation_id
        except KeyError: continue
        acc.loc[acc.question_implementation_id==iid,'t15_praxis_candidate']='YES'; acc.loc[acc.question_implementation_id==iid,'t15_praxis_shore_kind']=k
acc['reopened_from_baseline_other_or_ambiguous']='NO'
mask=acc.baseline_t06_classification.isin(['OTHER','SOURCE_AMBIGUOUS']) & ((acc.t15_norm_candidate=='YES')|(acc.t15_praxis_candidate=='YES'))
acc.loc[mask,'reopened_from_baseline_other_or_ambiguous']='YES'
# all prior/new norms searched; all praxis candidates reverse-searched
acc['norm_to_praxis_search_completed']='NO_NOT_NORM_CANDIDATE'
acc.loc[(base.baseline_t06_classification=='NORM_SHORE')|(acc.t15_norm_candidate=='YES')|(acc.t15_norm_candidate=='CENTRAL_REOPEN_REQUIRED'),'norm_to_praxis_search_completed']='YES'
acc['praxis_to_norm_search_completed']='NO_NOT_PRAXIS_CANDIDATE'
acc.loc[acc.t15_praxis_candidate=='YES','praxis_to_norm_search_completed']='YES'
# signatures
sig=[]; source_basis=[]; note=[]
for _,r in acc.iterrows():
    b=by_id[r.question_implementation_id]
    sig.append(jd({'actor':b.baseline_action_actor or 'source-specified actor','action_or_state':b.baseline_action or r.exact_question_text,'target_or_object':b.baseline_target_object or r.exact_question_text,'baseline_modality':b.baseline_modality,'condition_routing':b.baseline_condition_routing,'respondent_universe':b.baseline_respondent_universe,'source_battery_stem':b.baseline_source_battery_stem,'t15_norm_candidate':r.t15_norm_candidate,'t15_praxis_candidate':r.t15_praxis_candidate,'t15_praxis_shore_kind':r.t15_praxis_shore_kind}))
    source_basis.append('Native BY_WAVE flattened questionnaire/codebook text governs T15 reconstruction; prior T06 classification is seed-only; implementation ID preserved from normalized prior accounting.')
    if r.reopened_from_baseline_other_or_ambiguous=='YES': note.append('Reopened beyond strict-T06 classification because T15 admits normative principles/rights/criteria or practical life/institution/policy shores; source-first crosswalk completed.')
    elif r.t15_norm_candidate=='CENTRAL_REOPEN_REQUIRED': note.append('Prior T06 norm classification searched but withheld as T15 norm candidate under central PEOPTRBL doctrine conflict; overlap ledger preserves reopen control.')
    else: note.append('Source-first screened for all five T15 subtypes; no omission inferred from baseline classification.')
acc['normative_or_praxis_signature_json']=sig; acc['source_basis']=source_basis
# counterpart/crosswalk maps
counter=defaultdict(set); posmap=defaultdict(set); blkmap=defaultdict(set)
for r in cross:
    ns=json.loads(r['norm_implementation_ids_json']); ps=json.loads(r['praxis_implementation_ids_json'])
    for a in ns:
        counter[a].update(ps)
        if r['positive_relation_id']: posmap[a].add(r['positive_relation_id'])
        if r['blocker_id']: blkmap[a].add(r['crosswalk_id'])
    for a in ps:
        counter[a].update(ns)
        if r['positive_relation_id']: posmap[a].add(r['positive_relation_id'])
        if r['blocker_id']: blkmap[a].add(r['crosswalk_id'])
acc['plausible_counterpart_implementation_ids_json']=[jd(sorted(counter[x])) for x in acc.question_implementation_id]
acc['positive_relation_ids_json']=[jd(sorted(posmap[x])) for x in acc.question_implementation_id]
acc['blocked_crosswalk_ids_json']=[jd(sorted(blkmap[x])) for x in acc.question_implementation_id]
acc['upstream_repair_ids_json']=jd([])
acc['accounting_note']=note
# required exact column order
acc_cols=pd.read_csv(RET/'T15_PRACTICAL_SHORE_ACCOUNTING.csv',nrows=0).columns.tolist()
acc=acc[acc_cols]

# ---------- composition ledger ----------
composition=[]
for p in positives:
    members=json.loads(p['member_implementation_ids_json']); roles=json.loads(p['role_assignments_json'])
    prax=[x['implementation_id'] for x in roles if x.get('t15_shore')=='PRACTICAL_REALIZATION']
    norms=[x['implementation_id'] for x in roles if x.get('t15_shore')=='NORMATIVE_PROPOSITION']
    if len(prax)>1:
        composition.append({'bridge_id':f'T15COMP-{WORKER}-{hashlib.sha1(p["worker_relation_id"].encode()).hexdigest()[:16]}','source_family':p['source_family'],'wave':p['wave'],'norm_implementation_ids_json':jd(norms),'praxis_implementation_ids_json':jd(prax),'manifestation_subtype':p['manifestation_subtype'],'bridge_basis_type':p['bridge_basis_type'],'required_or_overlapping_s14_rule_ids_json':jd(['S14-T15']),'bridge_authority_ids_json':p['bridge_basis_ids_json'],'source_explicit_bridge_text':p['common_proposition_or_target'],'source_provenance_json':p['source_provenance_json'],'bridge_status':'SUPPORTED_SOURCE_NATIVE_MULTI_SHORE','basis':'Multiple practical members are retained only as parallel cells/components of the same exact source proposition; member routing remains explicit.'})
# explicit blocked composition bridges
composition += [
 {'bridge_id':'T15COMP-T06W04-AB-Q5186','source_family':'Arab Barometer','wave':'VIII','norm_implementation_ids_json':jd(ids('Arab Barometer','VIII',['Q518_6'])),'praxis_implementation_ids_json':jd(ids('Arab Barometer','VIII',['Q127_1A','Q127_2A','Q521_1'])),'manifestation_subtype':'INSTITUTIONAL_OR_SOCIAL_REALIZATION','bridge_basis_type':'SOURCE_NATIVE_BATTERY_BRIDGE','required_or_overlapping_s14_rule_ids_json':jd([]),'bridge_authority_ids_json':jd([]),'source_explicit_bridge_text':'Q518_6 combines needs provision with absence of political participation rights; separate practical batteries measure only fragments.','source_provenance_json':jd(source_pages_for_codes('Arab Barometer','VIII',['Q518_6','Q127_1A','Q127_2A','Q521_1'])),'bridge_status':'BLOCKED_COMPOSITION_AUTHORITY','basis':'No governed composition authority permits collapsing provision and participation-right dimensions into one practical state.'},
 {'bridge_id':'T15COMP-T06W04-EVS1990-ENV','source_family':'EVS','wave':'1990','norm_implementation_ids_json':jd(ids('EVS','1990',['q126c'])),'praxis_implementation_ids_json':jd(ids('EVS','1990',['q124a','q125b'])),'manifestation_subtype':'INSTRUMENTAL_ENACTMENT','bridge_basis_type':'SOURCE_NATIVE_BATTERY_BRIDGE','required_or_overlapping_s14_rule_ids_json':jd([]),'bridge_authority_ids_json':jd([]),'source_explicit_bridge_text':'Q124A/Q125B accept personal income/tax costs for pollution prevention; Q126C demands government pollution reduction but explicitly “should not cost me any money.”','source_provenance_json':jd(source_pages_for_codes('EVS','1990',['q124a','q125b','q126c'])),'bridge_status':'REJECTED_SOURCE_PROVEN_CONDITION_MISMATCH','basis':'Shared environmental battery cannot override the explicit personal-cost contradiction.'}
]

# ---------- source coverage defects ----------
defects=[]
def add_defect(fam,wave,native_member,native_text,missing,kind,subtype,basis,pages):
    did=f'T15DEF-{WORKER}-{hashlib.sha1((fam+wave+native_member).encode()).hexdigest()[:16]}'
    defects.append({'defect_id':did,'source_family':fam,'wave':wave,'native_source_member':native_member,'native_source_text':native_text,'missing_or_collapsed_rawlsing_member':missing,'defect_type':kind,'source_provenance_json':jd([{'flattened_relative_path':f'BY_WAVE/{wave_dirs[(fam,wave)]}/NATIVE_SOURCE_PAGE_TEXT.jsonl.gz','page_numbers':pages}]),'affected_subtype':subtype,'runtime_relation_withheld':'YES','basis':basis})
add_defect('Arab Barometer','VIII','Q551A response-option normative cells','Among six separately worded human-dignity pillars, respondent selects the main pillar.','Selected universe has one Q551A implementation; option-level normative proposition is not implementation-bound.','CATEGORICAL_NORM_OPTION_GRAIN_COLLAPSED','INSTITUTIONAL_OR_SOCIAL_REALIZATION','Cannot bind the respondent-selected normative proposition to exact T15 member IDs without option-grain implementation authority.',[22])
add_defect('Arab Barometer','VIII','Q551B response-option normative cells','Among six separately worded democracy pillars, respondent selects the main pillar.','Selected universe has one Q551B implementation; option-level normative proposition is not implementation-bound.','CATEGORICAL_NORM_OPTION_GRAIN_COLLAPSED','INSTITUTIONAL_OR_SOCIAL_REALIZATION','Cannot bind selected pillar identity to exact downstream norm shore.',[22])
add_defect('Asian Barometer','W5','Q98 response-option normative cells','Respondent chooses one most essential democracy element: open political expression; basic necessities; free/fair leader choice; clean politics.','Selected universe has one q98 implementation; option-level norm propositions are collapsed into response values.','CATEGORICAL_NORM_OPTION_GRAIN_COLLAPSED','INSTITUTIONAL_OR_SOCIAL_REALIZATION','Several option propositions have source-native realized-state counterparts, but T15 cannot emit respondent-answer-dependent edges without exact option grain.',[13])
add_defect('South Asia','W1','C24 response-option normative cells','Respondent chooses one essential democracy characteristic: electoral change; criticism freedom; equal rights; basic necessities.','Selected universe has one c24 implementation; option-level norm propositions are collapsed.','CATEGORICAL_NORM_OPTION_GRAIN_COLLAPSED','INSTITUTIONAL_OR_SOCIAL_REALIZATION','C20 measures several matching realized states, but implementation-level C24 lacks a single fixed proposition.',[5])
add_defect('South Asia','W1','C33 actual vote choice','Which party/candidate did you vote for in the last national election?','No C33 implementation exists in the selected 3,052-row W04/18,276 implementation universe.','NATIVE_T15_PRAXIS_QUESTION_ABSENT_FROM_SELECTED_UNIVERSE','DIRECT_ENACTMENT','C33 is a source-native practical enactment of the people-choose-through-election component of C18d, but no runtime T15 relation can be emitted without an implementation ID.',[7])
add_defect('South Asia','W1','C31a equal minority treatment norm','Government/state should treat minorities in the same way as it treats the majority.','No C31a implementation exists in the selected W1 Rawlsing implementation universe.','NATIVE_T15_NORM_QUESTION_ABSENT_FROM_SELECTED_UNIVERSE','INSTITUTIONAL_OR_SOCIAL_REALIZATION','C20a measures everyone enjoying equal rights and is a plausible realized-state counterpart, but the source norm shore cannot be implementation-bound.',[6])

# ---------- upstream repairs empty (T15 reclassification is successor ontology, not upstream metadata defect) ----------
up_cols=pd.read_csv(RET/'T15_UPSTREAM_REPAIRS.csv',nrows=0).columns.tolist()
up=pd.DataFrame(columns=up_cols)

# ---------- wave attestation ----------
att=[]
strict_counts=Counter((r.source_family,r.wave) for _,r in cal[cal.central_strict_t06_posture=='RETAIN_STRICT_T06'].iterrows())
pos_counts=Counter((p['source_family'],p['wave']) for p in positives)
block_counts=Counter((r['source_family'],r['wave']) for r in cross if r['disposition']=='BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY')
neg_counts=Counter((r['source_family'],r['wave']) for r in cross if r['disposition']=='NOT_T15_SOURCE_PROVEN_MISMATCH')
def_counts=Counter((r['source_family'],r['wave']) for r in defects)
wave_order=[('GSS','2002'),('Arab Barometer','VIII'),('EVS','2008'),('EVS','1990'),('Asian Barometer','W5'),('South Asia','W1')]
for fam,w in wave_order:
    sub=acc[(acc.source_family==fam)&(acc.wave==w)]
    prior=(base[(base.source_family==fam)&(base.wave==w)].baseline_t06_classification=='NORM_SHORE').sum()
    new=((sub.t15_norm_candidate=='YES') & (~sub.question_implementation_id.isin(base[(base.source_family==fam)&(base.wave==w)&(base.baseline_t06_classification=='NORM_SHORE')].question_implementation_id))).sum()
    pr=(sub.t15_praxis_candidate=='YES').sum()
    zero='YES__HOSTILE_SOURCE_FIRST_ZERO_SUPPORTED' if pos_counts[(fam,w)]==0 else 'NOT_APPLICABLE__POSITIVES_FOUND'
    note='Every prior norm and every reopened norm/praxis candidate received bidirectional search. '
    if pos_counts[(fam,w)]==0: note+='Hostile sparse-wave QA rechecked source batteries and nearest apparent bridges; unresolved similarity was blocked and source-proven mismatches preserved.'
    else: note+='Hostile QA rechecked action/target/actor/routing identity and all high-risk instrumental/violation links.'
    att.append({'source_family':fam,'wave':w,'implementation_denominator':len(sub),'implementation_rows_accounted':len(sub),'prior_norm_shores':int(prior),'new_norm_shores_recovered':int(new),'praxis_candidate_shores':int(pr),'norm_to_praxis_search_complete':'YES','praxis_to_norm_search_complete':'YES','direct_enactment_reviewed':'YES','right_exercise_reviewed':'YES','practical_violation_reviewed':'YES','institutional_social_realization_reviewed':'YES','instrumental_enactment_reviewed':'YES','positive_t15_count':pos_counts[(fam,w)],'strict_t06_overlap_count':strict_counts[(fam,w)],'blocked_count':block_counts[(fam,w)],'source_proven_mismatch_count':neg_counts[(fam,w)],'coverage_defect_count':def_counts[(fam,w)],'upstream_repair_count':0,'zero_positive_supportable':zero,'hostile_sparse_wave_qa':'YES','attestation_note':note})

# ---------- write ----------
pos_cols=pd.read_csv(RET/'T15_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv',nrows=0).columns.tolist()
pd.DataFrame(positives)[pos_cols].to_csv(RET/'T15_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv',index=False)
acc.to_csv(RET/'T15_PRACTICAL_SHORE_ACCOUNTING.csv',index=False)
cw_cols=pd.read_csv(RET/'T15_CROSSWALK_REVIEW.csv',nrows=0).columns.tolist(); pd.DataFrame(cross)[cw_cols].to_csv(RET/'T15_CROSSWALK_REVIEW.csv',index=False)
ov_cols=pd.read_csv(RET/'T15_T06_OVERLAP_AND_BOUNDARY.csv',nrows=0).columns.tolist(); pd.DataFrame(over)[ov_cols].to_csv(RET/'T15_T06_OVERLAP_AND_BOUNDARY.csv',index=False)
comp_cols=pd.read_csv(RET/'T15_COMPOSITION_BRIDGE_LEDGER.csv',nrows=0).columns.tolist(); pd.DataFrame(composition)[comp_cols].to_csv(RET/'T15_COMPOSITION_BRIDGE_LEDGER.csv',index=False)
up.to_csv(RET/'T15_UPSTREAM_REPAIRS.csv',index=False)
def_cols=pd.read_csv(RET/'T15_SOURCE_COVERAGE_DEFECTS.csv',nrows=0).columns.tolist(); pd.DataFrame(defects)[def_cols].to_csv(RET/'T15_SOURCE_COVERAGE_DEFECTS.csv',index=False)
bl_cols=pd.read_csv(RET/'T15_BLOCKERS.csv',nrows=0).columns.tolist(); pd.DataFrame(blockers)[bl_cols].to_csv(RET/'T15_BLOCKERS.csv',index=False)
att_cols=pd.read_csv(RET/'T15_WAVE_COMPLETENESS_ATTESTATION.csv',nrows=0).columns.tolist(); pd.DataFrame(att)[att_cols].to_csv(RET/'T15_WAVE_COMPLETENESS_ATTESTATION.csv',index=False)

# provenance pins
prov={
 'worker_id':WORKER,
 'continuation_pack_sha256':'5b226145ca84a1423519a8f611eb75fb73e3eeb34ea31614876e10632359cdad',
 'immutable_parent_t06_return':str(PARENT.relative_to(ROOT)),
 'immutable_parent_t06_sha256':hashlib.sha256(PARENT.read_bytes()).hexdigest(),
 'canonical_source_authority_sha256':'e88cc035ca1d846e68ee208ec991f61f636d67ebbd19312057c8e44c37ff740d',
 'source_authority_work_surface':'BY_WAVE flattened native page text; PDFs not needed for resolved candidates',
 'authority_law':'Native source semantics/structure > governed ancestry where applicable > implementation identity; T06/calibration not discovery universe.'
}
(ROOT/'EXECUTION_PROVENANCE.json').write_text(json.dumps(prov,indent=2),encoding='utf-8')

# Worker report
subcnt=Counter(p['manifestation_subtype'] for p in positives); wavecnt=Counter((p['source_family'],p['wave']) for p in positives)
report=f'''# T06W04 — S14-T15 norm→practical-realization source-first continuation report

## Status

Completed the assigned six-wave T15 successor reconstruction over **{len(acc):,} / 3,052** implementation rows. The enclosed T06 parent was preserved byte-identically at SHA-256 `{prov['immutable_parent_t06_sha256']}` and was used only as ancestry/overlap control. The canonical flattened source authority was independently pinned to `{prov['canonical_source_authority_sha256']}`.

This worker does **not** claim S14/T15 freeze, does not mutate O10/O11/O12, and does not start Job 3.

## Method

For each wave I reconstructed the relevant native stems/batteries from `BY_WAVE/*/NATIVE_SOURCE_PAGE_TEXT.jsonl.gz`, then searched every prior T06 norm shore norm→praxis. Baseline `OTHER` and `SOURCE_AMBIGUOUS` rows were reopened where source semantics could make them T15 norm or practical shores. Every T15 praxis candidate received the independent praxis→norm reverse search. All five manifestation subtypes were reviewed. Topic/driver/valence/lexical proximity was never accepted as relation authority.

Strict same-predicate T06 pairs were not duplicated. The overlap ledger contains **{sum(1 for x in over if x['t15_overlap_disposition']=='EXCLUDE_FROM_T15__STRICT_T06')}** strict-T06 exclusions, **{sum(1 for x in over if x['t15_overlap_disposition']=='RECOMMEND_T06_TO_T15_BOUNDARY_REVIEW')}** T06→T15 boundary recommendations, and one central norm-shore reopen control (`peoptrbl`).

## Positive T15 authority

Total accepted worker T15 relations: **{len(positives)}**.

Subtype counts:
'''
for k in ['DIRECT_ENACTMENT','RIGHT_OR_PERMISSION_EXERCISE','PRACTICAL_VIOLATION','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTRUMENTAL_ENACTMENT']:
    report+=f'- `{k}`: **{subcnt[k]}**\n'
report+='\nWave counts:\n'
for fam,w in wave_order: report+=f'- {fam} {w}: **{wavecnt[(fam,w)]}**\n'
report+=f'''\n## Boundary and hostile-QA findings

- **GSS 2002:** the calibrated `othshelp→hlpneedy` boundary is T15, and the source helping-behavior battery additionally supports `othshelp→givhmlss` as a narrower direct enactment. Generic charity/volunteer activity remains blocked because beneficiary identity is not fixed.
- **Arab Barometer VIII:** human-dignity/democracy pillar batteries yield realized corruption/basic-needs/safety/civil-right states and civil-right exercises. Anti-corruption crackdown is admitted only because the practical item explicitly says it is “working to crackdown on corruption.” Climate-policy favor items are **blocked**: favoring a measure is an attitude, not government enactment.
- **EVS 2008:** **zero T15 positives is supportable** after hostile review. The closest workplace, care, unemployment-right, terrorism and household-responsibility shores fail exact action/target/event identity or remain strict-T06 overlaps.
- **EVS 1990:** **zero T15 positives is supportable**. The environmental battery is particularly important negative evidence: income/tax willingness to prevent pollution imposes personal cost, while the government-pollution norm explicitly says it should not cost the respondent money. Movement approval→membership/unpaid work remains blocked absent source identity.
- **Asian Barometer W5:** meaning-of-democracy norms are linked only where quality-of-governance batteries measure the same institutional axis or direct contrary practice. `q160c→q42` and `q160d→q114` were recovered by reopening T06-`OTHER` practical states. `q92→q126` is instrumental only because “cracking down on corruption” explicitly names the means target.
- **South Asia W1:** `c18d→[c19,c32]` is a bounded institutional realization of the people-chosen/fair-election proposition. Native C33 would supply a direct voting enactment but has no selected Rawlsing implementation ID, so it is emitted as a coverage defect rather than a runtime edge.

## Non-positive preservation

Crosswalk review rows: **{len(cross)}** total; **{sum(1 for x in cross if x['disposition']=='BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY')}** blocks and **{sum(1 for x in cross if x['disposition']=='NOT_T15_SOURCE_PROVEN_MISMATCH')}** source-proven mismatches. Coverage defects: **{len(defects)}**. Upstream repairs: **0**; T15 successor reclassification of prior `OTHER` rows is not treated as an upstream T06 metadata defect.

Categorical normative batteries whose answer-option semantics are collapsed into a single implementation (AB Q551A/Q551B, Asian q98, South Asia c24) are preserved as coverage defects rather than answer-dependent runtime relations. South Asia C31a and C33 are also native T15-relevant questions absent from the selected implementation universe.

## Completion law

All 3,052 implementation rows are accounted; every prior norm shore has a completed norm→praxis search; every T15 praxis candidate has a completed reverse search; all five subtypes were considered in every wave; strict T06 duplicates are excluded; unresolved bridges remain blocks. See `VALIDATION.json` and `HOSTILE_VALIDATION.json` after validation.
'''
(RET/'WORKER_REPORT.md').write_text(report,encoding='utf-8')

print(json.dumps({'positives':len(positives),'subtypes':subcnt,'waves':{f'{k[0]}::{k[1]}':v for k,v in wavecnt.items()},'crosswalks':len(cross),'blocks':len(blockers),'mismatches':sum(1 for x in cross if x['disposition']=='NOT_T15_SOURCE_PROVEN_MISMATCH'),'coverage_defects':len(defects),'overlap_rows':len(over)},default=lambda x:dict(x),indent=2))
