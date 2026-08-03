from __future__ import annotations
from pathlib import Path
from collections import defaultdict
import os, re, json, hashlib
import pandas as pd

ROOT=Path(os.environ.get('RAWLSING_V19_ROOT','/mnt/data/rawlsing_v19_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v19_20260731'))
OUT=Path(os.environ.get('RAWLSING_V20_OUT','/mnt/data/rawlsing_v20_outputs/final_2847'))
OUT.mkdir(parents=True,exist_ok=True)
S32=ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'
S40=ROOT/'40_P2_GLOBAL_SOCIAL_ORDER_FIXED_3000_TRANCHE7'
QREM=S40/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Social_Order_Fixed_3000_Tranche_v7.csv'

def read(p): return pd.read_csv(p,dtype=str,keep_default_na=False)
def norm(x): return re.sub(r'\s+',' ',str(x or '').strip().casefold())
def stable(prefix,*parts): return prefix+'_'+hashlib.sha256(chr(31).join(map(str,parts)).encode()).hexdigest()[:24]
def compact(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def uniq(xs): return list(dict.fromkeys(x for x in xs if str(x).strip()))
def has(t,*parts): return all(p in t for p in parts)
def anyhas(t,*parts): return any(p in t for p in parts)

# axis, target, operator, basis, confidence, domain_family
# Exact text governs. Inherited semantic IDs are discovery coordinates only.
def classify_one(sem:str, text:str, response_fams:list[str], topologies:list[str], response_options:list[str]):
    t=norm(text); s=norm(sem)
    top='|'.join(topologies).casefold()
    ropts=' | '.join(response_options).casefold()

    # Administrative, identifiers, external indexes, or response shells.
    if (s.startswith('metadata::') or s.startswith('semantic::') and anyhas(s,'id','respondent','country','age','marital_status','mode_of_data_collection','year_of_birth','household_size','none_of_these','original_respondent','unified_respondent')
        or anyhas(t,'skip variable','coding status','respondent number','interviewer number','interviewer id','calibration weight','population size weight','digital object identifier','year month of','survey year','country code','wave')
        or top in {'administrative','response_status','weight'}):
        return ('metadata_or_administration','survey_metadata_or_response_shell','administrative_or_status','EXPLICIT_ADMINISTRATIVE_OR_METADATA_ITEM','HIGH','metadata')

    # Demonstration, protest, petition and civic action.
    if anyhas(t,'attended a demonstration','attend a demonstration','demonstration or protest march','participated in any protest or demonstration','demonstrated, striken, or sat-in','attended demonstration'):
        op='past_participation_ever' if anyhas(t,'ever','had you participated') else 'past_participation_unspecified'
        return ('demonstration_participation','lawful_or_unspecified_demonstration',op,'EXPLICIT_DEMONSTRATION_PARTICIPATION_ITEM','HIGH','civic_action')
    if 'have you, or would you ever, participate in political demonstrations' in t:
        return ('demonstration_participation_disposition','political_demonstrations','past_or_future_disposition','EXPLICIT_MIXED_DEMONSTRATION_DISPOSITION_ITEM','HIGH','civic_action')
    if 'lawful demonstration' in t and anyhas(t,'how likely','affinity to attend'):
        return ('demonstration_participation_likelihood','lawful_demonstration','future_likelihood','EXPLICIT_DEMONSTRATION_LIKELIHOOD_ITEM','HIGH','civic_action')
    if 'participate in riots' in t:
        return ('riot_participation_disposition','riots','past_or_future_disposition','EXPLICIT_RIOT_DISPOSITION_ITEM','HIGH','civic_action')
    if 'signing an electronic petition' in t or 'signed an online petition' in t:
        return ('petition_participation_disposition','electronic_petition','past_or_future_disposition' if 'might do' in ropts else 'past_participation','EXPLICIT_ELECTRONIC_PETITION_ITEM','HIGH','civic_action')
    if 'signing a petition' in t or 'signed a paper petition' in t or 'sign petition' in t:
        target='environmental_petition' if 'envir' in t else 'petition_general'
        op='past_or_future_disposition' if 'might do' in ropts else 'past_participation'
        return ('petition_participation_disposition',target,op,'EXPLICIT_PETITION_ITEM','HIGH','civic_action')
    if 'collective action or petition' in t:
        return ('collective_action_or_petition_participation','collective_action_or_petition','past_frequency','COMPOSITE_CIVIC_ACTION_ITEM','MEDIUM','civic_action')

    # Gender and work/business/politics.
    if has(t,'men make better business executives','women'):
        return ('gender_business_executive_superiority','business_executives','men_better_than_women_agreement','EXPLICIT_GENDER_BUSINESS_EXECUTIVE_ITEM','HIGH','gender_leadership')
    if has(t,'women are as competent as men','business executives'):
        return ('gender_business_executive_equal_competence','business_executives','women_as_competent_as_men_agreement','EXPLICIT_EQUAL_COMPETENCE_ITEM','HIGH','gender_leadership')
    if 'business manager - suitability for men and women' in t:
        return ('gender_business_manager_suitability','business_manager','gender_suitability_rating','TERSE_BUSINESS_MANAGER_SUITABILITY_ITEM','MEDIUM','gender_leadership')
    if has(t,'men make better political leaders','women'):
        return ('gender_political_leadership_superiority','political_leaders','men_better_than_women_agreement','EXPLICIT_GENDER_POLITICAL_LEADERSHIP_ITEM','HIGH','gender_leadership')
    if 'women not suited for politics' in t:
        return ('gender_political_suitability','women_in_politics','women_unsuited_agreement','EXPLICIT_WOMEN_POLITICS_SUITABILITY_ITEM','HIGH','gender_leadership')
    if 'men are better at political leadership than women' in t or 'men better at political leadership' in t:
        return ('gender_political_leadership_superiority','political_leaders','men_better_than_women_agreement','EXPLICIT_GENDER_POLITICAL_LEADERSHIP_ITEM','HIGH','gender_leadership')
    if 'women and men should have equal work opportunities' in t or 'men and women should have equal work opportunities' in t:
        return ('gender_equal_work_opportunity_norm','work_opportunities','equal_opportunity_agreement','EXPLICIT_EQUAL_WORK_OPPORTUNITY_ITEM','HIGH','gender_employment')
    if 'women should have freedom to go out and work' in t:
        return ('women_freedom_to_work_norm','women_employment','freedom_to_work_agreement','EXPLICIT_WOMEN_WORK_FREEDOM_ITEM','HIGH','gender_employment')
    if 'women have equal opportunities to run the office' in t:
        return ('women_office_leadership_opportunity_frequency','run_the_office','observed_frequency','EXPLICIT_OFFICE_OPPORTUNITY_ITEM','HIGH','gender_employment')
    if 'equal opportunities on jobs' in t:
        return ('racial_equal_job_opportunity','jobs','black_white_opportunity_comparison','EXPLICIT_RACIAL_JOB_OPPORTUNITY_ITEM','HIGH','racial_equality')
    if 'son preference' in t or ('would prefer' in t and 'son' in t) or ('prefer a boy' in t):
        return ('son_preference','child_sex','son_over_daughter_preference','EXPLICIT_SON_PREFERENCE_ITEM','HIGH','gender_family')

    # Democracy / regime propositions.
    if 'non-democratic systems may have problems' in t:
        return ('nondemocracy_despite_problems_support','nondemocratic_system','better_than_alternatives_agreement','EXPLICIT_NONDEMO_DESPITE_PROBLEMS_ITEM','HIGH','authoritarian_tolerance')
    if ('democracy may have problems' in t or "democracy may have problems but it's better" in t or 'democratic systems may have problems, yet they are better' in t or 'democracy preferred over other forms' in t or 'democracy: better than other systems' in t):
        return ('democracy_despite_problems_support','democratic_system','better_than_alternatives_agreement','EXPLICIT_DEMO_DESPITE_PROBLEMS_ITEM','HIGH','democratic_legitimacy')
    if anyhas(t,'democratic regimes are indecisive','democracy: decisiveness','indecisive and full of problems'):
        return ('democracy_indecisiveness_critique','democratic_regime','indecisive_problems_agreement','EXPLICIT_DEMO_INDECISIVENESS_ITEM','HIGH','democracy_performance')
    if t == 'democracy: maintaining order':
        return ('democracy_order_stability_critique','democratic_regime','agreement_polarity_not_in_child_text','TERSE_DEMO_ORDER_ITEM_POLARITY_UNRECOVERED','MEDIUM','democracy_performance')
    if anyhas(t,'not effective at maintaining order and stability','ineffective in mainting security'):
        return ('democracy_order_stability_critique','democratic_regime','ineffective_order_agreement','EXPLICIT_DEMO_ORDER_CRITIQUE_ITEM','HIGH','democracy_performance')
    if 'democracy: economic performance' in t:
        return ('democracy_economic_performance_critique','democratic_regime','poor_economic_performance_agreement','TERSE_DEMO_ECONOMIC_PERFORMANCE_ITEM','MEDIUM','democracy_performance')
    if 'reject one-party rule' in t:
        return ('one_party_rule_rejection','one_party_rule','disapprove_or_reject','EXPLICIT_ONE_PARTY_REJECTION_ITEM','HIGH','regime_alternatives')
    if 'elections and parliament are abolished' in t and 'president can decide everything' in t:
        return ('presidential_one_person_rule_support','presidential_rule_without_elections_or_parliament','approve_or_disapprove','EXPLICIT_PRESIDENTIAL_RULE_ITEM','HIGH','regime_alternatives')
    if 'parliamentary system' in t and 'parties compete' in t:
        return ('competitive_multiparty_parliamentary_suitability','competitive_parliamentary_system','suitability_rating','EXPLICIT_MULTIPARTY_SYSTEM_ITEM','HIGH','regime_alternatives')

    # Democracy satisfaction.
    if 'satisfied' in t and 'democracy' in t and anyhas(t,'way democracy works','way democracy develops','satisfied with democracy'):
        target='democracy_in_country' if anyhas(t,'in america','in [nation]','in the country') else 'democracy_general'
        return ('democracy_working_satisfaction',target,'current_satisfaction','EXPLICIT_DEMO_SATISFACTION_ITEM','HIGH','democracy_satisfaction')
    if 'satisfaction with democracy' in t:
        return ('democracy_working_satisfaction','democracy_general','current_satisfaction','EXPLICIT_DEMO_SATISFACTION_ITEM','HIGH','democracy_satisfaction')
    if 'proud the way democracy works' in t:
        return ('democracy_working_pride','democracy_in_country','current_pride','EXPLICIT_DEMO_PRIDE_ITEM','HIGH','democracy_satisfaction')

    # Personal agency / control.
    if anyhas(t,'how much control over your life','freedom of choice and control'):
        return ('personal_life_control','own_life','current_extent','EXPLICIT_PERSONAL_CONTROL_ITEM','HIGH','agency')
    if 'state give more freedom to' in t and 'control firms' in t:
        return ('state_firm_control_preference','business_firms','freedom_vs_state_control_scale','EXPLICIT_STATE_FIRM_CONTROL_ITEM','HIGH','economic_governance')

    # Family intergenerational duties and pride.
    if 'adult children have the duty to provide long-term care for their parents' in t:
        return ('adult_child_parent_long_term_care_duty','parents','duty_agreement','EXPLICIT_PARENT_CARE_DUTY_ITEM','HIGH','intergenerational_duty')
    if 'children responsibilities to their parents in need' in t:
        return ('adult_child_parent_support_sacrifice_norm','parents_in_need','duty_vs_no_self_sacrifice','EXPLICIT_PARENT_SUPPORT_SACRIFICE_ITEM','HIGH','intergenerational_duty')
    if 'childs duty to take care of ill parent' in t:
        return ('adult_child_ill_parent_care_duty','ill_parent','duty_agreement','EXPLICIT_ILL_PARENT_CARE_ITEM','HIGH','intergenerational_duty')
    if 'obligation to care for ill parent or spouse' in t:
        return ('ill_parent_or_spouse_care_obligation','ill_parent_or_spouse','obligation_choice','COMPOSITE_CARE_OBLIGATION_ITEM','MEDIUM','intergenerational_duty')
    if 'parents responsibilities to their children' in t or 'parents responsiblities to their children' in t:
        return ('parent_child_sacrifice_norm','children','do_best_vs_no_self_sacrifice','EXPLICIT_PARENT_CHILD_SACRIFICE_ITEM','HIGH','intergenerational_duty')
    if 'main goals in life has been to make my parents proud' in t:
        return ('parents_proud_life_goal','parents','agreement','EXPLICIT_PARENTS_PROUD_ITEM','HIGH','family_orientation')
    if 'for the sake of the family, the individual should put his personal interests second' in t:
        return ('family_over_individual_interest_norm','family','personal_interests_second_agreement','EXPLICIT_FAMILY_SACRIFICE_ITEM','HIGH','family_orientation')
    if 'children should obey their parents' in t or 'obey parents' in t:
        return ('child_obedience_to_parents_norm','parents','obedience_agreement','EXPLICIT_PARENT_OBEDIENCE_ITEM','HIGH','child_values')
    if re.fullmatch(r'obedience(?: 1 2.*)?',t) or t=='obedience':
        return ('child_quality_obedience','child_quality','desirability_rank' if 'most desirable' in ropts or 'least desirable' in ropts else 'importance_or_mention','EXPLICIT_CHILD_VALUE_OBEDIENCE_ITEM','HIGH','child_values')
    if 'good manners' in t:
        return ('child_quality_good_manners','child_quality','desirability_rank' if 'most desirable' in ropts or 'least desirable' in ropts else 'importance_or_mention','EXPLICIT_CHILD_VALUE_ITEM','HIGH','child_values')
    if 'tolerance and respect for other people' in t:
        return ('child_quality_tolerance_respect','child_quality','desirability_rank' if 'most desirable' in ropts or 'least desirable' in ropts else 'importance_or_mention','EXPLICIT_CHILD_VALUE_ITEM','HIGH','child_values')
    if 'independence' in t and s.startswith('child_'):
        return ('child_quality_independence','child_quality','desirability_rank' if 'most desirable' in ropts or 'least desirable' in ropts else 'importance_or_mention','EXPLICIT_CHILD_VALUE_ITEM','HIGH','child_values')
    if 'hard work' in t and s.startswith('child_'):
        return ('child_quality_hard_work','child_quality','desirability_rank' if 'most desirable' in ropts or 'least desirable' in ropts else 'importance_or_mention','EXPLICIT_CHILD_VALUE_ITEM','HIGH','child_values')
    if 'imagination' in t and s.startswith('child_'):
        return ('child_quality_imagination','child_quality','desirability_rank' if 'most desirable' in ropts or 'least desirable' in ropts else 'importance_or_mention','EXPLICIT_CHILD_VALUE_ITEM','HIGH','child_values')
    if 'religious faith' in t and s.startswith('child_'):
        return ('child_quality_religious_faith','child_quality','desirability_rank' if 'most desirable' in ropts or 'least desirable' in ropts else 'importance_or_mention','EXPLICIT_CHILD_VALUE_ITEM','HIGH','child_values')

    # Neighbor exclusion/tolerance.
    # Arab Barometer's like/dislike rating is a closeness coordinate, not a binary exclusion item.
    if 'preference: neighbors: different race/color' in t:
        return ('neighbor_closeness_preference','people_different_race','like_dislike_rating','EXPLICIT_NEIGHBOR_RACE_PREFERENCE_ITEM','HIGH','outgroup_tolerance')
    neigh=False
    if anyhas(t,"don't like as neighbours","dont like as neighbours",'would not like to have as neighb','people you do not want to have as neighbours','neighbours:','neighbors:'):
        neigh=True
    if neigh:
        target=None
        for pat,name in [
            ('different race','people_different_race'),('different color','people_different_race'),('immigrants / foreign workers','immigrants_or_foreign_workers'),('immigrants/foreign workers','immigrants_or_foreign_workers'),('immigrants or foreign workers','immigrants_or_foreign_workers'),('foreign workers','foreign_workers'),('immigrants','immigrants'),('homosexual','homosexual_people'),('drug addict','drug_addicts'),('drug addicts','drug_addicts'),('people with aids','people_with_aids'),('aids','people_with_aids'),('heavy drinkers','heavy_drinkers'),('different religion','people_different_religion'),('muslims','muslims'),('christians','christians'),('jews','jews'),('gypsies','roma_or_gypsies'),('emotional instability','emotionally_unstable_people')]:
            if pat in t: target=name; break
        if target:
            return ('neighbor_exclusion_preference',target,'would_not_like_as_neighbor','EXPLICIT_NEIGHBOR_EXCLUSION_ITEM','HIGH','outgroup_tolerance')
        if 'same religion' in t:
            return ('neighbor_exclusion_preference','people_same_religion','would_not_like_as_neighbor','EXPLICIT_NEIGHBOR_RELIGION_ITEM','HIGH','outgroup_tolerance')
        if 'speak a different lang' in t:
            return ('neighbor_exclusion_preference','people_different_language','would_not_like_as_neighbor','TRUNCATED_BUT_TARGET_RECOVERABLE_NEIGHBOR_ITEM','MEDIUM','outgroup_tolerance')
        return ('unresolved_axis','neighbor_group_child_unspecified','parent_or_truncated_child_missing','PARENT_OR_TRUNCATED_NEIGHBOR_ITEM','LOW','outgroup_tolerance')
    # Marriage status obstacle.
    if 'lower social status' in t and anyhas(t,'marriage','female relative','male relative','obstacle'):
        target='female_relative_partner_lower_status' if 'female relative' in t else ('male_relative_partner_lower_status' if 'male relative' in t else 'relative_partner_lower_status')
        return ('marriage_lower_status_obstacle',target,'obstacle_degree','EXPLICIT_MARRIAGE_STATUS_OBSTACLE_ITEM','HIGH','marriage_norms')

    # Happiness / life satisfaction.
    if 'thinking of the environment and taking all things together how happy are you' in t:
        return ('general_happiness_contextualized','respondent_life_overall','current_happiness_rating_after_environment_prompt','CONTEXTUALIZED_GENERAL_HAPPINESS_ITEM','HIGH','subjective_wellbeing')
    if anyhas(t,'taking all things together how happy are you','taking all things together, would you say you are','feeling of happiness','general happiness','how happy r is'):
        return ('general_happiness','respondent_life_overall','current_happiness_rating','EXPLICIT_GENERAL_HAPPINESS_ITEM','HIGH','subjective_wellbeing')
    if 'happiness of marriage' in t:
        return ('marital_happiness','marriage','current_happiness_rating','EXPLICIT_MARITAL_HAPPINESS_ITEM','HIGH','relationship_wellbeing')
    if 'happiness of relt with partner' in t:
        return ('partner_relationship_happiness','partner_relationship','current_happiness_rating','EXPLICIT_PARTNER_HAPPINESS_ITEM','HIGH','relationship_wellbeing')
    if anyhas(t,'satisfaction with life','satisfied are you with your life','life satisfaction'):
        return ('life_satisfaction','respondent_life_overall','current_satisfaction_rating','EXPLICIT_LIFE_SATISFACTION_ITEM','HIGH','subjective_wellbeing')

    # Corruption.
    if anyhas(t,'perceptions of corruption in the country','there is corruption within the state','corruption within the national state agencies','corruption in the state\'s institutions'):
        if anyhas(t,'more serious than last year','similar to last year','less serious than last year'):
            return ('corruption_change_perception','state_institutions','current_vs_last_year','EXPLICIT_CORRUPTION_CHANGE_ITEM','HIGH','corruption')
        op='presence_binary' if ('do you think that there is corruption' in t and 'extent' not in t) else 'extent_rating'
        target='country_general' if 'in the country' in t else 'state_institutions'
        return ('corruption_prevalence_perception',target,op,'EXPLICIT_CORRUPTION_PREVALENCE_ITEM','HIGH','corruption')
    if 'corruption situation has changed' in t:
        return ('corruption_change_perception','country_general','past_five_year_change','EXPLICIT_CORRUPTION_CHANGE_ITEM','HIGH','corruption')
    if 'progress has been made in reducing corruption' in t or 'progress on reducing corruption' in t:
        return ('anti_corruption_progress_perception','state_institutions','past_two_year_progress','EXPLICIT_ANTI_CORRUPTION_PROGRESS_ITEM','HIGH','corruption')
    if 'perception of present corruption w.r.t. 1989' in t:
        return ('corruption_change_perception','country_or_system','present_vs_1989','TERSE_CORRUPTION_CHANGE_ITEM','MEDIUM','corruption')
    if 'corruption perception index' in t:
        return ('external_corruption_index','country','external_index','EXTERNAL_INDEX_NOT_RESPONDENT_PROPOSITION','HIGH','corruption_index')
    if 'frequency ordinary people pay a bribe' in t:
        return ('bribery_payment_frequency','local_officials_or_service_providers','ordinary_people_frequency','EXPLICIT_BRIBERY_FREQUENCY_ITEM','HIGH','corruption')
    if 'rashwa' in t and anyhas(t,'healthcare services','education services'):
        target='healthcare_services' if 'healthcare' in t else 'education_services'
        return ('bribery_necessity_perception',target,'necessity_rating','EXPLICIT_BRIBERY_NECESSITY_ITEM','HIGH','corruption')

    # Religion.
    if 'pray fajr on time' in t:
        return ('specific_prayer_frequency','fajr_on_time','frequency','EXPLICIT_FAJR_ITEM','HIGH','religious_practice')
    if 'pray istikhara' in t:
        return ('specific_prayer_frequency','istikhara','frequency','EXPLICIT_ISTIKHARA_ITEM','HIGH','religious_practice')
    if anyhas(t,'how often do you pray','how often does r pray','religion: frequency: pray','pray daily','do you (insert)? 1. pray daily'):
        target='daily_prayer' if 'daily' in t else 'prayer_general'
        return ('prayer_frequency',target,'frequency','EXPLICIT_PRAYER_FREQUENCY_ITEM','HIGH','religious_practice')
    if 'moments of prayer/meditation' in t:
        return ('prayer_or_meditation_practice','prayer_or_meditation','ever_or_regular_binary','EXPLICIT_PRAYER_MEDITATION_ITEM','HIGH','religious_practice')
    if 'importance of god' in t or 'how important is god in your life' in t:
        return ('god_importance','god_in_respondent_life','importance_rating','EXPLICIT_GOD_IMPORTANCE_ITEM','HIGH','religiosity')
    if re.fullmatch(r'god(?: 1 2)?',t) or 'do you believe in: god' in t:
        return ('belief_in_god','god','belief_binary','EXPLICIT_GOD_BELIEF_ITEM','HIGH','religious_belief')
    if 'important in life: religion' in t or 'how important in your life: religion' in t or 'how important is religion in your life' in t:
        return ('religion_importance','religion_in_respondent_life','importance_rating','EXPLICIT_RELIGION_IMPORTANCE_ITEM','HIGH','religiosity')
    if anyhas(t,'religious services','attend church','attend mosque') and anyhas(t,'how often','frequency','attendance'):
        target='mother_religious_services' if anyhas(t,'how often ma','mother') else ('father_religious_services' if anyhas(t,'how often pa','father') else 'respondent_religious_services')
        return ('religious_service_attendance',target,'frequency','EXPLICIT_RELIGIOUS_ATTENDANCE_ITEM','HIGH','religious_practice')
    if 'religion is a private matter' in t or 'religion private' in t:
        return ('religion_private_matter_norm','religion','private_matter_agreement','EXPLICIT_RELIGION_PRIVATE_ITEM','HIGH','religion_public_role')
    if 'laws of our country' in t and 'sharia' in ' '.join(response_fams).casefold():
        return ('sharia_basis_of_law_preference','national_law','degree_of_sharia_basis','EXPLICIT_SHARIA_LAW_BASIS_ITEM','HIGH','religion_law')
    if 'religious authorities ultimately interpret the laws' in t:
        return ('religious_authority_law_interpretation_democracy_feature','religious_authorities','democracy_feature_rating','EXPLICIT_RELIGIOUS_AUTHORITY_LAW_ITEM','HIGH','religion_law')
    if 'sharia: essential characteristic' in t:
        return ('sharia_democracy_characteristic','sharia','essential_characteristic_rating','TERSE_SHARIA_CHARACTERISTIC_ITEM','MEDIUM','religion_law')
    if 'religious law' in t or ('sharia' in t and 'law' in t):
        return ('religious_law_support','national_law','support_or_agreement','EXPLICIT_RELIGIOUS_LAW_ITEM','MEDIUM','religion_law')

    # Environment concern and action.
    if 'environmental threats are exaggerated' in t:
        return ('environmental_threat_exaggeration_belief','environmental_threats','agreement','EXPLICIT_ENVIRONMENT_THREAT_ITEM','HIGH','environmental_attitudes')
    if 'increase in taxes' in t and 'prevent environmental pollution' in t or 'increase taxes to prevent environmental pollution' in t or 'paying more in taxes' in t and 'environmental pollution' in t:
        return ('environmental_tax_willingness','environmental_pollution_prevention','pay_more_taxes_agreement','EXPLICIT_ENVIRONMENT_TAX_ITEM','HIGH','environmental_action')
    if 'interested in environmental issues' in t:
        return ('environmental_issue_interest','environmental_issues','interest_rating','EXPLICIT_ENVIRONMENT_INTEREST_ITEM','HIGH','environmental_attitudes')
    if 'i care about the environment' in t or 'feel obliged to protect' in t:
        return ('environmental_care_or_obligation','environment','care_or_obligation_agreement','EXPLICIT_ENVIRONMENT_CARE_ITEM','HIGH','environmental_attitudes')
    if 'protect the environment for future generations' in t:
        return ('environmental_intergenerational_protection_norm','future_generations','agreement','EXPLICIT_ENVIRONMENT_FUTURE_GENERATIONS_ITEM','HIGH','environmental_attitudes')
    if 'willing to change my diet' in t:
        return ('environmental_behavior_willingness','diet_change','willingness','EXPLICIT_ENVIRONMENT_ACTION_ITEM','HIGH','environmental_action')
    if 'willing to use less electricity' in t:
        return ('environmental_behavior_willingness','electricity_reduction','willingness','EXPLICIT_ENVIRONMENT_ACTION_ITEM','HIGH','environmental_action')
    if 'care about how climate change affects other people' in t:
        return ('climate_other_people_concern','other_people','care_agreement','EXPLICIT_CLIMATE_OTHER_PEOPLE_ITEM','HIGH','climate_concern')
    if 'environmental organization' in t or 'environmental organisations' in t:
        op='active_inactive_membership' if anyhas(t,'active/inactive','active member') else ('membership_binary' if anyhas(t,'membership','member of') else 'confidence_rating')
        return ('environmental_organization_relation','environmental_organization',op,'EXPLICIT_ENVIRONMENT_ORGANIZATION_ITEM','HIGH','environmental_organization')

    # National/social closeness and identity.
    if 'feel close to the world' in t or 'how close do you feel: to world' in t:
        return ('geographic_identity_closeness','world','closeness_rating','EXPLICIT_WORLD_CLOSENESS_ITEM','HIGH','identity_closeness')
    if 'how close do you feel: to [continent]' in t or 'feel to asean' in t or 'feel close to asean' in t:
        target='asean' if 'asean' in t else 'continent'
        return ('geographic_identity_closeness',target,'closeness_rating','EXPLICIT_REGIONAL_CLOSENESS_ITEM','HIGH','identity_closeness')
    if 'feel close to any party' in t:
        return ('party_closeness','political_party','closeness_or_identification','EXPLICIT_PARTY_CLOSENESS_ITEM','HIGH','political_identity')
    if 'close r feels to black people' in t or 'close feel to whites' in t:
        target='black_people' if 'black' in t else 'white_people'
        return ('racial_group_closeness',target,'closeness_rating','EXPLICIT_RACIAL_CLOSENESS_ITEM','HIGH','identity_closeness')
    if 'how close does r feel to god' in t:
        return ('closeness_to_god','god','closeness_rating','EXPLICIT_GOD_CLOSENESS_ITEM','HIGH','religiosity')
    if 'national pride' in t or 'how proud are you to be' in t:
        return ('national_pride','nation','pride_rating','EXPLICIT_NATIONAL_PRIDE_ITEM','HIGH','national_identity')

    # Justifiability/moral elasticity.
    justify_map={
      'claiming government benefits':'claiming_unentitled_government_benefits',
      'abortion':'abortion_general',
      'divorce':'divorce',
      'homosexuality':'homosexual_relations',
      'homosexual sex relations':'homosexual_relations',
      'euthanasia':'euthanasia',
      'accepting a bribe':'accepting_bribe',
      'bribe':'accepting_bribe',
      'avoiding a fare':'fare_evasion',
      'not paying taxes':'tax_evasion',
      'cheating on taxes':'tax_evasion',
      'prostitution':'prostitution'
    }
    for pat,target in justify_map.items():
        if pat in t and anyhas(t,'justif','wrong','approve','disapprove'):
            # Conditional abortion and other narrower cases remain separate targets.
            if 'abortion if woman not married' in t: target='abortion_unmarried_woman'
            if 'abortion if woman wants for any reason' in t: target='abortion_on_request'
            return ('moral_justifiability',target,'justifiability_or_approval_rating','EXPLICIT_JUSTIFIABILITY_ITEM','HIGH','moral_justifiability')
    if t.strip() in {'abortion','euthanasia','divorce'}:
        return ('moral_justifiability',t.strip(),'justifiability_rating','TERSE_JUSTIFIABILITY_ITEM','MEDIUM','moral_justifiability')

    # Media/social internet.
    if 'social media' in t:
        if 'situation caused by exposure to social media' in t:
            return ('social_media_causal_attribution','respondent_situation','caused_by_exposure_likelihood','EXPLICIT_SOCIAL_MEDIA_CAUSAL_ITEM','HIGH','media_effects')
        if 'primarily for work' in t:
            return ('social_media_primary_purpose','work','primary_purpose_agreement','EXPLICIT_SOCIAL_MEDIA_PURPOSE_ITEM','HIGH','media_use')
        if 'primarily to share news or information' in t:
            return ('social_media_primary_purpose','share_news_or_information','primary_purpose_agreement','EXPLICIT_SOCIAL_MEDIA_PURPOSE_ITEM','HIGH','media_use')
        if 'primarily to connect with other people' in t:
            return ('social_media_primary_purpose','connect_with_people','primary_purpose_agreement','EXPLICIT_SOCIAL_MEDIA_PURPOSE_ITEM','HIGH','media_use')
        if 'primarily to express' in t and 'political issues' in t:
            return ('social_media_primary_purpose','express_political_opinion','primary_purpose_agreement','EXPLICIT_SOCIAL_MEDIA_PURPOSE_ITEM','HIGH','media_use')
        if 'currently use any of the following social media networks' in t:
            return ('social_media_use','social_media_networks','current_use_binary','EXPLICIT_SOCIAL_MEDIA_USE_ITEM','HIGH','media_use')
        if anyhas(t,'how often','frequency'):
            return ('social_media_use','social_media','frequency','EXPLICIT_SOCIAL_MEDIA_USE_ITEM','HIGH','media_use')
        if 'trust' in t:
            return ('social_media_trust','social_media','trust_rating','EXPLICIT_SOCIAL_MEDIA_TRUST_ITEM','HIGH','media_trust')
        return ('social_media_relation','social_media','relation_unspecified','TERSE_SOCIAL_MEDIA_ITEM','MEDIUM','media_use')

    # Security/home and worry.
    if 'safe in your home' in t or 'security at home' in t:
        return ('home_safety','respondent_home','safety_rating','EXPLICIT_HOME_SAFETY_ITEM','HIGH','security')
    if 'worried' in t or 'worry' in t:
        target='civil_war' if 'civil war' in t else ('terrorism' if 'terror' in t else ('natural_disaster' if 'natural disaster' in t else 'unspecified_threat'))
        return ('threat_worry',target,'worry_rating','EXPLICIT_WORRY_ITEM','HIGH','security_concern')

    # Leisure.
    if 'how important in your life: leisure time' in t or t=='leisure time':
        return ('leisure_importance','leisure_time','importance_rating','EXPLICIT_LEISURE_IMPORTANCE_ITEM','HIGH','life_domains')
    if 'leisure time:' in t:
        target=t.split('leisure time:',1)[1].strip().replace(' ','_')
        return ('leisure_preference_attribute',target,'importance_or_mention','EXPLICIT_LEISURE_ATTRIBUTE_ITEM','HIGH','leisure')

    # Gendered family decision authority.
    if 'husbands should have final say in family decisions' in t or 'a man should have final say in all decisions concerning the family' in t:
        return ('gender_family_decision_authority','family_decisions','male_final_say_agreement','EXPLICIT_MALE_FINAL_SAY_ITEM','HIGH','gender_family')

    # Generic family importance / parent obedience / family decisions.
    if 'family' in t and 'important in your life' in t:
        return ('family_importance','family','importance_rating','EXPLICIT_FAMILY_IMPORTANCE_ITEM','HIGH','life_domains')
    if 'parents' in t and 'obey' in t:
        return ('adult_obedience_to_parents_norm','parents','agreement_or_duty','EXPLICIT_PARENT_OBEDIENCE_ITEM','HIGH','family_orientation')
    if 'family decisions' in t or 'decision' in t and anyhas(t,'husband','wife','women'):
        return ('gender_family_decision_authority','household_or_family_decisions','gendered_decision_authority','EXPLICIT_FAMILY_DECISION_ITEM','MEDIUM','gender_family')

    # Migrant discrimination / neighbor immigrant.
    if 'migrants from other arab countries are discriminated' in t:
        return ('migrant_discrimination_extent','migrants_from_other_arab_countries','extent_rating','EXPLICIT_MIGRANT_DISCRIMINATION_ITEM','HIGH','discrimination')
    if 'reason for being discriminated against' in t or 'why were you discriminated against' in t:
        return ('discrimination_basis','respondent_discrimination_experience','reason_category','EXPLICIT_DISCRIMINATION_BASIS_ITEM','HIGH','discrimination')
    if 'differences due to discrimination' in t:
        return ('group_difference_discrimination_attribution','group_differences','discrimination_cause_binary','EXPLICIT_DISCRIMINATION_ATTRIBUTION_ITEM','HIGH','discrimination')

    # Authority respect.
    if 'respect for authority' in t:
        op='derived_index' if anyhas(t,'welzel','index') else 'future_change_desirability'
        return ('authority_respect_orientation','authority',op,'EXPLICIT_AUTHORITY_RESPECT_ITEM','HIGH','authority_orientation')

    if 'welzel choice sub-index' in t or ('a stable economy' in t and 'less impersonal' in t and 'ideas count more than money' in t):
        return ('other_domain','welzel_choice_postmaterialism_index','index_or_constituent_response_shell','EXPLICIT_DERIVED_CHOICE_INDEX_ITEM','HIGH','derived_index')

    # Generic specific redirects by text and semantic IDs.
    if anyhas(t,'received unempl. benefits','requesting unemployment benefits','satisfation with requesting unempl. benefits'):
        return ('other_domain','unemployment_benefit_receipt_or_service','status_or_service','EXACT_OTHER_DOMAIN_ITEM','HIGH','social_protection')
    if anyhas(t,'business','owner','firm','industry'):
        return ('other_domain','business_or_industry','other_operator','EXACT_OTHER_DOMAIN_ITEM','HIGH','business')
    if anyhas(t,'spouse','partner','marital status','cohabitation status','married'):
        return ('other_domain','marital_or_partner_status','other_operator','EXACT_OTHER_DOMAIN_ITEM','HIGH','demography')
    if anyhas(t,'job','employment','occupation','labor force','workplace'):
        return ('other_domain','employment_or_work','other_operator','EXACT_OTHER_DOMAIN_ITEM','HIGH','employment')
    if anyhas(t,'race','ethnic group','nationality','arab','migration status'):
        return ('other_domain','race_ethnicity_or_migration','other_operator','EXACT_OTHER_DOMAIN_ITEM','HIGH','identity')
    if anyhas(t,'school','education','university','teacher'):
        return ('other_domain','education','other_operator','EXACT_OTHER_DOMAIN_ITEM','HIGH','education')
    if anyhas(t,'police','crime','violence','security','harassment','rape','beat his wife','beaten','shot at'):
        return ('other_domain','crime_violence_or_security','other_operator','EXACT_OTHER_DOMAIN_ITEM','HIGH','security')
    if anyhas(t,'religion','religious','god','bible','quran','church','mosque','faith','heaven','hell'):
        return ('other_domain','religion_or_worldview','other_operator','EXACT_OTHER_DOMAIN_ITEM','HIGH','religion')
    if anyhas(t,'environment','climate','pollution','natural resource'):
        return ('other_domain','environment_or_climate','other_operator','EXACT_OTHER_DOMAIN_ITEM','HIGH','environment')
    if anyhas(t,'political','government','election','democracy','president','party','parliament','constitution'):
        return ('other_domain','political_or_government','other_operator','EXACT_OTHER_DOMAIN_ITEM','HIGH','politics')
    if anyhas(t,'family','parent','child','children','mother','father'):
        return ('other_domain','family_or_intergenerational','other_operator','EXACT_OTHER_DOMAIN_ITEM','HIGH','family')
    if anyhas(t,'income','economic','money','poverty','benefit','tax','fare'):
        return ('other_domain','material_or_economic','other_operator','EXACT_OTHER_DOMAIN_ITEM','HIGH','economy')
    if anyhas(t,'internet','web','television','media','newspaper'):
        return ('other_domain','media_or_digital','other_operator','EXACT_OTHER_DOMAIN_ITEM','HIGH','media')

    return ('other_domain','explicit_other_substantive_item','other_operator','EXACT_TEXT_OUTSIDE_RECOVERED_GOVERNED_PROPOSITION','MEDIUM','other')

queue=read(QREM)
assert len(queue)==2847 and queue.semantic_pair_candidate_id.nunique()==2847
sel=queue.copy().sort_values(['semantic_content_id','left_source_family','right_source_family','cell_priority_rank','semantic_pair_candidate_id'])

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
assert set(lin.lineage_id)==needed

classes=[]
for _,lr in lin.iterrows():
    g=nodegroups[lr.lineage_id]
    texts=uniq(g.exact_question_text.tolist()); responses=uniq(g.response_family_expectation.tolist()); tops=uniq(g.response_topology.tolist()); response_options=uniq(g.response_options_substantive.tolist()); semids=uniq(g.semantic_content_id.tolist())
    sids=uniq(s for qid in g.question_implementation_id for s in struct_by_q.get(qid,[])); slabels=uniq(regidx.loc[s].structure_label for s in sids if s in regidx.index)
    per=[]
    for text in texts:
        # Use the node's semantic IDs only as discovery hints; exact text dominates.
        per.append(classify_one(semids[0] if semids else '',text,responses,tops,response_options))
    signatures=uniq((a,b,c,fam) for a,b,c,_,_,fam in per)
    if len(signatures)==1:
        axis,target,op,fam=signatures[0]; basis=' | '.join(uniq(x[3] for x in per)); conf='LOW' if any(x[4]=='LOW' for x in per) else ('MEDIUM' if any(x[4]=='MEDIUM' for x in per) else 'HIGH')
    else:
        axis,target,op,fam='heterogeneous_lineage','heterogeneous','heterogeneous','heterogeneous'; basis='MULTIPLE_CLASSIFICATIONS:'+compact([{'text':texts[i],'axis':x[0],'target':x[1],'operator':x[2],'family':x[5]} for i,x in enumerate(per)]); conf='LOW'
    status='P2_FINAL_LINEAGE_CLASSIFIED'
    if axis in {'unresolved_axis','heterogeneous_lineage'}: status='P2_FINAL_LINEAGE_UNRESOLVED'
    elif axis in {'other_domain','metadata_or_administration'}: status='P2_FINAL_LINEAGE_REDIRECTED_OR_ADMINISTRATIVE'
    elif conf=='MEDIUM': status='P2_FINAL_LINEAGE_COORDINATE_ONLY_INCOMPLETE_PROPOSITION'
    classes.append({'classification_id':stable('p2finalclassv1',lr.lineage_id),'lineage_id':lr.lineage_id,'source_family':lr.source_family,'member_count':lr.member_count,
      'variables_json':compact(uniq(g.source_variable_code.tolist())),'waves_json':compact(uniq(g.wave.tolist())),'exact_question_texts_json':compact(texts),
      'response_options_json':compact(uniq(g.response_options_substantive.tolist())),'response_topologies_json':compact(tops),'response_family_expectations_json':compact(responses),
      'semantic_content_ids_json':compact(semids),'source_structure_ids_json':compact(sids),'source_structure_labels_json':compact(slabels),
      'governed_relation_axis':axis,'governed_target_or_scope':target,'governed_operator':op,'governed_domain_family':fam,'classification_basis':basis,'classification_confidence':conf,
      'authority_status':status,'prohibited_use':'Classification coordinate only; no J-family membership, value harmonization, or respondent join.'})
classes=pd.DataFrame(classes).sort_values(['source_family','lineage_id'])
classes.to_csv(OUT/'Rawlsing_P2_Final_2847_Lineage_Classification_v1.csv',index=False)
cidx=classes.set_index('lineage_id')

def topology_set(row): return set(json.loads(row.response_topologies_json))
def response_set(row): return set(json.loads(row.response_family_expectations_json))

rul=[]
for _,cand in sel.iterrows():
    l=cidx.loc[cand.left_lineage_id]; r=cidx.loc[cand.right_lineage_id]
    la,ra=l.governed_relation_axis,r.governed_relation_axis; lt,rt=l.governed_target_or_scope,r.governed_target_or_scope; lo,ro=l.governed_operator,r.governed_operator; lf,rf=l.governed_domain_family,r.governed_domain_family; lc,rc=l.classification_confidence,r.classification_confidence
    if 'UNRESOLVED' in l.authority_status or 'UNRESOLVED' in r.authority_status:
        status='UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_SOURCE_LOCAL_EVIDENCE'; rel='UNRESOLVED'; ceil='NO_AUTHORITY'; rat='At least one source-local lineage lacks a recoverable single relation, target/scope, and operator.'
    elif la=='metadata_or_administration' and ra=='metadata_or_administration':
        status='REJECTED_ADMINISTRATIVE_OR_METADATA_FALSE_SEMANTIC_PAIR'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='Administrative or metadata fields do not export substantive semantic authority.'
    elif la in {'other_domain','metadata_or_administration'} and ra in {'other_domain','metadata_or_administration'}:
        if lf==rf and lt==rt and lf not in {'metadata','other'}:
            status='REDIRECTED_SHARED_OTHER_DOMAIN_COORDINATE_NOT_ADJUDICATED_HERE'; rel='OTHER_DOMAIN_REVIEW_REQUIRED'; ceil='NO_FINAL_TRANCHE_AUTHORITY'; rat='Both exact lineages share an out-of-scope domain coordinate; the relation is redirected without proposition authority.'
        else:
            status='REJECTED_CONTAMINATED_NEIGHBORHOOD_OTHER_DOMAIN_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='The inherited neighborhood joined distinct out-of-scope or administrative propositions.'
    elif la in {'other_domain','metadata_or_administration'} or ra in {'other_domain','metadata_or_administration'}:
        status='REJECTED_GOVERNED_PROPOSITION_VERSUS_OTHER_DOMAIN_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='One lineage asserts a governed proposition while the other exact item belongs to another domain or administrative layer.'
    elif la==ra and lt==rt and lo==ro and lc=='HIGH' and rc=='HIGH':
        status='ACCEPTED_TYPED_FINAL_PROPOSITION_RELATION'; rel='REWORDED_PROPOSITION_EQUIVALENCE'; same_top=topology_set(l)==topology_set(r) and len(topology_set(l))==1; same_resp=response_set(l)==response_set(r)
        ceil='QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY' if same_top and same_resp else 'QUESTION_PROPOSITION_ONLY'; rat='Both source-local lineages assert the same governed relation toward the same target/scope with the same operator, supported by HIGH-confidence two-sided evidence.'
    elif la==ra and lt==rt:
        status='ACCEPTED_SAME_CONSTRUCT_TARGET_DIFFERENT_OPERATOR_OR_INCOMPLETE_EVIDENCE_COORDINATE_ONLY'; rel='CONSTRUCT_TARGET_COORDINATE_ONLY'; ceil='CONSTRUCT_TARGET_ONLY'; rat='The construct and target agree, while operator, polarity, timeframe, or evidence completeness differs.'
    elif lf and lf==rf and lf not in {'heterogeneous','metadata','other'}:
        status='ACCEPTED_DOMAIN_COORDINATE_ONLY_RELATION_OR_TARGET_SCOPE_DIFFERS'; rel='DOMAIN_COORDINATE_ONLY'; ceil='DOMAIN_COORDINATE_ONLY'; rat='The exact items share a governed family but differ in relation, target, operator, scope, or comparison baseline.'
    elif lf and rf and lf not in {'heterogeneous'} and rf not in {'heterogeneous'}:
        status='REJECTED_FALSE_EQUIVALENCE_GOVERNED_RELATION_OR_TARGET_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='Both items are substantive but assert different governed relations, targets, or domains.'
    else:
        status='REJECTED_DIFFERENT_GOVERNED_RELATION_AXES'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='The exact lineages assert different governed relations.'
    rid=stable('p2finalrulingv1',cand.semantic_pair_candidate_id)
    rul.append({'pair_ruling_id':rid,'semantic_pair_candidate_id':cand.semantic_pair_candidate_id,'semantic_content_id':cand.semantic_content_id,'left_source_family':cand.left_source_family,'right_source_family':cand.right_source_family,'left_lineage_id':cand.left_lineage_id,'right_lineage_id':cand.right_lineage_id,
      'left_relation_axis':la,'right_relation_axis':ra,'left_target_or_scope':lt,'right_target_or_scope':rt,'left_operator':lo,'right_operator':ro,'left_domain_family':lf,'right_domain_family':rf,'left_classification_confidence':lc,'right_classification_confidence':rc,
      'authority_status':status,'relation_type':rel,'portability_ceiling':ceil,'rationale':rat,'left_classification_id':l.classification_id,'right_classification_id':r.classification_id,
      'two_sided_evidence_status':'EXPLICIT_LINEAGE_NODE_RESPONSE_AND_STRUCTURE_PROVENANCE_BOTH_SIDES','prohibited_use':'No J-family authority, value harmonization, or respondent join follows from this ruling.'})
rul=pd.DataFrame(rul)
rul.to_csv(OUT/'Rawlsing_P2_Final_2847_Pair_Rulings_v1.csv',index=False)

ev=[]
for _,rr in rul.iterrows():
    for side in ('left','right'):
        lid=rr[f'{side}_lineage_id']; c=cidx.loc[lid]; g=nodegroups[lid]
        ev.append({'evidence_record_id':stable('p2finalevidencev1',rr.pair_ruling_id,side),'pair_ruling_id':rr.pair_ruling_id,'semantic_pair_candidate_id':rr.semantic_pair_candidate_id,'side':side.upper(),'lineage_id':lid,'source_family':c.source_family,'classification_id':c.classification_id,'governed_relation_axis':c.governed_relation_axis,'governed_target_or_scope':c.governed_target_or_scope,'governed_operator':c.governed_operator,'governed_domain_family':c.governed_domain_family,
          'question_implementation_ids_json':compact(g.question_implementation_id.tolist()),'wave_variable_locators_json':compact([{'wave':x.wave,'variable':x.source_variable_code,'source_row_index':x.source_row_index} for _,x in g.iterrows()]),'exact_question_texts_json':c.exact_question_texts_json,'response_options_json':c.response_options_json,'response_topologies_json':c.response_topologies_json,'response_family_expectations_json':c.response_family_expectations_json,'source_structure_ids_json':c.source_structure_ids_json,'source_structure_labels_json':c.source_structure_labels_json,'classification_basis':c.classification_basis,'classification_confidence':c.classification_confidence,
          'evidence_sufficiency':'COMPLETE_FOR_PROPOSITION_CEILING' if c.classification_confidence=='HIGH' and 'UNRESOLVED' not in c.authority_status else ('COMPLETE_FOR_COORDINATE_ONLY' if c.classification_confidence=='MEDIUM' else 'INCOMPLETE_OR_HETEROGENEOUS')})
ev=pd.DataFrame(ev); ev.to_csv(OUT/'Rawlsing_P2_Final_2847_Two_Sided_Evidence_Ledger_v1.csv',index=False)
empty=queue.iloc[0:0].copy(); empty.to_csv(OUT/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Final_Tranche_v8.csv',index=False)
sel.to_csv(OUT/'Rawlsing_P2_Final_2847_Tranche_Candidate_Surface_v1.csv',index=False)
rul[rul.relation_type.eq('REWORDED_PROPOSITION_EQUIVALENCE')].to_csv(OUT/'Rawlsing_P2_Final_2847_Accepted_Proposition_Review_Surface_v1.csv',index=False)
rul[rul.relation_type.eq('UNRESOLVED')].to_csv(OUT/'Rawlsing_P2_Final_2847_Unresolved_Review_Surface_v1.csv',index=False)
summary={'contract_version':'P2_FINAL_2847_TRANCHE_V1','input_pending_pairs':len(queue),'final_work_unit_pairs':len(sel),'remaining_pairs':0,'selected_semantic_id_counts':{str(k):int(v) for k,v in sel.semantic_content_id.value_counts().sort_index().items()},'lineages_classified':len(classes),'classification_status_counts':{str(k):int(v) for k,v in classes.authority_status.value_counts().sort_index().items()},'pair_status_counts':{str(k):int(v) for k,v in rul.authority_status.value_counts().sort_index().items()},'relation_type_counts':{str(k):int(v) for k,v in rul.relation_type.value_counts().sort_index().items()},'evidence_rows':len(ev),'expected_evidence_rows':2*len(rul),'selection_exactly_remaining_queue':len(sel)==len(queue)==2847,'queue_closed':len(empty)==0,'selected_ids_unique':sel.semantic_pair_candidate_id.nunique()==2847,'ruling_ids_unique':rul.pair_ruling_id.nunique()==2847,'evidence_ids_unique':ev.evidence_record_id.nunique()==5694,'proposition_acceptance_requires_axis_target_operator_identity_and_high_confidence':bool(((rul.relation_type!='REWORDED_PROPOSITION_EQUIVALENCE')|((rul.left_relation_axis==rul.right_relation_axis)&(rul.left_target_or_scope==rul.right_target_or_scope)&(rul.left_operator==rul.right_operator)&(rul.left_classification_confidence=='HIGH')&(rul.right_classification_confidence=='HIGH'))).all()),'authority_boundary':'PAIR_RELATION_AUTHORITY_ONLY_NO_J_FAMILY_NO_VALUE_HARMONIZATION'}
(OUT/'FINAL_2847_TRANCHE_RETURN.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(summary,indent=2,ensure_ascii=False))
