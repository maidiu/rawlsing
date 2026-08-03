#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path('/mnt/data/rawlsing_v14_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v14_20260731')
S32 = ROOT / '32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'
S33 = ROOT / '33_P2_GLOBAL_REWORDED_RELATION_AXIS_STRUCTURE_ADJUDICATION_TRANCHE2'
OUT = Path('/mnt/data/rawlsing_v15_outputs/trust_adjudication')


def read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def stable_id(prefix: str, *parts: object) -> str:
    payload = chr(31).join(map(str, parts)).encode('utf-8')
    return f'{prefix}_{hashlib.sha256(payload).hexdigest()[:24]}'


def norm(value: object) -> str:
    return re.sub(r'\s+', ' ', str(value or '').strip().casefold())


def json_compact(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def unique(values):
    return list(dict.fromkeys(v for v in values if str(v).strip()))


queue = read(S33 / 'Rawlsing_P2_Semantic_Priority_Queue_Remaining_v2.csv')
trust_semantic_ids = {
    'TRUST_GENERAL', 'TRUST_GOVERNMENT', 'TRUST_STRANGERS', 'TRUST_COURTS',
    'TRUST_POLICE', 'TRUST_ARMY', 'TRUST_PARLIAMENT', 'TRUST_RELIGIOUS_LEADERS',
    'TRUST_ELECTIONS', 'MEDIA_TRUST_SOCIAL',
}
trust_queue = queue[queue.semantic_content_id.isin(trust_semantic_ids)].copy()
nodes = read(S32 / 'Rawlsing_P2_All_Nine_Unified_Node_Evidence_Registry_v1.csv')
lineages = read(S32 / 'Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv')
structure_memberships = read(S32 / 'Rawlsing_P2_Normalized_Source_Structure_Memberships_v1.csv')
structures = read(S32 / 'Rawlsing_P2_Normalized_Source_Structure_Registry_v1.csv')

node_groups = {key: group for key, group in nodes.groupby('lineage_id')}
structure_by_id = structures.set_index('source_structure_id')
structures_by_question: dict[str, list[str]] = defaultdict(list)
for _, row in structure_memberships.iterrows():
    structures_by_question[row.question_implementation_id].append(row.source_structure_id)

needed_lineages = set(trust_queue.left_lineage_id) | set(trust_queue.right_lineage_id)
lineage_surface = lineages[lineages.lineage_id.isin(needed_lineages)].copy()

# Source-native bare battery children whose child text omits the relation operator.
# These are narrowly scoped to the recovered parent battery; the target is still read
# from the exact child text and is not generalized beyond it.
OVERRIDE_AXES = {
    'p2lineage_6e7e43e8ef8797bb1fface4c': ('institutional_trust', 'PARENT_BATTERY_RECOVERED_ASIAN_TRUST_RUN'),
    'p2lineage_6cfc2c25546f4102569aece4': ('institutional_trust', 'PARENT_BATTERY_RECOVERED_ASIAN_TRUST_RUN'),
    'p2lineage_ac280890f42505b4377c7525': ('institutional_trust', 'PARENT_BATTERY_RECOVERED_ASIAN_TRUST_RUN'),
    'p2lineage_fa26c041f07e8210140ecb5c': ('institutional_trust', 'PARENT_BATTERY_RECOVERED_ASIAN_TRUST_RUN'),
    'p2lineage_ba47f2cfd302d285c935d00e': ('institutional_trust', 'PARENT_BATTERY_RECOVERED_ASIAN_TRUST_RUN'),
    'p2lineage_e980d7a74bf489ca55d06cce': ('institutional_trust', 'PARENT_BATTERY_RECOVERED_ASIAN_TRUST_RUN'),
}

# Target recognition is deliberately ordered from narrower to broader targets.
TARGET_PATTERNS: list[tuple[str, list[str]]] = [
    ('police_assistance_service', [r'help from (?:the )?pol(?:ice|lice)', r'assistance from public security']),
    ('primary_school_access', [r'place in a public primary school', r'admission in a govt\.? primary school', r'public primary-school registration']),
    ('medical_treatment_access', [r'appropriate medical treatment', r'medical treatment at', r'obtain.*medical treatment', r'nearby clinic']),
    ('identity_document_access', [r'identity documents?', r'\bid card\b', r'receiving id']),
    ('tax_obligation_information', [r'what taxes and fees.*supposed to pay']),
    ('public_revenue_information', [r'how government uses the revenues']),
    ('ethnic_identity', [r'ethnic community', r'cultural group']),
    ('mother_tongue', [r'mother tongue']),
    ('election_commission', [r'electoral commission', r'election commission', r'commission.*election']),
    ('election_process', [r'trust.*election(?! commission)', r'confidence.*election(?! commission)', r'^elections?$', r'elections? (?:are|is|makes|make|conducted|free|fair)']),
    ('courts_and_legal_system', [r'courts?/legal system', r'courts? and legal system']),
    ('american_courts', [r'american courts']),
    ('courts', [r'court(?:s| of law)?', r'judiciar']),
    ('police_station', [r'police station']),
    ('police', [r'\bpolice\b', r'public security']),
    ('military_governing_council', [r'supreme council of the armed forces']),
    ('army', [r'\barmy\b', r'armed forces', r'\bmilitary\b']),
    ('parliament_member', [r'local mp', r'member of parliament']),
    ('shura_council', [r'shura council']),
    ('parliament', [r'\bparliament\b', r'\bcongress\b', r'council of representatives', r'national assembly', r'legislature']),
    ('tribal_leaders', [r'tribal leaders?']),
    ('religious_leaders', [r'religious leaders?', r'clergy']),
    ('religious_institutions', [r'church(?:es)?', r'religious institutions?', r'mosque']),
    ('muslim_brotherhood', [r'muslim brotherhood']),
    ('al_nahda', [r'al-nahda']),
    ('main_shia_party', [r'main shia party']),
    ('main_sunni_party', [r'main sunni party']),
    ('ruling_party', [r'ruling party']),
    ('opposition_parties', [r'opposition political parties?', r'opposition part']),
    ('political_parties', [r'political parties?', r'political party']),
    ('civil_service', [r'civil service', r'civil servants?', r'public administration']),
    ('justice_system', [r'justice system', r'legal system']),
    ('health_system', [r'health care system', r'healthcare system', r'health system']),
    ('education_system', [r'education system']),
    ('social_security_system', [r'social security system']),
    ('united_nations', [r'united nations']),
    ('european_union', [r'european union']),
    ('nato', [r'\bnato\b']),
    ('named_trade_union', [r'tunisian general union for labor']),
    ('trade_unions', [r'trade unions?', r'labor union', r'general union for labor']),
    ('financial_system', [r'banks and the financial system']),
    ('companies', [r'major companies', r'foreign investors']),
    ('local_government', [r'local government', r'local go$', r'municipal', r'district assembly', r'local council']),
    ('tax_department', [r'tax department']),
    ('cabinet', [r'government \(the cabinet\)', r'government \(council of ministers\)', r'council of ministers', r'\bcabinet\b']),
    ('head_of_state_or_government', [r'president/prime minister', r'executive office \(president or prime minister\)', r'excutive office \(president or prime minister\)']),
    ('head_of_government', [r'prime minister']),
    ('president', [r'\bpresident\b']),
    ('national_government', [r'national government', r'central government']),
    ('government_administration', [r'government administrators?', r'government officials?', r'people who run our government']),
    ('government_unspecified_scope', [r'^the government$', r'^government$', r'confidence in government$', r'trust.*government$', r'how much confidence.*government']),
    ('social_media', [r'social media', r'facebook', r'twitter']),
    ('internet_news', [r'news on the internet', r'internet news', r'online media']),
    ('television', [r'television', r'\btv\b']),
    ('newspapers', [r'newspaper', r'print media']),
    ('local_media', [r'local media']),
    ('media_general', [r'\bmedia\b', r'press']),
    ('co_resident_family', [r'family living with you', r'family.*living with you']),
    ('relatives', [r'relatives?', r'extended family']),
    ('family', [r'\bfamily\b']),
    ('neighbors', [r'neighbou?r']),
    ('online_acquaintances', [r'only met online', r'people.*online']),
    ('known_people', [r'people you know', r'known personally', r'acquaintance']),
    ('strangers', [r'strangers?', r'first time', r'do not know', r'unknown people']),
    ('other_religion', [r'other religions?', r'different religion']),
    ('other_nationality', [r'other nationalit', r'foreigners?', r'immigrants?']),
    ('fellow_citizens', [r'fellow citizens?', r'other \[[^]]+\]', r'other kenyans', r'other people in (?:this|your) country']),
    ('general_people', [r'most people', r'can people be trusted', r'people can be trusted', r'people can or cannot be trusted', r'people can be trusted/can', r'trust in people$', r'trust in others', r'general trust', r'people are trustworthy', r'people in general']),
    ('doctors', [r'doctors? judgment', r'\bdoctors?\b']),
    ('business', [r'business(?:es)?', r'private companies', r'industry']),
    ('ngo', [r'non-government', r'\bngo']),
]

NONTRUST_PATTERNS: list[tuple[str, list[str]]] = [
    ('membership_participation', [r'are you a member', r'member of or do you attend', r'member of or participant', r'name of the organization you belong', r'belong to']),
    ('service_access_difficulty', [r'easy or difficult.*obtain', r'difficult or easy.*obtain', r'access to', r'get the following information', r'could get the following information']),
    ('public_service_problem', [r'encountered any of these problems', r'long waiting time', r'lack of medicines']),
    ('institutional_performance', [r'evaluate the performance', r'doing enough', r'performance of']),
    ('corruption_perception', [r'involved in corruption', r'corrupt']),
    ('bribery_experience', [r'pay a bribe', r'give a gift.*favour', r'unofficial payments']),
    ('respectful_treatment', [r'treat you with respect']),
    ('social_distance', [r'would (?:not )?like.*neighbou?r', r'dislike.*neighbou?r']),
    ('government_support_benefit', [r'getting support / benefit from the government', r'receiv.*government benefit']),
    ('news_use_frequency', [r'how often do you get news', r'news from the following sources']),
    ('information_channel', [r'most important channel.*information']),
    ('information_withholding', [r'withhold important information']),
    ('climate_action_evaluation', [r'limit climate change', r'climate change']),
    ('representation_scope', [r'government represents all or just one group']),
    ('political_efficacy', [r'influence over what the government does', r'politics and government seems so complicated']),
    ('democratic_institution_requirement', [r'essential for democratic society', r'at least 2 parties competing', r'without political parties']),
    ('listening_responsiveness', [r'try their best to listen', r'responsive to people']),
    ('unfair_treatment', [r'treated unfairly']),
    ('contact_exposure', [r'past 12 months have you had contact', r'contacted a government official']),
    ('knowledge_identification', [r'can you tell me the name']),
    ('importance_ranking', [r'which .* most important']),
    ('social_connection_resource', [r'enough friends and connections.*get help']),
    ('social_ties_identity', [r'feel strong ties', r'how close do you feel']),
    ('long_term_orientation', [r'long-term relationship', r'temporary gains and losses']),
    ('government_responsibility_assignment', [r'primary responsibility', r'who should be responsible']),
    ('marriage_social_distance', [r'family member marry']),
    ('identity_recognition', [r'think of me as', r'ethnic community or cultural group', r'mother tongue']),
    ('verbatim_reason', [r'\(verbatim\)', r'reason for not reporting']),
    ('household_asset_or_service', [r'do you or any member of your family have', r'deposit in national or foreign currency']),
    ('moved_with_relatives', [r'moved in with relatives']),
    ('party_metadata', [r'party name', r'party preference.*name', r'party name abbreviation']),
    ('external_index', [r'\[v-dem', r'bertelsmann', r'global party survey']),
    ('satisfaction_evaluation', [r'satisfation with', r'satisfied']),
    ('security_privacy_evaluation', [r'security of sharing private information']),
    ('issue_or_problem_identification', [r'which of the following problems', r'biggest environmental challenges']),
    ('normative_justifiability', [r'never justified', r'always justified']),
    ('government_right_action_expectation', [r'trust the people who run our government to do what is right']),
]


def target_from_text(text: str) -> str:
    text = norm(text)
    for target, patterns in TARGET_PATTERNS:
        if any(re.search(pattern, text) for pattern in patterns):
            return target
    return 'unspecified_target'


def target_set(texts: list[str]) -> list[str]:
    return unique(target_from_text(text) for text in texts if norm(text))


def classify_lineage(
    lineage_id: str,
    texts: list[str],
    response_families: list[str],
    semantic_subroles: list[str],
) -> tuple[str, str, str, str, list[str]]:
    combined = norm(' || '.join(texts))
    targets = target_set(texts)

    for axis, patterns in NONTRUST_PATTERNS:
        if any(re.search(pattern, combined) for pattern in patterns):
            target = targets[0] if len(targets) == 1 else ('heterogeneous_target_lineage' if len(targets) > 1 else 'unspecified_target')
            return axis, target, 'EXPLICIT_NONTRUST_OPERATOR', 'HIGH', targets

    response_authorizes_trust = any(
        'trust' in norm(value) or 'confidence' in norm(value)
        for value in response_families
    ) or any(
        'institutional_trust' in norm(value) or 'trust_confidence' in norm(value)
        for value in semantic_subroles
    )
    explicit_trust = bool(re.search(r'\btrust\b|\btrusted\b|\btrustworthy\b|\bconfidence\b', combined))
    override_axis = OVERRIDE_AXES.get(lineage_id)

    if explicit_trust or response_authorizes_trust or override_axis:
        if len(targets) > 1:
            return 'trust_target_heterogeneous', 'heterogeneous_target_lineage', 'SOURCE_LOCAL_LINEAGE_CONTAINS_MATERIALLY_DIFFERENT_TARGETS', 'LOW', targets
        target = targets[0] if targets else 'unspecified_target'
        if re.search(r'more trust .*social media.*than.*traditional media', combined):
            return 'comparative_media_trust', target, 'EXPLICIT_COMPARATIVE_MEDIA_TRUST_PROPOSITION', 'HIGH', targets
        if override_axis:
            axis, basis = override_axis
            if target == 'unspecified_target':
                return 'trust_unspecified', target, f'{basis}_TARGET_UNRESOLVED', 'LOW', targets
            return axis, target, basis, 'HIGH', targets
        if target == 'general_people' or (target == 'fellow_citizens' and re.search(r'most people|careful in dealing with people', combined)):
            return 'generalized_social_trust', target, 'EXPLICIT_GENERALIZED_TRUST_PROPOSITION', 'HIGH', targets
        if target in {'relatives', 'family', 'co_resident_family', 'neighbors', 'known_people', 'online_acquaintances', 'strangers', 'other_religion', 'other_nationality', 'fellow_citizens'}:
            return 'interpersonal_trust', target, 'EXPLICIT_INTERPERSONAL_TRUST_PROPOSITION', 'HIGH', targets
        if target in {'social_media', 'internet_news', 'television', 'newspapers', 'local_media', 'media_general'}:
            return 'media_trust', target, 'EXPLICIT_MEDIA_TRUST_PROPOSITION', 'HIGH', targets
        if target != 'unspecified_target':
            return 'institutional_trust', target, 'EXPLICIT_OR_PARENT_AUTHORIZED_INSTITUTIONAL_TRUST_PROPOSITION', 'HIGH', targets
        return 'trust_unspecified', target, 'TRUST_OPERATOR_OR_RESPONSE_CONTRACT_TARGET_UNRESOLVED', 'LOW', targets

    if combined:
        target = targets[0] if len(targets) == 1 else ('heterogeneous_target_lineage' if len(targets) > 1 else 'unspecified_target')
        return 'nontrust_other', target, 'EXACT_TEXT_EXCLUDES_TRUST_OPERATOR_OTHER_DOMAIN_UNADJUDICATED', 'MEDIUM', targets
    return 'unresolved_axis', 'unspecified_target', 'NO_EXPLICIT_OR_GOVERNED_PARENT_OPERATOR', 'LOW', targets


classification_rows = []
for _, lineage in lineage_surface.iterrows():
    evidence = node_groups[lineage.lineage_id]
    question_ids = evidence.question_implementation_id.tolist()
    structure_ids = unique(
        structure_id
        for question_id in question_ids
        for structure_id in structures_by_question.get(question_id, [])
    )
    structure_labels = unique(structure_by_id.loc[structure_id].structure_label for structure_id in structure_ids)
    texts = unique(evidence.exact_question_text.tolist())
    variables = unique(evidence.source_variable_code.tolist())
    response_families = unique(evidence.response_family_expectation.tolist())
    semantic_subroles = unique(evidence.semantic_subrole.tolist())
    measurement_class = (
        'DERIVED_INDEX'
        if any('context_index' in norm(value) for value in response_families)
        or any(re.search(r'welzel|inverse trust', norm(value)) for value in texts)
        else 'SOURCE_QUESTION_OR_BATTERY_ITEM'
    )
    axis, target, basis, confidence, observed_targets = classify_lineage(
        lineage.lineage_id, texts, response_families, semantic_subroles
    )
    unresolved = axis in {'unresolved_axis', 'trust_unspecified', 'trust_target_heterogeneous'} or (axis in {'generalized_social_trust', 'interpersonal_trust', 'institutional_trust', 'media_trust', 'comparative_media_trust'} and target in {'unspecified_target', 'heterogeneous_target_lineage'})
    classification_rows.append({
        'trust_lineage_classification_id': stable_id('p2trustclassv2', lineage.lineage_id),
        'lineage_id': lineage.lineage_id,
        'source_family': lineage.source_family,
        'member_count': lineage.member_count,
        'variables_json': json_compact(variables),
        'waves_json': json_compact(unique(evidence.wave.tolist())),
        'exact_question_texts_json': json_compact(texts),
        'response_options_json': json_compact(unique(evidence.response_options_substantive.tolist())),
        'response_topologies_json': json_compact(unique(evidence.response_topology.tolist())),
        'response_family_expectations_json': json_compact(response_families),
        'semantic_content_ids_json': json_compact(unique(evidence.semantic_content_id.tolist())),
        'source_structure_ids_json': json_compact(structure_ids),
        'source_structure_labels_json': json_compact(structure_labels),
        'observed_exact_text_targets_json': json_compact(observed_targets),
        'governed_relation_axis': axis,
        'governed_target_entity': target,
        'classification_basis': basis,
        'classification_confidence': confidence,
        'measurement_class': measurement_class,
        'authority_status': ('P2_TRUST_LINEAGE_CLASSIFICATION_UNRESOLVED' if unresolved else ('P2_TRUST_LINEAGE_AXIS_TARGET_CLASSIFIED' if axis in {'generalized_social_trust', 'interpersonal_trust', 'institutional_trust', 'media_trust', 'comparative_media_trust'} else 'P2_NONTRUST_EXCLUSION_CLASSIFIED')),
        'prohibited_use': 'Discovery and pair-adjudication coordinate only; no J-family membership or value portability.',
    })

classification = pd.DataFrame(classification_rows).sort_values(['source_family', 'lineage_id'])
classification_path = OUT / 'Rawlsing_P2_Trust_Lineage_Axis_Target_Classification_v2.csv'
classification.to_csv(classification_path, index=False)
classification_by_lineage = classification.set_index('lineage_id')

TRUST_AXES = {
    'generalized_social_trust', 'interpersonal_trust', 'institutional_trust',
    'media_trust', 'comparative_media_trust',
}

# Relations that preserve a shared conceptual coordinate but not proposition identity.
NESTED_OR_FUNCTIONAL_TARGET_PAIRS = {
    frozenset({'family', 'co_resident_family'}),
    frozenset({'political_parties', 'opposition_parties'}),
    frozenset({'political_parties', 'ruling_party'}),
    frozenset({'general_people', 'fellow_citizens'}),
    frozenset({'courts', 'american_courts'}),
    frozenset({'courts', 'courts_and_legal_system'}),
    frozenset({'police', 'police_station'}),
    frozenset({'army', 'military_governing_council'}),
    frozenset({'parliament', 'shura_council'}),
    frozenset({'parliament', 'parliament_member'}),
    frozenset({'trade_unions', 'named_trade_union'}),
    frozenset({'national_government', 'government_unspecified_scope'}),
    frozenset({'national_government', 'cabinet'}),
    frozenset({'government_unspecified_scope', 'cabinet'}),
    frozenset({'national_government', 'head_of_government'}),
    frozenset({'national_government', 'head_of_state_or_government'}),
    frozenset({'government_unspecified_scope', 'head_of_government'}),
    frozenset({'government_unspecified_scope', 'head_of_state_or_government'}),
    frozenset({'cabinet', 'head_of_government'}),
    frozenset({'cabinet', 'head_of_state_or_government'}),
    frozenset({'head_of_government', 'head_of_state_or_government'}),
    frozenset({'president', 'head_of_state_or_government'}),
}


def target_coordinate_relation(left_target: str, right_target: str) -> bool:
    return frozenset({left_target, right_target}) in NESTED_OR_FUNCTIONAL_TARGET_PAIRS


ruling_rows = []
for _, candidate in trust_queue.iterrows():
    left = classification_by_lineage.loc[candidate.left_lineage_id]
    right = classification_by_lineage.loc[candidate.right_lineage_id]
    left_axis, right_axis = left.governed_relation_axis, right.governed_relation_axis
    left_target, right_target = left.governed_target_entity, right.governed_target_entity

    if left.authority_status.endswith('UNRESOLVED') or right.authority_status.endswith('UNRESOLVED'):
        status = 'UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_RELATION_AXIS_OR_TARGET_EVIDENCE'
        relation_type = 'UNRESOLVED'
        ceiling = 'NO_AUTHORITY'
        rationale = 'At least one source-local lineage lacks a single governed proposition operator or target; heterogeneous source-local continuity cannot be exported cross-source.'
    elif left_axis in TRUST_AXES and right_axis in TRUST_AXES:
        if left_axis == right_axis and left_target == right_target:
            if 'DERIVED_INDEX' in {left.measurement_class, right.measurement_class}:
                status = 'ACCEPTED_TRUST_CONSTRUCT_COORDINATE_WITH_DERIVED_INDEX'
                relation_type = 'DERIVED_INDEX_CONSTRUCT_COORDINATE'
                ceiling = 'DERIVED_INDEX_CONSTRUCT_ONLY'
                rationale = 'The trust construct and target agree, but a derived inverse/index measure cannot inherit question wording or response-topology authority.'
            else:
                status = 'ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION'
                relation_type = 'REWORDED_PROPOSITION_EQUIVALENCE'
                left_topologies = set(json.loads(left.response_topologies_json))
                right_topologies = set(json.loads(right.response_topologies_json))
                ceiling = (
                    'QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY'
                    if left_topologies == right_topologies and len(left_topologies) == 1
                    else 'QUESTION_PROPOSITION_ONLY'
                )
                rationale = 'Both exact lineages assert the same governed trust relation toward the same canonical target.'
        elif left_target == right_target and left_axis != right_axis:
            status = 'ACCEPTED_TRUST_CONSTRUCT_OR_TARGET_COORDINATE_ONLY'
            relation_type = 'TRUST_CONSTRUCT_COORDINATE_ONLY'
            ceiling = 'TARGET_AND_TRUST_DOMAIN_COORDINATE_ONLY'
            rationale = 'The target agrees, but the trust operators differ—for example absolute versus comparative media trust—and proposition equivalence is prohibited.'
        elif left_axis == right_axis and target_coordinate_relation(left_target, right_target):
            status = 'ACCEPTED_NESTED_OR_FUNCTIONAL_TRUST_TARGET_COORDINATE_ONLY'
            relation_type = 'TARGET_RELATION_COORDINATE_ONLY'
            ceiling = 'TARGET_AND_RELATION_COORDINATE_ONLY'
            rationale = 'The trust operator is shared, but one target is narrower, role-specific, jurisdiction-specific, or functionally adjacent; proposition equivalence is prohibited.'
        else:
            status = 'REJECTED_FALSE_EQUIVALENCE_TARGET_OR_TRUST_AXIS_MISMATCH'
            relation_type = 'NEGATIVE_AUTHORITY'
            ceiling = 'NO_EQUIVALENCE'
            rationale = 'The exact lineages differ in governed trust relation, canonical target, or both.'
    elif left_axis not in TRUST_AXES and right_axis not in TRUST_AXES:
        if left_axis == right_axis and left_target == right_target and left_axis not in {'unresolved_axis', 'trust_unspecified', 'nontrust_other'} and left_target not in {'unspecified_target', 'heterogeneous_target_lineage'}:
            status = 'ACCEPTED_NONTRUST_RELATION_REDIRECTED_FROM_CONTAMINATED_TRUST_NEIGHBORHOOD'
            relation_type = 'REWORDED_PROPOSITION_EQUIVALENCE'
            ceiling = 'QUESTION_PROPOSITION_ONLY'
            rationale = 'The inherited trust neighborhood is wrong, but both exact lineages assert the same non-trust relation and target.'
        elif 'nontrust_other' in {left_axis, right_axis} or left_target in {'unspecified_target', 'heterogeneous_target_lineage'} or right_target in {'unspecified_target', 'heterogeneous_target_lineage'}:
            status = 'REDIRECTED_OUT_OF_TRUST_NEIGHBORHOOD_OTHER_DOMAIN_NOT_ADJUDICATED'
            relation_type = 'OTHER_DOMAIN_REVIEW_REQUIRED'
            ceiling = 'NO_TRUST_AUTHORITY'
            rationale = 'Exact evidence excludes a trust relation, but this tranche does not manufacture authority for the items’ proper non-trust domain.'
        else:
            status = 'REJECTED_CONTAMINATED_TRUST_NEIGHBORHOOD_NONTRUST_MISMATCH'
            relation_type = 'NEGATIVE_AUTHORITY'
            ceiling = 'NO_EQUIVALENCE'
            rationale = 'Both items are outside trust and do not share the same governed relation and target.'
    else:
        status = 'REJECTED_TRUST_VERSUS_NONTRUST_OPERATOR_MISMATCH'
        relation_type = 'NEGATIVE_AUTHORITY'
        ceiling = 'NO_EQUIVALENCE'
        rationale = 'One lineage asserts trust while the other asserts access, performance, membership, corruption, social distance, or another relation.'

    ruling_id = stable_id('p2trustrulingv2', candidate.semantic_pair_candidate_id)
    ruling_rows.append({
        'trust_pair_ruling_id': ruling_id,
        'semantic_pair_candidate_id': candidate.semantic_pair_candidate_id,
        'semantic_content_id': candidate.semantic_content_id,
        'left_source_family': candidate.left_source_family,
        'right_source_family': candidate.right_source_family,
        'left_lineage_id': candidate.left_lineage_id,
        'right_lineage_id': candidate.right_lineage_id,
        'left_relation_axis': left_axis,
        'right_relation_axis': right_axis,
        'left_target_entity': left_target,
        'right_target_entity': right_target,
        'authority_status': status,
        'relation_type': relation_type,
        'portability_ceiling': ceiling,
        'rationale': rationale,
        'left_classification_id': left.trust_lineage_classification_id,
        'right_classification_id': right.trust_lineage_classification_id,
        'two_sided_evidence_status': 'EXPLICIT_LINEAGE_NODE_RESPONSE_AND_STRUCTURE_PROVENANCE_BOTH_SIDES',
        'prohibited_use': 'No value harmonization, respondent join, or J-family authority follows from this ruling.',
    })

rulings = pd.DataFrame(ruling_rows)
rulings_path = OUT / 'Rawlsing_P2_Trust_Neighborhood_Pair_Rulings_v2.csv'
rulings.to_csv(rulings_path, index=False)

# Two-sided evidence ledger bound directly to each ruling and its recorded ceiling.
evidence_rows = []
for _, ruling in rulings.iterrows():
    for side in ('left', 'right'):
        lineage_id = ruling[f'{side}_lineage_id']
        classification_row = classification_by_lineage.loc[lineage_id]
        lineage_nodes = node_groups[lineage_id]
        evidence_rows.append({
            'trust_evidence_record_id': stable_id('p2trustevidencev2', ruling.trust_pair_ruling_id, side),
            'trust_pair_ruling_id': ruling.trust_pair_ruling_id,
            'semantic_pair_candidate_id': ruling.semantic_pair_candidate_id,
            'side': side.upper(),
            'lineage_id': lineage_id,
            'source_family': classification_row.source_family,
            'classification_id': classification_row.trust_lineage_classification_id,
            'governed_relation_axis': classification_row.governed_relation_axis,
            'governed_target_entity': classification_row.governed_target_entity,
            'observed_exact_text_targets_json': classification_row.observed_exact_text_targets_json,
            'question_implementation_ids_json': json_compact(lineage_nodes.question_implementation_id.tolist()),
            'wave_variable_locators_json': json_compact([
                {'wave': item.wave, 'variable': item.source_variable_code, 'source_row_index': item.source_row_index}
                for _, item in lineage_nodes.iterrows()
            ]),
            'exact_question_texts_json': classification_row.exact_question_texts_json,
            'response_options_json': classification_row.response_options_json,
            'response_topologies_json': classification_row.response_topologies_json,
            'response_family_expectations_json': classification_row.response_family_expectations_json,
            'source_structure_ids_json': classification_row.source_structure_ids_json,
            'source_structure_labels_json': classification_row.source_structure_labels_json,
            'classification_basis': classification_row.classification_basis,
            'classification_confidence': classification_row.classification_confidence,
            'measurement_class': classification_row.measurement_class,
            'evidence_sufficiency': (
                'COMPLETE_FOR_RECORDED_CEILING'
                if classification_row.authority_status.endswith('CLASSIFIED')
                else 'INCOMPLETE_OR_HETEROGENEOUS_OPERATOR_OR_TARGET'
            ),
        })

evidence = pd.DataFrame(evidence_rows)
evidence_path = OUT / 'Rawlsing_P2_Trust_Neighborhood_Two_Sided_Evidence_Ledger_v2.csv'
evidence.to_csv(evidence_path, index=False)

remaining = queue[~queue.semantic_pair_candidate_id.isin(set(trust_queue.semantic_pair_candidate_id))].copy()
remaining_path = OUT / 'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Trust_Tranche_v3.csv'
remaining.to_csv(remaining_path, index=False)

summary = {
    'contract_version': 'P2_TRUST_NEIGHBORHOOD_ADJUDICATION_V2',
    'input_pending_pair_rows': int(len(queue)),
    'trust_domain_pair_rows_adjudicated': int(len(rulings)),
    'remaining_pair_rows': int(len(remaining)),
    'trust_domain_lineages_classified': int(len(classification)),
    'lineage_classification_status_counts': {str(k): int(v) for k, v in classification.authority_status.value_counts().sort_index().items()},
    'lineage_relation_axis_counts': {str(k): int(v) for k, v in classification.governed_relation_axis.value_counts().sort_index().items()},
    'pair_authority_status_counts': {str(k): int(v) for k, v in rulings.authority_status.value_counts().sort_index().items()},
    'pair_relation_type_counts': {str(k): int(v) for k, v in rulings.relation_type.value_counts().sort_index().items()},
    'semantic_id_counts': {str(k): int(v) for k, v in rulings.semantic_content_id.value_counts().sort_index().items()},
    'evidence_rows': int(len(evidence)),
    'evidence_rows_expected': int(2 * len(rulings)),
    'all_input_trust_pairs_partitioned': len(rulings) == len(trust_queue),
    'remaining_queue_partition_exact': len(remaining) + len(rulings) == len(queue),
    'accepted_proposition_rows_require_exact_axis_and_target': bool(
        ((rulings.authority_status != 'ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION') |
         ((rulings.left_relation_axis == rulings.right_relation_axis) &
          (rulings.left_target_entity == rulings.right_target_entity))).all()
    ),
    'authority_boundary': 'PAIR_RELATION_AUTHORITY_ONLY_NO_J_FAMILY_NO_VALUE_HARMONIZATION',
}
summary_path = OUT / 'TRUST_ADJUDICATION_RETURN_V2.json'
summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps(summary, indent=2, ensure_ascii=False))
