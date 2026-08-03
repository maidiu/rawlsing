#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, re
from collections import defaultdict
from pathlib import Path
import pandas as pd

ROOT=Path(os.environ.get('RAWLSING_V15_ROOT','/mnt/data/rawlsing_v15_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v15_20260731'))
OUT=Path(os.environ.get('RAWLSING_V16_OUT','/mnt/data/rawlsing_v16_outputs/democracy_electoral_3000'))
OUT.mkdir(parents=True,exist_ok=True)
S32=ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'
QREM=Path(os.environ.get('RAWLSING_PENDING_QUEUE',str(ROOT/'36_P2_GLOBAL_TRUST_SEMANTIC_NEIGHBORHOOD_ADJUDICATION_TRANCHE3/Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Trust_Tranche_v3.csv')))


def read(p): return pd.read_csv(p,dtype=str,keep_default_na=False)
def norm(x): return re.sub(r'\s+',' ',str(x or '').strip().casefold())
def stable(prefix,*parts): return prefix+'_'+hashlib.sha256(chr(31).join(map(str,parts)).encode()).hexdigest()[:24]
def compact(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def uniq(xs): return list(dict.fromkeys(x for x in xs if str(x).strip()))

def scope_target(t:str):
    t=norm(t)
    # election scope first
    if 'parliamentary election' in t or 'parliamentary elections' in t: return 'parliamentary_election'
    if 'presidential election' in t: return 'presidential_election'
    if 'local-level election' in t or 'local election' in t: return 'local_election'
    if 'referendum' in t: return 'election_or_referendum'
    if 'last national election' in t or 'most recent national election' in t or 'national election' in t: return 'national_election'
    if 'election' in t or 'elections' in t: return 'elections_general'
    return 'unspecified_scope'

def named_country(t:str):
    t=norm(t)
    mapping={
      'people\'s republic of china':'china','china':'china','iran':'iran','israel':'israel','turkey':'turkey',
      'united states of america':'united_states','the usa':'united_states','usa':'united_states','america':'united_states',
      'spain':'spain','cuba':'cuba','venezuela':'venezuela','canada':'canada','japan':'japan','saudi arabia':'saudi_arabia',
      'south africa':'south_africa','zimbabwe':'zimbabwe','united states':'united_states',
    }
    if 'former colonial power' in t:
        return 'former_colonial_power_unspecified'
    for k,v in mapping.items():
        if k in t: return v
    if "respondent's country" in t or '[respondent' in t or 'your country' in t or 'our country' in t or 'the country today' in t:
        return 'respondent_country'
    return 'unspecified_country'

# Explicit lineage overrides only where exact child labels are terse but source-native response/structure evidence is sufficient.
OVERRIDES={
 'p2lineage_9fa5c84bcd9b32ab7b12be93':('democracy_extent_rating','respondent_country_current','extent_rating','SOURCE_RESPONSE_OPTIONS_EXPLICIT_DEMOCRACY_CATEGORIES','HIGH'),
 'p2lineage_140598e1581a7fd40ca91fc5':('regime_model_attitude','military_rule','support_oppose','SOURCE_SUMMARY_LABEL_AND_RESPONSE_FAMILY','MEDIUM'),
 'p2lineage_9b80162bfd534df8208de8de':('regime_model_attitude','one_party_rule','support_oppose','SOURCE_SUMMARY_LABEL_AND_RESPONSE_FAMILY','MEDIUM'),
 'p2lineage_6f4d8077a7ace52509c0a54c':('vote_participation','parliamentary_election','retrospective_behavior','SOURCE_NATIVE_BELLI_TURNOUT_LABEL','HIGH'),
 'p2lineage_2c317ec21a29768f5f5d8f68':('election_integrity','elections_general','freeness_fairness_evaluation','SOURCE_NATIVE_LABEL_EXPLICIT','HIGH'),
 # Terse Afro R1 system ratings lack a delivered parent prompt and remain unresolved rather than inferred.
 'p2lineage_37b86896fab8c2adc3e8070c':('unresolved_main_domain','future_system_unspecified','numeric_rating','TERSE_LABEL_WITHOUT_PARENT_PROMPT','LOW'),
 'p2lineage_440c5652e50c423b63a8ae59':('unresolved_main_domain','current_government_unspecified','numeric_rating','TERSE_LABEL_WITHOUT_PARENT_PROMPT','LOW'),
 'p2lineage_d24d7cb6c8a6e216141c2753':('unresolved_main_domain','previous_system_unspecified','numeric_rating','TERSE_LABEL_WITHOUT_PARENT_PROMPT','LOW'),
 'p2lineage_a7ec536f7ce0ae6d1f339a8b':('vote_participation','national_election','retrospective_behavior','RESPONSE_OPTIONS_EXPLICIT_PARTICIPATION_STATUS','HIGH'),
 'p2lineage_016edfec1d9701aaebce6d29':('regime_model_attitude','democratic_system_defined_freedoms_equality_alternation','good_bad_governing_method','EXACT_TEXT_DEFINITION_AND_GOOD_BAD_RESPONSE_CONTRACT','HIGH'),
 'p2lineage_1b85888232a1638047e5193d':('vote_participation','parliamentary_election','retrospective_behavior','EXACT_TEXT_AND_YES_NO_RESPONSE_CONTRACT','HIGH'),
 'p2lineage_261ea8f403e9f6544da33270':('democracy_extent_rating','named_country:iran','extent_rating','EXPLICIT_NUMERIC_DEMOCRACY_SCALE','HIGH'),
 'p2lineage_502b2f1d1ad60567e4db0390':('democracy_extent_rating','respondent_country_current','extent_rating','EXPLICIT_NUMERIC_DEMOCRACY_SCALE','HIGH'),
 'p2lineage_2a2185694fafa6082374d6fb':('election_integrity','municipal_election','freeness_fairness_evaluation','EXPLICIT_MUNICIPAL_ELECTION_INTEGRITY_ITEM','HIGH'),
 'p2lineage_d79dfe2a7ec3c65f854955f1':('regime_model_attitude','religious_law_without_parties_or_elections','suitability','SOURCE_NATIVE_SUITABILITY_LABEL','HIGH'),
 'p2lineage_e642c76e6c83332ccd5c51d5':('regime_system_choice','presidential_parliamentary_mixed_system_options','system_preference','EXACT_PROMPT_AND_RESPONSE_OPTIONS','HIGH'),
 'p2lineage_d02a9d5215536716a8134cae':('regime_system_choice','presidential_parliamentary_mixed_system_options','system_preference','EXACT_PROMPT_AND_RESPONSE_OPTIONS','HIGH'),
 'p2lineage_8b1f72bfa184bc28c9fe15dd':('vote_participation_frequency','elections_general','retrospective_frequency','EXPLICIT_LIFETIME_VOTING_FREQUENCY_ITEM','HIGH'),
 'p2lineage_de1dfbc5c6ca3d676c9d4139':('vote_participation','elections_general','retrospective_behavior','EXPLICIT_LAST_ELECTION_PARTICIPATION_ITEM','HIGH'),
 'p2lineage_367d0f0c288c5b9dba62b19e':('regime_model_attitude','democratic_system','good_bad_governing_method','STANDARD_GOOD_BAD_SYSTEM_BATTERY_RESPONSE_CONTRACT','HIGH'),
 'p2lineage_90c498b3fd1c1e3dc34e650f':('regime_model_attitude','strong_leader_without_parliament_or_elections','good_bad_governing_method','STANDARD_GOOD_BAD_SYSTEM_BATTERY_RESPONSE_CONTRACT','HIGH'),
 'p2lineage_41ddd748f9f2a93683db785a':('regime_model_attitude','strong_leader_without_parliament_or_elections','good_bad_governing_method','STANDARD_GOOD_BAD_SYSTEM_BATTERY_RESPONSE_CONTRACT','HIGH'),
 'p2lineage_036eb0af8b7e0399ded4bf03':('democracy_extent_rating','respondent_country_current','extent_rating','EXPLICIT_NUMERIC_DEMOCRACY_SCALE','HIGH'),
 'p2lineage_3712deca66298b122393c730':('vote_efficacy','individual_vote_future_effect','difference_or_mattering_evaluation','EXPLICIT_INDIVIDUAL_VOTE_EFFECT_TRADEOFF','HIGH'),
 'p2lineage_5e0bfe13e2ee21dc9fd26557':('democracy_feature_ranking','democracy_feature_set','most_essential_feature_choice','EXPLICIT_DEMOCRACY_FEATURE_RANKING_PROMPT','HIGH'),
 'p2lineage_8837761f26bfe3064b3cf9f2':('democracy_feature_essentiality','small_income_gap','importance_or_essentiality','EXPLICIT_DEMOCRATIC_FEATURE_ITEM','HIGH'),
 'p2lineage_8d414802638cad36227d4512':('democracy_priority_tradeoff','democracy_vs_economic_development','forced_priority_choice','EXPLICIT_DEMOCRACY_DEVELOPMENT_TRADEOFF','HIGH'),
 'p2lineage_e470c4c26f0193118b7d7e39':('election_accountability_efficacy','elections_general','government_attention_effect','EXPLICIT_ELECTION_RESPONSIVENESS_ITEM','HIGH'),
 'p2lineage_6a6e7b98d2673ad076ace700':('democracy_general_attitude','democracy_general','agreement_evaluation','EXPLICIT_NONDEMOCRATIC_REGIME_PROBLEMS_ITEM','HIGH'),
 'p2lineage_ec5175ce23d1d790c7bc6895':('democracy_feature_ranking','democracy_feature_set','most_important_feature_choice','EXPLICIT_DEMOCRACY_FEATURE_RANKING_PROMPT','HIGH'),
 'p2lineage_dffc363e4c3b8e26b69d2a7a':('democracy_feature_ranking','democracy_feature_set','second_most_important_feature_choice','EXPLICIT_DEMOCRACY_FEATURE_RANKING_PROMPT','HIGH'),
 'p2lineage_1da06f0895dbefc6af6ad336':('regime_model_attitude','pluralist_parliamentary_elections','good_bad_governing_method','EXPLICIT_PLURALIST_PARLIAMENTARY_MODEL','HIGH'),
 'p2lineage_b9734f69f11663147f77b2cf':('regime_model_attitude','strong_authority_disregarding_electoral_results_and_opposition','good_bad_governing_method','EXPLICIT_AUTHORITARIAN_MODEL','HIGH'),
 'p2lineage_4c4ab877d521bf3b41a1b131':('democracy_general_attitude','democracy_economic_performance','agreement_evaluation','EXPLICIT_DEMOCRACY_ECONOMY_ITEM','HIGH'),
 'p2lineage_1f4094ca62b300286fb2f94e':('electoral_influence_norm','religious_associations_influence_voters','agreement_evaluation','EXPLICIT_ELECTORAL_INFLUENCE_NORM','HIGH'),
 'p2lineage_fc6e652c811093c3619f7e76':('electoral_influence_norm','religious_leaders_influence_voters','agreement_evaluation','EXPLICIT_ELECTORAL_INFLUENCE_NORM','HIGH'),
 'p2lineage_60c6a5636fc932384b344fa1':('democracy_religion_compatibility','democracy_and_islam','agreement_evaluation','EXPLICIT_DEMOCRACY_RELIGION_COMPATIBILITY_ITEM','HIGH'),
 'p2lineage_0a36691ceb3e261a5499bf03':('regime_model_attitude','one_party_rule','agreement','EXACT_PROPOSITION_AND_AGREEMENT_RESPONSE_CONTRACT','HIGH'),
 'p2lineage_de1dfbc5c6ca3d676c9d4139':('electoral_participation_unspecified_mode','elections_general','retrospective_participation','PARTICIPATED_DOES_NOT_PROVE_VOTING_MODE','MEDIUM'),
 'p2lineage_d55c3ce76863a07bbb8ac573':('other_domain','executive_legislative_oversight_tradeoff','other_operator','EXACT_TEXT_EXCLUDES_CURRENT_DOMAIN','HIGH'),
 'p2lineage_0199cc575916bc7deb7d0bbb':('other_domain','religious_leader_influence_on_government','other_operator','EXACT_TEXT_EXCLUDES_CURRENT_DOMAIN','HIGH'),
 'p2lineage_4e5be67780508dcb944ef44e':('other_domain','health_self_assessment','other_operator','EXACT_TEXT_EXCLUDES_CURRENT_DOMAIN','HIGH'),
}

OTHER_PATTERNS=[
 ('demographic_metadata',r'educational level|highest level of education|what is your age|current status|occupation|employment|unemployed|citizen of|language do you speak|mother tongue|religion\?|marital|household|size of town|sex at birth|income'),
 ('government_performance',r'government.*handling|performance of (?:the )?government|how well.*government|fighting corruption|government anti-corruption'),
 ('gender_attitude_or_experience',r'women|woman|men make better political leaders|gender'),
 ('political_accountability_or_efficacy',r'hold government accountable|parliament should ensure|legislature capable|government responds|influence over what the government does'),
 ('political_obligation',r'obey the government|obey the laws'),
 ('political_party_metadata_or_membership',r'party name|party size|global party survey|member of.*party|belong to.*party'),
 ('leader_rating',r'rating of leaders?:'),
 ('government_system_change',r'system of government works fine|needs minor change|needs major change|should be replaced|rather live under our system of government'),
 ('government_transparency_information',r'information held by public authorities|open and transparent|withhold important information'),
 ('religious_governance',r'religious leaders should influence|religious clerics have influence|islamic scholars|islamic jurists'),
 ('policy_or_service_tradeoff',r'school/health|civil servants|market variety|government bear the main responsibility|public education|income gap|prices stable|health services|creating jobs|living standards|environment'),
 ('social_or_personal_attitude',r'free to make decisions|hard work|optimistic|well liked|marriage|friends|thrift|re-incarnation|science|church answers|neighbou?r|work always|salary|health assessment'),
 ('ownership_or_asset',r'personally own|electric connection|own home|deposit in'),
 ('speech_or_association_rights',r'allow .* to speak|ban any organization|join any organization'),
 ('corruption',r'corrupt|bribe'),
 ('work_or_job',r'in your job|decisions in job|supervise|self-employed|work exhaust|profession'),
 ('political_interest_or_discussion',r'politics is so complicated|talk to person|discuss politics'),
 ('policy_ballot_choice',r'vote on open housing law'),
 ('non_domain_other',r'.+'),
]

def classify_one(text:str, response_fams:list[str], topologies:list[str]):
    t=norm(text)
    # Election integrity before generic vote.
    if re.search(r'free(?:ness)? and fair|freeness and fairness|elections? free and fair|way the elections are conducted|evaluate the last parliamentary elections',t):
        return ('election_integrity',scope_target(t),'freeness_fairness_evaluation','EXPLICIT_ELECTION_INTEGRITY_PROPOSITION','HIGH')
    if re.search(r'did you vote|remember if voted|electoral participation: belli turnout|voted in the most recent',t):
        return ('vote_participation',scope_target(t),'retrospective_behavior','EXPLICIT_REPORTED_ELECTORAL_PARTICIPATION','HIGH')
    if re.search(r'will you vote|voting intention|intend to vote',t):
        return ('vote_intention',scope_target(t),'prospective_intention','EXPLICIT_PROSPECTIVE_VOTING_INTENTION','HIGH')
    if re.search(r'if there were a national election tomorrow.*which party|who would r ha(?:s|ve) voted|who would r have voted|voted government\? opposition\?',t):
        return ('vote_choice',scope_target(t),'party_or_bloc_choice','EXPLICIT_OR_SOURCE_NATIVE_VOTE_CHOICE','HIGH')
    if re.search(r'most important influence on whom you voted',t):
        return ('vote_choice_influence','parliamentary_election','ranked_influence','EXPLICIT_VOTE_CHOICE_INFLUENCE','HIGH')
    if re.search(r'work for a candidate or party|participated in campaigning',t):
        return ('campaign_participation',scope_target(t),'retrospective_behavior','EXPLICIT_CAMPAIGN_PARTICIPATION','HIGH')
    if re.search(r'vote doesn.t matter|vote matters|way (?:one|you) votes? can|honest elections makes? a lot of difference',t):
        
        target='honest_elections_life_effect' if 'honest elections' in t else 'individual_vote_future_effect'
        return ('vote_efficacy',target,'difference_or_mattering_evaluation','EXPLICIT_VOTE_EFFECT_PROPOSITION','HIGH')
    if re.search(r'things you must do.*vote in elections',t):
        return ('vote_civic_duty','elections_general','civic_duty','EXPLICIT_CITIZENSHIP_DUTY_ITEM','HIGH')
    if re.search(r'essential for democratic society.*regular elections|importance of free ?& ?fair elections',t):
        
        target='free_fair_elections' if 'free' in t and 'fair' in t else 'regular_elections'
        return ('election_democratic_essentiality',target,'importance_or_essentiality','EXPLICIT_ELECTION_ESSENTIALITY_PROPOSITION','HIGH')
    if re.search(r'choose our leaders.*elections.*other methods|people choose their leaders in free elections',t):
        
        operator='preference_tradeoff' if 'other methods' in t else 'democracy_feature_statement'
        return ('electoral_leader_selection','free_elections',operator,'EXPLICIT_ELECTORAL_LEADER_SELECTION_PROPOSITION','HIGH')
    if re.search(r'without political parties democracy cannot|democracy can function without parties',t):
        return ('party_necessity_for_democracy','political_parties','necessity_evaluation','EXPLICIT_PARTY_NECESSITY_PROPOSITION','HIGH')
    if re.search(r'without a national congress there can be no democracy',t):
        return ('parliament_necessity_for_democracy','national_congress','necessity_evaluation','EXPLICIT_PARLIAMENT_NECESSITY_PROPOSITION','HIGH')
    # Democracy extent and functioning.
    if re.search(r'how (?:much of a democracy|democratic)|extent of democracy|completely undemocratic|not democratic at all|perceived democracy',t):
        country=named_country(t)
        if re.search(r'ten years ago|previous (?:non-democratic )?regime|previous system',t): target='respondent_country_past'
        elif re.search(r'want our country to be in the future|future system',t): target='respondent_country_future_desired'
        elif country=='respondent_country': target='respondent_country_current'
        elif country!='unspecified_country': target='named_country:'+country
        else: target='democracy_extent_unspecified_country'
        return ('democracy_extent_rating',target,'extent_rating','EXPLICIT_DEMOCRACY_EXTENT_SCALE','HIGH' if target!='democracy_extent_unspecified_country' else 'MEDIUM')
    if re.search(r'how well (?:will )?democracy work',t):
        target='respondent_country_future' if 'in ten yrs' in t or 'in ten years' in t or 'will democracy work' in t else 'respondent_country_current'
        return ('democracy_functioning',target,'functioning_evaluation','EXPLICIT_DEMOCRACY_FUNCTIONING_ITEM','HIGH')
    if re.search(r'suitability of democracy|democracy.*suitable|suitable.*democracy',t):
        return ('democracy_suitability','respondent_country','suitability_evaluation','EXPLICIT_DEMOCRACY_SUITABILITY_ITEM','HIGH')
    if re.search(r'democracy: best political system|democracy.*best.*system|having a democratic political system|political system: having a democratic political system',t):
        return ('regime_model_attitude','democratic_system','good_bad_governing_method','STANDARD_POLITICAL_SYSTEM_BATTERY_ITEM','HIGH')
    if 'political-system preference: strong non-democratic leader' in t:
        return ('regime_model_attitude','strong_leader_without_parliament_or_elections','system_preference','EXPLICIT_AUTHORITARIAN_SYSTEM_PREFERENCE','HIGH')
    if 'political-system preference: mixed democratic, strong-leader, and expert rule' in t:
        return ('regime_model_attitude','mixed_democratic_strong_leader_expert_rule','system_preference','EXPLICIT_MIXED_SYSTEM_PREFERENCE','HIGH')
    if re.search(r'democracy.*preferable|prefer.*democr|political-system preference: democratic system',t):
        return ('regime_model_attitude','democratic_system','system_preference','EXPLICIT_DEMOCRATIC_SYSTEM_PREFERENCE','HIGH')
    if re.search(r'non-democratic regimes are indecisive|democracy.*problems',t):
        return ('democracy_general_attitude','democracy_general','agreement_evaluation','EXPLICIT_DEMOCRACY_ATTITUDE_PROPOSITION','HIGH')
    if re.search(r'small income gap.*democratic society',t):
        return ('democracy_feature_essentiality','small_income_gap','importance_or_essentiality','EXPLICIT_DEMOCRATIC_FEATURE_ITEM','HIGH')
    # Regime models.
    if 'strong president and military without meaningful elections' in t:
        return ('regime_model_attitude','strong_president_and_military_without_meaningful_elections','suitability','EXPLICIT_HYBRID_AUTHORITARIAN_MODEL','HIGH')
    if re.search(r'strong leader.*(?:parliament|election)|strong non-democratic leader',t):
        op='agreement' if re.search(r'do you agree|we should have',t) else ('suitability' if 'suitab' in t else ('preference' if 'prefer' in t else 'good_bad_governing_method'))
        return ('regime_model_attitude','strong_leader_without_parliament_or_elections',op,'EXPLICIT_STRONG_LEADER_REGIME_MODEL','HIGH')
    if re.search(r'armed forces.*take control.*when elected leaders abuse power|legitimate for the armed forces to take control',t):
        return ('regime_model_attitude','conditional_military_takeover_when_elected_leaders_abuse_power','agreement','EXPLICIT_CONDITIONAL_MILITARY_INTERVENTION_TRADEOFF','HIGH')
    if re.search(r'army ruling|army rule|military rule|governed by the army',t):
        op='support_oppose' if t.startswith('reject ') else ('agreement' if 'statement 1' in t or 'legitimate' in t else 'good_bad_governing_method')
        return ('regime_model_attitude','military_rule',op,'EXPLICIT_MILITARY_RULE_MODEL','HIGH')
    if re.search(r'only one political party.*allowed|one-party rule|single party',t):
        op='support_oppose' if t.startswith('reject ') else ('approve_disapprove' if 'approve' in t or 'disapprove' in t else 'good_bad_governing_method')
        return ('regime_model_attitude','one_party_rule',op,'EXPLICIT_ONE_PARTY_REGIME_MODEL','HIGH')
    if re.search(r'islamic law without elections or political parties|religious law.*no political parties or elections',t):
        op='approve_disapprove' if 'approve' in t or 'disapprove' in t else ('suitability' if 'suitability' in t else 'good_bad_governing_method')
        return ('regime_model_attitude','religious_law_without_parties_or_elections',op,'EXPLICIT_RELIGIOUS_LAW_NON_ELECTORAL_MODEL','HIGH')
    if re.search(r'islamic-party-only parliamentary elections',t):
        return ('regime_model_attitude','islamic_party_only_parliamentary_elections','suitability','EXPLICIT_ISLAMIC_PARTY_ONLY_MODEL','HIGH')
    if re.search(r'pluralist parliamentary elections',t):
        return ('regime_model_attitude','pluralist_parliamentary_elections','suitability','EXPLICIT_PLURALIST_ELECTORAL_MODEL','HIGH')
    if re.search(r'experts make decisions|experts making decisions',t):
        return ('regime_model_attitude','expert_rule','good_bad_governing_method','STANDARD_POLITICAL_SYSTEM_BATTERY_ITEM','HIGH')
    # Relevant but different axes.
    if re.search(r'system of government works fine|needs minor change|needs major change|should be replaced',t):
        return ('government_system_change','respondent_country_system','change_need_evaluation','EXPLICIT_SYSTEM_CHANGE_ITEM','HIGH')
    if re.search(r'rather live under our system of government',t):
        return ('government_system_attachment','respondent_country_system','comparative_attachment','EXPLICIT_SYSTEM_ATTACHMENT_ITEM','HIGH')
    if re.search(r'men make better political leaders|same chance of being elected',t):
        return ('gender_political_leadership','elected_office','gender_equality_tradeoff','EXPLICIT_GENDER_LEADERSHIP_ITEM','HIGH')
    if re.search(r'woman.*runs? for elected office.*criticized|harassed',t):
        return ('gender_electoral_harassment','women_candidates','likelihood_evaluation','EXPLICIT_CANDIDATE_HARASSMENT_ITEM','HIGH')
    if re.search(r'obey the government.*who you voted|laws of a government.*did not vote',t):
        return ('political_obligation','government_not_voted_for','obedience_tradeoff','EXPLICIT_POLITICAL_OBLIGATION_ITEM','HIGH')
    if re.search(r'parliament should ensure.*president|legislature capable of keeping government leaders in check',t):
        return ('executive_accountability','executive_to_legislature','accountability_evaluation','EXPLICIT_EXECUTIVE_ACCOUNTABILITY_ITEM','HIGH')
    # generic other-domain classification
    for axis,pat in OTHER_PATTERNS:
        if re.search(pat,t): return ('other_domain',axis,'other_operator','EXACT_TEXT_EXCLUDES_CURRENT_DOMAIN','MEDIUM')
    return ('unresolved_axis','unspecified','unresolved','NO_GOVERNED_OPERATOR_RECOVERED','LOW')

queue=read(QREM)
selection_path=os.environ.get('RAWLSING_FIXED_3000_SELECTION','').strip()
if selection_path:
    sel=read(Path(selection_path))
else:
    full_ids=['DEMO_EXTENT','CIVIC_VOTE_MATTERS','CIVIC_VOTE','REJECT_STRONGMAN','REJECT_MILITARY']
    sel=queue[queue.semantic_content_id.isin(full_ids)].copy()
    need=3000-len(sel)
    assert need>=0
    partial=(queue[queue.semantic_content_id.eq('REJECT_ONEPARTY')]
        .assign(_score=lambda d:pd.to_numeric(d.review_priority_score,errors='coerce').fillna(-1),
                _rank=lambda d:pd.to_numeric(d.cell_priority_rank,errors='coerce').fillna(999999))
        .sort_values(['_score','_rank','semantic_pair_candidate_id'],ascending=[False,True,True])
        .head(need).drop(columns=['_score','_rank']))
    sel=pd.concat([sel,partial],ignore_index=True).sort_values(['semantic_content_id','left_source_family','right_source_family','cell_priority_rank','semantic_pair_candidate_id'])
assert len(sel)==3000 and sel.semantic_pair_candidate_id.nunique()==3000
assert set(sel.semantic_pair_candidate_id)<=set(queue.semantic_pair_candidate_id)
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
    texts=uniq(g.exact_question_text.tolist())
    responses=uniq(g.response_family_expectation.tolist())
    tops=uniq(g.response_topology.tolist())
    sids=uniq(s for qid in g.question_implementation_id for s in struct_by_q.get(qid,[]))
    slabels=uniq(regidx.loc[s].structure_label for s in sids if s in regidx.index)
    if lr.lineage_id in OVERRIDES:
        axis,target,op,basis,conf=OVERRIDES[lr.lineage_id]
        per=[(axis,target,op,basis,conf)]
    else:
        per=[classify_one(t,responses,tops) for t in texts]
        signatures=uniq((a,b,c) for a,b,c,_,_ in per)
        if len(signatures)==1:
            axis,target,op=signatures[0]
            basis=' | '.join(uniq(x[3] for x in per)); conf='LOW' if any(x[4]=='LOW' for x in per) else ('MEDIUM' if any(x[4]=='MEDIUM' for x in per) else 'HIGH')
        else:
            # Multiple exact texts in one source-local lineage may not export a single proposition.
            axis,target,op='heterogeneous_lineage','heterogeneous','heterogeneous'
            basis='MULTIPLE_MATERIAL_CLASSIFICATIONS:'+compact([{'axis':x[0],'target':x[1],'operator':x[2]} for x in per]); conf='LOW'
    status='P2_DEMO_ELECTORAL_LINEAGE_CLASSIFIED'
    if axis in {'unresolved_axis','unresolved_main_domain','heterogeneous_lineage'}: status='P2_DEMO_ELECTORAL_LINEAGE_UNRESOLVED'
    elif axis=='other_domain': status='P2_OUT_OF_DOMAIN_LINEAGE_REDIRECTED'
    classes.append({
      'classification_id':stable('p2democlassv1',lr.lineage_id),'lineage_id':lr.lineage_id,'source_family':lr.source_family,'member_count':lr.member_count,
      'variables_json':compact(uniq(g.source_variable_code.tolist())),'waves_json':compact(uniq(g.wave.tolist())),'exact_question_texts_json':compact(texts),
      'response_options_json':compact(uniq(g.response_options_substantive.tolist())),'response_topologies_json':compact(tops),'response_family_expectations_json':compact(responses),
      'semantic_content_ids_json':compact(uniq(g.semantic_content_id.tolist())),'source_structure_ids_json':compact(sids),'source_structure_labels_json':compact(slabels),
      'governed_relation_axis':axis,'governed_target_or_scope':target,'governed_operator':op,'classification_basis':basis,'classification_confidence':conf,
      'authority_status':status,'prohibited_use':'Classification coordinate only; no J-family membership, value harmonization, or respondent join.'
    })
classes=pd.DataFrame(classes).sort_values(['source_family','lineage_id'])
classes.to_csv(OUT/'Rawlsing_P2_Democracy_Electoral_Lineage_Classification_v1.csv',index=False)
cidx=classes.set_index('lineage_id')

MAIN_AXES={'democracy_extent_rating','democracy_functioning','democracy_suitability','democracy_general_attitude','democracy_feature_essentiality','regime_model_attitude','election_integrity','vote_participation','vote_intention','vote_choice','vote_choice_influence','campaign_participation','vote_efficacy','vote_civic_duty','election_democratic_essentiality','electoral_leader_selection','party_necessity_for_democracy','parliament_necessity_for_democracy','regime_system_choice','vote_participation_frequency','democracy_feature_ranking','democracy_priority_tradeoff','election_accountability_efficacy','electoral_influence_norm','democracy_religion_compatibility','electoral_participation_unspecified_mode'}
COORDINATE_AXIS_FAMILIES={
 'democracy_extent_rating':'democracy_evaluation','democracy_functioning':'democracy_evaluation','democracy_suitability':'democracy_evaluation',
 'democracy_general_attitude':'democracy_attitude','democracy_feature_essentiality':'democracy_feature','regime_model_attitude':'regime_model',
 'election_integrity':'election','vote_participation':'electoral_participation','vote_intention':'electoral_participation','vote_choice':'electoral_choice','vote_choice_influence':'electoral_choice',
 'campaign_participation':'electoral_participation','vote_efficacy':'electoral_efficacy','vote_civic_duty':'electoral_norm','election_democratic_essentiality':'electoral_norm',
 'electoral_leader_selection':'electoral_norm','party_necessity_for_democracy':'democratic_institutions','parliament_necessity_for_democracy':'democratic_institutions',
}

def topology_set(row): return set(json.loads(row.response_topologies_json))

rul=[]
for _,cand in sel.iterrows():
    l=cidx.loc[cand.left_lineage_id]; r=cidx.loc[cand.right_lineage_id]
    la,ra=l.governed_relation_axis,r.governed_relation_axis
    lt,rt=l.governed_target_or_scope,r.governed_target_or_scope
    lo,ro=l.governed_operator,r.governed_operator
    if 'UNRESOLVED' in l.authority_status or 'UNRESOLVED' in r.authority_status:
        status='UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_SOURCE_LOCAL_EVIDENCE'; rel='UNRESOLVED'; ceil='NO_AUTHORITY'; rat='At least one source-local lineage lacks one exportable relation, target/scope, and operator.'
    elif la=='other_domain' and ra=='other_domain':
        if lt==rt and lt!='non_domain_other':
            status='REDIRECTED_OUT_OF_DEMOCRACY_ELECTORAL_DOMAIN_SHARED_OTHER_AXIS_NOT_ADJUDICATED'; rel='OTHER_DOMAIN_REVIEW_REQUIRED'; ceil='NO_DEMOCRACY_ELECTORAL_AUTHORITY'; rat='Both exact lineages belong to the same other-domain axis, but this tranche does not manufacture authority for that domain.'
        else:
            status='REJECTED_CONTAMINATED_NEIGHBORHOOD_OTHER_DOMAIN_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='Both items are outside the governed domain and do not share a governed other-domain axis.'
    elif la=='other_domain' or ra=='other_domain':
        status='REJECTED_DEMOCRACY_ELECTORAL_VERSUS_OTHER_DOMAIN_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='One lineage asserts a democracy/electoral proposition while the other exact item belongs to another domain.'
    elif la==ra and lt==rt and lo==ro:
        status='ACCEPTED_TYPED_DEMOCRACY_ELECTORAL_PROPOSITION_RELATION'; rel='REWORDED_PROPOSITION_EQUIVALENCE'
        ceil='QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY' if topology_set(l)==topology_set(r) and len(topology_set(l))==1 else 'QUESTION_PROPOSITION_ONLY'
        rat='Both source-local lineages assert the same governed relation toward the same target/scope with the same operator class.'
    elif la==ra and lt==rt:
        status='ACCEPTED_SAME_CONSTRUCT_TARGET_DIFFERENT_OPERATOR_COORDINATE_ONLY'; rel='CONSTRUCT_TARGET_COORDINATE_ONLY'; ceil='CONSTRUCT_TARGET_ONLY'; rat='The construct and target/scope agree, but the question operators differ; proposition equivalence is prohibited.'
    elif COORDINATE_AXIS_FAMILIES.get(la)==COORDINATE_AXIS_FAMILIES.get(ra) and COORDINATE_AXIS_FAMILIES.get(la):
        status='ACCEPTED_DOMAIN_COORDINATE_ONLY_RELATION_OR_TARGET_SCOPE_DIFFERS'; rel='DOMAIN_COORDINATE_ONLY'; ceil='DOMAIN_COORDINATE_ONLY'; rat='The items share a governed domain family but differ in relation, target, election scope, temporal frame, or regime model.'
    elif la in MAIN_AXES and ra in MAIN_AXES:
        status='REJECTED_FALSE_EQUIVALENCE_DEMOCRACY_ELECTORAL_RELATION_OR_TARGET_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='Both items are in the broad domain but differ materially in relation axis or target/scope.'
    else:
        status='REJECTED_DIFFERENT_GOVERNED_RELATION_AXES'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='The exact lineages assert different governed relations.'
    rid=stable('p2demorulingv1',cand.semantic_pair_candidate_id)
    rul.append({
      'pair_ruling_id':rid,'semantic_pair_candidate_id':cand.semantic_pair_candidate_id,'semantic_content_id':cand.semantic_content_id,
      'left_source_family':cand.left_source_family,'right_source_family':cand.right_source_family,'left_lineage_id':cand.left_lineage_id,'right_lineage_id':cand.right_lineage_id,
      'left_relation_axis':la,'right_relation_axis':ra,'left_target_or_scope':lt,'right_target_or_scope':rt,'left_operator':lo,'right_operator':ro,
      'authority_status':status,'relation_type':rel,'portability_ceiling':ceil,'rationale':rat,'left_classification_id':l.classification_id,'right_classification_id':r.classification_id,
      'two_sided_evidence_status':'EXPLICIT_LINEAGE_NODE_RESPONSE_AND_STRUCTURE_PROVENANCE_BOTH_SIDES','prohibited_use':'No J-family authority, value harmonization, or respondent join follows from this ruling.'
    })
rul=pd.DataFrame(rul)
rul.to_csv(OUT/'Rawlsing_P2_Democracy_Electoral_3000_Pair_Rulings_v1.csv',index=False)

# Evidence ledger: one direct side record per ruling side.
ev=[]
for _,rr in rul.iterrows():
    for side in ('left','right'):
        lid=rr[f'{side}_lineage_id']; c=cidx.loc[lid]; g=nodegroups[lid]
        ev.append({
          'evidence_record_id':stable('p2demoevidencev1',rr.pair_ruling_id,side),'pair_ruling_id':rr.pair_ruling_id,'semantic_pair_candidate_id':rr.semantic_pair_candidate_id,'side':side.upper(),
          'lineage_id':lid,'source_family':c.source_family,'classification_id':c.classification_id,'governed_relation_axis':c.governed_relation_axis,'governed_target_or_scope':c.governed_target_or_scope,'governed_operator':c.governed_operator,
          'question_implementation_ids_json':compact(g.question_implementation_id.tolist()),'wave_variable_locators_json':compact([{'wave':x.wave,'variable':x.source_variable_code,'source_row_index':x.source_row_index} for _,x in g.iterrows()]),
          'exact_question_texts_json':c.exact_question_texts_json,'response_options_json':c.response_options_json,'response_topologies_json':c.response_topologies_json,'response_family_expectations_json':c.response_family_expectations_json,
          'source_structure_ids_json':c.source_structure_ids_json,'source_structure_labels_json':c.source_structure_labels_json,'classification_basis':c.classification_basis,'classification_confidence':c.classification_confidence,
          'evidence_sufficiency':'INCOMPLETE_OR_HETEROGENEOUS' if 'UNRESOLVED' in c.authority_status else 'COMPLETE_FOR_RECORDED_CEILING'
        })
ev=pd.DataFrame(ev)
ev.to_csv(OUT/'Rawlsing_P2_Democracy_Electoral_3000_Two_Sided_Evidence_Ledger_v1.csv',index=False)

remaining=queue[~queue.semantic_pair_candidate_id.isin(set(sel.semantic_pair_candidate_id))].copy()
remaining.to_csv(OUT/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Fixed_3000_Tranche_v4.csv',index=False)
sel.to_csv(OUT/'Rawlsing_P2_Fixed_3000_Tranche_Candidate_Surface_v1.csv',index=False)

summary={
 'contract_version':'P2_FIXED_3000_DEMOCRACY_ELECTORAL_TRANCHE_V1','input_pending_pairs':len(queue),'fixed_work_unit_pairs':len(sel),'remaining_pairs':len(remaining),
 'selected_semantic_id_counts':{str(k):int(v) for k,v in sel.semantic_content_id.value_counts().sort_index().items()},
 'lineages_classified':len(classes),'classification_status_counts':{str(k):int(v) for k,v in classes.authority_status.value_counts().sort_index().items()},
 'pair_status_counts':{str(k):int(v) for k,v in rul.authority_status.value_counts().sort_index().items()},'relation_type_counts':{str(k):int(v) for k,v in rul.relation_type.value_counts().sort_index().items()},
 'evidence_rows':len(ev),'expected_evidence_rows':2*len(rul),'selection_exactly_3000':len(sel)==3000,'queue_partition_exact':len(sel)+len(remaining)==len(queue),
 'selected_ids_unique':sel.semantic_pair_candidate_id.nunique()==3000,'ruling_ids_unique':rul.pair_ruling_id.nunique()==3000,'evidence_ids_unique':ev.evidence_record_id.nunique()==6000,
 'proposition_acceptance_requires_axis_target_operator_identity':bool(((rul.authority_status!='ACCEPTED_TYPED_DEMOCRACY_ELECTORAL_PROPOSITION_RELATION')|((rul.left_relation_axis==rul.right_relation_axis)&(rul.left_target_or_scope==rul.right_target_or_scope)&(rul.left_operator==rul.right_operator))).all()),
 'authority_boundary':'PAIR_RELATION_AUTHORITY_ONLY_NO_J_FAMILY_NO_VALUE_HARMONIZATION'
}
(OUT/'FIXED_3000_TRANCHE_RETURN.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(summary,indent=2,ensure_ascii=False))
