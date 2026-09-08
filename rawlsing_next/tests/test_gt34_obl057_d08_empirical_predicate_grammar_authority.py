from dataclasses import replace

import pytest

from rawlsing_next import gt34_d08_empirical_predicate_grammar_authority as m
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash


def _evidence(label: str) -> ExactRef:
    return ExactRef(
        "NONCURRENT_SYNTHETIC_TEST_ONLY_HQ_ADOPTION_EVIDENCE",
        label,
        semantic_hash({"synthetic_test_only": label}),
    )


def _valid_binding():
    adoption = (_evidence("adoption"), _evidence("current-selection"))
    binding = m.exact_runtime_binding(
        adoption_current_selection_evidence_refs=adoption,
        immutable_provenance_refs=m.IMMUTABLE_PROVENANCE_REFS + adoption,
    )
    return binding, adoption


def test_exact_candidate_content_hash_is_frozen():
    assert m.AUTHORITY_CONTENT_HASH == "acec40d03b5602aaa553f1f63cf2506bffe0491c008678ff973e39c3f7dcedd4"
    assert semantic_hash(m.AUTHORITY_MATERIAL) == m.AUTHORITY_CONTENT_HASH


def test_exact_pre553_authority_tuple_is_frozen():
    assert m.AUTHORITY_REF == AuthorityRef(
        "GT34_D08_EMPIRICAL_PREDICATE_GRAMMAR_AUTHORITY",
        "1.0.0",
        "acec40d03b5602aaa553f1f63cf2506bffe0491c008678ff973e39c3f7dcedd4",
    )


def test_exact_owned_grain_only():
    assert m.AUTHORITY_KIND == "PREDICATE_GRAMMAR"
    assert m.GOVERNED_OBJECT_FAMILY == "EmpiricalPredicate@1.0.0"
    assert m.GOVERNED_OPERATION == "RESOLVE_EXACT_EMPIRICAL_POSITION_COORDINATE_EQ_PREDICATE"
    assert m.PREDICATE_LEAF_TYPE == "EMPIRICAL_POSITION_COORDINATE"
    assert m.COMPARISON_OPERATOR == "EQ"


def test_operator_semantics_refs_are_content_addressed_and_frozen():
    assert m.COORDINATE_SEMANTICS_REF.content_hash == "53e3593784cebdd50f68f8d993786b7643ff64280b8b63efbd09bd6d6a6ae8cf"
    assert m.EQ_SEMANTICS_REF.content_hash == "4d1dd3a2514b86b5c1d633527bfa6d7ba2b0188b754d4f12c2edc89c4343dd69"


def test_owner_jurisdiction_is_frozen():
    assert m.OWNER_JURISDICTION_REF.content_hash == "900d13df2f3c8167be47be574549b8b98a1d87dc02d0f273104dbc353aa783bb"
    assert "VOZHD_HQ_PRE_MAIN" in m.OWNER_JURISDICTION_REF.object_id


def test_historical_d08_is_provenance_not_runtime_authority():
    assert "db03fcbcb5e34c28b486070628377ead0408e13a" in m.HISTORICAL_D08_REF.object_id
    assert m.HISTORICAL_D08_REF not in m.OPERATOR_SEMANTICS_REFS
    assert m.AUTHORITY_REF.authority_id != m.HISTORICAL_D08_REF.object_id


def test_current_q69b_coordinate_authority_is_not_owned_here():
    joined = "|".join(m.AUTHORITY_CEILING)
    assert "NO_Q69B_COORDINATE_SEMANTICS" in joined
    assert "NO_COMPARATOR_MAPPING_SEMANTICS" in joined


def test_candidate_definition_is_explicitly_not_adopted():
    candidate = m.candidate_definition()
    assert candidate["status"] == m.CANDIDATE_NOT_ADOPTED
    assert candidate["adoption_contract"].startswith("NO_RUNTIME_CURRENTNESS_UNTIL_EXPLICIT_VOZHD_HQ_ADOPTION")


def test_valid_d08_eq_leaf_shape_is_accepted_without_claiming_coordinate_truth():
    m.validate_predicate_ast_shape({
        "op": "LEAF",
        "leaf_type": "EMPIRICAL_POSITION_COORDINATE",
        "coordinate_ref": "EXTERNAL_EXACT_COORDINATE",
        "comparison_operator": "EQ",
        "canonical_value": "EXTERNAL_GOVERNED_VALUE",
    })


@pytest.mark.parametrize("field,value", [
    ("op", "AND"),
    ("leaf_type", "ACTOR_POSITION"),
    ("comparison_operator", "NEAREST"),
])
def test_predicate_grammar_mutations_fail(field, value):
    ast = {
        "op": "LEAF",
        "leaf_type": "EMPIRICAL_POSITION_COORDINATE",
        "coordinate_ref": "EXTERNAL_EXACT_COORDINATE",
        "comparison_operator": "EQ",
        "canonical_value": "EXTERNAL_GOVERNED_VALUE",
    }
    ast[field] = value
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_predicate_ast_shape(ast)


def test_empty_coordinate_ref_fails():
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_predicate_ast_shape({
            "op": "LEAF",
            "leaf_type": "EMPIRICAL_POSITION_COORDINATE",
            "coordinate_ref": "",
            "comparison_operator": "EQ",
            "canonical_value": "X",
        })


def test_missing_value_fails():
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_predicate_ast_shape({
            "op": "LEAF",
            "leaf_type": "EMPIRICAL_POSITION_COORDINATE",
            "coordinate_ref": "C",
            "comparison_operator": "EQ",
        })


def test_out_of_jurisdiction_actor_semantics_fail():
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_predicate_ast_shape({
            "op": "LEAF",
            "leaf_type": "EMPIRICAL_POSITION_COORDINATE",
            "coordinate_ref": "C",
            "comparison_operator": "EQ",
            "canonical_value": "V",
            "actor_id": "forbidden",
        })


def test_no_latest_default_or_fuzzy_resolver_surface():
    assert not hasattr(m, "resolve_latest")
    assert not hasattr(m, "resolve_default")
    assert not hasattr(m, "resolve_fuzzy")
    assert not hasattr(m, "lookup_authority")


def test_runtime_binding_fails_without_explicit_hq_adoption_selection_evidence():
    binding, _ = _valid_binding()
    with pytest.raises(m.GrammarAuthorityNotCurrent):
        m.validate_runtime_binding(
            binding,
            expected_adoption_current_selection_evidence_refs=(),
        )


def test_exact_post_adoption_binding_mechanics_pass_only_with_explicit_pinned_evidence():
    binding, adoption = _valid_binding()
    assert m.validate_runtime_binding(
        binding,
        expected_adoption_current_selection_evidence_refs=adoption,
    ) is binding


def test_authority_id_mutation_fails():
    binding, adoption = _valid_binding()
    mutated = replace(
        binding,
        authority_ref=AuthorityRef("WRONG", m.AUTHORITY_VERSION, m.AUTHORITY_CONTENT_HASH),
    )
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(mutated, expected_adoption_current_selection_evidence_refs=adoption)


def test_authority_version_mutation_fails():
    binding, adoption = _valid_binding()
    mutated = replace(
        binding,
        authority_ref=AuthorityRef(m.AUTHORITY_ID, "9.9.9", m.AUTHORITY_CONTENT_HASH),
    )
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(mutated, expected_adoption_current_selection_evidence_refs=adoption)


def test_authority_content_hash_mutation_fails():
    binding, adoption = _valid_binding()
    mutated = replace(
        binding,
        authority_ref=AuthorityRef(m.AUTHORITY_ID, m.AUTHORITY_VERSION, "0" * 64),
    )
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(mutated, expected_adoption_current_selection_evidence_refs=adoption)


@pytest.mark.parametrize("field,value", [
    ("authority_kind", "COORDINATE_AUTHORITY"),
    ("governed_operation", "RESOLVE_ANY_PREDICATE"),
    ("governed_object_family", "EmpiricalCoordinateFact@1.0.0"),
])
def test_runtime_scope_mutations_fail(field, value):
    binding, adoption = _valid_binding()
    mutated = replace(binding, **{field: value})
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(mutated, expected_adoption_current_selection_evidence_refs=adoption)


def test_operator_semantics_mutation_fails():
    binding, adoption = _valid_binding()
    mutated_ref = ExactRef(
        "PREDICATE_OPERATOR_SEMANTICS",
        "D08_EMPIRICAL_POSITION_COORDINATE_EQ@1.0.0",
        "0" * 64,
    )
    mutated = replace(binding, operator_semantics_refs=(m.COORDINATE_SEMANTICS_REF, mutated_ref))
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(mutated, expected_adoption_current_selection_evidence_refs=adoption)


def test_owner_jurisdiction_mutation_fails():
    binding, adoption = _valid_binding()
    wrong_owner = ExactRef("OWNER_JURISDICTION", "WRONG", "0" * 64)
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(
            replace(binding, owner_jurisdiction_ref=wrong_owner),
            expected_adoption_current_selection_evidence_refs=adoption,
        )


def test_currentness_mutation_fails():
    binding, adoption = _valid_binding()
    with pytest.raises(m.GrammarAuthorityNotCurrent):
        m.validate_runtime_binding(
            replace(binding, currentness=m.CANDIDATE_NOT_ADOPTED),
            expected_adoption_current_selection_evidence_refs=adoption,
        )


def test_adoption_selection_evidence_mutation_fails():
    binding, adoption = _valid_binding()
    wrong = (_evidence("wrong-adoption"),)
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(binding, expected_adoption_current_selection_evidence_refs=wrong)


def test_immutable_provenance_must_close_over_candidate_and_adoption_evidence():
    binding, adoption = _valid_binding()
    mutated = replace(binding, immutable_provenance_refs=adoption)
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(mutated, expected_adoption_current_selection_evidence_refs=adoption)
