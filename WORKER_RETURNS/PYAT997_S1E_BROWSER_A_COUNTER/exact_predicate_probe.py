"""Standalone stdlib RED->GREEN probe of the EXACT B/A guard ASTs.

Run from a git checkout containing the exact B parent in history:
    python WORKER_RETURNS/PYAT997_S1E_BROWSER_A_COUNTER/exact_predicate_probe.py

This is NOT PyArrow, cold-native I03/I05, or independent S1-E receiving.
It loads the two exact committed predicate functions without importing the
PyArrow-backed repository module. Its inputs are explicit synthetic Q2 rows.
"""
from __future__ import annotations

import ast
from collections.abc import Mapping
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from typing import Any

B_HEAD = "e05a0993c5e93bce47c48d52887a4d5f39e1c11d"
MODULE = "rawlsing_next/pre553_source_postconsumer_receipts.py"
ROOT = Path(__file__).resolve().parents[2]


class SourceReceiptJoinError(ValueError):
    pass


def _load_exact_guard(source: str, label: str):
    tree = ast.parse(source, filename=label)
    function = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "_verify_realized_q2_body_witness"
    )
    module = ast.Module(body=[function], type_ignores=[])
    env = {
        "Mapping": Mapping, "Any": Any,
        "SourceReceiptJoinError": SourceReceiptJoinError,
    }
    exec(compile(module, label, "exec"), env)
    return env["_verify_realized_q2_body_witness"]


def _fixture():
    return {
        "disposition": "ELIGIBLE", "source_realized": True,
        "routing_unresolved_keys": (), "unrealized_keys": (),
        "source_realization": (
            {
                "key": "K", "item_id": "item", "family": "RespondentEvent",
                "slot": (0, "q"), "question_id": "q", "emitted": 5,
                "routing_states": {"ELIGIBLE_APPLICABLE": 5},
                "routable_rows": 5, "routing_unresolved": False,
                "occurrence_realized": True, "occurrence_dimension": None,
            },
            {
                "key": "W", "item_id": "weight", "family": "WeightMeasureFact",
                "slot": (1, "w"), "question_id": None, "emitted": 5,
                "routing_states": {}, "routable_rows": None,
                "routing_unresolved": False, "occurrence_realized": True,
                "occurrence_dimension": None,
            },
        ),
    }


def _attack(kind):
    row = _fixture()
    witnesses = [dict(x) for x in row["source_realization"]]
    response = witnesses[0]
    if kind == "zero_routable":
        response["routing_states"] = {"ELIGIBLE_APPLICABLE": 0}
        response["routable_rows"] = 0
    elif kind == "hidden_unknown":
        response["routing_states"] = {
            **response["routing_states"], "ROUTING_UNKNOWN": 1,
        }
    elif kind == "routed_count_drift":
        response["routable_rows"] = 6
    elif kind == "nonresponse_routing":
        witnesses[1]["routing_states"] = {"ELIGIBLE_APPLICABLE": 1}
    elif kind == "forged_family":
        response["family"] = "FICTITIOUS_FAMILY"
    else:
        raise ValueError(kind)
    row["source_realization"] = tuple(witnesses)
    return row


def run():
    base = subprocess.check_output(
        ["git", "show", f"{B_HEAD}:{MODULE}"], cwd=ROOT, text=True,
    )
    latest = (ROOT / MODULE).read_text(encoding="utf-8")
    old = _load_exact_guard(base, B_HEAD)
    new = _load_exact_guard(latest, "worktree")
    old(_fixture())
    new(_fixture())
    # Q2's actual rule is 'any' routed slot per key; do not require ALL slots.
    mixed = _fixture()
    zero_slot = dict(mixed["source_realization"][0])
    zero_slot.update(
        slot=(2, "q2"), question_id="q2",
        routing_states={"NOT_ASKED": 5}, routable_rows=0,
    )
    mixed["source_realization"] = (
        mixed["source_realization"][0], zero_slot,
        mixed["source_realization"][1],
    )
    old(mixed)
    new(mixed)

    expected = {
        "zero_routable": "Q2_REALIZATION_ZERO_ROUTABLE_DENOMINATOR",
        "hidden_unknown": "Q2_REALIZATION_ROUTING_CENSUS_DRIFT",
        "routed_count_drift": "Q2_REALIZATION_ROUTING_CENSUS_DRIFT",
        "nonresponse_routing": "Q2_REALIZATION_NONRESPONSE_ROUTING_DRIFT",
        "forged_family": "Q2_REALIZATION_WITNESS_INVALID",
    }
    evidence = []
    for attack, refusal in expected.items():
        witness = _attack(attack)
        old(witness)  # B's exact guard lets it through: the expected RED
        try:
            new(witness)
        except SourceReceiptJoinError as exc:
            if refusal not in str(exc):
                raise AssertionError(
                    f"{attack}: unexpected A refusal {exc!s}"
                ) from exc
            evidence.append({"attack": attack, "b": "ADMITTED", "a": refusal})
        else:
            raise AssertionError(f"A erroneously admitted {attack}")
    return {
        "schema": "PYAT997_A_COUNTER_EXACT_GUARD_AST@1",
        "baseline_sha": B_HEAD,
        "baseline_source_sha256": sha256(base.encode()).hexdigest(),
        "counter_source_sha256": sha256(latest.encode()).hexdigest(),
        "cases": evidence,
        "legitimate_positive": "PRESERVED",
        "mixed_zero_slot_with_positive_sibling": "PRESERVED",
        "native_cold_reader": "NOT_RUN",
        "independent_g5": "NOT_RUN",
    }


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
