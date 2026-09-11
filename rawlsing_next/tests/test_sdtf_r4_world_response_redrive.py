from dataclasses import replace

import pytest

from rawlsing_next.sdtf_r4_world_response_redrive import (
    NON_DURABLE_DISPOSITION,
    CurrentResponseConsequence,
    ExternalizationState,
    ExternalizedOccurrenceCandidate,
    R4BindingMismatchError,
    R4OccurrenceStateError,
    R4RedriveError,
    R4SourceError,
    bind_admitted_externalized_occurrence_source,
    redrive_externalized_occurrence,
)
from rawlsing_next.wsc_gt0_protocol import GT0ExactRef, gt0_content_hash


def _h(label: str) -> str:
    return gt0_content_hash({"label": label})


def _ref(kind: str, label: str) -> GT0ExactRef:
    return GT0ExactRef(kind, f"urn:test:{label}", _h(label))


def _candidate(state=ExternalizationState.ADMITTED_EXTERNAL_OCCURRENCE):
    return ExternalizedOccurrenceCandidate(
        state=state,
        occurrence_id="urn:test:external-occurrence:1",
        occurrence_hash=_h("occurrence"),
        authority_id="ADP-019_EXTERNAL_EVENT_ADMISSION",
        authority_version="1.0.0",
        authority_hash=_h("authority"),
        effective_time_ref=_ref("EFFECTIVE_TIME", "time"),
        actor_ref=_ref("ACTOR", "actor"),
        scope_ref=_ref("WORLD_SCOPE", "scope"),
        world_context_ref=_ref("GENERATED_WORLD_CONTEXT", "world-context"),
        stream_ref=_ref("EVENT_STREAM", "stream"),
        admission_receipt_ref=_ref("ADP019_ADMISSION_RECEIPT", "admission"),
        causal_use_permission_ref=_ref("CAUSAL_USE_PERMISSION", "permission"),
        provenance_refs=(_ref("PROVENANCE", "prov"),),
        replay_refs=(_ref("REPLAY", "replay"),),
    )


def _bind(candidate=None):
    candidate = candidate or _candidate()
    return bind_admitted_externalized_occurrence_source(
        candidate,
        expected_actor_ref=candidate.actor_ref,
        expected_scope_ref=candidate.scope_ref,
    )


def test_exact_admitted_externalized_occurrence_is_accepted_as_precipitating_source():
    source = _bind()
    assert source.candidate.occurrence_ref in source.envelope.object_refs
    assert source.candidate.authority_ref in source.envelope.authority_refs
    assert "PRECIPITATING_EVENT_SOURCE" in source.envelope.permission_ceiling
    assert source.candidate.effective_time_ref in source.envelope.current_selection_refs


@pytest.mark.parametrize(
    "state",
    [
        ExternalizationState.DRAFT,
        ExternalizationState.REJECTED,
        ExternalizationState.UNEMITTED,
    ],
)
def test_draft_rejected_and_unemitted_artifacts_are_rejected(state):
    candidate = _candidate(state)
    with pytest.raises(R4OccurrenceStateError):
        _bind(candidate)


def test_emitted_but_unadmitted_artifact_is_rejected():
    with pytest.raises(R4OccurrenceStateError):
        _bind(_candidate(ExternalizationState.EMITTED_UNADMITTED))


def test_actor_and_scope_mismatch_are_rejected():
    candidate = _candidate()
    with pytest.raises(R4BindingMismatchError):
        bind_admitted_externalized_occurrence_source(
            candidate,
            expected_actor_ref=_ref("ACTOR", "other-actor"),
            expected_scope_ref=candidate.scope_ref,
        )
    with pytest.raises(R4BindingMismatchError):
        bind_admitted_externalized_occurrence_source(
            candidate,
            expected_actor_ref=candidate.actor_ref,
            expected_scope_ref=_ref("WORLD_SCOPE", "other-scope"),
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("authority_id", ""),
        ("authority_version", "latest"),
        ("authority_hash", "not-a-hash"),
        ("occurrence_hash", "not-a-hash"),
        ("effective_time_ref", None),
        ("world_context_ref", None),
        ("stream_ref", None),
        ("admission_receipt_ref", None),
        ("causal_use_permission_ref", None),
        ("provenance_refs", ()),
        ("replay_refs", ()),
    ],
)
def test_missing_or_inexact_authority_version_hash_time_provenance_and_replay_are_rejected(field, value):
    kwargs = {
        "state": ExternalizationState.ADMITTED_EXTERNAL_OCCURRENCE,
        "occurrence_id": "urn:test:external-occurrence:1",
        "occurrence_hash": _h("occurrence"),
        "authority_id": "ADP-019_EXTERNAL_EVENT_ADMISSION",
        "authority_version": "1.0.0",
        "authority_hash": _h("authority"),
        "effective_time_ref": _ref("EFFECTIVE_TIME", "time"),
        "actor_ref": _ref("ACTOR", "actor"),
        "scope_ref": _ref("WORLD_SCOPE", "scope"),
        "world_context_ref": _ref("GENERATED_WORLD_CONTEXT", "world-context"),
        "stream_ref": _ref("EVENT_STREAM", "stream"),
        "admission_receipt_ref": _ref("ADP019_ADMISSION_RECEIPT", "admission"),
        "causal_use_permission_ref": _ref("CAUSAL_USE_PERMISSION", "permission"),
        "provenance_refs": (_ref("PROVENANCE", "prov"),),
        "replay_refs": (_ref("REPLAY", "replay"),),
    }
    kwargs[field] = value
    with pytest.raises(R4SourceError):
        ExternalizedOccurrenceCandidate(**kwargs)


def test_label_only_world_context_cannot_be_promoted_to_current_generated_world():
    candidate = _candidate()
    with pytest.raises(R4SourceError):
        replace(candidate, world_context_ref=GT0ExactRef("GENERATED_WORLD_CONTEXT", "V3_SIM_WORLD_R1"))


def test_exact_replay_ref_and_hash_are_conserved_deterministically():
    source = _bind()
    result = redrive_externalized_occurrence(
        source,
        expected_source_hash=source.source_hash,
        expected_actor_ref=source.candidate.actor_ref,
        expected_scope_ref=source.candidate.scope_ref,
    )
    assert result.receipt.input_envelope_hashes == (source.envelope.content_hash,)
    assert result.receipt.output_envelope.content_hash == source.envelope.content_hash
    assert result.receipt.replay_refs == source.candidate.replay_refs
    assert result.source.source_hash == source.source_hash


def test_current_response_consequence_is_non_durable_and_cannot_be_promoted():
    source = _bind()
    result = redrive_externalized_occurrence(
        source,
        expected_source_hash=source.source_hash,
        expected_actor_ref=source.candidate.actor_ref,
        expected_scope_ref=source.candidate.scope_ref,
    )
    assert result.current_response_consequence.durability == NON_DURABLE_DISPOSITION
    with pytest.raises(R4SourceError):
        CurrentResponseConsequence(
            source_binding_hash=source.source_hash,
            actor_ref=source.candidate.actor_ref,
            scope_ref=source.candidate.scope_ref,
            durability="DURABLE_PERSON_STATE",
        )


def test_redrive_replays_exact_occurrence_or_fails_closed_on_missing_or_stale_source():
    source = _bind()
    ok = redrive_externalized_occurrence(
        source,
        expected_source_hash=source.source_hash,
        expected_actor_ref=source.candidate.actor_ref,
        expected_scope_ref=source.candidate.scope_ref,
    )
    assert ok.source.candidate.occurrence_ref == source.candidate.occurrence_ref

    with pytest.raises(R4RedriveError):
        redrive_externalized_occurrence(
            None,
            expected_source_hash=source.source_hash,
            expected_actor_ref=source.candidate.actor_ref,
            expected_scope_ref=source.candidate.scope_ref,
        )
    with pytest.raises(R4RedriveError):
        redrive_externalized_occurrence(
            source,
            expected_source_hash=_h("stale-source"),
            expected_actor_ref=source.candidate.actor_ref,
            expected_scope_ref=source.candidate.scope_ref,
        )
