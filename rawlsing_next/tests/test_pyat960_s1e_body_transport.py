"""Q2 B-role body-preserving transport and failure-cleanup courts."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

import rawlsing_next.pre553_physical_decoder as decoder
import rawlsing_next.pre553_source_i02_handoff as handoff_module
from rawlsing_next.pre553_r157_projection_adapter import (
    decode_fixture_config,
    row_native_keys_from_transport,
)
from rawlsing_next.pre553_source_i02_handoff import SourceI02Refusal
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
from rawlsing_next.tests.test_pyat960_s1e_support import (
    DenyResolver,
    GrantResolver,
    RecordingBodySink,
    build,
    certificate_counts,
    event_refs_from_certificate,
    source_fixture,
)


def _instrument_source_counts(monkeypatch):
    counts = {"snapshot": 0, "sha": 0}
    original_snapshot = decoder._acquire_source_snapshot
    original_sha = decoder._sha

    def snapshot(*args, **kwargs):
        counts["snapshot"] += 1
        return original_snapshot(*args, **kwargs)

    def sha(*args, **kwargs):
        counts["sha"] += 1
        return original_sha(*args, **kwargs)

    monkeypatch.setattr(decoder, "_acquire_source_snapshot", snapshot)
    monkeypatch.setattr(decoder, "_sha", sha)
    return counts


@pytest.mark.parametrize("source_format", ("SAV", "DTA"))
def test_s1e_body_sink_receives_exact_13_family_bodies_without_reread(
    tmp_path, monkeypatch, source_format
):
    fixture = source_fixture(tmp_path, source_format=source_format)
    counts = _instrument_source_counts(monkeypatch)
    sink = RecordingBodySink()
    handoff = build(
        tmp_path, fixture, name=f"body-{source_format}.sqlite", body_sink=sink)

    assert counts == {"snapshot": 1, "sha": 0}
    assert sink.begin_calls == 1
    assert sink.begin_args["source_sha256"] == fixture["source_sha"]
    assert sink.begin_args["source_id"] == fixture["document"]["identity"]["source_id"]
    assert sink.finished is True
    assert sink.aborted is False
    assert handoff.body_transport is not None
    assert handoff.body_transport["schema"] == (
        "PYAT960_S1E_SOURCE_I02_BODY_TRANSPORT@1.0.0")
    assert handoff.body_transport["complete"] is True
    assert handoff.body_transport["finished"] is True
    assert handoff.body_transport["object_count"] == sum(sink.counts.values())

    manifest_counts = {
        family: handoff.manifest.declared_record_counts_by_logical_family[family]
        for family in ALL_FAMILIES
    }
    observed_counts = {
        family: sink.counts.get(family, 0) for family in ALL_FAMILIES
    }
    assert observed_counts == manifest_counts
    assert set(sink.counts) | set(sink.absences) == set(ALL_FAMILIES)
    assert len(sink.absences) == 6
    assert sink.finish_roots == handoff.roots
    assert sink.finish_manifest.content_hash == handoff.manifest.content_hash
    assert dict(sink.finish_counts) == manifest_counts
    assert sink.finish_transport["finished"] is True

    certificate_counts_by_family, _header = certificate_counts(
        Path(handoff.destination))
    for family in ALL_FAMILIES:
        assert certificate_counts_by_family.get(family, 0) == manifest_counts[family]
    assert set(sink.events) == event_refs_from_certificate(
        Path(handoff.destination))

    assert handoff.stats.source_reads == 1
    assert handoff.stats.source_prehash_passes == 0
    assert handoff.stats.snapshot_acquisitions == 1
    assert handoff.stats.decode_calls == 1
    assert handoff.stats.key_witness_passes == 0
    assert handoff.stats.cell_passes == 1
    assert handoff.stats.full_c11_builds == 0
    assert handoff.stats.source_open_model == "FIXTURE_SNAPSHOT_ONLY"
    assert handoff.stats.cleanup_complete is True
    assert not list(tmp_path.glob(".s1e-i02-spool-*"))
    assert len(list(tmp_path.glob("*.sqlite"))) == 1


def test_s1e_body_sink_preserves_repeated_occurrence_bodies(tmp_path):
    fixture = source_fixture(
        tmp_path / "occurrences",
        config_kwargs={"occurrences": 2},
    )
    sink = RecordingBodySink()
    handoff = build(
        tmp_path / "occurrences",
        fixture,
        name="occurrences.sqlite",
        body_sink=sink,
    )
    expected = fixture["rows"] * 2
    assert handoff.stats.event_count == expected
    assert sink.counts["RespondentEvent"] == expected
    assert len(set(sink.events)) == expected
    assert len(event_refs_from_certificate(Path(handoff.destination))) == expected
    assert handoff.census_audit["operation_source_antijoin"][
        "eligible_realized_count"] == handoff.census_audit[
            "operation_source_antijoin"]["eligible_operation_count"]


def test_s1e_body_sink_original_path_reports_two_source_reads(tmp_path, monkeypatch):
    fixture = source_fixture(tmp_path / "original", original=True)
    counts = _instrument_source_counts(monkeypatch)
    sink = RecordingBodySink()
    handoff = build(
        tmp_path / "original",
        fixture,
        name="original.sqlite",
        body_sink=sink,
        resolver=GrantResolver(),
        host="s1e-host",
        purpose="s1e-purpose",
        consumer_use="s1e-consumer",
        semantic_use_scope=("S1E_SOURCEFREE_TEST",),
    )
    assert counts == {"snapshot": 1, "sha": 1}
    assert handoff.stats.source_reads == 2
    assert handoff.stats.source_prehash_passes == 1
    assert handoff.stats.snapshot_acquisitions == 1
    assert handoff.stats.decode_calls == 1
    assert handoff.stats.source_open_model == (
        "ORIGINAL_PREHASH_PLUS_SNAPSHOT")
    assert sink.finished is True
    assert sink.counts["RespondentEvent"] == fixture["rows"]


def test_s1e_body_sink_keyed_scenario_discloses_external_key_pass(
    tmp_path, monkeypatch
):
    fixture = source_fixture(tmp_path / "keyed", keyed=True)
    counts = _instrument_source_counts(monkeypatch)
    incidence = decode_fixture_config(fixture["config"], fixture["path"])
    try:
        keys = row_native_keys_from_transport(
            fixture["config"], incidence=incidence, batch_size=4)
    finally:
        incidence.close()
    external_key_reads = counts["snapshot"]
    sink = RecordingBodySink()
    handoff = build(
        tmp_path / "keyed",
        fixture,
        name="keyed.sqlite",
        body_sink=sink,
        row_native_keys=keys,
    )
    assert external_key_reads == 1
    assert handoff.stats.source_reads == 1
    assert handoff.stats.key_witness_passes == 1
    assert counts["snapshot"] == 2
    assert sink.finished is True
    assert sink.counts["RespondentEvent"] == len(keys)


@pytest.mark.parametrize("fail_at", ("emit", "finish"))
def test_s1e_body_sink_failure_invalidates_certificate_and_cleans(
    tmp_path, monkeypatch, fail_at
):
    fixture = source_fixture(tmp_path / fail_at)
    counts = _instrument_source_counts(monkeypatch)
    sink = RecordingBodySink(fail_at=fail_at)
    target = tmp_path / fail_at / "failed.sqlite"
    with pytest.raises(RuntimeError, match=f"sink {fail_at} failure"):
        build(tmp_path / fail_at, fixture, name=target.name, body_sink=sink)
    assert counts["snapshot"] == 1
    assert target.exists() is False
    assert sink.aborted is True
    assert sink.finished is False
    assert not list((tmp_path / fail_at).glob(".s1e-i02-spool-*"))


def test_s1e_body_sink_begin_failure_never_opens_source(tmp_path, monkeypatch):
    fixture = source_fixture(tmp_path / "begin")
    sink = RecordingBodySink(fail_at="begin")

    def forbidden(*args, **kwargs):
        raise AssertionError("source opened after sink begin failure")

    monkeypatch.setattr(handoff_module, "decode_sav", forbidden)
    monkeypatch.setattr(handoff_module, "decode_dta", forbidden)
    with pytest.raises(RuntimeError, match="sink begin failure"):
        build(tmp_path / "begin", fixture, name="never.sqlite", body_sink=sink)
    assert sink.begin_calls == 1
    assert sink.aborted is True
    assert (tmp_path / "begin" / "never.sqlite").exists() is False
    assert not list((tmp_path / "begin").glob(".s1e-i02-spool-*"))


def test_s1e_builder_failure_after_publication_invalidates_target(
    tmp_path, monkeypatch
):
    fixture = source_fixture(tmp_path / "builder")
    sink = RecordingBodySink()
    real_builder = handoff_module.build_sourcefree_direct_i02

    def publish_then_fail(*args, **kwargs):
        real_builder(*args, **kwargs)
        raise RuntimeError("post-publication builder failure")

    monkeypatch.setattr(
        handoff_module, "build_sourcefree_direct_i02", publish_then_fail)
    target = tmp_path / "builder" / "published.sqlite"
    with pytest.raises(RuntimeError, match="post-publication builder failure"):
        build(tmp_path / "builder", fixture, name=target.name, body_sink=sink)
    assert target.exists() is False
    assert sink.aborted is True
    assert not list((tmp_path / "builder").glob(".s1e-i02-spool-*"))


def test_s1e_census_failure_precedes_sink_begin_and_source(tmp_path, monkeypatch):
    fixture = source_fixture(tmp_path / "census")
    sink = RecordingBodySink()
    bad_census = replace(
        fixture["census"],
        source_candidates=fixture["census"].source_candidates[:-1],
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("source opened after census failure")

    monkeypatch.setattr(handoff_module, "decode_sav", forbidden)
    monkeypatch.setattr(handoff_module, "decode_dta", forbidden)
    with pytest.raises(SourceI02Refusal, match="SOURCE_CENSUS_HASH_DRIFT"):
        build(
            tmp_path / "census",
            fixture,
            name="census.sqlite",
            body_sink=sink,
            census=bad_census,
        )
    assert sink.begin_calls == 0
    assert (tmp_path / "census" / "census.sqlite").exists() is False


def test_s1e_denied_original_permission_aborts_sink_before_source(
    tmp_path, monkeypatch
):
    fixture = source_fixture(tmp_path / "denied", original=True)
    sink = RecordingBodySink()

    def forbidden(*args, **kwargs):
        raise AssertionError("source opened after denied decision")

    monkeypatch.setattr(decoder, "_acquire_source_snapshot", forbidden)
    monkeypatch.setattr(decoder, "_sha", forbidden)
    with pytest.raises(Exception, match="SOURCE_READ_NOT_CURRENT"):
        build(
            tmp_path / "denied",
            fixture,
            name="denied.sqlite",
            body_sink=sink,
            resolver=DenyResolver(),
            host="s1e-host",
            purpose="s1e-purpose",
            consumer_use="s1e-consumer",
            semantic_use_scope=("S1E_SOURCEFREE_TEST",),
        )
    assert sink.begin_calls == 1
    assert sink.aborted is True
    assert (tmp_path / "denied" / "denied.sqlite").exists() is False
