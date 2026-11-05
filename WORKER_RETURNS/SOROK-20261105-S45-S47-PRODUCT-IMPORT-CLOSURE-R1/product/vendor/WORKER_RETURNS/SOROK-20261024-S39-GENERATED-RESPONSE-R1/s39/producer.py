"""M35/S37 producer seam plus S39 source-bound generation."""
from __future__ import annotations

from typing import Any, Mapping

from .bootstrap import install

install()

from candidate import ResponseRuleRegistry, lookup_rule  # noqa: E402
from candidate.actor_access_response import (  # noqa: E402
    OBSERVED_CURRENT_REFUSAL,
    OBSERVED_IMMEDIATE_OBJECT_ORIENTATION,
    S35ActorAccessRequest,
    evaluate_actor_access_response,
    make_actor_owned_response_witness,
)
from s37.producer import IntegratedProducer  # noqa: E402

from .model import FULL_RULE, S39GenerationRefusal, generate_choice  # noqa: E402


class GeneratedProducer(IntegratedProducer):
    """S37 M35 producer plus a deterministic generated attempt request."""

    def __init__(self, root, *, case, source=None, variant="A_REPAIR_LONG"):
        super().__init__(root, case=case, source=source, variant=variant)
        self.generation_receipt: dict | None = None
        self.attempt_result: dict | None = None

    def generate(self, *, source_records, rule=FULL_RULE,
                 branch_id: str = "first_session") -> dict:
        if self.e1_event is None:
            raise S39GenerationRefusal("S39_M35_STAGE_NOT_READY")
        access = self._default_access()
        lookup = lookup_rule(
            ResponseRuleRegistry.test_only((self.response_rule,)),
            authority_id=self.response_rule.authority_id,
            rule_version=self.response_rule.rule_version,
            rule_content_hash=self.response_rule.rule_content_hash,
            subject=self.occurrence.actor_id,
        )
        access_probe = evaluate_actor_access_response(
            rule_lookup=lookup,
            event_ref=self.e1_event["hash"],
            event_time=self.event_time,
            subject=self.occurrence.actor_id,
            request=S35ActorAccessRequest(
                access_witness=access, response_witness=None
            ),
            conditioning_readset=(self.conditioning_source["source_ref"],),
            event_scene=self.e1_event["content"]["scene"],
            as_of=self.as_of,
            material_eligible=self.material_access == "granted",
            eligible_material_refs=(self.conditioning_source["source_ref"],),
        )
        state = self.occurrence.actor_snapshot.get("state", {})
        world = {
            "actor_present": True,
            "object_present": True,
            "tool_available": self.source["b_operation"] == "SHARE_TOOL",
            "material_available": int(state.get("material_remaining", 0)) > 0,
            "free_hours": int(state.get("free_hours", 0)) > 0,
        }
        receipt = generate_choice(
            actor_id=self.occurrence.actor_id,
            branch_id=branch_id,
            event_ref=self.e1_event["hash"],
            event_time=self.event_time,
            as_of=self.as_of,
            c8_state_digest=self.out9.readset["state_digest"],
            access_witness=access,
            access_outcome=access_probe.reason,
            source_records=list(source_records),
            world=world,
            rule=rule,
        )
        self.generation_receipt = receipt
        return receipt

    def response_witness_for_attempt(self, attempt_result: Mapping[str, Any]) -> dict | None:
        if not attempt_result.get("performed"):
            return None
        attempt_hash = attempt_result.get("hash", "")
        event_hash = attempt_result.get("event_hash", "")
        event_id = attempt_result.get("event_id", "")
        option = attempt_result["option_id"]
        return make_actor_owned_response_witness(
            actor_id=self.occurrence.actor_id,
            event_ref=self.e1_event["hash"],
            response_ref=event_id or attempt_hash,
            response_kind=attempt_result["s36_response_kind"],
            response_time=self.event_time + 1,
            source_ref="TEST_ONLY_A_RESPONSE_S39_" + option,
            content={
                "generation_receipt_hash": self.generation_receipt.get("hash", ""),
                "attempt_receipt_hash": attempt_hash,
                "attempt_event_id": event_id,
                "attempt_event_hash": event_hash,
                "option_id": option,
                "provenance": "TEST_ONLY_CONSTRUCTIVE_GENERATION_NOT_EXTERNALLY_OBSERVED",
                "admitted_action": True,
            },
        )

    def finalize_s36(self, *, attempt_result: Mapping[str, Any]):
        response = self.response_witness_for_attempt(attempt_result)
        pipeline = self.evaluate_s36(
            store=self.c9,
            access_witness=self._default_access(),
            response_witness=response,
        )
        if not pipeline.committed:
            raise S39GenerationRefusal("S39_C9_NOT_COMMITTED", pipeline.response.reason)
        if pipeline.response.target_proposals:
            raise S39GenerationRefusal("S39_TARGET_PROPOSALS_PRESENT")
        if pipeline.decision.branch.value != "NO_CHANGE":
            raise S39GenerationRefusal("S39_TARGET_NOT_NO_CHANGE")
        if pipeline.decision.reason.value != "NO_PROPOSAL":
            raise S39GenerationRefusal("S39_TARGET_NOT_NO_PROPOSAL")
        if self.c9.committed_target_ids():
            raise S39GenerationRefusal("S39_TARGET_ROWS_PRESENT")
        if attempt_result.get("performed"):
            if pipeline.response.status.value != "RESPONSE_COMMITTED":
                raise S39GenerationRefusal("S39_PERFORMED_NOT_OBSERVED", pipeline.response.reason)
            if pipeline.response.reason not in (
                OBSERVED_IMMEDIATE_OBJECT_ORIENTATION,
                OBSERVED_CURRENT_REFUSAL,
            ):
                raise S39GenerationRefusal("S39_PERFORMED_OUTCOME_INVALID", pipeline.response.reason)
        else:
            if pipeline.response.status.value != "RESPONSE_EFFECTS_VALID_EMPTY":
                raise S39GenerationRefusal("S39_DENIED_NOT_VALID_EMPTY")
            if pipeline.response.reason != "RECEIVABLE_NO_OBSERVED_UPTAKE":
                raise S39GenerationRefusal("S39_DENIED_OUTCOME_INVALID", pipeline.response.reason)
        self.pipeline = pipeline
        self.s36_binding = self._make_s36_binding(pipeline)
        return pipeline


__all__ = ["GeneratedProducer"]
