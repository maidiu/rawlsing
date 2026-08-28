"""Persisted recursive-branch handoff for PRE553 I05.

MX01 R2 closes one bounded common-contract gap only:

    discovered child -> exact persisted parent for discovery generation N+1

The semantic carrier is the existing C11-internal ``DiscoveryBranchReplayBinding``.
This module does not add a public semantic-object family, does not change the I05
frontier law, and does not introduce adaptive traversal.  It materializes exact
I05 compiler output together with the existing replay binding, persists the
predicate semantic projection and all hash-bound replay side material, and
provides a public N+1 consumption path that does not reconstruct the child from
caller knowledge.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next._pre553_query_predicate import _build_release_index, _eval_predicate
from rawlsing_next.pre553_c11_integrity import (
    DiscoveryBranchReplayBinding,
    TypedAbsence,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_discovery_exact import (
    I05_CONTRACT_ID,
    ExactBoundedDiscoveryError,
    ExactBoundedDiscoveryResult,
    _catalog_atoms,
    _catalog_templates,
    _compile_frontier,
    _verify_discovery_authority,
    execute_exact_bounded_discovery,
)
from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    DiscoveryAuthority,
    DiscoveryResultReceipt,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)

RECURSIVE_HANDOFF_CONTRACT_ID = "PRE553_MX01R2_RECURSIVE_HANDOFF@1.0.0"
RECURSIVE_BRANCH_FAMILIES = frozenset({"RECURSIVE_SUBGROUP_FORK"})


class RecursiveHandoffError(Pre553IntegrityError):
    """A recursive handoff is incomplete, mismatched, or not exactly replayable."""


def _derived_ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(
        kind,
        f"urn:rawlsing:pre553:mx01r2:{namespace}:sha256:{digest}",
        digest,
    )


def _canonical_refs(values: Iterable[ExactRef | Mapping[str, Any]]) -> tuple[ExactRef, ...]:
    return tuple(sorted({exact_ref(value).key: exact_ref(value) for value in values}.values(), key=lambda r: r.key))


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
    if not isinstance(value, str) or not value.strip():
        raise RecursiveHandoffError("text-or-absence field must contain exact text or TypedAbsence")
    return value.strip()


def _restore_predicate(payload: Mapping[str, Any]) -> EmpiricalPredicate:
    fields = payload.get("semantic_fields")
    if not isinstance(fields, Mapping):
        raise RecursiveHandoffError("persisted predicate lacks semantic_fields")
    predicate = EmpiricalPredicate(
        typed_state=payload.get("typed_state"),
        authority_snapshot_refs=payload.get("authority_snapshot_refs", ()),
        dependency_refs=payload.get("dependency_refs", ()),
        producer_replay_locator_or_reference_root=payload.get(
            "producer_replay_locator_or_reference_root"
        ),
        object_id=payload.get("object_id"),
        content_hash=payload.get("content_hash"),
        schema_id=payload.get("schema_id"),
        schema_version=payload.get("schema_version"),
        **dict(fields),
    )
    if predicate.as_dict() != canonicalize(payload):
        raise RecursiveHandoffError("persisted predicate projection is not identity-exact")
    return predicate


def _restore_binding(payload: Mapping[str, Any]) -> DiscoveryBranchReplayBinding:
    fields = payload.get("semantic_fields")
    if not isinstance(fields, Mapping):
        raise RecursiveHandoffError("persisted branch replay binding lacks semantic_fields")
    binding = DiscoveryBranchReplayBinding(
        state=fields.get("state"),
        search_family_id_or_typed_absence=_text_or_absence(
            fields.get("search_family_id_or_typed_absence")
        ),
        candidate_universe_ref_or_typed_absence=_exact_or_absence(
            fields.get("candidate_universe_ref_or_typed_absence")
        ),
        grammar_authority_ref_or_typed_absence=_authority_or_absence(
            fields.get("grammar_authority_ref_or_typed_absence")
        ),
        source_risk_topology_measure_scope_ref_or_typed_absence=_exact_or_absence(
            fields.get("source_risk_topology_measure_scope_ref_or_typed_absence")
        ),
        algorithm_identity_ref_or_typed_absence=_exact_or_absence(
            fields.get("algorithm_identity_ref_or_typed_absence")
        ),
        coverage_pruning_contract_ref_or_typed_absence=_exact_or_absence(
            fields.get("coverage_pruning_contract_ref_or_typed_absence")
        ),
        deterministic_parameters_ref_or_typed_absence=_exact_or_absence(
            fields.get("deterministic_parameters_ref_or_typed_absence")
        ),
        rng_state_ref_or_typed_absence=_exact_or_absence(
            fields.get("rng_state_ref_or_typed_absence")
        ),
        parent_branch_ref_or_typed_absence=_exact_or_absence(
            fields.get("parent_branch_ref_or_typed_absence")
        ),
        winning_predicate_ref_or_typed_absence=_exact_or_absence(
            fields.get("winning_predicate_ref_or_typed_absence")
        ),
        pruned_trace_ref_or_typed_absence=_exact_or_absence(
            fields.get("pruned_trace_ref_or_typed_absence")
        ),
    )
    if binding.object_id != payload.get("object_id") or binding.content_hash != payload.get("content_hash"):
        raise RecursiveHandoffError("persisted branch replay binding identity mismatch")
    return binding


@dataclass(frozen=True)
class RecursiveBranchHandoff:
    """Public operational handle over an existing DiscoveryBranchReplayBinding.

    ``ref`` is the exact existing replay-binding ref.  The additional mappings
    are hash-bound side material required to replay the binding, not new semantic
    ownership of the source payload.
    """

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
        if self.branch_replay_binding.state != "PRESENT":
            raise RecursiveHandoffError("recursive handoff requires PRESENT replay binding")
        parent = self.branch_replay_binding.parent_branch_ref_or_typed_absence
        winner = self.branch_replay_binding.winning_predicate_ref_or_typed_absence
        if not isinstance(parent, ExactRef):
            raise RecursiveHandoffError("recursive handoff requires exact immediate parent branch ref")
        if not isinstance(winner, ExactRef) or winner != self.winning_predicate.ref:
            raise RecursiveHandoffError("replay binding winning predicate does not bind persisted predicate")
        if not self.source_release_refs:
            raise RecursiveHandoffError("recursive handoff requires exact source release refs")
        candidate_ref = self.branch_replay_binding.candidate_universe_ref_or_typed_absence
        if not isinstance(candidate_ref, ExactRef):
            raise RecursiveHandoffError("recursive handoff requires exact candidate-universe ref")
        if candidate_ref.content_hash != semantic_hash(self.candidate_universe_definition):
            raise RecursiveHandoffError("candidate-universe side material hash mismatch")
        scope_ref = self.branch_replay_binding.source_risk_topology_measure_scope_ref_or_typed_absence
        if not isinstance(scope_ref, ExactRef) or scope_ref.content_hash != semantic_hash(self.scope_context):
            raise RecursiveHandoffError("scope-context side material hash mismatch")
        coverage_ref = self.branch_replay_binding.coverage_pruning_contract_ref_or_typed_absence
        if not isinstance(coverage_ref, ExactRef) or coverage_ref.content_hash != semantic_hash(self.coverage_pruning_material):
            raise RecursiveHandoffError("coverage/pruning side material hash mismatch")
        deterministic_ref = self.branch_replay_binding.deterministic_parameters_ref_or_typed_absence
        if not isinstance(deterministic_ref, ExactRef) or deterministic_ref.content_hash != semantic_hash(self.deterministic_parameters):
            raise RecursiveHandoffError("deterministic replay side material hash mismatch")

    @property
    def ref(self) -> ExactRef:
        return self.branch_replay_binding.ref

    @property
    def immediate_parent_branch_ref(self) -> ExactRef:
        parent = self.branch_replay_binding.parent_branch_ref_or_typed_absence
        if not isinstance(parent, ExactRef):
            raise RecursiveHandoffError("immediate parent branch ref unavailable")
        return parent

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
        if tuple(sorted(self.handoffs, key=lambda h: h.ref.key)) != self.handoffs:
            raise RecursiveHandoffError("recursive handoffs must be exact-ref sorted")
        if len({h.ref.key for h in self.handoffs}) != len(self.handoffs):
            raise RecursiveHandoffError("duplicate recursive handoff ref")

    def handoff_for_receipt(self, receipt_ref: ExactRef | Mapping[str, Any]) -> RecursiveBranchHandoff:
        target = exact_ref(receipt_ref)
        matches = [handoff for handoff in self.handoffs if handoff.receipt_ref == target]
        if len(matches) != 1:
            raise RecursiveHandoffError("receipt must resolve to exactly one recursive handoff")
        return matches[0]


def _make_handoff(
    *,
    candidate: Any,
    receipt: DiscoveryResultReceipt,
    discovery_authority: DiscoveryAuthority,
    discovery_result: ExactBoundedDiscoveryResult,
    release_refs: tuple[ExactRef, ...],
    candidate_universe_definition: Mapping[str, Any],
) -> RecursiveBranchHandoff:
    baseline_roles = [role for role in candidate.query_roles if role.role == "BASELINE"]
    if len(baseline_roles) != 1:
        raise RecursiveHandoffError("recursive branch candidate requires one exact BASELINE parent role")
    parent_ref = baseline_roles[0].predicate.ref
    if receipt.winning_predicate_ref != candidate.winning_predicate.ref:
        raise RecursiveHandoffError("receipt/winning compiled predicate ref mismatch")

    scope_context = canonicalize({
        "source_universe_scope": discovery_authority.source_universe_scope,
        "risk_set_scope": discovery_authority.risk_set_scope,
        "topology_scope": discovery_authority.topology_scope,
        "measure_scope": discovery_authority.measure_scope,
        "same_respondent_binding_semantics": candidate.winning_predicate.same_respondent_binding_semantics,
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
        "winning_predicate_ref": candidate.winning_predicate.ref,
        "immediate_parent_branch_ref": parent_ref,
        "support_rules": discovery_authority.support_rules,
        "validation_rules": discovery_authority.validation_rules,
        "query_role_refs": [
            {
                "role": role.role,
                "predicate_ref": role.predicate.ref,
                "query_ref": role.query.ref,
            }
            for role in candidate.query_roles
        ],
    })
    scope_ref = _derived_ref("PRE553_RECURSIVE_SCOPE_CONTEXT", "scope-context", scope_context)
    coverage_ref = _derived_ref(
        "PRE553_RECURSIVE_COVERAGE_PRUNING_CONTRACT",
        "coverage-pruning",
        coverage_pruning_material,
    )
    deterministic_ref = _derived_ref(
        "PRE553_RECURSIVE_DETERMINISTIC_PARAMETERS",
        "deterministic-parameters",
        deterministic_parameters,
    )
    algorithm_ref = _derived_ref(
        "PRE553_I05_ALGORITHM_IDENTITY",
        "algorithm-identity",
        {"algorithm_identity": I05_CONTRACT_ID},
    )
    binding = DiscoveryBranchReplayBinding(
        state="PRESENT",
        search_family_id_or_typed_absence=candidate.family,
        candidate_universe_ref_or_typed_absence=discovery_result.candidate_grammar_ref,
        grammar_authority_ref_or_typed_absence=authority_ref(
            candidate.winning_predicate.grammar_authority_ref
        ),
        source_risk_topology_measure_scope_ref_or_typed_absence=scope_ref,
        algorithm_identity_ref_or_typed_absence=algorithm_ref,
        coverage_pruning_contract_ref_or_typed_absence=coverage_ref,
        deterministic_parameters_ref_or_typed_absence=deterministic_ref,
        rng_state_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        parent_branch_ref_or_typed_absence=parent_ref,
        winning_predicate_ref_or_typed_absence=candidate.winning_predicate.ref,
        pruned_trace_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
    )
    return RecursiveBranchHandoff(
        receipt_ref=receipt.ref,
        branch_replay_binding=binding,
        winning_predicate=candidate.winning_predicate,
        source_release_refs=release_refs,
        discovery_authority_ref=discovery_authority.ref,
        evaluated_frontier_ref=discovery_result.evaluated_frontier_ref,
        candidate_universe_definition=canonicalize(candidate_universe_definition),
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
    """Execute I05 and materialize supported recursive branch children.

    The compiler is rerun deterministically from the same authority-declared
    pre-search grammar only to expose the already identity-matched compiled
    predicate.  The returned/persisted handoff, not compiler-private state, is
    the N+1 input.
    """
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

    definition = _verify_discovery_authority(discovery_authority, authority_registry)
    atoms = _catalog_atoms(definition, predicates)
    templates = _catalog_templates(definition, queries)
    candidates = _compile_frontier(definition, atoms, templates)
    candidates_by_identity = {
        (candidate.candidate_id, candidate.candidate_hash): candidate for candidate in candidates
    }
    if len(candidates_by_identity) != len(candidates):
        raise RecursiveHandoffError("compiled candidate identities are not unique")

    handoffs: list[RecursiveBranchHandoff] = []
    for receipt in result.receipts:
        identity = receipt.candidate_identity
        key = (identity.get("candidate_id"), identity.get("candidate_hash"))
        candidate = candidates_by_identity.get(key)
        if candidate is None:
            raise RecursiveHandoffError("discovery receipt has no exact compiled candidate match")
        if candidate.family not in RECURSIVE_BRANCH_FAMILIES:
            continue
        if receipt.typed_state != "DISCOVERED_RESULT_SUPPORTED":
            continue
        handoffs.append(_make_handoff(
            candidate=candidate,
            receipt=receipt,
            discovery_authority=discovery_authority,
            discovery_result=result,
            release_refs=releases,
            candidate_universe_definition=definition,
        ))
    return RecursiveHandoffDiscoveryResult(
        discovery_result=result,
        handoffs=tuple(sorted(handoffs, key=lambda h: h.ref.key)),
    )


def recursive_parent_atom(
    handoff: RecursiveBranchHandoff,
    atom_id: str,
) -> Mapping[str, Any]:
    """Return the exact N+1 grammar atom for a persisted discovered branch."""
    if not isinstance(atom_id, str) or not atom_id.strip():
        raise RecursiveHandoffError("recursive parent atom_id must be non-empty")
    return canonicalize({
        "atom_id": atom_id.strip(),
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
    """Replay the exact respondent cohort represented by a persisted handoff."""
    validate_object_authority_closure(handoff.winning_predicate, authority_registry)
    requested = (
        handoff.source_release_refs
        if release_refs is None
        else _canonical_refs(release_refs)
    )
    if tuple(requested) != tuple(handoff.source_release_refs):
        raise RecursiveHandoffError("membership replay requires the exact persisted source-release set")

    universe_refs = [
        exact_ref(value)
        for value in handoff.winning_predicate.scope_refs
        if exact_ref(value).kind == "EmpiricalUniverse@1.0.0"
    ]
    if not universe_refs:
        raise RecursiveHandoffError("winning predicate has no exact empirical-universe scope")

    members: dict[str, ExactRef] = {}
    for release_ref in requested:
        release = repository.resolve_release_exact(release_ref)
        for universe_ref in universe_refs:
            try:
                index = _build_release_index(release, universe_ref)
            except Exception as exc:
                if "exact universe must resolve once" in str(exc):
                    continue
                raise
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
    path: str | Path,
    handoffs: Sequence[RecursiveBranchHandoff],
) -> ExactRef:
    """Persist exact handoff side material; physical file bytes are not semantic authority."""
    canonical_handoffs = tuple(sorted(handoffs, key=lambda h: h.ref.key))
    if len({handoff.ref.key for handoff in canonical_handoffs}) != len(canonical_handoffs):
        raise RecursiveHandoffError("cannot persist duplicate handoff refs")
    payload = canonicalize({
        "contract_id": RECURSIVE_HANDOFF_CONTRACT_ID,
        "handoffs": [handoff.as_dict() for handoff in canonical_handoffs],
    })
    bundle_ref = _derived_ref("PRE553_RECURSIVE_HANDOFF_BUNDLE", "handoff-bundle", payload)
    envelope = canonicalize({
        "bundle_ref": bundle_ref,
        "payload": payload,
    })
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(canonical_json(envelope) + "\n", encoding="utf-8")
    return bundle_ref


def load_recursive_handoff_bundle(
    path: str | Path,
) -> tuple[ExactRef, tuple[RecursiveBranchHandoff, ...]]:
    """Fresh-process loader with full identity/hash verification."""
    envelope = json.loads(Path(path).read_text(encoding="utf-8"))
    bundle_ref = exact_ref(envelope.get("bundle_ref"))
    payload = envelope.get("payload")
    if not isinstance(payload, Mapping):
        raise RecursiveHandoffError("handoff bundle payload missing")
    if payload.get("contract_id") != RECURSIVE_HANDOFF_CONTRACT_ID:
        raise RecursiveHandoffError("handoff bundle contract id mismatch")
    expected_ref = _derived_ref("PRE553_RECURSIVE_HANDOFF_BUNDLE", "handoff-bundle", payload)
    if bundle_ref != expected_ref:
        raise RecursiveHandoffError("handoff bundle exact ref/hash mismatch")

    restored: list[RecursiveBranchHandoff] = []
    raw_handoffs = payload.get("handoffs", ())
    if isinstance(raw_handoffs, (str, bytes, bytearray)) or not isinstance(raw_handoffs, Sequence):
        raise RecursiveHandoffError("handoff bundle handoffs must be a sequence")
    for raw in raw_handoffs:
        if not isinstance(raw, Mapping):
            raise RecursiveHandoffError("handoff entry must be a mapping")
        if raw.get("contract_id") != RECURSIVE_HANDOFF_CONTRACT_ID:
            raise RecursiveHandoffError("handoff entry contract id mismatch")
        predicate = _restore_predicate(raw.get("winning_predicate", {}))
        binding = _restore_binding(raw.get("branch_replay_binding", {}))
        handoff = RecursiveBranchHandoff(
            receipt_ref=exact_ref(raw.get("receipt_ref")),
            branch_replay_binding=binding,
            winning_predicate=predicate,
            source_release_refs=_canonical_refs(raw.get("source_release_refs", ())),
            discovery_authority_ref=exact_ref(raw.get("discovery_authority_ref")),
            evaluated_frontier_ref=exact_ref(raw.get("evaluated_frontier_ref")),
            candidate_universe_definition=raw.get("candidate_universe_definition", {}),
            scope_context=raw.get("scope_context", {}),
            coverage_pruning_material=raw.get("coverage_pruning_material", {}),
            deterministic_parameters=raw.get("deterministic_parameters", {}),
        )
        if exact_ref(raw.get("handoff_ref")) != handoff.ref:
            raise RecursiveHandoffError("handoff entry exact ref mismatch")
        restored.append(handoff)
    canonical_restored = tuple(sorted(restored, key=lambda h: h.ref.key))
    if len({handoff.ref.key for handoff in canonical_restored}) != len(canonical_restored):
        raise RecursiveHandoffError("loaded bundle contains duplicate handoff refs")
    return bundle_ref, canonical_restored


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
