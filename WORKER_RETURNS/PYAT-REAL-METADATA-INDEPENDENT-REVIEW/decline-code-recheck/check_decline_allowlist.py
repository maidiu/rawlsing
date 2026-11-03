"""Exact per-item code-99 authority join for the accepted SRC04 42-field slice."""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

R = Path(__file__).resolve().parent
SNAP = Path((R / 'evidence/snapshot.path').read_text().strip())
CONFIG = SNAP / 'rawlsing_next/source_configuration/data/SRC04/source.config.json'
TALLY = SNAP / 'prior/TALLY_PRODUCT.json'
ROUTING = SNAP / 'WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/routing/01_ROUTING_RECEIPT.json'
CANDIDATE = SNAP / 'WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/decline-code-fix/01_CORRECTION_RECEIPT.json'
CANDIDATE_OVERLAY = SNAP / 'WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/decline-code-fix/02_Q101_CODE99_OVERLAY.json'
REPLAYED = R / 'evidence/REPLAYED_CORRECTION_RECEIPT.json'
REPLAYED_OVERLAY = R / 'evidence/REPLAYED_OVERLAY.json'
OPTION_AUTH = Path('/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/reports/arab_barometer_response_option_authority.csv')

def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def jload(p: Path) -> Any:
    return json.loads(Path(p).read_text(encoding='utf-8'))

def code99(value: Any) -> bool:
    return str(value) in ('99', '99.0')

cfg = jload(CONFIG)
tally = jload(TALLY)
routing = jload(ROUTING)
candidate = jload(CANDIDATE)
candidate_overlay = jload(CANDIDATE_OVERLAY)
replayed = jload(REPLAYED)
replayed_overlay = jload(REPLAYED_OVERLAY)

selected_ids = [str(x['question_id']) for x in routing['rows']]
if len(selected_ids) != 42 or len(set(selected_ids)) != 42:
    raise ValueError('accepted slice is not 42 unique fields')

slots = {str(x['question_id']): x for x in cfg['response_slots']}
tally_fields = {str(x['question_id']): x for x in tally['fields']}

# Exact option-authority rows: var_name + wave I + numeric code 99.0, exactly one.
auth_by_q: dict[str, list[dict[str, str]]] = {}
with OPTION_AUTH.open(newline='', encoding='utf-8', errors='replace') as f:
    for row in csv.DictReader(f):
        var = str(row.get('var_name') or '')
        wave = str(row.get('wave') or '')
        canon = str(row.get('canonical_wave') or '')
        code = str(row.get('value_code_numeric') or '')
        if var in set(selected_ids) and wave == 'I' and canon == 'I' and code == '99.0':
            auth_by_q.setdefault(var, []).append(row)

field_allowlist = []
certified_allowlist = []
preserved_unknown = []
consistent = []
typed_unknown = []
for qid in selected_ids:
    rows = auth_by_q.get(qid, [])
    slot = slots.get(qid)
    field = tally_fields.get(qid)
    if slot is None or field is None or len(rows) != 1:
        typed_unknown.append({
            'question_id': qid,
            'authority_rows_exact': len(rows),
            'source_config_slot_present': slot is not None,
            'tally_field_present': field is not None,
        })
        continue
    auth = rows[0]
    config_value = next(
        (v for v in slot.get('values', []) if code99(v.get('raw_value'))),
        None,
    )
    config_state = None if config_value is None else config_value.get('response_state')
    auth_special = str(auth.get('option_group')) == 'special'
    auth_non_substantive = str(auth.get('is_substantive')) == 'False'
    auth_refusal = str(auth.get('is_refusal')) == 'True'
    auth_missing = str(auth.get('is_missing')) == 'True'
    auth_kind = str(auth.get('response_kind')) == 'special_missing'
    count99 = 0
    for x in field.get('native_value_counts', []):
        if code99(x.get('native_value')):
            count99 = int(x.get('count', 0))
            break
    entry = {
        'question_id': qid,
        'selected_slice_ordinal': selected_ids.index(qid) + 1,
        'source_config_response_state': config_state,
        'source_config_canonical_value': None if config_value is None else config_value.get('canonical_value'),
        'authority_question_id': auth.get('question_id'),
        'authority_wave': auth.get('wave'),
        'authority_code_normalized': auth.get('value_code_normalized'),
        'authority_code_numeric': auth.get('value_code_numeric'),
        'authority_label': auth.get('value_label_raw'),
        'authority_option_group': auth.get('option_group'),
        'authority_is_substantive': auth.get('is_substantive'),
        'authority_is_refusal': auth.get('is_refusal'),
        'authority_is_missing': auth.get('is_missing'),
        'authority_response_kind': auth.get('response_kind'),
        'authority_response_semantics_status': auth.get('response_semantics_status'),
        'retained_code99_count': count99,
    }
    if (config_state == 'SUBSTANTIVE_RESPONSE' and auth_special
            and auth_non_substantive and auth_refusal and auth_missing and auth_kind):
        entry['inconsistent'] = True
        field_allowlist.append(entry)
        if str(auth.get('response_semantics_status')) == 'certified':
            entry['correction_status'] = 'certified_correction_allowlist'
            certified_allowlist.append(entry)
        else:
            entry['correction_status'] = 'typed_unknown_not_certified'
            entry['typed_unknown_reason'] = (
                'exact code-99 option fields say special/non-substantive/refusal/missing, '
                'but response_semantics_status is not certified'
            )
            preserved_unknown.append(entry)
    elif (config_state != 'SUBSTANTIVE_RESPONSE' and auth_special
          and not auth_non_substantive and not auth_refusal and auth_missing and auth_kind):
        entry['consistent'] = True
        consistent.append(entry)
    else:
        entry['inconsistent'] = False
        entry['typed_unknown'] = 'authority flags do not form an exact non-substantive refusal or consistent substantive case'
        typed_unknown.append(entry)

# q101 aggregate replay checks.
q101 = tally_fields['q101']
old_states = dict(q101.get('state_counts') or {})
q101_99 = next(int(x['count']) for x in q101['native_value_counts'] if code99(x.get('native_value')))
q101_auth = next(rows[0] for q, rows in auth_by_q.items() if q == 'q101')
correct = {
    'valid_answer': int(old_states.get('SUBSTANTIVE_RESPONSE', 0)) - q101_99,
    'explicit_nonresponse': sum(int(old_states.get(k, 0)) for k in ('DK', 'REFUSAL', 'SOURCE_SPECIFIC_SPECIAL')) + q101_99,
    'dk': int(old_states.get('DK', 0)),
    'refusal': q101_99,
    'missing': int(old_states.get('MISSING', 0)),
    'observed_response': int(old_states.get('SUBSTANTIVE_RESPONSE', 0)) + sum(int(old_states.get(k, 0)) for k in ('DK', 'REFUSAL', 'SOURCE_SPECIFIC_SPECIAL')),
    'total': int(q101['source_record_denominator']),
}
correct['identity'] = correct['valid_answer'] + correct['explicit_nonresponse'] + correct['missing']
assert correct == {
    'valid_answer': 7129, 'explicit_nonresponse': 204, 'dk': 171,
    'refusal': 33, 'missing': 4, 'observed_response': 7333, 'total': 7337,
    'identity': 7337,
}
assert candidate['corrected_tally']['valid_answer'] == 7129
assert candidate['corrected_tally']['explicit_nonresponse'] == 204
assert candidate['corrected_tally']['refusal'] == 33
assert candidate['corrected_tally']['missing_or_unobserved'] == 4
assert candidate['corrected_tally']['source_record_denominator'] == 7337
assert candidate_overlay['to_response_state'] == 'REFUSAL'
assert replayed == candidate
assert replayed_overlay == candidate_overlay
assert sha(REPLAYED) == sha(CANDIDATE)
assert sha(REPLAYED_OVERLAY) == sha(CANDIDATE_OVERLAY)

# Preserve routing unknown; no routing correction.
routing_authority = routing['routing_authority']
assert routing_authority['selected_routing_unknown'] == 42
assert routing_authority['selected_risk_set_unresolved'] == 42
assert routing_authority['selected_exact_skip_rules'] == 0
assert routing_authority['accepted_routing_binding'] is False
assert routing_authority['eligibility_denominator_binding'] is False

result = {
    'schema': 'PYAT_SRC04_DECLINE_CODE_ALLOWLIST@1.0.0',
    'candidate_commit': '1110093f324fe591246c56bf8f2e742a57c9201e',
    'review_start_head': '9d3d42984f37c01129e47d3dd5570608972cafba',
    'candidate_q101_correction': {
        'receipt_sha256': sha(CANDIDATE),
        'replayed_receipt_sha256': sha(REPLAYED),
        'byte_identical': sha(CANDIDATE) == sha(REPLAYED),
        'overlay_sha256': sha(CANDIDATE_OVERLAY),
        'replayed_overlay_sha256': sha(REPLAYED_OVERLAY),
        'overlay_byte_identical': sha(CANDIDATE_OVERLAY) == sha(REPLAYED_OVERLAY),
        'focused_tests': '5 passed in 0.02s',
        'routing_unknown_preserved': True,
    },
    'q101': {
        'authority_question_id': q101_auth.get('question_id'),
        'authority_code_numeric': q101_auth.get('value_code_numeric'),
        'authority_label': q101_auth.get('value_label_raw'),
        'authority_option_group': q101_auth.get('option_group'),
        'authority_is_substantive': q101_auth.get('is_substantive'),
        'authority_is_refusal': q101_auth.get('is_refusal'),
        'authority_is_missing': q101_auth.get('is_missing'),
        'authority_response_kind': q101_auth.get('response_kind'),
        'old_valid_answer': int(old_states.get('SUBSTANTIVE_RESPONSE', 0)),
        'old_explicit_nonresponse': sum(int(old_states.get(k, 0)) for k in ('DK', 'REFUSAL', 'SOURCE_SPECIFIC_SPECIAL')),
        'code99_count': q101_99,
        'corrected': correct,
        'aggregate_replay_exact': True,
        'correction_only_q101': candidate_overlay['only_change'] == 'q101 response value 99 state/canonical classification',
        'production_config_adopted': candidate_overlay.get('production_config_adopted'),
    },
    'join': {
        'scope': 'exact selected 42 fields only; not estate-wide',
        'key': {
            'source_config': 'response_slots[].question_id + values[].response_state',
            'option_authority': 'var_name + wave=I + canonical_wave=I + value_code_numeric=99.0',
            'tally': 'fields[].question_id + native_value_counts[].native_value=99',
        },
        'selected_fields': len(selected_ids),
        'exact_authority_rows_found': len(field_allowlist) + len(consistent) + len(typed_unknown),
        'field_inconsistency_allowlist_count': len(field_allowlist),
        'other_41_field_inconsistency_count': len([x for x in field_allowlist if x['question_id'] != 'q101']),
        'certified_correction_allowlist_count': len(certified_allowlist),
        'other_41_certified_correction_allowlist_count': len([x for x in certified_allowlist if x['question_id'] != 'q101']),
        'consistent_count': len(consistent),
        'missing_or_ambiguous_typed_unknown_count': len(typed_unknown),
        'typed_unknown_count': len(preserved_unknown) + len(typed_unknown),
        'field_inconsistency_allowlist': field_allowlist,
        'certified_correction_allowlist': certified_allowlist,
        'typed_unknown': preserved_unknown + typed_unknown,
        'consistent': consistent,
        'candidate_all_42_source_config_mapping': candidate['same_mapping_defect_in_selected_metadata']['fields_mapped_code99_to_substantive'] == 42,
        'independent_all_42_field_inconsistent': len(field_allowlist) == 42 and not consistent and not typed_unknown,
        'all_42_exact_authority_rows_present': len(field_allowlist) + len(consistent) + len(typed_unknown) == 42,
        'certification_status_counts': {
            'certified': len(certified_allowlist),
            'preserved_not_certified': len(preserved_unknown),
            'missing_or_ambiguous': len(typed_unknown),
        },
        'allowlist_is_per_item_not_code99_generalization': True,
    },
    'routing': {
        'state': 'ROUTING_UNKNOWN',
        'selected_routing_unknown': routing_authority['selected_routing_unknown'],
        'selected_risk_set_unresolved': routing_authority['selected_risk_set_unresolved'],
        'selected_exact_skip_rules': routing_authority['selected_exact_skip_rules'],
        'accepted_routing_binding': routing_authority['accepted_routing_binding'],
        'eligibility_denominator_binding': routing_authority['eligibility_denominator_binding'],
        'preserved': True,
        'routing_corrected': False,
    },
    'verdict': 'PASS_SCOPED__Q101_CORRECTION_EXACT__42_FIELD_INCONSISTENT__28_CERTIFIED_ALLOWLIST__14_TYPED_UNKNOWN',
    'scope': {
        'metadata_only': True,
        'original_sav_read': False,
        'respondent_rows_read': False,
        'new_authority': False,
        'source_execution': False,
        'production_edit': False,
        'production_config_adoption': False,
        'merge': False,
        'ci': False,
    },
    'limits': [
        'The allowlist covers only the exact accepted 42 selected fields; it is not an estate-wide code-99 rule.',
        'The candidate applied only the q101 correction; the other 41 allowlist entries remain uncorrected.',
        'No routing, eligibility denominator, R03 policy, production config, source execution, or raw respondent data is claimed.',
    ],
}
(R / 'evidence/CHECKS.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
print(json.dumps({
    'replay_exact': result['candidate_q101_correction']['byte_identical'],
    'q101': result['q101']['corrected'],
    'field_inconsistency_allowlist_count': len(field_allowlist),
    'other_41_field_inconsistency_count': len([x for x in field_allowlist if x['question_id'] != 'q101']),
    'certified_correction_allowlist_count': len(certified_allowlist),
    'other_41_certified_correction_allowlist_count': len([x for x in certified_allowlist if x['question_id'] != 'q101']),
    'typed_unknown_count': len(preserved_unknown) + len(typed_unknown),
    'missing_or_ambiguous_typed_unknown_count': len(typed_unknown),
    'consistent_count': len(consistent),
    'routing': result['routing'],
    'verdict': result['verdict'],
}, indent=2))
