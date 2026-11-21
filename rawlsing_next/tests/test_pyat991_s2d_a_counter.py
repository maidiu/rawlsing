"""A bounded counterattack on B's exact-scope saved-admission repair.

The original query/predicate schema treats ``scope_refs`` as exact scope
references, not as a singleton universe field.  The native I03 owner accepts a
query whose scope contains the admitted universe plus the exact admitted
release (and other non-universe scope references); B's saved adapter currently
rejects every such input because it requires the entire set to equal
``{universe}``.  That is an over-narrow saved admission, not a foreign-source
positive: the foreign-universe and foreign-release cases must still refuse.

The tests use the accepted S2-C estate and the actual native I03 first reader.
"""
from __future__ import annotations

import pytest

pytest.importorskip("pyarrow")

import rawlsing_next.tests.test_pre553_direct_estate_i03 as s2c
import rawlsing_next.tests.test_pre553_empirical_query as native
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    exact_ref,
)
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11AdmissionError,
)
from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03
from rawlsing_next.tests.test_pyat991_s2d_saved_admission import (
    _admission,
    _i03_parts,
    _source_with_candidate,
)


def _with_extra_scopes(document: EmpiricalQuerySpec | EmpiricalPredicate, extra: tuple[ExactRef, ...]):
    fields = dict(document.semantic_fields)
    current = {
        exact_ref(dict(value), "scope_ref")
        for value in fields["scope_refs"]
    }
    fields["scope_refs"] = tuple(
        sorted(current | set(extra), key=lambda ref: ref.key)
    )
    fields["scope_refs"] = tuple(ref.as_dict() for ref in fields["scope_refs"])
    if isinstance(document, EmpiricalQuerySpec):
        return EmpiricalQuerySpec(
            typed_state=document.typed_state,
            authority_snapshot_refs=document.authority_snapshot_refs,
            dependency_refs=document.dependency_refs,
            producer_replay_locator_or_reference_root=(
                document.producer_replay_locator_or_reference_root
            ),
            **fields,
        )
    return EmpiricalPredicate(
        typed_state=document.typed_state,
        authority_snapshot_refs=document.authority_snapshot_refs,
        dependency_refs=document.dependency_refs,
        producer_replay_locator_or_reference_root=(
            document.producer_replay_locator_or_reference_root
        ),
        **fields,
    )


def _catalog_with(*, authorities, predicate, query):
    return RuntimeObjectCatalog(
        authorities=authorities,
        predicates=(predicate,),
        queries=(query,),
        discovery_authorities=(),
    )


def _fact_sig(result):
    return tuple(fact.semantic_projection() for fact in result.facts)


def test_nonuniverse_scope_refs_are_preserved_not_over_narrowed(
    tmp_path, monkeypatch,
):
    tag = "S2D-A-SCOPE-COUNTER"
    source, candidate = _source_with_candidate(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    qauth, predicate, query, base_catalog = _i03_parts(source, tag)
    # The exact admitted release is a lawful additional scope reference; it is
    # not a foreign universe and does not select a second source.
    extra = (exact_ref(source["release_ref"]),)
    scoped_predicate = _with_extra_scopes(predicate, extra)
    scoped_query = _with_extra_scopes(query, extra)
    # Make the query condition exactly bind the extra-scoped predicate.
    fields = dict(scoped_query.semantic_fields)
    fields["condition_predicate_ref"] = scoped_predicate.ref
    dependency_refs = tuple(
        sorted(
            {*(exact_ref(value) for value in scoped_query.dependency_refs),
             scoped_predicate.ref},
            key=lambda ref: ref.key,
        )
    )
    scoped_query = EmpiricalQuerySpec(
        typed_state=scoped_query.typed_state,
        authority_snapshot_refs=scoped_query.authority_snapshot_refs,
        dependency_refs=dependency_refs,
        producer_replay_locator_or_reference_root=(
            scoped_query.producer_replay_locator_or_reference_root
        ),
        **fields,
    )
    catalog = _catalog_with(
        authorities=base_catalog.authorities,
        predicate=scoped_predicate, query=scoped_query,
    )
    oracle = native._run(source, qauth, scoped_predicate, scoped_query)
    assert oracle.facts[0].typed_state == "SUPPORTED"
    assert oracle.facts[0].raw_denominator_support == 2

    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "scoped-counter",
    )
    admission = _admission(root, receipt, source, catalog)
    observed = execute_saved_i03(
        admission, query_ref=scoped_query.ref,
        predicate_ref=scoped_predicate.ref,
    )
    assert _fact_sig(observed) == _fact_sig(oracle)
    assert tuple(f.ref for f in observed.facts) == tuple(f.ref for f in oracle.facts)


def test_foreign_universe_and_release_scope_refs_still_refuse(
    tmp_path, monkeypatch,
):
    tag = "S2D-A-SCOPE-FOREIGN"
    source, candidate = _source_with_candidate(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    qauth, predicate, query, base_catalog = _i03_parts(source, tag)
    foreign_universe = ExactRef(
        "EmpiricalUniverse@1.0.0",
        "urn:test:foreign-universe",
        "a" * 64,
    )
    foreign_release = ExactRef(
        "C11LogicalRelease",
        "urn:test:foreign-release",
        "b" * 64,
    )
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "foreign-scope",
    )

    for extra in ((foreign_universe,), (foreign_release,)):
        scoped_predicate = _with_extra_scopes(predicate, extra)
        scoped_query = _with_extra_scopes(query, extra)
        fields = dict(scoped_query.semantic_fields)
        fields["condition_predicate_ref"] = scoped_predicate.ref
        dependency_refs = tuple(
            sorted(
                {*(exact_ref(value) for value in scoped_query.dependency_refs),
                 scoped_predicate.ref},
                key=lambda ref: ref.key,
            )
        )
        scoped_query = EmpiricalQuerySpec(
            typed_state=scoped_query.typed_state,
            authority_snapshot_refs=scoped_query.authority_snapshot_refs,
            dependency_refs=dependency_refs,
            producer_replay_locator_or_reference_root=(
                scoped_query.producer_replay_locator_or_reference_root
            ),
            **fields,
        )
        catalog = _catalog_with(
            authorities=base_catalog.authorities,
            predicate=scoped_predicate, query=scoped_query,
        )
        admission = _admission(root, receipt, source, catalog)
        with pytest.raises(SavedC11AdmissionError, match="scope"):
            execute_saved_i03(
                admission, query_ref=scoped_query.ref,
                predicate_ref=scoped_predicate.ref,
            )
