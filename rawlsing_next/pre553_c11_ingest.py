"""Package-atomic C11 source ingest for PRE553 Wave-02 I02.

The ingest boundary validates and seals C11 information only.  It does not run
empirical queries/discovery, certify source equivalence, decide structural
admission, change V553+, or create actor/V3/V2 semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from enum import Enum
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    require_positive_authority,
    validate_authority_snapshot,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    CanonicalSemanticObject,
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    Pre553IntegrityError,
    RespondentEvent,
    RoutingEligibilityFact,
    SourceUniverseRelation,
    WeightMeasureFact,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_c11_integrity import (
    C11IntegrityError,
    C11InternalRecord,
    ComparatorReplayBinding,
    DiscoveryBranchReplayBinding,
    EmpiricalPredicateReplayBinding,
    QuestionVariableBinding,
    ReplayManifest,
    RespondentIdentity,
    StructuralAdmissionReplayBinding,
    TypedAbsence,
    authority_snapshot_set_hash,
    canonical_section_refs,
    ensure_distinct_event_occurrences,
    make_m01_m18_coverage,
    validate_public_carrier_object,
)
from rawlsing_next.pre553_c11_repository import (
    C11LogicalRelease, C11Repository, _make_validated_release,
)

INGEST_CONTRACT_VERSION = "PRE553_C11_INGEST@1.0.0"
FRONTIER_VERSION = "D13_C11_M01_M18@1.0.0"
SEMANTIC_PROJECTION_ID = "PRE553_C11_LOGICAL_RELEASE_PROJECTION@1.0.0"

FORBIDDEN_SELECTOR_TOKENS = ("latest", "default", "fuzzy", "nearest")


class IngestDisposition(str, Enum):
    ACCEPTED_C11_LOGICAL_RELEASE = "ACCEPTED_C11_LOGICAL_RELEASE"
    BLOCKED_MISSING_REQUIRED_AUTHORITY = "BLOCKED_MISSING_REQUIRED_AUTHORITY"
    BLOCKED_TYPED_SOURCE_UNKNOWN = "BLOCKED_TYPED_SOURCE_UNKNOWN"
    REJECTED_INTEGRITY_FAILURE = "REJECTED_INTEGRITY_FAILURE"
    REJECTED_TOPOLOGY_LOSS = "REJECTED_TOPOLOGY_LOSS"
    REJECTED_EVENT_IDENTITY_COLLAPSE = "REJECTED_EVENT_IDENTITY_COLLAPSE"
    REJECTED_RISK_SET_LOSS = "REJECTED_RISK_SET_LOSS"
    REJECTED_WEIGHT_AUTHORITY_DEFAULT = "REJECTED_WEIGHT_AUTHORITY_DEFAULT"
    REJECTED_SOURCE_UNIVERSE_COLLAPSE = "REJECTED_SOURCE_UNIVERSE_COLLAPSE"
    REJECTED_REPLAY_NONDETERMINISM = "REJECTED_REPLAY_NONDETERMINISM"
    REJECTED_UNAUTHORIZED_SEMANTIC_PROMOTION = "REJECTED_UNAUTHORIZED_SEMANTIC_PROMOTION"


class C11IngestValidationError(C11IntegrityError):
    def __init__(self, disposition: IngestDisposition, message: str) -> None:
        super().__init__(message)
        self.disposition = disposition


@dataclass(frozen=True)
class SourceReleaseManifest:
    source_artifact_id: str
    source_artifact_content_hash: str
    source_family_id: str
    study_product_id: str
    release_id: str
    instrument_release_id: str
    ingest_contract_version: str
    declared_universe_refs: tuple[ExactRef, ...]
    declared_authority_snapshot_refs: tuple[AuthorityRef, ...]
    declared_record_counts_by_logical_family: Mapping[str, int]
    source_snapshot_retention_ref: ExactRef

    def __post_init__(self) -> None:
        for name in (
            "source_artifact_id", "source_family_id", "study_product_id", "release_id",
            "instrument_release_id", "ingest_contract_version",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise C11IntegrityError(f"{name} must be a non-empty string")
            lowered = value.strip().lower()
            if any(token == lowered or lowered.startswith(token + ":")
                   for token in FORBIDDEN_SELECTOR_TOKENS):
                raise C11IntegrityError(f"{name} may not use latest/default/fuzzy/nearest selection")
        if self.ingest_contract_version != INGEST_CONTRACT_VERSION:
            raise C11IntegrityError("source package ingest contract version mismatch")
        if (not isinstance(self.source_artifact_content_hash, str)
                or len(self.source_artifact_content_hash) != 64
                or self.source_artifact_content_hash.lower() != self.source_artifact_content_hash
                or any(ch not in "0123456789abcdef" for ch in self.source_artifact_content_hash)):
            raise C11IntegrityError("source_artifact_content_hash must be lowercase sha256")
        for ref in self.declared_universe_refs:
            exact_ref(ref, "declared_universe_refs")
        for ref in self.declared_authority_snapshot_refs:
            authority_ref(ref, "declared_authority_snapshot_refs")
        exact_ref(self.source_snapshot_retention_ref, "source_snapshot_retention_ref")
        counts = dict(self.declared_record_counts_by_logical_family)
        for family, count in counts.items():
            if not isinstance(family, str) or not family:
                raise C11IntegrityError("declared count family must be non-empty string")
            if not isinstance(count, int) or isinstance(count, bool) or count < 0:
                raise C11IntegrityError("declared record count must be nonnegative integer")
        object.__setattr__(self, "declared_record_counts_by_logical_family",
                           MappingProxyType(counts))

    @property
    def source_artifact_ref(self) -> ExactRef:
        return ExactRef("SOURCE_ARTIFACT", self.source_artifact_id, self.source_artifact_content_hash)

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "source_artifact_ref": self.source_artifact_ref.as_dict(),
            "source_family_id": self.source_family_id,
            "study_product_id": self.study_product_id,
            "release_id": self.release_id,
            "instrument_release_id": self.instrument_release_id,
            "ingest_contract_version": self.ingest_contract_version,
            "declared_universe_refs": [r.as_dict() for r in sorted(self.declared_universe_refs, key=lambda r: r.key)],
            "declared_authority_snapshot_refs": [
                r.as_dict() for r in sorted(self.declared_authority_snapshot_refs, key=lambda r: r.key)
            ],
            "declared_record_counts_by_logical_family": dict(
                sorted(self.declared_record_counts_by_logical_family.items())
            ),
            "source_snapshot_retention_ref": self.source_snapshot_retention_ref.as_dict(),
        }

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.semantic_projection())


@dataclass(frozen=True)
class C11SourceReleaseCandidate:
    source_release_manifest: SourceReleaseManifest
    empirical_universes: tuple[EmpiricalUniverse, ...]
    respondent_identities: tuple[RespondentIdentity, ...]
    question_variable_bindings: tuple[QuestionVariableBinding, ...]
    respondent_events: tuple[RespondentEvent, ...]
    routing_eligibility_facts_or_exact_rules: tuple[RoutingEligibilityFact, ...]
    empirical_coordinate_facts: tuple[EmpiricalCoordinateFact, ...]
    weight_measure_facts_or_typed_absence: tuple[WeightMeasureFact, ...] | TypedAbsence
    authority_snapshots: tuple[AuthoritySnapshot, ...]
    source_universe_relations_or_explicit_distinct_default: tuple[SourceUniverseRelation, ...] | TypedAbsence
    predicate_replay_bindings_when_retained_objects_require_them: tuple[EmpiricalPredicateReplayBinding, ...] | TypedAbsence
    comparator_replay_bindings_or_typed_deferred_state: tuple[ComparatorReplayBinding, ...] | TypedAbsence
    discovery_branch_replay_bindings_or_typed_deferred_state: tuple[DiscoveryBranchReplayBinding, ...] | TypedAbsence
    structural_admission_replay_bindings_or_typed_not_applicable_state: tuple[StructuralAdmissionReplayBinding, ...] | TypedAbsence
    candidate_replay_manifest: ReplayManifest | None


@dataclass(frozen=True)
class C11IngestResult:
    disposition: IngestDisposition
    accepted: bool
    release_ref: ExactRef | None
    semantic_release_hash: str | None
    replay_manifest_ref: ExactRef | None
    m01_m18_coverage: Mapping[str, tuple[str, ...]]
    errors: tuple[str, ...]


def _is_sequence_section(value: Any, item_type: type, name: str) -> tuple[Any, ...]:
    if isinstance(value, TypedAbsence):
        raise C11IntegrityError(f"{name} unexpectedly carries TypedAbsence")
    if not isinstance(value, tuple):
        raise C11IntegrityError(f"{name} must be an immutable tuple")
    if any(not isinstance(item, item_type) for item in value):
        raise C11IntegrityError(f"{name} contains wrong record family")
    return value


def _section_explicit(value: Any, *, allowed_absence: frozenset[str], item_type: type, name: str) -> tuple[Any, ...]:
    if isinstance(value, TypedAbsence):
        if value.state not in allowed_absence:
            raise C11IntegrityError(f"{name} typed state {value.state!r} is not lawful")
        return ()
    return _is_sequence_section(value, item_type, name)


def _record_counts(candidate: C11SourceReleaseCandidate) -> dict[str, int]:
    def count(section: Any) -> int:
        return 0 if isinstance(section, TypedAbsence) else len(section)

    return {
        "EmpiricalUniverse": len(candidate.empirical_universes),
        "RespondentIdentity": len(candidate.respondent_identities),
        "QuestionVariableBinding": len(candidate.question_variable_bindings),
        "RespondentEvent": len(candidate.respondent_events),
        "RoutingEligibilityFact": len(candidate.routing_eligibility_facts_or_exact_rules),
        "EmpiricalCoordinateFact": len(candidate.empirical_coordinate_facts),
        "WeightMeasureFact": count(candidate.weight_measure_facts_or_typed_absence),
        "AuthoritySnapshot": len(candidate.authority_snapshots),
        "SourceUniverseRelation": count(candidate.source_universe_relations_or_explicit_distinct_default),
        "EmpiricalPredicateReplayBinding": count(
            candidate.predicate_replay_bindings_when_retained_objects_require_them),
        "ComparatorReplayBinding": count(candidate.comparator_replay_bindings_or_typed_deferred_state),
        "DiscoveryBranchReplayBinding": count(
            candidate.discovery_branch_replay_bindings_or_typed_deferred_state),
        "StructuralAdmissionReplayBinding": count(
            candidate.structural_admission_replay_bindings_or_typed_not_applicable_state),
        "ReplayManifest": 1 if candidate.candidate_replay_manifest is not None else 0,
    }


def record_counts_for_candidate(candidate: C11SourceReleaseCandidate) -> Mapping[str, int]:
    return MappingProxyType(_record_counts(candidate))


def _section_projection(section: Any) -> Any:
    if isinstance(section, TypedAbsence):
        return section.as_dict()
    refs = []
    for item in section:
        if isinstance(item, CanonicalSemanticObject):
            refs.append(item.ref)
        elif isinstance(item, C11InternalRecord):
            refs.append(item.ref)
        else:
            raise C11IntegrityError("unsupported C11 section member")
    return [ref.as_dict() for ref in sorted(refs, key=lambda r: r.key)]


def _candidate_projection(candidate: C11SourceReleaseCandidate) -> dict[str, Any]:
    """Order-invariant logical package projection, excluding replay manifest self-reference."""
    return {
        "ingest_contract_version": INGEST_CONTRACT_VERSION,
        "source_release_manifest": candidate.source_release_manifest.semantic_projection(),
        "empirical_universes": _section_projection(candidate.empirical_universes),
        "respondent_identities": _section_projection(candidate.respondent_identities),
        "question_variable_bindings": _section_projection(candidate.question_variable_bindings),
        "respondent_events": _section_projection(candidate.respondent_events),
        "routing_eligibility_facts_or_exact_rules": _section_projection(
            candidate.routing_eligibility_facts_or_exact_rules),
        "empirical_coordinate_facts": _section_projection(candidate.empirical_coordinate_facts),
        "weight_measure_facts_or_typed_absence": _section_projection(
            candidate.weight_measure_facts_or_typed_absence),
        "authority_snapshots": _section_projection(candidate.authority_snapshots),
        "source_universe_relations_or_explicit_distinct_default": _section_projection(
            candidate.source_universe_relations_or_explicit_distinct_default),
        "predicate_replay_bindings_when_retained_objects_require_them": _section_projection(
            candidate.predicate_replay_bindings_when_retained_objects_require_them),
        "comparator_replay_bindings_or_typed_deferred_state": _section_projection(
            candidate.comparator_replay_bindings_or_typed_deferred_state),
        "discovery_branch_replay_bindings_or_typed_deferred_state": _section_projection(
            candidate.discovery_branch_replay_bindings_or_typed_deferred_state),
        "structural_admission_replay_bindings_or_typed_not_applicable_state": _section_projection(
            candidate.structural_admission_replay_bindings_or_typed_not_applicable_state),
    }


def _candidate_projection_semantic_hash(candidate: C11SourceReleaseCandidate) -> str:
    """Hash the canonical candidate projection without materializing ref dictionaries.

    This is byte-identical to semantic_hash(_candidate_projection(candidate)).
    Candidate sections may be large, so immutable ExactRef values are sorted and
    serialized directly into the SHA-256 stream instead of expanding every ref
    into a fresh mapping first.
    """
    h = hashlib.sha256()

    def write(text: str) -> None:
        h.update(text.encode("utf-8"))

    def write_section(section: Any) -> None:
        if isinstance(section, TypedAbsence):
            write(canonical_json(section.as_dict()))
            return
        refs: list[ExactRef] = []
        for item in section:
            if isinstance(item, CanonicalSemanticObject):
                refs.append(item.ref)
            elif isinstance(item, C11InternalRecord):
                refs.append(item.ref)
            else:
                raise C11IntegrityError("unsupported C11 section member")
        refs.sort(key=lambda ref: ref.key)
        write("[")
        for index, ref in enumerate(refs):
            if index:
                write(",")
            write(canonical_json(ref.as_dict()))
        write("]")

    sections = {
        "authority_snapshots": candidate.authority_snapshots,
        "comparator_replay_bindings_or_typed_deferred_state":
            candidate.comparator_replay_bindings_or_typed_deferred_state,
        "discovery_branch_replay_bindings_or_typed_deferred_state":
            candidate.discovery_branch_replay_bindings_or_typed_deferred_state,
        "empirical_coordinate_facts": candidate.empirical_coordinate_facts,
        "empirical_universes": candidate.empirical_universes,
        "predicate_replay_bindings_when_retained_objects_require_them":
            candidate.predicate_replay_bindings_when_retained_objects_require_them,
        "question_variable_bindings": candidate.question_variable_bindings,
        "respondent_events": candidate.respondent_events,
        "respondent_identities": candidate.respondent_identities,
        "routing_eligibility_facts_or_exact_rules":
            candidate.routing_eligibility_facts_or_exact_rules,
        "source_universe_relations_or_explicit_distinct_default":
            candidate.source_universe_relations_or_explicit_distinct_default,
        "structural_admission_replay_bindings_or_typed_not_applicable_state":
            candidate.structural_admission_replay_bindings_or_typed_not_applicable_state,
        "weight_measure_facts_or_typed_absence":
            candidate.weight_measure_facts_or_typed_absence,
    }
    values = {
        "ingest_contract_version": INGEST_CONTRACT_VERSION,
        "source_release_manifest": candidate.source_release_manifest.semantic_projection(),
    }
    keys = sorted((*sections, *values))
    write("{")
    for index, key in enumerate(keys):
        if index:
            write(",")
        write(canonical_json(key))
        write(":")
        if key in sections:
            write_section(sections[key])
        else:
            write(canonical_json(values[key]))
    write("}")
    return h.hexdigest()


def _all_nonmanifest_refs(candidate: C11SourceReleaseCandidate) -> tuple[ExactRef, ...]:
    refs: list[ExactRef] = [
        candidate.source_release_manifest.source_artifact_ref,
        candidate.source_release_manifest.source_snapshot_retention_ref,
    ]
    for section in (
        candidate.empirical_universes,
        candidate.respondent_identities,
        candidate.question_variable_bindings,
        candidate.respondent_events,
        candidate.routing_eligibility_facts_or_exact_rules,
        candidate.empirical_coordinate_facts,
        candidate.weight_measure_facts_or_typed_absence,
        candidate.authority_snapshots,
        candidate.source_universe_relations_or_explicit_distinct_default,
        candidate.predicate_replay_bindings_when_retained_objects_require_them,
        candidate.comparator_replay_bindings_or_typed_deferred_state,
        candidate.discovery_branch_replay_bindings_or_typed_deferred_state,
        candidate.structural_admission_replay_bindings_or_typed_not_applicable_state,
    ):
        if isinstance(section, TypedAbsence):
            continue
        refs.extend(canonical_section_refs(section))
    return tuple(sorted(refs, key=lambda r: r.key))


def build_candidate_replay_manifest(
    candidate: C11SourceReleaseCandidate,
    *,
    replay_protocol_authority_ref: AuthorityRef,
    deterministic_tie_order_rules_ref: ExactRef,
    replay_protocol_version: str,
    frontier_version: str = FRONTIER_VERSION,
) -> ReplayManifest:
    """Build the unique deterministic manifest for candidate content excluding itself."""
    return ReplayManifest(
        frontier_version=frontier_version,
        authority_snapshot_set_hash=authority_snapshot_set_hash(candidate.authority_snapshots),
        source_substrate_content_refs=(candidate.source_release_manifest.source_artifact_ref,),
        semantic_projection_id=SEMANTIC_PROJECTION_ID,
        semantic_projection_hash=_candidate_projection_semantic_hash(candidate),
        deterministic_tie_order_rules_ref=deterministic_tie_order_rules_ref,
        replay_protocol_version=replay_protocol_version,
        replay_protocol_authority_ref=replay_protocol_authority_ref,
        closure_refs=_all_nonmanifest_refs(candidate),
    )


def _iter_internal_records(candidate: C11SourceReleaseCandidate) -> tuple[C11InternalRecord, ...]:
    records: list[C11InternalRecord] = [
        *candidate.respondent_identities,
        *candidate.question_variable_bindings,
    ]
    for section in (
        candidate.predicate_replay_bindings_when_retained_objects_require_them,
        candidate.comparator_replay_bindings_or_typed_deferred_state,
        candidate.discovery_branch_replay_bindings_or_typed_deferred_state,
        candidate.structural_admission_replay_bindings_or_typed_not_applicable_state,
    ):
        if not isinstance(section, TypedAbsence):
            records.extend(section)
    return tuple(records)


def _iter_public_objects(candidate: C11SourceReleaseCandidate) -> tuple[CanonicalSemanticObject, ...]:
    objects: list[CanonicalSemanticObject] = [
        *candidate.empirical_universes,
        *candidate.respondent_events,
        *candidate.routing_eligibility_facts_or_exact_rules,
        *candidate.empirical_coordinate_facts,
        *candidate.authority_snapshots,
    ]
    if not isinstance(candidate.weight_measure_facts_or_typed_absence, TypedAbsence):
        objects.extend(candidate.weight_measure_facts_or_typed_absence)
    if not isinstance(candidate.source_universe_relations_or_explicit_distinct_default, TypedAbsence):
        objects.extend(candidate.source_universe_relations_or_explicit_distinct_default)
    return tuple(objects)


def _walk_authority_refs(value: Any) -> Iterable[AuthorityRef]:
    if isinstance(value, AuthorityRef):
        yield value
        return
    if isinstance(value, Mapping):
        keys = set(value)
        authority_keys = {"authority_id", "authority_version", "authority_content_hash"}
        if keys == authority_keys:
            yield authority_ref(value)
            return
        for item in value.values():
            yield from _walk_authority_refs(item)
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            yield from _walk_authority_refs(item)


def _validate_declared_manifest(candidate: C11SourceReleaseCandidate) -> None:
    manifest = candidate.source_release_manifest
    actual_universes = tuple(sorted((u.ref for u in candidate.empirical_universes), key=lambda r: r.key))
    declared_universes = tuple(sorted(manifest.declared_universe_refs, key=lambda r: r.key))
    if actual_universes != declared_universes:
        raise C11IngestValidationError(
            IngestDisposition.REJECTED_SOURCE_UNIVERSE_COLLAPSE,
            "declared universe refs do not exactly match candidate universes",
        )
    actual_auth = tuple(sorted((a.authority_ref for a in candidate.authority_snapshots), key=lambda r: r.key))
    declared_auth = tuple(sorted(manifest.declared_authority_snapshot_refs, key=lambda r: r.key))
    if actual_auth != declared_auth:
        raise C11IngestValidationError(
            IngestDisposition.BLOCKED_MISSING_REQUIRED_AUTHORITY,
            "declared authority snapshot refs do not exactly match package snapshots",
        )
    actual_counts = _record_counts(candidate)
    declared_counts = dict(manifest.declared_record_counts_by_logical_family)
    for family, declared in declared_counts.items():
        if family not in actual_counts:
            raise C11IntegrityError(f"unknown declared logical family count {family!r}")
        if actual_counts[family] != declared:
            raise C11IntegrityError(
                f"declared record count mismatch for {family}: {declared} != {actual_counts[family]}")
    core_required = {
        "EmpiricalUniverse", "RespondentIdentity", "QuestionVariableBinding", "RespondentEvent",
        "RoutingEligibilityFact", "EmpiricalCoordinateFact", "AuthoritySnapshot",
    }
    missing_count_declarations = sorted(core_required - set(declared_counts))
    if missing_count_declarations:
        raise C11IntegrityError(
            f"source manifest omits core logical-family counts {missing_count_declarations!r}")


def _validate_sections(candidate: C11SourceReleaseCandidate) -> None:
    if not candidate.empirical_universes:
        raise C11IngestValidationError(
            IngestDisposition.BLOCKED_TYPED_SOURCE_UNKNOWN,
            "C11 source package requires at least one exact EmpiricalUniverse",
        )
    if not candidate.respondent_identities:
        raise C11IntegrityError("C11 package requires scoped respondent identities")
    if not candidate.question_variable_bindings:
        raise C11IntegrityError("C11 package requires native question/topology bindings")
    if not candidate.respondent_events:
        raise C11IntegrityError("C11 package requires respondent-event incidence")
    if not candidate.routing_eligibility_facts_or_exact_rules:
        raise C11IngestValidationError(
            IngestDisposition.REJECTED_RISK_SET_LOSS,
            "C11 package requires explicit routing/risk-set incidence or exact rule facts",
        )
    if not candidate.empirical_coordinate_facts:
        raise C11IntegrityError("C11 package requires future-authorizable respondent coordinates")
    if not candidate.authority_snapshots:
        raise C11IngestValidationError(
            IngestDisposition.BLOCKED_MISSING_REQUIRED_AUTHORITY,
            "C11 package requires immutable authority snapshots",
        )

    _section_explicit(
        candidate.weight_measure_facts_or_typed_absence,
        allowed_absence=frozenset({"NOT_APPLICABLE", "MISSING", "NOT_AUTHORIZED", "UNKNOWN"}),
        item_type=WeightMeasureFact,
        name="weight_measure_facts_or_typed_absence",
    )
    _section_explicit(
        candidate.source_universe_relations_or_explicit_distinct_default,
        allowed_absence=frozenset({"DISTINCT_BY_DEFAULT"}),
        item_type=SourceUniverseRelation,
        name="source_universe_relations_or_explicit_distinct_default",
    )
    _section_explicit(
        candidate.predicate_replay_bindings_when_retained_objects_require_them,
        allowed_absence=frozenset({"NOT_APPLICABLE", "DEFERRED"}),
        item_type=EmpiricalPredicateReplayBinding,
        name="predicate_replay_bindings_when_retained_objects_require_them",
    )
    _section_explicit(
        candidate.comparator_replay_bindings_or_typed_deferred_state,
        allowed_absence=frozenset({"DEFERRED"}),
        item_type=ComparatorReplayBinding,
        name="comparator_replay_bindings_or_typed_deferred_state",
    )
    _section_explicit(
        candidate.discovery_branch_replay_bindings_or_typed_deferred_state,
        allowed_absence=frozenset({"DEFERRED"}),
        item_type=DiscoveryBranchReplayBinding,
        name="discovery_branch_replay_bindings_or_typed_deferred_state",
    )
    _section_explicit(
        candidate.structural_admission_replay_bindings_or_typed_not_applicable_state,
        allowed_absence=frozenset({"NOT_APPLICABLE"}),
        item_type=StructuralAdmissionReplayBinding,
        name="structural_admission_replay_bindings_or_typed_not_applicable_state",
    )
    if candidate.candidate_replay_manifest is None:
        raise C11IngestValidationError(
            IngestDisposition.REJECTED_REPLAY_NONDETERMINISM,
            "candidate replay manifest is required before atomic admission",
        )


def _validate_authorities(candidate: C11SourceReleaseCandidate) -> AuthorityRegistry:
    try:
        for snapshot in candidate.authority_snapshots:
            validate_authority_snapshot(snapshot)
        registry = AuthorityRegistry(candidate.authority_snapshots)
        for obj in _iter_public_objects(candidate):
            validate_public_carrier_object(obj, registry)
            for ref in _walk_authority_refs(obj.semantic_fields):
                registry.resolve_exact(ref)
        for record in _iter_internal_records(candidate):
            for ref in _walk_authority_refs(record.semantic_projection()):
                registry.resolve_exact(ref)
        registry.resolve_exact(candidate.candidate_replay_manifest.replay_protocol_authority_ref)
        require_positive_authority(
            registry.resolve_exact(candidate.candidate_replay_manifest.replay_protocol_authority_ref).snapshot,
            authority_kind="REPLAY_PROTOCOL",
        )
        return registry
    except Pre553AuthorityError as exc:
        raise C11IngestValidationError(
            IngestDisposition.BLOCKED_MISSING_REQUIRED_AUTHORITY, str(exc)) from exc
    except C11IntegrityError:
        raise


def _validate_universe_and_respondent_scope(candidate: C11SourceReleaseCandidate) -> None:
    universe_by_key = {u.ref.key: u for u in candidate.empirical_universes}
    if len(universe_by_key) != len(candidate.empirical_universes):
        raise C11IngestValidationError(
            IngestDisposition.REJECTED_SOURCE_UNIVERSE_COLLAPSE,
            "duplicate exact EmpiricalUniverse object in package",
        )

    respondent_by_key: dict[str, RespondentIdentity] = {}
    respondent_pair: set[tuple[str, str]] = set()
    for respondent in candidate.respondent_identities:
        universe_ref = exact_ref(respondent.empirical_universe_ref)
        if universe_ref.key not in universe_by_key:
            raise C11IngestValidationError(
                IngestDisposition.REJECTED_SOURCE_UNIVERSE_COLLAPSE,
                "respondent identity points outside declared universe set",
            )
        pair = (universe_ref.key, respondent.respondent_key)
        if pair in respondent_pair:
            raise C11IntegrityError("duplicate respondent key within one exact universe namespace")
        respondent_pair.add(pair)
        respondent_by_key[respondent.ref.key] = respondent

    for obj in (
        *candidate.respondent_events,
        *candidate.routing_eligibility_facts_or_exact_rules,
        *candidate.empirical_coordinate_facts,
        *((candidate.weight_measure_facts_or_typed_absence)
          if not isinstance(candidate.weight_measure_facts_or_typed_absence, TypedAbsence) else ()),
    ):
        universe_ref = exact_ref(obj.empirical_universe_ref)
        respondent_ref = exact_ref(obj.scoped_respondent_ref)
        respondent = respondent_by_key.get(respondent_ref.key)
        if universe_ref.key not in universe_by_key or respondent is None:
            raise C11IngestValidationError(
                IngestDisposition.REJECTED_SOURCE_UNIVERSE_COLLAPSE,
                "carrier fact lacks exact in-package universe/respondent namespace binding",
            )
        if exact_ref(respondent.empirical_universe_ref).key != universe_ref.key:
            raise C11IngestValidationError(
                IngestDisposition.REJECTED_SOURCE_UNIVERSE_COLLAPSE,
                "cross-universe respondent reuse/inference is forbidden",
            )


def _validate_questions_and_events(candidate: C11SourceReleaseCandidate) -> None:
    question_keys: set[tuple[str, str]] = set()
    for binding in candidate.question_variable_bindings:
        universe_ref = exact_ref(binding.empirical_universe_ref)
        native = exact_ref(binding.native_question_ref)
        question_keys.add((universe_ref.key, native.key))
    for event in candidate.respondent_events:
        universe_ref = exact_ref(event.empirical_universe_ref)
        native = exact_ref(event.native_question_ref)
        if (universe_ref.key, native.key) not in question_keys:
            raise C11IngestValidationError(
                IngestDisposition.REJECTED_TOPOLOGY_LOSS,
                "response event lacks exact native question/topology binding",
            )
    try:
        ensure_distinct_event_occurrences(candidate.respondent_events)
    except C11IntegrityError as exc:
        raise C11IngestValidationError(
            IngestDisposition.REJECTED_EVENT_IDENTITY_COLLAPSE, str(exc)) from exc


def _validate_question_authorities(candidate: C11SourceReleaseCandidate, registry: AuthorityRegistry) -> None:
    try:
        for binding in candidate.question_variable_bindings:
            registry.resolve_exact(binding.semantic_authority_ref)
            registry.resolve_exact(binding.topology_authority_ref)
            if isinstance(binding.canonical_question_ref_or_typed_absence, ExactRef):
                require_positive_authority(
                    registry.resolve_exact(binding.semantic_authority_ref).snapshot,
                    authority_kind="NATIVE_CANONICAL_MAPPING_HARMONIZATION",
                )
        for respondent in candidate.respondent_identities:
            if isinstance(respondent.identity_map_authority_ref_or_typed_absence, AuthorityRef):
                registry.resolve_exact(respondent.identity_map_authority_ref_or_typed_absence)
    except Pre553AuthorityError as exc:
        raise C11IngestValidationError(
            IngestDisposition.REJECTED_UNAUTHORIZED_SEMANTIC_PROMOTION,
            "canonical/normalized identity material lacks exact positive mapping authority",
        ) from exc


def _validate_source_relations(candidate: C11SourceReleaseCandidate) -> None:
    section = candidate.source_universe_relations_or_explicit_distinct_default
    if isinstance(section, TypedAbsence):
        if section.state != "DISTINCT_BY_DEFAULT":
            raise C11IngestValidationError(
                IngestDisposition.REJECTED_SOURCE_UNIVERSE_COLLAPSE,
                "source universes require explicit DISTINCT_BY_DEFAULT or exact relation records",
            )
        return
    universe_keys = {u.ref.key for u in candidate.empirical_universes}
    for relation in section:
        refs = [exact_ref(r) for r in relation.source_universe_refs]
        if any(ref.key not in universe_keys for ref in refs):
            raise C11IngestValidationError(
                IngestDisposition.REJECTED_SOURCE_UNIVERSE_COLLAPSE,
                "source relation references an undeclared universe",
            )


def _validate_replay(candidate: C11SourceReleaseCandidate, registry: AuthorityRegistry) -> ReplayManifest:
    manifest = candidate.candidate_replay_manifest
    assert manifest is not None
    expected_projection_hash = _candidate_projection_semantic_hash(candidate)
    if manifest.frontier_version != FRONTIER_VERSION:
        raise C11IngestValidationError(
            IngestDisposition.REJECTED_REPLAY_NONDETERMINISM, "frontier version mismatch")
    if manifest.semantic_projection_id != SEMANTIC_PROJECTION_ID:
        raise C11IngestValidationError(
            IngestDisposition.REJECTED_REPLAY_NONDETERMINISM, "semantic projection id mismatch")
    if manifest.semantic_projection_hash != expected_projection_hash:
        raise C11IngestValidationError(
            IngestDisposition.REJECTED_REPLAY_NONDETERMINISM,
            "candidate package semantic projection differs from sealed replay hash",
        )
    if manifest.authority_snapshot_set_hash != authority_snapshot_set_hash(candidate.authority_snapshots):
        raise C11IngestValidationError(
            IngestDisposition.REJECTED_REPLAY_NONDETERMINISM,
            "authority snapshot set differs from sealed replay manifest",
        )
    if tuple(manifest.source_substrate_content_refs) != (candidate.source_release_manifest.source_artifact_ref,):
        raise C11IngestValidationError(
            IngestDisposition.REJECTED_REPLAY_NONDETERMINISM,
            "source artifact identity/hash differs from replay manifest",
        )
    if tuple(manifest.closure_refs) != _all_nonmanifest_refs(candidate):
        raise C11IngestValidationError(
            IngestDisposition.REJECTED_REPLAY_NONDETERMINISM,
            "replay manifest closure refs do not exactly cover candidate package",
        )
    try:
        snapshot = registry.resolve_exact(manifest.replay_protocol_authority_ref).snapshot
        require_positive_authority(snapshot, authority_kind="REPLAY_PROTOCOL")
    except Pre553AuthorityError as exc:
        raise C11IngestValidationError(
            IngestDisposition.BLOCKED_MISSING_REQUIRED_AUTHORITY,
            "replay protocol authority unavailable",
        ) from exc
    return manifest


def _classify_integrity_error(exc: Exception) -> IngestDisposition:
    text = str(exc).lower()
    if "canonical" in text and "authority" in text:
        return IngestDisposition.REJECTED_UNAUTHORIZED_SEMANTIC_PROMOTION
    if "topology" in text or "order/rank" in text:
        return IngestDisposition.REJECTED_TOPOLOGY_LOSS
    if "risk" in text or "routing" in text or "member_set" in text:
        return IngestDisposition.REJECTED_RISK_SET_LOSS
    if "weight" in text and ("1.0" in text or "default" in text):
        return IngestDisposition.REJECTED_WEIGHT_AUTHORITY_DEFAULT
    if "universe" in text or "namespace" in text or "respondent" in text:
        return IngestDisposition.REJECTED_SOURCE_UNIVERSE_COLLAPSE
    if "replay" in text or "manifest" in text:
        return IngestDisposition.REJECTED_REPLAY_NONDETERMINISM
    if "authority" in text:
        return IngestDisposition.BLOCKED_MISSING_REQUIRED_AUTHORITY
    return IngestDisposition.REJECTED_INTEGRITY_FAILURE


def validate_c11_source_release(candidate: C11SourceReleaseCandidate) -> C11LogicalRelease:
    if not isinstance(candidate, C11SourceReleaseCandidate):
        raise C11IntegrityError("expected C11SourceReleaseCandidate")
    _validate_sections(candidate)
    _validate_declared_manifest(candidate)
    registry = _validate_authorities(candidate)
    _validate_universe_and_respondent_scope(candidate)
    _validate_questions_and_events(candidate)
    _validate_question_authorities(candidate, registry)
    _validate_source_relations(candidate)
    replay_manifest = _validate_replay(candidate, registry)

    coverage = make_m01_m18_coverage(
        universes=candidate.empirical_universes,
        respondents=candidate.respondent_identities,
        questions=candidate.question_variable_bindings,
        events=candidate.respondent_events,
        routing=candidate.routing_eligibility_facts_or_exact_rules,
        coordinates=candidate.empirical_coordinate_facts,
        weight_section_explicit=True,
        authority_snapshots=candidate.authority_snapshots,
        source_relation_section_explicit=True,
        predicate_replay_section_explicit=True,
        comparator_section_explicit=True,
        discovery_section_explicit=True,
        structural_admission_section_explicit=True,
        replay_manifest=replay_manifest,
    )

    projection_hash = semantic_hash({
        "candidate_projection_hash": replay_manifest.semantic_projection_hash,
        "replay_manifest_ref": replay_manifest.ref.as_dict(),
        "m01_m18": {k: list(v) for k, v in coverage.items()},
    })
    public_objects = tuple(sorted(_iter_public_objects(candidate), key=lambda obj: obj.ref.key))
    internal_records = tuple(sorted(_iter_internal_records(candidate), key=lambda obj: obj.ref.key))
    return _make_validated_release(
        release_id=candidate.source_release_manifest.release_id,
        source_artifact_ref=candidate.source_release_manifest.source_artifact_ref,
        source_release_manifest_hash=candidate.source_release_manifest.content_hash,
        semantic_release_hash=projection_hash,
        replay_manifest=replay_manifest,
        public_objects=public_objects,
        internal_records=internal_records,
        m01_m18_coverage=coverage,
    )


def ingest_c11_source_release(
    candidate: C11SourceReleaseCandidate,
    repository: C11Repository,
) -> C11IngestResult:
    """Validate completely, then atomically commit. Failure leaves repository unchanged."""
    if not isinstance(repository, C11Repository):
        raise TypeError("repository must be C11Repository")
    before = repository.release_refs
    try:
        release = validate_c11_source_release(candidate)
        repository._commit_validated(release)
        return C11IngestResult(
            disposition=IngestDisposition.ACCEPTED_C11_LOGICAL_RELEASE,
            accepted=True,
            release_ref=release.release_ref,
            semantic_release_hash=release.semantic_release_hash,
            replay_manifest_ref=release.replay_manifest.ref,
            m01_m18_coverage=release.m01_m18_coverage,
            errors=(),
        )
    except C11IngestValidationError as exc:
        disposition = exc.disposition
        message = str(exc)
    except (C11IntegrityError, Pre553IntegrityError, Pre553AuthorityError) as exc:
        disposition = _classify_integrity_error(exc)
        message = str(exc)
    if repository.release_refs != before:
        raise C11IntegrityError("atomic ingest failure mutated C11 repository")
    return C11IngestResult(
        disposition=disposition,
        accepted=False,
        release_ref=None,
        semantic_release_hash=None,
        replay_manifest_ref=None,
        m01_m18_coverage=MappingProxyType({}),
        errors=(message,),
    )


__all__ = [
    "INGEST_CONTRACT_VERSION", "FRONTIER_VERSION", "SEMANTIC_PROJECTION_ID",
    "IngestDisposition", "C11IngestValidationError", "SourceReleaseManifest",
    "C11SourceReleaseCandidate", "C11IngestResult", "record_counts_for_candidate",
    "build_candidate_replay_manifest", "validate_c11_source_release", "ingest_c11_source_release",
]
