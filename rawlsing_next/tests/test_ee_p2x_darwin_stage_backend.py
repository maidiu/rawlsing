from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

D02_COMMIT = "40cb8585f076a66d9884b99022a59bb909606c03"
F02_COMMIT = "482bb884a99e31ba77e904d0df39fffc872cbed3"
G02_COMMIT = "01e1e8071ea98587dfbb755ec0fdc0da2f5e1663"

D02_PATH = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/"
    "HQ_FIRST_WAVE_FANIN_AND_SECOND_WAVE_DISPATCH_R1/SECOND_WAVE_WORKER_RETURNS/"
    "W2-D02/01_FROZEN_DISCOVERY_FRONTIER_AUTHORITY.json"
)
F02_PATH = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/"
    "HQ_THIRD_WAVE_FANIN_AND_FOURTH_WAVE_DISPATCH_R1/FOURTH_WAVE_WORKER_RETURNS/"
    "F02/03_LEARNED_FRONTIER_READOPTION_RECEIPT.json"
)
G02_PRODUCER = "rawlsing_next/prev3_learned_real_execution_r2.py"

P2R1_CATALOG = ROOT / "WORKER_RETURNS/EE-P2R1/08_EXACT_RUNTIME_OBJECT_CATALOG_PREIMAGE_RECEIPT.json"
P2R1_C = ROOT / "WORKER_RETURNS/EE-P2R1/11_LITS_C_REAL_DETERMINANT_19_ATOM_BINDING_RECEIPT.json"
BACKEND = ROOT / "rawlsing_next/ee_p2x_darwin_stage_backend.py"

F02_RELEASE = "bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297"
BASE_RELEASE = "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
SELECTOR_HASHES = {
    "c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a",
    "78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df",
    "c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca",
    "69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8",
    "f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849",
    "a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d",
}

_CACHE: dict[tuple[str, str], bytes] = {}


def _show(commit: str, path: str) -> bytes:
    key = (commit, path)
    if key in _CACHE:
        return _CACHE[key]
    probe = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if probe.returncode:
        subprocess.run(
            ["git", "fetch", "--quiet", "--no-tags", "origin", commit],
            cwd=ROOT,
            check=True,
        )
    data = subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)
    _CACHE[key] = data
    return data


def _show_json(commit: str, path: str):
    return json.loads(_show(commit, path))


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_d02_frozen_workload_requires_50_candidates_77_roles_and_six_conditioners():
    d02 = _show_json(D02_COMMIT, D02_PATH)
    grammar = d02["candidate_grammar"]
    assert grammar["expected_compiled_candidate_count"] == 50
    assert grammar["expected_i03_query_execution_count"] == 77
    selectors = d02["frozen_selector_atoms"]
    assert {item["atom_id"] for item in selectors} == {
        "Q310V1", "Q310V2", "Q310V3", "Q311V1", "Q311V2", "Q311V3"
    }
    assert all(item["operation"] == "survey_response_EQ" for item in selectors)


def test_f02_readoption_binds_exact_six_selector_refs_to_composite_release():
    f02 = _show_json(F02_COMMIT, F02_PATH)
    assert f02["new_release_ref"]["content_hash"] == F02_RELEASE
    substitutions = f02["selector_preimage_substitutions"]
    assert len(substitutions) == 6
    assert {value["content_hash"] for value in substitutions.values()} == SELECTOR_HASHES
    assert f02["allowed_mutation"] == "SELECTOR_PREIMAGE_SUBSTITUTION_ONLY"
    assert f02["workload_execution"] == "NOT_EXECUTED"


def test_p2r1_lits_catalog_does_not_materialize_f02_preimages_and_forbids_hash_inversion():
    p2r1 = _load(P2R1_CATALOG)
    assert p2r1["no_hash_inversion"] is True
    lits = p2r1["LITS_I"]
    assert lits["predicates_constructed"] == 19
    assert lits["distinct_predicates"] == 18
    assert lits["queries_constructed"] == 3
    material = P2R1_CATALOG.read_text(encoding="utf-8")
    assert F02_RELEASE not in material
    assert all(selector_hash not in material for selector_hash in SELECTOR_HASHES)


def test_lits_c_owner_binding_is_base_release_only_and_cannot_supply_f02_conditioners():
    c = _load(P2R1_C)
    assert c["c11_release_hash"] == BASE_RELEASE
    assert c["role_bindings"] == 19
    assert c["distinct_runtime_predicates"] == 18
    assert c["third_accelerator_created"] is False
    material = P2R1_C.read_text(encoding="utf-8")
    assert F02_RELEASE not in material
    assert all(selector_hash not in material for selector_hash in SELECTOR_HASHES)


def test_historical_g02_runner_is_direct_record_execution_not_the_adopted_p2r1_seam():
    producer = _show(G02_COMMIT, G02_PRODUCER).decode("utf-8")
    assert "def _query(records,q,atoms):" in producer
    assert "def execute_records(records,compiled):" in producer
    assert "pd.read_stata" in producer
    assert "RuntimeObjectCatalog" not in producer
    assert "execute_empirical_query" not in producer


def test_unqualified_backend_was_withdrawn_instead_of_claiming_pass():
    assert not BACKEND.exists()
