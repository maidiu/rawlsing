"""Fresh independent hostile matrix for GT34 OBL057 D08 grammar authority."""
from dataclasses import replace
import inspect

import pytest

from rawlsing_next import gt34_d08_empirical_predicate_grammar_authority as m
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash


def ev(label: str) -> ExactRef:
    return ExactRef("HOSTILE_SYNTHETIC_ADOPTION_EVIDENCE_TEST_ONLY", label, semantic_hash({"hostile": label}))


def valid():
    selection = (ev("hq-adoption"), ev("current-selection"))
    binding = m.exact_runtime_binding(
        adoption_current_selection_evidence_refs=selection,
        immutable_provenance_refs=m.IMMUTABLE_PROVENANCE_REFS + selection,
    )
    return binding, selection


def leaf():
    return {
        "op": "LEAF",
        "leaf_type": "EMPIRICAL_POSITION_COORDINATE",
        "coordinate_ref": "EXACT_EXTERNAL_COORDINATE",
        "comparison_operator": "EQ",
        "canonical_value": "EXACT_EXTERNAL_VALUE",
        "source_release": ["external", "external-hash"],
        "respondent_scope_refs": ["external-scope"],
        "temporal_authority": ["external-time-authority", "external-time-hash"],
    }


def test_h01_candidate_hash_exact_and_replayable():
    assert semantic_hash(m.AUTHORITY_MATERIAL) == m.AUTHORITY_CONTENT_HASH
    assert m.AUTHORITY_CONTENT_HASH == "acec40d03b5602aaa553f1f63cf2506bffe0491c008678ff973e39c3f7dcedd4"


@pytest.mark.parametrize("key", sorted(m.AUTHORITY_MATERIAL))
def test_h02_any_authority_material_mutation_changes_identity(key):
    mutated = dict(m.AUTHORITY_MATERIAL)
    value = mutated[key]
    if isinstance(value, str):
        mutated[key] = value + "__MUTATED"
    elif isinstance(value, list):
        mutated[key] = list(value) + ["MUTATED"]
    elif isinstance(value, dict):
        mutated[key] = {**value, "__mutated__": True}
    else:
        pytest.fail(f"unhandled material field type for {key}")
    assert semantic_hash(mutated) != m.AUTHORITY_CONTENT_HASH


def test_h03_historical_d08_cannot_be_substituted_as_runtime_authority():
    binding, selection = valid()
    historical = AuthorityRef("db03fcbcb5e34c28b486070628377ead0408e13a", "historical", "0" * 64)
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(replace(binding, authority_ref=historical),
                                   expected_adoption_current_selection_evidence_refs=selection)


def test_h04_q69b_coordinate_authority_cannot_be_substituted():
    binding, selection = valid()
    q69b = AuthorityRef(
        "R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY",
        "1.0.0",
        "cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c",
    )
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(replace(binding, authority_ref=q69b),
                                   expected_adoption_current_selection_evidence_refs=selection)


def test_h05_hostile_fixture_hash_cannot_be_substituted():
    binding, selection = valid()
    fixture = AuthorityRef(m.AUTHORITY_ID, m.AUTHORITY_VERSION, "f" * 64)
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(replace(binding, authority_ref=fixture),
                                   expected_adoption_current_selection_evidence_refs=selection)


@pytest.mark.parametrize("new_id,new_version,new_hash", [
    ("GT34_D08_EMPIRICAL_PREDICATE_GRAMMAR_AUTHORITY_X", m.AUTHORITY_VERSION, m.AUTHORITY_CONTENT_HASH),
    (m.AUTHORITY_ID, "1.0.1", m.AUTHORITY_CONTENT_HASH),
    (m.AUTHORITY_ID, m.AUTHORITY_VERSION, "1" * 64),
])
def test_h06_exact_tuple_mutation_fails(new_id, new_version, new_hash):
    binding, selection = valid()
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(
            replace(binding, authority_ref=AuthorityRef(new_id, new_version, new_hash)),
            expected_adoption_current_selection_evidence_refs=selection,
        )


@pytest.mark.parametrize("field,bad", [
    ("authority_kind", "COORDINATE"),
    ("authority_kind", "PREDICATE_GRAMMAR_LATEST"),
    ("governed_operation", "RESOLVE_EXACT_EMPIRICAL_POSITION_COORDINATE_NEAREST_PREDICATE"),
    ("governed_operation", "RESOLVE_ANY_EMPIRICAL_PREDICATE"),
    ("governed_object_family", "EmpiricalPredicate@latest"),
    ("governed_object_family", "EmpiricalCoordinateFact@1.0.0"),
])
def test_h07_scope_grain_mutations_fail(field, bad):
    binding, selection = valid()
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(replace(binding, **{field: bad}),
                                   expected_adoption_current_selection_evidence_refs=selection)


def test_h08_operator_semantics_order_mutation_fails():
    binding, selection = valid()
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(
            replace(binding, operator_semantics_refs=tuple(reversed(m.OPERATOR_SEMANTICS_REFS))),
            expected_adoption_current_selection_evidence_refs=selection,
        )


def test_h09_operator_semantics_missing_ref_fails():
    binding, selection = valid()
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(
            replace(binding, operator_semantics_refs=(m.COORDINATE_SEMANTICS_REF,)),
            expected_adoption_current_selection_evidence_refs=selection,
        )


def test_h10_operator_semantics_hash_mutation_fails():
    binding, selection = valid()
    bad = ExactRef(m.EQ_SEMANTICS_REF.kind, m.EQ_SEMANTICS_REF.object_id, "2" * 64)
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(
            replace(binding, operator_semantics_refs=(m.COORDINATE_SEMANTICS_REF, bad)),
            expected_adoption_current_selection_evidence_refs=selection,
        )


def test_h11_owner_jurisdiction_mutation_fails():
    binding, selection = valid()
    bad = ExactRef("OWNER_JURISDICTION", "SUB_VOZHD_SELF_ADOPTION", "3" * 64)
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(replace(binding, owner_jurisdiction_ref=bad),
                                   expected_adoption_current_selection_evidence_refs=selection)


def test_h12_candidate_currentness_lie_fails():
    binding, selection = valid()
    with pytest.raises(m.GrammarAuthorityNotCurrent):
        m.validate_runtime_binding(replace(binding, currentness=m.CANDIDATE_NOT_ADOPTED),
                                   expected_adoption_current_selection_evidence_refs=selection)


def test_h13_no_adoption_evidence_fails_closed():
    binding, _ = valid()
    with pytest.raises(m.GrammarAuthorityNotCurrent):
        m.validate_runtime_binding(binding, expected_adoption_current_selection_evidence_refs=())


def test_h14_adoption_evidence_mutation_fails():
    binding, selection = valid()
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(binding,
                                   expected_adoption_current_selection_evidence_refs=(selection[0], ev("wrong")))


def test_h15_adoption_evidence_order_mutation_fails():
    binding, selection = valid()
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(binding,
                                   expected_adoption_current_selection_evidence_refs=tuple(reversed(selection)))


def test_h16_missing_historical_provenance_fails():
    binding, selection = valid()
    prov = tuple(x for x in binding.immutable_provenance_refs if x != m.HISTORICAL_D08_REF)
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(replace(binding, immutable_provenance_refs=prov),
                                   expected_adoption_current_selection_evidence_refs=selection)


def test_h17_missing_pre553_contract_provenance_fails():
    binding, selection = valid()
    prov = tuple(x for x in binding.immutable_provenance_refs if x != m.PRE553_RUNTIME_CONTRACT_REF)
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(replace(binding, immutable_provenance_refs=prov),
                                   expected_adoption_current_selection_evidence_refs=selection)


def test_h18_missing_hq_commission_provenance_fails():
    binding, selection = valid()
    prov = tuple(x for x in binding.immutable_provenance_refs if x != m.HQ_OBL057_COMMISSION_REF)
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(replace(binding, immutable_provenance_refs=prov),
                                   expected_adoption_current_selection_evidence_refs=selection)


def test_h19_missing_adoption_provenance_fails():
    binding, selection = valid()
    prov = tuple(x for x in binding.immutable_provenance_refs if x != selection[1])
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_runtime_binding(replace(binding, immutable_provenance_refs=prov),
                                   expected_adoption_current_selection_evidence_refs=selection)


@pytest.mark.parametrize("field,bad", [
    ("op", "OR"),
    ("op", "NOT"),
    ("leaf_type", "SURVEY_RESPONSE_EVENT"),
    ("leaf_type", "ACTOR_POSITION"),
    ("comparison_operator", "NE"),
    ("comparison_operator", "LIKE"),
    ("comparison_operator", "FUZZY_EQ"),
])
def test_h20_nonowned_grammar_shapes_fail(field, bad):
    ast = leaf()
    ast[field] = bad
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_predicate_ast_shape(ast)


@pytest.mark.parametrize("forbidden", [
    "actor_id", "actor_state", "actor_semantics", "respondent_incidence",
    "subject_classification", "event_semantics", "comparator_mapping",
    "source_pooling", "psepf", "v3_mutation",
])
def test_h21_out_of_jurisdiction_semantic_imports_fail(forbidden):
    ast = leaf()
    ast[forbidden] = "ATTACK"
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_predicate_ast_shape(ast)


def test_h22_required_one_field_operands_fail_when_coordinate_missing():
    ast = leaf()
    del ast["coordinate_ref"]
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_predicate_ast_shape(ast)


def test_h23_required_one_field_operands_fail_when_value_missing():
    ast = leaf()
    del ast["canonical_value"]
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_predicate_ast_shape(ast)


def test_h24_empty_coordinate_fails():
    ast = leaf()
    ast["coordinate_ref"] = ""
    with pytest.raises(m.GrammarAuthorityIntegrityError):
        m.validate_predicate_ast_shape(ast)


def test_h25_exact_eq_leaf_with_external_nonowned_context_is_allowed():
    m.validate_predicate_ast_shape(leaf())


def test_h26_no_dynamic_resolution_surface_exists():
    names = set(dir(m))
    forbidden = {
        "resolve_latest", "resolve_default", "resolve_fuzzy", "lookup_authority",
        "latest_authority", "default_authority", "find_nearest_authority",
    }
    assert names.isdisjoint(forbidden)


def test_h27_module_does_not_import_comparator_or_v3_runtime():
    src = inspect.getsource(m)
    assert "gt34_obl031_q69b_comparator_resolver" not in src
    assert "v3_adp010_oee_executor" not in src


def test_h28_q69b_identity_is_absent_from_owned_authority_material():
    text = repr(m.AUTHORITY_MATERIAL)
    assert "R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY" not in text
    assert "PUBLIC_CLINIC_EXPERIENCE_PRESENT" not in text


def test_h29_candidate_definition_cannot_claim_adopted_current():
    candidate = m.candidate_definition()
    assert candidate["status"] == "CANDIDATE_NOT_ADOPTED"
    assert "CURRENT_ACCEPTED" not in repr(candidate)


def test_h30_exact_runtime_binding_does_not_supply_adoption_evidence_itself():
    binding = m.exact_runtime_binding(adoption_current_selection_evidence_refs=(),
                                      immutable_provenance_refs=m.IMMUTABLE_PROVENANCE_REFS)
    with pytest.raises(m.GrammarAuthorityNotCurrent):
        m.validate_runtime_binding(binding, expected_adoption_current_selection_evidence_refs=())
