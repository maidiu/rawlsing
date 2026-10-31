"""SOROK BP3 — exclusive C8 writer and external monotonic anchor (TEST_ONLY).

The accepted OUT9 `outbox_prototype.Journal.commit` / `admit_and_queue` remain
legally importable. This candidate installs an executable gate on those exact
class methods at import, so a process that loads the candidate cannot use the
old writer to replace an acknowledged journal. It then provides a keyed,
compare-and-append writer whose append proof is bound to an independently held
monotonic anchor.

This is a sourcefree TEST_ONLY security candidate. It is NOT production key
custody, NOT an ADP019 admission, NOT a native actor and NOT a C11 weld.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

HERE = Path(__file__).resolve().parent
VENDOR = HERE / "vendor"
if str(VENDOR) not in sys.path:
    sys.path.insert(0, str(VENDOR))

import outbox_prototype as op  # noqa: E402
import c8o_trusted_outbox as c8o  # noqa: E402

SCHEMA = "C8_BP3_EXCLUSIVE_APPEND@1"
DOMAIN = "C8_BP3_TEST_ONLY"
TEST_ONLY_GRADE = "TEST_ONLY_EXTERNAL_KEY_AND_ANCHOR_NOT_NATIVE"


def _canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash(value) -> str:
    return hashlib.sha256(_canonical(value).encode("utf8")).hexdigest()


def _mac(key: bytes, value) -> str:
    return hmac.new(key, _canonical(value).encode("utf8"), hashlib.sha256).hexdigest()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


class ExclusiveWriteRefused(Exception):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


class LegacyWriterRouteClosed(ExclusiveWriteRefused):
    def __init__(self, route: str) -> None:
        super().__init__("LEGACY_WRITER_ROUTE_CLOSED", route)
        self.route = route


class KeyCustodyNotExternal(ExclusiveWriteRefused):
    pass


class CapabilityRefused(ExclusiveWriteRefused):
    pass


class AnchorUnavailable(ExclusiveWriteRefused):
    pass


class AnchorRollbackDetected(ExclusiveWriteRefused):
    def __init__(self, observed, current) -> None:
        super().__init__("ANCHOR_ROLLBACK_DETECTED", f"{observed} < {current}")
        self.observed = observed
        self.current = current


class KeyedProofInvalid(ExclusiveWriteRefused):
    pass


def _closed_commit(self, *args, **kwargs):
    raise LegacyWriterRouteClosed("Journal.commit")


def _closed_admit(self, *args, **kwargs):
    raise LegacyWriterRouteClosed("Journal.admit_and_queue")


def install_exclusive_gate() -> bool:
    """Close the accepted legacy class write methods in this process.

    This is an executable compatibility gate, not a native cutover. The original
    module bytes are untouched; a process that never imports this candidate can
    still call the old writer. D1 remains an accepted-custodian decision.
    """
    if getattr(op.Journal, "_bp3_exclusive_gate", False):
        return False
    op.Journal.commit = _closed_commit
    op.Journal.admit_and_queue = _closed_admit
    op.Journal._bp3_exclusive_gate = True
    return True


@dataclass(frozen=True)
class WriterKeyStore:
    path: Path
    key_id: str
    key: bytes

    @classmethod
    def load(cls, path, key_id: str) -> "WriterKeyStore":
        raw = json.loads(Path(path).read_text(encoding="utf8"))
        if raw.get("key_id") != key_id:
            raise CapabilityRefused("KEY_ID_MISMATCH")
        import base64
        key = base64.b64decode(raw["key_b64"])
        if len(key) < 32:
            raise CapabilityRefused("KEY_TOO_SHORT")
        return cls(Path(path), key_id, key)

    def assert_external(self, journal_path) -> None:
        try:
            self.path.resolve().relative_to(Path(journal_path).resolve().parent)
        except ValueError:
            return
        raise KeyCustodyNotExternal("KEY_STORE_INSIDE_JOURNAL_DIRECTORY")


def journal_identity(path) -> str:
    return _hash({"domain": DOMAIN, "journal_path": str(Path(path).resolve())})


@dataclass(frozen=True)
class KeyedCapability:
    writer_id: str
    journal_id: str
    role: str
    issued_at: str
    expires_at: str
    nonce: str
    signature: str = ""

    def _body(self) -> dict:
        return {
            "domain": DOMAIN + ":capability",
            "writer_id": self.writer_id,
            "journal_id": self.journal_id,
            "role": self.role,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "nonce": self.nonce,
        }

    @classmethod
    def issue(cls, store: WriterKeyStore, journal_id: str, writer_id: str, *,
              role: str = "EXCLUSIVE_APPEND", ttl_seconds: int = 3600) -> "KeyedCapability":
        now = _now()
        cap = cls(writer_id, journal_id, role, _iso(now),
                  _iso(now.fromtimestamp(now.timestamp() + ttl_seconds, timezone.utc)),
                  os.urandom(16).hex())
        return cls(**{**cap.__dict__, "signature": _mac(store.key, cap._body())})

    def verify(self, store: WriterKeyStore, journal_id: str, *, now: Optional[datetime] = None) -> None:
        if self.journal_id != journal_id:
            raise CapabilityRefused("CAPABILITY_WRONG_JOURNAL")
        if self.role != "EXCLUSIVE_APPEND":
            raise CapabilityRefused("CAPABILITY_WRONG_ROLE")
        moment = now or _now()
        try:
            expiry = datetime.fromisoformat(self.expires_at)
        except ValueError:
            raise CapabilityRefused("CAPABILITY_EXPIRY_MALFORMED")
        if moment > expiry:
            raise CapabilityRefused("CAPABILITY_EXPIRED")
        expected = _mac(store.key, self._body())
        if not hmac.compare_digest(expected, self.signature):
            raise CapabilityRefused("CAPABILITY_SIGNATURE_INVALID")


@dataclass
class KeyedMonotonicAnchor:
    """TEST_ONLY external witness with a separately held watermark.

    The anchor log and watermark live OUTSIDE the journal directory. They are
    keyed with a key held by the separate anchor/key store. This is a test
    fixture, not native key custody; D2 remains unissued.
    """
    log_path: Path
    watermark_path: Path
    store: WriterKeyStore
    grade: str = TEST_ONLY_GRADE
    last_seq: int = 0
    last_receipt: Optional[str] = None

    def _rows(self) -> list:
        if not self.log_path.exists():
            return []
        data = json.loads(self.log_path.read_text(encoding="utf8"))
        rows = data.get("rows", [])
        for row in rows:
            body = {k: row.get(k) for k in ("seq", "version", "receipt_id", "prev")}
            if row.get("mac") != _mac(self.store.key, {"domain": DOMAIN + ":anchor-row", **body}):
                raise AnchorUnavailable("ANCHOR_ROW_MAC_INVALID")
        return rows

    def _write(self, rows: list, seq: int, version: int, receipt_id: str) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.watermark_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = Path(str(self.log_path) + ".tmp")
        tmp.write_text(_canonical({"rows": rows}), encoding="utf8")
        os.replace(tmp, self.log_path)
        body = {"seq": seq, "version": version, "receipt_id": receipt_id}
        witness = {**body, "mac": _mac(self.store.key, {"domain": DOMAIN + ":anchor-watermark", **body})}
        tmpw = Path(str(self.watermark_path) + ".tmp")
        tmpw.write_text(_canonical(witness), encoding="utf8")
        os.replace(tmpw, self.watermark_path)

    def observe(self, writer_version: int, receipt_id: str) -> str:
        rows = self._rows()
        if rows:
            last = rows[-1]
            if writer_version < last["version"] or (
                    writer_version == last["version"] and receipt_id != last["receipt_id"]):
                raise AnchorRollbackDetected((last["version"], last["receipt_id"]),
                                             (writer_version, receipt_id))
        seq = len(rows)
        prev = rows[-1]["mac"] if rows else None
        body = {"seq": seq, "version": writer_version, "receipt_id": receipt_id, "prev": prev}
        row = {**body, "mac": _mac(self.store.key, {"domain": DOMAIN + ":anchor-row", **body})}
        rows.append(row)
        self._write(rows, seq, writer_version, receipt_id)
        self.last_seq = seq
        self.last_receipt = receipt_id
        return _hash({"anchor_seq": seq, "receipt_id": receipt_id})

    def check(self, writer_version: int, receipt_id: str) -> None:
        if not self.watermark_path.exists():
            raise AnchorUnavailable("ANCHOR_WATERMARK_MISSING")
        witness = json.loads(self.watermark_path.read_text(encoding="utf8"))
        body = {k: witness.get(k) for k in ("seq", "version", "receipt_id")}
        if witness.get("mac") != _mac(self.store.key, {"domain": DOMAIN + ":anchor-watermark", **body}):
            raise AnchorUnavailable("ANCHOR_WATERMARK_MAC_INVALID")
        if writer_version < witness["version"] or (
                writer_version == witness["version"] and receipt_id != witness["receipt_id"]):
            raise AnchorRollbackDetected((witness["version"], witness["receipt_id"]),
                                         (writer_version, receipt_id))
        rows = self._rows()
        if not rows or rows[witness["seq"]]["receipt_id"] != witness["receipt_id"]:
            raise AnchorUnavailable("ANCHOR_LOG_MISSING_WITNESS_ROW")


@dataclass
class ExclusiveCommitReceipt:
    journal_id: str
    c8o: dict
    anchor_seq: int
    proof: dict

    def to_json(self) -> dict:
        return {"schema": SCHEMA, "journal_id": self.journal_id,
                "c8o": self.c8o, "anchor_seq": self.anchor_seq, "proof": self.proof,
                "grade": TEST_ONLY_GRADE}


class ExclusiveJournal(c8o.C8OccurrenceJournal):
    """Keyed compare-and-append journal over the accepted OUT9 occurrence state."""

    def __init__(self, path, *, store: WriterKeyStore, anchor: KeyedMonotonicAnchor,
                 lock_timeout: float = 15.0) -> None:
        store.assert_external(path)
        self.store = store
        self.journal_id = journal_identity(path)
        self.keyed_anchor = anchor
        super().__init__(path, lock_timeout=lock_timeout, anchor=anchor,
                         capability_verifier=c8o.UnkeyedFormatCapabilityVerifier())

    def _c8o_capability(self, capability: KeyedCapability) -> c8o.WriterCapability:
        return c8o.WriterCapability(capability.writer_id, capability.nonce,
                                    "TEST_ONLY_KEYED_CAPABILITY:" + capability.journal_id)

    def _proof(self, receipt: c8o.C8CommitReceipt, capability: KeyedCapability) -> dict:
        anchor_row = self.keyed_anchor._rows()[-1]
        body = {
            "domain": DOMAIN + ":append-proof",
            "journal_id": self.journal_id,
            "writer_id": capability.writer_id,
            "role": capability.role,
            "capability_nonce": capability.nonce,
            "writer_version": receipt.writer_version,
            "receipt_id": receipt.receipt_id,
            "state_digest": receipt.state_digest,
            "version_state_digest": receipt.version_state_digest,
            "anchor_seq": anchor_row["seq"],
            "anchor_version": anchor_row["version"],
            "anchor_receipt_id": anchor_row["receipt_id"],
            "anchor_prev": anchor_row["prev"],
        }
        return {**body, "mac": _mac(self.store.key, body)}

    def commit(self, p, expected_version: int, *, capability: KeyedCapability,
               crash_boundary: Optional[str] = None,
               require_trusted_time: bool = False) -> ExclusiveCommitReceipt:
        if not isinstance(capability, KeyedCapability):
            raise CapabilityRefused("KEYED_CAPABILITY_REQUIRED")
        capability.verify(self.store, self.journal_id)
        c8cap = self._c8o_capability(capability)
        receipt = super().commit(p, expected_version, capability=c8cap,
                                 crash_boundary=crash_boundary,
                                 require_trusted_time=require_trusted_time)
        proof = self._proof(receipt, capability)
        out = ExclusiveCommitReceipt(self.journal_id, receipt.to_json(),
                                     proof["anchor_seq"], proof)
        self._write_proof(out)
        return out

    def _proof_path(self) -> Path:
        return Path(str(self.path) + ".bp3proof")

    def _write_proof(self, receipt: ExclusiveCommitReceipt) -> None:
        tmp = Path(str(self._proof_path()) + ".tmp")
        tmp.write_text(_canonical(receipt.to_json()), encoding="utf8")
        os.replace(tmp, self._proof_path())

    def append_occurrence(self, candidate: dict, *, capability: KeyedCapability,
                          viewer_id: Optional[str] = None,
                          expected_version: Optional[int] = None):
        p, version = self.recover()
        if expected_version is not None and expected_version != version:
            raise c8o.StaleJournalConflict(expected_version, version, self.path)
        before_count = p.ledger.count()
        event = p.ledger.admit(candidate)
        if event is None:
            return None, p.ledger.last_refusal, None
        if p.ledger.count() == before_count:
            return None, "DUPLICATE_NO_CHANGE", None
        eid = event["occurrence_id"]
        if viewer_id is not None and not p.outbox.authorize_viewer(eid, viewer_id):
            return None, "VIEWER_NOT_AUTHORIZED", None
        state = p.outbox.emit(eid, viewer_id=viewer_id)
        if str(state) == "NOT_SENT":
            return None, "EMISSION_REFUSED", None
        if viewer_id is not None and p.outbox.emit_to(eid, viewer_id) is None:
            return None, "CLIENT_INTENT_REFUSED", None
        return event, None, self.commit(p, version, capability=capability)

    def verify_journal(self) -> dict:
        proof_path = self._proof_path()
        if not proof_path.exists():
            raise KeyedProofInvalid("PROOF_SIDECAR_MISSING")
        proof_doc = json.loads(proof_path.read_text(encoding="utf8"))
        if proof_doc.get("schema") != SCHEMA:
            raise KeyedProofInvalid("PROOF_SCHEMA_INVALID")
        custody = self.classify()
        if custody.status != "VERSIONED_VALID":
            raise KeyedProofInvalid("JOURNAL_NOT_VERSIONED_VALID:" + custody.status)
        receipt_raw = json.loads(self.path.read_text(encoding="utf8"))
        proof = proof_doc.get("proof") or {}
        body = {k: proof.get(k) for k in (
            "domain", "journal_id", "writer_id", "role", "capability_nonce",
            "writer_version", "receipt_id", "state_digest", "version_state_digest",
            "anchor_seq", "anchor_version", "anchor_receipt_id", "anchor_prev")}
        if proof.get("mac") != _mac(self.store.key, body):
            raise KeyedProofInvalid("PROOF_MAC_INVALID")
        if body["journal_id"] != self.journal_id:
            raise KeyedProofInvalid("PROOF_WRONG_JOURNAL")
        if body["receipt_id"] != receipt_raw.get("commit_receipt_id"):
            raise KeyedProofInvalid("PROOF_RECEIPT_MISMATCH")
        if body["state_digest"] != receipt_raw.get("state_digest"):
            raise KeyedProofInvalid("PROOF_STATE_MISMATCH")
        if body["writer_version"] != receipt_raw.get("writer_version"):
            raise KeyedProofInvalid("PROOF_VERSION_MISMATCH")
        self.keyed_anchor.check(body["writer_version"], body["receipt_id"])
        return proof_doc


install_exclusive_gate()
