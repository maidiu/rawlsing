"""Passive original35 owner-binding ledger. No source use or authority issuance.

This is an audit of inherited declarations, not a query/workload generator and
not a gateway that can authorize execution when a dictionary is filled in.
"""
from collections import Counter
import ast
import csv
import gzip
import hashlib
import json
from pathlib import Path

csv.field_size_limit(10_000_000)
ROOT = Path(__file__).resolve().parent
INPUT = ROOT / '.runtime/inputs'
HOLD = 'HOLD_UNISSUED_ORIGINAL_SOURCE_ITEM_OP_BINDING'
OWNER_FILES = {
    'register_A': 'REGISTER_A_question_structure_register.csv',
    'register_B': 'REGISTER_B_question_structure_register.csv',
    'v525b_semantic': 'v525b_questions_master_semantic.csv',
    'v525b_drivers': 'v525b_questions_master_drivers.csv',
    'd62_driver_provenance_only': 'd62_questions_master_drivers.csv',
}
REQUIRED_PACKET = {
    'current_source_host_purpose_warrant': 'named source/data custodian',
    'source_edition_hash': 'source custodian, exact edition',
    'administered_form_and_physical_item': 'instrument/source owner',
    'question_options_special_states': 'accepted item/response semantic owner',
    'country_population_and_time': 'source/design owner',
    'respondent_person_household_namespace': 'respondent/design owner',
    'repeat_missing_and_duplicate_respondent_policy': 'respondent/design owner',
    'routing_and_risk_denominator': 'routing/design owner',
    'weights_design_or_explicit_raw_mode': 'design/weight owner',
    'operation_specific_scope_and_eligibility': 'operation authority owner',
    'competent_original_U_and_E_pre': 'competent inventory/eligibility issuer',
    'canonical_authority_query_predicate_preimages': 'native authority/catalog owner',
    'exact_C11_release_preimage': 'C11 release custodian',
    'independent_pre_run_expected_item_operation_set': 'expectation custodian',
    'named_learned_rule_and_consumer': 'learned consumer/rule owner',
}


def load(relative):
    return json.loads((INPUT / relative).read_text())


def matrix():
    return load('original/PYAT-R28-O35E-ORIGINAL-35-ELIGIBILITY-NATIVE-R1_01_35_WAVE_ELIGIBLE_ITEM_OPERATION_MATRIX.json')


def verify_inputs():
    receipts = []
    for spec in json.loads((ROOT / 'source_manifest.json').read_text()):
        data = (ROOT / spec['local']).read_bytes()
        actual = (len(data), hashlib.sha256(data).hexdigest(),
                  hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest())
        expected = (spec['bytes'], spec['sha256'], spec['blob_sha1'])
        if actual != expected:
            raise ValueError('pinned metadata/code mismatch: ' + spec['path'])
        receipts.append({'path': spec['path'], 'commit': spec['commit'], 'sha256': actual[1], 'state': 'EXACT'})
    return receipts


def original_sets(doc):
    with (INPUT / 'original/local_archive_Rawlsing_P2_Phase0_Question_Node_Skeleton_v1.csv').open(newline='') as f:
        p2_rows = list(csv.DictReader(f))
    p2 = {row['exact_identity_sha256'] for row in p2_rows}
    active = [item for wave in doc['waves'] for item in wave['items']]
    common = {row['p2_exact_identity_sha256'] for row in active if row['p2_exact_identity_sha256']}
    blocked = [row for row in active if not row['p2_exact_identity_sha256']]
    return p2_rows, p2, common, blocked


def audit_owner_rows():
    """Compare each selected logical CSV record to original owner preimage.

    Exact ordinal preserves duplicate assertions. Host locator fields remain
    ignored locally; no authority is inferred from casefold matching.
    """
    projections = load('wg0x/sources/owner_row_projections.json')
    receipt = []
    for owner, filename in OWNER_FILES.items():
        with (INPUT / 'original' / filename).open(newline='', encoding='utf-8-sig') as f:
            rows = list(csv.DictReader(f))
        for selected in projections[owner]['selected_records']:
            actual = rows[selected['csv_record'] - 1]
            expected = selected['row']
            if {k: actual[k] for k in expected} != expected:
                raise ValueError('owner logical record changed: ' + owner + ':' + str(selected['csv_record']))
            original_hash = hashlib.sha256(json.dumps(actual, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            if original_hash != selected['row_sha256']:
                raise ValueError('owner whole logical row hash changed: ' + owner + ':' + str(selected['csv_record']))
            receipt.append({'owner': owner, 'csv_record': selected['csv_record'],
                            'exact_case_key': selected['exact_case_key'],
                            'inherited_row_sha256': selected['row_sha256'],
                            'state': 'ALL_PROJECTED_FIELDS_EXACT_AT_ORIGINAL_CSV_ORDINAL'})
    return receipt


def accounting_units(doc):
    """Enumerate inherited candidate-profile HOLD accounting, never eligible E_pre."""
    for wave in sorted(doc['waves'], key=lambda x: x['atlas_id']):
        for item in sorted(wave['items'], key=lambda x: (x['question_id'], x['governed_row_payload_hash'])):
            for profile in sorted(doc['original_operation_status_default']):
                unit = (wave['atlas_id'], item['question_id'], item['governed_row_payload_hash'], profile)
                yield unit


def unit_bytes(units):
    return b''.join((json.dumps(unit, ensure_ascii=False, separators=(',', ':')) + '\n').encode() for unit in units)


def anti_join(expected, actual):
    expected, actual = set(expected), set(actual)
    return {'missing': sorted(expected - actual), 'unexpected': sorted(actual - expected)}


def decisions():
    rows = []
    for inherited in load('wg0x/01_EXACT_26_PLUS_9_CROSSWALK.json')['rows']:
        row = dict(inherited)
        role = row['inherited_role']
        if role in ('admin', 'administrative_metadata'):
            operation = 'CARRIER_COORDINATE_DESIGN_CANDIDATE_ONLY'
        elif row['side'] == 'QRA_BLOCKED' or role == 'blocked_review':
            operation = 'IDENTITY_OR_RESPONSE_OWNER_REOPEN_BEFORE_OPERATION'
        elif role == 'structural_context':
            operation = 'RAW_CONTEXT_OR_CONDITION_CANDIDATE; NO_DIRECTED_SCALE_OR_JOINT_BATTERY_ISSUED'
        else:
            operation = 'SOURCE_LOCAL_NOMINAL_OR_RETAINED_RELATION_CANDIDATE; NO_CROSS_SOURCE_PORTABILITY'
        row['operation_binding_decision'] = operation
        row['owner_packet_missing'] = dict(REQUIRED_PACKET)
        row['ordered_decision_path'] = [
            'retain exact owner assertions and blocked identity',
            'resolve same edition/form/physical occurrence; aliases remain candidates',
            'obtain sourcefree retained preimages OR verified specific new-read warrant',
            'bind respondent/country/time/routing/risk/design/options at operation grain',
            'competent issuer supplies U/E_pre and operation eligibility; independent expectations frozen',
            'existing RuntimeObjectCatalog exact authority closure -> I03/I05 -> Batch -> named learned consumer',
        ]
        row['execution_permission'] = HOLD
        row['new_native_product'] = 'NOT_RUN'
        rows.append(row)
    return rows


def all35(doc):
    result = []
    for wave in doc['waves']:
        result.append({
            'atlas_id': wave['atlas_id'], 'family': wave['canonical_source_family'],
            'wave': wave['canonical_wave'], 'qra_items': len(wave['items']),
            'qra_status_counts': dict(Counter(x['qra_authority_status'] for x in wave['items'])),
            'declared_candidate_profile_units_not_E_pre': len(wave['items']) * len(doc['original_operation_status_default']),
            'source_identity': wave['dataset_manifest_identity'],
            'sample_risk_design_edition': wave['sample_risk_design_edition'],
            'source_use_status': wave['source_use_status'],
            'permission_warrant_ref': wave['permission_warrant_ref'],
            'competent_original_U_ref': wave['competent_original_U_ref'],
            'competent_original_E_pre_ref': wave['competent_original_E_pre_ref'],
            'eligible_original_count': wave['eligible_original_count'],
            'current_permitted': 0, 'new_original_runs': 0,
            'inherited_authority_pointer_artifacts': sorted({
                str(v) for item in wave['items'] for v in item['preserved_authority_pointers'].values() if v
            }),
            'owner_packet_missing': REQUIRED_PACKET,
            'operation_statuses': doc['original_operation_status_default'],
        })
    return result


def retained_evidence(doc):
    """Reproduce the bounded source projections and named producer audit."""
    evidence = ROOT / 'evidence'
    for src, dst in [
        ('wg0x/sources/owner_row_projections.json', 'owner_assertions_sanitized.json'),
        ('wg0x/evidence/excluded_inactive_ledger.jsonl', 'inactive_259_preserved.jsonl'),
        ('as2b/06_I03_CERTIFICATION_RECEIPT.csv', 'AS2B_HISTORICAL_NOT_NEW_EXECUTION.csv'),
        ('p10/03_P10_FINAL_AUTHORITY_FUNCTION_CENSUS.csv', 'P10_frozen_census.csv'),
    ]:
        raw = (INPUT / src).read_bytes()
        if b'/Users/' in raw:
            raise ValueError('personal host locator in publication projection')
        (evidence / dst).write_bytes(raw)
    (evidence / 'partial_response_and_profile_requirements.json').write_text(json.dumps(
        {k: doc[k] for k in ['partial_response_registry', 'operation_requirements', 'census']},
        indent=2, ensure_ascii=False) + '\n')
    specs = json.loads((ROOT / 'source_manifest.json').read_text())
    nodes = []
    for inherited in load('wg0x/02_PRODUCER_GENEALOGY.json')['nodes']:
        spec = next(x for x in specs if (x['commit'], x['path']) == (
            inherited['source']['commit'], inherited['source']['path']))
        source = (ROOT / spec['local']).read_text()
        found = [n for n in ast.walk(ast.parse(source))
                 if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef))
                 and n.name == inherited['function']]
        if len(found) != 1:
            raise ValueError('named owner function not unique: ' + inherited['id'])
        node = found[0]
        segment = '\n'.join(source.splitlines()[node.lineno - 1:node.end_lineno]) + '\n'
        nodes.append({
            'id': inherited['id'], 'function': inherited['function'], 'source': inherited['source'],
            'actual_line': node.lineno, 'actual_end_line': node.end_lineno,
            'function_source_sha256': hashlib.sha256(segment.encode()).hexdigest(),
            'inherited_WG0X_finding_not_new_execution': inherited['finding'],
            'classification': inherited['classification'],
        })
    (evidence / 'native_owner_seams.json').write_text(json.dumps({
        'overall': 'EXISTING_GENERATORS; MISSING_EXACT_AUTHORITY_AND_RETAINED_PREIMAGE_BINDING; NO_REPRESENTABILITY_FAILURE_ESTABLISHED',
        'nodes': nodes,
    }, indent=2) + '\n')


def main():
    verify = verify_inputs()
    owner_audit = audit_owner_rows()
    doc = matrix()
    retained_evidence(doc)
    p2_rows, p2, common, blocked = original_sets(doc)
    freeze = json.loads((ROOT / 'evidence/PREIMPLEMENTATION_FREEZE.json').read_text())
    left = sorted(p2 - common)
    if left != freeze['expected_p2_only_sha256']:
        raise ValueError('direct P2/O35E anti-join differs from independent freeze')
    units = list(accounting_units(doc))
    data = unit_bytes(units)
    if (len(units), hashlib.sha256(data).hexdigest()) != (
        freeze['declared_accounting_not_E_pre']['unit_count'], freeze['declared_accounting_not_E_pre']['sha256']
    ):
        raise ValueError('candidate profile accounting differs from independent freeze')
    evidence = ROOT / 'evidence'
    (evidence / 'declared_held_accounting.jsonl.gz').write_bytes(gzip.compress(data, mtime=0))
    out = {
        'schema': 'O35B_OWNER_BINDING_AUDIT_R1', 'grade': 'AUTHOR_METADATA_AUDIT_ONLY',
        'counts': {'P2': len(p2_rows), 'O35E_ACTIVE': sum(len(w['items']) for w in doc['waves']),
                   'COMMON': len(common), 'P2_ONLY': len(left), 'O35E_ONLY_BLOCKED': len(blocked),
                   'CURRENT_PERMITTED': 0, 'DECLARED_CANDIDATE_PROFILE_UNITS_NOT_E_PRE': len(units)},
        'source_verification': verify, 'owner_logical_record_audit': owner_audit,
        'rows': decisions(), 'all35': all35(doc),
        'inactive_259': {'state': 'PRESERVED_EXCLUDED_NO_ACTIVE_OPERATION',
                         'source': 'wg0x/evidence/excluded_inactive_ledger.jsonl'},
        'eligible_original_count': None, 'original_U': 'PARTIAL_NOT_EXHAUSTIVE',
        'original_E_pre': 'UNISSUED', 'new_original_native_positive': 'NOT_PROVED',
        'actual_native_execution_omission_RED': 'NOT_RUN',
    }
    (evidence / 'owner_binding_audit.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'counts': out['counts'], 'owner_records_verified': len(owner_audit),
                      'held_accounting_sha256': hashlib.sha256(data).hexdigest()}))


if __name__ == '__main__':
    main()
