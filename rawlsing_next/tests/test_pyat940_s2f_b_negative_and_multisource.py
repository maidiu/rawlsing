"""S2-F Role-B repairs: native typed-negative facts and multi-source census.

These tests were written after independently reproducing three failures in the
first artifact:

1. a genuine native ``UNRESOLVED`` fact (produced by the actual
   ``pre553_empirical_query.execute_empirical_query`` negative path) could not be
   published at all because the closure reconstructed only the positive
   ``_build_fact`` replay shape;
2. a native ``SOURCE_INDEXED_MULTI_UNIVERSE`` result could not be published
   because the closure required each per-source fact's universe set to equal the
   whole query universe set;
3. the F1 census was empty for closures whose marginal facts came from I05
   candidate execution rather than the explicit I03 request list.

The repairs are confined to the isolated S2-F adapter.  The native I03/I05
owners and their evidence are unchanged.
"""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import shutil

import pytest

from rawlsing_next.pre553_durable_empirical_closure import (
    DurableEmpiricalClosureError,
    NativeEmpiricalOutput,
    open_empirical_closure,
    publish_empirical_closure,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalQuerySpec,
    canonical_json,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_route_b_production import RouteBEmpiricalObjectGraph
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
from rawlsing_next.tests.test_pyat940_s2f_durable_closure import (
    _blob_path,
    _copy_closure,
    _discovery_output,
    _load_doc,
    _minority_output,
    _release_identity,
    _reversal_output,
    _rewrite_manifest,
    _save_manifest,
    _store_doc,
)


def _unsupported_topology_query(source, qauth, predicate, *, tag: str) -> EmpiricalQuerySpec:
    """Build a lawfully authorized query whose native target plan is unsupported.

    This is not a hand-built fact.  It forces the actual native
    ``_negative_result`` path when the exact I03 executor cannot parse the
    declared topology.
    """

    base = _query(source, qauth, predicate, ("Y",), tag=tag)
    component = base.target_arity_and_topology["components"][0]
    spec = {
        "arity": 1,
        "joint_order_semantics": "SEMANTIC_ORDERED",
        "components": [
            {
                "target_ref": dict(component["target_ref"]),
                "topology": "S2F_B_UNSUPPORTED_TOPOLOGY",
                "domain": ["0", "1"],
                "target_domain_replay_ref": dict(component["target_domain_replay_ref"]),
                "topology_authority_refs": [
                    dict(value) for value in component["topology_authority_refs"]
                ],
                "response_semantic_authority_refs": [
                    dict(value) for value in component["response_semantic_authority_refs"]
                ],
                "included_states": ["SUBSTANTIVE_RESPONSE"],
            }
        ],
    }
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
        target_refs=base.target_refs,
        target_arity_and_topology=spec,
        condition_predicate_ref=base.condition_predicate_ref,
        risk_set_ref=base.risk_set_ref,
        empirical_universe_refs=base.empirical_universe_refs,
        scope_refs=base.scope_refs,
        measure_basis_ref=base.measure_basis_ref,
        requested_output_grain=dict(base.requested_output_grain),
        query_authority_refs=base.query_authority_refs,
    )


def _negative_native_output() -> tuple[NativeEmpiricalOutput, object]:
    """Return a complete native output containing one genuine typed negative."""

    source = _build_source(
        "s2f-b-negative",
        [
            {"id": "R1", "responses": {"Y": 0}},
            {"id": "R2", "responses": {"Y": 1}},
        ],
    )
    qauth = _query_authority("s2f-b-negative")
    predicate = _branch_predicate(source, qauth, tag="all")
    negative_query = _unsupported_topology_query(
        source, qauth, predicate, tag="s2f-b-negative"
    )
    result = execute_empirical_query(
        repository=source["repo"],
        query=negative_query,
        predicate=predicate,
        authority_registry=AuthorityRegistry(
            tuple(source["authorities"]) + (qauth,)
        ),
        release_refs=(source["release_ref"],),
    )
    assert len(result.facts) == 1
    fact = result.facts[0]
    assert fact.typed_state == "UNRESOLVED"
    assert not hasattr(fact, "risk_set_member_refs")
    assert "complete_cell_semantic_projection" not in fact.target_topology

    dauth = _d_auth("s2f-b-negative-discovery")
    grammar = _grammar(
        operation="I03-OP-s2f-b-negative-discovery",
        atoms=(),
        templates=(),
        rules=(),
        allow_empty=True,
    )
    authority = _discovery_authority(
        source, grammar, dauth, tag="s2f-b-negative-discovery"
    )
    i05 = execute_i05(
        source,
        qauth,
        dauth,
        grammar,
        (predicate,),
        (negative_query,),
        authority=authority,
    )
    base = _discovery_output(
        source,
        qauth,
        dauth,
        (predicate,),
        (negative_query,),
        authority,
        i05,
        tag="s2f-b-negative",
    )
    graph = RouteBEmpiricalObjectGraph(
        authority_snapshots=base.object_graph.authority_snapshots,
        executed_predicates=base.object_graph.executed_predicates,
        executed_queries=base.object_graph.executed_queries,
        empirical_facts=tuple(
            sorted(
                {
                    obj.ref.key: obj
                    for obj in (*base.object_graph.empirical_facts, *result.facts)
                }.values(),
                key=lambda obj: obj.ref.key,
            )
        ),
        discovery_authorities=base.object_graph.discovery_authorities,
        discovery_receipts=base.object_graph.discovery_receipts,
    )
    output = NativeEmpiricalOutput(
        source_identity=base.source_identity,
        release_identities=base.release_identities,
        i03_results=(result,),
        i05_result=base.i05_result,
        object_graph=graph,
    )
    return output, fact


def _rewrite_stored_fact(victim: Path, closing: Path, fact_ref: dict, mutate) -> dict:
    """Coherently re-hash one stored fact document (new self-hash pin supplied)."""

    manifest = json.loads((closing / "manifest.json").read_text())
    entry = next(
        item for item in manifest["core"]["objects"] if item["ref"] == fact_ref
    )
    document = _load_doc(_blob_path(victim, entry["document_hash"]))
    mutate(document)
    projection = {
        key: document[key]
        for key in (
            "schema_id",
            "schema_version",
            "typed_state",
            "authority_snapshot_refs",
            "dependency_refs",
            "producer_replay_locator_or_reference_root",
            "semantic_fields",
        )
    }
    document["content_hash"] = semantic_hash(projection)
    document["object_id"] = (
        "urn:rawlsing:pre553:EmpiricalFact:sha256:" + document["content_hash"]
    )
    new_hash = semantic_hash(document)
    _store_doc(_blob_path(victim, new_hash), document)
    _blob_path(victim, entry["document_hash"]).unlink()
    entry["document_hash"] = new_hash
    entry["ref"] = {
        "kind": "EmpiricalFact@1.0.0",
        "object_id": document["object_id"],
        "content_hash": document["content_hash"],
    }
    entry["document_uncompressed_bytes"] = len(
        canonical_json(document).encode("utf-8")
    )
    entry["document_compressed_bytes"] = _blob_path(victim, new_hash).stat().st_size
    manifest = _rewrite_manifest(manifest)
    _save_manifest(manifest, closing / "manifest.json")
    return manifest


def test_b_native_typed_negative_fact_publishes_cold_and_censused(tmp_path):
    output, native_fact = _negative_native_output()
    receipt = publish_empirical_closure(output, tmp_path / "cas")
    closure = open_empirical_closure(
        receipt.root_path, expected_root=receipt.root_identity
    ).require_trusted()

    facts = closure.object_graph.empirical_facts
    assert len(facts) == 1
    fact = facts[0]
    assert fact.ref == native_fact.ref
    assert canonical_json(fact.as_dict()) == canonical_json(native_fact.as_dict())
    assert fact.typed_state == "UNRESOLVED"
    assert fact.p02_failure_state == "UNSUPPORTED_RESPONSE_TOPOLOGY"

    declared = closure.census["declared"]
    assert declared["fact_state_counts"] == {"UNRESOLVED": 1}
    assert [row["ref"] for row in declared["negative_or_held"]] == [
        fact.ref.as_dict()
    ]
    # A typed negative marginal fact remains part of the F1 census.  The first
    # artifact restricted F1 to explicit I03 requests and reported a false empty
    # F1 census for I05-executed marginals.
    assert list(closure.census["f1_f4"]["F1_marginal_fact_refs"]) == [
        fact.ref.as_dict()
    ]
    assert fact.raw_denominator_support == 0
    assert fact.raw_numerator_support == 0

    # The exact negative replay preimage was retained and re-derived from the
    # fact's own fields, not replaced by a counts-only checkpoint.
    replay_entry = next(
        entry
        for entry in closure.manifest["core"]["replays"]["facts"]
        if entry["fact_ref"]["content_hash"] == fact.ref.content_hash
    )
    assert replay_entry["material_hash"] == exact_ref(dict(fact.replay_ref)).content_hash

    # Hostile fate edit: change only the native failure code in the stored fact.
    # The self-hash pin is deliberately recomputed, so refusal must come from the
    # exact replay/negative closure rather than the old external pin.
    root = Path(receipt.root_path).parent.parent
    victim = _copy_closure(root)
    closing = victim / "closures" / Path(receipt.root_path).name
    manifest = _rewrite_stored_fact(
        victim,
        closing,
        fact.ref.as_dict(),
        lambda document: document["semantic_fields"].__setitem__(
            "p02_failure_state", "INTEGRITY_FAILURE"
        ),
    )
    with pytest.raises(DurableEmpiricalClosureError):
        open_empirical_closure(
            closing,
            expected_root=manifest["publication"]["root_identity"],
        )
    shutil.rmtree(victim)

    # Hostile count substitution: a nonpositive fact must not silently acquire
    # support while retaining its UNRESOLVED fate.  The native negative replay
    # material does not itself carry the counts, so the closure must enforce the
    # exact negative-fact invariant.
    victim = _copy_closure(root)
    closing = victim / "closures" / Path(receipt.root_path).name
    manifest = _rewrite_stored_fact(
        victim,
        closing,
        fact.ref.as_dict(),
        lambda document: document.update(
            {"raw_numerator_support": 1, "raw_denominator_support": 1}
        ),
    )
    with pytest.raises(DurableEmpiricalClosureError):
        open_empirical_closure(
            closing,
            expected_root=manifest["publication"]["root_identity"],
        )
    shutil.rmtree(victim)


def test_b_empty_target_domain_positive_fact_remains_publishable(tmp_path):
    """Self-check: the negative-fact invariant must not reject lawful VALID_EMPTY.

    An authorized query with a declared empty target domain has no cell rows but
    still carries a positive exact risk/denominator.  It is a positive-topology
    native fact, not a ``_build_negative_fact`` result.
    """

    source = _build_source(
        "s2f-b-empty-domain",
        [{"id": "R1", "responses": {"Y": 1}}, {"id": "R2", "responses": {"Y": 0}}],
    )
    qauth = _query_authority("s2f-b-empty-domain")
    predicate = _branch_predicate(source, qauth, tag="all")
    base = _query(source, qauth, predicate, ("Y",), tag="s2f-b-empty-domain")
    component = dict(base.target_arity_and_topology["components"][0])
    component["domain"] = []
    query = EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
        target_refs=base.target_refs,
        target_arity_and_topology={
            "arity": 1,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": [component],
        },
        condition_predicate_ref=base.condition_predicate_ref,
        risk_set_ref=base.risk_set_ref,
        empirical_universe_refs=base.empirical_universe_refs,
        scope_refs=base.scope_refs,
        measure_basis_ref=base.measure_basis_ref,
        requested_output_grain=dict(base.requested_output_grain),
        query_authority_refs=base.query_authority_refs,
    )
    result = execute_empirical_query(
        repository=source["repo"],
        query=query,
        predicate=predicate,
        authority_registry=AuthorityRegistry(tuple(source["authorities"]) + (qauth,)),
        release_refs=(source["release_ref"],),
    )
    fact = result.facts[0]
    assert fact.typed_state == "VALID_EMPTY"
    assert fact.target_topology["complete_cell_semantic_projection"] == ()
    assert fact.raw_denominator_support > 0
    assert fact.risk_set_member_refs

    dauth = _d_auth("s2f-b-empty-domain-discovery")
    grammar = _grammar(
        operation="I03-OP-s2f-b-empty-domain-discovery",
        atoms=(),
        templates=(),
        rules=(),
        allow_empty=True,
    )
    authority = _discovery_authority(
        source, grammar, dauth, tag="s2f-b-empty-domain-discovery"
    )
    i05 = execute_i05(
        source,
        qauth,
        dauth,
        grammar,
        (predicate,),
        (query,),
        authority=authority,
    )
    base_output = _discovery_output(
        source,
        qauth,
        dauth,
        (predicate,),
        (query,),
        authority,
        i05,
        tag="s2f-b-empty-domain",
    )
    graph = RouteBEmpiricalObjectGraph(
        authority_snapshots=base_output.object_graph.authority_snapshots,
        executed_predicates=base_output.object_graph.executed_predicates,
        executed_queries=base_output.object_graph.executed_queries,
        empirical_facts=tuple(
            sorted(
                {
                    obj.ref.key: obj
                    for obj in (*base_output.object_graph.empirical_facts, fact)
                }.values(),
                key=lambda obj: obj.ref.key,
            )
        ),
        discovery_authorities=base_output.object_graph.discovery_authorities,
        discovery_receipts=base_output.object_graph.discovery_receipts,
    )
    receipt = publish_empirical_closure(
        NativeEmpiricalOutput(
            source_identity=base_output.source_identity,
            release_identities=base_output.release_identities,
            i03_results=(result,),
            i05_result=base_output.i05_result,
            object_graph=graph,
        ),
        tmp_path / "cas",
    )
    closure = open_empirical_closure(
        receipt.root_path, expected_root=receipt.root_identity
    ).require_trusted()
    restored = next(
        item
        for item in closure.object_graph.empirical_facts
        if item.ref == fact.ref
    )
    assert restored.typed_state == "VALID_EMPTY"
    assert restored.raw_denominator_support == fact.raw_denominator_support
    assert restored.risk_set_member_refs == fact.risk_set_member_refs


def test_b_f1_census_includes_i05_marginal_facts(tmp_path):
    root = tmp_path / "cas"
    for name, builder in (
        ("reversal", _reversal_output),
        ("minority", _minority_output),
    ):
        receipt = publish_empirical_closure(builder(), root)
        closure = open_empirical_closure(
            receipt.root_path, expected_root=receipt.root_identity
        )
        arity_one = [
            fact.ref.as_dict()
            for fact in closure.object_graph.empirical_facts
            if fact.target_topology.get("arity") == 1
        ]
        assert arity_one, name
        assert list(closure.census["f1_f4"]["F1_marginal_fact_refs"]) == sorted(
            arity_one, key=canonical_json
        ), name


def test_b_multi_universe_and_multi_release_native_output_census(tmp_path):
    first = _build_source(
        "s2f-b-multi-a",
        [{"id": "A1", "responses": {"Y": 1}}, {"id": "A2", "responses": {"Y": 0}}],
    )
    second = _build_source(
        "s2f-b-multi-b",
        [{"id": "B1", "responses": {"Y": 1}}, {"id": "B2", "responses": {"Y": 1}}],
    )
    qauth = _query_authority("s2f-b-multi")
    predicate = _branch_predicate(first, qauth, tag="all")
    query = _query(
        first,
        qauth,
        predicate,
        ("Y",),
        tag="s2f-b-multi",
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
        repository=first["repo"],
        query=query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(first["release_ref"], second["release_ref"]),
    )
    assert result.source_scope_mode == "SOURCE_INDEXED_MULTI_UNIVERSE"
    assert len(result.facts) == 2
    assert {fact.typed_state for fact in result.facts} == {"UNAVAILABLE"}
    assert all(
        not fact.empirical_universe_refs == query.empirical_universe_refs
        for fact in result.facts
    )

    # A real I05 receipt is required here: it references only the first
    # release while the closure legitimately retains both releases.  The first
    # artifact required receipt release refs to equal the whole closure release
    # set and therefore rejected this complete multi-release output.
    dauth = _d_auth("s2f-b-multi-discovery")
    y_query = _query(first, qauth, predicate, ("Y",), tag="s2f-b-multi-y")
    grammar = _grammar(
        operation="I03-OP-s2f-b-multi-discovery",
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
        first, grammar, dauth, tag="s2f-b-multi-discovery"
    )
    i05 = execute_i05(
        first,
        qauth,
        dauth,
        grammar,
        (predicate,),
        (y_query,),
        authority=authority,
    )
    assert len(i05.receipts) == 1
    base = _discovery_output(
        first,
        qauth,
        dauth,
        (predicate,),
        (y_query,),
        authority,
        i05,
        tag="s2f-b-multi",
    )
    graph = RouteBEmpiricalObjectGraph(
        authority_snapshots=base.object_graph.authority_snapshots,
        executed_predicates=base.object_graph.executed_predicates,
        executed_queries=tuple(
            sorted(
                {
                    obj.ref.key: obj
                    for obj in (*base.object_graph.executed_queries, query)
                }.values(),
                key=lambda obj: obj.ref.key,
            )
        ),
        empirical_facts=tuple(
            sorted(
                {
                    obj.ref.key: obj
                    for obj in (*base.object_graph.empirical_facts, *result.facts)
                }.values(),
                key=lambda obj: obj.ref.key,
            )
        ),
        discovery_authorities=base.object_graph.discovery_authorities,
        discovery_receipts=base.object_graph.discovery_receipts,
    )
    output = NativeEmpiricalOutput(
        source_identity=base.source_identity,
        release_identities=(
            base.release_identities[0],
            _release_identity(first),
            _release_identity(second),
        ),
        i03_results=(result,),
        i05_result=base.i05_result,
        object_graph=graph,
    )
    receipt = publish_empirical_closure(output, tmp_path / "cas")
    closure = open_empirical_closure(
        receipt.root_path, expected_root=receipt.root_identity
    ).require_trusted()

    assert len(closure.release_identities) == len(output.release_identities)
    assert {identity.release_ref.key for identity in closure.release_identities} == {
        identity.release_ref.key for identity in output.release_identities
    }
    assert len(closure.object_graph.discovery_receipts) == 1
    receipt_release_refs = {
        exact_ref(dict(ref)).key
        for ref in closure.object_graph.discovery_receipts[0].source_release_refs
    }
    assert receipt_release_refs
    assert receipt_release_refs.issubset(
        {identity.release_ref.key for identity in closure.release_identities}
    )
    restored = [
        fact for fact in closure.object_graph.empirical_facts
        if fact.typed_state == "UNAVAILABLE"
    ]
    assert len(restored) == 2
    query_universes = {exact_ref(dict(ref)).key for ref in query.empirical_universe_refs}
    for fact in restored:
        assert fact.empirical_universe_refs
        assert {exact_ref(dict(ref)).key for ref in fact.empirical_universe_refs}.issubset(
            query_universes
        )
        assert any(
            row["ref"] == fact.ref.as_dict()
            for row in closure.census["declared"]["negative_or_held"]
        )
    assert len(closure.census["f1_f4"]["F1_marginal_fact_refs"]) == len(
        [
            fact
            for fact in closure.object_graph.empirical_facts
            if fact.target_topology.get("requested_target_arity_and_topology", {}).get(
                "arity"
            )
            == 1
            or fact.target_topology.get("arity") == 1
        ]
    )
