"""Re-query many contextual hypotheses against ONE existing S04 knowledge fact.

No second I03, C11 query, estimator, FF bridge, respondent materialization,
or data-adaptive discovery. Duplicate requests share an exact answer receipt;
novel conditions still use the canonical S04 F1/F2 implementation. The batch
report is a deterministic audit of requests and outputs, not a scientific rank.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    ExactRef, canonical_json, canonicalize, semantic_hash,
)
from rawlsing_next.pre553_s04_observed_research import (
    S04ObservedKnowledge, S04ResearchAnswer, ask_s04_exact_condition,
)

CONTRACT = "S04_ONE_JOINT_CONTEXT_BATCH_R1"
MAX_REQUESTS = 100
GRADE = "ONE_SOURCE_JOINT__EXACT_OBSERVED_SAMPLE__NOT_PREDICTIVE_MODEL"


class S04BatchError(ValueError):
    """Batch would lose exact source scope, ordering, science or budget."""


@dataclass(frozen=True)
class S04ContextRequest:
    target_index: int
    conditions: Mapping[int, Any]


@dataclass(frozen=True)
class S04BatchReceipt:
    payload_json: str
    digest: str

    def __post_init__(self) -> None:
        material = loads(self.payload_json)
        if (type(material) is not dict
                or canonical_json(material) != self.payload_json
                or material.get("contract") != CONTRACT
                or semantic_hash(material) != self.digest):
            raise S04BatchError("noncanonical or mismatched S04 batch receipt")

    @property
    def ref(self) -> ExactRef:
        return ExactRef(CONTRACT, f"urn:rawlsing:s04:batch:sha256:{self.digest}", self.digest)

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


def run_s04_context_batch(
    *,
    knowledge: S04ObservedKnowledge,
    requests: Sequence[S04ContextRequest],
) -> tuple[S04BatchReceipt, tuple[S04ResearchAnswer, ...]]:
    """Conserve each ordered request; memoize *exact* duplicate conditions.

    Unlike I05, this routine does NOT select or expand candidate hypotheses:
    all targets/conditions must have been explicitly supplied by the caller.
    """
    if type(knowledge) is not S04ObservedKnowledge:
        raise S04BatchError("exact original S04 research fact required")
    if isinstance(requests, (str, bytes)) or not isinstance(requests, (list, tuple)):
        raise S04BatchError("ordered S04 request list required")
    if not 1 <= len(requests) <= MAX_REQUESTS:
        raise S04BatchError("bounded batch must contain 1–100 requests")
    origin = knowledge.material()
    if origin.get("contract") != "S04_SOURCE_EXACT_OBSERVED_KNOWLEDGE@1.0.0":
        raise S04BatchError("unsupported source knowledge family")

    lookup: dict[str, S04ResearchAnswer] = {}
    ordered: list[S04ResearchAnswer] = []
    audit: list[dict[str, Any]] = []
    for position, request in enumerate(requests):
        if type(request) is not S04ContextRequest or type(request.target_index) is not int:
            raise S04BatchError("only exact typed S04 targets admitted")
        if not isinstance(request.conditions, Mapping):
            raise S04BatchError("condition selections must be a mapping")
        if any(type(index) is not int for index in request.conditions):
            raise S04BatchError("condition axis must be exact integer, not bool or string")
        # Use JSON content keys, NOT Python repr or object address. Request
        # order and exact condition values remain visible in the receipt.
        selector = {
            "target_index": request.target_index,
            "conditions": [
                {"index": index, "state": canonicalize(value)}
                for index, value in sorted(request.conditions.items())
            ],
        }
        key = canonical_json(selector)
        if key not in lookup:
            lookup[key] = ask_s04_exact_condition(
                knowledge=knowledge, target_index=request.target_index,
                conditions=request.conditions,
            )
        answer = lookup[key]
        result = answer.material()
        if (result.get("knowledge_ref") != knowledge.ref.as_dict()
                or result.get("source_fact_ref") != origin["fact_ref"]
                or result.get("source_release_ref") != origin["release_ref"]
                or result.get("risk_set_ref") != origin["risk_set_ref"]):
            raise S04BatchError("conditional answer escaped common source/risk/current state")
        ordered.append(answer)
        audit.append({
            "request_position": position,
            "selection": selector,
            "research_answer_ref": answer.ref.as_dict(),
            "answer_state": result["state"],
            "condition_fully_resolved_n": result["raw_conditioned_full_case_n"],
            "cache_reused": position > 0 and any(
                prior["selection"] == selector for prior in audit
            ),
        })
    payload = {
        "contract": CONTRACT,
        "grade": GRADE,
        "source_s04_ref": knowledge.ref.as_dict(),
        "source_query_ref": origin["query_ref"],
        "source_fact_ref": origin["fact_ref"],
        "source_release_ref": origin["release_ref"],
        "source_risk_set_ref": origin["risk_set_ref"],
        "source_measure_basis_ref": origin["measure_basis_ref"],
        "source_authentication_grade": origin["source_authenticity"],
        "batch_issuer_authority": "NOT_ISSUED__REQUIRES_ORIGINAL_I03_OR_SEPARATE_PIN",
        "raw_source_risk_eligible_n": origin["raw_eligible_condition_denominator"],
        "raw_full_joint_resolved_n": origin["raw_fully_resolved_joint_n"],
        "raw_unresolved_joint_eligible_n": (
            origin["raw_eligible_condition_denominator"]
            - origin["raw_fully_resolved_joint_n"]
        ),
        "unresolved_cause_grade": "NOT_DECOMPOSABLE_BY_ROUTING_OR_NONRESPONSE_FROM_I03_AGGREGATE",
        "requests_total": len(requests),
        "distinct_contextual_computations": len(lookup),
        "reused_exact_requests": len(requests) - len(lookup),
        "ordered_research": audit,
        "scientific_rank": None,
        "new_population_claim": None,
        "no_source_requery": True,
        "limitation": [
            "CONDITIONS_SUPPLIED_BY_CALLER_NOT_ADAPTIVELY_DISCOVERED",
            "SAMPLE_EXACT_RAW_NOT_ORIGINAL_SOURCE_AUTHORIZATION",
            "COMPARATIVE_PREDICTOR_METRIC_UNCERTAINTY_POSTSELECTION_UNISSUED",
            "NO_CAUSAL_FF02_ACTOR_V3_PROMOTION",
        ],
    }
    digest = semantic_hash(payload)
    return S04BatchReceipt(canonical_json(payload), digest), tuple(ordered)


__all__ = [
    "CONTRACT", "MAX_REQUESTS", "S04BatchError", "S04ContextRequest",
    "S04BatchReceipt", "run_s04_context_batch",
]
