"""B53H R2 hostile CHARACTERIZATION of R1 checker bypasses, not approvals.

All four tests PASS if the old self-attestation gates are inadequately restrictive.
Actual interpreter, PRE553 native engine, source rights and E04 not invoked here.
"""
import importlib.util
from pathlib import Path

root = Path(__file__).resolve().parent

def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, root / filename)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

old = load('old_gate', '03_manifest_gate_prototype.py')
case = load('old_case', '04_test_manifest_gate_prototype.py')


def test_forger_can_invent_native_calls_and_consumer_faults():
    roster, sha, claim = case.fixture()
    for item in claim['fixtures']:
        item['independent_fixture_authority_ref'] = 'FAKE-EXTERNAL-ORACLE'
        item['native_called_owners'] = ['C11', 'I03', 'I05', 'BATCH']
        item['source_value_mutation_assertion_id'] = 'NOT-RUN'
    claim['production_entrypoint'] = 'this.module.does.not.exist'
    claim['named_native_consumer'] = 'fake.client.nonexistent'
    claim['same_consumer_red_assertion'] = 'ASSERTED_NOT_EXECUTED'
    claim['restore_same_consumer_green_assertion'] = 'ASSERTED_NOT_EXECUTED'
    out = old.validate(roster, sha, claim)
    assert out['state'] == 'STRUCTURAL_CONTRACT_PASS_NEEDS_TRUSTED_NATIVE_PROOF'


def test_candidate_owns_its_own_expected_operation_oracle():
    roster, sha, claim = case.fixture()
    item = claim['fixtures'][0]
    item['expected_operation_ids'] = ['ONE_SELF_CHOSEN_OPERATION']
    item['result_operation_ids'] = ['ONE_SELF_CHOSEN_OPERATION']
    assert old.validate(roster, sha, claim)['errors'] == []


def test_identity_renaming_and_self_declared_shapes_pass_as_diversity():
    roster, sha, claim = case.fixture()
    for i, item in enumerate(claim['fixtures']):
        item['native_item_codes'] = [f'renamed_y_{i}', f'renamed_z_{i}']
        item['independent_fixture_authority_ref'] = f'CANDIDATE_OWNS_POLICY_{i}'
    assert old.validate(roster, sha, claim)['errors'] == []


def test_boolean_metamorphic_assertions_are_not_execution():
    roster, sha, claim = case.fixture()
    claim['metamorphic_pairs'] = [dict(reserved_names_absent=True,
        bijective_source_valid_rename=True, normalized_operation_parity=True,
        normalized_consumer_parity=True)]
    assert old.validate(roster, sha, claim)['errors'] == []
