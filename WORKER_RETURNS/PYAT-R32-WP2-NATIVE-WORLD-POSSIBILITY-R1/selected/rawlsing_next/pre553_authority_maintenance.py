"""Governed future semantic-authority maintenance lifecycle for PRE553.

Z06 closes the production/correction lifecycle around the existing immutable
AuthoritySnapshot object.  It does not introduce a new public empirical
semantic family, select latest/default authority, or inherit historical C5R2
owner identities.

The executor is deliberately operational: evidence, candidate, adjudication,
seal, release, invalidation and journal records are ref-addressed receipts.
Only an explicitly APPROVED candidate may mint an AuthoritySnapshot.  Current
selection changes only through an exact release receipt.  Historical snapshots
and journal events are append-only and remain exactly replayable.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AUTHORITY_KINDS,
    AuthorityRegistry,
    Pre553AuthorityConflict,
    validate_authority_snapshot,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    CanonicalSemanticObject,
    ExactRef,
    authority_ref,
    canonicalize,
    exact_ref,
    semantic_hash,
)

MAINTENANCE_CONTRACT_ID = "PRE553_AUTH40_SEMANTIC_AUTHORITY_MAINTENANCE@1.0.0"
MAINTENANCE_CHECKPOINT_SCHEMA = "PRE553_AUTH40_SEMANTIC_AUTHORITY_MAINTENANCE_CHECKPOINT@1.0.0"

AUTHORITY_PROPOSAL_STATES = frozenset({"ALLOW", "DENY", "DEFER"})
ADJUDICATION_STATES = frozenset({"APPROVED", "REJECTED", "DEFERRED"})
CORRECTION_KINDS = frozenset({
    "NONE",
    "COLLISION_RESOLUTION",
    "SPLIT",
    "EXCLUSION",
    "BOUNDARY_CORRECTION",
    "ALIAS_CORRECTION",
})
EVENT_KINDS = frozenset({
    "EVIDENCE_RECORDED",
    "CANDIDATE_PROPOSED",
    "CANDIDATE_EVIDENCE_ACCUMULATED",
    "CANDIDATE_ADJUDICATED",
    "REVISION_SEALED",
    "CURRENT_PROMOTED",
    "CURRENT_ROLLED_BACK",
})
_FORBIDDEN_SELECTOR_TOKENS = frozenset({
    "LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER", "SEMVER_FALLBACK", "*",
})

Recompiler = Callable[[ExactRef, tuple[AuthorityRef, ...]], ExactRef]

# --------------------------------------------------------------------------
# Generic negative lifecycle disposition.
#
# Exactly ONE noncurrent disposition exists. It is deliberately generic: it names
# no C1, survey, model, comparability or product vocabulary, and it does not split
# into separate deferred/unavailable/deleted classes, because the lifecycle owner
# has no authority that would distinguish them.
# --------------------------------------------------------------------------
NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT = "NO_CURRENT_NO_LAWFUL_REPLACEMENT"
NONCURRENT_DISPOSITIONS = frozenset({NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT})

# Dependency lifecycle visibility for a registered dependent under the current
# release. This is lifecycle state, never object/cache presence.
DEPENDENT_LIFECYCLE_CURRENT = "CURRENT"
DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT = "EXPLICIT_NONCURRENT"
#: The owner does not know this dependent at all, so no governed transition has ever
#: spoken about it. This is deliberately NOT ``CURRENT``: absence of a governed
#: outcome is absence of authority, not evidence of currentness. A ref the owner has
#: never registered must fail closed rather than inherit a positive claim from the
#: mere absence of a recorded transition.
DEPENDENT_LIFECYCLE_NOT_GOVERNED = "NOT_GOVERNED"

# The negative-row receipt schema. A receipt carrying noncurrent rows uses this
# explicit, separately identified schema; a positive-only receipt keeps the
# original projection byte for byte.
INVALIDATION_RECEIPT_NONCURRENT_SCHEMA = (
    "PRE553_AUTH40_SEMANTIC_AUTHORITY_INVALIDATION_NONCURRENT@1.0.0"
)


class AuthorityMaintenanceError(ValueError):
    """The governed maintenance lifecycle cannot lawfully perform the operation."""


class AuthorityMaintenanceConflict(AuthorityMaintenanceError):
    """An immutable authority identity, revision, or maintenance record conflicts."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AuthorityMaintenanceError(f"{name} must be a non-empty string")
    return value.strip()


def _reject_selector(value: str, name: str) -> str:
    text = _text(value, name)
    upper = text.upper()
    if upper in _FORBIDDEN_SELECTOR_TOKENS:
        raise AuthorityMaintenanceError(
            f"{name} may not use latest/default/fuzzy/nearest selection")
    if upper.startswith(("LATEST:", "DEFAULT:", "FUZZY:", "NEAREST:", "SEMVER:")):
        raise AuthorityMaintenanceError(
            f"{name} may not use mutable/fuzzy selector syntax")
    return text


def _sha(value: Any, name: str) -> str:
    text = _text(value, name)
    if len(text) != 64 or text.lower() != text or any(ch not in "0123456789abcdef" for ch in text):
        raise AuthorityMaintenanceError(f"{name} must be lowercase sha256")
    return text


def _exact_refs(values: Iterable[ExactRef | Mapping[str, Any]]) -> tuple[ExactRef, ...]:
    refs = {exact_ref(value).key: exact_ref(value) for value in values}
    return tuple(refs[key] for key in sorted(refs))


def _authority_refs(values: Iterable[AuthorityRef | Mapping[str, Any]]) -> tuple[AuthorityRef, ...]:
    refs = {authority_ref(value).key: authority_ref(value) for value in values}
    return tuple(refs[key] for key in sorted(refs))


def _optional_exact(value: ExactRef | Mapping[str, Any] | None) -> ExactRef | None:
    return None if value is None else exact_ref(value)


def _optional_authority(value: AuthorityRef | Mapping[str, Any] | None) -> AuthorityRef | None:
    return None if value is None else authority_ref(value)


def _strings(values: Iterable[str], name: str) -> tuple[str, ...]:
    material = {_text(value, name) for value in values}
    return tuple(sorted(material))


def _mapping(value: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise AuthorityMaintenanceError(f"{name} must be a mapping")
    normalized = canonicalize(value)
    if not isinstance(normalized, dict):
        raise AuthorityMaintenanceError(f"{name} did not canonicalize to a mapping")
    return MappingProxyType(normalized)


def _record_ref(kind: str, projection: Mapping[str, Any]) -> ExactRef:
    digest = semantic_hash(projection)
    return ExactRef(
        f"Maintenance:{kind}",
        f"urn:rawlsing:pre553:maintenance:{kind.lower()}:sha256:{digest}",
        digest,
    )


def _ref_dict(value: ExactRef | None) -> Mapping[str, Any] | None:
    return None if value is None else value.as_dict()


def _authority_dict(value: AuthorityRef | None) -> Mapping[str, Any] | None:
    return None if value is None else value.as_dict()


def _validate_embedded_record_ref(data: Mapping[str, Any], ref: ExactRef) -> None:
    supplied = data.get("record_ref")
    if supplied is not None and exact_ref(supplied) != ref:
        raise AuthorityMaintenanceConflict("record_ref does not match deterministic receipt identity")


@dataclass(frozen=True)
class AuthorityEvidenceReceipt:
    evidence_role: str
    evidence_refs: tuple[ExactRef, ...]
    provenance_refs: tuple[ExactRef, ...] = ()
    source_release_refs: tuple[ExactRef, ...] = ()
    parent_evidence_receipt_ref: ExactRef | None = None
    evidence_state: str = "RECORDED"

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_role", _text(self.evidence_role, "evidence_role"))
        object.__setattr__(self, "evidence_refs", _exact_refs(self.evidence_refs))
        object.__setattr__(self, "provenance_refs", _exact_refs(self.provenance_refs))
        object.__setattr__(self, "source_release_refs", _exact_refs(self.source_release_refs))
        object.__setattr__(
            self, "parent_evidence_receipt_ref", _optional_exact(self.parent_evidence_receipt_ref))
        if not self.evidence_refs:
            raise AuthorityMaintenanceError("evidence receipt requires at least one exact evidence ref")
        if self.evidence_state != "RECORDED":
            raise AuthorityMaintenanceError("evidence_state must be RECORDED")

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": MAINTENANCE_CONTRACT_ID,
            "record_type": "AuthorityEvidenceReceipt",
            "evidence_role": self.evidence_role,
            "evidence_refs": [ref.as_dict() for ref in self.evidence_refs],
            "provenance_refs": [ref.as_dict() for ref in self.provenance_refs],
            "source_release_refs": [ref.as_dict() for ref in self.source_release_refs],
            "parent_evidence_receipt_ref": _ref_dict(self.parent_evidence_receipt_ref),
            "evidence_state": self.evidence_state,
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("EVIDENCE", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AuthorityEvidenceReceipt":
        obj = cls(
            evidence_role=data["evidence_role"],
            evidence_refs=tuple(exact_ref(x) for x in data["evidence_refs"]),
            provenance_refs=tuple(exact_ref(x) for x in data.get("provenance_refs", ())),
            source_release_refs=tuple(exact_ref(x) for x in data.get("source_release_refs", ())),
            parent_evidence_receipt_ref=_optional_exact(data.get("parent_evidence_receipt_ref")),
            evidence_state=data.get("evidence_state", "RECORDED"),
        )
        _validate_embedded_record_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class AuthorityCandidate:
    candidate_id: str
    candidate_revision: int
    authority_id: str
    authority_version: str
    authority_kind: str
    proposed_decision_state: str
    governed_operations: tuple[str, ...]
    governed_object_families: tuple[str, ...]
    scope_envelope: Mapping[str, Any]
    effective_time_or_interval: Any
    evidence_receipt_refs: tuple[ExactRef, ...]
    proposed_parent_authority_refs: tuple[AuthorityRef, ...]
    proposed_negative_limit_refs: tuple[AuthorityRef, ...]
    proposed_supersession_refs: tuple[AuthorityRef, ...]
    interpretation_semantics: Mapping[str, Any]
    replay_protocol_ref: ExactRef
    correction_kind: str = "NONE"
    correction_target_refs: tuple[AuthorityRef, ...] = ()
    correction_scope_ref: ExactRef | None = None
    source_onboarding_refs: tuple[ExactRef, ...] = ()
    parent_candidate_ref: ExactRef | None = None
    candidate_state: str = "PROPOSED"

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_id", _text(self.candidate_id, "candidate_id"))
        if not isinstance(self.candidate_revision, int) or isinstance(self.candidate_revision, bool) or self.candidate_revision < 1:
            raise AuthorityMaintenanceError("candidate_revision must be a positive integer")
        object.__setattr__(self, "authority_id", _reject_selector(self.authority_id, "authority_id"))
        object.__setattr__(
            self, "authority_version", _reject_selector(self.authority_version, "authority_version"))
        if self.authority_kind not in AUTHORITY_KINDS:
            raise AuthorityMaintenanceError(f"unknown authority_kind {self.authority_kind!r}")
        if self.proposed_decision_state not in AUTHORITY_PROPOSAL_STATES:
            raise AuthorityMaintenanceError("candidate authority state must be ALLOW/DENY/DEFER")
        object.__setattr__(
            self, "governed_operations", _strings(self.governed_operations, "governed_operation"))
        object.__setattr__(
            self, "governed_object_families",
            _strings(self.governed_object_families, "governed_object_family"))
        if not self.governed_operations:
            raise AuthorityMaintenanceError("candidate must name at least one governed operation")
        if not self.governed_object_families:
            raise AuthorityMaintenanceError("candidate must name at least one governed object family")
        object.__setattr__(self, "scope_envelope", _mapping(self.scope_envelope, "scope_envelope"))
        canonicalize(self.effective_time_or_interval)
        object.__setattr__(
            self, "evidence_receipt_refs", _exact_refs(self.evidence_receipt_refs))
        if not self.evidence_receipt_refs:
            raise AuthorityMaintenanceError("candidate requires governed evidence receipt refs")
        object.__setattr__(
            self, "proposed_parent_authority_refs",
            _authority_refs(self.proposed_parent_authority_refs))
        object.__setattr__(
            self, "proposed_negative_limit_refs",
            _authority_refs(self.proposed_negative_limit_refs))
        object.__setattr__(
            self, "proposed_supersession_refs",
            _authority_refs(self.proposed_supersession_refs))
        object.__setattr__(
            self, "interpretation_semantics",
            _mapping(self.interpretation_semantics, "interpretation_semantics"))
        object.__setattr__(self, "replay_protocol_ref", exact_ref(self.replay_protocol_ref))
        if self.correction_kind not in CORRECTION_KINDS:
            raise AuthorityMaintenanceError("unknown correction_kind")
        object.__setattr__(
            self, "correction_target_refs", _authority_refs(self.correction_target_refs))
        object.__setattr__(self, "correction_scope_ref", _optional_exact(self.correction_scope_ref))
        object.__setattr__(
            self, "source_onboarding_refs", _exact_refs(self.source_onboarding_refs))
        object.__setattr__(self, "parent_candidate_ref", _optional_exact(self.parent_candidate_ref))
        if self.candidate_revision > 1 and self.parent_candidate_ref is None:
            raise AuthorityMaintenanceError("candidate revision after 1 requires exact parent_candidate_ref")
        if self.correction_kind != "NONE" and not self.correction_target_refs:
            raise AuthorityMaintenanceError("correction candidate requires exact correction target refs")
        if self.correction_kind in {"SPLIT", "EXCLUSION", "BOUNDARY_CORRECTION"} and self.correction_scope_ref is None:
            raise AuthorityMaintenanceError(
                f"{self.correction_kind} requires an exact correction_scope_ref")
        if self.candidate_state != "PROPOSED":
            raise AuthorityMaintenanceError("AuthorityCandidate state must remain PROPOSED")

    @property
    def interpretation_semantics_fingerprint(self) -> str:
        return semantic_hash(dict(self.interpretation_semantics))

    def authority_material(self) -> dict[str, Any]:
        return {
            "authority_id": self.authority_id,
            "authority_version": self.authority_version,
            "authority_kind": self.authority_kind,
            "decision_state": self.proposed_decision_state,
            "governed_operations": list(self.governed_operations),
            "governed_object_families": list(self.governed_object_families),
            "scope_envelope": dict(self.scope_envelope),
            "effective_time_or_interval": canonicalize(self.effective_time_or_interval),
            "parent_authority_refs": [ref.as_dict() for ref in self.proposed_parent_authority_refs],
            "negative_limit_refs": [ref.as_dict() for ref in self.proposed_negative_limit_refs],
            "supersession_refs": [ref.as_dict() for ref in self.proposed_supersession_refs],
            "interpretation_semantics_fingerprint": self.interpretation_semantics_fingerprint,
            "replay_protocol_ref": self.replay_protocol_ref.as_dict(),
        }

    @property
    def authority_content_hash(self) -> str:
        return semantic_hash(self.authority_material())

    @property
    def proposed_authority_ref(self) -> AuthorityRef:
        return AuthorityRef(
            self.authority_id, self.authority_version, self.authority_content_hash)

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": MAINTENANCE_CONTRACT_ID,
            "record_type": "AuthorityCandidate",
            "candidate_id": self.candidate_id,
            "candidate_revision": self.candidate_revision,
            "candidate_state": self.candidate_state,
            "authority_material": self.authority_material(),
            "evidence_receipt_refs": [ref.as_dict() for ref in self.evidence_receipt_refs],
            "interpretation_semantics": dict(self.interpretation_semantics),
            "correction_kind": self.correction_kind,
            "correction_target_refs": [ref.as_dict() for ref in self.correction_target_refs],
            "correction_scope_ref": _ref_dict(self.correction_scope_ref),
            "source_onboarding_refs": [ref.as_dict() for ref in self.source_onboarding_refs],
            "parent_candidate_ref": _ref_dict(self.parent_candidate_ref),
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("CANDIDATE", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AuthorityCandidate":
        material = data["authority_material"]
        obj = cls(
            candidate_id=data["candidate_id"],
            candidate_revision=data["candidate_revision"],
            authority_id=material["authority_id"],
            authority_version=material["authority_version"],
            authority_kind=material["authority_kind"],
            proposed_decision_state=material["decision_state"],
            governed_operations=tuple(material["governed_operations"]),
            governed_object_families=tuple(material["governed_object_families"]),
            scope_envelope=material["scope_envelope"],
            effective_time_or_interval=material["effective_time_or_interval"],
            evidence_receipt_refs=tuple(exact_ref(x) for x in data["evidence_receipt_refs"]),
            proposed_parent_authority_refs=tuple(
                authority_ref(x) for x in material["parent_authority_refs"]),
            proposed_negative_limit_refs=tuple(
                authority_ref(x) for x in material["negative_limit_refs"]),
            proposed_supersession_refs=tuple(
                authority_ref(x) for x in material["supersession_refs"]),
            interpretation_semantics=data["interpretation_semantics"],
            replay_protocol_ref=exact_ref(material["replay_protocol_ref"]),
            correction_kind=data.get("correction_kind", "NONE"),
            correction_target_refs=tuple(
                authority_ref(x) for x in data.get("correction_target_refs", ())),
            correction_scope_ref=_optional_exact(data.get("correction_scope_ref")),
            source_onboarding_refs=tuple(
                exact_ref(x) for x in data.get("source_onboarding_refs", ())),
            parent_candidate_ref=_optional_exact(data.get("parent_candidate_ref")),
            candidate_state=data.get("candidate_state", "PROPOSED"),
        )
        if obj.authority_content_hash != material.get(
            "authority_content_hash", obj.authority_content_hash
        ):
            raise AuthorityMaintenanceConflict("candidate authority content hash mismatch")
        _validate_embedded_record_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class AuthorityAdjudicationReceipt:
    candidate_ref: ExactRef
    decision: str
    adjudicator_ref: ExactRef
    adjudication_authority_ref: ExactRef
    evidence_receipt_refs: tuple[ExactRef, ...]
    findings_ref: ExactRef

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_ref", exact_ref(self.candidate_ref))
        if self.decision not in ADJUDICATION_STATES:
            raise AuthorityMaintenanceError("adjudication decision must be APPROVED/REJECTED/DEFERRED")
        object.__setattr__(self, "adjudicator_ref", exact_ref(self.adjudicator_ref))
        object.__setattr__(
            self, "adjudication_authority_ref", exact_ref(self.adjudication_authority_ref))
        object.__setattr__(
            self, "evidence_receipt_refs", _exact_refs(self.evidence_receipt_refs))
        if not self.evidence_receipt_refs:
            raise AuthorityMaintenanceError("adjudication requires exact evidence receipt refs")
        object.__setattr__(self, "findings_ref", exact_ref(self.findings_ref))

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": MAINTENANCE_CONTRACT_ID,
            "record_type": "AuthorityAdjudicationReceipt",
            "candidate_ref": self.candidate_ref.as_dict(),
            "decision": self.decision,
            "adjudicator_ref": self.adjudicator_ref.as_dict(),
            "adjudication_authority_ref": self.adjudication_authority_ref.as_dict(),
            "evidence_receipt_refs": [ref.as_dict() for ref in self.evidence_receipt_refs],
            "findings_ref": self.findings_ref.as_dict(),
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("ADJUDICATION", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AuthorityAdjudicationReceipt":
        obj = cls(
            candidate_ref=exact_ref(data["candidate_ref"]),
            decision=data["decision"],
            adjudicator_ref=exact_ref(data["adjudicator_ref"]),
            adjudication_authority_ref=exact_ref(data["adjudication_authority_ref"]),
            evidence_receipt_refs=tuple(exact_ref(x) for x in data["evidence_receipt_refs"]),
            findings_ref=exact_ref(data["findings_ref"]),
        )
        _validate_embedded_record_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class AuthorityRevisionSealReceipt:
    candidate_ref: ExactRef
    adjudication_ref: ExactRef
    authority_ref: AuthorityRef
    authority_snapshot_ref: ExactRef
    seal_attestation_ref: ExactRef
    parent_authority_refs: tuple[AuthorityRef, ...]
    supersession_refs: tuple[AuthorityRef, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_ref", exact_ref(self.candidate_ref))
        object.__setattr__(self, "adjudication_ref", exact_ref(self.adjudication_ref))
        object.__setattr__(self, "authority_ref", authority_ref(self.authority_ref))
        object.__setattr__(
            self, "authority_snapshot_ref", exact_ref(self.authority_snapshot_ref))
        object.__setattr__(
            self, "seal_attestation_ref", exact_ref(self.seal_attestation_ref))
        object.__setattr__(
            self, "parent_authority_refs", _authority_refs(self.parent_authority_refs))
        object.__setattr__(
            self, "supersession_refs", _authority_refs(self.supersession_refs))

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": MAINTENANCE_CONTRACT_ID,
            "record_type": "AuthorityRevisionSealReceipt",
            "candidate_ref": self.candidate_ref.as_dict(),
            "adjudication_ref": self.adjudication_ref.as_dict(),
            "authority_ref": self.authority_ref.as_dict(),
            "authority_snapshot_ref": self.authority_snapshot_ref.as_dict(),
            "seal_attestation_ref": self.seal_attestation_ref.as_dict(),
            "parent_authority_refs": [ref.as_dict() for ref in self.parent_authority_refs],
            "supersession_refs": [ref.as_dict() for ref in self.supersession_refs],
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("SEAL", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AuthorityRevisionSealReceipt":
        obj = cls(
            candidate_ref=exact_ref(data["candidate_ref"]),
            adjudication_ref=exact_ref(data["adjudication_ref"]),
            authority_ref=authority_ref(data["authority_ref"]),
            authority_snapshot_ref=exact_ref(data["authority_snapshot_ref"]),
            seal_attestation_ref=exact_ref(data["seal_attestation_ref"]),
            parent_authority_refs=tuple(authority_ref(x) for x in data["parent_authority_refs"]),
            supersession_refs=tuple(authority_ref(x) for x in data["supersession_refs"]),
        )
        _validate_embedded_record_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class SemanticDeterminantGraph:
    authority_edges: tuple[tuple[AuthorityRef, ExactRef], ...] = ()
    dependency_edges: tuple[tuple[ExactRef, ExactRef], ...] = ()
    known_dependent_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        aseen: dict[str, tuple[AuthorityRef, ExactRef]] = {}
        for raw_auth, raw_dep in self.authority_edges:
            auth, dep = authority_ref(raw_auth), exact_ref(raw_dep)
            aseen[f"{auth.key}->{dep.key}"] = (auth, dep)
        dseen: dict[str, tuple[ExactRef, ExactRef]] = {}
        for raw_parent, raw_child in self.dependency_edges:
            parent, child = exact_ref(raw_parent), exact_ref(raw_child)
            if parent == child:
                raise AuthorityMaintenanceError("semantic determinant graph may not self-loop")
            dseen[f"{parent.key}->{child.key}"] = (parent, child)
        known = _exact_refs(self.known_dependent_refs)
        all_known = {ref.key: ref for ref in known}
        for _, dep in aseen.values():
            all_known[dep.key] = dep
        for _, child in dseen.values():
            all_known[child.key] = child
        object.__setattr__(
            self, "authority_edges", tuple(aseen[key] for key in sorted(aseen)))
        object.__setattr__(
            self, "dependency_edges", tuple(dseen[key] for key in sorted(dseen)))
        object.__setattr__(
            self, "known_dependent_refs",
            tuple(all_known[key] for key in sorted(all_known)))

    @classmethod
    def from_objects(
        cls, objects: Iterable[CanonicalSemanticObject]
    ) -> "SemanticDeterminantGraph":
        authority_edges: list[tuple[AuthorityRef, ExactRef]] = []
        dependency_edges: list[tuple[ExactRef, ExactRef]] = []
        known: list[ExactRef] = []
        for obj in objects:
            if not isinstance(obj, CanonicalSemanticObject):
                raise AuthorityMaintenanceError(
                    "determinant graph from_objects requires canonical PRE553 objects")
            known.append(obj.ref)
            authority_edges.extend((ref, obj.ref) for ref in obj.authority_snapshot_refs)
            dependency_edges.extend((dep, obj.ref) for dep in obj.dependency_refs)
        return cls(tuple(authority_edges), tuple(dependency_edges), tuple(known))

    def affected(
        self, changed_authority_refs: Iterable[AuthorityRef | Mapping[str, Any]]
    ) -> tuple[ExactRef, ...]:
        changed = {ref.key for ref in _authority_refs(changed_authority_refs)}
        roots = {
            dep.key: dep for auth, dep in self.authority_edges if auth.key in changed
        }
        adjacency: dict[str, list[ExactRef]] = {}
        for parent, child in self.dependency_edges:
            adjacency.setdefault(parent.key, []).append(child)
        affected = dict(roots)
        queue = [roots[key] for key in sorted(roots)]
        while queue:
            parent = queue.pop(0)
            for child in sorted(adjacency.get(parent.key, ()), key=lambda ref: ref.key):
                if child.key not in affected:
                    affected[child.key] = child
                    queue.append(child)
        return tuple(affected[key] for key in sorted(affected))

    def unaffected(
        self, affected_refs: Iterable[ExactRef | Mapping[str, Any]]
    ) -> tuple[ExactRef, ...]:
        affected = {ref.key for ref in _exact_refs(affected_refs)}
        return tuple(ref for ref in self.known_dependent_refs if ref.key not in affected)

    def as_dict(self) -> dict[str, Any]:
        return {
            "authority_edges": [
                {"authority_ref": auth.as_dict(), "dependent_ref": dep.as_dict()}
                for auth, dep in self.authority_edges
            ],
            "dependency_edges": [
                {"parent_ref": parent.as_dict(), "child_ref": child.as_dict()}
                for parent, child in self.dependency_edges
            ],
            "known_dependent_refs": [ref.as_dict() for ref in self.known_dependent_refs],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SemanticDeterminantGraph":
        return cls(
            authority_edges=tuple(
                (authority_ref(row["authority_ref"]), exact_ref(row["dependent_ref"]))
                for row in data.get("authority_edges", ())
            ),
            dependency_edges=tuple(
                (exact_ref(row["parent_ref"]), exact_ref(row["child_ref"]))
                for row in data.get("dependency_edges", ())
            ),
            known_dependent_refs=tuple(
                exact_ref(x) for x in data.get("known_dependent_refs", ())),
        )


@dataclass(frozen=True)
class NoncurrentDependentOutcome:
    """One affected dependent that has no lawful replacement under a new release.

    This is the single generic negative lifecycle disposition. It carries no C1,
    survey, model or product vocabulary, and it never mints a product.

    Meaning, precisely:

    * the historical artifact remains historically addressable;
    * it is **not current** under the new governed authority release;
    * the governing authority is *not* withdrawn merely because this dependent is
      noncurrent.

    ``replacement_ref`` is always ``None``. A noncurrent row may never carry a
    replacement ref; a lawful replacement is a different outcome, not an extra
    field on this one.
    """

    old_ref: ExactRef
    disposition: str
    reason_code: str
    supporting_refs: tuple[ExactRef, ...] = ()
    replacement_ref: None = None

    def __post_init__(self) -> None:
        old = exact_ref(self.old_ref)
        object.__setattr__(self, "old_ref", old)
        if self.disposition != NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT:
            raise AuthorityMaintenanceError(
                "the owner supports exactly one generic noncurrent disposition, "
                f"{NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT!r}; got "
                f"{self.disposition!r}. Separate deferred/unavailable/deleted "
                "semantic classes are not owner vocabulary."
            )
        _reject_selector(_text(self.reason_code, "reason_code"), "reason_code")
        grounds = _exact_refs(self.supporting_refs)
        if not grounds:
            raise AuthorityMaintenanceError(
                "a noncurrent dependent row requires exact supporting evidence or "
                "policy refs as its ground; an ungrounded noncurrent claim is refused"
            )
        object.__setattr__(self, "supporting_refs", grounds)
        if self.replacement_ref is not None:
            raise AuthorityMaintenanceError(
                "a noncurrent dependent row may not carry a replacement ref; the "
                "historical artifact is retained and no new product is current"
            )

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "old_ref": self.old_ref.as_dict(),
            "disposition": self.disposition,
            "reason_code": self.reason_code,
            "supporting_refs": [ref.as_dict() for ref in self.supporting_refs],
            "replacement_ref": None,
        }

    def as_dict(self) -> dict[str, Any]:
        return dict(self.semantic_projection())

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "NoncurrentDependentOutcome":
        # The serialized ``replacement_ref`` is load-bearing negative evidence: its
        # exact null is what asserts "no lawful replacement exists for this
        # dependent". So it must be *stated*, and it must be null. A missing field is
        # never treated as a stated null, and a non-null value is never quietly
        # overwritten with one, because either move would let a serialized row
        # assert something the owner never emitted.
        if "replacement_ref" not in data:
            raise AuthorityMaintenanceError(
                "a serialized noncurrent dependent row must state replacement_ref "
                "explicitly; the owner does not synthesize null for a missing field, "
                "because that null is the row's own evidence that no lawful "
                "replacement exists (C1-03R-OWNER-BLOCK-NEGATIVE-FIELD-001)"
            )
        serialized_replacement = data["replacement_ref"]
        if serialized_replacement is not None:
            raise AuthorityMaintenanceError(
                "a serialized noncurrent dependent row may not carry a replacement "
                f"ref; got {serialized_replacement!r}. A lawful replacement is a "
                "different outcome, not an extra field on this one, so the owner "
                "refuses the row rather than discarding the value "
                "(C1-03R-OWNER-BLOCK-NEGATIVE-FIELD-001)"
            )
        return cls(
            old_ref=exact_ref(data["old_ref"]),
            disposition=_text(data["disposition"], "disposition"),
            reason_code=_text(data["reason_code"], "reason_code"),
            supporting_refs=tuple(exact_ref(x) for x in data.get("supporting_refs", ())),
            replacement_ref=None,
        )


@dataclass(frozen=True)
class AuthorityInvalidationReceipt:
    changed_authority_refs: tuple[AuthorityRef, ...]
    affected_dependent_refs: tuple[ExactRef, ...]
    unaffected_dependent_refs: tuple[ExactRef, ...]
    recompilation_pairs: tuple[tuple[ExactRef, ExactRef], ...]
    noncurrent_dependents: tuple[NoncurrentDependentOutcome, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "changed_authority_refs", _authority_refs(self.changed_authority_refs))
        object.__setattr__(
            self, "affected_dependent_refs", _exact_refs(self.affected_dependent_refs))
        object.__setattr__(
            self, "unaffected_dependent_refs", _exact_refs(self.unaffected_dependent_refs))
        pairs: dict[str, tuple[ExactRef, ExactRef]] = {}
        for raw_old, raw_new in self.recompilation_pairs:
            old, new = exact_ref(raw_old), exact_ref(raw_new)
            if old == new:
                raise AuthorityMaintenanceError(
                    "an affected dependent replacement must be a new exact ref, not "
                    "the old ref")
            # Reject a repeated source row BEFORE the dict assignment below can
            # silently overwrite one. Two rows for one old ref are refused whether
            # their targets agree or differ: with differing targets, last-write-wins
            # would let a caller substitute the owner's replacement successor.
            if old.key in pairs:
                raise AuthorityMaintenanceError(
                    "an affected dependent may carry at most one positive "
                    f"replacement row; duplicate replacement rows for source {old.key} "
                    f"(targets {pairs[old.key][1].key} and {new.key}) are refused "
                    "rather than silently collapsed "
                    "(C1-03R-OWNER-BLOCK-DUPLICATE-REPLACEMENT-001)"
                )
            pairs[old.key] = (old, new)
        rows: dict[str, NoncurrentDependentOutcome] = {}
        for raw in self.noncurrent_dependents:
            row = raw if isinstance(raw, NoncurrentDependentOutcome) else (
                NoncurrentDependentOutcome(**dict(raw)))
            rows[row.old_ref.key] = row
        if len(rows) != len(tuple(self.noncurrent_dependents)):
            raise AuthorityMaintenanceError(
                "a dependent may carry at most one noncurrent outcome")
        affected_keys = {ref.key for ref in self.affected_dependent_refs}
        noncurrent_keys = set(rows)
        # R and N must be disjoint and must together cover A exactly: every affected
        # old ref has exactly one outcome, and no unknown or duplicate source.
        overlap = set(pairs) & noncurrent_keys
        if overlap:
            raise AuthorityMaintenanceError(
                "an affected dependent may not receive both a replacement and a "
                f"noncurrent outcome: {sorted(overlap)}"
            )
        covered = set(pairs) | noncurrent_keys
        missing = affected_keys - covered
        if missing:
            raise AuthorityMaintenanceError(
                "every affected dependent requires exactly one outcome "
                f"(replacement or explicit noncurrent); missing {sorted(missing)}"
            )
        unknown = covered - affected_keys
        if unknown:
            raise AuthorityMaintenanceError(
                f"outcome set names dependents outside the affected set: {sorted(unknown)}"
            )
        if affected_keys & {ref.key for ref in self.unaffected_dependent_refs}:
            raise AuthorityMaintenanceError("affected and unaffected dependent sets overlap")
        object.__setattr__(
            self, "recompilation_pairs", tuple(pairs[key] for key in sorted(pairs)))
        object.__setattr__(
            self, "noncurrent_dependents", tuple(rows[key] for key in sorted(rows)))

    @property
    def preserves_legacy_identity(self) -> bool:
        """True when this receipt keeps the pre-extension positive-only identity.

        A receipt with no noncurrent rows projects exactly the original field set, so
        every historical positive-only receipt hash is reproduced byte for byte. No
        historical hash is ever silently reinterpreted.
        """
        return not self.noncurrent_dependents

    def semantic_projection(self) -> dict[str, Any]:
        projection = {
            "contract_id": MAINTENANCE_CONTRACT_ID,
            "record_type": "AuthorityInvalidationReceipt",
            "changed_authority_refs": [ref.as_dict() for ref in self.changed_authority_refs],
            "affected_dependent_refs": [ref.as_dict() for ref in self.affected_dependent_refs],
            "unaffected_dependent_refs": [ref.as_dict() for ref in self.unaffected_dependent_refs],
            "recompilation_pairs": [
                {"old_ref": old.as_dict(), "new_ref": new.as_dict()}
                for old, new in self.recompilation_pairs
            ],
        }
        if self.preserves_legacy_identity:
            # Byte-identical to the pre-extension projection. Do not add fields here.
            return projection
        return {
            **projection,
            "receipt_schema": INVALIDATION_RECEIPT_NONCURRENT_SCHEMA,
            "noncurrent_dependents": [
                row.semantic_projection() for row in self.noncurrent_dependents
            ],
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("INVALIDATION", self.semantic_projection())

    @property
    def noncurrent_old_refs(self) -> tuple[ExactRef, ...]:
        return tuple(row.old_ref for row in self.noncurrent_dependents)

    @property
    def replacement_old_refs(self) -> tuple[ExactRef, ...]:
        return tuple(old for old, _ in self.recompilation_pairs)

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AuthorityInvalidationReceipt":
        # Compatibility boundary. The owner emits the noncurrent schema only when at
        # least one dependent is noncurrent, and emits nothing at all beyond the
        # historical field set otherwise. So the two shapes are mutually exclusive and
        # a serialized receipt that mixes them is an incompatible reinterpretation,
        # never something to silently accept:
        #
        #   * any declaration of the new schema (the receipt_schema key or the
        #     noncurrent_dependents key) must be complete and exact -- the exact
        #     schema id AND at least one row;
        #   * anything else must be historical positive-only material, which
        #     continues to deserialize under its exact original field set and
        #     therefore reproduces its historical identity byte for byte.
        schema_declared = "receipt_schema" in data
        rows_declared = "noncurrent_dependents" in data
        schema = data.get("receipt_schema")
        rows = data.get("noncurrent_dependents") or ()
        if schema_declared or rows_declared:
            if schema != INVALIDATION_RECEIPT_NONCURRENT_SCHEMA:
                raise AuthorityMaintenanceError(
                    "a serialized invalidation receipt declares noncurrent material "
                    f"but does not carry the exact "
                    f"{INVALIDATION_RECEIPT_NONCURRENT_SCHEMA!r} schema id; got "
                    f"{schema!r}. A missing or forged schema is refused rather than "
                    "inferred (C1-03R-OWNER-BLOCK-SCHEMA-COMPAT-001)"
                )
            if not rows:
                raise AuthorityMaintenanceError(
                    "a serialized invalidation receipt declares the noncurrent schema "
                    "but carries no noncurrent rows; the owner emits "
                    "noncurrent_dependents only when at least one dependent is "
                    "noncurrent, so this is an incompatible reinterpretation of "
                    "positive-only legacy material "
                    "(C1-03R-OWNER-BLOCK-SCHEMA-COMPAT-001)"
                )
        obj = cls(
            changed_authority_refs=tuple(
                authority_ref(x) for x in data["changed_authority_refs"]),
            affected_dependent_refs=tuple(
                exact_ref(x) for x in data["affected_dependent_refs"]),
            unaffected_dependent_refs=tuple(
                exact_ref(x) for x in data["unaffected_dependent_refs"]),
            recompilation_pairs=tuple(
                (exact_ref(row["old_ref"]), exact_ref(row["new_ref"]))
                for row in data["recompilation_pairs"]
            ),
            noncurrent_dependents=tuple(
                NoncurrentDependentOutcome.from_dict(row)
                for row in rows
            ),
        )
        # Belt and braces: the reconstructed rows and the serialized declaration must
        # agree about whether this receipt is a noncurrent-schema receipt at all.
        if bool(obj.noncurrent_dependents) != bool(rows):
            raise AuthorityMaintenanceError(
                "serialized invalidation receipt schema does not match its "
                "reconstructed noncurrent rows "
                "(C1-03R-OWNER-BLOCK-SCHEMA-COMPAT-001)"
            )
        _validate_embedded_record_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class AuthorityReleaseReceipt:
    release_kind: str
    selected_authority_ref: AuthorityRef
    seal_ref: ExactRef
    selection_rule_ref: ExactRef
    selection_attestation_ref: ExactRef
    invalidation_receipt_ref: ExactRef
    previous_current_authority_ref: AuthorityRef | None = None
    prior_lawful_release_ref: ExactRef | None = None
    release_state: str = "CURRENT_SELECTED"

    def __post_init__(self) -> None:
        if self.release_kind not in {"PROMOTION", "ROLLBACK"}:
            raise AuthorityMaintenanceError("release_kind must be PROMOTION or ROLLBACK")
        object.__setattr__(
            self, "selected_authority_ref", authority_ref(self.selected_authority_ref))
        object.__setattr__(self, "seal_ref", exact_ref(self.seal_ref))
        object.__setattr__(self, "selection_rule_ref", exact_ref(self.selection_rule_ref))
        object.__setattr__(
            self, "selection_attestation_ref", exact_ref(self.selection_attestation_ref))
        object.__setattr__(
            self, "invalidation_receipt_ref", exact_ref(self.invalidation_receipt_ref))
        object.__setattr__(
            self, "previous_current_authority_ref",
            _optional_authority(self.previous_current_authority_ref))
        object.__setattr__(
            self, "prior_lawful_release_ref", _optional_exact(self.prior_lawful_release_ref))
        if self.release_kind == "ROLLBACK" and self.prior_lawful_release_ref is None:
            raise AuthorityMaintenanceError("rollback must cite an exact prior lawful release")
        if self.release_state != "CURRENT_SELECTED":
            raise AuthorityMaintenanceError("release_state must be CURRENT_SELECTED")

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": MAINTENANCE_CONTRACT_ID,
            "record_type": "AuthorityReleaseReceipt",
            "release_kind": self.release_kind,
            "release_state": self.release_state,
            "selected_authority_ref": self.selected_authority_ref.as_dict(),
            "seal_ref": self.seal_ref.as_dict(),
            "selection_rule_ref": self.selection_rule_ref.as_dict(),
            "selection_attestation_ref": self.selection_attestation_ref.as_dict(),
            "invalidation_receipt_ref": self.invalidation_receipt_ref.as_dict(),
            "previous_current_authority_ref": _authority_dict(
                self.previous_current_authority_ref),
            "prior_lawful_release_ref": _ref_dict(self.prior_lawful_release_ref),
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("RELEASE", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AuthorityReleaseReceipt":
        obj = cls(
            release_kind=data["release_kind"],
            selected_authority_ref=authority_ref(data["selected_authority_ref"]),
            seal_ref=exact_ref(data["seal_ref"]),
            selection_rule_ref=exact_ref(data["selection_rule_ref"]),
            selection_attestation_ref=exact_ref(data["selection_attestation_ref"]),
            invalidation_receipt_ref=exact_ref(data["invalidation_receipt_ref"]),
            previous_current_authority_ref=_optional_authority(
                data.get("previous_current_authority_ref")),
            prior_lawful_release_ref=_optional_exact(data.get("prior_lawful_release_ref")),
            release_state=data.get("release_state", "CURRENT_SELECTED"),
        )
        _validate_embedded_record_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class MaintenanceEvent:
    sequence_number: int
    event_kind: str
    subject_ref: ExactRef
    parent_event_ref: ExactRef | None
    evidence_refs: tuple[ExactRef, ...] = ()
    adjudication_ref: ExactRef | None = None
    authority_refs: tuple[AuthorityRef, ...] = ()
    dependent_refs: tuple[ExactRef, ...] = ()
    event_state: str = "COMMITTED"

    def __post_init__(self) -> None:
        if not isinstance(self.sequence_number, int) or isinstance(
            self.sequence_number, bool
        ) or self.sequence_number < 1:
            raise AuthorityMaintenanceError("event sequence_number must be positive integer")
        if self.event_kind not in EVENT_KINDS:
            raise AuthorityMaintenanceError("unknown maintenance event kind")
        object.__setattr__(self, "subject_ref", exact_ref(self.subject_ref))
        object.__setattr__(self, "parent_event_ref", _optional_exact(self.parent_event_ref))
        object.__setattr__(self, "evidence_refs", _exact_refs(self.evidence_refs))
        object.__setattr__(self, "adjudication_ref", _optional_exact(self.adjudication_ref))
        object.__setattr__(self, "authority_refs", _authority_refs(self.authority_refs))
        object.__setattr__(self, "dependent_refs", _exact_refs(self.dependent_refs))
        if self.event_state != "COMMITTED":
            raise AuthorityMaintenanceError("event_state must be COMMITTED")

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": MAINTENANCE_CONTRACT_ID,
            "record_type": "MaintenanceEvent",
            "sequence_number": self.sequence_number,
            "event_kind": self.event_kind,
            "subject_ref": self.subject_ref.as_dict(),
            "parent_event_ref": _ref_dict(self.parent_event_ref),
            "evidence_refs": [ref.as_dict() for ref in self.evidence_refs],
            "adjudication_ref": _ref_dict(self.adjudication_ref),
            "authority_refs": [ref.as_dict() for ref in self.authority_refs],
            "dependent_refs": [ref.as_dict() for ref in self.dependent_refs],
            "event_state": self.event_state,
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("EVENT", self.semantic_projection())

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "record_ref": self.ref.as_dict()}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MaintenanceEvent":
        obj = cls(
            sequence_number=data["sequence_number"],
            event_kind=data["event_kind"],
            subject_ref=exact_ref(data["subject_ref"]),
            parent_event_ref=_optional_exact(data.get("parent_event_ref")),
            evidence_refs=tuple(exact_ref(x) for x in data.get("evidence_refs", ())),
            adjudication_ref=_optional_exact(data.get("adjudication_ref")),
            authority_refs=tuple(authority_ref(x) for x in data.get("authority_refs", ())),
            dependent_refs=tuple(exact_ref(x) for x in data.get("dependent_refs", ())),
            event_state=data.get("event_state", "COMMITTED"),
        )
        _validate_embedded_record_ref(data, obj.ref)
        return obj


@dataclass(frozen=True)
class MaintenanceReplayReceipt:
    original_checkpoint_hash: str
    replayed_checkpoint_hash: str
    event_refs: tuple[ExactRef, ...]
    historical_authority_refs: tuple[AuthorityRef, ...]
    current_selection_refs: tuple[AuthorityRef, ...]
    replay_state: str = "REPLAY_VERIFIED"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "original_checkpoint_hash",
            _sha(self.original_checkpoint_hash, "original_checkpoint_hash"))
        object.__setattr__(
            self, "replayed_checkpoint_hash",
            _sha(self.replayed_checkpoint_hash, "replayed_checkpoint_hash"))
        object.__setattr__(self, "event_refs", _exact_refs(self.event_refs))
        object.__setattr__(
            self, "historical_authority_refs", _authority_refs(self.historical_authority_refs))
        object.__setattr__(
            self, "current_selection_refs", _authority_refs(self.current_selection_refs))
        if self.replay_state != "REPLAY_VERIFIED":
            raise AuthorityMaintenanceError("replay_state must be REPLAY_VERIFIED")
        if self.original_checkpoint_hash != self.replayed_checkpoint_hash:
            raise AuthorityMaintenanceConflict("maintenance replay checkpoint hash mismatch")

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "contract_id": MAINTENANCE_CONTRACT_ID,
            "record_type": "MaintenanceReplayReceipt",
            "original_checkpoint_hash": self.original_checkpoint_hash,
            "replayed_checkpoint_hash": self.replayed_checkpoint_hash,
            "event_refs": [ref.as_dict() for ref in self.event_refs],
            "historical_authority_refs": [
                ref.as_dict() for ref in self.historical_authority_refs],
            "current_selection_refs": [ref.as_dict() for ref in self.current_selection_refs],
            "replay_state": self.replay_state,
        }

    @property
    def ref(self) -> ExactRef:
        return _record_ref("REPLAY", self.semantic_projection())


def _snapshot_from_dict(data: Mapping[str, Any]) -> AuthoritySnapshot:
    if data.get("schema_id") != "AuthoritySnapshot":
        raise AuthorityMaintenanceConflict("checkpoint contains non-AuthoritySnapshot object")
    snapshot = AuthoritySnapshot(
        typed_state=data["typed_state"],
        authority_snapshot_refs=tuple(
            authority_ref(x) for x in data.get("authority_snapshot_refs", ())),
        dependency_refs=tuple(exact_ref(x) for x in data.get("dependency_refs", ())),
        producer_replay_locator_or_reference_root=data[
            "producer_replay_locator_or_reference_root"],
        object_id=data.get("object_id"),
        content_hash=data.get("content_hash"),
        **data["semantic_fields"],
    )
    return validate_authority_snapshot(snapshot)


def _snapshot_parent_refs(snapshot: AuthoritySnapshot) -> tuple[AuthorityRef, ...]:
    return _authority_refs(snapshot.parent_authority_refs)


def _snapshot_supersession_refs(snapshot: AuthoritySnapshot) -> tuple[AuthorityRef, ...]:
    return _authority_refs(snapshot.supersession_refs)


class AuthorityMaintenanceExecutor:
    """Append-only governed authority-production/correction executor.

    There is no latest/default/fuzzy lookup.  Existing snapshots are exact
    immutable history.  A current selection is an explicit release pointer.
    """

    def __init__(
        self,
        *,
        initial_snapshots: Iterable[AuthoritySnapshot] = (),
        initial_current_selection: Mapping[str, AuthorityRef | Mapping[str, Any]] | None = None,
        determinant_graph: SemanticDeterminantGraph | None = None,
    ) -> None:
        snapshots = tuple(validate_authority_snapshot(s) for s in initial_snapshots)
        try:
            AuthorityRegistry(snapshots)
        except Pre553AuthorityConflict as exc:
            raise AuthorityMaintenanceConflict(str(exc)) from exc
        self._snapshots: dict[str, AuthoritySnapshot] = {
            snapshot.authority_ref.key: snapshot for snapshot in snapshots
        }
        self._snapshot_exact_refs: dict[str, AuthoritySnapshot] = {
            snapshot.ref.key: snapshot for snapshot in snapshots
        }
        self._initial_snapshot_keys = frozenset(self._snapshots)
        self._initial_current: dict[str, AuthorityRef] = {}
        supplied_current = dict(initial_current_selection or {})
        for raw_id, raw_ref in supplied_current.items():
            authority_id = _reject_selector(raw_id, "initial current authority_id")
            ref = authority_ref(raw_ref)
            if ref.authority_id != authority_id:
                raise AuthorityMaintenanceError("initial current selection authority id mismatch")
            if ref.key not in self._snapshots:
                raise AuthorityMaintenanceError(
                    "initial current selection must reference an exact initial snapshot")
            self._initial_current[authority_id] = ref

        self._current = dict(self._initial_current)
        self._current_release: dict[str, ExactRef] = {}
        self._graph = determinant_graph or SemanticDeterminantGraph()

        self._evidence: dict[str, AuthorityEvidenceReceipt] = {}
        self._candidates: dict[str, AuthorityCandidate] = {}
        self._adjudications: dict[str, AuthorityAdjudicationReceipt] = {}
        self._seals: dict[str, AuthorityRevisionSealReceipt] = {}
        self._invalidations: dict[str, AuthorityInvalidationReceipt] = {}
        self._releases: dict[str, AuthorityReleaseReceipt] = {}
        self._events: list[MaintenanceEvent] = []

    @property
    def determinant_graph(self) -> SemanticDeterminantGraph:
        return self._graph

    @property
    def events(self) -> tuple[MaintenanceEvent, ...]:
        return tuple(self._events)

    @property
    def snapshots(self) -> tuple[AuthoritySnapshot, ...]:
        return tuple(
            self._snapshots[key] for key in sorted(self._snapshots))

    @property
    def current_selection(self) -> Mapping[str, AuthorityRef]:
        return MappingProxyType(dict(sorted(self._current.items())))

    @property
    def current_release_refs(self) -> Mapping[str, ExactRef]:
        return MappingProxyType(dict(sorted(self._current_release.items())))

    def authority_registry(self) -> AuthorityRegistry:
        return AuthorityRegistry(self.snapshots)

    def resolve_historical_exact(
        self, ref: AuthorityRef | Mapping[str, Any]
    ) -> AuthoritySnapshot:
        return self.authority_registry().resolve_exact(ref).snapshot

    def current_selection_receipt_ref(self, authority_id: str) -> ExactRef:
        authority_id = _reject_selector(authority_id, "authority_id")
        receipt = self._current_release.get(authority_id)
        if receipt is None:
            raise AuthorityMaintenanceError(
                "no Z06 current-selection receipt exists for this authority id")
        return receipt

    def resolve_current_exact(
        self, authority_id: str, *, selection_receipt_ref: ExactRef | Mapping[str, Any]
    ) -> AuthoritySnapshot:
        authority_id = _reject_selector(authority_id, "authority_id")
        supplied = exact_ref(selection_receipt_ref)
        expected = self._current_release.get(authority_id)
        if expected is None or supplied != expected:
            raise AuthorityMaintenanceError(
                "current authority resolution requires the exact current-selection receipt")
        return self.resolve_historical_exact(self._current[authority_id])

    def _event(
        self,
        kind: str,
        subject_ref: ExactRef,
        *,
        evidence_refs: Iterable[ExactRef] = (),
        adjudication_ref: ExactRef | None = None,
        authority_refs: Iterable[AuthorityRef] = (),
        dependent_refs: Iterable[ExactRef] = (),
    ) -> MaintenanceEvent:
        return MaintenanceEvent(
            sequence_number=len(self._events) + 1,
            event_kind=kind,
            subject_ref=subject_ref,
            parent_event_ref=self._events[-1].ref if self._events else None,
            evidence_refs=tuple(evidence_refs),
            adjudication_ref=adjudication_ref,
            authority_refs=tuple(authority_refs),
            dependent_refs=tuple(dependent_refs),
        )

    def _append_event(self, event: MaintenanceEvent) -> None:
        expected_parent = self._events[-1].ref if self._events else None
        if event.parent_event_ref != expected_parent or event.sequence_number != len(self._events) + 1:
            raise AuthorityMaintenanceConflict("maintenance event chain is not append-only")
        self._events.append(event)

    def intake_evidence(
        self, receipt: AuthorityEvidenceReceipt
    ) -> AuthorityEvidenceReceipt:
        if not isinstance(receipt, AuthorityEvidenceReceipt):
            raise AuthorityMaintenanceError("expected AuthorityEvidenceReceipt")
        if receipt.parent_evidence_receipt_ref is not None:
            if receipt.parent_evidence_receipt_ref.key not in self._evidence:
                raise AuthorityMaintenanceError("evidence genealogy parent is unavailable")
        existing = self._evidence.get(receipt.ref.key)
        if existing is not None:
            if existing != receipt:
                raise AuthorityMaintenanceConflict("evidence receipt ref collision")
            return existing
        event = self._event(
            "EVIDENCE_RECORDED", receipt.ref, evidence_refs=receipt.evidence_refs)
        self._evidence[receipt.ref.key] = receipt
        self._append_event(event)
        return receipt

    def record_evidence(
        self,
        *,
        evidence_role: str,
        evidence_refs: Iterable[ExactRef],
        provenance_refs: Iterable[ExactRef] = (),
        source_release_refs: Iterable[ExactRef] = (),
        parent_evidence_receipt_ref: ExactRef | None = None,
    ) -> AuthorityEvidenceReceipt:
        return self.intake_evidence(AuthorityEvidenceReceipt(
            evidence_role=evidence_role,
            evidence_refs=tuple(evidence_refs),
            provenance_refs=tuple(provenance_refs),
            source_release_refs=tuple(source_release_refs),
            parent_evidence_receipt_ref=parent_evidence_receipt_ref,
        ))

    def _known_authority_ref(self, ref: AuthorityRef) -> bool:
        return ref.key in self._snapshots

    def _assert_candidate_links(self, candidate: AuthorityCandidate) -> None:
        for ref in candidate.evidence_receipt_refs:
            if ref.key not in self._evidence:
                raise AuthorityMaintenanceError("candidate cites unavailable evidence receipt")
        if candidate.parent_candidate_ref is not None:
            if candidate.parent_candidate_ref.key not in self._candidates:
                raise AuthorityMaintenanceError("candidate genealogy parent is unavailable")
        for ref in candidate.proposed_parent_authority_refs:
            if not self._known_authority_ref(ref):
                raise AuthorityMaintenanceError("candidate parent authority is unavailable")
        for ref in candidate.proposed_supersession_refs:
            if not self._known_authority_ref(ref):
                raise AuthorityMaintenanceError("candidate supersession authority is unavailable")
        for ref in candidate.correction_target_refs:
            if not self._known_authority_ref(ref):
                raise AuthorityMaintenanceError("correction target authority is unavailable")
        if candidate.correction_kind != "NONE":
            genealogy = {
                ref.key for ref in (
                    candidate.proposed_parent_authority_refs
                    + candidate.proposed_supersession_refs
                )
            }
            missing = [ref.key for ref in candidate.correction_target_refs if ref.key not in genealogy]
            if missing:
                raise AuthorityMaintenanceError(
                    "correction targets must be explicit parent or supersession genealogy")

    def intake_candidate(
        self, candidate: AuthorityCandidate, *, accumulated: bool = False
    ) -> AuthorityCandidate:
        if not isinstance(candidate, AuthorityCandidate):
            raise AuthorityMaintenanceError("expected AuthorityCandidate")
        self._assert_candidate_links(candidate)

        same_id = [
            snapshot for snapshot in self._snapshots.values()
            if snapshot.authority_id == candidate.authority_id
        ]
        if same_id:
            if not candidate.proposed_parent_authority_refs:
                raise AuthorityMaintenanceError(
                    "revision of an existing authority requires an exact parent authority ref")
            if not any(
                parent.authority_id == candidate.authority_id
                for parent in candidate.proposed_parent_authority_refs
            ):
                raise AuthorityMaintenanceError(
                    "revision must retain same-authority genealogy to an exact parent")

        for snapshot in same_id:
            if snapshot.authority_version == candidate.authority_version:
                if snapshot.authority_content_hash != candidate.authority_content_hash:
                    raise AuthorityMaintenanceConflict(
                        "same authority id/version proposed with conflicting immutable content")
                raise AuthorityMaintenanceConflict(
                    "authority id/version is already sealed; mint an explicit new revision")

        existing = self._candidates.get(candidate.ref.key)
        if existing is not None:
            if existing != candidate:
                raise AuthorityMaintenanceConflict("candidate ref collision")
            return existing

        kind = "CANDIDATE_EVIDENCE_ACCUMULATED" if accumulated else "CANDIDATE_PROPOSED"
        event = self._event(
            kind,
            candidate.ref,
            evidence_refs=candidate.evidence_receipt_refs,
            authority_refs=(
                candidate.proposed_parent_authority_refs
                + candidate.proposed_supersession_refs
            ),
        )
        self._candidates[candidate.ref.key] = candidate
        self._append_event(event)
        return candidate

    def accumulate_candidate_evidence(
        self,
        candidate_ref: ExactRef | Mapping[str, Any],
        evidence_receipt_ref: ExactRef | Mapping[str, Any],
    ) -> AuthorityCandidate:
        candidate = self._candidate(candidate_ref)
        if self._terminal_adjudication(candidate.ref) is not None:
            raise AuthorityMaintenanceError(
                "terminally adjudicated candidate requires a new candidate lineage")
        evidence = exact_ref(evidence_receipt_ref)
        if evidence.key not in self._evidence:
            raise AuthorityMaintenanceError("new evidence receipt is unavailable")
        new_refs = _exact_refs(candidate.evidence_receipt_refs + (evidence,))
        if new_refs == candidate.evidence_receipt_refs:
            raise AuthorityMaintenanceError("candidate already cites this evidence receipt")
        revised = replace(
            candidate,
            candidate_revision=candidate.candidate_revision + 1,
            evidence_receipt_refs=new_refs,
            parent_candidate_ref=candidate.ref,
        )
        return self.intake_candidate(revised, accumulated=True)

    def propose_source_onboarding_candidate(
        self,
        *,
        source_release_ref: ExactRef,
        source_semantic_evidence_refs: Iterable[ExactRef],
        candidate_id: str,
        authority_id: str,
        authority_version: str,
        authority_kind: str,
        proposed_decision_state: str,
        governed_operations: Iterable[str],
        governed_object_families: Iterable[str],
        scope_envelope: Mapping[str, Any],
        effective_time_or_interval: Any,
        interpretation_semantics: Mapping[str, Any],
        replay_protocol_ref: ExactRef,
        proposed_parent_authority_refs: Iterable[AuthorityRef] = (),
        proposed_negative_limit_refs: Iterable[AuthorityRef] = (),
        proposed_supersession_refs: Iterable[AuthorityRef] = (),
        correction_kind: str = "NONE",
        correction_target_refs: Iterable[AuthorityRef] = (),
        correction_scope_ref: ExactRef | None = None,
    ) -> tuple[AuthorityEvidenceReceipt, AuthorityCandidate]:
        source_release_ref = exact_ref(source_release_ref)
        evidence = self.record_evidence(
            evidence_role="SOURCE_ONBOARDING_SEMANTIC_AUTHORITY_EVIDENCE",
            evidence_refs=tuple(source_semantic_evidence_refs),
            source_release_refs=(source_release_ref,),
        )
        candidate = AuthorityCandidate(
            candidate_id=candidate_id,
            candidate_revision=1,
            authority_id=authority_id,
            authority_version=authority_version,
            authority_kind=authority_kind,
            proposed_decision_state=proposed_decision_state,
            governed_operations=tuple(governed_operations),
            governed_object_families=tuple(governed_object_families),
            scope_envelope=scope_envelope,
            effective_time_or_interval=effective_time_or_interval,
            evidence_receipt_refs=(evidence.ref,),
            proposed_parent_authority_refs=tuple(proposed_parent_authority_refs),
            proposed_negative_limit_refs=tuple(proposed_negative_limit_refs),
            proposed_supersession_refs=tuple(proposed_supersession_refs),
            interpretation_semantics=interpretation_semantics,
            replay_protocol_ref=replay_protocol_ref,
            correction_kind=correction_kind,
            correction_target_refs=tuple(correction_target_refs),
            correction_scope_ref=correction_scope_ref,
            source_onboarding_refs=(source_release_ref,),
        )
        return evidence, self.intake_candidate(candidate)

    def _candidate(self, ref: ExactRef | Mapping[str, Any]) -> AuthorityCandidate:
        exact = exact_ref(ref)
        candidate = self._candidates.get(exact.key)
        if candidate is None:
            raise AuthorityMaintenanceError("exact maintenance candidate is unavailable")
        return candidate

    def _adjudication(
        self, ref: ExactRef | Mapping[str, Any]
    ) -> AuthorityAdjudicationReceipt:
        exact = exact_ref(ref)
        receipt = self._adjudications.get(exact.key)
        if receipt is None:
            raise AuthorityMaintenanceError("exact adjudication receipt is unavailable")
        return receipt

    def _seal(self, ref: ExactRef | Mapping[str, Any]) -> AuthorityRevisionSealReceipt:
        exact = exact_ref(ref)
        receipt = self._seals.get(exact.key)
        if receipt is None:
            raise AuthorityMaintenanceError("exact seal receipt is unavailable")
        return receipt

    def _release(self, ref: ExactRef | Mapping[str, Any]) -> AuthorityReleaseReceipt:
        exact = exact_ref(ref)
        receipt = self._releases.get(exact.key)
        if receipt is None:
            raise AuthorityMaintenanceError("exact release receipt is unavailable")
        return receipt

    def _terminal_adjudication(
        self, candidate_ref: ExactRef
    ) -> AuthorityAdjudicationReceipt | None:
        receipts = [
            receipt for receipt in self._adjudications.values()
            if receipt.candidate_ref == candidate_ref and receipt.decision in {"APPROVED", "REJECTED"}
        ]
        if len(receipts) > 1:
            raise AuthorityMaintenanceConflict("candidate has conflicting terminal adjudications")
        return receipts[0] if receipts else None

    def candidate_status(self, candidate_ref: ExactRef | Mapping[str, Any]) -> str:
        candidate = self._candidate(candidate_ref)
        terminal = self._terminal_adjudication(candidate.ref)
        if terminal is not None:
            return terminal.decision
        deferred = any(
            receipt.candidate_ref == candidate.ref and receipt.decision == "DEFERRED"
            for receipt in self._adjudications.values()
        )
        return "DEFERRED" if deferred else "PROPOSED"

    def adjudicate_candidate(
        self,
        candidate_ref: ExactRef | Mapping[str, Any],
        *,
        decision: str,
        adjudicator_ref: ExactRef,
        adjudication_authority_ref: ExactRef,
        findings_ref: ExactRef,
        evidence_receipt_refs: Iterable[ExactRef] | None = None,
    ) -> AuthorityAdjudicationReceipt:
        candidate = self._candidate(candidate_ref)
        terminal = self._terminal_adjudication(candidate.ref)
        if terminal is not None:
            raise AuthorityMaintenanceError(
                "terminal adjudication already exists; correction requires a new candidate lineage")
        cited = _exact_refs(
            candidate.evidence_receipt_refs
            if evidence_receipt_refs is None
            else evidence_receipt_refs
        )
        candidate_evidence = {ref.key for ref in candidate.evidence_receipt_refs}
        if not cited or any(ref.key not in candidate_evidence for ref in cited):
            raise AuthorityMaintenanceError(
                "adjudication evidence must be an exact subset of candidate evidence receipts")
        if decision == "APPROVED" and {ref.key for ref in cited} != candidate_evidence:
            raise AuthorityMaintenanceError(
                "positive adjudication must inspect the complete candidate evidence receipt set")
        receipt = AuthorityAdjudicationReceipt(
            candidate_ref=candidate.ref,
            decision=decision,
            adjudicator_ref=adjudicator_ref,
            adjudication_authority_ref=adjudication_authority_ref,
            evidence_receipt_refs=cited,
            findings_ref=findings_ref,
        )
        event = self._event(
            "CANDIDATE_ADJUDICATED",
            receipt.ref,
            evidence_refs=receipt.evidence_receipt_refs,
            adjudication_ref=receipt.ref,
        )
        self._adjudications[receipt.ref.key] = receipt
        self._append_event(event)
        return receipt

    def _assert_snapshot_can_register(self, snapshot: AuthoritySnapshot) -> None:
        for existing in self._snapshots.values():
            if (
                existing.authority_id == snapshot.authority_id
                and existing.authority_version == snapshot.authority_version
            ):
                if existing.authority_content_hash != snapshot.authority_content_hash:
                    raise AuthorityMaintenanceConflict(
                        "same authority id/version has conflicting immutable content")
                if existing != snapshot:
                    raise AuthorityMaintenanceConflict(
                        "same exact authority ref cannot carry different genealogy/evidence")
                raise AuthorityMaintenanceConflict(
                    "authority revision is already sealed; immutable history cannot be reminted")
        try:
            AuthorityRegistry((*self._snapshots.values(), snapshot))
        except Pre553AuthorityConflict as exc:
            raise AuthorityMaintenanceConflict(str(exc)) from exc

    def seal_revision(
        self,
        candidate_ref: ExactRef | Mapping[str, Any],
        adjudication_ref: ExactRef | Mapping[str, Any],
        *,
        seal_attestation_ref: ExactRef,
    ) -> AuthorityRevisionSealReceipt:
        candidate = self._candidate(candidate_ref)
        adjudication = self._adjudication(adjudication_ref)
        if adjudication.candidate_ref != candidate.ref:
            raise AuthorityMaintenanceError("adjudication does not belong to candidate")
        if adjudication.decision != "APPROVED":
            raise AuthorityMaintenanceError(
                "only explicit APPROVED adjudication may mint an authority revision")
        terminal = self._terminal_adjudication(candidate.ref)
        if terminal != adjudication:
            raise AuthorityMaintenanceConflict("candidate terminal adjudication is inconsistent")
        seal_attestation_ref = exact_ref(seal_attestation_ref)
        snapshot = AuthoritySnapshot(
            typed_state=candidate.proposed_decision_state,
            authority_snapshot_refs=(),
            dependency_refs=_exact_refs(
                candidate.evidence_receipt_refs
                + (candidate.ref, adjudication.ref, seal_attestation_ref)
            ),
            producer_replay_locator_or_reference_root=seal_attestation_ref,
            authority_id=candidate.authority_id,
            authority_version=candidate.authority_version,
            authority_content_hash=candidate.authority_content_hash,
            authority_kind=candidate.authority_kind,
            decision_state=candidate.proposed_decision_state,
            governed_operations=candidate.governed_operations,
            governed_object_families=candidate.governed_object_families,
            scope_envelope=dict(candidate.scope_envelope),
            effective_time_or_interval=candidate.effective_time_or_interval,
            parent_authority_refs=candidate.proposed_parent_authority_refs,
            negative_limit_refs=candidate.proposed_negative_limit_refs,
            supersession_refs=candidate.proposed_supersession_refs,
            interpretation_semantics_fingerprint=candidate.interpretation_semantics_fingerprint,
            replay_protocol_ref=candidate.replay_protocol_ref,
        )
        snapshot = validate_authority_snapshot(snapshot)
        if snapshot.authority_ref != candidate.proposed_authority_ref:
            raise AuthorityMaintenanceConflict(
                "sealed authority ref differs from adjudicated candidate authority ref")
        self._assert_snapshot_can_register(snapshot)
        receipt = AuthorityRevisionSealReceipt(
            candidate_ref=candidate.ref,
            adjudication_ref=adjudication.ref,
            authority_ref=snapshot.authority_ref,
            authority_snapshot_ref=snapshot.ref,
            seal_attestation_ref=seal_attestation_ref,
            parent_authority_refs=candidate.proposed_parent_authority_refs,
            supersession_refs=candidate.proposed_supersession_refs,
        )
        event = self._event(
            "REVISION_SEALED",
            receipt.ref,
            evidence_refs=candidate.evidence_receipt_refs,
            adjudication_ref=adjudication.ref,
            authority_refs=(snapshot.authority_ref,),
        )
        self._snapshots[snapshot.authority_ref.key] = snapshot
        self._snapshot_exact_refs[snapshot.ref.key] = snapshot
        self._seals[receipt.ref.key] = receipt
        self._append_event(event)
        return receipt

    def _snapshot_for_seal(
        self, seal: AuthorityRevisionSealReceipt
    ) -> AuthoritySnapshot:
        snapshot = self._snapshots.get(seal.authority_ref.key)
        if snapshot is None or snapshot.ref != seal.authority_snapshot_ref:
            raise AuthorityMaintenanceConflict("seal does not resolve to exact immutable snapshot")
        return snapshot

    def _recompile(
        self,
        *,
        changed_authority_refs: tuple[AuthorityRef, ...],
        recompiler: Recompiler | None,
        noncurrent_outcomes: Mapping[Any, Any] | None = None,
    ) -> AuthorityInvalidationReceipt:
        """Compute every affected dependent's single outcome.

        The owner alone computes the affected set and validates the outcome set. The
        domain adapter supplies either a recompiler or an explicit, grounded
        noncurrent outcome per affected dependent -- it never computes affected or
        unaffected, and never builds this receipt.

        Errors are NOT converted into noncurrent outcomes. A missing recompiler, a
        recompiler exception, an unchanged-ref return, or a noncurrent row for a
        dependent the owner did not mark affected all remain errors. Only an
        explicitly supplied, grounded noncurrent row may record absence.
        """
        affected = self._graph.affected(changed_authority_refs)
        unaffected = self._graph.unaffected(affected)
        affected_keys = {ref.key for ref in affected}
        supplied: dict[str, NoncurrentDependentOutcome] = {}
        for raw_key, raw_row in dict(noncurrent_outcomes or {}).items():
            key = raw_key if isinstance(raw_key, str) else exact_ref(raw_key).key
            row = raw_row if isinstance(raw_row, NoncurrentDependentOutcome) else (
                NoncurrentDependentOutcome(**dict(raw_row)))
            if row.old_ref.key != key:
                raise AuthorityMaintenanceError(
                    "a supplied noncurrent outcome must name the dependent it is keyed by")
            if key not in affected_keys:
                raise AuthorityMaintenanceError(
                    "a noncurrent outcome may only be recorded for a dependent the "
                    f"owner computed as affected; {key} is not affected"
                )
            if key in supplied:
                raise AuthorityMaintenanceError(
                    f"duplicate noncurrent outcome for {key}")
            supplied[key] = row

        if affected and recompiler is None and len(supplied) != len(affected):
            raise AuthorityMaintenanceError(
                "affected dependents require an explicit deterministic recompiler or an "
                "explicit grounded noncurrent outcome; a missing callback is an error, "
                "not proof that no lawful replacement exists")
        pairs: list[tuple[ExactRef, ExactRef]] = []
        recomposed: set[str] = set()
        if recompiler is not None:
            for old_ref in affected:
                if old_ref.key in supplied:
                    # The adapter already recorded an explicit absence for this
                    # dependent; do not also invoke a recomposition for it.
                    continue
                new_ref = exact_ref(recompiler(old_ref, changed_authority_refs))
                if new_ref == old_ref:
                    # An unchanged-ref return is an ERROR, never a silent noncurrent.
                    raise AuthorityMaintenanceError(
                        "affected dependent recompilation must produce a new exact ref; "
                        "an unchanged ref does not prove absence of a lawful replacement")
                pairs.append((old_ref, new_ref))
                recomposed.add(old_ref.key)
        overlap = recomposed & set(supplied)
        if overlap:
            raise AuthorityMaintenanceError(
                f"dependents may not receive both a replacement and noncurrent: {sorted(overlap)}")
        receipt = AuthorityInvalidationReceipt(
            changed_authority_refs=changed_authority_refs,
            affected_dependent_refs=affected,
            unaffected_dependent_refs=unaffected,
            recompilation_pairs=tuple(pairs),
            noncurrent_dependents=tuple(supplied[key] for key in sorted(supplied)),
        )
        if {ref.key for ref in receipt.affected_dependent_refs} != (
            recomposed | set(supplied)
        ):
            raise AuthorityMaintenanceError(
                "every affected dependent requires exactly one outcome")
        return receipt

    def dependent_lifecycle_status(
        self, dependent_ref: ExactRef | Mapping[str, Any]
    ) -> Mapping[str, Any]:
        """Owner-owned lifecycle visibility for one dependent under the newest release.

        Lifecycle currentness comes from the owner's recorded outcome, never from
        object or cache presence. The historical exact artifact stays addressable
        through :meth:`resolve_historical_exact`.

        Approval law, in order:

        * known explicit noncurrent -> typed noncurrent refusal;
        * known replacement          -> CURRENT, naming the exact replacement;
        * known unaffected           -> CURRENT, identity stable;
        * known, no governing release-> ``NOT_GOVERNED`` (fail closed);
        * **owner-unknown**          -> ``NOT_GOVERNED``, never ``CURRENT``.

        Both fail-closed cases matter. CURRENT requires a governing release/outcome:
        it may never be inferred from membership in ``known_dependent_refs``, from
        cache/object/evidence residency, or from the mere absence of a transition.

        After any real release the owner computes ``A`` and ``U`` over the same graph
        grain, so ``A`` and ``U`` cover every known dependent. A known dependent with
        no covering release is therefore reachable only in the zero-release state --
        exactly where no release has established currentness -- so it is
        ``NOT_GOVERNED`` rather than CURRENT.
        """
        ref = exact_ref(dependent_ref)
        # Releases are recorded in transition order, so the last governing release that
        # mentions this dependent is the one whose outcome law applies.
        latest: AuthorityInvalidationReceipt | None = None
        latest_release: AuthorityReleaseReceipt | None = None
        for release in self._releases.values():
            receipt = self._invalidations.get(release.invalidation_receipt_ref.key)
            if receipt is None:
                raise AuthorityMaintenanceConflict(
                    "release invalidation receipt is unavailable")
            touches = ref.key in {r.key for r in receipt.affected_dependent_refs} or (
                ref.key in {r.key for r in receipt.unaffected_dependent_refs})
            if touches:
                latest, latest_release = receipt, release
        if latest is None:
            # Owner knowledge is the determinant graph's own declared dependent set,
            # never cache or object presence.
            if ref.key not in {r.key for r in self._graph.known_dependent_refs}:
                return {
                    "dependent_ref": ref,
                    "lifecycle_state": DEPENDENT_LIFECYCLE_NOT_GOVERNED,
                    "reason": (
                        "this ref is absent from the owner's known dependent set, so "
                        "no governed transition has ever spoken about it; the owner "
                        "has no currentness to report and will not infer one from "
                        "the absence of a recorded outcome"
                    ),
                    "disposition": None,
                    "reason_code": "OWNER_UNKNOWN_DEPENDENT",
                    "supporting_refs": (),
                    "governing_release_ref": None,
                }
            return {
                "dependent_ref": ref,
                "lifecycle_state": DEPENDENT_LIFECYCLE_NOT_GOVERNED,
                "reason": (
                    "this dependent is registered with the owner, but no governing "
                    "release has established currentness for it. CURRENT requires a "
                    "governing release and recorded outcome; it is never inferred from "
                    "membership in known_dependent_refs, from cache/object/evidence "
                    "residency, or from the absence of a transition"
                ),
                "disposition": None,
                "reason_code": "NO_GOVERNING_RELEASE",
                "supporting_refs": (),
                "governing_release_ref": None,
            }
        assert latest_release is not None
        row = next(
            (r for r in latest.noncurrent_dependents if r.old_ref.key == ref.key), None)
        if row is not None:
            return {
                "dependent_ref": ref,
                "lifecycle_state": DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT,
                "reason": (
                    "the lifecycle owner recorded an explicit noncurrent outcome under "
                    "the governing release; no product is current for this dependent"),
                "disposition": row.disposition,
                "reason_code": row.reason_code,
                "supporting_refs": row.supporting_refs,
                "governing_release_ref": latest_release.ref,
            }
        pair = next((p for p in latest.recompilation_pairs if p[0].key == ref.key), None)
        if pair is not None:
            return {
                "dependent_ref": ref,
                "lifecycle_state": DEPENDENT_LIFECYCLE_CURRENT,
                "reason": "a lawful replacement is current for this dependent",
                "disposition": None,
                "reason_code": None,
                "supporting_refs": (),
                "governing_release_ref": latest_release.ref,
                "current_replacement_ref": pair[1],
            }
        if ref.key in {r.key for r in latest.unaffected_dependent_refs}:
            return {
                "dependent_ref": ref,
                "lifecycle_state": DEPENDENT_LIFECYCLE_CURRENT,
                "reason": "unaffected by the governing transition; identity is stable",
                "disposition": None,
                "reason_code": None,
                "supporting_refs": (),
                "governing_release_ref": latest_release.ref,
            }
        raise AuthorityMaintenanceConflict(
            "dependent has no recorded outcome in the governing invalidation receipt")

    def promote_current(
        self,
        seal_ref: ExactRef | Mapping[str, Any],
        *,
        selection_rule_ref: ExactRef,
        selection_attestation_ref: ExactRef,
        recompiler: Recompiler | None = None,
        noncurrent_outcomes: Mapping[Any, Any] | None = None,
    ) -> AuthorityReleaseReceipt:
        seal = self._seal(seal_ref)
        snapshot = self._snapshot_for_seal(seal)
        candidate = self._candidate(seal.candidate_ref)
        adjudication = self._adjudication(seal.adjudication_ref)
        if adjudication.decision != "APPROVED":
            raise AuthorityMaintenanceError("positive promotion requires APPROVED adjudication")
        previous = self._current.get(snapshot.authority_id)
        if previous == snapshot.authority_ref:
            raise AuthorityMaintenanceError("exact authority revision is already current")
        if previous is not None:
            parents = {ref.key for ref in _snapshot_parent_refs(snapshot)}
            superseded = {ref.key for ref in _snapshot_supersession_refs(snapshot)}
            if previous.key not in parents or previous.key not in superseded:
                raise AuthorityMaintenanceError(
                    "promotion over current authority requires exact parent and supersession refs")
        changed = _authority_refs(
            (() if previous is None else (previous,)) + (snapshot.authority_ref,))
        invalidation = self._recompile(
            changed_authority_refs=changed, recompiler=recompiler,
            noncurrent_outcomes=noncurrent_outcomes)
        release = AuthorityReleaseReceipt(
            release_kind="PROMOTION",
            selected_authority_ref=snapshot.authority_ref,
            seal_ref=seal.ref,
            selection_rule_ref=selection_rule_ref,
            selection_attestation_ref=selection_attestation_ref,
            invalidation_receipt_ref=invalidation.ref,
            previous_current_authority_ref=previous,
        )
        event = self._event(
            "CURRENT_PROMOTED",
            release.ref,
            evidence_refs=candidate.evidence_receipt_refs,
            adjudication_ref=adjudication.ref,
            authority_refs=changed,
            dependent_refs=invalidation.affected_dependent_refs,
        )
        self._invalidations[invalidation.ref.key] = invalidation
        self._releases[release.ref.key] = release
        self._current[snapshot.authority_id] = snapshot.authority_ref
        self._current_release[snapshot.authority_id] = release.ref
        self._append_event(event)
        return release

    def rollback_current(
        self,
        authority_id: str,
        *,
        target_prior_release_ref: ExactRef | Mapping[str, Any],
        rollback_rule_ref: ExactRef,
        rollback_attestation_ref: ExactRef,
        recompiler: Recompiler | None = None,
        noncurrent_outcomes: Mapping[Any, Any] | None = None,
    ) -> AuthorityReleaseReceipt:
        authority_id = _reject_selector(authority_id, "authority_id")
        current = self._current.get(authority_id)
        if current is None:
            raise AuthorityMaintenanceError("cannot rollback an authority with no current selection")
        prior_release = self._release(target_prior_release_ref)
        target = prior_release.selected_authority_ref
        if target.authority_id != authority_id:
            raise AuthorityMaintenanceError("rollback target release belongs to another authority id")
        if target == current:
            raise AuthorityMaintenanceError("rollback target is already current")
        if target.key not in self._snapshots:
            raise AuthorityMaintenanceConflict("rollback target historical snapshot is unavailable")
        target_seal = self._seal(prior_release.seal_ref)
        if target_seal.authority_ref != target:
            raise AuthorityMaintenanceConflict("prior release does not bind its exact seal")
        changed = _authority_refs((current, target))
        invalidation = self._recompile(
            changed_authority_refs=changed, recompiler=recompiler,
            noncurrent_outcomes=noncurrent_outcomes)
        release = AuthorityReleaseReceipt(
            release_kind="ROLLBACK",
            selected_authority_ref=target,
            seal_ref=target_seal.ref,
            selection_rule_ref=rollback_rule_ref,
            selection_attestation_ref=rollback_attestation_ref,
            invalidation_receipt_ref=invalidation.ref,
            previous_current_authority_ref=current,
            prior_lawful_release_ref=prior_release.ref,
        )
        event = self._event(
            "CURRENT_ROLLED_BACK",
            release.ref,
            authority_refs=changed,
            dependent_refs=invalidation.affected_dependent_refs,
        )
        self._invalidations[invalidation.ref.key] = invalidation
        self._releases[release.ref.key] = release
        self._current[authority_id] = target
        self._current_release[authority_id] = release.ref
        self._append_event(event)
        return release

    def invalidation_receipt_for_release(
        self, release_ref: ExactRef | Mapping[str, Any]
    ) -> AuthorityInvalidationReceipt:
        release = self._release(release_ref)
        receipt = self._invalidations.get(release.invalidation_receipt_ref.key)
        if receipt is None:
            raise AuthorityMaintenanceConflict("release invalidation receipt is unavailable")
        return receipt

    def _checkpoint_payload(self) -> dict[str, Any]:
        initial_refs = [
            self._snapshots[key].authority_ref.as_dict()
            for key in sorted(self._initial_snapshot_keys)
        ]
        return {
            "schema": MAINTENANCE_CHECKPOINT_SCHEMA,
            "contract_id": MAINTENANCE_CONTRACT_ID,
            "initial_snapshot_refs": initial_refs,
            "initial_current_selection": [
                {"authority_id": aid, "authority_ref": ref.as_dict()}
                for aid, ref in sorted(self._initial_current.items())
            ],
            "all_snapshots": [
                snapshot.as_dict()
                for snapshot in sorted(self._snapshots.values(), key=lambda x: x.authority_ref.key)
            ],
            "evidence_receipts": [
                self._evidence[key].as_dict() for key in sorted(self._evidence)
            ],
            "candidates": [
                self._candidates[key].as_dict() for key in sorted(self._candidates)
            ],
            "adjudications": [
                self._adjudications[key].as_dict() for key in sorted(self._adjudications)
            ],
            "seals": [self._seals[key].as_dict() for key in sorted(self._seals)],
            "invalidations": [
                self._invalidations[key].as_dict() for key in sorted(self._invalidations)
            ],
            "releases": [self._releases[key].as_dict() for key in sorted(self._releases)],
            "events": [event.as_dict() for event in self._events],
            "determinant_graph": self._graph.as_dict(),
            "current_selection": [
                {"authority_id": aid, "authority_ref": ref.as_dict()}
                for aid, ref in sorted(self._current.items())
            ],
            "current_release_refs": [
                {"authority_id": aid, "release_ref": ref.as_dict()}
                for aid, ref in sorted(self._current_release.items())
            ],
        }

    def export_checkpoint(self) -> dict[str, Any]:
        payload = self._checkpoint_payload()
        return {
            "checkpoint_payload": payload,
            "checkpoint_hash": semantic_hash(payload),
        }

    @classmethod
    def from_checkpoint(cls, checkpoint: Mapping[str, Any]) -> "AuthorityMaintenanceExecutor":
        if not isinstance(checkpoint, Mapping):
            raise AuthorityMaintenanceError("maintenance checkpoint must be a mapping")
        payload = checkpoint.get("checkpoint_payload")
        if not isinstance(payload, Mapping):
            raise AuthorityMaintenanceError("maintenance checkpoint payload is missing")
        supplied_hash = checkpoint.get("checkpoint_hash")
        if supplied_hash != semantic_hash(payload):
            raise AuthorityMaintenanceConflict("maintenance checkpoint hash mismatch")
        if payload.get("schema") != MAINTENANCE_CHECKPOINT_SCHEMA:
            raise AuthorityMaintenanceError("maintenance checkpoint schema mismatch")
        if payload.get("contract_id") != MAINTENANCE_CONTRACT_ID:
            raise AuthorityMaintenanceError("maintenance contract id mismatch")

        all_snapshots = [_snapshot_from_dict(row) for row in payload.get("all_snapshots", ())]
        snapshot_by_key = {snapshot.authority_ref.key: snapshot for snapshot in all_snapshots}
        initial_refs = [authority_ref(x) for x in payload.get("initial_snapshot_refs", ())]
        initial_snapshots = []
        for ref in initial_refs:
            snapshot = snapshot_by_key.get(ref.key)
            if snapshot is None:
                raise AuthorityMaintenanceConflict("initial snapshot missing from checkpoint")
            initial_snapshots.append(snapshot)
        initial_current = {
            row["authority_id"]: authority_ref(row["authority_ref"])
            for row in payload.get("initial_current_selection", ())
        }
        executor = cls(
            initial_snapshots=tuple(initial_snapshots),
            initial_current_selection=initial_current,
            determinant_graph=SemanticDeterminantGraph.from_dict(payload["determinant_graph"]),
        )

        evidence_pool = {
            obj.ref.key: obj
            for obj in (
                AuthorityEvidenceReceipt.from_dict(row)
                for row in payload.get("evidence_receipts", ())
            )
        }
        candidate_pool = {
            obj.ref.key: obj
            for obj in (
                AuthorityCandidate.from_dict(row) for row in payload.get("candidates", ())
            )
        }
        adjudication_pool = {
            obj.ref.key: obj
            for obj in (
                AuthorityAdjudicationReceipt.from_dict(row)
                for row in payload.get("adjudications", ())
            )
        }
        seal_pool = {
            obj.ref.key: obj
            for obj in (
                AuthorityRevisionSealReceipt.from_dict(row)
                for row in payload.get("seals", ())
            )
        }
        invalidation_pool = {
            obj.ref.key: obj
            for obj in (
                AuthorityInvalidationReceipt.from_dict(row)
                for row in payload.get("invalidations", ())
            )
        }
        release_pool = {
            obj.ref.key: obj
            for obj in (
                AuthorityReleaseReceipt.from_dict(row)
                for row in payload.get("releases", ())
            )
        }
        events = [
            MaintenanceEvent.from_dict(row) for row in payload.get("events", ())
        ]

        seen_evidence: set[str] = set()
        seen_candidates: set[str] = set()
        seen_adjudications: set[str] = set()
        seen_seals: set[str] = set()
        seen_invalidations: set[str] = set()
        seen_releases: set[str] = set()

        for event in events:
            expected_parent = executor._events[-1].ref if executor._events else None
            if event.parent_event_ref != expected_parent or event.sequence_number != len(
                executor._events
            ) + 1:
                raise AuthorityMaintenanceConflict("checkpoint maintenance event chain is broken")
            if event.event_kind == "EVIDENCE_RECORDED":
                obj = evidence_pool.get(event.subject_ref.key)
                if obj is None:
                    raise AuthorityMaintenanceConflict("evidence event subject missing")
                if obj.parent_evidence_receipt_ref is not None and (
                    obj.parent_evidence_receipt_ref.key not in executor._evidence
                ):
                    raise AuthorityMaintenanceConflict("evidence event genealogy is out of order")
                executor._evidence[obj.ref.key] = obj
                seen_evidence.add(obj.ref.key)

            elif event.event_kind in {
                "CANDIDATE_PROPOSED", "CANDIDATE_EVIDENCE_ACCUMULATED"
            }:
                obj = candidate_pool.get(event.subject_ref.key)
                if obj is None:
                    raise AuthorityMaintenanceConflict("candidate event subject missing")
                executor._assert_candidate_links(obj)
                executor._candidates[obj.ref.key] = obj
                seen_candidates.add(obj.ref.key)

            elif event.event_kind == "CANDIDATE_ADJUDICATED":
                obj = adjudication_pool.get(event.subject_ref.key)
                if obj is None or obj.candidate_ref.key not in executor._candidates:
                    raise AuthorityMaintenanceConflict("adjudication event subject/candidate missing")
                executor._adjudications[obj.ref.key] = obj
                seen_adjudications.add(obj.ref.key)

            elif event.event_kind == "REVISION_SEALED":
                seal = seal_pool.get(event.subject_ref.key)
                if seal is None:
                    raise AuthorityMaintenanceConflict("seal event subject missing")
                if seal.candidate_ref.key not in executor._candidates:
                    raise AuthorityMaintenanceConflict("seal candidate missing")
                adjudication = executor._adjudications.get(seal.adjudication_ref.key)
                if adjudication is None or adjudication.decision != "APPROVED":
                    raise AuthorityMaintenanceConflict("seal lacks approved adjudication")
                snapshot = snapshot_by_key.get(seal.authority_ref.key)
                if snapshot is None or snapshot.ref != seal.authority_snapshot_ref:
                    raise AuthorityMaintenanceConflict("seal snapshot missing or mismatched")
                executor._assert_snapshot_can_register(snapshot)
                executor._snapshots[snapshot.authority_ref.key] = snapshot
                executor._snapshot_exact_refs[snapshot.ref.key] = snapshot
                executor._seals[seal.ref.key] = seal
                seen_seals.add(seal.ref.key)

            elif event.event_kind in {"CURRENT_PROMOTED", "CURRENT_ROLLED_BACK"}:
                release = release_pool.get(event.subject_ref.key)
                if release is None:
                    raise AuthorityMaintenanceConflict("release event subject missing")
                invalidation = invalidation_pool.get(release.invalidation_receipt_ref.key)
                if invalidation is None:
                    raise AuthorityMaintenanceConflict("release invalidation receipt missing")
                selected = executor._snapshots.get(release.selected_authority_ref.key)
                if selected is None:
                    raise AuthorityMaintenanceConflict("release selected snapshot missing")
                current_before = executor._current.get(release.selected_authority_ref.authority_id)
                if current_before != release.previous_current_authority_ref:
                    raise AuthorityMaintenanceConflict("release current-pointer ancestry mismatch")
                expected_affected = executor._graph.affected(
                    invalidation.changed_authority_refs)
                if expected_affected != invalidation.affected_dependent_refs:
                    raise AuthorityMaintenanceConflict(
                        "replayed invalidation differs from determinant graph")
                # Independently recompute U as the graph's own complement of A.
                # Recomputing only A would make A and U disjoint and jointly
                # exhaustive over K at *initial production* only: a checkpoint whose
                # serialized U had been shrunk or altered would still replay, because
                # nothing re-derived U from the graph. Recomputing both here is what
                # makes the partition hold at replay as well.
                expected_unaffected = executor._graph.unaffected(expected_affected)
                if expected_unaffected != invalidation.unaffected_dependent_refs:
                    raise AuthorityMaintenanceConflict(
                        "replayed invalidation unaffected set differs from the "
                        "determinant graph's own complement of the affected set; A and "
                        "U must be disjoint and cover every known dependent at replay, "
                        "not merely at initial production "
                        "(C1-03R-OWNER-BLOCK-CHECKPOINT-TRUSTED-U-001)"
                    )
                if event.dependent_refs != invalidation.affected_dependent_refs:
                    raise AuthorityMaintenanceConflict(
                        "release event affected-dependent receipt mismatch")
                if event.authority_refs != invalidation.changed_authority_refs:
                    raise AuthorityMaintenanceConflict(
                        "release event changed-authority receipt mismatch")
                if release.release_kind == "ROLLBACK":
                    prior = release.prior_lawful_release_ref
                    if prior is None or prior.key not in executor._releases:
                        raise AuthorityMaintenanceConflict(
                            "rollback target was not a prior replayed lawful release")
                if release.seal_ref.key not in executor._seals:
                    raise AuthorityMaintenanceConflict("release exact seal missing")
                executor._invalidations[invalidation.ref.key] = invalidation
                executor._releases[release.ref.key] = release
                executor._current[release.selected_authority_ref.authority_id] = (
                    release.selected_authority_ref
                )
                executor._current_release[release.selected_authority_ref.authority_id] = (
                    release.ref
                )
                seen_invalidations.add(invalidation.ref.key)
                seen_releases.add(release.ref.key)
            else:
                raise AuthorityMaintenanceConflict("unsupported event kind during replay")
            executor._append_event(event)

        if seen_evidence != set(evidence_pool):
            raise AuthorityMaintenanceConflict("checkpoint contains orphan evidence receipts")
        if seen_candidates != set(candidate_pool):
            raise AuthorityMaintenanceConflict("checkpoint contains orphan candidates")
        if seen_adjudications != set(adjudication_pool):
            raise AuthorityMaintenanceConflict("checkpoint contains orphan adjudications")
        if seen_seals != set(seal_pool):
            raise AuthorityMaintenanceConflict("checkpoint contains orphan seals")
        if seen_invalidations != set(invalidation_pool):
            raise AuthorityMaintenanceConflict("checkpoint contains orphan invalidation receipts")
        if seen_releases != set(release_pool):
            raise AuthorityMaintenanceConflict("checkpoint contains orphan release receipts")

        if {snapshot.authority_ref.key for snapshot in executor.snapshots} != set(snapshot_by_key):
            raise AuthorityMaintenanceConflict("checkpoint snapshot set did not replay exactly")

        expected_current = {
            row["authority_id"]: authority_ref(row["authority_ref"])
            for row in payload.get("current_selection", ())
        }
        expected_current_release = {
            row["authority_id"]: exact_ref(row["release_ref"])
            for row in payload.get("current_release_refs", ())
        }
        if executor._current != expected_current:
            raise AuthorityMaintenanceConflict("checkpoint current selection did not replay exactly")
        if executor._current_release != expected_current_release:
            raise AuthorityMaintenanceConflict(
                "checkpoint current release pointers did not replay exactly")

        replayed = executor.export_checkpoint()
        if replayed["checkpoint_hash"] != supplied_hash:
            raise AuthorityMaintenanceConflict(
                "fresh replay checkpoint identity differs from original")
        return executor

    def audit_replay(self) -> MaintenanceReplayReceipt:
        original = self.export_checkpoint()
        replayed = self.from_checkpoint(original)
        replayed_checkpoint = replayed.export_checkpoint()
        return MaintenanceReplayReceipt(
            original_checkpoint_hash=original["checkpoint_hash"],
            replayed_checkpoint_hash=replayed_checkpoint["checkpoint_hash"],
            event_refs=tuple(event.ref for event in self._events),
            historical_authority_refs=tuple(
                snapshot.authority_ref for snapshot in self.snapshots),
            current_selection_refs=tuple(self._current.values()),
        )


__all__ = [
    "MAINTENANCE_CONTRACT_ID",
    "MAINTENANCE_CHECKPOINT_SCHEMA",
    "AUTHORITY_PROPOSAL_STATES",
    "ADJUDICATION_STATES",
    "CORRECTION_KINDS",
    "AuthorityMaintenanceError",
    "AuthorityMaintenanceConflict",
    "AuthorityEvidenceReceipt",
    "AuthorityCandidate",
    "AuthorityAdjudicationReceipt",
    "AuthorityRevisionSealReceipt",
    "SemanticDeterminantGraph",
    "AuthorityInvalidationReceipt",
    "AuthorityReleaseReceipt",
    "MaintenanceEvent",
    "MaintenanceReplayReceipt",
    "AuthorityMaintenanceExecutor",
]
