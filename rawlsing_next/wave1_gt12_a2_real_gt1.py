"""GT12 Closure A2 exact real GT1 execution binding.

This module consumes only the already sealed A1 C11 release and current GT12-B
I03 adapter.  It mints the two claim-scoped execution authorities that must be
bound after the exact empirical-universe identity exists, then executes/replays
GT1 without structural, actor, V3, V2, FIELD FORGE, or GT2 promotion.
"""
from __future__ import annotations

from dataclasses import dataclass

from rawlsing_next.pre553_c11_repository import C11LogicalRelease
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    EmpiricalUniverse,
    semantic_hash,
)
from rawlsing_next.wave1_r5_q86_c11_projection import (
    CURRENTNESS_REF,
    FROZEN_BINDINGS,
    GT1_TARGET_USE_REF,
    GT2_TARGET_USE_REF,
    Q86_NATIVE_STATES,
    REPLAY_PROTOCOL_REF,
    question_ref,
    target_domain_replay_ref,
)
from rawlsing_next.wave1_gt12_i03_positive_facts import (
    ExactTargetUseBinding,
    FROZEN_Q86A_QIMPL,
    FROZEN_Q86A_SOURCE_STRUCTURE,
    FROZEN_Q86B_QIMPL,
    FROZEN_RISK_MEMBER_SET_SHA256,
    FROZEN_RISK_SET_ID,
    FROZEN_RISK_SET_MEMBER_COUNT,
    GT1_CLAIM_ID,
    GT1_TARGET_USE_CEILING,
    GT2_CLAIM_ID,
    GT12BI03BindingError,
    GT12BI03Execution,
    R5Q86I03ExecutionBinding,
    R5Q86TargetBinding,
    build_gt1_q86a_i03_plan,
    execute_gt12b_i03_plan,
    replay_gt12b_i03_execution,
)

A1_RELEASE_ID = "R5_GT12_Q86A_Q86B_FROZEN"
A1_RELEASE_HASH = "8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295"
A1_REPLAY_HASH = "c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa"
A2_AUTHORITY_LAW = "GT12_CLOSURE_A2_REAL_GT1_CLAIM_SCOPED_AUTHORITY@1"
A2_QUERY_AUTHORITY_ID = "GT12-A2-R5-Q86A-I03-PREDICATE-GRAMMAR"
A2_TARGET_USE_AUTHORITY_ID = "GT12-A2-R5-Q86A-GT1-TARGET-USE"


@dataclass(frozen=True)
class A2GT1Context:
    release: C11LogicalRelease
    empirical_universe: EmpiricalUniverse
    binding: R5Q86I03ExecutionBinding
    authority_registry: AuthorityRegistry
    query_authority: AuthoritySnapshot
    target_use_authority: AuthoritySnapshot


@dataclass(frozen=True)
class A2GT1Result:
    context: A2GT1Context
    execution: GT12BI03Execution
    replay_result: object


def _dref(kind: str, object_id: str, material: object) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, object_id, digest)


def _one_public(release: C11LogicalRelease, *, cls=None, authority_id: str | None = None):
    matches = []
    for obj in release.public_objects:
        if cls is not None and not isinstance(obj, cls):
            continue
        if authority_id is not None and getattr(obj, "authority_id", None) != authority_id:
            continue
        matches.append(obj)
    if len(matches) != 1:
        name = authority_id or getattr(cls, "__name__", "public object")
        raise GT12BI03BindingError(f"A2 requires exactly one {name} in sealed A1 release")
    return matches[0]


def _claim_authority(
    *,
    release: C11LogicalRelease,
    universe: EmpiricalUniverse,
    authority_id: str,
    authority_kind: str,
    object_families: tuple[str, ...],
    target_use_ref: ExactRef | None = None,
) -> AuthoritySnapshot:
    scope = {
        "source_universe_refs": (universe.ref,),
        "predicate_or_risk_set_refs": (FROZEN_BINDINGS.risk_ref,),
    }
    if target_use_ref is not None:
        scope["target_use_refs"] = (target_use_ref,)
    material = {
        "law": A2_AUTHORITY_LAW,
        "frozen_contract_commit": "a9416094cbb4653dd2de2e4aa7b67577a355560c",
        "claim_id": GT1_CLAIM_ID,
        "release_ref": release.release_ref,
        "source_ref": release.source_artifact_ref,
        "empirical_universe_ref": universe.ref,
        "risk_set_ref": FROZEN_BINDINGS.risk_ref,
        "authority_id": authority_id,
        "authority_kind": authority_kind,
        "operation": GT1_CLAIM_ID,
        "families": object_families,
        "scope": scope,
        "permission_ceiling": GT1_TARGET_USE_CEILING if target_use_ref is not None else None,
        "currentness_ref": CURRENTNESS_REF,
    }
    authority_content_hash = semantic_hash(material)
    replay_root = _dref(
        "GT12_A2_AUTHORITY_REPLAY_ROOT",
        f"{authority_id}:replay",
        material,
    )
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(
            release.release_ref,
            release.source_artifact_ref,
            FROZEN_BINDINGS.risk_ref,
            CURRENTNESS_REF,
        ),
        producer_replay_locator_or_reference_root=replay_root,
        authority_id=authority_id,
        authority_version="1.0.0",
        authority_content_hash=authority_content_hash,
        authority_kind=authority_kind,
        decision_state="ALLOW",
        governed_operations=(GT1_CLAIM_ID,),
        governed_object_families=object_families,
        scope_envelope=scope,
        effective_time_or_interval="GT12_FROZEN_CANARY_CURRENTNESS",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash(
            {"material": material, "no_widening": True}
        ),
        replay_protocol_ref=REPLAY_PROTOCOL_REF,
    )


def _source_native_domain() -> tuple[object, ...]:
    values: list[object] = []
    for state in Q86_NATIVE_STATES:
        if state.response_state == "SUBSTANTIVE_RESPONSE":
            values.append(state.code)
        else:
            values.append({"typed_response_state": state.response_state})
    return tuple(values)


def build_a2_gt1_context(release: C11LogicalRelease) -> A2GT1Context:
    if not isinstance(release, C11LogicalRelease):
        raise GT12BI03BindingError("A2 requires a sealed C11LogicalRelease")
    if release.release_id != A1_RELEASE_ID or release.release_ref.content_hash != A1_RELEASE_HASH:
        raise GT12BI03BindingError("A2 release identity differs from terminal A1")
    if release.replay_manifest.ref.content_hash != A1_REPLAY_HASH:
        raise GT12BI03BindingError("A2 replay manifest differs from terminal A1")
    if release.source_artifact_ref.content_hash != FROZEN_BINDINGS.source_sha256:
        raise GT12BI03BindingError("A2 source identity differs from frozen R5 source")

    universe = _one_public(release, cls=EmpiricalUniverse)
    source_authority = _one_public(
        release, authority_id="GT12-A-R5-Q86-SOURCE-SEMANTICS"
    )
    frozen_gt2_permission = _one_public(
        release, authority_id="GT12-A-R5-Q86-FROZEN-TARGET-USE"
    )
    query_authority = _claim_authority(
        release=release,
        universe=universe,
        authority_id=A2_QUERY_AUTHORITY_ID,
        authority_kind="PREDICATE_GRAMMAR",
        object_families=(
            "EmpiricalPredicate@1.0.0",
            "EmpiricalQuerySpec@1.0.0",
            "EmpiricalFact@1.0.0",
        ),
    )
    target_use_authority = _claim_authority(
        release=release,
        universe=universe,
        authority_id=A2_TARGET_USE_AUTHORITY_ID,
        authority_kind="TARGET_USE_PERMISSION",
        object_families=("EmpiricalFact@1.0.0",),
        target_use_ref=GT1_TARGET_USE_REF,
    )
    release_authorities = tuple(
        obj for obj in release.public_objects if isinstance(obj, AuthoritySnapshot)
    )
    registry = AuthorityRegistry(
        (*release_authorities, query_authority, target_use_authority)
    )

    domain = _source_native_domain()
    included_states = tuple(dict.fromkeys(s.response_state for s in Q86_NATIVE_STATES))
    q86a = R5Q86TargetBinding(
        source_native_variable="Q86A",
        question_impl_id=FROZEN_Q86A_QIMPL,
        current_source_structure_id=FROZEN_Q86A_SOURCE_STRUCTURE,
        native_question_ref=question_ref("Q86A"),
        domain=domain,
        target_domain_replay_ref=target_domain_replay_ref("Q86A"),
        topology_authority_refs=(source_authority.authority_ref,),
        response_semantic_authority_refs=(source_authority.authority_ref,),
        included_states=included_states,
    )
    q86b = R5Q86TargetBinding(
        source_native_variable="Q86B",
        question_impl_id=FROZEN_Q86B_QIMPL,
        current_source_structure_id=FROZEN_BINDINGS.source_structure_id,
        native_question_ref=question_ref("Q86B"),
        domain=domain,
        target_domain_replay_ref=target_domain_replay_ref("Q86B"),
        topology_authority_refs=(source_authority.authority_ref,),
        response_semantic_authority_refs=(source_authority.authority_ref,),
        included_states=included_states,
    )
    response_semantics_ref = _dref(
        "RESPONSE_STATE_SEMANTICS",
        "Afrobarometer:R5:Q86:SOURCE_NATIVE_RESPONSE_STATES",
        {
            "domains": (
                target_domain_replay_ref("Q86A"),
                target_domain_replay_ref("Q86B"),
            ),
            "numeric_codes_are_identity_only": True,
        },
    )
    binding = R5Q86I03ExecutionBinding(
        release_ref=release.release_ref,
        empirical_universe_ref=universe.ref,
        risk_set_ref=FROZEN_BINDINGS.risk_ref,
        risk_set_identity=FROZEN_RISK_SET_ID,
        risk_set_semantic_member_set_sha256=FROZEN_RISK_MEMBER_SET_SHA256,
        response_state_semantics_ref=response_semantics_ref,
        query_authority_ref=query_authority.authority_ref,
        gt1_query_operation=GT1_CLAIM_ID,
        gt2_query_operation=GT2_CLAIM_ID,
        gt1_target_use=ExactTargetUseBinding(
            GT1_TARGET_USE_REF,
            target_use_authority.authority_ref,
            GT1_CLAIM_ID,
            GT1_TARGET_USE_CEILING,
        ),
        # Required only to complete the frozen two-target binding shape. A2 never
        # validates or executes this GT2 permission.
        gt2_target_use=ExactTargetUseBinding(
            GT2_TARGET_USE_REF,
            frozen_gt2_permission.authority_ref,
            GT2_CLAIM_ID,
            "EMPIRICAL_INPUT_TO_FROZEN_EXACT_CONDITIONAL_SUPPORT_ONLY__NO_CAUSAL_OR_ACTOR_PROMOTION",
        ),
        q86a=q86a,
        q86b=q86b,
    )
    return A2GT1Context(
        release,
        universe,
        binding,
        registry,
        query_authority,
        target_use_authority,
    )


def execute_and_replay_a2_gt1(release: C11LogicalRelease) -> A2GT1Result:
    context = build_a2_gt1_context(release)
    plan = build_gt1_q86a_i03_plan(
        release=release,
        binding=context.binding,
        authority_registry=context.authority_registry,
    )
    execution = execute_gt12b_i03_plan(
        release=release,
        plan=plan,
        authority_registry=context.authority_registry,
    )
    fact = execution.fact
    if fact.typed_state != "SUPPORTED":
        raise GT12BI03BindingError(f"real GT1 did not resolve SUPPORTED: {fact.typed_state}")
    if fact.raw_denominator_support != FROZEN_RISK_SET_MEMBER_COUNT:
        raise GT12BI03BindingError("real GT1 denominator drift from exact 19,210")
    if context.target_use_authority.authority_ref not in fact.authority_snapshot_refs:
        raise GT12BI03BindingError("real GT1 fact lost exact target-use permission authority")
    replay_result = replay_gt12b_i03_execution(
        release=release,
        execution=execution,
        authority_registry=context.authority_registry,
    )
    if replay_result != execution.result:
        raise GT12BI03BindingError("real GT1 deterministic replay differs")
    return A2GT1Result(context, execution, replay_result)


__all__ = [
    "A1_RELEASE_ID", "A1_RELEASE_HASH", "A1_REPLAY_HASH",
    "A2_QUERY_AUTHORITY_ID", "A2_TARGET_USE_AUTHORITY_ID",
    "A2GT1Context", "A2GT1Result", "build_a2_gt1_context",
    "execute_and_replay_a2_gt1",
]
