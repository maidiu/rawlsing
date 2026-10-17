from __future__ import annotations

import json
from pathlib import Path
import warnings

import pytest

import rawlsing_next.wave2_r5_q69b_conditioner_projection as q69b
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalCoordinateFact,
    EmpiricalPredicate,
    RespondentEvent,
    RoutingEligibilityFact,
)
from rawlsing_next.pre553_c11_integrity import RespondentIdentity
import rawlsing_next.wave1_r5_q86_c11_projection as q86


@pytest.fixture(scope="module")
def transport():
    return q69b.load_q69b_transport()


@pytest.fixture(scope="module")
def release():
    return q69b.build_q69b_bounded_c11_candidate_release()


def test_fixed_transport_identity_and_exact_counts(transport):
    assert transport.semantic_hash == q69b.TRANSPORT_SEMANTIC_SHA256
    assert len(transport.rows) == 51_587
    assert transport.raw["counts"]["q69b_native"] == {
        "-1": 79,
        "0": 12_951,
        "1": 8_213,
        "2": 10_822,
        "3": 10_670,
        "7": 8_554,
        "9": 298,
        "998": 0,
        "SYSTEM_MISSING": 0,
    }
    assert transport.raw["counts"]["q69b_typed"] == {
        "MISSING": 79,
        "PHYSICAL_SYSTEM_MISSING": 0,
        "PUBLIC_CLINIC_EXPERIENCE_ABSENT": 8_554,
        "PUBLIC_CLINIC_EXPERIENCE_PRESENT": 42_656,
        "REFUSAL_NOT_LAWFULLY_CONDITIONABLE": 0,
        "UNKNOWN": 298,
    }
    assert transport.raw["counts"]["dateintr"] == {
        "VALID": 51_587, "MISSING": 0, "INVALID": 0
    }
    assert transport.raw["counts"]["dateintr_min_iso"] == "2011-10-20"
    assert transport.raw["counts"]["dateintr_max_iso"] == "2013-06-04"
    assert transport.raw["metadata"]["q69b_physical_value_labels"] == {
        "-1": "Missing",
        "0": "Never",
        "1": "Once or Twice",
        "2": "A Few Times",
        "3": "Often",
        "7": "No experience with public clinics in past year",
        "9": "Don't Know",
        "998": "Refused",
    }


def test_transport_reader_is_fixed_repo_native_no_path_selector(monkeypatch):
    real = Path.read_bytes
    seen = []

    def guarded(path: Path):
        seen.append(path.as_posix())
        assert path.name == "q69b_exact_source_transport.json.gz"
        assert ".sav" not in path.as_posix()
        return real(path)

    monkeypatch.setattr(Path, "read_bytes", guarded)
    loaded = q69b.load_q69b_transport()
    assert len(loaded.rows) == 51_587
    assert len(seen) == 1


def test_tampered_transport_fails_before_rehydration():
    raw = q69b._fixed_transport_path().read_bytes()
    damaged = bytearray(raw)
    damaged[len(damaged) // 2] ^= 1
    with pytest.raises(q69b.R5Q69BProjectionError, match="gzip identity"):
        q69b._rehydrate_verified_transport(bytes(damaged))


def test_reconstructed_respondents_match_all_current_gt2_exact_refs(transport):
    universe, _ = q69b._accepted_universe()
    respondents = q69b._respondents(transport, universe)
    assert len(respondents) == 51_587
    assert len({r.ref for r in respondents}) == 51_587
    assert q69b.current_gt2_respondent_subset_match_count(respondents) == 19_210


def test_candidate_is_new_validated_release_and_old_q86_identity_is_unchanged(release):
    assert release.release_id == q69b.CANDIDATE_RELEASE_ID
    assert release.release_id != q69b.PREDECESSOR_RELEASE_ID
    assert q69b.PREDECESSOR_RELEASE_ID == "R5_GT12_Q86A_Q86B_FROZEN"
    assert q86.FROZEN_BINDINGS.source_sha256 == q69b.SOURCE_SHA256
    assert release.source_artifact_ref.content_hash == q69b.SOURCE_SHA256


def test_candidate_materializes_exact_minimum_q69b_sections(release):
    respondents = [x for x in release.internal_records if isinstance(x, RespondentIdentity)]
    events = [x for x in release.public_objects if isinstance(x, RespondentEvent)]
    routing = [x for x in release.public_objects if isinstance(x, RoutingEligibilityFact)]
    coords = [x for x in release.public_objects if isinstance(x, EmpiricalCoordinateFact)]
    assert len(respondents) == 51_587
    assert len(events) == 51_587
    assert len(routing) == 51_587
    assert len(coords) == 51_587
    assert not any(isinstance(x, EmpiricalPredicate) for x in release.public_objects)
    assert all(x.routing_state == "ELIGIBLE_APPLICABLE" for x in routing)


def test_coordinate_states_and_values_preserve_typed_negatives(release):
    coords = [x for x in release.public_objects if isinstance(x, EmpiricalCoordinateFact)]
    state_counts = {}
    value_counts = {}
    dates = []
    for fact in coords:
        state_counts[fact.coordinate_state] = state_counts.get(fact.coordinate_state, 0) + 1
        value = fact.canonical_coordinate_value_if_authorized
        key = "NONE" if value is None else value
        value_counts[key] = value_counts.get(key, 0) + 1
        dates.append(fact.effective_or_reference_time)
    assert state_counts == {
        "MISSING": 79,
        "OBSERVED_COORDINATE": 51_210,
        "UNKNOWN": 298,
    }
    assert value_counts == {
        "NONE": 377,
        "PUBLIC_CLINIC_EXPERIENCE_ABSENT": 8_554,
        "PUBLIC_CLINIC_EXPERIENCE_PRESENT": 42_656,
    }
    assert min(dates) == "2011-10-20"
    assert max(dates) == "2013-06-04"


def test_coordinate_replay_provenance_explicitly_binds_l1a_minimum(release):
    coords = [x for x in release.public_objects if isinstance(x, EmpiricalCoordinateFact)]
    required_dependencies = {
        q69b.SOURCE_REF,
        q69b.CODEBOOK_REF,
        q69b.TRANSPORT_REF,
        q69b.CURRENTNESS_REF,
        q69b.MEASURE_BASIS_REF,
        q69b.CANONICAL_COORDINATE_REF,
    }
    assert len(coords) == 51_587
    for fact in coords:
        assert required_dependencies.issubset(set(fact.dependency_refs))
        authority_ids = {ref.authority_id for ref in fact.authority_snapshot_refs}
        assert q69b.REPAIRED_COORDINATE_AUTHORITY_ID in authority_ids
        assert q69b.CROSSWALK_ID in authority_ids
        assert q69b.TIME_RULE_ID in authority_ids


def test_crosswalk_and_time_candidate_snapshots_preserve_negative_law(release):
    authorities = {
        x.authority_id: x
        for x in release.public_objects
        if isinstance(x, AuthoritySnapshot)
    }
    crosswalk = authorities[q69b.CROSSWALK_ID]
    assert crosswalk.scope_envelope["frequency_order_discarded"] is True
    assert crosswalk.scope_envelope["source_specific_law_only"] is True
    assert crosswalk.scope_envelope["named_problem_occurrence_not_promoted_to_actor_history"] is True
    assert crosswalk.scope_envelope["question_text_sha256"] == q69b.QUESTION_TEXT_SHA256
    assert crosswalk.scope_envelope["routing_note_sha256"] == q69b.ROUTING_NOTE_SHA256

    time_rule = authorities[q69b.TIME_RULE_ID]
    assert time_rule.scope_envelope["query_time_substitution"] == "FORBIDDEN"
    assert time_rule.scope_envelope["wall_clock_substitution"] == "FORBIDDEN"
    assert time_rule.scope_envelope["actor_current_time_substitution"] == "FORBIDDEN"
    assert time_rule.scope_envelope["invented_edge_inclusion"] == "FORBIDDEN"


def test_only_repaired_coordinate_authority_is_packaged(release):
    authorities = [x for x in release.public_objects if isinstance(x, AuthoritySnapshot)]
    hashes = {x.authority_content_hash for x in authorities}
    assert q69b.REPAIRED_COORDINATE_AUTHORITY_SHA256 in hashes
    assert q69b.REJECTED_OVERBROAD_AUTHORITY_SHA256 not in hashes
    repaired = [
        x for x in authorities
        if x.authority_content_hash == q69b.REPAIRED_COORDINATE_AUTHORITY_SHA256
    ]
    assert len(repaired) == 1
    assert repaired[0].governed_object_families == ("EmpiricalCoordinateFact@1.0.0",)
    assert "EmpiricalPredicate@1.0.0" not in repaired[0].governed_object_families


def test_deterministic_release_rebuild_and_emit_identity_court(release):
    rebuilt = q69b.build_q69b_bounded_c11_candidate_release()
    assert rebuilt.release_ref == release.release_ref
    assert rebuilt.source_release_manifest_hash == release.source_release_manifest_hash
    assert rebuilt.replay_manifest.ref == release.replay_manifest.ref

    respondents = tuple(
        record for record in release.internal_records if isinstance(record, RespondentIdentity)
    )
    coords = tuple(
        obj for obj in release.public_objects if isinstance(obj, EmpiricalCoordinateFact)
    )
    court = {
        "schema_id": "GT34_N2_Q69B_C11_COURT@1.0.0",
        "transport_semantic_sha256": q69b.TRANSPORT_SEMANTIC_SHA256,
        "transport_gzip_sha256": q69b.TRANSPORT_GZIP_SHA256,
        "source_sha256": q69b.SOURCE_SHA256,
        "respondents": len(respondents),
        "current_gt2_exact_respondent_subset_matches":
            q69b.current_gt2_respondent_subset_match_count(respondents),
        "events": sum(isinstance(x, RespondentEvent) for x in release.public_objects),
        "routing": sum(isinstance(x, RoutingEligibilityFact) for x in release.public_objects),
        "coordinate_facts": len(coords),
        "release_id": release.release_id,
        "release_semantic_sha256": release.semantic_release_hash,
        "release_manifest_sha256": release.source_release_manifest_hash,
        "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
        "authority_snapshot_count":
            sum(isinstance(x, AuthoritySnapshot) for x in release.public_objects),
        "repaired_coordinate_authority_sha256":
            q69b.REPAIRED_COORDINATE_AUTHORITY_SHA256,
        "old_overbroad_authority_present": False,
        "predecessor_release_id": q69b.PREDECESSOR_RELEASE_ID,
    }
    warnings.warn(
        "N2_C11_COURT_JSON="
        + json.dumps(court, sort_keys=True, separators=(",", ":")),
        RuntimeWarning,
        stacklevel=1,
    )


def test_o1_q69b_candidate_release_replay_authority_and_transport_identities_unchanged(release):
    assert q69b.TRANSPORT_SEMANTIC_SHA256 == (
        "c90ef7eaeea4b1536d3153beb344ce22156bf15bf835a3182c1b5784b8f238c5"
    )
    assert q69b.REPAIRED_COORDINATE_AUTHORITY_SHA256 == (
        "cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c"
    )
    assert q69b.COORDINATE_SHA256 == (
        "7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937"
    )
    assert release.release_id == "R5_GT34_N2_Q69B_BOUNDED_CANDIDATE_R1"
    assert release.semantic_release_hash == (
        "2343023560ea963b6b290575d93361256825897a7c32ff31519e3d2425b595ec"
    )
    assert release.release_ref.content_hash == (
        "2343023560ea963b6b290575d93361256825897a7c32ff31519e3d2425b595ec"
    )
    # HQ's shorthand "candidate release hash" 15b39... is the banked
    # source-release-manifest identity; N2 records the semantic release hash
    # separately as 234302...
    assert release.source_release_manifest_hash == (
        "15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4"
    )
    assert release.replay_manifest.content_hash == (
        "8ec8450d41524015c8e6b2716c00f622a9792334d2b952cac585b3b2971cb539"
    )
    assert release.replay_manifest.ref.content_hash == (
        "8ec8450d41524015c8e6b2716c00f622a9792334d2b952cac585b3b2971cb539"
    )
