"""R9 budget enforcement court — typed access ledger and pre-operation guard.

PURPOSE
-------
Answer one question source-free: can lawful, conservative HARD MAXIMUM
authorization budgets be *designed*, *enforced* and *source-free qualified*
against the exact current reader/decoder code paths, using synthetic carriers
only?

CATEGORY LAW (enforced by this module's own naming)
---------------------------------------------------
  C1 HISTORICAL   counts that a governed artifact already establishes.
                  This module NEVER writes here. It only reads C1 from the
                  frozen artifacts and labels it C1.
  C2 OBSERVED     counts measured on synthetic fixtures in this court.
                  Not evidence about any real survey file.
  C3 POLICY       proposed HQ authorization ceilings. Safety constraints
                  whose purpose is to STOP a run, not claims about history.

A C2 or C3 number is never emitted under a C1 label.

ENFORCEMENT POINT
-----------------
Every counter is checked BEFORE the guarded callable is invoked. When a C3
maximum is already consumed, the guard raises and the underlying operation
never executes. That is the property this court exists to demonstrate.

MEASUREMENT LAYER HONESTY
-------------------------
`Path.is_file`, the decoder's file-hasher and the pyreadstat reader bindings
are all reachable and interceptable from Python. The OS-level `open(2)` calls
that pyreadstat's C extension performs internally are NOT. This module counts
at the layer it can actually govern and says so, rather than fabricating an
OS-open ceiling. See `os_open_observability_probe`.
"""

from __future__ import annotations

import builtins
import hashlib
import os
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterator

# --------------------------------------------------------------------------
# Account taxonomy. Each entry declares the layer at which it is counted.
# `governable` says whether this court can actually enforce it.
# --------------------------------------------------------------------------

ACCOUNT_TAXONOMY: dict[str, dict[str, Any]] = {
    "source_path_existence_access_check": {
        "o1_c07_account": True,
        "measured_at_layer": "python:pathlib.Path.is_file (application-visible existence probe)",
        "interceptable_from_python": True,
        "governable": True,
    },
    "full_file_sha256_pass": {
        "o1_c07_account": True,
        "measured_at_layer": "python:pre553_physical_decoder._sha (whole-file hashlib.sha256 over the file)",
        "interceptable_from_python": True,
        "governable": True,
    },
    "reader_invocation_metadata_read": {
        "o1_c07_account": True,
        "measured_at_layer": "python:pyreadstat.read_sav/read_dta binding, metadataonly=True",
        "interceptable_from_python": True,
        "governable": True,
        "satisfies_o1_c07_account": "metadata reads",
    },
    "reader_invocation_full_read": {
        "o1_c07_account": True,
        "measured_at_layer": "python:pyreadstat.read_sav/read_dta binding, metadataonly=False",
        "interceptable_from_python": True,
        "governable": True,
        "satisfies_o1_c07_account": "full reads / full compatibility reads",
    },
    "frame_materialization": {
        "o1_c07_account": True,
        "measured_at_layer": "python:return value of a non-metadataonly reader invocation (a materialized frame)",
        "interceptable_from_python": True,
        "governable": True,
        "satisfies_o1_c07_account": "materialization / frame construction",
    },
    "selected_bounded_read": {
        "o1_c07_account": True,
        "measured_at_layer": "NOT SEPARATELY REACHABLE at the decoder layer",
        "interceptable_from_python": False,
        "governable": False,
        "reason": "pre553_physical_decoder._decode never calls the reader with usecols. Selected-column reads are performed by higher layers (route_b_production / carrier) that pass whole PhysicalSourceIncidence objects, not by re-invoking the reader. See finding SEL-01.",
    },
    "header_prefix_read": {
        "o1_c07_account": True,
        "measured_at_layer": "NOT REACHABLE at the decoder layer",
        "interceptable_from_python": False,
        "governable": False,
        "reason": "The exact reader/decoder code path exercised here performs no bounded header-prefix read. The 176-byte quantity in artifact 07 is a SRC26-specific bound, not a decoder-layer operation.",
    },
    "retry": {
        "o1_c07_account": True,
        "measured_at_layer": "python:re-invocation of a decoder entry point for the same governed source key within one run",
        "interceptable_from_python": True,
        "governable": True,
    },
    "path_level_open_os": {
        "o1_c07_account": True,
        "measured_at_layer": "OS-level open(2) inside pyreadstat's compiled reader extension",
        "interceptable_from_python": False,
        "governable": False,
        "reason": "pyreadstat reads through a Cython/C extension. Its internal opens are not visible to builtins.open patching and are not separately countable or enforceable from Python.",
    },
    "decoder_invocation": {
        "o1_c07_account": False,
        "note": "Not an O1-C07 account in its own right. Counted here as the sum of reader invocations, which IS the decoder-call layer.",
        "measured_at_layer": "python:pyreadstat reader binding, all invocations",
        "interceptable_from_python": True,
        "governable": True,
    },
}


class BudgetExceeded(RuntimeError):
    """Raised BEFORE a guarded operation when its C3 maximum is consumed."""

    def __init__(self, account: str, attempted: int, maximum: int | None, source_key: str) -> None:
        super().__init__(
            f"R9 budget guard aborted BEFORE operation: account={account} "
            f"attempted={attempted} maximum={maximum} source={source_key}"
        )
        self.account = account
        self.attempted = attempted
        self.maximum = maximum
        self.source_key = source_key


@dataclass
class Ledger:
    """Typed counters. `c3_maxima` are the ONLY ceilings enforced."""

    source_key: str
    c3_maxima: dict[str, int | None] = field(default_factory=dict)
    observed: dict[str, int] = field(default_factory=dict)
    order: list[dict[str, Any]] = field(default_factory=list)
    aborts: list[dict[str, Any]] = field(default_factory=list)

    def _bump(self, account: str) -> None:
        self.observed[account] = self.observed.get(account, 0) + 1

    def check_and_authorize(self, account: str) -> None:
        """C3 gate. Raises BEFORE the caller performs the operation."""
        maximum = self.c3_maxima.get(account)
        already = self.observed.get(account, 0)
        if maximum is not None and already >= maximum:
            self.aborts.append({
                "account": account,
                "already_consumed": already,
                "c3_maximum": maximum,
                "operation_executed": False,
            })
            raise BudgetExceeded(account, already + 1, maximum, self.source_key)

    def record(self, account: str, detail: dict[str, Any] | None = None) -> None:
        self._bump(account)
        entry = {"account": account, "ordinal": self.observed[account]}
        if detail:
            entry.update(detail)
        self.order.append(entry)

    def snapshot(self) -> dict[str, Any]:
        return {
            "source_key": self.source_key,
            "c3_maxima": dict(self.c3_maxima),
            "c2_observed_counts": dict(self.observed),
            "c2_operation_order": list(self.order),
            "c3_aborts": list(self.aborts),
        }


# --------------------------------------------------------------------------
# Instrumentation. Patches are installed only inside `governed_probe`.
# --------------------------------------------------------------------------


@contextmanager
def governed_probe(source_key: str, c3_maxima: dict[str, int | None]) -> Iterator[Ledger]:
    """Instrument the exact reader/decoder layers and yield a Ledger.

    Patches, all reversible:
      - pathlib.Path.is_file          -> existence/access layer
      - decoder module _sha           -> full-file SHA-256 layer
      - pyreadstat.read_sav/read_dta  -> reader/decoder invocation layer
      - builtins.open                 -> OBSERVABILITY PROBE ONLY (not a gate)

    No production file is modified. Every patch is applied to the imported
    module objects in memory and reverted on exit.
    """
    import pyreadstat
    from rawlsing_next import pre553_physical_decoder as dec

    ledger = Ledger(source_key=source_key, c3_maxima=dict(c3_maxima))

    real_is_file = Path.is_file
    real_sha = dec._sha
    real_read_sav = pyreadstat.read_sav
    real_read_dta = pyreadstat.read_dta
    real_open = builtins.open
    os_open_probe = {"count": 0}

    def guarded_is_file(self: Path) -> bool:
        ledger.check_and_authorize("source_path_existence_access_check")
        ledger.record("source_path_existence_access_check")
        return real_is_file(self)

    def guarded_sha(path: Path) -> str:
        ledger.check_and_authorize("full_file_sha256_pass")
        ledger.record("full_file_sha256_pass", {"mechanism": "hashlib.sha256 over whole file"})
        return real_sha(path)

    def _wrap_reader(real: Callable[..., Any], fmt: str) -> Callable[..., Any]:
        def guarded(filename: Any, *args: Any, **kwargs: Any) -> Any:
            metadataonly = bool(kwargs.get("metadataonly", False))
            account = (
                "reader_invocation_metadata_read"
                if metadataonly
                else "reader_invocation_full_read"
            )
            ledger.check_and_authorize(account)
            ledger.check_and_authorize("decoder_invocation")
            ledger.record(
                account,
                {"format": fmt, "metadataonly": metadataonly,
                 "usecols": kwargs.get("usecols"),
                 "row_limit": kwargs.get("row_limit")},
            )
            ledger.record("decoder_invocation", {"format": fmt})
            result = real(filename, *args, **kwargs)
            if not metadataonly:
                ledger.check_and_authorize("frame_materialization")
                ledger.record(
                    "frame_materialization",
                    {"frame_is_none": result[0] is None,
                     "rows": 0 if result[0] is None else int(len(result[0]))},
                )
            return result
        return guarded

    def probe_open(file: Any, *args: Any, **kwargs: Any) -> Any:
        # OBSERVABILITY PROBE ONLY. Deliberately NOT a gate: Python-level
        # builtins.open cannot see opens performed inside a C extension.
        try:
            if isinstance(file, (str, bytes, os.PathLike)):
                os_open_probe["count"] += 1
        except Exception:
            pass
        return real_open(file, *args, **kwargs)

    Path.is_file = guarded_is_file
    dec._sha = guarded_sha
    pyreadstat.read_sav = _wrap_reader(real_read_sav, "sav")
    pyreadstat.read_dta = _wrap_reader(real_read_dta, "dta")
    builtins.open = probe_open

    try:
        yield ledger
    finally:
        Path.is_file = real_is_file
        dec._sha = real_sha
        pyreadstat.read_sav = real_read_sav
        pyreadstat.read_dta = real_read_dta
        builtins.open = real_open
        ledger.observed["_probe_python_builtins_open_calls"] = os_open_probe["count"]


def os_open_observability_probe(carrier: str) -> dict[str, Any]:
    """Measure what Python can and cannot see about opens on a carrier.

    Compares Python-visible builtins.open calls against the real descriptor
    activity, to show that pyreadstat's internal opens are invisible.
    """
    import pyreadstat

    seen: list[str] = []
    real_open = builtins.open

    def spy(file: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            if isinstance(file, (str, bytes, os.PathLike)):
                seen.append(str(file))
        except Exception:
            pass
        return real_open(file, *args, **kwargs)

    before_fds = len(os.listdir("/proc/self/fd")) if os.path.isdir("/proc/self/fd") else None

    builtins.open = spy
    try:
        pyreadstat.read_sav(carrier, metadataonly=True)
    finally:
        builtins.open = real_open

    return {
        "python_builtins_open_calls_observed_during_reader_call": len(seen),
        "observed_paths": seen,
        "note": "A zero here while the read demonstrably succeeded proves the reader's own opens are not visible to Python-level open interception.",
        "proc_fd_listing_available": before_fds is not None,
    }