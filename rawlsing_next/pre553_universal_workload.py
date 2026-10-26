"""R61 R03 total sourcefree native workload compilation.

Consumes an admitted B49/R02 ``NativePreimageBundle`` and the exact recovered
U43 issued-workload transport.  Operations are derived from the administered
source inventory and response domains, never a selected question list.  Native
execution remains in the existing C11/Route B/I03/I05/Batch owners.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import json
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref, semantic_hash
from rawlsing_next.pre553_native_workload_binding import (
    OperationFixture, TestOnlyIssuedWorkload, WorkloadBindingRefusal,
    build_discovery_authority, build_frontier_native_catalog,
    build_projection_catalog, build_test_only_discovery_workload,
    build_test_only_workload, execute_test_only_discovery_workload,
    execute_test_only_workload,
)
from rawlsing_next.pre553_source_native_preimage_adapter import NativePreimageBundle
from rawlsing_next.universal_grammar.native_map import (
    COMPARATOR_PARENT, COMPARATOR_ROOT, NATIVE_UNSUPPORTED, SUPPORTED,
    lower_frontier, native_receipt_anti_join,
)
from rawlsing_next.universal_grammar.types import (
    ELIGIBLE, GrammarPolicy, ScientificFrontier, SourceInventory,
)

SCHEMA = "PRE553_R03_UNIVERSAL_NATIVE_WORKLOAD@1.0.0"
TEST_ONLY = "TEST_ONLY_SOURCEFREE"


def _hash(value: Any) -> str:
    return semantic_hash(value)


def _as_ref(value: Any) -> ExactRef:
    return value if isinstance(value, ExactRef) else exact_ref(value)


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
    if snapshot.get("checkpoint_ref") != _hash(payload):
        raise WorkloadBindingRefusal("RECURSIVE_SNAPSHOT_CHECKPOINT_MISMATCH")
    root_material = payload.get("root", {})
    if root_material.get("campaign_ref") != payload.get("campaign_ref"):
        raise WorkloadBindingRefusal("RECURSIVE_CAMPAIGN_ROOT_MISMATCH")
    root_releases = tuple(sorted(
        (ExactRef(**ref) for ref in root_material.get("source_release_refs", ())),
        key=lambda ref: ref.key))
    if not root_releases:
        raise WorkloadBindingRefusal("RECURSIVE_ROOT_SOURCE_RELEASE_MISSING")
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
    "GOVERNED_FRONTIER_SCHEMA", "GOVERNED_FRONTIER_RESULT_SCHEMA",
    "RECURSIVE_WORKLOAD_SCHEMA", "GovernedFrontierCompilation",
    "GovernedFrontierResult", "RecursiveWorkloadBinding",
    "compile_universal_workload", "execute_universal_workload",
    "bind_recursive_execution", "compile_governed_frontier",
    "execute_governed_frontier", "restore_governed_frontier_ledger",
    "bind_recursive_workload",
]


GOVERNED_FRONTIER_SCHEMA = "PRE553_R03_GOVERNED_FRONTIER_WORKLOAD@1.0.0"
GOVERNED_FRONTIER_RESULT_SCHEMA = "PRE553_R03_GOVERNED_FRONTIER_RESULT@1.0.0"
RECURSIVE_WORKLOAD_SCHEMA = "PRE553_R03_RECURSIVE_WORKLOAD_BINDING@1.0.0"


@dataclass(frozen=True)
class GovernedFrontierCompilation:
    schema: str
    bundle_hash: str
    source_sha256: str
    as_of: str
    host: str
    purpose: str
    inventory_hash: str
    policy_hash: str
    frontier_hash: str
    plan: Any
    issued: TestOnlyIssuedWorkload
    runtime_catalog: RuntimeObjectCatalog
    expected_operation_ids: tuple[str, ...]
    unsupported_operation_ids: tuple[str, ...]
    not_eligible_operation_ids: tuple[str, ...]
    pending_operation_ids: tuple[str, ...]
    expected_candidate_ids: tuple[str, ...]
    frontier_eligible_operation_ids: tuple[str, ...] = ()
    frontier_disposition_counts: Mapping[str, int] | None = None
    operation_claim_classes: Mapping[str, str] | None = None
    operation_dispositions: Mapping[str, str] | None = None

    def material(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "bundle_hash": self.bundle_hash,
            "source_sha256": self.source_sha256,
            "as_of": self.as_of, "host": self.host, "purpose": self.purpose,
            "inventory_hash": self.inventory_hash,
            "policy_hash": self.policy_hash,
            "frontier_hash": self.frontier_hash,
            "lowering": self.plan.material(),
            "issued": {
                "decision_ref": self.issued.record.decision_ref.as_dict(),
                "envelope_sha256": self.issued.envelope_sha256,
                "expected_jobs": [list(job) for job in self.issued.record.expected_jobs],
                "original_u_root": self.issued.record.original_u_root,
                "expected_frontier_root": self.issued.record.expected_frontier_root,
                "scope": self.issued.record.scope,
                "descriptor": dict(self.issued.descriptor),
            },
            "expected_operation_ids": list(self.expected_operation_ids),
            "unsupported_operation_ids": list(self.unsupported_operation_ids),
            "not_eligible_operation_ids": list(self.not_eligible_operation_ids),
            "pending_operation_ids": list(self.pending_operation_ids),
            "expected_candidate_ids": list(self.expected_candidate_ids),
            "frontier_eligible_operation_ids": list(
                self.frontier_eligible_operation_ids
            ),
            "frontier_disposition_counts": dict(
                self.frontier_disposition_counts or {}
            ),
            "operation_claim_classes": dict(
                self.operation_claim_classes or {}
            ),
            "operation_dispositions": dict(
                self.operation_dispositions or {}
            ),
        }

    @property
    def content_hash(self) -> str:
        return _hash(self.material())


@dataclass(frozen=True)
class GovernedFrontierResult:
    schema: str
    compilation: GovernedFrontierCompilation
    native_execution: Any
    operation_ledger: tuple[Mapping[str, Any], ...]
    anti_join: Mapping[str, Any]
    operation_anti_join: Mapping[str, Any]
    receipt_refs: tuple[ExactRef, ...]
    fact_refs: tuple[ExactRef, ...]

    def ledger(self) -> dict[str, Any]:
        native = self.native_execution.native_result
        material = {
            "schema": self.schema,
            "compilation_hash": self.compilation.content_hash,
            "operation_ledger": [dict(row) for row in self.operation_ledger],
            "candidate_anti_join": dict(self.anti_join),
            "operation_anti_join": dict(self.operation_anti_join),
            "receipt_refs": [ref.as_dict() for ref in self.receipt_refs],
            "fact_refs": [ref.as_dict() for ref in self.fact_refs],
            "native_receipts": [
                receipt.as_dict() for receipt in native.receipts
            ],
            "native_facts": [
                fact.as_dict() for fact in native.empirical_facts
            ],
            "evaluated_frontier_ref": native.evaluated_frontier_ref.as_dict(),
            "replay_ref": native.replay_ref.as_dict(),
            "batch_receipt_refs": [
                receipt.receipt_ref.as_dict()
                for receipt in self.native_execution.receipts
            ],
            "expected_jobs": [
                list(job) for job in self.compilation.issued.record.expected_jobs
            ],
            "expected_candidate_ids": list(self.compilation.expected_candidate_ids),
            "compilation": self.compilation.material(),
        }
        return {**material, "ledger_hash": _hash(material)}

    @property
    def content_hash(self) -> str:
        return self.ledger()["ledger_hash"]

    def freeze_restore_checkpoint(self) -> str:
        """Capture the original validated result checkpoint for cold restore."""
        ledger = self.ledger()
        material = dict(ledger)
        material.pop("ledger_hash", None)
        _validate_governed_ledger_material(material)
        return ledger["ledger_hash"]


def compile_governed_frontier(
    *,
    bundle: NativePreimageBundle,
    inventory: SourceInventory,
    policy: GrammarPolicy,
    frontier: ScientificFrontier,
    as_of: str,
    host: str,
    purpose: str,
    query_authority: Any | None = None,
    discovery_authority_snapshot: Any | None = None,
) -> GovernedFrontierCompilation:
    """Lower a caller-frozen R01 frontier into one issued native discovery.

    The caller supplies the already-governed inventory/policy/frontier. This
    function never enumerates a substitute frontier or selects an easier subset.
    """
    if not isinstance(bundle, NativePreimageBundle):
        raise WorkloadBindingRefusal("NATIVE_PREIMAGE_BUNDLE_REQUIRED")
    if not isinstance(inventory, SourceInventory):
        raise WorkloadBindingRefusal("SOURCE_INVENTORY_REQUIRED")
    if not isinstance(policy, GrammarPolicy):
        raise WorkloadBindingRefusal("GRAMMAR_POLICY_REQUIRED")
    if not isinstance(frontier, ScientificFrontier):
        raise WorkloadBindingRefusal("SCIENTIFIC_FRONTIER_REQUIRED")
    if frontier.inventory_hash != inventory.content_hash:
        raise WorkloadBindingRefusal("FRONTIER_INVENTORY_HASH_MISMATCH")
    if frontier.policy_hash != policy.content_hash:
        raise WorkloadBindingRefusal("FRONTIER_POLICY_HASH_MISMATCH")
    catalog, query_auth, baseline, _ = build_frontier_native_catalog(
        bundle=bundle, inventory=inventory, policy=policy,
        frontier=frontier, as_of=as_of,
        query_authority=query_authority,
    )
    pending = tuple(sorted(set(frontier.pending_operation_ids)))
    active_frontier = replace(
        frontier,
        operations=tuple(
            operation for operation in frontier.operations
            if operation.op_id not in set(pending)
        ),
    )
    plan = lower_frontier(inventory, policy, active_frontier, catalog)
    discovery_snapshot, discovery_authority = build_discovery_authority(
        bundle=bundle, grammar=plan.native_grammar(), policy=policy, as_of=as_of,
        authority=discovery_authority_snapshot,
    )
    records = tuple(
        replace(record, discovery_authority_ref=discovery_authority.ref)
        if record.discovery_authority_ref is None else record
        for record in plan.records
    )
    plan = replace(plan, records=records)
    # The lowerer's computed expected candidate identities remain unchanged.
    runtime = RuntimeObjectCatalog(
        authorities=tuple({
            snapshot.authority_ref.key: snapshot
            for snapshot in (
                *bundle.projection.authority_snapshots,
                query_auth, discovery_snapshot,
            )
        }.values()),
        predicates=tuple({
            predicate.ref.key: predicate
            for predicate in (
                *catalog.predicate_objects.values(),
                baseline,
                *(predicate for record in records
                  for predicate in record.derived_predicates.values()),
            )
        }.values()),
        queries=tuple({
            query.ref.key: query for query in catalog.query_objects.values()
        }.values()),
        discovery_authorities=(discovery_authority,),
    )
    targets = tuple(sorted({
        target.item_id for operation in frontier.operations
        for target in operation.targets
    }))
    conditions = tuple(sorted({
        key.item_id for operation in frontier.operations
        for key, _ in operation.conditions
    }))
    issued = build_test_only_discovery_workload(
        bundle=bundle, projection=bundle.projection, catalog=runtime,
        authority=discovery_authority,
        descriptor={
            "targets": list(targets),
            "conditions": list(conditions),
            "measures": [
                "RAW" if operation.measure_kind == "SAMPLE"
                else "GOVERNED_WEIGHTED"
                for operation in frontier.operations
            ],
        },
        inventory=inventory, plan_hash=plan.content_hash,
        as_of=as_of, host=host, purpose=purpose,
    )
    expected_candidates = tuple(sorted(
        candidate["candidate_id"] for candidate in plan.expected_candidates
    ))
    return GovernedFrontierCompilation(
        schema=GOVERNED_FRONTIER_SCHEMA,
        bundle_hash=bundle.bundle_hash,
        source_sha256=bundle.source_sha256,
        as_of=as_of, host=host, purpose=purpose,
        inventory_hash=inventory.content_hash,
        policy_hash=policy.content_hash,
        frontier_hash=frontier.content_hash,
        plan=plan, issued=issued, runtime_catalog=runtime,
        expected_operation_ids=blocked_operation_ids(plan),
        unsupported_operation_ids=tuple(plan.unsupported_operation_ids),
        not_eligible_operation_ids=tuple(plan.not_eligible_operation_ids),
        pending_operation_ids=pending,
        expected_candidate_ids=expected_candidates,
        frontier_eligible_operation_ids=tuple(sorted(
            operation.op_id for operation in frontier.eligible()
        )),
        frontier_disposition_counts=dict(frontier.disposition_counts),
        operation_claim_classes={
            operation.op_id: operation.claim_class
            for operation in frontier.operations
        },
        operation_dispositions={
            operation.op_id: operation.disposition
            for operation in frontier.operations
        },
    )


def blocked_operation_ids(plan: Any) -> tuple[str, ...]:
    if plan.expected_candidate_error is not None:
        raise WorkloadBindingRefusal(
            "EXPECTED_CANDIDATES_NOT_COMPUTED", plan.expected_candidate_error
        )
    return tuple(plan.supported_operation_ids)


def _receipt_candidate_id(receipt: Any) -> str:
    identity = receipt.candidate_identity
    value = identity.get("candidate_id") if isinstance(identity, Mapping) else None
    if not isinstance(value, str) or not value:
        raise WorkloadBindingRefusal("NATIVE_RECEIPT_LACKS_CANDIDATE_ID")
    return value


def _result_state_for(states: Sequence[str]) -> str:
    if not states:
        return "UNKNOWN"
    unique = set(states)
    if "DISCOVERED_RESULT_SUPPORTED" in unique:
        return "SUPPORTED"
    if unique == {"VALID_EMPTY"}:
        return "VALID_EMPTY"
    if "COVERAGE_LIMITED" in unique:
        return "UNKNOWN"
    if "NONCOMPARABLE" in unique:
        return "DIFFUSE"
    if unique <= {"INSUFFICIENT_SUPPORT", "ZERO_SUPPORT"}:
        return "ZERO_SUPPORT"
    return "UNKNOWN"


def execute_governed_frontier(
    *,
    compilation: GovernedFrontierCompilation,
    source_factory: Any,
) -> GovernedFrontierResult:
    """Execute the issued discovery and anti-join every operation/candidate."""
    if not isinstance(compilation, GovernedFrontierCompilation):
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_COMPILATION_REQUIRED")
    plan = compilation.plan
    if plan.expected_candidate_error is not None:
        raise WorkloadBindingRefusal(
            "EXPECTED_CANDIDATES_NOT_COMPUTED", plan.expected_candidate_error
        )
    execution = execute_test_only_discovery_workload(
        issued=compilation.issued, source_factory=source_factory,
        host=compilation.host, purpose=compilation.purpose,
    )
    native = execution.native_result
    anti = native_receipt_anti_join(plan, native.receipts)
    fact_by_ref = {fact.ref.key: fact for fact in native.empirical_facts}
    if len(fact_by_ref) != len(native.empirical_facts):
        anti = {**anti, "no_drop_ok": False, "duplicate_native_fact_ids": True}
    receipt_fact_refs: set[str] = set()
    fact_closure_ok = True
    for receipt in native.receipts:
        refs = [exact_ref(ref).key for ref in receipt.empirical_fact_refs]
        if any(ref not in fact_by_ref for ref in refs):
            fact_closure_ok = False
        receipt_fact_refs.update(refs)
    if receipt_fact_refs != set(fact_by_ref):
        fact_closure_ok = False
    if not fact_closure_ok:
        anti = {**anti, "no_drop_ok": False, "fact_closure_ok": False}
    else:
        anti = {**anti, "fact_closure_ok": True}
    receipt_by_candidate = {
        _receipt_candidate_id(receipt): receipt for receipt in native.receipts
    }
    if len(receipt_by_candidate) != len(native.receipts):
        anti = {**anti, "duplicate_candidate_ids": tuple(sorted({
            candidate for candidate in (
                _receipt_candidate_id(receipt) for receipt in native.receipts
            ) if sum(
                1 for other in native.receipts
                if _receipt_candidate_id(other) == candidate
            ) > 1
        })), "no_drop_ok": False}
    records = {record.operation_id: record for record in plan.records}
    operation_rows: list[Mapping[str, Any]] = []
    missing_operations: list[str] = []
    unexpected_candidates: set[str] = set(receipt_by_candidate)
    for operation in compilation.plan.records:
        source_operation = None
        for candidate in compilation.plan.records:
            if candidate.operation_id == operation.operation_id:
                source_operation = candidate
                break
        expected = set(operation.expected_candidate_keys)
        unexpected_candidates -= expected
        receipts = tuple(
            receipt_by_candidate[candidate_id]
            for candidate_id in sorted(expected)
            if candidate_id in receipt_by_candidate
        )
        missing = tuple(sorted(expected - set(receipt_by_candidate)))
        fact_refs = tuple(sorted({
            _as_ref(fact_ref) for receipt in receipts
            for fact_ref in receipt.empirical_fact_refs
        }, key=lambda ref: ref.key))
        typed_states = tuple(sorted({
            str(receipt.typed_state) for receipt in receipts
        }))
        execution_state = (
            "COMPLETED" if operation.status == SUPPORTED and not missing
            else ("UNSUPPORTED_RUNTIME" if operation.status == NATIVE_UNSUPPORTED
                  else ("NOT_ELIGIBLE" if operation.status != SUPPORTED
                        else "ERROR"))
        )
        if operation.status == SUPPORTED and missing:
            missing_operations.append(operation.operation_id)
        disposition = (compilation.operation_dispositions or {}).get(
            operation.operation_id
        )
        if operation.status == NATIVE_UNSUPPORTED:
            result_state = "UNSUPPORTED"
            execution_state = "UNSUPPORTED_RUNTIME"
        elif operation.status != SUPPORTED:
            result_state = disposition if disposition in {
                "HELD", "UNKNOWN", "PROHIBITED", "INAPPLICABLE_PROVED"
            } else "NOT_ELIGIBLE"
            execution_state = "NOT_STARTED"
        else:
            result_state = _result_state_for(typed_states)
        operation_rows.append({
            "operation_id": operation.operation_id,
            "lowering_status": operation.status,
            "reason": operation.reason,
            "eligibility_state": disposition,
            "execution_state": execution_state,
            "result_state": result_state,
            "expected_candidate_ids": list(sorted(expected)),
            "received_candidate_ids": [
                _receipt_candidate_id(receipt) for receipt in receipts
            ],
            "missing_candidate_ids": list(missing),
            "candidate_typed_states": list(typed_states),
            "coverage_states": [
                str(receipt.coverage_state) for receipt in receipts
            ],
            "receipt_refs": [receipt.ref.as_dict() for receipt in receipts],
            "fact_refs": [ref.as_dict() for ref in fact_refs],
            "claim_class": (
                (compilation.operation_claim_classes or {}).get(
                    operation.operation_id
                )
            ),
            "native_family": (
                source_operation.rule["family"] if source_operation
                and source_operation.rule else None
            ),
        })
    known = {row["operation_id"] for row in operation_rows}
    for operation_id in sorted(set(compilation.pending_operation_ids) - known):
        operation_rows.append({
            "operation_id": operation_id,
            "lowering_status": "PENDING",
            "reason": "POLICY_BUDGET_PENDING",
            "execution_state": "PENDING",
            "result_state": "UNKNOWN",
            "expected_candidate_ids": [],
            "received_candidate_ids": [], "missing_candidate_ids": [],
            "candidate_typed_states": [], "coverage_states": [],
            "receipt_refs": [], "fact_refs": [], "claim_class": (
                (compilation.operation_claim_classes or {}).get(operation_id)
            ), "native_family": None,
        })
    expected_operations = set(compilation.expected_operation_ids)
    actual_operations = {
        row["operation_id"] for row in operation_rows
        if row["lowering_status"] == SUPPORTED
        and row["execution_state"] == "COMPLETED"
    }
    supported = set(compilation.expected_operation_ids)
    unsupported = set(compilation.unsupported_operation_ids)
    pending = set(compilation.pending_operation_ids)
    eligible = set(compilation.frontier_eligible_operation_ids)
    accounted = supported | unsupported | pending
    unaccounted = tuple(sorted(eligible - accounted))
    overlap = (
        (supported & unsupported) | (supported & pending) | (unsupported & pending)
    )
    operation_anti = {
        "expected_operation_count": len(expected_operations),
        "completed_operation_count": len(actual_operations),
        "missing_operation_ids": tuple(sorted(expected_operations - actual_operations)),
        "unexpected_operation_ids": tuple(sorted(actual_operations - expected_operations)),
        "missing_candidate_operations": tuple(sorted(missing_operations)),
        "unexpected_candidate_ids": tuple(sorted(unexpected_candidates)),
        "unsupported_operation_ids": list(compilation.unsupported_operation_ids),
        "not_eligible_operation_ids": list(compilation.not_eligible_operation_ids),
        "pending_operation_ids": list(compilation.pending_operation_ids),
        "frontier_eligible_operation_count": len(eligible),
        "accounted_eligible_operation_count": len(accounted),
        "unaccounted_eligible_operation_ids": unaccounted,
        "overlapping_disposition_ids": tuple(sorted(overlap)),
        "accounting_ok": (
            eligible == accounted and not unaccounted and not overlap
        ),
        "no_drop_ok": (
            expected_operations == actual_operations
            and not missing_operations and not unexpected_candidates
            and eligible == accounted and not unaccounted and not overlap
            and anti.get("no_drop_ok") is True
        ),
    }
    receipt_refs = tuple(sorted(
        (receipt.ref for receipt in native.receipts), key=lambda ref: ref.key
    ))
    fact_refs = tuple(sorted(
        {_as_ref(fact.ref) for fact in native.empirical_facts},
        key=lambda ref: ref.key,
    ))
    return GovernedFrontierResult(
        schema=GOVERNED_FRONTIER_RESULT_SCHEMA,
        compilation=compilation, native_execution=execution,
        operation_ledger=tuple(sorted(
            operation_rows, key=lambda row: row["operation_id"]
        )),
        anti_join=anti, operation_anti_join=operation_anti,
        receipt_refs=receipt_refs, fact_refs=fact_refs,
    )


def _ledger_ref(value: Mapping[str, Any]) -> ExactRef:
    return ExactRef(value["kind"], value["object_id"], value["content_hash"])


def restore_governed_frontier_ledger(
    ledger: Mapping[str, Any], *, expected_checkpoint_ref: str | None = None
) -> Mapping[str, Any]:
    """Validate an exact persisted ledger against the original external pin."""
    if not isinstance(ledger, Mapping):
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_LEDGER_REQUIRED")
    if not isinstance(expected_checkpoint_ref, str) or not expected_checkpoint_ref:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_EXPECTED_CHECKPOINT_REQUIRED")
    material = dict(ledger)
    claimed = material.pop("ledger_hash", None)
    computed = _hash(material)
    if claimed is None or computed != claimed:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_LEDGER_HASH_MISMATCH")
    if computed != expected_checkpoint_ref:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_CHECKPOINT_PIN_MISMATCH")
def restore_governed_frontier_ledger(
    ledger: Mapping[str, Any], *, expected_checkpoint_ref: str | None = None
) -> Mapping[str, Any]:
    """Validate an exact persisted ledger against the original external pin."""
    if not isinstance(ledger, Mapping):
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_LEDGER_REQUIRED")
    if not isinstance(expected_checkpoint_ref, str) or not expected_checkpoint_ref:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_EXPECTED_CHECKPOINT_REQUIRED")
    material = dict(ledger)
    claimed = material.pop("ledger_hash", None)
    computed = _hash(material)
    if claimed is None or computed != claimed:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_LEDGER_HASH_MISMATCH")
    if computed != expected_checkpoint_ref:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_CHECKPOINT_PIN_MISMATCH")
    return _validate_governed_ledger_material(material)


def _validate_governed_ledger_material(
    material: Mapping[str, Any]
) -> Mapping[str, Any]:
    """Shared pin-free structural/expected/native closure validator."""
    if material.get("schema") != GOVERNED_FRONTIER_RESULT_SCHEMA:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_LEDGER_SCHEMA_MISMATCH")
    required = (
        "operation_ledger", "candidate_anti_join", "operation_anti_join",
        "receipt_refs", "fact_refs", "native_receipts", "native_facts",
        "expected_jobs", "expected_candidate_ids", "compilation",
        "batch_receipt_refs", "evaluated_frontier_ref", "replay_ref",
    )
    for field_name in required:
        if field_name not in material:
            raise WorkloadBindingRefusal(
                "GOVERNED_FRONTIER_LEDGER_FIELD_MISSING", field_name
            )
    compilation = material["compilation"]
    if _hash(compilation) != material.get("compilation_hash"):
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_COMPILATION_HASH_MISMATCH")
    expected_jobs = tuple(tuple(job) for job in material["expected_jobs"])
    issued_jobs = tuple(tuple(job) for job in
                        compilation.get("issued", {}).get("expected_jobs", ()))
    if expected_jobs != issued_jobs or not expected_jobs:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_EXPECTED_JOB_MISMATCH")
    expected_candidates = set(material["expected_candidate_ids"])
    if expected_candidates != set(compilation.get("expected_candidate_ids", ())):
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_EXPECTED_CANDIDATE_MISMATCH")
    rows = material["operation_ledger"]
    row_ids = [row["operation_id"] for row in rows]
    if len(set(row_ids)) != len(row_ids):
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_DUPLICATE_OPERATION")
    row_candidates: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        for candidate in row.get("expected_candidate_ids", ()):
            if candidate in row_candidates:
                raise WorkloadBindingRefusal("GOVERNED_FRONTIER_DUPLICATE_EXPECTED_CANDIDATE")
            row_candidates[candidate] = row
    if set(row_candidates) != expected_candidates:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_EXPECTED_CANDIDATE_ROW_MISMATCH")
    native_receipts = material["native_receipts"]
    native_facts = material["native_facts"]
    receipt_refs = tuple(_ledger_ref(ref) for ref in material["receipt_refs"])
    fact_refs = tuple(_ledger_ref(ref) for ref in material["fact_refs"])
    receipt_refs_from_objects = tuple(sorted(
        (ExactRef(f"{row['schema_id']}@{row['schema_version']}", row["object_id"], row["content_hash"])
         for row in native_receipts), key=lambda ref: ref.key))
    if tuple(sorted(receipt_refs, key=lambda ref: ref.key)) != receipt_refs_from_objects:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_RECEIPT_REF_MISMATCH")
    fact_by_key = {
        ExactRef(f"{row['schema_id']}@{row['schema_version']}", row["object_id"], row["content_hash"]).key: row
        for row in native_facts
    }
    if len(fact_by_key) != len(native_facts):
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_DUPLICATE_NATIVE_FACT")
    if len(receipt_refs_from_objects) != len(native_receipts):
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_DUPLICATE_NATIVE_RECEIPT")
    if tuple(sorted(fact_refs, key=lambda ref: ref.key)) != tuple(sorted(
        (ExactRef(f"{row['schema_id']}@{row['schema_version']}", row["object_id"], row["content_hash"])
         for row in native_facts), key=lambda ref: ref.key
    )):
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_FACT_REF_MISMATCH")
    covered_facts: set[str] = set()
    seen_candidates: list[str] = []
    for receipt in native_receipts:
        semantic = receipt.get("semantic_fields", {})
        identity = semantic.get("candidate_identity") if isinstance(semantic, Mapping) else None
        if not isinstance(identity, Mapping) or not isinstance(identity.get("candidate_id"), str):
            raise WorkloadBindingRefusal("GOVERNED_FRONTIER_RECEIPT_IDENTITY_MISSING")
        candidate = identity["candidate_id"]
        seen_candidates.append(candidate)
        row = row_candidates.get(candidate)
        if row is None:
            raise WorkloadBindingRefusal("GOVERNED_FRONTIER_UNEXPECTED_RECEIPT_CANDIDATE")
        ref = ExactRef(f"{receipt['schema_id']}@{receipt['schema_version']}", receipt["object_id"], receipt["content_hash"])
        if ref.as_dict() not in row.get("receipt_refs", ()):
            raise WorkloadBindingRefusal("GOVERNED_FRONTIER_ROW_RECEIPT_MISMATCH")
        receipt_facts = set()
        for fact_ref in semantic.get("empirical_fact_refs", ()):
            fact = _ledger_ref(fact_ref).key
            if fact not in fact_by_key:
                raise WorkloadBindingRefusal("GOVERNED_FRONTIER_RECEIPT_FACT_MISSING")
            receipt_facts.add(fact)
            if fact_ref not in row.get("fact_refs", ()):
                raise WorkloadBindingRefusal("GOVERNED_FRONTIER_ROW_FACT_MISMATCH")
        covered_facts.update(receipt_facts)
        if receipt["typed_state"] not in row.get("candidate_typed_states", ()):
            raise WorkloadBindingRefusal("GOVERNED_FRONTIER_ROW_STATE_MISMATCH")
        if semantic.get("coverage_state") not in row.get("coverage_states", ()):
            raise WorkloadBindingRefusal("GOVERNED_FRONTIER_ROW_COVERAGE_MISMATCH")
    if len(seen_candidates) != len(set(seen_candidates)):
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_DUPLICATE_RECEIPT_CANDIDATE")
    if set(seen_candidates) != expected_candidates:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_RECEIPT_CANDIDATE_SET_MISMATCH")
    if covered_facts != set(fact_by_key):
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_FACT_COVERAGE_MISMATCH")
    if material["candidate_anti_join"].get("no_drop_ok") is not True:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_CANDIDATE_ANTIJOIN_FAILED")
    if material["operation_anti_join"].get("no_drop_ok") is not True:
        raise WorkloadBindingRefusal("GOVERNED_FRONTIER_OPERATION_ANTIJOIN_FAILED")
    return material


@dataclass(frozen=True)
class RecursiveWorkloadBinding:
    schema: str
    campaign_ref: str
    execution_ref: str
    issuance_ref: str
    plan_ref: str
    generation: int
    checkpoint_ref: str
    policy_id: str
    policy_hash: str
    bounds: Mapping[str, int]
    target_label: str
    query_ref: Mapping[str, Any]
    root_predicate_ref: Mapping[str, Any]
    parents: tuple[Mapping[str, Any], ...]
    expected_operation_ids: tuple[str, ...]
    actual_rule_ids: tuple[str, ...]
    operations: tuple[Mapping[str, Any], ...]
    root_contrasts: tuple[Mapping[str, Any], ...]
    parent_contrasts: tuple[Mapping[str, Any], ...]
    unissued: tuple[Mapping[str, Any], ...]
    minority: tuple[Mapping[str, Any], ...]
    anti_join: Mapping[str, Any]
    receipt_refs: tuple[ExactRef, ...]
    handoff_refs: tuple[ExactRef, ...]
    fact_refs: tuple[ExactRef, ...]
    source_release_refs: tuple[ExactRef, ...]

    def material(self) -> dict[str, Any]:
        return {
            "schema": self.schema, "campaign_ref": self.campaign_ref,
            "execution_ref": self.execution_ref, "issuance_ref": self.issuance_ref,
            "plan_ref": self.plan_ref, "generation": self.generation,
            "checkpoint_ref": self.checkpoint_ref,
            "policy_id": self.policy_id, "policy_hash": self.policy_hash,
            "bounds": dict(self.bounds), "target_label": self.target_label,
            "query_ref": dict(self.query_ref),
            "root_predicate_ref": dict(self.root_predicate_ref),
            "parents": [dict(row) for row in self.parents],
            "expected_operation_ids": list(self.expected_operation_ids),
            "actual_rule_ids": list(self.actual_rule_ids),
            "operations": [dict(row) for row in self.operations],
            "root_contrasts": [dict(row) for row in self.root_contrasts],
            "parent_contrasts": [dict(row) for row in self.parent_contrasts],
            "unissued": [dict(row) for row in self.unissued],
            "minority": [dict(row) for row in self.minority],
            "anti_join": dict(self.anti_join),
            "receipt_refs": [ref.as_dict() for ref in self.receipt_refs],
            "handoff_refs": [ref.as_dict() for ref in self.handoff_refs],
            "fact_refs": [ref.as_dict() for ref in self.fact_refs],
            "source_release_refs": [ref.as_dict() for ref in self.source_release_refs],
        }

    @property
    def content_hash(self) -> str:
        # The R01 snapshot checkpoint canonicalizes list insertion order; the
        # bound operation/receipt/fact/activation material is the semantic
        # cold-restore identity.  The checkpoint remains exact custody evidence.
        material = self.material()
        material.pop("checkpoint_ref", None)
        return _hash(material)


def bind_recursive_workload(
    campaign: Any, execution_ref: str
) -> RecursiveWorkloadBinding:
    """Bind exact retained recurrence receipts to their issued operation plan."""
    snapshot = campaign.snapshot()
    payload = snapshot["payload"]
    if snapshot.get("checkpoint_ref") != _hash(payload):
        raise WorkloadBindingRefusal("RECURSIVE_SNAPSHOT_CHECKPOINT_MISMATCH")
    root_material = payload.get("root", {})
    if root_material.get("campaign_ref") != payload.get("campaign_ref"):
        raise WorkloadBindingRefusal("RECURSIVE_CAMPAIGN_ROOT_MISMATCH")
    root_releases = tuple(sorted(
        (ExactRef(**ref) for ref in root_material.get("source_release_refs", ())),
        key=lambda ref: ref.key))
    if not root_releases:
        raise WorkloadBindingRefusal("RECURSIVE_ROOT_SOURCE_RELEASE_MISSING")
    execution = next(
        (row for row in payload.get("executions", ())
         if row["execution_ref"] == execution_ref), None)
    if execution is None:
        raise WorkloadBindingRefusal("RECURSIVE_EXECUTION_NOT_RETAINED")
    issuance = next(
        (row for row in payload.get("issuances", ())
         if row["issuance_ref"] == execution["issuance_ref"]), None)
    if issuance is None:
        raise WorkloadBindingRefusal("RECURSIVE_ISSUANCE_NOT_RETAINED")
    plan = issuance["plan"]
    if issuance.get("plan_ref") != _hash(plan):
        raise WorkloadBindingRefusal("RECURSIVE_PLAN_REF_MISMATCH")
    if execution.get("plan_ref") != issuance.get("plan_ref"):
        raise WorkloadBindingRefusal("RECURSIVE_EXECUTION_PLAN_MISMATCH")
    preimage = execution["activation_preimage"]
    receipts = tuple(preimage["receipts"])
    for receipt in receipts:
        semantic = receipt.get("semantic_fields", {})
        receipt_releases = tuple(sorted(
            (ExactRef(**ref) for ref in semantic.get("source_release_refs", ())),
            key=lambda ref: ref.key))
        if receipt_releases != root_releases:
            raise WorkloadBindingRefusal("RECURSIVE_RECEIPT_SOURCE_RELEASE_MISMATCH")
    expected = tuple(plan["expected_operations"])
    expected_by_rule = {row["rule_id"]: row for row in expected}
    if len(expected_by_rule) != len(expected):
        raise WorkloadBindingRefusal("RECURSIVE_EXPECTED_RULE_DUPLICATE")
    observed_receipt_refs = {
        ExactRef(
            "DiscoveryResultReceipt@1.0.0", row["object_id"], row["content_hash"]
        )
        for row in receipts
    }
    declared_receipt_refs = {ExactRef(**ref) for ref in execution["receipt_refs"]}
    if observed_receipt_refs != declared_receipt_refs:
        raise WorkloadBindingRefusal("RECURSIVE_RECEIPT_REF_MISMATCH")
    observed_handoff_refs = {ExactRef(**row["handoff_ref"]) for row in preimage["handoffs"]}
    declared_handoff_refs = {ExactRef(**ref) for ref in execution["handoff_refs"]}
    if observed_handoff_refs != declared_handoff_refs:
        raise WorkloadBindingRefusal("RECURSIVE_HANDOFF_REF_MISMATCH")
    actual_by_rule: dict[str, list[Mapping[str, Any]]] = {}
    for receipt in receipts:
        semantic = receipt.get("semantic_fields")
        identity = semantic.get("candidate_identity") if isinstance(semantic, Mapping) else None
        if not isinstance(identity, Mapping):
            raise WorkloadBindingRefusal("RECURSIVE_RECEIPT_IDENTITY_MISSING")
        rule_id = identity.get("rule_id")
        if not isinstance(rule_id, str):
            raise WorkloadBindingRefusal("RECURSIVE_RECEIPT_RULE_MISSING")
        actual_by_rule.setdefault(rule_id, []).append(receipt)
    missing = tuple(sorted(set(expected_by_rule) - set(actual_by_rule)))
    unexpected = tuple(sorted(set(actual_by_rule) - set(expected_by_rule)))
    count_mismatches = {
        rule_id: {
            "expected": int(expected_by_rule[rule_id].get(
                "expected_candidate_count", 1
            )),
            "actual": len(rows),
        }
        for rule_id, rows in sorted(actual_by_rule.items())
        if rule_id in expected_by_rule and len(rows) != int(
            expected_by_rule[rule_id].get("expected_candidate_count", 1)
        )
    }
    operation_rows = []
    for operation in sorted(expected, key=lambda row: row["operation_id"]):
        rows = actual_by_rule.get(operation["rule_id"], [])
        receipt = rows[0] if len(rows) == 1 else None
        semantic = receipt.get("semantic_fields", {}) if receipt else {}
        identity = semantic.get("candidate_identity", {}) if semantic else {}
        receipt_ref = None
        if receipt is not None:
            receipt_ref = {
                "kind": receipt["schema_id"],
                "object_id": receipt["object_id"],
                "content_hash": receipt["content_hash"],
            }
        operation_rows.append({
            "operation_id": operation["operation_id"],
            "generation": operation["generation"],
            "parent_id": operation["parent_id"],
            "comparator": operation["comparator"],
            "rule_id": operation["rule_id"],
            "condition_keys": operation["condition_keys"],
            "condition_values": operation["condition_values"],
            "baseline_predicate_ref": operation["baseline_predicate_ref"],
            "candidate_id": identity.get("candidate_id"),
            "typed_state": receipt.get("typed_state") if receipt else "UNRUN",
            "coverage_state": semantic.get("coverage_state") if semantic else None,
            "fact_refs": list(semantic.get("empirical_fact_refs", ()))
            if semantic else [],
            "receipt_ref": receipt_ref,
            "winning_predicate_ref": (
                semantic.get("winning_predicate_ref") if semantic else None
            ),
        })
    root_rows = tuple(
        row for row in operation_rows if row["comparator"] == COMPARATOR_ROOT
    )
    parent_rows = tuple(
        row for row in operation_rows if row["comparator"] == COMPARATOR_PARENT
    )
    activation = next(
        (row for row in payload.get("activations", ())
         if row["execution_ref"] == execution_ref), None)
    minority = []
    if activation is not None:
        minority.extend({
            "kind": "WAITING", **dict(row),
        } for row in activation.get("waiting", ()))
        minority.extend({
            "kind": "STOPPED", **dict(row),
        } for row in activation.get("stopped", ()))
        minority.extend({
            "kind": "ACTIVATION_LEDGER", **dict(row),
        } for row in activation.get("ledger", ()))
    minority.extend({
        "kind": "RESULT_NONWINNING", "operation_id": row["operation_id"],
        "rule_id": row["rule_id"], "typed_state": row["typed_state"],
    } for row in operation_rows if row["typed_state"] != "DISCOVERED_RESULT_SUPPORTED")
    receipt_refs = tuple(sorted(
        (ExactRef(**ref) for ref in execution["receipt_refs"]),
        key=lambda ref: ref.key))
    handoff_refs = tuple(sorted(
        (ExactRef(**ref) for ref in execution["handoff_refs"]),
        key=lambda ref: ref.key))
    fact_refs = tuple(sorted({
        ExactRef(**ref)
        for row in operation_rows for ref in row["fact_refs"]
    }, key=lambda ref: ref.key))
    releases = tuple(sorted(
        (ExactRef(**ref) for ref in payload["root"]["source_release_refs"]),
        key=lambda ref: ref.key))
    anti = {
        "expected_operation_count": len(expected),
        "received_rule_count": len(actual_by_rule),
        "missing_rule_ids": missing,
        "unexpected_rule_ids": unexpected,
        "count_mismatches": count_mismatches,
        "missing_candidate_operations": [
            row["operation_id"] for row in operation_rows
            if row["typed_state"] == "UNRUN"
        ],
        "no_drop_ok": (
            not missing and not unexpected and not count_mismatches
            and all(row["typed_state"] != "UNRUN" for row in operation_rows)
        ),
    }
    return RecursiveWorkloadBinding(
        schema=RECURSIVE_WORKLOAD_SCHEMA,
        campaign_ref=payload["campaign_ref"],
        execution_ref=execution_ref,
        issuance_ref=execution["issuance_ref"],
        plan_ref=issuance["plan_ref"],
        generation=int(plan["generation"]),
        checkpoint_ref=snapshot["checkpoint_ref"],
        policy_id=str(plan["policy_id"]),
        policy_hash=str(plan["policy_hash"]),
        bounds=dict(payload["root"]["policy"]["bounds"]),
        target_label=str(plan["target_label"]),
        query_ref=dict(plan["query_ref"]),
        root_predicate_ref=dict(plan["root_predicate_ref"]),
        parents=tuple(dict(row) for row in plan.get("parents", ())),
        expected_operation_ids=tuple(
            sorted(row["operation_id"] for row in expected)
        ),
        actual_rule_ids=tuple(sorted(actual_by_rule)),
        operations=tuple(operation_rows),
        root_contrasts=root_rows,
        parent_contrasts=parent_rows,
        unissued=tuple(dict(row) for row in plan.get("unissued", ())),
        minority=tuple(minority), anti_join=anti,
        receipt_refs=receipt_refs, handoff_refs=handoff_refs,
        fact_refs=fact_refs, source_release_refs=releases,
    )
