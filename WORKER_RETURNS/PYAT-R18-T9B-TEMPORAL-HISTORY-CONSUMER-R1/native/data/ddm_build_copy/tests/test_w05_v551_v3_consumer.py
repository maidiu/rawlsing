from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy.ddm_pipeline_boundary_consumer import (
    V551_V3_CANONICAL_ARTIFACTS,
    verify_v551_v3_producer_manifest,
)
from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError,
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
)
import data.ddm_build_copy.resolve_pipeline_lineage as resolver
import data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke as smoke


def _fake_parquet(monkeypatch: pytest.MonkeyPatch, frames: dict[str, pd.DataFrame]) -> None:
    def read(path: str | Path) -> pd.DataFrame:
        name = Path(path).name
        if name not in frames:
            raise ValueError(f"unexpected parquet {name}")
        return frames[name].copy()

    monkeypatch.setattr(pd, "read_parquet", read)


def _write_v551_fixture(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    evidence_status: str,
    permission: str,
    candidate_count: int,
    atom_count: int,
    nonpromotable_count: int,
) -> Path:
    run_root = tmp_path / "run-1"
    run_root.mkdir()
    coverage_rows = 0 if candidate_count == 0 else 1
    frames = {
        "directional_candidate_adjudication.parquet": pd.DataFrame({"x": range(candidate_count)}),
        "relation_evidence_atoms.parquet": pd.DataFrame({"x": range(atom_count)}),
        "directional_distribution_coverage.parquet": pd.DataFrame({"x": range(coverage_rows)}),
    }
    _fake_parquet(monkeypatch, frames)
    artifacts = []
    for name in V551_V3_CANONICAL_ARTIFACTS:
        path = run_root / name
        payload = (name + "\n").encode("utf-8")
        path.write_bytes(payload)
        artifacts.append(
            {
                "artifact": Path(name).stem,
                "path": name,
                "artifact_kind": "canonical",
                "row_count": len(frames[name]),
                "artifact_file_sha256": hashlib.sha256(payload).hexdigest(),
                "logical_content_sha256": "1" * 64,
                "schema_version": "v3.0",
            }
        )
    manifest = {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "boundary_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "producer_run_id": "run-1",
        "run_id": "run-1",
        "source": "GSS",
        "wave": "2010",
        "canonical_wave": "2010",
        "country_code": "US",
        "shard_id": "GSS_2010_US",
        "schema_version": "v3.0",
        "compiler_version": "v3.0",
        "run_integrity_status": "PASS",
        "evidence_status": evidence_status,
        "downstream_permission_status": permission,
        "v551_evidence_detail": "fixture",
        "candidate_count": candidate_count,
        "promotable_candidate_count": atom_count,
        "nonpromotable_candidate_count": nonpromotable_count,
        "atom_count": atom_count,
        "distribution_coverage_rows": coverage_rows,
        "artifacts": artifacts,
        "canonical_artifact_names": [Path(name).stem for name in V551_V3_CANONICAL_ARTIFACTS],
    }
    (run_root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return run_root


@pytest.mark.parametrize(
    "evidence,permission,candidates,atoms,nonpromotable",
    [
        ("PRESENT", "ALLOW", 2, 1, 1),
        ("APPLICABLE_UNRESOLVED", "DENY", 2, 0, 2),
        ("NOT_APPLICABLE", "NOT_APPLICABLE", 0, 0, 0),
    ],
)
def test_v551_v3_typed_states_round_trip_without_nonempty_integrity_gate(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    evidence: str,
    permission: str,
    candidates: int,
    atoms: int,
    nonpromotable: int,
) -> None:
    root = _write_v551_fixture(
        tmp_path,
        monkeypatch,
        evidence_status=evidence,
        permission=permission,
        candidate_count=candidates,
        atom_count=atoms,
        nonpromotable_count=nonpromotable,
    )
    verified = verify_v551_v3_producer_manifest(
        root / "manifest.json",
        run_id="run-1",
        source="GSS",
        wave="2010",
        country_code="US",
        shard_id="GSS_2010_US",
    )
    assert verified.integrity_passed is True
    assert verified.state.evidence_status == evidence
    assert verified.state.downstream_permission_status == permission
    atom_artifact = next(item for item in verified.verified_artifacts if Path(item.path).name == "relation_evidence_atoms.parquet")
    assert atom_artifact.row_count == atoms
    assert atom_artifact.valid_empty is (atoms == 0)


def test_v551_v3_rejects_tampered_serialized_artifact(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _write_v551_fixture(
        tmp_path,
        monkeypatch,
        evidence_status="PRESENT",
        permission="ALLOW",
        candidate_count=1,
        atom_count=1,
        nonpromotable_count=0,
    )
    (root / "relation_evidence_atoms.parquet").write_bytes(b"tampered")
    with pytest.raises(BoundaryContractError, match="ARTIFACT_FILE_SHA256_MISMATCH"):
        verify_v551_v3_producer_manifest(
            root / "manifest.json",
            run_id="run-1",
            source="GSS",
            wave="2010",
            country_code="US",
            shard_id="GSS_2010_US",
        )


def test_v551_v3_rejects_wrong_scope_or_version(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _write_v551_fixture(
        tmp_path,
        monkeypatch,
        evidence_status="NOT_APPLICABLE",
        permission="NOT_APPLICABLE",
        candidate_count=0,
        atom_count=0,
        nonpromotable_count=0,
    )
    with pytest.raises(BoundaryContractError, match="IDENTITY_MISMATCH"):
        verify_v551_v3_producer_manifest(
            root / "manifest.json",
            run_id="run-2",
            source="GSS",
            wave="2010",
            country_code="US",
            shard_id="GSS_2010_US",
        )
    payload = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    payload["schema_version"] = "v2"
    (root / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(BoundaryContractError, match="PRODUCER_SCHEMA_VERSION_MISMATCH"):
        verify_v551_v3_producer_manifest(
            root / "manifest.json",
            run_id="run-1",
            source="GSS",
            wave="2010",
            country_code="US",
            shard_id="GSS_2010_US",
        )


def test_smoke_zero_atom_not_applicable_passes_v551_integrity_gate(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = _write_v551_fixture(
        tmp_path,
        monkeypatch,
        evidence_status="NOT_APPLICABLE",
        permission="NOT_APPLICABLE",
        candidate_count=0,
        atom_count=0,
        nonpromotable_count=0,
    )
    gate = smoke.summarize_v551_functional_gate(
        root / "manifest.json",
        run_id="run-1",
        source="GSS",
        wave="2010",
        country_code="US",
        shard_id="GSS_2010_US",
    )
    assert gate["passed"] is True
    assert gate["integrity_passed"] is True
    assert gate["terminal_not_applicable"] is True
    assert gate["atom_rows"] == 0
    assert gate["failure_reason"] == ""


def test_smoke_v551_invocation_uses_v3_cli_and_inherited_bridge_run_id(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    bridge = tmp_path / "bridge.parquet"
    bridge.write_bytes(b"bridge")
    monkeypatch.setattr(pd, "read_parquet", lambda _path: pd.DataFrame([{"run_id": "run-1"}]))
    captured: dict[str, object] = {}

    def fake_run(cmd, timeout_sec=None, config=None):
        captured["cmd"] = list(cmd)
        return {"exit_code": 0, "stdout_tail": "", "stderr_tail": "", "elapsed": 0.0, "command": ""}

    monkeypatch.setattr(smoke._impl, "_invoke_run", fake_run)
    result = smoke.run_v551(
        "legacy-shard-label",
        str(bridge),
        "unused-quc.parquet",
        "unused-response.parquet",
        str(tmp_path / "out"),
        smoke.DEFAULT_CONFIG,
    )
    cmd = captured["cmd"]
    assert isinstance(cmd, list)
    assert cmd[cmd.index("--run-id") + 1] == "run-1"
    assert cmd[cmd.index("--v551-compile-mode") + 1] == "canonical"
    for obsolete in (
        "--question-use-contract-path",
        "--response-option-map-path",
        "--v551-audit-mode",
        "--no-progress",
        "--no-write-csv",
    ):
        assert obsolete not in cmd
    assert result["producer_run_id"] == "run-1"


def test_resolver_v550j_association_index_is_not_nonempty_requirement(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    v550_root = tmp_path / "data/ddm_repository_copy/v550/shard_runs/run-1/GSS_2010_US"
    v550_root.mkdir(parents=True)
    stages = {
        name: resolver.StageResolution(name, "", False, "BLOCKED")
        for name in ("v550", "v550j", "v551", "v551j", "v552", "v552j")
    }
    stages["v550"] = resolver.StageResolution("v550", str(v550_root), True, "READY_V550")
    captured: dict[str, object] = {}

    monkeypatch.setattr(resolver, "_ORIGINAL_RESOLVE_STAGE_ROOTS", lambda *_args, **_kwargs: dict(stages))

    def fake_validate(root: Path, *, stage: str, **kwargs):
        if stage == "v550j":
            captured["required_files"] = tuple(kwargs.get("required_files") or ())
            captured["required_nonempty_files"] = tuple(kwargs.get("required_nonempty_files") or ())
        return resolver.StageResolution(stage, str(root), True, "READY")

    monkeypatch.setattr(resolver, "_validate_root", fake_validate)
    monkeypatch.setattr(
        resolver,
        "_resolve_v551_v3",
        lambda _repo, _v550: resolver.StageResolution("v551", "v551", True, "PASS/PRESENT/ALLOW"),
    )
    resolver.resolve_stage_roots(tmp_path, "GSS", "2010")
    required_files = captured["required_files"]
    required_nonempty = captured["required_nonempty_files"]
    assert any(str(item).endswith("joint_pattern_association_index.parquet") for item in required_files)
    assert not any(str(item).endswith("joint_pattern_association_index.parquet") for item in required_nonempty)
