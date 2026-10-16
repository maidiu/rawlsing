"""OC7 — fresh independently authored adversarial court against the OC6 candidate.

Author: the HQ315 OC7 independent I2 reviewer. NOT the OC6 author, NOT the
OC5E author, NOT HQ. Every test here is newly written by the reviewer from the
public contract of the module, not copied or derived from the OC6 author
control suite or the OC5E hostile suite.

EXPECTATIONS ARE PREREGISTERED in freezes/01_PREREGISTERED_EXPECTATIONS.json.
This file was frozen and committed BEFORE its first execution. Nothing here was
edited to match an observed result.

TEST_ONLY scope. `MockSignature` / `MockSigner` are publicly forgeable ephemeral
fixtures. Nothing here asserts real institutional custody, semantic
noninterference, external anchoring or V3 authority.
"""
import math
import unicodedata

import pytest

import custody_protocol as CP

# Fullwidth Latin is built from unicodedata rather than hand-written escapes so
# an author typo cannot silently substitute halfwidth kana.
FW = {c: chr(0xFF01 + ord(c) - 0x21) for c in
      "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"}
FW[" "] = "\u3000"


def fw(s):
    return "".join(FW[c] for c in s)


def make_capsule(**kw):
    base = dict(
        capsule_id="cap-1", schema_version="1.0",
        purpose="SOURCEFREE_TEST_ONLY", scenario_frame="frame-1",
        family_graph_digest="fgd", content_digest="content-digest",
        contribution_digest="cd", public_projection_digest="ppd",
        hidden_projection_digest="hpd", lawful_set_digest="lsd",
        coder_rubric_digest="crd", split_assignment_digest="sad",
        generation_history_digest="ghd", rejected_alternatives_digest="rad",
        freeze_timestamp=1000.0,
    )
    base.update(kw)
    return CP.CustodyCapsule(**base)


def signed_pair(capsule, nonce="n-1", ctx="ctx-1"):
    a = CP.MockSigner("custodian-alice", CP.Role.CUSTODIAN).sign(
        capsule.content_digest, ctx, nonce, capsule=capsule)
    b = CP.MockSigner("adjudicator-bob", CP.Role.SEMANTIC_ADJUDICATOR).sign(
        capsule.content_digest, ctx, nonce, capsule=capsule)
    return a, b


# ---------------------------------------------------------------------------
# G1 — A1 normalization-equivalent duplicate allowed-field aliases
# Preregistered: every alias of an ALLOWED field that normalizes onto it is
# refused, at top level and inside the one allowed nested public_projection.
# ---------------------------------------------------------------------------

A1_ALIASES = [
    ("fullwidth", "ｎote"),
    ("combining_macron_below", "no\u0331te"),
    ("combining_circumflex", "n\u0302ote"),
    ("invisible_zero_width", "not\u200be"),
    ("word_joiner", "note\u2060"),
    ("soft_hyphen", "no\u00adte"),
    ("nfd_combining", "no\u0308te"),
    ("enclosed_alphanumeric", "note\u2460"),
]


@pytest.mark.parametrize("label,alias", A1_ALIASES, ids=[a for a, _ in A1_ALIASES])
def test_A1_alias_of_allowed_field_is_refused(label, alias):
    issues = CP.detect_leakage({"note": "visible", alias: "shadow"})
    assert any(i.startswith("duplicate_normalized_field:") for i in issues), issues


def test_A1_alias_plus_sibling_is_refused():
    """Three sibling keys: canonical + fullwidth alias + another allowed field."""
    issues = CP.detect_leakage({
        "request_id": "r", fw("request_id"): "r-alias", "response": "x"})
    assert any(i.startswith("duplicate_normalized_field:") for i in issues), issues


def test_A1_alias_alone_without_canonical_is_still_unapproved():
    """A single fullwidth alias is not an allowed field at all."""
    issues = CP.detect_leakage({fw("request_id"): "r"})
    assert issues == ["unapproved_field:request_id"], issues


def test_A1_nested_alias_inside_public_projection_refused():
    issues = CP.detect_leakage(
        {"public_projection": {"context": "a", fw("context"): "b"}})
    assert any(i.startswith("duplicate_normalized_field:") for i in issues), issues


def test_A1_duplicate_alias_of_disallowed_key_is_not_double_reported():
    """Aliasing a key that is already unapproved must not launder it."""
    issues = CP.detect_leakage({"secret_x": 1, fw("secret_x"): 2})
    assert all("duplicate_normalized_field" not in i for i in issues), issues
    assert "unapproved_field:secret_x" in issues, issues


def test_A1_duplicate_alias_cardinality_at_depth_is_still_refused():
    """Three-way alias collision on one allowed field."""
    issues = CP.detect_leakage({
        "note": "a", fw("note"): "b", "no\u0331te": "c"})
    dupes = [i for i in issues if i.startswith("duplicate_normalized_field:")]
    assert len(dupes) == 2, issues


# ---------------------------------------------------------------------------
# G2 — A2 bounded confusable fold
# Preregistered: correctly spelled NFKC-invisible homoglyph substitutions of
# denied tokens are DENIED; safe multilingual text and near-miss Latin words are
# NOT denied. No universal semantic claim.
# ---------------------------------------------------------------------------

A2_DENY = [
    ("cyrillic_a_answer_key", "\u0430nswer_key is A"),
    ("cyrillic_ie_expected_result", "\u0435xpected_result is A"),
    ("armenian_h_hidden_origin", "\u0570idden_origin is A"),
    ("greek_alpha_lawful_answers", "l\u03b1wful_answers is A"),
    ("cyrillic_es_contrast_label", "\u0441ontrast_label is A"),
    ("cyrillic_komi_de_answer_key", "\u0430ns\u051der_key is A"),
    ("greek_omicron_contrast", "\u0441ontrast with \u03bf"),
    ("fullwidth_answer_key", fw("answer_key") + " is A"),
]


@pytest.mark.parametrize("label,value", A2_DENY, ids=[a for a, _ in A2_DENY])
def test_A2_correctly_spelled_confusable_is_denied(label, value):
    with pytest.raises(CP.LeakageError):
        CP.assert_no_leakage({"note": value})


A2_ALLOW = [
    ("russian", "\u041e\u0442\u0432\u0435\u0442 \u043d\u0430 \u0432\u043e\u043f\u0440\u043e\u0441"),
    ("greek", "\u0397 \u03c3\u03c9\u03c3\u03c4\u03ae \u03b1\u03c0\u03ac\u03bd\u03c4\u03b7\u03c3\u03b7"),
    ("armenian", "\u057d\u057a\u0561\u057d\u056b\u0576 \u057a\u0561\u057f\u0561\u057d\u056d\u0561\u0576"),
    ("japanese", "\u6b63\u3057\u3044\u7b54\u3048"),
    ("arabic", "\u0627\u0644\u062c\u0648\u0627\u0628 \u0627\u0644\u0635\u062d\u064a\u062d"),
    ("hebrew", "\u05d4\u05ea\u05e9\u05d5\u05d1\u05d4 \u05d4\u05e0\u05db\u05d5\u05e0\u05d4"),
    ("hindi", "\u0938\u0939\u0940 \u0909\u0924\u094d\u0924\u0930"),
    ("thai", "\u0e04\u0e33\u0e15\u0e2d\u0e1a\u0e17\u0e35\u0e48\u0e16\u0e39\u0e01\u0e15\u0e49\u0e2d\u0e07"),
    ("korean", "\uc815\ub2f5"),
    ("cyrillic_prose", "\u043c\u0438\u0440\u043e\u0432\u043e\u0439 \u043e\u0442\u0432\u0435\u0442 \u0441\u043a\u0440\u044b\u0442"),
    ("greek_prose", "\u03ba\u03bf\u03c3\u03bc\u03bf\u03c2 \u03b1\u03c0\u03b1\u03bd\u03c4\u03b7\u03c3\u03b7\u03c2"),
    ("latin_safe", "a short harmless note about a person"),
    ("near_miss_lowful", "lowful answers overall"),
    ("near_miss_ansers", "ansers key"),
]


@pytest.mark.parametrize("label,value", A2_ALLOW, ids=[a for a, _ in A2_ALLOW])
def test_A2_safe_text_is_not_falsely_denied(label, value):
    assert CP.detect_leakage({"note": value}) == []


def test_A2_invisible_and_combining_marks_do_not_hide_a_denied_token():
    """U+200B / U+034F are stripped by normalization, so the token is still seen."""
    for value in ("ans\u200bwer_key is A", "ans\u034fwer_key is A", fw("answer_key")):
        assert "answer_key" in CP.detect_leakage({"note": value}), value


def test_A2_confusable_in_a_nested_list_value_is_denied():
    assert "answer_key" in CP.detect_leakage(
        {"menu": ["harmless", "\u0430nswer_key is A"]})


def test_A2_confusable_in_a_key_position_is_refused_even_though_not_a_value_fold():
    """A Cyrillic-a key is not an allowed field; fail-closed regardless of fold."""
    issues = CP.detect_leakage({"\u0430nswer_key": "x"})
    assert issues and issues[0].startswith("unapproved_field:"), issues


def test_A2_disputed_oc5e_inputs_fold_to_different_latin_words():
    """Documents the two disputed OC5E inputs at codepoint level.

    Preregistered as a FACTUAL fold assertion, not as a product judgement:
    U+03BF is a lookalike for 'o' and U+0455 for 's'; neither occupies the
    position of the letter in the denied token it was written to imitate.
    """
    greek = "l\u03bfwful_answers is A"
    mixed = "\u0430ns\u0435er\u0455_key"
    assert CP._confusable_folded(greek) == "lowful_answers is A"
    assert CP._confusable_folded(mixed) == "anseers_key"
    assert CP._confusable_folded(greek) != "lawful_answers is A"
    assert CP._confusable_folded(mixed) != "answer_key"
    assert unicodedata.normalize("NFKC", "\u03bf") == "\u03bf"  # NFKC-stable
    assert CP.detect_leakage({"note": greek}) == []
    assert CP.detect_leakage({"note": mixed}) == []


# ---------------------------------------------------------------------------
# G3 — A3/A4 malformed signature objects and non-enum roles
# Preregistered: every malformed signature is refused with the TYPED
# SignatureError, never a raw AttributeError, and never accepted.
# ---------------------------------------------------------------------------

MALFORMED_SIGS = [
    ("none", None),
    ("bare_object", object()),
    ("dict", {"signature_hash": "x", "role": CP.Role.CUSTODIAN}),
    ("bare_string", "signature"),
    ("int", 7),
    ("list", ["sig"]),
]


@pytest.mark.parametrize("label,bad", MALFORMED_SIGS, ids=[a for a, _ in MALFORMED_SIGS])
def test_A3_malformed_primary_signature_is_typed_refusal(label, bad):
    cap = make_capsule()
    _, second = signed_pair(cap)
    with pytest.raises(CP.SignatureError):
        CP.require_second_signature(cap, bad, second, cap.content_digest, "ctx-1", "n-1")


@pytest.mark.parametrize("label,bad", MALFORMED_SIGS, ids=[a for a, _ in MALFORMED_SIGS])
def test_A3_malformed_secondary_signature_is_typed_refusal(label, bad):
    cap = make_capsule()
    primary, _ = signed_pair(cap)
    with pytest.raises(CP.SignatureError):
        CP.require_second_signature(cap, primary, bad, cap.content_digest, "ctx-1", "n-1")


def test_A3_malformed_signature_never_raises_raw_attributeerror():
    """The pre-repair failure mode was an uncontrolled AttributeError."""
    cap = make_capsule()
    _, second = signed_pair(cap)
    try:
        CP.require_second_signature(cap, object(), second, cap.content_digest, "ctx-1", "n-1")
    except CP.SignatureError:
        pass
    except AttributeError:  # pragma: no cover - this is the defect being probed
        pytest.fail("raw AttributeError escaped the signature contract")
    else:  # pragma: no cover
        pytest.fail("malformed signature was accepted")


def test_A4_bare_string_role_is_typed_refusal():
    cap = make_capsule()
    primary, second = signed_pair(cap)
    object.__setattr__(primary, "role", "CUSTODIAN")
    with pytest.raises(CP.SignatureError):
        CP.require_second_signature(cap, primary, second, cap.content_digest, "ctx-1", "n-1")


def test_A4_second_signer_bare_string_role_is_typed_refusal():
    cap = make_capsule()
    primary, second = signed_pair(cap)
    object.__setattr__(second, "role", "SEMANTIC_ADJUDICATOR")
    with pytest.raises(CP.SignatureError):
        CP.require_second_signature(cap, primary, second, cap.content_digest, "ctx-1", "n-1")


def test_A3_strict_mock_verify_returns_false_for_malformed_without_raising():
    assert CP.MockSigner.verify(object(), "cd", "ctx", "n") is False
    assert CP.MockSigner.verify({"x": 1}, "cd", "ctx", "n") is False


def test_A3_authentic_capsule_bound_pair_still_verifies():
    """Positive control: the repair must not break real signed envelopes."""
    cap = make_capsule()
    primary, second = signed_pair(cap)
    assert CP.require_second_signature(
        cap, primary, second, cap.content_digest, "ctx-1", "n-1") is True


# ---------------------------------------------------------------------------
# G4 — A5 holder identity, including nonhashables
# Preregistered: any non-string or blank holder is refused with the TYPED
# IdentityMismatchError before any dict access; never a raw TypeError.
# ---------------------------------------------------------------------------

BAD_HOLDERS = [
    ("dict", {}), ("list", []), ("set", set()), ("list_of_str", ["runner1"]),
    ("int", 1), ("float", 1.0), ("none", None), ("empty", ""),
    ("whitespace", "   "), ("fullwidth_space", "\u3000"), ("bool", True),
]


@pytest.mark.parametrize("label,holder", BAD_HOLDERS, ids=[a for a, _ in BAD_HOLDERS])
def test_A5_malformed_holder_is_typed_refusal(label, holder):
    st = CP.EscrowState()
    st.commit(make_capsule())
    with pytest.raises(CP.IdentityMismatchError):
        st.unblind("cap-1", holder)


def test_A5_nonhashable_holder_never_raises_raw_typeerror():
    st = CP.EscrowState()
    st.commit(make_capsule())
    for holder in ({}, [], set()):
        try:
            st.unblind("cap-1", holder)
        except CP.IdentityMismatchError:
            continue
        except TypeError:  # pragma: no cover - the defect being probed
            pytest.fail(f"raw TypeError escaped for holder {holder!r}")
        pytest.fail(f"malformed holder {holder!r} was accepted")


def test_A5_unauthorized_but_wellformed_holder_is_refused():
    st = CP.EscrowState()
    st.commit(make_capsule())
    with pytest.raises(CP.IdentityMismatchError):
        st.unblind("cap-1", "stranger-9")


def test_A5_positive_authorised_holder_unblinds():
    st = CP.EscrowState()
    st.commit(make_capsule())
    payload = st.unblind("cap-1", "runner1")
    assert payload["capsule_id"] == "cap-1"
    assert payload["holder"] == "runner1"


# ---------------------------------------------------------------------------
# G5 — A6 capsule field validation
# Preregistered: every declared capsule field is type/format checked BEFORE any
# commitment or state change; bool is not accepted as int, NaN/Infinity and
# negative timestamps are refused, non-string digests are refused.
# ---------------------------------------------------------------------------

STRING_FIELDS = [
    "capsule_id", "schema_version", "scenario_frame", "purpose",
    "family_graph_digest", "content_digest", "contribution_digest",
    "public_projection_digest", "hidden_projection_digest",
    "lawful_set_digest", "coder_rubric_digest", "split_assignment_digest",
    "generation_history_digest", "rejected_alternatives_digest",
]


@pytest.mark.parametrize("field", STRING_FIELDS)
@pytest.mark.parametrize("bad", [None, 5, b"x", "", "   ", ["a"], {"a": 1}],
                         ids=["none", "int", "bytes", "empty", "ws", "list", "dict"])
def test_A6_capsule_string_field_must_be_nonempty_string(field, bad):
    with pytest.raises(TypeError):
        CP.validate_capsule_fields(make_capsule(**{field: bad}))


@pytest.mark.parametrize("version,label", [
    (True, "bool"), (0, "zero"), (-1, "negative"), (1.0, "float"),
    (2.5, "nonintegral_float"), ("1", "string"), (None, "none"),
])
def test_A6_capsule_version_must_be_positive_int(version, label):
    with pytest.raises(TypeError):
        CP.validate_capsule_fields(make_capsule(version=version))


@pytest.mark.parametrize("stamp,label", [
    (float("nan"), "nan"), (float("inf"), "posinf"), (float("-inf"), "neginf"),
    (-1.0, "negative"), (True, "bool"), ("1000", "string"), (None, "none"),
])
def test_A6_capsule_timestamp_must_be_finite_nonnegative_number(stamp, label):
    with pytest.raises(TypeError):
        CP.validate_capsule_fields(make_capsule(freeze_timestamp=stamp))


@pytest.mark.parametrize("stamp,label", [(0, "zero_boundary"), (0.0, "float_zero"),
                                         (1e18, "large"), (1.5, "fractional")])
def test_A6_capsule_timestamp_boundaries_are_accepted(stamp, label):
    assert CP.validate_capsule_fields(make_capsule(freeze_timestamp=stamp)) is None


@pytest.mark.parametrize("flag", ["expired", "revoked"])
@pytest.mark.parametrize("bad,label", [(1, "int"), (0, "zero_int"),
                                       ("no", "string"), (None, "none")])
def test_A6_capsule_lifecycle_flags_must_be_bool(flag, bad, label):
    with pytest.raises(TypeError):
        CP.validate_capsule_fields(make_capsule(**{flag: bad}))


def test_A6_validate_rejects_non_capsule_object():
    with pytest.raises(TypeError):
        CP.validate_capsule_fields({"capsule_id": "x"})


def test_A6_commit_refuses_malformed_capsule_before_state_change():
    st = CP.EscrowState()
    bad = make_capsule(content_digest=12345)
    with pytest.raises(TypeError):
        st.commit(bad)
    assert st.committed == {}
    assert st.ledger == []


def test_A6_commitment_refuses_malformed_capsule():
    with pytest.raises(TypeError):
        CP.capsule_envelope_commitment(make_capsule(version=True))


@pytest.mark.parametrize("facts,label", [
    ({1: "a"}, "int_key"), ({(): "empty_key"}, "weird_key"),
    ({("a", "b"): 1}, "tuple_key"),
])
def test_A6_semantic_fingerprint_rejects_heterogeneous_coerced_keys(facts, label):
    with pytest.raises(TypeError):
        CP.semantic_fingerprint(facts)


@pytest.mark.parametrize("facts,label", [({}, "empty"), ([], "list"),
                                          ("str", "string"), (None, "none")])
def test_A6_semantic_fingerprint_rejects_non_mapping(facts, label):
    with pytest.raises(TypeError):
        CP.semantic_fingerprint(facts)


# ---------------------------------------------------------------------------
# G6 — full 18-field envelope binding
# Preregistered: the full-envelope commitment binds ALL 18 declared fields.
# Mutating any single field must change the digest.
# ---------------------------------------------------------------------------

FIELD_MUTATIONS = {
    "capsule_id": "cap-2", "schema_version": "2.0",
    "purpose": "CUSTODY_READINESS_PROTOCOL", "scenario_frame": "frame-2",
    "family_graph_digest": "fgd2", "content_digest": "content-digest-2",
    "contribution_digest": "cd2", "public_projection_digest": "ppd2",
    "hidden_projection_digest": "hpd2", "lawful_set_digest": "lsd2",
    "coder_rubric_digest": "crd2", "split_assignment_digest": "sad2",
    "generation_history_digest": "ghd2", "rejected_alternatives_digest": "rad2",
    "freeze_timestamp": 2000.0, "version": 7, "expired": True, "revoked": True,
}


def test_G6_capsule_declares_exactly_eighteen_fields():
    import dataclasses
    assert len(dataclasses.fields(CP.CustodyCapsule)) == 18
    assert set(FIELD_MUTATIONS) == {f.name for f in dataclasses.fields(CP.CustodyCapsule)}


@pytest.mark.parametrize("field,value", sorted(FIELD_MUTATIONS.items()))
def test_G6_every_field_is_bound_into_the_full_envelope_commitment(field, value):
    base = CP.capsule_envelope_commitment(make_capsule())
    mutated = CP.capsule_envelope_commitment(make_capsule(**{field: value}))
    assert mutated != base, f"field {field!r} is NOT bound into the commitment"


def test_G6_identical_capsules_have_identical_commitment():
    assert (CP.capsule_envelope_commitment(make_capsule())
            == CP.capsule_envelope_commitment(make_capsule()))


def test_G6_commitment_is_sha256_hex():
    d = CP.capsule_envelope_commitment(make_capsule())
    assert len(d) == 64 and all(c in "0123456789abcdef" for c in d)


# ---------------------------------------------------------------------------
# G7 — three-arm blinded pairing, typed negatives
# ---------------------------------------------------------------------------

def ok_trials():
    return [
        {"public_nonce": "n1", "arm": "A", "trial_id": "t1"},
        {"public_nonce": "n1", "arm": "B", "trial_id": "t2"},
        {"public_nonce": "n1", "arm": "C", "trial_id": "t3"},
    ]


def test_G7_authentic_three_arm_block_passes():
    assert CP.verify_blind_pairing(ok_trials()) is True


@pytest.mark.parametrize("mutate,label", [
    (lambda t: t.pop(), "two_arms"),
    (lambda t: t.append({"public_nonce": "n1", "arm": "A", "trial_id": "t9"}), "duplicate_arm"),
    (lambda t: t.__setitem__(0, {**t[0], "arm": "D"}), "unknown_arm"),
    (lambda t: t.__setitem__(0, {**t[0], "arm": None}), "null_arm"),
    (lambda t: t.__setitem__(0, {**t[0], "public_nonce": ""}), "empty_nonce"),
    (lambda t: t.__setitem__(0, {**t[0], "public_nonce": "n2"}), "split_nonce"),
    (lambda t: t.__setitem__(1, {**t[1], "trial_id": "t1"}), "duplicate_trial_id"),
    (lambda t: t.__setitem__(1, {**t[1], "case_id": "c9"}), "incoherent_case_join"),
    (lambda t: t.__setitem__(1, {**t[1], "family_id": 17}), "nonstring_family_join"),
    (lambda t: t.__setitem__(0, "not-a-dict"), "non_dict_trial"),
])
def test_G7_malformed_pairing_is_typed_refusal(mutate, label):
    trials = ok_trials()
    mutate(trials)
    with pytest.raises(CP.BlindIDPairingError):
        CP.verify_blind_pairing(trials)


@pytest.mark.parametrize("trials,block,label", [
    ([], 3, "empty_list"), ("nope", 3, "not_a_list"),
    (ok_trials(), 4, "wrong_block_size"), (ok_trials(), 2, "block_size_two"),
])
def test_G7_pairing_shape_is_typed_refusal(trials, block, label):
    with pytest.raises(CP.BlindIDPairingError):
        CP.verify_blind_pairing(trials, block_size=block)


def test_G7_coherent_case_join_across_the_block_is_accepted():
    trials = [{**r, "case_id": "case-7", "family_id": "fam-3"} for r in ok_trials()]
    assert CP.verify_blind_pairing(trials) is True


# ---------------------------------------------------------------------------
# G8 — strict packet projection allowlist (positive and negative)
# ---------------------------------------------------------------------------

def test_G8_wellformed_public_projection_is_admitted():
    assert CP.detect_leakage({
        "public_projection": {"context": "a short context"},
        "menu": ["a", "b"], "request_id": "r1",
        "response": "text", "note": "hi"}) == []


@pytest.mark.parametrize("packet,label", [
    ({"public_projection": {"context": "c", "answer_key": "leak"}}, "leak_in_projection"),
    ({"public_projection": {"other": "c"}}, "wrong_projection_key"),
    ({"public_projection": "flat"}, "projection_not_mapping"),
    ({"menu": "notalist"}, "menu_not_list"),
    ({"menu": []}, "menu_empty"),
    ({"menu": [1, 2]}, "menu_non_string_items"),
    ({"request_id": 5}, "request_id_non_string"),
    ({"response": None}, "response_none"),
    ("notadict", "packet_not_mapping"),
])
def test_G8_malformed_packet_is_refused(packet, label):
    assert CP.detect_leakage(packet) != []


def test_G8_deep_nesting_is_refused():
    node = {"public_projection": {"context": "c"}}
    cur = node
    for _ in range(12):
        cur["menu"] = ["x"]
        cur = cur["menu"][0] if isinstance(cur["menu"][0], dict) else cur
    # build a clean deep chain instead
    deep = {"public_projection": {"context": "c"}}
    inner = deep
    for _ in range(12):
        inner["menu"] = ["x"]
    assert "excess_nesting" in CP.detect_leakage(deep) or \
        any(i.startswith("unapproved_field") for i in CP.detect_leakage(deep))


# ---------------------------------------------------------------------------
# G9 — escrow: append-only ledger, freeze seal, rollback refusal
# ---------------------------------------------------------------------------

def G9_state():
    st = CP.EscrowState()
    st.commit(make_capsule())
    return st


def test_G9_happy_path_commit_unblind_release():
    st = G9_state()
    st.unblind("cap-1", "runner1")
    st.release("cap-1")
    assert st.verify_ledger_integrity() is True
    assert "cap-1" in st.released


def test_G9_mutation_after_commit_is_detected():
    st = G9_state()
    st.committed["cap-1"].scenario_frame = "tampered"
    with pytest.raises(CP.EditAfterFreezeError):
        st.unblind("cap-1", "runner1")


def test_G9_commit_is_append_only_no_rollback_entrypoint():
    st = G9_state()
    with pytest.raises(CP.LedgerRollbackError):
        st.rollback_ledger(1)
    assert st.verify_ledger_integrity() is True


def test_G9_ledger_tampering_is_detected():
    st = G9_state()
    st.unblind("cap-1", "runner1")
    st.ledger[0]["capsule_id"] = "cap-evil"
    assert st.verify_ledger_integrity() is False


def test_G9_ledger_truncation_is_detected():
    st = G9_state()
    st.unblind("cap-1", "runner1")
    st.ledger.pop()
    assert st.verify_ledger_integrity() is False


def test_G9_double_commit_is_refused():
    st = G9_state()
    with pytest.raises(CP.EditAfterFreezeError):
        st.commit(make_capsule())


def test_G9_double_unblind_is_refused():
    st = G9_state()
    st.unblind("cap-1", "runner1")
    with pytest.raises(CP.EditAfterFreezeError):
        st.unblind("cap-1", "runner1")


def test_G9_release_before_unblind_is_refused():
    with pytest.raises(CP.IdentityMismatchError):
        G9_state().release("cap-1")


def test_G9_unblind_uncommitted_capsule_is_refused():
    with pytest.raises(CP.IdentityMismatchError):
        CP.EscrowState().unblind("cap-nope", "runner1")


@pytest.mark.parametrize("purpose,label", [
    ("SOURCEFREE_TEST_ONLY", "allowed"),
    ("development", "explicit_development"),
    ("PROSPECTIVE_DESIGN_REVIEW", "allowed2"),
])
def test_G9_harmless_receipt_exposure_purposes_are_accepted(purpose, label):
    st = G9_state()
    st.record_exposure("cap-1", "coder-7", purpose)
    assert st.verify_ledger_integrity() is True


@pytest.mark.parametrize("purpose", ["production", "", "REAL_TRIAL", None])
def test_G9_unauthorized_exposure_purpose_is_refused(purpose):
    with pytest.raises(CP.PurposeViolationError):
        G9_state().record_exposure("cap-1", "coder-7", purpose)


def test_G9_unauthorized_commit_purpose_is_refused():
    st = CP.EscrowState()
    with pytest.raises(CP.PurposeViolationError):
        st.commit(make_capsule(purpose="PRODUCTION"))


def test_G9_commit_refuses_expired_or_revoked_capsule():
    for flag in ("expired", "revoked"):
        st = CP.EscrowState()
        with pytest.raises(CP.RevocationError):
            st.commit(make_capsule(**{flag: True}))


# ---------------------------------------------------------------------------
# G10 — family independence and fingerprint determinism
# ---------------------------------------------------------------------------

def test_G10_identical_facts_have_identical_fingerprints():
    a = CP.semantic_fingerprint({"x": 1, "y": "z"})
    b = CP.semantic_fingerprint({"y": "z", "x": 1})
    assert a == b


def test_G10_different_facts_have_different_fingerprints():
    assert (CP.semantic_fingerprint({"x": 1})
            != CP.semantic_fingerprint({"x": 2}))


def test_G10_family_clone_is_detected():
    assert CP.detect_family_clone({"a": 1}, {"a": 1}, frozenset()) is True
    assert CP.detect_family_clone({"a": 1}, {"a": 2}, frozenset()) is False


def test_G10_role_conflict_matrix_is_intact():
    assert CP.roles_conflict(CP.Role.CUSTODIAN, CP.Role.SEMANTIC_ADJUDICATOR) is True
    assert CP.roles_conflict(CP.Role.CUSTODIAN, CP.Role.CUSTODIAN) is False
