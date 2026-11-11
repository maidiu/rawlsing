from dataclasses import replace

import pytest

from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef,
    ContextQueryItem,
    ExactRef,
    RepositoryEntry,
    V557DecisionState,
    V557PublicationEntry,
    build_v557_publication_bundle,
    build_v558_repository_bundle,
    exact_resolution_key,
    govern_v557,
    make_context_query,
    make_producer_locator,
    make_structural_object,
    resolve_v558,
    semantic_hash,
)
from rawlsing_next.m5_runtime_rsc_peer_prior import (
    BOUNDED_FAIL_CLOSED,
    FORBIDDEN_ACTOR_OUTPUTS,
    M5_PEER_EFFECT,
    M5RuntimeIntegrityError,
    RSCEntry,
    ResolvedStructuralContext,
    StructuralCurrentnessState,
    bind_structural_peer_use,
    make_structural_currentness_receipt,
    make_v3_peer_prior_requirement_declaration,
    materialize_resolved_structural_context,
    refresh_structural_currentness,
    validate_resolved_structural_context,
)


def _h(label: str) -> str:
    return semantic_hash({"label": label})


def _authority(label: str) -> AuthorityRef:
    return AuthorityRef(f"AUTH-{label}", "1.0.0", _h(f"authority-{label}"))


def _exact_ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:{kind.lower()}:{label}", _h(f"{kind}-{label}"))


def _runtime_universe(
    tag: str,
    *,
    producer_uses=("REVIEW", "CONTEXT", "ACTIVE_CAUSAL"),
    v557_uses=None,
    requested_uses=("ACTIVE_CAUSAL",),
    provenance=None,
):
    v557_uses = tuple(v557_uses if v557_uses is not None else producer_uses)
    payload = {"tag": tag, "semantic_class": "TEMPORAL_KEY", "state": "SUPPORTED"}
    obj = make_structural_object(
        producer_family="V553",
        semantic_class="TEMPORAL_KEY",
        object_id=f"urn:test:v553:{tag}",
        schema_id="TEST_V553_SCHEMA",
        schema_version="1.0.0",
        typed_state="SUPPORTED",
        producer_allowed_uses=producer_uses,
        payload=payload,
        source_stage=f"TEST-{tag}",
    )
    if "ACTIVE_CAUSAL" in v557_uses:
        decision = V557DecisionState.ALLOW_ACTIVE_CAUSAL_CONTEXT
    elif "CONTEXT" in v557_uses:
        decision = V557DecisionState.ALLOW_CONTEXT_ONLY
    else:
        decision = V557DecisionState.ALLOW_REVIEW_ONLY
    governance = govern_v557(
        obj,
        decision_state=decision,
        v557_allowed_uses=v557_uses,
        authority_ref=_authority(f"gov-{tag}"),
    )
    locator = make_producer_locator(
        obj,
        governance,
        logical_collection_kind="TEST-V553-COLLECTION",
        authoritative_build_id=f"BUILD-{tag}",
        authoritative_build_hash=_h(f"build-{tag}"),
        producer_contract_id="TEST-V553-CONTRACT",
        producer_contract_version="1.0.0",
        producer_contract_hash=_h("test-v553-contract"),
        producer_rule_bindings=(_authority(f"rule-{tag}"),),
        provenance_locator=provenance or f"audit://V553/{tag}",
    )
    entry = RepositoryEntry(obj, governance, locator)
    publication = build_v557_publication_bundle((V557PublicationEntry(obj, governance),))
    repository = build_v558_repository_bundle(publication, (entry,))
    query = make_context_query((ContextQueryItem(exact_resolution_key(locator), requested_uses),))
    resolution = resolve_v558(repository, query)
    return repository, locator, query, resolution


def _currentness(resolution, tag: str, *, state=StructuralCurrentnessState.CURRENT, previous=None):
    kwargs = {}
    if previous is not None:
        kwargs["previous_currentness"] = previous
        kwargs["refresh_reason_ref"] = _exact_ref("REFRESH_REASON", tag)
    return make_structural_currentness_receipt(
        resolution,
        state=state,
        authority_ref=_authority(f"currentness-{tag}"),
        structural_currentness_basis_ref=_exact_ref("CURRENTNESS_BASIS", tag),
        decision_effective_time_ref=_exact_ref("EFFECTIVE_TIME", tag),
        **kwargs,
    )


def _peer_requirement(tag: str):
    return make_v3_peer_prior_requirement_declaration(
        transition_owner_authority_ref=_authority(f"transition-{tag}"),
        transition_class=f"TEST_TRANSITION_{tag}",
        structural_peer_requirement="REQUIRED",
        empirical_peer_requirement="NOT_USED",
        structural_peer_operation_ref=_exact_ref("STRUCTURAL_OPERATION", tag),
        effective_time_rule_ref=_exact_ref("EFFECTIVE_TIME_RULE", tag),
        causal_parent_rule_ref=_exact_ref("CAUSAL_PARENT_RULE", tag),
    )


def _materialized(tag: str = "good"):
    repository, locator, query, resolution = _runtime_universe(tag)
    currentness = _currentness(resolution, tag)
    rsc = materialize_resolved_structural_context(repository, query, resolution, currentness)
    validation = validate_resolved_structural_context(rsc, repository, query, resolution, currentness)
    return repository, locator, query, resolution, currentness, rsc, validation


def test_exact_m4_resolution_materializes_rsc_and_replays_deterministically():
    repository, locator, query, resolution, currentness, first, validation1 = _materialized("deterministic")
    second = materialize_resolved_structural_context(repository, query, resolution, currentness)
    validation2 = validate_resolved_structural_context(second, repository, query, resolution, currentness)

    assert resolution.resolved_structural_context is None
    assert first == second
    assert first.context_id == second.context_id
    assert first.context_content_hash == second.context_content_hash
    assert first.machine_signature_value == second.machine_signature_value
    assert validation1 == validation2
    assert first.resolved_entries[0].resolution_key == exact_resolution_key(locator)


def test_missing_partial_and_denied_resolution_fail_closed_without_rsc_fabrication():
    repository, locator, _, _, = _runtime_universe(
        "failclosed",
        producer_uses=("REVIEW",),
        v557_uses=("REVIEW",),
        requested_uses=("REVIEW",),
    )
    missing_key = _h("missing-exact-key")

    missing_query = make_context_query((ContextQueryItem(missing_key, ("REVIEW",)),))
    missing_result = resolve_v558(repository, missing_query)
    with pytest.raises(M5RuntimeIntegrityError) as missing_exc:
        materialize_resolved_structural_context(
            repository, missing_query, missing_result, _currentness(missing_result, "missing")
        )
    assert missing_exc.value.code == BOUNDED_FAIL_CLOSED

    partial_query = make_context_query((
        ContextQueryItem(exact_resolution_key(locator), ("REVIEW",)),
        ContextQueryItem(missing_key, ("REVIEW",)),
    ))
    partial_result = resolve_v558(repository, partial_query)
    with pytest.raises(M5RuntimeIntegrityError) as partial_exc:
        materialize_resolved_structural_context(
            repository, partial_query, partial_result, _currentness(partial_result, "partial")
        )
    assert partial_exc.value.code == BOUNDED_FAIL_CLOSED

    denied_query = make_context_query((ContextQueryItem(exact_resolution_key(locator), ("ACTIVE_CAUSAL",)),))
    denied_result = resolve_v558(repository, denied_query)
    with pytest.raises(M5RuntimeIntegrityError) as denied_exc:
        materialize_resolved_structural_context(
            repository, denied_query, denied_result, _currentness(denied_result, "denied")
        )
    assert denied_exc.value.code == BOUNDED_FAIL_CLOSED


def test_hash_mismatch_and_corrupt_m4_evidence_fail_closed_exactly():
    repository, _, query, resolution = _runtime_universe("hash")
    bad_receipt = replace(resolution.receipt, receipt_hash=_h("bad-receipt"))
    bad_result = replace(resolution, receipt=bad_receipt)
    bad_currentness = _currentness(bad_result, "bad-result")
    with pytest.raises(M5RuntimeIntegrityError) as exc:
        materialize_resolved_structural_context(repository, query, bad_result, bad_currentness)
    assert exc.value.code == "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH"

    corrupt_repository = replace(repository, repository_hash=_h("corrupt-repository"))
    with pytest.raises(M5RuntimeIntegrityError) as repo_exc:
        materialize_resolved_structural_context(
            corrupt_repository, query, resolution, _currentness(resolution, "corrupt-repository")
        )
    assert repo_exc.value.code in {
        "M5_RSC_REFERENCE_CLOSURE_INVALID",
        "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
    }


def test_explicit_currentness_and_prospective_refresh_never_rewrite_history():
    repository, _, query, resolution = _runtime_universe("refresh")
    current1 = _currentness(resolution, "current-1")
    rsc1 = materialize_resolved_structural_context(repository, query, resolution, current1)
    old_receipt_tuple = (current1.receipt_id, current1.receipt_hash, current1.ref)

    stale = _currentness(resolution, "stale", state=StructuralCurrentnessState.STALE)
    with pytest.raises(M5RuntimeIntegrityError) as stale_exc:
        materialize_resolved_structural_context(repository, query, resolution, stale)
    assert stale_exc.value.code == BOUNDED_FAIL_CLOSED

    current2 = refresh_structural_currentness(
        current1,
        resolution,
        state=StructuralCurrentnessState.CURRENT,
        authority_ref=_authority("currentness-2"),
        structural_currentness_basis_ref=_exact_ref("CURRENTNESS_BASIS", "current-2"),
        decision_effective_time_ref=_exact_ref("EFFECTIVE_TIME", "current-2"),
        refresh_reason_ref=_exact_ref("REFRESH_REASON", "current-2"),
    )
    rsc2 = materialize_resolved_structural_context(repository, query, resolution, current2)

    assert current2.previous_currentness_ref == current1.ref
    assert (current1.receipt_id, current1.receipt_hash, current1.ref) == old_receipt_tuple
    assert rsc2.context_id != rsc1.context_id
    assert validate_resolved_structural_context(rsc1, repository, query, resolution, current1).result
    with pytest.raises(M5RuntimeIntegrityError):
        validate_resolved_structural_context(rsc1, repository, query, resolution, current2)


def test_repository_index_and_provenance_never_widen_permission_or_create_actor_effect():
    repository, locator, query, resolution = _runtime_universe(
        "nonsemantic",
        producer_uses=("REVIEW",),
        v557_uses=("REVIEW",),
        requested_uses=("ACTIVE_CAUSAL",),
        provenance="audit://ACTIVE_CAUSAL/POOLING/AUTHORIZED",
    )
    assert exact_resolution_key(locator) in {record.key for record in repository.index_manifest.records}
    assert resolution.receipt.result_state == "RESOLUTION_DENIED_OR_NOT_APPLICABLE"
    with pytest.raises(M5RuntimeIntegrityError) as denied_exc:
        materialize_resolved_structural_context(
            repository, query, resolution, _currentness(resolution, "nonsemantic")
        )
    assert denied_exc.value.code == BOUNDED_FAIL_CLOSED

    repository, locator, query, resolution, currentness, rsc, validation = _materialized("eligibility")
    actor_state = {"belief": "unchanged", "memory": ("historical",)}
    before = dict(actor_state)
    peer_use = bind_structural_peer_use(
        rsc,
        validation,
        _peer_requirement("eligibility"),
        requested_use="ACTIVE_CAUSAL",
        required_resolution_keys=(exact_resolution_key(locator),),
    )
    assert peer_use.effect == M5_PEER_EFFECT
    assert peer_use.actor_state_effect is False
    assert actor_state == before

    with pytest.raises(M5RuntimeIntegrityError) as provenance_exc:
        bind_structural_peer_use(
            rsc,
            validation,
            _peer_requirement("pooling"),
            requested_use="SOURCE_POOL",
            required_resolution_keys=(exact_resolution_key(locator),),
        )
    assert provenance_exc.value.code == "M5_RSC_PERMISSION_PROOF_INVALID"


def test_rsc_epi_actor_state_noncollapse_and_no_prior_to_psyche_surface():
    _, _, _, _, _, rsc, _ = _materialized("noncollapse")
    fields = set(ResolvedStructuralContext.__dataclass_fields__)
    lowered = {field.lower() for field in fields}

    assert "v3empiricalpossibilityinput" not in "".join(lowered)
    assert "actorcausalstate" not in "".join(lowered)
    assert not any(output in lowered for output in FORBIDDEN_ACTOR_OUTPUTS)
    assert not hasattr(rsc, "psepf")
    assert not hasattr(rsc, "persona")
    assert not hasattr(rsc, "belief")
    assert not hasattr(rsc, "memory")


def test_missing_runtime_instance_and_tampered_rsc_digests_fail_with_frozen_codes():
    repository, _, query, resolution, currentness, rsc, _ = _materialized("tamper")

    with pytest.raises(M5RuntimeIntegrityError) as missing_exc:
        validate_resolved_structural_context(None, repository, query, resolution, currentness)
    assert missing_exc.value.code == "M5_RSC_RUNTIME_INSTANCE_MISSING"

    cases = (
        (replace(rsc, producer_binding_digest=_h("bad-producer")), "M5_RSC_PRODUCER_BINDING_MISMATCH"),
        (replace(rsc, permission_subset_proof_digest=_h("bad-permission")), "M5_RSC_PERMISSION_PROOF_INVALID"),
        (replace(rsc, reference_closure_digest=_h("bad-closure")), "M5_RSC_REFERENCE_CLOSURE_INVALID"),
        (replace(rsc, provenance_root_digest=_h("bad-provenance")), "M5_RSC_PROVENANCE_AUTHORITY_VIOLATION"),
        (replace(rsc, machine_signature_value=_h("bad-signature")), "M5_RSC_SIGNATURE_MISMATCH"),
        (replace(rsc, context_content_hash=_h("bad-context")), "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH"),
    )
    for bad_rsc, expected_code in cases:
        with pytest.raises(M5RuntimeIntegrityError) as exc:
            validate_resolved_structural_context(bad_rsc, repository, query, resolution, currentness)
        assert exc.value.code == expected_code


def test_forbidden_v3_reference_class_in_rsc_is_rejected_before_use():
    repository, _, query, resolution, currentness, rsc, _ = _materialized("forbidden")
    original = rsc.resolved_entries[0]
    forbidden = RSCEntry(
        original.resolution_key,
        original.selection_record_ref,
        original.canonical_producer_family,
        ExactRef("V3EmpiricalPossibilityInput", "urn:test:epi", _h("epi")),
        original.producer_locator_ref,
        original.resolver_allowed_uses,
        original.decision_state,
        original.closure_digest,
    )
    bad_rsc = replace(rsc, resolved_entries=(forbidden,))
    with pytest.raises(M5RuntimeIntegrityError) as exc:
        validate_resolved_structural_context(bad_rsc, repository, query, resolution, currentness)
    assert exc.value.code == "M5_RSC_FORBIDDEN_REFERENCE_CLASS_PRESENT"


def test_peer_requirement_is_exact_and_structural_currentness_never_substitutes_empirical_permission():
    repository, locator, query, resolution, currentness, rsc, validation = _materialized("declaration")
    declaration = _peer_requirement("declaration")
    assert declaration.empirical_peer_requirement == "NOT_USED"
    assert declaration.empirical_read_permission_id is None

    receipt1 = bind_structural_peer_use(
        rsc,
        validation,
        declaration,
        requested_use="ACTIVE_CAUSAL",
        required_resolution_keys=(exact_resolution_key(locator),),
    )
    receipt2 = bind_structural_peer_use(
        rsc,
        validation,
        declaration,
        requested_use="ACTIVE_CAUSAL",
        required_resolution_keys=(exact_resolution_key(locator),),
    )
    assert receipt1 == receipt2
    assert receipt1.actor_state_effect is False

    not_used = make_v3_peer_prior_requirement_declaration(
        transition_owner_authority_ref=_authority("transition-not-used"),
        transition_class="TEST_NOT_USED",
        structural_peer_requirement="NOT_USED",
        empirical_peer_requirement="NOT_USED",
        structural_peer_operation_ref=None,
        effective_time_rule_ref=_exact_ref("EFFECTIVE_TIME_RULE", "not-used"),
        causal_parent_rule_ref=_exact_ref("CAUSAL_PARENT_RULE", "not-used"),
    )
    with pytest.raises(M5RuntimeIntegrityError) as exc:
        bind_structural_peer_use(
            rsc,
            validation,
            not_used,
            requested_use="ACTIVE_CAUSAL",
            required_resolution_keys=(exact_resolution_key(locator),),
        )
    assert exc.value.code == BOUNDED_FAIL_CLOSED
