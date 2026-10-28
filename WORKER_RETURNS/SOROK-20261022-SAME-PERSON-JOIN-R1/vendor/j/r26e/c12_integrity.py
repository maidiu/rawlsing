"""Owned qualified C12 reading implementation.

Repairs the two preimage defects:
  * episode rows were hashed before the post-hash `episode_id` was appended;
  * world/checkpoint rows hash their exact stored preimage (exclude only `hash`).

The pinned BP4 store is not edited. `QualifiedC12Store` subclasses it and
overrides only verification. The external witness is TEST_ONLY: a same-user
attacker who can rewrite both DB and witness key is outside its protection;
that residual is typed `TRUST_CUSTODY_HOLD`, never claimed as production KMS.
"""
from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from bp1.canon import digest
from bp4.store import C12Store

TEST_ONLY_GRADE = "TEST_ONLY_QUALIFIED_C12_NOT_NATIVE"
TRUST_CUSTODY_HOLD = "TRUST_CUSTODY_HOLD"
EXTERNAL_WITNESS_GRADE = "TEST_ONLY_SAME_USER_EXTERNAL_WITNESS_NOT_SECURITY_BOUNDARY"


class QualifiedC12Store(C12Store):
    """BP4 C12 store with the actual row preimages verified, not self-hashed."""

    def verify(self, branch_id: str) -> dict:
        self.branch(branch_id)
        errors: list[str] = []
        counts: dict[str, int] = {}
        for table, column, drop_episode_id in (
            ("episode", "body", True),
            ("world_event", "body", False),
            ("checkpoint", "state", False),
        ):
            rows = list(self.db.execute(
                f"SELECT seq,{column},hash FROM {table} WHERE branch_id=? ORDER BY seq",
                (branch_id,)))
            counts[table] = len(rows)
            for seq, body, stored_hash in rows:
                parsed = json.loads(body)
                body_hash = parsed.get("hash")
                preimage = {key: value for key, value in parsed.items()
                            if key != "hash"}
                if drop_episode_id:
                    preimage.pop("episode_id", None)
                if body_hash != digest(preimage):
                    errors.append(f"{table}:{seq}:body_hash_mismatch")
                if stored_hash != body_hash:
                    errors.append(f"{table}:{seq}:column_hash_mismatch")
            if [row[0] for row in rows] != list(range(len(rows))):
                errors.append(f"{table}:seq_not_contiguous")
        perceptions = list(self.db.execute(
            "SELECT seq FROM perception WHERE branch_id=? ORDER BY seq", (branch_id,)))
        counts["perception"] = len(perceptions)
        if [row[0] for row in perceptions] != list(range(len(perceptions))):
            errors.append("perception:seq_not_contiguous")
        fork = self._fork_integrity(branch_id)
        errors.extend(fork["errors"])
        return {"ok": not errors, "errors": errors, "counts": counts,
                "branch_id": branch_id, "grade": TEST_ONLY_GRADE,
                "verifier": "R26E_QUALIFIED_C12_PREIMAGE", "fork": fork}


def chain_digest(store: C12Store, branch_id: str) -> str:
    """Ordered identity digest; its trust depends on separate custody."""
    rows: list[list[Any]] = []
    for table, column in (("episode", "body"), ("world_event", "body"),
                          ("checkpoint", "state")):
        for seq, _body, stored_hash in store.db.execute(
                f"SELECT seq,{column},hash FROM {table} WHERE branch_id=? ORDER BY seq",
                (branch_id,)):
            rows.append([table, seq, stored_hash])
    for seq, event_id in store.db.execute(
            "SELECT seq,event_id FROM perception WHERE branch_id=? ORDER BY seq",
            (branch_id,)):
        rows.append(["perception", seq, event_id])
    return digest(rows)


class ExternalCheckpointWitness:
    """TEST_ONLY keyed witness, separate file from the C12 database.

    If the same OS user can rewrite both the DB and this witness/key, deletion
    is not independently detectable. `trust_grade` records that honestly.
    """

    def __init__(self, path: str | Path, key: bytes) -> None:
        self.path = Path(path)
        self.key = key
        self.trust_grade = EXTERNAL_WITNESS_GRADE
        self.security_boundary = False

    def _mac(self, value: dict) -> str:
        return hmac.new(self.key, json.dumps(value, sort_keys=True,
                                             separators=(",", ":")).encode("utf8"),
                        hashlib.sha256).hexdigest()

    def record(self, store: C12Store, branch_id: str) -> dict:
        body = {"branch_id": branch_id, "chain": chain_digest(store, branch_id),
                "grade": self.trust_grade}
        document = {**body, "mac": self._mac(body)}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(document, sort_keys=True), encoding="utf8")
        return document

    def check(self, store: C12Store, branch_id: str) -> dict:
        if not self.path.exists():
            return {"ok": False, "code": "EXTERNAL_WITNESS_ABSENT",
                    "trust_grade": self.trust_grade, "security_boundary": False}
        document = json.loads(self.path.read_text(encoding="utf8"))
        body = {key: document.get(key) for key in ("branch_id", "chain", "grade")}
        if not hmac.compare_digest(document.get("mac", ""), self._mac(body)):
            return {"ok": False, "code": "EXTERNAL_WITNESS_MAC_INVALID",
                    "trust_grade": self.trust_grade, "security_boundary": False}
        current = chain_digest(store, branch_id)
        ok = current == body["chain"]
        return {"ok": ok, "code": "OK" if ok else "CHAIN_DIGEST_MISMATCH",
                "trust_grade": self.trust_grade, "security_boundary": False}

    def residual(self) -> dict:
        return {
            "code": TRUST_CUSTODY_HOLD,
            "reason": ("The witness key and checkpoint live in the same user's "
                       "filesystem trust domain as the C12 database. An attacker "
                       "able to rewrite both defeats the witness; no independent "
                       "security custodian exists in this sourcefree return."),
            "trust_grade": self.trust_grade,
            "production_kms_claim": False,
        }
