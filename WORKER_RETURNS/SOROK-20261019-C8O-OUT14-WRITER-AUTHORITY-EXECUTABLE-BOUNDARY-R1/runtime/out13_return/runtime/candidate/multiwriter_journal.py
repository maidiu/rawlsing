"""OUT12 return-local multiwriter concurrency candidate.

OPT-IN wrapper around the accepted OUT9 `outbox_prototype.Journal`. It does NOT
modify, subclass-monkeypatch or otherwise alter the accepted source; it adds a
separate, explicitly-selected concurrency discipline on top of it.

Two mechanisms, both required together for safety:

1. INTERPROCESS TRANSACTION LOCK -- an exclusive `fcntl.flock` on
   `<journal>.lock` is held across the ENTIRE read-modify-write, so two
   processes cannot interleave their read of the on-disk state with their
   publish of a replacement snapshot.

2. VERSIONED COMPARE-AND-SWAP -- a monotonically increasing `writer_version`
   is persisted in the journal receipt. `recover()` returns the version it
   observed; `commit()` refuses with a typed `StaleJournalConflict` unless the
   on-disk version still equals the expected one. The lock makes the
   compare-and-swap atomic; the CAS makes a stale holder's publish impossible
   even if it is released by a crash or a non-cooperating writer.

The added top-level `writer_version` key is backward compatible: the accepted
`Journal.recover()` validates `schema` and a digest over `state` only, so a
receipt carrying the extra key still loads. Running the accepted `Journal`
against such a file simply ignores the version and re-exposes the original
last-writer-wins hazard -- which is exactly the defect this candidate closes.
"""
from __future__ import annotations
import errno, fcntl, json, os, tempfile, time
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
        if not self.path.exists():
            return 0
        try:
            return int(json.loads(self.path.read_text()).get("writer_version", 0))
        except (ValueError, TypeError):
            return 0

    def recover(self):
        """Return (prototype, version). Reads under the lock for a coherent snapshot."""
        fd = self._acquire()
        try:
            return self._base.recover(), self._read_version()
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
            actual = self._read_version()
            if actual != expected_version:
                raise StaleJournalConflict(expected_version, actual, self.path)
            if p.world_state:
                raise ValueError("WORLD_STATE_REQUIRES_EXTERNAL_OWNER")
            p.validate_state()
            state = p.snapshot()
            receipt = {"schema": SCHEMA, "state": state, "state_digest": _hash(state),
                       "writer_version": actual + 1}
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tfd, temp = tempfile.mkstemp(prefix=".outbox-pending-", dir=str(self.path.parent))
            try:
                with os.fdopen(tfd, "w", encoding="utf8") as f:
                    f.write(_canonical(receipt)); f.flush(); os.fsync(f.fileno())
                if crash_boundary == "BEFORE_RENAME":
                    os._exit(79)
                os.replace(temp, self.path)
                dfd = os.open(str(self.path.parent), os.O_RDONLY)
                try:
                    os.fsync(dfd)
                finally:
                    os.close(dfd)
                if crash_boundary == "AFTER_COMMIT":
                    os._exit(79)
            finally:
                if os.path.exists(temp):
                    try:
                        os.unlink(temp)
                    except OSError:
                        pass
            return actual + 1
        finally:
            self._release(fd)
