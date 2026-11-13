"""Producer half of the #997 Q2 saved-estate fresh-process proof.

Run as a separate interpreter. It reads one generated TEST_ONLY SAV, writes the
real Q2/S2-C persisted estate, executes the actual consumers once as an oracle,
and exits after writing a capsule. It does not run the fresh consumer.
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import asdict, replace
from pathlib import Path
import sys

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec,
)
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission, SavedReleaseIdentity,
)
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_batch, execute_saved_i03, execute_saved_i05,
)
from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
from rawlsing_next.tests.test_pyat960_s1e_native_fact import (
    _NATIVE_HOST, _NATIVE_PURPOSE, _compile_native, _native_fixture,
)
from rawlsing_next.tests.test_pyat960_s1e_support import build
from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import _freeze_packet
from rawlsing_next.tests.test_universal_grammar import _frontier


def _fixed(fixture):
    inventory = replace(
        fixture["inventory"], inventory_id="PYAT997-FRESH-EXACT")
    frontier = _frontier(inventory, fixture["policy"])
    fixture = dict(fixture)
    fixture.update(
        inventory=inventory, frontier=frontier,
        census=_freeze_packet(frontier),
    )
    return fixture


def _payload(result):
    return {
        "facts": [f.ref.as_dict() for f in getattr(result, "facts", ())],
        "receipts": [r.ref.as_dict() for r in getattr(result, "receipts", ())],
        "typed_states": [
            getattr(x, "typed_state", None)
            for x in (*getattr(result, "facts", ()), *getattr(result, "receipts", ()))
        ],
        "candidate_count": getattr(result, "candidate_count", None),
        "covered_candidate_count": getattr(result, "covered_candidate_count", None),
    }


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    capsule_path = Path(sys.argv[2]).resolve()
    root.mkdir(parents=True, exist_ok=True)
    fixture = _fixed(_native_fixture(
        root / "fixture", values=(0., 1., 0., 1., 0.)))
    private = root / "private"
    private.mkdir(mode=0o700, exist_ok=True)
    sink = SourceSavedBodySink(
        certificate_path=root / "estate.sqlite",
        authorized_private_root=private, chunk_rows=2,
    )
    handoff = build(
        root, fixture, name="estate.sqlite", body_sink=sink, chunk_size=2)
    estate = sink.receipt
    release = SavedReleaseIdentity(estate.reconstructed_v1_release_ref)
    compilation = _compile_native(
        fixture, handoff, fixture["projection"], release)
    catalog = compilation.issued.workload.catalog
    q101_query = None
    q101_predicate = None
    for record in compilation.plan.records:
        if record.status != "SUPPORTED":
            continue
        for raw in record.query_refs:
            if isinstance(raw, Mapping):
                raw = {k: raw[k] for k in ("kind", "object_id", "content_hash")}
            qref = exact_ref(raw, "query")
            query = catalog.resolve_query_exact(qref)
            targets = tuple(exact_ref(t) for t in query.target_refs)
            if any(t.kind == "QUESTION_NATIVE" and t.object_id.endswith(":q101")
                   for t in targets):
                q101_query = query
                q101_predicate = catalog.resolve_predicate_exact(
                    query.condition_predicate_ref)
    if q101_query is None or q101_predicate is None:
        raise SystemExit("no compiled q101 query")
    admission = SavedC11Admission.open(
        root=private, exact_path=estate.path,
        independently_held_manifest_sha256=estate.manifest_sha256,
        independently_held_i02=estate.i02,
        release_ref=estate.reconstructed_v1_release_ref,
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )
    discovery = catalog.discovery_authorities[0]
    decision = compilation.issued.workload.decision_ref
    units = (
        BatchUnitSpec(
            "DISCOVERY", discovery.ref, (estate.reconstructed_v1_release_ref,),
            (decision,),
        ),
    )
    # The compiled workload issues no query unit; execute the actual saved
    # discovery Batch and the q101 I03 directly, preserving the shape. Do not
    # mint a query Batch unit that the issuer did not issue.
    batch = execute_saved_batch(
        admission, manifest=BatchManifest(units),
        predicate_ref_by_query={},
    )
    i03 = execute_saved_i03(
        admission, query_ref=q101_query.ref, predicate_ref=q101_predicate.ref)
    i05 = execute_saved_i05(
        admission, discovery_authority_ref=discovery.ref)
    expected = {
        "i03": _payload(i03),
        "i05": _payload(i05),
        "batch": {
            "states": [getattr(r, "state", None) for r in batch.receipts],
            "count": len(batch.receipts),
        },
    }
    capsule = {
        "root": str(private),
        "exact_path": estate.path,
        "manifest_sha256": estate.manifest_sha256,
        "i02": asdict(estate.i02),
        "release": estate.reconstructed_v1_release_ref.as_dict(),
        "authorities": [x.as_dict() for x in catalog.authorities],
        "predicates": [x.as_dict() for x in catalog.predicates],
        "queries": [x.as_dict() for x in catalog.queries],
        "discovery_authorities": [
            x.as_dict() for x in catalog.discovery_authorities],
        "query_ref": q101_query.ref.as_dict(),
        "predicate_ref": q101_predicate.ref.as_dict(),
        "discovery_ref": discovery.ref.as_dict(),
        "decision_ref": decision.as_dict(),
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
        "source_sha256": handoff.source_sha256,
        "source_reads": handoff.stats.source_reads,
        "decode_calls": handoff.stats.decode_calls,
        "cell_passes": handoff.stats.cell_passes,
        "family_counts": dict(estate.family_counts),
    }
    capsule_path.write_text(json.dumps(capsule, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "producer": "PASS",
        "source_sha256": handoff.source_sha256,
        "source_reads": handoff.stats.source_reads,
        "decode_calls": handoff.stats.decode_calls,
        "cell_passes": handoff.stats.cell_passes,
        "family_counts": dict(estate.family_counts),
        "expected": expected,
        "capsule": str(capsule_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
