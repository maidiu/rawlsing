"""Reopen one existing #1006 estate and measure selected native queries."""
from __future__ import annotations

import argparse
import json
import resource
import sys
import time
from pathlib import Path
from typing import Any

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import (
    RuntimeObjectCatalog,
    materialize_public_object,
)
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission

from instrument_1006 import stats


def _rss() -> int:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value) if sys.platform == "darwin" else int(value) * 1024


def _jsonable(value: Any) -> Any:
    if value is None:
        return None
    return json.loads(canonical_json(value))


def _load(capsule: dict[str, Any]) -> tuple[SavedC11Admission, RuntimeObjectCatalog, dict[str, Any]]:
    document = capsule["catalog"]
    catalog = RuntimeObjectCatalog(
        authorities=tuple(
            materialize_public_object(value) for value in document["authorities"]
        ),
        predicates=tuple(
            materialize_public_object(value) for value in document["predicates"]
        ),
        queries=tuple(
            materialize_public_object(value) for value in document["queries"]
        ),
        discovery_authorities=tuple(
            materialize_public_object(value)
            for value in document["discovery_authorities"]
        ),
    )
    admission = SavedC11Admission.open(
        root=capsule["root"],
        exact_path=capsule["exact_path"],
        independently_held_manifest_sha256=capsule["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**capsule["i02"]),
        release_ref=exact_ref(capsule["release"]),
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )
    return admission, catalog, capsule


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capsule", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--queries", default="selected,f2_reverse,f4_three")
    parser.add_argument("--repeat", type=int, default=1)
    args = parser.parse_args(argv)
    capsule = json.loads(Path(args.capsule).read_text(encoding="utf-8"))
    result: dict[str, Any] = {
        "schema": "PYAT1006_QUERY_PROBE@1",
        "status": "PARTIAL_RUNNING",
        "capsule": args.capsule,
        "queries": {},
    }
    out = Path(args.out)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    admission, catalog, _ = _load(capsule)
    for name in [value for value in args.queries.split(",") if value]:
        refs = capsule["query_refs"][name]
        query = next(
            item for item in catalog.queries
            if item.ref == exact_ref(refs["query"])
        )
        predicate = next(
            item for item in catalog.predicates
            if item.ref == exact_ref(refs["predicate"])
        )
        start = time.monotonic()
        observed = admission.execute_i03(
            query_ref=query.ref, predicate_ref=predicate.ref,
        )
        elapsed = time.monotonic() - start
        result["queries"][name] = {
            "seconds": elapsed,
            "query_ref": _jsonable(query.ref),
            "predicate_ref": _jsonable(predicate.ref),
            "facts": [
                {
                    "ref": _jsonable(fact.ref),
                    "typed_state": fact.typed_state,
                    "raw_denominator_support": getattr(
                        fact, "raw_denominator_support", None
                    ),
                }
                for fact in observed.facts
            ],
        }
        result["rss_bytes"] = _rss()
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.repeat:
        values = []
        refs = capsule["query_refs"]["selected"]
        query = next(
            item for item in catalog.queries
            if item.ref == exact_ref(refs["query"])
        )
        predicate = next(
            item for item in catalog.predicates
            if item.ref == exact_ref(refs["predicate"])
        )
        for _ in range(args.repeat):
            start = time.monotonic()
            admission.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
            values.append(time.monotonic() - start)
        result["selected_repeat"] = {"seconds": values, "stats": stats(values)}
    result["status"] = "MEASURED"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "queries": {
            name: value["seconds"] for name, value in result["queries"].items()
        },
        "selected_repeat": result.get("selected_repeat", {}).get("stats"),
        "rss_bytes": _rss(),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
