from __future__ import annotations

from dataclasses import dataclass, asdict, is_dataclass
from enum import Enum
import hashlib
import json
from typing import Any, Iterable, Mapping


COURT_OWNER_ID = "PRE553_SEMANTIC_MAINTENANCE_OWNER_C5R2_REF_V1"
COURT_EXECUTOR_ID = "PRE553_SEMANTIC_RELEASE_EXECUTOR_C5R2_REF_V1"
AUTHORITY_CEILING = "C5R2_ISOLATED_REFERENCE_EXECUTION_ONLY__NOT_LIVE_PROMOTION"
OWNER_CONTRACT = {
    "owner": COURT_OWNER_ID,
    "executor": COURT_EXECUTOR_ID,
    "boundary": "PRODUCER_SIDE_PRE553_SEMANTIC_AUTHORITY",
    "i04_role": "BIND_CONSUME_ONLY__NOT_SEMANTIC_TRUTH_OWNER",
    "v553_plus_role": "DOWNSTREAM_CONSUMER__NOT_SEMANTIC_TRUTH_OWNER",
    "authority_ceiling": AUTHORITY_CEILING,
    "truth_rule": "EXPLICIT_GOVERNED_ADJUDICATION_ONLY__NO_INFERENCE",
}


class SemanticMaintenanceError(RuntimeError):
    pass


class LifecycleType(str, Enum):
    SURVIVES_SAME_ID = "SURVIVES_SAME_ID"
    RECERTIFIES = "RECERTIFIES"
    CORRECTS = "CORRECTS"
    WITHDRAWS = "WITHDRAWS"
    CURRENT_SELECT = "CURRENT_SELECT"
    REOPENS_BLOCKED = "REOPENS_BLOCKED"
    APPENDS_SUCCESSOR_OBLIGATION = "APPENDS_SUCCESSOR_OBLIGATION"
    CHANGES_SCOPE_EXPLICITLY = "CHANGES_SCOPE_EXPLICITLY"


class GenealogyType(str, Enum):
    SUCCESSOR = "SUCCESSOR"
    SPLIT = "SPLIT"
    MERGE = "MERGE"
    VARIANT = "VARIANT"
    EXCLUSION = "EXCLUSION"


def _canon(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "as_dict"):
        return _canon(value.as_dict())
    if is_dataclass(value):
        return _canon(asdict(value))
    if isinstance(value, Mapping):
        return {str(k): _canon(value[k]) for k in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_canon(v) for v in value]
    if isinstance(value, set):
        return sorted((_canon(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_canon(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def semantic_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True, order=True)
class ExactRef:
    kind: str
    object_id: str
    content_hash: str

    @property
    def key(self) -> str:
        return f"{self.kind}|{self.object_id}|{self.content_hash}"

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceBundle:
    bundle_id: str
    evidence_refs: tuple[ExactRef, ...]
    completeness_state: str
    binding_authority_ref: ExactRef

    def __post_init__(self) -> None:
        if self.completeness_state != "COMPLETE":
            raise SemanticMaintenanceError("evidence bundle must be COMPLETE before adjudication")
        if not self.evidence_refs:
            raise SemanticMaintenanceError("complete evidence bundle cannot be empty")

    @property
    def ref(self) -> ExactRef:
        payload = {
            "bundle_id": self.bundle_id,
            "evidence_refs": [r.as_dict() for r in self.evidence_refs],
            "completeness_state": self.completeness_state,
            "binding_authority_ref": self.binding_authority_ref.as_dict(),
        }
        return ExactRef("SEMANTIC_EVIDENCE_BUNDLE", self.bundle_id, semantic_hash(payload))


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    family: str
    members: tuple[str, ...]
    member_roles: tuple[tuple[str, str], ...]
    constitutive_payload: Mapping[str, Any]
    scope: Mapping[str, Any]
    family_rule_ref: ExactRef
    evidence_bundle_ref: ExactRef

    @property
    def proposition_id(self) -> str:
        return semantic_hash({
            "family": self.family,
            "members": self.members,
            "member_roles": self.member_roles,
            "constitutive_payload": self.constitutive_payload,
            "scope": self.scope,
            "family_rule_ref": self.family_rule_ref.as_dict(),
        })

    @property
    def ref(self) -> ExactRef:
        return ExactRef("SEMANTIC_CANDIDATE", self.candidate_id, semantic_hash({
            "candidate_id": self.candidate_id,
            "proposition_id": self.proposition_id,
            "evidence_bundle_ref": self.evidence_bundle_ref.as_dict(),
        }))


@dataclass(frozen=True)
class GovernedDecision:
    decision_id: str
    candidate_ref: ExactRef
    outcome: str
    decision_authority_ref: ExactRef
    rationale_code: str

    def __post_init__(self) -> None:
        if self.outcome not in {"ACCEPT", "REJECT", "BLOCKED"}:
            raise SemanticMaintenanceError("unsupported adjudication outcome")

    @property
    def ref(self) -> ExactRef:
        return ExactRef("SEMANTIC_ADJUDICATION", self.decision_id, semantic_hash(asdict(self)))


@dataclass(frozen=True)
class SemanticAuthority:
    authority_id: str
    authority_version: str
    semantic_claim_id: str
    proposition_id: str
    truth_state: str
    family: str
    members: tuple[str, ...]
    member_roles: tuple[tuple[str, str], ...]
    constitutive_payload: Mapping[str, Any]
    scope: Mapping[str, Any]
    evidence_bundle_ref: ExactRef
    adjudication_ref: ExactRef
    owner_contract_hash: str
    predecessor_authority_ref: ExactRef | None

    @property
    def ref(self) -> ExactRef:
        return ExactRef("SEMANTIC_AUTHORITY", f"{self.authority_id}@{self.authority_version}", semantic_hash(self.payload()))

    def payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LifecycleEvent:
    event_id: str
    event_type: LifecycleType
    subject_authority_ref: ExactRef
    predecessor_authority_ref: ExactRef | None
    jurisdiction_key: str
    decision_authority_ref: ExactRef
    note: str

    @property
    def ref(self) -> ExactRef:
        return ExactRef("SEMANTIC_LIFECYCLE_EVENT", self.event_id, semantic_hash(asdict(self)))


@dataclass(frozen=True)
class GovernedGenealogyDecision:
    decision_id: str
    operation: GenealogyType
    parent_refs: tuple[ExactRef, ...]
    child_refs: tuple[ExactRef, ...]
    decision_authority_ref: ExactRef
    resolution_state: str
    rationale_code: str

    def __post_init__(self) -> None:
        if self.resolution_state not in {"RESOLVED", "AMBIGUOUS", "BLOCKED"}:
            raise SemanticMaintenanceError("unsupported genealogy resolution state")

    @property
    def ref(self) -> ExactRef:
        return ExactRef("SEMANTIC_GENEALOGY_DECISION", self.decision_id, semantic_hash(asdict(self)))


@dataclass(frozen=True)
class GenealogyEdge:
    edge_id: str
    edge_type: GenealogyType
    parent_refs: tuple[ExactRef, ...]
    child_refs: tuple[ExactRef, ...]
    parent_members: tuple[str, ...]
    child_member_sets: tuple[tuple[str, ...], ...]
    governing_decision_ref: ExactRef

    @property
    def ref(self) -> ExactRef:
        return ExactRef("SEMANTIC_GENEALOGY_EDGE", self.edge_id, semantic_hash(asdict(self)))


@dataclass(frozen=True)
class DependencyBinding:
    binding_id: str
    semantic_authority_ref: ExactRef
    descendant_refs: tuple[ExactRef, ...]

    @property
    def ref(self) -> ExactRef:
        return ExactRef("SEMANTIC_FORWARD_DEPENDENCY_BINDING", self.binding_id, semantic_hash(asdict(self)))


@dataclass(frozen=True)
class RevalidationReceipt:
    receipt_id: str
    triggering_event_ref: ExactRef
    triggering_event_type: LifecycleType
    semantic_authority_ref: ExactRef
    descendant_refs: tuple[ExactRef, ...]

    @property
    def ref(self) -> ExactRef:
        return ExactRef("SEMANTIC_REVALIDATION_RECEIPT", self.receipt_id, semantic_hash(asdict(self)))


@dataclass(frozen=True)
class SemanticRelease:
    release_id: str
    authority_refs: tuple[ExactRef, ...]
    lifecycle_refs: tuple[ExactRef, ...]
    genealogy_refs: tuple[ExactRef, ...]
    revalidation_refs: tuple[ExactRef, ...]
    predecessor_release_ref: ExactRef | None
    executor_contract_hash: str

    @property
    def ref(self) -> ExactRef:
        return ExactRef("SEMANTIC_RELEASE", self.release_id, semantic_hash(asdict(self)))


class FamilyPolicyRegistry:
    """Distinct family dispatch. Missing family policy fails closed."""

    REQUIRED_CONSTITUTIVE_KEYS = {
        "T01": {"predicate_identity", "target_mapping"},
        "T02": {"proposition_identity", "condition_mapping"},
        "T03": {"principle_application_roles"},
        "T04": {"goal_means_roles"},
        "T05": {"commitment_cost_roles"},
        "T06": {"actor", "target", "action_domain", "modality"},
        "T07": {"hierarchy_identity"},
        "T08": {"relation_semantics"},
        "T09": {"role_direction"},
        "T10": {"target_condition_matrix"},
        "T11": {"complementary_roles"},
        "T12": {"source_native_routing"},
        "T13": {"tradeoff_frame"},
        "T14": {"nomination_only"},
        "T15": {"manifestation_subtype", "praxis_shore_kind", "polarity", "realization_distance", "actor", "target", "bridge_semantic_kind"},
    }

    def validate(self, candidate: Candidate) -> None:
        required = self.REQUIRED_CONSTITUTIVE_KEYS.get(candidate.family)
        if required is None:
            raise SemanticMaintenanceError(f"no governed family policy for {candidate.family}")
        if candidate.family == "T14":
            raise SemanticMaintenanceError("T14 is nomination-only and cannot directly become typed relation truth")
        missing = required - set(candidate.constitutive_payload)
        if missing:
            raise SemanticMaintenanceError(f"family-specific constitutive fields missing: {sorted(missing)}")
        if len(candidate.members) < 2:
            raise SemanticMaintenanceError("relation authority requires at least two exact members")
        role_members = {m for m, _ in candidate.member_roles}
        if role_members != set(candidate.members):
            raise SemanticMaintenanceError("member-role coverage must exactly match member set")


class Pre553SemanticMaintenanceOwner:
    """Court-governed producer-side PRE553 reference owner.

    This is authoritative only for the isolated C5R2 execution proof. It never
    infers a semantic decision from evidence, chronology, dependency traversal,
    labels, or code proximity. A GovernedDecision is mandatory.
    """

    def __init__(self) -> None:
        self.owner_contract_hash = semantic_hash(OWNER_CONTRACT)
        self.family_policies = FamilyPolicyRegistry()
        self.governance_authorities: dict[str, ExactRef] = {}
        self.family_rule_refs: dict[str, ExactRef] = {}
        self.evidence_bundles: dict[str, EvidenceBundle] = {}
        self.candidates: dict[str, Candidate] = {}
        self.decisions: dict[str, GovernedDecision] = {}
        self.authorities: dict[str, SemanticAuthority] = {}
        self.authority_order: list[str] = []
        self.lifecycle_events: dict[str, LifecycleEvent] = {}
        self.current_selection: dict[str, ExactRef | None] = {}
        self.genealogy_decisions: dict[str, GovernedGenealogyDecision] = {}
        self.genealogy: dict[str, GenealogyEdge] = {}
        self.forward_bindings: dict[str, DependencyBinding] = {}
        self.revalidation_receipts: dict[str, RevalidationReceipt] = {}
        self.journal: list[dict[str, Any]] = []

    def _append(self, kind: str, obj: Any) -> None:
        record = {"seq": len(self.journal) + 1, "kind": kind, "payload": _canon(obj)}
        record["record_hash"] = semantic_hash(record)
        self.journal.append(record)

    def register_governance_authority(self, ref: ExactRef) -> ExactRef:
        if ref.kind != "COURT_DECISION_AUTHORITY":
            raise SemanticMaintenanceError("court/governance decision authority ref required")
        existing = self.governance_authorities.get(ref.object_id)
        if existing is not None and existing != ref:
            raise SemanticMaintenanceError("governance authority identity conflict")
        self.governance_authorities[ref.object_id] = ref
        self._append("GOVERNANCE_AUTHORITY_BINDING", ref)
        return ref

    def register_family_rule(self, family: str, ref: ExactRef) -> ExactRef:
        if family not in self.family_policies.REQUIRED_CONSTITUTIVE_KEYS:
            raise SemanticMaintenanceError("unknown semantic family")
        if ref.kind != "SEMANTIC_FAMILY_RULE":
            raise SemanticMaintenanceError("exact semantic family-rule ref required")
        existing = self.family_rule_refs.get(family)
        if existing is not None and existing != ref:
            raise SemanticMaintenanceError("family rule already governed by a different exact ref")
        self.family_rule_refs[family] = ref
        self._append("FAMILY_RULE_BINDING", {"family": family, "ref": ref})
        return ref

    def bind_evidence(self, bundle: EvidenceBundle) -> EvidenceBundle:
        existing = self.evidence_bundles.get(bundle.bundle_id)
        if existing is not None and existing != bundle:
            raise SemanticMaintenanceError("evidence bundle identity conflict")
        self.evidence_bundles[bundle.bundle_id] = bundle
        self._append("COMPLETE_EVIDENCE_BINDING", bundle)
        return bundle

    def _decision_by_ref(self, ref: ExactRef) -> GovernedDecision:
        for decision in self.decisions.values():
            if decision.ref == ref:
                return decision
        raise SemanticMaintenanceError("exact governed adjudication ref unavailable")

    def _require_governance_ref(self, ref: ExactRef) -> None:
        if ref not in self.governance_authorities.values():
            raise SemanticMaintenanceError("unregistered governance authority")

    def nominate(self, candidate: Candidate) -> Candidate:
        if candidate.candidate_id in self.candidates:
            raise SemanticMaintenanceError("candidate id already exists")
        self.family_policies.validate(candidate)
        governed_rule = self.family_rule_refs.get(candidate.family)
        if governed_rule is None or governed_rule != candidate.family_rule_ref:
            raise SemanticMaintenanceError("candidate family rule is not the registered exact governed rule")
        if candidate.evidence_bundle_ref.kind != "SEMANTIC_EVIDENCE_BUNDLE":
            raise SemanticMaintenanceError("candidate must name an exact semantic evidence-bundle ref")
        self.candidates[candidate.candidate_id] = candidate
        self._append("CANDIDATE_NOMINATION", candidate)
        return candidate

    def adjudicate(self, decision: GovernedDecision) -> GovernedDecision:
        if decision.candidate_ref.object_id not in self.candidates:
            raise SemanticMaintenanceError("adjudication candidate is unavailable")
        candidate = self.candidates[decision.candidate_ref.object_id]
        if candidate.ref != decision.candidate_ref:
            raise SemanticMaintenanceError("adjudication candidate ref mismatch")
        if candidate.evidence_bundle_ref not in {b.ref for b in self.evidence_bundles.values()}:
            raise SemanticMaintenanceError("adjudication requires the candidate's exact COMPLETE evidence bundle to be bound")
        self._require_governance_ref(decision.decision_authority_ref)
        if decision.decision_id in self.decisions:
            raise SemanticMaintenanceError("decision id already exists")
        self.decisions[decision.decision_id] = decision
        self._append("GOVERNED_ADJUDICATION", decision)
        return decision

    def create_authority(self, *, authority_id: str, authority_version: str, decision: GovernedDecision,
                         predecessor_authority_ref: ExactRef | None = None) -> SemanticAuthority:
        if decision.outcome != "ACCEPT":
            raise SemanticMaintenanceError("only explicit ACCEPT adjudication may create positive semantic authority")
        candidate = self.candidates.get(decision.candidate_ref.object_id)
        if candidate is None or candidate.ref != decision.candidate_ref:
            raise SemanticMaintenanceError("accepted candidate exact ref unavailable")
        self.family_policies.validate(candidate)
        claim_id = semantic_hash({"proposition_id": candidate.proposition_id, "truth_state": "ACCEPT"})
        authority = SemanticAuthority(
            authority_id=authority_id,
            authority_version=authority_version,
            semantic_claim_id=claim_id,
            proposition_id=candidate.proposition_id,
            truth_state="ACCEPT",
            family=candidate.family,
            members=candidate.members,
            member_roles=candidate.member_roles,
            constitutive_payload=dict(candidate.constitutive_payload),
            scope=dict(candidate.scope),
            evidence_bundle_ref=candidate.evidence_bundle_ref,
            adjudication_ref=decision.ref,
            owner_contract_hash=self.owner_contract_hash,
            predecessor_authority_ref=predecessor_authority_ref,
        )
        key = authority.ref.key
        if key in self.authorities:
            raise SemanticMaintenanceError("authority exact ref already exists")
        same_id_version = [a for a in self.authorities.values() if a.authority_id == authority_id and a.authority_version == authority_version]
        if same_id_version:
            raise SemanticMaintenanceError("same authority id/version cannot carry different immutable content")
        self.authorities[key] = authority
        self.authority_order.append(key)
        self._append("IMMUTABLE_SEMANTIC_AUTHORITY", authority)
        return authority

    def resolve_authority_exact(self, ref: ExactRef) -> SemanticAuthority:
        if ref.kind != "SEMANTIC_AUTHORITY":
            raise SemanticMaintenanceError("exact semantic authority ref required")
        try:
            return self.authorities[ref.key]
        except KeyError as exc:
            raise SemanticMaintenanceError("exact semantic authority unavailable; no latest/default fallback") from exc

    def record_lifecycle(self, event: LifecycleEvent) -> LifecycleEvent:
        self._require_governance_ref(event.decision_authority_ref)
        if event.event_type == LifecycleType.REOPENS_BLOCKED:
            blocked = self._decision_by_ref(event.subject_authority_ref)
            if blocked.outcome != "BLOCKED":
                raise SemanticMaintenanceError("REOPENS_BLOCKED requires an exact BLOCKED adjudication")
            if event.predecessor_authority_ref is not None:
                raise SemanticMaintenanceError("BLOCKED reopen cannot smuggle a positive predecessor authority")
        else:
            self.resolve_authority_exact(event.subject_authority_ref)
            if event.predecessor_authority_ref is not None:
                self.resolve_authority_exact(event.predecessor_authority_ref)
        if event.event_id in self.lifecycle_events:
            raise SemanticMaintenanceError("lifecycle event id already exists")
        self.lifecycle_events[event.event_id] = event
        self._append("TYPED_LIFECYCLE_EVENT", event)
        if event.event_type == LifecycleType.CURRENT_SELECT:
            self.current_selection[event.jurisdiction_key] = event.subject_authority_ref
        elif event.event_type == LifecycleType.WITHDRAWS:
            current = self.current_selection.get(event.jurisdiction_key)
            if current == event.subject_authority_ref:
                self.current_selection[event.jurisdiction_key] = None
        return event

    def select_current(self, *, event_id: str, authority_ref: ExactRef, jurisdiction_key: str,
                       decision_authority_ref: ExactRef) -> LifecycleEvent:
        return self.record_lifecycle(LifecycleEvent(
            event_id=event_id,
            event_type=LifecycleType.CURRENT_SELECT,
            subject_authority_ref=authority_ref,
            predecessor_authority_ref=self.current_selection.get(jurisdiction_key),
            jurisdiction_key=jurisdiction_key,
            decision_authority_ref=decision_authority_ref,
            note="explicit current selection; chronology has zero selection force",
        ))

    def withdraw(self, *, event_id: str, authority_ref: ExactRef, jurisdiction_key: str,
                 decision_authority_ref: ExactRef) -> LifecycleEvent:
        return self.record_lifecycle(LifecycleEvent(
            event_id=event_id,
            event_type=LifecycleType.WITHDRAWS,
            subject_authority_ref=authority_ref,
            predecessor_authority_ref=None,
            jurisdiction_key=jurisdiction_key,
            decision_authority_ref=decision_authority_ref,
            note="withdrawal changes current authorization only; history remains immutable",
        ))

    def current_exact(self, jurisdiction_key: str) -> SemanticAuthority | None:
        ref = self.current_selection.get(jurisdiction_key)
        return None if ref is None else self.resolve_authority_exact(ref)

    def _genealogy_decision_by_ref(self, ref: ExactRef) -> GovernedGenealogyDecision:
        for decision in self.genealogy_decisions.values():
            if decision.ref == ref:
                return decision
        raise SemanticMaintenanceError("exact governed genealogy decision ref unavailable")

    def adjudicate_genealogy(self, decision: GovernedGenealogyDecision) -> GovernedGenealogyDecision:
        self._require_governance_ref(decision.decision_authority_ref)
        for ref in decision.parent_refs + decision.child_refs:
            self.resolve_authority_exact(ref)
        if decision.resolution_state != "RESOLVED":
            raise SemanticMaintenanceError("ambiguous or blocked genealogy adjudication fails closed")
        if decision.decision_id in self.genealogy_decisions:
            raise SemanticMaintenanceError("genealogy decision id already exists")
        self.genealogy_decisions[decision.decision_id] = decision
        self._append("GOVERNED_GENEALOGY_ADJUDICATION", decision)
        return decision

    def append_genealogy(self, edge: GenealogyEdge, *, ambiguous: bool = False) -> GenealogyEdge:
        if ambiguous:
            raise SemanticMaintenanceError("ambiguous genealogy operation fails closed")
        if edge.edge_id in self.genealogy:
            raise SemanticMaintenanceError("genealogy edge id already exists")
        resolved_parents = [self.resolve_authority_exact(ref) for ref in edge.parent_refs]
        resolved_children = [self.resolve_authority_exact(ref) for ref in edge.child_refs]
        genealogy_decision = self._genealogy_decision_by_ref(edge.governing_decision_ref)
        if genealogy_decision.operation != edge.edge_type or genealogy_decision.parent_refs != edge.parent_refs or genealogy_decision.child_refs != edge.child_refs:
            raise SemanticMaintenanceError("genealogy edge does not match exact governed genealogy decision")
        if edge.edge_type == GenealogyType.SPLIT:
            if len(resolved_parents) != 1:
                raise SemanticMaintenanceError("split requires exactly one parent authority")
            if tuple(resolved_parents[0].members) != tuple(edge.parent_members):
                raise SemanticMaintenanceError("split parent-member declaration mismatches exact parent authority")
            if len(edge.child_member_sets) != len(resolved_children):
                raise SemanticMaintenanceError("split child-member declarations must match exact child authority count")
            for declared, child in zip(edge.child_member_sets, resolved_children):
                if set(declared) != set(child.members):
                    raise SemanticMaintenanceError("split child-member declaration mismatches exact child authority")
            parent = set(edge.parent_members)
            union: set[str] = set()
            seen: set[str] = set()
            for members in edge.child_member_sets:
                mset = set(members)
                if seen & mset:
                    raise SemanticMaintenanceError("split members may not overlap")
                seen |= mset
                union |= mset
            if union != parent:
                raise SemanticMaintenanceError("split-member conservation failed")
        if edge.edge_type == GenealogyType.MERGE:
            if len(resolved_children) != 1:
                raise SemanticMaintenanceError("merge requires exactly one child authority")
            parent_union: set[str] = set()
            for parent_authority in resolved_parents:
                parent_union |= set(parent_authority.members)
            if len(edge.child_member_sets) != 1 or set(edge.child_member_sets[0]) != set(resolved_children[0].members):
                raise SemanticMaintenanceError("merge child-member declaration mismatches exact child authority")
            if parent_union != set(resolved_children[0].members):
                raise SemanticMaintenanceError("merge-member conservation failed")
        if edge.edge_type in {GenealogyType.VARIANT, GenealogyType.EXCLUSION, GenealogyType.SPLIT, GenealogyType.MERGE}:
            if edge.governing_decision_ref.kind != "SEMANTIC_GENEALOGY_DECISION":
                raise SemanticMaintenanceError("governed genealogy decision required")
        self.genealogy[edge.edge_id] = edge
        self._append("APPEND_ONLY_GENEALOGY", edge)
        return edge

    def bind_descendants(self, binding: DependencyBinding) -> DependencyBinding:
        self.resolve_authority_exact(binding.semantic_authority_ref)
        if not binding.descendant_refs:
            raise SemanticMaintenanceError("dependency binding requires exact descendants")
        if binding.binding_id in self.forward_bindings:
            raise SemanticMaintenanceError("dependency binding id already exists")
        self.forward_bindings[binding.binding_id] = binding
        self._append("IMMUTABLE_FORWARD_DEPENDENCY_BINDING", binding)
        return binding

    def revalidate_descendants(self, *, receipt_id: str, authority_ref: ExactRef,
                               triggering_event: LifecycleEvent | None) -> RevalidationReceipt:
        if triggering_event is None:
            raise SemanticMaintenanceError("dependency traversal cannot infer lifecycle event type")
        self.resolve_authority_exact(authority_ref)
        descendants = sorted({r for b in self.forward_bindings.values()
                              if b.semantic_authority_ref == authority_ref for r in b.descendant_refs}, key=lambda r: r.key)
        if not descendants:
            raise SemanticMaintenanceError("no complete forward bindings for descendant revalidation")
        receipt = RevalidationReceipt(
            receipt_id=receipt_id,
            triggering_event_ref=triggering_event.ref,
            triggering_event_type=triggering_event.event_type,
            semantic_authority_ref=authority_ref,
            descendant_refs=tuple(descendants),
        )
        self.revalidation_receipts[receipt_id] = receipt
        self._append("DESCENDANT_REVALIDATION", receipt)
        return receipt


class Pre553SemanticReleaseExecutor:
    """Court-governed isolated release/promotion/rollback executor."""

    def __init__(self, owner: Pre553SemanticMaintenanceOwner) -> None:
        self.owner = owner
        self.executor_contract_hash = semantic_hash({"executor": COURT_EXECUTOR_ID, "owner_contract_hash": owner.owner_contract_hash, "ceiling": AUTHORITY_CEILING})
        self.releases: dict[str, SemanticRelease] = {}
        self.current_release_ref: ExactRef | None = None
        self.release_journal: list[dict[str, Any]] = []

    def _append(self, kind: str, payload: Any) -> None:
        record = {"seq": len(self.release_journal) + 1, "kind": kind, "payload": _canon(payload)}
        record["record_hash"] = semantic_hash(record)
        self.release_journal.append(record)

    def assemble_release(self, *, release_id: str, authority_refs: Iterable[ExactRef],
                         lifecycle_refs: Iterable[ExactRef], genealogy_refs: Iterable[ExactRef],
                         revalidation_refs: Iterable[ExactRef], predecessor_release_ref: ExactRef | None = None) -> SemanticRelease:
        auths = tuple(authority_refs)
        if not auths:
            raise SemanticMaintenanceError("semantic release requires at least one exact authority")
        for ref in auths:
            self.owner.resolve_authority_exact(ref)
        for ref in lifecycle_refs:
            if ref.key not in {e.ref.key for e in self.owner.lifecycle_events.values()}:
                raise SemanticMaintenanceError("release lifecycle ref is unavailable")
        for ref in genealogy_refs:
            if ref.key not in {e.ref.key for e in self.owner.genealogy.values()}:
                raise SemanticMaintenanceError("release genealogy ref is unavailable")
        for ref in revalidation_refs:
            if ref.key not in {e.ref.key for e in self.owner.revalidation_receipts.values()}:
                raise SemanticMaintenanceError("release revalidation ref is unavailable")
        if predecessor_release_ref is not None:
            self.resolve_release_exact(predecessor_release_ref)
        release = SemanticRelease(
            release_id=release_id,
            authority_refs=tuple(sorted(auths, key=lambda r: r.key)),
            lifecycle_refs=tuple(sorted(lifecycle_refs, key=lambda r: r.key)),
            genealogy_refs=tuple(sorted(genealogy_refs, key=lambda r: r.key)),
            revalidation_refs=tuple(sorted(revalidation_refs, key=lambda r: r.key)),
            predecessor_release_ref=predecessor_release_ref,
            executor_contract_hash=self.executor_contract_hash,
        )
        if release.ref.key in self.releases:
            raise SemanticMaintenanceError("release exact ref already exists")
        self.releases[release.ref.key] = release
        self._append("IMMUTABLE_SEMANTIC_RELEASE", release)
        return release

    def resolve_release_exact(self, ref: ExactRef) -> SemanticRelease:
        if ref.kind != "SEMANTIC_RELEASE":
            raise SemanticMaintenanceError("exact semantic release ref required")
        try:
            return self.releases[ref.key]
        except KeyError as exc:
            raise SemanticMaintenanceError("exact release unavailable; no latest/default fallback") from exc

    def promote(self, release_ref: ExactRef, *, decision_authority_ref: ExactRef) -> None:
        self.owner._require_governance_ref(decision_authority_ref)
        release = self.resolve_release_exact(release_ref)
        current_refs = {r for r in self.owner.current_selection.values() if r is not None}
        if any(ref not in current_refs for ref in release.authority_refs):
            raise SemanticMaintenanceError("promotion requires explicit current selection for every released semantic authority")
        prior = self.current_release_ref
        self.current_release_ref = release_ref
        self._append("EXPLICIT_RELEASE_PROMOTION", {"from": prior, "to": release_ref, "decision_authority_ref": decision_authority_ref})

    def rollback(self, predecessor_release_ref: ExactRef, *, decision_authority_ref: ExactRef) -> None:
        self.owner._require_governance_ref(decision_authority_ref)
        self.resolve_release_exact(predecessor_release_ref)
        prior = self.current_release_ref
        self.current_release_ref = predecessor_release_ref
        self._append("EXPLICIT_RELEASE_ROLLBACK", {"from": prior, "to": predecessor_release_ref, "decision_authority_ref": decision_authority_ref, "history_rewritten": False})


def make_ref(kind: str, object_id: str, payload: Any) -> ExactRef:
    return ExactRef(kind, object_id, semantic_hash(payload))


def build_authoritative_witness() -> dict[str, Any]:
    owner = Pre553SemanticMaintenanceOwner()
    executor = Pre553SemanticReleaseExecutor(owner)

    family_rule = make_ref("SEMANTIC_FAMILY_RULE", "T06_RULE_C5R2_FIXTURE", {"family": "T06", "rule": "explicit norm/conduct actor-target-action-modality"})
    binding_authority = make_ref("EVIDENCE_BINDING_AUTHORITY", "C5R2_BINDING_V1", {"complete": True, "mode": "exact_refs_only"})
    court_decision_authority = make_ref("COURT_DECISION_AUTHORITY", "C5R2_PROOF_JURISDICTION", OWNER_CONTRACT)
    evidence_v1 = make_ref("SOURCE_EVIDENCE", "fixture_doc_v1", {"text": "governed fixture evidence v1"})
    evidence_v2 = make_ref("SOURCE_EVIDENCE", "fixture_doc_v2", {"text": "corrected/stronger governed fixture evidence v2", "same_constitutive_semantics": True})

    owner.register_governance_authority(court_decision_authority)
    owner.register_family_rule("T06", family_rule)

    bundle_v1 = EvidenceBundle("EB-001", (evidence_v1,), "COMPLETE", binding_authority)
    candidate_v1 = Candidate(
        candidate_id="CAND-001",
        family="T06",
        members=("Q-NORM", "Q-CONDUCT"),
        member_roles=(("Q-NORM", "NORM"), ("Q-CONDUCT", "CONDUCT")),
        constitutive_payload={"actor": "RESPONDENT", "target": "PUBLIC_RULE", "action_domain": "COMPLY", "modality": "EXPECTED"},
        scope={"source": "C5R2_FIXTURE", "wave": "W1"},
        family_rule_ref=family_rule,
        evidence_bundle_ref=bundle_v1.ref,
    )
    owner.nominate(candidate_v1)
    if owner.authorities:
        raise AssertionError("nomination created authority")
    owner.bind_evidence(bundle_v1)
    decision_v1 = owner.adjudicate(GovernedDecision("ADJ-001", candidate_v1.ref, "ACCEPT", court_decision_authority, "EXACT_T06_EVIDENCE_ACCEPT"))
    authority_v1 = owner.create_authority(authority_id="SEM-AUTH-001", authority_version="1.0.0", decision=decision_v1)
    select_v1 = owner.select_current(event_id="EV-SEL-001", authority_ref=authority_v1.ref, jurisdiction_key="T06|C5R2_FIXTURE|W1", decision_authority_ref=court_decision_authority)
    bind_v1 = owner.bind_descendants(DependencyBinding("DEP-001", authority_v1.ref, (
        make_ref("I04_ADMISSION", "I04-FIXTURE-001", {"semantic_authority": authority_v1.ref.as_dict()}),
        make_ref("STRUCTURAL_DESCENDANT", "V553-FIXTURE-001", {"from": "I04-FIXTURE-001"}),
    )))
    rv_v1 = owner.revalidate_descendants(receipt_id="RV-001", authority_ref=authority_v1.ref, triggering_event=select_v1)
    release_v1 = executor.assemble_release(release_id="REL-001", authority_refs=(authority_v1.ref,), lifecycle_refs=(select_v1.ref,), genealogy_refs=(), revalidation_refs=(rv_v1.ref,))
    executor.promote(release_v1.ref, decision_authority_ref=court_decision_authority)

    bundle_v2 = EvidenceBundle("EB-002", (evidence_v1, evidence_v2), "COMPLETE", binding_authority)
    candidate_v2 = Candidate(
        candidate_id="CAND-002",
        family="T06",
        members=candidate_v1.members,
        member_roles=candidate_v1.member_roles,
        constitutive_payload=dict(candidate_v1.constitutive_payload),
        scope=dict(candidate_v1.scope),
        family_rule_ref=family_rule,
        evidence_bundle_ref=bundle_v2.ref,
    )
    owner.nominate(candidate_v2)
    owner.bind_evidence(bundle_v2)
    decision_v2 = owner.adjudicate(GovernedDecision("ADJ-002", candidate_v2.ref, "ACCEPT", court_decision_authority, "CORRECTED_EVIDENCE_RECERTIFIES_SAME_CLAIM"))
    authority_v2 = owner.create_authority(authority_id="SEM-AUTH-002", authority_version="1.0.0", decision=decision_v2, predecessor_authority_ref=authority_v1.ref)
    if authority_v1.semantic_claim_id != authority_v2.semantic_claim_id:
        raise AssertionError("nonconstitutive corrected evidence unexpectedly changed semantic claim identity")
    recert = owner.record_lifecycle(LifecycleEvent("EV-RECERT-001", LifecycleType.RECERTIFIES, authority_v2.ref, authority_v1.ref, "T06|C5R2_FIXTURE|W1", court_decision_authority, "same claim; new governing authority instance"))
    select_v2 = owner.select_current(event_id="EV-SEL-002", authority_ref=authority_v2.ref, jurisdiction_key="T06|C5R2_FIXTURE|W1", decision_authority_ref=court_decision_authority)
    genealogy_decision = owner.adjudicate_genealogy(GovernedGenealogyDecision(
        "GADJ-SUCC-001", GenealogyType.SUCCESSOR, (authority_v1.ref,), (authority_v2.ref,), court_decision_authority, "RESOLVED", "EXPLICIT_RECERTIFICATION_SUCCESSOR"
    ))
    genealogy = owner.append_genealogy(GenealogyEdge(
        "GEN-SUCC-001", GenealogyType.SUCCESSOR, (authority_v1.ref,), (authority_v2.ref,),
        parent_members=authority_v1.members, child_member_sets=(authority_v2.members,), governing_decision_ref=genealogy_decision.ref
    ))
    owner.bind_descendants(DependencyBinding("DEP-002", authority_v2.ref, bind_v1.descendant_refs))
    rv_v2 = owner.revalidate_descendants(receipt_id="RV-002", authority_ref=authority_v2.ref, triggering_event=recert)
    release_v2 = executor.assemble_release(release_id="REL-002", authority_refs=(authority_v2.ref,), lifecycle_refs=(recert.ref, select_v2.ref), genealogy_refs=(genealogy.ref,), revalidation_refs=(rv_v2.ref,), predecessor_release_ref=release_v1.ref)
    executor.promote(release_v2.ref, decision_authority_ref=court_decision_authority)
    executor.rollback(release_v1.ref, decision_authority_ref=court_decision_authority)

    replay_authority_v1 = owner.resolve_authority_exact(authority_v1.ref)
    replay_authority_v2 = owner.resolve_authority_exact(authority_v2.ref)
    replay_release_v1 = executor.resolve_release_exact(release_v1.ref)
    replay_release_v2 = executor.resolve_release_exact(release_v2.ref)

    return {
        "status": "C5R2_AUTHORITATIVE_REFERENCE_WITNESS_PASS",
        "authority_ceiling": AUTHORITY_CEILING,
        "owner": COURT_OWNER_ID,
        "executor": COURT_EXECUTOR_ID,
        "owner_contract_hash": owner.owner_contract_hash,
        "positive_chain": [
            "CORRECTED_EVIDENCE",
            "CANDIDATE_NOMINATION",
            "COMPLETE_EVIDENCE_BINDING",
            "FAMILY_SPECIFIC_ADJUDICATION",
            "IMMUTABLE_SEMANTIC_AUTHORITY",
            "TYPED_LIFECYCLE_EVENT_RECERTIFIES",
            "EXPLICIT_CURRENT_SELECT",
            "APPEND_ONLY_GENEALOGY",
            "DESCENDANT_REVALIDATION",
            "SEMANTIC_RELEASE",
            "EXPLICIT_PROMOTION",
            "EXPLICIT_ROLLBACK",
            "EXACT_PREDECESSOR_SUCCESSOR_REPLAY",
        ],
        "predecessor_authority_ref": authority_v1.ref.as_dict(),
        "successor_authority_ref": authority_v2.ref.as_dict(),
        "same_semantic_claim_under_recertification": authority_v1.semantic_claim_id == authority_v2.semantic_claim_id,
        "predecessor_release_ref": release_v1.ref.as_dict(),
        "successor_release_ref": release_v2.ref.as_dict(),
        "current_release_after_rollback": executor.current_release_ref.as_dict() if executor.current_release_ref else None,
        "exact_replay": {
            "predecessor_authority": replay_authority_v1.ref.as_dict(),
            "successor_authority": replay_authority_v2.ref.as_dict(),
            "predecessor_release": replay_release_v1.ref.as_dict(),
            "successor_release": replay_release_v2.ref.as_dict(),
        },
        "journal_record_count": len(owner.journal),
        "release_journal_record_count": len(executor.release_journal),
        "owner_journal_root": semantic_hash(owner.journal),
        "release_journal_root": semantic_hash(executor.release_journal),
        "owner_journal": owner.journal,
        "release_journal": executor.release_journal,
    }


if __name__ == "__main__":
    print(json.dumps(build_authoritative_witness(), indent=2, sort_keys=True))
