#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, re
from collections import defaultdict
from pathlib import Path
import pandas as pd

ROOT=Path(os.environ.get('RAWLSING_V18_ROOT','/mnt/data/rawlsing_v19_work/Rawlsing_J_Family_Authority_Strategy_Handoff_v18_20260731'))
OUT=Path(os.environ.get('RAWLSING_V19_OUT','/mnt/data/rawlsing_v19_outputs/social_order_3000'))
OUT.mkdir(parents=True,exist_ok=True)
S32=ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'
QREM=Path(os.environ.get('RAWLSING_PENDING_QUEUE',str(ROOT/'39_P2_GLOBAL_MATERIAL_ECONOMY_FIXED_3000_TRANCHE6/Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Material_Economy_Fixed_3000_Tranche_v6.csv')))

FULL_IDS=['DEMO_SUPPORT','GENDER_EDUCATION','GENDER_JOBS_SCARCE','RELIGION_SELF_RELIGIOSITY','SECURITY_NEIGHBORHOOD','ENVIRONMENT_VS_ECONOMY','CHANGE_SOCIETY','FREEDOM_SPEECH']
PARTIAL_ID='CIVIC_DEMONSTRATION'

def read(p): return pd.read_csv(p,dtype=str,keep_default_na=False)
def norm(x): return re.sub(r'\s+',' ',str(x or '').strip().casefold())
def stable(prefix,*parts): return prefix+'_'+hashlib.sha256(chr(31).join(map(str,parts)).encode()).hexdigest()[:24]
def compact(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def uniq(xs): return list(dict.fromkeys(x for x in xs if str(x).strip()))

def classify_one(text:str, response_fams:list[str], topologies:list[str], semantic_ids:list[str]):
    t=norm(text); sids=set(semantic_ids)
    # Missing/generic shells cannot export their inherited semantic label.
    if not t or re.fullmatch(r'(?:which|with which).{0,45}(?:statement|statements).{0,30}(?:opinion|agree).{0,5}',t) or t in {'religion','your neighborhood','support for democracy'} and not response_fams:
        return ('unresolved_axis','unspecified','unresolved','PARENT_OR_RESPONSE_AXIS_NOT_RECOVERED','LOW')
    if t in {'town','settlement name'}:
        return ('other_domain','settlement_identifier','metadata_or_location_label','EXACT_SETTLEMENT_METADATA_LABEL','HIGH')
    if len(t)<12 or re.search(r'^skip variable|randomization variable|form of split questionnaire|^don.?t know$|^refused$',t):
        return ('other_domain','survey_administration_or_response_shell','metadata_or_shell','EXACT_TEXT_EXCLUDES_GOVERNED_SURFACE','HIGH')
    if re.search(r'weight|interviewer|respondent number|country code|education index|government expenditure|population growth|digital object identifier|version [xyz]|ratio of graduate|settlement name|^city$|^town/village$',t):
        return ('other_domain','survey_metadata_or_external_index','metadata_or_external_context','EXACT_TEXT_EXCLUDES_GOVERNED_SURFACE','HIGH')
    if re.search(r'welzel|\bindex\b',t):
        if 'gender equality: education' in t: return ('derived_gender_education_index','education_gender_equality','derived_index','EXPLICIT_DERIVED_INDEX','HIGH')
        if 'gender equality: job' in t: return ('derived_gender_job_priority_index','jobs_scarce_gender_priority','derived_index','EXPLICIT_DERIVED_INDEX','HIGH')
        if 'inverse devoutness' in t: return ('derived_self_religiosity_index','respondent_self','inverse_devoutness_index','EXPLICIT_DERIVED_INDEX','HIGH')
        return ('other_domain','derived_or_external_index','derived_statistic','EXACT_TEXT_EXCLUDES_GOVERNED_SURFACE','HIGH')

    # Democratic legitimacy, authority, and support.
    if t=='support for democracy':
        # One Afrobarometer lineage carries the full three-way response contract; terse no-contract variants remain coordinate-only.
        conf='HIGH' if 'nominal_choice' in response_fams else 'MEDIUM'
        return ('democracy_regime_preference','regime_type','democracy_vs_nondemocracy_preference','SOURCE_NATIVE_SUPPORT_FOR_DEMOCRACY_ITEM',conf)
    if 'democracy is preferable to any other' in t and ('non-democratic' in t or "doesn't matter" in t or 'does not matter' in t):
        return ('democracy_regime_preference','regime_type','democracy_vs_nondemocracy_preference','EXPLICIT_THREE_WAY_REGIME_PREFERENCE_ITEM','HIGH')
    if 'democracy may have problems' in t and 'best form of government' in t:
        return ('democracy_despite_problems_support','democracy','agreement','EXPLICIT_DEMOCRACY_DESPITE_PROBLEMS_ITEM','HIGH')
    if 'system like ours' in t and 'deserves' in t and 'support' in t:
        return ('incumbent_system_support_despite_problems','current_political_system','agreement','EXPLICIT_CURRENT_SYSTEM_SUPPORT_ITEM','HIGH')
    if 'citizen must support government' in t:
        return ('citizen_duty_to_support_government','government','agreement','EXPLICIT_CITIZEN_SUPPORT_DUTY_ITEM','HIGH')
    if 'government has right to make authoritative decisions' in t:
        return ('government_authoritative_decision_legitimacy','government','agreement','EXPLICIT_GOVERNMENT_AUTHORITY_ITEM','HIGH')
    if "government is like the people's boss" in t and "people's employee" in t:
        return ('government_citizen_authority_model','government_and_citizens','boss_vs_employee_tradeoff','EXPLICIT_GOVERNMENT_CITIZEN_MODEL_ITEM','HIGH')
    if 'government leaders are like the head of a family' in t:
        return ('paternal_authority_obedience','government_leaders','agreement','EXPLICIT_PATERNAL_GOVERNMENT_OBEDIENCE_ITEM','HIGH')
    if 'undemocratic government came to power' in t and 'solve the problems' in t:
        return ('authoritarian_problem_solving_tolerance','undemocratic_government','agreement','EXPLICIT_AUTHORITARIAN_PROBLEM_SOLVING_ITEM','HIGH')
    if 'support a military government' in t:
        return ('military_government_support','military_government','support','EXPLICIT_MILITARY_GOVERNMENT_SUPPORT_ITEM','HIGH')
    if 'army takes over when government is incompetent' in t:
        return ('military_takeover_acceptability','army_takeover_under_government_incompetence','acceptability','EXPLICIT_ARMY_TAKEOVER_ITEM','HIGH')
    if 'president' in t and ('bound by laws' in t or 'obey the laws and the courts' in t):
        return ('executive_rule_of_law_constraint','president','bound_vs_unbound_by_law_tradeoff','EXPLICIT_EXECUTIVE_RULE_OF_LAW_ITEM','HIGH')
    if 'bypass regular channels' in t:
        return ('procedural_channel_legitimacy','official_procedures','agreement','EXPLICIT_PROCEDURAL_CHANNEL_ITEM','HIGH')
    if 'politics and government seem' in t and 'complicated' in t:
        return ('political_comprehension_efficacy','respondent_self','agreement','EXPLICIT_POLITICAL_COMPLEXITY_ITEM','HIGH')
    if 'people like me' in t and 'influence over what the government does' in t:
        return ('external_political_efficacy','respondent_influence_on_government','agreement','EXPLICIT_EXTERNAL_EFFICACY_ITEM','HIGH')
    if t=='understand government':
        return ('political_comprehension_efficacy','respondent_self','understanding_level','SOURCE_NATIVE_TERSE_UNDERSTAND_GOVERNMENT_ITEM','MEDIUM')
    if 'enact laws in accordance with the people' in t or "citizens' wishes" in t:
        return ('legislative_responsiveness_principle','law_enactment','people_wishes','EXPLICIT_PEOPLE_WISHES_LEGISLATION_ITEM','HIGH')
    if 'enact' in t and 'islamic law' in t:
        target='personal_status_law' if 'personal status' in t else ('inheritance_law' if 'inheritance' in t else ('penal_law' if 'penal' in t else 'law_general'))
        return ('religious_law_legislation_support',target,'agreement','EXPLICIT_ISLAMIC_LAW_LEGISLATION_ITEM','HIGH')

    # Gender and education.
    if ('university education' in t or 'university is more important' in t or "women's rights: university education more important for males" in t) and ('boy' in t or 'male' in t) and ('girl' in t or 'female' in t or "women's rights:" in t):
        return ('gendered_university_priority','university_education','male_over_female_priority','EXPLICIT_GENDER_EDUCATION_PRIORITY_ITEM','HIGH')
    if 'gender priority in university education' in t:
        return ('gendered_university_priority','university_education','male_over_female_priority','SOURCE_NATIVE_TERSE_GENDER_EDUCATION_ITEM','MEDIUM')
    if 'gender-mixed education' in t:
        return ('mixed_gender_education_permission','mixed_gender_education','agreement','EXPLICIT_MIXED_EDUCATION_ITEM','HIGH')
    if 'my son achieves university education' in t:
        return ('child_university_attainment_importance','son','agreement','EXPLICIT_SON_EDUCATION_IMPORTANCE_ITEM','HIGH')
    if 'my daughter achieves university education' in t:
        return ('child_university_attainment_importance','daughter','agreement','EXPLICIT_DAUGHTER_EDUCATION_IMPORTANCE_ITEM','HIGH')

    # Gender, jobs, and scarce-job priority.
    if ('jobs are scarce' in t or 'jobs scarce' in t) and ('men' in t or 'women' in t):
        return ('scarce_jobs_gender_priority','employment_access','men_over_women_priority','EXPLICIT_SCARCE_JOBS_GENDER_ITEM','HIGH')
    if ('jobs are scarce' in t or 'jobs scarce' in t) and ('locals' in t or 'nation' in t):
        target='locals_over_nonlocals' if 'locals' in t else 'nationals_over_foreigners'
        return ('scarce_jobs_national_priority','employment_access',target,'EXPLICIT_SCARCE_JOBS_NATIONAL_ITEM','HIGH')
    if ('jobs are scarce' in t or 'jobs scarce' in t) and 'retire early' in t:
        return ('scarce_jobs_retirement_priority','employment_access','older_workers_retire_early','EXPLICIT_SCARCE_JOBS_RETIREMENT_ITEM','HIGH')
    if ('jobs are scarce' in t or 'jobs scarce' in t) and ('handicapped' in t or 'disabled' in t):
        return ('scarce_jobs_disability_priority','employment_access','disabled_workers','EXPLICIT_SCARCE_JOBS_DISABILITY_ITEM','HIGH')
    if 'access to state jobs by gender' in t:
        return ('state_job_gender_access_index','state_employment','gender_access_external_index','EXTERNAL_GENDER_JOB_ACCESS_INDEX','MEDIUM')
    if 'take any job' in t and 'refuse job' in t:
        return ('unemployment_job_acceptance_norm','unemployed_person','take_any_job_vs_refusal_right','EXPLICIT_UNEMPLOYMENT_JOB_NORM_ITEM','HIGH')

    # Self-religiosity and religious identity.
    if re.search(r'(?:very devout|not devout|religiosit|describe yourself as very religious|somewhat religious|moderately religious|lightly religious)',t):
        conf='MEDIUM' if t in {'se7 religiosity','religiosity'} else 'HIGH'
        basis='SOURCE_NATIVE_TERSE_RELIGIOSITY_ITEM' if conf=='MEDIUM' else 'EXPLICIT_SELF_RELIGIOSITY_INTENSITY_ITEM'
        return ('self_religiosity_intensity','respondent_self','religiosity_degree',basis,conf)
    if ('religious person' in t and ('not a religious person' in t or 'atheist' in t)) or t=='are you a religious person':
        return ('self_religious_identification','respondent_self','religious_person_vs_nonreligious_or_atheist','EXPLICIT_SELF_RELIGIOUS_IDENTIFICATION_ITEM','HIGH')
    if t=='religion':
        return ('religious_affiliation_identity','respondent_self','affiliation_category','SOURCE_NATIVE_TERSE_RELIGION_IDENTITY_ITEM','MEDIUM')
    if 'is r atheist or agnostic' in t:
        return ('self_nonreligious_identification','respondent_self','atheist_or_agnostic_status','EXPLICIT_SELF_ATHEIST_AGNOSTIC_ITEM','HIGH')
    if re.search(r'(?:spouse|partner) no religion',t):
        target='spouse' if 'spouse' in t else 'partner'
        return ('other_person_religious_affiliation_absence',target,'no_religion_status','EXPLICIT_OTHER_PERSON_RELIGION_ITEM','HIGH')
    if 'r no religion age 16' in t:
        return ('past_self_religious_affiliation_absence','respondent_at_age_16','no_religion_status','EXPLICIT_PAST_SELF_RELIGION_ITEM','HIGH')
    if 'prefer the answer be' in t and 'religion' in t:
        return ('religion_question_privacy_preference','religion_disclosure','response_preference','EXPLICIT_RELIGION_PRIVACY_ITEM','HIGH')

    # Neighborhood and local safety.
    if ('safety of your neighborhood' in t or 'neighborhood safe' in t or 'local-area safety' in t or re.search(r'how safe is living in this city',t)):
        target='city_town_village' if 'city' in t or 'town' in t or 'village' in t else 'neighborhood_or_local_area'
        return ('local_area_safety_rating',target,'present_safety_rating','EXPLICIT_LOCAL_SAFETY_ITEM','HIGH')
    if 'felt unsafe walking in your neigh' in t:
        return ('unsafe_walking_experience','respondent_or_family_in_neighborhood','past_year_frequency','EXPLICIT_UNSAFE_WALKING_ITEM','HIGH')
    if 'how secure do you feel these days' in t and 'occur in your neighborhood' in t:
        return ('heterogeneous_lineage','general_security_and_neighborhood_incidence','multiple_operators','COMPOSITE_PROMPT_WITHOUT_CHILD_TARGET','LOW')
    if 'worried about safety / security' in t and 'reason for refusals' in t:
        return ('other_domain','fieldwork_refusal_reason','safety_security_reason','EXACT_TEXT_EXCLUDES_GOVERNED_SURFACE','HIGH')

    # Environment versus growth and adjacent climate constructs.
    if 'priority to the fight against climate change' in t and 'priority to economic growth' in t:
        return ('climate_growth_priority_tradeoff','climate_change_mitigation_and_economic_growth','priority_tradeoff','EXPLICIT_CLIMATE_GROWTH_TRADEOFF_ITEM','HIGH')
    if ('environment vs economic growth' in t or 'protecting environment vs. economic growth' in t or 'priority should be given to the environment' in t or 'environment v/s economic development' in t):
        return ('environment_growth_priority_tradeoff','environment_and_economic_growth','priority_tradeoff','EXPLICIT_ENVIRONMENT_GROWTH_TRADEOFF_ITEM','HIGH')
    if 'protecting the environment less urgent' in t:
        return ('environment_growth_priority_tradeoff','environment_and_economic_growth','environment_less_urgent_agreement','POLARITY_SPECIFIC_ENVIRONMENT_PRIORITY_ITEM','HIGH')
    if 'improving & protecting environment' in t:
        return ('environmental_spending_adequacy','environmental_protection','too_little_about_right_too_much','EXPLICIT_ENVIRONMENT_SPENDING_ITEM','HIGH')
    if 'economic progress dependent on environment' in t:
        return ('economy_environment_dependency_belief','economic_progress_and_environment','agreement','EXPLICIT_ECONOMY_ENVIRONMENT_DEPENDENCY_ITEM','HIGH')
    if 'would give more money to' in t and 'climate change' in t:
        return ('climate_financial_contribution_willingness','climate_change','give_more_money','EXPLICIT_CLIMATE_CONTRIBUTION_ITEM','HIGH')
    if 'paying more in taxes' in t and 'climate change' in t:
        return ('climate_tax_willingness','climate_change','pay_more_taxes','EXPLICIT_CLIMATE_TAX_ITEM','HIGH')
    if 'how concerned are you about climate change' in t:
        return ('climate_change_concern','climate_change','concern_rating','EXPLICIT_CLIMATE_CONCERN_ITEM','HIGH')
    if 'serious impact of climate change' in t:
        target='children_today' if 'children' in t else 'respondent_or_society_unspecified'
        return ('climate_impact_seriousness',target,'seriousness_rating','EXPLICIT_CLIMATE_IMPACT_ITEM','HIGH')
    if 'concern about climate-change impact on' in t:
        target=re.sub(r'^.*impact on\s*','',t).strip(' .').replace(' ','_')
        return ('climate_impact_concern',target,'concern_rating','EXPLICIT_CLIMATE_IMPACT_CONCERN_ITEM','HIGH')
    if 'contribution to climate change by' in t:
        target=re.sub(r'^.*?by\s*','',t).strip(' .').replace(' ','_')
        return ('climate_contribution_attribution',target,'contribution_rating','EXPLICIT_CLIMATE_CONTRIBUTION_ATTRIBUTION_ITEM','HIGH')
    if 'responsibility for addressing climate change of' in t:
        target=re.sub(r'^.*?of\s*','',t).strip(' .').replace(' ','_')
        return ('climate_responsibility_attribution',target,'responsibility_rating','EXPLICIT_CLIMATE_RESPONSIBILITY_ITEM','HIGH')
    if 'personally taken actions aimed at helping to fight climate change' in t:
        return ('personal_climate_action_participation','climate_change','ever_or_recent_action','EXPLICIT_PERSONAL_CLIMATE_ACTION_ITEM','HIGH')
    if 'actions aimed at fighting climate change have y' in t:
        return ('unresolved_axis','climate_action_child_unspecified','parent_child_not_recovered','TRUNCATED_CLIMATE_ACTION_CHILD','LOW')

    # Social-change and reform orientations.
    if ('political reform' in t and ('little by little' in t or 'all at once' in t or 'gradual versus immediate' in t)):
        return ('political_reform_pace_preference','political_reform','gradual_vs_immediate_or_none','EXPLICIT_REFORM_PACE_ITEM','HIGH')
    if t=='prefernce: political reform':
        return ('political_reform_pace_preference','political_reform','preference_unspecified_options','SOURCE_NATIVE_TERSE_REFORM_ITEM','MEDIUM')
    if 'economic system needs fundamential changes' in t or 'economic system needs fundamental changes' in t:
        return ('economic_system_change_need','economic_system','fundamental_change_agreement','EXPLICIT_ECONOMIC_SYSTEM_CHANGE_ITEM','HIGH')
    if 'basic needs for all' in t:
        return ('social_basic_needs_priority','basic_needs_for_all','importance_rating','EXPLICIT_BASIC_NEEDS_ITEM','HIGH')
    if 'society aimed: regulated vs. responsible society' in t:
        return ('society_regulation_responsibility_orientation','society','regulated_vs_responsible','EXPLICIT_SOCIETY_ORIENTATION_ITEM','HIGH')
    if 'society aimed: egalitarian vs. competitive' in t:
        return ('society_equality_competition_orientation','society','egalitarian_vs_competitive','EXPLICIT_SOCIETY_ORIENTATION_ITEM','HIGH')
    if 'basic kinds of attitudes concerning society' in t or 'four statements with different opinions about the' in t:
        return ('unresolved_axis','society_change_orientation','response_options_or_children_missing','PARENT_PROMPT_WITHOUT_RECOVERED_OPTIONS','LOW')

    # Speech and expressive freedom.
    if 'how free are you' in t and 'say what you think' in t:
        return ('expressive_freedom_experience','say_what_you_think','present_freedom_extent','EXPLICIT_CURRENT_SPEECH_FREEDOM_ITEM','HIGH')
    if t=='freedom to express opinions.':
        return ('expressive_freedom_experience','express_opinions','present_guarantee_extent','EXPLICIT_OPINION_EXPRESSION_FREEDOM_ITEM','HIGH')
    if 'freedom to criticize government without fear' in t:
        return ('government_criticism_freedom','criticize_government','present_freedom_or_agreement','EXPLICIT_GOVERNMENT_CRITICISM_ITEM','HIGH')
    if 'present vs. past: freedom to say what you think' in t:
        return ('expressive_freedom_change','say_what_you_think','present_vs_past_change','EXPLICIT_SPEECH_FREEDOM_CHANGE_ITEM','HIGH')
    if 'everyone is free to say what they think' in t and 'better than before' in t:
        return ('expressive_freedom_change','say_what_you_think','better_than_before','EXPLICIT_SPEECH_FREEDOM_CHANGE_ITEM','HIGH')
    if 'importance of freedom of speech' in t:
        return ('freedom_of_speech_importance','freedom_of_speech','importance_rating','EXPLICIT_SPEECH_IMPORTANCE_ITEM','HIGH')
    if 'freedom of expression should be guaranteed' in t and 'fake news' in t:
        return ('speech_freedom_fake_news_tradeoff','freedom_of_expression_and_fake_news_control','freedom_vs_control_tradeoff','EXPLICIT_SPEECH_FAKE_NEWS_TRADEOFF_ITEM','HIGH')
    if 'freedom to join political parties without fear' in t:
        return ('association_freedom_experience','political_parties','present_freedom_extent','EXPLICIT_PARTY_ASSOCIATION_FREEDOM_ITEM','HIGH')
    if 'freedom to join any organization' in t:
        return ('association_freedom_change','organizations','present_vs_past_change','EXPLICIT_ASSOCIATION_FREEDOM_CHANGE_ITEM','HIGH')
    if 'voting freedom' in t:
        return ('voting_freedom_change','voting','present_vs_past_change','EXPLICIT_VOTING_FREEDOM_CHANGE_ITEM','HIGH')

    # Demonstration/protest participation surface.
    if re.search(r'attended (?:a )?(?:demonstration|demonstration or protest march)',t) or 'participated in any protest or demonstration' in t or 'demonstrated, striken, or sat-in' in t:
        op='past_participation_ever' if ('ever' in t or 'had you participated' in t) else ('past_participation_unspecified' if 'attended' in t or 'demonstrated' in t else 'past_participation')
        return ('demonstration_participation','lawful_or_unspecified_demonstration',op,'EXPLICIT_DEMONSTRATION_PARTICIPATION_ITEM','HIGH')
    if 'have you, or would you ever, participate in political demonstrations' in t:
        return ('demonstration_participation_disposition','political_demonstrations','past_or_future_disposition','EXPLICIT_MIXED_DEMONSTRATION_DISPOSITION_ITEM','HIGH')
    if ('how likely' in t or 'affinity to attend lawful demonstrations' in t) and 'attend lawful demonstration' in t.replace('a lawful','lawful'):
        return ('demonstration_participation_likelihood','lawful_demonstration','future_likelihood','EXPLICIT_DEMONSTRATION_LIKELIHOOD_ITEM','HIGH')
    if 'participate in riots' in t:
        return ('riot_participation_disposition','riots','past_or_future_disposition','EXPLICIT_RIOT_DISPOSITION_ITEM','HIGH')
    if 'reason for the protests' in t:
        rank='second_reason' if 'second most important' in t else 'most_important_reason'
        return ('protest_motivation_ranking','named_historical_protests',rank,'EXPLICIT_PROTEST_REASON_ITEM','HIGH')

    # Explicit contaminants, preserving useful redirect coordinates without authorizing them here.
    other_patterns=[
      ('education_service_or_status',r'education|school|university|teacher|training'),
      ('employment_status_or_job_history',r'self-employed|working for wages|job at this moment|looking for a job|principal job|answered advertisements|retirement'),
      ('religious_affiliation_or_practice',r'religion|religious|quran|bible|church|faith|heaven'),
      ('gender_rights_or_roles',r'women|woman|men and women|wife|mother-in-law|daughter-in-law|divorce|travel alone|citizenship'),
      ('climate_or_environment_other',r'climate change|environment|pollution|natural resource'),
      ('political_or_civic_other',r'political|government|citizen|court|judicial|party|election|democracy|protest|official'),
      ('family_or_social_relations',r'family|parents|spouse|partner|children|neighbors|neighbours|town|community'),
      ('media_or_culture',r'television|entertainment|read book|novels|opera|dance perf|sports event|web'),
      ('material_or_economic_context',r'income|food|work|job|economic|money|own any|household'),
      ('crime_violence_or_security_other',r'violence|rape|safety|security|police|crime|honor killing|abused|physical force'),
      ('personal_identity_or_psychology',r'skin tone|masculine|feminine|proud|ashamed|regret|lonely|touched|self-sufficient'),
      ('science_religion_or_worldview',r'science and religion|science and not enough on faith|spiritual needs'),
    ]
    for target,pat in other_patterns:
        if re.search(pat,t): return ('other_domain',target,'other_operator','EXACT_TEXT_OUTSIDE_SELECTED_GOVERNED_PROPOSITION','HIGH')
    return ('other_domain','explicit_other_substantive_item','other_operator','EXACT_TEXT_OUTSIDE_SELECTED_GOVERNED_PROPOSITION','MEDIUM')

queue=read(QREM)
sel=queue[queue.semantic_content_id.isin(FULL_IDS)].copy()
need=3000-len(sel)
assert need==48,need
partial=(queue[queue.semantic_content_id.eq(PARTIAL_ID)]
    .assign(_score=lambda d:pd.to_numeric(d.review_priority_score,errors='coerce').fillna(-1),_rank=lambda d:pd.to_numeric(d.cell_priority_rank,errors='coerce').fillna(999999))
    .sort_values(['_score','_rank','semantic_pair_candidate_id'],ascending=[False,True,True]).head(need).drop(columns=['_score','_rank']))
sel=pd.concat([sel,partial],ignore_index=True).sort_values(['semantic_content_id','left_source_family','right_source_family','cell_priority_rank','semantic_pair_candidate_id'])
assert len(sel)==3000 and sel.semantic_pair_candidate_id.nunique()==3000 and set(sel.semantic_pair_candidate_id)<=set(queue.semantic_pair_candidate_id)

nodes=read(S32/'Rawlsing_P2_All_Nine_Unified_Node_Evidence_Registry_v1.csv')
lineages=read(S32/'Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv')
mem=read(S32/'Rawlsing_P2_Normalized_Source_Structure_Memberships_v1.csv')
reg=read(S32/'Rawlsing_P2_Normalized_Source_Structure_Registry_v1.csv')
regidx=reg.set_index('source_structure_id')
struct_by_q=defaultdict(list)
for _,r in mem.iterrows(): struct_by_q[r.question_implementation_id].append(r.source_structure_id)
needed=set(sel.left_lineage_id)|set(sel.right_lineage_id)
nodegroups={k:g for k,g in nodes[nodes.lineage_id.isin(needed)].groupby('lineage_id')}
lin=lineages[lineages.lineage_id.isin(needed)].copy()

classes=[]
for _,lr in lin.iterrows():
    g=nodegroups[lr.lineage_id]
    texts=uniq(g.exact_question_text.tolist()); responses=uniq(g.response_family_expectation.tolist()); tops=uniq(g.response_topology.tolist()); semids=uniq(g.semantic_content_id.tolist())
    sids=uniq(s for qid in g.question_implementation_id for s in struct_by_q.get(qid,[])); slabels=uniq(regidx.loc[s].structure_label for s in sids if s in regidx.index)
    per=[classify_one(t,responses,tops,semids) for t in texts]
    signatures=uniq((a,b,c) for a,b,c,_,_ in per)
    if len(signatures)==1:
        axis,target,op=signatures[0]; basis=' | '.join(uniq(x[3] for x in per)); conf='LOW' if any(x[4]=='LOW' for x in per) else ('MEDIUM' if any(x[4]=='MEDIUM' for x in per) else 'HIGH')
    else:
        axis,target,op='heterogeneous_lineage','heterogeneous','heterogeneous'; basis='MULTIPLE_CLASSIFICATIONS:'+compact([{'text':texts[i],'axis':x[0],'target':x[1],'operator':x[2]} for i,x in enumerate(per)]); conf='LOW'
    status='P2_SOCIAL_ORDER_LINEAGE_CLASSIFIED'
    if axis in {'unresolved_axis','heterogeneous_lineage'}: status='P2_SOCIAL_ORDER_LINEAGE_UNRESOLVED'
    elif axis=='other_domain': status='P2_OUT_OF_DOMAIN_LINEAGE_REDIRECTED'
    elif conf=='MEDIUM': status='P2_SOCIAL_ORDER_LINEAGE_COORDINATE_ONLY_INCOMPLETE_PROPOSITION'
    classes.append({'classification_id':stable('p2socialorderclassv1',lr.lineage_id),'lineage_id':lr.lineage_id,'source_family':lr.source_family,'member_count':lr.member_count,
      'variables_json':compact(uniq(g.source_variable_code.tolist())),'waves_json':compact(uniq(g.wave.tolist())),'exact_question_texts_json':compact(texts),
      'response_options_json':compact(uniq(g.response_options_substantive.tolist())),'response_topologies_json':compact(tops),'response_family_expectations_json':compact(responses),
      'semantic_content_ids_json':compact(semids),'source_structure_ids_json':compact(sids),'source_structure_labels_json':compact(slabels),
      'governed_relation_axis':axis,'governed_target_or_scope':target,'governed_operator':op,'classification_basis':basis,'classification_confidence':conf,
      'authority_status':status,'prohibited_use':'Classification coordinate only; no J-family membership, value harmonization, or respondent join.'})
classes=pd.DataFrame(classes).sort_values(['source_family','lineage_id'])
classes.to_csv(OUT/'Rawlsing_P2_Social_Order_Lineage_Classification_v1.csv',index=False)
cidx=classes.set_index('lineage_id')

DOMAIN_FAMILY={
 'democracy_regime_preference':'democratic_legitimacy','democracy_despite_problems_support':'democratic_legitimacy','incumbent_system_support_despite_problems':'political_system_support','citizen_duty_to_support_government':'government_obedience','government_authoritative_decision_legitimacy':'government_obedience','government_citizen_authority_model':'government_obedience','paternal_authority_obedience':'government_obedience','authoritarian_problem_solving_tolerance':'authoritarian_tolerance','military_government_support':'authoritarian_tolerance','military_takeover_acceptability':'authoritarian_tolerance','executive_rule_of_law_constraint':'rule_of_law','procedural_channel_legitimacy':'procedural_legitimacy','political_comprehension_efficacy':'political_efficacy','external_political_efficacy':'political_efficacy','legislative_responsiveness_principle':'legislative_legitimacy','religious_law_legislation_support':'religious_law',
 'gendered_university_priority':'gender_education','mixed_gender_education_permission':'gender_education','child_university_attainment_importance':'child_education','derived_gender_education_index':'gender_education',
 'scarce_jobs_gender_priority':'scarce_jobs','scarce_jobs_national_priority':'scarce_jobs','scarce_jobs_retirement_priority':'scarce_jobs','scarce_jobs_disability_priority':'scarce_jobs','derived_gender_job_priority_index':'scarce_jobs','state_job_gender_access_index':'gender_employment','unemployment_job_acceptance_norm':'labor_norms',
 'self_religiosity_intensity':'self_religiosity','self_religious_identification':'self_religiosity','derived_self_religiosity_index':'self_religiosity','religious_affiliation_identity':'religious_identity','self_nonreligious_identification':'religious_identity','past_self_religious_affiliation_absence':'religious_identity','other_person_religious_affiliation_absence':'religious_identity','religion_question_privacy_preference':'religion_privacy',
 'local_area_safety_rating':'local_safety','unsafe_walking_experience':'local_safety',
 'environment_growth_priority_tradeoff':'environment_growth','climate_growth_priority_tradeoff':'environment_growth','environmental_spending_adequacy':'environment_policy','economy_environment_dependency_belief':'environment_growth','climate_financial_contribution_willingness':'climate_action','climate_tax_willingness':'climate_action','climate_change_concern':'climate_concern','climate_impact_seriousness':'climate_impact','climate_impact_concern':'climate_impact','climate_contribution_attribution':'climate_attribution','climate_responsibility_attribution':'climate_attribution','personal_climate_action_participation':'climate_action',
 'political_reform_pace_preference':'social_change','economic_system_change_need':'social_change','social_basic_needs_priority':'social_priorities','society_regulation_responsibility_orientation':'society_orientation','society_equality_competition_orientation':'society_orientation',
 'expressive_freedom_experience':'speech_freedom','government_criticism_freedom':'speech_freedom','expressive_freedom_change':'speech_freedom','freedom_of_speech_importance':'speech_freedom','speech_freedom_fake_news_tradeoff':'speech_freedom','association_freedom_experience':'association_freedom','association_freedom_change':'association_freedom','voting_freedom_change':'voting_freedom',
 'demonstration_participation':'protest_participation','demonstration_participation_disposition':'protest_participation','demonstration_participation_likelihood':'protest_participation','riot_participation_disposition':'riot_participation','protest_motivation_ranking':'protest_motivation'
}
def family(a): return DOMAIN_FAMILY.get(a,'')
def topology_set(row): return set(json.loads(row.response_topologies_json))
def response_set(row): return set(json.loads(row.response_family_expectations_json))

rul=[]
for _,cand in sel.iterrows():
    l=cidx.loc[cand.left_lineage_id]; r=cidx.loc[cand.right_lineage_id]
    la,ra=l.governed_relation_axis,r.governed_relation_axis; lt,rt=l.governed_target_or_scope,r.governed_target_or_scope; lo,ro=l.governed_operator,r.governed_operator; lc,rc=l.classification_confidence,r.classification_confidence
    if 'UNRESOLVED' in l.authority_status or 'UNRESOLVED' in r.authority_status:
        status='UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_SOURCE_LOCAL_EVIDENCE'; rel='UNRESOLVED'; ceil='NO_AUTHORITY'; rat='At least one source-local lineage lacks a recoverable single relation, target/scope, and operator.'
    elif la=='other_domain' and ra=='other_domain':
        if lt==rt and lt not in {'survey_metadata_or_external_index','survey_administration_or_response_shell','explicit_other_substantive_item'}:
            status='REDIRECTED_SHARED_OTHER_DOMAIN_COORDINATE_NOT_ADJUDICATED_HERE'; rel='OTHER_DOMAIN_REVIEW_REQUIRED'; ceil='NO_SOCIAL_ORDER_AUTHORITY'; rat='Both exact lineages share an out-of-scope coordinate; this tranche records the redirect without manufacturing authority for that domain.'
        else:
            status='REJECTED_CONTAMINATED_NEIGHBORHOOD_OTHER_DOMAIN_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='The inherited neighborhood joined distinct out-of-scope propositions.'
    elif la=='other_domain' or ra=='other_domain':
        status='REJECTED_GOVERNED_PROPOSITION_VERSUS_OTHER_DOMAIN_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='One lineage asserts a governed proposition while the other exact item belongs to another domain.'
    elif la==ra and lt==rt and lo==ro and lc=='HIGH' and rc=='HIGH':
        status='ACCEPTED_TYPED_SOCIAL_ORDER_PROPOSITION_RELATION'; rel='REWORDED_PROPOSITION_EQUIVALENCE'; same_top=topology_set(l)==topology_set(r) and len(topology_set(l))==1; same_resp=response_set(l)==response_set(r)
        ceil='QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY' if same_top and same_resp else 'QUESTION_PROPOSITION_ONLY'; rat='Both source-local lineages assert the same governed relation toward the same target/scope with the same operator, supported by HIGH-confidence two-sided evidence.'
    elif la==ra and lt==rt:
        status='ACCEPTED_SAME_CONSTRUCT_TARGET_DIFFERENT_OPERATOR_OR_INCOMPLETE_EVIDENCE_COORDINATE_ONLY'; rel='CONSTRUCT_TARGET_COORDINATE_ONLY'; ceil='CONSTRUCT_TARGET_ONLY'; rat='The construct and target agree, while operator, polarity, timeframe, or evidence completeness differs.'
    elif family(la) and family(la)==family(ra):
        status='ACCEPTED_DOMAIN_COORDINATE_ONLY_RELATION_OR_TARGET_SCOPE_DIFFERS'; rel='DOMAIN_COORDINATE_ONLY'; ceil='DOMAIN_COORDINATE_ONLY'; rat='The exact items share a governed family but differ in relation, target, operator, scope, or comparison baseline.'
    elif family(la) and family(ra):
        status='REJECTED_FALSE_EQUIVALENCE_GOVERNED_RELATION_OR_TARGET_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='Both items are substantive but assert different governed relations or targets.'
    else:
        status='REJECTED_DIFFERENT_GOVERNED_RELATION_AXES'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='The exact lineages assert different governed relations.'
    rid=stable('p2socialorderrulingv1',cand.semantic_pair_candidate_id)
    rul.append({'pair_ruling_id':rid,'semantic_pair_candidate_id':cand.semantic_pair_candidate_id,'semantic_content_id':cand.semantic_content_id,'left_source_family':cand.left_source_family,'right_source_family':cand.right_source_family,'left_lineage_id':cand.left_lineage_id,'right_lineage_id':cand.right_lineage_id,
      'left_relation_axis':la,'right_relation_axis':ra,'left_target_or_scope':lt,'right_target_or_scope':rt,'left_operator':lo,'right_operator':ro,'left_classification_confidence':lc,'right_classification_confidence':rc,
      'authority_status':status,'relation_type':rel,'portability_ceiling':ceil,'rationale':rat,'left_classification_id':l.classification_id,'right_classification_id':r.classification_id,
      'two_sided_evidence_status':'EXPLICIT_LINEAGE_NODE_RESPONSE_AND_STRUCTURE_PROVENANCE_BOTH_SIDES','prohibited_use':'No J-family authority, value harmonization, or respondent join follows from this ruling.'})
rul=pd.DataFrame(rul)
rul.to_csv(OUT/'Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv',index=False)

ev=[]
for _,rr in rul.iterrows():
    for side in ('left','right'):
        lid=rr[f'{side}_lineage_id']; c=cidx.loc[lid]; g=nodegroups[lid]
        ev.append({'evidence_record_id':stable('p2socialorderevidencev1',rr.pair_ruling_id,side),'pair_ruling_id':rr.pair_ruling_id,'semantic_pair_candidate_id':rr.semantic_pair_candidate_id,'side':side.upper(),'lineage_id':lid,'source_family':c.source_family,'classification_id':c.classification_id,'governed_relation_axis':c.governed_relation_axis,'governed_target_or_scope':c.governed_target_or_scope,'governed_operator':c.governed_operator,
          'question_implementation_ids_json':compact(g.question_implementation_id.tolist()),'wave_variable_locators_json':compact([{'wave':x.wave,'variable':x.source_variable_code,'source_row_index':x.source_row_index} for _,x in g.iterrows()]),'exact_question_texts_json':c.exact_question_texts_json,'response_options_json':c.response_options_json,'response_topologies_json':c.response_topologies_json,'response_family_expectations_json':c.response_family_expectations_json,'source_structure_ids_json':c.source_structure_ids_json,'source_structure_labels_json':c.source_structure_labels_json,'classification_basis':c.classification_basis,'classification_confidence':c.classification_confidence,
          'evidence_sufficiency':'COMPLETE_FOR_PROPOSITION_CEILING' if c.classification_confidence=='HIGH' and 'UNRESOLVED' not in c.authority_status else ('COMPLETE_FOR_COORDINATE_ONLY' if c.classification_confidence=='MEDIUM' else 'INCOMPLETE_OR_HETEROGENEOUS')})
ev=pd.DataFrame(ev); ev.to_csv(OUT/'Rawlsing_P2_Social_Order_3000_Two_Sided_Evidence_Ledger_v1.csv',index=False)
remaining=queue[~queue.semantic_pair_candidate_id.isin(set(sel.semantic_pair_candidate_id))].copy(); remaining.to_csv(OUT/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Social_Order_Fixed_3000_Tranche_v7.csv',index=False)
sel.to_csv(OUT/'Rawlsing_P2_Social_Order_Fixed_3000_Tranche_Candidate_Surface_v1.csv',index=False)
rul[rul.authority_status.eq('ACCEPTED_TYPED_SOCIAL_ORDER_PROPOSITION_RELATION')].to_csv(OUT/'Rawlsing_P2_Social_Order_Accepted_Proposition_Review_Surface_v1.csv',index=False)
rul[rul.relation_type.eq('UNRESOLVED')].to_csv(OUT/'Rawlsing_P2_Social_Order_Unresolved_Review_Surface_v1.csv',index=False)
summary={'contract_version':'P2_FIXED_3000_SOCIAL_ORDER_TRANCHE_V1','input_pending_pairs':len(queue),'fixed_work_unit_pairs':len(sel),'remaining_pairs':len(remaining),'selected_semantic_id_counts':{str(k):int(v) for k,v in sel.semantic_content_id.value_counts().sort_index().items()},'lineages_classified':len(classes),'classification_status_counts':{str(k):int(v) for k,v in classes.authority_status.value_counts().sort_index().items()},'pair_status_counts':{str(k):int(v) for k,v in rul.authority_status.value_counts().sort_index().items()},'relation_type_counts':{str(k):int(v) for k,v in rul.relation_type.value_counts().sort_index().items()},'evidence_rows':len(ev),'expected_evidence_rows':2*len(rul),'selection_exactly_3000':len(sel)==3000,'queue_partition_exact':len(sel)+len(remaining)==len(queue),'selected_ids_unique':sel.semantic_pair_candidate_id.nunique()==3000,'ruling_ids_unique':rul.pair_ruling_id.nunique()==3000,'evidence_ids_unique':ev.evidence_record_id.nunique()==6000,'proposition_acceptance_requires_axis_target_operator_identity_and_high_confidence':bool(((rul.authority_status!='ACCEPTED_TYPED_SOCIAL_ORDER_PROPOSITION_RELATION')|((rul.left_relation_axis==rul.right_relation_axis)&(rul.left_target_or_scope==rul.right_target_or_scope)&(rul.left_operator==rul.right_operator)&(rul.left_classification_confidence=='HIGH')&(rul.right_classification_confidence=='HIGH'))).all()),'authority_boundary':'PAIR_RELATION_AUTHORITY_ONLY_NO_J_FAMILY_NO_VALUE_HARMONIZATION'}
(OUT/'FIXED_3000_SOCIAL_ORDER_TRANCHE_RETURN.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(summary,indent=2,ensure_ascii=False))
