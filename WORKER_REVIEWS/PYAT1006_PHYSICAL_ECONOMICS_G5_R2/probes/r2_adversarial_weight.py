"""Bounded sourcefree unequal-weight / order-sensitive locality parity case.

Builds a legitimate sourcefree 128-respondent weighted release with exact
non-integer rational/Decimal weights, then compares accepted baseline, the
physical-order runtime candidate, and the native oracle for full fact,
projection, replay and release identity.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
from types import MappingProxyType
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time
from typing import Any

REVIEW = Path(__file__).resolve().parents[1]
REPO = REVIEW.parents[1]
AUTHOR = REPO / "WORKER_RETURNS" / "PYAT1006_PHYSICAL_ECONOMICS_R1"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(AUTHOR))

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_c11_ingest import (
    build_candidate_replay_manifest,
    ingest_c11_source_release,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_carrier_execution import (
    RuntimeObjectCatalog, materialize_public_object,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalPredicate, EmpiricalQuerySpec, WeightMeasureFact, canonical_json, exact_ref,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate
import rawlsing_next._pre553_query_eval as query_eval
from rawlsing_next.tests.test_pre553_empirical_query import _query

from fixture_1006 import ShapeSpec, build_context, source_descriptor
from query_1006 import build_query_bundle
from r2_locality_probe import REAL_SORTED, _jsonable, fact_material, locality_sorted


WEIGHTS = (
    "1/3", "5/7", "11/13", "17/19", "0.1", "0.2",
    "0.30000000000000004", "7/3", "2/9", "13/11",
)


def modified_weight(fact: WeightMeasureFact, text: str) -> WeightMeasureFact:
    fields = dict(fact.semantic_fields)
    fields["exact_weight_value_representation"] = text
    return WeightMeasureFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=(
            fact.producer_replay_locator_or_reference_root
        ),
        **fields,
    )


def signature(result: Any) -> list[dict[str, Any]]:
    return [fact_material(fact) for fact in result.facts]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args(argv)
    outdir = Path(args.outdir).absolute()
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    root = outdir / "estate"
    root.mkdir(mode=0o700)
    result: dict[str, Any] = {
        "schema": "PYAT1006_R2_ADVERSARIAL_WEIGHT@1",
        "status": "RUNNING",
        "label": "SOURCEFREE_TEST_ONLY_EXPERIMENT",
    }
    out = outdir / "adversarial_weight.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    shape = ShapeSpec(
        "r2-adversarial-weight", 128, include_weights=True,
        tag="PYAT1006-R2-ADVERSARIAL-WEIGHT",
    )
    ctx = build_context(shape)
    bundle = build_query_bundle(ctx)
    original_weights = tuple(ctx.iter_weights())
    weights = tuple(
        modified_weight(fact, WEIGHTS[index % len(WEIGHTS)])
        for index, fact in enumerate(original_weights)
    )
    result["fixture"] = {
        "respondents": 128,
        "events": ctx.shape.event_count,
        "weight_count": len(weights),
        "weight_texts": sorted(set(WEIGHTS)),
        "weight_refs_sha256": hashlib.sha256(
            canonical_json([w.ref.as_dict() for w in weights]).encode()
        ).hexdigest(),
    }

    base_sections = ctx.direct_sections()
    streams = dict(base_sections.sections)
    streams["WeightMeasureFact"] = iter(weights)
    modified_sections = replace(
        base_sections, sections=MappingProxyType(streams)
    )
    candidate = ctx.candidate()
    no_replay = replace(
        candidate,
        weight_measure_facts_or_typed_absence=weights,
        candidate_replay_manifest=None,
    )
    replay = build_candidate_replay_manifest(
        no_replay,
        replay_protocol_authority_ref=candidate.candidate_replay_manifest.replay_protocol_authority_ref,
        deterministic_tie_order_rules_ref=candidate.candidate_replay_manifest.deterministic_tie_order_rules_ref,
        replay_protocol_version=candidate.candidate_replay_manifest.replay_protocol_version,
    )
    modified_candidate = replace(no_replay, candidate_replay_manifest=replay)
    repository = C11Repository()
    ingest = ingest_c11_source_release(modified_candidate, repository)
    if not ingest.accepted:
        raise AssertionError(ingest.errors)
    native_release = ingest.release_ref
    result["native_release"] = native_release.as_dict()

    qa = bundle.catalog.authorities[-2]
    extra_query = _query(
        source_descriptor(ctx), qa, bundle.f4_three_predicate, ("C", "D"),
        measure="GOVERNED_WEIGHTED", tag=f"{ctx.tag}-weighted-f4",
    )
    catalog = replace(
        bundle.catalog,
        queries=(*bundle.catalog.queries, extra_query),
    )
    receipt = write_direct_estate(
        modified_sections, ctx.universe.ref, root, chunk_rows=16,
    )
    result["receipt"] = {
        "manifest_sha256": receipt.manifest_sha256,
        "i02": {
            "logical": receipt.i02.logical,
            "physical": receipt.i02.physical,
            "release": receipt.i02.release,
            "source": receipt.i02.source,
            "replay": receipt.i02.replay,
            "universe": receipt.i02.universe,
            "schema": receipt.i02.schema,
        },
        "release": receipt.reconstructed_v1_release_ref.as_dict(),
        "retained_bytes": receipt.retained_bytes,
    }
    if receipt.reconstructed_v1_release_ref != native_release:
        result["status"] = "FAILED_RELEASE_RECONSTRUCTION"
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return 2

    admission = SavedC11Admission.open(
        root=root,
        exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=ExternalI02Roots(**{
            "logical": receipt.i02.logical,
            "physical": receipt.i02.physical,
            "release": receipt.i02.release,
            "source": receipt.i02.source,
            "replay": receipt.i02.replay,
            "universe": receipt.i02.universe,
            "schema": receipt.i02.schema,
        }),
        release_ref=receipt.reconstructed_v1_release_ref,
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )
    registry = AuthorityRegistry(catalog.authorities)
    queries = {
        "weighted": bundle.weighted,
        "weighted_f4": extra_query,
    }
    predicates = {
        "weighted": bundle.weighted_predicate,
        "weighted_f4": bundle.f4_three_predicate,
    }
    oracle = {}
    for name, query in queries.items():
        oracle[name] = signature(execute_empirical_query(
            repository=repository,
            query=query,
            predicate=predicates[name],
            authority_registry=registry,
            release_refs=(native_release,),
        ))
    baseline = {}
    for name, query in queries.items():
        baseline[name] = signature(admission.execute_i03(
            query_ref=query.ref, predicate_ref=predicates[name].ref,
        ))
    query_eval.sorted = locality_sorted
    candidate_results = {}
    try:
        for name, query in queries.items():
            candidate_results[name] = signature(admission.execute_i03(
                query_ref=query.ref, predicate_ref=predicates[name].ref,
            ))
    finally:
        query_eval.sorted = REAL_SORTED

    result["queries"] = {}
    all_equal = True
    for name in queries:
        base = baseline[name]
        cand = candidate_results[name]
        nat = oracle[name]
        equal_base_candidate = base == cand
        equal_base_oracle = base == nat
        all_equal = all_equal and equal_base_candidate and equal_base_oracle
        result["queries"][name] = {
            "baseline": base,
            "candidate": candidate_results[name],
            "oracle": nat,
            "baseline_candidate_exact": equal_base_candidate,
            "baseline_oracle_exact": equal_base_oracle,
            "public": [
                {
                    "ref": fact["ref"],
                    "state": fact["typed_state"],
                    "denominator": fact["raw_denominator_support"],
                    "numerator": fact["raw_numerator_support"],
                    "weighted_numerator": fact["weighted_numerator_support_if_authorized"],
                    "weighted_denominator": fact["weighted_denominator_support_if_authorized"],
                    "replay_ref": fact["replay_ref"],
                    "projection_sha256": fact["projection_sha256"],
                }
                for fact in base
            ],
        }
    result["status"] = "MEASURED" if all_equal else "FAILED_PARITY"
    result["all_exact"] = all_equal
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "all_exact": result["all_exact"],
        "fixture": result["fixture"],
        "release": result["receipt"]["release"],
        "queries": {
            name: {
                "baseline_candidate_exact": row["baseline_candidate_exact"],
                "baseline_oracle_exact": row["baseline_oracle_exact"],
                "public": row["public"],
            }
            for name, row in result["queries"].items()
        },
    }, indent=2, sort_keys=True))
    return 0 if all_equal else 2


if __name__ == "__main__":
    raise SystemExit(main())
