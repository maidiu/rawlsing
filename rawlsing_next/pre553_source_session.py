"""Governed per-source execution session owner for the PRE553 substrate.

Why this module exists
----------------------
The accepted broker scope was a single ``_decode()`` call: the broker was
constructed inside the decode, so the lifecycle and the aggregate accounts lived
one call deep.  R9 needs an explicit owner whose scope is a *bound source entry*,
created once and reused for every admitted operation in that scope.

This module supplies that owner, and nothing else.  It contains:

  * ``RowDataMode`` -- a typed plan discriminator distinguishing METADATA_ONLY,
    SELECTED, FULL and CHUNKED_FULL.  These are independent operations and are
    accounted independently.
  * ``SourceOperationPlan`` -- the generic plan.  It holds NO source-specific
    constants: nothing here encodes SRC02/SRC06/SRC14/SRC27 policy, because the
    documentary lanes have not adjudicated those plans.
  * ``GovernedSourceSession`` -- the owner.  One broker, one physical open, one
    aggregate receipt, one decoder-invocation account, deterministic close.

Two corrections this owner exists to make
-----------------------------------------
1. **Encoding is independent of row-data mode.**  Previously a non-null encoding
   alone forced a full row-data read.  Here ``encoding`` is a reader
   configuration value; the row-data mode is decided solely by the plan.  A
   METADATA_ONLY plan with a declared encoding performs metadata admission and
   ZERO full or selected row-data reads.

2. **Header-prefix access is explicit.**  A prefix read happens only when the
   plan admits a ``header_prefix_bytes`` size.  ``None`` means no prefix access
   at all, and that is recorded as its own account rather than inferred.

``decoder_invocations`` is NOT ``reader_invocations``.  One decoder entry may
issue several reader calls; one reader call is never a decoder entry.  Both are
separate accounts with separate budgets.

Nothing here interprets survey meaning.  Missingness, typed values, authority and
witness truth are unchanged; this module only decides how the source bytes are
reached and how the access is accounted.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
import os
from pathlib import Path
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_source_access_broker import (
    BROKER_IMPLEMENTATION_ID,
    RawSourcePathEscape,
    SourceAccessAccount,
    SourceAccessBroker,
    SourceAccessBudget,
    SourceAccessViolation,
)

__all__ = [
    "SESSION_IMPLEMENTATION_ID",
    "RowDataMode",
    "SourceOperationPlan",
    "GovernedSourceSession",
    "SessionPlanError",
    "SESSION_CLOSED",
]

SESSION_IMPLEMENTATION_ID = "rawlsing_next/pre553_source_session.py"
SESSION_CLOSED = "SESSION_CLOSED__BROKER_RELEASED"


class SessionPlanError(ValueError):
    """The requested plan is not internally coherent. Raised before any access."""


class RowDataMode(str, Enum):
    """Typed row-data discriminator. Each value is a DIFFERENT operation."""

    METADATA_ONLY = "METADATA_ONLY"
    SELECTED = "SELECTED"
    FULL = "FULL"
    CHUNKED_FULL = "CHUNKED_FULL"


# Which reader account each mode drives. A mode is never conflated with another.
_MODE_READER_ACCOUNT: Mapping[RowDataMode, str] = {
    RowDataMode.METADATA_ONLY: "metadata_reads",
    RowDataMode.SELECTED: "selected_reads",
    RowDataMode.FULL: "full_reads",
    RowDataMode.CHUNKED_FULL: "chunk_reads",
}


@dataclass(frozen=True)
class SourceOperationPlan:
    """A generic, source-agnostic operation plan.

    Deliberately free of any SRCxx constant. A caller binds the plan; this module
    never decides what a particular source's plan is.
    """

    mode: RowDataMode
    # SELECTED only. Names are bound against the real column inventory before any
    # row-data read; ordinals are recorded when bound.
    selected_variables: tuple[str, ...] | None = None
    # integer size, or None meaning NO header-prefix access whatsoever.
    header_prefix_bytes: int | None = None
    # Reader configuration, INDEPENDENT of the row-data mode. A non-null encoding
    # does not by itself authorise a full read.
    encoding: str | None = None
    # Rows per chunk for CHUNKED_FULL.
    chunk_rows: int | None = None
    max_retries: int = 0
    # Optional separately typed outer account, e.g. a full-route/pass token.
    outer_account_token: str | None = None

    def __post_init__(self) -> None:
        if self.mode is RowDataMode.SELECTED:
            if not self.selected_variables:
                raise SessionPlanError("SELECTED plan requires a non-empty selected_variables set")
            if len(set(self.selected_variables)) != len(self.selected_variables):
                raise SessionPlanError("SELECTED plan repeats a selected variable name")
        elif self.selected_variables:
            raise SessionPlanError(
                f"selected_variables is only meaningful for SELECTED, not {self.mode.value}")
        if self.header_prefix_bytes is not None:
            if not isinstance(self.header_prefix_bytes, int) or isinstance(self.header_prefix_bytes, bool):
                raise SessionPlanError("header_prefix_bytes must be an integer or None")
            if self.header_prefix_bytes < 0:
                raise SessionPlanError("header_prefix_bytes must not be negative")
        if self.mode is RowDataMode.CHUNKED_FULL:
            if self.chunk_rows is None or self.chunk_rows < 1:
                raise SessionPlanError("CHUNKED_FULL plan requires chunk_rows >= 1")
        elif self.chunk_rows is not None:
            raise SessionPlanError(f"chunk_rows is only meaningful for CHUNKED_FULL, not {self.mode.value}")
        if self.max_retries < 0:
            raise SessionPlanError("max_retries must not be negative")

    # -- derived, typed views ------------------------------------------------
    @property
    def reader_account(self) -> str:
        """The single reader account this plan drives."""
        return _MODE_READER_ACCOUNT[self.mode]

    @property
    def admits_row_data(self) -> bool:
        return self.mode is not RowDataMode.METADATA_ONLY

    @property
    def admits_header_prefix(self) -> bool:
        return self.header_prefix_bytes is not None

    def as_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode.value,
            "reader_account_driven": self.reader_account,
            "selected_variables": list(self.selected_variables) if self.selected_variables else None,
            "header_prefix_bytes": self.header_prefix_bytes,
            "admits_header_prefix": self.admits_header_prefix,
            "encoding": self.encoding,
            "encoding_is_independent_of_row_data_mode": True,
            "chunk_rows": self.chunk_rows,
            "max_retries": self.max_retries,
            "outer_account_token": self.outer_account_token,
        }


class GovernedSourceSession:
    """Owner of one bound source-entry lifecycle.

    Created once per caller-bound source entry and reused for every admitted
    operation in that scope. Owns exactly one SourceAccessBroker and therefore
    exactly one physical open, which is preserved across all operations.
    """

    def __init__(
        self,
        *,
        source_entry_key: str,
        path: str | os.PathLike[str],
        expected_source_sha256: str | None = None,
        source_format: str,
        budget: SourceAccessBudget | None = None,
        pyreadstat_module: Any | None = None,
        reader_options: Mapping[str, Any] | None = None,
    ) -> None:
        if not isinstance(source_entry_key, str) or not source_entry_key.strip():
            raise SessionPlanError("source_entry_key must be a non-empty string")
        self.source_entry_key = source_entry_key
        self.path = Path(path)
        self.source_format = str(source_format).upper()
        self.expected_source_sha256 = expected_source_sha256
        self.reader_options = dict(reader_options or {})
        self._broker = SourceAccessBroker(
            self.path,
            budget=budget if budget is not None else SourceAccessBudget(),
            expected_source_sha256=None,      # identity is asserted by this owner
            pyreadstat_module=pyreadstat_module,
        )
        self._broker.bind_reader(self.source_format)
        self._closed = False
        self._admitted_plans: list[SourceOperationPlan] = []
        self._selected_ordinals: dict[str, tuple[int, ...]] = {}

    # -- lifecycle -----------------------------------------------------------
    @property
    def broker(self) -> SourceAccessBroker:
        return self._broker

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def admitted_plans(self) -> tuple[SourceOperationPlan, ...]:
        return tuple(self._admitted_plans)

    def _require_open(self) -> None:
        if self._closed:
            raise SourceAccessViolation("SESSION_CLOSED", "this session has been closed")

    def __enter__(self) -> "GovernedSourceSession":
        self._require_open()
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def close(self) -> None:
        """Deterministic close. Idempotent, and safe on both normal and error paths."""
        if self._closed:
            return
        self._closed = True
        self._broker.close()

    # -- accounts ------------------------------------------------------------
    @property
    def account(self) -> SourceAccessAccount:
        return self._broker.account

    def account_dict(self) -> dict[str, int]:
        return self._broker.account_dict()

    def aggregate_receipt(self) -> dict[str, Any]:
        """LIVE aggregate receipt for this source entry.

        Built from the broker on each access so it reflects every operation
        performed so far, including chunk reads issued later.
        """
        receipt = self._broker.receipt()
        receipt["schema"] = "PRE553_GOVERNED_SOURCE_SESSION@1.0.0"
        receipt["session_implementation"] = SESSION_IMPLEMENTATION_ID
        receipt["source_entry_key"] = self.source_entry_key
        receipt["source_format"] = self.source_format
        receipt["session_closed"] = self._closed
        receipt["admitted_plans"] = [p.as_dict() for p in self._admitted_plans]
        receipt["selected_ordinals"] = {k: list(v) for k, v in self._selected_ordinals.items()}
        receipt["account_ownership"] = {
            "account_owner": "session",
            "one_broker_per_session": True,
            "decoder_invocations_vs_reader_invocations": "separate accounts; the former counts entry-boundary crossings, the latter counts compiled-reader calls",
        }
        return receipt

    # -- the governed operation ----------------------------------------------
    def run(self, plan: SourceOperationPlan) -> dict[str, Any]:
        """Execute one admitted plan under this session.

        Every branch records exactly the account its mode names. Encoding is
        applied to the reader configuration and NEVER selects a row-data mode.
        """
        self._require_open()
        if not isinstance(plan, SourceOperationPlan):
            raise SessionPlanError("run() requires a SourceOperationPlan")

        # Decoder entry boundary: counted once here, and refused BEFORE any
        # metadata, hash or row operation when the cap is 1.
        self._broker.admit_decoder_entry()

        # Identity: one existence check and one whole-file hash pass per session.
        if not self._broker.existence_check():
            raise SourceAccessViolation("SOURCE_BYTES_UNAVAILABLE",
                                        f"source bytes unavailable: {self.path}")
        observed_sha = self._broker.hash_pass()
        if self.expected_source_sha256 is not None and observed_sha != self.expected_source_sha256:
            raise SourceAccessViolation(
                "SOURCE_SHA256_MISMATCH",
                f"observed {observed_sha} does not match the bound identity for {self.source_entry_key}")

        encoding = plan.encoding
        out: dict[str, Any] = {
            "plan": plan.as_dict(),
            "source_sha256": observed_sha,
            "metadata": None,
            "frame": None,
            "selected_ordinals": None,
            "header_prefix": None,
            "chunk_frames": None,
        }

        # ---- METADATA_ONLY: metadata admission and NOTHING else.
        # A declared encoding is passed to the reader configuration but must not
        # promote this into a row-data read.
        out["metadata"] = self._broker.metadata_read(encoding=encoding)

        if plan.mode is RowDataMode.METADATA_ONLY:
            self._finish(plan, out)
            return out

        # ---- SELECTED: bind names/ordinals against the real inventory first.
        if plan.mode is RowDataMode.SELECTED:
            names = list(plan.selected_variables or ())
            columns = list(getattr(out["metadata"], "column_names", []) or [])
            ordinals = {n: i for i, n in enumerate(columns, 1)}
            missing = [n for n in names if n not in ordinals]
            if missing:
                raise SourceAccessViolation(
                    "SELECTED_VARIABLES_ABSENT",
                    f"selected variables absent from the bound source: {missing}")
            bound = tuple(ordinals[n] for n in names)
            self._selected_ordinals[self.source_entry_key] = bound
            self._broker.selected_read_config = {
                "mechanism": "pyreadstat usecols",
                "selected_names": names,
                "bound_ordinals": list(bound),
                "bound_before_row_data_read": True,
                "selected_count": len(names),
            }
            frame, metadata = self._broker.selected_read(names, encoding=encoding)
            out["frame"] = frame
            out["metadata"] = metadata
            out["selected_ordinals"] = bound
            self._finish(plan, out)
            return out

        # ---- FULL: exactly one full reader invocation, distinct from chunking.
        if plan.mode is RowDataMode.FULL:
            frame, metadata = self._broker.full_read(encoding=encoding)
            out["frame"] = frame
            out["metadata"] = metadata
            self._finish(plan, out)
            return out

        # ---- CHUNKED_FULL: explicit row_offset loop, one view per chunk.
        total = int(getattr(out["metadata"], "number_rows", 0) or 0)
        frames = []
        for frame in self._broker.chunk_reads(
            chunk_rows=int(plan.chunk_rows or 1), total_rows=total, encoding=encoding,
        ):
            frames.append(frame)
        out["chunk_frames"] = frames
        self._finish(plan, out)
        return out

    def _finish(self, plan: SourceOperationPlan, out: dict[str, Any]) -> None:
        # Header-prefix access ONLY when the plan admits a size.
        if plan.admits_header_prefix:
            out["header_prefix"] = self._broker.header_prefix(int(plan.header_prefix_bytes or 0))
        self._admitted_plans.append(plan)
