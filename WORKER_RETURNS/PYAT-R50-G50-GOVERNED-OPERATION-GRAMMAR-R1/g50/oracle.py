"""Independent expected-multiset oracle for the G50 symbolic frontier.

This module deliberately does not import the composer or its role function. It
re-derives the eligible operation set from the frozen bundle/policy with a
separate enumeration path and its own identity material, then exposes an
expected root for independent comparison.
"""
from __future__ import annotations

from itertools import combinations, permutations, product

from rawlsing_next.pre553_empirical_objects import semantic_hash

from .types import ScientificGrammarPolicy, SourceDecisionBundle


def _hash_identity(bundle, policy, *, claim_class, targets, conditions,
                   condition_mode, unit, measure, topology, state_variant, scope,
                   branch_depth):
    conds = [list(p) for p in conditions]
    if condition_mode == "AND":
        conds.sort(key=lambda p: (p[0], p[1]))
    return semantic_hash({
        "bundle": bundle.bundle_id, "policy": policy.policy_id,
        "class": claim_class, "targets": list(targets),
        "conditions": conds, "condition_mode": condition_mode,
        "unit": unit, "measure": measure, "topology": topology,
        "state_variant": state_variant, "scope": scope,
        "branch_depth": branch_depth,
    })


def _allowed(bundle, policy, *, targets, conditions, claim_class, condition_mode,
             measure, branch_depth):
    by_id = {i.item_id: i for i in bundle.items}
    if any(t in policy.denied_roles for t in targets):
        return False
    if any(c in policy.denied_roles for c, _ in conditions):
        return False
    if any(not by_id[t].target_role for t in targets):
        return False
    if any(not by_id[c].conditioner_role for c, _ in conditions):
        return False
    if set(targets) & {c for c, _ in conditions}:
        return False
    if len({c for c, _ in conditions}) != len(conditions):
        return False
    used = [by_id[t] for t in targets] + [by_id[c] for c, _ in conditions]
    if len({i.scope for i in used}) != 1 or len({i.unit for i in used}) != 1:
        return False
    if any(i.route_state != "KNOWN" or i.topology != "SCALAR_SINGULAR" for i in used):
        return False
    if not set.intersection(*(set(i.forms) for i in used)):
        return False
    if claim_class in policy.separate_classes or claim_class not in policy.allowed_classes:
        return False
    if measure == "POPULATION" and policy.population_requires_weight:
        return False
    if any(c == "Y" for c, _ in conditions):
        return False
    if condition_mode == "XOR_EXACTLY_ONE" and len(conditions) != 2:
        return False
    if branch_depth > int(policy.bounds["D"]):
        return False
    return True


def expected_eligible_ids(bundle: SourceDecisionBundle, policy: ScientificGrammarPolicy) -> list[str]:
    by_id = {i.item_id: i for i in bundle.items}
    target_pool = sorted(
        i for i, item in by_id.items()
        if item.target_role and i in policy.target_roles and i not in policy.denied_roles
    )
    cond_pool = sorted(
        i for i, item in by_id.items()
        if item.conditioner_role and i in policy.conditioner_roles
        and i not in policy.denied_roles
    )
    J, K = int(policy.bounds["J"]), int(policy.bounds["K"])
    ids: list[str] = []

    def emit(*, claim_class, targets, conditions=(), condition_mode="AND",
             measure="SAMPLE", state_variant="COMPLETE_RESPONSE", branch_depth=0):
        if not _allowed(bundle, policy, targets=targets, conditions=conditions,
                        claim_class=claim_class, condition_mode=condition_mode,
                        measure=measure, branch_depth=branch_depth):
            return
        unit = by_id[targets[0]].unit if targets else "adult"
        ids.append("urn:g50:op:" + _hash_identity(
            bundle, policy, claim_class=claim_class, targets=targets,
            conditions=conditions, condition_mode=condition_mode, unit=unit,
            measure=measure, topology="SCALAR_SINGULAR",
            state_variant=state_variant, scope=bundle.scope,
            branch_depth=branch_depth,
        ))

    for arity in range(1, min(J, len(target_pool)) + 1):
        for targets in permutations(target_pool, arity):
            rest = tuple(x for x in cond_pool if x not in targets)
            for depth in range(min(K, len(rest)) + 1):
                for chosen in combinations(rest, depth):
                    for values in product(*(by_id[c].domain for c in chosen)):
                        conds = tuple(zip(chosen, values))
                        if depth == 0:
                            emit(claim_class="DIST" if arity == 1 else "JOINT", targets=targets)
                            if arity > 1:
                                emit(claim_class="CO_TRAVEL", targets=targets)
                        else:
                            if arity == 1:
                                emit(claim_class="CONDITIONAL", targets=targets, conditions=conds)
                                if depth >= 2:
                                    emit(claim_class="FORK", targets=targets,
                                         conditions=conds, branch_depth=depth - 1)
                            else:
                                emit(claim_class="JOINT", targets=targets, conditions=conds)
                                emit(claim_class="CO_TRAVEL", targets=targets, conditions=conds)
                            if depth >= 2:
                                emit(claim_class="INTERACTION", targets=targets, conditions=conds)
                                if chosen[0] != chosen[1]:
                                    emit(claim_class="INTERACTION", targets=targets,
                                         conditions=conds, condition_mode="XOR_EXACTLY_ONE")

    # State variants that are scientifically eligible but not native-supported.
    emit(claim_class="STATE_ROBUSTNESS", targets=("Y",),
         state_variant="SPECIAL_STATES_PRESERVED")
    emit(claim_class="STATE_ROBUSTNESS", targets=("Y",),
         state_variant="SAMPLE_MEASURE_VARIANT")
    return sorted(ids)


def expected_epre_root(bundle: SourceDecisionBundle, policy: ScientificGrammarPolicy) -> str:
    return semantic_hash({
        "bundle": bundle.content_hash, "policy": policy.content_hash,
        "eligible": expected_eligible_ids(bundle, policy),
    })


__all__ = ["expected_eligible_ids", "expected_epre_root"]
