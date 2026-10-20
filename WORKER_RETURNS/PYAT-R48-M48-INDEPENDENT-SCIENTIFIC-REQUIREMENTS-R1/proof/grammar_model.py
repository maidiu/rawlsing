"""Executable sourcefree constitutional model; no native lowering or issuance.

Only declarative synthetic metadata enters generation. The evaluator accepts
synthetic rows separately. This module opens no source and imports no product.
"""
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product


@dataclass(frozen=True)
class Item:
    name: str
    domain: tuple
    unit: str = "adult"
    scope: str = "fixture-wave"
    target: bool = True
    conditioner: bool = True
    route: str = "KNOWN"
    topology: str = "SCALAR"
    forms: frozenset = frozenset({"F"})
    semantic_state: str = "UNRESOLVED"


@dataclass(frozen=True)
class Operation:
    targets: tuple[str, ...]
    conditions: tuple[tuple[str, int], ...]
    measure: str = "SAMPLE"
    claim: str = "DESCRIPTIVE"


def eligibility(op, catalog, *, weighted_plan=False):
    """Return independent scientific disposition, never permission to execute."""
    if op.claim != "DESCRIPTIVE":
        return "SEPARATE_CLAIM_AUTHORITY"
    if not op.targets or len(set(op.targets)) != len(op.targets):
        return "INVALID_TARGET"
    names = op.targets + tuple(n for n, _ in op.conditions)
    if any(n not in catalog for n in names):
        return "UNKNOWN_ITEM"
    if len({n for n, _ in op.conditions}) != len(op.conditions):
        return "REDUNDANT_CONDITION"
    if set(op.targets).intersection(n for n, _ in op.conditions):
        return "TARGET_LEAKAGE"
    if not all(catalog[n].target for n in op.targets):
        return "DENY_TARGET_ROLE"
    if not all(catalog[n].conditioner for n, _ in op.conditions):
        return "DENY_CONDITION_ROLE"
    items = tuple(catalog[n] for n in names)
    if len({i.scope for i in items}) != 1:
        return "UNLINKED_SOURCE"
    if len({i.unit for i in items}) != 1:
        return "UNRESOLVED_UNIT_LINK"
    if any(i.route != "KNOWN" for i in items):
        return "UNKNOWN_ROUTING"
    if not set.intersection(*(set(i.forms) for i in items)):
        return "DISJOINT_ADMINISTRATION"
    if any(i.topology != "SCALAR" for i in items):
        return "UNSUPPORTED_TOPOLOGY_OBLIGATION"
    if any(v not in catalog[n].domain for n, v in op.conditions):
        return "INVALID_CONDITION_CODE"
    if op.measure not in {"SAMPLE", "POPULATION"}:
        return "UNKNOWN_MEASURE"
    if op.measure == "POPULATION" and not weighted_plan:
        return "HOLD_POPULATION_MEASURE"
    return "ELIGIBLE"


def generate(catalog, *, k=2, j=3):
    if type(k) is not int or type(j) is not int or k < 0 or j < 1:
        raise ValueError("FINITE_NONNEGATIVE_K_POSITIVE_J_REQUIRED")
    names = tuple(sorted(catalog))
    if any(not i.domain or len(set(i.domain)) != len(i.domain) for i in catalog.values()):
        raise ValueError("FINITE_UNIQUE_NONEMPTY_DOMAIN_REQUIRED")
    ledger = {}
    for arity in range(1, min(j, len(names)) + 1):
        for targets in combinations(names, arity):
            rest = tuple(n for n in names if n not in targets)
            for depth in range(min(k, len(rest)) + 1):
                for conditions in combinations(rest, depth):
                    for values in product(*(catalog[n].domain for n in conditions)):
                        op = Operation(targets, tuple(zip(conditions, values)))
                        ledger[op] = eligibility(op, catalog)
    return ledger


def synthetic_distribution(op, catalog, rows, *, minimum=1):
    if eligibility(op, catalog) != "ELIGIBLE":
        raise ValueError("INELIGIBLE_SYNTHETIC_OPERATION")
    cells = {v: 0 for v in product(*(catalog[n].domain for n in op.targets))}
    selected = [r for r in rows if all(r[n] == v for n, v in op.conditions)]
    for row in selected:
        value = tuple(row[n] for n in op.targets)
        if value not in cells:
            raise ValueError("UNDECLARED_SYNTHETIC_TARGET_CODE")
        cells[value] += 1
    n = len(selected)
    return {
        "state": "VALID_EMPTY" if n == 0 else ("UNDERPOWERED" if n < minimum else "DESCRIPTIVE"),
        "n": n, "cells": cells,
        "probabilities": {c: Fraction(v, n) if n else None for c, v in cells.items()},
        "validation": "NOT_VALIDATED", "actor_belief": None,
    }


def pending_estate(waves):
    if len(waves) != 35 or len(set(waves)) != 35:
        raise ValueError("EXACT35_REQUIRED")
    return {w: {"original_U_count": None, "original_E_pre_count": None,
                "cause": "SOURCE_SPECIFIC_SCIENCE_UNISSUED",
                "E_exec_count": 0, "grade": "PENDING_NOT_ORIGINAL"} for w in sorted(waves)}


def execution_admission(*, current_source_grant=False):
    return "PERMISSION_CHECK_ONLY_NOT_NATIVE_EXECUTION" if current_source_grant else "SOURCE_HOST_PURPOSE_HOLD"
