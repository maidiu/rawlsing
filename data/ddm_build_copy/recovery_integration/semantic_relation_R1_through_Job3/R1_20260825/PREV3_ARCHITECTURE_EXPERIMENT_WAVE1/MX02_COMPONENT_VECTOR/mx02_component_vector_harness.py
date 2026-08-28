#!/usr/bin/env python3
"""MX02 bounded component-vector hostile oracle harness.

This experiment-only harness owns no production semantic authority. It executes
the Authority-32 scalarization oracle over the five required hostile cases and
emits a deterministic receipt. Repository semantic-sufficiency adjudication is
bound separately to exact GitHub refs in EXACT_REF_LEDGER.csv.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import hashlib
import json
from pathlib import Path
from typing import Optional

HARNESS_VERSION = "mx02_component_vector_harness@1.0.0"


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ExactRef:
    kind: str
    object_id: str
    content_hash: str


@dataclass(frozen=True)
class ComponentAuthority:
    component_id: str
    ordinal: int
    role: str
    producer_family: str
    producer_ref: ExactRef
    authority_state: str  # VALUE | GOVERNED_EMPTY | UNRESOLVED
    authoritative_value: Optional[str]


def _ref(kind: str, object_id: str) -> ExactRef:
    return ExactRef(kind, object_id, _hash(f"{kind}|{object_id}"))


def evaluate_vector(case_id: str, governed_component_ids: list[str], components: list[ComponentAuthority]) -> dict:
    ordered = sorted(components, key=lambda c: c.ordinal)
    present_ids = [c.component_id for c in ordered]
    complete_identity_coverage = (
        len(present_ids) == len(governed_component_ids)
        and set(present_ids) == set(governed_component_ids)
    )
    unresolved = [c.component_id for c in ordered if c.authority_state == "UNRESOLVED"]
    governed_empty = [c.component_id for c in ordered if c.authority_state == "GOVERNED_EMPTY"]
    all_nonempty = (
        complete_identity_coverage
        and not unresolved
        and not governed_empty
        and all(
            c.authority_state == "VALUE" and c.authoritative_value not in (None, "")
            for c in ordered
        )
    )
    values = [
        c.authoritative_value
        for c in ordered
        if c.authority_state == "VALUE" and c.authoritative_value not in (None, "")
    ]
    unanimous = bool(all_nonempty and len(set(values)) == 1)
    scalarize = bool(complete_identity_coverage and all_nonempty and unanimous)

    if scalarize:
        disposition = "SCALARIZED_COMPLETE_UNANIMOUS_NONEMPTY"
        scalar_value = values[0]
    elif not complete_identity_coverage or unresolved:
        disposition = "VECTOR_INCOMPLETE_COVERAGE"
        scalar_value = None
    elif governed_empty:
        disposition = "VECTOR_GOVERNED_EMPTY_COMPONENT"
        scalar_value = None
    else:
        disposition = "VECTOR_HETEROGENEOUS_COMPLETE"
        scalar_value = None

    return {
        "case_id": case_id,
        "governed_component_ids": governed_component_ids,
        "ordered_components": [
            {
                "component_id": c.component_id,
                "ordinal": c.ordinal,
                "role": c.role,
                "producer_family": c.producer_family,
                "producer_ref": asdict(c.producer_ref),
                "authority_state": c.authority_state,
                "authoritative_value": c.authoritative_value,
            }
            for c in ordered
        ],
        "coverage_proof": {
            "complete_identity_coverage": complete_identity_coverage,
            "present_count": len(present_ids),
            "governed_count": len(governed_component_ids),
            "missing_component_ids": sorted(set(governed_component_ids) - set(present_ids)),
            "unresolved_component_ids": unresolved,
            "governed_empty_component_ids": governed_empty,
            "all_governed_components_nonempty": all_nonempty,
            "unanimous_authoritative_value": unanimous,
        },
        "scalar_disposition": disposition,
        "scalar_value": scalar_value,
        "scalarization_law_satisfied": scalarize,
    }


def build_cases() -> list[dict]:
    a = ComponentAuthority("c1", 1, "MEMBER", "V551J", _ref("V551J_COMPONENT", "c1"), "VALUE", "stratum:A")
    b = ComponentAuthority("c2", 2, "MEMBER", "V552", _ref("V552_COMPONENT", "c2"), "VALUE", "stratum:B")
    a2 = ComponentAuthority("c2", 2, "MEMBER", "V552", _ref("V552_COMPONENT", "c2"), "VALUE", "stratum:A")
    empty = ComponentAuthority("c2", 2, "MEMBER", "V552", _ref("V552_COMPONENT", "c2"), "GOVERNED_EMPTY", None)

    return [
        evaluate_vector("HETEROGENEOUS_COMPLETE", ["c1", "c2"], [a, b]),
        evaluate_vector("INCOMPLETE_COVERAGE", ["c1", "c2"], [a]),
        evaluate_vector("GOVERNED_EMPTY_COMPONENT", ["c1", "c2"], [a, empty]),
        evaluate_vector("UNANIMOUS_COMPLETE_NONEMPTY", ["c1", "c2"], [a, a2]),
        evaluate_vector("MIXED_PRODUCER_PUBLICATION", ["c1", "c2"], [a, b]),
    ]


def run() -> dict:
    cases = build_cases()
    by_id = {x["case_id"]: x for x in cases}

    assert by_id["HETEROGENEOUS_COMPLETE"]["scalar_disposition"] == "VECTOR_HETEROGENEOUS_COMPLETE"
    assert by_id["INCOMPLETE_COVERAGE"]["scalar_disposition"] == "VECTOR_INCOMPLETE_COVERAGE"
    assert by_id["GOVERNED_EMPTY_COMPONENT"]["scalar_disposition"] == "VECTOR_GOVERNED_EMPTY_COMPONENT"
    assert by_id["UNANIMOUS_COMPLETE_NONEMPTY"]["scalar_disposition"] == "SCALARIZED_COMPLETE_UNANIMOUS_NONEMPTY"
    assert by_id["UNANIMOUS_COMPLETE_NONEMPTY"]["scalar_value"] == "stratum:A"
    mixed = by_id["MIXED_PRODUCER_PUBLICATION"]["ordered_components"]
    assert mixed[0]["producer_family"] != mixed[1]["producer_family"]

    return {
        "harness_version": HARNESS_VERSION,
        "oracle_cases_executed": 5,
        "oracle_assertions_passed": 5,
        "repo_code_imported": False,
        "repo_sufficiency_basis": (
            "exact GitHub code inspection bound in EXACT_REF_LEDGER.csv; "
            "this harness executes the binding scalarization oracle only"
        ),
        "expected_experiment_verdict": "FAIL_CLOSED__MISSING_COMMON_COMPONENT_AUTHORITY_VECTOR_RECEIPT",
        "cases": cases,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = run()
    text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
