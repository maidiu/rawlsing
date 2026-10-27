"""R157 P3 reader/key/loader integration tests over nonrespondent fixtures."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next.pre553_c11_repository import C11LogicalRelease
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_physical_decoder import (
    COMPATIBILITY_ALLOWLIST,
    COMPATIBILITY_ONLY,
    PhysicalCell,
    PhysicalMissingState,
    PhysicalSourceIncidence,
    PhysicalVariable,
)
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.pre553_source_read_admission import (
    CURRENT_GRANTED,
    EXACT_FILE,
    SOURCE_RESPONSE_DECODE,
    IssuedSourceReadDecision,
    SourceReadAdmissionRefusal,
    SourceReadRequest,
    SourceReaderConfiguration,
    decode_with_source_read_permission,
)
from rawlsing_next.source_configuration.errors import SourceConfigurationBindingError
from rawlsing_next.source_configuration.factory import (
    build_governed_c11_projection,
    build_source_backed_c11_repository_from_config,
    build_validated_c11_release_from_config,
    row_native_keys_from_transport,
)
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.reader import (
    decode_config_with_source_read_permission,
    reader_configuration_from_config,
    source_read_request_from_config,
)
from rawlsing_next.source_configuration.schema import SourceConfig, load_source_config
from rawlsing_next.tests.test_universal_source_projection import write_rows

ROOT = Path(__file__).resolve().parents[2]
P0_CONFIG = ROOT / "source_pre553_validation/foundation/examples/SRC09_q101_fixture.config.json"
P0_FIXTURE = ROOT / "source_pre553_validation/foundation/fixtures/SRC09_q101_nonrespondent.json"
P3_CONFIG = ROOT / "source_pre553_validation/integration/examples/SRC09_q101_keyed_fixture.config.json"
R154_LOADER = ROOT / "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/runtime/r154_load.py"


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:rawlsing:r157:p3:{tag}", semantic_hash({"tag": tag}))


def _decision(request: SourceReadRequest, **changes) -> IssuedSourceReadDecision:
    material = dict(
        decision_ref=_ref("DECISION", "d1"),
        source_permission_refs=(_ref("PERMISSION", "p1"),),
        source_id=request.source_id,
        source_sha256=request.source_sha256,
        source_format=request.source_format,
        custody_locator_binding=request.custody_locator_binding,
        host=request.host,
        purpose=request.purpose,
        consumer_use=request.consumer_use,
        read_operation=SOURCE_RESPONSE_DECODE,
        physical_read_extent=EXACT_FILE,
        metadata_freeze_refs=request.metadata_freeze_refs,
        semantic_use_scope=request.semantic_use_scope,
        effective_interval="2026-10-26/2026-10-27",
        currentness=CURRENT_GRANTED,
        revocation_ref=None,
        retention_export_limits={"export": "DENY", "retention": "SESSION"},
    )
    material.update(changes)
    return IssuedSourceReadDecision(**material)


class _Resolver:
    def __init__(self, *decisions):
        self.decisions = list(decisions)
        self.calls = 0

    def resolve_current(self, request):
        self.calls += 1
        return self.decisions[min(self.calls - 1, len(self.decisions) - 1)]


def _reader_doc(sha: str, fmt: str = "SAV", encoding: dict | None = None) -> dict:
    return {
        "identity": {
            "source_id": "SRC09",
            "expected_source_sha256": sha,
            "source_format": fmt,
            "metadata_witness_ref": _ref("METADATA_WITNESS", "m1").as_dict(),
            "locator": {"root": "EXTERNAL_LOCATOR_ID", "locator_id": "P3_NONRESPONDENT_READER"},
            "reader": {
                "configuration_ref": _ref("READER_CONFIGURATION", "r1").as_dict(),
                "encoding": encoding,
            },
        },
        "binding": {"identity_class": "ORIGINAL_SOURCE"},
    }


def _request(doc: dict) -> SourceReadRequest:
    return source_read_request_from_config(
        doc, host="p3-harness", purpose="R157_P3_HARNESS",
        consumer_use="R157_P3_HARNESS", semantic_use_scope=("R157_P3_HARNESS",))


def test_reader_configuration_extracts_exact_allowlisted_and_refuses_unqualified():
    sha = "6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8a"
    doc = _reader_doc(sha, encoding={
        "value": "latin1", "sha256": sha, "authority_status": COMPATIBILITY_ONLY,
    })
    reader = reader_configuration_from_config(doc)
    assert reader.source_sha256 == sha
    assert reader.encoding == "latin1"
    assert reader.authority_status == COMPATIBILITY_ONLY
    with pytest.raises(SourceReadAdmissionRefusal, match="NOT_QUALIFIED"):
        SourceReaderConfiguration("a" * 64, "latin1", COMPATIBILITY_ONLY)
    with pytest.raises(SourceConfigurationBindingError, match="fixtures are not original reads"):
        reader_configuration_from_config(load_source_config(P0_CONFIG))


@pytest.mark.parametrize("fmt", ["SAV", "DTA"])
def test_actual_decoder_receives_no_override_and_config_request(tmp_path, fmt):
    path = tmp_path / f"p3_reader.{fmt.lower()}"
    frame = pd.DataFrame({"ID": [1.0, 2.0], "X": [1.0, 0.0]})
    if fmt == "SAV":
        write_rows(path, [{"ID": 1.0, "X": 1.0}, {"ID": 2.0, "X": 0.0}])
    else:
        pyreadstat.write_dta(frame, path)
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    doc = _reader_doc(sha, fmt=fmt)
    request = _request(doc)
    resolver = _Resolver(_decision(request), _decision(request))
    incidence = decode_config_with_source_read_permission(
        doc, source_path=path, resolver=resolver,
        host="p3-harness", purpose="R157_P3_HARNESS",
        consumer_use="R157_P3_HARNESS", semantic_use_scope=("R157_P3_HARNESS",),
    )
    try:
        assert incidence.source_sha256 == sha
        assert incidence.row_count == 2
        assert incidence.reader_configuration["encoding"] is None
        assert resolver.calls == 2
    finally:
        incidence.close()


def test_reader_encoding_is_passed_to_decoder_and_reader_sha_mismatch_refuses_before_resolver(monkeypatch):
    allowlisted_sha = next(iter(COMPATIBILITY_ALLOWLIST))
    other_sha = next(sha for sha in COMPATIBILITY_ALLOWLIST if sha != allowlisted_sha)
    encoding = COMPATIBILITY_ALLOWLIST[allowlisted_sha]
    doc = _reader_doc(allowlisted_sha, encoding={
        "value": encoding, "sha256": allowlisted_sha, "authority_status": COMPATIBILITY_ONLY,
    })
    request = _request(doc)
    reader = reader_configuration_from_config(doc)
    calls = []

    class _Incidence:
        source_sha256 = allowlisted_sha
        source_format = "SAV"
        reader_configuration = {"encoding": encoding, "authority_status": COMPATIBILITY_ONLY}
        def close(self):
            pass

    def fake_decode(path, *, expected_source_sha256, encoding=None):
        calls.append((expected_source_sha256, encoding))
        return _Incidence()

    monkeypatch.setattr("rawlsing_next.pre553_source_read_admission.decode_sav", fake_decode)
    resolver = _Resolver(_decision(request), _decision(request))
    incidence = decode_with_source_read_permission(
        source_path="/not/opened", request=request, resolver=resolver, reader=reader)
    assert calls == [(allowlisted_sha, encoding)]
    assert incidence.reader_configuration["encoding"] == encoding
    assert resolver.calls == 2

    bad_reader = SourceReaderConfiguration(
        other_sha, COMPATIBILITY_ALLOWLIST[other_sha], COMPATIBILITY_ONLY)
    fresh = _Resolver(_decision(request))
    with pytest.raises(SourceReadAdmissionRefusal, match="READER_SOURCE_SHA_MISMATCH"):
        decode_with_source_read_permission(
            source_path="/not/opened", request=request, resolver=fresh, reader=bad_reader)
    assert fresh.calls == 0


def test_keyed_fixture_binds_exact_row_witnesses_and_native_release():
    cfg = load_source_config(P3_CONFIG)
    fixture = load_fixture_stream(P0_FIXTURE)
    keys = row_native_keys_from_transport(cfg, stream=fixture)
    assert keys is not None and len(keys) == 9
    assert keys[1].kind == "R157_NONRESPONDENT_FIXTURE_KEY"
    assert keys[1].content_hash == keys[6].content_hash
    assert keys[1].object_id != keys[6].object_id
    projection = build_governed_c11_projection(cfg, row_native_keys=keys)
    assert projection.respondents[0].source_native_respondent_key_ref_or_typed_absence == keys[1]
    release = build_validated_c11_release_from_config(cfg, stream=fixture)
    assert isinstance(release, C11LogicalRelease)
    repository, release2 = build_source_backed_c11_repository_from_config(cfg, fixture)
    assert release2.release_ref == release.release_ref
    assert repository is not None


def test_keyed_fixture_extracts_keys_from_permitted_physical_incidence():
    cfg = load_source_config(P3_CONFIG)
    variables = (
        PhysicalVariable(1, "country", "double", "Country code", {}, (), {}, {}),
        PhysicalVariable(124, "q101", "double", "q101", {}, (), {}, {}),
    )
    frame = pd.DataFrame({
        "country": [1.0, 2.0, 3.0, 4.0, 5.0, 1.0, 2.0, 3.0, 4.0],
        "q101": [1.0, 2.0, 3.0, 4.0, -1.0, 7.0, 8.0, 9.0, None],
    })
    incidence = PhysicalSourceIncidence(
        source_sha256=cfg.active_source_sha256,
        source_format="SAV",
        row_count=9,
        variables=variables,
        reader_configuration={"fixture": "R157_P3_KEYED"},
        file_metadata={"fixture": "R157_P3_KEYED"},
        _frame=frame,
    )
    keys = row_native_keys_from_transport(cfg, incidence=incidence)
    assert len(keys) == 9
    assert keys[1].kind == "R157_NONRESPONDENT_FIXTURE_KEY"
    release = build_validated_c11_release_from_config(cfg, incidence=incidence)
    assert isinstance(release, C11LogicalRelease)


def test_configured_key_slot_missing_cell_is_typed_unknown():
    cfg = load_source_config(P3_CONFIG)
    cells = (
        PhysicalCell(1, 124, "q101", 1.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(1, 1, "country", 1.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(2, 124, "q101", 2.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(2, 1, "country", None, PhysicalMissingState.SYSTEM_MISSING, None),
    )
    stream = ExactPhysicalCellStream("f" * 64, 2, lambda: cells)
    keys = row_native_keys_from_transport(cfg, stream=stream)
    assert keys[1].kind == "R157_NONRESPONDENT_FIXTURE_KEY"
    assert keys[2].state == "UNKNOWN"


def _load_r154():
    spec = importlib.util.spec_from_file_location("r157_p3_r154_load", R154_LOADER)
    module = importlib.util.module_from_spec(spec)
    sys.modules["r157_p3_r154_load"] = module
    spec.loader.exec_module(module)
    return module


def test_r154_loader_delegates_prepared_construction_not_issued_workload(monkeypatch):
    module = _load_r154()
    monkeypatch.setattr(module, "_b49", lambda: (_ for _ in ()).throw(
        AssertionError("private B49 loader must not be used by the prepared path")))
    cfg = load_source_config(P0_CONFIG)
    fixture = load_fixture_stream(P0_FIXTURE)
    prepared = module.build_native_workload("SRC09", config=cfg, source=fixture)
    assert prepared.status == "PREPARED_CONFIGURATION_ONLY__NOT_ISSUED_ORIGINAL_WORKLOAD"
    assert prepared.issued_original_workload is False
    assert prepared.execution_permission_required is True
    assert isinstance(prepared.release, C11LogicalRelease)
    assert prepared.row_native_key_count == 0
    assert prepared.native_calls == (
        "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
        "rawlsing_next.pre553_source_backed_c11_facade.build_source_backed_c11_repository",
    )

    keyed_cfg = load_source_config(P3_CONFIG)
    keyed = module.build_native_workload("SRC09", config=keyed_cfg, source=fixture)
    assert keyed.row_native_key_count == 9
    assert keyed.release.release_ref != prepared.release.release_ref

    with pytest.raises(module.LoadRefusal, match="PREPARED_NATIVE_CONSTRUCTION_REQUIRES"):
        module.build_native_workload("SRC09", config=cfg)
    with pytest.raises(module.LoadRefusal, match="PREPARED_NATIVE_CONSTRUCTION_REQUIRES"):
        module.build_native_workload("SRC09", source=fixture)


def test_r154_prepared_path_wrong_source_refusal_and_restore(monkeypatch):
    module = _load_r154()
    monkeypatch.setattr(module, "_b49", lambda: (_ for _ in ()).throw(
        AssertionError("private B49 loader must not be used by the prepared path")))
    cfg = load_source_config(P0_CONFIG)
    fixture = load_fixture_stream(P0_FIXTURE)
    first = module.build_native_workload("SRC09", config=cfg, source=fixture)
    cells = tuple(fixture.iter_cells())
    wrong = ExactPhysicalCellStream("f" * 64, 9, lambda: cells)
    with pytest.raises(Exception, match="SHA|binding|mismatch"):
        module.build_native_workload("SRC09", config=cfg, source=wrong)
    restored = module.build_native_workload("SRC09", config=cfg, source=fixture)
    assert restored.release.release_ref == first.release.release_ref
