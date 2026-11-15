"""Fresh-interpreter saved-estate consumer for the #997 cold proof.

The producer process has exited before this process starts. This file opens only
the persisted saved estate and existing TEST_ONLY catalog; it does not read the
original SAV/DTA source or build a full C11 graph.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_batch_runner import (
    BatchManifest, BatchUnitSpec,
)
from rawlsing_next.pre553_carrier_execution import (
    RuntimeObjectCatalog, materialize_public_object,
)
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_batch, execute_saved_i03, execute_saved_i05,
)


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
    capsule = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    catalog = RuntimeObjectCatalog.from_documents(
        authority_documents=capsule["authorities"],
        predicate_documents=capsule["predicates"],
        query_documents=capsule["queries"],
        discovery_authority_documents=capsule["discovery_authorities"],
    )
    query_ref = exact_ref(capsule["query_ref"])
    predicate_ref = exact_ref(capsule["predicate_ref"])
    query = catalog.resolve_query_exact(query_ref)
    predicate = catalog.resolve_predicate_exact(predicate_ref)
    admission = SavedC11Admission.open(
        root=capsule["root"], exact_path=capsule["exact_path"],
        independently_held_manifest_sha256=capsule["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**capsule["i02"]),
        release_ref=exact_ref(capsule["release"]),
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )
    binding = admission.binding_receipt()
    if binding.source_opens != 0:
        raise SystemExit("consumer opened the source")
    i03 = execute_saved_i03(
        admission, query_ref=query.ref, predicate_ref=predicate.ref)
    discovery = catalog.resolve_discovery_authority_exact(
        exact_ref(capsule["discovery_ref"]))
    i05 = execute_saved_i05(
        admission, discovery_authority_ref=discovery.ref)
    units = tuple(
        BatchUnitSpec(
            item["job_kind"], exact_ref(item["job_ref"]),
            tuple(exact_ref(r) for r in item["release_refs"]),
            tuple(exact_ref(r) for r in item["semantic_input_refs"]),
        )
        for item in capsule["batch_units"]
    )
    batch = execute_saved_batch(
        admission, manifest=BatchManifest(units),
        predicate_ref_by_query={query.ref.key: predicate.ref},
    )
    out = {
        "consumer": "PASS",
        "source_opens": binding.source_opens,
        "full_c11_repository_builds": binding.full_c11_repository_builds,
        "i03": _payload(i03),
        "i05": _payload(i05),
        "batch": {
            "states": [getattr(r, "state", None) for r in batch.receipts],
            "count": len(batch.receipts),
        },
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
