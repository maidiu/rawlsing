"""N10E empirical possibility-slice provider core: public seam over accepted C1-01.

This module is a *service/provider seam*, not an empirical calculator. It owns no
survey semantics, comparability meaning, possibility-model authority, structural
admission, or actor/person state. It carries exact caller-supplied determinants
into the already-accepted public analytical composition path and returns the
generated evidence plus an auditable provider receipt.

Ownership law (unchanged here):

* accepted analytical producer
  ``rawlsing_next.pre553_analytical_composition.compose_positioned_subject_possibility``;
* accepted public possibility consumer
  ``rawlsing_next.source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility``.

The provider never accepts a caller-supplied ``PossibilitySliceEvidence`` and never
accepts precomputed probability geometry as authoritative input. Slice geometry is
produced only by the accepted producer path from exact empirical products.

EPISTEMIC_CEILING: a PROVIDER RECEIPT is not an adoption, not a structural-world
claim, not an actor/person state, and not an AT33 progressive-world proof.
"""
from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_objects import (
    ExactRef,
    Pre553IntegrityError,
    canonicalize,
    semantic_hash,
)
from rawlsing_next.pre553_analytical_composition import (
    AnalyticalCompositionResult,
    compose_positioned_subject_possibility,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
    PositionedSubjectPossibilityResult,
    PossibilitySliceEvidence,
    evaluate_positioned_subject_possibility,
)

PROVIDER_CONTRACT_ID = "N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER@1.0.0"
PROVIDER_ROUTE = "EMPIRICAL_QUERY__C1_ANALYTICAL_COMPOSITION__GENERATED_EVIDENCE"
PROVIDER_INPUT_MODE = "EXACT_DETERMINANTS_ONLY__NO_PRECOMPUTED_SLICE_GEOMETRY"
RECEIPT_SCHEMA = "N10E_EMPIRICAL_SLICE_PROVIDER_RECEIPT@1"
RECEIPT_CONTRACT_ID = "N10E_EMPIRICAL_SLICE_PROVIDER_RECEIPT_REF@1"
PROVIDER_STATE_EXACT = "EXACT_SUPPORTED_SLICE_PRODUCED"
PROVIDER_STATE_REFUSED = "TYPED_REFUSAL"

REFUSAL_STATE_MISSING_EXACT_MODEL_OR_PRODUCER_AUTHORITY = (
    "MISSING_EXACT_MODEL_OR_PRODUCER_AUTHORITY"
)
REFUSAL_STATE_SLICE_NOT_SUPPORTED = "SLICE_NOT_SUPPORTED_UNDER_EXACT_MODEL_LAW"
REFUSAL_STATE_OWNER_ERROR = "OWNER_TYPED_REFUSAL"

PROVIDER_REFUSAL_STATES = frozenset(
    {
        REFUSAL_STATE_MISSING_EXACT_MODEL_OR_PRODUCER_AUTHORITY,
        REFUSAL_STATE_SLICE_NOT_SUPPORTED,
        REFUSAL_STATE_OWNER_ERROR,
    }
)

#: Fact states that reach provider refusal. ``UNSUPPORTED`` is included for
#: interface totality: a fact-level unsupported typed state discovered downstream
#: becomes a typed refusal (never invented geometry), not an untyped crash.
NON_SUPPORTED_FACT_STATES = frozenset(
    {
        "ZERO_SUPPORT",
        "OBSERVED_ZERO",
        "ZERO_OVERLAP",
        "LOW_SUPPORT",
        "NONCOMPARABLE",
        "NOT_APPLICABLE",
        "UNAVAILABLE",
        "UNRESOLVED",
        "VALID_EMPTY",
        "INTEGRITY_FAILURE",
        "UNSUPPORTED",
    }
)

#: Shapes the provider public API must never expose as authoritative input.
FORBIDDEN_AUTHORITATIVE_INPUT_NAMES = frozenset(
    {
        "evidence",
        "possibility_slice_evidence",
        "slice_evidence",
        "geometry",
        "slice_geometry",
        "precomputed_geometry",
        "probability",
        "probabilities",
        "probability_geometry",
    }
)


class EmpiricalPossibilityProviderError(Pre553IntegrityError):
    """Typed N10E provider-contract failure.

    This type is raised only for provider-contract violations. Owner-law failures
    (``AnalyticalCompositionError`` and upstream typed errors) are deliberately
    *not* laundered or bridged: they propagate unchanged from the accepted owners.
    """


class ProviderRequestShapeError(EmpiricalPossibilityProviderError):
    code = "PROVIDER_REQUEST_SHAPE_ERROR"


def _require(condition: bool, detail: str) -> None:
    if not condition:
        raise ProviderRequestShapeError(f"PROVIDER_REQUEST_SHAPE_ERROR: {detail}")


def _public_signature() -> inspect.Signature:
    return inspect.signature(provide_empirical_possibility_slice)


def assert_provider_public_api_excludes_handwritten_slice() -> None:
    """Fail closed if the public API ever grows a precomputed-slice channel."""

    names = set(_public_signature().parameters)
    forbidden = sorted(names & FORBIDDEN_AUTHORITATIVE_INPUT_NAMES)
    if forbidden:
        raise ProviderRequestShapeError(
            "PROVIDER_REQUEST_SHAPE_ERROR: public API exposes authoritative "
            f"precomputed slice input names: {forbidden!r}"
        )


@dataclass(frozen=True)
class EmpiricalPossibilityProviderRequest:
    """Exact caller-supplied determinants for one N10E provider invocation.

    ``repository`` and ``authority_registry`` are *carried* execution handles. They
    are not identity-hashed here: their identity is bound by the exact
    ``release_refs`` and the authority refs already embedded in the empirical
    query, predicate, consumer query, witness and model rule.

    The request deliberately has no geometry/probability field, so a caller cannot
    satisfy the provider with precomputed probability geometry.
    """

    repository: Any
    empirical_query: Any
    predicate: Any
    authority_registry: Any
    release_refs: tuple[ExactRef, ...]
    consumer_query: PositionedSubjectPossibilityQuery
    model_rule: PositionedSubjectPossibilityModelRule
    condition_binding_witness: Any

    def __post_init__(self) -> None:
        _require(
            isinstance(self.consumer_query, PositionedSubjectPossibilityQuery),
            "consumer_query must be a PositionedSubjectPossibilityQuery",
        )
        _require(
            isinstance(self.model_rule, PositionedSubjectPossibilityModelRule),
            "model_rule must be a PositionedSubjectPossibilityModelRule",
        )
        for name in ("repository", "empirical_query", "predicate", "authority_registry"):
            _require(getattr(self, name) is not None, f"{name} is required")
        release_refs = tuple(self.release_refs)
        _require(bool(release_refs), "release_refs may not be empty")
        _require(
            all(isinstance(x, ExactRef) for x in release_refs),
            "release_refs must be ExactRef",
        )
        object.__setattr__(
            self, "release_refs", tuple(sorted(set(release_refs), key=lambda x: x.key))
        )
        binding = _single_binding(self.consumer_query)
        for name in (
            "source_universe_ref",
            "release_ref",
            "comparability_authority_ref",
            "subject_fact_ref",
            "empirical_coordinate_ref",
        ):
            _require(
                getattr(binding, name) is not None,
                f"consumer conditioner binding {name} is required",
            )

    def identity_bindings(self) -> Mapping[str, Any]:
        """Exact identities the request is bound to (no handle objects)."""

        return {
            "provider_contract_id": PROVIDER_CONTRACT_ID,
            "provider_input_mode": PROVIDER_INPUT_MODE,
            "empirical_query_ref": self.empirical_query.ref.as_dict(),
            "predicate_ref": self.predicate.ref.as_dict(),
            "predicate_hash": self.predicate.predicate_hash,
            "release_refs": [x.as_dict() for x in self.release_refs],
            "consumer_query_ref": self.consumer_query.ref.as_dict(),
            "consumer_binding_fingerprint": semantic_hash(
                _single_binding(self.consumer_query).material()
            ),
            "model_rule_hash": self.model_rule.rule_hash,
            "condition_binding_witness_ref": (
                self.condition_binding_witness.witness_ref.as_dict()
            ),
            "source_universe_ref": self.consumer_query.source_universe_ref.as_dict(),
            "target_ref": self.consumer_query.target_ref.as_dict(),
        }


@dataclass(frozen=True)
class EmpiricalPossibilitySliceProviderReceipt:
    """Auditable provider receipt: producer input -> generated evidence -> consumer."""

    provider_contract_id: str
    provider_route: str
    provider_state: str
    producer_query_ref: ExactRef
    producer_predicate_ref: ExactRef
    producer_fact_ref: ExactRef
    producer_fact_state: str
    source_universe_refs: tuple[ExactRef, ...]
    release_refs: tuple[ExactRef, ...]
    consumer_query_ref: ExactRef
    consumer_binding_fingerprint: str
    condition_binding_witness_ref: ExactRef
    model_rule_hash: str
    generated_evidence_ref: ExactRef | None
    generated_evidence_identity_is_producer_derived: bool
    consumer_result_state: str | None
    consumer_result_identity_hash: str | None
    composed_result_identity_hash: str
    refusal_state: str | None = None

    def __post_init__(self) -> None:
        _require(
            self.provider_contract_id == PROVIDER_CONTRACT_ID,
            "unexpected provider contract id",
        )
        _require(self.provider_route == PROVIDER_ROUTE, "unexpected provider route")
        _require(
            self.provider_state in {PROVIDER_STATE_EXACT, PROVIDER_STATE_REFUSED},
            "unexpected provider state",
        )
        for name in (
            "producer_query_ref",
            "producer_predicate_ref",
            "producer_fact_ref",
            "consumer_query_ref",
            "condition_binding_witness_ref",
        ):
            _require(
                isinstance(getattr(self, name), ExactRef), f"{name} must be ExactRef"
            )
        _require(
            len(self.composed_result_identity_hash) == 64,
            "composed_result_identity_hash must be sha256",
        )
        _require(len(self.model_rule_hash) == 64, "model_rule_hash must be sha256")
        if self.provider_state == PROVIDER_STATE_EXACT:
            _require(self.refusal_state is None, "exact receipt may not carry refusal")
        else:
            _require(
                self.refusal_state in PROVIDER_REFUSAL_STATES,
                "refusal receipt requires a governed refusal state",
            )
            _require(
                self.generated_evidence_ref is None
                and self.consumer_result_identity_hash is None,
                "refusal receipt may not carry evidence or consumer result identity",
            )
            _require(
                self.generated_evidence_identity_is_producer_derived is False,
                "refusal receipt may not claim producer-derived evidence",
            )

    def material(self) -> Mapping[str, Any]:
        return {
            "schema": RECEIPT_SCHEMA,
            "provider_contract_id": self.provider_contract_id,
            "provider_route": self.provider_route,
            "provider_state": self.provider_state,
            "producer_input": {
                "producer_query_ref": self.producer_query_ref.as_dict(),
                "producer_predicate_ref": self.producer_predicate_ref.as_dict(),
                "producer_fact_ref": self.producer_fact_ref.as_dict(),
                "producer_fact_state": self.producer_fact_state,
                "source_universe_refs": [x.as_dict() for x in self.source_universe_refs],
                "release_refs": [x.as_dict() for x in self.release_refs],
            },
            "generated_evidence": {
                "evidence_ref_or_null": (
                    None
                    if self.generated_evidence_ref is None
                    else self.generated_evidence_ref.as_dict()
                ),
                "identity_is_producer_derived": (
                    self.generated_evidence_identity_is_producer_derived
                ),
            },
            "consumer": {
                "consumer_query_ref": self.consumer_query_ref.as_dict(),
                "consumer_binding_fingerprint": self.consumer_binding_fingerprint,
                "condition_binding_witness_ref": (
                    self.condition_binding_witness_ref.as_dict()
                ),
                "result_state_or_null": self.consumer_result_state,
                "result_identity_hash_or_null": self.consumer_result_identity_hash,
            },
            "composed_result_identity_hash": self.composed_result_identity_hash,
            "model_rule_hash": self.model_rule_hash,
            "refusal_state_or_null": self.refusal_state,
        }

    def identity_material(self) -> Mapping[str, Any]:
        """Receipt identity preimage.

        The receipt's own ref/hash is deliberately excluded so the identity is
        well-founded (no self-referential digest).
        """

        return {
            "schema": RECEIPT_SCHEMA,
            "provider_contract_id": self.provider_contract_id,
            "provider_route": self.provider_route,
            "provider_state": self.provider_state,
            "producer_query_ref": self.producer_query_ref.as_dict(),
            "producer_predicate_ref": self.producer_predicate_ref.as_dict(),
            "producer_fact_ref": self.producer_fact_ref.as_dict(),
            "producer_fact_state": self.producer_fact_state,
            "source_universe_refs": [x.as_dict() for x in self.source_universe_refs],
            "release_refs": [x.as_dict() for x in self.release_refs],
            "consumer_query_ref": self.consumer_query_ref.as_dict(),
            "consumer_binding_fingerprint": self.consumer_binding_fingerprint,
            "condition_binding_witness_ref": (
                self.condition_binding_witness_ref.as_dict()
            ),
            "model_rule_hash": self.model_rule_hash,
            "generated_evidence_ref_or_null": (
                None
                if self.generated_evidence_ref is None
                else self.generated_evidence_ref.as_dict()
            ),
            "generated_evidence_identity_is_producer_derived": (
                self.generated_evidence_identity_is_producer_derived
            ),
            "consumer_result_state_or_null": self.consumer_result_state,
            "consumer_result_identity_hash_or_null": (
                self.consumer_result_identity_hash
            ),
            "composed_result_identity_hash": self.composed_result_identity_hash,
            "refusal_state_or_null": self.refusal_state,
        }

    @property
    def receipt_hash(self) -> str:
        return semantic_hash(self.identity_material())

    @property
    def receipt_ref(self) -> ExactRef:
        h = self.receipt_hash
        return ExactRef(
            RECEIPT_CONTRACT_ID,
            f"urn:rawlsing:n10e:empirical-slice-provider-receipt:sha256:{h}",
            h,
        )

    @property
    def replay_identity(self) -> str:
        return self.receipt_ref.object_id


@dataclass(frozen=True)
class EmpiricalPossibilitySliceProviderResult:
    """Provider output: exact generated slice, consumer result, receipt, or refusal.

    Constructor guards make the result hostile to silent substitution: exact output
    must be producer-derived and carry evidence, while a refusal must carry no
    evidence and no geometry. There is no field for caller-supplied geometry.
    """

    provider_state: str
    provider_receipt: EmpiricalPossibilitySliceProviderReceipt
    composition_result: AnalyticalCompositionResult
    generated_evidence_or_null: PossibilitySliceEvidence | None
    consumer_result_or_null: PositionedSubjectPossibilityResult | None
    refusal_state: str | None = None
    refusal_reason: str | None = None
    refusal_owner_error_code: str | None = None

    def __post_init__(self) -> None:
        _require(
            isinstance(self.provider_receipt, EmpiricalPossibilitySliceProviderReceipt),
            "provider_receipt is required",
        )
        _require(
            isinstance(self.composition_result, AnalyticalCompositionResult),
            "composition_result is required",
        )
        _require(
            self.provider_receipt.provider_state == self.provider_state,
            "receipt/result provider state mismatch",
        )
        _require(
            self.provider_receipt.composed_result_identity_hash
            == self.composition_result.composed_result_identity_hash,
            "receipt/composition identity mismatch",
        )
        if self.provider_state == PROVIDER_STATE_EXACT:
            _require(self.refusal_state is None, "exact result may not carry refusal")
            _require(
                self.generated_evidence_or_null is not None,
                "exact result requires generated evidence",
            )
            _require(
                self.consumer_result_or_null is not None,
                "exact result requires a consumer result",
            )
            _require(
                self.generated_evidence_or_null is (
                    self.composition_result.possibility_slice_evidence_or_null
                ),
                "exact result evidence must be the composition's generated evidence object",
            )
            _require(
                self.consumer_result_or_null
                is self.composition_result.consumer_result_or_null,
                "exact result consumer must be the composition's consumer result object",
            )
        else:
            _require(
                self.provider_state == PROVIDER_STATE_REFUSED,
                "unexpected provider state",
            )
            _require(
                self.refusal_state in PROVIDER_REFUSAL_STATES,
                "refusal requires a governed refusal state",
            )
            _require(
                self.generated_evidence_or_null is None
                and self.consumer_result_or_null is None,
                "refusal may not carry evidence or consumer result",
            )

    def material(self) -> Mapping[str, Any]:
        return {
            "provider_state": self.provider_state,
            "provider_receipt": self.provider_receipt.material(),
            "generated_evidence_ref_or_null": (
                None
                if self.generated_evidence_or_null is None
                else self.generated_evidence_or_null.evidence_ref.as_dict()
            ),
            "consumer_result_identity_hash_or_null": (
                None
                if self.consumer_result_or_null is None
                else self.consumer_result_or_null.result_hash
            ),
            "refusal_state_or_null": self.refusal_state,
            "refusal_reason_or_null": self.refusal_reason,
            "refusal_owner_error_code_or_null": self.refusal_owner_error_code,
        }

    @property
    def receipt_ref(self) -> ExactRef:
        return self.provider_receipt.receipt_ref

    @property
    def result_identity_hash(self) -> str:
        return semantic_hash(self.material())


def _single_binding(
    query: PositionedSubjectPossibilityQuery,
) -> ConditionerBinding:
    if len(query.conditioner_bindings) != 1:
        raise ProviderRequestShapeError(
            "PROVIDER_REQUEST_SHAPE_ERROR: N10E R1 follows the accepted C1-01 "
            "scalar grain and requires exactly one conditioner binding"
        )
    return query.conditioner_bindings[0]


def _build_receipt(
    *,
    composition: AnalyticalCompositionResult,
    request: EmpiricalPossibilityProviderRequest,
    evidence: PossibilitySliceEvidence | None,
    consumer_result: PositionedSubjectPossibilityResult | None,
    provider_state: str,
    refusal_state: str | None,
) -> EmpiricalPossibilitySliceProviderReceipt:
    return EmpiricalPossibilitySliceProviderReceipt(
        provider_contract_id=PROVIDER_CONTRACT_ID,
        provider_route=PROVIDER_ROUTE,
        provider_state=provider_state,
        producer_query_ref=composition.producer_query_ref,
        producer_predicate_ref=composition.producer_predicate_ref,
        producer_fact_ref=composition.producer_fact_ref,
        producer_fact_state=composition.producer_fact_state,
        source_universe_refs=tuple(composition.source_universe_refs),
        release_refs=tuple(composition.release_refs),
        consumer_query_ref=composition.consumer_query_ref,
        consumer_binding_fingerprint=composition.consumer_binding_fingerprint,
        condition_binding_witness_ref=(
            composition.condition_binding_witness_ref_or_hash
        ),
        model_rule_hash=request.model_rule.rule_hash,
        generated_evidence_ref=(None if evidence is None else evidence.evidence_ref),
        generated_evidence_identity_is_producer_derived=(
            evidence is not None
            and evidence is composition.possibility_slice_evidence_or_null
        ),
        consumer_result_state=(
            None if consumer_result is None else consumer_result.result_state
        ),
        consumer_result_identity_hash=(
            None if consumer_result is None else consumer_result.result_hash
        ),
        composed_result_identity_hash=composition.composed_result_identity_hash,
        refusal_state=refusal_state,
    )


def provide_empirical_possibility_slice(
    *,
    repository: Any,
    empirical_query: Any,
    predicate: Any,
    authority_registry: Any,
    release_refs: Iterable[ExactRef],
    consumer_query: PositionedSubjectPossibilityQuery,
    model_rule: PositionedSubjectPossibilityModelRule,
    condition_binding_witness: Any,
) -> EmpiricalPossibilitySliceProviderResult:
    """Produce one governed empirical possibility slice through the accepted path.

    Exact path: empirical repository fact -> accepted C1-01 analytical composition
    -> generated slice evidence -> public positioned-subject possibility consumer
    -> provider receipt.

    Fail-closed law: source-universe, release, target-topology and witness/custody
    mismatches propagate as the owners' own typed errors. A producer fact that is
    not ``SUPPORTED`` returns a typed refusal with no evidence and no geometry; it
    is never replaced by invented, smoothed or proxy probability geometry.
    """

    assert_provider_public_api_excludes_handwritten_slice()

    if "evidence" in inspect.signature(
        provide_empirical_possibility_slice
    ).parameters:
        raise ProviderRequestShapeError(
            "PROVIDER_REQUEST_SHAPE_ERROR: provider may not accept a prebuilt slice"
        )

    request = EmpiricalPossibilityProviderRequest(
        repository=repository,
        empirical_query=empirical_query,
        predicate=predicate,
        authority_registry=authority_registry,
        release_refs=tuple(release_refs),
        consumer_query=consumer_query,
        model_rule=model_rule,
        condition_binding_witness=condition_binding_witness,
    )

    composition = compose_positioned_subject_possibility(
        repository=request.repository,
        empirical_query=request.empirical_query,
        predicate=request.predicate,
        authority_registry=request.authority_registry,
        release_refs=request.release_refs,
        consumer_query=request.consumer_query,
        model_rule=request.model_rule,
        condition_binding_witness=request.condition_binding_witness,
    )

    evidence = composition.possibility_slice_evidence_or_null
    consumer_result = composition.consumer_result_or_null

    if composition.producer_fact_state != "SUPPORTED" or evidence is None:
        state = composition.producer_fact_state
        refusal_state = (
            REFUSAL_STATE_OWNER_ERROR
            if state not in NON_SUPPORTED_FACT_STATES
            else REFUSAL_STATE_SLICE_NOT_SUPPORTED
        )
        receipt = _build_receipt(
            composition=composition,
            request=request,
            evidence=None,
            consumer_result=None,
            provider_state=PROVIDER_STATE_REFUSED,
            refusal_state=refusal_state,
        )
        return EmpiricalPossibilitySliceProviderResult(
            provider_state=PROVIDER_STATE_REFUSED,
            provider_receipt=receipt,
            composition_result=composition,
            generated_evidence_or_null=None,
            consumer_result_or_null=None,
            refusal_state=refusal_state,
            refusal_reason=(
                f"producer fact typed_state={state!r} produced no exact supported "
                "slice; N10E creates no smoothing, proxy or invented geometry"
            ),
            refusal_owner_error_code=state,
        )

    receipt = _build_receipt(
        composition=composition,
        request=request,
        evidence=evidence,
        consumer_result=consumer_result,
        provider_state=PROVIDER_STATE_EXACT,
        refusal_state=None,
    )
    return EmpiricalPossibilitySliceProviderResult(
        provider_state=PROVIDER_STATE_EXACT,
        provider_receipt=receipt,
        composition_result=composition,
        generated_evidence_or_null=evidence,
        consumer_result_or_null=consumer_result,
    )


def replay_empirical_possibility_slice(
    expected: EmpiricalPossibilitySliceProviderResult,
    *,
    repository: Any,
    empirical_query: Any,
    predicate: Any,
    authority_registry: Any,
    release_refs: Iterable[ExactRef],
    consumer_query: PositionedSubjectPossibilityQuery,
    model_rule: PositionedSubjectPossibilityModelRule,
    condition_binding_witness: Any,
) -> EmpiricalPossibilitySliceProviderResult:
    """Deterministic replay check: same frozen determinants -> same identities."""

    replayed = provide_empirical_possibility_slice(
        repository=repository,
        empirical_query=empirical_query,
        predicate=predicate,
        authority_registry=authority_registry,
        release_refs=tuple(release_refs),
        consumer_query=consumer_query,
        model_rule=model_rule,
        condition_binding_witness=condition_binding_witness,
    )
    if (
        replayed.result_identity_hash != expected.result_identity_hash
        or replayed.material() != expected.material()
    ):
        raise EmpiricalPossibilityProviderError(
            "N10E provider replay mismatch: deterministic identity not reproduced"
        )
    return replayed


def evaluate_generated_slice_directly(
    *,
    consumer_query: PositionedSubjectPossibilityQuery,
    model_rule: PositionedSubjectPossibilityModelRule,
    generated_evidence: PossibilitySliceEvidence,
) -> PositionedSubjectPossibilityResult:
    """Low-level consumer pass-through for an *already generated* slice only.

    This helper exists so a hostile court can prove the difference between a
    producer-derived slice and a handwritten one. It is not the provider path and
    grants no authority: it consumes an evidence object that some caller already
    holds, exactly as the public consumer already does.
    """

    return evaluate_positioned_subject_possibility(
        query=consumer_query,
        rule=model_rule,
        evidence=(generated_evidence,),
    )


__all__ = [
    "PROVIDER_CONTRACT_ID",
    "PROVIDER_ROUTE",
    "PROVIDER_INPUT_MODE",
    "RECEIPT_SCHEMA",
    "RECEIPT_CONTRACT_ID",
    "PROVIDER_STATE_EXACT",
    "PROVIDER_STATE_REFUSED",
    "PROVIDER_REFUSAL_STATES",
    "REFUSAL_STATE_MISSING_EXACT_MODEL_OR_PRODUCER_AUTHORITY",
    "REFUSAL_STATE_SLICE_NOT_SUPPORTED",
    "REFUSAL_STATE_OWNER_ERROR",
    "NON_SUPPORTED_FACT_STATES",
    "FORBIDDEN_AUTHORITATIVE_INPUT_NAMES",
    "EmpiricalPossibilityProviderError",
    "ProviderRequestShapeError",
    "EmpiricalPossibilityProviderRequest",
    "EmpiricalPossibilitySliceProviderReceipt",
    "EmpiricalPossibilitySliceProviderResult",
    "assert_provider_public_api_excludes_handwritten_slice",
    "provide_empirical_possibility_slice",
    "replay_empirical_possibility_slice",
    "evaluate_generated_slice_directly",
]
