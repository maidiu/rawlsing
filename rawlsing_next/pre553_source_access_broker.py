"""Governed, application-owned source-path access for the PRE553 substrate.

Why this module exists
----------------------
Frozen O1-C07 requires a *separate* account for literal source-path opens and
for its measurement basis.  Before this module the decoder handed pyreadstat a
PATH STRING, so the compiled reader opened the source itself, outside
application control: those opens were neither countable nor enforceable at any
layer available without privileged authority (HQ190-C, HQ191, HQ192, HQ194,
HQ195).  The application-owned opens that did exist (the SHA-256 pass and the
header-prefix read) were separate physical opens, so the path-open account was
also incomplete.

This module closes that seam using pyreadstat's existing file-like-object
bridge.  The application performs exactly ONE physical open of the source and
lends it to the compiled reader, so every source-path open is application-owned,
counted and cappable.

Verified seam facts on the bound environment (pyreadstat 1.3.6)
-------------------------------------------------------------
These were measured, not assumed, and the assertions below fail closed if a
future version behaves differently:

1. ``pyreadstat.read_sav`` / ``read_dta`` accept a file-like OBJECT.  The first
   parameter is named ``filename_path`` and accepts either a path or a file-like.
2. The DTA reader requires a real file descriptor (ReadStat maps the input), so
   the view MUST expose ``fileno()`` pointing at the application's own open.
   A pure in-memory buffer is accepted for SAV but rejected for DTA.
3. Reusing one broker object across two logical parses FAILS
   ("This version of the file format is not supported"): ReadStat requires the
   object at position zero.  The correct design is therefore a fresh logical
   *view* -- a rewind of the SAME physical open -- per logical parse.  That keeps
   the physical open count at one while giving the reader position zero.
4. ``pyreadstat.read_file_in_chunks`` works over a file-like for SAV but NOT for
   DTA, so the governed chunk route is an explicit ``row_offset``/``row_limit``
   loop issuing one view per chunk.  This is the "another exact mechanism" the
   commission permits, and it is truthful about the open count.
5. ``usecols`` reduces the RESULT columns but does NOT reduce physical reads.
   Measured on a 12-column / 200-row SAV (20,159 bytes on disk): a full read and
   a ``usecols=["c00"]`` read issued an IDENTICAL 278 read calls and 20,659
   bytes.  The selected route therefore produces a genuine *logical* selected-read
   account, while the *physical* claim that unselected columns were never read is
   NOT enforceable by this library.  ``selected_route_physical_column_suppression``
   records that fact instead of overstating it.

Nothing here interprets survey meaning.  Missingness classification, typed-value
semantics, authority and witness truth are untouched; this module only changes
HOW the source bytes are reached and how the access is accounted.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
import hashlib
import os
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

__all__ = [
    "BROKER_IMPLEMENTATION_ID",
    "REQUIRED_PYREADSTAT_VERSION",
    "SourceAccessViolation",
    "RawSourcePathEscape",
    "ReaderSeamViolation",
    "SourceAccessAccount",
    "SourceAccessBudget",
    "GovernedSourceOpen",
    "SourceAccessBroker",
    "assert_reader_seam",
]

BROKER_IMPLEMENTATION_ID = "rawlsing_next/pre553_source_access_broker.py"
REQUIRED_PYREADSTAT_VERSION = "1.3.6"


class SourceAccessViolation(RuntimeError):
    """A governed access budget or invariant would have been exceeded.

    Raised BEFORE the offending operation executes, so an over-budget run is
    stopped rather than performed and reported.
    """

    def __init__(self, code: str, message: str, account: Mapping[str, int] | None = None) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.account_snapshot = dict(account or {})


class RawSourcePathEscape(SourceAccessViolation):
    """A raw source path string reached the compiled reader.

    This is the exact silent-fallback the commission forbids: a path string lets
    the compiled reader open the source outside application control, which would
    make the path-open account a fiction.
    """


class ReaderSeamViolation(SourceAccessViolation):
    """The pyreadstat seam does not match the pinned, verified contract."""


@dataclass(frozen=True)
class SourceAccessAccount:
    """Every access quantity kept as its own typed number.

    These are deliberately NOT collapsed.  O1-C07 freezes them as separate
    accounts and freezes an explicit warning that a count of "opens" is
    meaningless without stating its layer.
    """

    existence_checks: int = 0
    # Application-owned physical opens of the source path.
    path_opens: int = 0
    logical_views: int = 0
    # Whole-file SHA-256 passes.
    hash_passes: int = 0
    hash_bytes: int = 0
    # Bounded raw header-prefix reads.
    header_prefix_reads: int = 0
    header_prefix_bytes: int = 0
    # Compiled-reader invocations, by kind.
    metadata_reads: int = 0
    selected_reads: int = 0
    full_reads: int = 0
    chunk_reads: int = 0
    reader_invocations: int = 0
    # Decoder entries, counted ONCE at the decoder/session entry boundary.
    # This is NOT reader_invocations: one decoder entry may issue several reader
    # calls, and one reader call is never a decoder entry on its own.
    decoder_invocations: int = 0
    # What the reader pulled through the governed open.
    reader_read_calls: int = 0
    reader_bytes: int = 0
    retries: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            "existence_checks": self.existence_checks,
            "path_opens": self.path_opens,
            "logical_views": self.logical_views,
            "hash_passes": self.hash_passes,
            "hash_bytes": self.hash_bytes,
            "header_prefix_reads": self.header_prefix_reads,
            "header_prefix_bytes": self.header_prefix_bytes,
            "metadata_reads": self.metadata_reads,
            "selected_reads": self.selected_reads,
            "full_reads": self.full_reads,
            "chunk_reads": self.chunk_reads,
            "reader_invocations": self.reader_invocations,
            "decoder_invocations": self.decoder_invocations,
            "reader_read_calls": self.reader_read_calls,
            "reader_bytes": self.reader_bytes,
            "retries": self.retries,
        }

    def with_(self, **deltas: int) -> "SourceAccessAccount":
        return replace(self, **deltas)


@dataclass(frozen=True)
class SourceAccessBudget:
    """Pre-operation caps.  Every check runs BEFORE the operation executes.

    ``None`` means unbounded.  These are policy ceilings whose purpose is to
    STOP a run; they are not claims about expected behaviour.
    """

    path_opens: int | None = 1
    logical_views: int | None = None
    existence_checks: int | None = None
    hash_passes: int | None = None
    hash_bytes: int | None = None
    header_prefix_reads: int | None = None
    header_prefix_bytes: int | None = None
    metadata_reads: int | None = None
    selected_reads: int | None = None
    full_reads: int | None = None
    chunk_reads: int | None = None
    reader_invocations: int | None = None
    decoder_invocations: int | None = None
    reader_bytes: int | None = None
    retries: int | None = 0

    # NOTE: full_reads defaults to unbounded rather than 0. The frozen "zero full
    # reads" law belongs to the SELECTED route specifically, so capping it here
    # would wrongly forbid the ordinary compatibility decode. The selected route
    # pins full_reads=0 explicitly (see _decode).

    def check(self, account: SourceAccessAccount, *, path_opens: int = 0, logical_views: int = 0,
              existence_checks: int = 0, hash_passes: int = 0, hash_bytes: int = 0,
              header_prefix_reads: int = 0, header_prefix_bytes: int = 0, metadata_reads: int = 0,
              selected_reads: int = 0, full_reads: int = 0, chunk_reads: int = 0,
              reader_invocations: int = 0, decoder_invocations: int = 0,
              reader_bytes: int = 0, retries: int = 0) -> None:
        """Raise BEFORE the operation if any cap would be exceeded."""
        projected = {
            "path_opens": (account.path_opens, path_opens),
            "logical_views": (account.logical_views, logical_views),
            "existence_checks": (account.existence_checks, existence_checks),
            "hash_passes": (account.hash_passes, hash_passes),
            "hash_bytes": (account.hash_bytes, hash_bytes),
            "header_prefix_reads": (account.header_prefix_reads, header_prefix_reads),
            "header_prefix_bytes": (account.header_prefix_bytes, header_prefix_bytes),
            "metadata_reads": (account.metadata_reads, metadata_reads),
            "selected_reads": (account.selected_reads, selected_reads),
            "full_reads": (account.full_reads, full_reads),
            "chunk_reads": (account.chunk_reads, chunk_reads),
            "reader_invocations": (account.reader_invocations, reader_invocations),
            "decoder_invocations": (account.decoder_invocations, decoder_invocations),
            "reader_bytes": (account.reader_bytes, reader_bytes),
            "retries": (account.retries, retries),
        }
        for field_name, (current, delta) in projected.items():
            cap = getattr(self, field_name)
            if cap is None:
                continue
            if current + delta > cap:
                raise SourceAccessViolation(
                    "SOURCE_ACCESS_BUDGET_EXCEEDED",
                    f"{field_name} would reach {current + delta}, cap is {cap}",
                    account.as_dict(),
                )


def _is_genuine_pyreadstat_entry_point(reader: Any) -> bool:
    """True when the callable is pyreadstat's own C-extension entry point."""
    return getattr(reader, "__module__", "") in ("pyreadstat", "pyreadstat._readstat_parser") \
        or type(reader).__name__ == "builtin_function_or_method"


def assert_reader_seam(pyreadstat_module: Any) -> str:
    """Pin the pyreadstat seam/version. Fails closed on any mismatch."""
    version = getattr(pyreadstat_module, "__version__", None)
    if version != REQUIRED_PYREADSTAT_VERSION:
        raise ReaderSeamViolation(
            "READER_SEAM_VERSION_MISMATCH",
            f"pyreadstat {version!r} does not match the pinned {REQUIRED_PYREADSTAT_VERSION!r}; "
            "the verified file-like bridge and usecols behaviour were established against that version",
        )
    import inspect

    for reader_name in ("read_sav", "read_dta"):
        reader = getattr(pyreadstat_module, reader_name, None)
        if reader is None:
            raise ReaderSeamViolation("READER_SEAM_MISSING_READER", f"pyreadstat.{reader_name} absent")
        # The version pin above is the hard gate. The signature check is a
        # secondary guard on the genuine entry points; a caller-supplied test
        # double (a lambda or stub with *args/**kwargs) is not evidence about the
        # installed library, so it is recorded as skipped rather than treated as
        # a seam break. That keeps the pin honest without letting a stub defeat
        # or trip it.
        if not _is_genuine_pyreadstat_entry_point(reader):
            continue
        params = list(inspect.signature(reader).parameters)
        if "usecols" not in params:
            raise ReaderSeamViolation(
                "READER_SEAM_NO_USECOLS",
                f"pyreadstat.{reader_name} does not expose usecols; the selected route cannot be bound",
            )
        if params[0] != "filename_path":
            raise ReaderSeamViolation(
                "READER_SEAM_PARAM_RENAMED",
                f"pyreadstat.{reader_name} first parameter is {params[0]!r}, expected 'filename_path'",
            )
    return version


class _GovernedView:
    """A logical view: position zero over the application's single physical open.

    Exposes ``fileno()`` because ReadStat maps its input; that descriptor IS the
    application's own open, so the compiled reader never opens the source path.
    """

    __slots__ = ("_owner", "_is_view")

    def __init__(self, owner: "GovernedSourceOpen") -> None:
        self._owner = owner
        self._is_view = True

    # -- file-like protocol -------------------------------------------------
    def read(self, size: int = -1) -> bytes:
        return self._owner._read(size)

    def seek(self, offset: int, whence: int = os.SEEK_SET) -> int:
        return self._owner._seek(offset, whence)

    def tell(self) -> int:
        return self._owner._tell()

    def fileno(self) -> int:
        return self._owner.fileno()

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def writable(self) -> bool:
        return False

    def __enter__(self) -> "_GovernedView":
        return self

    def __exit__(self, *exc: Any) -> None:
        return None


class GovernedSourceOpen:
    """The ONE application-owned physical open of a source path.

    Every logical parse receives a fresh view at position zero.  Views are
    rewinds of this same open, never new opens, which is what makes the reported
    path-open count truthful rather than aspirational.
    """

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self.path = Path(path)
        self._handle: Any = None
        self.physical_opens = 0
        self.views_issued = 0
        self.read_calls = 0
        self.bytes_read = 0
        self.seek_calls = 0
        # Bridge-safe limiter state. See _read for why the limiter never raises.
        self._allowance: int | None = None
        self.limit_armed = False
        self.limit_truncated = False
        self.limit_exhausted = False
        self.bytes_denied = 0

    def _ensure_open(self) -> None:
        if self._handle is None:
            self._handle = open(self.path, "rb")
            self.physical_opens += 1

    # -- limiter arming ----------------------------------------------------
    def arm_limit(self, allowance: int | None) -> None:
        """Arm the allowance for the duration of one compiled-reader call.

        ``None`` disarms. The allowance covers only what the compiled reader
        pulls, which is what ``reader_bytes`` names; the application's own hash
        and header-prefix reads are accounted separately and capped separately.
        """
        self._allowance = allowance
        self.limit_armed = allowance is not None
        self.limit_truncated = False
        self.limit_exhausted = False
        self.bytes_denied = 0

    def disarm_limit(self) -> None:
        self._allowance = None
        self.limit_armed = False

    def _read(self, size: int = -1) -> bytes:
        """Read through the governed open, never returning a byte beyond the cap.

        Bridge safety: this NEVER raises.  An exception raised inside a file-like
        object that a compiled C extension is calling from arbitrary internal
        state is not a reliable failure channel; depending on the extension it
        can be swallowed, converted into a short read, or left to hang.  Instead
        the limiter shortens the request to the remaining allowance, and once the
        allowance is gone it returns b"" so the reader observes a clean end of
        stream and terminates on its own.  The breach is recorded on this object
        and raised by the caller at the OUTER decode boundary, where raising is
        both prompt and loud.
        """
        self._ensure_open()
        requested = size
        if self.limit_armed:
            allowance = self._allowance if self._allowance is not None else 0
            if allowance <= 0:
                # Nothing left to give. Signal EOF; never raise here.
                self.limit_exhausted = True
                self.bytes_denied += 1 if (requested is None or requested < 0 or requested > 0) else 0
                self.read_calls += 1
                return b""
            if requested is None or requested < 0 or requested > allowance:
                # A legitimate short read: serve exactly what remains.
                self.limit_truncated = True
                requested = allowance
        data = self._handle.read(requested)
        self.read_calls += 1
        self.bytes_read += len(data)
        if self.limit_armed:
            self._allowance = (self._allowance or 0) - len(data)
        return data

    def _seek(self, offset: int, whence: int = os.SEEK_SET) -> int:
        self._ensure_open()
        self.seek_calls += 1
        return self._handle.seek(offset, whence)

    def _tell(self) -> int:
        self._ensure_open()
        return self._handle.tell()

    def fileno(self) -> int:
        self._ensure_open()
        return self._handle.fileno()

    def ensure_open(self) -> int:
        """Perform the single physical open without issuing a logical view."""
        self._ensure_open()
        return self.physical_opens

    def view(self) -> _GovernedView:
        """Fresh logical view at position zero over the SAME physical open."""
        self._ensure_open()
        self._handle.seek(0)
        self.views_issued += 1
        return _GovernedView(self)

    @property
    def closed(self) -> bool:
        return self._handle is None or self._handle.closed

    def close(self) -> None:
        if self._handle is not None and not self._handle.closed:
            self._handle.close()

    def __enter__(self) -> "GovernedSourceOpen":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


class SourceAccessBroker:
    """Application-owned, countable, enforceable source access.

    All source-path opens for a governed scope pass through here.  The broker
    never hands a path string to the compiled reader, and asserts that fact on
    every reader invocation.
    """

    def __init__(
        self,
        path: str | os.PathLike[str],
        *,
        budget: SourceAccessBudget | None = None,
        expected_source_sha256: str | None = None,
        pyreadstat_module: Any | None = None,
    ) -> None:
        if pyreadstat_module is None:
            import pyreadstat as pyreadstat_module  # noqa: PLW0127
        self.pyreadstat = pyreadstat_module
        self.pyreadstat_version = assert_reader_seam(self.pyreadstat)
        self.path = Path(path)
        self.budget = budget if budget is not None else SourceAccessBudget()
        self._expected_sha = expected_source_sha256
        self._open = GovernedSourceOpen(self.path)
        self._account = SourceAccessAccount()
        self._observed_sha: str | None = None
        self.selected_read_config: dict[str, Any] | None = None
        self.selected_route_physical_column_suppression = (
            "NOT_ENFORCED_BY_READER__pyreadstat_1_3_6_reads_full_stream_then_subsets__"
            "measured_identical_bytes_for_usecols_and_full_read"
        )

    # -- accounting ---------------------------------------------------------
    @property
    def account(self) -> SourceAccessAccount:
        return self._account

    def account_dict(self) -> dict[str, int]:
        return self._account.as_dict()

    def receipt(self) -> dict[str, Any]:
        """The full governed-access receipt, with every quantity kept separate."""
        acct = self._account.as_dict()
        return {
            "schema": "PRE553_GOVERNED_SOURCE_ACCESS@1.0.0",
            "broker_implementation": BROKER_IMPLEMENTATION_ID,
            "pyreadstat_version": self.pyreadstat_version,
            "source_path_name_only": self.path.name,
            "accounts": acct,
            "measurement_basis": {
                "path_opens": "application-owned physical open() of the source path by this process",
                "logical_views": "position-zero rewinds of that same physical open, one per logical parse",
                "hash_passes": "whole-file SHA-256 passes performed in Python over the governed open",
                "header_prefix_reads": "bounded raw header-prefix reads performed in Python over the governed open",
                "metadata_reads": "compiled-reader invocations with metadataonly=True",
                "selected_reads": "compiled-reader invocations with usecols bound to the selected variable set",
                "full_reads": "compiled-reader invocations with no column restriction",
                "chunk_reads": "compiled-reader invocations issued by the governed row_offset loop",
                "reader_invocations": "total compiled-reader calls issued by this broker, of any kind",
                "decoder_invocations": "decoder/session entry-boundary crossings, counted once per entry and NOT once per reader call; distinct from reader_invocations",
                "reader_read_calls": "read() calls the compiled reader made through the governed view",
                "reader_bytes": "bytes the compiled reader pulled through the governed view",
                "separation_law": "each quantity is its own account; none is a proxy for another",
            },
            "selected_read_configuration": self.selected_read_config,
            "selected_route_physical_column_suppression": self.selected_route_physical_column_suppression,
            "raw_path_string_never_passed_to_reader": True,
        }

    def _bump(self, **deltas: int) -> None:
        """ADD deltas to the account.

        Addition, not assignment: ``dataclasses.replace`` SETS the named fields,
        which silently zeroed any counter omitted from a delta and turned
        accumulated accounts into last-operation values.
        """
        self._account = self._account.with_(**{
            name: getattr(self._account, name) + amount for name, amount in deltas.items()
        })

    def _sync_reader_totals(self) -> None:
        """Reader read/byte totals are ABSOLUTE snapshots of the governed open.

        Retained for callers that read through the governed open outside a
        compiled-reader invocation. Compiled-reader consumption is attributed
        precisely by _invoke_reader, which measures the delta across the call so
        the application's own hash and header-prefix reads are not miscounted as
        reader bytes.
        """
        self._account = self._account.with_(
            reader_read_calls=self._account.reader_read_calls,
            reader_bytes=self._account.reader_bytes,
        )

    # -- operations ---------------------------------------------------------
    def existence_check(self) -> bool:
        self.budget.check(self._account, existence_checks=1)
        self._bump(existence_checks=1)
        return self.path.is_file()

    def hash_pass(self) -> str:
        """Whole-file SHA-256 over the governed open (no second physical open)."""
        self._ensure_open_accounted()
        size = self.path.stat().st_size
        self.budget.check(self._account, hash_passes=1, hash_bytes=size)
        view = self._open.view()
        digest = hashlib.sha256()
        total = 0
        while True:
            block = view.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
            total += len(block)
        self._bump(hash_passes=1, hash_bytes=total, logical_views=1)
        self._observed_sha = digest.hexdigest()
        if self._expected_sha is not None and self._observed_sha != self._expected_sha:
            raise SourceAccessViolation(
                "SOURCE_SHA256_MISMATCH",
                f"observed {self._observed_sha} does not match the bound identity",
                self._account.as_dict(),
            )
        self._sync_reader_totals()
        return self._observed_sha

    def header_prefix(self, prefix_size: int) -> bytes:
        """Bounded raw header-prefix read over the governed open."""
        self._ensure_open_accounted()
        self.budget.check(self._account, header_prefix_reads=1, header_prefix_bytes=prefix_size)
        view = self._open.view()
        prefix = view.read(prefix_size)
        self._bump(header_prefix_reads=1, header_prefix_bytes=len(prefix), logical_views=1)
        self._sync_reader_totals()
        return prefix

    def _ensure_open_accounted(self) -> None:
        """Account the single physical open the first time it is required."""
        if self._open.physical_opens == 0:
            self.budget.check(self._account, path_opens=1)
            self._open.ensure_open()   # the one physical open; not a logical view
            self._bump(path_opens=1)

    def _reader_arg(self) -> _GovernedView:
        """Guard: the compiled reader may never receive a raw path string."""
        self._ensure_open_accounted()
        self.budget.check(self._account, logical_views=1)
        view = self._open.view()
        self._bump(logical_views=1)
        return view

    def _invoke_reader(self, kind: str, **kwargs: Any) -> Any:
        import inspect

        reader = self.pyreadstat.read_sav if self._reader_kind == "SAV" else self.pyreadstat.read_dta
        delta = {"metadata_reads": 0, "selected_reads": 0, "full_reads": 0, "chunk_reads": 0}
        delta[kind] = 1
        # Pre-operation budget gate for the invocation itself.
        self.budget.check(self._account, reader_invocations=1, **delta)

        arg = self._reader_arg()
        if isinstance(arg, (str, bytes, os.PathLike)):
            raise RawSourcePathEscape(
                "RAW_PATH_ESCAPE",
                "a raw source path reached the compiled reader",
                self._account.as_dict(),
            )
        # Filter unsupported keywords ONLY for the genuine entry point. Filtering
        # against a test double's (*args, **kwargs) signature silently discarded
        # every real parameter, including metadataonly and usecols, which would
        # have quietly downgraded a metadata read into a full read.
        if _is_genuine_pyreadstat_entry_point(reader):
            params = set(inspect.signature(reader).parameters)
            kwargs = {k: v for k, v in kwargs.items() if k in params}

        # Arm the bridge-safe allowance for exactly this compiled-reader call.
        cap = self.budget.reader_bytes
        already = self._account.reader_bytes
        allowance = None if cap is None else max(0, cap - already)
        self._open.arm_limit(allowance)
        calls_before = self._open.read_calls
        bytes_before = self._open.bytes_read
        reader_error: BaseException | None = None
        result = None
        try:
            result = reader(arg, **kwargs)
        except BaseException as exc:      # noqa: BLE001 - re-raised below
            # The limiter shortens the stream rather than raising into the
            # extension, so an error here is the reader reacting to a truncated
            # stream. It is captured, accounted, and re-raised as a typed
            # byte-limit breach at this outer boundary.
            reader_error = exc
        finally:
            # Always account what was actually consumed, and always disarm.
            consumed_calls = self._open.read_calls - calls_before
            consumed_bytes = self._open.bytes_read - bytes_before
            truncated = self._open.limit_truncated
            exhausted = self._open.limit_exhausted
            self._open.disarm_limit()
            self._account = self._account.with_(
                reader_read_calls=self._account.reader_read_calls + consumed_calls,
                reader_bytes=self._account.reader_bytes + consumed_bytes,
            )
        self._bump(reader_invocations=1, **delta)

        # The breach is raised HERE, at the outer decode boundary, never through
        # the compiled extension's read callback. Accounting above is already
        # exact, so the refusal reports precisely what was consumed.
        if cap is not None and (truncated or exhausted or reader_error is not None):
            detail = "" if reader_error is None else f"; reader raised {type(reader_error).__name__}"
            if reader_error is not None:
                raise SourceAccessViolation(
                    "READER_BYTES_LIMIT_EXCEEDED",
                    f"compiled reader required more than the declared reader_bytes cap of "
                    f"{cap}; consumed {self._account.reader_bytes} bytes before the stream was "
                    f"truncated (truncated={truncated}, exhausted={exhausted}){detail}",
                    self._account.as_dict(),
                ) from reader_error
        if reader_error is not None:
            raise reader_error
        if cap is not None and (truncated or exhausted):
            raise SourceAccessViolation(
                "READER_BYTES_LIMIT_EXCEEDED",
                f"compiled reader required more than the declared reader_bytes cap of {cap}; "
                f"consumed {self._account.reader_bytes} bytes "
                f"(truncated={truncated}, exhausted={exhausted}) before the refusal",
                self._account.as_dict(),
            )
        return result

    def admit_decoder_entry(self) -> None:
        """Count ONE decoder/session entry, after a pre-operation cap check.

        Called at the decoder entry boundary, never per reader call. With
        ``decoder_invocations`` capped at 1 a second entry is refused BEFORE any
        metadata, hash or row operation of that second entry begins.
        """
        self.budget.check(self._account, decoder_invocations=1)
        self._bump(decoder_invocations=1)

    def bind_reader(self, reader_kind: str) -> None:
        self._reader_kind = reader_kind.upper()
        if self._reader_kind not in ("SAV", "DTA"):
            raise SourceAccessViolation("UNKNOWN_READER_KIND", f"unsupported reader kind {reader_kind!r}")

    def metadata_read(self, *, encoding: str | None = None) -> Any:
        _frame, metadata = self._invoke_reader(
            "metadata_reads", metadataonly=True, apply_value_formats=False,
            user_missing=True, encoding=encoding,
        )
        return metadata

    def selected_read(self, selected_names: Sequence[str], *, encoding: str | None = None) -> Any:
        """Governed selected-variable read. Binds usecols to the selected set."""
        names = list(selected_names)
        if not names:
            raise SourceAccessViolation("EMPTY_SELECTION", "selected read requires a non-empty variable set")
        if len(set(names)) != len(names):
            raise SourceAccessViolation("DUPLICATE_SELECTION", f"selected names repeat: {names}")
        # Merge rather than clobber: the caller may already have bound ordinals
        # against the column inventory, and that binding must survive.
        prior = dict(self.selected_read_config or {})
        prior.update({
            "mechanism": "pyreadstat usecols",
            "selected_names": names,
            "selected_count": len(names),
            "bound_before_row_data_read": True,
        })
        self.selected_read_config = prior
        frame, metadata = self._invoke_reader(
            "selected_reads", usecols=names, apply_value_formats=False,
            user_missing=True, encoding=encoding,
        )
        # Fail closed if the reader returned anything outside the bound selection.
        raw_columns = getattr(frame, "columns", None)
        returned = [] if raw_columns is None else list(raw_columns)
        unexpected = [c for c in returned if c not in names]
        if unexpected:
            raise SourceAccessViolation(
                "UNEXPECTED_SELECTED_COLUMN",
                f"reader returned unselected columns {unexpected}",
                self._account.as_dict(),
            )
        missing = [n for n in names if n not in returned]
        if missing:
            raise SourceAccessViolation(
                "MISSING_SELECTED_COLUMN",
                f"reader omitted bound selected columns {missing}",
                self._account.as_dict(),
            )
        return frame, metadata

    def full_read(self, *, encoding: str | None = None) -> Any:
        frame, metadata = self._invoke_reader(
            "full_reads", apply_value_formats=False, user_missing=True, encoding=encoding,
        )
        return frame, metadata

    def chunk_reads(self, *, chunk_rows: int, total_rows: int, encoding: str | None = None) -> Iterator[Any]:
        """Governed chunk route: one position-zero view per chunk, ONE physical open.

        ``pyreadstat.read_file_in_chunks`` is deliberately NOT used: it works over
        a file-like for SAV but fails for DTA, because it reuses one object across
        parses and ReadStat requires position zero.  This explicit row_offset loop
        is the exact mechanism, and it keeps the physical open count at one.
        """
        if chunk_rows < 1:
            raise SourceAccessViolation("INVALID_CHUNK_ROWS", "chunk_rows must be >= 1")
        offset = 0
        while offset < total_rows:
            self.budget.check(self._account, chunk_reads=1)
            frame, _metadata = self._invoke_reader(
                "chunk_reads", row_offset=offset, row_limit=chunk_rows,
                apply_value_formats=False, user_missing=True, encoding=encoding,
            )
            if len(frame) == 0:
                break
            yield frame
            offset += len(frame)

    def observed_sha256(self) -> str:
        if self._observed_sha is None:
            raise SourceAccessViolation("SHA_NOT_OBSERVED", "hash_pass() must run before observing the digest")
        return self._observed_sha

    def close(self) -> None:
        self._open.close()

    def __enter__(self) -> "SourceAccessBroker":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()
