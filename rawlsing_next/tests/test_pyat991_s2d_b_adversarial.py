"""S2-D Role-B hostile corrective tests on A's same saved-admission descendant.

The tests exercise the actual accepted S2-C estate through the existing native
I03/I05 owners.  They do not fake the five shared-owner readers.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

pytest.importorskip("pyarrow")

import rawlsing_next.tests.test_pre553_direct_estate_i03 as s2c
import rawlsing_next.tests.test_pre553_discovery_exact as dt
import rawlsing_next.tests.test_pre553_empirical_query as native
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_empirical_objects import (
    DiscoveryAuthority,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    exact_ref,
)
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission,
    SavedC11AdmissionError,
)
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_i03,
    execute_saved_i05,
)
from rawlsing_next.tests.test_pyat991_s2d_saved_admission import (
    _admission,
    _i03_parts,
    _i05_parts,
    _source_with_candidate,
)


def _combine_catalogs(*catalogs):
    return RuntimeObjectCatalog(
        authorities=tuple(sorted({
            obj.authority_ref.key: obj
            for catalog in catalogs for obj in catalog.authorities
        }.values(), key=lambda obj: obj.authority_ref.key)),
        predicates=tuple(sorted({
            obj.ref.key: obj
            for catalog in catalogs for obj in catalog.predicates
        }.values(), key=lambda obj: obj.ref.key)),
        queries=tuple(sorted({
            obj.ref.key: obj
            for catalog in catalogs for obj in catalog.queries
        }.values(), key=lambda obj: obj.ref.key)),
        discovery_authorities=tuple(sorted({
            obj.ref.key: obj
            for catalog in catalogs for obj in catalog.discovery_authorities
        }.values(), key=lambda obj: obj.ref.key)),
    )


def _multi_i05_parts(source, tag):
    qauth = native._query_authority(tag)
    dauth = dt._d_auth(f"{tag}-discovery")
    all_p = native._branch_predicate(source, qauth, tag=f"{tag}-all")
    x1 = native._predicate(
        source, qauth, native._response_leaf(source, qauth, "X", 1),
        tag=f"{tag}-x1",
    )
    x0 = native._predicate(
        source, qauth, native._response_leaf(source, qauth, "X", 0),
        tag=f"{tag}-x0",
    )
    yq = native._query(source, qauth, all_p, ("Y",), tag=f"{tag}-y")
    grammar = dt._grammar(
        operation=f"I03-OP-{tag}-discovery",
        atoms=[
            dt._atom("ALL", all_p, "BRANCH"),
            dt._atom("X1", x1, "RESPONSE"),
            dt._atom("X0", x0, "RESPONSE"),
        ],
        templates=[dt._qt("Y", yq)],
        rules=[
            dt._rule(
                "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
                atom_ids=("X1",), baseline_atom_id="ALL",
                query_template_id="Y",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            ),
            dt._rule(
                "minority", "MINORITY_OR_NONMODAL_DEPARTURE", "SINGLE_ATOM",
                atom_ids=("X0",), baseline_atom_id="ALL",
                query_template_id="Y",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            ),
        ],
    )
    base = dt._discovery_authority(source, grammar, dauth)
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
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth, dauth)),
        predicates=(all_p, x1, x0),
        queries=(yq,),
        discovery_authorities=(authority,),
    )
    return qauth, dauth, all_p, x1, x0, yq, authority, catalog


def _i03_sig(result):
    return (
        result.query_ref,
        tuple(result.release_refs),
        tuple(fact.semantic_projection() for fact in result.facts),
        tuple(fact.ref for fact in result.facts),
    )


def _i05_sig(result):
    return (
        result.candidate_count,
        result.covered_candidate_count,
        result.valid_empty,
        result.discovery_authority_ref,
        result.candidate_grammar_ref,
        result.evaluated_frontier_ref,
        result.replay_ref,
        tuple(result.empirical_fact_refs),
        tuple(f.ref for f in result.empirical_facts),
        tuple(f.semantic_projection() for f in result.empirical_facts),
        tuple(r.ref for r in result.receipts),
        tuple(r.semantic_projection() for r in result.receipts),
        tuple(o.ref for o in result.executed_predicates),
        tuple(o.ref for o in result.executed_queries),
    )


def test_b_i03_changed_native_rows_and_exact_restore(tmp_path, monkeypatch):
    tag = "S2D-B-I03-CHANGE"
    base_source, base_candidate = _source_with_candidate(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    changed_source, changed_candidate = _source_with_candidate(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 0}}],
    )
    qauth, predicate, query, catalog = _i03_parts(base_source, tag)
    base_oracle = native._run(base_source, qauth, predicate, query)
    changed_oracle = native._run(changed_source, qauth, predicate, query)
    base_root, base_receipt = s2c._cold(
        tmp_path, base_candidate, base_source["universe"].ref, "base-i03"
    )
    changed_root, changed_receipt = s2c._cold(
        tmp_path, changed_candidate, changed_source["universe"].ref, "changed-i03"
    )
    base_admission = _admission(base_root, base_receipt, base_source, catalog)
    changed_admission = _admission(
        changed_root, changed_receipt, changed_source, catalog
    )
    base = execute_saved_i03(
        base_admission, query_ref=query.ref, predicate_ref=predicate.ref
    )
    changed = execute_saved_i03(
        changed_admission, query_ref=query.ref, predicate_ref=predicate.ref
    )
    restored = execute_saved_i03(
        base_admission, query_ref=query.ref, predicate_ref=predicate.ref
    )
    assert _i03_sig(base) == _i03_sig(base_oracle)
    assert _i03_sig(changed) == _i03_sig(changed_oracle)
    assert _i03_sig(restored) == _i03_sig(base)
    assert changed.facts[0].ref != base.facts[0].ref
    assert changed.facts[0].semantic_projection() != base.facts[0].semantic_projection()


def test_b_i03_zero_support_negative_parity(tmp_path, monkeypatch):
    source, candidate = _source_with_candidate(
        monkeypatch, "S2D-B-I03-ZERO",
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    qauth = native._query_authority("S2D-B-I03-ZERO")
    empty = native._branch_predicate(source, qauth, members=(), tag="empty")
    query = native._query(source, qauth, empty, ("Y",), tag="zero")
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth)),
        predicates=(empty,), queries=(query,), discovery_authorities=(),
    )
    oracle = native._run(source, qauth, empty, query)
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "zero-i03"
    )
    admission = _admission(root, receipt, source, catalog)
    observed = execute_saved_i03(
        admission, query_ref=query.ref, predicate_ref=empty.ref
    )
    assert _i03_sig(observed) == _i03_sig(oracle)
    assert observed.facts[0].typed_state == "ZERO_SUPPORT"
    assert observed.facts[0].raw_denominator_support == 0


def test_b_i05_changed_native_rows_multi_frontier_and_exact_restore(
    tmp_path, monkeypatch,
):
    tag = "S2D-B-I05-CHANGE"
    base_source, base_candidate = _source_with_candidate(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"X": 1, "Y": 1}},
         {"id": "R2", "responses": {"X": 0, "Y": 0}},
         {"id": "R3", "responses": {"X": 0, "Y": 1}}],
    )
    changed_source, changed_candidate = _source_with_candidate(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"X": 0, "Y": 1}},
         {"id": "R2", "responses": {"X": 1, "Y": 0}},
         {"id": "R3", "responses": {"X": 0, "Y": 1}}],
    )
    qauth, dauth, all_p, x1, x0, yq, authority, catalog = _multi_i05_parts(
        base_source, tag
    )
    base_oracle = execute_exact_bounded_discovery(
        repository=base_source["repo"], discovery_authority=authority,
        authority_registry=native._registry(base_source, qauth, dauth),
        release_refs=(base_source["release_ref"],),
        predicate_catalog=(all_p, x1, x0),
        query_template_catalog=(yq,),
    )
    changed_oracle = execute_exact_bounded_discovery(
        repository=changed_source["repo"], discovery_authority=authority,
        authority_registry=native._registry(changed_source, qauth, dauth),
        release_refs=(changed_source["release_ref"],),
        predicate_catalog=(all_p, x1, x0),
        query_template_catalog=(yq,),
    )
    base_root, base_receipt = s2c._cold(
        tmp_path, base_candidate, base_source["universe"].ref, "base-i05"
    )
    changed_root, changed_receipt = s2c._cold(
        tmp_path, changed_candidate, changed_source["universe"].ref,
        "changed-i05",
    )
    base_admission = _admission(base_root, base_receipt, base_source, catalog)
    changed_admission = _admission(
        changed_root, changed_receipt, changed_source, catalog
    )
    base = execute_saved_i05(
        base_admission, discovery_authority_ref=authority.ref
    )
    changed = execute_saved_i05(
        changed_admission, discovery_authority_ref=authority.ref
    )
    restored = execute_saved_i05(
        base_admission, discovery_authority_ref=authority.ref
    )
    assert _i05_sig(base) == _i05_sig(base_oracle)
    assert _i05_sig(changed) == _i05_sig(changed_oracle)
    assert _i05_sig(restored) == _i05_sig(base)
    assert base.candidate_count == 2
    assert changed.replay_ref != base.replay_ref


def test_b_i05_negative_valid_empty_parity(tmp_path, monkeypatch):
    source, candidate = _source_with_candidate(
        monkeypatch, "S2D-B-I05-NEG",
        [{"id": "R1", "responses": {"X": 1, "Y": 0}},
         {"id": "R2", "responses": {"X": 0, "Y": 0}}],
    )
    qauth, dauth, all_p, x1, yq, authority, catalog = _i05_parts(
        source, "S2D-B-I05-NEG"
    )
    oracle = execute_exact_bounded_discovery(
        repository=source["repo"], discovery_authority=authority,
        authority_registry=native._registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=(all_p, x1), query_template_catalog=(yq,),
    )
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "neg-i05"
    )
    admission = _admission(root, receipt, source, catalog)
    observed = execute_saved_i05(
        admission, discovery_authority_ref=authority.ref
    )
    assert _i05_sig(observed) == _i05_sig(oracle)
    assert observed.valid_empty == oracle.valid_empty
    assert tuple(r.typed_state for r in observed.receipts) == tuple(
        r.typed_state for r in oracle.receipts
    )


def test_b_mixed_universe_is_hard_refused_and_valid_path_restored(
    tmp_path, monkeypatch,
):
    base_source, base_candidate = _source_with_candidate(
        monkeypatch, "S2D-B-MIX-A",
        [{"id": "R1", "responses": {"X": 1, "Y": 1}},
         {"id": "R2", "responses": {"X": 0, "Y": 0}}],
    )
    foreign_source, foreign_candidate = _source_with_candidate(
        monkeypatch, "S2D-B-MIX-B",
        [{"id": "Q1", "responses": {"X": 1, "Y": 0}},
         {"id": "Q2", "responses": {"X": 0, "Y": 1}}],
    )
    qa, pred, query, base_i03_catalog = _i03_parts(base_source, "S2D-B-MIX-A")
    qa2, pred2, query2, foreign_i03_catalog = _i03_parts(
        foreign_source, "S2D-B-MIX-B"
    )
    combined_i03 = _combine_catalogs(base_i03_catalog, foreign_i03_catalog)
    root, receipt = s2c._cold(
        tmp_path, base_candidate, base_source["universe"].ref, "mixed"
    )
    admission = _admission(root, receipt, base_source, combined_i03)
    base = execute_saved_i03(
        admission, query_ref=query.ref, predicate_ref=pred.ref
    )
    with pytest.raises(SavedC11AdmissionError, match="universe"):
        execute_saved_i03(
            admission, query_ref=query2.ref, predicate_ref=pred2.ref
        )
    assert execute_saved_i03(
        admission, query_ref=query.ref, predicate_ref=pred.ref
    ).facts[0].ref == base.facts[0].ref

    # A query that names the estate universe but also a foreign scope is a
    # mixed-scope positive unless the saved admission binds the exact scope.
    query_fields = dict(query.semantic_fields)
    query_fields["scope_refs"] = tuple(sorted({
        *(exact_ref(dict(value)) for value in query_fields["scope_refs"]),
        foreign_source["universe"].ref,
    }, key=lambda ref: ref.key))
    mixed_scope_query = EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=(
            query.producer_replay_locator_or_reference_root
        ),
        **query_fields,
    )
    # A predicate with an extra foreign scope must also be refused even when the
    # query itself is exact.
    predicate_fields = dict(pred.semantic_fields)
    predicate_fields["scope_refs"] = tuple(sorted({
        *(exact_ref(dict(value)) for value in predicate_fields["scope_refs"]),
        foreign_source["universe"].ref,
    }, key=lambda ref: ref.key))
    mixed_scope_predicate = EmpiricalPredicate(
        typed_state=pred.typed_state,
        authority_snapshot_refs=pred.authority_snapshot_refs,
        dependency_refs=pred.dependency_refs,
        producer_replay_locator_or_reference_root=(
            pred.producer_replay_locator_or_reference_root
        ),
        **predicate_fields,
    )
    mixed_predicate_query_fields = dict(query.semantic_fields)
    mixed_predicate_query_fields["condition_predicate_ref"] = (
        mixed_scope_predicate.ref
    )
    mixed_predicate_query = EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=(mixed_scope_predicate.ref,),
        producer_replay_locator_or_reference_root=(
            query.producer_replay_locator_or_reference_root
        ),
        **mixed_predicate_query_fields,
    )
    mixed_catalog = _combine_catalogs(
        base_i03_catalog,
        foreign_i03_catalog,
        RuntimeObjectCatalog(
            authorities=combined_i03.authorities,
            predicates=(pred, mixed_scope_predicate),
            queries=(query, mixed_scope_query, mixed_predicate_query),
            discovery_authorities=(),
        ),
    )
    mixed_admission = _admission(root, receipt, base_source, mixed_catalog)
    assert execute_saved_i03(
        mixed_admission, query_ref=query.ref, predicate_ref=pred.ref
    ).facts[0].ref == base.facts[0].ref
    with pytest.raises(SavedC11AdmissionError, match="scope"):
        execute_saved_i03(
            mixed_admission,
            query_ref=mixed_scope_query.ref,
            predicate_ref=pred.ref,
        )
    with pytest.raises(SavedC11AdmissionError, match="scope"):
        execute_saved_i03(
            mixed_admission,
            query_ref=mixed_predicate_query.ref,
            predicate_ref=mixed_scope_predicate.ref,
        )

    qa3, dauth, all_p, x1, yq, authority, base_i05_catalog = _i05_parts(
        base_source, "S2D-B-MIX-A-I05"
    )
    qa4, dauth4, all_p4, x14, yq4, foreign_authority, foreign_i05_catalog = (
        _i05_parts(foreign_source, "S2D-B-MIX-B-I05")
    )
    combined_i05 = _combine_catalogs(base_i05_catalog, foreign_i05_catalog)
    admission5 = _admission(root, receipt, base_source, combined_i05)
    base5 = execute_saved_i05(
        admission5, discovery_authority_ref=authority.ref
    )
    with pytest.raises(SavedC11AdmissionError, match="universe"):
        execute_saved_i05(
            admission5, discovery_authority_ref=foreign_authority.ref
        )
    assert tuple(r.ref for r in execute_saved_i05(
        admission5, discovery_authority_ref=authority.ref
    ).receipts) == tuple(r.ref for r in base5.receipts)


def test_b_admission_binding_is_immutable_and_estate_snapshot_private(
    tmp_path, monkeypatch,
):
    source, candidate = _source_with_candidate(
        monkeypatch, "S2D-B-IMMUT",
        [{"id": "R1", "responses": {"X": 1, "Y": 1}},
         {"id": "R2", "responses": {"X": 0, "Y": 0}}],
    )
    qa, pred, query, catalog = _i03_parts(source, "S2D-B-IMMUT")
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "immut"
    )
    admission = _admission(root, receipt, source, catalog)
    base = execute_saved_i03(
        admission, query_ref=query.ref, predicate_ref=pred.ref
    )
    for name, value in (
        ("release_ref", source["release_ref"]),
        ("runtime_catalog", catalog),
        ("_estate", admission._estate),
        ("estate", admission._estate),
    ):
        with pytest.raises(SavedC11AdmissionError):
            setattr(admission, name, value)

    held_roots = ExternalI02Roots(
        logical=receipt.i02.logical,
        physical=receipt.i02.physical,
        release=receipt.i02.release,
        source=receipt.i02.source,
        replay=receipt.i02.replay,
        universe=receipt.i02.universe,
        schema=receipt.i02.schema,
    )
    original = VerifiedDirectEstate(
        root,
        exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=held_roots,
        current_authorizer=lambda _roots: True,
    )
    direct = SavedC11Admission(
        estate=original, release_ref=source["release_ref"],
        runtime_catalog=catalog,
    )
    # Mutating the caller-held estate and its authorizer after construction
    # cannot retarget the private verified reader.
    original.i02 = receipt.i02
    original._authorize = lambda _roots: False
    assert execute_saved_i03(
        direct, query_ref=query.ref, predicate_ref=pred.ref
    ).facts[0].ref == base.facts[0].ref
    receipt_data = admission.binding_receipt().as_dict()
    assert receipt_data["counter_status"] == "DECLARED_ZERO__NOT_A_MEASUREMENT"
    assert receipt_data["source_opens"] == 0
    assert receipt_data["full_c11_repository_builds"] == 0


def test_b_fresh_process_i03_i05_no_c11_or_whole_table_fallback(
    tmp_path, monkeypatch,
):
    source, candidate = _source_with_candidate(
        monkeypatch, "S2D-B-FRESH",
        [{"id": "R1", "responses": {"X": 1, "Y": 1}},
         {"id": "R2", "responses": {"X": 0, "Y": 0}}],
    )
    qa, pred, query, i03_catalog = _i03_parts(source, "S2D-B-FRESH")
    qa5, dauth, all_p, x1, yq, authority, i05_catalog = _i05_parts(
        source, "S2D-B-FRESH-I05"
    )
    i03_oracle = native._run(source, qa, pred, query)
    i05_oracle = execute_exact_bounded_discovery(
        repository=source["repo"], discovery_authority=authority,
        authority_registry=native._registry(source, qa5, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=(all_p, x1), query_template_catalog=(yq,),
    )
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "fresh"
    )
    capsule = tmp_path / "saved-capsule.json"
    capsule.write_text(json.dumps({
        "root": str(root), "exact_path": receipt.path,
        "manifest_sha256": receipt.manifest_sha256,
        "i02": {
            "logical": receipt.i02.logical, "physical": receipt.i02.physical,
            "release": receipt.i02.release, "source": receipt.i02.source,
            "replay": receipt.i02.replay, "universe": receipt.i02.universe,
            "schema": receipt.i02.schema,
        },
        "release": source["release_ref"].as_dict(),
        "i03": {
            "authorities": [o.as_dict() for o in i03_catalog.authorities],
            "predicate": pred.as_dict(), "query": query.as_dict(),
        },
        "i05": {
            "authorities": [o.as_dict() for o in i05_catalog.authorities],
            "predicates": [o.as_dict() for o in i05_catalog.predicates],
            "queries": [o.as_dict() for o in i05_catalog.queries],
            "discovery": authority.as_dict(),
        },
    }, sort_keys=True), encoding="utf-8")
    child = r'''
import json, resource, sys
from pathlib import Path
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, materialize_public_object
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03, execute_saved_i05
import pyarrow.parquet as pq
opens = []
def audit(event, args):
    if event == "open" and args:
        text = str(args[0]).lower()
        if text.endswith((".sav", ".dta", ".csv", ".rda", ".rds")):
            opens.append(str(args[0]))
sys.addaudithook(audit)
c = json.loads(Path(sys.argv[1]).read_text())
orig_init = C11Repository.__init__
orig_read = pq.read_table
C11Repository.__init__ = lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("C11 graph"))
pq.read_table = lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("whole-table fallback"))
try:
    from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03, execute_saved_i05
    i03 = c["i03"]; i05 = c["i05"]
    cat3 = RuntimeObjectCatalog(
        authorities=tuple(materialize_public_object(v) for v in i03["authorities"]),
        predicates=(materialize_public_object(i03["predicate"]),),
        queries=(materialize_public_object(i03["query"]),),
        discovery_authorities=(),
    )
    cat5 = RuntimeObjectCatalog(
        authorities=tuple(materialize_public_object(v) for v in i05["authorities"]),
        predicates=tuple(materialize_public_object(v) for v in i05["predicates"]),
        queries=tuple(materialize_public_object(v) for v in i05["queries"]),
        discovery_authorities=(materialize_public_object(i05["discovery"]),),
    )
    a3 = SavedC11Admission.open(root=c["root"], exact_path=c["exact_path"],
        independently_held_manifest_sha256=c["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**c["i02"]),
        release_ref=exact_ref(c["release"]), runtime_catalog=cat3,
        current_authorizer=lambda _r: True)
    r3 = execute_saved_i03(a3, query_ref=cat3.queries[0].ref, predicate_ref=cat3.predicates[0].ref)
    a5 = SavedC11Admission.open(root=c["root"], exact_path=c["exact_path"],
        independently_held_manifest_sha256=c["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**c["i02"]),
        release_ref=exact_ref(c["release"]), runtime_catalog=cat5,
        current_authorizer=lambda _r: True)
    r5 = execute_saved_i05(a5, discovery_authority_ref=cat5.discovery_authorities[0].ref)
    print(json.dumps({
      "fact_refs": [f.ref.as_dict() for f in r3.facts],
      "fact_projections": [f.semantic_projection() for f in r3.facts],
      "i05_fact_refs": [f.ref.as_dict() for f in r5.empirical_facts],
      "i05_receipt_refs": [x.ref.as_dict() for x in r5.receipts],
      "i05_replay_ref": r5.replay_ref.as_dict(),
      "rss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      "source_opens": opens,
    }, sort_keys=True))
finally:
    C11Repository.__init__ = orig_init
    pq.read_table = orig_read
'''
    env = dict(os.environ)
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2])
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-c", child, str(capsule)],
        cwd=tmp_path, env=env, capture_output=True, text=True, timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout)
    assert observed["fact_refs"] == [f.ref.as_dict() for f in i03_oracle.facts]
    assert observed["fact_projections"] == json.loads(json.dumps(
        [f.semantic_projection() for f in i03_oracle.facts], sort_keys=True
    ))
    assert observed["i05_fact_refs"] == [
        f.ref.as_dict() for f in i05_oracle.empirical_facts
    ]
    assert observed["i05_receipt_refs"] == [
        x.ref.as_dict() for x in i05_oracle.receipts
    ]
    assert observed["i05_replay_ref"] == i05_oracle.replay_ref.as_dict()
    assert observed["source_opens"] == []
    assert observed["rss"] < 6 * 1024**3


def test_b_i05_current_revocation_refused_then_restored(tmp_path, monkeypatch):
    source, candidate = _source_with_candidate(
        monkeypatch, "S2D-B-I05-REV",
        [{"id": "R1", "responses": {"X": 1, "Y": 1}},
         {"id": "R2", "responses": {"X": 0, "Y": 0}}],
    )
    qauth, dauth, all_p, x1, yq, authority, catalog = _i05_parts(
        source, "S2D-B-I05-REV"
    )
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "rev-i05"
    )
    allow = {"value": True}
    admission = SavedC11Admission.open(
        root=root,
        exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        release_ref=source["release_ref"],
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: allow["value"],
    )
    base = execute_saved_i05(
        admission, discovery_authority_ref=authority.ref
    )
    assert base.candidate_count == 1
    allow["value"] = False
    with pytest.raises(Exception, match="current source/operation authority refused"):
        execute_saved_i05(admission, discovery_authority_ref=authority.ref)
    allow["value"] = True
    restored = execute_saved_i05(
        admission, discovery_authority_ref=authority.ref
    )
    assert _i05_sig(restored) == _i05_sig(base)


def test_b_i05_mixed_supported_and_valid_empty_frontier(tmp_path, monkeypatch):
    source, candidate = _source_with_candidate(
        monkeypatch, "S2D-B-I05-MIXED",
        [{"id": "R1", "responses": {"X": 1, "Y": 1}},
         {"id": "R2", "responses": {"X": 0, "Y": 0}}],
    )
    qauth = native._query_authority("S2D-B-I05-MIXED")
    dauth = dt._d_auth("S2D-B-I05-MIXED-discovery")
    all_p = native._branch_predicate(source, qauth, tag="mixed-all")
    x1 = native._predicate(
        source, qauth, native._response_leaf(source, qauth, "X", 1),
        tag="mixed-x1",
    )
    empty = native._branch_predicate(
        source, qauth, members=(), tag="mixed-empty"
    )
    yq = native._query(source, qauth, all_p, ("Y",), tag="mixed-y")
    grammar = dt._grammar(
        operation="I03-OP-S2D-B-I05-MIXED-discovery",
        atoms=[
            dt._atom("ALL", all_p, "BRANCH"),
            dt._atom("X1", x1, "RESPONSE"),
            dt._atom("EMPTY", empty, "BRANCH"),
        ],
        templates=[dt._qt("Y", yq)],
        rules=[
            dt._rule(
                "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
                atom_ids=("X1",), baseline_atom_id="ALL",
                query_template_id="Y",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            ),
            dt._rule(
                "empty", "MINORITY_OR_NONMODAL_DEPARTURE", "SINGLE_ATOM",
                atom_ids=("EMPTY",), baseline_atom_id="ALL",
                query_template_id="Y",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            ),
        ],
    )
    base = dt._discovery_authority(source, grammar, dauth)
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
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth, dauth)),
        predicates=(all_p, x1, empty),
        queries=(yq,),
        discovery_authorities=(authority,),
    )
    oracle = execute_exact_bounded_discovery(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=native._registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=(all_p, x1, empty),
        query_template_catalog=(yq,),
    )
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "mixed-frontier"
    )
    admission = _admission(root, receipt, source, catalog)
    observed = execute_saved_i05(
        admission, discovery_authority_ref=authority.ref
    )
    assert _i05_sig(observed) == _i05_sig(oracle)
    states = sorted(r.typed_state for r in observed.receipts)
    assert states == ["DISCOVERED_RESULT_SUPPORTED", "VALID_EMPTY"]
    assert observed.valid_empty is False
