"""Bounded GT1/GT2 I03 execution adapter for the frozen Afrobarometer R5 Q86 canary.

This module does not create a new empirical engine.  It binds an already-validated
PRE553 C11 release to the existing I03 executor for exactly two frozen uses:

* GT1: Q86A raw unary distribution on the exact common R5 risk set;
* GT2: Q86B x Q86A raw joint distribution on that same exact risk set.

The GT2 component order is intentionally ``(Q86B, Q86A)`` because the frozen
contract preserves Q86B as the later FIELD FORGE conditioner and Q86A as target.
The I03 fact itself remains producer-owned empirical truth and carries no causal,
structural, actor, or V3/V2 promotion.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_c11_integrity import RespondentIdentity
from rawlsing_next.pre553_c11_repository import C11LogicalRelease, C11Repository
from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    require_positive_authority,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    EmpiricalUniverse,
    ExactRef,
    Pre553IntegrityError,
    RespondentEvent,
    RoutingEligibilityFact,
    assert_zero_actor_v3_v2_effect,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    make_empirical_predicate,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import (
    QueryExecutionResult,
    execute_empirical_query,
    replay_empirical_query,
)

GT1_CLAIM_ID = "GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET@1"
GT2_CLAIM_ID = "GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1"
GT1_TARGET_USE_CEILING = "GT1_POSITIVE_EMPIRICAL_FACT_ONLY__NO_STRUCTURAL_OR_ACTOR_PROMOTION"

FROZEN_R5_SOURCE_SHA256 = "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651"
FROZEN_RISK_SET_ID = "FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1"
FROZEN_RISK_SET_MEMBER_COUNT = 19_210
FROZEN_RISK_MEMBER_SET_SHA256 = "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b"
FROZEN_Q86A_QIMPL = "question_impl.phase0.67f036c0efb7fb98ff4a"
FROZEN_Q86B_QIMPL = "question_impl.phase0.2fb3a62609dad4c1306d"
FROZEN_Q86A_SOURCE_STRUCTURE = "cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4"
FROZEN_CONTRACT_COMMIT = "a9416094cbb4653dd2de2e4aa7b67577a355560c"
FROZEN_CONTRACT_BLOB = "c956ffb46b6609d0e4e16abbe8180a3e1930d099"


class GT12BI03BindingError(Pre553IntegrityError):
    """The frozen GT1/GT2 I03 binding cannot be established exactly."""


def _require_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GT12BI03BindingError(f"{name} must be non-empty text")
    return value.strip()


def _require_sha256(value: Any, name: str) -> str:
    value = _require_text(value, name)
    if len(value) != 64 or value.lower() != value or any(ch not in "0123456789abcdef" for ch in value):
        raise GT12BI03BindingError(f"{name} must be lowercase sha256")
    return value


def _dref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:gt12b:{namespace}:sha256:{digest}", digest)


@dataclass(frozen=True)
class R5Q86TargetBinding:
    source_native_variable: str
    question_impl_id: str
    current_source_structure_id: str
    native_question_ref: ExactRef
    domain: tuple[Any, ...]
    target_domain_replay_ref: ExactRef
    topology_authority_refs: tuple[AuthorityRef, ...]
    response_semantic_authority_refs: tuple[AuthorityRef, ...]
    included_states: tuple[str, ...]
    topology: str = "SCALAR_SINGULAR"

    def __post_init__(self) -> None:
        _require_text(self.source_native_variable, "source_native_variable")
        _require_text(self.question_impl_id, "question_impl_id")
        _require_text(self.current_source_structure_id, "current_source_structure_id")
        exact_ref(self.native_question_ref, "native_question_ref")
        exact_ref(self.target_domain_replay_ref, "target_domain_replay_ref")
        if self.topology != "SCALAR_SINGULAR":
            raise GT12BI03BindingError("frozen Q86 GT1/GT2 targets must remain SCALAR_SINGULAR")
        if not self.domain:
            raise GT12BI03BindingError("complete source-native target domain may not be empty")
        keys = [canonical_json(value) for value in self.domain]
        if len(keys) != len(set(keys)):
            raise GT12BI03BindingError("target domain contains duplicate canonical states")
        if not self.topology_authority_refs or not self.response_semantic_authority_refs:
            raise GT12BI03BindingError("target topology/response authority bundles may not be empty")
        for ref in (*self.topology_authority_refs, *self.response_semantic_authority_refs):
            authority_ref(ref, "target authority ref")
        if not self.included_states or any(not isinstance(x, str) or not x.strip() for x in self.included_states):
            raise GT12BI03BindingError("included_states must be exact non-empty response-state names")
        if len(self.included_states) != len(set(self.included_states)):
            raise GT12BI03BindingError("included_states may not contain duplicates")


@dataclass(frozen=True)
class ExactTargetUseBinding:
    target_use_ref: ExactRef
    authority_ref: AuthorityRef
    operation: str
    permission_ceiling: str

    def __post_init__(self) -> None:
        exact_ref(self.target_use_ref, "target_use_ref")
        authority_ref(self.authority_ref, "target_use.authority_ref")
        _require_text(self.operation, "target_use.operation")
        _require_text(self.permission_ceiling, "target_use.permission_ceiling")


@dataclass(frozen=True)
class R5Q86I03ExecutionBinding:
    release_ref: ExactRef
    empirical_universe_ref: ExactRef
    risk_set_ref: ExactRef
    risk_set_identity: str
    risk_set_semantic_member_set_sha256: str
    response_state_semantics_ref: ExactRef
    query_authority_ref: AuthorityRef
    gt1_query_operation: str
    gt2_query_operation: str
    gt1_target_use: ExactTargetUseBinding
    gt2_target_use: ExactTargetUseBinding
    q86a: R5Q86TargetBinding
    q86b: R5Q86TargetBinding

    def __post_init__(self) -> None:
        exact_ref(self.release_ref, "release_ref")
        exact_ref(self.empirical_universe_ref, "empirical_universe_ref")
        exact_ref(self.risk_set_ref, "risk_set_ref")
        exact_ref(self.response_state_semantics_ref, "response_state_semantics_ref")
        authority_ref(self.query_authority_ref, "query_authority_ref")
        _require_text(self.risk_set_identity, "risk_set_identity")
        _require_sha256(self.risk_set_semantic_member_set_sha256, "risk_set_semantic_member_set_sha256")
        _require_text(self.gt1_query_operation, "gt1_query_operation")
        _require_text(self.gt2_query_operation, "gt2_query_operation")


@dataclass(frozen=True)
class GT12BI03Plan:
    claim_id: str
    target_use: ExactTargetUseBinding
    predicate: EmpiricalPredicate
    query: EmpiricalQuerySpec
    exact_risk_member_refs: tuple[ExactRef, ...]


@dataclass(frozen=True)
class GT12BI03Execution:
    plan: GT12BI03Plan
    result: QueryExecutionResult

    @property
    def fact(self) -> EmpiricalFact:
        if len(self.result.facts) != 1:
            raise GT12BI03BindingError("SINGLE_UNIVERSE frozen GT12 execution must return exactly one fact")
        return self.result.facts[0]


def _frozen_contract_ref() -> ExactRef:
    return _dref(
        "GT12_FROZEN_CANARY_CONTRACT",
        "frozen-contract",
        {"commit": FROZEN_CONTRACT_COMMIT, "blob": FROZEN_CONTRACT_BLOB},
    )


def _validate_frozen_binding(binding: R5Q86I03ExecutionBinding) -> None:
    if binding.risk_set_identity != FROZEN_RISK_SET_ID:
        raise GT12BI03BindingError("risk-set identity drift from frozen GT1/GT2 contract")
    if binding.risk_set_semantic_member_set_sha256 != FROZEN_RISK_MEMBER_SET_SHA256:
        raise GT12BI03BindingError("risk-set semantic member-set hash drift")
    if binding.gt1_target_use.permission_ceiling != GT1_TARGET_USE_CEILING:
        raise GT12BI03BindingError("GT1 target-use permission ceiling drift")
    if binding.q86a.source_native_variable != "Q86A" or binding.q86a.question_impl_id != FROZEN_Q86A_QIMPL:
        raise GT12BI03BindingError("Q86A identity/qimpl drift")
    if binding.q86a.current_source_structure_id != FROZEN_Q86A_SOURCE_STRUCTURE:
        raise GT12BI03BindingError("Q86A current source-structure drift")
    if binding.q86b.source_native_variable != "Q86B" or binding.q86b.question_impl_id != FROZEN_Q86B_QIMPL:
        raise GT12BI03BindingError("Q86B identity/qimpl drift")
    if not binding.q86b.current_source_structure_id.startswith("cssu.r1.afrobarometer.r5."):
        raise GT12BI03BindingError("Q86B must remain bound to exact current Afrobarometer R5 source-structure grain")
    if binding.q86a.native_question_ref == binding.q86b.native_question_ref:
        raise GT12BI03BindingError("Q86A and Q86B exact native question refs must remain distinct")


def _release_universe(release: C11LogicalRelease, universe_ref: ExactRef) -> EmpiricalUniverse:
    matches = [obj for obj in release.public_objects if isinstance(obj, EmpiricalUniverse) and obj.ref == universe_ref]
    if len(matches) != 1:
        raise GT12BI03BindingError("frozen empirical universe must resolve exactly once in validated release")
    return matches[0]


def _release_respondent_refs(release: C11LogicalRelease, universe_ref: ExactRef) -> tuple[ExactRef, ...]:
    refs = []
    for record in release.internal_records:
        if not isinstance(record, RespondentIdentity):
            continue
        if exact_ref(record.empirical_universe_ref, "RespondentIdentity.empirical_universe_ref") == universe_ref:
            refs.append(record.ref)
    refs = sorted(set(refs), key=lambda ref: ref.key)
    if not refs:
        raise GT12BI03BindingError("validated release contains no respondent identities for frozen universe")
    return tuple(refs)


def _routing_map(
    release: C11LogicalRelease,
    *,
    universe_ref: ExactRef,
    target_ref: ExactRef,
    risk_set_ref: ExactRef,
) -> dict[ExactRef, RoutingEligibilityFact]:
    result: dict[ExactRef, RoutingEligibilityFact] = {}
    for obj in release.public_objects:
        if not isinstance(obj, RoutingEligibilityFact):
            continue
        if exact_ref(obj.empirical_universe_ref, "routing.empirical_universe_ref") != universe_ref:
            continue
        if exact_ref(obj.question_or_target_ref, "routing.question_or_target_ref") != target_ref:
            continue
        if exact_ref(obj.risk_set_ref, "routing.risk_set_ref") != risk_set_ref:
            continue
        respondent = exact_ref(obj.scoped_respondent_ref, "routing.scoped_respondent_ref")
        prior = result.get(respondent)
        if prior is not None:
            same = (
                prior.routing_state == obj.routing_state
                and prior.applicability_state == obj.applicability_state
                and exact_ref(prior.member_set_replay_ref, "routing.member_set_replay_ref")
                == exact_ref(obj.member_set_replay_ref, "routing.member_set_replay_ref")
            )
            if not same:
                raise GT12BI03BindingError("conflicting routing facts for one respondent/target/risk set")
            continue
        result[respondent] = obj
    return result


def _common_exact_risk_members(release: C11LogicalRelease, binding: R5Q86I03ExecutionBinding) -> tuple[ExactRef, ...]:
    all_respondents = set(_release_respondent_refs(release, binding.empirical_universe_ref))
    qa = _routing_map(
        release,
        universe_ref=binding.empirical_universe_ref,
        target_ref=binding.q86a.native_question_ref,
        risk_set_ref=binding.risk_set_ref,
    )
    qb = _routing_map(
        release,
        universe_ref=binding.empirical_universe_ref,
        target_ref=binding.q86b.native_question_ref,
        risk_set_ref=binding.risk_set_ref,
    )
    if set(qa) != all_respondents or set(qb) != all_respondents:
        raise GT12BI03BindingError(
            "exact routing facts must cover every release respondent for both Q86A and Q86B; response presence is not routing"
        )
    unresolved = {"ROUTING_UNKNOWN", "RULE_UNAVAILABLE"}
    if any(str(f.routing_state) in unresolved for f in (*qa.values(), *qb.values())):
        raise GT12BI03BindingError("unresolved routing cannot be coerced into frozen common-risk membership")
    a_members = {ref for ref, fact in qa.items() if str(fact.routing_state) == "ELIGIBLE_APPLICABLE"}
    b_members = {ref for ref, fact in qb.items() if str(fact.routing_state) == "ELIGIBLE_APPLICABLE"}
    if a_members != b_members:
        raise GT12BI03BindingError(
            "Q86A/Q86B exact eligible member sets differ; jointability may not be inferred from source-block membership"
        )
    if len(a_members) != FROZEN_RISK_SET_MEMBER_COUNT:
        raise GT12BI03BindingError(
            f"frozen common risk-set count mismatch: {len(a_members)} != {FROZEN_RISK_SET_MEMBER_COUNT}"
        )
    return tuple(sorted(a_members, key=lambda ref: ref.key))


def _event_value(event: RespondentEvent) -> Any:
    if event.typed_state == "SUBSTANTIVE_RESPONSE":
        canonical = event.canonical_response_value_if_authorized
        return canonicalize(canonical if canonical is not None else event.raw_response_value)
    return canonicalize({"typed_response_state": event.typed_state})


def _validate_target_events(
    release: C11LogicalRelease,
    *,
    universe_ref: ExactRef,
    members: Iterable[ExactRef],
    target: R5Q86TargetBinding,
) -> None:
    wanted = set(members)
    by_respondent: dict[ExactRef, list[RespondentEvent]] = {ref: [] for ref in wanted}
    for obj in release.public_objects:
        if not isinstance(obj, RespondentEvent):
            continue
        if exact_ref(obj.empirical_universe_ref, "event.empirical_universe_ref") != universe_ref:
            continue
        if exact_ref(obj.native_question_ref, "event.native_question_ref") != target.native_question_ref:
            continue
        respondent = exact_ref(obj.scoped_respondent_ref, "event.scoped_respondent_ref")
        if respondent in by_respondent:
            by_respondent[respondent].append(obj)
    domain_keys = {canonical_json(value) for value in target.domain}
    included = set(target.included_states)
    for respondent, events in by_respondent.items():
        eligible = [event for event in events if event.typed_state in included]
        if len(eligible) != 1:
            raise GT12BI03BindingError(
                "each frozen risk-set respondent must resolve exactly one included scalar response event per target"
            )
        event = eligible[0]
        fields = event.multiplicity_order_rank_fields
        if not isinstance(fields, Mapping) or fields.get("kind") != "SCALAR_SINGULAR":
            raise GT12BI03BindingError("Q86 event carrier topology drift from SCALAR_SINGULAR")
        if canonical_json(_event_value(event)) not in domain_keys:
            raise GT12BI03BindingError("validated projection domain omits an observed exact source-native response state")


def _validate_release_member_scope_linear(
    release: C11LogicalRelease,
    binding: R5Q86I03ExecutionBinding,
) -> tuple[ExactRef, ...]:
    """Validate the frozen two-target carrier in one compact pass.

    The original bounded adapter independently materialized two routing maps and
    two event maps over the same 19,210-member release.  At genuine scale those
    duplicate maps create a memory-pressure cliff.  This routine preserves the
    exact checks while indexing immutable ref keys once.
    """
    respondent_by_key = {
        ref.key: ref for ref in _release_respondent_refs(release, binding.empirical_universe_ref)
    }
    if not respondent_by_key:
        raise GT12BI03BindingError("validated release contains no frozen respondents")

    universe_key = binding.empirical_universe_ref.key
    risk_key = binding.risk_set_ref.key
    target_keys = {
        binding.q86a.native_question_ref.key: "Q86A",
        binding.q86b.native_question_ref.key: "Q86B",
    }
    routing: dict[str, dict[str, tuple[str, str, str]]] = {"Q86A": {}, "Q86B": {}}

    for obj in release.public_objects:
        if not isinstance(obj, RoutingEligibilityFact):
            continue
        if exact_ref(obj.empirical_universe_ref, "routing.empirical_universe_ref").key != universe_key:
            continue
        target_name = target_keys.get(
            exact_ref(obj.question_or_target_ref, "routing.question_or_target_ref").key
        )
        if target_name is None:
            continue
        if exact_ref(obj.risk_set_ref, "routing.risk_set_ref").key != risk_key:
            continue
        respondent_key = exact_ref(
            obj.scoped_respondent_ref, "routing.scoped_respondent_ref"
        ).key
        signature = (
            str(obj.routing_state),
            str(obj.applicability_state),
            exact_ref(obj.member_set_replay_ref, "routing.member_set_replay_ref").key,
        )
        prior = routing[target_name].get(respondent_key)
        if prior is not None and prior != signature:
            raise GT12BI03BindingError(
                "conflicting routing facts for one respondent/target/risk set"
            )
        routing[target_name][respondent_key] = signature

    all_keys = set(respondent_by_key)
    for target_name in ("Q86A", "Q86B"):
        if set(routing[target_name]) != all_keys:
            raise GT12BI03BindingError(
                "exact routing facts must cover every release respondent for both Q86A and Q86B; response presence is not routing"
            )
    unresolved = {"ROUTING_UNKNOWN", "RULE_UNAVAILABLE"}
    if any(
        signature[0] in unresolved
        for target_name in ("Q86A", "Q86B")
        for signature in routing[target_name].values()
    ):
        raise GT12BI03BindingError(
            "unresolved routing cannot be coerced into frozen common-risk membership"
        )
    a_keys = {key for key, signature in routing["Q86A"].items() if signature[0] == "ELIGIBLE_APPLICABLE"}
    b_keys = {key for key, signature in routing["Q86B"].items() if signature[0] == "ELIGIBLE_APPLICABLE"}
    if a_keys != b_keys:
        raise GT12BI03BindingError(
            "Q86A/Q86B exact eligible member sets differ; jointability may not be inferred from source-block membership"
        )
    if len(a_keys) != FROZEN_RISK_SET_MEMBER_COUNT:
        raise GT12BI03BindingError(
            f"frozen common risk-set count mismatch: {len(a_keys)} != {FROZEN_RISK_SET_MEMBER_COUNT}"
        )

    domains = {
        "Q86A": {canonical_json(value) for value in binding.q86a.domain},
        "Q86B": {canonical_json(value) for value in binding.q86b.domain},
    }
    included = {
        "Q86A": set(binding.q86a.included_states),
        "Q86B": set(binding.q86b.included_states),
    }
    event_target_keys = {
        binding.q86a.native_question_ref.key: "Q86A",
        binding.q86b.native_question_ref.key: "Q86B",
    }
    seen: dict[str, set[str]] = {"Q86A": set(), "Q86B": set()}
    for obj in release.public_objects:
        if not isinstance(obj, RespondentEvent):
            continue
        if exact_ref(obj.empirical_universe_ref, "event.empirical_universe_ref").key != universe_key:
            continue
        target_name = event_target_keys.get(
            exact_ref(obj.native_question_ref, "event.native_question_ref").key
        )
        if target_name is None or obj.typed_state not in included[target_name]:
            continue
        respondent_key = exact_ref(
            obj.scoped_respondent_ref, "event.scoped_respondent_ref"
        ).key
        if respondent_key not in a_keys:
            continue
        if respondent_key in seen[target_name]:
            raise GT12BI03BindingError(
                "each frozen risk-set respondent must resolve exactly one included scalar response event per target"
            )
        fields = obj.multiplicity_order_rank_fields
        if not isinstance(fields, Mapping) or fields.get("kind") != "SCALAR_SINGULAR":
            raise GT12BI03BindingError("Q86 event carrier topology drift from SCALAR_SINGULAR")
        if canonical_json(_event_value(obj)) not in domains[target_name]:
            raise GT12BI03BindingError(
                "validated projection domain omits an observed exact source-native response state"
            )
        seen[target_name].add(respondent_key)

    for target_name in ("Q86A", "Q86B"):
        if seen[target_name] != a_keys:
            raise GT12BI03BindingError(
                "each frozen risk-set respondent must resolve exactly one included scalar response event per target"
            )
    return tuple(sorted((respondent_by_key[key] for key in a_keys), key=lambda ref: ref.key))


def _validate_release_and_members(
    release: C11LogicalRelease,
    binding: R5Q86I03ExecutionBinding,
) -> tuple[ExactRef, ...]:
    _validate_frozen_binding(binding)
    if not isinstance(release, C11LogicalRelease):
        raise GT12BI03BindingError("validated C11LogicalRelease required")
    if release.release_ref != binding.release_ref:
        raise GT12BI03BindingError("release ref mismatch")
    if release.source_artifact_ref.content_hash != FROZEN_R5_SOURCE_SHA256:
        raise GT12BI03BindingError("validated release source SHA drift from frozen R5 source")
    _release_universe(release, binding.empirical_universe_ref)
    return _validate_release_member_scope_linear(release, binding)


def _resolve_positive_authority(registry: AuthorityRegistry, ref: AuthorityRef, *, name: str):
    try:
        return registry.resolve_exact(ref).snapshot
    except (Pre553AuthorityError, KeyError) as exc:
        raise GT12BI03BindingError(f"missing exact {name}") from exc


def _validate_query_authority(
    registry: AuthorityRegistry,
    *,
    binding: R5Q86I03ExecutionBinding,
    operation: str,
) -> None:
    snapshot = _resolve_positive_authority(registry, binding.query_authority_ref, name="I03 query authority")
    try:
        for family in ("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"):
            require_positive_authority(
                snapshot,
                authority_kind="PREDICATE_GRAMMAR",
                operation=operation,
                object_family=family,
                source_universe_ref=binding.empirical_universe_ref.as_dict(),
            )
    except Pre553AuthorityError as exc:
        raise GT12BI03BindingError("exact query/predicate/fact authority does not cover frozen operation") from exc


def _validate_target_use(
    registry: AuthorityRegistry,
    *,
    binding: R5Q86I03ExecutionBinding,
    target_use: ExactTargetUseBinding,
) -> None:
    snapshot = _resolve_positive_authority(registry, target_use.authority_ref, name="target-use authority")
    try:
        require_positive_authority(
            snapshot,
            authority_kind="TARGET_USE_PERMISSION",
            operation=target_use.operation,
            source_universe_ref=binding.empirical_universe_ref.as_dict(),
            target_use_ref=target_use.target_use_ref.as_dict(),
        )
    except Pre553AuthorityError as exc:
        raise GT12BI03BindingError("exact target-use authority does not cover frozen query use") from exc


def _predicate_for_members(
    binding: R5Q86I03ExecutionBinding,
    members: tuple[ExactRef, ...],
) -> EmpiricalPredicate:
    member_material = {
        "contract": _frozen_contract_ref().as_dict(),
        "risk_set_ref": binding.risk_set_ref.as_dict(),
        "members": [ref.as_dict() for ref in members],
    }
    membership_ref = _dref("GT12_EXACT_RISK_MEMBERSHIP", "risk-membership", member_material)
    replay_ref = _dref("GT12_EXACT_RISK_MEMBERSHIP_REPLAY", "risk-membership-replay", member_material)
    operator_ref = _dref(
        "OPERATOR_SEMANTICS",
        "operator-exact-branch-membership",
        {"operator": "DERIVED_BRANCH_COHORT", "same_respondent": "EXACT_SCOPED_RESPONDENT"},
    )
    ast = {
        "op": "LEAF",
        "leaf_type": "DERIVED_BRANCH_COHORT",
        "branch_definition_id": FROZEN_RISK_SET_ID,
        "resolved_predicate_hash_or_exact_membership_ref": membership_ref,
        "parent_ancestry_ref": _frozen_contract_ref(),
        "branch_algorithm_authority_ref": binding.query_authority_ref,
        "branch_membership_replay_ref": replay_ref,
        "branch_source_scope_ref": binding.empirical_universe_ref,
        "exact_member_respondent_refs": members,
    }
    return make_empirical_predicate(
        predicate_ast=ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(binding.query_authority_ref,),
        dependency_refs=(binding.risk_set_ref, membership_ref, _frozen_contract_ref()),
        producer_replay_locator_or_reference_root=replay_ref,
        grammar_authority_ref=binding.query_authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=(binding.risk_set_ref,),
        scope_refs=(binding.empirical_universe_ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(operator_ref,),
    )


def _target_component(target: R5Q86TargetBinding) -> dict[str, Any]:
    return {
        "target_ref": target.native_question_ref,
        "topology": target.topology,
        "domain": target.domain,
        "target_domain_replay_ref": target.target_domain_replay_ref,
        "topology_authority_refs": target.topology_authority_refs,
        "response_semantic_authority_refs": target.response_semantic_authority_refs,
        "included_states": target.included_states,
    }


def _query_for_targets(
    *,
    claim_id: str,
    binding: R5Q86I03ExecutionBinding,
    predicate: EmpiricalPredicate,
    targets: tuple[R5Q86TargetBinding, ...],
    target_use: ExactTargetUseBinding,
) -> EmpiricalQuerySpec:
    measure_ref = _dref("MEASURE_BASIS", "raw-measure", {"measure_kind": "RAW"})
    replay_material = {
        "claim_id": claim_id,
        "release_ref": binding.release_ref.as_dict(),
        "universe_ref": binding.empirical_universe_ref.as_dict(),
        "risk_set_ref": binding.risk_set_ref.as_dict(),
        "predicate_ref": predicate.ref.as_dict(),
        "target_refs": [target.native_question_ref.as_dict() for target in targets],
        "target_domain_replay_refs": [target.target_domain_replay_ref.as_dict() for target in targets],
        "target_use_ref": target_use.target_use_ref.as_dict(),
        "target_use_authority_ref": target_use.authority_ref.as_dict(),
        "target_use_operation": target_use.operation,
        "permission_ceiling": target_use.permission_ceiling,
    }
    deps = [predicate.ref, binding.risk_set_ref, target_use.target_use_ref, _frozen_contract_ref()]
    deps.extend(target.target_domain_replay_ref for target in targets)
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        # The target-use permission remains a distinct TARGET_USE_PERMISSION
        # authority.  Carry it in the query closure so a positive EmpiricalFact
        # preserves the exact permission snapshot rather than only naming it in
        # requested_output_grain.
        authority_snapshot_refs=(binding.query_authority_ref, target_use.authority_ref),
        dependency_refs=tuple(deps),
        producer_replay_locator_or_reference_root=_dref("GT12_I03_QUERY_REPLAY_ROOT", "query-replay", replay_material),
        target_refs=tuple(target.native_question_ref for target in targets),
        target_arity_and_topology={
            "arity": len(targets),
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": [_target_component(target) for target in targets],
        },
        condition_predicate_ref=predicate.ref,
        risk_set_ref=binding.risk_set_ref,
        empirical_universe_refs=(binding.empirical_universe_ref,),
        scope_refs=(binding.empirical_universe_ref,),
        measure_basis_ref=measure_ref,
        requested_output_grain={
            "source_scope_mode": "SINGLE_UNIVERSE",
            "measure_kind": "RAW",
            "risk_set_type": "COMMON_ELIGIBLE_RISK_SET",
            "response_state_semantics_ref": binding.response_state_semantics_ref,
            "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
            "gt12_claim_id": claim_id,
            "frozen_risk_set_identity": FROZEN_RISK_SET_ID,
            "frozen_risk_set_semantic_member_set_sha256": binding.risk_set_semantic_member_set_sha256,
            "target_use_ref": target_use.target_use_ref,
            "target_use_authority_ref": target_use.authority_ref,
            "target_use_operation": target_use.operation,
            "permission_ceiling": target_use.permission_ceiling,
        },
        query_authority_refs=(binding.query_authority_ref,),
    )


def build_gt1_q86a_i03_plan(
    *,
    release: C11LogicalRelease,
    binding: R5Q86I03ExecutionBinding,
    authority_registry: AuthorityRegistry,
) -> GT12BI03Plan:
    members = _validate_release_and_members(release, binding)
    _validate_query_authority(
        authority_registry, binding=binding, operation=binding.gt1_query_operation
    )
    _validate_target_use(
        authority_registry, binding=binding, target_use=binding.gt1_target_use
    )
    predicate = _predicate_for_members(binding, members)
    query = _query_for_targets(
        claim_id=GT1_CLAIM_ID,
        binding=binding,
        predicate=predicate,
        targets=(binding.q86a,),
        target_use=binding.gt1_target_use,
    )
    return GT12BI03Plan(GT1_CLAIM_ID, binding.gt1_target_use, predicate, query, members)


def build_gt2_q86a_q86b_i03_plan(
    *,
    release: C11LogicalRelease,
    binding: R5Q86I03ExecutionBinding,
    authority_registry: AuthorityRegistry,
) -> GT12BI03Plan:
    members = _validate_release_and_members(release, binding)
    _validate_query_authority(
        authority_registry, binding=binding, operation=binding.gt2_query_operation
    )
    _validate_target_use(
        authority_registry, binding=binding, target_use=binding.gt2_target_use
    )
    predicate = _predicate_for_members(binding, members)
    # Frozen semantic component order is Q86B conditioner dimension, then Q86A target dimension.
    query = _query_for_targets(
        claim_id=GT2_CLAIM_ID,
        binding=binding,
        predicate=predicate,
        targets=(binding.q86b, binding.q86a),
        target_use=binding.gt2_target_use,
    )
    return GT12BI03Plan(GT2_CLAIM_ID, binding.gt2_target_use, predicate, query, members)


def execute_gt12b_i03_plan(
    *,
    release: C11LogicalRelease,
    plan: GT12BI03Plan,
    authority_registry: AuthorityRegistry,
) -> GT12BI03Execution:
    repository = C11Repository((release,))
    result = execute_empirical_query(
        repository=repository,
        query=plan.query,
        predicate=plan.predicate,
        authority_registry=authority_registry,
        release_refs=(release.release_ref,),
    )
    if result.source_scope_mode != "SINGLE_UNIVERSE" or result.release_refs != (release.release_ref,):
        raise GT12BI03BindingError("I03 execution escaped exact SINGLE_UNIVERSE release scope")
    if len(result.facts) != 1:
        raise GT12BI03BindingError("frozen single-universe operation must emit exactly one EmpiricalFact")
    assert_zero_actor_v3_v2_effect(result.facts[0])
    return GT12BI03Execution(plan, result)


def replay_gt12b_i03_execution(
    *,
    release: C11LogicalRelease,
    execution: GT12BI03Execution,
    authority_registry: AuthorityRegistry,
) -> QueryExecutionResult:
    repository = C11Repository((release,))
    replayed = replay_empirical_query(
        repository=repository,
        query=execution.plan.query,
        predicate=execution.plan.predicate,
        authority_registry=authority_registry,
        release_refs=(release.release_ref,),
        expected_fact_refs=tuple(fact.ref for fact in execution.result.facts),
    )
    if replayed != execution.result:
        raise GT12BI03BindingError("deterministic I03 replay diverged from first execution")
    return replayed


__all__ = [
    "GT1_CLAIM_ID",
    "GT2_CLAIM_ID",
    "GT1_TARGET_USE_CEILING",
    "FROZEN_R5_SOURCE_SHA256",
    "FROZEN_RISK_SET_ID",
    "FROZEN_RISK_SET_MEMBER_COUNT",
    "FROZEN_RISK_MEMBER_SET_SHA256",
    "GT12BI03BindingError",
    "R5Q86TargetBinding",
    "ExactTargetUseBinding",
    "R5Q86I03ExecutionBinding",
    "GT12BI03Plan",
    "GT12BI03Execution",
    "build_gt1_q86a_i03_plan",
    "build_gt2_q86a_q86b_i03_plan",
    "execute_gt12b_i03_plan",
    "replay_gt12b_i03_execution",
]
