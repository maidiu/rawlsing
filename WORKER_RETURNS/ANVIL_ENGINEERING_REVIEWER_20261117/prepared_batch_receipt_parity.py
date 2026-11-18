"""Review-only full receipt/parity for prepared vs plain saved Batch."""
from __future__ import annotations

from pathlib import Path
import json
import tempfile

from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec
from rawlsing_next.pre553_issued_workload import material
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture


def _plain(prepared):
    root = Path(prepared.estate_path).parents[1]
    return SavedC11Admission.open(
        root=root, exact_path=prepared.estate_path,
        independently_held_manifest_sha256=prepared.manifest_sha256,
        independently_held_i02=prepared.i02,
        release_ref=prepared.release_ref,
        runtime_catalog=prepared._runtime_catalog,
        current_authorizer=lambda _roots: True,
    )


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: prepared_batch_receipt_parity.py <proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("private proofroot required")
    tmp = Path(tempfile.mkdtemp(prefix="anvil-cut1-parity-", dir=proofroot))
    source, qa, predicate, _other, queries, prepared = _fixture(
        __import__("pytest").MonkeyPatch(), tmp, "CUT1-PARITY",
    )
    units = tuple(
        BatchUnitSpec("QUERY", q.ref, (prepared.release_ref,))
        for q in queries.values()
    )
    manifest = BatchManifest(units)
    pmap = {q.ref.key: predicate.ref for q in queries.values()}
    prepared_runner = execute_saved_batch(
        prepared, manifest=manifest, predicate_ref_by_query=pmap,
    )
    plain = _plain(prepared)
    plain_runner = execute_saved_batch(
        plain, manifest=manifest, predicate_ref_by_query=pmap,
    )
    preceipts = tuple(material(r) for r in prepared_runner.receipts)
    lreceipts = tuple(material(r) for r in plain_runner.receipts)
    out = {
        "schema": "ANVIL_CUT1_PREPARED_BATCH_RECEIPT_PARITY@1",
        "receipts_equal": preceipts == lreceipts,
        "prepared_receipts": preceipts,
        "plain_receipts": lreceipts,
        "prepared_states": [r.state for r in prepared_runner.receipts],
        "plain_states": [r.state for r in plain_runner.receipts],
        "prepared_summary": material(prepared_runner.summary()),
        "plain_summary": material(plain_runner.summary()),
        "result_refs_equal": tuple(
            r.result_refs for r in prepared_runner.receipts
        ) == tuple(r.result_refs for r in plain_runner.receipts),
    }
    (proofroot / "prepared_batch_receipt_parity.json").write_text(
        json.dumps(out, indent=2, sort_keys=True, default=str), encoding="utf-8",
    )
    print(json.dumps({
        "receipts_equal": out["receipts_equal"],
        "result_refs_equal": out["result_refs_equal"],
        "prepared_states": out["prepared_states"],
        "plain_states": out["plain_states"],
        "prepared_summary": out["prepared_summary"],
        "plain_summary": out["plain_summary"],
    }, indent=2, sort_keys=True))
    return 0 if out["receipts_equal"] and out["result_refs_equal"] else 2


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv))
