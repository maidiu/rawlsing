"""C0 physical-preservation contract against the ACTUAL source-direct I02 writer.

No original survey data or new interpretation is fabricated. An otherwise
qualified SAV/DTA fixture is rebuilt with one physically observed response
mapping omitted; the resulting same-source C11 release must retain its
uninterpreted raw cell, continue existing mapped rows and preserve separately
authorized coordinate ownership even when response interpretation is unknown.
"""
from copy import deepcopy
from pathlib import Path
import sqlite3

import pytest

from rawlsing_next.pre553_r157_projection_adapter import SourceConfig
from rawlsing_next.tests.test_pyat960_s1e_source_i02 import _fixture, _build


def _states(path: Path, family: str) -> dict[str, int]:
    db = sqlite3.connect(path)
    try:
        return dict(db.execute(
            "SELECT state,COUNT(*) FROM main.objects WHERE family=? GROUP BY state",
            (family,),
        ))
    finally:
        db.close()


@pytest.mark.parametrize("source_format", ["SAV", "DTA"])
def test_missing_mapping_preserves_raw_observed_and_mapped_responses_cold(
    tmp_path, source_format,
):
    fixture = _fixture(
        tmp_path / source_format,
        source_format=source_format,
        values=(0.0, 1.0, 2.0, 0.0, 1.0),
    )
    full = _build(tmp_path / source_format, fixture, name="fully-mapped.sqlite")
    altered = deepcopy(fixture[4])
    original_values = altered["response_slots"][0]["values"]
    mapped_rules = [v for v in original_values if v["raw_value"] != 2.0]
    assert len(mapped_rules) == len(original_values) - 1
    altered["response_slots"][0]["values"] = mapped_rules

    # C11 must not require a scientific mapping to preserve an observed
    # physical value; the *interpretation* of that one row remains held.
    first = _build(
        tmp_path / source_format, fixture,
        name="with-uninterpreted.sqlite", config=SourceConfig(altered),
    )
    second = _build(
        tmp_path / source_format, fixture,
        name="uninterpreted-reopen-parity.sqlite",
        config=SourceConfig(deepcopy(altered)),
    )
    states = _states(Path(first.destination), "RespondentEvent")
    assert states["INVALID_UNRESOLVED"] == 1
    assert states["SUBSTANTIVE_RESPONSE"] == 4
    assert first.stats.event_count == full.stats.event_count == 5
    assert first.stats.coordinate_count == full.stats.coordinate_count == 5
    assert first.roots.logical == second.roots.logical
    assert first.roots.physical == second.roots.physical
    assert first.roots.logical != full.roots.logical
    assert _states(Path(first.destination), "EmpiricalCoordinateFact") == _states(
        Path(full.destination), "EmpiricalCoordinateFact"
    )


def test_unmapped_response_does_not_skip_independent_approved_coordinate_owner(
    tmp_path,
):
    # Deliberately have BOTH independently approved owners share the
    # same physical response slot. Unknown response meaning must not
    # suppress a valid, separate source-coordinate fact.
    fixture = _fixture(
        tmp_path, source_format="SAV",
        values=(0.0, 1.0, 2.0, 1.0, 0.0),
    )
    altered = deepcopy(fixture[4])
    altered["response_slots"][0]["values"] = [
        rule for rule in altered["response_slots"][0]["values"]
        if rule["raw_value"] != 2.0
    ]
    # Reuse the exact authority/owner-set structure defined by the
    # existing S1-B fixture factory; do not improvise any permission.
    from rawlsing_next.tests.test_pyat940_s1b_support import make_config
    dual = make_config(
        source_format="SAV",
        active_source_sha256=fixture[1],
        row_count=fixture[2],
        values=(0.0, 1.0, 2.0, 1.0, 0.0),
        keyed=False,
        duplicate_slot_owner=True,
        include_slot_owner_set=True,
    )
    dual["response_slots"][0]["values"] = [
        rule for rule in dual["response_slots"][0]["values"]
        if rule["raw_value"] != 2.0
    ]
    from rawlsing_next.tests.test_pyat960_s1e_support import RecordingBodySink
    sink = RecordingBodySink()
    handoff = _build(
        tmp_path, fixture, name="qualified-dual-owner.sqlite",
        config=SourceConfig(dual), body_sink=sink,
    )
    assert sink.finished and not sink.aborted
    declared = dual["slot_owner_sets"][0]["owners"]
    expected_authorities = {
        owner["owner_family"]: {
            (a["authority_id"], a["authority_version"], a["authority_content_hash"])
            for a in owner["authority_refs"]
        }
        for owner in declared
    }
    observed = {"RespondentEvent@1.0.0": [], "EmpiricalCoordinateFact@1.0.0": []}
    for family, obj in sink.bodies:
        if family in ("RespondentEvent", "EmpiricalCoordinateFact"):
            observed[family + "@1.0.0"].append(obj)
    assert len(observed["RespondentEvent@1.0.0"]) == fixture[2]
    assert len(observed["EmpiricalCoordinateFact@1.0.0"]) >= fixture[2]
    for family, objects in observed.items():
        qualified = 0
        for obj in objects:
            actual = {
                (a.authority_id, a.authority_version, a.authority_content_hash)
                for a in obj.authority_snapshot_refs
            }
            if expected_authorities[family].issubset(actual):
                qualified += 1
        # The country coordinate is a different physical slot and has no
        # dual-owner requirement. Exactly the shared q101 slot's full
        # respondent body must carry each respective approved owner set.
        assert qualified == fixture[2], (
            family, "shared physical-slot owner authority did not survive"
        )
    assert _states(Path(handoff.destination), "RespondentEvent")[
        "INVALID_UNRESOLVED"
    ] == 1
    # One country coordinate plus the q101 coordinate, every physical
    # respondent including the one whose response meaning was unmapped.
    assert handoff.stats.coordinate_count == 2 * fixture[2]
    assert sum(_states(Path(handoff.destination), "EmpiricalCoordinateFact").values()) == 2 * fixture[2]



def test_unmapped_value_must_not_acquire_union_of_conflicting_known_occurrences():
    from types import SimpleNamespace
    from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
    from rawlsing_next.pre553_source_backed_c11_facade import OccurrenceRule
    from rawlsing_next.pre553_source_i02_handoff import (
        _occurrence_templates, SourceI02Refusal,
    )

    def occurrence(tag, key="0"):
        ref = ExactRef(
            "RESPONSE_TOPOLOGY", f"urn:test:preff:c0:{tag}",
            semantic_hash(tag),
        )
        return OccurrenceRule(
            key=key, topology_ref=ref,
            multiplicity_order_rank_fields={"index": int(key),
                                             "kind": "SCALAR_SINGULAR"},
        )

    one = occurrence("T1")
    other = occurrence("T2")
    same = SimpleNamespace(values=(
        SimpleNamespace(occurrences=(one,)),
        SimpleNamespace(occurrences=(one,)),
    ))
    assert _occurrence_templates(same) == (one,)
    wrong = SimpleNamespace(values=(
        SimpleNamespace(occurrences=(one,)),
        SimpleNamespace(occurrences=(other,)),
    ))
    with pytest.raises(SourceI02Refusal, match="TOPOLOGY_AMBIGUOUS"):
        _occurrence_templates(wrong)
    added = SimpleNamespace(values=(
        SimpleNamespace(occurrences=(one,)),
        SimpleNamespace(occurrences=(one, occurrence("T3", key="1"))),
    ))
    with pytest.raises(SourceI02Refusal, match="TOPOLOGY_AMBIGUOUS"):
        _occurrence_templates(added)
    no_source_template = SimpleNamespace(values=())
    with pytest.raises(SourceI02Refusal, match="NO_OCCURRENCE_TEMPLATE"):
        _occurrence_templates(no_source_template)


@pytest.mark.parametrize("source_format", ("SAV", "DTA"))
def test_cold_saved_unmapped_event_keeps_physical_class_and_mapped_event_identity(
    tmp_path, source_format,
):
    """Cold 13-family saved reader, not merely in-memory author projection.

    Reuse the exact physical source twice. Change only its response mapping.
    All already-interpreted event identities and values must remain byte-equal;
    one formerly mapped event becomes explicitly uninterpreted without
    changing its original raw witness or losing the source cell.
    """
    from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
    from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
    from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture, build

    root = tmp_path / source_format
    root.mkdir()
    fixture = source_fixture(
        root / "source", source_format=source_format,
        values=(0.0, 1.0, 2.0, 0.0, 1.0),
    )
    altered = deepcopy(fixture["document"])
    altered["response_slots"][0]["values"] = [
        rule for rule in altered["response_slots"][0]["values"]
        if rule["raw_value"] != 2.0
    ]

    def saved(name, config):
        private = root / (name + "-private")
        private.mkdir(mode=0o700)
        certificate = root / (name + ".sqlite")
        sink = SourceSavedBodySink(
            certificate_path=certificate,
            authorized_private_root=private, chunk_rows=2,
        )
        handoff = build(
            root, fixture, name=name + ".sqlite", config=config,
            body_sink=sink, chunk_size=2,
        )
        receipt = sink.receipt
        estate = VerifiedDirectEstate(
            private, exact_path=receipt.path,
            independently_held_manifest_sha256=receipt.manifest_sha256,
            independently_held_i02=receipt.i02,
            current_authorizer=lambda _: True,
        )
        events = list(estate.iter_family("RespondentEvent", batch_size=2))
        assert len(events) == handoff.stats.event_count == fixture["rows"]
        return handoff, events

    full_handoff, full = saved("mapped", fixture["config"])
    partial_handoff, partial = saved("unmapped", SourceConfig(altered))
    assert full_handoff.source_sha256 == partial_handoff.source_sha256
    assert full_handoff.roots.logical != partial_handoff.roots.logical
    assert sum(e.typed_state == "INVALID_UNRESOLVED" for e in partial) == 1

    by_respondent = lambda events: {
        e.scoped_respondent_ref.key: e for e in events
    }
    mapped_by_respondent = by_respondent(full)
    partial_by_respondent = by_respondent(partial)
    assert set(mapped_by_respondent) == set(partial_by_respondent)

    for respondent, event in partial_by_respondent.items():
        original = mapped_by_respondent[respondent]
        assert event.raw_response_value == original.raw_response_value
        if event.typed_state == "INVALID_UNRESOLVED":
            assert original.typed_state == "SUBSTANTIVE_RESPONSE"
            assert event.semantic_fields["uninterpreted_physical_missing_state"] == (
                "OBSERVED_STORAGE_VALUE"
            )
            assert event.semantic_fields["uninterpreted_source_missing_declaration"] is None
            assert len(event.semantic_fields["uninterpreted_physical_cell_key"]) == 64
            assert event.canonical_response_value_if_authorized is None
        else:
            # The response meaning is unchanged, but the source-mapping
            # projection identity is part of a derived semantic event ref.
            # Never confuse that semantic ref with the stable physical cell.
            assert event.typed_state == original.typed_state
            assert (
                event.canonical_response_value_if_authorized
                == original.canonical_response_value_if_authorized
            )
            assert event.scoped_respondent_ref == original.scoped_respondent_ref
            assert "uninterpreted_physical_missing_state" not in event.semantic_fields
            # PF-006: retaining a stable semantic EVENT identity across
            # mapping revisions requires an owner decision; source physical
            # identity is independently protected by the new raw journal.


def test_unmapped_source_missing_classification_never_invents_observed_coverage():
    from rawlsing_next.pre553_physical_decoder import (
        PhysicalCell, PhysicalMissingState,
    )
    from rawlsing_next.pre553_source_i02_handoff import (
        SourceI02Refusal, _unresolved_response_state,
    )
    for state in (
        PhysicalMissingState.SYSTEM_MISSING,
        PhysicalMissingState.FORMAT_USER_MISSING_VALUE,
        PhysicalMissingState.FORMAT_USER_MISSING_RANGE,
        PhysicalMissingState.FORMAT_EXTENDED_MISSING,
        PhysicalMissingState.SOURCE_CELL_ABSENT_OR_UNREPRESENTED,
    ):
        c = PhysicalCell(1, 1, "Q", 42, state, {"kind": "source"})
        assert _unresolved_response_state(c) == "MISSING"
    observed = PhysicalCell(
        1, 1, "Q", 42,
        PhysicalMissingState.OBSERVED_STORAGE_VALUE, None,
    )
    assert _unresolved_response_state(observed) == "INVALID_UNRESOLVED"
    with pytest.raises(SourceI02Refusal, match="UNSUPPORTED_PHYSICAL_MISSING_STATE"):
        _unresolved_response_state(PhysicalCell(
            1, 1, "Q", 42,
            PhysicalMissingState.PHYSICAL_STATE_UNKNOWN, None,
        ))
