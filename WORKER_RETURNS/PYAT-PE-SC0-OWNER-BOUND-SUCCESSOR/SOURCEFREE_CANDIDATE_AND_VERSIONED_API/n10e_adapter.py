"""Explicit adapter from the actual N10E provider to ProducerEvidence."""
from __future__ import annotations

import copy
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_possibility_provider import (
    PROVIDER_STATE_EXACT,
    provide_empirical_possibility_slice,
)
from owner_bound_successor import (
    N10E_CONTRACT_ID,
    ProducerEvidence,
    ROLE_FORWARD,
    ROLE_REVERSE,
)


class N10EProducer:
    def __init__(self, *, case: Mapping[str, Any]) -> None:
        self.case = case
        direction = case.get("direction")
        if direction == "forward":
            role = ROLE_FORWARD
        elif direction == "reverse":
            role = ROLE_REVERSE
        else:
            raise ValueError(f"unsupported N10E fixture direction: {direction!r}")
        self.role_direction = role

    def produce(self) -> ProducerEvidence:
        case = self.case
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
            raise RuntimeError(
                f"N10E producer refused: {result.provider_state} {result.refusal_state}"
            )
        receipt = result.provider_receipt
        evidence = result.generated_evidence_or_null
        consumer = result.consumer_result_or_null
        if evidence is None or consumer is None:
            raise RuntimeError("N10E exact result lacks generated evidence or consumer")
        geometry = evidence.geometry
        denominator = geometry["denominator"]["raw_denominator_support"]
        consumer_query = case["consumer_query"]
        binding = consumer_query.conditioner_bindings[0]
        release_ref = case["release_refs"][0]
        return ProducerEvidence(
            provider_contract_id=N10E_CONTRACT_ID,
            provider_state=result.provider_state,
            producer_receipt_ref=receipt.receipt_ref,
            producer_query_ref=receipt.producer_query_ref,
            producer_fact_ref=receipt.producer_fact_ref,
            consumer_query_ref=receipt.consumer_query_ref,
            consumer_result_state=consumer.result_state,
            consumer_result_identity_hash=consumer.result_hash,
            role_direction=self.role_direction,
            target_ref=consumer_query.target_ref,
            risk_set_ref=case["empirical_query"].risk_set_ref,
            conditioner_coordinate_ref=binding.empirical_coordinate_ref,
            source_universe_ref=consumer_query.source_universe_ref,
            release_ref=release_ref,
            model_rule_hash=case["model_rule"].rule_hash,
            cells=tuple(copy.deepcopy(cell) for cell in geometry["cells"]),
            denominator=denominator,
        )


__all__ = ["N10EProducer"]
