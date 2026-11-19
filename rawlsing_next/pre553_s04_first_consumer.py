"""Single I03 execution -> reusable S04 -> optional existing FF01 first consumer.

The *new intended path* consumes S04 rather than independently calculating
FF01 from I03. The accepted direct FF01 compatibility function remains
untouched. No second native I03, respondent corpus, scientific rank or actor.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from typing import Any, Iterable, Sequence

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalPredicate, EmpiricalQuerySpec, ExactRef, canonical_json,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_s04_ff01_consumer import receive_ff01_from_s04
from rawlsing_next.pre553_s04_observed_research import (
    S04ObservedKnowledge, receive_s04_i03_research,
)
from rawlsing_next.pre553_s04_research_batch import (
    S04BatchReceipt, S04ContextRequest, run_s04_context_batch,
)
from rawlsing_next.field_forge_generic_empirical_ingress import FF01ObservedJoint

CONTRACT = "S04_SINGLE_I03_FIRST_CONSUMER@1.0.0"
GRADE = "EXACT_SOURCEFREE_OBSERVED_FIRST_CONSUMER__NO_NEW_SOURCE_RIGHTS"


class S04OnePassError(ValueError):
    """A research or consumer boundary is incomplete or falsely promoted."""


@dataclass(frozen=True)
class S04OnePassReceipt:
    payload_json: str
    digest: str

    def __post_init__(self) -> None:
        content = loads(self.payload_json)
        if (type(content) is not dict or content.get("contract") != CONTRACT
                or canonical_json(content) != self.payload_json
                or semantic_hash(content) != self.digest):
            raise S04OnePassError("one-pass S04 receipt is not exact hash-valid")

    @property
    def ref(self) -> ExactRef:
        return ExactRef(CONTRACT, f"urn:rawlsing:s04:first-consumer:sha256:{self.digest}", self.digest)

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


@dataclass(frozen=True)
class S04OnePassResult:
    execution: QueryExecutionResult
    knowledge: S04ObservedKnowledge
    ff01: FF01ObservedJoint | None
    batch: S04BatchReceipt | None
    receipt: S04OnePassReceipt


def receive_s04_first_consumer(
    *,
    query: EmpiricalQuerySpec,
    execution: QueryExecutionResult,
    conditioner_index: int | None = None,
    producer_permission_ceiling: tuple[str, ...] = ("FF01_DESCRIPTIVE_SOURCEFREE",),
    context_requests: Sequence[S04ContextRequest] = (),
) -> S04OnePassResult:
    """One *existing* original I03 aggregate, S04 then consumer.

    Unary native I03 is lawful S04/F1 even though there is no k>=2 FF01
    relation to issue. To create FF01, select an actual conditioner index.
    """
    if type(query) is not EmpiricalQuerySpec or type(execution) is not QueryExecutionResult:
        raise S04OnePassError("original exact native I03 query and result required")
    knowledge = receive_s04_i03_research(query=query, execution=execution)
    downstream = None
    if conditioner_index is not None:
        downstream = receive_ff01_from_s04(
            knowledge=knowledge, query=query, execution=execution,
            conditioner_index=conditioner_index,
            producer_permission_ceiling=producer_permission_ceiling,
        )
    batch = None
    if context_requests:
        batch, _ = run_s04_context_batch(
            knowledge=knowledge, requests=context_requests,
        )
    if downstream is not None and batch is not None:
        consumer_status = "S04_TO_FF01_WITH_CONTEXT_BATCH"
    elif downstream is not None:
        consumer_status = "S04_TO_FF01_FIRST_CONSUMER"
    elif batch is not None:
        consumer_status = "S04_CONTEXT_BATCH_ONLY"
    else:
        # S04 itself is a valid unary F1 product without mandatory FF01.
        consumer_status = "UPSTREAM_S04_ONLY"
    material = knowledge.material()
    payload = {
        "contract": CONTRACT,
        "grade": GRADE,
        "consumer_status": consumer_status,
        "producer_operation": "ONE_PREEXISTING_I03_RESULT__NO_ADDITIONAL_QUERY",
        "source_query_ref": query.ref.as_dict(),
        "source_fact_ref": execution.facts[0].ref.as_dict(),
        "source_release_ref": material["release_ref"],
        "source_risk_set_ref": material["risk_set_ref"],
        "s04_knowledge_ref": knowledge.ref.as_dict(),
        "s04_typed_state": material["state"],
        "ff01_consumer_ref": downstream.ref.as_dict() if downstream else None,
        "batch_research_ref": batch.ref.as_dict() if batch else None,
        "FF02_structural_authority": None,
        "population_rank_or_uncertainty": None,
        "N10E_actor_authority": None,
        "not_issued": [
            "SOURCEFREE_ORIGINAL_SOURCE_USE_NOT_REVALIDATED_HERE",
            "S05_LEARNED_PUBLICATION_INDEPENDENT",
            "SCIENTIFIC_DETERMINICITY_RANK_AND_ADAPTIVE_MINORITY_METHOD_HELD",
            "NO_REPEATED_I03_OR_C11_READ_IN_THIS_ADAPTER",
        ],
    }
    receipt = S04OnePassReceipt(canonical_json(payload), semantic_hash(payload))
    return S04OnePassResult(execution, knowledge, downstream, batch, receipt)


def execute_s04_first_consumer_once(
    *,
    repository: Any,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    authority_registry: Any,
    release_refs: Iterable[ExactRef],
    conditioner_index: int | None = None,
    producer_permission_ceiling: tuple[str, ...] = ("FF01_DESCRIPTIVE_SOURCEFREE",),
    context_requests: Sequence[S04ContextRequest] = (),
) -> S04OnePassResult:
    """Call THE EXISTING I03 owner exactly once, then replay no source."""
    if type(query) is not EmpiricalQuerySpec or type(predicate) is not EmpiricalPredicate:
        raise S04OnePassError("exact C11 query/predicate required")
    original = execute_empirical_query(
        repository=repository, query=query, predicate=predicate,
        authority_registry=authority_registry, release_refs=tuple(release_refs),
    )
    return receive_s04_first_consumer(
        query=query, execution=original, conditioner_index=conditioner_index,
        producer_permission_ceiling=producer_permission_ceiling,
        context_requests=context_requests,
    )


__all__ = [
    "CONTRACT", "S04OnePassError", "S04OnePassReceipt", "S04OnePassResult",
    "receive_s04_first_consumer", "execute_s04_first_consumer_once",
]
