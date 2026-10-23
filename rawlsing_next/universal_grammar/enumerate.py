"""R61 prospective finite symbolic frontier enumeration.

Enumeration is driven only by a frozen typed inventory and grammar policy. It
never reads respondent values and never lets a value, item label or population
count select frontier membership.
"""
from __future__ import annotations

from itertools import permutations, product
from typing import Any, Iterable, Iterator, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import semantic_hash

from .types import (
    ADMINISTERED, ADMINISTRATION_UNKNOWN, DEFERRED, ELIGIBLE,
    EXECUTION_STATES, FRONTIER_SCHEMA, HELD, INAPPLICABLE_PROVED, NOT_ADMINISTERED,
    PENDING, PARTITION_SCHEMA, PROHIBITED, RESULT_STATES, UNKNOWN,
    UNSUPPORTED_RUNTIME, FrontierPartition, GrammarPolicy, HeldRecord,
    InventoryLedgerEntry, MeasurePlan, Occurrence, OccurrenceKey,
    ScientificFrontier, ScientificOperation, SourceInventory, content_hash,
    make_operation,
)

DEFAULT_PARTITION_SIZE = 64


def _sorted_occurrences(occurrences: Iterable[Occurrence]) -> list[Occurrence]:
    return sorted(occurrences, key=lambda occurrence: occurrence.key.key)


def inventory_ledger(
    inventory: SourceInventory, policy: GrammarPolicy
) -> tuple[InventoryLedgerEntry, ...]:
    """Account for every frozen occurrence, including nonsemantic exclusions."""

    held_by_id: dict[str, HeldRecord] = {}
    for record in inventory.held_records:
        held_by_id[record.occurrence_id] = record
    entries: list[InventoryLedgerEntry] = []
    for occurrence in _sorted_occurrences(inventory.occurrences):
        identity = occurrence.occurrence_id
        held_reason = None
        held_authority = None
        if occurrence.administrative_role is not None:
            disposition, reasons = PROHIBITED, ("ADMINISTRATIVE_NONSEMANTIC",)
        elif occurrence.target_role is None and occurrence.conditioner_role is None:
            disposition, reasons = PROHIBITED, ("NO_SEMANTIC_ROLE",)
        elif occurrence.administration == NOT_ADMINISTERED:
            disposition, reasons = HELD, ("OCCURRENCE_NOT_ADMINISTERED",)
        elif occurrence.administration == ADMINISTRATION_UNKNOWN:
            disposition, reasons = UNKNOWN, ("ADMINISTRATION_UNKNOWN",)
        elif identity in held_by_id or occurrence.key.key in held_by_id:
            record = held_by_id.get(identity) or held_by_id[occurrence.key.key]
            if record.structured and record.authority_ref:
                disposition = HELD
                reasons = ("HELD_BY_STRUCTURED_OWNER_RECORD",)
                held_reason = record.reason
                held_authority = record.authority_ref
            else:
                disposition = UNKNOWN
                reasons = ("UNSTRUCTURED_HELD_CLAIM_NOT_AUTHORIZATION",)
                held_reason = record.reason
        elif not (
            (occurrence.target_role is not None and occurrence.target_role in policy.target_roles)
            or (
                occurrence.conditioner_role is not None
                and occurrence.conditioner_role in policy.conditioner_roles
            )
        ):
            disposition, reasons = PROHIBITED, ("ROLE_NOT_AUTHORIZED",)
        else:
            disposition, reasons = ELIGIBLE, ()
        entries.append(InventoryLedgerEntry(
            occurrence_id=identity,
            target_role=occurrence.target_role,
            conditioner_role=occurrence.conditioner_role,
            administrative_role=occurrence.administrative_role,
            administration=occurrence.administration,
            disposition=disposition,
            reasons=tuple(reasons),
            held_reason=held_reason,
            held_authority_ref=held_authority,
        ))
    return tuple(entries)


def role_disposition(
    inventory: SourceInventory,
    policy: GrammarPolicy,
    *,
    targets: tuple[OccurrenceKey, ...],
    target_roles: tuple[str, ...],
    conditions: tuple[tuple[OccurrenceKey, Any], ...],
    conditioner_roles: tuple[str, ...],
    claim_class: str,
    condition_mode: str = "AND",
    measure: MeasurePlan | None = None,
    branch_depth: int = 0,
) -> tuple[str, tuple[str, ...], str | None]:
    """Return (disposition, reasons, common risk refs) from frozen records only."""

    if not targets:
        return PROHIBITED, ("NO_TARGET",), ()
    by_key = inventory.by_key()
    if any(key not in by_key for key in targets):
        return PROHIBITED, ("UNKNOWN_TARGET_OCCURRENCE",), ()
    if any(key not in by_key for key, _ in conditions):
        return PROHIBITED, ("UNKNOWN_CONDITIONER_OCCURRENCE",), ()
    used_targets = [by_key[key] for key in targets]
    used_conditions = [by_key[key] for key, _ in conditions]
    used = used_targets + used_conditions
    held_by_id = {
        record.occurrence_id: record for record in inventory.held_records
        if record.structured and record.authority_ref
    }
    if any(
        item.occurrence_id in held_by_id or item.key.key in held_by_id for item in used
    ):
        return HELD, ("HELD_BY_STRUCTURED_OWNER_RECORD",), ()
    if any(item.administrative_role is not None for item in used):
        return PROHIBITED, ("ADMINISTRATIVE_ROLE_DENIED",), ()
    if any(item.target_role is None or item.target_role not in policy.target_roles for item in used_targets):
        return PROHIBITED, ("TARGET_ROLE_DENIED",), ()
    if any(
        item.conditioner_role is None or item.conditioner_role not in policy.conditioner_roles
        for item in used_conditions
    ):
        return PROHIBITED, ("CONDITIONER_ROLE_DENIED",), ()
    if len({key for key in targets}) != len(targets):
        return PROHIBITED, ("DUPLICATE_TARGET_OCCURRENCE",), ()
    if len({key for key, _ in conditions}) != len(conditions):
        return PROHIBITED, ("REDUNDANT_CONDITION",), ()
    target_items = {key.item_id for key in targets}
    if any(key.item_id in target_items for key, _ in conditions):
        return PROHIBITED, ("TARGET_LEAKAGE",), ()
    if len({item.scope for item in used}) != 1:
        return PROHIBITED, ("UNLINKED_SOURCE",), ()
    if len({item.unit for item in used}) != 1:
        return HELD, ("UNRESOLVED_UNIT_LINK",), ()
    if any(not item.risk_set_refs for item in used):
        if policy.risk_set_policy != "UNCONSTRAINED":
            return UNKNOWN, ("UNKNOWN_RISK_SET",), ()
        common_risk = ()
    else:
        common_risk = tuple(sorted(set.intersection(
            *(set(item.risk_set_refs) for item in used)
        )))
        if not common_risk:
            return INAPPLICABLE_PROVED, ("DISJOINT_RISK_SET",), ()
    if any(item.route_state != "KNOWN" for item in used):
        return HELD, ("UNKNOWN_ROUTING_NONPROMOTION",), common_risk
    if not set.intersection(*(set(item.forms) for item in used)):
        return INAPPLICABLE_PROVED, ("DISJOINT_ADMINISTRATION_FORM",), common_risk
    if any(item.administration == NOT_ADMINISTERED for item in used):
        return HELD, ("OCCURRENCE_NOT_ADMINISTERED",), common_risk
    if any(item.administration == ADMINISTRATION_UNKNOWN for item in used):
        return UNKNOWN, ("ADMINISTRATION_UNKNOWN",), common_risk
    if claim_class in policy.separate_classes:
        return HELD, ("METHOD_GATED_CLASS:" + claim_class,), common_risk
    if claim_class not in policy.allowed_classes:
        return PROHIBITED, ("CLASS_NOT_ALLOWED:" + claim_class,), common_risk
    if measure is None:
        return PROHIBITED, ("UNKNOWN_MEASURE",), common_risk
    if measure.kind == "POPULATION" and policy.population_requires_weight:
        if not measure.weight_ref or not measure.design_ref:
            return HELD, ("POPULATION_WITHOUT_WEIGHT_OR_DESIGN",), common_risk
    grant = policy.direction_for(target_roles, conditioner_roles, claim_class)
    if grant is None:
        return PROHIBITED, ("DIRECTION_NOT_GRANTED",), common_risk
    if condition_mode == "XOR_EXACTLY_ONE" and len(conditions) != 2:
        return PROHIBITED, ("XOR_REQUIRES_TWO_OCCURRENCES",), common_risk
    if branch_depth > int(policy.bounds["D"]):
        return HELD, ("DEPTH_BEYOND_ISSUED_BOUND",), common_risk
    return ELIGIBLE, (), common_risk


def _measure_plans(inventory: SourceInventory) -> tuple[MeasurePlan, ...]:
    return tuple(sorted(inventory.measure_plans, key=lambda plan: plan.measure_id))


def _record(
    ledger: dict[str, ScientificOperation],
    aliases: dict[str, set[str]],
    operation: ScientificOperation,
) -> ScientificOperation:
    key = operation.op_id
    if key not in ledger:
        ledger[key] = operation
        aliases.setdefault(key, set()).update(operation.aliases)
        return operation
    aliases[key].update(operation.aliases)
    if operation.disposition == ELIGIBLE and ledger[key].disposition != ELIGIBLE:
        ledger[key] = operation
        return operation
    return ledger[key]


def _add(
    ledger: dict[str, ScientificOperation],
    aliases: dict[str, set[str]],
    *,
    inventory: SourceInventory,
    policy: GrammarPolicy,
    claim_class: str,
    targets: tuple[OccurrenceKey, ...],
    target_roles: tuple[str, ...],
    conditions: tuple[tuple[OccurrenceKey, Any], ...] = (),
    conditioner_roles: tuple[str, ...] = (),
    condition_mode: str = "AND",
    measure: MeasurePlan,
    state_variant: str = "COMPLETE_RESPONSE",
    branch_depth: int = 0,
    recursion_depth: int = 0,
    baseline_ref: str | None = None,
    alias: str | None = None,
) -> ScientificOperation:
    disposition, reasons, risk_set_refs = role_disposition(
        inventory, policy, targets=targets, target_roles=target_roles,
        conditions=conditions, conditioner_roles=conditioner_roles,
        claim_class=claim_class, condition_mode=condition_mode,
        measure=measure, branch_depth=branch_depth,
    )
    grant = policy.direction_for(target_roles, conditioner_roles, claim_class)
    used = [inventory.by_key()[key] for key in targets] + [
        inventory.by_key()[key] for key, _ in conditions
    ]
    operation = make_operation(
        inventory=inventory, policy=policy, claim_class=claim_class,
        targets=targets, target_roles=target_roles, conditions=conditions,
        conditioner_roles=conditioner_roles, condition_mode=condition_mode,
        unit=used[0].unit, topology=used[0].topology, state_variant=state_variant,
        measure=measure, risk_set_ref=(risk_set_refs[0] if risk_set_refs else None),
        risk_set_refs=risk_set_refs,
        direction_ref=None if grant is None else grant.direction_ref,
        form_scope=sorted(set.intersection(*(set(item.forms) for item in used))),
        scope=used[0].scope, branch_depth=branch_depth,
        recursion_depth=recursion_depth, baseline_ref=baseline_ref,
        disposition=disposition, reasons=reasons,
        native_support="PENDING" if disposition == ELIGIBLE else "NOT_APPLICABLE",
        administration_states=sorted({item.administration for item in used}),
        aliases=((alias,) if alias else ()),
    )
    return _record(ledger, aliases, operation)


def _partition_material(partition_size: int, operation_ids: Sequence[str]) -> str:
    return semantic_hash({
        "schema": PARTITION_SCHEMA, "partition_size": partition_size,
        "operation_ids": list(operation_ids),
    })


def iter_partitions(
    frontier: ScientificFrontier, partition_size: int | None = None
) -> Iterator[FrontierPartition]:
    """Yield deterministic lazy partitions in stable operation-id order."""

    size = frontier.partition_size if partition_size is None else partition_size
    if not isinstance(size, int) or isinstance(size, bool) or size < 1:
        raise ValueError("PARTITION_SIZE_MUST_BE_POSITIVE_INTEGER")
    ids = tuple(sorted(op.op_id for op in frontier.operations))
    for index, start in enumerate(range(0, len(ids), size)):
        chunk = ids[start:start + size]
        yield FrontierPartition(
            schema=PARTITION_SCHEMA, index=index, partition_size=size,
            operation_ids=chunk, operation_count=len(chunk),
            root=_partition_material(size, chunk),
        )


def partition_frontier(
    frontier: ScientificFrontier, partition_size: int | None = None
) -> tuple[FrontierPartition, ...]:
    return tuple(iter_partitions(frontier, partition_size))


def conservation_report(
    frontier: ScientificFrontier,
    executed_ids: Iterable[str] | Mapping[str, Any],
) -> dict[str, Any]:
    """Independent whole-frontier membership anti-join.

    Counts never substitute for exact operation identities: replacing one
    expected operation with another while preserving the count is rejected.
    """

    expected_ids = tuple(op.op_id for op in frontier.operations)
    expected = set(expected_ids)
    received_list = list(executed_ids.keys() if isinstance(executed_ids, Mapping) else executed_ids)
    if not all(isinstance(value, str) for value in received_list):
        raise TypeError("executed_ids must contain exact operation id strings")
    counts: dict[str, int] = {}
    for value in received_list:
        counts[value] = counts.get(value, 0) + 1
    duplicates = tuple(sorted(value for value, count in counts.items() if count > 1))
    received = set(received_list)
    missing = tuple(sorted(expected - received))
    unexpected = tuple(sorted(received - expected))
    count_preserving_substitution = bool(
        len(received_list) == len(expected_ids) and (missing or unexpected)
    )
    return {
        "expected_count": len(expected_ids),
        "received_count": len(received_list),
        "missing_operation_ids": missing,
        "unexpected_operation_ids": unexpected,
        "duplicate_operation_ids": duplicates,
        "count_preserving_substitution": count_preserving_substitution,
        "no_drop_ok": not missing and not unexpected and not duplicates
        and len(received_list) == len(expected_ids),
    }


def enumerate_frontier(
    inventory: SourceInventory,
    policy: GrammarPolicy,
    *,
    budget: int | None = None,
    partition_size: int = DEFAULT_PARTITION_SIZE,
) -> ScientificFrontier:
    inventory.require_version()
    policy.require_version()
    if budget is not None and (type(budget) is not int or budget < 0):
        raise ValueError("BUDGET_MUST_BE_NONNEGATIVE_INTEGER")
    if not isinstance(partition_size, int) or isinstance(partition_size, bool) or partition_size < 1:
        raise ValueError("PARTITION_SIZE_MUST_BE_POSITIVE_INTEGER")

    by_key = inventory.by_key()
    measures = _measure_plans(inventory)
    if not measures:
        raise ValueError("inventory must declare at least one measure plan")
    default_measure = next(
        (measure for measure in measures if measure.kind == "SAMPLE"), measures[0]
    )
    target_pool = _sorted_occurrences(
        occurrence for occurrence in inventory.occurrences if occurrence.target_role is not None
    )
    conditioner_pool = _sorted_occurrences(
        occurrence for occurrence in inventory.occurrences if occurrence.conditioner_role is not None
    )
    j = int(policy.bounds["J"])
    k = int(policy.bounds["K"])
    d = int(policy.bounds["D"])

    ledger: dict[str, ScientificOperation] = {}
    aliases: dict[str, set[str]] = {}

    def add(
        claim_class: str,
        targets: tuple[OccurrenceKey, ...],
        conditions: tuple[tuple[OccurrenceKey, Any], ...] = (),
        *,
        condition_mode: str = "AND",
        measure: MeasurePlan,
        state_variant: str = "COMPLETE_RESPONSE",
        branch_depth: int = 0,
        recursion_depth: int = 0,
        baseline_ref: str | None = None,
        alias: str | None = None,
    ) -> ScientificOperation:
        target_roles = tuple(by_key[key].target_role for key in targets)  # type: ignore[misc]
        conditioner_roles = tuple(by_key[key].conditioner_role for key, _ in conditions)  # type: ignore[misc]
        return _add(
            ledger, aliases, inventory=inventory, policy=policy,
            claim_class=claim_class, targets=targets, target_roles=target_roles,
            conditions=conditions, conditioner_roles=conditioner_roles,
            condition_mode=condition_mode, measure=measure,
            state_variant=state_variant, branch_depth=branch_depth,
            recursion_depth=recursion_depth, baseline_ref=baseline_ref, alias=alias,
        )

    for arity in range(1, min(j, len(target_pool)) + 1):
        for targets in permutations(target_pool, arity):
            target_keys = tuple(item.key for item in targets)
            remaining = [item for item in conditioner_pool if item.key not in target_keys]
            max_depth = min(k, len(remaining))
            for depth in range(0, max_depth + 1):
                for chosen in permutations(remaining, depth):
                    condition_keys = tuple(item.key for item in chosen)
                    for values in product(*(item.domain for item in chosen)):
                        conditions = tuple(zip(condition_keys, values))
                        for measure in measures:
                            if depth == 0:
                                if arity == 1:
                                    add("DIST", target_keys, measure=measure)
                                else:
                                    add("JOINT", target_keys, measure=measure)
                                    add("CO_TRAVEL", target_keys, measure=measure)
                            else:
                                if arity == 1:
                                    parent = add("CONDITIONAL", target_keys, conditions,
                                                 measure=measure)
                                    if depth >= 2:
                                        add("FORK", target_keys, conditions,
                                            measure=measure, branch_depth=depth - 1,
                                            recursion_depth=depth - 1,
                                            baseline_ref=parent.op_id,
                                            alias=parent.op_id)
                                else:
                                    add("JOINT", target_keys, conditions, measure=measure)
                                    add("CO_TRAVEL", target_keys, conditions, measure=measure)
                                if depth >= 2:
                                    add("INTERACTION", target_keys, conditions, measure=measure)
                                    if len({key.item_id for key in condition_keys}) == 2:
                                        add("INTERACTION", target_keys, conditions,
                                            condition_mode="XOR_EXACTLY_ONE", measure=measure)
                        if depth == 0 and arity == 1:
                            add("STATE_ROBUSTNESS", target_keys, measure=default_measure,
                                state_variant="SPECIAL_STATES_PRESERVED")

    for occurrence in target_pool:
        for class_name in policy.separate_classes:
            add(class_name, (occurrence.key,), measure=default_measure)

    ordered = tuple(sorted(ledger.values(), key=lambda op: (op.op_id, op.disposition)))
    ordered = tuple(
        ScientificOperation(**{
            **{name: getattr(op, name) for name in op.__dataclass_fields__},
            "aliases": tuple(sorted(aliases.get(op.op_id, ()))),
        })
        for op in ordered
    )

    eligible = tuple(op for op in ordered if op.disposition == ELIGIBLE)

    operation_ids = tuple(sorted(op.op_id for op in ordered))
    pending = ()
    budget_state = "COMPLETE"
    if budget is not None and len(eligible) > budget:
        budget_state = "PARTIAL"
        pending = tuple(op.op_id for op in eligible[budget:])
    pending_set = set(pending)
    if pending_set:
        ordered = tuple(
            ScientificOperation(**{
                **{name: getattr(op, name) for name in op.__dataclass_fields__},
                "execution_state": PENDING if op.op_id in pending_set else op.execution_state,
            })
            for op in ordered
        )

    class_counts: dict[str, int] = {}
    disposition_counts: dict[str, int] = {}
    execution_counts: dict[str, int] = {}
    result_counts: dict[str, int] = {}
    for op in ordered:
        disposition_counts[op.disposition] = disposition_counts.get(op.disposition, 0) + 1
        execution_counts[op.execution_state] = execution_counts.get(op.execution_state, 0) + 1
        result_counts[op.result_state] = result_counts.get(op.result_state, 0) + 1
        if op.disposition == ELIGIBLE:
            class_counts[op.claim_class] = class_counts.get(op.claim_class, 0) + 1

    occurrence_ledger = inventory_ledger(inventory, policy)
    occurrence_counts: dict[str, int] = {}
    for entry in occurrence_ledger:
        occurrence_counts[entry.disposition] = occurrence_counts.get(entry.disposition, 0) + 1

    if inventory.inventory_complete:
        u_item_root = content_hash({
            "occurrences": [occurrence.material() for occurrence in _sorted_occurrences(inventory.occurrences)],
            "edition": inventory.edition, "source_sha256": inventory.source_sha256,
        })
        u_unit_root = content_hash({
            "units": sorted({occurrence.unit for occurrence in inventory.occurrences}),
            "transforms": sorted(inventory.unit_transforms),
        })
        u_app_root = content_hash({
            "risk_set_refs": sorted(inventory.risk_set_refs),
            "state_map": sorted(inventory.state_map.items()),
            "route_states": sorted({occurrence.route_state for occurrence in inventory.occurrences}),
        })
        e_pre_root = semantic_hash({
            "inventory": inventory.content_hash, "policy": policy.content_hash,
            "eligible": [op.op_id for op in eligible],
            "occurrence_ledger": [entry.material() for entry in occurrence_ledger],
        })
        e_pre_count = len(eligible)
        e_pre_cause = None
    else:
        u_item_root = u_unit_root = u_app_root = None
        e_pre_root = None
        e_pre_count = None
        e_pre_cause = "INCOMPLETE_DECLARED_INVENTORY:" + ",".join(inventory.inventory_gaps)

    deferred = tuple(
        {"class": class_name, "reason": "METHOD_GATED_OR_BOUNDED",
         "trigger": "COMPETENT_METHOD_ISSUANCE"}
        for class_name in policy.separate_classes
    ) + (
        {"kind": "ARITY_DEFERRED", "beyond": {"J": j, "K": k, "D": d},
         "trigger": "ISSUED_RELEASE_EXPANSION"},
    )

    partition_count = (len(operation_ids) + partition_size - 1) // partition_size

    return ScientificFrontier(
        schema=FRONTIER_SCHEMA,
        inventory_id=inventory.inventory_id,
        inventory_hash=inventory.content_hash,
        policy_id=policy.policy_id,
        policy_hash=policy.content_hash,
        policy_grade=policy.grade,
        source_identity={
            "source_id": inventory.source_id, "wave": inventory.wave,
            "edition": inventory.edition, "source_sha256": inventory.source_sha256,
            "scope": inventory.scope, "current_selection": inventory.current_selection,
        },
        operations=ordered,
        inventory_ledger=occurrence_ledger,
        class_counts=dict(sorted(class_counts.items())),
        disposition_counts=dict(sorted(disposition_counts.items())),
        execution_counts=dict(sorted(execution_counts.items())),
        result_counts=dict(sorted(result_counts.items())),
        deferred=deferred,
        unknown=tuple(
            op.material() for op in ordered if op.disposition == UNKNOWN
        ),
        excluded=tuple(
            {"op_id": op.op_id, "class": op.claim_class,
             "disposition": op.disposition, "reasons": list(op.reasons)}
            for op in ordered if op.disposition in {PROHIBITED, INAPPLICABLE_PROVED}
        ),
        budget_state=budget_state,
        pending_operation_ids=pending,
        partition_size=partition_size,
        partition_root=_partition_material(partition_size, operation_ids),
        partition_count=partition_count,
        maximum_bounds={"J": j, "K": k, "D": d},
        u_item_root=u_item_root,
        u_unit_root=u_unit_root,
        u_app_root=u_app_root,
        e_pre_count=e_pre_count,
        e_pre_root=e_pre_root,
        e_pre_cause=e_pre_cause,
    )


def condition_mode_allows_xor(conditions: Sequence[tuple[OccurrenceKey, Any]]) -> bool:
    return len(conditions) == 2 and conditions[0][0].item_id != conditions[1][0].item_id


__all__ = [
    "DEFAULT_PARTITION_SIZE", "inventory_ledger", "role_disposition",
    "enumerate_frontier", "iter_partitions", "partition_frontier",
    "conservation_report", "condition_mode_allows_xor",
]
