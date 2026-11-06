"""Current-base R157 source-pack port: pinned resources, selector and ABI."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from rawlsing_next.source_configuration import factory, reader
from rawlsing_next.source_configuration.errors import (
    SourceConfigurationBindingError,
    SourceConfigurationSchemaError,
)
from rawlsing_next.source_configuration.library import (
    SourceArtifactError,
    SourceConfigLibrary,
    SourceNotPrepared,
    build_index,
)
from rawlsing_next.source_configuration.provider import GitObjectProvider, ProviderError
from rawlsing_next.source_configuration.schema import (
    load_source_config,
    load_source_config_bytes,
    validate_source_config,
)

ROOT = Path(__file__).resolve().parents[2]
BINDINGS = ROOT / "rawlsing_next/source_configuration/source_locator_bindings.json"
ABI = ROOT / "rawlsing_next/source_configuration/ABI.json"


def _library(tmp_path: Path) -> SourceConfigLibrary:
    index = build_index(index_path=tmp_path / "index.json", sqlite_path=tmp_path / "index.sqlite")
    assert index["counts"]["available"] == 35
    return SourceConfigLibrary(index_path=tmp_path / "index.json")


def test_pinned_r157_index_preserves_all35_denominators(tmp_path: Path):
    index = build_index(index_path=tmp_path / "index.json", sqlite_path=tmp_path / "index.sqlite")
    assert index["counts"] == {
        "available": 35,
        "available_original_items": 18_276,
        "available_physical_slots": 18_413,
        "other_incomplete": 0,
        "pending": 0,
    }
    assert index["baseline"]["exact_relation_matches"] == 18_250
    assert index["baseline"]["unmatched_relation_ids"] == 26
    assert len(index["sources"]) == 35
    assert index["pending_source_ids"] == []


def test_source_root_override_changes_resolution_not_artifact_root(tmp_path: Path):
    library = _library(tmp_path)
    root_a = tmp_path / "root-a"
    root_b = tmp_path / "root-b"
    root_a.mkdir()
    root_b.mkdir()
    selected_a = library.select("SRC01", source_root=root_a)
    selected_b = library.select("SRC01", source_root=root_b)
    assert selected_a["source_resolution"]["status"] == "RESOLVED_UNDER_EFFECTIVE_ROOT"
    assert selected_a["source_resolution"]["effective_source_root"] == str(root_a.resolve())
    assert selected_b["source_resolution"]["effective_source_root"] == str(root_b.resolve())
    assert selected_a["source_resolution"]["resolved_source_path"] != selected_b["source_resolution"]["resolved_source_path"]
    assert selected_a["source_resolution"]["relative_path"] == "Afro Barometer Round 1.sav"
    assert selected_a["source_read_performed"] is False
    assert selected_a["original_config_path"].startswith("rawlsing_next/source_configuration/data/")
    plan = library.original_plan(
        "SRC01", source_root=root_b, host="test-host", purpose="TEST",
        consumer_use="TEST", semantic_use_scope=("TEST",))
    assert plan["source_path"].startswith(str(root_b.resolve()))
    assert plan["source_read_performed"] is False
    assert plan["original_workload_issued"] is False
    with pytest.raises(Exception, match="NO_SOURCE_ROOT_OVERRIDE"):
        library.original_plan(
            "SRC01", host="test-host", purpose="TEST",
            consumer_use="TEST", semantic_use_scope=("TEST",))


def test_reader_uses_effective_source_root_before_decoder(tmp_path: Path, monkeypatch):
    library = _library(tmp_path)
    config = library.load_original("SRC01")
    captured = {}

    def fake_decode(**kwargs):
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(reader, "decode_with_source_read_permission", fake_decode)
    root = tmp_path / "effective-root"
    reader.decode_config_with_source_read_permission(
        config, source_root=root, source_relative_path="nested/SRC01.sav",
        resolver=object(), host="h", purpose="p", consumer_use="c",
        semantic_use_scope=("s",))
    assert captured["source_path"] == (root / "nested/SRC01.sav").resolve()
    assert str(root.resolve()) in str(captured["source_path"])
    with pytest.raises(SourceConfigurationBindingError, match="SOURCE_ROOT_OVERRIDE_REQUIRED"):
        reader.decode_config_with_source_read_permission(
            config, resolver=object(), host="h", purpose="p", consumer_use="c",
            semantic_use_scope=("s",))


def test_locator_bindings_are_relative_and_cover_35_sources():
    document = json.loads(BINDINGS.read_text(encoding="utf-8"))
    rows = document["rows"]
    assert len(rows) == 35
    assert {row["source_id"] for row in rows} == {f"SRC{i:02d}" for i in range(1, 36)}
    for row in rows:
        assert not Path(row["relative_path"]).is_absolute()
        assert ".." not in Path(row["relative_path"]).parts
        assert len(row["source_sha256"]) == 64
        assert row["presence_grade"] == "LOCAL_BYTES_PRESENT_EXACT_SHA"


def test_wrong_sha_and_unknown_source_are_refused(tmp_path: Path):
    index = build_index(index_path=tmp_path / "index.json", sqlite_path=tmp_path / "index.sqlite")
    document = json.loads((tmp_path / "index.json").read_text(encoding="utf-8"))
    row = next(item for item in document["sources"] if item["source_id"] == "SRC01")
    row["original_config_file_sha256"] = "f" * 64
    wrong = tmp_path / "wrong-index.json"
    wrong.write_text(json.dumps(document), encoding="utf-8")
    library = SourceConfigLibrary(index_path=wrong, provider=GitObjectProvider())
    with pytest.raises(SourceArtifactError, match="SHA mismatch"):
        library.load_original("SRC01")
    with pytest.raises(SourceNotPrepared, match="UNKNOWN_SOURCE"):
        library.load_original("SRC99")
    provider = GitObjectProvider()
    assert provider.exists("rawlsing_next/source_configuration/data/SRC01/SRC01.config.json")
    assert not provider.exists("rawlsing_next/source_configuration/data/SRC01/NONEXISTENT.json")
    with pytest.raises(ProviderError):
        provider.read_bytes("rawlsing_next/source_configuration/data/SRC01/NONEXISTENT.json")


def test_actual_first_consumer_and_frozen_abi(tmp_path: Path):
    library = _library(tmp_path)
    release = library.build_fixture_release("SRC01")
    row = library.record("SRC01")
    assert release.release_ref.content_hash == row["release_ref"]["content_hash"]
    assert release.release_ref.kind == "C11LogicalRelease"
    assert set(release.m01_m18_coverage) == {f"M{i:02d}" for i in range(1, 19)}
    abi = json.loads(ABI.read_text(encoding="utf-8"))
    assert abi["schema"] == "PYAT_R157_SOURCE_PACK_ABI@1.0.0"
    assert abi["pinned_r157_commit"] == "1924499ef52403a0f331b8aff9b7c7eff99bf1e2"
    assert abi["first_consumer"]["callable"].endswith("SourceConfigLibrary.build_fixture_release")
    assert abi["source_root_contract"]["absolute_paths_hardcoded"] is False
    assert "source_root" in abi["library"]["methods"]["select"]
    assert "source_root" in abi["reader"]["resolve_source_path_from_config"]
    assert callable(factory.build_governed_c11_projection)
    assert callable(factory.build_validated_c11_release_from_config)


def test_occurrence_and_wrong_physical_slot_are_refused():
    doc = json.loads((ROOT / "source_pre553_validation/foundation/examples/SRC09_q101_fixture.config.json").read_text(encoding="utf-8"))
    wrong_slot = copy.deepcopy(doc)
    wrong_slot["response_slots"][0]["slot"]["ordinal"] = 9999
    with pytest.raises(SourceConfigurationSchemaError, match="unknown physical slot"):
        validate_source_config(wrong_slot)
    no_occurrence = copy.deepcopy(doc)
    no_occurrence["response_slots"][0]["values"][0]["occurrences"] = []
    with pytest.raises(SourceConfigurationSchemaError):
        validate_source_config(no_occurrence)


def test_source_specific_exceptions_are_preserved_in_pinned_pack():
    provider = GitObjectProvider()
    def config(path):
        return load_source_config_bytes(provider.read_bytes(path), path=path)
    src25 = config("rawlsing_next/source_configuration/data/SRC25/source.config.json")
    src26 = config("rawlsing_next/source_configuration/data/SRC26/source.config.json")
    assert len(src26.document["items"]) == 195
    assert len(src26.document["physical_slots"]) == 332
    assert src25.document["items"][0]["source_variable_code"] != src26.document["items"][0]["source_variable_code"]
    assert sum(1 for item in src25.document["items"] if item.get("relation")) == 414
    assert sum(1 for item in src26.document["items"] if item.get("relation")) == 190
    lits = config("rawlsing_next/source_configuration/data/SRC27/src27.config.json")
    assert lits.document["respondents"]["subject_unit"] == "HOUSEHOLD"
    assert any(item["source_variable_code"] == "q101_1" for item in lits.document["items"])
    src13 = config("rawlsing_next/source_configuration/data/SRC13/SRC13.config.json")
    assert src13.document["identity"]["reader"]["encoding"]["value"] == "latin1"
    assert src13.document["respondents"]["source_native_key_slot"] == {"ordinal": 5, "name": "id_cocas"}
