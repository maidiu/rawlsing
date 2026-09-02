from __future__ import annotations

from itertools import product

import pytest

from rawlsing_next.field_forge_conditional_support import (
    CONDITIONER_ROLE,
    INFORMATION_LOSS,
    RELATION_FAMILY,
    TARGET_ROLE,
    FieldForgeConditionalSupportError,
    FieldForgePermissionWideningError,
    produce_exact_conditional_support_profile,
    replay_exact_conditional_support_profile,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    semantic_hash,
)


def _h(label: str) -> str:
    return semantic_hash({"test": label})


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:gt12c:{label}", _h(label))


def _auth(label: str = "source") -> AuthorityRef:
    return AuthorityRef(
        f"AUTH-{label}",
        "1.0.0",
        _h(f"authority:{label}"),
    )


def _domain_identity(conditioner_ref, target_ref, conditioner_domain, target_domain):
    components = [
        {
            "target_ref": conditioner_ref.as_dict(),
            "topology": "SCALAR_SINGULAR",
            "domain": list(conditioner_domain),
            "target_domain_replay_ref": _ref("TARGET_DOMAIN", "q86b-domain").as_dict(),
        },
        {
            "target_ref": target_ref.as_dict(),
            "topology": "SCALAR_SINGULAR",
            "domain": list(target_domain),
            "target_domain_replay_ref": _ref("TARGET_DOMAIN", "q86a-domain").as_dict(),
        },
    ]
    full_domain = [list(v) for v in product(conditioner_domain, target_domain)]
    return semantic_hash({
        "components": components,
        "joint_order_semantics": "SEMANTIC_ORDERED",
        "full_domain": full_domain,
    })


def _fixture(*, fact_state="SUPPORTED", tamper_domain_identity=False, reverse_targets=False):
    conditioner_ref = _ref("QUESTION", "Q86B")
    target_ref = _ref("QUESTION", "Q86A")
    conditioner_domain = ("0", "1", "9")
    target_domain = ("1", "2", "9")
    source_auth = _auth()
    risk = _ref("RISK_SET", "FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1")
    universe = _ref("UNIVERSE", "AFROBAROMETER-R5")
    predicate = _ref("PREDICATE", "ALL-RISK-MEMBERS")
    response_semantics = _ref("RESPONSE_STATE_SEMANTICS", "Q86-SOURCE-NATIVE")
    measure = _ref("MEASURE_BASIS", "RAW")
    q86b_domain_ref = _ref("TARGET_DOMAIN", "q86b-domain")
    q86a_domain_ref = _ref("TARGET_DOMAIN", "q86a-domain")

    targets = (target_ref, conditioner_ref) if reverse_targets else (conditioner_ref, target_ref)
    domain_by_ref = {
        conditioner_ref: (conditioner_domain, q86b_domain_ref),
        target_ref: (target_domain, q86a_domain_ref),
    }
    components = []
    for ref in targets:
        domain, replay = domain_by_ref[ref]
        components.append({
            "target_ref": ref,
            "topology": "SCALAR_SINGULAR",
            "domain": domain,
            "target_domain_replay_ref": replay,
            "topology_authority_refs": (source_auth,),
            "response_semantic_authority_refs": (source_auth,),
            "included_states": ("SUBSTANTIVE_RESPONSE", "MISSING", "DK", "REFUSAL"),
        })

    query = EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(source_auth,),
        dependency_refs=(predicate,),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "query"),
        target_refs=targets,
        target_arity_and_topology={
            "arity": 2,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": components,
        },
        condition_predicate_ref=predicate,
        risk_set_ref=risk,
        empirical_universe_refs=(universe,),
        scope_refs=(universe,),
        measure_basis_ref=measure,
        requested_output_grain={
            "source_scope_mode": "SINGLE_UNIVERSE",
            "measure_kind": "RAW",
            "risk_set_type": "COMMON_ELIGIBLE_RISK_SET",
            "response_state_semantics_ref": response_semantics,
            "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
        },
        query_authority_refs=(source_auth,),
    )

    if reverse_targets:
        # The hostile role-order test only needs a self-consistent producer object.
        first_domain, _ = domain_by_ref[targets[0]]
        second_domain, _ = domain_by_ref[targets[1]]
        cells = []
        for first, second in product(first_domain, second_domain):
            cells.append({
                "cell": [first, second],
                "cell_state": "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET",
                "raw_numerator_support": 0,
                "weighted_numerator_support_if_authorized": None,
            })
        domain_identity = semantic_hash({
            "components": [
                {
                    "target_ref": targets[0].as_dict(),
                    "topology": "SCALAR_SINGULAR",
                    "domain": list(first_domain),
                    "target_domain_replay_ref": domain_by_ref[targets[0]][1].as_dict(),
                },
                {
                    "target_ref": targets[1].as_dict(),
                    "topology": "SCALAR_SINGULAR",
                    "domain": list(second_domain),
                    "target_domain_replay_ref": domain_by_ref[targets[1]][1].as_dict(),
                },
            ],
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "full_domain": [list(v) for v in product(first_domain, second_domain)],
        })
        raw_denominator = 1 if fact_state == "SUPPORTED" else 0
        raw_numerator = 0
    else:
        counts = {
            ("0", "1"): 2,
            ("0", "2"): 1,
            ("0", "9"): 0,
            ("1", "1"): 1,
            ("1", "2"): 0,
            ("1", "9"): 2,
            ("9", "1"): 0,
            ("9", "2"): 0,
            ("9", "9"): 0,
        }
        cells = []
        for c, t in product(conditioner_domain, target_domain):
            count = counts[(c, t)] if fact_state == "SUPPORTED" else 0
            cells.append({
                "cell": [c, t],
                "cell_state": (
                    "OBSERVED_POSITIVE"
                    if count > 0
                    else ("OBSERVED_ZERO_IN_SUPPORTED_RISK_SET" if fact_state == "SUPPORTED" else "ZERO_SUPPORT")
                ),
                "raw_numerator_support": count,
                "weighted_numerator_support_if_authorized": None,
            })
        domain_identity = _domain_identity(
            conditioner_ref, target_ref, conditioner_domain, target_domain)
        raw_denominator = 6 if fact_state == "SUPPORTED" else 0
        raw_numerator = 6 if fact_state == "SUPPORTED" else 0

    if tamper_domain_identity:
        domain_identity = "0" * 64

    replay = _ref("PRE553_I03_QUERY_REPLAY", "fact-replay")
    release = _ref("C11_RELEASE", "r5")
    provenance = (release, universe)
    dependencies = (query.ref, predicate, replay, release, universe)

    fact = EmpiricalFact(
        typed_state=fact_state,
        authority_snapshot_refs=(source_auth,),
        dependency_refs=dependencies,
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
        raw_numerator_support=raw_numerator,
        raw_denominator_support=raw_denominator,
        weighted_numerator_support_if_authorized=None,
        weighted_denominator_support_if_authorized=None,
        measure_basis_ref=measure,
        response_state_semantics_ref=response_semantics,
        uncertainty_method_or_typed_state="UNCERTAINTY_UNQUANTIFIED",
        source_empirical_provenance_refs=provenance,
        replay_ref=replay,
        query_execution_contract_id="PRE553_I03_QUERY_EXECUTION@TEST",
        execution_detail="bounded GT12-C test fixture",
        source_scope_mode="SINGLE_UNIVERSE",
        measure_kind="RAW",
        risk_set_type="COMMON_ELIGIBLE_RISK_SET",
        target_domain_identity=domain_identity,
        raw_resolved_target_support=raw_numerator,
    )
    return query, fact, conditioner_ref, target_ref


def _produce(**overrides):
    query, fact, conditioner_ref, target_ref = _fixture(
        fact_state=overrides.pop("fact_state", "SUPPORTED"),
        tamper_domain_identity=overrides.pop("tamper_domain_identity", False),
        reverse_targets=overrides.pop("reverse_targets", False),
    )
    kwargs = {
        "joint_fact": fact,
        "joint_query": query,
        "conditioner_ref": conditioner_ref,
        "target_ref": target_ref,
        "producer_permission_ceiling": ("FIELD_FORGE_RELATION_PRODUCTION",),
    }
    kwargs.update(overrides)
    return produce_exact_conditional_support_profile(**kwargs), kwargs


def test_exact_count_profile_preserves_q86b_condition_denominators_and_zero_cells():
    relation, _ = _produce()
    assert relation.family == RELATION_FAMILY
    assert relation.typed_state == "SUPPORTED"
    assert relation.producer_state_blocking is False
    assert relation.semantic_projection()["participant_role_order"] == [CONDITIONER_ROLE, TARGET_ROLE]
    assert relation.semantic_projection()["information_loss"] == INFORMATION_LOSS

    rows = relation.conditional_count_profile
    assert [row["condition_state"] for row in rows] == ["0", "1", "9"]
    assert [row["condition_denominator_support"] for row in rows] == [3, 3, 0]
    q86b0 = rows[0]["target_counts"]
    assert [x["joint_support_count"] for x in q86b0] == [2, 1, 0]
    assert q86b0[2]["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"

    payload = relation.as_dict()
    assert "ratio" not in repr(payload).lower()
    assert "cause" not in payload["relation_semantics"].lower()
    assert relation.producer_fact_ref.object_id.startswith("urn:rawlsing:pre553:EmpiricalFact")


def test_deterministic_identity_and_exact_replay():
    relation, kwargs = _produce()
    relation2 = produce_exact_conditional_support_profile(**kwargs)
    assert relation2.ref == relation.ref
    replayed = replay_exact_conditional_support_profile(
        expected_ref=relation.ref,
        **kwargs,
    )
    assert replayed.ref == relation.ref


def test_role_order_is_frozen_q86b_conditioner_q86a_target():
    with pytest.raises(FieldForgeConditionalSupportError, match="role/order"):
        _produce(reverse_targets=True)


def test_domain_identity_tamper_fails_closed():
    with pytest.raises(FieldForgeConditionalSupportError, match="domain identity"):
        _produce(tamper_domain_identity=True)


def test_permission_widening_fails_closed():
    with pytest.raises(FieldForgePermissionWideningError):
        _produce(
            relation_permission_ceiling=(
                "FIELD_FORGE_RELATION_PRODUCTION",
                "STRUCTURAL_MEDIATION_INPUT",
            )
        )


@pytest.mark.parametrize(
    "state",
    ["VALID_EMPTY", "NONCOMPARABLE", "UNRESOLVED", "INTEGRITY_FAILURE"],
)
def test_nonpositive_producer_states_remain_typed_and_do_not_mint_count_profile(state):
    relation, _ = _produce(fact_state=state)
    assert relation.typed_state == state
    assert relation.producer_state_blocking is True
    assert relation.conditional_count_profile == ()
    assert relation.producer_fact_ref.kind == "EmpiricalFact@1.0.0"


def test_reference_preserving_closure_keeps_query_authority_replay_and_scope():
    relation, kwargs = _produce()
    fact = kwargs["joint_fact"]
    query = kwargs["joint_query"]
    assert relation.producer_fact_ref == fact.ref
    assert relation.producer_query_ref == query.ref
    assert relation.risk_set_ref == ExactRef(
        fact.risk_set_ref["kind"], fact.risk_set_ref["object_id"], fact.risk_set_ref["content_hash"])
    assert relation.producer_replay_ref == ExactRef(
        fact.replay_ref["kind"], fact.replay_ref["object_id"], fact.replay_ref["content_hash"])
    assert set(relation.producer_authority_refs) == set(fact.authority_snapshot_refs)
    assert relation.relation_permission_ceiling == relation.producer_permission_ceiling


def test_incomplete_or_duplicate_joint_cell_domain_fails_closed():
    query, fact, conditioner_ref, target_ref = _fixture()
    topology = dict(fact.target_topology)
    cells = list(topology["complete_cell_semantic_projection"])
    topology["complete_cell_semantic_projection"] = cells[:-1]

    replacement = EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        empirical_query_spec_ref=fact.empirical_query_spec_ref,
        empirical_universe_refs=fact.empirical_universe_refs,
        target_topology=topology,
        condition_predicate_ref=fact.condition_predicate_ref,
        risk_set_ref=fact.risk_set_ref,
        raw_numerator_support=fact.raw_numerator_support,
        raw_denominator_support=fact.raw_denominator_support,
        weighted_numerator_support_if_authorized=None,
        weighted_denominator_support_if_authorized=None,
        measure_basis_ref=fact.measure_basis_ref,
        response_state_semantics_ref=fact.response_state_semantics_ref,
        uncertainty_method_or_typed_state=fact.uncertainty_method_or_typed_state,
        source_empirical_provenance_refs=fact.source_empirical_provenance_refs,
        replay_ref=fact.replay_ref,
        query_execution_contract_id=fact.query_execution_contract_id,
        execution_detail=fact.execution_detail,
        source_scope_mode=fact.source_scope_mode,
        measure_kind=fact.measure_kind,
        risk_set_type=fact.risk_set_type,
        target_domain_identity=fact.target_domain_identity,
        raw_resolved_target_support=fact.raw_resolved_target_support,
    )
    with pytest.raises(FieldForgeConditionalSupportError, match="complete native"):
        produce_exact_conditional_support_profile(
            joint_fact=replacement,
            joint_query=query,
            conditioner_ref=conditioner_ref,
            target_ref=target_ref,
            producer_permission_ceiling=("FIELD_FORGE_RELATION_PRODUCTION",),
        )
