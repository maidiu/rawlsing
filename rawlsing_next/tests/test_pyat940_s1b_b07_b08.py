from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pandas as pd
import pyreadstat
import pytest

import rawlsing_next.pre553_physical_decoder as decoder
from rawlsing_next.pre553_r157_projection_adapter import (
    CURRENT_GRANTED,
    IssuedSourceReadDecision,
    SourceConfig,
    SourceReadAdmissionRefusal,
    decode_config_with_source_read_permission,
    decode_fixture_config,
    source_read_request_from_config,
    reader_configuration_from_config,
)
from rawlsing_next.tests.test_pyat940_s1b_support import (
    make_config,
    ref,
    write_fixture,
)


class _TripwirePath:
    """A source path that must never be converted to a filesystem path."""

    def __fspath__(self):
        raise AssertionError("source path was accessed before source-read admission")

    def __str__(self):
        raise AssertionError("source path was stringified before source-read admission")

    def __repr__(self):
        return "<source-path-not-admitted>"

    def is_file(self):
        raise AssertionError("source path was stat'ed before source-read admission")

    def open(self, *args, **kwargs):
        raise AssertionError("source path was opened before source-read admission")


def _decision(request, *, currentness: str = CURRENT_GRANTED, revoked: bool = False):
    return IssuedSourceReadDecision(
        decision_ref=ref("SOURCE_READ_DECISION", "urn:rawlsing:s1b:decision"),
        source_permission_refs=(ref("SOURCE_PERMISSION", "urn:rawlsing:s1b:permission"),),
        source_id=request.source_id,
        source_sha256=request.source_sha256,
        source_format=request.source_format,
        custody_locator_binding=request.custody_locator_binding,
        host=request.host,
        purpose=request.purpose,
        consumer_use=request.consumer_use,
        read_operation=request.read_operation,
        physical_read_extent=request.physical_read_extent,
        metadata_freeze_refs=request.metadata_freeze_refs,
        semantic_use_scope=request.semantic_use_scope,
        effective_interval="S1B_SESSION",
        currentness=currentness,
        revocation_ref=(
            ref("REVOCATION", "urn:rawlsing:s1b:revocation") if revoked else None
        ),
        retention_export_limits={"retention": "SESSION_ONLY"},
    )


class _Resolver:
    def __init__(self, behavior):
        self.behavior = behavior
        self.calls = 0

    def resolve_current(self, request):
        self.calls += 1
        return self.behavior(request, self.calls)


def _original_config(tmp_path: Path, source_format: str = "SAV"):
    path, source_sha, rows = write_fixture(
        tmp_path / f"admission-{source_format}", source_format=source_format,
        values=(1.0, 2.0, 7.0),
    )
    config = SourceConfig(make_config(
        source_format=source_format,
        active_source_sha256=source_sha,
        row_count=rows,
        values=(1.0, 2.0, 7.0),
        original=True,
    ))
    return path, config


@pytest.mark.parametrize("behavior", (
    lambda request, call: _decision(request, currentness="EXPIRED"),
    lambda request, call: _decision(request, currentness="REVOKED"),
    lambda request, call: _decision(request, currentness=CURRENT_GRANTED, revoked=True),
))
def test_b07_denied_current_decision_never_opens_source(tmp_path, monkeypatch, behavior):
    _path, config = _original_config(tmp_path)
    request = source_read_request_from_config(
        config,
        host="s1b-host",
        purpose="s1b-purpose",
        consumer_use="s1b-consumer",
        semantic_use_scope=("S1B_SYNTHETIC_READ",),
    )
    reader = reader_configuration_from_config(config)
    resolver = _Resolver(behavior)

    def forbidden_open(*args, **kwargs):
        raise AssertionError("decoder opened a source after a denied decision")

    monkeypatch.setattr(decoder, "_acquire_source_snapshot", forbidden_open)
    monkeypatch.setattr(decoder, "_sha", forbidden_open)
    with pytest.raises(SourceReadAdmissionRefusal) as caught:
        decode_config_with_source_read_permission(
            config,
            source_path=_TripwirePath(),
            resolver=resolver,
            host="s1b-host",
            purpose="s1b-purpose",
            consumer_use="s1b-consumer",
            semantic_use_scope=("S1B_SYNTHETIC_READ",),
        )
    assert caught.value.code in {
        "SOURCE_READ_NOT_CURRENT", "SOURCE_READ_REVOKED",
    }
    assert resolver.calls == 1


def test_b07_decision_binding_mismatch_never_opens_source(tmp_path):
    _path, config = _original_config(tmp_path)

    def mismatch(request, call):
        decision = _decision(request)
        object.__setattr__(decision, "host", "other-host")
        return decision

    with pytest.raises(SourceReadAdmissionRefusal, match="HOST_MISMATCH"):
        decode_config_with_source_read_permission(
            config,
            source_path=_TripwirePath(),
            resolver=_Resolver(mismatch),
            host="s1b-host",
            purpose="s1b-purpose",
            consumer_use="s1b-consumer",
            semantic_use_scope=("S1B_SYNTHETIC_READ",),
        )


def test_b07_current_decision_admits_then_post_decode_revocation_refuses(tmp_path):
    path, config = _original_config(tmp_path)

    def revoke_after_decode(request, call):
        return _decision(
            request,
            currentness=CURRENT_GRANTED if call == 1 else "REVOKED",
        )

    with pytest.raises(SourceReadAdmissionRefusal, match="SOURCE_READ_NOT_CURRENT"):
        decode_config_with_source_read_permission(
            config,
            source_path=path,
            resolver=_Resolver(revoke_after_decode),
            host="s1b-host",
            purpose="s1b-purpose",
            consumer_use="s1b-consumer",
            semantic_use_scope=("S1B_SYNTHETIC_READ",),
        )


def test_b08_bounded_sav_and_dta_use_only_chunked_reads(tmp_path, monkeypatch):
    values = tuple(float((index % 4) + 1) for index in range(1200))
    observed = {}

    original_chunks = pyreadstat.read_file_in_chunks

    for source_format in ("SAV", "DTA"):
        path, source_sha, rows = write_fixture(
            tmp_path / f"bounded-{source_format}",
            source_format=source_format,
            values=values,
        )
        config = SourceConfig(make_config(
            source_format=source_format,
            active_source_sha256=source_sha,
            row_count=rows,
            values=values,
        ))

        chunk_lengths = []
        original_reader = pyreadstat.read_sav if source_format == "SAV" else pyreadstat.read_dta

        def guarded_reader(path_arg, *args, **kwargs):
            metadata_only = bool(kwargs.get("metadataonly", False))
            has_chunk_bounds = "row_limit" in kwargs and "row_offset" in kwargs
            if not metadata_only and not has_chunk_bounds:
                raise AssertionError(
                    f"full-frame {source_format} read attempted outside chunk bounds"
                )
            return original_reader(path_arg, *args, **kwargs)

        def tracked_chunks(reader, file_path, *args, **kwargs):
            # Re-wrap the reader so every actual frame length proves a bounded
            # window, while the production decoder still supplies its own reader.
            def frame_tracker(path_arg, **inner_kwargs):
                frame = reader(path_arg, **inner_kwargs)
                if not inner_kwargs.get("metadataonly", False):
                    try:
                        chunk_lengths.append(len(frame[0]))
                    except TypeError:
                        pass
                return frame

            return original_chunks(frame_tracker, file_path, *args, **kwargs)

        monkeypatch.setattr(pyreadstat, "read_sav" if source_format == "SAV" else "read_dta", guarded_reader)
        monkeypatch.setattr(pyreadstat, "read_file_in_chunks", tracked_chunks)
        monkeypatch.setattr(pd, "read_stata", lambda *a, **k: (_ for _ in ()).throw(
            AssertionError("pandas full-frame fallback is forbidden")
        ))

        incidence = decode_fixture_config(config, path)
        probe_chunks = list(chunk_lengths)
        chunk_lengths.clear()
        try:
            cell_batches = list(incidence.iter_batches(128))
            cell_count = sum(len(batch) for batch in cell_batches)
            assert incidence.row_count == rows == 1200
            assert cell_count == rows * len(incidence.variables)
            assert len(chunk_lengths) > 1
            assert sum(chunk_lengths) == rows
            assert max(chunk_lengths) <= decoder.MAX_READ_ROWS
            if source_format == "DTA":
                assert sum(probe_chunks) == rows
            else:
                assert probe_chunks == []
            observed[source_format] = {
                "rows": rows,
                "probe_chunks": probe_chunks,
                "data_chunks": list(chunk_lengths),
                "cells": cell_count,
            }
        finally:
            incidence.close()

        monkeypatch.setattr(pyreadstat, "read_file_in_chunks", original_chunks)


@pytest.mark.parametrize("source_format", ("SAV", "DTA"))
def test_b08_small_fixture_process_rss_and_chunk_receipt(tmp_path, source_format):
    path, source_sha, rows = write_fixture(
        tmp_path / "rss",
        source_format=source_format,
        values=tuple(float((index % 4) + 1) for index in range(1200)),
    )
    config_path = tmp_path / "rss.config.json"
    document = make_config(
        source_format=source_format,
        active_source_sha256=source_sha,
        row_count=rows,
        values=tuple(float((index % 4) + 1) for index in range(1200)),
    )
    config_path.write_text(json.dumps(document), encoding="utf-8")

    script = """
import json, resource, sys
from rawlsing_next.pre553_r157_projection_adapter import SourceConfig, decode_fixture_config
config = SourceConfig(json.load(open(sys.argv[1], encoding='utf-8')))
incidence = decode_fixture_config(config, sys.argv[2])
try:
    batches = [batch for batch in incidence.iter_batches(128)]
finally:
    incidence.close()
print(json.dumps({
    'rows': incidence.row_count,
    'cells': sum(len(batch) for batch in batches),
    'peak_rss_ru_maxrss': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    'platform': sys.platform,
}))
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(config_path), str(path)],
        cwd=str(Path(__file__).resolve().parents[2]),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    evidence = json.loads(result.stdout)
    assert evidence["rows"] == 1200
    assert evidence["cells"] == 2400
    assert evidence["peak_rss_ru_maxrss"] > 0
    # Honest small-fixture receipt: this is not a 100k or 6 GiB integration claim.
    assert Path(path).stat().st_size > 0
