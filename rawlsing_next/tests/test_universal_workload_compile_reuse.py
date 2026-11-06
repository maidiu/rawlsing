"""Focused tests for preparation reuse in the finite universal-workload compile."""
from __future__ import annotations

from pathlib import Path

import pytest

import rawlsing_next.pre553_universal_workload as workload
from rawlsing_next.pre553_native_workload_binding import (
    OperationFixture,
    WorkloadBindingRefusal,
    build_projection_catalog,
    build_test_only_workload,
    prepare_projection_catalog,
)
from rawlsing_next.tests.test_universal_source_projection import load_s3, write_rows


def _bundle(path: Path, *, changed: bool = False):
    rows = [
        {
            "PID": float(index), "OCCASION": 0.0,
            "SCORE": float(index % 10), "MR1": None, "RANK1": None,
            "FORM": float(index % 2),
        }
        for index in range(20)
    ]
    if changed:
        rows[0]["SCORE"] = 9.0
    write_rows(path, rows)
    return load_s3(path, variable="SCORE")


def test_compile_reuses_prepared_projection_with_exact_identity(tmp_path, monkeypatch):
    bundle = _bundle(tmp_path / "reuse.sav")
    original_prepare = workload.prepare_projection_catalog
    original_catalog = workload.build_projection_catalog
    original_workload = workload.build_test_only_workload
    calls = {"prepare": 0, "catalog": 0, "workload": 0}

    def prepare(**kwargs):
        calls["prepare"] += 1
        return original_prepare(**kwargs)

    def catalog(**kwargs):
        calls["catalog"] += 1
        return original_catalog(**kwargs)

    def issued(**kwargs):
        calls["workload"] += 1
        return original_workload(**kwargs)

    monkeypatch.setattr(workload, "prepare_projection_catalog", prepare)
    monkeypatch.setattr(workload, "build_projection_catalog", catalog)
    monkeypatch.setattr(workload, "build_test_only_workload", issued)
    first = workload.compile_universal_workload(
        bundle=bundle, as_of="2026-11-06", host="compile-reuse",
        purpose="TEST_ONLY_SOURCEFREE",
    )
    assert calls == {"prepare": 1, "catalog": 10, "workload": 10}
    assert len(first.operations) == len(first.compiled) == 10
    assert len(first.expected_jobs) == 10
    assert len({c.issued.envelope_sha256 for c in first.compiled}) == 10
    result = workload.execute_universal_workload(
        compilation=first, source_factory=lambda _ref: bundle.physical_stream,
    )
    assert result.anti_join()["no_drop_ok"] is True
    assert len(result.fact_refs) == 10
    assert len(result.receipt_refs) == 10
    assert result.failed == ()

    restored = workload.compile_universal_workload(
        bundle=bundle, as_of="2026-11-06", host="compile-reuse",
        purpose="TEST_ONLY_SOURCEFREE",
    )
    assert restored.content_hash == first.content_hash
    assert restored.expected_jobs == first.expected_jobs
    assert [c.issued.envelope_sha256 for c in restored.compiled] == [
        c.issued.envelope_sha256 for c in first.compiled]


def test_prepared_projection_mismatch_and_changed_input_refuse_reuse(tmp_path):
    base = _bundle(tmp_path / "base.sav")
    changed = _bundle(tmp_path / "changed.sav", changed=True)
    prepared = prepare_projection_catalog(bundle=base, as_of="2026-11-06")
    fixture = OperationFixture("probe", "SCORE", "0")
    with pytest.raises(WorkloadBindingRefusal, match="PREPARED_PROJECTION_MISMATCH"):
        build_projection_catalog(
            bundle=changed, operation=fixture, as_of="2026-11-06",
            prepared=prepared,
        )
    with pytest.raises(WorkloadBindingRefusal, match="PREPARED_PROJECTION_MISMATCH"):
        build_projection_catalog(
            bundle=base, operation=fixture, as_of="2026-11-07",
            prepared=prepared,
        )
    catalog, request = build_projection_catalog(
        bundle=changed, operation=fixture, as_of="2026-11-06",
    )
    with pytest.raises(WorkloadBindingRefusal, match="PREPARED_PROJECTION_MISMATCH"):
        build_test_only_workload(
            bundle=changed, projection=changed.projection, catalog=catalog,
            request=request, operation=fixture, as_of="2026-11-06",
            host="compile-reuse", purpose="TEST_ONLY_SOURCEFREE",
            prepared=prepared,
        )
    first = workload.compile_universal_workload(
        bundle=base, as_of="2026-11-06", host="compile-reuse",
        purpose="TEST_ONLY_SOURCEFREE",
    )
    second = workload.compile_universal_workload(
        bundle=changed, as_of="2026-11-06", host="compile-reuse",
        purpose="TEST_ONLY_SOURCEFREE",
    )
    assert first.content_hash != second.content_hash
    assert first.expected_jobs != second.expected_jobs
    restored = workload.compile_universal_workload(
        bundle=base, as_of="2026-11-06", host="compile-reuse",
        purpose="TEST_ONLY_SOURCEFREE",
    )
    assert restored.content_hash == first.content_hash
    assert restored.expected_jobs == first.expected_jobs
