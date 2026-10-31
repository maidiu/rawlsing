"""Source-bound transition rules and the explicit missing-rule hold."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from v3.core.state import BackboneState

from .contracts import ActorResponse, ActorWorldEvent, MaterialDelta, SourceActorSnapshot, Status
from .provenance import source_hash


@dataclass(frozen=True)
class RuleResult:
    """Result of one transition-rule evaluation."""

    status: Status
    material_deltas: tuple[MaterialDelta, ...] = ()
    material_facts: Mapping[str, Any] = field(default_factory=dict)
    details: Mapping[str, Any] = field(default_factory=dict)
    reason: str = ""


@dataclass(frozen=True)
class TransitionRule:
    """A rule with explicit scientific and issuance status.

    ``scientific=False`` means the rule is an adapter accounting policy, not a
    developmental-science rule. ``issued=False`` on a scientific rule is HELD.
    """

    rule_id: str
    event_kind: str
    response_kind: str
    scientific: bool
    issued: bool
    authority: str
    description: str

    def matches(self, event: ActorWorldEvent, response: ActorResponse) -> bool:
        return event.kind == self.event_kind and response.kind == self.response_kind


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


class MaterialAccountingRule:
    """Record actual cash movement from a source-owned offscreen work event.

    This is not a psychological transition rule. It applies only recorded
    material deltas and verifies them against the consumer's before/after
    material snapshot.
    """

    spec = TransitionRule(
        rule_id="TEST_ONLY_MATERIAL_ACCOUNTING_OFFSCREEN_WORK@1",
        event_kind="OFFSCREEN_REPAIR",
        response_kind="PERFORMED_OFFSCREEN_WORK",
        scientific=False,
        issued=False,
        authority="TEST_ONLY_MATERIAL_ACCOUNTING_POLICY",
        description="Preserve recorded cash/material facts; no psychological field.",
    )

    def evaluate(
        self,
        event: ActorWorldEvent,
        response: ActorResponse,
        state: BackboneState,
        prior: SourceActorSnapshot,
        post: SourceActorSnapshot | None = None,
    ) -> RuleResult:
        if not self.spec.matches(event, response):
            return RuleResult(status=Status.HELD_MISSING_RULE, reason="rule_kind_mismatch")
        if not response.performed:
            return RuleResult(status=Status.HELD_MISSING_RESPONSE, reason="response_not_performed")
        if not event.source_owned or not bool(response.body.get("source_owned", event.source_owned)):
            return RuleResult(status=Status.HELD_ACCOUNTING_MISMATCH, reason="source_not_owned")
        cash_delta = _safe_float(event.body.get("cash_delta"))
        material_delta = _safe_float(event.body.get("material_delta"))
        if cash_delta == 0.0 and material_delta == 0.0:
            return RuleResult(status=Status.NO_CHANGE_EVALUATED, reason="recorded_material_delta_zero")
        if post is not None:
            actual_cash_delta = round(post.cash - prior.cash, 6)
            if actual_cash_delta != round(cash_delta, 6):
                return RuleResult(
                    status=Status.HELD_ACCOUNTING_MISMATCH,
                    reason=f"cash_delta={cash_delta} but consumer_delta={actual_cash_delta}",
                )
        before = float(state.capacity.money)
        after = max(0.0, min(100.0, before + cash_delta))
        delta = MaterialDelta(
            event_id=event.event_id,
            field="capacity.money",
            before=before,
            delta=cash_delta,
            after=after,
            source_fact_hash=source_hash(event.body),
        )
        facts = {
            "position": post.position if post is not None else event.location,
            "cash": post.cash if post is not None else prior.cash + cash_delta,
            "material_remaining": post.material_remaining if post is not None else prior.material_remaining,
            "free_hours": post.free_hours if post is not None else prior.free_hours,
            "completed_units": post.completed_units if post is not None else prior.completed_units,
            "skill": post.skill if post is not None else prior.skill,
            "debt_units": post.debt_units if post is not None else prior.debt_units,
            "tools_remaining": post.tools_remaining if post is not None else prior.tools_remaining,
            "material_delta": material_delta,
            "source_owned": True,
        }
        return RuleResult(
            status=Status.APPLIED_TEST_ONLY_SOURCEFREE,
            material_deltas=(delta,),
            material_facts=facts,
            details={
                "cash_delta": cash_delta,
                "material_delta": material_delta,
                "accounting_verified_against_consumer": post is not None,
            },
        )


class ZeroDeltaTestRule:
    """A genuinely evaluated test-only rule whose result is no change."""

    spec = TransitionRule(
        rule_id="TEST_ONLY_ZERO_DELTA_EVALUATION@1",
        event_kind="TEST_ONLY_ZERO_EVENT",
        response_kind="TEST_ONLY_ZERO_RESPONSE",
        scientific=False,
        issued=False,
        authority="TEST_ONLY_ZERO_RULE_NOT_SCIENCE",
        description="Evaluates to zero durable delta; distinct from a missing rule.",
    )

    def evaluate(
        self,
        event: ActorWorldEvent,
        response: ActorResponse,
        state: BackboneState,
        prior: SourceActorSnapshot,
        post: SourceActorSnapshot | None = None,
    ) -> RuleResult:
        if not self.spec.matches(event, response):
            return RuleResult(status=Status.HELD_MISSING_RULE, reason="rule_kind_mismatch")
        return RuleResult(status=Status.NO_CHANGE_EVALUATED, reason="rule_evaluated_zero_delta")


class UnissuedScientificRule:
    """A scientific-looking rule that has not been issued; it must remain HELD."""

    spec = TransitionRule(
        rule_id="UNISSUED_SCIENTIFIC_TRANSITION@1",
        event_kind="SCIENTIFIC_PENDING_EVENT",
        response_kind="SCIENTIFIC_PENDING_RESPONSE",
        scientific=True,
        issued=False,
        authority="NO_CAN_ADP_ISSUANCE",
        description="No issued scientific authority; no durable mutation.",
    )

    def evaluate(
        self,
        event: ActorWorldEvent,
        response: ActorResponse,
        state: BackboneState,
        prior: SourceActorSnapshot,
        post: SourceActorSnapshot | None = None,
    ) -> RuleResult:
        if not self.spec.matches(event, response):
            return RuleResult(status=Status.HELD_MISSING_RULE, reason="rule_kind_mismatch")
        return RuleResult(status=Status.HELD_RULE_NOT_ISSUED, reason="scientific_rule_not_issued")


class RuleRegistry:
    """Lookup of competent rules by event/response kind."""

    def __init__(self) -> None:
        self._rules: dict[tuple[str, str], Any] = {}

    def register(self, rule: Any) -> None:
        self._rules[(rule.spec.event_kind, rule.spec.response_kind)] = rule

    def lookup(self, event: ActorWorldEvent, response: ActorResponse) -> Any | None:
        return self._rules.get((event.kind, response.kind))

    def rule_ids(self) -> tuple[str, ...]:
        return tuple(sorted(rule.spec.rule_id for rule in self._rules.values()))


def default_registry() -> RuleRegistry:
    registry = RuleRegistry()
    registry.register(MaterialAccountingRule())
    registry.register(ZeroDeltaTestRule())
    registry.register(UnissuedScientificRule())
    return registry
