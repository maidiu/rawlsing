"""R03 v2: TEST_ONLY governed QUERY issuance from an authentic R03 lowering.

The existing R03 v1 issuer deliberately issues discovery alone.  This module
does not modify that contract, create an original-data permission, decide
source-scientific eligibility or patch S1-E's v1 postconsumer guard. It
derives the only possible v2 QUERY jobs from original eligible + supported
lowered operation/query-role preimages, not from caller-requested query refs.

An issuer-owned sourcefree contract candidate, pending its competent owner,
actual native first-consumer and independent G5 acceptance.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import (
    ExactRef, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_issued_workload import operation_jobs
from rawlsing_next.pre553_native_workload_binding import (
    TestOnlyIssuedWorkload, WorkloadBindingRefusal, _ref,
)
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
from rawlsing_next.pre553_source_postconsumer_receipts import (
    _verify_original_governed_issuer, SourceReceiptJoinError,
)
from rawlsing_next.pre553_universal_workload import (
    GOVERNED_FRONTIER_SCHEMA, GovernedFrontierCompilation,
    compile_governed_frontier,
)
from rawlsing_next.universal_grammar.native_map import SUPPORTED
from rawlsing_next.universal_grammar.types import ELIGIBLE


GOVERNED_QUERY_ISSUER_SCHEMA = "PRE553_R03_ORIGINAL_GOVERNED_QUERY_ISSUER@2.0.0"


@dataclass(frozen=True)
class GovernedQueryJobBinding:
    """Original scientific operation + role to the exact native QUERY job."""

    operation_id: str
    query_role: str
    query_ref: ExactRef
    predicate_ref: ExactRef

    def material(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "query_role": self.query_role,
            "query_ref": self.query_ref.as_dict(),
            "predicate_ref": self.predicate_ref.as_dict(),
        }


@dataclass(frozen=True)
class GovernedQueryIssuanceV2:
    """Separate versioned issuance; old v1 S1-E verifier must NOT accept it."""

    schema: str
    original_compilation: GovernedFrontierCompilation
    issued: TestOnlyIssuedWorkload
    operation_jobs: tuple[GovernedQueryJobBinding, ...]
    unissued_supported_operation_ids: tuple[str, ...]

    def material(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "original_compilation_hash": self.original_compilation.content_hash,
            "source_sha256": self.original_compilation.source_sha256,
            "inventory_hash": self.original_compilation.inventory_hash,
            "frontier_hash": self.original_compilation.frontier_hash,
            "policy_hash": self.original_compilation.policy_hash,
            "plan_hash": self.original_compilation.plan.content_hash,
            "issuer_decision_ref": self.issued.record.decision_ref.as_dict(),
            "issued_envelope_sha256": self.issued.envelope_sha256,
            "issued_expected_jobs": [
                list(row) for row in self.issued.record.expected_jobs
            ],
            "query_operation_bindings": [
                item.material() for item in self.operation_jobs
            ],
            "unissued_supported_operation_ids": list(
                self.unissued_supported_operation_ids
            ),
            "permission_grade": "TEST_ONLY_SOURCEFREE",
            "native_original_source_rights": "NOT_GRANTED",
            "legacy_r03_discovery_version": GOVERNED_FRONTIER_SCHEMA,
        }

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.material())


def _issue_compiled_governed_queries_v2(
    compilation: GovernedFrontierCompilation,
) -> GovernedQueryIssuanceV2:
    """Issue from the authentic v1 producer without caller-selected QUERY jobs.

    This private helper is for a compilation constructed under the original
    source/inventory/policy/frontier compiler. Public users should call
    compile_and_issue_governed_queries_v2 with ALL original inputs.
    """
    if (not isinstance(compilation, GovernedFrontierCompilation)
            or compilation.schema != GOVERNED_FRONTIER_SCHEMA):
        raise WorkloadBindingRefusal("R03_V2_ORIGINAL_COMPILATION_REQUIRED")
    old = compilation.issued
    try:
        _verify_original_governed_issuer(
            compilation, old.workload, old.record,
            host=compilation.host, purpose=compilation.purpose,
        )
    except SourceReceiptJoinError as exc:
        raise WorkloadBindingRefusal(
            "R03_V2_ORIGINAL_ISSUER_MUST_BE_AUTHENTIC"
        ) from exc
    plan = compilation.plan
    if plan.expected_candidate_error is not None:
        raise WorkloadBindingRefusal("R03_V2_EXPECTED_CANDIDATES_UNAVAILABLE")
    eligible_ids = set(compilation.frontier_eligible_operation_ids)
    claimed_dispositions = compilation.operation_dispositions or {}
    runtime = compilation.runtime_catalog

    seen_requests: dict[str, I03ExecutionRequest] = {}
    bindings: set[tuple[str, str, str, str]] = set()
    unissued: set[str] = set()
    for record in plan.records:
        if record.status != SUPPORTED:
            if record.query_role_refs:
                raise WorkloadBindingRefusal("R03_V2_NONSUPPORTED_QUERY_ROLE")
            continue
        if (record.operation_id not in eligible_ids
                or claimed_dispositions.get(record.operation_id) != ELIGIBLE):
            raise WorkloadBindingRefusal("R03_V2_NONELIGIBLE_SUPPORTED_OPERATION")
        valid_query_refs = {
            exact_ref(
                {key: row[key] for key in ("kind", "object_id", "content_hash")},
                "R03 v2 supported query ref",
            ).key
            for row in record.query_refs
        }
        if not record.query_role_refs:
            unissued.add(record.operation_id)
            continue
        for row in record.query_role_refs:
            if not isinstance(row, Mapping):
                raise WorkloadBindingRefusal("R03_V2_INVALID_QUERY_ROLE")
            role = row.get("role")
            if not isinstance(role, str) or role not in record.coverage_roles:
                raise WorkloadBindingRefusal("R03_V2_UNDECLARED_QUERY_ROLE")
            query_ref = exact_ref(row["query_ref"], "R03 v2 role query")
            predicate_ref = exact_ref(
                row["predicate_ref"], "R03 v2 role predicate"
            )
            if query_ref.key not in valid_query_refs:
                raise WorkloadBindingRefusal("R03_V2_ROLE_QUERY_NOT_FROM_LOWERING")
            # Exact public object preimages and their existing authority law.
            runtime.resolve_query_exact(query_ref)
            runtime.resolve_predicate_exact(predicate_ref)
            request = I03ExecutionRequest(query_ref, predicate_ref)
            earlier = seen_requests.get(query_ref.key)
            if earlier is not None and earlier != request:
                # BatchUnitSpec addresses one QUERY by query ref: two different
                # predicates for that ref cannot be merged into one job.
                raise WorkloadBindingRefusal(
                    "R03_V2_AMBIGUOUS_QUERY_PREDICATE_ROLE"
                )
            seen_requests[query_ref.key] = request
            bindings.add((
                record.operation_id, role, query_ref.key, predicate_ref.key,
            ))

    requests = tuple(sorted(
        seen_requests.values(),
        key=lambda request: (request.query_ref.key, request.predicate_ref.key),
    ))
    by_query = {
        request.query_ref.key: request for request in requests
    }
    ordered_bindings = tuple(
        GovernedQueryJobBinding(
            operation_id=operation_id,
            query_role=role,
            query_ref=by_query[query_key].query_ref,
            predicate_ref=by_query[query_key].predicate_ref,
        )
        for operation_id, role, query_key, _predicate_key in sorted(bindings)
    )
    identity = semantic_hash({
        "schema": GOVERNED_QUERY_ISSUER_SCHEMA,
        "original": compilation.content_hash,
        "plan": plan.content_hash,
        "original_eligible_ids": sorted(eligible_ids),
        "job_bindings": [row.material() for row in ordered_bindings],
        "requests": [request.as_dict() for request in requests],
    })
    label = "r03-governed-query-v2-" + identity[:24]
    decision = _ref(
        "TEST_ONLY_DECISION", label + "-" + compilation.as_of
    )
    workload = replace(
        old.workload,
        decision_ref=decision,
        requests=requests,
    )
    envelope = semantic_hash(workload.envelope())
    record = replace(
        old.record,
        decision_ref=decision,
        source_permission_ref=_ref(
            "TEST_ONLY_SOURCE_PERMISSION", label,
        ),
        scientific_permission_refs=(
            _ref("TEST_ONLY_SCIENTIFIC_PERMISSION", label),
        ),
        expected_jobs=operation_jobs(
            workload.requests, workload.discoveries,
        ),
        envelope_sha256=envelope,
    )
    issued = TestOnlyIssuedWorkload(
        workload=workload,
        record=record,
        descriptor=old.descriptor,
        envelope_sha256=envelope,
    )
    return GovernedQueryIssuanceV2(
        schema=GOVERNED_QUERY_ISSUER_SCHEMA,
        original_compilation=compilation,
        issued=issued,
        operation_jobs=ordered_bindings,
        unissued_supported_operation_ids=tuple(sorted(unissued)),
    )


def compile_and_issue_governed_queries_v2(
    *,
    bundle: Any,
    inventory: Any,
    policy: Any,
    frontier: Any,
    as_of: str,
    host: str,
    purpose: str,
) -> GovernedQueryIssuanceV2:
    """Recompile caller-frozen original science; issue only mapped eligible jobs.

    This is TEST_ONLY_SOURCEFREE. The real source/science issuer, qualified
    source-realization proof and separately versioned S1-E verified receipt
    adapter are NOT provided by this function.
    """
    original = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=as_of, host=host, purpose=purpose,
    )
    return _issue_compiled_governed_queries_v2(original)


__all__ = [
    "GOVERNED_QUERY_ISSUER_SCHEMA",
    "GovernedQueryJobBinding",
    "GovernedQueryIssuanceV2",
    "compile_and_issue_governed_queries_v2",
]
