"""Second-event admission and generation over the same continuing person."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .bootstrap import install

install()

import firstclass  # noqa: E402
from bp2_joined.binding import (  # noqa: E402
    Out9Binding,
    WorldOccurrence,
    validate_occurrence_payload,
    verify_out9_against_source,
)
from c8_readonly_consumer import C8ReadOnlyConsumer  # noqa: E402
from c9_event_ingress import receive_event  # noqa: E402
from bp2_joined.producer import (  # noqa: E402
    make_actor_record,
    make_conditioning_source,
    make_e1_event,
)
from bp2_joined import ports  # noqa: E402
from candidate import (  # noqa: E402
    ResponseRuleRegistry,
    digest,
    lookup_rule,
    seal,
)
from candidate.actor_access_response import (  # noqa: E402
    S35ActorAccessRequest,
    evaluate_actor_access_response,
)
from s39.model import FULL_RULE, generate_choice  # noqa: E402
from s39.producer import GeneratedProducer  # noqa: E402
from s39.sources import make_source  # noqa: E402


class S41EventRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def world_prerequisites(session) -> dict:
    state = session.world().actor_state.get("A", {})
    workshop = session.world().resources.get("workshop", {})
    return {
        "actor_present": session.world().positions.get("A") == "workshop",
        "object_present": True,
        "tool_available": (
            int(state.get("tools_remaining", 0)) > 0
            and workshop.get("tool_available") is True
        ),
        "material_available": int(state.get("material_remaining", 0)) > 0,
        "free_hours": int(state.get("free_hours", 0)) > 0,
    }


def build_current_snapshot(session, first_binding: Mapping[str, Any]) -> dict:
    template = dict(session.product.seed.life.a_snapshot)
    template.pop("hash", None)
    state = dict(session.world().actor_state.get("A", {}))
    history_refs = [{
        "event_id": first_binding["e1_event_id"],
        "event_hash": first_binding["e1_event_hash"],
        "c8_occurrence_id": first_binding["c8"]["occurrence_id"],
    }]
    history_hash = digest({
        "prior_event_refs": history_refs,
        "prior_action_event_ids": [
            first_binding.get("action", {}).get("event_id", "")
        ],
        "world_clock": session.clock(),
    })
    performed = list(template.get("performed_action_refs", []))
    prior_action = first_binding.get("action", {}).get("event_id", "")
    if prior_action and prior_action not in performed:
        performed.append(prior_action)
    template.update({
        "state": state,
        "state_hash": digest(state),
        "last_clock": session.clock(),
        "history_hash": history_hash,
        "event_head": prior_action or first_binding["e1_event_hash"],
        "event_count": int(template.get("event_count", 0)) + 1,
        "performed_action_refs": performed,
    })
    template["hash"] = digest(template)
    return template


def build_second_occurrence(
    session,
    *,
    first_binding: Mapping[str, Any],
    first_payload: Mapping[str, Any],
    second_source: Mapping[str, Any],
    event_time: int,
) -> tuple[WorldOccurrence, dict]:
    current_snapshot = build_current_snapshot(session, first_binding)
    state = dict(session.world().actor_state.get("A", {}))
    payload = deepcopy(dict(first_payload))
    actor = dict(payload["actor"])
    actor.update({
        "state": state,
        "state_hash": current_snapshot["state_hash"],
        "snapshot_hash": current_snapshot["hash"],
        "history_hash": current_snapshot["history_hash"],
        "clock": session.clock(),
        "event_head": current_snapshot["event_head"],
        "performed_act_ref": current_snapshot["performed_action_refs"][-1]
        if current_snapshot["performed_action_refs"] else actor.get("performed_act_ref", ""),
    })
    payload["actor"] = actor
    world = dict(payload["world"])
    world.update({
        "material_ref": second_source["b_event_ref"],
        "material_receipt_id": second_source["b_event_hash"],
        "tool_available": world_prerequisites(session)["tool_available"],
        "material_remaining": state.get("material_remaining"),
        "prior_c8_occurrence_id": first_binding["c8"]["occurrence_id"],
        "prior_c8_content_hash": first_binding["c8"].get("c8_content_hash", ""),
        "prior_e1_ref": first_binding["e1_event_id"],
        "prior_e1_event_hash": first_binding["e1_event_hash"],
        "prior_action_event_ref": first_binding.get("action", {}).get("event_id", ""),
        "prior_c9_response_ref": first_binding["c9"]["response_ref"],
        "event_ordinal": 2,
    })
    payload["world"] = world
    payload["clock"] = int(event_time)
    payload["gm01_pre_c9_source"] = dict(second_source)
    payload["causal_parent_event_ids"] = [
        first_binding["e1_event_hash"],
        first_binding["c8"].get("c8_content_hash", ""),
    ]
    payload["s41_continuation"] = {
        "schema": "S41_CONTINUING_OCCURRENCE@1",
        "event_ordinal": 2,
        "branch_id": session.branch_id,
        "actor_id": actor["actor_id"],
        "prior_e1_ref": first_binding["e1_event_id"],
        "prior_e1_event_hash": first_binding["e1_event_hash"],
        "prior_c8_occurrence_id": first_binding["c8"]["occurrence_id"],
        "prior_c8_content_hash": first_binding["c8"].get("c8_content_hash", ""),
        "prior_action_event_ref": first_binding.get("action", {}).get("event_id", ""),
        "prior_c9_response_ref": first_binding["c9"]["response_ref"],
        "source_operation": second_source["b_operation"],
        "current_world_clock": session.clock(),
        "tool_available": world_prerequisites(session)["tool_available"],
        "material_remaining": state.get("material_remaining"),
        "actor_state_hash": digest(state),
        "history_refs": [first_binding["e1_event_id"], first_binding["e1_event_hash"]],
    }
    validate_occurrence_payload(payload)
    candidate = {
        "candidate_id": "S41-OCC-" + digest(payload)[:24].upper(),
        "payload": payload,
        "source_refs": [current_snapshot["source_ref"], payload["other_actor"]["source_ref"]],
        "causal_time": int(event_time),
    }
    occurrence = WorldOccurrence(
        actor_key="A",
        actor_id=actor["actor_id"],
        other_id=payload["other_actor"]["actor_id"],
        event_time=int(event_time),
        candidate=candidate,
        payload=payload,
        causal_parent_event_ids=tuple(payload["causal_parent_event_ids"]),
        actor_snapshot=current_snapshot,
        other_snapshot=session.product.seed.life.b_snapshot,
        performed_act_ref=actor.get("performed_act_ref", ""),
        other_act_ref=second_source["b_event_ref"],
        objective_ref=world["bp1_objective_ref"],
        objective_hash=world["bp1_objective_hash"],
        material_ref=second_source["b_event_ref"],
        material_receipt_id=second_source["b_event_hash"],
        witness_ref=world["witness_ref"],
        actor_source_ref=actor["source_ref"],
        actor_source_hash=actor["source_hash"],
        other_source_ref=payload["other_actor"]["source_ref"],
        other_source_hash=payload["other_actor"]["source_hash"],
        actor_performed_receipt_id=world.get("performed_act_receipt_id", ""),
        other_performed_receipt_id=second_source["b_event_hash"],
        life=session.product.seed.life,
    )
    return occurrence, current_snapshot


def read_out9_continuation(
    *,
    journal_path,
    expected_state_digest: str,
    expected_occurrence_id: str,
    proof_verifier,
) -> Out9Binding:
    """OUT9 read for a later occurrence in the same keyed journal.

    The accepted ``read_out9`` hard-requires exactly one occurrence ID. The S41
    continuation intentionally retains prior occurrences, so this bounded
    adapter reuses the same read-only consumer/ingress and verifies the expected
    occurrence without deleting or replacing the earlier bytes.
    """
    ingress = receive_event(
        journal_path,
        expected_state_digest=expected_state_digest,
        proof_verifier=proof_verifier,
    )
    consumer = C8ReadOnlyConsumer(journal_path)
    view = consumer.load()
    readset = view.readset.to_json()
    if readset["state_digest"] != expected_state_digest:
        raise S41EventRefusal("S41_OUT9_STATE_DIGEST_DIVERGES")
    if expected_occurrence_id not in list(readset["occurrence_ids"]):
        raise S41EventRefusal("S41_OUT9_OCCURRENCE_ABSENT")
    event = view.get(expected_occurrence_id)
    if event is None:
        raise S41EventRefusal("S41_OUT9_EVENT_ABSENT")
    consumer.assert_read_only_against(journal_path.read_bytes())
    return Out9Binding(
        occurrence_id=expected_occurrence_id,
        event=dict(event),
        readset=readset,
        ingress=ingress,
        grade=str(event.get("admission_grade")),
        verified_proof=proof_verifier is not None,
        canonical_bytes_sha256=readset["canonical_bytes_sha256"],
    )


class ContinuationProducer(GeneratedProducer):
    """Admit a new event into the existing journal/C9; never reapply seed state."""

    def __init__(self, root, *, case, source, occurrence, current_tools):
        super().__init__(root, case=case, source=source)
        self.occurrence = occurrence
        self.clock["value"] = occurrence.event_time
        self.material_access = "granted" if int(current_tools) > 0 else "denied"

    def commit_incoming(self):
        self.stage_c8()
        self.out9 = read_out9_continuation(
            journal_path=self.env.journal_path,
            expected_state_digest=self.commit.state_digest,
            expected_occurrence_id=self.commit.occurrence_id,
            proof_verifier=self.env.journal.verify_journal,
        )
        verify_out9_against_source(self.out9, self.commit, self.occurrence)
        self._bind_e1()
        return self

    def generate(self, *, source_records, rule=FULL_RULE, branch_id,
                 world: Mapping[str, Any], access_witness=None):
        if self.e1_event is None:
            raise S41EventRefusal("S41_EVENT_NOT_ADMITTED")
        access = access_witness or self._default_access()
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
            material_eligible=bool(world.get("tool_available")),
            eligible_material_refs=(self.conditioning_source["source_ref"],),
        )
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
            world=dict(world),
            rule=rule,
        )
        self.generation_receipt = receipt
        return receipt


def history_record_from_prior(
    session, *, first_binding: Mapping[str, Any], as_of: int
) -> dict:
    first_source = first_binding["source"]
    operation = first_source["b_operation"]
    predicates = {"SHARE_TOOL": "PRIOR_B_SHARE", "REFUSE_TOOL": "PRIOR_B_REFUSAL"}
    if operation not in predicates:
        raise S41EventRefusal("S41_PRIOR_B_OPERATION_UNSUPPORTED", str(operation))
    generation = first_binding["generation"]
    return make_source(
        source_ref="TEST_ONLY_S41_HIST_" + first_binding["e1_event_id"],
        source_class="HISTORICAL_EPISODE",
        actor_id=first_binding["actor_id"],
        branch_id=first_binding["branch_id"],
        as_of=as_of,
        predicate=predicates[operation],
        value=1,
        content={
            "mapping_premise": "WITNESSED_PRIOR_B_OPERATION_TO_EXISTING_HISTORICAL_PREDICATE",
            "mapped_from_e1_event_id": first_binding["e1_event_id"],
            "mapped_from_e1_event_hash": first_binding["e1_event_hash"],
            "prior_e1_event_id": first_binding["e1_event_id"],
            "prior_e1_event_hash": first_binding["e1_event_hash"],
            "prior_c8_occurrence_id": first_binding["c8"]["occurrence_id"],
            "prior_c8_content_hash": first_binding["c8"].get("c8_content_hash", ""),
            "prior_b_operation": operation,
            "prior_b_event_hash": first_source["b_event_hash"],
            "prior_actor_id": first_binding["actor_id"],
            "prior_branch_id": first_binding["branch_id"],
            "prior_event_time": first_binding["event_time"],
            "prior_access_witness_hash": generation.get("access_witness_hash", ""),
            "prior_access_source_ref": generation.get("access_source_ref", ""),
            "prior_access_source_hash": generation.get("access_source_hash", ""),
            "prior_source_actor_map": first_binding["source_actor_map"],
        },
    )


__all__ = [
    "ContinuationProducer",
    "S41EventRefusal",
    "build_current_snapshot",
    "build_second_occurrence",
    "history_record_from_prior",
    "world_prerequisites",
]
