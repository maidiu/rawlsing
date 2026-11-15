"""Independent G5 multi-release source-ownership falsifier for PYAT960 S2-G.

Builds one S2-F closure containing release A facts and a receipt whose declared
source-release subset also names a second real release B, then builds an
M1/M2/B5 product from the release-A facts while the cold consumer query is bound
to release B.  The question is whether the existing actual world consumer
refuses the release mismatch or silently serves a product whose determinant
source release is not the source release of the selected fact.

This is a review harness only; it writes to the caller's private proofroot.
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import sys

import rawlsing_next.pre553_learned_empirical_adjudication as m1
import rawlsing_next.pre553_learned_world_composition as i4
from rawlsing_next.pre553_analytical_composition import (
    _validate_discovery_consumption,
    compose_positioned_subject_possibility,
)
from rawlsing_next.pre553_discovery_exact import ExactBoundedDiscoveryResult
from rawlsing_next.pre553_durable_empirical_closure import (
    NativeEmpiricalOutput,
    ReleaseIdentity,
    _final_replay_material,
    _receipt_replay_material,
    open_empirical_closure,
    publish_empirical_closure,
)
from rawlsing_next.pre553_durable_learned_lifecycle import (
    DurableLearnedLifecycleRefusal,
    LearnedConsumerDeterminants,
    open_learned_lifecycle,
    publish_learned_lifecycle,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    DiscoveryResultReceipt,
    ExactRef,
    canonical_json,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleExecutor
from rawlsing_next.pre553_learned_product_release import M2Repository
from rawlsing_next.pre553_route_b_production import RouteBEmpiricalObjectGraph
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import _registry
from rawlsing_next.tests.test_pre553_route_b_production import (
    _execute as execute_m01,
    _fixture as m01_fixture,
)
from rawlsing_next.tests.test_pyat960_s2g_durable_lifecycle import _artifact_case


def _identity(release) -> ReleaseIdentity:
    return ReleaseIdentity(
        release_ref=release.release_ref,
        replay_ref=release.replay_manifest.ref,
        source_artifact_ref=release.source_artifact_ref,
        source_release_manifest_hash=release.source_release_manifest_hash,
        semantic_release_hash=release.semantic_release_hash,
    )


def _multi_release_closure(tmp_path: Path, base: dict):
    base_result = base["result"]
    base_release = base_result.c11_release
    second_fixture = m01_fixture(missing_weight=True)
    second_result = execute_m01(second_fixture)
    second_release = second_result.c11_release
    assert second_release.release_ref != base_release.release_ref

    receipt = base["receipt"]
    release_refs = (base_release.release_ref, second_release.release_ref)
    fields = dict(receipt.semantic_fields)
    fields["source_release_refs"] = release_refs
    fields["replay_ref"] = ExactRef("TMP", "urn:test:multi-release-tmp", "0" * 64)
    temporary = DiscoveryResultReceipt(
        typed_state=receipt.typed_state,
        authority_snapshot_refs=receipt.authority_snapshot_refs,
        dependency_refs=receipt.dependency_refs,
        producer_replay_locator_or_reference_root=fields["replay_ref"],
        **fields,
    )
    receipt_digest = semantic_hash(_receipt_replay_material(temporary, release_refs))
    new_receipt_replay = ExactRef(
        "PRE553_I05_DISCOVERY_REPLAY",
        f"urn:rawlsing:pre553:i05:candidate-replay:sha256:{receipt_digest}",
        receipt_digest,
    )
    fields["replay_ref"] = new_receipt_replay
    receipt_v2 = DiscoveryResultReceipt(
        typed_state=receipt.typed_state,
        authority_snapshot_refs=receipt.authority_snapshot_refs,
        dependency_refs=receipt.dependency_refs,
        producer_replay_locator_or_reference_root=new_receipt_replay,
        **fields,
    )
    i05 = base_result.i05_result
    temporary_i05 = replace(
        i05,
        receipts=(receipt_v2,),
        replay_ref=ExactRef("TMP2", "urn:test:multi-release-final-tmp", "0" * 64),
    )
    final_digest = semantic_hash(_final_replay_material(temporary_i05))
    final_ref = ExactRef(
        "PRE553_I05_FRONTIER_REPLAY",
        f"urn:rawlsing:pre553:i05:frontier-replay:sha256:{final_digest}",
        final_digest,
    )
    i05_v2 = replace(i05, receipts=(receipt_v2,), replay_ref=final_ref)
    graph_v2 = replace(
        base_result.object_graph, discovery_receipts=(receipt_v2,)
    )
    base_identity = NativeEmpiricalOutput.from_route_b_result(base_result)
    output = NativeEmpiricalOutput(
        source_identity=base_identity.source_identity,
        release_identities=(_identity(base_release), _identity(second_release)),
        i03_results=base_result.i03_results,
        i05_result=i05_v2,
        object_graph=graph_v2,
    )
    receipt = publish_empirical_closure(output, tmp_path / "multi-s2f")
    closure = open_empirical_closure(
        receipt.root_path, expected_root=receipt.root_identity
    ).require_trusted()
    return {
        "receipt": receipt,
        "closure": closure,
        "i05": i05_v2,
        "receipt_v2": receipt_v2,
        "base_release": base_release,
        "second_release": second_release,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        raise SystemExit("usage: repro_multirelease.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    proofroot.mkdir(parents=True, exist_ok=True)
    base = _artifact_case(proofroot / "base")
    base_consumed = base["artifact"].consume(base["s2f_receipt"].root_path)
    if base_consumed.state != "LEARNED_CONSUMER_EXACT_SUPPORTED":
        raise SystemExit(f"base positive control not supported: {base_consumed.state}")
    multi = _multi_release_closure(proofroot, base)
    receipt_v2 = multi["receipt_v2"]
    release_b = multi["second_release"].release_ref
    release_a = multi["base_release"].release_ref

    base_consumer = base["consumer"]
    conditioner_a = base_consumer.conditioner_bindings[0]
    conditioner_b = replace(conditioner_a, release_ref=release_b)
    consumer_b = replace(
        base_consumer,
        release_ref=release_b,
        conditioner_bindings=(conditioner_b,),
    )
    fact, predicate, query = _validate_discovery_consumption(
        discovery_result=multi["i05"],
        consumer_query=consumer_b,
        receipt_ref=receipt_v2.ref,
    )
    witness_b = fx.build_witness_for_binding(
        witness_object_id="urn:test:s2g:g5:multi-release-witness",
        consumer_query=consumer_b,
        producer_query=query,
        producer_predicate=predicate,
        bindings=[conditioner_b],
        coordinate_value_pairs=[(base["m01"]["qrefs"]["X"], 1)],
        pairing_authority=conditioner_b.comparability_authority_ref,
        source_universe_ref=base["m01"]["projection"].universes[0].ref,
        release_ref=release_b,
    )
    composition = compose_positioned_subject_possibility(
        repository=None,
        empirical_query=query,
        predicate=predicate,
        authority_registry=base["case"]["registry"],
        release_refs=(release_b,),
        consumer_query=consumer_b,
        model_rule=base["model"],
        condition_binding_witness=witness_b,
        discovery_result=multi["i05"],
        discovery_receipt_ref=receipt_v2.ref,
    )
    if composition.analytical_state != "SUPPORTED":
        raise SystemExit(f"multi-release composition not supported: {composition.analytical_state}")

    bundle = m1.build_m1_adjudication_input_bundle(
        requested_claim_family_id=base["m1_bundle"].requested_claim_family_id,
        requested_claim_rule_id=base["m1_bundle"].requested_claim_rule_id,
        selected_discovery_receipts=(receipt_v2,),
        discovery_authority_catalog=base["result"].object_graph.discovery_authorities,
        empirical_fact_catalog=base["result"].object_graph.empirical_facts,
        empirical_query_catalog=base["result"].object_graph.executed_queries,
        empirical_predicate_catalog=base["result"].object_graph.executed_predicates,
        authority_snapshots=base["m1_bundle"].authority_snapshots,
        requested_scope=base["m1_bundle"].requested_scope,
        prerequisite_channels=(),
        additional_dependency_refs=(release_b,),
    )
    disposition = m1.adjudicate_learned_empirical(
        bundle, base["binding"], validator_registry=_registry(base["binding"])
    )
    if disposition.adjudication_outcome != "RULE_SATISFIED":
        raise SystemExit(f"multi-release M1 not satisfied: {disposition.adjudication_outcome}")
    executor = LearnedProductLifecycleExecutor()
    learned = i4.compose_learned_world(
        base["contract"],
        m2_repository=M2Repository(),
        lifecycle_executor=executor,
        m1_disposition=disposition,
    )
    if learned.receipt.terminal_state != "RULE_SATISFIED":
        raise SystemExit(f"multi-release M2/B5 not satisfied: {learned.receipt.terminal_state}")
    determinants = LearnedConsumerDeterminants(
        s2f_root_identity=multi["closure"].root_identity,
        discovery_receipt_ref=receipt_v2.ref,
        producer_query_ref=query.ref,
        producer_predicate_ref=predicate.ref,
        release_ref=release_b,
        consumer_query=consumer_b,
        model_rule=base["model"],
        condition_binding_witness=witness_b,
        expected_composition_identity=composition.composed_result_identity_hash,
        expected_consumer_result_hash=(
            None
            if composition.consumer_result_or_null is None
            else composition.consumer_result_or_null.result_hash
        ),
        purpose_ref=base["contract"].consumer_product_purpose_ref,
    )
    published = publish_learned_lifecycle(
        proofroot / "multi-learned",
        learned=learned,
        executor=executor,
        determinants=determinants,
        m1_input_bundle=bundle.as_dict(),
        m1_family_rule_binding=base["binding"].as_dict(),
    )
    artifact = open_learned_lifecycle(
        published.artifact_path, expected_root=published.root_identity
    ).require_trusted()
    try:
        consumed = artifact.consume(multi["closure"].root_path)
        outcome = {
            "consumer_state": consumed.state,
            "reason_code": consumed.reason_code,
            "consumer_result_hash": consumed.consumer_result_hash,
            "composition_identity": consumed.composition_identity,
            "accepted": consumed.state == "LEARNED_CONSUMER_EXACT_SUPPORTED",
        }
    except DurableLearnedLifecycleRefusal as exc:
        outcome = {
            "consumer_state": "REFUSED",
            "reason_code": str(exc),
            "consumer_result_hash": None,
            "composition_identity": None,
            "accepted": False,
        }

    evidence = {
        "base_positive_control": {
            "consumer_state": base_consumed.state,
            "consumer_result_hash": base_consumed.consumer_result_hash,
            "s2f_root_identity": base["s2f_receipt"].root_identity,
            "artifact_root_identity": base["published"].root_identity,
        },
        "base_release": release_a.as_dict(),
        "second_release": release_b.as_dict(),
        "selected_fact_ref": fact.ref.as_dict(),
        "selected_fact_release_provenance": [
            exact_ref(dict(ref)).as_dict()
            for ref in fact.source_empirical_provenance_refs
            if dict(ref).get("kind") == "C11LogicalRelease"
        ],
        "receipt_declared_releases": [
            exact_ref(dict(ref)).as_dict() for ref in receipt_v2.source_release_refs
        ],
        "consumer_determinant_release": release_b.as_dict(),
        "s2f_root_identity": multi["closure"].root_identity,
        "artifact_root_identity": published.root_identity,
        "m1_disposition_ref": disposition.ref.as_dict(),
        "m2_release_ref": learned.m2_artifacts.release.ref.as_dict(),
        "b5_selection_ref": None
        if learned.b5_selection_receipt is None
        else learned.b5_selection_receipt.ref.as_dict(),
        "outcome": outcome,
        "defect_if_accepted": outcome["accepted"],
    }
    out = proofroot / "multirelease_evidence.json"
    out.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if not outcome["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
