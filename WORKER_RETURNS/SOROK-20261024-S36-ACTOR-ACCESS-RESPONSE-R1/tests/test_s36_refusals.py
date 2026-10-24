"""S36 source-bound refusals for wrong actor/event/hash/time/revocation."""
from __future__ import annotations

import pytest

from candidate import CandidateStore, ResponseStatus
from s36_harness import access_witness, event_record, refusal_case, run_s35_case


def _tables_empty(store: CandidateStore) -> bool:
    return all(not rows for rows in store.snapshot().values())


@pytest.mark.parametrize(
    "case",
    [
        "access_wrong_actor",
        "access_wrong_event",
        "access_wrong_source_hash",
        "access_wrong_scene",
        "access_scene_empty",
        "access_scene_missing",
        "access_before_event",
        "access_after_as_of",
        "access_revoked_field",
        "access_revoked_source",
        "access_bad_namespace",
        "response_wrong_actor",
        "response_wrong_event",
        "response_wrong_source_hash",
        "response_before_access",
        "response_after_as_of",
        "response_revoked_field",
        "response_revoked_source",
        "response_bad_kind",
        "response_bad_namespace",
    ],
)
def test_source_bound_refusal_is_atomic_and_targetless(case, tmp_path):
    access, response, revoked = refusal_case(case)
    with CandidateStore(tmp_path / f"{case}.sqlite") as store:
        result, _ = run_s35_case(
            store,
            access=access,
            response=response,
            revoked_source_refs=revoked,
        )
        assert result.response.status is ResponseStatus.REFUSED
        assert result.response.target_proposals == ()
        assert result.decision is None
        assert result.receipt is None
        assert result.committed is False
        assert result.no_ghost is True
        assert result.stage("s35_response_refusal") is not None
        assert _tables_empty(store)


def test_unbound_contradictory_context_is_refused(tmp_path):
    with CandidateStore(tmp_path / "contrary_unbound.sqlite") as store:
        result, _ = run_s35_case(
            store,
            contradictory_context=True,
            contradictory_refs=(),
        )
        assert result.response.status is ResponseStatus.REFUSED
        assert result.response.reason == "S35_CONTRADICTORY_CONTEXT_UNBOUND"
        assert result.response.target_proposals == ()
        assert result.committed is False
        assert _tables_empty(store)


@pytest.mark.parametrize("scene", ["", None])
def test_empty_or_missing_access_scene_is_refused(scene, tmp_path):
    event = event_record()
    access = access_witness(event, scene=scene)
    with CandidateStore(tmp_path / f"scene_missing_{scene!r}.sqlite") as store:
        result, _ = run_s35_case(store, access=access, response=None)
        assert result.response.status is ResponseStatus.REFUSED
        assert result.response.reason == "S35_ACCESS_SCENE_MISSING"
        assert result.response.target_proposals == ()
        assert result.decision is None
        assert result.receipt is None
        assert result.committed is False
        assert result.no_ghost is True
        assert _tables_empty(store)


def test_empty_actual_event_scene_is_refused(tmp_path):
    event = event_record(scene="")
    access = access_witness(event, scene="garage")
    with CandidateStore(tmp_path / "event_scene_missing.sqlite") as store:
        result, _ = run_s35_case(
            store,
            scene="",
            access=access,
            response=None,
        )
        assert result.response.status is ResponseStatus.REFUSED
        assert result.response.reason == "S35_ACCESS_EVENT_SCENE_MISSING"
        assert result.response.target_proposals == ()
        assert result.decision is None
        assert result.receipt is None
        assert result.committed is False
        assert result.no_ghost is True
        assert _tables_empty(store)
