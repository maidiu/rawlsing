"""Bounded baseline probe: prepared admission is rejected by the normal wrappers.

Run from the IMPLEMENTER checkout with PYTHONPATH=. This is return-local only.
"""
from __future__ import annotations

import json
from pathlib import Path
import tempfile

import pytest

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchIntegrityError, BatchManifest, BatchUnitSpec,
)
from rawlsing_next.pre553_saved_c11_admission import SavedC11AdmissionError
from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture


def main() -> int:
    root = Path(tempfile.mkdtemp(
        prefix="anvil-cut1-abi-",
        dir="/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T",
    ))
    monkeypatch = pytest.MonkeyPatch()
    try:
        source, qa, predicate, other, queries, admission = _fixture(
            monkeypatch, root / "fixture", "ANVIL-CUT1-ABI")
        result = {
            "fixture_root": str(root),
            "admission_type": type(admission).__name__,
            "admission_manifest_sha256": admission.manifest_sha256,
            "source_sha256": source.get("source_sha") if isinstance(source, dict) else None,
            "queries": {name: query.ref.as_dict() for name, query in queries.items()},
            "predicate": predicate.ref.as_dict(),
            "direct_i03_error": None,
            "batch_error": None,
        }
        try:
            execute_saved_i03(
                admission,
                query_ref=queries["selected"].ref,
                predicate_ref=predicate.ref,
            )
        except SavedC11AdmissionError as exc:
            result["direct_i03_error"] = {
                "type": type(exc).__name__, "message": str(exc),
            }
        else:
            result["direct_i03_error"] = "UNEXPECTED_ACCEPT"

        unit = BatchUnitSpec(
            job_kind="QUERY",
            job_ref=queries["selected"].ref,
            release_refs=(admission.release_ref,),
        )
        try:
            BatchExecutionRunner(
                manifest=BatchManifest(units=(unit,)),
                repository=admission,
                saved_mode=True,
            )
        except BatchIntegrityError as exc:
            result["batch_error"] = {
                "type": type(exc).__name__, "message": str(exc),
            }
        else:
            result["batch_error"] = "UNEXPECTED_ACCEPT"
        result["desired_feature"] = "PreparedSavedC11Admission accepted by saved wrappers/Batch"
        result["baseline_disposition"] = (
            "BASELINE_READY_PENDING_CURRENT_OWNER_ACK"
            if result["direct_i03_error"] != "UNEXPECTED_ACCEPT"
            and result["batch_error"] != "UNEXPECTED_ACCEPT"
            else "UNEXPECTED_ACCEPT"
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    finally:
        monkeypatch.undo()


if __name__ == "__main__":
    raise SystemExit(main())
