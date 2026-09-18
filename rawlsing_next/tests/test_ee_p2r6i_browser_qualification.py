from __future__ import annotations
import base64, hashlib, importlib.util, json, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "WORKER_RETURNS" / "EE-P2R6I"
SUPPORT = OUT / "SUPPORT"
R6L = ROOT / "WORKER_RETURNS" / "EE-P2R6L" / "RUN_OUTPUT"
R5B = SUPPORT / "02_REPAIRED_SUCCESSOR_RELEASE_VERIFIER.py"
ISSUER_PATH = SUPPORT / "03_REPAIRED_R6B_BINDING_ISSUER.py"
VERIFIER = SUPPORT / "04_REPAIRED_R6B_BINDING_VERIFIER.py"
SNAPSHOT = SUPPORT / "00_ADOPTED_ZERO_BINDING_REGISTRY_SNAPSHOT.json"

def canonical(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def sha256_file(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def git_blob_sha1(p):
    data = p.read_bytes()
    h = hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode("ascii"))
    h.update(data)
    return h.hexdigest()

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def build_authority(issuer, receipt, snapshot):
    assert issuer.sha256_obj(snapshot["identity_material"]) == snapshot["snapshot_ref"]["content_hash"]
    assert snapshot["snapshot_ref"]["content_hash"] == "9f96121b35fff6b56d69d60cedcea04d91ca1784e7636eded73655ad8b5a7168"
    scope = snapshot["identity_material"]["snapshot_scope"]
    assert scope["uniqueness_key"] == issuer.uniqueness_key() == "659a8929df10b31da4c82eaf5a6b8bd74234b6f21430422beff186cab804fc16"
    assert snapshot["identity_material"]["active_positive_binding_count"] == 0
    assert snapshot["identity_material"]["active_positive_bindings"] == []
    inventory_material = {
        "schema": "EE_P2R6B_ACTIVE_BINDING_INVENTORY@1.0.0",
        "resolution_mode": "EXACT_SCOPE_SOURCE_AUTHORITY_EPOCH",
        "inventory_source_ref": snapshot["snapshot_ref"],
        "frozen_scope_anchor_hash": issuer.FROZEN_SCOPE_HASH,
        "source_sha256": issuer.SOURCE_SHA256,
        "authority_epoch_id": issuer.AUTHORITY_EPOCH_ID,
        "uniqueness_key": issuer.uniqueness_key(),
        "active_positive_bindings": [],
        "active_positive_binding_count": 0,
    }
    inventory = dict(inventory_material)
    inventory["inventory_material_hash"] = issuer.sha256_obj(inventory_material)
    authority = {
        "schema": "EE_P2R6B_ADOPTED_R5A_AUTHORITY_MATERIAL@1.0.0",
        "status": "ADOPTED_R5A_AUTHORITY_MATERIAL__PRE_BINDING",
        "authority_epoch": issuer.exact_epoch_material(),
        "authority_epoch_id": issuer.AUTHORITY_EPOCH_ID,
        "adopted_refs": {
            "release_realization_authority": issuer.RELATION_AUTHORITY_REF,
            "binding_schema": issuer.BINDING_SCHEMA_REF,
            "r4a_successor_clause": issuer.R4A_SUCCESSOR_CLAUSE_REF,
            "r5a_aggregate": issuer.R5A_AGGREGATE_REF,
        },
        "source_sha256": issuer.SOURCE_SHA256,
        "frozen_scope_anchor_ref": issuer.FROZEN_SCOPE_REF,
        "accepted_base_i02_release_ref": issuer.BASE_RELEASE_REF,
        "accepted_base_replay_manifest_hash": issuer.BASE_REPLAY_HASH,
        "r4a_authority_hashes": issuer.R4A_AUTHORITY_HASHES,
        "f02_extension_refs": receipt["extension"]["question_and_member_refs"],
        "selector_refs": receipt["extension"]["selector_refs"],
        "f02_authority_refs": receipt["extension"]["authority_refs"],
        "issuance_guard": {
            "measured_outcomes_observed": False,
            "p2x_executed": False,
            "post_outcome_mutation": False,
            "runtime_release_hash_predeclared": False,
        },
        "active_binding_inventory": inventory,
    }
    issuer.validate_authority_material(authority)
    return authority

def test_ee_p2r6i_exact_concrete_binding_generation_surface_payload():
    assert git_blob_sha1(R5B) == "e7752c558c7fb407852ef7377f45eca775d3b86b"
    assert git_blob_sha1(ISSUER_PATH) == "8fd59bc69cd549c39b81bef7d44bb96c1bc0b7c6"
    assert git_blob_sha1(VERIFIER) == "94d4b6a500925b62fd016b57870083f4d41fc85d"
    issuer = load_module("ee_p2r6i_issuer", ISSUER_PATH)
    receipt_path = R6L / "successor_release_receipt.json"
    m01_path = R6L / "successor_release_m01_m18.json"
    scan_path = R6L / "successor_release_extension_scan.json"
    zip_path = R6L / "successor_release_replay_manifest.json.zip"
    assert sha256_file(receipt_path) == "a011febaf5f4641ba24edc1a2b4dde24be9172d21caade8b940ba5339a3bd533"
    assert sha256_file(m01_path) == "665655afd961bd627776bcca03ac18ae69fdab057927d317eac506e9001fe5ae"
    assert sha256_file(scan_path) == "28454d4148aa814a0637e3f61705691bfd00a019978af06c5b3492d89e695fe2"
    assert zip_path.stat().st_size == 17663792
    assert git_blob_sha1(zip_path) == "d20b8aeee5abe5a1348e5ab17546c82e3592ab6e"
    assert sha256_file(zip_path) == "9d2c608f21d9d93111c7418bce945f6245340389d7e8c2ccff70b18af358dd70"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    authority = build_authority(issuer, receipt, snapshot)
    with tempfile.TemporaryDirectory(prefix="ee-p2r6i-") as td:
        td = Path(td)
        replay_path = td / "successor_release_replay_manifest.json"
        with zipfile.ZipFile(zip_path, "r") as zf:
            infos = zf.infolist()
            assert len(infos) == 1
            assert infos[0].filename == "successor_release_replay_manifest.json"
            assert not infos[0].is_dir()
            with zf.open(infos[0], "r") as src, replay_path.open("wb") as dst:
                shutil.copyfileobj(src, dst, length=1024 * 1024)
        assert replay_path.stat().st_size == 118508673
        assert sha256_file(replay_path) == "aa3b6026d4dbc3df8b142725704974eaef810e5dbf5b31d14b19c88cf8ecafd5"
        temp_receipt = td / "successor_release_receipt.json"
        temp_m01 = td / "successor_release_m01_m18.json"
        temp_scan = td / "successor_release_extension_scan.json"
        shutil.copyfile(receipt_path, temp_receipt)
        shutil.copyfile(m01_path, temp_m01)
        shutil.copyfile(scan_path, temp_scan)
        authority_path = td / "authority.json"
        authority_path.write_text(json.dumps(authority, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        candidate = issuer.issue_binding_candidate(temp_receipt, replay_path, temp_m01, temp_scan, authority_path)
        assert candidate["status"] == "CANDIDATE__HQ_ADOPTION_REQUIRED__NOT_ACTIVE_UNTIL_ADOPTED"
        assert candidate["activation"] == "HQ_ADOPTION_REQUIRED__ISSUER_OUTPUT_ALONE_IS_NOT_ACTIVE_AUTHORITY"
        candidate_path = td / "candidate.json"
        candidate_path.write_text(json.dumps(candidate, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        proc = subprocess.run([
            sys.executable, str(VERIFIER),
            "--candidate", str(candidate_path),
            "--receipt", str(temp_receipt),
            "--replay-manifest", str(replay_path),
            "--m01-m18", str(temp_m01),
            "--extension-scan", str(temp_scan),
            "--authority-material", str(authority_path),
        ], text=True, capture_output=True, check=False)
        assert proc.returncode == 0, proc.stderr or proc.stdout
        verification = json.loads(proc.stdout.strip().splitlines()[-1])
        assert verification["status"] == "PASS"
        assert verification["candidate_active"] is False
        assert verification["hq_adoption_required"] is True
        zip_receipt = {
            "schema": "EE_P2R6I_ZIP_RECONSTRUCTION_RECEIPT@1.0.0",
            "zip_git_blob_sha1": "d20b8aeee5abe5a1348e5ab17546c82e3592ab6e",
            "zip_byte_length": 17663792,
            "zip_sha256": "9d2c608f21d9d93111c7418bce945f6245340389d7e8c2ccff70b18af358dd70",
            "member_count": 1,
            "member_name": "successor_release_replay_manifest.json",
            "logical_json_byte_length": 118508673,
            "logical_json_sha256": "aa3b6026d4dbc3df8b142725704974eaef810e5dbf5b31d14b19c88cf8ecafd5",
            "replay_manifest_content_hash": candidate["identity_material"]["replay_manifest_ref"]["content_hash"],
            "semantic_projection_hash": candidate["identity_material"]["candidate_projection_identity"],
            "transient_extraction_removed_with_tempdir": True,
        }
        payload = {"authority": authority, "candidate": candidate, "verification": verification, "zip_receipt": zip_receipt}
        encoded = base64.b64encode(canonical(payload).encode("utf-8")).decode("ascii")
        raise AssertionError("EE_P2R6I_GENERATED_PAYLOAD_B64=" + encoded)
