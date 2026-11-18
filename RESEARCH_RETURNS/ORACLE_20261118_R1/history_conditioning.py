"""Research implementation. Condition a finite forward life generator on a RAW I03 law.

All probabilities below refer to fictional generation or an explicitly selected
observed-sample target. No production authority, psychological law or actor write.
"""
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from math import lcm
from random import Random

from rawlsing_next.pre553_empirical_query import replay_empirical_query


def raw_joint(repository, query, predicate, registry, releases, expected_fact):
    """Recompute the exact fact under the caller's current query authority."""
    if query.requested_output_grain.get("measure_kind") != "RAW" or len(releases) != 1:
        raise ValueError("this reader supports single-release RAW only")
    result = replay_empirical_query(repository=repository, query=query, predicate=predicate,
                                    authority_registry=registry, release_refs=releases,
                                    expected_fact_refs=(expected_fact,))
    fact, = result.facts
    if fact.typed_state != "SUPPORTED" or fact.raw_denominator_support <= 0:
        raise ValueError(f"no supported observation law: {fact.typed_state}")
    cells = {}
    for entry in fact.target_topology["complete_cell_semantic_projection"]:
        key = entry["cell"]
        key = (key,) if isinstance(key, str) else tuple(key)
        if key in cells or len(key) != len(query.target_refs):
            raise ValueError("invalid ordered cell")
        cells[key] = Fraction(entry["raw_numerator_support"], fact.raw_denominator_support)
    if sum(cells.values()) != 1:
        raise ValueError("observation categories do not partition this risk set")
    return cells


@dataclass(frozen=True)
class Alternative:
    child: str
    probability: Fraction


class ConditionedHistories:
    """Finite prefix DAG. A node represents a complete future-relevant owner state.

    Leaves are whole-world continuations independently projected into one
    declared observation instrument. The caller owns semantic comparability.
    """
    def __init__(self, root, transitions, observed, target):
        if not target or any(p < 0 for p in target.values()) or sum(target.values()) != 1:
            raise ValueError("target must be a probability law")
        if set(transitions) & set(observed):
            raise ValueError("a prefix cannot also be a measured leaf")
        # Iterative topological traversal. Shared continuations receive their
        # incoming mass from *every* predecessor before they are propagated.
        from graphlib import TopologicalSorter
        order = tuple(reversed(tuple(TopologicalSorter({
            parent: tuple(a.child for a in edges) for parent, edges in transitions.items()
        }).static_order())))
        if root not in order:
            if root not in observed or transitions:
                raise ValueError("missing root")
            order = (root,)
        reachable = {root}
        mass = defaultdict(Fraction, {root: Fraction(1)})
        for node in order:
            if node not in reachable:
                raise ValueError("disconnected prefix")
            if node in transitions:
                edges = transitions[node]
                if not edges or sum(a.probability for a in edges) != 1:
                    raise ValueError("unclosed outgoing mass")
                if len({a.child for a in edges}) != len(edges):
                    raise ValueError("duplicate continuation")
                for edge in edges:
                    if not isinstance(edge.probability, Fraction) or edge.probability <= 0:
                        raise ValueError("explicit positive rational proposal required")
                    reachable.add(edge.child)
                    mass[edge.child] += mass[node] * edge.probability
            elif node not in observed:
                raise ValueError(f"unmeasured continuation: {node}")
        if set(observed) != reachable - set(transitions):
            raise ValueError("observation and generator coverage differ")
        baseline = defaultdict(Fraction)
        for node, cell in observed.items():
            if cell not in target:
                raise ValueError(f"emission outside the instrument domain: {cell}")
            baseline[cell] += mass[node]
        for cell, probability in target.items():
            if probability and not baseline[cell]:
                raise ValueError(f"positive source cell unreachable in supplied generator: {cell}")
        self.leaf_mass = {}
        continuation = {}
        self.routes = {}
        for node in reversed(order):
            if node in observed:
                cell = observed[node]
                continuation[node] = target[cell] / baseline[cell]
                self.leaf_mass[node] = mass[node] * continuation[node]
            else:
                weights = [(a.child, a.probability * continuation[a.child])
                           for a in transitions[node]]
                total = sum(w for _, w in weights)
                continuation[node] = total
                if total:
                    self.routes[node] = tuple(Alternative(child, w / total)
                                              for child, w in weights if w)
        if continuation[root] != 1:
            raise ArithmeticError("calibrated root mass is not unity")
        self.root = root

    def draw(self, rng: Random):
        """Draw a path without float conversion, carrier duplication or forced actor action."""
        path = [self.root]
        while path[-1] in self.routes:
            routes = self.routes[path[-1]]
            scale = lcm(*(a.probability.denominator for a in routes))
            ticket = rng.randrange(scale)
            for edge in routes:
                ticket -= int(edge.probability * scale)
                if ticket < 0:
                    path.append(edge.child)
                    break
        return tuple(path)


def identified_range(target, observed, outcome):
    """Sharp across all within-cell mixtures on this finite support only."""
    by_cell = defaultdict(list)
    if observed.keys() != outcome.keys():
        raise ValueError("outcome missing for some forward histories")
    for node, cell in observed.items():
        by_cell[cell].append(outcome[node])
    lower = upper = Fraction()
    for cell, p in target.items():
        if p:
            if not by_cell[cell]:
                raise ValueError("positive target without evaluated support")
            lower += p * min(by_cell[cell])
            upper += p * max(by_cell[cell])
    return lower, upper


@dataclass(frozen=True)
class PopulationConstraint:
    """One cell's counts within a qualified common risk set, one column per entire world."""
    evidence: str
    probability: Fraction
    counts: tuple[tuple[int, int], ...]


def _reduce(rows, columns):
    """Exact row reduction of [A|b], including redundant and inconsistent constraints."""
    rows = [list(map(Fraction, row)) for row in rows]
    rank = 0
    for col in range(columns):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][col]
        rows[rank] = [v / scale for v in rows[rank]]
        for i, row in enumerate(rows):
            if i != rank and row[col]:
                rows[i] = [v - row[col] * p for v, p in zip(row, rows[rank])]
        rank += 1
    if any(row[-1] for row in rows[rank:]):
        return None
    return rows[:rank]


def constrained_world_range(constraints, outcome, *, basis_budget):
    """Exact small-library receiving calculation, not a production LP optimizer.

    outcome is a whole-world payoff. The returned witnesses are distributions of
    complete worlds. A conditional target additionally needs an independently
    nonvanishing risk set; this reader refuses if the input permits its collapse.
    """
    from itertools import combinations
    from math import comb

    n = len(outcome)
    if not n or not constraints:
        raise ValueError("world library and constraints required")
    rows = [[1] * n + [1]]
    for c in constraints:
        if (not c.evidence or len(c.counts) != n or not isinstance(c.probability, Fraction)
                or not 0 <= c.probability <= 1):
            raise ValueError("invalid population constraint")
        for yes, total in c.counts:
            if type(yes) is not int or type(total) is not int or not 0 <= yes <= total:
                raise ValueError("invalid world counts")
        rows.append([yes - c.probability * total for yes, total in c.counts] + [0])
    rows = _reduce(rows, n)
    if rows is None:
        raise ValueError("incompatible constraints on supplied world library")
    rank = len(rows)
    if comb(n, rank) > basis_budget:
        raise ValueError("basis budget exceeded; identification not computed")
    lower = upper = None
    for active in combinations(range(n), rank):
        square = [[row[i] for i in active] + [row[-1]] for row in rows]
        solution = _reduce(square, rank)
        if solution is None or len(solution) != rank or any(row[-1] < 0 for row in solution):
            continue
        weights = [Fraction()] * n
        for i, row in zip(active, solution):
            weights[i] = row[-1]
        for c in constraints:
            if not sum(w * total for w, (_, total) in zip(weights, c.counts)):
                raise ValueError(f"risk can vanish; independent risk constraint required: {c.evidence}")
        value = sum(w * v for w, v in zip(weights, outcome))
        if lower is None or value < lower[0]:
            lower = value, tuple(weights)
        if upper is None or value > upper[0]:
            upper = value, tuple(weights)
    if lower is None:
        raise ValueError("incompatible constraints on supplied world library")
    return lower, upper


def free_action_range(emission, target, outcome, *, basis_budget):
    """Invert a fixed forward instrument, changing *only* initial world weights.

    emission[j][y] is the forward probability of y in initial world j with
    subsequent owner policies kept intact. Only for one risk unit per world
    with the same qualified instrument. Display counts may be arbitrarily
    scaled, but must never alter the relative risk weight of one column.
    """
    worlds = tuple(emission)
    if not worlds or not target or outcome.keys() != emission.keys():
        raise ValueError("missing initial worlds, source target, or outcome")
    if sum(target.values()) != 1 or any(not isinstance(p, Fraction) or p < 0 for p in target.values()):
        raise ValueError("exact normalized target required")
    for row in emission.values():
        if (row.keys() != target.keys() or sum(row.values()) != 1
                or any(not isinstance(p, Fraction) or p < 0 for p in row.values())):
            raise ValueError("incomplete fixed forward emission law")
    scale = lcm(*(p.denominator for row in emission.values() for p in row.values()))
    constraints = [PopulationConstraint(repr(cell), probability, tuple(
        (int(scale * emission[name][cell]), scale) for name in worlds
    )) for cell, probability in target.items()]
    return constrained_world_range(constraints, tuple(outcome[w] for w in worlds),
                                   basis_budget=basis_budget)
