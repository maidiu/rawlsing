"""Two-event continuation over one persistent S40/S37 person."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from .bootstrap import CUTS, install

install()

from c8_readonly_consumer import C8ReadOnlyConsumer  # noqa: E402
from r30a.first_session import SessionRefusal  # noqa: E402
from s39.model import FULL_RULE  # noqa: E402
from s39.sources import context_records  # noqa: E402
from s40.session import S40GeneratedSession  # noqa: E402

from .bindings import (
    append_event_binding,
    binding_episodes,
    make_continuation_binding,
    make_first_event_binding,
)
from .event import (
    ContinuationProducer,
    S41EventRefusal,
    build_second_occurrence,
    history_record_from_prior,
    world_prerequisites,
)
from .performer import perform_continuation_attempt  # noqa: E402
from .reader import S41ReadRefusal, read_all_events, read_event, read_latest_event

S41_SCHEMA = "SOROK_S41_CONTINUING_PERSON_SESSION@1"


class S41Session(S40GeneratedSession):
    """S40 first event plus one later admitted event, same root/branch/store."""

    @classmethod
    def start(cls, state_root, **kwargs) -> "S41Session":
        session = super().start(state_root, **kwargs)
        try:
            if not isinstance(session, cls):
                raise SessionRefusal("S41_START_CLASS_MISMATCH", type(session).__name__)
            first = make_first_event_binding(session)
            append_event_binding(session, first)
            session.meta.update({
                "s41_schema": S41_SCHEMA,
                "s41_events": [{
                    "event_ordinal": 1,
                    "e1_event_id": first["e1_event_id"],
                    "e1_event_hash": first["e1_event_hash"],
                    "c8_occurrence_id": first["c8"]["occurrence_id"],
                    "binding_hash": first["hash"],
                }],
                "s41_latest_ordinal": 1,
            })
            session._save_join_meta()
            verification = session.verify()
            if not verification.get("ok"):
                raise SessionRefusal("S41_VERIFY_FAILED", str(verification))
            return session
        except Exception:
            session.close()
            raise

    def read_event(self, event_ref: str) -> dict:
        return read_event(self, event_ref)

    def read_events(self) -> list[dict]:
        return read_all_events(self)

    def read_latest(self) -> dict:
        return read_latest_event(self)

    def _first_binding(self) -> dict:
        bindings = binding_episodes(self)
        if not bindings:
            raise S41ReadRefusal("S41_NO_EVENTS")
        return bindings[0]

    def continue_event(
        self,
        *,
        case: Mapping[str, Any],
        source: Mapping[str, Any] | None = None,
        source_records: list[Mapping[str, Any]] | None = None,
        rule=FULL_RULE,
        labels: Mapping[str, Any] | None = None,
        event_time: int | None = None,
        access_witness: Mapping[str, Any] | None = None,
    ) -> dict:
        bindings = binding_episodes(self)
        if any(row.get("event_ordinal", 0) >= 2 for row in bindings):
            raise S41EventRefusal("S41_ALREADY_CONTINUED")
        first = self._first_binding()
        first_read = self.read_event(first["e1_event_id"])
        if first_read.get("status") not in {"OK", "OPEN", "REFUSED"}:
            raise S41EventRefusal("S41_FIRST_EVENT_INVALID")

        first_c8 = first["c8"]
        view = C8ReadOnlyConsumer(str(first_c8["journal_path"])).load()
        first_event = view.get(first_c8["occurrence_id"])
        if not first_event:
            raise S41EventRefusal("S41_FIRST_C8_ABSENT")
        first_payload = dict(first_event.get("payload") or {})

        from s40.bootstrap import install as s40_install

        s40_install()
        import firstclass  # noqa: E402

        second_case = dict(case)
        second_source = firstclass.validate_source(
            source or firstclass.source_from_case(second_case), second_case
        )
        current_world = self.world().snapshot()
        current_state = dict(current_world["actor_state"].get("A", {}))
        if event_time is None:
            event_time = max(self.clock() + 1, int(first["event_time"]) + 1)
        if not isinstance(event_time, int) or event_time <= int(first["event_time"]):
            raise S41EventRefusal("S41_EVENT_TIME_NOT_LATER")
        if event_time <= self.clock():
            raise S41EventRefusal("S41_C12_CLOCK_NOT_LATER")
        second_as_of = event_time + 5
        occurrence, _ = build_second_occurrence(
            self,
            first_binding=first,
            first_payload=first_payload,
            second_source=second_source,
            event_time=event_time,
        )
        history_record = history_record_from_prior(
            self, first_binding=first, as_of=second_as_of
        )
        records = context_records(
            actor_id=self.meta["source_actor_map"]["TEST_ONLY_R31J_A"],
            branch_id=self.branch_id,
            as_of=second_as_of,
            repair_urgent=True,
            avoid_debt=True,
            labels=labels,
        )
        if source_records is not None:
            records = [
                record for record in source_records
                if record.get("predicate") not in {"PRIOR_B_SHARE", "PRIOR_B_REFUSAL"}
            ]
        records.append(history_record)
        world = world_prerequisites(self)

        producer = ContinuationProducer(
            self.state_root / "source",
            case=second_case,
            source=second_source,
            occurrence=occurrence,
            current_tools=current_state.get("tools_remaining", 0),
        )
        try:
            producer.commit_incoming()
            receipt = producer.generate(
                source_records=records,
                rule=rule,
                branch_id=self.branch_id,
                world=world,
                access_witness=access_witness,
            )
            if receipt.get("selection_status") != "UNIQUE_SELECTED":
                producer.close()
                binding = make_continuation_binding(
                    self,
                    producer=producer,
                    generation=receipt,
                    attempt=None,
                    s36=None,
                    source=second_source,
                    first_binding=first,
                    history_source=history_record,
                    world_before=current_world,
                    world_after=self.world().snapshot(),
                    status="OPEN",
                )
                append_event_binding(self, binding)
                self._record_continuation(binding)
                return {
                    "status": "OPEN",
                    "reason": receipt.get("unresolved_reason", ""),
                    "event": self.read_event(binding["e1_event_id"]),
                    "actor_action_appended": False,
                }
            if event_time > self.clock():
                world_now = self.world()
                world_now.advance(event_time)
                self.product._checkpoint(self.branch_id, world_now.clock, world_now)
            e1_identity = {
                "event_id": producer.e1_event["event_id"],
                "event_hash": producer.e1_event["hash"],
                "c8_occurrence_id": producer.out9.occurrence_id,
                "c8_state_digest": producer.out9.readset["state_digest"],
            }
            attempt = perform_continuation_attempt(
                self,
                receipt["attempt_request"],
                generation_receipt=receipt,
                e1_identity=e1_identity,
            )
            producer.finalize_s36(attempt_result=attempt)
            s36 = dict(producer.s36_binding or {})
            producer.close()
            binding = make_continuation_binding(
                self,
                producer=producer,
                generation=receipt,
                attempt=attempt,
                s36=s36,
                source=second_source,
                first_binding=first,
                history_source=history_record,
                world_before=current_world,
                world_after=self.world().snapshot(),
                status=attempt.get("attempt_status", ""),
            )
            append_event_binding(self, binding)
            self._record_continuation(binding)
            return {
                "status": "OK",
                "event": self.read_event(binding["e1_event_id"]),
                "actor_action_appended": bool(attempt.get("performed")),
            }
        except Exception as exc:
            try:
                producer.close()
            except Exception:
                pass
            code = getattr(exc, "code", type(exc).__name__)
            try:
                binding = make_continuation_binding(
                    self,
                    producer=producer,
                    generation=getattr(producer, "generation_receipt", None) or {},
                    attempt=None,
                    s36=None,
                    source=second_source,
                    first_binding=first,
                    history_source=history_record,
                    world_before=current_world,
                    world_after=self.world().snapshot(),
                    status="REFUSED",
                )
                if binding.get("generation_hash"):
                    append_event_binding(self, binding)
                    self._record_continuation(binding)
            except Exception:
                pass
            raise S41EventRefusal("S41_CONTINUATION_REFUSED", str(code)) from exc

    def _record_continuation(self, binding: Mapping[str, Any]) -> None:
        events = list(self.meta.get("s41_events") or [])
        events.append({
            "event_ordinal": binding["event_ordinal"],
            "e1_event_id": binding["e1_event_id"],
            "e1_event_hash": binding["e1_event_hash"],
            "c8_occurrence_id": binding["c8"]["occurrence_id"],
            "binding_hash": binding["hash"],
            "status": binding.get("status"),
        })
        self.meta["s41_events"] = events
        self.meta["s41_latest_ordinal"] = binding["event_ordinal"]
        self._save_join_meta()

    def verify(self) -> dict:
        result = super().verify()
        try:
            events = self.read_events()
            summaries = [{
                "event_ordinal": row["event_ordinal"],
                "e1_event_id": row["e1_event_id"],
                "e1_event_hash": row["e1_event_hash"],
                "status": row["status"],
                "source_operation": row.get("source_operation"),
                "selected_option": row.get("selected_option"),
                "attempt_status": row.get("attempt_status"),
                "target_proposals": row.get("target_proposals", []),
            } for row in events]
            events_ok = True
        except (S41ReadRefusal, KeyError, OSError, ValueError) as exc:
            summaries = [{"status": "REFUSED", "code": str(exc)}]
            events_ok = False
        result["s41_events"] = summaries
        result["ok"] = bool(result.get("ok")) and events_ok
        return result

    def status(self) -> dict:
        result = super().status()
        try:
            events = self.read_events()
            summaries = [{
                "event_ordinal": row["event_ordinal"],
                "e1_event_id": row["e1_event_id"],
                "e1_event_hash": row["e1_event_hash"],
                "status": row["status"],
                "source_operation": row.get("source_operation"),
                "selected_option": row.get("selected_option"),
                "attempt_status": row.get("attempt_status"),
                "performed": row.get("performed"),
                "language_status": (row.get("language") or {}).get("status", ""),
                "target_proposals": row.get("target_proposals", []),
            } for row in events]
            latest = self.read_latest()
        except (S41ReadRefusal, KeyError, OSError, ValueError) as exc:
            summaries = [{"status": "REFUSED", "code": str(exc)}]
            latest = None
        result.update({
            "schema": S41_SCHEMA,
            "s40_schema": "SOROK_S40_GENERATED_NATIVE_SPEECH_SESSION@1",
            "s41_events": summaries,
            "s41_latest": latest,
        })
        return result


__all__ = ["S41_SCHEMA", "S41Session"]
