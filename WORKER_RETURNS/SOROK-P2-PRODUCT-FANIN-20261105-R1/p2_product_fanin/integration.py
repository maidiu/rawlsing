"""Unified P2 throughline: local access boundary, interval input, later events."""
from __future__ import annotations

from typing import Any, Mapping

from . import runtime

SCHEMA = "SOROK_P2_PRODUCT_FANIN@1"
OPPORTUNITY_SCHEMA = "SOROK_P2_PRODUCT_FANIN_OPPORTUNITY@1"
VERIFY_SCHEMA = "SOROK_P2_PRODUCT_FANIN_VERIFY@1"
GRADE = "TEST_ONLY_SOURCEFREE_P2_PRODUCT_FANIN_NOT_NATIVE"


def apply_explicit_interval(state, interval_input) -> dict:
    deps = runtime.load()
    result = deps["interval_apply"](
        state, interval_input, base_root=deps["WORKSPACE"]
    )
    result["do_help_executed"] = False
    result["general_autonomous_absence_life"] = False
    return result


class P2ProductFanin:
    def __init__(self, deps: dict, session, lifecycle, continuation) -> None:
        self.deps = deps
        self.session = session
        self.lifecycle = lifecycle
        self.continuation = continuation

    @classmethod
    def start(cls, state_root, *, seed: str = "01" * 32, **kwargs) -> "P2ProductFanin":
        deps = runtime.load()
        case = kwargs.pop("case", deps["case_for"](True))
        source = kwargs.pop("source", deps["source_for"](case))
        session = deps["S47Session"].start(
            state_root,
            bundle=deps["root_bundle"](seed),
            case=case,
            source=source,
            language_context={"milieu_id": "workshop"},
            **kwargs,
        )
        return cls._wrap(deps, session, state_root)

    @classmethod
    def open(cls, state_root, **kwargs) -> "P2ProductFanin":
        deps = runtime.load()
        session = deps["S47Session"].open(state_root, **kwargs)
        return cls._wrap(deps, session, state_root)

    @classmethod
    def _wrap(cls, deps: dict, session, state_root) -> "P2ProductFanin":
        try:
            projection = deps["S45Projection"](session)
            lifecycle = deps["LifecycleEncounter"]._wrap(projection, state_root)
            continuation = deps["P2Continuation"](session)
            return cls(deps, session, lifecycle, continuation)
        except Exception:
            session.close()
            raise

    @property
    def root_hash(self) -> str:
        return self.lifecycle.root_hash

    @property
    def local_mode(self) -> str:
        return self.lifecycle.mode

    def view(self) -> dict:
        return self.lifecycle.view()

    def say(self, text: str) -> dict:
        return self.lifecycle.say(text)

    def do_help(self) -> dict:
        return self.lifecycle.do_help()

    def attend(self) -> dict:
        return self.lifecycle.attend()

    def exit(self) -> dict:
        return self.lifecycle.exit()

    def return_(self) -> dict:
        return self.lifecycle.return_()

    def status(self) -> dict:
        return self.lifecycle.status()

    def local_state(self) -> dict:
        return self.lifecycle.local_state()

    def current_interval_state(self) -> dict | None:
        return self.session.current_interval_state()

    def revoke_interval(self, state_id: str, *, reason: str) -> dict:
        return self.session.revoke_interval_condition(state_id, reason=reason)

    def restore_interval(self, state_id: str, *, reason: str) -> dict:
        return self.session.restore_interval_condition(state_id, reason=reason)

    def admit_later_event(self, history_refs: tuple[str, ...] = ()) -> dict:
        if not history_refs:
            history_refs = (self.session.read_events()[0]["e1_event_id"],)
        try:
            return self.continuation.admit_later_event(tuple(history_refs))
        except self.deps["S46Refusal"] as exc:
            return {
                "schema": "SOROK_P2_PRODUCT_FANIN_ADMISSION@1",
                "grade": GRADE,
                "native": False,
                "status": "REFUSED",
                "code": exc.code,
                "event_ref": "",
                "event_hash": "",
                "history_refs": [],
                "s43": {},
                "c9": {},
            }

    def read_later_event(self, event_ref: str) -> dict:
        return self.continuation.read_later_event(event_ref)

    def public_opportunity(self, later_event: Mapping[str, Any]) -> dict:
        event = later_event or {}
        c9 = event.get("c9") or {}
        s43 = event.get("s43") or {}
        return {
            "schema": OPPORTUNITY_SCHEMA,
            "grade": GRADE,
            "native": False,
            "local_mode": self.local_mode,
            "event_present": bool(event.get("event_ref")),
            "event_ordinal": event.get("event_ordinal"),
            "event_status": event.get("status", ""),
            "code": event.get("code", ""),
            "reason": event.get("reason", ""),
            "performed": event.get("performed"),
            "c9_material_eligible": c9.get("objective_material_eligible"),
            "c9_source_in_readset": c9.get("s47_source_in_readset"),
            "language_status": s43.get("language_status", ""),
            "native_text": s43.get("native_text", ""),
            "translation_text": s43.get("translation_text", ""),
            "repertoire_id": s43.get("repertoire_id", ""),
            "do_help_executed": False,
            "user_attempt": False,
            "note": (
                "Opportunity observation only; no DO_HELP attempt was executed. "
                "Use do-help explicitly for a user attempt."
            ),
            "view": self.view(),
        }

    def verify_public(self) -> dict:
        result = self.session.verify()
        intervals = self.session.read_interval_states()
        return {
            "schema": VERIFY_SCHEMA,
            "grade": GRADE,
            "native": False,
            "ok": bool(result.get("ok")),
            "event_count": len(self.session.read_events()),
            "encounter_count": len(self.session.read_encounters()),
            "interval_count": len(intervals),
            "current_interval_status": (
                intervals[-1].get("status") if intervals else ""
            ),
            "current_interval_currentness": (
                intervals[-1].get("currentness") if intervals else ""
            ),
        }

    def close(self) -> None:
        self.lifecycle.close()

    def __enter__(self) -> "P2ProductFanin":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


__all__ = [
    "GRADE",
    "OPPORTUNITY_SCHEMA",
    "P2ProductFanin",
    "SCHEMA",
    "VERIFY_SCHEMA",
    "apply_explicit_interval",
]
