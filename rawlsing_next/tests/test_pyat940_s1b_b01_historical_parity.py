"""B01 independent historical fixture/roster parity at the nonrespondent grade.

The historical R157 source tree is not present in the protected checkout.  These
tests read only the accepted historical **nonrespondent** configuration/cells and
the roster metadata with ``git show``, write them under ``tmp_path``, and run the
current ported adapter plus the actual current first consumer.  No original SAV/
DTA source byte or respondent row is represented.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
from rawlsing_next.pre553_r157_projection_adapter import (
    R157_HISTORICAL_COMMIT,
    SourceConfigLibrary,
    build_governed_c11_projection,
    build_validated_c11_release_from_config,
    canonical_config_hash,
    load_source_config,
    load_fixture_stream,
    project_c11_candidate_from_config,
    row_native_keys_from_transport,
)

ROOT = Path(__file__).resolve().parents[2]

HISTORICAL_SRC09_ORIGINAL = (
    "rawlsing_next/source_configuration/data/SRC09/SRC09.config.json"
)
HISTORICAL_SRC09_FIXTURE_CONFIG = (
    "rawlsing_next/source_configuration/data/SRC09/SRC09.full.fixture.config.json"
)
HISTORICAL_SRC09_FIXTURE = "source_pre553_validation/SRC09/SRC09.full.fixture.json"
HISTORICAL_SRC09_NATIVE = "source_pre553_validation/SRC09/FULL_NATIVE_RESULTS.json"
HISTORICAL_ROSTER = "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json"

EXPECTED_SRC09_RELEASE_HASH = (
    "15f65920ec025a02a67b1572c3ce43f343186322f7dd2c381f18733c2d58194b"
)
EXPECTED_SRC09_REPLAY_HASH = (
    "733aa20553949f341ed08cd2624342abe55cd0f878abad5b6edc7165ba8520ed"
)
EXPECTED_SRC09_FIXTURE_SHA = (
    "fa0c989e71cce275316e307fdb5925f1a3c1a11952b3cbbce35e4822666b6d4b"
)


def _git_blob(relative: str) -> bytes:
    result = subprocess.run(
        [
            "git", "-C", str(ROOT), "show",
            f"{R157_HISTORICAL_COMMIT}:{relative}",
        ],
        capture_output=True,
        check=True,
    )
    return result.stdout


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _historical_src09_library(tmp_path: Path):
    original_bytes = _git_blob(HISTORICAL_SRC09_ORIGINAL)
    fixture_config_bytes = _git_blob(HISTORICAL_SRC09_FIXTURE_CONFIG)
    fixture_bytes = _git_blob(HISTORICAL_SRC09_FIXTURE)
    native = json.loads(_git_blob(HISTORICAL_SRC09_NATIVE))
    roster = json.loads(_git_blob(HISTORICAL_ROSTER))
    roster_entry = next(
        row for row in roster["sources"] if row["source_id"] == "SRC09"
    )

    original_path = tmp_path / "SRC09.config.json"
    fixture_config_path = tmp_path / "SRC09.full.fixture.config.json"
    fixture_path = tmp_path / "SRC09.full.fixture.json"
    native_path = tmp_path / "FULL_NATIVE_RESULTS.json"
    original_path.write_bytes(original_bytes)
    fixture_config_path.write_bytes(fixture_config_bytes)
    fixture_path.write_bytes(fixture_bytes)
    native_path.write_bytes(json.dumps(native).encode("utf-8"))

    original_document = json.loads(original_bytes)
    fixture_document = json.loads(fixture_config_bytes)
    index = {
        "schema": "PYAT_R157_SOURCE_LIBRARY_INDEX@1.0.0",
        "sources": [{
            "source_id": "SRC09",
            "family": "Asian Barometer",
            "wave": "W4",
            "lane": "ASIAN",
            "status": "AVAILABLE_NATIVE_RECEIPT",
            "original_config_path": original_path.name,
            "original_config_file_sha256": _sha256(original_bytes),
            "original_config_canonical_sha256": canonical_config_hash(original_document),
            "fixture_config_path": fixture_config_path.name,
            "fixture_config_file_sha256": _sha256(fixture_config_bytes),
            "fixture_path": fixture_path.name,
            "fixture_file_sha256": _sha256(fixture_bytes),
            "fixture_source_sha256": fixture_document["binding"]["source_sha256"],
            "native_results_path": native_path.name,
            "native_results_file_sha256": _sha256(native_path.read_bytes()),
            "release_ref": native["full_fixture_native_validation"]["release_ref"],
            "counts": {
                "physical_slots": len(original_document["physical_slots"]),
                "original_items": len(original_document["items"]),
            },
            "held": {},
            "details": [],
        }],
    }
    index_path = tmp_path / "index.json"
    index_path.write_text(json.dumps(index, sort_keys=True), encoding="utf-8")
    return (
        SourceConfigLibrary(index_path=index_path, root=tmp_path),
        roster_entry,
        original_path,
        fixture_config_path,
        fixture_path,
    )


def test_b01_historical_roster_totals_and_unjoined_census_are_exact():
    roster = json.loads(_git_blob(HISTORICAL_ROSTER))
    assert roster["counts"]["sources"] == 35
    assert roster["counts"]["original_items"] == 18_276
    assert roster["counts"]["physical_columns"] == 18_413
    assert roster["counts"]["exact_relation_matches"] == 18_250
    assert roster["counts"]["unmatched_relation_ids"] == 26
    unjoined = {
        (row["source_id"], implementation_id)
        for row in roster["sources"]
        for implementation_id in row.get("unmatched_relation_ids", ())
    }
    assert len(unjoined) == 26
    assert {source_id for source_id, _ in unjoined} == {"SRC01", "SRC24", "SRC26"}


def test_b01_historical_src09_full_nonrespondent_fixture_release_parity(tmp_path):
    library, roster_entry, _original_path, fixture_config_path, fixture_path = (
        _historical_src09_library(tmp_path)
    )

    validation = library.validate_source(
        "SRC09", historical_roster_entry=roster_entry)
    assert validation["passed"] is True
    assert validation["historical_roster_comparison"] == "PASS"
    assert validation["checks"]["historical_physical_slots"] is True
    assert validation["checks"]["historical_original_items"] is True

    release_from_library = library.build_fixture_release("SRC09")
    assert release_from_library.release_ref.content_hash == EXPECTED_SRC09_RELEASE_HASH
    assert release_from_library.replay_manifest.ref.content_hash == EXPECTED_SRC09_REPLAY_HASH
    assert release_from_library.source_artifact_ref.content_hash == EXPECTED_SRC09_FIXTURE_SHA

    config = load_source_config(fixture_config_path)
    stream = load_fixture_stream(fixture_path)
    keys = row_native_keys_from_transport(config, stream=stream)
    projection = build_governed_c11_projection(config, row_native_keys=keys)
    candidate = project_c11_candidate_from_config(
        config,
        projection,
        cells_factory=stream.iter_cells,
        row_native_keys=keys,
        source_sha256=stream.source_sha256,
        row_count=stream.row_count,
    )
    release_from_first_consumer = validate_c11_source_release(candidate)
    assert (
        release_from_first_consumer.release_ref.content_hash
        == EXPECTED_SRC09_RELEASE_HASH
    )
    assert (
        release_from_first_consumer.replay_manifest.ref.content_hash
        == EXPECTED_SRC09_REPLAY_HASH
    )

    full_release = build_validated_c11_release_from_config(config, stream=stream)
    assert full_release.release_ref.content_hash == EXPECTED_SRC09_RELEASE_HASH


def test_b01_historical_roster_comparison_refuses_wrong_denominators(tmp_path):
    library, _roster_entry, _original_path, _fixture_config_path, _fixture_path = (
        _historical_src09_library(tmp_path)
    )
    wrong = library.validate_source(
        "SRC09",
        historical_roster_entry={"physical_columns": 290, "original_items": 289},
    )
    assert wrong["passed"] is False
    assert wrong["historical_roster_comparison"] == "FAIL"
    assert wrong["checks"]["historical_physical_slots"] is False
    assert wrong["checks"]["historical_original_items"] is True
