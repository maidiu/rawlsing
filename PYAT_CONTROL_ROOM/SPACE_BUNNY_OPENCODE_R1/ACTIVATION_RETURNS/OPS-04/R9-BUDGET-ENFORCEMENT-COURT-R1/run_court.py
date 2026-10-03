"""R9 budget enforcement court — driver.

Runs the exact current decoder against synthetic carriers only, under the
typed ledger and the C3 pre-operation guard. Emits machine-readable results.

Source-free. Reads and writes ONLY synthetic carriers created by
`synthetic_carriers.py` in a temporary directory. Never touches a real survey
file, a locator, or any raw source directory.
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


def _attempt(fn: Callable_ish, *a: Any, **k: Any) -> dict[str, Any]:
    try:
        value = fn(*a, **k)
        return {"outcome": "COMPLETED", "detail": _describe(value)}
    except r9be.BudgetExceeded as exc:
        return {
            "outcome": "ABORTED_BY_C3_GUARD",
            "detail": {
                "account": exc.account,
                "attempted": exc.attempted,
                "c3_maximum": exc.maximum,
                "underlying_operation_executed": False,
            },
        }
    except Exception as exc:  # decoder fail-closed paths
        return {
            "outcome": "REFUSED_FAIL_CLOSED",
            "detail": {"error_type": type(exc).__name__, "message": str(exc)[:200]},
        }


def _describe(value: Any) -> dict[str, Any]:
    return {
        "type": type(value).__name__,
        "row_count": int(getattr(value, "row_count", 0) or 0),
        "variable_count": len(getattr(value, "variables", ()) or ()),
        "source_sha256": getattr(value, "source_sha256", None),
    }


from typing import Callable as Callable_ish  # noqa: E402  (used in annotation above)


def run() -> dict[str, Any]:
    from rawlsing_next.pre553_physical_decoder import DecoderError, decode_dta, decode_sav

    results: dict[str, Any] = {
        "schema": "PYAT_HQ191_R9_BUDGET_COURT_OBSERVATIONS@1.0.0",
        "source_free": True,
        "real_source_access": 0,
        "locator_discovery": 0,
        "carriers": {},
        "probes": {},
        "observability": {},
        "category_law": {
            "C1_historical": "read only from frozen artifacts; this court writes nothing here",
            "C2_observed_synthetic": "measured below on synthetic carriers only; not evidence about any real survey file",
            "C3_policy_maxima": "proposed authorization ceilings supplied to the guard; safety constraints, not claims about history",
        },
    }

    with tempfile.TemporaryDirectory(prefix="r9court-") as tmp:
        manifest = sc.generate(tmp)
        results["carriers"] = manifest

        sav = manifest["SYN_SAV_TINY"]["path"]
        dta = manifest["SYN_DTA_TINY"]["path"]

        # ---- P1: SAV metadata-only success, UNBOUNDED (measure C2) ----
        with r9be.governed_probe("SYN_SAV_TINY", {}) as led:
            r = _attempt(decode_sav, sav)
            results["probes"]["P1_sav_metadata_success_unbounded"] = {
                "attempt": r,
                "ledger": led.snapshot(),
            }

        # ---- P2: DTA metadata-only success, UNBOUNDED (measure C2) ----
        with r9be.governed_probe("SYN_DTA_TINY", {}) as led:
            r = _attempt(decode_dta, dta)
            results["probes"]["P2_dta_metadata_success_unbounded"] = {
                "attempt": r,
                "ledger": led.snapshot(),
            }

        # ---- P3: fail-closed on SHA mismatch (decoder's own law) ----
        with r9be.governed_probe("SYN_SAV_TINY", {}) as led:
            r = _attempt(decode_sav, sav, expected_source_sha256="0" * 64)
            results["probes"]["P3_sav_sha_mismatch_fail_closed"] = {
                "attempt": r,
                "ledger": led.snapshot(),
                "expected": "DecoderError, and NO reader invocation should have occurred",
            }

        # ---- P4: fail-closed on unlisted encoding (compatibility gate) ----
        with r9be.governed_probe("SYN_SAV_TINY", {}) as led:
            r = _attempt(decode_sav, sav, encoding="latin1")
            results["probes"]["P4_sav_unlisted_encoding_refused"] = {
                "attempt": r,
                "ledger": led.snapshot(),
                "expected": "DecoderError because synthetic SHA is not in COMPATIBILITY_ALLOWLIST",
            }

        # ---- P5: compatibility full-read branch, in-memory injection ----
        # C4C3 precedent: measure the unmodified fail-closed behaviour FIRST
        # (probe P4 above), then extend the allowlist IN MEMORY ONLY, disclose
        # it, and revert. This is the only way to exercise the SRC27-shaped
        # full compatibility read without a real source.
        from rawlsing_next import pre553_physical_decoder as dec

        original_allowlist = dict(dec.COMPATIBILITY_ALLOWLIST)
        injection_disclosed = True
        try:
            sha = manifest["SYN_SAV_TINY"]["sha256"]
            dec.COMPATIBILITY_ALLOWLIST[sha] = "latin1"
            with r9be.governed_probe("SYN_SAV_TINY_COMPAT_INJECTED", {}) as led:
                r = _attempt(decode_sav, sav, encoding="latin1")
                results["probes"]["P5_sav_compat_full_read_injected"] = {
                    "attempt": r,
                    "ledger": led.snapshot(),
                    "harness_injection": {
                        "disclosed": injection_disclosed,
                        "what": "COMPATIBILITY_ALLOWLIST extended in memory with the synthetic carrier's own SHA",
                        "why": "the SRC27-shaped compatibility read is gated on an exact SHA that only a real source has",
                        "reverted_after_probe": True,
                        "production_mutated": False,
                    },
                    "expected": "BOTH a metadata read AND a full read AND a frame materialization",
                }
        finally:
            dec.COMPATIBILITY_ALLOWLIST.clear()
            dec.COMPATIBILITY_ALLOWLIST.update(original_allowlist)

        results["allowlist_restored_after_injection"] = (
            dec.COMPATIBILITY_ALLOWLIST == original_allowlist
        )

        # ---- P6..P8: C3 guard must abort BEFORE the next operation ----
        # A single _decode performs each layer class exactly ONCE, so a
        # maximum of 1 authorises the whole first decode. The enforcement
        # property under test is therefore: with a budget of exactly 1, the
        # SECOND decode of that source must abort at the guarded layer
        # WITHOUT the underlying operation executing.
        p1_counts = results["probes"]["P1_sav_metadata_success_unbounded"]["ledger"]["c2_observed_counts"]

        for name, account, expect_first, expect_second in (
            ("P6_guard_existence_aborts_second_decode", "source_path_existence_access_check", 1, 1),
            ("P7_guard_hash_aborts_second_decode", "full_file_sha256_pass", 1, 1),
            ("P8_guard_metadata_read_aborts_second_decode", "reader_invocation_metadata_read", 1, 1),
        ):
            with r9be.governed_probe("SYN_SAV_TINY_GUARD", {account: 1}) as led:
                first = _attempt(decode_sav, sav)
                second = _attempt(decode_sav, sav)
                results["probes"][name] = {
                    "c3_maxima_set": {account: 1},
                    "guarded_account": account,
                    "first_decode": first,
                    "second_decode": second,
                    "ledger": led.snapshot(),
                    "expected": {
                        "first_outcome": "COMPLETED",
                        "second_outcome": "ABORTED_BY_C3_GUARD",
                        "second_underlying_operation_executed": False,
                    },
                    "verdict": (
                        "ENFORCED_BEFORE_OPERATION"
                        if first["outcome"] == "COMPLETED"
                        and second["outcome"] == "ABORTED_BY_C3_GUARD"
                        and second["detail"].get("underlying_operation_executed") is False
                        else "NOT_DEMONSTRATED"
                    ),
                }

        # ---- P9: retry accounting, governed zero-retry law ----
        # P9a: C3 maximum retries = 0 (the governing law). The FIRST retry
        # authorization must abort BEFORE any second decode runs.
        with r9be.governed_probe("SYN_SAV_TINY_RETRY0", {"retry": 0}) as led:
            first = _attempt(decode_sav, sav)
            retry_attempt = _attempt(led.check_and_authorize, "retry")
            results["probes"]["P9a_zero_retry_enforced"] = {
                "first_invocation": first,
                "first_retry_authorization": retry_attempt,
                "ledger": led.snapshot(),
                "key_property": "with retries capped at 0 the retry is refused and no second decode is attempted",
            }

        # P9b: C3 maximum retries = 1, to show a retry is separately
        # accountable and is NOT free - it consumes further layer budgets.
        with r9be.governed_probe("SYN_SAV_TINY_RETRY1", {"retry": 1}) as led:
            first = _attempt(decode_sav, sav)
            led.record("retry", {"ordinal": 1})
            second = _attempt(decode_sav, sav)
            results["probes"]["P9b_one_retry_consumes_further_budget"] = {
                "first_invocation": first,
                "second_invocation": second,
                "ledger": led.snapshot(),
                "key_property": "the retry added a further existence check, hash pass and reader invocation",
            }

        # ---- Observability: can Python see the reader's own opens? ----
        results["observability"]["os_open_probe"] = r9be.os_open_observability_probe(sav)

    return results


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))