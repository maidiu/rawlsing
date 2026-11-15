"""S2-F durable empirical closure mandatory cases (F01-F09).

These tests exercise the isolated sourcefree adapter at its actual grade:
synthetic native F1-F4/I05 output -> complete durable closure -> cold exact
reconstruction -> actual existing M1 composer + descriptive Field Forge reader.

They do not claim incoming S2-E acceptance, protected merge, original35 science,
or independent G5 receiving.  The original S2-F integration obligation remains a
declared dependency hold.
"""
from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import tempfile
import time
import zlib

import pytest

import rawlsing_next.pre553_route_b_production as route_b
from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.field_forge_conditional_support import (
    FieldForgeConditionalSupportError,
    produce_exact_conditional_support_profile,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_discovery_exact import (
    ExactBoundedDiscoveryResult,
    execute_exact_bounded_discovery,
)
from rawlsing_next.pre553_durable_empirical_closure import (
    DURABLE_CLOSURE_CONTRACT_SHA,
    DurableEmpiricalClosureError,
    DurableEmpiricalClosureUntrusted,
    EVIDENCE_GRADE,
    NativeEmpiricalOutput,
    ReleaseIdentity,
    _blob_manifest,
    _root_identity,
    open_empirical_closure,
    publish_empirical_closure,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    canonical_json,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_learned_world_composition import (
    LearnedWorldProductContractBinding,
    build_m1_bundle_from_m01,
)
from rawlsing_next.pre553_learned_empirical_adjudication import (
    M1ValidatorRegistry,
    _verify_bundle,
    adjudicate_learned_empirical,
)
from rawlsing_next.tests.pre553_query_frontier_fixtures import (
    k_way_bounded_joint_fixture,
)
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
    _auth,
    _branch_predicate,
    _build_source,
    _coordinate_leaf,
    _predicate,
    _query,
    _query_authority,
    _ref,
    _response_leaf,
    _run,
)
from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import (
    _binding,
)
from rawlsing_next.tests.test_pre553_route_b_production import (
    _execute as execute_m01,
    _fixture as m01_fixture,
)

ROOT = Path(__file__).resolve().parents[2]
RUNNER = Path(__file__).with_name("test_pyat940_s2f_fresh_process.py")
M1_CLAIM_FAMILY = "S2F_SOURCEFREE_CLAIM_FAMILY"
M1_CLAIM_RULE = "S2F_SOURCEFREE_CLAIM_RULE"


# ---------------------------------------------------------------------------
# native output builders
# ---------------------------------------------------------------------------


def _release_identity(source) -> ReleaseIdentity:
    release = source["repo"].resolve_release_exact(source["release_ref"])
    return ReleaseIdentity(
        release_ref=release.release_ref,
        replay_ref=release.replay_manifest.ref,
        source_artifact_ref=release.source_artifact_ref,
        source_release_manifest_hash=release.source_release_manifest_hash,
        semantic_release_hash=release.semantic_release_hash,
    )


def _discovery_output(
    source,
    qauth,
    dauth,
    predicates,
    queries,
    authority,
    result,
    *,
    tag: str,
) -> NativeEmpiricalOutput:
    graph = route_b.RouteBEmpiricalObjectGraph(
        authority_snapshots=tuple(
            sorted(
                {
                    obj.authority_ref.key: obj
                    for obj in (*source["authorities"], qauth, dauth)
                }.values(),
                key=lambda obj: obj.authority_ref.key,
            )
        ),
        executed_predicates=tuple(
            sorted(
                {obj.ref.key: obj for obj in (*predicates, *result.executed_predicates)}.values(),
                key=lambda obj: obj.ref.key,
            )
        ),
        executed_queries=tuple(
            sorted(
                {obj.ref.key: obj for obj in (*queries, *result.executed_queries)}.values(),
                key=lambda obj: obj.ref.key,
            )
        ),
        empirical_facts=tuple(sorted(result.empirical_facts, key=lambda obj: obj.ref.key)),
        discovery_authorities=(authority,),
        discovery_receipts=tuple(sorted(result.receipts, key=lambda obj: obj.ref.key)),
    )
    return NativeEmpiricalOutput(
        source_identity={
            "schema": "PYAT_S2F_SYNTHETIC_SOURCE_IDENTITY@1.0.0",
            "fixture_tag": tag,
            "original_source_objects_retained": 0,
        },
        release_identities=(_release_identity(source),),
        i03_results=(),
        i05_result=result,
        object_graph=graph,
    )


def _m01_output() -> dict:
    """Native M01 output with F1 marginal, F2/F3-free I05 receipt, F4 4-way fact."""

    fx = m01_fixture()
    source_stub = {
        "universe": fx["projection"].universes[0],
        "qrefs": fx["qrefs"],
        "risk_refs": {"R": fx["risk"]},
    }
    joint_two = _query(
        source_stub,
        fx["qauth"],
        fx["all_p"],
        ("X", "Y"),
        tag="s2f-joint-xy",
        target_authority_refs=(fx["projection_auth"].authority_ref,),
    )
    catalog = RuntimeObjectCatalog(
        authorities=fx["catalog"].authorities,
        predicates=fx["catalog"].predicates,
        queries=tuple((*fx["catalog"].queries, joint_two)),
        discovery_authorities=fx["catalog"].discovery_authorities,
    )
    requests = (
        *fx["requests"],
        route_b.I03ExecutionRequest(joint_two.ref, fx["all_p"].ref),
    )
    result = execute_m01(fx, catalog=catalog, requests=requests)
    joint_fact = next(
        fact
        for fact in result.object_graph.empirical_facts
        if exact_ref(dict(fact.empirical_query_spec_ref)) == joint_two.ref
    )
    return {
        "output": NativeEmpiricalOutput.from_route_b_result(result),
        "result": result,
        "joint_fact": joint_fact,
        "joint_query": joint_two,
    }


def _k_way_output() -> NativeEmpiricalOutput:
    source, fact = k_way_bounded_joint_fixture()
    qauth = _query_authority("r12-kway")
    predicate = _branch_predicate(source, qauth, tag="all")
    query = _query(source, qauth, predicate, ("A", "B", "C", "Y"), tag="four-way")
    execution = _run(source, qauth, predicate, query)
    assert execution.facts == (fact,)
    dauth = _d_auth("s2f-kway-discovery")
    grammar = _grammar(
        operation="I03-OP-s2f-kway-discovery",
        atoms=(),
        templates=(),
        rules=(),
        allow_empty=True,
    )
    authority = _discovery_authority(source, grammar, dauth, tag="s2f-kway-discovery")
    i05 = execute_i05(
        source,
        qauth,
        dauth,
        grammar,
        (predicate,),
        (query,),
        authority=authority,
    )
    graph = route_b.RouteBEmpiricalObjectGraph(
        authority_snapshots=tuple(
            sorted(
                {obj.authority_ref.key: obj for obj in (*source["authorities"], qauth, dauth)}.values(),
                key=lambda obj: obj.authority_ref.key,
            )
        ),
        executed_predicates=(predicate,),
        executed_queries=(query,),
        empirical_facts=(fact,),
        discovery_authorities=(authority,),
        discovery_receipts=(),
    )
    return NativeEmpiricalOutput(
        source_identity={
            "schema": "PYAT_S2F_SYNTHETIC_SOURCE_IDENTITY@1.0.0",
            "fixture_tag": "r12-kway",
            "original_source_objects_retained": 0,
        },
        release_identities=(_release_identity(source),),
        i03_results=(execution,),
        i05_result=i05,
        object_graph=graph,
    )


def _reversal_output() -> NativeEmpiricalOutput:
    rows = []
    for i in range(3):
        rows.append({"id": f"A1-{i}", "responses": {"X": 1, "Y": 1}, "coords": {"G": "A"}})
    for i in range(8):
        rows.append({"id": f"A0s-{i}", "responses": {"X": 0, "Y": 1}, "coords": {"G": "A"}})
    for i in range(2):
        rows.append({"id": f"A0f-{i}", "responses": {"X": 0, "Y": 0}, "coords": {"G": "A"}})
    for i in range(2):
        rows.append({"id": f"B1s-{i}", "responses": {"X": 1, "Y": 1}, "coords": {"G": "B"}})
    for i in range(8):
        rows.append({"id": f"B1f-{i}", "responses": {"X": 1, "Y": 0}, "coords": {"G": "B"}})
    for i in range(2):
        rows.append({"id": f"B0-{i}", "responses": {"X": 0, "Y": 0}, "coords": {"G": "B"}})
    source = _build_source("s2f-simpson", rows)
    qauth, dauth = _query_authority("s2f-simpson"), _d_auth("s2f-simpson-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="x1")
    x0 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 0), tag="x0")
    ga = _predicate(source, qauth, _coordinate_leaf(source, "G", "A"), tag="ga")
    gb = _predicate(source, qauth, _coordinate_leaf(source, "G", "B"), tag="gb")
    yq = _query(source, qauth, all_p, ("Y",), tag="y-template")
    grammar = _grammar(
        operation="I03-OP-s2f-simpson-discovery",
        atoms=(
            _atom("ALL", all_p, "BRANCH"),
            _atom("X1", x1, "RESPONSE"),
            _atom("X0", x0, "RESPONSE"),
            _atom("GA", ga, "COORDINATE"),
            _atom("GB", gb, "COORDINATE"),
        ),
        templates=(_qt("Y", yq),),
        rules=(
            _rule(
                "simpson",
                "CONDITIONAL_REVERSAL_OR_SIMPSON",
                "REVERSAL_GRID",
                baseline_atom_id="ALL",
                exposure_positive_atom_id="X1",
                exposure_negative_atom_id="X0",
                stratum_atom_ids=("GA", "GB"),
                query_template_id="Y",
                validation={"kind": "CONDITIONAL_REVERSAL", "target_cell": "1"},
            ),
        ),
        k=2,
    )
    authority = _discovery_authority(source, grammar, dauth, tag="s2f-simpson-discovery")
    result = execute_i05(
        source, qauth, dauth, grammar, (all_p, x1, x0, ga, gb), (yq,), authority=authority
    )
    return _discovery_output(
        source,
        qauth,
        dauth,
        (all_p, x1, x0, ga, gb),
        (yq,),
        authority,
        result,
        tag="s2f-simpson",
    )


def _minority_output() -> NativeEmpiricalOutput:
    rows = []
    for i in range(10):
        rows.append({"id": f"A{i}", "responses": {"Y": 0}, "coords": {"G": "A"}})
    for i in range(8):
        rows.append({"id": f"B{i}", "responses": {"Y": 0}, "coords": {"G": "B"}})
    for i in range(2):
        rows.append({"id": f"C{i}", "responses": {"Y": 1}, "coords": {"G": "C"}})
    source = _build_source("s2f-minority", rows)
    qauth, dauth = _query_authority("s2f-minority"), _d_auth("s2f-minority-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    c = _predicate(source, qauth, _coordinate_leaf(source, "G", "C"), tag="c")
    yq = _query(source, qauth, all_p, ("Y",), tag="y")
    grammar = _grammar(
        operation="I03-OP-s2f-minority-discovery",
        atoms=(_atom("ALL", all_p, "BRANCH"), _atom("C", c, "COORDINATE")),
        templates=(_qt("Y", yq),),
        rules=(
            _rule(
                "minority",
                "MINORITY_OR_NONMODAL_DEPARTURE",
                "SINGLE_ATOM",
                atom_ids=("C",),
                baseline_atom_id="ALL",
                query_template_id="Y",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            ),
        ),
    )
    authority = _discovery_authority(source, grammar, dauth, tag="s2f-minority-discovery")
    result = execute_i05(source, qauth, dauth, grammar, (all_p, c), (yq,), authority=authority)
    return _discovery_output(
        source, qauth, dauth, (all_p, c), (yq,), authority, result, tag="s2f-minority"
    )


def _empty_output() -> NativeEmpiricalOutput:
    source = _build_source(
        "s2f-empty",
        [{"id": "R1", "responses": {"Y": 0}}, {"id": "R2", "responses": {"Y": 1}}],
    )
    qauth, dauth = _query_authority("s2f-empty"), _d_auth("s2f-empty-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    empty = _branch_predicate(source, qauth, members=(), tag="empty")
    yq = _query(source, qauth, all_p, ("Y",), tag="y")
    grammar = _grammar(
        operation="I03-OP-s2f-empty-discovery",
        atoms=(_atom("ALL", all_p, "BRANCH"), _atom("EMPTY", empty, "BRANCH")),
        templates=(_qt("Y", yq),),
        rules=(
            _rule(
                "empty",
                "MINORITY_OR_NONMODAL_DEPARTURE",
                "SINGLE_ATOM",
                atom_ids=("EMPTY",),
                baseline_atom_id="ALL",
                query_template_id="Y",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            ),
        ),
    )
    authority = _discovery_authority(source, grammar, dauth, tag="s2f-empty-discovery")
    result = execute_i05(
        source, qauth, dauth, grammar, (all_p, empty), (yq,), authority=authority
    )
    return _discovery_output(
        source, qauth, dauth, (all_p, empty), (yq,), authority, result, tag="s2f-empty"
    )


def _changed_output(rows) -> NativeEmpiricalOutput:
    source = _build_source("s2f-change", rows)
    qauth, dauth = _query_authority("s2f-change"), _d_auth("s2f-change-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    query = _query(source, qauth, all_p, ("X", "Y"), tag="joint")
    execution = _run(source, qauth, all_p, query)
    grammar = _grammar(
        operation="I03-OP-s2f-change-discovery",
        atoms=(),
        templates=(),
        rules=(),
        allow_empty=True,
    )
    authority = _discovery_authority(source, grammar, dauth, tag="s2f-change-discovery")
    i05 = execute_i05(source, qauth, dauth, grammar, (), (), authority=authority)
    graph = route_b.RouteBEmpiricalObjectGraph(
        authority_snapshots=tuple(
            sorted(
                {obj.authority_ref.key: obj for obj in (*source["authorities"], qauth, dauth)}.values(),
                key=lambda obj: obj.authority_ref.key,
            )
        ),
        executed_predicates=(all_p,),
        executed_queries=(query,),
        empirical_facts=execution.facts,
        discovery_authorities=(authority,),
        discovery_receipts=(),
    )
    return NativeEmpiricalOutput(
        source_identity={
            "schema": "PYAT_S2F_SYNTHETIC_SOURCE_IDENTITY@1.0.0",
            "fixture_tag": "s2f-change",
            "rows": len(rows),
        },
        release_identities=(_release_identity(source),),
        i03_results=(execution,),
        i05_result=i05,
        object_graph=graph,
    )


# ---------------------------------------------------------------------------
# consumer binding / descriptive consumer
# ---------------------------------------------------------------------------


def _consumer_binding(result) -> tuple[dict, Any]:
    validator = _auth("s2f-m1-validator", "M1_VALIDATOR", families=("EmpiricalFact@1.0.0",))
    binding = _binding(
        validator,
        claim_family=M1_CLAIM_FAMILY,
        claim_rule=M1_CLAIM_RULE,
    )
    contract = LearnedWorldProductContractBinding(
        route="M01_M1_M2_B5",
        product_family_ref=_ref("PRODUCT_FAMILY", "s2f"),
        producer_owner_ref=_ref("PRODUCER_OWNER", "s2f"),
        producer_contract_ref=_ref("PRODUCER_CONTRACT", "s2f"),
        release_subject_kind="LEARNED_EMPIRICAL_PRODUCT",
        selection_scope_ref=_ref("SELECTION_SCOPE", "s2f"),
        producer_permission_ceiling_ref=_ref("PERMISSION_CEILING", "s2f"),
        consumer_product_purpose_ref=_ref("CONSUMER_PURPOSE", "s2f"),
        m1_family_rule_binding_ref=binding.ref,
    )
    selected = tuple(receipt.ref for receipt in result.i05_result.receipts)
    scope = {"fixture": "S2F_SOURCEFREE_ISOLATED", "claim": M1_CLAIM_RULE}
    document = {
        "kind": "M1_BUNDLE_COMPOSER",
        "contract_kwargs": {
            "route": contract.route,
            "product_family_ref": contract.product_family_ref.as_dict(),
            "producer_owner_ref": contract.producer_owner_ref.as_dict(),
            "producer_contract_ref": contract.producer_contract_ref.as_dict(),
            "release_subject_kind": contract.release_subject_kind,
            "selection_scope_ref": contract.selection_scope_ref.as_dict(),
            "producer_permission_ceiling_ref": contract.producer_permission_ceiling_ref.as_dict(),
            "consumer_product_purpose_ref": contract.consumer_product_purpose_ref.as_dict(),
            "m1_family_rule_binding_ref": contract.m1_family_rule_binding_ref.as_dict(),
        },
        "binding_kwargs": {
            "claim_family_id": binding.claim_family_id,
            "claim_rule_id": binding.claim_rule_id,
            "validator_authority_ref": binding.validator_authority_ref.as_dict(),
            "selection_purpose": binding.selection_purpose,
            "current_selection_authority_ref": None,
            "applicability_scope": dict(binding.applicability_scope),
            "allowed_input_object_families_and_states": {
                key: list(value)
                for key, value in binding.allowed_input_object_families_and_states.items()
            },
            "required_prerequisite_channels": list(binding.required_prerequisite_channels),
            "required_source_relation_kinds": list(binding.required_source_relation_kinds),
            "required_measure_weight_estimand_authorities": [
                ref.as_dict() for ref in binding.required_measure_weight_estimand_authorities
            ],
            "required_coverage_strength": {
                key: list(value) for key, value in binding.required_coverage_strength.items()
            },
            "uncertainty_policy_ref": binding.uncertainty_policy_ref.as_dict(),
            "output_semantic_contract": dict(binding.output_semantic_contract),
            "semantic_ceiling": binding.semantic_ceiling,
            "validator_algorithm_identity_if_required": binding.validator_algorithm_identity_if_required,
            "validator_parameters_ref": binding.validator_parameters_ref.as_dict(),
            "replay_contract_ref": binding.replay_contract_ref.as_dict(),
            "authority_closure_refs": [
                ref.as_dict() for ref in binding.authority_closure_refs
            ],
        },
        "selected_discovery_receipt_refs": [ref.as_dict() for ref in selected],
        "requested_scope": scope,
        "additional_authority_refs": [],
        "additional_dependency_refs": [],
        "prerequisite_channel_documents": [],
    }
    return document, (contract, binding, selected, scope)


def _field_forge_consumer(joint_fact, joint_query, qrefs) -> dict:
    return {
        "kind": "FIELD_FORGE_EXACT_CONDITIONAL_SUPPORT",
        "joint_fact_ref": joint_fact.ref.as_dict(),
        "joint_query_ref": joint_query.ref.as_dict(),
        "conditioner_ref": qrefs["X"].as_dict(),
        "target_ref": qrefs["Y"].as_dict(),
        "producer_permission_ceiling": ["DESCRIPTIVE_SUPPORT_ONLY"],
        "relation_permission_ceiling": ["DESCRIPTIVE_SUPPORT_ONLY"],
    }


def _native_m1_bundle(m01: dict):
    contract, binding, selected, scope = m01["binding_parts"]
    return build_m1_bundle_from_m01(
        m01["result"],
        contract=contract,
        family_rule_binding=binding,
        selected_discovery_receipt_refs=selected,
        requested_scope=scope,
    )


# ---------------------------------------------------------------------------
# mutation helpers
# ---------------------------------------------------------------------------


def _blob_path(root: Path, digest: str) -> Path:
    return root / "cas" / "blobs" / f"{digest}.json.z"


def _load_doc(blob_path: Path):
    return json.loads(zlib.decompress(blob_path.read_bytes()).decode("utf-8"))


def _store_doc(blob_path: Path, document) -> None:
    blob_path.write_bytes(zlib.compress(canonical_json(document).encode("utf-8"), 9))


def _rewrite_manifest(manifest: dict) -> dict:
    core = manifest["core"]
    closure_identity = semantic_hash(core)
    root_identity = _root_identity(
        closure_identity, _blob_manifest(core["objects"], core["fragments"])
    )
    manifest["publication"] = {
        "closure_identity": closure_identity,
        "root_identity": root_identity,
        "evidence_grade": EVIDENCE_GRADE,
    }
    return manifest


def _save_manifest(manifest: dict, path: Path) -> None:
    path.write_bytes(canonical_json(manifest).encode("utf-8"))


def _copy_closure(root: Path) -> Path:
    destination = Path(tempfile.mkdtemp(prefix="s2f-mutation-"))
    shutil.copytree(root, destination, dirs_exist_ok=True)
    return destination


# ---------------------------------------------------------------------------
# F01 complete F1-F4/I05 preimage census
# ---------------------------------------------------------------------------


def test_f01_complete_native_f1_f4_i05_preimage_census(tmp_path):
    root = tmp_path / "cas"
    m01 = _m01_output()
    m01_doc, m01_parts = _consumer_binding(m01["result"])
    m01["binding_parts"] = m01_parts
    joint_query = m01["joint_query"]
    qrefs = {
        "X": exact_ref(dict(joint_query.target_refs[0])),
        "Y": exact_ref(dict(joint_query.target_refs[1])),
    }
    ff = _field_forge_consumer(m01["joint_fact"], joint_query, qrefs)
    closures = {
        "M01": publish_empirical_closure(
            m01["output"],
            root,
            consumer_binding=m01_doc,
            descriptive_consumer=ff,
        ),
        "REVERSAL": publish_empirical_closure(_reversal_output(), root),
        "MINORITY": publish_empirical_closure(_minority_output(), root),
        "K_WAY": publish_empirical_closure(_k_way_output(), root),
        "EMPTY": publish_empirical_closure(_empty_output(), root),
    }
    opened = {
        name: open_empirical_closure(receipt.root_path, expected_root=receipt.root_identity)
        for name, receipt in closures.items()
    }
    for closure in opened.values():
        closure.require_trusted()
        closure.assert_no_current_authority()
        declared = closure.census["declared"]
        assert declared["original_source_objects_materialized"] == 0
        assert declared["source_objects_retained"] == 0
        assert declared["fact_rows"]
        if closure.i05_result.receipts:
            assert declared["receipt_rows"]
        # every retained fact carries its exact risk/denominator/used provenance refs
        provenance_kinds: set[str] = set()
        for fact in closure.object_graph.empirical_facts:
            provenance = {exact_ref(dict(ref)).kind for ref in fact.source_empirical_provenance_refs}
            provenance_kinds.update(provenance)
            assert "C11LogicalRelease" in provenance
            assert "PRE553_I03_QUERY_REPLAY" not in provenance  # replay is a separate exact field
        assert "RespondentEvent@1.0.0" in provenance_kinds or (
            "EmpiricalCoordinateFact@1.0.0" in provenance_kinds
        )

    assert opened["M01"].census["f1_f4"]["F1_marginal_fact_refs"]
    assert opened["M01"].census["f1_f4"]["F4_same_respondent_joint_fact_refs"] == ()
    assert opened["K_WAY"].census["f1_f4"]["F4_same_respondent_joint_fact_refs"]
    assert opened["REVERSAL"].census["f1_f4"]["F2_reversal_receipt_refs"]
    assert opened["MINORITY"].census["f1_f4"]["F3_minority_receipt_refs"]
    assert opened["EMPTY"].census["declared"]["negative_or_held"]
    assert opened["EMPTY"].census["declared"]["receipt_state_counts"] == {"VALID_EMPTY": 1}

    # Complete object census: every native graph object is stored exactly once.
    m01_closure = opened["M01"]
    stored = {
        exact_ref(dict(entry["ref"])).key for entry in m01_closure.manifest["core"]["objects"]
    }
    native = {obj.ref.key for obj in m01["result"].object_graph.public_objects()}
    assert stored == native
    assert len(stored) == len(m01["result"].object_graph.public_objects())

    # Reconstructed preimages are byte-exact against the native in-memory objects.
    for family, objects in (
        ("authority_snapshots", m01_closure.object_graph.authority_snapshots),
        ("executed_predicates", m01_closure.object_graph.executed_predicates),
        ("executed_queries", m01_closure.object_graph.executed_queries),
        ("empirical_facts", m01_closure.object_graph.empirical_facts),
        ("discovery_authorities", m01_closure.object_graph.discovery_authorities),
        ("discovery_receipts", m01_closure.object_graph.discovery_receipts),
    ):
        native_objects = {
            obj.ref.key: obj for obj in getattr(m01["result"].object_graph, family)
        }
        assert len(objects) == len(native_objects)
        for obj in objects:
            assert canonical_json(obj.semantic_projection()) == canonical_json(
                native_objects[obj.ref.key].semantic_projection()
            )

    # Negative/held/unvisited conservation is declared, not inferred.
    for closure in opened.values():
        declared = closure.census["declared"]
        assert isinstance(declared["unvisited_state"], str)
        assert declared["absent_fact_states_in_this_output"]
        assert declared["absent_receipt_states_in_this_output"]


# ---------------------------------------------------------------------------
# FIABC exact fragment primitive parity (sourcefree adaptation check)
# ---------------------------------------------------------------------------


def test_fragment_map_matches_fiabc_exact_primitive():
    from rawlsing_next.fiabc_final_oracle_freeze_producers import (
        _hydrate_lits_canonical_preimage,
        _pack_lits_canonical_preimage,
    )
    from rawlsing_next.pre553_durable_empirical_fragments import (
        hydrate_canonical_preimage,
        pack_canonical_preimage,
    )

    m01 = _m01_output()
    facts = m01["output"].object_graph.empirical_facts
    ours: dict = {}
    theirs: dict = {}
    for fact in facts:
        document = fact.as_dict()
        assert pack_canonical_preimage(document, ours) == _pack_lits_canonical_preimage(
            document, theirs
        )
    assert canonical_json(ours) == canonical_json(theirs)
    for fact in facts:
        assert hydrate_canonical_preimage(
            pack_canonical_preimage(fact.as_dict(), ours), ours
        ) == _hydrate_lits_canonical_preimage(
            _pack_lits_canonical_preimage(fact.as_dict(), theirs), theirs
        )


# ---------------------------------------------------------------------------
# F02 native -> cold M1 composer + descriptive Field Forge
# ---------------------------------------------------------------------------


def _publish_primary(tmp_path) -> dict:
    root = tmp_path / "cas"
    m01 = _m01_output()
    binding_doc, parts = _consumer_binding(m01["result"])
    m01["binding_parts"] = parts
    # Recover the exact native question refs from the fixture's query objects.
    joint_query = m01["joint_query"]
    qrefs = {
        "X": exact_ref(dict(joint_query.target_refs[0])),
        "Y": exact_ref(dict(joint_query.target_refs[1])),
    }
    ff = _field_forge_consumer(m01["joint_fact"], joint_query, qrefs)
    receipt = publish_empirical_closure(
        m01["output"],
        root,
        consumer_binding=binding_doc,
        descriptive_consumer=ff,
    )
    native_bundle = _native_m1_bundle(m01)
    native_profile = produce_exact_conditional_support_profile(
        joint_fact=m01["joint_fact"],
        joint_query=joint_query,
        conditioner_ref=qrefs["X"],
        target_ref=qrefs["Y"],
        producer_permission_ceiling=("DESCRIPTIVE_SUPPORT_ONLY",),
    )
    return {
        "m01": m01,
        "receipt": receipt,
        "native_bundle": native_bundle,
        "native_profile": native_profile,
        "consumer_binding": binding_doc,
        "descriptive_consumer": ff,
    }


def test_f02_native_to_cold_m1_and_descriptive_reader(tmp_path):
    primary = _publish_primary(tmp_path)
    closure = open_empirical_closure(
        primary["receipt"].root_path, expected_root=primary["receipt"].root_identity
    ).require_trusted()
    cold_bundle = closure.m1_bundle_from_declared_binding()
    assert cold_bundle.content_hash == primary["native_bundle"].content_hash
    assert cold_bundle.object_id == primary["native_bundle"].object_id
    assert canonical_json(cold_bundle.semantic_projection()) == canonical_json(
        primary["native_bundle"].semantic_projection()
    )

    cold_profile = closure.field_forge_profile_from_declared_consumer()
    assert cold_profile.content_hash == primary["native_profile"].content_hash
    assert cold_profile.object_id == primary["native_profile"].object_id
    assert canonical_json(cold_profile.semantic_projection()) == canonical_json(
        primary["native_profile"].semantic_projection()
    )

    # The actual existing M1 composer accepted the reconstructed graph; the
    # consumer result is the same exact native object graph, not a model proxy.
    assert len(cold_bundle.discovery_receipts) == len(primary["m01"]["result"].i05_result.receipts)
    assert all(
        isinstance(fact, EmpiricalFact) for fact in cold_bundle.empirical_facts
    )
    assert all(
        isinstance(query, EmpiricalQuerySpec) for query in cold_bundle.empirical_queries
    )
    assert all(
        isinstance(predicate, EmpiricalPredicate)
        for predicate in cold_bundle.empirical_predicates
    )
    # The actual M1 owner accepts the reconstructed bundle structurally and its
    # actual adjudicator reaches a governed BLOCKED outcome solely because no
    # synthetic family validator is registered (not because closure is missing).
    _verify_bundle(cold_bundle)
    _verify_bundle(primary["native_bundle"])
    binding = primary["m01"]["binding_parts"][1]
    disposition = adjudicate_learned_empirical(
        cold_bundle, binding, validator_registry=M1ValidatorRegistry()
    )
    assert disposition.adjudication_outcome == "BLOCKED"
    assert disposition.reason_code == "RULE_BINDING_OR_PREREQUISITE_BLOCKED"

    registry = AuthorityRegistry(tuple(cold_bundle.authority_snapshots))
    for obj in (
        *cold_bundle.empirical_facts,
        *cold_bundle.empirical_queries,
        *cold_bundle.empirical_predicates,
        *cold_bundle.discovery_receipts,
        *cold_bundle.discovery_authorities,
    ):
        # A replay closure never mints current rights; it only resolves the
        # retained historical snapshots under their exact identities.
        from rawlsing_next.pre553_empirical_authority import (
            validate_object_authority_closure,
        )

        validate_object_authority_closure(obj, registry)


# ---------------------------------------------------------------------------
# F03 changed value / restoration exact identity
# ---------------------------------------------------------------------------


def test_f03_changed_value_restoration_exact_identity(tmp_path):
    original_rows = [
        {"id": "R1", "responses": {"X": 1, "Y": 1}},
        {"id": "R2", "responses": {"X": 0, "Y": 0}},
        {"id": "R3", "responses": {"X": 1, "Y": 0}},
    ]
    changed_rows = [
        {"id": "R1", "responses": {"X": 1, "Y": 1}},
        {"id": "R2", "responses": {"X": 0, "Y": 0}},
        {"id": "R3", "responses": {"X": 0, "Y": 0}},
    ]
    root = tmp_path / "cas"
    first_output = _changed_output(original_rows)
    changed_output = _changed_output(changed_rows)
    restored_output = _changed_output(original_rows)
    first = publish_empirical_closure(first_output, root)
    changed = publish_empirical_closure(changed_output, root)
    restored = publish_empirical_closure(restored_output, root)

    assert first_output.i03_results[0].facts[0].ref != changed_output.i03_results[0].facts[0].ref
    assert first_output.i03_results[0].facts[0].ref == restored_output.i03_results[0].facts[0].ref
    assert first.root_identity != changed.root_identity
    assert restored.root_identity == first.root_identity
    assert restored.closure_identity == first.closure_identity
    assert restored.published is False

    first_closure = open_empirical_closure(
        first.root_path, expected_root=first.root_identity
    )
    restored_closure = open_empirical_closure(
        restored.root_path, expected_root=restored.root_identity
    )
    assert canonical_json(first_closure.object_graph.empirical_facts[0].as_dict()) == canonical_json(
        restored_closure.object_graph.empirical_facts[0].as_dict()
    )
    assert first_closure.i05_result.valid_empty is True
    assert first_closure.i05_result.replay_ref == restored_closure.i05_result.replay_ref


# ---------------------------------------------------------------------------
# F04 delete/modify mandatory fragment refusal
# ---------------------------------------------------------------------------


def _fresh_primary(tmp_path) -> dict:
    return _publish_primary(tmp_path)


def test_f04_delete_modify_required_fragment_refusal(tmp_path):
    primary = _fresh_primary(tmp_path)
    root = Path(primary["receipt"].root_path).parent.parent

    # 1. delete one mandatory fact fragment blob
    victim = _copy_closure(root)
    manifest = json.loads((Path(primary["receipt"].root_path) / "manifest.json").read_text())
    fragment = manifest["core"]["fragments"][0]
    _blob_path(victim, fragment["fragment_hash"]).unlink()
    with pytest.raises(DurableEmpiricalClosureError):
        open_empirical_closure(
            victim / "closures" / Path(primary["receipt"].root_path).name,
            expected_root=primary["receipt"].root_identity,
        )
    shutil.rmtree(victim)

    # 2. corrupt one mandatory fragment blob without changing its name
    victim = _copy_closure(root)
    blob = _blob_path(victim, fragment["fragment_hash"])
    blob.write_bytes(blob.read_bytes()[:-3] + b"\x00\x00\x00")
    with pytest.raises((DurableEmpiricalClosureError, zlib.error, ValueError)):
        open_empirical_closure(
            victim / "closures" / Path(primary["receipt"].root_path).name,
            expected_root=primary["receipt"].root_identity,
        )
    shutil.rmtree(victim)

    # 3. delete one mandatory query object blob
    victim = _copy_closure(root)
    query_entry = next(
        entry for entry in manifest["core"]["objects"] if entry["family"].startswith("EmpiricalQuerySpec")
    )
    _blob_path(victim, query_entry["document_hash"]).unlink()
    with pytest.raises(DurableEmpiricalClosureError):
        open_empirical_closure(
            victim / "closures" / Path(primary["receipt"].root_path).name,
            expected_root=primary["receipt"].root_identity,
        )
    shutil.rmtree(victim)

    # 4. coherently re-hash a changed query direction without repairing the
    #    exact fact/receipt role preimages.
    victim = _copy_closure(root)
    closing = victim / "closures" / Path(primary["receipt"].root_path).name
    manifest = json.loads((closing / "manifest.json").read_text())
    query_entry = None
    document = None
    for entry in manifest["core"]["objects"]:
        if entry["family"] != "EmpiricalQuerySpec@1.0.0":
            continue
        candidate = _load_doc(_blob_path(victim, entry["document_hash"]))
        components = candidate["semantic_fields"]["target_arity_and_topology"]["components"]
        if len(components) == 2:
            query_entry = entry
            document = candidate
            break
    assert query_entry is not None and document is not None
    components = document["semantic_fields"]["target_arity_and_topology"]["components"]
    components.reverse()
    old_hash = query_entry["document_hash"]
    document["content_hash"] = semantic_hash(
        {key: value for key, value in document.items() if key not in {"object_id", "content_hash"}}
    )
    document["object_id"] = (
        "urn:rawlsing:pre553:EmpiricalQuerySpec:sha256:" + document["content_hash"]
    )
    new_hash = semantic_hash(document)
    assert new_hash != old_hash
    _store_doc(_blob_path(victim, new_hash), document)
    _blob_path(victim, old_hash).unlink()
    query_entry["document_hash"] = new_hash
    query_entry["ref"] = {
        "kind": "EmpiricalQuerySpec@1.0.0",
        "object_id": document["object_id"],
        "content_hash": document["content_hash"],
    }
    query_entry["document_uncompressed_bytes"] = len(canonical_json(document).encode())
    query_entry["document_compressed_bytes"] = _blob_path(victim, new_hash).stat().st_size
    manifest = _rewrite_manifest(manifest)
    _save_manifest(manifest, closing / "manifest.json")
    # The external old pin rejects the coherent self-rehash outright.
    with pytest.raises(DurableEmpiricalClosureError):
        open_empirical_closure(closing, expected_root=primary["receipt"].root_identity)
    # With the rewritten self-hash supplied as a new pin, the semantic closure
    # still refuses: the fact/receipt role preimages no longer resolve to the
    # changed query direction.  A self-rehash is not a repair.
    with pytest.raises(DurableEmpiricalClosureError):
        open_empirical_closure(
            closing, expected_root=manifest["publication"]["root_identity"]
        )
    # Without an external pin the closure is untrusted even if internally
    # coherent.
    with pytest.raises(DurableEmpiricalClosureUntrusted):
        open_empirical_closure(closing, expected_root=None)
    shutil.rmtree(victim)


# ---------------------------------------------------------------------------
# F05 condition/risk/denominator/negative frontier/replay conservation
# ---------------------------------------------------------------------------


def test_f05_condition_risk_denominator_negative_frontier_replay_conservation(tmp_path):
    primary = _fresh_primary(tmp_path)
    root = Path(primary["receipt"].root_path).parent.parent
    closure = open_empirical_closure(
        primary["receipt"].root_path, expected_root=primary["receipt"].root_identity
    )
    closing = Path(primary["receipt"].root_path)
    manifest = json.loads((closing / "manifest.json").read_text())

    # Replay preimage substitution is refused.
    victim = _copy_closure(root)
    mutated = json.loads((victim / "closures" / closing.name / "manifest.json").read_text())
    mutated["core"]["replays"]["facts"][0]["material_hash"] = "f" * 64
    mutated = _rewrite_manifest(mutated)
    _save_manifest(mutated, victim / "closures" / closing.name / "manifest.json")
    with pytest.raises(DurableEmpiricalClosureError):
        open_empirical_closure(
            victim / "closures" / closing.name, expected_root=mutated["publication"]["root_identity"]
        )
    shutil.rmtree(victim)

    # Frontier candidate identity substitution is refused.
    victim = _copy_closure(root)
    mutated = json.loads((victim / "closures" / closing.name / "manifest.json").read_text())
    mutated["core"]["replays"]["frontier"]["material"]["candidate_identities"][0][
        "candidate_hash"
    ] = "e" * 64
    mutated = _rewrite_manifest(mutated)
    _save_manifest(mutated, victim / "closures" / closing.name / "manifest.json")
    with pytest.raises(DurableEmpiricalClosureError):
        open_empirical_closure(
            victim / "closures" / closing.name, expected_root=mutated["publication"]["root_identity"]
        )
    shutil.rmtree(victim)

    # A negative/unvisited fate cannot be silently promoted while the final
    # frontier still declares valid_empty.
    empty = _empty_output()
    empty_receipt = publish_empirical_closure(empty, root)
    empty_closing = Path(empty_receipt.root_path)
    victim = _copy_closure(root)
    mutated = json.loads((victim / "closures" / empty_closing.name / "manifest.json").read_text())
    receipt_entry = next(
        entry
        for entry in mutated["core"]["objects"]
        if entry["family"] == "DiscoveryResultReceipt@1.0.0"
    )
    blob = _blob_path(victim, receipt_entry["document_hash"])
    document = _load_doc(blob)
    document["typed_state"] = "DISCOVERED_RESULT_SUPPORTED"
    document["content_hash"] = semantic_hash(
        {key: value for key, value in document.items() if key not in {"object_id", "content_hash"}}
    )
    document["object_id"] = (
        "urn:rawlsing:pre553:DiscoveryResultReceipt:sha256:" + document["content_hash"]
    )
    old_hash = receipt_entry["document_hash"]
    new_hash = semantic_hash(document)
    _store_doc(_blob_path(victim, new_hash), document)
    _blob_path(victim, old_hash).unlink()
    receipt_entry["document_hash"] = new_hash
    receipt_entry["ref"] = {
        "kind": "DiscoveryResultReceipt@1.0.0",
        "object_id": document["object_id"],
        "content_hash": document["content_hash"],
    }
    receipt_entry["document_uncompressed_bytes"] = len(canonical_json(document).encode())
    receipt_entry["document_compressed_bytes"] = _blob_path(victim, new_hash).stat().st_size
    mutated = _rewrite_manifest(mutated)
    _save_manifest(mutated, victim / "closures" / empty_closing.name / "manifest.json")
    with pytest.raises(DurableEmpiricalClosureError):
        open_empirical_closure(
            victim / "closures" / empty_closing.name, expected_root=mutated["publication"]["root_identity"]
        )
    shutil.rmtree(victim)

    # A tampered denominator member set is refused by the exact conservation
    # check even if the fact object is re-materialized under a fresh identity.
    from rawlsing_next.pre553_durable_empirical_closure import _fact_rows

    positive = next(
        fact
        for fact in closure.object_graph.empirical_facts
        if fact.raw_denominator_support > 0 and fact.denominator_member_refs
    )
    fields = dict(positive.semantic_fields)
    fields["denominator_member_refs"] = tuple(positive.denominator_member_refs)[:-1]
    tampered = EmpiricalFact(
        typed_state=positive.typed_state,
        authority_snapshot_refs=positive.authority_snapshot_refs,
        dependency_refs=positive.dependency_refs,
        producer_replay_locator_or_reference_root=positive.producer_replay_locator_or_reference_root,
        **fields,
    )
    queries = {obj.ref.key: obj for obj in closure.object_graph.executed_queries}
    predicates = {obj.ref.key: obj for obj in closure.object_graph.executed_predicates}
    with pytest.raises(DurableEmpiricalClosureError):
        _fact_rows(tampered, queries, predicates)

    # The unmodified closure still passes the semantic conservation checks.
    for fact in closure.object_graph.empirical_facts:
        assert len(fact.denominator_member_refs) == fact.raw_denominator_support
        if fact.typed_state in {"SUPPORTED", "OBSERVED_ZERO"}:
            assert (
                sum(
                    row["raw_numerator_support"]
                    for row in fact.target_topology["complete_cell_semantic_projection"]
                )
                == fact.raw_numerator_support
            )


# ---------------------------------------------------------------------------
# F06 wrong source / unpinned self-hash / no current-rights reissue
# ---------------------------------------------------------------------------


def test_f06_wrong_source_unpinned_selfhash_and_current_rights(tmp_path):
    primary = _fresh_primary(tmp_path)
    closing = Path(primary["receipt"].root_path)
    root = closing.parent.parent

    with pytest.raises(DurableEmpiricalClosureUntrusted):
        open_empirical_closure(closing, expected_root=None)

    unpinned = open_empirical_closure(
        closing, expected_root=None, allow_unpinned=True
    )
    assert unpinned.trust_state == "UNPINNED_SELF_HASH"
    with pytest.raises(DurableEmpiricalClosureUntrusted):
        unpinned.m1_bundle_from_declared_binding()
    with pytest.raises(DurableEmpiricalClosureUntrusted):
        unpinned.field_forge_profile_from_declared_consumer()

    closure = open_empirical_closure(
        closing, expected_root=primary["receipt"].root_identity
    ).require_trusted()
    closure.assert_no_current_authority()
    # Verified consumer/replay state is immutable in-process; a caller cannot
    # mutate the declared binding after verification.
    with pytest.raises(TypeError):
        closure.consumer_binding["kind"] = "MUTATED"
    with pytest.raises(TypeError):
        closure.manifest["core"]["rights_state"] = "CURRENT_AUTHORITY"
    untrusted_view = replace(closure, trust_state="UNPINNED_SELF_HASH")
    with pytest.raises(DurableEmpiricalClosureUntrusted):
        untrusted_view.require_trusted()
    # The replay view is deliberately not a C11LogicalRelease and exposes no
    # repository/source reader.
    view = closure.m01_replay_view()
    assert type(view.c11_release).__name__ == "DurableReleaseRefView"
    assert not hasattr(view.c11_release, "public_objects")
    assert not hasattr(view.c11_release, "internal_records")

    # Wrong source/release identity is refused even with a new self-hash pin.
    victim = _copy_closure(root)
    mutated = json.loads((victim / "closures" / closing.name / "manifest.json").read_text())
    mutated["core"]["native_result"]["release_identities"][0]["release_ref"] = {
        "kind": "C11LogicalRelease",
        "object_id": "WRONG-SOURCE-RELEASE",
        "content_hash": "a" * 64,
    }
    mutated = _rewrite_manifest(mutated)
    _save_manifest(mutated, victim / "closures" / closing.name / "manifest.json")
    with pytest.raises(DurableEmpiricalClosureError):
        open_empirical_closure(
            victim / "closures" / closing.name, expected_root=mutated["publication"]["root_identity"]
        )
    shutil.rmtree(victim)

    # Exact authority alteration is refused even under a new self-hash pin.
    victim = _copy_closure(root)
    mutated = json.loads((victim / "closures" / closing.name / "manifest.json").read_text())
    authority_entry = next(
        entry
        for entry in mutated["core"]["objects"]
        if entry["family"] == "AuthoritySnapshot@1.0.0"
    )
    authority_blob = _blob_path(victim, authority_entry["document_hash"])
    authority_doc = _load_doc(authority_blob)
    authority_doc["typed_state"] = "DENY"
    authority_doc["semantic_fields"]["decision_state"] = "DENY"
    old_authority_hash = authority_entry["document_hash"]
    authority_doc["content_hash"] = semantic_hash(
        {
            key: value
            for key, value in authority_doc.items()
            if key not in {"object_id", "content_hash"}
        }
    )
    authority_doc["object_id"] = (
        "urn:rawlsing:pre553:AuthoritySnapshot:sha256:" + authority_doc["content_hash"]
    )
    new_authority_hash = semantic_hash(authority_doc)
    _store_doc(_blob_path(victim, new_authority_hash), authority_doc)
    _blob_path(victim, old_authority_hash).unlink()
    authority_entry["document_hash"] = new_authority_hash
    authority_entry["ref"] = {
        "kind": "AuthoritySnapshot@1.0.0",
        "object_id": authority_doc["object_id"],
        "content_hash": authority_doc["content_hash"],
    }
    authority_entry["document_uncompressed_bytes"] = len(
        canonical_json(authority_doc).encode()
    )
    authority_entry["document_compressed_bytes"] = _blob_path(
        victim, new_authority_hash
    ).stat().st_size
    mutated = _rewrite_manifest(mutated)
    _save_manifest(mutated, victim / "closures" / closing.name / "manifest.json")
    with pytest.raises(DurableEmpiricalClosureError):
        open_empirical_closure(
            victim / "closures" / closing.name,
            expected_root=mutated["publication"]["root_identity"],
        )
    shutil.rmtree(victim)

    # A right-state promotion is refused.
    victim = _copy_closure(root)
    mutated = json.loads((victim / "closures" / closing.name / "manifest.json").read_text())
    mutated["core"]["rights_state"] = "CURRENT_AUTHORITY"
    mutated = _rewrite_manifest(mutated)
    _save_manifest(mutated, victim / "closures" / closing.name / "manifest.json")
    promoted = open_empirical_closure(
        victim / "closures" / closing.name, expected_root=mutated["publication"]["root_identity"]
    )
    with pytest.raises(DurableEmpiricalClosureError):
        promoted.assert_no_current_authority()
    shutil.rmtree(victim)


# ---------------------------------------------------------------------------
# F07 fresh process, zero original source opens
# ---------------------------------------------------------------------------


def test_f07_fresh_process_zero_original_source_opens(tmp_path):
    primary = _fresh_primary(tmp_path)
    expected = {
        "root_identity": primary["receipt"].root_identity,
        "closure_identity": primary["receipt"].closure_identity,
        "m1_bundle_content_hash": primary["native_bundle"].content_hash,
        "m1_bundle_object_id": primary["native_bundle"].object_id,
        "ff_profile_content_hash": primary["native_profile"].content_hash,
        "ff_profile_object_id": primary["native_profile"].object_id,
        "fact_refs": [
            fact.ref.as_dict()
            for fact in primary["m01"]["output"].object_graph.empirical_facts
        ],
        "receipt_refs": [
            receipt.ref.as_dict()
            for receipt in primary["m01"]["output"].object_graph.discovery_receipts
        ],
    }
    expected_path = tmp_path / "expected.json"
    expected_path.write_text(canonical_json(expected))
    child_cwd = Path(tempfile.mkdtemp(prefix="s2f-child-cwd-"))
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    completed = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            str(primary["receipt"].root_path),
            primary["receipt"].root_identity,
            str(expected_path),
        ],
        cwd=child_cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout)
    assert observed["trust_state"] == "EXTERNALLY_PINNED"
    assert observed["source_opens"] == 0
    assert observed["closure_opens"] > 0
    assert observed["m1_bundle_content_hash"] == primary["native_bundle"].content_hash
    assert observed["ff_profile_content_hash"] == primary["native_profile"].content_hash
    assert observed["fact_refs"] == expected["fact_refs"]
    assert observed["receipt_refs"] == expected["receipt_refs"]
    assert observed["release_view_type"] == "DurableReleaseRefView"
    assert observed["rights_state"] == "HISTORICAL_REPLAY_ONLY__NO_CURRENT_AUTHORITY_MINTED"
    shutil.rmtree(child_cwd)


# ---------------------------------------------------------------------------
# F08 atomic crash/rollback, dedup and resource measures
# ---------------------------------------------------------------------------


def test_f08_atomic_crash_rollback_dedup_resource_measures(tmp_path):
    root = tmp_path / "cas"
    output = _m01_output()["output"]
    first = publish_empirical_closure(output, root)
    second = publish_empirical_closure(output, root)
    assert first.published is True
    assert second.published is False
    assert second.root_identity == first.root_identity
    assert second.cas_new_bytes == 0
    assert first.logical_evidence_bytes > first.referenced_physical_bytes
    assert 0 < first.dedup_ratio < 1
    assert first.fragment_count > 0
    assert first.peak_scratch_bytes > 0
    assert first.manifest_bytes > 0
    assert first.source_open_count == 0
    assert first.rows["native_facts"] >= 4

    # No second complete uncompressed product archive: the manifest carries
    # exact refs/metadata/replay preimages, but no full object document.
    manifest_text = (Path(first.root_path) / "manifest.json").read_text(encoding="utf-8")
    for fact in output.object_graph.empirical_facts:
        assert canonical_json(fact.as_dict()) not in manifest_text
    assert len(list((root / "cas" / "blobs").glob("*.json.z"))) == first.blob_count
    assert not list((root / "cas" / "blobs").glob("*.json"))

    # Crash after blob staging must leave no visible closure and no staging dir.
    crash_output = _k_way_output()
    crash_root = tmp_path / "crash-cas"

    def _fail_after_blob(name: str) -> None:
        if name == "after_blob_write":
            raise RuntimeError("injected crash after blob write")

    with pytest.raises(RuntimeError):
        publish_empirical_closure(
            crash_output, crash_root, failpoint=_fail_after_blob
        )
    assert not list((crash_root / "closures").glob("closure-*"))
    assert not list((crash_root / "closures").glob(".staging-*"))
    assert list((crash_root / "cas" / "blobs").glob("*.json.z"))  # safe reusable CAS blobs

    recovered = publish_empirical_closure(crash_output, crash_root)
    assert recovered.published is True
    assert open_empirical_closure(
        recovered.root_path, expected_root=recovered.root_identity
    ).root_identity == recovered.root_identity

    # Crash immediately before the atomic manifest rename must roll back.
    def _fail_before_manifest(name: str) -> None:
        if name == "before_manifest_replace":
            raise RuntimeError("injected crash before manifest rename")

    rollback_output = _reversal_output()
    rollback_root = tmp_path / "rollback-cas"
    with pytest.raises(RuntimeError):
        publish_empirical_closure(
            rollback_output, rollback_root, failpoint=_fail_before_manifest
        )
    assert not list((rollback_root / "closures").glob("closure-*"))
    assert not list((rollback_root / "closures").glob(".staging-*"))
    recovered = publish_empirical_closure(rollback_output, rollback_root)
    assert recovered.published is True

    # Dead-publisher staging/tmp leftovers are cleaned without touching live
    # publishers or final content-addressed blobs.
    stale_root = tmp_path / "stale-cas"
    (stale_root / "cas" / "blobs").mkdir(parents=True)
    (stale_root / "closures").mkdir(parents=True)
    dead = subprocess.Popen([sys.executable, "-c", "pass"])
    dead.wait()
    stale_stage = stale_root / "closures" / f".staging-{dead.pid}-deadbeef"
    stale_stage.mkdir()
    (stale_stage / "manifest.json").write_text("{}")
    stale_tmp = stale_root / "cas" / "blobs" / f".dead.json.z.tmp-{dead.pid}-deadbeef"
    stale_tmp.write_bytes(b"partial")
    live_tmp = (
        stale_root
        / "cas"
        / "blobs"
        / f".live.json.z.tmp-{os.getpid()}-livebeef"
    )
    live_tmp.write_bytes(b"live-publisher-partial")
    legacy_uuid_tmp = (
        stale_root
        / "cas"
        / "blobs"
        / ".legacy.json.z.tmp-0123456789abcdef0123456789abcdef"
    )
    legacy_uuid_tmp.write_bytes(b"pre-repair-uuid-only-partial")
    publish_empirical_closure(_k_way_output(), stale_root)
    assert not stale_stage.exists()
    assert not stale_tmp.exists()
    # A live publisher's temp must never be deleted by another publisher's
    # cleanup pass.
    assert live_tmp.exists()
    # Legacy UUID-only temp names carry no attributable pid and are deliberately
    # not claimed as cleaned; they remain until an operator chooses to remove
    # them.  This test accounts for that residual honestly.
    assert legacy_uuid_tmp.exists()
    live_tmp.unlink()
    legacy_uuid_tmp.unlink()

    # Cold and repeat read timing plus process-tree RSS at the isolated grade.
    cold_started = time.monotonic()
    cold = open_empirical_closure(
        first.root_path, expected_root=first.root_identity
    ).require_trusted()
    cold_seconds = time.monotonic() - cold_started
    repeat_started = time.monotonic()
    repeat = open_empirical_closure(
        first.root_path, expected_root=first.root_identity
    ).require_trusted()
    repeat_seconds = time.monotonic() - repeat_started
    assert cold.root_identity == repeat.root_identity
    max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        max_rss_bytes = int(max_rss)
    else:
        max_rss_bytes = int(max_rss) * 1024
    cap_bytes = 6 * 1024**3
    assert max_rss_bytes < cap_bytes
    assert cold_seconds >= 0 and repeat_seconds >= 0

    # Keep the measured resource envelope for the handoff/receipt.
    evidence = {
        "rows": dict(first.rows),
        "object_count": first.object_count,
        "fragment_count": first.fragment_count,
        "blob_count": first.blob_count,
        "logical_evidence_bytes": first.logical_evidence_bytes,
        "referenced_physical_bytes": first.referenced_physical_bytes,
        "compressed_fragment_bytes": first.compressed_fragment_bytes,
        "manifest_bytes": first.manifest_bytes,
        "peak_scratch_bytes": first.peak_scratch_bytes,
        "cas_new_bytes": first.cas_new_bytes,
        "dedup_ratio": first.dedup_ratio,
        "source_open_count": first.source_open_count,
        "cold_seconds": cold_seconds,
        "repeat_seconds": repeat_seconds,
        "process_tree_peak_rss_bytes": max_rss_bytes,
        "cap_bytes": cap_bytes,
        "cap_result": "PASS",
        "integrated_100k": "NOT_RUN",
    }
    (tmp_path / "resource_evidence.json").write_text(json.dumps(evidence, sort_keys=True))
    assert json.loads((tmp_path / "resource_evidence.json").read_text())["cap_result"] == "PASS"


def test_f08_hard_crash_blob_temp_lifecycle(tmp_path):
    """Actual child crash between blob temp write and rename must be cleaned.

    The test deliberately exercises the publisher's real temp filename, not a
    handcrafted name: the child opens the real CAS path, writes the real temp,
    and exits before ``os.replace``.  A subsequent normal publish must remove
    the dead publisher's temp and still produce a valid closure.
    """

    crash_root = tmp_path / "crash-cas"
    child = r"""
import os
from rawlsing_next.pre553_durable_empirical_closure import publish_empirical_closure
from rawlsing_next.tests.test_pyat940_s2f_durable_closure import _k_way_output

root = os.environ["S2F_CRASH_ROOT"]
real_replace = os.replace

def crash_on_blob_rename(src, dst):
    if ".json.z.tmp-" in str(src):
        os._exit(77)
    return real_replace(src, dst)

os.replace = crash_on_blob_rename
publish_empirical_closure(_k_way_output(), root)
"""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["S2F_CRASH_ROOT"] = str(crash_root)
    completed = subprocess.run(
        [sys.executable, "-c", child],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert completed.returncode == 77, completed.stderr
    blob_dir = crash_root / "cas" / "blobs"
    tmps = sorted(blob_dir.glob(".*.json.z.tmp-*"))
    assert tmps, "the real publisher emitted no blob temp before the crash"
    suffix = tmps[0].name.rsplit(".tmp-", 1)[1]
    pid_text, separator, _uuid = suffix.partition("-")
    assert separator and pid_text.isdigit(), (
        "publisher blob temp must carry the publisher PID for dead-publisher cleanup"
    )
    assert list((crash_root / "closures").glob(".staging-*"))

    recovered = publish_empirical_closure(_k_way_output(), crash_root)
    assert recovered.published is True
    assert not list(blob_dir.glob(".*.json.z.tmp-*"))
    assert not list((crash_root / "closures").glob(".staging-*"))
    opened = open_empirical_closure(
        recovered.root_path, expected_root=recovered.root_identity
    ).require_trusted()
    assert opened.root_identity == recovered.root_identity


# ---------------------------------------------------------------------------
# F09 S2-E dependency grade separation
# ---------------------------------------------------------------------------


def test_f09_s2e_dependency_grade_separation(tmp_path):
    primary = _fresh_primary(tmp_path)
    closure = open_empirical_closure(
        primary["receipt"].root_path, expected_root=primary["receipt"].root_identity
    )
    core = closure.manifest["core"]
    assert core["evidence_grade"] == EVIDENCE_GRADE == "S2_SOURCEFREE_ISOLATED_FIXTURE"
    assert core["ab_contract"]["incoming_s2e_accepted"] is False
    assert core["ab_contract"]["full_integrated_s2f"] == "HOLD_DEPENDENCY"
    assert core["ab_contract"]["scientific_authority"] == "SEPARATE_OWNER_NOT_MINTED"
    assert core["contract_sha"] == DURABLE_CLOSURE_CONTRACT_SHA
    assert core["source_access_state"] == "DISABLED__NO_ORIGINAL_SOURCE_BYTES_RETAINED"
    assert core["rights_state"] == "HISTORICAL_REPLAY_ONLY__NO_CURRENT_AUTHORITY_MINTED"
    assert closure.trust_state == "EXTERNALLY_PINNED"

    # The closure can be published without incoming S2-E, but it must never
    # claim the integrated S2-F contract.
    assert core["native_result"]["i05"]["contract_id"] == "PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0"
    assert "source-native" not in canonical_json(core).lower()
    assert "original35" not in canonical_json(core).lower()
