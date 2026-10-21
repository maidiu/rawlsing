"""Capture UR-B native chain, custody and import receipts."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
for path in (ROOT, REPO,
             Path.home() / ".cache/uv/archive-v0/sFE7VO7nHEpr328Z",
             Path.home() / ".cache/uv/archive-v0/quC1M_vhOV9lE6BI"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from ur_b.batch_resume import dump as batch_dump, resume as batch_resume
from ur_b.custody import compare as custody_compare
from ur_b.s1 import build as build_s1
from ur_b.s1_batch import run as run_batch
from ur_b.s1_queries import run as run_s1_queries
from ur_b.s1_route_b import execute as execute_s1_route_b
from ur_b.s2 import build_household, build_person
from ur_b.s2_queries import cross_unit_attempt, run_household, run_person
from ur_b.s3 import release as s3_release
from ur_b.s3_repeated_query import run as s3_repeated_query


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _git_blob(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _cells(fact):
    return [
        {"cell": row["cell"], "state": row.get("cell_state"),
         "raw": row.get("raw_numerator_support"),
         "weighted": row.get("weighted_numerator_support_if_authorized")}
        for row in fact.target_topology.get("complete_cell_semantic_projection", [])
    ]


def main():
    evidence = ROOT / "evidence"
    receipts = ROOT / "receipts"
    evidence.mkdir(exist_ok=True)
    receipts.mkdir(exist_ok=True)
    fixtures = ROOT / "fixtures"

    s1 = build_s1(fixtures / "ur_b_s1_xor.sav")
    s1_queries = run_s1_queries(s1)
    s1_route_setup, s1_route = execute_s1_route_b(s1)
    s1_batch = run_batch(s1)
    batch_path = receipts / "s1_batch_resume.json"
    batch_document = batch_dump(s1, batch_path)
    batch_resumed = batch_resume(s1, batch_path)
    custody = custody_compare(fixtures / "ur_b_s1_xor.sav")

    s2_person = build_person(fixtures / "ur_b_s2_person.dta")
    s2_house = build_household(fixtures / "ur_b_s2_household.dta")
    s2_person_out = run_person(s2_person)
    s2_house_out = run_household(s2_house)
    s2_cross = cross_unit_attempt(s2_person, s2_house)

    s3_fx, s3_release_obj = s3_release(
        fixtures / "ur_b_s3_repeated.sav", respondents_count=12, repeated=True)
    s3_query = s3_repeated_query(s3_fx)
    s3_events = [obj for obj in s3_release_obj.public_objects
                 if type(obj).__name__ == "RespondentEvent"]

    def oid(value):
        try:
            return value["object_id"]
        except Exception:
            return value.object_id

    question_ids = {oid(q.native_question_ref): oid(q.native_question_ref)
                    for q in s3_fx["projection"].questions}
    s3_counts = Counter(question_ids[oid(event.native_question_ref)]
                        for event in s3_events)

    chain = {
        "schema": "UR_B_NATIVE_CHAIN@1",
        "S1": {
            "source_sha256": s1["incidence"].source_sha256,
            "projection_ref": s1["projection"].projection_identity_ref.as_dict(),
            "release_ref": s1_route.c11_release.release_ref.as_dict(),
            "c11_public_objects": len(s1_route.c11_release.public_objects),
            "i03_fact_count": sum(len(x.facts) for x in s1_route.i03_results),
            "i03_facts": {
                name: {"typed_state": result.facts[0].typed_state,
                       "raw_denominator": result.facts[0].raw_denominator_support,
                       "weighted_denominator": result.facts[0].weighted_denominator_support_if_authorized,
                       "cells": _cells(result.facts[0])}
                for name, result in s1_queries["results"].items()},
            "i05_receipt_count": len(s1_route.i05_result.receipts),
            "learned_receipt": s1_route.learned_empirical_execution_receipt,
            "object_graph_counts": {
                "facts": len(s1_route.object_graph.empirical_facts),
                "discovery_receipts": len(s1_route.object_graph.discovery_receipts),
                "authorities": len(s1_route.object_graph.authority_snapshots),
            },
            "batch": {
                "unit_count": len(s1_batch["manifest"].units),
                "receipt_count": len(s1_batch["receipts"]),
                "states": [r.state for r in s1_batch["receipts"]],
                "resume_pending": len(batch_resumed["pending"]),
                "resume_manifest_hash": batch_resumed["manifest_hash"],
            },
            "custody": custody,
        },
        "S2": {
            "person_source_sha256": s2_person["incidence"].source_sha256,
            "household_source_sha256": s2_house["incidence"].source_sha256,
            "person_results": {
                name: {"typed_state": result.facts[0].typed_state,
                       "raw_denominator": result.facts[0].raw_denominator_support,
                       "weighted_denominator": result.facts[0].weighted_denominator_support_if_authorized,
                       "cells": _cells(result.facts[0])}
                for name, result in s2_person_out["results"].items()},
            "household_result": {
                "typed_state": s2_house_out["result"].facts[0].typed_state,
                "raw_denominator": s2_house_out["result"].facts[0].raw_denominator_support,
                "cells": _cells(s2_house_out["result"].facts[0])},
            "cross_unit_attempt": s2_cross,
        },
        "S3": {
            "source_sha256": s3_fx["incidence"].source_sha256,
            "release_ref": s3_release_obj.release_ref.as_dict(),
            "respondent_count": 12,
            "physical_row_count": 24,
            "event_count": len(s3_events),
            "event_counts_by_question": dict(s3_counts),
            "repeated_query_status": s3_query["result"].facts[0].typed_state,
            "repeated_query_raw_denominator": s3_query["result"].facts[0].raw_denominator_support,
        },
    }
    (evidence / "native_chain.json").write_text(
        json.dumps(chain, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8")
    (receipts / "s1_batch_resume.json").write_text(
        json.dumps(batch_document, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    import numpy
    import pandas
    import pyreadstat
    imports = {
        "schema": "UR_B_IMPORT_CUSTODY@1",
        "python": sys.version,
        "packages": {
            "pyreadstat": {"version": pyreadstat.__version__,
                           "path": pyreadstat.__file__,
                           "sha256": _sha256(pyreadstat.__file__)},
            "pandas": {"version": pandas.__version__,
                       "path": pandas.__file__,
                       "sha256": _sha256(pandas.__file__)},
            "numpy": {"version": numpy.__version__,
                      "path": numpy.__file__,
                      "sha256": _sha256(numpy.__file__)},
        },
        "native_modules": {},
    }
    for relative in (
        "rawlsing_next/pre553_physical_decoder.py",
        "rawlsing_next/pre553_source_backed_c11_facade.py",
        "rawlsing_next/pre553_physical_c11_bridge.py",
        "rawlsing_next/pre553_c11_ingest.py",
        "rawlsing_next/pre553_c11_repository.py",
        "rawlsing_next/pre553_empirical_objects.py",
        "rawlsing_next/pre553_empirical_query.py",
        "rawlsing_next/pre553_route_b_production.py",
        "rawlsing_next/pre553_discovery_exact.py",
        "rawlsing_next/pre553_batch_runner.py",
        "rawlsing_next/pre553_carrier_execution.py",
        "rawlsing_next/pre553_empirical_authority.py",
    ):
        path = REPO / relative
        imports["native_modules"][relative] = {
            "path": str(path), "sha256": _sha256(path),
            "git_blob": _git_blob(path),
        }
    (evidence / "imports.json").write_text(
        json.dumps(imports, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    fixture_manifest = {
        "schema": "UR_B_FIXTURE_MANIFEST@1",
        "files": {p.name: {"bytes": p.stat().st_size, "sha256": _sha256(p)}
                  for p in sorted(fixtures.iterdir())},
    }
    (evidence / "fixtures.json").write_text(
        json.dumps(fixture_manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
