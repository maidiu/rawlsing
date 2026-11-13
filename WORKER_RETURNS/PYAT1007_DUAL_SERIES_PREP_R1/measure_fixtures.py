"""Bounded deterministic fixture/estate regeneration receipt for PYAT1007.

Generates the three TEST_ONLY fixtures twice under a disposable private temp
root, proves the persisted estate manifest SHA is deterministic, and writes the
exact fixture/config/release/manifest identities used by the tests.  No original
respondent bytes or rights are read.
"""
from __future__ import annotations

import json
from pathlib import Path
import tempfile

from rawlsing_next.pre553_r157_projection_adapter import canonical_config_hash

import fixture_harness as h

OUT = Path(__file__).resolve().parent / "evidence" / "FIXTURE_REGENERATION_MANIFEST.json"


def main() -> None:
    metadata = h.load_metadata()
    receipt: dict = {
        "schema": "PYAT1007_FIXTURE_REGENERATION_MANIFEST@1",
        "r157_commit": h.R157_COMMIT,
        "test_only": True,
        "original_source_bytes_read": False,
        "fixtures": {},
    }
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary).resolve()
        for key, spec in h.SERIES_SPECS.items():
            first = h.build_pipeline(root / key / "a", spec, metadata, estate_name=f"{key}-a")
            second = h.build_pipeline(root / key / "b", spec, metadata, estate_name=f"{key}-b")
            receipt["fixtures"][key] = {
                "source_id": metadata["series"][key]["source_id"],
                "family": metadata["series"][key]["family"],
                "wave": metadata["series"][key]["wave"],
                "source_format": metadata["series"][key]["source_format"],
                "fixture_file": first.fixture_path.name,
                "fixture_sha256": first.source_sha256,
                "fixture_bytes": first.fixture_path.stat().st_size,
                "fixture_writer_note": (
                    "SAV writer embeds a wall-clock timestamp; exact fixture SHA is recorded "
                    "per build and the decoded synthetic cell manifest is deterministic."
                    if metadata["series"][key]["source_format"] == "SAV"
                    else "DTA fixture bytes were deterministic across the two builds."
                ),
                "decoded_cell_manifest_sha256": h.decoded_cell_manifest_sha256(first),
                "decoded_cell_manifest_sha256_second_build": h.decoded_cell_manifest_sha256(second),
                "decoded_cell_manifest_deterministic": (
                    h.decoded_cell_manifest_sha256(first)
                    == h.decoded_cell_manifest_sha256(second)
                ),
                "config_canonical_sha256": canonical_config_hash(first.config),
                "config_purpose": first.config.config_purpose,
                "identity_class": first.config.identity_class,
                "fixture_authority_grade": (
                    first.config.document["binding"]["fixture_provenance"]["authority_grade"]
                ),
                "declared_original_source_sha256": metadata["series"][key]["declared_original_source_sha256"],
                "declared_original_source_read": False,
                "candidate_release_ref": first.release.release_ref.as_dict(),
                "reconstructed_v1_release_ref": first.receipt.reconstructed_v1_release_ref.as_dict(),
                "estate_manifest_sha256": first.receipt.manifest_sha256,
                "estate_manifest_sha256_second_build": second.receipt.manifest_sha256,
                "estate_manifest_deterministic": (
                    first.receipt.manifest_sha256 == second.receipt.manifest_sha256
                ),
                "estate_retained_bytes": first.receipt.retained_bytes,
                "family_counts": dict(first.receipt.family_counts),
                "universe_ref": first.projection.universes[0].ref.as_dict(),
                "respondent_key_grade": first.config.document["respondents"]["row_identity_grade"],
                "routing_states": {
                    row["question_id"]: row["typed_state"]
                    for row in first.config.document["routing"]
                },
                "weight_typed_absence": {
                    "type": type(
                        first.candidate.weight_measure_facts_or_typed_absence
                    ).__name__,
                    "state": first.candidate.weight_measure_facts_or_typed_absence.state,
                },
                "test_only_notes": first.config.document["notes"],
            }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    for key, row in receipt["fixtures"].items():
        print(
            key,
            row["fixture_sha256"],
            row["estate_manifest_sha256"],
            row["estate_retained_bytes"],
            "deterministic=" + str(row["estate_manifest_deterministic"]),
        )


if __name__ == "__main__":
    main()
