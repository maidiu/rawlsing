"""P5 portable library/index/CLI contract tests."""
from __future__ import annotations

import json
from pathlib import Path
import sqlite3

import pytest

from rawlsing_next.source_configuration.library import (
    SourceArtifactError,
    SourceConfigLibrary,
    SourceNotPrepared,
    assert_exact_index_paths,
    build_index,
)


@pytest.fixture(scope="module")
def index_dir(tmp_path_factory):
    target = tmp_path_factory.mktemp("p5-index")
    index = build_index(index_path=target / "index.json", sqlite_path=target / "index.sqlite")
    return target, index


def test_index_has_32_available_and_exactly_3_pending(index_dir):
    _, index = index_dir
    assert index["baseline"]["sources"] == 35
    assert index["baseline"]["original_items"] == 18_276
    assert index["baseline"]["physical_columns"] == 18_413
    assert index["counts"]["available"] == 32
    assert index["counts"]["pending"] == 3
    assert index["counts"]["other_incomplete"] == 0
    assert index["pending_source_ids"] == ["SRC33", "SRC34", "SRC35"]
    assert index["counts"]["available_original_items"] == 17_057
    assert index["counts"]["available_physical_slots"] == 17_194


def test_library_loads_full_original_and_fixture_identity(index_dir):
    target, _ = index_dir
    library = SourceConfigLibrary(index_path=target / "index.json")
    assert len(library.available_source_ids()) == 32
    original = library.load_original("SRC01")
    fixture = library.load_fixture_config("SRC01")
    stream = library.load_fixture_stream("SRC01")
    assert original.config_purpose == "SOURCE_PREPARATION"
    assert fixture.config_purpose == "NONRESPONDENT_FIXTURE"
    assert fixture.identity_class == "NONRESPONDENT_FIXTURE"
    assert fixture.active_source_sha256 == stream.source_sha256
    assert fixture.active_row_count == stream.row_count
    assert len(original.document["physical_slots"]) == 144
    assert len(original.document["items"]) == 144


def test_all_available_configs_validate_without_original_read(index_dir):
    target, _ = index_dir
    library = SourceConfigLibrary(index_path=target / "index.json")
    for source_id in library.available_source_ids():
        result = library.validate_source(source_id)
        assert result["passed"], (source_id, result["checks"])


def test_fixture_native_call_matches_recorded_receipt(index_dir):
    target, _ = index_dir
    library = SourceConfigLibrary(index_path=target / "index.json")
    release = library.build_fixture_release("SRC01")
    row = library.record("SRC01")
    assert release.release_ref.content_hash == row["release_ref"]["content_hash"]
    assert release.release_ref.kind == "C11LogicalRelease"


def test_pending_source_is_not_accepted_or_materialized(index_dir):
    target, _ = index_dir
    library = SourceConfigLibrary(index_path=target / "index.json")
    with pytest.raises(SourceNotPrepared, match="PENDING_ACCEPTED_RETURN"):
        library.load_original("SRC33")
    with pytest.raises(SourceNotPrepared, match="PENDING_ACCEPTED_RETURN"):
        library.load_fixture_config("SRC33")


def test_original_plan_is_explicitly_unexecuted(index_dir, tmp_path):
    target, _ = index_dir
    library = SourceConfigLibrary(index_path=target / "index.json")
    plan = library.original_plan(
        "SRC01", source_path=str(tmp_path / "never-opened.sav"),
        host="p5-test", purpose="P5_TEST", consumer_use="P5_TEST",
        semantic_use_scope=("P5_TEST",))
    assert plan["source_read_performed"] is False
    assert plan["original_workload_issued"] is False
    assert plan["source_read_request"]["source_sha256"] == "6c9869a7cc7321cc74efb708835e21c8b65286a25c76deac45aba84d75697ee2"
    assert plan["reader_configuration"]["encoding"] is None


def test_index_is_portable_and_has_no_private_worktree_paths(index_dir):
    target, _ = index_dir
    text = (target / "index.json").read_text(encoding="utf-8")
    for fragment in ("/Users/", ".r61", "Rawlsing_Worktrees", "Rawlsing_Authority_Document_Archive"):
        assert fragment not in text
    json.loads(text)


def test_sqlite_index_lookup(index_dir):
    target, _ = index_dir
    con = sqlite3.connect(target / "index.sqlite")
    try:
        assert con.execute("select count(*) from sources").fetchone()[0] == 35
        assert con.execute("select count(*) from sources where status='AVAILABLE_NATIVE_RECEIPT'").fetchone()[0] == 32
        assert con.execute("select count(*) from sources where status='PENDING_ACCEPTED_RETURN'").fetchone()[0] == 3
        row = con.execute("select source_id,status,release_content_hash from sources where source_id='SRC01'").fetchone()
        assert row[0] == "SRC01"
        assert row[1] == "AVAILABLE_NATIVE_RECEIPT"
        assert len(row[2]) == 64
        for source_id in ("SRC27", "SRC28", "SRC29", "SRC30"):
            paths = con.execute(
                "select original_config_path,native_results_path from sources where source_id=?",
                (source_id,)).fetchone()
            assert paths[0].endswith(f"/src{source_id[3:]}.config.json")
            assert paths[1].endswith("/validation_results.json")
    finally:
        con.close()


def test_cold_load_from_unrelated_cwd(index_dir, tmp_path, monkeypatch):
    target, _ = index_dir
    monkeypatch.chdir(tmp_path)
    library = SourceConfigLibrary(index_path=target / "index.json")
    assert library.record("SRC04")["status"] == "AVAILABLE_NATIVE_RECEIPT"
    assert library.load_original("SRC04").source_id == "SRC04"


def _assert_exact_directory_entry(root: Path, relative: str) -> None:
    current = root
    for part in Path(relative).parts:
        names = {entry.name for entry in current.iterdir()}
        assert part in names, (relative, part, sorted(names))
        current = current / part
    assert current.is_file(), relative


def test_every_indexed_artifact_path_matches_real_exact_case(index_dir):
    target, index = index_dir
    from rawlsing_next.source_configuration.library import ROOT

    assert_exact_index_paths(index, ROOT)
    for row in index["sources"]:
        for field in ("original_config_path", "fixture_config_path", "fixture_path", "native_results_path"):
            relative = row.get(field)
            if relative:
                _assert_exact_directory_entry(ROOT, relative)


def test_lits_paths_preserve_committed_lowercase_spelling(index_dir):
    _, index = index_dir
    rows = {row["source_id"]: row for row in index["sources"]}
    for source_id in ("SRC27", "SRC28", "SRC29", "SRC30"):
        lower = source_id.lower()
        assert rows[source_id]["original_config_path"].endswith(f"/{lower}.config.json")
        assert rows[source_id]["native_results_path"].endswith("/validation_results.json")


def test_library_rejects_wrong_case_serialized_path(index_dir, tmp_path):
    target, _ = index_dir
    document = json.loads((target / "index.json").read_text(encoding="utf-8"))
    row = next(item for item in document["sources"] if item["source_id"] == "SRC27")
    row["original_config_path"] = row["original_config_path"].replace("src27", "SRC27")
    wrong = tmp_path / "wrong-case-index.json"
    wrong.write_text(json.dumps(document), encoding="utf-8")
    library = SourceConfigLibrary(index_path=wrong)
    with pytest.raises(SourceArtifactError, match="non-exact path component"):
        library.load_original("SRC27")
