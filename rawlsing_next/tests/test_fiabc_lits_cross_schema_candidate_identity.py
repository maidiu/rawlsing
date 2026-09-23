from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

from rawlsing_next.fiabc_lits_cross_schema_candidate_identity import (
    CrossSchemaCandidateIdentityError,
    candidate_semantics,
    g02_execution_candidate_hash,
    logical_candidate_key,
    logical_candidate_material,
)
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash


ROOT = Path(__file__).resolve().parents[2]
MATERIALIZER = ROOT / "rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py"
ASTRA_COMMIT = "e631de162c582423639b7067a4f36b29f8aa4d89"
ASTRA_PRODUCT = "WORKER_RETURNS/ASTRA-D04-R2/01_TYPED_LEARNED_EMPIRICAL_PRODUCT.json"


def _support():
    spec = importlib.util.spec_from_file_location("_fiabc_cross_schema_lits_materializer", MATERIALIZER)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _astra_product():
    subprocess.run(
        ["git", "fetch", "--no-tags", "origin", ASTRA_COMMIT],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    raw = subprocess.check_output(["git", "show", f"{ASTRA_COMMIT}:{ASTRA_PRODUCT}"], cwd=ROOT)
    return json.loads(raw)


@pytest.fixture(scope="module")
def real_current_bindings():
    package = _support().materialize_runtime_package()
    rows = package["cross_schema_logical_candidate_bindings"]
    assert package["candidate_count"] == 50
    assert package["query_role_executions"] == 77
    assert len(rows) == 50
    assert len({x["logical_candidate_key"] for x in rows}) == 50
    assert len({x["current_pre553_candidate_hash"] for x in rows}) == 50
    for row in rows:
        assert semantic_hash(row["logical_candidate_material"]) == row["logical_candidate_key"]
    return rows


def _historical_semantics_rows(product):
    rows = []
    for item in product["P0_positive_controls"]:
        rows.append(("P0", {"target_cell": item["target_cell"]}, item["candidate_hash"]))
    p1 = product["P1_joint_dependence"]
    rows.append(("P1", {}, p1["candidate_hash"]))
    for item in product["P2_conditioned_frontier"]:
        rows.append(("P2", item["parameters"], item["candidate_hash"]))
    p3 = product["P3_conditional_reversal"]
    rows.append((
        "P3",
        {"stratum_atom_ids": ["Q310V1", "Q310V2", "Q310V3"]},
        p3["candidate_hash"],
    ))
    return rows


def test_historical_g02_hashes_recompute_from_immutable_candidate_semantics(real_current_bindings):
    product = _astra_product()
    current = {row["logical_candidate_key"]: row for row in real_current_bindings}
    historical_keys = set()
    for lane, params, native_hash in _historical_semantics_rows(product):
        semantics = candidate_semantics(lane=lane, parameters=params)
        key = logical_candidate_key(semantics)
        historical_keys.add(key)
        assert g02_execution_candidate_hash(semantics) == native_hash
        assert key in current
        assert current[key]["current_pre553_candidate_hash"] != native_hash
    assert len(historical_keys) == 25


def test_p2_exact_parameters_and_current_condition_baseline_refs_are_bound(real_current_bindings):
    product = _astra_product()
    current = {row["logical_candidate_key"]: row for row in real_current_bindings}
    seen = set()
    for item in product["P2_conditioned_frontier"]:
        params = item["parameters"]
        semantics = candidate_semantics(lane="P2", parameters=params)
        key = logical_candidate_key(semantics)
        binding = current[key]
        assert binding["lane"] == "P2"
        assert binding["logical_candidate_material"] == logical_candidate_material(semantics)
        roles = {row["role"]: row for row in binding["role_bindings"]}
        assert set(roles) == {"CONDITION", "BASELINE"}
        for role in ("CONDITION", "BASELINE"):
            assert roles[role]["current_predicate_ref"]["kind"] == "EmpiricalPredicate@1.0.0"
            assert roles[role]["current_query_ref"]["kind"] == "EmpiricalQuerySpec@1.0.0"
            assert len(roles[role]["current_predicate_ref"]["content_hash"]) == 64
            assert len(roles[role]["current_query_ref"]["content_hash"]) == 64
        seen.add((params["q301_2"], params["q310"], params["q311"]))
    assert seen == {
        (q2, q310, q311)
        for q2 in (1, 5)
        for q310 in (1, 2, 3)
        for q311 in (1, 2, 3)
    }


def test_all_fifty_shared_logical_candidates_are_recovered(real_current_bindings):
    product = _astra_product()
    expected = set()
    for lane, params, _native_hash in _historical_semantics_rows(product):
        expected.add(logical_candidate_key(candidate_semantics(lane=lane, parameters=params)))
    for raw_cell in product["P4_joint_5x5_target_support"]:
        cell = [int(v) for v in raw_cell.split(",")]
        expected.add(logical_candidate_key(candidate_semantics(lane="P4", parameters={"target_cell": cell})))
    current = {row["logical_candidate_key"] for row in real_current_bindings}
    assert len(expected) == 50
    assert current == expected


@pytest.mark.parametrize(
    "field,new_value",
    [
        ("q301_2", 5),
        ("q310", 2),
        ("q311", 3),
    ],
)
def test_p2_parameter_mutation_changes_shared_logical_identity(field, new_value):
    base = {"q301_2": 1, "q310": 1, "q311": 1}
    mutated = dict(base)
    mutated[field] = new_value
    assert logical_candidate_key(candidate_semantics(lane="P2", parameters=base)) != logical_candidate_key(
        candidate_semantics(lane="P2", parameters=mutated)
    )


def test_out_of_frontier_p2_and_schema_shortcuts_fail_closed():
    with pytest.raises(CrossSchemaCandidateIdentityError):
        candidate_semantics(lane="P2", parameters={"q301_2": 2, "q310": 1, "q311": 1})
    with pytest.raises(CrossSchemaCandidateIdentityError):
        candidate_semantics(lane="P2", parameters={"q301_2": 1, "q310": 4, "q311": 1})
    with pytest.raises(CrossSchemaCandidateIdentityError):
        candidate_semantics(lane="P2", parameters={"q301_2": 1, "q310": 1})


def test_native_hash_is_not_the_shared_logical_key(real_current_bindings):
    for row in real_current_bindings:
        assert row["current_pre553_candidate_hash"] != row["logical_candidate_key"]
        material = canonicalize(row["logical_candidate_material"])
        assert semantic_hash(material) == row["logical_candidate_key"]
