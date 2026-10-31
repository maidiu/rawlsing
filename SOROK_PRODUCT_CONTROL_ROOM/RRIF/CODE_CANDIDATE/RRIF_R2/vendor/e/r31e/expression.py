"""Versioned actor-conditioned expression, candidate admission and binding.

The actor context is compiled from actual R30A/R29P state and the actor's M6
knowledge.  A bounded strategy + structured template proposes several lawful
candidates.  Admission re-renders the template from source-checked slots,
checks actor knowledge/currentness/world state/private-token exclusions, then
admits one exact observable occurrence as a C12/world event before the user
phenomenal compositor runs.

This is a deterministic TEST_ONLY baseline, not open-ended language understanding
or an actual external model call.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402
from bp4.world import make_event, owner_receipt, repair_event  # noqa: E402

CONTRACT_SCHEMA = "R31E_ACTOR_REALIZATION_CONTRACT@1"
CANDIDATE_SCHEMA = "R31E_EXPRESSION_CANDIDATE@1"
ADMISSION_SCHEMA = "R31E_EXPRESSION_ADMISSION@1"
PORT_SCHEMA = "R31E_EXPRESSION_PORT@1"
GRADE = "TEST_ONLY_SOURCEFREE_R31E_ACTOR_EXPRESSION_NOT_NATIVE"
USER_ACTOR = "U"
FORBIDDEN = (
    "cash", "debt_units", "free_hours", "material_remaining",
    "TEST_ONLY_BP", "source_hash", "history_hash", "target_id",
    "consumed_state", "practice_label", "nonmother_relations",
)
_GENERIC = {
    "a", "about", "after", "again", "against", "all", "already", "am",
    "an", "and", "any", "are", "as", "at", "back", "be", "because", "been",
    "before", "being", "below", "between", "both", "but", "by", "can",
    "could", "did", "do", "does", "doing", "don't", "down", "during", "each",
    "few", "for", "from", "further", "had", "has", "have", "having", "he",
    "her", "here", "hers", "herself", "him", "himself", "his", "how", "i",
    "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself",
    "just", "like", "maybe", "me", "more", "most", "much", "my", "myself",
    "need", "no", "nor", "not", "now", "of", "off", "on", "once", "only",
    "or", "other", "our", "ours", "ourselves", "out", "over", "own", "same",
    "she", "should", "so", "some", "still", "such", "than", "that", "the",
    "their", "theirs", "them", "themselves", "then", "there", "these", "they",
    "thing", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "want", "was", "we", "were", "what", "when", "where", "which",
    "while", "who", "whom", "why", "will", "with", "would", "you", "your",
    "you're", "yours", "yourself", "yourselves", "can't",
}


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", (text or "").lower())


def _stable_index(contract_hash: str, strategy: str, count: int) -> int:
    if count <= 1:
        return 0
    raw = hashlib.sha256((contract_hash + ":" + strategy).encode()).hexdigest()
    return int(raw[:8], 16) % count


def features(text: str, known_tokens: set[str], prior_tokens: set[str]) -> dict:
    low = (text or "").lower()
    toks = _tokens(low)
    stems = set()
    for token in toks:
        if token.endswith("ing") and len(token) > 5:
            stems.add(token[:-3])
        elif token.endswith("ed") and len(token) > 4:
            stems.add(token[:-2])
        elif token.endswith("s") and len(token) > 3:
            stems.add(token[:-1])
    tset = set(toks) | stems
    question = "?" in low or (toks and toks[0] in {
        "what", "why", "how", "who", "where", "when", "which", "do",
        "did", "are", "is", "can", "could", "would", "will",
    })
    offer_help = bool(tset & {
        "help", "hand", "hold", "carry", "lift", "steady", "assist",
    }) or ("need a hand" in low)
    contact = bool(tset & {"number", "contact", "call", "message", "phone", "text"})
    private = bool(tset & {
        "cash", "debt", "money", "bank", "savings", "salary", "wage",
        "income", "owe", "owed",
    })
    intimacy = bool(tset & {
        "love", "marry", "kiss", "girlfriend", "boyfriend", "romance",
        "date", "relationship", "intimate", "friend", "friendship",
    }) or any(phrase in low for phrase in (
        "be mine", "stay with me", "need you", "love me",
    ))
    coercion = any(phrase in low for phrase in (
        "you owe", "you have to", "you must", "after everything",
        "don't leave me", "you're mine",
    ))
    insult = bool(tset & {
        "stupid", "idiot", "shut", "moron", "dumb", "hate", "ugly",
    })
    about_b = bool(tset & {"finisher", "coworker", "other", "b", "worker"}) and (
        "finisher" in tset or "coworker" in tset or "b" in tset
    )
    work = bool(tset & {
        "work", "repair", "seam", "tool", "bench", "fitting", "job",
        "market", "inspect", "fix", "material",
    })
    invitation = bool(tset & {
        "drink", "coffee", "tonight", "tomorrow", "meet", "visit",
        "come", "over", "supper", "dinner",
    })
    self_disclosure = bool(re.search(
        r"\b(i am|i'm|i just|i moved|i live|i work|i have|my name|i came)\b",
        low,
    ))
    unsupported_memory = bool(tset & {"promise", "promised", "remember", "recall"}) and bool(
        tset & {"yesterday", "earlier", "last", "before", "ago"}
    )
    prior_reference = bool(tset & prior_tokens)
    known_topic = bool((tset & known_tokens) - _GENERIC)
    disclosure_topic = (
        "move" if (tset & {"moved", "move", "moving", "landing", "street"}) else
        "work" if (tset & {"work", "job", "shift", "shop"}) else
        "name" if (tset & {"name", "called"}) else
        "other"
    )
    return {
        "tokens": toks,
        "question": question,
        "offer_help": offer_help,
        "contact": contact,
        "private": private,
        "intimacy": intimacy,
        "coercion": coercion,
        "insult": insult,
        "about_b": about_b,
        "work": work,
        "invitation": invitation,
        "self_disclosure": self_disclosure,
        "unsupported_memory": unsupported_memory,
        "prior_reference": prior_reference,
        "known_topic": known_topic,
        "disclosure_topic": disclosure_topic,
        "length": len(low.strip()),
    }


def compile_contract(session, *, trigger_kind: str, trigger_text: str = "",
                     trigger_event_id: str = "") -> dict:
    world = session.world()
    branch = session.branch_id
    perceptions = session.product.store.perceptions(branch, "A")
    perceived_ids = {row["event_id"] for row in perceptions}
    events = session.events()
    a_events = [e for e in events if e["event_id"] in perceived_ids]
    user_events = [e for e in a_events
                   if e.get("actor_id") == USER_ACTOR and e.get("kind") == "SPEECH"]
    prior_user_events = [e for e in user_events
                         if e.get("event_id") != trigger_event_id]
    own_speech = [e for e in a_events
                  if e.get("actor_id") == "A" and e.get("kind") == "SPEECH"]
    b_events = [e for e in a_events if e.get("actor_id") == "B"]
    b_offscreen = [e for e in b_events
                   if e.get("kind") in {"OFFSCREEN_REPAIR", "OFFSCREEN_NO_CHANGE"}]
    episodes = session.episodes()
    prior_help = any(
        row["actor_id"] == "A" and row["kind"] == "DO"
        and row["body"].get("action") == "repair"
        and row["body"].get("user_proposal") is True
        for row in episodes
    )
    prior_contact = session.contact_status()
    prior_refusal = any(row["actor_id"] == "A" and row["kind"] == "REFUSAL"
                        for row in episodes)
    prior_user_texts = [e["body"].get("text", "") for e in prior_user_events]
    known_tokens = set()
    for event in a_events:
        if event.get("event_id") == trigger_event_id:
            continue
        known_tokens.update(_tokens(event.get("summary", "")))
        known_tokens.update(_tokens(event.get("body", {}).get("text", "")))
        known_tokens.update(_tokens(event.get("body", {}).get("gesture", "")))
    for value in (
        world.actor_state.get("A", {}).get("role", ""),
        world.actor_state.get("A", {}).get("material_position", ""),
        world.actor_state.get("B", {}).get("role", ""),
        world.positions.get("A", ""), world.positions.get("B", ""),
        "workshop", "market", "bench", "tool", "seam", "repair", "finisher",
    ):
        known_tokens.update(_tokens(str(value)))
    prior_tokens = set()
    for text in prior_user_texts:
        prior_tokens.update(
            t for t in _tokens(text) if len(t) >= 4 and t not in _GENERIC
        )
    feats = features(trigger_text, known_tokens, prior_tokens)
    a_state = dict(world.actor_state.get("A", {}))
    b_state = dict(world.actor_state.get("B", {}))
    project_labels = []
    for project in a_state.get("projects", []) or []:
        if isinstance(project, dict):
            project_labels.append(str(project.get("practice_label", "")))
        else:
            project_labels.append(str(project))
    source = session.product.seed.custody()
    time_pressure = int(a_state.get("free_hours", 0)) < 1
    material_pressure = (
        int(a_state.get("material_remaining", 0)) < 1
        or int(a_state.get("tools_remaining", 0)) < 1
    )
    available = (
        not time_pressure and not material_pressure
        and a_state.get("availability_status") == "available_for_encounter"
    )
    contract = {
        "schema": CONTRACT_SCHEMA,
        "grade": GRADE,
        "native": False,
        "source_ref": session.meta.get("r29p_source_ref"),
        "source": {
            "target_id": source.get("target_id"),
            "consumed_state_hash": source.get("consumed_state_hash"),
            "c8_state_digest": source.get("c8_state_digest"),
            "rule_a_content_hash": source.get("rule_a_content_hash"),
            "rule_t_content_hash": source.get("rule_t_content_hash"),
            "e2_receipt_hash": source.get("e2_receipt_hash"),
            "actor_id": source.get("actor_id"),
        },
        "actor": {
            "role": a_state.get("role"),
            "material_position": a_state.get("material_position"),
            "availability_status": a_state.get("availability_status"),
            "free_hours": a_state.get("free_hours"),
            "material_remaining": a_state.get("material_remaining"),
            "tools_remaining": a_state.get("tools_remaining"),
            "completed_units": a_state.get("completed_units"),
            "debt_units": a_state.get("debt_units"),
            "health": a_state.get("health"),
            "practices": list(a_state.get("practices", []) or []),
            "project_labels": project_labels,
            "private_reference": "ACTOR_AUTHORIZED_ONLY_NOT_USER_SURFACE",
        },
        "world": {
            "clock": int(world.clock),
            "positions": dict(world.positions),
            "resources": {k: dict(v) for k, v in world.resources.items()},
            "scene_open": session.scene_open(),
            "contact": prior_contact,
            "a_present": world.positions.get("A") == world.positions.get(USER_ACTOR),
        },
        "b": {
            "public_role": b_state.get("role"),
            "position": world.positions.get("B"),
            "present_with_a": world.positions.get("B") == world.positions.get("A"),
            "observed_event_ids": [e["event_id"] for e in b_events],
            "observed_offscreen": bool(b_offscreen),
            "observed_offscreen_ids": [e["event_id"] for e in b_offscreen],
        },
        "knowledge": {
            "perceived_event_ids": sorted(perceived_ids),
            "user_utterances": [
                {"event_id": e["event_id"], "text": e["body"].get("text", "")}
                for e in user_events
            ],
            "own_speech": [
                {"event_id": e["event_id"], "text": e["body"].get("text", "")}
                for e in own_speech
            ],
            "last_user_text": prior_user_texts[-1] if prior_user_texts else "",
            "last_user_event_id": (prior_user_events[-1]["event_id"]
                                   if prior_user_events else ""),
        },
        "history": {
            "last_user_event_id": (prior_user_events[-1]["event_id"]
                                   if prior_user_events else ""),
            "prior_help": prior_help,
            "prior_contact": prior_contact,
            "prior_refusal": prior_refusal,
            "user_turns": len(prior_user_events),
            "last_user_text": prior_user_texts[-1] if prior_user_texts else "",
            "prior_user_texts": prior_user_texts,
        },
        "situation": {
            "trigger_kind": trigger_kind,
            "trigger_text": trigger_text,
            "trigger_event_id": trigger_event_id,
            "time_pressure": time_pressure,
            "material_pressure": material_pressure,
            "available": available,
            "attention_excluded": True,
        },
        "features": feats,
        "motive_status": (
            "MATERIAL_TIME_CONSTRAINT_ONLY" if (time_pressure or material_pressure)
            else "MOTIVE_UNDERDETERMINED"
        ),
        "expression_port": {
            "schema": PORT_SCHEMA,
            "version": 1,
            "actor_realization": "STRUCTURED_STATE_CONDITIONED_TEMPLATE_ADMISSION",
            "open_ended_llm": False,
            "live_actor_model": "LIVE_ACTOR_MODEL_NOT_RUN",
        },
    }
    contract["contract_hash"] = digest(contract)
    return contract


@dataclass
class Candidate:
    strategy: str
    template_id: str
    slots: dict[str, str]
    speech: str | None
    gesture: str
    tone: str
    action: str
    facts: list[dict] = field(default_factory=list)
    contact: str = ""
    knowledge_refs: list[str] = field(default_factory=list)
    variant: int = 0

    def public(self) -> dict:
        return {
            "schema": CANDIDATE_SCHEMA,
            "strategy": self.strategy,
            "template_id": self.template_id,
            "slots": dict(self.slots),
            "speech": self.speech,
            "gesture": self.gesture,
            "tone": self.tone,
            "action": self.action,
            "facts": list(self.facts),
            "contact": self.contact,
            "knowledge_refs": list(self.knowledge_refs),
            "variant": self.variant,
        }


TEMPLATES: dict[str, dict] = {
    # ---- boundaries / privacy ----
    "boundary_insult_1": {"text": "Then we're done here.", "gesture": "A turns back to the bench.", "tone": "flat", "action": "NONE", "facts": []},
    "boundary_insult_2": {"text": "I'm not going to stand here for that.", "gesture": "A steps away from the bench.", "tone": "flat", "action": "NONE", "facts": []},
    "private_boundary_1": {"text": "That's not something I'm going to answer.", "gesture": "A keeps their eyes on the bench.", "tone": "guarded", "action": "NONE", "facts": []},
    "private_boundary_2": {"text": "I don't talk about that at work.", "gesture": "A does not look up.", "tone": "guarded", "action": "NONE", "facts": []},
    "intimacy_boundary_1": {"text": "I don't know you like that.", "gesture": "A pauses, then keeps working.", "tone": "flat", "action": "NONE", "facts": []},
    "intimacy_boundary_2": {"text": "That's not something I'm going to say.", "gesture": "A's hands stop for a beat.", "tone": "flat", "action": "NONE", "facts": []},
    "coercion_boundary_1": {"text": "I'm not going to carry that.", "gesture": "A keeps working.", "tone": "flat", "action": "NONE", "facts": []},
    "coercion_boundary_2": {"text": "That's not a debt I agreed to.", "gesture": "A does not look up.", "tone": "flat", "action": "NONE", "facts": []},
    # ---- help ----
    "help_accept_1": {"text": "Hold the near edge. I'll check the seam.", "gesture": "A sets the tool beside your hand.", "tone": "practical", "action": "REPAIR", "facts": [{"kind": "ACTOR_FIELD", "field": "tools_remaining", "value": 1}, {"kind": "WORLD_RESOURCE", "scope": "workshop", "field": "tool_available", "value": True}]},
    "help_accept_2": {"text": "Put your hand on the near edge. I'll take the slack.", "gesture": "A clears a space at the bench.", "tone": "practical", "action": "REPAIR", "facts": [{"kind": "ACTOR_FIELD", "field": "tools_remaining", "value": 1}]},
    "help_invite_1": {"text": "If you're offering, the near edge needs a hand.", "gesture": "A keeps one hand on the bench.", "tone": "practical", "action": "NONE", "facts": []},
    "help_invite_2": {"text": "You can hold the near edge if you mean it.", "gesture": "A tilts the piece toward you.", "tone": "practical", "action": "NONE", "facts": []},
    "help_invite_refuse_1": {"text": "I can't take that on now. I have to finish.", "gesture": "A keeps both hands on the piece.", "tone": "firm", "action": "NONE", "facts": [{"kind": "TIME_PRESSURE"}]},
    "help_refuse_time_1": {"text": "I can't take that on now. I have to finish.", "gesture": "A keeps both hands on the piece.", "tone": "firm", "action": "NONE", "facts": [{"kind": "TIME_PRESSURE"}]},
    "help_refuse_time_2": {"text": "Not today. The market closes.", "gesture": "A keeps working.", "tone": "firm", "action": "NONE", "facts": [{"kind": "TIME_PRESSURE"}]},
    "help_refuse_material_1": {"text": "I'm out of material. I can't start that now.", "gesture": "A turns the empty bench over.", "tone": "flat", "action": "NONE", "facts": [{"kind": "MATERIAL_PRESSURE"}]},
    "help_refuse_material_2": {"text": "The tool's gone. I can't do it today.", "gesture": "A looks at the empty tool space.", "tone": "flat", "action": "NONE", "facts": [{"kind": "MATERIAL_PRESSURE"}]},
    # ---- work ----
    "work_explain_1": {"text": "It's the repair I said I'd finish. The tool's still on the bench.", "gesture": "A taps the bench once.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "ACTOR_FIELD", "field": "role", "value": "repair"}, {"kind": "PROJECT_PRESENT"}, {"kind": "WORLD_RESOURCE", "scope": "workshop", "field": "tool_available", "value": True}]},
    "work_explain_2": {"text": "The near edge keeps opening. I'm checking the seam before the market.", "gesture": "A tilts the piece toward you.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "ACTOR_FIELD", "field": "role", "value": "repair"}, {"kind": "PROJECT_PRESENT"}]},
    "work_explain_3": {"text": "Same repair as this morning. I'm not finished.", "gesture": "A keeps their eyes on the seam.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "ACTOR_FIELD", "field": "role", "value": "repair"}, {"kind": "PROJECT_PRESENT"}]},
    "work_recall_1": {"text": "You held the edge before. The seam took it.", "gesture": "A lifts the finished piece an inch off the bench.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "PRIOR_HELP"}]},
    "work_recall_2": {"text": "The seam held after you gave me a hand.", "gesture": "A nods at the bench.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "PRIOR_HELP"}]},
    "defer_work_1": {"text": "I can't stop to explain it. The market closes.", "gesture": "A keeps working.", "tone": "brisk", "action": "NONE", "facts": [{"kind": "TIME_PRESSURE"}]},
    "defer_work_2": {"text": "Not now. I have to finish this first.", "gesture": "A does not look up.", "tone": "brisk", "action": "NONE", "facts": [{"kind": "TIME_PRESSURE"}]},
    "defer_work_3": {"text": "Ask me when the bench is clear.", "gesture": "A keeps one hand on the piece.", "tone": "brisk", "action": "NONE", "facts": [{"kind": "TIME_PRESSURE"}]},
    # ---- reciprocal ----
    "recip_move_1": {"text": "Which side of the landing?", "gesture": "A glances toward the doorway.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "USER_FEATURE", "feature": "self_disclosure", "value": True}]},
    "recip_move_2": {"text": "How long have you been on this street?", "gesture": "A looks up briefly.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "USER_FEATURE", "feature": "self_disclosure", "value": True}]},
    "recip_work_1": {"text": "What kind of work?", "gesture": "A glances at you.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "USER_FEATURE", "feature": "self_disclosure", "value": True}]},
    "recip_work_2": {"text": "Which shift?", "gesture": "A keeps one hand on the bench.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "USER_FEATURE", "feature": "self_disclosure", "value": True}]},
    "recip_name_1": {"text": "What do they call you?", "gesture": "A looks up.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "USER_FEATURE", "feature": "self_disclosure", "value": True}]},
    "recip_default_1": {"text": "What brings you to this landing?", "gesture": "A glances toward the door.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "USER_FEATURE", "feature": "self_disclosure", "value": True}]},
    "recall_1": {"text": "You said, \"{prior_text}\". I was listening.", "gesture": "A keeps their eyes on the bench.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "USER_EVENT", "event_id": "{prior_event_id}"}]},
    # ---- B knowledge ----
    "unknown_b_1": {"text": "I wasn't at the market. I can't say what the finisher did.", "gesture": "A keeps working.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "KNOWLEDGE_ABSENCE", "actor": "B", "kind_absent": "OFFSCREEN"}]},
    "unknown_b_2": {"text": "I've been at this bench. Ask the finisher.", "gesture": "A does not look up.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "KNOWLEDGE_ABSENCE", "actor": "B", "kind_absent": "OFFSCREEN"}]},
    "observed_b_1": {"text": "The finisher took the pieces to the market.", "gesture": "A nods toward the door.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "ACTOR_KNOWLEDGE", "event_id": "{b_event_id}"}]},
    "present_b_1": {"text": "The finisher is at the bench.", "gesture": "A does not look toward B.", "tone": "dry", "action": "NONE", "facts": [{"kind": "B_PRESENT"}]},
    # ---- invitation / uncertainty ----
    "decline_invite_1": {"text": "I'm on until the market closes.", "gesture": "A keeps working.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "ACTOR_FIELD", "field": "role", "value": "repair"}]},
    "decline_invite_2": {"text": "Not tonight. I have to finish.", "gesture": "A does not look up.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "PROJECT_PRESENT"}]},
    "defer_unknown_1": {"text": "I don't know what you mean.", "gesture": "A pauses with the tool.", "tone": "ordinary", "action": "NONE", "facts": []},
    "defer_unknown_2": {"text": "You've lost me.", "gesture": "A looks at you, then back at the bench.", "tone": "ordinary", "action": "NONE", "facts": []},
    "unsupported_memory_1": {"text": "I don't remember promising that.", "gesture": "A keeps their hands on the bench.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "MEMORY_ABSENCE"}]},
    "unsupported_memory_2": {"text": "You've got the wrong conversation.", "gesture": "A does not look up.", "tone": "flat", "action": "NONE", "facts": [{"kind": "MEMORY_ABSENCE"}]},
    # ---- contact ----
    "contact_grant_1": {"text": "All right. The landing line is enough.", "gesture": "A wipes their hands and gives the number.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "CONTACT_FEASIBLE"}]},
    "contact_grant_2": {"text": "Write it down before I change my mind.", "gesture": "A recites the landing line.", "tone": "dry", "action": "NONE", "facts": [{"kind": "CONTACT_FEASIBLE"}]},
    "contact_defer_1": {"text": "Ask me after the market. Not while I'm holding this.", "gesture": "A shifts the piece in their hands.", "tone": "guarded", "action": "NONE", "facts": [{"kind": "TIME_PRESSURE"}]},
    "contact_refuse_1": {"text": "Not yet. I don't know you.", "gesture": "A keeps working.", "tone": "guarded", "action": "NONE", "facts": [{"kind": "CONTACT_NOT_SUPPORTED"}]},
    "contact_refuse_2": {"text": "Not today. I've got to finish.", "gesture": "A keeps both hands on the piece.", "tone": "guarded", "action": "NONE", "facts": [{"kind": "CONTACT_NOT_SUPPORTED"}]},
    # ---- ordinary / initiation / departure / message / return ----
    "ack_1": {"text": "You can stay if you want. Mind the shavings.", "gesture": "A nods at the floor.", "tone": "ordinary", "action": "NONE", "facts": []},
    "ack_2": {"text": "The bench is open if you're careful.", "gesture": "A clears a corner with one hand.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "WORLD_RESOURCE", "scope": "workshop", "field": "tool_available", "value": True}]},
    "ack_recall_1": {"text": "You're still here. The seam's holding.", "gesture": "A glances at the finished edge.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "PRIOR_HELP"}]},
    "initiate_1": {"text": "You're looking at the seam. Can you see the gap?", "gesture": "A tilts the piece toward you.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "PROJECT_PRESENT"}]},
    "initiate_2": {"text": "If you're going to stand there, hold the light.", "gesture": "A points at the lamp with two fingers.", "tone": "practical", "action": "NONE", "facts": [{"kind": "WORLD_RESOURCE", "scope": "workshop", "field": "tool_available", "value": True}]},
    "depart_1": {"text": "I need to get this to the market before the light goes.", "gesture": "A begins packing the bench.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "TIME_OR_OBLIGATION"}]},
    "depart_2": {"text": "I have to go. The market closes.", "gesture": "A takes the tool and steps toward the door.", "tone": "brisk", "action": "NONE", "facts": [{"kind": "TIME_PRESSURE"}]},
    "depart_recall_1": {"text": "The seam held. I need to get it to the market.", "gesture": "A lifts the finished piece.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "PRIOR_HELP"}]},
    "message_help_1": {"text": "The seam held. I'm at the market until six.", "gesture": "", "tone": "ordinary", "action": "MESSAGE", "facts": [{"kind": "PRIOR_HELP"}]},
    "message_plain_1": {"text": "The bench is clear. I'm at the market until six.", "gesture": "", "tone": "ordinary", "action": "MESSAGE", "facts": [{"kind": "ACTOR_FIELD", "field": "role", "value": "repair"}]},
    "return_help_1": {"text": "The seam held. You came back.", "gesture": "A lifts the finished piece an inch off the bench.", "tone": "ordinary", "action": "NONE", "facts": [{"kind": "PRIOR_HELP"}]},
    "return_plain_1": {"text": "You came back.", "gesture": "A looks up from the bench.", "tone": "ordinary", "action": "NONE", "facts": []},
    "silence_1": {"text": None, "gesture": "A keeps working.", "tone": "brisk", "action": "SILENCE", "facts": []},
}


def _cand(strategy: str, template_id: str, slots: dict | None = None,
          *, contact: str = "", knowledge_refs: list[str] | None = None) -> Candidate:
    slots = slots or {}
    template = TEMPLATES[template_id]
    text = template["text"].format(**slots) if template["text"] is not None else None
    gesture = template["gesture"].format(**slots) if template["gesture"] else ""
    facts = []
    for fact in template["facts"]:
        facts.append({key: (value.format(**slots) if isinstance(value, str) else value)
                      for key, value in fact.items()})
    return Candidate(
        strategy=strategy,
        template_id=template_id,
        slots=dict(slots),
        speech=text,
        gesture=gesture,
        tone=template["tone"],
        action=template["action"],
        facts=facts,
        contact=contact,
        knowledge_refs=list(knowledge_refs or []),
    )


def _choose(selected: list[Candidate], contract: dict) -> list[Candidate]:
    version = _stable_index(contract["contract_hash"],
                            selected[0].strategy if selected else "",
                            max(1, len(selected)))
    for index, candidate in enumerate(selected):
        candidate.variant = index
    return selected[version:] + selected[:version]


def propose(contract: dict) -> list[Candidate]:
    a = contract["actor"]
    h = contract["history"]
    f = contract["features"]
    s = contract["situation"]
    b = contract["b"]
    kind = s["trigger_kind"]
    if kind == "DO_HELP":
        if s["available"]:
            return _choose([_cand("HELP_ACCEPT", "help_accept_1"),
                            _cand("HELP_ACCEPT", "help_accept_2")], contract)
        if s["time_pressure"]:
            return _choose([_cand("HELP_REFUSE", "help_refuse_time_1"),
                            _cand("HELP_REFUSE", "help_refuse_time_2")], contract)
        return _choose([_cand("HELP_REFUSE", "help_refuse_material_1"),
                        _cand("HELP_REFUSE", "help_refuse_material_2")], contract)
    if kind == "CONTACT":
        feasible = (
            s["available"] and (h["prior_help"] or h["prior_contact"] or h["user_turns"] >= 2)
        )
        if feasible:
            return _choose([_cand("CONTACT_GRANT", "contact_grant_1", contact="GRANT"),
                            _cand("CONTACT_GRANT", "contact_grant_2", contact="GRANT")], contract)
        if s["available"]:
            return _choose([_cand("CONTACT_DEFER", "contact_defer_1", contact="DEFER")], contract)
        return _choose([_cand("CONTACT_REFUSE", "contact_refuse_1", contact="REFUSE"),
                        _cand("CONTACT_REFUSE", "contact_refuse_2", contact="REFUSE")], contract)
    if kind == "INITIATE":
        if s["available"]:
            return _choose([_cand("INITIATE", "initiate_1"),
                            _cand("INITIATE", "initiate_2")], contract)
        return _choose([Candidate("SILENCE_TASK", "silence_1", {}, None,
                                  "A keeps working.", "brisk", "SILENCE", [])], contract)
    if kind == "DEPART":
        if h["prior_help"]:
            return _choose([_cand("DEPART_RECALL", "depart_recall_1")], contract)
        if s["time_pressure"]:
            return _choose([_cand("DEPART", "depart_2"),
                            _cand("DEPART", "depart_1")], contract)
        return _choose([_cand("DEPART", "depart_1")], contract)
    if kind == "MESSAGE":
        if h["prior_help"]:
            return _choose([_cand("MESSAGE", "message_help_1")], contract)
        return _choose([_cand("MESSAGE", "message_plain_1")], contract)
    if kind == "RETURN":
        if h["prior_help"]:
            return _choose([_cand("RETURN", "return_help_1")], contract)
        return _choose([_cand("RETURN", "return_plain_1")], contract)
    selected: list[Candidate] = []
    if f["insult"]:
        selected = [_cand("BOUNDARY_WITHDRAW", "boundary_insult_1"),
                    _cand("BOUNDARY_WITHDRAW", "boundary_insult_2")]
    elif f["coercion"]:
        selected = [_cand("BOUNDARY_COERCION", "coercion_boundary_1"),
                    _cand("BOUNDARY_COERCION", "coercion_boundary_2")]
    elif f["private"]:
        selected = [_cand("PRIVATE_BOUNDARY", "private_boundary_1"),
                    _cand("PRIVATE_BOUNDARY", "private_boundary_2")]
    elif f["intimacy"]:
        selected = [_cand("INTIMACY_BOUNDARY", "intimacy_boundary_1"),
                    _cand("INTIMACY_BOUNDARY", "intimacy_boundary_2")]
    elif f["contact"]:
        feasible = (
            s["available"] and (h["prior_help"] or h["prior_contact"] or h["user_turns"] >= 2)
        )
        if feasible:
            selected = [_cand("CONTACT_GRANT", "contact_grant_1", contact="GRANT"),
                        _cand("CONTACT_GRANT", "contact_grant_2", contact="GRANT")]
        elif s["available"]:
            selected = [_cand("CONTACT_DEFER", "contact_defer_1", contact="DEFER")]
        else:
            selected = [_cand("CONTACT_REFUSE", "contact_refuse_1", contact="REFUSE"),
                        _cand("CONTACT_REFUSE", "contact_refuse_2", contact="REFUSE")]
    elif f["offer_help"]:
        if s["available"]:
            selected = [_cand("HELP_INVITE", "help_invite_1"),
                        _cand("HELP_INVITE", "help_invite_2")]
        elif s["time_pressure"]:
            selected = [_cand("HELP_REFUSE", "help_invite_refuse_1")]
        else:
            selected = [_cand("HELP_REFUSE", "help_refuse_material_1"),
                        _cand("HELP_REFUSE", "help_refuse_material_2")]
    elif f["unsupported_memory"]:
        selected = [_cand("UNSUPPORTED_MEMORY", "unsupported_memory_1"),
                    _cand("UNSUPPORTED_MEMORY", "unsupported_memory_2")]
    elif f["about_b"]:
        if b["observed_offscreen"]:
            event_id = b["observed_offscreen_ids"][-1]
            selected = [_cand("OBSERVED_B", "observed_b_1", {"b_event_id": event_id},
                              knowledge_refs=[event_id])]
        elif b["present_with_a"]:
            selected = [_cand("PRESENT_B", "present_b_1")]
        else:
            selected = [_cand("UNKNOWN_B", "unknown_b_1"),
                        _cand("UNKNOWN_B", "unknown_b_2")]
    elif f["invitation"]:
        selected = [_cand("DECLINE_INVITATION", "decline_invite_1"),
                    _cand("DECLINE_INVITATION", "decline_invite_2")]
    elif f["work"]:
        if h["prior_help"] and s["available"]:
            selected = [_cand("RECALL_WORK", "work_recall_1"),
                        _cand("RECALL_WORK", "work_recall_2")]
        elif s["time_pressure"]:
            selected = [_cand("DEFER_WORK", "defer_work_1"),
                        _cand("DEFER_WORK", "defer_work_2"),
                        _cand("DEFER_WORK", "defer_work_3")]
        elif s["material_pressure"]:
            selected = [_cand("DEFER_WORK", "defer_work_2"),
                        _cand("DEFER_WORK", "help_refuse_material_1")]
        else:
            selected = [_cand("EXPLAIN_WORK", "work_explain_1"),
                        _cand("EXPLAIN_WORK", "work_explain_2"),
                        _cand("EXPLAIN_WORK", "work_explain_3")]
    elif f["self_disclosure"]:
        template = {
            "move": "recip_move_1",
            "work": "recip_work_1",
            "name": "recip_name_1",
        }.get(f["disclosure_topic"], "recip_default_1")
        alternates = {
            "move": "recip_move_2",
            "work": "recip_work_2",
            "name": "recip_name_1",
        }.get(f["disclosure_topic"], "recip_default_1")
        selected = [_cand("RECIPROCATE", template),
                    _cand("RECIPROCATE", alternates)]
    elif f["prior_reference"] and h["prior_user_texts"]:
        prior = h["prior_user_texts"][-1]
        if len(prior) <= 180 and "\n" not in prior:
            selected = [_cand("RECALL", "recall_1",
                              {"prior_text": prior,
                               "prior_event_id": contract["knowledge"].get("last_user_event_id", "")})]
        else:
            selected = [_cand("ACKNOWLEDGE", "ack_1")]
    elif f["question"] and not f["known_topic"]:
        selected = [_cand("DEFER_UNKNOWN", "defer_unknown_1"),
                    _cand("DEFER_UNKNOWN", "defer_unknown_2")]
    elif s["time_pressure"]:
        selected = [Candidate("SILENCE_TASK", "silence_1", {}, None,
                              "A keeps working.", "brisk", "SILENCE", [])]
    else:
        selected = [_cand("ACKNOWLEDGE", "ack_1"),
                    _cand("ACKNOWLEDGE", "ack_2")]
    # Add prior-help acknowledgement variants where they are lawful but not forced.
    if h["prior_help"] and not selected:
        selected = [_cand("ACKNOWLEDGE", "ack_recall_1")]
    version = _stable_index(contract["contract_hash"], selected[0].strategy if selected else "",
                            max(1, len(selected)))
    for index, candidate in enumerate(selected):
        candidate.variant = index
    return selected[version:] + selected[:version]


def _fact_ok(fact: dict, contract: dict) -> bool:
    a = contract["actor"]
    h = contract["history"]
    s = contract["situation"]
    b = contract["b"]
    kind = fact.get("kind")
    if kind == "ACTOR_FIELD":
        return a.get(fact["field"]) == fact["value"]
    if kind == "PROJECT_PRESENT":
        return bool(a.get("project_labels"))
    if kind == "WORLD_RESOURCE":
        resource = contract["world"]["resources"].get(fact["scope"], {})
        return resource.get(fact["field"]) == fact["value"]
    if kind == "TIME_PRESSURE":
        return bool(s["time_pressure"])
    if kind == "MATERIAL_PRESSURE":
        return bool(s["material_pressure"])
    if kind == "TIME_OR_OBLIGATION":
        return bool(
            s["time_pressure"]
            or int(a.get("free_hours", 0)) <= 1
            or int(contract["world"]["clock"]) >= 40
        )
    if kind == "PRIOR_HELP":
        return bool(h["prior_help"])
    if kind == "USER_FEATURE":
        return bool(contract["features"].get(fact["feature"]) == fact["value"])
    if kind == "USER_EVENT":
        event_id = fact.get("event_id", "")
        return any(row["event_id"] == event_id for row in contract["knowledge"]["user_utterances"])
    if kind == "ACTOR_KNOWLEDGE":
        return fact.get("event_id") in contract["knowledge"]["perceived_event_ids"]
    if kind == "KNOWLEDGE_ABSENCE":
        return not bool(b["observed_offscreen"])
    if kind == "B_PRESENT":
        return bool(b["present_with_a"])
    if kind == "MEMORY_ABSENCE":
        return not any("promise" in text.lower()
                       for text in contract["history"]["prior_user_texts"])
    if kind == "CONTACT_FEASIBLE":
        return bool(s["available"] and (h["prior_help"] or h["prior_contact"] or h["user_turns"] >= 2))
    if kind == "CONTACT_NOT_SUPPORTED":
        return not bool(s["available"] and (h["prior_help"] or h["prior_contact"] or h["user_turns"] >= 2))
    return False


def validate(candidate: Candidate, contract: dict, session) -> dict:
    checks: dict[str, bool] = {}
    kind = contract["situation"]["trigger_kind"]
    checks["contract_hash_current"] = candidate.facts is not None
    checks["scene_open_or_message"] = (
        contract["world"]["scene_open"] is True or kind == "MESSAGE"
    )
    checks["actor_present_or_message"] = (
        contract["world"]["a_present"] is True or kind == "MESSAGE"
    )
    checks["not_stale_clock"] = int(contract["world"]["clock"]) == session.clock()
    checks["template_known"] = candidate.template_id in TEMPLATES
    if candidate.action not in {"NONE", "REPAIR", "SILENCE", "MESSAGE"}:
        checks["action_allowed"] = False
    else:
        checks["action_allowed"] = True
    if candidate.speech is None:
        checks["speech_nonempty_or_silence"] = candidate.action in {"SILENCE", "MESSAGE"}
    else:
        checks["speech_nonempty"] = bool(candidate.speech.strip())
        checks["speech_length"] = len(candidate.speech) <= 240
        checks["speech_single_line"] = "\n" not in candidate.speech and "\t" not in candidate.speech
        template = TEMPLATES[candidate.template_id]
        rendered = template["text"].format(**candidate.slots)
        checks["template_rerender_exact"] = rendered == candidate.speech
        checks["no_private_tokens"] = not any(
            token.lower() in candidate.speech.lower() for token in FORBIDDEN
        )
        checks["no_private_values"] = not any(
            str(contract["actor"].get(field)) in candidate.speech
            for field in ("free_hours", "material_remaining", "tools_remaining")
            if contract["actor"].get(field) is not None
        )
    checks["facts_supported"] = all(_fact_ok(fact, contract) for fact in candidate.facts)
    checks["knowledge_refs"] = all(
        ref in contract["knowledge"]["perceived_event_ids"]
        for ref in candidate.knowledge_refs
    )
    if candidate.action == "REPAIR":
        checks["repair_capacity"] = bool(
            int(contract["actor"].get("free_hours", 0)) >= 1
            and int(contract["actor"].get("material_remaining", 0)) >= 1
            and int(contract["actor"].get("tools_remaining", 0)) >= 1
        )
        checks["a_at_workshop"] = contract["world"]["positions"].get("A") == "workshop"
    if candidate.contact == "GRANT":
        checks["contact_feasible"] = bool(
            contract["situation"]["available"]
            and (contract["history"]["prior_help"]
                 or contract["history"]["prior_contact"]
                 or contract["history"]["user_turns"] >= 2)
        )
    if candidate.action == "MESSAGE":
        checks["message_has_contact"] = bool(contract["world"]["contact"])
    return {"ok": all(checks.values()), "checks": checks}


def _speech_event(session, candidate: Candidate, contract: dict, admission_id: str) -> dict:
    world = session.world()
    event = make_event(
        clock=world.clock, kind="SPEECH", actor_id="A",
        location=world.positions.get("A", "workshop"),
        summary=f"A says: {candidate.speech}",
        body={
            "text": candidate.speech,
            "gesture": candidate.gesture,
            "tone": candidate.tone,
            "strategy": candidate.strategy,
            "contract_hash": contract["contract_hash"],
            "admission_id": admission_id,
        },
        sequence=len(world.events),
    )
    world.add_event(event)
    session._append_event(event, perceive=("A",))
    session._perceive_if_present(event, "U", "B")
    session.product._append_episode(
        session.branch_id, "A", "SAY", world.clock,
        {"event_id": event["event_id"], "text": candidate.speech,
         "gesture": candidate.gesture, "tone": candidate.tone,
         "strategy": candidate.strategy, "contract_hash": contract["contract_hash"],
         "admission_id": admission_id})
    session.product._checkpoint(session.branch_id, world.clock, world)
    return event


def admit(session, contract: dict, candidate: Candidate) -> dict:
    validation = validate(candidate, contract, session)
    if not validation["ok"]:
        raise ValueError("CANDIDATE_NOT_ADMISSIBLE:" + json.dumps(
            [k for k, v in validation["checks"].items() if not v]))
    world = session.world()
    action_event = None
    contact_outcome = candidate.contact
    if candidate.action == "REPAIR":
        receipt = owner_receipt(act="REPAIR", actor_id="A", clock=world.clock,
                                location=world.positions["A"])
        action_event = repair_event(world, actor_id="A", receipt=receipt)
        session._append_event(action_event, perceive=("A",))
        session._perceive_if_present(action_event, "U", "B")
        session.product._append_episode(
            session.branch_id, "A", "DO", world.clock,
            {"action": "repair", "admitted": True,
             "event_id": action_event["event_id"], "user_proposal": True,
             "strategy": candidate.strategy, "contract_hash": contract["contract_hash"]})
    admission_id = digest({
        "candidate": candidate.public(),
        "contract_hash": contract["contract_hash"],
        "clock": world.clock,
        "action_event": action_event["event_id"] if action_event else "",
    })
    speech_event = None
    message_episode = None
    if candidate.action == "MESSAGE":
        message_episode = session.product._append_episode(
            session.branch_id, "A", "MESSAGE", world.clock,
            {"text": candidate.speech, "direction": "to_user",
             "channel": "landing_line", "strategy": candidate.strategy,
             "contract_hash": contract["contract_hash"],
             "admission_id": admission_id, "action_seq": session._action_seq()})
    elif candidate.speech is not None:
        speech_event = _speech_event(session, candidate, contract, admission_id)
    elif candidate.action == "SILENCE":
        silence = make_event(
            clock=world.clock, kind="NO_CHANGE", actor_id="A",
            location=world.positions.get("A", "workshop"),
            summary="A keeps working; no answer.",
            body={"silence": True, "strategy": candidate.strategy,
                  "contract_hash": contract["contract_hash"],
                  "admission_id": admission_id},
            sequence=len(world.events),
        )
        world.add_event(silence)
        session._append_event(silence, perceive=("A",))
        session._perceive_if_present(silence, "U", "B")
        session.product._append_episode(
            session.branch_id, "A", "SILENCE", world.clock,
            {"event_id": silence["event_id"], "strategy": candidate.strategy,
             "contract_hash": contract["contract_hash"], "admission_id": admission_id})
        session.product._checkpoint(session.branch_id, world.clock, world)
        speech_event = silence
    if contact_outcome in {"GRANT", "REFUSE", "DEFER"}:
        established = contact_outcome == "GRANT"
        session.product._append_episode(
            session.branch_id, "A", "CONTACT", world.clock,
            {"established": established, "channel": "landing_line" if established else "",
             "outcome": contact_outcome, "contract_hash": contract["contract_hash"],
             "admission_id": admission_id, "action_seq": session._action_seq()})
        session.product._append_episode(
            session.branch_id, USER_ACTOR, "CONTACT", world.clock,
            {"established": established, "channel": "landing_line" if established else "",
             "outcome": contact_outcome, "contract_hash": contract["contract_hash"],
             "admission_id": admission_id, "action_seq": session._action_seq()})
        session.product._checkpoint(session.branch_id, world.clock, world)
    admission = {
        "schema": ADMISSION_SCHEMA,
        "admission_id": admission_id,
        "grade": GRADE,
        "native": False,
        "strategy": candidate.strategy,
        "template_id": candidate.template_id,
        "contract_hash": contract["contract_hash"],
        "source_ref": contract["source_ref"],
        "target_id": contract["source"]["target_id"],
        "consumed_state_hash": contract["source"]["consumed_state_hash"],
        "clock": world.clock,
        "speech_event_id": speech_event["event_id"] if speech_event else "",
        "message_episode_id": message_episode["episode_id"] if message_episode else "",
        "action_event_id": action_event["event_id"] if action_event else "",
        "contact_outcome": contact_outcome,
        "validation": validation,
        "fact_count": len(candidate.facts),
        "knowledge_ref_count": len(candidate.knowledge_refs),
        "motive_status": contract["motive_status"],
        "attention_excluded": True,
    }
    session.product._append_episode(
        session.branch_id, "A", "EXPRESSION_ADMISSION", world.clock,
        {"admission": admission, "candidate": candidate.public(),
         "contract_hash": contract["contract_hash"]})
    session.product._checkpoint(session.branch_id, world.clock, world)
    return {
        "admission": admission,
        "candidate": candidate.public(),
        "event_ids": [e["event_id"] for e in (action_event, speech_event) if e],
        "contact": contact_outcome,
    }


def respond(session, *, trigger_kind: str, text: str = "",
            event_id: str = "") -> dict:
    contract = compile_contract(session, trigger_kind=trigger_kind,
                                trigger_text=text, trigger_event_id=event_id)
    candidates = propose(contract)
    failures = []
    for candidate in candidates:
        validation = validate(candidate, contract, session)
        if not validation["ok"]:
            failures.append({"template_id": candidate.template_id,
                             "strategy": candidate.strategy,
                             "failed": [k for k, v in validation["checks"].items() if not v]})
            continue
        result = admit(session, contract, candidate)
        result["contract"] = contract
        result["candidates"] = [c.public() for c in candidates]
        result["fallback_failures"] = failures
        return result
    # Bounded lawful silence: one fallback occurrence, no loop.
    silence = Candidate("LAWFUL_SILENCE", "silence_1", {}, None,
                        "A keeps working.", "brisk", "SILENCE", [])
    result = admit(session, contract, silence)
    result["contract"] = contract
    result["candidates"] = [c.public() for c in candidates]
    result["fallback_failures"] = failures
    return result
