from dataclasses import replace

import pytest

from rawlsing_next.m4_v557_v558_publication_repository import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next.objective_non_event_publication_serving_adapter import (
    CANONICAL_PRODUCER_FAMILY,
    NonEventAdapterIntegrityError,
    build_non_event_publication_bundle,
    build_non_event_repository_bundle,
    make_non_event_context_query,
    make_non_event_context_query_item,
    make_non_event_publication_entry,
    make_non_event_staged_item,
    make_objective_non_event_currentness_receipt,
    make_objective_non_event_serving_receipt,
    resolve_non_event,
)


def _h(label):
    return semantic_hash({"label": label})


def _ref(kind, label):
    return ExactRef(kind, f"urn:test:{label}", _h(label))


def _auth(label):
    return AuthorityRef(f"AUTH-{label}", "1.0.0", _h(f"auth-{label}"))


def _chain(tag, *, currentness="CURRENT"):
    item = make_non_event_staged_item(
        producer_object_ref=_ref("SDTF_OBJECTIVE_FACT", f"fact-{tag}"),
        producer_locator_ref=_ref("PRODUCER_LOCATOR", f"loc-{tag}"),
        canonical_producer_family=CANONICAL_PRODUCER_FAMILY,
        producer_semantic_class="OBJECTIVE_POSITIONED_CONSEQUENCE",
        producer_owner_authority_ref=_auth(f"owner-{tag}"),
        producer_schema_ref=_ref("PRODUCER_SCHEMA", f"schema-{tag}"),
        temporal_form="CONDITION",
        assertion_kind="K1_CONSTITUTIVE_POSITIONAL",
        polarity="POSITIVE",
        currentness=currentness,
        modality="ACTUAL",
        proof_adjudication="SUPPORTED",
        valid_time_binding_ref=_ref("VALID_TIME_BINDING", f"valid-{tag}"),
        decision_effective_time_ref=_ref("DECISION_EFFECTIVE_TIME", f"effective-{tag}"),
        world_or_release_root_ref_or_null=(
            _ref("OBJECTIVE_WORLD_RELEASE_ROOT", f"world-{tag}") if currentness == "CURRENT" else None
        ),
        source_evidence_refs=(_ref("SOURCE_EVIDENCE", f"evidence-{tag}"),),
        producer_allowed_uses=("REVIEW", "CONTEXT"),
    )
    entry = make_non_event_publication_entry(
        item, publication_authority_ref=_auth("publication"),
        publication_allowed_uses=("REVIEW", "CONTEXT"),
    )
    publication = build_non_event_publication_bundle((entry,))
    repository = build_non_event_repository_bundle(publication)
    query_item = make_non_event_context_query_item(entry, ("CONTEXT",))
    query = make_non_event_context_query((query_item,))
    resolution = resolve_non_event(repository, query)
    return item, publication, repository, query_item, query, resolution


def test_current_service_requires_actual_compatible_currentness_object():
    item, publication, repository, query_item, query, resolution = _chain("ok")
    authority = _auth("currentness")
    basis = _ref("CURRENTNESS_BASIS", "basis")
    currentness = make_objective_non_event_currentness_receipt(
        repository, query, resolution, resolution_key=query_item.resolution_key,
        state="CURRENT", authority_ref=authority,
        structural_currentness_basis_ref=basis,
    )
    receipt = make_objective_non_event_serving_receipt(
        publication, repository, query, resolution,
        resolution_key=query_item.resolution_key,
        currentness_receipt_or_null=currentness,
        currentness_authority_ref_or_null=authority,
        structural_currentness_basis_ref_or_null=basis,
    )
    assert receipt.currentness_receipt_ref_or_null == currentness.ref
    assert receipt.world_or_release_root_ref_or_null == item.world_or_release_root_ref_or_null


def test_ref_only_input_is_rejected():
    _, publication, repository, query_item, query, resolution = _chain("ref-only")
    with pytest.raises(NonEventAdapterIntegrityError, match="ref-only"):
        make_objective_non_event_serving_receipt(
            publication, repository, query, resolution,
            resolution_key=query_item.resolution_key,
            currentness_receipt_ref_or_null=_ref("OBJECTIVE_CURRENTNESS_RECEIPT", "opaque"),
        )


def test_historical_remains_historical_without_currentness_object():
    _, publication, repository, query_item, query, resolution = _chain("historical", currentness="HISTORICAL")
    receipt = make_objective_non_event_serving_receipt(
        publication, repository, query, resolution,
        resolution_key=query_item.resolution_key,
    )
    assert receipt.currentness == "HISTORICAL"
    assert receipt.currentness_receipt_ref_or_null is None
