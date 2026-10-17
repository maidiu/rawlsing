from __future__ import annotations

import gzip
import json
import warnings

import pytest

import rawlsing_next.gt34_q2_q69b_q86a_same_source_materialization as q2
import rawlsing_next.wave1_r5_q86_c11_projection as q86
import rawlsing_next.wave2_r5_q69b_conditioner_projection as q69b
from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
from rawlsing_next.pre553_empirical_objects import exact_ref


@pytest.fixture(scope="module")
def built_q2():
    candidate = q2.build_q69b_q86a_same_source_candidate()
    release = validate_c11_source_release(candidate)
    return candidate, release


def test_q2_transport_is_exact_and_bounded() -> None:
    transport = q2.load_same_source_transport()
    assert len(transport.rows) == 19_210
    assert len({row.respondent_key for row in transport.rows}) == 19_210
    assert {row.q86a_native_code for row in transport.rows} <= {"-1", "0", "1", "9"}
    assert {row.q69b_typed_state for row in transport.rows} == {
        "MISSING",
        "PUBLIC_CLINIC_EXPERIENCE_ABSENT",
        "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
        "UNKNOWN",
    }
    assert all(row.q86a_exposure_state == "EXPOSED__PROVED" for row in transport.rows)


def test_q2_builds_one_validated_same_source_release_without_identity_collapse(built_q2) -> None:
    candidate, release = built_q2

    assert release.release_id == q2.CANDIDATE_RELEASE_ID
    assert release.source_artifact_ref.content_hash == q69b.SOURCE_SHA256
    assert len(candidate.empirical_universes) == 1
    assert candidate.empirical_universes[0].content_hash == q69b.ACCEPTED_UNIVERSE_SHA256
    assert len(candidate.respondent_identities) == 19_210
    assert len(candidate.question_variable_bindings) == 2
    assert len(candidate.respondent_events) == 38_420
    assert len(candidate.routing_eligibility_facts_or_exact_rules) == 38_420
    assert len(candidate.empirical_coordinate_facts) == 19_210

    questions = {exact_ref(binding.native_question_ref).key for binding in candidate.question_variable_bindings}
    assert q86.question_ref("Q86A").key in questions
    assert q86.question_ref("Q86B").key not in questions

    q86a_events = tuple(
        event for event in candidate.respondent_events
        if exact_ref(event.native_question_ref).key == q86.question_ref("Q86A").key
    )
    q86a_routing = tuple(
        fact for fact in candidate.routing_eligibility_facts_or_exact_rules
        if exact_ref(fact.question_or_target_ref).key == q86.question_ref("Q86A").key
    )
    assert len(q86a_events) == 19_210
    assert len(q86a_routing) == 19_210

    replay = next(
        authority for authority in candidate.authority_snapshots
        if authority.authority_id == "GT34-Q2-R5-Q69B-Q86A-SAME-SOURCE-REPLAY"
    )
    assert replay.authority_kind == "REPLAY_PROTOCOL"
    assert replay.scope_envelope["semantic_owner_transfer"] is False
    assert replay.scope_envelope["portability"] == "NONE"
    assert replay.scope_envelope["pooling"] == "NONE"
    assert replay.scope_envelope["predecessor_mutation"] is False


def test_q2_reuses_exact_objects_from_accepted_q86_claim_scoped_release(built_q2) -> None:
    candidate, _release = built_q2
    accepted = q2._rehydrate_accepted_q86_release()

    assert accepted.semantic_release_hash == q2.Q86_ACCEPTED_RELEASE_SHA256
    assert accepted.replay_manifest.content_hash == q2.Q86_ACCEPTED_REPLAY_MANIFEST_SHA256

    accepted_q86a_events = {
        event.ref.key: event
        for event in accepted.public_objects
        if hasattr(event, "native_question_ref")
        and q2.exact_ref(event.native_question_ref).key == q86.question_ref("Q86A").key
    }
    accepted_q86a_routing = {
        fact.ref.key: fact
        for fact in accepted.public_objects
        if hasattr(fact, "question_or_target_ref")
        and q2.exact_ref(fact.question_or_target_ref).key == q86.question_ref("Q86A").key
    }
    candidate_q86a_events = {
        event.ref.key: event
        for event in candidate.respondent_events
        if q2.exact_ref(event.native_question_ref).key == q86.question_ref("Q86A").key
    }
    candidate_q86a_routing = {
        fact.ref.key: fact
        for fact in candidate.routing_eligibility_facts_or_exact_rules
        if q2.exact_ref(fact.question_or_target_ref).key == q86.question_ref("Q86A").key
    }

    assert len(accepted_q86a_events) == len(candidate_q86a_events) == 19_210
    assert len(accepted_q86a_routing) == len(candidate_q86a_routing) == 19_210
    assert set(candidate_q86a_events) == set(accepted_q86a_events)
    assert set(candidate_q86a_routing) == set(accepted_q86a_routing)
    assert all(
        candidate_q86a_events[key] is accepted_q86a_events[key]
        for key in accepted_q86a_events
    )
    assert all(
        candidate_q86a_routing[key] is accepted_q86a_routing[key]
        for key in accepted_q86a_routing
    )

    accepted_q86a_binding = next(
        record for record in accepted.internal_records
        if hasattr(record, "native_question_ref")
        and q2.exact_ref(record.native_question_ref).key == q86.question_ref("Q86A").key
    )
    candidate_q86a_binding = next(
        binding for binding in candidate.question_variable_bindings
        if q2.exact_ref(binding.native_question_ref).key == q86.question_ref("Q86A").key
    )
    assert candidate_q86a_binding is accepted_q86a_binding


def test_q2_release_identity_is_deterministic_and_bounded(built_q2) -> None:
    candidate, release = built_q2
    again = validate_c11_source_release(candidate)
    assert again.release_ref == release.release_ref
    assert again.semantic_release_hash == release.semantic_release_hash
    assert again.source_release_manifest_hash == release.source_release_manifest_hash
    assert again.replay_manifest.ref == release.replay_manifest.ref

    report = {
        "contract": q2.CONTRACT_ID,
        "release_id": release.release_id,
        "release_semantic_sha256": release.semantic_release_hash,
        "release_manifest_sha256": release.source_release_manifest_hash,
        "replay_manifest_sha256": release.replay_manifest.content_hash,
        "source_sha256": release.source_artifact_ref.content_hash,
        "transport_semantic_sha256": q2.TRANSPORT_SEMANTIC_SHA256,
        "transport_gzip_sha256": q2.TRANSPORT_GZIP_SHA256,
        "rows": len(candidate.respondent_identities),
        "events": len(candidate.respondent_events),
        "routing": len(candidate.routing_eligibility_facts_or_exact_rules),
        "coordinates": len(candidate.empirical_coordinate_facts),
        "q69b_predecessor_release_sha256": q2.Q69B_CURRENT_RELEASE_SHA256,
        "q86_predecessor_release_sha256": q69b.PREDECESSOR_RELEASE_SHA256,
        "predecessors_mutated": False,
        "semantic_owner_transfer": False,
        "portability": "NONE",
        "pooling": "NONE",
        "comparator": "NOT_CREATED",
        "psepf": "NOT_CREATED",
        "positive_v3": False,
    }
    warnings.warn(
        "Q2_STAGE2_IDENTITY_REPORT="
        + json.dumps(report, sort_keys=True, separators=(",", ":")),
        RuntimeWarning,
        stacklevel=1,
    )


def test_q2_committed_transport_fails_closed_under_semantic_tamper(tmp_path, monkeypatch) -> None:
    raw = q2._transport_path().read_bytes()
    canonical = json.loads(gzip.decompress(raw))
    canonical["rows"][0][9] = "1" if canonical["rows"][0][9] != "1" else "0"
    tampered = tmp_path / "tampered.json.gz"
    tampered.write_bytes(gzip.compress(
        json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"),
        compresslevel=9,
        mtime=0,
    ))
    monkeypatch.setattr(q2, "_transport_path", lambda: tampered)
    with pytest.raises(q2.Q2SameSourceMaterializationError, match="committed gzip identity mismatch"):
        q2.load_same_source_transport()
