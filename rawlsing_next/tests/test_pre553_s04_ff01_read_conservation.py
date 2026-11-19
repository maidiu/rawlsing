"""S04 exact knowledge must agree with generic FF01 on the SAME native I03.

This does not make FF01 authoritative upstream. It is an independent seam
falsifier until FF01's owner explicitly consumes the S04 research product.
"""
from itertools import product

from rawlsing_next.field_forge_generic_empirical_ingress import receive_ff01_observed_joint
from rawlsing_next.pre553_s04_observed_research import (
    ask_s04_exact_condition, receive_s04_i03_research,
)
from rawlsing_next.tests import test_pre553_empirical_query as native


def _same_source(parity=0):
    rows = [
        {"id": f"R{x}{y}", "responses": {"X": x, "Y": y, "Z": x ^ y ^ parity}}
        for x, y in product((0, 1), repeat=2)
    ]
    source = native._build_source(
        f"S04-FF01-PARITY-{parity}", rows, question_namespace="S04-FF01-COMMON",
    )
    issuer = native._query_authority(f"S04-FF01-PARITY-{parity}")
    predicate = native._branch_predicate(source, issuer)
    query = native._query(source, issuer, predicate, ("X", "Y", "Z"), tag="joint")
    result = native._run(source, issuer, predicate, query)
    return query, result


def test_s04_f1_f2_f4_respondent_coherent_evidence_conserves_ff01_cells():
    query, actual = _same_source()
    s04 = receive_s04_i03_research(query=query, execution=actual)
    ff = receive_ff01_observed_joint(
        query=query, execution=actual, conditioner_index=0,
        producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
    )
    up = s04.material()
    down = ff.semantic_projection()
    assert up["fact_ref"] == down["producer_fact_ref"]
    assert up["query_ref"] == down["producer_query_ref"]
    assert up["release_ref"] == down["release_ref"]
    assert up["risk_set_ref"] == down["risk_set_ref"]
    assert up["raw_eligible_condition_denominator"] == down["raw_eligible_condition_denominator"]
    assert up["raw_fully_resolved_joint_n"] == down["raw_fully_resolved_joint_n"]
    assert {
        tuple(row["cell"]): row["raw_count"] for row in up["complete_cells"]
    } == {
        tuple(row["cell"]): row["raw_support"] for row in down["complete_cells"]
    }
    assert ask_s04_exact_condition(
        knowledge=s04, target_index=2, conditions={0: "0", 1: "0"},
    ).material()["raw_conditioned_full_case_n"] == 1


def test_upstream_and_ff01_distinguish_real_3way_change_with_identical_pairs():
    q0, actual0 = _same_source(0)
    q1, actual1 = _same_source(1)
    pre0 = receive_s04_i03_research(query=q0, execution=actual0)
    pre1 = receive_s04_i03_research(query=q1, execution=actual1)
    ff0 = receive_ff01_observed_joint(
        query=q0, execution=actual0, conditioner_index=0,
        producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
    )
    ff1 = receive_ff01_observed_joint(
        query=q1, execution=actual1, conditioner_index=0,
        producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
    )
    assert pre0.ref != pre1.ref
    assert ff0.ref != ff1.ref
    assert [row["raw_count"] for row in pre0.material()["complete_cells"]] != [
        row["raw_count"] for row in pre1.material()["complete_cells"]
    ]
