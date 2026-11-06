"""R140 predecode source-read transport tests; synthetic and harness-only."""
from __future__ import annotations

import dataclasses
import hashlib
import os
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_source_read_admission import (
    EXACT_FILE, SOURCE_RESPONSE_DECODE, CURRENT_GRANTED,
    IssuedSourceReadDecision, SourceReadAdmissionRefusal, SourceReadRequest,
    decode_with_source_read_permission,
)
from rawlsing_next.tests.test_universal_source_projection import write_rows


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:r140:{kind.lower()}:{tag}", semantic_hash({"kind": kind, "tag": tag}))


def _request(path: Path | None = None, **changes) -> SourceReadRequest:
    sha = hashlib.sha256(path.read_bytes()).hexdigest() if path else "a" * 64
    material = dict(
        source_id="R140-SYNTHETIC", source_sha256=sha, source_format="SAV",
        custody_locator_binding="r04-snapshot:synthetic",
        host="r140-harness-host", purpose="R140_PREDECODE_HARNESS",
        consumer_use="R140_HARNESS_ONLY",
        metadata_freeze_refs=(_ref("METADATA_FREEZE", "m1"),),
        semantic_use_scope=("R140_SYNTHETIC_TRANSPORT",),
    )
    material.update(changes)
    return SourceReadRequest(**material)


def _decision(request: SourceReadRequest, **changes) -> IssuedSourceReadDecision:
    material = dict(
        decision_ref=_ref("SOURCE_READ_DECISION", "d1"),
        source_permission_refs=(_ref("SOURCE_PERMISSION", "s1"),),
        source_id=request.source_id, source_sha256=request.source_sha256,
        source_format=request.source_format,
        custody_locator_binding=request.custody_locator_binding,
        host=request.host, purpose=request.purpose, consumer_use=request.consumer_use,
        read_operation=SOURCE_RESPONSE_DECODE, physical_read_extent=EXACT_FILE,
        metadata_freeze_refs=request.metadata_freeze_refs,
        semantic_use_scope=request.semantic_use_scope,
        effective_interval="2026-10-26/2026-10-27", currentness=CURRENT_GRANTED,
        revocation_ref=None, retention_export_limits={"export": "DENY", "retention": "SESSION"},
    )
    material.update(changes)
    return IssuedSourceReadDecision(**material)


class _Resolver:
    def __init__(self, *decisions):
        self.decisions = list(decisions)
        self.calls = []

    def resolve_current(self, request):
        self.calls.append(request)
        value = self.decisions[min(len(self.calls) - 1, len(self.decisions) - 1)]
        if isinstance(value, BaseException):
            raise value
        return value


class _Incidence:
    def __init__(self, sha, fmt="SAV"):
        self.source_sha256 = sha
        self.source_format = fmt
        self.closed = False

    def close(self):
        self.closed = True


def test_authorized_synthetic_whole_file_uses_unchanged_r04_values_and_custody(tmp_path):
    path = tmp_path / "r140.sav"
    write_rows(path, [
        {"PID": 1.0, "OCCASION": 0.0, "SCORE": 1.0},
        {"PID": 2.0, "OCCASION": 0.0, "SCORE": 0.0},
    ])
    request = _request(path)
    resolver = _Resolver(_decision(request), _decision(request))
    incidence = decode_with_source_read_permission(
        source_path=path, request=request, resolver=resolver)
    direct = decode_sav(path, expected_source_sha256=request.source_sha256)
    try:
        assert incidence.source_sha256 == request.source_sha256
        assert incidence.source_format == "SAV"
        assert incidence.row_count == direct.row_count == 2
        assert incidence.physical_metadata_digest == direct.physical_metadata_digest
        assert incidence.source_custody == direct.source_custody
        assert [cell.raw_value for cell in incidence.iter_cells()] == [
            cell.raw_value for cell in direct.iter_cells()]
    finally:
        incidence.close()
        direct.close()


def test_refused_decision_has_zero_decoder_and_source_open_calls(tmp_path, monkeypatch):
    path = tmp_path / "r140-refused.sav"
    write_rows(path, [{"PID": 1.0, "OCCASION": 0.0, "SCORE": 1.0}])
    request = _request(path)
    calls = {"decode": 0, "open": 0}
    def decode(*args, **kwargs):
        calls["decode"] += 1
        raise AssertionError("decoder called")
    def open_fail(*args, **kwargs):
        calls["open"] += 1
        raise AssertionError("source opened")
    monkeypatch.setattr("rawlsing_next.pre553_source_read_admission.decode_sav", decode)
    monkeypatch.setattr("rawlsing_next.pre553_source_read_admission.decode_dta", decode)
    def stat_fail(*args, **kwargs):
        calls["open"] += 1
        raise AssertionError("source stat/hash attempted")
    monkeypatch.setattr("builtins.open", open_fail)
    monkeypatch.setattr(os, "open", open_fail)
    monkeypatch.setattr(os, "stat", stat_fail)
    monkeypatch.setattr(Path, "stat", stat_fail)
    monkeypatch.setattr(Path, "read_bytes", stat_fail)
    refusals = {
        "not_current": {"currentness": "REVOKED"},
        "expired": {"currentness": "EXPIRED"},
        "revoked": {"revocation_ref": _ref("REVOCATION", "r1")},
        "foreign_source": {"source_id": "FOREIGN"},
        "foreign_edition": {"source_sha256": "b" * 64},
        "foreign_format": {"source_format": "DTA"},
        "foreign_custody": {"custody_locator_binding": "foreign"},
        "foreign_host": {"host": "foreign-host"},
        "foreign_purpose": {"purpose": "FOREIGN_PURPOSE"},
        "foreign_consumer": {"consumer_use": "FOREIGN_USE"},
        "foreign_operation": {"read_operation": "SOURCE_HEADER_READ"},
        "foreign_extent": {"physical_read_extent": "SELECTED_COLUMNS"},
        "foreign_freeze": {"metadata_freeze_refs": (_ref("METADATA_FREEZE", "m2"),)},
        "foreign_semantics": {"semantic_use_scope": ("OTHER_USE",)},
    }
    for name, changes in refusals.items():
        with pytest.raises((SourceReadAdmissionRefusal, ValueError)):
            if name in {"foreign_operation", "foreign_extent"}:
                _decision(request, **changes)
            else:
                decode_with_source_read_permission(
                    source_path=path, request=request,
                    resolver=_Resolver(_decision(request, **changes)))

    with pytest.raises((SourceReadAdmissionRefusal, RuntimeError)):
        decode_with_source_read_permission(
            source_path=path, request=request,
            resolver=_Resolver(RuntimeError("EXTERNAL_AUTH_FAILED")),
        )
    assert calls == {"decode": 0, "open": 0}


def test_permission_is_resolved_before_decoder_and_rechecked_after(tmp_path, monkeypatch):
    path = tmp_path / "r140-order.sav"
    write_rows(path, [{"PID": 1.0, "OCCASION": 0.0, "SCORE": 1.0}])
    request = _request(path)
    calls = {"order": []}
    incidence = _Incidence(request.source_sha256)
    resolver = _Resolver(_decision(request), _decision(request))
    def decode(*args, **kwargs):
        calls["order"].append("decode")
        assert len(resolver.calls) == 1
        return incidence
    monkeypatch.setattr("rawlsing_next.pre553_source_read_admission.decode_sav", decode)
    monkeypatch.setattr("rawlsing_next.pre553_source_read_admission.decode_dta", decode)
    got = decode_with_source_read_permission(source_path=path, request=request, resolver=resolver)
    assert got is incidence
    assert calls["order"] == ["decode"]
    assert len(resolver.calls) == 2


def test_revocation_after_decode_closes_incidence_and_returns_nothing(tmp_path, monkeypatch):
    path = tmp_path / "r140-revoke.sav"
    write_rows(path, [{"PID": 1.0, "OCCASION": 0.0, "SCORE": 1.0}])
    request = _request(path)
    incidence = _Incidence(request.source_sha256)
    revoked = _decision(request, currentness="REVOKED", revocation_ref=_ref("REVOCATION", "r2"))
    resolver = _Resolver(_decision(request), revoked)
    monkeypatch.setattr("rawlsing_next.pre553_source_read_admission.decode_sav",
                        lambda *args, **kwargs: incidence)
    with pytest.raises(SourceReadAdmissionRefusal, match="SOURCE_READ_NOT_CURRENT"):
        decode_with_source_read_permission(source_path=path, request=request, resolver=resolver)
    assert incidence.closed is True


def test_request_refuses_selected_columns_extent_without_source_io(tmp_path):
    with pytest.raises(SourceReadAdmissionRefusal, match="SOURCE_READ_EXTENT_UNSUPPORTED"):
        _request(None, physical_read_extent="SELECTED_COLUMNS")
