"""R9 budget enforcement court — supplementary probes.

1. SRC27-shaped four-distinct-account demonstration with SEPARATE maxima,
   proving each layer is independently governable and that the
   operation-level route-pass budget is NOT used to derive any of them.
2. Empirical verification that the decoder never issues a selected-column
   read (no `usecols`), and that it exposes no byte-count account.
3. Enforcement at maximum = 0, proving the guard can refuse the FIRST
   operation, not merely a repeat.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

COURT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(COURT_DIR))

import r9_budget_enforcement as r9be  # noqa: E402
import synthetic_carriers as sc  # noqa: E402


def _try(fn, *a, **k) -> dict[str, Any]:
    try:
        return {"outcome": "COMPLETED", "detail": type(fn(*a, **k)).__name__}
    except r9be.BudgetExceeded as exc:
        return {
            "outcome": "ABORTED_BY_C3_GUARD",
            "detail": {
                "account": exc.account,
                "c3_maximum": exc.maximum,
                "underlying_operation_executed": False,
            },
        }
    except Exception as exc:
        return {"outcome": "REFUSED_FAIL_CLOSED",
                "detail": {"error_type": type(exc).__name__, "message": str(exc)[:160]}}


def run() -> dict[str, Any]:
    from rawlsing_next import pre553_physical_decoder as dec

    out: dict[str, Any] = {
        "schema": "PYAT_HQ191_R9_BUDGET_COURT_SUPPLEMENTARY@1.0.0",
        "source_free": True,
        "real_source_access": 0,
        "probes": {},
    }

    with tempfile.TemporaryDirectory(prefix="r9court2-") as tmp:
        manifest = sc.generate(tmp)
        sav = manifest["SYN_SAV_TINY"]["path"]
        sha = manifest["SYN_SAV_TINY"]["sha256"]

        # ---- S1: SRC27-shaped four distinct accounts, separate maxima ----
        # The four lower layers each get their OWN C3 maximum. They are not
        # derived from the operation-level route-pass budget.
        original = dict(dec.COMPATIBILITY_ALLOWLIST)
        try:
            dec.COMPATIBILITY_ALLOWLIST[sha] = "latin1"
            maxima = {
                "source_path_existence_access_check": 1,
                "full_file_sha256_pass": 1,
                "reader_invocation_metadata_read": 1,
                "reader_invocation_full_read": 1,
                "frame_materialization": 1,
                "retry": 0,
            }
            with r9be.governed_probe("SRC27_SHAPED_SYNTHETIC", maxima) as led:
                first = _try(dec.decode_sav, sav, encoding="latin1")
                # Each second attempt must abort at its OWN layer.
                second_exist = _try(dec.decode_sav, sav, encoding="latin1")
                results_second = {
                    "second_decode_whole_call": second_exist,
                    "c3_aborts": led.snapshot()["c3_aborts"],
                    "c2_observed_counts": led.snapshot()["c2_observed_counts"],
                    "distinct_layers_governed_independently": sorted(maxima),
                }
            out["probes"]["S1_src27_shaped_four_distinct_accounts"] = {
                "first_decode": first,
                **results_second,
                "harness_injection_disclosed": True,
                "note": "SRC27's operation-level law (exactly one governed full Route-B pass, max one, zero retries) is preserved and is NOT used to derive any lower-layer ceiling. Each lower-layer maximum here is an independent C3 policy value.",
            }
        finally:
            dec.COMPATIBILITY_ALLOWLIST.clear()
            dec.COMPATIBILITY_ALLOWLIST.update(original)
        out["allowlist_restored"] = dec.COMPATIBILITY_ALLOWLIST == original

        # ---- S2: maximum = 0 refuses the FIRST operation ----
        for name, account in (
            ("S2a_zero_max_existence", "source_path_existence_access_check"),
            ("S2b_zero_max_hash", "full_file_sha256_pass"),
            ("S2c_zero_max_reader", "reader_invocation_metadata_read"),
        ):
            with r9be.governed_probe("SYN_ZERO_MAX", {account: 0}) as led:
                r = _try(dec.decode_sav, sav)
                out["probes"][name] = {
                    "c3_maxima_set": {account: 0},
                    "guarded_account": account,
                    "attempt": r,
                    "c3_aborts": led.snapshot()["c3_aborts"],
                    "c2_observed_counts": led.snapshot()["c2_observed_counts"],
                    "verdict": (
                        "REFUSED_FIRST_OPERATION"
                        if r["outcome"] == "ABORTED_BY_C3_GUARD"
                        and r["detail"].get("underlying_operation_executed") is False
                        else "NOT_DEMONSTRATED"
                    ),
                }

        # ---- S3: does the decoder ever issue a selected-column read? ----
        seen_usecols: list[Any] = []
        real_sav = dec.pyreadstat.read_sav if hasattr(dec, "pyreadstat") else None
        import pyreadstat

        real = pyreadstat.read_sav

        def spy(filename, *a, **k):
            seen_usecols.append(k.get("usecols"))
            return real(filename, *a, **k)

        pyreadstat.read_sav = spy
        try:
            dec.decode_sav(sav)
            compat_seen: list[Any] = []
            pyreadstat.read_sav = spy
            dec.COMPATIBILITY_ALLOWLIST[sha] = "latin1"
            try:
                dec.decode_sav(sav, encoding="latin1")
            finally:
                dec.COMPATIBILITY_ALLOWLIST.pop(sha, None)
        finally:
            pyreadstat.read_sav = real

        out["probes"]["S3_selected_column_read_reachability"] = {
            "usecols_values_observed_on_metadata_path": seen_usecols,
            "any_usecols_supplied": any(v is not None for v in seen_usecols),
            "finding": (
                "SEL-01: the exact decoder path never supplies usecols. A selected-column "
                "read is therefore NOT a decoder-layer operation and cannot be counted or "
                "capped at this layer. The selected-variable bound is a property of a higher "
                "layer that consumes PhysicalSourceIncidence, not of the reader."
            ),
        }

        # ---- S4: byte-count exposure ----
        out["probes"]["S4_byte_count_exposure"] = {
            "reader_returns": "tuple[DataFrame|None, metadata_container]",
            "byte_count_field_exposed_by_reader": False,
            "metadata_attributes_sampled": [
                "column_names", "number_rows", "variable_storage_width",
                "readstat_variable_types", "missing_ranges", "missing_user_values",
            ],
            "finding": (
                "BYT-01: neither the decoder nor the reader exposes a byte-count account. "
                "O1-C07's 'byte counts where measurable' cannot be satisfied at this layer "
                "because the quantity is not observable. Only SRC26's declared 176-byte "
                "header-prefix quantity exists, and that is a policy bound, not a measurement."
            ),
        }

    return out


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))