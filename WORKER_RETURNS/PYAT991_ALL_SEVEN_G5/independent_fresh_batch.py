"""Independent fresh-child Batch witness on the saved estate (G5 review only)."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from rawlsing_next.pre553_issued_workload import execute_issued_workload, material
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import HOST, PURPOSE
from rawlsing_next.tests.test_pyat991_s2d_five_readers import _admission_for, _fixture


CHILD = r"""
import json
import sys
from pathlib import Path
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_issued_workload import material
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
c=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
catalog=RuntimeObjectCatalog.from_documents(
    authority_documents=c["catalog"]["authorities"],
    predicate_documents=c["catalog"]["predicates"],
    query_documents=c["catalog"]["queries"],
    discovery_authority_documents=c["catalog"]["discovery_authorities"],
)
units=tuple(
    BatchUnitSpec(
        u["job_kind"], exact_ref(u["job_ref"]),
        tuple(exact_ref(x) for x in u["release_refs"]),
        tuple(exact_ref(x) for x in u.get("semantic_input_refs", ())),
    )
    for u in c["manifest"]["units"]
)
manifest=BatchManifest(units)
admission=SavedC11Admission.open(
    root=c["root"], exact_path=c["exact_path"],
    independently_held_manifest_sha256=c["manifest_sha256"],
    independently_held_i02=ExternalI02Roots(**c["i02"]),
    release_ref=exact_ref(c["release"]), runtime_catalog=catalog,
    current_authorizer=lambda _roots: True,
)
runner=execute_saved_batch(
    admission, manifest=manifest,
    predicate_ref_by_query={
        key: exact_ref(value) for key, value in c["predicate_ref_by_query"].items()
    },
)
print(json.dumps({
    "receipts": [material(r) for r in runner.receipts],
    "summary": material(runner.summary()),
}, sort_keys=True))
"""


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: independent_fresh_batch.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("proofroot must be the approved private temp path")
    tmp = proofroot / "fresh-batch"
    tmp.mkdir(parents=True, exist_ok=True)
    path, oracle_bundle, saved_bundle, issued, root, receipt, issuer = _fixture(tmp)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    oracle = execute_issued_workload(
        issued.workload, issuer,
        source_factory=lambda _ref: oracle_bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    capsule = {
        "root": str(admission.estate_path).rsplit("/releases/", 1)[0],
        "exact_path": admission.estate_path,
        "manifest_sha256": admission.manifest_sha256,
        "i02": admission.i02.__dict__,
        "release": admission.release_ref.as_dict(),
        "catalog": material(issued.workload)["catalog"],
        "manifest": material(oracle.manifest),
        "predicate_ref_by_query": {
            request.query_ref.key: request.predicate_ref.as_dict()
            for request in issued.workload.requests
        },
    }
    capsule_path = tmp / "fresh-batch-capsule.json"
    capsule_path.write_text(json.dumps(capsule, sort_keys=True), encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, "-c", CHILD, str(capsule_path)],
        cwd=str(Path(__file__).resolve().parents[2]),
        capture_output=True, text=True, timeout=180,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr)
    observed = json.loads(completed.stdout)
    observed_refs = tuple(sorted(
        ref["object_id"] for receipt in observed["receipts"] for ref in receipt["result_refs"]
    ))
    expected_refs = tuple(sorted(ref.object_id for ref in oracle.output_refs))
    out = {
        "schema": "PYAT991_ALL_SEVEN_G5_FRESH_BATCH@1",
        "child_returncode": completed.returncode,
        "observed_receipt_count": len(observed["receipts"]),
        "observed_receipt_states": sorted({r["state"] for r in observed["receipts"]}),
        "result_refs_equal_to_normal_oracle": observed_refs == expected_refs,
        "observed_manifest_hash": observed["receipts"][0]["manifest_hash"] if observed["receipts"] else None,
        "oracle_manifest_hash": oracle.manifest.manifest_hash,
        "observed_summary": observed["summary"],
        "child_stderr": completed.stderr,
    }
    (proofroot / "fresh_batch.json").write_text(
        json.dumps(out, indent=2, sort_keys=True), encoding="utf-8",
    )
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["result_refs_equal_to_normal_oracle"] else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
