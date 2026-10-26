"""R145 focused metadata-only source-package binder checks."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))
if str(RUNTIME.parents[2]) not in sys.path:
    sys.path.insert(0, str(RUNTIME.parents[2]))

import source_package_binder as binder  # noqa: E402

SCOPE = Path(".r61/r145-current-source-packages/inputs/METADATA_INPUTS.json")


def _specs():
    return binder.load_metadata_scope(SCOPE)


def _receipt(spec, **changes):
    base = {
        "schema": "PYAT_R145_AUTHORIZED_METADATA_RECEIPT@1",
        "source_id": spec.source_id, "family": spec.family, "wave": spec.wave,
        "edition_sha256": "a" * 64, "source_format": spec.source_format,
        "dictionary_sha256": spec.sha256,
        "header_variables": ["X", "Y"],
        "row_count": 2,
        "authority_state": "EXTERNALLY_AUTHORIZED_METADATA_ONLY",
        "issuer_ref": {"kind": "ISSUER", "object_id": "urn:r145:issuer",
                       "content_hash": "b" * 64},
        "source_identity_receipt_ref": {"kind": "SOURCE_IDENTITY_RECEIPT",
                                        "object_id": "urn:r145:receipt",
                                        "content_hash": "c" * 64},
    }
    base.update(changes)
    return base


def _all_accounts(spec):
    _prep, accounts, _freeze = binder.build_preparation(spec)
    return accounts


def test_all_three_independent_dictionaries_full_row_accounting():
    specs = _specs()
    assert [spec.source_id for spec in specs] == ["SRC23", "SRC22", "SRC30"]
    assert [spec.codebook_rows for spec in specs] == [980, 1018, 1319]
    for spec in specs:
        preparation, accounts, freeze = binder.build_preparation(spec)
        assert len(accounts) == spec.codebook_rows == preparation["row_accounting"]["total_rows"]
        assert sum(preparation["row_accounting"]["role_counts"].values()) == spec.codebook_rows
        assert all(account["retained"] is True for account in accounts)
        assert len({account["var_name"] for account in accounts}) == spec.codebook_rows
        assert len({account["row_identity"] for account in accounts}) == spec.codebook_rows
        assert preparation["survey_file_touched"] is False
        assert preparation["source_unit"].startswith(("PERSON_RESPONDENT" if spec.family == "GSS" else "HOUSEHOLD_ID"))
        assert preparation["edition_sha256"] is None
        assert preparation["edition_sha256_status"].startswith("PENDING_")
        assert preparation["source_read_request_template"]["read_operation"] == "SOURCE_RESPONSE_DECODE"
        assert preparation["source_read_request_template"]["physical_read_extent"] == "EXACT_FILE"
        assert freeze.kind == "R145_METADATA_FREEZE"
        assert [row["consumer_id"] for row in preparation["consumer_requirements"]] == [
            "F1_EMPIRICAL_CLOSURE", "F2_DISCOVERY_AND_NO_DROP",
            "F3_M1_LEARNED_DISPOSITION", "F4_FF_V553_CONFRONTATION"]


def test_metadata_tamper_and_column_missing_refuse_without_raw_source(tmp_path):
    spec = _specs()[0]
    raw = spec.metadata_path.read_bytes()
    bad = tmp_path / "bad.csv"
    bad.write_bytes(raw + b"\n")
    bad_spec = binder.DictionarySpec(
        spec.source_id, spec.family, spec.wave, bad, spec.sha256,
        spec.bytes, spec.codebook_rows, spec.survey_locator, spec.source_format, spec.scope)
    with pytest.raises(binder.PackageBindingRefusal, match="DICTIONARY_HASH_OR_BYTES_MISMATCH"):
        binder.build_preparation(bad_spec)
    truncated = tmp_path / "truncated.csv"
    rows = list(csv.reader(raw.decode("utf-8-sig").splitlines()))
    rows[0] = [name for name in rows[0] if name != "var_name"]
    with truncated.open("w", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerows(rows)
    trunc_spec = binder.DictionarySpec(
        spec.source_id, spec.family, spec.wave, truncated,
        hashlib.sha256(truncated.read_bytes()).hexdigest(), truncated.stat().st_size,
        spec.codebook_rows, spec.survey_locator, spec.source_format, spec.scope)
    with pytest.raises(binder.PackageBindingRefusal, match="DICTIONARY_COLUMNS_MISSING"):
        binder.build_preparation(trunc_spec)


def test_row_identity_tamper_changes_hash_and_stays_retained():
    spec = _specs()[0]
    _prep, accounts, _freeze = binder.build_preparation(spec)
    account = accounts[0]
    row = {"var_name": account["var_name"], "source": "GSS", "wave": "2024"}
    changed = dict(row, var_name="TAMPERED")
    assert binder._row_account(spec, 1, row)["row_hash"] != binder._row_account(spec, 1, changed)["row_hash"]
    assert account["retained"] is True


def test_authorized_metadata_receipt_binds_native_identity_and_refuses_wrong(tmp_path):
    spec = _specs()[0]
    prep, _accounts, _freeze = binder.build_preparation(spec)
    receipt = _receipt(spec)
    bound = binder.bind_authorized_metadata_receipt(
        spec, receipt, codebook_variables=[account["var_name"] for account in _all_accounts(spec)])
    assert bound["native_source_identity"]["declared_sha256"] == "a" * 64
    assert bound["source_read_grant_present"] is False
    assert bound["response_decode_authorized"] is False
    for changes in (
        {"authority_state": "CALLER_LABEL"},
        {"dictionary_sha256": "0" * 64},
        {"source_id": "FOREIGN"},
        {"edition_sha256": "x"},
        {"header_variables": []},
        {"row_count": 0},
    ):
        with pytest.raises(binder.PackageBindingRefusal):
            binder.bind_authorized_metadata_receipt(
                spec, _receipt(spec, **changes),
                codebook_variables=[account["var_name"] for account in _all_accounts(spec)])
    missing = _receipt(spec)
    missing.pop("issuer_ref")
    with pytest.raises(binder.PackageBindingRefusal, match="AUTHORIZED_METADATA_RECEIPT_MISSING"):
        binder.bind_authorized_metadata_receipt(
            spec, missing, codebook_variables=[account["var_name"] for account in _all_accounts(spec)])


def test_no_decoder_or_survey_file_transport_is_invoked(monkeypatch):
    spec = _specs()[0]
    calls = {"decode": 0}
    monkeypatch.setattr(
        "rawlsing_next.pre553_physical_decoder.decode_sav",
        lambda *a, **k: calls.__setitem__("decode", calls["decode"] + 1))
    monkeypatch.setattr(
        "rawlsing_next.pre553_physical_decoder.decode_dta",
        lambda *a, **k: calls.__setitem__("decode", calls["decode"] + 1))
    preparation, _accounts, _freeze = binder.build_preparation(spec)
    assert calls["decode"] == 0
    assert preparation["survey_file_touched"] is False
    assert preparation["source_read_request_template"]["source_sha256"] is None


def test_summary_records_all_rows_and_no_source_claim(tmp_path):
    summary = binder.build_all(SCOPE, tmp_path)
    assert summary["source_count"] == 3
    assert sum(row["rows"] for row in summary["sources"]) == 3317
    assert summary["survey_files_touched"] == 0
    assert summary["source_read_grants_created"] == 0
    assert summary["native_preimage_bundles_created"] == 0
    for row in summary["sources"]:
        assert (tmp_path / row["preparation_record"]).is_file()
        assert (tmp_path / row["row_accounting"]).is_file()
