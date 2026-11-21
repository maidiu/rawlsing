"""E01/J1 sourcefree composition of C04/P6 speech experience and D03 uptake.

This module is a read-only integration seam. It consumes the actual committed
parent speech through the normal P6 child-experience path, the actual D03
immediate uptake over the same C12 child receipt, and the admitted/performed
parent decision. It does not choose a child response, write durable state, or
promote D03 eligible modes into a performed child event.

The terminal E01 step is deliberately held: no existing sourcefree owner or
rule selects a child response and performs a subsequent child event. D04/D05
are queued, unlaunched dependencies, so the join reports the exact missing
performer instead of inventing one.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

from developmental_recursion.contracts import RecursionRefusal, detached, digest
from developmental_recursion.parent_decision import read_parent_decision
from p3 import immediate_uptake

GRADE = "SOURCEFREE_S2_ONLY"
SCHEMA = "SOROK_E01_J1_THREE_HEAD_JOIN@1"
SOURCE_SCHEMA = "SOROK_E01_J1_SOURCE_CLOSURE@1"
HELD_JOIN = "SUBSEQUENT_CHILD_EVENT_HELD_NO_COMPETENT_PERFORMER"
UPSTREAM_PROVEN = "UPSTREAM_CAUSAL_CHAIN_PROVEN_SUBSEQUENT_EVENT_HELD"
_WORKER_RETURNS = Path(__file__).resolve().parents[1]


def _refuse(code: str, detail: str = "") -> None:
    raise RecursionRefusal(code if not detail else code + ":" + detail)


def _text(value: Any, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _refuse(code)
    return value


def _mapping(value: Any, code: str) -> dict:
    if not isinstance(value, Mapping):
        _refuse(code)
    return detached(value)


def _hash(value: Any, code: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        _refuse(code)
    try:
        int(value, 16)
    except ValueError:
        _refuse(code)
    return value.lower()


def _label(path: Path) -> str:
    path = Path(path).resolve()
    try:
        return str(path.relative_to(_WORKER_RETURNS))
    except ValueError:
        return str(path)


def _additional_source_files() -> list[Path]:
    return [
        _WORKER_RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1" / "run_p6.py",
        _WORKER_RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1" / "situated.py",
        _WORKER_RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1" / "house.py",
        _WORKER_RETURNS / "SOROK-DUEL-B02-R1" / "historical_period.py",
        _WORKER_RETURNS / "SOROK-DUEL-B04-R1" / "material_operations.py",
        _WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
        / "developmental_recursion" / "parent_decision.py",
        _WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
        / "developmental_recursion" / "parent_activity.py",
    ]


def source_closure() -> dict:
    """Pin D03's reader closure plus the additional J1 readers it consumes."""
    rows: dict[str, Path] = {}
    for row in immediate_uptake.source_closure().get("files", []):
        label = _text(row.get("path"), "J1_D03_SOURCE_LABEL")
        rows[label] = (_WORKER_RETURNS / label).resolve()
    for path in _additional_source_files():
        path = path.resolve()
        rows[_label(path)] = path
    files = []
    for label, path in sorted(rows.items()):
        if not path.is_file():
            _refuse("J1_SOURCE_MISSING:" + label)
        files.append({
            "path": label,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    return {"schema": SOURCE_SCHEMA, "files": files, "hash": digest(files)}


def _expected_closure_hash(value: Any) -> str:
    if isinstance(value, str):
        return _hash(value, "J1_EXPECTED_SOURCE_CLOSURE")
    document = _mapping(value, "J1_EXPECTED_SOURCE_CLOSURE")
    return _hash(document.get("hash"), "J1_EXPECTED_SOURCE_CLOSURE:HASH")


def _validate_experience(experience: Mapping[str, Any],
                         utterance_receipt: Mapping[str, Any],
                         child_id: str) -> dict:
    body = _mapping(experience, "J1_CHILD_EXPERIENCE")
    if body.get("status") != "PERCEIVED":
        _refuse("J1_CHILD_EXPERIENCE_NOT_PERCEIVED")
    if body.get("schema") != "SOROK_CHILD_SPEECH_EXPERIENCE@1":
        _refuse("J1_CHILD_EXPERIENCE_SCHEMA")
    if body.get("p6_experience_source") != "situated.recent_speech":
        _refuse("J1_CHILD_EXPERIENCE_SOURCE")
    if body.get("child_actor_id") != child_id:
        _refuse("J1_CHILD_EXPERIENCE_CHILD_MISMATCH")
    event_id = _text(body.get("event_id"), "J1_CHILD_EXPERIENCE_EVENT")
    event_hash = _hash(body.get("event_hash"), "J1_CHILD_EXPERIENCE_HASH")
    if utterance_receipt.get("event_id") != event_id:
        _refuse("J1_UTTERANCE_EVENT_MISMATCH")
    if utterance_receipt.get("event_hash") != event_hash:
        _refuse("J1_UTTERANCE_HASH_MISMATCH")
    if body.get("speaker_actor_id") != utterance_receipt.get("actor_id"):
        _refuse("J1_SPEAKER_MISMATCH")
    if body.get("speaker_alias") != utterance_receipt.get("alias"):
        _refuse("J1_SPEAKER_ALIAS_MISMATCH")
    event = body.get("event")
    if not isinstance(event, Mapping):
        _refuse("J1_CHILD_EXPERIENCE_EVENT_BODY")
    public = event.get("body_public")
    if not isinstance(public, Mapping):
        _refuse("J1_CHILD_EXPERIENCE_PUBLIC_BODY")
    if public.get("text") != utterance_receipt.get("text"):
        _refuse("J1_UTTERANCE_TEXT_MISMATCH")
    response_input = body.get("response_input")
    if not isinstance(response_input, Mapping):
        _refuse("J1_CHILD_RESPONSE_INPUT")
    if response_input.get("event_id") != event_id:
        _refuse("J1_CHILD_RESPONSE_EVENT_MISMATCH")
    if response_input.get("public_text") != public.get("text"):
        _refuse("J1_CHILD_RESPONSE_TEXT_MISMATCH")
    if body.get("hidden_reason") != "NOT_READ":
        _refuse("J1_CHILD_EXPERIENCE_PRIVATE_INPUT")
    return body


def _validate_d03(d03: Mapping[str, Any], experience: Mapping[str, Any],
                  utterance_receipt: Mapping[str, Any], child_id: str) -> dict:
    body = _mapping(d03, "J1_D03_OUTPUT")
    if body.get("schema") != immediate_uptake.SCHEMA:
        _refuse("J1_D03_SCHEMA")
    speech = body.get("speech_scope")
    if not isinstance(speech, Mapping):
        _refuse("J1_D03_SPEECH_SCOPE")
    if speech.get("status") != "PERCEIVED":
        _refuse("J1_D03_NOT_PERCEIVED")
    if speech.get("event_id") != experience.get("event_id"):
        _refuse("J1_D03_EVENT_MISMATCH")
    if speech.get("event_hash") != experience.get("event_hash"):
        _refuse("J1_D03_HASH_MISMATCH")
    if speech.get("speaker_actor_id") != experience.get("speaker_actor_id"):
        _refuse("J1_D03_SPEAKER_MISMATCH")
    if speech.get("alias") != experience.get("speaker_alias"):
        _refuse("J1_D03_SPEAKER_ALIAS_MISMATCH")
    if speech.get("child_actor_id") != child_id:
        _refuse("J1_D03_CHILD_MISMATCH")
    if speech.get("text") != utterance_receipt.get("text"):
        _refuse("J1_D03_TEXT_MISMATCH")
    if speech.get("hidden_reason") != "NOT_READ":
        _refuse("J1_D03_PRIVATE_INPUT")
    return body


def _decision_evidence(session: Any, parent_id: str, decision_id: str) -> dict:
    decision = read_parent_decision(
        session, parent_id, decision_id, as_actor=parent_id)
    proposal = decision.get("proposal") or {}
    evaluation = proposal.get("evaluation") or {}
    feasibility = evaluation.get("b03_feasibility") or {}
    action = decision.get("action") or {}
    return {
        "decision_id": decision_id,
        "decision": detached(decision.get("decision") or {}),
        "performed": bool(decision.get("performed")),
        "action": {
            "status": action.get("status"),
            "decision_action": action.get("decision_action"),
            "performed": bool(action.get("performed")),
            "valid_empty": bool(action.get("valid_empty")),
            "physical_admission": action.get("physical_admission"),
            "possession": action.get("possession"),
            "event_effect": action.get("event_effect"),
        },
        "objective_feasibility": {
            "status": feasibility.get("status"),
            "reasons": list(feasibility.get("reasons") or []),
            "unknowns": list(feasibility.get("unknowns") or []),
        },
        "evaluation_reasons": list(evaluation.get("reasons") or []),
        "evaluation_unknowns": list(evaluation.get("unknowns") or []),
        "child_request": "NOT_EVALUATED",
        "nadia_state": "NOT_READ",
    }


def _held_subsequent() -> dict:
    return {
        "status": HELD_JOIN,
        "performed": False,
        "admitted_event": None,
        "eligible_modes_are_candidates_not_actions": True,
        "native_action": "NOT_ISSUED_BY_D03_RULE",
        "durable_formation": "MISSING_RULE",
        "missing_owner": "D04_TARGET_RULE_OR_D05_PERFORMED_CONSUMER",
        "required_next_owner": (
            "an explicit sourcefree target/recruiter rule plus an authorized "
            "child-event performer; D04 and D05 are queued and unlaunched"),
        "reason": "NO_COMPETENT_SOURCEFREE_CHILD_EVENT_PERFORMER",
    }


def compose_j1(
    owner: Any,
    session: Any,
    *,
    child_id: str,
    speech_event_id: str,
    utterance_receipt: Any,
    plan: Any,
    expected: Any = None,
    expected_source_closure: Any = None,
    expected_speaker_actor_id: str | None = None,
) -> dict:
    """Consume the actual speech/perception chain and hold the terminal act."""
    receipt = _mapping(utterance_receipt, "J1_UTTERANCE_RECEIPT")
    closure = source_closure()
    if expected_source_closure is not None:
        if _expected_closure_hash(expected_source_closure) != closure["hash"]:
            _refuse("J1_SOURCE_CLOSURE_CHANGED")
    from run_p6 import child_speech_experience

    experience = child_speech_experience(
        session, event_id=speech_event_id)
    experience_body = _mapping(experience, "J1_CHILD_EXPERIENCE")
    if experience_body.get("status") != "PERCEIVED":
        d03 = immediate_uptake.build_immediate_uptake(
            owner,
            speech_event_id=speech_event_id,
            child_id=child_id,
            utterance_receipt=receipt,
            plan=plan,
            expected=expected,
            expected_speaker_actor_id=expected_speaker_actor_id,
        )
        if d03.get("status") != "HELD_NOT_PERCEIVED":
            _refuse("J1_HELD_D03_STATUS")
        body = {
            "schema": SCHEMA,
            "grade": GRADE,
            "status": "HELD_NOT_PERCEIVED",
            "child_experience": detached(experience_body),
            "immediate_uptake": detached(d03),
            "parent_decision": {
                "status": "NOT_READ_UNPERCEIVED",
                "child_request": "NOT_EVALUATED",
                "nadia_state": "NOT_READ",
            },
            "subsequent_event": _held_subsequent(),
            "source_closure": detached(closure),
            "read_boundary": {
                "child_speech": "NOT_PERCEIVED_NO_TEXT",
                "parent_private_state": "NOT_READ",
                "parent_decision": "NOT_READ",
                "period_context": "NOT_READ",
                "cash": "NOT_READ",
                "portal_user_view": "NOT_READ",
                "store_write": "NOT_WRITTEN",
            },
            "store_head": detached(d03.get("store_head") or {}),
            "native_rule": "MISSING_RULE",
            "native_action": "NOT_ISSUED_BY_D03_RULE",
            "durable_formation": "MISSING_RULE",
        }
        body["hash"] = digest(body)
        return detached(body)

    experience_body = _validate_experience(
        experience_body, receipt, child_id)
    d03 = immediate_uptake.build_immediate_uptake(
        owner,
        speech_event_id=speech_event_id,
        child_id=child_id,
        utterance_receipt=receipt,
        plan=plan,
        expected=expected,
        expected_speaker_actor_id=expected_speaker_actor_id,
    )
    d03_body = _validate_d03(d03, experience_body, receipt, child_id)
    parent_id = _text(
        experience_body.get("speaker_actor_id"), "J1_PARENT_ID")
    decision_id = _text(
        receipt.get("decision_id"), "J1_DECISION_ID")
    parent = _decision_evidence(session, parent_id, decision_id)
    if parent["action"].get("decision_action") != receipt.get("decision_action"):
        _refuse("J1_DECISION_ACTION_MISMATCH")
    if parent["decision"].get("action") != receipt.get("decision_action"):
        _refuse("J1_DECISION_ACTION_MISMATCH")
    body = {
        "schema": SCHEMA,
        "grade": GRADE,
        "status": UPSTREAM_PROVEN,
        "child_experience": detached(experience_body),
        "immediate_uptake": detached(d03_body),
        "parent_decision": parent,
        "subsequent_event": _held_subsequent(),
        "source_closure": detached(closure),
        "read_boundary": {
            "child_speech": "C04_PUBLIC_SPEECH_PLUS_P6_ACTOR_CURRENT_EXPERIENCE",
            "child_readset": "PUBLIC_SPEECH_AND_PRIOR_P3_ORGANIZATION_ONLY",
            "parent_private_state": "NOT_READ",
            "parent_decision": "PARENT_SELF_READ_NOT_CHILD_FACING",
            "period_context": "NOT_READ",
            "cash": "NOT_READ",
            "portal_user_view": "NOT_READ",
            "world_material": "PARENT_FEASIBILITY_BEFORE_PERFORM_ONLY",
            "store_write": "NOT_WRITTEN",
        },
        "store_head": detached(d03_body.get("store_head") or {}),
        "native_rule": "MISSING_RULE",
        "native_action": "NOT_ISSUED_BY_D03_RULE",
        "durable_formation": "MISSING_RULE",
    }
    body["hash"] = digest(body)
    return detached(body)


__all__ = [
    "compose_j1",
    "source_closure",
    "SCHEMA",
    "GRADE",
    "HELD_JOIN",
    "UPSTREAM_PROVEN",
]
