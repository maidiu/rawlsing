"""Read the actual committed S36 response/receipt from the persistent C9 DB.

The reader is shared by both lawful source histories. It does not return the
C12 episode or sidecar summary as the primary result: it opens the committed C9
SQLite database read-only, reads the exact response and receipt rows, validates
their sealed hashes, and only then cross-checks the C12/session bindings.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Mapping

from .bootstrap import install

install()

from candidate import valid  # noqa: E402


class S37ReadRefusal(ValueError):
    """The persistent session cannot produce the actual committed S36 rows."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def _loads(row, code: str, record_hash: str) -> dict:
    if row is None:
        raise S37ReadRefusal(code)
    try:
        value = json.loads(row[0])
    except (TypeError, ValueError) as exc:
        raise S37ReadRefusal(code + "_UNREADABLE", str(exc)) from exc
    if not isinstance(value, dict):
        raise S37ReadRefusal(code + "_NOT_OBJECT")
    value.setdefault("hash", record_hash)
    return value


def _read_rows(c9_path: Path, response_ref: str, receipt_ref: str) -> tuple[dict, dict, int]:
    if not c9_path.is_file():
        raise S37ReadRefusal("C9_DB_MISSING", str(c9_path))
    try:
        conn = sqlite3.connect(f"file:{c9_path}?mode=ro", uri=True)
    except sqlite3.Error as exc:
        raise S37ReadRefusal("C9_DB_UNREADABLE", str(exc)) from exc
    try:
        response_row = conn.execute(
            "SELECT body FROM response WHERE hash=?", (response_ref,)
        ).fetchone()
        receipt_row = conn.execute(
            "SELECT body FROM receipt WHERE hash=?", (receipt_ref,)
        ).fetchone()
        target_rows = conn.execute(
            "SELECT count(*) FROM target_state"
        ).fetchone()[0]
    except sqlite3.Error as exc:
        raise S37ReadRefusal("C9_ROW_READ_FAILED", str(exc)) from exc
    finally:
        conn.close()
    return (
        _loads(response_row, "C9_RESPONSE_ROW_MISSING", response_ref),
        _loads(receipt_row, "C9_RECEIPT_ROW_MISSING", receipt_ref),
        int(target_rows),
    )


def read_committed_s36(
    *,
    c9_path: Path,
    s36_binding: Mapping[str, Any],
    c8_binding: Mapping[str, Any],
    source: Mapping[str, Any],
    product,
    branch_id: str,
    meta: Mapping[str, Any],
    sidecar: Mapping[str, Any],
) -> dict:
    """Read and validate the exact C9 response/receipt for this session."""
    response_ref = str(s36_binding.get("response_ref", ""))
    receipt_ref = str(s36_binding.get("c9_receipt_hash", ""))
    if not response_ref or not receipt_ref:
        raise S37ReadRefusal("C9_BINDING_INCOMPLETE")
    response, receipt, target_rows = _read_rows(c9_path, response_ref, receipt_ref)

    if not valid(response):
        raise S37ReadRefusal("C9_RESPONSE_UNSEALED")
    if not valid(receipt):
        raise S37ReadRefusal("C9_RECEIPT_UNSEALED")
    if response.get("event_ref") != s36_binding.get("e1_event_hash"):
        raise S37ReadRefusal("C9_RESPONSE_EVENT_MISMATCH")
    if response.get("receipt_hash") != s36_binding.get("response_receipt_hash"):
        raise S37ReadRefusal("C9_RESPONSE_RECEIPT_MISMATCH")
    if receipt.get("response_ref") != response_ref:
        raise S37ReadRefusal("C9_RECEIPT_RESPONSE_REF_MISMATCH")
    if receipt.get("event_ref") != s36_binding.get("e1_event_hash"):
        raise S37ReadRefusal("C9_RECEIPT_EVENT_MISMATCH")
    if receipt.get("target_branch") != "NO_CHANGE":
        raise S37ReadRefusal("C9_TARGET_NOT_NO_CHANGE")
    if receipt.get("target_reason") != "NO_PROPOSAL":
        raise S37ReadRefusal("C9_TARGET_NOT_NO_PROPOSAL")
    if receipt.get("target_id", "") != "" or receipt.get("record_hash", "") != "":
        raise S37ReadRefusal("C9_TARGET_PRESENT")
    if target_rows != 0:
        raise S37ReadRefusal("C9_TARGET_STATE_NOT_EMPTY", str(target_rows))
    if response.get("target_proposal_ref", "") != "":
        raise S37ReadRefusal("C9_RESPONSE_TARGET_PROPOSAL_PRESENT")

    s35 = response.get("s35_receipt")
    if not isinstance(s35, Mapping) or not valid(dict(s35)):
        raise S37ReadRefusal("S36_RECEIPT_MISSING_OR_UNSEALED")
    s35 = dict(s35)
    if s35.get("event_ref") != s36_binding.get("e1_event_hash"):
        raise S37ReadRefusal("S36_RECEIPT_EVENT_MISMATCH")
    if s35.get("actor_id") != s36_binding.get("actor_id"):
        raise S37ReadRefusal("S36_RECEIPT_ACTOR_MISMATCH")
    if s35.get("target_proposals") != []:
        raise S37ReadRefusal("S36_RECEIPT_TARGET_PROPOSALS_PRESENT")
    if s35.get("access_source_ref") != s36_binding.get("access_source_ref"):
        raise S37ReadRefusal("S36_ACCESS_REF_MISMATCH")
    if s35.get("access_source_hash") != s36_binding.get("access_source_hash"):
        raise S37ReadRefusal("S36_ACCESS_HASH_MISMATCH")
    if s35.get("response_source_ref") != s36_binding.get("response_source_ref"):
        raise S37ReadRefusal("S36_RESPONSE_REF_MISMATCH")
    if s35.get("response_source_hash") != s36_binding.get("response_source_hash"):
        raise S37ReadRefusal("S36_RESPONSE_HASH_MISMATCH")
    if s35.get("response_kind") != s36_binding.get("response_kind"):
        raise S37ReadRefusal("S36_RESPONSE_KIND_MISMATCH")
    if s35.get("outcome") not in {
        "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
        "OBSERVED_CURRENT_REFUSAL",
        "RECEIVABLE_NO_OBSERVED_UPTAKE",
        "UNKNOWN_RECEIVABILITY",
        "AMBIGUOUS_CONTRADICTORY",
    }:
        raise S37ReadRefusal("S36_OUTCOME_UNKNOWN")

    episode = product.s36_episode_body() or {}
    episode_s36 = episode.get("s36") or {}
    if episode_s36.get("response_ref") != response_ref:
        raise S37ReadRefusal("C12_EPISODE_RESPONSE_REF_MISMATCH")
    if episode_s36.get("c9_receipt_hash") != receipt_ref:
        raise S37ReadRefusal("C12_EPISODE_RECEIPT_MISMATCH")
    if episode.get("source") != dict(source):
        raise S37ReadRefusal("C12_EPISODE_SOURCE_MISMATCH")
    if episode.get("c8") != dict(c8_binding):
        raise S37ReadRefusal("C12_EPISODE_C8_MISMATCH")
    if dict(sidecar.get("s36") or {}) != dict(meta.get("s36") or {}):
        raise S37ReadRefusal("SIDECAR_S36_SUMMARY_MISMATCH")

    return {
        "schema": "SOROK_S37_COMMITTED_S36_READ@1",
        "grade": "TEST_ONLY_SOURCEFREE_NOT_NATIVE",
        "status": "OK",
        "native": False,
        "c9_db_path": str(c9_path),
        "response_ref": response_ref,
        "response_receipt_hash": response.get("receipt_hash", ""),
        "c9_receipt_hash": receipt_ref,
        "response": response,
        "receipt": receipt,
        "s35_receipt": s35,
        "outcome": s35.get("outcome"),
        "target_branch": receipt.get("target_branch"),
        "target_reason": receipt.get("target_reason"),
        "target_id": receipt.get("target_id", ""),
        "target_proposals": list(s35.get("target_proposals", [])),
        "target_state_rows": target_rows,
        "e1_event_hash": s36_binding.get("e1_event_hash"),
        "e1_event_id": s36_binding.get("e1_event_id"),
        "actor_id": s36_binding.get("actor_id"),
        "c8_state_digest": c8_binding.get("c8_state_digest"),
        "source_operation": source.get("b_operation"),
        "source_b_event_hash": source.get("b_event_hash"),
        "material_access": s36_binding.get("material_access"),
        "response_kind": s35.get("response_kind"),
        "source_preserved": True,
        "product_model_calls": 0,
    }


__all__ = ["S37ReadRefusal", "read_committed_s36"]
