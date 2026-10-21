"""Exact Batch manifest/receipt serialization and cold-resume reconstruction."""
from __future__ import annotations

import json
from pathlib import Path

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec, UnitExecutionReceipt,
)
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
from ur_b.s1_batch import run as run_batch


def dump(fx, path):
    out = run_batch(fx)
    document = {
        "schema": "UR_B_BATCH_RESUME@1",
        "manifest_units": [
            {"job_kind": u.job_kind, "job_ref": u.job_ref.as_dict(),
             "release_refs": [r.as_dict() for r in u.release_refs],
             "semantic_input_refs": [r.as_dict() for r in u.semantic_input_refs]}
            for u in out["manifest"].units
        ],
        "receipts": [r.projection() for r in out["receipts"]],
        "release_ref": out["release"].release_ref.as_dict(),
    }
    Path(path).write_text(json.dumps(document, indent=2, sort_keys=True) + "\n",
                          encoding="utf-8")
    return document


def resume(fx, path):
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    units = tuple(
        BatchUnitSpec(
            row["job_kind"], ExactRef(**row["job_ref"]),
            tuple(ExactRef(**ref) for ref in row["release_refs"]),
            tuple(ExactRef(**ref) for ref in row["semantic_input_refs"]))
        for row in document["manifest_units"])
    manifest = BatchManifest(units)
    receipts = []
    for row in document["receipts"]:
        receipts.append(UnitExecutionReceipt(
            manifest_hash=row["manifest_hash"],
            unit_ref=ExactRef(**row["unit_ref"]),
            attempt_index=row["attempt_index"],
            state=row["state"],
            execution_performed=row["execution_performed"],
            executor_ref=(None if row["executor_ref"] is None else ExactRef(**row["executor_ref"])),
            result_refs=tuple(ExactRef(**ref) for ref in row["result_refs"]),
            provenance_refs=tuple(ExactRef(**ref) for ref in row["provenance_refs"]),
            failure_code=row["failure_code"],
            detail_hash=row["detail_hash"],
        ))
    repo, release = build_source_backed_c11_repository(fx["incidence"], fx["projection"])
    runner = BatchExecutionRunner(manifest=manifest, repository=repo,
                                  prior_receipts=receipts)
    return {"manifest": manifest, "runner": runner, "receipts": tuple(receipts),
            "pending": runner.pending_units(), "release": release,
            "manifest_hash": manifest.manifest_hash}
