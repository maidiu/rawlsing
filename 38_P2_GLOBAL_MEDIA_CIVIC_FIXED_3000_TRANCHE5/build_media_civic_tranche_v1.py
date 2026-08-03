#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, re
from collections import defaultdict
from pathlib import Path
import pandas as pd

ROOT=Path(os.environ.get('RAWLSING_V16_ROOT','/mnt/data/rawlsing_v17_extract/Rawlsing_J_Family_Authority_Strategy_Handoff_v16_20260731'))
OUT=Path(os.environ.get('RAWLSING_V17_OUT','/mnt/data/rawlsing_v17_outputs/media_civic_3000'))
OUT.mkdir(parents=True,exist_ok=True)
S32=ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'
QREM=Path(os.environ.get('RAWLSING_PENDING_QUEUE',str(ROOT/'37_P2_GLOBAL_DEMOCRACY_ELECTORAL_FIXED_3000_TRANCHE4/Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Fixed_3000_Tranche_v4.csv')))


def read(p): return pd.read_csv(p,dtype=str,keep_default_na=False)
def norm(x): return re.sub(r'\s+',' ',str(x or '').strip().casefold())
def stable(prefix,*parts): return prefix+'_'+hashlib.sha256(chr(31).join(map(str,parts)).encode()).hexdigest()[:24]
def compact(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def uniq(xs): return list(dict.fromkeys(x for x in xs if str(x).strip()))

def medium_target(t:str):
    t=norm(t)
    if 'television or radio' in t or 'radio or tv' in t or 'tv or radio' in t: return 'radio_or_television'
    if 'television' in t or re.search(r'\btv\b',t): return 'television'
    if 'radio' in t or 'podcast' in t: return 'radio_or_podcast' if 'podcast' in t else 'radio'
    if 'newspaper' in t or 'news paper' in t or 'daily papers' in t: return 'newspaper'
    if 'internet' in t or re.search(r'\bweb\b',t): return 'internet'
    if 'social media' in t: return 'social_media'
    if 'friends or colleagues' in t or 'talk with friends' in t: return 'interpersonal_contacts'
    return 'media_unspecified'

def internet_purpose(t:str):
    t=norm(t)
    if 'express your opinion about political' in t: return 'political_opinion_expression'
    if 'find information about politics' in t: return 'political_information_search'
    if 'for communication' in t or 'electronic mail/messaging' in t: return 'communication_or_messaging'
    if 'for search' in t or 'search information' in t: return 'information_search'
    if 'financial transaction' in t: return 'financial_transactions'
    if 'do shopping' in t: return 'shopping'
    if 'entertainment' in t: return 'entertainment'
    if re.search(r'\bwork\b',t): return 'work'
    if 'to do steps' in t: return 'administrative_tasks'
    if 'chatroom' in t: return 'chatroom_use'
    if 'email' in t: return 'email_use'
    return 'general_internet_use'

# Lineage-specific rulings are limited to source-native evidence that cannot be reconstructed from child text alone.
OVERRIDES={
    # WVS Q202-Q209 media-frequency battery; response contract and governing structure recover the terse targets.
    'p2lineage_854a85ab4fd9b9b48cdf0549':('news_medium_use_frequency','television_news','frequency','SOURCE_NATIVE_MEDIA_FREQUENCY_BATTERY_MEMBER','HIGH'),
    'p2lineage_d3070de14bd823f5cedd47e4':('news_medium_use_frequency','radio_news','frequency','SOURCE_NATIVE_MEDIA_FREQUENCY_BATTERY_MEMBER','HIGH'),
    'p2lineage_bcdcbb99fea51a2302640b3c':('internet_use_frequency','internet_general','frequency','SOURCE_NATIVE_MEDIA_FREQUENCY_BATTERY_MEMBER','HIGH'),
    # WVS values battery: terse Politics child is importance of politics in life, not interest in politics.
    'p2lineage_f71bb0718e5d0dfa56e1ae24':('politics_life_importance','politics','importance_rating','SOURCE_NATIVE_VALUES_BATTERY_RESPONSE_CONTRACT','HIGH'),
    # LiTS q810ce has a missing child label in delivered exact authority. Diagnostic codebook says Internet, but proposition authority stays incomplete.
    'p2lineage_b99220f731bab2b3bf1d1a1e':('internet_use_frequency','internet_general','frequency','INCOMPLETE_EXACT_CHILD_TEXT_DIAGNOSTIC_CODEBOOK_AND_PARENT_GROUP_ONLY','MEDIUM'),
    # Asian W1 q022 has no recoverable participation target and must not inherit CIVIC_DISCUSS_POLITICS from the semantic queue.
    'p2lineage_78193a6f13f138c9728f81d8':('unresolved_axis','participation_target_unspecified','frequency','TERSE_PARTICIPATION_ITEM_WITHOUT_RECOVERABLE_PARENT_TARGET','LOW'),
    # WVS party/aggregate metadata in a contaminated discussion neighborhood.
    'p2lineage_12fc1dcd08d0c749bb458fc0':('other_domain','party_aggregate_position','derived_statistic','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_a9aa053bcd8657e777b99a74':('other_domain','party_aggregate_mistrust','derived_statistic','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_b2f0a87c0cd84674cef1ee9e':('other_domain','party_values_typology','derived_typology','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_b3ac227f67e5947f2ead79b0':('other_domain','party_populism_position','derived_scale','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_e38d92bd51cfa05df50f98dc':('other_domain','party_economic_position','derived_scale','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_eadd16897bb8cb80a89a9694':('other_domain','country_region_identifier','metadata','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    # LiTS refusal fragment has no substantive informant proposition.
    'p2lineage_cbf5c14369702fb45d5010bf':('other_domain','survey_special_response_fragment','metadata_fragment','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    # Terse source-native battery children recovered from response contracts and structures.
    'p2lineage_4af70b143e10923ae7bc0a9d':('news_medium_use_frequency','newspaper_news','frequency','SOURCE_NATIVE_MEDIA_FREQUENCY_ITEM_RESPONSE_CONTRACT','HIGH'),
    'p2lineage_860e51e2a12fad0b2b655eb3':('other_domain','trust_in_television','trust_rating','SOURCE_NATIVE_TRUST_BATTERY_RESPONSE_CONTRACT','HIGH'),
    'p2lineage_e03c0c22c3dd49553af9ff6e':('general_media_use_duration','radio_general','duration','SOURCE_NATIVE_MEDIA_USE_DURATION_BATTERY','HIGH'),
    'p2lineage_f6e28439e9fe19023e1a90c9':('general_media_use_duration','television_general','duration','SOURCE_NATIVE_MEDIA_USE_DURATION_BATTERY','HIGH'),
    'p2lineage_01c0a2f7066da98da198d51b':('political_contact','news_media','retrospective_contact_frequency_or_status','SOURCE_NATIVE_CONTACT_BATTERY_CHILD','HIGH'),
    'p2lineage_3bcd74d48ab66ddc7b51b926':('political_contact','news_media','retrospective_contact_frequency_or_status','SOURCE_NATIVE_CONTACT_BATTERY_CHILD','HIGH'),
    'p2lineage_6983513430339bb8ce374c35':('media_device_ownership','radio_receiver','ownership_or_availability','SOURCE_NATIVE_HOUSEHOLD_ASSET_BATTERY_CHILD','HIGH'),
    'p2lineage_e1cb4755fa67f2a02a151fea':('media_service_access','cable_television','access_or_ownership','SOURCE_NATIVE_HOUSEHOLD_ASSET_BATTERY_CHILD','HIGH'),
    'p2lineage_24b846c2bb6861bb68406d15':('internet_access','webtv_internet','access_or_availability','EXPLICIT_WEBTV_INTERNET_ACCESS_ITEM','HIGH'),
    'p2lineage_ae4a7467d14b22efe6474236':('news_medium_use_frequency','radio_or_television_in_depth_reports','frequency','SOURCE_NATIVE_MEDIA_FREQUENCY_BATTERY_CHILD','HIGH'),
    'p2lineage_2a54041d5d82a7100bd92d40':('information_source_use_frequency','interpersonal_contacts','frequency','SOURCE_NATIVE_INFORMATION_SOURCE_FREQUENCY_CHILD','HIGH'),
    'p2lineage_5581e967f47edc0a2adf6f14':('other_domain','public_transport_stop_distance','distance','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_514d0984fad5458428849108':('other_domain','neighborhood_people_concern','concern_rating','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_693388d4e197aef26ca5f10e':('other_domain','party_vote_choice','party_selection','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_eb4f5f84bfa3e9ba947af1b7':('other_domain','college_composition_ratio','derived_category','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_0f50d43f78d039af81f52b85':('other_domain','weekly_work_hours','duration','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_13283c6ce9d6d47aeff0f87d':('other_domain','crisis_work_hours_reduction_household_head','impact_indicator','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_638365a5b67b02d5832b0ad8':('other_domain','crisis_work_hours_reduction_other_household_member','impact_indicator','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_184e996c229f51f2136772f9':('other_domain','double_glazed_windows','housing_attribute','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_23622ce161f04607ce59abdd':('other_domain','employment_contract_type','contract_classification','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_6c4d18192bb4f1567ee81cce':('other_domain','mother_occupation_sector','occupation_classification','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_8d70505c531f81933b56ae47':('other_domain','father_occupation_sector','occupation_classification','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_8bd5b10a2957262f2b62aba1':('other_domain','survey_refusal_reason','paradata_reason','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_c15414c12ad35d16a100e1bf':('other_domain','fixed_telephone_access','access','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_d986b5d7011e0ab595771438':('other_domain','central_heating_access','access','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH'),
    'p2lineage_2a3adcc60effbdaf48644913':('news_medium_use_frequency','television_news','frequency','EXPLICIT_NEWS_MEDIUM_FREQUENCY_ITEM','HIGH'),
    'p2lineage_61defd60af0212d874f00c9e':('news_medium_use_frequency','television_news','frequency','EXPLICIT_NEWS_MEDIUM_FREQUENCY_ITEM','HIGH'),
    'p2lineage_7852438f318a8487926fe185':('news_medium_use_frequency','newspaper_news','ordinary_week_frequency','EXPLICIT_ORDINARY_WEEK_NEWS_MEDIUM_ITEM','HIGH'),
    'p2lineage_2a3adcc60effbdaf48644913':('news_medium_use_frequency','television_news','ordinary_week_frequency','EXPLICIT_ORDINARY_WEEK_NEWS_MEDIUM_ITEM','HIGH'),
    'p2lineage_2efdbdff991f448eed8b956a':('news_medium_use_frequency','radio_news','ordinary_week_frequency','EXPLICIT_ORDINARY_WEEK_NEWS_MEDIUM_ITEM','HIGH'),
    'p2lineage_6d0b6f5e2cc0692ff727f0da':('internet_access_frequency','home_internet','frequency','EXPLICIT_HOME_INTERNET_ACCESS_FREQUENCY_ITEM','HIGH'),
    'p2lineage_302e35ca68490e15812f98c9':('internet_access','home_broadband_internet','access_or_availability','EXPLICIT_HOME_BROADBAND_ACCESS_ITEM','HIGH'),
    'p2lineage_ccf97616b2b11c178d262ef4':('internet_mobile_use','mobile_device_internet','use_incidence','EXPLICIT_MOBILE_INTERNET_USE_ITEM','HIGH'),
    'p2lineage_37582e3a41a5aba0a10d3b0a':('general_television_use_duration','television_general_daily','duration_per_day','EXPLICIT_DAILY_TELEVISION_DURATION_ITEM','HIGH'),
    'p2lineage_022edf37e583913f1443b775':('general_television_use_duration','television_general_unspecified_period','duration_unspecified_period','INCOMPLETE_TIMEFRAME_TELEVISION_DURATION_ITEM','MEDIUM'),
    'p2lineage_e03c0c22c3dd49553af9ff6e':('general_media_use_duration','radio_general_unspecified_period','duration_unspecified_period','SOURCE_NATIVE_MEDIA_USE_DURATION_BATTERY_TIMEFRAME_NOT_IN_CHILD_TEXT','MEDIUM'),
    'p2lineage_f6e28439e9fe19023e1a90c9':('general_media_use_duration','television_general_unspecified_period','duration_unspecified_period','SOURCE_NATIVE_MEDIA_USE_DURATION_BATTERY_TIMEFRAME_NOT_IN_CHILD_TEXT','MEDIUM'),
    'p2lineage_1dd3ee49b7617d596ac88ee7':('news_medium_use_frequency','television_news','days_count_unspecified_period','EXPLICIT_DAYS_COUNT_WITHOUT_PERIOD_IN_CHILD_TEXT','MEDIUM'),
    'p2lineage_3d59f246d34b867d63174909':('news_medium_use_frequency','radio_news','days_count_unspecified_period','EXPLICIT_DAYS_COUNT_WITHOUT_PERIOD_IN_CHILD_TEXT','MEDIUM'),
    'p2lineage_85d948f84c11590798049018':('news_medium_use_frequency','newspaper_news','days_count_unspecified_period','EXPLICIT_DAYS_COUNT_WITHOUT_PERIOD_IN_CHILD_TEXT','MEDIUM'),
    'p2lineage_ec5eeaaf9c01eb49dee7dde2':('news_medium_use_frequency','television_news','last_week_days_count','EXPLICIT_LAST_WEEK_DAYS_COUNT_ITEM','HIGH'),
    'p2lineage_854a85ab4fd9b9b48cdf0549':('news_medium_use_frequency','television_news','general_frequency','SOURCE_NATIVE_MEDIA_FREQUENCY_BATTERY_MEMBER','HIGH'),
    'p2lineage_d3070de14bd823f5cedd47e4':('news_medium_use_frequency','radio_news','general_frequency','SOURCE_NATIVE_MEDIA_FREQUENCY_BATTERY_MEMBER','HIGH'),
    'p2lineage_61defd60af0212d874f00c9e':('news_medium_use_frequency','television_news','general_frequency','EXPLICIT_GENERAL_NEWS_MEDIUM_FREQUENCY_ITEM','HIGH'),
    'p2lineage_3f9b3a54fa8d6eccaed36fa0':('news_medium_use_frequency','radio_news','general_frequency','EXPLICIT_GENERAL_NEWS_MEDIUM_FREQUENCY_ITEM','HIGH'),
    'p2lineage_67acaa58def29af73a931a70':('protest_disposition','demonstration_or_protest_march','past_frequency_or_willingness_status','SOURCE_RESPONSE_CONTRACT_MIXES_PAST_AND_WOULD_PARTICIPATION','HIGH'),
    'p2lineage_76b84082bd648fe769ea0ce7':('protest_participation','demonstration_or_protest_march','retrospective_frequency','SOURCE_RESPONSE_CONTRACT_PAST_FREQUENCY','HIGH'),
    'p2lineage_309f2a0887e6f196f9f3f44e':('protest_participation','demonstration_or_protest_march','retrospective_status_or_frequency','TERSE_SOURCE_CHILD_WITH_CATEGORY_COUNT_NO_DELIVERED_LABELS','MEDIUM'),
    'p2lineage_9952401d4600a74512383ce0':('protest_participation','demonstration_or_protest_march','retrospective_status_or_frequency','TERSE_SOURCE_CHILD_WITH_CATEGORY_COUNT_NO_DELIVERED_LABELS','MEDIUM'),
}

OTHER_PATTERNS=[
 ('survey_metadata',r'questionnaire identifier|survey number|country/region|flag variable|anes follow-on eligible|education summary|responsive design experiment|seed address|owner code|refusal$|none of these$'),
 ('employment_status_or_history',r'employment/self-employment|reason for not working|worked in the last|officially retired|accepted wage cuts|work(?:ed)? for wages|occupational situation|hours worked in .*job|short working hours|partner usually works|spouse worked last week'),
 ('household_composition',r'living in household|age of youngest person|main earner in your household'),
 ('party_vote_choice',r'which political party would you vote|party .* appeals to you|party that would never vote|which party\?\(india\)|would you vote at a general election tomorrow'),
 ('party_ideological_position',r'political party:.*left/right|party voters.*left-right|which political party.*left/right'),
 ('religion_identity_or_truth',r'^religion$|only one true religion|no religion offers|church influence national politics'),
 ('economic_condition',r'economic condition|responsible for the economic crisis'),
 ('election_integrity',r'free and fair.*election'),
 ('job_satisfaction',r'satisfied are you with your job'),
 ('environment_attitude',r'humans were meant to rule over nature|polar ice caps|pollution'),
 ('generalized_fairness',r'most people try to take advantage|try to be fair'),
 ('science_or_technology_interest',r'interested in space exploration|interested how and why things happen|interested in technologies|interested in new scientific discoveries|scientific community'),
 ('community_organization_membership',r'do you belong to: cultural activities|do you belong to: local community action'),
 ('parental_obligation',r'love and respect parents'),
 ('work_schedule_control',r'allowed change schedule|takes an hour off during working hours'),
 ('art_elitism',r'few people can judge art'),
 ('politician_self_interest',r'politicians are only for what get out of politics'),
 ('housing_or_asset',r'names on the deed|ownership of a .*dwelling|building owned|equipment and machinery owned|source of finance of dwelling|bank/postal account'),
 ('utility_access',r'access to gas|access to central heating|access to telephone|access to electricity|access to tap water|pipeline gas|main fuel source'),
 ('food_affordability',r'afford meat, chicken or fish'),
 ('marital_event',r'got married|divorced in 1999'),
 ('mortgage_terms',r'mortgage interest rate'),
 ('social_trust_or_connections',r'enough friends and connections|friends with influence'),
 ('education_institution',r'postsecondary institution attended|type of college|graduate to undergraduate'),
 ('arts_or_sports_attendance',r'attended classical|attended sports event|attended dance perf'),
 ('social_companion',r'attended with friend|attended with relative|attended with spouse'),
 ('emotion_self_evaluation',r'felt proud|felt ashamed|regret having done'),
 ('job_attribute',r'important in a job'),
 ('prayer_or_contemplation',r'moments of prayer|meditation or contemplation'),
]

def classify_one(text:str, response_fams:list[str], topologies:list[str]):
    t=norm(text)
    # --- Media and news ---
    if re.search(r'how often do you follow news about politics|follow news about politics and government',t):
        if 'on television' in t: target='political_news_on_television'
        elif 'on the radio' in t: target='political_news_on_radio'
        elif 'daily newspaper' in t and ('television' in t or 'radio' in t): target='political_news_newspaper_television_radio'
        elif 'daily newspaper' in t: target='political_news_in_newspaper'
        else: target='politics_and_government_news_all_or_unspecified_media'
        return ('political_news_following_frequency',target,'frequency','EXPLICIT_POLITICAL_NEWS_FOLLOWING_ITEM','HIGH')
    if re.search(r'how often do you follow politics in the news',t):
        return ('political_news_following_frequency','politics_news_television_radio_newspaper','frequency','EXPLICIT_POLITICAL_NEWS_FOLLOWING_ITEM','HIGH')
    if re.search(r'how often do you follow political news',t):
        return ('political_news_following_frequency','political_news_unspecified_medium','frequency','EXPLICIT_POLITICAL_NEWS_FOLLOWING_ITEM','HIGH')
    if 'tv news favors the governing party' in t:
        return ('news_partisan_bias_perception','television_news_governing_party','bias_evaluation','EXPLICIT_MEDIA_BIAS_ITEM','HIGH')
    if re.search(r'news broadcasts on radio or tv|listen to news on radio|watch(?:ed)? (?:the )?news on television|number of days you (?:watch|listen to|read) news|radio news|tv news',t):
        med=medium_target(t)
        if med=='television': target='television_news'
        elif med=='radio': target='radio_news'
        elif med=='radio_or_television': target='radio_or_television_news'
        elif med=='newspaper': target='newspaper_news'
        elif med=='internet': target='internet_news'
        else: target='news_unspecified_medium'
        if 'last week' in t: operator='last_week_days_count'
        elif 'ordinary week' in t: operator='ordinary_week_frequency'
        elif re.search(r'number of days',t): operator='days_count_unspecified_period'
        else: operator='general_frequency'
        confidence='MEDIUM' if operator=='days_count_unspecified_period' else 'HIGH'
        return ('news_medium_use_frequency',target,operator,'EXPLICIT_NEWS_MEDIUM_FREQUENCY_ITEM',confidence)
    if re.search(r'how often r watches tv news',t):
        return ('news_medium_use_frequency','television_news','general_frequency','EXPLICIT_NEWS_MEDIUM_FREQUENCY_ITEM','HIGH')
    if re.search(r'where news events info|main source of information about events in the news',t):
        return ('information_source_selection','general_news_events','primary_source_selection','EXPLICIT_NEWS_SOURCE_SELECTION_ITEM','HIGH')
    if re.search(r'probable source of information about scientific issues|main source of information about science and technology',t):
        return ('information_source_selection','science_and_technology','primary_source_selection','EXPLICIT_INFORMATION_SOURCE_SELECTION_ITEM','HIGH')
    if re.search(r'principal source of information on the european union',t):
        return ('information_source_selection','european_union','primary_source_selection','EXPLICIT_INFORMATION_SOURCE_SELECTION_ITEM','HIGH')
    if re.search(r'sources of information.*climate change',t):
        return ('information_source_selection','climate_change','multiple_source_selection','EXPLICIT_INFORMATION_SOURCE_SELECTION_ITEM','HIGH')
    if re.search(r'main source for employment information|main source of information for employment opportunities|sought job information from',t):
        return ('information_source_selection','employment_opportunities','source_use_or_selection','EXPLICIT_EMPLOYMENT_INFORMATION_SOURCE_ITEM','HIGH')
    if re.search(r'sought health information tv or radio',t):
        return ('information_source_selection','health_information','source_use','EXPLICIT_HEALTH_INFORMATION_SOURCE_ITEM','HIGH')
    if re.search(r'reliability of news',t):
        med=medium_target(t)
        target={'television':'television_news','internet':'internet_news','newspaper':'newspaper_news','radio_or_podcast':'radio_or_podcast_news'}.get(med,med)
        return ('news_reliability_rating',target,'reliability_rating','EXPLICIT_NEWS_RELIABILITY_ITEM','HIGH')
    if re.search(r'mother liked to follow the news',t):
        target='mother_at_age_14' if 'age 14' in t else 'mother_unspecified_period'
        return ('parental_news_interest',target,'reported_interest','EXPLICIT_PARENTAL_NEWS_INTEREST_ITEM','HIGH')
    if re.search(r'father liked to follow the news',t):
        target='father_at_age_14' if 'age 14' in t else 'father_unspecified_period'
        return ('parental_news_interest',target,'reported_interest','EXPLICIT_PARENTAL_NEWS_INTEREST_ITEM','HIGH')
    if re.search(r'hours spent watching tv|total minutes watched tv',t):
        return ('general_television_use_duration','television_general','duration','EXPLICIT_TELEVISION_DURATION_ITEM','HIGH')
    if re.fullmatch(r'television(?::version z)?',t):
        return ('media_device_or_medium_indicator','television','indicator_or_ownership','TERSE_MEDIA_INDICATOR','MEDIUM')
    if re.search(r'color or b/w television|colour tv set',t):
        return ('media_device_ownership','television_set','ownership_or_type','EXPLICIT_TELEVISION_OWNERSHIP_ITEM','HIGH')
    # --- Internet/computer ---
    if re.search(r'on average, how often do you use the internet|internet-use frequency|how often do you use: the internet|how often do you use the internet(?:,|\?| either)|do you use the internet\.\.\.',t):
        return ('internet_use_frequency','internet_general','frequency','EXPLICIT_GENERAL_INTERNET_FREQUENCY_ITEM','HIGH')
    if re.fullmatch(r'internet',t):
        return ('internet_use_frequency','internet_general','frequency','SOURCE_NATIVE_FREQUENCY_BATTERY_CHILD','HIGH')
    if re.search(r'internet users, total',t):
        return ('internet_population_penetration','population_internet_use','derived_percentage','EXPLICIT_DERIVED_POPULATION_INDICATOR','HIGH')
    if re.search(r'internet access at home|access to internet at home|internet access in r.s home|home internet access|have internet access at home|household has access to internet using broadband',t):
        if 'frequency' in t: return ('internet_access_frequency','home_internet','frequency','EXPLICIT_HOME_INTERNET_ACCESS_FREQUENCY_ITEM','HIGH')
        target='home_broadband_internet' if 'broadband' in t else 'home_internet'
        return ('internet_access',target,'access_or_availability','EXPLICIT_HOME_INTERNET_ACCESS_ITEM','HIGH')
    if re.search(r'internet access on a mobile phone|internet through cell phone|home internet through mobile device|use internet/apps from phone|mobile phone or smart phone to access the internet',t):
        return ('internet_access','mobile_device_internet','access_or_use','EXPLICIT_MOBILE_INTERNET_ITEM','HIGH')
    if re.search(r'internet access in public|work/school internet access',t):
        target='public_internet' if 'public' in t else 'work_or_school_internet'
        return ('internet_access_frequency',target,'frequency','EXPLICIT_LOCATION_SPECIFIC_INTERNET_ACCESS_ITEM','HIGH')
    if re.search(r'www hours per week|hours per week .*computer www|minutes per week .*computer www|hours of internet use|minutes of internet use',t):
        loc='work_computer' if 'work computer' in t else ('other_computer' if 'other computer' in t else 'internet_general')
        period='weekday' if 'weekday' in t else ('weekend' if 'weekend' in t else 'weekly')
        return ('internet_use_duration',f'{loc}:{period}','duration','EXPLICIT_INTERNET_DURATION_ITEM','HIGH')
    if re.search(r'email hours per week|hours per week .*computer email|minutes per week .*computer email',t):
        loc='work_computer_email' if 'work computer' in t else ('other_computer_email' if 'other computer' in t else 'email_general')
        return ('internet_activity_duration',loc,'duration','EXPLICIT_EMAIL_DURATION_ITEM','HIGH')
    if re.search(r'email messages (?:sent|received) per day|personal email messages sent|personal messages received',t):
        direction='sent' if 'sent' in t else 'received'
        scope='personal' if 'personal' in t else 'all'
        return ('email_message_volume',f'{scope}:{direction}','daily_count','EXPLICIT_EMAIL_VOLUME_ITEM','HIGH')
    if re.search(r'use internet/apps more than|used internet/apps yesterday',t):
        op='recent_use_yesterday' if 'yesterday' in t else 'use_threshold'
        return ('internet_use_incidence','internet_or_apps_general',op,'EXPLICIT_INTERNET_USE_INCIDENCE_ITEM','HIGH')
    if re.search(r'how often r uses internet for|use of electronic mail or internet connection:',t):
        return ('internet_activity_use',internet_purpose(t),'frequency_or_incidence','EXPLICIT_INTERNET_PURPOSE_ITEM','HIGH')
    if re.search(r'use the internet in order to|use the internet or social media networks to (?:express|find)',t):
        return ('internet_political_activity',internet_purpose(t),'frequency_or_incidence','EXPLICIT_POLITICAL_INTERNET_ACTIVITY_ITEM','HIGH')
    if re.search(r'ability to use internet|skill at using the internet',t):
        return ('internet_skill','internet_general','self_assessed_skill','EXPLICIT_INTERNET_SKILL_ITEM','HIGH')
    if re.search(r'asked to use internet for someone else|asked someone to use the internet on their behalf',t):
        target='assisted_other_person' if 'for someone else' in t else 'received_assistance'
        return ('internet_proxy_use','internet_general:'+target,'frequency','EXPLICIT_PROXY_INTERNET_USE_ITEM','HIGH')
    if re.search(r'reason r reduced time spent on internet',t):
        return ('internet_use_reduction_reason','internet_general','reason_selection','EXPLICIT_INTERNET_REDUCTION_REASON_ITEM','HIGH')
    if re.search(r'r.s knowledge of online information discretion',t):
        return ('digital_information_literacy','online_information_discretion','knowledge_assessment','EXPLICIT_DIGITAL_LITERACY_ITEM','HIGH')
    if re.search(r'permission to access r.s facebook account',t):
        return ('social_media_privacy_permission','facebook_account','permission','EXPLICIT_SOCIAL_MEDIA_PRIVACY_ITEM','HIGH')
    if re.search(r'r learn something new on (?:the )?web',t):
        target='arts' if 'arts' in t else 'general'
        return ('internet_learning','web:'+target,'incidence','EXPLICIT_WEB_LEARNING_ITEM','HIGH')
    if re.search(r'web make r attend a political meeting',t):
        return ('internet_political_mobilization','political_meeting_attendance','reported_effect','EXPLICIT_DIGITAL_MOBILIZATION_ITEM','HIGH')
    if re.search(r'r use computer|does r use computer|holding of a computer|^computer$|desktop computer|smartphone$|mobile phone not smartphone',t):
        if 'smartphone' in t and 'not smartphone' not in t: target='smartphone'
        elif 'mobile phone not smartphone' in t: target='non_smart_mobile_phone'
        elif 'desktop computer' in t: target='desktop_laptop_tablet'
        else: target='computer_general'
        return ('digital_device_use_or_ownership',target,'use_or_ownership','EXPLICIT_DIGITAL_DEVICE_ITEM','HIGH')
    if re.search(r'does r use computer at|where does r use computer most',t):
        if 'school' in t: target='school'
        elif 'library' in t: target='library'
        elif 'friends house' in t: target='friends_house'
        elif 'work' in t: target='work'
        else: target='primary_location'
        return ('computer_use_location',target,'use_or_primary_location','EXPLICIT_COMPUTER_LOCATION_ITEM','HIGH')
    # --- Political discussion, interest, and engagement ---
    if re.search(r'how often do you discuss politics|how often discuss politics|discuss political matters|discuss politics with your friends|how frequently do you discuss politics|how often do you talk politics|^discuss politics$',t):
        if 'family members' in t and 'friends' in t: target='family_members_or_friends'
        elif 'friends and colleagues' in t: target='friends_and_colleagues'
        elif 'friends' in t: target='friends'
        else: target='people_unspecified'
        return ('political_discussion_frequency',target,'frequency','EXPLICIT_POLITICAL_DISCUSSION_ITEM','HIGH')
    if re.search(r'try to persuade friends|try to convince others politically',t):
        target='friends' if 'friends' in t else 'other_people_unspecified'
        return ('political_persuasion_frequency',target,'frequency','EXPLICIT_POLITICAL_PERSUASION_ITEM','HIGH')
    if re.search(r'try to persuade others to vote',t):
        return ('campaign_vote_persuasion','candidate_or_party_vote_choice','retrospective_participation','EXPLICIT_ELECTION_PERSUASION_ITEM','HIGH')
    if re.search(r'how interested.*politics|interested in politics|interest in politics|describing interest in politics|your interest in politics',t):
        return ('political_interest','politics','interest_rating','EXPLICIT_POLITICAL_INTEREST_ITEM','HIGH')
    if re.search(r'interested.*public affairs',t):
        return ('public_affairs_interest','public_affairs','interest_rating','EXPLICIT_PUBLIC_AFFAIRS_INTEREST_ITEM','HIGH')
    if re.fullmatch(r'politics',t):
        # Without a response contract this would be unresolved; the WVS importance battery is governed by an override.
        return ('unresolved_axis','politics_unspecified','unspecified_operator','TERSE_POLITICS_LABEL_WITHOUT_OPERATOR','LOW')
    if re.search(r'(?:hard time conversing.*opinions on politics differed|opinions on politics differed.*hard time conversing)',t):
        return ('political_disagreement_conversation_tolerance','politically_disagreeing_friends_or_coworkers','difficulty_rating','EXPLICIT_POLITICAL_TOLERANCE_ITEM','HIGH')
    if re.search(r'ability to participate in politics',t):
        return ('internal_political_efficacy','political_participation','ability_agreement','EXPLICIT_INTERNAL_EFFICACY_ITEM','HIGH')
    if re.search(r'follow political news',t):
        return ('political_news_following_frequency','political_news_unspecified_medium','frequency','EXPLICIT_POLITICAL_NEWS_ITEM','HIGH')
    # --- Contacting and collective action ---
    if re.search(r'got together with others.*resolve local problems',t):
        return ('collective_local_problem_action','local_community_problems','retrospective_participation','EXPLICIT_COLLECTIVE_ACTION_ITEM','HIGH')
    if re.search(r'participate in the activities of (?:community|neighbou?rhood)',t):
        return ('community_activity_participation','community_or_neighborhood','frequency','EXPLICIT_COMMUNITY_PARTICIPATION_ITEM','HIGH')
    if re.search(r'contacted? an influential person',t):
        return ('political_contact','influential_person','ever_contacted','EXPLICIT_POLITICAL_CONTACT_ITEM','HIGH')
    if re.search(r'contacted? (?:the )?government or a party official',t):
        return ('political_contact','government_or_party_official','ever_contacted','EXPLICIT_POLITICAL_CONTACT_ITEM','HIGH')
    if re.search(r'contacted? any government official|contacted officials.*higher level',t):
        target='higher_level_government_official' if 'higher level' in t else 'government_official'
        return ('political_contact',target,'retrospective_contact','EXPLICIT_POLITICAL_CONTACT_ITEM','HIGH')
    if re.search(r'contacted political parties|political organizations',t):
        return ('political_contact','political_party_or_organization','retrospective_contact','EXPLICIT_POLITICAL_CONTACT_ITEM','HIGH')
    if re.search(r'contacted non-government|civil society organizations',t):
        return ('political_contact','ngo_or_civil_society_organization','retrospective_contact','EXPLICIT_POLITICAL_CONTACT_ITEM','HIGH')
    if re.search(r'contacted media',t):
        return ('political_contact','media','retrospective_contact','EXPLICIT_POLITICAL_CONTACT_ITEM','HIGH')
    if re.search(r'contacted other people',t):
        return ('political_contact','other_people','retrospective_contact','EXPLICIT_POLITICAL_CONTACT_ITEM','HIGH')
    if re.search(r'ask civil servants or politicians for things',t):
        return ('political_contact','civil_servant_or_politician','frequency','EXPLICIT_POLITICAL_CONTACT_ITEM','HIGH')
    if re.search(r'raised an issue affecting citizens',t):
        return ('civic_issue_raising','citizen_issue','ever_participated','EXPLICIT_CIVIC_ISSUE_ITEM','HIGH')
    # --- Demonstration/protest/strike/rally ---
    if re.search(r'attended a campaign meeting or rally|attended an election rally|attend a campaign meeting or rally',t):
        if 'last national election' in t: target='campaign_rally_last_national_election'
        elif 'ever attended' in t: target='election_rally_ever'
        else: target='campaign_or_election_rally_unspecified_period'
        return ('campaign_rally_participation',target,'retrospective_participation','EXPLICIT_CAMPAIGN_RALLY_ITEM','HIGH')
    if re.search(r'most important reason for the protests|second most important reason for the protests',t):
        rank='second_reason' if 'second' in t else 'first_reason'
        return ('protest_reason_ranking','named_2010_2011_uprising:'+rank,'reason_selection','EXPLICIT_PROTEST_REASON_RANKING_ITEM','HIGH')
    if re.search(r'participated in any protest or demonstration or struggle or movement',t):
        return ('protest_participation','protest_demonstration_struggle_or_movement','retrospective_participation','EXPLICIT_PROTEST_PARTICIPATION_ITEM','HIGH')
    if re.search(r'attended a demonstration or protest march|attend a demonstration or protest march|civic participation: demonstration or protest march',t):
        op='past_year_participation' if 'past year' in t else 'retrospective_or_ever_participation'
        return ('protest_participation','demonstration_or_protest_march',op,'EXPLICIT_DEMONSTRATION_PARTICIPATION_ITEM','HIGH')
    if re.search(r'demonstrated, striken, or sat-in|demonstration, strike, sit-in',t):
        return ('contentious_action_participation','demonstration_strike_or_sit_in','retrospective_participation','EXPLICIT_CONTENTIOUS_ACTION_ITEM','HIGH')
    if re.search(r'political demonstrations\?',t) and re.search(r'have you, or would you ever',t):
        return ('protest_disposition','political_demonstration','past_or_willingness_status','EXPLICIT_PAST_OR_WOULD_PARTICIPATION_ITEM','HIGH')
    if re.search(r'participate in riots',t):
        return ('riot_disposition','riot','past_or_willingness_status','EXPLICIT_RIOT_ITEM','HIGH')
    if re.search(r'attend a lawful demonstration|affinity to attend lawful demonstrations',t):
        return ('protest_willingness','lawful_demonstration','likelihood','EXPLICIT_LAWFUL_DEMONSTRATION_ITEM','HIGH')
    if re.search(r'participate in a strike|affinity to participate in strikes',t):
        return ('strike_willingness','strike','likelihood','EXPLICIT_STRIKE_ITEM','HIGH')
    if re.search(r'political cause.*risk of getting injured',t):
        return ('high_risk_political_action','political_cause_with_injury_risk','retrospective_participation','EXPLICIT_HIGH_RISK_POLITICAL_ACTION_ITEM','HIGH')
    if re.search(r'school related demonstration',t):
        return ('school_demonstration_experience','school_demonstration','experience_indicator','EXPLICIT_SCHOOL_DEMONSTRATION_ITEM','HIGH')
    if re.search(r'stranger in protest march',t):
        return ('protest_march_social_context','stranger_in_protest_march','scenario_or_contact','EXPLICIT_PROTEST_CONTEXT_ITEM','MEDIUM')
    if re.search(r'important.*(?:people|ppl) given chance to participate in (?:decisions|decsns)',t):
        return ('participatory_decision_norm','people_in_decisions','importance_rating','EXPLICIT_PARTICIPATION_NORM_ITEM','HIGH')
    if re.search(r'important to keep watch on action of govt',t):
        return ('government_watchdog_norm','citizen_monitoring_of_government','importance_rating','EXPLICIT_GOVERNMENT_WATCH_NORM_ITEM','HIGH')
    if re.search(r'how often do you use: a computer',t):
        return ('computer_use_frequency','computer_general','frequency','EXPLICIT_COMPUTER_USE_FREQUENCY_ITEM','HIGH')
    if re.search(r'have you ever attended a demonstration$',t):
        return ('protest_disposition','demonstration_general','past_frequency_or_willingness_status','EXPLICIT_MIXED_PAST_AND_WOULD_DEMONSTRATION_ITEM','HIGH')
    if re.search(r'most essential characteristic of democracy',t):
        return ('other_domain','democracy_feature_choice','ranked_or_forced_choice','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.search(r'name legislative representative',t):
        return ('other_domain','legislative_representative_knowledge','knowledge_assessment','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.fullmatch(r'education(?:\(four categories\))?',t):
        return ('other_domain','respondent_education','demographic_classification','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.search(r'watch or listen to religious programs',t):
        return ('religious_media_consumption_frequency','religious_programs_radio_or_television','frequency','EXPLICIT_RELIGIOUS_MEDIA_ITEM','HIGH')
    if re.search(r'fast during ramadan|fast the 40 days of lent',t):
        return ('other_domain','religious_fasting_frequency','practice_frequency','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.search(r'primary source of information to follow the breaking news',t):
        return ('information_source_selection','breaking_news','primary_source_selection','EXPLICIT_BREAKING_NEWS_SOURCE_ITEM','HIGH')
    if re.search(r'sources of local political and government information',t):
        return ('information_source_selection','local_political_and_government_information','ranked_source_selection','EXPLICIT_POLITICAL_INFORMATION_SOURCE_ITEM','HIGH')
    if re.search(r'follow major events in foreign countries|follow major events.*the world',t):
        return ('international_news_following_frequency','foreign_or_world_events','attention_frequency','EXPLICIT_INTERNATIONAL_NEWS_ITEM','HIGH')
    if re.search(r'any town halls or community buildings',t):
        return ('other_domain','community_meeting_infrastructure','availability','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.search(r'harmony of the community.*organize lots of groups',t):
        return ('civic_association_pluralism_attitude','group_organization_and_community_harmony','agreement_evaluation','EXPLICIT_ASSOCIATIONAL_PLURALISM_ITEM','HIGH')
    if re.search(r'how many people do you have contact',t):
        return ('other_domain','interpersonal_contact_volume','typical_day_count','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.search(r'number of supervised people',t):
        return ('other_domain','job_supervisory_span','count_category','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.search(r'length of interview',t):
        return ('other_domain','interview_duration','paradata_duration','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.search(r'access to stress management',t):
        return ('other_domain','stress_management_access','access','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.search(r'hours per day r have to relax',t):
        return ('other_domain','daily_leisure_time','duration','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.search(r'more comfortable meeting people online',t):
        return ('digital_social_comfort','online_interpersonal_contact','agreement_evaluation','EXPLICIT_DIGITAL_SOCIAL_ATTITUDE_ITEM','HIGH')
    if re.search(r'next important issue .*none of these',t):
        return ('other_domain','survey_followup_option_fragment','coded_option_indicator','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.search(r'interested in economic issues',t):
        return ('other_domain','economic_issue_interest','interest_rating','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    if re.search(r'likely can r do sth for improvmnt in community',t):
        return ('community_action_efficacy','community_improvement_action','likelihood','EXPLICIT_COMMUNITY_EFFICACY_ITEM','HIGH')
    if re.search(r'heard, through the media.*united states involvement',t):
        return ('media_exposure_awareness','reported_us_involvement','awareness','EXPLICIT_MEDIA_AWARENESS_ITEM','HIGH')
    if re.search(r'chatroom hours per week',t):
        return ('internet_activity_duration','chatroom_use','duration','EXPLICIT_CHATROOM_DURATION_ITEM','HIGH')
    if re.search(r'access to justice \[v-dem',t):
        return ('other_domain','access_to_justice_derived_indicator','derived_statistic','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','HIGH')
    # generic other-domain classification
    for axis,pat in OTHER_PATTERNS:
        if re.search(pat,t): return ('other_domain',axis,'other_operator','EXACT_TEXT_EXCLUDES_GOVERNED_DOMAIN','MEDIUM')
    return ('unresolved_axis','unspecified','unresolved','NO_GOVERNED_OPERATOR_RECOVERED','LOW')

queue=read(QREM)
selection_path=os.environ.get('RAWLSING_FIXED_3000_SELECTION','').strip()
if selection_path:
    sel=read(Path(selection_path))
else:
    full_ids=['MEDIA_NEWS_SOURCE','MEDIA_INTERNET','CIVIC_DISCUSS_POLITICS','CIVIC_INTEREST_POLITICS']
    sel=queue[queue.semantic_content_id.isin(full_ids)].copy()
    need=3000-len(sel)
    assert need>=0
    partial=(queue[queue.semantic_content_id.eq('CIVIC_DEMONSTRATION')]
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
            axis,target,op='heterogeneous_lineage','heterogeneous','heterogeneous'
            basis='MULTIPLE_MATERIAL_CLASSIFICATIONS:'+compact([{'text':texts[i],'axis':x[0],'target':x[1],'operator':x[2]} for i,x in enumerate(per)])
            conf='LOW'
    status='P2_MEDIA_CIVIC_LINEAGE_CLASSIFIED'
    if axis in {'unresolved_axis','heterogeneous_lineage'}: status='P2_MEDIA_CIVIC_LINEAGE_UNRESOLVED'
    elif axis=='other_domain': status='P2_OUT_OF_DOMAIN_LINEAGE_REDIRECTED'
    elif conf=='MEDIUM': status='P2_MEDIA_CIVIC_LINEAGE_COORDINATE_ONLY_INCOMPLETE_PROPOSITION'
    classes.append({
      'classification_id':stable('p2mediacivicclassv1',lr.lineage_id),'lineage_id':lr.lineage_id,'source_family':lr.source_family,'member_count':lr.member_count,
      'variables_json':compact(uniq(g.source_variable_code.tolist())),'waves_json':compact(uniq(g.wave.tolist())),'exact_question_texts_json':compact(texts),
      'response_options_json':compact(uniq(g.response_options_substantive.tolist())),'response_topologies_json':compact(tops),'response_family_expectations_json':compact(responses),
      'semantic_content_ids_json':compact(uniq(g.semantic_content_id.tolist())),'source_structure_ids_json':compact(sids),'source_structure_labels_json':compact(slabels),
      'governed_relation_axis':axis,'governed_target_or_scope':target,'governed_operator':op,'classification_basis':basis,'classification_confidence':conf,
      'authority_status':status,'prohibited_use':'Classification coordinate only; no J-family membership, value harmonization, or respondent join.'
    })
classes=pd.DataFrame(classes).sort_values(['source_family','lineage_id'])
classes.to_csv(OUT/'Rawlsing_P2_Media_Civic_Lineage_Classification_v1.csv',index=False)
cidx=classes.set_index('lineage_id')

DOMAIN_FAMILY={
 'political_news_following_frequency':'political_information_engagement','international_news_following_frequency':'news_consumption','news_medium_use_frequency':'news_consumption','information_source_use_frequency':'information_source','information_source_selection':'information_source','news_reliability_rating':'news_evaluation','news_partisan_bias_perception':'news_evaluation','parental_news_interest':'news_socialization','general_television_use_duration':'general_media_use','media_device_or_medium_indicator':'media_access','media_device_ownership':'media_access','media_service_access':'media_access','general_media_use_duration':'general_media_use','religious_media_consumption_frequency':'general_media_use','media_exposure_awareness':'media_exposure',
 'internet_use_frequency':'internet_general_use','computer_use_frequency':'digital_device_use','internet_population_penetration':'internet_general_use','internet_access':'internet_access','internet_access_frequency':'internet_access','internet_mobile_use':'internet_access','internet_use_duration':'internet_general_use','internet_activity_duration':'internet_activity','email_message_volume':'internet_activity','internet_use_incidence':'internet_general_use','internet_activity_use':'internet_activity','internet_political_activity':'digital_political_engagement','internet_skill':'digital_capacity','internet_proxy_use':'digital_capacity','internet_use_reduction_reason':'internet_general_use','digital_information_literacy':'digital_capacity','social_media_privacy_permission':'digital_privacy','internet_learning':'internet_activity','internet_political_mobilization':'digital_political_engagement','digital_device_use_or_ownership':'media_access','computer_use_location':'media_access',
 'political_discussion_frequency':'political_interpersonal_engagement','political_persuasion_frequency':'political_interpersonal_engagement','campaign_vote_persuasion':'campaign_participation','political_interest':'political_attention','public_affairs_interest':'political_attention','politics_life_importance':'political_attention','political_disagreement_conversation_tolerance':'political_tolerance','internal_political_efficacy':'political_efficacy','civic_association_pluralism_attitude':'civic_attitude','digital_social_comfort':'digital_sociality',
 'collective_local_problem_action':'community_civic_action','community_activity_participation':'community_civic_action','community_action_efficacy':'community_civic_action','political_contact':'institutional_contact','civic_issue_raising':'institutional_contact',
 'campaign_rally_participation':'campaign_participation','protest_reason_ranking':'contentious_politics','protest_participation':'contentious_politics','contentious_action_participation':'contentious_politics','protest_disposition':'contentious_politics','riot_disposition':'contentious_politics','protest_willingness':'contentious_politics','strike_willingness':'contentious_politics','high_risk_political_action':'contentious_politics','school_demonstration_experience':'contentious_politics','protest_march_social_context':'contentious_politics','participatory_decision_norm':'civic_norm','government_watchdog_norm':'civic_norm'
}

def topology_set(row): return set(json.loads(row.response_topologies_json))
def family(axis): return DOMAIN_FAMILY.get(axis,'')

rul=[]
for _,cand in sel.iterrows():
    l=cidx.loc[cand.left_lineage_id]; r=cidx.loc[cand.right_lineage_id]
    la,ra=l.governed_relation_axis,r.governed_relation_axis
    lt,rt=l.governed_target_or_scope,r.governed_target_or_scope
    lo,ro=l.governed_operator,r.governed_operator
    lc,rc=l.classification_confidence,r.classification_confidence
    if 'UNRESOLVED' in l.authority_status or 'UNRESOLVED' in r.authority_status:
        status='UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_SOURCE_LOCAL_EVIDENCE'; rel='UNRESOLVED'; ceil='NO_AUTHORITY'; rat='At least one source-local lineage lacks one exportable relation, target/scope, and operator.'
    elif la=='other_domain' and ra=='other_domain':
        if lt==rt and lt not in {'survey_metadata','survey_special_response_fragment'}:
            status='REDIRECTED_OUT_OF_MEDIA_CIVIC_DOMAIN_SHARED_OTHER_AXIS_NOT_ADJUDICATED'; rel='OTHER_DOMAIN_REVIEW_REQUIRED'; ceil='NO_MEDIA_CIVIC_AUTHORITY'; rat='Both exact lineages belong to the same other-domain axis, but this tranche does not manufacture authority for that domain.'
        else:
            status='REJECTED_CONTAMINATED_NEIGHBORHOOD_OTHER_DOMAIN_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='Both items are outside the governed domain and do not share a governed substantive axis.'
    elif la=='other_domain' or ra=='other_domain':
        status='REJECTED_MEDIA_CIVIC_VERSUS_OTHER_DOMAIN_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='One lineage asserts a media/civic proposition while the other exact item belongs to another domain.'
    elif la==ra and lt==rt and lo==ro and lc=='HIGH' and rc=='HIGH':
        status='ACCEPTED_TYPED_MEDIA_CIVIC_PROPOSITION_RELATION'; rel='REWORDED_PROPOSITION_EQUIVALENCE'
        same_top=topology_set(l)==topology_set(r) and len(topology_set(l))==1
        same_resp=set(json.loads(l.response_family_expectations_json))==set(json.loads(r.response_family_expectations_json))
        ceil='QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY' if same_top and same_resp else 'QUESTION_PROPOSITION_ONLY'
        rat='Both source-local lineages assert the same governed relation toward the same target/scope with the same operator; both classifications are HIGH-confidence.'
    elif la==ra and lt==rt:
        status='ACCEPTED_SAME_CONSTRUCT_TARGET_DIFFERENT_OPERATOR_OR_INCOMPLETE_EVIDENCE_COORDINATE_ONLY'; rel='CONSTRUCT_TARGET_COORDINATE_ONLY'; ceil='CONSTRUCT_TARGET_ONLY'; rat='The construct and target/scope agree, but the operators differ or at least one source record cannot support proposition-level export.'
    elif family(la) and family(la)==family(ra):
        status='ACCEPTED_DOMAIN_COORDINATE_ONLY_RELATION_OR_TARGET_SCOPE_DIFFERS'; rel='DOMAIN_COORDINATE_ONLY'; ceil='DOMAIN_COORDINATE_ONLY'; rat='The items share a governed domain family but differ in relation, target, medium, location, temporal frame, or participation mode.'
    elif family(la) and family(ra):
        status='REJECTED_FALSE_EQUIVALENCE_MEDIA_CIVIC_RELATION_OR_TARGET_MISMATCH'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='Both items are on the broad media/civic surface but assert materially different relations or targets.'
    else:
        status='REJECTED_DIFFERENT_GOVERNED_RELATION_AXES'; rel='NEGATIVE_AUTHORITY'; ceil='NO_EQUIVALENCE'; rat='The exact lineages assert different governed relations.'
    rid=stable('p2mediacivicrulingv1',cand.semantic_pair_candidate_id)
    rul.append({
      'pair_ruling_id':rid,'semantic_pair_candidate_id':cand.semantic_pair_candidate_id,'semantic_content_id':cand.semantic_content_id,
      'left_source_family':cand.left_source_family,'right_source_family':cand.right_source_family,'left_lineage_id':cand.left_lineage_id,'right_lineage_id':cand.right_lineage_id,
      'left_relation_axis':la,'right_relation_axis':ra,'left_target_or_scope':lt,'right_target_or_scope':rt,'left_operator':lo,'right_operator':ro,
      'left_classification_confidence':lc,'right_classification_confidence':rc,
      'authority_status':status,'relation_type':rel,'portability_ceiling':ceil,'rationale':rat,'left_classification_id':l.classification_id,'right_classification_id':r.classification_id,
      'two_sided_evidence_status':'EXPLICIT_LINEAGE_NODE_RESPONSE_AND_STRUCTURE_PROVENANCE_BOTH_SIDES','prohibited_use':'No J-family authority, value harmonization, or respondent join follows from this ruling.'
    })
rul=pd.DataFrame(rul)
rul.to_csv(OUT/'Rawlsing_P2_Media_Civic_3000_Pair_Rulings_v1.csv',index=False)

# Evidence ledger: one direct side record per ruling side.
ev=[]
for _,rr in rul.iterrows():
    for side in ('left','right'):
        lid=rr[f'{side}_lineage_id']; c=cidx.loc[lid]; g=nodegroups[lid]
        ev.append({
          'evidence_record_id':stable('p2mediacivicevidencev1',rr.pair_ruling_id,side),'pair_ruling_id':rr.pair_ruling_id,'semantic_pair_candidate_id':rr.semantic_pair_candidate_id,'side':side.upper(),
          'lineage_id':lid,'source_family':c.source_family,'classification_id':c.classification_id,'governed_relation_axis':c.governed_relation_axis,'governed_target_or_scope':c.governed_target_or_scope,'governed_operator':c.governed_operator,
          'question_implementation_ids_json':compact(g.question_implementation_id.tolist()),'wave_variable_locators_json':compact([{'wave':x.wave,'variable':x.source_variable_code,'source_row_index':x.source_row_index} for _,x in g.iterrows()]),
          'exact_question_texts_json':c.exact_question_texts_json,'response_options_json':c.response_options_json,'response_topologies_json':c.response_topologies_json,'response_family_expectations_json':c.response_family_expectations_json,
          'source_structure_ids_json':c.source_structure_ids_json,'source_structure_labels_json':c.source_structure_labels_json,'classification_basis':c.classification_basis,'classification_confidence':c.classification_confidence,
          'evidence_sufficiency':'COMPLETE_FOR_PROPOSITION_CEILING' if c.classification_confidence=='HIGH' and 'UNRESOLVED' not in c.authority_status else ('COMPLETE_FOR_COORDINATE_ONLY' if c.classification_confidence=='MEDIUM' else 'INCOMPLETE_OR_HETEROGENEOUS')
        })
ev=pd.DataFrame(ev)
ev.to_csv(OUT/'Rawlsing_P2_Media_Civic_3000_Two_Sided_Evidence_Ledger_v1.csv',index=False)

remaining=queue[~queue.semantic_pair_candidate_id.isin(set(sel.semantic_pair_candidate_id))].copy()
remaining.to_csv(OUT/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Media_Civic_Fixed_3000_Tranche_v5.csv',index=False)
sel.to_csv(OUT/'Rawlsing_P2_Media_Civic_Fixed_3000_Tranche_Candidate_Surface_v1.csv',index=False)

summary={
 'contract_version':'P2_FIXED_3000_MEDIA_CIVIC_TRANCHE_V1','input_pending_pairs':len(queue),'fixed_work_unit_pairs':len(sel),'remaining_pairs':len(remaining),
 'selected_semantic_id_counts':{str(k):int(v) for k,v in sel.semantic_content_id.value_counts().sort_index().items()},
 'lineages_classified':len(classes),'classification_status_counts':{str(k):int(v) for k,v in classes.authority_status.value_counts().sort_index().items()},
 'pair_status_counts':{str(k):int(v) for k,v in rul.authority_status.value_counts().sort_index().items()},'relation_type_counts':{str(k):int(v) for k,v in rul.relation_type.value_counts().sort_index().items()},
 'evidence_rows':len(ev),'expected_evidence_rows':2*len(rul),'selection_exactly_3000':len(sel)==3000,'queue_partition_exact':len(sel)+len(remaining)==len(queue),
 'selected_ids_unique':sel.semantic_pair_candidate_id.nunique()==3000,'ruling_ids_unique':rul.pair_ruling_id.nunique()==3000,'evidence_ids_unique':ev.evidence_record_id.nunique()==6000,
 'proposition_acceptance_requires_axis_target_operator_identity_and_high_confidence':bool(((rul.authority_status!='ACCEPTED_TYPED_MEDIA_CIVIC_PROPOSITION_RELATION')|((rul.left_relation_axis==rul.right_relation_axis)&(rul.left_target_or_scope==rul.right_target_or_scope)&(rul.left_operator==rul.right_operator)&(rul.left_classification_confidence=='HIGH')&(rul.right_classification_confidence=='HIGH'))).all()),
 'authority_boundary':'PAIR_RELATION_AUTHORITY_ONLY_NO_J_FAMILY_NO_VALUE_HARMONIZATION'
}
(OUT/'FIXED_3000_MEDIA_CIVIC_TRANCHE_RETURN.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(summary,indent=2,ensure_ascii=False))
