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

from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_discovery_exact import (
    _Atom, _Template, _compile_frontier,
)
from rawlsing_next.pre553_empirical_objects import (
    ExactRef, canonicalize, exact_ref, semantic_hash,
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


def _reconstruct_compiled_candidates(
    compilation: GovernedFrontierCompilation,
    runtime: RuntimeObjectCatalog,
) -> dict[str, Any]:
    """Re-run the existing exact lowerer to materialize its query-role objects.

    The governed compilation retains only role refs, not their exact query and
    predicate preimages. Those preimages are deterministic functions of the
    same frozen grammar the compiler already used. Reusing ``_compile_frontier``
    (the accepted lowerer, not a second engine) recovers exactly the objects
    that the original candidate identities refer to, so issued QUERY units can
    be resolved by the saved I03 owner without a new evaluator.
    """
    plan = compilation.plan
    grammar = plan.native_grammar()
    derived_by_atom: dict[str, Any] = {}
    for record in plan.records:
        derived_by_atom.update(record.derived_predicates)
    predicates = {obj.ref.key: obj for obj in runtime.predicates}
    queries = {obj.ref.key: obj for obj in runtime.queries}
    atoms: dict[str, Any] = {}
    for item in grammar["atoms"]:
        ref = exact_ref(item["predicate_ref"], "R03 v2 lowered atom ref")
        obj = derived_by_atom.get(item["atom_id"]) or predicates.get(ref.key)
        if obj is None:
            raise WorkloadBindingRefusal("R03_V2_LOWERED_ATOM_UNAVAILABLE")
        atoms[item["atom_id"]] = _Atom(
            item["atom_id"], str(item.get("kind", "RESPONSE")), obj, ()
        )
    templates: dict[str, Any] = {}
    for item in grammar["query_templates"]:
        ref = exact_ref(item["query_ref"], "R03 v2 template query ref")
        obj = queries.get(ref.key)
        if obj is None:
            raise WorkloadBindingRefusal("R03_V2_LOWERED_TEMPLATE_UNAVAILABLE")
        templates[item["template_id"]] = _Template(item["template_id"], obj)
    candidates = _compile_frontier(grammar, atoms, templates)
    by_id: dict[str, Any] = {}
    for candidate in candidates:
        if candidate.candidate_id in by_id:
            raise WorkloadBindingRefusal("R03_V2_DUPLICATE_RECOMPILED_CANDIDATE")
        by_id[candidate.candidate_id] = candidate
    return by_id


def _verify_planned_candidates(
    plan: Any, candidates: Mapping[str, Any],
) -> None:
    """Require the plan's frozen candidate census to match exact re-derivation."""
    planned: dict[str, Any] = {}
    for row in plan.expected_candidates:
        candidate_id = row.get("candidate_id")
        if not isinstance(candidate_id, str) or candidate_id in planned:
            raise WorkloadBindingRefusal("R03_V2_PLANNED_CANDIDATE_CENSUS_DRIFT")
        planned[candidate_id] = row
    if set(planned) != set(candidates):
        raise WorkloadBindingRefusal("R03_V2_PLANNED_CANDIDATE_CENSUS_DRIFT")
    for candidate_id, row in planned.items():
        candidate = candidates[candidate_id]
        if candidate.candidate_hash != row.get("candidate_hash"):
            raise WorkloadBindingRefusal("R03_V2_PLANNED_CANDIDATE_IDENTITY_DRIFT")
        planned_roles = [
            (
                role.get("role"),
                canonicalize(role.get("predicate_ref")),
                canonicalize(role.get("query_ref")),
            )
            for role in row.get("query_roles", ())
            if isinstance(role, Mapping)
        ]
        actual_roles = [
            (
                role.role,
                canonicalize(role.predicate.ref.as_dict()),
                canonicalize(role.query.ref.as_dict()),
            )
            for role in candidate.query_roles
        ]
        if planned_roles != actual_roles:
            raise WorkloadBindingRefusal(
                "R03_V2_PLANNED_QUERY_ROLE_IDENTITY_DRIFT"
            )


def _operation_query_roles(
    compilation: GovernedFrontierCompilation,
    candidates: Mapping[str, Any],
) -> tuple[
    tuple[tuple[str, str, str, str], ...],
    tuple[tuple[Any, Any], ...],
    set[str],
]:
    """Return exact operation/role bindings and their object preimages."""
    plan = compilation.plan
    eligible_ids = set(compilation.frontier_eligible_operation_ids)
    dispositions = compilation.operation_dispositions or {}
    bindings: set[tuple[str, str, str, str]] = set()
    role_objects: dict[tuple[str, str], tuple[Any, Any]] = {}
    unissued: set[str] = set()
    for record in plan.records:
        if record.status != SUPPORTED:
            if record.query_role_refs:
                raise WorkloadBindingRefusal("R03_V2_NONSUPPORTED_QUERY_ROLE")
            continue
        if (record.operation_id not in eligible_ids
                or dispositions.get(record.operation_id) != ELIGIBLE):
            raise WorkloadBindingRefusal(
                "R03_V2_NONELIGIBLE_SUPPORTED_OPERATION"
            )
        candidate_keys = tuple(record.expected_candidate_keys)
        if not candidate_keys:
            raise WorkloadBindingRefusal(
                "R03_V2_SUPPORTED_CANDIDATES_UNAVAILABLE"
            )
        planned_rows: set[tuple[str, str, str]] = set()
        for candidate_key in candidate_keys:
            candidate = candidates.get(candidate_key)
            if candidate is None or candidate.rule_id != record.rule_id:
                raise WorkloadBindingRefusal(
                    "R03_V2_SUPPORTED_CANDIDATE_BINDING_DRIFT"
                )
            for role in candidate.query_roles:
                planned_rows.add((
                    role.role, role.predicate.ref.key, role.query.ref.key,
                ))
        actual_rows = {
            (
                row.get("role"),
                exact_ref(row["predicate_ref"], "R03 v2 role predicate").key,
                exact_ref(row["query_ref"], "R03 v2 role query").key,
            )
            for row in record.query_role_refs
            if isinstance(row, Mapping)
        }
        if actual_rows != planned_rows:
            raise WorkloadBindingRefusal("R03_V2_COMPILED_QUERY_ROLE_DRIFT")
        if not actual_rows:
            unissued.add(record.operation_id)
            continue
        for candidate_key in candidate_keys:
            candidate = candidates[candidate_key]
            for role in candidate.query_roles:
                if role.role not in record.coverage_roles:
                    raise WorkloadBindingRefusal("R03_V2_UNDECLARED_QUERY_ROLE")
                # A role query binds its exact role predicate as its condition.
                if exact_ref(
                    role.query.condition_predicate_ref,
                    "R03 v2 role query condition",
                ) != role.predicate.ref:
                    raise WorkloadBindingRefusal(
                        "R03_V2_ROLE_QUERY_PREDICATE_DRIFT"
                    )
                bindings.add((
                    record.operation_id,
                    role.role,
                    role.query.ref.key,
                    role.predicate.ref.key,
                ))
                role_objects.setdefault(
                    (role.predicate.ref.key, role.query.ref.key),
                    (role.predicate, role.query),
                )
    ordered = tuple(sorted(bindings))
    return (
        ordered,
        tuple(role_objects[key] for key in sorted(role_objects)),
        unissued,
    )


def _extend_runtime_catalog(
    runtime: RuntimeObjectCatalog,
    role_objects: tuple[tuple[Any, Any], ...],
) -> RuntimeObjectCatalog:
    """Add the exact issued role preimages to the immutable execution catalog."""
    predicates = {obj.ref.key: obj for obj in runtime.predicates}
    queries = {obj.ref.key: obj for obj in runtime.queries}
    for predicate, query in role_objects:
        for label, target, obj in (
            ("predicate", predicates, predicate),
            ("query", queries, query),
        ):
            previous = target.get(obj.ref.key)
            if previous is not None:
                if canonicalize(previous.as_dict()) != canonicalize(obj.as_dict()):
                    raise WorkloadBindingRefusal(
                        f"R03_V2_ROLE_{label.upper()}_IDENTITY_DRIFT"
                    )
                continue
            target[obj.ref.key] = obj
    return RuntimeObjectCatalog(
        authorities=tuple(runtime.authorities),
        predicates=tuple(predicates.values()),
        queries=tuple(queries.values()),
        discovery_authorities=tuple(runtime.discovery_authorities),
    )


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
    runtime = compilation.runtime_catalog

    candidates = _reconstruct_compiled_candidates(compilation, runtime)
    _verify_planned_candidates(plan, candidates)
    bindings, role_objects, unissued = _operation_query_roles(
        compilation, candidates,
    )
    role_by_key = {
        (predicate.ref.key, query.ref.key): (predicate.ref, query.ref)
        for predicate, query in role_objects
    }
    seen_requests: dict[str, I03ExecutionRequest] = {}
    for _operation_id, _role, query_key, predicate_key in bindings:
        predicate_ref, query_ref = role_by_key[(predicate_key, query_key)]
        request = I03ExecutionRequest(query_ref, predicate_ref)
        earlier = seen_requests.get(query_key)
        if earlier is not None and earlier != request:
            # BatchUnitSpec addresses one QUERY by query ref: two different
            # predicates for that ref cannot be merged into one job.
            raise WorkloadBindingRefusal(
                "R03_V2_AMBIGUOUS_QUERY_PREDICATE_ROLE"
            )
        seen_requests[query_key] = request
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
        for operation_id, role, query_key, _predicate_key in bindings
    )
    extended_catalog = _extend_runtime_catalog(runtime, role_objects)
    for request in requests:
        query = extended_catalog.resolve_query_exact(request.query_ref)
        extended_catalog.resolve_predicate_exact(request.predicate_ref)
        if exact_ref(
            query.condition_predicate_ref, "R03 v2 issued query condition",
        ) != request.predicate_ref:
            raise WorkloadBindingRefusal(
                "R03_V2_ROLE_QUERY_PREDICATE_DRIFT"
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
        catalog=extended_catalog,
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
