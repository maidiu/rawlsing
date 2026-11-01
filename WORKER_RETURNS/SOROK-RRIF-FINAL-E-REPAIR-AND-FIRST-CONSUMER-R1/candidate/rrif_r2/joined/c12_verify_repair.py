"""Repaired independent C12 chain verifier.

The vendored ``bp2p4.c12_verify`` helper hashes the episode body including the
post-hash ``episode_id`` field, so a legitimate intact episode fails. This
module preserves the vendored helper as exact source donor and supplies the
correct same-assertion verifier: ``digest(body without hash and without
episode_id)`` for episodes, and ``digest(body without hash)`` for the other
preimage tables.
"""
from __future__ import annotations

import json
from typing import Any

from bp1.canon import digest
from bp2p4.c12_verify import _rows


def verify_branch_chain_repaired(store, branch_id: str) -> dict[str, Any]:
    """Return GREEN only for intact preimages; RED for tamper/restore court."""
    store.branch(branch_id)
    errors: list[str] = []
    counts: dict[str, int] = {}
    for table in ("episode", "world_event", "checkpoint"):
        rows = _rows(store, branch_id, table)
        counts[table] = len(rows)
        for seq, body, stored_hash in rows:
            parsed = json.loads(body)
            body_hash = parsed.get("hash")
            preimage = {key: value for key, value in parsed.items()
                        if key != "hash"}
            if table == "episode":
                preimage.pop("episode_id", None)
            if body_hash != digest(preimage):
                errors.append(f"{table}:{seq}:body_hash_mismatch")
            if stored_hash != body_hash:
                errors.append(f"{table}:{seq}:column_hash_mismatch")
        if [row[0] for row in rows] != list(range(len(rows))):
            errors.append(f"{table}:seq_not_contiguous")
    perceptions = _rows(store, branch_id, "perception")
    counts["perception"] = len(perceptions)
    if [row[0] for row in perceptions] != list(range(len(perceptions))):
        errors.append("perception:seq_not_contiguous")
    return {
        "ok": not errors,
        "errors": errors,
        "counts": counts,
        "branch_id": branch_id,
        "verifier": "RRIF_E_REPAIRED_C12_PREIMAGE@1",
        "self_hash_only": True,
        "external_owner_anchor": "OWNER_ANCHOR_REQUIRED",
    }


def upstream_defect_is_reproducible(store, branch_id: str) -> dict[str, Any]:
    """Report the preserved vendored defect without treating it as acceptance."""
    from bp2p4.c12_verify import verify_branch_chain

    upstream = verify_branch_chain(store, branch_id)
    repaired = verify_branch_chain_repaired(store, branch_id)
    return {
        "upstream_ok": upstream["ok"],
        "upstream_errors": upstream["errors"],
        "repaired_ok": repaired["ok"],
        "repaired_errors": repaired["errors"],
        "upstream_known_defect": "episode_id was added after the hashed preimage",
    }


__all__ = ["upstream_defect_is_reproducible", "verify_branch_chain_repaired"]
