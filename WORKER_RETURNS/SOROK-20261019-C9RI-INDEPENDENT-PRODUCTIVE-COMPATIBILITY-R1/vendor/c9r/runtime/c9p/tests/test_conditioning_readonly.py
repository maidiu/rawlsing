"""(c) Read-only person/world conditioning and forbidden conversion tests."""
from __future__ import annotations

from conftest import ACTOR_ID, build_conditioning_sources
from candidate.canon import seal
from candidate.conditioning import (
    ConditioningReason,
    ConditioningRefusal,
    ConditioningStatus,
    bind_conditioning,
    make_conditioning_source,
)


def test_bound_conditioning_preserves_native_guard_zero_effect() -> None:
    sources = build_conditioning_sources()
    view = bind_conditioning(subject=ACTOR_ID, sources=sources, as_of=20)
    assert view.status is ConditioningStatus.BOUND
    assert view.reason is ConditioningReason.OK
    assert "DENY_ZERO_EFFECT" in view.guard_outcome
    assert view.readset_refs == tuple(source["source_ref"] for source in sources)


def test_conditioning_view_is_read_only() -> None:
    view = bind_conditioning(
        subject=ACTOR_ID, sources=build_conditioning_sources(), as_of=20
    )
    try:
        view.assert_read_only()
    except ConditioningRefusal as error:
        assert error.code == ConditioningReason.WRITE_ATTEMPTED.value
    else:  # pragma: no cover - the read-only contract must raise
        raise AssertionError("conditioning view allowed a write attempt")


def test_forbidden_source_to_psychology_conversion_is_refused() -> None:
    view = bind_conditioning(
        subject=ACTOR_ID,
        sources=build_conditioning_sources(),
        as_of=20,
        requested_conversions={"structural_position_to_trait": True},
    )
    assert view.status is ConditioningStatus.REFUSED
    assert view.reason is ConditioningReason.FORBIDDEN_CONVERSION


def test_observer_note_to_belief_conversion_is_refused() -> None:
    view = bind_conditioning(
        subject=ACTOR_ID,
        sources=build_conditioning_sources(),
        as_of=20,
        requested_conversions={"observer_note_to_belief": True},
    )
    assert view.status is ConditioningStatus.REFUSED
    assert view.guard_reason == "OBSERVER_TO_BELIEF"


def test_unsealed_source_is_refused() -> None:
    source = make_conditioning_source(
        source_ref="TEST_ONLY_PERSON_STATE:standing",
        source_class="ResolvedStructuralContext",
        subject=ACTOR_ID,
    )
    broken = dict(source)
    broken["hash"] = "0" * 64
    view = bind_conditioning(subject=ACTOR_ID, sources=[broken], as_of=20)
    assert view.status is ConditioningStatus.REFUSED
    assert view.reason is ConditioningReason.SOURCE_UNSEALED


def test_foreign_subject_source_is_refused() -> None:
    source = make_conditioning_source(
        source_ref="TEST_ONLY_PERSON_STATE:standing",
        source_class="ResolvedStructuralContext",
        subject="OTHER_ACTOR",
    )
    view = bind_conditioning(subject=ACTOR_ID, sources=[source], as_of=20)
    assert view.status is ConditioningStatus.REFUSED
    assert view.reason is ConditioningReason.BUNDLE_INTEGRITY_FAILURE


def test_unauthorized_source_class_is_refused() -> None:
    source = make_conditioning_source(
        source_ref="TEST_ONLY_PYAT_RAW:wave",
        source_class="PYAT_RAW_SOURCE",
        subject=ACTOR_ID,
    )
    view = bind_conditioning(subject=ACTOR_ID, sources=[source], as_of=20)
    assert view.status is ConditioningStatus.REFUSED
    assert view.reason is ConditioningReason.SOURCE_CLASS_UNAUTHORIZED
