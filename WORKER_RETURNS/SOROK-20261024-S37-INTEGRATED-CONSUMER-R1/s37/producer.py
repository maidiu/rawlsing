"""One actual chain: M35 B-source/C8/OUT9 -> S36 C9 -> targetless binding.

This is a TEST_ONLY adapter. It does not issue a CAN008/CAN011 rule, grant or
native event. The M35 producer remains the source of the B/E1/C8 occurrence; the
accepted S36 pipeline remains the source of the observed-response receipt and
the no-target decision.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .bootstrap import CUTS, install

install()

import firstclass  # noqa: E402
from bp2_joined import JoinedProducer, ports  # noqa: E402
from bp2_joined.producer import (  # noqa: E402
    make_actor_record,
    make_conditioning_source,
    make_e1_event,
)
from candidate import (  # noqa: E402
    CandidateStore,
    LaterActionConsumer,
    ResponseRule,
    ResponseRuleRegistry,
    TargetRuleRegistry,
    digest,
)
from candidate.actor_access_response import (  # noqa: E402
    OBSERVED_CURRENT_REFUSAL,
    OBSERVED_IMMEDIATE_OBJECT_ORIENTATION,
    S35ActorAccessRequest,
    make_actor_local_access_witness,
    make_actor_owned_response_witness,
)
from candidate.pipeline import run_candidate_path  # noqa: E402

RULE_ID = "TEST_ONLY_S37_CAN008_A"
RULE_AUTHORITY = "TEST_ONLY_S37_CAN008"
RULE_VERSION = "1"
RULE_CONTENT_HASH = digest({"test_only": "S37_S36_ACCESS_RESPONSE_RULE"})
RULE_ISSUER = "TEST_ONLY_S37_RESPONSE_OWNER"
GRADE = "TEST_ONLY_SOURCEFREE_TECHNICAL"
READER_ID = "TEST_ONLY_S37_TARGETLESS_READER"
_AUTO = object()


class S37Refusal(ValueError):
    """A typed S37 integration refusal."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def _rule(actor_id: str) -> ResponseRule:
    return ResponseRule(
        RULE_ID,
        RULE_VERSION,
        RULE_CONTENT_HASH,
        RULE_AUTHORITY,
        "1",
        RULE_ISSUER,
        True,
        (actor_id,),
        ("ADP017_ACTOR_LOCAL_ACCESS", "A_ACTOR_PERFORMED_IMMEDIATE_RESPONSE"),
        GRADE,
        (
            "source_bound_actor_local_e1_access",
            "separately_witnessed_actor_owned_response",
            "zero_target_proposals",
        ),
    )


class IntegratedProducer(JoinedProducer):
    """M35 producer stages plus the actual accepted S36 C9 evaluation."""

    def __init__(self, root, *, case: Mapping[str, Any], source=None,
                 variant: str = "A_REPAIR_LONG") -> None:
        self.case = case
        self.variant = variant
        self.source = firstclass.validate_source(
            source or firstclass.source_from_case(dict(case)), case
        )
        self.source_root = Path(root)
        self.source_root.mkdir(parents=True, exist_ok=True)
        life = firstclass.prepare_life(self.source, variant)
        super().__init__(
            self.source_root / "bp2", material_source=self.source, life=life
        )
        self.operation = self.source["b_operation"]
        self.material_access = (
            "granted" if self.operation == "SHARE_TOOL" else "denied"
        )
        self.access_witness: Mapping[str, Any] | None = None
        self.response_witness: Mapping[str, Any] | None = None
        self.conditioning_source: Mapping[str, Any] | None = None
        self.e1 = None
        self.e1_event = None
        self.actor_record = None
        self.response_rule = None
        self.pipeline = None
        self.s36_binding: dict | None = None
        self.last_store: CandidateStore | None = None

    def stage_m35(self) -> "IntegratedProducer":
        self.stage_world()
        self.stage_c8()
        self.stage_out9()
        self._bind_e1()
        return self

    def _bind_e1(self) -> None:
        occurrence = self.occurrence
        out9 = self.out9
        self.e1 = ports.ADP019EventPort().bind_test_only_e1(
            occurrence={
                "occurrence_id": out9.occurrence_id,
                "identity_digest": out9.event.get("identity_digest"),
                "_state_digest": out9.readset["state_digest"],
                "_commit_receipt_id": out9.readset["commit_receipt_id"],
                "_writer_version": out9.readset["writer_version"],
            },
            event_time=self.event_time,
            verified_proof=out9.verified_proof,
        )
        self.actor_record = make_actor_record(occurrence, occurrence.actor_snapshot)
        self.e1_event = make_e1_event(
            occurrence, out9, self.e1, time=self.event_time
        )
        self.conditioning_source = make_conditioning_source(
            occurrence, as_of=self.as_of, access=self.material_access
        )
        self.response_rule = _rule(occurrence.actor_id)

    def _default_access(self) -> dict:
        return make_actor_local_access_witness(
            actor_id=self.occurrence.actor_id,
            event_ref=self.e1_event["hash"],
            access_time=self.event_time,
            source_ref="TEST_ONLY_ADP017_ACCESS_S37_" + self.operation,
            access_status="ACCESSIBLE",
            scene=self.e1_event["content"]["scene"],
            content={
                "c8_occurrence_id": self.out9.occurrence_id,
                "c8_state_digest": self.out9.readset["state_digest"],
                "source_b_event_hash": self.source["b_event_hash"],
                "material_access": self.material_access,
            },
        )

    def _default_response(self) -> dict:
        kind = (
            "REQUEST_TOOL"
            if self.operation == "SHARE_TOOL"
            else "EXPLICIT_REFUSAL"
        )
        public_surface = (
            "REQUEST_TOOL_WITHIN_CURRENT_MATERIAL_CONTEXT"
            if self.operation == "SHARE_TOOL"
            else "EXPLICIT_REFUSAL_DUE_TO_CURRENT_TOOL_SHORTAGE"
        )
        return make_actor_owned_response_witness(
            actor_id=self.occurrence.actor_id,
            event_ref=self.e1_event["hash"],
            response_ref="TEST_ONLY_S37_A_" + kind,
            response_kind=kind,
            response_time=self.event_time + 1,
            source_ref="TEST_ONLY_A_RESPONSE_S37_" + self.operation,
            content={
                "c8_occurrence_id": self.out9.occurrence_id,
                "public_surface": public_surface,
                "actor_knows_b_motive": False,
            },
        )

    def evaluate_s36(
        self,
        *,
        store: CandidateStore | None = None,
        access_witness: Any = _AUTO,
        response_witness: Any = _AUTO,
        contradictory_context: bool = False,
        contradictory_refs: tuple[str, ...] = (),
        revoked_source_refs: frozenset[str] = frozenset(),
    ):
        if self.e1_event is None:
            raise S37Refusal("M35_STAGE_NOT_READY")
        target = store or self.c9
        access = self._default_access() if access_witness is _AUTO else access_witness
        response = (
            self._default_response()
            if response_witness is _AUTO
            else response_witness
        )
        request = S35ActorAccessRequest(
            access_witness=access,
            response_witness=response,
            contradictory_context=contradictory_context,
            contradictory_refs=tuple(contradictory_refs),
            revoked_source_refs=frozenset(revoked_source_refs),
        )
        pipeline = run_candidate_path(
            store=target,
            actor_raw=self.actor_record,
            event_raw=self.e1_event,
            conditioning_sources=[self.conditioning_source],
            response_registry=ResponseRuleRegistry.test_only((self.response_rule,)),
            target_registry=TargetRuleRegistry.production(),
            authority_id=self.response_rule.authority_id,
            rule_version=self.response_rule.rule_version,
            rule_content_hash=self.response_rule.rule_content_hash,
            as_of=self.as_of,
            permitted_issuer_refs=frozenset(),
            other_person_offer_ref="",
            material_opportunity_ref="",
            enacted_history_refs=(),
            later_consumer=LaterActionConsumer(
                READER_ID, "committed_target_state"
            ),
            later_as_of=self.later_as_of,
            target_permission=None,
            action_owner_receipt=None,
            expected_act="",
            s35_request=request,
        )
        self.last_store = target
        self.access_witness = access
        self.response_witness = response
        return pipeline

    def stage_s36(self) -> Any:
        pipeline = self.evaluate_s36(store=self.c9)
        if not pipeline.committed:
            raise S37Refusal("S36_C9_NOT_COMMITTED", pipeline.response.reason)
        if pipeline.response.status.value != "RESPONSE_COMMITTED":
            raise S37Refusal("S36_RESPONSE_NOT_POSITIVE", pipeline.response.reason)
        if pipeline.response.reason not in (
            OBSERVED_IMMEDIATE_OBJECT_ORIENTATION,
            OBSERVED_CURRENT_REFUSAL,
        ):
            raise S37Refusal("S36_RESPONSE_NOT_OBSERVED", pipeline.response.reason)
        if pipeline.response.target_proposals:
            raise S37Refusal("S36_TARGET_PROPOSALS_PRESENT")
        if pipeline.decision.branch.value != "NO_CHANGE":
            raise S37Refusal("S36_TARGET_NOT_NO_CHANGE")
        if pipeline.decision.reason.value != "NO_PROPOSAL":
            raise S37Refusal("S36_TARGET_NOT_NO_PROPOSAL")
        if pipeline.decision.target_id:
            raise S37Refusal("S36_TARGET_ID_PRESENT")
        if self.c9.committed_target_ids():
            raise S37Refusal("S36_TARGET_ROWS_PRESENT")
        self.pipeline = pipeline
        self.s36_binding = self._make_s36_binding(pipeline)
        return pipeline

    def _make_s36_binding(self, pipeline) -> dict:
        c9_path = Path(self.c9.path)
        try:
            relpath = str(c9_path.relative_to(self.source_root))
        except ValueError:
            relpath = str(c9_path)
        return {
            "schema": "SOROK_S37_S36_COMMITTED_RESPONSE_BINDING@1",
            "grade": "TEST_ONLY_SOURCEFREE_NOT_NATIVE",
            "e1_event_id": self.e1_event["event_id"],
            "e1_event_hash": self.e1_event["hash"],
            "actor_id": self.occurrence.actor_id,
            "source_b_event_hash": self.source["b_event_hash"],
            "source_operation": self.operation,
            "material_access": self.material_access,
            "access_witness_hash": self.access_witness["hash"]
            if self.access_witness
            else "",
            "access_source_ref": self.access_witness.get("source_ref", "")
            if self.access_witness
            else "",
            "access_source_hash": self.access_witness.get("source_hash", "")
            if self.access_witness
            else "",
            "response_witness_hash": self.response_witness["hash"]
            if self.response_witness
            else "",
            "response_source_ref": self.response_witness.get("source_ref", "")
            if self.response_witness
            else "",
            "response_source_hash": self.response_witness.get("source_hash", "")
            if self.response_witness
            else "",
            "response_kind": self.response_witness.get("response_kind", "")
            if self.response_witness
            else "",
            "response_ref": pipeline.receipt.response_ref,
            "response_receipt_hash": pipeline.response.receipt_hash,
            "c9_receipt_hash": pipeline.receipt.receipt_hash,
            "s35_outcome": pipeline.response.reason,
            "target_branch": pipeline.decision.branch.value,
            "target_reason": pipeline.decision.reason.value,
            "target_id": pipeline.decision.target_id,
            "target_proposals": len(pipeline.response.target_proposals),
            "c9_db_path": str(c9_path),
            "c9_db_relpath": relpath,
        }

    def c8_binding(self) -> dict:
        return {
            "occurrence_id": self.out9.occurrence_id,
            "journal_path": str(self.env.journal_path),
            "key_path": str(self.env.key_path),
            "key_id": self.env.key_store.key_id,
            "anchor_log": str(self.env.anchor.log_path),
            "anchor_watermark": str(self.env.anchor.watermark_path),
            "c8_state_digest": self.out9.readset["state_digest"],
            "c8_content_hash": self.out9.event.get("content_hash"),
            "c8_commit_receipt_id": self.out9.readset["commit_receipt_id"],
            "c8_writer_version": self.out9.readset["writer_version"],
            "e1_event_hash": self.e1_event["hash"],
            "e1_event_id": self.e1_event["event_id"],
        }

    def source_map(self) -> dict:
        return {
            "TEST_ONLY_R31J_A": self.occurrence.actor_id,
            "TEST_ONLY_R31J_B": self.occurrence.other_id,
        }

    def close(self) -> None:
        super().close()


__all__ = [
    "GRADE",
    "IntegratedProducer",
    "RULE_AUTHORITY",
    "RULE_CONTENT_HASH",
    "RULE_ID",
    "RULE_ISSUER",
    "S37Refusal",
]
