"""OC6 — author-side targeted controls for the repaired input contracts.

Every test runs at the actual repaired entrypoints in the STAGED custody
candidate (never a transcribed excerpt).  Cases are grouped by the OC6 family
they fence: A1 normalized-duplicate aliases, A2 bounded confusable tokens,
A3 malformed signature objects, A4 role identities, A5 malformed holders, and
A6 capsule field types.

TEST_ONLY sourcefree custody scope only.  A mock signer does not create real
independent custody, and a lexical/schema check does not establish universal
semantic non-leakage.
"""
from __future__ import annotations

import dataclasses
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
    detect_leakage,
    detect_family_clone,
    require_second_signature,
    semantic_fingerprint,
    validate_capsule_fields,
)
from dummy_corpus import build_capsule, build_dummy_corpus


def cap():
    return build_capsule('SOURCEFREE_TEST_ONLY', 'oc6-frame', build_dummy_corpus())


def bound(c, ctx='ctx', nonce='n'):
    a = MockSigner('custodian-alice', Role.CUSTODIAN).sign(
        c.content_digest, ctx, nonce, capsule=c)
    b = MockSigner('adjudicator-bob', Role.SEMANTIC_ADJUDICATOR).sign(
        c.content_digest, ctx, nonce, capsule=c)
    return a, b


# ---------------------------------------------------------------------------
# A1 — normalization-equivalent duplicate allowed-field aliases
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('packet', [
    {'public_projection': {'context': 'safe', 'ｃontext': 'shadow'}},
    {'public_projection': {'context': 'safe', 'con\u034ftext': 'shadow'}},
    {'public_projection': {'context': 'safe', 'CONT\u00c9XT': 'shadow'}},
    {'note': 'charming', 'n\u034fote': 'shadow'},
    {'note': 'safe', 'N\u00d3TE': 'shadow'},
    {'request_id': 'safe', 'requ\u0301est_id': 'shadow'},
    {'response': 'safe', 'RESPONS\u00cb': 'shadow'},
    {'menu': ['A'], '\uff4denu': ['B']},
    {'public_projection': {'context': 'safe'},
     '\uff50ublic_projection': {'context': 'shadow'}},
    {'public_projection': {'context': 'safe', '\uff43ontext': 'a',
                           'con\u034ftext': 'b'}},
], ids=['fullwidth-context', 'cgj-context', 'accented-context', 'cgj-note',
        'accented-note', 'accented-request-id', 'accented-response',
        'fullwidth-menu', 'fullwidth-public-projection', 'double-context-alias'])
def test_a1_normalization_equivalent_duplicate_alias_refused(packet):
    with pytest.raises(LeakageError):
        assert_no_leakage(packet)


@pytest.mark.parametrize('packet', [
    # a single canonical spelling of each allowed field
    {'public_projection': {'context': 'safe'}},
    {'note': 'charming'},
    {'menu': ['A', 'B'], 'request_id': 'r'},
    {'response': 'yes', 'schema_rubric': 'rubric'},
    {'public_projection': {'context': 'a'}, 'note': 'b', 'menu': ['A'],
     'request_id': 'r', 'response': 'x', 'schema_rubric': 's'},
    # genuinely distinct normalized spellings are still separate fields
    {'public_projection': {'context': 'safe'}, 'note': 'n'},
    # an alias carrying an invalid value is already refused, and its code
    # stays exactly the value type error (no spurious extra code)
    {'note': 'safe', 'n\u034fote': 5},
    {'menu': ['A'], '\uff4denu': 5},
    {'response': 'ok', 'RESPONS\u00cb': ['x']},
    # an alias alone (no canonical sibling) is refused by the value type check
    {'public_projection': {'CONT\u00c9XT': 'shadow'}},
], ids=['context-only', 'note-only', 'menu+request', 'response+rubric',
        'all-six-single', 'two-distinct-fields', 'alias-value-nonstr',
        'menu-alias-nonlist', 'response-alias-nonstr', 'alias-alone'])
def test_a1_single_and_invalid_controls_behave_exactly(packet):
    issues = detect_leakage(packet)
    if issues:
        # still refused, and never with a duplicate-alias code
        assert not any(i.startswith('duplicate_normalized_field')
                       for i in issues), issues
    else:
        assert issues == []


def test_a1_duplicate_alias_value_is_never_a_second_admitted_value():
    """The alias value must not be reachable as the field's value."""
    packet = {'public_projection': {'context': 'safe', '\uff43ontext': 'shadow'}}
    issues = detect_leakage(packet)
    assert issues == ['duplicate_normalized_field:\uff43ontext']
    # the only value the raw lookup can reach is the canonical one
    assert packet['public_projection'].get('context') == 'safe'


def test_a1_multiplicity_is_not_discarded_for_the_canonical_pair():
    """Two different normalizations of the same allowed key cannot coexist."""
    inner = {'context': 'safe', '\uff43ontext': 'shadow'}
    assert set(map(CP._normalized, inner)) == {'context'}
    assert len(inner) == 2
    assert CP._normalized('\uff43ontext') == 'context'


# ---------------------------------------------------------------------------
# A2 — bounded, NFKC-invisible confusable spellings of denied leak tokens
# ---------------------------------------------------------------------------

# Each value below spells a REAL denied token with one NFKC-invisible
# homoglyph substituted.  These are the correctly spelled controls.
@pytest.mark.parametrize('value', [
    '\u0430nswer_key is A',           # Cyrillic a -> a      = answer_key
    '\u0435xpected_result is A',      # Cyrillic e -> e      = expected_result
    '\u0570idden_origin is A',        # Armenian  հ -> h     = hidden_origin
    'c\u03bfntrast_label is A',       # Greek    ο -> o      = contrast_label
    '\u0441ontrast_label is A',       # Cyrillic с -> c      = contrast_label
    'expected_r\u0435sult',           # Cyrillic е -> e      = expected_result
    '\u0435xp\u0435\u0441t\u0435d_result',   # Cyrillic е/е/с/е  = expected_result
], ids=['cyrillic-a', 'cyrillic-e', 'armenian-h', 'greek-o', 'cyrillic-s',
        'cyrillic-e-mid', 'cyrillic-many'])
def test_a2_confusable_leak_token_spelling_refused(value):
    with pytest.raises(LeakageError):
        assert_no_leakage({'note': value})


@pytest.mark.parametrize('value', [
    'ANSWER_KEY', 'answer_key', '\uff41nswer_key', 'ans\u200bwer_key',
    'ans\u034fwer_key', 'expected_result', 'hidden_origin',
], ids=['upper', 'plain', 'fullwidth-a', 'zwsp', 'cgj', 'expected', 'hidden'])
def test_a2_nfkc_visible_and_plain_spellings_still_flagged(value):
    assert detect_leakage({'note': value})


@pytest.mark.parametrize('value,expected', [
    ('\uff39nswer_key', []),            # U+FF39 '9': NFKC-invisible, NOT a letter
    ('charming', []),
    ('A quiet afternoon', []),
    ('legitimate multiling\xfcal t\u00e9xt', []),
    ('\u4f60\u597d\u4e16\u754c', []),   # CJK: no Latin homoglyphs
    ('\u043f\u0440\u0438\u0432\u0435\u0442 \u043c\u0438\u0440', []),  # Cyrillic word
    ('\u03bb\u03cc\u03b3\u03bf\u03c2 \u03b5\u03bb\u03bb\u03ac\u03b4\u03b1', []),  # Greek word
], ids=['digit-9', 'plain-word', 'sentence', 'accented-latin', 'cjk',
        'cyrillic-word', 'greek-word'])
def test_a2_legitimate_multilingual_and_confusable_non_tokens_admitted(value, expected):
    """Multilingual text and non-token confusables are not refused by fiat."""
    assert detect_leakage({'note': value}) == expected


def test_a2_confusable_fold_is_bounded_and_enumerated():
    """The fold map is an explicit, finite, NFKC-invisible homoglyph table."""
    fold = CP._CONFUSABLE_FOLD
    from types import MappingProxyType
    assert isinstance(fold, MappingProxyType)
    assert fold, 'fold map must be nonempty'
    for source, target in fold.items():
        assert len(source) == 1 and len(target) == 1 and target.isascii()
        # every mapped source must survive NFKC/NFKD unchanged (else the
        # normalization path already covers it and no fold is needed)
        assert CP._ud.normalize('NFKC', source) == source
        assert CP._ud.normalize('NFKD', source) == source
        assert CP._ud.category(source) not in {'Cf', 'Cc', 'Mn', 'Me'}


def test_a2_fold_never_feeds_the_field_allowlist():
    """A confusable field spelling is still an unapproved field, fail-closed."""
    # Cyrillic es standing in for the denied token 'case_id' as a KEY
    issues = detect_leakage({'\u0441ase_id': 'x'})
    assert issues == ['unapproved_field:\u0441ase_id']
    # Cyrillic es standing in for the ALLOWED field 'note' is still unapproved
    assert detect_leakage({'n\u043ete': 'x'}) == ['unapproved_field:n\u043ete']


def test_a2_no_claim_of_universal_semantic_non_leakage():
    """The gate stays a lexical/schema gate; it does not solve semantics."""
    assert detect_leakage({'note': 'the answr key is A'}) == []
    assert detect_leakage({'note': 'r3sult k3y'}) == []
    assert detect_leakage({'note': 'answer\u2212key'}) == []  # minus sign, not _
    with pytest.raises(LeakageError):
        assert_no_leakage({'note': 'a genuine answer_key token'})


# ---------------------------------------------------------------------------
# A3 — malformed signature objects must produce a typed SignatureError
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('bad', [object(), 12, {'signature_hash': 'x'}, [1],
                                 'str', True, b'bytes', 3.5, ('t',), None],
                         ids=['object', 'int', 'dict', 'list', 'str', 'bool',
                              'bytes', 'float', 'tuple', 'none'])
@pytest.mark.parametrize('position', ['primary', 'second'])
def test_a3_malformed_signature_object_is_typed(bad, position):
    c = cap()
    a, b = bound(c)
    args = ((c, bad, b, c.content_digest, 'ctx', 'n') if position == 'primary'
            else (c, a, bad, c.content_digest, 'ctx', 'n'))
    with pytest.raises(SignatureError):
        require_second_signature(*args)


@pytest.mark.parametrize('bad', [object(), 12, {'signature_hash': 'x'}, [1],
                                 'str', True, b'bytes', 3.5, ('t',)],
                         ids=['object', 'int', 'dict', 'list', 'str', 'bool',
                              'bytes', 'float', 'tuple'])
def test_a3_malformed_object_never_raises_attributeerror(bad):
    c = cap()
    a, b = bound(c)
    for position in ('primary', 'second'):
        args = ((c, bad, b, c.content_digest, 'ctx', 'n') if position == 'primary'
                else (c, a, bad, c.content_digest, 'ctx', 'n'))
        try:
            require_second_signature(*args)
        except SignatureError:
            continue
        except AttributeError:  # pragma: no cover - regression guard
            raise AssertionError(
                f'untyped AttributeError for {position} {bad!r}')
        else:  # pragma: no cover - regression guard
            raise AssertionError('malformed signature silently accepted')


def test_a3_none_is_still_the_only_typed_none_case():
    c = cap()
    a, b = bound(c)
    for args in ((c, None, b, c.content_digest, 'ctx', 'n'),
                 (c, a, None, c.content_digest, 'ctx', 'n')):
        with pytest.raises(SignatureError, match='both signatures required'):
            require_second_signature(*args)


# ---------------------------------------------------------------------------
# A4 — signature role identity must be a Role enum
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('bad_role', ['CUSTODIAN', 'custodian', '', None, 12,
                                      Role.CUSTODIAN.value],
                         ids=['upper-str', 'lower-str', 'empty', 'none', 'int',
                              'value-str'])
@pytest.mark.parametrize('position', ['primary', 'second'])
def test_a4_non_enum_role_is_typed_refusal(bad_role, position):
    c = cap()
    a, b = bound(c)
    target = replace(a, role=bad_role) if position == 'primary' else \
        replace(b, role=bad_role)
    other = b if position == 'primary' else a
    with pytest.raises(SignatureError):
        require_second_signature(c, target, other, c.content_digest, 'ctx', 'n')


def test_a4_non_enum_role_never_raises_attributeerror():
    c = cap()
    a, b = bound(c)
    for position in ('primary', 'second'):
        target = replace(a, role='CUSTODIAN') if position == 'primary' \
            else replace(b, role='CUSTODIAN')
        other = b if position == 'primary' else a
        try:
            require_second_signature(c, target, other, c.content_digest, 'ctx', 'n')
        except SignatureError:
            continue
        except AttributeError:  # pragma: no cover - regression guard
            raise AssertionError('untyped AttributeError for non-enum role')
        else:  # pragma: no cover - regression guard
            raise AssertionError('non-enum role silently accepted')


def test_a4_mock_signer_rejects_non_enum_role_typed():
    with pytest.raises(TypeError):
        MockSigner('custodian-alice', 'CUSTODIAN')
    with pytest.raises(TypeError):
        MockSigner('custodian-alice', None)
    with pytest.raises(TypeError):
        MockSigner('', Role.CUSTODIAN)


def test_a4_mock_verify_still_fails_closed_on_a_non_enum_role():
    c = cap()
    a, _b = bound(c)
    assert MockSigner.verify(replace(a, role='CUSTODIAN'), c.content_digest,
                             'ctx', 'n') is False


# ---------------------------------------------------------------------------
# A5 — malformed holder identities must produce a typed refusal
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('holder', [['list'], {'dict': 1}, set(), ('t',), 12,
                                    3.5, True, b'x', None, '', '   '],
                         ids=['list', 'dict', 'set', 'tuple', 'int', 'float',
                              'bool', 'bytes', 'none', 'empty', 'blank'])
def test_a5_malformed_holder_identity_is_typed(holder):
    c = cap()
    escrow = EscrowState()
    escrow.commit(c)
    with pytest.raises(IdentityMismatchError):
        escrow.unblind(c.capsule_id, holder)


@pytest.mark.parametrize('holder', [['list'], {'dict': 1}, set()],
                         ids=['list', 'dict', 'set'])
def test_a5_unhashable_holder_never_raises_typeerror(holder):
    c = cap()
    escrow = EscrowState()
    escrow.commit(c)
    try:
        escrow.unblind(c.capsule_id, holder)
    except IdentityMismatchError:
        return
    except TypeError:  # pragma: no cover - regression guard
        raise AssertionError('untyped TypeError for unhashable holder')
    else:  # pragma: no cover - regression guard
        raise AssertionError('unhashable holder silently accepted')


def test_a5_authorized_holder_still_works_and_receipt_is_a_deepcopy_alias():
    c = cap()
    escrow = EscrowState()
    escrow.commit(c)
    receipt = escrow.unblind(c.capsule_id, 'runner1')
    assert receipt['holder'] == 'runner1'
    receipt['holder'] = 'intruder'
    receipt['unblinded_at'] = -1
    assert escrow.unblinded[c.capsule_id]['holder'] == 'runner1'
    assert escrow.verify_ledger_integrity() is True
    escrow.release(c.capsule_id)
    with pytest.raises(IdentityMismatchError):
        escrow.unblind(c.capsule_id, 'stranger')


def test_a5_holder_grant_authorization_is_still_typed():
    escrow = EscrowState()
    with pytest.raises(IdentityMismatchError):
        escrow.authorize_holder('', Role.CUSTODIAN)
    with pytest.raises(IdentityMismatchError):
        escrow.authorize_holder('x', 'CUSTODIAN')
    with pytest.raises(ConflictError):
        escrow.authorize_holder('x', Role.EXPERIMENT_RUNNER)
    escrow.authorize_holder('x', Role.CUSTODIAN)
    assert escrow.holder_roles['x'] == Role.CUSTODIAN


# ---------------------------------------------------------------------------
# A6 — capsule identity / digest / version / freeze field types
# ---------------------------------------------------------------------------

_IDENTITY_FIELDS = (
    'capsule_id', 'schema_version', 'scenario_frame', 'family_graph_digest',
    'content_digest', 'contribution_digest', 'public_projection_digest',
    'hidden_projection_digest', 'lawful_set_digest', 'coder_rubric_digest',
    'split_assignment_digest', 'generation_history_digest',
    'rejected_alternatives_digest',
)


@pytest.mark.parametrize('field', _IDENTITY_FIELDS)
@pytest.mark.parametrize('bad', [None, 12, {'a': 1}, ['a'], ('a',), b'x', 1.5, True],
                         ids=['none', 'int', 'dict', 'list', 'tuple', 'bytes',
                              'float', 'bool'])
def test_a6_identity_and_digest_fields_require_nonempty_strings(field, bad):
    c = cap()
    with pytest.raises(TypeError):
        validate_capsule_fields(replace(c, **{field: bad}))
    escrow = EscrowState()
    with pytest.raises(TypeError):
        escrow.commit(replace(c, **{field: bad}))
    with pytest.raises(TypeError):
        capsule_envelope_commitment(replace(c, **{field: bad}))


@pytest.mark.parametrize('field', _IDENTITY_FIELDS)
def test_a6_identity_and_digest_fields_accept_valid_strings(field):
    c = cap()
    validate_capsule_fields(replace(c, **{field: 'SUBSTITUTED-' + field}))
    assert capsule_envelope_commitment(
        replace(c, **{field: 'SUBSTITUTED-' + field})) != \
        capsule_envelope_commitment(c)


@pytest.mark.parametrize('bad', ['2', None, '1; DROP', 1.5, True, [1], {'a': 1}],
                         ids=['str', 'none', 'injection', 'float', 'bool', 'list',
                              'dict'])
def test_a6_version_requires_a_positive_integer(bad):
    c = cap()
    with pytest.raises(TypeError):
        validate_capsule_fields(replace(c, version=bad))
    with pytest.raises(TypeError):
        EscrowState().commit(replace(c, version=bad))


def test_a6_version_zero_and_negative_are_refused():
    c = cap()
    for bad in (0, -1, -99):
        with pytest.raises(TypeError):
            validate_capsule_fields(replace(c, version=bad))


@pytest.mark.parametrize('bad', [None, 'now', {'a': 1}, ['x'], True],
                         ids=['none', 'str', 'dict', 'list', 'bool'])
def test_a6_freeze_timestamp_requires_a_finite_nonnegative_number(bad):
    c = cap()
    with pytest.raises(TypeError):
        validate_capsule_fields(replace(c, freeze_timestamp=bad))
    with pytest.raises(TypeError):
        EscrowState().commit(replace(c, freeze_timestamp=bad))


def test_a6_freeze_timestamp_accepts_a_valid_number():
    c = cap()
    for good in (0.0, 1.0, 1760000000.5, 3):
        validate_capsule_fields(replace(c, freeze_timestamp=good))


@pytest.mark.parametrize('field', ['expired', 'revoked'])
@pytest.mark.parametrize('bad', [None, 0, 1, 'true', [], {}],
                         ids=['none', 'zero', 'one', 'str', 'list', 'dict'])
def test_a6_lifecycle_flags_require_booleans(field, bad):
    c = cap()
    with pytest.raises(TypeError):
        validate_capsule_fields(replace(c, **{field: bad}))


def test_a6_invalid_declaration_leaves_no_state_and_no_ledger_entry():
    c = cap()
    escrow = EscrowState()
    before_ledger = len(escrow.ledger)
    with pytest.raises(TypeError):
        escrow.commit(replace(c, version='2'))
    assert escrow.committed == {}
    assert len(escrow.ledger) == before_ledger
    assert escrow.verify_ledger_integrity() is True


def test_a6_mixed_type_digest_dict_is_refused_before_any_commitment():
    c = cap()
    broken = replace(c, lawful_set_digest={1: 'a', 'b': 2})
    with pytest.raises(TypeError):
        capsule_envelope_commitment(broken)
    with pytest.raises(TypeError):
        EscrowState().commit(broken)
    with pytest.raises(TypeError):
        validate_capsule_fields(broken)


def test_a6_semantic_fingerprint_requires_string_keys():
    for bad in ({1: 'a', 'b': 2}, {None: 'a', 'b': 2}, {(1, 2): 'a'}, {}, 'x', None):
        with pytest.raises(TypeError):
            semantic_fingerprint(bad)
    assert semantic_fingerprint({'a': '1'})
    assert detect_family_clone({'a': '1'}, {'a': '1'}, frozenset()) is True


def test_a6_all_eighteen_capsule_fields_still_bind_the_envelope():
    c = cap()
    a, b = bound(c)
    for f in dataclasses.fields(CustodyCapsule):
        if f.name in ('expired', 'revoked'):
            value = not getattr(c, f.name)
        elif f.name == 'version':
            value = c.version + 1
        elif f.name == 'freeze_timestamp':
            value = c.freeze_timestamp + 1.0
        else:
            value = 'SUBSTITUTED-' + f.name
        altered = replace(c, **{f.name: value})
        assert capsule_envelope_commitment(c) != capsule_envelope_commitment(altered)
        with pytest.raises((SignatureError, PurposeViolationError, RevocationError)):
            require_second_signature(altered, a, b, c.content_digest, 'ctx', 'n')


def test_a6_valid_declaration_still_commits_and_unblinds():
    c = cap()
    escrow = EscrowState()
    escrow.commit(c)
    escrow.unblind(c.capsule_id, 'runner1')
    escrow.release(c.capsule_id)
    assert escrow.verify_ledger_integrity() is True


# ---------------------------------------------------------------------------
# Preserved contracts that must not be weakened by the repair
# ---------------------------------------------------------------------------

def test_full_capsule_commitment_positive_still_holds():
    c = cap()
    a, b = bound(c)
    assert require_second_signature(c, a, b, c.content_digest, 'ctx', 'n')
    assert MockSigner.verify(a, c.content_digest, 'ctx', 'n')


@pytest.mark.parametrize('ctx,nonce', [
    ('ctx-2', 'n'), ('ctx', 'n-2'), ('ctx', ''), ('ctx', ' ')],
    ids=['wrong-context', 'wrong-nonce', 'empty-nonce', 'blank-nonce'])
def test_signature_context_and_nonce_binding_preserved(ctx, nonce):
    c = cap()
    a, b = bound(c)
    with pytest.raises(SignatureError):
        require_second_signature(c, a, b, c.content_digest, ctx, nonce)


@pytest.mark.parametrize('mutation', [
    dict(test_only=False), dict(verification_root='FOREIGN_ROOT'),
    dict(signer_person_id='intruder'), dict(content_digest='other'),
    dict(context_id='other'), dict(nonce='other'),
    dict(signature_hash='f' * 64)],
    ids=['test-only', 'root', 'signer', 'content', 'context', 'nonce',
         'signature-hash'])
def test_signature_payload_tampering_preserved(mutation):
    c = cap()
    a, b = bound(c)
    with pytest.raises(SignatureError):
        require_second_signature(c, replace(a, **mutation), b,
                                 c.content_digest, 'ctx', 'n')


def test_mock_verify_never_raises_and_fails_closed():
    c = cap()
    a, _b = bound(c)
    for bad in (None, object(), 12, {}, 'x', [1], True):
        assert MockSigner.verify(bad, c.content_digest, 'ctx', 'n') is False
    for mutation in (dict(test_only=False), dict(verification_root='X'),
                     dict(context_id='Y'), dict(nonce='Z'),
                     dict(signature_hash='0' * 64)):
        assert MockSigner.verify(replace(a, **mutation), c.content_digest,
                                 'ctx', 'n') is False


def test_generated_packets_still_pass_the_leakage_gate():
    from dummy_corpus import (build_coder_input, build_model_visible_packet,
                              build_dummy_corpus as corpus)
    for case in corpus():
        assert_no_leakage(build_model_visible_packet(case))
        assert_no_leakage(build_coder_input(case, 'OPTION_A'))


def test_three_arm_blind_pairing_preserved():
    rows = [{'public_nonce': 'n1', 'arm': arm, 'trial_id': f'n1{i}',
             'case_id': 'c1'} for i, arm in enumerate('ABC')]
    assert CP.verify_blind_pairing(rows) is True
    for malformed in ([], 'x', [{'public_nonce': 'n', 'arm': 'A'},
                                {'public_nonce': 'n', 'arm': 'A'},
                                {'public_nonce': 'n', 'arm': 'C'}]):
        with pytest.raises(BlindIDPairingError):
            CP.verify_blind_pairing(malformed)


def test_purpose_discipline_preserved():
    for bad in ('LIVE_MODEL_REQUEST', 'SOURCE_USE', '', None):
        with pytest.raises(PurposeViolationError):
            CP.verify_purpose(bad)
    for good in CP.ALLOWED_PURPOSES:
        assert CP.verify_purpose(good) is None


def test_append_only_escrow_preserved():
    c = cap()
    escrow = EscrowState()
    escrow.commit(c)
    with pytest.raises(CP.LedgerRollbackError):
        escrow.rollback_ledger(1)
    assert escrow.verify_ledger_integrity() is True


def test_inactive_capsule_refused_before_any_state_change():
    c = cap()
    escrow = EscrowState()
    with pytest.raises(RevocationError):
        escrow.commit(replace(c, revoked=True))
    assert escrow.committed == {}
    with pytest.raises(RevocationError):
        escrow.commit(replace(c, expired=True))
    assert escrow.committed == {}
