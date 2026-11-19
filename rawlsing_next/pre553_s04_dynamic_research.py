"""Dynamic prepared-native I03 -> S04 -> general analytical joint workspace.

Unlike the earlier 1/10/100 author-batch adapters, this session has NO
scientific/query-count ceiling and NO preselected workload. An authorized
caller can select a query from its existing exact runtime catalog, obtain the
original evaluator's fact and a qualified S04 value, and ask an indefinite
sequence of analytical followups from that value without reopening C11.

This does not replace the original S2-C DirectEstateI03Session, mutate its
physical code, grant original survey analysis, or provide grouped reuse
between *different* I03 respondent scans. Each new native I03 query still
runs the accepted evaluator. Reuse across conditioned questions on a single
respondent-coherent S04 joint is provided by S04GeneralJointWorkspace.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_s04_first_consumer import (
    S04OnePassResult, receive_s04_first_consumer,
)
from rawlsing_next.pre553_s04_general_joint_algebra import S04GeneralJointWorkspace
from rawlsing_next.pre553_interpretation_qualification import (
    S04InterpretationCurrent,
)
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
from rawlsing_next.pre553_distinct_cold_s04_batch import (
    SOURCEFREE_ONLY_ASSERTION,
)


class S04DynamicResearchError(ValueError):
    """Operation would overstep original source/current/query/reader boundary."""


@dataclass(frozen=True)
class S04DynamicQuestion:
    """Runtime-catalog-selected original query, not a template invented here."""
    query_ref: ExactRef
    predicate_ref: ExactRef
    conditioner_index: int | None = None


@dataclass(frozen=True)
class S04DynamicResearchResult:
    """One executed I03 fact and its exact downstream S04-first reader."""
    original: S04OnePassResult
    joint_workspace: S04GeneralJointWorkspace


class S04DynamicResearchSession:
    """One native verified session, dynamically selected questions until close.

    Callers own their previously returned answers. No complete batch of
    results is retained in this service and no final all-or-nothing batch
    issuance is claimed. If source CURRENT is revoked, the next operation
    refuses rather than serve a cached prior authority.
    """

    def __init__(
        self,
        *,
        executor: CarrierNeutralResearchExecutor,
        sourcefree_origin_assertion: str,
        resolve_current_response_semantics_ref: Callable[[ExactRef], ExactRef] | None = None,
    ) -> None:
        if sourcefree_origin_assertion != SOURCEFREE_ONLY_ASSERTION:
            raise S04DynamicResearchError(
                "synthetic-sourcefree declaration required; ANVIL construction grants "
                "cannot issue original I03/S04 analysis rights"
            )
        if (type(executor) is not CarrierNeutralResearchExecutor
                or type(executor.repository) is not VerifiedDirectEstate
                or len(executor.release_refs) != 1):
            raise S04DynamicResearchError(
                "exact one-release verified saved C11 executor required"
            )
        if (resolve_current_response_semantics_ref is not None
                and not callable(resolve_current_response_semantics_ref)):
            raise S04DynamicResearchError(
                "version resolver must be callable or absent"
            )
        self._interpretation_resolver = resolve_current_response_semantics_ref
        self._executor = executor
        self._native: DirectEstateI03Session | None = None
        self._opened = False
        self._executed = 0

    def __enter__(self) -> "S04DynamicResearchSession":
        if self._opened:
            raise S04DynamicResearchError("native research session cannot reenter")
        self._executor.repository._live()
        native = DirectEstateI03Session(self._executor.repository)
        self._native = native.__enter__()
        self._opened = True
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self._native is not None:
            self._native.__exit__(exc_type, exc, traceback)
            self._native = None
        self._opened = False

    def ask(self, question: S04DynamicQuestion) -> S04DynamicResearchResult:
        """Original native owner evaluation exactly once, S04 and on-demand algebra.

        A committed result is returned only after CURRENT is checked after
        the S04 consumer. There is no new source caching independent of native
        session custody; ordinary multi-query activity remains subject to
        source revocation between calls.
        """
        if not self._opened or self._native is None:
            raise S04DynamicResearchError("open verified saved session required")
        if (type(question) is not S04DynamicQuestion
                or type(question.query_ref) is not ExactRef
                or type(question.predicate_ref) is not ExactRef):
            raise S04DynamicResearchError("exact catalog-issued query references required")
        repo = self._executor.repository
        repo._live()
        query = self._executor.runtime_catalog.resolve_query_exact(question.query_ref)
        predicate = self._executor.runtime_catalog.resolve_predicate_exact(question.predicate_ref)
        if exact_ref(query.condition_predicate_ref, "query predicate") != predicate.ref:
            raise S04DynamicResearchError("query/predicate identity mismatch")
        # A source's CURRENT is distinct from the CURRENT of its
        # interpretation/mapping. The exact response-semantics ref already
        # belongs to this query's issued output grain; no new fabricated
        # mapping reference is issued by the PYAT service.
        interpretation = None
        if self._interpretation_resolver is not None:
            expected = exact_ref(
                query.requested_output_grain["response_state_semantics_ref"],
                "original query response semantics",
            )
            resolver = self._interpretation_resolver
            interpretation = S04InterpretationCurrent(
                expected_response_semantics_ref=expected,
                resolve_current_response_semantics_ref=lambda: resolver(expected),
            )
            interpretation.check_current()
        actual: QueryExecutionResult = execute_empirical_query(
            repository=self._native,
            query=query,
            predicate=predicate,
            authority_registry=self._executor.runtime_catalog.authority_registry,
            release_refs=self._executor.release_refs,
        )
        repo._live()
        if interpretation is not None:
            interpretation.check_current()
        product = receive_s04_first_consumer(
            query=query,
            execution=actual,
            conditioner_index=question.conditioner_index,
        )
        repo._live()
        if interpretation is not None:
            interpretation.check_current()
        workspace = S04GeneralJointWorkspace(
            knowledge=product.knowledge,
            expected_knowledge_ref=product.knowledge.ref,
            current_guard=repo._live,
            interpretation_current=interpretation,
        )
        self._executed += 1
        return S04DynamicResearchResult(original=product, joint_workspace=workspace)

    def ask_many(
        self, questions: Iterable[S04DynamicQuestion],
    ) -> Iterable[S04DynamicResearchResult]:
        """Lazy dynamic sourcefree research, NO artificial 1/10/100 cap.

        Each returned answer is individually CURRENT checked; if caller
        needs atomic aggregate publication it must use a separate governed
        receiving transaction. Earlier yielded items cannot be labeled as
        whole-stream success after an exception or source revocation.
        """
        for question in questions:
            yield self.ask(question)

    def stats(self) -> dict[str, Any]:
        return {
            "original_native_i03_queries_executed": self._executed,
            "sourcefree_verified_postings_sessions": 1 if self._opened else 0,
            "batch_cardinality_limit": None,
            "interpretation_current_check": (
                "BOUND_EXACT_RESPONSE_SEMANTICS_PRE_POST__CALLER_RESOLVER_NOT_ISSUER"
                if self._interpretation_resolver else
                "INTERPRETATION_CURRENT_UNVERIFIED"
            ),
            "mapping_edition_dependencies": (
                "NEEDS_C11_SOURCE_ISSUED_MAPPING_VERSION_REF_IN_QUERY_AND_FACT"
            ),
            "scientific_rank_or_original_source_authority": None,
        }


__all__ = [
    "S04DynamicResearchError", "S04DynamicQuestion",
    "S04DynamicResearchResult", "S04DynamicResearchSession",
]
