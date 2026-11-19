"""Codex acc264 joined sourcefree interpretation boundary, PYAT downstream guards.

The ANVIL raw-lane/predicate/I05/Batch patches are NOT part of this PR:
tests here prove only the exact PRE553 S04/FF01 consumer defenses and
operation-version CURRENT behavior from already-qualified native I03 facts.
No constructed original GSS, no original-source use, no mapping issuer.
"""
from copy import deepcopy

import pytest

from rawlsing_next.pre553_empirical_objects import (
    ExactRef, canonical_json, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_interpretation_qualification import (
    InterpretationQualificationError, S04InterpretationCurrent,
    contains_unresolved_response, refuse_positive_uninterpreted_support,
)
from rawlsing_next.pre553_s04_observed_research import (
    S04ObservedKnowledge, receive_s04_i03_research,
)
from rawlsing_next.pre553_s04_general_joint_algebra import (
    S04GeneralAlgebraError, S04GeneralJointWorkspace, S04Projection,
)
from rawlsing_next.tests.test_pre553_s04_observed_research import _real


def _observed():
    _, _, _, query, execution = _real(tag="S04-INTERPRETATION-CURRENT")
    return query, execution, receive_s04_i03_research(
        query=query, execution=execution,
    )


def test_uninterpreted_observed_value_is_not_a_source_missing_or_boolean_false():
    unknown = {"typed_response_state": "INVALID_UNRESOLVED"}
    assert contains_unresolved_response(unknown)
    assert contains_unresolved_response(["0", unknown, "1"])
    assert contains_unresolved_response({"cell": {"response_state": "INVALID_UNRESOLVED"}})
    for still_distinct in (
        "INVALID_UNRESOLVED",
        "42", None, "MISSING", {"typed_response_state": "MISSING"},
        {"typed_response_state": "NOT_ASKED"},
        {"typed_response_state": "INAPPLICABLE"},
    ):
        assert not contains_unresolved_response(still_distinct)
    refuse_positive_uninterpreted_support(
        cell=unknown, raw_support=0, consumer="test",
    )
    with pytest.raises(InterpretationQualificationError, match="UNRESOLVED_INTERPRETATION"):
        refuse_positive_uninterpreted_support(
            cell=unknown, raw_support=1, consumer="test",
        )


def test_self_rehashed_positive_unresolved_s04_cannot_be_counted_by_cached_algebra():
    _, _, valid = _observed()
    m = valid.material()
    # Build a hash-valid counterfeit that looks internally complete but
    # replaces a positive target state with Codex's unresolved raw-lane
    # marker. The original I03 query never issued this new interpretation.
    marker = {"typed_response_state": "INVALID_UNRESOLVED"}
    m["target_domains"][0][1] = marker
    for cell in m["complete_cells"]:
        if cell["cell"][0] == "1":
            cell["cell"][0] = marker
    m["full_query_target_topology"]["components"][0]["domain"][1] = marker
    counterfeit = S04ObservedKnowledge(canonical_json(m), semantic_hash(m))
    with pytest.raises(S04GeneralAlgebraError, match="UNRESOLVED_INTERPRETATION"):
        S04GeneralJointWorkspace(
            knowledge=counterfeit,
            expected_knowledge_ref=counterfeit.ref,
        )


def test_exact_mapping_epoch_changes_invalidate_cached_context_even_when_source_is_current():
    _, _, valid = _observed()
    semantics = exact_ref(valid.material()["response_semantics_ref"], "source response semantics")
    current = {"mapping": semantics}
    authority = S04InterpretationCurrent(
        expected_response_semantics_ref=semantics,
        resolve_current_response_semantics_ref=lambda: current["mapping"],
    )
    workspace = S04GeneralJointWorkspace(
        knowledge=valid,
        expected_knowledge_ref=valid.ref,
        current_guard=lambda: None,
        interpretation_current=authority,
    )
    first = workspace.query(S04Projection((0,), {1: "0"})).material()
    assert first["raw_selected_full_case_n"] == 2
    assert first["interpretation_version_ref"] == semantics.as_dict()
    assert first["interpretation_current_check"].startswith("BOUND_EXACT")
    before = workspace.cache_stats()["filter_cache_hits"]
    workspace.query(S04Projection((0,), {1: "0"}))
    assert workspace.cache_stats()["filter_cache_hits"] > before
    current["mapping"] = ExactRef(semantics.kind, "urn:test:changed-interpreter",
                                  semantic_hash("new valid mapping"))
    with pytest.raises(InterpretationQualificationError, match="VERSION_STALE"):
        workspace.query(S04Projection((0,), {1: "0"}))
    # The exact immutable old research remains historically inspectable
    # under its old source state, but cannot claim CURRENT under new mapping.
    offline = S04GeneralJointWorkspace(
        knowledge=valid, expected_knowledge_ref=valid.ref,
    ).query(S04Projection((0,), {1: "0"})).material()
    assert offline["interpretation_current_check"] == "INTERPRETATION_CURRENT_UNVERIFIED"


def test_new_mapping_self_echo_cannot_rebind_old_source_knowledge():
    _, _, valid = _observed()
    semantics = exact_ref(valid.material()["response_semantics_ref"], "response semantics")
    new = ExactRef(semantics.kind, "urn:test:changed-interpreter", semantic_hash("new mapping"))
    forged = S04InterpretationCurrent(
        expected_response_semantics_ref=new,
        resolve_current_response_semantics_ref=lambda: new,
    )
    with pytest.raises(S04GeneralAlgebraError, match="INTERPRETATION_BINDING_NOT_IN_SOURCE"):
        S04GeneralJointWorkspace(
            knowledge=valid,
            expected_knowledge_ref=valid.ref,
            interpretation_current=forged,
        )


def test_unpinned_and_callback_false_results_do_not_invent_issuer_approval():
    _, _, valid = _observed()
    semantics = exact_ref(valid.material()["response_semantics_ref"], "response semantics")
    invalid = S04InterpretationCurrent(
        expected_response_semantics_ref=semantics,
        resolve_current_response_semantics_ref=lambda: "valid",
    )
    with pytest.raises(InterpretationQualificationError, match="VERSION_STALE"):
        S04GeneralJointWorkspace(
            knowledge=valid, expected_knowledge_ref=valid.ref,
            interpretation_current=invalid,
        )
