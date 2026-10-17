"""Canonical PRE553 empirical semantic objects.

Wave-02 I01 implements only public type/identity/validation surfaces. It does
not store C11 data, execute queries/discovery, decide structural admission, or
alter V553+/V3/V2 behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from fractions import Fraction
import hashlib
import json
import re
from types import MappingProxyType
from typing import Any, ClassVar, Iterable, Mapping, Sequence

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
URN_PREFIX = "urn:rawlsing:pre553"

PUBLIC_OBJECT_FAMILIES = (
    "EmpiricalUniverse@1.0.0",
    "RespondentEvent@1.0.0",
    "EmpiricalCoordinateFact@1.0.0",
    "RoutingEligibilityFact@1.0.0",
    "WeightMeasureFact@1.0.0",
    "AuthoritySnapshot@1.0.0",
    "SourceUniverseRelation@1.0.0",
    "EmpiricalPredicate@1.0.0",
    "EmpiricalQuerySpec@1.0.0",
    "EmpiricalFact@1.0.0",
    "DiscoveryAuthority@1.0.0",
    "DiscoveryResultReceipt@1.0.0",
    "StructuralEmpiricalAdmission@1.0.0",
    "ReplayReceipt@1.0.0",
)
PUBLIC_OBJECT_FAMILY_NAMES = frozenset(x.split("@", 1)[0] for x in PUBLIC_OBJECT_FAMILIES)

# P10 logical carrier/replay records remain internal carrier records. Their
# existence must never enlarge the public semantic ontology.
INTERNAL_C11_RECORD_FAMILIES = frozenset({
    "RespondentIdentity",
    "QuestionVariableBinding",
    "EmpiricalPredicateReplayBinding",
    "ComparatorReplayBinding",
    "DiscoveryBranchReplayBinding",
    "StructuralAdmissionReplayBinding",
    "ReplayManifest",
})
DEFERRED_PUBLIC_FAMILIES = frozenset({
    "ActorComparatorReceipt",
    "PositionedSubjectEmpiricalPossibilityField",
    "V3EmpiricalPossibilityInput",
})
DIAGNOSTIC_ONLY_KINDS = frozenset({
    "MI", "NMI", "CRAMERS_V", "ENTROPY_REDUCTION", "LIFT",
    "TREE_SCORE", "CLOUD_SCORE", "ASSOCIATION_STRENGTH",
})

STATE_FAMILIES: Mapping[str, frozenset[str]] = MappingProxyType({
    "RESPONSE_EVENT_STATE": frozenset({
        "SUBSTANTIVE_RESPONSE", "MISSING", "DK", "REFUSAL", "IAP",
        "INAPPLICABLE", "NOT_ASKED", "SOURCE_SPECIFIC_SPECIAL", "INVALID_UNRESOLVED",
    }),
    "EMPIRICAL_COORDINATE_STATE": frozenset({
        "OBSERVED_COORDINATE", "UNKNOWN", "MISSING", "NOT_LAWFULLY_CONDITIONABLE",
        "INVALID_UNRESOLVED",
    }),
    "ROUTING_ELIGIBILITY_STATE": frozenset({
        "ELIGIBLE_APPLICABLE", "NOT_ASKED", "INAPPLICABLE", "ROUTING_UNKNOWN",
        "RULE_UNAVAILABLE", "NOT_ELIGIBLE",
    }),
    "WEIGHT_MEASURE_STATE": frozenset({
        "WEIGHT_VALID_AUTHORIZED", "WEIGHT_MISSING", "WEIGHT_INVALID",
        "WEIGHT_NOT_AUTHORIZED", "WEIGHT_BASIS_UNRESOLVED",
    }),
    "SOURCE_UNIVERSE_STATE": frozenset({
        "UNIVERSE_IDENTIFIED", "UNKNOWN_SOURCE_RELATION", "NONCOMPARABLE",
        "LINKAGE_NOT_AUTHORIZED", "POOLING_NOT_AUTHORIZED", "BACKFILL_NOT_AUTHORIZED",
    }),
    "AUTHORITY_STATE": frozenset({
        "ALLOW", "DENY", "DEFER", "MISSING_AUTHORITY", "UNKNOWN", "OUT_OF_SCOPE",
        "SUPERSEDED_NOT_REPLAYABLE", "AUTHORITY_HASH_MISMATCH", "AUTHORITY_SCOPE_MISMATCH",
    }),
    "SOURCE_UNIVERSE_RELATION_STATE": frozenset({
        "RELATION_AUTHORIZED_FOR_EXACT_KIND_AND_SCOPE", "DISTINCT_BY_DEFAULT",
        "UNKNOWN_SOURCE_RELATION", "NONCOMPARABLE", "LINKAGE_NOT_AUTHORIZED",
        "POOLING_NOT_AUTHORIZED", "BACKFILL_NOT_AUTHORIZED",
        "OVERLAP_TREATMENT_UNAUTHORIZED", "RELATION_DENIED", "RELATION_OUT_OF_SCOPE",
    }),
    "PREDICATE_STATE": frozenset({
        "PREDICATE_RESOLVED_AUTHORIZED", "PREDICATE_UNRESOLVED", "PREDICATE_UNAUTHORIZED",
        "OPERAND_UNAVAILABLE", "RISK_SET_UNAVAILABLE", "OUT_OF_SCOPE",
    }),
    "QUERY_STATE": frozenset({
        "QUERY_AUTHORIZED_RESOLVABLE", "QUERY_UNAUTHORIZED", "TARGET_UNAVAILABLE",
        "PREDICATE_UNRESOLVED", "RISK_SET_UNAVAILABLE", "MEASURE_UNAVAILABLE",
        "SOURCE_SCOPE_UNAVAILABLE", "VALID_EMPTY_QUERY_FRONTIER",
    }),
    "EMPIRICAL_FACT_STATE": frozenset({
        "SUPPORTED", "OBSERVED_ZERO", "ZERO_SUPPORT", "ZERO_OVERLAP", "LOW_SUPPORT",
        "NONCOMPARABLE", "NOT_APPLICABLE", "UNAVAILABLE", "UNCERTAINTY_UNQUANTIFIED",
        "UNRESOLVED", "VALID_EMPTY", "INTEGRITY_FAILURE",
    }),
    "DISCOVERY_AUTHORITY_STATE": frozenset({
        "EXACT_BOUNDED_AUTHORIZED", "ADAPTIVE_EXPLORATORY_AUTHORIZED",
        "NO_LAWFUL_CANDIDATES", "COVERAGE_NOT_CLAIMED", "AUTHORITY_MISSING",
        "AUTHORITY_DENIED", "OUT_OF_SCOPE",
    }),
    "DISCOVERY_RESULT_STATE": frozenset({
        "DISCOVERED_RESULT_SUPPORTED", "VALID_EMPTY", "INSUFFICIENT_SUPPORT",
        "NONCOMPARABLE", "COVERAGE_LIMITED", "PRUNED_BY_AUTHORITY", "UNEVALUATED",
    }),
    "STRUCTURAL_ADMISSION_STATE": frozenset({
        "ADMITTED_FOR_EXACT_STRUCTURAL_USE", "ADMISSION_DENIED", "MISSING_AUTHORITY",
        "DEFERRED", "NONCOMPARABLE", "INSUFFICIENT_EVIDENCE", "OUT_OF_SCOPE",
        "UNRESOLVED", "INTEGRITY_FAILURE",
    }),
    "REPLAY_STATE": frozenset({
        "REPLAY_VERIFIED", "REPLAY_INPUT_MISSING", "AUTHORITY_UNAVAILABLE",
        "REPLAY_UNRESOLVED", "HASH_MISMATCH", "SEMANTIC_PROJECTION_MISMATCH",
        "NONDETERMINISTIC_REPLAY",
    }),
})

P06_ADMISSION_DECISION_STATES = frozenset({
    "ADMITTED", "MISSING_STRUCTURAL_ADMISSION_AUTHORITY", "ADMISSION_DENIED",
    "ADMISSION_DEFERRED", "EMPIRICAL_FACT_NONCOMPARABLE",
    "SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE", "INSUFFICIENT_EVIDENCE_UNDER_RULE",
    "TEMPORAL_SCOPE_MISMATCH", "STRUCTURAL_TARGET_UNRESOLVED", "NEGATIVE_AUTHORITY_ONLY",
    "UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY", "VALID_EMPTY", "INTEGRITY_FAILURE",
})
P07_RELATION_KINDS = frozenset({
    "SOURCE_SEMANTIC_EQUIVALENCE", "RESPONDENT_LINKAGE", "OVERLAP_NON_DUPLICATION",
    "SAMPLE_POOLING", "ESTIMAND_COMPOSITION", "BACKFILL", "PROVENANCE_ORIGIN",
    "HARMONIZATION_ALIAS",
})
P07_RELATION_DECISIONS = frozenset({
    "AUTHORIZED", "DENIED", "NOT_APPLICABLE", "UNKNOWN_AUTHORITY",
    "CONFLICTING_AUTHORITY", "EXPIRED_OR_STALE",
})
P09_DISCOVERY_MODES = frozenset({"EXACT_BOUNDED", "ADAPTIVE_EXPLORATORY"})
P09_COVERAGE_CLAIMS = frozenset({
    "COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
    "EXACT_RESULTS__NONEXHAUSTIVE_FRONTIER_COVERAGE",
})


class Pre553IntegrityError(ValueError):
    """Exact identity, schema, state, or reference closure is invalid."""


class Pre553SemanticCollapseError(Pre553IntegrityError):
    """A forbidden cross-ontology substitution was attempted."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Pre553IntegrityError(f"{name} must be a non-empty string")
    return value.strip()


def _sha256(value: Any, name: str) -> str:
    value = _text(value, name)
    if not SHA256_RE.fullmatch(value):
        raise Pre553IntegrityError(f"{name} must be a lowercase sha256")
    return value


def _decimal_text(value: Decimal) -> str:
    if not value.is_finite():
        raise Pre553IntegrityError("non-finite Decimal forbidden in semantic identity")
    normalized = value.normalize()
    text = format(normalized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def canonicalize(value: Any) -> Any:
    """Return deterministic JSON-safe semantic material.

    Binary floats (including NaN/Infinity) are forbidden. Exact numerics may be
    represented as integers, Decimal, Fraction, or exact strings.
    """
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        raise Pre553IntegrityError("float/NaN/Infinity forbidden in semantic identity")
    if isinstance(value, Decimal):
        return {"$exact_decimal": _decimal_text(value)}
    if isinstance(value, Fraction):
        return {"$exact_fraction": [value.numerator, value.denominator]}
    if isinstance(value, Enum):
        return canonicalize(value.value)
    if isinstance(value, ExactRef):
        return value.as_dict()
    if isinstance(value, AuthorityRef):
        return value.as_dict()
    if isinstance(value, CanonicalSemanticObject):
        return value.ref.as_dict()
    if isinstance(value, Mapping):
        if any(not isinstance(k, str) for k in value):
            raise Pre553IntegrityError("semantic mapping keys must be strings")
        return {k: canonicalize(value[k]) for k in sorted(value)}
    if isinstance(value, (set, frozenset)):
        items = [canonicalize(v) for v in value]
        return sorted(items, key=canonical_json)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [canonicalize(v) for v in value]
    raise Pre553IntegrityError(f"unsupported semantic identity type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(canonicalize(value), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def semantic_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def canonical_set(values: Iterable[Any]) -> tuple[Any, ...]:
    by_json: dict[str, Any] = {}
    for value in values:
        material = canonicalize(value)
        by_json[canonical_json(material)] = material
    return tuple(by_json[key] for key in sorted(by_json))


class _FrozenSemanticList(tuple):
    """Attribute-free immutable marker for canonical material that originated as a list."""

    __slots__ = ()

    def __new__(cls, values: Iterable[Any]):
        return tuple.__new__(cls, tuple(values))

    def __repr__(self) -> str:
        return repr(list(self))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Sequence) and not isinstance(other, (str, bytes, bytearray)):
            return list(self) == list(other)
        return False

    __hash__ = tuple.__hash__


def _freeze_semantic_descendants(value: Any) -> Any:
    """Recursively freeze already-canonical semantic descendants without byte drift."""
    if isinstance(value, Mapping):
        # The backing dict is created here and never exported. MappingProxyType
        # therefore cannot be bypassed through dict.__setitem__ on the public value.
        return MappingProxyType(
            {key: _freeze_semantic_descendants(value[key]) for key in sorted(value)}
        )
    if isinstance(value, list):
        return _FrozenSemanticList(_freeze_semantic_descendants(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_semantic_descendants(item) for item in value)
    return value


def _detach_semantic_descendants(value: Any) -> Any:
    """Return a detached ordinary export preserving the pre-repair public shape."""
    if isinstance(value, Mapping):
        return {key: _detach_semantic_descendants(value[key]) for key in value}
    if isinstance(value, _FrozenSemanticList):
        return [_detach_semantic_descendants(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_detach_semantic_descendants(item) for item in value)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_detach_semantic_descendants(item) for item in value]
    return value


@dataclass(frozen=True, order=True)
class ExactRef:
    kind: str
    object_id: str
    content_hash: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", _text(self.kind, "kind"))
        object.__setattr__(self, "object_id", _text(self.object_id, "object_id"))
        object.__setattr__(self, "content_hash", _sha256(self.content_hash, "content_hash"))

    @property
    def key(self) -> str:
        return f"{self.kind}|{self.object_id}|{self.content_hash}"

    def as_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "object_id": self.object_id, "content_hash": self.content_hash}


@dataclass(frozen=True, order=True)
class AuthorityRef:
    authority_id: str
    authority_version: str
    authority_content_hash: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "authority_id", _text(self.authority_id, "authority_id"))
        object.__setattr__(self, "authority_version", _text(self.authority_version, "authority_version"))
        object.__setattr__(self, "authority_content_hash",
                           _sha256(self.authority_content_hash, "authority_content_hash"))

    @property
    def key(self) -> str:
        return f"{self.authority_id}|{self.authority_version}|{self.authority_content_hash}"

    def as_dict(self) -> dict[str, str]:
        return {"authority_id": self.authority_id,
                "authority_version": self.authority_version,
                "authority_content_hash": self.authority_content_hash}


def exact_ref(value: ExactRef | Mapping[str, Any], name: str = "ref") -> ExactRef:
    if isinstance(value, ExactRef):
        return value
    if not isinstance(value, Mapping):
        raise Pre553IntegrityError(f"{name} must be ExactRef or mapping")
    if set(value) != {"kind", "object_id", "content_hash"}:
        raise Pre553IntegrityError(f"{name} must contain exact kind/object_id/content_hash only")
    return ExactRef(value["kind"], value["object_id"], value["content_hash"])


def authority_ref(value: AuthorityRef | Mapping[str, Any], name: str = "authority_ref") -> AuthorityRef:
    if isinstance(value, AuthorityRef):
        return value
    if not isinstance(value, Mapping):
        raise Pre553IntegrityError(f"{name} must be AuthorityRef or mapping")
    keys = {"authority_id", "authority_version", "authority_content_hash"}
    if set(value) != keys:
        raise Pre553IntegrityError(
            f"{name} must contain exact authority_id/authority_version/authority_content_hash only")
    return AuthorityRef(value["authority_id"], value["authority_version"],
                        value["authority_content_hash"])


def _refs(values: Iterable[ExactRef | Mapping[str, Any]], name: str) -> tuple[ExactRef, ...]:
    return tuple(exact_ref(v, name) for v in values)


def _authority_refs(values: Iterable[AuthorityRef | Mapping[str, Any]], name: str) -> tuple[AuthorityRef, ...]:
    return tuple(authority_ref(v, name) for v in values)


def _canonical_ref_set(refs: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    return tuple(sorted(set(refs), key=lambda r: r.key))


def _canonical_authority_ref_set(refs: Iterable[AuthorityRef]) -> tuple[AuthorityRef, ...]:
    return tuple(sorted(set(refs), key=lambda r: r.key))


def _replay_root(value: Any) -> Any:
    if isinstance(value, ExactRef):
        return value
    if isinstance(value, Mapping):
        return exact_ref(value, "producer_replay_locator_or_reference_root")
    return _text(value, "producer_replay_locator_or_reference_root")


class CanonicalSemanticObject:
    FAMILY: ClassVar[str] = ""
    STATE_FAMILY: ClassVar[str] = ""
    REQUIRED_FIELDS: ClassVar[frozenset[str]] = frozenset()
    SET_LIKE_FIELDS: ClassVar[frozenset[str]] = frozenset()

    __slots__ = ("schema_id", "schema_version", "object_id", "content_hash", "typed_state",
                 "authority_snapshot_refs", "dependency_refs",
                 "producer_replay_locator_or_reference_root", "_semantic_fields", "_frozen")

    def __init__(
        self,
        *,
        typed_state: str,
        authority_snapshot_refs: Iterable[AuthorityRef | Mapping[str, Any]] = (),
        dependency_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
        producer_replay_locator_or_reference_root: Any,
        object_id: str | None = None,
        content_hash: str | None = None,
        schema_id: str | None = None,
        schema_version: str | None = None,
        **semantic_fields: Any,
    ) -> None:
        if self.FAMILY not in PUBLIC_OBJECT_FAMILIES:
            raise Pre553SemanticCollapseError(f"{self.FAMILY!r} is not a public P01 family")
        family_name, family_version = self.FAMILY.split("@", 1)
        if schema_id is not None and schema_id != family_name:
            raise Pre553IntegrityError("schema_id cannot substitute another public family")
        if schema_version is not None and schema_version != family_version:
            raise Pre553IntegrityError("schema_version mismatch")
        state = _text(typed_state, "typed_state")
        allowed = STATE_FAMILIES.get(self.STATE_FAMILY)
        if allowed is None or state not in allowed:
            raise Pre553IntegrityError(f"typed_state {state!r} is not valid for {self.STATE_FAMILY}")
        missing = sorted(self.REQUIRED_FIELDS - set(semantic_fields))
        if missing:
            raise Pre553IntegrityError(f"{family_name} missing required semantic fields: {missing!r}")

        auth_refs = _canonical_authority_ref_set(
            _authority_refs(authority_snapshot_refs, "authority_snapshot_refs"))
        deps = _canonical_ref_set(_refs(dependency_refs, "dependency_refs"))
        if family_name != "AuthoritySnapshot" and not auth_refs:
            raise Pre553IntegrityError(f"{family_name} requires exact authority_snapshot_refs for closure")

        normalized: dict[str, Any] = {}
        for key, value in semantic_fields.items():
            if key in {"family", "schema_id", "schema_version", "object_id", "content_hash"}:
                raise Pre553IntegrityError(f"{key} is reserved identity material")
            if key in self.SET_LIKE_FIELDS:
                if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Iterable):
                    raise Pre553IntegrityError(f"{key} must be a set-like iterable")
                normalized[key] = _freeze_semantic_descendants(canonical_set(value))
            else:
                normalized[key] = _freeze_semantic_descendants(canonicalize(value))

        replay_root = _replay_root(producer_replay_locator_or_reference_root)
        projection = {
            "schema_id": family_name,
            "schema_version": family_version,
            "typed_state": state,
            "authority_snapshot_refs": [x.as_dict() for x in auth_refs],
            "dependency_refs": [x.as_dict() for x in deps],
            "producer_replay_locator_or_reference_root": canonicalize(replay_root),
            "semantic_fields": normalized,
        }
        digest = semantic_hash(projection)
        expected_id = f"{URN_PREFIX}:{family_name}:sha256:{digest}"
        if object_id is not None and object_id != expected_id:
            raise Pre553IntegrityError("object_id does not match deterministic semantic identity")
        if content_hash is not None and _sha256(content_hash, "content_hash") != digest:
            raise Pre553IntegrityError("content_hash does not match semantic projection")

        object.__setattr__(self, "schema_id", family_name)
        object.__setattr__(self, "schema_version", family_version)
        object.__setattr__(self, "object_id", expected_id)
        object.__setattr__(self, "content_hash", digest)
        object.__setattr__(self, "typed_state", state)
        object.__setattr__(self, "authority_snapshot_refs", auth_refs)
        object.__setattr__(self, "dependency_refs", deps)
        object.__setattr__(self, "producer_replay_locator_or_reference_root", replay_root)
        object.__setattr__(self, "_semantic_fields", MappingProxyType(normalized))
        object.__setattr__(self, "_frozen", True)
        self._validate_family()

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_frozen", False):
            raise AttributeError(f"{self.schema_id} is immutable")
        object.__setattr__(self, name, value)

    def __getattr__(self, name: str) -> Any:
        fields = object.__getattribute__(self, "_semantic_fields")
        if name in fields:
            return fields[name]
        raise AttributeError(name)

    def __repr__(self) -> str:
        return f"{self.schema_id}(object_id={self.object_id!r}, typed_state={self.typed_state!r})"

    def __eq__(self, other: Any) -> bool:
        return type(self) is type(other) and self.object_id == other.object_id and self.content_hash == other.content_hash

    def __hash__(self) -> int:
        return hash((self.FAMILY, self.object_id, self.content_hash))

    @property
    def family(self) -> str:
        return self.FAMILY

    @property
    def ref(self) -> ExactRef:
        return ExactRef(self.FAMILY, self.object_id, self.content_hash)

    @property
    def semantic_fields(self) -> Mapping[str, Any]:
        return self._semantic_fields

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "typed_state": self.typed_state,
            "authority_snapshot_refs": [x.as_dict() for x in self.authority_snapshot_refs],
            "dependency_refs": [x.as_dict() for x in self.dependency_refs],
            "producer_replay_locator_or_reference_root": canonicalize(
                self.producer_replay_locator_or_reference_root),
            "semantic_fields": _detach_semantic_descendants(self._semantic_fields),
        }

    def as_dict(self) -> dict[str, Any]:
        return {**self.semantic_projection(), "object_id": self.object_id,
                "content_hash": self.content_hash}

    def _validate_family(self) -> None:
        pass


class EmpiricalUniverse(CanonicalSemanticObject):
    FAMILY = "EmpiricalUniverse@1.0.0"
    STATE_FAMILY = "SOURCE_UNIVERSE_STATE"
    REQUIRED_FIELDS = frozenset({
        "raw_source_identity", "source_family", "study_product_release", "instrument_release",
        "country_geography", "sampling_geography", "raw_wave", "canonical_wave_if_governed",
        "field_or_reference_time", "target_population_and_sample_frame", "sampling_design_regime",
        "respondent_namespace", "source_artifact_import_lineage", "harmonization_authority_ref",
        "source_relation_refs",
    })
    SET_LIKE_FIELDS = frozenset({"source_relation_refs"})


class RespondentEvent(CanonicalSemanticObject):
    FAMILY = "RespondentEvent@1.0.0"
    STATE_FAMILY = "RESPONSE_EVENT_STATE"
    REQUIRED_FIELDS = frozenset({
        "empirical_universe_ref", "scoped_respondent_ref", "native_question_ref",
        "canonical_question_ref_if_authorized", "component_or_subitem_ref", "event_group_id",
        "response_event_id_or_deterministic_index", "raw_response_value",
        "canonical_response_value_if_authorized", "value_transform_authority_ref",
        "response_topology_ref", "multiplicity_order_rank_fields", "response_state",
    })

    def _validate_family(self) -> None:
        if self.response_state != self.typed_state:
            raise Pre553IntegrityError("RespondentEvent response_state must equal typed_state")


class EmpiricalCoordinateFact(CanonicalSemanticObject):
    FAMILY = "EmpiricalCoordinateFact@1.0.0"
    STATE_FAMILY = "EMPIRICAL_COORDINATE_STATE"
    REQUIRED_FIELDS = frozenset({
        "empirical_universe_ref", "scoped_respondent_ref", "native_coordinate_ref",
        "canonical_coordinate_ref_if_authorized", "raw_coordinate_value",
        "canonical_coordinate_value_if_authorized", "unit_category_taxonomy_ref",
        "effective_or_reference_time", "coordinate_state", "normalization_crosswalk_authority_ref",
        "source_semantic_authority_ref",
    })

    def _validate_family(self) -> None:
        if self.coordinate_state != self.typed_state:
            raise Pre553IntegrityError("EmpiricalCoordinateFact coordinate_state must equal typed_state")


class RoutingEligibilityFact(CanonicalSemanticObject):
    FAMILY = "RoutingEligibilityFact@1.0.0"
    STATE_FAMILY = "ROUTING_ELIGIBILITY_STATE"
    REQUIRED_FIELDS = frozenset({
        "empirical_universe_ref", "scoped_respondent_ref", "question_or_target_ref",
        "risk_set_ref", "routing_rule_ref", "applicability_state", "routing_state",
        "parent_predicate_refs", "member_set_replay_ref",
    })
    SET_LIKE_FIELDS = frozenset({"parent_predicate_refs"})


class WeightMeasureFact(CanonicalSemanticObject):
    FAMILY = "WeightMeasureFact@1.0.0"
    STATE_FAMILY = "WEIGHT_MEASURE_STATE"
    REQUIRED_FIELDS = frozenset({
        "empirical_universe_ref", "scoped_respondent_ref", "weight_basis_id",
        "exact_weight_value_representation", "weight_state", "weight_source_ref",
        "design_authority_ref", "estimand_authority_ref", "normalization_or_recalibration_rule_ref",
        "effective_scope_ref",
    })

    def _validate_family(self) -> None:
        if self.weight_state != self.typed_state:
            raise Pre553IntegrityError("WeightMeasureFact weight_state must equal typed_state")
        if self.typed_state != "WEIGHT_VALID_AUTHORIZED" and self.exact_weight_value_representation in (1, "1", "1.0"):
            raise Pre553IntegrityError("nonpositive weight cannot be silently repaired to 1.0")


class AuthoritySnapshot(CanonicalSemanticObject):
    FAMILY = "AuthoritySnapshot@1.0.0"
    STATE_FAMILY = "AUTHORITY_STATE"
    REQUIRED_FIELDS = frozenset({
        "authority_id", "authority_version", "authority_content_hash", "authority_kind",
        "decision_state", "governed_operations", "governed_object_families", "scope_envelope",
        "effective_time_or_interval", "parent_authority_refs", "negative_limit_refs",
        "supersession_refs", "interpretation_semantics_fingerprint", "replay_protocol_ref",
    })
    SET_LIKE_FIELDS = frozenset({
        "governed_operations", "governed_object_families", "parent_authority_refs",
        "negative_limit_refs", "supersession_refs",
    })

    def _validate_family(self) -> None:
        if self.decision_state != self.typed_state:
            raise Pre553IntegrityError("AuthoritySnapshot decision_state must equal typed_state")
        _text(self.authority_id, "authority_id")
        _text(self.authority_version, "authority_version")
        _sha256(self.authority_content_hash, "authority_content_hash")
        selector = str(self.authority_kind).upper()
        if selector in {"LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER_FALLBACK"}:
            raise Pre553IntegrityError("mutable/fuzzy authority selection is forbidden")

    @property
    def authority_ref(self) -> AuthorityRef:
        return AuthorityRef(self.authority_id, self.authority_version, self.authority_content_hash)


class SourceUniverseRelation(CanonicalSemanticObject):
    FAMILY = "SourceUniverseRelation@1.0.0"
    STATE_FAMILY = "SOURCE_UNIVERSE_RELATION_STATE"
    REQUIRED_FIELDS = frozenset({
        "relation_id", "relation_kind", "source_universe_refs", "relation_authority_ref",
        "effective_scope", "overlap_or_nonduplication_evidence_refs", "composition_estimand_refs",
        "deduplication_rule_ref_if_any", "negative_limit_refs",
    })
    SET_LIKE_FIELDS = frozenset({
        "source_universe_refs", "overlap_or_nonduplication_evidence_refs",
        "composition_estimand_refs", "negative_limit_refs",
    })

    def _validate_family(self) -> None:
        if self.relation_kind not in P07_RELATION_KINDS:
            raise Pre553IntegrityError("unknown SourceUniverseRelation relation_kind")
        if len(self.source_universe_refs) < 2:
            raise Pre553IntegrityError("SourceUniverseRelation requires at least two exact universes")
        decision = self.semantic_fields.get("decision")
        if decision is not None and decision not in P07_RELATION_DECISIONS:
            raise Pre553IntegrityError("invalid P07 relation decision")
        if self.relation_kind in {"PROVENANCE_ORIGIN", "HARMONIZATION_ALIAS"} and self.typed_state == "RELATION_AUTHORIZED_FOR_EXACT_KIND_AND_SCOPE":
            raise Pre553SemanticCollapseError(
                f"{self.relation_kind} cannot grant composition/linkage/equivalence semantics")


class EmpiricalPredicate(CanonicalSemanticObject):
    FAMILY = "EmpiricalPredicate@1.0.0"
    STATE_FAMILY = "PREDICATE_STATE"
    REQUIRED_FIELDS = frozenset({
        "predicate_ast", "predicate_hash", "grammar_authority_ref", "coordinate_question_value_refs",
        "risk_set_refs", "scope_refs", "same_respondent_binding_semantics", "operator_semantics_refs",
    })
    SET_LIKE_FIELDS = frozenset({
        "coordinate_question_value_refs", "risk_set_refs", "scope_refs", "operator_semantics_refs",
    })

    def _validate_family(self) -> None:
        if semantic_hash(self.predicate_ast) != self.predicate_hash:
            raise Pre553IntegrityError("predicate_hash does not match canonical predicate_ast")
        self._validate_ast(self.predicate_ast)

    @classmethod
    def _validate_ast(cls, node: Any) -> None:
        if not isinstance(node, Mapping):
            raise Pre553IntegrityError("predicate_ast nodes must be mappings")
        op = node.get("op")
        if op in {"AND", "OR"}:
            children = node.get("children")
            if not isinstance(children, Sequence) or isinstance(children, (str, bytes)) or not children:
                raise Pre553IntegrityError(f"{op} requires children")
            for child in children:
                cls._validate_ast(child)
            hashes = [semantic_hash(child) for child in children]
            if hashes != sorted(set(hashes)):
                raise Pre553IntegrityError(
                    f"{op} children must be canonical hash-sorted with duplicates collapsed")
        elif op == "NOT":
            children = node.get("children")
            if not isinstance(children, Sequence) or len(children) != 1:
                raise Pre553IntegrityError("NOT requires exactly one child")
            cls._validate_ast(children[0])
        elif op == "LEAF":
            leaf_type = node.get("leaf_type")
            if leaf_type not in {"EMPIRICAL_POSITION_COORDINATE", "SURVEY_RESPONSE_EVENT",
                                 "DERIVED_BRANCH_COHORT", "ROUTING_APPLICABILITY_STATE",
                                 "TYPED_RESPONSE_STATE"}:
                raise Pre553SemanticCollapseError("forbidden or unknown predicate leaf meaning")
        else:
            raise Pre553IntegrityError("predicate op must be AND/OR/NOT/LEAF")


class EmpiricalQuerySpec(CanonicalSemanticObject):
    FAMILY = "EmpiricalQuerySpec@1.0.0"
    STATE_FAMILY = "QUERY_STATE"
    REQUIRED_FIELDS = frozenset({
        "target_refs", "target_arity_and_topology", "condition_predicate_ref", "risk_set_ref",
        "empirical_universe_refs", "scope_refs", "measure_basis_ref", "requested_output_grain",
        "query_authority_refs",
    })
    SET_LIKE_FIELDS = frozenset({"empirical_universe_refs", "scope_refs", "query_authority_refs"})

    def _validate_family(self) -> None:
        if not self.target_refs:
            raise Pre553IntegrityError("EmpiricalQuerySpec requires one or more target_refs")
        if not self.empirical_universe_refs:
            raise Pre553IntegrityError("EmpiricalQuerySpec requires exact source universe scope")
        if self.semantic_fields.get("diagnostic_kind") in DIAGNOSTIC_ONLY_KINDS:
            raise Pre553SemanticCollapseError("diagnostic material cannot define EmpiricalQuerySpec authority")


class EmpiricalFact(CanonicalSemanticObject):
    FAMILY = "EmpiricalFact@1.0.0"
    STATE_FAMILY = "EMPIRICAL_FACT_STATE"
    REQUIRED_FIELDS = frozenset({
        "empirical_query_spec_ref", "empirical_universe_refs", "target_topology",
        "condition_predicate_ref", "risk_set_ref", "raw_numerator_support",
        "raw_denominator_support", "weighted_numerator_support_if_authorized",
        "weighted_denominator_support_if_authorized", "measure_basis_ref",
        "response_state_semantics_ref", "uncertainty_method_or_typed_state",
        "source_empirical_provenance_refs", "replay_ref",
    })
    SET_LIKE_FIELDS = frozenset({"empirical_universe_refs", "source_empirical_provenance_refs"})

    def _validate_family(self) -> None:
        for name in ("raw_numerator_support", "raw_denominator_support"):
            value = self.semantic_fields[name]
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise Pre553IntegrityError(f"{name} must be a nonnegative exact integer")
        n, d = self.raw_numerator_support, self.raw_denominator_support
        if n > d:
            raise Pre553IntegrityError("raw numerator cannot exceed denominator")
        if self.typed_state == "ZERO_SUPPORT" and d != 0:
            raise Pre553IntegrityError("ZERO_SUPPORT requires zero exact raw denominator")
        if self.typed_state == "OBSERVED_ZERO" and (d <= 0 or n != 0):
            raise Pre553IntegrityError("OBSERVED_ZERO requires positive denominator and zero numerator")
        if self.typed_state == "SUPPORTED" and d <= 0:
            raise Pre553IntegrityError("SUPPORTED requires positive denominator")
        if self.semantic_fields.get("diagnostic_kind") in DIAGNOSTIC_ONLY_KINDS:
            raise Pre553SemanticCollapseError("diagnostic score cannot masquerade as EmpiricalFact")


class DiscoveryAuthority(CanonicalSemanticObject):
    FAMILY = "DiscoveryAuthority@1.0.0"
    STATE_FAMILY = "DISCOVERY_AUTHORITY_STATE"
    REQUIRED_FIELDS = frozenset({
        "candidate_grammar_ref", "candidate_universe_definition", "source_universe_scope",
        "risk_set_scope", "topology_scope", "measure_scope", "support_rules", "validation_rules",
        "coverage_claim", "pruning_contract", "algorithm_identity_if_semantically_required",
        "tie_order_rules", "rng_policy_if_any",
    })

    def _validate_family(self) -> None:
        mode = self.semantic_fields.get("mode")
        if mode is None:
            if self.typed_state == "EXACT_BOUNDED_AUTHORIZED":
                mode = "EXACT_BOUNDED"
            elif self.typed_state == "ADAPTIVE_EXPLORATORY_AUTHORIZED":
                mode = "ADAPTIVE_EXPLORATORY"
        if mode not in P09_DISCOVERY_MODES:
            raise Pre553IntegrityError("DiscoveryAuthority requires exact discovery mode")
        if self.coverage_claim not in P09_COVERAGE_CLAIMS:
            raise Pre553IntegrityError("invalid discovery coverage_claim")
        if mode == "EXACT_BOUNDED" and self.coverage_claim != "COMPLETE_FOR_EXACT_DECLARED_FRONTIER":
            raise Pre553IntegrityError("EXACT_BOUNDED requires complete declared-frontier coverage")
        if mode == "ADAPTIVE_EXPLORATORY" and self.coverage_claim != "EXACT_RESULTS__NONEXHAUSTIVE_FRONTIER_COVERAGE":
            raise Pre553IntegrityError("ADAPTIVE_EXPLORATORY must disclose nonexhaustive coverage")


class DiscoveryResultReceipt(CanonicalSemanticObject):
    FAMILY = "DiscoveryResultReceipt@1.0.0"
    STATE_FAMILY = "DISCOVERY_RESULT_STATE"
    REQUIRED_FIELDS = frozenset({
        "discovery_authority_ref", "candidate_identity", "winning_predicate_ref",
        "empirical_fact_refs", "validation_fact_refs", "coverage_state", "evaluated_frontier_ref",
        "branch_or_parent_ancestry_refs", "support_uncertainty_state", "replay_ref",
    })
    SET_LIKE_FIELDS = frozenset({
        "empirical_fact_refs", "validation_fact_refs", "branch_or_parent_ancestry_refs",
    })

    def _validate_family(self) -> None:
        if self.typed_state == "UNEVALUATED" and self.empirical_fact_refs:
            raise Pre553IntegrityError("UNEVALUATED discovery cannot carry positive empirical facts")


class StructuralEmpiricalAdmission(CanonicalSemanticObject):
    FAMILY = "StructuralEmpiricalAdmission@1.0.0"
    STATE_FAMILY = "STRUCTURAL_ADMISSION_STATE"
    REQUIRED_FIELDS = frozenset({
        "admission_decision_state", "decision_reason_code", "empirical_query_spec_ref",
        "empirical_fact_ref", "admission_authority_ref", "source_universe_refs",
        "native_scope_identity_refs", "target_use", "target_use_permission_refs",
        "focal_structural_proposition_ref", "structural_semantic_identity_refs",
        "effective_time_or_interval_refs_required_by_target_use", "estimand_refs",
        "measure_and_weight_authority_refs", "support_uncertainty_state", "support_uncertainty_refs",
        "applicable_negative_denial_noncomparability_refs", "interpretation_critical_authority_refs",
        "authority_closure_refs",
    })
    SET_LIKE_FIELDS = frozenset({
        "source_universe_refs", "native_scope_identity_refs", "target_use_permission_refs",
        "structural_semantic_identity_refs", "effective_time_or_interval_refs_required_by_target_use",
        "estimand_refs", "measure_and_weight_authority_refs", "support_uncertainty_refs",
        "applicable_negative_denial_noncomparability_refs", "interpretation_critical_authority_refs",
        "authority_closure_refs", "discovery_result_receipt_refs", "legacy_compatibility_refs",
    })

    def _validate_family(self) -> None:
        decision = self.admission_decision_state
        if decision not in P06_ADMISSION_DECISION_STATES:
            raise Pre553IntegrityError("unknown P06 admission decision state")
        positive = self.typed_state == "ADMITTED_FOR_EXACT_STRUCTURAL_USE"
        if positive != (decision == "ADMITTED"):
            raise Pre553IntegrityError(
                "positive public admission state iff P06 admission_decision_state is ADMITTED")
        if positive and "structural_interpretation_payload" not in self.semantic_fields:
            raise Pre553IntegrityError("ADMITTED structural receipt requires interpretation payload")
        if positive and self.semantic_fields.get("blocking_negative_present", False):
            raise Pre553SemanticCollapseError("blocking negative cannot be downgraded to admission")


class ReplayReceipt(CanonicalSemanticObject):
    FAMILY = "ReplayReceipt@1.0.0"
    STATE_FAMILY = "REPLAY_STATE"
    REQUIRED_FIELDS = frozenset({
        "replayed_object_ref", "input_content_identity_refs", "authority_snapshot_refs_replayed",
        "producer_or_algorithm_identity", "canonical_semantic_projection_hash",
        "deterministic_order_or_tie_rule_refs", "replay_protocol_ref", "replay_state",
    })
    SET_LIKE_FIELDS = frozenset({
        "input_content_identity_refs", "authority_snapshot_refs_replayed",
        "deterministic_order_or_tie_rule_refs",
    })

    def _validate_family(self) -> None:
        if self.replay_state != self.typed_state:
            raise Pre553IntegrityError("ReplayReceipt replay_state must equal typed_state")
        _sha256(self.canonical_semantic_projection_hash, "canonical_semantic_projection_hash")


def canonicalize_predicate_ast(node: Mapping[str, Any]) -> dict[str, Any]:
    """P02 canonical AND/OR/NOT normalization without heuristic rewrites."""
    if not isinstance(node, Mapping):
        raise Pre553IntegrityError("predicate AST node must be a mapping")
    op = node.get("op")
    if op == "LEAF":
        result = canonicalize(node)
        EmpiricalPredicate._validate_ast(result)
        return result
    if op == "NOT":
        children = node.get("children")
        if not isinstance(children, Sequence) or isinstance(children, (str, bytes)) or len(children) != 1:
            raise Pre553IntegrityError("NOT requires exactly one child")
        child = canonicalize_predicate_ast(children[0])
        if child.get("op") == "NOT":
            return canonicalize_predicate_ast(child["children"][0])
        result = {k: canonicalize(v) for k, v in node.items() if k not in {"op", "children"}}
        return {"op": "NOT", "children": [child], **result}
    if op in {"AND", "OR"}:
        children = node.get("children")
        if not isinstance(children, Sequence) or isinstance(children, (str, bytes)) or not children:
            raise Pre553IntegrityError(f"{op} requires children")
        flat = []
        for raw in children:
            child = canonicalize_predicate_ast(raw)
            if child.get("op") == op:
                flat.extend(child["children"])
            else:
                flat.append(child)
        by_hash = {semantic_hash(child): child for child in flat}
        ordered = [by_hash[h] for h in sorted(by_hash)]
        extra = {k: canonicalize(v) for k, v in node.items() if k not in {"op", "children"}}
        result = {"op": op, "children": ordered, **extra}
        EmpiricalPredicate._validate_ast(result)
        return result
    raise Pre553IntegrityError("predicate op must be AND/OR/NOT/LEAF")


def make_empirical_predicate(*, predicate_ast: Mapping[str, Any], **kwargs: Any) -> EmpiricalPredicate:
    ast = canonicalize_predicate_ast(predicate_ast)
    return EmpiricalPredicate(predicate_ast=ast, predicate_hash=semantic_hash(ast), **kwargs)


def is_public_object_family(name: str) -> bool:
    return name in PUBLIC_OBJECT_FAMILY_NAMES or name in PUBLIC_OBJECT_FAMILIES


def require_public_object_family(name: str) -> str:
    name = _text(name, "object family")
    bare = name.split("@", 1)[0]
    if bare in INTERNAL_C11_RECORD_FAMILIES:
        raise Pre553SemanticCollapseError(
            f"{bare} is a P10 internal carrier record, not public semantic ontology")
    if bare in DEFERRED_PUBLIC_FAMILIES:
        raise Pre553SemanticCollapseError(f"{bare} is deferred and out of I01 scope")
    if not is_public_object_family(name):
        raise Pre553SemanticCollapseError(f"{name} is not a P01 public semantic family")
    return name


def assert_zero_actor_v3_v2_effect(obj: CanonicalSemanticObject) -> None:
    """I01 records are inert and cannot themselves mutate actor/V3/V2 state."""
    if not isinstance(obj, CanonicalSemanticObject):
        raise Pre553IntegrityError("expected PRE553 canonical semantic object")
    for key in {"actor_state_effect", "v3_state_effect", "v2_state_effect", "persona_effect",
                "belief_effect", "response_effect"}:
        value = obj.semantic_fields.get(key)
        if value not in (None, False, 0, "", (), []):
            raise Pre553SemanticCollapseError(f"I01 public object cannot carry positive {key}")


__all__ = [
    "AuthorityRef", "ExactRef", "Pre553IntegrityError", "Pre553SemanticCollapseError",
    "canonicalize", "canonical_json", "canonical_set", "semantic_hash", "exact_ref",
    "authority_ref", "PUBLIC_OBJECT_FAMILIES", "PUBLIC_OBJECT_FAMILY_NAMES",
    "INTERNAL_C11_RECORD_FAMILIES", "DEFERRED_PUBLIC_FAMILIES", "DIAGNOSTIC_ONLY_KINDS",
    "STATE_FAMILIES", "EmpiricalUniverse", "RespondentEvent", "EmpiricalCoordinateFact",
    "RoutingEligibilityFact", "WeightMeasureFact", "AuthoritySnapshot", "SourceUniverseRelation",
    "EmpiricalPredicate", "EmpiricalQuerySpec", "EmpiricalFact", "DiscoveryAuthority",
    "DiscoveryResultReceipt", "StructuralEmpiricalAdmission", "ReplayReceipt",
    "canonicalize_predicate_ast", "make_empirical_predicate", "is_public_object_family",
    "require_public_object_family", "assert_zero_actor_v3_v2_effect",
]
