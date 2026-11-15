from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

from rawlsing_next.pre553_recursive_handoff import (
    RecursiveHandoffError,
    execute_exact_bounded_discovery_with_handoffs,
    load_recursive_handoff_bundle,
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


def _respondents(source, ids):
    return tuple(source["respondents"][rid] for rid in ids)


def _refs(source, ids):
    return tuple(sorted((source["respondents"][rid].ref for rid in ids), key=lambda ref: ref.key))


def _generation_one(source, qauth):
    parent = _branch_predicate(
        source,
        qauth,
        members=_respondents(source, ("R1", "R2", "R3", "R4", "R5", "R6")),
        tag="mx01r2-parent",
    )
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="mx01r2-x1")
    x_query = _query(source, qauth, parent, ("X",), tag="mx01r2-g1-x")
    dauth = _d_auth("mx01r2-g1-discovery")
    grammar = _grammar(
        operation="I03-OP-mx01r2-g1-discovery",
        atoms=[_atom("PARENT", parent, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("X", x_query)],
        rules=[_rule(
            "child", "RECURSIVE_SUBGROUP_FORK", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="PARENT", query_template_id="X",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    authority = _discovery_authority(source, grammar, dauth, tag="mx01r2-g1")
    registry = _registry(source, qauth, dauth)
    result = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        predicate_catalog=(parent, x1),
        query_template_catalog=(x_query,),
    )
    return parent, result, registry


def test_depth_two_recursive_handoff_frozen_hostile_fixture_and_fresh_process_replay(tmp_path):
    source, qauth = _fixture()
    parent, g1, g1_registry = _generation_one(source, qauth)
    assert len(g1.handoffs) == 1
    child = g1.handoffs[0]
    assert g1.discovery_result.receipts[0].typed_state == "DISCOVERED_RESULT_SUPPORTED"
    assert child.immediate_parent_branch_ref == parent.ref
    child_members = replay_recursive_branch_membership(
        repository=source["repo"], handoff=child, authority_registry=g1_registry
    )
    assert child_members == _refs(source, ("R1", "R2", "R3", "R4"))

    bundle_path = tmp_path / "child.bundle.json"
    bundle_ref = write_recursive_handoff_bundle(bundle_path, g1.handoffs)
    loaded_bundle_ref, loaded = load_recursive_handoff_bundle(bundle_path)
    assert loaded_bundle_ref == bundle_ref
    assert len(loaded) == 1
    assert loaded[0].ref == child.ref
    assert loaded[0].winning_predicate.ref == child.winning_predicate.ref
    assert loaded[0].immediate_parent_branch_ref == parent.ref

    repo_root = Path(__file__).resolve().parents[2]
    outputs = []
    for index in (1, 2):
        out = tmp_path / f"fresh-{index}.json"
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "rawlsing_next.tests.mx01r2_fresh_process_runner",
                str(bundle_path),
                str(out),
            ],
            cwd=repo_root,
            check=True,
            text=True,
            capture_output=True,
        )
        assert completed.returncode == 0, completed.stderr
        outputs.append(json.loads(out.read_text(encoding="utf-8")))

    # Two independent Python processes must reproduce every identity-bearing observable.
    assert outputs[0] == outputs[1]
    replay = outputs[0]
    assert replay["child_bundle_ref"] == bundle_ref.as_dict()
    assert replay["child_handoff_ref"] == child.ref.as_dict()
    assert replay["child_predicate_ref"] == child.winning_predicate.ref.as_dict()
    assert replay["child_immediate_parent_ref"] == parent.ref.as_dict()
    assert replay["child_member_refs"] == [ref.as_dict() for ref in _refs(source, ("R1", "R2", "R3", "R4"))]
    assert replay["grandchild_immediate_parent_ref"] == child.winning_predicate.ref.as_dict()
    assert replay["grandchild_member_refs"] == [ref.as_dict() for ref in _refs(source, ("R1", "R2"))]
    assert replay["conditioned_cotravel_state"] == "DISCOVERED_RESULT_SUPPORTED"
    assert replay["conditioned_cotravel_coverage_state"] == "EVALUATED_SUPPORTED"
    assert replay["lookalike_state"] == "VALID_EMPTY"
    assert replay["lookalike_coverage_state"] == "EVALUATED_VALID_EMPTY"
    assert replay["underpowered_state"] == "INSUFFICIENT_SUPPORT"
    assert replay["underpowered_coverage_state"] == "EVALUATED_UNDERPOWERED"
    assert replay["conditioned_cotravel_receipt_ref"] != replay["lookalike_receipt_ref"]
    assert replay["conditioned_cotravel_replay_ref"] != replay["lookalike_replay_ref"]


def test_recursive_handoff_bundle_tamper_fails_closed(tmp_path):
    source, qauth = _fixture()
    _, g1, _ = _generation_one(source, qauth)
    bundle_path = tmp_path / "child.bundle.json"
    write_recursive_handoff_bundle(bundle_path, g1.handoffs)

    payload = json.loads(bundle_path.read_text(encoding="utf-8"))
    payload["payload"]["handoffs"][0]["winning_predicate"]["content_hash"] = "0" * 64
    bundle_path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    with pytest.raises(RecursiveHandoffError):
        load_recursive_handoff_bundle(bundle_path)
