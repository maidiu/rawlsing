"""Reusable ongoing admitted-event session over one continuing person."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .bootstrap import CUTS, install

install()

from c8_readonly_consumer import C8ReadOnlyConsumer  # noqa: E402
from r30a.first_session import SessionRefusal  # noqa: E402
from s41.bindings import binding_episodes as s41_binding_episodes  # noqa: E402
from s41.event import (  # noqa: E402
    ContinuationProducer,
    S41EventRefusal,
    world_prerequisites,
)
from s41.history import (  # noqa: E402
    S41HistoryRefusal,
    validate_generation_readset,
    validate_history_source,
)
from s41.performer import perform_continuation_attempt  # noqa: E402
from s41.session import S41Session  # noqa: E402
from s39.model import FULL_RULE  # noqa: E402
from s39.sources import context_records  # noqa: E402

from .bindings import append_event_binding, binding_episodes, make_event_binding
from .event import build_ongoing_occurrence, make_history_records
from .reader import (
    S42ReadRefusal,
    read_all_events,
    read_event,
    read_latest_event,
    validate_predecessor_chain,
)

S42_SCHEMA = "SOROK_S42_ONGOING_EVENT_SESSION@1"


class S42Session(S41Session):
    """S41 first event plus an unbounded reusable later-event API."""

    @classmethod
    def start(cls, state_root, **kwargs) -> "S42Session":
        session = super().start(state_root, **kwargs)
        try:
            if not isinstance(session, cls):
                raise SessionRefusal("S42_START_CLASS_MISMATCH", type(session).__name__)
            session.meta.update({
                "s42_schema": S42_SCHEMA,
                "s42_events": [],
                "s42_latest_ordinal": 1,
            })
            session._save_join_meta()
            verification = session.verify()
            if not verification.get("ok"):
                raise SessionRefusal("S42_VERIFY_FAILED", str(verification))
            return session
        except Exception:
            session.close()
            raise

    def _all_bindings(self) -> list[dict]:
        rows = list(s41_binding_episodes(self)) + list(binding_episodes(self))
        rows.sort(key=lambda item: (item.get("event_ordinal", 0), item.get("event_time", 0)))
        return rows

    def continue_event(self, *args, **kwargs):
        raise S41EventRefusal(
            "S42_USE_ADMIT_EVENT",
            "S41 fixed continuation is not the S42 ongoing API",
        )

    def _world_prerequisites(self) -> dict:
        return world_prerequisites(self)

    def _extra_conditioning_sources(self) -> list[dict]:
        return []

    def _validate_admit_source_chain(self, source: Mapping[str, Any],
                                     case: Mapping[str, Any],
                                     event_time: int) -> None:
        return None

    def read_event(self, event_ref: str) -> dict:
        return read_event(self, event_ref)

    def read_events(self) -> list[dict]:
        return read_all_events(self)

    def read_latest(self) -> dict:
        return read_latest_event(self)

    def admit_event(
        self,
        *,
        case: Mapping[str, Any],
        source: Mapping[str, Any] | None = None,
        history_event_refs: tuple[str, ...] = (),
        source_records: list[Mapping[str, Any]] | None = None,
        rule=FULL_RULE,
        labels: Mapping[str, Any] | None = None,
        event_time: int | None = None,
        access_witness: Mapping[str, Any] | None = None,
    ) -> dict:
        bindings = self._all_bindings()
        validate_predecessor_chain(self, bindings)
        predecessor = bindings[-1]
        ordinal = max(int(row["event_ordinal"]) for row in bindings) + 1
        if event_time is None:
            event_time = max(self.clock() + 1, int(predecessor["event_time"]) + 1)
        if not isinstance(event_time, int) or event_time <= int(predecessor["event_time"]):
            raise S41EventRefusal("S42_EVENT_TIME_NOT_LATER")
        if event_time <= self.clock():
            raise S41EventRefusal("S42_C12_CLOCK_NOT_LATER")

        from s40.bootstrap import install as s40_install

        s40_install()
        import firstclass  # noqa: E402

        second_case = dict(case)
        raw_source = source or firstclass.source_from_case(second_case)
        second_source = firstclass.validate_source(raw_source, second_case)
        second_source.update({
            key: value for key, value in dict(raw_source).items()
            if str(key).startswith("s49_")
        })
        self._validate_admit_source_chain(second_source, second_case, event_time)
        # Reject an exact incoming source identity replayed at the same derived clock.
        for row in bindings:
            if (
                row.get("source", {}).get("b_event_hash") == second_source["b_event_hash"]
                and int(row.get("event_time", -1)) == int(event_time)
            ):
                raise S41EventRefusal("S42_INCOMING_SOURCE_REPLAY")

        history_bindings = []
        seen = set()
        last_ordinal = -1
        last_time = -1
        for ref in history_event_refs:
            prior = next(
                (
                    row for row in bindings
                    if row.get("e1_event_id") == ref or row.get("e1_event_hash") == ref
                ),
                None,
            )
            if prior is None:
                raise S41EventRefusal("S42_HISTORY_REF_MISSING", str(ref))
            if prior["e1_event_id"] in seen:
                raise S41EventRefusal("S42_HISTORY_REF_DUPLICATE")
            seen.add(prior["e1_event_id"])
            if int(prior["event_ordinal"]) >= ordinal or int(prior["event_time"]) >= event_time:
                raise S41EventRefusal("S42_HISTORY_REF_ORDER_INVALID")
            if int(prior["event_ordinal"]) <= last_ordinal or int(prior["event_time"]) <= last_time:
                raise S41EventRefusal("S42_HISTORY_INPUT_OUT_OF_ORDER")
            last_ordinal = int(prior["event_ordinal"])
            last_time = int(prior["event_time"])
            if prior.get("branch_id") != self.branch_id:
                raise S41EventRefusal("S42_HISTORY_BRANCH_MISMATCH")
            if prior.get("actor_id") != self.meta["source_actor_map"]["TEST_ONLY_R31J_A"]:
                raise S41EventRefusal("S42_HISTORY_ACTOR_MISMATCH")
            history_bindings.append(prior)

        second_as_of = event_time + 5
        history_records = make_history_records(self, history_bindings, second_as_of)
        for record, prior in zip(history_records, history_bindings):
            try:
                validate_history_source(
                    self, record, prior,
                    branch_id=self.branch_id, as_of=second_as_of,
                )
            except S41HistoryRefusal as exc:
                raise S41EventRefusal("S42_HISTORY_BINDING_INVALID", exc.code) from exc

        first_binding = bindings[0]
        first_event = C8ReadOnlyConsumer(
            first_binding["c8"]["journal_path"]
        ).load().get(first_binding["c8"]["occurrence_id"])
        if not first_event:
            raise S41EventRefusal("S42_FIRST_C8_ABSENT")
        occurrence = build_ongoing_occurrence(
            self,
            first_binding=first_binding,
            first_payload=first_event["payload"],
            predecessor=predecessor,
            history_bindings=history_bindings,
            second_source=second_source,
            ordinal=ordinal,
            event_time=event_time,
        )
        current_world = self.world().snapshot()
        world = self._world_prerequisites()
        records = context_records(
            actor_id=self.meta["source_actor_map"]["TEST_ONLY_R31J_A"],
            branch_id=self.branch_id,
            as_of=second_as_of,
            repair_urgent=True,
            avoid_debt=True,
            labels=labels,
        ) + history_records
        if source_records is not None:
            contexts = [
                row for row in source_records
                if row.get("source_class") != "HISTORICAL_EPISODE"
            ]
            records = contexts + history_records

        producer = ContinuationProducer(
            self.state_root / "source",
            case=second_case,
            source=second_source,
            occurrence=occurrence,
            current_tools=self.world().actor_state["A"].get("tools_remaining", 0),
        )
        producer.extra_conditioning_sources = self._extra_conditioning_sources()
        try:
            producer.commit_incoming()
            receipt = producer.generate(
                source_records=records,
                rule=rule,
                branch_id=self.branch_id,
                world=world,
                access_witness=access_witness,
            )
            declared = {row["source_ref"] for row in history_records}
            historical = [
                row for row in records
                if row.get("source_class") == "HISTORICAL_EPISODE"
            ]
            if {row.get("source_ref") for row in historical} != declared:
                raise S41EventRefusal(
                    "S42_GENERATION_HISTORY_SET_MISMATCH"
                )
            for history in history_records:
                try:
                    validate_generation_readset(receipt, history, records)
                except S41HistoryRefusal as exc:
                    raise S41EventRefusal(
                        "S42_GENERATION_READSET_INVALID", exc.code
                    ) from exc
            if receipt.get("selection_status") != "UNIQUE_SELECTED":
                producer.close()
                binding = make_event_binding(
                    self,
                    producer=producer,
                    ordinal=ordinal,
                    predecessor=predecessor,
                    history_bindings=history_bindings,
                    history_sources=history_records,
                    generation=receipt,
                    attempt=None,
                    s36=None,
                    source=second_source,
                    world_before=current_world,
                    world_after=self.world().snapshot(),
                    status="OPEN",
                    generation_sources=records,
                )
                append_event_binding(self, binding)
                self._record_ongoing(binding)
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
            binding = make_event_binding(
                self,
                producer=producer,
                ordinal=ordinal,
                predecessor=predecessor,
                history_bindings=history_bindings,
                history_sources=history_records,
                generation=receipt,
                attempt=attempt,
                s36=s36,
                source=second_source,
                world_before=current_world,
                world_after=self.world().snapshot(),
                status=attempt.get("attempt_status", ""),
                generation_sources=records,
            )
            append_event_binding(self, binding)
            self._record_ongoing(binding)
            return {
                "status": "OK",
                "event": self.read_event(binding["e1_event_id"]),
                "actor_action_appended": bool(attempt.get("performed")),
            }
        except (S41EventRefusal, S42ReadRefusal):
            try:
                producer.close()
            except Exception:
                pass
            raise
        except Exception as exc:
            try:
                producer.close()
            except Exception:
                pass
            code = getattr(exc, "code", type(exc).__name__)
            try:
                generation = getattr(producer, "generation_receipt", None)
                if isinstance(generation, dict) and generation.get("hash"):
                    binding = make_event_binding(
                        self,
                        producer=producer,
                        ordinal=ordinal,
                        predecessor=predecessor,
                        history_bindings=history_bindings,
                        history_sources=history_records,
                        generation=generation,
                        attempt=None,
                        s36=None,
                        source=second_source,
                        world_before=current_world,
                        world_after=self.world().snapshot(),
                        status="REFUSED",
                        generation_sources=records,
                    )
                    append_event_binding(self, binding)
                    self._record_ongoing(binding)
            except Exception:
                pass
            raise S41EventRefusal("S42_CONTINUATION_REFUSED", str(code)) from exc

    def _record_ongoing(self, binding: Mapping[str, Any]) -> None:
        events = list(self.meta.get("s42_events") or [])
        events.append({
            "event_ordinal": binding["event_ordinal"],
            "e1_event_id": binding["e1_event_id"],
            "e1_event_hash": binding["e1_event_hash"],
            "c8_occurrence_id": binding["c8"]["occurrence_id"],
            "binding_hash": binding["hash"],
            "status": binding.get("status"),
        })
        self.meta["s42_events"] = events
        self.meta["s42_latest_ordinal"] = binding["event_ordinal"]
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
        except (S42ReadRefusal, S41EventRefusal, KeyError, OSError, ValueError) as exc:
            summaries = [{"status": "REFUSED", "code": str(exc)}]
            events_ok = False
        result["s42_events"] = summaries
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
        except (S42ReadRefusal, S41EventRefusal, KeyError, OSError, ValueError) as exc:
            summaries = [{"status": "REFUSED", "code": str(exc)}]
            latest = None
        result.update({
            "schema": S42_SCHEMA,
            "s41_schema": "SOROK_S41_CONTINUING_PERSON_SESSION@1",
            "s42_events": summaries,
            "s42_latest": latest,
        })
        return result


__all__ = ["S42_SCHEMA", "S42Session"]
