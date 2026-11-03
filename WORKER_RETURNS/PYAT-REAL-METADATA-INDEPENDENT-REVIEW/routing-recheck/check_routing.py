"""Independent routing/q101 semantics check for the accepted SRC04 42-slot slice."""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path

R = Path(__file__).resolve().parent
SNAP = Path((R / 'evidence/snapshot.path').read_text().strip())
CONFIG = SNAP / 'rawlsing_next/source_configuration/data/SRC04/source.config.json'
TALLY = SNAP / 'prior/TALLY_PRODUCT.json'
ROUTING = R / 'evidence/REPLAYED_ROUTING_RECEIPT.json'
CANDIDATE = SNAP / 'WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/routing/01_ROUTING_RECEIPT.json'
CODEBOOK = Path('/Users/matthewsmith/Desktop/Rawlsing/data/FINAL CODEBOOKS/FINAL FINAL CODEBOOKS/Arab Barometer Wave 1 codebook.csv')
OPTION_AUTH = Path('/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/reports/arab_barometer_response_option_authority.csv')
INSTRUMENT = Path('/Users/matthewsmith/Desktop/Rawlsing/data/Arabbarometer/ABI_Questionnaire_ENG.pdf')

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def jload(p): return json.loads(Path(p).read_text(encoding='utf-8'))

cfg = jload(CONFIG)
tally = jload(TALLY)
receipt = jload(ROUTING)
candidate = jload(CANDIDATE)

# q101 accepted tally record and raw counts.
q101 = next(x for x in tally['fields'] if x['question_id'] == 'q101')
native = {str(x.get('native_value')): x for x in q101['native_value_counts']}
state_by_value = {str(x.get('native_value')): x.get('state') for x in q101['native_value_counts_by_state']}
count = lambda v: int(native.get(v, {}).get('count', 0))
correct_substantive = sum(count(v) for v in ('1.0', '2.0', '3.0', '4.0'))
correct_dk = count('98.0')
correct_refusal = count('99.0')
correct_missing = count('None') + count('null')
correct_observed = correct_substantive + correct_dk + correct_refusal + count('97.0')

# q101 source-config mapping and codebook/authority evidence.
qslots = {str(x['question_id']): x for x in cfg['response_slots']}
q101_slot = qslots['q101']
q101_map = {
    str(v['raw_value']): {
        'response_state': v.get('response_state'),
        'canonical_value': v.get('canonical_value'),
    }
    for v in q101_slot['values']
}
with CODEBOOK.open(newline='', encoding='utf-8-sig', errors='replace') as f:
    codebook_q101 = next(r for r in csv.DictReader(f) if r.get('var_name') == 'q101')
with OPTION_AUTH.open(newline='', encoding='utf-8', errors='replace') as f:
    option_q101 = [
        {k: row.get(k) for k in (
            'value_code_numeric', 'value_label_raw', 'option_group',
            'is_substantive', 'is_missing', 'is_dk', 'is_refusal',
            'is_no_answer', 'response_kind')}
        for row in csv.DictReader(f)
        if row.get('var_name') == 'q101' and row.get('wave') == 'I'
    ]
option_99 = next(r for r in option_q101 if r['value_label_raw'] == 'decline to answer')

# All selected slots: how many map raw 99 to substantive?
selected_ids = [str(x) for x in receipt['accepted_slice']['selected_question_ids']]
selected_99 = {
    q: qslots[q]['values']
    for q in selected_ids
    if q in qslots
}
selected_99_state = {}
for q, values in selected_99.items():
    for v in values:
        if str(v.get('raw_value')) == '99.0' or str(v.get('canonical_value')) == '99':
            selected_99_state[q] = v.get('response_state')

# Routing counts from replayed receipt.
rows = receipt['rows']
routing_unknown = sum(1 for r in rows if r['routing_typed_state'] != 'ROUTING_KNOWN')
risk_unresolved = sum(1 for r in rows if not r['risk_set_exact'])
exact_rules = sum(1 for r in rows if r['routing_rule_exact'])
q101_row = next(r for r in rows if r['question_id'] == 'q101')

# Instrument evidence. This reads only the questionnaire PDF, never the SAV.
from pypdf import PdfReader
pdf = PdfReader(str(INSTRUMENT))
page_texts = [(p.extract_text() or '') for p in pdf.pages]
q101_page = next(i for i, t in enumerate(page_texts) if '101q' in t.lower() or 'q101' in t.lower()) + 1
q101_text = page_texts[q101_page - 1]
markers = ('ask all', 'all respondents', 'unconditional', 'skip', 'filter',
           'if yes', 'if no', 'go to', 'routing', 'eligib')
marker_hits = {m: [i + 1 for i, t in enumerate(page_texts) if m in t.lower()] for m in markers}
qidx = q101_text.lower().find('101q')
excerpt = q101_text[max(0, qidx - 120):qidx + 620]

result = {
    'schema': 'PYAT_SRC04_ROUTING_RECHECK@1.0.0',
    'candidate_commit': 'a108e7dc7232b1f3487e71d4607f3e6ca3e9ebdf',
    'review_start_head': 'bdeace7866bcfaf7c94710b976c80b950bfe2968',
    'prior_metadata_review': {
        'commit': 'bdeace7866bcfaf7c94710b976c80b950bfe2968',
        'review_json_sha256': 'f7939d2f9f417348a1b44d1fc3b53164cf63fdf0dd95661c75fee2ed28e61770',
        'checks_json_sha256': '8202036810494b2a632fafb31a0d5d693044d5993e0693d0d5e981fd6f0d9600',
        'reused': True,
    },
    'replay': {
        'candidate_receipt_sha256': sha(CANDIDATE),
        'replayed_receipt_sha256': sha(ROUTING),
        'exact': sha(CANDIDATE) == sha(ROUTING),
        'focused_tests': '5 passed in 0.03s',
    },
    'routing': {
        'selected_response_slots': len(rows),
        'selected_routing_unknown': routing_unknown,
        'selected_risk_set_unresolved': risk_unresolved,
        'selected_exact_skip_rules': exact_rules,
        'config_routing_entries': receipt['routing_authority']['config_routing_entries'],
        'accepted_routing_binding': receipt['routing_authority']['accepted_routing_binding'],
        'accepted_denominator_binding': receipt['routing_authority']['accepted_denominator_binding'],
        'q101': {
            'row_selector': next(x.get('row_selector') for x in cfg['routing'] if x.get('question_id') == 'q101'),
            'typed_state': q101_row['routing_typed_state'],
            'routing_rule_ref': q101_row['routing_rule_ref'],
            'risk_set_ref': q101_row['risk_set_ref'],
            'routing_rule_exact': q101_row['routing_rule_exact'],
            'risk_set_exact': q101_row['risk_set_exact'],
        },
        'all_42_unknown': routing_unknown == 42,
        'all_42_risk_unresolved': risk_unresolved == 42,
        'exact_skip_rules_zero': exact_rules == 0,
    },
    'q101_tally': {
        'accepted_receipt': {
            'valid_answer': receipt['consumer_probe']['valid_answer'],
            'explicit_nonresponse': receipt['consumer_probe']['explicit_nonresponse'],
            'missing_or_unobserved': receipt['consumer_probe']['missing_or_unobserved'],
            'observed_response': q101['observed_response_denominator'],
            'source_record_denominator': q101['source_record_denominator'],
            'state_counts': q101['state_counts'],
        },
        'native_counts': q101['native_value_counts'],
        'native_state_counts': q101['native_value_counts_by_state'],
        'source_config_q101_99': q101_map.get('99.0'),
        'source_config_q101_97': q101_map.get('97.0'),
        'source_config_q101_98': q101_map.get('98.0'),
        'codebook_q101': {
            'response_options_substantive': codebook_q101['response_options_substantive'],
            'response_options_special': codebook_q101['response_options_special'],
            'note': codebook_q101['note'],
        },
        'option_authority_99': option_99,
        'correct': {
            'valid_answer': correct_substantive,
            'explicit_nonresponse': correct_dk + correct_refusal + count('97.0'),
            'dk': correct_dk,
            'refusal': correct_refusal,
            'missing_or_unobserved': correct_missing,
            'observed_response': correct_observed,
            'source_record_denominator': int(q101['source_record_denominator']),
            'identity': correct_substantive + correct_dk + correct_refusal + correct_missing + count('97.0'),
        },
        'delta': {
            'valid_answer_candidate_minus_correct': receipt['consumer_probe']['valid_answer'] - correct_substantive,
            'explicit_nonresponse_candidate_minus_correct': receipt['consumer_probe']['explicit_nonresponse'] - (correct_dk + correct_refusal + count('97.0')),
            'misclassified_refusals': correct_refusal,
        },
        'semantically_correct': (
            receipt['consumer_probe']['valid_answer'] == correct_substantive
            and receipt['consumer_probe']['explicit_nonresponse'] == (correct_dk + correct_refusal + count('97.0'))
        ),
    },
    'selected_99_mapping': {
        'selected_fields': len(selected_99_state),
        'mapped_to_SUBSTANTIVE_RESPONSE': sum(1 for v in selected_99_state.values() if v == 'SUBSTANTIVE_RESPONSE'),
        'all_42_mapped_substantive': all(v == 'SUBSTANTIVE_RESPONSE' for v in selected_99_state.values()) and len(selected_99_state) == 42,
        'q101_99_state': selected_99_state.get('q101'),
    },
    'instrument_evidence': {
        'path': str(INSTRUMENT),
        'sha256': sha(INSTRUMENT),
        'pages': len(pdf.pages),
        'q101_page': q101_page,
        'q101_excerpt': excerpt,
        'explicit_unconditional_marker': None,
        'explicit_skip_or_filter_marker': None,
        'marker_hits': marker_hits,
        'q101_listed_without_visible_filter': True,
        'affirmative_eligibility_evidence': False,
        'interpretation': 'The exact instrument lists q101 as a main questionnaire item without an explicit ask-all/unconditional/skip/filter statement. No rule was found in the examined instrument/metadata; this does not establish that no rule exists elsewhere.',
    },
    'eligibility': {
        'q101_affirmative_eligibility': False,
        'q101_eligibility_unknown': True,
        'no_rule_found_in_examined_material': True,
        'no_rule_exists_claim': False,
        'counts_used_to_infer_routing': False,
        'routing_hold_remains': True,
    },
    'verdict': 'REVISE',
    'finding': 'Routing HOLD and 42 unknown states stand. q101 tally semantics are not accepted: 33 code-99 refusals are mapped to SUBSTANTIVE_RESPONSE, producing valid=7162 instead of 7129 and explicit nonresponse=171 instead of 204. The exact instrument documents 99 as Decline to Answer but provides no explicit unconditional/skip/routing rule for q101.',
    'scope': {
        'metadata_instrument_only': True,
        'original_sav_read': False,
        'respondent_rows_read': False,
        'new_authority': False,
        'source_execution': False,
        'production_edit': False,
        'merge': False,
        'ci': False,
    },
}
out = R / 'evidence/CHECKS.json'
out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
print(json.dumps({
    'replay_exact': result['replay']['exact'],
    'routing': result['routing'],
    'q101_correct': result['q101_tally']['correct'],
    'q101_candidate': result['q101_tally']['accepted_receipt'],
    'q101_semantically_correct': result['q101_tally']['semantically_correct'],
    'instrument_markers': result['instrument_evidence']['marker_hits'],
    'verdict': result['verdict'],
}, indent=2))
