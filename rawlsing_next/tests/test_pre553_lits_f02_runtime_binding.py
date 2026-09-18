from __future__ import annotations

import hashlib

import pytest

from rawlsing_next.pre553_discovery_exact import ExactBoundedDiscoveryError, _combine_predicates
from rawlsing_next.pre553_empirical_objects import ExactRef, make_empirical_predicate, semantic_hash
from rawlsing_next.pre553_lits_f02_runtime_binding import (
    BASE_GRAMMAR_AUTHORITY,
    BASE_SAME_RESPONDENT_BINDING,
    BLOCKER_TERMINAL,
    F02_GRAMMAR_AUTHORITY,
    F02RuntimeBindingBlocker,
    F02_SAME_RESPONDENT_BINDING,
    F02_SELECTOR_HASHES,
    QUERY_HASHES,
    candidate_c_disposition,
    lossless_i05_composition_blocker,
    require_lossless_i05_composability,
)


def _ref(tag: str) -> ExactRef:
    digest = hashlib.sha256(tag.encode("utf-8")).hexdigest()
    return ExactRef("EE_P2R2_TEST_REF", f"urn:rawlsing:test:ee-p2r2:{tag}:sha256:{digest}", digest)


def _predicate(grammar, binding: str, tag: str):
    qref = _ref(tag + ":question")
    vref = _ref(tag + ":value")
    opref = _ref(tag + ":operator")
    return make_empirical_predicate(
        predicate_ast={
            "op": "LEAF",
            "leaf_type": "SURVEY_RESPONSE_EVENT",
            "ee_p2r2_probe": tag,
        },
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(grammar,),
        dependency_refs=(qref, vref, opref),
        producer_replay_locator_or_reference_root=_ref(tag + ":replay"),
        grammar_authority_ref=grammar,
        coordinate_question_value_refs=(qref, vref),
        risk_set_refs=(),
        scope_refs=(),
        same_respondent_binding_semantics=binding,
        operator_semantics_refs=(opref,),
    )


def test_governed_f02_and_base_composition_contracts_are_exactly_distinct():
    blocker = lossless_i05_composition_blocker()
    assert blocker["terminal"] == BLOCKER_TERMINAL
    assert BASE_GRAMMAR_AUTHORITY != F02_GRAMMAR_AUTHORITY
    assert BASE_SAME_RESPONDENT_BINDING != F02_SAME_RESPONDENT_BINDING
    assert blocker["affected_frozen_rules"] == [
        "D02_P2_HIGHER_ORDER_K3",
        "D02_P3_CONDITIONAL_REVERSAL",
    ]
    assert len(F02_SELECTOR_HASHES) == 6
    assert len(set(F02_SELECTOR_HASHES.values())) == 6
    assert len(QUERY_HASHES) == 3
    assert len(set(QUERY_HASHES)) == 3


def test_existing_generic_i05_rejects_the_exact_kind_of_mixed_contract_d02_requires():
    base = _predicate(BASE_GRAMMAR_AUTHORITY, BASE_SAME_RESPONDENT_BINDING, "base")
    f02 = _predicate(F02_GRAMMAR_AUTHORITY, F02_SAME_RESPONDENT_BINDING, "f02")
    with pytest.raises(
        ExactBoundedDiscoveryError,
        match="composed predicates must share exact grammar and respondent binding law",
    ):
        _combine_predicates(
            (base, f02),
            op="AND",
            tag_material={"worker": "EE-P2R2", "probe": "lossless-composition"},
        )


def test_fail_closed_preflight_refuses_to_encode_a_lossy_adapter():
    with pytest.raises(F02RuntimeBindingBlocker) as exc:
        require_lossless_i05_composability()
    assert exc.value.code == BLOCKER_TERMINAL


def test_candidate_c_is_independently_candidate_local_nonqualifying_without_cacc3():
    disposition = candidate_c_disposition()
    assert disposition["earliest_p2_stage"] == "S02_C11_REACHABILITY"
    assert disposition["cacc1_missing_required_f02_response_slots"] == ["q310", "q311"]
    assert disposition["later_independent_cacc2_failure"]["frozen_role_count"] == 19
    assert set(disposition["later_independent_cacc2_failure"]["missing_f02_roles"]) == set(F02_SELECTOR_HASHES)
    assert disposition["cacc3_created"] is False
    assert disposition["cacc1_widened"] is False
    assert disposition["cacc2_widened"] is False
    assert disposition["hidden_ab_fallback"] is False
    assert disposition["candidate_local_only"] is True
    assert disposition["blocks_lits_ab"] is False
    assert disposition["blocks_wvs_ab"] is False
