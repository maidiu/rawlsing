from __future__ import annotations

from dataclasses import replace
import inspect

import pytest

import rawlsing_next.pre553_learned_empirical_adjudication as m1
import rawlsing_next.pre553_learned_world_composition as i4
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import (
    LearnedProductLifecycleError,
    LearnedProductLifecycleExecutor,
    LearnedProductLifecycleSubject,
)
from rawlsing_next.pre553_learned_product_release import (
    M2Repository,
    publish_binding,
    register_representation,
)
from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import (
    _binding,
    _bundle,
    _clone_fact,
    _m1_authority,
    _receipt_with_fact,
    _registry,
    _replace_bundle_receipt_and_fact,
    _validator,
)
from rawlsing_next.tests.test_pre553_route_b_production import (
    _execute as execute_m01,
    _fixture as m01_fixture,
)


def _ref(kind: str, tag: str) -> ExactRef:
    digest = semantic_hash({"kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:test:i4:{kind.lower()}:{tag}:sha256:{digest}", digest)


def _contract(
    *,
    route: str = "M1_M2_B5",
    binding: m1.M1FamilyRuleBinding | None = None,
    actions: tuple[str, ...] = (),
    tag: str = "base",
    **overrides,
) -> i4.LearnedWorldProductContractBinding:
    data = dict(
        route=route,
        product_family_ref=_ref("ProductFamily", f"{tag}-family"),
        producer_owner_ref=_ref("ProducerOwner", "m1-owner"),
        producer_contract_ref=i4.M1_DISPOSITION_PRODUCER_CONTRACT_REF,
        release_subject_kind="TYPED_DISPOSITION",
        selection_scope_ref=_ref("SelectionScope", f"{tag}-scope"),
        producer_permission_ceiling_ref=_ref("PermissionCeiling", f"{tag}-ceiling"),
        consumer_product_purpose_ref=_ref("ConsumerPurpose", f"{tag}-purpose"),
        m1_family_rule_binding_ref=None if binding is None else binding.ref,
        lifecycle_actions=actions,
        registration_event_authority_ref=(
            _ref("LifecycleAuthority", f"{tag}-register-auth")
            if "REGISTER" in actions else None
        ),
        registration_event_rule_ref=(
            _ref("LifecycleRule", f"{tag}-register-rule")
            if "REGISTER" in actions else None
        ),
        publication_event_authority_ref=(
            _ref("LifecycleAuthority", f"{tag}-publish-auth")
            if "PUBLISH" in actions else None
        ),
        publication_event_rule_ref=(
            _ref("LifecycleRule", f"{tag}-publish-rule")
            if "PUBLISH" in actions else None
        ),
        selection_purpose_ref=(
            _ref("SelectionPurpose", f"{tag}-serve")
            if "SELECT_CURRENT" in actions else None
        ),
        selection_event_authority_ref=(
            _ref("LifecycleAuthority", f"{tag}-select-auth")
            if "SELECT_CURRENT" in actions else None
        ),
        selection_event_rule_ref=(
            _ref("LifecycleRule", f"{tag}-select-rule")
            if "SELECT_CURRENT" in actions else None
        ),
        selection_attestation_ref=(
            _ref("SelectionAttestation", f"{tag}-select-attest")
            if "SELECT_CURRENT" in actions else None
        ),
    )
    data.update(overrides)
    return i4.LearnedWorldProductContractBinding(**data)


def _disposition(
    tag: str,
    *,
    outcome: str = "RULE_SATISFIED",
    valid_empty: bool = False,
    channel_state: str | None = None,
):
    validator_auth = _m1_authority(f"i4-{tag}")
    channels = ()
    required_channels = ()
    if channel_state is not None:
        channel = m1.M1PrerequisiteChannel(
            channel_id="i4-required-premise",
            channel_kind="COMPARABILITY",
            state=channel_state,
            detail={"fixture": tag},
        )
        channels = (channel,)
        required_channels = ("i4-required-premise",)
    _, _, bundle = _bundle(
        valid_empty=valid_empty,
        validator_authorities=(validator_auth,),
        prerequisite_channels=channels,
    )
    binding = _binding(
        validator_auth,
        required_channels=required_channels,
    )
    validator = _validator(outcome=outcome)
    disposition = m1.adjudicate_learned_empirical(
        bundle,
        binding,
        validator_registry=_registry(binding, validator),
    )
    return disposition, binding, validator_auth


def _compose_disposition(
    disposition,
    *,
    contract=None,
    executor=None,
    repo=None,
):
    contract = contract or _contract()
    executor = executor or LearnedProductLifecycleExecutor()
    repo = repo or M2Repository()
    result = i4.compose_learned_world(
        contract,
        m2_repository=repo,
        lifecycle_executor=executor,
        m1_disposition=disposition,
    )
    return result, repo, executor


def _state_names(receipt):
    rows = receipt.conserved_state_material.get("conserved_empirical_states", ())
    return {
        row["state"] if isinstance(row, dict) else row["state"]
        for row in rows
    }


def test_t01_full_synthetic_m01_m1_m2_b5_composition_succeeds():
    auth = _m1_authority("i4-full")
    fx = m01_fixture()
    m01_result = execute_m01(fx)
    binding = _binding(auth)
    contract = _contract(
        route="M01_M1_M2_B5",
        binding=binding,
        actions=("REGISTER", "PUBLISH", "SELECT_CURRENT"),
        tag="full",
    )
    repo = M2Repository()
    executor = LearnedProductLifecycleExecutor()
    result = i4.compose_learned_world(
        contract,
        m2_repository=repo,
        lifecycle_executor=executor,
        m01_result=m01_result,
        selected_discovery_receipt_refs=tuple(
            receipt.ref for receipt in m01_result.i05_result.receipts
        ),
        requested_scope={"fixture": "I4_FULL_SYNTHETIC"},
        m1_family_rule_binding=binding,
        validator_registry=_registry(binding),
        m1_authority_snapshots=(auth,),
    )
    assert result.receipt.terminal_state == "RULE_SATISFIED"
    assert result.receipt.m01_execution_receipt_ref is not None
    assert result.receipt.m01_object_graph_ref is not None
    assert result.receipt.side_effects["b5_registration_effect"] is True
    assert result.receipt.side_effects["b5_publication_effect"] is True
    assert result.receipt.side_effects["b5_current_selection_effect"] is True
    assert result.b5_replay_receipt is not None
    assert result.b5_replay_receipt.replay_state == "REPLAY_VERIFIED"


def test_t02_m01_graph_cannot_self_select_m1_rule():
    m01_result = execute_m01(m01_fixture())
    contract = _contract(route="M01_M1_M2_B5", tag="no-rule")
    result = i4.compose_learned_world(
        contract,
        m2_repository=M2Repository(),
        lifecycle_executor=LearnedProductLifecycleExecutor(),
        m01_result=m01_result,
        selected_discovery_receipt_refs=tuple(
            receipt.ref for receipt in m01_result.i05_result.receipts
        ),
        requested_scope={"fixture": "NO_RULE"},
        validator_registry=m1.M1ValidatorRegistry(),
    )
    assert result.receipt.terminal_state == "BLOCKED"
    assert result.m1_disposition is None
    assert result.receipt.m2_release_ref is None


def test_t03_missing_product_family_fails_closed():
    disposition, _, _ = _disposition("missing-family")
    contract = _contract(product_family_ref=None)
    result, _, _ = _compose_disposition(disposition, contract=contract)
    assert result.receipt.terminal_state == "BLOCKED"
    assert result.receipt.m2_release_ref is None


def test_t04_missing_selection_scope_fails_closed_for_b5_path():
    disposition, _, _ = _disposition("missing-scope")
    result, _, _ = _compose_disposition(
        disposition,
        contract=_contract(selection_scope_ref=None),
    )
    assert result.receipt.terminal_state == "BLOCKED"


def test_t05_missing_permission_ceiling_fails_closed():
    disposition, _, _ = _disposition("missing-ceiling")
    result, _, _ = _compose_disposition(
        disposition,
        contract=_contract(producer_permission_ceiling_ref=None),
    )
    assert result.receipt.terminal_state == "BLOCKED"


def test_t06_m1_disposition_ref_is_exact_m2_subject_ref():
    disposition, _, _ = _disposition("subject-ref")
    result, _, _ = _compose_disposition(disposition)
    assert result.m2_artifacts.subject.ref == disposition.ref
    assert result.receipt.m1_disposition_ref == result.receipt.m2_subject_ref


def test_t07_m1_typed_state_is_exact_m2_subject_state():
    disposition, _, _ = _disposition("typed-state", outcome="RULE_NOT_SATISFIED")
    result, _, _ = _compose_disposition(disposition)
    assert result.m2_artifacts.subject.typed_state == "RULE_NOT_SATISFIED"
    assert result.b5_protocol_view.producer_typed_state == "RULE_NOT_SATISFIED"


def test_t08_m1_authority_dependency_determinant_replay_explanation_conserved():
    disposition, _, _ = _disposition("closures")
    result, _, _ = _compose_disposition(disposition)
    artifacts = result.m2_artifacts
    expected_auth_transport = {
        i4.authority_transport_ref(ref) for ref in disposition.authority_closure_refs
    }
    assert expected_auth_transport.issubset(set(artifacts.authority_closure.member_refs))
    assert tuple(artifacts.dependency_closure.member_refs) == tuple(
        sorted(set(disposition.dependency_refs), key=lambda ref: ref.key)
    )
    assert artifacts.determinant_closure.member_refs == (
        disposition.determinant_manifest_ref,
    )
    assert artifacts.replay_closure.member_refs == (disposition.replay_ref,)
    assert disposition.explanation_ref in artifacts.explanation_closure.member_refs
    assert (
        disposition.determinant_explanation_receipt_ref
        in artifacts.explanation_closure.member_refs
    )


def test_t09_m2_release_ref_is_exact_b5_release_ref():
    disposition, _, _ = _disposition("release-ref")
    result, _, _ = _compose_disposition(disposition)
    assert result.m2_artifacts.release.ref == result.b5_protocol_view.release_ref
    assert result.b5_subject.release_ref == result.m2_artifacts.release.ref


def test_t10_m2_closure_members_are_exact_b5_protocol_members():
    disposition, _, _ = _disposition("closure-members")
    result, _, _ = _compose_disposition(disposition)
    assert (
        result.b5_protocol_view.direct_dependency_refs
        == result.m2_artifacts.dependency_closure.member_refs
    )
    assert (
        result.b5_protocol_view.determinant_refs
        == result.m2_artifacts.determinant_closure.member_refs
    )
    assert tuple(result.b5_protocol_view.authority_snapshot_refs) == tuple(
        sorted(set(disposition.authority_closure_refs), key=lambda ref: ref.key)
    )


def test_t11_determinant_set_hash_is_recomputed_exactly():
    disposition, _, _ = _disposition("det-hash")
    result, _, _ = _compose_disposition(disposition)
    expected = semantic_hash(
        [ref.as_dict() for ref in result.b5_protocol_view.determinant_refs]
    )
    assert result.b5_protocol_view.determinant_set_hash == expected
    assert result.b5_subject.determinant_set_hash == expected


def test_t12_m2_publication_binding_does_not_make_b5_published():
    disposition, _, _ = _disposition("m2-binding")
    contract = _contract(actions=("REGISTER",), tag="m2-binding")
    executor = LearnedProductLifecycleExecutor()
    repo = M2Repository()
    result, repo, executor = _compose_disposition(
        disposition, contract=contract, executor=executor, repo=repo
    )
    release = result.m2_artifacts.release
    locator = _ref("RepresentationLocator", "m2-binding")
    integrity = _ref("RepresentationIntegrity", "m2-binding")
    register_representation(
        repo,
        release_ref=release.ref,
        resolution_mode="DIRECT_PRODUCER_REF",
        resolver_or_locator_ref=locator,
        representation_integrity_ref=integrity,
        resolved_subject_ref=release.release_subject_ref,
        producer_contract_ref=release.semantic_producer_contract_ref,
    )
    publish_binding(
        repo,
        release_ref=release.ref,
        resolution_mode="DIRECT_PRODUCER_REF",
        resolver_or_locator_ref=locator,
        representation_integrity_ref=integrity,
    )
    assert executor.lifecycle_state(release.ref).publication == "UNPUBLISHED"


def test_t13_m2_release_existence_does_not_register_b5_subject():
    disposition, _, _ = _disposition("no-register")
    executor = LearnedProductLifecycleExecutor()
    result, _, executor = _compose_disposition(disposition, executor=executor)
    assert result.m2_artifacts.release is not None
    assert executor.registered_release_refs == ()
    assert executor.staged_release_refs == ()
    assert result.receipt.side_effects["b5_registration_effect"] is False


def test_t14_b5_registration_does_not_publish():
    disposition, _, _ = _disposition("register-only")
    contract = _contract(actions=("REGISTER",), tag="register-only")
    result, _, executor = _compose_disposition(disposition, contract=contract)
    state = executor.lifecycle_state(result.m2_artifacts.release.ref)
    assert state.registered is True
    assert state.publication == "UNPUBLISHED"
    assert result.receipt.side_effects["b5_publication_effect"] is False


def test_t15_b5_publication_does_not_select_current():
    disposition, _, _ = _disposition("publish-only")
    contract = _contract(actions=("REGISTER", "PUBLISH"), tag="publish-only")
    result, _, executor = _compose_disposition(disposition, contract=contract)
    assert executor.lifecycle_state(result.m2_artifacts.release.ref).publication == "PUBLISHED"
    assert result.b5_selection_receipt is None
    assert result.receipt.b5_selection_receipt_ref is None
    assert result.receipt.side_effects["b5_current_selection_effect"] is False


def test_t16_current_selection_requires_explicit_action_and_exact_authority():
    disposition, _, _ = _disposition("select")
    missing = _contract(
        actions=("REGISTER", "PUBLISH", "SELECT_CURRENT"),
        tag="select-missing",
        selection_attestation_ref=None,
    )
    blocked, _, _ = _compose_disposition(disposition, contract=missing)
    assert blocked.receipt.terminal_state == "BLOCKED"
    assert blocked.receipt.side_effects["b5_registration_effect"] is False

    exact = _contract(
        actions=("REGISTER", "PUBLISH", "SELECT_CURRENT"),
        tag="select-exact",
    )
    selected, _, executor = _compose_disposition(disposition, contract=exact)
    assert selected.b5_selection_receipt is not None
    resolution = executor.resolve_selection_exact(
        selected.receipt.b5_selection_key_ref,
        selected.receipt.b5_selection_receipt_ref,
    )
    assert resolution.state == "CURRENT_SELECTED"


def test_t17_latest_default_newest_fuzzy_fallback_is_impossible():
    disposition, _, _ = _disposition("selectors")
    base = _contract()
    bad_hash = semantic_hash({"selector": "latest"})
    latest = ExactRef(
        "ProductFamily",
        f"urn:test:product:latest:sha256:{bad_hash}",
        bad_hash,
    )
    with pytest.raises(i4.LearnedWorldCompositionBlocked):
        replace(base, product_family_ref=latest)
    result, _, _ = _compose_disposition(disposition, contract=base)
    assert "LATEST" not in result.receipt.as_dict().__repr__().upper()


def test_t18_rule_not_satisfied_does_not_become_negative_semantic_truth():
    disposition, _, _ = _disposition("not-satisfied", outcome="RULE_NOT_SATISFIED")
    assert isinstance(disposition.semantic_claim_identity_ref, TypedAbsence)
    assert disposition.semantic_assertion_polarity_or_state == "NONE"
    result, _, _ = _compose_disposition(disposition)
    assert result.receipt.terminal_state == "RULE_NOT_SATISFIED"
    assert result.m2_artifacts.subject.ref == disposition.ref
    assert (
        result.receipt.conserved_state_material["semantic_assertion_polarity_or_state"]
        == "NONE"
    )


def test_t19_valid_empty_is_preserved_end_to_end():
    disposition, _, _ = _disposition(
        "valid-empty", valid_empty=True, outcome="ABSTAINED"
    )
    result, _, _ = _compose_disposition(disposition)
    assert "VALID_EMPTY" in _state_names(result.receipt)
    assert result.m2_artifacts.subject.ref == disposition.ref


def test_t20_noncomparable_blocked_unknown_and_integrity_failure_are_preserved():
    # NONCOMPARABLE empirical state
    auth = _m1_authority("i4-noncomp")
    _, m01_result, base = _bundle(validator_authorities=(auth,))
    binding = _binding(auth)
    receipt = m01_result.i05_result.receipts[0]
    old_ref = ExactRef(**dict(receipt.empirical_fact_refs[0]))
    old_fact = next(
        fact for fact in m01_result.object_graph.empirical_facts
        if fact.ref == old_ref
    )
    noncomp_fact = _clone_fact(
        old_fact,
        state="NONCOMPARABLE",
        numerator=old_fact.raw_numerator_support,
        denominator=old_fact.raw_denominator_support,
        tag="i4-noncomp",
    )
    noncomp_receipt = _receipt_with_fact(
        receipt,
        old_fact,
        noncomp_fact,
        tag="i4-noncomp-receipt",
    )
    noncomp_bundle = _replace_bundle_receipt_and_fact(
        m01_result, base, old_fact, noncomp_fact, noncomp_receipt
    )
    noncomp = m1.adjudicate_learned_empirical(
        noncomp_bundle,
        binding,
        validator_registry=_registry(binding, _validator(outcome="ABSTAINED")),
    )
    noncomp_result, _, _ = _compose_disposition(noncomp)
    assert "NONCOMPARABLE" in _state_names(noncomp_result.receipt)

    blocked, _, _ = _disposition("blocked-premise", channel_state="BLOCKED")
    blocked_result, _, _ = _compose_disposition(blocked)
    assert blocked_result.receipt.terminal_state == "BLOCKED"
    assert (
        blocked_result.receipt.conserved_state_material[
            "required_prerequisite_channel_states"
        ]["i4-required-premise"]
        == "BLOCKED"
    )

    unknown, _, _ = _disposition("unknown-premise", channel_state="UNKNOWN")
    unknown_result, _, _ = _compose_disposition(unknown)
    assert unknown_result.receipt.terminal_state == "UNRESOLVED"
    assert (
        unknown_result.receipt.conserved_state_material[
            "required_prerequisite_channel_states"
        ]["i4-required-premise"]
        == "UNKNOWN"
    )

    bad_auth = _m1_authority("i4-integrity")
    _, _, bad_bundle = _bundle(validator_authorities=(bad_auth,))
    bad_binding = _binding(bad_auth)
    bad_effects = dict(m1._FALSE_EFFECTS)
    bad_effects["structural_admission_effect"] = True
    integrity = m1.adjudicate_learned_empirical(
        bad_bundle,
        bad_binding,
        validator_registry=_registry(
            bad_binding, _validator(effects=bad_effects)
        ),
    )
    integrity_result, _, _ = _compose_disposition(integrity)
    assert integrity_result.receipt.terminal_state == "INTEGRITY_FAILURE"


def test_t21_direct_producer_route_requires_explicit_route_authority_and_acceptance():
    owner = _ref("ProducerOwner", "direct")
    producer = _ref("ProducerContract", "direct")
    ingress = i4.DirectProducerIngress(
        subject_ref=_ref("DirectProducerSubject", "direct"),
        producer_owner_ref=owner,
        producer_contract_ref=producer,
        typed_state="EXACT_DIRECT_PRODUCT",
        determinant_refs=(_ref("Determinant", "direct"),),
        replay_ref=_ref("Replay", "direct"),
        explanation_ref=_ref("Explanation", "direct"),
        semantic_ceiling="DIRECT_EXACT_GRAIN_ONLY",
    )
    blocked_contract = _contract(
        route="DIRECT_PRODUCER",
        producer_owner_ref=owner,
        producer_contract_ref=producer,
        direct_producer_route_authority_ref=None,
        direct_consumer_acceptance_ref=None,
    )
    blocked = i4.compose_direct_producer(blocked_contract, ingress)
    assert blocked.receipt.terminal_state == "BLOCKED"

    allowed_contract = replace(
        blocked_contract,
        direct_producer_route_authority_ref=_ref("DirectRouteAuthority", "direct"),
        direct_consumer_acceptance_ref=_ref("ConsumerAcceptance", "direct"),
    )
    allowed = i4.compose_direct_producer(allowed_contract, ingress)
    assert allowed.receipt.terminal_state == "EXACT_DIRECT_PRODUCT"
    assert allowed.receipt.reason_code == "DIRECT_PRODUCER_ROUTE_EXACTLY_AUTHORIZED"


def test_t22_missing_required_stage_cannot_switch_to_direct_route():
    contract = _contract(
        route="M1_M2_B5",
        direct_producer_route_authority_ref=_ref("DirectRouteAuthority", "tempting"),
        direct_consumer_acceptance_ref=_ref("ConsumerAcceptance", "tempting"),
    )
    result = i4.compose_learned_world(
        contract,
        m2_repository=M2Repository(),
        lifecycle_executor=LearnedProductLifecycleExecutor(),
        m1_disposition=None,
    )
    assert result.receipt.route_taken == "M1_M2_B5"
    assert result.receipt.terminal_state == "BLOCKED"
    assert result.receipt.m2_release_ref is None


def test_t23_composition_never_mints_consumer_permission():
    disposition, _, _ = _disposition("no-consumer-permission")
    result, _, _ = _compose_disposition(
        disposition,
        contract=_contract(
            actions=("REGISTER", "PUBLISH", "SELECT_CURRENT"),
            tag="no-consumer-permission",
        ),
    )
    assert result.receipt.side_effects["consumer_permission_effect"] is False
    assert result.b5_subject.producer_permission_ceiling_ref is not None


def test_t24_no_structural_causal_field_forge_or_v3_effect():
    disposition, _, _ = _disposition("no-other-effects")
    result, _, _ = _compose_disposition(disposition)
    effects = result.receipt.side_effects
    assert effects["structural_admission_effect"] is False
    assert effects["causal_truth_effect"] is False
    assert effects["field_forge_effect"] is False
    assert effects["actor_v3_effect"] is False


def test_t25_identical_input_and_contract_yield_identical_receipt():
    disposition, _, _ = _disposition("determinism")
    contract = _contract(tag="determinism")
    a, _, _ = _compose_disposition(disposition, contract=contract)
    b, _, _ = _compose_disposition(disposition, contract=contract)
    assert a.receipt.ref == b.receipt.ref
    assert a.m2_artifacts.release.ref == b.m2_artifacts.release.ref


def test_t26_changed_constitutive_contract_field_changes_contract_and_receipt_identity():
    disposition, _, _ = _disposition("contract-identity")
    a_contract = _contract(tag="contract-a")
    b_contract = replace(
        a_contract,
        consumer_product_purpose_ref=_ref("ConsumerPurpose", "contract-b"),
    )
    a, _, _ = _compose_disposition(disposition, contract=a_contract)
    b, _, _ = _compose_disposition(disposition, contract=b_contract)
    assert a_contract.ref != b_contract.ref
    assert a.receipt.ref != b.receipt.ref
    assert a.m2_artifacts.release.ref == b.m2_artifacts.release.ref


def test_t27_publication_binding_relayout_does_not_change_semantic_product_or_release():
    disposition, _, _ = _disposition("relayout")
    result, repo, _ = _compose_disposition(disposition)
    release = result.m2_artifacts.release
    bindings = []
    for tag in ("a", "b"):
        locator = _ref("RepresentationLocator", f"relayout-{tag}")
        integrity = _ref("RepresentationIntegrity", f"relayout-{tag}")
        register_representation(
            repo,
            release_ref=release.ref,
            resolution_mode="DIRECT_PRODUCER_REF",
            resolver_or_locator_ref=locator,
            representation_integrity_ref=integrity,
            resolved_subject_ref=release.release_subject_ref,
            producer_contract_ref=release.semantic_producer_contract_ref,
        )
        bindings.append(
            publish_binding(
                repo,
                release_ref=release.ref,
                resolution_mode="DIRECT_PRODUCER_REF",
                resolver_or_locator_ref=locator,
                representation_integrity_ref=integrity,
            )
        )
    assert bindings[0].ref != bindings[1].ref
    assert result.m2_artifacts.release.ref == release.ref
    assert result.b5_protocol_view.product_ref == disposition.ref


def test_t28_default_composition_preserves_b5_history_exactly():
    disposition, _, _ = _disposition("history")
    executor = LearnedProductLifecycleExecutor()
    before = executor.export_checkpoint()
    result, _, executor = _compose_disposition(disposition, executor=executor)
    after = executor.export_checkpoint()
    assert before == after
    assert result.receipt.b5_event_refs == ()
    assert executor.events == ()


def test_t29_replay_or_tamper_failure_closes():
    disposition, _, _ = _disposition("tamper")
    result, _, _ = _compose_disposition(disposition)
    tampered = replace(
        result.b5_protocol_view,
        determinant_set_hash="0" * 64,
    )
    with pytest.raises(LearnedProductLifecycleError):
        LearnedProductLifecycleSubject.from_protocol(tampered)


def test_t30_no_candidate_fiabc_astra_historical_stage_resurrection():
    source = inspect.getsource(i4).lower()
    imports = "\n".join(
        line for line in source.splitlines()
        if line.startswith("from ") or line.startswith("import ")
    )
    forbidden = (
        "candidate_a",
        "candidate_b",
        "candidate_c",
        "fiabc",
        "astra",
        "field_forge",
        "pre553_structural_admission",
        "p2x",
    )
    assert all(token not in imports for token in forbidden)
