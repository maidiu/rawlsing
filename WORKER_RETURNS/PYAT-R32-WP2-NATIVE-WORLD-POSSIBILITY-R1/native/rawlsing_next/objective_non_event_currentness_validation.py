from __future__ import annotations

from typing import Mapping

from rawlsing_next import objective_non_event_publication_serving_adapter_legacy as legacy
from rawlsing_next.m4_v557_v558_publication_repository import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next.objective_non_event_currentness_contract import (
    CONTRACT_REF,
    RECEIPT_SCHEMA,
    STATES,
    ObjectiveNonEventCurrentnessReceipt,
    receipt_material,
    seal_receipt,
)


def selected_current_item(repository, query, resolution, resolution_key):
    legacy._validate_repository(repository)
    legacy._validate_query(query)
    legacy._validate_resolution(repository, query, resolution)
    if resolution.receipt.result_state != "RESOLUTION_COMPLETE":
        raise legacy.NonEventAdapterIntegrityError("currentness requires complete D05 resolution")
    key = legacy._hash_text(resolution_key, "resolution_key")
    selections = [s for s in resolution.selections if s.resolution_key == key and s.decision == "SELECTED"]
    entries = [e for e in repository.entries if legacy.exact_non_event_resolution_key(e) == key]
    if len(selections) != 1 or len(entries) != 1:
        raise legacy.NonEventAdapterIntegrityError("currentness requires one exact selected D05 item")
    item = entries[0].staged_item
    if selections[0].producer_object_ref != item.producer_object_ref:
        raise legacy.NonEventAdapterIntegrityError("currentness producer binding mismatch")
    if item.currentness != "CURRENT" or item.world_or_release_root_ref_or_null is None:
        raise legacy.NonEventAdapterIntegrityError("D05 currentness requires CURRENT item and world root")
    return key, selections[0], item


def make_currentness_receipt(repository, query, resolution, *, resolution_key: str, state: str,
                             authority_ref: AuthorityRef,
                             structural_currentness_basis_ref: ExactRef | Mapping[str, str]):
    _, selection, item = selected_current_item(repository, query, resolution, resolution_key)
    state_value = legacy._text(state, "currentness.state")
    if state_value not in STATES:
        raise legacy.NonEventAdapterIntegrityError("unknown D05 currentness state")
    authority = legacy._authority(authority_ref, "currentness.authority_ref")
    basis = legacy._ref(structural_currentness_basis_ref, "currentness.structural_currentness_basis_ref")
    draft = ObjectiveNonEventCurrentnessReceipt(
        "PENDING", "0" * 64, RECEIPT_SCHEMA, CONTRACT_REF, state_value, authority, basis,
        item.decision_effective_time_ref, resolution.receipt.ref, selection.ref,
        item.producer_object_ref, item.world_or_release_root_ref_or_null,
    )
    return seal_receipt(draft)


def validate_currentness_receipt(receipt, repository, query, resolution, *, resolution_key: str,
                                 expected_authority_ref: AuthorityRef,
                                 expected_structural_currentness_basis_ref: ExactRef | Mapping[str, str]):
    if not isinstance(receipt, ObjectiveNonEventCurrentnessReceipt):
        raise legacy.NonEventAdapterIntegrityError("CURRENT service requires actual D05 currentness receipt object")
    if receipt.schema != RECEIPT_SCHEMA or receipt.compatibility_contract_ref != CONTRACT_REF:
        raise legacy.NonEventAdapterIntegrityError("D05 currentness receipt contract/schema mismatch")
    if receipt.state not in STATES:
        raise legacy.NonEventAdapterIntegrityError("unknown D05 currentness state")
    h = semantic_hash(receipt_material(receipt))
    if receipt.receipt_hash != h or receipt.receipt_id != f"D05CUR:{h}":
        raise legacy.NonEventAdapterIntegrityError("D05 currentness receipt identity/hash mismatch")
    _, selection, item = selected_current_item(repository, query, resolution, resolution_key)
    expected_authority = legacy._authority(expected_authority_ref, "expected_currentness_authority_ref")
    expected_basis = legacy._ref(expected_structural_currentness_basis_ref, "expected_structural_currentness_basis_ref")
    actual = (receipt.non_event_resolution_receipt_ref, receipt.selection_record_ref,
              receipt.producer_object_ref, receipt.world_or_release_root_ref,
              receipt.decision_effective_time_ref, receipt.authority_ref,
              receipt.structural_currentness_basis_ref)
    expected = (resolution.receipt.ref, selection.ref, item.producer_object_ref,
                item.world_or_release_root_ref_or_null, item.decision_effective_time_ref,
                expected_authority, expected_basis)
    if actual != expected:
        raise legacy.NonEventAdapterIntegrityError("D05 currentness binding tuple mismatch")
    if receipt.state != "CURRENT":
        raise legacy.NonEventAdapterIntegrityError(f"D05 currentness state is {receipt.state}, not CURRENT")
    return receipt
