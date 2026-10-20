"""Frozen M48 oracles; model claims only, not I03/E04 integration claims."""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import json

import pytest
from grammar_model import Item, Operation, eligibility, generate, pending_estate, synthetic_distribution, execution_admission


def catalog():
    return {i.name: i for i in (Item("A", (0, 1)), Item("B", (0, 1)),
            Item("M", (0, 1)), Item("Y", (0, 1)),
            Item("ID", (0, 1), target=False, conditioner=False),
            Item("H", (0, 1), unit="household"))}


def xor_rows():
    # Independent balanced 2x2 truth table, replicated 10 times; values never
    # enter generate(). An independent 10%-minority fixture is tested below.
    return [dict(A=a, B=b, Y=a ^ b, M=0) for a in (0, 1) for b in (0, 1) for _ in range(10)]


def test_invalid_meaning_denied():
    c = catalog()
    assert eligibility(Operation(("ID",), ()), c) == "DENY_TARGET_ROLE"
    assert eligibility(Operation(("Y",), (("H", 1),)), c) == "UNRESOLVED_UNIT_LINK"
    assert eligibility(Operation(("Y",), (("Y", 1),)), c) == "TARGET_LEAKAGE"


def test_xor_reached_without_unary_screen():
    c = catalog()
    ledger = generate(c)
    rows = xor_rows()
    unconditional = synthetic_distribution(Operation(("Y",), ()), c, rows)
    unary = synthetic_distribution(Operation(("Y",), (("A", 1),)), c, rows)
    op = Operation(("Y",), (("A", 1), ("B", 0)))
    assert ledger[op] == "ELIGIBLE"
    conditional = synthetic_distribution(op, c, rows)
    assert unconditional["probabilities"][(1,)] == Fraction(1, 2)
    assert unary["probabilities"][(1,)] == Fraction(1, 2)
    assert conditional["probabilities"][(1,)] == 1
    curated_unary = {Operation(("Y",), ()), Operation(("Y",), (("A", 1),)), Operation(("Y",), (("B", 1),))}
    assert op not in curated_unary


def test_unlisted_minority_survives():
    c = catalog()
    rows = [dict(A=0, B=0, M=int(i < 10), Y=int(i < 10)) for i in range(100)]
    op = Operation(("Y",), (("M", 1),))
    assert generate(c)[op] == "ELIGIBLE"
    minority = synthetic_distribution(op, c, rows)
    assert minority["n"] == 10
    assert minority["cells"] == {(0,): 0, (1,): 10}
    assert synthetic_distribution(Operation(("Y",), ()), c, rows)["probabilities"][(1,)] == Fraction(1, 10)


def test_frontier_values_independent_and_recursive_closure():
    c = catalog()
    before = generate(c)
    rows = xor_rows()
    a = synthetic_distribution(Operation(("Y",), (("A", 1), ("B", 0))), c, rows)
    flipped = [{**r, "Y": 1-r["Y"]} for r in rows]
    b = synthetic_distribution(Operation(("Y",), (("A", 1), ("B", 0))), c, flipped)
    assert a["cells"] != b["cells"]
    assert before == generate(dict(reversed(tuple(c.items()))))
    assert all(len(op.conditions) <= 2 and len(op.targets) <= 3 for op in before)
    for op, state in before.items():
        if state == "ELIGIBLE" and op.conditions:
            assert before[Operation(op.targets, op.conditions[:-1])] == "ELIGIBLE"


def test_routing_and_split_forms():
    c = catalog()
    c["A"] = replace(c["A"], route="UNKNOWN")
    assert eligibility(Operation(("Y",), (("A", 1),)), c) == "UNKNOWN_ROUTING"
    c["A"] = replace(c["A"], route="KNOWN", forms=frozenset({"OTHER"}))
    assert eligibility(Operation(("Y", "A"), ()), c) == "DISJOINT_ADMINISTRATION"


@pytest.mark.parametrize("topology", ["SET", "RANKED", "REPEATED"])
def test_topology_obligation_not_silent_scalar(topology):
    c = catalog()
    c["A"] = replace(c["A"], topology=topology)
    assert eligibility(Operation(("Y", "A"), ()), c) == "UNSUPPORTED_TOPOLOGY_OBLIGATION"


def test_sample_population_semantic_and_permission_are_separate():
    c = catalog()
    op = Operation(("Y",), (("A", 1),))
    assert eligibility(op, c) == "ELIGIBLE"
    assert eligibility(replace(op, measure="POPULATION"), c) == "HOLD_POPULATION_MEASURE"
    assert eligibility(replace(op, claim="STRUCTURAL"), c) == "SEPARATE_CLAIM_AUTHORITY"
    assert execution_admission() == "SOURCE_HOST_PURPOSE_HOLD"
    assert c["Y"].semantic_state == "UNRESOLVED"


def test_states_denominators_and_validation():
    c = catalog()
    op = Operation(("Y",), (("A", 1), ("B", 0)))
    few = synthetic_distribution(op, c, xor_rows(), minimum=11)
    assert few["state"] == "UNDERPOWERED"
    assert few["cells"][(0,)] == 0
    assert few["validation"] == "NOT_VALIDATED"
    assert few["actor_belief"] is None
    empty = synthetic_distribution(op, c, [])
    assert empty["state"] == "VALID_EMPTY"
    assert empty["probabilities"] == {(0,): None, (1,): None}


def test_source_scope_and_reverse_roles():
    c = catalog()
    c["B"] = replace(c["B"], scope="other-wave")
    assert eligibility(Operation(("Y", "B"), ()), c) == "UNLINKED_SOURCE"
    c["A"] = replace(c["A"], target=False)
    assert eligibility(Operation(("Y",), (("A", 1),)), c) == "ELIGIBLE"
    assert eligibility(Operation(("A",), (("Y", 1),)), c) == "DENY_TARGET_ROLE"


def test_equal_marginals_do_not_identify_joint():
    c = catalog()
    equal = [dict(A=0, B=0), dict(A=1, B=1)]
    opposite = [dict(A=0, B=1), dict(A=1, B=0)]
    for t in ("A", "B"):
        assert synthetic_distribution(Operation((t,), ()), c, equal)["cells"] == synthetic_distribution(Operation((t,), ()), c, opposite)["cells"]
    assert synthetic_distribution(Operation(("A", "B"), ()), c, equal)["cells"] != synthetic_distribution(Operation(("A", "B"), ()), c, opposite)["cells"]


def test_all35_unknown_counts_conserved():
    root = Path(__file__).resolve().parents[3]
    sources = json.loads((root / "PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/ESTATE_35X_REQUIREMENTS_MATRIX.json").read_text())["sources"]
    ids = tuple(s["id"] for s in sources)
    estate = pending_estate(ids)
    assert set(estate) == set(ids)
    assert len(estate) == 35
    assert all(r["original_U_count"] is None and r["original_E_pre_count"] is None and r["cause"] for r in estate.values())
    assert sum(r["E_exec_count"] for r in estate.values()) == 0
    with pytest.raises(ValueError, match="EXACT35"):
        pending_estate(ids[:-1])


def test_finite_grammar_invalid_bounds():
    with pytest.raises(ValueError, match="FINITE_NONNEGATIVE"):
        generate(catalog(), k=-1)
    with pytest.raises(ValueError, match="FINITE_UNIQUE"):
        generate({"A": Item("A", ())})
