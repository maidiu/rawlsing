from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
RET = ROOT / "WORKER_RETURNS" / "EE-P2R6B"
ISSUER = RET / "02_REALIZATION_BINDING_ISSUER.py"
VERIFIER = RET / "03_REALIZATION_BINDING_VERIFIER.py"
R5B = RET / "SUPPORT" / "R5B" / "05_SUCCESSOR_RELEASE_VERIFIER.py"

EXPECTED_ISSUER = "c83058ec51ef731166bde06465a3b72c022c9c47"
EXPECTED_VERIFIER = "641f1e50af416441cba7650956123aa1d32f9b59"
EXPECTED_R5B = "348c533a3dff477c3ea0c2f19b41a4e131ef3d3f"

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

def test_exact_prepared_blob_chain_and_python_parse():
    assert git_blob_sha1(ISSUER) == EXPECTED_ISSUER
    assert git_blob_sha1(VERIFIER) == EXPECTED_VERIFIER
    assert git_blob_sha1(R5B) == EXPECTED_R5B
    for path in (ISSUER, VERIFIER, R5B):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

def test_authority_epoch_is_exact_and_content_addressed():
    issuer = load_module(ISSUER, "ee_p2r6b_issuer_epoch")
    assert issuer.sha256_obj(issuer.exact_epoch_material()) == issuer.AUTHORITY_EPOCH_ID
    assert issuer.AUTHORITY_EPOCH_ID == "30815cfb20f4f66140cee8f6a2b5e5cafd5e20fb4d1b0c607bad1e3699fae2ff"
    assert issuer.FROZEN_SCOPE_HASH != issuer.BASE_RELEASE_HASH

def test_structural_fixture_is_nonempirical_nonbinding_and_deterministic():
    issuer = load_module(ISSUER, "ee_p2r6b_issuer_fixture")
    a = issuer.build_nonbinding_structural_fixture_candidate()
    b = issuer.build_nonbinding_structural_fixture_candidate()
    assert a == b
    assert a["schema"] == "EE_P2R6B_NONEMPIRICAL_NONBINDING_STRUCTURAL_FIXTURE_CANDIDATE@1.0.0"
    assert a["status"] == "NONEMPIRICAL__NONBINDING__STRUCTURAL_FIXTURE"
    assert a["actual_release_realization_binding"] is False
    assert a["eligible_for_hq_adoption_as_binding"] is False
    assert a["fixture_ref"]["kind"] == "NonbindingStructuralFixture"
    assert a["identity_material"]["empirical_data_present"] is False
    assert a["identity_material"]["binding_authority_present"] is False
    assert "runtime_i02_release_ref" not in a["identity_material"]
    assert a["fixture_ref"]["content_hash"] == issuer.sha256_obj(a["identity_material"])

def test_structural_fixture_uniqueness_fails_closed():
    issuer = load_module(ISSUER, "ee_p2r6b_issuer_fixture_uniqueness")
    with pytest.raises(issuer.IssuerError, match="nonzero active binding"):
        issuer.build_nonbinding_structural_fixture_candidate(active_binding_count=1)

def test_production_issuer_rejects_non_r5b_fixture_before_output(tmp_path: Path):
    receipt = tmp_path / "successor_release_receipt.json"
    receipt.write_text(json.dumps({
        "schema": "EE_P2R6B_NONEMPIRICAL_NONBINDING_STRUCTURAL_FIXTURE_RECEIPT@1.0.0",
        "status": "NONEMPIRICAL__NONBINDING__STRUCTURAL_FIXTURE"
    }) + "\n", encoding="utf-8")
    output = tmp_path / "release_realization_binding_candidate.json"
    proc = subprocess.run([
        sys.executable, str(ISSUER),
        "--receipt", str(receipt),
        "--replay-manifest", str(tmp_path / "successor_release_replay_manifest.json"),
        "--m01-m18", str(tmp_path / "successor_release_m01_m18.json"),
        "--extension-scan", str(tmp_path / "successor_release_extension_scan.json"),
        "--authority-material", str(tmp_path / "authority.json"),
        "--output", str(output),
    ], text=True, capture_output=True, check=False)
    assert proc.returncode == 2
    assert "R5B verifier did not PASS" in proc.stderr
    assert not output.exists()

def test_verifier_rejects_nonproduction_fixture_schema_before_proof_reconstruction(tmp_path: Path):
    verifier = load_module(VERIFIER, "ee_p2r6b_verifier_fixture")
    issuer = load_module(ISSUER, "ee_p2r6b_issuer_for_verifier_fixture")
    candidate = issuer.build_nonbinding_structural_fixture_candidate()
    candidate_path = tmp_path / "fixture_candidate.json"
    authority_path = tmp_path / "authority.json"
    candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
    authority_path.write_text("{}\n", encoding="utf-8")
    with pytest.raises(verifier.VerificationError, match="candidate schema mismatch"):
        verifier.verify_candidate(
            candidate_path=candidate_path,
            receipt_path=tmp_path / "receipt.json",
            replay_path=tmp_path / "replay.json",
            m01_m18_path=tmp_path / "m.json",
            extension_scan_path=tmp_path / "scan.json",
            authority_path=authority_path,
        )

def test_contract_proves_no_actual_binding_emitted_during_browser_preparation():
    contract = json.loads((RET / "01_BINDING_ISSUER_CONTRACT.json").read_text(encoding="utf-8"))
    inputs = json.loads((RET / "04_POST_LOCAL_INPUT_CONTRACT.json").read_text(encoding="utf-8"))
    receipt = json.loads((RET / "05_BROWSER_QUALIFICATION_RECEIPT.json").read_text(encoding="utf-8"))
    assert contract["binding_law"]["runtime_release_hash_predeclared"] is False
    assert contract["browser_fixture_law"]["actual_binding_emission_forbidden"] is True
    assert inputs["runtime_release_identity_law"]["caller_supplied_runtime_hash"] == "FORBIDDEN"
    assert inputs["actual_binding_issued_by_this_r6b_commission"] is False
    assert receipt["actual_successor_runtime_release_ref_present"] is False
    assert receipt["actual_concrete_realization_binding_emitted"] is False
