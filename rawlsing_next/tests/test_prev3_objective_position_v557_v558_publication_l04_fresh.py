from dataclasses import replace

import pytest

from rawlsing_next.m4_v557_v558_publication_repository import (
    ContextQueryItem,
    M4IntegrityError,
    ReferenceClassError,
    V557PublicationEntry,
    build_v557_publication_bundle,
    exact_resolution_key,
    make_context_query,
)
from rawlsing_next.prev3_objective_position_v557_v558_publication import (
    M4_CONTEXT_USE,
    ObjectivePositionPublicationError,
    SOURCE_DOMAIN_USE,
    make_bound_objective_position_context_query,
    require_bound_objective_position_context_query,
    resolve_bound_objective_position_context,
    validate_objective_position_publication_carrier,
)
from rawlsing_next.tests.test_prev3_objective_position_v557_v558_publication import _carrier, _r


def test_l04_f24_exact_bound_query_fails_closed_without_exact_dependency_bodies():
    carrier = _carrier()
    query = make_bound_objective_position_context_query(
        carrier, requested_source_domain_use=SOURCE_DOMAIN_USE
    )
    result = resolve_bound_objective_position_context(carrier, query)
    assert result.receipt.result_state == "RESOLUTION_INTEGRITY_FAILED"
    assert len(result.selection_records) == 1
    assert result.selection_records[0].decision == "INTEGRITY_FAILURE"
    assert result.resolved_entries == ()


def test_l04_f25_wrong_domain_binding_ref_is_rejected():
    carrier = _carrier()
    item = ContextQueryItem(
        exact_resolution_key(carrier.root_entry.locator), (M4_CONTEXT_USE,)
    )
    fake = _r(
        "PREV3_OBJECTIVE_POSITION_DOMAIN_USE_BINDING",
        "PREV3POSUSE:" + "8" * 64,
        "8" * 64,
    )
    query = make_context_query((item,), generated_binding_refs=(fake,))
    with pytest.raises(ObjectivePositionPublicationError):
        require_bound_objective_position_context_query(carrier, query)


def test_l04_f26_generic_m4_family_boundary_is_still_closed():
    carrier = _carrier()
    assert validate_objective_position_publication_carrier(carrier) is carrier
    with pytest.raises(ReferenceClassError):
        build_v557_publication_bundle(
            (V557PublicationEntry(carrier.root_entry.obj, carrier.root_entry.governance),)
        )


def test_l04_f27_locator_identity_mutation_remains_invalid():
    carrier = _carrier()
    bad = replace(
        carrier.root_entry.locator,
        authoritative_object_id="PREV3POS:" + "7" * 64,
    )
    with pytest.raises(M4IntegrityError):
        replace(carrier.root_entry, locator=bad)
