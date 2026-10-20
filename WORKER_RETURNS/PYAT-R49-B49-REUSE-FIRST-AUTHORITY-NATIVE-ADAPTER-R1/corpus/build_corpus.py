#!/usr/bin/env python3
"""Build the frozen B49 source-authority corpus from the exact H48 evidence.

Reads the H48 R48 evidence blobs (already committed to the private rawlsing
repository) and writes a deterministic JSON corpus for the B49 source-rule
selection tests. No respondent data, no raw SAV/DTA bytes, no source grant.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

H48_COMMIT = "359ddabc89d78ceb4c8fa45561588ee4cad7dd11"
H48_DIR = "WORKER_RETURNS/PYAT-R48-H48-AUTHORITY-AND-CODE-ATLAS-R1"
OUT = Path(__file__).resolve().parent


def blob(path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{H48_COMMIT}:{H48_DIR}/{path}"],
        check=True, capture_output=True,
    ).stdout


def main() -> int:
    source_identity = json.loads(
        blob("evidence/closed35_source_identity_and_decoder_metadata.json")
    )
    coverage_rows = list(csv.DictReader(
        blob("04_SOURCE35_MEASUREMENT_AND_AUTHORITY_COVERAGE.csv").decode().splitlines()
    ))
    items = json.loads(gzip.decompress(
        blob("evidence/original_item_authority_candidates.json.gz")
    ))
    unmatched = json.loads(
        blob("evidence/full_relation_unmatched_exact_ids.json")
    )
    surfaces = list(csv.DictReader(
        blob("evidence/closed35_typed_surface_metadata.csv").decode().splitlines()
    ))

    coverage = {}
    for row in coverage_rows:
        coverage[(row["source_family"], row["wave"])] = {
            "source_id": row["source_id"],
            "canonical_filename": row["canonical_filename"],
            "declared_source_sha256": row["declared_source_sha256"],
            "declared_source_bytes": int(row["declared_source_bytes"] or 0),
            "source_format": row["source_format"],
            "accepted_historical_decoder_mode": row["accepted_historical_decoder_mode"],
            "p2_implementation_rows": int(row["p2_implementation_rows"] or 0),
            "original_administered_measurement_U": row["original_administered_measurement_U"],
            "actual_eligible_E_pre": row["actual_eligible_E_pre"],
            "current_source_host_purpose_grant": row["current_source_host_purpose_grant"],
            "source_documentary_unknowns": row["source_documentary_unknowns"],
        }

    sources = []
    for entry in source_identity["sources"]:
        key = (entry["family"], entry["wave_or_release"])
        cov = coverage.get(key)
        sources.append({
            "source_id": entry["source_id"],
            "family": entry["family"],
            "wave": entry["wave_or_release"],
            "canonical_filename": entry["canonical_filename"],
            "declared_sha256": entry["canonical_sha256"],
            "size_bytes": entry["size_bytes"],
            "source_format": entry["source_format"],
            "decoder_mode": entry["accepted_decoder_mode"],
            "expected_rows": (entry.get("expected_shape") or {}).get("rows"),
            "documentary_unknowns": entry.get("documentary_unknowns", ""),
            "authority_launch_class": entry.get("authority72_launch_class"),
            "coverage": cov,
        })

    unmatched_ids = {
        row["question_implementation_id"] for row in unmatched["rows"]
    }
    items_out = []
    item_counts: dict[tuple[str, str], int] = {}
    for item in items:
        item_counts[(item["source_family"], item["wave"])] = (
            item_counts.get((item["source_family"], item["wave"]), 0) + 1
        )
        if item["source_family"] != "LiTS" and item["question_implementation_id"] not in unmatched_ids:
            continue
        bindings = {b["family"]: b for b in item["candidate_bindings"]}
        p2 = bindings.get("P2_IMPLEMENTATION_IDENTITY", {})
        deep_key = next(
            (k for k in bindings if k.startswith("P2_DEEP_")), None
        )
        deep = bindings.get(deep_key, {}) if deep_key else {}
        manual_key = next((k for k in bindings if k.startswith("MANUAL_")), None)
        manual = bindings.get(manual_key, {}) if manual_key else {}
        direction = bindings.get(
            next((k for k in bindings if k.endswith("_directionality")), ""), {}
        )
        o06 = bindings.get("O06_IMPLEMENTATION_ROUTING_CENTRAL.jsonl", {})
        relations = item.get("full_relation_explicit_id_bindings", [])
        items_out.append({
            "implementation_id": item["question_implementation_id"],
            "source_family": item["source_family"],
            "wave": item["wave"],
            "source_variable_code": item["source_variable_code"],
            "p2_row": item["p2_row"],
            "p2_evidence_id": item["p2_evidence_id"],
            "exact_identity_sha256": item["exact_identity_sha256"],
            "disposition": item["disposition"],
            "binding_grade": item["binding_grade"],
            "p2_disposition": p2.get("status", {}).get("canonical_disposition", ""),
            "response_binding_status": (
                deep.get("status", {}).get("response_binding_status")
                or p2.get("status", {}).get("response_binding_status")
                or ""
            ),
            "directional_certification_status": (
                manual.get("status", {}).get("directional_certification_status")
                or direction.get("status", {}).get("directional_certification_status")
                or deep.get("status", {}).get("directional_certification_status")
                or ""
            ),
            "current_directional_atom_eligible": (
                str(
                    manual.get("status", {}).get("current_directional_atom_eligible")
                    or direction.get("status", {}).get("current_directional_atom_eligible")
                    or deep.get("status", {}).get("current_directional_atom_eligible")
                    or "False"
                ).lower() == "true"
            ),
            "routing_status": o06.get("status", {}).get("routing_status", ""),
            "relation_evidence_id": relations[0]["evidence_id"] if relations else None,
            "relation_data_row": relations[0]["data_row"] if relations else None,
            "relation_assertions": (
                relations[0].get("preserved_assertions", {}) if relations else {}
            ),
            "overlay_evidence_ids": sorted(
                b["evidence_id"] for k, b in bindings.items()
                if k.startswith("WAVE_OVERLAY_")
            ),
        })

    for source in sources:
        key = (source["family"], source["wave"])
        if source["coverage"] is not None:
            source["coverage"]["observed_item_records"] = item_counts.get(key, 0)
        source["observed_item_records"] = item_counts.get(key, 0)

    corpus = {
        "schema": "B49_SOURCE_AUTHORITY_CORPUS@1.0.0",
        "h48_commit": H48_COMMIT,
        "source_count": len(sources),
        "item_count": len(items_out),
        "total_authority_items": len(items),
        "unmatched_count": unmatched["count"],
        "wave_aliases": {
            "LiTS": {"2006": "I"},
            "Afrobarometer": {"R1": "Round 1", "R5": "Round 5", "R9": "Round 9"},
        },
        "sources": sorted(sources, key=lambda s: (s["family"], s["wave"])),
        "items": sorted(items_out, key=lambda x: x["implementation_id"]),
        "unmatched_ids": sorted(
            (row["question_implementation_id"] for row in unmatched["rows"])
        ),
        "typed_surfaces": [
            {
                "surface_id": s["surface_id"],
                "source_id": s["source_id"],
                "variable_name": s["variable_name"],
                "ordinal": s["ordinal"],
                "surface_kind": s["surface_kind"],
                "rule_native_domain_json": s["rule_native_domain_json"],
                "representation_authority": s["representation_authority"],
                "documentary_unknowns": s["documentary_unknowns"],
            }
            for s in surfaces
        ],
    }
    raw = json.dumps(corpus, sort_keys=True, separators=(",", ":")).encode()
    (OUT / "source_authority_corpus.json").write_bytes(raw)
    print(json.dumps({
        "sources": len(sources),
        "items": len(items_out),
        "unmatched": corpus["unmatched_count"],
        "surfaces": len(surfaces),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
