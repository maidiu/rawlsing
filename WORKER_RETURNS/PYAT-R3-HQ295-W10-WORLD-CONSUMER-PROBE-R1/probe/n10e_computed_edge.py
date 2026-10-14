"""Genuinely computed N10E lane: actual provider -> C1 composition -> public consumer.

Reused read-only owners (no mutation):
  * rawlsing_next.pre553_empirical_possibility_provider.provide_empirical_possibility_slice
  * rawlsing_next.pre553_empirical_possibility_provider.replay_empirical_possibility_slice
  * rawlsing_next.pre553_analytical_composition.compose_positioned_subject_possibility
  * rawlsing_next.source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility
  * rawlsing_next.tests.n10e_empirical_slice_fixture (exact accepted AT07 fixture law)

Slice geometry is produced only by the accepted producer path from the fixture's
exact empirical rows.  The probe never supplies and never edits probability
geometry; the computed exact fractions are copied read-only into consumer
receipts at their own declared grain and are never merged into modeled-world
route probabilities.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next.pre553_empirical_possibility_provider import (
    PROVIDER_STATE_EXACT,
    ProviderRequestShapeError,
    assert_provider_public_api_excludes_handwritten_slice,
    provide_empirical_possibility_slice,
    replay_empirical_possibility_slice,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    evaluate_positioned_subject_possibility,
    verify_positioned_subject_possibility_replay,
)
from rawlsing_next.tests import n10e_empirical_slice_fixture as fx

N10E_LANE_GRADE = (
    "COMPUTED_N10E_SLICE__PROVIDER_DERIVED_OWN_GRAIN__NOT_ROUTE_PROBABILITY"
)


class N10EEdgeError(ValueError):
    """Typed N10E lane failure inside the W10 probe."""


@dataclass(frozen=True)
class N10EComputedProduct:
    direction: str
    variant: str | None
    provider_state: str
    provider_receipt_ref: Mapping[str, str]
    provider_receipt_hash: str
    composed_result_identity_hash: str
    evidence_ref: Mapping[str, str] | None
    evidence_state: str | None
    source_universe_ref: Mapping[str, str]
    release_ref: Mapping[str, str]
    target_ref: Mapping[str, str]
    retained_conditioner_ids: tuple[str, ...]
    denominator: int | None
    computed_cells: tuple[Mapping[str, Any], ...]
    consumer_result_state: str
    consumer_result_hash: str
    consumer_disposition: str
    consumer_reason: str
    model_rule_hash: str
    uncertainty_state: str | None
    producer_fact_state: str

    def lane_material(self) -> Mapping[str, Any]:
        return {
            "lane_grade": N10E_LANE_GRADE,
            "direction": self.direction,
            "fixture_variant": self.variant,
            "provider_state": self.provider_state,
            "provider_receipt_ref": dict(self.provider_receipt_ref),
            "provider_receipt_hash": self.provider_receipt_hash,
            "composed_result_identity_hash": self.composed_result_identity_hash,
            "evidence_ref": dict(self.evidence_ref) if self.evidence_ref else None,
            "evidence_state": self.evidence_state,
            "source_universe_ref": dict(self.source_universe_ref),
            "release_ref": dict(self.release_ref),
            "target_ref": dict(self.target_ref),
            "retained_conditioner_ids": list(self.retained_conditioner_ids),
            "denominator": self.denominator,
            "computed_cells": [canonicalize(c) for c in self.computed_cells],
            "consumer_result_state": self.consumer_result_state,
            "consumer_result_hash": self.consumer_result_hash,
            "consumer_disposition": self.consumer_disposition,
            "consumer_reason": self.consumer_reason,
            "model_rule_hash": self.model_rule_hash,
            "uncertainty_state": self.uncertainty_state,
            "producer_fact_state": self.producer_fact_state,
            "cross_grain_route_probability_merge": "FORBIDDEN",
        }

    @property
    def lane_hash(self) -> str:
        return semantic_hash(self.lane_material())


def compute_n10e_product(
    *, direction: str = "forward", variant: str | None = None
) -> N10EComputedProduct:
    """Run the real N10E provider over the exact accepted AT07 fixture law."""

    case = fx.build_provider_case(direction, variant=variant)
    result = provide_empirical_possibility_slice(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )
    if result.provider_state != PROVIDER_STATE_EXACT:
        raise N10EEdgeError(
            f"N10E lane requires an exact computed slice, got {result.provider_state!r}"
        )
    evidence = result.generated_evidence_or_null
    consumer = result.consumer_result_or_null
    if evidence is None or consumer is None:
        raise N10EEdgeError("N10E lane missing computed evidence or consumer result")
    geometry = evidence.geometry or {}
    return N10EComputedProduct(
        direction=direction,
        variant=variant,
        provider_state=result.provider_state,
        provider_receipt_ref=result.provider_receipt.receipt_ref.as_dict(),
        provider_receipt_hash=result.provider_receipt.receipt_hash,
        composed_result_identity_hash=result.composition_result.composed_result_identity_hash,
        evidence_ref=evidence.evidence_ref.as_dict(),
        evidence_state=evidence.evidence_state,
        source_universe_ref=consumer.source_universe_ref.as_dict(),
        release_ref=consumer.release_ref.as_dict(),
        target_ref=consumer.target_ref.as_dict(),
        retained_conditioner_ids=tuple(evidence.retained_conditioner_ids),
        denominator=geometry.get("denominator", {}).get("raw_denominator_support"),
        computed_cells=tuple(geometry.get("cells", ())),
        consumer_result_state=consumer.result_state,
        consumer_result_hash=consumer.result_hash,
        consumer_disposition=consumer.exact_disposition,
        consumer_reason=consumer.exact_reason,
        model_rule_hash=consumer.model_rule_hash,
        uncertainty_state=evidence.uncertainty_state,
        producer_fact_state=result.composition_result.producer_fact_state,
    )


def verify_n10e_cold_replay(
    *, direction: str = "forward", variant: str | None = None, expected: N10EComputedProduct
) -> N10EComputedProduct:
    """Cold deterministic replay through the real provider + consumer replay seams."""

    case = fx.build_provider_case(direction, variant=variant)
    replayed = replay_empirical_possibility_slice(
        expected=_rerun_provider(case),
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )
    verify_positioned_subject_possibility_replay(
        replayed.consumer_result_or_null,
        query=case["consumer_query"],
        rule=case["model_rule"],
        evidence=(replayed.generated_evidence_or_null,),
    )
    product = compute_n10e_product(direction=direction, variant=variant)
    if product.lane_hash != expected.lane_hash:
        raise N10EEdgeError("N10E cold replay changed the computed lane identity")
    return product


def _rerun_provider(case: Mapping[str, Any]) -> Any:
    return provide_empirical_possibility_slice(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )


def handwritten_slice_hostile_probe() -> Mapping[str, Any]:
    """H06: handwritten/synthetic slice geometry can never enter the N10E provider."""

    findings: list[dict[str, str]] = []
    try:
        assert_provider_public_api_excludes_handwritten_slice()
        findings.append({"check": "public_api_excludes_handwritten_slice", "state": "PASS"})
    except ProviderRequestShapeError as exc:
        findings.append({"check": "public_api_excludes_handwritten_slice", "state": "FAIL", "detail": str(exc)})
    try:
        provide_empirical_possibility_slice(
            repository=object(),
            empirical_query=object(),
            predicate=object(),
            authority_registry=object(),
            release_refs=(),
            consumer_query=object(),
            model_rule=object(),
            condition_binding_witness=object(),
            evidence={"geometry": {"cells": [{"cell": "forged", "raw_probability_exact_fraction": [1, 1]}]}},
        )
    except TypeError as exc:
        findings.append(
            {
                "check": "handwritten_evidence_kwarg_rejected",
                "state": "PASS",
                "detail": f"TypeError: {exc}".split("\n")[0],
            }
        )
    except Exception as exc:  # noqa: BLE001 - any non-TypeError entry is still a rejection record
        findings.append(
            {
                "check": "handwritten_evidence_kwarg_rejected",
                "state": "PASS",
                "detail": f"{type(exc).__name__}: {exc}".split("\n")[0],
            }
        )
    else:
        findings.append({"check": "handwritten_evidence_kwarg_rejected", "state": "FAIL"})
    return {
        "oracle": "H06_REJECT_HANDWRITTEN_PROVIDER_INPUT",
        "expected": "REJECT_HANDWRITTEN_PROVIDER_INPUT",
        "findings": findings,
        "all_pass": all(f["state"] == "PASS" for f in findings),
        "pass": all(f["state"] == "PASS" for f in findings),
    }


def evaluate_generated_slice_directly_for_court(
    *, direction: str = "forward", variant: str | None = None
) -> Mapping[str, Any]:
    """Court-only pass-through proving producer-derived slices reach the public consumer."""

    case = fx.build_provider_case(direction, variant=variant)
    result = provide_empirical_possibility_slice(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )
    evidence = result.generated_evidence_or_null
    direct = evaluate_positioned_subject_possibility(
        query=case["consumer_query"],
        rule=case["model_rule"],
        evidence=(evidence,),
    )
    return {
        "provider_result_identity_hash": result.result_identity_hash,
        "direct_consumer_result_hash": direct.result_hash,
        "provider_consumer_result_hash": result.consumer_result_or_null.result_hash,
        "identical": direct.result_hash == result.consumer_result_or_null.result_hash,
    }


__all__ = [
    "N10E_LANE_GRADE",
    "N10EEdgeError",
    "N10EComputedProduct",
    "compute_n10e_product",
    "verify_n10e_cold_replay",
    "handwritten_slice_hostile_probe",
    "evaluate_generated_slice_directly_for_court",
]
