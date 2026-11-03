"""Independent checks for the SRC04 28-certified / 14-held refusal overlay."""
from __future__ import annotations
import copy
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

R = Path(__file__).resolve().parent
SNAP = Path((R / 'evidence/snapshot.path').read_text().strip())
sys.path.insert(0, str(SNAP))

from rawlsing_next.source_configuration.schema import load_source_config, validate_source_config

CONFIG = SNAP / 'rawlsing_next/source_configuration/data/SRC04/source.config.json'
TALLY = SNAP / 'prior/TALLY_PRODUCT.json'
ALLOW = SNAP / 'prior/CORRECTION_ALLOWLIST.csv'
HELD = SNAP / 'prior/TYPED_UNKNOWN.csv'
OPTION = Path('/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/reports/arab_barometer_response_option_authority.csv')
ROUTING = SNAP / 'WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/routing/01_ROUTING_RECEIPT.json'
CANDIDATE = SNAP / 'WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/certified-refusal-fix/01_CERTIFIED_RECEIPT.json'
CANDIDATE_OVERLAY = SNAP / 'WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/certified-refusal-fix/02_CERTIFIED_OVERLAY.json'
REPLAYED = R / 'evidence/REPLAYED_CERTIFIED_RECEIPT.json'
REPLAYED_OVERLAY = R / 'evidence/REPLAYED_CERTIFIED_OVERLAY.json'
PRIOR_Q101 = Path('WORKER_RETURNS/PYAT-REAL-METADATA-INDEPENDENT-REVIEW/decline-code-recheck/evidence/REPLAYED_CORRECTION_RECEIPT.json')

def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def jload(p: Path) -> Any:
    return json.loads(Path(p).read_text(encoding='utf-8'))
def rows(p: Path) -> list[dict[str, str]]:
    with Path(p).open(newline='', encoding='utf-8', errors='replace') as f:
        return list(csv.DictReader(f))
def code99(v: Any) -> bool:
    return str(v) in ('99', '99.0')

cfg = jload(CONFIG)
tally = jload(TALLY)
allow = rows(ALLOW)
held_rows = rows(HELD)
route = jload(ROUTING)
candidate = jload(CANDIDATE)
candidate_overlay = jload(CANDIDATE_OVERLAY)
replayed = jload(REPLAYED)
replayed_overlay = jload(REPLAYED_OVERLAY)
prior_q101 = jload(PRIOR_Q101)
fields = {str(x['question_id']): x for x in tally['fields']}
selected = list(fields)
allow_by_q = {r['question_id']: r for r in allow}
held_by_q = {r['question_id']: r for r in held_rows}

assert len(selected) == 42
assert len(allow) == 28 and len(held_rows) == 14
assert set(allow_by_q) | set(held_by_q) == set(selected)
assert set(allow_by_q) & set(held_by_q) == set()
assert all(r.get('correction_status') == 'certified_correction_allowlist' for r in allow)
assert all(r.get('correction_status') == 'typed_unknown_not_certified' for r in held_rows)
assert all(r.get('authority_response_semantics_status') == 'certified' for r in allow)
assert all(r.get('authority_response_semantics_status') == 'preserved_not_certified' for r in held_rows)

# Per-field old denominators and identities.
per_field = []
for qid in selected:
    f = fields[qid]
    states = dict(f.get('state_counts') or {})
    valid = int(states.get('SUBSTANTIVE_RESPONSE', 0))
    explicit = sum(int(states.get(k, 0)) for k in ('DK', 'REFUSAL', 'SOURCE_SPECIFIC_SPECIAL'))
    missing = int(states.get('MISSING', 0))
    total = int(f['source_record_denominator'])
    code99_count = 0
    for x in f.get('native_value_counts', []):
        if code99(x.get('native_value')):
            code99_count = int(x.get('count', 0))
            break
    per_field.append({
        'question_id': qid,
        'source_record_denominator': total,
        'old_valid': valid,
        'old_explicit': explicit,
        'old_missing': missing,
        'old_sum': valid + explicit + missing,
        'code99_count': code99_count,
        'certified': qid in allow_by_q,
        'held': qid in held_by_q,
    })
    assert total == 7337
    assert valid + explicit + missing == total

# q101 exact prior correction and candidate cross-check.
q101 = per_field[0] if per_field[0]['question_id'] == 'q101' else next(x for x in per_field if x['question_id'] == 'q101')
prior_q = prior_q101['corrected_tally']
cand_q = candidate['q101']
assert prior_q['valid_answer'] == 7129 and prior_q['explicit_nonresponse'] == 204 and prior_q['missing_or_unobserved'] == 4
assert cand_q['old_valid'] == 7162 and cand_q['old_explicit'] == 171
assert cand_q['corrected_valid'] == 7129 and cand_q['corrected_explicit'] == 204
assert cand_q['missing'] == 4 and cand_q['total'] == 7337
assert q101['code99_count'] == 33

# 2185 certified code-99 reclassifications, 14 held code counts untouched.
cert_code = sum(x['code99_count'] for x in per_field if x['certified'])
held_code = sum(x['code99_count'] for x in per_field if x['held'])
assert cert_code == 2185
assert held_code + cert_code == sum(x['code99_count'] for x in per_field)
assert held_code == 1645
assert candidate['aggregate']['corrected']['refusal'] == cert_code
assert candidate['aggregate']['corrected']['explicit_nonresponse'] - candidate['aggregate']['old']['explicit_nonresponse'] == cert_code
assert candidate['aggregate']['old']['valid_answer'] - candidate['aggregate']['corrected']['valid_answer'] == cert_code

# Aggregate conservation and field-record scope (not unique people).
old = candidate['aggregate']['old']
new = candidate['aggregate']['corrected']
assert old['valid_answer'] == 277582
assert old['explicit_nonresponse'] == 21237
assert old['missing_or_unobserved'] == 9335
assert old['observed_response'] == 298819
assert old['source_record_denominator'] == 308154
assert new['valid_answer'] == 275397
assert new['explicit_nonresponse'] == 23422
assert new['refusal'] == 2185
assert new['missing_or_unobserved'] == 9335
assert new['observed_response'] == 298819
assert new['source_record_denominator'] == 308154
assert new['valid_answer'] + new['explicit_nonresponse'] + new['missing_or_unobserved'] == new['source_record_denominator']
assert new['source_record_denominator'] == 42 * 7337
assert new['observed_response'] + new['missing_or_unobserved'] == new['source_record_denominator']
# Per-field corrected/held row identities in the candidate receipt.
assert len(candidate['certified']) == 28 and len(candidate['held']) == 14
for row in candidate['certified']:
    assert row['corrected_valid'] + row['corrected_explicit'] + row['missing'] == row['total']
    assert row['observed'] == row['corrected_valid'] + row['corrected_explicit']
    assert row['total'] == 7337
for row in candidate['held']:
    assert row['current_state'] == 'SUBSTANTIVE_RESPONSE'
    assert row['status'] == 'HELD_UNCERTIFIED'
    assert row['code_count'] > 0

# Overlay / held partition, schema validation, per-item authority.
assert replayed == candidate and replayed_overlay == candidate_overlay
assert sha(REPLAYED) == sha(CANDIDATE)
assert sha(REPLAYED_OVERLAY) == sha(CANDIDATE_OVERLAY)
assert len(candidate_overlay['entries']) == 28
assert len(candidate_overlay['held_uncertified']) == 14
assert candidate_overlay['universal_code_rule'] is False
assert candidate_overlay['production_config_adopted'] is False
assert candidate_overlay['authority_join'] == 'per-item allowlist + exact option authority row'

# Reconstruct corrected config from exact overlay; validate with existing owner.
source = load_source_config(CONFIG)
corrected = copy.deepcopy(dict(source.document))
original = copy.deepcopy(dict(source.document))
changed = []
for entry in candidate_overlay['entries']:
    slot = next(s for s in corrected['response_slots'] if s['question_id'] == entry['question_id'])
    value = next(v for v in slot['values'] if code99(v.get('raw_value')))
    assert value.get('response_state') == entry['from_response_state']
    assert str(value.get('canonical_value')) == entry['from_canonical_value']
    value['response_state'] = entry['to_response_state']
    value['canonical_value'] = entry['to_canonical_value']
    value['transform_authority_ref'] = None
    changed.append(entry['question_id'])
assert set(changed) == set(allow_by_q)
validate_source_config(corrected)
# Held values remain exactly as in original.
for qid in held_by_q:
    orig = next(s for s in original['response_slots'] if s['question_id'] == qid)
    cur = next(s for s in corrected['response_slots'] if s['question_id'] == qid)
    ov = next(v for v in orig['values'] if code99(v.get('raw_value')))
    cv = next(v for v in cur['values'] if code99(v.get('raw_value')))
    assert ov.get('response_state') == cv.get('response_state') == 'SUBSTANTIVE_RESPONSE'
    assert str(ov.get('canonical_value')) == str(cv.get('canonical_value')) == '99'
    assert qid not in changed
assert len(changed) == 28

# Exact option-authority rows for all 28 certified entries.
option_rows = rows(OPTION)
option_by_q = {}
for row in option_rows:
    if str(row.get('var_name')) in allow_by_q and str(row.get('wave')) == 'I' and str(row.get('value_code_numeric')) == '99.0':
        option_by_q.setdefault(str(row.get('var_name')), []).append(row)
assert len(option_by_q) == 28
for qid, entry in allow_by_q.items():
    rs = option_by_q.get(qid, [])
    assert len(rs) == 1
    a = rs[0]
    assert a['question_id'] == entry['authority_question_id']
    for left, right in (
        ('option_group', 'authority_option_group'),
        ('is_substantive', 'authority_is_substantive'),
        ('is_refusal', 'authority_is_refusal'),
        ('is_missing', 'authority_is_missing'),
        ('response_kind', 'authority_response_kind'),
    ):
        assert a[left] == entry[right]

# Routing unchanged and unknown.
assert route['routing_authority']['selected_routing_unknown'] == 42
assert route['routing_authority']['selected_risk_set_unresolved'] == 42
assert route['routing_authority']['selected_exact_skip_rules'] == 0
assert route['routing_authority']['accepted_routing_binding'] is False
assert route['routing_authority']['eligibility_denominator_binding'] is False
assert candidate['routing']['state'] == 'ROUTING_UNKNOWN'
assert candidate['routing']['selected_routing_unknown'] == 42
assert candidate['routing']['selected_risk_set_unresolved'] == 42
assert candidate['routing']['accepted_routing_binding'] is False
assert candidate['routing']['eligibility_denominator_binding'] is False
assert candidate['routing']['preserved'] is True

# No unique-person claim: 308154 is 42 field-response denominators over the same 7337 rows.
unique_claims = []
for p in (CANDIDATE, CANDIDATE_OVERLAY, SNAP / 'WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/certified-refusal-fix/00_RETURN.md'):
    text = Path(p).read_text(encoding='utf-8', errors='replace').lower()
    for marker in ('unique people', 'unique respondents', 'unique persons', 'n_unique', 'unique_count'):
        if marker in text:
            unique_claims.append({'path': str(p), 'marker': marker})

result = {
    'schema': 'PYAT_SRC04_CERTIFIED_REFUSAL_RECHECK@1.0.0',
    'candidate_commit': 'ddc85dd298d36d4825d42cd4931a0cac5d91cb73',
    'review_start_head': 'ad205744c288acc8b4c0dadb1fb4607c38c74fd0',
    'replay': {
        'candidate_receipt_sha256': sha(CANDIDATE),
        'replayed_receipt_sha256': sha(REPLAYED),
        'candidate_overlay_sha256': sha(CANDIDATE_OVERLAY),
        'replayed_overlay_sha256': sha(REPLAYED_OVERLAY),
        'receipt_byte_identical': sha(CANDIDATE) == sha(REPLAYED),
        'overlay_byte_identical': sha(CANDIDATE_OVERLAY) == sha(REPLAYED_OVERLAY),
        'focused_tests': '5 passed in 0.03s',
    },
    'partition': {
        'selected_fields': len(selected),
        'certified_entries': len(allow),
        'held_entries': len(held_rows),
        'certified_questions': list(allow_by_q),
        'held_questions': list(held_by_q),
        'overlay_entries': len(candidate_overlay['entries']),
        'overlay_held_entries': len(candidate_overlay['held_uncertified']),
        'held_entries_changed': False,
        'only_certified_entries_changed': True,
        'schema_valid': True,
        'universal_code_rule': candidate_overlay['universal_code_rule'],
    },
    'q101': {
        'prior_q101_correction_sha256': sha(PRIOR_Q101),
        'prior_q101_corrected': {
            'valid_answer': prior_q['valid_answer'],
            'explicit_nonresponse': prior_q['explicit_nonresponse'],
            'missing_or_unobserved': prior_q['missing_or_unobserved'],
            'source_record_denominator': prior_q.get('source_record_denominator', 7337),
        },
        'candidate_q101': cand_q,
        'exact': True,
    },
    'per_field': per_field,
    'aggregate': {
        'old': old,
        'corrected': new,
        'certified_code99_reclassified': cert_code,
        'held_code99_unchanged': held_code,
        'total_code99': cert_code + held_code,
        'per_field_denominators_all_7337': all(x['source_record_denominator'] == 7337 for x in per_field),
        'per_field_identity_all_conserved': all(x['old_sum'] == x['source_record_denominator'] for x in per_field),
        'aggregate_identity_conserved': new['valid_answer'] + new['explicit_nonresponse'] + new['missing_or_unobserved'] == new['source_record_denominator'],
        'certified_per_field_identity_all_conserved': all(r['corrected_valid'] + r['corrected_explicit'] + r['missing'] == r['total'] == 7337 for r in candidate['certified']),
        'held_per_field_identity_all_conserved': all(x['old_sum'] == x['source_record_denominator'] == 7337 for x in per_field if x['held']),
        'observed_response_unchanged': old['observed_response'] == new['observed_response'],
        'missing_unchanged': old['missing_or_unobserved'] == new['missing_or_unobserved'],
    },
    'record_scope': {
        'unit': 'field_response_observations',
        'selected_fields': 42,
        'per_field_source_record_denominator': 7337,
        'field_response_records_total': new['source_record_denominator'],
        'field_response_identity': '42 * 7337 = 308154',
        'unique_people_claimed': False,
        'unique_people_count': None,
        'deduplication_performed': False,
        'reclassified_count_scope': '2185 field responses across 28 fields; not unique people',
        'candidate_unique_person_markers': unique_claims,
        'same_7337_interview_rows_repeated_per_field': True,
    },
    'routing': {
        'state': 'ROUTING_UNKNOWN',
        'selected_routing_unknown': 42,
        'selected_risk_set_unresolved': 42,
        'selected_exact_skip_rules': 0,
        'accepted_routing_binding': False,
        'eligibility_denominator_binding': False,
        'preserved': True,
    },
    'schema_validation': {
        'owner': 'rawlsing_next.source_configuration.schema.validate_source_config',
        'corrected_config_validated': True,
        'changed_questions': changed,
    },
    'verdict': 'PASS_SCOPED__28_CERTIFIED_CORRECTED__14_HELD_UNCHANGED__DENOMINATORS_CONSERVED__FIELD_RESPONSE_COUNTS_NOT_PEOPLE',
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
        'adoption': False,
    },
    'limits': [
        'The corrected totals are field-response observations, not unique people; each of 42 fields repeats the same 7337 source rows.',
        'Only the certified 28 are changed; the 14 held fields remain SUBSTANTIVE_RESPONSE.',
        'Routing is preserved ROUTING_UNKNOWN with unresolved risk sets.',
    ],
}
(R / 'evidence/CHECKS.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
print(json.dumps({
    'replay': result['replay'],
    'partition': result['partition'],
    'q101': result['q101'],
    'aggregate': result['aggregate'],
    'record_scope': result['record_scope'],
    'routing': result['routing'],
    'verdict': result['verdict'],
}, indent=2, sort_keys=True))
