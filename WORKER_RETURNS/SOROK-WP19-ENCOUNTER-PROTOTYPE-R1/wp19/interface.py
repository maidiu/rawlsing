"""Runnable bounded WP-19 encounter interface over real read-side consumers."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from . import sources, spec

VIEW_SCHEMA = "SOROK_WP19_ENCOUNTER_VIEW@1"
RESULT_SCHEMA = "SOROK_WP19_INTERACTION_RESULT@1"
GRADE = "TEST_ONLY_SOURCEFREE_UX_PROTOTYPE_NOT_NATIVE"
EXIT_LABEL = "Exit portal"
RETURN_LABEL = "Return to encounter"
PORTAL_CONTROLS = ("SAY", "DO", "ATTEND", "WAIT", EXIT_LABEL.upper())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _public_event(event: dict, source_ref: str) -> dict:
    return {
        "event_id": event.get("event_id", ""),
        "kind": event.get("kind", ""),
        "clock": event.get("clock"),
        "location": event.get("location", ""),
        "summary": event.get("summary", ""),
        "body_public": dict(event.get("body") or {}),
        "source_ref": source_ref,
        "perceived_by_user": True,
    }


def _speech(event: dict) -> dict:
    body = event.get("body") or {}
    return {
        "event_id": event.get("event_id", ""),
        "speaker": event.get("actor_id", ""),
        "clock": event.get("clock"),
        "text": body.get("text", ""),
        "gesture": body.get("gesture", ""),
        "strategy": body.get("strategy", ""),
        "summary": event.get("summary", ""),
    }


class EncounterInterface:
    """One source-bound low-fidelity encounter view and control surface."""

    def __init__(
        self,
        source: str,
        root: str | Path | None = None,
        *,
        disposition: str = "PERFORMED",
        perform: str = "omit",
    ) -> None:
        self.source = source
        self.disposition = disposition
        self.perform = perform
        self.mode = "PORTAL"
        self._spec = spec.load()
        self._controls = list(
            self._spec["surfaces"]["PORTAL"]["controls"]
        )
        self._hidden = set(self._spec["hidden_fields"])
        if source == "join-e":
            self.root = (
                Path(root).resolve()
                if root
                else Path(sources.RUNTIME / "wp19-join-e-root")
            )
            self._bundle = sources.run_join_e_probe(
                state_root=self.root,
                disposition=disposition,
                perform=perform,
                mode="start",
                do_help=True,
            )
            self._cp_view = None
            self._store_path = sources.join_e_store_path(self._bundle)
        elif source == "cp-a5":
            self.root = (
                Path(root).resolve()
                if root
                else Path(sources.RUNTIME / "wp19-cp-a5-root")
            )
            sources.materialize_cp_a5(self.root)
            self._cp_view = sources.run_cp_a5_command(self.root, "view")
            self._bundle = None
            self._store_path = sources.cp_a5_store_path(self.root)
        else:
            raise ValueError("UNKNOWN_WP19_SOURCE:" + source)
        self._baseline_store_hash = (
            _sha256(self._store_path) if self._store_path.exists() else ""
        )
        self._last_result: dict | None = None

    @property
    def store_path(self) -> Path:
        return self._store_path

    def _store_hash(self) -> str:
        return _sha256(self._store_path) if self._store_path.exists() else ""

    def _result(
        self,
        status: str,
        *,
        code: str,
        attempted: bool = False,
        performed: bool = False,
        world_event_created: bool = False,
        clock_changed: bool = False,
        **extra: Any,
    ) -> dict:
        before = self._store_hash()
        result = {
            "schema": RESULT_SCHEMA,
            "grade": GRADE,
            "native": False,
            "source": self.source,
            "status": status,
            "code": code,
            "attempted": attempted,
            "performed": performed,
            "world_event_created": world_event_created,
            "clock_changed": clock_changed,
            "actor_response_generated": False,
            "simulated_delivery": False,
            "store_hash_before": before,
            "store_hash_after": self._store_hash(),
            **extra,
        }
        self._last_result = result
        return result

    def _join_e_visible(self) -> dict:
        bundle = self._bundle
        perceptions = bundle.get("perceptions") or []
        viewer = "U" if any(
            row.get("actor_id") == "U" for row in perceptions
        ) else "A"
        known_ids = {
            row.get("event_id")
            for row in perceptions
            if row.get("actor_id") == viewer
        }
        events = bundle.get("world_events") or []
        visible = [
            event for event in events if event.get("event_id") in known_ids
        ]
        speech = [
            _speech(event) for event in visible if event.get("kind") == "SPEECH"
        ]
        actions = [
            _public_event(event, "JOIN_E_C12_WORLD_EVENT@5e6367")
            for event in visible
            if event.get("kind") != "SPEECH"
        ]
        help_result = bundle.get("help") or {}
        help_public = {
            "accepted": help_result.get("accepted"),
            "strategy": help_result.get("strategy"),
            "surface": help_result.get("surface", []),
        } if help_result else None
        clock = bundle.get("branch_clock")
        return {
            "viewer_actor": viewer,
            "clock": clock,
            "location": bundle.get("position") or "",
            "visible_events": [
                _public_event(event, "JOIN_E_C12_WORLD_EVENT@5e6367")
                for event in visible
            ],
            "visible_speech": speech,
            "visible_actions": actions,
            "encounter_admission": help_public,
            "unperceived_event_count": max(0, len(events) - len(visible)),
            "tool_available": bool(
                (bundle.get("world", {}).get("resources", {})
                 .get("workshop", {}) or {}).get("tool_available")
            ),
            "tools_remaining": bundle.get("tools_remaining"),
            "refusal_present": any(
                item.get("strategy") == "HELP_REFUSE" for item in speech
            ),
            "absence_evidence": (
                "UNPERCEIVED_EVENTS_REMAIN_UNKNOWN"
                if len(events) > len(visible)
                else "NO_UNPERCEIVED_EVENT_IN_THIS_VIEW"
            ),
        }

    def _cp_a5_visible(self) -> dict:
        view = self._cp_view or {}
        remembered = view.get("remembered_events") or []
        events = [
            {
                "event_id": event.get("event_id", ""),
                "kind": event.get("kind", ""),
                "clock": event.get("clock"),
                "location": event.get("location", ""),
                "summary": event.get("summary", ""),
                "body_public": {},
                "source_ref": "CP_A5_ENCOUNTER_VIEW@9137653",
                "perceived_by_user": True,
            }
            for event in remembered
        ]
        speech = [
            {
                "event_id": event["event_id"],
                "speaker": "",
                "clock": event["clock"],
                "text": "",
                "gesture": "",
                "strategy": "",
                "summary": event["summary"],
            }
            for event in events if event["kind"] == "SPEECH"
        ]
        return {
            "viewer_actor": "A",
            "clock": view.get("as_of_clock"),
            "location": view.get("position", ""),
            "visible_events": events,
            "visible_speech": speech,
            "visible_actions": [
                event for event in events if event["kind"] != "SPEECH"
            ],
            "encounter_admission": None,
            "unperceived_event_count": view.get("unperceived_event_count", 0),
            "tool_available": view.get("tool_available"),
            "tools_remaining": None,
            "refusal_present": False,
            "absence_evidence": (
                "UNPERCEIVED_EVENTS_REMAIN_UNKNOWN"
                if view.get("unperceived_event_count", 0)
                else "NO_UNPERCEIVED_EVENT_IN_THIS_VIEW"
            ),
            "known_event_ids": list(view.get("known_event_ids") or []),
        }

    def view(self) -> dict:
        source_view = (
            self._join_e_visible()
            if self.source == "join-e"
            else self._cp_a5_visible()
        )
        announcements = [
            "Mode: portal.",
            "Clock: " + str(source_view["clock"]) + ".",
            "Location: " + str(source_view["location"] or "UNKNOWN") + ".",
            "Visible events: " + str(len(source_view["visible_events"])) + ".",
            "Unperceived events remain unknown: "
            + str(source_view["unperceived_event_count"]) + ".",
            "Exit is always available.",
            "Return requires an actual meeting or channel; typed hold otherwise.",
        ]
        view = {
            "schema": VIEW_SCHEMA,
            "grade": GRADE,
            "native": False,
            "source": self.source,
            "mode": self.mode,
            "accessible": {
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
                    "EXIT": EXIT_LABEL,
                    "RETURN": RETURN_LABEL,
                },
                "text_alternatives": True,
                "color_only_meaning": False,
                "exit_always_visible": True,
                "typed_holds_announced": True,
            },
            "controls": self._controls,
            "exit_control": {
                "label": EXIT_LABEL,
                "always_visible": True,
                "accessible": True,
            },
            "return_control": {
                "label": RETURN_LABEL,
                "available": False,
                "reason": "RETURN_UNSUPPORTED_TYPED_HOLD",
            },
            "hidden_state_held": True,
            "hidden_fields": sorted(self._hidden),
            "accessibility_announcement": announcements,
            "uncertainty": [
                "USER_SAY_DO_ATTEMPT_ADMISSION_MISSING",
                "USER_ATTEND_RECEIPT_MISSING",
                "WAIT_TIME_ADVANCE_RECEIPT_MISSING",
                "PORTAL_EXIT_RETURN_RECEIPT_MISSING",
                "USER_ABSENCE_LIFE_ADVANCE_MISSING",
                "MESSAGE_CHANNEL_ESTABLISHMENT_AND_DELIVERY_MISSING",
            ],
            **source_view,
        }
        return view

    def ask(self, question: str) -> dict:
        if self.source != "cp-a5":
            return self._result(
                "HELD",
                code="USER_ASK_PRODUCER_MISSING",
                attempted=True,
                note="JOIN-E exposes no user question producer at this cut.",
            )
        before = self._store_hash()
        answer = sources.run_cp_a5_command(self.root, "encounter", question)
        after = self._store_hash()
        result = {
            "schema": RESULT_SCHEMA,
            "grade": GRADE,
            "native": False,
            "source": self.source,
            "status": answer.get("status"),
            "code": "CP_A5_READER_ANSWER",
            "attempted": True,
            "performed": False,
            "world_event_created": False,
            "clock_changed": False,
            "actor_response_generated": False,
            "simulated_delivery": False,
            "store_hash_before": before,
            "store_hash_after": after,
            "read_only": answer.get("read_only"),
            "answer": answer.get("answer", ""),
            "evidence_event_ids": list(answer.get("evidence_event_ids") or []),
        }
        self._last_result = result
        return result

    def attend(self, target: str) -> dict:
        view = self.view()
        events = view.get("visible_events") or []
        match = next(
            (event for event in events if event.get("event_id") == target),
            None,
        )
        if match is not None:
            return self._result(
                "OK",
                code="LOCAL_ATTEND_ONLY",
                attempted=True,
                target=match,
                note="Local focus only; no world event or actor knowledge is created.",
            )
        return self._result(
            "UNKNOWN",
            code="UNPERCEIVED_TARGET",
            attempted=True,
            target_ref=target,
            note="UNKNOWN: target is not in the user's lawful perception.",
        )

    def say(self, text: str) -> dict:
        return self._result(
            "HELD",
            code="USER_SAY_DO_ATTEMPT_ADMISSION_MISSING",
            attempted=True,
            input=text,
            note="No user SAY producer; no actor response is invented.",
        )

    def do(self, intent: str) -> dict:
        return self._result(
            "HELD",
            code="USER_SAY_DO_ATTEMPT_ADMISSION_MISSING",
            attempted=True,
            input=intent,
            note="No user DO producer; no world action is invented.",
        )

    def wait(self) -> dict:
        return self._result(
            "HELD",
            code="WAIT_UNSUPPORTED_TYPED_HOLD",
            attempted=True,
            clock_changed=False,
            note="No WAIT producer; scene clock and events are unchanged.",
        )

    def exit(self) -> dict:
        self.mode = "OUTSIDE"
        return self._result(
            "OK",
            code="LOCAL_EXIT_ONLY",
            attempted=True,
            note="Local interface exit only; no actor leave event.",
        )

    def return_(self) -> dict:
        return self._result(
            "HELD",
            code="RETURN_UNSUPPORTED_TYPED_HOLD",
            attempted=True,
            note="Return requires an actual meeting/opportunity/channel.",
        )

    def absence(self) -> dict:
        view = self.view()
        return self._result(
            "UNKNOWN",
            code="USER_ABSENCE_LIFE_ADVANCE_MISSING",
            attempted=True,
            unperceived_event_count=view.get("unperceived_event_count", 0),
            note="Absence is not simulated; only actual persisted events are visible.",
        )

    def status(self) -> dict:
        current = self._store_hash()
        return {
            "schema": "SOROK_WP19_STATUS@1",
            "grade": GRADE,
            "native": False,
            "source": self.source,
            "root": str(self.root),
            "store_path": str(self._store_path),
            "baseline_store_hash": self._baseline_store_hash,
            "current_store_hash": current,
            "store_mutated_since_load": current != self._baseline_store_hash,
            "last_result": self._last_result,
        }


def render_text(view: dict) -> str:
    lines = [
        "Mode: " + str(view.get("mode", "")),
        "Clock: " + str(view.get("clock", "")),
        "Location: " + str(view.get("location", "") or "UNKNOWN"),
    ]
    for event in view.get("visible_events") or []:
        lines.append(
            "- " + str(event.get("kind", "")) + " at "
            + str(event.get("clock", "")) + ": "
            + str(event.get("summary", ""))
        )
    for speech in view.get("visible_speech") or []:
        if speech.get("text"):
            lines.append(
                "- SAY: " + str(speech["text"])
                + (" [" + str(speech.get("gesture")) + "]"
                   if speech.get("gesture") else "")
            )
    for item in view.get("accessibility_announcement") or []:
        lines.append("Announcement: " + str(item))
    lines.append("Exit: " + str(view.get("exit_control", {}).get("label")))
    lines.append("Return: " + str(view.get("return_control", {}).get("reason")))
    return "\n".join(lines)


__all__ = ["EncounterInterface", "GRADE", "VIEW_SCHEMA", "render_text"]
