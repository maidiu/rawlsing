from __future__ import annotations

import copy
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
from rawlsing_next.fiabc_lits_astra_substantive_parity import (
    LitsAstraSubstantiveParityError,
    _current_logical_identity,
    _historical_logical_identity,
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


def test_all_fifty_native_provenance_identities_are_preserved(real_current_bindings):
    product = _astra_product()
    native_to_logical, p4_by_cell, historical_logical_rows, historical_provenance = (
        _historical_logical_identity(product)
    )
    current_by_native, current_logical_rows, current_provenance = _current_logical_identity(
        real_current_bindings
    )
    assert len(native_to_logical) == 50
    assert len(current_by_native) == 50
    assert len(historical_logical_rows) == 50
    assert len(current_logical_rows) == 50
    assert len(historical_provenance["rows"]) == 50
    assert len(current_provenance["rows"]) == 50
    assert sum(
        row["provenance_basis"] == "ASTRA_RECORDED_AND_G02_PREIMAGE_RECOMPUTED"
        for row in historical_provenance["rows"]
    ) == 25
    assert sum(
        row["provenance_basis"] == "ACCEPTED_G02_PREIMAGE_DERIVED"
        for row in historical_provenance["rows"]
    ) == 25

    for raw_cell in product["P4_joint_5x5_target_support"]:
        cell = [int(v) for v in raw_cell.split(",")]
        semantics = candidate_semantics(lane="P4", parameters={"target_cell": cell})
        g02_hash = g02_execution_candidate_hash(semantics)
        key = logical_candidate_key(semantics)
        assert native_to_logical[g02_hash] == key
        assert p4_by_cell[json.dumps(cell, separators=(",", ":"))] == key


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


def _reseal_binding(binding):
    material = {k: v for k, v in binding.items() if k != "binding_identity"}
    binding["binding_identity"] = semantic_hash(canonicalize(material))
    return binding


def _one_p2_binding(real_current_bindings):
    return next(
        row
        for row in real_current_bindings
        if row["lane"] == "P2"
        and row["logical_candidate_material"]["candidate_semantics"]["parameters"]
        == {"q301_2": 1, "q310": 1, "q311": 1}
    )


def test_changed_historical_g02_hash_with_fixed_semantics_fails_closed():
    product = _astra_product()
    product["P2_conditioned_frontier"][0]["candidate_hash"] = "0" * 64
    with pytest.raises(LitsAstraSubstantiveParityError, match="native hash"):
        _historical_logical_identity(product)


def test_changed_current_pre553_hash_with_fixed_native_preimage_fails_closed(real_current_bindings):
    rows = copy.deepcopy(list(real_current_bindings))
    target = next(row for row in rows if row["lane"] == "P2")
    target["current_pre553_candidate_hash"] = "1" * 64
    target["current_pre553_candidate_id"] = (
        "urn:rawlsing:pre553:i05:candidate:sha256:" + target["current_pre553_candidate_hash"]
    )
    _reseal_binding(target)
    with pytest.raises(LitsAstraSubstantiveParityError, match="native candidate hash/preimage"):
        _current_logical_identity(rows)


def test_historical_g02_hash_injected_as_current_pre553_hash_fails_closed(real_current_bindings):
    product = _astra_product()
    historical = product["P2_conditioned_frontier"][0]
    key = logical_candidate_key(candidate_semantics(lane="P2", parameters=historical["parameters"]))
    rows = copy.deepcopy(list(real_current_bindings))
    target = next(row for row in rows if row["logical_candidate_key"] == key)
    target["current_pre553_candidate_hash"] = historical["candidate_hash"]
    target["current_pre553_candidate_id"] = (
        "urn:rawlsing:pre553:i05:candidate:sha256:" + historical["candidate_hash"]
    )
    _reseal_binding(target)
    with pytest.raises(LitsAstraSubstantiveParityError, match="native candidate hash/preimage"):
        _current_logical_identity(rows)


@pytest.mark.parametrize(
    "role,ref_field,error_fragment",
    [
        ("CONDITION", "current_predicate_ref", "CONDITION predicate/native-preimage"),
        ("CONDITION", "current_query_ref", "CONDITION query/native-preimage"),
        ("BASELINE", "current_predicate_ref", "BASELINE predicate/native-preimage"),
        ("BASELINE", "current_query_ref", "BASELINE query/native-preimage"),
    ],
)
def test_p2_exact_current_role_ref_mutation_fails_closed(
    real_current_bindings, role, ref_field, error_fragment
):
    rows = copy.deepcopy(list(real_current_bindings))
    target = next(row for row in rows if row["lane"] == "P2")
    role_row = next(x for x in target["role_bindings"] if x["role"] == role)
    hostile = copy.deepcopy(role_row[ref_field])
    hostile["content_hash"] = "2" * 64
    hostile["object_id"] = f"urn:hostile:{role.lower()}:{ref_field}:sha256:{'2' * 64}"
    role_row[ref_field] = hostile
    _reseal_binding(target)
    with pytest.raises(LitsAstraSubstantiveParityError, match=error_fragment):
        _current_logical_identity(rows)


def test_p2_query_role_semantic_template_drift_fails_closed(real_current_bindings):
    rows = copy.deepcopy(list(real_current_bindings))
    target = next(row for row in rows if row["lane"] == "P2")
    condition = next(x for x in target["role_bindings"] if x["role"] == "CONDITION")
    condition["logical_query_template_id"] = "T_Q301_2_RAW"
    _reseal_binding(target)
    with pytest.raises(LitsAstraSubstantiveParityError, match="logical query-template"):
        _current_logical_identity(rows)


@pytest.mark.parametrize("field,value", [("q301_2", 5), ("q310", 2), ("q311", 3)])
def test_p2_parameter_substitution_with_native_refs_held_fixed_fails_closed(
    real_current_bindings, field, value
):
    rows = copy.deepcopy(list(real_current_bindings))
    target = next(
        row
        for row in rows
        if row["lane"] == "P2"
        and row["logical_candidate_material"]["candidate_semantics"]["parameters"]
        == {"q301_2": 1, "q310": 1, "q311": 1}
    )
    params = {"q301_2": 1, "q310": 1, "q311": 1}
    params[field] = value
    semantics = candidate_semantics(lane="P2", parameters=params)
    target["logical_candidate_material"] = logical_candidate_material(semantics)
    target["logical_candidate_key"] = logical_candidate_key(semantics)
    _reseal_binding(target)
    with pytest.raises(LitsAstraSubstantiveParityError):
        _current_logical_identity(rows)


def test_distinct_current_candidates_cannot_be_forced_onto_one_shared_key(real_current_bindings):
    rows = copy.deepcopy(list(real_current_bindings))
    first, second = [row for row in rows if row["lane"] == "P2"][:2]
    second["logical_candidate_key"] = first["logical_candidate_key"]
    _reseal_binding(second)
    with pytest.raises(LitsAstraSubstantiveParityError, match="key/material"):
        _current_logical_identity(rows)


def test_arithmetic_equality_cannot_substitute_for_exact_candidate_semantics(real_current_bindings):
    rows = copy.deepcopy(list(real_current_bindings))
    target = _one_p2_binding(rows)
    original_native_hash = target["current_pre553_candidate_hash"]
    original_roles = copy.deepcopy(target["role_bindings"])
    semantics = candidate_semantics(
        lane="P2",
        parameters={"q301_2": 5, "q310": 3, "q311": 3},
    )
    target["logical_candidate_material"] = logical_candidate_material(semantics)
    target["logical_candidate_key"] = logical_candidate_key(semantics)
    _reseal_binding(target)
    assert target["current_pre553_candidate_hash"] == original_native_hash
    assert target["role_bindings"] == original_roles
    with pytest.raises(LitsAstraSubstantiveParityError):
        _current_logical_identity(rows)
