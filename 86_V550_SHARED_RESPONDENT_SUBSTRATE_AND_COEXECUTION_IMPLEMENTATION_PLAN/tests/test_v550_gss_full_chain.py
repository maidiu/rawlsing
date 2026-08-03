from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_CODE = REPO_ROOT / "35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE/runtime_reproducibility_code"
if str(RUNTIME_CODE) not in sys.path:
    sys.path.insert(0, str(RUNTIME_CODE))

from data.ddm_build_copy.ddm_v550_shared_respondent_substrate import (  # noqa: E402
    canonicalize_shared_respondent_substrate,
    logical_shared_substrate_hash,
    shared_substrate_paths,
    write_shared_respondent_substrate_atomic,
)


ATOM_CSV = REPO_ROOT / "35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE/runtime_reproducibility_inputs/v551_atoms/crosssurvey/GSS_2010_US/relation_evidence_atoms.csv"
GSS_REGISTRY = REPO_ROOT / "85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY/authority/registry_gss.yaml"
GSS_VARS = ["abany", "abdefect", "abhlth", "abnomore", "abrape", "absingle"]


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _frame_hash(frame: pd.DataFrame) -> str:
    out = frame.copy()
    for column in out.columns:
        out[column] = out[column].fillna("").astype(str)
    out = out.sort_values(list(out.columns), kind="mergesort").reset_index(drop=True)
    return hashlib.sha256(out.to_csv(index=False).encode("utf-8")).hexdigest()


def _semantic_hash(frame: pd.DataFrame, *, drop_columns: set[str]) -> str:
    comparable = frame.drop(columns=[column for column in drop_columns if column in frame.columns])
    return _frame_hash(comparable)


def _run(cmd: list[str], *, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    return result


def _build_gss_chain(root: Path) -> dict[str, object]:
    root.mkdir(parents=True, exist_ok=True)
    atoms = pd.read_csv(ATOM_CSV, dtype=str, keep_default_na=False)
    fixture_atoms = atoms[atoms["var_code"].str.lower().isin(GSS_VARS)].copy()
    atom_parquet = root / "relation_evidence_atoms.parquet"
    fixture_atoms.to_parquet(atom_parquet, index=False)
    reloaded_atoms = pd.read_parquet(atom_parquet).fillna("").astype(str)
    original_norm = fixture_atoms.fillna("").astype(str)
    assert len(fixture_atoms) == 12
    assert list(reloaded_atoms.columns) == list(original_norm.columns)
    assert reloaded_atoms.to_dict("records") == original_norm.to_dict("records")
    for column in ["atom_id", "atom_contract_hash", "empirical_object_id", "question_id", "var_code", "response_value_normalized"]:
        assert reloaded_atoms[column].tolist() == original_norm[column].tolist()

    run_id = "gss2010_synth"
    shard_id = "GSS_2010_US"
    shard = root / "v550/shard_runs" / run_id / shard_id
    (shard / "core").mkdir(parents=True)
    pd.DataFrame([{"source": "GSS", "source_family": "GSS", "wave": "2010", "canonical_wave": "2010", "country_code": "US"}]).to_parquet(
        shard / "shard_scope.parquet", index=False
    )
    fixture_atoms[["source", "source_family", "wave", "canonical_wave", "country_code", "var_code", "question_id", "question_text"]].drop_duplicates("var_code").to_parquet(
        shard / "core/question_use_contract.parquet", index=False
    )

    respondent_rows = []
    for respondent_id, offset in [("r1", 0), ("r2", 1), ("r3", 0)]:
        for idx, var_code in enumerate(GSS_VARS):
            candidates = fixture_atoms[fixture_atoms["var_code"].str.lower().eq(var_code)]
            row = candidates.iloc[(idx + offset) % len(candidates)].to_dict()
            row["respondent_id"] = respondent_id
            row["is_substantive"] = True
            row["is_valid_substantive_response"] = True
            respondent_rows.append(row)
    respondent_frame = pd.DataFrame(respondent_rows)
    assert respondent_frame["respondent_id"].nunique() == 3

    substrate = canonicalize_shared_respondent_substrate(
        respondent_frame,
        run_id=run_id,
        shard_id=shard_id,
        source="GSS",
        source_id="GSS",
        wave="2010",
        canonical_wave="2010",
        country_code="US",
        base_var_codes=GSS_VARS[:2],
        joint_required_var_codes=GSS_VARS,
        joint_configuration_ids_by_var={var_code: ["JCFG-GSS-ABORTION-CONDITIONS"] for var_code in GSS_VARS},
    )
    substrate_paths = shared_substrate_paths(shard / "checkpoints/respondent_substrate", source="GSS", canonical_wave="2010", country_code="US")
    substrate_manifest = write_shared_respondent_substrate_atomic(
        substrate,
        substrate_paths,
        manifest_fields={
            "run_id": run_id,
            "shard_id": shard_id,
            "source": "GSS",
            "source_id": "GSS",
            "wave": "2010",
            "canonical_wave": "2010",
            "country_code": "US",
            "response_semantics_contract_hash": "preserved_gss_fixture",
            "question_family_registry_hash": "preserved_gss_registry",
            "joint_configuration_authority_release_id": "V550J-BOUNDED-AUTHORITY-2026-08-02-R1",
            "p3_authority_release_id": "P3-AUTHORITY-2026-08-02-R184",
            "respondent_relation_schema_hash": "synthetic_relation_schema",
            "synthetic_respondent_query_count": 1,
        },
        base_var_codes=GSS_VARS[:2],
        joint_required_var_codes=GSS_VARS,
    )

    response_map = fixture_atoms[["source", "wave", "var_code", "response_value_normalized", "normalized_response_label", "semantic_role"]].drop_duplicates()
    response_map = response_map.rename(
        columns={
            "response_value_normalized": "value_code_normalized",
            "normalized_response_label": "value_label_clean",
            "semantic_role": "semantic_response_role",
        }
    )
    response_map["var_name"] = response_map["var_code"]
    response_map_path = root / "response_option_map.parquet"
    response_map.to_parquet(response_map_path, index=False)

    env = os.environ.copy()
    env.pop("DATABASE_URL", None)
    env["PYTHONPATH"] = str(RUNTIME_CODE)
    _run(
        [
            sys.executable,
            str(RUNTIME_CODE / "data/ddm_build_copy/compile_v550j_joint_response_patterns.py"),
            "--v550-shard-dir",
            str(shard),
            "--output-root",
            str(root / "v550j"),
            "--registry-path",
            str(GSS_REGISTRY),
            "--response-option-map",
            str(response_map_path),
            "--association-mode",
            "off",
            "--no-progress",
            "--no-write-csv",
            "--v550j-substrate-mode",
            "prepared_required",
            "--prepared-substrate-path",
            str(substrate_paths.parquet_path),
            "--prepared-substrate-manifest-path",
            str(substrate_paths.manifest_path),
            "--forbid-database-access",
        ],
        env=env,
    )
    v550j_root = root / "v550j/runs" / run_id / shard_id / "joint_patterns"
    pattern_index = pd.read_parquet(v550j_root / "joint_response_pattern_index.parquet")
    assert len(pattern_index) == 2
    assert set(pattern_index["family_id"]) == {"JCFG-GSS-ABORTION-CONDITIONS"}

    _run(
        [
            sys.executable,
            str(REPO_ROOT / "02_CORE_REFERENCE/code/compile_v551j_joint_evidence_packets.py"),
            "--run-id",
            shard_id,
            "--v551-atoms-path",
            str(atom_parquet),
            "--v550j-pattern-index-path",
            str(v550j_root / "joint_response_pattern_index.parquet"),
            "--v550j-pattern-item-index-path",
            str(v550j_root / "joint_response_pattern_item_index.parquet"),
            "--v550j-relation-signature-path",
            str(v550j_root / "joint_pattern_relation_signature.parquet"),
            "--v550j-manifest-path",
            str(v550j_root / "v550j_manifest.json"),
            "--v550j-readiness-report-path",
            str(v550j_root / "v550j_source_wave_readiness_report.json"),
            "--registry-path",
            str(GSS_REGISTRY),
            "--v550j-meaning-summary-path",
            str(v550j_root / "joint_pattern_meaning_summary.parquet"),
            "--output-root",
            str(root / "v551j"),
            "--emit-review-surface",
            "--emit-certified-index",
            "--no-write-csv",
        ],
        env=env,
    )
    v551j_root = root / "v551j" / shard_id
    readiness = json.loads((v551j_root / "manifest/v551j_readiness_report.json").read_text(encoding="utf-8"))
    components = pd.read_parquet(v551j_root / "packets/v551j_joint_component_index.parquet")
    candidates = pd.read_parquet(v551j_root / "packets/v551j_joint_packet_candidate_index.parquet")
    preserved_atom_ids = set(fixture_atoms["atom_id"])
    assert readiness["candidate_packet_count"] >= 1
    assert readiness["component_row_count"] == 12
    assert int(candidates["unmatched_unexplained_component_count"].astype(int).sum()) == 0
    assert int(candidates["ambiguous_component_count"].astype(int).sum()) == 0
    assert int(candidates["cross_contract_conflict_count"].astype(int).sum()) == 0
    assert set(components["v551_atom_id"]).issubset(preserved_atom_ids)
    assert candidates["component_order_integrity_status"].eq("PASS").all()

    _run(
        [
            sys.executable,
            str(RUNTIME_CODE / "data/ddm_build_copy/compile_v552_structural_ddm.py"),
            "--run-id",
            shard_id,
            "--atoms-path",
            str(atom_parquet),
            "--output-root",
            str(root / "v552"),
            "--strict-handoff",
            "--no-progress",
            "--no-write-csv",
        ],
        env=env,
    )
    v552_root = root / "v552" / shard_id
    v552_manifest = json.loads((v552_root / "manifest/manifest.json").read_text(encoding="utf-8"))
    assert v552_manifest["status"] == "READY_V552_STRUCTURAL_PRESSURE_CONTRACT"

    _run(
        [
            sys.executable,
            str(RUNTIME_CODE / "data/ddm_build_copy/compile_v552j_runtime_safe_structural_handoff.py"),
            "--run-id",
            shard_id,
            "--v551j-run-root",
            str(v551j_root),
            "--output-root",
            str(root / "v552j"),
            "--v552-question-semantic-hierarchy-path",
            str(v552_root / "structural/question_semantic_hierarchy.parquet"),
            "--v552-structural-channel-index-path",
            str(v552_root / "structural/structural_channel_index.parquet"),
            "--v552-relation-axis-pressure-path",
            str(v552_root / "structural/relation_axis_pressure.parquet"),
            "--v552-target-entity-pressure-path",
            str(v552_root / "structural/target_entity_pressure.parquet"),
            "--v552-driver-facet-pressure-path",
            str(v552_root / "structural/driver_facet_pressure.parquet"),
            "--v552-contradiction-surface-path",
            str(v552_root / "structural/contradiction_surface.parquet"),
            "--v552-horizon-constraint-index-path",
            str(v552_root / "structural/horizon_constraint_index.parquet"),
            "--v552-parent-prior-manifest-path",
            str(v552_root / "manifest/parent_prior_manifest.parquet"),
            "--no-write-csv",
        ],
        env=env,
    )
    return {
        "atom_csv_sha256": _file_sha(ATOM_CSV),
        "atom_parquet_hash": _frame_hash(reloaded_atoms),
        "substrate_hash": logical_shared_substrate_hash(substrate),
        "substrate_manifest_hash": substrate_manifest["content_hash"],
        "v550j_pattern_hash": _semantic_hash(pattern_index, drop_columns={"created_at"}),
        "v551j_candidate_hash": _semantic_hash(
            candidates,
            drop_columns={
                "created_at",
                "packet_contract_hash",
                "v550j_pattern_index_artifact_hash",
                "v550j_pattern_item_index_artifact_hash",
                "v550j_relation_signature_artifact_hash",
                "v550j_manifest_hash",
            },
        ),
        "v552_status": v552_manifest["status"],
    }


def test_preserved_gss_fixture_full_synthetic_v550_to_v552j_chain(tmp_path: Path) -> None:
    first = _build_gss_chain(tmp_path / "run_a")
    second = _build_gss_chain(tmp_path / "run_b")
    assert first["atom_csv_sha256"] == "bc0ca9e221c08d97a3045b069c9a4c08c02cf9fa990ebb3362565123279ae15d"
    assert first["substrate_hash"] == first["substrate_manifest_hash"]
    assert first["v552_status"] == "READY_V552_STRUCTURAL_PRESSURE_CONTRACT"
    for key in ["atom_parquet_hash", "v550j_pattern_hash", "v551j_candidate_hash", "v552_status"]:
        assert first[key] == second[key]
