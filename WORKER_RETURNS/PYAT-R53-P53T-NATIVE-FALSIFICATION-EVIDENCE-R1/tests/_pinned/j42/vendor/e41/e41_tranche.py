"""E41 tranche engine: execute the frozen workload through the real owners.

Every operation in ``frozen/expected_use_universe.json`` is executed through the
ACCEPTED public owners:

* ``rawlsing_next.pre553_empirical_possibility_provider`` (direct scalar route)
* the E41 versioned extension (multi-conditioner, discovery, recursive routes),
  which delegates to the accepted composition owner
  ``rawlsing_next.pre553_analytical_composition.compose_positioned_subject_possibility``
* the accepted empirical query/discovery/recursive owners via the accepted
  fixture builders for typed-state, replay, invalidation, learned-release and
  source-backed substrate operations.

The engine mints nothing: expected truth comes only from the frozen universe;
actuals come only from accepted-owner executions. The anti-join is computed
from those two sides.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping, Callable

import bootstrap  # noqa: F401

from e41_provider_extension import (
    EXT_ROUTE_DIRECT_MULTI_CONDITIONER,
    EXT_ROUTE_DIRECT_VIA_ACCEPTED_PROVIDER,
    EXT_ROUTE_DISCOVERY,
    EXT_ROUTE_RECURSIVE,
    EmpiricalPossibilitySliceExtensionResult,
    provide_empirical_possibility_slice_ext,
)
import e41_frozen_expectations as frozen

RETURN_DIR = Path(__file__).resolve().parent
ROOT = bootstrap.ROOT
ARTIFACTS_DIR = RETURN_DIR / "artifacts"
EVIDENCE_DIR = RETURN_DIR / "evidence"

from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests import c1_03_join_fixture as join_fx
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests import c1_at14_at16_fixture as states_fx
from rawlsing_next.tests import c1_at18_at19_fixture as replay_fx
from rawlsing_next.tests import n10e_empirical_slice_fixture as n10e
from rawlsing_next.tests import n10e_at17_successor_requal as successor_fx
from rawlsing_next.tests.test_pre553_analytical_composition_higher_order import (
    _attitude_domain,
    _attitude_source_and_authority,
    _ranked_query,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom,
    _d_auth,
    _discovery_authority,
    _execute as _execute_discovery,
    _grammar,
    _qt,
    _rule,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _build_source,
    _coordinate_leaf,
    _predicate,
    _query,
    _query_authority,
    _registry,
    _response_leaf,
    _run,
)
from rawlsing_next.pre553_recursive_handoff import (
    execute_exact_bounded_discovery_with_handoffs,
    recursive_parent_atom,
)


class TrancheError(Exception):
    """Tranche-level failure (not an owner typed refusal)."""


# ---------------------------------------------------------------------------
# normalization helpers
# ---------------------------------------------------------------------------


def _norm_cell_key(cell: Any) -> str:
    if isinstance(cell, (tuple, list)):
        return "|".join(str(part) for part in cell)
    return str(cell)


def norm_result_cells(result) -> tuple[dict[str, list[int]], int]:
    """Normalize accepted composition geometry to {cell: [num, den]}, denominator."""

    denominator = int(result.raw_denominator_support)
    cells: dict[str, list[int]] = {}
    for row in result.complete_cell_geometry:
        key = _norm_cell_key(row["cell"])
        cells[key] = [int(row["raw_numerator_support"]), denominator]
    return cells, denominator


def refs_of(values) -> list[dict[str, Any]]:
    return [value.as_dict() for value in values if value is not None]


# ---------------------------------------------------------------------------
# direct material builder (mirrors the accepted fixture driver but returns the
# extension/owner kwargs instead of executing)
# ---------------------------------------------------------------------------


def direct_material(
    *,
    source,
    qauth,
    registry,
    conditions,
    target_question,
    tag,
    target_domain=None,
):
    from rawlsing_next.tests.c1_at08_at13_fixture import (
        build_witness_for_binding,
        make_conditioner_binding,
        make_multi_conditioner_consumer_query,
        make_model_rule,
        make_pairing_authority,
        subject_fact_ref,
        with_target_domains,
    )

    leaves = []
    for kind, question, value in conditions:
        if kind == "RESPONSE":
            leaves.append(_response_leaf(source, qauth, question, value))
        else:
            leaves.append(_coordinate_leaf(source, question, value))
    if not conditions:
        raise TrancheError(f"direct_material requires at least one condition ({tag})")
    if len(leaves) == 1:
        predicate = _predicate(source, qauth, leaves[0], tag=f"{tag}-predicate")
    else:
        predicate = _predicate(
            source, qauth, {"op": "AND", "children": list(leaves)}, tag=f"{tag}-predicate"
        )
    producer_query = _query(
        source, qauth, predicate, (target_question,), risk="R", measure="RAW", tag=f"{tag}-query"
    )
    if target_domain is not None:
        producer_query = with_target_domains(producer_query, target_domain)

    pairing = make_pairing_authority(tag)
    leaf_types = {
        "RESPONSE": "SURVEY_RESPONSE_EVENT",
        "COORDINATE": "EMPIRICAL_POSITION_COORDINATE",
    }
    if len({leaf_types[kind] for kind, _, _ in conditions}) > 1:
        raise TrancheError("mixed conditioner leaf kinds are not supported here")
    leaf_type = leaf_types[conditions[0][0]]
    bindings = []
    pairs = []
    for index, (kind, question, value) in enumerate(conditions):
        coordinate_ref = source["qrefs"][question] if kind == "RESPONSE" else source["crefs"][question]
        bindings.append(
            make_conditioner_binding(
                binding_id=f"c{index}",
                subject_fact_ref=ExactRef(**subject_fact_ref(source, question, value)),
                empirical_coordinate_ref=coordinate_ref,
                comparability_authority_ref=pairing,
                source_universe_ref=source["universe"].ref,
                release_ref=source["release_ref"],
            )
        )
        pairs.append((coordinate_ref, value))

    consumer_query = make_multi_conditioner_consumer_query(
        query_id=f"{tag}-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            f"urn:test:c1-02:{tag}:subject",
            semantic_hash({"fixture_id": tag}),
        ),
        target_ref=source["qrefs"][target_question],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=bindings,
        projection_kind=f"C1_{tag}_CONDITIONAL_DISTRIBUTION",
    )
    witness = build_witness_for_binding(
        witness_object_id=f"urn:test:c1-02:{tag}:witness",
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=predicate,
        bindings=bindings,
        coordinate_value_pairs=pairs,
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        leaf_type=leaf_type,
    )
    return {
        "repository": source["repo"],
        "empirical_query": producer_query,
        "predicate": predicate,
        "authority_registry": registry,
        "release_refs": (source["release_ref"],),
        "consumer_query": consumer_query,
        "model_rule": make_model_rule(source["universe"].ref, tag),
        "condition_binding_witness": witness,
    }


def _extension_receipt_summary(result: EmpiricalPossibilitySliceExtensionResult) -> dict[str, Any]:
    receipt = result.extension_receipt
    return {
        "extension_contract_id": receipt.extension_contract_id,
        "receipt_hash": receipt.receipt_hash,
        "producer_route": receipt.producer_route,
        "producer_fact_ref": receipt.producer_fact_ref.as_dict(),
        "producer_fact_state": receipt.producer_fact_state,
        "generated_evidence_ref": (
            None if receipt.generated_evidence_ref is None else receipt.generated_evidence_ref.as_dict()
        ),
        "generated_evidence_identity_is_producer_derived": (
            receipt.generated_evidence_identity_is_producer_derived
        ),
        "consumer_result_state": receipt.consumer_result_state,
        "consumer_result_identity_hash": receipt.consumer_result_identity_hash,
        "composed_result_identity_hash": receipt.composed_result_identity_hash,
        "coverage_state": receipt.coverage_state,
        "discovery_receipt_refs": refs_of(receipt.discovery_receipt_refs),
        "discovery_frontier_ref": (
            None
            if receipt.discovery_frontier_ref is None
            else receipt.discovery_frontier_ref.as_dict()
        ),
        "recursive_handoff_refs": refs_of(receipt.recursive_handoff_refs),
        "recursive_lineage_refs": refs_of(receipt.recursive_lineage_refs),
        "base_receipt_ref_or_null": receipt.base_receipt_ref_or_null.as_dict()
        if receipt.base_receipt_ref_or_null is not None
        else None,
    }


def _run_extension(material: Mapping[str, Any]) -> EmpiricalPossibilitySliceExtensionResult:
    return provide_empirical_possibility_slice_ext(**material)


# ---------------------------------------------------------------------------
# operation runners
# ---------------------------------------------------------------------------


def run_at07(op_id: str, direction: str) -> dict[str, Any]:
    case = n10e.build_provider_case(direction)
    material = {
        "repository": case["source"]["repo"],
        "empirical_query": case["empirical_query"],
        "predicate": case["predicate"],
        "authority_registry": case["registry"],
        "release_refs": case["release_refs"],
        "consumer_query": case["consumer_query"],
        "model_rule": case["model_rule"],
        "condition_binding_witness": case["condition_binding_witness"],
    }
    result = _run_extension(material)
    cells, denominator = norm_result_cells(result.composition_result)
    return {
        "route_actual": result.producer_route,
        "actual_state": result.consumer_result_or_null.result_state
        if result.consumer_result_or_null is not None
        else result.provider_state,
        "actual_cells": cells,
        "actual_denominator": denominator,
        "receipt": _extension_receipt_summary(result),
    }


def run_direct(op_id: str, source, conditions, target, tag: str, *, target_domain=None) -> dict[str, Any]:
    qauth = _query_authority(tag)
    registry = _registry(source, qauth)
    material = direct_material(
        source=source, qauth=qauth, registry=registry, conditions=conditions,
        target_question=target, tag=tag, target_domain=target_domain,
    )
    result = _run_extension(material)
    cells, denominator = norm_result_cells(result.composition_result)
    return {
        "route_actual": result.producer_route,
        "actual_state": result.consumer_result_or_null.result_state
        if result.consumer_result_or_null is not None
        else result.provider_state,
        "actual_cells": cells,
        "actual_denominator": denominator,
        "receipt": _extension_receipt_summary(result),
    }


def run_at10_discovery(op_id: str) -> dict[str, Any]:
    source = _build_source(
        "c1-at10",
        [
            {"id": "R1", "responses": {"X": 1, "Y": 1}},
            {"id": "R2", "responses": {"X": 1, "Y": 1}},
            {"id": "R3", "responses": {"X": 0, "Y": 0}},
            {"id": "R4", "responses": {"X": 0, "Y": 0}},
        ],
    )
    qauth = _query_authority("c1-at10")
    dauth = _d_auth("c1-at10-discovery")
    pairing = fx.make_pairing_authority("at10")
    registry = _registry(source, qauth, dauth)
    all_p = _branch_predicate(source, qauth, tag="c1-at10-all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="c1-at10-x1")
    yq = _query(source, qauth, all_p, ("Y",), tag="c1-at10-y")
    grammar = _grammar(
        operation="I03-OP-c1-at10-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="ALL", query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
    )
    discovery = _execute_discovery(
        source, qauth, dauth, grammar, (all_p, x1), (yq,),
        authority=_discovery_authority(source, grammar, dauth, tag="at10"),
    )
    receipt = discovery.receipts[0]
    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "urn:test:c1-02:at10:subject",
        semantic_hash({"fixture_id": "AT10"}),
    )
    binding = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="c1-at10-consumer",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT10_DISCOVERY_ROUTE_CONDITIONAL_DISTRIBUTION",
    )
    pred_by_ref = {p.ref: p for p in discovery.executed_predicates}
    query_by_ref = {q.ref: q for q in discovery.executed_queries}
    fact_by_ref = {f.ref: f for f in discovery.empirical_facts}
    produced_predicate = pred_by_ref[ExactRef(**receipt.winning_predicate_ref)]
    produced_fact = fact_by_ref[ExactRef(**receipt.empirical_fact_refs[0])]
    produced_query = query_by_ref[ExactRef(**produced_fact.empirical_query_spec_ref)]
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at10:witness",
        consumer_query=consumer_query,
        producer_query=produced_query,
        producer_predicate=produced_predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    material = {
        "repository": source["repo"],
        "empirical_query": produced_query,
        "predicate": produced_predicate,
        "authority_registry": registry,
        "release_refs": (source["release_ref"],),
        "consumer_query": consumer_query,
        "model_rule": fx.make_model_rule(source["universe"].ref, "at10"),
        "condition_binding_witness": witness,
        "discovery_result": discovery,
        "discovery_receipt_ref": receipt.ref,
    }
    result = _run_extension(material)
    cells, denominator = norm_result_cells(result.composition_result)
    return {
        "route_actual": result.producer_route,
        "actual_state": receipt.typed_state,
        "actual_cells": cells,
        "actual_denominator": denominator,
        "receipt": _extension_receipt_summary(result),
    }


def run_at11_recursive(op_id: str) -> dict[str, Any]:
    source = _build_source(
        "c1-at11-depth2",
        [
            {"id": "R1", "responses": {"X": 1, "H": 1, "Y": 1}},
            {"id": "R2", "responses": {"X": 1, "H": 1, "Y": 0}},
            {"id": "R3", "responses": {"X": 1, "H": 0, "Y": 1}},
            {"id": "R4", "responses": {"X": 1, "H": 0, "Y": 0}},
            {"id": "R5", "responses": {"X": 0, "H": 1, "Y": 1}},
            {"id": "R6", "responses": {"X": 0, "H": 0, "Y": 0}},
        ],
    )
    qauth = _query_authority("c1-at11-depth2")
    from rawlsing_next.tests.test_pre553_analytical_composition_higher_order import (
        _recursive_generation,
    )

    parent = _branch_predicate(source, qauth, tag="gen1-parent")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="depth2-x1")
    h1_leaf = _predicate(source, qauth, _response_leaf(source, qauth, "H", 1), tag="depth2-h1")
    gen1_query = _query(source, qauth, parent, ("X",), tag="depth2-gen1-query")
    gen1, registry1 = _recursive_generation(
        source, qauth, _atom("PARENT", parent, "BRANCH"), parent,
        x1, "RESPONSE", gen1_query, tag="depth2gen1", operation="I03-OP-depth2gen1",
    )
    handoff1 = gen1.handoffs[0]
    child_atom = recursive_parent_atom(handoff1, "CHILD")
    gen2_query = _query(source, qauth, handoff1.winning_predicate, ("H",), tag="depth2-gen2-query")
    gen2, registry2 = _recursive_generation(
        source, qauth, child_atom, handoff1.winning_predicate,
        h1_leaf, "RESPONSE", gen2_query, tag="depth2gen2", operation="I03-OP-depth2gen2",
    )
    handoff2 = gen2.handoffs[0]
    depth2_query = _query(source, qauth, handoff2.winning_predicate, ("Y",), tag="depth2-consume")
    pairing = fx.make_pairing_authority("at11-depth2")
    binding = fx.make_conditioner_binding(
        binding_id="h",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "H", 1)),
        empirical_coordinate_ref=source["qrefs"]["H"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="at11-depth2-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1", "urn:test:c1-02:at11-depth2",
            semantic_hash({"fixture_id": "AT11-D2"}),
        ),
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT11_DEPTH_TWO_CONDITIONAL_DISTRIBUTION",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at11-depth2:witness",
        consumer_query=consumer_query,
        producer_query=depth2_query,
        producer_predicate=handoff2.winning_predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["H"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    material = {
        "repository": source["repo"],
        "empirical_query": depth2_query,
        "predicate": handoff2.winning_predicate,
        "authority_registry": registry2,
        "release_refs": (source["release_ref"],),
        "consumer_query": consumer_query,
        "model_rule": fx.make_model_rule(source["universe"].ref, "at11-depth2"),
        "condition_binding_witness": witness,
        "recursive_handoff": handoff2,
    }
    result = _run_extension(material)
    cells, denominator = norm_result_cells(result.composition_result)
    receipt = _extension_receipt_summary(result)
    receipt["recursive_generation_one_ref"] = handoff1.ref.as_dict()
    receipt["cohort1_members"] = 4
    receipt["cohort2_members"] = 2
    return {
        "route_actual": result.producer_route,
        "actual_state": result.consumer_result_or_null.result_state
        if result.consumer_result_or_null is not None
        else result.provider_state,
        "actual_cells": cells,
        "actual_denominator": denominator,
        "receipt": receipt,
    }


def run_ranked(op_id: str, *, reverse: bool) -> dict[str, Any]:
    tag = "c1-at13-reordered-flipped" if reverse else "c1-at13-ranked-modal"
    source = fx.ranked_fixture(tag, reverse_rank=reverse)
    qauth = _query_authority(tag)
    registry = _registry(source, qauth)
    predicate = _predicate(source, qauth, _response_leaf(source, qauth, "ATT", "1"), tag=f"{tag}-p")
    producer_query = _ranked_query(source, qauth, predicate, topology="RANKED_RESPONSE", tag=f"{tag}-producer")
    pairing = fx.make_pairing_authority(tag)
    binding = fx.make_conditioner_binding(
        binding_id="att",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "ATT", "1")),
        empirical_coordinate_ref=source["qrefs"]["ATT"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id=f"{tag}-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1", f"urn:test:c1-02:{tag}",
            semantic_hash({"fixture_id": tag}),
        ),
        target_ref=source["qrefs"]["RANK"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind=f"C1_{tag.upper()}_NONSCALAR_COMPONENT_VECTOR",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id=f"urn:test:c1-02:{tag}:witness",
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["ATT"], "1")],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    material = {
        "repository": source["repo"],
        "empirical_query": producer_query,
        "predicate": predicate,
        "authority_registry": registry,
        "release_refs": (source["release_ref"],),
        "consumer_query": consumer_query,
        "model_rule": fx.make_model_rule(source["universe"].ref, tag),
        "condition_binding_witness": witness,
    }
    result = _run_extension(material)
    cells, denominator = norm_result_cells(result.composition_result)
    return {
        "route_actual": result.producer_route,
        "actual_state": result.consumer_result_or_null.result_state
        if result.consumer_result_or_null is not None
        else result.provider_state,
        "actual_cells": cells,
        "actual_denominator": denominator,
        "receipt": _extension_receipt_summary(result),
    }


def run_typed_state(op_id: str, fixture_name: str, kind: str) -> dict[str, Any]:
    if kind == "empirical":
        projection, data = states_fx.project_empirical(fixture_name)
    elif kind == "receipt":
        projection, data = states_fx.project_receipt(fixture_name)
    elif kind == "adaptive":
        projection, data = states_fx.project_adaptive(fixture_name)
    elif kind == "integrity":
        projection, data = states_fx.project_empirical_integrity_refusal(fixture_name)
    elif kind == "blocked":
        projection, data = states_fx.project_blocked_authority_refusal(fixture_name)
    else:
        raise TrancheError(f"unknown typed-state kind {kind!r}")
    actual_state = data.get("producer_state") or getattr(projection, "state", None)
    return {
        "route_actual": "OWNER_TYPED_STATE",
        "actual_state": actual_state,
        "actual_cells": {},
        "actual_denominator": data.get("raw_denominator_support"),
        "receipt": {
            "owner": data.get("owner"),
            "reason": data.get("reason"),
            "coverage_state": data.get("coverage_state"),
            "projection_state": getattr(projection, "state", None),
        },
    }


def run_at17(op_id: str, direction: str) -> dict[str, Any]:
    case = n10e.build_provider_case(direction)
    material = {
        "repository": case["source"]["repo"],
        "empirical_query": case["empirical_query"],
        "predicate": case["predicate"],
        "authority_registry": case["registry"],
        "release_refs": case["release_refs"],
        "consumer_query": case["consumer_query"],
        "model_rule": case["model_rule"],
        "condition_binding_witness": case["condition_binding_witness"],
    }
    result = _run_extension(material)
    digest = result.composition_result.composed_result_identity_hash
    expected = frozen.AT17_ADOPTED_SUCCESSOR[direction]
    return {
        "route_actual": result.producer_route,
        "actual_state": "EXACT_SUPPORTED" if digest == expected else "SUCCESSOR_IDENTITY_DRIFT",
        "actual_cells": {"successor_identity_digest": digest},
        "actual_denominator": int(result.composition_result.raw_denominator_support),
        "receipt": _extension_receipt_summary(result),
    }


def run_at18(op_id: str) -> dict[str, Any]:
    case = n10e.build_provider_case("forward")
    material = {
        "repository": case["source"]["repo"],
        "empirical_query": case["empirical_query"],
        "predicate": case["predicate"],
        "authority_registry": case["registry"],
        "release_refs": case["release_refs"],
        "consumer_query": case["consumer_query"],
        "model_rule": case["model_rule"],
        "condition_binding_witness": case["condition_binding_witness"],
    }
    in_process = _run_extension(material)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "rawlsing_next.tests.n10e_empirical_slice_fresh_process_runner",
            "forward",
        ],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=900,
    )
    if completed.returncode != 0:
        raise TrancheError(f"fresh-process replay runner failed: {completed.stderr[-800:]}")
    fresh = json.loads(completed.stdout)
    base_result = in_process.base_result_or_null
    if base_result is None:
        raise TrancheError("at18 requires the direct provider delegation base result")
    identical = (
        fresh["result_identity_hash"] == base_result.result_identity_hash
        and fresh["composed_result_identity_hash"]
        == in_process.composition_result.composed_result_identity_hash
        and fresh["receipt_ref_hash"] == base_result.provider_receipt.receipt_ref.content_hash
    )
    return {
        "route_actual": in_process.producer_route,
        "actual_state": "IDENTICAL_IDENTITY_ON_REPLAY" if identical else "REPLAY_IDENTITY_MISMATCH",
        "actual_cells": {
            "identity_relation": "EQUAL" if identical else "DIFFER",
            "fresh_process_identity": fresh["result_identity_hash"],
            "in_process_accepted_provider_identity": base_result.result_identity_hash,
        },
        "actual_denominator": int(in_process.composition_result.raw_denominator_support),
        "receipt": {
            **_extension_receipt_summary(in_process),
            "fresh_process": {
                "result_identity_hash": fresh["result_identity_hash"],
                "composed_result_identity_hash": fresh["composed_result_identity_hash"],
                "raw_denominator_support": fresh["raw_denominator_support"],
                "cell_numerators": fresh["cell_numerators"],
            },
        },
    }


def run_at19(op_id: str) -> dict[str, Any]:
    deps = join_fx.real_accepted_dependents()
    ctx = join_fx.join_transition(deps)
    seal = join_fx.join_seal(ctx["executor"], ctx["old_snapshot"])
    release = ctx["executor"].promote_current(
        seal,
        selection_rule_ref=ExactRef("JOIN_RULE@1", "urn:c1-03-join:at19:rule", "f" * 64),
        selection_attestation_ref=ExactRef("JOIN_ATT@1", "urn:c1-03-join:at19:att", "1" * 64),
        recompiler=join_fx.join_recompiler(deps, "at19"),
        noncurrent_outcomes=ctx["declarations"],
    )
    receipt = ctx["executor"].invalidation_receipt_for_release(release.ref)
    affected = {r.key for r in receipt.affected_dependent_refs}
    unaffected = {r.key for r in receipt.unaffected_dependent_refs}
    known = {d.key for d in deps.values()}
    partition_ok = affected.isdisjoint(unaffected) and (affected | unaffected) == known
    return {
        "route_actual": "OWNER_LIFECYCLE_TRANSITION",
        "actual_state": (
            "ONLY_GRAPH_DECLARED_DEPENDENTS_AFFECTED" if partition_ok else "DEPENDENT_PARTITION_BROKEN"
        ),
        "actual_cells": {
            "declared_dependents": str(len(known)),
            "affected": str(len(affected)),
            "unaffected": str(len(unaffected)),
            "sibling_unaffected": str(deps["sibling"].key in unaffected),
        },
        "actual_denominator": None,
        "receipt": {
            "release_ref": release.ref.as_dict(),
            "selection_rule_ref": receipt.selection_rule_ref.as_dict()
            if hasattr(receipt, "selection_rule_ref")
            else None,
        },
    }


def run_learned_chain(op_id: str) -> dict[str, Any]:
    from rawlsing_next import pre553_learned_world_composition as i4
    from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleExecutor
    from rawlsing_next.pre553_learned_product_release import M2Repository
    from rawlsing_next.tests import test_pre553_learned_world_composition as lw

    auth = lw._m1_authority("i4-full")
    fixture = lw.m01_fixture()
    m01_result = lw.execute_m01(fixture)
    binding = lw._binding(auth)
    contract = lw._contract(
        route="M01_M1_M2_B5",
        binding=binding,
        actions=("REGISTER", "PUBLISH", "SELECT_CURRENT"),
        tag="full",
    )
    result = i4.compose_learned_world(
        contract,
        m2_repository=M2Repository(),
        lifecycle_executor=LearnedProductLifecycleExecutor(),
        m01_result=m01_result,
        selected_discovery_receipt_refs=tuple(r.ref for r in m01_result.i05_result.receipts),
        requested_scope={"fixture": "I4_FULL_SYNTHETIC"},
        m1_family_rule_binding=binding,
        validator_registry=lw._registry(binding),
        m1_authority_snapshots=(auth,),
    )
    state = result.receipt.terminal_state
    return {
        "route_actual": "M01_M1_M2_B5_I4_COMPOSITION",
        "actual_state": state,
        "actual_cells": {
            "b5_registration": str(result.receipt.side_effects["b5_registration_effect"]),
            "b5_publication": str(result.receipt.side_effects["b5_publication_effect"]),
            "b5_current_selection": str(result.receipt.side_effects["b5_current_selection_effect"]),
        },
        "actual_denominator": None,
        "receipt": {
            "terminal_state": state,
            "m01_execution_receipt_ref": result.receipt.m01_execution_receipt_ref.as_dict()
            if result.receipt.m01_execution_receipt_ref is not None
            else None,
            "b5_replay_state": result.b5_replay_receipt.replay_state
            if result.b5_replay_receipt is not None
            else None,
        },
    }


def run_sourcebacked(op_id: str) -> dict[str, Any]:
    from rawlsing_next.pre553_source_backed_c11_facade import (
        build_validated_source_backed_c11_release_from_stream,
    )
    from rawlsing_next.tests import test_pre553_source_backed_c11_facade_multi_owner_r1 as sb

    built = sb._fixture(dual_owner=True, explicit_owner_set=True)
    projection = built["projection"]
    first = build_validated_source_backed_c11_release_from_stream(built["stream"], projection)
    second = build_validated_source_backed_c11_release_from_stream(built["stream"], projection)
    parity = first.release_ref == second.release_ref and tuple(
        x.ref for x in first.public_objects
    ) == tuple(x.ref for x in second.public_objects)
    return {
        "route_actual": "PHYSICAL_STREAM_TO_C11_TO_I03",
        "actual_state": "SUPPORTED" if parity else "REPLAY_PARITY_BROKEN",
        "actual_cells": {
            "public_objects": str(len(first.public_objects)),
            "release_replays_identically": str(parity),
        },
        "actual_denominator": len(first.public_objects),
        "receipt": {
            "release_ref": first.release_ref.as_dict(),
            "replay_manifest_ref": first.replay_manifest.ref.as_dict(),
        },
    }


def run_e04_consumption(op_id: str) -> dict[str, Any]:
    from e41_e04_service import drive_original_e04_client

    driven = drive_original_e04_client()
    receipt = driven["receipt"]["material"]
    return {
        "route_actual": "POSITIONED_SERVICE_TO_NONPARENT_OPTIONS",
        "actual_state": receipt["state"],
        "actual_cells": {
            "route_probability_is_null": str(receipt["route_probability"] is None),
            "values_read_count": str(len(driven["value_reads"])),
            "empirical_state": receipt["empirical"]["state"],
        },
        "actual_denominator": None,
        "receipt": {
            "consumer": "NONPARENT_OPTIONS",
            "consumer_receipt_hash": driven["receipt"]["receipt_hash"],
            "snapshot_ref": driven["snapshot_ref"],
            "step_states": [step["state"] for step in receipt["empirical"]["steps"]],
            "step_evidence_refs": [
                step.get("evidence_ref") for step in receipt["empirical"]["steps"]
            ],
            "service_contract": receipt["service_contract"],
        },
    }


# ---------------------------------------------------------------------------
# runner registry (op_id -> callable)
# ---------------------------------------------------------------------------


def _state_runners() -> dict[str, Callable[[], dict[str, Any]]]:
    return {
        "state.observed_zero": lambda: run_typed_state("state.observed_zero", "observed_zero_fixture", "empirical"),
        "state.zero_support": lambda: run_typed_state("state.zero_support", "zero_support_fixture", "empirical"),
        "state.valid_empty": lambda: run_typed_state("state.valid_empty", "valid_empty_fixture", "empirical"),
        "state.underpowered": lambda: run_typed_state("state.underpowered", "underpowered_fixture", "receipt"),
        "state.unresolved": lambda: run_typed_state("state.unresolved", "unresolved_fixture", "empirical"),
        "state.noncomparable": lambda: run_typed_state("state.noncomparable", "noncomparable_fixture", "empirical"),
        "state.integrity_failure": lambda: run_typed_state("state.integrity_failure", "integrity_failure_fixture", "integrity"),
        "state.adaptive_unvisited": lambda: run_typed_state("state.adaptive_unvisited", "unvisited_adaptive_fixture", "adaptive"),
        "state.blocked_required_authority": lambda: run_typed_state("state.blocked_required_authority", "blocked_required_authority_fixture", "blocked"),
    }


def runner_registry() -> dict[str, Callable[[], dict[str, Any]]]:
    registry: dict[str, Callable[[], dict[str, Any]]] = {
        "f2.at07.forward": lambda: run_at07("f2.at07.forward", "forward"),
        "f2.at07.reverse": lambda: run_at07("f2.at07.reverse", "reverse"),
        "f2.at08.agree_to_att2": lambda: run_direct(
            "f2.at08.agree_to_att2",
            _attitude_source_and_authority("at08")[0],
            [("RESPONSE", "ATT1", "agree")], "ATT2", "at08-agree",
            target_domain=_attitude_domain(),
        ),
        "f2.at08.disagree_to_att2": lambda: run_direct(
            "f2.at08.disagree_to_att2",
            _attitude_source_and_authority("at08b")[0],
            [("RESPONSE", "ATT1", "disagree")], "ATT2", "at08-disagree",
            target_domain=_attitude_domain(),
        ),
        "f4.at09.xor_joint": lambda: run_direct(
            "f4.at09.xor_joint", fx.xor_fixture(),
            [("RESPONSE", "A", 1), ("RESPONSE", "B", 0)], "C", "at09-joint",
        ),
        "f4.at09.equal_marginals_left": lambda: run_direct(
            "f4.at09.equal_marginals_left", fx.equal_marginals_fixtures()[0],
            [("RESPONSE", "A", 1)], "B", "at09-left",
        ),
        "f4.at09.equal_marginals_right": lambda: run_direct(
            "f4.at09.equal_marginals_right", fx.equal_marginals_fixtures()[1],
            [("RESPONSE", "A", 1)], "B", "at09-right",
        ),
        "f3.at10.branch_A": lambda: run_direct(
            "f3.at10.branch_A", fx.minority_fixture(),
            [("COORDINATE", "G", "A")], "Y", "at10-comp-A",
        ),
        "f3.at10.branch_B": lambda: run_direct(
            "f3.at10.branch_B", fx.minority_fixture(),
            [("COORDINATE", "G", "B")], "Y", "at10-comp-B",
        ),
        "f3.at10.branch_C": lambda: run_direct(
            "f3.at10.branch_C", fx.minority_fixture(),
            [("COORDINATE", "G", "C")], "Y", "at10-comp-C",
        ),
        "f3.at10.discovery_cotravel": lambda: run_at10_discovery("f3.at10.discovery_cotravel"),
        "f3.at11.recursive_depth2": lambda: run_at11_recursive("f3.at11.recursive_depth2"),
        "f4.at12.cotravel_cloud": lambda: run_direct(
            "f4.at12.cotravel_cloud", fx.cotravel_fixture(),
            [("RESPONSE", "X", 1)], "Y", "at12-cotravel",
        ),
        "f4.at13.ranked_modal": lambda: run_ranked("f4.at13.ranked_modal", reverse=False),
        "f4.at13.ranked_reidentified": lambda: run_ranked("f4.at13.ranked_reidentified", reverse=True),
        "replay.at17.successor_forward": lambda: run_at17("replay.at17.successor_forward", "forward"),
        "replay.at17.successor_reverse": lambda: run_at17("replay.at17.successor_reverse", "reverse"),
        "replay.at18.fresh_process": lambda: run_at18("replay.at18.fresh_process"),
        "replay.at19.selective_invalidation": lambda: run_at19("replay.at19.selective_invalidation"),
        "learned.full_chain_composition": lambda: run_learned_chain("learned.full_chain_composition"),
        "sourcebacked.stream_query": lambda: run_sourcebacked("sourcebacked.stream_query"),
        "e04.nonparent_consumption": lambda: run_e04_consumption("e04.nonparent_consumption"),
    }
    registry.update(_state_runners())
    return registry


# ---------------------------------------------------------------------------
# tranche execution + anti-join
# ---------------------------------------------------------------------------


def _expected_form(op: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "expected_state": op["expected_producer_or_consumer_state"],
        "expected_cells": op["expected_cells"],
        "expected_denominator": op["expected_denominator"],
    }


def _compare(op: Mapping[str, Any], actual: Mapping[str, Any]) -> dict[str, Any]:
    expected = _expected_form(op)
    diffs: list[str] = []
    exp_cells = expected["expected_cells"] or {}
    act_cells = actual.get("actual_cells") or {}
    if exp_cells:
        for key, value in exp_cells.items():
            if key not in act_cells:
                diffs.append(f"missing_cell:{key}")
                continue
            if act_cells[key] != value:
                diffs.append(f"cell_mismatch:{key}:expected={value}:actual={act_cells[key]}")
        extra = [key for key in act_cells if key not in exp_cells]
        identity_only = all(
            key.startswith("successor_identity_digest") or key == "identity_relation"
            for key in exp_cells
        )
        if extra and not identity_only:
            diffs.append(f"extra_cells={extra}")
    if expected["expected_denominator"] is not None and actual.get("actual_denominator") is not None:
        if int(expected["expected_denominator"]) != int(actual["actual_denominator"]):
            diffs.append(
                f"denominator_mismatch:expected={expected['expected_denominator']}:"
                f"actual={actual['actual_denominator']}"
            )
    state_ok = None
    if expected["expected_state"]:
        state_ok = actual.get("actual_state") == expected["expected_state"]
        if state_ok is False:
            diffs.append(
                f"state_mismatch:expected={expected['expected_state']}:actual={actual.get('actual_state')}"
            )
    return {"diffs": diffs, "matched": not diffs, "state_ok": state_ok}


def run_tranche(*, workload_ops: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Execute a workload against the frozen expected universe.

    ``workload_ops`` is the actually submitted workload (defaults to the frozen
    universe). ``expected_ids`` always comes from the independently frozen
    universe, so dropping an eligible operation from the submitted workload is
    detected as a dropped operation — never silently re-scoped.
    """

    universe = frozen.load_universe()
    expected_ops = universe["operations"]
    ops = expected_ops if workload_ops is None else workload_ops
    runners = runner_registry()
    expected_ids = [op["op_id"] for op in expected_ops]
    expected_id_set = set(expected_ids)
    results: list[dict[str, Any]] = []
    executed_ids: set[str] = set()

    for op in ops:
        op_id = op["op_id"]
        runner = runners.get(op_id)
        if runner is None:
            results.append({
                "op_id": op_id,
                "family_id": op["family_id"],
                "gate": op["gate"],
                "grade": op["grade"],
                "status": "NO_RUNNER",
                **_expected_form(op),
                "actual": None,
                "comparison": {"diffs": ["no_runner_registered"], "matched": False, "state_ok": False},
            })
            continue
        executed_ids.add(op_id)
        try:
            actual = runner()
            status = "EXECUTED"
        except Exception as exc:  # owner typed refusals are data, not engine crashes
            actual = {
                "route_actual": "OWNER_REFUSAL",
                "actual_state": f"ERROR:{type(exc).__name__}",
                "actual_cells": {},
                "actual_denominator": None,
                "receipt": {"error": str(exc)[:600]},
            }
            status = "OWNER_TYPED_REFUSAL"
        comparison = _compare(op, actual)
        results.append({
            "op_id": op_id,
            "family_id": op["family_id"],
            "gate": op["gate"],
            "grade": op["grade"],
            "status": status,
            **_expected_form(op),
            "actual": actual,
            "comparison": comparison,
        })

    dropped = [op_id for op_id in expected_ids if op_id not in executed_ids]
    unexpected = sorted(executed_ids - expected_id_set)
    mismatched = [
        row["op_id"]
        for row in results
        if row["op_id"] in expected_id_set and not row["comparison"]["matched"]
    ]
    return {
        "schema": "E41_TRANCHE_REPORT@1",
        "frozen_universe_sha256": hashlib.sha256(
            frozen.canonical_json(universe).encode("utf-8")
        ).hexdigest(),
        "expected_operation_count": len(expected_ids),
        "executed_operation_count": len(executed_ids),
        "dropped_operations": dropped,
        "unexpected_operations": unexpected,
        "mismatched_operations": mismatched,
        "no_drop_ok": not dropped and not unexpected,
        "all_expected_reached": not mismatched,
        "results": results,
    }


# ---------------------------------------------------------------------------
# artifact emission
# ---------------------------------------------------------------------------


#: Original-estate cells that remain HELD (not occupied, not refusals-as-completion).
#: Facts transcribed from the R41 flight intake and the O35B return at
#: c714af26a5a749706c6da06df40ac0ef026c6296 (kept count-only; no original read).
HELD_ORIGINAL_SCOPE = {
    "original35_u_epre_state": "UNISSUED_HELD",
    "authorized_original_reads_this_pass": 0,
    "lits_original_c11_blocker": {
        "state": "BLOCKED",
        "missing": "all 15 native C11 SourceReleaseCandidate sections including respondent internal records/events/routing/manifest",
        "source_release_ref": "LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669",
        "semantic_hash": "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f",
        "custodian_request": "WORKER_RETURNS/PYAT-R40-O35B-ORIGINAL35-AUTHORITY-OPERATION-BINDING-R1/evidence/C11_REPLAY_CUSTODIAN_DELIVERY_REQUEST.json",
        "o35b_commit": "c714af26a5a749706c6da06df40ac0ef026c6296",
    },
    "o35b_accounting": {
        "p2_active": 18276,
        "o35e_active": 18259,
        "overlap": 18250,
        "p2_only": 26,
        "p2_only_carrier_admin": 6,
        "p2_only_substantive": 20,
        "o35e_only": 9,
        "candidate_units_held": 127813,
        "lits_checkpoint_bytes": 3404445161,
        "original_facts_recovered": 3,
    },
    "law": "held_original_scope is NOT counted as completion and NOT reported as refusal; "
    "it remains a finite issuer/custodian obligation outside this campaign's rights",
}


def _write_json(path: Path, payload: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def emit_artifacts(report: Mapping[str, Any]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    rows = report["results"]

    hashes["f1f4_coverage_ledger.json"] = _write_json(
        ARTIFACTS_DIR / "f1f4_coverage_ledger.json",
        {
            "schema": "E41_F1F4_COVERAGE_LEDGER@1",
            "frozen_universe_sha256": report["frozen_universe_sha256"],
            "expected_operation_count": report["expected_operation_count"],
            "executed_operation_count": report["executed_operation_count"],
            "no_drop_ok": report["no_drop_ok"],
            "all_expected_reached": report["all_expected_reached"],
            "grades_present": sorted({row["grade"] for row in rows}),
            "original_source_occupied_count": 0,
            "held_original_scope": HELD_ORIGINAL_SCOPE,
            "rows": [
                {
                    "op_id": row["op_id"],
                    "family_id": row["family_id"],
                    "gate": row["gate"],
                    "grade": row["grade"],
                    "status": row["status"],
                    "route_actual": (row["actual"] or {}).get("route_actual"),
                    "expected_state": row["expected_state"],
                    "actual_state": (row["actual"] or {}).get("actual_state"),
                    "expected_denominator": row["expected_denominator"],
                    "actual_denominator": (row["actual"] or {}).get("actual_denominator"),
                    "expected_cells": row["expected_cells"],
                    "actual_cells": (row["actual"] or {}).get("actual_cells"),
                    "matched": row["comparison"]["matched"],
                    "diffs": row["comparison"]["diffs"],
                }
                for row in rows
            ],
        },
    )

    by_gate: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_gate.setdefault(row["gate"], []).append(row)

    def gate_payload(gate: str, schema: str) -> dict[str, Any]:
        gate_rows = by_gate.get(gate, [])
        return {
            "schema": schema,
            "gate": gate,
            "operation_count": len(gate_rows),
            "matched_count": sum(1 for row in gate_rows if row["comparison"]["matched"]),
            "rows": [
                {
                    "op_id": row["op_id"],
                    "family_id": row["family_id"],
                    "actual_cells": (row["actual"] or {}).get("actual_cells"),
                    "actual_denominator": (row["actual"] or {}).get("actual_denominator"),
                    "actual_state": (row["actual"] or {}).get("actual_state"),
                    "matched": row["comparison"]["matched"],
                }
                for row in gate_rows
            ],
        }

    hashes["f2_predictor_surface.json"] = _write_json(
        ARTIFACTS_DIR / "f2_predictor_surface.json",
        gate_payload("F2", "E41_F2_PREDICTOR_SURFACE@1"),
    )
    hashes["f3_branch_alternatives.json"] = _write_json(
        ARTIFACTS_DIR / "f3_branch_alternatives.json",
        gate_payload("F3", "E41_F3_BRANCH_ALTERNATIVES@1"),
    )
    hashes["f4_cloud_joint.json"] = _write_json(
        ARTIFACTS_DIR / "f4_cloud_joint.json",
        gate_payload("F4", "E41_F4_CLOUD_JOINT@1"),
    )

    computed_slices = []
    consumer_receipts = []
    for row in rows:
        actual = row["actual"] or {}
        receipt = actual.get("receipt") or {}
        if receipt.get("generated_evidence_ref") is not None or actual.get("route_actual") in {
            EXT_ROUTE_DIRECT_VIA_ACCEPTED_PROVIDER,
            EXT_ROUTE_DIRECT_MULTI_CONDITIONER,
            EXT_ROUTE_DISCOVERY,
            EXT_ROUTE_RECURSIVE,
        }:
            computed_slices.append({
                "op_id": row["op_id"],
                "route": actual.get("route_actual"),
                "producer_fact_state": receipt.get("producer_fact_state"),
                "generated_evidence_ref": receipt.get("generated_evidence_ref"),
                "composed_result_identity_hash": receipt.get("composed_result_identity_hash"),
                "coverage_state": receipt.get("coverage_state"),
                "consumer_result_state": receipt.get("consumer_result_state"),
            })
            consumer_receipts.append({
                "op_id": row["op_id"],
                "consumer_result_state": receipt.get("consumer_result_state"),
                "consumer_result_identity_hash": receipt.get("consumer_result_identity_hash"),
                "extension_receipt_hash": receipt.get("receipt_hash"),
            })
    hashes["computed_slice_evidence.json"] = _write_json(
        ARTIFACTS_DIR / "computed_slice_evidence.json",
        {
            "schema": "E41_COMPUTED_SLICE_EVIDENCE@1",
            "derivation_law": "producer-derived only; no caller-supplied fixture probabilities",
            "slice_count": len(computed_slices),
            "slices": computed_slices,
        },
    )
    hashes["slice_consumer_receipt.json"] = _write_json(
        ARTIFACTS_DIR / "slice_consumer_receipt.json",
        {
            "schema": "E41_SLICE_CONSUMER_RECEIPT@1",
            "consumer_count": len(consumer_receipts),
            "consumers": consumer_receipts,
        },
    )
    hashes["anti_join_expected_actual.json"] = _write_json(
        ARTIFACTS_DIR / "anti_join_expected_actual.json",
        {
            "schema": "E41_ANTI_JOIN_REPORT@1",
            "frozen_universe_sha256": report["frozen_universe_sha256"],
            "expected_not_actual": report["dropped_operations"],
            "actual_not_expected": report["unexpected_operations"],
            "mismatched": report["mismatched_operations"],
            "no_drop_ok": report["no_drop_ok"],
        },
    )
    return hashes


def main() -> int:
    report = run_tranche()
    hashes = emit_artifacts(report)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    (EVIDENCE_DIR / "tranche_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"expected={report['expected_operation_count']} executed={report['executed_operation_count']}")
    print(f"dropped={report['dropped_operations']}")
    print(f"unexpected={report['unexpected_operations']}")
    print(f"mismatched={report['mismatched_operations']}")
    for name, digest in sorted(hashes.items()):
        print(f"artifact {name}: {digest}")
    return 0 if report["no_drop_ok"] and report["all_expected_reached"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
