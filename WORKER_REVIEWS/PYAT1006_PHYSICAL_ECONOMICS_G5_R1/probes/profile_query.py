"""ROWGROUPREAD and first-reader profile for one #1006 saved estate.

Review-only instrumentation wraps accepted production calls; the accepted
implementation is always invoked unchanged.  Writes only under the review
path's per-shape outdir.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time
from typing import Any

import pyarrow.parquet as pq

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import (
    RuntimeObjectCatalog, materialize_public_object,
)
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
import rawlsing_next.pre553_direct_estate_i03 as direct_module

from review_common import host_info, write_json


def _rss_peak() -> int:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value) if sys.platform == "darwin" else int(value) * 1024


class ReadCounter:
    def __init__(self) -> None:
        self.phase = "other"
        self.records: list[dict[str, Any]] = []

    def reset(self, phase: str = "other") -> None:
        self.phase = phase
        self.records = []

    def add(self, family: str, gid: int, rows: int, seconds: float, columns: Any) -> None:
        self.records.append({
            "phase": self.phase,
            "family": family,
            "gid": gid,
            "rows": rows,
            "seconds": seconds,
            "columns": columns,
        })

    def material(self) -> dict[str, Any]:
        by_phase: dict[str, dict[str, Any]] = {}
        for record in self.records:
            phase = record["phase"]
            entry = by_phase.setdefault(phase, {
                "reads": 0,
                "rows_decoded": 0,
                "seconds": 0.0,
                "families": {},
            })
            entry["reads"] += 1
            entry["rows_decoded"] += record["rows"]
            entry["seconds"] += record["seconds"]
            family = entry["families"].setdefault(record["family"], {
                "reads": 0,
                "rows_decoded": 0,
                "seconds": 0.0,
                "gids": [],
            })
            family["reads"] += 1
            family["rows_decoded"] += record["rows"]
            family["seconds"] += record["seconds"]
            family["gids"].append(record["gid"])
        for entry in by_phase.values():
            for family, values in entry["families"].items():
                gids = values.pop("gids")
                transitions = sum(
                    1 for left, right in zip(gids, gids[1:]) if left != right
                )
                values["unique_gids"] = len(set(gids))
                values["gid_transitions"] = transitions
                values["consecutive_same_gid"] = len(gids) - 1 - transitions
                values["cache_hit_ratio_if_single_cache"] = (
                    (len(gids) - 1 - transitions) / (len(gids) - 1)
                    if len(gids) > 1 else 0.0
                )
                values["first_gids"] = gids[:20]
                values["gid_sequence_sha256"] = hashlib.sha256(
                    ",".join(str(gid) for gid in gids).encode()
                ).hexdigest()
        return {"by_phase": by_phase, "total_reads": len(self.records)}


COUNTER = ReadCounter()
REAL_PARQUET_FILE = pq.ParquetFile
ORIGINAL_BUILD = DirectEstateI03Session._build
ORIGINAL_OBJECT = direct_module._object_from_row
ORIGINAL_FAMILY = DirectEstateI03Session._respondent_family
BUILD_SECONDS: list[float] = []
OBJECT_COUNTS: Counter = Counter()
COUNT_FAMILY: Counter = Counter()


class TrackedParquetFile:
    def __init__(self, path: Any, *args: Any, **kwargs: Any) -> None:
        self._review_real = REAL_PARQUET_FILE(path, *args, **kwargs)
        self._review_name = Path(path).name
        self._review_path = str(path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._review_real, name)

    def read_row_group(self, i: Any, columns: Any = None, *args: Any, **kwargs: Any) -> Any:
        start = time.monotonic()
        table = self._review_real.read_row_group(i, columns=columns, *args, **kwargs)
        elapsed = time.monotonic() - start
        COUNTER.add(self._review_name, int(i), int(table.num_rows), elapsed, columns)
        return table

    def close(self) -> None:
        self._review_real.close()


def tracked_parquet_file(path: Any, *args: Any, **kwargs: Any) -> TrackedParquetFile:
    return TrackedParquetFile(path, *args, **kwargs)


def patched_build(self: Any) -> None:
    COUNTER.phase = "session_build"
    start = time.monotonic()
    try:
        return ORIGINAL_BUILD(self)
    finally:
        BUILD_SECONDS.append(time.monotonic() - start)
        COUNTER.phase = "query_eval"


def patched_object(value: Any) -> Any:
    OBJECT_COUNTS[COUNTER.phase] += 1
    return ORIGINAL_OBJECT(value)


def patched_family(self: Any, family: str, respondent_key: str) -> Any:
    COUNT_FAMILY[family] += 1
    yield from ORIGINAL_FAMILY(self, family, respondent_key)


def _jsonable(value: Any) -> Any:
    if value is None:
        return None
    return json.loads(canonical_json(value))


def load_capsule(path: Path) -> tuple[SavedC11Admission, RuntimeObjectCatalog, dict[str, Any]]:
    capsule = json.loads(path.read_text())
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
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--queries", default="selected")
    parser.add_argument("--ab-routing", action="store_true")
    args = parser.parse_args(argv)
    outdir = Path(args.outdir).absolute()
    outdir.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {
        "schema": "PYAT1006_G5_ROWGROUP_PROFILE@1",
        "host": host_info(),
        "capsule": args.capsule,
        "status": "RUNNING",
    }
    path = outdir / "query_profile.json"
    write_json(path, result)

    pq.ParquetFile = tracked_parquet_file
    DirectEstateI03Session._build = patched_build
    direct_module._object_from_row = patched_object
    DirectEstateI03Session._respondent_family = patched_family
    try:
        COUNTER.reset()
        admission_start = time.monotonic()
        admission, catalog, capsule = load_capsule(Path(args.capsule))
        result["admission_seconds"] = time.monotonic() - admission_start
        result["admission_counter"] = COUNTER.material()
        result["release_ref"] = admission.release_ref.as_dict()
        result["family_counts"] = dict(capsule["family_counts"])
        result["queries"] = {}
        for name in [value for value in args.queries.split(",") if value]:
            refs = capsule["query_refs"][name]
            query = next(
                item for item in catalog.queries if item.ref == exact_ref(refs["query"])
            )
            predicate = next(
                item for item in catalog.predicates
                if item.ref == exact_ref(refs["predicate"])
            )
            COUNTER.reset()
            BUILD_SECONDS.clear()
            OBJECT_COUNTS.clear()
            COUNT_FAMILY.clear()
            start = time.monotonic()
            observed = admission.execute_i03(
                query_ref=query.ref, predicate_ref=predicate.ref,
            )
            wall = time.monotonic() - start
            build_seconds = sum(BUILD_SECONDS)
            result["queries"][name] = {
                "wall_seconds": wall,
                "session_build_seconds": build_seconds,
                "query_eval_seconds": wall - build_seconds,
                "build_calls": len(BUILD_SECONDS),
                "object_materializations": dict(OBJECT_COUNTS),
                "respondent_family_calls": dict(COUNT_FAMILY),
                "reads": COUNTER.material(),
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
            result["rss_peak_bytes"] = _rss_peak()
            write_json(path, result)
        if args.ab_routing:
            ab: dict[str, Any] = {}
            with DirectEstateI03Session(admission._estate) as session:
                keys = list(session.respondents.keys())
                orders = {
                    "hash_ref_order": sorted(keys),
                    "physical_insertion_order": keys,
                }
                for order_name, order in orders.items():
                    session._row_group_cache.clear()
                    COUNTER.reset("ab_" + order_name)
                    OBJECT_COUNTS.clear()
                    start = time.monotonic()
                    rows = 0
                    for key in order:
                        rows += len(tuple(
                            session._respondent_family("RoutingEligibilityFact", key)
                        ))
                    elapsed = time.monotonic() - start
                    ab[order_name] = {
                        "seconds": elapsed,
                        "rows": rows,
                        "objects": dict(OBJECT_COUNTS),
                        "reads": COUNTER.material(),
                    }
            result["routing_order_ab"] = ab
        result["status"] = "MEASURED"
        result["rss_peak_bytes"] = _rss_peak()
        write_json(path, result)
        print(json.dumps({
            "status": result["status"],
            "queries": {
                name: {
                    "wall": item["wall_seconds"],
                    "build": item["session_build_seconds"],
                    "eval": item["query_eval_seconds"],
                    "reads": item["reads"]["total_reads"],
                    "query_families": {
                        fam: {
                            "reads": value["reads"],
                            "unique_gids": value["unique_gids"],
                            "cache_hit_ratio": value["cache_hit_ratio_if_single_cache"],
                            "rows_decoded": value["rows_decoded"],
                        }
                        for fam, value in item["reads"]["by_phase"].get(
                            "query_eval", {}
                        ).get("families", {}).items()
                    },
                }
                for name, item in result["queries"].items()
            },
            "ab": {
                key: {
                    "seconds": value["seconds"],
                    "reads": value["reads"]["total_reads"],
                    "gids": {
                        fam: val["unique_gids"]
                        for phase in value["reads"]["by_phase"].values()
                        for fam, val in phase.get("families", {}).items()
                    },
                }
                for key, value in result.get("routing_order_ab", {}).items()
            },
        }, indent=2, sort_keys=True))
        return 0
    finally:
        pq.ParquetFile = REAL_PARQUET_FILE
        DirectEstateI03Session._build = ORIGINAL_BUILD
        direct_module._object_from_row = ORIGINAL_OBJECT
        DirectEstateI03Session._respondent_family = ORIGINAL_FAMILY


if __name__ == "__main__":
    raise SystemExit(main())
