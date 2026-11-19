"""One native saved-C11 session -> DISTINCT I03 -> S04 -> optional FF01.

This composes the accepted existing I03 evaluator with the #1153
sourcefree one-postings-preparation adapter and existing S04-first consumer.
It does not introduce a C11 engine, choose a scientific estimator, import
ANVIL construction-only source grants into analytical authority, or certify
full 100k/6GiB economics.

Batch identity is deterministic; elapsed wall clock and RSS are deliberately
excluded from semantic receipts. Local economics are measured separately.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from typing import Any, Sequence

from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
from rawlsing_next.pre553_distinct_cold_i03_batch import (
    ColdI03BatchResult, ColdI03Operation, ColdI03BatchError,
    execute_distinct_native_cold_i03, MAX_DISTINCT,
)
from rawlsing_next.pre553_empirical_objects import (
    ExactRef, canonical_json, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_s04_first_consumer import (
    S04OnePassResult, receive_s04_first_consumer,
)
from rawlsing_next.pre553_s04_research_batch import S04ContextRequest
from rawlsing_next.field_forge_generic_empirical_ingress import _permission_set
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate

CONTRACT = "S04_DISTINCT_SAVED_I03_RESEARCH_BATCH@1.0.0"
GRADE = "SOURCEFREE_ONE_NATIVE_PREPARATION__S04_RESEARCH_FIRST__FF01_OPTIONAL"
FF01_DESCRIPTIVE = ("FF01_DESCRIPTIVE_SOURCEFREE",)


class S04DistinctBatchError(ValueError):
    """Selected I03/S04 consumer cannot be executed without source/risk drift."""


@dataclass(frozen=True)
class S04DistinctOperation:
    query_ref: ExactRef
    predicate_ref: ExactRef
    conditioner_index: int | None = None
    context_requests: tuple[S04ContextRequest, ...] = ()
    producer_permission_ceiling: tuple[str, ...] = FF01_DESCRIPTIVE


@dataclass(frozen=True)
class S04DistinctBatchReceipt:
    canonical_payload: str
    content_hash: str

    def __post_init__(self) -> None:
        try:
            m = loads(self.canonical_payload)
            if (type(m) is not dict or m.get("contract") != CONTRACT
                    or canonical_json(m) != self.canonical_payload
                    or semantic_hash(m) != self.content_hash):
                raise S04DistinctBatchError("noncanonical S04 native batch receipt")
        except (TypeError, ValueError) as exc:
            raise S04DistinctBatchError("malformed S04 native batch receipt") from exc

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            CONTRACT,
            f"urn:rawlsing:s04:distinct-saved-batch:sha256:{self.content_hash}",
            self.content_hash,
        )

    def material(self) -> dict[str, Any]:
        return loads(self.canonical_payload)


@dataclass(frozen=True)
class S04DistinctBatchResult:
    """Actual I03 original output and each S04-first entry stay attached."""

    original_i03_batch: ColdI03BatchResult
    first_consumers: tuple[S04OnePassResult, ...]
    receipt: S04DistinctBatchReceipt


def execute_distinct_native_s04_research(
    *,
    executor: CarrierNeutralResearchExecutor,
    operations: Sequence[S04DistinctOperation],
) -> S04DistinctBatchResult:
    """Preflight original-owned queries; execute I03 once each in one session.

    All operations are catalog-issued and share one release, but each keeps its
    OWN empirical risk and query. It is forbidden to pool counts or describe
    the batch as one population/combined joint. On mid-batch revocation,
    the existing native I03 adapter throws without a partial returned batch.
    No side effect (archive, FF issuance) occurs until all I03 succeeds.
    """
    if type(executor) is not CarrierNeutralResearchExecutor:
        raise S04DistinctBatchError("exact native CarrierNeutralResearchExecutor required")
    if type(executor.repository) is not VerifiedDirectEstate:
        raise S04DistinctBatchError("only verified sourcefree cold C11 estate admitted")
    if type(operations) not in (tuple, list) or not 1 <= len(operations) <= MAX_DISTINCT:
        raise S04DistinctBatchError("1..100 finite ordered original operations required")

    requests: list[ColdI03Operation] = []
    selected: list[tuple[Any, S04DistinctOperation]] = []
    seen: set[str] = set()

    # Full binding and research/FF01 configuration validation takes place
    # BEFORE creating the expensive native cold postings index.
    for item in operations:
        if type(item) is not S04DistinctOperation:
            raise S04DistinctBatchError("exact S04DistinctOperation type required")
        if type(item.query_ref) is not ExactRef or type(item.predicate_ref) is not ExactRef:
            raise S04DistinctBatchError("exact query/predicate references required")
        query = executor.runtime_catalog.resolve_query_exact(item.query_ref)
        predicate = executor.runtime_catalog.resolve_predicate_exact(item.predicate_ref)
        if exact_ref(query.condition_predicate_ref, "original condition") != predicate.ref:
            raise S04DistinctBatchError("original query/predicate binding mismatch")
        if query.ref.key in seen:
            raise S04DistinctBatchError("duplicate query cannot count as distinct native work")
        seen.add(query.ref.key)
        if item.conditioner_index is not None:
            if (type(item.conditioner_index) is not int
                    or not 0 <= item.conditioner_index < len(query.target_refs)
                    or len(query.target_refs) < 2):
                raise S04DistinctBatchError("FF01 conditioning requires a genuine k>=2 query role")
        if type(item.context_requests) is not tuple:
            raise S04DistinctBatchError("contexts must be bounded immutable typed tuple")
        if len(item.context_requests) > 100 or any(
                type(req) is not S04ContextRequest for req in item.context_requests):
            raise S04DistinctBatchError("no invented adaptive/unknown S04 context requests")
        if type(item.producer_permission_ceiling) is not tuple or any(
                type(label) is not str for label in item.producer_permission_ceiling):
            raise S04DistinctBatchError("exact caller-declared permission ceiling labels required")
        # Reuse the original FF01 protected-use guard *before* native source
        # preparation, not only on the eventual consumer. This does not issue
        # or extend a source permission: it rejects invalid caller text early.
        _permission_set(item.producer_permission_ceiling, "producer permissions")
        for req in item.context_requests:
            if (type(req.target_index) is not int
                    or not 0 <= req.target_index < len(query.target_refs)
                    or not isinstance(req.conditions, dict)
                    or any(type(index) is not int
                           or index == req.target_index
                           or not 0 <= index < len(query.target_refs)
                           for index in req.conditions)):
                raise S04DistinctBatchError("context axes invalid for original query topology")
        requests.append(ColdI03Operation(query.ref, predicate.ref))
        selected.append((query, item))

    source = executor.repository
    source._live()
    native = execute_distinct_native_cold_i03(
        executor=executor,
        operations=tuple(requests),
    )
    source._live()
    if (len(native.results) != len(selected)
            or tuple(q.ref for q, _ in selected) != native.query_refs
            or native.source_release_ref != executor.release_refs[0]
            or native.prepared_session_count != 1):
        raise S04DistinctBatchError("native saved I03 batch changed exact request or release")

    first: list[S04OnePassResult] = []
    receipt_rows: list[dict[str, Any]] = []
    for position, ((query, instruction), original) in enumerate(zip(selected, native.results)):
        source._live()  # CURRENT check before each new research consumer
        if (original.query_ref != query.ref
                or original.release_refs != executor.release_refs
                or len(original.facts) != 1):
            raise S04DistinctBatchError("saved native I03 result escaped original request scope")
        publication = receive_s04_first_consumer(
            query=query,
            execution=original,
            conditioner_index=instruction.conditioner_index,
            producer_permission_ceiling=instruction.producer_permission_ceiling,
            context_requests=instruction.context_requests,
        )
        source._live()  # refused revocation: no partial return/publication
        product = publication.receipt.material()
        if (product["source_fact_ref"] != original.facts[0].ref.as_dict()
                or product["source_query_ref"] != query.ref.as_dict()
                or product["source_release_ref"] != native.source_release_ref.as_dict()
                or product["s04_knowledge_ref"] != publication.knowledge.ref.as_dict()):
            raise S04DistinctBatchError("S04 first reader changed native fact/release identity")
        first.append(publication)
        receipt_rows.append({
            "index": position,
            "query_ref": query.ref.as_dict(),
            "predicate_ref": instruction.predicate_ref.as_dict(),
            "i03_fact_ref": original.facts[0].ref.as_dict(),
            "risk_ref": publication.knowledge.material()["risk_set_ref"],
            "s04_knowledge_ref": publication.knowledge.ref.as_dict(),
            "ff01_ref": publication.ff01.ref.as_dict() if publication.ff01 else None,
            "context_batch_ref": publication.batch.ref.as_dict() if publication.batch else None,
            "first_consumer_ref": publication.receipt.ref.as_dict(),
            "first_consumer_status": product["consumer_status"],
            "producer_typed_state": publication.knowledge.material()["producer_typed_state"],
        })

    source._live()
    material = {
        "contract": CONTRACT,
        "claim_grade": GRADE,
        "one_existing_native_source_release_ref": native.source_release_ref.as_dict(),
        "prepared_postings_sessions": native.prepared_session_count,
        "distinct_original_i03_operations": len(requests),
        "distinct_source_risks_kept_separate": True,
        "ordered_research_products": receipt_rows,
        "authorities_not_issued": [
            "ORIGINAL_SURVEY_ACCESS_OR_SEMANTIC_USE_NOT_GRANTED_BY_THIS_SOURCEFREE_ADAPTER",
            "SRC16_GSS1972_CONSTRUCTION_ONLY_GRANT_DOES_NOT_ISSUE_I03_I05_OR_S04",
            "NO_BATCH_POPULATION_OR_CROSS_RISK_POOLING",
            "NO_COMPARATIVE_DETERMINICITY_RANK_SAMPLING_VARIANCE_OR_CAUSALITY",
            "NO_ADAPTIVE_RECURSIVE_MINORITY_SEARCH_OR_ACTOR",
            "NO_DEFAULT_FF01_PRODUCTION_SWITCH_OR_N10E_ONE_PASS",
        ],
    }
    final = S04DistinctBatchReceipt(canonical_json(material), semantic_hash(material))
    return S04DistinctBatchResult(
        original_i03_batch=native,
        first_consumers=tuple(first),
        receipt=final,
    )


__all__ = [
    "CONTRACT", "GRADE", "S04DistinctBatchError", "S04DistinctOperation",
    "S04DistinctBatchReceipt", "S04DistinctBatchResult",
    "execute_distinct_native_s04_research",
]
