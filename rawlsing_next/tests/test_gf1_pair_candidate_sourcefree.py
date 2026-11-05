"""GF1 selective capital-reuse proof, sourcefree current native objects only.

TEST_ONLY only. No generic Field Forge scientific issuer or production grant.
"""
from __future__ import annotations

from itertools import product

import pytest

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, EmpiricalFact, EmpiricalQuerySpec, ExactRef, semantic_hash,
)
from rawlsing_next._gf1_candidate.generic_native_pair_relation import (
    GenericNativePairError, produce_generic_native_pair_relation,
    replay_generic_native_pair_relation,
)
from rawlsing_next._gf1_candidate.gf1_pair_support_consumer import (
    compute_pair_support_signature,
)


def _ref(kind, label):
    return ExactRef(kind, f"urn:test:gf1:nonq86:{label}", semantic_hash({"gf1": label}))


def _native_binary_pair(*, mixed=False):
    """Use actual current PRE553 EmpiricalQuerySpec/EmpiricalFact, not a mock DTO."""
    c_ref, t_ref = _ref("QUESTION", "Q41X"), _ref("QUESTION", "Q53Y")
    auth = AuthorityRef("GF1-TEST-SOURCE", "1.0.0", semantic_hash({"authority": "GF1 test"}))
    universe, risk = _ref("UNIVERSE", "WAVE-SOURCEFREE"), _ref("RISK_SET", "same-respondent")
    predicate = _ref("PREDICATE", "all-eligible")
    measure = _ref("MEASURE_BASIS", "raw")
    response = _ref("RESPONSE_STATE_SEMANTICS", "binary")
    domains = ("0", "1")
    components = [
        {
            "target_ref": ref,
            "topology": "SCALAR_SINGULAR",
            "domain": domains,
            "target_domain_replay_ref": _ref("TARGET_DOMAIN", label + "-domain"),
            "topology_authority_refs": (auth,),
            "response_semantic_authority_refs": (auth,),
            "included_states": ("SUBSTANTIVE_RESPONSE", "MISSING", "DK", "REFUSAL"),
        }
        for ref, label in ((c_ref, "Q41X"), (t_ref, "Q53Y"))
    ]
    query = EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(auth,),
        dependency_refs=(predicate,),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "query"),
        target_refs=(c_ref, t_ref),
        target_arity_and_topology={
            "arity": 2, "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": components,
        },
        condition_predicate_ref=predicate,
        risk_set_ref=risk,
        empirical_universe_refs=(universe,),
        scope_refs=(universe,),
        measure_basis_ref=measure,
        requested_output_grain={
            "source_scope_mode": "SINGLE_UNIVERSE", "measure_kind": "RAW",
            "risk_set_type": "COMMON_ELIGIBLE_RISK_SET",
            "response_state_semantics_ref": response,
            "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
        },
        query_authority_refs=(auth,),
    )
    projected_components = [
        {
            "target_ref": comp["target_ref"].as_dict(),
            "topology": comp["topology"], "domain": list(comp["domain"]),
            "target_domain_replay_ref": comp["target_domain_replay_ref"].as_dict(),
        }
        for comp in components
    ]
    domain_identity = semantic_hash({
        "components": projected_components,
        "joint_order_semantics": "SEMANTIC_ORDERED",
        "full_domain": [list(v) for v in product(domains, repeat=2)],
    })
    cells = []
    for x, y in product(domains, repeat=2):
        n = 1 if mixed or x == y else 0
        cells.append({
            "cell": [x, y],
            "cell_state": "OBSERVED_POSITIVE" if n else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET",
            "raw_numerator_support": n,
            "weighted_numerator_support_if_authorized": None,
        })
    replay, release = _ref("PRE553_I03_QUERY_REPLAY", "fact-replay"), _ref("C11_RELEASE", "frozen")
    total = sum(cell["raw_numerator_support"] for cell in cells)
    fact = EmpiricalFact(
        typed_state="SUPPORTED",
        authority_snapshot_refs=(auth,),
        dependency_refs=(query.ref, predicate, replay, release, universe),
        producer_replay_locator_or_reference_root=replay,
        empirical_query_spec_ref=query.ref,
        empirical_universe_refs=(universe,),
        target_topology={
            "arity": 2,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "target_domain_identity": domain_identity,
            "complete_cell_semantic_projection": cells,
        },
        condition_predicate_ref=predicate,
        risk_set_ref=risk,
        raw_numerator_support=total,
        raw_denominator_support=total,
        weighted_numerator_support_if_authorized=None,
        weighted_denominator_support_if_authorized=None,
        measure_basis_ref=measure,
        response_state_semantics_ref=response,
        uncertainty_method_or_typed_state="UNCERTAINTY_UNQUANTIFIED",
        source_empirical_provenance_refs=(release, universe),
        replay_ref=replay,
        query_execution_contract_id="PRE553_I03_QUERY_EXECUTION@TEST",
        execution_detail="non-Q86 current native object sourcefree fixture",
        source_scope_mode="SINGLE_UNIVERSE",
        measure_kind="RAW",
        risk_set_type="COMMON_ELIGIBLE_RISK_SET",
        target_domain_identity=domain_identity,
        raw_resolved_target_support=total,
    )
    return fact, query, c_ref, t_ref


def _produce(*, mixed=False, relation_permission_ceiling=("GF1_SOURCEFREE_TEST",)):
    fact, query, c_ref, t_ref = _native_binary_pair(mixed=mixed)
    relation = produce_generic_native_pair_relation(
        joint_fact=fact, joint_query=query,
        conditioner_ref=c_ref, target_ref=t_ref,
        producer_permission_ceiling=("GF1_SOURCEFREE_TEST",),
        relation_permission_ceiling=relation_permission_ceiling,
    )
    return relation, fact, query


def test_nonq86_native_pair_real_consumer_and_count_ablation():
    positive, fact, query = _produce(mixed=False)
    observed = compute_pair_support_signature(positive)
    assert observed["decision_state"] == "PAIR_SUPPORT_SIGNATURE_COMPUTED"
    assert observed["separation_class"] == "EXACT_PAIR_SEPARATION"
    assert observed["joint_support_total"] == 2
    assert observed["support_vectors"] == {
        "0": {"0": 1, "1": 0}, "1": {"0": 0, "1": 1},
    }
    assert observed["read_relation_object_id"] == positive.object_id
    assert observed["production_owner_commit"] is False
    assert replay_generic_native_pair_relation(positive, joint_fact=fact, joint_query=query)["matches_original"]

    mixed, _, _ = _produce(mixed=True)
    changed = compute_pair_support_signature(mixed)
    assert changed["separation_class"] == "NO_PAIR_SEPARATION"
    assert changed["joint_support_total"] == 4
    assert changed["result_hash"] != observed["result_hash"]
    assert mixed.object_id != positive.object_id


def test_sourcefree_authority_refusal_and_identity_poison():
    with pytest.raises(GenericNativePairError):
        _produce(relation_permission_ceiling=("GF1_SOURCEFREE_TEST", "UNGRANTED"))
    from dataclasses import replace
    valid, _, _ = _produce()
    poisoned = replace(valid, content_hash="0" * 64)
    refusal = compute_pair_support_signature(poisoned)
    assert refusal["decision_state"] == "CONSUMER_RELATION_IDENTITY_MISMATCH"
    assert refusal["downstream_value_produced"] is False
    assert refusal.get("result_hash") is None
