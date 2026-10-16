#!/usr/bin/env python3
"""C07P — TEST_ONLY cross-process custody journal adapter over the pinned OC6 source.

This module does NOT modify, wrap or replace `custody_protocol`. It imports the
pinned native module and persists an authorised escrow event stream to a
filesystem journal, then restores it in a *separate* OS process by replaying the
public `EscrowState` API only.

Design is frozen by 01_PREREGISTERED_PROTOCOL_R1.md at commit 82ba75680.

TEST_ONLY. The journal is an ordinary local mutable file. It is NOT institutional
custody and NOT an externally anchored append-only record. See prereg §5.3.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, fields
from pathlib import Path
from typing import Any, Dict, List, Optional

import custody_protocol as CP

SCHEMA_VERSION = 1
ZERO_PREV = "0" * 64

CAPSULE_FIELDS = tuple(f.name for f in fields(CP.CustodyCapsule))
assert len(CAPSULE_FIELDS) == 18, CAPSULE_FIELDS

KINDS = ("AUTHORIZE", "COMMIT", "UNBLIND", "RELEASE", "EXPOSURE")


class JournalError(Exception):
    """Refusal to read or trust a journal. Never silently repaired."""


class CrashPoint(Exception):
    """Raised by the injected crash hooks. Never caught by journal code."""


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def capsule_to_json(cap: CP.CustodyCapsule) -> Dict[str, Any]:
    """Plain-JSON the 18 declared fields. Never pickles a live object."""
    data = asdict(cap)
    assert set(data) == set(CAPSULE_FIELDS)
    return data


def capsule_from_json(data: Dict[str, Any]) -> CP.CustodyCapsule:
    if set(data) != set(CAPSULE_FIELDS):
        raise JournalError(
            f"capsule field set mismatch: missing={sorted(set(CAPSULE_FIELDS)-set(data))} "
            f"extra={sorted(set(data)-set(CAPSULE_FIELDS))}")
    return CP.CustodyCapsule(**data)


# ---------------------------------------------------------------------------
# Journal record construction and verification
# ---------------------------------------------------------------------------

def build_record(seq: int, kind: str, payload: Dict[str, Any], prev: str) -> Dict[str, Any]:
    if kind not in KINDS:
        raise JournalError(f"unknown journal kind {kind!r}")
    body = {"v": SCHEMA_VERSION, "seq": seq, "kind": kind, "payload": payload, "prev": prev}
    body["rec"] = _sha256(canonical(body))
    return body


def verify_chain(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Verify seq contiguity, prev chaining and every record digest.

    Raises JournalError on the first violation. Never repairs, never skips.
    """
    if not records:
        return {"records": 0, "head": ZERO_PREV, "ok": True}
    prev = ZERO_PREV
    for i, rec in enumerate(records, start=1):
        if rec.get("v") != SCHEMA_VERSION:
            raise JournalError(f"record {i}: bad schema version {rec.get('v')!r}")
        if rec.get("seq") != i:
            raise JournalError(f"record {i}: seq is {rec.get('seq')!r}, expected {i}")
        if rec.get("prev") != prev:
            raise JournalError(
                f"record {i}: prev chain break (have {str(rec.get('prev'))[:12]!r}, "
                f"expected {prev[:12]!r})")
        claimed = rec.get("rec")
        body = {k: v for k, v in rec.items() if k != "rec"}
        recomputed = _sha256(canonical(body))
        if claimed != recomputed:
            raise JournalError(
                f"record {i}: digest mismatch (recorded {str(claimed)[:12]!r}, "
                f"recomputed {recomputed[:12]!r}) — payload tampered")
        prev = claimed
    return {"records": len(records), "head": prev, "ok": True}


# ---------------------------------------------------------------------------
# Atomic journal writer
# ---------------------------------------------------------------------------

def append_records(path: Path, new_records: List[Dict[str, Any]],
                   crash: Optional[str] = None,
                   fsync_file: bool = True,
                   fsync_dir: bool = True,
                   kill_at: Optional[Any] = None) -> Dict[str, Any]:
    """Atomically extend the journal.

    Sequence: write tmp -> flush -> fsync tmp -> [CRASH 1] -> os.replace ->
    [CRASH 2] -> fsync directory -> [CRASH 3].

    `crash` raises CrashPoint at the named point. `kill_at` is called *in place*
    instead and is expected to deliver an uncatchable SIGKILL, so the process
    dies genuinely mid-protocol with no unwinding, no flush and no atexit.
    """
    def die(point: str) -> None:
        if kill_at is not None:
            kill_at(point)
        raise CrashPoint(point)

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_records(path) if path.exists() else []
    prev = existing[-1]["rec"] if existing else ZERO_PREV
    seq0 = len(existing)
    combined = list(existing)
    for offset, rec in enumerate(new_records, start=1):
        combined.append(build_record(seq0 + offset, rec["kind"], rec["payload"], prev))
        prev = combined[-1]["rec"]
    body = "".join(canonical(r) + "\n" for r in combined)

    tmp = path.with_name(path.name + ".tmp")
    limits = {"fsync_file_requested": fsync_file, "fsync_dir_requested": fsync_dir}
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(body)
        fh.flush()
        if fsync_file:
            try:
                os.fsync(fh.fileno())
                limits["fsync_file"] = "SUPPORTED"
            except (OSError, AttributeError) as exc:
                limits["fsync_file"] = f"UNSUPPORTED:{type(exc).__name__}"
        else:
            limits["fsync_file"] = "SKIPPED_BY_CALLER"

    if crash == "1_after_tmp_fsync_before_replace":
        die(crash)

    open(path,'w').write(body)  # MUTANT C: non-atomic
    limits["rename"] = "os_replace_atomic_on_same_directory"

    if crash == "2_after_replace_before_dir_fsync":
        die(crash)

    if fsync_dir:
        try:
            dfd = os.open(str(path.parent), os.O_RDONLY)
            try:
                os.fsync(dfd)
            finally:
                os.close(dfd)
            limits["fsync_dir"] = "SUPPORTED"
        except (OSError, AttributeError) as exc:
            limits["fsync_dir"] = f"UNSUPPORTED:{type(exc).__name__}"
    else:
        limits["fsync_dir"] = "SKIPPED_BY_CALLER"

    if crash == "3_after_dir_fsync":
        die(crash)

    return {"records_total": len(combined), "head": prev, "limits": limits}


def read_records(path: Path) -> List[Dict[str, Any]]:
    """Parse the journal strictly. A truncated or malformed line is a refusal."""
    path = Path(path)
    if not path.exists():
        return []
    raw = path.read_bytes()
    if raw == b"":
        return []
    if not raw.endswith(b"\n"):
        raise JournalError(
            "journal does not end with a newline — truncated trailing record")
    out = []
    for lineno, line in enumerate(raw.decode("utf-8").splitlines(), start=1):
        if not line.strip():
            raise JournalError(f"line {lineno}: blank line inside journal")
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise JournalError(f"line {lineno}: unparseable record ({exc.msg})") from None
    return out


# ---------------------------------------------------------------------------
# Public-API-only persistence driver
# ---------------------------------------------------------------------------

class EscrowJournal:
    """Drives a native `EscrowState` and journals each authorised operation.

    Every mutation goes through the native public API FIRST and is only then
    persisted. If persistence fails the in-memory state is not rolled back by
    this adapter; the caller decides. Restore likewise replays through the
    public API and never assigns to an internal dictionary.
    """

    def __init__(self, path: Path, state: Optional[CP.EscrowState] = None):
        self.path = Path(path)
        self.state = state if state is not None else CP.EscrowState()

    # -- operations ------------------------------------------------------
    def authorize_holder(self, person_id: str, role: CP.Role) -> None:
        self.state.authorize_holder(person_id, role)
        self._persist([{"kind": "AUTHORIZE",
                        "payload": {"person_id": person_id, "role": role.value}}])

    def commit(self, capsule: CP.CustodyCapsule, crash: Optional[str] = None,
               kill_at: Optional[Any] = None) -> None:
        self.state.commit(capsule)
        self._persist([{"kind": "COMMIT",
                        "payload": {"capsule": capsule_to_json(capsule),
                                    "commitment": CP.capsule_envelope_commitment(capsule)}}],
                       crash=crash, kill_at=kill_at)

    def unblind(self, capsule_id: str, holder: str) -> Dict[str, Any]:
        payload = self.state.unblind(capsule_id, holder)
        self._persist([{"kind": "UNBLIND",
                        "payload": {"capsule_id": capsule_id, "holder": holder,
                                    "unblinded_at": payload["unblinded_at"]}}])
        return payload

    def release(self, capsule_id: str) -> None:
        self.state.release(capsule_id)
        self._persist([{"kind": "RELEASE", "payload": {"capsule_id": capsule_id}}])

    def record_exposure(self, capsule_id: str, exposed_to: str, purpose: str) -> None:
        self.state.record_exposure(capsule_id, exposed_to, purpose)
        row = next(r for r in reversed(self.state.exposure_log)
                   if r["capsule_id"] == capsule_id and r["exposed_to"] == exposed_to)
        self._persist([{"kind": "EXPOSURE",
                        "payload": {"capsule_id": capsule_id, "exposed_to": exposed_to,
                                    "purpose": purpose, "exposure_ts": row["ts"]}}])

    def _persist(self, records: List[Dict[str, Any]], crash: Optional[str] = None,
                 kill_at: Optional[Any] = None) -> None:
        append_records(self.path, records, crash=crash, kill_at=kill_at)

    # -- restore ---------------------------------------------------------
    def restore(self) -> Dict[str, Any]:
        """Rebuild escrow by replaying the journal through the public API only."""
        records = read_records(self.path)
        chain = verify_chain(records)
        state = CP.EscrowState()
        applied = 0
        for rec in records:
            kind, p = rec["kind"], rec["payload"]
            if kind == "AUTHORIZE":
                state.authorize_holder(p["person_id"], CP.Role(p["role"]))
            elif kind == "COMMIT":
                cap = capsule_from_json(p["capsule"])
                recomputed = CP.capsule_envelope_commitment(cap)
                if recomputed != p["commitment"]:
                    raise JournalError(
                        f"record {rec['seq']}: forged capsule — recorded commitment "
                        f"{p['commitment'][:12]} != recomputed {recomputed[:12]}")
                state.commit(cap)
            elif kind == "UNBLIND":
                state.unblind(p["capsule_id"], p["holder"])
            elif kind == "RELEASE":
                state.release(p["capsule_id"])
            elif kind == "EXPOSURE":
                state.record_exposure(p["capsule_id"], p["exposed_to"], p["purpose"])
            else:  # pragma: no cover - verify_chain/typing already constrain this
                raise JournalError(f"unknown kind {kind!r}")
            applied += 1
        self.state = state
        return {"applied": applied, "chain": chain,
                "integrity": state.verify_ledger_integrity()}


# ---------------------------------------------------------------------------
# Fingerprint used to compare process A against process B
# ---------------------------------------------------------------------------

def escrow_fingerprint(state: CP.EscrowState) -> Dict[str, Any]:
    """Identity of an escrow that MUST survive a restart.

    Deliberately excludes escrow event timestamps: the native public API
    re-stamps them on replay (prereg hold C07_DEPENDENCY_TS). The capsule
    commitment IS included, because it binds all 18 capsule fields.
    """
    return {
        "committed_ids": sorted(state.committed),
        "commitments": {cid: CP.capsule_envelope_commitment(cap)
                        for cid, cap in sorted(state.committed.items())},
        "capsule_fields": {cid: capsule_to_json(cap)
                           for cid, cap in sorted(state.committed.items())},
        "unblinded_ids": sorted(state.unblinded),
        "unblinded_holders": {cid: state.unblinded[cid]["holder"]
                              for cid in sorted(state.unblinded)},
        "released": sorted(state.released),
        "exposure_rows": sorted(
            [r["capsule_id"], r["exposed_to"], r["purpose"]] for r in state.exposure_log),
        "holder_roles": {k: (v.value if isinstance(v, CP.Role) else None)
                         for k, v in sorted(state.holder_roles.items())},
        "ledger_ops": [r["op"] for r in state.ledger],
        "ledger_seq": [r["seq"] for r in state.ledger],
        "integrity": state.verify_ledger_integrity(),
    }
