"""Sourcefree model-unit controls for B53H structural prefilter only.

These tests do not import Rawlsing native PRE553 and cannot qualify R1/R4/R5/R6.
"""
import copy
import importlib.util
from pathlib import Path

P = Path(__file__).with_name('03_manifest_gate_prototype.py')
spec = importlib.util.spec_from_file_location('b53h_gate', P)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def fixture():
    roster = {'waves': [
        {'source_wave_id': f'EXACT-CLOSED35-{i:02d}', 'format': 'SAV' if i < 31 else 'DTA'}
        for i in range(35)
    ]}
    sha = gate.digest(roster)
    waves = [{'source_wave_id': w['source_wave_id'], 'status': 'SCIENTIFIC_UNISSUED',
              'original_u_root': None, 'original_e_pre_root': None,
              'hold_reason': 'independently unissued original E_pre'} for w in roster['waves']]
    fixtures = []
    for i, (family, fmt, markers, codes) in enumerate([
        ('f1', 'SAV', ['SPLIT_FORM', 'WEIGHT_DESIGN'], ['att_1', 'class_0']),
        ('f2', 'DTA', ['HOUSEHOLD_UNIT'], ['income_q', 'bel_3']),
        ('f3', 'SAV', ['ROUTED', 'MULTIRESPONSE'], ['trust_a', 'trust_b']),
    ]):
        fixtures.append({
            'fixture_id': f'F{i}', 'family': family, 'format': fmt,
            'shape_markers': markers, 'native_item_codes': codes,
            'independent_fixture_authority_ref': f'FROZEN-EXTERNAL-F{i}',
            'expected_operation_ids': [f'E{i}'], 'result_operation_ids': [f'E{i}'],
            'native_called_owners': ['C11', 'I03', 'I05', 'BATCH'],
            'source_value_mutation_assertion_id': f'RED-A{i}',
        })
    candidate = {
        'schema': gate.SCHEMA, 'grade': 'UNIVERSAL_SOURCEFREE_SHAPE_PROVED',
        'canonical_roster_sha256': sha, 'base_sha': 'f' * 40,
        'waves': waves, 'production_entrypoint': 'qualified.generic_sourcefront',
        'scientific_original_grade': 'NOT_ISSUED',
        'e_pre_value_blind': True, 'cold_restoration': True,
        'fixtures': fixtures,
        'metamorphic_pairs': [{'reserved_names_absent': True,
                               'bijective_source_valid_rename': True,
                               'normalized_operation_parity': True,
                               'normalized_consumer_parity': True}],
        'named_native_consumer': 'existing nonperson E04',
        'same_consumer_red_assertion': 'native assertion RED',
        'restore_same_consumer_green_assertion': 'cold GREEN',
    }
    return roster, sha, candidate


def test_synthetic_structural_happy_path_does_not_claim_execution():
    roster, sha, candidate = fixture()
    out = gate.validate(roster, sha, candidate)
    assert out['state'] == 'STRUCTURAL_CONTRACT_PASS_NEEDS_TRUSTED_NATIVE_PROOF'
    assert not out['errors']
    assert 'NATIVE_RUNTIME_PROVED' in out['never_implies']


def test_omitted_original_wave_rejected():
    roster, sha, candidate = fixture()
    candidate['waves'].pop()
    out = gate.validate(roster, sha, candidate)
    assert 'WAVE_EXPECTED_EMITTED_ANTI_JOIN' in out['errors']


def test_original_unissued_zero_fabrication_rejected():
    roster, sha, candidate = fixture()
    candidate['waves'][0]['original_e_pre_root'] = 0
    out = gate.validate(roster, sha, candidate)
    assert any(x.startswith('UNISSUED_ORIGINAL_ROOT_MUST_BE_NULL') for x in out['errors'])


def test_single_lits_shape_repeated_cannot_pass():
    roster, sha, candidate = fixture()
    for i, f in enumerate(candidate['fixtures']):
        f['family'] = 'LiTS'
        f['format'] = 'DTA'
        f['native_item_codes'] = ['q301_2', 'q301_7']
        f['shape_markers'] = ['HOUSEHOLD_UNIT']
    out = gate.validate(roster, sha, candidate)
    assert 'FAMILY_DIVERSITY_MISSING' in out['errors']
    assert 'SAV_DTA_HETEROGENEITY_MISSING' in out['errors']
    assert 'IDENTITY_RELABELED_FIXTURE_NOT_HETEROGENEOUS' in out['errors']


def test_real_i05_diversity_required():
    roster, sha, candidate = fixture()
    candidate['fixtures'][1]['native_called_owners'].remove('I05')
    candidate['fixtures'][2]['native_called_owners'].remove('I05')
    out = gate.validate(roster, sha, candidate)
    assert 'TWO_DISTINCT_I05_NATIVE_SHAPES_REQUIRED' in out['errors']


def test_missing_operation_anti_join_rejected():
    roster, sha, candidate = fixture()
    candidate['fixtures'][0]['result_operation_ids'] = ['E-UNAUTHORIZED']
    out = gate.validate(roster, sha, candidate)
    assert 'SOURCEFREE_OPERATION_ANTI_JOIN:F0' in out['errors']


def test_meta_invariance_and_consumer_required():
    roster, sha, candidate = fixture()
    candidate['metamorphic_pairs'] = []
    candidate['same_consumer_red_assertion'] = None
    out = gate.validate(roster, sha, candidate)
    assert 'ARBITRARY_NAMES_METAMORPHIC_GATE_MISSING' in out['errors']
    assert 'SOURCE_FAULT_NAMED_RED_MISSING' in out['errors']


def test_wrong_trusted_roster_pin_rejected():
    roster, sha, candidate = fixture()
    out = gate.validate(roster, '0' * 64, candidate)
    assert 'TRUSTED_ROSTER_SHA_MISMATCH' in out['errors']
