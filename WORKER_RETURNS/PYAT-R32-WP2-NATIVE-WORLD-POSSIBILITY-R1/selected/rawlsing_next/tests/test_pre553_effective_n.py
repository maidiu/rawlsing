from __future__ import annotations

import hashlib
from fractions import Fraction

import pytest

from rawlsing_next.pre553_effective_n import (
    EffectiveNError,
    compute_effective_n,
    replay_effective_n,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    WeightMeasureFact,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:f018:{kind.lower()}:{tag}", _h(f"f018:{kind}:{tag}"))


def _auth(tag: str, *, state: str = "ALLOW") -> AuthoritySnapshot:
    digest = _h(f"f018-authority:{tag}:1.0.0:{state}")
    return AuthoritySnapshot(
        typed_state=state,
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"authority-{tag}-{state}"),
        authority_id=f"F018-AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=digest,
        authority_kind="WEIGHT_DESIGN_ESTIMAND",
        decision_state=state,
        governed_operations=(f"F018-OP-{tag}",),
        governed_object_families=("WeightMeasureFact@1.0.0",),
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"f018-semantics:{tag}:{state}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", f"{tag}-{state}"),
    )


def _query_auth(tag: str) -> AuthoritySnapshot:
    digest = _h(f"f018-query-authority:{tag}:1.0.0")
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"query-authority-{tag}"),
        authority_id=f"F018-QUERY-AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=digest,
        authority_kind="PREDICATE_GRAMMAR",
        decision_state="ALLOW",
        governed_operations=(f"F018-QUERY-OP-{tag}",),
        governed_object_families=("EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"f018-query-semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", f"query-{tag}"),
    )


def _query(
    tag: str,
    *,
    universe_ref: ExactRef,
    risk_ref: ExactRef,
    condition_ref: ExactRef,
    query_auth: AuthoritySnapshot,
    measure_kind: str,
    weight_basis_id: str | None = "W",
) -> EmpiricalQuerySpec:
    grain = {
        "source_scope_mode": "SINGLE_UNIVERSE",
        "measure_kind": measure_kind,
        "risk_set_type": "COMMON_ELIGIBLE_RISK_SET",
        "response_state_semantics_ref": _ref("RESPONSE_STATE_SEMANTICS", tag),
    }
    if weight_basis_id is not None:
        grain["weight_basis_id"] = weight_basis_id
    target_a = _ref("QUESTION_NATIVE", f"{tag}-A")
    target_b = _ref("QUESTION_NATIVE", f"{tag}-B")
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(query_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"query-{tag}"),
        target_refs=(target_a, target_b),
        target_arity_and_topology={
            "arity": 2,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": (
                {"target_ref": target_a.as_dict(), "topology": "SCALAR_SINGULAR"},
                {"target_ref": target_b.as_dict(), "topology": "SCALAR_SINGULAR"},
            ),
        },
        condition_predicate_ref=condition_ref,
        risk_set_ref=risk_ref,
        empirical_universe_refs=(universe_ref,),
        scope_refs=(universe_ref,),
        measure_basis_ref=_ref("MEASURE_BASIS", measure_kind),
        requested_output_grain=grain,
        query_authority_refs=(query_auth.authority_ref,),
    )


def _weight(
    tag: str,
    *,
    universe_ref: ExactRef,
    respondent_ref: ExactRef,
    scope_ref: ExactRef,
    source_ref: ExactRef,
    design_auth: AuthoritySnapshot,
    estimand_auth: AuthoritySnapshot,
    value,
    state: str = "WEIGHT_VALID_AUTHORIZED",
    basis: str = "W",
) -> WeightMeasureFact:
    # The object's own authority closure can remain positive while the explicit
    # estimand authority is separately nonpositive; that is how the separation
    # hostile fixture below proves the two fields are not collapsed.
    return WeightMeasureFact(
        typed_state=state,
        authority_snapshot_refs=(design_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"weight-{tag}"),
        empirical_universe_ref=universe_ref,
        scoped_respondent_ref=respondent_ref,
        weight_basis_id=basis,
        exact_weight_value_representation=value,
        weight_state=state,
        weight_source_ref=source_ref,
        design_authority_ref=design_auth.authority_ref,
        estimand_authority_ref=estimand_auth.authority_ref,
        normalization_or_recalibration_rule_ref=None,
        effective_scope_ref=scope_ref,
    )


def _fact(
    tag: str,
    *,
    query: EmpiricalQuerySpec,
    query_auth: AuthoritySnapshot,
    universe_ref: ExactRef,
    risk_ref: ExactRef,
    condition_ref: ExactRef,
    release_ref: ExactRef,
    denominator_members: tuple[ExactRef, ...],
    weights: tuple[WeightMeasureFact, ...] = (),
    weighted_denominator=None,
    state: str = "SUPPORTED",
) -> EmpiricalFact:
    provenance = (release_ref, *(weight.ref for weight in weights))
    return EmpiricalFact(
        typed_state=state,
        authority_snapshot_refs=(query_auth.authority_ref,),
        dependency_refs=(query.ref,),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"fact-{tag}"),
        empirical_query_spec_ref=query.ref,
        empirical_universe_refs=(universe_ref,),
        target_topology={
            "arity": 2,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "target_domain_identity": _h(f"domain:{tag}"),
            "complete_cell_semantic_projection": (),
        },
        condition_predicate_ref=condition_ref,
        risk_set_ref=risk_ref,
        raw_numerator_support=len(denominator_members),
        raw_denominator_support=len(denominator_members),
        weighted_numerator_support_if_authorized=weighted_denominator,
        weighted_denominator_support_if_authorized=weighted_denominator,
        measure_basis_ref=query.measure_basis_ref,
        response_state_semantics_ref=_ref("RESPONSE_STATE_SEMANTICS", tag),
        uncertainty_method_or_typed_state="UNCERTAINTY_UNQUANTIFIED",
        source_empirical_provenance_refs=provenance,
        replay_ref=_ref("I03_REPLAY", tag),
        query_execution_contract_id="PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0",
        execution_detail="test exact fact",
        source_scope_mode="SINGLE_UNIVERSE",
        measure_kind=query.requested_output_grain["measure_kind"],
        risk_set_type="COMMON_ELIGIBLE_RISK_SET",
        denominator_member_refs=tuple(sorted(denominator_members, key=lambda ref: ref.key)),
    )


def _weighted_fixture(tag: str = "weighted"):
    universe = _ref("EmpiricalUniverse", tag)
    release = _ref("C11LogicalRelease", tag)
    risk = _ref("RISK_SET", tag)
    condition = _ref("EmpiricalPredicate", tag)
    scope = _ref("WEIGHT_SCOPE", tag)
    source = _ref("WEIGHT_SOURCE", tag)
    members = tuple(sorted((_ref("RespondentIdentity", f"{tag}-R1"), _ref("RespondentIdentity", f"{tag}-R2")), key=lambda r: r.key))
    query_auth = _query_auth(tag)
    design_auth = _auth(f"{tag}-design")
    estimand_auth = _auth(f"{tag}-estimand")
    query = _query(
        tag,
        universe_ref=universe,
        risk_ref=risk,
        condition_ref=condition,
        query_auth=query_auth,
        measure_kind="GOVERNED_WEIGHTED",
    )
    weights = (
        _weight(
            f"{tag}-1",
            universe_ref=universe,
            respondent_ref=members[0],
            scope_ref=scope,
            source_ref=source,
            design_auth=design_auth,
            estimand_auth=estimand_auth,
            value="1",
        ),
        _weight(
            f"{tag}-2",
            universe_ref=universe,
            respondent_ref=members[1],
            scope_ref=scope,
            source_ref=source,
            design_auth=design_auth,
            estimand_auth=estimand_auth,
            value="2",
        ),
    )
    fact = _fact(
        tag,
        query=query,
        query_auth=query_auth,
        universe_ref=universe,
        risk_ref=risk,
        condition_ref=condition,
        release_ref=release,
        denominator_members=members,
        weights=weights,
        weighted_denominator={"$exact_fraction": [3, 1]},
    )
    registry = AuthorityRegistry((query_auth, design_auth, estimand_auth))
    return {
        "universe": universe,
        "release": release,
        "risk": risk,
        "condition": condition,
        "scope": scope,
        "source": source,
        "members": members,
        "query_auth": query_auth,
        "design_auth": design_auth,
        "estimand_auth": estimand_auth,
        "query": query,
        "weights": weights,
        "fact": fact,
        "registry": registry,
    }


def test_weighted_effective_n_is_exact_replayable_and_input_order_invariant():
    fx = _weighted_fixture()
    product = compute_effective_n(
        fact=fx["fact"],
        query=fx["query"],
        weight_facts=fx["weights"],
        authority_registry=fx["registry"],
        release_refs=(fx["release"],),
        authorized_weight_scope_ref=fx["scope"],
    )
    assert product.typed_state == "SUPPORTED"
    assert product.sum_w == Fraction(3, 1)
    assert product.sum_w2 == Fraction(5, 1)
    assert product.effective_n == Fraction(9, 5)
    assert product.design_authority_refs
    assert product.estimand_authority_refs

    reversed_product = compute_effective_n(
        fact=fx["fact"],
        query=fx["query"],
        weight_facts=tuple(reversed(fx["weights"])),
        authority_registry=fx["registry"],
        release_refs=(fx["release"],),
        authorized_weight_scope_ref=fx["scope"],
    )
    assert reversed_product.product_ref == product.product_ref
    assert reversed_product.replay_ref == product.replay_ref

    replayed = replay_effective_n(
        expected_product_ref=product.product_ref,
        expected_replay_ref=product.replay_ref,
        fact=fx["fact"],
        query=fx["query"],
        weight_facts=fx["weights"],
        authority_registry=fx["registry"],
        release_refs=(fx["release"],),
        authorized_weight_scope_ref=fx["scope"],
    )
    assert replayed == product


def test_raw_unweighted_does_not_manufacture_effective_n_from_respondent_count():
    tag = "raw"
    universe = _ref("EmpiricalUniverse", tag)
    release = _ref("C11LogicalRelease", tag)
    risk = _ref("RISK_SET", tag)
    condition = _ref("EmpiricalPredicate", tag)
    query_auth = _query_auth(tag)
    query = _query(
        tag,
        universe_ref=universe,
        risk_ref=risk,
        condition_ref=condition,
        query_auth=query_auth,
        measure_kind="RAW",
        weight_basis_id=None,
    )
    members = tuple(_ref("RespondentIdentity", f"{tag}-R{i}") for i in range(1, 5))
    fact = _fact(
        tag,
        query=query,
        query_auth=query_auth,
        universe_ref=universe,
        risk_ref=risk,
        condition_ref=condition,
        release_ref=release,
        denominator_members=members,
        weighted_denominator=None,
    )
    product = compute_effective_n(
        fact=fact,
        query=query,
        weight_facts=(),
        authority_registry=AuthorityRegistry((query_auth,)),
        release_refs=(release,),
        authorized_weight_scope_ref=None,
    )
    assert product.typed_state == "NOT_APPLICABLE"
    assert product.sum_w is None
    assert product.sum_w2 is None
    assert product.effective_n is None
    assert fact.raw_denominator_support == 4


def test_absent_weight_authority_is_typed_not_authorized_without_default_weight():
    fx = _weighted_fixture("missing-auth")
    registry_without_weight_authority = AuthorityRegistry((fx["query_auth"],))
    product = compute_effective_n(
        fact=fx["fact"],
        query=fx["query"],
        weight_facts=fx["weights"],
        authority_registry=registry_without_weight_authority,
        release_refs=(fx["release"],),
        authorized_weight_scope_ref=fx["scope"],
    )
    assert product.typed_state == "NOT_AUTHORIZED"
    assert product.effective_n is None
    assert product.sum_w is None
    assert product.sum_w2 is None


def test_invalid_weight_state_never_leaks_partial_numeric_effective_n():
    fx = _weighted_fixture("invalid-weight")
    invalid = _weight(
        "invalid-weight-2",
        universe_ref=fx["universe"],
        respondent_ref=fx["members"][1],
        scope_ref=fx["scope"],
        source_ref=fx["source"],
        design_auth=fx["design_auth"],
        estimand_auth=fx["estimand_auth"],
        value=None,
        state="WEIGHT_INVALID",
    )
    weights = (fx["weights"][0], invalid)
    fact = _fact(
        "invalid-weight",
        query=fx["query"],
        query_auth=fx["query_auth"],
        universe_ref=fx["universe"],
        risk_ref=fx["risk"],
        condition_ref=fx["condition"],
        release_ref=fx["release"],
        denominator_members=fx["members"],
        weights=weights,
        weighted_denominator={"$exact_fraction": [1, 1]},
    )
    product = compute_effective_n(
        fact=fact,
        query=fx["query"],
        weight_facts=weights,
        authority_registry=fx["registry"],
        release_refs=(fx["release"],),
        authorized_weight_scope_ref=fx["scope"],
    )
    assert product.typed_state == "INVALID_WEIGHT"
    assert product.sum_w is None
    assert product.sum_w2 is None
    assert product.effective_n is None


def test_zero_or_degenerate_weights_return_typed_state_not_numeric_zero():
    fx = _weighted_fixture("zero-weight")
    weights = tuple(
        _weight(
            f"zero-weight-{i}",
            universe_ref=fx["universe"],
            respondent_ref=member,
            scope_ref=fx["scope"],
            source_ref=fx["source"],
            design_auth=fx["design_auth"],
            estimand_auth=fx["estimand_auth"],
            value="0",
        )
        for i, member in enumerate(fx["members"], start=1)
    )
    fact = _fact(
        "zero-weight",
        query=fx["query"],
        query_auth=fx["query_auth"],
        universe_ref=fx["universe"],
        risk_ref=fx["risk"],
        condition_ref=fx["condition"],
        release_ref=fx["release"],
        denominator_members=fx["members"],
        weights=weights,
        weighted_denominator={"$exact_fraction": [0, 1]},
    )
    product = compute_effective_n(
        fact=fact,
        query=fx["query"],
        weight_facts=weights,
        authority_registry=fx["registry"],
        release_refs=(fx["release"],),
        authorized_weight_scope_ref=fx["scope"],
    )
    assert product.typed_state == "DEGENERATE_WEIGHT_SUM"
    assert product.sum_w is None
    assert product.sum_w2 is None
    assert product.effective_n is None


def test_mismatched_weight_scope_fails_closed_without_reselecting_a_weight():
    fx = _weighted_fixture("scope-mismatch")
    product = compute_effective_n(
        fact=fx["fact"],
        query=fx["query"],
        weight_facts=fx["weights"],
        authority_registry=fx["registry"],
        release_refs=(fx["release"],),
        authorized_weight_scope_ref=_ref("WEIGHT_SCOPE", "different"),
    )
    assert product.typed_state == "SCOPE_MISMATCH"
    assert product.effective_n is None


def test_missing_explicit_weight_scope_does_not_infer_scope_or_estimand():
    fx = _weighted_fixture("no-scope")
    product = compute_effective_n(
        fact=fx["fact"],
        query=fx["query"],
        weight_facts=fx["weights"],
        authority_registry=fx["registry"],
        release_refs=(fx["release"],),
        authorized_weight_scope_ref=None,
    )
    assert product.typed_state == "NOT_AUTHORIZED"
    assert product.effective_n is None


def test_governed_weighted_query_without_exact_basis_cannot_infer_default_weight():
    fx = _weighted_fixture("no-basis")
    query = _query(
        "no-basis",
        universe_ref=fx["universe"],
        risk_ref=fx["risk"],
        condition_ref=fx["condition"],
        query_auth=fx["query_auth"],
        measure_kind="GOVERNED_WEIGHTED",
        weight_basis_id=None,
    )
    fact = _fact(
        "no-basis",
        query=query,
        query_auth=fx["query_auth"],
        universe_ref=fx["universe"],
        risk_ref=fx["risk"],
        condition_ref=fx["condition"],
        release_ref=fx["release"],
        denominator_members=fx["members"],
        weights=(),
        weighted_denominator=None,
    )
    with pytest.raises(EffectiveNError, match="weight_basis_id"):
        compute_effective_n(
            fact=fact,
            query=query,
            weight_facts=(),
            authority_registry=fx["registry"],
            release_refs=(fx["release"],),
            authorized_weight_scope_ref=fx["scope"],
        )


def test_design_and_estimand_authority_are_checked_as_distinct_bindings():
    fx = _weighted_fixture("authority-separation")
    denied_estimand = _auth("authority-separation-estimand-denied", state="DENY")
    weights = tuple(
        _weight(
            f"authority-separation-{i}",
            universe_ref=fx["universe"],
            respondent_ref=member,
            scope_ref=fx["scope"],
            source_ref=fx["source"],
            design_auth=fx["design_auth"],
            estimand_auth=denied_estimand,
            value=str(i),
        )
        for i, member in enumerate(fx["members"], start=1)
    )
    fact = _fact(
        "authority-separation",
        query=fx["query"],
        query_auth=fx["query_auth"],
        universe_ref=fx["universe"],
        risk_ref=fx["risk"],
        condition_ref=fx["condition"],
        release_ref=fx["release"],
        denominator_members=fx["members"],
        weights=weights,
        weighted_denominator={"$exact_fraction": [3, 1]},
    )
    registry = AuthorityRegistry((fx["query_auth"], fx["design_auth"], denied_estimand))
    product = compute_effective_n(
        fact=fact,
        query=fx["query"],
        weight_facts=weights,
        authority_registry=registry,
        release_refs=(fx["release"],),
        authorized_weight_scope_ref=fx["scope"],
    )
    assert product.typed_state == "NOT_AUTHORIZED"
    assert product.effective_n is None


def test_weight_set_must_reproduce_i03_weighted_denominator_and_provenance():
    fx = _weighted_fixture("i03-coupling")
    mismatched_fact = _fact(
        "i03-coupling",
        query=fx["query"],
        query_auth=fx["query_auth"],
        universe_ref=fx["universe"],
        risk_ref=fx["risk"],
        condition_ref=fx["condition"],
        release_ref=fx["release"],
        denominator_members=fx["members"],
        weights=fx["weights"],
        weighted_denominator={"$exact_fraction": [4, 1]},
    )
    product = compute_effective_n(
        fact=mismatched_fact,
        query=fx["query"],
        weight_facts=fx["weights"],
        authority_registry=fx["registry"],
        release_refs=(fx["release"],),
        authorized_weight_scope_ref=fx["scope"],
    )
    assert product.typed_state == "SCOPE_MISMATCH"
    assert product.effective_n is None
