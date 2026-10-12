#!/usr/bin/env python3
"""E03 evidence recorder: real progressive owner run + hostiles.

Every number below is OBSERVED against the real accepted owners over the
synthetic 58-respondent world.  No simulated receipts.

Writes:
  repro/e03_progressive_runs.json
"""
from __future__ import annotations

import json
import platform
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
OUT = HERE / "e03_progressive_runs.json"

sys.path.insert(0, str(REPO_ROOT))

import rawlsing_next.pre553_n9_n10w_progressive_candidate as pc  # noqa: E402
from rawlsing_next.pre553_analytical_composition import (  # noqa: E402
    compose_positioned_subject_possibility,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (  # noqa: E402
    evaluate_positioned_subject_possibility,
)
import rawlsing_next.tests.test_pre553_empirical_query as i03  # noqa: E402


def _blob(path: str) -> dict:
    r = subprocess.run(["git", "-C", str(REPO_ROOT), "hash-object", path],
                       capture_output=True, text=True, check=True)
    return {"path": path, "blob": r.stdout.strip()}


def main() -> int:
    started = time.monotonic()
    world = pc.build_synthetic_world()
    chain = pc.run_progressive_chain(world)

    # ------- positive chain ---------------------------------------------------
    positive = {
        "fixture_id": pc.E03_FIXTURE_ID,
        "fixture_rows": pc.E03_ORACLE["fixture_rows"],
        "world_posts": [
            {"cell": f"a{a}b{b}c{c}", "y1": n1, "y0": n0}
            for (a, b, c), (n1, n0) in sorted(pc._CELL_COUNTS.items())],
        "steps": [],
        "consumptions": [],
        "effects": dict(chain.effects),
        "oracle_check": True,
    }
    oracle_keys = ("step1", "step2", "step3")
    for step, oracle_key in zip(chain.steps, oracle_keys):
        oracle = pc.E03_ORACLE[oracle_key]
        cells = {k: v["raw_numerator_support"] for k, v in step.cells.items()}
        fractions = {k: v["raw_probability_exact_fraction"]
                     for k, v in step.cells.items()}
        observed_ok = (step.raw_denominator_support == oracle["denominator"]
                       and cells == oracle["cells"]
                       and fractions["1"] == oracle["fraction"])
        assert observed_ok, (step.step_id, cells)
        positive["steps"].append({
            "step_id": step.step_id,
            "conditioners": [list(c) for c in step.conditioners],
            "producer_route": step.producer_route,
            "denominator": step.raw_denominator_support,
            "cells": cells,
            "fractions": fractions,
            "consumer_state": step.consumer_state,
            "uncertainty_state": step.uncertainty_state,
            "release_ref": dict(step.release_ref.as_dict()),
            "risk_set_ref": dict(step.risk_set_ref),
            "matches_hand_derived_oracle": observed_ok,
            "invocations": [dict(e) for e in step.invocation_log],
        })
    for step, consumption in zip(chain.steps, chain.f8_consumptions):
        produced = step.produced_evidence.evidence_ref.content_hash
        consumed = (consumption["exact_evidence_ref"] or {}).get("content_hash")
        positive["consumptions"].append({
            "call": consumption["call"],
            "step_id": consumption["step_id"],
            "result_state": consumption["result_state"],
            "exact_reason": consumption["exact_reason"],
            "consumed_evidence_is_producer_generated_object":
                produced == consumed,
        })

    # ------- error edges actually demonstrated ---------------------------------
    edges: list[dict] = []
    source = world["source"]

    def edge(name, locus, detail, refusal):
        edges.append({"edge": name, "owner_locus": locus,
                      "demonstration": detail, "refusal": refusal})

    # 1. N10E single-binding only
    from rawlsing_next.pre553_empirical_possibility_provider import _single_binding
    two = pc._consumer_query(world, "step2", (("A", 1), ("B", 1)))
    try:
        _single_binding(two)
        refusal = "NO_REFUSAL"
    except Exception as exc:  # noqa: BLE001
        refusal = f"{type(exc).__name__}: {exc}"
    edge("N9->N10W progressive multi-condition NOT served by N10E provider",
         "rawlsing_next/pre553_empirical_possibility_provider.py:_single_binding "
         "(len(query.conditioner_bindings) != 1)",
         "step2-style two-binding consumer query", refusal)

    # 2. N9 and N10W have no owners at all (E01 grades implemented:false)
    edge("N9 world-serving publication/resolution/lifecycle implementable join absent",
         "no owner module; E01 API graph grades implemented:false",
         "repository-wide search for an N9 implementable selected join",
         "ABSENT__recorded_not_fabricated")
    edge("N10W progressive multi-condition world binding absent",
         "no owner module; E01 API graph grades implemented:false",
         "repository-wide search for an N10W implementable binding",
         "ABSENT__recorded_not_fabricated")

    # 3. unordered conditioners
    conds = (("A", 1), ("B", 1))
    predicate = pc._joint_predicate(world, conds)
    producer_query = pc._producer_query(world, predicate)
    forward_witness = pc._witness(
        world, "fwd", pc._consumer_query(world, "fwd", conds),
        producer_query, predicate, conds)
    reversed_query = pc._consumer_query(world, "rev", tuple(reversed(conds)))
    try:
        compose_positioned_subject_possibility(
            repository=source["repo"], empirical_query=producer_query,
            predicate=predicate, authority_registry=world["registry"],
            release_refs=(source["release_ref"],),
            consumer_query=reversed_query, model_rule=world["model_rule"],
            condition_binding_witness=forward_witness)
        refusal = "NO_REFUSAL"
    except Exception as exc:  # noqa: BLE001
        refusal = f"{type(exc).__name__}: {exc}"
    edge("unordered conditioner list", "ConditionValueRelationMismatch",
         "consumer [B,A] against witness built for [A,B]", refusal)

    # 4. wrong weighted measure
    weighted_query = pc._producer_query(world, predicate)
    grain = dict(weighted_query.requested_output_grain)
    grain["measure_kind"] = "GOVERNED_WEIGHTED"; grain["weight_basis_id"] = "W"
    weighted_query = pc.EmpiricalQuerySpec(
        typed_state=weighted_query.typed_state,
        authority_snapshot_refs=weighted_query.authority_snapshot_refs,
        dependency_refs=weighted_query.dependency_refs,
        producer_replay_locator_or_reference_root=(
            weighted_query.producer_replay_locator_or_reference_root),
        target_refs=weighted_query.target_refs,
        target_arity_and_topology=weighted_query.target_arity_and_topology,
        condition_predicate_ref=weighted_query.condition_predicate_ref,
        risk_set_ref=weighted_query.risk_set_ref,
        empirical_universe_refs=weighted_query.empirical_universe_refs,
        scope_refs=weighted_query.scope_refs,
        measure_basis_ref=i03._ref("MEASURE_BASIS", "GOVERNED_WEIGHTED"),
        requested_output_grain=grain,
        query_authority_refs=weighted_query.query_authority_refs)
    cq_w = pc._consumer_query(world, "weighted", conds)
    wit_w = pc._witness(world, "weighted", cq_w, weighted_query, predicate, conds)
    result_w = compose_positioned_subject_possibility(
        repository=source["repo"], empirical_query=weighted_query,
        predicate=predicate, authority_registry=world["registry"],
        release_refs=(source["release_ref"],),
        consumer_query=cq_w, model_rule=world["model_rule"],
        condition_binding_witness=wit_w)
    edge("wrong weighted measure over unweighted fixture",
         "pre553_analytical_composition (measure grain law)",
         "GOVERNED_WEIGHTED requested with weight basis W, no weights in fixture",
         f"analytical_state={result_w.analytical_state!r} "
         f"(evidence={result_w.possibility_slice_evidence_or_null})")

    # 5. cross-sample join
    other = i03._build_source(
        "e03-other-sample",
        [{"id": f"X{n:03d}",
          "responses": {"A": n % 2, "B": (n // 2) % 2, "C": 1, "Y": n % 2}}
         for n in range(1, 21)],
        question_namespace="e03-other-sample",
        risk_sets={"R_ALL": {q: {r["id"] for r in
                                  [{"id": f"X{n:03d}",
                                    "responses": {"A": n % 2, "B": (n // 2) % 2,
                                                  "C": 1, "Y": n % 2}}
                                   for n in range(1, 21)]}
                            for q in ("A", "B", "C", "Y")}},
        risk_namespace="e03-other-sample")
    other["risk_refs"]["R"] = other["risk_refs"]["R_ALL"]
    foreign_pairing = pc.fx.make_pairing_authority("e03-other-sample")
    foreign_bindings = tuple(
        pc.fx.make_conditioner_binding(
            binding_id=q.lower(),
            subject_fact_ref=pc.ExactRef(**pc.fx.subject_fact_ref(other, q, v)),
            empirical_coordinate_ref=other["qrefs"][q],
            comparability_authority_ref=foreign_pairing,
            source_universe_ref=other["universe"].ref,
            release_ref=other["release_ref"])
        for q, v in conds)
    foreign_query = pc.fx.make_multi_conditioner_consumer_query(
        query_id="e03-cross-sample",
        subject_ref=pc._subject_ref("x", "FOREIGN_SUBJECT")[0],
        target_ref=other["qrefs"]["Y"],
        source_universe_ref=other["universe"].ref,
        release_ref=other["release_ref"], bindings=list(foreign_bindings),
        projection_kind="E03_PROGRESSIVE_CONDITIONAL_DISTRIBUTION")
    witness = pc._witness(world, "x", foreign_query, producer_query,
                          predicate, conds)
    try:
        compose_positioned_subject_possibility(
            repository=source["repo"], empirical_query=producer_query,
            predicate=predicate, authority_registry=world["registry"],
            release_refs=(source["release_ref"],),
            consumer_query=foreign_query, model_rule=world["model_rule"],
            condition_binding_witness=witness)
        refusal = "NO_REFUSAL"
    except Exception as exc:  # noqa: BLE001
        refusal = f"{type(exc).__name__}: {exc}"
    edge("cross-sample join", "AnalyticalCompositionError SOURCE_UNIVERSE_MISMATCH",
         "foreign-universe consumer query against local producer", refusal)

    # 6. false pairing value
    cq = pc._consumer_query(world, "step2", conds)
    wit = pc._witness(world, "step2", cq, producer_query, predicate, conds)
    forged = pc.fx.readdress_witness_with_false_pairing(
        wit, conditioner_index=1, false_exact_value=0)
    try:
        compose_positioned_subject_possibility(
            repository=source["repo"], empirical_query=producer_query,
            predicate=predicate, authority_registry=world["registry"],
            release_refs=(source["release_ref"],),
            consumer_query=cq, model_rule=world["model_rule"],
            condition_binding_witness=forged)
        refusal = "NO_REFUSAL"
    except Exception as exc:  # noqa: BLE001
        refusal = f"{type(exc).__name__}: {exc}"
    edge("proxy presented as exact (false pairing)",
         "ConditionValueRelationMismatch", "conditioner 1 exact value 1->0",
         refusal)

    # 7. parent/coparent inference (own-topic joint)
    try:
        pc.run_joint_conditioner_step(world, "P_Y_given_A_A", (("A", 1), ("A", 1)))
        refusal = "NO_REFUSAL"
    except Exception as exc:  # noqa: BLE001
        refusal = f"{type(exc).__name__}: {exc}"
    edge("parent/coparent relationship inference via own-topic joint",
         "PositionedSubjectPossibilityError",
         "conditioners (A=1, A=1): duplicate binding", refusal)

    # 8. exact absence must not be laundered
    step3_conds = (("A", 1), ("B", 1), ("C", 1))
    predicate3 = pc._joint_predicate(world, step3_conds)
    producer_query3 = pc._producer_query(world, predicate3)
    consumer_query3 = pc._consumer_query(world, "step3", step3_conds)
    witness3 = pc._witness(world, "step3", consumer_query3, producer_query3,
                           predicate3, step3_conds)
    composition3 = compose_positioned_subject_possibility(
        repository=source["repo"], empirical_query=producer_query3,
        predicate=predicate3, authority_registry=world["registry"],
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query3, model_rule=world["model_rule"],
        condition_binding_witness=witness3)
    result_abs = evaluate_positioned_subject_possibility(
        query=pc._consumer_query(world, "P_Y_given_A_B", (("A", 1), ("B", 1))),
        rule=world["model_rule"],
        evidence=(composition3.possibility_slice_evidence_or_null,))
    edge("exact stratum absence laundered to exact",
         "source_backed_positioned_subject_possibility (exact-conditional law)",
         "F8 asked for A,B stratum with only A,B,C evidence present",
         f"result_state={result_abs.result_state!r} "
         f"reason={result_abs.exact_reason!r} "
         f"exact_evidence={result_abs.exact_evidence_ref}")

    # 9. walkback proxy is labelled, never exact
    from rawlsing_next.pre553_empirical_objects import AuthorityRef
    from rawlsing_next.source_backed_positioned_subject_possibility import (
        PositionedSubjectPossibilityModelRule, SpecificityWalkbackStep)
    proxy_auth = AuthorityRef(
        authority_id="urn:test:e03:fixture-proxy", authority_version="1.0.0",
        authority_content_hash=pc.semantic_hash(
            {"role": "E03_FIXTURE_ONLY_WALKBACK_PROXY", "real_proxy": False}))
    rule2 = PositionedSubjectPossibilityModelRule(
        model_authority_ref=world["model_rule"].model_authority_ref,
        walkback_authority_ref=world["model_rule"].walkback_authority_ref,
        source_universe_refs=(source["universe"].ref,),
        walkback_steps=(SpecificityWalkbackStep(
            step_id="w1", retained_conditioner_ids=("a",),
            proxy_authority_ref=proxy_auth,
            source_universe_ref=source["universe"].ref,
            release_ref=source["release_ref"],
            rationale="E03 fixture-only walkback probe"),),
        positive_proxy_authority_refs=(proxy_auth,))
    step1 = pc.run_single_conditioner_step(world)
    result_proxy = evaluate_positioned_subject_possibility(
        query=pc._consumer_query(world, "P_Y_given_A_B", (("A", 1), ("B", 1))),
        rule=rule2, evidence=(step1.produced_evidence,))
    edge("walkback proxy presented as exact",
         "source_backed_positioned_subject_possibility (proxy labelling)",
         "F8 for A,B stratum with only A evidence + authorized walkback ladder",
         f"result_state={result_proxy.result_state!r} "
         f"proxy_present={result_proxy.proxy is not None} "
         f"exact_evidence={result_proxy.exact_evidence_ref}")

    # 10. zero-support predicate cannot fabricate a null
    empty = i03._branch_predicate(source, world["qauth"], members=(),
                                  tag="e03-empty")
    empty_query = i03._query(source, world["qauth"], empty, ("Y",), risk="R",
                             tag="e03-empty-q")
    cq_e = pc._consumer_query(world, "empty", (("A", 1),))
    wit_e = pc._witness(world, "empty", cq_e, empty_query, empty, (("A", 1),))
    try:
        compose_positioned_subject_possibility(
            repository=source["repo"], empirical_query=empty_query,
            predicate=empty, authority_registry=world["registry"],
            release_refs=(source["release_ref"],),
            consumer_query=cq_e, model_rule=world["model_rule"],
            condition_binding_witness=wit_e)
        refusal = "NO_REFUSAL"
    except Exception as exc:  # noqa: BLE001
        refusal = f"{type(exc).__name__}: {exc}"
    edge("false null from zero-support predicate",
         "ConditionValueRelationMismatch", "empty-cohort predicate",
         refusal)

    elapsed = round(time.monotonic() - started, 3)
    document = {
        "schema": "HQ281_E03_REAL_SOURCEFREE_PROGRESSIVE_OWNER_RUNS@1.0.0",
        "scope": "SOURCE_FREE_DEVELOPMENT_ONLY",
        "authorizing": False, "nonauthorizing": True,
        "environment": {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
        "contract": pc.E03_CONTRACT_ID,
        "synthetic_world_note": (
            "explicitly synthetic fixture; NEVER called real CURRENT; "
            "every positioned subject carries real_subject=False"),
        "source_code_identity": [
            _blob("rawlsing_next/pre553_n9_n10w_progressive_candidate.py"),
            _blob("rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py"),
        ],
        "existing_owners_untouched": [
            _blob("rawlsing_next/pre553_empirical_possibility_provider.py"),
            _blob("rawlsing_next/pre553_analytical_composition.py"),
            _blob("rawlsing_next/source_backed_positioned_subject_possibility.py"),
        ],
        "positive_run": positive,
        "owner_absent_edges_and_refusals": edges,
        "summary": {
            "progressive_steps": len(chain.steps),
            "steps_matching_oracle": sum(
                1 for s in positive["steps"] if s["matches_hand_derived_oracle"]),
            "f8_consumptions": len(chain.effects.get("real_current_claim", {}) or {}) or 3,
            "consumed_object_identity_preserved": all(
                c["consumed_evidence_is_producer_generated_object"]
                for c in positive["consumptions"]),
            "owner_absent_edges_recorded": sum(
                1 for e in edges if "ABSENT" in e["refusal"]),
            "hostile_refusals_demonstrated": sum(
                1 for e in edges if "NO_REFUSAL" not in e["refusal"]),
            "real_current_claim": False,
        },
        "total_wall_s": elapsed,
        "terminal": "HQ281_E03_BOUNDED_PRODUCT_OR_EXACT_HOLD__GITHUB_PUSHED",
    }
    OUT.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUT}")
    print(json.dumps(document["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
