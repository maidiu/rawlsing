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
from dataclasses import dataclass, field
from decimal import Decimal
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

REQUEST_CONTRACT_ID = "R61_UNIVERSAL_EVIDENCE_REQUEST@1"
RESULT_CONTRACT_ID = "R61_UNIVERSAL_EVIDENCE_RESULT@1"
SUMMARY_CONTRACT_ID = "R61_UNIVERSAL_SUPPORT_SUMMARY@1"
CACHE_SCHEMA = "R61_AUTHENTICATED_EVIDENCE_CACHE@1"
CACHE_SEAL_ALGORITHM = "SHA256_CANONICAL_FULLK_PRODUCER_CONSUMER_PREIMAGE"
K_ENCODING_VERSION = "K_TAGGED_CANONICAL@1"

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
) -> EvidenceRequest:
    """Build K from actual accepted owner objects (no copied producer hashes)."""

    if len(consumer_query.conditioner_bindings) != 1:
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
        consumer_binding_fingerprint=semantic_hash(binding.material()),
        source_universe_ref=consumer_query.source_universe_ref,
        target_ref=consumer_query.target_ref,
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
    producer: Callable[..., EmpiricalPossibilitySliceProviderResult] = field(
        default=provide_empirical_possibility_slice, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        if not isinstance(self.request, EvidenceRequest):
            raise EvidenceBindingMismatch("binding.request must be EvidenceRequest")
        if self.request.consumer_query_ref != self.consumer_query.ref:
            raise EvidenceBindingMismatch("request consumer query ref mismatch")
        if self.request.producer_query_ref != self.empirical_query.ref:
            raise EvidenceBindingMismatch("request producer query ref mismatch")
        if self.request.predicate_ref != self.predicate.ref:
            raise EvidenceBindingMismatch("request predicate ref mismatch")
        if self.request.predicate_hash != self.predicate.predicate_hash:
            raise EvidenceBindingMismatch("request predicate hash mismatch")
        if tuple(sorted(self.release_refs, key=lambda x: x.key)) != (
            self.request.release_ref,
        ):
            raise EvidenceBindingMismatch("request release ref mismatch")
        if self.request.model_rule_hash != self.model_rule.rule_hash:
            raise EvidenceBindingMismatch("request model rule hash mismatch")
        if len(self.consumer_query.conditioner_bindings) != 1:
            raise EvidenceBindingMismatch("C1 single-conditioner grain required")
        if (
            self.request.consumer_binding_fingerprint
            != semantic_hash(self.consumer_query.conditioner_bindings[0].material())
        ):
            raise EvidenceBindingMismatch("request consumer binding fingerprint mismatch")
        if self.request.source_universe_ref != self.consumer_query.source_universe_ref:
            raise EvidenceBindingMismatch("request source universe mismatch")
        if self.request.target_ref != self.consumer_query.target_ref:
            raise EvidenceBindingMismatch("request target ref mismatch")
        if self.request.risk_set_ref != exact_ref(
            self.empirical_query.risk_set_ref, "risk_set_ref"
        ):
            raise EvidenceBindingMismatch("request risk set mismatch")
        if tuple(self.request.ordered_target_refs) != tuple(
            exact_ref(target, "target_ref")
            for target in self.empirical_query.target_refs
        ):
            raise EvidenceBindingMismatch("request ordered targets mismatch")

    def identity_material(self) -> Mapping[str, Any]:
        return {
            "request_key": self.request.key,
            "producer_query_ref": self.empirical_query.ref.as_dict(),
            "predicate_ref": self.predicate.ref.as_dict(),
            "predicate_hash": self.predicate.predicate_hash,
            "release_refs": [x.as_dict() for x in self.release_refs],
            "consumer_query_ref": self.consumer_query.ref.as_dict(),
            "consumer_binding_fingerprint": semantic_hash(
                self.consumer_query.conditioner_bindings[0].material()
            ),
            "model_rule_hash": self.model_rule.rule_hash,
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
    composition: AnalyticalCompositionResult,
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
        "denominator": composition.raw_denominator_support,
        "cells": [canonicalize(cell) for cell in _cells(composition)],
        "model_rule_hash": request.model_rule_hash,
    }


class EvidenceResolver:
    """Exact full-K registry and authenticated-cache resolver."""

    def __init__(self) -> None:
        self._bindings: dict[str, EmpiricalProducerBinding] = {}
        self._cache: dict[str, EvidenceResult] = {}

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
        if (
            binding.request.material() != request.material()
            or binding.request.key != request.key
        ):
            return _result_refusal(request, REFUSAL_IDENTITY_MISMATCH)
        result = self._produce(binding)
        if result.result_state == "SUPPORTED":
            self._cache[request.key] = result
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
                return _result_refusal(
                    request, REFUSAL_MISSING_STRUCTURAL_STATE
                )
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
            values = _consumer_values(
                request, evidence, actual_consumer, composition
            )
            return EvidenceResult(
                request_key=request.key,
                eligibility_state="ELIGIBLE",
                execution_state="COMPLETED",
                result_state="SUPPORTED",
                provenance=PROVENANCE_CANONICAL,
                denominator=composition.raw_denominator_support,
                cells=_cells(composition),
                evidence_ref=evidence.evidence_ref,
                producer_receipt_ref=provider.receipt_ref,
                producer_fact_ref=composition.producer_fact_ref,
                producer_fact_state=composition.producer_fact_state,
                consumer_query_ref=request.consumer_query_ref,
                consumer_result_state=actual_consumer.result_state,
                consumer_result_hash=actual_consumer.result_hash,
                consumer_values_read=values,
                uncertainty_state=composition.uncertainty_state,
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

    def _replay_cache(
        self, request: EvidenceRequest, cached: EvidenceResult
    ) -> EvidenceResult:
        if cached.request_key != request.key:
            return _result_refusal(request, REFUSAL_IDENTITY_MISMATCH)
        if cached.result_state != "SUPPORTED":
            return EvidenceResult(
                request_key=cached.request_key,
                eligibility_state=cached.eligibility_state,
                execution_state=cached.execution_state,
                result_state=cached.result_state,
                provenance=PROVENANCE_CACHE,
                denominator=cached.denominator,
                producer_receipt_ref=cached.producer_receipt_ref,
                producer_fact_ref=cached.producer_fact_ref,
                producer_fact_state=cached.producer_fact_state,
                consumer_query_ref=cached.consumer_query_ref,
                uncertainty_state=cached.uncertainty_state,
                typed_refusal=cached.typed_refusal,
            )
        evidence = cached.evidence_object
        query = cached.consumer_query_object
        rule = cached.model_rule_object
        if evidence is None or query is None or rule is None:
            return _result_refusal(request, REFUSAL_STALE_CACHE)
        actual = evaluate_positioned_subject_possibility(
            query=query, rule=rule, evidence=(evidence,)
        )
        if actual.result_hash != cached.consumer_result_hash:
            return _result_refusal(request, REFUSAL_STALE_CACHE)
        values = dict(cached.consumer_values_read or {})
        values["request_key"] = request.key
        values["cache_seal"] = semantic_hash(cached.material())
        return EvidenceResult(
            request_key=request.key,
            eligibility_state=cached.eligibility_state,
            execution_state=cached.execution_state,
            result_state=cached.result_state,
            provenance=PROVENANCE_CACHE,
            denominator=cached.denominator,
            cells=cached.cells,
            evidence_ref=cached.evidence_ref,
            producer_receipt_ref=cached.producer_receipt_ref,
            producer_fact_ref=cached.producer_fact_ref,
            producer_fact_state=cached.producer_fact_state,
            consumer_query_ref=cached.consumer_query_ref,
            consumer_result_state=actual.result_state,
            consumer_result_hash=actual.result_hash,
            consumer_values_read=values,
            uncertainty_state=cached.uncertainty_state,
            evidence_object=evidence,
            consumer_query_object=query,
            model_rule_object=rule,
            consumer_result_object=actual,
        )

    def export_cache(self) -> Mapping[str, Any]:
        entries = []
        for key in sorted(self._cache):
            result = self._cache[key]
            payload = {
                "schema": CACHE_SCHEMA,
                "seal_algorithm": CACHE_SEAL_ALGORITHM,
                "request_key": key,
                "result": canonicalize(result.material()),
                "evidence": None
                if result.evidence_object is None
                else _evidence_material(result.evidence_object),
                "consumer_query": None
                if result.consumer_query_object is None
                else canonicalize(result.consumer_query_object.material()),
                "model_rule": None
                if result.model_rule_object is None
                else canonicalize(result.model_rule_object.material()),
            }
            entries.append({**payload, "seal": semantic_hash(payload)})
        return {"schema": CACHE_SCHEMA, "entries": entries}

    def import_authenticated_cache(self, material: Mapping[str, Any]) -> None:
        if not isinstance(material, Mapping) or material.get("schema") != CACHE_SCHEMA:
            raise EvidenceCacheIntegrityError("unrecognized authenticated cache schema")
        entries = material.get("entries")
        if not isinstance(entries, Sequence) or isinstance(entries, (str, bytes)):
            raise EvidenceCacheIntegrityError("cache entries must be a sequence")
        imported: dict[str, EvidenceResult] = {}
        for raw in entries:
            if not isinstance(raw, Mapping):
                raise EvidenceCacheIntegrityError("cache entry must be a mapping")
            payload = {
                key: canonicalize(value)
                for key, value in raw.items()
                if key != "seal"
            }
            seal = raw.get("seal")
            if seal != semantic_hash(payload):
                raise EvidenceCacheIntegrityError("cache entry seal mismatch")
            request_key = _sha(raw.get("request_key"), "cache.request_key")
            result_material = raw.get("result")
            if not isinstance(result_material, Mapping):
                raise EvidenceCacheIntegrityError("cache result material required")
            if result_material.get("request_key") != request_key:
                raise EvidenceCacheIntegrityError("cache request key mismatch")
            evidence = None
            evidence_material = raw.get("evidence")
            if evidence_material is not None:
                evidence = _evidence_from_material(evidence_material)
            query = None
            query_material = raw.get("consumer_query")
            if query_material is not None:
                query = _query_from_material(query_material)
            rule = None
            rule_material = raw.get("model_rule")
            if rule_material is not None:
                rule = _rule_from_material(rule_material)
            result = EvidenceResult(
                request_key=request_key,
                eligibility_state=result_material["eligibility_state"],
                execution_state=result_material["execution_state"],
                result_state=result_material["result_state"],
                provenance=PROVENANCE_CACHE,
                denominator=result_material["denominator"],
                cells=tuple(result_material["cells"]),
                evidence_ref=_optional_ref(result_material["evidence_ref"]),
                producer_receipt_ref=_optional_ref(
                    result_material["producer_receipt_ref"]
                ),
                producer_fact_ref=_optional_ref(result_material["producer_fact_ref"]),
                producer_fact_state=result_material["producer_fact_state"],
                consumer_query_ref=_optional_ref(
                    result_material["consumer_query_ref"]
                ),
                consumer_result_state=result_material["consumer_result_state"],
                consumer_result_hash=result_material["consumer_result_hash"],
                consumer_values_read=result_material["consumer_values_read"],
                uncertainty_state=result_material["uncertainty_state"],
                typed_refusal=result_material["typed_refusal"],
                evidence_object=evidence,
                consumer_query_object=query,
                model_rule_object=rule,
            )
            if result.result_state == "SUPPORTED":
                if evidence is None or query is None or rule is None:
                    raise EvidenceCacheIntegrityError(
                        "supported cache entry requires evidence/query/rule"
                    )
                actual = evaluate_positioned_subject_possibility(
                    query=query, rule=rule, evidence=(evidence,)
                )
                if actual.result_hash != result.consumer_result_hash:
                    raise EvidenceCacheIntegrityError(
                        "cached consumer result does not replay"
                    )
                if (
                    result.evidence_ref is None
                    or evidence.evidence_ref != result.evidence_ref
                ):
                    raise EvidenceCacheIntegrityError("cached evidence ref mismatch")
            if request_key in imported:
                raise EvidenceCacheIntegrityError("duplicate cache request key")
            imported[request_key] = result
        if set(imported) & set(self._bindings):
            raise EvidenceCacheIntegrityError(
                "cache/import conflicts with a registered producer binding"
            )
        self._cache.update(imported)


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

    def __init__(self, request: EvidenceRequest, result: EvidenceResult) -> None:
        if not isinstance(request, EvidenceRequest):
            raise EvidenceAssociationError("request must be EvidenceRequest")
        if not isinstance(result, EvidenceResult):
            raise EvidenceAssociationError("result must be EvidenceResult")
        self.request = request
        self.result = result

    def _assert_association(self) -> None:
        if self.request.key != self.result.request_key:
            raise EvidenceAssociationError(
                "request/result K mismatch: refusing target/depth reuse"
            )
        if self.result.result_state != "SUPPORTED":
            raise EvidenceAssociationError(
                f"result is not exact support: {self.result.result_state}"
            )
        values = self.result.consumer_values_read
        if not isinstance(values, Mapping):
            raise EvidenceAssociationError("actual consumer values-read is absent")
        if values.get("request_key") != self.request.key:
            raise EvidenceAssociationError("values-read request key mismatch")
        if values.get("consumer_query_ref") != self.request.consumer_query_ref.as_dict():
            raise EvidenceAssociationError("values-read consumer query mismatch")
        if values.get("target_ref") != self.request.target_ref.as_dict():
            raise EvidenceAssociationError("values-read target mismatch")
        if values.get("ordered_conditions") != [
            x.material() for x in self.request.ordered_conditions
        ]:
            raise EvidenceAssociationError("values-read condition/value mismatch")
        if values.get("direction") != self.request.direction:
            raise EvidenceAssociationError("values-read direction mismatch")
        if values.get("role") != self.request.role:
            raise EvidenceAssociationError("values-read role mismatch")
        if self.result.evidence_object is None:
            raise EvidenceAssociationError("no actual evidence object to consume")
        if self.result.consumer_query_object is None or self.result.model_rule_object is None:
            raise EvidenceAssociationError("no actual consumer query/rule to consume")

    def read(self) -> Mapping[str, Any]:
        self._assert_association()
        actual = evaluate_positioned_subject_possibility(
            query=self.result.consumer_query_object,
            rule=self.result.model_rule_object,
            evidence=(self.result.evidence_object,),
        )
        if actual.result_hash != self.result.consumer_result_hash:
            raise EvidenceAssociationError(
                "consumer replay hash differs from bound result"
            )
        values = dict(self.result.consumer_values_read or {})
        values["consumer_result_hash"] = actual.result_hash
        values["consumer_result_state"] = actual.result_state
        values["consumer_result_material"] = canonicalize(actual.material())
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
    elif positive:
        support_state = "PARTIAL_SUPPORT"
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
