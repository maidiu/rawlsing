"""SOROK C8O — maximal lawful source-free C8 occurrence/journal trusted-write boundary.

TEST_ONLY owner-custody candidate over the ACCEPTED OUT9 `outbox_prototype.Journal`
source (blob 331840768ce0b5f6f73e5e93094ca0d217ddaebf). The accepted source is not
modified, subclass-monkeypatched or replaced. This module adds a separate,
explicitly-selected custody discipline on top of it:

1. INTERPROCESS TRANSACTION LOCK - exclusive `fcntl.flock` on `<journal>.lock`
   held across version check, validation and publication.
2. VERSIONED COMPARE-AND-APPEND - `writer_version` is sealed together with the
   state, the acknowledged ledger prefix, the writer identity and the effective
   clock into `version_state_digest`; a stale holder is refused with typed
   `StaleJournalConflict`.
3. VERSION-STATE CUSTODY - a nonexistent file is the ONLY valid genesis version
   zero. Missing, malformed, injected, noncanonical or legacy-overwritten
   envelopes are typed refusals, never silent version-zero coercion.
4. ACKNOWLEDGED LEDGER PREFIX INTEGRITY - a replacement may extend but never
   rewrite the acknowledged prefix of committed occurrences.
5. TRUE WRITER CAPABILITY SEPARATION - commits require a `WriterCapability`
   object. The capability fingerprint recorded in the receipt is an UNKEYED
   hash. Without a separately trusted issuer/verifier it is NOT writer
   authentication and NOT a signature; a court case exists to falsify any
   such reading.
6. EXTERNAL VERSION ANCHOR INTERFACE - rollback to an earlier byte-valid
   receipt is undetectable by any recomputable unkeyed digest. Detection needs
   a separately trusted monotonic anchor. Without one this module raises typed
   `TrustedAnchorUnissued` and refuses any authenticated anti-rollback claim.

RESIDUAL (typed, not closed here): the ACCEPTED `Journal.commit` remains a
legally callable writer of the same path. It takes no lock and no version
precondition and its receipt carries no version envelope at all. This module
DETECTS that bypass after it occurs (typed `LegacyWriterBypassDetected`); it
CANNOT prevent already-erased state and cannot withdraw the old writer's
permission. Authority forms: `C8_TRUSTED_WRITE_OWNER_HELD`,
`LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED`, `C8_TRUSTED_ANCHOR_UNISSUED`,
`C8_CAPABILITY_TRUST_ANCHOR_UNISSUED`, security claim `NOT_PROVED`.

NOT an ADP019 issuer. NOT a native actor/event admission. NOT production
installation. NO trusted-writer issuance. NO keyed receipt authenticity.
"""
from __future__ import annotations

import errno
import fcntl
import json
import os
import signal
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from outbox_prototype import Journal, make_prototype, _canonical, _hash

SCHEMA = "OUTBOX_F2_JOURNAL_V2"

C8_TRUSTED_WRITE_OWNER_HELD = "C8_TRUSTED_WRITE_OWNER_HELD"
LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED = "LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED"
C8_TRUSTED_ANCHOR_UNISSUED = "C8_TRUSTED_ANCHOR_UNISSUED"
C8_CAPABILITY_TRUST_ANCHOR_UNISSUED = "C8_CAPABILITY_TRUST_ANCHOR_UNISSUED"
C8_EFFECTIVE_CLOCK_SOURCE_UNTRUSTED = "C8_EFFECTIVE_CLOCK_SOURCE_UNTRUSTED"
SECURITY_CLAIM_NOT_PROVED = "NOT_PROVED"
CAPABILITY_FORMAT_ONLY_NOT_AUTHENTICATION = "CAPABILITY_FORMAT_ONLY_NOT_AUTHENTICATION"
ANTI_ROLLBACK_WITHOUT_ANCHOR = "ANTI_ROLLBACK_WITHOUT_ANCHOR_NOT_PROVED"

CRASH_BOUNDARIES = (
    "BEFORE_RENAME",
    "AFTER_COMMIT",
    "SIGKILL_BEFORE_RENAME",
    "SIGKILL_AFTER_COMMIT",
)


class StaleJournalConflict(Exception):
    def __init__(self, expected: int, actual: int, path) -> None:
        super().__init__(
            f"STALE_JOURNAL_CONFLICT expected_version={expected} actual_version={actual} path={path}"
        )
        self.expected = expected
        self.actual = actual
        self.code = "STALE_JOURNAL_CONFLICT"


class VersionStateUnreadable(ValueError):
    def __init__(self, path, reason: str) -> None:
        super().__init__(f"VERSION_STATE_UNREADABLE reason={reason} path={path}")
        self.code = "VERSION_STATE_UNREADABLE"
        self.reason = reason


class LegacyWriterBypassDetected(VersionStateUnreadable):
    def __init__(self, path, reason: str = "LEGACY_UNVERSIONED_OVERWRITE") -> None:
        super().__init__(path, reason)
        self.code = "LEGACY_WRITER_BYPASS_DETECTED"


class LockTimeoutError(Exception):
    def __init__(self, path, timeout) -> None:
        super().__init__(f"JOURNAL_LOCK_TIMEOUT path={path} timeout={timeout}")
        self.code = "JOURNAL_LOCK_TIMEOUT"
        self.timeout = timeout


class AcknowledgedPrefixRewriteRefused(ValueError):
    def __init__(self, path) -> None:
        super().__init__(f"ACKNOWLEDGED_LEDGER_PREFIX_REWRITE_NOT_GRANTED path={path}")
        self.code = "ACKNOWLEDGED_LEDGER_PREFIX_REWRITE_NOT_GRANTED"


class GhostReplayRefused(ValueError):
    def __init__(self, path, reason: str) -> None:
        super().__init__(f"GHOST_REPLAY_REFUSED reason={reason} path={path}")
        self.code = "GHOST_REPLAY_REFUSED"
        self.reason = reason


class WriterCapabilityRequired(TypeError):
    def __init__(self, path) -> None:
        super().__init__(f"WRITER_CAPABILITY_REQUIRED path={path}")
        self.code = "WRITER_CAPABILITY_REQUIRED"


class CapabilityTrustAnchorUnissued(Exception):
    def __init__(self) -> None:
        super().__init__(C8_CAPABILITY_TRUST_ANCHOR_UNISSUED)
        self.code = C8_CAPABILITY_TRUST_ANCHOR_UNISSUED


class TrustedAnchorUnissued(Exception):
    def __init__(self) -> None:
        super().__init__(C8_TRUSTED_ANCHOR_UNISSUED)
        self.code = C8_TRUSTED_ANCHOR_UNISSUED


class AnchorRollbackDetected(Exception):
    def __init__(self, observed, current) -> None:
        super().__init__(f"ANCHOR_ROLLBACK_DETECTED observed={observed} current={current}")
        self.code = "ANCHOR_ROLLBACK_DETECTED"
        self.observed = observed
        self.current = current


class TrustedTimeSourceUnissued(Exception):
    def __init__(self) -> None:
        super().__init__(C8_EFFECTIVE_CLOCK_SOURCE_UNTRUSTED)
        self.code = C8_EFFECTIVE_CLOCK_SOURCE_UNTRUSTED


@dataclass(frozen=True)
class WriterCapability:
    """Writer identity/capability, separated from any hash-as-signature claim.

    `capability_token` is opaque and meaningful only to a separately trusted
    issuer/verifier. This candidate ships NO trusted issuer, therefore every
    capability accepted here is UNKEYED and unauthenticated.
    """

    writer_id: str
    capability_token: str
    issuer_ref: str = "UNISSUED_NO_TRUSTED_ISSUER"

    def fingerprint(self) -> str:
        return _hash(
            {
                "writer_id": self.writer_id,
                "capability_token": self.capability_token,
                "issuer_ref": self.issuer_ref,
            }
        )


class UnkeyedFormatCapabilityVerifier:
    """TEST_FIXTURE_ONLY format checker. Explicitly NOT authentication."""

    trust_grade = CAPABILITY_FORMAT_ONLY_NOT_AUTHENTICATION

    def __init__(self, min_token_length: int = 16) -> None:
        self.min_token_length = min_token_length

    def present(self, capability: WriterCapability) -> bool:
        return (
            isinstance(capability, WriterCapability)
            and isinstance(capability.writer_id, str)
            and bool(capability.writer_id.strip())
            and isinstance(capability.capability_token, str)
            and len(capability.capability_token) >= self.min_token_length
        )

    def verify_trust(self, capability: WriterCapability) -> str:
        raise CapabilityTrustAnchorUnissued()


@dataclass
class FileBackedMonotonicAnchor:
    """TEST_FIXTURE_ONLY local stand-in for a trusted external version anchor.

    A real anchor must live outside every writer that can rewrite the journal.
    This file-backed stand-in is sufficient only in the tested local threat
    model where the anchor file is not attacker-writable. It confers NO
    production authenticity and is NOT a substitute for owner-issued custody.
    """

    path: Path
    grade: str = "TEST_FIXTURE_ONLY_LOCAL_ANCHOR_NOT_OWNER_ISSUED"

    def observe(self, writer_version: int, receipt_id: str) -> str:
        rows = self._rows()
        if rows:
            last_version, last_receipt = rows[-1]
            if writer_version < last_version or (
                writer_version == last_version and receipt_id != last_receipt
            ):
                raise AnchorRollbackDetected((last_version, last_receipt), (writer_version, receipt_id))
        rows.append([writer_version, receipt_id])
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = Path(str(self.path) + ".tmp")
        tmp.write_text(_canonical({"anchor": rows}), encoding="utf8")
        os.replace(tmp, self.path)
        return _hash({"anchor_index": len(rows) - 1, "receipt_id": receipt_id})

    def latest(self) -> Optional[list]:
        rows = self._rows()
        return list(rows[-1]) if rows else None

    def check(self, writer_version: int, receipt_id: str) -> None:
        latest = self.latest()
        if latest is None:
            return
        if writer_version < latest[0] or (
            writer_version == latest[0] and receipt_id != latest[1]
        ):
            raise AnchorRollbackDetected(tuple(latest), (writer_version, receipt_id))

    def _rows(self) -> list:
        if not self.path.exists():
            return []
        data = json.loads(self.path.read_text(encoding="utf8"))
        rows = data.get("anchor")
        if not isinstance(rows, list) or not all(
            isinstance(r, list) and len(r) == 2 and type(r[0]) is int for r in rows
        ):
            raise VersionStateUnreadable(self.path, "ANCHOR_ROWS_MALFORMED")
        return rows


def os_clock() -> dict:
    return {
        "source": "OS_CLOCK_SOURCEFREE_FIXTURE",
        "value": datetime.now(timezone.utc).isoformat(timespec="microseconds"),
    }


def trusted_clock_or_refuse() -> dict:
    raise TrustedTimeSourceUnissued()


def ledger_prefix_digest(state: dict) -> str:
    return _hash(
        [
            [e.get("occurrence_id"), e.get("identity_digest")]
            for e in state.get("ledger", [])
        ]
    )


def sealed_envelope(state: dict, writer_version: int, writer_id: str, effective_clock: dict) -> dict:
    return {
        "schema": SCHEMA,
        "state": state,
        "writer_version": writer_version,
        "ledger_prefix_digest": ledger_prefix_digest(state),
        "writer_id": writer_id,
        "effective_clock": effective_clock,
    }


@dataclass
class C8CommitReceipt:
    receipt_id: str
    writer_id: str
    writer_version: int
    state_digest: str
    version_state_digest: str
    ledger_prefix_digest: str
    capability_fingerprint: str
    capability_trust_grade: str
    effective_clock: dict
    acknowledged_occurrence_ids: list
    anti_rollback_grade: str

    def to_json(self) -> dict:
        return {
            "receipt_id": self.receipt_id,
            "writer_id": self.writer_id,
            "writer_version": self.writer_version,
            "state_digest": self.state_digest,
            "version_state_digest": self.version_state_digest,
            "ledger_prefix_digest": self.ledger_prefix_digest,
            "capability_fingerprint": self.capability_fingerprint,
            "capability_trust_grade": self.capability_trust_grade,
            "effective_clock": self.effective_clock,
            "acknowledged_occurrence_ids": list(self.acknowledged_occurrence_ids),
            "anti_rollback_grade": self.anti_rollback_grade,
        }


@dataclass
class EnvelopeCustody:
    status: str
    writer_version: int
    writer_id: Optional[str]
    receipt_id: Optional[str]
    reason: Optional[str]


class C8OccurrenceJournal:
    """Compare-and-append C8 occurrence journal under fcntl lock + sealed version state."""

    def __init__(
        self,
        path,
        *,
        lock_timeout: float = 15.0,
        poll: float = 0.002,
        capability_verifier: Optional[UnkeyedFormatCapabilityVerifier] = None,
        anchor: Optional[FileBackedMonotonicAnchor] = None,
        clock: Callable[[], dict] = os_clock,
    ) -> None:
        self.path = Path(path)
        self.lock_path = Path(str(self.path) + ".lock")
        self.lock_timeout = lock_timeout
        self.poll = poll
        self.capability_verifier = capability_verifier or UnkeyedFormatCapabilityVerifier()
        self.anchor = anchor
        self.clock = clock
        self._base = Journal(self.path)

    def _acquire(self) -> int:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(str(self.lock_path), os.O_CREAT | os.O_RDWR, 0o644)
        deadline = time.monotonic() + self.lock_timeout
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return fd
            except OSError as exc:
                if exc.errno not in (errno.EACCES, errno.EAGAIN):
                    os.close(fd)
                    raise
                if time.monotonic() >= deadline:
                    os.close(fd)
                    raise LockTimeoutError(self.lock_path, self.lock_timeout)
                time.sleep(self.poll)

    @staticmethod
    def _release(fd: int) -> None:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)

    def classify(self) -> EnvelopeCustody:
        if not self.path.exists():
            return EnvelopeCustody("GENESIS_V0", 0, None, None, None)
        try:
            contents = self.path.read_text(encoding="utf8")
            receipt = json.loads(contents)
        except (OSError, UnicodeError, ValueError) as exc:
            return EnvelopeCustody("CORRUPT", -1, None, None, type(exc).__name__)
        if not isinstance(receipt, dict):
            return EnvelopeCustody("CORRUPT", -1, None, None, "NON_OBJECT")
        if receipt.get("schema") != SCHEMA:
            return EnvelopeCustody("CORRUPT", -1, None, None, "UNSUPPORTED_SCHEMA")
        if "writer_version" not in receipt or "version_state_digest" not in receipt:
            return EnvelopeCustody("LEGACY_UNVERSIONED_OVERWRITE", -1, None, None, "LEGACY_UNVERSIONED_OVERWRITE")
        required = {
            "schema",
            "state",
            "state_digest",
            "writer_version",
            "version_state_digest",
            "ledger_prefix_digest",
            "writer_id",
            "capability_fingerprint",
            "capability_trust_grade",
            "effective_clock",
            "commit_receipt_id",
        }
        if set(receipt) != required:
            return EnvelopeCustody("CORRUPT", -1, None, None, "MISSING_OR_UNKNOWN_ENVELOPE_FIELDS")
        ver = receipt["writer_version"]
        if type(ver) is not int or ver < 1:
            return EnvelopeCustody("CORRUPT", -1, None, None, "VERSION_NOT_POSITIVE_INTEGER")
        state = receipt["state"]
        if not isinstance(state, dict):
            return EnvelopeCustody("CORRUPT", -1, None, None, "STATE_NOT_OBJECT")
        if receipt["state_digest"] != _hash(state):
            return EnvelopeCustody("CORRUPT", -1, None, None, "STATE_DIGEST_MISMATCH")
        clock = receipt["effective_clock"]
        if not isinstance(clock, dict) or set(clock) != {"source", "value"} or not all(
            isinstance(clock[k], str) and clock[k] for k in ("source", "value")
        ):
            return EnvelopeCustody("CORRUPT", -1, None, None, "EFFECTIVE_CLOCK_MALFORMED")
        sealed = sealed_envelope(state, ver, receipt["writer_id"], clock)
        if receipt["ledger_prefix_digest"] != sealed["ledger_prefix_digest"]:
            return EnvelopeCustody("CORRUPT", -1, None, None, "LEDGER_PREFIX_DIGEST_MISMATCH")
        if receipt["version_state_digest"] != _hash(sealed):
            return EnvelopeCustody("CORRUPT", -1, None, None, "VERSION_STATE_DIGEST_MISMATCH")
        if _canonical(receipt) != contents:
            return EnvelopeCustody("CORRUPT", -1, None, None, "NONCANONICAL_RECEIPT")
        if receipt["commit_receipt_id"] != _receipt_id(receipt):
            return EnvelopeCustody("CORRUPT", -1, None, None, "COMMIT_RECEIPT_ID_MISMATCH")
        return EnvelopeCustody(
            "VERSIONED_VALID",
            ver,
            receipt["writer_id"],
            receipt["commit_receipt_id"],
            None,
        )

    def _read_version(self) -> int:
        custody = self.classify()
        if custody.status == "GENESIS_V0":
            return 0
        if custody.status == "LEGACY_UNVERSIONED_OVERWRITE":
            raise LegacyWriterBypassDetected(self.path)
        if custody.status != "VERSIONED_VALID":
            raise VersionStateUnreadable(self.path, custody.reason or "UNREADABLE")
        return custody.writer_version

    def recover(self):
        fd = self._acquire()
        try:
            version = self._read_version()
            return self._base.recover(), version
        finally:
            self._release(fd)

    def recover_custody(self):
        fd = self._acquire()
        try:
            custody = self.classify()
            if custody.status == "GENESIS_V0":
                return make_prototype(), 0, custody
            if custody.status == "LEGACY_UNVERSIONED_OVERWRITE":
                raise LegacyWriterBypassDetected(self.path)
            if custody.status != "VERSIONED_VALID":
                raise VersionStateUnreadable(self.path, custody.reason or "UNREADABLE")
            return self._base.recover(), custody.writer_version, custody
        finally:
            self._release(fd)

    def commit(
        self,
        p,
        expected_version: int,
        *,
        capability: WriterCapability,
        crash_boundary: Optional[str] = None,
        require_trusted_time: bool = False,
    ) -> C8CommitReceipt:
        if crash_boundary is not None and crash_boundary not in CRASH_BOUNDARIES:
            raise ValueError("UNKNOWN_CRASH_BOUNDARY")
        if not isinstance(capability, WriterCapability):
            raise WriterCapabilityRequired(self.path)
        if not self.capability_verifier.present(capability):
            raise WriterCapabilityRequired(self.path)
        fd = self._acquire()
        try:
            if type(expected_version) is not int or expected_version < 0:
                raise VersionStateUnreadable(self.path, "NOT_GRANTED_EXPECTED_VERSION")
            actual = self._read_version()
            if actual != expected_version:
                raise StaleJournalConflict(expected_version, actual, self.path)
            if p.world_state:
                raise ValueError("WORLD_STATE_REQUIRES_EXTERNAL_OWNER")
            p.validate_state()
            state = p.snapshot()
            prior = self._base.recover().snapshot()
            old_events = prior["ledger"]
            if state["ledger"][: len(old_events)] != old_events:
                raise AcknowledgedPrefixRewriteRefused(self.path)
            new_events = state["ledger"][len(old_events) :]
            for event in new_events:
                if not isinstance(event, dict) or not event.get("occurrence_id"):
                    raise GhostReplayRefused(self.path, "EVENT_IDENTITY_MISSING")
                if event.get("occurrence_id") in [
                    e.get("occurrence_id") for e in old_events
                ]:
                    raise GhostReplayRefused(self.path, "DUPLICATE_OCCURRENCE_GHOST")
            effective_clock = trusted_clock_or_refuse() if require_trusted_time else self.clock()
            version = actual + 1
            writer_id = capability.writer_id
            sealed = sealed_envelope(state, version, writer_id, effective_clock)
            receipt = {
                **sealed,
                "state_digest": _hash(state),
                "version_state_digest": _hash(sealed),
                "capability_fingerprint": capability.fingerprint(),
                "capability_trust_grade": self.capability_verifier.trust_grade,
            }
            receipt["commit_receipt_id"] = _receipt_id(receipt)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tfd, temp = tempfile.mkstemp(prefix=".c8o-pending-", dir=str(self.path.parent))
            try:
                with os.fdopen(tfd, "w", encoding="utf8") as f:
                    f.write(_canonical(receipt))
                    f.flush()
                    os.fsync(f.fileno())
                if crash_boundary == "BEFORE_RENAME":
                    os._exit(79)
                if crash_boundary == "SIGKILL_BEFORE_RENAME":
                    os.kill(os.getpid(), signal.SIGKILL)
                os.replace(temp, self.path)
                dfd = os.open(str(self.path.parent), os.O_RDONLY)
                try:
                    os.fsync(dfd)
                finally:
                    os.close(dfd)
                if crash_boundary == "AFTER_COMMIT":
                    os._exit(79)
                if crash_boundary == "SIGKILL_AFTER_COMMIT":
                    os.kill(os.getpid(), signal.SIGKILL)
            finally:
                if os.path.exists(temp):
                    try:
                        os.unlink(temp)
                    except OSError:
                        pass
            anti_rollback_grade = ANTI_ROLLBACK_WITHOUT_ANCHOR
            if self.anchor is not None:
                self.anchor.observe(version, receipt["commit_receipt_id"])
                anti_rollback_grade = self.anchor.grade
            return C8CommitReceipt(
                receipt_id=receipt["commit_receipt_id"],
                writer_id=writer_id,
                writer_version=version,
                state_digest=receipt["state_digest"],
                version_state_digest=receipt["version_state_digest"],
                ledger_prefix_digest=receipt["ledger_prefix_digest"],
                capability_fingerprint=receipt["capability_fingerprint"],
                capability_trust_grade=receipt["capability_trust_grade"],
                effective_clock=effective_clock,
                acknowledged_occurrence_ids=[
                    e.get("occurrence_id") for e in state["ledger"]
                ],
                anti_rollback_grade=anti_rollback_grade,
            )
        finally:
            self._release(fd)

    def admit_and_queue(
        self,
        candidate: dict,
        *,
        capability: WriterCapability,
        viewer_id: Optional[str] = None,
        expected_version: Optional[int] = None,
        crash_boundary: Optional[str] = None,
    ):
        p, version = self.recover()
        if expected_version is not None and expected_version != version:
            raise StaleJournalConflict(expected_version, version, self.path)
        event = p.ledger.admit(candidate)
        if event is None:
            return None, p.ledger.last_refusal, None
        eid = event["occurrence_id"]
        if viewer_id is not None:
            if not p.outbox.authorize_viewer(eid, viewer_id):
                return None, "VIEWER_NOT_AUTHORIZED", None
        state = p.outbox.emit(eid, viewer_id=viewer_id)
        if str(state) == "NOT_SENT":
            return None, "EMISSION_REFUSED", None
        if viewer_id is not None and p.outbox.emit_to(eid, viewer_id) is None:
            return None, "CLIENT_INTENT_REFUSED", None
        receipt = self.commit(p, version, capability=capability, crash_boundary=crash_boundary)
        return event, None, receipt

    def anti_rollback_check(self, writer_version: int, receipt_id: str) -> str:
        if self.anchor is None:
            raise TrustedAnchorUnissued()
        self.anchor.check(writer_version, receipt_id)
        return self.anchor.grade

    def detect_legacy_bypass(self) -> Optional[dict]:
        """After-the-fact detection only. Prevention is NOT claimed."""
        custody = self.classify()
        if custody.status in ("LEGACY_UNVERSIONED_OVERWRITE", "CORRUPT"):
            return {
                "bypass_detected": True,
                "status": custody.status,
                "reason": custody.reason,
                "code": "LEGACY_WRITER_BYPASS_DETECTED",
                "authority_form": LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED,
                "prevention": "NOT_POSSIBLE_WITH_CURRENT_LEGAL_CALLABLE_API",
            }
        return None


def _receipt_id(receipt: dict) -> str:
    return _hash(
        {
            "schema": receipt["schema"],
            "writer_version": receipt["writer_version"],
            "state_digest": receipt["state_digest"],
            "version_state_digest": receipt["version_state_digest"],
            "ledger_prefix_digest": receipt["ledger_prefix_digest"],
            "writer_id": receipt["writer_id"],
            "capability_fingerprint": receipt["capability_fingerprint"],
            "effective_clock": receipt["effective_clock"],
        }
    )


def forged_receipt(receipt: dict, **overrides) -> str:
    """Recompute every unkeyed digest after arbitrary field overrides.

    Exists as a falsifier helper: any actor allowed to rewrite the file can
    produce this. It is the concrete counterexample to reading `state_digest`
    or `version_state_digest` as writer authentication or anti-rollback.
    """
    mutated = dict(receipt)
    mutated.update(overrides)
    state = mutated["state"]
    sealed = sealed_envelope(
        state,
        mutated["writer_version"],
        mutated["writer_id"],
        mutated["effective_clock"],
    )
    mutated["state_digest"] = _hash(state)
    mutated["ledger_prefix_digest"] = sealed["ledger_prefix_digest"]
    mutated["version_state_digest"] = _hash(sealed)
    mutated["commit_receipt_id"] = _receipt_id(mutated)
    return _canonical(mutated)
