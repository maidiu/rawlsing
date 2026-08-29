"""Authority-37 deterministic fracture-map result -> next-frontier controller.

I05 remains unchanged and exact-bounded. Result-driven generation is permitted
only between complete I05 invocations.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Iterable, Mapping, Protocol, Sequence

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_discovery_exact import (
    CANDIDATE_GRAMMAR_SCHEMA,
    ExactBoundedDiscoveryResult,
    _combine_predicates as _i05_combine_predicates,
    execute_exact_bounded_discovery,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    DiscoveryAuthority,
    EmpiricalCoordinateFact,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    make_empirical_predicate,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_fracture_map_contract import (
    EmpiricalFractureMapReceipt,
    FractureMapContinuationDecision,
    FractureMapControllerPolicy,
)
from rawlsing_next.pre553_recursive_handoff import (
    RecursiveBranchHandoff,
    RecursiveHandoffDiscoveryResult,
    execute_exact_bounded_discovery_with_handoffs,
    recursive_parent_atom,
)

CONTROLLER_CONTRACT_ID = "PRE553_AUTH37_FRACTURE_MAP_CONTROLLER@1.0.0"
AUTH37_POLICY_ID = "AUTHORITY37_CONTROLLER_POLICY_V1"


class FractureMapControllerError(Pre553IntegrityError):
    pass


# I01 owns the exact controller-policy identity.  The I02-local policy class is
# intentionally retired at integration rather than becoming a second authority.
ControllerPolicy = FractureMapControllerPolicy
Authority37ControllerPolicy = FractureMapControllerPolicy


class DiscoveryAuthorityBinder(Protocol):
    def bind(self, frontier: "SealedFrontier") -> DiscoveryAuthority: ...


class ControllerReceiptSink(Protocol):
    def record(self, envelope: "OperationalRefEnvelope") -> None: ...


@dataclass(frozen=True)
class ResponseCellSupport:
    cell: Any
    raw_support: int
    weighted_support_if_authorized: Fraction | None
    substantive: bool


@dataclass(frozen=True)
class ResponseMorphology:
    fact_ref: ExactRef
    support_basis: str
    cells: tuple[ResponseCellSupport, ...]
    substantive_cells: tuple[Any, ...]
    modal_cells: tuple[Any, ...]
    unresolved_maximal_tie: bool
    presence_support: Mapping[str, Any]

    @property
    def unique_modal_cell(self) -> Any | None:
        return self.modal_cells[0] if len(self.modal_cells) == 1 else None


@dataclass(frozen=True)
class CoordinateCondition:
    coordinate_ref: ExactRef
    exact_value: str
    atom_id: str
    condition_predicate: EmpiricalPredicate
    resolved_coordinate_predicate: EmpiricalPredicate
    coordinate_fact_refs: tuple[ExactRef, ...]


@dataclass(frozen=True)
class BranchRole:
    role: str
    predicate: EmpiricalPredicate


@dataclass(frozen=True)
class SealedFrontier:
    generation_kind: str
    parent_predicate: EmpiricalPredicate
    query_template: EmpiricalQuerySpec
    candidate_universe_definition: Mapping[str, Any]
    candidate_grammar_ref: ExactRef
    predicate_catalog: tuple[EmpiricalPredicate, ...]
    query_template_catalog: tuple[EmpiricalQuerySpec, ...]
    coordinate_conditions: tuple[CoordinateCondition, ...] = ()
    branch_roles: tuple[BranchRole, ...] = ()

    def assert_sealed(self) -> None:
        if self.candidate_grammar_ref.content_hash != semantic_hash(self.candidate_universe_definition):
            raise FractureMapControllerError("sealed frontier mutated")


@dataclass(frozen=True)
class OperationalRefEnvelope:
    controller_policy_id: str
    controller_policy_ref: ExactRef
    controller_policy_authority_ref: AuthorityRef
    root_query_ref: ExactRef
    parent_predicate_ref: ExactRef
    source_release_refs: tuple[ExactRef, ...]
    candidate_grammar_ref: ExactRef
    evaluated_frontier_ref: ExactRef
    discovery_authority_ref: ExactRef
    receipt_refs: tuple[ExactRef, ...]
    empirical_fact_refs: tuple[ExactRef, ...]
    handoff_refs: tuple[ExactRef, ...]
    depth: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "controller_policy_ref", exact_ref(self.controller_policy_ref))
        object.__setattr__(
            self, "controller_policy_authority_ref",
            authority_ref(self.controller_policy_authority_ref),
        )
        for name in (
            "root_query_ref", "parent_predicate_ref", "candidate_grammar_ref",
            "evaluated_frontier_ref", "discovery_authority_ref",
        ):
            object.__setattr__(self, name, exact_ref(getattr(self, name)))
        for name in ("source_release_refs", "receipt_refs", "empirical_fact_refs", "handoff_refs"):
            object.__setattr__(self, name, _refs(exact_ref(ref) for ref in getattr(self, name)))

    def as_dict(self) -> Mapping[str, Any]:
        return canonicalize({
            "contract_id": CONTROLLER_CONTRACT_ID,
            "controller_policy_id": self.controller_policy_id,
            "controller_policy_ref": self.controller_policy_ref,
            "controller_policy_authority_ref": self.controller_policy_authority_ref,
            "root_query_ref": self.root_query_ref,
            "parent_predicate_ref": self.parent_predicate_ref,
            "source_release_refs": self.source_release_refs,
            "candidate_grammar_ref": self.candidate_grammar_ref,
            "evaluated_frontier_ref": self.evaluated_frontier_ref,
            "discovery_authority_ref": self.discovery_authority_ref,
            "receipt_refs": self.receipt_refs,
            "empirical_fact_refs": self.empirical_fact_refs,
            "handoff_refs": self.handoff_refs,
            "depth": self.depth,
        })


class FractureMapReceiptAccumulator:
    """Wire I02 operational envelopes into I01's public ref-only receipt."""

    def __init__(self, *, policy: FractureMapControllerPolicy) -> None:
        if not isinstance(policy, FractureMapControllerPolicy):
            raise FractureMapControllerError("I01 FractureMapControllerPolicy is required")
        self.policy = policy
        self._envelopes: list[OperationalRefEnvelope] = []
        self._continuation_decisions: list[FractureMapContinuationDecision] = []
        self._cosignature_closure_refs: list[ExactRef] = []

    def record(self, envelope: OperationalRefEnvelope) -> None:
        if not isinstance(envelope, OperationalRefEnvelope):
            raise FractureMapControllerError("typed OperationalRefEnvelope required")
        if envelope.controller_policy_ref != self.policy.ref:
            raise FractureMapControllerError("operational envelope policy ref mismatch")
        if envelope.controller_policy_authority_ref != self.policy.policy_authority_ref:
            raise FractureMapControllerError("operational envelope policy authority mismatch")
        self._envelopes.append(envelope)

    def record_continuation(self, decision: FractureMapContinuationDecision) -> None:
        if decision.controller_policy_ref != self.policy.ref:
            raise FractureMapControllerError("continuation decision policy ref mismatch")
        if decision.controller_policy_authority_ref != self.policy.policy_authority_ref:
            raise FractureMapControllerError("continuation decision policy authority mismatch")
        self._continuation_decisions.append(decision)

    def record_cosignature_closure(self, closure_ref: ExactRef | Mapping[str, Any]) -> None:
        self._cosignature_closure_refs.append(exact_ref(closure_ref))

    def seal(
        self,
        *,
        root_query_ref: ExactRef | Mapping[str, Any],
        branch_predicate_refs: Iterable[ExactRef | Mapping[str, Any]],
        branch_ancestry_refs: Iterable[ExactRef | Mapping[str, Any]],
        final_replay_ref: ExactRef | Mapping[str, Any],
        closure_state: str = "FRACTURE_MAP_CLOSURE_COMPLETE",
        additional_authority_snapshot_refs: Iterable[AuthorityRef | Mapping[str, Any]] = (),
    ) -> EmpiricalFractureMapReceipt:
        if not self._envelopes:
            raise FractureMapControllerError("cannot seal fracture-map receipt without I02 execution envelopes")
        root = exact_ref(root_query_ref)
        replay = exact_ref(final_replay_ref)
        ordered = tuple(sorted(
            self._envelopes,
            key=lambda env: (env.depth, env.candidate_grammar_ref.key, env.evaluated_frontier_ref.key),
        ))
        sources = _refs(ref for env in ordered for ref in env.source_release_refs)
        frontiers = tuple(env.candidate_grammar_ref for env in ordered)
        facts = _refs(ref for env in ordered for ref in env.empirical_fact_refs)
        discovery = _refs(ref for env in ordered for ref in env.receipt_refs)
        topology = _refs(self._cosignature_closure_refs)
        decisions = _refs(decision.ref for decision in self._continuation_decisions)
        branches = _refs((
            *(exact_ref(ref) for ref in branch_predicate_refs),
            *(env.parent_predicate_ref for env in ordered),
        ))
        ancestry = _refs(exact_ref(ref) for ref in branch_ancestry_refs)
        dependencies = _refs((
            root, *sources, self.policy.ref, *branches, *ancestry, *frontiers,
            *facts, *discovery, *topology, *decisions, replay,
        ))
        authorities = _auths((
            self.policy.policy_authority_ref,
            *(authority_ref(ref) for ref in additional_authority_snapshot_refs),
        ))
        return EmpiricalFractureMapReceipt(
            typed_state=closure_state,
            authority_snapshot_refs=authorities,
            dependency_refs=dependencies,
            producer_replay_locator_or_reference_root=replay,
            root_query_ref=root,
            source_release_refs=sources,
            controller_policy_ref=self.policy.ref,
            controller_policy_authority_ref=self.policy.policy_authority_ref,
            branch_predicate_refs=branches,
            branch_ancestry_refs=ancestry,
            generation_frontier_refs=frontiers,
            empirical_fact_refs=facts,
            discovery_result_receipt_refs=discovery,
            branch_cosignature_topology_closure_refs=topology,
            continuation_decision_refs=decisions,
            final_replay_ref=replay,
            closure_state=closure_state,
            copied_empirical_payload=False,
            pre_v3_actor_independent=True,
            requires_separate_semantic_transformation_authority=True,
            requires_separate_structural_admission_authority=True,
            requires_separate_actor_binding_authority=True,
            requires_explicit_v3_metabolism_authority=True,
            actor_state_effect=False,
            v3_state_effect=False,
            v2_state_effect=False,
            persona_effect=False,
            belief_effect=False,
            response_effect=False,
        )


def _derived_ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:pre553:fracture-controller:{namespace}:sha256:{digest}", digest)


def _refs(values: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    return tuple(sorted(set(values), key=lambda ref: ref.key))


def _auths(values: Iterable[AuthorityRef]) -> tuple[AuthorityRef, ...]:
    return tuple(sorted(set(values), key=lambda ref: ref.key))


def _fraction(value: Any) -> Fraction:
    if isinstance(value, Mapping) and "$exact_fraction" in value:
        n, d = value["$exact_fraction"]
        return Fraction(int(n), int(d))
    if isinstance(value, int) and not isinstance(value, bool):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    raise FractureMapControllerError("weighted support is not exact")


def _response_component_semantics(query: EmpiricalQuerySpec) -> Mapping[str, Any]:
    if int(query.target_arity_and_topology.get("arity", 0)) != 1:
        raise FractureMapControllerError("I02 is unary focal-surface composition only")
    raw = query.target_arity_and_topology.get("components", ())
    if isinstance(raw, (str, bytes, bytearray)) or not isinstance(raw, Sequence) or len(raw) != 1:
        raise FractureMapControllerError("exact unary target component required")
    component = raw[0]
    if not isinstance(component, Mapping):
        raise FractureMapControllerError("target component semantics must be an exact mapping")
    return component


def _is_substantive_response_cell(query: EmpiricalQuerySpec, cell: Any) -> bool:
    component = _response_component_semantics(query)
    raw = component.get("non_substantive_domain", ())
    if isinstance(raw, (str, bytes, bytearray)) or not isinstance(raw, Sequence):
        raise FractureMapControllerError("non_substantive_domain must be an exact sequence")
    non_substantive = {canonical_json(value) for value in raw}
    return canonical_json(cell) not in non_substantive


def _presence_labels_for_cell(query: EmpiricalQuerySpec, cell: Any) -> tuple[str, ...]:
    component = _response_component_semantics(query)
    raw = component.get("presence_labels_by_cell")
    topology = str(component.get("topology", ""))
    multiselect = topology in {"UNORDERED_MULTISELECT_SET", "MULTISELECT"}
    if raw is None:
        if multiselect:
            raise FractureMapControllerError(
                "multi-select fracture morphology requires exact source-governed presence labels"
            )
        return ()
    if not isinstance(raw, Mapping):
        raise FractureMapControllerError("presence_labels_by_cell must be an exact mapping")
    labels = raw.get(canonical_json(cell), ())
    if isinstance(labels, (str, bytes, bytearray)) or not isinstance(labels, Sequence):
        raise FractureMapControllerError("presence label material must be an exact sequence")
    return tuple(sorted({str(label) for label in labels}))


def derive_response_morphology(
    fact: EmpiricalFact,
    query: EmpiricalQuerySpec,
    policy: ControllerPolicy,
) -> ResponseMorphology:
    if int(query.target_arity_and_topology.get("arity", 0)) != 1:
        raise FractureMapControllerError("I02 is unary focal-surface composition only")
    basis = fact.semantic_fields.get("measure_kind", query.requested_output_grain.get("measure_kind", "RAW"))
    if basis not in {"RAW", "GOVERNED_WEIGHTED"}:
        raise FractureMapControllerError("unresolved modal measure")
    rows = tuple(fact.target_topology.get("complete_cell_semantic_projection", ()))
    cells = []
    presence: dict[str, Fraction] = {}
    for row in rows:
        cell = canonicalize(row.get("cell"))
        raw = int(row.get("raw_numerator_support", 0))
        weighted_value = row.get("weighted_numerator_support_if_authorized")
        weighted = _fraction(weighted_value) if weighted_value is not None else None
        substantive = _is_substantive_response_cell(query, cell)
        cells.append(ResponseCellSupport(cell, raw, weighted, substantive))
        if substantive:
            amount = weighted if basis == "GOVERNED_WEIGHTED" else Fraction(raw, 1)
            if amount is None:
                raise FractureMapControllerError("weighted modal support unavailable")
            for label in _presence_labels_for_cell(query, cell):
                presence[label] = presence.get(label, Fraction(0, 1)) + amount
    substantive = tuple(c for c in cells if c.substantive)
    if not substantive:
        modal = ()
    else:
        supports = tuple(
            c.weighted_support_if_authorized if basis == "GOVERNED_WEIGHTED" else Fraction(c.raw_support, 1)
            for c in substantive
        )
        if any(v is None for v in supports):
            raise FractureMapControllerError("weighted modal support unavailable")
        top = max(supports)
        modal = tuple(c.cell for c, value in zip(substantive, supports) if value == top)
    return ResponseMorphology(
        fact_ref=fact.ref,
        support_basis=basis,
        cells=tuple(cells),
        substantive_cells=tuple(c.cell for c in substantive),
        modal_cells=modal,
        unresolved_maximal_tie=len(modal) > 1,
        presence_support=canonicalize(presence),
    )


def _compose(predicates: Sequence[EmpiricalPredicate], op: str, tag: str, material: Any) -> EmpiricalPredicate:
    if not predicates or op not in {"AND", "OR"}:
        raise FractureMapControllerError("invalid predicate composition")
    if len({canonical_json(p.grammar_authority_ref) for p in predicates}) != 1:
        raise FractureMapControllerError("predicate grammar mismatch")
    if len({p.same_respondent_binding_semantics for p in predicates}) != 1:
        raise FractureMapControllerError("respondent-binding mismatch")
    return make_empirical_predicate(
        predicate_ast={"op": op, "children": [p.predicate_ast for p in predicates]},
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=_auths(ref for p in predicates for ref in p.authority_snapshot_refs),
        dependency_refs=_refs(p.ref for p in predicates),
        producer_replay_locator_or_reference_root=_derived_ref("PRE553_FRACTURE_CONTROLLER_PREDICATE_REPLAY", tag, material),
        grammar_authority_ref=predicates[0].grammar_authority_ref,
        coordinate_question_value_refs=_refs(exact_ref(ref) for p in predicates for ref in p.coordinate_question_value_refs),
        risk_set_refs=_refs(exact_ref(ref) for p in predicates for ref in p.risk_set_refs),
        scope_refs=_refs(exact_ref(ref) for p in predicates for ref in p.scope_refs),
        same_respondent_binding_semantics=predicates[0].same_respondent_binding_semantics,
        operator_semantics_refs=_refs(exact_ref(ref) for p in predicates for ref in p.operator_semantics_refs),
    )


def _not(predicate: EmpiricalPredicate, material: Any) -> EmpiricalPredicate:
    return make_empirical_predicate(
        predicate_ast={"op": "NOT", "children": [predicate.predicate_ast]},
        typed_state=predicate.typed_state,
        authority_snapshot_refs=predicate.authority_snapshot_refs,
        dependency_refs=(predicate.ref,),
        producer_replay_locator_or_reference_root=_derived_ref("PRE553_FRACTURE_CONTROLLER_PREDICATE_REPLAY", "not", material),
        grammar_authority_ref=predicate.grammar_authority_ref,
        coordinate_question_value_refs=predicate.coordinate_question_value_refs,
        risk_set_refs=predicate.risk_set_refs,
        scope_refs=predicate.scope_refs,
        same_respondent_binding_semantics=predicate.same_respondent_binding_semantics,
        operator_semantics_refs=predicate.operator_semantics_refs,
    )


def _coordinate_predicate(
    root_predicate: EmpiricalPredicate,
    root_query: EmpiricalQuerySpec,
    coordinate_ref: ExactRef,
    value: str,
    coord_authority: AuthorityRef,
    fact_refs: Sequence[ExactRef],
) -> EmpiricalPredicate:
    value_ref = _derived_ref("PRE553_COORDINATE_VALUE", "value", {"coordinate_ref": coordinate_ref, "value": value})
    return make_empirical_predicate(
        predicate_ast={
            "op": "LEAF",
            "leaf_type": "EMPIRICAL_POSITION_COORDINATE",
            "coordinate_semantic_ref": coordinate_ref,
            "value_or_value_set_ref": value_ref,
            "comparison_operator_ref": _derived_ref("PRE553_COMPARISON_OPERATOR", "eq", {"operator": "EQ"}),
            "typed_state_policy_ref": _derived_ref("PRE553_TYPED_STATE_POLICY", "observed-only", {"state": "OBSERVED_COORDINATE"}),
            "coordinate_authority_ref": coord_authority,
            "operator": "EQ",
            "exact_value": value,
        },
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=_auths((*root_predicate.authority_snapshot_refs, coord_authority)),
        dependency_refs=_refs(fact_refs),
        producer_replay_locator_or_reference_root=_derived_ref(
            "PRE553_FRACTURE_CONTROLLER_PREDICATE_REPLAY",
            "coordinate",
            {"coordinate_ref": coordinate_ref, "value": value, "facts": tuple(fact_refs)},
        ),
        grammar_authority_ref=root_predicate.grammar_authority_ref,
        coordinate_question_value_refs=_refs((coordinate_ref, value_ref)),
        risk_set_refs=_refs((*tuple(exact_ref(x) for x in root_predicate.risk_set_refs), exact_ref(root_query.risk_set_ref))),
        scope_refs=_refs(exact_ref(x) for x in root_query.empirical_universe_refs),
        same_respondent_binding_semantics=root_predicate.same_respondent_binding_semantics,
        operator_semantics_refs=root_predicate.operator_semantics_refs,
    )


def enumerate_coordinate_conditions(
    *,
    repository: C11Repository,
    root_query: EmpiricalQuerySpec,
    root_predicate: EmpiricalPredicate,
    release_refs: Iterable[ExactRef],
    coordinate_authority_refs: Iterable[AuthorityRef],
) -> tuple[CoordinateCondition, ...]:
    allowed_auth = {authority_ref(ref).key for ref in coordinate_authority_refs}
    allowed_universes = {exact_ref(ref).key for ref in root_query.empirical_universe_refs}
    grouped: dict[tuple[str, str], list[EmpiricalCoordinateFact]] = {}
    refs_by_key: dict[str, ExactRef] = {}
    auth_by_key: dict[str, AuthorityRef] = {}
    for release_ref in _refs(release_refs):
        release = repository.resolve_release_exact(release_ref)
        for obj in release.public_objects:
            if not isinstance(obj, EmpiricalCoordinateFact) or obj.typed_state != "OBSERVED_COORDINATE":
                continue
            if exact_ref(obj.empirical_universe_ref).key not in allowed_universes:
                continue
            auth = authority_ref(obj.source_semantic_authority_ref)
            if auth.key not in allowed_auth:
                continue
            coord_value = obj.canonical_coordinate_ref_if_authorized
            coord = exact_ref(coord_value if coord_value is not None else obj.native_coordinate_ref)
            raw_value = obj.canonical_coordinate_value_if_authorized
            value = str(raw_value if raw_value is not None else obj.raw_coordinate_value)
            grouped.setdefault((coord.key, value), []).append(obj)
            refs_by_key[coord.key] = coord
            auth_by_key[coord.key] = auth
    by_coord: dict[str, list[str]] = {}
    for coord_key, value in grouped:
        by_coord.setdefault(coord_key, []).append(value)
    result = []
    for coord_key in sorted(by_coord):
        coord = refs_by_key[coord_key]
        auth = auth_by_key[coord_key]
        values = sorted(set(by_coord[coord_key]))
        value_preds = {}
        for value in values:
            facts = grouped[(coord_key, value)]
            value_preds[value] = _coordinate_predicate(root_predicate, root_query, coord, value, auth, [f.ref for f in facts])
        resolved = value_preds[values[0]] if len(values) == 1 else _compose(
            tuple(value_preds[v] for v in values),
            "OR",
            "coordinate-resolved",
            {"coordinate_ref": coord, "values": values},
        )
        for value in values:
            token = semantic_hash({"coordinate_ref": coord, "value": value})
            result.append(CoordinateCondition(
                coordinate_ref=coord,
                exact_value=value,
                atom_id=f"COORD_{token[:20]}",
                condition_predicate=value_preds[value],
                resolved_coordinate_predicate=resolved,
                coordinate_fact_refs=_refs(f.ref for f in grouped[(coord_key, value)]),
            ))
    return tuple(sorted(result, key=lambda c: (c.coordinate_ref.key, c.exact_value, c.atom_id)))


def _response_predicate(parent: EmpiricalPredicate, query: EmpiricalQuerySpec, cell: Any) -> EmpiricalPredicate:
    components = tuple(query.target_arity_and_topology.get("components", ()))
    if len(query.target_refs) != 1 or len(components) != 1:
        raise FractureMapControllerError("I02 branch roles require one focal response component")
    component = components[0]
    topology_auths = tuple(authority_ref(x) for x in component.get("topology_authority_refs", ()))
    response_auths = tuple(authority_ref(x) for x in component.get("response_semantic_authority_refs", ()))
    if not topology_auths or not response_auths:
        raise FractureMapControllerError("response authority missing")
    value_ref = _derived_ref("PRE553_RESPONSE_VALUE", "cell", {"target": query.target_refs[0], "cell": cell})
    return make_empirical_predicate(
        predicate_ast={
            "op": "LEAF",
            "leaf_type": "SURVEY_RESPONSE_EVENT",
            "question_semantic_ref": query.target_refs[0],
            "component_or_event_selector_ref": _derived_ref("PRE553_EVENT_SELECTOR", "any", {"target": query.target_refs[0]}),
            "response_value_or_state_ref": value_ref,
            "response_topology_authority_ref": topology_auths[0],
            "response_semantic_authority_ref": response_auths[0],
            "operator": "EQ",
            "exact_value": str(cell),
        },
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=_auths((*parent.authority_snapshot_refs, *topology_auths, *response_auths)),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_derived_ref("PRE553_FRACTURE_CONTROLLER_PREDICATE_REPLAY", "response-cell", {"cell": cell}),
        grammar_authority_ref=parent.grammar_authority_ref,
        coordinate_question_value_refs=(value_ref,),
        risk_set_refs=_refs((*tuple(exact_ref(x) for x in parent.risk_set_refs), exact_ref(query.risk_set_ref))),
        scope_refs=_refs(exact_ref(x) for x in query.empirical_universe_refs),
        same_respondent_binding_semantics=parent.same_respondent_binding_semantics,
        operator_semantics_refs=parent.operator_semantics_refs,
    )


def construct_four_way_branches(
    *,
    parent_predicate: EmpiricalPredicate,
    root_query: EmpiricalQuerySpec,
    morphology: ResponseMorphology,
    predictor: CoordinateCondition,
) -> tuple[BranchRole, ...]:
    modal = morphology.unique_modal_cell
    if modal is None:
        return ()
    nonmodal = tuple(cell for cell in morphology.substantive_cells if canonical_json(cell) != canonical_json(modal))
    m = _response_predicate(parent_predicate, root_query, modal)
    nm = None
    if nonmodal:
        parts = tuple(_response_predicate(parent_predicate, root_query, cell) for cell in nonmodal)
        nm = parts[0] if len(parts) == 1 else _compose(parts, "OR", "substantive-nonmodal", {"cells": nonmodal})
    not_p = _not(predictor.condition_predicate, {"predictor": predictor.atom_id})
    present = _compose(
        (predictor.resolved_coordinate_predicate, predictor.condition_predicate),
        "AND", "present-resolved", {"predictor": predictor.atom_id},
    )
    absent = _compose(
        (predictor.resolved_coordinate_predicate, not_p),
        "AND", "absent-resolved", {"predictor": predictor.atom_id},
    )
    roles = [
        BranchRole("CONFORMER", _compose((parent_predicate, present, m), "AND", "conformer", {"predictor": predictor.atom_id, "m": modal})),
        BranchRole("ALT_CONVERGER", _compose((parent_predicate, absent, m), "AND", "alt-converger", {"predictor": predictor.atom_id, "m": modal})),
    ]
    if nm is not None:
        roles.extend([
            BranchRole("DEVIANT_EXIT", _compose((parent_predicate, present, nm), "AND", "deviant", {"predictor": predictor.atom_id, "nm": nonmodal})),
            BranchRole("ALT_MINORITY", _compose((parent_predicate, absent, nm), "AND", "alt-minority", {"predictor": predictor.atom_id, "nm": nonmodal})),
        ])
    return tuple(sorted(roles, key=lambda role: role.role))


def _grammar_ref(grammar: Mapping[str, Any]) -> ExactRef:
    digest = semantic_hash(grammar)
    return ExactRef("PRE553_I05_CANDIDATE_GRAMMAR", f"urn:rawlsing:pre553:fracture-controller:grammar:sha256:{digest}", digest)


def _predicate_catalog(predicates: Iterable[EmpiricalPredicate]) -> tuple[EmpiricalPredicate, ...]:
    by_ref = {p.ref.key: p for p in predicates}
    return tuple(by_ref[key] for key in sorted(by_ref))


class FractureMapController:
    def __init__(self, *, policy: FractureMapControllerPolicy, receipt_sink: ControllerReceiptSink | None = None) -> None:
        if not isinstance(policy, FractureMapControllerPolicy):
            raise FractureMapControllerError("I01 FractureMapControllerPolicy is the exact controller policy owner")
        self.policy = policy
        self.receipt_sink = receipt_sink
        self._open_frontier_ref: ExactRef | None = None

    def _between_invocations(self) -> None:
        if self._open_frontier_ref is not None:
            raise FractureMapControllerError("cannot generate/mutate frontier during an open I05 invocation")

    def root_morphology(
        self,
        *,
        repository: C11Repository,
        root_query: EmpiricalQuerySpec,
        root_predicate: EmpiricalPredicate,
        authority_registry: AuthorityRegistry,
        release_refs: Iterable[ExactRef],
    ) -> ResponseMorphology:
        self._between_invocations()
        result = execute_empirical_query(
            repository=repository,
            query=root_query,
            predicate=root_predicate,
            authority_registry=authority_registry,
            release_refs=_refs(release_refs),
        )
        if len(result.facts) != 1:
            raise FractureMapControllerError("modal selection refuses implicit pooling across multiple fact scopes")
        return derive_response_morphology(result.facts[0], root_query, self.policy)

    def coordinate_catalog(self, **kwargs: Any) -> tuple[CoordinateCondition, ...]:
        self._between_invocations()
        return enumerate_coordinate_conditions(**kwargs)

    def seal_predictor_frontier(
        self,
        *,
        parent_predicate: EmpiricalPredicate,
        root_query: EmpiricalQuerySpec,
        coordinate_conditions: Sequence[CoordinateCondition],
        depth: int,
        ancestry_refs: Iterable[ExactRef] = (),
    ) -> SealedFrontier:
        self._between_invocations()
        coordinate_conditions = tuple(sorted(
            coordinate_conditions,
            key=lambda item: (item.coordinate_ref.key, item.exact_value, item.atom_id),
        ))
        atoms = [{
            "atom_id": "PARENT",
            "predicate_ref": parent_predicate.ref,
            "kind": "BRANCH",
            "ancestry_refs": tuple(ancestry_refs),
        }]
        atoms.extend({
            "atom_id": c.atom_id,
            "predicate_ref": c.condition_predicate.ref,
            "kind": "COORDINATE",
            "ancestry_refs": (),
        } for c in coordinate_conditions)
        ids = tuple(c.atom_id for c in coordinate_conditions)
        rules = () if not ids else ({
            "rule_id": "AUTH37_ATOMIC_POSITIONAL_V1",
            "family": "RESPONSE_X_EMPIRICAL_COORDINATE",
            "form": "SINGLE_ATOM",
            "atom_ids": ids,
            "baseline_atom_id": "PARENT",
            "query_template_id": "FOCAL",
            "validation": {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        },)
        grammar = canonicalize({
            "schema": CANDIDATE_GRAMMAR_SCHEMA,
            "discovery_operation": f"AUTH37-FRACTURE-PREDICTOR-GEN-{depth}",
            "atoms": tuple(atoms),
            "query_templates": ({"template_id": "FOCAL", "query_ref": root_query.ref},),
            "rules": rules,
            "limits": {"maximum_conditioner_arity_K": 1, "maximum_target_arity_J": int(root_query.target_arity_and_topology.get("arity", 1))},
            "allow_empty_frontier": not bool(ids),
            "controller_policy_id": self.policy.policy_id,
            "controller_policy_version": self.policy.policy_version,
            "controller_policy_ref": self.policy.ref,
            "controller_policy_authority_ref": self.policy.policy_authority_ref,
        })
        frontier = SealedFrontier(
            generation_kind="POSITIONAL_PREDICTOR",
            parent_predicate=parent_predicate,
            query_template=root_query,
            candidate_universe_definition=grammar,
            candidate_grammar_ref=_grammar_ref(grammar),
            predicate_catalog=_predicate_catalog([parent_predicate, *(c.condition_predicate for c in coordinate_conditions)]),
            query_template_catalog=(root_query,),
            coordinate_conditions=tuple(coordinate_conditions),
        )
        frontier.assert_sealed()
        return frontier

    def seal_branch_frontier(
        self,
        *,
        parent_predicate: EmpiricalPredicate,
        root_query: EmpiricalQuerySpec,
        branch_roles: Sequence[BranchRole],
        depth: int,
        ancestry_refs: Iterable[ExactRef] = (),
    ) -> SealedFrontier:
        self._between_invocations()
        branch_roles = tuple(sorted(branch_roles, key=lambda item: item.role))
        atoms = [{
            "atom_id": "PARENT",
            "predicate_ref": parent_predicate.ref,
            "kind": "BRANCH",
            "ancestry_refs": tuple(ancestry_refs),
        }]
        atoms.extend({
            "atom_id": f"ROLE_{r.role}",
            "predicate_ref": r.predicate.ref,
            "kind": "BRANCH",
            "ancestry_refs": tuple(ancestry_refs),
        } for r in branch_roles)
        ids = tuple(f"ROLE_{r.role}" for r in branch_roles)
        rules = () if not ids else ({
            "rule_id": "AUTH37_BRANCH_REALIZATION_V1",
            "family": "RECURSIVE_SUBGROUP_FORK",
            "form": "SINGLE_ATOM",
            "atom_ids": ids,
            "baseline_atom_id": "PARENT",
            "query_template_id": "FOCAL",
            "validation": {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        },)
        grammar = canonicalize({
            "schema": CANDIDATE_GRAMMAR_SCHEMA,
            "discovery_operation": f"AUTH37-FRACTURE-BRANCH-GEN-{depth}",
            "atoms": tuple(atoms),
            "query_templates": ({"template_id": "FOCAL", "query_ref": root_query.ref},),
            "rules": rules,
            "limits": {"maximum_conditioner_arity_K": 1, "maximum_target_arity_J": int(root_query.target_arity_and_topology.get("arity", 1))},
            "allow_empty_frontier": not bool(ids),
            "controller_policy_id": self.policy.policy_id,
        })
        frontier = SealedFrontier(
            generation_kind="BRANCH_REALIZATION",
            parent_predicate=parent_predicate,
            query_template=root_query,
            candidate_universe_definition=grammar,
            candidate_grammar_ref=_grammar_ref(grammar),
            predicate_catalog=_predicate_catalog([parent_predicate, *(r.predicate for r in branch_roles)]),
            query_template_catalog=(root_query,),
            branch_roles=tuple(branch_roles),
        )
        frontier.assert_sealed()
        return frontier

    def execute_frontier(
        self,
        *,
        repository: C11Repository,
        frontier: SealedFrontier,
        binder: DiscoveryAuthorityBinder,
        authority_registry: AuthorityRegistry,
        release_refs: Iterable[ExactRef],
        depth: int,
        recursive_handoffs: bool = False,
    ) -> ExactBoundedDiscoveryResult | RecursiveHandoffDiscoveryResult:
        self._between_invocations()
        frontier.assert_sealed()
        self._open_frontier_ref = frontier.candidate_grammar_ref
        try:
            authority = binder.bind(frontier)
            if exact_ref(authority.candidate_grammar_ref) != frontier.candidate_grammar_ref:
                raise FractureMapControllerError("binder changed sealed grammar")
            if semantic_hash(authority.candidate_universe_definition) != frontier.candidate_grammar_ref.content_hash:
                raise FractureMapControllerError("binder changed sealed grammar content")
            if recursive_handoffs:
                result = execute_exact_bounded_discovery_with_handoffs(
                    repository=repository,
                    discovery_authority=authority,
                    authority_registry=authority_registry,
                    release_refs=_refs(release_refs),
                    predicate_catalog=frontier.predicate_catalog,
                    query_template_catalog=frontier.query_template_catalog,
                )
                base = result.discovery_result
                handoffs = tuple(h.ref for h in result.handoffs)
            else:
                result = execute_exact_bounded_discovery(
                    repository=repository,
                    discovery_authority=authority,
                    authority_registry=authority_registry,
                    release_refs=_refs(release_refs),
                    predicate_catalog=frontier.predicate_catalog,
                    query_template_catalog=frontier.query_template_catalog,
                )
                base = result
                handoffs = ()
            frontier.assert_sealed()
            if self.receipt_sink is not None:
                empirical_fact_refs = _refs(
                    exact_ref(ref)
                    for receipt in base.receipts
                    for ref in receipt.empirical_fact_refs
                )
                self.receipt_sink.record(OperationalRefEnvelope(
                    controller_policy_id=self.policy.policy_id,
                    controller_policy_ref=self.policy.ref,
                    controller_policy_authority_ref=self.policy.policy_authority_ref,
                    root_query_ref=frontier.query_template.ref,
                    parent_predicate_ref=frontier.parent_predicate.ref,
                    source_release_refs=_refs(release_refs),
                    candidate_grammar_ref=frontier.candidate_grammar_ref,
                    evaluated_frontier_ref=base.evaluated_frontier_ref,
                    discovery_authority_ref=authority.ref,
                    receipt_refs=tuple(r.ref for r in base.receipts),
                    empirical_fact_refs=empirical_fact_refs,
                    handoff_refs=handoffs,
                    depth=depth,
                ))
            return result
        finally:
            self._open_frontier_ref = None

    def supported_predictor_conditions(
        self,
        *,
        result: ExactBoundedDiscoveryResult,
        frontier: SealedFrontier,
    ) -> tuple[CoordinateCondition, ...]:
        self._between_invocations()
        supported = {
            exact_ref(r.winning_predicate_ref).key
            for r in result.receipts
            if r.typed_state == "DISCOVERED_RESULT_SUPPORTED"
        }
        selected = []
        for c in frontier.coordinate_conditions:
            compiled = _i05_combine_predicates(
                (frontier.parent_predicate, c.condition_predicate),
                op="AND",
                tag_material={
                    "rule": "AUTH37_ATOMIC_POSITIONAL_V1",
                    "baseline": "PARENT",
                    "condition": c.condition_predicate.ref.as_dict(),
                },
            )
            if compiled.ref.key in supported:
                selected.append(c)
        return tuple(sorted(selected, key=lambda c: c.atom_id))

    def _continuation_terms(self, *, raw_n: int, depth: int, remaining_candidates: int) -> tuple[str, str, str]:
        if not isinstance(raw_n, int) or isinstance(raw_n, bool) or raw_n < 0:
            raise FractureMapControllerError("raw_n must be an exact nonnegative integer")
        if not isinstance(depth, int) or isinstance(depth, bool) or depth < 0:
            raise FractureMapControllerError("depth must be an exact nonnegative integer")
        if not isinstance(remaining_candidates, int) or isinstance(remaining_candidates, bool):
            raise FractureMapControllerError("remaining_candidates must be an exact integer")
        if depth >= self.policy.maximum_depth:
            return "RETAIN_EXACT_BRANCH", "RETAIN_TERMINAL_STOP", "MAX_DEPTH"
        if raw_n < self.policy.minimum_report_raw_n:
            return "RETAIN_LOW_SUPPORT_STATE", "RETAIN_REPORT_ONLY_STOP", "LOW_N_OR_INSUFFICIENT_SUPPORT"
        if raw_n < self.policy.minimum_split_raw_n:
            return "RETAIN_RESULT_WITH_LIMITATION", "RETAIN_REPORT_ONLY_STOP", "LOW_SUPPORT_OR_CONTROLLER_POLICY_ABSENT"
        if remaining_candidates <= 0:
            return "RETAIN_EXACT_BRANCH", "RETAIN_TERMINAL_STOP", "NO_REMAINING_ELIGIBLE_PREDICTORS"
        return "RETAIN_EXACT_BRANCH", "RETAIN_AND_CONTINUE_ELIGIBLE", "NONE"

    def continuation_disposition(self, *, raw_n: int, depth: int, remaining_candidates: int) -> str:
        return self._continuation_terms(
            raw_n=raw_n, depth=depth, remaining_candidates=remaining_candidates
        )[1]

    def continuation_decision(
        self,
        *,
        branch_predicate: EmpiricalPredicate,
        producer_state_bindings: Iterable[tuple[ExactRef | Mapping[str, Any], str]],
        raw_n: int,
        depth: int,
        remaining_candidates: int,
    ) -> FractureMapContinuationDecision:
        retention, continuation, stop = self._continuation_terms(
            raw_n=raw_n, depth=depth, remaining_candidates=remaining_candidates
        )
        decision = FractureMapContinuationDecision(
            controller_policy_ref=self.policy.ref,
            controller_policy_authority_ref=self.policy.policy_authority_ref,
            branch_predicate_ref=branch_predicate.ref,
            producer_state_bindings=producer_state_bindings,
            retention_disposition=retention,
            continuation_disposition=continuation,
            stop_reason=stop,
            depth=depth,
        )
        recorder = getattr(self.receipt_sink, "record_continuation", None)
        if recorder is not None:
            recorder(decision)
        return decision

    def next_frontier_from_handoff(
        self,
        *,
        handoff: RecursiveBranchHandoff,
        root_query: EmpiricalQuerySpec,
        repository: C11Repository,
        release_refs: Iterable[ExactRef],
        coordinate_authority_refs: Iterable[AuthorityRef],
        depth: int,
    ) -> SealedFrontier:
        self._between_invocations()
        atom = recursive_parent_atom(handoff, "PARENT")
        if exact_ref(atom["predicate_ref"]) != handoff.winning_predicate.ref:
            raise FractureMapControllerError("MX01R2 parent atom mismatch")
        conditions = enumerate_coordinate_conditions(
            repository=repository,
            root_query=root_query,
            root_predicate=handoff.winning_predicate,
            release_refs=release_refs,
            coordinate_authority_refs=coordinate_authority_refs,
        )
        return self.seal_predictor_frontier(
            parent_predicate=handoff.winning_predicate,
            root_query=root_query,
            coordinate_conditions=conditions,
            depth=depth,
            ancestry_refs=(handoff.ref,),
        )


__all__ = [
    "CONTROLLER_CONTRACT_ID", "AUTH37_POLICY_ID", "FractureMapControllerError",
    "ControllerPolicy", "DiscoveryAuthorityBinder", "ControllerReceiptSink",
    "FractureMapControllerPolicy", "Authority37ControllerPolicy",
    "FractureMapContinuationDecision", "EmpiricalFractureMapReceipt",
    "ResponseCellSupport", "ResponseMorphology",
    "CoordinateCondition", "BranchRole", "SealedFrontier", "OperationalRefEnvelope",
    "FractureMapReceiptAccumulator",
    "derive_response_morphology", "enumerate_coordinate_conditions",
    "construct_four_way_branches", "FractureMapController",
]
