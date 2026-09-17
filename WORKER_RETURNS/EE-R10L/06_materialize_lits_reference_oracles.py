#!/usr/bin/env python3
"""Mechanically freeze the nine LiTS-I reference-oracle inputs before A/B/C.

This is an EE-R10L return helper, not a production CLI.  It loads the accepted
banked projection builder with the accepted HB04 runtime objects already bound,
then records only source-local release/query identities for the frozen cells.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


SOURCE_SHA = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
PROJECTION = "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872"
C11 = "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
REPLAY = "6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd"


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load_builder(path: Path):
    # Import the exact owner modules first.  The banked builder then consumes
    # these already-loaded classes; no source/projection law is substituted.
    import rawlsing_next.pre553_c11_ingest  # noqa: F401
    import rawlsing_next.pre553_c11_integrity  # noqa: F401
    import rawlsing_next.pre553_c11_repository  # noqa: F401
    import rawlsing_next.pre553_empirical_authority  # noqa: F401
    import rawlsing_next.pre553_empirical_objects  # noqa: F401
    import rawlsing_next.pre553_empirical_query  # noqa: F401
    import rawlsing_next.pre553_physical_decoder  # noqa: F401
    import rawlsing_next.pre553_source_backed_c11_facade  # noqa: F401
    spec = importlib.util.spec_from_file_location("ee_r10l_banked_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load accepted banked AS2B builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def refs(items):
    return [item.ref.as_dict() for item in sorted(items, key=lambda item: item.ref.key)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--builder", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    from rawlsing_next.as4.loader import load_hb04_manifest
    from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
    from rawlsing_next.pre553_c11_repository import C11Repository
    from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    from rawlsing_next.pre553_empirical_query import execute_empirical_query

    builder = load_builder(Path(args.builder))
    banked_driver_root = Path(args.builder).parent.parent
    builder.PART_A_DIR = banked_driver_root / "banked_as2a"
    builder.LEDGER = builder.PART_A_DIR / "01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv"
    builder.PACKAGE = builder.PART_A_DIR / "04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json"
    source = Path(args.source)
    if builder.sha256_file(source) != SOURCE_SHA:
        raise RuntimeError("exact LiTS-I source SHA mismatch")
    package, ledger, slots = builder.read_banked_authority()
    incidence = builder.decode_dta(source, encoding="latin1")
    projection, context = builder.build_projection(incidence, package, ledger, slots)
    if projection.cache_identity != PROJECTION:
        raise RuntimeError("banked projection identity mismatch")
    selected_names = ("country", "city", "region", "q301_2", "q301_7", "tablec", "tabled")
    variables = tuple(v for v in incidence.variables if v.name in selected_names)
    selected = builder.PhysicalSourceIncidence(
        source_sha256=incidence.source_sha256,
        source_format=incidence.source_format,
        row_count=incidence.row_count,
        variables=variables,
        reader_configuration={**incidence.reader_configuration, "transport": "EE_R10L_REFERENCE_SELECTED_SLOT_STREAM"},
        file_metadata=incidence.file_metadata,
        _frame=incidence._frame[[v.name for v in variables]],
    )
    candidate = builder.project_c11_candidate_from_physical_cells(
        source_sha256=SOURCE_SHA,
        row_count=builder.ROWS,
        cells=(builder.exact_cell(cell) for cell in selected.iter_cells(batch_size=20_000)),
        projection=projection,
    )
    release = validate_c11_source_release(candidate)
    if release.semantic_release_hash != C11 or release.replay_manifest.content_hash != REPLAY:
        raise RuntimeError("accepted C11/replay identity mismatch")

    manifest = load_hb04_manifest()
    registry = AuthorityRegistry((*context["authorities"], manifest.frontier_authority_snapshot))
    repository = C11Repository((release,))
    query_by_hash = {query.content_hash: query for query in manifest.query_templates}
    query_specs = {
        "OP004": ("8a7bf5bbb1c2d8d6328dc5507416931a9c12e2c76668e0fc47af8add254c5d44", "A000"),
        "OP005": ("ef8b19744ec3c06e352f7accf75efbc216ffc454905da09948763a2c54fdc053", "A000"),
        "OP006": ("deb71e653592d8bdb246f8c4d53359e290708d3875e38433f518b307f520c6f7", "A000"),
    }
    query_oracles = {}
    for operation, (query_hash, role) in query_specs.items():
        result = execute_empirical_query(
            repository=repository,
            query=query_by_hash[query_hash],
            predicate=manifest.role_predicates[role],
            authority_registry=registry,
            release_refs=(release.release_ref,),
        )
        facts = refs(result.facts)
        query_oracles[operation] = {
            "query_ref": query_by_hash[query_hash].ref.as_dict(),
            "predicate_role": role,
            "predicate_ref": manifest.role_predicates[role].ref.as_dict(),
            "fact_refs": facts,
            "semantic_output_sha256": semantic_hash({"operation": operation, "fact_refs": facts}),
        }

    routing_refs = refs(candidate.routing_eligibility_facts_or_exact_rules)
    event_refs = refs(candidate.respondent_events)
    cell_oracles = {
        "OP001": {"kind": "SOURCE_FIDELITY_RELEASE_IDENTITY", "semantic_output_sha256": semantic_hash({"source_sha256": SOURCE_SHA, "projection_cache_identity": PROJECTION, "c11_logical_release": C11, "replay_manifest": REPLAY})},
        "OP002": {"kind": "SOURCE_NATIVE_RESPONSE_EVENT_TOPOLOGY", "semantic_output_sha256": semantic_hash({"event_refs": event_refs}), "event_ref_count": len(event_refs)},
        "OP003": {"kind": "ROUTING_RISK_DENOMINATOR_IDENTITY", "semantic_output_sha256": semantic_hash({"routing_refs": routing_refs}), "routing_ref_count": len(routing_refs), "r2_root": "f224533ce0a705bf0839e6bb40bd49dec0c8366e5a5ede0a389e3e67811a13b3", "r7_root": "0978bd4d87afd88831593ca5977fa9978948d598bf981adfd7fd96ceab979844", "r27_root": "f9c87f610bcaf0539cc91e7f2608b230cea39d806d3611d6a398519a86386d29"},
        **query_oracles,
        "OP020": {"kind": "PINNED_R3E_LIFECYCLE_PROFILE", "authority_commit": "dd218b1182b29259a19837c89222cbc47024b2ec", "blob": "9e3cc4ab92e4a72fe509691393f4ec5721ddc165"},
        "OP021": {"kind": "PINNED_R3E_LIFECYCLE_PROFILE", "authority_commit": "dd218b1182b29259a19837c89222cbc47024b2ec", "blob": "64a4a43bf8787f0ea2b849cdab346a3e968349af"},
        "OP022": {"kind": "PINNED_R3E_LIFECYCLE_PROFILE", "authority_commit": "dd218b1182b29259a19837c89222cbc47024b2ec", "blob": "10fa0c9980267112cd88a094a6b6eb80e40aa831"},
    }
    result = {
        "schema": "RAWLSING_EE_R10L_LITS_REFERENCE_ORACLE_FREEZE@1.0.0",
        "status": "PASS__CANDIDATE_NEUTRAL_REFERENCE_ORACLES_MATERIALIZED_BEFORE_A",
        "candidate_execution_order": ["A", "B", "C"],
        "candidate_invocations_before_freeze": 0,
        "source_sha256": SOURCE_SHA,
        "projection_cache_identity": PROJECTION,
        "c11_logical_release": C11,
        "as2b_replay_manifest": REPLAY,
        "reference_runtime": {"pyreadstat": "1.3.6", "pyarrow": "25.0.1", "decoder": "decode_dta(source_path, encoding=latin1)"},
        "cells": cell_oracles,
        "frozen_w4_telemetry_fields": ["wall_ns", "cpu_user_ns", "cpu_system_ns", "peak_rss_bytes", "scratch_bytes_before", "scratch_bytes_after", "peak_scratch_bytes_observed", "peak_scratch_file_count_observed", "max_single_temp_object_bytes_observed", "durable_bytes_before", "durable_bytes_after", "durable_bytes_created_delta", "source_open_count", "source_decode_count", "bytes_read", "bytes_written", "temporary_spill_bytes_reported", "cache_index_bytes_created", "rewritten_bytes", "semantic_oracle_status", "identity_oracle_status"],
        "no_rank_or_policy_decision": True,
    }
    Path(args.out).write_bytes(canonical(result))
    print(json.dumps({"out": args.out, "status": result["status"], "cells": list(cell_oracles)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
