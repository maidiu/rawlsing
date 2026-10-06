#!/usr/bin/env python3
"""HQ221 fresh-process N10E provider -> consumer -> dependency/lifecycle replay runner.

This runner is a *fresh Python process*. It reads a retained-determinant INPUT
artifact that contains only exact determinant/authority/release/query/model/witness
identity material. It carries no answer: no expected output identity, no result or
evidence ref, no fact/evidence ref copied from an answer, no denominator/support
oracle, and no probability geometry.

The runner executes the FULL accepted owner chain in this process and prints only
what it computed:

    exact determinants
      -> provide_empirical_possibility_slice          (N10E provider seam)
      -> compose_positioned_subject_possibility       (accepted analytical producer)
      -> producer-generated PossibilitySliceEvidence
      -> evaluate_positioned_subject_possibility      (named public consumer)
      -> provider receipt
      -> AnalyticalProductRegistration / graph        (dependency registration)
      -> transition_analytical_dependencies           (accepted lifecycle owner)
      -> resolve_current_analytical_product           (currentness resolution)

The runner never reads a stored receipt, a stored product, or any expected identity.
It recomputes everything and prints the recomputed identities. A stored-output
deserialization cannot satisfy this runner, and the parent court holds the oracle.

The expected identity is supplied only on the ORACLE side by the parent court via
``--expect``; it is used solely for an in-process equality check after the fact and
is never consulted to *produce* any output.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from rawlsing_next.pre553_analytical_replay_dependency import (
    DETERMINANT_DEPENDENT_PRODUCT,
    DETERMINANT_IMMUTABLE_IDENTITY,
    DETERMINANT_ROOT_AUTHORITY,
    DETERMINANT_UNOWNED,
    AnalyticalDependencyRegistry,
    AnalyticalProductRegistration,
    DeterminantOwnerEvidence,
    ExactDeterminantOwnership,
    assert_runner_input_carries_no_answer,
    resolve_current_analytical_product,
    transition_analytical_dependencies,
)
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_empirical_possibility_provider import (
    provide_empirical_possibility_slice,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    PositionedSubjectPossibilityModelRule,
)
from rawlsing_next.tests import c1_at18_at19_fixture as fx

PRODUCT_KIND = "N10E_EMPIRICAL_POSSIBILITY_SLICE_PRODUCT@1"
PRODUCT_OBJECT_ID = "urn:test:hq221:n10e:provider-product:forward"
#: The N10E provider seam that this runner invokes.
PROVIDER_PATH = (
    "rawlsing_next.pre553_empirical_possibility_provider."
    "provide_empirical_possibility_slice"
)
#: The ACCEPTED ANALYTICAL PRODUCER that actually computes the slice. This is a
#: distinct callable from the provider seam and is named separately so the transcript
#: never mislabels the provider as the producer (HQ223 documentary correction 1).
PRODUCER_PATH = (
    "rawlsing_next.pre553_analytical_composition."
    "compose_positioned_subject_possibility"
)
CONSUMER_PATH = (
    "rawlsing_next.source_backed_positioned_subject_possibility."
    "evaluate_positioned_subject_possibility"
)


def rebuild_case(determinants: dict[str, Any]) -> dict[str, Any]:
    """Rebuild the accepted provider case and verify it matches the retained refs.

    This is the deterministic-reconstruction half: the fresh process rebuilds the
    synthetic source-free fixture and every accepted determinant from the retained
    identity material, and fails closed if any retained identity does not rebuild
    exactly. It reads no answer.
    """

    direction = determinants["direction"]
    case = fx.build_case(direction)

    checks = {
        "empirical_query_ref": case["empirical_query"].ref,
        "predicate_ref": case["predicate"].ref,
        "condition_binding_witness_ref": case["condition_binding_witness"].witness_ref,
        "consumer_query_ref": case["consumer_query"].ref,
        "source_universe_ref": case["source"]["universe"].ref,
    }
    for key, rebuilt in checks.items():
        retained = exact_ref(determinants[key], key)
        if rebuilt != retained:
            raise AssertionError(
                f"retained determinant {key} did not rebuild exactly: "
                f"{rebuilt.key} != {retained.key}"
            )
    if case["predicate"].predicate_hash != determinants["predicate_hash"]:
        raise AssertionError("retained predicate_hash did not rebuild exactly")
    if case["model_rule"].rule_hash != determinants["model_rule_hash"]:
        raise AssertionError("retained model_rule_hash did not rebuild exactly")

    retained_releases = tuple(
        exact_ref(x, "release_ref") for x in determinants["release_refs"]
    )
    if tuple(case["release_refs"]) != retained_releases:
        raise AssertionError("retained release refs did not rebuild exactly")
    return case


def provide(case: dict[str, Any], rule: Any) -> Any:
    """Invoke the accepted N10E provider seam on exact determinants only."""

    return provide_empirical_possibility_slice(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=rule,
        condition_binding_witness=case["condition_binding_witness"],
    )


def _producer_fact(produced: Any) -> Any:
    composition = produced.composition_result
    facts = tuple(composition.producer_result.facts)
    matches = tuple(fact for fact in facts if fact.ref == composition.producer_fact_ref)
    if len(matches) != 1:
        raise AssertionError("provider composition did not resolve exactly one producer EmpiricalFact")
    return matches[0]


def _complete_determinant_census(
    case: dict[str, Any], produced: Any
) -> tuple[tuple[Any, ...], tuple[ExactDeterminantOwnership, ...], Any]:
    """Immediate consumed boundary plus authenticated owner evidence for every exact ref."""

    query = case["empirical_query"]
    predicate = case["predicate"]
    consumer_query = case["consumer_query"]
    witness = case["condition_binding_witness"]
    binding = case["conditioner_binding"]
    universe = case["source"]["universe"]
    fact = _producer_fact(produced)

    owned = (
        ExactDeterminantOwnership(
            determinant_ref=query.ref,
            root_class=DETERMINANT_ROOT_AUTHORITY,
            owning_authority_refs=tuple(query.authority_snapshot_refs),
            owner_evidence=DeterminantOwnerEvidence(
                query.ref,
                query.semantic_projection(),
                ("authority_snapshot_refs",),
                tuple(query.authority_snapshot_refs),
            ),
        ),
        ExactDeterminantOwnership(
            determinant_ref=predicate.ref,
            root_class=DETERMINANT_ROOT_AUTHORITY,
            owning_authority_refs=tuple(predicate.authority_snapshot_refs),
            owner_evidence=DeterminantOwnerEvidence(
                predicate.ref,
                predicate.semantic_projection(),
                ("authority_snapshot_refs",),
                tuple(predicate.authority_snapshot_refs),
            ),
        ),
        ExactDeterminantOwnership(
            determinant_ref=consumer_query.ref,
            root_class=DETERMINANT_ROOT_AUTHORITY,
            owning_authority_refs=(binding.comparability_authority_ref,),
            owner_evidence=DeterminantOwnerEvidence(
                consumer_query.ref,
                consumer_query.material(),
                ("conditioner_bindings.0.comparability_authority_ref",),
                (binding.comparability_authority_ref,),
            ),
        ),
        ExactDeterminantOwnership(
            determinant_ref=witness.witness_ref,
            root_class=DETERMINANT_ROOT_AUTHORITY,
            owning_authority_refs=tuple(witness.pairing_authority_refs),
            owner_evidence=DeterminantOwnerEvidence(
                witness.witness_ref,
                witness.identity_material,
                ("pairing_authority_ref",),
                tuple(witness.pairing_authority_refs),
            ),
        ),
        ExactDeterminantOwnership(
            determinant_ref=universe.ref,
            root_class=DETERMINANT_ROOT_AUTHORITY,
            owning_authority_refs=tuple(universe.authority_snapshot_refs),
            owner_evidence=DeterminantOwnerEvidence(
                universe.ref,
                universe.semantic_projection(),
                ("authority_snapshot_refs",),
                tuple(universe.authority_snapshot_refs),
            ),
        ),
        ExactDeterminantOwnership(
            determinant_ref=fact.ref,
            root_class=DETERMINANT_DEPENDENT_PRODUCT,
            owning_authority_refs=tuple(fact.authority_snapshot_refs),
            owner_evidence=DeterminantOwnerEvidence(
                fact.ref,
                fact.semantic_projection(),
                ("authority_snapshot_refs",),
                tuple(fact.authority_snapshot_refs),
            ),
            reason="upstream EmpiricalFact is a governed exact product",
        ),
        ExactDeterminantOwnership(
            determinant_ref=case["release_refs"][0],
            root_class=DETERMINANT_UNOWNED,
            lifecycle_relevant=False,
            reason="C11LogicalRelease has no current lifecycle AuthorityRef owner",
        ),
        ExactDeterminantOwnership(
            determinant_ref=consumer_query.target_ref,
            root_class=DETERMINANT_IMMUTABLE_IDENTITY,
            lifecycle_relevant=False,
            reason="QUESTION_NATIVE target is immutable request identity at this grain",
        ),
        ExactDeterminantOwnership(
            determinant_ref=binding.subject_fact_ref,
            root_class=DETERMINANT_IMMUTABLE_IDENTITY,
            lifecycle_relevant=False,
            reason="subject-condition preimage is immutable exact binding identity",
        ),
        ExactDeterminantOwnership(
            determinant_ref=binding.empirical_coordinate_ref,
            root_class=DETERMINANT_IMMUTABLE_IDENTITY,
            lifecycle_relevant=False,
            reason="empirical coordinate is immutable exact binding identity at this grain",
        ),
    )
    by_key = {row.determinant_ref.key: row for row in owned}
    refs = tuple(sorted((row.determinant_ref for row in by_key.values()), key=lambda ref: ref.key))
    ownerships = tuple(by_key[ref.key] for ref in refs)
    return refs, ownerships, fact


def run(determinants: dict[str, Any]) -> dict[str, Any]:
    """Execute the whole provider -> consumer -> dependency/lifecycle/replay chain."""

    case = rebuild_case(determinants)
    base_rule = case["model_rule"]
    old_model = base_rule.model_authority_ref

    # ---- 1. fresh-process provider recomputation -> named consumer ----------
    produced = provide(case, base_rule)
    if produced.provider_state != "EXACT_SUPPORTED_SLICE_PRODUCED":
        raise AssertionError(
            f"fresh recomputation did not reach the positive provider path: "
            f"{produced.provider_state!r} / {produced.refusal_state!r}"
        )
    evidence = produced.generated_evidence_or_null
    consumer = produced.consumer_result_or_null

    product_ref = exact_ref(
        {
            "kind": PRODUCT_KIND,
            "object_id": PRODUCT_OBJECT_ID,
            "content_hash": produced.result_identity_hash,
        },
        "product_ref",
    )

    # ---- 2. dependency registration over the determinants actually consumed --
    exact_refs, ownerships, producer_fact = _complete_determinant_census(case, produced)
    registry = AnalyticalDependencyRegistry()
    registry.register(
        AnalyticalProductRegistration(
            product_ref=product_ref,
            product_identity_hash=produced.result_identity_hash,
            determinant_authority_refs=(old_model,),
            determinant_exact_refs=exact_refs,
            determinant_ownerships=ownerships,
        )
    )
    # Lifecycle closure is requested here, so any omitted classification fails now.
    graph = registry.build_graph()

    # ---- 3. accepted lifecycle owner performs the dependency transition -----
    transition = _stage_transition(case, registry, product_ref, old_model)
    successor = transition["successor"]

    def recompose(affected_ref, authority):
        rule = PositionedSubjectPossibilityModelRule(
            authority,
            base_rule.walkback_authority_ref,
            base_rule.source_universe_refs,
            base_rule.walkback_steps,
            base_rule.positive_proxy_authority_refs,
        )
        recomposed = provide(case, rule)
        if recomposed.provider_state != "EXACT_SUPPORTED_SLICE_PRODUCED":
            raise AssertionError(
                "recomposition under the successor authority left the positive path"
            )
        return exact_ref(
            {
                "kind": affected_ref.kind,
                "object_id": affected_ref.object_id,
                "content_hash": recomposed.result_identity_hash,
            },
            "recomposed_ref",
        )

    outcome = transition_analytical_dependencies(
        executor=transition["executor"],
        registry=registry,
        seal_ref=transition["seal_ref"],
        selection_rule_ref=transition["selection_rule_ref"],
        selection_attestation_ref=transition["selection_attestation_ref"],
        recompose={product_ref.key: recompose},
    )
    receipt = outcome.invalidation_receipt

    # ---- 4. currentness resolution through the lifecycle owner --------------
    status = resolve_current_analytical_product(
        executor=transition["executor"], dependent_ref=product_ref
    )

    return {
        "provider_state": produced.provider_state,
        "provider_route": produced.provider_receipt.provider_route,
        "receipt_ref_hash": produced.provider_receipt.receipt_hash,
        "product_identity_hash": produced.result_identity_hash,
        "composed_result_identity_hash": (
            produced.composition_result.composed_result_identity_hash
        ),
        "evidence_ref_or_null": evidence.evidence_ref.as_dict(),
        "evidence_identity_is_producer_derived": (
            produced.provider_receipt.generated_evidence_identity_is_producer_derived
        ),
        "consumer_result_hash_or_null": consumer.result_hash,
        "consumer_result_state_or_null": consumer.result_state,
        "consumer_path": CONSUMER_PATH,
        "producer_path": PRODUCER_PATH,
        "provider_path": PROVIDER_PATH,
        "product_ref": product_ref.as_dict(),
        "registered_determinant_authority_refs": [
            a.as_dict() for a in (old_model,)
        ],
        "registered_determinant_exact_refs": [x.as_dict() for x in exact_refs],
        "registered_determinant_classifications": [
            {
                "ref": row.determinant_ref.as_dict(),
                "root_class": row.root_class,
                "lifecycle_relevant": row.lifecycle_relevant,
                "owning_authority_refs": [
                    authority.as_dict() for authority in row.owning_authority_refs
                ],
            }
            for row in ownerships
        ],
        "producer_fact_ref": producer_fact.ref.as_dict(),
        "graph_affected": [x.as_dict() for x in receipt.affected_dependent_refs],
        "graph_unaffected": [
            x.as_dict() for x in receipt.unaffected_dependent_refs
        ],
        "recomposition_pairs": [
            {"old_ref": o.as_dict(), "new_ref": n.as_dict()}
            for o, n in receipt.recompilation_pairs
        ],
        "noncurrent_dependents": [
            row.as_dict() for row in receipt.noncurrent_dependents
        ],
        "lifecycle_state": status["lifecycle_state"],
        "current_replacement_ref_or_null": (
            None
            if status.get("current_replacement_ref") is None
            else status["current_replacement_ref"].as_dict()
        ),
        "successor_authority_ref": successor.as_dict(),
        "raw_denominator_support": (
            produced.composition_result.raw_denominator_support
        ),
        "cell_numerators": {
            cell["cell"]: cell["raw_numerator_support"]
            for cell in evidence.geometry["cells"]
        },
    }


def _stage_transition(
    case: dict[str, Any],
    registry: AnalyticalDependencyRegistry,
    product_ref: Any,
    old_model: Any,
) -> dict[str, Any]:
    """Stage one governed model-authority revision around the provider product.

    The determinant graph binds exactly the one authority the provider product
    consumed. The revised successor is minted and adjudicated through the accepted
    owner's own candidate -> APPROVED -> seal ceremony; no successor is invented here.
    """

    from rawlsing_next.pre553_authority_maintenance import (
        AuthorityEvidenceReceipt,
        AuthorityMaintenanceExecutor,
        SemanticDeterminantGraph,
    )

    direction = case["direction"]
    graph = registry.build_graph()
    executor = AuthorityMaintenanceExecutor(
        initial_snapshots=(fx.model_authority_snapshot(direction),),
        initial_current_selection={old_model.authority_id: old_model},
        determinant_graph=graph,
    )
    evidence = AuthorityEvidenceReceipt(
        evidence_role="SEMANTIC_AUTHORITY_EVIDENCE",
        evidence_refs=(fx._ref_for("EVIDENCE", f"hq221-{direction}-model"),),
        provenance_refs=(fx._ref_for("PROVENANCE", f"hq221-{direction}-model"),),
        source_release_refs=(),
    )
    executor.intake_evidence(evidence)
    revision = fx._model_candidate(
        fx.revised_model_authority(direction),
        version="2.0.0",
        evidence_ref=evidence.ref,
        parent=(old_model,),
        supersession=(old_model,),
        semantics=f"{direction}-hq221-v2",
    )
    executor.intake_candidate(revision)
    adjudication = executor.adjudicate_candidate(
        revision.ref,
        decision="APPROVED",
        adjudicator_ref=fx._ref_for("ADJUDICATOR", f"hq221-{direction}-v2"),
        adjudication_authority_ref=fx._ref_for("GOVERNING_AUTHORITY", "HQ221"),
        findings_ref=fx._ref_for("FINDINGS", f"hq221-{direction}-v2"),
    )
    seal = executor.seal_revision(
        revision.ref,
        adjudication.ref,
        seal_attestation_ref=fx._ref_for("SEAL_ATTESTATION", f"hq221-{direction}-v2"),
    )
    successor = revision.proposed_authority_ref
    if successor.authority_content_hash == old_model.authority_content_hash:
        raise AssertionError(
            "the sealed successor must differ in content hash from the consumed prior"
        )
    return {
        "executor": executor,
        "seal_ref": seal.ref,
        "successor": successor,
        "selection_rule_ref": fx._ref_for("SELECTION_RULE", f"hq221-{direction}-v2"),
        "selection_attestation_ref": fx._ref_for(
            "SELECTION_ATTESTATION", f"hq221-{direction}-v2"
        ),
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: runner <retained_determinants.json> [--expect <oracle.json>]",
              file=sys.stderr)
        return 2
    determinants = json.loads(Path(argv[1]).read_text(encoding="utf-8"))

    # Fail closed if the input artifact ever carries an expected answer.
    assert_runner_input_carries_no_answer(determinants)

    payload = run(determinants)

    # Optional oracle-side equality check. This happens strictly AFTER the
    # identities above were computed in this process; it cannot produce them.
    if "--expect" in argv:
        expected = json.loads(Path(argv[argv.index("--expect") + 1]).read_text(
            encoding="utf-8"
        ))
        mismatches = sorted(
            key
            for key, want in expected.items()
            if key in payload and payload[key] != want
        )
        if mismatches:
            print(
                "fresh recomputation disagreed with the oracle on: "
                f"{mismatches}",
                file=sys.stderr,
            )
            return 3
        payload["oracle_agreement"] = True

    sys.stdout.write(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))