"""Generic PRE-V3 source/semantic batch control plane.

This module implements only candidate-agnostic control-plane plumbing for the
staged PRE-V3 source -> semantic-core pipeline.  It does not adjudicate source
text, issue authority, qualify candidates, materialize actor facts, construct
R4 rule envelopes, select rule currentness, or compose topology.

The semantic identities below are content-addressed from exact governed refs.
Batch order, sharding, retries, wall-clock time, and worker identity are not
part of any semantic identity.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash


CONTROL_PLANE_CONTRACT_ID = (
    "PREV3_GENERIC_SOURCE_SEMANTIC_BATCH_CONTROL_PLANE_R1@1.0.0"
)
SOURCE_LOCAL_INTAKE_REF_KIND = "PREV3_SOURCE_LOCAL_INTAKE"
POSITION_SEMANTIC_CORE_REF_KIND = "PREV3_POSITION_SEMANTIC_CORE"
SEMANTIC_CANDIDATE_REF_KIND = "PREV3_SEMANTIC_CANDIDATE_SNAPSHOT"
POSITION_MATERIALIZATION_REQUEST_REF_KIND = "PREV3_POSITION_MATERIALIZATION_REQUEST"
MECHANISM_ROUTE_REF_KIND = "PREV3_MECHANISM_RULE_CANDIDATE_ROUTE"
POSITION_ROUTE_REF_KIND = "PREV3_POSITION_QUALIFICATION_ROUTE"
BLOCKER_REF_KIND = "PREV3_CANDIDATE_BLOCKER"
QUARANTINE_REF_KIND = "PREV3_CANDIDATE_QUARANTINE"
STATUS_REF_KIND = "PREV3_CANDIDATE_STATUS"
STAGE_RECEIPT_REF_KIND = "PREV3_BATCH_STAGE_RECEIPT"
SEMANTIC_CORE_AGGREGATE_REF_KIND = "PREV3_SEMANTIC_CORE_AGGREGATE"

_FORBIDDEN_SELECTOR_TOKENS = frozenset(
    {"LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER", "SEMVER_FALLBACK", "*"}
)
_FORBIDDEN_SELECTOR_PREFIXES = (
    "LATEST:",
    "LATEST@",
    "DEFAULT:",
    "DEFAULT@",
    "FUZZY:",
    "FUZZY@",
    "NEAREST:",
    "NEAREST@",
    "SEMVER:",
    "SEMVER@",
)
_FORBIDDEN_RANGE_CHARS = frozenset("*<>^~")
_FORBIDDEN_POSITION_CORE_KEYS = frozenset(
    {
        "occupant_actor_or_entity_ref",
        "occupant_ref",
        "actor_ref",
        "entity_ref",
        "person_ref",
    }
)


class StructuralBatchControlPlaneError(ValueError):
    """Base fail-closed control-plane error."""


class MalformedExactRefError(StructuralBatchControlPlaneError):
    """A required exact reference was absent or of the wrong type."""


class MutableSelectorError(StructuralBatchControlPlaneError):
    """A mutable/fuzzy selector was supplied where exact identity is required."""


class IdentityConflictError(StructuralBatchControlPlaneError):
    """The same governed logical identity was supplied with conflicting hashes."""


class ReplayMismatchError(StructuralBatchControlPlaneError):
    """Deterministic replay produced an identity different from the expected ref."""


class PositionOccupantLeakError(StructuralBatchControlPlaneError):
    """Occupant identity leaked into reusable structural-position semantics."""


class MissingAuthorityOrAdmissionError(StructuralBatchControlPlaneError):
    """A routing/materialization operation lacks exact admission/authority basis."""


class QuarantinedCandidateError(StructuralBatchControlPlaneError):
    """A quarantined or otherwise non-routable candidate was routed downstream."""


class TopologyBoundaryError(StructuralBatchControlPlaneError):
    """Automatic candidate processing attempted to cross the topology boundary."""


class CandidateKind(str, Enum):
    STRUCTURAL_POSITION = "STRUCTURAL_POSITION"
    MECHANISM_RULE = "MECHANISM_RULE"


class CandidateStage(str, Enum):
    CLAIM_NORMALIZED = "CLAIM_NORMALIZED"
    SEMANTIC_CORE_REDUCED = "SEMANTIC_CORE_REDUCED"
    GENERIC_CONTRACT_VALIDATED = "GENERIC_CONTRACT_VALIDATED"
    AUTHORITY_CLOSURE = "AUTHORITY_CLOSURE"
    QUALIFICATION_ENVELOPE = "QUALIFICATION_ENVELOPE"
    INDEPENDENT_CURRENT_SELECTION = "INDEPENDENT_CURRENT_SELECTION"


class BatchStage(str, Enum):
    SOURCE_LOCAL_INTAKE = "SOURCE_LOCAL_INTAKE"
    CLAIM_NORMALIZATION = "CLAIM_NORMALIZATION"
    SEMANTIC_CORE_REDUCTION = "SEMANTIC_CORE_REDUCTION"
    GENERIC_CONTRACT_VALIDATION = "GENERIC_CONTRACT_VALIDATION"
    AUTHORITY_CLOSURE = "AUTHORITY_CLOSURE"
    QUALIFICATION_ENVELOPE = "QUALIFICATION_ENVELOPE"
    INDEPENDENT_CURRENT_SELECTION = "INDEPENDENT_CURRENT_SELECTION"


_STAGE_ORDER = {stage: index for index, stage in enumerate(BatchStage)}


class CandidateOutcome(str, Enum):
    PASS = "PASS"
    BLOCKED = "BLOCKED"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    CANDIDATE_ONLY = "CANDIDATE_ONLY"
    QUALIFIED = "QUALIFIED"
    CURRENT = "CURRENT"
    HISTORICAL_NONCURRENT = "HISTORICAL_NONCURRENT"
    QUARANTINED = "QUARANTINED"


class BlockerClass(str, Enum):
    SOURCE_EVIDENCE = "SOURCE_EVIDENCE"
    SEMANTIC_IDENTITY = "SEMANTIC_IDENTITY"
    CONTRACT_FIELD = "CONTRACT_FIELD"
    AUTHORITY = "AUTHORITY"
    SCOPE = "SCOPE"
    QUALIFICATION = "QUALIFICATION"
    TEMPORAL_PORTABILITY = "TEMPORAL_PORTABILITY"
    CURRENTNESS = "CURRENTNESS"
    REPLAY_INTEGRITY = "REPLAY_INTEGRITY"
    TOPOLOGY_BOUNDARY = "TOPOLOGY_BOUNDARY"


class QuarantineReason(str, Enum):
    REPLAY_MISMATCH = "REPLAY_MISMATCH"
    IDENTITY_CONFLICT = "IDENTITY_CONFLICT"
    SEMANTIC_CORE_CONFLICT = "SEMANTIC_CORE_CONFLICT"
    MALFORMED_REF = "MALFORMED_REF"
    MUTABLE_SELECTOR = "MUTABLE_SELECTOR"
    MISSING_AUTHORITY_OR_ADMISSION = "MISSING_AUTHORITY_OR_ADMISSION"
    CONTRACT_BLOCKED = "CONTRACT_BLOCKED"


class SpecializedRouteKind(str, Enum):
    POSITION_QUALIFICATION = "POSITION_QUALIFICATION"
    R4_GENERIC_BATCH_ENVELOPE = "R4_GENERIC_BATCH_ENVELOPE"


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise StructuralBatchControlPlaneError(f"{name} must be non-empty text")
    return value.strip()


def _reject_mutable_selector_text(value: str, name: str, *, version: bool = False) -> str:
    text = _text(value, name)
    upper = text.upper()
    if upper in _FORBIDDEN_SELECTOR_TOKENS or upper.startswith(_FORBIDDEN_SELECTOR_PREFIXES):
        raise MutableSelectorError(f"{name} must be exact; mutable/fuzzy selector forbidden")
    if "*" in text:
        raise MutableSelectorError(f"{name} may not contain a wildcard")
    if version and any(ch in text for ch in (_FORBIDDEN_RANGE_CHARS - {"*"})):
        raise MutableSelectorError(f"{name} may not be a version range or wildcard")
    return text


def _exact_ref(value: Any, name: str) -> ExactRef:
    if not isinstance(value, ExactRef):
        raise MalformedExactRefError(f"{name} must be an ExactRef")
    _reject_mutable_selector_text(value.kind, f"{name}.kind")
    _reject_mutable_selector_text(value.object_id, f"{name}.object_id")
    return value


def _authority_ref(value: Any, name: str) -> AuthorityRef:
    if not isinstance(value, AuthorityRef):
        raise MalformedExactRefError(f"{name} must be an AuthorityRef")
    _reject_mutable_selector_text(value.authority_id, f"{name}.authority_id")
    _reject_mutable_selector_text(
        value.authority_version, f"{name}.authority_version", version=True
    )
    return value


def _exact_ref_tuple(
    values: Iterable[ExactRef],
    name: str,
    *,
    require_nonempty: bool,
    allow_logical_conflicts: bool = False,
) -> tuple[ExactRef, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise MalformedExactRefError(f"{name} must be an iterable of ExactRef")
    refs = tuple(_exact_ref(value, name) for value in values)
    if require_nonempty and not refs:
        raise MissingAuthorityOrAdmissionError(f"{name} must not be empty")

    by_key: dict[str, ExactRef] = {}
    logical_hashes: dict[tuple[str, str], str] = {}
    for ref in refs:
        logical = (ref.kind, ref.object_id)
        prior_hash = logical_hashes.get(logical)
        if (
            not allow_logical_conflicts
            and prior_hash is not None
            and prior_hash != ref.content_hash
        ):
            raise IdentityConflictError(
                f"{name} contains conflicting snapshots for {ref.kind}|{ref.object_id}"
            )
        if prior_hash is None:
            logical_hashes[logical] = ref.content_hash
        by_key[ref.key] = ref
    return tuple(by_key[key] for key in sorted(by_key))


def _authority_ref_tuple(
    values: Iterable[AuthorityRef],
    name: str,
) -> tuple[AuthorityRef, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise MalformedExactRefError(f"{name} must be an iterable of AuthorityRef")
    refs = tuple(_authority_ref(value, name) for value in values)
    by_key: dict[str, AuthorityRef] = {}
    logical_hashes: dict[tuple[str, str], str] = {}
    for ref in refs:
        logical = (ref.authority_id, ref.authority_version)
        prior_hash = logical_hashes.get(logical)
        if prior_hash is not None and prior_hash != ref.authority_content_hash:
            raise IdentityConflictError(
                f"{name} contains conflicting authority snapshots for "
                f"{ref.authority_id}@{ref.authority_version}"
            )
        logical_hashes[logical] = ref.authority_content_hash
        by_key[ref.key] = ref
    return tuple(by_key[key] for key in sorted(by_key))


def _optional_exact_ref(value: ExactRef | None, name: str) -> ExactRef | None:
    return None if value is None else _exact_ref(value, name)


def _enum(value: Any, enum_type: type[Enum], name: str) -> Enum:
    try:
        return value if isinstance(value, enum_type) else enum_type(value)
    except (TypeError, ValueError) as exc:
        raise StructuralBatchControlPlaneError(f"unknown {name}: {value!r}") from exc


def _ref(kind: str, object_id: str, material: Mapping[str, Any]) -> ExactRef:
    return ExactRef(kind, object_id, semantic_hash(material))


def _same_ref(left: ExactRef, right: ExactRef) -> bool:
    return left.key == right.key


def _reject_topology_ref(ref: ExactRef, name: str) -> ExactRef:
    exact = _exact_ref(ref, name)
    text = f"{exact.kind}|{exact.object_id}".upper()
    if "TOPOLOGY" in text or "SOURCE_TO_RECEIVER_EDGE" in text:
        raise TopologyBoundaryError(
            f"{name} cannot target or emit topology from automatic candidate processing"
        )
    return exact


def require_replay(expected_ref: ExactRef, actual_ref: ExactRef, context: str) -> ExactRef:
    expected = _exact_ref(expected_ref, "expected_ref")
    actual = _exact_ref(actual_ref, "actual_ref")
    if not _same_ref(expected, actual):
        raise ReplayMismatchError(
            f"{context} replay mismatch: expected {expected.key}, got {actual.key}"
        )
    return actual


__all__ = [
    "CONTROL_PLANE_CONTRACT_ID",
    "StructuralBatchControlPlaneError",
    "MalformedExactRefError",
    "MutableSelectorError",
    "IdentityConflictError",
    "ReplayMismatchError",
    "PositionOccupantLeakError",
    "MissingAuthorityOrAdmissionError",
    "QuarantinedCandidateError",
    "TopologyBoundaryError",
    "CandidateKind",
    "CandidateStage",
    "BatchStage",
    "CandidateOutcome",
    "BlockerClass",
    "QuarantineReason",
    "SpecializedRouteKind",
    "require_replay",
]
