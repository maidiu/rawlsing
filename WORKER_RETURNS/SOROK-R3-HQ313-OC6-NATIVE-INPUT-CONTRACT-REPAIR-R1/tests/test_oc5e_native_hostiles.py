"""OC5E — fresh independently authored actual-entrypoint hostiles against OC4.

Every test runs against the pinned OC4 native module (git blob
af2b7e943018077cb36808b5af1cd67704624bec), never a transcribed excerpt.
OC5's four predicted normalized-key falsifiers and its predicted
malformed-primary-signature defect are disclosed and independently re-derived;
the remaining cases are reviewer-authored.

TEST_ONLY fixture scope only: no real signer institution, protected holdout,
durable external journal or independently issued semantic oracle.
"""
from __future__ import annotations

import dataclasses
from copy import deepcopy
from dataclasses import replace

import pytest

import custody_protocol as CP
from custody_protocol import (
    BlindIDPairingError,
    ConflictError,
    CustodyCapsule,
    EscrowState,
    IdentityMismatchError,
    LeakageError,
    MockSignature,
    MockSigner,
    PurposeViolationError,
    RevocationError,
    Role,
    SignatureError,
    assert_no_leakage,
    capsule_envelope_commitment,
    detect_family_clone,
    detect_leakage,
    require_second_signature,
    semantic_fingerprint,
    verify_blind_pairing,
)
from dummy_corpus import build_capsule, build_dummy_corpus


def cap():
    return build_capsule('SOURCEFREE_TEST_ONLY', 'oc5e-frame', build_dummy_corpus())


def bound(c, ctx='ctx', nonce='n'):
    a = MockSigner('custodian-alice', Role.CUSTODIAN).sign(
        c.content_digest, ctx, nonce, capsule=c)
    b = MockSigner('adjudicator-bob', Role.SEMANTIC_ADJUDICATOR).sign(
        c.content_digest, ctx, nonce, capsule=c)
    return a, b


def witness_is_native():
    """Guard: the imported module really is the pinned OC4 blob."""
    import hashlib
    import subprocess
    blob = subprocess.check_output(['git', 'hash-object', CP.__file__]).decode().strip()
    assert blob == 'af2b7e943018077cb36808b5af1cd67704624bec', \
        f'imported module is not the pinned OC4 blob: {blob}'
    return True


# ---------------------------------------------------------------------------
# G0. The tests below really address the pinned native OC4 module
# ---------------------------------------------------------------------------

def test_imported_module_is_the_pinned_oc4_blob():
    assert CP.__file__.endswith('/source/custody_protocol.py')
    assert witness_is_native()
    assert hashlib_sha256(open(CP.__file__, 'rb').read()) == \
        '447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662e56f846f9e3a'


def hashlib_sha256(raw):
    import hashlib
    return hashlib.sha256(raw).hexdigest()


# ---------------------------------------------------------------------------
# G1. Normalization-equivalent aliases of ALLOWED fields
#     OC5 predicted 4 cases; these are independently re-derived.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('packet', [
    # OC5's four disclosed predictions, restated.
    {'public_projection': {'context': 'safe', 'ｃontext': 'shadow'}},
    {'public_projection': {'context': 'safe', 'con\u034ftext': 'shadow'}},
    {'public_projection': {'context': 'safe', 'CONT\u00c9XT': 'shadow'}},
    {'note': 'charming', 'n\u034fote': 'shadow'},
    # Reviewer extensions: every remaining allowed top-level key.
    {'menu': ['A'], '\uff4denu': ['B']},
    {'public_projection': {'context': 'safe'},
     '\uff50ublic_projection': {'context': 'shadow'}},
    {'note': 'safe', 'N\u00d3TE': 'shadow'},
    {'request_id': 'safe', 'requ\u0301est_id': 'shadow'},
    {'response': 'safe', 'RESPONS\u00cb': 'shadow'},
    # Two aliases at once, neither of which is the plain spelling.
    {'public_projection': {'context': 'safe', '\uff43ontext': 'a',
                           'con\u034ftext': 'b'}},
], ids=['fullwidth-context', 'cgj-context', 'accented-context', 'cgj-note',
        'fullwidth-menu', 'fullwidth-public-projection', 'accented-note',
        'accented-request-id', 'accented-response', 'double-context-alias'])
def test_normalization_equivalent_allowed_field_alias_must_be_refused(packet):
    """A packet must not silently admit a second normalization-equivalent
    spelling of an already-allowed field: the set comparison discards
    multiplicity, so the extra value is never type-checked nor scanned."""
    with pytest.raises(LeakageError):
        assert_no_leakage(packet)


def test_alias_holes_are_observed_not_theorised():
    """Direct observation: each HOLE packet currently yields no issue at all."""
    holes = [
        {'public_projection': {'context': 'safe', 'ｃontext': 'shadow'}},
        {'public_projection': {'context': 'safe', 'con\u034ftext': 'shadow'}},
        {'public_projection': {'context': 'safe', 'CONT\u00c9XT': 'shadow'}},
        {'note': 'charming', 'n\u034fote': 'shadow'},
        {'menu': ['A'], '\uff4denu': ['B']},
        {'public_projection': {'context': 'safe'},
         '\uff50ublic_projection': {'context': 'shadow'}},
        {'note': 'safe', 'N\u00d3TE': 'shadow'},
        {'request_id': 'safe', 'requ\u0301est_id': 'shadow'},
        {'response': 'safe', 'RESPONS\u00cb': 'shadow'},
    ]
    observed = {label: detect_leakage(packet) for label, packet in zip(
        ['fullwidth-context', 'cgj-context', 'accented-context', 'cgj-note',
         'fullwidth-menu', 'fullwidth-public-projection', 'accented-note',
         'accented-request-id', 'accented-response'], holes)}
    assert observed, 'observed'
    assert all(v == [] for v in observed.values()), \
        f'unexpectedly flagged: {observed}'
    # The multiplicity genuinely is discarded by the set comparison.
    inner = {'context': 'safe', 'ｃontext': 'shadow'}
    assert set(map(CP._normalized, inner)) == {'context'}
    assert len(inner) == 2


# ---------------------------------------------------------------------------
# G2. Controls that must NOT be weakened while closing G1
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('packet', [
    {'public_projection': {'CONT\u00c9XT': 'shadow'}},          # alias alone
    {'public_projection': {'con\u0301text': 'safe'}},          # genuinely other key
    {'schema_rubric': 'ok', 'schema\u0301rubric': 'x'},        # underscore differs
    {'note': 5},
    {'menu': 'not-a-list'},
    {'public_projection': {'context': ['a']}},
    {'public_projection': {'context': 'safe', 'hidden': 'x'}},
    {'note': 'The answ\u034fer_key is A'},
    {'note': 'ans\u200bwer_key is A'},
    {'note': '\uff41nswer_key is A'},
], ids=['alias-only-no-sibling', 'acute-i-context', 'underscore-differs',
        'note-non-str', 'menu-non-list', 'context-non-str', 'extra-public-key',
        'value-cgj', 'value-zwsp', 'value-fullwidth'])
def test_genuinely_other_or_invalid_packets_still_refused(packet):
    with pytest.raises(LeakageError):
        assert_no_leakage(packet)


def test_alias_values_are_still_type_checked_at_top_level():
    """The top-level check normalises every raw key, so an alias carrying a
    wrong-typed value is refused.  Only the MULTIPLICITY loss is a defect."""
    assert detect_leakage({'note': 'safe', 'n\u034fote': 5}) == \
        ['invalid_scalar_value_type']
    assert detect_leakage({'menu': ['A'], '\uff4denu': 5}) == \
        ['invalid_menu_value_type']
    assert detect_leakage({'response': 'ok', 'RESPONS\u00cb': ['x']}) == \
        ['invalid_scalar_value_type']


def test_valid_generated_packets_still_pass():
    from dummy_corpus import build_dummy_corpus as corpus
    for case in corpus():
        assert_no_leakage(CP) if False else None
        from dummy_corpus import build_model_visible_packet, build_coder_input
        assert_no_leakage(build_model_visible_packet(case))
        assert_no_leakage(build_coder_input(case, 'OPTION_A'))


# ---------------------------------------------------------------------------
# G3. NFKC-invisible confusable substitutions of leak tokens (reviewer-authored)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('value', [
    '\u0430nswer_key is A',       # Cyrillic a
    '\u0435xpected_result is A',  # Cyrillic e
    '\u0570idden_origin is A',    # Armenian h
    'l\u03bfwful_answers is A',   # Greek omicron
    '\u0441ontrast_label is A',   # Cyrillic es
    '\u0430ns\u0435er\u0455_key', # mixed Cyrillic
], ids=['cyrillic-a', 'cyrillic-e', 'armenian-h', 'greek-o', 'cyrillic-s',
        'mixed-cyrillic'])
def test_confusable_leak_token_substitution_must_be_flagged(value):
    """A visually present leak token written with NFKC-invisible homoglyphs is
    not detected, because scanning is normalization-based, not confusable-based."""
    with pytest.raises(LeakageError):
        assert_no_leakage({'note': value})


def test_confusable_holes_are_observed_only_for_nfkc_invisible_scripts():
    invisible = ['\u0430nswer_key is A', '\u0435xpected_result is A',
                 '\u0570idden_origin is A', 'l\u03bfwful_answers is A',
                 '\u0441ontrast_label is A']
    visible = ['ANSWER_KEY', 'answer_key', '\uff41nswer_key', 'ans\u200bwer_key',
               'ans\u034fwer_key']
    assert all(detect_leakage({'note': v}) == [] for v in invisible)
    assert all(detect_leakage({'note': v}) == ['answer_key'] for v in visible)


def test_genuinely_different_confusable_string_is_correctly_admitted():
    """U+FF39 '9' is NFKC-invisible to letters and is not a leak token at all."""
    assert detect_leakage({'note': '\uff39nswer_key'}) == []


# ---------------------------------------------------------------------------
# G4. Malformed signature objects — OC5's second prediction, confirmed
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('bad', [object(), 12, {'signature_hash': 'x'}, [1],
                                 'str', True, b'bytes', 3.5, ({},)],
                         ids=['object', 'int', 'dict', 'list', 'str', 'bool',
                              'bytes', 'float', 'tuple'])
@pytest.mark.parametrize('position', ['primary', 'second'])
def test_malformed_signature_object_must_fail_typed(bad, position):
    """Any non-None malformed signature object currently raises AttributeError
    instead of the protocol's SignatureError."""
    c = cap()
    a, b = bound(c)
    good = MockSignature('custodian-alice', Role.CUSTODIAN, c.content_digest,
                         'ctx', 'n', 'h')
    if position == 'primary':
        args = (c, bad, b, c.content_digest, 'ctx', 'n')
    else:
        args = (c, a, bad, c.content_digest, 'ctx', 'n')
    assert good is not None
    with pytest.raises(SignatureError):
        require_second_signature(*args)


def test_none_is_the_only_typed_malformed_signature():
    c = cap()
    a, b = bound(c)
    with pytest.raises(SignatureError, match='both signatures required'):
        require_second_signature(c, None, b, c.content_digest, 'ctx', 'n')
    with pytest.raises(SignatureError, match='both signatures required'):
        require_second_signature(c, a, None, c.content_digest, 'ctx', 'n')


def test_malformed_signature_holes_are_observed_as_attributeerror():
    c = cap()
    a, b = bound(c)
    for bad in (object(), 12, {'signature_hash': 'x'}, [1], 'str', True):
        for position in ('primary', 'second'):
            args = (c, bad, b, c.content_digest, 'ctx', 'n') if position == \
                'primary' else (c, a, bad, c.content_digest, 'ctx', 'n')
            with pytest.raises(AttributeError):
                require_second_signature(*args)


def test_non_enum_role_string_must_fail_typed():
    """A plain-string role on an otherwise valid signature currently raises
    AttributeError from MockSigner(...).sign(...) re-derivation."""
    c = cap()
    a, b = bound(c)
    with pytest.raises(SignatureError):
        require_second_signature(c, replace(a, role='CUSTODIAN'), b,
                                  c.content_digest, 'ctx', 'n')


def test_non_enum_role_string_hole_is_observed_as_attributeerror():
    c = cap()
    a, b = bound(c)
    with pytest.raises(AttributeError):
        require_second_signature(c, replace(a, role='CUSTODIAN'), b,
                                  c.content_digest, 'ctx', 'n')


# ---------------------------------------------------------------------------
# G5. Untyped holder identity and untyped capsule field types
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('holder', [['list'], {'dict': 1}, set()],
                         ids=['list', 'dict', 'set'])
def test_unblind_unhashable_holder_must_fail_typed(holder):
    c = cap()
    escrow = EscrowState()
    escrow.commit(c)
    with pytest.raises(IdentityMismatchError):
        escrow.unblind(c.capsule_id, holder)


@pytest.mark.parametrize('holder', [['list'], {'dict': 1}, set()],
                         ids=['list', 'dict', 'set'])
def test_unblind_unhashable_holder_hole_is_observed_as_typeerror(holder):
    c = cap()
    escrow = EscrowState()
    escrow.commit(c)
    with pytest.raises(TypeError):
        escrow.unblind(c.capsule_id, holder)


def test_unblind_scalar_holder_types_are_typed():
    c = cap()
    escrow = EscrowState()
    escrow.commit(c)
    for holder in (42, None, 3.5, True, b'x'):
        with pytest.raises(IdentityMismatchError):
            escrow.unblind(c.capsule_id, holder)


@pytest.mark.parametrize('field,value', [
    ('version', '2'), ('version', None), ('version', '1; DROP'),
    ('freeze_timestamp', None), ('freeze_timestamp', {'a': 1}),
    ('freeze_timestamp', 'now'), ('schema_version', None),
    ('content_digest', None), ('lawful_set_digest', None),
    ('coder_rubric_digest', None), ('split_assignment_digest', None),
], ids=['version-str', 'version-none', 'version-injection', 'freeze-none',
        'freeze-dict', 'freeze-str', 'schema-none', 'content-none',
        'lawful-none', 'rubric-none', 'split-none'])
def test_capsule_identity_field_types_must_be_validated(field, value):
    """Capsule identity/purpose/digest/version/freeze fields are accepted with
    any Python type, so the envelope commitment is computed over a coerced
    default=str projection rather than a validated contract."""
    c = cap()
    capsule = replace(c, **{field: value})
    escrow = EscrowState()
    with pytest.raises((TypeError, ValueError)):
        escrow.commit(capsule)


def test_capsule_identity_field_type_hole_is_observed():
    c = cap()
    committed = []
    for field, value in [('version', '2'), ('version', None),
                         ('freeze_timestamp', None),
                         ('freeze_timestamp', {'a': 1}),
                         ('schema_version', None), ('content_digest', None)]:
        escrow = EscrowState()
        capsule = replace(c, **{field: value})
        escrow.commit(capsule)
        committed.append((field, value))
    assert len(committed) == 6


def test_mixed_type_capsule_digest_dict_must_fail_typed():
    c = cap()
    broken = replace(c, lawful_set_digest={1: 'a', 'b': 2})
    with pytest.raises((TypeError, ValueError)):
        capsule_envelope_commitment(broken)
    with pytest.raises((TypeError, ValueError)):
        EscrowState().commit(broken)


def test_mixed_type_capsule_digest_dict_hole_is_observed_as_typeerror():
    c = cap()
    broken = replace(c, lawful_set_digest={1: 'a', 'b': 2})
    with pytest.raises(TypeError):
        capsule_envelope_commitment(broken)
    with pytest.raises(TypeError):
        EscrowState().commit(broken)


@pytest.mark.parametrize('facts', [{1: 'a', 'b': 2}, {None: 'a', 'b': 2},
                                  {(1, 2): 'a'}],
                         ids=['mixed-int-str', 'none-with-str', 'tuple-key'])
def test_semantic_fingerprint_mixed_keys_must_fail_typed(facts):
    with pytest.raises((TypeError, ValueError)):
        semantic_fingerprint(facts)


@pytest.mark.parametrize('facts', [{1: 'a', 'b': 2}, {None: 'a', 'b': 2},
                                  {(1, 2): 'a'}],
                         ids=['mixed-int-str', 'none-with-str', 'tuple-key'])
def test_semantic_fingerprint_hole_is_observed_as_typeerror(facts):
    with pytest.raises(TypeError):
        semantic_fingerprint(facts)


# ---------------------------------------------------------------------------
# G6. Full-capsule envelope commitment must bind every field (control)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('field', [
    f.name for f in dataclasses.fields(CustodyCapsule)])
def test_every_capsule_field_binds_the_envelope_commitment(field):
    c = cap()
    a, b = bound(c)
    if field in ('expired', 'revoked'):
        value = not getattr(c, field)
    elif field == 'version':
        value = c.version + 1
    elif field == 'freeze_timestamp':
        value = c.freeze_timestamp + 1.0
    else:
        value = 'SUBSTITUTED-' + field
    altered = replace(c, **{field: value})
    assert capsule_envelope_commitment(c) != capsule_envelope_commitment(altered), field
    with pytest.raises((SignatureError, PurposeViolationError, RevocationError)):
        require_second_signature(altered, a, b, c.content_digest, 'ctx', 'n')


def test_full_capsule_pair_positive_still_holds():
    c = cap()
    a, b = bound(c)
    assert require_second_signature(c, a, b, c.content_digest, 'ctx', 'n')
    assert MockSigner.verify(a, c.content_digest, 'ctx', 'n')


@pytest.mark.parametrize('ctx,nonce', [
    ('ctx-2', 'n'), ('ctx', 'n-2'), ('ctx', ''), ('ctx', ' ')], ids=[
    'wrong-context', 'wrong-nonce', 'empty-nonce', 'blank-nonce'])
def test_signature_context_and_nonce_binding(ctx, nonce):
    c = cap()
    a, b = bound(c)
    with pytest.raises(SignatureError):
        require_second_signature(c, a, b, c.content_digest, ctx, nonce)


@pytest.mark.parametrize('mutation', [
    dict(test_only=False), dict(verification_root='FOREIGN_ROOT'),
    dict(signer_person_id='intruder'), dict(content_digest='other'),
    dict(context_id='other'), dict(nonce='other'), dict(signature_hash='f' * 64),
], ids=['test-only', 'root', 'signer', 'content', 'context', 'nonce',
        'signature-hash'])
def test_signature_payload_tampering_refused(mutation):
    c = cap()
    a, b = bound(c)
    with pytest.raises(SignatureError):
        require_second_signature(c, replace(a, **mutation), b,
                                  c.content_digest, 'ctx', 'n')


def test_mock_verify_never_raises_and_fails_closed():
    c = cap()
    a, b = bound(c)
    for bad in (None, object(), 12, {}, 'x', [1], True):
        assert MockSigner.verify(bad, c.content_digest, 'ctx', 'n') is False
    for mutation in (dict(test_only=False), dict(verification_root='X'),
                     dict(context_id='Y'), dict(nonce='Z'),
                     dict(signature_hash='0' * 64)):
        assert MockSigner.verify(replace(a, **mutation), c.content_digest,
                                 'ctx', 'n') is False


# ---------------------------------------------------------------------------
# G7. Escrow integrity: event sealing, immutability, unblind-after-mutation
# ---------------------------------------------------------------------------

def _released_escrow():
    c = cap()
    escrow = EscrowState()
    escrow.commit(c)
    escrow.unblind(c.capsule_id, 'runner1')
    escrow.release(c.capsule_id)
    return c, escrow


@pytest.mark.parametrize('mutate', [
    'unblind-capsule-id', 'unblind-unblinded-at', 'unblind-holder',
    'unblind-lawful-answers', 'committed-object-swapped', 'committed-key-added',
    'exposure-log-appended', 'ledger-appended', 'ledger-dropped',
    'ledger-seq-rewritten', 'capsule-seals-rewritten', 'event-proofs-dropped',
], ids=['unblind-id', 'unblind-at', 'unblind-holder', 'unblind-lawful',
        'committed-swap', 'committed-key', 'exposure', 'ledger-add',
        'ledger-drop', 'ledger-seq', 'seals', 'proofs'])
def test_every_escrow_event_mutation_is_detected(mutate):
    capsule, escrow = _released_escrow()
    tampered = deepcopy(escrow)
    key = capsule.capsule_id
    if mutate == 'unblind-capsule-id':
        tampered.unblinded[key]['capsule_id'] = 'INTRUDER'
    elif mutate == 'unblind-unblinded-at':
        tampered.unblinded[key]['unblinded_at'] = -999
    elif mutate == 'unblind-holder':
        tampered.unblinded[key]['holder'] = 'intruder'
    elif mutate == 'unblind-lawful-answers':
        tampered.unblinded[key]['lawful_answers'] = ['FORGED']
    elif mutate == 'committed-object-swapped':
        tampered.committed[key] = replace(tampered.committed[key],
                                           content_digest='FORGED')
    elif mutate == 'committed-key-added':
        tampered.committed['GHOST'] = tampered.committed[key]
    elif mutate == 'exposure-log-appended':
        tampered.exposure_log.append({'event': 'FORGED'})
    elif mutate == 'ledger-appended':
        tampered.ledger.append({'event': 'FORGED'})
    elif mutate == 'ledger-dropped':
        tampered.ledger.pop(0)
    elif mutate == 'ledger-seq-rewritten':
        tampered._ledger_seq = 999
    elif mutate == 'capsule-seals-rewritten':
        tampered._capsule_seals[key] = 'FORGED'
    elif mutate == 'event-proofs-dropped':
        tampered._event_proofs.pop(0)
    assert escrow.verify_ledger_integrity() is True
    assert tampered.verify_ledger_integrity() is False


def test_holder_grant_registry_is_outside_the_event_seal():
    """The holder grant registry is a mutable precondition registry by design;
    its substitution is NOT event-sealed, and authorize_holder itself neither
    validates the grant type at ledger level nor is sealed.  Recorded as an
    observation with its boundary: the substitute still fails unblind, and a
    non-CUSTODIAN grant is refused at authorize_holder."""
    capsule, escrow = _released_escrow()
    substituted = deepcopy(escrow)
    substituted.holder_roles['runner1'] = Role.SCENARIO_AUTHOR
    assert substituted.verify_ledger_integrity() is True
    with pytest.raises(IdentityMismatchError):
        substituted.unblind(capsule.capsule_id, 'runner1')
    fresh = EscrowState()
    with pytest.raises(ConflictError):
        fresh.authorize_holder('x', Role.EXPERIMENT_RUNNER)
    fresh.authorize_holder('x', Role.CUSTODIAN)
    assert fresh.verify_ledger_integrity() is True


def test_unblind_receipt_alias_does_not_change_retained_integrity():
    c = cap()
    escrow = EscrowState()
    escrow.commit(c)
    receipt = escrow.unblind(c.capsule_id, 'runner1')
    receipt['unblinded_at'] = -1
    receipt['holder'] = 'intruder'
    assert escrow.verify_ledger_integrity() is True
    assert escrow.unblinded[c.capsule_id]['unblinded_at'] != -1


@pytest.mark.parametrize('stage,expected', [
    ('revoked', RevocationError), ('expired', RevocationError),
    ('illegal-purpose', PurposeViolationError),
    ('uncommitted', IdentityMismatchError), ('no-grant', IdentityMismatchError),
    ('double-commit', None), ('double-release', None)], ids=[
    'revoked', 'expired', 'illegal-purpose', 'uncommitted', 'no-grant',
    'double-commit', 'double-release'])
def test_escrow_lifecycle_early_refusals(stage, expected):
    corpus = build_dummy_corpus()
    if stage == 'revoked':
        capsule = build_capsule('SOURCEFREE_TEST_ONLY', 'f', corpus)
        capsule = replace(capsule, revoked=True)
        escrow, commit_raises = EscrowState(), RevocationError
    elif stage == 'expired':
        capsule = build_capsule('SOURCEFREE_TEST_ONLY', 'f', corpus)
        capsule = replace(capsule, expired=True)
        escrow, commit_raises = EscrowState(), RevocationError
    elif stage == 'illegal-purpose':
        capsule = build_capsule('SOURCEFREE_TEST_ONLY', 'f', corpus)
        capsule = replace(capsule, purpose='LIVE_MODEL_REQUEST')
        escrow, commit_raises = EscrowState(), PurposeViolationError
    elif stage == 'uncommitted':
        capsule = build_capsule('SOURCEFREE_TEST_ONLY', 'f', corpus)
        escrow, commit_raises = EscrowState(), None
    elif stage == 'no-grant':
        capsule = build_capsule('SOURCEFREE_TEST_ONLY', 'f', corpus)
        escrow, commit_raises = EscrowState(), None
    else:
        capsule = build_capsule('SOURCEFREE_TEST_ONLY', 'f', corpus)
        escrow, commit_raises = EscrowState(), None
    if stage in ('revoked', 'expired', 'illegal-purpose'):
        with pytest.raises(commit_raises):
            escrow.commit(capsule)
        return
    if stage == 'uncommitted':
        with pytest.raises(IdentityMismatchError):
            escrow.unblind(capsule.capsule_id, 'runner1')
        return
    escrow.commit(capsule)
    if stage == 'no-grant':
        with pytest.raises(IdentityMismatchError):
            escrow.unblind(capsule.capsule_id, 'stranger')
        return
    with pytest.raises(Exception):
        escrow.commit(capsule)
    escrow.unblind(capsule.capsule_id, 'runner1')
    escrow.release(capsule.capsule_id)
    with pytest.raises(Exception):
        escrow.release(capsule.capsule_id)


def test_ledger_rollback_is_always_refused_typed():
    c = cap()
    escrow = EscrowState()
    escrow.commit(c)
    with pytest.raises(CP.LedgerRollbackError):
        escrow.rollback_ledger(1)


# ---------------------------------------------------------------------------
# G8. Blind-ID trial pairing typed refusals
# ---------------------------------------------------------------------------

def _trials(nonce, arms, **extra):
    rows = []
    for index, arm in enumerate(arms):
        row = {'public_nonce': nonce, 'arm': arm, 'trial_id': f'{nonce}{index}'}
        row.update(extra)
        rows.append(row)
    return rows


@pytest.mark.parametrize('trials', [
    _trials('n1', ['A', 'A', 'C']),
    _trials('n1', ['A', 'B']),
    _trials('', ['A', 'B', 'C']),
    _trials('   ', ['A', 'B', 'C']),
    [],
    'not-a-list',
    _trials('n1', [[], 'B', 'C']),
    _trials('n1', [{}, 'B', 'C']),
    _trials('n1', [42, 'B', 'C']),
    _trials('n1', [None, 'B', 'C']),
    _trials('n1', ['A', 'B', 'C', 'A']),
    [{'public_nonce': 'n', 'arm': 'A', 'trial_id': 't',
      'case_id': 'c1'},
     {'public_nonce': 'n', 'arm': 'B', 'trial_id': 't', 'case_id': 'c1'},
     {'public_nonce': 'n', 'arm': 'C', 'trial_id': 't2', 'case_id': 'c2'}],
    [{'public_nonce': 'n', 'arm': 'A', 'trial_id': 't1', 'case_id': 5},
     {'public_nonce': 'n', 'arm': 'B', 'trial_id': 't2'},
     {'public_nonce': 'n', 'arm': 'C', 'trial_id': 't3'},
     ],
    ['not-a-dict'],
], ids=['two-A', 'two-arms', 'blank-nonce', 'whitespace-nonce', 'empty-list',
        'string', 'unhashable-arm', 'dict-arm', 'int-arm', 'none-arm',
        'extra-arm', 'inconsistent-case-join', 'int-case-join', 'non-dict'])
def test_blind_pairing_malformed_inputs_are_typed(trials):
    with pytest.raises(BlindIDPairingError):
        verify_blind_pairing(trials)


@pytest.mark.parametrize('block_size', [1, 2, 4, 0], ids=['b1', 'b2', 'b4', 'b0'])
def test_blind_pairing_block_size_must_be_three(block_size):
    with pytest.raises(BlindIDPairingError):
        verify_blind_pairing(_trials('n', ['A', 'B', 'C']), block_size=block_size)


def test_blind_pairing_valid_three_arm_blocks_pass():
    trials = (_trials('n1', ['A', 'B', 'C'], case_id='c1', family_id='f1') +
              _trials('n2', ['C', 'A', 'B']))
    assert verify_blind_pairing(trials) is True


# ---------------------------------------------------------------------------
# G9. Purpose discipline and family-clone separation (controls)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('purpose', ['LIVE_MODEL_REQUEST', 'SOURCE_USE', '', None],
                         ids=['live-model', 'source-use', 'empty', 'none'])
def test_unauthorized_purposes_refused_typed(purpose):
    with pytest.raises(PurposeViolationError):
        CP.verify_purpose(purpose)


def test_authorized_purposes_accepted():
    for purpose in CP.ALLOWED_PURPOSES:
        assert CP.verify_purpose(purpose) is None


def test_escrow_commit_refuses_inactive_capsule_before_any_state_change():
    c = cap()
    escrow = EscrowState()
    with pytest.raises(RevocationError):
        escrow.commit(replace(c, revoked=True))
    assert escrow.committed == {}
    with pytest.raises(RevocationError):
        escrow.commit(replace(c, expired=True))
    assert escrow.committed == {}
