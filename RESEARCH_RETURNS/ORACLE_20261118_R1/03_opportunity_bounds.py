"""Run from the repository root with PYTHONPATH=. and the repository's test dependencies."""
import json
from itertools import combinations, permutations, product

from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate, _build_source, _cell_map, _query, _query_authority, _run,
)


def examine(parity):
    names = ("free", "authorized", "in_range")
    rows = [
        {"id": f"H{x}{y}", "responses": dict(zip(names, (x, y, x ^ y ^ parity)))}
        for x, y in product(range(2), repeat=2)
    ]
    source = _build_source(f"relief-{parity}", rows, risk_namespace="relief")
    authority = _query_authority("relief")
    predicate = _branch_predicate(source, authority)
    tables = {}
    for size in range(1, 4):
        for targets in combinations(names, size):
            query = _query(source, authority, predicate, targets, tag="-".join(targets))
            fact, = _run(source, authority, predicate, query).facts
            assert fact.raw_denominator_support == len(rows)
            tables[",".join(targets)] = {
                "".join(cell): body["raw_numerator_support"]
                for cell, body in _cell_map(fact).items()
            }
    k = tables[",".join(names)]["111"]
    # Anonymous roster slots. All permutations are admissible placements, with no probabilities.
    slots = [1] * k + [0] * (len(rows) - k)
    reachable = sorted({sum(placement[:2]) for placement in permutations(slots)})
    return dict(parity=parity, release=str(source["release_ref"]), joint_fact=str(fact.ref),
                denominator=len(rows), tables=tables, reachable_counts=reachable)


if __name__ == "__main__":
    left, right = map(examine, (0, 1))
    for key in left["tables"]:
        if key.count(",") < 2:
            assert left["tables"][key] == right["tables"][key]
    assert (left["reachable_counts"], right["reachable_counts"]) == ([0], [0, 1])
    print(json.dumps([left, right], indent=2, sort_keys=True))
