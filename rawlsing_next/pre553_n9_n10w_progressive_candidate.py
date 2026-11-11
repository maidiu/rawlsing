"""PYAT HQ281 E03 - source-free N9 to N10W two-step progressive owner run CANDIDATE.

Development-only bounded adapter.  It joins ACTUAL accepted owners that exist
today — N10E ``provide_empirical_possibility_slice`` (single conditioner),
C1 ``compose_positioned_subject_possibility`` (multi-conditioner witness),
and plain F8 ``evaluate_positioned_subject_possibility`` — into one measured
progressive chain P(Y|A) -> P(Y|A,B) [-> P(Y|A,B,C)] over an explicitly
synthetic world fixture that is NEVER called real CURRENT.

What this candidate does NOT do (and refuses to imply)
------------------------------------------------------
* N9 (publication/resolution/lifecycle world-serving) and N10W (progressive
  multi-condition world binding) are NOT implemented anywhere in the
  repository (E01 API graph grades both ``implemented: false``).  This module
  does not implement them either.  It demonstrates the progressive
  conditioning the N10E->N10W edge demands, using real owners, at
  development scope only.
* No G0b issuance, no model-use grant, no B5 CURRENT selection, no Field
  Forge, no temporal/CURRENT, no actor/V3 state.  Every positioned subject
  in the fixture carries ``real_subject: False``.
* No raw SAV/DTA is read; the world is 58 synthetic respondents defined
  below.  No respondent row leaves this module except inside exact owner
  objects.

Synthetic world law (hand-derived BEFORE any owner runs; 58 respondents)
------------------------------------------------------------------------
Questions A, B, C, Y are binary (0/1).  Cell counts (Y=1, Y=0):

  A B C :  1 1 1: 6,2 | 1 1 0: 4,4 | 1 0 1: 5,3 | 1 0 0: 3,5
           0 1 1: 4,2 | 0 1 0: 2,4 | 0 0 1: 3,3 | 0 0 0: 2,6

Exact progressive truth this chain must reproduce (and does):

  P(Y=1|A=1)           = 18/32 = 9/16   (denominator 32)
  P(Y=1|A=1,B=1)       = 10/16 = 5/8    (denominator 16)
  P(Y=1|A=1,B=1,C=1)   = 6/8   = 3/4    (denominator 8)

Every cell keeps both Y values present (minimum count 2): minority
alternatives survive at every step; nothing is pruned.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_objects import (
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    canonicalize,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_possibility_provider import (
    PROVIDER_STATE_EXACT,
    provide_empirical_possibility_slice,
)
from rawlsing_next.pre553_analytical_composition import (
    compose_positioned_subject_possibility,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
    evaluate_positioned_subject_possibility,
)
import rawlsing_next.tests.c1_at08_at13_fixture as fx
import rawlsing_next.tests.test_pre553_empirical_query as i03


E03_CONTRACT_ID = "PYAT_HQ281_E03_PROGRESSIVE_N9_N10W_JOIN_CANDIDATE@1.0.0"
E03_FIXTURE_ID = "E03_PROGRESSIVE_ABC_Y_58"
E03_TAG = "e03-progressive"

#: Hand-derived exact truth, fixed before any owner runs (see module docstring).
E03_ORACLE = MappingProxyType({
    "fixture_id": E03_FIXTURE_ID,
    "fixture_rows": 58,
    "step1": {"conditioners": ("A",), "target": "Y",
              "denominator": 32, "cells": {"1": 18, "0": 14},
              "fraction": {"$exact_fraction": [9, 16]}},
    "step2": {"conditioners": ("A", "B"), "target": "Y",
              "denominator": 16, "cells": {"1": 10, "0": 6},
              "fraction": {"$exact_fraction": [5, 8]}},
    "step3": {"conditioners": ("A", "B", "C"), "target": "Y",
              "denominator": 8, "cells": {"1": 6, "0": 2},
              "fraction": {"$exact_fraction": [3, 4]}},
})

_CELL_COUNTS = {
    (1, 1, 1): (6, 2),
    (1, 1, 0): (4, 4),
    (1, 0, 1): (5, 3),
    (1, 0, 0): (3, 5),
    (0, 1, 1): (4, 2),
    (0, 1, 0): (2, 4),
    (0, 0, 1): (3, 3),
    (0, 0, 0): (2, 6),
}


class E03ProgressiveError(ValueError):
    """The progressive candidate cannot lawfully emit the requested run."""


def _effects() -> Mapping[str, bool]:
    return MappingProxyType({
        "source_meaning_inference": False,
        "model_use_grant": False,
        "g0b_issuance": False,
        "b5_current_selection": False,
        "field_forge_effect": False,
        "temporal_current_effect": False,
        "actor_v3_effect": False,
        "real_current_claim": False,
    })


def synthetic_world_rows() -> list:
    """The exact 58-respondent synthetic law.  No raw survey, no real subject."""
    rows = []
    for (a, b, c), (n1, n0) in sorted(_CELL_COUNTS.items()):
        for n in range(1, n1 + 1):
            rows.append({"id": f"E03-{a}{b}{c}Y{n:02d}",
                         "responses": {"A": a, "B": b, "C": c, "Y": 1}})
        for n in range(1, n0 + 1):
            rows.append({"id": f"E03-{a}{b}{c}N{n:02d}",
                         "responses": {"A": a, "B": b, "C": c, "Y": 0}})
    return rows


def build_synthetic_world(*, tag: str = E03_TAG) -> dict:
    """Build the synthetic world through the accepted test-source factory.

    One shared risk set over all respondents and all four questions, so every
    progressive step measures its denominator over the exact same respondent
    pool with the exact same risk identity.
    """
    rows = synthetic_world_rows()
    assert len(rows) == 58
    source = i03._build_source(
        tag,
        rows,
        question_namespace=tag,
        risk_sets={"R_ALL": {
            "A": {r["id"] for r in rows},
            "B": {r["id"] for r in rows},
            "C": {r["id"] for r in rows},
            "Y": {r["id"] for r in rows},
        }},
        risk_namespace=tag,
    )
    source["risk_refs"]["R"] = source["risk_refs"]["R_ALL_58"] \
        if "R_ALL_58" in source["risk_refs"] else source["risk_refs"]["R_ALL"]
    qauth = i03._query_authority(f"{tag}-query")
    registry = i03._registry(source, qauth)
    pairing = fx.make_pairing_authority(tag)
    model_rule = fx.make_model_rule(source["universe"].ref, tag)
    return {
        "tag": tag,
        "source": source,
        "qauth": qauth,
        "registry": registry,
        "pairing": pairing,
        "model_rule": model_rule,
        "source_sha_note": "synthetic-only; no source bytes exist",
    }


def _leaf(world: dict, question: str, value: int) -> dict:
    return i03._response_leaf(world["source"], world["qauth"], question, value)


def _joint_predicate(world: dict, conditions: tuple) -> Any:
    """AND of response leaves, canonical hash-sorted (owner law)."""
    leaves = [_leaf(world, question, value) for question, value in conditions]
    ordered = sorted(
        leaves, key=lambda leaf: semantic_hash(canonicalize(leaf))
    )
    return i03._predicate(
        world["source"],
        world["qauth"],
        {"op": "AND", "children": ordered},
        tag=f"{world['tag']}-joint-" + "-".join(
            f"{q}{v}" for q, v in conditions),
    )


def _producer_query(world: dict, predicate: Any, target: str = "Y") -> Any:
    query = i03._query(
        world["source"],
        world["qauth"],
        predicate,
        (target,),
        risk="R",
        tag=f"{world['tag']}-to-{target.lower()}",
    )
    component = dict(query.target_arity_and_topology["components"][0])
    component["domain"] = ["0", "1"]
    component["target_domain_replay_ref"] = i03._ref(
        "TARGET_DOMAIN", f"{target}-01")
    return EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=query.producer_replay_locator_or_reference_root,
        target_refs=query.target_refs,
        target_arity_and_topology={
            "arity": 1,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": [component],
        },
        condition_predicate_ref=query.condition_predicate_ref,
        risk_set_ref=query.risk_set_ref,
        empirical_universe_refs=query.empirical_universe_refs,
        scope_refs=query.scope_refs,
        measure_basis_ref=query.measure_basis_ref,
        requested_output_grain=query.requested_output_grain,
        query_authority_refs=query.query_authority_refs,
    )


def _subject_ref(step: str, role: str) -> tuple[ExactRef, dict]:
    """Synthetic positioned-subject identity. ``real_subject`` is False.

    Returns (ref, material): the material carries the honest synthetic flag
    so no caller can mistake this subject for a real population member.
    """
    material = {
        "schema": "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "fixture_id": E03_FIXTURE_ID,
        "role": role,
        "step": step,
        "real_subject": False,
    }
    return ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        f"urn:test:e03:{step}:{role.lower()}",
        semantic_hash(material),
    ), material


def _consumer_query(world: dict, step: str, conditions: tuple) -> Any:
    source = world["source"]
    bindings = tuple(
        fx.make_conditioner_binding(
            binding_id=question.lower(),
            subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, question, value)),
            empirical_coordinate_ref=source["qrefs"][question],
            comparability_authority_ref=world["pairing"],
            source_universe_ref=source["universe"].ref,
            release_ref=source["release_ref"],
        )
        for question, value in conditions
    )
    return fx.make_multi_conditioner_consumer_query(
        query_id=f"{world['tag']}-{step}",
        subject_ref=_subject_ref(step, "CONDITIONED_SUBJECT")[0],
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=list(bindings),
        projection_kind="E03_PROGRESSIVE_CONDITIONAL_DISTRIBUTION",
        projection_payload={"step": step},
    )


def _witness(world: dict, step: str, consumer_query: Any,
             producer_query: Any, predicate: Any,
             conditions: tuple) -> Any:
    source = world["source"]
    bindings = list(consumer_query.conditioner_bindings)
    return fx.build_witness_for_binding(
        witness_object_id=f"urn:test:e03:{step}:witness",
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=predicate,
        bindings=bindings,
        coordinate_value_pairs=[
            (source["qrefs"][question], value) for question, value in conditions
        ],
        pairing_authority=world["pairing"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )


@dataclass(frozen=True)
class ProgressiveStepResult:
    step_id: str
    conditioners: tuple
    producer_route: str
    producer_fact_state: str
    raw_denominator_support: int
    cells: Mapping[str, Any]
    consumer_state: str
    release_ref: ExactRef
    risk_set_ref: ExactRef
    invocation_log: tuple
    produced_evidence: Any = None
    uncertainty_state: str = ""


def _log(call: str, inputs: Mapping[str, Any], outputs: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType({"call": call, "inputs": dict(inputs),
                             "outputs": dict(outputs)})


def _cells_of(geometry_cells: Any) -> dict:
    return {str(cell["cell"]): dict(cell) for cell in geometry_cells}


def _composition_cells(composition: Any) -> dict:
    return _cells_of(composition.complete_cell_geometry)


def run_single_conditioner_step(world: dict) -> ProgressiveStepResult:
    """Step 1, P(Y|A=1): the REAL N10E provider (single conditioner)."""
    conditions = (("A", 1),)
    predicate = _joint_predicate(world, conditions)
    producer_query = _producer_query(world, predicate)
    consumer_query = _consumer_query(world, "step1", conditions)
    witness = _witness(world, "step1", consumer_query, producer_query,
                       predicate, conditions)
    source = world["source"]
    result = provide_empirical_possibility_slice(
        repository=source["repo"],
        empirical_query=producer_query,
        predicate=predicate,
        authority_registry=world["registry"],
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=world["model_rule"],
        condition_binding_witness=witness,
    )
    if result.provider_state != PROVIDER_STATE_EXACT:
        raise E03ProgressiveError(
            f"step1 N10E provider refused: state={result.provider_state!r} "
            f"reason={result.refusal_reason!r}"
        )
    composition = result.composition_result
    evidence = result.generated_evidence_or_null
    consumer = result.consumer_result_or_null
    return ProgressiveStepResult(
        step_id="P_Y_given_A",
        conditioners=conditions,
        producer_route="N10E_SINGLE_CONDITIONER",
        producer_fact_state="SUPPORTED",
        raw_denominator_support=composition.raw_denominator_support,
        cells=_composition_cells(composition),
        consumer_state=consumer.result_state,
        release_ref=source["release_ref"],
        risk_set_ref=producer_query.risk_set_ref,
        produced_evidence=evidence,
        uncertainty_state=evidence.uncertainty_state,
        invocation_log=(
            _log("provide_empirical_possibility_slice",
                 {"empirical_query": producer_query.ref.as_dict(),
                  "predicate": predicate.ref.as_dict(),
                  "consumer_query": consumer_query.ref.as_dict(),
                  "conditioners": [list(c) for c in conditions]},
                 {"provider_state": result.provider_state,
                  "evidence_ref": evidence.evidence_ref.as_dict(),
                  "consumer_state": consumer.result_state}),
        ),
    )


def run_joint_conditioner_step(world: dict, step_id: str,
                               conditions: tuple) -> ProgressiveStepResult:
    """Steps 2..N, P(Y|A,..): the REAL C1 multi-conditioner composition."""
    if len(conditions) < 2:
        raise E03ProgressiveError("joint step requires two or more conditioners")
    predicate = _joint_predicate(world, conditions)
    producer_query = _producer_query(world, predicate)
    consumer_query = _consumer_query(world, step_id, conditions)
    witness = _witness(world, step_id, consumer_query, producer_query,
                       predicate, conditions)
    source = world["source"]
    result = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=producer_query,
        predicate=predicate,
        authority_registry=world["registry"],
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=world["model_rule"],
        condition_binding_witness=witness,
    )
    if result.analytical_state != "SUPPORTED":
        raise E03ProgressiveError(
            f"{step_id} C1 composition refused: analytical_state="
            f"{result.analytical_state!r}"
        )
    evidence = result.possibility_slice_evidence_or_null
    consumer = result.consumer_result_or_null
    return ProgressiveStepResult(
        step_id=step_id,
        conditioners=conditions,
        producer_route="C1_MULTI_CONDITIONER",
        producer_fact_state="SUPPORTED",
        raw_denominator_support=result.raw_denominator_support,
        cells=_composition_cells(result),
        consumer_state=consumer.result_state,
        release_ref=source["release_ref"],
        risk_set_ref=producer_query.risk_set_ref,
        produced_evidence=evidence,
        uncertainty_state=evidence.uncertainty_state,
        invocation_log=(
            _log("compose_positioned_subject_possibility",
                 {"empirical_query": producer_query.ref.as_dict(),
                  "predicate": predicate.ref.as_dict(),
                  "consumer_query": consumer_query.ref.as_dict(),
                  "conditioners": [list(c) for c in conditions]},
                 {"analytical_state": result.analytical_state,
                  "evidence_ref": evidence.evidence_ref.as_dict(),
                  "consumer_state": consumer.result_state}),
        ),
    )


@dataclass(frozen=True)
class ProgressiveChainResult:
    steps: tuple
    f8_consumptions: tuple
    invocation_log: tuple
    effects: Mapping[str, bool]

    def oracle_cell(self, step_id: str) -> Mapping[str, Any]:
        step = next(s for s in self.steps if s.step_id == step_id)
        return {"denominator": step.raw_denominator_support,
                "cells": {k: v["raw_numerator_support"]
                          for k, v in step.cells.items()}}


def consume_step_with_f8(world: dict, step: ProgressiveStepResult) -> Mapping[str, Any]:
    """Separate CONSUMPTION invocation through the real plain F8 evaluator.

    Production (provider/compose) and consumption (this call) are logged as
    distinct invocations with distinct call identities.  The evidence object
    handed to F8 is the owner-produced object from that step's own production
    call — never a recomposed twin and never a handwritten slice.
    """
    result = evaluate_positioned_subject_possibility(
        query=_consumer_query(world, step.step_id, step.conditioners),
        rule=world["model_rule"],
        evidence=(step.produced_evidence,),
    )
    return MappingProxyType({
        "call": "evaluate_positioned_subject_possibility",
        "step_id": step.step_id,
        "result_state": result.result_state,
        "exact_disposition": result.exact_disposition,
        "exact_reason": result.exact_reason,
        "exact_evidence_ref": (
            None if result.exact_evidence_ref is None
            else result.exact_evidence_ref.as_dict()),
    })


def _consumer_query_for_f8(world: dict, step: ProgressiveStepResult) -> Any:
    return _consumer_query(world, step.step_id, step.conditioners)


def run_progressive_chain(world: dict | None = None) -> ProgressiveChainResult:
    """Execute P(Y|A) -> P(Y|A,B) -> P(Y|A,B,C), each step real."""
    world = world or build_synthetic_world()
    source = world["source"]

    step1 = run_single_conditioner_step(world)
    step2 = run_joint_conditioner_step(world, "P_Y_given_A_B", (("A", 1), ("B", 1)))
    step3 = run_joint_conditioner_step(
        world, "P_Y_given_A_B_C", (("A", 1), ("B", 1), ("C", 1)))

    # CONSUMPTION is a distinct invocation: each step's OWN produced evidence
    # object is handed to the real F8 evaluator, never recomposed.
    f8_calls = [consume_step_with_f8(world, step) for step in (step1, step2, step3)]

    log = (
        step1.invocation_log + step2.invocation_log + step3.invocation_log
        + tuple(f8_calls)
    )
    return ProgressiveChainResult(
        steps=(step1, step2, step3),
        f8_consumptions=tuple(f8_calls),
        invocation_log=log,
        effects=_effects(),
    )


__all__ = [
    "E03_CONTRACT_ID",
    "E03_FIXTURE_ID",
    "E03_ORACLE",
    "E03ProgressiveError",
    "synthetic_world_rows",
    "build_synthetic_world",
    "run_single_conditioner_step",
    "run_joint_conditioner_step",
    "consume_step_with_f8",
    "run_progressive_chain",
]
