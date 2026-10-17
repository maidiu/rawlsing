#!/usr/bin/env python3
"""Producer-preserving publication/serving adapter for objective PRE-V3 non-events.

This module implements the HQ-adopted C06 non-event contract without extending the
frozen M4 root-family allowlist.  It mirrors M4's exact-identity, content-addressed,
item-wise permission and fail-closed resolution laws for the one adopted generic
D1-prime producer family.  It creates context availability only; it exposes no event
fabrication and no person-state mutation surface.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping, Sequence

from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef,
    ExactRef,
    M4IntegrityError,
    PERMISSION_ATOMS,
    exact_ref,
    semantic_hash,
)

ADAPTER_CONTRACT_ID = "PREV3_OBJECTIVE_NON_EVENT_PUBLICATION_SERVING_ADAPTER@1.0.0"
CANONICAL_PRODUCER_FAMILY = "SDTF_D1_PRIME_OBJECTIVE_POSITIONED_CONSEQUENCE"

STAGED_ITEM_SCHEMA = "PREV3_OBJECTIVE_NON_EVENT_STAGED_ITEM@1.0.0"
PUBLICATION_ENTRY_SCHEMA = "PREV3_OBJECTIVE_NON_EVENT_PUBLICATION_ENTRY@1.0.0"
PUBLICATION_BUNDLE_SCHEMA = "PREV3_OBJECTIVE_NON_EVENT_PUBLICATION_BUNDLE@1.0.0"
REPOSITORY_SCHEMA = "PREV3_OBJECTIVE_NON_EVENT_REPOSITORY@1.0.0"
QUERY_SCHEMA = "PREV3_OBJECTIVE_NON_EVENT_CONTEXT_QUERY@1.0.0"
SELECTION_SCHEMA = "PREV3_OBJECTIVE_NON_EVENT_SELECTION_RECORD@1.0.0"
RESOLUTION_RECEIPT_SCHEMA = "PREV3_OBJECTIVE_NON_EVENT_RESOLUTION_RECEIPT@1.0.0"
SERVING_RECEIPT_SCHEMA_ID = "OBJECTIVE_NON_EVENT_SERVING_RECEIPT"
SERVING_RECEIPT_SCHEMA_VERSION = "1.0.0"

ELIGIBLE_TEMPORAL_FORMS = frozenset({"CONDITION", "DIRECTED_RELATION", "RECURRENT_ACTIVITY"})
ELIGIBLE_ASSERTION_KINDS = frozenset(
    {"K1_CONSTITUTIVE_POSITIONAL", "K2_QUALIFIED_POSSIBILITY", "K4_ACTIVE_DURATIVE"}
)
CURRENTNESS_VALUES = frozenset({"CURRENT", "HISTORICAL"})
NON_EVENT_SERVING_USE_ATOMS = frozenset({"REVIEW", "CONTEXT"})
UNKNOWN_NOT_PROVEN = "UNKNOWN_NOT_PROVEN"

INGRESS_EFFECT = "STRUCTURAL_CONTEXT_ELIGIBILITY_ONLY__NOT_V3_MUTATION_PERMISSION"
ACTOR_STATE_EFFECT = False
_SHA = re.compile(r"^[0-9a-f]{64}$")


class NonEventAdapterIntegrityError(M4IntegrityError):
    """Fail-closed identity, semantic-shape, currentness or replay error."""


class NonEventPermissionError(NonEventAdapterIntegrityError):
    """Producer/publication/resolver permission subset violation."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise NonEventAdapterIntegrityError(f"{name} must be a non-empty string")
    out = value.strip()
    if out.lower() in {"latest", "default", "*"}:
        raise NonEventAdapterIntegrityError(f"{name} may not use latest/default/fuzzy selection")
    return out


def _hash_text(value: Any, name: str) -> str:
    out = _text(value, name)
    if not _SHA.fullmatch(out):
        raise NonEventAdapterIntegrityError(f"{name} must be lowercase sha256")
    return out


def _ref(value: ExactRef | Mapping[str, str], name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except M4IntegrityError as exc:
        raise NonEventAdapterIntegrityError(str(exc)) from exc


def _refs(values: Sequence[ExactRef | Mapping[str, str]], name: str) -> tuple[ExactRef, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise NonEventAdapterIntegrityError(f"{name} must be a sequence")
    out = tuple(_ref(value, name) for value in values)
    keys = [(r.kind, r.object_id, r.content_hash) for r in out]
    if len(set(keys)) != len(keys):
        raise NonEventAdapterIntegrityError(f"{name} contains duplicate exact refs")
    return tuple(sorted(out, key=lambda r: (r.kind, r.object_id, r.content_hash)))


def _authority(value: AuthorityRef, name: str) -> AuthorityRef:
    if not isinstance(value, AuthorityRef):
        raise NonEventAdapterIntegrityError(f"{name} must be an exact AuthorityRef")
    return value


def _uses(
    values: Sequence[str],
    name: str,
    *,
    allow_empty: bool = False,
    non_event_serving_ceiling: bool = False,
) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise NonEventAdapterIntegrityError(f"{name} must be a sequence")
    out = tuple(sorted({_text(v, name) for v in values}))
    if not allow_empty and not out:
        raise NonEventAdapterIntegrityError(f"{name} must not be empty")
    if not set(out) <= PERMISSION_ATOMS:
        raise NonEventAdapterIntegrityError(f"{name} contains non-frozen permission atoms")
    if non_event_serving_ceiling and not set(out) <= NON_EVENT_SERVING_USE_ATOMS:
        raise NonEventPermissionError(
            f"{name} exceeds generic non-event REVIEW/CONTEXT ceiling; ACTIVE_CAUSAL is not admitted"
        )
    return out


def _opt_ref(value: ExactRef | Mapping[str, str] | None, name: str) -> ExactRef | None:
    return None if value is None else _ref(value, name)


def _ref_dict(value: ExactRef | None) -> dict[str, str] | None:
    return value.as_dict() if value is not None else None


@dataclass(frozen=True)
class NonEventStagedItem:
    item_id: str
    item_hash: str
    schema: str
    producer_object_ref: ExactRef
    producer_locator_ref: ExactRef
    canonical_producer_family: str
    producer_semantic_class: str
    producer_owner_authority_ref: AuthorityRef
    producer_schema_ref: ExactRef
    temporal_form: str
    assertion_kind: str
    polarity: str
    currentness: str
    modality: str
    proof_adjudication: str
    valid_time_binding_ref: ExactRef
    decision_effective_time_ref: ExactRef
    objective_actor_binding_ref_or_null: ExactRef | None
    objective_position_context_binding_ref_or_null: ExactRef | None
    world_or_release_root_ref_or_null: ExactRef | None
    source_evidence_refs: tuple[ExactRef, ...]
    determinant_or_witness_refs: tuple[ExactRef, ...]
    negative_or_closure_refs: tuple[ExactRef, ...]
    producer_allowed_uses: tuple[str, ...]

    @property
    def ref(self) -> ExactRef:
        return ExactRef("PREV3_OBJECTIVE_NON_EVENT_STAGED_ITEM", self.item_id, self.item_hash)


def _staged_material(item: NonEventStagedItem) -> dict[str, Any]:
    return {
        "schema": STAGED_ITEM_SCHEMA,
        "adapter_contract_id": ADAPTER_CONTRACT_ID,
        "producer_object_ref": item.producer_object_ref.as_dict(),
        "producer_locator_ref": item.producer_locator_ref.as_dict(),
        "canonical_producer_family": item.canonical_producer_family,
        "producer_semantic_class": item.producer_semantic_class,
        "producer_owner_authority_ref": item.producer_owner_authority_ref.as_dict(),
        "producer_schema_ref": item.producer_schema_ref.as_dict(),
        "temporal_form": item.temporal_form,
        "assertion_kind": item.assertion_kind,
        "polarity": item.polarity,
        "currentness": item.currentness,
        "modality": item.modality,
        "proof_adjudication": item.proof_adjudication,
        "valid_time_binding_ref": item.valid_time_binding_ref.as_dict(),
        "decision_effective_time_ref": item.decision_effective_time_ref.as_dict(),
        "objective_actor_binding_ref_or_null": _ref_dict(item.objective_actor_binding_ref_or_null),
        "objective_position_context_binding_ref_or_null": _ref_dict(
            item.objective_position_context_binding_ref_or_null
        ),
        "world_or_release_root_ref_or_null": _ref_dict(item.world_or_release_root_ref_or_null),
        "source_evidence_refs": [r.as_dict() for r in item.source_evidence_refs],
        "determinant_or_witness_refs": [r.as_dict() for r in item.determinant_or_witness_refs],
        "negative_or_closure_refs": [r.as_dict() for r in item.negative_or_closure_refs],
        "producer_allowed_uses": list(item.producer_allowed_uses),
        "actor_state_effect": False,
    }


def _validate_staged_item(item: NonEventStagedItem) -> None:
    if not isinstance(item, NonEventStagedItem) or item.schema != STAGED_ITEM_SCHEMA:
        raise NonEventAdapterIntegrityError("staged item type/schema mismatch")
    if item.canonical_producer_family != CANONICAL_PRODUCER_FAMILY:
        raise NonEventAdapterIntegrityError("producer family is outside adopted generic D1-prime binding")
    if item.temporal_form not in ELIGIBLE_TEMPORAL_FORMS:
        raise NonEventAdapterIntegrityError("event/transition/history form is not generic non-event ingress")
    if item.assertion_kind not in ELIGIBLE_ASSERTION_KINDS:
        raise NonEventAdapterIntegrityError("K3 or unknown assertion kind is not generic non-event ingress")
    if item.proof_adjudication == UNKNOWN_NOT_PROVEN:
        raise NonEventAdapterIntegrityError("UNKNOWN_NOT_PROVEN is not a positive objective fact")
    if item.currentness not in CURRENTNESS_VALUES:
        raise NonEventAdapterIntegrityError("currentness must be exact CURRENT or HISTORICAL")
    if item.currentness == "CURRENT" and item.world_or_release_root_ref_or_null is None:
        raise NonEventAdapterIntegrityError("CURRENT objective fact requires exact world/release root binding")
    if (
        item.assertion_kind == "K4_ACTIVE_DURATIVE"
        and item.currentness == "CURRENT"
        and not item.negative_or_closure_refs
    ):
        raise NonEventAdapterIntegrityError(
            "CURRENT K4 durative fact requires exact termination/supersession/closure evidence"
        )
    _uses(item.producer_allowed_uses, "producer_allowed_uses")
    expected = semantic_hash(_staged_material(item))
    if item.item_hash != expected or item.item_id != f"NON_EVENT_ITEM:{expected}":
        raise NonEventAdapterIntegrityError("staged item identity/hash mismatch")


def make_non_event_staged_item(
    *,
    producer_object_ref: ExactRef | Mapping[str, str],
    producer_locator_ref: ExactRef | Mapping[str, str],
    canonical_producer_family: str,
    producer_semantic_class: str,
    producer_owner_authority_ref: AuthorityRef,
    producer_schema_ref: ExactRef | Mapping[str, str],
    temporal_form: str,
    assertion_kind: str,
    polarity: str,
    currentness: str,
    modality: str,
    proof_adjudication: str,
    valid_time_binding_ref: ExactRef | Mapping[str, str],
    decision_effective_time_ref: ExactRef | Mapping[str, str],
    objective_actor_binding_ref_or_null: ExactRef | Mapping[str, str] | None = None,
    objective_position_context_binding_ref_or_null: ExactRef | Mapping[str, str] | None = None,
    world_or_release_root_ref_or_null: ExactRef | Mapping[str, str] | None = None,
    source_evidence_refs: Sequence[ExactRef | Mapping[str, str]] = (),
    determinant_or_witness_refs: Sequence[ExactRef | Mapping[str, str]] = (),
    negative_or_closure_refs: Sequence[ExactRef | Mapping[str, str]] = (),
    producer_allowed_uses: Sequence[str] = ("REVIEW",),
) -> NonEventStagedItem:
    family = _text(canonical_producer_family, "canonical_producer_family")
    semantic_class = _text(producer_semantic_class, "producer_semantic_class")
    form = _text(temporal_form, "temporal_form")
    assertion = _text(assertion_kind, "assertion_kind")
    current = _text(currentness, "currentness")
    proof = _text(proof_adjudication, "proof_adjudication")
    draft = NonEventStagedItem(
        "PENDING",
        "0" * 64,
        STAGED_ITEM_SCHEMA,
        _ref(producer_object_ref, "producer_object_ref"),
        _ref(producer_locator_ref, "producer_locator_ref"),
        family,
        semantic_class,
        _authority(producer_owner_authority_ref, "producer_owner_authority_ref"),
        _ref(producer_schema_ref, "producer_schema_ref"),
        form,
        assertion,
        _text(polarity, "polarity"),
        current,
        _text(modality, "modality"),
        proof,
        _ref(valid_time_binding_ref, "valid_time_binding_ref"),
        _ref(decision_effective_time_ref, "decision_effective_time_ref"),
        _opt_ref(objective_actor_binding_ref_or_null, "objective_actor_binding_ref_or_null"),
        _opt_ref(
            objective_position_context_binding_ref_or_null,
            "objective_position_context_binding_ref_or_null",
        ),
        _opt_ref(world_or_release_root_ref_or_null, "world_or_release_root_ref_or_null"),
        _refs(source_evidence_refs, "source_evidence_refs"),
        _refs(determinant_or_witness_refs, "determinant_or_witness_refs"),
        _refs(negative_or_closure_refs, "negative_or_closure_refs"),
        _uses(producer_allowed_uses, "producer_allowed_uses"),
    )
    if family != CANONICAL_PRODUCER_FAMILY:
        raise NonEventAdapterIntegrityError("producer family is outside adopted generic D1-prime binding")
    if form not in ELIGIBLE_TEMPORAL_FORMS:
        raise NonEventAdapterIntegrityError("event/transition/history form is not generic non-event ingress")
    if assertion not in ELIGIBLE_ASSERTION_KINDS:
        raise NonEventAdapterIntegrityError("K3 or unknown assertion kind is not generic non-event ingress")
    if proof == UNKNOWN_NOT_PROVEN:
        raise NonEventAdapterIntegrityError("UNKNOWN_NOT_PROVEN is not a positive objective fact")
    if current not in CURRENTNESS_VALUES:
        raise NonEventAdapterIntegrityError("currentness must be exact CURRENT or HISTORICAL")
    if current == "CURRENT" and draft.world_or_release_root_ref_or_null is None:
        raise NonEventAdapterIntegrityError("CURRENT objective fact requires exact world/release root binding")
    if assertion == "K4_ACTIVE_DURATIVE" and current == "CURRENT" and not draft.negative_or_closure_refs:
        raise NonEventAdapterIntegrityError(
            "CURRENT K4 durative fact requires exact termination/supersession/closure evidence"
        )
    material = _staged_material(draft)
    h = semantic_hash(material)
    out = NonEventStagedItem(
        f"NON_EVENT_ITEM:{h}", h, draft.schema, draft.producer_object_ref,
        draft.producer_locator_ref, draft.canonical_producer_family,
        draft.producer_semantic_class, draft.producer_owner_authority_ref,
        draft.producer_schema_ref, draft.temporal_form, draft.assertion_kind,
        draft.polarity, draft.currentness, draft.modality, draft.proof_adjudication,
        draft.valid_time_binding_ref, draft.decision_effective_time_ref,
        draft.objective_actor_binding_ref_or_null,
        draft.objective_position_context_binding_ref_or_null,
        draft.world_or_release_root_ref_or_null, draft.source_evidence_refs,
        draft.determinant_or_witness_refs, draft.negative_or_closure_refs,
        draft.producer_allowed_uses,
    )
    _validate_staged_item(out)
    return out


@dataclass(frozen=True)
class NonEventPublicationEntry:
    entry_id: str
    entry_hash: str
    schema: str
    staged_item: NonEventStagedItem
    publication_authority_ref: AuthorityRef
    publication_allowed_uses: tuple[str, ...]

    @property
    def ref(self) -> ExactRef:
        return ExactRef("PREV3_OBJECTIVE_NON_EVENT_PUBLICATION_ENTRY", self.entry_id, self.entry_hash)


def _publication_entry_material(entry: NonEventPublicationEntry) -> dict[str, Any]:
    return {
        "schema": PUBLICATION_ENTRY_SCHEMA,
        "adapter_contract_id": ADAPTER_CONTRACT_ID,
        "staged_item_ref": entry.staged_item.ref.as_dict(),
        "producer_object_ref": entry.staged_item.producer_object_ref.as_dict(),
        "publication_authority_ref": entry.publication_authority_ref.as_dict(),
        "producer_allowed_uses": list(entry.staged_item.producer_allowed_uses),
        "publication_allowed_uses": list(entry.publication_allowed_uses),
    }


def _validate_publication_entry(entry: NonEventPublicationEntry) -> None:
    if not isinstance(entry, NonEventPublicationEntry) or entry.schema != PUBLICATION_ENTRY_SCHEMA:
        raise NonEventAdapterIntegrityError("publication entry type/schema mismatch")
    _validate_staged_item(entry.staged_item)
    _uses(entry.publication_allowed_uses, "publication_allowed_uses", non_event_serving_ceiling=True)
    if not set(entry.publication_allowed_uses) <= set(entry.staged_item.producer_allowed_uses):
        raise NonEventPermissionError("publication allowed uses widen producer permission")
    expected = semantic_hash(_publication_entry_material(entry))
    if entry.entry_hash != expected or entry.entry_id != f"NON_EVENT_PUB_ENTRY:{expected}":
        raise NonEventAdapterIntegrityError("publication entry identity/hash mismatch")


def make_non_event_publication_entry(
    item: NonEventStagedItem, *, publication_authority_ref: AuthorityRef,
    publication_allowed_uses: Sequence[str],
) -> NonEventPublicationEntry:
    _validate_staged_item(item)
    allowed = _uses(publication_allowed_uses, "publication_allowed_uses", non_event_serving_ceiling=True)
    if not set(allowed) <= set(item.producer_allowed_uses):
        raise NonEventPermissionError("publication allowed uses widen producer permission")
    draft = NonEventPublicationEntry(
        "PENDING", "0" * 64, PUBLICATION_ENTRY_SCHEMA, item,
        _authority(publication_authority_ref, "publication_authority_ref"), allowed,
    )
    h = semantic_hash(_publication_entry_material(draft))
    out = NonEventPublicationEntry(f"NON_EVENT_PUB_ENTRY:{h}", h, draft.schema, draft.staged_item,
                                   draft.publication_authority_ref, draft.publication_allowed_uses)
    _validate_publication_entry(out)
    return out


@dataclass(frozen=True)
class NonEventPublicationBundle:
    publication_id: str
    publication_hash: str
    schema: str
    entries: tuple[NonEventPublicationEntry, ...]

    @property
    def ref(self) -> ExactRef:
        return ExactRef("PREV3_OBJECTIVE_NON_EVENT_PUBLICATION_BUNDLE", self.publication_id, self.publication_hash)


def _publication_bundle_material(entries: Sequence[NonEventPublicationEntry]) -> dict[str, Any]:
    return {"schema": PUBLICATION_BUNDLE_SCHEMA, "adapter_contract_id": ADAPTER_CONTRACT_ID,
            "entry_refs": [entry.ref.as_dict() for entry in entries]}


def _validate_publication_bundle(bundle: NonEventPublicationBundle) -> None:
    if not isinstance(bundle, NonEventPublicationBundle) or bundle.schema != PUBLICATION_BUNDLE_SCHEMA:
        raise NonEventAdapterIntegrityError("publication bundle type/schema mismatch")
    if not bundle.entries:
        raise NonEventAdapterIntegrityError("publication bundle must contain at least one exact entry")
    for entry in bundle.entries:
        _validate_publication_entry(entry)
    expected = semantic_hash(_publication_bundle_material(bundle.entries))
    if bundle.publication_hash != expected or bundle.publication_id != f"NON_EVENT_PUB:{expected}":
        raise NonEventAdapterIntegrityError("publication bundle identity/hash mismatch")


def build_non_event_publication_bundle(entries: Sequence[NonEventPublicationEntry]) -> NonEventPublicationBundle:
    if isinstance(entries, (str, bytes)) or not isinstance(entries, Sequence) or not entries:
        raise NonEventAdapterIntegrityError("publication entries must be a non-empty sequence")
    normalized = tuple(sorted(entries, key=lambda entry: entry.entry_id))
    if len({entry.entry_id for entry in normalized}) != len(normalized):
        raise NonEventAdapterIntegrityError("duplicate publication entry")
    for entry in normalized:
        _validate_publication_entry(entry)
    h = semantic_hash(_publication_bundle_material(normalized))
    bundle = NonEventPublicationBundle(f"NON_EVENT_PUB:{h}", h, PUBLICATION_BUNDLE_SCHEMA, normalized)
    _validate_publication_bundle(bundle)
    return bundle


@dataclass(frozen=True)
class NonEventRepositoryBundle:
    repository_id: str
    repository_hash: str
    schema: str
    publication_bundle_ref: ExactRef
    entries: tuple[NonEventPublicationEntry, ...]

    @property
    def ref(self) -> ExactRef:
        return ExactRef("PREV3_OBJECTIVE_NON_EVENT_REPOSITORY", self.repository_id, self.repository_hash)


def exact_non_event_resolution_key(entry: NonEventPublicationEntry) -> str:
    _validate_publication_entry(entry)
    return semantic_hash({"producer_object_ref": entry.staged_item.producer_object_ref.as_dict(),
                          "producer_locator_ref": entry.staged_item.producer_locator_ref.as_dict(),
                          "publication_entry_ref": entry.ref.as_dict()})


def _repository_material(publication_ref: ExactRef, entries: Sequence[NonEventPublicationEntry]) -> dict[str, Any]:
    return {
        "schema": REPOSITORY_SCHEMA,
        "adapter_contract_id": ADAPTER_CONTRACT_ID,
        "publication_bundle_ref": publication_ref.as_dict(),
        "entries": [{"resolution_key": exact_non_event_resolution_key(entry),
                     "publication_entry_ref": entry.ref.as_dict(),
                     "producer_object_ref": entry.staged_item.producer_object_ref.as_dict(),
                     "producer_locator_ref": entry.staged_item.producer_locator_ref.as_dict()}
                    for entry in entries],
    }


def _validate_repository(repository: NonEventRepositoryBundle) -> None:
    if not isinstance(repository, NonEventRepositoryBundle) or repository.schema != REPOSITORY_SCHEMA:
        raise NonEventAdapterIntegrityError("repository type/schema mismatch")
    for entry in repository.entries:
        _validate_publication_entry(entry)
    keys = [exact_non_event_resolution_key(entry) for entry in repository.entries]
    if len(set(keys)) != len(keys):
        raise NonEventAdapterIntegrityError("repository contains ambiguous exact resolution key")
    expected = semantic_hash(_repository_material(repository.publication_bundle_ref, repository.entries))
    if repository.repository_hash != expected or repository.repository_id != f"NON_EVENT_REPO:{expected}":
        raise NonEventAdapterIntegrityError("repository identity/hash mismatch")


def build_non_event_repository_bundle(publication: NonEventPublicationBundle) -> NonEventRepositoryBundle:
    _validate_publication_bundle(publication)
    h = semantic_hash(_repository_material(publication.ref, publication.entries))
    repository = NonEventRepositoryBundle(f"NON_EVENT_REPO:{h}", h, REPOSITORY_SCHEMA,
                                          publication.ref, publication.entries)
    _validate_repository(repository)
    return repository


@dataclass(frozen=True)
class NonEventContextQueryItem:
    resolution_key: str
    requested_uses: tuple[str, ...]


def make_non_event_context_query_item(entry: NonEventPublicationEntry,
                                      requested_uses: Sequence[str]) -> NonEventContextQueryItem:
    return NonEventContextQueryItem(exact_non_event_resolution_key(entry),
                                    _uses(requested_uses, "requested_uses", non_event_serving_ceiling=True))


@dataclass(frozen=True)
class NonEventContextQuery:
    query_id: str
    query_hash: str
    schema: str
    items: tuple[NonEventContextQueryItem, ...]

    @property
    def ref(self) -> ExactRef:
        return ExactRef("PREV3_OBJECTIVE_NON_EVENT_CONTEXT_QUERY", self.query_id, self.query_hash)


def _query_material(items: Sequence[NonEventContextQueryItem]) -> dict[str, Any]:
    return {"schema": QUERY_SCHEMA, "adapter_contract_id": ADAPTER_CONTRACT_ID,
            "items": [{"resolution_key": item.resolution_key,
                       "requested_uses": list(item.requested_uses)} for item in items]}


def _validate_query(query: NonEventContextQuery) -> None:
    if not isinstance(query, NonEventContextQuery) or query.schema != QUERY_SCHEMA:
        raise NonEventAdapterIntegrityError("query type/schema mismatch")
    if len({item.resolution_key for item in query.items}) != len(query.items):
        raise NonEventAdapterIntegrityError("duplicate exact resolution key in query")
    for item in query.items:
        _hash_text(item.resolution_key, "resolution_key")
        _uses(item.requested_uses, "requested_uses", non_event_serving_ceiling=True)
    expected = semantic_hash(_query_material(query.items))
    if query.query_hash != expected or query.query_id != f"NON_EVENT_QUERY:{expected}":
        raise NonEventAdapterIntegrityError("query identity/hash mismatch")


def make_non_event_context_query(items: Sequence[NonEventContextQueryItem]) -> NonEventContextQuery:
    if isinstance(items, (str, bytes)) or not isinstance(items, Sequence):
        raise NonEventAdapterIntegrityError("query items must be a sequence")
    normalized = tuple(items)
    h = semantic_hash(_query_material(normalized))
    query = NonEventContextQuery(f"NON_EVENT_QUERY:{h}", h, QUERY_SCHEMA, normalized)
    _validate_query(query)
    return query


@dataclass(frozen=True)
class NonEventSelectionRecord:
    selection_id: str
    selection_hash: str
    schema: str
    resolution_key: str
    publication_entry_ref: ExactRef | None
    producer_object_ref: ExactRef | None
    producer_locator_ref: ExactRef | None
    producer_allowed_uses: tuple[str, ...]
    publication_allowed_uses: tuple[str, ...]
    resolver_allowed_uses: tuple[str, ...]
    decision: str
    reason: str

    @property
    def ref(self) -> ExactRef:
        return ExactRef("PREV3_OBJECTIVE_NON_EVENT_SELECTION_RECORD", self.selection_id, self.selection_hash)


def _selection_material(repository: NonEventRepositoryBundle, query: NonEventContextQuery,
                        item: NonEventContextQueryItem, entry: NonEventPublicationEntry | None,
                        *, resolver_allowed_uses: Sequence[str], decision: str, reason: str) -> dict[str, Any]:
    return {"schema": SELECTION_SCHEMA, "repository_ref": repository.ref.as_dict(),
            "query_ref": query.ref.as_dict(), "resolution_key": item.resolution_key,
            "requested_uses": list(item.requested_uses),
            "publication_entry_ref": entry.ref.as_dict() if entry else None,
            "producer_object_ref": entry.staged_item.producer_object_ref.as_dict() if entry else None,
            "producer_locator_ref": entry.staged_item.producer_locator_ref.as_dict() if entry else None,
            "producer_allowed_uses": list(entry.staged_item.producer_allowed_uses) if entry else [],
            "publication_allowed_uses": list(entry.publication_allowed_uses) if entry else [],
            "resolver_allowed_uses": list(resolver_allowed_uses), "decision": decision, "reason": reason}


def _make_selection(repository: NonEventRepositoryBundle, query: NonEventContextQuery,
                    item: NonEventContextQueryItem, entry: NonEventPublicationEntry | None,
                    *, resolver_allowed_uses: Sequence[str] = (), decision: str,
                    reason: str) -> NonEventSelectionRecord:
    resolver = _uses(resolver_allowed_uses, "resolver_allowed_uses", allow_empty=True,
                     non_event_serving_ceiling=True)
    h = semantic_hash(_selection_material(repository, query, item, entry,
                                          resolver_allowed_uses=resolver,
                                          decision=decision, reason=reason))
    return NonEventSelectionRecord(
        f"NON_EVENT_SEL:{h}", h, SELECTION_SCHEMA, item.resolution_key,
        entry.ref if entry else None,
        entry.staged_item.producer_object_ref if entry else None,
        entry.staged_item.producer_locator_ref if entry else None,
        entry.staged_item.producer_allowed_uses if entry else (),
        entry.publication_allowed_uses if entry else (), resolver, decision, reason,
    )


def _validate_selection(repository: NonEventRepositoryBundle, query: NonEventContextQuery,
                        selection: NonEventSelectionRecord) -> None:
    if not isinstance(selection, NonEventSelectionRecord) or selection.schema != SELECTION_SCHEMA:
        raise NonEventAdapterIntegrityError("selection record type/schema mismatch")
    _hash_text(selection.resolution_key, "selection.resolution_key")
    matches = [item for item in query.items if item.resolution_key == selection.resolution_key]
    if len(matches) != 1:
        raise NonEventAdapterIntegrityError("selection does not bind exactly one query item")
    query_item = matches[0]
    entry_matches = [entry for entry in repository.entries
                     if exact_non_event_resolution_key(entry) == selection.resolution_key]
    entry = entry_matches[0] if len(entry_matches) == 1 else None
    if selection.decision == "UNRESOLVED_EXACT_KEY":
        if entry is not None:
            raise NonEventAdapterIntegrityError("unresolved selection has an exact repository entry")
        expected_entry = None
    else:
        if entry is None:
            raise NonEventAdapterIntegrityError("resolved/denied selection lacks exact repository entry")
        expected_entry = entry
        if (selection.publication_entry_ref != entry.ref
                or selection.producer_object_ref != entry.staged_item.producer_object_ref
                or selection.producer_locator_ref != entry.staged_item.producer_locator_ref
                or selection.producer_allowed_uses != entry.staged_item.producer_allowed_uses
                or selection.publication_allowed_uses != entry.publication_allowed_uses):
            raise NonEventAdapterIntegrityError("selection changed exact producer/publication binding")
    resolver = _uses(selection.resolver_allowed_uses, "selection.resolver_allowed_uses",
                     allow_empty=True, non_event_serving_ceiling=True)
    if selection.decision == "SELECTED":
        if not resolver or resolver != query_item.requested_uses or expected_entry is None:
            raise NonEventAdapterIntegrityError("SELECTED record does not preserve exact requested use/entry")
        if not set(resolver) <= set(expected_entry.publication_allowed_uses):
            raise NonEventPermissionError("selection widens publication permission")
        if not set(expected_entry.publication_allowed_uses) <= set(expected_entry.staged_item.producer_allowed_uses):
            raise NonEventPermissionError("publication widens producer permission")
    elif resolver:
        raise NonEventAdapterIntegrityError("non-selected record may not carry resolver permission")
    expected = semantic_hash(_selection_material(repository, query, query_item, expected_entry,
                                                 resolver_allowed_uses=resolver,
                                                 decision=selection.decision,
                                                 reason=selection.reason))
    if selection.selection_hash != expected or selection.selection_id != f"NON_EVENT_SEL:{expected}":
        raise NonEventAdapterIntegrityError("selection record identity/hash mismatch")


def _expected_resolution_state(selections: Sequence[NonEventSelectionRecord]) -> tuple[str, tuple[str, ...]]:
    unresolved = tuple(selection.resolution_key for selection in selections
                       if selection.decision == "UNRESOLVED_EXACT_KEY")
    selected = any(selection.decision == "SELECTED" for selection in selections)
    denied = any(selection.decision == "PERMISSION_DENIED" for selection in selections)
    if unresolved and selected:
        return "RESOLUTION_PARTIAL_TYPED_DEFERRED", unresolved
    if unresolved:
        return "RESOLUTION_MISSING_REQUIRED_AUTHORITY", unresolved
    if denied and selected:
        return "RESOLUTION_PARTIAL_TYPED_DEFERRED", unresolved
    if denied:
        return "RESOLUTION_DENIED_OR_NOT_APPLICABLE", unresolved
    return "RESOLUTION_COMPLETE", unresolved


@dataclass(frozen=True)
class NonEventResolutionReceipt:
    receipt_id: str
    receipt_hash: str
    schema: str
    result_state: str
    repository_ref: ExactRef
    query_ref: ExactRef
    selection_record_refs: tuple[ExactRef, ...]
    unresolved_keys: tuple[str, ...]
    replay_input_digest: str

    @property
    def ref(self) -> ExactRef:
        return ExactRef("PREV3_OBJECTIVE_NON_EVENT_RESOLUTION_RECEIPT", self.receipt_id, self.receipt_hash)


@dataclass(frozen=True)
class NonEventResolutionResult:
    selections: tuple[NonEventSelectionRecord, ...]
    receipt: NonEventResolutionReceipt


def _resolution_receipt_material(result_state: str, repository: NonEventRepositoryBundle,
                                 query: NonEventContextQuery,
                                 selections: Sequence[NonEventSelectionRecord],
                                 unresolved_keys: Sequence[str], replay_input_digest: str) -> dict[str, Any]:
    return {"schema": RESOLUTION_RECEIPT_SCHEMA, "adapter_contract_id": ADAPTER_CONTRACT_ID,
            "result_state": result_state, "repository_ref": repository.ref.as_dict(),
            "query_ref": query.ref.as_dict(),
            "selection_record_refs": [selection.ref.as_dict() for selection in selections],
            "unresolved_keys": list(unresolved_keys), "replay_input_digest": replay_input_digest}


def _validate_resolution(repository: NonEventRepositoryBundle, query: NonEventContextQuery,
                         result: NonEventResolutionResult) -> None:
    _validate_repository(repository)
    _validate_query(query)
    if not isinstance(result, NonEventResolutionResult):
        raise NonEventAdapterIntegrityError("resolution result type mismatch")
    receipt = result.receipt
    if not isinstance(receipt, NonEventResolutionReceipt) or receipt.schema != RESOLUTION_RECEIPT_SCHEMA:
        raise NonEventAdapterIntegrityError("resolution receipt type/schema mismatch")
    if receipt.repository_ref != repository.ref or receipt.query_ref != query.ref:
        raise NonEventAdapterIntegrityError("resolution receipt repository/query binding mismatch")
    if tuple(selection.ref for selection in result.selections) != receipt.selection_record_refs:
        raise NonEventAdapterIntegrityError("resolution selection closure mismatch")
    for selection in result.selections:
        _validate_selection(repository, query, selection)
    expected_state, expected_unresolved = _expected_resolution_state(result.selections)
    if receipt.result_state != expected_state or receipt.unresolved_keys != expected_unresolved:
        raise NonEventAdapterIntegrityError("resolution result-state/unresolved closure mismatch")
    replay = semantic_hash({"repository_ref": repository.ref.as_dict(), "query_ref": query.ref.as_dict(),
                            "adapter_contract_id": ADAPTER_CONTRACT_ID})
    if receipt.replay_input_digest != replay:
        raise NonEventAdapterIntegrityError("resolution replay digest mismatch")
    expected = semantic_hash(_resolution_receipt_material(receipt.result_state, repository, query,
                                                          result.selections, receipt.unresolved_keys, replay))
    if receipt.receipt_hash != expected or receipt.receipt_id != f"NON_EVENT_RES:{expected}":
        raise NonEventAdapterIntegrityError("resolution receipt identity/hash mismatch")


def resolve_non_event(repository: NonEventRepositoryBundle,
                      query: NonEventContextQuery) -> NonEventResolutionResult:
    _validate_repository(repository)
    _validate_query(query)
    by_key = {exact_non_event_resolution_key(entry): entry for entry in repository.entries}
    selections: list[NonEventSelectionRecord] = []
    unresolved: list[str] = []
    for query_item in query.items:
        entry = by_key.get(query_item.resolution_key)
        if entry is None:
            unresolved.append(query_item.resolution_key)
            selections.append(_make_selection(repository, query, query_item, None,
                                              decision="UNRESOLVED_EXACT_KEY",
                                              reason="exact immutable resolution key absent; no fuzzy/latest repair"))
            continue
        _validate_publication_entry(entry)
        requested = set(query_item.requested_uses)
        if not requested <= set(entry.staged_item.producer_allowed_uses):
            selections.append(_make_selection(repository, query, query_item, entry,
                                              decision="PERMISSION_DENIED",
                                              reason="requested use exceeds producer permission ceiling"))
            continue
        if not requested <= set(entry.publication_allowed_uses):
            selections.append(_make_selection(repository, query, query_item, entry,
                                              decision="PERMISSION_DENIED",
                                              reason="requested use exceeds publication permission ceiling"))
            continue
        selections.append(_make_selection(repository, query, query_item, entry,
                                          resolver_allowed_uses=query_item.requested_uses,
                                          decision="SELECTED",
                                          reason="exact producer/publication/resolver item-wise permission subsets verified"))
    state, expected_unresolved = _expected_resolution_state(selections)
    if tuple(unresolved) != expected_unresolved:
        raise NonEventAdapterIntegrityError("internal unresolved-key accounting drift")
    replay = semantic_hash({"repository_ref": repository.ref.as_dict(), "query_ref": query.ref.as_dict(),
                            "adapter_contract_id": ADAPTER_CONTRACT_ID})
    h = semantic_hash(_resolution_receipt_material(state, repository, query, selections,
                                                   unresolved, replay))
    receipt = NonEventResolutionReceipt(f"NON_EVENT_RES:{h}", h, RESOLUTION_RECEIPT_SCHEMA,
                                        state, repository.ref, query.ref,
                                        tuple(selection.ref for selection in selections),
                                        tuple(unresolved), replay)
    result = NonEventResolutionResult(tuple(selections), receipt)
    _validate_resolution(repository, query, result)
    return result


@dataclass(frozen=True)
class ObjectiveNonEventServingReceipt:
    schema_id: str
    schema_version: str
    receipt_id: str
    receipt_content_hash: str
    producer_object_ref: ExactRef
    producer_locator_ref: ExactRef
    canonical_producer_family: str
    producer_semantic_class: str
    producer_owner_authority_ref: AuthorityRef
    producer_schema_ref: ExactRef
    temporal_form: str
    assertion_kind: str
    polarity: str
    currentness: str
    modality: str
    proof_adjudication: str
    valid_time_binding_ref: ExactRef
    decision_effective_time_ref: ExactRef
    objective_actor_binding_ref_or_null: ExactRef | None
    objective_position_context_binding_ref_or_null: ExactRef | None
    world_or_release_root_ref_or_null: ExactRef | None
    source_evidence_refs: tuple[ExactRef, ...]
    determinant_or_witness_refs: tuple[ExactRef, ...]
    negative_or_closure_refs: tuple[ExactRef, ...]
    producer_allowed_uses: tuple[str, ...]
    publication_allowed_uses: tuple[str, ...]
    resolver_allowed_uses: tuple[str, ...]
    publication_bundle_ref: ExactRef
    repository_ref: ExactRef
    context_query_ref: ExactRef
    resolution_receipt_ref: ExactRef
    selection_record_ref: ExactRef
    currentness_receipt_ref_or_null: ExactRef | None
    v3_transition_owner_declaration_ref_or_null: ExactRef | None
    structural_peer_use_receipt_ref_or_null: ExactRef | None
    ingress_effect: str
    actor_state_effect: bool

    @property
    def ref(self) -> ExactRef:
        return ExactRef(SERVING_RECEIPT_SCHEMA_ID, self.receipt_id, self.receipt_content_hash)


def _serving_material(receipt: ObjectiveNonEventServingReceipt) -> dict[str, Any]:
    return {
        "schema_id": SERVING_RECEIPT_SCHEMA_ID,
        "schema_version": SERVING_RECEIPT_SCHEMA_VERSION,
        "adapter_contract_id": ADAPTER_CONTRACT_ID,
        "producer_object_ref": receipt.producer_object_ref.as_dict(),
        "producer_locator_ref": receipt.producer_locator_ref.as_dict(),
        "canonical_producer_family": receipt.canonical_producer_family,
        "producer_semantic_class": receipt.producer_semantic_class,
        "producer_owner_authority_ref": receipt.producer_owner_authority_ref.as_dict(),
        "producer_schema_ref": receipt.producer_schema_ref.as_dict(),
        "temporal_form": receipt.temporal_form,
        "assertion_kind": receipt.assertion_kind,
        "polarity": receipt.polarity,
        "currentness": receipt.currentness,
        "modality": receipt.modality,
        "proof_adjudication": receipt.proof_adjudication,
        "valid_time_binding_ref": receipt.valid_time_binding_ref.as_dict(),
        "decision_effective_time_ref": receipt.decision_effective_time_ref.as_dict(),
        "objective_actor_binding_ref_or_null": _ref_dict(receipt.objective_actor_binding_ref_or_null),
        "objective_position_context_binding_ref_or_null": _ref_dict(receipt.objective_position_context_binding_ref_or_null),
        "world_or_release_root_ref_or_null": _ref_dict(receipt.world_or_release_root_ref_or_null),
        "source_evidence_refs": [r.as_dict() for r in receipt.source_evidence_refs],
        "determinant_or_witness_refs": [r.as_dict() for r in receipt.determinant_or_witness_refs],
        "negative_or_closure_refs": [r.as_dict() for r in receipt.negative_or_closure_refs],
        "producer_allowed_uses": list(receipt.producer_allowed_uses),
        "publication_allowed_uses": list(receipt.publication_allowed_uses),
        "resolver_allowed_uses": list(receipt.resolver_allowed_uses),
        "publication_bundle_ref": receipt.publication_bundle_ref.as_dict(),
        "repository_ref": receipt.repository_ref.as_dict(),
        "context_query_ref": receipt.context_query_ref.as_dict(),
        "resolution_receipt_ref": receipt.resolution_receipt_ref.as_dict(),
        "selection_record_ref": receipt.selection_record_ref.as_dict(),
        "currentness_receipt_ref_or_null": _ref_dict(receipt.currentness_receipt_ref_or_null),
        "v3_transition_owner_declaration_ref_or_null": _ref_dict(receipt.v3_transition_owner_declaration_ref_or_null),
        "structural_peer_use_receipt_ref_or_null": _ref_dict(receipt.structural_peer_use_receipt_ref_or_null),
        "ingress_effect": INGRESS_EFFECT,
        "actor_state_effect": False,
    }


def validate_objective_non_event_serving_receipt(receipt: ObjectiveNonEventServingReceipt) -> ObjectiveNonEventServingReceipt:
    if not isinstance(receipt, ObjectiveNonEventServingReceipt):
        raise NonEventAdapterIntegrityError("serving receipt type mismatch")
    if receipt.schema_id != SERVING_RECEIPT_SCHEMA_ID or receipt.schema_version != SERVING_RECEIPT_SCHEMA_VERSION:
        raise NonEventAdapterIntegrityError("serving receipt schema mismatch")
    if receipt.temporal_form not in ELIGIBLE_TEMPORAL_FORMS:
        raise NonEventAdapterIntegrityError("serving receipt event laundering detected")
    if receipt.assertion_kind not in ELIGIBLE_ASSERTION_KINDS:
        raise NonEventAdapterIntegrityError("serving receipt K3/unknown assertion rejected")
    if receipt.canonical_producer_family != CANONICAL_PRODUCER_FAMILY:
        raise NonEventAdapterIntegrityError("serving receipt producer family mismatch")
    if receipt.proof_adjudication == UNKNOWN_NOT_PROVEN:
        raise NonEventAdapterIntegrityError("UNKNOWN_NOT_PROVEN cannot be served as fact")
    if receipt.currentness == "CURRENT":
        if receipt.world_or_release_root_ref_or_null is None:
            raise NonEventAdapterIntegrityError("CURRENT serving receipt lacks world/release root")
        if receipt.currentness_receipt_ref_or_null is None:
            raise NonEventAdapterIntegrityError("CURRENT serving receipt lacks exact currentness receipt")
    _uses(receipt.producer_allowed_uses, "receipt.producer_allowed_uses")
    _uses(receipt.publication_allowed_uses, "receipt.publication_allowed_uses", non_event_serving_ceiling=True)
    _uses(receipt.resolver_allowed_uses, "receipt.resolver_allowed_uses", non_event_serving_ceiling=True)
    if not set(receipt.resolver_allowed_uses) <= set(receipt.publication_allowed_uses):
        raise NonEventPermissionError("resolver uses widen publication permission")
    if not set(receipt.publication_allowed_uses) <= set(receipt.producer_allowed_uses):
        raise NonEventPermissionError("publication uses widen producer permission")
    if receipt.actor_state_effect is not False:
        raise NonEventAdapterIntegrityError("non-event serving receipt may not have person-state effect")
    if receipt.ingress_effect != INGRESS_EFFECT:
        raise NonEventAdapterIntegrityError("non-event ingress effect exceeds structural eligibility")
    expected = semantic_hash(_serving_material(receipt))
    if receipt.receipt_content_hash != expected or receipt.receipt_id != f"NON_EVENT_SERVE:{expected}":
        raise NonEventAdapterIntegrityError("serving receipt identity/hash mismatch")
    return receipt


def make_objective_non_event_serving_receipt(
    publication: NonEventPublicationBundle,
    repository: NonEventRepositoryBundle,
    query: NonEventContextQuery,
    resolution: NonEventResolutionResult,
    *,
    resolution_key: str,
    currentness_receipt_ref_or_null: ExactRef | Mapping[str, str] | None,
    v3_transition_owner_declaration_ref_or_null: ExactRef | Mapping[str, str] | None = None,
    structural_peer_use_receipt_ref_or_null: ExactRef | Mapping[str, str] | None = None,
) -> ObjectiveNonEventServingReceipt:
    _validate_publication_bundle(publication)
    _validate_repository(repository)
    _validate_query(query)
    _validate_resolution(repository, query, resolution)
    if repository.publication_bundle_ref != publication.ref:
        raise NonEventAdapterIntegrityError("repository does not bind exact publication bundle")
    if resolution.receipt.result_state != "RESOLUTION_COMPLETE":
        raise NonEventAdapterIntegrityError("serving receipt requires complete exact resolution; partial/denied/unresolved fails closed")
    key = _hash_text(resolution_key, "resolution_key")
    selection_matches = [selection for selection in resolution.selections
                         if selection.resolution_key == key and selection.decision == "SELECTED"]
    if len(selection_matches) != 1:
        raise NonEventAdapterIntegrityError("serving receipt requires exactly one selected resolution key")
    selection = selection_matches[0]
    entry_matches = [entry for entry in repository.entries if exact_non_event_resolution_key(entry) == key]
    if len(entry_matches) != 1:
        raise NonEventAdapterIntegrityError("selected resolution key is absent or ambiguous in repository")
    entry = entry_matches[0]
    item = entry.staged_item
    _validate_publication_entry(entry)
    if (selection.publication_entry_ref != entry.ref
            or selection.producer_object_ref != item.producer_object_ref
            or selection.producer_locator_ref != item.producer_locator_ref
            or selection.producer_allowed_uses != item.producer_allowed_uses
            or selection.publication_allowed_uses != entry.publication_allowed_uses):
        raise NonEventAdapterIntegrityError("selection changed exact producer/publication identity")
    if not set(selection.resolver_allowed_uses) <= set(entry.publication_allowed_uses):
        raise NonEventPermissionError("resolver uses widen publication permission")
    if not set(entry.publication_allowed_uses) <= set(item.producer_allowed_uses):
        raise NonEventPermissionError("publication uses widen producer permission")
    currentness_ref = _opt_ref(currentness_receipt_ref_or_null, "currentness_receipt_ref_or_null")
    if item.currentness == "CURRENT" and currentness_ref is None:
        raise NonEventAdapterIntegrityError("CURRENT serving requires exact currentness receipt")
    transition_ref = _opt_ref(v3_transition_owner_declaration_ref_or_null,
                              "v3_transition_owner_declaration_ref_or_null")
    peer_ref = _opt_ref(structural_peer_use_receipt_ref_or_null,
                        "structural_peer_use_receipt_ref_or_null")
    provisional = ObjectiveNonEventServingReceipt(
        SERVING_RECEIPT_SCHEMA_ID, SERVING_RECEIPT_SCHEMA_VERSION, "PENDING", "0" * 64,
        item.producer_object_ref, item.producer_locator_ref, item.canonical_producer_family,
        item.producer_semantic_class, item.producer_owner_authority_ref, item.producer_schema_ref,
        item.temporal_form, item.assertion_kind, item.polarity, item.currentness, item.modality,
        item.proof_adjudication, item.valid_time_binding_ref, item.decision_effective_time_ref,
        item.objective_actor_binding_ref_or_null, item.objective_position_context_binding_ref_or_null,
        item.world_or_release_root_ref_or_null, item.source_evidence_refs, item.determinant_or_witness_refs,
        item.negative_or_closure_refs, item.producer_allowed_uses, entry.publication_allowed_uses,
        selection.resolver_allowed_uses, publication.ref, repository.ref, query.ref,
        resolution.receipt.ref, selection.ref, currentness_ref, transition_ref, peer_ref,
        INGRESS_EFFECT, False,
    )
    h = semantic_hash(_serving_material(provisional))
    receipt = ObjectiveNonEventServingReceipt(
        provisional.schema_id, provisional.schema_version, f"NON_EVENT_SERVE:{h}", h,
        provisional.producer_object_ref, provisional.producer_locator_ref,
        provisional.canonical_producer_family, provisional.producer_semantic_class,
        provisional.producer_owner_authority_ref, provisional.producer_schema_ref,
        provisional.temporal_form, provisional.assertion_kind, provisional.polarity,
        provisional.currentness, provisional.modality, provisional.proof_adjudication,
        provisional.valid_time_binding_ref, provisional.decision_effective_time_ref,
        provisional.objective_actor_binding_ref_or_null,
        provisional.objective_position_context_binding_ref_or_null,
        provisional.world_or_release_root_ref_or_null, provisional.source_evidence_refs,
        provisional.determinant_or_witness_refs, provisional.negative_or_closure_refs,
        provisional.producer_allowed_uses, provisional.publication_allowed_uses,
        provisional.resolver_allowed_uses, provisional.publication_bundle_ref,
        provisional.repository_ref, provisional.context_query_ref,
        provisional.resolution_receipt_ref, provisional.selection_record_ref,
        provisional.currentness_receipt_ref_or_null,
        provisional.v3_transition_owner_declaration_ref_or_null,
        provisional.structural_peer_use_receipt_ref_or_null, provisional.ingress_effect, False,
    )
    return validate_objective_non_event_serving_receipt(receipt)
