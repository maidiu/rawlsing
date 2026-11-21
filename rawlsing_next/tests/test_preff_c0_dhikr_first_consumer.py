"""C0/C3 DHIKR conservation: I05 executed discovery -> S04 -> real FF01.

This is not a new scientific selector or a copied research engine. It
exercises the EXISTING independently source-executed I05 all-k-way
frontier, preserving supported / valid-empty validation while consuming
the real same-person joint via S04, then FF01, without second I03.

No inference to population, source-original rights, predictor rank,
adaptive stopping, causal force or SEAM actors is permitted here.
"""
from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_s04_i05_reception import receive_s04_i05_role
from rawlsing_next.pre553_s04_general_joint_algebra import (
    S04GeneralJointWorkspace, S04Projection,
)
from rawlsing_next.pre553_s04_ff01_consumer import receive_ff01_from_s04
from rawlsing_next.tests.test_pyat1009_ff01_i05_role_ingress import _real_frontier


def _receive_canonical_chain(discovery, receipt):
    knowledge, role = receive_s04_i05_role(
        discovery=discovery,
        candidate_receipt_ref=receipt.ref,
        query_role="BASE",
    )
    r = role.material()
    query_ref = exact_ref(r["query_ref"], "I05 selected query")
    fact_ref = exact_ref(r["fact_ref"], "I05 selected fact")
    release = exact_ref(r["source_release_ref"], "I05 exact release")
    qs = [q for q in discovery.executed_queries if q.ref == query_ref]
    fs = [f for f in discovery.empirical_facts if f.ref == fact_ref]
    assert len(qs) == len(fs) == 1
    original = QueryExecutionResult(
        query_ref=query_ref,
        facts=(fs[0],),
        source_scope_mode="SINGLE_UNIVERSE",
        release_refs=(release,),
    )
    ff = receive_ff01_from_s04(
        knowledge=knowledge,
        query=qs[0],
        execution=original,
        conditioner_index=0,
        producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
    )
    workspace = S04GeneralJointWorkspace(
        knowledge=knowledge,
        expected_knowledge_ref=knowledge.ref,
    )
    return knowledge, role, ff, workspace


def test_existing_dhikr_i05_frontier_full_eight_candidate_positive_and_negative_to_same_s04_ff01():
    frontier = _real_frontier()
    assert frontier.candidate_count == frontier.covered_candidate_count == 8
    assert {r.typed_state for r in frontier.receipts} == {
        "VALID_EMPTY", "DISCOVERED_RESULT_SUPPORTED",
    }
    observed = []
    for receipt in frontier.receipts:
        knowledge, role, ff, workspace = _receive_canonical_chain(
            frontier, receipt,
        )
        material = role.material()
        assert material["candidate_receipt_ref"] == receipt.ref.as_dict()
        assert material["candidate_validation_state"] == receipt.typed_state
        assert material["s04_observed_ref"] == knowledge.ref.as_dict()
        assert ff.semantic_projection()["producer_fact_ref"] == material["fact_ref"]
        assert ff.semantic_projection()["joint_arity"] == 3
        assert len(ff.semantic_projection()["complete_cells"]) == 8
        assert ff.semantic_projection()["raw_fully_resolved_joint_n"] == 4
        assert sum(c["raw_support"] for c in ff.semantic_projection()["complete_cells"]) == 4
        exact = workspace.query(S04Projection((1, 2), {0: "0"})).material()
        assert exact["raw_selected_full_case_n"] == 2
        assert exact["source_fact_ref"] == material["fact_ref"]
        assert exact["no_second_i03_or_source_query"]
        assert exact["comparative_predictor_rank"] is None
        projection = ff.semantic_projection()
        observed.append((
            knowledge.ref, ff.ref, receipt.typed_state,
            canonical_json(projection["complete_cells"]),
            canonical_json(projection["target_refs"]),
            projection["raw_fully_resolved_joint_n"],
            canonical_json(projection["risk_set_ref"]),
            canonical_json(projection["release_ref"]),
        ))
    # Eight differently adjudicated I05 candidates carry eight distinct
    # original query/fact evidence identities. Collapsing those identities
    # is not conservation. The *same source-observed full case data* is
    # conserved across those separately scoped first consumers.
    assert len({x[0] for x in observed}) == 8
    assert len({x[1] for x in observed}) == 8
    assert len({x[3] for x in observed}) == 1
    assert len({x[4] for x in observed}) == 1
    assert {x[5] for x in observed} == {4}
    assert len({x[6] for x in observed}) == 1
    assert len({x[7] for x in observed}) == 1
    assert {x[2] for x in observed} == {
        "VALID_EMPTY", "DISCOVERED_RESULT_SUPPORTED",
    }
