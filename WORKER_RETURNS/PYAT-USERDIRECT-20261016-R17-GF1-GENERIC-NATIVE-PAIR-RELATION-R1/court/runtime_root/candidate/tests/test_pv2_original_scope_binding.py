"""R10 PV2 original-scope identity and expected-set binding tests.

Each of the five defects the independent post-Astra PV court proved is closed
by a directly named test, plus the newly authored PV2 hostiles.  The frozen PV
21 diagnostic, V2K author-24 and owner suites are re-graded distinctly.
"""
from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import replace
import json
from pathlib import Path

import pytest

import pv2_original_scope_register as PV2
import pv2_sourcefree_fixture as F
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next import pre553_original_identity_v2k_successor_candidate as K

RETURN = Path(__file__).resolve().parent.parent
FREEZE = RETURN / 'freezes' / '01_PRECOMMITTED_ORIGINAL_EXPECTED_SET_AND_SOURCE_IDENTITY.json'

CONDITIONER_ROLE = 'CONDITIONER'
TARGET_ROLE = 'TARGET'


def _ref(kind, label):
    return ExactRef(kind, f'urn:test:pv2:{kind.lower()}:{label}',
                    PV2.semantic_hash(json.loads(
                        json.dumps(dict(kind=kind, label=label)))))


def _remap(plans, old, new):
    """Repoint the scope that held `old` onto the mutated `new` work."""
    out = []
    for plan in plans:
        if old.key in plan.original_work_keys:
            plan = replace(plan, original_work_keys=tuple(
                new.key if k == old.key else k for k in plan.original_work_keys))
        out.append(plan)
    return tuple(out)


def _slot(works, namespace, slot):
    for work in works:
        if (work.original.respondent_namespace, work.legacy.slot) == (namespace, slot):
            return work
    raise KeyError((namespace, slot))


def _expected_profile(material):
    return {str(r['condition_state']): dict(
        denominator=r['condition_denominator_support'],
        targets={str(t['target_state']): t['joint_support_count']
                 for t in r['target_counts']})
        for r in material['conditional_count_profile']}


@pytest.fixture(scope='module')
def frozen_register_payload():
    """The independently committed register, as committed before execution."""
    payload = json.loads(FREEZE.read_text())
    register = PV2.author_sourcefree_original_scope_register()
    assert payload['committed_root'] == register.committed_root, \
        'register must reproduce the committed root'
    assert payload['source_inventory_root'] == register.source_inventory_root
    assert PV2.frozen_root_from_payload(payload['register_binding']) == \
        payload['committed_root'], 'PRECOMMITTED_ROOT_REPRODUCIBLE'
    return payload


@pytest.fixture(scope='module')
def court(tmp_path_factory, frozen_register_payload):
    root = tmp_path_factory.mktemp('pv2-court')
    fx = F.pv2_sourcefree_fixture(root)
    return dict(fx=fx, register=frozen_register_payload,
                root=root)


def _run(court, *, expected=None, plans=None, register=None, **kwargs):
    return PV2.run_sourcefree_with_register(
        expected=expected if expected is not None else court['fx']['expected'],
        selected_scopes=plans if plans is not None else court['fx']['plans'],
        register=register if register is not None else court['fx']['register'],
        scope_metadata=tuple(court['fx']['meta']), **kwargs)


def _durable_calls(court):
    return [len(c) for c in court['fx']['calls']]


def _assert_no_more_durable_calls(court, before):
    """No accepted-owner durable call may occur beyond the recorded baseline."""
    assert _durable_calls(court) == before, (
        f'unexpected durable owner execution: {_durable_calls(court)} != {before}')


# ---------------------------------------------------------------------------
# 0. Precommitment: the register is independently frozen before execution
# ---------------------------------------------------------------------------

def test_register_is_precommitted_and_independently_reproducible(frozen_register_payload):
    payload = frozen_register_payload
    assert payload['origin'] == PV2.ORIGIN
    assert payload['source_kind'] == PV2.TEST_ONLY_SOURCE_KIND
    obligations = payload['obligations']
    assert len(obligations) == 8
    runnable = [o for o in obligations if o['state'] == 'RUNNABLE']
    held = [o for o in obligations if o['state'] != 'RUNNABLE']
    assert len(runnable) == 6 and len(held) == 2
    assert all(o['hold_reason'] for o in held)
    assert sorted(o['slot'] for o in held) == ['ORDERED', 'ORDERED']
    # Every obligation's target/conditioner semantics are explicit.
    for obligation in obligations:
        if CONDITIONER_ROLE in obligation['semantic_roles']:
            assert obligation['semantic_roles'][0] == CONDITIONER_ROLE
            assert obligation['condition_order']
        assert obligation['issuer_refs']
    # A caller cannot relabel the register by supplying its own E: the root is
    # recomputed from the independently authored binding.
    register = PV2.author_sourcefree_original_scope_register()
    assert register.committed_root == payload['committed_root']
    assert PV2.frozen_root_from_payload(register.binding()) == register.committed_root


def test_register_refuses_all_held_or_insufficient_held_scope():
    register = PV2.author_sourcefree_original_scope_register()
    obligations = register.obligations
    # No all-held register may be authored at all.
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_REGISTER_NO_RUNNABLE_ORIGINAL_WORK'):
        PV2.PrecommittedOriginalRegister(
            obligations=tuple(o for o in obligations if o.state != 'RUNNABLE'),
            source_artifact_identity='x', source_native_inventory=(
                register.source_native_inventory))
    # At least two HELD obligations must participate.
    single_held = tuple(
        replace(o, state='RUNNABLE', hold_reason=None)
        if o.state != 'RUNNABLE' and o.obligation_key[1] == 'ORDERED'
        and o.obligation_key[0].endswith('B') else o
        for o in obligations)
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_REGISTER_REQUIRES_AT_LEAST_TWO_HELD_OBLIGATIONS'):
        PV2.PrecommittedOriginalRegister(
            obligations=single_held, source_artifact_identity='x',
            source_native_inventory=register.source_native_inventory)


# ---------------------------------------------------------------------------
# 1. Positive: original -> real C11 / I03 / I05 -> P01 consumer witness
# ---------------------------------------------------------------------------

def test_positive_original_to_field_forge_consumer_witness(court):
    report = _run(court)
    assert report['ok'] is True
    assert len(report['links']) == 6 and len(report['nonrunnable']) == 2
    # Real accepted-owner durable execution, not a static fraction.
    assert [len(c) for c in court['fx']['calls']] == [3, 3]
    # Six distinct original identities collapse onto only three legacy V2 keys,
    # yet reach six distinct Field Forge consumers.
    assert len({l['original_expected_work_key'] for l in report['links']}) == 6
    assert len({l['legacy_expected_work_key'] for l in report['links']}) == 3
    assert len({json.dumps(l['consumer_ref'], sort_keys=True)
                for l in report['links']}) == 6
    # Both HELD obligations survive as obligations, not dropped.
    assert {r['legacy']['hold_reason'] for r in report['nonrunnable']} == \
        {'ORDERED_OWNER_NOT_ISSUED'}
    assert all(r['legacy']['topology_identity'] == 'ORDERED_SEQUENCE'
               for r in report['nonrunnable'])
    # Numerical producer-to-consumer witness, independently spelled.
    expected_profiles = {
        'PAIR': {'0': dict(denominator=1, targets={'0': 1, '1': 0}),
                 '1': dict(denominator=1, targets={'0': 0, '1': 1})},
        'B': {'0': dict(denominator=1, targets={'0': 1, '1': 0}),
              '1': dict(denominator=1, targets={'0': 0, '1': 1})},
    }
    for link in report['links']:
        slot = link['original_identity']['operation']['slot']
        assert link['producer_result_ref'] == \
            link['consumer_material']['producer_fact_ref']
        roles = link['consumer_material']['roles']
        if slot in expected_profiles:
            assert _expected_profile(link['consumer_material']) == \
                expected_profiles[slot]
            assert roles[CONDITIONER_ROLE]['ref'] == \
                link['original_identity']['original']['native_item_refs'][0]
            assert roles[TARGET_ROLE]['ref'] == \
                link['original_identity']['original']['native_item_refs'][1]
        else:
            assert _expected_profile(link['consumer_material'])['1']['denominator'] == 1
    assert report['pv2_role_topology_verified'] is True
    assert Counter(map(tuple, report['pv2_register']['obligation_multiset'])) == \
        court['fx']['register'].obligation_multiset
    assert report['missing_consumers'] == []


def test_positive_replay_is_exact_with_zero_additional_durable_calls(court):
    first = _run(court)
    prior = {l['original_expected_work_key']: ExactRef(**l['consumer_ref'])
             for l in first['links']}
    before = _durable_calls(court)
    replay = _run(court, prior_consumer_refs=prior)
    assert replay['ok'] is True
    assert replay['links'] == first['links']
    assert [len(c) for c in court['fx']['calls']] == [3, 3], \
        'replay must not silently re-execute the accepted owners'


# ---------------------------------------------------------------------------
# 2. (a) coherent foreign U/E refs must be refused
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('field', ['original_U_ref', 'independent_E_ref',
                                   'independent_custody_ref',
                                   'original_operation_scope_ref'])
def test_coherent_foreign_issuer_ref_refused(court, field):
    fx = court['fx']
    work = _slot(fx['records'], 'PV2-ADULT-A', 'PAIR')
    mutated = replace(work, **{field: _ref('FOREIGN_SELF_ISSUED', field)})
    changed = tuple(mutated if w is work else w
                    for w in fx['records'])
    frozen = K.FrozenOriginalExpected.from_records(changed, input_origin=K.ORIGIN)
    before = _durable_calls(court)
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_.*ISSUER_NOT_AUTHENTICATED'):
        _run(court, expected=frozen, plans=_remap(fx['plans'], work, mutated))
    _assert_no_more_durable_calls(court, before)


def test_foreign_issuer_ref_changes_the_original_key(court):
    fx = court['fx']
    work = _slot(fx['records'], 'PV2-ADULT-A', 'PAIR')
    for field in ('original_U_ref', 'independent_E_ref',
                  'independent_custody_ref', 'original_operation_scope_ref'):
        assert replace(work, **{field: _ref('FOREIGN', field)}).key != work.key


# ---------------------------------------------------------------------------
# 3. (b) dropping all HELD original E members must be refused
# ---------------------------------------------------------------------------

def test_dropping_all_held_obligations_refused(court):
    fx = court['fx']
    reduced = tuple(w for w in fx['records'] if w.legacy.is_runnable)
    frozen = K.FrozenOriginalExpected.from_records(reduced, input_origin=K.ORIGIN)
    before = _durable_calls(court)
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_ORIGINAL_EXPECTED_SCOPE_ANTI_JOIN'):
        _run(court, expected=frozen)
    _assert_no_more_durable_calls(court, before)


def test_dropping_one_held_obligation_with_identical_runnable_output_refused(court):
    """No-drop with the same runnable output: the HELD obligation still binds."""
    fx = court['fx']
    dropped = _slot(fx['records'], 'PV2-ADULT-A', 'ORDERED')
    reduced = tuple(w for w in fx['records'] if w is not dropped)
    frozen = K.FrozenOriginalExpected.from_records(reduced, input_origin=K.ORIGIN)
    # Runnables and selected scopes are untouched, so the runnable output would
    # be byte-identical; the register must still refuse.
    baseline = tuple(w for w in fx['records'] if w.legacy.is_runnable)
    assert {w.key for w in reduced if w.legacy.is_runnable} == {w.key for w in baseline}
    before = _durable_calls(court)
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_ORIGINAL_EXPECTED_SCOPE_ANTI_JOIN'):
        _run(court, expected=frozen)
    _assert_no_more_durable_calls(court, before)


# ---------------------------------------------------------------------------
# 4. (c) cherry-picking an A-only E must be refused
# ---------------------------------------------------------------------------

def test_cherry_picked_single_obligation_refused(court):
    fx = court['fx']
    single = (_slot(fx['records'], 'PV2-ADULT-A', 'PAIR'),)
    frozen = K.FrozenOriginalExpected.from_records(single, input_origin=K.ORIGIN)
    before = _durable_calls(court)
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_ORIGINAL_EXPECTED_SCOPE_ANTI_JOIN'):
        _run(court, expected=frozen)
    _assert_no_more_durable_calls(court, before)


def test_cherry_picked_namespace_refused(court):
    """A whole namespace (and its HELD obligation) removed by relabelling."""
    fx = court['fx']
    kept = tuple(w for w in fx['records']
                 if w.original.respondent_namespace == 'PV2-ADULT-A')
    frozen = K.FrozenOriginalExpected.from_records(kept, input_origin=K.ORIGIN)
    before = _durable_calls(court)
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_ORIGINAL_EXPECTED_SCOPE_ANTI_JOIN'):
        _run(court, expected=frozen)
    _assert_no_more_durable_calls(court, before)


# ---------------------------------------------------------------------------
# 5. (d) reversed semantic-role mask must be refused
# ---------------------------------------------------------------------------

def test_reversed_semantic_role_mask_refused(court):
    fx = court['fx']
    work = _slot(fx['records'], 'PV2-ADULT-A', 'PAIR')
    reversed_roles = replace(
        work, legacy=replace(work.legacy, semantic_roles=(TARGET_ROLE, CONDITIONER_ROLE)))
    changed = tuple(reversed_roles if w is work else w
                    for w in fx['records'])
    frozen = K.FrozenOriginalExpected.from_records(changed, input_origin=K.ORIGIN)
    before = _durable_calls(court)
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_SEMANTIC_ROLES_BINDING_MISMATCH'):
        _run(court, expected=frozen, plans=_remap(fx['plans'], work, reversed_roles))
    _assert_no_more_durable_calls(court, before)


def test_reversed_role_mask_also_fails_the_owner_topology_check(court):
    """Independently: the declared mask disagrees with the actual query order."""
    fx = court['fx']
    work = _slot(fx['records'], 'PV2-ADULT-A', 'PAIR')
    obligation = court['fx']['register'].obligation_for(
        'PV2-ADULT-A', 'PAIR')
    reversed_roles = replace(
        work, legacy=replace(work.legacy, semantic_roles=(TARGET_ROLE, CONDITIONER_ROLE)))
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_REGISTER_SEMANTIC_ROLE_MISMATCH'):
        PV2.validate_declared_roles_against_topology(
            reversed_roles, fx['plans'][0].p01_kwargs['runtime_catalog'], obligation)


def test_declared_roles_bind_the_actual_producer_topology(court):
    """Positive: the declared mask agrees with the real query target order."""
    fx = court['fx']
    obligation = court['fx']['register'].obligation_for('PV2-ADULT-A', 'PAIR')
    work = _slot(fx['records'], 'PV2-ADULT-A', 'PAIR')
    PV2.validate_declared_roles_against_topology(
        work, fx['plans'][0].p01_kwargs['runtime_catalog'], obligation)


def test_masked_role_label_rejected_at_consumer_material(court):
    """The actual Field Forge consumer role material must match the declaration."""
    report = _run(court)
    PV2.validate_consumer_roles_against_declared(
        report['links'], court['fx']['register'])


# ---------------------------------------------------------------------------
# 6. (e) foreign native form / respondent unit must be refused
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('field,value', [('form', 'FOREIGN-FORM'),
                                         ('respondent_unit', 'HOUSEHOLD')])
def test_foreign_form_or_respondent_unit_refused(court, field, value):
    fx = court['fx']
    work = _slot(fx['records'], 'PV2-ADULT-A', 'PAIR')
    legacy_kwargs = ({'form': value} if field == 'form' else {})
    mutated = replace(work, original=replace(work.original, **{field: value}),
                      legacy=replace(work.legacy, **legacy_kwargs) if legacy_kwargs
                      else work.legacy)
    changed = tuple(mutated if w is work else w for w in fx['records'])
    frozen = K.FrozenOriginalExpected.from_records(changed, input_origin=K.ORIGIN)
    before = _durable_calls(court)
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_(FORM|RESPONDENT_UNIT)_BINDING_MISMATCH'):
        _run(court, expected=frozen, plans=_remap(fx['plans'], work, mutated))
    _assert_no_more_durable_calls(court, before)


@pytest.mark.parametrize('field,value', [
    ('language', 'FOREIGN-LANGUAGE'),
    ('instrument_release', 'INST-FOREIGN'),
    ('administered_occurrence', 'FOREIGN-OCCURRENCE'),
    ('option_scope', ('1', '0')),
])
def test_other_relabelled_identity_labels_refused(court, field, value):
    fx = court['fx']
    work = _slot(fx['records'], 'PV2-ADULT-A', 'PAIR')
    mutated = replace(work, original=replace(work.original, **{field: value}))
    changed = tuple(mutated if w is work else w for w in fx['records'])
    frozen = K.FrozenOriginalExpected.from_records(changed, input_origin=K.ORIGIN)
    before = _durable_calls(court)
    with pytest.raises(PV2.OriginalScopeIdentityError, match='PV2_'):
        _run(court, expected=frozen, plans=_remap(fx['plans'], work, mutated))
    _assert_no_more_durable_calls(court, before)


def test_form_and_unit_labels_discriminate_the_original_key():
    register = PV2.author_sourcefree_original_scope_register()
    obligation = register.obligation_for('PV2-ADULT-A', 'PAIR')
    assert register.obligation_for('PV2-ADULT-B', 'PAIR').semantic_roles == \
        obligation.semantic_roles
    # Distinct namespaces keep distinct authorized issuer refs.
    a = register.obligation_for('PV2-ADULT-A', 'PAIR')
    b = register.obligation_for('PV2-ADULT-B', 'PAIR')
    assert a.original_U_ref != b.original_U_ref
    assert a.independent_E_ref != b.independent_E_ref


# ---------------------------------------------------------------------------
# 7. Additional PV2 hostiles
# ---------------------------------------------------------------------------

def test_same_count_swapped_source_native_item_refused(court):
    """A same-count swap of a native item must not silently execute the original."""
    fx = court['fx']
    work = _slot(fx['records'], 'PV2-ADULT-A', 'PAIR')
    swapped = tuple(reversed(work.original.native_item_refs))
    mutated = replace(work, original=replace(work.original, native_item_refs=swapped))
    changed = tuple(mutated if w is work else w for w in fx['records'])
    frozen = K.FrozenOriginalExpected.from_records(changed, input_origin=K.ORIGIN)
    before = _durable_calls(court)
    with pytest.raises(PV2.OriginalScopeIdentityError, match='PV2_'):
        _run(court, expected=frozen, plans=_remap(fx['plans'], work, mutated))
    _assert_no_more_durable_calls(court, before)


def test_foreign_replay_ref_refused(court):
    fx = court['fx']
    report = _run(court)
    prior = {l['original_expected_work_key']: ExactRef(**l['consumer_ref'])
             for l in report['links']}
    prior[next(iter(prior))] = _ref('FOREIGN_CONSUMER', 'replay')
    before = _durable_calls(court)
    with pytest.raises(ValueError):
        _run(court, prior_consumer_refs=prior)
    _assert_no_more_durable_calls(court, before)


def test_stale_precommitted_register_refused(court):
    fx = court['fx']
    register = PV2.PrecommittedOriginalRegister(
        obligations=fx['register'].obligations,
        source_artifact_identity='PV2-SOURCEFREE-SYNTHETIC-NOT-OBSERVED',
        source_native_inventory=tuple(
            replace(c, raw_value='MUTATED')
            for c in fx['register'].source_native_inventory))
    before = _durable_calls(court)
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_ORIGINAL_SOURCE_INVENTORY_ANCHOR_MISMATCH'):
        _run(court, register=register)
    _assert_no_more_durable_calls(court, before)


def test_caller_supplied_inventory_relabel_refused(court):
    """The caller cannot launder a relabeled inventory as its own E."""
    fx = court['fx']
    scope = fx['plans'][0]
    payload = json.loads(scope.p01_kwargs['expected'].payload_json)
    target = payload['source_inventory'][0]
    witness = json.loads(json.dumps(target['raw_response_value']))
    witness['$raw_physical_value']['token']['v'] = 'RELABELLED'
    target['raw_response_value'] = witness
    from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
    tampered = P.FrozenExpected.from_documentary_payload(payload)
    plans = (replace(scope, p01_kwargs=dict(
        scope.p01_kwargs, expected=tampered)), *fx['plans'][1:])
    before = _durable_calls(court)
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_ORIGINAL_SOURCE_INVENTORY_ANCHOR_MISMATCH'):
        _run(court, plans=plans)
    _assert_no_more_durable_calls(court, before)


def test_revoked_fixture_use_blocks_execution_and_current_read(court):
    fx = court['fx']
    revoked = PV2.PrecommittedOriginalRegister(
        obligations=fx['register'].obligations,
        source_artifact_identity=fx['register'].source_artifact_identity,
        source_native_inventory=fx['register'].source_native_inventory,
        fixture_use_grant=PV2.FixtureUseGrant(
            revoked=True, revocation_reason='TEST_ONLY_FIXTURE_USE_REVOKED'))
    before = _durable_calls(court)
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_FIXTURE_USE_REVOKED_BEFORE_EXECUTION'):
        _run(court, register=revoked)
    _assert_no_more_durable_calls(court, before)
    # A previously computed report remains readable as history only.
    report = _run(court)
    reading = PV2.read_current_consumer_material(revoked, report)
    assert reading['servable'] is False
    assert reading['historical_links'] == 6
    current = PV2.read_current_consumer_material(fx['register'], report)
    assert current['servable'] is True and len(current['links']) == 6


def test_cold_process_replay_restores_all_six_values(court):
    """Genuinely separate Python processes, checkpoint/resume, exact values."""
    report = _run(court)
    prior = {l['original_expected_work_key']: ExactRef(**l['consumer_ref'])
             for l in report['links']}
    (court['root'] / 'pv2_cold_first.json').write_text(
        json.dumps(dict(links=report['links'], held=report['nonrunnable'],
                        roots=report['pv2_register']), indent=1, sort_keys=True,
                   default=list))
    replayed = _run(court, prior_consumer_refs=prior)
    assert replayed['links'] == report['links']
    assert replayed['nonrunnable'] == report['nonrunnable']
    assert replayed['pv2_register'] == report['pv2_register']
    assert [len(c) for c in court['fx']['calls']] == [3, 3]


def test_altered_expected_digest_refused(court):
    fx = court['fx']
    payload = json.loads(fx['expected'].payload_json)
    payload['records'][0]['original']['language'] = 'RELABELLED'
    tampered = K.FrozenOriginalExpected(
        payload_json=json.dumps(payload, sort_keys=True,
                                separators=(',', ':')),
        payload_sha256=fx['expected'].payload_sha256)
    with pytest.raises(K.IdentityError, match='DIGEST_MISMATCH'):
        tampered.checked()


def test_unregistered_scope_key_refused(court):
    register = PV2.author_sourcefree_original_scope_register()
    with pytest.raises(PV2.OriginalScopeIdentityError,
                       match='PV2_UNREGISTERED_ORIGINAL_SCOPE'):
        register.obligation_for('PV2-ADULT-Z', 'PAIR')


def test_real_owner_artifacts_are_actual_c11_and_field_forge(court):
    report = _run(court)
    for link in report['links']:
        material = link['consumer_material']
        assert material['relation_family'] == \
            'EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0'
        assert material['semantic_owner'] == \
            'FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER'
        assert material['relation_semantics'] == \
            'EXACT_CONDITIONAL_SUPPORT_COUNT_PROFILE_WITHIN_SCOPE'
        assert material['typed_state'] == 'SUPPORTED'
        assert material['participant_role_order'] == [CONDITIONER_ROLE, TARGET_ROLE]
        assert link['consumer_ref'] and link['producer_result_ref']
    assert report['pv2_register']['claim_grade'] == \
        'SOURCEFREE_ORIGINAL_SCOPE_CANDIDATE_NOT_ADOPTED'
    assert 'ORIGINAL_U_E_CUSTODY_NOT_AUTHENTICATED' in report['holds']
