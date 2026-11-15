"""Public projection from actual S45 encounter results to the pinned WP19 surface."""
from __future__ import annotations

from typing import Any, Mapping

VIEW_SCHEMA = "SOROK_WP19_ENCOUNTER_VIEW@1"
RESULT_SCHEMA = "SOROK_WP19_INTERACTION_RESULT@1"
STATUS_SCHEMA = "SOROK_WP19_STATUS@1"
GRADE = "TEST_ONLY_S45_WP19_PROJECTION_NOT_NATIVE"
SOURCE = "s45"
S45_COMMIT = "f26a138e20d53c809d611cf8d834ec647b0804bf"
SOURCE_REF = "S45_C12_WORLD_EVENT@" + S45_COMMIT[:7]
EXIT_LABEL = "Exit portal"
RETURN_LABEL = "Return to encounter"

PUBLIC_EVENT_FIELDS = (
    "event_id",
    "kind",
    "clock",
    "location",
    "actor_visible_id",
    "summary",
    "body_public",
    "source_ref",
    "perceived_by_user",
)

PUBLIC_BODY_FIELDS = (
    "text",
    "gesture",
    "tone",
    "strategy",
    "public_role",
    "observable",
    "language_tag",
    "changed",
    "cash_delta",
    "completed_delta",
    "hours_delta",
    "material_delta",
    "source_owned",
    "present_with",
)

PORTAL_CONTROLS = ("SAY", "DO", "ATTEND", "WAIT", "EXIT")

HIDDEN_FIELDS = (
    "actor_traits",
    "affinity",
    "trust",
    "suspicion",
    "private_motive",
    "private_emotion",
    "private_actor_model",
    "unperceived_event_content",
    "relationship_score",
    "rarity",
    "completion_percentage",
    "unlock_level",
    "hidden_market_commission",
    "future_outcome",
)

TYPED_HOLDS = {
    "WAIT": "WAIT_UNSUPPORTED_TYPED_HOLD",
    "EXIT": "LOCAL_EXIT_ONLY",
    "RETURN": "RETURN_UNSUPPORTED_TYPED_HOLD",
    "ABSENCE": "USER_ABSENCE_LIFE_ADVANCE_MISSING",
}

REMAINING_MISSING_PRODUCERS = (
    "WAIT_TIME_ADVANCE_RECEIPT",
    "PORTAL_EXIT_RETURN_RECEIPT",
    "USER_ABSENCE_LIFE_ADVANCE",
    "MESSAGE_CHANNEL_ESTABLISHMENT_AND_DELIVERY",
    "ACCESSIBILITY_PREFERENCE_ACK",
)

SUPPLIED_BY_S45 = (
    "USER_SAY_DO_ATTEMPT_ADMISSION",
    "USER_ATTEND_RECEIPT",
)

PRIVATE_KEYS = frozenset({
    "access_receipt",
    "access_receipt_id",
    "access_receipt_ids",
    "actor_id",
    "actor_state",
    "admission",
    "admission_id",
    "attempt_hash",
    "attempt_status",
    "branch_id",
    "c8_content_hash",
    "c8_occurrence_id",
    "c8_state_digest",
    "c9",
    "c9_lineage",
    "contract_hash",
    "consumed_state_hash",
    "encounter_id",
    "encounter_hash",
    "episode_id",
    "equivalence_codes",
    "equivalence_receipt_hash",
    "equivalence_status",
    "generation_hash",
    "generation_source_refs",
    "hash",
    "history_predicate",
    "history_refs",
    "language",
    "lme",
    "native_artifact_hash",
    "owner_receipt",
    "plan",
    "plan_hash",
    "private_generation_sources_in_plan",
    "projection_episode_id",
    "root_hash",
    "root_id",
    "selected_option",
    "source_event_hash",
    "source_event_id",
    "source_event_ids",
    "source_event_refs",
    "source_operation",
    "spans",
    "target_proposals",
    "target_state_rows",
    "translation_artifact_hash",
    "world_after",
    "world_before",
})

FORBIDDEN_VALUE_MARKERS = (
    "LME_ACCESS_",
    "TEST_ONLY_S39_",
    "TEST_ONLY_BP1_R26V_ACTOR",
    "TEST_ONLY_BP2_E1_OCC",
    "world_before",
    "generation_source_refs",
    "history_refs",
    "source_event_refs",
    "admission_id",
    "plan_hash",
)


def _public_body(body: Mapping[str, Any]) -> dict:
    return {
        key: body[key]
        for key in PUBLIC_BODY_FIELDS
        if key in body and isinstance(body[key], (str, int, float, bool, list, tuple, dict))
    }


def project_event(event: Mapping[str, Any]) -> dict:
    body = event.get("body") or {}
    return {
        "event_id": str(event.get("event_id") or ""),
        "kind": str(event.get("kind") or ""),
        "clock": event.get("clock"),
        "location": str(event.get("location") or ""),
        "actor_visible_id": str(event.get("actor_id") or ""),
        "summary": str(event.get("summary") or ""),
        "body_public": _public_body(body if isinstance(body, Mapping) else {}),
        "source_ref": SOURCE_REF,
        "perceived_by_user": True,
    }


def _status_for(control: str, raw_status: str, strategy: str) -> tuple[str, str]:
    if raw_status == "UNSUPPORTED":
        return "UNKNOWN", "S45_UNSUPPORTED_INPUT"
    if control == "ATTEND":
        return raw_status or "NO_CHANGE", "LOCAL_ATTEND_ONLY"
    if strategy == "HELP_REFUSE":
        return "REFUSED", "S45_HELP_REFUSE"
    if strategy:
        return raw_status or "OK", "S45_" + strategy
    return raw_status or "OK", "S45_OK"


def project_result(
    control: str,
    result: Mapping[str, Any],
    *,
    user_input: str = "",
    clock_before: int = 0,
    clock_after: int = 0,
    store_hash_before: str = "",
    store_hash_after: str = "",
    mode: str = "PORTAL",
) -> dict:
    control = control.upper()
    if control not in {"SAY", "DO_HELP", "ATTEND"}:
        raise ValueError("UNSUPPORTED_S45_PROJECTION_CONTROL:" + control)
    raw_status = str(result.get("status") or "")
    strategy = str(result.get("strategy") or "")
    admission = result.get("admission") or {}
    language = result.get("language") or {}
    candidate = result.get("candidate") or {}
    user_event = result.get("user_event") or {}
    speech = str(language.get("native_text") or candidate.get("speech") or "")
    translation = str(
        language.get("translation_text") or candidate.get("speech_english") or ""
    )
    gesture = str(candidate.get("gesture") or "")
    action_event_id = str(admission.get("action_event_id") or "")
    speech_event_id = str(
        language.get("speech_event_id") or admission.get("speech_event_id") or ""
    )
    user_event_id = str(user_event.get("event_id") or "")
    accepted = result.get("accepted")
    status, code = _status_for(control, raw_status, strategy)
    actor_response = None
    if control != "ATTEND" and status != "UNKNOWN":
        actor_response = {
            "strategy": strategy,
            "speech": speech,
            "speech_english": translation,
            "gesture": gesture,
            "action": "REPAIR" if action_event_id else "",
            "performed": bool(action_event_id),
            "performed_by": "A" if action_event_id else "",
        }
    event_ids = [
        event_id
        for event_id in (user_event_id, speech_event_id, action_event_id)
        if event_id
    ]
    if control == "ATTEND":
        world_event_created = False
    else:
        world_event_created = bool(user_event_id or speech_event_id or action_event_id)
    user_attempt = {
        "control": control,
        "input": str(user_input),
        "source_status": raw_status,
        "accepted": accepted if control != "ATTEND" else None,
        "attempted": True,
        "performed": False,
    }
    projected = {
        "schema": RESULT_SCHEMA,
        "grade": GRADE,
        "native": False,
        "source": SOURCE,
        "control": control,
        "status": status,
        "code": code,
        "reason": str(result.get("reason") or ""),
        "attempted": True,
        "performed": False,
        "world_event_created": world_event_created,
        "clock_changed": int(clock_before) != int(clock_after),
        "actor_response_generated": bool(actor_response and speech),
        "simulated_delivery": False,
        "refusal": status == "REFUSED",
        "mode": mode,
        "user_attempt": user_attempt,
        "actor_response": actor_response,
        "event_ids": event_ids,
        "surface": list(result.get("surface") or []),
        "store_hash_before": store_hash_before,
        "store_hash_after": store_hash_after,
    }
    return projected


def _encounter_public(
    encounter: Mapping[str, Any],
    *,
    gesture_by_event: Mapping[str, str],
    translation_by_event: Mapping[str, str],
) -> dict:
    kind = str(encounter.get("kind") or "")
    status = encounter.get("status")
    strategy = str(encounter.get("strategy") or "")
    speech_event_id = str(encounter.get("speech_event_id") or "")
    speech = str(encounter.get("native_text") or "")
    translation = str(
        encounter.get("translation_text")
        or translation_by_event.get(speech_event_id, "")
    )
    accepted = None if kind == "ATTEND" else (
        status == "OK" and strategy in {"HELP_ACCEPT", "HELP_INVITE"}
    )
    return {
        "kind": kind,
        "status": status,
        "strategy": strategy,
        "accepted": accepted,
        "refusal": strategy == "HELP_REFUSE",
        "user_text": str(encounter.get("user_text") or ""),
        "speech": speech,
        "speech_english": translation,
        "gesture": gesture_by_event.get(speech_event_id, ""),
    }


def project_view(
    session,
    *,
    mode: str = "PORTAL",
    controls: tuple[str, ...] = PORTAL_CONTROLS,
    hidden_fields: tuple[str, ...] = HIDDEN_FIELDS,
    uncertainty: tuple[str, ...] = REMAINING_MISSING_PRODUCERS,
    accessible: Mapping[str, Any] | None = None,
    exit_label: str = EXIT_LABEL,
    return_label: str = RETURN_LABEL,
) -> dict:
    raw_events = list(session.events())
    perceived = set(session.user_perceived_ids())
    visible = [
        project_event(event)
        for event in raw_events
        if str(event.get("event_id") or "") in perceived
    ]
    encounters = list(session.read_encounters())
    translation_by_event = {
        str(row.get("speech_event_id") or ""): str(row.get("translation_text") or "")
        for row in encounters
        if row.get("speech_event_id")
    }
    gesture_by_event = {
        str(event.get("event_id") or ""): str(
            (event.get("body") or {}).get("gesture") or ""
        )
        for event in visible
        if event.get("kind") == "SPEECH"
    }
    visible_speech = []
    for event in visible:
        if event.get("kind") != "SPEECH":
            continue
        body = event.get("body_public") or {}
        visible_speech.append({
            "event_id": event.get("event_id", ""),
            "speaker": event.get("actor_visible_id", ""),
            "clock": event.get("clock"),
            "text": body.get("text", ""),
            "labeled_english": translation_by_event.get(
                str(event.get("event_id") or ""), ""
            ),
            "gesture": body.get("gesture", ""),
            "strategy": body.get("strategy", ""),
            "summary": event.get("summary", ""),
        })
    visible_actions = [
        event for event in visible if event.get("kind") != "SPEECH"
    ]
    help_rows = [
        row for row in encounters if row.get("kind") in {"SAY", "DO_HELP"}
    ]
    admission = (
        _encounter_public(
            help_rows[-1],
            gesture_by_event=gesture_by_event,
            translation_by_event=translation_by_event,
        )
        if help_rows
        else None
    )
    world = session.world()
    resources = getattr(world, "resources", {}) or {}
    workshop = resources.get("workshop", {}) if isinstance(resources, Mapping) else {}
    actor_state = getattr(world, "actor_state", {}) or {}
    actor_a = actor_state.get("A", {}) if isinstance(actor_state, Mapping) else {}
    positions = getattr(world, "positions", {}) or {}
    location = positions.get("U") or positions.get("A") or "UNKNOWN"
    default_accessible = {
        "keyboard_only": True,
        "focus_order": [
            "transcript",
            "SAY input",
            "DO input",
            "ATTEND target",
            "WAIT",
            "EXIT",
            "RETURN",
        ],
        "screen_reader_labels": {
            "SAY": "Say something",
            "DO": "Attempt an action",
            "ATTEND": "Attend to a visible event or object",
            "WAIT": "Wait without advancing time",
            "EXIT": exit_label,
            "RETURN": return_label,
        },
        "text_alternatives": True,
        "color_only_meaning": False,
        "exit_always_visible": True,
        "typed_holds_announced": True,
    }
    unperceived = max(0, len(raw_events) - len(visible))
    announcements = [
        "Mode: " + str(mode).lower() + ".",
        "Clock: " + str(session.clock()) + ".",
        "Location: " + str(location or "UNKNOWN") + ".",
        "Visible events: " + str(len(visible)) + ".",
        "Unperceived events remain unknown: " + str(unperceived) + ".",
        "Exit is always available.",
        "Return requires an actual meeting or channel; typed hold otherwise.",
    ]
    view = {
        "schema": VIEW_SCHEMA,
        "grade": GRADE,
        "native": False,
        "source": SOURCE,
        "mode": mode,
        "clock": session.clock(),
        "location": location,
        "visible_events": visible,
        "visible_speech": visible_speech,
        "visible_actions": visible_actions,
        "encounter_admission": admission,
        "unperceived_event_count": unperceived,
        "tool_available": bool(workshop.get("tool_available")),
        "tools_remaining": actor_a.get("tools_remaining"),
        "refusal_present": bool(admission and admission.get("refusal")),
        "absence_evidence": (
            "UNPERCEIVED_EVENTS_REMAIN_UNKNOWN"
            if unperceived
            else "NO_UNPERCEIVED_EVENT_IN_THIS_VIEW"
        ),
        "accessible": dict(accessible or default_accessible),
        "accessibility_announcement": announcements,
        "controls": list(controls),
        "exit_control": {
            "label": exit_label,
            "always_visible": True,
            "accessible": True,
        },
        "return_control": {
            "label": return_label,
            "available": False,
            "reason": TYPED_HOLDS["RETURN"],
        },
        "hidden_state_held": True,
        "hidden_fields": list(hidden_fields),
        "uncertainty": list(uncertainty),
    }
    return view


__all__ = [
    "EXIT_LABEL",
    "FORBIDDEN_VALUE_MARKERS",
    "GRADE",
    "HIDDEN_FIELDS",
    "PORTAL_CONTROLS",
    "PRIVATE_KEYS",
    "PUBLIC_BODY_FIELDS",
    "PUBLIC_EVENT_FIELDS",
    "REMAINING_MISSING_PRODUCERS",
    "RESULT_SCHEMA",
    "RETURN_LABEL",
    "S45_COMMIT",
    "SOURCE",
    "SOURCE_REF",
    "STATUS_SCHEMA",
    "SUPPLIED_BY_S45",
    "TYPED_HOLDS",
    "VIEW_SCHEMA",
    "project_event",
    "project_result",
    "project_view",
]
