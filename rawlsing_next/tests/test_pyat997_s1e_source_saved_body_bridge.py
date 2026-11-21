"""#997 S1-E P0 source-backed Q2 -> accepted S2-C body bridge court.

These are sourcefree SAV/DTA fixtures, never original35 source issuance.
Run with: python -m pytest -q -o addopts='' -p no:cacheprovider
rawlsing_next/tests/test_pyat997_s1e_source_saved_body_bridge.py
"""
from __future__ import annotations

from pathlib import Path
import os
import sqlite3

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_source_saved_body_bridge import (
    SourceSavedBodySink, SourceSavedBridgeError,
)
from rawlsing_next.pre553_source_direct_parquet_estate import (
    VerifiedDirectEstate, DirectEstateError,
)
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture, build


def _saved(root: Path, *, source_format="SAV", values=(0., 1., 2., 0., 1.),
           monkeypatch=None):
    root.mkdir(mode=0o700)
    fixture = source_fixture(root / "source", source_format=source_format,
                             values=values)
    private = root / "private"
    private.mkdir(mode=0o700)
    cert = root / "direct.sqlite"
    sink = SourceSavedBodySink(certificate_path=cert,
                               authorized_private_root=private,
                               chunk_rows=2)
    handoff = build(root, fixture, name="direct.sqlite", body_sink=sink,
                    chunk_size=2)
    receipt = sink.receipt
    return fixture, handoff, sink, private, receipt


def _cold(private, receipt, *, allow=lambda _: True):
    return VerifiedDirectEstate(
        private, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        current_authorizer=allow,
    )


@pytest.mark.parametrize("format", ("SAV", "DTA"))
def test_one_source_snapshot_real_cold_thirteen_body_members(
    tmp_path, monkeypatch, format,
):
    import rawlsing_next.pre553_physical_decoder as decoder
    original_snapshot = decoder._acquire_source_snapshot
    opens = []
    def spy(*args, **kwargs):
        opens.append(1)
        return original_snapshot(*args, **kwargs)
    monkeypatch.setattr(decoder, "_acquire_source_snapshot", spy)
    # Full-graph compatibility fallback is expressly NOT part of this bridge.
    def forbidden(*args, **kwargs):
        raise AssertionError("legacy full C11 graph was constructed")
    monkeypatch.setattr(C11Repository, "__init__", forbidden)
    fixture, handoff, sink, private, receipt = _saved(
        tmp_path / format, source_format=format,
    )
    assert opens == [1], opens
    assert handoff.stats.source_reads == 1
    assert handoff.stats.cell_passes == 1
    assert handoff.stats.full_c11_builds == 0
    assert handoff.roots == receipt.i02
    assert receipt.reconstructed_v1_release_ref.kind == "C11LogicalRelease"
    assert handoff.body_transport["complete"] is True
    assert sink.stats["body_objects"] == sum(sink.stats["family_yields"].values())
    assert sink.stats["journal_bytes"] > 0
    assert sink.stats["retained_bytes"] == receipt.retained_bytes
    assert not list(private.glob(".s1e-body-journal-*"))
    assert not list(private.glob(".s2c-stage-*"))
    assert not list(private.rglob("*.sqlite"))
    cold = _cold(private, receipt)
    for family in ALL_FAMILIES:
        bodies = tuple(cold.iter_family(family, batch_size=2))
        assert len(bodies) == handoff.counts[family], family
        assert tuple(o.ref.key for o in bodies) == tuple(
            o.ref.key for o in _cold(private, receipt).iter_family(family))
    events = list(cold.iter_family("RespondentEvent", batch_size=2))
    respondents = list(cold.iter_family("RespondentIdentity", batch_size=2))
    assert len(events) == len(respondents) == fixture["rows"]
    observed = tuple(cold.select_events(respondents[0].ref))
    assert observed
    assert {o.ref.key for o in observed}.issubset({o.ref.key for o in events})
    with sqlite3.connect(handoff.destination) as db:
        actual = dict(db.execute("SELECT family,count(*) FROM main.objects GROUP BY family"))
    assert actual["RespondentEvent"] == len(events)


def test_actual_source_cell_changed_cold_body_changed_then_exact_restore(tmp_path):
    baseline = _saved(tmp_path / "before")
    changed = _saved(tmp_path / "after", values=(0., 1., 1., 0., 1.))
    restored = _saved(tmp_path / "restore")
    (_, hand0, sink0, private0, rec0) = baseline
    (_, hand1, sink1, private1, rec1) = changed
    (_, hand2, sink2, private2, rec2) = restored
    assert hand0.source_sha256 != hand1.source_sha256
    assert rec0.i02.logical != rec1.i02.logical
    assert rec0.i02.logical == rec2.i02.logical
    assert rec0.reconstructed_v1_release_ref == rec2.reconstructed_v1_release_ref
    def events(p, r):
        return tuple((o.ref.key, o.raw_response_value, o.typed_state)
                     for o in _cold(p, r).iter_family("RespondentEvent"))
    first, second, third = events(private0, rec0), events(private1, rec1), events(private2, rec2)
    assert first != second
    assert first == third


def test_missing_body_member_fails_closed_and_cleans_all_stages(tmp_path):
    fixture_root = tmp_path / "case"
    fixture_root.mkdir()
    fixture = source_fixture(fixture_root / "source")
    private = fixture_root / "private"
    private.mkdir(mode=0o700)
    class DropOne(SourceSavedBodySink):
        def emit(self, family, obj):
            if family == "RespondentEvent" and not getattr(self, "dropped", False):
                self.dropped = True
                return
            super().emit(family, obj)
    cert = fixture_root / "direct.sqlite"
    sink = DropOne(certificate_path=cert, authorized_private_root=private)
    with pytest.raises(SourceSavedBridgeError, match="BODY_CENSUS_DRIFT"):
        build(fixture_root, fixture, name="direct.sqlite", body_sink=sink)
    assert sink.state == "aborted"
    assert not cert.exists()
    assert not list(private.glob(".s1e-body-journal-*"))
    assert not list(private.glob(".s2c-stage-*"))
    assert not list(private.glob("releases/*"))


def test_wrong_pinned_root_and_current_revocation_refuse_native_cold(tmp_path):
    fixture, handoff, sink, private, receipt = _saved(tmp_path / "root")
    from dataclasses import replace
    wrong = replace(receipt.i02, source="SOURCE_ARTIFACT|forged|" + "0"*64)
    with pytest.raises(DirectEstateError):
        VerifiedDirectEstate(private, exact_path=receipt.path,
                             independently_held_manifest_sha256=receipt.manifest_sha256,
                             independently_held_i02=wrong,
                             current_authorizer=lambda _: True)
    blocked = {"allow": True}
    cold = _cold(private, receipt, allow=lambda _: blocked["allow"])
    blocked["allow"] = False
    with pytest.raises(DirectEstateError, match="current source/operation authority refused"):
        list(cold.iter_family("RespondentEvent"))


def test_sink_requires_exact_source_and_rejects_wrong_transport_before_publish(tmp_path):
    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    sink = SourceSavedBodySink(
        certificate_path=tmp_path / "not-created.sqlite",
        authorized_private_root=private,
    )
    with pytest.raises(SourceSavedBridgeError, match="INVALID_SOURCE_SHA"):
        sink.begin(source_sha256="X"*64, source_id="S",
                   universe_ref=None, projection_identity_ref=None)
    assert not list(private.iterdir())
    with pytest.raises(SourceSavedBridgeError, match="SAVED_ESTATE_NOT_COMMITTED"):
        _ = sink.receipt
