"""#1007: actual metadata-grounded physical inputs through the consolidated B path.

The original archived fixture assets are reused exactly. All records and rows
here are TEST_ONLY, not the original waves, original science or permission.
The older fixture direct-estate construction is deliberately preserved; this
court is cross-family delivery, not one-pass ingest or production economics.
"""
from pathlib import Path
import shutil
import sys

import pytest

pytest.importorskip("pyarrow")
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_issued_workload import (
    NativeWorkload, IssuedWorkloadRecord, canonical, operation_jobs,
)
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
from rawlsing_next.pre553_saved_durable_delivery import (
    execute_publish_saved, open_saved_product,
)
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom, _d_auth, _discovery_authority, _grammar, _qt, _rule,
)
from rawlsing_next.tests.test_pre553_empirical_query import _predicate, _response_leaf

sys.path.insert(0, str(Path(__file__).resolve().parents[2] /
                       "WORKER_RETURNS/PYAT1007_DUAL_SERIES_PREP_R1"))
import fixture_harness as h

HOST = "pyat1007-test-only"
PURPOSE = "THREE_SERIES_NATIVE_DURABLE_COURT"
ROWS = {
    "ARAB_SRC07": (1, 2, 3, 6),
    "WVS_SRC35": (1, 2, 3, 4),
    "LITS_SRC28_HOSTILE": (1, 2, 3, 6),
}


def _issue(result):
    """Fixture-only explicit native query issuance; never an original compiler grant."""
    spec = result.spec
    view = h.source_view(result)
    qa = h.query_authority(spec.series_key)
    base = h.build_branch_predicate(result, view, qa, tag="complete-fixture-cohort",
        member_keys=h.respondent_keys(result, ROWS[spec.series_key]))
    positive = h.build_query(result, view, qa, base, spec.positive_questions,
                             domains=spec.scalar_domains, tag="positive")
    negative = h.build_query(result, view, qa, base, spec.route_unknown_questions,
                             domains=spec.scalar_domains, tag="unresolved-routing")
    predicates, queries, discoveries, extra = [base], [positive, negative], [], []
    if spec.series_key == "WVS_SRC35":
        tag = "pyat1007-wvs_src35-discovery"
        da = _d_auth(tag)
        atom = _predicate(view, qa, _response_leaf(view, qa, "Q1", 1), tag="x1")
        unary = h.build_query(result, view, qa, base, ("Q2",),
                              domains=spec.scalar_domains, tag="y")
        grammar = _grammar(operation=f"I03-OP-{tag}",
            atoms=[_atom("ALL", base, "BRANCH"), _atom("X1", atom, "RESPONSE")],
            templates=[_qt("Y", unary)],
            rules=[_rule("pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
                        atom_ids=("X1",), baseline_atom_id="ALL", query_template_id="Y",
                        validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"})])
        discovery = _discovery_authority(view, grammar, da)
        predicates.append(atom)
        queries.append(unary)
        discoveries.append(discovery)
        extra.append(da)
    catalog = h.catalog(result, qa, predicates, queries, discoveries, extra)
    requests = tuple(I03ExecutionRequest(q.ref, base.ref) for q in (positive, negative))
    discovery_refs = tuple(d.ref for d in discoveries)
    doc = result.config.document
    descriptor = {
        "source_edition": result.source_sha256,
        "native_item_ids": list(spec.positive_questions + spec.route_unknown_questions),
        "release_tag": result.projection.instrument_release_id,
        "routing_and_risk": {"routing_facts": len(result.projection.routing)},
        "carrier": {"source_format": doc["identity"]["source_format"], "fixture": spec.fixture_id},
        "country_and_population": {"grade": "NONRESPONDENT_FIXTURE_ONLY"},
        "weight_design_estimand": {"measure": "RAW", "grade": "TEST_ONLY"},
        "missing_and_occurrence_policy": {"grade": "EXACT_FIXTURE_TYPED_STATES"},
        "target_conditioner_roles": {"fixture_queries": [q.ref.as_dict() for q in (positive, negative)]},
    }
    root = semantic_hash({"fixture": spec.fixture_id, "source": result.source_sha256,
                          "projection": result.projection.projection_identity_ref.as_dict()})
    jobs = operation_jobs(requests, discovery_refs)
    frontier = semantic_hash({"test_only_jobs": jobs, "root": root})
    decision = h.ref("TEST_ONLY_DECISION", "urn:pyat1007:fixture:" + frontier)
    workload = NativeWorkload(decision_ref=decision,
        source_factory_ref=h.ref("TEST_ONLY_FACTORY", "urn:pyat1007:fixture:" + result.source_sha256),
        descriptor=canonical(descriptor), projection=result.projection, catalog=catalog,
        requests=requests, discoveries=discovery_refs, original_u_root=root,
        expected_frontier_root=frontier)
    record = IssuedWorkloadRecord(decision_ref=decision,
        source_permission_ref=h.ref("TEST_ONLY_SOURCE_PERMISSION", spec.fixture_id),
        scientific_permission_refs=(h.ref("TEST_ONLY_SCIENCE_PERMISSION", spec.fixture_id),),
        host=HOST, purpose=PURPOSE, source_sha256=result.source_sha256,
        envelope_sha256=semantic_hash(workload.envelope()),
        original_u_root=root, expected_frontier_root=frontier, expected_jobs=jobs,
        currentness="CURRENT_GRANTED", scope="TEST_ONLY_SOURCEFREE",
        native_universe_refs=(view["universe"].ref,))
    return workload, TestOnlyDecisionResolver(record), positive, negative


@pytest.mark.parametrize("key", tuple(ROWS))
def test_three_series_durable_first_consumer(tmp_path, monkeypatch, key):
    metadata = h.load_metadata()
    result = h.build_pipeline(tmp_path/"source", h.SERIES_SPECS[key], metadata)
    assert result.config.document["binding"]["identity_class"] == "NONRESPONDENT_FIXTURE"
    assert result.source_sha256 != metadata["series"][key]["declared_original_source_sha256"]
    workload, resolver, positive, negative = _issue(result)
    # Actual physical source not available during native analytical execution.
    result.fixture_path.unlink()
    publication = execute_publish_saved(
        workload, resolver, host=HOST, purpose=PURPOSE,
        saved_admission_factory=lambda: h.admission(result, workload.catalog),
        root_dir=tmp_path/"products")
    assert publication.complete
    assert publication.batch_census["unit_count"] == 2 + len(workload.discoveries)
    shutil.rmtree(result.receipt.path)
    def forbidden(*a, **k):
        pytest.fail("cold first reader opened C11 or recomputed native results")
    monkeypatch.setattr(SavedC11Admission, "open", forbidden)
    monkeypatch.setattr(DirectEstateI03Session, "_build", forbidden)
    cold = open_saved_product(publication.receipt.root_path,
        expected_root=publication.receipt.root_identity,
        expected_release_ref=result.receipt.reconstructed_v1_release_ref,
        expected_saved_manifest_sha256=result.receipt.manifest_sha256,
        workload=workload, resolver=resolver, host=HOST, purpose=PURPOSE)
    pos = cold.read_s04(positive.ref)
    neg = cold.read_s04(negative.ref)
    fact = pos.first_consumer.execution.facts[0]
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == len(ROWS[key])
    assert neg.first_consumer.execution.facts[0].typed_state == "UNAVAILABLE"
    assert neg.first_consumer.knowledge.material()["state"] == "PRODUCER_TYPED_HELD"
    assert pos.first_consumer.knowledge.material()["state"] == "SUPPORTED_SAMPLE_DESCRIPTIVE"
    if key == "WVS_SRC35":
        read = cold.read_s04(positive.ref, conditioner_index=0)
        assert read.first_consumer.ff01.semantic_projection()["raw_fully_resolved_joint_n"] == 4
        discovery, = cold._closure.discovery_results
        assert discovery.candidate_count == discovery.covered_candidate_count == 1
    else:
        assert not cold._closure.discovery_results
    print("THREE_SERIES_COLD", key, result.config.document["identity"]["source_format"],
          "positive", fact.raw_denominator_support, "unresolved", neg.first_consumer.execution.facts[0].typed_state,
          "units", publication.batch_census["unit_count"], "root", publication.receipt.root_identity,
          "native_seconds", publication.execution_seconds, "archive_seconds", publication.publication_seconds)
