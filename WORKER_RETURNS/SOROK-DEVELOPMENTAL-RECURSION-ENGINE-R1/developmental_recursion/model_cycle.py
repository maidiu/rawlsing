"""Durable recursive batch coordinator.

The coordinator owns only orchestration and custody.  It never applies a
psychological delta, never interprets prospective prose, and never gives a
provider or an impression proposal a writer into the owner.  The supplied
``BatchEngine`` owns sequential realization and history; ``DevelopmentOwner``
owns state and source/operation admissibility.

The external contract is frozen in ``ABI.md`` and ``contracts.py``.
"""
from __future__ import annotations

import fcntl
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

from .contracts import (
    EventProposal,
    RecursionRefusal,
    StateIdentity,
    canonical,
    detached,
    digest,
)

STORE_SCHEMA = "SOROK_DEVELOPMENTAL_RECURSION_CYCLE@1.0.0"
MODES = ("BOOTSTRAP", "ORDINARY", "TERMINAL")
PHASES = ("READY_BOOTSTRAP", "PENDING_BATCH", "COMPLETE", "HELD")
RESPONSE_KEYS = {"retrospective", "prospective"}
RETRO_KEYS = {"batch_id", "history_hash", "event_ids", "impressions"}
EVENT_REQUIRED = {
    "event_id",
    "event_time",
    "operation",
    "source_refs",
    "participants",
    "circumstances",
}
EVENT_OPTIONAL = {"interval"}
STATE_KEYS = {"root", "actor", "branch", "clock", "state_hash"}


class AmbiguousModelCall(RecursionRefusal):
    """The cycle cannot safely reissue a provider or engine operation."""


class CycleStoreError(RecursionRefusal):
    """The durable cycle store is absent, malformed, or inconsistent."""


def _state_document(value: Any) -> dict[str, Any]:
    if isinstance(value, StateIdentity):
        doc = value.document()
    elif isinstance(value, Mapping):
        doc = detached(value)
    else:
        raise RecursionRefusal("owner.snapshot() must return StateIdentity")
    if not isinstance(doc, Mapping) or set(doc) != STATE_KEYS:
        raise RecursionRefusal("owner state identity has malformed fields")
    if not isinstance(doc["root"], str) or not isinstance(doc["actor"], str):
        raise RecursionRefusal("owner root/actor must be strings")
    if not isinstance(doc["branch"], str):
        raise RecursionRefusal("owner branch must be a string")
    if isinstance(doc["clock"], bool) or not isinstance(doc["clock"], int):
        raise RecursionRefusal("owner clock must be an integer")
    if not isinstance(doc["state_hash"], str) or not doc["state_hash"]:
        raise RecursionRefusal("owner state_hash must be a nonempty string")
    return detached(doc)


def _validate_context(value: Any) -> Any:
    try:
        return detached(value)
    except Exception as exc:
        raise RecursionRefusal("context must be detached JSON, not a writer") from exc


def _report(exc: Exception) -> str:
    code = type(exc).__name__
    text = str(exc)
    return f"{code}: {text}" if text else code


def _new_store(before: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema": STORE_SCHEMA,
        "identity": {
            "root": before["root"],
            "actor": before["actor"],
            "branch": before["branch"],
        },
        "expected_owner_state": detached(before),
        "phase": "READY_BOOTSTRAP",
        "next_sequence": 1,
        "pending": None,
        "retrospectives": [],
        "proposed_impressions": [],
        "model_call": None,
        "last_error": None,
    }


def _validate_store(store: Any) -> dict[str, Any]:
    if not isinstance(store, Mapping):
        raise CycleStoreError("cycle store must be a JSON object")
    if set(store) != {
        "schema",
        "identity",
        "expected_owner_state",
        "phase",
        "next_sequence",
        "pending",
        "retrospectives",
        "proposed_impressions",
        "model_call",
        "last_error",
    }:
        raise CycleStoreError("cycle store has unexpected keys")
    if store["schema"] != STORE_SCHEMA:
        raise CycleStoreError("cycle store schema mismatch")
    if not isinstance(store["identity"], Mapping) or set(store["identity"]) != {
        "root",
        "actor",
        "branch",
    }:
        raise CycleStoreError("cycle store identity is malformed")
    expected = _state_document(store["expected_owner_state"])
    if any(
        store["identity"][key] != expected[key]
        for key in ("root", "actor", "branch")
    ):
        raise CycleStoreError("cycle store identity does not match expected state")
    if store["phase"] not in PHASES:
        raise CycleStoreError("cycle store phase is invalid")
    if isinstance(store["next_sequence"], bool) or not isinstance(
        store["next_sequence"], int
    ) or store["next_sequence"] < 1:
        raise CycleStoreError("cycle store next_sequence is invalid")
    pending = store["pending"]
    if pending is not None:
        if not isinstance(pending, Mapping) or set(pending) != {
            "batch_id",
            "history_hash",
            "records",
        }:
            raise CycleStoreError("cycle store pending batch is malformed")
        if not isinstance(pending["batch_id"], str) or not pending["batch_id"]:
            raise CycleStoreError("pending batch_id is invalid")
        if not isinstance(pending["history_hash"], str):
            raise CycleStoreError("pending history_hash is invalid")
        if not isinstance(pending["records"], list):
            raise CycleStoreError("pending records are invalid")
    if store["phase"] == "PENDING_BATCH" and pending is None:
        raise CycleStoreError("pending phase has no pending batch")
    if store["phase"] == "COMPLETE" and pending is not None:
        raise CycleStoreError("complete phase retains a pending batch")
    if not isinstance(store["retrospectives"], list):
        raise CycleStoreError("retrospectives must be a list")
    if not isinstance(store["proposed_impressions"], list):
        raise CycleStoreError("proposed_impressions must be a list")
    if store["model_call"] is not None:
        if not isinstance(store["model_call"], Mapping):
            raise CycleStoreError("model_call reservation is malformed")
        if store["model_call"].get("mode") not in MODES:
            raise CycleStoreError("model_call mode is invalid")
        if not isinstance(store["model_call"].get("status"), str):
            raise CycleStoreError("model_call status is invalid")
    if store["last_error"] is not None and not isinstance(
        store["last_error"], Mapping
    ):
        raise CycleStoreError("last_error must be null or an object")
    return detached(store)


class RecursionCycle:
    """Coordinate provider halves and sequential batch realization.

    The store is a single JSON file.  Every public method takes an exclusive
    lock, persists a model-call reservation before invoking the provider, and
    leaves an ambiguous reservation durable rather than guessing whether the
    call happened.
    """

    def __init__(self, engine: Any, provider: Any, store_path: str | Path) -> None:
        if not hasattr(engine, "owner"):
            raise RecursionRefusal("engine has no owner")
        if not hasattr(provider, "call"):
            raise RecursionRefusal("provider has no call()")
        self.engine = engine
        self.provider = provider
        self.store_path = Path(store_path)

    # -- public cycle methods -------------------------------------------------

    def bootstrap(self, context: Any = None) -> dict[str, Any]:
        context_doc = _validate_context(context)
        with self._locked():
            if self.store_path.exists():
                raise RecursionRefusal("bootstrap is exactly-once: store exists")
            before = self._snapshot()
            store = _new_store(before)
            self._save(store)
            self._active(store)
            response = self._call(
                store,
                mode="BOOTSTRAP",
                context=context_doc,
                previous=None,
                before=before,
            )
            try:
                retrospective, proposals = self._parse_response(
                    response, "BOOTSTRAP", None, store
                )
            except Exception as exc:
                self._hold(store, "INVALID_PROVIDER_RESPONSE", _report(exc))
                raise AmbiguousModelCall(
                    f"BOOTSTRAP response invalid; cycle held: {_report(exc)}"
                ) from exc
            if retrospective is not None:
                self._hold(store, "BOOTSTRAP_MEMORY", "bootstrap retrospective must be null")
                raise AmbiguousModelCall("bootstrap must not invent prior memory")
            assert proposals is not None
            batch, after = self._run_batch(
                store, self._next_batch_id(store), proposals, before
            )
            store["pending"] = batch
            store["next_sequence"] += 1
            store["phase"] = "PENDING_BATCH"
            store["expected_owner_state"] = detached(after)
            store["model_call"] = None
            store["last_error"] = None
            self._save(store)
            return detached(batch)

    def advance(self, context: Any = None) -> dict[str, Any]:
        context_doc = _validate_context(context)
        with self._locked():
            store = self._load()
            self._active(store)
            if store["phase"] != "PENDING_BATCH":
                raise RecursionRefusal("advance requires a pending realized batch")
            before = self._check_expected(store)
            pending, records, previous = self._verified_previous(store)
            response = self._call(
                store,
                mode="ORDINARY",
                context=context_doc,
                previous=previous,
                before=before,
            )
            try:
                retrospective, proposals = self._parse_response(
                    response, "ORDINARY", pending, store
                )
            except Exception as exc:
                self._hold(store, "INVALID_PROVIDER_RESPONSE", _report(exc))
                raise AmbiguousModelCall(
                    f"ORDINARY response invalid; cycle held: {_report(exc)}"
                ) from exc
            if retrospective is None or proposals is None:
                self._hold(
                    store,
                    "ORDINARY_SHAPE",
                    "ordinary response requires both retrospective and prospective",
                )
                raise AmbiguousModelCall("ordinary response must contain both halves")
            # The retrospective half completes the preceding recursion before
            # any effects from the next prospective batch can occur.
            self._remember_retrospective(store, retrospective)
            store["model_call"]["status"] = "RETROSPECTED_PENDING_REALIZATION"
            self._save(store)
            new_batch, after = self._run_batch(
                store, self._next_batch_id(store), proposals, before
            )
            store["pending"] = new_batch
            store["next_sequence"] += 1
            store["phase"] = "PENDING_BATCH"
            store["expected_owner_state"] = detached(after)
            store["model_call"] = None
            store["last_error"] = None
            self._save(store)
            return detached(new_batch)

    def finish(self, context: Any = None) -> dict[str, Any]:
        context_doc = _validate_context(context)
        with self._locked():
            store = self._load()
            self._active(store)
            if store["phase"] != "PENDING_BATCH":
                raise RecursionRefusal("finish requires a pending realized batch")
            before = self._check_expected(store)
            pending, _records, previous = self._verified_previous(store)
            response = self._call(
                store,
                mode="TERMINAL",
                context=context_doc,
                previous=previous,
                before=before,
            )
            try:
                retrospective, proposals = self._parse_response(
                    response, "TERMINAL", pending, store
                )
            except Exception as exc:
                self._hold(store, "INVALID_PROVIDER_RESPONSE", _report(exc))
                raise AmbiguousModelCall(
                    f"TERMINAL response invalid; cycle held: {_report(exc)}"
                ) from exc
            if retrospective is None:
                self._hold(store, "TERMINAL_SHAPE", "terminal retrospective is missing")
                raise AmbiguousModelCall("terminal retrospective is required")
            if proposals is not None:
                self._hold(
                    store, "TERMINAL_NEXT_BATCH", "terminal response proposed a next batch"
                )
                raise AmbiguousModelCall("terminal response must not propose a next batch")
            self._remember_retrospective(store, retrospective)
            store["phase"] = "COMPLETE"
            store["pending"] = None
            store["model_call"] = None
            store["last_error"] = None
            self._save(store)
            return detached(retrospective)

    # -- provider / engine custody -------------------------------------------

    def _call(
        self,
        store: dict[str, Any],
        *,
        mode: str,
        context: Any,
        previous: Mapping[str, Any] | None,
        before: Mapping[str, Any],
    ) -> dict[str, Any]:
        request = {
            "mode": mode,
            "context": detached(context),
            "previous": None if previous is None else detached(previous),
        }
        reservation = {
            "mode": mode,
            "batch_id": None if previous is None else previous["batch_id"],
            "request_hash": digest(request),
            "status": "RESERVED",
            "expected_owner_state": detached(before),
        }
        store["model_call"] = reservation
        self._save(store)
        try:
            raw = self.provider.call(detached(request))
            response = detached(raw)
        except Exception as exc:
            self._hold(store, "AMBIGUOUS_PROVIDER_CALL", _report(exc))
            raise AmbiguousModelCall(
                f"ambiguous provider call; preserved reservation: {_report(exc)}"
            ) from exc
        store["model_call"]["status"] = "RETURNED"
        store["model_call"]["response_hash"] = digest(response)
        self._save(store)
        try:
            after = self._snapshot()
        except Exception as exc:
            self._hold(store, "OWNER_SNAPSHOT", _report(exc))
            raise AmbiguousModelCall(
                f"owner snapshot failed after provider call: {_report(exc)}"
            ) from exc
        if detached(after) != detached(before):
            self._hold(
                store,
                "PROVIDER_MUTATED_OWNER",
                "provider call changed owner state; refusing effects",
            )
            raise AmbiguousModelCall("provider mutated owner state; cycle held")
        return response

    def _run_batch(
        self,
        store: dict[str, Any],
        batch_id: str,
        proposals: Sequence[EventProposal],
        before: Mapping[str, Any],
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        try:
            raw = self.engine.run_batch(batch_id, list(proposals))
            result = detached(raw)
        except Exception as exc:
            self._hold(store, "ENGINE_ERROR", _report(exc))
            raise AmbiguousModelCall(
                f"engine batch failed; saved recursion history retained: {_report(exc)}"
            ) from exc
        if not isinstance(result, Mapping):
            self._hold(store, "ENGINE_RESULT", "run_batch must return an object")
            raise AmbiguousModelCall("engine returned a malformed batch")
        if set(result) != {"batch_id", "history_hash", "records"}:
            self._hold(store, "ENGINE_RESULT", "run_batch result keys are not exact")
            raise AmbiguousModelCall("engine returned a malformed batch")
        if result["batch_id"] != batch_id:
            self._hold(store, "ENGINE_RESULT", "run_batch batch id mismatch")
            raise AmbiguousModelCall("engine returned the wrong batch id")
        if not isinstance(result["history_hash"], str):
            self._hold(store, "ENGINE_RESULT", "history_hash must be a string")
            raise AmbiguousModelCall("engine returned a malformed history hash")
        records = detached(result["records"])
        if not isinstance(records, list):
            self._hold(store, "ENGINE_RESULT", "records must be a list")
            raise AmbiguousModelCall("engine returned malformed records")
        if digest(records) != result["history_hash"]:
            self._hold(store, "ENGINE_RESULT", "history hash does not bind records")
            raise AmbiguousModelCall("engine history hash does not bind records")
        expected_ids = [p.event_id for p in proposals]
        actual_ids = [
            row.get("event_id") if isinstance(row, Mapping) else None
            for row in records
        ]
        if actual_ids != expected_ids or any(not isinstance(x, str) or not x for x in actual_ids):
            self._hold(store, "ENGINE_ORDER", "records do not match proposed event order")
            raise AmbiguousModelCall("engine records do not match proposal order")
        try:
            after = self._snapshot()
        except Exception as exc:
            self._hold(store, "OWNER_SNAPSHOT", _report(exc))
            raise AmbiguousModelCall(
                f"owner snapshot failed after engine batch: {_report(exc)}"
            ) from exc
        if any(after[key] != before[key] for key in ("root", "actor", "branch")):
            self._hold(store, "ENGINE_IDENTITY", "root/actor/branch changed after batch")
            raise AmbiguousModelCall("owner identity changed after engine batch")
        if after["clock"] < before["clock"]:
            self._hold(store, "ENGINE_CLOCK", "owner clock moved backwards")
            raise AmbiguousModelCall("owner clock moved backwards")
        return detached(result), after

    # -- parsing and validation ----------------------------------------------

    def _parse_response(
        self,
        response: Mapping[str, Any],
        mode: str,
        pending: Mapping[str, Any] | None,
        store: dict[str, Any],
    ) -> tuple[dict[str, Any] | None, list[EventProposal] | None]:
        if not isinstance(response, Mapping):
            raise RecursionRefusal("provider response must be an object")
        response = detached(response)
        if set(response) != RESPONSE_KEYS:
            raise RecursionRefusal("provider response must have only retrospective/prospective")
        retrospective = response["retrospective"]
        prospective = response["prospective"]
        if mode == "BOOTSTRAP":
            if retrospective is not None:
                raise RecursionRefusal("bootstrap retrospective must be null")
            if not isinstance(prospective, list):
                raise RecursionRefusal("bootstrap prospective must be a list")
        elif mode == "ORDINARY":
            if retrospective is None or prospective is None:
                raise RecursionRefusal("ordinary requires retrospective and prospective")
            if not isinstance(prospective, list):
                raise RecursionRefusal("ordinary prospective must be a list")
        elif mode == "TERMINAL":
            if retrospective is None:
                raise RecursionRefusal("terminal retrospective is required")
            if prospective is not None:
                raise RecursionRefusal("terminal prospective must be null")
        else:
            raise RecursionRefusal("unknown provider mode")
        retro_doc = None
        if retrospective is not None:
            if pending is None:
                raise RecursionRefusal("retrospective without a preceding batch")
            retro_doc = self._parse_retrospective(retrospective, pending)
        proposals = None
        if prospective is not None:
            proposals = self._parse_proposals(prospective, store)
        return retro_doc, proposals

    @staticmethod
    def _parse_retrospective(
        value: Any, pending: Mapping[str, Any]
    ) -> dict[str, Any]:
        if not isinstance(value, Mapping):
            raise RecursionRefusal("retrospective must be an object")
        value = detached(value)
        if set(value) != RETRO_KEYS:
            raise RecursionRefusal("retrospective keys are not exact")
        if value["batch_id"] != pending["batch_id"]:
            raise RecursionRefusal("retrospective batch id does not bind pending batch")
        if value["history_hash"] != pending["history_hash"]:
            raise RecursionRefusal("retrospective history hash does not bind pending batch")
        event_ids = value["event_ids"]
        if not isinstance(event_ids, list) or any(
            not isinstance(x, str) or not x for x in event_ids
        ):
            raise RecursionRefusal("retrospective event_ids are malformed")
        if event_ids != [
            row.get("event_id") for row in pending["records"] if isinstance(row, Mapping)
        ]:
            raise RecursionRefusal("retrospective event order does not bind history")
        if not isinstance(value["impressions"], list):
            raise RecursionRefusal("retrospective impressions must be a list")
        return detached(value)

    def _parse_proposals(
        self, value: Any, store: dict[str, Any]
    ) -> list[EventProposal]:
        if not isinstance(value, list) or not 3 <= len(value) <= 5:
            raise RecursionRefusal("prospective must contain 3-5 event documents")
        owner = getattr(self.engine, "owner", None)
        if owner is None:
            raise RecursionRefusal("engine has no owner for proposal validation")
        proposals: list[EventProposal] = []
        seen: set[str] = set()
        for raw in value:
            if not isinstance(raw, Mapping):
                raise RecursionRefusal("prospective event must be an object")
            doc = detached(raw)
            if not isinstance(doc, Mapping) or not isinstance(doc, dict):
                raise RecursionRefusal("prospective event must detach to an object")
            if set(doc) - (EVENT_REQUIRED | EVENT_OPTIONAL):
                raise RecursionRefusal("prospective event has extra keys")
            if not EVENT_REQUIRED <= set(doc):
                raise RecursionRefusal("prospective event is missing required keys")
            event_id = doc["event_id"]
            if not isinstance(event_id, str) or not event_id:
                raise RecursionRefusal("event_id must be a nonempty string")
            if event_id in seen:
                raise RecursionRefusal("event_id is duplicated in one prospective batch")
            seen.add(event_id)
            event_time = doc["event_time"]
            if isinstance(event_time, bool) or not isinstance(event_time, int):
                raise RecursionRefusal("event_time must be an integer")
            operation = doc["operation"]
            if not isinstance(operation, str) or not operation:
                raise RecursionRefusal("operation must be a nonempty string")
            source_refs = doc["source_refs"]
            if not isinstance(source_refs, list) or any(
                not isinstance(x, str) or not x for x in source_refs
            ):
                raise RecursionRefusal("source_refs must be a list of nonempty strings")
            participants = doc["participants"]
            if not isinstance(participants, list) or any(
                not isinstance(x, str) or not x for x in participants
            ):
                raise RecursionRefusal("participants must be a list of nonempty strings")
            circumstances = doc["circumstances"]
            if not isinstance(circumstances, Mapping):
                raise RecursionRefusal("circumstances must be an object")
            interval = doc.get("interval")
            if interval is not None and not isinstance(interval, Mapping):
                raise RecursionRefusal("interval must be an object or null")
            proposal = EventProposal(
                event_id=event_id,
                event_time=event_time,
                operation=operation,
                source_refs=tuple(source_refs),
                participants=tuple(participants),
                circumstances=detached(circumstances),
                interval=None if interval is None else detached(interval),
            )
            owner.validate_proposal(proposal)
            proposals.append(proposal)
        return proposals

    # -- durable batch/state custody -----------------------------------------

    def _verified_previous(
        self, store: dict[str, Any]
    ) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
        pending = store["pending"]
        if not isinstance(pending, Mapping):
            raise RecursionRefusal("no pending realized batch")
        try:
            history = self.engine.history(pending["batch_id"])
            history = detached(history)
        except Exception as exc:
            self._hold(store, "HISTORY_MISSING", _report(exc))
            raise AmbiguousModelCall(
                f"preceding batch history unavailable: {_report(exc)}"
            ) from exc
        if not isinstance(history, Mapping) or set(history) != {
            "batch_id",
            "history_hash",
            "records",
        }:
            self._hold(store, "HISTORY_MALFORMED", "engine history is malformed")
            raise AmbiguousModelCall("preceding batch history is malformed")
        if history["batch_id"] != pending["batch_id"]:
            self._hold(store, "HISTORY_MISMATCH", "history batch id changed")
            raise AmbiguousModelCall("history batch id changed")
        records = detached(history["records"])
        if not isinstance(records, list) or detached(records) != detached(
            pending["records"]
        ):
            self._hold(store, "HISTORY_REWRITE", "history records changed")
            raise AmbiguousModelCall("history records changed")
        if history["history_hash"] != pending["history_hash"] or digest(
            records
        ) != pending["history_hash"]:
            self._hold(store, "HISTORY_HASH", "history hash does not bind records")
            raise AmbiguousModelCall("history hash does not bind records")
        event_ids: list[str] = []
        events: list[dict[str, Any]] = []
        for row in records:
            if not isinstance(row, Mapping):
                self._hold(store, "HISTORY_RECORD", "record is not an object")
                raise AmbiguousModelCall("history record is malformed")
            event_id = row.get("event_id")
            accessible = row.get("accessible")
            if not isinstance(event_id, str) or not event_id:
                self._hold(store, "HISTORY_RECORD", "record event_id is invalid")
                raise AmbiguousModelCall("history event id is malformed")
            if event_id in event_ids:
                self._hold(store, "HISTORY_RECORD", "record event_id is duplicated")
                raise AmbiguousModelCall("history event id is duplicated")
            if not isinstance(accessible, Mapping):
                self._hold(store, "HISTORY_ACCESS", "record lacks accessible object")
                raise AmbiguousModelCall("history accessible payload is malformed")
            event_ids.append(event_id)
            events.append(
                {"event_id": event_id, "accessible": detached(accessible)}
            )
        if set(event_ids) != {
            row.get("event_id") for row in pending["records"] if isinstance(row, Mapping)
        }:
            self._hold(store, "HISTORY_ORDER", "event ids do not match pending history")
            raise AmbiguousModelCall("history event ids do not match pending batch")
        return detached(pending), records, {
            "batch_id": pending["batch_id"],
            "history_hash": pending["history_hash"],
            "events": events,
        }

    def _active(self, store: Mapping[str, Any]) -> None:
        if store["phase"] == "HELD":
            raise AmbiguousModelCall("cycle is held; ambiguous custody must be resolved")
        if store["model_call"] is not None:
            raise AmbiguousModelCall("cycle has an unresolved model-call reservation")
        if store["phase"] == "COMPLETE":
            raise RecursionRefusal("cycle is complete")

    def _check_expected(self, store: dict[str, Any]) -> dict[str, Any]:
        try:
            current = self._snapshot()
        except Exception as exc:
            self._hold(store, "OWNER_SNAPSHOT", _report(exc))
            raise AmbiguousModelCall(
                f"owner snapshot unavailable: {_report(exc)}"
            ) from exc
        expected = store["expected_owner_state"]
        if detached(current) != detached(expected):
            self._hold(store, "OWNER_STATE_MISMATCH", "owner state changed outside cycle")
            raise AmbiguousModelCall("owner state changed outside cycle")
        return current

    def _snapshot(self) -> dict[str, Any]:
        owner = getattr(self.engine, "owner", None)
        if owner is None:
            raise RecursionRefusal("engine has no owner")
        return _state_document(owner.snapshot())

    def _next_batch_id(self, store: Mapping[str, Any]) -> str:
        return f"batch-{store['next_sequence']:06d}"

    @staticmethod
    def _remember_retrospective(
        store: dict[str, Any], retrospective: Mapping[str, Any]
    ) -> None:
        retro = detached(retrospective)
        store["retrospectives"].append(retro)
        store["proposed_impressions"].append(
            {
                "batch_id": retro["batch_id"],
                "impressions": detached(retro["impressions"]),
            }
        )

    def _hold(self, store: dict[str, Any], code: str, detail: str) -> None:
        store["phase"] = "HELD"
        if isinstance(store.get("model_call"), dict):
            store["model_call"]["status"] = code
        store["last_error"] = {"code": code, "detail": detail}
        self._save(store)

    # -- store I/O ------------------------------------------------------------

    @contextmanager
    def _locked(self) -> Iterator[None]:
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self.store_path.with_name(self.store_path.name + ".lock")
        with lock_path.open("a+", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def _load(self) -> dict[str, Any]:
        if not self.store_path.exists():
            raise CycleStoreError("no cycle store; bootstrap is required")
        try:
            raw = json.loads(self.store_path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise CycleStoreError("cycle store is not valid JSON") from exc
        return _validate_store(raw)

    def _save(self, store: Mapping[str, Any]) -> None:
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            detached(store),
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        fd, name = tempfile.mkstemp(
            prefix=self.store_path.name + ".",
            suffix=".tmp",
            dir=str(self.store_path.parent),
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(name, self.store_path)
            try:
                dir_fd = os.open(self.store_path.parent, os.O_RDONLY)
                try:
                    os.fsync(dir_fd)
                finally:
                    os.close(dir_fd)
            except OSError:
                pass
        except Exception:
            try:
                os.unlink(name)
            except OSError:
                pass
            raise
