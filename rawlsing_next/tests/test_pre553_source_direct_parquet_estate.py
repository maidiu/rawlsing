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
