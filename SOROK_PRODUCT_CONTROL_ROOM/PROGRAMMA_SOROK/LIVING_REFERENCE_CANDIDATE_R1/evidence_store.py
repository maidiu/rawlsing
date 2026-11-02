#!/usr/bin/env python3
"""Append-only canonical evidence/change journal for PROGRAMMA SOROK.

The journal is the canonical operating evidence stream.  State, snapshot and
views are deterministic reductions over the journal plus frozen source-backed
seeds.  Duplicate event identities are idempotent.  A local hash is an integrity
check, not external custody.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
from pathlib import Path
from typing import Any

SCHEMA = "SOROK_PROGRAMMA_EVIDENCE_JOURNAL@1"
GENESIS = "GENESIS"


class JournalError(ValueError):
    """The journal is missing, truncated, tampered or append-conflicted."""


class JournalRegression(JournalError):
    """A valid journal prefix is older than the known derived-state marker."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _body(event: dict) -> dict:
    return {k: v for k, v in event.items() if k not in {"event_id", "prev_event_hash", "sequence", "schema"}}


def event_identity(body: dict) -> str:
    return digest(_body(body))


def _head_line(event: dict) -> dict:
    return {
        "schema": SCHEMA,
        "event_id": event["event_id"],
        "sequence": event["sequence"],
        "prev_event_hash": event["prev_event_hash"],
        "kind": event.get("kind"),
        "created_at": event.get("created_at"),
    }


def read_journal(path: Path) -> list[dict]:
    """Read and verify the complete hash chain, failing closed on tamper/truncation."""
    target = Path(path)
    if not target.exists():
        return []
    raw = target.read_text(encoding="utf-8")
    if not raw:
        return []
    if not raw.endswith("\n"):
        raise JournalError("JOURNAL_TRUNCATED_OR_INCOMPLETE_LAST_LINE")
    events: list[dict] = []
    previous = GENESIS
    for index, line in enumerate(raw.splitlines(), start=1):
        if not line.strip():
            raise JournalError(f"JOURNAL_BLANK_LINE:{index}")
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise JournalError(f"JOURNAL_INVALID_JSON:{index}:{error}") from error
        if event.get("schema") != SCHEMA:
            raise JournalError(f"JOURNAL_SCHEMA_MISMATCH:{index}")
        if event.get("sequence") != index:
            raise JournalError(f"JOURNAL_SEQUENCE_MISMATCH:{index}")
        if event.get("prev_event_hash") != previous:
            raise JournalError(f"JOURNAL_PREV_HASH_MISMATCH:{index}")
        if event.get("event_id") != event_identity(event):
            raise JournalError(f"JOURNAL_EVENT_HASH_MISMATCH:{index}")
        events.append(event)
        previous = event["event_id"]
    return events


def journal_head(path: Path) -> str:
    events = read_journal(path)
    return events[-1]["event_id"] if events else GENESIS


def append_event(
    path: Path,
    body: dict,
    *,
    expected_head: str | None = None,
) -> dict:
    """Append one canonical event under an exclusive lock.

    A stale ``expected_head`` is reported, not silently overwritten.  The event
    is still appended because canonical evidence must not be lost on a stale
    concurrent writer; the caller then replays the complete journal.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lock_path = target.with_name(target.name + ".lock")
    with lock_path.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            events = read_journal(target)
            head = events[-1]["event_id"] if events else GENESIS
            candidate = dict(body)
            candidate["sequence"] = len(events) + 1
            candidate["prev_event_hash"] = head
            candidate["schema"] = SCHEMA
            candidate["event_id"] = event_identity(candidate)
            duplicate = next((e for e in events if e["event_id"] == candidate["event_id"]), None)
            if duplicate is not None:
                return {
                    "status": "DUPLICATE_EVENT_IDEMPOTENT",
                    "event": duplicate,
                    "head": head,
                    "stale_expected_head": bool(expected_head is not None and expected_head != head),
                    "expected_head": expected_head,
                }
            line = (canonical_json(candidate) + "\n").encode("utf-8")
            with target.open("ab") as handle:
                handle.write(line)
                handle.flush()
                os.fsync(handle.fileno())
            return {
                "status": "EVENT_APPENDED",
                "event": candidate,
                "head": candidate["event_id"],
                "stale_expected_head": bool(expected_head is not None and expected_head != head),
                "expected_head": expected_head,
            }
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def event_summary(events: list[dict]) -> dict:
    return {
        "schema": SCHEMA,
        "count": len(events),
        "head": events[-1]["event_id"] if events else GENESIS,
        "kinds": [e.get("kind") for e in events],
        "events": [_head_line(e) for e in events],
    }
