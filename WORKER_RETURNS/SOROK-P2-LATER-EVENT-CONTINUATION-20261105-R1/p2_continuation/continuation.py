"""Additive S41-S43 later-event continuation over the shipped S45/S47 person."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .bootstrap import load

SCHEMA = "SOROK_P2_LATER_EVENT_CONTINUATION@1"
GRADE = "TEST_ONLY_SOURCEFREE_P2_LATER_EVENT_CONTINUATION_NOT_NATIVE"


def _source_summary(source: Mapping[str, Any] | None) -> dict:
    source = source or {}
    content = source.get("content") or {}
    return {
        "source_ref": source.get("source_ref", ""),
        "source_hash": source.get("source_hash", ""),
        "source_class": source.get("source_class", ""),
        "access": content.get("access", ""),
        "coverage": list(content.get("coverage") or []),
        "currentness": content.get("currentness", ""),
        "interval_state_id": content.get("interval_state_id", ""),
    }


def _c9_summary(read: Mapping[str, Any]) -> dict:
    return {
        "event_ref": read.get("event_ref", ""),
        "selected_event_ref": read.get("selected_event_ref", ""),
        "response_status": read.get("response_status", ""),
        "s47_source_ref": read.get("s47_source_ref", ""),
        "s47_source_hash": read.get("s47_source_hash", ""),
        "s47_source_in_readset": read.get("s47_source_in_readset"),
        "s47_source_currentness": read.get("s47_source_currentness", ""),
        "s47_source_coverage": list(read.get("s47_source_coverage") or []),
        "current_source_ref": read.get("current_source_ref", ""),
        "current_source_hash": read.get("current_source_hash", ""),
        "objective_material_eligible": read.get("objective_material_eligible"),
        "objective_material_refs": list(read.get("objective_material_refs") or []),
        "target_branch": read.get("target_branch", ""),
        "target_reason": read.get("target_reason", ""),
        "target_proposals": list(read.get("target_proposals") or []),
        "readset_refs": list(read.get("readset_refs") or []),
        "present_condition_revoked": read.get("present_condition_revoked"),
        "historical_condition_revoked": read.get("historical_condition_revoked"),
    }


def _s43_summary(read: Mapping[str, Any]) -> dict:
    s43 = read.get("s43") or {}
    language = read.get("language") or {}
    return {
        "status": read.get("status", ""),
        "attempt_status": read.get("attempt_status", ""),
        "performed": read.get("performed"),
        "action_event_kind": read.get("action_event_kind", ""),
        "repertoire_id": s43.get("repertoire_id", ""),
        "repertoire_hash": s43.get("repertoire_hash", ""),
        "currently_available": s43.get("currently_available"),
        "selected_relation_ids": list(s43.get("selected_relation_ids") or []),
        "contrary_relation_ids": list(s43.get("contrary_relation_ids") or []),
        "language_status": language.get("status", ""),
        "native_text": language.get("native_text", ""),
        "translation_text": language.get("translation_text", ""),
        "source_event_id": language.get("source_event_id", ""),
        "plan_hash": language.get("plan_hash", ""),
        "private_generation_sources_in_plan": s43.get(
            "private_generation_sources_in_plan"
        ),
    }


def _history_ids(read: Mapping[str, Any]) -> list[str]:
    return [
        row.get("e1_event_id", "")
        for row in (read.get("history_refs") or [])
        if isinstance(row, Mapping)
    ]


def _callables(session, adapter) -> dict:
    return {
        "later_event_producer": getattr(
            getattr(session.admit_event, "__func__", None), "__qualname__", ""
        ),
        "later_event_reader": getattr(
            getattr(session.read_event, "__func__", None), "__qualname__", ""
        ),
        "later_event_reader_delegate": "s42.reader.read_event",
        "source_bound_expression_reader": getattr(
            getattr(session.read_s43_event, "__func__", None), "__qualname__", ""
        ),
        "event_local_c9_reader": getattr(
            getattr(session.read_c9_conditioning, "__func__", None), "__qualname__", ""
        ),
        "projected_say": getattr(
            getattr(adapter.say, "__func__", None), "__qualname__", ""
        ),
        "projected_do_help": getattr(
            getattr(adapter.do_help, "__func__", None), "__qualname__", ""
        ),
        "projected_attend": getattr(
            getattr(adapter.attend, "__func__", None), "__qualname__", ""
        ),
        "s41_continuation_producer": "s41.event.ContinuationProducer.generate",
        "s41_continuation_performer": "s41.performer.perform_continuation_attempt",
        "s42_history_builder": "s42.event.make_history_records",
        "s42_occurrence_builder": "s42.event.build_ongoing_occurrence",
    }


class P2Continuation:
    """One same-root later-event continuation; interval is an input, not duplicated."""

    def __init__(self, session) -> None:
        deps = load()
        self.session = session
        self.adapter = deps["S45Projection"](session)
        self.case = deps["case_for"](True)
        self.source = deps["source_for"](self.case)

    @classmethod
    def start(cls, state_root, *, seed: str = "01" * 32, **kwargs) -> "P2Continuation":
        deps = load()
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
        return cls(session)

    @classmethod
    def open(cls, state_root, **kwargs) -> "P2Continuation":
        deps = load()
        return cls(deps["S47Session"].open(state_root, **kwargs))

    def produce_input_interval(self, mode: str = "ACTUAL", span: int = 4) -> dict:
        deps = load()
        start = self.session.clock()
        produced = self.session.produce_interval(
            deps["make_domain"](mode=mode, start=start, end=start + span)
        )
        source = self.session.c9_interval_source()
        return {
            "mode": mode,
            "start": start,
            "end": start + span,
            "state_id": produced.get("state_id", ""),
            "status": produced.get("status", ""),
            "coverage": list(produced.get("coverage") or []),
            "material_after_interval": self.session.world().actor_state["A"].get(
                "material_remaining"
            ),
            "source": _source_summary(source),
            "actual_daily_events_invented": produced.get("actual_daily_events_invented"),
            "actor_knowledge_inferred": produced.get("actor_knowledge_inferred"),
            "psychology_state_written": produced.get("psychology_state_written"),
        }

    def admit_later_event(
        self,
        history_refs: tuple[str, ...] = (),
        *,
        event_time: int | None = None,
        language_context: Mapping[str, Any] | None = None,
    ) -> dict:
        if event_time is None:
            event_time = self.session.clock() + 1
        kwargs = {}
        if language_context is not None:
            kwargs["language_context"] = dict(language_context)
        result = self.session.admit_event(
            case=self.case,
            source=self.source,
            history_event_refs=tuple(history_refs),
            event_time=event_time,
            **kwargs,
        )
        event = result.get("event") or {}
        event_ref = event.get("e1_event_id", "")
        read = self.session.read_event(event_ref)
        s43 = self.session.read_s43_event(event_ref)
        c9 = self.session.read_c9_conditioning(event_ref)
        return {
            "status": result.get("status", ""),
            "reason": result.get("reason", ""),
            "event_ref": event_ref,
            "event_hash": event.get("e1_event_hash", ""),
            "event_ordinal": event.get("event_ordinal"),
            "selected_option": event.get("selected_option", ""),
            "attempt_status": event.get("attempt_status", ""),
            "performed": event.get("performed"),
            "actor_action_appended": result.get("actor_action_appended"),
            "history_refs": _history_ids(read),
            "s43": _s43_summary(s43),
            "c9": _c9_summary(c9),
        }

    def read_later_event(self, event_ref: str) -> dict:
        read = self.session.read_event(event_ref)
        s43 = self.session.read_s43_event(event_ref)
        c9 = self.session.read_c9_conditioning(event_ref)
        return {
            "event_ref": event_ref,
            "event_hash": read.get("e1_event_hash", ""),
            "status": read.get("status", ""),
            "performed": read.get("performed"),
            "history_refs": _history_ids(read),
            "s43": _s43_summary(s43),
            "c9": _c9_summary(c9),
        }

    def project_say(self, text: str) -> dict:
        return self.adapter.say(text)

    def project_do_help(self) -> dict:
        return self.adapter.do_help()

    def project_attend(self) -> dict:
        return self.adapter.attend()

    def view(self) -> dict:
        return self.adapter.view()

    def verify(self) -> dict:
        return self.session.verify()

    def revoke_interval_condition(self, state_id: str, *, reason: str) -> dict:
        return self.session.revoke_interval_condition(state_id, reason=reason)

    def restore_interval_condition(self, state_id: str, *, reason: str) -> dict:
        return self.session.restore_interval_condition(state_id, reason=reason)

    def close(self) -> None:
        self.adapter.close()

    def __enter__(self) -> "P2Continuation":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def cold_read(state_root, event_refs: tuple[str, ...]) -> dict:
    deps = load()
    session = deps["S47Session"].open(state_root)
    try:
        events = {}
        for event_ref in event_refs:
            read = session.read_event(event_ref)
            s43 = session.read_s43_event(event_ref)
            c9 = session.read_c9_conditioning(event_ref)
            events[event_ref] = {
                "event_ref": event_ref,
                "event_hash": read.get("e1_event_hash", ""),
                "status": read.get("status", ""),
                "history_refs": _history_ids(read),
                "s43": _s43_summary(s43),
                "c9": _c9_summary(c9),
            }
        return {
            "root_hash": session.read_root().get("root_hash", ""),
            "event_count": len(session.read_events()),
            "encounter_count": len(session.read_encounters()),
            "verify_ok": bool(session.verify().get("ok")),
            "events": events,
        }
    finally:
        session.close()


def _positive_checks(report: Mapping[str, Any]) -> dict:
    interval = report["interval"]
    e2 = report["later_event_2"]
    e3 = report["later_event_3"]
    e2_after = report["earlier_event_after_later"]
    said = report["say"]
    helped = report["do_help"]
    attended = report["attend"]
    cold = report["cold"]
    e2_c9 = e2["c9"]
    e3_c9 = e3["c9"]
    e2_cold = cold["events"].get(e2["event_ref"], {})
    e3_cold = cold["events"].get(e3["event_ref"], {})
    e2_s43 = e2["s43"]
    return {
        "interval_actual_consumes_material": interval["status"] in {
            "PARTIAL", "REALIZED"
        } and interval["source"]["source_hash"] != "" and report[
            "material_after_interval"
        ] == 0,
        "e2_real_later_event": e2["status"] == "OK" and e2["performed"] is True,
        "e3_real_later_event": e3["status"] == "OK" and e3["performed"] is True,
        "e3_history_includes_e2": e2["event_ref"] in e3["history_refs"],
        "e2_source_in_c9_readset": e2_c9["s47_source_in_readset"] is True,
        "e2_c9_uses_interval_source": e2_c9["s47_source_hash"]
        == interval["source"]["source_hash"],
        "e3_c9_uses_interval_source": e3_c9["s47_source_hash"]
        == interval["source"]["source_hash"],
        "e2_source_bound_expression": e2_s43["language_status"] == "ACCEPTED"
        and e2_s43["repertoire_hash"] != ""
        and e2_s43["currently_available"] is True,
        "earlier_event_identity_preserved_after_later": e2_after["event_hash"]
        == e2["event_hash"]
        and e2_after["c9"]["s47_source_hash"] == e2_c9["s47_source_hash"]
        and e2_after["c9"]["s47_source_ref"] == e2_c9["s47_source_ref"],
        "say_attempt_not_performance": said.get("attempted") is True
        and said.get("performed") is False,
        "do_help_attempt_not_performance": helped.get("attempted") is True
        and helped.get("performed") is False,
        "do_help_refused_by_earlier_activity": helped.get("status") == "REFUSED"
        and helped.get("refusal") is True
        and (helped.get("actor_response") or {}).get("strategy") == "HELP_REFUSE"
        and (helped.get("actor_response") or {}).get("performed") is False,
        "attend_presentation_only": attended.get("status") == "NO_CHANGE"
        and attended.get("world_event_created") is False
        and attended.get("clock_changed") is False
        and attended.get("performed") is False,
        "verify_ok": report["verify_ok"] is True,
        "cold_same_root": cold["root_hash"] == report["root_hash"],
        "cold_e2_source_same": e2_cold.get("c9", {}).get("s47_source_hash")
        == e2_c9["s47_source_hash"],
        "cold_e3_source_same": e3_cold.get("c9", {}).get("s47_source_hash")
        == e3_c9["s47_source_hash"],
        "cold_s43_same": e2_cold.get("s43", {}).get("repertoire_hash")
        == e2_s43["repertoire_hash"],
        "cold_verify_ok": cold["verify_ok"] is True,
    }


def run_positive(state_root, *, seed: str = "01" * 32) -> dict:
    continuation = P2Continuation.start(Path(state_root), seed=seed)
    try:
        callables = _callables(continuation.session, continuation.adapter)
        interval = continuation.produce_input_interval("ACTUAL", 4)
        first_ref = continuation.session.read_events()[0]["e1_event_id"]
        e2 = continuation.admit_later_event((first_ref,))
        e3 = continuation.admit_later_event((first_ref, e2["event_ref"]))
        e2_after = continuation.read_later_event(e2["event_ref"])
        said = continuation.project_say("Can I help?")
        helped = continuation.project_do_help()
        attended = continuation.project_attend()
        view = continuation.view()
        verify = continuation.verify()
        root_hash = continuation.session.read_root()["root_hash"]
        event_count = len(continuation.session.read_events())
        encounter_count = len(continuation.session.read_encounters())
    finally:
        continuation.close()

    cold = cold_read(state_root, (e2["event_ref"], e3["event_ref"]))
    report = {
        "schema": SCHEMA,
        "grade": GRADE,
        "native": False,
        "scenario": "ACTUAL_LATER_EVENT_POSITIVE",
        "state_root": str(Path(state_root)),
        "root_hash": root_hash,
        "event_count": event_count,
        "encounter_count": encounter_count,
        "callables": callables,
        "interval": interval,
        "interval_source_ref": interval["source"]["source_ref"],
        "interval_source_hash": interval["source"]["source_hash"],
        "material_after_interval": interval["material_after_interval"],
        "first_event_ref": first_ref,
        "later_event_2": e2,
        "later_event_3": e3,
        "earlier_event_after_later": e2_after,
        "say": said,
        "do_help": helped,
        "attend": attended,
        "view": view,
        "verify_ok": bool(verify.get("ok")),
        "cold": cold,
    }
    report["checks"] = _positive_checks(report)
    report["ok"] = all(report["checks"].values())
    return report


def run_scheduled(state_root, *, seed: str = "01" * 32) -> dict:
    continuation = P2Continuation.start(Path(state_root), seed=seed)
    try:
        callables = _callables(continuation.session, continuation.adapter)
        interval = continuation.produce_input_interval("SCHEDULED_ONLY", 4)
        first_ref = continuation.session.read_events()[0]["e1_event_id"]
        e2 = continuation.admit_later_event((first_ref,))
        e3 = continuation.admit_later_event((first_ref, e2["event_ref"]))
        helped = continuation.project_do_help()
        view = continuation.view()
        verify = continuation.verify()
        root_hash = continuation.session.read_root()["root_hash"]
    finally:
        continuation.close()

    checks = {
        "interval_not_performed": interval["status"] == "NOT_PERFORMED",
        "material_remains": interval["material_after_interval"] == 1,
        "later_events_admitted": e2["status"] == "OK" and e3["status"] == "OK",
        "e3_history_includes_e2": e2["event_ref"] in e3["history_refs"],
        "c9_material_eligible": e2["c9"]["objective_material_eligible"] is True,
        "do_help_attempt_not_performance": helped.get("attempted") is True
        and helped.get("performed") is False,
        "do_help_accepted_by_earlier_mode": helped.get("status") == "OK"
        and helped.get("refusal") is False
        and (helped.get("actor_response") or {}).get("strategy") == "HELP_ACCEPT"
        and (helped.get("actor_response") or {}).get("performed") is True,
        "verify_ok": bool(verify.get("ok")),
    }
    return {
        "schema": SCHEMA,
        "grade": GRADE,
        "native": False,
        "scenario": "SCHEDULED_LATER_EVENT_CONTROL",
        "state_root": str(Path(state_root)),
        "root_hash": root_hash,
        "callables": callables,
        "interval": interval,
        "material_after_interval": interval["material_after_interval"],
        "first_event_ref": first_ref,
        "later_event_2": e2,
        "later_event_3": e3,
        "do_help": helped,
        "view": view,
        "verify_ok": bool(verify.get("ok")),
        "checks": checks,
        "ok": all(checks.values()),
    }


def run_cut_restore(state_root, *, seed: str = "01" * 32) -> dict:
    continuation = P2Continuation.start(Path(state_root), seed=seed)
    try:
        callables = _callables(continuation.session, continuation.adapter)
        interval = continuation.produce_input_interval("ACTUAL", 4)
        first_ref = continuation.session.read_events()[0]["e1_event_id"]
        before_source = continuation.session.c9_interval_source()
        events_before_cut = len(continuation.session.read_events())
        continuation.revoke_interval_condition(
            interval["state_id"], reason="TEST_ONLY_P2_CUT"
        )
        cut_code = ""
        try:
            continuation.admit_later_event((first_ref,))
        except Exception as exc:
            cut_code = getattr(exc, "code", type(exc).__name__)
        events_after_cut = len(continuation.session.read_events())
        continuation.restore_interval_condition(
            interval["state_id"], reason="TEST_ONLY_P2_RESTORE"
        )
        restored_source = continuation.session.c9_interval_source()
        admitted = continuation.admit_later_event((first_ref,))
        verify = continuation.verify()
        root_hash = continuation.session.read_root()["root_hash"]
    finally:
        continuation.close()

    cold = cold_read(state_root, (admitted["event_ref"],))
    cold_event = cold["events"].get(admitted["event_ref"], {})
    checks = {
        "cut_refused": cut_code == "S46_INTERVAL_CONDITION_REVOKED",
        "cut_appended_no_later_event": events_after_cut == events_before_cut,
        "restored_source_same": restored_source.get("source_hash")
        == before_source.get("source_hash"),
        "restored_admission_ok": admitted["status"] == "OK",
        "restored_c9_uses_source": admitted["c9"]["s47_source_hash"]
        == before_source.get("source_hash")
        and admitted["c9"]["s47_source_in_readset"] is True,
        "verify_ok": bool(verify.get("ok")),
        "cold_same_root": cold["root_hash"] == root_hash,
        "cold_source_same": cold_event.get("c9", {}).get("s47_source_hash")
        == before_source.get("source_hash"),
        "cold_verify_ok": cold["verify_ok"] is True,
    }
    return {
        "schema": SCHEMA,
        "grade": GRADE,
        "native": False,
        "scenario": "INTERVAL_CONDITION_CUT_RESTORE",
        "state_root": str(Path(state_root)),
        "root_hash": root_hash,
        "callables": callables,
        "interval": interval,
        "before_source": _source_summary(before_source),
        "restored_source": _source_summary(restored_source),
        "cut_code": cut_code,
        "events_before_cut": events_before_cut,
        "events_after_cut": events_after_cut,
        "admitted": admitted,
        "verify_ok": bool(verify.get("ok")),
        "cold": cold,
        "checks": checks,
        "ok": all(checks.values()),
    }


__all__ = [
    "GRADE",
    "P2Continuation",
    "SCHEMA",
    "cold_read",
    "run_cut_restore",
    "run_positive",
    "run_scheduled",
]
