from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
RET = ROOT / "WORKER_RETURNS" / "EE-P2R6R"
OLD_R5B = ROOT / "WORKER_RETURNS" / "EE-P2R6B" / "SUPPORT" / "R5B" / "05_SUCCESSOR_RELEASE_VERIFIER.py"
NEW_R5B = RET / "02_REPAIRED_SUCCESSOR_RELEASE_VERIFIER.py"
OLD_ISSUER = ROOT / "WORKER_RETURNS" / "EE-P2R6B" / "02_REALIZATION_BINDING_ISSUER.py"
NEW_ISSUER = RET / "03_REPAIRED_R6B_BINDING_ISSUER.py"
OLD_BINDING_VERIFIER = ROOT / "WORKER_RETURNS" / "EE-P2R6B" / "03_REALIZATION_BINDING_VERIFIER.py"
NEW_BINDING_VERIFIER = RET / "04_REPAIRED_R6B_BINDING_VERIFIER.py"

OLD_R5B_BLOB = "348c533a3dff477c3ea0c2f19b41a4e131ef3d3f"
NEW_R5B_BLOB = "e7752c558c7fb407852ef7377f45eca775d3b86b"
OLD_ISSUER_BLOB = "c83058ec51ef731166bde06465a3b72c022c9c47"
NEW_ISSUER_BLOB = "8fd59bc69cd549c39b81bef7d44bb96c1bc0b7c6"
OLD_BINDING_VERIFIER_BLOB = "641f1e50af416441cba7650956123aa1d32f9b59"
NEW_BINDING_VERIFIER_BLOB = "94d4b6a500925b62fd016b57870083f4d41fc85d"
AUTHORITY_EPOCH = "30815cfb20f4f66140cee8f6a2b5e5cafd5e20fb4d1b0c607bad1e3699fae2ff"

TRUNCATED_BLOCK = """EXPECTED_SCAN = {
    "q310": {
        "counts": {"1": 12340, "2": 7511, "3": 9085, "MISSING": 66},
        "row_semantic_root_sha256": "a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455",
    },
    "q311": {
        "counts": {"1": 16582, "2": 4548, "3": 7826, "MISSING": 46},
        "row_semantic_root_sha256": "af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa",
    },
}"""

COMPLETE_BLOCK = """EXPECTED_SCAN = {
    "q310": {
        "counts": {"1": 12340, "2": 7511, "3": 9085, "MISSING": 66},
        "row_semantic_root_sha256": "a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455",
        "selector_roots": {
            "1": "0a62f6f0e3d78b429022b95c2594a3fcbf053b8af588f0ceb304ac3dafe700d2",
            "2": "0bad1e397f5b74b6136ba82e8d81fc608d1df7124e6ff043048cc5cd91ef9c83",
            "3": "b477bf705a93bb672d9ae670a1daa38013c2aa2841d0c506f722ab1bbdbb2f3d",
            "MISSING": "810a81a5663c05dcd0e2f4c2c972f66dc16e7446c87054bb412242632dc57348",
        },
    },
    "q311": {
        "counts": {"1": 16582, "2": 4548, "3": 7826, "MISSING": 46},
        "row_semantic_root_sha256": "af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa",
        "selector_roots": {
            "1": "bffb9d2e9da447a27aaf7c8f889a07d5c47389a58ad933d3ea9867f83e127869",
            "2": "43ffb4ef1de60354b9c943135fd0f31ee54d31edbcd3bb6abf147e5bff1dce1f",
            "3": "642a70ba00a4f7292d96267647068c3bfc83f5efc75451ce00a7df4cd2d62837",
            "MISSING": "847c4e89a7336a5cb5ac6d73953b87091640231ba7cd5c5376e37044a12a03fb",
        },
    },
}"""


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    h = hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode("ascii"))
    h.update(data)
    return h.hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_repaired_r5b_is_exact_old_verifier_plus_complete_scan_only():
    old = OLD_R5B.read_text(encoding="utf-8")
    new = NEW_R5B.read_text(encoding="utf-8")
    assert git_blob_sha1(OLD_R5B) == OLD_R5B_BLOB
    assert git_blob_sha1(NEW_R5B) == NEW_R5B_BLOB
    assert old.count(TRUNCATED_BLOCK) == 1
    assert new == old.replace(TRUNCATED_BLOCK, COMPLETE_BLOCK)
    ast.parse(new, filename=str(NEW_R5B))
    assert new.count('if scan.get("source_scan") != EXPECTED_SCAN:') == 1


def test_complete_scan_passes_and_all_required_hostiles_fail():
    old = load_module(OLD_R5B, "ee_p2r6r_old_r5b")
    repaired = load_module(NEW_R5B, "ee_p2r6r_repaired_r5b")
    exact = copy.deepcopy(repaired.EXPECTED_SCAN)
    assert old.EXPECTED_SCAN != exact
    assert set(exact) == {"q310", "q311"}
    for q in ("q310", "q311"):
        assert set(exact[q]) == {"counts", "row_semantic_root_sha256", "selector_roots"}
        assert set(exact[q]["selector_roots"]) == {"1", "2", "3", "MISSING"}

    hostile = copy.deepcopy(exact)
    del hostile["q310"]["selector_roots"]
    assert hostile != repaired.EXPECTED_SCAN

    hostile = copy.deepcopy(exact)
    hostile["q311"]["selector_roots"]["2"] = "0" * 64
    assert hostile != repaired.EXPECTED_SCAN

    hostile = copy.deepcopy(exact)
    hostile["q310"]["counts"]["1"] += 1
    assert hostile != repaired.EXPECTED_SCAN

    hostile = copy.deepcopy(exact)
    hostile["q311"]["row_semantic_root_sha256"] = "f" * 64
    assert hostile != repaired.EXPECTED_SCAN

    hostile = copy.deepcopy(exact)
    hostile["unexpected"] = {}
    assert hostile != repaired.EXPECTED_SCAN


def test_refreshed_issuer_is_exact_r6b_plus_repaired_r5b_pin_only():
    old = OLD_ISSUER.read_text(encoding="utf-8")
    new = NEW_ISSUER.read_text(encoding="utf-8")
    old_path = 'R5B_VERIFIER = HERE / "SUPPORT" / "R5B" / "05_SUCCESSOR_RELEASE_VERIFIER.py"'
    new_path = 'R5B_VERIFIER = HERE / "02_REPAIRED_SUCCESSOR_RELEASE_VERIFIER.py"'
    old_pin = 'R5B_VERIFIER_GIT_BLOB_SHA1 = "348c533a3dff477c3ea0c2f19b41a4e131ef3d3f"'
    new_pin = 'R5B_VERIFIER_GIT_BLOB_SHA1 = "e7752c558c7fb407852ef7377f45eca775d3b86b"'
    assert git_blob_sha1(OLD_ISSUER) == OLD_ISSUER_BLOB
    assert git_blob_sha1(NEW_ISSUER) == NEW_ISSUER_BLOB
    assert old.count(old_path) == 1 and old.count(old_pin) == 1
    assert new == old.replace(old_path, new_path).replace(old_pin, new_pin)
    ast.parse(new, filename=str(NEW_ISSUER))


def test_refreshed_binding_verifier_is_exact_r6b_plus_issuer_pin_only():
    old = OLD_BINDING_VERIFIER.read_text(encoding="utf-8")
    new = NEW_BINDING_VERIFIER.read_text(encoding="utf-8")
    old_path = 'ISSUER_PATH = HERE / "02_REALIZATION_BINDING_ISSUER.py"'
    new_path = 'ISSUER_PATH = HERE / "03_REPAIRED_R6B_BINDING_ISSUER.py"'
    old_pin = 'EXPECTED_ISSUER_GIT_BLOB_SHA1 = "c83058ec51ef731166bde06465a3b72c022c9c47"'
    new_pin = 'EXPECTED_ISSUER_GIT_BLOB_SHA1 = "8fd59bc69cd549c39b81bef7d44bb96c1bc0b7c6"'
    assert git_blob_sha1(OLD_BINDING_VERIFIER) == OLD_BINDING_VERIFIER_BLOB
    assert git_blob_sha1(NEW_BINDING_VERIFIER) == NEW_BINDING_VERIFIER_BLOB
    assert old.count(old_path) == 1 and old.count(old_pin) == 1
    assert new == old.replace(old_path, new_path).replace(old_pin, new_pin)
    ast.parse(new, filename=str(NEW_BINDING_VERIFIER))


def test_authority_epoch_and_nonbinding_semantics_are_preserved():
    issuer = load_module(NEW_ISSUER, "ee_p2r6r_issuer")
    assert issuer.AUTHORITY_EPOCH_ID == AUTHORITY_EPOCH
    assert issuer.sha256_obj(issuer.exact_epoch_material()) == AUTHORITY_EPOCH
    assert issuer.R5B_VERIFIER_GIT_BLOB_SHA1 == NEW_R5B_BLOB
    fixture = issuer.build_nonbinding_structural_fixture_candidate()
    assert fixture["status"] == "NONEMPIRICAL__NONBINDING__STRUCTURAL_FIXTURE"
    assert fixture["actual_release_realization_binding"] is False
    assert fixture["eligible_for_hq_adoption_as_binding"] is False
    assert not list(RET.rglob("release_realization_binding_candidate.json"))


def test_static_proof_and_reverify_packet_enforce_no_carrier_boundary():
    proof = json.loads((RET / "01_STATIC_DEFECT_PROOF.json").read_text(encoding="utf-8"))
    packet = json.loads((RET / "05_EXISTING_R6L_OUTPUT_REVERIFY_PACKET.json").read_text(encoding="utf-8"))
    assert proof["classification"] == "EXPECTED_SCAN_SCHEMA_TRUNCATION__SELECTOR_ROOTS_OMITTED_FROM_VERIFIER_EXPECTATION"
    assert proof["repair"]["driver_modified"] is False
    assert proof["repair"]["preserved_driver_git_blob_sha1"] == "b819fdff50470a71f1c570aa8021e28b361fa986"
    assert proof["empirical_boundary"]["carrier_accessed"] is False
    assert packet["execution_surface"] == "LOCAL-MACHINE CODEX"
    assert packet["maximum_intelligence_required"] == "LUNA"
    assert packet["library_access"] == "NO"
    assert packet["source_reopen"] == "FORBIDDEN"
    assert packet["driver_rerun"] == "FORBIDDEN"
    assert packet["repaired_verifier"]["git_blob_sha1"] == NEW_R5B_BLOB
    assert packet["steps"][0]["action"] == "RUN_REPAIRED_VERIFIER_ONLY"
    assert packet["steps"][0]["source_or_driver_execution"] is False
    assert packet["steps"][0]["on_failure"].startswith("STOP_AT_EXACT_FIRST_LATER_VERIFICATION_CHECK")
