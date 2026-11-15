"""Exact universal evidence binding over the accepted C1/N10E producer.

The contract implemented here is deliberately narrow: an exact typed
``EvidenceRequest`` identity K is resolved to either

* an actual canonical provider execution through
  ``rawlsing_next.pre553_empirical_possibility_provider``, or
* an authenticated cache entry whose full K, producer receipt, evidence
  preimage and consumer result were sealed by an earlier actual execution.

There is no target/depth lookup, no best-match fallback, no trace-only evaluator
claim and no caller-supplied evidence channel.  Eligibility, execution and
result are separate axes, and the support reducer keeps valid zero/null/empty
products distinct from ZERO_SUPPORT / missing structural state.

EPISTEMIC CEILING: this module binds and reduces TEST_ONLY source-local
evidence.  It issues no source permission, original scientific support, actor
state, F6/F7 method or production adoption.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field, replace
from decimal import Decimal
import hashlib
import hmac
import json
import secrets
from typing import Any, Callable, Iterable, Mapping, Sequence

from rawlsing_next.pre553_analytical_composition import (
    AnalyticalCompositionResult,
    ConditionValueBindingWitness,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_possibility_provider import (
    PROVIDER_STATE_EXACT,
    PROVIDER_STATE_REFUSED,
    EmpiricalPossibilitySliceProviderResult,
    provide_empirical_possibility_slice,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
    PositionedSubjectPossibilityResult,
    PossibilitySliceEvidence,
    SpecificityWalkbackStep,
    evaluate_positioned_subject_possibility,
)

REQUEST_CONTRACT_ID = "R61_UNIVERSAL_EVIDENCE_REQUEST@2"
RESULT_CONTRACT_ID = "R61_UNIVERSAL_EVIDENCE_RESULT@4"
SUMMARY_CONTRACT_ID = "R61_UNIVERSAL_SUPPORT_SUMMARY@2"
CACHE_SCHEMA = "R61_AUTHENTICATED_EVIDENCE_CACHE@5"
CACHE_OWNER_DESCRIPTOR_SCHEMA = "R61_CACHE_OWNER_DESCRIPTOR@1"
CACHE_OWNER_FIELDS = frozenset({
    "context_ref", "context", "actual_conditions", "producer_query_ref",
    "predicate_ref", "predicate_hash", "release_refs", "consumer_query_ref",
    "consumer_binding_fingerprint", "model_rule_hash", "source_universe_ref",
    "risk_set_ref", "target_ref",
})
CACHE_OWNER_DESCRIPTOR_FIELDS = frozenset({
    "schema", "request_key", "owner_identity_material", "owner_identity_hash",
    "validated_conditions", "descriptor_hash",
})
CACHE_SEAL_ALGORITHM = "SHA256_CANONICAL_FULLK_PRODUCER_CONSUMER_PREIMAGE"
CACHE_TRUST_ASSOCIATION = "FULL_K_PRODUCER_ASSOCIATION_SHA256"
CACHE_TRUST_ISSUER = "EPHEMERAL_ISSUER_HMAC_SHA256"
CACHE_TRUST_ADMISSION = "TRUSTED_OWNER_EVIDENCE_ADMISSION_HMAC_SHA256"
K_ENCODING_VERSION = "K_TAGGED_CANONICAL@2"

ELIGIBILITY_STATES = frozenset(
    {"ELIGIBLE", "PROHIBITED", "INAPPLICABLE_PROVED", "HELD", "UNKNOWN"}
)
EXECUTION_STATES = frozenset(
    {"NOT_STARTED", "PENDING", "COMPLETED", "UNSUPPORTED_RUNTIME", "ERROR"}
)
RESULT_STATES = frozenset(
    {
        "SUPPORTED",
        "OBSERVED_ZERO",
        "VALID_NULL",
        "DIFFUSE",
        "VALID_EMPTY",
        "ZERO_SUPPORT",
        "UNSUPPORTED",
        "UNKNOWN",
    }
)
PRODUCTIVE_RESULT_STATES = frozenset(
    {"SUPPORTED", "OBSERVED_ZERO", "VALID_NULL", "DIFFUSE", "VALID_EMPTY"}
)
PROVENANCE_CANONICAL = "CANONICAL_PRODUCER"
PROVENANCE_CACHE = "AUTHENTICATED_CACHE"
PROVENANCE_REFUSAL = "TYPED_REFUSAL"

REFUSAL_IDENTITY_MISMATCH = "IDENTITY_MISMATCH"
REFUSAL_NO_EXACT_BINDING = "NO_EXACT_PRODUCER_BINDING"
REFUSAL_MISSING_STRUCTURAL_STATE = "MISSING_STRUCTURAL_STATE"
REFUSAL_STALE_CACHE = "STALE_OR_UNAUTHENTICATED_CACHE"
REFUSAL_CONSUMER_ASSOCIATION = "CONSUMER_ASSOCIATION_MISMATCH"
REFUSAL_UNKNOWN_SUPPORT = "UNKNOWN_SUPPORT"
REFUSAL_UNSUPPORTED = "UNSUPPORTED_OR_UNAVAILABLE"
REFUSAL_FORBIDDEN = "FORBIDDEN_OR_INAPPLICABLE"


class EvidenceBindingError(Pre553IntegrityError):
    """Typed contract failure for ``pre553_universal_evidence_binding``."""


class EvidenceRequestShapeError(EvidenceBindingError):
    code = "EVIDENCE_REQUEST_SHAPE_ERROR"


class EvidenceBindingMismatch(EvidenceBindingError):
    code = "EVIDENCE_BINDING_MISMATCH"


class EvidenceCacheIntegrityError(EvidenceBindingError):
    code = "EVIDENCE_CACHE_INTEGRITY_ERROR"


class EvidenceAssociationError(EvidenceBindingError):
    code = "EVIDENCE_ASSOCIATION_ERROR"


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceRequestShapeError(f"{name} must be a non-empty string")
    out = value.strip()
    if out.lower() in {"latest", "default", "nearest", "fuzzy", "*"}:
        raise EvidenceRequestShapeError(f"{name} may not be mutable or fuzzy")
    return out


def _sha(value: Any, name: str) -> str:
    out = _text(value, name).lower()
    if len(out) != 64 or any(ch not in "0123456789abcdef" for ch in out):
        raise EvidenceRequestShapeError(f"{name} must be a sha256 hex digest")
    return out


def _ref(value: Any, name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Pre553IntegrityError as exc:
        raise EvidenceRequestShapeError(f"{name} must be ExactRef") from exc


def _refs(values: Iterable[Any], name: str) -> tuple[ExactRef, ...]:
    out = tuple(_ref(value, name) for value in values)
    if len({ref.key for ref in out}) != len(out):
        raise EvidenceRequestShapeError(f"{name} contains duplicate refs")
    return out


def _auth(value: Any, name: str) -> AuthorityRef:
    if not isinstance(value, AuthorityRef):
        raise EvidenceRequestShapeError(f"{name} must be AuthorityRef")
    return value


def _typed_from_material(material: Mapping[str, Any]) -> Any:
    tag = material.get("tag")
    if tag == "NULL":
        return None
    if tag == "BOOLEAN":
        return material["value"]
    if tag == "INTEGER":
        return int(material["value"])
    if tag == "DECIMAL":
        return Decimal(str(material["value"]))
    return material["value"]


@dataclass(frozen=True)
class TypedValue:
    """Tagged scalar value; never coerced between string/int/bool/null."""

    tag: str
    value: Any

    def __post_init__(self) -> None:
        if self.tag not in {"NULL", "STRING", "BOOLEAN", "INTEGER", "DECIMAL"}:
            raise EvidenceRequestShapeError(f"unsupported typed value tag {self.tag!r}")
        if self.tag == "NULL":
            if self.value is not None:
                raise EvidenceRequestShapeError("NULL typed value requires None")
        elif self.tag == "STRING":
            if not isinstance(self.value, str):
                raise EvidenceRequestShapeError("STRING typed value requires str")
        elif self.tag == "BOOLEAN":
            if type(self.value) is not bool:
                raise EvidenceRequestShapeError("BOOLEAN typed value requires bool")
        elif self.tag == "INTEGER":
            if type(self.value) is not int:
                raise EvidenceRequestShapeError("INTEGER typed value requires int")
        else:
            if not isinstance(self.value, Decimal):
                raise EvidenceRequestShapeError("DECIMAL typed value requires Decimal")

    @classmethod
    def build(cls, value: Any) -> "TypedValue":
        if value is None:
            return cls("NULL", None)
        if type(value) is bool:
            return cls("BOOLEAN", value)
        if type(value) is int:
            return cls("INTEGER", value)
        if isinstance(value, Decimal):
            return cls("DECIMAL", value)
        if isinstance(value, str):
            return cls("STRING", value)
        raise EvidenceRequestShapeError(
            f"unsupported typed value {type(value).__name__}; floats and objects "
            "are forbidden because they invite silent coercion"
        )

    def material(self) -> Mapping[str, Any]:
        return {
            "tag": self.tag,
            "value": None if self.value is None else str(self.value)
            if isinstance(self.value, Decimal)
            else self.value,
        }


@dataclass(frozen=True)
class OccurrenceKey:
    item: str
    option: str
    form: str
    repeat: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "item", _text(self.item, "occurrence.item"))
        object.__setattr__(self, "option", _text(self.option, "occurrence.option"))
        object.__setattr__(self, "form", _text(self.form, "occurrence.form"))
        object.__setattr__(self, "repeat", _text(self.repeat, "occurrence.repeat"))

    def material(self) -> Mapping[str, Any]:
        return {
            "item": self.item,
            "option": self.option,
            "form": self.form,
            "repeat": self.repeat,
        }


@dataclass(frozen=True)
class TypedCondition:
    occurrence: OccurrenceKey
    value: TypedValue
    domain_state_version: str
    conditioner_binding_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.occurrence, OccurrenceKey):
            raise EvidenceRequestShapeError("condition occurrence must be OccurrenceKey")
        if not isinstance(self.value, TypedValue):
            raise EvidenceRequestShapeError("condition value must be TypedValue")
        object.__setattr__(
            self,
            "domain_state_version",
            _text(self.domain_state_version, "condition.domain_state_version"),
        )
        if self.conditioner_binding_id is not None:
            object.__setattr__(
                self,
                "conditioner_binding_id",
                _text(self.conditioner_binding_id, "condition.conditioner_binding_id"),
            )

    def material(self) -> Mapping[str, Any]:
        return {
            "occurrence": self.occurrence.material(),
            "typed_value": self.value.material(),
            "domain_state_version": self.domain_state_version,
            "conditioner_binding_id": self.conditioner_binding_id,
        }


@dataclass(frozen=True)
class AdmittedEvidenceContext:
    """Explicit admitted source/operation context bound by the supervisor.

    The labels are declarations by the admitting boundary, not semantic
    inventions by this module.  Source/release/risk/target refs and authority
    refs must match the actual owner objects before a producer binding is
    accepted; the context hash is part of the cache preimage.
    """

    context_id: str
    admission_ref: ExactRef
    provenance_refs: tuple[ExactRef, ...]
    authority_refs: tuple[AuthorityRef, ...]
    source_id: str
    dataset_id: str
    wave_id: str
    edition: str
    byte_digest: str
    instrument_version: str
    sampled_unit: str
    reporting_unit: str
    link_refs: tuple[ExactRef, ...]
    estimand: str
    weight_method: str
    design_ref: ExactRef
    uncertainty_method: str
    direction: str
    role: str
    consumer_use: str
    grammar_version: str
    custody_ref: ExactRef
    observation_clock: str
    reference_clock: str
    as_of_clock: str
    publication_clock: str
    permission_ref: ExactRef
    source_universe_ref: ExactRef
    release_ref: ExactRef
    risk_set_ref: ExactRef
    target_ref: ExactRef
    occurrence_item: str
    occurrence_option: str
    occurrence_form: str
    occurrence_repeat: str
    domain_state_version: str

    def __post_init__(self) -> None:
        for name in (
            "context_id",
            "source_id",
            "dataset_id",
            "wave_id",
            "edition",
            "instrument_version",
            "sampled_unit",
            "reporting_unit",
            "estimand",
            "weight_method",
            "uncertainty_method",
            "direction",
            "role",
            "consumer_use",
            "grammar_version",
            "observation_clock",
            "reference_clock",
            "as_of_clock",
            "publication_clock",
            "occurrence_item",
            "occurrence_option",
            "occurrence_form",
            "occurrence_repeat",
            "domain_state_version",
        ):
            object.__setattr__(self, name, _text(getattr(self, name), name))
        object.__setattr__(self, "byte_digest", _sha(self.byte_digest, "context.byte_digest"))
        for name in (
            "admission_ref",
            "design_ref",
            "custody_ref",
            "permission_ref",
            "source_universe_ref",
            "release_ref",
            "risk_set_ref",
            "target_ref",
        ):
            object.__setattr__(self, name, _ref(getattr(self, name), name))
        province = _refs(self.provenance_refs, "context.provenance_refs")
        if not province:
            raise EvidenceRequestShapeError("context provenance refs may not be empty")
        object.__setattr__(self, "provenance_refs", province)
        object.__setattr__(self, "link_refs", _refs(self.link_refs, "context.link_refs"))
        auths = tuple(self.authority_refs)
        if not auths or any(not isinstance(x, AuthorityRef) for x in auths):
            raise EvidenceRequestShapeError("context authority refs required")
        object.__setattr__(self, "authority_refs", tuple(sorted(set(auths), key=lambda x: x.key)))

    def material(self) -> Mapping[str, Any]:
        return {
            "contract": "R61_ADMITTED_EVIDENCE_CONTEXT@1",
            "context_id": self.context_id,
            "admission_ref": self.admission_ref.as_dict(),
            "provenance_refs": [x.as_dict() for x in self.provenance_refs],
            "authority_refs": [x.as_dict() for x in self.authority_refs],
            "source_identity": {
                "source_id": self.source_id,
                "dataset_id": self.dataset_id,
                "wave_id": self.wave_id,
                "edition": self.edition,
                "byte_digest": self.byte_digest,
                "instrument_version": self.instrument_version,
            },
            "units": {
                "sampled_unit": self.sampled_unit,
                "reporting_unit": self.reporting_unit,
                "link_refs": [x.as_dict() for x in self.link_refs],
            },
            "measure": {
                "estimand": self.estimand,
                "weight_method": self.weight_method,
                "design_ref": self.design_ref.as_dict(),
                "uncertainty_method": self.uncertainty_method,
            },
            "authority": {
                "direction": self.direction,
                "role": self.role,
                "consumer_use": self.consumer_use,
                "permission_ref": self.permission_ref.as_dict(),
            },
            "bindings": {
                "grammar_version": self.grammar_version,
                "custody_ref": self.custody_ref.as_dict(),
                "source_universe_ref": self.source_universe_ref.as_dict(),
                "release_ref": self.release_ref.as_dict(),
                "risk_set_ref": self.risk_set_ref.as_dict(),
                "target_ref": self.target_ref.as_dict(),
            },
            "occurrence": {
                "item": self.occurrence_item,
                "option": self.occurrence_option,
                "form": self.occurrence_form,
                "repeat": self.occurrence_repeat,
            },
            "domain_state_version": self.domain_state_version,
        }

    @property
    def context_ref(self) -> ExactRef:
        digest = semantic_hash(self.material())
        return ExactRef(
            "R61_ADMITTED_EVIDENCE_CONTEXT@1",
            f"urn:rawlsing:r61:admitted-evidence-context:sha256:{digest}",
            digest,
        )


@dataclass(frozen=True)
class EvidenceRequest:
    """Exact request key K; every field participates in the canonical identity."""

    request_id: str
    schema_version: str
    claim_grade: str
    source_id: str
    dataset_id: str
    wave_id: str
    edition: str
    byte_digest: str
    instrument_version: str
    occurrence: OccurrenceKey
    sampled_unit: str
    reporting_unit: str
    link_refs: tuple[ExactRef, ...]
    risk_set_ref: ExactRef
    predicate_ref: ExactRef
    predicate_hash: str
    ordered_target_refs: tuple[ExactRef, ...]
    ordered_conditions: tuple[TypedCondition, ...]
    operation_class: str
    arity: int
    estimand: str
    weight_method: str
    design_ref: ExactRef
    uncertainty_method: str
    direction: str
    role: str
    consumer_use: str
    grammar_version: str
    model_rule_hash: str
    release_ref: ExactRef
    custody_ref: ExactRef
    observation_clock: str
    reference_clock: str
    as_of_clock: str
    publication_clock: str
    permission_ref: ExactRef
    producer_query_ref: ExactRef
    consumer_query_ref: ExactRef
    consumer_binding_fingerprint: str
    source_universe_ref: ExactRef
    target_ref: ExactRef

    def __post_init__(self) -> None:
        for name in (
            "request_id",
            "schema_version",
            "claim_grade",
            "source_id",
            "dataset_id",
            "wave_id",
            "edition",
            "instrument_version",
            "sampled_unit",
            "reporting_unit",
            "operation_class",
            "estimand",
            "weight_method",
            "uncertainty_method",
            "direction",
            "role",
            "consumer_use",
            "grammar_version",
            "observation_clock",
            "reference_clock",
            "as_of_clock",
            "publication_clock",
        ):
            object.__setattr__(self, name, _text(getattr(self, name), name))
        object.__setattr__(self, "byte_digest", _sha(self.byte_digest, "byte_digest"))
        object.__setattr__(self, "predicate_hash", _sha(self.predicate_hash, "predicate_hash"))
        object.__setattr__(
            self, "model_rule_hash", _sha(self.model_rule_hash, "model_rule_hash")
        )
        object.__setattr__(
            self,
            "consumer_binding_fingerprint",
            _sha(self.consumer_binding_fingerprint, "consumer_binding_fingerprint"),
        )
        if not isinstance(self.occurrence, OccurrenceKey):
            raise EvidenceRequestShapeError("occurrence must be OccurrenceKey")
        object.__setattr__(self, "link_refs", _refs(self.link_refs, "link_refs"))
        for name in (
            "risk_set_ref",
            "predicate_ref",
            "design_ref",
            "release_ref",
            "custody_ref",
            "permission_ref",
            "producer_query_ref",
            "consumer_query_ref",
            "source_universe_ref",
            "target_ref",
        ):
            object.__setattr__(self, name, _ref(getattr(self, name), name))
        targets = _refs(self.ordered_target_refs, "ordered_target_refs")
        if not targets:
            raise EvidenceRequestShapeError("ordered_target_refs may not be empty")
        object.__setattr__(self, "ordered_target_refs", targets)
        conditions = tuple(self.ordered_conditions)
        if not conditions:
            raise EvidenceRequestShapeError("ordered_conditions may not be empty")
        if any(not isinstance(x, TypedCondition) for x in conditions):
            raise EvidenceRequestShapeError("ordered_conditions must be TypedCondition")
        occurrences = [x.occurrence.material() for x in conditions]
        if len({semantic_hash(x) for x in occurrences}) != len(occurrences):
            raise EvidenceRequestShapeError("ambiguous duplicate condition occurrence")
        object.__setattr__(self, "ordered_conditions", conditions)
        if type(self.arity) is not int or self.arity != len(targets):
            raise EvidenceRequestShapeError(
                "arity must equal the ordered target tuple length"
            )
        if self.target_ref != targets[0]:
            raise EvidenceRequestShapeError(
                "target_ref must be the first ordered target (single-target C1 grain)"
            )

    def material(self) -> Mapping[str, Any]:
        return {
            "encoding": K_ENCODING_VERSION,
            "contract": REQUEST_CONTRACT_ID,
            "request_id": self.request_id,
            "schema_version": self.schema_version,
            "claim_grade": self.claim_grade,
            "source_identity": {
                "source_id": self.source_id,
                "dataset_id": self.dataset_id,
                "wave_id": self.wave_id,
                "edition": self.edition,
                "byte_digest": self.byte_digest,
                "instrument_version": self.instrument_version,
            },
            "occurrence": self.occurrence.material(),
            "units": {
                "sampled_unit": self.sampled_unit,
                "reporting_unit": self.reporting_unit,
                "link_refs": [x.as_dict() for x in self.link_refs],
            },
            "applicability": {
                "risk_set_ref": self.risk_set_ref.as_dict(),
                "predicate_ref": self.predicate_ref.as_dict(),
                "predicate_hash": self.predicate_hash,
            },
            "query": {
                "ordered_target_refs": [x.as_dict() for x in self.ordered_target_refs],
                "ordered_conditions": [x.material() for x in self.ordered_conditions],
                "operation_class": self.operation_class,
                "arity": self.arity,
            },
            "measure": {
                "estimand": self.estimand,
                "weight_method": self.weight_method,
                "design_ref": self.design_ref.as_dict(),
                "uncertainty_method": self.uncertainty_method,
            },
            "authority": {
                "direction": self.direction,
                "role": self.role,
                "consumer_use": self.consumer_use,
                "permission_ref": self.permission_ref.as_dict(),
            },
            "bindings": {
                "grammar_version": self.grammar_version,
                "model_rule_hash": self.model_rule_hash,
                "release_ref": self.release_ref.as_dict(),
                "custody_ref": self.custody_ref.as_dict(),
                "producer_query_ref": self.producer_query_ref.as_dict(),
                "consumer_query_ref": self.consumer_query_ref.as_dict(),
                "consumer_binding_fingerprint": self.consumer_binding_fingerprint,
                "source_universe_ref": self.source_universe_ref.as_dict(),
                "target_ref": self.target_ref.as_dict(),
            },
            "clocks": {
                "observation": self.observation_clock,
                "reference": self.reference_clock,
                "as_of": self.as_of_clock,
                "publication": self.publication_clock,
            },
        }

    @property
    def key(self) -> str:
        return semantic_hash(self.material())

    @property
    def key_ref(self) -> ExactRef:
        return ExactRef(
            REQUEST_CONTRACT_ID,
            f"urn:rawlsing:r61:evidence-request:sha256:{self.key}",
            self.key,
        )

    @classmethod
    def from_material(cls, material: Mapping[str, Any]) -> "EvidenceRequest":
        if not isinstance(material, Mapping):
            raise EvidenceRequestShapeError("request material must be a mapping")
        if material.get("contract") != REQUEST_CONTRACT_ID:
            raise EvidenceRequestShapeError("unexpected request contract")
        source = material["source_identity"]
        units = material["units"]
        applicability = material["applicability"]
        query = material["query"]
        measure = material["measure"]
        authority = material["authority"]
        bindings = material["bindings"]
        clocks = material["clocks"]
        conditions = tuple(
            TypedCondition(
                OccurrenceKey(
                    item["occurrence"]["item"],
                    item["occurrence"]["option"],
                    item["occurrence"]["form"],
                    item["occurrence"]["repeat"],
                ),
                TypedValue(item["typed_value"]["tag"], _typed_from_material(item["typed_value"])),
                item["domain_state_version"],
                item["conditioner_binding_id"],
            )
            for item in query["ordered_conditions"]
        )
        occurrence = material["occurrence"]
        return cls(
            request_id=material["request_id"],
            schema_version=material["schema_version"],
            claim_grade=material["claim_grade"],
            source_id=source["source_id"],
            dataset_id=source["dataset_id"],
            wave_id=source["wave_id"],
            edition=source["edition"],
            byte_digest=source["byte_digest"],
            instrument_version=source["instrument_version"],
            occurrence=OccurrenceKey(
                occurrence["item"], occurrence["option"], occurrence["form"], occurrence["repeat"]
            ),
            sampled_unit=units["sampled_unit"],
            reporting_unit=units["reporting_unit"],
            link_refs=tuple(ExactRef(**x) for x in units["link_refs"]),
            risk_set_ref=ExactRef(**applicability["risk_set_ref"]),
            predicate_ref=ExactRef(**applicability["predicate_ref"]),
            predicate_hash=applicability["predicate_hash"],
            ordered_target_refs=tuple(
                ExactRef(**x) for x in query["ordered_target_refs"]
            ),
            ordered_conditions=conditions,
            operation_class=query["operation_class"],
            arity=query["arity"],
            estimand=measure["estimand"],
            weight_method=measure["weight_method"],
            design_ref=ExactRef(**measure["design_ref"]),
            uncertainty_method=measure["uncertainty_method"],
            direction=authority["direction"],
            role=authority["role"],
            consumer_use=authority["consumer_use"],
            grammar_version=bindings["grammar_version"],
            model_rule_hash=bindings["model_rule_hash"],
            release_ref=ExactRef(**bindings["release_ref"]),
            custody_ref=ExactRef(**bindings["custody_ref"]),
            observation_clock=clocks["observation"],
            reference_clock=clocks["reference"],
            as_of_clock=clocks["as_of"],
            publication_clock=clocks["publication"],
            permission_ref=ExactRef(**authority["permission_ref"]),
            producer_query_ref=ExactRef(**bindings["producer_query_ref"]),
            consumer_query_ref=ExactRef(**bindings["consumer_query_ref"]),
            consumer_binding_fingerprint=bindings["consumer_binding_fingerprint"],
            source_universe_ref=ExactRef(**bindings["source_universe_ref"]),
            target_ref=ExactRef(**bindings["target_ref"]),
        )

    def changed(self, **changes: Any) -> "EvidenceRequest":
        from dataclasses import replace

        return replace(self, **changes)


def request_from_empirical_case(
    *,
    request_id: str,
    claim_grade: str,
    source_id: str,
    dataset_id: str,
    wave_id: str,
    edition: str,
    byte_digest: str,
    instrument_version: str,
    occurrence: OccurrenceKey,
    sampled_unit: str,
    reporting_unit: str,
    link_refs: Iterable[ExactRef] = (),
    estimand: str,
    weight_method: str,
    design_ref: ExactRef,
    uncertainty_method: str,
    direction: str,
    role: str,
    consumer_use: str,
    grammar_version: str,
    custody_ref: ExactRef,
    observation_clock: str,
    reference_clock: str,
    as_of_clock: str,
    publication_clock: str,
    permission_ref: ExactRef,
    ordered_conditions: Sequence[TypedCondition],
    empirical_query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    consumer_query: PositionedSubjectPossibilityQuery,
    model_rule: PositionedSubjectPossibilityModelRule,
    consumer_binding_fingerprint: str | None = None,
) -> EvidenceRequest:
    """Build K from actual accepted owner objects (no copied producer hashes)."""

    if len(consumer_query.conditioner_bindings) not in {1}:
        if consumer_binding_fingerprint is None:
            raise EvidenceRequestShapeError(
                "multi-conditioner requests require the exact consumer fingerprint"
            )
        raise EvidenceRequestShapeError(
            "R61 C1 binding follows the accepted single-conditioner grain"
        )
    binding = consumer_query.conditioner_bindings[0]
    release_ref = consumer_query.release_ref
    return EvidenceRequest(
        request_id=request_id,
        schema_version="R61_EVIDENCE_SCHEMA@1",
        claim_grade=claim_grade,
        source_id=source_id,
        dataset_id=dataset_id,
        wave_id=wave_id,
        edition=edition,
        byte_digest=byte_digest,
        instrument_version=instrument_version,
        occurrence=occurrence,
        sampled_unit=sampled_unit,
        reporting_unit=reporting_unit,
        link_refs=tuple(link_refs),
        risk_set_ref=exact_ref(empirical_query.risk_set_ref, "risk_set_ref"),
        predicate_ref=predicate.ref,
        predicate_hash=predicate.predicate_hash,
        ordered_target_refs=tuple(
            exact_ref(target, "target_ref") for target in empirical_query.target_refs
        ),
        ordered_conditions=tuple(ordered_conditions),
        operation_class="POSITIONED_SUBJECT_EXACT_CONDITIONAL",
        arity=len(tuple(empirical_query.target_refs)),
        estimand=estimand,
        weight_method=weight_method,
        design_ref=design_ref,
        uncertainty_method=uncertainty_method,
        direction=direction,
        role=role,
        consumer_use=consumer_use,
        grammar_version=grammar_version,
        model_rule_hash=model_rule.rule_hash,
        release_ref=release_ref,
        custody_ref=custody_ref,
        observation_clock=observation_clock,
        reference_clock=reference_clock,
        as_of_clock=as_of_clock,
        publication_clock=publication_clock,
        permission_ref=permission_ref,
        producer_query_ref=empirical_query.ref,
        consumer_query_ref=consumer_query.ref,
        consumer_binding_fingerprint=(
            consumer_binding_fingerprint
            if consumer_binding_fingerprint is not None
            else semantic_hash(binding.material())
        ),
        source_universe_ref=consumer_query.source_universe_ref,
        target_ref=consumer_query.target_ref,
    )


def _consumer_binding_fingerprint(
    consumer_query: PositionedSubjectPossibilityQuery,
    witness: ConditionValueBindingWitness,
) -> str:
    identity = canonicalize(witness.identity_material)
    if "consumer_binding_materials" in identity:
        return semantic_hash(
            [binding.material() for binding in consumer_query.conditioner_bindings]
        )
    if len(consumer_query.conditioner_bindings) != 1:
        raise EvidenceBindingMismatch(
            "legacy single-binding witness cannot cover multiple conditioners"
        )
    return semantic_hash(consumer_query.conditioner_bindings[0].material())


def _value_bearing_leaves(predicate: EmpiricalPredicate) -> tuple[Mapping[str, Any], ...]:
    ast = canonicalize(predicate.predicate_ast)
    leaves: list[Mapping[str, Any]] = []

    def collect(node: Mapping[str, Any]) -> None:
        if (
            node.get("op") == "LEAF"
            and node.get("leaf_type") in {"SURVEY_RESPONSE_EVENT", "EMPIRICAL_POSITION_COORDINATE"}
            and node.get("operator") == "EQ"
            and "exact_value" in node
        ):
            leaves.append(node)
        elif node.get("op") in {"AND", "OR", "NOT"}:
            for child in node.get("children", ()):
                collect(child)

    collect(ast)
    return tuple(leaves)


def _leaf_semantic_ref(leaf: Mapping[str, Any]) -> Mapping[str, Any]:
    if leaf.get("leaf_type") == "EMPIRICAL_POSITION_COORDINATE":
        return leaf.get("coordinate_semantic_ref")
    return leaf.get("question_semantic_ref")


def _actual_condition_identities(binding: "EmpiricalProducerBinding") -> tuple[Mapping[str, Any], ...]:
    leaves = _value_bearing_leaves(binding.predicate)
    bindings = binding.consumer_query.conditioner_bindings
    if len(leaves) != len(bindings):
        raise EvidenceBindingMismatch(
            "actual producer leaf/conditioner count differs from consumer bindings"
        )
    out = []
    # Predicate AND leaves are canonically sorted; consumer bindings preserve
    # requested prefix order. Associate by exact coordinate, never position.
    remaining = list(leaves)
    for conditioner in bindings:
        matches = [leaf for leaf in remaining
                   if canonicalize(_leaf_semantic_ref(leaf))
                   == canonicalize(conditioner.empirical_coordinate_ref.as_dict())]
        if len(matches) != 1:
            raise EvidenceBindingMismatch("producer leaf/conditioner exact coordinate association ambiguous")
        leaf = matches[0]
        remaining.remove(leaf)
        semantic_ref = _leaf_semantic_ref(leaf)
        if not isinstance(semantic_ref, Mapping):
            raise EvidenceBindingMismatch("producer leaf lacks a semantic ref")
        exact = leaf.get("exact_value")
        value = TypedValue.build(exact)
        out.append(
            {
                "conditioner_binding_id": conditioner.binding_id,
                "occurrence": {
                    "item": exact,
                    "option": str(exact),
                    "form": binding.context.occurrence_form,
                    "repeat": binding.context.occurrence_repeat,
                },
                "leaf_semantic_ref": canonicalize(semantic_ref),
                "typed_value": value.material(),
                "domain_state_version": binding.context.domain_state_version,
            }
        )
    return tuple(out)


def _item_matches_leaf(item: str, leaf_semantic_ref: Mapping[str, Any]) -> bool:
    object_id = leaf_semantic_ref.get("object_id")
    if not isinstance(object_id, str):
        return False
    tail = object_id.rsplit(":", 1)[-1]
    return tail == item or tail.endswith("-" + item) or tail.endswith("_" + item)


def _context_matches_request(context: AdmittedEvidenceContext, request: EvidenceRequest) -> bool:
    labels = (
        "source_id", "dataset_id", "wave_id", "edition", "byte_digest",
        "instrument_version", "sampled_unit", "reporting_unit", "estimand",
        "weight_method", "uncertainty_method", "direction", "role",
        "consumer_use", "grammar_version", "observation_clock", "reference_clock",
        "as_of_clock", "publication_clock",
    )
    for name in labels:
        if getattr(context, name) != getattr(request, name):
            return False
    if context.link_refs != request.link_refs:
        return False
    for name in ("design_ref", "custody_ref", "permission_ref", "source_universe_ref", "release_ref", "risk_set_ref", "target_ref"):
        if getattr(context, name) != getattr(request, name):
            return False
    return (
        context.occurrence_item == request.occurrence.item
        and context.occurrence_option == request.occurrence.option
        and context.occurrence_form == request.occurrence.form
        and context.occurrence_repeat == request.occurrence.repeat
    )


@dataclass(frozen=True)
class EmpiricalProducerBinding:
    """Exact actual-provider determinants for one registered request key."""

    request: EvidenceRequest
    repository: Any
    empirical_query: EmpiricalQuerySpec
    predicate: EmpiricalPredicate
    authority_registry: Any
    release_refs: tuple[ExactRef, ...]
    consumer_query: PositionedSubjectPossibilityQuery
    model_rule: PositionedSubjectPossibilityModelRule
    condition_binding_witness: ConditionValueBindingWitness
    context: AdmittedEvidenceContext
    admission: TrustedOwnerAdmission | None = None
    producer: Callable[..., EmpiricalPossibilitySliceProviderResult] = field(
        default=provide_empirical_possibility_slice, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        if not isinstance(self.request, EvidenceRequest):
            raise EvidenceBindingMismatch("binding.request must be EvidenceRequest")
        if not isinstance(self.context, AdmittedEvidenceContext):
            raise EvidenceBindingMismatch("binding.context must be AdmittedEvidenceContext")
        if tuple(sorted(self.release_refs, key=lambda x: x.key)) != (self.context.release_ref,):
            raise EvidenceBindingMismatch("actual release refs differ from admitted context")
        if self.context.source_universe_ref != self.consumer_query.source_universe_ref:
            raise EvidenceBindingMismatch("admitted context source universe mismatch")
        if self.context.release_ref != self.consumer_query.release_ref:
            raise EvidenceBindingMismatch("admitted context release mismatch")
        if self.context.risk_set_ref != exact_ref(
            self.empirical_query.risk_set_ref, "risk_set_ref"
        ):
            raise EvidenceBindingMismatch("admitted context risk set mismatch")
        if self.context.target_ref != self.consumer_query.target_ref:
            raise EvidenceBindingMismatch("admitted context target mismatch")
        if self.context.authority_refs != tuple(
            sorted(set(self.predicate.authority_snapshot_refs), key=lambda x: x.key)
        ):
            raise EvidenceBindingMismatch(
                "admitted context authority refs differ from the actual predicate authorities"
            )
        if len(self.context.link_refs) != len(set(self.context.link_refs)):
            raise EvidenceBindingMismatch("admitted context link refs are ambiguous")

    def mismatch_reason(self, request: EvidenceRequest) -> str | None:
        if request.material() != self.request.material() or request.key != self.request.key:
            return "registered request material differs from requested K"
        if not _context_matches_request(self.context, request):
            return "request labels/clocks/currentness differ from admitted context"
        if request.consumer_query_ref != self.consumer_query.ref:
            return "request consumer query ref mismatch"
        if request.producer_query_ref != self.empirical_query.ref:
            return "request producer query ref mismatch"
        if request.predicate_ref != self.predicate.ref:
            return "request predicate ref mismatch"
        if request.predicate_hash != self.predicate.predicate_hash:
            return "request predicate hash mismatch"
        if request.release_ref != self.context.release_ref:
            return "request release ref mismatch"
        if request.model_rule_hash != self.model_rule.rule_hash:
            return "request model rule hash mismatch"
        if request.consumer_binding_fingerprint != _consumer_binding_fingerprint(
            self.consumer_query, self.condition_binding_witness
        ):
            return "request consumer binding fingerprint mismatch"
        if request.source_universe_ref != self.consumer_query.source_universe_ref:
            return "request source universe mismatch"
        if request.target_ref != self.consumer_query.target_ref:
            return "request target ref mismatch"
        if request.risk_set_ref != exact_ref(self.empirical_query.risk_set_ref, "risk_set_ref"):
            return "request risk set mismatch"
        if tuple(request.ordered_target_refs) != tuple(
            exact_ref(target, "target_ref") for target in self.empirical_query.target_refs
        ):
            return "request ordered targets mismatch"
        actual = _actual_condition_identities(self)
        if len(request.ordered_conditions) != len(actual):
            return "request condition arity differs from actual producer determinants"
        for index, (condition, identity) in enumerate(zip(request.ordered_conditions, actual)):
            if condition.conditioner_binding_id != identity["conditioner_binding_id"]:
                return f"condition {index} binding id mismatch"
            if condition.domain_state_version != identity["domain_state_version"]:
                return f"condition {index} domain/state version mismatch"
            if condition.value.material() != identity["typed_value"]:
                return f"condition {index} typed value mismatch"
            occurrence = identity["occurrence"]
            if condition.occurrence.option != occurrence["option"]:
                return f"condition {index} option/value mismatch"
            if condition.occurrence.form != occurrence["form"] or condition.occurrence.repeat != occurrence["repeat"]:
                return f"condition {index} form/repeat mismatch"
            if not _item_matches_leaf(condition.occurrence.item, identity["leaf_semantic_ref"]):
                return f"condition {index} item does not match actual producer question"
        return None

    def owner_identity_material(self) -> Mapping[str, Any]:
        return {
            "context_ref": self.context.context_ref.as_dict(),
            "context": canonicalize(self.context.material()),
            "actual_conditions": [canonicalize(x) for x in _actual_condition_identities(self)],
            "producer_query_ref": self.empirical_query.ref.as_dict(),
            "predicate_ref": self.predicate.ref.as_dict(),
            "predicate_hash": self.predicate.predicate_hash,
            "release_refs": [x.as_dict() for x in self.release_refs],
            "consumer_query_ref": self.consumer_query.ref.as_dict(),
            "consumer_binding_fingerprint": _consumer_binding_fingerprint(
                self.consumer_query, self.condition_binding_witness
            ),
            "model_rule_hash": self.model_rule.rule_hash,
            "source_universe_ref": exact_ref(
                self.empirical_query.empirical_universe_refs[0], "source_universe_ref"
            ).as_dict(),
            "risk_set_ref": exact_ref(
                self.empirical_query.risk_set_ref, "risk_set_ref"
            ).as_dict(),
            "target_ref": self.consumer_query.target_ref.as_dict(),
        }

    @property
    def owner_identity_hash(self) -> str:
        return semantic_hash(self.owner_identity_material())

    def identity_material(self) -> Mapping[str, Any]:
        return {
            "request_key": self.request.key,
            **self.owner_identity_material(),
            "validated_conditions": [condition.material() for condition in self.request.ordered_conditions],
            "admission": None
            if self.admission is None
            else self.admission.material(),
        }

    @property
    def binding_hash(self) -> str:
        return semantic_hash(self.identity_material())


@dataclass(frozen=True)
class EvidenceResult:
    request_key: str
    eligibility_state: str
    execution_state: str
    result_state: str
    provenance: str
    denominator: int | None = None
    cells: tuple[Mapping[str, Any], ...] = ()
    evidence_ref: ExactRef | None = None
    producer_receipt_ref: ExactRef | None = None
    producer_fact_ref: ExactRef | None = None
    producer_fact_state: str | None = None
    consumer_query_ref: ExactRef | None = None
    consumer_result_state: str | None = None
    consumer_result_hash: str | None = None
    consumer_values_read: Mapping[str, Any] | None = None
    uncertainty_state: str | None = None
    typed_refusal: str | None = None
    execution_envelope: ExecutedEvidenceEnvelope | None = None
    envelope_signature: str | None = None
    evidence_object: Any = field(default=None, repr=False, compare=False)
    consumer_query_object: Any = field(default=None, repr=False, compare=False)
    model_rule_object: Any = field(default=None, repr=False, compare=False)
    consumer_result_object: Any = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_key", _sha(self.request_key, "request_key"))
        if self.eligibility_state not in ELIGIBILITY_STATES:
            raise EvidenceBindingError("invalid eligibility state")
        if self.execution_state not in EXECUTION_STATES:
            raise EvidenceBindingError("invalid execution state")
        if self.result_state not in RESULT_STATES:
            raise EvidenceBindingError("invalid result state")
        if self.provenance not in {
            PROVENANCE_CANONICAL,
            PROVENANCE_CACHE,
            PROVENANCE_REFUSAL,
        }:
            raise EvidenceBindingError("invalid result provenance")
        if self.denominator is not None and (
            type(self.denominator) is not int or self.denominator < 0
        ):
            raise EvidenceBindingError("denominator must be nonnegative int or None")
        object.__setattr__(
            self,
            "cells",
            tuple(canonicalize(cell) for cell in self.cells),
        )
        if self.result_state == "SUPPORTED":
            if self.provenance not in {PROVENANCE_CANONICAL, PROVENANCE_CACHE}:
                raise EvidenceBindingError("SUPPORTED requires producer/cache provenance")
            if self.typed_refusal is not None:
                raise EvidenceBindingError("SUPPORTED may not carry a typed refusal")
            if not self.denominator or self.denominator <= 0:
                raise EvidenceBindingError("SUPPORTED requires a positive denominator")
            if not self.cells:
                raise EvidenceBindingError("SUPPORTED requires actual cells")
            if (
                self.evidence_ref is None
                or self.consumer_result_hash is None
                or self.consumer_values_read is None
            ):
                raise EvidenceBindingError(
                    "SUPPORTED requires evidence, consumer result and values-read"
                )
            if self.execution_envelope is None or self.envelope_signature is None:
                raise EvidenceBindingError(
                    "SUPPORTED requires a signed complete execution envelope"
                )
        else:
            if self.evidence_ref is not None:
                raise EvidenceBindingError(
                    "non-SUPPORTED result may not carry exact evidence"
                )
            if self.consumer_values_read is not None:
                raise EvidenceBindingError(
                    "non-SUPPORTED result may not carry consumer values-read"
                )
            if self.consumer_result_hash is not None:
                raise EvidenceBindingError(
                    "non-SUPPORTED result may not carry a consumer result hash"
                )
            if self.typed_refusal is None and self.result_state in {
                "ZERO_SUPPORT",
                "UNSUPPORTED",
                "UNKNOWN",
            }:
                raise EvidenceBindingError(
                    "refused/unknown result requires an explicit typed refusal"
                )
        if self.result_state == "ZERO_SUPPORT" and self.denominator not in {0, None}:
            raise EvidenceBindingError("ZERO_SUPPORT requires a zero denominator")

    @property
    def positive_support(self) -> bool:
        return self.result_state == "SUPPORTED"

    @property
    def productive(self) -> bool:
        return (
            self.eligibility_state == "ELIGIBLE"
            and self.execution_state == "COMPLETED"
            and self.result_state in PRODUCTIVE_RESULT_STATES
        )

    def material(self) -> Mapping[str, Any]:
        return {
            "contract": RESULT_CONTRACT_ID,
            "request_key": self.request_key,
            "eligibility_state": self.eligibility_state,
            "execution_state": self.execution_state,
            "result_state": self.result_state,
            "provenance": self.provenance,
            "denominator": self.denominator,
            "cells": [canonicalize(cell) for cell in self.cells],
            "evidence_ref": None if self.evidence_ref is None else self.evidence_ref.as_dict(),
            "producer_receipt_ref": (
                None if self.producer_receipt_ref is None
                else self.producer_receipt_ref.as_dict()
            ),
            "producer_fact_ref": (
                None if self.producer_fact_ref is None
                else self.producer_fact_ref.as_dict()
            ),
            "producer_fact_state": self.producer_fact_state,
            "consumer_query_ref": (
                None if self.consumer_query_ref is None
                else self.consumer_query_ref.as_dict()
            ),
            "consumer_result_state": self.consumer_result_state,
            "consumer_result_hash": self.consumer_result_hash,
            "consumer_values_read": canonicalize(self.consumer_values_read)
            if self.consumer_values_read is not None
            else None,
            "uncertainty_state": self.uncertainty_state,
            "typed_refusal": self.typed_refusal,
            "execution_envelope_ref": (
                None if self.execution_envelope is None else self.execution_envelope.ref.as_dict()
            ),
            "envelope_signature": self.envelope_signature,
        }

    @property
    def result_identity_hash(self) -> str:
        return semantic_hash(self.material())


def _result_refusal(
    request: EvidenceRequest,
    refusal: str,
    *,
    eligibility: str = "ELIGIBLE",
    execution: str = "COMPLETED",
    result_state: str = "UNKNOWN",
    denominator: int | None = None,
    producer_receipt_ref: ExactRef | None = None,
    producer_fact_ref: ExactRef | None = None,
    producer_fact_state: str | None = None,
    uncertainty_state: str | None = None,
) -> EvidenceResult:
    return EvidenceResult(
        request_key=request.key,
        eligibility_state=eligibility,
        execution_state=execution,
        result_state=result_state,
        provenance=PROVENANCE_REFUSAL,
        denominator=denominator,
        producer_receipt_ref=producer_receipt_ref,
        producer_fact_ref=producer_fact_ref,
        producer_fact_state=producer_fact_state,
        uncertainty_state=uncertainty_state,
        typed_refusal=refusal,
    )


def _provider_result_state(state: str) -> tuple[str, str, str]:
    if state == "VALID_EMPTY":
        return ("ELIGIBLE", "COMPLETED", "VALID_EMPTY")
    if state == "ZERO_SUPPORT" or state == "OBSERVED_ZERO":
        return ("ELIGIBLE", "COMPLETED", "ZERO_SUPPORT")
    if state in {"UNRESOLVED", "UNKNOWN"}:
        return ("UNKNOWN", "COMPLETED", "UNKNOWN")
    if state in {"NOT_APPLICABLE", "INAPPLICABLE"}:
        return ("INAPPLICABLE_PROVED", "COMPLETED", "UNSUPPORTED")
    if state in {"UNAVAILABLE"}:
        return ("HELD", "COMPLETED", "UNSUPPORTED")
    if state in {"PROHIBITED"}:
        return ("PROHIBITED", "COMPLETED", "UNSUPPORTED")
    return ("ELIGIBLE", "UNSUPPORTED_RUNTIME", "UNSUPPORTED")


def _cells(composition: AnalyticalCompositionResult) -> tuple[Mapping[str, Any], ...]:
    return tuple(
        {
            "cell": cell.get("cell"),
            "cell_state": cell.get("cell_state"),
            "raw_numerator_support": cell.get("raw_numerator_support"),
            "raw_probability_exact_fraction": cell.get(
                "raw_probability_exact_fraction"
            ),
        }
        for cell in composition.complete_cell_geometry
    )


def _consumer_values(
    request: EvidenceRequest,
    evidence: PossibilitySliceEvidence,
    consumer_result: PositionedSubjectPossibilityResult,
    denominator: int,
    cells: Iterable[Mapping[str, Any]],
) -> Mapping[str, Any]:
    return {
        "schema": "R61_EVIDENCE_CONSUMER_VALUES_READ@1",
        "request_key": request.key,
        "target_ref": request.target_ref.as_dict(),
        "ordered_conditions": [x.material() for x in request.ordered_conditions],
        "direction": request.direction,
        "role": request.role,
        "consumer_query_ref": request.consumer_query_ref.as_dict(),
        "evidence_ref": evidence.evidence_ref.as_dict(),
        "result_state": consumer_result.result_state,
        "result_hash": consumer_result.result_hash,
        "retained_conditioner_ids": list(evidence.retained_conditioner_ids),
        "denominator": denominator,
        "cells": [canonicalize(cell) for cell in cells],
        "model_rule_hash": request.model_rule_hash,
    }


def _cell_core(cell: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "cell": cell.get("cell"),
        "cell_state": cell.get("cell_state"),
        "raw_numerator_support": cell.get("raw_numerator_support"),
        "raw_probability_exact_fraction": cell.get("raw_probability_exact_fraction"),
    }


def _evidence_cells(evidence: PossibilitySliceEvidence) -> tuple[Mapping[str, Any], ...]:
    geometry = canonicalize(evidence.geometry or {})
    return tuple(_cell_core(cell) for cell in geometry.get("cells", ()))


def _context_material_matches_request(
    material: Mapping[str, Any], request: EvidenceRequest
) -> bool:
    try:
        source = material["source_identity"]
        units = material["units"]
        measure = material["measure"]
        authority = material["authority"]
        bindings = material["bindings"]
        occurrence = material["occurrence"]
        labels = {
            "source_id": source["source_id"],
            "dataset_id": source["dataset_id"],
            "wave_id": source["wave_id"],
            "edition": source["edition"],
            "byte_digest": source["byte_digest"],
            "instrument_version": source["instrument_version"],
            "sampled_unit": units["sampled_unit"],
            "reporting_unit": units["reporting_unit"],
            "estimand": measure["estimand"],
            "weight_method": measure["weight_method"],
            "uncertainty_method": measure["uncertainty_method"],
            "direction": authority["direction"],
            "role": authority["role"],
            "consumer_use": authority["consumer_use"],
            "grammar_version": bindings["grammar_version"],
        }
    except (KeyError, TypeError):
        return False
    for name, value in labels.items():
        if getattr(request, name) != value:
            return False
    if [ExactRef(**x) for x in units["link_refs"]] != list(request.link_refs):
        return False
    ref_fields = {
        "design_ref": measure["design_ref"],
        "custody_ref": bindings["custody_ref"],
        "permission_ref": authority["permission_ref"],
        "source_universe_ref": bindings["source_universe_ref"],
        "release_ref": bindings["release_ref"],
        "risk_set_ref": bindings["risk_set_ref"],
        "target_ref": bindings["target_ref"],
    }
    for name, value in ref_fields.items():
        if getattr(request, name) != ExactRef(**value):
            return False
    return (
        request.occurrence.item == occurrence["item"]
        and request.occurrence.option == occurrence["option"]
        and request.occurrence.form == occurrence["form"]
        and request.occurrence.repeat == occurrence["repeat"]
    )


R61_TRUST_DOMAIN = "R61_TEST_ONLY_TRUSTED_HOST_DOMAIN"
R61_TRUST_DOMAIN_VERSION = "1"
R61_TRUST_GRADE = "TEST_ONLY_SCOPED_LOCAL_TRUSTED_HOST"


@dataclass(frozen=True)
class TrustedOwnerAdmission:
    authority_id: str
    scope: str
    context_ref: ExactRef
    producer_identity_hash: str
    evidence_ref: ExactRef | None
    evidence_content_hash: str | None
    token: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "authority_id", _text(self.authority_id, "admission.authority_id"))
        if self.scope not in {"PRODUCER", "EVIDENCE"}:
            raise EvidenceBindingError("admission scope must be PRODUCER or EVIDENCE")
        if not isinstance(self.context_ref, ExactRef):
            raise EvidenceBindingError("admission context_ref must be ExactRef")
        object.__setattr__(
            self, "producer_identity_hash", _sha(self.producer_identity_hash, "admission.producer_identity_hash")
        )
        object.__setattr__(self, "token", _sha(self.token, "admission.token"))
        if self.evidence_ref is not None and not isinstance(self.evidence_ref, ExactRef):
            raise EvidenceBindingError("admission evidence_ref must be ExactRef or null")
        if self.evidence_content_hash is not None:
            object.__setattr__(
                self,
                "evidence_content_hash",
                _sha(self.evidence_content_hash, "admission.evidence_content_hash"),
            )

    def material(self, *, include_token: bool = True) -> Mapping[str, Any]:
        out = {
            "schema": "R61_TRUSTED_OWNER_ADMISSION@2",
            "authority_id": self.authority_id,
            "scope": self.scope,
            "context_ref": self.context_ref.as_dict(),
            "producer_identity_hash": self.producer_identity_hash,
            "evidence_ref": None if self.evidence_ref is None else self.evidence_ref.as_dict(),
            "evidence_content_hash": self.evidence_content_hash,
        }
        if include_token:
            out["token"] = self.token
        return out

    @classmethod
    def from_material(cls, material: Mapping[str, Any]) -> "TrustedOwnerAdmission":
        try:
            return cls(
                authority_id=material["authority_id"],
                scope=material["scope"],
                context_ref=ExactRef(**material["context_ref"]),
                producer_identity_hash=material["producer_identity_hash"],
                evidence_ref=None
                if material["evidence_ref"] is None
                else ExactRef(**material["evidence_ref"]),
                evidence_content_hash=material["evidence_content_hash"],
                token=material["token"],
            )
        except (KeyError, TypeError) as exc:
            raise EvidenceCacheIntegrityError("malformed trusted owner admission") from exc


@dataclass(frozen=True)
class ExecutedEvidenceEnvelope:
    request_material: Mapping[str, Any]
    request_key: str
    context_ref: ExactRef
    context_material: Mapping[str, Any]
    owner_identity_material: Mapping[str, Any]
    owner_identity_hash: str
    source_universe_ref: ExactRef
    release_ref: ExactRef
    producer_query_ref: ExactRef
    predicate_ref: ExactRef
    predicate_hash: str
    producer_receipt_ref: ExactRef
    producer_fact_ref: ExactRef
    producer_fact_state: str
    evidence_ref: ExactRef
    evidence_content_hash: str
    consumer_query_ref: ExactRef
    consumer_query_material_hash: str
    model_rule_hash: str
    evaluator_result_state: str
    evaluator_result_hash: str
    eligibility_state: str
    execution_state: str
    result_state: str
    uncertainty_state: str | None
    denominator: int
    cells: tuple[Mapping[str, Any], ...]
    consumer_values_read: Mapping[str, Any]
    execution_provenance: str = PROVENANCE_CANONICAL
    execution_mode: str = "LIVE_TRUSTED_EXECUTION"
    trust_domain: str = R61_TRUST_DOMAIN
    trust_domain_version: str = R61_TRUST_DOMAIN_VERSION
    trust_grade: str = R61_TRUST_GRADE

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_key", _sha(self.request_key, "envelope.request_key"))
        object.__setattr__(self, "owner_identity_hash", _sha(self.owner_identity_hash, "envelope.owner_identity_hash"))
        object.__setattr__(self, "predicate_hash", _sha(self.predicate_hash, "envelope.predicate_hash"))
        object.__setattr__(self, "evidence_content_hash", _sha(self.evidence_content_hash, "envelope.evidence_content_hash"))
        object.__setattr__(self, "consumer_query_material_hash", _sha(self.consumer_query_material_hash, "envelope.consumer_query_material_hash"))
        object.__setattr__(self, "model_rule_hash", _sha(self.model_rule_hash, "envelope.model_rule_hash"))
        object.__setattr__(self, "evaluator_result_hash", _sha(self.evaluator_result_hash, "envelope.evaluator_result_hash"))
        if self.trust_domain != R61_TRUST_DOMAIN or self.trust_domain_version != R61_TRUST_DOMAIN_VERSION:
            raise EvidenceBindingError("untrusted execution envelope domain/version")
        if self.trust_grade != R61_TRUST_GRADE:
            raise EvidenceBindingError("untrusted execution envelope grade")
        if self.execution_provenance != PROVENANCE_CANONICAL:
            raise EvidenceBindingError("envelope execution provenance must be canonical")
        if self.execution_mode != "LIVE_TRUSTED_EXECUTION":
            raise EvidenceBindingError("envelope execution mode must be live trusted execution")
        if type(self.denominator) is not int or self.denominator <= 0:
            raise EvidenceBindingError("executed envelope requires a positive denominator")
        for name in ("request_material", "context_material", "owner_identity_material", "consumer_values_read"):
            object.__setattr__(self, name, canonicalize(getattr(self, name)))
        object.__setattr__(self, "cells", tuple(canonicalize(cell) for cell in self.cells))

    def material(self) -> Mapping[str, Any]:
        return {
            "schema": "R61_EXECUTED_EVIDENCE_ENVELOPE@2",
            "execution_provenance": self.execution_provenance,
            "execution_mode": self.execution_mode,
            "trust_domain": self.trust_domain,
            "trust_domain_version": self.trust_domain_version,
            "trust_grade": self.trust_grade,
            "request_material": canonicalize(self.request_material),
            "request_key": self.request_key,
            "context_ref": self.context_ref.as_dict(),
            "context_material": canonicalize(self.context_material),
            "owner_identity_material": canonicalize(self.owner_identity_material),
            "owner_identity_hash": self.owner_identity_hash,
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "release_ref": self.release_ref.as_dict(),
            "producer_query_ref": self.producer_query_ref.as_dict(),
            "predicate_ref": self.predicate_ref.as_dict(),
            "predicate_hash": self.predicate_hash,
            "producer_receipt_ref": self.producer_receipt_ref.as_dict(),
            "producer_fact_ref": self.producer_fact_ref.as_dict(),
            "producer_fact_state": self.producer_fact_state,
            "evidence_ref": self.evidence_ref.as_dict(),
            "evidence_content_hash": self.evidence_content_hash,
            "consumer_query_ref": self.consumer_query_ref.as_dict(),
            "consumer_query_material_hash": self.consumer_query_material_hash,
            "model_rule_hash": self.model_rule_hash,
            "evaluator_result_state": self.evaluator_result_state,
            "evaluator_result_hash": self.evaluator_result_hash,
            "eligibility_state": self.eligibility_state,
            "execution_state": self.execution_state,
            "result_state": self.result_state,
            "uncertainty_state": self.uncertainty_state,
            "denominator": self.denominator,
            "cells": [canonicalize(cell) for cell in self.cells],
            "consumer_values_read": canonicalize(self.consumer_values_read),
        }

    @property
    def envelope_hash(self) -> str:
        return semantic_hash(self.material())

    @property
    def ref(self) -> ExactRef:
        h = self.envelope_hash
        return ExactRef(
            "R61_EXECUTED_EVIDENCE_ENVELOPE@2",
            f"urn:rawlsing:r61:executed-evidence-envelope:sha256:{h}",
            h,
        )


class TrustedAdmissionVerifier:
    """Verification-only capability; no issue, sign or key-export operation."""

    def __init__(self, key: bytes, *, authority_id: str) -> None:
        if len(key) < 32:
            raise EvidenceBindingError("verifier key must be at least 32 bytes")
        self._key = key
        self.authority_id = authority_id

    def _seal(self, material: Mapping[str, Any]) -> str:
        body = json.dumps(
            canonicalize(material), sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("utf-8")
        return hmac.new(self._key, body, hashlib.sha256).hexdigest()

    def verify_producer(
        self,
        admission: TrustedOwnerAdmission,
        *,
        context_ref: ExactRef,
        owner_identity_material: Mapping[str, Any],
    ) -> bool:
        if admission.authority_id != self.authority_id or admission.scope != "PRODUCER":
            return False
        if admission.context_ref != context_ref:
            return False
        if admission.producer_identity_hash != semantic_hash(owner_identity_material):
            return False
        return hmac.compare_digest(
            self._seal(admission.material(include_token=False)), admission.token
        )

    def verify_envelope(self, envelope: ExecutedEvidenceEnvelope, signature: Any) -> bool:
        return isinstance(signature, str) and hmac.compare_digest(
            self._seal(envelope.material()), signature
        )


class TrustedAdmissionAuthority:
    """Trusted setup issuer. Not exported to/defaulted in subject-facing APIs."""

    def __init__(self, key: bytes | None = None, *, authority_id: str | None = None) -> None:
        self._key = key if key is not None else secrets.token_bytes(32)
        if len(self._key) < 32:
            raise EvidenceBindingError("admission authority key must be at least 32 bytes")
        self.authority_id = authority_id or "R61_TRUSTED_HOST_AUTHORITY"

    @property
    def key_hex(self) -> str:
        return self._key.hex()

    def verifier(self) -> TrustedAdmissionVerifier:
        return TrustedAdmissionVerifier(self._key, authority_id=self.authority_id)

    def _seal(self, material: Mapping[str, Any]) -> str:
        body = json.dumps(
            canonicalize(material), sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("utf-8")
        return hmac.new(self._key, body, hashlib.sha256).hexdigest()

    def issue_producer(
        self,
        *,
        context_ref: ExactRef,
        owner_identity_material: Mapping[str, Any],
    ) -> TrustedOwnerAdmission:
        base = {
            "schema": "R61_TRUSTED_OWNER_ADMISSION@2",
            "authority_id": self.authority_id,
            "scope": "PRODUCER",
            "context_ref": context_ref.as_dict(),
            "producer_identity_hash": semantic_hash(owner_identity_material),
            "evidence_ref": None,
            "evidence_content_hash": None,
        }
        return TrustedOwnerAdmission(
            authority_id=self.authority_id,
            scope="PRODUCER",
            context_ref=context_ref,
            producer_identity_hash=base["producer_identity_hash"],
            evidence_ref=None,
            evidence_content_hash=None,
            token=self._seal(base),
        )

    def issue_envelope(self, envelope: ExecutedEvidenceEnvelope) -> str:
        return self._seal(envelope.material())


class TrustedCacheIssuer:
    """Test-only ephemeral issuer boundary for cold cache records.

    The key is generated in memory or supplied explicitly by a supervisor.  It is
    deliberately not written into cache material by this module.  Production
    secrets are never read.
    """

    def __init__(self, key: bytes | None = None) -> None:
        self._key = key if key is not None else secrets.token_bytes(32)
        if len(self._key) < 32:
            raise EvidenceCacheIntegrityError("issuer key must be at least 32 bytes")

    @property
    def key_hex(self) -> str:
        return self._key.hex()

    def seal(self, payload: Mapping[str, Any]) -> str:
        body = json.dumps(
            canonicalize(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("utf-8")
        return hmac.new(self._key, body, hashlib.sha256).hexdigest()

    def verify(self, payload: Mapping[str, Any], seal: Any) -> bool:
        return isinstance(seal, str) and hmac.compare_digest(self.seal(payload), seal)


def _same_material(left: Any, right: Any) -> bool:
    """Canonical identity comparison preserves bool/int/null and ordered arrays."""
    return semantic_hash(left) == semantic_hash(right)


def _checked_cache_owner_descriptor(
    request: EvidenceRequest,
    result: EvidenceResult,
    verifier: TrustedAdmissionVerifier | None,
    *,
    descriptor: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    """One authenticated read-only owner projection for every productive API.

    Descriptor hashes are public integrity aids. Only the configured verifier's
    original executed-envelope signature authenticates this projection.
    """
    envelope = result.execution_envelope
    if verifier is None or envelope is None or not verifier.verify_envelope(envelope, result.envelope_signature):
        raise EvidenceCacheIntegrityError("signed execution envelope absent/untrusted")
    if not _envelope_matches_request(envelope, request):
        raise EvidenceCacheIntegrityError("execution envelope does not match K")
    owner = envelope.owner_identity_material
    if not isinstance(owner, Mapping) or set(owner) != CACHE_OWNER_FIELDS:
        raise EvidenceCacheIntegrityError("unknown/missing canonical owner fields")
    if envelope.owner_identity_hash != semantic_hash(owner):
        raise EvidenceCacheIntegrityError("signed owner hash/material disagreement")
    context = owner["context"]
    if not isinstance(context, Mapping) or not _same_material(context, envelope.context_material):
        raise EvidenceCacheIntegrityError("signed owner/envelope context disagreement")
    context_hash = semantic_hash(context)
    context_ref = ExactRef(
        "R61_ADMITTED_EVIDENCE_CONTEXT@1",
        f"urn:rawlsing:r61:admitted-evidence-context:sha256:{context_hash}", context_hash,
    )
    if envelope.context_ref != context_ref or not _same_material(owner["context_ref"], context_ref.as_dict()):
        raise EvidenceCacheIntegrityError("canonical owner context ref/content disagreement")
    if not _context_material_matches_request(context, request):
        raise EvidenceCacheIntegrityError("canonical owner context does not match K")
    expected = {
        "producer_query_ref": request.producer_query_ref.as_dict(),
        "predicate_ref": request.predicate_ref.as_dict(),
        "predicate_hash": request.predicate_hash,
        "release_refs": [request.release_ref.as_dict()],
        "consumer_query_ref": request.consumer_query_ref.as_dict(),
        "consumer_binding_fingerprint": request.consumer_binding_fingerprint,
        "model_rule_hash": request.model_rule_hash,
        "source_universe_ref": request.source_universe_ref.as_dict(),
        "risk_set_ref": request.risk_set_ref.as_dict(),
        "target_ref": request.target_ref.as_dict(),
    }
    for name, value in expected.items():
        if not _same_material(owner[name], value):
            raise EvidenceCacheIntegrityError(f"canonical owner {name} does not match K")
    actual_conditions = owner["actual_conditions"]
    if not isinstance(actual_conditions, (list, tuple)) or len(actual_conditions) != len(request.ordered_conditions):
        raise EvidenceCacheIntegrityError("canonical owner condition arity mismatch")
    for actual, condition in zip(actual_conditions, request.ordered_conditions):
        if not isinstance(actual, Mapping) or set(actual) != {
            "conditioner_binding_id", "occurrence", "leaf_semantic_ref", "typed_value", "domain_state_version"
        }:
            raise EvidenceCacheIntegrityError("canonical actual condition fields invalid")
        leaf_ref = actual["leaf_semantic_ref"]
        if not isinstance(leaf_ref, Mapping) or not _item_matches_leaf(condition.occurrence.item, leaf_ref):
            raise EvidenceCacheIntegrityError("canonical condition leaf/item mismatch")
        exact_ref(leaf_ref, "canonical condition leaf ref")
        native_value = _typed_from_material(condition.value.material())
        expected_condition = {
            "conditioner_binding_id": condition.conditioner_binding_id,
            "occurrence": {
                "item": native_value, "option": str(native_value),
                "form": condition.occurrence.form, "repeat": condition.occurrence.repeat,
            },
            "leaf_semantic_ref": leaf_ref,
            "typed_value": condition.value.material(),
            "domain_state_version": condition.domain_state_version,
        }
        if not _same_material(actual, expected_condition) or context["domain_state_version"] != condition.domain_state_version:
            raise EvidenceCacheIntegrityError("canonical actual/typed condition mismatch")
    evidence, query, rule = result.evidence_object, result.consumer_query_object, result.model_rule_object
    if not _objects_match_envelope(evidence, query, rule, envelope):
        raise EvidenceCacheIntegrityError("signed evidence/query/rule association mismatch")
    if (
        query.ref != request.consumer_query_ref
        or query.source_universe_ref != request.source_universe_ref
        or query.release_ref != request.release_ref
        or query.target_ref != request.target_ref
        or evidence.source_universe_ref != request.source_universe_ref
        or evidence.release_ref != request.release_ref
        or evidence.target_ref != request.target_ref
        or evidence.raw_support != envelope.denominator
        or [b.binding_id for b in query.conditioner_bindings] != [c.conditioner_binding_id for c in request.ordered_conditions]
    ):
        raise EvidenceCacheIntegrityError("native consumer/source/typed conditions do not match K")
    fingerprints = {semantic_hash([b.material() for b in query.conditioner_bindings])}
    if len(query.conditioner_bindings) == 1:
        fingerprints.add(semantic_hash(query.conditioner_bindings[0].material()))
    if request.consumer_binding_fingerprint not in fingerprints:
        raise EvidenceCacheIntegrityError("native consumer binding fingerprint mismatch")
    actual = evaluate_positioned_subject_possibility(query=query, rule=rule, evidence=(evidence,))
    cells = _evidence_cells(evidence)
    if (
        actual.result_state != "EXACT_SUPPORTED"
        or actual.result_state != envelope.evaluator_result_state
        or actual.result_hash != envelope.evaluator_result_hash
        or envelope.result_state != "SUPPORTED"
        or envelope.eligibility_state != "ELIGIBLE"
        or envelope.execution_state != "COMPLETED"
        or not _same_material(cells, envelope.cells)
        or not _same_material(envelope.consumer_values_read, _consumer_values(request, evidence, actual, envelope.denominator, cells))
        or not _result_matches_envelope(result, envelope)
    ):
        raise EvidenceCacheIntegrityError("signed evaluator/result/value/status disagreement")
    projection = {
        "schema": CACHE_OWNER_DESCRIPTOR_SCHEMA,
        "request_key": request.key,
        "owner_identity_material": canonicalize(owner),
        "owner_identity_hash": envelope.owner_identity_hash,
        "validated_conditions": [condition.material() for condition in request.ordered_conditions],
    }
    projection["descriptor_hash"] = semantic_hash(projection)
    if descriptor is not None and (
        not isinstance(descriptor, Mapping)
        or set(descriptor) != CACHE_OWNER_DESCRIPTOR_FIELDS
        or not _same_material(descriptor, projection)
    ):
        raise EvidenceCacheIntegrityError("cache owner descriptor is not the authenticated normal form")
    return canonicalize(projection)


class EvidenceResolver:
    """Exact full-K registry and association/issuer-bound cache resolver."""

    def __init__(
        self,
        *,
        cache_issuer: TrustedCacheIssuer | None = None,
        trusted_binding_hashes: Iterable[str] = (),
        trusted_descriptor_hashes: Iterable[str] = (),
        admission_verifier: TrustedAdmissionVerifier | None = None,
        executor: TrustedAdmissionAuthority | None = None,
        admitted_producer: Callable[..., Any] | None = None,
    ) -> None:
        self._bindings: dict[str, EmpiricalProducerBinding] = {}
        self._cache: dict[str, EvidenceResult] = {}
        self._requests: dict[str, EvidenceRequest] = {}
        self._cache_descriptors: dict[str, Mapping[str, Any]] = {}
        self._admitted: dict[str, bool] = {}
        self._issuer = cache_issuer
        self._trusted_binding_hashes = frozenset(trusted_binding_hashes)
        self._trusted_descriptor_hashes = frozenset(trusted_descriptor_hashes)
        self._admission_verifier = admission_verifier
        self._executor = executor
        self._admitted_producer = admitted_producer

    def bind(self, binding: EmpiricalProducerBinding) -> str:
        if not isinstance(binding, EmpiricalProducerBinding):
            raise EvidenceBindingMismatch("binding must be EmpiricalProducerBinding")
        key = binding.request.key
        existing = self._bindings.get(key)
        if existing is not None and existing.binding_hash != binding.binding_hash:
            raise EvidenceBindingMismatch(
                "same request key registered with different producer determinants"
            )
        if key in self._cache:
            raise EvidenceBindingMismatch(
                "cannot bind a producer over an existing authenticated cache entry"
            )
        self._bindings[key] = binding
        self._requests[key] = binding.request
        self._admitted[key] = bool(
            self._admission_verifier is not None
            and binding.admission is not None
            and self._admission_verifier.verify_producer(
                binding.admission,
                context_ref=binding.context.context_ref,
                owner_identity_material=binding.owner_identity_material(),
            )
            and self._admitted_producer is not None
            and binding.producer is self._admitted_producer
        )
        return key

    def resolve(self, request: EvidenceRequest) -> EvidenceResult:
        if not isinstance(request, EvidenceRequest):
            raise EvidenceRequestShapeError("resolve requires EvidenceRequest")
        cached = self._cache.get(request.key)
        if cached is not None:
            return self._replay_cache(request, cached)
        binding = self._bindings.get(request.key)
        if binding is None:
            return _result_refusal(
                request,
                REFUSAL_NO_EXACT_BINDING,
                eligibility="UNKNOWN",
                execution="NOT_STARTED",
            )
        if self._admission_verifier is None:
            return _result_refusal(
                request,
                "NO_CONFIGURED_TRUST_ROOT",
                eligibility="UNKNOWN",
                execution="NOT_STARTED",
            )
        if not self._admitted.get(request.key, False):
            return _result_refusal(
                request,
                "OWNER_ADMISSION_UNRESOLVED",
                eligibility="UNKNOWN",
                execution="NOT_STARTED",
            )
        reason = binding.mismatch_reason(request)
        if reason is not None:
            return _result_refusal(
                request,
                REFUSAL_IDENTITY_MISMATCH,
                eligibility="UNKNOWN",
                execution="NOT_STARTED",
            )
        result = self._produce(binding)
        if result.result_state == "SUPPORTED":
            self._cache[request.key] = result
            self._requests[request.key] = request
            self._cache_descriptors[request.key] = _checked_cache_owner_descriptor(
                request, result, self._admission_verifier
            )
        return result

    def _produce(self, binding: EmpiricalProducerBinding) -> EvidenceResult:
        request = binding.request
        provider = binding.producer(
            repository=binding.repository,
            empirical_query=binding.empirical_query,
            predicate=binding.predicate,
            authority_registry=binding.authority_registry,
            release_refs=binding.release_refs,
            consumer_query=binding.consumer_query,
            model_rule=binding.model_rule,
            condition_binding_witness=binding.condition_binding_witness,
        )
        composition = provider.composition_result

        identity_ok = (
            composition.consumer_query_ref == request.consumer_query_ref
            and composition.producer_query_ref == request.producer_query_ref
            and composition.producer_predicate_ref == request.predicate_ref
            and tuple(composition.release_refs) == tuple(binding.release_refs)
            and request.source_universe_ref in tuple(composition.source_universe_refs)
            and request.target_ref in tuple(composition.ordered_target_refs)
        )
        if not identity_ok:
            return _result_refusal(
                request,
                REFUSAL_IDENTITY_MISMATCH,
                denominator=composition.raw_denominator_support,
                producer_receipt_ref=provider.receipt_ref,
                producer_fact_ref=composition.producer_fact_ref,
                producer_fact_state=composition.producer_fact_state,
                uncertainty_state=composition.uncertainty_state,
            )

        if provider.provider_state == PROVIDER_STATE_EXACT:
            evidence = provider.generated_evidence_or_null
            producer_consumer = provider.consumer_result_or_null
            if evidence is None or producer_consumer is None:
                return _result_refusal(request, REFUSAL_MISSING_STRUCTURAL_STATE)
            if (
                evidence.target_ref != request.target_ref
                or evidence.source_universe_ref != request.source_universe_ref
                or evidence.release_ref != request.release_ref
                or evidence.raw_support != composition.raw_denominator_support
            ):
                return _result_refusal(request, REFUSAL_IDENTITY_MISMATCH)
            actual_consumer = evaluate_positioned_subject_possibility(
                query=binding.consumer_query,
                rule=binding.model_rule,
                evidence=(evidence,),
            )
            if (
                actual_consumer.result_hash != producer_consumer.result_hash
                or actual_consumer.material() != producer_consumer.material()
            ):
                return _result_refusal(request, REFUSAL_CONSUMER_ASSOCIATION)
            if actual_consumer.result_state != "EXACT_SUPPORTED":
                eligibility, execution, result_state = _provider_result_state(
                    actual_consumer.result_state
                )
                return _result_refusal(
                    request,
                    REFUSAL_UNKNOWN_SUPPORT,
                    eligibility=eligibility,
                    execution=execution,
                    result_state=result_state,
                    denominator=composition.raw_denominator_support,
                    producer_receipt_ref=provider.receipt_ref,
                    producer_fact_ref=composition.producer_fact_ref,
                    producer_fact_state=composition.producer_fact_state,
                    uncertainty_state=composition.uncertainty_state,
                )
            if self._executor is None:
                return _result_refusal(
                    request,
                    "NO_CONFIGURED_EXECUTION_AUTHORITY",
                    eligibility="UNKNOWN",
                    execution="NOT_STARTED",
                )
            cells = _cells(composition)
            values = _consumer_values(
                request,
                evidence,
                actual_consumer,
                composition.raw_denominator_support,
                cells,
            )
            envelope = ExecutedEvidenceEnvelope(
                request_material=request.material(),
                request_key=request.key,
                context_ref=binding.context.context_ref,
                context_material=binding.context.material(),
                owner_identity_material=binding.owner_identity_material(),
                owner_identity_hash=binding.owner_identity_hash,
                source_universe_ref=request.source_universe_ref,
                release_ref=request.release_ref,
                producer_query_ref=request.producer_query_ref,
                predicate_ref=request.predicate_ref,
                predicate_hash=request.predicate_hash,
                producer_receipt_ref=provider.receipt_ref,
                producer_fact_ref=composition.producer_fact_ref,
                producer_fact_state=composition.producer_fact_state,
                evidence_ref=evidence.evidence_ref,
                evidence_content_hash=semantic_hash(_evidence_material(evidence)),
                consumer_query_ref=request.consumer_query_ref,
                consumer_query_material_hash=semantic_hash(binding.consumer_query.material()),
                model_rule_hash=request.model_rule_hash,
                evaluator_result_state=actual_consumer.result_state,
                evaluator_result_hash=actual_consumer.result_hash,
                eligibility_state="ELIGIBLE",
                execution_state="COMPLETED",
                result_state="SUPPORTED",
                uncertainty_state=composition.uncertainty_state,
                denominator=composition.raw_denominator_support,
                cells=cells,
                consumer_values_read=values,
            )
            signature = self._executor.issue_envelope(envelope)
            return EvidenceResult(
                request_key=request.key,
                eligibility_state="ELIGIBLE",
                execution_state="COMPLETED",
                result_state="SUPPORTED",
                provenance=PROVENANCE_CANONICAL,
                denominator=composition.raw_denominator_support,
                cells=cells,
                evidence_ref=evidence.evidence_ref,
                producer_receipt_ref=provider.receipt_ref,
                producer_fact_ref=composition.producer_fact_ref,
                producer_fact_state=composition.producer_fact_state,
                consumer_query_ref=request.consumer_query_ref,
                consumer_result_state=actual_consumer.result_state,
                consumer_result_hash=actual_consumer.result_hash,
                consumer_values_read=values,
                uncertainty_state=composition.uncertainty_state,
                execution_envelope=envelope,
                envelope_signature=signature,
                evidence_object=evidence,
                consumer_query_object=binding.consumer_query,
                model_rule_object=binding.model_rule,
                consumer_result_object=actual_consumer,
            )

        if provider.provider_state != PROVIDER_STATE_REFUSED:
            return _result_refusal(
                request,
                REFUSAL_UNKNOWN_SUPPORT,
                execution="ERROR",
                result_state="UNKNOWN",
                producer_receipt_ref=provider.receipt_ref,
            )
        state = composition.analytical_state
        eligibility, execution, result_state = _provider_result_state(state)
        refusal = (
            REFUSAL_UNKNOWN_SUPPORT
            if result_state == "UNKNOWN"
            else REFUSAL_UNSUPPORTED
            if result_state == "UNSUPPORTED"
            else REFUSAL_FORBIDDEN
            if eligibility in {"PROHIBITED", "INAPPLICABLE_PROVED"}
            else "VALID_TYPED_NO_SUPPORT"
            if result_state == "ZERO_SUPPORT"
            else "VALID_TYPED_EMPTY"
            if result_state == "VALID_EMPTY"
            else REFUSAL_UNKNOWN_SUPPORT
        )
        return _result_refusal(
            request,
            refusal,
            eligibility=eligibility,
            execution=execution,
            result_state=result_state,
            denominator=composition.raw_denominator_support,
            producer_receipt_ref=provider.receipt_ref,
            producer_fact_ref=composition.producer_fact_ref,
            producer_fact_state=composition.producer_fact_state,
            uncertainty_state=composition.uncertainty_state,
        )

    def _check_cache_configuration(self) -> None:
        if self._admission_verifier is None:
            raise EvidenceCacheIntegrityError("NO_CONFIGURED_TRUST_ROOT")
        if self._trusted_binding_hashes:
            raise EvidenceCacheIntegrityError("LEGACY_BINDING_PINS_REQUIRE_MIGRATION")

    def _check_descriptor_pin(self, descriptor: Mapping[str, Any]) -> None:
        if self._trusted_descriptor_hashes and descriptor["descriptor_hash"] not in self._trusted_descriptor_hashes:
            raise EvidenceCacheIntegrityError("CACHE_OWNER_DESCRIPTOR_NOT_PINNED")

    def _replay_cache(
        self, request: EvidenceRequest, cached: EvidenceResult
    ) -> EvidenceResult:
        try:
            self._check_cache_configuration()
            retained = self._cache_descriptors.get(request.key)
            if retained is None:
                raise EvidenceCacheIntegrityError("cache owner descriptor missing")
            descriptor = _checked_cache_owner_descriptor(
                request, cached, self._admission_verifier, descriptor=retained,
            )
            self._check_descriptor_pin(descriptor)
        except EvidenceCacheIntegrityError as exc:
            code = str(exc)
            if code in {
                "LEGACY_BINDING_PINS_REQUIRE_MIGRATION",
                "CACHE_OWNER_DESCRIPTOR_NOT_PINNED",
                "NO_CONFIGURED_TRUST_ROOT",
            }:
                return _result_refusal(request, code)
            return _result_refusal(request, REFUSAL_STALE_CACHE)
        except (Pre553IntegrityError, KeyError, TypeError, ValueError):
            return _result_refusal(request, REFUSAL_STALE_CACHE)
        return replace(cached, provenance=PROVENANCE_CACHE)

    def export_cache(self) -> Mapping[str, Any]:
        self._check_cache_configuration()
        entries = []
        for key in sorted(self._cache):
            result = self._cache[key]
            request = self._requests.get(key)
            descriptor = self._cache_descriptors.get(key)
            if request is None or descriptor is None:
                raise EvidenceCacheIntegrityError("cache entry lacks canonical owner descriptor")
            descriptor = _checked_cache_owner_descriptor(
                request, result, self._admission_verifier, descriptor=descriptor,
            )
            self._check_descriptor_pin(descriptor)
            payload = {
                "schema": CACHE_SCHEMA,
                "seal_algorithm": CACHE_SEAL_ALGORITHM,
                "request_key": key,
                "request_material": canonicalize(request.material()),
                "cache_owner_descriptor": descriptor,
                "execution_envelope": canonicalize(result.execution_envelope.material()),
                "envelope_signature": result.envelope_signature,
                "result": canonicalize(_envelope_result_projection(result.execution_envelope)),
                "evidence": _evidence_material(result.evidence_object),
                "consumer_query": canonicalize(result.consumer_query_object.material()),
                "model_rule": canonicalize(result.model_rule_object.material()),
            }
            entry = {**payload, "seal": semantic_hash(payload)}
            if self._issuer is not None:
                entry["issuer_grade"] = CACHE_TRUST_ISSUER
                entry["issuer_seal"] = self._issuer.seal(
                    {k: v for k, v in entry.items() if k != "issuer_seal"}
                )
            entries.append(entry)
        return {"schema": CACHE_SCHEMA, "entries": entries}

    def import_authenticated_cache(self, material: Mapping[str, Any]) -> None:
        self._check_cache_configuration()
        # Detach before parsing: retained objects must not alias caller-owned bytes.
        try:
            self._import_authenticated_cache(canonicalize(material))
        except EvidenceCacheIntegrityError:
            raise
        except (Pre553IntegrityError, KeyError, TypeError, ValueError, AttributeError) as exc:
            raise EvidenceCacheIntegrityError("malformed authenticated cache") from exc

    def _import_authenticated_cache(self, material: Mapping[str, Any]) -> None:
        if not isinstance(material, Mapping) or material.get("schema") != CACHE_SCHEMA:
            raise EvidenceCacheIntegrityError("LEGACY_OR_UNKNOWN_CACHE_SCHEMA")
        if set(material) != {"schema", "entries"}:
            raise EvidenceCacheIntegrityError("unknown cache fields")
        entries = material["entries"]
        if not isinstance(entries, list):
            raise EvidenceCacheIntegrityError("cache entries must be a list")
        imported: dict[str, EvidenceResult] = {}
        imported_requests: dict[str, EvidenceRequest] = {}
        imported_descriptors: dict[str, Mapping[str, Any]] = {}
        required = {
            "schema", "seal_algorithm", "request_key", "request_material",
            "cache_owner_descriptor", "execution_envelope", "envelope_signature",
            "result", "evidence", "consumer_query", "model_rule", "seal",
        }
        for raw in entries:
            if not isinstance(raw, Mapping) or not required <= set(raw) or set(raw) - required - {"issuer_grade", "issuer_seal"}:
                raise EvidenceCacheIntegrityError("unknown/missing cache entry fields")
            if raw["schema"] != CACHE_SCHEMA or raw["seal_algorithm"] != CACHE_SEAL_ALGORITHM:
                raise EvidenceCacheIntegrityError("cache entry schema/algorithm mismatch")
            payload = {key: value for key, value in raw.items() if key not in {"seal", "issuer_seal", "issuer_grade"}}
            if raw["seal"] != semantic_hash(payload):
                raise EvidenceCacheIntegrityError("cache entry seal mismatch")
            if self._issuer is not None and not self._issuer.verify(
                {k: v for k, v in raw.items() if k != "issuer_seal"}, raw.get("issuer_seal"),
            ):
                raise EvidenceCacheIntegrityError("cache issuer seal missing/invalid")
            request = EvidenceRequest.from_material(raw["request_material"])
            if request.key != raw["request_key"] or not _same_material(request.material(), raw["request_material"]):
                raise EvidenceCacheIntegrityError("cache request preimage does not match K")
            envelope = _envelope_from_material(raw["execution_envelope"])
            evidence = _evidence_from_material(raw["evidence"])
            query = _query_from_material(raw["consumer_query"])
            rule = _rule_from_material(raw["model_rule"])
            actual = evaluate_positioned_subject_possibility(query=query, rule=rule, evidence=(evidence,))
            result = EvidenceResult(
                request_key=request.key,
                eligibility_state=envelope.eligibility_state,
                execution_state=envelope.execution_state,
                result_state=envelope.result_state,
                provenance=PROVENANCE_CACHE,
                denominator=envelope.denominator,
                cells=_evidence_cells(evidence),
                evidence_ref=evidence.evidence_ref,
                producer_receipt_ref=envelope.producer_receipt_ref,
                producer_fact_ref=envelope.producer_fact_ref,
                producer_fact_state=envelope.producer_fact_state,
                consumer_query_ref=query.ref,
                consumer_result_state=actual.result_state,
                consumer_result_hash=actual.result_hash,
                consumer_values_read=canonicalize(envelope.consumer_values_read),
                uncertainty_state=envelope.uncertainty_state,
                execution_envelope=envelope,
                envelope_signature=raw["envelope_signature"],
                evidence_object=evidence,
                consumer_query_object=query,
                model_rule_object=rule,
                consumer_result_object=actual,
            )
            if not isinstance(raw["cache_owner_descriptor"], Mapping):
                raise EvidenceCacheIntegrityError("canonical cache owner descriptor required")
            descriptor = _checked_cache_owner_descriptor(
                request, result, self._admission_verifier,
                descriptor=raw["cache_owner_descriptor"],
            )
            self._check_descriptor_pin(descriptor)
            if not _same_material(raw["result"], _envelope_result_projection(envelope)):
                raise EvidenceCacheIntegrityError("cache result differs from signed projection")
            if request.key in imported:
                raise EvidenceCacheIntegrityError("duplicate cache request key")
            imported[request.key] = result
            imported_requests[request.key] = request
            imported_descriptors[request.key] = descriptor
        if set(imported) & set(self._bindings):
            raise EvidenceCacheIntegrityError("cache/import conflicts with a registered binding")
        self._cache.update(imported)
        self._requests.update(imported_requests)
        self._cache_descriptors.update(imported_descriptors)


def _envelope_from_material(material: Mapping[str, Any]) -> ExecutedEvidenceEnvelope:
    try:
        envelope = ExecutedEvidenceEnvelope(
            request_material=material["request_material"],
            request_key=material["request_key"],
            context_ref=ExactRef(**material["context_ref"]),
            context_material=material["context_material"],
            owner_identity_material=material["owner_identity_material"],
            owner_identity_hash=material["owner_identity_hash"],
            source_universe_ref=ExactRef(**material["source_universe_ref"]),
            release_ref=ExactRef(**material["release_ref"]),
            producer_query_ref=ExactRef(**material["producer_query_ref"]),
            predicate_ref=ExactRef(**material["predicate_ref"]),
            predicate_hash=material["predicate_hash"],
            producer_receipt_ref=ExactRef(**material["producer_receipt_ref"]),
            producer_fact_ref=ExactRef(**material["producer_fact_ref"]),
            producer_fact_state=material["producer_fact_state"],
            evidence_ref=ExactRef(**material["evidence_ref"]),
            evidence_content_hash=material["evidence_content_hash"],
            consumer_query_ref=ExactRef(**material["consumer_query_ref"]),
            consumer_query_material_hash=material["consumer_query_material_hash"],
            model_rule_hash=material["model_rule_hash"],
            evaluator_result_state=material["evaluator_result_state"],
            evaluator_result_hash=material["evaluator_result_hash"],
            eligibility_state=material["eligibility_state"],
            execution_state=material["execution_state"],
            result_state=material["result_state"],
            uncertainty_state=material["uncertainty_state"],
            denominator=material["denominator"],
            cells=tuple(material["cells"]),
            consumer_values_read=material["consumer_values_read"],
            execution_provenance=material["execution_provenance"],
            execution_mode=material["execution_mode"],
            trust_domain=material["trust_domain"],
            trust_domain_version=material["trust_domain_version"],
            trust_grade=material["trust_grade"],
        )
        if not _same_material(envelope.material(), material):
            raise EvidenceCacheIntegrityError("noncanonical executed envelope schema/fields")
        return envelope
    except (KeyError, TypeError) as exc:
        raise EvidenceCacheIntegrityError("malformed executed evidence envelope") from exc


def _envelope_matches_request(
    envelope: ExecutedEvidenceEnvelope, request: EvidenceRequest
) -> bool:
    return (
        envelope.request_key == request.key
        and canonicalize(envelope.request_material) == canonicalize(request.material())
        and envelope.source_universe_ref == request.source_universe_ref
        and envelope.release_ref == request.release_ref
        and envelope.producer_query_ref == request.producer_query_ref
        and envelope.predicate_ref == request.predicate_ref
        and envelope.predicate_hash == request.predicate_hash
        and envelope.consumer_query_ref == request.consumer_query_ref
        and envelope.model_rule_hash == request.model_rule_hash
        and _context_material_matches_request(envelope.context_material, request)
    )


def _envelope_result_projection(envelope: ExecutedEvidenceEnvelope) -> Mapping[str, Any]:
    """The only result material authorized by the signed execution envelope."""
    return {
        "request_key": envelope.request_key,
        "eligibility_state": envelope.eligibility_state,
        "execution_state": envelope.execution_state,
        "result_state": envelope.result_state,
        "denominator": envelope.denominator,
        "cells": [canonicalize(cell) for cell in envelope.cells],
        "evidence_ref": envelope.evidence_ref.as_dict(),
        "producer_receipt_ref": envelope.producer_receipt_ref.as_dict(),
        "producer_fact_ref": envelope.producer_fact_ref.as_dict(),
        "producer_fact_state": envelope.producer_fact_state,
        "consumer_query_ref": envelope.consumer_query_ref.as_dict(),
        "consumer_result_state": envelope.evaluator_result_state,
        "consumer_result_hash": envelope.evaluator_result_hash,
        "consumer_values_read": canonicalize(envelope.consumer_values_read),
        "uncertainty_state": envelope.uncertainty_state,
        "original_execution_provenance": envelope.execution_provenance,
        "original_execution_mode": envelope.execution_mode,
    }


def _result_matches_envelope(
    result: EvidenceResult, envelope: ExecutedEvidenceEnvelope
) -> bool:
    if result.request_key != envelope.request_key:
        return False
    if result.eligibility_state != envelope.eligibility_state:
        return False
    if result.execution_state != envelope.execution_state:
        return False
    if result.result_state != envelope.result_state:
        return False
    if result.denominator != envelope.denominator:
        return False
    if not _same_material(result.cells, envelope.cells):
        return False
    if result.evidence_ref != envelope.evidence_ref:
        return False
    if result.producer_receipt_ref != envelope.producer_receipt_ref:
        return False
    if result.producer_fact_ref != envelope.producer_fact_ref:
        return False
    if result.producer_fact_state != envelope.producer_fact_state:
        return False
    if result.consumer_query_ref != envelope.consumer_query_ref:
        return False
    if result.consumer_result_state != envelope.evaluator_result_state:
        return False
    if result.consumer_result_hash != envelope.evaluator_result_hash:
        return False
    if result.uncertainty_state != envelope.uncertainty_state:
        return False
    if result.consumer_values_read is None:
        return False
    return _same_material(result.consumer_values_read, envelope.consumer_values_read)


def _assert_result_matches_envelope(
    result: EvidenceResult, envelope: ExecutedEvidenceEnvelope
) -> None:
    if not _result_matches_envelope(result, envelope):
        raise EvidenceAssociationError(
            "result fields/values do not equal the complete signed execution envelope"
        )


def _objects_match_envelope(
    evidence: PossibilitySliceEvidence | None,
    query: PositionedSubjectPossibilityQuery | None,
    rule: PositionedSubjectPossibilityModelRule | None,
    envelope: ExecutedEvidenceEnvelope,
) -> bool:
    if evidence is None or query is None or rule is None:
        return False
    return (
        evidence.evidence_ref == envelope.evidence_ref
        and semantic_hash(_evidence_material(evidence)) == envelope.evidence_content_hash
        and query.ref == envelope.consumer_query_ref
        and semantic_hash(query.material()) == envelope.consumer_query_material_hash
        and rule.rule_hash == envelope.model_rule_hash
    )


def _optional_ref(value: Any) -> ExactRef | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise EvidenceCacheIntegrityError("exact ref material must be a mapping")
    return ExactRef(
        value["kind"], value["object_id"], value["content_hash"]
    )


def _authority_from_material(value: Mapping[str, Any]) -> AuthorityRef:
    return AuthorityRef(
        value["authority_id"],
        value["authority_version"],
        value["authority_content_hash"],
    )


def _evidence_material(evidence: PossibilitySliceEvidence) -> Mapping[str, Any]:
    return {
        "evidence_ref": evidence.evidence_ref.as_dict(),
        "source_universe_ref": evidence.source_universe_ref.as_dict(),
        "release_ref": evidence.release_ref.as_dict(),
        "target_ref": evidence.target_ref.as_dict(),
        "retained_conditioner_ids": list(evidence.retained_conditioner_ids),
        "evidence_state": evidence.evidence_state,
        "geometry": canonicalize(evidence.geometry),
        "raw_support": evidence.raw_support,
        "uncertainty_state": evidence.uncertainty_state,
        "provenance_refs": [x.as_dict() for x in evidence.provenance_refs],
        "authority_refs": [x.as_dict() for x in evidence.authority_refs],
    }


def _evidence_from_material(value: Mapping[str, Any]) -> PossibilitySliceEvidence:
    return PossibilitySliceEvidence(
        evidence_ref=ExactRef(**value["evidence_ref"]),
        source_universe_ref=ExactRef(**value["source_universe_ref"]),
        release_ref=ExactRef(**value["release_ref"]),
        target_ref=ExactRef(**value["target_ref"]),
        retained_conditioner_ids=tuple(value["retained_conditioner_ids"]),
        evidence_state=value["evidence_state"],
        geometry=value["geometry"],
        raw_support=value["raw_support"],
        uncertainty_state=value["uncertainty_state"],
        provenance_refs=tuple(ExactRef(**x) for x in value["provenance_refs"]),
        authority_refs=tuple(
            _authority_from_material(x) for x in value["authority_refs"]
        ),
    )


def _query_from_material(value: Mapping[str, Any]) -> PositionedSubjectPossibilityQuery:
    bindings = []
    for binding in value["conditioner_bindings"]:
        bindings.append(
            ConditionerBinding(
                binding_id=binding["binding_id"],
                subject_fact_ref=ExactRef(**binding["subject_fact_ref"]),
                empirical_coordinate_ref=ExactRef(
                    **binding["empirical_coordinate_ref"]
                ),
                comparability_authority_ref=_authority_from_material(
                    binding["comparability_authority_ref"]
                ),
                source_universe_ref=ExactRef(**binding["source_universe_ref"]),
                release_ref=ExactRef(**binding["release_ref"]),
                effective_time_or_interval=binding["effective_time_or_interval"],
            )
        )
    return PositionedSubjectPossibilityQuery(
        query_id=value["query_id"],
        subject_ref=ExactRef(**value["subject_ref"]),
        target_ref=ExactRef(**value["target_ref"]),
        source_universe_ref=ExactRef(**value["source_universe_ref"]),
        release_ref=ExactRef(**value["release_ref"]),
        conditioner_bindings=tuple(bindings),
        requested_projection=value["requested_projection"],
        purpose=value["purpose"],
    )


def _rule_from_material(
    value: Mapping[str, Any],
) -> PositionedSubjectPossibilityModelRule:
    steps = tuple(
        SpecificityWalkbackStep(
            step_id=step["step_id"],
            retained_conditioner_ids=tuple(step["retained_conditioner_ids"]),
            proxy_authority_ref=_authority_from_material(
                step["proxy_authority_ref"]
            ),
            source_universe_ref=ExactRef(**step["source_universe_ref"]),
            release_ref=ExactRef(**step["release_ref"]),
            rationale=step["rationale"],
        )
        for step in value["walkback_steps"]
    )
    return PositionedSubjectPossibilityModelRule(
        model_authority_ref=_authority_from_material(value["model_authority_ref"]),
        walkback_authority_ref=_authority_from_material(
            value["walkback_authority_ref"]
        ),
        source_universe_refs=tuple(
            ExactRef(**x) for x in value["source_universe_refs"]
        ),
        walkback_steps=steps,
        positive_proxy_authority_refs=tuple(
            _authority_from_material(x)
            for x in value["positive_proxy_authority_refs"]
        ),
        model_rule_id=value["model_rule_id"],
        algorithm_id=value["algorithm_id"],
    )


class EvidenceConsumerReader:
    """Actual unchanged evaluator consumer bound to one request/result pair."""

    def __init__(
        self,
        request: EvidenceRequest,
        result: EvidenceResult,
        *,
        verifier: TrustedAdmissionVerifier | None = None,
    ) -> None:
        if not isinstance(request, EvidenceRequest):
            raise EvidenceAssociationError("request must be EvidenceRequest")
        if not isinstance(result, EvidenceResult):
            raise EvidenceAssociationError("result must be EvidenceResult")
        self.request = request
        self.result = result
        self.verifier = verifier

    def _assert_association(self) -> None:
        if self.request.key != self.result.request_key:
            raise EvidenceAssociationError(
                "request/result K mismatch: refusing target/depth reuse"
            )
        if self.result.result_state != "SUPPORTED":
            raise EvidenceAssociationError(
                f"result is not exact support: {self.result.result_state}"
            )
        if self.verifier is None:
            raise EvidenceAssociationError("NO_CONFIGURED_TRUST_ROOT: reader is not pinned")
        try:
            _checked_cache_owner_descriptor(self.request, self.result, self.verifier)
        except (Pre553IntegrityError, KeyError, TypeError, ValueError, AttributeError) as exc:
            raise EvidenceAssociationError("signed execution/owner/object association invalid") from exc

    def read(self) -> Mapping[str, Any]:
        self._assert_association()
        actual = evaluate_positioned_subject_possibility(
            query=self.result.consumer_query_object,
            rule=self.result.model_rule_object,
            evidence=(self.result.evidence_object,),
        )
        if actual.result_hash != self.result.consumer_result_hash or actual.result_hash != (
            self.result.execution_envelope.evaluator_result_hash
        ):
            raise EvidenceAssociationError(
                "consumer replay hash differs from signed envelope/result"
            )
        envelope = self.result.execution_envelope
        values = dict(envelope.consumer_values_read)
        values["consumer_result_hash"] = actual.result_hash
        values["consumer_result_state"] = actual.result_state
        values["consumer_result_material"] = canonicalize(actual.material())
        values["original_execution_provenance"] = envelope.execution_provenance
        values["original_execution_mode"] = envelope.execution_mode
        return values

    def e04_step(self) -> Mapping[str, Any]:
        values = self.read()
        return {
            "target": "POSITIONED_SUBJECT_TARGET",
            "target_ref": values["target_ref"],
            "conditioners": [
                [condition["occurrence"]["item"], condition["typed_value"]]
                for condition in values["ordered_conditions"]
            ],
            "state": values["result_state"],
            "denominator": values["denominator"],
            "cells": [
                {
                    "cell": cell["cell"],
                    "raw_numerator_support": cell["raw_numerator_support"],
                }
                for cell in values["cells"]
            ],
            "evidence_ref": values["evidence_ref"],
            "composed_hash": values["consumer_result_hash"],
            "request_key": values["request_key"],
        }


@dataclass(frozen=True)
class SupportSummary:
    total_required: int
    eligibility_counts: Mapping[str, int]
    execution_counts: Mapping[str, int]
    result_counts: Mapping[str, int]
    denominator_support: int
    unresolved_denominator_support: int
    positive_support_count: int
    valid_empty_frontier: bool
    exact_all_support: bool
    productive_all_required: bool
    support_state: str
    request_keys: tuple[str, ...]

    def material(self) -> Mapping[str, Any]:
        return {
            "contract": SUMMARY_CONTRACT_ID,
            "total_required": self.total_required,
            "eligibility_counts": dict(self.eligibility_counts),
            "execution_counts": dict(self.execution_counts),
            "result_counts": dict(self.result_counts),
            "denominator_support": self.denominator_support,
            "unresolved_denominator_support": self.unresolved_denominator_support,
            "positive_support_count": self.positive_support_count,
            "valid_empty_frontier": self.valid_empty_frontier,
            "exact_all_support": self.exact_all_support,
            "productive_all_required": self.productive_all_required,
            "support_state": self.support_state,
            "request_keys": list(self.request_keys),
        }

    @property
    def summary_hash(self) -> str:
        return semantic_hash(self.material())


def reduce_required_support(
    results: Iterable[EvidenceResult], *, valid_empty_frontier: bool = False
) -> SupportSummary:
    materialized = tuple(results)
    if any(not isinstance(result, EvidenceResult) for result in materialized):
        raise EvidenceBindingError("support reduction requires EvidenceResult objects")
    keys = tuple(result.request_key for result in materialized)
    if len(set(keys)) != len(keys):
        raise EvidenceBindingError(
            "duplicate request keys: repeated results cannot double count support"
        )
    total = len(materialized)
    eligibility_counts = Counter(x.eligibility_state for x in materialized)
    execution_counts = Counter(x.execution_state for x in materialized)
    result_counts = Counter(x.result_state for x in materialized)
    denominator_support = sum(
        x.denominator for x in materialized if x.denominator is not None
    )
    unresolved_denominator_support = sum(
        x.denominator
        for x in materialized
        if x.denominator is not None
        and (x.result_state == "UNKNOWN" or x.execution_state != "COMPLETED")
    )
    positive = result_counts.get("SUPPORTED", 0)
    exact_all_support = total > 0 and all(
        x.eligibility_state == "ELIGIBLE"
        and x.execution_state == "COMPLETED"
        and x.result_state == "SUPPORTED"
        for x in materialized
    )
    productive_all_required = total > 0 and all(x.productive for x in materialized)
    if total == 0:
        support_state = "VALID_EMPTY" if valid_empty_frontier else "NO_REQUIRED_SUPPORT"
    elif exact_all_support:
        support_state = "EXACT_SUPPORT"
    elif productive_all_required:
        productive_states = {
            state for state in result_counts if state in PRODUCTIVE_RESULT_STATES
        }
        support_state = (
            f"{next(iter(productive_states))}_PRODUCTIVE"
            if len(productive_states) == 1
            else "MIXED_VALID_PRODUCTS"
        )
    elif positive:
        support_state = "PARTIAL_SUPPORT"
    elif result_counts.get("ZERO_SUPPORT"):
        support_state = "ZERO_SUPPORT"
    elif result_counts.get("UNKNOWN"):
        support_state = "UNKNOWN_SUPPORT"
    else:
        support_state = "NO_SUPPORT"
    return SupportSummary(
        total_required=total,
        eligibility_counts=dict(sorted(eligibility_counts.items())),
        execution_counts=dict(sorted(execution_counts.items())),
        result_counts=dict(sorted(result_counts.items())),
        denominator_support=denominator_support,
        unresolved_denominator_support=unresolved_denominator_support,
        positive_support_count=positive,
        valid_empty_frontier=bool(valid_empty_frontier),
        exact_all_support=exact_all_support,
        productive_all_required=productive_all_required,
        support_state=support_state,
        request_keys=keys,
    )


__all__ = [
    "REQUEST_CONTRACT_ID",
    "RESULT_CONTRACT_ID",
    "SUMMARY_CONTRACT_ID",
    "CACHE_SCHEMA",
    "CACHE_OWNER_DESCRIPTOR_SCHEMA",
    "CACHE_OWNER_FIELDS",
    "CACHE_OWNER_DESCRIPTOR_FIELDS",
    "CACHE_TRUST_ASSOCIATION",
    "CACHE_TRUST_ISSUER",
    "CACHE_TRUST_ADMISSION",
    "K_ENCODING_VERSION",
    "ELIGIBILITY_STATES",
    "EXECUTION_STATES",
    "RESULT_STATES",
    "PRODUCTIVE_RESULT_STATES",
    "PROVENANCE_CANONICAL",
    "PROVENANCE_CACHE",
    "PROVENANCE_REFUSAL",
    "REFUSAL_IDENTITY_MISMATCH",
    "REFUSAL_NO_EXACT_BINDING",
    "REFUSAL_MISSING_STRUCTURAL_STATE",
    "REFUSAL_STALE_CACHE",
    "REFUSAL_CONSUMER_ASSOCIATION",
    "REFUSAL_UNKNOWN_SUPPORT",
    "REFUSAL_UNSUPPORTED",
    "EvidenceBindingError",
    "EvidenceRequestShapeError",
    "EvidenceBindingMismatch",
    "EvidenceCacheIntegrityError",
    "EvidenceAssociationError",
    "TypedValue",
    "AdmittedEvidenceContext",
    "TrustedOwnerAdmission",
    "TrustedAdmissionAuthority",
    "TrustedAdmissionVerifier",
    "ExecutedEvidenceEnvelope",
    "R61_TRUST_DOMAIN",
    "R61_TRUST_DOMAIN_VERSION",
    "R61_TRUST_GRADE",
    "OccurrenceKey",
    "TypedCondition",
    "EvidenceRequest",
    "request_from_empirical_case",
    "EmpiricalProducerBinding",
    "EvidenceResult",
    "EvidenceResolver",
    "EvidenceConsumerReader",
    "SupportSummary",
    "reduce_required_support",
]
