from __future__ import annotations

import inspect
import hashlib
import pytest

from rawlsing_next.pre553_discovery_exact import ExactBoundedDiscoveryError, _combine_predicates
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, make_empirical_predicate
import rawlsing_next.prev3_lits1_selector_closure as f02
import rawlsing_next._pre553_query_predicate as evaluator


BASE_AUTH = AuthorityRef(
    "urn:rawlsing:pre553:as2b:lits1:authority:i03_query",
    "AS2A-BANKED-1.0.0",
    "6c6d2f5fb5f4165e5de19989bd456ee8c09f42ab175fa4d10572dc2b9403ca0d",
)
F02_AUTH = AuthorityRef(
    "urn:rawlsing:prev3:f02:lits1:predicate-grammar",
    "1.0.0",
    "bc6d433ff58e67e343f1bd1d8e3e92d691b81931dca6447716b08dbf0c8eff8b",
)

def _ref(tag: str) -> ExactRef:
    h=hashlib.sha256(tag.encode()).hexdigest()
    return ExactRef("EE_P2R3_TEST_REF", f"urn:rawlsing:test:ee-p2r3:{tag}:sha256:{h}", h)

def _p(auth, binding, tag):
    q=_ref(tag+":q")
    return make_empirical_predicate(
        predicate_ast={"op":"LEAF","leaf_type":"SURVEY_RESPONSE_EVENT","probe":tag},
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(auth,),
        dependency_refs=(q,),
        producer_replay_locator_or_reference_root=_ref(tag+":replay"),
        grammar_authority_ref=auth,
        coordinate_question_value_refs=(q,),
        risk_set_refs=(),
        scope_refs=(),
        same_respondent_binding_semantics=binding,
        operator_semantics_refs=(_ref(tag+":op"),),
    )

def test_current_i05_rejects_exact_kind_of_mixed_contract():
    base=_p(BASE_AUTH,"EXACT_SAME_RESPONDENT_ONLY","base")
    child=_p(F02_AUTH,"EXACT_SOURCE_ROW_REPLAY_WITHIN_SAME_LITS1_RELEASE","f02")
    with pytest.raises(ExactBoundedDiscoveryError, match="share exact grammar and respondent binding law"):
        _combine_predicates((base,child),op="AND",tag_material={"worker":"EE-P2R3"})

def test_f02_selector_producer_uses_distinct_survey_response_event_leaf_dialect():
    src=inspect.getsource(f02.predicate)
    assert '"operation":"survey_response_EQ"' in src
    assert '"question_ref":qr' in src
    assert '"response_value_ref":vr' in src
    assert '"source_native_value":v' in src
    assert '"release_ref":release' in src
    assert "question_semantic_ref" not in src
    assert "response_topology_authority_ref" not in src

def test_accepted_evaluator_requires_public_pre553_leaf_fields_not_f02_aliases():
    src=inspect.getsource(evaluator._leaf_match)
    for token in (
        "question_semantic_ref",
        "component_or_event_selector_ref",
        "response_value_or_state_ref",
        "response_topology_authority_ref",
        "response_semantic_authority_ref",
    ):
        assert token in src
    assert 'operator not in {"EQ", "IN", "STATE_EQ"}' in src
    assert 'node.get("question_ref")' not in src
    assert 'node.get("response_value_ref")' not in src

def test_f02_composite_release_is_custom_reference_union_not_i02_realization():
    src=inspect.getsource(f02.build_selector_closure)
    assert "F02_LITS1_C11_COMPOSITE_RELEASE@1.0.0" in src
    assert '"base_release_ref":base' in src
    assert "validate_c11_source_release" not in src
    assert "C11Repository" not in src

def test_frozen_frontier_and_query_identities_are_not_rewritten_by_this_court():
    assert f02.D02_FRONTIER_INVARIANTS["expected_compiled_candidate_count"] == 50
    assert f02.D02_FRONTIER_INVARIANTS["expected_i03_query_execution_count"] == 77
    assert f02.D02_FRONTIER_INVARIANTS["maximum_conditioner_arity_K"] == 3
    assert f02.D02_FRONTIER_INVARIANTS["maximum_target_arity_J"] == 2
