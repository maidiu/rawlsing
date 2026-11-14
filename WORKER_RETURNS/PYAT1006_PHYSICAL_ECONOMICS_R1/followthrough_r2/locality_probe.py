"""TEST_ONLY runtime locality experiment on one accepted #1006 estate.

EXPERIMENT_NOT_IMPLEMENTED: the accepted production tree is unchanged.  This
probe monkeypatches only the module-global ``sorted`` lookup in
``_pre553_query_eval`` so respondent traversal follows the session's physical
insertion order instead of ref-key order.  Every other sort, integrity check,
native predicate/risk/fact/replay owner and accepted reader remains unchanged.
"""
from __future__ import annotations

import argparse
import builtins
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
from rawlsing_next.pre553_c11_integrity import RespondentIdentity
from rawlsing_next.pre553_carrier_execution import (
    RuntimeObjectCatalog,
    materialize_public_object,
)
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
import rawlsing_next._pre553_query_eval as query_eval
import rawlsing_next.pre553_direct_estate_i03 as direct_module

REAL_SORTED = builtins.sorted
REAL_PARQUET_FILE = pq.ParquetFile
REAL_BUILD = DirectEstateI03Session._build
REAL_ENTER = DirectEstateI03Session.__enter__
REAL_EXIT = DirectEstateI03Session.__exit__


def _rss_peak() -> int:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value) if sys.platform == "darwin" else int(value) * 1024


def _jsonable(value: Any) -> Any:
    if value is None:
        return None
    return json.loads(canonical_json(value))


def _directory_bytes(path: Path) -> int:
    try:
        return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())
    except FileNotFoundError:
        return 0


class Counter:
    def __init__(self) -> None:
        self.phase = "admission"
        self.records: list[dict[str, Any]] = []

    def reset(self, phase: str = "admission") -> None:
        self.phase = phase
        self.records = []

    def add(self, family: str, gid: int, rows: int, seconds: float) -> None:
        self.records.append({
            "phase": self.phase,
            "family": family,
            "gid": gid,
            "rows": rows,
            "seconds": seconds,
        })

    def material(self) -> dict[str, Any]:
        by_phase: dict[str, Any] = {}
        for record in self.records:
            phase = by_phase.setdefault(record["phase"], {
                "reads": 0, "rows_decoded": 0, "seconds": 0.0, "families": {},
            })
            phase["reads"] += 1
            phase["rows_decoded"] += record["rows"]
            phase["seconds"] += record["seconds"]
            family = phase["families"].setdefault(record["family"], {
                "reads": 0, "rows_decoded": 0, "seconds": 0.0, "gids": [],
            })
            family["reads"] += 1
            family["rows_decoded"] += record["rows"]
            family["seconds"] += record["seconds"]
            family["gids"].append(record["gid"])
        for phase in by_phase.values():
            for family in phase["families"].values():
                gids = family.pop("gids")
                transitions = sum(
                    1 for left, right in zip(gids, gids[1:]) if left != right
                )
                family["unique_gids"] = len(set(gids))
                family["gid_transitions"] = transitions
                family["consecutive_same_gid"] = len(gids) - 1 - transitions
                family["cache_hit_ratio_if_single_cache"] = (
                    (len(gids) - 1 - transitions) / (len(gids) - 1)
                    if len(gids) > 1 else 0.0
                )
                family["first_gids"] = gids[:20]
                family["gid_sequence_sha256"] = hashlib.sha256(
                    ",".join(str(gid) for gid in gids).encode()
                ).hexdigest()
        return {"by_phase": by_phase, "total_reads": len(self.records)}


COUNTER = Counter()
TEMP_PEAK = {"value": 0}


class TrackedParquetFile:
    def __init__(self, path: Any, *args: Any, **kwargs: Any) -> None:
        self._real = REAL_PARQUET_FILE(path, *args, **kwargs)
        self._name = Path(path).name

    def __getattr__(self, name: str) -> Any:
        return getattr(self._real, name)

    def read_row_group(self, i: Any, columns: Any = None, *args: Any, **kwargs: Any) -> Any:
        start = time.monotonic()
        table = self._real.read_row_group(i, columns=columns, *args, **kwargs)
        COUNTER.add(self._name, int(i), int(table.num_rows), time.monotonic() - start)
        return table

    def close(self) -> None:
        self._real.close()


def _tracked_parquet_file(path: Any, *args: Any, **kwargs: Any) -> TrackedParquetFile:
    return TrackedParquetFile(path, *args, **kwargs)


def _patched_build(self: Any) -> None:
    previous = COUNTER.phase
    COUNTER.phase = "session_build"
    try:
        return REAL_BUILD(self)
    finally:
        COUNTER.phase = previous


def _patched_enter(self: Any) -> Any:
    result = REAL_ENTER(self)
    temporary = getattr(self, "_temporary", None)
    if temporary is not None:
        TEMP_PEAK["value"] = max(
            TEMP_PEAK["value"], _directory_bytes(Path(temporary.name))
        )
    return result


def _patched_exit(self: Any, exc_type: Any, exc: Any, tb: Any) -> Any:
    temporary = getattr(self, "_temporary", None)
    if temporary is not None:
        TEMP_PEAK["value"] = max(
            TEMP_PEAK["value"], _directory_bytes(Path(temporary.name))
        )
    return REAL_EXIT(self, exc_type, exc, tb)


def _locality_sorted(iterable: Any, *, key: Any = None, reverse: bool = False) -> Any:
    if key is not None and not reverse:
        values = list(iterable)
        if values and all(isinstance(value, RespondentIdentity) for value in values):
            return values
        return REAL_SORTED(values, key=key)
    return REAL_SORTED(iterable, key=key, reverse=reverse)


def _load_capsule(path: Path) -> tuple[SavedC11Admission, RuntimeObjectCatalog, dict[str, Any]]:
    capsule = json.loads(path.read_text(encoding="utf-8"))
    document = capsule["catalog"]
    catalog = RuntimeObjectCatalog(
        authorities=tuple(materialize_public_object(v) for v in document["authorities"]),
        predicates=tuple(materialize_public_object(v) for v in document["predicates"]),
        queries=tuple(materialize_public_object(v) for v in document["queries"]),
        discovery_authorities=tuple(
            materialize_public_object(v) for v in document["discovery_authorities"]
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


def _fact_material(fact: Any) -> dict[str, Any]:
    projection = _jsonable(fact.semantic_projection())
    return {
        "ref": _jsonable(fact.ref),
        "typed_state": fact.typed_state,
        "raw_denominator_support": getattr(fact, "raw_denominator_support", None),
        "replay_ref": _jsonable(getattr(fact, "replay_ref", None)),
        "projection_sha256": hashlib.sha256(
            canonical_json(fact.semantic_projection()).encode()
        ).hexdigest(),
        "projection": projection,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capsule", required=True)
    parser.add_argument("--mode", choices=("baseline", "candidate"), required=True)
    parser.add_argument("--queries", default="selected")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    result: dict[str, Any] = {
        "schema": "PYAT1006_LOCALITY_EXPERIMENT@1",
        "label": "EXPERIMENT_NOT_IMPLEMENTED",
        "mode": args.mode,
        "capsule": args.capsule,
        "host": {
            "hostname": os.uname().nodename,
            "platform": sys.platform,
            "machine": os.uname().machine,
            "python": sys.version,
            "pyarrow": pq.__version__ if hasattr(pq, "__version__") else None,
        },
        "status": "RUNNING",
        "queries": {},
    }
    out = Path(args.out)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    pq.ParquetFile = _tracked_parquet_file
    DirectEstateI03Session._build = _patched_build
    DirectEstateI03Session.__enter__ = _patched_enter
    DirectEstateI03Session.__exit__ = _patched_exit
    if args.mode == "candidate":
        query_eval.sorted = _locality_sorted
    try:
        COUNTER.reset("admission")
        start = time.monotonic()
        admission, catalog, capsule = _load_capsule(Path(args.capsule))
        result["admission_seconds"] = time.monotonic() - start
        result["admission"] = COUNTER.material()
        result["release"] = capsule["release"]
        result["family_counts"] = capsule.get("family_counts")
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
            COUNTER.reset("query_eval")
            TEMP_PEAK["value"] = 0
            cpu_start = time.process_time()
            start = time.monotonic()
            observed = admission.execute_i03(
                query_ref=query.ref, predicate_ref=predicate.ref,
            )
            wall = time.monotonic() - start
            cpu = time.process_time() - cpu_start
            result["queries"][name] = {
                "wall_seconds": wall,
                "cpu_seconds": cpu,
                "temp_sqlite_peak_bytes": TEMP_PEAK["value"],
                "reads": COUNTER.material(),
                "facts": [_fact_material(fact) for fact in observed.facts],
                "release_refs": [_jsonable(ref) for ref in observed.release_refs],
                "query_ref": _jsonable(query.ref),
                "predicate_ref": _jsonable(predicate.ref),
            }
            result["rss_peak_bytes"] = _rss_peak()
            out.write_text(
                json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
        result["status"] = "MEASURED"
        result["rss_peak_bytes"] = _rss_peak()
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({
            "status": result["status"],
            "mode": result["mode"],
            "queries": {
                name: {
                    "wall_seconds": row["wall_seconds"],
                    "cpu_seconds": row["cpu_seconds"],
                    "reads": row["reads"]["total_reads"],
                    "rows_decoded": sum(
                        phase["rows_decoded"]
                        for phase in row["reads"]["by_phase"].values()
                    ),
                    "fact_refs": [fact["ref"] for fact in row["facts"]],
                    "states": [fact["typed_state"] for fact in row["facts"]],
                    "denominators": [fact["raw_denominator_support"] for fact in row["facts"]],
                    "projection_sha256": [fact["projection_sha256"] for fact in row["facts"]],
                }
                for name, row in result["queries"].items()
            },
            "rss_peak_bytes": result["rss_peak_bytes"],
        }, indent=2, sort_keys=True))
        return 0
    finally:
        pq.ParquetFile = REAL_PARQUET_FILE
        DirectEstateI03Session._build = REAL_BUILD
        DirectEstateI03Session.__enter__ = REAL_ENTER
        DirectEstateI03Session.__exit__ = REAL_EXIT
        if args.mode == "candidate":
            query_eval.sorted = REAL_SORTED


if __name__ == "__main__":
    raise SystemExit(main())
