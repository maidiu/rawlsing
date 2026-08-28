"""Authority-37 branch co-signature target enumeration and composition.

This module derives a finite, source-governed substantive response target
catalog before inspecting branch-conditioned outcomes, executes the complete
authorized J1/J2/J3 target frontier with the integrated I03 query engine, and
seals a ref-only topology-closure receipt.

It deliberately does not modify I05, controller traversal, V3, structural
admission, or empirical storage.  Authority 37 caps the integrated direct exact
higher-order executor at J=3; J>3 remains fail closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next._pre553_query_common import TARGET_TOPOLOGIES, _TargetComponent
from rawlsing_next._pre553_query_eval import _routing_fact_for, _target_component_value
from rawlsing_next._pre553_query_predicate import _build_release_index
from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalCoordinateFact,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    RespondentEvent,
    RoutingEligibilityFact,
    WeightMeasureFact,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import (
    QueryExecutionResult,
    execute_empirical_query,
)

COSIGNATURE_COMPOSITION_CONTRACT_ID = (
    "PRE553_AUTH37_BRANCH_COSIGNATURE_COMPOSITION@1.0.0"
)
TARGET_CATALOG_CONTRACT_ID = "PRE553_AUTH37_COSIGNATURE_TARGET_CATALOG@1.0.0"
TOPOLOGY_CLOSURE_CONTRACT_ID = "BranchCosignatureTopologyClosureReceipt@1.0.0"
CURRENT_EXECUTOR_MAXIMUM_TARGET_ARITY_J = 3
AUTHORITY37_MAXIMUM_TARGET_ARITY_J = 3

FORBIDDEN_TARGET_KIND_TOKENS = frozenset({
    "COORDINATE", "POSITION", "DEMOGRAPHIC", "GEOGRAPHIC", "STRUCTURAL",
    "ACTOR", "PERSONA", "PERSONALITY", "BELIEF", "CAUSAL", "DIAGNOSTIC",
})
NEGATIVE_NO_MEMBER_ENVELOPE = frozenset({
    "UNAVAILABLE", "UNRESOLVED", "NONCOMPARABLE", "NOT_APPLICABLE",
    "VALID_EMPTY", "ZERO_SUPPORT", "INTEGRITY_FAILURE",
})


class CosignatureCompositionError(Pre553IntegrityError):
    """I04 exact target enumeration/composition/closure is invalid."""


def _refs(values: Iterable[ExactRef | Mapping[str, Any]]) -> tuple[ExactRef, ...]:
    return tuple(sorted({exact_ref(value) for value in values}, key=lambda ref: ref.key))


def _auth_from(value: AuthorityRef | Mapping[str, Any]) -> AuthorityRef:
    if isinstance(value, AuthorityRef):
        return value
    if not isinstance(value, Mapping):
        raise CosignatureCompositionError("exact AuthorityRef required")
    try:
        return AuthorityRef(
            value["authority_id"], value["authority_version"], value["authority_content_hash"]
        )
    except (KeyError, TypeError) as exc:
        raise CosignatureCompositionError("malformed AuthorityRef") from exc


def _auths(values: Iterable[AuthorityRef | Mapping[str, Any]]) -> tuple[AuthorityRef, ...]:
    return tuple(sorted({_auth_from(value) for value in values}, key=lambda ref: ref.key))


def _derived_ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(
        kind,
        f"urn:rawlsing:pre553:i04-cosignature:{namespace}:sha256:{digest}",
        digest,
    )


def _topology(event: RespondentEvent) -> str:
    fields = event.multiplicity_order_rank_fields
    if not isinstance(fields, Mapping):
        raise CosignatureCompositionError("response topology mapping is unresolved")
    kind = fields.get("kind") or fields.get("topology_kind")
    if not isinstance(kind, str) or kind not in TARGET_TOPOLOGIES:
        raise CosignatureCompositionError("response topology is unresolved or unsupported")
    return kind


@dataclass(frozen=True)
class BranchCosignatureContext:
    branch_predicate: EmpiricalPredicate
    branch_replay_ref: ExactRef
    immediate_parent_ref: ExactRef
    ancestry_refs: tuple[ExactRef, ...]
    source_release_refs: tuple[ExactRef, ...]
    universe_refs: tuple[ExactRef, ...]
    risk_set_ref: ExactRef

    def __post_init__(self) -> None:
        if not isinstance(self.branch_predicate, EmpiricalPredicate):
            raise CosignatureCompositionError("exact EmpiricalPredicate required")
        object.__setattr__(self, "branch_replay_ref", exact_ref(self.branch_replay_ref))
        object.__setattr__(self, "immediate_parent_ref", exact_ref(self.immediate_parent_ref))
        object.__setattr__(self, "ancestry_refs", _refs(self.ancestry_refs))
        object.__setattr__(self, "source_release_refs", _refs(self.source_release_refs))
        object.__setattr__(self, "universe_refs", _refs(self.universe_refs))
        object.__setattr__(self, "risk_set_ref", exact_ref(self.risk_set_ref))
        if len(self.source_release_refs) != 1 or len(self.universe_refs) != 1:
            raise CosignatureCompositionError(
                "I04 R1 requires one exact source release/universe; no implicit pooling"
            )
        scope_refs = {exact_ref(value).key for value in self.branch_predicate.scope_refs}
        if self.universe_refs[0].key not in scope_refs:
            raise CosignatureCompositionError("branch predicate scope does not bind exact universe")
        risk_refs = {exact_ref(value).key for value in self.branch_predicate.risk_set_refs}
        if self.risk_set_ref.key not in risk_refs:
            raise CosignatureCompositionError("branch predicate risk set does not bind exact risk")
        if self.branch_predicate.same_respondent_binding_semantics not in {
            "EXACT_SCOPED_RESPONDENT", "SAME_SCOPED_RESPONDENT"
        }:
            raise CosignatureCompositionError("branch lacks exact same-respondent semantics")

    @property
    def ref(self) -> ExactRef:
        return _derived_ref("PRE553_COSIGNATURE_BRANCH_CONTEXT", "branch-context", {
            "branch_predicate_ref": self.branch_predicate.ref.as_dict(),
            "branch_replay_ref": self.branch_replay_ref.as_dict(),
            "immediate_parent_ref": self.immediate_parent_ref.as_dict(),
            "ancestry_refs": [ref.as_dict() for ref in self.ancestry_refs],
            "source_release_refs": [ref.as_dict() for ref in self.source_release_refs],
            "universe_refs": [ref.as_dict() for ref in self.universe_refs],
            "risk_set_ref": self.risk_set_ref.as_dict(),
        })


@dataclass(frozen=True)
class TargetExclusion:
    target_ref: ExactRef
    reason: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_ref", exact_ref(self.target_ref))
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise CosignatureCompositionError("target exclusion reason required")

    def as_dict(self) -> dict[str, Any]:
        return {"target_ref": self.target_ref.as_dict(), "reason": self.reason}


@dataclass(frozen=True)
class GovernedSubstantiveTarget:
    target_ref: ExactRef
    instrument_question_version: str
    topology: str
    domain: tuple[Any, ...]
    domain_replay_ref: ExactRef
    semantic_authority_refs: tuple[AuthorityRef, ...]
    topology_authority_refs: tuple[AuthorityRef, ...]
    routing_authority_refs: tuple[AuthorityRef, ...]
    routing_rule_refs: tuple[ExactRef, ...]
    included_states: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_ref", exact_ref(self.target_ref))
        object.__setattr__(self, "domain_replay_ref", exact_ref(self.domain_replay_ref))
        object.__setattr__(self, "semantic_authority_refs", _auths(self.semantic_authority_refs))
        object.__setattr__(self, "topology_authority_refs", _auths(self.topology_authority_refs))
        object.__setattr__(self, "routing_authority_refs", _auths(self.routing_authority_refs))
        object.__setattr__(self, "routing_rule_refs", _refs(self.routing_rule_refs))
        if self.topology not in TARGET_TOPOLOGIES:
            raise CosignatureCompositionError("unsupported substantive target topology")
        states = tuple(sorted(set(str(value) for value in self.included_states)))
        if not states:
            raise CosignatureCompositionError("target has no governed response states")
        object.__setattr__(self, "included_states", states)
        domain = tuple(sorted((canonicalize(value) for value in self.domain), key=canonical_json))
        if len({canonical_json(value) for value in domain}) != len(domain):
            raise CosignatureCompositionError("duplicate target domain cell")
        object.__setattr__(self, "domain", domain)

    @property
    def ref(self) -> ExactRef:
        return _derived_ref("PRE553_COSIGNATURE_TARGET_DESCRIPTOR", "target-descriptor", {
            "target_ref": self.target_ref.as_dict(),
            "instrument_question_version": self.instrument_question_version,
            "topology": self.topology,
            "domain": list(self.domain),
            "domain_replay_ref": self.domain_replay_ref.as_dict(),
            "semantic_authority_refs": [ref.as_dict() for ref in self.semantic_authority_refs],
            "topology_authority_refs": [ref.as_dict() for ref in self.topology_authority_refs],
            "routing_authority_refs": [ref.as_dict() for ref in self.routing_authority_refs],
            "routing_rule_refs": [ref.as_dict() for ref in self.routing_rule_refs],
            "included_states": list(self.included_states),
        })

    def component(self) -> dict[str, Any]:
        return {
            "target_ref": self.target_ref.as_dict(),
            "topology": self.topology,
            "domain": list(self.domain),
            "target_domain_replay_ref": self.domain_replay_ref.as_dict(),
            "topology_authority_refs": [ref.as_dict() for ref in self.topology_authority_refs],
            "response_semantic_authority_refs": [
                ref.as_dict() for ref in self.semantic_authority_refs
            ],
            "included_states": list(self.included_states),
        }


@dataclass(frozen=True)
class GovernedTargetCatalog:
    branch_context_ref: ExactRef
    source_release_ref: ExactRef
    universe_ref: ExactRef
    risk_set_ref: ExactRef
    targets: tuple[GovernedSubstantiveTarget, ...]
    exclusions: tuple[TargetExclusion, ...]

    def __post_init__(self) -> None:
        for name in ("branch_context_ref", "source_release_ref", "universe_ref", "risk_set_ref"):
            object.__setattr__(self, name, exact_ref(getattr(self, name)))
        targets = tuple(sorted(self.targets, key=lambda target: target.target_ref.key))
        if len({target.target_ref.key for target in targets}) != len(targets):
            raise CosignatureCompositionError("duplicate target ref")
        object.__setattr__(self, "targets", targets)
        unique = {(item.target_ref.key, item.reason): item for item in self.exclusions}
        object.__setattr__(
            self, "exclusions",
            tuple(sorted(unique.values(), key=lambda item: (item.target_ref.key, item.reason)))
        )

    @property
    def target_count(self) -> int:
        return len(self.targets)

    def semantic_projection(self) -> Mapping[str, Any]:
        return canonicalize({
            "contract_id": TARGET_CATALOG_CONTRACT_ID,
            "reachability_precedes_outcomes": True,
            "ranking_controls_reachability": False,
            "branch_context_ref": self.branch_context_ref.as_dict(),
            "source_release_ref": self.source_release_ref.as_dict(),
            "universe_ref": self.universe_ref.as_dict(),
            "risk_set_ref": self.risk_set_ref.as_dict(),
            "targets": [
                {"target_ref": target.target_ref.as_dict(), "descriptor_ref": target.ref.as_dict()}
                for target in self.targets
            ],
            "exclusions": [item.as_dict() for item in self.exclusions],
        })

    @property
    def ref(self) -> ExactRef:
        return _derived_ref(
            "PRE553_COSIGNATURE_TARGET_CATALOG",
            "target-catalog",
            self.semantic_projection(),
        )

    def require_target(
        self, ref: ExactRef | Mapping[str, Any]
    ) -> GovernedSubstantiveTarget:
        wanted = exact_ref(ref)
        for target in self.targets:
            if target.target_ref == wanted:
                return target
        for item in self.exclusions:
            if item.target_ref == wanted:
                raise CosignatureCompositionError(f"target excluded: {item.reason}")
        raise CosignatureCompositionError("target absent from exact governed catalog")


@dataclass(frozen=True)
class CosignatureCompositionPolicy:
    topology_authority_ref: AuthorityRef
    query_authority_refs: tuple[AuthorityRef, ...]
    authority_maximum_target_arity_J: int
    measure_kind: str
    measure_basis_ref: ExactRef
    response_state_semantics_ref: ExactRef
    weight_basis_id: str | None = None
    uncertainty_method_or_typed_state: Any = "UNCERTAINTY_UNQUANTIFIED"

    def __post_init__(self) -> None:
        if not isinstance(self.topology_authority_ref, AuthorityRef):
            raise CosignatureCompositionError("exact topology authority ref required")
        object.__setattr__(self, "query_authority_refs", _auths(self.query_authority_refs))
        object.__setattr__(self, "measure_basis_ref", exact_ref(self.measure_basis_ref))
        object.__setattr__(
            self, "response_state_semantics_ref",
            exact_ref(self.response_state_semantics_ref),
        )
        if not self.query_authority_refs:
            raise CosignatureCompositionError("query authority required")
        if (
            not isinstance(self.authority_maximum_target_arity_J, int)
            or not 1 <= self.authority_maximum_target_arity_J <= AUTHORITY37_MAXIMUM_TARGET_ARITY_J
        ):
            raise CosignatureCompositionError("Authority-37 arity must be in [1,3]")
        if self.measure_kind not in {"RAW", "GOVERNED_WEIGHTED"}:
            raise CosignatureCompositionError("unknown measure kind")
        if self.measure_kind == "GOVERNED_WEIGHTED":
            if not isinstance(self.weight_basis_id, str) or not self.weight_basis_id.strip():
                raise CosignatureCompositionError("weighted policy requires exact weight basis")
        elif self.weight_basis_id is not None:
            raise CosignatureCompositionError("RAW policy may not carry weight basis")
        object.__setattr__(
            self, "uncertainty_method_or_typed_state",
            canonicalize(self.uncertainty_method_or_typed_state),
        )

    @property
    def ref(self) -> ExactRef:
        return _derived_ref("PRE553_COSIGNATURE_COMPOSITION_POLICY", "policy", {
            "contract_id": COSIGNATURE_COMPOSITION_CONTRACT_ID,
            "topology_authority_ref": self.topology_authority_ref.as_dict(),
            "query_authority_refs": [ref.as_dict() for ref in self.query_authority_refs],
            "authority_maximum_target_arity_J": self.authority_maximum_target_arity_J,
            "measure_kind": self.measure_kind,
            "measure_basis_ref": self.measure_basis_ref.as_dict(),
            "response_state_semantics_ref": self.response_state_semantics_ref.as_dict(),
            "weight_basis_id": self.weight_basis_id,
            "uncertainty_method_or_typed_state": self.uncertainty_method_or_typed_state,
        })


def _require_positive_ref(registry: AuthorityRegistry, ref: AuthorityRef) -> None:
    if registry.resolve_exact(ref).snapshot.typed_state != "ALLOW":
        raise CosignatureCompositionError("required exact authority is not positive")


def _policy_authority(
    policy: CosignatureCompositionPolicy, registry: AuthorityRegistry
) -> None:
    _require_positive_ref(registry, policy.topology_authority_ref)
    for ref in policy.query_authority_refs:
        _require_positive_ref(registry, ref)


def enumerate_governed_substantive_targets(
    *,
    repository: C11Repository,
    context: BranchCosignatureContext,
    authority_registry: AuthorityRegistry,
) -> GovernedTargetCatalog:
    """Derive a complete finite target catalog from source/instrument authority.

    No branch-conditioned empirical outcome is inspected.  Target reachability
    depends only on the exact release, question bindings, response topology and
    semantics, routing authority and replayable source-native target domain.
    """
    release = repository.resolve_release_exact(context.source_release_refs[0])
    universe_ref = context.universe_refs[0]
    index = _build_release_index(release, universe_ref)
    coordinate_refs: dict[str, ExactRef] = {}
    for obj in release.public_objects:
        if isinstance(obj, EmpiricalCoordinateFact) and exact_ref(obj.empirical_universe_ref) == universe_ref:
            for raw in (obj.native_coordinate_ref, obj.canonical_coordinate_ref_if_authorized):
                if raw is not None:
                    ref = exact_ref(raw)
                    coordinate_refs[ref.key] = ref

    exclusions = [
        TargetExclusion(ref, "POSITIONAL_COORDINATE__NOT_COSIGNATURE_TARGET")
        for ref in coordinate_refs.values()
    ]
    bindings = [
        record for record in release.internal_records
        if isinstance(record, QuestionVariableBinding)
        and record.empirical_universe_ref == universe_ref
    ]
    by_target: dict[str, GovernedSubstantiveTarget] = {}
    for binding in sorted(bindings, key=lambda item: item.native_question_ref.key):
        target_ref = (
            binding.canonical_question_ref_or_typed_absence
            if isinstance(binding.canonical_question_ref_or_typed_absence, ExactRef)
            else binding.native_question_ref
        )
        if target_ref.key in coordinate_refs:
            exclusions.append(
                TargetExclusion(target_ref, "POSITIONAL_COORDINATE__NOT_COSIGNATURE_TARGET")
            )
            continue
        if any(token in target_ref.kind.upper() for token in FORBIDDEN_TARGET_KIND_TOKENS):
            exclusions.append(
                TargetExclusion(target_ref, "FORBIDDEN_NON_SUBSTANTIVE_TARGET_KIND")
            )
            continue
        for ref in (binding.semantic_authority_ref, binding.topology_authority_ref):
            _require_positive_ref(authority_registry, ref)

        events = [
            event for event in release.public_objects
            if isinstance(event, RespondentEvent)
            and exact_ref(event.empirical_universe_ref) == universe_ref
            and (
                exact_ref(event.native_question_ref) == target_ref
                or (
                    event.canonical_question_ref_if_authorized is not None
                    and exact_ref(event.canonical_question_ref_if_authorized) == target_ref
                )
            )
        ]
        if not events:
            exclusions.append(TargetExclusion(target_ref, "NO_GOVERNED_RESPONSE_EVENTS"))
            continue
        topologies = {_topology(event) for event in events}
        if len(topologies) != 1:
            exclusions.append(TargetExclusion(target_ref, "UNRESOLVED_RESPONSE_TOPOLOGY"))
            continue
        topology = next(iter(topologies))
        states = tuple(sorted({event.typed_state for event in events}))

        routing_auths: list[AuthorityRef] = []
        routing_rules: list[ExactRef] = []
        routing_ok = True
        used: list[Any] = []
        used_auth: list[AuthorityRef] = []
        for respondent in sorted(index.respondents.values(), key=lambda item: item.ref.key):
            try:
                routing = _routing_fact_for(
                    respondent,
                    index,
                    target_ref=target_ref,
                    risk_set_ref=context.risk_set_ref,
                    registry=authority_registry,
                    used=used,
                    used_auth=used_auth,
                )
            except (Pre553AuthorityError, Pre553IntegrityError):
                routing_ok = False
                break
            routing_auths.extend(routing.authority_snapshot_refs)
            routing_rules.append(exact_ref(routing.routing_rule_ref))
        if not routing_ok:
            exclusions.append(TargetExclusion(target_ref, "ROUTING_AUTHORITY_UNRESOLVED"))
            continue

        provisional = _TargetComponent(
            target_ref=target_ref,
            topology=topology,
            domain=(),
            target_domain_replay_ref=_derived_ref(
                "PRE553_COSIGNATURE_TARGET_DOMAIN_REPLAY",
                "target-domain-placeholder",
                {"target_ref": target_ref.as_dict(), "source_release_ref": release.release_ref.as_dict()},
            ),
            topology_authority_refs=(binding.topology_authority_ref,),
            response_semantic_authority_refs=(binding.semantic_authority_ref,),
            included_states=frozenset(states),
        )
        values: dict[str, Any] = {}
        domain_ok = True
        for respondent in sorted(index.respondents.values(), key=lambda item: item.ref.key):
            try:
                resolved, value = _target_component_value(
                    respondent, index, provisional, authority_registry, [], []
                )
            except (Pre553AuthorityError, Pre553IntegrityError):
                domain_ok = False
                break
            if resolved:
                material = canonicalize(value)
                values[canonical_json(material)] = material
        if not domain_ok:
            exclusions.append(TargetExclusion(target_ref, "RESPONSE_SEMANTICS_UNRESOLVED"))
            continue
        domain = tuple(values[key] for key in sorted(values))
        domain_replay = _derived_ref(
            "PRE553_COSIGNATURE_TARGET_DOMAIN_REPLAY",
            "target-domain",
            {
                "source_release_ref": release.release_ref.as_dict(),
                "universe_ref": universe_ref.as_dict(),
                "target_ref": target_ref.as_dict(),
                "topology": topology,
                "domain": list(domain),
                "states": list(states),
            },
        )
        candidate = GovernedSubstantiveTarget(
            target_ref=target_ref,
            instrument_question_version=binding.instrument_question_version,
            topology=topology,
            domain=domain,
            domain_replay_ref=domain_replay,
            semantic_authority_refs=(binding.semantic_authority_ref,),
            topology_authority_refs=(binding.topology_authority_ref,),
            routing_authority_refs=_auths(routing_auths),
            routing_rule_refs=_refs(routing_rules),
            included_states=states,
        )
        prior = by_target.get(target_ref.key)
        if prior is not None and prior.ref != candidate.ref:
            raise CosignatureCompositionError(
                "same target has conflicting governed instrument/topology descriptors"
            )
        by_target[target_ref.key] = candidate

    if not by_target:
        raise CosignatureCompositionError("no eligible governed substantive response targets")
    return GovernedTargetCatalog(
        branch_context_ref=context.ref,
        source_release_ref=release.release_ref,
        universe_ref=universe_ref,
        risk_set_ref=context.risk_set_ref,
        targets=tuple(by_target.values()),
        exclusions=tuple(exclusions),
    )


def enumerate_target_tuples(
    catalog: GovernedTargetCatalog,
    *,
    requested_arity: int,
    authority_maximum_target_arity_J: int,
    executor_maximum_target_arity_J: int = CURRENT_EXECUTOR_MAXIMUM_TARGET_ARITY_J,
) -> tuple[tuple[GovernedSubstantiveTarget, ...], ...]:
    """Enumerate the complete canonical target frontier for one exact arity."""
    if not isinstance(requested_arity, int) or requested_arity < 1:
        raise CosignatureCompositionError("requested target arity must be positive")
    if requested_arity > authority_maximum_target_arity_J:
        raise CosignatureCompositionError("requested target arity exceeds exact authority")
    if requested_arity > executor_maximum_target_arity_J:
        raise CosignatureCompositionError(
            "requested target arity exceeds currently integrated executor capability"
        )
    return tuple(combinations(catalog.targets, requested_arity))


def compose_branch_target_query(
    *,
    context: BranchCosignatureContext,
    catalog: GovernedTargetCatalog,
    targets: Sequence[GovernedSubstantiveTarget],
    policy: CosignatureCompositionPolicy,
    executor_maximum_target_arity_J: int = CURRENT_EXECUTOR_MAXIMUM_TARGET_ARITY_J,
) -> EmpiricalQuerySpec:
    targets = tuple(sorted(targets, key=lambda target: target.target_ref.key))
    if not targets:
        raise CosignatureCompositionError("target tuple cannot be empty")
    if len({target.target_ref.key for target in targets}) != len(targets):
        raise CosignatureCompositionError("target tuple contains duplicate target")
    if len(targets) > policy.authority_maximum_target_arity_J:
        raise CosignatureCompositionError("target tuple exceeds Authority-37 policy")
    if len(targets) > executor_maximum_target_arity_J:
        raise CosignatureCompositionError(
            "target tuple exceeds currently integrated executor capability"
        )
    for target in targets:
        if catalog.require_target(target.target_ref).ref != target.ref:
            raise CosignatureCompositionError("caller attempted target descriptor injection")
    replay = _derived_ref("PRE553_I04_COSIGNATURE_QUERY_REPLAY", "query-replay", {
        "contract_id": COSIGNATURE_COMPOSITION_CONTRACT_ID,
        "branch_context_ref": context.ref.as_dict(),
        "catalog_ref": catalog.ref.as_dict(),
        "target_refs": [target.ref.as_dict() for target in targets],
        "policy_ref": policy.ref.as_dict(),
    })
    grain: dict[str, Any] = {
        "source_scope_mode": "SINGLE_UNIVERSE",
        "measure_kind": policy.measure_kind,
        "risk_set_type": (
            "WHOLE_QUESTION_RISK_SET"
            if len(targets) == 1 else "COMMON_ELIGIBLE_RISK_SET"
        ),
        "response_state_semantics_ref": policy.response_state_semantics_ref.as_dict(),
        "uncertainty_method_or_typed_state": policy.uncertainty_method_or_typed_state,
    }
    if policy.measure_kind == "GOVERNED_WEIGHTED":
        grain["weight_basis_id"] = policy.weight_basis_id
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=_auths(
            (policy.topology_authority_ref, *policy.query_authority_refs)
        ),
        dependency_refs=_refs((
            context.branch_predicate.ref,
            context.branch_replay_ref,
            catalog.ref,
            policy.ref,
            *context.source_release_refs,
            *(target.ref for target in targets),
        )),
        producer_replay_locator_or_reference_root=replay,
        target_refs=tuple(target.target_ref for target in targets),
        target_arity_and_topology={
            "arity": len(targets),
            "joint_order_semantics": "CANONICAL_SET_ORDER",
            "components": [target.component() for target in targets],
        },
        condition_predicate_ref=context.branch_predicate.ref,
        risk_set_ref=context.risk_set_ref,
        empirical_universe_refs=context.universe_refs,
        scope_refs=context.universe_refs,
        measure_basis_ref=policy.measure_basis_ref,
        requested_output_grain=grain,
        query_authority_refs=policy.query_authority_refs,
        cosignature_target_catalog_ref=catalog.ref,
        cosignature_branch_context_ref=context.ref,
        cosignature_policy_ref=policy.ref,
    )


@dataclass(frozen=True)
class ExecutedCosignatureQuery:
    target_refs: tuple[ExactRef, ...]
    query: EmpiricalQuerySpec
    result: QueryExecutionResult

    def __post_init__(self) -> None:
        refs = tuple(exact_ref(ref) for ref in self.target_refs)
        if refs != tuple(sorted(refs, key=lambda ref: ref.key)):
            raise CosignatureCompositionError("executed target refs are not canonical")
        object.__setattr__(self, "target_refs", refs)
        if self.query.ref != self.result.query_ref:
            raise CosignatureCompositionError("query/result identity mismatch")
        if tuple(exact_ref(ref) for ref in self.query.target_refs) != refs:
            raise CosignatureCompositionError("query target identity mismatch")
        if len(self.result.facts) != 1:
            raise CosignatureCompositionError("single-universe I04 requires one fact")

    @property
    def fact(self) -> EmpiricalFact:
        return self.result.facts[0]


def _member_refs(fact: EmpiricalFact, field: str) -> tuple[ExactRef, ...] | None:
    value = fact.semantic_fields.get(field)
    if value is None:
        return None
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise CosignatureCompositionError(f"{field} must be exact-ref sequence")
    return _refs(exact_ref(item) for item in value)


def _validate_denominators(
    item: ExecutedCosignatureQuery, context: BranchCosignatureContext
) -> None:
    fact = item.fact
    if exact_ref(fact.condition_predicate_ref) != context.branch_predicate.ref:
        raise CosignatureCompositionError("branch predicate denominator substitution")
    if exact_ref(fact.risk_set_ref) != context.risk_set_ref:
        raise CosignatureCompositionError("risk denominator substitution")
    risk = _member_refs(fact, "risk_set_member_refs")
    denominator = _member_refs(fact, "denominator_member_refs")
    if risk is None or denominator is None:
        if (
            fact.typed_state not in NEGATIVE_NO_MEMBER_ENVELOPE
            or fact.raw_denominator_support != 0
        ):
            raise CosignatureCompositionError("fact lost exact denominator member envelope")
        return
    if fact.raw_denominator_support != len(denominator):
        raise CosignatureCompositionError(
            "raw denominator substituted for exact denominator-member count"
        )
    if not set(denominator).issubset(set(risk)):
        raise CosignatureCompositionError("branch denominator exceeds source/risk denominator")
    resolved = fact.semantic_fields.get("raw_resolved_target_support")
    if (
        not isinstance(resolved, int)
        or resolved < 0
        or resolved > fact.raw_denominator_support
    ):
        raise CosignatureCompositionError("resolved target denominator invalid")
    if fact.raw_numerator_support != resolved:
        raise CosignatureCompositionError("resolved support/raw numerator mismatch")


def _validate_j3_denominator_contract(
    joint: ExecutedCosignatureQuery,
    marginal_items: Sequence[ExecutedCosignatureQuery],
) -> None:
    fact = joint.fact
    topology = fact.target_topology
    if topology.get("higher_order_evidence_semantics") != "DIRECT_EXACT_SAME_RESPONDENT_THREE_WAY_JOINT":
        raise CosignatureCompositionError("J3 fact is not direct exact same-respondent higher-order evidence")
    if topology.get("pairwise_projection_not_identity_equivalent") is not True:
        raise CosignatureCompositionError("J3 fact permits unlawful pairwise identity substitution")
    if _refs(topology.get("target_refs", ())) != joint.target_refs:
        raise CosignatureCompositionError("J3 fact target refs differ from exact query triple")
    material = topology.get("authority37_j3_denominators")
    if not isinstance(material, Mapping) or material.get("contract") != "AUTHORITY37_J3_DENOMINATOR_CONSERVATION@1.0.0":
        raise CosignatureCompositionError("J3 fact lost Authority-37 denominator contract")

    source_risk = material.get("source_risk")
    branch = material.get("branch")
    per_target = material.get("per_target")
    three_way = material.get("three_way_joint")
    if not isinstance(source_risk, Mapping) or not isinstance(branch, Mapping) or not isinstance(three_way, Mapping):
        raise CosignatureCompositionError("J3 denominator grains are incomplete")
    if isinstance(per_target, (str, bytes, bytearray)) or not isinstance(per_target, Sequence) or len(per_target) != 3:
        raise CosignatureCompositionError("J3 per-target denominator vector must have arity three")

    source_members = _refs(source_risk.get("member_refs", ()))
    branch_members = _refs(branch.get("member_refs", ()))
    joint_members = _refs(three_way.get("member_refs", ()))
    if source_risk.get("raw_denominator_support") != len(source_members):
        raise CosignatureCompositionError("J3 source/risk denominator count mismatch")
    if branch.get("raw_denominator_support") != len(branch_members):
        raise CosignatureCompositionError("J3 branch denominator count mismatch")
    if not set(branch_members).issubset(set(source_members)):
        raise CosignatureCompositionError("J3 branch denominator exceeds source/risk denominator")
    if three_way.get("raw_denominator_support") != len(joint_members):
        raise CosignatureCompositionError("J3 three-way denominator count mismatch")
    fact_den = _member_refs(fact, "denominator_member_refs")
    if fact_den is not None and joint_members != fact_den:
        raise CosignatureCompositionError("J3 three-way denominator differs from fact denominator")
    if _refs(three_way.get("target_refs", ())) != joint.target_refs:
        raise CosignatureCompositionError("J3 denominator target triple mismatch")

    for target_ref, row, marginal in zip(joint.target_refs, per_target, marginal_items):
        if not isinstance(row, Mapping) or exact_ref(row.get("target_ref")) != target_ref:
            raise CosignatureCompositionError("J3 per-target denominator target mismatch")
        members = _refs(row.get("member_refs", ()))
        if row.get("raw_denominator_support") != len(members):
            raise CosignatureCompositionError("J3 per-target denominator count mismatch")
        marginal_den = _member_refs(marginal.fact, "denominator_member_refs")
        if marginal_den is not None and members != marginal_den:
            raise CosignatureCompositionError("J3 per-target denominator differs from exact marginal")
        if not set(joint_members).issubset(set(members)):
            raise CosignatureCompositionError("J3 joint denominator exceeds a target denominator")

    seen: set[str] = set()
    for row in topology.get("complete_cell_semantic_projection", ()):
        if not isinstance(row, Mapping):
            raise CosignatureCompositionError("J3 cell projection must be exact mappings")
        members = _refs(row.get("exact_same_respondent_member_refs", ()))
        if row.get("raw_numerator_support") != len(members):
            raise CosignatureCompositionError("J3 cell support differs from exact membership")
        keys = {ref.key for ref in members}
        if seen.intersection(keys):
            raise CosignatureCompositionError("J3 respondent appears in multiple exact cells")
        seen.update(keys)
    if fact.typed_state == "SUPPORTED" and seen != {ref.key for ref in joint_members}:
        raise CosignatureCompositionError("supported J3 cells do not partition the exact joint denominator")


def _validate_joint(
    joint: ExecutedCosignatureQuery,
    marginals: Mapping[str, ExecutedCosignatureQuery],
) -> None:
    if len(joint.target_refs) not in {2, 3}:
        raise CosignatureCompositionError("higher-order validation supports only exact J2/J3")
    marginal_items = tuple(marginals[ref.key] for ref in joint.target_refs)
    joint_risk = _member_refs(joint.fact, "risk_set_member_refs")
    joint_den = _member_refs(joint.fact, "denominator_member_refs")
    marginal_risk = tuple(_member_refs(item.fact, "risk_set_member_refs") for item in marginal_items)
    marginal_den = tuple(_member_refs(item.fact, "denominator_member_refs") for item in marginal_items)
    if joint_risk is not None and all(value is not None for value in marginal_risk):
        common_risk = set(marginal_risk[0])  # type: ignore[arg-type]
        for values in marginal_risk[1:]:
            common_risk.intersection_update(values)  # type: ignore[arg-type]
        if not set(joint_risk).issubset(common_risk):
            raise CosignatureCompositionError(
                "joint risk denominator is not exact common target risk set"
            )
    if joint_den is not None and all(value is not None for value in marginal_den):
        common_den = set(marginal_den[0])  # type: ignore[arg-type]
        for values in marginal_den[1:]:
            common_den.intersection_update(values)  # type: ignore[arg-type]
        if not set(joint_den).issubset(common_den):
            raise CosignatureCompositionError(
                "joint branch denominator substituted non-common target members"
            )
    if len(joint.target_refs) == 3:
        _validate_j3_denominator_contract(joint, marginal_items)


@dataclass(frozen=True)
class BranchCosignatureTopologyClosureReceipt:
    branch_context_ref: ExactRef
    branch_predicate_ref: ExactRef
    immediate_parent_ref: ExactRef
    ancestry_refs: tuple[ExactRef, ...]
    branch_replay_ref: ExactRef
    source_release_ref: ExactRef
    universe_ref: ExactRef
    risk_set_ref: ExactRef
    source_risk_denominator_ref: ExactRef
    branch_denominator_ref: ExactRef
    target_catalog_ref: ExactRef
    policy_ref: ExactRef
    topology_authority_ref: AuthorityRef
    query_authority_refs: tuple[AuthorityRef, ...]
    routing_authority_refs: tuple[AuthorityRef, ...]
    response_semantic_authority_refs: tuple[AuthorityRef, ...]
    response_topology_authority_refs: tuple[AuthorityRef, ...]
    measure_basis_ref: ExactRef
    measure_authority_refs: tuple[AuthorityRef, ...]
    ordered_target_refs: tuple[ExactRef, ...]
    marginal_query_refs: tuple[ExactRef, ...]
    marginal_fact_refs: tuple[ExactRef, ...]
    joint_query_refs: tuple[ExactRef, ...]
    joint_fact_refs: tuple[ExactRef, ...]
    triple_query_refs: tuple[ExactRef, ...]
    triple_fact_refs: tuple[ExactRef, ...]
    target_count: int
    expected_pair_count: int
    evaluated_pair_count: int
    expected_triple_count: int
    evaluated_triple_count: int
    maximum_completed_target_arity_J: int
    coverage_state: str

    def __post_init__(self) -> None:
        for name in (
            "branch_context_ref", "branch_predicate_ref", "immediate_parent_ref",
            "branch_replay_ref", "source_release_ref", "universe_ref", "risk_set_ref",
            "source_risk_denominator_ref", "branch_denominator_ref",
            "target_catalog_ref", "policy_ref", "measure_basis_ref",
        ):
            object.__setattr__(self, name, exact_ref(getattr(self, name)))
        for name in (
            "ancestry_refs", "ordered_target_refs", "marginal_query_refs",
            "marginal_fact_refs", "joint_query_refs", "joint_fact_refs",
            "triple_query_refs", "triple_fact_refs",
        ):
            object.__setattr__(self, name, _refs(getattr(self, name)))
        for name in (
            "query_authority_refs", "routing_authority_refs",
            "response_semantic_authority_refs", "response_topology_authority_refs",
            "measure_authority_refs",
        ):
            object.__setattr__(self, name, _auths(getattr(self, name)))
        if self.target_count != len(self.ordered_target_refs):
            raise CosignatureCompositionError("closure target count mismatch")
        if (
            self.expected_pair_count != self.evaluated_pair_count
            or self.evaluated_pair_count != len(self.joint_query_refs)
            or len(self.joint_query_refs) != len(self.joint_fact_refs)
        ):
            raise CosignatureCompositionError("incomplete J2 target frontier")
        if (
            len(self.marginal_query_refs) != self.target_count
            or len(self.marginal_fact_refs) != self.target_count
        ):
            raise CosignatureCompositionError("marginal target coverage incomplete")
        if (
            self.expected_triple_count != self.evaluated_triple_count
            or self.evaluated_triple_count != len(self.triple_query_refs)
            or len(self.triple_query_refs) != len(self.triple_fact_refs)
        ):
            raise CosignatureCompositionError("incomplete J3 target frontier")
        if self.maximum_completed_target_arity_J not in {2, 3}:
            raise CosignatureCompositionError("closure maximum completed target arity must be J2 or J3")
        if self.maximum_completed_target_arity_J == 2 and self.expected_triple_count != 0:
            raise CosignatureCompositionError("J2 closure cannot claim J3 tuples")
        expected_state = (
            "COMPLETE_FOR_AUTHORIZED_J1_TO_J3_TARGET_FRONTIER"
            if self.maximum_completed_target_arity_J == 3
            else "COMPLETE_FOR_AUTHORIZED_J1_TO_J2_TARGET_FRONTIER"
        )
        if self.coverage_state != expected_state:
            raise CosignatureCompositionError("unknown topology closure state")

    def _base(self) -> dict[str, Any]:
        return {
            "contract_id": TOPOLOGY_CLOSURE_CONTRACT_ID,
            "branch_context_ref": self.branch_context_ref.as_dict(),
            "branch_predicate_ref": self.branch_predicate_ref.as_dict(),
            "immediate_parent_ref": self.immediate_parent_ref.as_dict(),
            "ancestry_refs": [ref.as_dict() for ref in self.ancestry_refs],
            "branch_replay_ref": self.branch_replay_ref.as_dict(),
            "source_release_ref": self.source_release_ref.as_dict(),
            "universe_ref": self.universe_ref.as_dict(),
            "risk_set_ref": self.risk_set_ref.as_dict(),
            "source_risk_denominator_ref": self.source_risk_denominator_ref.as_dict(),
            "branch_denominator_ref": self.branch_denominator_ref.as_dict(),
            "target_catalog_ref": self.target_catalog_ref.as_dict(),
            "policy_ref": self.policy_ref.as_dict(),
            "topology_authority_ref": self.topology_authority_ref.as_dict(),
            "query_authority_refs": [ref.as_dict() for ref in self.query_authority_refs],
            "routing_authority_refs": [ref.as_dict() for ref in self.routing_authority_refs],
            "response_semantic_authority_refs": [
                ref.as_dict() for ref in self.response_semantic_authority_refs
            ],
            "response_topology_authority_refs": [
                ref.as_dict() for ref in self.response_topology_authority_refs
            ],
            "measure_basis_ref": self.measure_basis_ref.as_dict(),
            "measure_authority_refs": [
                ref.as_dict() for ref in self.measure_authority_refs
            ],
            "ordered_target_refs": [ref.as_dict() for ref in self.ordered_target_refs],
            "marginal_query_refs": [ref.as_dict() for ref in self.marginal_query_refs],
            "marginal_fact_refs": [ref.as_dict() for ref in self.marginal_fact_refs],
            "joint_query_refs": [ref.as_dict() for ref in self.joint_query_refs],
            "joint_fact_refs": [ref.as_dict() for ref in self.joint_fact_refs],
            "triple_query_refs": [ref.as_dict() for ref in self.triple_query_refs],
            "triple_fact_refs": [ref.as_dict() for ref in self.triple_fact_refs],
            "target_count": self.target_count,
            "expected_pair_count": self.expected_pair_count,
            "evaluated_pair_count": self.evaluated_pair_count,
            "expected_triple_count": self.expected_triple_count,
            "evaluated_triple_count": self.evaluated_triple_count,
            "maximum_completed_target_arity_J": self.maximum_completed_target_arity_J,
            "coverage_state": self.coverage_state,
            "copied_empirical_payload": False,
        }

    @property
    def replay_ref(self) -> ExactRef:
        return _derived_ref(
            "PRE553_I04_COSIGNATURE_TOPOLOGY_REPLAY",
            "topology-replay",
            self._base(),
        )

    @property
    def content_hash(self) -> str:
        return semantic_hash({**self._base(), "replay_ref": self.replay_ref.as_dict()})

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            TOPOLOGY_CLOSURE_CONTRACT_ID,
            f"urn:rawlsing:pre553:i04-cosignature:topology-closure:sha256:{self.content_hash}",
            self.content_hash,
        )

    def semantic_projection(self) -> dict[str, Any]:
        return {**self._base(), "replay_ref": self.replay_ref.as_dict()}


def _measure_authorities(
    repository: C11Repository,
    context: BranchCosignatureContext,
    policy: CosignatureCompositionPolicy,
    registry: AuthorityRegistry,
) -> tuple[AuthorityRef, ...]:
    if policy.measure_kind == "RAW":
        return ()
    release = repository.resolve_release_exact(context.source_release_refs[0])
    refs: list[AuthorityRef] = []
    for obj in release.public_objects:
        if not isinstance(obj, WeightMeasureFact):
            continue
        if (
            exact_ref(obj.empirical_universe_ref) != context.universe_refs[0]
            or obj.weight_basis_id != policy.weight_basis_id
        ):
            continue
        validate_object_authority_closure(obj, registry)
        for name in ("design_authority_ref", "estimand_authority_ref"):
            ref = _auth_from(obj.semantic_fields[name])
            snapshot = registry.resolve_exact(ref).snapshot
            if snapshot.typed_state != "ALLOW" or snapshot.authority_kind != "WEIGHT_DESIGN_ESTIMAND":
                raise CosignatureCompositionError("weight authority is not positive")
            refs.append(ref)
    if not refs:
        raise CosignatureCompositionError("weighted composition lacks exact weight authority")
    return _auths(refs)


def seal_branch_cosignature_closure(
    *,
    repository: C11Repository,
    context: BranchCosignatureContext,
    catalog: GovernedTargetCatalog,
    policy: CosignatureCompositionPolicy,
    marginals: Sequence[ExecutedCosignatureQuery],
    joints: Sequence[ExecutedCosignatureQuery],
    triples: Sequence[ExecutedCosignatureQuery] = (),
    authority_registry: AuthorityRegistry,
) -> BranchCosignatureTopologyClosureReceipt:
    _policy_authority(policy, authority_registry)
    for item in (*marginals, *joints, *triples):
        _validate_denominators(item, context)

    marginal_map: dict[str, ExecutedCosignatureQuery] = {}
    for item in marginals:
        if len(item.target_refs) != 1 or item.target_refs[0].key in marginal_map:
            raise CosignatureCompositionError("invalid or duplicate marginal")
        marginal_map[item.target_refs[0].key] = item
    if set(marginal_map) != {target.target_ref.key for target in catalog.targets}:
        raise CosignatureCompositionError("marginals do not cover governed catalog")

    expected = enumerate_target_tuples(
        catalog,
        requested_arity=2,
        authority_maximum_target_arity_J=policy.authority_maximum_target_arity_J,
    )
    expected_keys = {
        tuple(target.target_ref.key for target in pair) for pair in expected
    }
    actual_keys: set[tuple[str, str]] = set()
    for item in joints:
        if len(item.target_refs) != 2:
            raise CosignatureCompositionError("joint arity must be two")
        key = tuple(ref.key for ref in item.target_refs)
        if key in actual_keys:
            raise CosignatureCompositionError("duplicate joint")
        actual_keys.add(key)
        _validate_joint(item, marginal_map)
    if actual_keys != expected_keys:
        raise CosignatureCompositionError(
            "joint results do not cover complete governed target frontier"
        )

    expected_triples = (
        enumerate_target_tuples(
            catalog,
            requested_arity=3,
            authority_maximum_target_arity_J=policy.authority_maximum_target_arity_J,
        )
        if policy.authority_maximum_target_arity_J >= 3 else ()
    )
    expected_triple_keys = {
        tuple(target.target_ref.key for target in triple) for triple in expected_triples
    }
    actual_triple_keys: set[tuple[str, ...]] = set()
    for item in triples:
        if len(item.target_refs) != 3:
            raise CosignatureCompositionError("triple arity must be three")
        key = tuple(ref.key for ref in item.target_refs)
        if key in actual_triple_keys:
            raise CosignatureCompositionError("duplicate J3 triple")
        actual_triple_keys.add(key)
        _validate_joint(item, marginal_map)
    if actual_triple_keys != expected_triple_keys:
        raise CosignatureCompositionError(
            "J3 results do not cover complete governed target frontier"
        )

    routing = _auths(
        ref for target in catalog.targets for ref in target.routing_authority_refs
    )
    response_semantics = _auths(
        ref for target in catalog.targets for ref in target.semantic_authority_refs
    )
    response_topology = _auths(
        ref for target in catalog.targets for ref in target.topology_authority_refs
    )
    source_risk = _derived_ref(
        "PRE553_COSIGNATURE_SOURCE_RISK_DENOMINATOR",
        "source-risk-denominator",
        {
            "release_ref": context.source_release_refs[0].as_dict(),
            "universe_ref": context.universe_refs[0].as_dict(),
            "risk_set_ref": context.risk_set_ref.as_dict(),
        },
    )
    branch_denominator = _derived_ref(
        "PRE553_COSIGNATURE_BRANCH_DENOMINATOR",
        "branch-denominator",
        {
            "branch_predicate_ref": context.branch_predicate.ref.as_dict(),
            "branch_replay_ref": context.branch_replay_ref.as_dict(),
            "risk_set_ref": context.risk_set_ref.as_dict(),
        },
    )
    return BranchCosignatureTopologyClosureReceipt(
        branch_context_ref=context.ref,
        branch_predicate_ref=context.branch_predicate.ref,
        immediate_parent_ref=context.immediate_parent_ref,
        ancestry_refs=context.ancestry_refs,
        branch_replay_ref=context.branch_replay_ref,
        source_release_ref=context.source_release_refs[0],
        universe_ref=context.universe_refs[0],
        risk_set_ref=context.risk_set_ref,
        source_risk_denominator_ref=source_risk,
        branch_denominator_ref=branch_denominator,
        target_catalog_ref=catalog.ref,
        policy_ref=policy.ref,
        topology_authority_ref=policy.topology_authority_ref,
        query_authority_refs=policy.query_authority_refs,
        routing_authority_refs=routing,
        response_semantic_authority_refs=response_semantics,
        response_topology_authority_refs=response_topology,
        measure_basis_ref=policy.measure_basis_ref,
        measure_authority_refs=_measure_authorities(
            repository, context, policy, authority_registry
        ),
        ordered_target_refs=tuple(target.target_ref for target in catalog.targets),
        marginal_query_refs=tuple(item.query.ref for item in marginals),
        marginal_fact_refs=tuple(item.fact.ref for item in marginals),
        joint_query_refs=tuple(item.query.ref for item in joints),
        joint_fact_refs=tuple(item.fact.ref for item in joints),
        triple_query_refs=tuple(item.query.ref for item in triples),
        triple_fact_refs=tuple(item.fact.ref for item in triples),
        target_count=catalog.target_count,
        expected_pair_count=len(expected),
        evaluated_pair_count=len(joints),
        expected_triple_count=len(expected_triples),
        evaluated_triple_count=len(triples),
        maximum_completed_target_arity_J=(
            3 if policy.authority_maximum_target_arity_J >= 3 else 2
        ),
        coverage_state=(
            "COMPLETE_FOR_AUTHORIZED_J1_TO_J3_TARGET_FRONTIER"
            if policy.authority_maximum_target_arity_J >= 3
            else "COMPLETE_FOR_AUTHORIZED_J1_TO_J2_TARGET_FRONTIER"
        ),
    )


@dataclass(frozen=True)
class BranchCosignatureCompositionResult:
    target_catalog: GovernedTargetCatalog
    marginal_queries: tuple[ExecutedCosignatureQuery, ...]
    joint_queries: tuple[ExecutedCosignatureQuery, ...]
    triple_queries: tuple[ExecutedCosignatureQuery, ...]
    closure_receipt: BranchCosignatureTopologyClosureReceipt

    def joint_for(
        self,
        left: ExactRef | Mapping[str, Any],
        right: ExactRef | Mapping[str, Any],
    ) -> ExecutedCosignatureQuery:
        refs = tuple(sorted((exact_ref(left), exact_ref(right)), key=lambda ref: ref.key))
        for item in self.joint_queries:
            if item.target_refs == refs:
                return item
        raise KeyError("pair is not in exact completed target frontier")

    def triple_for(
        self,
        first: ExactRef | Mapping[str, Any],
        second: ExactRef | Mapping[str, Any],
        third: ExactRef | Mapping[str, Any],
    ) -> ExecutedCosignatureQuery:
        refs = tuple(sorted(
            (exact_ref(first), exact_ref(second), exact_ref(third)),
            key=lambda ref: ref.key,
        ))
        for item in self.triple_queries:
            if item.target_refs == refs:
                return item
        raise KeyError("triple is not in exact completed target frontier")


def compose_branch_cosignatures(
    *,
    repository: C11Repository,
    context: BranchCosignatureContext,
    authority_registry: AuthorityRegistry,
    policy: CosignatureCompositionPolicy,
) -> BranchCosignatureCompositionResult:
    """Enumerate all lawful targets, execute every J1 marginal/J2 pair, and seal."""
    _policy_authority(policy, authority_registry)
    if policy.authority_maximum_target_arity_J < 2:
        raise CosignatureCompositionError("J2 authority required for I04 R1")
    catalog = enumerate_governed_substantive_targets(
        repository=repository,
        context=context,
        authority_registry=authority_registry,
    )
    marginals: list[ExecutedCosignatureQuery] = []
    joints: list[ExecutedCosignatureQuery] = []
    triples: list[ExecutedCosignatureQuery] = []
    execution_plan = [(1, marginals), (2, joints)]
    if policy.authority_maximum_target_arity_J >= 3:
        execution_plan.append((3, triples))
    for arity, sink in execution_plan:
        for target_tuple in enumerate_target_tuples(
            catalog,
            requested_arity=arity,
            authority_maximum_target_arity_J=policy.authority_maximum_target_arity_J,
        ):
            query = compose_branch_target_query(
                context=context,
                catalog=catalog,
                targets=target_tuple,
                policy=policy,
            )
            result = execute_empirical_query(
                repository=repository,
                query=query,
                predicate=context.branch_predicate,
                authority_registry=authority_registry,
                release_refs=context.source_release_refs,
            )
            sink.append(ExecutedCosignatureQuery(
                target_refs=tuple(target.target_ref for target in target_tuple),
                query=query,
                result=result,
            ))
    closure = seal_branch_cosignature_closure(
        repository=repository,
        context=context,
        catalog=catalog,
        policy=policy,
        marginals=marginals,
        joints=joints,
        triples=triples,
        authority_registry=authority_registry,
    )
    return BranchCosignatureCompositionResult(
        target_catalog=catalog,
        marginal_queries=tuple(marginals),
        joint_queries=tuple(joints),
        triple_queries=tuple(triples),
        closure_receipt=closure,
    )


__all__ = [
    "COSIGNATURE_COMPOSITION_CONTRACT_ID",
    "TARGET_CATALOG_CONTRACT_ID",
    "TOPOLOGY_CLOSURE_CONTRACT_ID",
    "CURRENT_EXECUTOR_MAXIMUM_TARGET_ARITY_J",
    "AUTHORITY37_MAXIMUM_TARGET_ARITY_J",
    "CosignatureCompositionError",
    "BranchCosignatureContext",
    "TargetExclusion",
    "GovernedSubstantiveTarget",
    "GovernedTargetCatalog",
    "CosignatureCompositionPolicy",
    "ExecutedCosignatureQuery",
    "BranchCosignatureTopologyClosureReceipt",
    "BranchCosignatureCompositionResult",
    "enumerate_governed_substantive_targets",
    "enumerate_target_tuples",
    "compose_branch_target_query",
    "seal_branch_cosignature_closure",
    "compose_branch_cosignatures",
]
