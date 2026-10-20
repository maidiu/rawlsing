"""Bounded adapter: generated symbolic grammar -> real imported PRE553 I05 exact compiler.

It populates the existing ``rawlsing_next.pre553_discovery_exact._compile_frontier``
through its public grammar shape. It does not rewrite I05, C11, Batch or U43.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom, _d_auth, _discovery_authority, _grammar, _qt, _rule,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate, _build_source, _predicate, _query, _query_authority,
    _registry, _response_leaf,
)

from .fixture import synthetic_rows
from .native_map import native_rule_key
from .types import ScientificFrontier


@dataclass(frozen=True)
class NativeRun:
    source_tag: str
    grammar: Mapping[str, Any]
    grammar_hash: str
    candidate_rule_counts: Mapping[str, int]
    candidate_count: int
    receipt_refs: tuple[str, ...]
    receipt_states: tuple[str, ...]
    frontier_ref_hash: str
    replay_ref_hash: str
    result_identity_hash: str
    predicate_count: int
    query_count: int
    fact_count: int
    rule_coverage: Mapping[str, tuple[str, ...]]
    fact_states: tuple[str, ...] = ()
    observed_zero_cell_count: int = 0
    zero_denominator_fact_count: int = 0
    fact_summaries: tuple[Mapping[str, Any], ...] = ()

    def material(self) -> dict:
        return {
            "source_tag": self.source_tag, "grammar_hash": self.grammar_hash,
            "candidate_rule_counts": dict(self.candidate_rule_counts),
            "candidate_count": self.candidate_count,
            "receipt_refs": list(self.receipt_refs),
            "receipt_states": list(self.receipt_states),
            "frontier_ref_hash": self.frontier_ref_hash,
            "replay_ref_hash": self.replay_ref_hash,
            "result_identity_hash": self.result_identity_hash,
            "predicate_count": self.predicate_count,
            "query_count": self.query_count, "fact_count": self.fact_count,
            "rule_coverage": {k: list(v) for k, v in self.rule_coverage.items()},
            "fact_states": list(self.fact_states),
            "observed_zero_cell_count": self.observed_zero_cell_count,
            "zero_denominator_fact_count": self.zero_denominator_fact_count,
            "fact_summaries": list(self.fact_summaries),
        }

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.material())


NATIVE_RULE_DEFS = (
    # rule_id, family, expected_candidates, symbolic classes covered
    ("DIST-Y", "BRANCH_CONDITIONED_DISTRIBUTION", 2, ("DIST",)),
    ("COND-A0", "BRANCH_CONDITIONED_DISTRIBUTION", 1, ("CONDITIONAL",)),
    ("COND-A1", "BRANCH_CONDITIONED_DISTRIBUTION", 1, ("CONDITIONAL",)),
    ("COND-B0", "BRANCH_CONDITIONED_DISTRIBUTION", 1, ("CONDITIONAL",)),
    ("COND-B1", "BRANCH_CONDITIONED_DISTRIBUTION", 1, ("CONDITIONAL",)),
    ("COND-M0", "BRANCH_CONDITIONED_DISTRIBUTION", 1, ("CONDITIONAL",)),
    ("COND-M1", "BRANCH_CONDITIONED_DISTRIBUTION", 1, ("CONDITIONAL",)),
    ("GRID-AB", "BOUNDED_K_WAY_RESPONSE_CONFIGURATION", 4, ("INTERACTION",)),
    ("XOR-AB", "BOUNDED_K_WAY_RESPONSE_CONFIGURATION", 1, ("INTERACTION",)),
    ("JOINT-YM", "PAIR_RESPONSE_COTRAVEL", 1, ("JOINT", "CO_TRAVEL")),
    ("FORK-A1-M1", "RECURSIVE_SUBGROUP_FORK", 1, ("FORK",)),
)
EXPECTED_RULE_COUNTS = {r[0]: r[2] for r in NATIVE_RULE_DEFS}


def _source_and_authorities():
    source = _build_source("g50-synth", synthetic_rows())
    qauth = _query_authority("g50")
    dauth = _d_auth("g50-discovery")
    registry = _registry(source, qauth, dauth)
    return source, qauth, dauth, registry


def build_native_grammar(*, drop_rule: str | None = None, rows=None) -> tuple[dict, dict, dict, dict]:
    source = _build_source("g50-synth", synthetic_rows() if rows is None else rows)
    qauth = _query_authority("g50")
    all_p = _branch_predicate(source, qauth, tag="g50-all")
    leaf = {}
    for item in ("A", "B", "M"):
        for value in (0, 1):
            leaf[(item, value)] = _predicate(
                source, qauth, _response_leaf(source, qauth, item, value),
                tag=f"g50-{item}{value}",
            )
    yq = _query(source, qauth, all_p, ("Y",), tag="g50-y")
    mq = _query(source, qauth, all_p, ("M",), tag="g50-m")
    ymq = _query(source, qauth, all_p, ("Y", "M"), tag="g50-ym")
    atoms = [_atom("ALL", all_p, "BRANCH")]
    atoms += [_atom(f"{item}{value}", predicate, "RESPONSE")
              for (item, value), predicate in leaf.items()]
    templates = [_qt("TY", yq), _qt("TM", mq), _qt("TYM", ymq)]
    diff = {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"}
    rules = []
    rules.append(_rule(
        "DIST-Y", "BRANCH_CONDITIONED_DISTRIBUTION", "BASE_QUERY", baseline_atom_id="ALL",
        query_template_id="TY", target_cells=["0", "1"],
        validation={"kind": "TARGET_CELL_SUPPORTED"},
    ))
    for item in ("A", "B", "M"):
        for value in (0, 1):
            rules.append(_rule(
                f"COND-{item}{value}", "BRANCH_CONDITIONED_DISTRIBUTION", "SINGLE_ATOM",
                atom_ids=[f"{item}{value}"], baseline_atom_id="ALL",
                query_template_id="TY", validation=diff,
            ))
    rules.append(_rule(
        "GRID-AB", "BOUNDED_K_WAY_RESPONSE_CONFIGURATION", "AND_CARTESIAN_GROUPS",
        baseline_atom_id="ALL", query_template_id="TY",
        atom_groups=[["A0", "A1"], ["B0", "B1"]], validation=diff,
    ))
    rules.append(_rule(
        "XOR-AB", "BOUNDED_K_WAY_RESPONSE_CONFIGURATION", "XOR_EXACTLY_ONE_COMBINATIONS",
        baseline_atom_id="ALL", query_template_id="TY",
        atom_ids=["A1", "B1"], arity=2, validation=diff,
    ))
    rules.append(_rule(
        "JOINT-YM", "PAIR_RESPONSE_COTRAVEL", "JOINT_DEPENDENCE", baseline_atom_id="ALL",
        joint_template_id="TYM", marginal_template_ids=["TY", "TM"],
        validation={"kind": "JOINT_NOT_PRODUCT_OF_MARGINALS"},
    ))
    rules.append(_rule(
        "FORK-A1-M1", "RECURSIVE_SUBGROUP_FORK", "SINGLE_ATOM", atom_ids=["M1"],
        baseline_atom_id="A1", query_template_id="TY", validation=diff,
    ))
    if drop_rule is not None:
        rules = [rule for rule in rules if rule["rule_id"] != drop_rule]
        if len(rules) == len(NATIVE_RULE_DEFS):
            raise ValueError(f"UNKNOWN_DROP_RULE:{drop_rule}")
    grammar = _grammar(
        operation="I03-OP-g50-discovery",
        atoms=atoms, templates=templates, rules=rules, k=2, j=3,
    )
    return grammar, {"source": source, "qauth": qauth,
                     "predicates": tuple(sorted(leaf.values(), key=lambda p: p.ref.key)) + (all_p,),
                     "queries": (yq, mq, ymq)}, leaf, all_p


def run_native(*, drop_rule: str | None = None, rows=None) -> NativeRun:
    grammar, materialized, leaf, all_p = build_native_grammar(drop_rule=drop_rule, rows=rows)
    source = materialized["source"]
    qauth = materialized["qauth"]
    dauth = _d_auth("g50-discovery")
    registry = _registry(source, qauth, dauth)
    predicates = materialized["predicates"]
    queries = materialized["queries"]
    authority = _discovery_authority(source, grammar, dauth, tag="g50-native")
    result = execute_exact_bounded_discovery(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        predicate_catalog=predicates,
        query_template_catalog=queries,
    )
    counts: dict[str, int] = {}
    for receipt in result.receipts:
        rule_id = receipt.candidate_identity["rule_id"]
        counts[rule_id] = counts.get(rule_id, 0) + 1
    return NativeRun(
        source_tag="g50-synth",
        grammar=grammar,
        grammar_hash=semantic_hash(canonicalize(grammar)),
        candidate_rule_counts=dict(sorted(counts.items())),
        candidate_count=result.candidate_count,
        receipt_refs=tuple(receipt.ref.key for receipt in result.receipts),
        receipt_states=tuple(receipt.typed_state for receipt in result.receipts),
        frontier_ref_hash=result.evaluated_frontier_ref.content_hash,
        replay_ref_hash=result.replay_ref.content_hash,
        result_identity_hash=semantic_hash({
            "frontier": result.evaluated_frontier_ref.as_dict(),
            "replay": result.replay_ref.as_dict(),
            "receipts": [r.ref.as_dict() for r in result.receipts],
        }),
        predicate_count=len(result.executed_predicates),
        query_count=len(result.executed_queries),
        fact_count=len(result.empirical_facts),
        rule_coverage=_rule_coverage(result),
        fact_states=tuple(sorted({f.typed_state for f in result.empirical_facts})),
        observed_zero_cell_count=_observed_zero_cells(result),
        zero_denominator_fact_count=sum(
            1 for f in result.empirical_facts if f.raw_denominator_support == 0
        ),
        fact_summaries=_fact_summaries(result),
    )


def _rule_coverage(result) -> dict[str, tuple[str, ...]]:
    coverage: dict[str, list[str]] = {}
    for receipt in result.receipts:
        coverage.setdefault(receipt.candidate_identity["rule_id"], []).append(
            receipt.candidate_identity["candidate_id"]
        )
    return {key: tuple(sorted(value)) for key, value in sorted(coverage.items())}


def _fact_summaries(result) -> tuple[Mapping[str, Any], ...]:
    facts = {f.ref.key: f for f in result.empirical_facts}
    summaries = []
    for receipt in result.receipts:
        rows = []
        for ref in receipt.empirical_fact_refs:
            if isinstance(ref, Mapping):
                ref_key = f"{ref['kind']}|{ref['object_id']}|{ref['content_hash']}"
            else:
                ref_key = ref.key
            fact = facts[ref_key]
            cells = (fact.target_topology or {}).get("complete_cell_semantic_projection") or []
            rows.append({
                "fact_hash": fact.ref.content_hash,
                "state": fact.typed_state,
                "denominator": fact.raw_denominator_support,
                "cells": [
                    {"cell": cell.get("cell"),
                     "numerator": cell.get("raw_numerator_support")}
                    for cell in cells
                ],
            })
        summaries.append({
            "candidate_id": receipt.candidate_identity["candidate_id"],
            "rule_id": receipt.candidate_identity["rule_id"],
            "receipt_state": receipt.typed_state,
            "coverage_state": receipt.coverage_state,
            "facts": rows,
        })
    return tuple(sorted(summaries, key=lambda x: (x["rule_id"], x["candidate_id"])))


def _observed_zero_cells(result) -> int:
    count = 0
    for fact in result.empirical_facts:
        if fact.raw_denominator_support <= 0:
            continue
        rows = (fact.target_topology or {}).get("complete_cell_semantic_projection") or []
        for row in rows:
            if int(row.get("raw_numerator_support", 0)) == 0:
                count += 1
    return count


def run_empty_probe() -> dict[str, Any]:
    """Native I05 probe: a logically impossible joint route has zero denominator."""

    source = _build_source("g50-empty", synthetic_rows())
    qauth = _query_authority("g50-empty")
    dauth = _d_auth("g50-empty-discovery")
    all_p = _branch_predicate(source, qauth, tag="g50-empty-all")
    rt1 = _predicate(source, qauth, _response_leaf(source, qauth, "RT", 1), tag="g50-rt1")
    rt0 = _predicate(source, qauth, _response_leaf(source, qauth, "RT", 0), tag="g50-rt0")
    impossible = _predicate(
        source, qauth, {"op": "AND", "children": [rt1.predicate_ast, rt0.predicate_ast]},
        tag="g50-empty",
    )
    yq = _query(source, qauth, all_p, ("Y",), tag="g50-empty-y")
    grammar = _grammar(
        operation="I03-OP-g50-empty-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("EMPTY", impossible, "RESPONSE")],
        templates=[_qt("TY", yq)],
        rules=[_rule(
            "EMPTY-Y", "BRANCH_CONDITIONED_DISTRIBUTION", "SINGLE_ATOM",
            atom_ids=["EMPTY"], baseline_atom_id="ALL", query_template_id="TY",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2, j=3,
    )
    authority = _discovery_authority(source, grammar, dauth, tag="g50-empty")
    result = execute_exact_bounded_discovery(
        repository=source["repo"], discovery_authority=authority,
        authority_registry=_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=(all_p, impossible), query_template_catalog=(yq,),
    )
    fact = result.empirical_facts[0] if result.empirical_facts else None
    return {
        "candidate_count": result.candidate_count,
        "receipt_states": tuple(r.typed_state for r in result.receipts),
        "coverage_states": tuple(r.coverage_state for r in result.receipts),
        "fact_state": None if fact is None else fact.typed_state,
        "raw_denominator_support": None if fact is None else fact.raw_denominator_support,
        "zero_denominator_fact_count": sum(1 for f in result.empirical_facts if f.raw_denominator_support == 0),
        "frontier_ref_hash": result.evaluated_frontier_ref.content_hash,
    }


def expected_rule_coverage(frontier: ScientificFrontier) -> dict[str, tuple[str, ...]]:
    """Map native rule ids to the symbolic operation ids they must cover."""

    coverage: dict[str, list[str]] = {}
    for op in frontier.eligible():
        key = native_rule_key(op)
        if key is not None:
            coverage.setdefault(key, []).append(op.op_id)
    return {key: tuple(sorted(value)) for key, value in sorted(coverage.items())}


def native_no_drop(frontier: ScientificFrontier, run: NativeRun) -> dict[str, Any]:
    expected_rules = expected_rule_coverage(frontier)
    received_rules = set(run.candidate_rule_counts)
    expected_rule_ids = set(EXPECTED_RULE_COUNTS) & set(expected_rules)
    missing_rules = sorted(expected_rule_ids - received_rules)
    unexpected_rules = sorted(received_rules - expected_rule_ids)
    count_mismatches = {
        rule_id: {"expected": EXPECTED_RULE_COUNTS[rule_id],
                  "actual": run.candidate_rule_counts.get(rule_id, 0)}
        for rule_id in sorted(expected_rule_ids)
        if run.candidate_rule_counts.get(rule_id, 0) != EXPECTED_RULE_COUNTS[rule_id]
    }
    return {
        "expected_rule_coverage": expected_rules,
        "received_rule_counts": dict(run.candidate_rule_counts),
        "missing_rules": missing_rules,
        "unexpected_rules": unexpected_rules,
        "count_mismatches": count_mismatches,
        "no_drop_ok": not missing_rules and not unexpected_rules and not count_mismatches,
        "candidate_count_ok": run.candidate_count == sum(EXPECTED_RULE_COUNTS.values()),
    }


__all__ = [
    "NATIVE_RULE_DEFS", "EXPECTED_RULE_COUNTS", "NativeRun",
    "build_native_grammar", "run_native", "run_empty_probe",
    "expected_rule_coverage", "native_no_drop",
]
