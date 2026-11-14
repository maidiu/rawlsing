"""Fresh-process selected I03 probe for PYAT #1006."""
from __future__ import annotations

import json
import resource
import sys
import time
from pathlib import Path

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import (
    RuntimeObjectCatalog,
    materialize_public_object,
)
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission


def _rss() -> int:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value) if sys.platform == "darwin" else int(value) * 1024


def main(argv: list[str]) -> int:
    capsule = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    catalog_document = capsule["catalog"]
    catalog = RuntimeObjectCatalog(
        authorities=tuple(
            materialize_public_object(value)
            for value in catalog_document["authorities"]
        ),
        predicates=tuple(
            materialize_public_object(value)
            for value in catalog_document["predicates"]
        ),
        queries=tuple(
            materialize_public_object(value)
            for value in catalog_document["queries"]
        ),
        discovery_authorities=tuple(
            materialize_public_object(value)
            for value in catalog_document["discovery_authorities"]
        ),
    )
    start = time.monotonic()
    admission = SavedC11Admission.open(
        root=capsule["root"],
        exact_path=capsule["exact_path"],
        independently_held_manifest_sha256=capsule["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**capsule["i02"]),
        release_ref=exact_ref(capsule["release"]),
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )
    admission_seconds = time.monotonic() - start
    query = materialize_public_object(capsule["query"])
    predicate = materialize_public_object(capsule["predicate"])
    start = time.monotonic()
    result = admission.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    query_seconds = time.monotonic() - start
    print(json.dumps({
        "admission_seconds": admission_seconds,
        "query_seconds": query_seconds,
        "fact_refs": [fact.ref.as_dict() for fact in result.facts],
        "fact_states": [fact.typed_state for fact in result.facts],
        "rss_bytes": _rss(),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
