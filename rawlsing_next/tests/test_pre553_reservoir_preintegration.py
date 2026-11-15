from __future__ import annotations

from pathlib import Path

import pytest

from rawlsing_next.m1_temporal_v554_admission_dedup import M1DecisionState, TemporalCompleteness
from rawlsing_next.m2_v555_atomic_route import M2DecisionState
from rawlsing_next.m3_v556_higher_order_structural import M3DecisionState
from rawlsing_next.m4_v557_v558_publication_repository import ClosureIntegrityError, build_v558_repository_bundle
from rawlsing_next.tests.pre553_reservoir_harness import (
    FROZEN_DOWNSTREAM_BLOBS,
    HARNESS_CONTRACT,
    HARNESS_CONTRACT_HASH,
    HarnessFixtureError,
    build_positive_repository,
    evaluate_v556,
    git_blob_sha1,
    make_admission_fixture,
    make_source_composition_stub,
    make_v553_stub,
    run_lane,
    v556_bindings,
)


def _positive_lane(tag: str, source: str = "source:one"):
    admission = make_admission_fixture(tag=tag, source_universe=source, decision_state="ADMITTED")
    v553 = make_v553_stub(
        admission,
        tag=tag,
        scr553_decision_state="V553_REQUIRED",
        temporal_completeness=TemporalCompleteness.REQUIRES_V553_OWNED_TEMPORAL_MEANING.value,
        include_candidate=True,
    )
    return run_lane(admission, v553, tag=tag)


def test_harness_contract_is_explicitly_non_semantic_and_content_addressed():
    assert HARNESS_CONTRACT["semantic_authority"] is False
    assert HARNESS_CONTRACT["admission_decision_service"] is False
    assert HARNESS_CONTRACT["fixture_content_is_authority"] is False
    assert len(HARNESS_CONTRACT_HASH) == 64


def test_positive_exact_admission_shape_traverses_v553_v554_v555_v556_v557_v558():
    a, b = _positive_lane("positive-a"), _positive_lane("positive-b")
    artifacts = build_positive_repository((a, b))
    assert all(x.m1.decision_state is M1DecisionState.ELIGIBLE for x in artifacts.lanes)
    assert all(x.m1.required_basis_kind == "V553_TEMPORAL_OBJECT" for x in artifacts.lanes)
    assert all(x.m2.decision_state is M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED for x in artifacts.lanes)
    assert artifacts.m3.decision_state is M3DecisionState.SUPPORTED
    assert artifacts.publication.publication_id.startswith("V557PUB:")
    assert artifacts.repository.repository_id.startswith("V558REPO:")
    assert artifacts.resolution.receipt.result_state == "RESOLUTION_COMPLETE"
    assert artifacts.resolution.resolved_entries[0].producer_object_ref == artifacts.root_entry.obj.ref
    assert {e.obj.producer_family for e in artifacts.entries} == {"V554", "V555", "V556"}


def test_replay_identity_is_exact_for_same_stubbed_inputs():
    lanes1 = (_positive_lane("replay-a"), _positive_lane("replay-b"))
    lanes2 = (_positive_lane("replay-a"), _positive_lane("replay-b"))
    one = build_positive_repository(lanes1)
    two = build_positive_repository(lanes2)
    assert one.lanes == two.lanes
    assert one.m3 == two.m3
    assert one.publication.publication_hash == two.publication.publication_hash
    assert one.repository.repository_hash == two.repository.repository_hash
    assert one.repository.index_manifest.manifest_hash == two.repository.index_manifest.manifest_hash
    assert one.resolution.receipt.receipt_hash == two.resolution.receipt.receipt_hash


def test_reference_closure_fails_closed_if_any_required_edge_is_removed():
    artifacts = build_positive_repository((_positive_lane("closure-a"), _positive_lane("closure-b")))
    assert artifacts.reference_edges
    with pytest.raises(ClosureIntegrityError):
        build_v558_repository_bundle(
            artifacts.publication,
            artifacts.entries,
            reference_edges=artifacts.reference_edges[:-1],
        )


def test_denied_admission_shape_stays_nonpositive_and_never_creates_route():
    admission = make_admission_fixture(tag="denied", source_universe="source:one", decision_state="DENIED")
    v553 = make_v553_stub(
        admission,
        tag="denied",
        scr553_decision_state="NO_POSITIVE_V553_OUTPUT__ADMISSION_NOT_POSITIVE",
        temporal_completeness=TemporalCompleteness.REQUIRES_V553_OWNED_TEMPORAL_MEANING.value,
        include_candidate=False,
    )
    lane = run_lane(admission, v553, tag="denied")
    assert lane.m1.decision_state is M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE
    assert lane.m1.f1 is None
    assert lane.m2.decision_state is M2DecisionState.V554_STRUCTURAL_USE_DENIED
    assert lane.m2.route is None


def test_harness_rejects_positive_v553_candidate_laundering_from_denied_admission_fixture():
    admission = make_admission_fixture(tag="launder", source_universe="source:one", decision_state="DENIED")
    v553 = make_v553_stub(
        admission,
        tag="launder",
        scr553_decision_state="V553_REQUIRED",
        temporal_completeness=TemporalCompleteness.REQUIRES_V553_OWNED_TEMPORAL_MEANING.value,
        include_candidate=True,
    )
    with pytest.raises(HarnessFixtureError):
        run_lane(admission, v553, tag="launder")


def test_negative_temporal_authority_remains_typed_negative_and_never_creates_route():
    admission = make_admission_fixture(
        tag="negative", source_universe="source:one", decision_state="ADMITTED", negative_refs=("temporal-negative:1",)
    )
    v553 = make_v553_stub(
        admission,
        tag="negative",
        scr553_decision_state="V553_NEGATIVE_LIMIT_ONLY",
        temporal_completeness=TemporalCompleteness.BLOCKED_BY_APPLICABLE_TEMPORAL_OR_SOURCE_NEGATIVE.value,
        include_candidate=True,
        condition_kinds=("K08",),
    )
    lane = run_lane(admission, v553, tag="negative")
    assert lane.m1.decision_state is M1DecisionState.INELIGIBLE_NEGATIVE_TEMPORAL_AUTHORITY
    assert lane.m1.f1 is None
    assert lane.m2.decision_state is M2DecisionState.V554_STRUCTURAL_USE_DENIED
    assert lane.m2.route is None


def test_typed_valid_empty_does_not_create_filler_route_or_repository_root():
    admission = make_admission_fixture(tag="empty", source_universe="source:one", decision_state="ADMITTED")
    v553 = make_v553_stub(
        admission,
        tag="empty",
        scr553_decision_state="V553_REQUIRED",
        temporal_completeness=TemporalCompleteness.REQUIRES_V553_OWNED_TEMPORAL_MEANING.value,
        include_candidate=False,
    )
    lane = run_lane(admission, v553, tag="empty")
    assert lane.m1.decision_state is M1DecisionState.VALID_EMPTY
    assert lane.m1.f1 is None
    assert lane.m2.decision_state is M2DecisionState.VALID_EMPTY
    assert lane.m2.route is None


def test_source_plurality_is_distinct_by_default_and_does_not_implicitly_compose():
    a = _positive_lane("plural-a", source="source:A")
    b = _positive_lane("plural-b", source="source:B")
    result = evaluate_v556((a.m2, b.m2), (a.source_universe, b.source_universe))
    assert result.decision_state is M3DecisionState.UNKNOWN_AUTHORITY
    assert "NONE_BY_DEFAULT" in result.reason
    assert result.v556_object is None


def test_explicit_noncomparable_source_relation_remains_noncomparable_without_v556_object():
    a = _positive_lane("noncomp-a", source="source:A")
    b = _positive_lane("noncomp-b", source="source:B")
    bindings = v556_bindings((a.m2, b.m2), (a.source_universe, b.source_universe))
    composition = make_source_composition_stub(bindings, decision="NONCOMPARABLE")
    result = evaluate_v556(
        (a.m2, b.m2),
        (a.source_universe, b.source_universe),
        composition=composition,
    )
    assert result.decision_state is M3DecisionState.NONCOMPARABLE
    assert result.v556_object is None


def test_downstream_m1_m6_render_and_psepf_bytes_match_frozen_base_git_blobs():
    root = Path(__file__).resolve().parents[1]
    observed = {
        name: git_blob_sha1((root / name).read_bytes())
        for name in FROZEN_DOWNSTREAM_BLOBS
    }
    assert observed == dict(FROZEN_DOWNSTREAM_BLOBS)
