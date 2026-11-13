"""Q2 S1-E source→direct-I02 construction tests.

The source fixtures are generated nonrespondent SAV/DTA bytes.  The operation/
fate census is the existing S1-C frozen-census shape over the same physical
variables.  No original source/respondent bytes are used.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import sqlite3

import pytest

from rawlsing_next._pre553_external_i02_certificate import (
    DIRECT_SCHEMA,
    ExternalI02IntegrityError,
    _digest_file,
    _logical_root,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_r157_projection_adapter import (
    build_validated_c11_release_from_config,
    decode_fixture_config,
)
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_r157_projection_adapter import (
    SourceConfig,
    row_native_keys_from_transport,
)
from rawlsing_next.pre553_r157_projection_adapter import (
    CURRENT_GRANTED,
    IssuedSourceReadDecision,
    SourceReadAdmissionRefusal,
)
from rawlsing_next.pre553_source_i02_handoff import (
    SourceI02Hold,
    SourceI02Refusal,
    build_source_i02_handoff,
    open_direct_native_i03,
)
from rawlsing_next.tests.test_pyat940_s1b_support import make_config, ref, sha256_text, write_fixture
from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import _freeze_packet
from rawlsing_next.tests.test_universal_grammar import (
    _frontier,
    _inventory,
    _occurrence,
    _policy,
)


def _fixture(tmp_path: Path, *, source_format: str = "SAV", values=(0.0, 1.0, 2.0, 0.0, 1.0), keyed=False):
    path, source_sha, rows = write_fixture(
        tmp_path / f"src-{source_format}", source_format=source_format, values=values)
    document = make_config(
        source_format=source_format,
        active_source_sha256=source_sha,
        row_count=rows,
        values=values,
        keyed=keyed,
    )
    config = SourceConfig(document)
    inventory = replace(
        _inventory((_occurrence("q101"), _occurrence("country")), complete=True),
        source_id=document["identity"]["source_id"],
        wave=document["identity"]["wave"],
        edition=document["identity"]["instrument_release_id"],
        source_sha256=source_sha,
        inventory_id="PYAT960-S1E-INVENTORY",
    )
    policy = _policy(j=2, k=2, d=1)
    frontier = _frontier(inventory, policy)
    census = _freeze_packet(frontier)
    return path, source_sha, rows, config, document, inventory, policy, frontier, census


def _build(tmp_path, fixture, name="out.sqlite", config=None, **kwargs):
    path, source_sha, rows, cfg, doc, inv, policy, frontier, census = fixture
    return build_source_i02_handoff(
        config=config or cfg,
        source_path=path,
        destination=tmp_path / name,
        census=census,
        inventory=inv,
        policy=policy,
        frontier=frontier,
        **kwargs,
    )


def _event_refs(path: Path):
    db = sqlite3.connect(path)
    try:
        return tuple(row[0] for row in db.execute(
            "SELECT ref FROM main.objects WHERE family='RespondentEvent' ORDER BY ref"))
    finally:
        db.close()


def _certificate_counts(path: Path):
    db = sqlite3.connect(path)
    try:
        rows = dict(db.execute(
            "SELECT family,COUNT(*) FROM main.objects GROUP BY family"))
        header = dict(db.execute("SELECT name,value FROM main.header"))
    finally:
        db.close()
    return rows, header


def test_s1e_source_direct_i02_positive_and_real_roots(tmp_path, monkeypatch):
    fixture = _fixture(tmp_path)
    import rawlsing_next.pre553_physical_decoder as decoder
    original = decoder._acquire_source_snapshot
    reads = []
    monkeypatch.setattr(
        decoder, "_acquire_source_snapshot",
        lambda *a, **k: reads.append(1) or original(*a, **k),
    )
    import rawlsing_next.pre553_r157_projection_adapter as legacy_mod
    monkeypatch.setattr(
        legacy_mod, "build_validated_c11_release_from_config",
        lambda *a, **k: (_ for _ in ()).throw(
            AssertionError("full legacy C11 build called")),
    )
    handoff = _build(tmp_path, fixture)
    assert reads == [1]
    assert len(handoff.roots.logical) == 64
    assert len(handoff.roots.physical) == 64
    assert handoff.roots.schema == DIRECT_SCHEMA
    assert handoff.stats.source_reads == 1
    assert handoff.stats.cell_passes == 1
    assert handoff.stats.full_c11_builds == 0
    assert handoff.stats.event_count == fixture[2]  # one scalar occurrence per row
    assert handoff.stats.coordinate_count == fixture[2]
    assert handoff.stats.spool_files == 3
    assert not list(tmp_path.glob(".s1e-i02-spool-*"))
    assert handoff.census_audit["source_candidate_count"] > 0
    assert handoff.census_audit["fate_counts"].get("ELIGIBLE", 0) > 0
    assert handoff.census_audit["fate_counts"].get("HELD", 0) > 0
    counts, header = _certificate_counts(Path(handoff.destination))
    for family, declared in handoff.manifest.declared_record_counts_by_logical_family.items():
        if family == "ReplayManifest":
            continue
        assert counts.get(family, 0) == declared
    assert header["schema"] == DIRECT_SCHEMA
    db = sqlite3.connect(handoff.destination)
    try:
        assert _logical_root(db, schema=DIRECT_SCHEMA) == handoff.roots.logical
    finally:
        db.close()
    assert _digest_file(Path(handoff.destination)) == handoff.roots.physical
    assert {row["operation_id"] for row in handoff.operation_fates} == {
        row.op_id for row in fixture[7].operations}


@pytest.mark.parametrize("source_format", ("SAV", "DTA"))
def test_s1e_changed_source_meaning_changes_root_and_restore(tmp_path, source_format):
    fixture = _fixture(tmp_path / source_format, source_format=source_format)
    baseline = _build(tmp_path / source_format, fixture, name="base.sqlite")
    changed_doc = deepcopy(fixture[4])
    changed_doc["response_slots"][0]["values"][0]["response_state"] = "DK"
    changed = _build(
        tmp_path / source_format, fixture, name="changed.sqlite",
        config=SourceConfig(changed_doc),
    )
    assert changed.roots.logical != baseline.roots.logical
    assert changed.roots.physical != baseline.roots.physical
    assert _event_refs(Path(changed.destination)) != _event_refs(Path(baseline.destination))
    restored = _build(
        tmp_path / source_format, fixture, name="restored.sqlite",
        config=SourceConfig(deepcopy(fixture[4])),
    )
    assert restored.roots.logical == baseline.roots.logical
    assert restored.roots.physical == baseline.roots.physical
    assert _event_refs(Path(restored.destination)) == _event_refs(Path(baseline.destination))
    assert restored.stats.event_count == baseline.stats.event_count


def test_s1e_census_refuses_before_any_source_read(tmp_path, monkeypatch):
    fixture = _fixture(tmp_path)
    path, sha, rows, config, doc, inv, policy, frontier, census = fixture
    calls = []
    import rawlsing_next.pre553_source_i02_handoff as handoff_mod
    def forbidden(*a, **k):
        calls.append((a, k))
        raise AssertionError("source opened")
    monkeypatch.setattr(handoff_mod, "decode_sav", forbidden)
    monkeypatch.setattr(handoff_mod, "decode_dta", forbidden)

    bad_census = replace(census, source_candidates=census.source_candidates[1:])
    with pytest.raises(SourceI02Refusal, match="SOURCE_CENSUS_HASH_DRIFT"):
        build_source_i02_handoff(
            config=config, source_path=path, destination=tmp_path / "bad1.sqlite",
            census=bad_census, inventory=inv, policy=policy, frontier=frontier)
    assert calls == []

    bad_inventory = replace(inv, source_sha256="0" * 64)
    with pytest.raises(SourceI02Refusal, match="SOURCE_CENSUS_SHA_MISMATCH"):
        build_source_i02_handoff(
            config=config, source_path=path, destination=tmp_path / "bad2.sqlite",
            census=census, inventory=bad_inventory, policy=policy, frontier=frontier)
    assert calls == []
    bad_id = replace(inv, source_id="OTHER-SOURCE")
    with pytest.raises(SourceI02Refusal, match="SOURCE_CENSUS_ID_MISMATCH"):
        build_source_i02_handoff(
            config=config, source_path=path, destination=tmp_path / "bad2b.sqlite",
            census=census, inventory=bad_id, policy=policy, frontier=frontier)
    assert calls == []

    bad_items = replace(
        inv, occurrences=(_occurrence("absent"),) + tuple(inv.occurrences[1:]))
    bad_frontier = _frontier(bad_items, policy)
    bad_census2 = _freeze_packet(bad_frontier)
    with pytest.raises(SourceI02Refusal, match="SELECTED_OCCURRENCE_NOT_IN_SOURCE"):
        build_source_i02_handoff(
            config=config, source_path=path, destination=tmp_path / "bad3.sqlite",
            census=bad_census2, inventory=bad_items, policy=policy,
            frontier=bad_frontier)
    assert calls == []


def test_s1e_operation_duplicate_and_fate_audit(tmp_path):
    fixture = _fixture(tmp_path)
    path, sha, rows, config, doc, inv, policy, frontier, census = fixture
    duplicate = replace(
        census,
        source_candidates=census.source_candidates + (census.source_candidates[0],),
    )
    with pytest.raises(Exception, match="SOURCE_CENSUS_HASH_DRIFT|DUPLICATE"):
        build_source_i02_handoff(
            config=config, source_path=path, destination=tmp_path / "dup.sqlite",
            census=duplicate, inventory=inv, policy=policy, frontier=frontier)

    other_frontier = _frontier(inv, _policy(j=1, k=1, d=0))
    other_census = _freeze_packet(other_frontier)
    other = build_source_i02_handoff(
        config=config, source_path=path, destination=tmp_path / "other.sqlite",
        census=other_census, inventory=inv, policy=_policy(j=1, k=1, d=0),
        frontier=other_frontier)
    assert len(other.operation_fates) != len(frontier.operations) or {
        row["operation_id"] for row in other.operation_fates
    } != {row.operation_id for row in frontier.operations}
    assert other.census_audit["fate_counts"]


def test_s1e_cold_certificate_host_capability_is_explicit(tmp_path):
    fixture = _fixture(tmp_path)
    handoff = _build(tmp_path, fixture)
    if not os.path.isdir("/proc/self/fd"):
        with pytest.raises(Exception) as caught:
            handoff.open_certificate()
        assert "Linux /proc/self/fd" in str(caught.value) or "descriptor-pinned" in str(caught.value)
    else:
        with handoff.open_certificate() as reader:
            assert list(reader.respondent_refs())

def test_s1e_direct_identity_matches_legacy_owner_fixture(tmp_path):
    fixture = _fixture(tmp_path)
    handoff = _build(tmp_path, fixture, name="direct.sqlite")
    incidence = decode_fixture_config(fixture[3], fixture[0])
    try:
        legacy = build_validated_c11_release_from_config(
            fixture[3], incidence=incidence, batch_size=4)
    finally:
        incidence.close()
    db = sqlite3.connect(handoff.destination)
    try:
        header = dict(db.execute("SELECT name,value FROM main.header"))
    finally:
        db.close()
    assert header["reconstructed_v1_release_ref"] == legacy.release_ref.key
    assert header["reconstructed_v1_replay_ref"] == legacy.replay_manifest.ref.key
    db = sqlite3.connect(handoff.destination)
    try:
        direct_events = {row[0] for row in db.execute(
            "SELECT ref FROM main.objects WHERE family='RespondentEvent'")}
        direct_respondents = {row[0] for row in db.execute(
            "SELECT ref FROM main.objects WHERE family='RespondentIdentity'")}
    finally:
        db.close()
    from rawlsing_next.pre553_empirical_objects import RespondentEvent
    assert direct_events == {
        obj.ref.key for obj in legacy.public_objects if isinstance(obj, RespondentEvent)}
    from rawlsing_next.pre553_c11_integrity import RespondentIdentity
    assert direct_respondents == {obj.ref.key for obj in legacy.internal_records if isinstance(obj, RespondentIdentity)}


def test_s1e_direct_native_i03_uses_existing_cold_reader_or_explicit_host_hold(tmp_path):
    fixture = _fixture(tmp_path)
    handoff = _build(tmp_path, fixture, name="native.sqlite")
    incidence = decode_fixture_config(fixture[3], fixture[0])
    try:
        legacy = build_validated_c11_release_from_config(
            fixture[3], incidence=incidence, batch_size=4)
    finally:
        incidence.close()
    repository = C11Repository((legacy,))
    if not os.path.isdir("/proc/self/fd"):
        with pytest.raises(ExternalI02IntegrityError, match="Linux /proc/self/fd|descriptor-pinned"):
            open_direct_native_i03(handoff, repository, legacy.release_ref)
    else:
        reader = open_direct_native_i03(handoff, repository, legacy.release_ref)
        try:
            assert list(reader.respondent_refs())
        finally:
            reader.close()

def test_s1e_output_collision_and_optional_weight_raw_conservation(tmp_path):
    fixture = _fixture(tmp_path)
    path, sha, rows, config, doc, inv, policy, frontier, census = fixture
    handoff = _build(tmp_path, fixture, name="receipt.sqlite")
    with pytest.raises(SourceI02Refusal, match="OUTPUT_DESTINATION_INVALID"):
        build_source_i02_handoff(
            config=config, source_path=path, destination=tmp_path / "receipt.sqlite",
            census=census, inventory=inv, policy=policy, frontier=frontier)
    assert handoff.census_audit["fate_counts"]["HELD"] > 0
    assert any(
        operation.measure_kind == "SAMPLE" and operation.disposition == "ELIGIBLE"
        for operation in frontier.operations
    )
    assert not list(tmp_path.glob(".s1e-i02-spool-*"))

def test_s1e_original_source_denied_before_bytes(tmp_path):
    source_sha = sha256_text("S1E_ORIGINAL_NOT_READ")
    document = make_config(
        source_format="SAV", active_source_sha256=source_sha, row_count=2,
        values=(0.0, 1.0), keyed=False, original=True)
    config = SourceConfig(document)
    inventory = replace(
        _inventory((_occurrence("q101"),), complete=True),
        source_id=document["identity"]["source_id"],
        wave=document["identity"]["wave"],
        edition=document["identity"]["instrument_release_id"],
        source_sha256=source_sha,
        inventory_id="S1E-DENIED",
    )
    policy = _policy(j=1, k=1, d=0)
    frontier = _frontier(inventory, policy)
    census = _freeze_packet(frontier)

    class Deny:
        def resolve_current(self, request):
            return IssuedSourceReadDecision(
                decision_ref=ref("SOURCE_READ_DECISION", "urn:s1e:denied"),
                source_permission_refs=(ref("SOURCE_PERMISSION", "urn:s1e:denied"),),
                source_id=request.source_id, source_sha256=request.source_sha256,
                source_format=request.source_format,
                custody_locator_binding=request.custody_locator_binding,
                host=request.host, purpose=request.purpose,
                consumer_use=request.consumer_use,
                read_operation=request.read_operation,
                physical_read_extent=request.physical_read_extent,
                metadata_freeze_refs=request.metadata_freeze_refs,
                semantic_use_scope=request.semantic_use_scope,
                effective_interval="S1E", currentness="EXPIRED",
                revocation_ref=None, retention_export_limits={"retention": "NONE"},
            )

    with pytest.raises(SourceReadAdmissionRefusal, match="SOURCE_READ_NOT_CURRENT"):
        build_source_i02_handoff(
            config=config, source_path=tmp_path / "never-opened.sav",
            destination=tmp_path / "denied.sqlite", census=census,
            inventory=inventory, policy=policy, frontier=frontier,
            resolver=Deny(), host="h", purpose="p", consumer_use="c",
            semantic_use_scope=("S1E_SOURCEFREE",))
    assert not (tmp_path / "denied.sqlite").exists()

def test_s1e_keyed_source_requires_exact_physical_key_witnesses(tmp_path):
    fixture = _fixture(tmp_path / "keyed", keyed=True)
    path, sha, rows, config, doc, inv, policy, frontier, census = fixture
    incidence = decode_fixture_config(config, path)
    try:
        keys = row_native_keys_from_transport(config, incidence=incidence, batch_size=4)
    finally:
        incidence.close()
    handoff = _build(
        tmp_path / "keyed", fixture, name="keyed.sqlite", row_native_keys=keys)
    assert handoff.stats.event_count == len(keys)
    swapped = dict(keys)
    swapped[1], swapped[2] = keys[2], keys[1]
    with pytest.raises(SourceI02Refusal, match="ROW_NATIVE_KEY_WITNESS_MISMATCH"):
        _build(
            tmp_path / "keyed", fixture, name="keyed-bad.sqlite",
            row_native_keys=swapped)
