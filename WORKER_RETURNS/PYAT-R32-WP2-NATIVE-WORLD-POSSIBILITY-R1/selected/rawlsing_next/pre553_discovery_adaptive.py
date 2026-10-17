"""PRE553 adaptive exploratory discovery scheduling and deterministic replay.

This is the inherited second discovery mode, separate from exact-bounded I05.
Adaptive exploration schedules only sealed evaluation units. Results may add or
prioritize later units only after the current unit closes. Partial/unvisited
territory remains unknown and can never become a negative empirical claim.
Search ranking has zero semantic-truth authority; learned facts still require
the normal exact empirical validation/authority path. This module has no
actor/V3 effect and does not import or mutate exact I05 internals.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    DiscoveryAuthority,
    ExactRef,
    Pre553IntegrityError,
    ReplayReceipt,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)

ADAPTIVE_DISCOVERY_CONTRACT_ID = "PRE553_ADAPTIVE_EXPLORATORY_DISCOVERY@1.0.0"
ADAPTIVE_SEARCH_SCHEMA = "PRE553_ADAPTIVE_SEARCH_UNIVERSE@1.0.0"
ADAPTIVE_SEARCH_POLICY_SCHEMA = "PRE553_ADAPTIVE_SEARCH_POLICY@1.0.0"
ADAPTIVE_COVERAGE_CLAIM = "EXACT_RESULTS__NONEXHAUSTIVE_FRONTIER_COVERAGE"
SEALED_UNIT_COVERAGE = "COMPLETE_SEALED_EVALUATION_UNIT"
TIE_ORDER_RULE = "HEURISTIC_RANK_DESC_THEN_UNIT_REF"
RANKING_RULE = "DECLARED_HEURISTIC_RANK_DESC_THEN_UNIT_REF"
PRUNING_KIND = "ADAPTIVE_PARTIAL_SEARCH_BETWEEN_SEALED_UNITS"

SEARCH_COMPLETENESS_STATES = frozenset({
    "PARTIAL_BUDGET_EXHAUSTED",
    "PARTIAL_INTERRUPTED",
    "EXPLORATORY_POLICY_FRONTIER_EXHAUSTED",
})
PARTIAL_SEARCH_STATES = frozenset({"PARTIAL_BUDGET_EXHAUSTED", "PARTIAL_INTERRUPTED"})

ADAPTIVE_SEARCH_COMPLETENESS_CONTRACT: Mapping[str, Any] = {
    "schema": "PRE553_ADAPTIVE_SEARCH_COMPLETENESS@1.0.0",
    "authoritative_exact_mode": "UNCHANGED_PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0",
    "adaptive_mode": ADAPTIVE_DISCOVERY_CONTRACT_ID,
    "unit_rule": "one unit is fully sealed before any result-driven frontier change",
    "partial_negative_rule": "FORBIDDEN",
    "unvisited_state": "EXPLICIT_UNKNOWN_UNVISITED",
    "ranking_authority": "SEARCH_ORDER_ONLY__NEVER_EMPIRICAL_OR_STRUCTURAL_TRUTH",
    "terminal_exhaustion_meaning": (
        "all units reachable under the frozen exploratory policy were visited; "
        "this is not authoritative global empirical absence"
    ),
    "promotion_rule": "EXACT_EMPIRICAL_VALIDATION_AND_AUTHORITY_REQUIRED_OUTSIDE_THIS_SERVICE",
    "actor_v3_effect": False,
}


class AdaptiveDiscoveryError(Pre553IntegrityError):
    pass


class AdaptiveSearchIdentityError(AdaptiveDiscoveryError):
    pass


class PartialSearchNegativeError(AdaptiveDiscoveryError):
    pass


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AdaptiveDiscoveryError(f"{name} must be a non-empty string")
    return value.strip()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise AdaptiveDiscoveryError(f"{name} must be an exact mapping")
    return value


def _sequence(value: Any, name: str, *, allow_empty: bool = False) -> Sequence[Any]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise AdaptiveDiscoveryError(f"{name} must be a sequence")
    if not allow_empty and not value:
        raise AdaptiveDiscoveryError(f"{name} may not be empty")
    return value


def _derived_ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:pre553:adaptive:{namespace}:sha256:{digest}", digest)


def _canonical_refs(values: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    return tuple(sorted(set(values), key=lambda ref: ref.key))


def _optional_ref(value: Any, name: str) -> ExactRef | None:
    return None if value is None else exact_ref(value, name)


@dataclass(frozen=True)
class AdaptiveExplorationUnit:
    """Opaque sealed evaluation request; heuristic_rank affects search order only."""
    unit_ref: ExactRef
    proposal_rule_ref: ExactRef
    generation: int
    heuristic_rank: int
    determinant_refs: tuple[ExactRef, ...]
    parent_unit_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "unit_ref", exact_ref(self.unit_ref, "unit_ref"))
        object.__setattr__(self, "proposal_rule_ref", exact_ref(self.proposal_rule_ref, "proposal_rule_ref"))
        if not isinstance(self.generation, int) or isinstance(self.generation, bool) or self.generation < 0:
            raise AdaptiveDiscoveryError("generation must be a nonnegative exact integer")
        if not isinstance(self.heuristic_rank, int) or isinstance(self.heuristic_rank, bool):
            raise AdaptiveDiscoveryError("heuristic_rank must be an exact integer")
        refs = _canonical_refs(exact_ref(ref, "determinant_ref") for ref in self.determinant_refs)
        if not refs:
            raise AdaptiveDiscoveryError("exploration unit requires determinant_refs")
        object.__setattr__(self, "determinant_refs", refs)
        parent = _optional_ref(self.parent_unit_ref, "parent_unit_ref")
        object.__setattr__(self, "parent_unit_ref", parent)
        if self.generation == 0 and parent is not None:
            raise AdaptiveDiscoveryError("generation-0 root unit cannot have parent_unit_ref")
        if self.generation > 0 and parent is None:
            raise AdaptiveDiscoveryError("non-root exploration unit requires exact parent_unit_ref")

    def as_dict(self) -> dict[str, Any]:
        return canonicalize({
            "unit_ref": self.unit_ref,
            "proposal_rule_ref": self.proposal_rule_ref,
            "generation": self.generation,
            "heuristic_rank": self.heuristic_rank,
            "determinant_refs": self.determinant_refs,
            "parent_unit_ref": self.parent_unit_ref,
        })

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "AdaptiveExplorationUnit":
        value = _mapping(value, "AdaptiveExplorationUnit")
        return cls(
            unit_ref=exact_ref(value.get("unit_ref"), "unit_ref"),
            proposal_rule_ref=exact_ref(value.get("proposal_rule_ref"), "proposal_rule_ref"),
            generation=value.get("generation"),
            heuristic_rank=value.get("heuristic_rank"),
            determinant_refs=tuple(
                exact_ref(ref, "determinant_ref")
                for ref in _sequence(value.get("determinant_refs", ()), "determinant_refs")
            ),
            parent_unit_ref=_optional_ref(value.get("parent_unit_ref"), "parent_unit_ref"),
        )


@dataclass(frozen=True)
class AdaptiveUnitOutcome:
    """One complete sealed result plus proposals for later exploration only."""
    unit_ref: ExactRef
    sealed_result_ref: ExactRef
    proposal_basis_ref: ExactRef
    unit_result_state: str
    proposal_units: tuple[AdaptiveExplorationUnit, ...] = ()
    sealed_unit_coverage: str = SEALED_UNIT_COVERAGE
    global_negative_claim: bool = False
    semantic_truth_effect: bool = False
    actor_v3_effect: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "unit_ref", exact_ref(self.unit_ref, "unit_ref"))
        object.__setattr__(self, "sealed_result_ref", exact_ref(self.sealed_result_ref, "sealed_result_ref"))
        object.__setattr__(self, "proposal_basis_ref", exact_ref(self.proposal_basis_ref, "proposal_basis_ref"))
        object.__setattr__(self, "unit_result_state", _text(self.unit_result_state, "unit_result_state"))
        if self.sealed_unit_coverage != SEALED_UNIT_COVERAGE:
            raise AdaptiveDiscoveryError("adaptive scheduling may consume only complete sealed evaluation units")
        proposals = tuple(sorted(self.proposal_units, key=lambda unit: unit.unit_ref.key))
        if len({unit.unit_ref.key for unit in proposals}) != len(proposals):
            raise AdaptiveDiscoveryError("outcome contains duplicate proposal unit refs")
        object.__setattr__(self, "proposal_units", proposals)
        if self.global_negative_claim:
            raise PartialSearchNegativeError("adaptive outcome may not claim global empirical absence")
        if self.semantic_truth_effect:
            raise AdaptiveDiscoveryError("adaptive heuristic outcome cannot itself create semantic truth")
        if self.actor_v3_effect:
            raise AdaptiveDiscoveryError("adaptive discovery has zero actor/V3 effect")

    def semantic_material(self) -> Mapping[str, Any]:
        return canonicalize({
            "unit_ref": self.unit_ref,
            "sealed_result_ref": self.sealed_result_ref,
            "proposal_basis_ref": self.proposal_basis_ref,
            "unit_result_state": self.unit_result_state,
            "proposal_units": [unit.as_dict() for unit in self.proposal_units],
            "sealed_unit_coverage": self.sealed_unit_coverage,
            "global_negative_claim": False,
            "semantic_truth_effect": False,
            "actor_v3_effect": False,
        })

    @property
    def ref(self) -> ExactRef:
        return _derived_ref("PRE553_ADAPTIVE_UNIT_OUTCOME", "unit-outcome", self.semantic_material())

    def as_dict(self) -> dict[str, Any]:
        return dict(self.semantic_material())

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "AdaptiveUnitOutcome":
        value = _mapping(value, "AdaptiveUnitOutcome")
        return cls(
            unit_ref=exact_ref(value.get("unit_ref"), "unit_ref"),
            sealed_result_ref=exact_ref(value.get("sealed_result_ref"), "sealed_result_ref"),
            proposal_basis_ref=exact_ref(value.get("proposal_basis_ref"), "proposal_basis_ref"),
            unit_result_state=value.get("unit_result_state"),
            proposal_units=tuple(
                AdaptiveExplorationUnit.from_dict(item)
                for item in _sequence(value.get("proposal_units", ()), "proposal_units", allow_empty=True)
            ),
            sealed_unit_coverage=value.get("sealed_unit_coverage", SEALED_UNIT_COVERAGE),
            global_negative_claim=bool(value.get("global_negative_claim", False)),
            semantic_truth_effect=bool(value.get("semantic_truth_effect", False)),
            actor_v3_effect=bool(value.get("actor_v3_effect", False)),
        )


@dataclass(frozen=True)
class AdaptiveVisit:
    ordinal: int
    unit: AdaptiveExplorationUnit
    outcome: AdaptiveUnitOutcome

    def __post_init__(self) -> None:
        if not isinstance(self.ordinal, int) or isinstance(self.ordinal, bool) or self.ordinal < 0:
            raise AdaptiveDiscoveryError("visit ordinal must be a nonnegative exact integer")
        if self.outcome.unit_ref != self.unit.unit_ref:
            raise AdaptiveDiscoveryError("unit outcome does not belong to visited unit")

    def as_dict(self) -> dict[str, Any]:
        return canonicalize({"ordinal": self.ordinal, "unit": self.unit.as_dict(), "outcome": self.outcome.as_dict()})

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "AdaptiveVisit":
        value = _mapping(value, "AdaptiveVisit")
        return cls(
            ordinal=value.get("ordinal"),
            unit=AdaptiveExplorationUnit.from_dict(_mapping(value.get("unit"), "visit.unit")),
            outcome=AdaptiveUnitOutcome.from_dict(_mapping(value.get("outcome"), "visit.outcome")),
        )


@dataclass(frozen=True)
class AdaptiveSearchCheckpoint:
    discovery_authority_ref: ExactRef
    search_policy_ref: ExactRef
    determinant_state_ref: ExactRef
    root_unit_refs: tuple[ExactRef, ...]
    known_units: tuple[AdaptiveExplorationUnit, ...]
    visits: tuple[AdaptiveVisit, ...]
    completeness_state: str
    stop_reason: str
    global_negative_claim: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "discovery_authority_ref", exact_ref(self.discovery_authority_ref, "discovery_authority_ref"))
        object.__setattr__(self, "search_policy_ref", exact_ref(self.search_policy_ref, "search_policy_ref"))
        object.__setattr__(self, "determinant_state_ref", exact_ref(self.determinant_state_ref, "determinant_state_ref"))
        roots = _canonical_refs(exact_ref(ref, "root_unit_ref") for ref in self.root_unit_refs)
        if not roots:
            raise AdaptiveDiscoveryError("adaptive checkpoint requires one or more root units")
        object.__setattr__(self, "root_unit_refs", roots)
        units = tuple(sorted(self.known_units, key=lambda unit: unit.unit_ref.key))
        if len({unit.unit_ref.key for unit in units}) != len(units):
            raise AdaptiveDiscoveryError("checkpoint known units contain duplicate refs")
        object.__setattr__(self, "known_units", units)
        known = {unit.unit_ref.key: unit for unit in units}
        if any(root.key not in known for root in roots):
            raise AdaptiveDiscoveryError("checkpoint root ref is absent from known units")
        visits = tuple(self.visits)
        if [visit.ordinal for visit in visits] != list(range(len(visits))):
            raise AdaptiveDiscoveryError("checkpoint visit ordinals must be contiguous from zero")
        visited_keys = [visit.unit.unit_ref.key for visit in visits]
        if len(set(visited_keys)) != len(visited_keys):
            raise AdaptiveDiscoveryError("checkpoint may not visit one unit twice")
        if any(key not in known for key in visited_keys):
            raise AdaptiveDiscoveryError("checkpoint visit refers to unknown unit")
        object.__setattr__(self, "visits", visits)
        if self.completeness_state not in SEARCH_COMPLETENESS_STATES:
            raise AdaptiveDiscoveryError("unknown adaptive search completeness state")
        object.__setattr__(self, "stop_reason", _text(self.stop_reason, "stop_reason"))
        if self.global_negative_claim:
            raise PartialSearchNegativeError("adaptive checkpoint can never authorize a global negative")
        if self.completeness_state == "EXPLORATORY_POLICY_FRONTIER_EXHAUSTED" and self.unvisited_unit_refs:
            raise AdaptiveDiscoveryError("exhausted exploratory frontier cannot retain unvisited units")
        if self.completeness_state in PARTIAL_SEARCH_STATES and not self.unvisited_unit_refs:
            raise AdaptiveDiscoveryError("partial search state requires explicit unvisited territory")

    @property
    def visited_unit_refs(self) -> tuple[ExactRef, ...]:
        return tuple(visit.unit.unit_ref for visit in self.visits)

    @property
    def unvisited_unit_refs(self) -> tuple[ExactRef, ...]:
        visited = {ref.key for ref in self.visited_unit_refs}
        return tuple(unit.unit_ref for unit in self.known_units if unit.unit_ref.key not in visited)

    def semantic_material(self) -> Mapping[str, Any]:
        return canonicalize({
            "contract": ADAPTIVE_DISCOVERY_CONTRACT_ID,
            "discovery_authority_ref": self.discovery_authority_ref,
            "search_policy_ref": self.search_policy_ref,
            "determinant_state_ref": self.determinant_state_ref,
            "root_unit_refs": self.root_unit_refs,
            "known_units": [unit.as_dict() for unit in self.known_units],
            "visits": [visit.as_dict() for visit in self.visits],
            "visited_unit_refs": self.visited_unit_refs,
            "unvisited_unit_refs": self.unvisited_unit_refs,
            "completeness_state": self.completeness_state,
            "stop_reason": self.stop_reason,
            "global_negative_claim": False,
        })

    @property
    def ref(self) -> ExactRef:
        return _derived_ref("PRE553_ADAPTIVE_SEARCH_CHECKPOINT", "checkpoint", self.semantic_material())

    def as_dict(self) -> dict[str, Any]:
        return dict(self.semantic_material())

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "AdaptiveSearchCheckpoint":
        value = _mapping(value, "AdaptiveSearchCheckpoint")
        return cls(
            discovery_authority_ref=exact_ref(value.get("discovery_authority_ref"), "discovery_authority_ref"),
            search_policy_ref=exact_ref(value.get("search_policy_ref"), "search_policy_ref"),
            determinant_state_ref=exact_ref(value.get("determinant_state_ref"), "determinant_state_ref"),
            root_unit_refs=tuple(exact_ref(ref, "root_unit_ref") for ref in _sequence(value.get("root_unit_refs", ()), "root_unit_refs")),
            known_units=tuple(AdaptiveExplorationUnit.from_dict(item) for item in _sequence(value.get("known_units", ()), "known_units")),
            visits=tuple(AdaptiveVisit.from_dict(item) for item in _sequence(value.get("visits", ()), "visits", allow_empty=True)),
            completeness_state=value.get("completeness_state"),
            stop_reason=value.get("stop_reason"),
            global_negative_claim=bool(value.get("global_negative_claim", False)),
        )


@dataclass(frozen=True)
class AdaptiveSearchResult:
    discovery_authority_ref: ExactRef
    search_policy_ref: ExactRef
    determinant_state_ref: ExactRef
    checkpoint: AdaptiveSearchCheckpoint
    start_checkpoint_ref: ExactRef | None
    run_budget: int
    visited_this_run: tuple[ExactRef, ...]
    global_negative_claim: bool = False
    semantic_truth_effect: bool = False
    actor_v3_effect: bool = False

    def __post_init__(self) -> None:
        for name in ("discovery_authority_ref", "search_policy_ref", "determinant_state_ref"):
            object.__setattr__(self, name, exact_ref(getattr(self, name), name))
        object.__setattr__(self, "start_checkpoint_ref", _optional_ref(self.start_checkpoint_ref, "start_checkpoint_ref"))
        if not isinstance(self.run_budget, int) or isinstance(self.run_budget, bool) or self.run_budget < 0:
            raise AdaptiveDiscoveryError("run_budget must be a nonnegative exact integer")
        object.__setattr__(self, "visited_this_run", tuple(exact_ref(ref, "visited_this_run") for ref in self.visited_this_run))
        if self.discovery_authority_ref != self.checkpoint.discovery_authority_ref:
            raise AdaptiveSearchIdentityError("result/checkpoint discovery authority mismatch")
        if self.search_policy_ref != self.checkpoint.search_policy_ref:
            raise AdaptiveSearchIdentityError("result/checkpoint search policy mismatch")
        if self.determinant_state_ref != self.checkpoint.determinant_state_ref:
            raise AdaptiveSearchIdentityError("result/checkpoint determinant state mismatch")
        if self.global_negative_claim:
            raise PartialSearchNegativeError("adaptive result cannot claim global empirical absence")
        if self.semantic_truth_effect:
            raise AdaptiveDiscoveryError("adaptive search result cannot create semantic truth")
        if self.actor_v3_effect:
            raise AdaptiveDiscoveryError("adaptive search result has zero actor/V3 effect")

    @property
    def completeness_state(self) -> str:
        return self.checkpoint.completeness_state

    @property
    def stop_reason(self) -> str:
        return self.checkpoint.stop_reason

    @property
    def visited_unit_refs(self) -> tuple[ExactRef, ...]:
        return self.checkpoint.visited_unit_refs

    @property
    def unvisited_unit_refs(self) -> tuple[ExactRef, ...]:
        return self.checkpoint.unvisited_unit_refs

    @property
    def result_ref(self) -> ExactRef:
        return _derived_ref("PRE553_ADAPTIVE_SEARCH_RESULT", "result", {
            "contract": ADAPTIVE_DISCOVERY_CONTRACT_ID,
            "checkpoint_ref": self.checkpoint.ref,
            "semantic_completeness_claim": False,
            "global_negative_claim": False,
            "ranking_is_empirical_fact": False,
            "promotion_requires_exact_validation": True,
            "actor_v3_effect": False,
        })

    @property
    def replay_ref(self) -> ExactRef:
        return _derived_ref("PRE553_ADAPTIVE_SEARCH_REPLAY", "run-replay", {
            "contract": ADAPTIVE_DISCOVERY_CONTRACT_ID,
            "result_ref": self.result_ref,
            "start_checkpoint_ref": self.start_checkpoint_ref,
            "run_budget": self.run_budget,
            "visited_this_run": self.visited_this_run,
            "completion_state": self.completeness_state,
        })


@dataclass(frozen=True)
class _AdaptiveAuthorityContract:
    definition: Mapping[str, Any]
    policy: Mapping[str, Any]
    policy_ref: ExactRef
    replay_protocol_ref: ExactRef
    allowed_proposal_rule_refs: tuple[ExactRef, ...]
    maximum_generation: int
    maximum_frontier_size: int


def _verify_adaptive_authority(authority: DiscoveryAuthority, registry: AuthorityRegistry) -> _AdaptiveAuthorityContract:
    if not isinstance(registry, AuthorityRegistry):
        raise AdaptiveDiscoveryError("authority_registry must be exact immutable AuthorityRegistry")
    if not isinstance(authority, DiscoveryAuthority):
        raise AdaptiveDiscoveryError("expected DiscoveryAuthority@1.0.0")
    if semantic_hash(authority.semantic_projection()) != authority.content_hash:
        raise AdaptiveDiscoveryError("DiscoveryAuthority semantic identity mismatch")
    if authority.typed_state != "ADAPTIVE_EXPLORATORY_AUTHORIZED":
        raise AdaptiveDiscoveryError("adaptive service accepts ADAPTIVE_EXPLORATORY_AUTHORIZED only")
    if authority.semantic_fields.get("mode") != "ADAPTIVE_EXPLORATORY":
        raise AdaptiveDiscoveryError("adaptive authority must explicitly declare ADAPTIVE_EXPLORATORY mode")
    if authority.coverage_claim != ADAPTIVE_COVERAGE_CLAIM:
        raise PartialSearchNegativeError("adaptive authority must disclose nonexhaustive frontier coverage")
    validate_object_authority_closure(authority, registry)

    definition = _mapping(authority.candidate_universe_definition, "candidate_universe_definition")
    if definition.get("schema") != ADAPTIVE_SEARCH_SCHEMA:
        raise AdaptiveDiscoveryError("adaptive candidate-universe schema mismatch")
    grammar_ref = exact_ref(authority.candidate_grammar_ref, "candidate_grammar_ref")
    if grammar_ref.content_hash != semantic_hash(definition):
        raise AdaptiveDiscoveryError("candidate_grammar_ref must hash the frozen adaptive search universe")

    policy = _mapping(authority.semantic_fields.get("adaptive_search_policy"), "adaptive_search_policy")
    if policy.get("schema") != ADAPTIVE_SEARCH_POLICY_SCHEMA:
        raise AdaptiveDiscoveryError("adaptive search policy schema mismatch")
    if policy.get("ranking_rule") != RANKING_RULE:
        raise AdaptiveDiscoveryError("unsupported adaptive ranking rule")
    if policy.get("result_driven_changes_only_between_sealed_units") is not True:
        raise AdaptiveDiscoveryError("adaptive policy must forbid within-unit frontier mutation")
    if policy.get("partial_search_negative_forbidden") is not True:
        raise PartialSearchNegativeError("adaptive policy must forbid partial-search negative inference")
    if policy.get("promotion_requires_exact_validation") is not True:
        raise AdaptiveDiscoveryError("adaptive policy cannot promote learned facts directly")
    policy_ref = _derived_ref("PRE553_ADAPTIVE_SEARCH_POLICY", "policy", policy)

    if authority.algorithm_identity_if_semantically_required != ADAPTIVE_DISCOVERY_CONTRACT_ID:
        raise AdaptiveSearchIdentityError("adaptive authority does not pin this algorithm identity")
    if authority.tie_order_rules != TIE_ORDER_RULE:
        raise AdaptiveSearchIdentityError("adaptive authority tie-order rule mismatch")
    pruning = _mapping(authority.pruning_contract, "pruning_contract")
    if pruning.get("kind") != PRUNING_KIND:
        raise AdaptiveDiscoveryError("adaptive authority pruning/search contract mismatch")
    if pruning.get("unvisited_state") != "UNKNOWN_UNVISITED":
        raise PartialSearchNegativeError("unvisited adaptive territory must remain UNKNOWN_UNVISITED")
    rng = authority.rng_policy_if_any
    if rng not in (None, "NONE", {"kind": "NONE"}):
        raise AdaptiveSearchIdentityError("minimum adaptive service is deterministic and does not authorize RNG")

    operation = _text(definition.get("discovery_operation"), "discovery_operation")
    replay_operation = _text(definition.get("replay_operation"), "replay_operation")
    positive_frontier = False
    positive_replay = False
    for ref in authority.authority_snapshot_refs:
        snapshot = registry.resolve_exact(ref).snapshot
        if snapshot.authority_kind == "DISCOVERY_FRONTIER":
            registry.require(ref, authority_kind="DISCOVERY_FRONTIER", operation=operation, object_family="DiscoveryAuthority@1.0.0")
            positive_frontier = True
        if snapshot.authority_kind == "REPLAY_PROTOCOL":
            registry.require(ref, authority_kind="REPLAY_PROTOCOL", operation=replay_operation, object_family="DiscoveryAuthority@1.0.0")
            positive_replay = True
    if not positive_frontier:
        raise Pre553AuthorityError("adaptive search requires exact DISCOVERY_FRONTIER authority")
    if not positive_replay:
        raise Pre553AuthorityError("adaptive search requires exact REPLAY_PROTOCOL authority")

    allowed = _canonical_refs(
        exact_ref(ref, "allowed_proposal_rule_ref")
        for ref in _sequence(definition.get("allowed_proposal_rule_refs", ()), "allowed_proposal_rule_refs")
    )
    maximum_generation = definition.get("maximum_generation")
    maximum_frontier_size = definition.get("maximum_frontier_size")
    for value, name in ((maximum_generation, "maximum_generation"), (maximum_frontier_size, "maximum_frontier_size")):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise AdaptiveDiscoveryError(f"{name} must be a nonnegative exact integer")
    if maximum_frontier_size < 1:
        raise AdaptiveDiscoveryError("maximum_frontier_size must be positive")

    replay_protocol_ref = _derived_ref("PRE553_ADAPTIVE_REPLAY_PROTOCOL", "replay-protocol", {
        "contract": ADAPTIVE_DISCOVERY_CONTRACT_ID,
        "policy_ref": policy_ref,
        "tie_order": TIE_ORDER_RULE,
        "partial_negative": "FORBIDDEN",
        "checkpoint_serialization": "CANONICAL_JSON_SEMANTIC_MATERIAL",
    })
    return _AdaptiveAuthorityContract(
        definition=canonicalize(definition),
        policy=canonicalize(policy),
        policy_ref=policy_ref,
        replay_protocol_ref=replay_protocol_ref,
        allowed_proposal_rule_refs=allowed,
        maximum_generation=maximum_generation,
        maximum_frontier_size=maximum_frontier_size,
    )


def _unit_key(unit: AdaptiveExplorationUnit) -> tuple[int, str]:
    return (-unit.heuristic_rank, unit.unit_ref.key)


def _validate_unit(
    unit: AdaptiveExplorationUnit,
    *,
    contract: _AdaptiveAuthorityContract,
    determinant_state_ref: ExactRef,
    expected_parent: AdaptiveExplorationUnit | None,
    sealed_parent_result_ref: ExactRef | None,
) -> None:
    if unit.proposal_rule_ref not in contract.allowed_proposal_rule_refs:
        raise Pre553AuthorityError("exploration unit proposal rule exceeds adaptive authority")
    if determinant_state_ref not in unit.determinant_refs:
        raise AdaptiveSearchIdentityError("exploration unit omits frozen determinant state ref")
    if unit.generation > contract.maximum_generation:
        raise Pre553AuthorityError("exploration unit exceeds governed maximum generation")
    if expected_parent is None:
        if unit.generation != 0 or unit.parent_unit_ref is not None:
            raise AdaptiveDiscoveryError("initial adaptive units must be generation-0 roots")
    else:
        if unit.parent_unit_ref != expected_parent.unit_ref:
            raise AdaptiveDiscoveryError("result-driven proposal has wrong exact parent unit")
        if unit.generation != expected_parent.generation + 1:
            raise AdaptiveDiscoveryError("result-driven proposal generation is not parent+1")
        if sealed_parent_result_ref is None or sealed_parent_result_ref not in unit.determinant_refs:
            raise AdaptiveSearchIdentityError("result-driven proposal must bind exact sealed parent result")


def _merge_unit(known: dict[str, AdaptiveExplorationUnit], unit: AdaptiveExplorationUnit) -> None:
    existing = known.get(unit.unit_ref.key)
    if existing is not None and canonical_json(existing.as_dict()) != canonical_json(unit.as_dict()):
        raise AdaptiveSearchIdentityError("same unit ref was proposed with conflicting scheduling material")
    known[unit.unit_ref.key] = unit


def execute_adaptive_exploration(
    *,
    discovery_authority: DiscoveryAuthority,
    authority_registry: AuthorityRegistry,
    determinant_state_ref: ExactRef,
    initial_units: Iterable[AdaptiveExplorationUnit],
    evaluate_unit: Callable[[AdaptiveExplorationUnit, tuple[AdaptiveVisit, ...]], AdaptiveUnitOutcome],
    budget: int,
    resume_from: AdaptiveSearchCheckpoint | None = None,
    interrupt_after: int | None = None,
) -> AdaptiveSearchResult:
    """Run/restart bounded adaptive exploration over complete sealed units."""
    contract = _verify_adaptive_authority(discovery_authority, authority_registry)
    determinant = exact_ref(determinant_state_ref, "determinant_state_ref")
    if not isinstance(budget, int) or isinstance(budget, bool) or budget < 0:
        raise AdaptiveDiscoveryError("budget must be a nonnegative exact integer")
    if interrupt_after is not None:
        if not isinstance(interrupt_after, int) or isinstance(interrupt_after, bool) or interrupt_after < 1:
            raise AdaptiveDiscoveryError("interrupt_after must be a positive exact integer")
        if interrupt_after > budget:
            raise AdaptiveDiscoveryError("interrupt_after cannot exceed run budget")
    if not callable(evaluate_unit):
        raise AdaptiveDiscoveryError("evaluate_unit must be callable")

    roots = tuple(sorted(initial_units, key=lambda unit: unit.unit_ref.key))
    if not roots:
        raise AdaptiveDiscoveryError("adaptive exploration requires one or more initial root units")
    if len({unit.unit_ref.key for unit in roots}) != len(roots):
        raise AdaptiveDiscoveryError("duplicate initial root unit refs")
    for root in roots:
        _validate_unit(root, contract=contract, determinant_state_ref=determinant, expected_parent=None, sealed_parent_result_ref=None)
    root_refs = tuple(unit.unit_ref for unit in roots)

    if resume_from is None:
        known = {unit.unit_ref.key: unit for unit in roots}
        visits: list[AdaptiveVisit] = []
        start_checkpoint_ref = None
    else:
        if not isinstance(resume_from, AdaptiveSearchCheckpoint):
            raise AdaptiveDiscoveryError("resume_from must be AdaptiveSearchCheckpoint")
        if resume_from.discovery_authority_ref != discovery_authority.ref:
            raise AdaptiveSearchIdentityError("resume authority changed")
        if resume_from.search_policy_ref != contract.policy_ref:
            raise AdaptiveSearchIdentityError("resume search policy/version changed")
        if resume_from.determinant_state_ref != determinant:
            raise AdaptiveSearchIdentityError("resume determinant state changed")
        if resume_from.root_unit_refs != _canonical_refs(root_refs):
            raise AdaptiveSearchIdentityError("resume root-unit universe changed")
        known = {unit.unit_ref.key: unit for unit in resume_from.known_units}
        for root in roots:
            existing = known.get(root.unit_ref.key)
            if existing is None or canonical_json(existing.as_dict()) != canonical_json(root.as_dict()):
                raise AdaptiveSearchIdentityError("resume root-unit scheduling material changed")
        visits = list(resume_from.visits)
        start_checkpoint_ref = resume_from.ref

    if len(known) > contract.maximum_frontier_size:
        raise Pre553AuthorityError("adaptive checkpoint already exceeds maximum frontier size")

    visited_keys = {visit.unit.unit_ref.key for visit in visits}
    visited_this_run: list[ExactRef] = []
    interrupted = False
    for _ in range(budget):
        available = sorted((unit for key, unit in known.items() if key not in visited_keys), key=_unit_key)
        if not available:
            break
        unit = available[0]
        outcome = evaluate_unit(unit, tuple(visits))
        if not isinstance(outcome, AdaptiveUnitOutcome):
            raise AdaptiveDiscoveryError("evaluate_unit must return AdaptiveUnitOutcome")
        if outcome.unit_ref != unit.unit_ref:
            raise AdaptiveDiscoveryError("evaluate_unit returned outcome for another unit")
        for proposal in outcome.proposal_units:
            _validate_unit(
                proposal,
                contract=contract,
                determinant_state_ref=determinant,
                expected_parent=unit,
                sealed_parent_result_ref=outcome.sealed_result_ref,
            )
            _merge_unit(known, proposal)
            if len(known) > contract.maximum_frontier_size:
                raise Pre553AuthorityError("result-driven proposals exceed governed maximum frontier size")
        visit = AdaptiveVisit(len(visits), unit, outcome)
        visits.append(visit)
        visited_keys.add(unit.unit_ref.key)
        visited_this_run.append(unit.unit_ref)
        remaining = any(key not in visited_keys for key in known)
        if interrupt_after is not None and len(visited_this_run) >= interrupt_after and remaining:
            interrupted = True
            break

    remaining_units = tuple(sorted((unit for key, unit in known.items() if key not in visited_keys), key=_unit_key))
    if remaining_units:
        if interrupted:
            completeness_state = "PARTIAL_INTERRUPTED"
            stop_reason = "INTERRUPTED_AFTER_COMPLETE_SEALED_UNIT"
        else:
            completeness_state = "PARTIAL_BUDGET_EXHAUSTED"
            stop_reason = "RUN_BUDGET_EXHAUSTED_WITH_EXPLICIT_UNVISITED_FRONTIER"
    else:
        completeness_state = "EXPLORATORY_POLICY_FRONTIER_EXHAUSTED"
        stop_reason = "ALL_UNITS_REACHABLE_UNDER_FROZEN_EXPLORATORY_POLICY_VISITED"

    checkpoint = AdaptiveSearchCheckpoint(
        discovery_authority_ref=discovery_authority.ref,
        search_policy_ref=contract.policy_ref,
        determinant_state_ref=determinant,
        root_unit_refs=root_refs,
        known_units=tuple(known.values()),
        visits=tuple(visits),
        completeness_state=completeness_state,
        stop_reason=stop_reason,
        global_negative_claim=False,
    )
    return AdaptiveSearchResult(
        discovery_authority_ref=discovery_authority.ref,
        search_policy_ref=contract.policy_ref,
        determinant_state_ref=determinant,
        checkpoint=checkpoint,
        start_checkpoint_ref=start_checkpoint_ref,
        run_budget=budget,
        visited_this_run=tuple(visited_this_run),
        global_negative_claim=False,
        semantic_truth_effect=False,
        actor_v3_effect=False,
    )


def verify_adaptive_replay(
    expected: AdaptiveSearchResult,
    *,
    discovery_authority: DiscoveryAuthority,
    authority_registry: AuthorityRegistry,
    determinant_state_ref: ExactRef,
    initial_units: Iterable[AdaptiveExplorationUnit],
    evaluate_unit: Callable[[AdaptiveExplorationUnit, tuple[AdaptiveVisit, ...]], AdaptiveUnitOutcome],
    budget: int,
    resume_from: AdaptiveSearchCheckpoint | None = None,
    interrupt_after: int | None = None,
) -> ReplayReceipt:
    """Re-execute one adaptive run and return a typed deterministic replay receipt."""
    if not isinstance(expected, AdaptiveSearchResult):
        raise AdaptiveDiscoveryError("expected must be AdaptiveSearchResult")
    root_units = tuple(initial_units)
    actual = execute_adaptive_exploration(
        discovery_authority=discovery_authority,
        authority_registry=authority_registry,
        determinant_state_ref=determinant_state_ref,
        initial_units=root_units,
        evaluate_unit=evaluate_unit,
        budget=budget,
        resume_from=resume_from,
        interrupt_after=interrupt_after,
    )
    same = (
        expected.result_ref == actual.result_ref
        and expected.checkpoint.ref == actual.checkpoint.ref
        and expected.replay_ref == actual.replay_ref
        and expected.visited_this_run == actual.visited_this_run
    )
    replay_state = "REPLAY_VERIFIED" if same else "NONDETERMINISTIC_REPLAY"
    contract = _verify_adaptive_authority(discovery_authority, authority_registry)
    roots = _canonical_refs(unit.unit_ref for unit in root_units)
    inputs = [discovery_authority.ref, exact_ref(determinant_state_ref, "determinant_state_ref"), contract.policy_ref, *roots]
    if resume_from is not None:
        inputs.append(resume_from.ref)
    return ReplayReceipt(
        typed_state=replay_state,
        authority_snapshot_refs=discovery_authority.authority_snapshot_refs,
        dependency_refs=_canonical_refs([expected.result_ref, actual.result_ref, discovery_authority.ref, contract.policy_ref]),
        producer_replay_locator_or_reference_root=actual.replay_ref,
        replayed_object_ref=expected.result_ref,
        input_content_identity_refs=_canonical_refs(inputs),
        authority_snapshot_refs_replayed=discovery_authority.authority_snapshot_refs,
        producer_or_algorithm_identity=ADAPTIVE_DISCOVERY_CONTRACT_ID,
        canonical_semantic_projection_hash=actual.result_ref.content_hash,
        deterministic_order_or_tie_rule_refs=(contract.policy_ref,),
        replay_protocol_ref=contract.replay_protocol_ref,
        replay_state=replay_state,
        exact_i05_mutation=False,
        semantic_truth_effect=False,
        actor_v3_effect=False,
    )


__all__ = [
    "ADAPTIVE_DISCOVERY_CONTRACT_ID",
    "ADAPTIVE_SEARCH_SCHEMA",
    "ADAPTIVE_SEARCH_POLICY_SCHEMA",
    "ADAPTIVE_COVERAGE_CLAIM",
    "ADAPTIVE_SEARCH_COMPLETENESS_CONTRACT",
    "SEARCH_COMPLETENESS_STATES",
    "AdaptiveDiscoveryError",
    "AdaptiveSearchIdentityError",
    "PartialSearchNegativeError",
    "AdaptiveExplorationUnit",
    "AdaptiveUnitOutcome",
    "AdaptiveVisit",
    "AdaptiveSearchCheckpoint",
    "AdaptiveSearchResult",
    "execute_adaptive_exploration",
    "verify_adaptive_replay",
]
