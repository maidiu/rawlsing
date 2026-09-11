from dataclasses import replace

import pytest

from rawlsing_next.sdtf_r4_world_response_redrive import (
    NON_DURABLE_DISPOSITION,
    OBJECTIVE_CHANGED_DETERMINANT_KIND,
    CurrentResponseConsequence,
    ExternalizationState,
    ExternalizedOccurrenceCandidate,
    ExternalWorldResponseCandidate,
    R4BindingMismatchError,
    R4OccurrenceStateError,
    R4RedriveError,
    R4SourceError,
    R4WorldResponseStateError,
    WorldResponseAdmissionState,
    WorldResponseSourceKind,
    bind_admitted_external_world_response_source,
    bind_admitted_externalized_occurrence_source,
    request_r4_invalidation_rederivation,
)
from rawlsing_next.wsc_gt0_protocol import GT0ExactRef, gt0_content_hash


def _h(label: str) -> str:
    return gt0_content_hash({"label": label})


def _ref(kind: str, label: str) -> GT0ExactRef:
    return GT0ExactRef(kind, f"urn:test:{label}", _h(label))


def _occurrence(state=ExternalizationState.ADMITTED_EXTERNAL_OCCURRENCE):
    return ExternalizedOccurrenceCandidate(
        state=state,
        occurrence_id="urn:test:external-occurrence:1",
        occurrence_hash=_h("occurrence"),
        authority_id="ADP-019_EXTERNAL_EVENT_ADMISSION",
        authority_version="1.0.0",
        authority_hash=_h("occurrence-authority"),
        effective_time_ref=_ref("EFFECTIVE_TIME", "occurrence-time"),
        actor_ref=_ref("ACTOR", "actor"),
        scope_ref=_ref("WORLD_SCOPE", "scope"),
        world_context_ref=_ref("GENERATED_WORLD_CONTEXT", "world-context"),
        stream_ref=_ref("EVENT_STREAM", "stream"),
        admission_receipt_ref=_ref("ADP019_ADMISSION_RECEIPT", "occurrence-admission"),
        causal_use_permission_ref=_ref("CAUSAL_USE_PERMISSION", "occurrence-permission"),
        provenance_refs=(_ref("PROVENANCE", "occurrence-prov"),),
        replay_refs=(_ref("REPLAY", "occurrence-replay"),),
    )


def _world_response(
    state=WorldResponseAdmissionState.ADMITTED_OBJECTIVE_WORLD_RESPONSE,
    source_kind=WorldResponseSourceKind.COMPETENT_EXTERNAL_OBJECTIVE_SOURCE,
):
    return ExternalWorldResponseCandidate(
        state=state,
        source_kind=source_kind,
        response_id="urn:test:objective-world-response:1",
        response_hash=_h("world-response"),
        authority_id="EXTERNAL_OBJECTIVE_SOURCE",
        authority_version="7.1.0",
        authority_hash=_h("world-response-authority"),
        effective_time_ref=_ref("EFFECTIVE_TIME", "world-response-time"),
        counterpart_ref=_ref("COUNTERPART", "counterpart"),
        scope_ref=_ref("WORLD_SCOPE", "scope"),
        world_context_ref=_ref("GENERATED_WORLD_CONTEXT", "world-context"),
        admission_receipt_ref=_ref("OBJECTIVE_SOURCE_ADMISSION_RECEIPT", "world-response-admission"),
        objective_source_permission_ref=_ref("OBJECTIVE_SOURCE_AUTHORSHIP_PERMISSION", "world-response-permission"),
        changed_determinant_refs=(
            _ref(OBJECTIVE_CHANGED_DETERMINANT_KIND, "changed-det-a"),
            _ref(OBJECTIVE_CHANGED_DETERMINANT_KIND, "changed-det-b"),
        ),
        provenance_refs=(_ref("PROVENANCE", "world-response-prov"),),
        replay_refs=(_ref("REPLAY", "world-response-replay"),),
    )


def _bind_occurrence(candidate=None):
    candidate = candidate or _occurrence()
    return bind_admitted_externalized_occurrence_source(
        candidate,
        expected_actor_ref=candidate.actor_ref,
        expected_scope_ref=candidate.scope_ref,
        expected_world_context_ref=candidate.world_context_ref,
    )


def _bind_world_response(candidate=None):
    candidate = candidate or _world_response()
    return bind_admitted_external_world_response_source(
        candidate,
        expected_scope_ref=candidate.scope_ref,
        expected_world_context_ref=candidate.world_context_ref,
    )


def _request(occurrence=None, world_response=None):
    occurrence = occurrence or _bind_occurrence()
    world_response = world_response or _bind_world_response()
    return request_r4_invalidation_rederivation(
        occurrence,
        world_response,
        expected_occurrence_source_hash=occurrence.source_hash,
        expected_world_response_source_hash=world_response.source_hash,
        expected_actor_ref=occurrence.candidate.actor_ref,
        expected_scope_ref=occurrence.candidate.scope_ref,
        expected_world_context_ref=occurrence.candidate.world_context_ref,
    )


def test_exact_admitted_externalized_occurrence_is_accepted_as_precipitating_source():
    source = _bind_occurrence()
    assert source.candidate.occurrence_ref in source.envelope.object_refs
    assert source.candidate.authority_ref in source.envelope.authority_refs
    assert source.candidate.causal_use_permission_ref in source.envelope.authority_refs
    assert "PRECIPITATING_EVENT_SOURCE" in source.envelope.permission_ceiling


@pytest.mark.parametrize(
    "state",
    [ExternalizationState.DRAFT, ExternalizationState.REJECTED, ExternalizationState.UNEMITTED],
)
def test_draft_rejected_and_unemitted_artifacts_are_not_occurrences(state):
    with pytest.raises(R4OccurrenceStateError):
        _bind_occurrence(_occurrence(state))


def test_emitted_but_unadmitted_artifact_is_not_an_occurrence():
    with pytest.raises(R4OccurrenceStateError):
        _bind_occurrence(_occurrence(ExternalizationState.EMITTED_UNADMITTED))


def test_occurrence_actor_scope_and_world_context_mismatch_fail_closed():
    candidate = _occurrence()
    with pytest.raises(R4BindingMismatchError):
        bind_admitted_externalized_occurrence_source(
            candidate,
            expected_actor_ref=_ref("ACTOR", "other-actor"),
            expected_scope_ref=candidate.scope_ref,
            expected_world_context_ref=candidate.world_context_ref,
        )
    with pytest.raises(R4BindingMismatchError):
        bind_admitted_externalized_occurrence_source(
            candidate,
            expected_actor_ref=candidate.actor_ref,
            expected_scope_ref=_ref("WORLD_SCOPE", "other-scope"),
            expected_world_context_ref=candidate.world_context_ref,
        )
    with pytest.raises(R4BindingMismatchError):
        bind_admitted_externalized_occurrence_source(
            candidate,
            expected_actor_ref=candidate.actor_ref,
            expected_scope_ref=candidate.scope_ref,
            expected_world_context_ref=_ref("GENERATED_WORLD_CONTEXT", "other-world"),
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
def test_occurrence_missing_or_inexact_authority_version_hash_time_provenance_replay_fail(field, value):
    candidate = _occurrence()
    with pytest.raises(R4SourceError):
        replace(candidate, **{field: value})


def test_label_only_world_context_cannot_be_promoted_to_current_generated_world():
    with pytest.raises(R4SourceError):
        replace(
            _occurrence(),
            world_context_ref=GT0ExactRef("GENERATED_WORLD_CONTEXT", "V3_SIM_WORLD_R1"),
        )


def test_competent_external_objective_world_response_is_accepted_without_r4_authorship():
    source = _bind_world_response()
    candidate = source.candidate
    assert candidate.response_ref in source.envelope.object_refs
    assert set(candidate.changed_determinant_refs) < set(source.envelope.object_refs)
    assert source.envelope.semantic_owner_ref == candidate.authority_ref
    assert "OBJECTIVE_CHANGED_DETERMINANT_SOURCE" in source.envelope.permission_ceiling


@pytest.mark.parametrize(
    "state",
    [
        WorldResponseAdmissionState.DRAFT,
        WorldResponseAdmissionState.REJECTED,
        WorldResponseAdmissionState.UNEMITTED,
        WorldResponseAdmissionState.EMITTED_UNADMITTED,
    ],
)
def test_unadmitted_world_response_never_becomes_objective_source(state):
    with pytest.raises(R4WorldResponseStateError):
        _bind_world_response(_world_response(state=state))


@pytest.mark.parametrize(
    "kind",
    [
        WorldResponseSourceKind.PRIVATE_V3_STATE,
        WorldResponseSourceKind.GENERIC_WORLD_SIMULATION,
        WorldResponseSourceKind.INTERPRETATION_EXPECTATION_STRIVING,
        WorldResponseSourceKind.OEE_ENCOUNTER_DERIVATION,
    ],
)
def test_private_v3_simulation_interpretation_and_oee_encounter_cannot_author_world_response(kind):
    with pytest.raises(R4WorldResponseStateError):
        _bind_world_response(_world_response(source_kind=kind))


def test_world_response_scope_and_world_context_mismatch_fail_closed():
    candidate = _world_response()
    with pytest.raises(R4BindingMismatchError):
        bind_admitted_external_world_response_source(
            candidate,
            expected_scope_ref=_ref("WORLD_SCOPE", "other-scope"),
            expected_world_context_ref=candidate.world_context_ref,
        )
    with pytest.raises(R4BindingMismatchError):
        bind_admitted_external_world_response_source(
            candidate,
            expected_scope_ref=candidate.scope_ref,
            expected_world_context_ref=_ref("GENERATED_WORLD_CONTEXT", "other-world"),
        )


def test_world_response_cannot_mint_d1_facts_directly_as_changed_determinants():
    with pytest.raises(R4WorldResponseStateError):
        replace(
            _world_response(),
            changed_determinant_refs=(_ref("D1_PRIME_FACT", "forbidden-d1-fact"),),
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("authority_version", "default"),
        ("authority_hash", "bad"),
        ("effective_time_ref", None),
        ("admission_receipt_ref", None),
        ("objective_source_permission_ref", None),
        ("changed_determinant_refs", ()),
        ("provenance_refs", ()),
        ("replay_refs", ()),
    ],
)
def test_world_response_missing_authority_admission_determinant_or_replay_material_fails(field, value):
    with pytest.raises(R4SourceError):
        replace(_world_response(), **{field: value})


def test_exact_external_occurrence_plus_objective_world_response_yields_only_r4_request():
    occurrence = _bind_occurrence()
    world_response = _bind_world_response()
    result = _request(occurrence, world_response)
    request = result.invalidation_rederivation_request
    assert request.changed_determinant_refs == world_response.candidate.changed_determinant_refs
    assert tuple(request.request_envelope.object_refs) == world_response.candidate.changed_determinant_refs
    assert request.receipt.input_envelope_hashes == tuple(
        sorted((occurrence.source_hash, world_response.source_hash))
    )
    assert request.receipt.output_envelope.content_hash == request.request_envelope.content_hash
    assert request.request_envelope.permission_ceiling == ("REQUEST_R4_INVALIDATION_REDERIVATION",)


def test_redrive_conserves_exact_replay_refs_from_both_external_sources():
    result = _request()
    request = result.invalidation_rederivation_request
    expected = tuple(
        sorted(
            result.occurrence_source.candidate.replay_refs
            + result.world_response_source.candidate.replay_refs,
            key=lambda ref: ref.key,
        )
    )
    assert request.receipt.replay_refs == expected
    assert request.request_envelope.replay_refs == expected


def test_current_response_consequence_is_non_durable_and_cannot_be_promoted():
    result = _request()
    consequence = result.current_response_consequence
    assert consequence.durability == NON_DURABLE_DISPOSITION
    with pytest.raises(R4SourceError):
        CurrentResponseConsequence(
            occurrence_source_hash=result.occurrence_source.source_hash,
            world_response_source_hash=result.world_response_source.source_hash,
            actor_ref=result.occurrence_source.candidate.actor_ref,
            scope_ref=result.occurrence_source.candidate.scope_ref,
            durability="DURABLE_PERSON_STATE",
        )


def test_request_is_deterministic_for_exact_sources():
    first = _request()
    second = _request(first.occurrence_source, first.world_response_source)
    assert first.invalidation_rederivation_request.content_hash == second.invalidation_rederivation_request.content_hash
    assert first.invalidation_rederivation_request.receipt.content_hash == second.invalidation_rederivation_request.receipt.content_hash


def test_redrive_fails_closed_on_missing_or_stale_occurrence_source():
    occurrence = _bind_occurrence()
    world_response = _bind_world_response()
    common = dict(
        expected_occurrence_source_hash=occurrence.source_hash,
        expected_world_response_source_hash=world_response.source_hash,
        expected_actor_ref=occurrence.candidate.actor_ref,
        expected_scope_ref=occurrence.candidate.scope_ref,
        expected_world_context_ref=occurrence.candidate.world_context_ref,
    )
    with pytest.raises(R4RedriveError):
        request_r4_invalidation_rederivation(None, world_response, **common)
    with pytest.raises(R4RedriveError):
        request_r4_invalidation_rederivation(
            occurrence,
            world_response,
            **{**common, "expected_occurrence_source_hash": _h("stale-occurrence")},
        )


def test_redrive_fails_closed_on_missing_or_stale_world_response_source():
    occurrence = _bind_occurrence()
    world_response = _bind_world_response()
    common = dict(
        expected_occurrence_source_hash=occurrence.source_hash,
        expected_world_response_source_hash=world_response.source_hash,
        expected_actor_ref=occurrence.candidate.actor_ref,
        expected_scope_ref=occurrence.candidate.scope_ref,
        expected_world_context_ref=occurrence.candidate.world_context_ref,
    )
    with pytest.raises(R4RedriveError):
        request_r4_invalidation_rederivation(occurrence, None, **common)
    with pytest.raises(R4RedriveError):
        request_r4_invalidation_rederivation(
            occurrence,
            world_response,
            **{**common, "expected_world_response_source_hash": _h("stale-world-response")},
        )
