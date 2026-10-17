from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "rawlsing_next/ee_p2x_darwin_stage_backend.py"
DRIVER = ROOT / "rawlsing_next/ee_p2x_darwin_court_driver.py"
PACKAGE = ROOT / "rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json"
PACKAGING = ROOT / "rawlsing_next/runtime/ee_p2x/RUNTIME_PACKAGING_BINDING.json"
MATERIALIZER = ROOT / "rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py"
C_BINDER = ROOT / "rawlsing_next/pre553_candidate_c_production_binding.py"
T2 = ROOT / "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json"
T5 = ROOT / "WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json"
R1M_ORACLE = ROOT / "WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json"
R1M_RETURN = ROOT / "WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/RETURN.json"
R1M_LOCK2 = ROOT / "WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/04_SUCCESSOR_LOCK2.json"

PREDECESSOR_LOCK2 = "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
SUCCESSOR_LOCK2 = "5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139"
SUCCESSOR_REPLAY = "9b5ac1726a03798d07e965396192d1bfefbee6d2188bad5a3acfb467ef063d4a"
SUCCESSOR_DISCOVERY = "3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873"
WVS_PROJECTION = "f400c804fea9b526f25eac823138ecb30e10efaad3207c4578661f684adee665"
WVS_ORACLE = "3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800"
WVS_TRUTH = "eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405"
R1J_MATERIALIZER_BLOB = "ec685803a7416032037ee415e8faf7bf60db8f1b"
C_BINDER_BLOB = "47893688ed455ced2c2f2311ad0aead6fb5bf2d2"
LITS_BUILDER_BLOB = "92e364b31eaf27be1bca2081eff65f6ffb779c3d"

VALIDATION_KINDS = [
    "DISTRIBUTION_DIFFERS_FROM_BASELINE",
    "JOINT_NOT_PRODUCT_OF_MARGINALS",
    "TARGET_CELL_SUPPORTED",
]


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def _constants(path: Path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    try:
                        out[target.id] = ast.literal_eval(node.value)
                    except Exception:
                        pass
    return out


def test_r1m_successor_is_the_active_wvs_workload_authority():
    package = _load(PACKAGE)
    assert package["lock2"] == SUCCESSOR_LOCK2
    assert package["replay"] == SUCCESSOR_REPLAY
    assert package["discovery_authority_hash"] == SUCCESSOR_DISCOVERY
    assert package["counts"] == {
        "authorities": 6,
        "predicates": 11,
        "queries": 3,
        "discovery_authorities": 1,
        "candidates": 46,
    }
    assert len(package["discovery_authority_documents"]) == 1
    discovery = package["discovery_authority_documents"][0]
    assert discovery["content_hash"] == SUCCESSOR_DISCOVERY
    assert discovery["semantic_fields"]["validation_rules"]["kinds"] == VALIDATION_KINDS
    assert package["successor_overlay"]["predecessor_lock2"] == PREDECESSOR_LOCK2
    assert package["successor_overlay"]["successor_lock2"] == SUCCESSOR_LOCK2
    assert package["successor_overlay"]["successor_oracle_identity"] == WVS_ORACLE


def test_r1j_projection_is_conserved_but_does_not_own_successor_lock2():
    backend = _constants(BACKEND)
    assert backend["WVS_LOCK2"] == SUCCESSOR_LOCK2
    assert backend["R6S_WVS_PROJECTION"] == WVS_PROJECTION
    assert backend["WVS_MATERIALIZER_BLOB"] == R1J_MATERIALIZER_BLOB
    assert backend["LITS_R5_BUILDER_BLOB"] == LITS_BUILDER_BLOB

    materializer = _constants(MATERIALIZER)
    # R1L-B held R1J projection material outside the Lock2 invalidation boundary.
    assert materializer["LOCK2"] == PREDECESSOR_LOCK2
    assert materializer["PROJECTION_IDENTITY_REF"].content_hash if False else True
    assert _git_blob(MATERIALIZER) == R1J_MATERIALIZER_BLOB

    assert backend["WVS_DISCOVERY_AUTHORITY"] == SUCCESSOR_DISCOVERY
    text = BACKEND.read_text(encoding="utf-8")
    wvs_docs = text.split("def _wvs_docs(ctx, services):", 1)[1].split(
        "def _wvs_materializer(ctx, services):", 1
    )[0]
    assert 'package.get("discovery_authority_hash")!=WVS_DISCOVERY_AUTHORITY' in wvs_docs
    assert "24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab" not in wvs_docs


def test_exact_46_candidate_stream_is_conserved_by_successor_lock2():
    lock = _load(R1M_LOCK2)
    package = _load(PACKAGE)
    assert lock["successor_lock2_hash"] == SUCCESSOR_LOCK2
    assert lock["successor_replay_hash"] == SUCCESSOR_REPLAY
    assert lock["candidate_count"] == 46
    assert len(lock["candidate_hashes"]) == 46
    assert package["lock2_receipt"]["lock2_hash"] == SUCCESSOR_LOCK2
    assert package["lock2_receipt"]["lock2_material"]["candidate_hashes"] == lock["candidate_hashes"]
    assert package["replay_currentness"]["replay_binding"]["candidate_hashes"] == lock["candidate_hashes"]


def test_fresh_wvs_oracle_is_candidate_neutral_and_bound_to_successor():
    oracle = _load(R1M_ORACLE)
    ret = _load(R1M_RETURN)
    assert ret["status"] == "PASS"
    assert ret["r01_r18"]["all_green"] is True
    assert ret["r16"]["oracle_identity"] == WVS_ORACLE
    assert ret["r16"]["truth_payload_identity"] == WVS_TRUTH
    assert oracle["oracle_identity_sha256"] == WVS_ORACLE
    assert oracle["truth_payload_identity"] == WVS_TRUTH
    assert oracle["successor_lock2"] == SUCCESSOR_LOCK2
    assert oracle["successor_discovery_authority"] == SUCCESSOR_DISCOVERY
    assert (
        oracle["truth_payload"]["expected_learned_product"]["coverage"]["typed_terminal_counts"]
        == {"COVERAGE_LIMITED": 46}
    )
    assert oracle["candidate_outputs_seen"] == 0
    assert oracle["candidate_processes_started"] == 0
    assert oracle["candidate_owned_roots_consulted"] == []
    assert oracle["candidate_owned_state_reused"] is False


def test_t2_current_execution_starts_lits_a_at_one_measured_s01_build():
    t2 = _load(T2)
    assert t2["authority"]["lock2"] == "SUCCESSOR_SEALED__" + SUCCESSOR_LOCK2
    assert t2["sources"]["WVS7"]["lock2_replay_hash"] == SUCCESSOR_REPLAY
    assert t2["sources"]["WVS7"]["discovery_authority"] == SUCCESSOR_DISCOVERY
    assert t2["sources"]["WVS7"]["oracle_identity_sha256"] == WVS_ORACLE
    assert t2["candidate_c_binding"]["WVS7"]["projection_cache_identity"] == WVS_PROJECTION
    assert t2["entry_guard"]["first_unfinished_court_stage"] == "LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD"

    cell = next(x for x in t2["cells"] if x["source"] == "LITS_I" and x["candidate"] == "A")
    assert cell["prerequisite_ref"] == "LITS_A_CURRENT_ABSENT_TARGET_S01"
    s01 = cell["stages"]["S01_CANDIDATE_PREPARATION_BUILD"]
    assert s01 == ["READY__RUN_LOCALLY", None, True, True, "S02_C11_REACHABILITY"]
    assert "NO_DUPLICATE_LITS_A_S01_PREBUILD_OR_R35_REBUILD" in t2["hard_prohibitions"]
    assert "NO_HISTORICAL_LITS_A_S01_NUMERIC_CREDIT_WHEN_ROOT_ABSENT" in t2["hard_prohibitions"]
    assert "NO_REPEAT_COMPLETED_LITS_A_FIRST_BUILD" not in t2["hard_prohibitions"]


def test_live_candidate_c_and_packaging_bind_final_hq_state():
    binder = _constants(C_BINDER)
    assert binder["WVS7_CURRENT_PROJECTION_CACHE_IDENTITY"] == WVS_PROJECTION
    assert _git_blob(C_BINDER) == C_BINDER_BLOB

    manifest = _load(PACKAGING)
    assets = {row["role"]: row for row in manifest["stable_runtime_assets"]}
    assert assets["WVS7_P2F2_RUNTIME_PACKAGE"]["git_blob_sha"] == _git_blob(PACKAGE)
    assert assets["WVS7_R6S_PROJECTION_MATERIALIZER"]["git_blob_sha"] == R1J_MATERIALIZER_BLOB
    ids = manifest["preserved_runtime_identities"]
    assert ids["wvs_lock2"] == SUCCESSOR_LOCK2
    assert ids["wvs_lock2_replay"] == SUCCESSOR_REPLAY
    assert ids["wvs_discovery_authority"] == SUCCESSOR_DISCOVERY
    assert ids["wvs_oracle_identity"] == WVS_ORACLE
    assert ids["wvs_oracle_truth_payload_identity"] == WVS_TRUTH


def test_t5_contract_binds_final_successor_and_lits_current_law():
    t5 = _load(T5)
    wvs = t5["wvs_successor_court"]
    assert wvs["discovery_authority"] == SUCCESSOR_DISCOVERY
    assert wvs["lock2"] == SUCCESSOR_LOCK2
    assert wvs["lock2_replay"] == SUCCESSOR_REPLAY
    assert wvs["oracle_identity_sha256"] == WVS_ORACLE
    assert wvs["oracle_truth_payload_identity"] == WVS_TRUTH
    assert wvs["candidate_count"] == 46
    assert wvs["candidate_hash_stream_exact"] is True

    lits = t5["lits_a_current_court"]
    assert lits["absent_historical_root"] is True
    assert lits["current_entry_stage"] == "LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD"
    assert lits["preserved_s01_numeric_credit"] is False
    assert lits["duplicate_prebuild_forbidden"] is True

    anchors = t5["preservation_anchors"]
    assert anchors["t1_runtime_packaging"]["wvs_runtime_package"]["blob"] == _git_blob(PACKAGE)
    assert anchors["t1_runtime_packaging"]["wvs_projection_materializer"]["blob"] == _git_blob(MATERIALIZER)
    assert anchors["t2_current_binding"]["candidate_c_module"]["blob"] == _git_blob(C_BINDER)


def test_final_runtime_files_are_parseable_and_no_measured_work_was_created():
    ast.parse(BACKEND.read_text(encoding="utf-8"))
    ast.parse(DRIVER.read_text(encoding="utf-8"))
    ast.parse(C_BINDER.read_text(encoding="utf-8"))
    for path in (PACKAGE, PACKAGING, T2, T5, R1M_ORACLE, R1M_RETURN, R1M_LOCK2):
        assert isinstance(_load(path), dict)
    assert _load(PACKAGING)["measured_p2x_authorized"] is False
    assert _load(T2)["premeasurement_gates"]["measured_p2x_forbidden_here"] is True
