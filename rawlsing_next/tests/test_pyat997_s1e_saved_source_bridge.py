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
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_r157_projection_adapter import (
    SourceConfig, build_governed_c11_projection,
)
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission, SavedReleaseIdentity,
)
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate,
)
from rawlsing_next.pre553_source_saved_body_bridge import (
    SourceSavedBodySink,
)
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
from rawlsing_next.tests.test_pyat960_s1e_native_fact import (
    _compile_native, _native_document,
)
from rawlsing_next.tests.test_pyat960_s1e_source_i02 import _build, _fixture
from rawlsing_next.tests.test_pyat960_s1e_support import build
from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import (
    _freeze_packet,
)
from rawlsing_next.tests.test_universal_grammar import _frontier, _policy


def _native_fixture_for(root: Path, *, source_format: str, values):
    fixture_root = root / "source"
    fixture_root.mkdir(parents=True, exist_ok=True)
    path, source_sha, rows, _cfg, document, inventory, _policy0, _fr, _census = (
        _fixture(fixture_root, source_format=source_format, values=values)
    )
    document = _native_document(document)
    config = SourceConfig(document)
    projection = build_governed_c11_projection(config)
    risk_set_ref = exact_ref(
        projection.routing[0].risk_set_ref, "risk_set_ref")
    occurrences = tuple(
        replace(occurrence, risk_set_refs=(risk_set_ref.key,))
        for occurrence in inventory.occurrences
    )
    inventory = replace(
        inventory,
        occurrences=occurrences,
        risk_set_refs=(risk_set_ref.key,),
        inventory_id="PYAT997-S1E-EXACT-RESTORE",
    )
    policy = _policy(j=1, k=1, d=0)
    frontier = _frontier(inventory, policy)
    census = _freeze_packet(frontier)
    return {
        "path": path, "source_sha": source_sha, "rows": rows,
        "config": config, "document": document, "inventory": inventory,
        "policy": policy, "frontier": frontier, "census": census,
        "projection": projection,
    }


def _build_saved(tmp_path: Path, *, name: str = "one",
                 values=(0.0, 1.0, 2.0, 0.0, 1.0),
                 source_format: str = "SAV", sink_cls=SourceSavedBodySink,
                 source_fixture=None):
    tmp_path.mkdir(parents=True, exist_ok=True)
    if source_fixture is None:
        fixture_root = tmp_path / (name + "-source")
        fixture_root.mkdir(parents=True, exist_ok=True)
        fixture = _native_fixture_for(
            fixture_root, source_format=source_format, values=values,
        )
    else:
        fixture = source_fixture
    private = tmp_path / (name + "-private")
    private.mkdir(mode=0o700)
    certificate = tmp_path / (name + ".sqlite")
    sink = sink_cls(
        certificate_path=certificate,
        authorized_private_root=private,
        chunk_rows=4,
    )
    handoff = build(
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


def _native_i03(estate: VerifiedDirectEstate, *, tag: str, handoff, fixture):
    """Run the exact compiled q101 native I03 on the saved Q2 physical source.

    The compiled plan contains q101 question queries and separate country
    coordinate queries. The former is the intended response target; the latter
    must remain a typed negative witness, not be erased by query cherry-picking.
    """
    events = tuple(estate.iter_family("RespondentEvent"))
    assert events
    release_identity = SavedReleaseIdentity(
        estate.reconstructed_v1_release_ref)
    compilation = _compile_native(
        fixture, handoff, fixture["projection"], release_identity)
    catalog = compilation.issued.workload.catalog
    re_admitted = SavedC11Admission.open(
        root=estate.root, exact_path=estate.directory,
        independently_held_manifest_sha256=estate.held_manifest_sha256,
        independently_held_i02=estate.i02,
        release_ref=estate.reconstructed_v1_release_ref,
        runtime_catalog=catalog,
        current_authorizer=estate._authorize,
    )
    intended = None
    negatives = []
    for entry in compilation.plan.records:
        if entry.status != "SUPPORTED":
            continue
        for raw in entry.query_refs:
            if isinstance(raw, dict):
                raw = {
                    key: raw[key] for key in
                    ("kind", "object_id", "content_hash")
                }
            query_ref = exact_ref(raw, "compiled query")
            query = catalog.resolve_query_exact(query_ref)
            predicate_ref = exact_ref(
                query.condition_predicate_ref, "compiled predicate")
            result = re_admitted.execute_i03(
                query_ref=query_ref, predicate_ref=predicate_ref)
            if not result.facts:
                continue
            fact = result.facts[0]
            targets = tuple(exact_ref(target) for target in query.target_refs)
            is_q101 = any(
                target.kind == "QUESTION_NATIVE"
                and target.object_id.endswith(":q101")
                for target in targets
            )
            if is_q101 and fact.typed_state == "SUPPORTED":
                intended = result
            elif any(
                target.kind == "COORDINATE_NATIVE"
                for target in targets
            ):
                negatives.append(fact)
    if intended is None:
        pytest.fail("compiled q101 native I03 first reader is unavailable")
    fact = intended.facts[0]
    assert fact.raw_denominator_support == 5
    assert sum(
        int(cell["raw_numerator_support"])
        for cell in fact.target_topology["complete_cell_semantic_projection"]
    ) == 5
    assert any(
        negative.typed_state == "UNAVAILABLE"
        and negative.target_topology.get("p02_failure_state")
        == "RISK_SET_UNAVAILABLE"
        for negative in negatives
    )
    return intended, {str(e.raw_response_value) for e in events}, negatives


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
        values=(0.0, 1.0, 0.0, 1.0, 0.0),
    )
    changed = _build_saved(
        tmp_path, name="changed", source_format=source_format,
        values=(0.0, 1.0, 1.0, 0.0, 1.0),
    )
    restored = _build_saved(
        tmp_path, name="restored", source_format=source_format,
        source_fixture=baseline[0],
    )
    a, b, c = (x[1] for x in (baseline, changed, restored))
    assert a.roots.logical != b.roots.logical
    assert a.roots.logical == c.roots.logical
    def evidence(bundle):
        _, handoff, sink, root = bundle
        estate = _estate(handoff, sink, root)
        return tuple(sorted(
            (exact_ref(e.scoped_respondent_ref).key, e.raw_response_value, e.response_state)
            for e in estate.iter_family("RespondentEvent")
        ))
    assert evidence(baseline) != evidence(changed)
    assert evidence(baseline) == evidence(restored)
    assert a.manifest.source_artifact_ref == c.manifest.source_artifact_ref
    assert a.manifest.source_artifact_ref != b.manifest.source_artifact_ref
    # Real saved native I03 (same test query/target domain): material change,
    # not just altered source SHA or altered Parquet bytes.
    def native_cells(bundle):
        fixture, handoff, sink, root = bundle
        estate = _estate(handoff, sink, root)
        result, _, negatives = _native_i03(
            estate, tag="PYAT997-CHANGED-SOURCE",
            handoff=handoff, fixture=fixture,
        )
        assert result.facts and result.facts[0].typed_state == "SUPPORTED"
        assert negatives
        fact = result.facts[0]
        return tuple(
            (str(cell["cell"]), cell["raw_numerator_support"])
            for cell in fact.target_topology["complete_cell_semantic_projection"]
        )
    assert native_cells(baseline) != native_cells(changed)
    assert native_cells(baseline) == native_cells(restored)


def test_cold_saved_real_native_i03_from_exact_q2_source(tmp_path):
    fixture, handoff, sink, root = _build_saved(
        tmp_path, values=(0.0, 1.0, 0.0, 1.0, 0.0))
    estate = _estate(handoff, sink, root)
    result, raw_domain, negatives = _native_i03(
        estate, tag="PYAT997-SAVED-Q2", handoff=handoff, fixture=fixture)
    assert result.facts
    fact = result.facts[0]
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 5
    assert raw_domain
    assert negatives
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
