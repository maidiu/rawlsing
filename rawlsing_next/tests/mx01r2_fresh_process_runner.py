#!/usr/bin/env python3
"""Fresh-process half of the MX01 R2 hostile recursive-handoff proof."""
from __future__ import annotations

import json
from pathlib import Path
import sys

from rawlsing_next.pre553_empirical_objects import DiscoveryAuthority, canonicalize
from rawlsing_next.pre553_recursive_handoff import (
    execute_exact_bounded_discovery_with_handoffs,
    load_recursive_handoff_bundle,
    recursive_parent_atom,
    replay_recursive_branch_membership,
    write_recursive_handoff_bundle,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom,
    _d_auth,
    _discovery_authority,
    _grammar,
    _qt,
    _rule,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _build_source,
    _predicate,
    _query,
    _query_authority,
    _registry,
    _response_leaf,
)


def _fixture():
    rows = [
        {"id": "R1", "responses": {"X": 1, "H": 1, "Y": 1, "Z": 1}},
        {"id": "R2", "responses": {"X": 1, "H": 1, "Y": 0, "Z": 0}},
        {"id": "R3", "responses": {"X": 1, "H": 0, "Y": 1, "Z": 0}},
        {"id": "R4", "responses": {"X": 1, "H": 0, "Y": 0, "Z": 1}},
        {"id": "R5", "responses": {"X": 0, "H": 1, "Y": 1, "Z": 1}},
        {"id": "R6", "responses": {"X": 0, "H": 0, "Y": 0, "Z": 0}},
        {"id": "R7", "responses": {"X": 1, "H": 1, "Y": 1, "Z": 0}},
        {"id": "R8", "responses": {"X": 0, "H": 0, "Y": 0, "Z": 1}},
    ]
    source = _build_source("mx01r2", rows)
    qauth = _query_authority("mx01r2-q")
    return source, qauth


def _authority_with_minimum(source, grammar, dauth, minimum, *, tag):
    base = _discovery_authority(source, grammar, dauth, tag=tag)
    return DiscoveryAuthority(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
        **{**dict(base.semantic_fields), "support_rules": {"minimum_raw_denominator": minimum}},
    )


def _respondents_for(source, ids):
    return tuple(source["respondents"][rid] for rid in ids)


def _refs_for(source, ids):
    return tuple(source["respondents"][rid].ref for rid in ids)


def run(child_bundle_path: Path, output_path: Path) -> dict:
    source, qauth = _fixture()
    child_bundle_ref, child_handoffs = load_recursive_handoff_bundle(child_bundle_path)
    if len(child_handoffs) != 1:
        raise AssertionError("fresh runner requires exactly one child handoff")
    child = child_handoffs[0]
    child_members = replay_recursive_branch_membership(
        repository=source["repo"],
        handoff=child,
        authority_registry=_registry(source, qauth),
    )
    if child_members != tuple(sorted(_refs_for(source, ("R1", "R2", "R3", "R4")), key=lambda ref: ref.key)):
        raise AssertionError("fresh-process child membership replay mismatch")

    # Generation 2 consumes the persisted CHILD. It is never pre-authored.
    h1 = _predicate(source, qauth, _response_leaf(source, qauth, "H", 1), tag="mx01r2-h1")
    h_query = _query(source, qauth, child.winning_predicate, ("H",), tag="mx01r2-g2-h")
    g2_dauth = _d_auth("mx01r2-g2-discovery")
    g2_grammar = _grammar(
        operation="I03-OP-mx01r2-g2-discovery",
        atoms=[recursive_parent_atom(child, "CHILD"), _atom("H1", h1, "RESPONSE")],
        templates=[_qt("H", h_query)],
        rules=[_rule(
            "grandchild", "RECURSIVE_SUBGROUP_FORK", "SINGLE_ATOM",
            atom_ids=("H1",), baseline_atom_id="CHILD", query_template_id="H",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    g2_authority = _discovery_authority(source, g2_grammar, g2_dauth, tag="mx01r2-g2")
    g2_registry = _registry(source, qauth, g2_dauth)
    g2 = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=g2_authority,
        authority_registry=g2_registry,
        release_refs=(source["release_ref"],),
        predicate_catalog=(child.winning_predicate, h1),
        query_template_catalog=(h_query,),
    )
    if len(g2.handoffs) != 1:
        raise AssertionError("generation 2 must materialize one supported grandchild handoff")
    grandchild = g2.handoffs[0]
    grandchild_members = replay_recursive_branch_membership(
        repository=source["repo"], handoff=grandchild, authority_registry=g2_registry
    )
    if grandchild_members != tuple(sorted(_refs_for(source, ("R1", "R2")), key=lambda ref: ref.key)):
        raise AssertionError("grandchild exact membership replay mismatch")
    if grandchild.immediate_parent_branch_ref != child.winning_predicate.ref:
        raise AssertionError("grandchild immediate parent is not the persisted child predicate")

    grandchild_bundle_path = output_path.with_suffix(".grandchild.bundle.json")
    grandchild_bundle_ref = write_recursive_handoff_bundle(grandchild_bundle_path, g2.handoffs)
    reloaded_gc_ref, reloaded_gc = load_recursive_handoff_bundle(grandchild_bundle_path)
    if reloaded_gc_ref != grandchild_bundle_ref or len(reloaded_gc) != 1:
        raise AssertionError("grandchild bundle fresh reload mismatch")
    if reloaded_gc[0].winning_predicate.ref != grandchild.winning_predicate.ref:
        raise AssertionError("grandchild predicate identity changed across bundle reload")

    # Branch-conditioned same-respondent Y -> Z cotravel inside GRANDCHILD.
    y1 = _predicate(source, qauth, _response_leaf(source, qauth, "Y", 1), tag="mx01r2-y1")
    z_gc_query = _query(source, qauth, grandchild.winning_predicate, ("Z",), tag="mx01r2-gc-z")
    cot_dauth = _d_auth("mx01r2-cotravel-discovery")
    cot_grammar = _grammar(
        operation="I03-OP-mx01r2-cotravel-discovery",
        atoms=[recursive_parent_atom(grandchild, "GRANDCHILD"), _atom("Y1", y1, "RESPONSE")],
        templates=[_qt("Z", z_gc_query)],
        rules=[_rule(
            "grandchild-y-z", "BRANCH_CONDITIONED_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("Y1",), baseline_atom_id="GRANDCHILD", query_template_id="Z",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    cot_authority = _discovery_authority(source, cot_grammar, cot_dauth, tag="mx01r2-cotravel")
    cot = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=cot_authority,
        authority_registry=_registry(source, qauth, cot_dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=(grandchild.winning_predicate, y1),
        query_template_catalog=(z_gc_query,),
    ).discovery_result
    cot_receipt = cot.receipts[0]
    if cot_receipt.typed_state != "DISCOVERED_RESULT_SUPPORTED":
        raise AssertionError("recursive grandchild-conditioned cotravel must be supported")

    # Superficially similar whole-universe Y -> Z is exactly unchanged.
    all_p = _branch_predicate(source, qauth, tag="mx01r2-all")
    z_all_query = _query(source, qauth, all_p, ("Z",), tag="mx01r2-all-z")
    look_dauth = _d_auth("mx01r2-lookalike-discovery")
    look_grammar = _grammar(
        operation="I03-OP-mx01r2-lookalike-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("Y1", y1, "RESPONSE")],
        templates=[_qt("Z", z_all_query)],
        rules=[_rule(
            "whole-y-z", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("Y1",), baseline_atom_id="ALL", query_template_id="Z",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    look_authority = _discovery_authority(source, look_grammar, look_dauth, tag="mx01r2-lookalike")
    look = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=look_authority,
        authority_registry=_registry(source, qauth, look_dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=(all_p, y1),
        query_template_catalog=(z_all_query,),
    ).discovery_result
    look_receipt = look.receipts[0]
    if look_receipt.typed_state != "VALID_EMPTY" or look_receipt.coverage_state != "EVALUATED_VALID_EMPTY":
        raise AssertionError("whole-universe lookalike must remain typed VALID_EMPTY")

    # Exact one-member branch under minimum denominator 2 remains underpowered.
    parent = _branch_predicate(
        source,
        qauth,
        members=_respondents_for(source, ("R1", "R2", "R3", "R4", "R5", "R6")),
        tag="mx01r2-parent",
    )
    x0 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 0), tag="mx01r2-x0")
    x_parent_query = _query(source, qauth, parent, ("X",), tag="mx01r2-underpowered-x")
    under_dauth = _d_auth("mx01r2-underpowered-discovery")
    under_grammar = _grammar(
        operation="I03-OP-mx01r2-underpowered-discovery",
        atoms=[_atom("PARENT", parent, "BRANCH"), _atom("X0", x0, "RESPONSE"), _atom("H1", h1, "RESPONSE")],
        templates=[_qt("X", x_parent_query)],
        rules=[_rule(
            "one-member", "RECURSIVE_SUBGROUP_FORK", "AND_COMBINATIONS",
            atom_ids=("X0", "H1"), arity=2, baseline_atom_id="PARENT", query_template_id="X",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    under_authority = _authority_with_minimum(source, under_grammar, under_dauth, 2, tag="mx01r2-underpowered")
    under = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=under_authority,
        authority_registry=_registry(source, qauth, under_dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=(parent, x0, h1),
        query_template_catalog=(x_parent_query,),
    ).discovery_result
    under_receipt = under.receipts[0]
    if under_receipt.typed_state != "INSUFFICIENT_SUPPORT" or under_receipt.coverage_state != "EVALUATED_UNDERPOWERED":
        raise AssertionError("one-member recursive branch must remain typed underpowered")

    payload = canonicalize({
        "child_bundle_ref": child_bundle_ref,
        "child_handoff_ref": child.ref,
        "child_predicate_ref": child.winning_predicate.ref,
        "child_immediate_parent_ref": child.immediate_parent_branch_ref,
        "child_member_refs": child_members,
        "grandchild_handoff_ref": grandchild.ref,
        "grandchild_predicate_ref": grandchild.winning_predicate.ref,
        "grandchild_immediate_parent_ref": grandchild.immediate_parent_branch_ref,
        "grandchild_member_refs": grandchild_members,
        "grandchild_bundle_ref": grandchild_bundle_ref,
        "g2_receipt_refs": tuple(receipt.ref for receipt in g2.discovery_result.receipts),
        "g2_replay_ref": g2.discovery_result.replay_ref,
        "conditioned_cotravel_state": cot_receipt.typed_state,
        "conditioned_cotravel_coverage_state": cot_receipt.coverage_state,
        "conditioned_cotravel_receipt_ref": cot_receipt.ref,
        "conditioned_cotravel_fact_refs": cot_receipt.empirical_fact_refs,
        "conditioned_cotravel_replay_ref": cot_receipt.replay_ref,
        "lookalike_state": look_receipt.typed_state,
        "lookalike_coverage_state": look_receipt.coverage_state,
        "lookalike_receipt_ref": look_receipt.ref,
        "lookalike_replay_ref": look_receipt.replay_ref,
        "underpowered_state": under_receipt.typed_state,
        "underpowered_coverage_state": under_receipt.coverage_state,
        "underpowered_receipt_ref": under_receipt.ref,
        "underpowered_replay_ref": under_receipt.replay_ref,
    })
    output_path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    return payload


def main(argv):
    if len(argv) != 3:
        raise SystemExit("usage: mx01r2_fresh_process_runner.py CHILD_BUNDLE OUTPUT_JSON")
    run(Path(argv[1]), Path(argv[2]))


if __name__ == "__main__":
    main(sys.argv)
