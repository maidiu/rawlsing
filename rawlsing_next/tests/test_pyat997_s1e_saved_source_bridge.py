"""#997 P0: real Q2 SAV/DTA -> frozen S2-C persisted 13-family C11.

The source data are TEST_ONLY generated nonrespondent bytes. These tests do
not grant original35 source/current/issuer rights, measure 100k/6GiB, or claim
S1-C's pending postconsumer fate join is already accepted.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")
pytest.importorskip("pyreadstat")

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalQuerySpec, exact_ref,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate,
)
from rawlsing_next.pre553_source_saved_body_bridge import (
    SourceSavedBodySink,
)
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
from rawlsing_next.tests.test_pyat960_s1e_source_i02 import _build, _fixture
import rawlsing_next.tests.test_pre553_empirical_query as native


def _build_saved(tmp_path: Path, *, name: str = "one",
                 values=(0.0, 1.0, 2.0, 0.0, 1.0),
                 source_format: str = "SAV", sink_cls=SourceSavedBodySink):
    fixture_root = tmp_path / (name + "-source")
    fixture_root.mkdir()
    fixture = _fixture(
        fixture_root, source_format=source_format, values=values,
    )
    private = tmp_path / (name + "-private")
    private.mkdir(mode=0o700)
    certificate = tmp_path / (name + ".sqlite")
    sink = sink_cls(
        certificate_path=certificate,
        authorized_private_root=private,
        chunk_rows=4,
    )
    handoff = _build(
        tmp_path, fixture, name=name + ".sqlite",
        body_sink=sink, chunk_size=4,
    )
    return fixture, handoff, sink, private


def _estate(handoff, sink, private, guard=lambda _roots: True):
    return VerifiedDirectEstate(
        private, exact_path=sink.receipt.path,
        independently_held_manifest_sha256=sink.receipt.manifest_sha256,
        independently_held_i02=handoff.roots,
        current_authorizer=guard,
    )


def _native_i03(admitted: SavedC11Admission, *, tag: str):
    """Run the accepted S2-D real I03 on the *saved Q2 physical source*."""
    estate = admitted._estate  # read-only first-reader test harness
    universe = next(estate.iter_family("EmpiricalUniverse"))
    respondents = tuple(estate.iter_family("RespondentIdentity"))
    events = tuple(estate.iter_family("RespondentEvent"))
    assert events
    first = events[0]
    native_question = exact_ref(first.native_question_ref)
    routing = tuple(estate.iter_family("RoutingEligibilityFact"))
    eligible_routing = [
        r for r in routing
        if exact_ref(r.question_or_target_ref) == native_question
    ]
    assert eligible_routing
    risk_ref = exact_ref(eligible_routing[0].risk_set_ref)
    snapshots = tuple(estate.iter_family("AuthoritySnapshot"))
    source_authority = next(
        a for a in snapshots if a.authority_ref == first.authority_snapshot_refs[0]
    )
    source = {
        "universe": universe,
        "respondents": {r.ref.key: r for r in respondents},
        "qrefs": {"Y": native_question},
        "risk_refs": {"R": risk_ref},
        "source_auth": source_authority,
    }
    grammar = native._query_authority(tag)
    predicate = native._branch_predicate(source, grammar, tag=tag)
    proposed = native._query(source, grammar, predicate, ("Y",), tag=tag)
    # The physical fixture's exact response domain is 0.0 / 1.0 / 2.0,
    # not the unrelated native test helper's default domain ['0','1'].
    domain = sorted({str(e.raw_response_value) for e in events})
    topology = dict(proposed.target_arity_and_topology)
    topology["components"] = [
        {**dict(component), "domain": domain}
        for component in proposed.target_arity_and_topology["components"]
    ]
    query = EmpiricalQuerySpec(
        typed_state=proposed.typed_state,
        authority_snapshot_refs=proposed.authority_snapshot_refs,
        dependency_refs=proposed.dependency_refs,
        producer_replay_locator_or_reference_root=(
            proposed.producer_replay_locator_or_reference_root
        ),
        **{**dict(proposed.semantic_fields), "target_arity_and_topology": topology},
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*snapshots, grammar)),
        predicates=(predicate,),
        queries=(query,),
        discovery_authorities=(),
    )
    # Reopen using exact independent roots and original accepted S2-D facade.
    re_admitted = SavedC11Admission.open(
        root=estate.root, exact_path=estate.directory,
        independently_held_manifest_sha256=estate.held_manifest_sha256,
        independently_held_i02=estate.i02,
        release_ref=admitted.release_ref,
        runtime_catalog=catalog,
        current_authorizer=estate._authorize,
    )
    result = re_admitted.execute_i03(
        query_ref=query.ref, predicate_ref=predicate.ref,
    )
    return result, {str(e.raw_response_value) for e in events}


def test_q2_one_sav_to_complete_cold_saved_thirteen_families(tmp_path, monkeypatch):
    import rawlsing_next.pre553_physical_decoder as decoder
    snapshot = decoder._acquire_source_snapshot
    opens = []
    monkeypatch.setattr(
        decoder, "_acquire_source_snapshot",
        lambda *a, **kw: opens.append(1) or snapshot(*a, **kw),
    )
    # A direct writer must never slip into the legacy full object C11 graph.
    with monkeypatch.context() as guard:
        guard.setattr(
            C11Repository, "__init__",
            lambda *_a, **_k: (_ for _ in ()).throw(
                AssertionError("legacy full C11 construction forbidden")
            ),
        )
        fixture, handoff, sink, private = _build_saved(tmp_path)
    assert opens == [1]
    assert handoff.stats.source_reads == 1
    assert handoff.stats.decode_calls == 1
    assert handoff.stats.cell_passes == 1
    assert handoff.stats.full_c11_builds == 0
    assert handoff.body_transport["families"] == sink.stats["family_yields"]
    assert sink.stats["body_objects"] > 0
    assert sink.stats["second_i02_certification_in_frozen_writer"]
    assert sink.receipt.i02 == handoff.roots
    assert sink.receipt.family_counts == {
        k: v for k, v in handoff.counts.items() if k in ALL_FAMILIES
    }
    assert not list(private.glob(".s1e-body-journal-*"))
    assert not list(private.glob(".s2c-stage-*"))
    assert len(list(Path(sink.receipt.path).glob("*.parquet"))) == 14
    assert not list(Path(sink.receipt.path).glob("*.sqlite"))
    estate = _estate(handoff, sink, private)
    for family in ALL_FAMILIES:
        assert sum(1 for _ in estate.iter_family(family, batch_size=2)) == (
            sink.receipt.family_counts[family]
        )
    assert estate.reconstructed_v1_release_ref == sink.receipt.reconstructed_v1_release_ref
    assert handoff.census_audit["fate_counts"]["HELD"] > 0
    assert handoff.census_audit["fate_counts"]["ELIGIBLE"] > 0


@pytest.mark.parametrize("source_format", ["SAV", "DTA"])
def test_changed_source_cell_changes_saved_native_events_then_exact_restore(
    tmp_path, source_format,
):
    baseline = _build_saved(
        tmp_path, name="baseline", source_format=source_format,
        values=(0.0, 1.0, 2.0, 0.0, 1.0),
    )
    changed = _build_saved(
        tmp_path, name="changed", source_format=source_format,
        values=(0.0, 1.0, 1.0, 0.0, 1.0),
    )
    restored = _build_saved(
        tmp_path, name="restored", source_format=source_format,
        values=(0.0, 1.0, 2.0, 0.0, 1.0),
    )
    a, b, c = (x[1] for x in (baseline, changed, restored))
    assert a.roots.logical != b.roots.logical
    assert a.roots.logical == c.roots.logical
    def evidence(bundle):
        _, handoff, sink, root = bundle
        estate = _estate(handoff, sink, root)
        return tuple(sorted(
            (e.scoped_respondent_ref, e.raw_response_value, e.response_state)
            for e in estate.iter_family("RespondentEvent")
        ))
    assert evidence(baseline) != evidence(changed)
    assert evidence(baseline) == evidence(restored)
    assert a.manifest.source_artifact_ref == c.manifest.source_artifact_ref
    assert a.manifest.source_artifact_ref != b.manifest.source_artifact_ref


def test_cold_saved_real_native_i03_from_exact_q2_source(tmp_path):
    _, handoff, sink, root = _build_saved(tmp_path)
    estate = _estate(handoff, sink, root)
    # The empty bootstrap catalog is accepted only as a binding. The actual
    # query catalog is source-bound and constructed from saved physical bodies.
    catalog = RuntimeObjectCatalog(
        authorities=tuple(estate.iter_family("AuthoritySnapshot")),
        predicates=(), queries=(), discovery_authorities=(),
    )
    admission = SavedC11Admission.open(
        root=root, exact_path=sink.receipt.path,
        independently_held_manifest_sha256=sink.receipt.manifest_sha256,
        independently_held_i02=handoff.roots,
        release_ref=sink.receipt.reconstructed_v1_release_ref,
        runtime_catalog=catalog,
        current_authorizer=lambda _: True,  # TEST_ONLY only, never production grant
    )
    result, raw_domain = _native_i03(admission, tag="PYAT997-SAVED-Q2")
    assert result.facts
    fact = result.facts[0]
    assert fact.raw_denominator_support > 0
    assert raw_domain
    assert sum(
        int(c["raw_numerator_support"])
        for c in fact.target_topology["complete_cell_semantic_projection"]
    ) == fact.raw_denominator_support


class _DropOneJournalBody(SourceSavedBodySink):
    def _rows(self, family):
        for ordinal, body in enumerate(super()._rows(family)):
            if family == "RespondentEvent" and ordinal == 0:
                continue
            yield body


def test_q2_fail_closed_on_missing_saved_body_and_cleans_stage(tmp_path):
    fixture_root = tmp_path / "input"
    fixture_root.mkdir()
    fixture = _fixture(fixture_root)
    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    sink = _DropOneJournalBody(
        certificate_path=tmp_path / "bad.sqlite",
        authorized_private_root=private, chunk_rows=4,
    )
    with pytest.raises(Exception):
        _build(tmp_path, fixture, name="bad.sqlite", body_sink=sink, chunk_size=4)
    assert not (tmp_path / "bad.sqlite").exists()
    assert not list(private.glob(".s1e-body-journal-*"))
    assert not list(private.glob(".s2c-stage-*"))
    assert not list(private.glob("releases/*/manifest.json"))


def test_wrong_held_root_and_revoked_source_refuse_native_cold(tmp_path):
    _, handoff, sink, root = _build_saved(tmp_path)
    with pytest.raises(DirectEstateError):
        VerifiedDirectEstate(
            root, exact_path=sink.receipt.path,
            independently_held_manifest_sha256="0" * 64,
            independently_held_i02=handoff.roots,
            current_authorizer=lambda _: True,
        )
    state = {"current": True}
    estate = _estate(handoff, sink, root, lambda _: state["current"])
    assert sum(1 for _ in estate.iter_family("RespondentEvent")) > 0
    state["current"] = False
    with pytest.raises(DirectEstateError, match="current source/operation authority refused"):
        list(estate.iter_family("RespondentEvent"))
