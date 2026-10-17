"""OUT12 return-local multiwriter concurrency candidate.

OPT-IN wrapper around the accepted OUT9 `outbox_prototype.Journal`. It does NOT
modify, subclass-monkeypatch or otherwise alter the accepted source; it adds a
separate, explicitly-selected concurrency discipline on top of it.

Two mechanisms, both required together for safety:

1. INTERPROCESS TRANSACTION LOCK -- an exclusive `fcntl.flock` on
   `<journal>.lock` is held across version check, validation and publication.
   Caller-side snapshot mutation occurs outside this lock; CAS rejects stale
   snapshots before the atomic replacement write.

2. VERSIONED COMPARE-AND-SWAP -- a monotonically increasing `writer_version`
   is persisted in the journal receipt. `recover()` returns the version it
   observed; `commit()` refuses with a typed `StaleJournalConflict` unless the
   on-disk version still equals the expected one. The lock makes the
   compare-and-swap atomic; the CAS makes a stale holder's publish impossible
   even if it is released by a crash or a non-cooperating writer.

OUT14 adds a canonical full-envelope version digest and fail-closed validation
for missing, malformed, tampered or legacy-overwritten metadata. It is an
UNKEYED integrity check, not cryptographic authentication of writers. The
accepted Journal.commit remains independently callable and BYPASSES this
facade: this module CANNOT claim system-wide multiwriter authorization until
a competent owner removes or denies that legacy write path. Replay of an
entire authentic old receipt also needs an external trusted monotonic anchor.
The accepted Journal source, its semantics, and frozen tests are not modified.
"""
from __future__ import annotations
import errno, fcntl, json, os, signal, tempfile, time
from pathlib import Path

from outbox_prototype import Journal, _canonical, _hash

SCHEMA = "OUTBOX_F2_JOURNAL_V2"


class StaleJournalConflict(Exception):
    """Typed conflict: the on-disk version moved on since this writer recovered."""

    def __init__(self, expected: int, actual: int, path) -> None:
        super().__init__(f"STALE_JOURNAL_CONFLICT expected_version={expected} actual_version={actual} path={path}")
        self.expected = expected
        self.actual = actual
        self.code = "STALE_JOURNAL_CONFLICT"


class VersionStateUnreadable(ValueError):
    """No silent version-zero coercion. Does not confer ADP019 authority."""

    def __init__(self, path, reason: str) -> None:
        super().__init__(f"VERSION_STATE_UNREADABLE reason={reason} path={path}")
        self.code = "VERSION_STATE_UNREADABLE"
        self.reason = reason


class LockTimeoutError(Exception):
    def __init__(self, path, timeout) -> None:
        super().__init__(f"JOURNAL_LOCK_TIMEOUT path={path} timeout={timeout}")
        self.code = "JOURNAL_LOCK_TIMEOUT"


class MultiwriterJournal:
    """Opt-in multiwriter-safe journal. Same on-disk schema as the accepted Journal."""

    def __init__(self, path, *, lock_timeout: float = 15.0, poll: float = 0.002) -> None:
        self.path = Path(path)
        self.lock_path = Path(str(self.path) + ".lock")
        self.lock_timeout = lock_timeout
        self.poll = poll
        self._base = Journal(self.path)

    # ---------------- lock ----------------
    def _acquire(self):
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
    def _release(fd):
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)

    # ---------------- read ----------------
    def _read_version(self) -> int:
        """Validate one exact version-bound canonical receipt or reject.

        A nonexistent file is the ONLY valid genesis version 0. An existing
        unversioned/legacy, truncated, injected, or malformed file is NOT a
        fresh journal. An unkeyed digest cannot authenticate the writer or
        detect replay of an entirely previous valid receipt; owner grants
        and trusted anti-rollback custody remain separate prerequisites.
        """
        if not self.path.exists():
            return 0
        try:
            contents = self.path.read_text(encoding="utf8")
            receipt = json.loads(contents)
            if not isinstance(receipt, dict):
                raise ValueError("NON_OBJECT")
            required = {"schema", "state", "state_digest",
                        "writer_version", "version_state_digest"}
            if set(receipt) != required:
                raise ValueError("MISSING_OR_UNKNOWN_ENVELOPE_FIELDS")
            if receipt["schema"] != SCHEMA:
                raise ValueError("UNSUPPORTED_SCHEMA")
            ver = receipt["writer_version"]
            if type(ver) is not int or ver < 1:
                raise ValueError("VERSION_NOT_POSITIVE_INTEGER")
            if not isinstance(receipt["state"], dict):
                raise ValueError("STATE_NOT_OBJECT")
            if receipt["state_digest"] != _hash(receipt["state"]):
                raise ValueError("STATE_DIGEST_MISMATCH")
            sealed = {"schema": SCHEMA, "state": receipt["state"],
                      "writer_version": ver}
            if receipt["version_state_digest"] != _hash(sealed):
                raise ValueError("VERSION_STATE_DIGEST_MISMATCH")
            if _canonical(receipt) != contents:
                raise ValueError("NONCANONICAL_RECEIPT")
            return ver
        except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
            raise VersionStateUnreadable(self.path, type(exc).__name__ + ":" + str(exc)) from exc

    def recover(self):
        """Return (prototype, version). Reads under the lock for a coherent snapshot."""
        fd = self._acquire()
        try:
            version = self._read_version()
            return self._base.recover(), version
        finally:
            self._release(fd)

    # ---------------- write (CAS) ----------------
    def commit(self, p, expected_version: int, *, crash_boundary=None) -> int:
        """Publish `p` iff the on-disk version still equals `expected_version`.

        Raises StaleJournalConflict otherwise -- the caller may re-recover and
        legitimately retry against the new version.
        """
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
            if state["ledger"][:len(old_events)] != old_events:
                raise ValueError("ACKNOWLEDGED_LEDGER_PREFIX_REWRITE_NOT_GRANTED")
            versioned = {"schema": SCHEMA, "state": state,
                         "writer_version": actual + 1}
            receipt = {**versioned, "state_digest": _hash(state),
                       "version_state_digest": _hash(versioned)}
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tfd, temp = tempfile.mkstemp(prefix=".outbox-pending-", dir=str(self.path.parent))
            try:
                with os.fdopen(tfd, "w", encoding="utf8") as f:
                    f.write(_canonical(receipt)); f.flush(); os.fsync(f.fileno())
                if crash_boundary == "BEFORE_RENAME":
                    os._exit(79)  # abrupt exit, NOT SIGKILL
                if crash_boundary == "SIGKILL_BEFORE_RENAME":
                    os.kill(os.getpid(), signal.SIGKILL)
                os.replace(temp, self.path)
                dfd = os.open(str(self.path.parent), os.O_RDONLY)
                try:
                    os.fsync(dfd)
                finally:
                    os.close(dfd)
                if crash_boundary == "AFTER_COMMIT":
                    os._exit(79)  # abrupt exit after fsync, NOT SIGKILL
                if crash_boundary == "SIGKILL_AFTER_COMMIT":
                    os.kill(os.getpid(), signal.SIGKILL)
            finally:
                if os.path.exists(temp):
                    try:
                        os.unlink(temp)
                    except OSError:
                        pass
            return actual + 1
        finally:
            self._release(fd)
