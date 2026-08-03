#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, re
from collections import defaultdict
from pathlib import Path
import pandas as pd

ROOT=Path(os.environ.get('RAWLSING_V17_ROOT','/mnt/data/rawlsing_v17_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v17_20260731'))
OUT=Path(os.environ.get('RAWLSING_V18_OUT','/mnt/data/rawlsing_v18_outputs/material_economy_3000'))
OUT.mkdir(parents=True,exist_ok=True)
S32=ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'
QREM=Path(os.environ.get('RAWLSING_PENDING_QUEUE',str(ROOT/'38_P2_GLOBAL_MEDIA_CIVIC_FIXED_3000_TRANCHE5/Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Media_Civic_Fixed_3000_Tranche_v5.csv')))

FULL_IDS=[
 'ECON_COUNTRY_FUTURE','ECON_PERSONAL_NOW','ECON_COUNTRY_NOW','ECON_GAP_RICH_POOR','ECON_SATISFACTION_FINANCIAL',
 'ECON_GOVT_VS_INDIVIDUAL','WORK_SUCCESS_HARDWORK','ECON_INEQUALITY_ATTITUDE','ECON_ELITE_CAPTURE','ECON_PERSONAL_FUTURE',
 'INTERGENERATIONAL_COMPARE','INTERGENERATIONAL_FUTURE','LIVING_CONDITIONS','DEPRIVATION_FOOD','DEPRIVATION_MEDICINE',
 'DEPRIVATION_WATER','DEPRIVATION_CASH','WASTA_JOBS','IMMIGRANT_JOBS','WORK_IMPORTANCE','WORK_DUTY_SOCIETY',
 'materialSecurity::important_in_a_job_good_hours','materialSecurity::important_in_a_job_good_pay','materialSecurity::important_in_a_job_generous_holidays'
]
PARTIAL_ID='GENDER_JOBS_SCARCE'

LINEAGE_OVERRIDES={
 # Country economy source-local variants and bounded timeframe changes.
 'p2lineage_b019c858db0a8556705df940':('country_economic_condition_expectation','country_economy','future_2_to_5_year_change','SOURCE_LOCAL_VARIANTS_SPAN_2_TO_5_YEARS_COORDINATE_ONLY','MEDIUM'),
 'p2lineage_d95fc1952bb25eced01c36d6':('country_economic_condition_evaluation','country_economy','present_evaluation','SOURCE_NATIVE_CURRENT_COUNTRY_ECONOMY_VARIANTS','HIGH'),
 'p2lineage_8d8ba3122176e31424d11958':('country_economic_condition_evaluation','country_economy','present_evaluation','SOURCE_NATIVE_CURRENT_COUNTRY_ECONOMY_VARIANTS','HIGH'),
 'p2lineage_d856388f89aebbc651ece50c':('country_economic_condition_evaluation','country_economy','present_evaluation','EXPLICIT_PRESENT_COUNTRY_ECONOMY_ITEM','HIGH'),
 'p2lineage_bc8d94fab8d7bc4449f91830':('country_economic_condition_evaluation','country_economy','present_evaluation','EXPLICIT_PRESENT_COUNTRY_ECONOMY_ITEM','HIGH'),
 'p2lineage_d263f982cacdc302f45a8765':('country_economic_condition_expectation','country_economy','future_few_years_change','SOURCE_LOCAL_FIVE_OR_FEW_YEARS_VARIANT_COORDINATE_ONLY','MEDIUM'),
 'p2lineage_35d53915a72978009d151d1b':('country_economic_condition_expectation','country_economy','future_12_month_change','EXPLICIT_COUNTRY_ECONOMY_FUTURE_ITEM','HIGH'),
 'p2lineage_ac7725f47dacb3755fa3addc':('government_economy_management_performance','managing_national_economy','performance_rating','EXPLICIT_GOVERNMENT_ECONOMY_PERFORMANCE_CHILD','HIGH'),
 'p2lineage_b766a24a7cca542f1834f424':('country_economic_satisfaction','country_economy','present_satisfaction','EXPLICIT_NATIONAL_ECONOMY_SATISFACTION_ITEM','HIGH'),
 # Personal and household economy.
 'p2lineage_dddb209a62b6fb0bfb8e3f8f':('personal_economic_condition_evaluation','family_or_household_economy','present_evaluation','EXPLICIT_FAMILY_ECONOMY_ITEM','HIGH'),
 'p2lineage_bf769777d255092d78dc0dd6':('personal_economic_condition_evaluation','family_or_household_economy','present_evaluation','EXPLICIT_FAMILY_ECONOMY_ITEM','HIGH'),
 'p2lineage_b5134ab9662ff5401ec339ae':('personal_economic_condition_evaluation','personal_and_family_economy','present_evaluation','EXPLICIT_PERSONAL_AND_FAMILY_ECONOMY_ITEM','HIGH'),
 'p2lineage_bc57a58166506643c68de800':('personal_economic_condition_expectation','personal_and_family_economy','future_12_month_change','EXPLICIT_PERSONAL_AND_FAMILY_ECONOMY_FUTURE_ITEM','HIGH'),
 'p2lineage_903cd24268737baa1dc8f9c1':('personal_economic_condition_expectation','family_or_household_economy','future_few_years_change','SOURCE_LOCAL_FIVE_OR_FEW_YEARS_VARIANT_COORDINATE_ONLY','MEDIUM'),
 'p2lineage_5891e5d5cb0fd4be06a03abd':('personal_economic_condition_evaluation','personal_economy','present_evaluation','SOURCE_NATIVE_TERSE_PERSONAL_ECONOMY_ITEM','HIGH'),
 'p2lineage_47f9e1d41dab3dc78c8fff4c':('personal_economic_condition_expectation','personal_economy','future_unspecified_change','SOURCE_NATIVE_TERSE_PERSONAL_ECONOMY_ITEM','MEDIUM'),
 'p2lineage_c28b2f3dd9b06b002034ac74':('personal_economic_condition_evaluation','personal_economy','retrospective_unspecified_change','SOURCE_NATIVE_TERSE_PERSONAL_ECONOMY_ITEM','MEDIUM'),
 'p2lineage_25b3ee185c74ec7d228d5ca2':('personal_economic_condition_evaluation','family_or_household_economy','present_evaluation','SOURCE_NATIVE_TERSE_FAMILY_ECONOMY_ITEM','HIGH'),
 # Living standards and intergenerational mobility.
 'p2lineage_0f2b7fd9962ecfa4c3930924':('living_standard_change','own_or_household_living_conditions','retrospective_12_month_change','EXPLICIT_LIVING_CONDITIONS_RETROSPECTIVE_ITEM','HIGH'),
 'p2lineage_9c19a8a129e3ed355016b713':('living_standard_change','own_or_household_living_conditions','future_12_month_change','EXPLICIT_LIVING_CONDITIONS_FUTURE_ITEM','HIGH'),
 'p2lineage_4f521e40feb2bb78e9a1d5d4':('intergenerational_living_standard_comparison','respondent_vs_parents','comparison','EXPLICIT_INTERGENERATIONAL_COMPARISON_ITEM','HIGH'),
 'p2lineage_a10aa01cc187ea44b7a5b811':('intergenerational_living_standard_comparison','respondent_vs_parents','comparison','EXPLICIT_INTERGENERATIONAL_COMPARISON_ITEM','HIGH'),
 'p2lineage_b7518cce062b4eebb5be1b38':('intergenerational_living_standard_comparison','respondent_vs_parents','comparison','EXPLICIT_INTERGENERATIONAL_COMPARISON_ITEM','HIGH'),
 'p2lineage_943dfe01bb1d2cc7ac06d3e0':('intergenerational_opportunity_comparison','respondent_generation_vs_parents','standard_of_living_or_social_status_opportunity','EXPLICIT_INTERGENERATIONAL_OPPORTUNITY_ITEM','HIGH'),
 'p2lineage_6cab95aa2878f5ec257519c5':('intergenerational_future_outlook','respondent_children','future_comparison','EXPLICIT_CHILDREN_FUTURE_OUTLOOK_ITEM','HIGH'),
 'p2lineage_94ff17fa70f60b21da766cda':('intergenerational_future_outlook','next_generation','future_comparison','EXPLICIT_NEXT_GENERATION_OUTLOOK_ITEM','HIGH'),
 'p2lineage_b9f657d1bc53edf9d83433a9':('intergenerational_future_outlook','next_generation_country_prosperity','future_comparison','EXPLICIT_NEXT_GENERATION_COUNTRY_PROSPERITY_ITEM','HIGH'),
 # Inequality and distribution: preserve distinct relation axes.
 'p2lineage_f57929f1c73b0f3d084e90c8':('government_inequality_performance_evaluation','narrowing_rich_poor_gap','performance_rating','SOURCE_NATIVE_GOVERNMENT_PERFORMANCE_CHILD','HIGH'),
 'p2lineage_d2aed4864b0294e128461772':('rich_poor_gap_change','rich_poor_gap','retrospective_1_year_change','EXPLICIT_RICH_POOR_GAP_CHANGE_ITEM','HIGH'),
 'p2lineage_271c423238fe36c9d30ac88f':('income_distribution_fairness','national_income_distribution','fairness_rating','EXPLICIT_INCOME_DISTRIBUTION_FAIRNESS_ITEM','HIGH'),
 'p2lineage_b10221f585666a7b1ddefdb8':('subjective_income_position','income_ladder','self_placement','SOURCE_NATIVE_INCOME_LADDER_ITEM','HIGH'),
 'p2lineage_6f947aa22dc1d8d81d16091e':('democracy_feature_evaluation','state_income_equalization','essential_democracy_feature_rating','EXPLICIT_DEMOCRACY_FEATURE_ITEM','HIGH'),
 'p2lineage_42833ea9d285ff15d572f425':('private_vs_government_ownership','business_and_industry','ownership_position','SOURCE_NATIVE_OWNERSHIP_POSITION_VARIANTS','HIGH'),
 # Household-income adequacy/level are not satisfaction.
 'p2lineage_9056d6aff654f3d7026c863a':('household_income_adequacy','household_income','needs_coverage','EXPLICIT_HOUSEHOLD_INCOME_ADEQUACY_ITEM','HIGH'),
 'p2lineage_302a35c5ed8df0545586b692':('household_income_adequacy','household_income','income_situation_category','EXPLICIT_HOUSEHOLD_INCOME_SITUATION_ITEM','HIGH'),
 'p2lineage_577ceab2ecada0c87288c645':('household_income_adequacy','household_income','income_situation_category','SOURCE_NATIVE_HOUSEHOLD_INCOME_CATEGORY_ITEM','HIGH'),
 'p2lineage_17edd0c60e8542839c589d56':('household_income_level','household_income','threshold_comparison','EXPLICIT_HOUSEHOLD_INCOME_THRESHOLD_ITEM','HIGH'),
 # Labor competition and scarce-job priority.
 'p2lineage_dfe0636afbf9a4f25877d87e':('scarce_jobs_priority_attitude','men_over_women','agreement_or_position','EXPLICIT_SCARCE_JOBS_GENDER_PRIORITY_ITEM','HIGH'),
 'p2lineage_0a8ccba6feaa1a616b64d895':('scarce_jobs_priority_attitude','locals_over_nonlocals','agreement_or_position','EXPLICIT_SCARCE_JOBS_LOCAL_PRIORITY_ITEM','HIGH'),
 'p2lineage_9d65a8ec69ceb1c37dce38e3':('scarce_jobs_priority_attitude','locals_over_nonlocals','agreement_or_position','EXPLICIT_SCARCE_JOBS_LOCAL_PRIORITY_ITEM','HIGH'),
 'p2lineage_6351211e2601a95eae396316':('scarce_jobs_priority_attitude','nationals_over_foreigners','agreement_or_position','EXPLICIT_SCARCE_JOBS_NATIONAL_PRIORITY_ITEM','HIGH'),
 'p2lineage_c903881d974d6f854f0e5a70':('scarce_jobs_priority_attitude','nationals_over_foreigners','agreement_or_position','EXPLICIT_SCARCE_JOBS_NATIONAL_PRIORITY_ITEM','HIGH'),
 # Work social meaning: desired job attribute and current-job evaluation remain separate.
 'p2lineage_51c3bb6532299da4600d9a5f':('job_attribute_importance','social_usefulness','selected_as_important','SOURCE_NATIVE_DESIRED_JOB_ATTRIBUTE_CHILD','HIGH'),
 'p2lineage_5b29b6d5f24778595a5a5c3b':('current_job_social_usefulness','respondent_current_job','agreement_evaluation','EXPLICIT_CURRENT_JOB_USEFULNESS_ITEM','HIGH'),
}

def read(p): return pd.read_csv(p,dtype=str,keep_default_na=False)
def norm(x): return re.sub(r'\s+',' ',str(x or '').strip().casefold())
def stable(prefix,*parts): return prefix+'_'+hashlib.sha256(chr(31).join(map(str,parts)).encode()).hexdigest()[:24]
def compact(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def uniq(xs): return list(dict.fromkeys(x for x in xs if str(x).strip()))

def operator_time(t:str, default='general_evaluation'):
    t=norm(t)
    if re.search(r'(?:next|in) (?:twelve|12) months|12 months.? time',t): return 'future_12_month_change'
    if re.search(r'next few years \(3-5 years\)|3-5 years',t): return 'future_3_to_5_year_change'
    if re.search(r'next few years \(2-3 years\)|2-3 years',t): return 'future_2_to_3_year_change'
    if re.search(r'compared to (?:twelve|12) months ago|compared with (?:twelve|12) months ago|looking back',t): return 'retrospective_12_month_change'
    if re.search(r'past five years|last five years',t): return 'retrospective_5_year_change'
    if 'currently' in t or 'current ' in t or 'present ' in t or 'now' in t: return 'present_evaluation'
    return default

def classify_one(text:str, response_fams:list[str], topologies:list[str]):
    t=norm(text)
    # administrative / derived / obvious contamination first
    if not t or t in {'code none o','none of these','don\'t know','dont know'}:
        return ('unresolved_axis','unspecified','unresolved','MISSING_OR_FRAGMENTARY_EXACT_TEXT','LOW')
    if re.search(r'^(age|age_cond|country|region|weight|wave|respondent|interviewer|year of birth|survey year)|calibration weight|population size weight|digital object identifier',t):
        return ('other_domain','survey_metadata','metadata','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.search(r'index|derived|imputed|ratio|aggregate|scale score|welzel',t):
        # retain substantive index coordinates separately where obvious
        if 'womjob' in t or 'gender equality: job' in t:
            return ('derived_gender_job_priority_index','jobs_scarce_gender_priority','derived_index','EXPLICIT_DERIVED_INDEX','HIGH')
        return ('other_domain','derived_or_constructed_variable','derived_statistic','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')

    # Country economy: current, retrospective, future, satisfaction.
    if re.search(r'(?:current|present).*?(?:national |country.?s |your country|our country).*economic|economic (?:conditions|situation) in (?:this|your|our) country|state of the national economy|country.?s present economic situation',t):
        return ('country_economic_condition_evaluation','country_economy',operator_time(t,'present_evaluation'),'EXPLICIT_COUNTRY_ECONOMY_ITEM','HIGH')
    if re.search(r'looking back.*economic conditions in (?:this|the) country|economic conditions in (?:this|the) country compared to (?:twelve|12) months ago',t):
        return ('country_economic_condition_evaluation','country_economy','retrospective_12_month_change','EXPLICIT_COUNTRY_ECONOMY_RETROSPECTIVE_ITEM','HIGH')
    if re.search(r'economic (?:conditions|situation) in (?:this|your|our) country.*(?:twelve|12) months|economic situation in (?:this|your|our) country.*next few years|next (?:twelve|12) months.*economic situation of the country|economic situation of the country.*next (?:twelve|12) months',t):
        return ('country_economic_condition_expectation','country_economy',operator_time(t,'future_unspecified_change'),'EXPLICIT_COUNTRY_ECONOMY_FUTURE_ITEM','HIGH')
    if re.fullmatch(r'(?:current )?national economic conditions',t):
        return ('country_economic_condition_evaluation','country_economy','present_evaluation','SOURCE_NATIVE_TERSE_COUNTRY_ECONOMY_ITEM','HIGH')
    if re.search(r'how satisfied.*(?:state of the )?(?:national|country.?s) economy',t):
        return ('country_economic_satisfaction','country_economy','present_satisfaction','EXPLICIT_COUNTRY_ECONOMY_SATISFACTION_ITEM','HIGH')

    # Personal / household economy and finances.
    if re.fullmatch(r'current family economic conditions|personal current economic situation',t) or re.search(r'current (?:personal|family|household) economic',t):
        target='family_or_household_economy' if ('family' in t or 'household' in t) else 'personal_economy'
        return ('personal_economic_condition_evaluation',target,'present_evaluation','EXPLICIT_PERSONAL_OR_HOUSEHOLD_ECONOMY_ITEM','HIGH')
    if re.fullmatch(r'past personal economic situation',t) or re.search(r'(?:personal|family|household).*economic.*(?:compared to|than) (?:twelve|12) months ago|looking back.*(?:your|family|household).*economic',t):
        target='family_or_household_economy' if ('family' in t or 'household' in t) else 'personal_economy'
        return ('personal_economic_condition_evaluation',target,'retrospective_12_month_change','EXPLICIT_PERSONAL_ECONOMY_RETROSPECTIVE_ITEM','HIGH')
    if re.fullmatch(r'future personal economic situation',t) or re.search(r'(?:personal|family|household).*economic.*(?:next|future|twelve|12 months)|looking ahead.*(?:your|family|household).*economic',t):
        target='family_or_household_economy' if ('family' in t or 'household' in t) else 'personal_economy'
        return ('personal_economic_condition_expectation',target,operator_time(t,'future_unspecified_change'),'EXPLICIT_PERSONAL_ECONOMY_FUTURE_ITEM','HIGH')
    if re.search(r'satisfaction with (?:the )?financial situation of (?:your |the )?household|how satisfied.*(?:personal|family|household).*financial',t):
        return ('household_financial_satisfaction','household_finances','present_satisfaction','EXPLICIT_HOUSEHOLD_FINANCIAL_SATISFACTION_ITEM','HIGH')
    if re.search(r'(?:own|your) living conditions compared to (?:those of )?other|rate your living conditions compared',t):
        return ('living_standard_comparison','own_living_conditions','comparison_to_other_people','EXPLICIT_RELATIVE_LIVING_CONDITIONS_ITEM','HIGH')
    if re.search(r'present living standards better or worse than in the past|present hh.?s living conditions w.r.t. 1989|living conditions.*compared to.*past',t):
        op='comparison_to_1989' if '1989' in t else 'retrospective_unspecified_period'
        return ('living_standard_change','own_or_household_living_conditions',op,'EXPLICIT_LIVING_STANDARD_CHANGE_ITEM','HIGH')

    # Intergenerational mobility / future.
    if re.search(r'(?:living standard|quality of (?:your )?life).*compared (?:to|with).*parents|compared to my parent.?s generation.*standard of living|generation has more or fewer opportunities.*standard of living or social status',t):
        return ('intergenerational_living_standard_comparison','respondent_generation_vs_parents','comparison','EXPLICIT_INTERGENERATIONAL_COMPARISON_ITEM','HIGH')
    if re.search(r'quality of your children.?s lives.*better|children who are born now will have a better life|future for the next generation.*prosperous',t):
        target='respondent_children' if 'your children' in t else 'next_generation'
        return ('intergenerational_future_outlook',target,'future_comparison','EXPLICIT_NEXT_GENERATION_OUTLOOK_ITEM','HIGH')

    # Inequality / distribution / government responsibility.
    if re.search(r'incomes should be made more equal|differences in income.*larger|scale of incomes|state makes people.?s incomes equal',t):
        return ('income_equality_preference','income_distribution','equality_vs_incentives_position','EXPLICIT_INCOME_EQUALITY_ATTITUDE_ITEM','HIGH')
    if re.search(r'attitude towards reducing present income inequality|government.?s responsibility to reduce economic inequality',t):
        return ('inequality_reduction_support','income_inequality','support_or_responsibility_rating','EXPLICIT_INEQUALITY_REDUCTION_ITEM','HIGH')
    if re.search(r'change in the gap between rich and poor',t):
        return ('rich_poor_gap_change','rich_poor_gap','reported_change','EXPLICIT_RICH_POOR_GAP_CHANGE_ITEM','HIGH')
    if re.search(r'narrowing the gap between rich and poor',t):
        return ('government_performance_evaluation','narrowing_rich_poor_gap','performance_rating','EXPLICIT_GOVERNMENT_PERFORMANCE_ITEM','HIGH')
    if re.search(r'rich and poor people are treated equally by the government',t):
        return ('government_equal_treatment_evaluation','rich_and_poor_people','agreement_evaluation','EXPLICIT_EQUAL_TREATMENT_ITEM','HIGH')
    if re.search(r'gap between rich and poor|income inequality|differences between (?:the )?rich and (?:the )?poor',t):
        return ('rich_poor_gap_evaluation','rich_poor_gap','evaluation','EXPLICIT_RICH_POOR_GAP_ITEM','MEDIUM')
    if re.search(r'government should take more responsibility.*people should take more responsibility|government.*responsibility.*provided for|people.*responsibility.*provide for themselves',t):
        return ('government_vs_individual_responsibility','social_provision','government_vs_individual_position','EXPLICIT_GOVERNMENT_INDIVIDUAL_RESPONSIBILITY_ITEM','HIGH')
    if re.search(r'government ownership vs.? privatization|private vs.? government ownership|private ownership.*government ownership',t):
        return ('private_vs_government_ownership','business_and_industry','ownership_position','EXPLICIT_OWNERSHIP_POSITION_ITEM','HIGH')
    if re.search(r'economy.*(?:benefit|serve).*(?:few|rich|elite)|economic system.*(?:few|elite)|captured by.*elite',t):
        return ('economic_elite_capture_perception','national_economy','elite_capture_evaluation','EXPLICIT_ELITE_CAPTURE_ITEM','HIGH')

    # Material deprivation. Timeframe is kept explicit where supplied.
    if re.search(r'gone without (?:enough )?food|without enough food to eat',t):
        op='past_year_frequency' if 'past year' in t else 'deprivation_frequency_unspecified_period'
        return ('material_deprivation_frequency','food','%s'%op,'EXPLICIT_FOOD_DEPRIVATION_ITEM','HIGH')
    if re.search(r'cut down on basic food consumption',t):
        op='retrospective_2000_incidence' if '2000' in t else 'retrospective_incidence'
        return ('material_deprivation_incidence','food_consumption','%s'%op,'EXPLICIT_FOOD_CUTBACK_ITEM','HIGH')
    if re.search(r'buy food on credit',t):
        return ('material_deprivation_coping','food','credit_purchase_frequency_or_incidence','EXPLICIT_FOOD_CREDIT_COPING_ITEM','HIGH')
    if re.search(r'gone without (?:enough )?(?:clean )?water|without: enough clean water',t):
        op='past_year_frequency' if 'past year' in t else 'deprivation_frequency_unspecified_period'
        return ('material_deprivation_frequency','clean_water_for_home_use','%s'%op,'EXPLICIT_WATER_DEPRIVATION_ITEM','HIGH')
    if re.search(r'gone without (?:healthcare|health care)',t):
        op='past_year_frequency' if 'past year' in t else 'deprivation_frequency_unspecified_period'
        return ('material_deprivation_frequency','healthcare_access','%s'%op,'EXPLICIT_HEALTHCARE_DEPRIVATION_ITEM','HIGH')
    if re.search(r'gone without.*medicine|without: medicines or medical treatment|medicine or medical treatment that you needed',t):
        op='past_year_frequency' if 'past year' in t else 'deprivation_frequency_unspecified_period'
        return ('material_deprivation_frequency','medicine_or_medical_treatment','%s'%op,'EXPLICIT_MEDICAL_DEPRIVATION_ITEM','HIGH')
    if re.search(r'gone without (?:a )?cash income',t):
        op='deprivation_frequency_unspecified_period'
        return ('material_deprivation_frequency','cash_income',op,'EXPLICIT_CASH_INCOME_DEPRIVATION_ITEM','HIGH')

    # Wasta / connections / immigrant job competition.
    if re.search(r'wasta|piston',t):
        target='jobs' if 'job' in t else 'service_or_outcome_unspecified'
        return ('wasta_necessity_or_use','%s'%target,'frequency_or_necessity','EXPLICIT_WASTA_ITEM','HIGH' if target=='jobs' else 'MEDIUM')
    if re.search(r'influence of connections.*get a good job',t):
        target='government_job' if 'government' in t else ('private_sector_job' if 'private' in t else 'good_job_unspecified_sector')
        return ('connections_importance_for_job','%s'%target,'importance_rating','EXPLICIT_CONNECTIONS_FOR_JOB_ITEM','HIGH')
    if re.search(r'immigrants? (?:come to )?take (?:our )?jobs|immigrants? take jobs away|take away jobs from',t):
        return ('immigrant_job_displacement_attitude','immigrants_and_native_jobs','agreement_or_position','EXPLICIT_IMMIGRANT_JOB_DISPLACEMENT_ITEM','HIGH')
    if re.search(r'when jobs are scarce.*(?:men|nationals|citizens).*priority|jobs are scarce: giving men priority|men should have more right to a job than women',t):
        target='men_over_women' if ('men' in t or 'women' in t) else 'nationals_over_immigrants'
        return ('scarce_jobs_priority_attitude',target,'agreement_or_position','EXPLICIT_SCARCE_JOBS_PRIORITY_ITEM','HIGH')

    # Work success, centrality, attributes, social duty.
    if re.search(r'hard work.*better life|hard work.*doesn.?t.*success|luck and connections',t):
        return ('hard_work_success_belief','life_success','hard_work_vs_luck_connections_position','EXPLICIT_HARD_WORK_SUCCESS_ITEM','HIGH')
    if re.search(r'how important in your life: work',t) or (t=='work' and ('importance_scale' in response_fams)):
        return ('work_life_importance','work','importance_rating','EXPLICIT_WORK_LIFE_IMPORTANCE_ITEM','HIGH')
    if re.search(r'work most important in my life',t):
        return ('work_life_centrality','work','agreement_or_selection','EXPLICIT_WORK_CENTRALITY_ITEM','HIGH')
    if re.search(r'less importance placed on work',t):
        return ('future_work_importance_change','work_in_society','future_change_evaluation','EXPLICIT_FUTURE_WORK_IMPORTANCE_ITEM','HIGH')
    if re.search(r'work is a duty towards society',t):
        return ('work_social_duty_attitude','work','agreement_evaluation','EXPLICIT_WORK_DUTY_ITEM','HIGH')
    if re.search(r'job is useful to society|useful for society',t):
        return ('job_social_usefulness','current_or_desired_job','usefulness_or_importance','EXPLICIT_JOB_SOCIAL_USEFULNESS_ITEM','HIGH')
    if re.search(r'important in a job: good pay',t):
        return ('job_attribute_importance','good_pay','selected_as_important','EXPLICIT_JOB_ATTRIBUTE_CHILD','HIGH')
    if re.search(r'important in a job: good hours',t):
        return ('job_attribute_importance','good_hours','selected_as_important','EXPLICIT_JOB_ATTRIBUTE_CHILD','HIGH')
    if re.search(r'important in a job: generous holidays',t):
        return ('job_attribute_importance','generous_holidays','selected_as_important','EXPLICIT_JOB_ATTRIBUTE_CHILD','HIGH')
    if re.search(r'importance of .* in a job|important in a job:',t):
        # preserve attribute-specific target rather than collapse the battery
        target=re.sub(r'^.*?(?:importance of|important in a job:)\s*','',t).strip(' ?.:').replace(' ','_')[:80] or 'job_attribute_unspecified'
        return ('job_attribute_importance',target,'importance_rating_or_selection','EXPLICIT_JOB_ATTRIBUTE_ITEM','MEDIUM')

    # Contaminants with explicit other-domain coordinates.
    other_patterns=[
      ('gender_rights_or_roles',r'women and men|woman won.?t get a job|man won.?t get a job|better for man to work|mother working|gender equality|women have the same rights'),
      ('environment_or_climate',r'climate change|pollution|environment|save water'),
      ('corruption_or_bribery',r'corruption|bribery|unofficial payments|payments/gifts'),
      ('public_service_access_or_satisfaction',r'trash collection|accessing healthcare|satisfaction with receiving.*medical|school feeding program'),
      ('social_support_network',r'do you know anyone whom you could ask|friends and connections'),
      ('job_characteristic_or_employment',r'weekly work hours|hours.*work|employment contract|skills.*needed for job|experience needed for the job|job allows|job interferes|family life interfere job|exploited in your job'),
      ('religion_or_religiosity',r'religio|god|prayer|church|mosque|sharia'),
      ('family_or_parenting',r'parents|children|family|married|divorc|spouse'),
      ('health_or_treatment',r'hospital|medical treatment|medicine:version|poor physical health'),
      ('media_or_internet_use',r'use .*site|web|internet|television|radio|news site'),
      ('housing_or_assets',r'ownership of|own any|dwelling|deed|windows|heating|telephone access|electricity'),
      ('security_or_police',r'police|crime|force.*criminal|protest'),
      ('education_or_science',r'education|school|college|science|technology'),
      ('civic_or_political',r'democracy|government.*law|political|protest|voluntary work|citizens'),
      ('personal_psychology_or_wellbeing',r'happy|satisfaction with life|successful|proud|ashamed|control over life'),
    ]
    for target,pat in other_patterns:
        if re.search(pat,t): return ('other_domain',target,'other_operator','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    return ('other_domain','explicit_other_substantive_item','other_operator','EXACT_TEXT_OUTSIDE_SELECTED_MATERIAL_ECONOMY_DOMAINS','MEDIUM')

queue=read(QREM)
selection_path=os.environ.get('RAWLSING_FIXED_3000_SELECTION','').strip()
if selection_path:
    sel=read(Path(selection_path))
else:
    sel=queue[queue.semantic_content_id.isin(FULL_IDS)].copy()
    need=3000-len(sel)
    assert need==109,need
    partial=(queue[queue.semantic_content_id.eq(PARTIAL_ID)]
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
    texts=uniq(g.exact_question_text.tolist()); responses=uniq(g.response_family_expectation.tolist()); tops=uniq(g.response_topology.tolist())
    sids=uniq(s for qid in g.question_implementation_id for s in struct_by_q.get(qid,[])); slabels=uniq(regidx.loc[s].structure_label for s in sids if s in regidx.index)
    if lr.lineage_id in LINEAGE_OVERRIDES:
        axis,target,op,basis,conf=LINEAGE_OVERRIDES[lr.lineage_id]
        per=[(axis,target,op,basis,conf)]
        signatures=[(axis,target,op)]
    else:
        per=[classify_one(t,responses,tops) for t in texts]
        signatures=uniq((a,b,c) for a,b,c,_,_ in per)
    if len(signatures)==1:
        axis,target,op=signatures[0]; basis=' | '.join(uniq(x[3] for x in per)); conf='LOW' if any(x[4]=='LOW' for x in per) else ('MEDIUM' if any(x[4]=='MEDIUM' for x in per) else 'HIGH')
    else:
        # A lineage cannot export authority if its exact members assert different material propositions.
        axis,target,op='heterogeneous_lineage','heterogeneous','heterogeneous'
        basis='MULTIPLE_MATERIAL_CLASSIFICATIONS:'+compact([{'text':texts[i],'axis':x[0],'target':x[1],'operator':x[2]} for i,x in enumerate(per)]); conf='LOW'
    status='P2_MATERIAL_ECONOMY_LINEAGE_CLASSIFIED'
    if axis in {'unresolved_axis','heterogeneous_lineage'}: status='P2_MATERIAL_ECONOMY_LINEAGE_UNRESOLVED'
    elif axis=='other_domain': status='P2_OUT_OF_DOMAIN_LINEAGE_REDIRECTED'
    elif conf=='MEDIUM': status='P2_MATERIAL_ECONOMY_LINEAGE_COORDINATE_ONLY_INCOMPLETE_PROPOSITION'
    classes.append({
      'classification_id':stable('p2materialeconclassv1',lr.lineage_id),'lineage_id':lr.lineage_id,'source_family':lr.source_family,'member_count':lr.member_count,
      'variables_json':compact(uniq(g.source_variable_code.tolist())),'waves_json':compact(uniq(g.wave.tolist())),'exact_question_texts_json':compact(texts),
      'response_options_json':compact(uniq(g.response_options_substantive.tolist())),'response_topologies_json':compact(tops),'response_family_expectations_json':compact(responses),
      'semantic_content_ids_json':compact(uniq(g.semantic_content_id.tolist())),'source_structure_ids_json':compact(sids),'source_structure_labels_json':compact(slabels),
      'governed_relation_axis':axis,'governed_target_or_scope':target,'governed_operator':op,'classification_basis':basis,'classification_confidence':conf,
      'authority_status':status,'prohibited_use':'Classification coordinate only; no J-family membership, value harmonization, or respondent join.'
    })
classes=pd.DataFrame(classes).sort_values(['source_family','lineage_id'])
classes.to_csv(OUT/'Rawlsing_P2_Material_Economy_Lineage_Classification_v1.csv',index=False)
cidx=classes.set_index('lineage_id')

DOMAIN_FAMILY={
 'country_economic_condition_evaluation':'country_economic_outlook','country_economic_condition_expectation':'country_economic_outlook','country_economic_satisfaction':'country_economic_outlook',
 'personal_economic_condition_evaluation':'personal_economic_outlook','personal_economic_condition_expectation':'personal_economic_outlook','household_financial_satisfaction':'personal_economic_outlook',
 'living_standard_comparison':'living_standards','living_standard_change':'living_standards','intergenerational_living_standard_comparison':'intergenerational_mobility','intergenerational_opportunity_comparison':'intergenerational_mobility','intergenerational_future_outlook':'intergenerational_mobility',
 'income_equality_preference':'economic_inequality','income_distribution_fairness':'economic_inequality','subjective_income_position':'income_position','democracy_feature_evaluation':'democracy_feature','inequality_reduction_support':'economic_inequality','rich_poor_gap_change':'economic_inequality','government_inequality_performance_evaluation':'economic_inequality','government_equal_treatment_evaluation':'economic_inequality','rich_poor_gap_evaluation':'economic_inequality','economic_elite_capture_perception':'economic_inequality',
 'government_vs_individual_responsibility':'economic_governance','private_vs_government_ownership':'economic_governance','government_economy_management_performance':'economic_governance',
 'material_deprivation_frequency':'material_deprivation','material_deprivation_incidence':'material_deprivation','material_deprivation_coping':'material_deprivation',
 'wasta_necessity_or_use':'labor_access_connections','connections_importance_for_job':'labor_access_connections','immigrant_job_displacement_attitude':'labor_competition','scarce_jobs_priority_attitude':'labor_competition','derived_gender_job_priority_index':'labor_competition',
 'household_income_adequacy':'household_finance','household_income_level':'household_finance','hard_work_success_belief':'work_success_ideology','work_life_importance':'work_centrality','work_life_centrality':'work_centrality','future_work_importance_change':'work_centrality','work_social_duty_attitude':'work_social_meaning','job_social_usefulness':'work_social_meaning','current_job_social_usefulness':'work_social_meaning','job_attribute_importance':'job_attributes'
}
def topology_set(row): return set(json.loads(row.response_topologies_json))
def response_set(row): return set(json.loads(row.response_family_expectations_json))
def family(axis): return DOMAIN_FAMILY.get(axis,'')

rul=[]
for _,cand in sel.iterrows():
    l=cidx.loc[cand.left_lineage_id]; r=cidx.loc[cand.right_lineage_id]
    la,ra=l.governed_relation_axis,r.governed_relation_axis; lt,rt=l.governed_target_or_scope,r.governed_target_or_scope; lo,ro=l.governed_operator,r.governed_operator
    lc,rc=l.classification_confidence,r.classification_confidence
    if 'UNRESOLVED' in l.authority_status or 'UNRESOLVED' in r.authority_status:
        status='UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_SOURCE_LOCAL_EVIDENCE'; rel='UNRESOLVED'; ceil='NO_AUTHORITY'; rat='At least one source-local lineage lacks one exportable relation, target/scope, and operator.'
    elif la=='other_domain' and ra=='other_domain':
        if lt==rt and lt not in {'survey_metadata','derived_or_constructed_variable','explicit_other_substantive_item'}:
            status='REDIRECTED_OUT_OF_MATERIAL_ECONOMY_DOMAIN_SHARED_OTHER_AXIS_NOT_ADJUDICATED'; rel='OTHER_DOMAIN_REVIEW_REQUIRED'; ceil='NO_MATERIAL_ECONOMY_AUTHORITY'; rat='Both exact lineages belong to the same other-domain coordinate, but this tranche does not manufacture authority for that domain.'
        else:
            status='REJECTED_CONTAMINATED_NEIGHBORHOOD_OTHER_DOMAIN_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='Both items are outside the governed material-economy surface and do not share a governed substantive coordinate.'
    elif la=='other_domain' or ra=='other_domain':
        status='REJECTED_MATERIAL_ECONOMY_VERSUS_OTHER_DOMAIN_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='One lineage asserts a material-economy proposition while the other exact item belongs to another domain.'
    elif la==ra and lt==rt and lo==ro and lc=='HIGH' and rc=='HIGH':
        status='ACCEPTED_TYPED_MATERIAL_ECONOMY_PROPOSITION_RELATION'; rel='REWORDED_PROPOSITION_EQUIVALENCE'
        same_top=topology_set(l)==topology_set(r) and len(topology_set(l))==1; same_resp=response_set(l)==response_set(r)
        ceil='QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY' if same_top and same_resp else 'QUESTION_PROPOSITION_ONLY'
        rat='Both source-local lineages assert the same governed relation toward the same target/scope with the same operator; both classifications are HIGH-confidence.'
    elif la==ra and lt==rt:
        status='ACCEPTED_SAME_CONSTRUCT_TARGET_DIFFERENT_OPERATOR_OR_INCOMPLETE_EVIDENCE_COORDINATE_ONLY'; rel='CONSTRUCT_TARGET_COORDINATE_ONLY'; ceil='CONSTRUCT_TARGET_ONLY'; rat='The construct and target/scope agree, but the operators differ or at least one source record cannot support proposition-level export.'
    elif family(la) and family(la)==family(ra):
        status='ACCEPTED_DOMAIN_COORDINATE_ONLY_RELATION_OR_TARGET_SCOPE_DIFFERS'; rel='DOMAIN_COORDINATE_ONLY'; ceil='DOMAIN_COORDINATE_ONLY'; rat='The items share a governed domain family but differ in relation, target, sector, timeframe, comparison baseline, or operator.'
    elif family(la) and family(ra):
        status='REJECTED_FALSE_EQUIVALENCE_MATERIAL_ECONOMY_RELATION_OR_TARGET_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='Both items are on the broad material-economy surface but assert materially different relations or targets.'
    else:
        status='REJECTED_DIFFERENT_GOVERNED_RELATION_AXES'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='The exact lineages assert different governed relations.'
    rid=stable('p2materialeconrulingv1',cand.semantic_pair_candidate_id)
    rul.append({'pair_ruling_id':rid,'semantic_pair_candidate_id':cand.semantic_pair_candidate_id,'semantic_content_id':cand.semantic_content_id,'left_source_family':cand.left_source_family,'right_source_family':cand.right_source_family,'left_lineage_id':cand.left_lineage_id,'right_lineage_id':cand.right_lineage_id,
      'left_relation_axis':la,'right_relation_axis':ra,'left_target_or_scope':lt,'right_target_or_scope':rt,'left_operator':lo,'right_operator':ro,'left_classification_confidence':lc,'right_classification_confidence':rc,
      'authority_status':status,'relation_type':rel,'portability_ceiling':ceil,'rationale':rat,'left_classification_id':l.classification_id,'right_classification_id':r.classification_id,
      'two_sided_evidence_status':'EXPLICIT_LINEAGE_NODE_RESPONSE_AND_STRUCTURE_PROVENANCE_BOTH_SIDES','prohibited_use':'No J-family authority, value harmonization, or respondent join follows from this ruling.'})
rul=pd.DataFrame(rul)
rul.to_csv(OUT/'Rawlsing_P2_Material_Economy_3000_Pair_Rulings_v1.csv',index=False)

ev=[]
for _,rr in rul.iterrows():
    for side in ('left','right'):
        lid=rr[f'{side}_lineage_id']; c=cidx.loc[lid]; g=nodegroups[lid]
        ev.append({'evidence_record_id':stable('p2materialeconevidencev1',rr.pair_ruling_id,side),'pair_ruling_id':rr.pair_ruling_id,'semantic_pair_candidate_id':rr.semantic_pair_candidate_id,'side':side.upper(),
          'lineage_id':lid,'source_family':c.source_family,'classification_id':c.classification_id,'governed_relation_axis':c.governed_relation_axis,'governed_target_or_scope':c.governed_target_or_scope,'governed_operator':c.governed_operator,
          'question_implementation_ids_json':compact(g.question_implementation_id.tolist()),'wave_variable_locators_json':compact([{'wave':x.wave,'variable':x.source_variable_code,'source_row_index':x.source_row_index} for _,x in g.iterrows()]),
          'exact_question_texts_json':c.exact_question_texts_json,'response_options_json':c.response_options_json,'response_topologies_json':c.response_topologies_json,'response_family_expectations_json':c.response_family_expectations_json,
          'source_structure_ids_json':c.source_structure_ids_json,'source_structure_labels_json':c.source_structure_labels_json,'classification_basis':c.classification_basis,'classification_confidence':c.classification_confidence,
          'evidence_sufficiency':'COMPLETE_FOR_PROPOSITION_CEILING' if c.classification_confidence=='HIGH' and 'UNRESOLVED' not in c.authority_status else ('COMPLETE_FOR_COORDINATE_ONLY' if c.classification_confidence=='MEDIUM' else 'INCOMPLETE_OR_HETEROGENEOUS')})
ev=pd.DataFrame(ev)
ev.to_csv(OUT/'Rawlsing_P2_Material_Economy_3000_Two_Sided_Evidence_Ledger_v1.csv',index=False)

remaining=queue[~queue.semantic_pair_candidate_id.isin(set(sel.semantic_pair_candidate_id))].copy()
remaining.to_csv(OUT/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Material_Economy_Fixed_3000_Tranche_v6.csv',index=False)
sel.to_csv(OUT/'Rawlsing_P2_Material_Economy_Fixed_3000_Tranche_Candidate_Surface_v1.csv',index=False)

accepted=rul[rul.authority_status.eq('ACCEPTED_TYPED_MATERIAL_ECONOMY_PROPOSITION_RELATION')].copy()
accepted.to_csv(OUT/'Rawlsing_P2_Material_Economy_Accepted_Proposition_Review_Surface_v1.csv',index=False)
unres=rul[rul.relation_type.eq('UNRESOLVED')].copy(); unres.to_csv(OUT/'Rawlsing_P2_Material_Economy_Unresolved_Review_Surface_v1.csv',index=False)

summary={'contract_version':'P2_FIXED_3000_MATERIAL_ECONOMY_TRANCHE_V1','input_pending_pairs':len(queue),'fixed_work_unit_pairs':len(sel),'remaining_pairs':len(remaining),
 'selected_semantic_id_counts':{str(k):int(v) for k,v in sel.semantic_content_id.value_counts().sort_index().items()},'lineages_classified':len(classes),
 'classification_status_counts':{str(k):int(v) for k,v in classes.authority_status.value_counts().sort_index().items()},'pair_status_counts':{str(k):int(v) for k,v in rul.authority_status.value_counts().sort_index().items()},
 'relation_type_counts':{str(k):int(v) for k,v in rul.relation_type.value_counts().sort_index().items()},'evidence_rows':len(ev),'expected_evidence_rows':2*len(rul),
 'selection_exactly_3000':len(sel)==3000,'queue_partition_exact':len(sel)+len(remaining)==len(queue),'selected_ids_unique':sel.semantic_pair_candidate_id.nunique()==3000,
 'ruling_ids_unique':rul.pair_ruling_id.nunique()==3000,'evidence_ids_unique':ev.evidence_record_id.nunique()==6000,
 'proposition_acceptance_requires_axis_target_operator_identity_and_high_confidence':bool(((rul.authority_status!='ACCEPTED_TYPED_MATERIAL_ECONOMY_PROPOSITION_RELATION')|((rul.left_relation_axis==rul.right_relation_axis)&(rul.left_target_or_scope==rul.right_target_or_scope)&(rul.left_operator==rul.right_operator)&(rul.left_classification_confidence=='HIGH')&(rul.right_classification_confidence=='HIGH'))).all()),
 'authority_boundary':'PAIR_RELATION_AUTHORITY_ONLY_NO_J_FAMILY_NO_VALUE_HARMONIZATION'}
(OUT/'FIXED_3000_MATERIAL_ECONOMY_TRANCHE_RETURN.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(summary,indent=2,ensure_ascii=False))
