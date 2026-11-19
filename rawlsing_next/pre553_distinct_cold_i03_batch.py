"""Experimental one-prepared-session native cold I03 work, NOT an I03 engine.

The default accepted CarrierNeutralResearchExecutor.execute_i03 opens and
tears down DirectEstateI03Session for EACH query. That means rebuilding an
O(events) verified SQLite postings index per invocation. This additive,
sourcefree-only adapter shares ONE already-verified native cold session across
1..100 DISTINCT, original-catalog-issued I03 operations. Every operation is
still evaluated by the unchanged original execute_empirical_query kernel.

It does NOT persist or weaken the index, skip source/current/hash checks,
group risk sets across queries, construct a second C11, infer scientific
rankings, issue source rights, or claim the 100k/high-width resource court.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor, CarrierExecutionBindingError,
)
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate

MAX_DISTINCT = 100
GRADE = "SOURCEFREE_SINGLE_PREPARED_I03_SESSION__NO_GROUPED_OR_SOURCE_GRANT"


class ColdI03BatchError(ValueError):
    """Batch does not conserve existing owner query, source or session law."""


@dataclass(frozen=True)
class ColdI03Operation:
    query_ref: ExactRef
    predicate_ref: ExactRef


@dataclass(frozen=True)
class ColdI03BatchResult:
    results: tuple[QueryExecutionResult, ...]
    source_release_ref: ExactRef
    query_refs: tuple[ExactRef, ...]
    prepared_session_count: int
    claim_grade: str


def execute_distinct_native_cold_i03(
    *, executor: CarrierNeutralResearchExecutor,
    operations: Sequence[ColdI03Operation],
) -> ColdI03BatchResult:
    """Execute distinct catalog-selected genuine I03 operations in ONE session.

    All preflight issuer/predicate/query binding runs BEFORE opening the
    expensive cold index. CURRENT is checked both before and after every
    I03 execution; existing native per-respondent/material read guards remain.
    On any exception no partial batch result is returned and context closes.
    """
    if type(executor) is not CarrierNeutralResearchExecutor:
        raise ColdI03BatchError("exact existing carrier executor required")
    if type(executor.repository) is not VerifiedDirectEstate:
        raise ColdI03BatchError("only independently pinned native cold estate supported")
    if isinstance(operations, (str, bytes)) or not isinstance(operations, (list, tuple)):
        raise ColdI03BatchError("finite ordered original operation list required")
    if not 1 <= len(operations) <= MAX_DISTINCT:
        raise ColdI03BatchError("1..100 original selected distinct queries required")
    if len(executor.release_refs) != 1:
        raise ColdI03BatchError("native saved source must be a single exact release")

    source = executor.repository
    source._live()
    selected = []
    seen: set[str] = set()
    for item in operations:
        if (type(item) is not ColdI03Operation
                or type(item.query_ref) is not ExactRef
                or type(item.predicate_ref) is not ExactRef):
            raise ColdI03BatchError("exact typed query/predicate references required")
        query = executor.runtime_catalog.resolve_query_exact(item.query_ref)
        predicate = executor.runtime_catalog.resolve_predicate_exact(item.predicate_ref)
        if exact_ref(query.condition_predicate_ref, "I03 query condition") != predicate.ref:
            raise ColdI03BatchError("original query/predicate binding differs")
        if query.ref.key in seen:
            raise ColdI03BatchError("duplicate query cannot impersonate distinct operations")
        seen.add(query.ref.key)
        selected.append((query, predicate))
    source._live()

    results: list[QueryExecutionResult] = []
    # Unlike CarrierNeutralResearchExecutor.execute_i03, create the SAME
    # original physical scoped index exactly once for the complete batch.
    with DirectEstateI03Session(source) as native_session:
        for query, predicate in selected:
            source._live()
            actual = execute_empirical_query(
                repository=native_session,
                query=query,
                predicate=predicate,
                authority_registry=executor.runtime_catalog.authority_registry,
                release_refs=executor.release_refs,
            )
            source._live()
            if (type(actual) is not QueryExecutionResult
                    or actual.query_ref != query.ref
                    or actual.release_refs != executor.release_refs
                    or actual.source_scope_mode != "SINGLE_UNIVERSE"):
                raise ColdI03BatchError("original I03 changed query/source/operation scope")
            results.append(actual)
    source._live()
    return ColdI03BatchResult(
        results=tuple(results),
        source_release_ref=executor.release_refs[0],
        query_refs=tuple(q.ref for q, _ in selected),
        prepared_session_count=1,
        claim_grade=GRADE,
    )


__all__ = [
    "MAX_DISTINCT", "GRADE", "ColdI03BatchError", "ColdI03Operation",
    "ColdI03BatchResult", "execute_distinct_native_cold_i03",
]
