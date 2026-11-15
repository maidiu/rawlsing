"""Complete C9R candidate transaction/consumer path (E1 -> RULE_A -> RULE_T -> E2).

One anti-shadow entrypoint runs actor ingress, event-witness ingress, read-only
conditioning with material eligibility, CAN008 response-rule lookup, separately
authorized CAN011 target evaluation, atomic full-record commit, a named later
E2 committed-state read and performed-action admission. Every stage returns a
typed result; a refusal at any stage stops the chain with no ghost state.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .action_admission import (
    OccurrenceResolver,
    PerformedActionAdmission,
    PerformedActionHold,
    admit_performed_action,
)
from .conditioning import (
    ConditioningReason,
    ConditioningStatus,
    ConditioningView,
    bind_conditioning,
    eligible_material,
)
from .events import (
    EventWitnessResult,
    OwnerReceiptResolver,
    WitnessStatus,
    ingress_event,
)
from .identity import (
    ActorIngressResult,
    ActorSourceResolver,
    IngressStatus,
    ingress_actor,
)
from .actor_access_response import (
    S35ActorAccessRequest,
    evaluate_actor_access_response,
)
from .later_action import LaterActionConsumer, LaterActionRead, read_target_for_later_action
from .response_rules import (
    ResponseResult,
    ResponseRuleRegistry,
    ResponseStatus,
    evaluate_response,
    lookup_rule,
)
from .target_rules import (
    TargetBranch,
    TargetDecision,
    TargetReason,
    TargetRuleRegistry,
    evaluate_target,
)
from .canon import seal
from .transaction import CandidateStore, CommitReceipt, TransactionRefusal


@dataclass(frozen=True)
class PipelineStage:
    """One named stage result in the candidate transaction path."""

    stage: str
    ok: bool
    reason: str
    detail: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PipelineResult:
    """Full result of one candidate transaction/consumer path execution."""

    stages: tuple[PipelineStage, ...]
    actor: ActorIngressResult | None
    event: EventWitnessResult | None
    conditioning: ConditioningView | None
    response: ResponseResult | None
    decision: TargetDecision | None
    receipt: CommitReceipt | None
    later_read: LaterActionRead | None
    action_admission: PerformedActionAdmission | PerformedActionHold | None
    committed: bool
    no_ghost: bool
    material_eligible: bool = False
    material_reason: str = ""
    authorization_hash: str = ""
    target_id: str = ""

    def stage(self, name: str) -> PipelineStage | None:
        for item in self.stages:
            if item.stage == name:
                return item
        return None


def _abort(
    stages: list[PipelineStage],
    **values: Any,
) -> PipelineResult:
    base = dict(
        stages=tuple(stages),
        actor=None,
        event=None,
        conditioning=None,
        response=None,
        decision=None,
        receipt=None,
        later_read=None,
        action_admission=None,
        committed=False,
        no_ghost=True,
    )
    base.update(values)
    return PipelineResult(**base)


def run_candidate_path(
    *,
    store: CandidateStore,
    actor_raw: Mapping[str, Any],
    event_raw: Mapping[str, Any],
    conditioning_sources: list[Mapping[str, Any]],
    response_registry: ResponseRuleRegistry,
    target_registry: TargetRuleRegistry,
    authority_id: str,
    rule_version: str,
    rule_content_hash: str,
    as_of: int,
    permitted_issuer_refs: frozenset[str],
    other_person_offer_ref: str,
    material_opportunity_ref: str,
    enacted_history_refs: tuple[str, ...],
    later_consumer: LaterActionConsumer | None,
    later_as_of: int,
    target_permission: Mapping[str, Any] | None = None,
    action_owner_receipt: Mapping[str, Any] | None = None,
    expected_act: str = "",
    request_is_self_issued: bool = False,
    fault: str | None = None,
    actor_resolver: ActorSourceResolver | None = None,
    owner_resolver: OwnerReceiptResolver | None = None,
    occurrence_resolver: OccurrenceResolver | None = None,
    native_positive_claim: bool = False,
    s35_request: S35ActorAccessRequest | None = None,
) -> PipelineResult:
    """Execute one complete candidate transaction/consumer path."""
    stages: list[PipelineStage] = []
    actor = ingress_actor(actor_raw, as_of=as_of, resolver=actor_resolver)
    stages.append(
        PipelineStage(
            "actor_ingress",
            actor.admitted,
            actor.reason.value,
            {
                "actor_id": actor.actor_id,
                "source_grade": actor.source_grade,
                "readset_refs": list(actor.readset_refs),
            },
        )
    )
    if not actor.admitted:
        return _abort(stages, actor=actor)
    prior_events = store.committed_event_hashes()
    event = ingress_event(
        event_raw,
        as_of=as_of,
        last_time=store.last_clock(),
        prior_event_hashes=prior_events,
        focal_actor_id=actor.actor_id,
        owner_resolver=owner_resolver,
    )
    stages.append(
        PipelineStage(
            "event_witness_ingress",
            event.admitted,
            event.reason.value,
            {
                "event_id": event.event_id,
                "event_hash": event.event_hash,
                "admission_grade": event.admission_grade,
            },
        )
    )
    if not event.admitted:
        return _abort(stages, actor=actor, event=event)
    conditioning = bind_conditioning(
        subject=actor.actor_id,
        sources=conditioning_sources,
        as_of=as_of,
    )
    stages.append(
        PipelineStage(
            "conditioning_read_only",
            conditioning.bound,
            conditioning.reason.value,
            {
                "guard_outcome": conditioning.guard_outcome,
                "readset_refs": list(conditioning.readset_refs),
            },
        )
    )
    if not conditioning.bound:
        return _abort(stages, actor=actor, event=event, conditioning=conditioning)
    material_ok, material_refs, material_reason = eligible_material(
        conditioning,
        event_scene=event.scene,
        event_time=event.event_time,
        as_of=as_of,
    )
    stages.append(
        PipelineStage(
            "material_eligibility",
            material_ok,
            material_reason,
            {"eligible_material_refs": list(material_refs)},
        )
    )
    rule_lookup = lookup_rule(
        response_registry,
        authority_id=authority_id,
        rule_version=rule_version,
        rule_content_hash=rule_content_hash,
        subject=actor.actor_id,
    )
    if s35_request is None:
        response = evaluate_response(
            rule_lookup=rule_lookup,
            event_ref=event.event_hash,
            event_time=event.event_time,
            subject=actor.actor_id,
            conditioning_readset=conditioning.readset_refs,
            actor_history_refs=enacted_history_refs,
            other_person_offer_ref=other_person_offer_ref,
            material_opportunity_ref=material_opportunity_ref,
            prior_response_count=0,
            material_eligible=material_ok,
            eligible_material_refs=material_refs,
        )
    else:
        response = evaluate_actor_access_response(
            rule_lookup=rule_lookup,
            event_ref=event.event_hash,
            event_time=event.event_time,
            subject=actor.actor_id,
            request=s35_request,
            conditioning_readset=conditioning.readset_refs,
            event_scene=event.scene,
            as_of=as_of,
            material_eligible=material_ok,
            eligible_material_refs=material_refs,
        )
    stages.append(
        PipelineStage(
            "can008_response_rule_lookup",
            response.status
            in (ResponseStatus.RESPONSE_COMMITTED, ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY),
            response.reason,
            {
                "rule_status": rule_lookup.status.value,
                "response_status": response.status.value,
                "target_proposals": len(response.target_proposals),
                "s35_bridge": s35_request is not None,
            },
        )
    )
    if s35_request is not None and response.status in (
        ResponseStatus.REFUSED,
        ResponseStatus.HELD,
    ):
        stages.append(
            PipelineStage(
                "s35_response_refusal",
                False,
                response.reason,
                {"no_target_proposals": True, "no_occurrence_or_response_commit": True},
            )
        )
        return _abort(
            stages,
            actor=actor,
            event=event,
            conditioning=conditioning,
            response=response,
            material_eligible=material_ok,
            material_reason=material_reason,
        )
    if store.event_identity_conflict(event_raw):
        stages.append(
            PipelineStage(
                "occurrence_admission",
                False,
                "EVENT_IDENTITY_CONFLICT",
                {"event_id": event.event_id},
            )
        )
        return _abort(
            stages,
            actor=actor,
            event=event,
            conditioning=conditioning,
            response=response,
            material_eligible=material_ok,
            material_reason=material_reason,
        )
    try:
        store.admit_occurrence(event_raw)
        admitted = True
        admission_reason = "OK"
    except TransactionRefusal as error:
        admitted = False
        admission_reason = error.code
    stages.append(
        PipelineStage(
            "occurrence_admission",
            admitted,
            admission_reason,
            {"event_hash": event.event_hash},
        )
    )
    if not admitted:
        return _abort(
            stages,
            actor=actor,
            event=event,
            conditioning=conditioning,
            response=response,
            material_eligible=material_ok,
            material_reason=material_reason,
        )
    proposal = response.target_proposals[0] if response.target_proposals else None
    before_target_hash = store.target_state_hash()
    decision = evaluate_target(
        registry=target_registry,
        proposal=proposal,
        permission=target_permission,
        actor_id=actor.actor_id,
        before_target_hash=before_target_hash,
        existing_target_ids=store.committed_target_ids(),
        prior_event_hash=event.event_hash,
        as_of=as_of,
        enacted_history_refs=enacted_history_refs,
        permitted_issuer_refs=permitted_issuer_refs,
        request_is_self_issued=request_is_self_issued,
        response_hash=response.receipt_hash,
        native_positive_claim=native_positive_claim,
    )
    stages.append(
        PipelineStage(
            "can011_target_evaluation",
            decision.branch is not TargetBranch.DENY
            or decision.reason
            in (
                TargetReason.TARGET_RULE_ABSENT,
                TargetReason.TARGET_RULE_UNISSUED,
                TargetReason.PERMISSION_MISSING,
                TargetReason.NO_PROPOSAL,
            ),
            decision.reason.value,
            {
                "branch": decision.branch.value,
                "proposal_hash": decision.proposal_hash,
                "target_id": decision.target_id,
                "publication_grade": decision.publication_grade,
            },
        )
    )
    readset = tuple(
        [event.event_hash, *conditioning.readset_refs, *enacted_history_refs]
        + list(decision.readset_refs)
    )
    response_body = {
        "event_ref": event.event_hash,
        "status": response.status.value,
        "rule_status": rule_lookup.status.value,
        "rule_content_hash": rule_lookup.rule_content_hash,
        "receipt_hash": response.receipt_hash,
        "candidate_route": response.candidate_route,
        "declared_history_refs": list(response.declared_history_refs),
        "declared_offer_ref": response.declared_offer_ref,
        "eligible_material_refs": list(response.eligible_material_refs),
        "target_proposal_ref": proposal.get("hash", "") if proposal else "",
        "publication_grade": decision.publication_grade,
    }
    if s35_request is not None:
        response_body["s35_receipt"] = dict(response.s35_receipt or {})
    response_record = seal(response_body)
    try:
        receipt = store.commit(
            event=event_raw,
            response=response_record,
            decision=decision,
            readset_refs=readset,
            fault=fault,
        )
    except TransactionRefusal as error:
        stages.append(
            PipelineStage("atomic_commit", False, error.code, {"no_mutation": True})
        )
        return _abort(
            stages,
            actor=actor,
            event=event,
            conditioning=conditioning,
            response=response,
            decision=decision,
            committed=False,
            no_ghost=True,
            material_eligible=material_ok,
            material_reason=material_reason,
            authorization_hash=decision.authorization_hash,
            target_id=decision.target_id,
        )
    stages.append(
        PipelineStage(
            "atomic_commit",
            receipt.committed,
            receipt.status,
            {
                "before_hash": receipt.before_hash,
                "after_hash": receipt.after_hash,
                "no_mutation": receipt.no_mutation,
            },
        )
    )
    later_read = read_target_for_later_action(
        store,
        consumer=later_consumer,
        middle_state_id=decision.target_id or decision.proposal_hash,
        as_of=later_as_of,
        commit_time=event.event_time,
        action_admission_owner_ref="",
        expected_actor_id=actor.actor_id,
        expected_act=expected_act,
    )
    stages.append(
        PipelineStage(
            "later_action_target_read",
            later_read.status.value in ("READ_OK", "ACTION_ADMISSION_HELD"),
            later_read.reason,
            {
                "consumer_id": later_read.consumer_id,
                "state_hash": later_read.state_hash,
                "read_receipt_hash": later_read.read_receipt_hash,
            },
        )
    )
    action_admission: PerformedActionAdmission | PerformedActionHold
    action_admission = admit_performed_action(
        owner_receipt=action_owner_receipt,
        expected_actor_id=actor.actor_id,
        expected_act=expected_act or "UNSPECIFIED_ACT",
        consumed_state_hash=later_read.state_hash,
        as_of=later_as_of,
        target_commit_time=event.event_time,
        occurrence_resolver=occurrence_resolver,
    )
    stages.append(
        PipelineStage(
            "performed_action_admission",
            getattr(action_admission, "admitted", False),
            action_admission.reason.value,
            {"status": action_admission.status.value},
        )
    )
    return PipelineResult(
        stages=tuple(stages),
        actor=actor,
        event=event,
        conditioning=conditioning,
        response=response,
        decision=decision,
        receipt=receipt,
        later_read=later_read,
        action_admission=action_admission,
        committed=receipt.committed,
        no_ghost=receipt.no_mutation or receipt.committed,
        material_eligible=material_ok,
        material_reason=material_reason,
        authorization_hash=decision.authorization_hash,
        target_id=decision.target_id,
    )


__all__ = ["PipelineResult", "PipelineStage", "run_candidate_path"]
