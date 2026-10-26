"""R154 focused store, reconciliation, native-load and cold-reload checks."""
from __future__ import annotations

import json
import shutil
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))
if str(RUNTIME.parents[2]) not in sys.path:
    sys.path.insert(0, str(RUNTIME.parents[2]))

from r154_load import LoadRefusal, build_native_workload, load_all, load_source  # noqa: E402
from rawlsing_next.pre553_issued_workload import OriginalWaveIdentity  # noqa: E402
from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceIdentity  # noqa: E402

DB = ROOT / "store" / "r154_all35.sqlite"


@pytest.fixture(scope="module")
def store():
    assert DB.is_file(), "R154 store is missing"
    return DB


def test_all35_physical_columns_and_codebook_rows_accounted(store):
    con = sqlite3.connect(store)
    try:
        assert con.execute("select count(*) from sources").fetchone()[0] == 35
        assert con.execute("select count(*) from physical_columns").fetchone()[0] == 18413
        assert con.execute("select count(*) from codebook_rows").fetchone()[0] == 18276
        assert con.execute("select count(*) from evidence").fetchone()[0] == 4493
        assert con.execute("select count(*) from requirements").fetchone()[0] == 15
        assert con.execute("select count(*) from source_requirements").fetchone()[0] == 35 * 15
        assert con.execute("select count(*) from native_packages").fetchone()[0] == 35
        assert con.execute("select count(*) from tasks where state='RUNNING'").fetchone()[0] == 0
        assert con.execute("select count(*) from tasks where state='BLOCKED'").fetchone()[0] == 0
        assert con.execute("select count(*) from tasks where state='DONE'").fetchone()[0] == 178
        assert con.execute("select count(*) from tasks where state='DONE_WITH_EXACT_UNRESOLVED_FIELDS'").fetchone()[0] == 35
        assert con.execute("select count(*) from tasks where task='BOOTSTRAP' and state='DONE'").fetchone()[0] == 1
        assert con.execute("select count(*) from tasks where task in ('ASSEMBLE','VERIFY_DELIVER') and state='DONE'").fetchone()[0] == 2
        assert con.execute("select count(*) from sourceprep_artifacts").fetchone()[0] == 43
        assert con.execute("select count(*) from requirements where id='FIELD_FORGE'").fetchone()[0] == 0
        po = sum(len(json.loads(r[0])) for r in con.execute("select physical_only from reconciliation"))
        co = sum(len(json.loads(r[0])) for r in con.execute("select codebook_only from reconciliation"))
        assert (po, co) == (538, 401)
    finally:
        con.close()


def test_physical_receipts_and_retry_evidence():
    physical = sorted((ROOT / "records" / "physical").glob("SRC*_PHYSICAL_METADATA.json"))
    assert len(physical) == 35
    for p in physical:
        d = json.loads(p.read_text())
        assert d["response_rows_read_or_exported"] is False
        assert d["state"] in {"METADATA_INSPECTED", "METADATA_INSPECTED_LATIN1_COMPAT_PHYSICAL_ONLY__SEMANTIC_AUTHORITY_FALSE"}
        assert len(d["sha256"]) == 64
    s13 = json.loads((ROOT / "records" / "physical" / "SRC13_PHYSICAL_METADATA.json").read_text())
    s14 = json.loads((ROOT / "records" / "physical" / "SRC14_PHYSICAL_METADATA.json").read_text())
    assert s13["state"].startswith("METADATA_INSPECTED_LATIN1")
    assert s14["state"].startswith("METADATA_INSPECTED_LATIN1")
    assert s13["sha256"] == "6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8a"
    assert s14["sha256"] == "5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379"


def test_native_loader_constructs_actual_all35_inputs(store):
    packages = load_all(store)
    assert len(packages) == 35
    assert [p.source_id for p in packages] == [f"SRC{i:02d}" for i in range(1, 36)]
    for p in packages:
        assert isinstance(p.native_source_identity, NativeSourceIdentity)
        assert isinstance(p.original_wave_identity, OriginalWaveIdentity)
        assert p.selected_source_rule_package.schema.startswith("PRE553_SELECTED")
        assert p.physical_column_count > 0
        assert p.codebook_row_count > 0
        assert p.current_grant.get("u_root") is None
        assert p.current_grant.get("e_pre_root") is None
        assert p.native_workload_status.startswith("BLOCKED")
    with pytest.raises(LoadRefusal, match="CURRENT_SOURCE_READ_GRANT_REQUIRED"):
        build_native_workload("SRC01", store)


def test_cold_store_and_export_reload(tmp_path, store):
    cold = tmp_path / "r154_cold.sqlite"
    shutil.copyfile(store, cold)
    packages = load_all(cold)
    assert len(packages) == 35
    assert load_source("SRC23", cold).source_id == "SRC23"
    exports = sorted((ROOT / "exports").glob("SRC*.json"))
    assert len(exports) == 35
    assert (ROOT / "exports" / "SUMMARY.json").is_file()
    assert (ROOT / "exports" / "TASKS.json").is_file()
    con = sqlite3.connect(cold)
    con.execute("delete from native_packages where source_id='SRC35'")
    con.commit(); con.close()
    with pytest.raises(LoadRefusal, match="NATIVE_PACKAGE_MISSING"):
        load_source("SRC35", cold)


def test_no_decoder_or_survey_call_on_load(store, monkeypatch):
    calls = {"decode": 0}
    def decode(*args, **kwargs):
        calls["decode"] += 1
        raise AssertionError("decoder called")
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_sav", decode)
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_dta", decode)
    load_all(store)
    assert calls["decode"] == 0
