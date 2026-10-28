"""Bounded streaming execution for the accepted SRC04 native workload.

The ordinary builder is retained for fixture-sized/review workloads.  The
durable original product is large enough that retaining every constructed
query and every aggregate cell at once is not a responsible 16 GiB operation.
This adapter constructs each existing ``EmpiricalQuerySpec`` immediately before
it calls the existing I03 ``execute_empirical_query`` owner, writes one
aggregate operation receipt at a time, and keeps only the base/consumer facts.
It does not create a second query engine, a new release, or source payload.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from campaign_src04_completion.empirical.native_workload import (
    NativeOperation,
    NativeWorkload,
    NativeWorkloadRefusal,
    TargetView,
    WorkloadPolicy,
    _branch_predicate_ast,
    _condition_members,
    _condition_predicate_ast,
    _make_predicate,
    _make_query,
    _operation_id,
    _target_views,
)
from rawlsing_next.pre553_c11_integrity import RespondentIdentity
from rawlsing_next.pre553_c11_repository import C11LogicalRelease, C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref, semantic_hash
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_observed_response import (
    CO_OBSERVED_RESPONSE_RISK_SET,
    OBSERVED_RESPONSE_RISK_SET,
    ObservedResponseContract,
)

STREAMING_SCHEMA = "PYAT_SRC04_NATIVE_OBSERVED_RESPONSE_STREAMING_RESULT@1.0.0"


@dataclass
class StreamingNativeResult:
    workload: NativeWorkload
    receipt_path: Path
    receipt_sha256: str
    accounting: Mapping[str, Any]

    def return_projection(self) -> dict[str, Any]:
        return {
            "schema": STREAMING_SCHEMA,
            "contract_ref": self.workload.contract_ref.as_dict(),
            "release_ref": self.workload.release_ref.as_dict() if self.workload.release_ref else None,
            "policy": {
                "policy_id": self.workload.policy.policy_id,
                "families": list(self.workload.policy.families),
                "max_arity": self.workload.policy.max_arity,
            },
            "operation_receipt_path": str(self.receipt_path),
            "operation_receipt_sha256": self.receipt_sha256,
            "accounting": dict(self.accounting),
            "consumer_base_operation_id": next(
                (op.operation_id for op in self.workload.operations
                 if op.family == "UNARY_OBSERVED_DISTRIBUTION"), None),
            "consumer_condition_operation_id": next(
                (op.operation_id for op in self.workload.operations
                 if op.family == "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION"), None),
        }


def _set_fact(operation: NativeOperation, fact) -> None:
    operation.fact_ref = fact.ref
    operation.fact_state = fact.typed_state
    operation.raw_denominator = fact.raw_denominator_support
    operation.raw_numerator = fact.raw_numerator_support
    operation.cells = [
        {
            "cell": row["cell"],
            "raw_numerator_support": row["raw_numerator_support"],
            "cell_state": row["cell_state"],
        }
        for row in fact.target_topology.get("complete_cell_semantic_projection", ())
    ]
    operation.observed_ledger = dict(
        fact.target_topology.get("observed_response", {}).get("ledger", {})
    ) or None


def execute_native_workload_stream(
    *,
    repository: C11Repository,
    release_ref,
    contract: ObservedResponseContract,
    authority_registry: AuthorityRegistry,
    policy: WorkloadPolicy,
    receipt_path: str | Path,
    include_consumer_conditional: bool = True,
    progress_callback: Callable[[Mapping[str, Any]], None] | None = None,
    resume: bool = False,
) -> StreamingNativeResult:
    """Execute a declared finite family set with one aggregate receipt at a time.

    ``include_consumer_conditional`` issues exactly one ordinary conditional
    operation so the accepted Lane D consumer receives the same predicate/query
    shape it requires.  The joint family retains the complete same-person cell
    projection, which is the exact representation of both directional
    conditional distributions for every retained pair; the accounting states
    that representation explicitly rather than silently scaling a hidden value
    cross-product.
    """
    if not isinstance(repository, C11Repository):
        raise NativeWorkloadRefusal("C11_REPOSITORY_REQUIRED")
    release = repository.resolve_release_exact(exact_ref(release_ref, "release_ref"))
    if contract.contract_state != "AUTHORIZED" or contract.operation_authority_ref is None:
        raise NativeWorkloadRefusal("CONTRACT_NOT_AUTHORIZED_FOR_EXECUTION")
    if contract.release_ref is not None and contract.release_ref != release.release_ref:
        raise NativeWorkloadRefusal("CONTRACT_RELEASE_MISMATCH")
    if contract.source_artifact_ref != release.source_artifact_ref:
        raise NativeWorkloadRefusal("CONTRACT_SOURCE_ARTIFACT_MISMATCH")
    if contract.source_release_manifest_hash is not None and \
            contract.source_release_manifest_hash != release.source_release_manifest_hash:
        raise NativeWorkloadRefusal("CONTRACT_SOURCE_MANIFEST_MISMATCH")
    views = _target_views(release, contract)
    selected = tuple(view for view in views if view.observed_event_count > 0)
    shared_predicate = _make_predicate(
        contract, release, _branch_predicate_ast(contract, release), tag="release-scope")
    receipt_path = Path(receipt_path)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    family_counts: dict[str, int] = {}
    states: dict[str, int] = {}
    denominators: list[int] = []
    cells_total = 0
    base: NativeOperation | None = None
    condition_op: NativeOperation | None = None
    executed = 0
    refused = 0
    total = 0
    completed: set[str] = set()
    prior_base_record: Mapping[str, Any] | None = None
    prior_condition_record: Mapping[str, Any] | None = None
    if resume and receipt_path.exists():
        with receipt_path.open("r", encoding="utf-8") as prior_handle:
            for line in prior_handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = __import__("json").loads(line)
                except ValueError:
                    # A process kill can leave only the final receipt line
                    # incomplete.  Prior complete lines remain the checkpoint.
                    break
                operation_id = str(record.get("operation_id") or "")
                if not operation_id:
                    continue
                completed.add(operation_id)
                total += 1
                status = str(record.get("status") or "")
                counts[status] = counts.get(status, 0) + 1
                family = str(record.get("family") or "")
                family_counts[family] = family_counts.get(family, 0) + 1
                if status == "EXECUTED":
                    executed += 1
                    fact_state = str(record.get("fact_state") or "")
                    states[fact_state] = states.get(fact_state, 0) + 1
                    denominator = record.get("raw_denominator")
                    if isinstance(denominator, int):
                        denominators.append(denominator)
                    cells_total += len(record.get("cells") or ())
                    if prior_base_record is None and family == "UNARY_OBSERVED_DISTRIBUTION" \
                            and fact_state == "SUPPORTED":
                        prior_base_record = {
                            key: record.get(key) for key in (
                                "operation_id", "target_refs", "fact_ref", "fact_state",
                                "raw_denominator", "raw_numerator", "observed_ledger")
                        }
                        prior_base_record["cells"] = []
                    if prior_condition_record is None and family == "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION" \
                            and fact_state == "SUPPORTED":
                        prior_condition_record = {
                            key: record.get(key) for key in (
                                "operation_id", "target_refs", "condition_ref", "condition_state",
                                "condition_kind", "condition_value_ref", "condition_counts",
                                "fact_ref", "fact_state", "raw_denominator", "raw_numerator",
                                "observed_ledger")
                        }
                        prior_condition_record["cells"] = []
                elif status == "REFUSED":
                    refused += 1
        receipt_handle = receipt_path.open("a", encoding="utf-8")
    else:
        receipt_handle = receipt_path.open("w", encoding="utf-8")

    def emit(operation: NativeOperation) -> None:
        nonlocal base, condition_op, executed, refused, total, cells_total
        total += 1
        try:
            if operation.query is None or operation.predicate is None:
                operation.status = "BLOCKED_QUERY_NOT_CONSTRUCTED"
                refusal = operation.status
            else:
                result = execute_empirical_query(
                    repository=repository,
                    query=operation.query,
                    predicate=operation.predicate,
                    authority_registry=authority_registry,
                    release_refs=(release.release_ref,),
                )
                _set_fact(operation, result.facts[0])
                operation.status = "EXECUTED"
                executed += 1
                states[operation.fact_state] = states.get(operation.fact_state, 0) + 1
                if operation.raw_denominator is not None:
                    denominators.append(operation.raw_denominator)
                cells_total += len(operation.cells)
                if base is None and operation.family == "UNARY_OBSERVED_DISTRIBUTION" \
                        and operation.fact_state == "SUPPORTED":
                    base = operation
                if condition_op is None and operation.family == "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION" \
                        and operation.fact_state == "SUPPORTED":
                    condition_op = operation
                refusal = None
        except Exception as exc:  # exact refusal is evidence; never fabricate success
            operation.status = "REFUSED"
            operation.error = f"{type(exc).__name__}: {exc}"
            refused += 1
            refusal = operation.error
        counts[operation.status] = counts.get(operation.status, 0) + 1
        family_counts[operation.family] = family_counts.get(operation.family, 0) + 1
        receipt_handle.write(canonical_json(operation.receipt()) + "\n")
        receipt_handle.flush()
        if total % 100 == 0:
            if progress_callback is not None:
                progress_callback({
                    "operations_total": total,
                    "executed_operations": executed,
                    "refused_operations": refused,
                    "family": operation.family,
                    "status": operation.status,
                    "fact_state": operation.fact_state,
                })

    if "UNARY_OBSERVED_DISTRIBUTION" in policy.families:
        for view in selected:
            operation_id = _operation_id("UNARY_OBSERVED_DISTRIBUTION", (view.target_ref,), None)
            if operation_id in completed:
                continue
            operation = NativeOperation(
                operation_id=operation_id,
                family="UNARY_OBSERVED_DISTRIBUTION",
                target_refs=(view.target_ref,),
                condition_ref=None,
                condition_state=None,
                condition_kind=None,
                condition_value_ref=None,
                predicate=shared_predicate,
                status="CONSTRUCTED",
            )
            operation.query = _make_query(
                contract=contract, views=(view,), predicate=shared_predicate,
                risk_set_type=OBSERVED_RESPONSE_RISK_SET,
                tag=f"unary:{operation.operation_id}")
            emit(operation)

    if "SAME_RESPONDENT_JOINT_DISTRIBUTION" in policy.families and policy.max_arity >= 2:
        for left_index, left in enumerate(selected):
            for right in selected[left_index + 1:]:
                operation_id = _operation_id(
                    "SAME_RESPONDENT_JOINT_DISTRIBUTION",
                    (left.target_ref, right.target_ref), None)
                if operation_id in completed:
                    continue
                operation = NativeOperation(
                    operation_id=operation_id,
                    family="SAME_RESPONDENT_JOINT_DISTRIBUTION",
                    target_refs=(left.target_ref, right.target_ref),
                    condition_ref=None,
                    condition_state=None,
                    condition_kind=None,
                    condition_value_ref=None,
                    predicate=shared_predicate,
                    status="CONSTRUCTED",
                )
                operation.query = _make_query(
                    contract=contract, views=(left, right), predicate=shared_predicate,
                    risk_set_type=CO_OBSERVED_RESPONSE_RISK_SET,
                    tag=f"joint:{operation.operation_id}")
                emit(operation)

    if include_consumer_conditional:
        found = False
        for target in selected:
            for condition_target in selected:
                if condition_target.target_ref == target.target_ref:
                    continue
                for condition in condition_target.conditions:
                    operation_id = _operation_id(
                        "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION",
                        (target.target_ref,), condition)
                    if operation_id in completed:
                        found = True
                        break
                    member_refs, condition_counts = _condition_members(
                        release, condition_target, condition, contract, target.target_ref)
                    operation = NativeOperation(
                        operation_id=operation_id,
                        family="BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION",
                        target_refs=(target.target_ref,),
                        condition_ref=condition_target.target_ref,
                        condition_state=condition.get("state"),
                        condition_kind=condition.get("kind"),
                        condition_value_ref=condition.get("value_ref"),
                        condition_counts=condition_counts,
                        status="CONSTRUCTED",
                    )
                    ast = _condition_predicate_ast(
                        contract, condition_target, condition, member_refs, target.target_ref)
                    operation.predicate = _make_predicate(
                        contract, release, ast, tag=f"conditional:{operation.operation_id}")
                    operation.query = _make_query(
                        contract=contract, views=(target,), predicate=operation.predicate,
                        risk_set_type=OBSERVED_RESPONSE_RISK_SET,
                        tag=f"conditional:{operation.operation_id}",
                        condition_counts=condition_counts)
                    emit(operation)
                    found = True
                    break
                if found:
                    break
            if found:
                break
    # On a resumed run the completed base/consumer operations are already in
    # the durable receipt; reconstruct only their exact QuerySpec/Predicate
    # objects (without re-executing them) so the accepted Lane D consumer still
    # receives the original producer shape.
    if base is None and prior_base_record is not None:
        record = prior_base_record
        target_ref = exact_ref(record["target_refs"][0], "target_refs[0]")
        view = next((item for item in selected if item.target_ref == target_ref), None)
        if view is not None:
            base = NativeOperation(
                operation_id=str(record["operation_id"]),
                family="UNARY_OBSERVED_DISTRIBUTION",
                target_refs=(target_ref,),
                condition_ref=None,
                condition_state=None,
                condition_kind=None,
                condition_value_ref=None,
                predicate=shared_predicate,
                status="EXECUTED",
                fact_ref=exact_ref(record["fact_ref"], "fact_ref"),
                fact_state="SUPPORTED",
                raw_denominator=record.get("raw_denominator"),
                raw_numerator=record.get("raw_numerator"),
                cells=list(record.get("cells") or ()),
                observed_ledger=record.get("observed_ledger"),
            )
            base.query = _make_query(
                contract=contract, views=(view,), predicate=shared_predicate,
                risk_set_type=OBSERVED_RESPONSE_RISK_SET,
                tag=f"unary:{base.operation_id}")
    if condition_op is None and include_consumer_conditional and prior_condition_record is not None:
        record = prior_condition_record
        target_ref = exact_ref(record["target_refs"][0], "target_refs[0]")
        condition_ref = exact_ref(record["condition_ref"], "condition_ref")
        target = next((item for item in selected if item.target_ref == target_ref), None)
        condition_target = next((item for item in selected if item.target_ref == condition_ref), None)
        if target is not None and condition_target is not None:
            wanted_value_ref = record.get("condition_value_ref")
            wanted_state = record.get("condition_state")
            condition = None
            for candidate in condition_target.conditions:
                if wanted_value_ref is not None:
                    if candidate.get("value_ref") is not None \
                            and exact_ref(candidate["value_ref"], "condition.value_ref") == exact_ref(
                                wanted_value_ref, "condition_value_ref"):
                        condition = candidate
                        break
                elif wanted_state is not None and candidate.get("state") == wanted_state:
                    condition = candidate
                    break
            if condition is not None:
                member_refs, condition_counts = _condition_members(
                    release, condition_target, condition, contract, target.target_ref)
                operation = NativeOperation(
                    operation_id=str(record["operation_id"]),
                    family="BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION",
                    target_refs=(target.target_ref,),
                    condition_ref=condition_target.target_ref,
                    condition_state=condition.get("state"),
                    condition_kind=condition.get("kind"),
                    condition_value_ref=condition.get("value_ref"),
                    condition_counts=condition_counts,
                    status="EXECUTED",
                    fact_ref=exact_ref(record["fact_ref"], "fact_ref"),
                    fact_state="SUPPORTED",
                    raw_denominator=record.get("raw_denominator"),
                    raw_numerator=record.get("raw_numerator"),
                    cells=list(record.get("cells") or ()),
                    observed_ledger=record.get("observed_ledger"),
                )
                operation.predicate = _make_predicate(
                    contract, release,
                    _condition_predicate_ast(contract, condition_target, condition, member_refs, target.target_ref),
                    tag=f"conditional:{operation.operation_id}")
                operation.query = _make_query(
                    contract=contract, views=(target,), predicate=operation.predicate,
                    risk_set_type=OBSERVED_RESPONSE_RISK_SET,
                    tag=f"conditional:{operation.operation_id}",
                    condition_counts=condition_counts)
                condition_op = operation
    receipt_handle.close()
    import hashlib
    receipt_sha = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    conditional_target_pairs = len(selected) * (len(selected) - 1)
    conditional_values = sum(
        len(condition_target.conditions)
        for target in selected for condition_target in selected
        if condition_target.target_ref != target.target_ref
    )
    accounting = {
        "selected_observed_targets": len(selected),
        "contract_target_refs": len(contract.target_refs),
        "held_or_unobserved_targets": len(contract.target_refs) - len(selected),
        "operations_total": total,
        "operations_by_family": dict(sorted(family_counts.items())),
        "operations_by_status": dict(sorted(counts.items())),
        "executed_operations": executed,
        "refused_operations": refused,
        "supported_facts": states.get("SUPPORTED", 0),
        "fact_states": dict(sorted(states.items())),
        "raw_denominator_min": min(denominators) if denominators else None,
        "raw_denominator_max": max(denominators) if denominators else None,
        "aggregate_cells_retained": cells_total,
        "conditional_target_ordered_pairs": conditional_target_pairs,
        "conditional_value_instances_represented_in_joint_cells": conditional_values,
        "conditional_representation": (
            "BOTH_DIRECTIONS_EXACTLY_DERIVABLE_FROM_SAME_RESPONDENT_JOINT_CELL_PROJECTIONS"),
        "separate_conditional_operations_issued_for_consumer": (
            1 if condition_op is not None else 0),
        "routing_conditions_used": 0,
        "routing_state": "ROUTING_NOT_USED_FOR_OBSERVED_RESPONSE_EXECUTION_VIEW",
        "receipt_scope": "EXACT_OPERATION_FACTS_ONLY_NO_RESPONDENT_ROWS",
        "receipt_sha256": receipt_sha,
        "receipt_line_count": total,
    }
    operations = tuple(op for op in (base, condition_op) if op is not None)
    workload = NativeWorkload(
        contract_ref=contract.ref,
        release_ref=release.release_ref,
        policy=policy,
        targets=views,
        operations=operations,
        accounting=accounting,
    )
    return StreamingNativeResult(
        workload=workload,
        receipt_path=receipt_path,
        receipt_sha256=receipt_sha,
        accounting=accounting,
    )


__all__ = ["StreamingNativeResult", "execute_native_workload_stream"]
