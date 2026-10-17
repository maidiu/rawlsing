from dataclasses import replace

from rawlsing_next.pre553_empirical_objects import ExactRef
import rawlsing_next.gt34_obl031_q69b_comparator_resolver_r4 as target

ACTOR = "urn:r4:test:actor"


def h(ch):
    return ch * 64


def window(currentness=target.NONCURRENT_SYNTHETIC_TEST_ONLY):
    return target.RespondentDateIntrWindow(
        respondent_ref=ExactRef("RESPONDENT", "urn:r4:r1", h("a")),
        dateintr_ref=ExactRef("DATEINTR", "urn:r4:r1:date", h("b")),
        window_start="2024-01-01T00:00:00Z",
        window_end="2024-12-31T23:59:59Z",
        lower_edge_inclusive=True,
        currentness=currentness,
    )


def fixture():
    return target.SyntheticEncounterFixture.build(ACTOR, "2024-06-15T12:00:00Z")


def fake_actor():
    class Record:
        pass
    return Record()


def current_call(grammar):
    return target.resolve_current(
        actor_record=fake_actor(),
        expected_actor_id=ACTOR,
        classification_proof=target.current_obl048_proof(),
        q69b_binding=target.Q69BSourceBinding(),
        grammar_binding=grammar,
        respondent_windows=(window(target.CURRENT_ACCEPTED),),
    )


class EqualitySpoof:
    def __eq__(self, other):
        return True

    def __ne__(self, other):
        return False

    authority_id = target.D08_AUTHORITY_ID
    authority_version = target.D08_AUTHORITY_VERSION
    authority_hash = target.D08_AUTHORITY_CONTENT_HASH
    authority_kind = target.D08_AUTHORITY_KIND
    governed_operation = target.D08_GOVERNED_OPERATION
    governed_object_family = target.D08_GOVERNED_OBJECT_FAMILY
    predicate_leaf_type = target.D08_PREDICATE_LEAF_TYPE
    comparison_operator = target.D08_COMPARISON_OPERATOR
    operator_semantics_refs = target.D08_OPERATOR_SEMANTICS_REFS


def test_equality_spoof_is_rejected_before_r3_or_r2():
    result = current_call(EqualitySpoof())
    assert result.outcome == target.D08_GRAMMAR_UNRESOLVED
    assert result.predicate is None and result.receipt is None


def test_plain_structural_dict_is_rejected_even_with_exact_values():
    g = target.current_d08_grammar_binding()
    result = current_call({"authority_id": g.authority_id, "authority_version": g.authority_version})
    assert result.outcome == target.D08_GRAMMAR_UNRESOLVED


def test_subclass_cannot_substitute_for_exact_frozen_binding_type():
    class Subclass(target.D08GrammarBinding):
        pass
    g = target.current_d08_grammar_binding()
    sub = Subclass(**{name: getattr(g, name) for name in g.__dataclass_fields__})
    result = current_call(sub)
    assert result.outcome == target.D08_GRAMMAR_UNRESOLVED


def test_exact_current_binding_remains_accepted_into_synthetic_mechanics():
    result = target.prove_noncurrent_synthetic(
        fixture=fixture(),
        classification_proof=target.current_obl048_proof(),
        q69b_binding=target.Q69BSourceBinding(),
        grammar_binding=target.current_d08_grammar_binding(),
        respondent_windows=(window(),),
    )
    assert result.outcome == target.NONCURRENT_SYNTHETIC_PROOF
    assert result.predicate is None
    assert result.receipt.currentness == target.NONCURRENT_SYNTHETIC_TEST_ONLY
    assert result.receipt.comparator_rule_identity == target.authority_identity()


def test_r4_receipt_preserves_exact_hq_d08_selection_closure():
    result = target.prove_noncurrent_synthetic(
        fixture=fixture(),
        classification_proof=target.current_obl048_proof(),
        q69b_binding=target.Q69BSourceBinding(),
        grammar_binding=target.current_d08_grammar_binding(),
        respondent_windows=(window(),),
    )
    closure = result.receipt.d08_hq_selection_closure
    for exact in (
        target.D08_AUTHORITY_ID,
        target.D08_AUTHORITY_VERSION,
        target.D08_AUTHORITY_CONTENT_HASH,
        target.D08_HQ_ADOPTION_COMMIT,
        target.D08_HQ_ADOPTION_ARTIFACT_BLOB,
        target.D08_HQ_ADOPTION_JSON_BLOB,
        target.D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB,
        target.D08_RESOLUTION_CONTRACT,
    ):
        assert exact in closure


def test_mutated_exact_type_value_still_rejected():
    bad = replace(target.current_d08_grammar_binding(), authority_hash=h("9"))
    assert current_call(bad).outcome == target.D08_GRAMMAR_UNRESOLVED


def test_real_missing_actor_encounter_remains_controlling_negative():
    result = target.resolve_current(
        actor_record=None,
        expected_actor_id=ACTOR,
        classification_proof=target.current_obl048_proof(),
        q69b_binding=target.Q69BSourceBinding(),
        grammar_binding=target.current_d08_grammar_binding(),
        respondent_windows=(),
    )
    assert result.outcome == target.ACTOR_FACT_MISSING_OR_UNAUTHORIZED
    assert result.predicate is None and result.receipt is None


def test_authority_identity_changes_for_strict_type_closure_successor():
    assert target.authority_identity()[1] == "1.1.3"
    assert len(target.authority_identity()[2]) == 64
