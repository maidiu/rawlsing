"""Same-source V0/V1/V2 compact-physical comparison driver (prepared, not run here).

V0 = full validated native C11 release + repository + actual I03.
V1 = existing default compact Arrow facade.
V2 = same compact facade with an explicit workload-owned private Parquet/Zstd cache.
Each variant must run in its own fresh process so Darwin ru_maxrss is not inherited.
This file contains no architecture bakeoff and no new carrier/truth engine.
"""
from __future__ import annotations

import argparse
import contextlib
import gc
import hashlib
import json
import os
import platform
import resource
import statistics
import subprocess
import sys
import time
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping

HERE = Path(__file__).resolve().parent
RETURN_DIR = HERE.parent
REPO_ROOT = RETURN_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import bench_common as bc  # noqa: E402
from rawlsing_next import _pre553_c11_execution_view as compact_view  # noqa: E402
from rawlsing_next import pre553_source_backed_c11_facade as facade  # noqa: E402
import rawlsing_next.pre553_empirical_query as empirical_query  # noqa: E402
import rawlsing_next._pre553_query_eval as query_eval  # noqa: E402
from rawlsing_next.pre553_c11_ingest import QuestionVariableBinding, RespondentIdentity, TypedAbsence  # noqa: E402
from rawlsing_next.pre553_c11_repository import C11Repository  # noqa: E402
from rawlsing_next.pre553_carrier_execution import (  # noqa: E402
    CarrierNeutralResearchExecutor,
    RuntimeObjectCatalog,
)
from rawlsing_next.pre553_empirical_query import I03GroupedExecutionScope  # noqa: E402
from rawlsing_next.pre553_empirical_objects import (  # noqa: E402
    EmpiricalQuerySpec,
    EmpiricalUniverse,
    ExactRef,
    RoutingEligibilityFact,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import (  # noqa: E402
    PhysicalCell,
    PhysicalMissingState,
    PhysicalVariable,
)
from rawlsing_next.pre553_source_backed_c11_facade import (  # noqa: E402
    CoordinateSlotRule,
    ExactPhysicalCellStream,
    GovernedC11Projection,
    OccurrenceRule,
    PhysicalSlot,
    ResponseSlotRule,
    ResponseValueRule,
    RowRespondentBinding,
    WeightSlotRule,
    WeightValueRule,
    build_source_backed_c11_repository,
    build_validated_source_backed_c11_release_from_stream,
    physical_value_binding_key,
)
from rawlsing_next.tests.test_pre553_empirical_query import (  # noqa: E402
    _auth,
    _branch_predicate,
    _h,
    _predicate,
    _query,
    _query_authority,
    _ref,
    _response_leaf,
)
from rawlsing_next.tests.pre553_query_frontier_fixtures import _custom_query  # noqa: E402


SCHEMA = "PROGRAMMA_PYAT_L03_C4_COMPACT_CURRENT@1"
VARIANTS = ("v0", "v1", "v2-cold", "v2-warm")
QUESTIONS = ("X", "Y", "Z", "K", "O", "R", "M")
VARIABLE_ORDINALS = {name: i for i, name in enumerate(QUESTIONS, 1)}
CELL_ORDINALS = {**VARIABLE_ORDINALS, "G": 8, "W": 9}
SOURCE_FORMAT = "SYNTHETIC_NONRESPONDENT_FIXTURE"


def _occ(question: str, kind: str = "SCALAR_SINGULAR", **extra) -> OccurrenceRule:
    return OccurrenceRule(
        "0", _ref("TOPOLOGY", f"compact-current-{question}-{kind}"),
        {"kind": kind, **extra},
    )


def _ordered_occ(question: str, ordinal: int) -> OccurrenceRule:
    return OccurrenceRule(
        str(ordinal), _ref("TOPOLOGY", f"compact-current-{question}-ORDERED"),
        {"kind": "ORDERED_SEQUENCE", "semantic_ordinal": ordinal},
    )


def _repeated_occ(question: str, index: int) -> OccurrenceRule:
    return OccurrenceRule(
        str(index), _ref("TOPOLOGY", f"compact-current-{question}-REPEATED"),
        {"kind": "REPEATED_EVENT", "multiplicity_index": index},
    )


def _source_fixture(n: int, *, tag: str = "compact-current"):
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    source_auth = _auth(
        f"{tag}-source", "SOURCE_SEMANTICS_TOPOLOGY",
        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
    )
    mapping_auth = _auth(
        f"{tag}-mapping", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
        families=("RespondentEvent@1.0.0",),
    )
    coord_auth = _auth(
        f"{tag}-coord", "COORDINATE_SEMANTICS",
        families=("EmpiricalCoordinateFact@1.0.0",),
    )
    routing_auth = _auth(
        f"{tag}-routing", "ROUTING_RISK_SET",
        families=("RoutingEligibilityFact@1.0.0",),
    )
    weight_auth = _auth(
        f"{tag}-weight", "WEIGHT_DESIGN_ESTIMAND",
        families=("WeightMeasureFact@1.0.0",),
    )
    replay_auth = _auth(
        f"{tag}-replay", "REPLAY_PROTOCOL",
        families=("ReplayReceipt@1.0.0",),
    )
    projection_auth = _auth(
        f"{tag}-projection", "SOURCE_SEMANTICS_TOPOLOGY",
        families=("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0", "WeightMeasureFact@1.0.0"),
    )
    authorities = (
        source_auth, mapping_auth, coord_auth, routing_auth, weight_auth,
        replay_auth, projection_auth,
    )
    source_sha = _h(f"compact-current-source:{tag}:{n}")
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"{tag}-universe"),
        raw_source_identity=f"RAW-{tag}-{n}",
        source_family="SURVEY",
        study_product_release=f"STUDY-{tag}/REL-1",
        instrument_release=f"INST-{tag}",
        country_geography="US",
        sampling_geography="US-NATIONAL",
        raw_wave="W1",
        canonical_wave_if_governed=None,
        field_or_reference_time="2026-01",
        target_population_and_sample_frame="ADULTS",
        sampling_design_regime="DESIGN-COMPACT-CURRENT",
        respondent_namespace=f"NS-{tag}",
        source_artifact_import_lineage=f"SOURCE-LINEAGE-{tag}",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    qrefs = {name: _ref("QUESTION_NATIVE", f"{tag}-{name}") for name in QUESTIONS}
    questions = tuple(
        QuestionVariableBinding(
            empirical_universe_ref=universe.ref,
            native_question_ref=qrefs[name],
            instrument_question_version="1",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=source_auth.authority_ref,
            topology_authority_ref=source_auth.authority_ref,
        )
        for name in QUESTIONS
    )
    qbind = dict(zip(QUESTIONS, questions))
    respondent_ids = [f"R{i:06d}" for i in range(n)]
    respondents = tuple(
        RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=rid,
            source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", f"{tag}-{rid}"),
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        )
        for rid in respondent_ids
    )
    by_id = dict(zip(respondent_ids, respondents))
    risk = _ref("RISK_SET", f"{tag}-risk")
    routing = []
    for index, rid in enumerate(respondent_ids):
        respondent = by_id[rid]
        for name in QUESTIONS:
            eligible = not (name == "Y" and index % 7 == 0)
            state = "ELIGIBLE_APPLICABLE" if eligible else "NOT_ELIGIBLE"
            routing.append(RoutingEligibilityFact(
                typed_state=state,
                authority_snapshot_refs=(routing_auth.authority_ref,),
                dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"{tag}-routing-{rid}-{name}"),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                question_or_target_ref=qrefs[name],
                risk_set_ref=risk,
                routing_rule_ref=_ref("ROUTING_RULE", f"{tag}-{name}"),
                applicability_state=state,
                routing_state=state,
                parent_predicate_refs=(),
                member_set_replay_ref=_ref("MEMBER_SET", f"{tag}-{name}-{state}"),
            ))

    rows = []
    for i in range(n):
        rows.append({
            "X": str(i & 1),
            "Y": str((i >> 1) & 1),
            "Z": str((i >> 2) & 1),
            "K": str((i & 1) ^ ((i >> 1) & 1) ^ ((i >> 2) & 1)),
            "O": "AB" if i % 2 == 0 else "BA",
            "R": "XY" if i % 3 else "XZ",
            "M": None if i % 13 == 0 else str(i % 2),
            "G": "A" if i % 4 else "B",
            "W": 1 + (i % 4),
        })
    variables = tuple(
        PhysicalVariable(ordinal, name, None, f"label-{name}", {}, (), {}, {})
        for name, ordinal in CELL_ORDINALS.items()
    )
    cells = []
    for index, row in enumerate(rows, 1):
        for name, ordinal in CELL_ORDINALS.items():
            raw = row[name]
            state = PhysicalMissingState.SYSTEM_MISSING if raw is None else PhysicalMissingState.OBSERVED_STORAGE_VALUE
            cells.append(PhysicalCell(index, ordinal, name, raw, state, None))
    cells = tuple(cells)

    pkey = lambda raw, state=PhysicalMissingState.OBSERVED_STORAGE_VALUE: physical_value_binding_key(raw, state)
    response_slots = []
    for name in ("X", "Y", "Z", "K"):
        values = []
        for value in ("0", "1"):
            values.append(ResponseValueRule(
                pkey(value), "SUBSTANTIVE_RESPONSE", (_occ(name),), value, mapping_auth.authority_ref,
            ))
        response_slots.append(ResponseSlotRule(PhysicalSlot(CELL_ORDINALS[name], name), qbind[name], tuple(values)))
    response_slots = tuple(response_slots) + (
        ResponseSlotRule(PhysicalSlot(CELL_ORDINALS["O"], "O"), qbind["O"], (
            ResponseValueRule(pkey("AB"), "SUBSTANTIVE_RESPONSE", (_ordered_occ("O", 0), _ordered_occ("O", 1)), "AB", mapping_auth.authority_ref),
            ResponseValueRule(pkey("BA"), "SUBSTANTIVE_RESPONSE", (_ordered_occ("O", 0), _ordered_occ("O", 1)), "BA", mapping_auth.authority_ref),
        )),
        ResponseSlotRule(PhysicalSlot(CELL_ORDINALS["R"], "R"), qbind["R"], (
            ResponseValueRule(pkey("XY"), "SUBSTANTIVE_RESPONSE", (_repeated_occ("R", 0), _repeated_occ("R", 1)), "XY", mapping_auth.authority_ref),
            ResponseValueRule(pkey("XZ"), "SUBSTANTIVE_RESPONSE", (_repeated_occ("R", 0), _repeated_occ("R", 1)), "XZ", mapping_auth.authority_ref),
        )),
        ResponseSlotRule(PhysicalSlot(CELL_ORDINALS["M"], "M"), qbind["M"], (
            ResponseValueRule(pkey("1"), "SUBSTANTIVE_RESPONSE", (_occ("M"),), "1", mapping_auth.authority_ref),
            ResponseValueRule(pkey("0"), "SUBSTANTIVE_RESPONSE", (_occ("M"),), "0", mapping_auth.authority_ref),
            ResponseValueRule(pkey(None, PhysicalMissingState.SYSTEM_MISSING), "MISSING", (_occ("M"),)),
        )),
    )
    coordinate_slots = (
        CoordinateSlotRule(
            PhysicalSlot(CELL_ORDINALS["G"], "G"),
            _ref("COORDINATE_NATIVE", f"{tag}-G"),
            _ref("UNIT_TAXONOMY", f"{tag}-G"),
            "2026-01",
            coord_auth.authority_ref,
            copy_observed_raw=True,
        ),
    )
    weight_values = tuple(WeightValueRule(pkey(value), value) for value in (1, 2, 3, 4))
    weight_slots = (
        WeightSlotRule(
            PhysicalSlot(CELL_ORDINALS["W"], "W"),
            "W",
            _ref("WEIGHT_SOURCE", f"{tag}-W"),
            weight_auth.authority_ref,
            weight_auth.authority_ref,
            _ref("SCOPE", f"{tag}-W"),
            values=weight_values,
        ),
    )
    projection = GovernedC11Projection(
        projection_identity_ref=_ref("C11_SEMANTIC_PROJECTION", f"{tag}-{n}"),
        source_artifact_id=f"SOURCE-{tag}",
        expected_source_sha256=source_sha,
        source_family_id="SURVEY",
        study_product_id=f"STUDY-{tag}",
        release_id=f"REL-{tag}",
        instrument_release_id=f"INST-{tag}",
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:test:compact-current:snapshot:{tag}:{n}", source_sha,
        ),
        universes=(universe,),
        respondents=respondents,
        row_bindings=tuple(
            RowRespondentBinding(index, respondent.ref)
            for index, respondent in enumerate(respondents, 1)
        ),
        questions=questions,
        response_slots=response_slots,
        coordinate_slots=coordinate_slots,
        routing=tuple(routing),
        weight_slots=weight_slots,
        authority_snapshots=authorities,
        source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"),
        structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(auth.authority_ref for auth in authorities),
        projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay_auth.authority_ref,
        tie_order_ref=_ref("ORDER_RULE", f"{tag}-canonical-ref-sort"),
        replay_protocol_version="1.0.0",
    )
    decoder_digest = _h(f"compact-current-admitted-decoder:{tag}:{n}")
    stream = ExactPhysicalCellStream(
        source_sha256=source_sha,
        row_count=n,
        cell_iter_factory=lambda: iter(cells),
        transport_identity="COMPACT_CURRENT_EXACT_SOURCE_BACKED_STREAM",
        decoder_metadata_digest=decoder_digest,
    )
    source_stub = {
        "universe": universe,
        "respondents": by_id,
        "qrefs": qrefs,
        "crefs": {"G": _ref("COORDINATE_NATIVE", f"{tag}-G")},
        "risk_refs": {"R": risk},
        "source_auth": source_auth,
        "authorities": authorities,
    }
    return {
        "tag": tag,
        "n": n,
        "source_sha": source_sha,
        "decoder_digest": decoder_digest,
        "stream": stream,
        "projection": projection,
        "source_stub": source_stub,
        "cells": cells,
        "rows": rows,
    }


def _operations(fixture):
    source = fixture["source_stub"]
    qa = _query_authority(fixture["tag"])
    all_p = _branch_predicate(source, qa, tag=f"{fixture['tag']}-all")
    minority_members = tuple(list(source["respondents"].values())[: max(1, fixture["n"] // 100)])
    minority_p = _branch_predicate(source, qa, members=minority_members, tag=f"{fixture['tag']}-minority")
    x1 = _predicate(source, qa, _response_leaf(source, qa, "X", 1), tag=f"{fixture['tag']}-x1")
    y1 = _predicate(source, qa, _response_leaf(source, qa, "Y", 1), tag=f"{fixture['tag']}-y1")
    x_leaf = _response_leaf(source, qa, "X", 1)
    y_leaf = _response_leaf(source, qa, "Y", 1)
    xor_p = _predicate(
        source, qa,
        {"op": "AND", "children": [
            {"op": "OR", "children": [x_leaf, y_leaf]},
            {"op": "NOT", "children": [{"op": "AND", "children": [x_leaf, y_leaf]}]},
        ]},
        tag=f"{fixture['tag']}-xor",
    )
    empty_p = _branch_predicate(source, qa, members=(), tag=f"{fixture['tag']}-empty")
    queries = {
        "raw_Y": _query(source, qa, all_p, ("Y",), measure="RAW", tag=f"{fixture['tag']}-raw-Y"),
        "weighted_Y": _query(source, qa, all_p, ("Y",), measure="GOVERNED_WEIGHTED", tag=f"{fixture['tag']}-weighted-Y"),
        "joint_XY": _query(source, qa, all_p, ("X", "Y"), measure="RAW", tag=f"{fixture['tag']}-joint-XY"),
        "joint_XYZ": _query(source, qa, all_p, ("X", "Y", "Z"), measure="RAW", tag=f"{fixture['tag']}-joint-XYZ"),
        "joint_XYZK": _query(source, qa, all_p, ("X", "Y", "Z", "K"), measure="RAW", tag=f"{fixture['tag']}-joint-XYZK"),
        "cond_X1_Y": _query(source, qa, x1, ("Y",), measure="RAW", tag=f"{fixture['tag']}-cond-X1-Y"),
        "cond_Y1_X": _query(source, qa, y1, ("X",), measure="RAW", tag=f"{fixture['tag']}-cond-Y1-X"),
        "xor_Z": _query(source, qa, xor_p, ("Z",), measure="RAW", tag=f"{fixture['tag']}-xor-Z"),
        "minority_Y": _query(source, qa, minority_p, ("Y",), measure="RAW", tag=f"{fixture['tag']}-minority-Y"),
        "zero_support_Y": _query(source, qa, empty_p, ("Y",), measure="RAW", tag=f"{fixture['tag']}-zero-Y"),
        "unsupported_O": _query(source, qa, all_p, ("O",), measure="RAW", tag=f"{fixture['tag']}-unsupported-O"),
    }
    missing = _query(source, qa, all_p, ("M",), measure="RAW", tag=f"{fixture['tag']}-missing-M")
    missing_fields = dict(missing.semantic_fields)
    missing_topology = dict(missing_fields["target_arity_and_topology"])
    missing_components = [dict(component) for component in missing_topology["components"]]
    missing_components[0]["domain"] = ["0", "1", {"typed_response_state": "MISSING"}]
    missing_components[0]["included_states"] = ["SUBSTANTIVE_RESPONSE", "MISSING"]
    missing_topology["components"] = missing_components
    missing_fields["target_arity_and_topology"] = missing_topology
    queries["missing_M"] = EmpiricalQuerySpec(
        typed_state=missing.typed_state,
        authority_snapshot_refs=missing.authority_snapshot_refs,
        dependency_refs=missing.dependency_refs,
        producer_replay_locator_or_reference_root=missing.producer_replay_locator_or_reference_root,
        **missing_fields,
    )
    ordered = _custom_query(
        source, qa, all_p, "O", topology="ORDERED_SEQUENCE",
        domain=[["AB", "AB"], ["BA", "BA"]], included_states=("SUBSTANTIVE_RESPONSE",),
        tag=f"{fixture['tag']}-ordered-O",
    )
    queries["ordered_O"] = ordered
    predicate_catalog = []
    for predicate in (all_p, minority_p, x1, y1, xor_p, empty_p):
        if all(predicate.ref != existing.ref for existing in predicate_catalog):
            predicate_catalog.append(predicate)
    predicate_by_key = {predicate.ref.key: predicate for predicate in predicate_catalog}
    ops = []
    for op_id, query in queries.items():
        predicate = predicate_by_key[
            exact_ref(query.condition_predicate_ref, "query.condition_predicate_ref").key
        ]
        ops.append({"op_id": op_id, "query": query, "predicate": predicate})
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*fixture["source_stub"]["authorities"], qa)),
        predicates=tuple(predicate_catalog),
        queries=tuple(query for query in queries.values()),
        discovery_authorities=(),
    )
    return ops, catalog


class Recorder:
    def __init__(self):
        self.entries: dict[str, dict[str, float | int]] = {}

    def add(self, name: str, wall: float, cpu: float, count: int = 1) -> None:
        item = self.entries.setdefault(name, {"wall_s": 0.0, "cpu_s": 0.0, "count": 0})
        item["wall_s"] += wall
        item["cpu_s"] += cpu
        item["count"] += count

    def timer(self, name: str, function):
        def wrapper(*args, **kwargs):
            start_wall, start_cpu = time.perf_counter(), time.process_time()
            try:
                return function(*args, **kwargs)
            finally:
                self.add(name, time.perf_counter() - start_wall, time.process_time() - start_cpu)
        wrapper.__name__ = getattr(function, "__name__", name)
        return wrapper

    def phase(self, name: str):
        recorder = self

        @contextlib.contextmanager
        def context():
            start_wall, start_cpu = time.perf_counter(), time.process_time()
            try:
                yield
            finally:
                recorder.add(name, time.perf_counter() - start_wall, time.process_time() - start_cpu)

        return context()


def _cache_probe():
    original_read = compact_view._read_bodies
    original_write = compact_view._write_bodies
    state = {"reads": [], "writes": 0}

    def read(path, key, selectors):
        value = original_read(path, key, selectors)
        state["reads"].append(value is not None)
        return value

    def write(path, key, bodies):
        state["writes"] += 1
        return original_write(path, key, bodies)

    @contextlib.contextmanager
    def probe():
        compact_view._read_bodies = read
        compact_view._write_bodies = write
        try:
            yield state
        finally:
            compact_view._read_bodies = original_read
            compact_view._write_bodies = original_write

    return probe


def _cache_stats(directory: Path | None):
    return bc.cache_stats(directory)


def _fact_record(fact):
    return {
        "fact_ref": bc.ref_material(fact.ref),
        "replay_ref": bc.ref_material(fact.replay_ref),
        "typed_state": fact.typed_state,
        "p02_failure_state": getattr(fact, "p02_failure_state", None),
        "raw_numerator_support": fact.raw_numerator_support,
        "raw_denominator_support": fact.raw_denominator_support,
        "raw_resolved_target_support": getattr(fact, "raw_resolved_target_support", None),
        "weighted_numerator_support_if_authorized": fact.weighted_numerator_support_if_authorized,
        "weighted_denominator_support_if_authorized": fact.weighted_denominator_support_if_authorized,
        "cell_projection": list(fact.target_topology.get("complete_cell_semantic_projection", ())),
        "risk_member_count": len(getattr(fact, "risk_set_member_refs", ())),
        "denominator_member_count": len(getattr(fact, "denominator_member_refs", ())),
        "provenance_ref_count": len(fact.source_empirical_provenance_refs),
        "dependency_ref_count": len(fact.dependency_refs),
        "exact_fact_material_sha256": semantic_hash(fact.as_dict()),
    }


def _run_variant(args):
    if args.variant is None:
        raise SystemExit("variant mode requires --variant")
    n = args.n or (3 if args.smoke else None)
    if not n:
        raise SystemExit("variant mode requires --n")
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    cache_root = Path(args.cache_root).resolve() if args.cache_root else None
    report_cache_root = cache_root if args.variant.startswith("v2") else None
    if args.variant.startswith("v2"):
        if cache_root is None:
            raise SystemExit("V2 requires --cache-root")
        cache_root.mkdir(mode=0o700, parents=True, exist_ok=True)
        os.chmod(cache_root, 0o700)
        os.environ["RAWLSING_C11_ACCELERATOR_DIR"] = str(cache_root)
    else:
        os.environ.pop("RAWLSING_C11_ACCELERATOR_DIR", None)

    recorder = Recorder()
    with recorder.phase("fixture_build"):
        fixture = _source_fixture(n, tag="compact-current")
        ops, catalog = _operations(fixture)
    source = fixture["stream"]
    projection = fixture["projection"]

    probe = _cache_probe()
    with probe() as cache_state:
        if args.variant == "v0":
            with recorder.phase("validation_build"):
                release = build_validated_source_backed_c11_release_from_stream(source, projection)
            with recorder.phase("repository_commit"):
                repository = C11Repository((release,))
        elif args.variant in {"v1", "v2-cold", "v2-warm"}:
            original_validation = facade.build_validated_source_backed_c11_release_from_stream
            original_compact = facade._compact_public_objects
            facade.build_validated_source_backed_c11_release_from_stream = recorder.timer(
                "validation_build", original_validation
            )
            facade._compact_public_objects = recorder.timer("compact_conversion", original_compact)
            try:
                with recorder.phase("facade_build"):
                    repository, release = build_source_backed_c11_repository(
                        source, projection,
                        current_authorities=projection.authority_snapshots,
                    )
            finally:
                facade.build_validated_source_backed_c11_release_from_stream = original_validation
                facade._compact_public_objects = original_compact
        else:
            raise SystemExit(f"unknown variant {args.variant}")

        executor = CarrierNeutralResearchExecutor(
            repository, (release.release_ref,), catalog,
        )
        original_build_index = empirical_query._build_release_index
        original_build_fact = empirical_query._build_fact
        original_replay = query_eval._make_execution_replay_ref
        empirical_query._build_release_index = recorder.timer("index_build", original_build_index)
        empirical_query._build_fact = recorder.timer("fact_build", original_build_fact)
        query_eval._make_execution_replay_ref = recorder.timer("replay_build", original_replay)
        fact_records = []
        facts_path = outdir / f"{args.variant}_facts.jsonl"
        try:
            with facts_path.open("w", encoding="utf-8") as facts_handle:
                for op in ops:
                    gc.collect()
                    start_wall, start_cpu = time.perf_counter(), time.process_time()
                    result = executor.execute_i03(
                        query_ref=op["query"].ref,
                        predicate_ref=op["predicate"].ref,
                    )
                    wall = time.perf_counter() - start_wall
                    cpu = time.process_time() - start_cpu
                    recorder.add("query_execution", wall, cpu)
                    for position, fact in enumerate(result.facts):
                        facts_handle.write(json.dumps(fact.as_dict(), sort_keys=True, separators=(",", ":")) + "\n")
                        record = {"op_id": op["op_id"], "position": position, **_fact_record(fact)}
                        record["wall_s"] = wall
                        record["cpu_s"] = cpu
                        fact_records.append(record)
        finally:
            empirical_query._build_release_index = original_build_index
            empirical_query._build_fact = original_build_fact
            query_eval._make_execution_replay_ref = original_replay

    compact_public = release.public_objects
    compact_info = {
        "class": type(compact_public).__name__,
        "compact": isinstance(compact_public, compact_view._CompactPublicObjects),
    }
    if compact_info["compact"]:
        compact_info.update({
            "entry_count": len(compact_public.entries),
            "selector_count": len(compact_public.lane.selectors),
            "non_event_count": len(compact_public.non_events),
            "by_respondent_groups": len(compact_public.by_respondent),
        })
        source_bytes = {
            "compact_body_nbytes": getattr(compact_public.lane.bodies, "nbytes", None),
            "event_body_json_bytes": None,
        }
    else:
        compact_info.update({
            "public_object_count": len(compact_public),
            "event_count": sum(
                1 for obj in compact_public if obj.schema_id == "RespondentEvent"
            ),
        })
        source_bytes = {
            "compact_body_nbytes": None,
            "event_body_json_bytes": sum(
                len(bc.canonical_json(obj.semantic_projection()).encode("utf-8"))
                for obj in compact_public
                if obj.schema_id == "RespondentEvent"
            ),
        }
    process = {
        "pid": os.getpid(),
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
        "ru_maxrss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "ru_utime_s": resource.getrusage(resource.RUSAGE_SELF).ru_utime,
        "ru_stime_s": resource.getrusage(resource.RUSAGE_SELF).ru_stime,
        "argv": sys.argv,
        "env": {
            key: os.environ.get(key) for key in (
                "PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE", "TMPDIR",
                "RAWLSING_C11_ACCELERATOR_DIR",
            )
        },
    }
    payload = {
        "schema": SCHEMA,
        "mode": "variant",
        "variant": args.variant,
        "n": n,
        "smoke": bool(args.smoke),
        "timing_claim": "SMOKE_ONLY_NOT_BENCHMARK" if args.smoke else "MEASURED_VARIANT",
        "source": {
            "source_sha256": fixture["source_sha"],
            "decoder_metadata_digest": fixture["decoder_digest"],
            "physical_cell_count": len(fixture["cells"]),
            "row_count": n,
            "cache_binding_eligible": bool(fixture["decoder_digest"]),
            "legacy_in_memory_incidence": False,
            "event_body_json_bytes": source_bytes["event_body_json_bytes"],
            "compact_body_nbytes": source_bytes["compact_body_nbytes"],
        },
        "projection": {
            "identity": bc.ref_material(projection.projection_identity_ref),
            "cache_identity": projection.cache_identity,
        },
        "release": {
            "release_ref": bc.ref_material(release.release_ref),
            "replay_ref": bc.ref_material(release.replay_manifest.ref),
            "compact": compact_info,
        },
        "phases": recorder.entries,
        "counts": {
            "index_builds": recorder.entries.get("index_build", {}).get("count", 0),
            "fact_builds": recorder.entries.get("fact_build", {}).get("count", 0),
            "replay_builds": recorder.entries.get("replay_build", {}).get("count", 0),
            "compact_conversions": recorder.entries.get("compact_conversion", {}).get("count", 0),
        },
        "rss_note": "ru_maxrss_bytes is whole-process Darwin high-water; phases report wall/CPU only, not RSS attribution",
        "queries": fact_records,
        "facts_file": str(facts_path),
        "cache": {
            "directory": str(report_cache_root) if report_cache_root else None,
            "read_hits": sum(1 for hit in cache_state["reads"] if hit),
            "read_misses": sum(1 for hit in cache_state["reads"] if not hit),
            "writes": cache_state["writes"],
            "files": _cache_stats(report_cache_root),
            "legacy_in_memory_incidence_not_used": True,
        },
        "process": process,
    }
    if args.variant == "v2-warm" and payload["cache"]["read_hits"] < 1:
        payload["cache"]["eligible_hit"] = False
        payload["error"] = "V2_WARM_CACHE_NOT_ELIGIBLE_OR_NOT_HIT"
    else:
        payload["cache"]["eligible_hit"] = payload["cache"]["read_hits"] > 0
    bc.dump_json(outdir / f"{args.variant}.json", payload)
    if payload.get("error"):
        raise SystemExit(payload["error"])


def _run_compare(args):
    n = args.n or (3 if args.smoke else None)
    if not n:
        raise SystemExit("compare mode requires --n")
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    cache_root = Path(args.cache_root).resolve() if args.cache_root else (outdir / "cache").resolve()
    cache_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(cache_root, 0o700)
    if not args.keep_cache:
        for path in cache_root.glob("*.parquet"):
            path.unlink()
    base_env = dict(os.environ)
    base_env["PYTHONHASHSEED"] = "0"
    base_env["PYTHONDONTWRITEBYTECODE"] = "1"
    tmp_dir = outdir / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    base_env["TMPDIR"] = str(tmp_dir)
    base_env.pop("RAWLSING_C11_ACCELERATOR_DIR", None)
    commands = []
    for variant in VARIANTS:
        env = dict(base_env)
        if variant.startswith("v2"):
            env["RAWLSING_C11_ACCELERATOR_DIR"] = str(cache_root)
        command = [
            sys.executable, str(Path(__file__).resolve()),
            "--mode", "variant", "--variant", variant, "--n", str(n),
            "--outdir", str(outdir), "--cache-root", str(cache_root),
        ]
        if args.smoke:
            command.append("--smoke")
        start = time.perf_counter()
        proc = subprocess.run(command, env=env, cwd=str(REPO_ROOT), capture_output=True, text=True)
        wall = time.perf_counter() - start
        commands.append({
            "variant": variant,
            "command": command,
            "exit": proc.returncode,
            "parent_wall_s": wall,
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
        })
        if proc.returncode != 0:
            raise SystemExit(f"{variant} failed: {proc.stderr[-2000:]}")
    payloads = {
        variant: json.loads((outdir / f"{variant}.json").read_text())
        for variant in VARIANTS
    }
    facts = {}
    for variant in VARIANTS:
        with (outdir / f"{variant}_facts.jsonl").open("r", encoding="utf-8") as handle:
            facts[variant] = [json.loads(line) for line in handle if line.strip()]
    baseline = facts["v0"]
    equality = {
        variant: facts[variant] == baseline for variant in ("v1", "v2-cold", "v2-warm")
    }
    release_identity_equal = (
        payloads["v0"]["release"]["release_ref"] == payloads["v1"]["release"]["release_ref"]
        == payloads["v2-cold"]["release"]["release_ref"] == payloads["v2-warm"]["release"]["release_ref"]
    )
    source_identity_equal = (
        payloads["v0"]["source"]["source_sha256"] == payloads["v1"]["source"]["source_sha256"]
        == payloads["v2-cold"]["source"]["source_sha256"] == payloads["v2-warm"]["source"]["source_sha256"]
        and payloads["v0"]["projection"]["identity"] == payloads["v1"]["projection"]["identity"]
        == payloads["v2-cold"]["projection"]["identity"] == payloads["v2-warm"]["projection"]["identity"]
    )
    cache_checks = {
        "v2_cold_miss_write": (
            payloads["v2-cold"]["cache"]["read_misses"] >= 1
            and payloads["v2-cold"]["cache"]["writes"] >= 1
        ),
        "v2_warm_hit": payloads["v2-warm"]["cache"]["read_hits"] >= 1,
        "v2_same_cache_files": (
            payloads["v2-cold"]["cache"]["files"] == payloads["v2-warm"]["cache"]["files"]
        ),
    }
    summary = {
        "schema": SCHEMA,
        "mode": "compare",
        "n": n,
        "smoke": bool(args.smoke),
        "timing_claim": "SMOKE_ONLY_NOT_BENCHMARK" if args.smoke else "MEASURED_COMPARISON",
        "cache_root": str(cache_root),
        "commands": commands,
        "variants": payloads,
        "facts_exact_equal": equality,
        "release_identity_equal": release_identity_equal,
        "source_identity_equal": source_identity_equal,
        "cache_checks": cache_checks,
        "pass": (
            all(equality.values())
            and release_identity_equal
            and source_identity_equal
            and all(cache_checks.values())
        ),
    }
    path = outdir / ("compare_smoke.json" if args.smoke else f"compare_n{n}.json")
    bc.dump_json(path, summary)
    print(json.dumps({
        "path": str(path),
        "n": n,
        "smoke": bool(args.smoke),
        "facts_exact_equal": equality,
        "release_identity_equal": release_identity_equal,
        "source_identity_equal": source_identity_equal,
        "cache_checks": cache_checks,
        "pass": summary["pass"],
    }, indent=2, sort_keys=True))
    if not summary["pass"]:
        raise SystemExit("COMPACT_CURRENT_COMPARISON_FAILED")



def _grouped_ops(fixture):
    ops, catalog = _operations(fixture)
    qa = _query_authority(fixture["tag"])
    source = fixture["source_stub"]
    by_id = {op["op_id"]: op for op in ops}
    extras = []
    for op_id, base_id, targets, measure in (
        ("raw_Y_sibling", "raw_Y", ("Y",), "RAW"),
        ("weighted_Y_sibling", "weighted_Y", ("Y",), "GOVERNED_WEIGHTED"),
        ("joint_XY_sibling", "joint_XY", ("X", "Y"), "RAW"),
    ):
        predicate = by_id[base_id]["predicate"]
        query = _query(
            source, qa, predicate, targets, measure=measure,
            tag=f"{fixture['tag']}-{op_id}",
        )
        extras.append({"op_id": op_id, "query": query, "predicate": predicate})
    all_ops = ops + extras
    catalog = RuntimeObjectCatalog(
        authorities=catalog.authorities,
        predicates=catalog.predicates,
        queries=tuple(op["query"] for op in all_ops),
        discovery_authorities=(),
    )
    return all_ops, catalog


def _compact_release(fixture):
    os.environ.pop("RAWLSING_C11_ACCELERATOR_DIR", None)
    repository, release = build_source_backed_c11_repository(
        fixture["stream"], fixture["projection"],
        current_authorities=fixture["projection"].authority_snapshots,
    )
    return release


def _same_facts(left, right):
    return [fact.as_dict() for fact in left] == [fact.as_dict() for fact in right]


def _grouped_pass(executor, ops, scope, keep_facts=False, compare_to=None):
    records = {}
    materials = {}
    for op in ops:
        gc.collect()
        start_wall, start_cpu = time.perf_counter(), time.process_time()
        result = executor.execute_i03(
            query_ref=op["query"].ref,
            predicate_ref=op["predicate"].ref,
            group_scope=scope,
        )
        wall = time.perf_counter() - start_wall
        cpu = time.process_time() - start_cpu
        facts = tuple(result.facts)
        fact_material = [fact.as_dict() for fact in facts]
        record = {
            "op_id": op["op_id"],
            "wall_s": wall,
            "cpu_s": cpu,
            "typed_states": [fact.typed_state for fact in facts],
            "fact_refs": [bc.ref_material(fact.ref) for fact in facts],
            "replay_refs": [bc.ref_material(fact.replay_ref) for fact in facts],
            "exact_fact_material_sha256": semantic_hash(fact_material),
            "summary": [_fact_record(fact) for fact in facts],
        }
        if compare_to is not None:
            record["facts_equal"] = fact_material == compare_to.get(op["op_id"])
        records[op["op_id"]] = record
        if keep_facts:
            materials[op["op_id"]] = fact_material
    return records, materials


def _totals(records):
    return {
        "wall_s": sum(item["wall_s"] for item in records.values()),
        "cpu_s": sum(item["cpu_s"] for item in records.values()),
    }


def _expected_cells(fixture, op_id):
    rows = fixture["rows"]
    n = fixture["n"]
    by_id = {}
    if op_id in {"raw_Y", "weighted_Y", "raw_Y_sibling", "weighted_Y_sibling"}:
        targets, predicate, risk_target = ("Y",), "all", "Y"
    elif op_id in {"joint_XY", "joint_XY_sibling"}:
        targets, predicate, risk_target = ("X", "Y"), "all", "Y"
    elif op_id == "joint_XYZ":
        targets, predicate, risk_target = ("X", "Y", "Z"), "all", "Y"
    elif op_id == "joint_XYZK":
        targets, predicate, risk_target = ("X", "Y", "Z", "K"), "all", "Y"
    elif op_id == "cond_X1_Y":
        targets, predicate, risk_target = ("Y",), "x1", "Y"
    elif op_id == "cond_Y1_X":
        targets, predicate, risk_target = ("X",), "y1", "X"
    elif op_id == "xor_Z":
        targets, predicate, risk_target = ("Z",), "xor", "Z"
    elif op_id == "minority_Y":
        targets, predicate, risk_target = ("Y",), "minority", "Y"
    elif op_id == "missing_M":
        targets, predicate, risk_target = ("M",), "all", "M"
    elif op_id == "ordered_O":
        targets, predicate, risk_target = ("O",), "all", "O"
    elif op_id == "zero_support_Y":
        return {"typed_state": "ZERO_SUPPORT", "raw_denominator": 0}
    elif op_id == "unsupported_O":
        return {"typed_state": "UNRESOLVED", "p02_failure_state": "UNSUPPORTED_RESPONSE_TOPOLOGY"}
    else:
        return None
    members = []
    for index, row in enumerate(rows):
        if risk_target == "Y" and index % 7 == 0:
            continue
        if predicate == "x1" and row["X"] != "1":
            continue
        if predicate == "y1" and row["Y"] != "1":
            continue
        if predicate == "xor" and row["X"] == row["Y"]:
            continue
        if predicate == "minority" and index >= max(1, n // 100):
            continue
        members.append((index, row))
    domain = None
    if targets == ("M",):
        domain = ["0", "1", {"typed_response_state": "MISSING"}]
    elif targets == ("O",):
        domain = [["AB", "AB"], ["BA", "BA"]]
    elif len(targets) == 1:
        domain = ["0", "1"]
    else:
        import itertools
        domain = list(itertools.product(("0", "1"), repeat=len(targets)))
    raw_cells = {bc.canonical_json(cell): 0 for cell in domain}
    weighted_cells = {bc.canonical_json(cell): Fraction(0, 1) for cell in domain}
    weighted_denominator = Fraction(0, 1)
    for index, row in members:
        values = []
        for target in targets:
            if target == "M":
                value = {"typed_response_state": "MISSING"} if row["M"] is None else row["M"]
            elif target == "O":
                value = [row["O"], row["O"]]
            else:
                value = row[target]
            values.append(value)
        cell = values[0] if len(values) == 1 else values
        key = bc.canonical_json(cell)
        if key not in raw_cells:
            return {"oracle_domain_error": key}
        raw_cells[key] += 1
        weight = Fraction(1 + (index % 4), 1)
        weighted_cells[key] += weight
        weighted_denominator += weight
    return {
        "typed_state": "SUPPORTED" if members else "ZERO_SUPPORT",
        "raw_denominator": len(members),
        "raw_numerator": len(members),
        "raw_cells": raw_cells,
        "weighted_denominator": weighted_denominator if op_id.startswith("weighted") else None,
        "weighted_cells": weighted_cells if op_id.startswith("weighted") else None,
    }


def _check_expected(fact_material, expected):
    if expected is None:
        return []
    fields = fact_material.get("semantic_fields", fact_material)
    errors = []
    if fact_material["typed_state"] != expected["typed_state"]:
        errors.append(f"typed_state {fact_material['typed_state']} != {expected['typed_state']}")
        return errors
    if "p02_failure_state" in expected:
        if fields.get("p02_failure_state") != expected["p02_failure_state"]:
            errors.append("p02 failure state mismatch")
        return errors
    if fields["raw_denominator_support"] != expected["raw_denominator"]:
        errors.append("raw denominator mismatch")
    if fields["raw_numerator_support"] != expected.get("raw_numerator", 0):
        errors.append("raw numerator mismatch")
    cells = {
        bc.canonical_json(row["cell"]): row
        for row in fields["target_topology"].get("complete_cell_semantic_projection", ())
    }
    for key, count in expected.get("raw_cells", {}).items():
        row = cells.get(key)
        if row is None:
            errors.append(f"missing cell {key}")
            continue
        if row["raw_numerator_support"] != count:
            errors.append(f"cell {key} raw mismatch")
        if expected.get("weighted_cells") is not None:
            actual = bc.frac(row["weighted_numerator_support_if_authorized"])
            if actual != expected["weighted_cells"][key]:
                errors.append(f"cell {key} weighted mismatch")
    if expected.get("weighted_denominator") is not None:
        actual = bc.frac(fields["weighted_denominator_support_if_authorized"])
        if actual != expected["weighted_denominator"]:
            errors.append("weighted denominator mismatch")
    return errors


def _grouped_process_metadata():
    return {
        "pid": os.getpid(),
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
        "ru_maxrss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "ru_utime_s": resource.getrusage(resource.RUSAGE_SELF).ru_utime,
        "ru_stime_s": resource.getrusage(resource.RUSAGE_SELF).ru_stime,
        "argv": sys.argv,
        "env": {key: os.environ.get(key) for key in (
            "PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE", "TMPDIR",
            "RAWLSING_C11_ACCELERATOR_DIR",
        )},
        "rss_note": "ru_maxrss_bytes is whole-process Darwin high-water; phases report wall/CPU only",
    }


def _run_grouped(args):
    n = args.n or (3 if args.smoke else None)
    if not n:
        raise SystemExit("grouped mode requires --n")
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    os.environ.pop("RAWLSING_C11_ACCELERATOR_DIR", None)
    recorder = Recorder()
    with recorder.phase("fixture_build"):
        fixture = _source_fixture(n, tag="compact-current")
        ops, catalog = _grouped_ops(fixture)
    setup_start = time.perf_counter()
    release = _compact_release(fixture)
    setup_wall = time.perf_counter() - setup_start

    def make_executor():
        return CarrierNeutralResearchExecutor(
            C11Repository((release,)), (release.release_ref,), catalog,
        )

    cold_base = make_executor()
    cold_cand = make_executor()
    cold_scope = I03GroupedExecutionScope()
    cold_base_records, cold_base_facts = _grouped_pass(cold_base, ops, None, keep_facts=True)
    cold_cand_records, cold_cand_facts = _grouped_pass(
        cold_cand, ops, cold_scope, keep_facts=True, compare_to=cold_base_facts,
    )
    facts_files = {}
    for label, materials in (("baseline", cold_base_facts), ("candidate", cold_cand_facts)):
        path = outdir / f"grouped_cold_{label}_facts.jsonl"
        with path.open("w", encoding="utf-8") as handle:
            for op in ops:
                for material in materials.get(op["op_id"], ()):
                    handle.write(json.dumps(material, sort_keys=True, separators=(",", ":")) + "\n")
        facts_files[label] = str(path)
    cold_equal = all(
        cold_cand_records[op_id].get("facts_equal") is True
        and cold_base_records[op_id]["fact_refs"] == cold_cand_records[op_id]["fact_refs"]
        and cold_base_records[op_id]["replay_refs"] == cold_cand_records[op_id]["replay_refs"]
        for op_id in cold_base_records
    )

    warm_base = make_executor()
    warm_cand = make_executor()
    warm_scope = I03GroupedExecutionScope()
    _grouped_pass(warm_base, ops, None)
    _grouped_pass(warm_cand, ops, warm_scope)
    warm_rounds = []
    for round_index in range(1, args.rounds + 1):
        baseline, baseline_facts = _grouped_pass(warm_base, ops, None, keep_facts=True)
        candidate, _ = _grouped_pass(warm_cand, ops, warm_scope, compare_to=baseline_facts)
        warm_rounds.append({
            "round": round_index,
            "baseline": {"ops": baseline, **_totals(baseline)},
            "candidate": {"ops": candidate, **_totals(candidate)},
            "all_facts_equal": all(
                candidate[op_id].get("facts_equal") is True
                and baseline[op_id]["fact_refs"] == candidate[op_id]["fact_refs"]
                and baseline[op_id]["replay_refs"] == candidate[op_id]["replay_refs"]
                for op_id in baseline
            ),
            "scope": warm_scope.receipt(),
        })

    single_op = ops[0]
    single_base = make_executor()
    single_cand = make_executor()
    single_scope = I03GroupedExecutionScope()
    single_base_records, single_base_facts = _grouped_pass(single_base, [single_op], None, keep_facts=True)
    single_cand_records, _ = _grouped_pass(single_cand, [single_op], single_scope, compare_to=single_base_facts)
    single_equal = single_cand_records[single_op["op_id"]].get("facts_equal") is True

    by_id = {op["op_id"]: op for op in ops}
    incompatible_ids = (
        "raw_Y", "joint_XYZK", "cond_X1_Y", "cond_Y1_X",
        "xor_Z", "minority_Y", "zero_support_Y", "ordered_O",
    )
    incompatible_ops = [by_id[op_id] for op_id in incompatible_ids]
    inc_base = make_executor()
    inc_cand = make_executor()
    inc_scope = I03GroupedExecutionScope()
    inc_first_base, inc_first_base_facts = _grouped_pass(inc_base, incompatible_ops, None, keep_facts=True)
    inc_first_cand, _ = _grouped_pass(inc_cand, incompatible_ops, inc_scope, compare_to=inc_first_base_facts)
    scope_first = inc_scope.receipt()
    inc_second_base, inc_second_base_facts = _grouped_pass(inc_base, incompatible_ops, None, keep_facts=True)
    inc_second_cand, _ = _grouped_pass(inc_cand, incompatible_ops, inc_scope, compare_to=inc_second_base_facts)
    inc_equal_first = all(
        inc_first_cand[op_id].get("facts_equal") is True for op_id in inc_first_base
    )
    inc_equal_second = all(
        inc_second_cand[op_id].get("facts_equal") is True for op_id in inc_second_base
    )

    capacity_ops = [by_id["raw_Y"], by_id["joint_XYZK"]]
    cap_base = make_executor()
    cap_cand = make_executor()
    cap_scope = I03GroupedExecutionScope(max_groups=1)
    cap_base_records, cap_base_facts = _grouped_pass(cap_base, capacity_ops, None, keep_facts=True)
    cap_cand_records, _ = _grouped_pass(cap_cand, capacity_ops, cap_scope, compare_to=cap_base_facts)
    capacity_equal = all(
        cap_cand_records[op_id].get("facts_equal") is True for op_id in cap_base_records
    )

    from bench_grouped_phase2 import Counters

    counter_base = make_executor()
    counter_cand = make_executor()
    counter_scope = I03GroupedExecutionScope()
    _grouped_pass(counter_base, ops, None)
    _grouped_pass(counter_cand, ops, counter_scope)
    baseline_counters = Counters()
    saved = baseline_counters.wrap()
    try:
        _grouped_pass(counter_base, ops, None)
    finally:
        Counters.restore(saved)
    candidate_counters = Counters()
    saved = candidate_counters.wrap()
    try:
        _grouped_pass(counter_cand, ops, counter_scope)
    finally:
        Counters.restore(saved)

    oracle_errors = {}
    for op in ops:
        expected = _expected_cells(fixture, op["op_id"])
        errors = []
        for material in cold_base_facts.get(op["op_id"], ()):
            errors.extend(_check_expected(material, expected))
        oracle_errors[op["op_id"]] = errors

    payload = {
        "schema": SCHEMA,
        "mode": "grouped",
        "n": n,
        "smoke": bool(args.smoke),
        "timing_claim": "SMOKE_ONLY_NOT_BENCHMARK" if args.smoke else "MEASURED_GROUPED_COMPACT",
        "source": {
            "source_sha256": fixture["source_sha"],
            "decoder_metadata_digest": fixture["decoder_digest"],
            "row_count": n,
            "physical_cell_count": len(fixture["cells"]),
        },
        "release": {
            "release_ref": bc.ref_material(release.release_ref),
            "replay_ref": bc.ref_material(release.replay_manifest.ref),
            "compact": isinstance(release.public_objects, compact_view._CompactPublicObjects),
            "selector_count": (
                len(release.public_objects.lane.selectors)
                if isinstance(release.public_objects, compact_view._CompactPublicObjects) else None
            ),
        },
        "setup_s": {
            "fixture_build": recorder.entries,
            "compact_release_build": setup_wall,
        },
        "facts_files": facts_files,
        "cold": {
            "baseline": {"ops": cold_base_records, **_totals(cold_base_records)},
            "candidate": {"ops": cold_cand_records, **_totals(cold_cand_records)},
            "all_facts_equal": cold_equal,
            "scope": cold_scope.receipt(),
        },
        "warm_rounds": warm_rounds,
        "single_operation": {
            "op_id": single_op["op_id"],
            "baseline": {"ops": single_base_records, **_totals(single_base_records)},
            "candidate": {"ops": single_cand_records, **_totals(single_cand_records)},
            "all_facts_equal": single_equal,
            "scope": single_scope.receipt(),
        },
        "incompatible": {
            "op_ids": list(incompatible_ids),
            "first_pass": {
                "baseline": {"ops": inc_first_base, **_totals(inc_first_base)},
                "candidate": {"ops": inc_first_cand, **_totals(inc_first_cand)},
                "all_facts_equal": inc_equal_first,
                "scope": scope_first,
            },
            "second_pass": {
                "baseline": {"ops": inc_second_base, **_totals(inc_second_base)},
                "candidate": {"ops": inc_second_cand, **_totals(inc_second_cand)},
                "all_facts_equal": inc_equal_second,
                "scope": inc_scope.receipt(),
            },
        },
        "capacity_fallback": {
            "op_ids": [op["op_id"] for op in capacity_ops],
            "max_groups": 1,
            "baseline": {"ops": cap_base_records, **_totals(cap_base_records)},
            "candidate": {"ops": cap_cand_records, **_totals(cap_cand_records)},
            "all_facts_equal": capacity_equal,
            "scope": cap_scope.receipt(),
            "note": "capacity fallback is a bounded limit, not evidence of cheaper behavior",
        },
        "counters": {
            "baseline": {"calls": baseline_counters.calls, "times_s": baseline_counters.times},
            "candidate": {"calls": candidate_counters.calls, "times_s": candidate_counters.times},
            "scope": counter_scope.receipt(),
        },
        "oracle": {
            "checked_ops": len(ops),
            "errors": oracle_errors,
            "all_pass": all(not errors for errors in oracle_errors.values()),
        },
        "process": _grouped_process_metadata(),
    }
    path = outdir / ("grouped_smoke.json" if args.smoke else f"grouped_n{n}.json")
    bc.dump_json(path, payload)
    print(json.dumps({
        "path": str(path),
        "n": n,
        "smoke": bool(args.smoke),
        "cold_equal": cold_equal,
        "warm_equal": all(item["all_facts_equal"] for item in warm_rounds),
        "single_equal": single_equal,
        "incompatible_equal": inc_equal_first and inc_equal_second,
        "capacity_equal": capacity_equal,
        "oracle_all_pass": payload["oracle"]["all_pass"],
        "cold_scope": cold_scope.receipt(),
        "warm_scope": warm_scope.receipt(),
    }, indent=2, sort_keys=True))



def _capacity_metadata():
    return {
        "pid": os.getpid(),
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
        "ru_maxrss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "ru_utime_s": resource.getrusage(resource.RUSAGE_SELF).ru_utime,
        "ru_stime_s": resource.getrusage(resource.RUSAGE_SELF).ru_stime,
        "argv": sys.argv,
        "env": {key: os.environ.get(key) for key in (
            "PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE", "TMPDIR",
            "RAWLSING_C11_ACCELERATOR_DIR",
        )},
        "rss_note": "ru_maxrss_bytes is whole-process Darwin high-water; phase wall/CPU only",
    }


def _run_capacity(args):
    n = args.n or 200
    outdir = Path(args.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    os.environ.pop("RAWLSING_C11_ACCELERATOR_DIR", None)
    fixture = _source_fixture(n, tag="compact-current")
    ops, catalog = _grouped_ops(fixture)
    release = _compact_release(fixture)
    by_id = {op["op_id"]: op for op in ops}
    op_a = by_id["raw_Y"]
    op_b = by_id["joint_XYZK"]

    def make_executor():
        return CarrierNeutralResearchExecutor(
            C11Repository((release,)), (release.release_ref,), catalog,
        )

    baseline_a = make_executor().execute_i03(
        query_ref=op_a["query"].ref, predicate_ref=op_a["predicate"].ref,
    ).facts[0].as_dict()
    baseline_b = make_executor().execute_i03(
        query_ref=op_b["query"].ref, predicate_ref=op_b["predicate"].ref,
    ).facts[0].as_dict()

    def run_grouped_case():
        executor = make_executor()
        scope = I03GroupedExecutionScope(max_groups=1)
        start_wall, start_cpu = time.perf_counter(), time.process_time()
        fill = executor.execute_i03(
            query_ref=op_a["query"].ref, predicate_ref=op_a["predicate"].ref,
            group_scope=scope,
        ).facts[0]
        fill_wall = time.perf_counter() - start_wall
        fill_cpu = time.process_time() - start_cpu
        start_wall, start_cpu = time.perf_counter(), time.process_time()
        hit = executor.execute_i03(
            query_ref=op_a["query"].ref, predicate_ref=op_a["predicate"].ref,
            group_scope=scope,
        ).facts[0]
        hit_wall = time.perf_counter() - start_wall
        hit_cpu = time.process_time() - start_cpu
        start_wall, start_cpu = time.perf_counter(), time.process_time()
        miss = executor.execute_i03(
            query_ref=op_b["query"].ref, predicate_ref=op_b["predicate"].ref,
            group_scope=scope,
        ).facts[0]
        miss_wall = time.perf_counter() - start_wall
        miss_cpu = time.process_time() - start_cpu
        return {
            "fill_wall_s": fill_wall,
            "fill_cpu_s": fill_cpu,
            "hit_wall_s": hit_wall,
            "hit_cpu_s": hit_cpu,
            "miss_wall_s": miss_wall,
            "miss_cpu_s": miss_cpu,
            "fill_equal": fill.as_dict() == baseline_a,
            "hit_equal": hit.as_dict() == baseline_a,
            "miss_equal": miss.as_dict() == baseline_b,
            "scope": scope.receipt(),
        }

    def run_before():
        original = I03GroupedExecutionScope._miss_capacity_exhausted
        I03GroupedExecutionScope._miss_capacity_exhausted = lambda self, cached_members: False
        try:
            return run_grouped_case()
        finally:
            I03GroupedExecutionScope._miss_capacity_exhausted = original

    def run_no_scope():
        executor = make_executor()
        executor.execute_i03(
            query_ref=op_a["query"].ref, predicate_ref=op_a["predicate"].ref,
        )
        start_wall, start_cpu = time.perf_counter(), time.process_time()
        miss = executor.execute_i03(
            query_ref=op_b["query"].ref, predicate_ref=op_b["predicate"].ref,
        ).facts[0]
        miss_wall = time.perf_counter() - start_wall
        miss_cpu = time.process_time() - start_cpu
        return {
            "miss_wall_s": miss_wall,
            "miss_cpu_s": miss_cpu,
            "miss_equal": miss.as_dict() == baseline_b,
        }

    orders = (
        ("before", "after", "no_scope"),
        ("after", "no_scope", "before"),
        ("no_scope", "before", "after"),
    )
    results = {name: [] for name in ("before", "after", "no_scope")}
    for round_index in range(1, args.rounds + 1):
        order = orders[(round_index - 1) % len(orders)]
        for name in order:
            if name == "before":
                record = run_before()
            elif name == "after":
                record = run_grouped_case()
            else:
                record = run_no_scope()
            record["round"] = round_index
            results[name].append(record)
    summary = {}
    for name, records in results.items():
        misses = [item["miss_wall_s"] for item in records]
        summary[name] = {
            "miss_wall_s": misses,
            "miss_wall_median_s": statistics.median(misses),
            "miss_cpu_median_s": statistics.median([item["miss_cpu_s"] for item in records]),
            "all_miss_equal": all(item["miss_equal"] for item in records),
            "records": records,
        }
        if name != "no_scope":
            summary[name]["fill_wall_s"] = [item["fill_wall_s"] for item in records]
            summary[name]["hit_wall_s"] = [item["hit_wall_s"] for item in records]
            summary[name]["all_fill_equal"] = all(item["fill_equal"] for item in records)
            summary[name]["all_hit_equal"] = all(item["hit_equal"] for item in records)
            summary[name]["scope_first"] = records[0]["scope"]
    payload = {
        "schema": SCHEMA,
        "mode": "capacity",
        "n": n,
        "rounds": args.rounds,
        "op_fill": op_a["op_id"],
        "op_miss": op_b["op_id"],
        "baseline_facts_equal": True,
        "summary": summary,
        "process": _capacity_metadata(),
    }
    path = outdir / f"capacity_n{n}.json"
    bc.dump_json(path, payload)
    print(json.dumps({
        "path": str(path),
        "n": n,
        "before_miss_median_s": summary["before"]["miss_wall_median_s"],
        "after_miss_median_s": summary["after"]["miss_wall_median_s"],
        "no_scope_miss_median_s": summary["no_scope"]["miss_wall_median_s"],
        "before_scope": summary["before"]["scope_first"],
        "after_scope": summary["after"]["scope_first"],
        "all_facts_equal": all(
            summary[name]["all_miss_equal"] for name in summary
        ),
    }, indent=2, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", required=True, choices=("variant", "compare", "grouped", "capacity"))
    parser.add_argument("--variant", choices=VARIANTS)
    parser.add_argument("--n", type=int, default=None)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--cache-root", default=None)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--keep-cache", action="store_true")
    parser.add_argument("--rounds", type=int, default=3)
    args = parser.parse_args()
    if args.mode == "variant":
        _run_variant(args)
    elif args.mode == "compare":
        _run_compare(args)
    elif args.mode == "grouped":
        _run_grouped(args)
    else:
        _run_capacity(args)


if __name__ == "__main__":
    main()
