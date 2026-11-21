from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import subprocess

import pytest

from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_physical_decoder import (
    COMPATIBILITY_ALLOWLIST,
    COMPATIBILITY_ONLY,
    DecoderError,
    PhysicalCell,
    PhysicalMissingState,
    decode_sav,
)
from rawlsing_next.pre553_r157_projection_adapter import (
    FIXTURE_SCHEMA_ID,
    CURRENT_GRANTED,
    EXACT_FILE,
    R157_ABSENT_CURRENT_PORTS,
    R157_HISTORICAL_COMMIT,
    R157_HISTORICAL_FUNCTION_MAP,
    R157_IRREDUCIBLE_DETERMINANTS,
    SOURCE_RESPONSE_DECODE,
    IssuedSourceReadDecision,
    SourceConfig,
    SourceConfigLibrary,
    SourceConfigurationBindingError,
    SourceConfigurationFactoryError,
    SourceConfigurationSchemaError,
    SourceLibraryError,
    SourceReadAdmissionRefusal,
    assert_exact_index_paths,
    build_index,
    build_governed_c11_projection,
    build_source_backed_c11_repository_from_config,
    build_validated_c11_release_from_config,
    decode_fixture_config,
    decode_with_source_read_permission,
    project_c11_candidate_from_config,
    reader_configuration_from_config,
    canonical_config_hash,
    config_file_sha256,
    fixture_document_sha256,
    fixture_stream_from_document,
    row_native_keys_from_transport,
    source_read_request_from_config,
    unjoined_r157_original_item_census,
    validate_source_config,
    verify_config_projection_binding,
)
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.tests.test_pyat940_s1b_support import (
    build_scenario,
    make_config,
    ref,
    sha256_text,
    write_fixture,
)


ROOT = Path(__file__).resolve().parents[2]
HISTORICAL_SRC09 = (
    "source_pre553_validation/integration/examples/SRC09_q101_keyed_fixture.config.json"
)


def _historical_document() -> dict:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{R157_HISTORICAL_COMMIT}:{HISTORICAL_SRC09}"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        "the exact historical R157 fixture config must be readable with git show; "
        f"stderr={result.stderr!r}"
    )
    return json.loads(result.stdout)


def _event_refs(candidate):
    return tuple(event.ref.content_hash for event in candidate.respondent_events)


def _respondent_refs(candidate):
    return tuple(item.ref.content_hash for item in candidate.respondent_identities)


def test_b01_historical_function_and_determinant_map_uses_real_config():
    census = unjoined_r157_original_item_census()
    assert census["count"] == 26
    assert census["status"] == "PREPARATION_HELD__NOT_SCIENCE"
    assert set(census["by_source"]) == {"SRC01", "SRC24", "SRC26"}
    assert census["by_source"] == {"SRC01": 3, "SRC24": 18, "SRC26": 5}
    assert len({item[1] for item in census["items"]}) == 26

    assert R157_HISTORICAL_FUNCTION_MAP
    for key, item in R157_HISTORICAL_FUNCTION_MAP.items():
        assert item["status"] in {
            "PORTED", "PORTED_REPAIRED_BINDING", "PORTED_MISSING_OWNER",
            "PORTED_WITH_EXTERNAL_HOLD", "REPAIRED_CURRENT_OWNER", "ABSENT_CURRENT_PORT",
        }, key
    assert "library.build_index" in R157_HISTORICAL_FUNCTION_MAP
    assert R157_HISTORICAL_FUNCTION_MAP["library.build_index"]["status"] == "ABSENT_CURRENT_PORT"
    assert "rawlsing_next.source_configuration package" in R157_ABSENT_CURRENT_PORTS
    assert "originals" not in " ".join(R157_ABSENT_CURRENT_PORTS).lower()
    assert set(R157_IRREDUCIBLE_DETERMINANTS) >= {
        "source_identity", "custody_and_reader", "binding_and_edition",
        "row_and_respondent", "instrument_question_and_topology",
        "physical_slot", "response_and_occurrence", "coordinate", "weight",
        "routing_eligibility", "authority_and_replay", "ownership",
        "scope_and_conservation",
    }

    # The real historical R157 fixture config must pass the ported closed schema.
    document = _historical_document()
    validate_source_config(document)
    config = SourceConfig(document)
    values = [value["raw_value"] for value in document["response_slots"][0]["values"]]
    rows = document["binding"]["row_count"]
    cells = []
    for row, value in enumerate(values, 1):
        state = (
            PhysicalMissingState.SYSTEM_MISSING
            if value is None
            else PhysicalMissingState.OBSERVED_STORAGE_VALUE
        )
        cells.append(PhysicalCell(row, 124, "q101", value, state, None))
        cells.append(PhysicalCell(row, 1, "country", float(row), PhysicalMissingState.OBSERVED_STORAGE_VALUE, None))
    stream = ExactPhysicalCellStream(
        source_sha256=document["binding"]["source_sha256"],
        row_count=rows,
        cell_iter_factory=lambda: tuple(cells),
    )
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
    release = validate_c11_source_release(candidate)
    assert len(candidate.respondent_identities) == 9
    assert len(candidate.respondent_events) == 9
    assert release.release_ref.content_hash
    assert candidate.source_release_manifest.instrument_release_id == (
        document["binding"]["fixture_provenance"]["fixture_instrument_release_id"]
    )


@pytest.mark.parametrize("source_format", ("SAV", "DTA"))
def test_b02_b03_real_projection_change_and_exact_restore(tmp_path, source_format):
    scenario = build_scenario(tmp_path / source_format, source_format=source_format)
    incidence = scenario["incidence"]
    try:
        base_release = scenario["release"].release_ref.content_hash
        base_events = _event_refs(scenario["candidate"])
        base_respondents = _respondent_refs(scenario["candidate"])
        assert len(base_events) == scenario["rows"]
        assert len(base_respondents) == scenario["rows"]

        # Changed but still-valid response mapping changes the exact event identity.
        changed_document = deepcopy(scenario["document"])
        changed_document["response_slots"][0]["values"][0]["response_state"] = "DK"
        changed_config = SourceConfig(changed_document)
        changed_projection = build_governed_c11_projection(
            changed_config, row_native_keys=scenario["keys"]
        )
        changed_candidate = project_c11_candidate_from_config(
            changed_config,
            changed_projection,
            cells=tuple(incidence.iter_cells(4)),
            row_native_keys=scenario["keys"],
            source_sha256=incidence.source_sha256,
            row_count=incidence.row_count,
        )
        changed_release = validate_c11_source_release(changed_candidate)
        assert changed_release.release_ref.content_hash != base_release
        assert _event_refs(changed_candidate) != base_events
        assert len(set(_event_refs(changed_candidate)) & set(base_events)) == len(base_events) - 1

        # Exact restoration reproduces the original identity, not merely a loader.
        restored_config = SourceConfig(deepcopy(scenario["document"]))
        restored_projection = build_governed_c11_projection(
            restored_config, row_native_keys=scenario["keys"]
        )
        restored_candidate = project_c11_candidate_from_config(
            restored_config,
            restored_projection,
            cells=tuple(incidence.iter_cells(4)),
            row_native_keys=scenario["keys"],
            source_sha256=incidence.source_sha256,
            row_count=incidence.row_count,
        )
        restored_release = validate_c11_source_release(restored_candidate)
        assert restored_release.release_ref.content_hash == base_release
        assert _event_refs(restored_candidate) == base_events
        assert _respondent_refs(restored_candidate) == base_respondents

        # A changed valid edition (row-native key) changes respondent/event identity.
        alternate_countries = [float(((index + 5) % 9) + 1) for index in range(scenario["rows"])]
        alternate_path, alternate_sha, alternate_rows = write_fixture(
            tmp_path / f"{source_format}-alternate",
            source_format=source_format,
            values=scenario["values"],
            countries=alternate_countries,
        )
        alternate_document = make_config(
            source_format=source_format,
            active_source_sha256=alternate_sha,
            row_count=alternate_rows,
            values=scenario["values"],
        )
        alternate_config = SourceConfig(alternate_document)
        alternate_incidence = decode_fixture_config(alternate_config, alternate_path)
        try:
            alternate_keys = row_native_keys_from_transport(
                alternate_config, incidence=alternate_incidence, batch_size=4
            )
            alternate_projection = build_governed_c11_projection(
                alternate_config, row_native_keys=alternate_keys
            )
            alternate_candidate = project_c11_candidate_from_config(
                alternate_config,
                alternate_projection,
                cells=tuple(alternate_incidence.iter_cells(4)),
                row_native_keys=alternate_keys,
                source_sha256=alternate_incidence.source_sha256,
                row_count=alternate_incidence.row_count,
            )
            alternate_release = validate_c11_source_release(alternate_candidate)
            assert alternate_release.release_ref.content_hash != base_release
            assert _respondent_refs(alternate_candidate) != base_respondents
            assert _event_refs(alternate_candidate) != base_events
        finally:
            alternate_incidence.close()

        # The ordinary full factory path agrees with the direct first-consumer path.
        full_release = build_validated_c11_release_from_config(
            scenario["config"], incidence=incidence, batch_size=4
        )
        assert full_release.release_ref.content_hash == base_release
        repository, repository_release = build_source_backed_c11_repository_from_config(
            scenario["config"], incidence, batch_size=4
        )
        assert repository_release.release_ref.content_hash == base_release
        assert repository is not None
    finally:
        incidence.close()


def test_b04_wrong_source_sha_refuses_before_decode(tmp_path):
    scenario = build_scenario(tmp_path / "sha", source_format="SAV")
    try:
        with pytest.raises(DecoderError, match="sha256 mismatch"):
            decode_sav(scenario["path"], expected_source_sha256="0" * 64)
        wrong_document = deepcopy(scenario["document"])
        wrong_document["binding"]["source_sha256"] = "0" * 64
        wrong_document["binding"]["source_snapshot_ref"]["content_hash"] = "0" * 64
        with pytest.raises(DecoderError, match="sha256 mismatch"):
            decode_fixture_config(SourceConfig(wrong_document), scenario["path"])
    finally:
        scenario["incidence"].close()


def test_b04_wrong_instrument_edition_and_projection_binding_refuse(tmp_path):
    scenario = build_scenario(tmp_path / "edition", source_format="SAV")
    incidence = scenario["incidence"]
    try:
        other_document = deepcopy(scenario["document"])
        other_document["binding"]["fixture_provenance"]["fixture_instrument_release_id"] = (
            "S1B_FIXTURE_INSTRUMENT_OTHER"
        )
        other_config = SourceConfig(other_document)
        other_projection = build_governed_c11_projection(
            other_config, row_native_keys=scenario["keys"]
        )
        with pytest.raises(SourceConfigurationBindingError, match="instrument edition"):
            verify_config_projection_binding(
                other_config,
                scenario["projection"],
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
        with pytest.raises(SourceConfigurationBindingError, match="instrument edition"):
            project_c11_candidate_from_config(
                other_config,
                scenario["projection"],
                cells=tuple(incidence.iter_cells(4)),
                row_native_keys=scenario["keys"],
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
        assert other_projection.instrument_release_id == "S1B_FIXTURE_INSTRUMENT_OTHER"
    finally:
        incidence.close()


def test_b04_caller_supplied_projection_cannot_change_config_mapping(tmp_path):
    scenario = build_scenario(tmp_path / "projection-mismatch", source_format="SAV")
    incidence = scenario["incidence"]
    try:
        changed_document = deepcopy(scenario["document"])
        changed_document["response_slots"][0]["values"][0]["response_state"] = "DK"
        changed_config = SourceConfig(changed_document)
        changed_projection = build_governed_c11_projection(
            changed_config, row_native_keys=scenario["keys"]
        )
        with pytest.raises(SourceConfigurationBindingError, match="response rules differ"):
            project_c11_candidate_from_config(
                scenario["config"],
                changed_projection,
                cells=tuple(incidence.iter_cells(4)),
                row_native_keys=scenario["keys"],
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )

        identity_document = deepcopy(scenario["document"])
        identity_document["authority"]["projection_identity_ref"] = ref(
            "C11_PROJECTION", "urn:rawlsing:s1b:other-projection"
        )
        identity_config = SourceConfig(identity_document)
        identity_projection = build_governed_c11_projection(
            identity_config, row_native_keys=scenario["keys"]
        )
        with pytest.raises(SourceConfigurationBindingError, match="projection identity reference"):
            project_c11_candidate_from_config(
                scenario["config"],
                identity_projection,
                cells=tuple(incidence.iter_cells(4)),
                row_native_keys=scenario["keys"],
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
    finally:
        incidence.close()


def test_b04_unqualified_encoding_and_unknown_config_keys_refuse(tmp_path):
    scenario = build_scenario(tmp_path / "encoding", source_format="SAV")
    try:
        with pytest.raises(DecoderError, match="encoding override is not in an exact SHA"):
            decode_sav(scenario["path"], encoding="latin1")
        with pytest.raises(DecoderError, match="automatic encoding guessing/fallback is forbidden"):
            decode_sav(scenario["path"], encoding="auto")

        allowlisted_sha = next(iter(COMPATIBILITY_ALLOWLIST))
        qualified = COMPATIBILITY_ALLOWLIST[allowlisted_sha]
        wrong = "BIG5" if qualified.lower() != "big5" else "latin1"
        path, file_sha, rows = write_fixture(
            tmp_path / "encoding-original", source_format="SAV", values=(1.0, 2.0)
        )
        document = make_config(
            source_format="SAV",
            active_source_sha256=file_sha,
            row_count=rows,
            values=(1.0, 2.0),
            original=True,
        )
        document["identity"]["expected_source_sha256"] = allowlisted_sha
        document["identity"]["source_snapshot_retention_ref"]["content_hash"] = allowlisted_sha
        document["binding"]["source_sha256"] = allowlisted_sha
        document["binding"]["source_snapshot_ref"]["content_hash"] = allowlisted_sha
        document["identity"]["reader"]["encoding"] = {
            "value": wrong,
            "sha256": allowlisted_sha,
            "authority_status": COMPATIBILITY_ONLY,
        }
        with pytest.raises(SourceConfigurationSchemaError, match="allowlisted encoding"):
            SourceConfig(document)
        document["identity"]["reader"]["encoding"]["value"] = qualified
        SourceConfig(document)
    finally:
        scenario["incidence"].close()


def test_b04_row_native_key_structure_refuses(tmp_path):
    scenario = build_scenario(tmp_path / "key", source_format="SAV")
    incidence = scenario["incidence"]
    try:
        bad_document = deepcopy(scenario["document"])
        bad_document["respondents"]["source_native_key_slot"] = {"ordinal": 99, "name": "absent"}
        bad_config = SourceConfig(bad_document)
        with pytest.raises(SourceConfigurationBindingError, match="absent from physical_slots"):
            row_native_keys_from_transport(bad_config, incidence=incidence)

        duplicate = list(scenario["cells"])
        key_cell = next(
            cell for cell in duplicate
            if cell.row_ordinal == 1 and cell.variable_name == "country"
        )
        duplicate.append(key_cell)
        stream = ExactPhysicalCellStream(
            source_sha256=scenario["source_sha"],
            row_count=scenario["rows"],
            cell_iter_factory=lambda: tuple(duplicate),
        )
        with pytest.raises(SourceConfigurationFactoryError, match="duplicate configured key cell"):
            row_native_keys_from_transport(scenario["config"], stream=stream)

        missing_rows = dict(scenario["keys"])
        missing_rows.pop(1)
        with pytest.raises(SourceConfigurationBindingError, match="requires row_native_keys"):
            build_governed_c11_projection(scenario["config"], row_native_keys=missing_rows)
    finally:
        incidence.close()

def test_b01_all_historical_r157_configs_and_unjoined_census_are_exact():
    listed = subprocess.run(
        [
            "git", "-C", str(ROOT), "ls-tree", "-r", "--name-only",
            R157_HISTORICAL_COMMIT, "rawlsing_next/source_configuration/data",
        ],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    config_files = [name for name in listed if name.endswith(".config.json")]
    assert len(config_files) == 51
    for config_file in sorted(config_files):
        blob = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{R157_HISTORICAL_COMMIT}:{config_file}"],
            capture_output=True, text=True, check=True,
        ).stdout
        validate_source_config(json.loads(blob))

    roster_blob = subprocess.run(
        [
            "git", "-C", str(ROOT), "show",
            f"{R157_HISTORICAL_COMMIT}:rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
        ],
        capture_output=True, text=True, check=True,
    ).stdout
    roster = json.loads(roster_blob)
    historical_unjoined = {
        (row["source_id"], implementation_id)
        for row in roster["sources"]
        for implementation_id in row.get("unmatched_relation_ids", ())
    }
    census = unjoined_r157_original_item_census()
    assert historical_unjoined == set(census["items"])
    assert roster["counts"]["unmatched_relation_ids"] == 26

def test_b01_fixture_stream_and_portable_library_are_real(tmp_path):
    scenario = build_scenario(tmp_path / "fixture-source", source_format="SAV")
    try:
        cells = []
        for cell in scenario["cells"]:
            cells.append({
                "row_ordinal": cell.row_ordinal,
                "variable_ordinal": cell.variable_ordinal,
                "variable_name": cell.variable_name,
                "raw_value": cell.raw_value,
                "missing_state": cell.missing_state.value,
                "source_missing_declaration": cell.source_missing_declaration,
            })
        fixture_document = {
            "schema": FIXTURE_SCHEMA_ID,
            "identity_class": "NONRESPONDENT_FIXTURE",
            "nonrespondent": True,
            "fixture_id": "S1B_PORTABLE_LIBRARY_FIXTURE",
            "row_count": scenario["rows"],
            "cells": cells,
        }
        fixture_document["fixture_source_sha256"] = fixture_document_sha256(fixture_document)
        stream = fixture_stream_from_document(fixture_document)
        assert stream.source_sha256 == fixture_document["fixture_source_sha256"]
        assert stream.row_count == scenario["rows"]

        fixture_config_document = make_config(
            source_format="SAV",
            active_source_sha256=stream.source_sha256,
            row_count=stream.row_count,
            values=scenario["values"],
        )
        fixture_config = SourceConfig(fixture_config_document)
        release = build_validated_c11_release_from_config(fixture_config, stream=stream)
        assert release.release_ref.content_hash
        assert release.source_artifact_ref.content_hash == stream.source_sha256

        original_document = make_config(
            source_format="SAV",
            active_source_sha256=sha256_text("S1B_LIBRARY_ORIGINAL_NOT_READ"),
            row_count=2,
            values=(1.0, 2.0),
            original=True,
        )
        original_path = tmp_path / "original.config.json"
        original_path.write_text(json.dumps(original_document), encoding="utf-8")
        fixture_config_path = tmp_path / "fixture.config.json"
        fixture_config_path.write_text(json.dumps(fixture_config_document), encoding="utf-8")
        fixture_path = tmp_path / "fixture.json"
        fixture_path.write_text(json.dumps(fixture_document), encoding="utf-8")
        index = {
            "schema": "PYAT_R157_SOURCE_LIBRARY_INDEX@1.0.0",
            "sources": [{
                "source_id": "SRC09",
                "family": "S1B_SYNTHETIC_NONRESPONDENT",
                "wave": "S1B",
                "lane": None,
                "status": "AVAILABLE_NATIVE_RECEIPT",
                "original_config_path": original_path.name,
                "original_config_file_sha256": config_file_sha256(original_path),
                "original_config_canonical_sha256": canonical_config_hash(original_document),
                "fixture_config_path": fixture_config_path.name,
                "fixture_config_file_sha256": config_file_sha256(fixture_config_path),
                "fixture_path": fixture_path.name,
                "fixture_file_sha256": config_file_sha256(fixture_path),
                "fixture_source_sha256": stream.source_sha256,
                "native_results_path": None,
                "native_results_file_sha256": None,
                "release_ref": None,
                "counts": {},
                "held": {},
                "details": [],
            }],
        }
        assert_exact_index_paths(index, root=tmp_path)
        index_path = tmp_path / "index.json"
        index_path.write_text(json.dumps(index), encoding="utf-8")
        library = SourceConfigLibrary(index_path=index_path, root=tmp_path)
        assert library.available_source_ids() == ("SRC09",)
        loaded_original = library.load_original("SRC09")
        assert loaded_original.config_purpose == "SOURCE_PREPARATION"
        loaded_fixture = library.load_fixture_config("SRC09")
        assert loaded_fixture.identity_class == "NONRESPONDENT_FIXTURE"
        loaded_stream = library.load_fixture_stream("SRC09")
        assert loaded_stream.source_sha256 == stream.source_sha256
        library_release = library.build_fixture_release("SRC09")
        assert library_release.release_ref.content_hash == release.release_ref.content_hash
        plan = library.original_plan(
            "SRC09",
            source_path="EXTERNAL_NOT_OPENED",
            host="s1b-host",
            purpose="s1b-purpose",
            consumer_use="s1b-consumer",
            semantic_use_scope=("S1B_SYNTHETIC_READ",),
        )
        assert plan["source_read_performed"] is False
        source_validation = library.validate_source("SRC09")
        assert source_validation["passed"] is False
        assert source_validation["historical_roster_comparison"].startswith("HOLD_EXTERNAL")
        assert source_validation["historical_roster_denominators_checked"] is False

        roster_checked = library.validate_source(
            "SRC09",
            historical_roster_entry={"physical_columns": 2, "original_items": 1},
        )
        assert roster_checked["passed"] is True
        assert roster_checked["historical_roster_comparison"] == "PASS"
        assert roster_checked["historical_roster_denominators_checked"] is True

        wrong_roster = library.validate_source(
            "SRC09",
            historical_roster_entry={"physical_columns": 3, "original_items": 1},
        )
        assert wrong_roster["passed"] is False
        assert wrong_roster["historical_roster_comparison"] == "FAIL"
        assert wrong_roster["checks"]["historical_physical_slots"] is False
        with pytest.raises(SourceLibraryError, match="ABSENT_CURRENT_PORT"):
            build_index(index_path=tmp_path / "unused-index.json")
    finally:
        scenario["incidence"].close()

def test_b04_row_native_key_witness_swap_is_refused(tmp_path):
    from dataclasses import replace

    from rawlsing_next.pre553_r157_projection_adapter import _question, _routing
    from rawlsing_next.pre553_source_backed_c11_facade import RowRespondentBinding

    scenario = build_scenario(tmp_path / "key-witness-swap", source_format="SAV")
    incidence = scenario["incidence"]
    try:
        projection = scenario["projection"]
        respondents = list(projection.respondents)
        key1 = respondents[0].source_native_respondent_key_ref_or_typed_absence
        key2 = respondents[1].source_native_respondent_key_ref_or_typed_absence
        respondents[0] = replace(
            respondents[0],
            source_native_respondent_key_ref_or_typed_absence=key2,
        )
        respondents[1] = replace(
            respondents[1],
            source_native_respondent_key_ref_or_typed_absence=key1,
        )
        row_bindings = tuple(
            RowRespondentBinding(
                binding.row_ordinal,
                respondents[binding.row_ordinal - 1].ref,
            )
            for binding in projection.row_bindings
        )
        questions = {
            section["question_id"]: _question(section)
            for section in scenario["document"]["questions"]
        }
        routing = _routing(
            scenario["document"],
            questions,
            tuple(respondents),
            active_rows=incidence.row_count,
        )
        tampered = replace(
            projection,
            respondents=tuple(respondents),
            row_bindings=row_bindings,
            routing=routing,
        )
        with pytest.raises(SourceConfigurationBindingError, match="respondents differ"):
            project_c11_candidate_from_config(
                scenario["config"],
                tampered,
                cells=tuple(incidence.iter_cells(4)),
                row_native_keys=scenario["keys"],
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
        with pytest.raises(SourceConfigurationBindingError, match="respondents differ"):
            project_c11_candidate_from_config(
                scenario["config"],
                tampered,
                cells=tuple(incidence.iter_cells(4)),
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
        streaming_candidate = project_c11_candidate_from_config(
            scenario["config"],
            projection,
            cells=iter(tuple(incidence.iter_cells(4))),
            row_native_keys=scenario["keys"],
            source_sha256=incidence.source_sha256,
            row_count=incidence.row_count,
        )
        assert streaming_candidate.respondent_events
        with pytest.raises(
            SourceConfigurationBindingError, match="requires row_native_keys"
        ):
            project_c11_candidate_from_config(
                scenario["config"],
                projection,
                cells=iter(tuple(incidence.iter_cells(4))),
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
    finally:
        incidence.close()

def test_b01_second_historical_full_nonrespondent_fixture_parity_src01(tmp_path):
    from rawlsing_next.pre553_r157_projection_adapter import (
        load_fixture_stream,
        load_source_config,
    )

    commit = R157_HISTORICAL_COMMIT
    paths = {
        "config": "rawlsing_next/source_configuration/data/SRC01/SRC01.full.fixture.config.json",
        "fixture": "source_pre553_validation/SRC01/SRC01.full.fixture.json",
        "native": "source_pre553_validation/SRC01/FULL_NATIVE_RESULTS.json",
    }
    blobs = {}
    for name, relative in paths.items():
        blobs[name] = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{commit}:{relative}"],
            capture_output=True, check=True,
        ).stdout
    config_path = tmp_path / "SRC01.full.fixture.config.json"
    fixture_path = tmp_path / "SRC01.full.fixture.json"
    config_path.write_bytes(blobs["config"])
    fixture_path.write_bytes(blobs["fixture"])
    native = json.loads(blobs["native"])
    config = load_source_config(config_path)
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
    release = validate_c11_source_release(candidate)
    expected = native["full_fixture_native_validation"]
    assert release.release_ref.content_hash == expected["release_ref"]["content_hash"]
    assert release.replay_manifest.ref.content_hash == expected["replay_manifest_ref"]["content_hash"]
    assert stream.source_sha256 == native["fixture_source_sha256"]
    full_release = build_validated_c11_release_from_config(config, stream=stream)
    assert full_release.release_ref.content_hash == expected["release_ref"]["content_hash"]

@pytest.mark.parametrize("field,match", (
    ("universes", "universes differ"),
    ("questions", "question bindings differ"),
    ("required_authority_refs", "required authority closure differs"),
))
def test_b04_duplicate_config_projection_objects_are_refused(tmp_path, field, match):
    scenario = build_scenario(tmp_path / f"duplicate-{field}", source_format="SAV")
    incidence = scenario["incidence"]
    try:
        projection = scenario["projection"]
        value = getattr(projection, field)
        tampered = replace(projection, **{field: value + (value[0],)})
        with pytest.raises(SourceConfigurationBindingError, match=match):
            project_c11_candidate_from_config(
                scenario["config"],
                tampered,
                cells=tuple(incidence.iter_cells(4)),
                row_native_keys=scenario["keys"],
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
    finally:
        incidence.close()
