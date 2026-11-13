"""Producer half of R3: 3-question Q2 estate, issued query+discovery Batch oracle, exit."""
from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import sys

from harness import _make_fixture, _materialize, _payload
from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_batch, execute_saved_i03, execute_saved_i05,
)


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    capsule_path = Path(sys.argv[2]).resolve()
    root.mkdir(parents=True, exist_ok=True)
    fixture = _make_fixture(
        root / "fixture",
        [(0, 0, 0, 1), (1, 1, 1, 1), (0, 1, 0, 2),
         (1, 0, 1, 3), (0, 0, 1, 4)],
    )
    bundle = _materialize(root / "stage", fixture)
    estate = bundle["estate"]
    admission = bundle["admission"]
    query = bundle["joint_query"]
    predicate = bundle["predicate"]
    discovery = bundle["discovery"]
    issued = bundle["issued"]
    query_unit = BatchUnitSpec(
        "QUERY", query.ref, (admission.release_ref,),
        (issued.record.decision_ref,))
    discovery_unit = BatchUnitSpec(
        "DISCOVERY", discovery.ref, (admission.release_ref,),
        (issued.record.decision_ref,))
    units = (query_unit, discovery_unit)
    batch = execute_saved_batch(
        admission, manifest=BatchManifest(units),
        predicate_ref_by_query={query.ref.key: predicate.ref},
    )
    i03 = execute_saved_i03(
        admission, query_ref=query.ref, predicate_ref=predicate.ref)
    i05 = execute_saved_i05(
        admission, discovery_authority_ref=discovery.ref)
    expected = {
        "i03": _payload(i03),
        "i05": _payload(i05),
        "batch": {
            "states": [r.state for r in batch.receipts],
            "count": len(batch.receipts),
        },
    }
    capsule = {
        "root": str(bundle["private"]),
        "exact_path": estate.path,
        "manifest_sha256": estate.manifest_sha256,
        "i02": asdict(estate.i02),
        "release": estate.reconstructed_v1_release_ref.as_dict(),
        "authorities": [x.as_dict() for x in bundle["compilation"].runtime_catalog.authorities],
        "predicates": [x.as_dict() for x in bundle["compilation"].runtime_catalog.predicates],
        "queries": [x.as_dict() for x in bundle["compilation"].runtime_catalog.queries],
        "discovery_authorities": [
            x.as_dict() for x in bundle["compilation"].runtime_catalog.discovery_authorities],
        "query_ref": query.ref.as_dict(),
        "predicate_ref": predicate.ref.as_dict(),
        "discovery_ref": discovery.ref.as_dict(),
        "decision_ref": issued.record.decision_ref.as_dict(),
        "batch_units": [
            {
                "job_kind": unit.job_kind,
                "job_ref": unit.job_ref.as_dict(),
                "release_refs": [r.as_dict() for r in unit.release_refs],
                "semantic_input_refs": [
                    r.as_dict() for r in unit.semantic_input_refs],
            }
            for unit in units
        ],
        "expected": expected,
        "source_path": str(fixture["path"]),
        "source_sha256": bundle["handoff"].source_sha256,
        "source_reads": bundle["handoff"].stats.source_reads,
        "decode_calls": bundle["handoff"].stats.decode_calls,
        "cell_passes": bundle["handoff"].stats.cell_passes,
        "family_counts": dict(estate.family_counts),
    }
    capsule_path.write_text(json.dumps(capsule, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "producer": "PASS",
        "source_sha256": capsule["source_sha256"],
        "source_reads": capsule["source_reads"],
        "decode_calls": capsule["decode_calls"],
        "cell_passes": capsule["cell_passes"],
        "family_counts": capsule["family_counts"],
        "expected": expected,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
