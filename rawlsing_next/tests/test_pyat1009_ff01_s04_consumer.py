"""Hostile S04 -> actual existing FF01 ABI sourcefree seam. Never original source."""
from dataclasses import replace
from itertools import product

import pytest

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact, ExactRef, canonical_json, semantic_hash,
)
from rawlsing_next.pre553_s04_observed_research import (
    S04KnowledgeError, S04ObservedKnowledge, receive_s04_i03_research,
)
from rawlsing_next.pre553_s04_ff01_consumer import (
    S04FF01SeamError, receive_ff01_from_s04,
)
from rawlsing_next.field_forge_generic_empirical_ingress import (
    FF01GenericIngressError, receive_ff01_observed_joint,
)
from rawlsing_next.field_forge_observed_research import ask_observed_conditioned_support
from rawlsing_next.tests.test_pyat1009_ff01_generic_ingress import _case

RIGHTS = ("FF01_DESCRIPTIVE_SOURCEFREE",)


def _both(parity=0, *, tag="INDEPENDENT-S04-FF01"):
    _, _, _, q, r = _case(parity=parity, tag=tag)
    s04 = receive_s04_i03_research(query=q, execution=r)
    consumed = receive_ff01_from_s04(
        knowledge=s04, query=q, execution=r, conditioner_index=0,
        producer_permission_ceiling=RIGHTS,
    )
    independent_oracle = receive_ff01_observed_joint(
        query=q, execution=r, conditioner_index=0,
        producer_permission_ceiling=RIGHTS,
    )
    assert consumed.ref == independent_oracle.ref
    assert consumed.semantic_projection() == independent_oracle.semantic_projection()
    return q, r, s04, consumed


def test_existing_ff01_abi_consumes_s04_without_second_i03_execution():
    q, r, s04, ff = _both()
    assert ff.semantic_projection()["joint_arity"] == 3
    assert len(ff.semantic_projection()["complete_cells"]) == 8
    assert ff.semantic_projection()["producer_fact_ref"] == s04.material()["fact_ref"]
    answer = ask_observed_conditioned_support(
        received=ff, target_index=2, conditions={0: "0", 1: "0"},
    ).material()
    assert answer["condition_fully_resolved_n"] == 1
    assert answer["state"] != "UPSTREAM_SCIENCE_OR_SOURCE_HELD"


def test_same_pairwise_marginal_different_three_way_fates_through_s04_ff01():
    _, _, first, ff0 = _both(0, tag="REAL-TRIPLE-PARITY")
    _, _, changed, ff1 = _both(1, tag="REAL-TRIPLE-ANTIPARITY")
    assert first.ref != changed.ref
    assert ff0.ref != ff1.ref
    assert ff0.semantic_projection()["complete_cells"] != ff1.semantic_projection()["complete_cells"]


def test_direction_is_role_specific_with_different_complete_case_denominators():
    _, _, _, ff = _both()
    fwd = ask_observed_conditioned_support(
        received=ff, target_index=2, conditions={0: "0", 1: "0"},
    ).material()
    rev = ask_observed_conditioned_support(
        received=ff, target_index=0, conditions={2: "0"},
    ).material()
    assert fwd["condition_fully_resolved_n"] == 1
    assert rev["condition_fully_resolved_n"] == 2
    assert fwd["target_ref"] != rev["target_ref"]


def test_rehashed_s04_counterfeit_cannot_authorize_original_i03():
    q, r, s04, _ = _both()
    forged = s04.material()
    forged["complete_cells"][0]["raw_count"] = 999
    fake = S04ObservedKnowledge(canonical_json(forged), semantic_hash(forged))
    with pytest.raises(S04FF01SeamError, match="not issued"):
        receive_ff01_from_s04(
            knowledge=fake, query=q, execution=r, conditioner_index=0,
            producer_permission_ceiling=RIGHTS,
        )


def test_different_release_or_query_cannot_reuse_prior_s04_product():
    q0, r0, s04, _ = _both(0, tag="SOURCE-S04-0")
    q1, r1, _, _ = _both(1, tag="SOURCE-S04-1")
    with pytest.raises(S04FF01SeamError, match="not issued"):
        receive_ff01_from_s04(
            knowledge=s04, query=q1, execution=r1, conditioner_index=0,
            producer_permission_ceiling=RIGHTS,
        )


def test_causal_and_permission_widening_refuse_at_s04_ff01_edge():
    q, r, s04, _ = _both()
    with pytest.raises(FF01GenericIngressError, match="protected use"):
        receive_ff01_from_s04(
            knowledge=s04, query=q, execution=r, conditioner_index=0,
            producer_permission_ceiling=RIGHTS,
            relation_permission_ceiling=("FF02_STRUCTURAL",),
        )
    with pytest.raises(S04FF01SeamError, match="widen"):
        receive_ff01_from_s04(
            knowledge=s04, query=q, execution=r, conditioner_index=0,
            producer_permission_ceiling=RIGHTS,
            relation_permission_ceiling=("FF01_DIAGNOSTIC_READ_ONLY",),
        )


def test_s04_rejects_original_fact_domain_identity_substitution():
    q, r, _, _ = _both()
    fact = r.facts[0]
    altered = dict(fact.semantic_fields)
    altered["target_domain_identity"] = "WRONG_DOMAIN_ID"
    invalid = EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **altered,
    )
    with pytest.raises(S04KnowledgeError, match="domain identity"):
        receive_s04_i03_research(query=q, execution=replace(r, facts=(invalid,)))


def test_held_low_support_positive_count_does_not_become_ff01_joint():
    q, r, _, _ = _both()
    fact = r.facts[0]
    held = EmpiricalFact(
        typed_state="LOW_SUPPORT",
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **dict(fact.semantic_fields),
    )
    changed = replace(r, facts=(held,))
    s04 = receive_s04_i03_research(query=q, execution=changed)
    ff = receive_ff01_from_s04(
        knowledge=s04, query=q, execution=changed, conditioner_index=0,
        producer_permission_ceiling=RIGHTS,
    )
    data = ff.semantic_projection()
    assert data["producer_state"] == "LOW_SUPPORT"
    assert data["complete_cells"] == []
    assert data["held_observed_n_if_nonpositive"] == 4


def test_s04_to_ff01_cold_reader_seam_keeps_same_release_without_second_query(
    tmp_path, monkeypatch,
):
    pytest.importorskip("pyarrow")
    from rawlsing_next.tests.test_pyat1009_ff01_cold_direct_estate import _actual_cold_ff01
    old_ff, execution, query, receipt = _actual_cold_ff01(
        tmp_path, monkeypatch, parity=0,
        tag="COLD-S04-SINGLE-RELEASE", saved_name="cold-s04",
    )
    s04 = receive_s04_i03_research(query=query, execution=execution)
    actual = receive_ff01_from_s04(
        knowledge=s04, query=query, execution=execution, conditioner_index=0,
        producer_permission_ceiling=RIGHTS,
    )
    assert old_ff.ref == actual.ref
    assert actual.semantic_projection()["release_ref"] == s04.material()["release_ref"]
    assert actual.semantic_projection()["raw_fully_resolved_joint_n"] == 4
