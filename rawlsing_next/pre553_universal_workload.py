"""R61 R03 total sourcefree native workload compilation.

Consumes an admitted B49/R02 ``NativePreimageBundle`` and the exact recovered
U43 issued-workload transport.  Operations are derived from the administered
source inventory and response domains, never a selected question list.  Native
execution remains in the existing C11/Route B/I03/I05/Batch owners.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_native_workload_binding import (
    OperationFixture, TestOnlyIssuedWorkload, WorkloadBindingRefusal,
    build_projection_catalog, build_test_only_workload,
    execute_test_only_workload,
)
from rawlsing_next.pre553_source_native_preimage_adapter import NativePreimageBundle

SCHEMA = "PRE553_R03_UNIVERSAL_NATIVE_WORKLOAD@1.0.0"
TEST_ONLY = "TEST_ONLY_SOURCEFREE"


def _hash(value: Any) -> str:
    return semantic_hash(value)


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class UniversalOperation:
    operation_id: str
    source_variable_code: str
    response_value: str
    occurrence_identity: Mapping[str, Any]
    measure_kind: str = "RAW"
    status: str = "COMPILED"
    reason: str | None = None

    def material(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "source_variable_code": self.source_variable_code,
            "response_value": self.response_value,
            "occurrence_identity": dict(self.occurrence_identity),
            "measure_kind": self.measure_kind,
            "status": self.status, "reason": self.reason,
        }


@dataclass(frozen=True)
class CompiledOperation:
    operation: UniversalOperation
    issued: TestOnlyIssuedWorkload | None = None


@dataclass(frozen=True)
class WorkloadCompilation:
    schema: str
    bundle_hash: str
    source_sha256: str
    as_of: str
    host: str
    purpose: str
    operations: tuple[UniversalOperation, ...]
    compiled: tuple[CompiledOperation, ...]
    expected_frontier_root: str
    expected_jobs: tuple[tuple[str, str, str], ...]

    def material(self) -> dict[str, Any]:
        return {
            "schema": self.schema, "bundle_hash": self.bundle_hash,
            "source_sha256": self.source_sha256, "as_of": self.as_of,
            "host": self.host, "purpose": self.purpose,
            "operations": [op.material() for op in self.operations],
            "expected_frontier_root": self.expected_frontier_root,
            "expected_jobs": [list(x) for x in self.expected_jobs],
        }

    @property
    def content_hash(self) -> str:
        return _hash(self.material())


@dataclass(frozen=True)
class UniversalWorkloadResult:
    compilation: WorkloadCompilation
    native_results: tuple[Any, ...]
    executed_operation_ids: tuple[str, ...]
    receipt_refs: tuple[ExactRef, ...]
    fact_refs: tuple[ExactRef, ...]
    failed: tuple[Mapping[str, Any], ...]

    def anti_join(self) -> dict[str, Any]:
        expected = {op.operation_id for op in self.compilation.operations
                    if op.status == "COMPILED"}
        executed = set(self.executed_operation_ids)
        return {
            "expected_count": len(expected),
            "executed_count": len(executed),
            "missing_operation_ids": tuple(sorted(expected - executed)),
            "unexpected_operation_ids": tuple(sorted(executed - expected)),
            "duplicate_operation_ids": tuple(sorted({
                x for x in self.executed_operation_ids
                if self.executed_operation_ids.count(x) > 1
            })),
            "no_drop_ok": expected == executed and len(self.executed_operation_ids) == len(executed),
        }


def _domain_values(bundle: NativePreimageBundle, item: Any) -> tuple[str, ...]:
    qref = bundle.question_refs.get(item.source_variable_code)
    if qref is None:
        return ()
    values = set()
    for slot in bundle.projection.response_slots:
        if slot.question_binding.native_question_ref != qref:
            continue
        for rule in slot.values:
            if rule.response_state == "SUBSTANTIVE_RESPONSE" and rule.canonical_value is not None:
                values.add(str(rule.canonical_value))
    return tuple(sorted(values))


def compile_universal_workload(
    *,
    bundle: NativePreimageBundle,
    as_of: str,
    host: str,
    purpose: str,
    measure_kind: str = "RAW",
) -> WorkloadCompilation:
    """Freeze the finite administered inventory frontier before any native run."""
    if not isinstance(bundle, NativePreimageBundle):
        raise WorkloadBindingRefusal("NATIVE_PREIMAGE_BUNDLE_REQUIRED")
    operations: list[UniversalOperation] = []
    compiled: list[CompiledOperation] = []
    expected_jobs: list[tuple[str, str, str]] = []
    for item in bundle.administered:
        values = _domain_values(bundle, item)
        if not values:
            operation = UniversalOperation(
                operation_id="urn:r03:op:" + _hash({
                    "source": bundle.source_sha256, "item": item.source_variable_code,
                    "value": None, "as_of": as_of}),
                source_variable_code=item.source_variable_code,
                response_value="", occurrence_identity=item.as_dict(),
                measure_kind=measure_kind, status="UNSUPPORTED_RUNTIME",
                reason="NO_SUBSTANTIVE_DOMAIN_VALUE",
            )
            operations.append(operation)
            compiled.append(CompiledOperation(operation=operation))
            continue
        for value in values:
            occurrence = item.as_dict()
            operation_id = "urn:r03:op:" + _hash({
                "schema": SCHEMA, "source": bundle.source_sha256,
                "item": item.source_variable_code, "value": value,
                "occurrence": occurrence, "measure": measure_kind, "as_of": as_of,
            })
            operation = UniversalOperation(
                operation_id=operation_id,
                source_variable_code=item.source_variable_code,
                response_value=value, occurrence_identity=occurrence,
                measure_kind=measure_kind,
            )
            fixture = OperationFixture(
                fixture_id="R03-" + _hash({"item": item.source_variable_code, "value": value})[:16],
                target_variable_code=item.source_variable_code,
                response_value=value, measure_kind=measure_kind,
            )
            try:
                catalog, request = build_projection_catalog(
                    bundle=bundle, operation=fixture, as_of=as_of)
                issued = build_test_only_workload(
                    bundle=bundle, projection=bundle.projection, catalog=catalog,
                    request=request, operation=fixture, as_of=as_of,
                    host=host, purpose=purpose,
                )
                operations.append(operation)
                compiled.append(CompiledOperation(operation=operation, issued=issued))
                expected_jobs.extend(issued.record.expected_jobs)
            except WorkloadBindingRefusal as exc:
                refused = UniversalOperation(
                    operation_id=operation.operation_id,
                    source_variable_code=operation.source_variable_code,
                    response_value=operation.response_value,
                    occurrence_identity=operation.occurrence_identity,
                    measure_kind=operation.measure_kind,
                    status="UNSUPPORTED_RUNTIME", reason=exc.code,
                )
                operations.append(refused)
                compiled.append(CompiledOperation(operation=refused))
    expected_jobs_tuple = tuple(sorted(expected_jobs))
    if len(set(expected_jobs_tuple)) != len(expected_jobs_tuple):
        raise WorkloadBindingRefusal("DUPLICATE_EXPECTED_NATIVE_JOB")
    root = _hash({
        "schema": SCHEMA, "bundle": bundle.bundle_hash,
        "source_sha256": bundle.source_sha256, "as_of": as_of,
        "operations": [op.material() for op in operations],
        "expected_jobs": [list(x) for x in expected_jobs_tuple],
    })
    return WorkloadCompilation(
        schema=SCHEMA, bundle_hash=bundle.bundle_hash,
        source_sha256=bundle.source_sha256, as_of=as_of, host=host,
        purpose=purpose, operations=tuple(operations), compiled=tuple(compiled),
        expected_frontier_root=root, expected_jobs=expected_jobs_tuple,
    )


def execute_universal_workload(
    *, compilation: WorkloadCompilation, source_factory: Any
) -> UniversalWorkloadResult:
    if not isinstance(compilation, WorkloadCompilation):
        raise WorkloadBindingRefusal("WORKLOAD_COMPILATION_REQUIRED")
    native_results = []
    executed_ids: list[str] = []
    receipt_refs: list[ExactRef] = []
    fact_refs: list[ExactRef] = []
    failed: list[Mapping[str, Any]] = []
    for item in compilation.compiled:
        if item.issued is None:
            failed.append({"operation_id": item.operation.operation_id,
                           "status": item.operation.status,
                           "reason": item.operation.reason})
            continue
        try:
            result = execute_test_only_workload(
                issued=item.issued, source_factory=source_factory,
                host=compilation.host, purpose=compilation.purpose,
            )
        except Exception as exc:
            failed.append({"operation_id": item.operation.operation_id,
                           "status": "ERROR", "reason": type(exc).__name__})
            continue
        native_results.append(result)
        executed_ids.append(item.operation.operation_id)
        receipt_refs.extend(result.receipts and tuple(
            r.receipt_ref for r in result.receipts) or ())
        for output in result.native_outputs:
            for fact in getattr(output, "facts", ()):
                fact_refs.append(fact.ref)
    return UniversalWorkloadResult(
        compilation=compilation, native_results=tuple(native_results),
        executed_operation_ids=tuple(executed_ids),
        receipt_refs=tuple(sorted(set(receipt_refs), key=lambda r: r.key)),
        fact_refs=tuple(sorted(set(fact_refs), key=lambda r: r.key)),
        failed=tuple(failed),
    )


@dataclass(frozen=True)
class RecursiveWorkloadFragment:
    campaign_ref: str
    execution_ref: str
    operation_ids: tuple[str, ...]
    receipt_refs: tuple[ExactRef, ...]
    handoff_refs: tuple[ExactRef, ...]
    fact_refs: tuple[ExactRef, ...]
    source_release_refs: tuple[ExactRef, ...]

    def material(self) -> dict[str, Any]:
        return {
            "campaign_ref": self.campaign_ref, "execution_ref": self.execution_ref,
            "operation_ids": list(self.operation_ids),
            "receipt_refs": [r.as_dict() for r in self.receipt_refs],
            "handoff_refs": [r.as_dict() for r in self.handoff_refs],
            "fact_refs": [r.as_dict() for r in self.fact_refs],
            "source_release_refs": [r.as_dict() for r in self.source_release_refs],
        }


def bind_recursive_execution(campaign: Any, execution_ref: str) -> RecursiveWorkloadFragment:
    """Consume exact retained R01 campaign execution; never re-run lineage."""
    snapshot = campaign.snapshot()
    payload = snapshot["payload"]
    execution = next(
        (row for row in payload.get("executions", ())
         if row["execution_ref"] == execution_ref), None)
    if execution is None:
        raise WorkloadBindingRefusal("RECURSIVE_EXECUTION_NOT_RETAINED")
    preimage = execution["activation_preimage"]
    receipt_refs = tuple(sorted(
        (ExactRef(**ref) for ref in execution["receipt_refs"]), key=lambda r: r.key))
    handoff_refs = tuple(sorted(
        (ExactRef(**ref) for ref in execution["handoff_refs"]), key=lambda r: r.key))
    fact_refs = tuple(sorted({
        ExactRef(**ref) for receipt in preimage["receipts"]
        for ref in receipt.get("semantic_fields", {}).get("empirical_fact_refs", ())
    }, key=lambda r: r.key))
    operation_ids = tuple(sorted(
        receipt.get("semantic_fields", {}).get("candidate_identity", {}).get("rule_id")
        for receipt in preimage["receipts"]
    ))
    releases = tuple(sorted(
        (ExactRef(**ref) for ref in payload["root"]["source_release_refs"]),
        key=lambda r: r.key))
    return RecursiveWorkloadFragment(
        campaign_ref=payload["campaign_ref"], execution_ref=execution_ref,
        operation_ids=operation_ids, receipt_refs=receipt_refs,
        handoff_refs=handoff_refs, fact_refs=fact_refs,
        source_release_refs=releases,
    )


__all__ = [
    "SCHEMA", "TEST_ONLY", "UniversalOperation", "WorkloadCompilation",
    "UniversalWorkloadResult", "RecursiveWorkloadFragment",
    "compile_universal_workload", "execute_universal_workload",
    "bind_recursive_execution",
]
