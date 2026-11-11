from __future__ import annotations

from typing import Mapping

from rawlsing_next import objective_non_event_publication_serving_adapter_legacy as legacy
from rawlsing_next.objective_non_event_publication_serving_adapter_legacy import *  # noqa: F401,F403
from rawlsing_next.m4_v557_v558_publication_repository import AuthorityRef, ExactRef
from rawlsing_next.objective_non_event_currentness_contract import ObjectiveNonEventCurrentnessReceipt
from rawlsing_next.objective_non_event_currentness_validation import make_currentness_receipt, validate_currentness_receipt

make_objective_non_event_currentness_receipt = make_currentness_receipt
validate_objective_non_event_currentness_receipt = validate_currentness_receipt


def __getattr__(name):
    return getattr(legacy, name)


def validate_objective_non_event_serving_receipt(
    receipt, *, currentness_receipt_or_null=None, repository=None, query=None,
    resolution=None, resolution_key=None, expected_currentness_authority_ref=None,
    expected_structural_currentness_basis_ref=None,
):
    legacy.validate_objective_non_event_serving_receipt(receipt)
    if receipt.currentness == "CURRENT":
        required = (
            currentness_receipt_or_null, repository, query, resolution, resolution_key,
            expected_currentness_authority_ref, expected_structural_currentness_basis_ref,
        )
        if any(value is None for value in required):
            raise NonEventAdapterIntegrityError(
                "CURRENT serving validation requires actual D05 currentness object and exact validation context"
            )
        currentness = validate_currentness_receipt(
            currentness_receipt_or_null, repository, query, resolution,
            resolution_key=resolution_key,
            expected_authority_ref=expected_currentness_authority_ref,
            expected_structural_currentness_basis_ref=expected_structural_currentness_basis_ref,
        )
        if receipt.currentness_receipt_ref_or_null != currentness.ref:
            raise NonEventAdapterIntegrityError("serving/currentness receipt binding mismatch")
    elif currentness_receipt_or_null is not None or receipt.currentness_receipt_ref_or_null is not None:
        raise NonEventAdapterIntegrityError("HISTORICAL serving may not carry D05 CURRENT currentness")
    return receipt


def make_objective_non_event_serving_receipt(
    publication, repository, query, resolution, *, resolution_key: str,
    currentness_receipt_or_null: ObjectiveNonEventCurrentnessReceipt | None = None,
    currentness_authority_ref_or_null: AuthorityRef | None = None,
    structural_currentness_basis_ref_or_null: ExactRef | Mapping[str, str] | None = None,
    currentness_receipt_ref_or_null=None,
    v3_transition_owner_declaration_ref_or_null=None,
    structural_peer_use_receipt_ref_or_null=None,
):
    if currentness_receipt_ref_or_null is not None:
        raise NonEventAdapterIntegrityError("ref-only currentness input is not accepted")
    if currentness_receipt_or_null is not None and not isinstance(
        currentness_receipt_or_null, ObjectiveNonEventCurrentnessReceipt
    ):
        raise NonEventAdapterIntegrityError("currentness input must be the actual D05 receipt object")
    current_ref = currentness_receipt_or_null.ref if currentness_receipt_or_null is not None else None
    receipt = legacy.make_objective_non_event_serving_receipt(
        publication, repository, query, resolution,
        resolution_key=resolution_key,
        currentness_receipt_ref_or_null=current_ref,
        v3_transition_owner_declaration_ref_or_null=v3_transition_owner_declaration_ref_or_null,
        structural_peer_use_receipt_ref_or_null=structural_peer_use_receipt_ref_or_null,
    )
    if receipt.currentness == "CURRENT":
        if currentness_authority_ref_or_null is None or structural_currentness_basis_ref_or_null is None:
            raise NonEventAdapterIntegrityError("CURRENT serving requires exact currentness authority and basis")
    return validate_objective_non_event_serving_receipt(
        receipt,
        currentness_receipt_or_null=currentness_receipt_or_null,
        repository=repository,
        query=query,
        resolution=resolution,
        resolution_key=resolution_key,
        expected_currentness_authority_ref=currentness_authority_ref_or_null,
        expected_structural_currentness_basis_ref=structural_currentness_basis_ref_or_null,
    )
