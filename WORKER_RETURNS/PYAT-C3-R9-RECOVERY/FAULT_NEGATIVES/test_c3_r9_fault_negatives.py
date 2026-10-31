"""Sourcefree C3/R9 fault negatives against the current PRE-MAIN receivers.

This is evidence-only.  It never opens a survey source, never issues a warrant,
and never imports or resurrects the historical C3/R9 production tree.  The
TEST_ONLY resolver below is the current R61 test double and is labelled as
such; it is not a production issuer and no production issuer is claimed.
"""
from __future__ import annotations

from dataclasses import fields, replace
import datetime as dt
import hashlib
import importlib
import pathlib

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next import pre553_physical_decoder as decoder
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_issued_workload import WorkloadAdmissionError, admit
from rawlsing_next.pre553_native_workload_binding import (
    TestOnlyDecisionResolver, WorkloadBindingRefusal,
)
from rawlsing_next.pre553_physical_decoder import (
    DecoderError, PhysicalMissingState, decode_sav,
)
from rawlsing_next.pre553_r5_codec import R5CodecError, R5OpaqueValue, R5TypedValueCodec
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key
from rawlsing_next.pre553_universal_workload import (
    compile_universal_workload, execute_universal_workload,
)
from rawlsing_next.tests.test_universal_workload import (
    AS_OF, HOST, PURPOSE, build_s3, s3_rows,
)

G01_FLOAT_KEY = "47f141e43fb2a330ebd2286a0bb658eaa6320768d1bb75a0b969761731ace7bd"
G01_DECLARED_SHA_BIG5 = "ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2"


def _sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_sav(path: pathlib.Path, rows, **kwargs) -> pathlib.Path:
    pyreadstat.write_sav(pd.DataFrame(rows), str(path), **kwargs)
    return path


def _current_bundle(tmp_path: pathlib.Path):
    path = tmp_path / "c3r9_current.sav"
    bundle = build_s3(path, s3_rows(respondents=4, occasions=2))
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE
    )
    return bundle, compilation


def _issued(compilation):
    return next(item.issued for item in compilation.compiled if item.issued is not None)


def test_current_universal_receiver_positive_baseline(tmp_path):
    bundle, compilation = _current_bundle(tmp_path)
    result = execute_universal_workload(
        compilation=compilation, source_factory=lambda _ref: bundle.physical_stream
    )
    assert result.anti_join()["no_drop_ok"] is True
    assert result.native_results
    assert result.receipt_refs
    assert result.fact_refs
    assert not result.failed


def test_g01_nine_surface_authority_module_absent_and_type_fault_restores():
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(
            "rawlsing_next.closed35_g01_sav_numeric_representation_authority"
        )

    float_key = physical_value_binding_key(
        float(1), PhysicalMissingState.OBSERVED_STORAGE_VALUE, None
    )
    int_key = physical_value_binding_key(
        1, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None
    )
    assert float_key == G01_FLOAT_KEY
    assert int_key != G01_FLOAT_KEY

    def named_g01_receiving_assertion(observed_key: str) -> None:
        assert observed_key == G01_FLOAT_KEY

    with pytest.raises(AssertionError):
        named_g01_receiving_assertion(int_key)
    named_g01_receiving_assertion(float_key)


def test_wrong_sav_raw_geometry_changes_digest_and_baseline_restores(tmp_path):
    good = _write_sav(tmp_path / "f82.sav", {"X": [1.0, 2.0]}, variable_format={"X": "F8.2"})
    wrong = _write_sav(tmp_path / "f80.sav", {"X": [1.0, 2.0]}, variable_format={"X": "F8.0"})
    good_inc = decode_sav(good)
    wrong_inc = decode_sav(wrong)
    try:
        good_digest = good_inc.physical_metadata_digest
        wrong_digest = wrong_inc.physical_metadata_digest
        assert good_inc.variables[0].display_metadata["format"] == "F8.2"
        assert wrong_inc.variables[0].display_metadata["format"] == "F8.0"
        assert good_digest != wrong_digest

        def named_geometry_receiving_assertion(observed: str) -> None:
            assert observed == good_digest

        with pytest.raises(AssertionError):
            named_geometry_receiving_assertion(wrong_digest)
        named_geometry_receiving_assertion(good_digest)
    finally:
        good_inc.close()
        wrong_inc.close()


def test_d01_declared_encoding_lane_absent_and_compatibility_lane_conserved(tmp_path):
    assert not hasattr(decoder, "DECLARED_ENCODING_ALLOWLIST")
    assert not hasattr(decoder, "SOURCE_DECLARED_ENCODING_ONLY")
    with pytest.raises(DecoderError, match="frozen exact SHA/config allowlist"):
        decoder._compatibility_config(G01_DECLARED_SHA_BIG5, "BIG5")
    assert decoder._compatibility_config(G01_DECLARED_SHA_BIG5, None) == {
        "encoding": None, "authority_status": None,
    }
    compatibility_sha, compatibility_encoding = next(iter(decoder.COMPATIBILITY_ALLOWLIST.items()))
    assert decoder._compatibility_config(compatibility_sha, compatibility_encoding) == {
        "encoding": compatibility_encoding,
        "authority_status": decoder.COMPATIBILITY_ONLY,
    }
    path = _write_sav(tmp_path / "d01_positive.sav", {"X": [1.0]})
    incidence = decode_sav(path)
    try:
        assert incidence.row_count == 1
    finally:
        incidence.close()


def test_d02_naive_datetime_is_stringified_and_opaque_carrier_absent(tmp_path):
    assert not hasattr(R5TypedValueCodec, "opaque_decoder_value")
    assert not hasattr(R5TypedValueCodec, "normalize_decoder_physical_value")
    with pytest.raises(R5CodecError, match="date/time meaning may not be invented"):
        R5TypedValueCodec().encode(dt.date(2020, 1, 2))
    assert decoder._jsonable(dt.date(2020, 1, 2)) == "2020-01-02"
    assert isinstance(decoder._jsonable(dt.date(2020, 1, 2)), str)

    path = _write_sav(
        tmp_path / "d02.sav",
        {"D": [dt.date(2020, 1, 2)]},
        variable_format={"D": "DATE11"},
    )
    incidence = decode_sav(path)
    try:
        cell = next(incidence.iter_cells())
        assert cell.variable_name == "D"
        assert isinstance(cell.raw_value, str)

        def named_d02_receiving_assertion(raw_value) -> None:
            assert isinstance(raw_value, R5OpaqueValue)

        with pytest.raises(AssertionError):
            named_d02_receiving_assertion(cell.raw_value)
    finally:
        incidence.close()

    assert R5TypedValueCodec().roundtrip_equal("2020-01-02")
    assert R5TypedValueCodec().roundtrip_equal(1.0)


def test_tampered_source_bytes_do_not_change_bound_snapshot_and_fresh_gate_restores(tmp_path):
    path = _write_sav(tmp_path / "custody.sav", {"X": [1.0, 2.0]})
    original = path.read_bytes()
    original_sha = _sha(path)
    incidence = decode_sav(path, expected_source_sha256=original_sha)
    try:
        custody = incidence.source_custody
        assert custody["contract"] == decoder.SOURCE_CUSTODY_CONTRACT
        assert custody["source_sha256"] == original_sha
        assert custody["snapshot_sha256"] == original_sha
        assert custody["content_bound"] is True
        assert custody["snapshot_path_unlinked"] is True
        assert custody["reader_access_mode"] == "O_RDONLY"
        path.write_bytes(b"tampered")
        assert incidence.verify_source_identity() == original_sha
        assert [cell.raw_value for cell in incidence.iter_cells()] == [1.0, 2.0]
    finally:
        incidence.close()

    with pytest.raises(DecoderError, match="source sha256 mismatch before governed decode"):
        decode_sav(path, expected_source_sha256=original_sha)

    path.write_bytes(original)
    restored = decode_sav(path, expected_source_sha256=original_sha)
    try:
        assert [cell.raw_value for cell in restored.iter_cells()] == [1.0, 2.0]
    finally:
        restored.close()


def test_snapshot_byte_tamper_and_stale_close_are_named_refusals_then_restore(tmp_path, monkeypatch):
    path = _write_sav(tmp_path / "snapshot.sav", {"X": [1.0]})
    original_sha = _sha(path)
    incidence = decode_sav(path, expected_source_sha256=original_sha)
    original_sha_fd = decoder._sha_fd
    try:
        monkeypatch.setattr(decoder, "_sha_fd", lambda _fd: "0" * 64)
        with pytest.raises(DecoderError, match="source snapshot bytes changed after identity acquisition"):
            incidence.verify_source_identity()
        monkeypatch.setattr(decoder, "_sha_fd", original_sha_fd)
        assert incidence.verify_source_identity() == original_sha
    finally:
        incidence.close()

    with pytest.raises(DecoderError, match="source snapshot is closed"):
        incidence.verify_source_identity()

    restored = decode_sav(path, expected_source_sha256=original_sha)
    try:
        assert restored.verify_source_identity() == original_sha
    finally:
        restored.close()


def test_removed_source_and_missing_r9_broker_faults_restore(tmp_path):
    path = _write_sav(tmp_path / "removed.sav", {"X": [1.0]})
    original = path.read_bytes()
    original_sha = _sha(path)
    incidence = decode_sav(path, expected_source_sha256=original_sha)
    try:
        path.unlink()
        assert incidence.verify_source_identity() == original_sha
        assert [cell.raw_value for cell in incidence.iter_cells()] == [1.0]
    finally:
        incidence.close()

    with pytest.raises(DecoderError, match="source bytes unavailable"):
        decode_sav(path, expected_source_sha256=original_sha)

    path.write_bytes(original)
    restored = decode_sav(path, expected_source_sha256=original_sha)
    restored.close()

    for module in (
        "rawlsing_next.pre553_source_access_broker",
        "rawlsing_next.pre553_source_session",
        "rawlsing_next.pre553_execution_binding",
    ):
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module(module)


def test_current_issuer_gate_rejects_wrong_host_scope_edition_and_replay(tmp_path):
    _bundle, compilation = _current_bundle(tmp_path)
    issued = _issued(compilation)
    record = issued.record
    resolver = TestOnlyDecisionResolver(record)

    assert admit(
        issued.workload, resolver, host=HOST, purpose=PURPOSE, allow_test_only=True
    ) == record

    with pytest.raises(WorkloadAdmissionError, match="SOURCE_HOST_PURPOSE_MISMATCH"):
        admit(
            issued.workload,
            TestOnlyDecisionResolver(replace(record, host="wrong-host")),
            host=HOST, purpose=PURPOSE, allow_test_only=True,
        )
    with pytest.raises(
        WorkloadAdmissionError,
        match="CURRENT_COMPETENT_SOURCE_AND_SCIENCE_DECISION_REQUIRED",
    ):
        admit(issued.workload, resolver, host=HOST, purpose=PURPOSE, allow_test_only=False)
    with pytest.raises(WorkloadAdmissionError, match="ISSUED_SOURCE_EDITION_MISMATCH"):
        admit(
            issued.workload,
            TestOnlyDecisionResolver(replace(record, source_sha256="a" * 64)),
            host=HOST, purpose=PURPOSE, allow_test_only=True,
        )
    with pytest.raises(
        WorkloadAdmissionError,
        match="SEPARATE_SOURCE_AND_SCIENTIFIC_PERMISSIONS_REQUIRED",
    ):
        admit(
            issued.workload,
            TestOnlyDecisionResolver(replace(record, scientific_permission_refs=())),
            host=HOST, purpose=PURPOSE, allow_test_only=True,
        )

    switched = ExactRef(
        record.decision_ref.kind, record.decision_ref.object_id, "b" * 64
    )
    with pytest.raises(WorkloadBindingRefusal, match="UNKNOWN_DECISION_REF"):
        admit(
            replace(issued.workload, decision_ref=switched), resolver,
            host=HOST, purpose=PURPOSE, allow_test_only=True,
        )
    assert admit(
        issued.workload, resolver, host=HOST, purpose=PURPOSE, allow_test_only=True
    ) == record

    record_fields = {field.name for field in fields(record)}
    assert "role" not in record_fields
    assert "issuer_role" not in record_fields
