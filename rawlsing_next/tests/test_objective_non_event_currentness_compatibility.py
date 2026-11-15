from dataclasses import replace

import pytest

from rawlsing_next.objective_non_event_publication_serving_adapter import (
    NonEventAdapterIntegrityError,
    make_objective_non_event_currentness_receipt,
    make_objective_non_event_serving_receipt,
    validate_objective_non_event_currentness_receipt,
)
from rawlsing_next.tests.test_objective_non_event_publication_serving_adapter import _auth, _chain, _ref


@pytest.mark.parametrize("state", ("STALE", "REFRESH_REQUIRED", "INVALID"))
def test_noncurrent_states_do_not_support_current_service(state):
    _, publication, repository, query_item, query, resolution = _chain(f"state-{state}")
    authority = _auth("currentness")
    basis = _ref("CURRENTNESS_BASIS", "basis")
    currentness = make_objective_non_event_currentness_receipt(
        repository, query, resolution, resolution_key=query_item.resolution_key,
        state=state, authority_ref=authority, structural_currentness_basis_ref=basis,
    )
    with pytest.raises(NonEventAdapterIntegrityError, match="not CURRENT"):
        make_objective_non_event_serving_receipt(
            publication, repository, query, resolution,
            resolution_key=query_item.resolution_key,
            currentness_receipt_or_null=currentness,
            currentness_authority_ref_or_null=authority,
            structural_currentness_basis_ref_or_null=basis,
        )


def test_authority_and_basis_mismatch_are_rejected():
    _, _, repository, query_item, query, resolution = _chain("mismatch")
    authority = _auth("currentness")
    basis = _ref("CURRENTNESS_BASIS", "basis")
    currentness = make_objective_non_event_currentness_receipt(
        repository, query, resolution, resolution_key=query_item.resolution_key,
        state="CURRENT", authority_ref=authority, structural_currentness_basis_ref=basis,
    )
    with pytest.raises(NonEventAdapterIntegrityError, match="binding tuple"):
        validate_objective_non_event_currentness_receipt(
            currentness, repository, query, resolution,
            resolution_key=query_item.resolution_key,
            expected_authority_ref=_auth("other"),
            expected_structural_currentness_basis_ref=basis,
        )
    with pytest.raises(NonEventAdapterIntegrityError, match="binding tuple"):
        validate_objective_non_event_currentness_receipt(
            currentness, repository, query, resolution,
            resolution_key=query_item.resolution_key,
            expected_authority_ref=authority,
            expected_structural_currentness_basis_ref=_ref("CURRENTNESS_BASIS", "other"),
        )


def test_hash_and_resolution_binding_changes_are_rejected():
    _, _, repository, query_item, query, resolution = _chain("tamper")
    authority = _auth("currentness")
    basis = _ref("CURRENTNESS_BASIS", "basis")
    currentness = make_objective_non_event_currentness_receipt(
        repository, query, resolution, resolution_key=query_item.resolution_key,
        state="CURRENT", authority_ref=authority, structural_currentness_basis_ref=basis,
    )
    with pytest.raises(NonEventAdapterIntegrityError, match="identity/hash"):
        validate_objective_non_event_currentness_receipt(
            replace(currentness, receipt_hash="0" * 64), repository, query, resolution,
            resolution_key=query_item.resolution_key,
            expected_authority_ref=authority,
            expected_structural_currentness_basis_ref=basis,
        )
    other = _ref("PREV3_OBJECTIVE_NON_EVENT_RESOLUTION_RECEIPT", "other")
    with pytest.raises(NonEventAdapterIntegrityError):
        validate_objective_non_event_currentness_receipt(
            replace(currentness, non_event_resolution_receipt_ref=other), repository, query, resolution,
            resolution_key=query_item.resolution_key,
            expected_authority_ref=authority,
            expected_structural_currentness_basis_ref=basis,
        )
