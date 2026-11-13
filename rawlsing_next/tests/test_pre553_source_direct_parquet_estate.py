"""Hostile sourcefree S2-C candidate tests, not original35 or S2-D acceptance.

Exercise the actual S2-B direct builder, NOT a mocked certificate. The held
root in these tests models transfer to another principal; it does not supply
competent production authority or replace G5.
"""
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
import json

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next._pre553_direct_i02_sourcefree import (
    SourcefreeDirectI02Sections, direct_sections_from_candidate,
)
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate, write_direct_estate,
)
from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate


def _source(tag):
    candidate = _candidate(tag)
    replay = candidate.candidate_replay_manifest
    assert replay is not None
    direct = direct_sections_from_candidate(
        replace(candidate, candidate_replay_manifest=None),
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        replay_protocol_version=replay.replay_protocol_version,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
    )
    return candidate, direct


def _write(tmp_path, tag):
    root = tmp_path / tag
    root.mkdir(mode=0o700)
    candidate, direct = _source(tag)
    record = write_direct_estate(
        direct, candidate.empirical_universes[0].ref, root, chunk_rows=1,
    )
    return root, candidate, record


def _open(root, record, grant=lambda _roots: True):
    return VerifiedDirectEstate(
        root, exact_path=record.path,
        independently_held_manifest_sha256=record.manifest_sha256,
        independently_held_i02=record.i02,
        current_authorizer=grant,
    )


def test_direct_one_pass_thirteen_families_and_selected_exact_body(tmp_path):
    root, candidate, receipt = _write(tmp_path, "S2C-POS")
    assert receipt.i02.schema.endswith("DIRECT_SOURCEFREE_CANDIDATE_CERT@1")
    assert len(receipt.family_counts) == 13
    assert receipt.family_counts["RespondentEvent"] == len(candidate.respondent_events)
    path = Path(receipt.path)
    assert not list(path.glob("*.sqlite"))
    assert not list(path.glob("*.pkl"))
    assert sorted(item.name for item in path.glob("*.parquet")) == sorted([
        *(family + ".parquet" for family in receipt.family_counts),
        "event_locator.parquet",
    ])
    cold = _open(root, receipt)
    observed = tuple(cold.iter_family("RespondentEvent", batch_size=1))
    assert [o.ref for o in observed] == [o.ref for o in candidate.respondent_events]
    first = candidate.respondent_events[0]
    selected = tuple(cold.select_events(
        first.scoped_respondent_ref, first.native_question_ref,
        native_only=True,
    ))
    assert first.ref in {row.ref for row in selected}
    assert all(row.scoped_respondent_ref == first.scoped_respondent_ref
               for row in selected)



def test_canonical_mapping_proxy_and_dict_selectors_but_reject_forgery(tmp_path):
    """The native semantic-object ABI emits immutable mapping refs, not ExactRef."""
    root, candidate, receipt = _write(tmp_path, "S2C-EXACT-MAPPING")
    cold = _open(root, receipt)
    event = candidate.respondent_events[0]
    respondent_mapping = event.scoped_respondent_ref
    question_mapping = event.native_question_ref
    assert type(respondent_mapping) is MappingProxyType
    assert type(question_mapping) is MappingProxyType
    direct = tuple(cold.select_events(respondent_mapping, question_mapping,
                                      native_only=True))
    copied = tuple(cold.select_events(dict(respondent_mapping),
                                      dict(question_mapping), native_only=True))
    assert [x.ref for x in direct] == [x.ref for x in copied]
    assert event.ref in {x.ref for x in direct}

    forged_respondent = MappingProxyType({**dict(respondent_mapping),
                                         "not_an_exact_ref_field": "forged"})
    invalid_target = MappingProxyType({**dict(question_mapping),
                                       "content_hash": "non-sha256"})
    with pytest.raises(DirectEstateError, match="exact respondent and question"):
        tuple(cold.select_events(forged_respondent, question_mapping,
                                 native_only=True))
    with pytest.raises(DirectEstateError, match="exact respondent and question"):
        tuple(cold.select_events(respondent_mapping, invalid_target,
                                 native_only=True))

def test_missing_member_and_tamper_fail_before_any_empty_or_fact(tmp_path):
    root, candidate, receipt = _write(tmp_path, "S2C-MISSING")
    (Path(receipt.path) / "event_locator.parquet").unlink()
    with pytest.raises(DirectEstateError):
        _open(root, receipt)

    root2, _, receipt2 = _write(tmp_path, "S2C-TAMPER")
    path = Path(receipt2.path) / "RespondentEvent.parquet"
    with path.open("ab") as f:
        f.write(b"\nPOISON")
    with pytest.raises(DirectEstateError):
        _open(root2, receipt2)


def test_self_rehash_cannot_replace_independent_held_root(tmp_path):
    root, _, receipt = _write(tmp_path, "S2C-SELFREHASH")
    manifest = Path(receipt.path) / "manifest.json"
    data = json.loads(manifest.read_text())
    data["family_counts"]["RespondentEvent"] += 1
    manifest.write_text(json.dumps(data, sort_keys=True))
    with pytest.raises(DirectEstateError):
        _open(root, receipt)


def test_wrong_source_root_and_live_revocation_refuse(tmp_path):
    root, candidate, receipt = _write(tmp_path, "S2C-REVOKE")
    wrong = replace(receipt.i02, source="SOURCE_ARTIFACT:forged:0")
    with pytest.raises(DirectEstateError):
        VerifiedDirectEstate(
            root, exact_path=receipt.path,
            independently_held_manifest_sha256=receipt.manifest_sha256,
            independently_held_i02=wrong,
            current_authorizer=lambda _: True,
        )
    allow = {"value": True}
    cold = _open(root, receipt, lambda _: allow["value"])
    assert tuple(cold.iter_family("RespondentEvent"))
    allow["value"] = False
    with pytest.raises(DirectEstateError):
        tuple(cold.iter_family("RespondentEvent"))
    with pytest.raises(DirectEstateError):
        tuple(cold.select_events(candidate.respondent_events[0].scoped_respondent_ref))


def test_new_release_nonclobber_and_root_symlink_refusal(tmp_path):
    root, candidate, receipt = _write(tmp_path, "S2C-COLLIDE")
    _, second_source = _source("S2C-COLLIDE")
    with pytest.raises(DirectEstateError):
        write_direct_estate(
            second_source, candidate.empirical_universes[0].ref,
            root, chunk_rows=1,
        )
    assert _open(root, receipt).manifest["schema"].endswith("PARQUET_SOURCEFREE@1")
    redirected = tmp_path / "redirect"
    redirected.symlink_to(root, target_is_directory=True)
    _, direct = _source("S2C-REDIRECT")
    with pytest.raises(DirectEstateError):
        write_direct_estate(
            direct, candidate.empirical_universes[0].ref, redirected,
        )


def test_source_stream_is_consumed_once_even_when_certified_twice(tmp_path):
    candidate, direct = _source("S2C-ONESHOT")
    counts = {}
    def once(family, values):
        def iterate():
            counts[family] = counts.get(family, 0) + 1
            if counts[family] > 1:
                raise AssertionError("source section was re-read")
            yield from values
        return iterate()
    direct = replace(direct, sections=MappingProxyType({
        family: once(family, stream)
        for family, stream in direct.sections.items()
    }))
    root = tmp_path / "private"
    root.mkdir(mode=0o700)
    receipt = write_direct_estate(
        direct, candidate.empirical_universes[0].ref, root, chunk_rows=2,
    )
    assert counts == {family: 1 for family in direct.sections}
    assert tuple(_open(root, receipt).iter_family("RespondentEvent"))


def test_wrong_independent_expected_i02_refuses_complete_publication(tmp_path):
    candidate, direct = _source("S2C-EXPECTED")
    root = tmp_path / "private"
    root.mkdir(mode=0o700)
    wrong = ExternalI02Roots(
        logical="0" * 64, physical="0" * 64,
        release="wrong", source="wrong", replay="wrong", universe="wrong",
        schema="PYAT_S2B_DIRECT_SOURCEFREE_CANDIDATE_CERT@1",
    )
    with pytest.raises(DirectEstateError):
        write_direct_estate(
            direct, candidate.empirical_universes[0].ref,
            root, expected_i02=wrong,
        )
    assert not list((root / "releases").glob("*")) if (root / "releases").exists() else True


def test_denied_current_does_not_open_estate_bytes(tmp_path, monkeypatch):
    """G3: CURRENT must refuse before reading manifest or any persisted body."""
    root, _, receipt = _write(tmp_path, "S2C-DENY-BEFORE-BYTES")
    read_paths = []
    original_open = Path.open

    def spy_open(path, *args, **kwargs):
        read_paths.append(Path(path))
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", spy_open)
    with pytest.raises(DirectEstateError, match="current source/operation authority refused"):
        _open(root, receipt, lambda _roots: False)
    assert not any(path.is_relative_to(Path(receipt.path)) for path in read_paths), (
        "denied CURRENT still read a committed semantic/physical byte"
    )


@pytest.mark.parametrize("changed_field", [
    "respondent", "native", "canonical", "component", "state",
])
def test_forged_posting_rehashed_under_same_i02_detected(tmp_path, changed_field):
    """G3: exact ref and a rehashed physical manifest do not authenticate selectors.

    This models a flawed *writer or repinning decision*, NOT a way to bypass
    a previously held independent manifest hash. Same direct I02 roots are kept.
    """
    import hashlib
    import pyarrow as pa
    import pyarrow.parquet as pq
    from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref

    root, candidate, receipt = _write(tmp_path, "S2C-POSTING-" + changed_field)
    first = candidate.respondent_events[0]
    directory = Path(receipt.path)
    locator = directory / "event_locator.parquet"
    table = pq.read_table(locator)
    postings = table.to_pylist()
    forged = (exact_ref(candidate.empirical_universes[0].ref).key
              if changed_field != "state" else "DK")
    assert postings[0][changed_field] != forged
    postings[0][changed_field] = forged
    pq.write_table(pa.Table.from_pylist(postings, schema=table.schema),
                   locator, row_group_size=1, compression="zstd")
    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["members"]["event_locator.parquet"] = hashlib.sha256(locator.read_bytes()).hexdigest()
    manifest_path.write_text(canonical_json(manifest) + "\n")
    # Simulate a new independent receipt that pins this newly published
    # *incorrect* physical manifestation; direct I02 roots do not change.
    new_manifest_digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    cold = VerifiedDirectEstate(
        root, exact_path=receipt.path,
        independently_held_manifest_sha256=new_manifest_digest,
        independently_held_i02=receipt.i02,
        current_authorizer=lambda _roots: True,
    )
    respondent = (candidate.empirical_universes[0].ref
                  if changed_field == "respondent" else first.scoped_respondent_ref)
    with pytest.raises(DirectEstateError, match="posting disagrees with exact native body"):
        tuple(cold.select_events(respondent))


def test_corrupt_locator_before_publication_refused(tmp_path, monkeypatch):
    """G1/G3: matched census and valid native bodies cannot hide a false selector."""
    import rawlsing_next.pre553_source_direct_parquet_estate as estate

    candidate, direct = _source("S2C-PREBIND")
    root = tmp_path / "private-prebind"
    root.mkdir(mode=0o700)
    add = estate._IndexSink.add
    changed = {"done": False}

    def poisoned_add(self, row, group, offset):
        if not changed["done"]:
            row = dict(row)
            row["respondent"] = candidate.empirical_universes[0].ref.key
            changed["done"] = True
        return add(self, row, group, offset)

    monkeypatch.setattr(estate._IndexSink, "add", poisoned_add)
    with pytest.raises(DirectEstateError, match="event posting/body/direct I02 parity"):
        write_direct_estate(
            direct, candidate.empirical_universes[0].ref, root, chunk_rows=1,
        )
    assert changed["done"]
    assert not list((root / "releases").iterdir()) if (root / "releases").exists() else True


def test_every_emitted_family_cold_reconstructs_at_its_exact_census(tmp_path):
    """G1: no empty placeholder family may stand in for its actual body set."""
    root, _, receipt = _write(tmp_path, "S2C-THIRTEEN-BODIES")
    cold = _open(root, receipt)
    for family, expected_count in receipt.family_counts.items():
        objects = tuple(cold.iter_family(family, batch_size=1))
        assert len(objects) == expected_count, family
        assert all(type(obj).__name__ == family for obj in objects)
        assert len({obj.ref.key for obj in objects}) == expected_count, family


def test_duplicate_physical_event_cannot_replace_missing_exact_event(tmp_path, monkeypatch):
    """G1: source-certified counts and membership alone do not prove no-drop."""
    import rawlsing_next.pre553_source_direct_parquet_estate as estate

    candidate, direct = _source("S2C-DUPLICATE-PHYSICAL")
    root = tmp_path / "private-duplicate"
    root.mkdir(mode=0o700)
    original_flush = estate._Sink.flush
    poisoned = {"done": False}

    def poison_one_chunk(self):
        if (self.family == "RespondentEvent"
                and len(self.pending) >= 2 and not poisoned["done"]):
            self.pending[1] = dict(self.pending[0])
            poisoned["done"] = True
        return original_flush(self)

    monkeypatch.setattr(estate._Sink, "flush", poison_one_chunk)
    with pytest.raises(DirectEstateError, match="bounded physical-to-direct-I02 proof failed"):
        write_direct_estate(
            direct, candidate.empirical_universes[0].ref, root, chunk_rows=2,
        )
    assert poisoned["done"]
    assert not list((root / "releases").iterdir()) if (root / "releases").exists() else True


@pytest.mark.parametrize("lane", [
    "raw_typed", "occurrence", "kind", "content_hash", "raw_bool",
])
def test_physical_projection_lane_forgery_refused_before_publication(
    tmp_path, monkeypatch, lane,
):
    """A2 hostile: source-I02 membership and event posting can remain valid
    while a typed/value/occurrence/identity Parquet lane is silently wrong.
    The entire physical projection must match the source-certified exact body.
    """
    import rawlsing_next.pre553_source_direct_parquet_estate as estate

    candidate, direct = _source("S2C-A2-LANE-" + lane)
    root = tmp_path / ("private-" + lane)
    root.mkdir(mode=0o700)
    original_flush = estate._Sink.flush
    corrupted = {"done": False}

    def poison_typed_lane(self):
        if self.family == "RespondentEvent" and self.pending and not corrupted["done"]:
            entry = dict(self.pending[0])
            if lane == "raw_bool":
                entry[lane] = not bool(entry[lane])
            else:
                entry[lane] = str(entry[lane]) + "::FORGED"
            self.pending[0] = entry
            corrupted["done"] = True
        return original_flush(self)

    monkeypatch.setattr(estate._Sink, "flush", poison_typed_lane)
    with pytest.raises(DirectEstateError, match="physical typed/identity/occurrence lane"):
        write_direct_estate(
            direct, candidate.empirical_universes[0].ref, root, chunk_rows=2,
        )
    assert corrupted["done"]
    assert not list((root / "releases").iterdir()) if (root / "releases").exists() else True


def test_reconstructed_v1_release_is_distinct_and_manifest_pinned(tmp_path):
    """A2 R1: source-direct I02 is NOT a historic v1 validation seal."""
    import hashlib
    from rawlsing_next.pre553_empirical_objects import canonical_json

    root, candidate, receipt = _write(tmp_path, "S2C-V1-DISTINCT")
    cold = _open(root, receipt)
    assert receipt.i02.release.startswith("C11_DIRECT_SOURCEFREE_RELEASE|")
    assert receipt.reconstructed_v1_release_ref.kind == "C11LogicalRelease"
    assert receipt.reconstructed_v1_release_ref.object_id == (
        candidate.source_release_manifest.release_id
    )
    assert cold.reconstructed_v1_release_ref == receipt.reconstructed_v1_release_ref
    assert receipt.reconstructed_v1_release_ref.key != receipt.i02.release

    # Even with a freshly repinned *physical* manifest SHA, a direct-schema
    # release may not masquerade as a historic C11LogicalRelease.
    manifest = Path(receipt.path) / "manifest.json"
    material = json.loads(manifest.read_text(encoding="utf-8"))
    material["reconstructed_v1_release_ref"] = receipt.i02.release
    manifest.write_text(canonical_json(material) + "\n", encoding="utf-8")
    new_held_digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
    with pytest.raises(DirectEstateError, match="reconstructed v1 release identity"):
        VerifiedDirectEstate(
            root, exact_path=receipt.path,
            independently_held_manifest_sha256=new_held_digest,
            independently_held_i02=receipt.i02,
            current_authorizer=lambda _: True,
        )


def test_tampered_direct_certificate_v1_header_refuses_before_publication(
    tmp_path, monkeypatch,
):
    """A2 R1: never persist a changed certificate header as a new v1 identity."""
    import sqlite3
    import rawlsing_next.pre553_source_direct_parquet_estate as estate

    candidate, direct = _source("S2C-V1-HEADER-TAMPER")
    root = tmp_path / "private-v1-header"
    root.mkdir(mode=0o700)
    actual_builder = estate.build_sourcefree_direct_i02
    tampered = {"value": False}

    def mutate_header(source, universe, destination, *, chunk_size):
        roots = actual_builder(
            source, universe, destination, chunk_size=chunk_size,
        )
        with sqlite3.connect(destination) as db:
            db.execute(
                "UPDATE header SET value=? "
                "WHERE name='reconstructed_v1_release_ref'",
                ("C11LogicalRelease|FORGED|" + "0" * 64,),
            )
        tampered["value"] = True
        return roots

    monkeypatch.setattr(estate, "build_sourcefree_direct_i02", mutate_header)
    with pytest.raises(DirectEstateError, match="certificate bytes changed after qualification"):
        write_direct_estate(
            direct, candidate.empirical_universes[0].ref, root, chunk_rows=2,
        )
    assert tampered["value"]
    assert not list((root / "releases").iterdir()) if (root / "releases").exists() else True
