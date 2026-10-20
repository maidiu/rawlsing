"""R50 G50 generic finite semantic-typed prospective operation enumerator.

Emits every candidate operation from a frozen synthetic SourceDecisionBundle and a
proposal ScientificGrammarPolicy without inspecting respondent outcomes. The
E_pre root is a sourcefree symbolic proposal root, never an original survey
U/E_pre count.
"""
from __future__ import annotations

from itertools import combinations, permutations, product
from typing import Iterable

from rawlsing_next.pre553_empirical_objects import semantic_hash

from .types import (
    ScientificFrontier, ScientificGrammarPolicy, ScientificOperation,
    SourceDecisionBundle, make_operation,
)
from .native_map import NATIVE_PREFIX, native_rule_key

STATE_NATIVE_UNSUPPORTED = "SPEC_ONLY_NATIVE_UNSUPPORTED"
NATIVE_I05 = "I05_EXACT"


def _first_reason(pairs: Iterable[tuple[str, str]]) -> tuple[str, list[str]]:
    disposition, reasons = next(iter(pairs))
    return disposition, [reasons]


def role_disposition(
    bundle: SourceDecisionBundle,
    policy: ScientificGrammarPolicy,
    *,
    targets: tuple[str, ...],
    conditions: tuple[tuple[str, int], ...],
    topology: str = "SCALAR_SINGULAR",
    measure: str = "SAMPLE",
    class_name: str = "DIST",
    condition_mode: str = "AND",
    branch_depth: int = 0,
) -> tuple[str, list[str]]:
    """Return (disposition, reasons) from frozen records only; never outcomes."""

    items = {item.item_id: item for item in bundle.items}
    if not targets:
        return "PROHIBITED", ["NO_TARGET"]
    if any(t in policy.denied_roles for t in targets):
        return "PROHIBITED", ["ADMINISTRATIVE_TARGET_DENIED"]
    if any(c in policy.denied_roles for c, _ in conditions):
        return "PROHIBITED", ["ADMINISTRATIVE_CONDITIONER_DENIED"]
    if any(t not in items or not items[t].target_role for t in targets):
        return "PROHIBITED", ["TARGET_ROLE_DENIED"]
    if any(c not in items or not items[c].conditioner_role for c, _ in conditions):
        return "PROHIBITED", ["CONDITIONER_ROLE_DENIED"]
    if set(targets) & {c for c, _ in conditions}:
        return "PROHIBITED", ["TARGET_LEAKAGE"]
    if len({c for c, _ in conditions}) != len(conditions):
        return "PROHIBITED", ["REDUNDANT_CONDITION"]
    used = [items[t] for t in targets] + [items[c] for c, _ in conditions]
    if len({i.scope for i in used}) != 1:
        return "PROHIBITED", ["UNLINKED_SOURCE"]
    if len({i.unit for i in used}) != 1:
        return "UNRESOLVED_SCIENCE", ["UNRESOLVED_UNIT_LINK"]
    if any(i.route_state != "KNOWN" for i in used):
        return "UNRESOLVED_SCIENCE", ["UNKNOWN_ROUTING_NONPROMOTION"]
    if not set.intersection(*(set(i.forms) for i in used)):
        return "INAPPLICABLE_PROVED", ["DISJOINT_ADMINISTRATION"]
    if topology != "SCALAR_SINGULAR" or any(i.topology != "SCALAR_SINGULAR" for i in used):
        return "UNSUPPORTED_RUNTIME", ["UNSANCTIONED_TOPOLOGY_OBLIGATION"]
    if class_name in policy.separate_classes:
        return "DEFERRED", ["METHOD_GATED_CLASS:" + class_name]
    if class_name not in policy.allowed_classes:
        return "PROHIBITED", ["CLASS_NOT_ALLOWED:" + class_name]
    if measure == "POPULATION" and policy.population_requires_weight:
        plan = next((p for p in bundle.measure_plans if p.kind == "POPULATION"), None)
        if plan is None or not plan.weight_ref:
            return "UNRESOLVED_SCIENCE", ["HOLD_POPULATION_WITHOUT_WEIGHT_OR_DESIGN"]
    if not getattr(policy, "reverse_authorized", False) and any(c == "Y" for c, _ in conditions):
        return "PROHIBITED", ["REVERSE_ROLE_RISK_NOT_AUTHORIZED"]
    if condition_mode == "XOR_EXACTLY_ONE" and len(conditions) != 2:
        return "PROHIBITED", ["XOR_REQUIRES_TWO_ATOM_GROUPS"]
    if branch_depth > int(policy.bounds["D"]):
        return "DEFERRED", ["DEPTH_BEYOND_ISSUED_BOUND"]
    return "ELIGIBLE", []


def _native_support(op: ScientificOperation) -> str:
    key = native_rule_key(op)
    return NATIVE_PREFIX + key if key else "POLICY_ONLY"


def enumerate_frontier(
    bundle: SourceDecisionBundle,
    policy: ScientificGrammarPolicy,
    *,
    budget: int | None = None,
) -> ScientificFrontier:
    bundle.require_version()
    policy.require_version()
    if budget is not None and (type(budget) is not int or budget < 0):
        raise ValueError("BUDGET_MUST_BE_NONNEGATIVE_INTEGER")

    j = int(policy.bounds["J"])
    k = int(policy.bounds["K"])
    d = int(policy.bounds["D"])
    items = {item.item_id: item for item in bundle.items}
    target_pool = sorted(
        item_id for item_id, item in items.items()
        if item.target_role and item_id in policy.target_roles
        and item_id not in policy.denied_roles
    )
    conditioner_pool = sorted(
        item_id for item_id, item in items.items()
        if item.conditioner_role and item_id in policy.conditioner_roles
        and item_id not in policy.denied_roles
    )

    ledger: dict[str, ScientificOperation] = {}
    aliases: dict[str, set[str]] = {}

    def record(op: ScientificOperation) -> None:
        key = op.op_id
        if key not in ledger:
            ledger[key] = op
            aliases.setdefault(key, set()).update(op.aliases)
        else:
            aliases[key].update(op.aliases)
            previous = ledger[key]
            if op.disposition == "ELIGIBLE" and previous.disposition != "ELIGIBLE":
                ledger[key] = op

    def add(
        class_name: str,
        targets: tuple[str, ...],
        conditions: tuple[tuple[str, int], ...] = (),
        *,
        condition_mode: str = "AND",
        measure: str = "SAMPLE",
        state_variant: str = "COMPLETE_RESPONSE",
        branch_depth: int = 0,
        alias: str | None = None,
    ) -> ScientificOperation:
        disposition, reasons = role_disposition(
            bundle, policy, targets=targets, conditions=conditions,
            class_name=class_name, condition_mode=condition_mode,
            measure=measure, branch_depth=branch_depth,
        )
        op = make_operation(
            bundle=bundle, policy=policy, claim_class=class_name, targets=targets,
            conditions=conditions, condition_mode=condition_mode,
            unit=items[targets[0]].unit if targets else "adult",
            measure=measure, topology="SCALAR_SINGULAR", state_variant=state_variant,
            branch_depth=branch_depth, disposition=disposition, reasons=tuple(reasons),
            native_support="PENDING",
            aliases=((alias,) if alias else ()),
        )
        native = _native_support(op) if disposition == "ELIGIBLE" else "NONE"
        op = ScientificOperation(**{**{name: getattr(op, name) for name in op.__dataclass_fields__},
                                   "native_support": native})
        record(op)
        return op

    # Main finite grammar: ordered target tuples, bounded condition conjunctions.
    for arity in range(1, min(j, len(target_pool)) + 1):
        for targets in permutations(target_pool, arity):
            remaining = [x for x in conditioner_pool if x not in targets]
            for depth in range(0, min(k, len(remaining)) + 1):
                for chosen in combinations(remaining, depth):
                    for values in product(*(items[c].domain for c in chosen)):
                        conditions = tuple(zip(chosen, values))
                        if depth == 0:
                            if arity == 1:
                                add("DIST", targets)
                            else:
                                add("JOINT", targets)
                                add("CO_TRAVEL", targets)
                        else:
                            if arity == 1:
                                parent = add("CONDITIONAL", targets, conditions)
                                if depth >= 2 and depth - 1 <= d:
                                    add("FORK", targets, conditions,
                                        branch_depth=depth - 1, alias=parent.op_id)
                            else:
                                add("JOINT", targets, conditions)
                                add("CO_TRAVEL", targets, conditions)
                            if depth >= 2:
                                add("INTERACTION", targets, conditions)
                            if depth == 2 and condition_mode_allows_xor(conditions):
                                add("INTERACTION", targets, conditions,
                                    condition_mode="XOR_EXACTLY_ONE")

    # Explicit hostile/typed ledger entries (accounted, not silently dropped).
    add("DIST", ("ID",))
    add("CONDITIONAL", ("Y",), (("ID", 1),))
    add("JOINT", ("Y", "H"))
    add("CONDITIONAL", ("Y",), (("RT", 1),))
    add("JOINT", ("X1", "X2"))
    for unsupported in ("SET", "RANK", "REP"):
        add("JOINT", ("Y", unsupported))
    add("CONDITIONAL", ("A",), (("Y", 1),))  # reverse role
    add("DIST", ("Y",), measure="POPULATION")
    add("STATE_ROBUSTNESS", ("Y",), state_variant="SPECIAL_STATES_PRESERVED")
    add("STATE_ROBUSTNESS", ("Y",), state_variant="SAMPLE_MEASURE_VARIANT")

    # Separately method-gated capability declarations.
    for class_name in policy.separate_classes:
        add(class_name, ("Y",))

    # Conservative static disposition for the synthetic fixture: the declared
    # SCIENTIFIC policy is proposal-grade, so even eligible operations are not
    # current source permission and not native execution permission.
    ordered = tuple(sorted(ledger.values(), key=lambda op: (op.op_id, op.disposition)))
    ordered = tuple(
        ScientificOperation(
            **{**{name: getattr(op, name) for name in op.__dataclass_fields__},
               "aliases": tuple(sorted(aliases.get(op.op_id, ())))}
        ) for op in ordered
    )

    eligible = tuple(op for op in ordered if op.disposition == "ELIGIBLE")
    disposition_counts: dict[str, int] = {}
    class_counts: dict[str, int] = {}
    for op in ordered:
        disposition_counts[op.disposition] = disposition_counts.get(op.disposition, 0) + 1
        if op.disposition == "ELIGIBLE":
            class_counts[op.claim_class] = class_counts.get(op.claim_class, 0) + 1

    if bundle.inventory_complete:
        u_item_root = semantic_hash({
            "items": sorted((i.item_id, i.forms, i.domain, i.administered) for i in bundle.items),
            "edition": bundle.edition, "source_sha256": bundle.source_sha256,
        })
        u_unit_root = semantic_hash({
            "units": sorted({i.unit for i in bundle.items}),
            "transforms": sorted(bundle.unit_transforms),
        })
        u_app_root = semantic_hash({
            "route_states": sorted(bundle.route_states),
            "state_map": sorted(bundle.state_map.items()),
            "risk_set_ref": bundle.risk_set_ref,
        })
        e_pre_root = semantic_hash({
            "bundle": bundle.content_hash, "policy": policy.content_hash,
            "eligible": [op.op_id for op in eligible],
        })
        e_pre_count = len(eligible)
        e_pre_cause = None
    else:
        u_item_root = u_unit_root = u_app_root = None
        e_pre_root = None
        e_pre_count = None
        e_pre_cause = "INCOMPLETE_DECLARED_ADMINISTERED_INVENTORY:" + ",".join(bundle.inventory_gaps)

    deferred = tuple(
        {"class": c, "reason": "METHOD_GATED_OR_BOUNDED", "trigger": "COMPETENT_METHOD_ISSUANCE"}
        for c in policy.separate_classes
    ) + (
        {"kind": "ARITY_DEFERRED", "beyond": {"J": j, "K": k, "D": d},
         "trigger": "ISSUED_RELEASE_EXPANSION", "capability": "higher-order/J-K-D expansion"},
    )

    pending = ()
    budget_state = "COMPLETE"
    if budget is not None and len(eligible) > budget:
        budget_state = "PARTIAL"
        pending = tuple(op.op_id for op in eligible[budget:])

    return ScientificFrontier(
        schema="ScientificFrontier@candidate1",
        bundle_id=bundle.bundle_id,
        bundle_hash=bundle.content_hash,
        policy_id=policy.policy_id,
        policy_hash=policy.content_hash,
        policy_grade=policy.grade,
        source_identity={
            "source_id": bundle.source_id, "wave": bundle.wave,
            "edition": bundle.edition, "source_sha256": bundle.source_sha256,
            "scope": bundle.scope,
        },
        u_item_root=u_item_root, u_unit_root=u_unit_root, u_app_root=u_app_root,
        e_pre_count=e_pre_count, e_pre_root=e_pre_root, e_pre_cause=e_pre_cause,
        operations=ordered,
        class_counts=dict(sorted(class_counts.items())),
        disposition_counts=dict(sorted(disposition_counts.items())),
        deferred=deferred,
        unknown=(),
        excluded=tuple(
            {"op_id": op.op_id, "class": op.claim_class, "disposition": op.disposition,
             "reasons": list(op.reasons)}
            for op in ordered if op.disposition in {"PROHIBITED", "INAPPLICABLE_PROVED"}
        ),
        budget_state=budget_state,
        pending_operation_ids=pending,
        maximum_bounds={"J": j, "K": k, "D": d},
    )


def condition_mode_allows_xor(conditions: tuple[tuple[str, int], ...]) -> bool:
    return len(conditions) == 2 and conditions[0][0] != conditions[1][0]


__all__ = ["enumerate_frontier", "role_disposition", "condition_mode_allows_xor",
           "NATIVE_I05", "STATE_NATIVE_UNSUPPORTED"]
