"""Actual executable PYAT1007 EARLY SOURCEFREE FIXTURE PREP courts.

All inputs are repository-generated NONRESPONDENT TEST_ONLY SAV/DTA cells.  The
R157 metadata witness supplies exact selected variable labels/value states; no
original respondent bytes, original source hash, translation, rights, weight or
design issuer is read or invented.
"""
from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fixture_harness as h

from rawlsing_next._pre553_direct_i02_sourcefree import build_sourcefree_direct_i02
from rawlsing_next._pre553_external_i02_certificate import ExternalI02IntegrityError
from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import DiscoveryAuthority, exact_ref
from rawlsing_next.pre553_r157_projection_adapter import (
    SourceConfig,
    SourceConfigurationBindingError,
    SourceConfigurationSchemaError,
    build_governed_c11_projection,
)
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission,
    SavedC11AdmissionError,
)
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_batch,
    execute_saved_i03,
    execute_saved_i05,
)
from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError
from rawlsing_next.tests import test_pre553_discovery_exact as disc
from rawlsing_next.tests import test_pre553_empirical_query as native


POSITIVE_ROWS = {
    "ARAB_SRC07": (1, 2, 3, 6),
    "WVS_SRC35": (1, 2, 3, 4),
    "LITS_SRC28_HOSTILE": (1, 2, 3, 6),
}


@pytest.fixture(scope="module")
def metadata() -> dict:
    return h.load_metadata()


@pytest.fixture(scope="module")
def pipelines(tmp_path_factory, metadata):
    root = tmp_path_factory.mktemp("pyat1007-fixtures").resolve()
    return {
        key: h.build_pipeline(root, spec, metadata, estate_name=f"estate-{key}")
        for key, spec in h.SERIES_SPECS.items()
    }


def _positive_parts(result, rows):
    view = h.source_view(result)
    qauth = h.query_authority(result.spec.series_key)
    predicate = h.build_branch_predicate(
        result, view, qauth, tag="positive",
        member_keys=h.respondent_keys(result, rows),
    )
    targets = result.spec.positive_questions
    query = h.build_query(
        result, view, qauth, predicate, targets,
        domains={target: result.spec.scalar_domains[target] for target in targets},
        tag="positive",
    )
    catalog = h.catalog(result, qauth, (predicate,), (query,))
    return view, qauth, predicate, query, h.admission(result, catalog)


def _fact(result, rows, *, measure="RAW"):
    view, qauth, predicate, query, admission = _positive_parts(result, rows)
    if measure != "RAW":
        query = h.build_query(
            result, view, qauth, predicate, result.spec.positive_questions,
            domains={
                target: result.spec.scalar_domains[target]
                for target in result.spec.positive_questions
            },
            measure=measure, tag="measure",
        )
        admission = h.admission(result, h.catalog(result, qauth, (predicate,), (query,)))
    return execute_saved_i03(
        admission, query_ref=query.ref, predicate_ref=predicate.ref,
    ).facts[0]


def _i05_parts(result, metadata):
    view = h.source_view(result)
    qauth = h.query_authority(result.spec.series_key)
    tag = f"pyat1007-{result.spec.series_key.lower()}-discovery"
    dauth = disc._d_auth(tag)
    allp = h.build_branch_predicate(
        result, view, qauth, tag="all",
        member_keys=h.respondent_keys(result, POSITIVE_ROWS[result.spec.series_key]),
    )
    x1 = native._predicate(
        view, qauth, native._response_leaf(view, qauth, "Q1", 1), tag="x1",
    )
    yq = h.build_query(
        result, view, qauth, allp, ("Q2",),
        domains={"Q2": ("1.0", "2.0", "3.0", "4.0")}, tag="y",
    )
    grammar = disc._grammar(
        operation=f"I03-OP-{tag}",
        atoms=[
            disc._atom("ALL", allp, "BRANCH"),
            disc._atom("X1", x1, "RESPONSE"),
        ],
        templates=[disc._qt("Y", yq)],
        rules=[disc._rule(
            "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="ALL", query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
    )
    base = disc._discovery_authority(view, grammar, dauth)
    authority = DiscoveryAuthority(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=(
            base.producer_replay_locator_or_reference_root
        ),
        **{
            **dict(base.semantic_fields),
            "validation_rules": {
                "rules": ({"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},),
            },
        },
    )
    catalog = h.catalog(result, qauth, (allp, x1), (yq,), (authority,), (dauth,))
    return view, qauth, dauth, allp, x1, yq, authority, catalog


def test_three_series_positive_cold_i03_one_generic_pipeline(pipelines, metadata):
    for key, result in pipelines.items():
        spec = result.spec
        document = result.config.document
        declared_original = metadata["series"][key]["declared_original_source_sha256"]
        assert document["config_purpose"] == "NONRESPONDENT_FIXTURE"
        assert document["binding"]["identity_class"] == "NONRESPONDENT_FIXTURE"
        assert document["binding"]["source_sha256"] != declared_original
        assert document["identity"]["expected_source_sha256"] != declared_original
        assert (
            document["binding"]["fixture_provenance"]["authority_grade"]
            == "NONRESPONDENT_FIXTURE_ONLY"
        )
        assert all("TEST_ONLY" in note for note in document["notes"][:1])
        fact = _fact(result, POSITIVE_ROWS[key])
        assert fact.typed_state == "SUPPORTED", (key, fact.execution_detail)
        assert fact.raw_denominator_support == len(POSITIVE_ROWS[key])
        assert fact.raw_numerator_support == len(POSITIVE_ROWS[key])
        assert fact.execution_detail == "exact governed target distribution resolved"
        _, _, _, _, admission = _positive_parts(result, POSITIVE_ROWS[key])
        binding = admission.binding_receipt()
        assert binding.source_opens == 0
        assert binding.full_c11_repository_builds == 0
        assert binding.persistent_body_corpora == 0
        published = {
            cell["cell"] if isinstance(cell["cell"], str) else tuple(cell["cell"])
            for cell in fact.target_topology["complete_cell_semantic_projection"]
            if cell["cell_state"] == "OBSERVED_POSITIVE"
        }
        assert published
        assert result.receipt.reconstructed_v1_release_ref == h.release_ref(result)
    assert pipelines["LITS_SRC28_HOSTILE"].config.document["identity"]["source_format"] == "DTA"
    assert pipelines["ARAB_SRC07"].config.document["identity"]["source_format"] == "SAV"
    assert pipelines["WVS_SRC35"].config.document["identity"]["source_format"] == "SAV"


def test_route_unknown_is_typed_unavailable_not_zero(pipelines):
    for key, result in pipelines.items():
        target = result.spec.route_unknown_questions[0]
        view = h.source_view(result)
        qauth = h.query_authority(key)
        predicate = h.build_branch_predicate(
            result, view, qauth, tag="all",
            member_keys=h.respondent_keys(result, POSITIVE_ROWS[key]),
        )
        query = h.build_query(
            result, view, qauth, predicate, (target,),
            domains={target: result.spec.scalar_domains[target]}, tag="unknown",
        )
        admission = h.admission(
            result, h.catalog(result, qauth, (predicate,), (query,)),
        )
        fact = execute_saved_i03(
            admission, query_ref=query.ref, predicate_ref=predicate.ref,
        ).facts[0]
        assert fact.typed_state == "UNAVAILABLE"
        assert fact.target_topology["p02_failure_state"] == "RISK_SET_UNAVAILABLE"
        assert "unresolved" in fact.execution_detail
        assert fact.raw_numerator_support == 0


def test_missing_is_not_zero_and_observed_zero_is_exact(pipelines):
    arab = pipelines["ARAB_SRC07"]
    positive = _fact(arab, (1, 2, 3, 6))
    zero_cell = next(
        cell for cell in positive.target_topology["complete_cell_semantic_projection"]
        if cell["cell"] == "0.0"
    )
    assert zero_cell["raw_numerator_support"] == 1
    assert zero_cell["cell_state"] == "OBSERVED_POSITIVE"

    without_zero = _fact(arab, (2, 3, 6))
    zero_absent = next(
        cell for cell in without_zero.target_topology["complete_cell_semantic_projection"]
        if cell["cell"] == "0.0"
    )
    assert zero_absent["raw_numerator_support"] == 0
    assert zero_absent["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
    assert without_zero.raw_denominator_support == 3

    all_rows = _fact(arab, (1, 2, 3, 4, 5, 6))
    assert all_rows.typed_state == "UNRESOLVED"
    assert all_rows.raw_denominator_support == 6
    assert all_rows.raw_numerator_support == 4
    assert "unresolved" in all_rows.execution_detail

    wvs = pipelines["WVS_SRC35"]
    wvs_all = _fact(wvs, (1, 2, 3, 4, 5, 6))
    assert wvs_all.typed_state == "UNRESOLVED"
    assert wvs_all.raw_numerator_support < wvs_all.raw_denominator_support


def test_ranked_occurrence_identity_and_duplicate_refusal(pipelines):
    arab = pipelines["ARAB_SRC07"]
    rank = arab.spec.rank_question
    rank_ref = h.source_view(arab)["qrefs"][rank]
    events = [
        event for event in arab.candidate.respondent_events
        if exact_ref(event.native_question_ref) == rank_ref
    ]
    assert len(events) == 12
    assert len({event.ref.key for event in events}) == 12
    assert {
        event.multiplicity_order_rank_fields["index"] for event in events
    } == {0, 1}
    assert {
        event.multiplicity_order_rank_fields["kind"] for event in events
    } == {"MULTISELECT"}

    view = h.source_view(arab)
    qauth = h.query_authority("ARAB_SRC07")
    predicate = h.build_branch_predicate(
        arab, view, qauth, tag="rank",
        member_keys=h.respondent_keys(arab, (1, 2, 3, 4, 5, 6)),
    )
    query = h.build_query(
        arab, view, qauth, predicate, (rank,),
        domains={rank: arab.spec.scalar_domains[rank]}, tag="rank",
    )
    admission = h.admission(
        arab, h.catalog(arab, qauth, (predicate,), (query,)),
    )
    fact = execute_saved_i03(
        admission, query_ref=query.ref, predicate_ref=predicate.ref,
    ).facts[0]
    assert fact.typed_state == "UNRESOLVED"
    assert fact.target_topology["p02_failure_state"] == "UNSUPPORTED_RESPONSE_TOPOLOGY"

    sections = h.duplicate_occurrence_sections(arab.candidate, arab.projection)
    with pytest.raises(
        ExternalI02IntegrityError,
        match="duplicate sourcefree event occurrence identity",
    ):
        build_sourcefree_direct_i02(
            sections, arab.projection.universes[0].ref,
            arab.root / "duplicate-occurrence.sqlite",
        )


def test_id_grain_key_witness_and_missing_key_typed_unknown(
    pipelines, metadata, tmp_path,
):
    wvs = pipelines["WVS_SRC35"]
    assert len(wvs.row_native_keys) == 6
    assert {value.kind for value in wvs.row_native_keys.values()} == {
        "R157_NONRESPONDENT_FIXTURE_KEY"
    }
    assert len({value.key for value in wvs.row_native_keys.values()}) == 6
    assert all(
        isinstance(
            identity.source_native_respondent_key_ref_or_typed_absence, h.ExactRef
        )
        for identity in wvs.projection.respondents
    )

    arab = pipelines["ARAB_SRC07"]
    assert arab.row_native_keys is None
    assert {
        identity.source_native_respondent_key_ref_or_typed_absence.kind
        for identity in arab.projection.respondents
    } == {"R157_NONRESPONDENT_FIXTURE_ROW"}

    spec = wvs.spec
    path, sha, rows = h.write_fixture_file(
        tmp_path.resolve(), spec, metadata,
        values_override={"S007": (9001.0, None, 9003.0, 9004.0, 9005.0, 9006.0)},
    )
    document = h.build_fixture_config(
        metadata, spec,
        active_source_sha256=sha, row_count=rows,
        source_bytes=path.stat().st_size, source_format="SAV",
        config_id="PYAT1007-WVS-MISSING-KEY-TEST",
        fixture_release_id="PYAT1007_WVS_MISSING_KEY_TEST",
    )
    config = SourceConfig(document)
    incidence = h.decode_fixture_config(config, path)
    keys = h.row_native_keys_from_transport(config, incidence=incidence, batch_size=8)
    assert isinstance(keys[2], TypedAbsence)
    assert keys[2].state == "UNKNOWN"


def test_weight_design_placeholder_is_typed_and_weighted_query_unavailable(pipelines, metadata):
    for key, result in pipelines.items():
        absence = result.candidate.weight_measure_facts_or_typed_absence
        assert isinstance(absence, TypedAbsence)
        assert absence.state == "NOT_APPLICABLE"
        assert metadata["series"][key]["weight_slots_count"] == 0
        fact = _fact(result, POSITIVE_ROWS[key], measure="GOVERNED_WEIGHTED")
        assert fact.typed_state == "UNAVAILABLE"
        assert fact.target_topology["p02_failure_state"] == "MEASURE_UNAVAILABLE"
        assert "weight" in fact.execution_detail


def test_source_current_and_forged_identity_mismatch_refuse(pipelines, metadata, tmp_path):
    spec = h.SERIES_SPECS["ARAB_SRC07"]
    synthetic_original = h.sha256_text(
        "PYAT1007_TEST_ONLY_ORIGINAL_IDENTITY_NOT_READ:SRC07"
    )
    with pytest.raises(ValueError, match="may not reuse"):
        h.build_fixture_config(
            metadata, spec,
            active_source_sha256=synthetic_original, row_count=6,
            source_bytes=100, source_format="SAV",
            config_id="FORGED", fixture_release_id="FORGED",
        )
    arab = pipelines["ARAB_SRC07"]
    with pytest.raises(
        SourceConfigurationBindingError, match="active source SHA differs"
    ):
        build_governed_c11_projection(arab.config, source_sha256="0" * 64)
    forged = json.loads(json.dumps(arab.config.document))
    forged["binding"]["identity_class"] = "ORIGINAL_SOURCE"
    with pytest.raises(SourceConfigurationSchemaError, match="config_purpose"):
        SourceConfig(forged)

    view = h.source_view(arab)
    qauth = h.query_authority("ARAB_SRC07")
    predicate = h.build_branch_predicate(
        arab, view, qauth, tag="p",
        member_keys=h.respondent_keys(arab, (1, 2, 3, 6)),
    )
    query = h.build_query(
        arab, view, qauth, predicate, ("Q508",),
        domains={"Q508": arab.spec.scalar_domains["Q508"]}, tag="q",
    )
    catalog = h.catalog(arab, qauth, (predicate,), (query,))
    allow = {"value": True}
    admission = h.admission(
        arab, catalog, current_authorizer=lambda _roots: allow["value"],
    )
    allow["value"] = False
    with pytest.raises(DirectEstateError, match="current source/operation authority refused"):
        execute_saved_i03(
            admission, query_ref=query.ref, predicate_ref=predicate.ref,
        )
    with pytest.raises(DirectEstateError):
        SavedC11Admission.open(
            root=arab.root, exact_path=arab.receipt.path,
            independently_held_manifest_sha256=arab.receipt.manifest_sha256,
            independently_held_i02=pipelines["WVS_SRC35"].receipt.i02,
            release_ref=arab.receipt.reconstructed_v1_release_ref,
            runtime_catalog=catalog, current_authorizer=lambda _roots: True,
        )


def test_cross_series_joint_query_is_typed_refused(pipelines):
    arab = pipelines["ARAB_SRC07"]
    wvs = pipelines["WVS_SRC35"]
    arab_view = h.source_view(arab)
    wvs_view = h.source_view(wvs)
    assert arab_view["universe"].ref != wvs_view["universe"].ref
    qauth = h.query_authority("ARAB_SRC07")
    predicate = h.build_branch_predicate(
        arab, arab_view, qauth, tag="cross",
        member_keys=h.respondent_keys(arab, (1, 2, 3, 6)),
    )
    query = h.build_query(
        arab, arab_view, qauth, predicate, ("Q508",),
        domains={"Q508": arab.spec.scalar_domains["Q508"]}, tag="cross",
        universe_refs=(arab_view["universe"].ref, wvs_view["universe"].ref),
    )
    admission = h.admission(
        arab, h.catalog(arab, qauth, (predicate,), (query,)),
    )
    with pytest.raises(
        SavedC11AdmissionError,
        match="not the exact admitted estate universe",
    ):
        execute_saved_i03(
            admission, query_ref=query.ref, predicate_ref=predicate.ref,
        )


def test_changed_input_changes_real_fact_and_exact_restore(
    pipelines, metadata, tmp_path,
):
    base = pipelines["ARAB_SRC07"]
    changed = h.build_pipeline(
        tmp_path.resolve(), base.spec, metadata,
        values_override={"Q508": (0.0, 5.0, 9.0, 98.0, 99.0, 3.0)},
        estate_name="changed-arab",
    )
    assert changed.source_sha256 != base.source_sha256
    assert h.release_ref(changed) != h.release_ref(base)
    base_view = h.source_view(base)
    changed_view = h.source_view(changed)
    assert base_view["universe"].ref == changed_view["universe"].ref

    first = _fact(base, (1, 2, 3, 6))
    changed_fact = _fact(changed, (1, 2, 3, 6))
    restored = _fact(base, (1, 2, 3, 6))
    assert first.ref != changed_fact.ref
    assert changed_fact.raw_denominator_support == 4
    changed_cells = {
        cell["cell"]: cell["raw_numerator_support"]
        for cell in changed_fact.target_topology["complete_cell_semantic_projection"]
    }
    assert changed_cells["9.0"] == 1
    assert changed_cells["10.0"] == 0
    assert restored.ref == first.ref
    assert restored.semantic_projection() == first.semantic_projection()


def test_fresh_process_cold_i03_same_persisted_release(pipelines, tmp_path):
    wvs = pipelines["WVS_SRC35"]
    view, qauth, predicate, query, admission = _positive_parts(
        wvs, (1, 2, 3, 4)
    )
    expected = execute_saved_i03(
        admission, query_ref=query.ref, predicate_ref=predicate.ref,
    )
    capsule = tmp_path.resolve() / "pyat1007-capsule.json"
    capsule.write_text(json.dumps({
        "root": str(wvs.root),
        "exact_path": wvs.receipt.path,
        "manifest_sha256": wvs.receipt.manifest_sha256,
        "i02": asdict(wvs.receipt.i02),
        "release": wvs.receipt.reconstructed_v1_release_ref.as_dict(),
        "authorities": [
            authority.as_dict()
            for authority in h.catalog(wvs, qauth, (predicate,), (query,)).authorities
        ],
        "predicate": predicate.as_dict(),
        "query": query.as_dict(),
    }, sort_keys=True), encoding="utf-8")
    child = r"""
import json,sys
from pathlib import Path
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, materialize_public_object
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03
capsule=json.loads(Path(sys.argv[1]).read_text())
query=materialize_public_object(capsule["query"])
predicate=materialize_public_object(capsule["predicate"])
catalog=RuntimeObjectCatalog(
    authorities=tuple(materialize_public_object(v) for v in capsule["authorities"]),
    predicates=(predicate,), queries=(query,), discovery_authorities=(),
)
admission=SavedC11Admission.open(
    root=capsule["root"], exact_path=capsule["exact_path"],
    independently_held_manifest_sha256=capsule["manifest_sha256"],
    independently_held_i02=ExternalI02Roots(**capsule["i02"]),
    release_ref=exact_ref(capsule["release"]), runtime_catalog=catalog,
    current_authorizer=lambda _roots: True,
)
result=execute_saved_i03(admission, query_ref=query.ref, predicate_ref=predicate.ref)
print(json.dumps({
    "fact_refs":[fact.ref.as_dict() for fact in result.facts],
    "projections":[fact.semantic_projection() for fact in result.facts],
}, sort_keys=True))
"""
    completed = subprocess.run(
        [sys.executable, "-c", child, str(capsule)],
        cwd=str(Path(__file__).resolve().parents[3]),
        capture_output=True, text=True, timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout)
    assert observed["fact_refs"] == [fact.ref.as_dict() for fact in expected.facts]
    assert observed["projections"] == [
        json.loads(json.dumps(fact.semantic_projection(), sort_keys=True))
        for fact in expected.facts
    ]


def test_saved_i05_cold_frontier_matches_native_c11_oracle(pipelines):
    wvs = pipelines["WVS_SRC35"]
    _, qauth, dauth, allp, x1, yq, authority, catalog = _i05_parts(wvs, h.load_metadata())
    admission = h.admission(wvs, catalog)
    saved = execute_saved_i05(admission, discovery_authority_ref=authority.ref)

    repository = C11Repository()
    admitted = ingest_c11_source_release(wvs.candidate, repository)
    assert admitted.accepted, admitted.errors
    registry = AuthorityRegistry(tuple(wvs.candidate.authority_snapshots) + (qauth, dauth))
    oracle = execute_exact_bounded_discovery(
        repository=repository,
        discovery_authority=authority,
        authority_registry=registry,
        release_refs=(admitted.release_ref,),
        predicate_catalog=(allp, x1),
        query_template_catalog=(yq,),
    )
    assert saved.candidate_count == oracle.candidate_count
    assert saved.covered_candidate_count == oracle.covered_candidate_count
    assert saved.valid_empty == oracle.valid_empty
    assert tuple(receipt.ref for receipt in saved.receipts) == tuple(
        receipt.ref for receipt in oracle.receipts
    )
    assert tuple(fact.ref for fact in saved.empirical_facts) == tuple(
        fact.ref for fact in oracle.empirical_facts
    )


def test_saved_batch_query_and_discovery_units_complete(pipelines):
    wvs = pipelines["WVS_SRC35"]
    view = h.source_view(wvs)
    qauth = h.query_authority("WVS_SRC35")
    _, _, _, allp, x1, yq, authority, catalog = _i05_parts(wvs, h.load_metadata())
    query = h.build_query(
        wvs, view, qauth, allp, ("Q1",),
        domains={"Q1": ("1.0", "2.0", "3.0", "4.0")}, tag="batch-query",
    )
    catalog = h.catalog(
        wvs, qauth, (allp, x1), (query, yq), (authority,),
        tuple(
            item for item in catalog.authorities
            if item.authority_ref.authority_id.startswith("I03-AUTH-")
        ),
    )
    admission = h.admission(wvs, catalog)
    manifest = BatchManifest((
        BatchUnitSpec("QUERY", query.ref, (h.release_ref(wvs),), (allp.ref,)),
        BatchUnitSpec("DISCOVERY", authority.ref, (h.release_ref(wvs),), ()),
    ))
    runner = execute_saved_batch(
        admission, manifest=manifest,
        predicate_ref_by_query={query.ref.key: allp.ref},
        discovery_authority_ref_by_key={authority.ref.key: authority.ref},
        prior_receipts=(),
    )
    assert len(runner.receipts) == 2
    assert {receipt.state for receipt in runner.receipts} == {"COMPLETED"}
    assert all(receipt.result_refs for receipt in runner.receipts)
