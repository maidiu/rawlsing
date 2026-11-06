from __future__ import annotations

import gc
import hashlib
import itertools
import json
import os
import resource
import sys
import time
from collections import Counter
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor,
    RuntimeObjectCatalog,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry as PublicAuthorityRegistry
from rawlsing_next.pre553_empirical_objects import canonical_json, semantic_hash
from rawlsing_next.pre553_empirical_query import (
    execute_empirical_query,
    replay_empirical_query,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _build_source,
    _cell_map,
    _predicate,
    _query,
    _query_authority,
    _ref,
    _response_leaf,
)

QUESTION_NAMES = ("A", "B", "C", "K", "X", "Y", "Z", "U")


def perf() -> float:
    return time.perf_counter()


def cpu() -> float:
    return time.process_time()


def maxrss_bytes() -> int:
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def frac(value: Any) -> Fraction | None:
    if value is None:
        return None
    if isinstance(value, Mapping) and "$exact_fraction" in value:
        numerator, denominator = value["$exact_fraction"]
        return Fraction(int(numerator), int(denominator))
    return Fraction(value)


def fraction_dict(value: Fraction | None) -> Mapping[str, Any] | None:
    if value is None:
        return None
    return {"$exact_fraction": [value.numerator, value.denominator]}


def ref_value(ref: Any, field: str) -> Any:
    if isinstance(ref, Mapping):
        return ref[field]
    return getattr(ref, field)


def ref_material(ref: Any, full: bool = True) -> Any:
    if isinstance(ref, Mapping) and "authority_id" in ref:
        return {
            "authority_id": ref.get("authority_id"),
            "authority_version": ref.get("authority_version"),
            "authority_content_hash": ref.get("authority_content_hash"),
        }
    if not isinstance(ref, Mapping) and hasattr(ref, "authority_id"):
        return {
            "authority_id": ref.authority_id,
            "authority_version": ref.authority_version,
            "authority_content_hash": ref.authority_content_hash,
        }
    if isinstance(ref, Mapping):
        material = {"kind": ref.get("kind"), "object_id": ref.get("object_id"),
                    "content_hash": ref.get("content_hash")}
    else:
        material = {"kind": ref.kind, "object_id": ref.object_id,
                    "content_hash": ref.content_hash}
    if full:
        return material
    return [material["object_id"], material["content_hash"]]


def refs_digest(refs: Sequence[Any]) -> str:
    payload = [ref_material(ref, True) for ref in refs]
    return semantic_hash(payload)


def main_rows(n: int):
    rows = []
    weights = {}
    ids = []
    for i in range(n):
        a = i & 1
        b = (i >> 1) & 1
        c = (i >> 2) & 1
        x = a
        y = b
        z = x ^ y
        u = c
        k = a ^ b ^ c
        rid = f"R{i:06d}"
        ids.append(rid)
        rows.append({
            "id": rid,
            "responses": {"A": a, "B": b, "C": c, "K": k, "X": x, "Y": y, "Z": z, "U": u},
            "coords": {"G": "A" if i % 3 == 0 else "B"},
        })
        weights[rid] = ("WEIGHT_VALID_AUTHORIZED", str(1 + (i % 4)))
    risk_sets = {
        "R": {q: set(ids) for q in QUESTION_NAMES},
        "S": {q: {rid for i, rid in enumerate(ids) if i % 2 == 0} for q in QUESTION_NAMES},
    }
    return rows, weights, risk_sets


def build_main_source(n: int):
    tag = f"c4-main-{n}"
    rows, weights, risk_sets = main_rows(n)
    source = _build_source(tag, rows, risk_sets=risk_sets, weights=weights)
    qa = _query_authority(tag)
    all_p = _branch_predicate(source, qa, tag=f"{tag}-all")
    minority_members = tuple(list(source["respondents"].values())[: max(1, n // 100)])
    minority_p = _branch_predicate(source, qa, members=minority_members, tag=f"{tag}-minority")
    x1_p = _predicate(source, qa, _response_leaf(source, qa, "X", 1), tag=f"{tag}-x1")
    y1_p = _predicate(source, qa, _response_leaf(source, qa, "Y", 1), tag=f"{tag}-y1")
    x_leaf = _response_leaf(source, qa, "X", 1)
    y_leaf = _response_leaf(source, qa, "Y", 1)
    xor_p = _predicate(
        source, qa,
        {"op": "AND", "children": [
            {"op": "OR", "children": [x_leaf, y_leaf]},
            {"op": "NOT", "children": [{"op": "AND", "children": [x_leaf, y_leaf]}]},
        ]},
        tag=f"{tag}-xor",
    )
    ops = [
        ("all_K_raw", "G1_compatible", all_p, ("K",), "R", "RAW", f"{tag}-allKr"),
        ("all_K_weighted", "G1_compatible", all_p, ("K",), "R", "GOVERNED_WEIGHTED", f"{tag}-allKw"),
        ("all_K_raw_sibling", "G1_compatible", all_p, ("K",), "R", "RAW", f"{tag}-allKr2"),
        ("all_X_raw", "G2_target_sibling", all_p, ("X",), "R", "RAW", f"{tag}-allXr"),
        ("all_Z_raw", "G2_target_sibling", all_p, ("Z",), "R", "RAW", f"{tag}-allZr"),
        ("all_XY_raw", "G3_arity", all_p, ("X", "Y"), "R", "RAW", f"{tag}-allXYr"),
        ("all_XYZ_raw", "G3_arity", all_p, ("X", "Y", "Z"), "R", "RAW", f"{tag}-allXYZr"),
        ("all_ABCK_raw", "G3_arity", all_p, ("A", "B", "C", "K"), "R", "RAW", f"{tag}-allABCKr"),
        ("cond_X1_target_Y", "G4_directional", x1_p, ("Y",), "R", "RAW", f"{tag}-x1Y"),
        ("cond_Y1_target_X", "G4_directional", y1_p, ("X",), "R", "RAW", f"{tag}-y1X"),
        ("xor_condition_target_Z", "G5_xor", xor_p, ("Z",), "R", "RAW", f"{tag}-xorZ"),
        ("minority_branch_target_K", "G6_minority", minority_p, ("K",), "R", "RAW", f"{tag}-minK"),
        ("risk_S_target_K", "G7_incompatible_risk", all_p, ("K",), "S", "RAW", f"{tag}-riskSK"),
    ]
    queries = []
    for op_id, group, predicate, targets, risk, measure, query_tag in ops:
        query = _query(source, qa, predicate, targets, risk=risk, measure=measure, tag=query_tag)
        queries.append({
            "op_id": op_id,
            "group": group,
            "predicate": predicate,
            "query": query,
            "targets": targets,
            "risk": risk,
            "measure": measure,
        })
    predicates = []
    for candidate in (all_p, minority_p, x1_p, y1_p, xor_p):
        if all(candidate.ref != existing.ref for existing in predicates):
            predicates.append(candidate)
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qa)),
        predicates=tuple(predicates),
        queries=tuple(item["query"] for item in queries),
        discovery_authorities=(),
    )
    ref_to_id = {respondent.ref.object_id: rid for rid, respondent in source["respondents"].items()}
    return {
        "source": source,
        "qa": qa,
        "ops": queries,
        "catalog": catalog,
        "ref_to_id": ref_to_id,
        "rows": rows,
        "weights": weights,
    }


def _predicate_truth(op: Mapping[str, Any], rid: str, values: Mapping[str, Mapping[str, int]]) -> bool:
    group = op["group"]
    if group in {"G1_compatible", "G2_target_sibling", "G3_arity", "G7_incompatible_risk"}:
        return True
    if op["op_id"] == "cond_X1_target_Y":
        return values["X"][rid] == 1
    if op["op_id"] == "cond_Y1_target_X":
        return values["Y"][rid] == 1
    if op["op_id"] == "xor_condition_target_Z":
        return values["X"][rid] != values["Y"][rid]
    if op["op_id"] == "minority_branch_target_K":
        return False
    raise AssertionError(op["op_id"])


def oracle_for(rows: Sequence[Mapping[str, Any]], op: Mapping[str, Any], weights: Mapping[str, Any]):
    ids = [row["id"] for row in rows]
    values = {
        q: {row["id"]: int(row["responses"][q]) for row in rows} for q in QUESTION_NAMES
    }
    index = {rid: i for i, rid in enumerate(ids)}
    if op["risk"] == "R":
        risk_ids = set(ids)
    elif op["risk"] == "S":
        risk_ids = {rid for i, rid in enumerate(ids) if i % 2 == 0}
    else:
        raise AssertionError(op["risk"])
    if op["op_id"] == "minority_branch_target_K":
        minority = set(ids[: max(1, len(ids) // 100)])
        members = [rid for rid in ids if rid in risk_ids and rid in minority]
    else:
        members = [rid for rid in ids if rid in risk_ids and _predicate_truth(op, rid, values)]
    targets = tuple(op["targets"])
    if len(targets) == 1:
        domain = ["0", "1"]
    else:
        domain = list(itertools.product(("0", "1"), repeat=len(targets)))
    raw_cells = {}
    weighted_cells = {}
    for cell in domain:
        raw_cells[cell] = 0
        weighted_cells[cell] = Fraction(0, 1)
    for rid in members:
        if len(targets) == 1:
            cell = str(values[targets[0]][rid])
        else:
            cell = tuple(str(values[target][rid]) for target in targets)
        raw_cells[cell] += 1
        weight = Fraction(1 + (index[rid] % 4), 1)
        weighted_cells[cell] += weight
    weighted_denominator = (
        sum((Fraction(1 + (index[rid] % 4), 1) for rid in members), Fraction(0, 1))
        if op["measure"] == "GOVERNED_WEIGHTED" else None
    )
    return {
        "typed_state": "SUPPORTED" if members else "ZERO_SUPPORT",
        "risk_ids": sorted(risk_ids, key=index.get),
        "denominator_ids": sorted(members, key=index.get),
        "raw_cells": raw_cells,
        "weighted_cells": weighted_cells if op["measure"] == "GOVERNED_WEIGHTED" else None,
        "weighted_denominator": weighted_denominator,
        "domain": domain,
    }


def normalized_cells(fact: Any) -> dict[Any, Mapping[str, Any]]:
    result = {}
    for row in fact.target_topology["complete_cell_semantic_projection"]:
        cell = row["cell"]
        key = cell if isinstance(cell, str) else tuple(cell)
        result[key] = row
    return result


def fact_projection(
    fact: Any,
    ref_to_id: Mapping[str, str],
    *,
    full_refs: bool = True,
    full_provenance: bool = True,
) -> Mapping[str, Any]:
    def member_identity(refs):
        if full_refs:
            return [ref_material(ref, True) for ref in refs]
        return [ref_material(ref, False) for ref in refs]

    def ids(refs):
        return [ref_to_id.get(ref_value(ref, "object_id"), ref_value(ref, "object_id")) for ref in refs]

    provenance = tuple(fact.source_empirical_provenance_refs)
    dependencies = tuple(fact.dependency_refs)
    cells = []
    for row in fact.target_topology.get("complete_cell_semantic_projection", ()):
        cell = row["cell"]
        cells.append({
            "cell": cell,
            "cell_state": row["cell_state"],
            "raw_numerator_support": row["raw_numerator_support"],
            "weighted_numerator_support_if_authorized":
                row["weighted_numerator_support_if_authorized"],
        })
    risk_member_refs = tuple(getattr(fact, "risk_set_member_refs", ()))
    denominator_member_refs = tuple(getattr(fact, "denominator_member_refs", ()))
    return {
        "fact_ref": ref_material(fact.ref, True),
        "replay_ref": ref_material(fact.replay_ref, True),
        "producer_replay_locator_or_reference_root":
            ref_material(fact.producer_replay_locator_or_reference_root, True),
        "typed_state": fact.typed_state,
        "execution_detail": fact.execution_detail,
        "p02_failure_state": getattr(fact, "p02_failure_state", None),
        "raw_numerator_support": fact.raw_numerator_support,
        "raw_denominator_support": fact.raw_denominator_support,
        "raw_resolved_target_support": getattr(fact, "raw_resolved_target_support", None),
        "weighted_numerator_support_if_authorized":
            fact.weighted_numerator_support_if_authorized,
        "weighted_denominator_support_if_authorized":
            fact.weighted_denominator_support_if_authorized,
        "empirical_query_spec_ref": ref_material(fact.empirical_query_spec_ref, True),
        "condition_predicate_ref": ref_material(fact.condition_predicate_ref, True),
        "risk_set_ref": ref_material(fact.risk_set_ref, True),
        "measure_basis_ref": ref_material(fact.measure_basis_ref, True),
        "empirical_universe_refs": [ref_material(ref, True) for ref in fact.empirical_universe_refs],
        "source_scope_mode": fact.source_scope_mode,
        "measure_kind": fact.measure_kind,
        "risk_set_type": fact.risk_set_type,
        "target_domain_identity": getattr(fact, "target_domain_identity", None),
        "target_arity": fact.target_topology.get("arity"),
        "complete_cell_semantic_projection": cells,
        "risk_set_member_count": len(risk_member_refs),
        "denominator_member_count": len(denominator_member_refs),
        "risk_set_member_ids": ids(risk_member_refs),
        "denominator_member_ids": ids(denominator_member_refs),
        "risk_set_member_refs": member_identity(risk_member_refs),
        "denominator_member_refs": member_identity(denominator_member_refs),
        "authority_snapshot_refs": [ref_material(ref, True) for ref in fact.authority_snapshot_refs],
        "source_empirical_provenance_ref_count": len(provenance),
        "source_empirical_provenance_ref_sha256": refs_digest(provenance),
        "dependency_ref_count": len(dependencies),
        "dependency_ref_sha256": refs_digest(dependencies),
        "source_empirical_provenance_refs":
            [ref_material(ref, True) for ref in provenance] if full_provenance else None,
        "dependency_refs":
            [ref_material(ref, True) for ref in dependencies] if full_provenance else None,
    }

def compare_fact(fact: Any, expected: Mapping[str, Any], ref_to_id: Mapping[str, str]):
    errors = []
    actual_cells = normalized_cells(fact)
    expected_cells = expected["raw_cells"]
    if fact.typed_state != expected["typed_state"]:
        errors.append(f"typed_state {fact.typed_state!r} != {expected['typed_state']!r}")
    if set(actual_cells) != set(expected_cells):
        errors.append(f"cell domain {sorted(map(str, actual_cells))} != {sorted(map(str, expected_cells))}")
    for cell, expected_count in expected_cells.items():
        row = actual_cells.get(cell)
        if row is None:
            errors.append(f"missing cell {cell!r}")
            continue
        if row["raw_numerator_support"] != expected_count:
            errors.append(f"cell {cell!r} raw {row['raw_numerator_support']} != {expected_count}")
    if expected["weighted_cells"] is not None:
        for cell, expected_value in expected["weighted_cells"].items():
            row = actual_cells.get(cell)
            if row is None:
                errors.append(f"missing weighted cell {cell!r}")
                continue
            actual_value = frac(row["weighted_numerator_support_if_authorized"])
            if actual_value != expected_value:
                errors.append(f"cell {cell!r} weighted {actual_value} != {expected_value}")
        actual_weighted_denominator = frac(fact.weighted_denominator_support_if_authorized)
        if actual_weighted_denominator != expected["weighted_denominator"]:
            errors.append(
                f"weighted denominator {actual_weighted_denominator} != "
                f"{expected['weighted_denominator']}"
            )
    actual_risk = sorted(
        (ref_to_id.get(ref_value(ref, "object_id"), ref_value(ref, "object_id")) for ref in fact.risk_set_member_refs)
    )
    actual_denominator = sorted(
        (ref_to_id.get(ref_value(ref, "object_id"), ref_value(ref, "object_id")) for ref in fact.denominator_member_refs)
    )
    if actual_risk != sorted(expected["risk_ids"]):
        errors.append("risk member identity mismatch")
    if actual_denominator != sorted(expected["denominator_ids"]):
        errors.append("denominator member identity mismatch")
    if fact.raw_denominator_support != len(expected["denominator_ids"]):
        errors.append("raw denominator count mismatch")
    if fact.raw_numerator_support != len(expected["denominator_ids"]):
        errors.append("raw numerator count mismatch")
    return errors


class Recorder:
    def __init__(self) -> None:
        self.current: str | None = None
        self.records: dict[str, dict[str, Any]] = {}

    def begin(self, op_id: str) -> None:
        self.current = op_id
        self.records[op_id] = {"components": {}, "counts": Counter()}

    def add(self, name: str, seconds: float) -> None:
        entry = self.records[self.current]["components"].setdefault(
            name, {"calls": 0, "seconds": 0.0}
        )
        entry["calls"] += 1
        entry["seconds"] += seconds

    def count(self, name: str) -> None:
        self.records[self.current]["counts"][name] += 1


def timed(recorder: Recorder, name: str, function):
    def wrapper(*args, **kwargs):
        start = perf()
        try:
            return function(*args, **kwargs)
        finally:
            recorder.add(name, perf() - start)
    wrapper.__name__ = getattr(function, "__name__", name)
    return wrapper


def counted(recorder: Recorder, name: str, function):
    def wrapper(*args, **kwargs):
        recorder.count(name)
        return function(*args, **kwargs)
    wrapper.__name__ = getattr(function, "__name__", name)
    return wrapper


def install_recorder(recorder: Recorder):
    import rawlsing_next._pre553_query_eval as qeval
    import rawlsing_next._pre553_query_predicate as qpred
    import rawlsing_next.pre553_empirical_query as query

    saved = {}
    for module, name in (
        (qeval, "_routing_fact_for"),
        (qeval, "_eval_predicate"),
        (qeval, "_weight_for"),
        (qeval, "_target_configuration"),
        (qeval, "_make_execution_replay_ref"),
        (qeval, "_cell_projection"),
        (query, "_resolve_release_indices"),
        (query, "_release_index_for"),
        (query, "_build_release_index"),
        (query, "_evaluate_index_group"),
        (query, "_build_fact"),
        (query, "_build_negative_fact"),
    ):
        saved[(module.__name__, name)] = getattr(module, name)
        setattr(module, name, timed(recorder, name, getattr(module, name)))
    for module in (qeval, qpred):
        saved[(module.__name__, "_select_respondent_events")] = getattr(module, "_select_respondent_events")
        setattr(module, "_select_respondent_events",
                counted(recorder, "_select_respondent_events", getattr(module, "_select_respondent_events")))
    for module in (qeval, qpred):
        saved[(module.__name__, "_validate_public_object_authorities")] = getattr(
            module, "_validate_public_object_authorities"
        )
        setattr(module, "_validate_public_object_authorities",
                timed(recorder, "_validate_public_object_authorities",
                      getattr(module, "_validate_public_object_authorities")))
    return saved


def index_state(repository: C11Repository) -> Mapping[str, Any]:
    entries = []
    for (release_ref, universe_ref), index in sorted(
        repository._i03_release_indices.items(), key=lambda item: (item[0][0].key, item[0][1].key)
    ):
        entries.append({
            "release_key": release_ref.key,
            "universe_key": universe_ref.key,
            "index_object_id": hex(id(index)),
            "respondent_count": len(index.respondents),
        })
    token = hashlib.sha256(
        "|".join(
            f"{item['release_key']}::{item['universe_key']}::{item['index_object_id']}"
            for item in entries
        ).encode("utf-8")
    ).hexdigest()
    return {"count": len(entries), "token": token, "entries": entries}


def source_stats(source: Mapping[str, Any], release: Any) -> Mapping[str, Any]:
    from rawlsing_next._pre553_c11_execution_view import _CompactPublicObjects
    from rawlsing_next.pre553_empirical_objects import RespondentEvent

    public = release.public_objects
    if isinstance(public, _CompactPublicObjects):
        return {
            "release_ref": ref_material(release.release_ref, True),
            "replay_ref": ref_material(release.replay_manifest.ref, True),
            "public_entry_count": len(public.entries),
            "non_event_count": len(public.non_events),
            "compact_event_count": len(public.lane.selectors),
            "event_body_json_bytes": None,
            "internal_record_count": len(release.internal_records),
            "release_public_objects_class": type(public).__name__,
        }
    event_count = 0
    body_bytes = 0
    counts = Counter()
    for obj in public:
        counts[type(obj).__name__] += 1
        if isinstance(obj, RespondentEvent):
            event_count += 1
            body_bytes += len(canonical_json(obj.semantic_projection()).encode("utf-8"))
    return {
        "release_ref": ref_material(release.release_ref, True),
        "replay_ref": ref_material(release.replay_manifest.ref, True),
        "public_object_count": len(public),
        "event_count": event_count,
        "event_body_json_bytes": body_bytes,
        "object_family_counts": dict(sorted(counts.items())),
        "internal_record_count": len(release.internal_records),
        "release_public_objects_class": type(public).__name__,
    }


def cache_stats(directory: Path | None) -> Mapping[str, Any]:
    if directory is None:
        return {"enabled": False}
    files = []
    if directory.is_dir():
        for path in sorted(directory.glob("*.parquet")):
            files.append({"name": path.name, "bytes": path.stat().st_size})
    return {
        "enabled": True,
        "directory": str(directory),
        "file_count": len(files),
        "total_bytes": sum(item["bytes"] for item in files),
        "files": files,
    }


def execute_op(executor, op):
    return executor.execute_i03(
        query_ref=op["query"].ref,
        predicate_ref=op["predicate"].ref,
    )


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _json_default(value):
    if isinstance(value, Mapping):
        return dict(value)
    if isinstance(value, Fraction):
        return {"$exact_fraction": [value.numerator, value.denominator]}
    if isinstance(value, (set, frozenset)):
        return sorted(value)
    if isinstance(value, tuple):
        return list(value)
    return str(value)


def dump_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, sort_keys=True, indent=2, default=_json_default)
        handle.write("\n")


def compact_release(release, cache_dir: str | None, read_counter=None, write_counter=None):
    from rawlsing_next import _pre553_c11_execution_view as compact

    original_read = compact._read_bodies
    original_write = compact._write_bodies
    if read_counter is not None:
        def read(path, key, selectors):
            value = original_read(path, key, selectors)
            read_counter.append(value is not None)
            return value
        compact._read_bodies = read
    if write_counter is not None:
        def write(path, key, bodies):
            write_counter.append(1)
            return original_write(path, key, bodies)
        compact._write_bodies = write
    try:
        public = compact._compact_public_objects(
            release,
            physical_binding=lambda: {"bench": "phase1", "schema": "tools/bench_common.py"},
            projection_binding="programma-pyat-l03-c4-phase1",
        )
    finally:
        compact._read_bodies = original_read
        compact._write_bodies = original_write
    return replace(release, public_objects=public)


def fresh_repository(release) -> C11Repository:
    return C11Repository((release,))


__all__ = [
    "QUESTION_NAMES", "REPO_ROOT", "PublicAuthorityRegistry",
    "CarrierNeutralResearchExecutor", "C11Repository", "RuntimeObjectCatalog",
    "build_main_source", "oracle_for", "compare_fact", "fact_projection",
    "execute_empirical_query", "replay_empirical_query", "main_rows", "normalized_cells",
    "Recorder", "install_recorder", "index_state", "source_stats", "cache_stats",
    "execute_op", "load_json", "dump_json", "compact_release", "fresh_repository",
    "ref_material", "ref_value", "refs_digest", "frac", "fraction_dict", "perf", "cpu", "maxrss_bytes",
    "sha256_text", "canonical_json", "semantic_hash", "replace", "gc",
]
