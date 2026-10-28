"""Read-only bridge from issued native observed facts into accepted Lane D.

The accepted Lane D consumer is an external read-only dependency.  This module
does not copy or modify it: when the joined tree provides
``campaign_src04_completion.consumers.consumer``, this bridge constructs the
exact ProducerBundle and calls its existing ``consume_native_producer`` owner.
Without that dependency, it returns a precise pending-dependency record.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from campaign_src04_completion.empirical.authorized_execution import (
    TARGET_USE_REF,
    AuthorizedExecutionRefusal,
    HumanGrant,
    IssuedExecution,
)
from campaign_src04_completion.empirical.native_workload import NativeWorkload
from rawlsing_next.pre553_discovery_exact import CANDIDATE_GRAMMAR_SCHEMA
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    DiscoveryAuthority,
    EmpiricalFact,
    ExactRef,
    semantic_hash,
)


@dataclass(frozen=True)
class ConsumerBridgeResult:
    status: str
    product: Mapping[str, Any] | None
    detail: str


def _discovery_snapshot(grant: HumanGrant, issued: IssuedExecution) -> AuthoritySnapshot:
    material = {
        "authority_id": "SRC04-USER-EMPIRICAL-DISCOVERY",
        "kind": "DISCOVERY_FRONTIER",
        "operation": "SOURCE_LOCAL_OBSERVED_DISCOVERY@1.0.0",
        "source_sha256": grant.sha256,
        "release_ref": issued.release.release_ref.as_dict(),
        "universe_ref": issued.contract.universe_ref.as_dict() if issued.contract.universe_ref else None,
        "risk_set_ref": issued.contract.risk_set_ref.as_dict(),
    }
    digest = semantic_hash(material)
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(grant.ref,),
        producer_replay_locator_or_reference_root=ExactRef(
            "REPLAY_ROOT", f"urn:rawlsing:user-grant-replay:discovery:{digest}", digest),
        authority_id="SRC04-USER-EMPIRICAL-DISCOVERY",
        authority_version="1.0.0",
        authority_content_hash=digest,
        authority_kind="DISCOVERY_FRONTIER",
        decision_state="ALLOW",
        governed_operations=("SOURCE_LOCAL_OBSERVED_DISCOVERY@1.0.0",),
        governed_object_families=("DiscoveryAuthority@1.0.0", "DiscoveryResultReceipt@1.0.0"),
        scope_envelope={
            "source_universe_refs": [issued.contract.universe_ref.as_dict()],
            "predicate_or_risk_set_refs": [issued.contract.risk_set_ref.as_dict()],
            "release_ref": issued.release.release_ref.as_dict(),
            "source_artifact_ref": issued.release.source_artifact_ref.as_dict(),
            "source_release_manifest_hash": issued.release.source_release_manifest_hash,
            "source_id": "SRC04",
            "source_sha256": grant.document["source_sha256"],
            "grant_sha256": grant.sha256,
            "fixture_only": False,
            "grade": "USER_EMPIRICAL_GRANT",
            "canonical_adoption": "DENY",
            "target_use_refs": [TARGET_USE_REF.as_dict()],
        },
        effective_time_or_interval="2026-10-28/USER_EMPIRICAL_GRANT",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=digest,
        replay_protocol_ref=ExactRef(
            "REPLAY_PROTOCOL", f"urn:rawlsing:user-grant-replay-protocol:discovery", digest),
    )


def _select_base_and_condition(workload: NativeWorkload):
    base = next((op for op in workload.operations
                 if op.family == "UNARY_OBSERVED_DISTRIBUTION"
                 and op.status == "EXECUTED" and op.fact_state == "SUPPORTED"
                 and op.query is not None and op.predicate is not None), None)
    if base is None:
        raise AuthorizedExecutionRefusal("NO_SUPPORTED_UNARY_FACT_FOR_CONSUMER")
    condition = next((op for op in workload.operations
                      if op.family == "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION"
                      and op.status == "EXECUTED" and op.fact_state == "SUPPORTED"
                      and op.query is not None and op.predicate is not None
                      and op.operation_id != base.operation_id), None)
    if condition is None:
        raise AuthorizedExecutionRefusal("NO_SUPPORTED_CONDITIONAL_FACT_FOR_DISCOVERY")
    return base, condition


def consume_with_lane_d(
    *,
    grant: HumanGrant,
    issued: IssuedExecution,
    workload: NativeWorkload,
) -> ConsumerBridgeResult:
    try:
        from campaign_src04_completion.consumers.consumer import (  # type: ignore[import-not-found]
            DiscoveryConsumer,
            ProducerBundle,
            ProducerContract,
            consume_native_producer,
        )
    except Exception as exc:
        return ConsumerBridgeResult(
            status="D_CONSUMER_DEPENDENCY_NOT_JOINED",
            product=None,
            detail=f"{type(exc).__name__}: {exc}",
        )
    base, condition = _select_base_and_condition(workload)
    if base.fact_ref is None:
        raise AuthorizedExecutionRefusal("BASE_FACT_REF_MISSING")
    snapshot = _discovery_snapshot(grant, issued)
    grammar = {
        "schema": CANDIDATE_GRAMMAR_SCHEMA,
        "discovery_operation": "SOURCE_LOCAL_OBSERVED_DISCOVERY@1.0.0",
        "atoms": (
            {"atom_id": "BASELINE", "predicate_ref": base.predicate.ref.as_dict(),
             "kind": "BRANCH", "ancestry_refs": ()},
            {"atom_id": "CONDITION", "predicate_ref": condition.predicate.ref.as_dict(),
             "kind": "RESPONSE", "ancestry_refs": ()},
        ),
        "query_templates": ({"template_id": "BASE_QUERY", "query_ref": base.query.ref.as_dict()},),
        "rules": (
            {"rule_id": "source_local_conditioned_distribution",
             "family": "BRANCH_CONDITIONED_DISTRIBUTION",
             "form": "SINGLE_ATOM", "atom_ids": ("CONDITION",),
             "baseline_atom_id": "BASELINE", "query_template_id": "BASE_QUERY",
             "validation": {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"}},
        ),
        "limits": {"maximum_conditioner_arity_K": 1, "maximum_target_arity_J": 1},
        "allow_empty_frontier": False,
    }
    grammar_ref = ExactRef(
        "PRE553_I05_CANDIDATE_GRAMMAR",
        f"urn:rawlsing:src04:source-local-observed:grammar:{semantic_hash(grammar)}",
        semantic_hash(grammar),
    )
    discovery_authority = DiscoveryAuthority(
        typed_state="EXACT_BOUNDED_AUTHORIZED",
        authority_snapshot_refs=(snapshot.authority_ref,),
        dependency_refs=(grant.ref, issued.contract.ref),
        producer_replay_locator_or_reference_root=ExactRef(
            "REPLAY_ROOT", "urn:rawlsing:src04:source-local-observed:discovery", semantic_hash(grammar)),
        candidate_grammar_ref=grammar_ref,
        candidate_universe_definition=grammar,
        source_universe_scope={"allowed_universe_refs": (issued.contract.universe_ref,)},
        risk_set_scope={"allowed_risk_set_refs": (issued.contract.risk_set_ref,)},
        topology_scope={"maximum_target_arity_J": 1},
        measure_scope={"allowed_measure_kinds": ("RAW",)},
        support_rules={"minimum_raw_denominator": 1},
        validation_rules={"kinds": ("DISTRIBUTION_DIFFERS_FROM_BASELINE",)},
        coverage_claim="COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
        pruning_contract={"kind": "NONE_EXACT_EVALUATE_ALL"},
        algorithm_identity_if_semantically_required="PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0",
        tie_order_rules="CANONICAL_CANDIDATE_HASH_ORDER",
        rng_policy_if_any="NONE",
        mode="EXACT_BOUNDED",
        candidate_scoring_or_ranking_rule_if_any={"kind": "NONE", "controls_frontier": False},
    )
    discovery = DiscoveryConsumer(
        authority=discovery_authority,
        authority_snapshot=snapshot,
        predicate_catalog=(base.predicate, condition.predicate),
        query_template_catalog=(base.query,),
        scope="SRC04_SOURCE_LOCAL_OBSERVED_RESPONSE",
    )
    contract = ProducerContract(
        source_id="SRC04",
        source_sha256=grant.document["source_sha256"],
        source_rows=int(grant.document.get("scope", {}).get("source_records", 7337)),
        release_ref=issued.release.release_ref,
        query_ref=base.query.ref,
        predicate_ref=base.predicate.ref,
        fact_ref=base.fact_ref,
        producer_family=(
            "C11LogicalRelease", "EmpiricalQuerySpec@1.0.0",
            "EmpiricalPredicate@1.0.0", "EmpiricalFact@1.0.0",
        ),
        evidence_tier="SOURCE_LOCAL_CERTIFIED",
        claim_ceiling="SOURCE_LOCAL_STATISTIC",
        use_scopes=("SOURCE_LOCAL_STATISTIC",),
        native_authority_refs=tuple(base.query.authority_snapshot_refs),
        fixture_only=False,
    )
    registry = AuthorityRegistry((*issued.authorities, snapshot))
    bundle = ProducerBundle(
        release=issued.release,
        query=base.query,
        predicate=base.predicate,
        repository=issued.repository,
        authority_registry=registry,
        contract=contract,
        discovery=discovery,
    )
    product = consume_native_producer(
        bundle,
        expected_source_id="SRC04",
        requested_claim_ceiling="SOURCE_LOCAL_STATISTIC",
        use_scope="SOURCE_LOCAL_STATISTIC",
    )
    return ConsumerBridgeResult(status=product["status"], product=product, detail=product["downstream_value_effect"])


__all__ = ["ConsumerBridgeResult", "consume_with_lane_d"]
