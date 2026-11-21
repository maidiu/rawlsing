"""A counter-round controls for B's multi-source conservation repairs.

Frozen scope: F01/F05 conservation of native source/release ties.  These tests
target the two holes left by B's otherwise correct subset relaxations:

1. a fact may name any universe that appears in the multi-universe query even
   when that universe is absent from the fact's own exact provenance;
2. a receipt may name any release subset of the closure even when that subset
   does not cover the releases of the facts the receipt owns.

Both are internal closure inconsistencies, not external-pin attacks.  The
positive controls prove a genuine native multi-source/multi-release output still
publishes and opens cold after the repair.
"""
from __future__ import annotations

from pathlib import Path
import shutil

import pytest

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_discovery_exact import ExactBoundedDiscoveryResult
from rawlsing_next.pre553_durable_empirical_closure import (
    DurableEmpiricalClosureError,
    NativeEmpiricalOutput,
    _final_replay_material,
    _receipt_replay_material,
    open_empirical_closure,
    publish_empirical_closure,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    DiscoveryResultReceipt,
    EmpiricalFact,
    ExactRef,
    canonical_json,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_route_b_production import RouteBEmpiricalObjectGraph
from rawlsing_next.tests.pre553_query_frontier_fixtures import _combined_repo
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom,
    _d_auth,
    _discovery_authority,
    _execute as execute_i05,
    _grammar,
    _qt,
    _rule,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _build_source,
    _query,
    _query_authority,
)
from rawlsing_next.tests.test_pyat940_s2f_durable_closure import _release_identity


def _unique(objects):
    return tuple(
        sorted({obj.ref.key: obj for obj in objects}.values(), key=lambda obj: obj.ref.key)
    )


def _multi_source_output(*, tamper_universe: bool) -> NativeEmpiricalOutput:
    first = _build_source(
        "s2f-a-counter-multi-a",
        [{"id": "A1", "responses": {"Y": 1}}, {"id": "A2", "responses": {"Y": 0}}],
    )
    second = _build_source(
        "s2f-a-counter-multi-b",
        [{"id": "B1", "responses": {"Y": 1}}, {"id": "B2", "responses": {"Y": 0}}],
    )
    qauth = _query_authority("s2f-a-counter-multi")
    predicate = _branch_predicate(first, qauth, tag="all")
    query = _query(
        first,
        qauth,
        predicate,
        ("Y",),
        tag="s2f-a-counter-multi",
        source_mode="SOURCE_INDEXED_MULTI_UNIVERSE",
        universe_refs=(first["universe"].ref, second["universe"].ref),
    )
    registry = AuthorityRegistry(
        tuple(
            sorted(
                {
                    obj.authority_ref.key: obj
                    for obj in (*first["authorities"], *second["authorities"], qauth)
                }.values(),
                key=lambda obj: obj.authority_ref.key,
            )
        )
    )
    result = execute_empirical_query(
        repository=_combined_repo(first, second),
        query=query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(first["release_ref"], second["release_ref"]),
    )
    positive = next(fact for fact in result.facts if fact.typed_state == "SUPPORTED")
    assert exact_ref(dict(positive.empirical_universe_refs[0])) == first["universe"].ref

    if tamper_universe:
        fields = dict(positive.semantic_fields)
        fields["empirical_universe_refs"] = (second["universe"].ref,)
        positive = EmpiricalFact(
            typed_state=positive.typed_state,
            authority_snapshot_refs=positive.authority_snapshot_refs,
            dependency_refs=positive.dependency_refs,
            producer_replay_locator_or_reference_root=(
                positive.producer_replay_locator_or_reference_root
            ),
            **fields,
        )
        # The claimed universe is lawful for the query but is not in the fact's
        # retained provenance.
        provenance_universes = {
            dict(ref)["object_id"]
            for ref in positive.source_empirical_provenance_refs
            if dict(ref)["kind"] == "EmpiricalUniverse@1.0.0"
        }
        assert dict(positive.empirical_universe_refs[0])["object_id"] not in provenance_universes

    facts = tuple(
        sorted(
            {obj.ref.key: obj for obj in (*result.facts, positive)}.values(),
            key=lambda obj: obj.ref.key,
        )
    )
    i03 = QueryExecutionResult(
        query_ref=result.query_ref,
        facts=facts,
        source_scope_mode=result.source_scope_mode,
        release_refs=result.release_refs,
    )
    dauth = _d_auth("s2f-a-counter-multi-discovery")
    grammar = _grammar(
        operation="I03-OP-s2f-a-counter-multi-discovery",
        atoms=(),
        templates=(),
        rules=(),
        allow_empty=True,
    )
    authority = _discovery_authority(
        first, grammar, dauth, tag="s2f-a-counter-multi-discovery"
    )
    i05 = execute_i05(
        first,
        qauth,
        dauth,
        grammar,
        (predicate,),
        (query,),
        authority=authority,
    )
    graph = RouteBEmpiricalObjectGraph(
        authority_snapshots=tuple(
            sorted(
                {
                    obj.authority_ref.key: obj
                    for obj in (*first["authorities"], *second["authorities"], qauth, dauth)
                }.values(),
                key=lambda obj: obj.authority_ref.key,
            )
        ),
        executed_predicates=(predicate,),
        executed_queries=(query,),
        empirical_facts=facts,
        discovery_authorities=(authority,),
        discovery_receipts=(),
    )
    return NativeEmpiricalOutput(
        source_identity={"schema": "S2F_A_COUNTER_MULTI_SOURCE@1", "tag": "multi"},
        release_identities=(_release_identity(first), _release_identity(second)),
        i03_results=(i03,),
        i05_result=i05,
        object_graph=graph,
    )


def _multi_release_receipt_output(*, tamper_receipt_release: bool) -> NativeEmpiricalOutput:
    first = _build_source(
        "s2f-a-counter-mr-a",
        [{"id": "A1", "responses": {"Y": 1}}, {"id": "A2", "responses": {"Y": 0}}],
    )
    second = _build_source(
        "s2f-a-counter-mr-b",
        [{"id": "B1", "responses": {"Y": 1}}, {"id": "B2", "responses": {"Y": 1}}],
    )
    third = _build_source(
        "s2f-a-counter-mr-c",
        [{"id": "C1", "responses": {"Y": 1}}, {"id": "C2", "responses": {"Y": 0}}],
    )
    qauth = _query_authority("s2f-a-counter-mr")
    predicate = _branch_predicate(first, qauth, tag="all")
    query = _query(first, qauth, predicate, ("Y",), tag="s2f-a-counter-mr")
    result = execute_empirical_query(
        repository=first["repo"],
        query=query,
        predicate=predicate,
        authority_registry=AuthorityRegistry(tuple(first["authorities"]) + (qauth,)),
        release_refs=(first["release_ref"],),
    )
    y_query = _query(first, qauth, predicate, ("Y",), tag="s2f-a-counter-mr-y")
    dauth = _d_auth("s2f-a-counter-mr-discovery")
    grammar = _grammar(
        operation="I03-OP-s2f-a-counter-mr-discovery",
        atoms=(_atom("ALL", predicate, "BRANCH"),),
        templates=(_qt("Y", y_query),),
        rules=(
            _rule(
                "minority",
                "MINORITY_OR_NONMODAL_DEPARTURE",
                "SINGLE_ATOM",
                atom_ids=("ALL",),
                baseline_atom_id="ALL",
                query_template_id="Y",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            ),
        ),
    )
    authority = _discovery_authority(
        first, grammar, dauth, tag="s2f-a-counter-mr-discovery"
    )
    i05 = execute_i05(
        first, qauth, dauth, grammar, (predicate,), (y_query,), authority=authority
    )
    releases = (
        _release_identity(first),
        _release_identity(second),
        _release_identity(third),
    )
    receipt = i05.receipts[0]
    if tamper_receipt_release:
        # Declare a different lawful closure release while retaining facts whose
        # provenance is the first release.
        fields = dict(receipt.semantic_fields)
        fields["source_release_refs"] = (second["release_ref"],)
        fields["replay_ref"] = ExactRef("TMP", "urn:test:tmp-replay", "0" * 64)
        temporary = DiscoveryResultReceipt(
            typed_state=receipt.typed_state,
            authority_snapshot_refs=receipt.authority_snapshot_refs,
            dependency_refs=receipt.dependency_refs,
            producer_replay_locator_or_reference_root=(
                receipt.producer_replay_locator_or_reference_root
            ),
            **fields,
        )
        material = _receipt_replay_material(
            temporary, tuple(identity.release_ref for identity in releases)
        )
        digest = semantic_hash(material)
        new_replay = ExactRef(
            "PRE553_I05_DISCOVERY_REPLAY",
            f"urn:rawlsing:pre553:i05:candidate-replay:sha256:{digest}",
            digest,
        )
        fields["replay_ref"] = new_replay
        receipt = DiscoveryResultReceipt(
            typed_state=receipt.typed_state,
            authority_snapshot_refs=receipt.authority_snapshot_refs,
            dependency_refs=receipt.dependency_refs,
            producer_replay_locator_or_reference_root=new_replay,
            **fields,
        )
        i05_facts = tuple(i05.empirical_facts)
        temporary_i05 = ExactBoundedDiscoveryResult(
            contract_id=i05.contract_id,
            discovery_authority_ref=i05.discovery_authority_ref,
            candidate_grammar_ref=i05.candidate_grammar_ref,
            evaluated_frontier_ref=i05.evaluated_frontier_ref,
            coverage_claim=i05.coverage_claim,
            candidate_count=i05.candidate_count,
            covered_candidate_count=i05.covered_candidate_count,
            receipts=(receipt,),
            empirical_fact_refs=i05.empirical_fact_refs,
            empirical_facts=i05_facts,
            executed_predicates=i05.executed_predicates,
            executed_queries=i05.executed_queries,
            valid_empty=i05.valid_empty,
            replay_ref=ExactRef("TMP2", "urn:test:tmp-final", "0" * 64),
        )
        final = _final_replay_material(temporary_i05)
        final_digest = semantic_hash(final)
        final_ref = ExactRef(
            "PRE553_I05_FRONTIER_REPLAY",
            f"urn:rawlsing:pre553:i05:frontier-replay:sha256:{final_digest}",
            final_digest,
        )
        new_i05 = ExactBoundedDiscoveryResult(
            contract_id=i05.contract_id,
            discovery_authority_ref=i05.discovery_authority_ref,
            candidate_grammar_ref=i05.candidate_grammar_ref,
            evaluated_frontier_ref=i05.evaluated_frontier_ref,
            coverage_claim=i05.coverage_claim,
            candidate_count=i05.candidate_count,
            covered_candidate_count=i05.covered_candidate_count,
            receipts=(receipt,),
            empirical_fact_refs=i05.empirical_fact_refs,
            empirical_facts=i05_facts,
            executed_predicates=i05.executed_predicates,
            executed_queries=i05.executed_queries,
            valid_empty=i05.valid_empty,
            replay_ref=final_ref,
        )
    else:
        new_i05 = i05

    graph = RouteBEmpiricalObjectGraph(
        authority_snapshots=tuple(
            sorted(
                {
                    obj.authority_ref.key: obj
                    for obj in (*first["authorities"], qauth, dauth)
                }.values(),
                key=lambda obj: obj.authority_ref.key,
            )
        ),
        executed_predicates=_unique((predicate, *i05.executed_predicates)),
        executed_queries=_unique((query, *i05.executed_queries)),
        empirical_facts=_unique((*result.facts, *i05.empirical_facts)),
        discovery_authorities=(authority,),
        discovery_receipts=(receipt,),
    )
    return NativeEmpiricalOutput(
        source_identity={"schema": "S2F_A_COUNTER_MULTI_RELEASE@1", "tag": "mr"},
        release_identities=releases,
        i03_results=(result,),
        i05_result=new_i05,
        object_graph=graph,
    )


def test_a_counter_f1_mixed_i03_i05_census_is_complete(tmp_path):
    from rawlsing_next.tests.test_pyat940_s2f_durable_closure import _m01_output

    output = _m01_output()["output"]
    receipt = publish_empirical_closure(output, tmp_path / "cas")
    closure = open_empirical_closure(
        receipt.root_path, expected_root=receipt.root_identity
    ).require_trusted()
    arity_one = sorted(
        (
            fact.ref.as_dict()
            for fact in closure.object_graph.empirical_facts
            if fact.target_topology.get("arity") == 1
        ),
        key=canonical_json,
    )
    assert arity_one
    assert list(closure.census["f1_f4"]["F1_marginal_fact_refs"]) == arity_one
    i03_keys = {
        fact.ref.key for result in output.i03_results for fact in result.facts
    }
    i05_keys = {fact.ref.key for fact in output.i05_result.empirical_facts}
    assert any(fact.ref.key in i03_keys for fact in closure.object_graph.empirical_facts if fact.target_topology.get("arity") == 1)
    assert any(fact.ref.key in i05_keys - i03_keys for fact in closure.object_graph.empirical_facts if fact.target_topology.get("arity") == 1)


def test_a_counter_wrong_universe_fact_is_refused(tmp_path):
    # Positive control: the genuine native multi-source output still publishes.
    native = _multi_source_output(tamper_universe=False)
    native_receipt = publish_empirical_closure(native, tmp_path / "native-cas")
    native_closure = open_empirical_closure(
        native_receipt.root_path, expected_root=native_receipt.root_identity
    ).require_trusted()
    assert any(f.typed_state == "SUPPORTED" for f in native_closure.object_graph.empirical_facts)

    # Hostile control: a fact claims a query universe that is absent from its own
    # exact provenance.  This is not an external-pin attack; it is an internally
    # inconsistent fact that must never be admitted into the closure.
    tampered = _multi_source_output(tamper_universe=True)
    with pytest.raises(DurableEmpiricalClosureError, match="provenance"):
        publish_empirical_closure(tampered, tmp_path / "tampered-cas")


def test_a_counter_receipt_release_must_cover_its_facts(tmp_path):
    # Positive control: a three-release closure with a one-release receipt works.
    native = _multi_release_receipt_output(tamper_receipt_release=False)
    native_receipt = publish_empirical_closure(native, tmp_path / "native-cas")
    native_closure = open_empirical_closure(
        native_receipt.root_path, expected_root=native_receipt.root_identity
    ).require_trusted()
    receipt = native_closure.object_graph.discovery_receipts[0]
    assert len(native_closure.release_identities) == 3
    receipt_releases = {dict(ref)["content_hash"] for ref in receipt.source_release_refs}
    assert receipt_releases

    # Hostile control: the receipt declares the second release while every fact
    # it owns retains first-release provenance.  The exact receipt replay is
    # internally self-consistent, so only the fact-ownership check can refuse it.
    tampered = _multi_release_receipt_output(tamper_receipt_release=True)
    with pytest.raises(DurableEmpiricalClosureError, match="source release refs"):
        publish_empirical_closure(tampered, tmp_path / "tampered-cas")
