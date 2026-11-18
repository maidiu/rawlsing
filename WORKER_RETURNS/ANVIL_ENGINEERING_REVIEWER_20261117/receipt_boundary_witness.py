"""Review-only ANVIL cut1 actual receipt-boundary revocation and class whitelist witness."""
from __future__ import annotations

from pathlib import Path
import json
import tempfile

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec,
)
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import (
    _fixture as prepared_fixture,
)


def _manifest(queries, predicate, admission):
    units = tuple(
        BatchUnitSpec("QUERY", q.ref, (admission.release_ref,))
        for q in queries.values()
    )
    return BatchManifest(units), {
        q.ref.key: predicate.ref for q in queries.values()
    }


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: receipt_boundary_witness.py <proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("private proofroot required")
    tmp = Path(tempfile.mkdtemp(prefix="anvil-cut1-receipt-", dir=proofroot))
    # A two-query fixture is enough to cross the actual receipt boundary.
    source, qa, predicate, other, queries, admission = prepared_fixture(
        __import__("pytest").MonkeyPatch(), tmp,
        "CUT1-RECEIPT-BOUNDARY", grant=lambda _roots: True,
    )
    manifest, pmap = _manifest(queries, predicate, admission)
    state = {"revoked": False, "calls": 0, "receipts_observed": []}
    original = BatchExecutionRunner.record_receipt

    def record(self, receipt):
        original(self, receipt)
        state["calls"] += 1
        state["receipts_observed"].append(receipt.state)
        if receipt.state == "COMPLETED" and not state["revoked"]:
            state["revoked"] = True
            # Revoke only after the actual first Batch receipt exists.
            admission._estate._authorize = lambda _roots: state["revoked"] and False

    result_error = None
    runner = None
    BatchExecutionRunner.record_receipt = record
    try:
        runner = execute_saved_batch(
            admission, manifest=manifest, predicate_ref_by_query=pmap,
        )
    except Exception as exc:
        result_error = f"{type(exc).__name__}: {exc}"
    finally:
        BatchExecutionRunner.record_receipt = original
    # Exact subclass check: object.__new__ bypasses constructors but not type.
    class EvilPrepared(PreparedSavedC11Admission):
        pass

    illegal = object.__new__(EvilPrepared)
    subclass_error = None
    try:
        execute_saved_batch(illegal, manifest=manifest, predicate_ref_by_query=pmap)
    except Exception as exc:
        subclass_error = f"{type(exc).__name__}: {exc}"
    out = {
        "schema": "ANVIL_CUT1_RECEIPT_BOUNDARY_WITNESS@1",
        "query_units": len(manifest.units),
        "actual_receipt_states_observed": state["receipts_observed"],
        "revoked_after_completed_receipt": state["revoked"],
        "execute_saved_batch_error": result_error,
        "runner_receipts": (
            None if runner is None else [r.state for r in runner.receipts]
        ),
        "subclass_refused": subclass_error,
        "fixture": "sourcefree prepared saved I03 fixture; no source bytes",
    }
    (proofroot / "receipt_boundary_witness.json").write_text(
        json.dumps(out, indent=2, sort_keys=True), encoding="utf-8",
    )
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
