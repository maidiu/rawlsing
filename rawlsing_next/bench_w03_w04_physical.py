#!/usr/bin/env python3
"""Sourcefree W03/W04 physical-economy benchmark.

This is a benchmark harness over the existing selected physical-cell, governed
projection, I02/C11 seal, compact view, Parquet carrier and real I03/I05
consumers.  It does not add a statistical engine, source meaning, or a second
C11 store.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
import os
import platform
import resource
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable, Mapping

# The source root is imported from PYTHONPATH by the parent/child launcher.  A
# baseline run can invoke this same file with the baseline root on PYTHONPATH.
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor, RuntimeObjectCatalog
from rawlsing_next.tests.test_pre553_discovery_exact import _atom, _d_auth, _discovery_authority, _grammar, _qt, _rule
from rawlsing_next.tests.test_pre553_empirical_query import _branch_predicate, _predicate, _query, _response_leaf
from rawlsing_next.pre553_empirical_objects import ExactRef, RespondentEvent, RoutingEligibilityFact, canonical_json, semantic_hash
from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
    build_source_backed_c11_repository,
    source_backed_facade_key,
)
from rawlsing_next.tests.test_pre553_route_b_production import _fixture

SCHEMA = "PYAT_W03_W04_PHYSICAL_BENCH@1"
MAX_CHILD_BYTES = 6 * 1024 * 1024 * 1024
PROFILES = ("narrow", "wide", "repeat")
SCENARIOS = ("cold", "cells-and-hash", "full-matrix")


def _sha(value: Any) -> str:
    return semantic_hash(value)


def _rss_peak_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    # macOS reports bytes; Linux reports KiB.  The benchmark is expected on the
    # declared macOS host, but normalise the common Linux form too.
    return value if sys.platform == "darwin" else value * 1024


def _cpu_seconds() -> tuple[float, float]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return float(usage.ru_utime), float(usage.ru_stime)


def _files_and_bytes(root: Path) -> tuple[int, int]:
    count = 0
    size = 0
    if root.exists():
        for path in root.rglob("*"):
            if path.is_file():
                count += 1
                try:
                    size += path.stat().st_size
                except OSError:
                    pass
    return count, size


def _stage(name: str, fn):
    before_rss = _rss_peak_bytes()
    before_user, before_sys = _cpu_seconds()
    started = time.perf_counter()
    value = fn()
    wall = time.perf_counter() - started
    user, system = _cpu_seconds()
    return value, {
        "stage": name,
        "wall_seconds": wall,
        "cpu_user_seconds": user - before_user,
        "cpu_system_seconds": system - before_sys,
        "rss_peak_bytes": _rss_peak_bytes(),
        "rss_peak_delta_bytes": max(0, _rss_peak_bytes() - before_rss),
    }


def _counting_cells(rows: int, names: tuple[str, ...], ordinals: Mapping[str, int]):
    stats = {"count": 0, "generation_seconds": 0.0}
    started = time.perf_counter()

    def values(name: str, row: int):
        if name in {"X", "Y"}:
            return str(row % 2)
        if name == "O":
            return "AB" if row % 2 == 0 else "BA"
        if name == "R":
            return "XY" if row % 2 == 0 else "XZ"
        if name == "G":
            return "A" if row % 2 == 0 else "B"
        if name == "W":
            return 1 + (row % 3)
        raise ValueError(f"unknown benchmark variable {name}")

    def factory():
        for row in range(1, rows + 1):
            for name in names:
                started_cell = time.perf_counter()
                yield PhysicalCell(
                    row_ordinal=row,
                    variable_ordinal=ordinals[name],
                    variable_name=name,
                    raw_value=values(name, row),
                    missing_state=PhysicalMissingState.OBSERVED_STORAGE_VALUE,
                    source_missing_declaration=None,
                )
                stats["count"] += 1
                stats["generation_seconds"] += time.perf_counter() - started_cell

    return factory, stats


def _profile(name: str, rows: int) -> dict[str, Any]:
    if name not in PROFILES:
        raise ValueError(f"unknown profile {name!r}")
    if rows < 1:
        raise ValueError("rows must be positive")
    base = _fixture()
    projection = base["projection"]
    qrefs = base["qrefs"]
    base_routing: dict[str, Any] = {}
    for fact in projection.routing:
        key = dict(fact.question_or_target_ref)["object_id"]
        if key not in base_routing and fact.typed_state == "ELIGIBLE_APPLICABLE":
            base_routing[key] = fact
    for fact in projection.routing:
        key = dict(fact.question_or_target_ref)["object_id"]
        base_routing.setdefault(key, fact)
    base_questions = {
        binding.native_question_ref.key: binding for binding in projection.questions
    }
    base_response_slots = {
        rule.slot.name: rule for rule in projection.response_slots
    }
    base_coordinate_slots = tuple(projection.coordinate_slots)
    base_weight_slots = tuple(projection.weight_slots)
    source_sha = _sha({"schema": SCHEMA, "profile": name, "rows": rows, "fixture": "m01-sourcefree"})
    response_names = ("X", "Y") if name == "narrow" else ("X", "Y", "O", "R")
    names = response_names + ("G",) + (("W",) if name != "narrow" else ())
    ordinals = {"X": 1, "Y": 2, "O": 3, "R": 4, "G": 5, "W": 6}

    template_respondent = projection.respondents[0]
    respondents = tuple(
        replace(
            template_respondent,
            respondent_key=f"B{i:06d}",
            source_native_respondent_key_ref_or_typed_absence=ExactRef(
                "SOURCE_RESPONDENT",
                f"urn:bench:{name}:respondent:{i:06d}",
                _sha({"profile": name, "row": i, "kind": "respondent"}),
            ),
        )
        for i in range(1, rows + 1)
    )
    row_bindings = tuple(
        replace(projection.row_bindings[0], row_ordinal=i, respondent_ref=respondent.ref)
        for i, respondent in enumerate(respondents, 1)
    )
    routing = []
    for i, respondent in enumerate(respondents, 1):
        for qname in response_names:
            template = base_routing[qrefs[qname].object_id]
            template_data = template.as_dict()
            semantic_fields = dict(template_data["semantic_fields"])
            semantic_fields.update(
                scoped_respondent_ref=respondent.ref.as_dict(),
                routing_rule_ref=ExactRef(
                    "ROUTING_RULE",
                    f"urn:bench:{name}:rule:{i:06d}:{qname}",
                    _sha({"profile": name, "row": i, "question": qname, "rule": 1}),
                ).as_dict(),
                member_set_replay_ref=ExactRef(
                    "MEMBER_SET",
                    f"urn:bench:{name}:member:{i:06d}:{qname}",
                    _sha({"profile": name, "row": i, "question": qname, "member": 1}),
                ).as_dict(),
            )
            routing.append(
                RoutingEligibilityFact(
                    typed_state=template_data["typed_state"],
                    authority_snapshot_refs=template_data["authority_snapshot_refs"],
                    dependency_refs=template_data["dependency_refs"],
                    producer_replay_locator_or_reference_root=ExactRef(
                        "REPLAY_ROOT",
                        f"urn:bench:{name}:routing:{i:06d}:{qname}",
                        _sha({"profile": name, "row": i, "question": qname}),
                    ).as_dict(),
                    **semantic_fields,
                )
            )
    questions = tuple(
        base_questions[qrefs[qname].key] for qname in response_names
    )
    response_slots = tuple(base_response_slots[qname] for qname in response_names)
    weight_slots = base_weight_slots if name != "narrow" else ()
    projection = replace(
        projection,
        expected_source_sha256=source_sha,
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT",
            f"urn:bench:{name}:snapshot",
            source_sha,
        ),
        respondents=respondents,
        row_bindings=row_bindings,
        questions=questions,
        response_slots=response_slots,
        coordinate_slots=base_coordinate_slots,
        routing=tuple(routing),
        weight_slots=weight_slots,
    )
    factory, stats = _counting_cells(rows, names, ordinals)
    stream = ExactPhysicalCellStream(
        source_sha256=source_sha,
        row_count=rows,
        cell_iter_factory=factory,
        transport_identity="PYAT_W03_W04_SOURCEFREE_EXACT_PHYSICAL_CELL_STREAM",
    )
    source_auth = next(a for a in base["catalog"].authorities if a.authority_id.endswith("-source"))
    source_stub = {
        "universe": projection.universes[0],
        "respondents": {respondent.respondent_key: respondent for respondent in respondents},
        "qrefs": qrefs,
        "risk_refs": {"R": base["risk"]},
        "source_auth": source_auth,
        "authorities": base["catalog"].authorities,
    }
    qauth = base["qauth"]
    dauth = base["dauth"]
    all_p = _branch_predicate(source_stub, qauth, tag=f"bench-{name}-all")
    x1 = _predicate(
        source_stub,
        qauth,
        _response_leaf(source_stub, qauth, "X", 1),
        tag=f"bench-{name}-x1",
    )
    empty = _branch_predicate(source_stub, qauth, members=(), tag=f"bench-{name}-empty")
    raw_query = _query(source_stub, qauth, all_p, ("Y",), measure="RAW", tag=f"bench-{name}-raw-y")
    weighted_query = _query(
        source_stub, qauth, all_p, ("Y",), measure="GOVERNED_WEIGHTED",
        tag=f"bench-{name}-weighted-y",
    )
    grammar = _grammar(
        operation="I03-OP-m01-discovery",
        atoms=[
            _atom("ALL", all_p, "BRANCH"),
            _atom("X1", x1, "RESPONSE"),
        ],
        templates=[_qt("Y", raw_query)],
        rules=[_rule(
            f"bench-{name}-rule",
            "PAIR_RESPONSE_COTRAVEL",
            "SINGLE_ATOM",
            atom_ids=("X1",),
            baseline_atom_id="ALL",
            query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
    )
    discovery_authority = _discovery_authority(
        source_stub, grammar, dauth, tag=f"bench-{name}-discovery"
    )
    catalog = RuntimeObjectCatalog(
        authorities=base["catalog"].authorities,
        predicates=(all_p, x1, empty),
        queries=(raw_query, weighted_query),
        discovery_authorities=(discovery_authority,),
    )
    from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
    requests = (
        (I03ExecutionRequest(raw_query.ref, all_p.ref),)
        if name == "narrow"
        else (
            I03ExecutionRequest(raw_query.ref, all_p.ref),
            I03ExecutionRequest(weighted_query.ref, all_p.ref),
        )
    )
    return {
        "profile": name,
        "rows": rows,
        "source_sha256": source_sha,
        "stream": stream,
        "projection": projection,
        "catalog": catalog,
        "requests": requests,
        "discovery_authority": discovery_authority,
        "repeat_count": 3 if name == "repeat" else 1,
        "cell_stats": stats,
        "names": names,
    }


POLICY_ENV = "RAWLSING_C11_ACCELERATOR_POLICY"
LEGACY_ENV = "RAWLSING_C11_ACCELERATOR_DIR"
DERIVED_CACHE_GLOB = "c11-events-*.parquet"


def _derived_state(root: Path) -> dict[str, Any]:
    files = sorted(root.glob(DERIVED_CACHE_GLOB)) if root.exists() else []
    entries = []
    for path in files:
        try:
            info = path.stat()
            entries.append({
                "name": path.name,
                "size": info.st_size,
                "mtime_ns": info.st_mtime_ns,
            })
        except OSError:
            continue
    envelope = None
    if files:
        try:
            import pyarrow.parquet as pq
            metadata = pq.read_schema(files[0]).metadata or {}
            raw = metadata.get(b"rawlsing.c11.event_accelerator.envelope")
            if raw:
                envelope = json.loads(raw.decode("utf-8"))
        except Exception:
            envelope = None
    return {"root": str(root), "files": entries, "envelope": envelope}


def _ensure_policy(base_root: Path) -> tuple[Path, Path]:
    base_root.mkdir(parents=True, exist_ok=True)
    derived = base_root / "derived-accelerator"
    derived.mkdir(mode=0o700, exist_ok=True)
    derived.chmod(0o700)
    policy_path = base_root / "accelerator-policy.json"
    policy = {
        "schema": "PYAT_C11_ACCELERATOR_POLICY@1",
        "enabled": True,
        "root": str(derived.resolve()),
        "source_permission": "NONRESPONDENT_SOURCEFREE",
        "authorization_id": "sourcefree-w03-w04-benchmark",
        "retention_budget": {
            "max_bytes": 268_435_456,
            "max_files": 4,
            "max_age_seconds": 86_400,
        },
    }
    policy_path.write_text(json.dumps(policy, sort_keys=True) + "\n", encoding="utf-8")
    policy_path.chmod(0o600)
    os.environ[POLICY_ENV] = str(policy_path.resolve())
    os.environ.pop(LEGACY_ENV, None)
    return derived, policy_path


def _event_count(release: Any) -> int:
    public = release.public_objects
    lane = getattr(public, "lane", None)
    selectors = getattr(lane, "selectors", None)
    if selectors is not None:
        return len(selectors)
    return sum(1 for obj in public if isinstance(obj, RespondentEvent))


def _build_release(
    profile: Mapping[str, Any], *, root: Path | None, stages: dict[str, Any]
) -> tuple[Any, dict[str, Any]]:
    stream = profile["stream"]
    projection = profile["projection"]
    catalog = profile["catalog"]
    derived = None
    before = {"root": "", "files": [], "envelope": None}
    policy_started = time.perf_counter()
    if root is not None:
        derived, policy_path = _ensure_policy(root)
        before = _derived_state(derived)
    else:
        policy_path = None
    method_overhead = time.perf_counter() - policy_started
    stages["policy_setup"] = {
        "stage": "policy_setup",
        "wall_seconds": method_overhead,
        "status": "ACTUAL_GOVERNED_POLICY_FILE_AND_DERIVED_ROOT_SETUP" if policy_path else "NO_DERIVED_ROOT",
    }

    # The actual normal caller path: current exact physical stream + governed
    # projection -> streaming cold C11 -> I02 validation/seal -> governed
    # compact cache attachment.  It is kept as one honest combined boundary;
    # the current public facade exposes no separable I02 sub-stage.
    (repository, release), normal_stage = _stage(
        "normal_current_cold_build",
        lambda: build_source_backed_c11_repository(
            stream,
            projection,
            current_authorities=catalog.authorities,
        ),
    )
    stages[normal_stage["stage"]] = normal_stage
    stages["cells"] = {
        "stage": "cells",
        "wall_seconds": profile["cell_stats"]["generation_seconds"],
        "rss_peak_bytes": _rss_peak_bytes(),
        "cell_count": profile["cell_stats"]["count"],
        "status": "OBSERVED_LAZY_CELL_ITERATION__PEAK_INCLUDED_IN_NORMAL_COLD_BUILD",
    }
    stages["decode"] = {
        "stage": "decode",
        "status": "NOT_APPLICABLE__EXACT_PHYSICAL_CELL_STREAM__NO_SOURCE_DECODE",
        "wall_seconds": 0.0,
    }
    stages["cold_combined"] = {
        **normal_stage,
        "stage": "cold_combined",
        "status": "STREAMING_CELLS__OBJECT_CONSTRUCTION__CANONICAL_HASH__I02_VALIDATION_SEAL__GOVERNED_CACHE_ATTACH__COMBINED_PUBLIC_PATH",
    }
    for alias in ("projection", "objectconstruction", "canonicalhash", "i02validation", "seal", "compact"):
        stages[alias] = {
            "stage": alias,
            "status": "COMBINED_INSIDE_NORMAL_CURRENT_COLD_BUILD__NO_PUBLIC_SEPARABLE_BOUNDARY",
            "wall_seconds": None,
            "rss_peak_bytes": normal_stage["rss_peak_bytes"],
        }
    after = _derived_state(derived) if derived is not None else {"root": "", "files": [], "envelope": None}
    before_keys = {(x["name"], x["size"], x["mtime_ns"]) for x in before["files"]}
    after_keys = {(x["name"], x["size"], x["mtime_ns"]) for x in after["files"]}
    derived_hit = bool(before["files"]) and before_keys == after_keys
    derived_write = bool(after["files"]) and before_keys != after_keys
    derived_status = (
        "HIT_EXACT_ENVELOPE_AND_MTIME" if derived_hit
        else "MISS_WRITE_NEW_OR_REPLACED" if derived_write
        else "NO_GOVERNED_DERIVED_CACHE_WRITE"
    )
    stages["derived_cache"] = {
        "stage": "derived_cache",
        "status": derived_status,
        "before": before,
        "after": after,
        "derived_cache_hit": derived_hit,
        "derived_cache_write": derived_write,
        "derived_cache_miss": bool(after["files"]) and not before["files"],
        "policy_path": str(policy_path) if policy_path else None,
    }
    return release, {
        "repository": repository,
        "projection_identity": source_backed_facade_key(stream, projection).projection_identity,
        "derived_cache": stages["derived_cache"],
        "event_count": _event_count(release),
        "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
        "method_overhead_seconds": method_overhead,
        "cold_combined_wall_seconds": normal_stage["wall_seconds"],
        "cold_combined_rss_peak_bytes": normal_stage["rss_peak_bytes"],
    }


def _consumer(profile: Mapping[str, Any], release: Any, *, stages: dict[str, Any]) -> dict[str, Any]:
    catalog = profile["catalog"]
    repository = C11Repository((release,))
    executor = CarrierNeutralResearchExecutor(repository, (release.release_ref,), catalog)
    def run():
        i03 = []
        for request in profile["requests"]:
            result = executor.execute_i03(
                query_ref=request.query_ref,
                predicate_ref=request.predicate_ref,
            )
            i03.append(
                {
                    "facts": [fact.as_dict() for fact in result.facts],
                    "fact_states": [fact.typed_state for fact in result.facts],
                }
            )
        i05 = executor.execute_i05(discovery_authority_ref=profile["discovery_authority"].ref)
        return {
            "i03": i03,
            "i05_receipt_refs": [receipt.ref.as_dict() for receipt in i05.receipts],
            "i05_fact_refs": [fact.ref.as_dict() for fact in i05.empirical_facts],
            "i05_candidate_count": i05.candidate_count,
            "i05_coverage": i05.coverage_claim,
        }
    value, stage = _stage("firstconsumer", run)
    stages["firstconsumer"] = stage
    value["consumer_fingerprint"] = hashlib.sha256(
        canonical_json(value).encode("utf-8")
    ).hexdigest()
    for _ in range(max(0, int(profile["repeat_count"]) - 1)):
        repeated, repeat_stage = _stage("repeat_firstconsumer", run)
        repeated["consumer_fingerprint"] = hashlib.sha256(
            canonical_json(repeated).encode("utf-8")
        ).hexdigest()
        value = repeated
        stages.setdefault("repeat_firstconsumer", []).append(repeat_stage)
    return value


def _cache_stats(root: Path) -> tuple[int, int]:
    return _files_and_bytes(root)


def _worker(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.worker_root) if args.worker_root else None
    worker_started = time.perf_counter()
    profile, profile_stage = _stage(
        "profile_setup", lambda: _profile(args.worker_profile, args.worker_rows)
    )
    stages: dict[str, Any] = {"profile_setup": profile_stage}
    output: dict[str, Any] = {
        "schema": SCHEMA,
        "scenario": args.worker_scenario,
        "profile": args.worker_profile,
        "rows": args.worker_rows,
        "pid": os.getpid(),
        "host": platform.node(),
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cap_bytes": MAX_CHILD_BYTES,
        "cap_enforced": False,
        "stages": stages,
    }
    if sys.platform != "win32":
        try:
            resource.setrlimit(resource.RLIMIT_AS, (MAX_CHILD_BYTES, MAX_CHILD_BYTES))
            output["cap_enforced"] = True
        except (ValueError, OSError):
            output["cap_enforced"] = False

    base_root = Path(args.worker_root) if args.worker_root else None
    canonical_root = base_root / "canonical-carrier" if base_root is not None else None
    selector_path = base_root / "selector.json" if base_root is not None else None
    if args.worker_scenario in {"warm", "reopen"}:
        if base_root is None or canonical_root is None or selector_path is None:
            raise ValueError("warm/reopen requires persisted roots")
        if not selector_path.is_file():
            raise FileNotFoundError("persisted selector.json is missing")

    release, release_meta = _build_release(profile, root=base_root, stages=stages)
    output["source_sha256"] = profile["source_sha256"]
    output["release_id"] = release.release_id
    output["release_ref"] = release.release_ref.as_dict()
    output["release_manifest_hash"] = release.source_release_manifest_hash
    output["semantic_release_hash"] = release.semantic_release_hash
    output["projection_identity"] = release_meta.get("projection_identity")
    output["cell_count"] = profile["cell_stats"]["count"]
    output["cell_generation_seconds"] = profile["cell_stats"]["generation_seconds"]
    output["event_count"] = release_meta["event_count"]
    output["replay_manifest_ref"] = release_meta.get("replay_manifest_ref")
    output["method_overhead_seconds"] = release_meta.get("method_overhead_seconds")
    output["rows"] = profile["rows"]
    output["derived_cache"] = release_meta["derived_cache"]
    output["normal_current_cold_build"] = True
    output["cold_combined_wall_seconds"] = release_meta["cold_combined_wall_seconds"]
    output["cold_combined_rss_peak_bytes"] = release_meta["cold_combined_rss_peak_bytes"]

    consumer = _consumer(profile, release, stages=stages)
    output["consumer"] = consumer
    output["consumer_fact_count"] = sum(len(item["facts"]) for item in consumer["i03"])
    output["consumer_fact_states"] = [
        state for item in consumer["i03"] for state in item["fact_states"]
    ]
    output["consumer_fingerprint"] = consumer["consumer_fingerprint"]
    output["i05_receipt_count"] = len(consumer["i05_receipt_refs"])
    output["i05_fact_count"] = len(consumer["i05_fact_refs"])

    if args.worker_scenario in {"full-matrix", "cold"} and base_root is not None:
        derived_root = base_root / "derived-accelerator"
        derived_files, derived_bytes = _cache_stats(derived_root)
        output["derived_cache_files"], output["derived_cache_bytes"] = derived_files, derived_bytes
        output["derived_cache_hit"] = bool(release_meta["derived_cache"]["derived_cache_hit"])
        output["derived_cache_write"] = bool(release_meta["derived_cache"]["derived_cache_write"])
        output["derived_cache_miss"] = bool(release_meta["derived_cache"]["derived_cache_miss"])
        output["derived_cache_envelope"] = release_meta["derived_cache"]["after"]["envelope"]
        if args.worker_scenario == "full-matrix":
            carrier = ParquetC11Carrier(canonical_root)
            directory, persist_stage = _stage("canonical_persist", lambda: carrier.persist(release))
            stages["canonical_persist"] = persist_stage
            output["canonical_persist_directory"] = str(directory)
            output["canonical_files"], output["canonical_bytes"] = _cache_stats(canonical_root)
            output["canonical_reopen_hit"] = False
            selector_path.write_text(json.dumps({
                "source_sha256": release.source_artifact_ref.content_hash,
                "release_id": release.release_id,
                "semantic_release_hash": release.semantic_release_hash,
                "projection_identity": release_meta.get("projection_identity"),
            }, sort_keys=True) + "\n", encoding="utf-8")
    elif args.worker_scenario in {"warm", "reopen"}:
        selector = json.loads(selector_path.read_text(encoding="utf-8"))
        carrier = ParquetC11Carrier(canonical_root)
        reopened, reopen_stage = _stage(
            "canonical_reopen",
            lambda: carrier.reopen(
                selector["source_sha256"],
                selector["release_id"],
                selector["semantic_release_hash"],
            ),
        )
        stages["canonical_reopen"] = reopen_stage
        output["canonical_reopen_hit"] = True
        output["canonical_reopened_release_ref"] = reopened.release_ref.as_dict()
        canonical_consumer = _consumer(profile, reopened, stages={"canonical_firstconsumer": {}})
        output["canonical_consumer_fingerprint"] = canonical_consumer["consumer_fingerprint"]
        output["canonical_consumer_fact_states"] = [
            state for item in canonical_consumer["i03"] for state in item["fact_states"]
        ]
        output["canonical_files"], output["canonical_bytes"] = _cache_stats(canonical_root)
        derived_root = base_root / "derived-accelerator"
        output["derived_cache_files"], output["derived_cache_bytes"] = _cache_stats(derived_root)
        output["derived_cache_hit"] = bool(release_meta["derived_cache"]["derived_cache_hit"])
        output["derived_cache_write"] = bool(release_meta["derived_cache"]["derived_cache_write"])
        output["derived_cache_miss"] = bool(release_meta["derived_cache"]["derived_cache_miss"])
        output["derived_cache_envelope"] = release_meta["derived_cache"]["after"]["envelope"]
        output["cache_fingerprint_parity"] = (
            output.get("consumer_fingerprint") == canonical_consumer["consumer_fingerprint"]
        )

    user, system = _cpu_seconds()
    output["metrics"] = {
        "wall_seconds": time.perf_counter() - worker_started,
        "cpu_user_seconds": user,
        "cpu_system_seconds": system,
        "rss_peak_bytes": _rss_peak_bytes(),
        "source_opens": 0,
        "cache_write_amortization": (
            float(stages["canonical_persist"]["wall_seconds"]) / max(1, int(profile["repeat_count"]))
            if isinstance(stages.get("canonical_persist"), Mapping) else None
        ),
    }
    return output


def _run_child(args: argparse.Namespace, *, source_root: Path) -> dict[str, Any]:
    payload_path = Path(args.worker_json)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(source_root) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker",
        "--worker-scenario", args.worker_scenario,
        "--worker-profile", args.worker_profile,
        "--worker-rows", str(args.worker_rows),
        "--worker-root", args.worker_root or "",
        "--worker-json", str(payload_path),
    ]
    started = time.perf_counter()
    proc = subprocess.run(cmd, cwd=str(source_root), env=env, capture_output=True, text=True)
    wall = time.perf_counter() - started
    if proc.returncode != 0:
        return {
            "schema": SCHEMA,
            "status": "BLOCKED_EXACT_DEPENDENCY",
            "scenario": args.worker_scenario,
            "profile": args.worker_profile,
            "rows": args.worker_rows,
            "returncode": proc.returncode,
            "wall_seconds": wall,
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-4000:],
        }
    try:
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "schema": SCHEMA,
            "status": "BLOCKED_EXACT_DEPENDENCY",
            "detail": f"child JSON unreadable: {exc}",
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-4000:],
        }
    payload["parent_wall_seconds"] = wall
    return payload


def _median(values: Iterable[float]) -> float | None:
    values = [x for x in values if x is not None]
    return statistics.median(values) if values else None


def _aggregate(runs: list[dict[str, Any]]) -> dict[str, Any]:
    complete = [r for r in runs if r.get("status") != "BLOCKED_EXACT_DEPENDENCY"]
    return {
        "runs": len(runs),
        "complete_runs": len(complete),
        "blocked_runs": len(runs) - len(complete),
        "median_wall_seconds": _median(
            float(r.get("metrics", {}).get("wall_seconds", 0.0)) for r in complete
        ),
        "median_rss_peak_bytes": _median(
            float(r.get("metrics", {}).get("rss_peak_bytes", 0.0)) for r in complete
        ),
        "median_cpu_user_seconds": _median(
            float(r.get("metrics", {}).get("cpu_user_seconds", 0.0)) for r in complete
        ),
        "median_cpu_system_seconds": _median(
            float(r.get("metrics", {}).get("cpu_system_seconds", 0.0)) for r in complete
        ),
        "min_wall_seconds": min((float(r.get("metrics", {}).get("wall_seconds", 0.0)) for r in complete), default=None),
        "max_wall_seconds": max((float(r.get("metrics", {}).get("wall_seconds", 0.0)) for r in complete), default=None),
        "min_rss_peak_bytes": min((int(r.get("metrics", {}).get("rss_peak_bytes", 0)) for r in complete), default=None),
        "max_rss_peak_bytes": max((int(r.get("metrics", {}).get("rss_peak_bytes", 0)) for r in complete), default=None),
    }


def _compare(old: Any, new: Any) -> dict[str, Any]:
    if not isinstance(old, Mapping):
        return {"status": "NO_BASELINE"}
    out: dict[str, Any] = {}
    for key in ("median_wall_seconds", "median_rss_peak_bytes"):
        a = old.get(key)
        b = new.get(key) if isinstance(new, Mapping) else None
        out[key] = {
            "baseline": a,
            "candidate": b,
            "ratio": (b / a) if isinstance(a, (int, float)) and isinstance(b, (int, float)) and a else None,
        }
    out["status"] = "OBSERVED" if out["median_wall_seconds"]["baseline"] is not None else "NO_BASELINE"
    return out


def _run_scenario(args: argparse.Namespace, scenario: str, profile: str, baseline: Any) -> dict[str, Any]:
    root = Path(args.root) / profile if args.root else Path(tempfile.mkdtemp(prefix=f"pyat-w03-w04-{profile}-"))
    cold_runs: list[dict[str, Any]] = []
    warm_runs: list[dict[str, Any]] = []
    rebuild_runs: list[dict[str, Any]] = []
    for repetition in range(args.repetitions):
        cold_root = root / f"cold-{repetition}"
        if cold_root.exists():
            shutil.rmtree(cold_root)
        cold_runs.append(_run_child(argparse.Namespace(
            worker_scenario=scenario if scenario in {"cold", "cells-and-hash"} else "full-matrix",
            worker_profile=profile,
            worker_rows=args.rows,
            worker_root=str(cold_root),
            worker_json=str(root / f"cold-{repetition}.json"),
        ), source_root=args.source_root))
        if scenario == "full-matrix":
            warm_runs.append(_run_child(argparse.Namespace(
                worker_scenario="warm",
                worker_profile=profile,
                worker_rows=args.rows,
                worker_root=str(cold_root),
                worker_json=str(root / f"warm-{repetition}.json"),
            ), source_root=args.source_root))
            if cold_root.exists():
                shutil.rmtree(cold_root)
            rebuild_runs.append(_run_child(argparse.Namespace(
                worker_scenario="full-matrix",
                worker_profile=profile,
                worker_rows=args.rows,
                worker_root=str(cold_root),
                worker_json=str(root / f"rebuild-{repetition}.json"),
            ), source_root=args.source_root))
    cold_aggregate = _aggregate(cold_runs)
    warm_aggregate = _aggregate(warm_runs)
    rebuild_aggregate = _aggregate(rebuild_runs)
    baseline_for = ((baseline or {}).get("results", {}) if isinstance(baseline, Mapping) else {}).get(scenario, {}).get(profile) if isinstance(baseline, Mapping) else None
    result = {
        "profile": profile,
        "scenario": scenario,
        "rows": args.rows,
        "repetitions": args.repetitions,
        "cold": {"aggregate": cold_aggregate, "runs": cold_runs},
        "warm": {"aggregate": warm_aggregate, "runs": warm_runs} if warm_runs else None,
        "delete_rebuild": {"aggregate": rebuild_aggregate, "runs": rebuild_runs} if rebuild_runs else None,
        "actual_event_counts": {
            "cold": [r.get("event_count") for r in cold_runs],
            "warm": [r.get("event_count") for r in warm_runs],
            "delete_rebuild": [r.get("event_count") for r in rebuild_runs],
        },
        "cold_vs_baseline": _compare((baseline_for or {}).get("cold", {}).get("aggregate") if isinstance(baseline_for, Mapping) else None, cold_aggregate),
        "warm_vs_baseline": _compare((baseline_for or {}).get("warm", {}).get("aggregate") if isinstance(baseline_for, Mapping) else None, warm_aggregate),
        "regressions": [],
    }
    for label, current, old in (("cold", cold_aggregate, (baseline_for or {}).get("cold", {}).get("aggregate") if isinstance(baseline_for, Mapping) else None), ("warm", warm_aggregate, (baseline_for or {}).get("warm", {}).get("aggregate") if isinstance(baseline_for, Mapping) else None)):
        if isinstance(old, Mapping) and old.get("median_wall_seconds") and current.get("median_wall_seconds"):
            ratio = current["median_wall_seconds"] / old["median_wall_seconds"]
            if ratio > 1.10:
                result["regressions"].append({"scope": label, "metric": "median_wall_seconds", "ratio": ratio, "status": "REGRESSION_GT_10_PERCENT"})
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", default="cold", help="cold,cells-and-hash,full-matrix (comma separated)")
    parser.add_argument("--profiles", default="narrow,wide,repeat")
    parser.add_argument("--rows", type=int, default=100000)
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--jsonpath", "--json", dest="jsonpath", default=None)
    parser.add_argument("--root", default=None)
    parser.add_argument("--baseline-json", default=None)
    parser.add_argument("--source-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--worker-scenario", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--worker-profile", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--worker-rows", type=int, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--worker-root", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--worker-json", default=None, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.worker:
        payload = _worker(args)
        Path(args.worker_json).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return 0
    scenarios = [part.strip() for part in args.scenario.split(",") if part.strip()]
    profiles = [part.strip() for part in args.profiles.split(",") if part.strip()]
    if any(s not in SCENARIOS for s in scenarios):
        parser.error(f"scenario must be one of {SCENARIOS}")
    if any(p not in PROFILES for p in profiles):
        parser.error(f"profile must be one of {PROFILES}")
    if args.rows < 1 or args.repetitions < 1:
        parser.error("rows and repetitions must be positive")
    args.source_root = Path(args.source_root).resolve()
    baseline = None
    if args.baseline_json:
        baseline = json.loads(Path(args.baseline_json).read_text(encoding="utf-8"))
    results = {}
    for scenario in scenarios:
        results[scenario] = {}
        for profile in profiles:
            results[scenario][profile] = _run_scenario(args, scenario, profile, baseline)
    final_eligible = (
        "full-matrix" in scenarios
        and args.rows >= 100000
        and args.repetitions >= 3
        and set(profiles) == set(PROFILES)
    )
    output = {
        "schema": SCHEMA,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "final_matrix_eligible": final_eligible,
        "final_matrix_requirements": {
            "scenario": "full-matrix",
            "profiles": list(PROFILES),
            "rows_min": 100000,
            "repetitions_min": 3,
            "actual_events_reported": True,
        },
        "acceptance_status": "ELIGIBLE_FOR_FINAL_MATRIX_NOT_YET_RECEIVED" if final_eligible else "NON_FINAL_DIAGNOSTIC__DO_NOT_REPORT_AS_FULL_MATRIX_PASS",
        "host": {
            "node": platform.node(),
            "platform": platform.platform(),
            "python": sys.version,
            "load_average": list(os.getloadavg()),
            "cap_bytes": MAX_CHILD_BYTES,
        },
        "model": "opencode-go/deepseek-v4.1-flash#max",
        "scenarios": scenarios,
        "profiles": profiles,
        "rows": args.rows,
        "repetitions": args.repetitions,
        "results": results,
        "limits": [
            "Sourcefree S2 benchmark only; not original35/native/science/actor evidence.",
            "One child at a time; child cap is 6 GiB; no downsizing is used for a claimed PASS.",
            "Cold-warm-delete-rebuild use fresh child processes.",
            "ExactPhysicalCellStream has no source decode; decode stage is explicitly not applicable.",
            "Object construction and canonical closure hashing share the public candidate boundary; stages are labelled combined rather than falsely split.",
        ],
    }
    text = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.jsonpath:
        path = Path(args.jsonpath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
