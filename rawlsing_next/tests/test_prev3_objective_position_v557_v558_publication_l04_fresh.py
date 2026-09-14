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
from rawlsing_next.tests import test_prev3_objective_position_v557_v558_publication as hcases
from rawlsing_next.tests.test_prev3_objective_position_v557_v558_publication import _carrier


H00_H23 = tuple(getattr(hcases, f"test_j04_h{i:02d}_" + suffix) for i, suffix in (
    (0, "exact_proving_fact_publication_and_replay"),
    (1, "relabel_producer_family_as_v552_rejected"),
    (2, "relabel_as_v553_v554_v555_v556_rejected"),
    (3, "schema_or_version_mutation_rejected"),
    (4, "fact_ref_kind_mutation_rejected"),
    (5, "prev3pos_object_id_mutation_rejected"),
    (6, "content_hash_mutation_rejected"),
    (7, "nonpositive_position_result_not_publication_root"),
    (8, "source_domain_use_widen_or_substitute_rejected"),
    (9, "bare_context_without_domain_binding_rejected"),
    (10, "active_causal_request_rejected"),
    (11, "review_is_not_inferred_from_context_mapping"),
    (12, "drop_canonical_dependency_rejected"),
    (13, "invent_dependency_ref_rejected"),
    (14, "negative_ceiling_mutation_rejected"),
    (15, "runtime_clock_temporal_surrogate_rejected"),
    (16, "present_day_persistence_substitution_rejected"),
    (17, "strip_evidence_or_provenance_rejected"),
    (18, "authority_ref_mutation_rejected"),
    (19, "latest_default_fuzzy_resolution_rejected"),
    (20, "person_v3_psychological_use_rejected"),
    (21, "m2_m3_stage_authority_not_inferred_from_publication"),
    (22, "setlike_reordering_replays_identically"),
    (23, "v558_locator_reidentification_rejected"),
))


def test_l04_reproduce_complete_h00_h23_matrix_in_fresh_execution():
    assert len(H00_H23) == 24
    for case in H00_H23:
        case()


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
    fake = replace(
        carrier.domain_use_binding.ref,
        object_id="PREV3POSUSE:" + "8" * 64,
        content_hash="8" * 64,
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
