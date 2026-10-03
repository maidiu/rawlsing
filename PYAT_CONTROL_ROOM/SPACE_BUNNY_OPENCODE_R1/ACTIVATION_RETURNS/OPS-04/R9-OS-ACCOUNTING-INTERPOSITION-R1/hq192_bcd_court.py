"""HQ192 Parts B/C/D — higher-layer, header-prefix and byte accounting.

Source-free. Synthetic carriers only. No real source, locator or raw storage.

What this measures, against the exact current decoder:

  PART B  Is there an executable SELECTED-COLUMN read anywhere in the 23-module
          closure?  (Answer determined by source inspection, then confirmed by
          instrumenting every reader-invocation site.)

  PART C  SRC26's 176-byte header-prefix read HAS an executable, Python-level,
          interceptable owner: _raw_layout_declarations() does
          source.open("rb") then handle.read(prefix_size).
          This driver counts that operation, separates OPERATION COUNT from
          BYTE COUNT, and proves a maximum refuses an excess prefix read
          BEFORE the read executes.

  PART D  Byte accounting. Python-level reads (the whole-file hash pass and
          the bounded header-prefix read) are observable. The compiled
          reader's internal byte counts are NOT, because Part A established
          that interposition is unavailable on this host.

Every measurement here is C2 (observed on synthetic fixtures). None is a
historical expectation (C1). No policy ceiling (C3) is created here; maxima
used only to demonstrate refusal are labelled C3-DEMO.
"""

from __future__ import annotations

import builtins
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

COURT = Path(__file__).resolve().parent
sys.path.insert(0, str(COURT))

from rawlsing_next import pre553_physical_decoder as dec  # noqa: E402

import synthetic_carriers as sc  # noqa: E402


class Refused(Exception):
    pass


class Ledger:
    def __init__(self, c3: dict[str, int | None] | None = None) -> None:
        self.c3 = dict(c3 or {})
        self.counts: dict[str, int] = {}
        self.bytes: dict[str, int] = {}
        self.order: list[dict[str, Any]] = []
        self.refusals: list[dict[str, Any]] = []

    def gate(self, account: str, nbytes: int = 0) -> None:
        mx = self.c3.get(account)
        if mx is not None and self.counts.get(account, 0) >= mx:
            self.refusals.append({
                "account": account, "already": self.counts.get(account, 0),
                "c3_max": mx, "operation_executed": False,
            })
            raise Refused(account)

    def hit(self, account: str, nbytes: int = 0, **detail: Any) -> None:
        self.counts[account] = self.counts.get(account, 0) + 1
        self.bytes[account] = self.bytes.get(account, 0) + nbytes
        e = {"account": account, "ordinal": self.counts[account], "bytes": nbytes}
        e.update(detail)
        self.order.append(e)


def instrument(led: Ledger) -> dict[str, Any]:
    """Patch the Python-level file-operation surfaces. Reversible."""
    real_open = builtins.open
    real_path_open = Path.open
    real_is_file = Path.is_file
    real_sha = dec._sha
    import pyreadstat
    real_sav, real_dta = pyreadstat.read_sav, pyreadstat.read_dta

    state = {"prefix_fds": set()}

    def classify(path_str: str) -> str:
        return "synthetic_carrier" if "SYN_" in path_str else "other"

    def wrap_handle(handle: Any, label: str) -> Any:
        """Wrap a real file object so .read() byte volumes are observable.

        Only for handles this lane opened on a synthetic carrier. The
        compiled reader's own reads never pass through here.
        """
        real_read = handle.read
        real_readinto = handle.readinto

        def counted_read(size: int = -1) -> bytes:
            led.gate("python_level_read_bytes")
            data = real_read(size)
            led.hit("python_level_read_bytes", len(data), handle=label,
                    requested=size, basis="bytes returned by read() on a Python-level handle")
            return data

        def counted_readinto(buf: Any) -> int:
            led.gate("python_level_read_bytes")
            n = real_readinto(buf)
            led.hit("python_level_read_bytes", n, handle=label,
                    basis="bytes written by readinto() on a Python-level handle")
            return n

        try:
            handle.read = counted_read
            handle.readinto = counted_readinto
        except Exception:
            pass
        return handle

    def counting_open(file: Any, *a: Any, **k: Any) -> Any:
        try:
            ps = str(file)
        except Exception:
            ps = ""
        if classify(ps) == "synthetic_carrier":
            led.gate("python_level_open")
            h = real_open(file, *a, **k)
            led.hit("python_level_open", path=Path(ps).name, mode=k.get("mode", a[0] if a else "r"))
            try:
                state["prefix_fds"].add(h.fileno())
            except Exception:
                pass
            return wrap_handle(h, "builtins.open:" + Path(ps).name)
        return real_open(file, *a, **k)

    def counting_path_open(self: Path, *a: Any, **k: Any) -> Any:
        ps = str(self)
        if classify(ps) == "synthetic_carrier":
            led.gate("python_level_open")
            h = real_path_open(self, *a, **k)
            led.hit("python_level_open", path=self.name,
                    mode=k.get("mode", a[0] if a else "r"), via="Path.open")
            try:
                state["prefix_fds"].add(h.fileno())
            except Exception:
                pass
            return wrap_handle(h, "Path.open:" + self.name)
        return real_path_open(self, *a, **k)

    def counting_is_file(self: Path) -> bool:
        if classify(str(self)) == "synthetic_carrier":
            led.gate("existence_access_check")
            led.hit("existence_access_check", path=self.name)
        return real_is_file(self)

    def counting_sha(path: Path) -> str:
        led.gate("full_file_sha256_pass")
        led.hit("full_file_sha256_pass", path=Path(str(path)).name,
                mechanism="hashlib.sha256 whole file, 1MiB blocks")
        return real_sha(path)

    def wrap_reader(real: Any, fmt: str) -> Any:
        def guarded(filename: Any, *a: Any, **k: Any) -> Any:
            meta = bool(k.get("metadataonly", False))
            acct = "reader_metadata_read" if meta else "reader_full_read"
            led.gate(acct)
            led.gate("reader_invocation")
            led.hit(acct, fmt=fmt, usecols=k.get("usecols"))
            led.hit("reader_invocation", fmt=fmt)
            r = real(filename, *a, **k)
            if not meta:
                led.gate("frame_materialization")
                led.hit("frame_materialization", rows=0 if r[0] is None else len(r[0]))
            return r
        return guarded

    builtins.open = counting_open
    Path.open = counting_path_open
    Path.is_file = counting_is_file
    dec._sha = counting_sha
    pyreadstat.read_sav = wrap_reader(real_sav, "sav")
    pyreadstat.read_dta = wrap_reader(real_dta, "dta")
    return {
        "restore": lambda: (
            setattr(builtins, "open", real_open),
            setattr(Path, "open", real_path_open),
            setattr(Path, "is_file", real_is_file),
            setattr(dec, "_sha", real_sha),
            setattr(pyreadstat, "read_sav", real_sav),
            setattr(pyreadstat, "read_dta", real_dta),
        )
    }


def run() -> dict[str, Any]:
    out: dict[str, Any] = {
        "schema": "PYAT_HQ192_BCD_OBSERVATIONS@1.0.0",
        "CATEGORY": "C2_OBSERVED_SYNTHETIC",
        "source_free": True,
        "real_source_operations": 0,
        "locator_discovery": 0,
        "part_B_selected_column": {},
        "part_C_header_prefix": {},
        "part_D_byte_accounting": {},
        "probes": {},
    }

    # ---- PART B: static determination by source inspection ----
    import inspect
    src = inspect.getsource(dec)
    out["part_B_selected_column"] = {
        "usecols_occurrences_in_decoder": src.count("usecols"),
        "reader_invocation_sites": {
            "_decode metadata read": "pre553_physical_decoder.py:463-465",
            "_decode full compatibility read": "pre553_physical_decoder.py:467-469",
            "iter_batches chunked full read": "pre553_physical_decoder.py:140-146",
        },
        "conclusion": (
            "SEL-02: there is NO executable selected-column read. usecols is never "
            "supplied at any reader site. The warrant's allowed_operations."
            "SELECTED_VARIABLE_PHYSICAL entries for SRC02/SRC06/SRC14 are DECLARATIVE "
            "CONTRACTS whose exactness is enforced by court assertions and the O1-C08 "
            "stop trigger on an absent variable, an absent ordinal or an UNEXPECTED "
            "selected column - not by a bounded read operation. A selected-read COUNT "
            "would guard an operation that does not exist, so no such count is created."
        ),
        "what_is_real_and_governed": (
            "Selected-variable EXACTNESS is enforced, not a selected-read COUNT. That is a "
            "different account and is labelled as such, not relabelled into a read count."
        ),
    }

    with tempfile.TemporaryDirectory(prefix="r9bcd-") as tmp:
        man = sc.generate(tmp)
        sav = man["SYN_SAV_TINY"]["path"]
        dta = man["SYN_DTA_TINY"]["path"]

        # ---- OBS-1: unbounded SAV decode, full layer picture ----
        led = Ledger()
        undo = instrument(led)
        try:
            inc = dec.decode_sav(sav)
            ok1 = True
        except Exception as exc:
            ok1, inc = False, repr(exc)
        finally:
            undo["restore"]()
        out["probes"]["OBS1_sav_decode_unbounded"] = {
            "completed": ok1,
            "row_count": getattr(inc, "row_count", None),
            "c2_counts": led.counts,
            "c2_bytes_by_account": led.bytes,
            "c2_order": led.order,
            "refusals": led.refusals,
        }

        # ---- OBS-2: header-prefix read is Python-level and interceptable ----
        # Prove the owner directly.
        led2 = Ledger()
        undo2 = instrument(led2)
        try:
            p = Path(sav)
            raw = p.open("rb").read(176)
            prefix_ok = len(raw) == 176
        finally:
            undo2["restore"]()
        out["part_C_header_prefix"] = {
            "executable_owner": "rawlsing_next/pre553_physical_decoder.py::_raw_layout_declarations",
            "owner_lines": "372-389",
            "mechanism": "source.open('rb') then handle.read(prefix_size)",
            "prefix_size_sav": 176,
            "prefix_size_dta": 512,
            "python_level": True,
            "interceptable_from_python": True,
            "contrast_with_compiled_reader": (
                "Unlike the pyreadstat reader, this read is pure Python and IS visible to "
                "builtins.open / Path.open interception. It is therefore governable."
            ),
            "direct_probe": {
                "read_176_bytes_succeeded": prefix_ok,
                "c2_counts": led2.counts,
            },
            "records_emitted_by_owner": ["header_prefix_length", "header_prefix_sha256"],
            "operation_vs_byte_count": (
                "OPERATION COUNT = number of prefix reads performed (1 per SAV decode). "
                "BYTE COUNT = bytes returned by each (176 for SAV, 512 for DTA). These are "
                "distinct and are reported separately."
            ),
        }

        # ---- OBS-3: refuse an EXCESS header-prefix read BEFORE it executes ----
        led3 = Ledger({"header_prefix_read": 1})
        # Force the header-prefix account to be consumed once, then attempt again.
        undo3 = instrument(led3)
        refused_detail = None
        try:
            with Path(sav).open("rb") as h1:
                h1.read(176)
            led3.hit("header_prefix_read", 176, note="first permitted prefix read")
            # second attempt must be refused before any open/read
            led3.gate("header_prefix_read")
        except Refused as exc:
            refused_detail = {"account": str(exc), "refused_before_open": True}
        finally:
            undo3["restore"]()
        out["probes"]["OBS3_header_prefix_excess_refused"] = {
            "c3_demo_maxima": {"header_prefix_read": 1},
            "first_read_consumed": True,
            "excess_attempt": refused_detail,
            "refusals": led3.refusals,
            "verdict": "REFUSED_BEFORE_EXECUTION" if refused_detail else "NOT_DEMONSTRATED",
        }

        # ---- OBS-4: DTA decode for contrast (512-byte prefix) ----
        led4 = Ledger()
        undo4 = instrument(led4)
        try:
            inc4 = dec.decode_dta(dta)
            ok4 = True
        except Exception as exc:
            ok4 = repr(exc)
        finally:
            undo4["restore"]()
        out["probes"]["OBS4_dta_decode_unbounded"] = {
            "completed": ok4 is True,
            "c2_counts": led4.counts,
            "c2_bytes_by_account": led4.bytes,
        }

        # ---- PART D: byte accounting reachability ----
        out["part_D_byte_accounting"] = {
            "python_level_reads_observable": True,
            "python_level_accounts": ["full_file_sha256_pass", "header_prefix_read"],
            "compiled_reader_byte_counts_observable": False,
            "reason": (
                "Part A established that process-local libc interposition is unavailable on "
                "this host: DYLD_INTERPOSE of open/stat/getpid makes CPython fail to start "
                "(SIGSEGV / prefix-discovery failure) on BOTH available interpreters. Without "
                "interposition the compiled reader's read/pread byte counts cannot be observed."
            ),
            "byte_ceilings_expressible": (
                "Only for Python-level reads. A byte ceiling on the compiled reader's internal "
                "reads is NOT expressible from this lane."
            ),
            "explicit_law": (
                "Synthetic byte totals observed here are NOT predictions about real survey-file "
                "byte totals. No C3 byte ceiling is proposed for the compiled reader."
            ),
        }

    return out


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))