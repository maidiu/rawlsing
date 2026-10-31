"""Generation readiness adapted from the historical V3 accumulator."""

from __future__ import annotations

from typing import Any, Iterable

from v3.core.generation_integrity import (
    GenerationIntegrityAccumulator,
    IntegrityStatus,
)

from .contracts import EventDisposition, Status, StepOutcome

BLOCKING_STATUSES = frozenset(
    {
        Status.HELD_FORBIDDEN_DEFAULT,
        Status.HELD_RENDERER_MUTATION,
        Status.HELD_DERIVED_MUTATION,
        Status.HELD_TRANSACTION_ABORTED,
        Status.BLOCKED_AUTHORITY,
    }
)

READINESS = {
    IntegrityStatus.CLEAN: "CLEAN_READY_TEST_ONLY",
    IntegrityStatus.DEGRADED: "DEGRADED_READY_TEST_ONLY",
    IntegrityStatus.BLOCKED: "BLOCKED",
}


class HistoricalReadiness:
    """Readiness verdict with a source-free authority label."""

    def __init__(self) -> None:
        self.accumulator = GenerationIntegrityAccumulator()

    def record(
        self,
        stage: str,
        status: str,
        *,
        reason: str,
        fields_impacted: Iterable[str] = (),
        details: dict[str, Any] | None = None,
    ) -> None:
        self.accumulator.record(
            stage,
            status,
            fallback_used=status != IntegrityStatus.CLEAN,
            fallback_reason=reason,
            fields_impacted=list(fields_impacted),
            chat_surface_impact="none" if status == IntegrityStatus.CLEAN else "degraded",
            details=details or {},
        )

    def from_outcomes(
        self,
        dispositions: Iterable[EventDisposition],
        steps: Iterable[StepOutcome],
    ) -> dict[str, Any]:
        dispositions = tuple(dispositions)
        steps = tuple(steps)
        for item in dispositions:
            if item.status in BLOCKING_STATUSES:
                self.record(
                    "event_admission",
                    IntegrityStatus.BLOCKED,
                    reason=item.status.value,
                    fields_impacted=("events_this_year", "capacity", "material_facts"),
                    details={"event_id": item.event_id, "reason": item.reason},
                )
            elif item.status not in {Status.APPLIED_TEST_ONLY_SOURCEFREE, Status.NO_CHANGE_EVALUATED}:
                self.record(
                    "event_admission",
                    IntegrityStatus.DEGRADED,
                    reason=item.status.value,
                    fields_impacted=("events_this_year",),
                    details={"event_id": item.event_id, "reason": item.reason},
                )
        for step in steps:
            if step.status in BLOCKING_STATUSES:
                self.record(
                    "annual_step",
                    IntegrityStatus.BLOCKED,
                    reason=step.status.value,
                    fields_impacted=(step.step_id,),
                    details=dict(step.details),
                )
            elif step.status in {Status.HELD_MISSING_ISSUED_RULE, Status.HELD_CONSERVED_CHARGE_MODEL}:
                self.record(
                    "annual_step",
                    IntegrityStatus.DEGRADED,
                    reason=step.status.value,
                    fields_impacted=(step.step_id,),
                    details=dict(step.details),
                )
        verdict = self.accumulator.verdict()
        return {
            **verdict,
            "readiness": READINESS.get(verdict["overall_status"], "BLOCKED"),
            "authority": "TEST_ONLY_SOURCEFREE_NOT_NATIVE_NOT_SCIENCE",
        }
