from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
HARNESS_PATH = REPO_ROOT / (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/CURRENT_ZERO_LOSS_REPAIR_WAVE_R1/"
    "Z05_VERTICAL_LINEAGE_INVALIDATION/run_z05_vertical_proof.py"
)

Z05_GRAPH_HASH = "69417e48cf33de159c8e2cf3a56917dc3afff0c7b6a29ad1b3afdbe5a90abc6b"
Z05_EXPLANATION_HASH = "da73c482b22ca097066318785f85d2c3ac3d04f2a5b7b097604a7ee93682fbf4"
Z05_TERMINAL_HASH = "f10a47a8eee765b9c43a86d4479123e0001e1e1ac2e7c7371e3b0a075f427af4"
Z05_MUTATION_HASH = "e7f1ac10dd0aee6ab2860927a7845c5dae29afbe6491f4ecfb10a33bef646ce9"
Z05_RESTART_HASH = "ac03f7b77b4f290e9611edd8fdbf70018bbd745672bdcca783bd3cb1b2e90403"
Z05_HOSTILE_HASH = "771f529c975e9f0cb7812f4002b9d95c5f5340bc2e6b7c83b1953363ffd81584"

EXPECTED_REVERSE_KEYS = (
    "source", "projection", "c11", "fact", "admission",
    "v554", "v555", "v556", "v557", "v558",
)


def _load():
    spec = importlib.util.spec_from_file_location("z05_vertical_proof_native", HARNESS_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_current_line_reexecutes_z05_and_reproduces_exact_receipt_identities(tmp_path):
    z05 = _load()
    out = tmp_path / "native-run"
    assert z05.run(out) == 0
    summary = json.loads((out / "PROOF_SUMMARY.json").read_text())
    assert summary["graph_hash"] == Z05_GRAPH_HASH
    assert summary["explanation_hash"] == Z05_EXPLANATION_HASH
    assert summary["terminal_ref"]["content_hash"] == Z05_TERMINAL_HASH
    assert summary["mutation_receipt_hash"] == Z05_MUTATION_HASH
    assert summary["restart_receipt_hash"] == Z05_RESTART_HASH
    assert summary["hostile_receipt_hash"] == Z05_HOSTILE_HASH

    hostile = json.loads((out / "HOSTILE_TEST_RECEIPT.json").read_text())
    assert hostile["result"] == "PASS"
    assert hostile["passed"] == 8
    assert hostile["failed"] == 0


def test_representative_source_to_terminal_reverse_lineage_and_current_anchors():
    z05 = _load()
    manifest, nodes, _ = z05.build(z05.fixture())
    critical = tuple(
        node["key"] for node in manifest["nodes"]
        if node["critical"] and node["key"] != "audit"
    )
    assert critical == EXPECTED_REVERSE_KEYS
    assert manifest["graph_hash"] == Z05_GRAPH_HASH
    assert manifest["explanation_hash"] == Z05_EXPLANATION_HASH
    assert manifest["terminal_ref"]["content_hash"] == Z05_TERMINAL_HASH

    assert nodes["source"]["ref"]["content_hash"] == z05.SOURCE
    assert nodes["projection"]["ref"]["content_hash"] == z05.PROJECTION
    assert nodes["c11"]["ref"]["content_hash"] == z05.C11
    assert nodes["fact"]["ref"]["content_hash"] == z05.FACT
    assert z05.SOURCE == "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
    assert z05.PROJECTION == "9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06"
    assert z05.C11 == "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
    assert z05.FACT == "516c1a8b1bfa2f84a39f0423220ecb37f8880e8916e961e61909f5cc933d7cd8"


def test_forward_edge_roles_authority_order_cardinality_and_multiplicity_are_exact():
    z05 = _load()
    specs = z05.fixture()
    manifest, nodes, _ = z05.build(specs)
    edges = {(edge["parent"], edge["child"]): edge for edge in manifest["edges"]}

    for child_spec in specs:
        child = child_spec["k"]
        for (
            parent, producer_role, consumer_role, authority_roles,
            cardinality, multiplicity, ordered, ordinal,
        ) in child_spec["p"]:
            edge = edges[(parent, child)]
            assert edge["producer_role"] == producer_role == nodes[parent]["producer_role"]
            assert edge["consumer_role"] == consumer_role
            assert tuple(edge["authority_roles"]) == tuple(authority_roles)
            assert edge["declared_cardinality"] == cardinality
            assert edge["multiplicity_key"] == multiplicity
            assert edge["order_significant"] is ordered
            assert edge["semantic_ordinal"] == ordinal

    v556 = edges[("v555", "v556")]
    assert v556["declared_cardinality"] == "ONE_OF_ONE"
    assert v556["multiplicity_key"] == "route-0"
    assert v556["order_significant"] is True
    assert v556["semantic_ordinal"] == 1


def test_selective_determinant_invalidation_recomputes_only_transitive_descendants():
    z05 = _load()
    baseline, before, _ = z05.build(z05.fixture())
    mutated, receipt = z05.invalidation(z05.fixture(), "v555")
    assert receipt["exact_stale_keys"] == ["v555", "v556", "v557", "v558"]
    assert receipt["changed_identity_keys"] == ["v555", "v556", "v557", "v558"]
    assert receipt["unrelated_identity_stability"] == "PASS"
    assert receipt["receipt_hash"] == Z05_MUTATION_HASH
    assert baseline["terminal_ref"] != mutated["terminal_ref"]

    _, after, _ = z05.build(z05.fixture("R2"))
    for key in ("source", "projection", "c11", "fact", "admission", "v554", "audit"):
        assert before[key]["ref"] == after[key]["ref"]


def test_destructive_cacheless_rebuild_and_relayout_materialization_identity_parity(tmp_path):
    z05 = _load()
    first_manifest, _, _ = z05.build(z05.fixture())
    first_identity = (
        first_manifest["graph_hash"],
        first_manifest["terminal_ref"],
        first_manifest["explanation_hash"],
    )

    cache = tmp_path / "cache"
    cache.mkdir()
    (cache / "materialized.json").write_text(json.dumps(first_manifest))
    for path in cache.iterdir():
        path.unlink()
    cache.rmdir()

    rebuilt, _, _ = z05.build(z05.fixture())
    rebuilt_identity = (
        rebuilt["graph_hash"], rebuilt["terminal_ref"], rebuilt["explanation_hash"]
    )
    assert rebuilt_identity == first_identity

    out_a = tmp_path / "layout-a"
    out_b = tmp_path / "different-materialization-layout"
    z05.run(out_a)
    z05.run(out_b)
    summary_a = json.loads((out_a / "PROOF_SUMMARY.json").read_text())
    summary_b = json.loads((out_b / "PROOF_SUMMARY.json").read_text())
    assert summary_a == summary_b


def test_interrupted_stage_promotion_and_current_root_recovery_are_atomic(tmp_path):
    z05 = _load()
    baseline, _, _ = z05.build(z05.fixture())
    mutated, _ = z05.invalidation(z05.fixture(), "v555")
    store = z05.Store(tmp_path)

    g1 = store.stage(baseline)
    store.promote(g1)
    current_before = store.recover()
    assert current_before["generation_id"] == g1

    g2 = store.stage(mutated)
    store.promote(g2, interrupt=True)
    interrupted = z05.Store(tmp_path).recover()
    assert interrupted["generation_id"] == g1
    assert interrupted["terminal_ref"] == baseline["terminal_ref"]

    store.promote(g2)
    completed = z05.Store(tmp_path).recover()
    assert completed["generation_id"] == g2
    assert completed["terminal_ref"] == mutated["terminal_ref"]
    assert completed["terminal_ref"] != current_before["terminal_ref"]


def test_stale_corrupt_and_incomplete_lineage_fail_closed(tmp_path):
    z05 = _load()
    manifest, _, _ = z05.build(z05.fixture())
    store = z05.Store(tmp_path)
    gid = store.stage(manifest)
    store.promote(gid)

    generation_path = tmp_path / f"generation-{gid}.json"
    original_generation = generation_path.read_text()
    generation_path.write_text(original_generation.replace('"graph_hash":"', '"graph_hash":"0', 1))
    with pytest.raises(z05.FailClosed):
        z05.Store(tmp_path).recover()
    generation_path.write_text(original_generation)

    current_path = tmp_path / "CURRENT.json"
    original_current = current_path.read_text()
    current = json.loads(original_current)
    current["graph_hash"] = "0" * 64
    current_path.write_text(json.dumps(current))
    with pytest.raises(z05.FailClosed):
        z05.Store(tmp_path).recover()
    current_path.write_text(original_current)

    incomplete = z05.fixture()
    incomplete[-1] = {**incomplete[-1], "critical": True}
    with pytest.raises(z05.FailClosed, match="terminal omits critical determinants"):
        z05.build(incomplete)

    role_drift = z05.fixture()
    v556 = next(spec for spec in role_drift if spec["k"] == "v556")
    bad_parent = list(v556["p"][0])
    bad_parent[1] = "WRONG_PRODUCER_ROLE"
    v556["p"] = [tuple(bad_parent)]
    with pytest.raises(z05.FailClosed, match="producer-role drift"):
        z05.build(role_drift)


def test_bounded_claim_and_architecture_neutrality_are_enforced_by_native_surface():
    z05 = _load()
    source = HARNESS_PATH.read_text()
    assert "court-local proof harness" in source.lower()
    assert "ranks no" in source.lower()
    assert "proof_fixture" in source
    assert "NO_NEW_STRUCTURAL_MEANING" in source
    assert "court mutation only authorizes v555 proof determinant" in source
