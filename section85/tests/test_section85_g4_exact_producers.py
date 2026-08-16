from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "section85/code"
HELPER = CODE / "section85_exact_producer_state.py"
BOUNDED = CODE / "run_bounded_nine_v550j_v551j_v552j.py"
DIAGNOSTIC = CODE / "run_section85_diagnostic_smoke_matrix.py"
AUTHORITY = ROOT / "section85/authority/section85_typed_stage_contract.json"


def load(path: Path, name: str):
    if str(CODE) not in sys.path:
        sys.path.insert(0, str(CODE))
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ident() -> dict:
    return {
        "producer_run_id": "run-a", "run_id": "run-a", "source": "GSS",
        "wave": "2010", "canonical_wave": "2010", "country_code": "US", "shard_id": "",
        "producer_scope_identity": {
            "run_id": "run-a", "source": "GSS", "wave": "2010",
            "canonical_wave": "2010", "country_code": "US", "shard_id": "", "scope_kind": "country",
        },
    }


def expected() -> dict:
    return {"run_id": "run-a", "source": "GSS", "wave": "2010", "country_code": "US", "shard_id": ""}


def fake_frame(rows: int, *, zero: bool = False) -> pd.DataFrame:
    data = []
    for i in range(rows):
        row = {"run_id": "run-a", "source": "GSS", "canonical_wave": "2010", "country_code": "US", "packet_id": f"p{i}"}
        if zero:
            row.update(observed_zero=True, pressure_score=0.0, pressure_score_status="OBSERVED_ZERO", measurement_evidence_status="PRESENT")
        data.append(row)
    return pd.DataFrame(data)


def install_fake_parquet(monkeypatch, helper, frames: dict[str, pd.DataFrame]) -> None:
    def inspect(path):
        p = Path(path)
        frame = frames.get(str(p.resolve()))
        return SimpleNamespace(path=str(p), exists=p.exists(), readable=p.exists() and frame is not None,
                               row_count=None if frame is None else len(frame),
                               artifact_file_sha256=sha(p) if p.exists() else "", error="")
    monkeypatch.setattr(helper, "inspect_artifact", inspect)
    monkeypatch.setattr(helper.pd, "read_parquet", lambda p: frames[str(Path(p).resolve())].copy())


def artifact(root: Path, frames: dict[str, pd.DataFrame], name: str, rel: str, schema: str, rows: int, *, zero: bool = False) -> dict:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(f"fake:{name}:{rows}".encode())
    frames[str(p.resolve())] = fake_frame(rows, zero=zero)
    return {"artifact": name, "path": rel, "artifact_kind": "canonical", "row_count": rows,
            "artifact_file_sha256": sha(p), "schema_version": schema}


def v551j_manifest(tmp: Path, frames: dict[str, pd.DataFrame], evidence: str, permission: str) -> Path:
    root = tmp / "v551j/run-a"
    arts = []
    if evidence == "PRESENT":
        for name, rel, rows in [
            ("candidate", "packets/v551j_joint_packet_candidate_index.parquet", 1),
            ("component", "packets/v551j_joint_component_index.parquet", 1),
            ("certified", "packets/v551j_certified_joint_packet_index.parquet", 1 if permission == "ALLOW" else 0),
            ("review_surface", "packets/v551j_review_surface.parquet", 1 if permission == "DENY" else 0),
        ]:
            row = artifact(root, frames, name, rel, "v2.2.3", rows)
            row["path"] = "../" + rel
            arts.append(row)
    path = root / "manifest/manifest.json"
    dump(path, {"contract_version": "rawlsing_pipeline_boundary_v1", **ident(), "schema_version": "v2.2.3",
                "compiler_version": "v551j_joint_evidence_contract_v2_2_3", "run_integrity_status": "PASS",
                "evidence_status": evidence, "downstream_permission_status": permission, "artifacts": arts,
                "row_counts": {"candidate": int(evidence == "PRESENT")}})
    return path


def upstream(path: Path, stage: str) -> Path:
    schema, compiler = (("v2.2.3", "v551j_joint_evidence_contract_v2_2_3") if stage == "v551j" else ("v3.0", "v3.0"))
    dump(path, {"contract_version": "rawlsing_pipeline_boundary_v1", **ident(), "schema_version": schema,
                "compiler_version": compiler, "run_integrity_status": "PASS", "evidence_status": "PRESENT",
                "downstream_permission_status": "ALLOW"})
    return path


def v552j_manifest(tmp: Path, frames: dict[str, pd.DataFrame], evidence: str, permission: str, *, zero: bool = False) -> Path:
    uv551j = upstream(tmp / "up/v551j.json", "v551j")
    uv552 = upstream(tmp / "up/v552.json", "v552")
    root = tmp / "v552j/run-a"
    join = artifact(root, frames, "v552j_structural_join_index", "packets/v552j_structural_join_index.parquet", "v1.0", 1 if zero else 0, zero=zero)
    audit = artifact(root, frames, "v552j_join_audit", "audits/v552j_join_audit.parquet", "v1.0", 0)
    path = root / "manifest.json"
    dump(path, {"contract_version": "rawlsing_pipeline_boundary_v1", **ident(), "schema_version": "v1.0",
                "compiler_version": "v552j_structural_join_v1", "run_integrity_status": "PASS",
                "evidence_status": evidence, "downstream_permission_status": permission,
                "observed_zero_count": 1 if zero else 0, "observed_zero_is_measurement_not_absence": True,
                "artifacts": [join, audit], "canonical_artifact_names": ["v552j_structural_join_index", "v552j_join_audit"],
                "upstream_v551j": {"manifest_path": str(uv551j), "manifest_file_sha256": sha(uv551j), "schema_version": "v2.2.3", "compiler_version": "v551j_joint_evidence_contract_v2_2_3"},
                "upstream_v552": {"manifest_path": str(uv552), "manifest_file_sha256": sha(uv552), "schema_version": "v3.0", "compiler_version": "v3.0"},
                "contract_boundary": {"synthetic_unknown_primary_rows_allowed": False, "missing_constraint_metrics_are_zero": False,
                    "structural_matching_requires_exact_scope_before_semantic_score": True,
                    "observed_zero_distinct_from_absence_or_unresolved": True, "canonical_machine_format": "parquet"}})
    return path


def test_v551j_certified_review_empty_and_unresolved_are_distinct(tmp_path, monkeypatch):
    helper = load(HELPER, "exact_state_a")
    for evidence, permission, classification, permitted in [
        ("PRESENT", "ALLOW", "PRESENT_ALLOWED", True),
        ("PRESENT", "DENY", "PRESENT_REVIEW_ONLY", False),
        ("VALID_EMPTY", "NOT_APPLICABLE", "VALID_EMPTY", False),
        ("APPLICABLE_UNRESOLVED", "DENY", "APPLICABLE_UNRESOLVED", False),
    ]:
        frames = {}
        path = v551j_manifest(tmp_path / classification, frames, evidence, permission)
        install_fake_parquet(monkeypatch, helper, frames)
        result = helper.verify_v551j_producer_manifest(path, expected_identity=expected())
        assert result["integrity_pass"] is True
        assert result["state_classification"] == classification
        assert result["operation_permitted"] is permitted


def test_v551j_wrong_version_scope_hash_and_legacy_boolean_fail_closed(tmp_path, monkeypatch):
    helper = load(HELPER, "exact_state_b")
    frames = {}
    path = v551j_manifest(tmp_path, frames, "PRESENT", "ALLOW")
    install_fake_parquet(monkeypatch, helper, frames)
    payload = json.loads(path.read_text())
    payload["schema_version"] = "v2.2.2"; dump(path, payload)
    assert helper.exact_producer_gate(path, stage="v551j", expected_identity=expected())["typed_contract_valid"] is False
    path = v551j_manifest(tmp_path / "scope", frames, "PRESENT", "ALLOW")
    payload = json.loads(path.read_text()); payload["source"] = "EVS"; dump(path, payload)
    assert helper.exact_producer_gate(path, stage="v551j", expected_identity=expected())["typed_contract_valid"] is False
    path = v551j_manifest(tmp_path / "hash", frames, "PRESENT", "ALLOW")
    payload = json.loads(path.read_text()); payload["artifacts"][0]["artifact_file_sha256"] = "0" * 64; dump(path, payload)
    assert "SHA256_MISMATCH" in helper.exact_producer_gate(path, stage="v551j", expected_identity=expected())["failure_reason"]
    legacy = tmp_path / "legacy.json"; dump(legacy, {"ready_for_v552j_joint_evidence": True})
    assert helper.exact_producer_gate(legacy, stage="v551j")["typed_contract_valid"] is False


def test_malformed_typed_pair_is_rejected(tmp_path):
    helper = load(HELPER, "exact_state_c")
    path = tmp_path / "bad.json"
    dump(path, {"contract_version": "rawlsing_pipeline_boundary_v1", **ident(), "schema_version": "v2.2.3",
                "compiler_version": "v551j_joint_evidence_contract_v2_2_3", "run_integrity_status": "PASS",
                "evidence_status": "VALID_EMPTY", "downstream_permission_status": "ALLOW", "artifacts": []})
    assert helper.exact_producer_gate(path, stage="v551j")["typed_contract_valid"] is False


def test_v552j_empty_not_applicable_unresolved_and_observed_zero_stay_distinct(tmp_path, monkeypatch):
    helper = load(HELPER, "exact_state_d")
    for evidence, permission, classification in [
        ("VALID_EMPTY", "NOT_APPLICABLE", "VALID_EMPTY"),
        ("NOT_APPLICABLE", "NOT_APPLICABLE", "NOT_APPLICABLE"),
        ("APPLICABLE_UNRESOLVED", "DENY", "APPLICABLE_UNRESOLVED"),
    ]:
        frames = {}; path = v552j_manifest(tmp_path / classification, frames, evidence, permission)
        install_fake_parquet(monkeypatch, helper, frames)
        result = helper.verify_v552j_producer_manifest(path, expected_identity=expected())
        assert result["integrity_pass"] is True and result["operation_permitted"] is False
        assert result["state_classification"] == classification and result["observed_zero_count"] == 0
    frames = {}; path = v552j_manifest(tmp_path / "zero", frames, "PRESENT", "ALLOW", zero=True)
    install_fake_parquet(monkeypatch, helper, frames)
    result = helper.verify_v552j_producer_manifest(path, expected_identity=expected())
    assert result["operation_permitted"] is True and result["measurement_state"] == "OBSERVED_ZERO_PRESENT"


def test_v552j_nonempty_blocked_upstream_hash_and_artifact_hash_fail_closed(tmp_path, monkeypatch):
    helper = load(HELPER, "exact_state_e")
    blocked = tmp_path / "blocked.json"; dump(blocked, {"status": "BLOCKED_V552J_INPUT_INVALID"})
    assert helper.exact_producer_gate(blocked, stage="v552j")["typed_contract_valid"] is False
    frames = {}; path = v552j_manifest(tmp_path / "uphash", frames, "PRESENT", "ALLOW")
    install_fake_parquet(monkeypatch, helper, frames)
    payload = json.loads(path.read_text()); Path(payload["upstream_v551j"]["manifest_path"]).write_text("tampered", encoding="utf-8")
    assert "SHA256_MISMATCH" in helper.exact_producer_gate(path, stage="v552j", expected_identity=expected())["failure_reason"]
    frames = {}; path = v552j_manifest(tmp_path / "arthash", frames, "PRESENT", "ALLOW")
    install_fake_parquet(monkeypatch, helper, frames)
    payload = json.loads(path.read_text()); payload["artifacts"][0]["artifact_file_sha256"] = "0" * 64; dump(path, payload)
    assert "SHA256_MISMATCH" in helper.exact_producer_gate(path, stage="v552j", expected_identity=expected())["failure_reason"]


def test_bounded_gate_consumes_exact_root_manifest_not_readiness_presence(tmp_path, monkeypatch):
    bounded = load(BOUNDED, "bounded_final")
    vm = tmp_path / "v550j.json"; vr = tmp_path / "v550j_ready.json"; j = tmp_path / "v551j.json"; z = tmp_path / "v552j.json"; r = tmp_path / "readiness.json"
    dump(vm, {"success": True, "validation_status": "pass"}); dump(vr, {"family_registry_status": "applicable", "blocking_issues": []})
    for p in (j, z): dump(p, {"x": 1})
    dump(r, {"status": "BLOCKED_BUT_NONEMPTY"})
    seen = []
    def exact(path, *, stage, expected_identity=None):
        seen.append((stage, str(path)))
        return {"typed_contract_valid": True, "integrity_pass": True, "operation_permitted": stage == "v551j",
                "evidence_status": "PRESENT" if stage == "v551j" else "VALID_EMPTY",
                "downstream_permission_status": "ALLOW" if stage == "v551j" else "NOT_APPLICABLE"}
    monkeypatch.setattr(bounded, "exact_producer_gate", exact)
    entry = {"run_id": "run-a", "source_family": "GSS", "wave": "2010", "country_code": "US", "shard_id": "",
             "expected_outputs": {"v550j_manifest": str(vm), "v550j_readiness": str(vr), "v551j_manifest": str(j), "v552j_manifest": str(z), "v552j_readiness": str(r)}}
    _, v552j, checks = bounded._typed_functional_gate(entry)
    assert all(checks.values()) and v552j["operation_permitted"] is False
    assert ("v552j", str(z)) in seen and all(path != str(r) for _, path in seen)


def test_diagnostic_rejects_legacy_boolean_and_preserves_review_only(tmp_path, monkeypatch):
    diagnostic = load(DIAGNOSTIC, "diag_final")
    legacy_root = tmp_path / "legacy"
    dump(legacy_root / "manifest/manifest.json", {"final_status": "READY_V551J"})
    dump(legacy_root / "manifest/v551j_readiness_report.json", {"ready_for_v552j_joint_evidence": True, "candidate_packet_count": 9})
    gate = diagnostic.current_v551j_gate(legacy_root)
    assert gate["typed_contract_valid"] is False and gate["candidate_packet_count"] == 9
    monkeypatch.setattr(diagnostic, "exact_producer_gate", lambda *a, **k: {
        "typed_contract_valid": True, "integrity_pass": True, "operation_permitted": False,
        "run_integrity_status": "PASS", "evidence_status": "PRESENT", "downstream_permission_status": "DENY",
        "state_classification": "PRESENT_REVIEW_ONLY"})
    gate = diagnostic.current_v551j_gate(legacy_root)
    assert gate["run_integrity_status"] == "PASS" and gate["operation_permitted"] is False
    assert gate["hook_status"] == "ACTIVE_G4_EXACT_PRODUCER_CONTRACT"


def test_authority_names_exact_g4_versions_and_preserves_v551() -> None:
    typed = json.loads(AUTHORITY.read_text(encoding="utf-8"))
    assert typed["stage_contracts"]["v551"]["atom_row_count_is_integrity_gate"] is False
    assert typed["stage_contracts"]["v551j"]["status"] == "ACTIVE_G4_MERGED_PRODUCER"
    assert typed["stage_contracts"]["v551j"]["producer_schema_version"] == "v2.2.3"
    assert typed["stage_contracts"]["v552j"]["status"] == "ACTIVE_G4_MERGED_PRODUCER"
    assert typed["stage_contracts"]["v552j"]["producer_compiler_version"] == "v552j_structural_join_v1"
