"""One product invocation per ordinary continuing-person turn."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .bootstrap import RETURN, install

install()

from candidate import digest  # noqa: E402
from s47.session import S47Session  # noqa: E402

from .errors import ProductCallError, S48Refusal  # noqa: E402
from .product import build_payload, build_prompt, run_product_cli  # noqa: E402
from .sources import (  # noqa: E402
    MISSING_FUNCTION,
    SOURCE_OWNER_HOLD,
    issue_current_source,
)

S48_SCHEMA = "SOROK_S48_ONE_CALL_CONTINUING_TURN@1"
PRODUCT_DISPATCH_KIND = "S48_PRODUCT_DISPATCH"
PRODUCT_TURN_KIND = "S48_PRODUCT_TURN"
TURN_RESULT_KIND = "S48_TURN_RESULT"
SCI05_REASON = "S48_SCI05_HOLD_NO_COMPETENT_INTERNAL_ACT_OWNER"


class S48Session(S47Session):
    """S47 person plus one-call product envelope orchestration."""

    def product_dispatches(self) -> list[dict]:
        rows = [
            row for row in self.product.store.episodes(self.branch_id)
            if row.get("kind") == PRODUCT_DISPATCH_KIND
        ]
        return [
            {
                "episode_id": row.get("episode_id"),
                "clock": row.get("clock"),
                "body": dict(row.get("body") or {}),
            }
            for row in rows
        ]

    def product_dispatch(self, source_event_ref: str) -> dict | None:
        rows = [
            row for row in self.product_dispatches()
            if (row["body"].get("source_event_ref") == source_event_ref)
        ]
        return rows[-1] if rows else None

    def product_turns(self) -> list[dict]:
        rows = [
            row for row in self.product.store.episodes(self.branch_id)
            if row.get("kind") == PRODUCT_TURN_KIND
        ]
        return [
            {
                "episode_id": row.get("episode_id"),
                "clock": row.get("clock"),
                "body": dict(row.get("body") or {}),
            }
            for row in rows
        ]

    def product_turn(self, source_event_ref: str) -> dict | None:
        rows = [
            row for row in self.product_turns()
            if (row["body"].get("source_event_ref") == source_event_ref)
        ]
        return rows[-1] if rows else None

    def product_turn_by_id(self, turn_id: str) -> dict | None:
        rows = [
            row for row in self.product_turns()
            if row["body"].get("turn_id") == turn_id
        ]
        return rows[-1] if rows else None

    def product_result(self, turn_id: str) -> dict | None:
        rows = [
            row for row in self.product.store.episodes(self.branch_id)
            if row.get("kind") == TURN_RESULT_KIND
            and (row.get("body") or {}).get("turn_id") == turn_id
        ]
        if not rows:
            return None
        row = rows[-1]
        return {
            "episode_id": row.get("episode_id"),
            "clock": row.get("clock"),
            "body": dict(row.get("body") or {}),
        }

    def _append_dispatch(self, body: Mapping[str, Any]) -> dict:
        episode = self.product._append_episode(
            self.branch_id, "A", PRODUCT_DISPATCH_KIND, self.clock(), dict(body)
        )
        self.product._checkpoint(self.branch_id, self.clock(), self.world())
        return episode

    def _append_turn(self, body: Mapping[str, Any]) -> dict:
        episode = self.product._append_episode(
            self.branch_id, "A", PRODUCT_TURN_KIND, self.clock(), dict(body)
        )
        self.product._checkpoint(self.branch_id, self.clock(), self.world())
        return episode

    def _append_result(self, body: Mapping[str, Any]) -> dict:
        episode = self.product._append_episode(
            self.branch_id, "A", TURN_RESULT_KIND, self.clock(), dict(body)
        )
        self.product._checkpoint(self.branch_id, self.clock(), self.world())
        return episode

    def _cached_result(self, turn: dict) -> dict:
        turn_id = turn["body"].get("turn_id", "")
        result = self.product_result(turn_id)
        if result is None:
            return {
                "schema": S48_SCHEMA,
                "status": "PENDING_UNKNOWN",
                "cached": True,
                "provider_call_count": 0,
                "turn_id": turn_id,
                "source_event_ref": turn["body"].get("source_event_ref"),
                "event_ref": "",
                "reason": "S48_PRODUCT_TURN_WITHOUT_RESULT",
            }
        body = dict(result["body"])
        body.update({
            "schema": S48_SCHEMA,
            "cached": True,
            "provider_call_count": 0,
            "turn_id": turn_id,
            "source_event_ref": turn["body"].get("source_event_ref"),
            "result_episode_id": result["episode_id"],
        })
        return body

    def _pending_dispatch(self, dispatch: dict) -> dict:
        return {
            "schema": S48_SCHEMA,
            "status": "PENDING_UNKNOWN",
            "cached": False,
            "provider_call_count": 0,
            "turn_id": dispatch["body"].get("turn_id"),
            "dispatch_id": dispatch["episode_id"],
            "source_event_ref": dispatch["body"].get("source_event_ref"),
            "event_ref": "",
            "reason": "S48_DISPATCH_WITHOUT_RESULT_NOT_REISSUED",
        }

    @staticmethod
    def _source_event(events: list[dict], source_ref: str | None) -> dict:
        if source_ref is None:
            if not events:
                raise S48Refusal("S48_OCCURRED_EVENT_MISSING")
            return events[-1]
        for event in events:
            if (
                event.get("e1_event_id") == source_ref
                or event.get("e1_event_hash") == source_ref
            ):
                return event
        raise S48Refusal("S48_SOURCE_EVENT_NOT_FOUND", source_ref)

    def _event_for_payload(self, events: list[dict], source_ref: str) -> dict:
        return self._source_event(events, source_ref)

    def _append_failure(self, *, turn_id: str, source_ref: str,
                        source_hash: str, payload_hash: str, prompt_hash: str,
                        code: str, receipt: Mapping[str, Any] | None) -> dict:
        body = {
            "schema": S48_SCHEMA,
            "status": "CALL_FAILED",
            "turn_id": turn_id,
            "source_event_ref": source_ref,
            "source_event_hash": source_hash,
            "payload_hash": payload_hash,
            "prompt_hash": prompt_hash,
            "reason": code,
            "call_receipt": dict(receipt or {}),
            "provider_call_count": int(
                (receipt or {}).get("provider_call_count", 0) or 0
            ),
            "event_ref": "",
            "cached": False,
        }
        turn = self._append_turn(body)
        result = self._append_result({
            **body,
            "status": "CALL_FAILED",
            "product_turn_ref": turn["episode_id"],
            "result_episode_id": "",
        })
        body["product_turn_ref"] = turn["episode_id"]
        body["result_episode_id"] = result["episode_id"]
        return body

    def run_turn(
        self,
        *,
        source_event_ref: str | None = None,
        replay_turn_id: str | None = None,
        product_runner=None,
        product_workdir: str | Path | None = None,
        product_log_dir: str | Path | None = None,
        timeout: int = 300,
    ) -> dict:
        events = self.read_events()
        if replay_turn_id is not None:
            turn = self.product_turn_by_id(replay_turn_id)
            if turn is None:
                dispatch = next(
                    (
                        row for row in self.product_dispatches()
                        if row["body"].get("turn_id") == replay_turn_id
                    ),
                    None,
                )
                if dispatch is not None:
                    return self._pending_dispatch(dispatch)
                raise S48Refusal("S48_TURN_NOT_FOUND", replay_turn_id)
            return self._cached_result(turn)

        source_event = self._source_event(events, source_event_ref)
        source_ref = source_event.get("e1_event_id")
        source_hash = source_event.get("e1_event_hash", "")
        if not source_ref or not isinstance(source_event.get("c9"), Mapping):
            raise S48Refusal("S48_FIRST_C9_RESULT_MISSING")

        existing_turn = self.product_turn(source_ref)
        if existing_turn is not None:
            return self._cached_result(existing_turn)
        existing_dispatch = self.product_dispatch(source_ref)
        if existing_dispatch is not None:
            return self._pending_dispatch(existing_dispatch)
        if source_event_ref is not None and source_event is not events[-1]:
            raise S48Refusal("S48_SOURCE_EVENT_NOT_CURRENT", source_ref)

        payload = build_payload(self, event=source_event)
        prompt = build_prompt(payload)
        payload_hash = digest(payload)
        prompt_hash = digest({"prompt": prompt})
        turn_id = "S48_TURN_" + digest({
            "source_event_ref": source_ref,
            "payload_hash": payload_hash,
            "prompt_hash": prompt_hash,
        })[:24].upper()
        before_world = digest(self.world().snapshot())
        workdir = Path(product_workdir or RETURN / "runtime" / "product-workdir")
        log_dir = Path(product_log_dir or RETURN / "logs")
        runner = product_runner or run_product_cli

        dispatch_body = {
            "schema": S48_SCHEMA,
            "status": "DISPATCHED",
            "turn_id": turn_id,
            "source_event_ref": source_ref,
            "source_event_hash": source_hash,
            "payload_hash": payload_hash,
            "prompt_hash": prompt_hash,
            "provider_call_count": 0,
            "actual_provider_call": False,
        }
        dispatch = self._append_dispatch(dispatch_body)

        try:
            call = runner(
                prompt, workdir=workdir, log_dir=log_dir, timeout=timeout
            )
        except ProductCallError as exc:
            return self._append_failure(
                turn_id=turn_id, source_ref=source_ref,
                source_hash=source_hash, payload_hash=payload_hash,
                prompt_hash=prompt_hash, code=exc.code, receipt=exc.receipt,
            )
        except Exception as exc:
            return self._append_failure(
                turn_id=turn_id, source_ref=source_ref,
                source_hash=source_hash, payload_hash=payload_hash,
                prompt_hash=prompt_hash, code=getattr(exc, "code", type(exc).__name__),
                receipt={},
            )

        envelope = call.get("envelope")
        receipt = dict(call.get("call_receipt") or {})
        if not isinstance(envelope, dict):
            return self._append_failure(
                turn_id=turn_id, source_ref=source_ref,
                source_hash=source_hash, payload_hash=payload_hash,
                prompt_hash=prompt_hash, code="S48_PRODUCT_ENVELOPE_MISSING",
                receipt=receipt,
            )
        if digest(self.world().snapshot()) != before_world:
            return self._append_failure(
                turn_id=turn_id, source_ref=source_ref,
                source_hash=source_hash, payload_hash=payload_hash,
                prompt_hash=prompt_hash, code="S48_PRODUCT_MUTATED_WORLD",
                receipt=receipt,
            )
        self.world_prerequisites()
        turn_body = {
            "schema": S48_SCHEMA,
            "status": "CALLED",
            "turn_id": turn_id,
            "source_event_ref": source_ref,
            "source_event_hash": source_hash,
            "source_c9": dict(source_event.get("c9") or {}),
            "payload": payload,
            "payload_hash": payload_hash,
            "prompt_hash": prompt_hash,
            "call_receipt": receipt,
            "provider_call_count": int(receipt.get("provider_call_count", 0) or 0),
            "envelope": envelope,
            "no_input_barrier": (
                "SELF_ACCOUNT_ABSENT_NO_NEW_INTERPRETIVE_INPUT"
                if not envelope.get("self_account_present") else ""
            ),
            "dispatch_id": dispatch["episode_id"],
        }
        turn = self._append_turn(turn_body)

        if envelope.get("self_account_present"):
            result = self._append_result({
                "schema": S48_SCHEMA,
                "status": "SCI05_HOLD",
                "turn_id": turn_id,
                "source_event_ref": source_ref,
                "source_event_hash": source_hash,
                "product_turn_ref": turn["episode_id"],
                "sci05_hold": True,
                "reason": SCI05_REASON,
                "self_account": envelope.get("self_account"),
                "prospective_not_realized": True,
                "event_ref": "",
                "cached": False,
                "provider_call_count": turn_body["provider_call_count"],
            })
            return {
                **result["body"],
                "turn_id": turn_id,
                "product_turn_ref": turn["episode_id"],
                "result_episode_id": result["episode_id"],
                "cached": False,
                "provider_call_count": turn_body["provider_call_count"],
            }

        allowed = {
            row.get("candidate_id")
            for row in payload.get("allowed_prospective_candidates") or []
        }
        prospective = list(envelope.get("prospective") or [])
        if not allowed:
            result = self._append_result({
                "schema": S48_SCHEMA,
                "status": "SOURCE_OWNER_HOLD",
                "turn_id": turn_id,
                "source_event_ref": source_ref,
                "source_event_hash": source_hash,
                "product_turn_ref": turn["episode_id"],
                "reason": SOURCE_OWNER_HOLD,
                "missing_function": MISSING_FUNCTION,
                "candidate_id": (
                    prospective[0].get("candidate_id") if prospective else ""
                ),
                "event_ref": "",
                "cached": False,
                "provider_call_count": turn_body["provider_call_count"],
            })
            return {
                **result["body"],
                "turn_id": turn_id,
                "product_turn_ref": turn["episode_id"],
                "result_episode_id": result["episode_id"],
                "cached": False,
                "provider_call_count": turn_body["provider_call_count"],
            }
        if len(prospective) != 1:
            status = "UNRESOLVED" if len(prospective) > 1 else "NO_PROSPECTIVE_PROPOSAL"
            result = self._append_result({
                "schema": S48_SCHEMA,
                "status": status,
                "turn_id": turn_id,
                "source_event_ref": source_ref,
                "source_event_hash": source_hash,
                "product_turn_ref": turn["episode_id"],
                "prospective": prospective,
                "event_ref": "",
                "cached": False,
                "provider_call_count": turn_body["provider_call_count"],
            })
            return {
                **result["body"],
                "turn_id": turn_id,
                "product_turn_ref": turn["episode_id"],
                "result_episode_id": result["episode_id"],
                "cached": False,
                "provider_call_count": turn_body["provider_call_count"],
            }

        candidate = prospective[0].get("candidate_id")
        if candidate not in allowed:
            result = self._append_result({
                "schema": S48_SCHEMA,
                "status": "SOURCE_OWNER_HOLD",
                "turn_id": turn_id,
                "source_event_ref": source_ref,
                "source_event_hash": source_hash,
                "product_turn_ref": turn["episode_id"],
                "reason": SOURCE_OWNER_HOLD,
                "candidate_id": candidate,
                "event_ref": "",
                "cached": False,
                "provider_call_count": turn_body["provider_call_count"],
            })
            return {
                **result["body"],
                "turn_id": turn_id,
                "product_turn_ref": turn["episode_id"],
                "result_episode_id": result["episode_id"],
                "cached": False,
                "provider_call_count": turn_body["provider_call_count"],
            }
        try:
            case, source, source_event = issue_current_source(self, candidate)
        except S48Refusal as exc:
            result = self._append_result({
                "schema": S48_SCHEMA,
                "status": "SOURCE_OWNER_HOLD",
                "turn_id": turn_id,
                "source_event_ref": source_ref,
                "source_event_hash": source_hash,
                "product_turn_ref": turn["episode_id"],
                "reason": SOURCE_OWNER_HOLD,
                "candidate_id": candidate,
                "source_refusal": exc.code,
                "event_ref": "",
                "cached": False,
                "provider_call_count": turn_body["provider_call_count"],
            })
            return {
                **result["body"],
                "turn_id": turn_id,
                "product_turn_ref": turn["episode_id"],
                "result_episode_id": result["episode_id"],
                "cached": False,
                "provider_call_count": turn_body["provider_call_count"],
            }
        admitted = self.admit_event(
            case=case,
            source=source,
            history_event_refs=(source_ref,),
            event_time=self.clock() + 1,
        )
        event = admitted.get("event") or {}
        result = self._append_result({
            "schema": S48_SCHEMA,
            "status": "REALIZED",
            "turn_id": turn_id,
            "source_event_ref": source_ref,
            "source_event_hash": source_hash,
            "product_turn_ref": turn["episode_id"],
            "candidate_id": candidate,
            "source_owner": source.get("b_owner"),
            "source_performer_owner": source.get("source_performer_owner"),
            "source_actor": source.get("b_actor"),
            "source_event_ref_candidate": source.get("b_event_ref"),
            "source_event_hash_candidate": source.get("b_event_hash"),
            "source_world_event_ref": source_event.get("event_id"),
            "source_world_event_hash": source_event.get("hash"),
            "prospective": prospective,
            "no_input_barrier": turn_body["no_input_barrier"],
            "event_ref": event.get("e1_event_id", ""),
            "event_hash": event.get("e1_event_hash", ""),
            "event_ordinal": event.get("event_ordinal"),
            "event_time": event.get("event_time"),
            "admission_status": admitted.get("status"),
            "cached": False,
            "provider_call_count": turn_body["provider_call_count"],
            "target_proposals": list(event.get("target_proposals") or []),
        })
        return {
            **result["body"],
            "turn_id": turn_id,
            "product_turn_ref": turn["episode_id"],
            "result_episode_id": result["episode_id"],
            "cached": False,
            "provider_call_count": turn_body["provider_call_count"],
            "event": event,
        }

    def verify(self) -> dict:
        result = super().verify()
        try:
            turns = self.product_turns()
            dispatches = self.product_dispatches()
            result["s48_product_turns"] = {
                "status": "OK",
                "count": len(turns),
                "dispatches": len(dispatches),
                "calls": [
                    {
                        "turn_id": row["body"].get("turn_id"),
                        "source_event_ref": row["body"].get("source_event_ref"),
                        "status": row["body"].get("status"),
                        "provider_call_count": row["body"].get("provider_call_count"),
                    }
                    for row in turns
                ],
            }
            ok = True
        except Exception as exc:
            result["s48_product_turns"] = {
                "status": "REFUSED", "code": getattr(exc, "code", type(exc).__name__)
            }
            ok = False
        result["ok"] = bool(result.get("ok")) and ok
        return result


__all__ = [
    "PRODUCT_DISPATCH_KIND", "PRODUCT_TURN_KIND", "S48_SCHEMA", "S48Session",
    "SCI05_REASON", "SOURCE_OWNER_HOLD", "TURN_RESULT_KIND",
]
