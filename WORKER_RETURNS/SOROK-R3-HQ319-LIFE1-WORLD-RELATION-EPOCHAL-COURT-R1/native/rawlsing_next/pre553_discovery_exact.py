"""PRE553 I05 exact-bounded autonomous empirical discovery.

This module consumes only accepted PRE553 I01-I03 public objects and exact
query execution.  Discovery authority fixes a finite/finitely-constructible
frontier before data are examined; every compiled candidate is evaluated.
No adaptive traversal, structural admission, V553, actor/V3 semantics, legacy
profile machinery, or diagnostic-to-fact promotion exists here.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    DiscoveryAuthority,
    DiscoveryResultReceipt,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    Pre553SemanticCollapseError,
    canonical_json,
    canonicalize,
    exact_ref,
    make_empirical_predicate,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next._pre553_query_common import QUERY_EXECUTION_CONTRACT_ID, QueryExecutionResult

I05_CONTRACT_ID = "PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0"
CANDIDATE_GRAMMAR_SCHEMA = "PRE553_I05_EXACT_BOUNDED_CANDIDATE_GRAMMAR@1.0.0"
COVERAGE_CLAIM = "COMPLETE_FOR_EXACT_DECLARED_FRONTIER"

CANDIDATE_FAMILIES = frozenset({
    "UNARY_SOCIAL_FORK",
    "RESPONSE_X_EMPIRICAL_COORDINATE",
    "BOUNDED_COORDINATE_CONJUNCTION",
    "RESPONSE_X_COORDINATE_CONJUNCTION",
    "PAIR_RESPONSE_COTRAVEL",
    "BOUNDED_K_WAY_RESPONSE_CONFIGURATION",
    "CONDITIONAL_REVERSAL_OR_SIMPSON",
    "MINORITY_OR_NONMODAL_DEPARTURE",
    "RECURSIVE_SUBGROUP_FORK",
    "BRANCH_CONDITIONED_DISTRIBUTION",
    "BRANCH_CONDITIONED_COTRAVEL",
})
PREDICATE_FORMS = frozenset({
    "SINGLE_ATOM",
    "AND_COMBINATIONS",
    "AND_CARTESIAN_GROUPS",
    "XOR_EXACTLY_ONE_COMBINATIONS",
    "BASE_QUERY",
    "JOINT_DEPENDENCE",
    "REVERSAL_GRID",
})
VALIDATION_KINDS = frozenset({
    "DISTRIBUTION_DIFFERS_FROM_BASELINE",
    "JOINT_NOT_PRODUCT_OF_MARGINALS",
    "CONDITIONAL_REVERSAL",
    "TARGET_CELL_SUPPORTED",
})
DIAGNOSTIC_TOKENS = frozenset({
    "MI", "NMI", "CRAMERS_V", "CRAMER'S_V", "LIFT", "ENTROPY",
    "ENTROPY_REDUCTION", "TREE_SCORE", "CLOUD_SCORE", "ASSOCIATION_STRENGTH",
})
TERMINAL_COVERAGE_STATES = frozenset({
    "EVALUATED_SUPPORTED",
    "EVALUATED_VALID_EMPTY",
    "EVALUATED_UNDERPOWERED",
    "EVALUATED_NONCOMPARABLE",
    "EVALUATED_DENIED_BY_EXACT_AUTHORITY",
    "EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY",
})


class ExactBoundedDiscoveryError(Pre553IntegrityError):
    """Exact I05 frontier, authority, or evaluation contract is invalid."""


class ExactBoundedCoverageError(ExactBoundedDiscoveryError):
    """A complete-for-frontier claim cannot truthfully close."""


@dataclass(frozen=True)
class _Atom:
    atom_id: str
    kind: str
    predicate: EmpiricalPredicate
    ancestry_refs: tuple[ExactRef, ...]


@dataclass(frozen=True)
class _Template:
    template_id: str
    query: EmpiricalQuerySpec


@dataclass(frozen=True)
class _QueryRole:
    role: str
    predicate: EmpiricalPredicate
    query: EmpiricalQuerySpec


@dataclass(frozen=True)
class _Candidate:
    family: str
    rule_id: str
    candidate_id: str
    candidate_hash: str
    winning_predicate: EmpiricalPredicate
    query_roles: tuple[_QueryRole, ...]
    validation: Mapping[str, Any]
    ancestry_refs: tuple[ExactRef, ...]


@dataclass(frozen=True)
class ExactBoundedDiscoveryResult:
    contract_id: str
    discovery_authority_ref: ExactRef
    candidate_grammar_ref: ExactRef
    evaluated_frontier_ref: ExactRef
    coverage_claim: str
    candidate_count: int
    covered_candidate_count: int
    receipts: tuple[DiscoveryResultReceipt, ...]
    empirical_fact_refs: tuple[ExactRef, ...]
    empirical_facts: tuple[EmpiricalFact, ...]
    executed_predicates: tuple[EmpiricalPredicate, ...]
    executed_queries: tuple[EmpiricalQuerySpec, ...]
    valid_empty: bool
    replay_ref: ExactRef

    def __post_init__(self) -> None:
        if self.contract_id != I05_CONTRACT_ID:
            raise ExactBoundedDiscoveryError("unexpected I05 contract id")
        if self.coverage_claim != COVERAGE_CLAIM:
            raise ExactBoundedCoverageError("I05 may only return exact declared-frontier coverage")
        if self.candidate_count != self.covered_candidate_count:
            raise ExactBoundedCoverageError("complete frontier requires every candidate covered")
        if tuple(sorted(self.receipts, key=lambda r: r.ref.key)) != self.receipts:
            raise ExactBoundedDiscoveryError("receipts must be exact-ref sorted")
        if tuple(sorted(set(self.empirical_fact_refs), key=lambda r: r.key)) != self.empirical_fact_refs:
            raise ExactBoundedDiscoveryError("empirical_fact_refs must be canonical")
        if tuple(sorted({f.ref.key: f for f in self.empirical_facts}.values(), key=lambda f: f.ref.key)) != self.empirical_facts:
            raise ExactBoundedDiscoveryError("empirical_facts must be exact-ref canonical")
        if tuple(f.ref for f in self.empirical_facts) != self.empirical_fact_refs:
            raise ExactBoundedDiscoveryError("empirical fact preimages do not close over exact refs")
        for objects, cls, label in (
            (self.executed_predicates, EmpiricalPredicate, "executed_predicates"),
            (self.executed_queries, EmpiricalQuerySpec, "executed_queries"),
        ):
            if tuple(sorted(objects, key=lambda obj: obj.ref.key)) != objects:
                raise ExactBoundedDiscoveryError(f"{label} must be exact-ref sorted")
            if len({obj.ref.key for obj in objects}) != len(objects):
                raise ExactBoundedDiscoveryError(f"{label} must be exact-ref unique")
            for obj in objects:
                _verify_object_identity(obj, cls, f"{label} item")

        predicate_by_key = {obj.ref.key: obj for obj in self.executed_predicates}
        query_by_key = {obj.ref.key: obj for obj in self.executed_queries}
        for receipt in self.receipts:
            identity = receipt.candidate_identity
            roles = identity.get("query_roles") if isinstance(identity, Mapping) else None
            if not isinstance(roles, Sequence) or isinstance(roles, (str, bytes)):
                raise ExactBoundedDiscoveryError("receipt query roles are malformed")
            for role in roles:
                if not isinstance(role, Mapping):
                    raise ExactBoundedDiscoveryError("receipt query role is malformed")
                predicate_ref = exact_ref(role.get("predicate_ref"), "role predicate_ref")
                query_ref = exact_ref(role.get("query_ref"), "role query_ref")
                predicate = predicate_by_key.get(predicate_ref.key)
                query = query_by_key.get(query_ref.key)
                if predicate is None or query is None:
                    raise ExactBoundedDiscoveryError(
                        "executed role object closure omits exact predicate/query preimage"
                    )
                if exact_ref(query.condition_predicate_ref, "role query condition") != predicate_ref:
                    raise ExactBoundedDiscoveryError(
                        "executed role query does not bind its exact predicate"
                    )


CANDIDATE_GRAMMAR_CONTRACT: Mapping[str, Any] = {
    "schema": CANDIDATE_GRAMMAR_SCHEMA,
    "authority_precedes_search": True,
    "atom_binding": "exact EmpiricalPredicate refs only",
    "query_template_binding": "exact EmpiricalQuerySpec refs only",
    "forms": tuple(sorted(PREDICATE_FORMS)),
    "validations": tuple(sorted(VALIDATION_KINDS)),
    "complete_frontier_rule": "every compiled candidate is executed; no score/top-k/unary screen/adaptive stop",
    "diagnostic_nonauthority": "diagnostics may be declared for reporting/ranking only and never prune or become EmpiricalFact",
}


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ExactBoundedDiscoveryError(f"{name} must be an exact mapping")
    return value


def _sequence(value: Any, name: str, *, allow_empty: bool = False) -> Sequence[Any]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise ExactBoundedDiscoveryError(f"{name} must be a sequence")
    if not allow_empty and not value:
        raise ExactBoundedDiscoveryError(f"{name} may not be empty")
    return value


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExactBoundedDiscoveryError(f"{name} must be a non-empty string")
    return value.strip()


def _allowed_validation_kinds(validation_rules: Any) -> set[str]:
    """Read only exact declared validation kinds, including rules-only owners."""
    envelope = _mapping(validation_rules, "validation_rules")
    declared: set[str] | None = None
    if "kinds" in envelope:
        declared = {
            _text(value, "validation_rules.kinds member")
            for value in _sequence(
                envelope["kinds"], "validation_rules.kinds", allow_empty=True
            )
        }
        if not declared <= VALIDATION_KINDS:
            raise Pre553AuthorityError(
                "discovery validation authority declares an unknown validation kind"
            )

    ruled: set[str] | None = None
    if "rules" in envelope:
        ruled = set()
        for raw in _sequence(
            envelope["rules"], "validation_rules.rules", allow_empty=True
        ):
            rule = _mapping(raw, "validation_rules rule")
            kind = _text(rule.get("kind"), "validation_rules rule kind")
            if kind not in VALIDATION_KINDS:
                raise Pre553AuthorityError(
                    "discovery validation authority rule has an unknown kind"
                )
            ruled.add(kind)

    if declared is None and ruled is None:
        return set()
    if declared is None:
        return ruled or set()
    if ruled is not None and not ruled <= declared:
        raise Pre553AuthorityError(
            "discovery validation authority kinds contradict its explicit rules"
        )
    return declared


def _derived_ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:pre553:i05:{namespace}:sha256:{digest}", digest)


def _canonical_refs(values: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    return tuple(sorted(set(values), key=lambda r: r.key))


def _canonical_auths(values: Iterable[AuthorityRef]) -> tuple[AuthorityRef, ...]:
    return tuple(sorted(set(values), key=lambda r: r.key))


def _verify_object_identity(obj: Any, expected_type: type, label: str) -> None:
    if not isinstance(obj, expected_type):
        raise ExactBoundedDiscoveryError(f"{label} has wrong exact public object type")
    if semantic_hash(obj.semantic_projection()) != obj.content_hash:
        raise ExactBoundedDiscoveryError(f"{label} semantic projection/content hash mismatch")
    if obj.ref.object_id != obj.object_id or obj.ref.content_hash != obj.content_hash:
        raise ExactBoundedDiscoveryError(f"{label} ExactRef identity mismatch")


def _verify_discovery_authority(
    authority: DiscoveryAuthority,
    registry: AuthorityRegistry,
) -> Mapping[str, Any]:
    _verify_object_identity(authority, DiscoveryAuthority, "discovery_authority")
    if authority.typed_state != "EXACT_BOUNDED_AUTHORIZED":
        raise ExactBoundedDiscoveryError("I05 accepts EXACT_BOUNDED authority only")
    if authority.coverage_claim != COVERAGE_CLAIM:
        raise ExactBoundedCoverageError("authority does not claim complete exact frontier")
    if authority.semantic_fields.get("mode", "EXACT_BOUNDED") != "EXACT_BOUNDED":
        raise ExactBoundedDiscoveryError("adaptive/exploratory authority is forbidden in I05")
    validate_object_authority_closure(authority, registry)

    definition = _mapping(authority.candidate_universe_definition, "candidate_universe_definition")
    if definition.get("schema") != CANDIDATE_GRAMMAR_SCHEMA:
        raise ExactBoundedDiscoveryError("candidate grammar schema mismatch")
    grammar_ref = exact_ref(authority.candidate_grammar_ref, "candidate_grammar_ref")
    if grammar_ref.content_hash != semantic_hash(definition):
        raise ExactBoundedDiscoveryError("candidate grammar ref does not hash exact pre-search grammar")

    operation = _text(definition.get("discovery_operation"), "discovery_operation")
    positive_frontier = False
    for ref in authority.authority_snapshot_refs:
        snapshot = registry.resolve_exact(ref).snapshot
        if snapshot.authority_kind == "DISCOVERY_FRONTIER":
            registry.require(
                ref,
                authority_kind="DISCOVERY_FRONTIER",
                operation=operation,
                object_family="DiscoveryAuthority@1.0.0",
            )
            registry.require(
                ref,
                authority_kind="DISCOVERY_FRONTIER",
                operation=operation,
                object_family="DiscoveryResultReceipt@1.0.0",
            )
            positive_frontier = True
    if not positive_frontier:
        raise Pre553AuthorityError("exact DISCOVERY_FRONTIER authority is required")

    pruning = _mapping(authority.pruning_contract, "pruning_contract")
    if pruning.get("kind") != "NONE_EXACT_EVALUATE_ALL":
        raise ExactBoundedCoverageError(
            "I05 implements no heuristic/safe-theorem pruning; exact authority must require evaluate-all"
        )
    rng = authority.rng_policy_if_any
    if rng not in (None, "NONE", {"kind": "NONE"}):
        raise ExactBoundedDiscoveryError("I05 exact frontier does not authorize proposal randomness")
    ranking = authority.semantic_fields.get("candidate_scoring_or_ranking_rule_if_any")
    if isinstance(ranking, Mapping) and ranking.get("controls_frontier") is True:
        raise ExactBoundedCoverageError("diagnostic ranking may not control exact frontier reachability")
    if authority.algorithm_identity_if_semantically_required != I05_CONTRACT_ID:
        raise ExactBoundedDiscoveryError("discovery authority algorithm identity does not pin this I05 implementation")
    if authority.tie_order_rules != "CANONICAL_CANDIDATE_HASH_ORDER":
        raise ExactBoundedDiscoveryError("I05 requires exact canonical candidate-hash evaluation order")
    return definition


def _catalog_atoms(
    definition: Mapping[str, Any],
    predicates: Iterable[EmpiricalPredicate],
) -> dict[str, _Atom]:
    by_ref: dict[str, EmpiricalPredicate] = {}
    for predicate in predicates:
        _verify_object_identity(predicate, EmpiricalPredicate, "predicate_catalog item")
        if predicate.ref.key in by_ref:
            raise ExactBoundedDiscoveryError("duplicate predicate exact ref in catalog")
        by_ref[predicate.ref.key] = predicate
    result: dict[str, _Atom] = {}
    for raw in _sequence(definition.get("atoms", ()), "candidate grammar atoms", allow_empty=True):
        item = _mapping(raw, "atom")
        atom_id = _text(item.get("atom_id"), "atom_id")
        if atom_id in result:
            raise ExactBoundedDiscoveryError("duplicate atom_id")
        ref = exact_ref(item.get("predicate_ref"), f"atom {atom_id}.predicate_ref")
        predicate = by_ref.get(ref.key)
        if predicate is None:
            raise ExactBoundedDiscoveryError(f"atom {atom_id} exact predicate unavailable")
        kind = _text(item.get("kind"), f"atom {atom_id}.kind")
        ancestry = _canonical_refs(
            exact_ref(value, f"atom {atom_id}.ancestry_refs")
            for value in _sequence(item.get("ancestry_refs", ()), "ancestry_refs", allow_empty=True)
        )
        result[atom_id] = _Atom(atom_id, kind, predicate, ancestry)
    return result


def _validate_catalog_scope(
    authority: DiscoveryAuthority,
    atoms: Mapping[str, _Atom],
    templates: Mapping[str, _Template],
) -> None:
    source_scope = _mapping(authority.source_universe_scope, "source_universe_scope")
    risk_scope = _mapping(authority.risk_set_scope, "risk_set_scope")
    measure_scope = _mapping(authority.measure_scope, "measure_scope")
    topology_scope = _mapping(authority.topology_scope, "topology_scope")
    allowed_universes = {
        exact_ref(value, "allowed_universe_ref").key
        for value in _sequence(source_scope.get("allowed_universe_refs"), "allowed_universe_refs")
    }
    allowed_risks = {
        exact_ref(value, "allowed_risk_set_ref").key
        for value in _sequence(risk_scope.get("allowed_risk_set_refs"), "allowed_risk_set_refs")
    }
    allowed_measures = {
        _text(value, "allowed_measure_kind")
        for value in _sequence(measure_scope.get("allowed_measure_kinds"), "allowed_measure_kinds")
    }
    max_j = topology_scope.get("maximum_target_arity_J")
    if not isinstance(max_j, int) or isinstance(max_j, bool) or max_j < 1:
        raise ExactBoundedDiscoveryError("topology_scope.maximum_target_arity_J must be positive integer")
    for atom in atoms.values():
        for ref_value in atom.predicate.scope_refs:
            ref = exact_ref(ref_value, f"atom {atom.atom_id}.scope_ref")
            if ref.kind == "EmpiricalUniverse@1.0.0" and ref.key not in allowed_universes:
                raise Pre553AuthorityError("discovery atom scope exceeds exact source-universe authority")
        for ref_value in atom.predicate.risk_set_refs:
            ref = exact_ref(ref_value, f"atom {atom.atom_id}.risk_set_ref")
            if ref.key not in allowed_risks:
                raise Pre553AuthorityError("discovery atom risk set exceeds exact authority")
    for template in templates.values():
        query = template.query
        for ref_value in query.empirical_universe_refs:
            if exact_ref(ref_value, "query empirical_universe_ref").key not in allowed_universes:
                raise Pre553AuthorityError("query template source universe exceeds discovery authority")
        if exact_ref(query.risk_set_ref, "query risk_set_ref").key not in allowed_risks:
            raise Pre553AuthorityError("query template risk set exceeds discovery authority")
        grain = _mapping(query.requested_output_grain, "requested_output_grain")
        if grain.get("measure_kind") not in allowed_measures:
            raise Pre553AuthorityError("query template measure exceeds discovery authority")
        arity = _mapping(query.target_arity_and_topology, "target_arity_and_topology").get("arity")
        if not isinstance(arity, int) or isinstance(arity, bool) or arity < 1 or arity > max_j:
            raise Pre553AuthorityError("query template target arity exceeds discovery topology authority")


def _catalog_templates(
    definition: Mapping[str, Any],
    queries: Iterable[EmpiricalQuerySpec],
) -> dict[str, _Template]:
    by_ref: dict[str, EmpiricalQuerySpec] = {}
    for query in queries:
        _verify_object_identity(query, EmpiricalQuerySpec, "query_template_catalog item")
        if query.ref.key in by_ref:
            raise ExactBoundedDiscoveryError("duplicate query exact ref in catalog")
        by_ref[query.ref.key] = query
    result: dict[str, _Template] = {}
    for raw in _sequence(definition.get("query_templates", ()), "query_templates", allow_empty=True):
        item = _mapping(raw, "query template")
        template_id = _text(item.get("template_id"), "template_id")
        if template_id in result:
            raise ExactBoundedDiscoveryError("duplicate template_id")
        ref = exact_ref(item.get("query_ref"), f"template {template_id}.query_ref")
        query = by_ref.get(ref.key)
        if query is None:
            raise ExactBoundedDiscoveryError(f"query template {template_id} exact object unavailable")
        result[template_id] = _Template(template_id, query)
    return result


def _combine_predicates(
    predicates: Sequence[EmpiricalPredicate],
    *,
    op: str,
    tag_material: Any,
) -> EmpiricalPredicate:
    if not predicates:
        raise ExactBoundedDiscoveryError("cannot compose empty predicate set")
    grammar_refs = {canonical_json(p.grammar_authority_ref) for p in predicates}
    bindings = {p.same_respondent_binding_semantics for p in predicates}
    if len(grammar_refs) != 1 or len(bindings) != 1:
        try:
            from rawlsing_next.pre553_runtime_context import current_runtime_authorities
            runtime = current_runtime_authorities()
        except ImportError:
            runtime = None
        if runtime is None:
            raise ExactBoundedDiscoveryError(
                "composed predicates must share exact grammar and respondent binding law")
        from rawlsing_next.pre553_runtime_composition import compose_predicates_runtime
        return compose_predicates_runtime(
            predicates,
            op=op,
            tag_material=tag_material,
            runtime_authorities=runtime,
        )
    if op == "AND":
        ast = {"op": "AND", "children": [p.predicate_ast for p in predicates]}
    elif op == "OR":
        ast = {"op": "OR", "children": [p.predicate_ast for p in predicates]}
    else:
        raise ExactBoundedDiscoveryError("unsupported predicate composition op")
    return make_empirical_predicate(
        predicate_ast=ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=_canonical_auths(
            ref for p in predicates for ref in p.authority_snapshot_refs
        ),
        dependency_refs=_canonical_refs(p.ref for p in predicates),
        producer_replay_locator_or_reference_root=_derived_ref(
            "PRE553_I05_PREDICATE_REPLAY_ROOT", "predicate-replay", tag_material
        ),
        grammar_authority_ref=predicates[0].grammar_authority_ref,
        coordinate_question_value_refs=_canonical_refs(
            exact_ref(ref, "coordinate_question_value_ref")
            for p in predicates for ref in p.coordinate_question_value_refs
        ),
        risk_set_refs=_canonical_refs(
            exact_ref(ref, "risk_set_ref") for p in predicates for ref in p.risk_set_refs
        ),
        scope_refs=_canonical_refs(
            exact_ref(ref, "scope_ref") for p in predicates for ref in p.scope_refs
        ),
        same_respondent_binding_semantics=predicates[0].same_respondent_binding_semantics,
        operator_semantics_refs=_canonical_refs(
            exact_ref(ref, "operator_semantics_ref")
            for p in predicates for ref in p.operator_semantics_refs
        ),
    )


def _xor_exactly_one(predicates: Sequence[EmpiricalPredicate], *, tag_material: Any) -> EmpiricalPredicate:
    if len(predicates) < 2:
        raise ExactBoundedDiscoveryError("XOR_EXACTLY_ONE requires at least two atoms")
    ors = {"op": "OR", "children": [p.predicate_ast for p in predicates]}
    pair_ands = [
        {"op": "AND", "children": [a.predicate_ast, b.predicate_ast]}
        for a, b in combinations(predicates, 2)
    ]
    no_pair = {"op": "NOT", "children": [{"op": "OR", "children": pair_ands}]}
    common = _combine_predicates(predicates, op="OR", tag_material={"probe": tag_material})
    # Reuse exact metadata from the verified common predicate; replace only the AST.
    return make_empirical_predicate(
        predicate_ast={"op": "AND", "children": [ors, no_pair]},
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=common.authority_snapshot_refs,
        dependency_refs=_canonical_refs(p.ref for p in predicates),
        producer_replay_locator_or_reference_root=_derived_ref(
            "PRE553_I05_PREDICATE_REPLAY_ROOT", "xor-predicate-replay", tag_material
        ),
        grammar_authority_ref=common.grammar_authority_ref,
        coordinate_question_value_refs=common.coordinate_question_value_refs,
        risk_set_refs=common.risk_set_refs,
        scope_refs=common.scope_refs,
        same_respondent_binding_semantics=common.same_respondent_binding_semantics,
        operator_semantics_refs=common.operator_semantics_refs,
    )


def _clone_query(template: EmpiricalQuerySpec, predicate: EmpiricalPredicate, *, role_material: Any) -> EmpiricalQuerySpec:
    fields = dict(template.semantic_fields)
    old_condition = exact_ref(template.condition_predicate_ref, "template condition_predicate_ref")
    fields["condition_predicate_ref"] = predicate.ref
    deps = [ref for ref in template.dependency_refs if ref != old_condition]
    deps.append(predicate.ref)
    return EmpiricalQuerySpec(
        typed_state=template.typed_state,
        authority_snapshot_refs=template.authority_snapshot_refs,
        dependency_refs=_canonical_refs(deps),
        producer_replay_locator_or_reference_root=_derived_ref(
            "PRE553_I05_QUERY_REPLAY_ROOT", "query-replay", role_material
        ),
        **fields,
    )


def _candidate(
    *,
    family: str,
    rule_id: str,
    winning_predicate: EmpiricalPredicate,
    query_roles: Sequence[_QueryRole],
    validation: Mapping[str, Any],
    ancestry_refs: Iterable[ExactRef] = (),
) -> _Candidate:
    material = {
        "contract": I05_CONTRACT_ID,
        "family": family,
        "rule_id": rule_id,
        "winning_predicate_ref": winning_predicate.ref.as_dict(),
        "query_roles": [
            {"role": x.role, "predicate_ref": x.predicate.ref.as_dict(), "query_ref": x.query.ref.as_dict()}
            for x in query_roles
        ],
        "validation": canonicalize(validation),
        "ancestry_refs": [x.as_dict() for x in _canonical_refs(ancestry_refs)],
    }
    digest = semantic_hash(material)
    return _Candidate(
        family=family,
        rule_id=rule_id,
        candidate_id=f"urn:rawlsing:pre553:i05:candidate:sha256:{digest}",
        candidate_hash=digest,
        winning_predicate=winning_predicate,
        query_roles=tuple(query_roles),
        validation=canonicalize(validation),
        ancestry_refs=_canonical_refs(ancestry_refs),
    )


def _normal_candidate(
    rule: Mapping[str, Any],
    condition: EmpiricalPredicate,
    baseline: EmpiricalPredicate,
    template: _Template,
    *,
    ancestry_refs: Iterable[ExactRef],
) -> _Candidate:
    family = _text(rule.get("family"), "rule.family")
    rule_id = _text(rule.get("rule_id"), "rule.rule_id")
    validation = _mapping(rule.get("validation"), "rule.validation")
    if validation.get("kind") != "DISTRIBUTION_DIFFERS_FROM_BASELINE":
        raise ExactBoundedDiscoveryError("normal candidate requires exact distribution-difference validation")
    q_condition = _clone_query(template.query, condition, role_material={"rule": rule_id, "role": "CONDITION", "predicate": condition.ref.as_dict()})
    q_baseline = _clone_query(template.query, baseline, role_material={"rule": rule_id, "role": "BASELINE", "predicate": baseline.ref.as_dict()})
    return _candidate(
        family=family,
        rule_id=rule_id,
        winning_predicate=condition,
        query_roles=(
            _QueryRole("CONDITION", condition, q_condition),
            _QueryRole("BASELINE", baseline, q_baseline),
        ),
        validation=validation,
        ancestry_refs=ancestry_refs,
    )


def _compile_frontier(
    definition: Mapping[str, Any],
    atoms: Mapping[str, _Atom],
    templates: Mapping[str, _Template],
) -> tuple[_Candidate, ...]:
    candidates: list[_Candidate] = []
    seen_rules: set[str] = set()
    max_k = int(_mapping(definition.get("limits", {}), "limits").get("maximum_conditioner_arity_K", 0))
    max_j = int(_mapping(definition.get("limits", {}), "limits").get("maximum_target_arity_J", 0))
    if max_k < 0 or max_j < 1:
        raise ExactBoundedDiscoveryError("invalid exact K/J frontier limits")

    def atom(atom_id: str) -> _Atom:
        if atom_id not in atoms:
            raise ExactBoundedDiscoveryError(f"rule references undeclared atom {atom_id!r}")
        return atoms[atom_id]

    def template(template_id: str) -> _Template:
        if template_id not in templates:
            raise ExactBoundedDiscoveryError(f"rule references undeclared query template {template_id!r}")
        return templates[template_id]

    for raw in _sequence(definition.get("rules", ()), "candidate grammar rules", allow_empty=True):
        rule = _mapping(raw, "candidate rule")
        rule_id = _text(rule.get("rule_id"), "rule_id")
        if rule_id in seen_rules:
            raise ExactBoundedDiscoveryError("duplicate discovery rule_id")
        seen_rules.add(rule_id)
        family = _text(rule.get("family"), "family")
        form = _text(rule.get("form"), "form")
        if family not in CANDIDATE_FAMILIES or form not in PREDICATE_FORMS:
            raise ExactBoundedDiscoveryError("unknown candidate family/form")
        validation = _mapping(rule.get("validation"), "validation")
        kind = _text(validation.get("kind"), "validation.kind")
        if kind not in VALIDATION_KINDS:
            raise ExactBoundedDiscoveryError("validation rule is not an accepted I05 exact validator")
        if any(token in canonical_json(validation).upper() for token in DIAGNOSTIC_TOKENS):
            raise Pre553SemanticCollapseError("diagnostic score cannot become I05 validation fact or truth")

        if form in {"SINGLE_ATOM", "AND_COMBINATIONS", "AND_CARTESIAN_GROUPS", "XOR_EXACTLY_ONE_COMBINATIONS"}:
            baseline = atom(_text(rule.get("baseline_atom_id"), "baseline_atom_id"))
            tmpl = template(_text(rule.get("query_template_id"), "query_template_id"))
            target_arity = int(_mapping(tmpl.query.target_arity_and_topology, "target topology").get("arity", 0))
            if target_arity > max_j:
                raise ExactBoundedCoverageError("query target arity exceeds authority J frontier")
            groups: list[tuple[_Atom, ...]] = []
            if form == "SINGLE_ATOM":
                groups = [(atom(_text(x, "atom_id")),) for x in _sequence(rule.get("atom_ids"), "atom_ids")]
            elif form == "AND_COMBINATIONS":
                pool = [atom(_text(x, "atom_id")) for x in _sequence(rule.get("atom_ids"), "atom_ids")]
                arity = int(rule.get("arity", 0))
                if arity < 1 or arity > max_k:
                    raise ExactBoundedCoverageError("conditioner arity outside authority K frontier")
                groups = [tuple(x) for x in combinations(pool, arity)]
            elif form == "AND_CARTESIAN_GROUPS":
                raw_groups = _sequence(rule.get("atom_groups"), "atom_groups")
                if len(raw_groups) > max_k:
                    raise ExactBoundedCoverageError("cartesian conditioner arity outside authority K frontier")
                pools = [tuple(atom(_text(x, "atom_id")) for x in _sequence(g, "atom group")) for g in raw_groups]
                groups = [tuple(x) for x in product(*pools)]
            else:
                pool = [atom(_text(x, "atom_id")) for x in _sequence(rule.get("atom_ids"), "atom_ids")]
                arity = int(rule.get("arity", 0))
                if arity < 2 or arity > max_k:
                    raise ExactBoundedCoverageError("XOR conditioner arity outside authority K frontier")
                groups = [tuple(x) for x in combinations(pool, arity)]

            for selected in groups:
                if form == "SINGLE_ATOM":
                    condition = selected[0].predicate
                elif form == "XOR_EXACTLY_ONE_COMBINATIONS":
                    condition = _xor_exactly_one(
                        [x.predicate for x in selected],
                        tag_material={"rule": rule_id, "atoms": [x.atom_id for x in selected]},
                    )
                else:
                    condition = _combine_predicates(
                        [x.predicate for x in selected],
                        op="AND",
                        tag_material={"rule": rule_id, "atoms": [x.atom_id for x in selected]},
                    )
                if baseline.atom_id not in {x.atom_id for x in selected}:
                    # Branch/scope baselines constrain the generated condition exactly.
                    condition = _combine_predicates(
                        [baseline.predicate, condition],
                        op="AND",
                        tag_material={"rule": rule_id, "baseline": baseline.atom_id, "condition": condition.ref.as_dict()},
                    )
                candidates.append(_normal_candidate(
                    rule, condition, baseline.predicate, tmpl,
                    ancestry_refs=[ref for x in selected for ref in x.ancestry_refs] + list(baseline.ancestry_refs),
                ))

        elif form == "BASE_QUERY":
            if kind != "TARGET_CELL_SUPPORTED":
                raise ExactBoundedDiscoveryError("BASE_QUERY requires exact target-cell support validation")
            baseline = atom(_text(rule.get("baseline_atom_id"), "baseline_atom_id"))
            tmpl = template(_text(rule.get("query_template_id"), "query_template_id"))
            target_arity = int(_mapping(tmpl.query.target_arity_and_topology, "target topology").get("arity", 0))
            if target_arity < 1 or target_arity > max_j:
                raise ExactBoundedCoverageError("BASE_QUERY target arity exceeds authority J frontier")
            target_cells = _sequence(rule.get("target_cells"), "target_cells", allow_empty=True)
            target_spec = _mapping(tmpl.query.target_arity_and_topology, "target topology")
            components = _sequence(target_spec.get("components"), "target components")
            domains = [
                tuple(_sequence(_mapping(component, "target component").get("domain", ()), "target component domain", allow_empty=True))
                for component in components
            ]
            if all(domains):
                declared_cells = (
                    {canonical_json(cell) for cell in domains[0]}
                    if target_arity == 1
                    else {canonical_json(cell) for cell in product(*domains)}
                )
                if any(canonical_json(cell) not in declared_cells for cell in target_cells):
                    raise ExactBoundedDiscoveryError("BASE_QUERY target cell lies outside exact declared target domain")
            for cell in target_cells:
                cell_validation = {**dict(validation), "target_cell": canonicalize(cell)}
                q = _clone_query(
                    tmpl.query, baseline.predicate,
                    role_material={"rule": rule_id, "role": "BASE", "target_cell": canonicalize(cell)},
                )
                candidates.append(_candidate(
                    family=family,
                    rule_id=rule_id,
                    winning_predicate=baseline.predicate,
                    query_roles=(_QueryRole("BASE", baseline.predicate, q),),
                    validation=cell_validation,
                    ancestry_refs=baseline.ancestry_refs,
                ))

        elif form == "JOINT_DEPENDENCE":
            if kind != "JOINT_NOT_PRODUCT_OF_MARGINALS":
                raise ExactBoundedDiscoveryError("JOINT_DEPENDENCE requires joint exact-dependence validator")
            baseline = atom(_text(rule.get("baseline_atom_id"), "baseline_atom_id"))
            joint_t = template(_text(rule.get("joint_template_id"), "joint_template_id"))
            marginal_ids = [_text(x, "marginal_template_id") for x in _sequence(rule.get("marginal_template_ids"), "marginal_template_ids")]
            joint_arity = int(_mapping(joint_t.query.target_arity_and_topology, "joint target topology").get("arity", 0))
            if joint_arity < 2 or joint_arity > max_j or len(marginal_ids) != joint_arity:
                raise ExactBoundedCoverageError("joint/marginal template arity violates declared J frontier")
            roles = [_QueryRole(
                "JOINT", baseline.predicate,
                _clone_query(joint_t.query, baseline.predicate, role_material={"rule": rule_id, "role": "JOINT"}),
            )]
            for idx, template_id in enumerate(marginal_ids):
                mt = template(template_id)
                if int(_mapping(mt.query.target_arity_and_topology, "marginal topology").get("arity", 0)) != 1:
                    raise ExactBoundedDiscoveryError("joint dependence marginals must be scalar target templates")
                roles.append(_QueryRole(
                    f"MARGINAL_{idx}", baseline.predicate,
                    _clone_query(mt.query, baseline.predicate, role_material={"rule": rule_id, "role": f"MARGINAL_{idx}"}),
                ))
            candidates.append(_candidate(
                family=family, rule_id=rule_id, winning_predicate=baseline.predicate,
                query_roles=roles, validation=validation, ancestry_refs=baseline.ancestry_refs,
            ))

        elif form == "REVERSAL_GRID":
            if kind != "CONDITIONAL_REVERSAL":
                raise ExactBoundedDiscoveryError("REVERSAL_GRID requires conditional-reversal validator")
            baseline = atom(_text(rule.get("baseline_atom_id"), "baseline_atom_id"))
            pos = atom(_text(rule.get("exposure_positive_atom_id"), "exposure_positive_atom_id"))
            neg = atom(_text(rule.get("exposure_negative_atom_id"), "exposure_negative_atom_id"))
            strata = [atom(_text(x, "stratum_atom_id")) for x in _sequence(rule.get("stratum_atom_ids"), "stratum_atom_ids")]
            if 2 > max_k or len(strata) < 2:
                raise ExactBoundedCoverageError("reversal grid requires K>=2 and at least two declared strata")
            tmpl = template(_text(rule.get("query_template_id"), "query_template_id"))
            roles: list[_QueryRole] = []
            for label, exposure in (("POOLED_POS", pos), ("POOLED_NEG", neg)):
                pred = _combine_predicates(
                    [baseline.predicate, exposure.predicate], op="AND",
                    tag_material={"rule": rule_id, "role": label},
                )
                roles.append(_QueryRole(label, pred, _clone_query(
                    tmpl.query, pred, role_material={"rule": rule_id, "role": label}
                )))
            for stratum in strata:
                for suffix, exposure in (("POS", pos), ("NEG", neg)):
                    label = f"STRATUM:{stratum.atom_id}:{suffix}"
                    pred = _combine_predicates(
                        [baseline.predicate, stratum.predicate, exposure.predicate], op="AND",
                        tag_material={"rule": rule_id, "role": label},
                    )
                    roles.append(_QueryRole(label, pred, _clone_query(
                        tmpl.query, pred, role_material={"rule": rule_id, "role": label}
                    )))
            candidates.append(_candidate(
                family=family, rule_id=rule_id, winning_predicate=roles[0].predicate,
                query_roles=roles, validation=validation,
                ancestry_refs=[ref for x in strata for ref in x.ancestry_refs] + list(baseline.ancestry_refs),
            ))

    ordered = tuple(sorted(candidates, key=lambda c: c.candidate_hash))
    if len({c.candidate_hash for c in ordered}) != len(ordered):
        raise ExactBoundedDiscoveryError("candidate grammar generated duplicate exact candidate identities")
    return ordered


def _fraction(value: Any) -> Fraction:
    if isinstance(value, int) and not isinstance(value, bool):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    if isinstance(value, Mapping) and set(value) == {"$exact_fraction"}:
        pair = value["$exact_fraction"]
        if isinstance(pair, Sequence) and len(pair) == 2 and all(isinstance(x, int) and not isinstance(x, bool) for x in pair):
            return Fraction(pair[0], pair[1])
    if isinstance(value, Mapping) and set(value) == {"$exact_decimal"} and isinstance(value["$exact_decimal"], str):
        return Fraction(value["$exact_decimal"])
    raise ExactBoundedDiscoveryError("validation encountered non-exact numeric material")


def _fact_scope_key(fact: EmpiricalFact) -> str:
    return canonical_json([exact_ref(x, "fact universe ref").as_dict() for x in fact.empirical_universe_refs])


def _fact_measure_kind(fact: EmpiricalFact) -> str:
    value = fact.semantic_fields.get("measure_kind", "RAW")
    if value not in {"RAW", "GOVERNED_WEIGHTED"}:
        raise ExactBoundedDiscoveryError("fact measure kind is unresolved")
    return value


def _cell_counts(fact: EmpiricalFact) -> tuple[dict[str, Fraction], Fraction]:
    mode = _fact_measure_kind(fact)
    rows = _mapping(fact.target_topology, "fact target_topology").get("complete_cell_semantic_projection")
    if rows is None:
        return {}, Fraction(0, 1)
    result: dict[str, Fraction] = {}
    for raw in _sequence(rows, "complete cells", allow_empty=True):
        row = _mapping(raw, "cell row")
        key = canonical_json(row.get("cell"))
        if mode == "RAW":
            result[key] = Fraction(int(row.get("raw_numerator_support", 0)), 1)
        else:
            weighted = row.get("weighted_numerator_support_if_authorized")
            result[key] = _fraction(weighted) if weighted is not None else Fraction(0, 1)
    denominator = (
        Fraction(fact.raw_denominator_support, 1)
        if mode == "RAW"
        else _fraction(fact.weighted_denominator_support_if_authorized)
    )
    return result, denominator


def _terminal_fact_class(facts: Sequence[EmpiricalFact]) -> str | None:
    states = {fact.typed_state for fact in facts}
    if "INTEGRITY_FAILURE" in states:
        raise ExactBoundedCoverageError("I03 integrity failure cannot be laundered into discovery coverage")
    if states & {"NONCOMPARABLE", "NOT_APPLICABLE"}:
        return "NONCOMPARABLE"
    if states & {"UNAVAILABLE", "UNRESOLVED"}:
        return "UNAVAILABLE"
    if all(fact.raw_denominator_support == 0 or fact.typed_state in {"ZERO_SUPPORT", "VALID_EMPTY"} for fact in facts):
        return "VALID_EMPTY"
    return None


def _distribution_differs(condition: QueryExecutionResult, baseline: QueryExecutionResult) -> bool:
    c = {_fact_scope_key(f): f for f in condition.facts}
    b = {_fact_scope_key(f): f for f in baseline.facts}
    if set(c) != set(b):
        raise ExactBoundedCoverageError("condition/baseline source scopes differ")
    changed = False
    for key in sorted(c):
        cf, bf = c[key], b[key]
        if _fact_measure_kind(cf) != _fact_measure_kind(bf):
            raise ExactBoundedCoverageError("condition/baseline measure mismatch")
        cc, cd = _cell_counts(cf)
        bc, bd = _cell_counts(bf)
        if cd == 0:
            continue
        if bd == 0:
            raise ExactBoundedCoverageError("positive conditioned fact cannot compare to zero-support baseline")
        for cell in sorted(set(cc) | set(bc)):
            if cc.get(cell, Fraction(0, 1)) * bd != bc.get(cell, Fraction(0, 1)) * cd:
                changed = True
                break
    return changed


def _joint_dependence(results: Mapping[str, QueryExecutionResult]) -> bool:
    joint = results["JOINT"]
    marginal_roles = sorted(role for role in results if role.startswith("MARGINAL_"))
    joint_by_scope = {_fact_scope_key(f): f for f in joint.facts}
    marginals_by_role = {
        role: {_fact_scope_key(f): f for f in results[role].facts} for role in marginal_roles
    }
    for scope, jf in joint_by_scope.items():
        if any(scope not in marginals_by_role[role] for role in marginal_roles):
            raise ExactBoundedCoverageError("joint/marginal source scopes differ")
        jc, jd = _cell_counts(jf)
        if jd == 0:
            continue
        marg_material = []
        for role in marginal_roles:
            mf = marginals_by_role[role][scope]
            mc, md = _cell_counts(mf)
            if md == 0:
                raise ExactBoundedCoverageError("joint positive support has zero-support marginal")
            marg_material.append((mc, md))
        for cell_key, observed in jc.items():
            cell = canonicalize(__import__("json").loads(cell_key))
            if not isinstance(cell, Sequence) or isinstance(cell, str) or len(cell) != len(marg_material):
                raise ExactBoundedDiscoveryError("joint cell arity does not match marginal templates")
            lhs = observed
            rhs = jd
            for idx, (counts, denominator) in enumerate(marg_material):
                lhs *= denominator
                rhs *= counts.get(canonical_json(cell[idx]), Fraction(0, 1))
            # observed/jd != product(count_i/den_i)
            if lhs != rhs:
                return True
    return False


def _target_cell_supported(result: QueryExecutionResult, target_cell: Any) -> bool:
    key = canonical_json(target_cell)
    for fact in result.facts:
        cells, denominator = _cell_counts(fact)
        if denominator > 0 and cells.get(key, Fraction(0, 1)) > 0:
            return True
    return False


def _cell_rate(result: QueryExecutionResult, target_cell: Any) -> Fraction | None:
    if len(result.facts) != 1:
        raise ExactBoundedDiscoveryError("reversal validation currently requires one exact source universe")
    fact = result.facts[0]
    cells, denominator = _cell_counts(fact)
    if denominator == 0:
        return None
    return cells.get(canonical_json(target_cell), Fraction(0, 1)) / denominator


def _sign(value: Fraction) -> int:
    return 1 if value > 0 else (-1 if value < 0 else 0)


def _conditional_reversal(results: Mapping[str, QueryExecutionResult], validation: Mapping[str, Any]) -> bool:
    target_cell = validation.get("target_cell")
    pooled_pos = _cell_rate(results["POOLED_POS"], target_cell)
    pooled_neg = _cell_rate(results["POOLED_NEG"], target_cell)
    if pooled_pos is None or pooled_neg is None:
        return False
    pooled_sign = _sign(pooled_pos - pooled_neg)
    if pooled_sign == 0:
        return False
    strata = sorted({role.split(":", 2)[1] for role in results if role.startswith("STRATUM:")})
    signs = []
    for stratum in strata:
        pos = _cell_rate(results[f"STRATUM:{stratum}:POS"], target_cell)
        neg = _cell_rate(results[f"STRATUM:{stratum}:NEG"], target_cell)
        if pos is None or neg is None:
            return False
        signs.append(_sign(pos - neg))
    return bool(signs) and all(sign != 0 and sign == signs[0] for sign in signs) and signs[0] == -pooled_sign


def _support_summary(facts: Sequence[EmpiricalFact]) -> Mapping[str, Any]:
    return canonicalize({
        "fact_states": [f.typed_state for f in sorted(facts, key=lambda f: f.ref.key)],
        "raw_denominators": [f.raw_denominator_support for f in sorted(facts, key=lambda f: f.ref.key)],
        "weighted_denominators_if_authorized": [
            f.weighted_denominator_support_if_authorized for f in sorted(facts, key=lambda f: f.ref.key)
        ],
        "uncertainty": [
            f.uncertainty_method_or_typed_state for f in sorted(facts, key=lambda f: f.ref.key)
        ],
        "risk_set_refs": [canonicalize(f.risk_set_ref) for f in sorted(facts, key=lambda f: f.ref.key)],
        "source_universe_refs": [
            [canonicalize(x) for x in f.empirical_universe_refs] for f in sorted(facts, key=lambda f: f.ref.key)
        ],
        "measure_basis_refs": [canonicalize(f.measure_basis_ref) for f in sorted(facts, key=lambda f: f.ref.key)],
    })


def _evaluate_candidate(
    candidate: _Candidate,
    *,
    repository,
    registry: AuthorityRegistry,
    release_refs: Iterable[ExactRef],
    minimum_raw_denominator: int,
) -> tuple[str, str, tuple[EmpiricalFact, ...], Mapping[str, Any]]:
    results: dict[str, QueryExecutionResult] = {}
    facts: list[EmpiricalFact] = []
    for role in candidate.query_roles:
        result = execute_empirical_query(
            repository=repository,
            query=role.query,
            predicate=role.predicate,
            authority_registry=registry,
            release_refs=release_refs,
        )
        results[role.role] = result
        facts.extend(result.facts)
    canonical_facts = tuple(sorted({f.ref.key: f for f in facts}.values(), key=lambda f: f.ref.key))
    if not canonical_facts:
        raise ExactBoundedCoverageError("I03 candidate evaluation returned no EmpiricalFact; row absence is not a terminal state")
    support = dict(_support_summary(canonical_facts))
    support["query_role_fact_refs"] = canonicalize({
        role: [fact.ref.as_dict() for fact in results[role].facts]
        for role in sorted(results)
    })
    terminal = _terminal_fact_class(canonical_facts)
    if terminal == "NONCOMPARABLE":
        return "EVALUATED_NONCOMPARABLE", "NONCOMPARABLE", canonical_facts, support
    if terminal == "UNAVAILABLE":
        return "EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY", "COVERAGE_LIMITED", canonical_facts, support
    if terminal == "VALID_EMPTY":
        return "EVALUATED_VALID_EMPTY", "VALID_EMPTY", canonical_facts, support

    primary = [f for f in canonical_facts if f.typed_state in {"SUPPORTED", "LOW_SUPPORT", "OBSERVED_ZERO"}]
    if primary and any(f.raw_denominator_support < minimum_raw_denominator for f in primary):
        return "EVALUATED_UNDERPOWERED", "INSUFFICIENT_SUPPORT", canonical_facts, support

    kind = candidate.validation["kind"]
    if kind == "DISTRIBUTION_DIFFERS_FROM_BASELINE":
        supported = _distribution_differs(results["CONDITION"], results["BASELINE"])
    elif kind == "JOINT_NOT_PRODUCT_OF_MARGINALS":
        supported = _joint_dependence(results)
    elif kind == "CONDITIONAL_REVERSAL":
        supported = _conditional_reversal(results, candidate.validation)
    elif kind == "TARGET_CELL_SUPPORTED":
        supported = _target_cell_supported(results["BASE"], candidate.validation.get("target_cell"))
    else:
        raise ExactBoundedDiscoveryError("unreachable validation kind")
    if supported:
        return "EVALUATED_SUPPORTED", "DISCOVERED_RESULT_SUPPORTED", canonical_facts, support
    return "EVALUATED_VALID_EMPTY", "VALID_EMPTY", canonical_facts, support


def execute_exact_bounded_discovery(
    *,
    repository,
    discovery_authority: DiscoveryAuthority,
    authority_registry: AuthorityRegistry,
    release_refs: Iterable[ExactRef],
    predicate_catalog: Iterable[EmpiricalPredicate],
    query_template_catalog: Iterable[EmpiricalQuerySpec],
) -> ExactBoundedDiscoveryResult:
    """Compile and exhaustively evaluate the exact authority-declared frontier.

    Candidate enumeration is entirely determined before the first I03 query is
    executed.  Results can affect validation outcomes, never frontier reachability.
    """
    if not isinstance(authority_registry, AuthorityRegistry):
        raise ExactBoundedDiscoveryError("authority_registry must be exact immutable AuthorityRegistry")
    definition = _verify_discovery_authority(discovery_authority, authority_registry)
    atoms = _catalog_atoms(definition, predicate_catalog)
    templates = _catalog_templates(definition, query_template_catalog)
    _validate_catalog_scope(discovery_authority, atoms, templates)
    candidates = _compile_frontier(definition, atoms, templates)
    allowed_validation = _allowed_validation_kinds(discovery_authority.validation_rules)
    used_validation = {c.validation["kind"] for c in candidates}
    if not used_validation <= allowed_validation:
        raise Pre553AuthorityError("candidate validation rule exceeds exact discovery validation authority")

    grammar_ref = exact_ref(discovery_authority.candidate_grammar_ref, "candidate_grammar_ref")
    frontier_material = {
        "contract": I05_CONTRACT_ID,
        "discovery_authority_ref": discovery_authority.ref.as_dict(),
        "candidate_grammar_ref": grammar_ref.as_dict(),
        "query_execution_contract": QUERY_EXECUTION_CONTRACT_ID,
        "candidate_identities": [
            {"candidate_id": c.candidate_id, "candidate_hash": c.candidate_hash} for c in candidates
        ],
        "coverage_claim": COVERAGE_CLAIM,
    }
    frontier_ref = _derived_ref("PRE553_I05_EVALUATED_FRONTIER", "frontier", frontier_material)
    support_rules = _mapping(discovery_authority.support_rules, "support_rules")
    minimum_raw_denominator = support_rules.get("minimum_raw_denominator", 1)
    if not isinstance(minimum_raw_denominator, int) or isinstance(minimum_raw_denominator, bool) or minimum_raw_denominator < 0:
        raise ExactBoundedDiscoveryError("minimum_raw_denominator must be exact nonnegative integer")

    receipts: list[DiscoveryResultReceipt] = []
    all_facts: list[EmpiricalFact] = []
    release_refs_tuple = _canonical_refs(exact_ref(ref, "release_ref") for ref in release_refs)
    if not release_refs_tuple:
        raise ExactBoundedDiscoveryError("one or more exact C11 release refs required")

    for candidate in candidates:
        coverage_state, typed_state, facts, support = _evaluate_candidate(
            candidate,
            repository=repository,
            registry=authority_registry,
            release_refs=release_refs_tuple,
            minimum_raw_denominator=minimum_raw_denominator,
        )
        if coverage_state not in TERMINAL_COVERAGE_STATES:
            raise ExactBoundedCoverageError("candidate did not receive terminal exact coverage state")
        fact_refs = _canonical_refs(f.ref for f in facts)
        all_facts.extend(facts)
        replay_material = {
            "contract": I05_CONTRACT_ID,
            "authority_ref": discovery_authority.ref.as_dict(),
            "frontier_ref": frontier_ref.as_dict(),
            "candidate_id": candidate.candidate_id,
            "candidate_hash": candidate.candidate_hash,
            "coverage_state": coverage_state,
            "fact_refs": [x.as_dict() for x in fact_refs],
            "release_refs": [x.as_dict() for x in release_refs_tuple],
            "query_execution_contract": QUERY_EXECUTION_CONTRACT_ID,
        }
        replay_ref = _derived_ref("PRE553_I05_DISCOVERY_REPLAY", "candidate-replay", replay_material)
        receipt = DiscoveryResultReceipt(
            typed_state=typed_state,
            authority_snapshot_refs=_canonical_auths([
                *discovery_authority.authority_snapshot_refs,
                *(ref for f in facts for ref in f.authority_snapshot_refs),
            ]),
            dependency_refs=_canonical_refs([
                discovery_authority.ref,
                grammar_ref,
                frontier_ref,
                candidate.winning_predicate.ref,
                *fact_refs,
            ]),
            producer_replay_locator_or_reference_root=replay_ref,
            discovery_authority_ref=discovery_authority.ref,
            candidate_identity={
                "candidate_id": candidate.candidate_id,
                "candidate_hash": candidate.candidate_hash,
                "family": candidate.family,
                "rule_id": candidate.rule_id,
                "validation": candidate.validation,
                "query_roles": [
                    {"role": role.role, "predicate_ref": role.predicate.ref, "query_ref": role.query.ref}
                    for role in candidate.query_roles
                ],
            },
            winning_predicate_ref=candidate.winning_predicate.ref,
            empirical_fact_refs=fact_refs,
            validation_fact_refs=fact_refs,
            coverage_state=coverage_state,
            evaluated_frontier_ref=frontier_ref,
            branch_or_parent_ancestry_refs=candidate.ancestry_refs,
            support_uncertainty_state=support,
            replay_ref=replay_ref,
            source_release_refs=release_refs_tuple,
            exact_query_contract_id=QUERY_EXECUTION_CONTRACT_ID,
            diagnostic_score_is_empirical_fact=False,
            structural_truth_effect=False,
            actor_v3_effect=False,
        )
        receipts.append(receipt)

    canonical_receipts = tuple(sorted(receipts, key=lambda r: r.ref.key))
    if len(canonical_receipts) != len(candidates):
        raise ExactBoundedCoverageError("candidate/receipt cardinality mismatch")
    if any(r.coverage_state not in TERMINAL_COVERAGE_STATES for r in canonical_receipts):
        raise ExactBoundedCoverageError("complete frontier contains nonterminal candidate")

    all_fact_objects = tuple(
        sorted({fact.ref.key: fact for fact in all_facts}.values(), key=lambda fact: fact.ref.key)
    )
    predicate_objects: dict[str, EmpiricalPredicate] = {}
    query_objects: dict[str, EmpiricalQuerySpec] = {}
    for candidate in candidates:
        for role in candidate.query_roles:
            for collection, obj, cls, label in (
                (predicate_objects, role.predicate, EmpiricalPredicate, "executed predicate"),
                (query_objects, role.query, EmpiricalQuerySpec, "executed query"),
            ):
                _verify_object_identity(obj, cls, label)
                previous = collection.setdefault(obj.ref.key, obj)
                if canonical_json(previous.as_dict()) != canonical_json(obj.as_dict()):
                    raise ExactBoundedDiscoveryError(
                        f"conflicting {label} preimages share one exact ref"
                    )
    all_executed_predicates = tuple(
        sorted(predicate_objects.values(), key=lambda obj: obj.ref.key)
    )
    all_executed_queries = tuple(
        sorted(query_objects.values(), key=lambda obj: obj.ref.key)
    )
    all_fact_refs = tuple(fact.ref for fact in all_fact_objects)
    valid_empty = not canonical_receipts or all(
        r.typed_state == "VALID_EMPTY" for r in canonical_receipts
    )
    final_replay = _derived_ref(
        "PRE553_I05_FRONTIER_REPLAY",
        "frontier-replay",
        {
            "contract": I05_CONTRACT_ID,
            "frontier_ref": frontier_ref.as_dict(),
            "receipt_refs": [r.ref.as_dict() for r in canonical_receipts],
            "fact_refs": [r.as_dict() for r in all_fact_refs],
            "valid_empty": valid_empty,
        },
    )
    return ExactBoundedDiscoveryResult(
        contract_id=I05_CONTRACT_ID,
        discovery_authority_ref=discovery_authority.ref,
        candidate_grammar_ref=grammar_ref,
        evaluated_frontier_ref=frontier_ref,
        coverage_claim=COVERAGE_CLAIM,
        candidate_count=len(candidates),
        covered_candidate_count=len(canonical_receipts),
        receipts=canonical_receipts,
        empirical_fact_refs=all_fact_refs,
        empirical_facts=all_fact_objects,
        executed_predicates=all_executed_predicates,
        executed_queries=all_executed_queries,
        valid_empty=valid_empty,
        replay_ref=final_replay,
    )


__all__ = [
    "I05_CONTRACT_ID",
    "CANDIDATE_GRAMMAR_SCHEMA",
    "CANDIDATE_GRAMMAR_CONTRACT",
    "COVERAGE_CLAIM",
    "ExactBoundedDiscoveryError",
    "ExactBoundedCoverageError",
    "ExactBoundedDiscoveryResult",
    "execute_exact_bounded_discovery",
]
