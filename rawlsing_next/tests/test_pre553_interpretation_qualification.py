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



def test_hash_consistent_supported_original_i03_claim_with_positive_unmapped_cell_refused():
    """A self-consistent source query+fact counterfeit must fail BOTH S04/FF01.

    This is stronger than simply forging an S04 JSON. Even when the source
    query domain, exact fact topology, identity hashes and supported-count
    totals agree, source interpretation UNKNOWN is NOT substantive support.
    """
    from dataclasses import replace
    from itertools import product

    from rawlsing_next.pre553_empirical_objects import (
        EmpiricalFact, EmpiricalQuerySpec, canonicalize,
    )
    from rawlsing_next.pre553_s04_observed_research import S04KnowledgeError
    from rawlsing_next.field_forge_generic_empirical_ingress import (
        FF01GenericIngressError, receive_ff01_observed_joint,
    )

    q, execution, _ = _observed()
    original = execution.facts[0]
    marker = {"typed_response_state": "INVALID_UNRESOLVED"}
    fields = dict(q.semantic_fields)
    topo = deepcopy(fields["target_arity_and_topology"])
    topo["components"][0]["domain"][1] = marker
    fields["target_arity_and_topology"] = topo
    new_q = EmpiricalQuerySpec(
        typed_state=q.typed_state,
        authority_snapshot_refs=q.authority_snapshot_refs,
        dependency_refs=q.dependency_refs,
        producer_replay_locator_or_reference_root=q.producer_replay_locator_or_reference_root,
        **fields,
    )
    domains = [list(c["domain"]) for c in topo["components"]]
    normalized_components = [
        {
            "target_ref": exact_ref(c["target_ref"], "target").as_dict(),
            "topology": "SCALAR_SINGULAR",
            "domain": list(c["domain"]),
            "target_domain_replay_ref": exact_ref(
                c["target_domain_replay_ref"], "domain replay"
            ).as_dict(),
        }
        for c in topo["components"]
    ]
    identity = semantic_hash({
        "components": normalized_components,
        "joint_order_semantics": topo["joint_order_semantics"],
        "full_domain": [
            canonicalize(list(combination)) for combination in product(*domains)
        ],
    })

    fact_fields = dict(original.semantic_fields)
    fact_topology = deepcopy(fact_fields["target_topology"])
    fact_topology["target_domain_identity"] = identity
    for row in fact_topology["complete_cell_semantic_projection"]:
        if row["cell"][0] == "1":
            row["cell"][0] = marker
    fact_fields["target_topology"] = fact_topology
    fact_fields["target_domain_identity"] = identity
    fact_fields["empirical_query_spec_ref"] = new_q.ref
    synthetic = EmpiricalFact(
        typed_state="SUPPORTED",
        authority_snapshot_refs=original.authority_snapshot_refs,
        dependency_refs=(*original.dependency_refs, new_q.ref),
        producer_replay_locator_or_reference_root=original.producer_replay_locator_or_reference_root,
        **fact_fields,
    )
    changed = replace(execution, query_ref=new_q.ref, facts=(synthetic,))
    assert synthetic.raw_numerator_support == synthetic.raw_denominator_support == 4
    assert new_q.ref != q.ref
    assert synthetic.ref != original.ref
    with pytest.raises(S04KnowledgeError, match="UNRESOLVED_INTERPRETATION"):
        receive_s04_i03_research(query=new_q, execution=changed)
    with pytest.raises(FF01GenericIngressError, match="UNRESOLVED_INTERPRETATION"):
        receive_ff01_observed_joint(
            query=new_q, execution=changed, conditioner_index=0,
            producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
        )
