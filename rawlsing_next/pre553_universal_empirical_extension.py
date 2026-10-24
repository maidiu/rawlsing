"""E41 versioned sourcefree public extension of the accepted N10E provider.

Contract: ``N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0``.

Why this exists
---------------
The accepted N10E provider (
``rawlsing_next.pre553_empirical_possibility_provider``) exposes only the
DIRECT_I03 route at one scalar conditioner binding. The already-accepted C1
machinery (``rawlsing_next.pre553_analytical_composition`` with
``discovery_result`` / ``recursive_handoff``) lawfully supports the
I05_EXACT_BOUNDED and MX01R2_RECURSIVE routes, but no public provider seam
carried them.

This NEW module is a *versioned, permission-bounded* extension. It owns no
empirical semantics and no geometry. It:

* delegates the DIRECT route to the accepted provider function itself (exact
  object reuse), and
* delegates the discovery/recursive routes to the accepted composition owner
  with the caller's exact discovery result/receipt/handoff,

returning the accepted composition result objects unchanged plus a v1.1
receipt that additionally records producer route, discovery/recursive refs,
coverage state and joint morphology.

EPISTEMIC_CEILING: a receipt is not an adoption, not a source right, not a
structural-world claim, not an actor/person state.
"""
from __future__ import annotations

from dataclasses import dataclass
import inspect
from pathlib import Path
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_analytical_composition import (
    AnalyticalCompositionResult,
    compose_positioned_subject_possibility,
)
from rawlsing_next.pre553_empirical_objects import (
    ExactRef,
    Pre553IntegrityError,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_possibility_provider import (
    NON_SUPPORTED_FACT_STATES,
    PROVIDER_STATE_EXACT,
    PROVIDER_STATE_REFUSED,
    REFUSAL_STATE_OWNER_ERROR,
    REFUSAL_STATE_SLICE_NOT_SUPPORTED,
    EmpiricalPossibilitySliceProviderResult,
    provide_empirical_possibility_slice,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
    PositionedSubjectPossibilityResult,
    PossibilitySliceEvidence,
)

EXT_CONTRACT_ID = "N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0"
EXT_RECEIPT_SCHEMA = "N10E_EMPIRICAL_SLICE_PROVIDER_RECEIPT@1.1"
EXT_ROUTE_DIRECT_VIA_ACCEPTED_PROVIDER = "DIRECT_VIA_ACCEPTED_PROVIDER_FUNCTION"
EXT_ROUTE_DIRECT_MULTI_CONDITIONER = "DIRECT_MULTI_CONDITIONER_VIA_ACCEPTED_COMPOSITION"
EXT_ROUTE_DISCOVERY = "I05_EXACT_BOUNDED_VIA_ACCEPTED_COMPOSITION"
EXT_ROUTE_RECURSIVE = "MX01R2_RECURSIVE_VIA_ACCEPTED_COMPOSITION"

EXTENSION_REFUSAL_STATES = frozenset(
    {REFUSAL_STATE_SLICE_NOT_SUPPORTED, REFUSAL_STATE_OWNER_ERROR}
)


class ProviderExtensionError(Pre553IntegrityError):
    """Typed extension-contract failure; owner errors are never laundered."""


def assert_extension_delegates_to_inherited_c1() -> None:
    """Fail closed unless this module actually calls the accepted owners.

    Structural self-check: the extension module source must reference the
    accepted provider function (direct route) and the accepted composition
    owner (discovery/recursive routes) by their exact qualified names, and the
    imported callables must be the accepted module members.
    """

    source = Path(__file__).read_text(encoding="utf-8")
    required = (
        "provide_empirical_possibility_slice(",
        "compose_positioned_subject_possibility(",
    )
    for needle in required:
        if needle not in source:
            raise ProviderExtensionError(
                f"EXTENSION_DELEGATION_CHECK_FAILED: missing call site {needle!r}"
            )
    if provide_empirical_possibility_slice.__module__ != (
        "rawlsing_next.pre553_empirical_possibility_provider"
    ):
        raise ProviderExtensionError(
            "EXTENSION_DELEGATION_CHECK_FAILED: direct provider is not the accepted owner"
        )
    if compose_positioned_subject_possibility.__module__ != (
        "rawlsing_next.pre553_analytical_composition"
    ):
        raise ProviderExtensionError(
            "EXTENSION_DELEGATION_CHECK_FAILED: composition is not the accepted owner"
        )


@dataclass(frozen=True)
class EmpiricalPossibilitySliceExtensionReceipt:
    """v1.1 receipt: accepted composition fields plus route/refs/coverage."""

    extension_contract_id: str
    producer_route: str
    provider_state: str
    producer_query_ref: ExactRef
    producer_predicate_ref: ExactRef
    producer_fact_ref: ExactRef
    producer_fact_state: str
    source_universe_refs: tuple[ExactRef, ...]
    release_refs: tuple[ExactRef, ...]
    consumer_query_ref: ExactRef
    consumer_binding_fingerprint: str
    condition_binding_witness_ref_or_hash: Any
    model_rule_hash: str
    generated_evidence_ref: ExactRef | None
    generated_evidence_identity_is_producer_derived: bool
    consumer_result_state: str | None
    consumer_result_identity_hash: str | None
    composed_result_identity_hash: str
    coverage_state: str
    joint_component_count: int
    joint_order_semantics: str
    discovery_receipt_refs: tuple[ExactRef, ...]
    discovery_frontier_ref: ExactRef | None
    recursive_handoff_refs: tuple[ExactRef, ...]
    recursive_lineage_refs: tuple[ExactRef, ...]
    base_receipt_ref_or_null: ExactRef | None
    refusal_state: str | None

    def material(self) -> Mapping[str, Any]:
        def refs(values: Iterable[ExactRef]) -> list[Any]:
            return [v.as_dict() for v in values]

        return {
            "schema": EXT_RECEIPT_SCHEMA,
            "extension_contract_id": self.extension_contract_id,
            "producer_route": self.producer_route,
            "provider_state": self.provider_state,
            "producer_query_ref": self.producer_query_ref.as_dict(),
            "producer_predicate_ref": self.producer_predicate_ref.as_dict(),
            "producer_fact_ref": self.producer_fact_ref.as_dict(),
            "producer_fact_state": self.producer_fact_state,
            "source_universe_refs": refs(self.source_universe_refs),
            "release_refs": refs(self.release_refs),
            "consumer_query_ref": self.consumer_query_ref.as_dict(),
            "consumer_binding_fingerprint": self.consumer_binding_fingerprint,
            "condition_binding_witness_ref_or_hash": _witness_material(
                self.condition_binding_witness_ref_or_hash
            ),
            "model_rule_hash": self.model_rule_hash,
            "generated_evidence_ref": (
                None
                if self.generated_evidence_ref is None
                else self.generated_evidence_ref.as_dict()
            ),
            "generated_evidence_identity_is_producer_derived": (
                self.generated_evidence_identity_is_producer_derived
            ),
            "consumer_result_state": self.consumer_result_state,
            "consumer_result_identity_hash": self.consumer_result_identity_hash,
            "composed_result_identity_hash": self.composed_result_identity_hash,
            "coverage_state": self.coverage_state,
            "joint_component_count": self.joint_component_count,
            "joint_order_semantics": self.joint_order_semantics,
            "discovery_receipt_refs": refs(self.discovery_receipt_refs),
            "discovery_frontier_ref": (
                None
                if self.discovery_frontier_ref is None
                else self.discovery_frontier_ref.as_dict()
            ),
            "recursive_handoff_refs": refs(self.recursive_handoff_refs),
            "recursive_lineage_refs": refs(self.recursive_lineage_refs),
            "base_receipt_ref_or_null": (
                None
                if self.base_receipt_ref_or_null is None
                else self.base_receipt_ref_or_null.as_dict()
            ),
            "refusal_state": self.refusal_state,
        }

    @property
    def receipt_hash(self) -> str:
        return semantic_hash(self.material())


def _witness_material(value: Any) -> Any:
    if value is None:
        return None
    as_dict = getattr(value, "as_dict", None)
    if callable(as_dict):
        return as_dict()
    if isinstance(value, str):
        return value
    digest = getattr(value, "content_hash", None)
    if isinstance(digest, str):
        return {"content_hash": digest}
    return canonical_scalar(value)


def canonical_scalar(value: Any) -> Any:
    from rawlsing_next.pre553_empirical_objects import canonicalize

    return canonicalize(value)


@dataclass(frozen=True)
class EmpiricalPossibilitySliceExtensionResult:
    """Extension output: exact generated slice + optional accepted base result."""

    provider_state: str
    producer_route: str
    extension_receipt: EmpiricalPossibilitySliceExtensionReceipt
    composition_result: AnalyticalCompositionResult
    generated_evidence_or_null: PossibilitySliceEvidence | None
    consumer_result_or_null: PositionedSubjectPossibilityResult | None
    base_result_or_null: EmpiricalPossibilitySliceProviderResult | None = None
    refusal_state: str | None = None
    refusal_reason: str | None = None
    refusal_owner_error_code: str | None = None

    def __post_init__(self) -> None:
        if self.provider_state == PROVIDER_STATE_EXACT:
            if self.refusal_state is not None:
                raise ProviderExtensionError("exact result may not carry refusal")
            if self.generated_evidence_or_null is None:
                raise ProviderExtensionError("exact result requires generated evidence")
            if self.consumer_result_or_null is None:
                raise ProviderExtensionError("exact result requires a consumer result")
            if self.generated_evidence_or_null is not (
                self.composition_result.possibility_slice_evidence_or_null
            ):
                raise ProviderExtensionError(
                    "exact result evidence must be the composition's generated evidence"
                )
            if self.consumer_result_or_null is not self.composition_result.consumer_result_or_null:
                raise ProviderExtensionError(
                    "exact result consumer must be the composition's consumer result"
                )
        else:
            if self.provider_state != PROVIDER_STATE_REFUSED:
                raise ProviderExtensionError(f"unexpected provider state {self.provider_state!r}")
            if self.refusal_state not in EXTENSION_REFUSAL_STATES:
                raise ProviderExtensionError("refusal requires a governed refusal state")
            if self.generated_evidence_or_null is not None:
                raise ProviderExtensionError("refusal may not carry evidence")
            if self.consumer_result_or_null is not None:
                raise ProviderExtensionError("refusal may not carry a consumer result")

    def material(self) -> Mapping[str, Any]:
        return {
            "provider_state": self.provider_state,
            "producer_route": self.producer_route,
            "extension_receipt": self.extension_receipt.material(),
            "base_result_identity_hash_or_null": (
                None if self.base_result_or_null is None else self.base_result_or_null.result_identity_hash
            ),
            "generated_evidence_ref_or_null": (
                None
                if self.generated_evidence_or_null is None
                else self.generated_evidence_or_null.evidence_ref.as_dict()
            ),
            "consumer_result_identity_hash_or_null": (
                None if self.consumer_result_or_null is None else self.consumer_result_or_null.result_hash
            ),
            "refusal_state_or_null": self.refusal_state,
            "refusal_reason_or_null": self.refusal_reason,
            "refusal_owner_error_code_or_null": self.refusal_owner_error_code,
        }

    @property
    def result_identity_hash(self) -> str:
        return semantic_hash(self.material())


def _build_extension_receipt(
    *,
    composition: AnalyticalCompositionResult,
    model_rule: PositionedSubjectPossibilityModelRule,
    evidence: PossibilitySliceEvidence | None,
    consumer_result: PositionedSubjectPossibilityResult | None,
    provider_state: str,
    refusal_state: str | None,
    base_receipt_ref_or_null: ExactRef | None,
    producer_route: str,
) -> EmpiricalPossibilitySliceExtensionReceipt:
    return EmpiricalPossibilitySliceExtensionReceipt(
        extension_contract_id=EXT_CONTRACT_ID,
        producer_route=producer_route,
        provider_state=provider_state,
        producer_query_ref=composition.producer_query_ref,
        producer_predicate_ref=composition.producer_predicate_ref,
        producer_fact_ref=composition.producer_fact_ref,
        producer_fact_state=composition.producer_fact_state,
        source_universe_refs=tuple(composition.source_universe_refs),
        release_refs=tuple(composition.release_refs),
        consumer_query_ref=composition.consumer_query_ref,
        consumer_binding_fingerprint=composition.consumer_binding_fingerprint,
        condition_binding_witness_ref_or_hash=composition.condition_binding_witness_ref_or_hash,
        model_rule_hash=model_rule.rule_hash,
        generated_evidence_ref=(None if evidence is None else evidence.evidence_ref),
        generated_evidence_identity_is_producer_derived=(
            evidence is not None and evidence is composition.possibility_slice_evidence_or_null
        ),
        consumer_result_state=(None if consumer_result is None else consumer_result.result_state),
        consumer_result_identity_hash=(
            None if consumer_result is None else consumer_result.result_hash
        ),
        composed_result_identity_hash=composition.composed_result_identity_hash,
        coverage_state=composition.coverage_state,
        joint_component_count=composition.joint_component_count,
        joint_order_semantics=composition.joint_order_semantics,
        discovery_receipt_refs=tuple(composition.discovery_receipt_refs),
        discovery_frontier_ref=composition.discovery_frontier_ref,
        recursive_handoff_refs=tuple(composition.recursive_handoff_refs),
        recursive_lineage_refs=tuple(composition.recursive_lineage_refs),
        base_receipt_ref_or_null=base_receipt_ref_or_null,
        refusal_state=refusal_state,
    )


def provide_empirical_possibility_slice_ext(
    *,
    repository: Any,
    empirical_query: Any,
    predicate: Any,
    authority_registry: Any,
    release_refs: Iterable[ExactRef],
    consumer_query: PositionedSubjectPossibilityQuery,
    model_rule: PositionedSubjectPossibilityModelRule,
    condition_binding_witness: Any,
    discovery_result: Any = None,
    discovery_receipt_ref: ExactRef | None = None,
    recursive_handoff: Any = None,
) -> EmpiricalPossibilitySliceExtensionResult:
    """Produce one governed slice through the accepted owners, v1.1 receipt.

    * direct route (no discovery/recursive material): delegates verbatim to the
      accepted ``provide_empirical_possibility_slice`` and re-wraps its result;
    * discovery/recursive routes: calls the accepted composition owner with the
      exact caller-supplied discovery result/receipt/handoff.
    """

    assert_extension_delegates_to_inherited_c1()

    if discovery_result is not None or recursive_handoff is not None:
        if discovery_result is None and discovery_receipt_ref is not None:
            raise ProviderExtensionError(
                "EXTENSION_REQUEST_SHAPE_ERROR: discovery receipt without discovery result"
            )
        if discovery_result is not None and discovery_receipt_ref is None:
            raise ProviderExtensionError(
                "EXTENSION_REQUEST_SHAPE_ERROR: discovery result requires its exact receipt ref"
            )
        composition = compose_positioned_subject_possibility(
            repository=repository,
            empirical_query=empirical_query,
            predicate=predicate,
            authority_registry=authority_registry,
            release_refs=tuple(release_refs),
            consumer_query=consumer_query,
            model_rule=model_rule,
            condition_binding_witness=condition_binding_witness,
            discovery_result=discovery_result,
            discovery_receipt_ref=discovery_receipt_ref,
            recursive_handoff=recursive_handoff,
        )
        producer_route = (
            EXT_ROUTE_RECURSIVE if recursive_handoff is not None else EXT_ROUTE_DISCOVERY
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
            receipt = _build_extension_receipt(
                composition=composition,
                model_rule=model_rule,
                evidence=None,
                consumer_result=None,
                provider_state=PROVIDER_STATE_REFUSED,
                refusal_state=refusal_state,
                base_receipt_ref_or_null=None,
                producer_route=producer_route,
            )
            return EmpiricalPossibilitySliceExtensionResult(
                provider_state=PROVIDER_STATE_REFUSED,
                producer_route=producer_route,
                extension_receipt=receipt,
                composition_result=composition,
                generated_evidence_or_null=None,
                consumer_result_or_null=None,
                refusal_state=refusal_state,
                refusal_reason=(
                    f"producer fact typed_state={state!r} produced no exact supported "
                    "slice; the extension creates no smoothing, proxy or invented geometry"
                ),
                refusal_owner_error_code=state,
            )
        receipt = _build_extension_receipt(
            composition=composition,
            model_rule=model_rule,
            evidence=evidence,
            consumer_result=consumer_result,
            provider_state=PROVIDER_STATE_EXACT,
            refusal_state=None,
            base_receipt_ref_or_null=None,
            producer_route=producer_route,
        )
        return EmpiricalPossibilitySliceExtensionResult(
            provider_state=PROVIDER_STATE_EXACT,
            producer_route=producer_route,
            extension_receipt=receipt,
            composition_result=composition,
            generated_evidence_or_null=evidence,
            consumer_result_or_null=consumer_result,
        )

    if len(consumer_query.conditioner_bindings) != 1:
        composition = compose_positioned_subject_possibility(
            repository=repository,
            empirical_query=empirical_query,
            predicate=predicate,
            authority_registry=authority_registry,
            release_refs=tuple(release_refs),
            consumer_query=consumer_query,
            model_rule=model_rule,
            condition_binding_witness=condition_binding_witness,
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
            receipt = _build_extension_receipt(
                composition=composition,
                model_rule=model_rule,
                evidence=None,
                consumer_result=None,
                provider_state=PROVIDER_STATE_REFUSED,
                refusal_state=refusal_state,
                base_receipt_ref_or_null=None,
                producer_route=EXT_ROUTE_DIRECT_MULTI_CONDITIONER,
            )
            return EmpiricalPossibilitySliceExtensionResult(
                provider_state=PROVIDER_STATE_REFUSED,
                producer_route=EXT_ROUTE_DIRECT_MULTI_CONDITIONER,
                extension_receipt=receipt,
                composition_result=composition,
                generated_evidence_or_null=None,
                consumer_result_or_null=None,
                refusal_state=refusal_state,
                refusal_reason=(
                    f"producer fact typed_state={state!r} produced no exact supported "
                    "slice for the multi-conditioner request"
                ),
                refusal_owner_error_code=state,
            )
        receipt = _build_extension_receipt(
            composition=composition,
            model_rule=model_rule,
            evidence=evidence,
            consumer_result=consumer_result,
            provider_state=PROVIDER_STATE_EXACT,
            refusal_state=None,
            base_receipt_ref_or_null=None,
            producer_route=EXT_ROUTE_DIRECT_MULTI_CONDITIONER,
        )
        return EmpiricalPossibilitySliceExtensionResult(
            provider_state=PROVIDER_STATE_EXACT,
            producer_route=EXT_ROUTE_DIRECT_MULTI_CONDITIONER,
            extension_receipt=receipt,
            composition_result=composition,
            generated_evidence_or_null=evidence,
            consumer_result_or_null=consumer_result,
        )

    base = provide_empirical_possibility_slice(
        repository=repository,
        empirical_query=empirical_query,
        predicate=predicate,
        authority_registry=authority_registry,
        release_refs=tuple(release_refs),
        consumer_query=consumer_query,
        model_rule=model_rule,
        condition_binding_witness=condition_binding_witness,
    )
    composition = base.composition_result
    receipt = _build_extension_receipt(
        composition=composition,
        model_rule=model_rule,
        evidence=base.generated_evidence_or_null,
        consumer_result=base.consumer_result_or_null,
        provider_state=base.provider_state,
        refusal_state=base.refusal_state,
        base_receipt_ref_or_null=base.provider_receipt.receipt_ref,
        producer_route=EXT_ROUTE_DIRECT_VIA_ACCEPTED_PROVIDER,
    )
    return EmpiricalPossibilitySliceExtensionResult(
        provider_state=base.provider_state,
        producer_route=EXT_ROUTE_DIRECT_VIA_ACCEPTED_PROVIDER,
        extension_receipt=receipt,
        composition_result=composition,
        generated_evidence_or_null=base.generated_evidence_or_null,
        consumer_result_or_null=base.consumer_result_or_null,
        base_result_or_null=base,
        refusal_state=base.refusal_state,
        refusal_reason=base.refusal_reason,
        refusal_owner_error_code=base.refusal_owner_error_code,
    )


def replay_extension_slice(expected: EmpiricalPossibilitySliceExtensionResult, **kwargs: Any) -> EmpiricalPossibilitySliceExtensionResult:
    """Deterministic replay check: same frozen determinants -> same identities."""

    replayed = provide_empirical_possibility_slice_ext(**kwargs)
    if (
        replayed.result_identity_hash != expected.result_identity_hash
        or replayed.material() != expected.material()
    ):
        raise ProviderExtensionError(
            "N10E provider extension replay mismatch: deterministic identity not reproduced"
        )
    return replayed


__all__ = [
    "EXT_CONTRACT_ID",
    "EXT_RECEIPT_SCHEMA",
    "EXT_ROUTE_DIRECT_VIA_ACCEPTED_PROVIDER",
    "EXT_ROUTE_DIRECT_MULTI_CONDITIONER",
    "EXT_ROUTE_DISCOVERY",
    "EXT_ROUTE_RECURSIVE",
    "EXTENSION_REFUSAL_STATES",
    "ProviderExtensionError",
    "EmpiricalPossibilitySliceExtensionReceipt",
    "EmpiricalPossibilitySliceExtensionResult",
    "assert_extension_delegates_to_inherited_c1",
    "provide_empirical_possibility_slice_ext",
    "replay_extension_slice",
]
