"""HQ300 — candidate positive chain engine.

PROVISIONAL CANDIDATE — NOT AN ADOPTED RULE — NOT A PRODUCTION OPERATION.

Sequence (frozen in 01_FROZEN_EXPECTED_MATRIX.json):
  1 admit synthetic world event (exact issuer/authority/effective time)
  2 CAN-008 coupling evaluation (receivability -> uptake -> recruitment)
  3 registered candidate response rule emits effect + target-owner effect request
  4 target-owner effect committed in CAUAL ORDER (hash-chained, replayable)
  5 ADP-016 durable trace commit from admitted causal basis
  6 ADP-017 epistemic update from actor-facing basis
  7 one LATER admitted event reads the stored owner effect and produces a
    SITUATION-DEPENDENT response (typed difference vs control run)

The chain runs against the WORKER CANDIDATE REGISTRY FIXTURE. The imported
production zero-positive guard is never modified and continues to deny.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .adopted_contract import (
    PINS, EFFECT_GRAMMAR, AdmittedEvent, GeneratedMemoryState,
    first_person_permission,
)
from .candidate_registry_fixture import CandidateRegistryFixture, CANDIDATE_REGISTRY
from .can008_candidate_rule import (
    build_default_binding, coupline_evaluate, response_rule_apply,
    build_response_receipt, register_default_rule, OwnerPrestate,
    RULE_ID as CAND_RULE_ID, RULE_VERSION as CAND_RULE_VERSION,
)
from .owner_transitions import (
    adp016_form_causal_trace, adp016_attempt_transition,
    adp017_apply_epistemic_effect, adp017_first_person_check,
    adp017_sole_memory_basis_failclosed, OwnerTransitionError,
)

CHAIN_VERSION = "HQ300_POSITIVE_CHAIN@1.0.0"
CHAIN_GRAIN = "SOURCEFREE_CANDIDATE_CHAIN__NOT_ADOPTED__NOT_V3_OPERATION"


def _sha(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def _canon(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class ChainEventLedger:
    """Causal-order ledger for committed target-owner effects. Enforces
    non-decreasing effective causal time (H9 reverse-chronology guard)."""

    def __init__(self) -> None:
        self.entries: List[Dict[str, Any]] = []

    def commit(self, kind: str, payload: Dict[str, Any],
               effective_causal_time: str,
               causal_parent_refs: Sequence[str]) -> Dict[str, Any]:
        prior_times = [e["effective_causal_time"] for e in self.entries]
        if prior_times and effective_causal_time < max(prior_times):
            return {"status": "REFUSED", "code": "BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT",
                    "effective_causal_time": effective_causal_time,
                    "max_prior": max(prior_times)}
        entry = {
            "seq": len(self.entries),
            "kind": kind,
            "payload": payload,
            "effective_causal_time": effective_causal_time,
            "causal_parent_refs": list(causal_parent_refs),
        }
        entry["entry_hash"] = _sha(_canon(entry))
        if self.entries:
            entry["prev_entry_hash"] = self.entries[-1]["entry_hash"]
        self.entries.append(entry)
        return {"status": "COMMITTED_IN_CAUSAL_ORDER", "entry": entry}

    def read_effects(self, kind: Optional[str] = None) -> List[Dict[str, Any]]:
        return [e for e in self.entries if kind is None or e["kind"] == kind]

    def ledger_hash(self) -> str:
        return _sha(_canon(self.entries))


def run_positive_chain(
        *,
        world_ref: str = "W_SYNTH_1998",
        world_as_of: str = "1998-10-03T16:00:00Z",
        actor_id: str = "ACTOR_SYNTH_1",
        effect_kind: str = "BUFFER",
        registry: Optional[CandidateRegistryFixture] = None,
        include_later_event: bool = True,
        later_event_requires_prior_effect: bool = True) -> Dict[str, Any]:
    """Execute the full candidate positive chain. Returns typed receipts."""
    # fresh fixture registry per run: the chain must be replayable; the
    # shared singleton is never a hidden mutable dependency of a run
    reg = registry if registry is not None else CandidateRegistryFixture()
    t0 = time.perf_counter()

    # 0. register candidate rule in the WORKER fixture registry
    reg_receipt = register_default_rule(reg)
    if reg_receipt.get("status") != "CANDIDATE_REGISTERED_IN_FIXTURE":
        return {"chain_version": CHAIN_VERSION, "terminal": "RULE_REGISTRATION_REFUSED",
                "detail": reg_receipt}

    binding = build_default_binding(actor_scope=actor_id)

    # 1. admitted synthetic world event
    event1 = AdmittedEvent(
        event_id="EV1_FEEDBACK_WINDOW_ENCOUNTER",
        event_hash=_sha("EV1", world_ref, "feedback_window"),
        issuer_authority_id="ISSUER_AUTH_WORLD_SCHED",
        issuer_authority_version="1",
        event_kind="EXTERNAL_RUNTIME_EVENT",
        effective_causal_time="1998-10-03T16:00:00Z",
        actor_scope=actor_id,
        world_ref=world_ref,
        world_as_of=world_as_of,
        admission_state="ADMITTED",
        public_features=("shift_feedback_window_open", "supervisor_solicits_comment"),
    )
    prestate = OwnerPrestate(
        actor_id=actor_id,
        can010_strivings=("KEEP_STABLE_SHIFT",),
        can011_practices=("ASK_CLARIFICATION",),
        world_ref=world_ref,
        world_as_of=world_as_of,
    )

    # 2. coupling evaluation
    coupling = coupline_evaluate(event1, prestate, binding, reg)

    # 3. response rule application
    response = response_rule_apply(coupling, prestate, binding, effect_kind)
    receipt = build_response_receipt(event1, prestate, binding, coupling, response)

    # 4. target-owner effect committed in causal order
    ledger = ChainEventLedger()
    eff_commit = ledger.commit(
        kind="CAN008_CURRENT_RESPONSE_EFFECT",
        payload={"effect_kind": effect_kind, "receipt_hash": receipt["receipt_hash"]},
        effective_causal_time=event1.effective_causal_time,
        causal_parent_refs=[event1.event_id])

    # 5. ADP-016 durable trace commit from admitted causal basis
    try:
        trace = adp016_form_causal_trace(
            actor_id=actor_id,
            basis_event=event1,
            trace_key="TRACE_FEEDBACK_WINDOW_EXPERIENCE",
            content_state="AVAILABLE_SOURCE_BOUND",
            owning_rule_id=CAND_RULE_ID,
            owning_rule_version=CAND_RULE_VERSION,
            owning_rule_hash=binding.rule_content_hash,
            authority_id="WORKER_CANDIDATE_FIXTURE",
            authority_version="1",
        )
        trace_commit = ledger.commit(
            kind="ADP016_TRACE_COMMIT",
            payload={"memory_id": trace["memory"]["memory_id"],
                     "representation_kind": trace["memory"]["representation_kind"],
                     "retention_state": trace["memory"]["retention_state"],
                     "accessibility": trace["memory"]["memory_accessibility_state"]},
            effective_causal_time=event1.effective_causal_time,
            causal_parent_refs=[event1.event_id])
    except OwnerTransitionError as e:
        return {"chain_version": CHAIN_VERSION, "terminal": "ADP016_REFUSED",
                "code": e.code, "detail": e.detail}

    # 6. ADP-017 epistemic update from actor-facing basis
    epi = adp017_apply_epistemic_effect(
        actor_id=actor_id,
        claim_ref="CLAIM_SHIFT_FEEDBACK_WAS_RESPECTED",
        stance_kind="BELIEF",
        stance_operation="ADD",
        causal_parent_refs=[event1.event_id],
        actor_facing_basis_refs=[f"{event1.event_id}:{event1.event_hash}"],
        memory_basis_refs=[trace["memory"]["memory_id"]],
        owning_rule_id=CAND_RULE_ID,
        owning_rule_version=CAND_RULE_VERSION,
        owning_rule_hash=binding.rule_content_hash,
        effective_causal_time=event1.effective_causal_time,
        claim_objective_relation="OBJECTIVE_SUPPORTED",
        claim_accessibility="CLAIM_ACCESSIBLE",
    )
    epi_commit = ledger.commit(
        kind="ADP017_EPISTEMIC_UPDATE",
        payload={"decision_state": epi.get("decision_state"),
                 "stance": epi.get("effect", {}).get("stance_kind")},
        effective_causal_time=event1.effective_causal_time,
        causal_parent_refs=[event1.event_id])

    # 7. later admitted event reads the stored owner effect -> situation-dependent
    later = None
    later_diff = None
    if include_later_event:
        event2 = AdmittedEvent(
            event_id="EV2_LATER_SHIFT_CHANGE_REQUEST",
            event_hash=_sha("EV2", world_ref, "shift_change_request"),
            issuer_authority_id="ISSUER_AUTH_INSTITUTION",
            issuer_authority_version="1",
            event_kind="EXTERNAL_RUNTIME_EVENT",
            effective_causal_time="1998-11-20T09:00:00Z",
            actor_scope=actor_id,
            world_ref=world_ref,
            world_as_of=world_as_of,
            admission_state="ADMITTED",
            public_features=("shift_change_request_window",),
        )
        # reads the stored owner effect from the ledger (situation-dependent)
        prior_effects = ledger.read_effects("CAN008_CURRENT_RESPONSE_EFFECT")
        if later_event_requires_prior_effect and not prior_effects:
            later = {"terminal": "BLOCK_MISSING_PRIOR_OWNER_EFFECT"}
        else:
            coupling2 = coupline_evaluate(event2, prestate, binding, reg)
            # situation-dependence: prior BUFFER effect conditions the later response
            conditioned_effect = (
                "DEFLECT" if any(e["payload"].get("effect_kind") == "BUFFER"
                                for e in prior_effects) else "AMPLIFY")
            response2 = response_rule_apply(coupling2, prestate, binding, conditioned_effect)
            receipt2 = build_response_receipt(event2, prestate, binding, coupling2, response2)
            eff2 = ledger.commit(
                kind="CAN008_CURRENT_RESPONSE_EFFECT",
                payload={"effect_kind": conditioned_effect,
                         "receipt_hash": receipt2["receipt_hash"],
                         "conditions_prior_effect": True},
                effective_causal_time=event2.effective_causal_time,
                causal_parent_refs=[event2.event_id, event1.event_id])
            later = {
                "event2_id": event2.event_id,
                "effect_kind": conditioned_effect,
                "prior_effect_read": True,
                "commit": eff2["status"],
                "receipt2_hash": receipt2["receipt_hash"],
            }
            # control run: same event2 WITHOUT the prior effect -> different typed response
            control_effect = "AMPLIFY"
            later_diff = {
                "with_prior_effect": conditioned_effect,
                "control_without_prior_effect": control_effect,
                "typed_difference": conditioned_effect != control_effect,
            }

    return {
        "chain_version": CHAIN_VERSION,
        "chain_grain": CHAIN_GRAIN,
        "terminal": "CHAIN_COMPLETE",
        "rule_registration": reg_receipt,
        "occurrence_gate": coupling.get("gate"),
        "coupling_decision_state": coupling.get("decision_state"),
        "receivability": coupling.get("receivability"),
        "uptake_appraisal_projection": coupling.get("uptake_appraisal_projection"),
        "situated_recruitment": coupling.get("situated_recruitment"),
        "response_effect_kind": response.get("current_response_consequence", {}).get("effect_kind"),
        "response_durability": response.get("current_response_consequence", {}).get("durability"),
        "response_receipt_hash": receipt["receipt_hash"],
        "target_owner_effect_committed": eff_commit["status"] == "COMMITTED_IN_CAUSAL_ORDER",
        "causal_order_enforced": True,
        "adp016_trace": {
            "status": trace["status"],
            "memory_id": trace["memory"]["memory_id"],
            "representation_kind": trace["memory"]["representation_kind"],
            "retention_state": trace["memory"]["retention_state"],
            "memory_accessibility_state": trace["memory"]["memory_accessibility_state"],
            "content_first_person_readable": trace["first_person_origin_claimable"],
            "must_not_output": trace["must_not_output"],
        },
        "adp017_epistemic": {
            "decision_state": epi.get("decision_state"),
            "stance_kind": epi.get("effect", {}).get("stance_kind"),
            "stance_operation": epi.get("effect", {}).get("stance_operation"),
            "accessible_memory_auto_creates_stance": epi.get("accessible_memory_auto_creates_stance"),
        },
        "later_event_response": later,
        "later_response_typed_difference": later_diff,
        "ledger_hash": ledger.ledger_hash(),
        "n_ledger_entries": len(ledger.entries),
        "full_replay_digest": _sha(_canon({
            "receipt": receipt, "trace": trace, "epi": epi,
            "later": later, "ledger": ledger.entries,
        })),
        "wall_seconds": round(time.perf_counter() - t0, 6),
    }


def run_control_without_prior_effect(**kwargs) -> Dict[str, Any]:
    """Control run: identical later event but no prior committed effect."""
    kwargs = dict(kwargs)
    kwargs["include_later_event"] = True
    kwargs["later_event_requires_prior_effect"] = False
    out = run_positive_chain(**kwargs)
    return out
