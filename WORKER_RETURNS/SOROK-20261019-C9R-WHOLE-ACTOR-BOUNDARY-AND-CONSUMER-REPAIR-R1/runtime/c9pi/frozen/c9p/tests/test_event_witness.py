"""(b) Precipitating event witness ingress tests including typed missing witnesses."""
from __future__ import annotations

from conftest import build_event_witness
from candidate.events import (
    GRADE_MISSING,
    GRADE_NATIVE,
    GRADE_TEST_ONLY,
    WitnessReason,
    WitnessStatus,
    ingress_event,
    make_event_witness,
)


def test_admitted_test_only_witness_binds_owner_readset() -> None:
    witness = build_event_witness()
    result = ingress_event(
        witness, as_of=20, last_time=0, prior_event_hashes=frozenset()
    )
    assert result.status is WitnessStatus.ADMITTED
    assert result.reason is WitnessReason.OK
    assert result.admission_grade == GRADE_TEST_ONLY
    assert result.owner_ref == "TEST_ONLY_EVENT_OWNER"
    assert "TEST_ONLY_EVENT_OWNER" in result.readset_refs


def test_native_witness_without_owner_receipt_is_typed_missing() -> None:
    witness = make_event_witness(
        event_id="event-native-e1",
        owner_ref="REAL_ADP019_OWNER",
        time=15,
        content={"fact": "transit_strike"},
        actor_role="ACTOR_A",
        admission_grade=GRADE_NATIVE,
    )
    result = ingress_event(
        witness, as_of=20, last_time=0, prior_event_hashes=frozenset()
    )
    assert result.status is WitnessStatus.MISSING
    assert result.reason is WitnessReason.MISSING_ADP019_OWNER_RECEIPT


def test_typed_missing_grade_returns_missing_not_fabricated_event() -> None:
    witness = make_event_witness(
        event_id="event-absent",
        owner_ref="TEST_ONLY_EVENT_OWNER",
        time=15,
        content={"fact": "absent"},
        actor_role="ACTOR_A",
        admission_grade=GRADE_MISSING,
    )
    result = ingress_event(
        witness, as_of=20, last_time=0, prior_event_hashes=frozenset()
    )
    assert result.status is WitnessStatus.MISSING
    assert result.event_hash == ""


def test_clock_outside_frame_is_refused() -> None:
    witness = build_event_witness(time=25)
    result = ingress_event(
        witness, as_of=20, last_time=0, prior_event_hashes=frozenset()
    )
    assert result.status is WitnessStatus.REFUSED
    assert result.reason is WitnessReason.CLOCK_OUTSIDE_FRAME


def test_time_reversed_is_refused() -> None:
    witness = build_event_witness(time=15)
    result = ingress_event(
        witness, as_of=20, last_time=15, prior_event_hashes=frozenset()
    )
    assert result.status is WitnessStatus.REFUSED
    assert result.reason is WitnessReason.TIME_REVERSED


def test_unresolved_causal_parent_is_refused() -> None:
    witness = build_event_witness(causal_parent_refs=("UNKNOWN_PARENT",))
    result = ingress_event(
        witness, as_of=20, last_time=0, prior_event_hashes=frozenset()
    )
    assert result.status is WitnessStatus.REFUSED
    assert result.reason is WitnessReason.CAUSAL_PARENT_UNRESOLVED


def test_resolved_causal_parent_is_admitted() -> None:
    parent = build_event_witness(event_id="event-parent", time=5)
    parent_hash = ingress_event(
        parent, as_of=20, last_time=0, prior_event_hashes=frozenset()
    ).event_hash
    child = build_event_witness(
        event_id="event-child", time=10, causal_parent_refs=(parent_hash,)
    )
    result = ingress_event(
        child, as_of=20, last_time=5, prior_event_hashes=frozenset({parent_hash})
    )
    assert result.status is WitnessStatus.ADMITTED


def test_test_only_owner_grade_mismatch_is_refused() -> None:
    witness = make_event_witness(
        event_id="event-foreign",
        owner_ref="FOREIGN_OWNER",
        time=15,
        content={"fact": "x"},
        actor_role="ACTOR_A",
        admission_grade=GRADE_TEST_ONLY,
    )
    result = ingress_event(
        witness, as_of=20, last_time=0, prior_event_hashes=frozenset()
    )
    assert result.status is WitnessStatus.REFUSED
    assert result.reason is WitnessReason.OWNER_GRADE_MISMATCH
