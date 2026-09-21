from __future__ import annotations

import ast
import compileall
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIVE_MATERIALIZER = ROOT / "rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py"
SEALED_MATERIALIZER = ROOT / "WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py"
BACKEND = ROOT / "rawlsing_next/ee_p2x_darwin_stage_backend.py"
C_BINDER = ROOT / "rawlsing_next/pre553_candidate_c_production_binding.py"
ORACLE = ROOT / "rawlsing_next/pre553_independent_parity_oracle.py"
FACADE = ROOT / "rawlsing_next/pre553_source_backed_c11_facade.py"
PACKAGING = ROOT / "rawlsing_next/runtime/ee_p2x/RUNTIME_PACKAGING_BINDING.json"
T2 = ROOT / "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json"
T5 = ROOT / "WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json"

LOCK2 = "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
PROJECTION = "f400c804fea9b526f25eac823138ecb30e10efaad3207c4578661f684adee665"
PROJECTION_AUTHORITY = "5e793e2fe255d0a0ef6dd405f4bd4c7df125c2d6fb23bd464a0f77d65cb1fcdf"
PROJECTION_SNAPSHOT = "540914a3ddf3b0349720fd81de49b1a88f194929adf1ea5506718af94e65c0d2"
REPRESENTATION_AUTHORITY = "63543411892d8d30fb5670a39714a3dc115145e3f054a7017a325dab1c6cf053"
REPRESENTATION_SNAPSHOT = "e23ec7451d150597799bbd9049cdab45339e647694a9ccfacb2e53aaf09b609b"
RESPONSE_BINDING = "f225e6289b553ab221902c95c1b416bbd01fb722efcc77c909e239d4ee02e87b"
LIVE_MATERIALIZER_BLOB = "ec685803a7416032037ee415e8faf7bf60db8f1b"
C_BINDER_BLOB = "47893688ed455ced2c2f2311ad0aead6fb5bf2d2"
ORACLE_BLOB = "2b2b5fb869e8a1a47814dc8aaa7ff2e2ae20e757"
FACADE_BLOB = "8a761119e4a8d68eb291fc4edfadb52e027f8284"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def assigned_constants(path: Path) -> dict[str, object]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    out: dict[str, object] = {}
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


def load_materializer():
    spec = importlib.util.spec_from_file_location("_fiabc_post_r1j_live_materializer", LIVE_MATERIALIZER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_source_independent_compileall_and_json_contracts():
    assert compileall.compile_dir(str(ROOT / "rawlsing_next"), quiet=1)
    for path in (PACKAGING, T2, T5):
        assert isinstance(json.loads(path.read_text(encoding="utf-8")), dict)


def test_live_materializer_is_exact_sealed_r1j_materializer():
    assert LIVE_MATERIALIZER.read_bytes() == SEALED_MATERIALIZER.read_bytes()
    assert git_blob_sha(LIVE_MATERIALIZER) == LIVE_MATERIALIZER_BLOB
    m = load_materializer()
    assert m.LOCK2 == LOCK2
    assert m.PROJECTION_IDENTITY_REF.content_hash == PROJECTION
    assert m.PROJECTION_AUTH_REF.authority_content_hash == PROJECTION_AUTHORITY
    assert m.REPRESENTATION_AUTHORITY_REF.authority_content_hash == REPRESENTATION_AUTHORITY
    assert m.RESPONSE_BINDING_REF.content_hash == RESPONSE_BINDING
    mapping, representation, coordinate, projection = m.r6s_authorities()
    assert representation.ref.content_hash == REPRESENTATION_SNAPSHOT
    assert projection.ref.content_hash == PROJECTION_SNAPSHOT
    assert mapping.authority_ref == m.MAPPING_AUTHORITY_REF
    assert coordinate.authority_ref == m.COORDINATE_AUTH_REF


def test_live_backend_and_candidate_c_bind_exact_r1j_projection():
    backend = assigned_constants(BACKEND)
    binder = assigned_constants(C_BINDER)
    assert backend["R6S_WVS_PROJECTION"] == PROJECTION
    assert backend["WVS_MATERIALIZER_BLOB"] == LIVE_MATERIALIZER_BLOB
    assert backend["WVS_LOCK2"] == LOCK2
    assert binder["WVS7_CURRENT_PROJECTION_CACHE_IDENTITY"] == PROJECTION
    assert git_blob_sha(C_BINDER) == C_BINDER_BLOB


def test_runtime_packaging_records_only_r1j_delta_and_conserves_lock2():
    d = json.loads(PACKAGING.read_text(encoding="utf-8"))
    assets = {row["role"]: row for row in d["stable_runtime_assets"]}
    assert assets["WVS7_R6S_PROJECTION_MATERIALIZER"]["git_blob_sha"] == LIVE_MATERIALIZER_BLOB
    ids = d["preserved_runtime_identities"]
    assert ids["wvs_lock2"] == LOCK2
    assert ids["wvs_projection"] == PROJECTION
    assert ids["wvs_representation_authority"] == REPRESENTATION_AUTHORITY
    assert ids["wvs_representation_snapshot"] == REPRESENTATION_SNAPSHOT
    assert ids["wvs_response_binding"] == RESPONSE_BINDING
    assert ids["wvs_projection_authority"] == PROJECTION_AUTHORITY
    assert ids["wvs_projection_snapshot"] == PROJECTION_SNAPSHOT
    package = json.loads((ROOT / "rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json").read_text(encoding="utf-8"))
    assert package["lock2"] == LOCK2
    assert package["counts"] == {
        "authorities": 6,
        "predicates": 11,
        "queries": 3,
        "discovery_authorities": 1,
        "candidates": 46,
    }


def test_t2_and_t5_current_bindings_follow_successor_blobs():
    t2 = json.loads(T2.read_text(encoding="utf-8"))
    assert t2["candidate_c_binding"]["WVS7"]["projection_cache_identity"] == PROJECTION
    assert len(t2["current_capabilities"]) == 6
    assert [(x["source"], x["candidate"]) for x in t2["current_capabilities"]] == [
        ("LITS_I", "A"), ("LITS_I", "B"), ("LITS_I", "C"),
        ("WVS7", "A"), ("WVS7", "B"), ("WVS7", "C"),
    ]
    t5 = json.loads(T5.read_text(encoding="utf-8"))
    anchors = t5["preservation_anchors"]
    assert anchors["t1_runtime_packaging"]["wvs_projection_materializer"]["blob"] == LIVE_MATERIALIZER_BLOB
    assert anchors["t2_current_binding"]["candidate_c_module"]["blob"] == C_BINDER_BLOB
    assert anchors["t3_freeze_and_isolation"]["oracle_module"]["blob"] == ORACLE_BLOB
    assert git_blob_sha(ORACLE) == ORACLE_BLOB
    assert git_blob_sha(FACADE) == FACADE_BLOB


def test_no_r1k_oracle_identity_is_fabricated_by_live_rebind():
    packaging = json.loads(PACKAGING.read_text(encoding="utf-8"))
    serialized = json.dumps(packaging, sort_keys=True)
    assert "R1K" not in serialized
    assert "oracle_identity_sha256" not in serialized
    t2 = json.loads(T2.read_text(encoding="utf-8"))
    assert t2["premeasurement_gates"]["measured_p2x_forbidden_here"] is True
