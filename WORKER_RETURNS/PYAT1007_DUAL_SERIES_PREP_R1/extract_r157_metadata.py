"""Extract compact R157 semantic-edition metadata for PYAT1007 TEST_ONLY fixtures.

Reads only Git metadata blobs at the accepted R157 commit.  It does not read,
download, hash, decode, or copy original respondent bytes or SAV/DTA holdings.
The emitted JSON is a provenance witness for the TEST_ONLY fixture configs:
selected physical variables, labels, missing/state rules, routing states,
respondent-key grain and weight-slot absence.  Full R157 value maps are not
copied into the repository; only the exact subset exercised by the fixtures is
retained with the source blob SHA-256.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
COMMIT = "1924499ef52403a0f331b8aff9b7c7eff99bf1e2"
OUT = Path(__file__).resolve().parent / "metadata" / "R157_METADATA_GROUNDING.json"

SERIES = {
    "ARAB_SRC07": {
        "source_id": "SRC07",
        "config_path": "rawlsing_next/source_configuration/data/SRC07/source.config.json",
        "variables": ("COUNTRY", "Q508", "Q509", "Q104A_2_1"),
        "coordinates": ("COUNTRY",),
    },
    "WVS_SRC35": {
        "source_id": "SRC35",
        "config_path": "rawlsing_next/source_configuration/data/SRC35/SRC35.source.config.json",
        "variables": ("S007", "A_YEAR", "Q1", "Q2", "Q3", "Q4"),
        "coordinates": ("A_YEAR",),
    },
    "LITS_SRC28_HOSTILE": {
        "source_id": "SRC28",
        "config_path": "rawlsing_next/source_configuration/data/SRC28/src28.config.json",
        "variables": ("psu", "q201", "q102_1"),
        "coordinates": ("psu",),
    },
}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "schema": "PYAT1007_R157_METADATA_GROUNDING@1",
        "r157_commit": COMMIT,
        "r157_config_schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
        "evidence_grade": (
            "METADATA_ONLY__R157_GIT_CONFIG_BLOBS__NO_ORIGINAL_RESPONDENT_BYTES_READ"
        ),
        "original_source_bytes_read": False,
        "original_source_hold": {
            "state": "SOURCE_BYTES_UNAVAILABLE|SOURCE_PERMISSION_HELD",
            "current_use_grant": "UNKNOWN_NOT_ESTABLISHED_BY_THIS_PREP",
            "translation_or_rights_edition_state": "UNKNOWN_TYPED_HOLD",
        },
        "fixture_policy": {
            "grade": "NONRESPONDENT_FIXTURE_ONLY",
            "row_ids": "SYNTHETIC_TEST_ONLY",
            "bytes": "SYNTHETIC_TEST_ONLY_SAV_DTA",
            "source_sha256": "SYNTHETIC_TEST_ONLY_NOT_ORIGINAL",
            "scientific_comparability": "NOT_CLAIMED",
            "design_issuer": "NOT_ISSUED",
        },
        "series": {},
    }
    for key, spec in SERIES.items():
        blob = git("show", f"{COMMIT}:{spec['config_path']}")
        size = int(git("cat-file", "-s", f"{COMMIT}:{spec['config_path']}").strip())
        document = json.loads(blob)
        identity = document["identity"]
        routing_by_qid = {
            row["question_id"]: row["typed_state"]
            for row in document.get("routing", [])
        }
        response_by_name = {
            row["slot"]["name"]: row for row in document.get("response_slots", [])
        }
        coordinate_by_name = {
            row["slot"]["name"]: row for row in document.get("coordinate_slots", [])
        }
        physical_by_name = {
            row["name"]: row for row in document.get("physical_slots", [])
        }
        selected: dict[str, Any] = {}
        for name in spec["variables"]:
            slot = physical_by_name[name]
            payload: dict[str, Any] = {
                "ordinal": slot["ordinal"],
                "label": slot.get("label"),
                "storage_type": slot.get("storage_type"),
                "original_type": slot.get("original_type"),
                "storage_width": slot.get("storage_width"),
                "measure": slot.get("measure"),
                "value_labels": slot.get("value_labels"),
                "missing_declarations": slot.get("missing_declarations"),
                "mr_declarations": slot.get("mr_declarations"),
                "disposition": slot.get("disposition"),
                "codebook_mapping": slot.get("codebook_mapping"),
            }
            response = response_by_name.get(name)
            if response is not None:
                payload["r157_question_id"] = response["question_id"]
                payload["r157_routing_state"] = routing_by_qid.get(
                    response["question_id"]
                )
                payload["r157_value_states"] = [
                    {
                        "raw_value": value["raw_value"],
                        "missing_state": value["missing_state"],
                        "source_missing_declaration": value.get(
                            "source_missing_declaration"
                        ),
                        "response_state": value["response_state"],
                        "occurrences": [
                            {
                                "key": occurrence["key"],
                                "topology_ref_kind": occurrence["topology_ref"]["kind"],
                                "multiplicity_order_rank_fields": occurrence[
                                    "multiplicity_order_rank_fields"
                                ],
                            }
                            for occurrence in value["occurrences"]
                        ],
                    }
                    for value in response["values"]
                ]
            coordinate = coordinate_by_name.get(name)
            if coordinate is not None:
                payload["r157_coordinate_slot"] = {
                    "native_coordinate_ref": coordinate["native_coordinate_ref"],
                    "unit_taxonomy_ref": coordinate["unit_taxonomy_ref"],
                    "effective_time": coordinate["effective_time"],
                    "copy_observed_raw": coordinate.get("copy_observed_raw", False),
                }
            selected[name] = payload
        manifest["series"][key] = {
            "source_id": spec["source_id"],
            "config_path": spec["config_path"],
            "config_blob_sha256": hashlib.sha256(blob).hexdigest(),
            "config_blob_bytes": size,
            "config_id": document["config_id"],
            "config_revision": document["config_revision"],
            "family": identity["family"],
            "wave": identity["wave"],
            "source_family_id": identity["source_family_id"],
            "release_id": identity["release_id"],
            "instrument_release_id": identity["instrument_release_id"],
            "source_artifact_id": identity["source_artifact_id"],
            "source_format": identity["source_format"],
            "declared_original_source_sha256": identity["expected_source_sha256"],
            "declared_original_source_sha256_state": (
                "DECLARED_IN_R157_METADATA__NOT_READ__NOT_A_PERMISSION_GRANT"
            ),
            "source_row_count_declared": identity["source_row_count"],
            "source_column_count_declared": identity["source_column_count"],
            "source_bytes_declared": identity["source_bytes"],
            "respondents": document["respondents"],
            "weight_slots_count": len(document.get("weight_slots", [])),
            "weight_declaration_state": (
                "NO_WEIGHT_SLOT_IN_R157_CONFIG__DESIGN_PLACEHOLDER_TYPED_ABSENCE"
                if not document.get("weight_slots")
                else "WEIGHT_SLOT_PRESENT_IN_R157_CONFIG"
            ),
            "coordinate_slot_names": tuple(
                row["slot"]["name"] for row in document.get("coordinate_slots", [])
            ),
            "selected_variables": selected,
        }
    OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    for key, row in manifest["series"].items():
        print(
            key,
            row["source_id"],
            row["family"],
            row["wave"],
            row["source_format"],
            "config_sha256=" + row["config_blob_sha256"],
        )


if __name__ == "__main__":
    main()
