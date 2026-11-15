from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy import ddm_v551_atoms as atoms
from data.ddm_build_copy import compile_v551_relation_evidence_atoms as compiler

AUTH = {
    "h1": {
        "response_semantics_contract_hash": "h1",
        "authority_intensity_semantics": "DIRECTIONAL_MAGNITUDE",
        "projection_rule_id": "r1",
        "authority_status": "CERTIFIED",
        "review_status": "NO_REVIEW",
    }
}


def row(**overrides):
    value = dict(
        run_id="run-1",
        source="S",
        source_family="S",
        wave="W",
        canonical_wave="W",
        country_code="C",
        analysis_scope="country",
        source_table="answer_distribution",
        source_row_hash="x",
        question_id="q",
        var_code="v",
        position_field="",
        position_value="",
        response_value_raw="1",
        response_value_normalized="1",
        response_label="x",
        normalized_response_label="x",
        response_family="agreement_scale",
        response_direction="positive",
        response_intensity=0.8,
        directional_applicability_status="APPLICABLE_BY_AUTHORITY",
        bridge_evidence_lane="direct_relation_response",
        is_substantive=True,
        is_missing=False,
        is_special=False,
        response_semantics_contract_hash="h1",
        semantic_role="RELATION_EVIDENCE",
        semantic_role_authority_status="CERTIFIED",
        response_semantics_authority_status="CERTIFIED",
        directionality_authority_status="CERTIFIED",
        structural_mapping_status="COMPLETE",
        response_option_map_matched=True,
        usable_for_evidence=True,
        allowed_as_v551_relation_evidence=True,
        n_unweighted=10,
        n_respondents=20,
        n_weighted=10,
        pct_unweighted=0.5,
        pct_weighted=0.5,
        weight_status="weighted",
        response_topology="scalar",
        empirical_object_type="answer_distribution",
        empirical_object_id="e",
        driver_id="d",
        driver_facet_id="f",
        relation_axis_id="a",
        target_entity_id="t",
        manual_review_flag=False,
        source_structure_review_required=False,
        question_use_contract_hash="rowhash",
    )
    value.update(overrides)
    return value


def _fake_parquet(monkeypatch: pytest.MonkeyPatch) -> None:
    def write_pickle(frame: pd.DataFrame, path: str | Path, index: bool = False) -> None:
        del index
        frame.to_pickle(path)

    monkeypatch.setattr(pd.DataFrame, "to_parquet", write_pickle)
    monkeypatch.setattr(pd, "read_parquet", lambda path: pd.read_pickle(path))


def test_shared_boundary_status_mapping_is_frozen() -> None:
    assert compiler._boundary_statuses(2, 1) == ("PASS", "PRESENT", "ALLOW", "PROMOTABLE_EVIDENCE_PRESENT")
    assert compiler._boundary_statuses(2, 0) == ("PASS", "APPLICABLE_UNRESOLVED", "DENY", "APPLICABLE_REPAIR_DEBT_ONLY")
    assert compiler._boundary_statuses(0, 0) == ("PASS", "NOT_APPLICABLE", "NOT_APPLICABLE", "NO_APPLICABLE_DIRECTIONAL_EVIDENCE")


def test_compiler_requires_exact_singular_source_wave_and_country_or_shard() -> None:
    good = compiler._producer_scope_identity(pd.DataFrame([row()]))
    assert good == {
        "source": "S",
        "wave": "W",
        "canonical_wave": "W",
        "country_code": "C",
        "shard_id": "",
        "scope_kind": "country",
    }
    with pytest.raises(RuntimeError, match="COUNTRY_SCOPE_NOT_SINGULAR"):
        compiler._producer_scope_identity(
            pd.DataFrame([row(source_row_hash="a", country_code="C"), row(source_row_hash="b", country_code="D")])
        )
    shard_scope = compiler._producer_scope_identity(
        pd.DataFrame(
            [
                row(source_row_hash="a", country_code="C", shard_id="shard-1"),
                row(source_row_hash="b", country_code="D", shard_id="shard-1"),
            ]
        )
    )
    assert shard_scope["scope_kind"] == "shard"
    assert shard_scope["country_code"] == ""
    assert shard_scope["shard_id"] == "shard-1"


def test_fresh_v551_output_round_trips_shared_boundary_verifier(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    boundary = pytest.importorskip("data.ddm_build_copy.ddm_pipeline_boundary_contract")
    _fake_parquet(monkeypatch)
    monkeypatch.setattr(atoms, "_load_registry", lambda: AUTH)
    bridge_path = tmp_path / "bridge.csv"
    bridge_path.write_text("producer bridge placeholder\n", encoding="utf-8")
    compiler.compile_v551_run(
        pd.DataFrame([row()]),
        run_id="run-1",
        bridge_path=bridge_path,
        output_root=tmp_path / "out",
    )
    run_dir = tmp_path / "out" / "run-1"
    required = [f"{name}.parquet" for name in compiler.CANONICAL_ARTIFACTS]
    verified = boundary.verify_boundary_manifest(
        run_dir / "manifest.json",
        run_id="run-1",
        source="S",
        wave="W",
        country_code="C",
        required_artifacts=required,
    )
    assert verified.state.run_integrity_status == "PASS"
    assert verified.state.evidence_status == "PRESENT"
    assert verified.state.downstream_permission_status == "ALLOW"
    payload = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert payload["contract_version"] == boundary.PIPELINE_BOUNDARY_CONTRACT_VERSION
    assert payload["producer_scope_identity"]["scope_kind"] == "country"
    assert {item["path"] for item in payload["artifacts"]} == set(required)
    assert all(len(item["artifact_file_sha256"]) == 64 for item in payload["artifacts"])
    assert all(len(item["logical_content_sha256"]) == 64 for item in payload["artifacts"])


def test_reused_run_publication_removes_stale_prior_outputs(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    pytest.importorskip("data.ddm_build_copy.ddm_pipeline_boundary_contract")
    _fake_parquet(monkeypatch)
    monkeypatch.setattr(atoms, "_load_registry", lambda: AUTH)
    bridge_path = tmp_path / "bridge.csv"
    bridge_path.write_text("producer bridge placeholder\n", encoding="utf-8")
    bridge = pd.DataFrame([row()])
    output_root = tmp_path / "out"
    compiler.compile_v551_run(
        bridge,
        run_id="run-1",
        bridge_path=bridge_path,
        output_root=output_root,
        write_csv=True,
    )
    run_dir = output_root / "run-1"
    assert (run_dir / "relation_evidence_atoms.csv").exists()
    (run_dir / "retired_v551_output.parquet").write_bytes(b"stale")
    compiler.compile_v551_run(
        bridge,
        run_id="run-1",
        bridge_path=bridge_path,
        output_root=output_root,
        write_csv=False,
    )
    assert not (run_dir / "relation_evidence_atoms.csv").exists()
    assert not (run_dir / "retired_v551_output.parquet").exists()
    payload = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    assert all(item["path"].endswith(".parquet") for item in payload["artifacts"])
