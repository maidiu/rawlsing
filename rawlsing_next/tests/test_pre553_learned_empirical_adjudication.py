from __future__ import annotations

import inspect

import pytest

import rawlsing_next.pre553_learned_empirical_adjudication as m1
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    DiscoveryResultReceipt,
    EmpiricalFact,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.tests.test_pre553_empirical_query import _auth, _h, _ref
from rawlsing_next.tests.test_pre553_route_b_production import (
    _execute as execute_m01,
    _fixture as m01_fixture,
)


CLAIM_FAMILY = "SYNTHETIC_LEARNED_RELATION"
CLAIM_RULE = "SYNTHETIC_RULE_R1"


def _m1_authority(tag: str, *, state: str = "ALLOW") -> AuthoritySnapshot:
    base = _auth(
        f"m1-{tag}",
        "TARGET_USE_PERMISSION",
        families=("EmpiricalFact@1.0.0",),
    )
    if state == "ALLOW":
        return base
    fields = dict(base.semantic_fields)
    fields["decision_state"] = state
    return AuthoritySnapshot(
        typed_state=state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
        **fields,
    )


def _coverage_contract(*, allow_limited: bool = False):
    receipt_states = [
        "DISCOVERED_RESULT_SUPPORTED",
        "VALID_EMPTY",
        "INSUFFICIENT_SUPPORT",
        "NONCOMPARABLE",
    ]
    coverage_states = [
        "EVALUATED_SUPPORTED",
        "EVALUATED_VALID_EMPTY",
    ]
    if allow_limited:
        receipt_states.append("COVERAGE_LIMITED")
        coverage_states.append("COVERAGE_LIMITED")
    return {
        "allowed_coverage_claims": (
            "COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
        ),
        "allowed_receipt_states": tuple(receipt_states),
        "allowed_coverage_states": tuple(coverage_states),
    }


def _allowed_states():
    return {
        "DiscoveryResultReceipt@1.0.0": (
            "DISCOVERED_RESULT_SUPPORTED",
            "VALID_EMPTY",
            "INSUFFICIENT_SUPPORT",
            "NONCOMPARABLE",
            "COVERAGE_LIMITED",
            "UNEVALUATED",
        ),
        "DiscoveryAuthority@1.0.0": (
            "EXACT_BOUNDED_AUTHORIZED",
            "ADAPTIVE_EXPLORATORY_AUTHORIZED",
        ),
        "EmpiricalFact@1.0.0": (
            "SUPPORTED",
            "OBSERVED_ZERO",
            "ZERO_SUPPORT",
            "ZERO_OVERLAP",
            "LOW_SUPPORT",
            "NONCOMPARABLE",
            "NOT_APPLICABLE",
            "UNAVAILABLE",
            "UNRESOLVED",
            "VALID_EMPTY",
            "INTEGRITY_FAILURE",
        ),
        "EmpiricalQuerySpec@1.0.0": (
            "QUERY_AUTHORIZED_RESOLVABLE",
            "VALID_EMPTY_QUERY_FRONTIER",
        ),
        "EmpiricalPredicate@1.0.0": (
            "PREDICATE_RESOLVED_AUTHORIZED",
        ),
    }


def _binding(
    validator_authority: AuthoritySnapshot,
    *,
    claim_family: str = CLAIM_FAMILY,
    claim_rule: str = CLAIM_RULE,
    required_channels=(),
    required_relation_kinds=(),
    required_measure_authorities=(),
    allow_limited: bool = False,
    output_claims: bool = False,
    selection_purpose: str = "EXACT_PINNED_REPLAY",
    current_selection_authority: AuthoritySnapshot | None = None,
):
    closure = [validator_authority.authority_ref]
    current_ref = None
    if current_selection_authority is not None:
        current_ref = current_selection_authority.authority_ref
        closure.append(current_ref)
    return m1.M1FamilyRuleBinding(
        claim_family_id=claim_family,
        claim_rule_id=claim_rule,
        validator_authority_ref=validator_authority.authority_ref,
        selection_purpose=selection_purpose,
        current_selection_authority_ref=current_ref,
        applicability_scope={
            "source_universe_refs": "EXPLICIT_UNRESTRICTED",
            "risk_set_refs": "EXPLICIT_UNRESTRICTED",
            "measure_basis_refs": "EXPLICIT_UNRESTRICTED",
            "topology_scope_material": "EXPLICIT_UNRESTRICTED",
            "requested_scope": "EXPLICIT_UNRESTRICTED",
        },
        allowed_input_object_families_and_states=_allowed_states(),
        required_prerequisite_channels=tuple(required_channels),
        required_source_relation_kinds=tuple(required_relation_kinds),
        required_measure_weight_estimand_authorities=tuple(
            ref.authority_ref if isinstance(ref, AuthoritySnapshot) else ref
            for ref in required_measure_authorities
        ),
        required_coverage_strength=_coverage_contract(allow_limited=allow_limited),
        uncertainty_policy_ref=_ref("M1_UNCERTAINTY_POLICY", "synthetic"),
        output_semantic_contract={
            "truth_bearing_claim_emission": (
                "EXPLICITLY_AUTHORIZED" if output_claims else "PROHIBITED"
            )
        },
        semantic_ceiling=m1.M1_DEFAULT_SEMANTIC_CEILING,
        validator_algorithm_identity_if_required="SYNTHETIC_M1_VALIDATOR@1.0.0",
        validator_parameters_ref=_ref("M1_VALIDATOR_PARAMETERS", "synthetic"),
        replay_contract_ref=_ref("M1_REPLAY_CONTRACT", "synthetic"),
        authority_closure_refs=tuple(closure),
    )


def _validator(
    outcome: str = "RULE_SATISFIED",
    *,
    semantic_claim_ref: ExactRef | None = None,
    relation_ref: ExactRef | None = None,
    polarity: str = "NONE",
    effects=None,
    reason: str = "SYNTHETIC_RULE_DECISION",
):
    def run(context: m1.M1ValidatorContext) -> m1.FamilyValidationResult:
        binding = context.family_rule_binding
        return m1.FamilyValidationResult(
            claim_family_id=binding.claim_family_id,
            claim_rule_id=binding.claim_rule_id,
            family_rule_binding_ref=binding.ref,
            validator_authority_ref=binding.validator_authority_ref,
            validator_algorithm_identity=binding.validator_algorithm_identity_if_required,
            adjudication_outcome=outcome,
            reason_code=reason,
            relation_proposition_identity_ref=relation_ref,
            semantic_claim_identity_ref=semantic_claim_ref,
            semantic_assertion_polarity_or_state=polarity,
            semantic_ceiling=binding.semantic_ceiling,
            determinant_material={
                "synthetic_rule": binding.claim_rule_id,
                "evidence_state_vector": context.evidence_context[
                    "conserved_empirical_states"
                ],
            },
            explanation_material={
                "why": reason,
                "substantive_rule_owned_by_fixture": True,
            },
            effects=effects if effects is not None else dict(m1._FALSE_EFFECTS),
        )

    return run


def _registry(binding, validator=None):
    if validator is None:
        validator = _validator()
    return m1.M1ValidatorRegistry(
        (m1.FamilyValidatorRegistration.from_binding(binding, validator),)
    )


def _bundle(
    *,
    valid_empty: bool = False,
    validator_authorities=(),
    prerequisite_channels=(),
    selected_receipts=None,
    fact_catalog=None,
    query_catalog=None,
    predicate_catalog=None,
    authority_catalog=None,
):
    fx = m01_fixture(valid_empty=valid_empty)
    result = execute_m01(fx)
    receipts = (
        tuple(selected_receipts)
        if selected_receipts is not None
        else result.i05_result.receipts
    )
    facts = (
        tuple(fact_catalog)
        if fact_catalog is not None
        else result.object_graph.empirical_facts
    )
    queries = (
        tuple(query_catalog)
        if query_catalog is not None
        else result.object_graph.executed_queries
    )
    predicates = (
        tuple(predicate_catalog)
        if predicate_catalog is not None
        else result.object_graph.executed_predicates
    )
    authorities = (
        tuple(authority_catalog)
        if authority_catalog is not None
        else tuple(result.object_graph.authority_snapshots)
        + tuple(validator_authorities)
    )
    bundle = m1.build_m1_adjudication_input_bundle(
        requested_claim_family_id=CLAIM_FAMILY,
        requested_claim_rule_id=CLAIM_RULE,
        selected_discovery_receipts=receipts,
        discovery_authority_catalog=result.object_graph.discovery_authorities,
        empirical_fact_catalog=facts,
        empirical_query_catalog=queries,
        empirical_predicate_catalog=predicates,
        authority_snapshots=authorities,
        requested_scope={"fixture": "M01_SYNTHETIC_EXACT_GRAPH"},
        prerequisite_channels=tuple(prerequisite_channels),
        additional_dependency_refs=(result.c11_release.release_ref,),
    )
    return fx, result, bundle


def _clone_fact(fact: EmpiricalFact, *, state: str, numerator: int, denominator: int, tag: str):
    fields = dict(fact.semantic_fields)
    fields["raw_numerator_support"] = numerator
    fields["raw_denominator_support"] = denominator
    fields["raw_resolved_target_support"] = numerator
    return EmpiricalFact(
        typed_state=state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=_ref("M1_FACT_REPLAY", tag),
        **fields,
    )


def _receipt_with_fact(
    receipt: DiscoveryResultReceipt,
    old_fact: EmpiricalFact,
    new_fact: EmpiricalFact,
    *,
    typed_state: str | None = None,
    coverage_state: str | None = None,
    tag: str,
):
    fields = dict(receipt.semantic_fields)

    def replace_refs(values):
        return tuple(
            new_fact.ref if ExactRef(**dict(ref)) == old_fact.ref else ExactRef(**dict(ref))
            for ref in values
        )

    fields["empirical_fact_refs"] = replace_refs(receipt.empirical_fact_refs)
    fields["validation_fact_refs"] = replace_refs(receipt.validation_fact_refs)
    if typed_state is not None:
        fields["coverage_state"] = coverage_state or fields["coverage_state"]
    replay = _ref("M1_DISCOVERY_REPLAY", tag)
    fields["replay_ref"] = replay

    dependencies = [
        new_fact.ref if ref == old_fact.ref else ref
        for ref in receipt.dependency_refs
    ]

    return DiscoveryResultReceipt(
        typed_state=typed_state or receipt.typed_state,
        authority_snapshot_refs=receipt.authority_snapshot_refs,
        dependency_refs=tuple(dependencies),
        producer_replay_locator_or_reference_root=replay,
        **fields,
    )


def _replace_bundle_receipt_and_fact(
    result,
    base_bundle,
    old_fact,
    new_fact,
    new_receipt,
    extra_authorities=(),
):
    facts = tuple(
        new_fact if fact.ref == old_fact.ref else fact
        for fact in result.object_graph.empirical_facts
    )
    receipts = tuple(
        new_receipt if receipt.ref == result.i05_result.receipts[0].ref else receipt
        for receipt in result.i05_result.receipts
    )
    return m1.build_m1_adjudication_input_bundle(
        requested_claim_family_id=base_bundle.requested_claim_family_id,
        requested_claim_rule_id=base_bundle.requested_claim_rule_id,
        selected_discovery_receipts=receipts,
        discovery_authority_catalog=result.object_graph.discovery_authorities,
        empirical_fact_catalog=facts,
        empirical_query_catalog=result.object_graph.executed_queries,
        empirical_predicate_catalog=result.object_graph.executed_predicates,
        authority_snapshots=tuple(base_bundle.authority_snapshots) + tuple(extra_authorities),
        requested_scope=base_bundle.requested_scope,
        prerequisite_channels=base_bundle.prerequisite_channels,
        additional_dependency_refs=base_bundle.additional_dependency_refs,
    )


def _states(disposition):
    return {
        row["state"] if isinstance(row, dict) else row["state"]
        for row in disposition.conserved_empirical_states
    }


def test_m01_exact_graph_supplies_m1_and_exact_rule_binding_dispatches():
    validator_auth = _m1_authority("basic")
    _, result, bundle = _bundle(validator_authorities=(validator_auth,))
    binding = _binding(validator_auth)
    disposition = m1.adjudicate_learned_empirical(
        bundle, binding, validator_registry=_registry(binding)
    )
    assert disposition.adjudication_outcome == "RULE_SATISFIED"
    assert disposition.rule_outcome == "RULE_SATISFIED"
    assert disposition.family_rule_binding_ref == binding.ref
    assert tuple(disposition.discovery_result_receipt_refs) == tuple(
        receipt.ref for receipt in result.i05_result.receipts
    )
    assert m1.verify_m1_disposition_replay(disposition) == disposition.replay_ref.content_hash


def test_missing_rule_binding_blocks_even_supported_replay_complete_evidence():
    validator_auth = _m1_authority("missing-binding")
    _, _, bundle = _bundle(validator_authorities=(validator_auth,))
    disposition = m1.adjudicate_learned_empirical(
        bundle, None, validator_registry=m1.M1ValidatorRegistry()
    )
    assert disposition.status_token == (
        "BLOCKED__MISSING_FAMILY_VALIDATION_RULE_AUTHORITY"
    )
    assert isinstance(disposition.family_rule_binding_ref, TypedAbsence)
    assert isinstance(disposition.semantic_claim_identity_ref, TypedAbsence)


def test_no_latest_default_or_nearby_validator_fallback():
    requested_auth = _m1_authority("requested")
    other_auth = _m1_authority("newer-looking")
    _, _, bundle = _bundle(
        validator_authorities=(requested_auth, other_auth)
    )
    requested = _binding(requested_auth)
    other = _binding(other_auth)
    registry = _registry(other)
    disposition = m1.adjudicate_learned_empirical(
        bundle, requested, validator_registry=registry
    )
    assert disposition.adjudication_outcome == "BLOCKED"
    assert "RULE_BINDING_OR_PREREQUISITE_BLOCKED" in disposition.status_token

    with pytest.raises(m1.M1BlockedError):
        m1.M1FamilyRuleBinding(
            **{
                **{
                    field: getattr(requested, field)
                    for field in requested.__dataclass_fields__
                },
                "validator_authority_ref": AuthorityRef(
                    "LATEST",
                    "1",
                    _h("forbidden-latest-selector"),
                ),
                "authority_closure_refs": (
                    AuthorityRef("LATEST", "1", _h("forbidden-latest-selector")),
                ),
            }
        )


def test_wrong_family_rule_or_validator_authority_binding_fails_closed():
    validator_auth = _m1_authority("wrong-family")
    _, _, bundle = _bundle(validator_authorities=(validator_auth,))
    wrong_family = _binding(validator_auth, claim_family="OTHER_FAMILY")
    disposition = m1.adjudicate_learned_empirical(
        bundle, wrong_family, validator_registry=_registry(wrong_family)
    )
    assert disposition.adjudication_outcome == "BLOCKED"

    binding = _binding(validator_auth)
    wrong_registration = m1.FamilyValidatorRegistration(
        claim_family_id=binding.claim_family_id,
        claim_rule_id=binding.claim_rule_id,
        validator_authority_ref=binding.validator_authority_ref,
        validator_algorithm_identity=binding.validator_algorithm_identity_if_required,
        validator_parameters_ref=binding.validator_parameters_ref,
        validator_contract_fingerprint=_h("wrong-contract-fingerprint"),
        validator=_validator(),
    )
    disposition = m1.adjudicate_learned_empirical(
        bundle,
        binding,
        validator_registry=m1.M1ValidatorRegistry((wrong_registration,)),
    )
    assert disposition.adjudication_outcome == "BLOCKED"


def test_missing_object_authority_closure_blocks():
    validator_auth = _m1_authority("closure")
    fx, result, bundle = _bundle(validator_authorities=(validator_auth,))
    authorities = tuple(
        auth
        for auth in bundle.authority_snapshots
        if auth.authority_ref != fx["dauth"].authority_ref
    )
    broken = m1.M1AdjudicationInputBundle(
        requested_claim_family_id=bundle.requested_claim_family_id,
        requested_claim_rule_id=bundle.requested_claim_rule_id,
        discovery_receipts=bundle.discovery_receipts,
        discovery_authorities=bundle.discovery_authorities,
        empirical_facts=bundle.empirical_facts,
        empirical_queries=bundle.empirical_queries,
        empirical_predicates=bundle.empirical_predicates,
        authority_snapshots=authorities,
        evaluated_frontier_refs=bundle.evaluated_frontier_refs,
        discovery_replay_refs=bundle.discovery_replay_refs,
        requested_scope=bundle.requested_scope,
        prerequisite_channels=bundle.prerequisite_channels,
        additional_dependency_refs=bundle.additional_dependency_refs,
    )
    binding = _binding(validator_auth)
    disposition = m1.adjudicate_learned_empirical(
        broken, binding, validator_registry=_registry(binding)
    )
    assert disposition.status_token == "BLOCKED__MISSING_AUTHORITY_CLOSURE"


@pytest.mark.parametrize("kind", ["fact", "query", "predicate", "frontier", "replay"])
def test_ref_or_replay_substitution_is_integrity_failure(kind):
    validator_auth = _m1_authority(f"sub-{kind}")
    _, _, bundle = _bundle(validator_authorities=(validator_auth,))
    kwargs = dict(
        requested_claim_family_id=bundle.requested_claim_family_id,
        requested_claim_rule_id=bundle.requested_claim_rule_id,
        discovery_receipts=bundle.discovery_receipts,
        discovery_authorities=bundle.discovery_authorities,
        empirical_facts=bundle.empirical_facts,
        empirical_queries=bundle.empirical_queries,
        empirical_predicates=bundle.empirical_predicates,
        authority_snapshots=bundle.authority_snapshots,
        evaluated_frontier_refs=bundle.evaluated_frontier_refs,
        discovery_replay_refs=bundle.discovery_replay_refs,
        requested_scope=bundle.requested_scope,
        prerequisite_channels=bundle.prerequisite_channels,
        additional_dependency_refs=bundle.additional_dependency_refs,
    )
    if kind == "fact":
        kwargs["empirical_facts"] = bundle.empirical_facts[1:]
    elif kind == "query":
        kwargs["empirical_queries"] = bundle.empirical_queries[1:]
    elif kind == "predicate":
        kwargs["empirical_predicates"] = bundle.empirical_predicates[1:]
    elif kind == "frontier":
        kwargs["evaluated_frontier_refs"] = (_ref("FRONTIER", "substituted"),)
    else:
        kwargs["discovery_replay_refs"] = (_ref("REPLAY", "substituted"),)
    broken = m1.M1AdjudicationInputBundle(**kwargs)
    binding = _binding(validator_auth)
    disposition = m1.adjudicate_learned_empirical(
        broken, binding, validator_registry=_registry(binding)
    )
    assert disposition.adjudication_outcome == "INTEGRITY_FAILURE"


@pytest.mark.parametrize("channel_id,channel_kind", [
    ("comparability", "COMPARABILITY"),
    ("composition", "COMPOSITION"),
])
def test_required_comparability_or_composition_premise_absent_blocks(
    channel_id, channel_kind
):
    validator_auth = _m1_authority(channel_id)
    _, _, bundle = _bundle(validator_authorities=(validator_auth,))
    binding = _binding(validator_auth, required_channels=(channel_id,))
    disposition = m1.adjudicate_learned_empirical(
        bundle, binding, validator_registry=_registry(binding)
    )
    assert disposition.adjudication_outcome == "BLOCKED"
    assert isinstance(disposition.semantic_claim_identity_ref, TypedAbsence)


def test_coverage_limited_cannot_satisfy_complete_rule_unless_explicitly_permitted():
    validator_auth = _m1_authority("coverage")
    _, result, base_bundle = _bundle(validator_authorities=(validator_auth,))
    receipt = result.i05_result.receipts[0]
    fact = next(
        f for f in result.object_graph.empirical_facts
        if f.ref in tuple(ExactRef(**dict(x)) for x in receipt.empirical_fact_refs)
    )
    limited_receipt = _receipt_with_fact(
        receipt,
        fact,
        fact,
        typed_state="COVERAGE_LIMITED",
        coverage_state="COVERAGE_LIMITED",
        tag="coverage-limited",
    )
    limited_bundle = m1.build_m1_adjudication_input_bundle(
        requested_claim_family_id=CLAIM_FAMILY,
        requested_claim_rule_id=CLAIM_RULE,
        selected_discovery_receipts=(limited_receipt,),
        discovery_authority_catalog=result.object_graph.discovery_authorities,
        empirical_fact_catalog=result.object_graph.empirical_facts,
        empirical_query_catalog=result.object_graph.executed_queries,
        empirical_predicate_catalog=result.object_graph.executed_predicates,
        authority_snapshots=base_bundle.authority_snapshots,
        requested_scope=base_bundle.requested_scope,
    )

    strict = _binding(validator_auth, allow_limited=False)
    blocked = m1.adjudicate_learned_empirical(
        limited_bundle, strict, validator_registry=_registry(strict)
    )
    assert blocked.adjudication_outcome == "BLOCKED"

    permissive = _binding(validator_auth, allow_limited=True)
    satisfied = m1.adjudicate_learned_empirical(
        limited_bundle, permissive, validator_registry=_registry(permissive)
    )
    assert satisfied.adjudication_outcome == "RULE_SATISFIED"
    assert any(
        row["receipt_state"] == "COVERAGE_LIMITED"
        for row in satisfied.coverage_states
    )


def test_valid_empty_observed_zero_zero_support_are_distinct_and_conserved():
    validator_auth = _m1_authority("negative-vector")

    _, _, valid_empty_bundle = _bundle(
        valid_empty=True, validator_authorities=(validator_auth,)
    )
    binding = _binding(validator_auth)
    valid_empty = m1.adjudicate_learned_empirical(
        valid_empty_bundle,
        binding,
        validator_registry=_registry(binding, _validator(outcome="ABSTAINED")),
    )
    assert "VALID_EMPTY" in _states(valid_empty)

    _, result, base = _bundle(validator_authorities=(validator_auth,))
    receipt = result.i05_result.receipts[0]
    old_fact_ref = ExactRef(**dict(receipt.empirical_fact_refs[0]))
    old_fact = next(f for f in result.object_graph.empirical_facts if f.ref == old_fact_ref)

    observed_fact = _clone_fact(
        old_fact, state="OBSERVED_ZERO", numerator=0, denominator=2, tag="observed-zero"
    )
    observed_receipt = _receipt_with_fact(
        receipt, old_fact, observed_fact, tag="observed-zero-receipt"
    )
    observed_bundle = _replace_bundle_receipt_and_fact(
        result, base, old_fact, observed_fact, observed_receipt
    )
    observed = m1.adjudicate_learned_empirical(
        observed_bundle, binding, validator_registry=_registry(binding)
    )

    zero_fact = _clone_fact(
        old_fact, state="ZERO_SUPPORT", numerator=0, denominator=0, tag="zero-support"
    )
    zero_receipt = _receipt_with_fact(
        receipt, old_fact, zero_fact, tag="zero-support-receipt"
    )
    zero_bundle = _replace_bundle_receipt_and_fact(
        result, base, old_fact, zero_fact, zero_receipt
    )
    zero = m1.adjudicate_learned_empirical(
        zero_bundle,
        binding,
        validator_registry=_registry(binding, _validator(outcome="ABSTAINED")),
    )

    assert "OBSERVED_ZERO" in _states(observed)
    assert "ZERO_SUPPORT" in _states(zero)
    assert "VALID_EMPTY" in _states(valid_empty)
    assert observed.ref != zero.ref != valid_empty.ref


def test_noncomparable_and_integrity_failure_states_are_preserved_not_laundered():
    validator_auth = _m1_authority("state-conservation")
    _, result, base = _bundle(validator_authorities=(validator_auth,))
    binding = _binding(validator_auth)
    receipt = result.i05_result.receipts[0]
    old_ref = ExactRef(**dict(receipt.empirical_fact_refs[0]))
    old_fact = next(f for f in result.object_graph.empirical_facts if f.ref == old_ref)

    noncomp_fact = _clone_fact(
        old_fact,
        state="NONCOMPARABLE",
        numerator=old_fact.raw_numerator_support,
        denominator=old_fact.raw_denominator_support,
        tag="noncomparable",
    )
    noncomp_receipt = _receipt_with_fact(
        receipt, old_fact, noncomp_fact, tag="noncomparable-receipt"
    )
    noncomp_bundle = _replace_bundle_receipt_and_fact(
        result, base, old_fact, noncomp_fact, noncomp_receipt
    )
    noncomp = m1.adjudicate_learned_empirical(
        noncomp_bundle,
        binding,
        validator_registry=_registry(binding, _validator(outcome="ABSTAINED")),
    )
    assert noncomp.adjudication_outcome == "ABSTAINED"
    assert "NONCOMPARABLE" in _states(noncomp)

    broken_fact = _clone_fact(
        old_fact, state="INTEGRITY_FAILURE", numerator=0, denominator=0, tag="integrity"
    )
    broken_receipt = _receipt_with_fact(
        receipt, old_fact, broken_fact, tag="integrity-receipt"
    )
    broken_bundle = _replace_bundle_receipt_and_fact(
        result, base, old_fact, broken_fact, broken_receipt
    )
    broken = m1.adjudicate_learned_empirical(
        broken_bundle, binding, validator_registry=_registry(binding)
    )
    assert broken.adjudication_outcome == "INTEGRITY_FAILURE"
    assert "INTEGRITY_FAILURE" in _states(broken)


@pytest.mark.parametrize(
    "state,expected",
    [
        ("BLOCKED", "BLOCKED"),
        ("UNKNOWN", "UNRESOLVED"),
        ("UNRESOLVED", "UNRESOLVED"),
    ],
)
def test_blocked_unknown_unresolved_prerequisite_states_remain_typed(state, expected):
    validator_auth = _m1_authority(f"premise-{state}")
    channel = m1.M1PrerequisiteChannel(
        channel_id="required-premise",
        channel_kind="COMPARABILITY",
        state=state,
        detail={"fixture": state},
    )
    _, _, bundle = _bundle(
        validator_authorities=(validator_auth,),
        prerequisite_channels=(channel,),
    )
    binding = _binding(
        validator_auth, required_channels=("required-premise",)
    )
    disposition = m1.adjudicate_learned_empirical(
        bundle, binding, validator_registry=_registry(binding)
    )
    assert disposition.adjudication_outcome == expected
    assert disposition.required_prerequisite_channel_states["required-premise"] == state


def test_satisfied_never_promotes_to_release_current_structure_causal_or_v3_truth():
    validator_auth = _m1_authority("anti-promotion")
    _, _, bundle = _bundle(validator_authorities=(validator_auth,))
    binding = _binding(validator_auth)
    disposition = m1.adjudicate_learned_empirical(
        bundle, binding, validator_registry=_registry(binding)
    )
    assert disposition.adjudication_outcome == "RULE_SATISFIED"
    assert dict(disposition.effects) == dict(m1._FALSE_EFFECTS)
    assert isinstance(disposition.semantic_claim_identity_ref, TypedAbsence)


def test_rule_not_satisfied_does_not_mint_negative_semantic_truth():
    validator_auth = _m1_authority("not-satisfied")
    _, _, bundle = _bundle(validator_authorities=(validator_auth,))
    binding = _binding(validator_auth)
    disposition = m1.adjudicate_learned_empirical(
        bundle,
        binding,
        validator_registry=_registry(
            binding, _validator(outcome="RULE_NOT_SATISFIED", reason="NO_MATCH")
        ),
    )
    assert disposition.adjudication_outcome == "RULE_NOT_SATISFIED"
    assert disposition.rule_outcome == "RULE_NOT_SATISFIED"
    assert isinstance(disposition.semantic_claim_identity_ref, TypedAbsence)
    assert disposition.semantic_assertion_polarity_or_state == "NONE"


def test_identical_input_and_rule_replay_to_identical_disposition_identity():
    validator_auth = _m1_authority("determinism")
    _, _, bundle = _bundle(validator_authorities=(validator_auth,))
    binding = _binding(validator_auth)
    registry = _registry(binding)
    a = m1.adjudicate_learned_empirical(bundle, binding, validator_registry=registry)
    b = m1.adjudicate_learned_empirical(bundle, binding, validator_registry=registry)
    assert a.ref == b.ref
    assert a.replay_ref == b.replay_ref
    assert a.determinant_manifest_ref == b.determinant_manifest_ref
    assert a.explanation_ref == b.explanation_ref


def test_validator_authority_change_changes_disposition_not_same_p1_claim_identity():
    auth_a = _m1_authority("authority-a")
    auth_b = _m1_authority("authority-b")
    _, _, bundle = _bundle(validator_authorities=(auth_a, auth_b))
    claim_ref = _ref("SEMANTIC_CLAIM_IDENTITY", "same-p1-claim")
    proposition_ref = _ref("RELATION_PROPOSITION_IDENTITY", "same-proposition")
    binding_a = _binding(auth_a, output_claims=True)
    binding_b = _binding(auth_b, output_claims=True)
    validator = _validator(
        semantic_claim_ref=claim_ref,
        relation_ref=proposition_ref,
        polarity="ASSERTED",
    )
    a = m1.adjudicate_learned_empirical(
        bundle, binding_a, validator_registry=_registry(binding_a, validator)
    )
    b = m1.adjudicate_learned_empirical(
        bundle, binding_b, validator_registry=_registry(binding_b, validator)
    )
    assert a.semantic_claim_identity_ref == b.semantic_claim_identity_ref == claim_ref
    assert a.ref != b.ref
    assert a.validator_authority_ref != b.validator_authority_ref


def test_current_governed_use_requires_explicit_current_selection_authority():
    validator_auth = _m1_authority("current-validator")
    selection_auth = _m1_authority("current-selection")
    _, _, bundle_without = _bundle(validator_authorities=(validator_auth,))
    binding = _binding(
        validator_auth,
        selection_purpose="CURRENT_GOVERNED_USE",
        current_selection_authority=selection_auth,
    )
    blocked = m1.adjudicate_learned_empirical(
        bundle_without, binding, validator_registry=_registry(binding)
    )
    assert blocked.adjudication_outcome == "BLOCKED"

    _, _, bundle_with = _bundle(
        validator_authorities=(validator_auth, selection_auth)
    )
    allowed = m1.adjudicate_learned_empirical(
        bundle_with, binding, validator_registry=_registry(binding)
    )
    assert allowed.adjudication_outcome == "RULE_SATISFIED"
    assert allowed.rule_selection_authority_ref == selection_auth.authority_ref


def test_required_relation_and_measure_authority_channels_are_exact_not_neighboring():
    validator_auth = _m1_authority("premise-exact")
    measure_auth = _m1_authority("measure-premise")
    channel = m1.M1PrerequisiteChannel(
        channel_id="exact-premise",
        channel_kind="COMPOSITION",
        state="SATISFIED",
        authority_refs=(measure_auth.authority_ref,),
        relation_kinds=("EXACT_POOLING_RELATION",),
    )
    _, _, bundle = _bundle(
        validator_authorities=(validator_auth, measure_auth),
        prerequisite_channels=(channel,),
    )
    binding = _binding(
        validator_auth,
        required_channels=("exact-premise",),
        required_relation_kinds=("EXACT_POOLING_RELATION",),
        required_measure_authorities=(measure_auth,),
    )
    allowed = m1.adjudicate_learned_empirical(
        bundle, binding, validator_registry=_registry(binding)
    )
    assert allowed.adjudication_outcome == "RULE_SATISFIED"

    wrong = _binding(
        validator_auth,
        required_channels=("exact-premise",),
        required_relation_kinds=("OTHER_RELATION",),
        required_measure_authorities=(measure_auth,),
    )
    blocked = m1.adjudicate_learned_empirical(
        bundle, wrong, validator_registry=_registry(wrong)
    )
    assert blocked.adjudication_outcome == "BLOCKED"


def test_denied_validator_authority_blocks_and_state_is_conserved():
    denied = _m1_authority("denied", state="DENY")
    _, _, bundle = _bundle(validator_authorities=(denied,))
    binding = _binding(denied)
    disposition = m1.adjudicate_learned_empirical(
        bundle, binding, validator_registry=_registry(binding)
    )
    assert disposition.adjudication_outcome == "BLOCKED"
    assert any(
        row["state"] == "DENY" for row in disposition.conserved_authority_states
    )


def test_validator_side_effect_or_semantic_ceiling_breach_is_integrity_failure():
    validator_auth = _m1_authority("side-effect")
    _, _, bundle = _bundle(validator_authorities=(validator_auth,))
    binding = _binding(validator_auth)
    bad_effects = dict(m1._FALSE_EFFECTS)
    bad_effects["structural_admission_effect"] = True
    disposition = m1.adjudicate_learned_empirical(
        bundle,
        binding,
        validator_registry=_registry(
            binding, _validator(effects=bad_effects)
        ),
    )
    assert disposition.adjudication_outcome == "INTEGRITY_FAILURE"
    assert dict(disposition.effects) == dict(m1._FALSE_EFFECTS)


def test_no_m2_b5_field_forge_or_historical_candidate_import_surface():
    source = inspect.getsource(m1).lower()
    imports = "\n".join(
        line for line in source.splitlines()
        if line.startswith("from ") or line.startswith("import ")
    )
    forbidden = (
        "pre553_route_b_production",
        "fiabc",
        "astra",
        "candidate_a",
        "candidate_b",
        "candidate_c",
        "pre553_structural_admission",
        "field_forge",
        "learned_product_release",
        "learned_product_lifecycle",
        "v3",
    )
    assert all(token not in imports for token in forbidden)
