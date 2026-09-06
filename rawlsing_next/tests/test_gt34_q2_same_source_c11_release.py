from __future__ import annotations

from dataclasses import replace
import gzip
import json

import pytest

import rawlsing_next.gt34_q2_q69b_q86a_same_source_materialization as q2
import rawlsing_next.wave1_r5_q86_c11_projection as q86
import rawlsing_next.wave2_r5_q69b_conditioner_projection as q69b
from rawlsing_next.pre553_empirical_objects import exact_ref


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


def test_q2_builds_one_validated_same_source_release_without_identity_collapse() -> None:
    candidate = q2.build_q69b_q86a_same_source_candidate()
    release = q2.build_validated_q69b_q86a_same_source_release()

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
    assert any("Q69B" in key for key in questions)

    assert all(
        exact_ref(event.native_question_ref).key != q86.question_ref("Q86B").key
        for event in candidate.respondent_events
    )

    replay = next(
        authority for authority in candidate.authority_snapshots
        if authority.authority_id == "GT34-Q2-R5-Q69B-Q86A-SAME-SOURCE-REPLAY"
    )
    assert replay.authority_kind == "REPLAY_PROTOCOL"
    assert replay.scope_envelope["semantic_owner_transfer"] is False
    assert replay.scope_envelope["portability"] == "NONE"
    assert replay.scope_envelope["pooling"] == "NONE"
    assert replay.scope_envelope["predecessor_mutation"] is False


def test_q2_q86a_objects_are_exact_subsets_of_current_gt2_payload() -> None:
    report = q2.identity_report()
    assert report["q86a_exact_current_event_refs"] == 19_210
    assert report["q86a_exact_current_routing_refs"] == 19_210
    assert report["q69b_predecessor_release_sha256"] == q2.Q69B_CURRENT_RELEASE_SHA256
    assert report["q86_predecessor_release_sha256"] == q69b.PREDECESSOR_RELEASE_SHA256
    assert report["predecessors_mutated"] is False
    assert report["semantic_owner_transfer"] is False
    assert report["portability"] == "NONE"
    assert report["pooling"] == "NONE"
    assert report["comparator"] == "NOT_CREATED"
    assert report["psepf"] == "NOT_CREATED"
    assert report["positive_v3"] is False


def test_q2_release_identity_is_deterministic() -> None:
    first = q2.identity_report()
    second = q2.identity_report()
    assert second == first
    # Surface exact identities to the governed court log for durable HQ receipt.
    import warnings
    warnings.warn(
        "Q2_STAGE2_IDENTITY_REPORT="
        + json.dumps(first, sort_keys=True, separators=(",", ":")),
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
