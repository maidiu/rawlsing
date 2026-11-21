"""Focused G5 delta regression: exact admitted source artifact scope.

The accepted S2-C estate exposes an exact source artifact scope in
``receipt.i02.source``.  The native I03 and I05 owners accept that exact
admitted source descriptor as lawful scope metadata.  The saved admission must
preserve it while still refusing foreign source/universe/release/authority
scope.
"""
from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

import rawlsing_next.tests.test_pre553_direct_estate_i03 as s2c
import rawlsing_next.tests.test_pre553_discovery_exact as dt
import rawlsing_next.tests.test_pre553_empirical_query as native
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_direct_estate_i03 import _ref_from_key
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_empirical_objects import (
    DiscoveryAuthority,
    EmpiricalQuerySpec,
    ExactRef,
    exact_ref,
)
from rawlsing_next.pre553_saved_c11_admission import SavedC11AdmissionError
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_i03,
    execute_saved_i05,
)
from rawlsing_next.tests.test_pyat991_s2d_a_counter import (
    _with_extra_scopes,
)
from rawlsing_next.tests.test_pyat991_s2d_saved_admission import (
    _admission,
    _i03_parts,
    _i05_parts,
    _source_with_candidate,
)


def _source_scope(receipt):
    kind = receipt.i02.source.split("|", 1)[0]
    return _ref_from_key(receipt.i02.source, kind)


def _scoped_i03(predicate, query, extra):
    scoped_predicate = _with_extra_scopes(predicate, (extra,))
    scoped_query = _with_extra_scopes(query, (extra,))
    fields = dict(scoped_query.semantic_fields)
    fields["condition_predicate_ref"] = scoped_predicate.ref
    deps = tuple(sorted(
        {
            *(exact_ref(value) for value in scoped_query.dependency_refs),
            scoped_predicate.ref,
        },
        key=lambda ref: ref.key,
    ))
    scoped_query = EmpiricalQuerySpec(
        typed_state=scoped_query.typed_state,
        authority_snapshot_refs=scoped_query.authority_snapshot_refs,
        dependency_refs=deps,
        producer_replay_locator_or_reference_root=(
            scoped_query.producer_replay_locator_or_reference_root
        ),
        **{k: v for k, v in fields.items() if k != "dependency_refs"},
    )
    return scoped_predicate, scoped_query


def _i03_catalog(base_catalog, predicate, query):
    return RuntimeObjectCatalog(
        authorities=base_catalog.authorities,
        predicates=(predicate,),
        queries=(query,),
        discovery_authorities=(),
    )


def _i03_sig(result):
    return (
        tuple(f.ref for f in result.facts),
        tuple(f.semantic_projection() for f in result.facts),
        tuple(result.release_refs),
    )


def _scoped_i05(source, tag, extra):
    qauth, dauth, all_p, x1, yq, _base_authority, _base_catalog = _i05_parts(
        source, tag
    )
    scoped_all = _with_extra_scopes(all_p, (extra,))
    scoped_x1 = _with_extra_scopes(x1, (extra,))
    scoped_yq = _with_extra_scopes(yq, (extra,))
    grammar = dt._grammar(
        operation=f"I03-OP-{tag}-discovery",
        atoms=[
            dt._atom("ALL", scoped_all, "BRANCH"),
            dt._atom("X1", scoped_x1, "RESPONSE"),
        ],
        templates=[dt._qt("Y", scoped_yq)],
        rules=[dt._rule(
            "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="ALL",
            query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
    )
    base = dt._discovery_authority(source, grammar, dauth)
    authority = DiscoveryAuthority(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=(
            base.producer_replay_locator_or_reference_root
        ),
        **{**dict(base.semantic_fields),
           "validation_rules": {
               "rules": ({"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},),
           }},
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth, dauth)),
        predicates=(scoped_all, scoped_x1),
        queries=(scoped_yq,),
        discovery_authorities=(authority,),
    )
    return qauth, dauth, scoped_all, scoped_x1, scoped_yq, authority, catalog


def test_g5_exact_admitted_source_scope_is_accepted_for_i03_query_and_predicate(
    tmp_path, monkeypatch,
):
    tag = "S2D-G5-SOURCE-SCOPE-I03"
    source, candidate = _source_with_candidate(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    qauth, predicate, query, base_catalog = _i03_parts(source, tag)
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "g5-i03",
    )
    source_scope = _source_scope(receipt)
    scoped_predicate, scoped_query = _scoped_i03(
        predicate, query, source_scope,
    )
    catalog = _i03_catalog(base_catalog, scoped_predicate, scoped_query)
    oracle = native._run(source, qauth, scoped_predicate, scoped_query)
    assert oracle.facts[0].typed_state == "SUPPORTED"
    assert oracle.facts[0].raw_denominator_support == 2
    admission = _admission(root, receipt, source, catalog)
    observed = execute_saved_i03(
        admission, query_ref=scoped_query.ref,
        predicate_ref=scoped_predicate.ref,
    )
    assert _i03_sig(observed) == _i03_sig(oracle)


def test_g5_foreign_source_scope_still_refuses(tmp_path, monkeypatch):
    tag = "S2D-G5-SOURCE-SCOPE-FOREIGN"
    source, candidate = _source_with_candidate(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    qauth, predicate, query, base_catalog = _i03_parts(source, tag)
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "g5-foreign",
    )
    admitted = _source_scope(receipt)
    foreign_source = ExactRef(
        admitted.kind, "urn:test:foreign-source-scope", "c" * 64,
    )
    scoped_predicate, scoped_query = _scoped_i03(
        predicate, query, foreign_source,
    )
    catalog = _i03_catalog(base_catalog, scoped_predicate, scoped_query)
    admission = _admission(root, receipt, source, catalog)
    with pytest.raises(SavedC11AdmissionError, match="foreign"):
        execute_saved_i03(
            admission, query_ref=scoped_query.ref,
            predicate_ref=scoped_predicate.ref,
        )


def test_g5_admitted_source_scope_is_preserved_for_i05_discovery(
    tmp_path, monkeypatch,
):
    tag = "S2D-G5-SOURCE-SCOPE-I05"
    source, candidate = _source_with_candidate(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"X": 1, "Y": 1}},
         {"id": "R2", "responses": {"X": 0, "Y": 0}}],
    )
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "g5-i05",
    )
    source_scope = _source_scope(receipt)
    qauth, dauth, all_p, x1, yq, authority, catalog = _scoped_i05(
        source, tag, source_scope,
    )
    oracle = execute_exact_bounded_discovery(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=native._registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=(all_p, x1),
        query_template_catalog=(yq,),
    )
    admission = _admission(root, receipt, source, catalog)
    observed = execute_saved_i05(
        admission, discovery_authority_ref=authority.ref,
    )
    assert observed.candidate_count == oracle.candidate_count
    assert observed.covered_candidate_count == oracle.covered_candidate_count
    assert tuple(f.ref for f in observed.empirical_facts) == tuple(
        f.ref for f in oracle.empirical_facts
    )
    assert tuple(r.ref for r in observed.receipts) == tuple(
        r.ref for r in oracle.receipts
    )
    assert observed.valid_empty == oracle.valid_empty
