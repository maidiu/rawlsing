"""Persisted recursive-branch handoff for PRE553 I05.

MX01 R2 closes exactly one common-contract seam:

    discovered child -> canonical persisted parent for discovery generation N+1

The semantic carrier is the existing C11-internal ``DiscoveryBranchReplayBinding``.
No new public semantic-object family is introduced.  The handoff resolves the
receipt-bound compiled child predicate from the authority-frozen public grammar
and exact predicate catalog, persists that predicate plus replay side material,
and exposes a fresh-process N+1 consumption path without caller-guessed branch
membership, ``_Candidate`` state, or private ``_compile_frontier`` state.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next._pre553_query_predicate import _build_release_index, _eval_predicate
from rawlsing_next.pre553_c11_integrity import DiscoveryBranchReplayBinding, TypedAbsence
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_discovery_exact import (
    I05_CONTRACT_ID,
    ExactBoundedDiscoveryResult,
    execute_exact_bounded_discovery,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry, validate_object_authority_closure
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    DiscoveryAuthority,
    DiscoveryResultReceipt,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    EmpiricalUniverse,
    ExactRef,
    Pre553IntegrityError,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    make_empirical_predicate,
    semantic_hash,
)

RECURSIVE_HANDOFF_CONTRACT_ID = "PRE553_MX01R2_RECURSIVE_HANDOFF@1.0.0"
RECURSIVE_BRANCH_FAMILIES = frozenset({"RECURSIVE_SUBGROUP_FORK"})
SUPPORTED_RECURSIVE_FORMS = frozenset({
    "SINGLE_ATOM",
    "AND_COMBINATIONS",
    "AND_CARTESIAN_GROUPS",
    "XOR_EXACTLY_ONE_COMBINATIONS",
})


class RecursiveHandoffError(Pre553IntegrityError):
    """Recursive handoff identity, lineage, or replay closure is invalid."""


def _derived_ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:pre553:mx01r2:{namespace}:sha256:{digest}", digest)


def _i05_derived_ref(kind: str, namespace: str, material: Any) -> ExactRef:
    """Reproduce I05's content-addressed replay-ref namespace exactly."""
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:pre553:i05:{namespace}:sha256:{digest}", digest)


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise RecursiveHandoffError(f"{name} must be an exact mapping")
    return value


def _sequence(value: Any, name: str, *, allow_empty: bool = False) -> Sequence[Any]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise RecursiveHandoffError(f"{name} must be a sequence")
    if not allow_empty and not value:
        raise RecursiveHandoffError(f"{name} may not be empty")
    return value


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecursiveHandoffError(f"{name} must be non-empty text")
    return value.strip()


def _canonical_refs(values: Iterable[ExactRef | Mapping[str, Any]]) -> tuple[ExactRef, ...]:
    refs = [exact_ref(value) for value in values]
    return tuple(sorted(set(refs), key=lambda ref: ref.key))


def _canonical_auths(values: Iterable[AuthorityRef | Mapping[str, Any]]) -> tuple[AuthorityRef, ...]:
    refs = [authority_ref(value) for value in values]
    return tuple(sorted(set(refs), key=lambda ref: ref.key))


def _typed_absence(value: Mapping[str, Any]) -> TypedAbsence:
    if set(value) != {"typed_absence_state", "detail"}:
        raise RecursiveHandoffError("typed absence material has unexpected fields")
    return TypedAbsence(value["typed_absence_state"], value["detail"])


def _exact_or_absence(value: Any) -> ExactRef | TypedAbsence:
    if isinstance(value, Mapping) and "typed_absence_state" in value:
        return _typed_absence(value)
    return exact_ref(value)


def _authority_or_absence(value: Any) -> AuthorityRef | TypedAbsence:
    if isinstance(value, Mapping) and "typed_absence_state" in value:
        return _typed_absence(value)
    return authority_ref(value)


def _text_or_absence(value: Any) -> str | TypedAbsence:
    if isinstance(value, Mapping) and "typed_absence_state" in value:
        return _typed_absence(value)
    return _text(value, "text-or-absence")


def _restore_predicate(payload: Mapping[str, Any]) -> EmpiricalPredicate:
    fields = _mapping(payload.get("semantic_fields"), "persisted predicate semantic_fields")
    predicate = EmpiricalPredicate(
        typed_state=payload.get("typed_state"),
        authority_snapshot_refs=payload.get("authority_snapshot_refs", ()),
        dependency_refs=payload.get("dependency_refs", ()),
        producer_replay_locator_or_reference_root=payload.get("producer_replay_locator_or_reference_root"),
        object_id=payload.get("object_id"),
        content_hash=payload.get("content_hash"),
        schema_id=payload.get("schema_id"),
        schema_version=payload.get("schema_version"),
        **dict(fields),
    )
    if canonical_json(predicate.as_dict()) != canonical_json(payload):
        raise RecursiveHandoffError("persisted predicate projection is not identity-exact")
    return predicate


def _restore_binding(payload: Mapping[str, Any]) -> DiscoveryBranchReplayBinding:
    fields = _mapping(payload.get("semantic_fields"), "persisted replay binding semantic_fields")
    binding = DiscoveryBranchReplayBinding(
        state=fields.get("state"),
        search_family_id_or_typed_absence=_text_or_absence(fields.get("search_family_id_or_typed_absence")),
        candidate_universe_ref_or_typed_absence=_exact_or_absence(fields.get("candidate_universe_ref_or_typed_absence")),
        grammar_authority_ref_or_typed_absence=_authority_or_absence(fields.get("grammar_authority_ref_or_typed_absence")),
        source_risk_topology_measure_scope_ref_or_typed_absence=_exact_or_absence(fields.get("source_risk_topology_measure_scope_ref_or_typed_absence")),
        algorithm_identity_ref_or_typed_absence=_exact_or_absence(fields.get("algorithm_identity_ref_or_typed_absence")),
        coverage_pruning_contract_ref_or_typed_absence=_exact_or_absence(fields.get("coverage_pruning_contract_ref_or_typed_absence")),
        deterministic_parameters_ref_or_typed_absence=_exact_or_absence(fields.get("deterministic_parameters_ref_or_typed_absence")),
        rng_state_ref_or_typed_absence=_exact_or_absence(fields.get("rng_state_ref_or_typed_absence")),
        parent_branch_ref_or_typed_absence=_exact_or_absence(fields.get("parent_branch_ref_or_typed_absence")),
        winning_predicate_ref_or_typed_absence=_exact_or_absence(fields.get("winning_predicate_ref_or_typed_absence")),
        pruned_trace_ref_or_typed_absence=_exact_or_absence(fields.get("pruned_trace_ref_or_typed_absence")),
    )
    if binding.object_id != payload.get("object_id") or binding.content_hash != payload.get("content_hash"):
        raise RecursiveHandoffError("persisted replay binding identity mismatch")
    return binding


def _compose_predicates(
    predicates: Sequence[EmpiricalPredicate], *, op: str, tag_material: Any
) -> EmpiricalPredicate:
    """Exact public re-materialization of I05 boolean predicate composition."""
    if not predicates:
        raise RecursiveHandoffError("cannot compose empty predicate set")
    grammar_refs = {canonical_json(predicate.grammar_authority_ref) for predicate in predicates}
    bindings = {predicate.same_respondent_binding_semantics for predicate in predicates}
    if len(grammar_refs) != 1 or len(bindings) != 1:
        raise RecursiveHandoffError("composed predicates must share exact grammar/respondent binding")
    if op not in {"AND", "OR"}:
        raise RecursiveHandoffError("recursive predicate composition supports AND/OR only")
    return make_empirical_predicate(
        predicate_ast={"op": op, "children": [predicate.predicate_ast for predicate in predicates]},
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=_canonical_auths(
            ref for predicate in predicates for ref in predicate.authority_snapshot_refs
        ),
        dependency_refs=_canonical_refs(predicate.ref for predicate in predicates),
        producer_replay_locator_or_reference_root=_i05_derived_ref(
            "PRE553_I05_PREDICATE_REPLAY_ROOT", "predicate-replay", tag_material
        ),
        grammar_authority_ref=predicates[0].grammar_authority_ref,
        coordinate_question_value_refs=_canonical_refs(
            ref for predicate in predicates for ref in predicate.coordinate_question_value_refs
        ),
        risk_set_refs=_canonical_refs(
            ref for predicate in predicates for ref in predicate.risk_set_refs
        ),
        scope_refs=_canonical_refs(
            ref for predicate in predicates for ref in predicate.scope_refs
        ),
        same_respondent_binding_semantics=predicates[0].same_respondent_binding_semantics,
        operator_semantics_refs=_canonical_refs(
            ref for predicate in predicates for ref in predicate.operator_semantics_refs
        ),
    )


def _xor_exactly_one(predicates: Sequence[EmpiricalPredicate], *, tag_material: Any) -> EmpiricalPredicate:
    if len(predicates) < 2:
        raise RecursiveHandoffError("XOR_EXACTLY_ONE requires at least two predicates")
    ors = {"op": "OR", "children": [predicate.predicate_ast for predicate in predicates]}
    pair_ands = [
        {"op": "AND", "children": [left.predicate_ast, right.predicate_ast]}
        for left, right in combinations(predicates, 2)
    ]
    no_pair = {"op": "NOT", "children": [{"op": "OR", "children": pair_ands}]}
    common = _compose_predicates(predicates, op="OR", tag_material={"probe": tag_material})
    return make_empirical_predicate(
        predicate_ast={"op": "AND", "children": [ors, no_pair]},
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=common.authority_snapshot_refs,
        dependency_refs=_canonical_refs(predicate.ref for predicate in predicates),
        producer_replay_locator_or_reference_root=_i05_derived_ref(
            "PRE553_I05_PREDICATE_REPLAY_ROOT", "xor-predicate-replay", tag_material
        ),
        grammar_authority_ref=common.grammar_authority_ref,
        coordinate_question_value_refs=common.coordinate_question_value_refs,
        risk_set_refs=common.risk_set_refs,
        scope_refs=common.scope_refs,
        same_respondent_binding_semantics=common.same_respondent_binding_semantics,
        operator_semantics_refs=common.operator_semantics_refs,
    )


def _public_atom_predicates(
    definition: Mapping[str, Any], predicates: Sequence[EmpiricalPredicate]
) -> dict[str, EmpiricalPredicate]:
    by_ref: dict[str, EmpiricalPredicate] = {}
    for predicate in predicates:
        if not isinstance(predicate, EmpiricalPredicate):
            raise RecursiveHandoffError("predicate catalog item has wrong type")
        if semantic_hash(predicate.semantic_projection()) != predicate.content_hash:
            raise RecursiveHandoffError("predicate catalog item identity mismatch")
        if predicate.ref.key in by_ref:
            raise RecursiveHandoffError("duplicate predicate exact ref in catalog")
        by_ref[predicate.ref.key] = predicate
    atoms: dict[str, EmpiricalPredicate] = {}
    for raw in _sequence(definition.get("atoms", ()), "candidate grammar atoms", allow_empty=True):
        item = _mapping(raw, "candidate atom")
        atom_id = _text(item.get("atom_id"), "atom_id")
        ref = exact_ref(item.get("predicate_ref"), f"atom {atom_id}.predicate_ref")
        predicate = by_ref.get(ref.key)
        if predicate is None:
            raise RecursiveHandoffError(f"candidate atom {atom_id!r} exact predicate unavailable")
        atoms[atom_id] = predicate
    return atoms


def _selected_groups(rule: Mapping[str, Any], atoms: Mapping[str, EmpiricalPredicate]):
    form = _text(rule.get("form"), "recursive rule form")
    if form not in SUPPORTED_RECURSIVE_FORMS:
        raise RecursiveHandoffError(f"unsupported recursive rule form {form!r}")
    if form == "SINGLE_ATOM":
        for value in _sequence(rule.get("atom_ids"), "atom_ids"):
            atom_id = _text(value, "atom_id")
            yield ((atom_id, atoms[atom_id]),)
        return
    if form in {"AND_COMBINATIONS", "XOR_EXACTLY_ONE_COMBINATIONS"}:
        ids = tuple(_text(value, "atom_id") for value in _sequence(rule.get("atom_ids"), "atom_ids"))
        arity = rule.get("arity")
        if not isinstance(arity, int) or isinstance(arity, bool) or arity < 1:
            raise RecursiveHandoffError("recursive combination arity must be positive integer")
        for selected in combinations(ids, arity):
            yield tuple((atom_id, atoms[atom_id]) for atom_id in selected)
        return
    groups = [
        tuple(_text(value, "atom_id") for value in _sequence(group, "atom group"))
        for group in _sequence(rule.get("atom_groups"), "atom_groups")
    ]
    for selected in product(*groups):
        yield tuple((atom_id, atoms[atom_id]) for atom_id in selected)


def _resolve_receipt_winner(
    receipt: DiscoveryResultReceipt,
    definition: Mapping[str, Any],
    predicates: Sequence[EmpiricalPredicate],
) -> tuple[EmpiricalPredicate, EmpiricalPredicate]:
    identity = _mapping(receipt.candidate_identity, "candidate_identity")
    family = _text(identity.get("family"), "candidate family")
    rule_id = _text(identity.get("rule_id"), "candidate rule_id")
    if family not in RECURSIVE_BRANCH_FAMILIES:
        raise RecursiveHandoffError("receipt is not a recursive branch family")
    winning_ref = exact_ref(receipt.winning_predicate_ref, "receipt.winning_predicate_ref")
    atoms = _public_atom_predicates(definition, predicates)
    rules = [
        _mapping(raw, "candidate rule")
        for raw in _sequence(definition.get("rules", ()), "candidate rules", allow_empty=True)
        if _mapping(raw, "candidate rule").get("rule_id") == rule_id
        and _mapping(raw, "candidate rule").get("family") == family
    ]
    if len(rules) != 1:
        raise RecursiveHandoffError("receipt must resolve to exactly one governed recursive rule")
    rule = rules[0]
    baseline_id = _text(rule.get("baseline_atom_id"), "baseline_atom_id")
    if baseline_id not in atoms:
        raise RecursiveHandoffError("recursive baseline predicate unavailable")
    baseline = atoms[baseline_id]
    form = _text(rule.get("form"), "recursive rule form")
    matches: list[EmpiricalPredicate] = []
    for selected in _selected_groups(rule, atoms):
        selected_ids = [atom_id for atom_id, _ in selected]
        selected_predicates = [predicate for _, predicate in selected]
        if form == "SINGLE_ATOM":
            condition = selected_predicates[0]
        elif form == "XOR_EXACTLY_ONE_COMBINATIONS":
            condition = _xor_exactly_one(
                selected_predicates,
                tag_material={"rule": rule_id, "atoms": selected_ids},
            )
        else:
            condition = _compose_predicates(
                selected_predicates,
                op="AND",
                tag_material={"rule": rule_id, "atoms": selected_ids},
            )
        if baseline_id not in selected_ids:
            condition = _compose_predicates(
                (baseline, condition),
                op="AND",
                tag_material={
                    "rule": rule_id,
                    "baseline": baseline_id,
                    "condition": condition.ref.as_dict(),
                },
            )
        if condition.ref == winning_ref:
            matches.append(condition)
    if len(matches) != 1:
        raise RecursiveHandoffError(
            "receipt winning predicate must resolve to exactly one governed compiled predicate"
        )
    return matches[0], baseline


@dataclass(frozen=True)
class RecursiveBranchHandoff:
    receipt_ref: ExactRef
    branch_replay_binding: DiscoveryBranchReplayBinding
    winning_predicate: EmpiricalPredicate
    source_release_refs: tuple[ExactRef, ...]
    discovery_authority_ref: ExactRef
    evaluated_frontier_ref: ExactRef
    candidate_universe_definition: Mapping[str, Any]
    scope_context: Mapping[str, Any]
    coverage_pruning_material: Mapping[str, Any]
    deterministic_parameters: Mapping[str, Any]

    def __post_init__(self) -> None:
        binding = self.branch_replay_binding
        if binding.state != "PRESENT":
            raise RecursiveHandoffError("recursive handoff requires PRESENT replay binding")
        parent = binding.parent_branch_ref_or_typed_absence
        winner = binding.winning_predicate_ref_or_typed_absence
        if not isinstance(parent, ExactRef):
            raise RecursiveHandoffError("recursive handoff requires exact immediate parent")
        if not isinstance(winner, ExactRef) or winner != self.winning_predicate.ref:
            raise RecursiveHandoffError("replay binding winner does not bind persisted predicate")
        grammar_auth = binding.grammar_authority_ref_or_typed_absence
        if not isinstance(grammar_auth, AuthorityRef) or grammar_auth != authority_ref(self.winning_predicate.grammar_authority_ref):
            raise RecursiveHandoffError("replay binding grammar authority mismatch")
        if not self.source_release_refs:
            raise RecursiveHandoffError("recursive handoff requires exact source releases")
        candidate_ref = binding.candidate_universe_ref_or_typed_absence
        if not isinstance(candidate_ref, ExactRef) or candidate_ref.content_hash != semantic_hash(self.candidate_universe_definition):
            raise RecursiveHandoffError("candidate-universe side material mismatch")
        scope_ref = binding.source_risk_topology_measure_scope_ref_or_typed_absence
        if not isinstance(scope_ref, ExactRef) or scope_ref.content_hash != semantic_hash(self.scope_context):
            raise RecursiveHandoffError("scope-context side material mismatch")
        coverage_ref = binding.coverage_pruning_contract_ref_or_typed_absence
        if not isinstance(coverage_ref, ExactRef) or coverage_ref.content_hash != semantic_hash(self.coverage_pruning_material):
            raise RecursiveHandoffError("coverage/pruning side material mismatch")
        deterministic_ref = binding.deterministic_parameters_ref_or_typed_absence
        if not isinstance(deterministic_ref, ExactRef) or deterministic_ref.content_hash != semantic_hash(self.deterministic_parameters):
            raise RecursiveHandoffError("deterministic replay side material mismatch")
        scope = _mapping(self.scope_context, "scope_context")
        if exact_ref(scope.get("discovery_authority_ref")) != self.discovery_authority_ref:
            raise RecursiveHandoffError("scope discovery-authority ref mismatch")
        if exact_ref(scope.get("evaluated_frontier_ref")) != self.evaluated_frontier_ref:
            raise RecursiveHandoffError("scope frontier ref mismatch")
        if _canonical_refs(scope.get("source_release_refs", ())) != self.source_release_refs:
            raise RecursiveHandoffError("scope source-release set mismatch")

    @property
    def ref(self) -> ExactRef:
        return self.branch_replay_binding.ref

    @property
    def immediate_parent_branch_ref(self) -> ExactRef:
        value = self.branch_replay_binding.parent_branch_ref_or_typed_absence
        if not isinstance(value, ExactRef):
            raise RecursiveHandoffError("immediate parent unavailable")
        return value

    def as_dict(self) -> dict[str, Any]:
        return canonicalize({
            "contract_id": RECURSIVE_HANDOFF_CONTRACT_ID,
            "handoff_ref": self.ref,
            "receipt_ref": self.receipt_ref,
            "branch_replay_binding": self.branch_replay_binding.as_dict(),
            "winning_predicate": self.winning_predicate.as_dict(),
            "source_release_refs": self.source_release_refs,
            "discovery_authority_ref": self.discovery_authority_ref,
            "evaluated_frontier_ref": self.evaluated_frontier_ref,
            "candidate_universe_definition": self.candidate_universe_definition,
            "scope_context": self.scope_context,
            "coverage_pruning_material": self.coverage_pruning_material,
            "deterministic_parameters": self.deterministic_parameters,
        })


@dataclass(frozen=True)
class RecursiveHandoffDiscoveryResult:
    discovery_result: ExactBoundedDiscoveryResult
    handoffs: tuple[RecursiveBranchHandoff, ...]

    def __post_init__(self) -> None:
        if tuple(sorted(self.handoffs, key=lambda handoff: handoff.ref.key)) != self.handoffs:
            raise RecursiveHandoffError("recursive handoffs must be exact-ref sorted")
        if len({handoff.ref.key for handoff in self.handoffs}) != len(self.handoffs):
            raise RecursiveHandoffError("duplicate recursive handoff ref")

    def handoff_for_receipt(self, receipt_ref: ExactRef | Mapping[str, Any]) -> RecursiveBranchHandoff:
        target = exact_ref(receipt_ref)
        matches = [handoff for handoff in self.handoffs if handoff.receipt_ref == target]
        if len(matches) != 1:
            raise RecursiveHandoffError("receipt must resolve to exactly one recursive handoff")
        return matches[0]


def _make_handoff(
    *,
    winning_predicate: EmpiricalPredicate,
    immediate_parent: EmpiricalPredicate,
    receipt: DiscoveryResultReceipt,
    discovery_authority: DiscoveryAuthority,
    discovery_result: ExactBoundedDiscoveryResult,
    release_refs: tuple[ExactRef, ...],
    definition: Mapping[str, Any],
) -> RecursiveBranchHandoff:
    if exact_ref(receipt.winning_predicate_ref) != winning_predicate.ref:
        raise RecursiveHandoffError("receipt/winning predicate ref mismatch")
    identity = _mapping(receipt.candidate_identity, "candidate_identity")
    family = _text(identity.get("family"), "candidate family")
    scope_context = canonicalize({
        "source_universe_scope": discovery_authority.source_universe_scope,
        "risk_set_scope": discovery_authority.risk_set_scope,
        "topology_scope": discovery_authority.topology_scope,
        "measure_scope": discovery_authority.measure_scope,
        "same_respondent_binding_semantics": winning_predicate.same_respondent_binding_semantics,
        "discovery_authority_ref": discovery_authority.ref,
        "evaluated_frontier_ref": discovery_result.evaluated_frontier_ref,
        "source_release_refs": release_refs,
        "query_execution_contract_id": receipt.exact_query_contract_id,
    })
    coverage_pruning_material = canonicalize({
        "coverage_claim": discovery_authority.coverage_claim,
        "pruning_contract": discovery_authority.pruning_contract,
        "candidate_scoring_or_ranking_rule_if_any": discovery_authority.semantic_fields.get(
            "candidate_scoring_or_ranking_rule_if_any"
        ),
        "tie_order_rules": discovery_authority.tie_order_rules,
        "rng_policy_if_any": discovery_authority.rng_policy_if_any,
    })
    deterministic_parameters = canonicalize({
        "receipt_ref": receipt.ref,
        "candidate_identity": receipt.candidate_identity,
        "winning_predicate_ref": winning_predicate.ref,
        "immediate_parent_branch_ref": immediate_parent.ref,
        "support_rules": discovery_authority.support_rules,
        "validation_rules": discovery_authority.validation_rules,
    })
    binding = DiscoveryBranchReplayBinding(
        state="PRESENT",
        search_family_id_or_typed_absence=family,
        candidate_universe_ref_or_typed_absence=discovery_result.candidate_grammar_ref,
        grammar_authority_ref_or_typed_absence=authority_ref(winning_predicate.grammar_authority_ref),
        source_risk_topology_measure_scope_ref_or_typed_absence=_derived_ref(
            "PRE553_RECURSIVE_SCOPE_CONTEXT", "scope-context", scope_context
        ),
        algorithm_identity_ref_or_typed_absence=_derived_ref(
            "PRE553_I05_ALGORITHM_IDENTITY", "algorithm-identity", {"algorithm_identity": I05_CONTRACT_ID}
        ),
        coverage_pruning_contract_ref_or_typed_absence=_derived_ref(
            "PRE553_RECURSIVE_COVERAGE_PRUNING_CONTRACT", "coverage-pruning", coverage_pruning_material
        ),
        deterministic_parameters_ref_or_typed_absence=_derived_ref(
            "PRE553_RECURSIVE_DETERMINISTIC_PARAMETERS", "deterministic-parameters", deterministic_parameters
        ),
        rng_state_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        parent_branch_ref_or_typed_absence=immediate_parent.ref,
        winning_predicate_ref_or_typed_absence=winning_predicate.ref,
        pruned_trace_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
    )
    return RecursiveBranchHandoff(
        receipt_ref=receipt.ref,
        branch_replay_binding=binding,
        winning_predicate=winning_predicate,
        source_release_refs=release_refs,
        discovery_authority_ref=discovery_authority.ref,
        evaluated_frontier_ref=discovery_result.evaluated_frontier_ref,
        candidate_universe_definition=canonicalize(definition),
        scope_context=scope_context,
        coverage_pruning_material=coverage_pruning_material,
        deterministic_parameters=deterministic_parameters,
    )


def execute_exact_bounded_discovery_with_handoffs(
    *,
    repository: C11Repository,
    discovery_authority: DiscoveryAuthority,
    authority_registry: AuthorityRegistry,
    release_refs: Iterable[ExactRef | Mapping[str, Any]],
    predicate_catalog: Iterable[EmpiricalPredicate],
    query_template_catalog: Iterable[EmpiricalQuerySpec],
) -> RecursiveHandoffDiscoveryResult:
    releases = _canonical_refs(release_refs)
    predicates = tuple(predicate_catalog)
    queries = tuple(query_template_catalog)
    result = execute_exact_bounded_discovery(
        repository=repository,
        discovery_authority=discovery_authority,
        authority_registry=authority_registry,
        release_refs=releases,
        predicate_catalog=predicates,
        query_template_catalog=queries,
    )
    definition = _mapping(discovery_authority.candidate_universe_definition, "candidate_universe_definition")
    grammar_ref = exact_ref(discovery_authority.candidate_grammar_ref)
    if grammar_ref != result.candidate_grammar_ref or grammar_ref.content_hash != semantic_hash(definition):
        raise RecursiveHandoffError("executed discovery grammar identity mismatch")
    handoffs: list[RecursiveBranchHandoff] = []
    for receipt in result.receipts:
        identity = _mapping(receipt.candidate_identity, "candidate_identity")
        family = _text(identity.get("family"), "candidate family")
        if family not in RECURSIVE_BRANCH_FAMILIES or receipt.typed_state != "DISCOVERED_RESULT_SUPPORTED":
            continue
        winner, parent = _resolve_receipt_winner(receipt, definition, predicates)
        handoffs.append(_make_handoff(
            winning_predicate=winner,
            immediate_parent=parent,
            receipt=receipt,
            discovery_authority=discovery_authority,
            discovery_result=result,
            release_refs=releases,
            definition=definition,
        ))
    return RecursiveHandoffDiscoveryResult(
        discovery_result=result,
        handoffs=tuple(sorted(handoffs, key=lambda handoff: handoff.ref.key)),
    )


def recursive_parent_atom(handoff: RecursiveBranchHandoff, atom_id: str) -> Mapping[str, Any]:
    """Exact public N+1 grammar atom for a persisted discovered branch."""
    return canonicalize({
        "atom_id": _text(atom_id, "recursive parent atom_id"),
        "predicate_ref": handoff.winning_predicate.ref,
        "kind": "BRANCH",
        "ancestry_refs": (handoff.ref,),
    })


def replay_recursive_branch_membership(
    *,
    repository: C11Repository,
    handoff: RecursiveBranchHandoff,
    authority_registry: AuthorityRegistry,
    release_refs: Iterable[ExactRef | Mapping[str, Any]] | None = None,
) -> tuple[ExactRef, ...]:
    """Replay the exact same-respondent cohort from persisted predicate/context."""
    validate_object_authority_closure(handoff.winning_predicate, authority_registry)
    requested = handoff.source_release_refs if release_refs is None else _canonical_refs(release_refs)
    if tuple(requested) != handoff.source_release_refs:
        raise RecursiveHandoffError("membership replay requires exact persisted source-release set")
    universe_refs = tuple(
        exact_ref(value)
        for value in handoff.winning_predicate.scope_refs
        if exact_ref(value).kind == "EmpiricalUniverse@1.0.0"
    )
    if not universe_refs:
        raise RecursiveHandoffError("winning predicate has no empirical-universe scope")
    members: dict[str, ExactRef] = {}
    for release_ref in requested:
        release = repository.resolve_release_exact(release_ref)
        available = {
            obj.ref.key for obj in release.public_objects if isinstance(obj, EmpiricalUniverse)
        }
        for universe_ref in universe_refs:
            if universe_ref.key not in available:
                continue
            index = _build_release_index(release, universe_ref)
            for respondent in index.respondents.values():
                used: list[Any] = []
                used_auth: list[AuthorityRef] = []
                if _eval_predicate(
                    handoff.winning_predicate.predicate_ast,
                    respondent=respondent,
                    index=index,
                    registry=authority_registry,
                    used=used,
                    used_auth=used_auth,
                ):
                    members[respondent.ref.key] = respondent.ref
    return tuple(sorted(members.values(), key=lambda ref: ref.key))


def write_recursive_handoff_bundle(
    path: str | Path, handoffs: Sequence[RecursiveBranchHandoff]
) -> ExactRef:
    """Persist exact semantic/replay side material; file bytes are not authority."""
    ordered = tuple(sorted(handoffs, key=lambda handoff: handoff.ref.key))
    if len({handoff.ref.key for handoff in ordered}) != len(ordered):
        raise RecursiveHandoffError("cannot persist duplicate handoff refs")
    payload = canonicalize({
        "contract_id": RECURSIVE_HANDOFF_CONTRACT_ID,
        "handoffs": [handoff.as_dict() for handoff in ordered],
    })
    bundle_ref = _derived_ref("PRE553_RECURSIVE_HANDOFF_BUNDLE", "handoff-bundle", payload)
    envelope = canonicalize({"bundle_ref": bundle_ref, "payload": payload})
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(canonical_json(envelope) + "\n", encoding="utf-8")
    return bundle_ref


def load_recursive_handoff_bundle(
    path: str | Path,
) -> tuple[ExactRef, tuple[RecursiveBranchHandoff, ...]]:
    """Fresh-process loader with exact hash/ref reconstruction."""
    envelope = json.loads(Path(path).read_text(encoding="utf-8"))
    bundle_ref = exact_ref(envelope.get("bundle_ref"))
    payload = _mapping(envelope.get("payload"), "handoff bundle payload")
    if payload.get("contract_id") != RECURSIVE_HANDOFF_CONTRACT_ID:
        raise RecursiveHandoffError("handoff bundle contract mismatch")
    expected = _derived_ref("PRE553_RECURSIVE_HANDOFF_BUNDLE", "handoff-bundle", payload)
    if bundle_ref != expected:
        raise RecursiveHandoffError("handoff bundle exact ref/hash mismatch")
    restored: list[RecursiveBranchHandoff] = []
    for raw in _sequence(payload.get("handoffs", ()), "handoffs", allow_empty=True):
        item = _mapping(raw, "handoff entry")
        if item.get("contract_id") != RECURSIVE_HANDOFF_CONTRACT_ID:
            raise RecursiveHandoffError("handoff entry contract mismatch")
        handoff = RecursiveBranchHandoff(
            receipt_ref=exact_ref(item.get("receipt_ref")),
            branch_replay_binding=_restore_binding(_mapping(item.get("branch_replay_binding"), "branch replay binding")),
            winning_predicate=_restore_predicate(_mapping(item.get("winning_predicate"), "winning predicate")),
            source_release_refs=_canonical_refs(item.get("source_release_refs", ())),
            discovery_authority_ref=exact_ref(item.get("discovery_authority_ref")),
            evaluated_frontier_ref=exact_ref(item.get("evaluated_frontier_ref")),
            candidate_universe_definition=_mapping(item.get("candidate_universe_definition"), "candidate universe definition"),
            scope_context=_mapping(item.get("scope_context"), "scope context"),
            coverage_pruning_material=_mapping(item.get("coverage_pruning_material"), "coverage pruning material"),
            deterministic_parameters=_mapping(item.get("deterministic_parameters"), "deterministic parameters"),
        )
        if exact_ref(item.get("handoff_ref")) != handoff.ref:
            raise RecursiveHandoffError("handoff entry exact ref mismatch")
        restored.append(handoff)
    ordered = tuple(sorted(restored, key=lambda handoff: handoff.ref.key))
    if len({handoff.ref.key for handoff in ordered}) != len(ordered):
        raise RecursiveHandoffError("loaded bundle contains duplicate handoff refs")
    return bundle_ref, ordered


__all__ = [
    "RECURSIVE_HANDOFF_CONTRACT_ID",
    "RecursiveHandoffError",
    "RecursiveBranchHandoff",
    "RecursiveHandoffDiscoveryResult",
    "execute_exact_bounded_discovery_with_handoffs",
    "recursive_parent_atom",
    "replay_recursive_branch_membership",
    "write_recursive_handoff_bundle",
    "load_recursive_handoff_bundle",
]
