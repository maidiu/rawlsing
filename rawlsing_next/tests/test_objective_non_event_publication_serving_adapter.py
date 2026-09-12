from dataclasses import replace

import pytest

from rawlsing_next.m4_v557_v558_publication_repository import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next.objective_non_event_publication_serving_adapter import (
    CANONICAL_PRODUCER_FAMILY,
    INGRESS_EFFECT,
    NonEventAdapterIntegrityError,
    NonEventPermissionError,
    build_non_event_publication_bundle,
    build_non_event_repository_bundle,
    make_non_event_context_query,
    make_non_event_context_query_item,
    make_non_event_publication_entry,
    make_non_event_staged_item,
    make_objective_non_event_serving_receipt,
    resolve_non_event,
    validate_objective_non_event_serving_receipt,
)


def _h(label: str) -> str:
    return semantic_hash({"label": label})


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:{label}", _h(label))


def _authority(label: str = "owner") -> AuthorityRef:
    return AuthorityRef(f"AUTH-{label}", "1.0.0", _h(f"authority-{label}"))


def _item(
    tag: str,
    *,
    temporal_form: str = "CONDITION",
    assertion_kind: str = "K1_CONSTITUTIVE_POSITIONAL",
    currentness: str = "CURRENT",
    uses=("REVIEW", "CONTEXT"),
    actor_indexed: bool = False,
    closure: bool = False,
):
    return make_non_event_staged_item(
        producer_object_ref=_ref("SDTF_OBJECTIVE_FACT", f"fact-{tag}"),
        producer_locator_ref=_ref("PRODUCER_LOCATOR", f"locator-{tag}"),
        canonical_producer_family=CANONICAL_PRODUCER_FAMILY,
        producer_semantic_class="OBJECTIVE_POSITIONED_CONSEQUENCE",
        producer_owner_authority_ref=_authority(f"owner-{tag}"),
        producer_schema_ref=_ref("PRODUCER_SCHEMA", f"schema-{tag}"),
        temporal_form=temporal_form,
        assertion_kind=assertion_kind,
        polarity="POSITIVE",
        currentness=currentness,
        modality="ACTUAL_OR_QUALIFIED",
        proof_adjudication="SUPPORTED",
        valid_time_binding_ref=_ref("VALID_TIME_BINDING", f"valid-{tag}"),
        decision_effective_time_ref=_ref("DECISION_EFFECTIVE_TIME", f"decision-{tag}"),
        objective_actor_binding_ref_or_null=(
            _ref("OBJECTIVE_ACTOR_BINDING", f"actor-{tag}") if actor_indexed else None
        ),
        objective_position_context_binding_ref_or_null=(
            _ref("OBJECTIVE_POSITION_CONTEXT", f"position-{tag}") if actor_indexed else None
        ),
        world_or_release_root_ref_or_null=(
            _ref("OBJECTIVE_WORLD_RELEASE_ROOT", f"world-{tag}") if currentness == "CURRENT" else None
        ),
        source_evidence_refs=(_ref("SOURCE_EVIDENCE", f"evidence-{tag}"),),
        determinant_or_witness_refs=(_ref("OBJECTIVE_WITNESS", f"witness-{tag}"),),
        negative_or_closure_refs=(
            (_ref("TERMINATION_COVERAGE", f"closure-{tag}"),) if closure else ()
        ),
        producer_allowed_uses=uses,
    )


def _published(item, *, uses=("REVIEW", "CONTEXT")):
    entry = make_non_event_publication_entry(
        item,
        publication_authority_ref=_authority("publication"),
        publication_allowed_uses=uses,
    )
    publication = build_non_event_publication_bundle((entry,))
    repository = build_non_event_repository_bundle(publication)
    return entry, publication, repository


def _resolved(entry, repository, *, uses=("CONTEXT",)):
    query_item = make_non_event_context_query_item(entry, uses)
    query = make_non_event_context_query((query_item,))
    resolution = resolve_non_event(repository, query)
    return query_item, query, resolution


@pytest.mark.parametrize(
    ("temporal_form", "assertion_kind", "closure"),
    (
        ("CONDITION", "K1_CONSTITUTIVE_POSITIONAL", False),
        ("DIRECTED_RELATION", "K2_QUALIFIED_POSSIBILITY", False),
        ("RECURRENT_ACTIVITY", "K4_ACTIVE_DURATIVE", True),
    ),
)
def test_all_adopted_non_event_forms_publish_and_resolve_without_k3_laundering(
    temporal_form, assertion_kind, closure
):
    item = _item(
        f"{temporal_form}-{assertion_kind}",
        temporal_form=temporal_form,
        assertion_kind=assertion_kind,
        closure=closure,
    )
    entry, publication, repository = _published(item)
    query_item, query, resolution = _resolved(entry, repository)

    assert resolution.receipt.result_state == "RESOLUTION_COMPLETE"
    receipt = make_objective_non_event_serving_receipt(
        publication,
        repository,
        query,
        resolution,
        resolution_key=query_item.resolution_key,
        currentness_receipt_ref_or_null=_ref("OBJECTIVE_CURRENTNESS_RECEIPT", "current"),
    )
    assert receipt.temporal_form == temporal_form
    assert receipt.assertion_kind == assertion_kind
    assert receipt.actor_state_effect is False
    assert receipt.ingress_effect == INGRESS_EFFECT
    assert receipt.resolver_allowed_uses == ("CONTEXT",)


def test_lawful_objective_actor_indexing_remains_context_only_and_zero_person_state():
    item = _item("actor-indexed", actor_indexed=True)
    entry, publication, repository = _published(item)
    query_item, query, resolution = _resolved(entry, repository)
    receipt = make_objective_non_event_serving_receipt(
        publication,
        repository,
        query,
        resolution,
        resolution_key=query_item.resolution_key,
        currentness_receipt_ref_or_null=_ref("OBJECTIVE_CURRENTNESS_RECEIPT", "actor-current"),
        v3_transition_owner_declaration_ref_or_null=_ref(
            "V3_PEER_PRIOR_REQUIREMENT_DECLARATION", "v3-owner"
        ),
    )

    assert receipt.objective_actor_binding_ref_or_null == item.objective_actor_binding_ref_or_null
    assert (
        receipt.objective_position_context_binding_ref_or_null
        == item.objective_position_context_binding_ref_or_null
    )
    assert receipt.actor_state_effect is False
    material_names = set(receipt.__dataclass_fields__)
    assert not {"belief", "appraisal", "motivation", "memory", "response", "persona"} & material_names


@pytest.mark.parametrize(
    ("temporal_form", "assertion_kind"),
    (
        ("EVENT", "K1_CONSTITUTIVE_POSITIONAL"),
        ("TRANSITION", "K1_CONSTITUTIVE_POSITIONAL"),
        ("ORDERED_HISTORY", "K1_CONSTITUTIVE_POSITIONAL"),
        ("CONDITION", "K3_REALIZED_OCCURRENCE"),
    ),
)
def test_event_laundering_and_nonadopted_generic_forms_fail_closed(
    temporal_form, assertion_kind
):
    with pytest.raises(NonEventAdapterIntegrityError):
        _item(
            f"reject-{temporal_form}-{assertion_kind}",
            temporal_form=temporal_form,
            assertion_kind=assertion_kind,
        )


def test_unknown_not_proven_and_current_without_world_root_are_not_positive_facts():
    base = dict(
        producer_object_ref=_ref("SDTF_OBJECTIVE_FACT", "unknown"),
        producer_locator_ref=_ref("PRODUCER_LOCATOR", "unknown-locator"),
        canonical_producer_family=CANONICAL_PRODUCER_FAMILY,
        producer_semantic_class="OBJECTIVE_POSITIONED_CONSEQUENCE",
        producer_owner_authority_ref=_authority("unknown"),
        producer_schema_ref=_ref("PRODUCER_SCHEMA", "unknown-schema"),
        temporal_form="CONDITION",
        assertion_kind="K1_CONSTITUTIVE_POSITIONAL",
        polarity="POSITIVE",
        currentness="CURRENT",
        modality="ACTUAL",
        valid_time_binding_ref=_ref("VALID_TIME_BINDING", "unknown-vt"),
        decision_effective_time_ref=_ref("DECISION_EFFECTIVE_TIME", "unknown-dt"),
        source_evidence_refs=(_ref("SOURCE_EVIDENCE", "unknown-ev"),),
        producer_allowed_uses=("REVIEW",),
    )
    with pytest.raises(NonEventAdapterIntegrityError, match="UNKNOWN_NOT_PROVEN"):
        make_non_event_staged_item(**base, proof_adjudication="UNKNOWN_NOT_PROVEN")

    with pytest.raises(NonEventAdapterIntegrityError, match="world/release"):
        make_non_event_staged_item(**base, proof_adjudication="SUPPORTED")


def test_k4_current_durative_requires_exact_closure_or_termination_coverage():
    with pytest.raises(NonEventAdapterIntegrityError, match="termination"):
        _item(
            "durative-no-closure",
            temporal_form="RECURRENT_ACTIVITY",
            assertion_kind="K4_ACTIVE_DURATIVE",
            closure=False,
        )


def test_publication_and_resolver_cannot_widen_producer_permissions():
    active_capable = _item(
        "active-ceiling", uses=("REVIEW", "CONTEXT", "ACTIVE_CAUSAL")
    )
    with pytest.raises(NonEventPermissionError, match="ACTIVE_CAUSAL"):
        make_non_event_publication_entry(
            active_capable,
            publication_authority_ref=_authority("publication-active"),
            publication_allowed_uses=("ACTIVE_CAUSAL",),
        )

    review_only = _item("review-only", uses=("REVIEW",))
    with pytest.raises(NonEventPermissionError):
        make_non_event_publication_entry(
            review_only,
            publication_authority_ref=_authority("publication-widen"),
            publication_allowed_uses=("CONTEXT",),
        )

    item = _item("resolver-widen", uses=("REVIEW", "CONTEXT"))
    entry, _, repository = _published(item, uses=("REVIEW",))
    query_item = make_non_event_context_query_item(entry, ("CONTEXT",))
    query = make_non_event_context_query((query_item,))
    resolution = resolve_non_event(repository, query)
    assert resolution.receipt.result_state == "RESOLUTION_DENIED_OR_NOT_APPLICABLE"
    assert resolution.selections[0].decision == "PERMISSION_DENIED"
    assert resolution.selections[0].resolver_allowed_uses == ()


def test_current_serving_receipt_requires_exact_currentness_ref_and_preserves_world_binding():
    item = _item("currentness")
    entry, publication, repository = _published(item)
    query_item, query, resolution = _resolved(entry, repository)

    with pytest.raises(NonEventAdapterIntegrityError, match="currentness"):
        make_objective_non_event_serving_receipt(
            publication,
            repository,
            query,
            resolution,
            resolution_key=query_item.resolution_key,
            currentness_receipt_ref_or_null=None,
        )

    current_ref = _ref("OBJECTIVE_CURRENTNESS_RECEIPT", "currentness-exact")
    receipt = make_objective_non_event_serving_receipt(
        publication,
        repository,
        query,
        resolution,
        resolution_key=query_item.resolution_key,
        currentness_receipt_ref_or_null=current_ref,
    )
    assert receipt.currentness_receipt_ref_or_null == current_ref
    assert receipt.world_or_release_root_ref_or_null == item.world_or_release_root_ref_or_null


def test_historical_item_is_not_relabelled_current_and_may_preserve_null_currentness_receipt():
    item = _item("historical", currentness="HISTORICAL")
    entry, publication, repository = _published(item)
    query_item, query, resolution = _resolved(entry, repository, uses=("REVIEW",))
    receipt = make_objective_non_event_serving_receipt(
        publication,
        repository,
        query,
        resolution,
        resolution_key=query_item.resolution_key,
        currentness_receipt_ref_or_null=None,
    )
    assert receipt.currentness == "HISTORICAL"
    assert receipt.currentness_receipt_ref_or_null is None
    assert receipt.world_or_release_root_ref_or_null is None


def test_serving_receipt_hash_tamper_and_person_state_effect_fail_closed():
    item = _item("tamper")
    entry, publication, repository = _published(item)
    query_item, query, resolution = _resolved(entry, repository)
    receipt = make_objective_non_event_serving_receipt(
        publication,
        repository,
        query,
        resolution,
        resolution_key=query_item.resolution_key,
        currentness_receipt_ref_or_null=_ref("OBJECTIVE_CURRENTNESS_RECEIPT", "tamper-current"),
    )

    with pytest.raises(NonEventAdapterIntegrityError, match="identity/hash"):
        validate_objective_non_event_serving_receipt(
            replace(receipt, receipt_content_hash="0" * 64)
        )
    with pytest.raises(NonEventAdapterIntegrityError, match="person-state"):
        validate_objective_non_event_serving_receipt(
            replace(receipt, actor_state_effect=True)
        )


def test_exact_resolution_key_has_no_fuzzy_repair():
    item = _item("exact-key")
    entry, _, repository = _published(item)
    query_item_type = type(make_non_event_context_query_item(entry, ("REVIEW",)))
    query = make_non_event_context_query((query_item_type("0" * 64, ("REVIEW",)),))
    resolution = resolve_non_event(repository, query)
    assert resolution.receipt.result_state == "RESOLUTION_MISSING_REQUIRED_AUTHORITY"
    assert resolution.selections[0].decision == "UNRESOLVED_EXACT_KEY"
