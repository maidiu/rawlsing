"""Independent C12 chain verification.

BP4's ``C12Store.verify`` recomputes ``digest(body)`` where ``body`` still
contains its own ``hash`` field, so the recomputation is self-referential and
every non-empty table reports an error. This module verifies the chain the way
the rows were actually written (``digest(body without hash) == body.hash``) and
provides an out-of-band chain digest for deletion detection.

This is a verification add-on over BP4's durable store. It does not modify BP4.
Completeness (that no row was deleted by someone with raw database access) is
only detectable against a separately recorded chain digest; content hashing
alone cannot prove it.
"""
from __future__ import annotations

import json
from typing import Any

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402

TABLES = {
    "episode": ("seq", "hash"),
    "world_event": ("seq", "hash"),
    "checkpoint": ("seq", "hash"),
    "perception": ("seq", "event_id"),
}


def _rows(store, branch_id: str, table: str) -> list[tuple]:
    columns = {
        "episode": "seq, body, hash",
        "world_event": "seq, body, hash",
        "checkpoint": "seq, state AS body, hash",
        "perception": "seq, event_id",
    }[table]
    return list(store.db.execute(
        f"SELECT {columns} FROM {table} WHERE branch_id=? ORDER BY seq",
        (branch_id,)))


def verify_branch_chain(store, branch_id: str) -> dict:
    """Recompute the real row hashes and sequence integrity for one branch."""
    store.branch(branch_id)
    errors: list[str] = []
    counts: dict[str, int] = {}
    for table in ("episode", "world_event", "checkpoint"):
        rows = _rows(store, branch_id, table)
        counts[table] = len(rows)
        for seq, body, stored_hash in rows:
            parsed = json.loads(body)
            body_hash = parsed.get("hash")
            recomputed = digest({key: value for key, value in parsed.items()
                                 if key != "hash"})
            if body_hash != recomputed:
                errors.append(f"{table}:{seq}:body_hash_mismatch")
            if stored_hash != body_hash:
                errors.append(f"{table}:{seq}:column_hash_mismatch")
        if [row[0] for row in rows] != list(range(len(rows))):
            errors.append(f"{table}:seq_not_contiguous")
    perceptions = _rows(store, branch_id, "perception")
    counts["perception"] = len(perceptions)
    if [row[0] for row in perceptions] != list(range(len(perceptions))):
        errors.append("perception:seq_not_contiguous")
    return {"ok": not errors, "errors": errors, "counts": counts,
            "branch_id": branch_id}


def chain_digest(store, branch_id: str) -> str:
    """Ordered digest of every row identity; record it out of band to detect drops."""
    store.branch(branch_id)
    rows: list[list[Any]] = []
    for table in ("episode", "world_event", "checkpoint"):
        for seq, body, stored_hash in _rows(store, branch_id, table):
            rows.append([table, seq, stored_hash])
    for seq, event_id in _rows(store, branch_id, "perception"):
        rows.append(["perception", seq, event_id])
    return digest(rows)


def upstream_verify_defect(store, branch_id: str) -> dict:
    """Show the upstream ``store.verify`` disagreement without modifying BP4."""
    upstream = store.verify(branch_id)
    independent = verify_branch_chain(store, branch_id)
    return {
        "upstream_verify": upstream,
        "independent_verify": independent,
        "upstream_defect": (
            "BP4 C12Store.verify recomputes digest(body) including the body's own "
            "hash field; the rows were written as digest(body without hash)."),
        "agrees": upstream.get("ok") == independent.get("ok"),
    }


__all__ = ["TABLES", "chain_digest", "upstream_verify_defect", "verify_branch_chain"]
