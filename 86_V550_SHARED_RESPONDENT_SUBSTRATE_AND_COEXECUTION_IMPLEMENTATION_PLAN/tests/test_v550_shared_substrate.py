from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_CODE = REPO_ROOT / "35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE/runtime_reproducibility_code"
if str(RUNTIME_CODE) not in sys.path:
    sys.path.insert(0, str(RUNTIME_CODE))

from data.ddm_build_copy.ddm_v550_shared_respondent_substrate import (  # noqa: E402
    canonicalize_shared_respondent_substrate,
    load_shared_respondent_substrate,
    logical_shared_substrate_hash,
    resolve_shared_substrate_requirements,
    shared_substrate_cache_signature_matches,
    shared_substrate_paths,
    validate_shared_respondent_substrate,
    write_shared_respondent_substrate_atomic,
)
from data.ddm_build_copy.ddm_v550_storage import V550ShardPaths  # noqa: E402
from data.ddm_build_copy.run_v550_shards_from_plan import _build_command  # noqa: E402


V550J_COMPILER = (
    RUNTIME_CODE
    / "data/ddm_build_copy/compile_v550j_joint_response_patterns.py"
)
SECTION85_AUTHORITY = REPO_ROOT / "85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY/authority"


def _base_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "respondent_id": 2,
                "var_code": "BASE1",
                "question_id": "q.base1",
                "question_text": "Base one",
                "response_value_normalized": "1",
                "is_substantive": True,
            },
            {
                "respondent_id": 1,
                "var_code": "JOINT1",
                "question_id": "q.joint1",
                "question_text": "Joint one",
                "response_value_normalized": "2",
                "is_substantive": True,
            },
            {
                "respondent_id": 1,
                "var_code": "BASE1",
                "question_id": "q.base1",
                "question_text": "Base one",
                "response_value_normalized": "9",
                "is_missing": True,
                "is_dk": True,
                "is_substantive": False,
            },
        ]
    )


def _canonical(frame: pd.DataFrame | None = None) -> pd.DataFrame:
    return canonicalize_shared_respondent_substrate(
        _base_frame() if frame is None else frame,
        run_id="synthetic_run",
        shard_id="Synthetic_R1_US",
        source="Synthetic",
        source_id="Synthetic",
        wave="R1",
        canonical_wave="R1",
        country_code="US",
        base_var_codes=["BASE1"],
        joint_required_var_codes=["BASE1", "JOINT1"],
        joint_configuration_ids_by_var={"BASE1": ["cfg-1"], "JOINT1": ["cfg-1"]},
    )


def _manifest_fields() -> dict[str, str]:
    return {
        "run_id": "synthetic_run",
        "shard_id": "Synthetic_R1_US",
        "source": "Synthetic",
        "source_id": "Synthetic",
        "wave": "R1",
        "canonical_wave": "R1",
        "country_code": "US",
        "respondent_relation": "synthetic_response_relation",
        "respondent_relation_schema_hash": "schemahash",
        "response_semantics_contract_hash": "responsehash",
        "question_family_registry_hash": "registryhash",
        "joint_configuration_authority_release_id": "V550J-BOUNDED-AUTHORITY-2026-08-02-R1",
        "joint_configuration_adjudication_set_hash": "adjudicationhash",
        "p3_authority_release_id": "P3-AUTHORITY-2026-08-02-R184",
        "authority_compendium_hash": "authorityhash",
    }


def _registry_payload() -> dict[str, object]:
    return {
        "status": "governed",
        "source_family": "Synthetic",
        "p3_authority_release_id": "P3-AUTHORITY-2026-08-02-R184",
        "joint_configuration_authority_release_id": "V550J-BOUNDED-AUTHORITY-2026-08-02-R1",
        "families": [
            {
                "family_id": "JCFG-SYNTH-OVERLAP",
                "joint_configuration_id": "JCFG-SYNTH-OVERLAP",
                "source_family": "Synthetic",
                "eligible_waves": ["R1"],
                "item_role_groups": {
                    "base_overlap": {"items": [{"var_code": "BASE1", "question_implementation_id": "q.base1"}]},
                    "joint_only": {"items": [{"var_code": "JOINT2", "question_implementation_id": "q.joint2"}]},
                },
            }
        ],
    }


def _registry_var_codes(registry: dict[str, object]) -> list[str]:
    codes: set[str] = set()
    for family_cfg in registry.get("families", []):
        if not isinstance(family_cfg, dict):
            continue
        groups = family_cfg.get("item_role_groups") or {}
        if isinstance(groups, dict):
            for group_payload in groups.values():
                if isinstance(group_payload, list):
                    items = group_payload
                elif isinstance(group_payload, dict):
                    items = group_payload.get("items") or [group_payload]
                else:
                    items = []
                for item in items:
                    if isinstance(item, dict) and item.get("var_code"):
                        codes.add(str(item["var_code"]).strip().upper())
        for item in family_cfg.get("items") or []:
            if isinstance(item, dict) and item.get("var_code"):
                codes.add(str(item["var_code"]).strip().upper())
    return sorted(codes)


def _registry_first_wave(registry: dict[str, object]) -> str:
    for family_cfg in registry.get("families", []):
        if isinstance(family_cfg, dict):
            waves = family_cfg.get("eligible_waves") or []
            if waves:
                return str(waves[0])
    return "R1"


def test_logical_hash_is_row_order_independent() -> None:
    frame = _canonical()
    shuffled = frame.iloc[[2, 0, 1]].reset_index(drop=True)
    assert logical_shared_substrate_hash(frame) == logical_shared_substrate_hash(shuffled)


def test_logical_hash_preserves_duplicate_multiplicity() -> None:
    frame = _canonical()
    duplicated = pd.concat([frame, frame.iloc[[0]]], ignore_index=True)
    assert logical_shared_substrate_hash(frame) != logical_shared_substrate_hash(duplicated)


def test_base_joint_union_selection_roles() -> None:
    frame = _canonical()
    roles = dict(zip(frame["var_code"], frame["selection_role"]))
    assert roles["BASE1"] == "BASE_AND_JOINT"
    assert roles["JOINT1"] == "JOINT_ONLY"
    assert frame.loc[frame["var_code"].eq("JOINT1"), "base_fixture_selected"].eq(False).all()


def test_storage_paths_include_respondent_substrate(tmp_path: Path) -> None:
    paths = V550ShardPaths(root=tmp_path, run_id="run", shard_id="shard")
    paths.ensure()
    assert paths.respondent_substrate == paths.checkpoints / "respondent_substrate"
    assert paths.respondent_substrate.exists()


def test_atomic_write_load_and_complete_marker(tmp_path: Path) -> None:
    frame = _canonical()
    paths = shared_substrate_paths(tmp_path, source="Synthetic", canonical_wave="R1", country_code="US")
    manifest = write_shared_respondent_substrate_atomic(
        frame,
        paths,
        manifest_fields=_manifest_fields(),
        base_var_codes=["BASE1"],
        joint_required_var_codes=["BASE1", "JOINT1"],
    )
    assert shared_substrate_cache_signature_matches(
        manifest,
        {
            "schema_version": "v1",
            "execution_contract_version": "v550-v550j-coexecution-v1",
            "source": "Synthetic",
            "canonical_wave": "R1",
            "country_code": "US",
            "union_selection_hash": manifest["union_selection_hash"],
            "response_semantics_contract_hash": "responsehash",
            "question_family_registry_hash": "registryhash",
            "joint_configuration_authority_release_id": "V550J-BOUNDED-AUTHORITY-2026-08-02-R1",
            "p3_authority_release_id": "P3-AUTHORITY-2026-08-02-R184",
            "respondent_relation_schema_hash": "schemahash",
        },
    )
    assert not shared_substrate_cache_signature_matches(
        manifest,
        {
            "source": "Synthetic",
            "canonical_wave": "R1",
            "country_code": "US",
            "union_selection_hash": "stale",
            "response_semantics_contract_hash": "responsehash",
            "question_family_registry_hash": "registryhash",
            "joint_configuration_authority_release_id": "V550J-BOUNDED-AUTHORITY-2026-08-02-R1",
            "p3_authority_release_id": "P3-AUTHORITY-2026-08-02-R184",
            "respondent_relation_schema_hash": "schemahash",
        },
    )
    assert paths.complete_path.exists()
    assert not list(paths.root.glob("*.csv"))
    loaded, loaded_manifest, validation = load_shared_respondent_substrate(paths)
    assert len(loaded) == len(frame)
    assert loaded_manifest["content_hash"] == manifest["content_hash"]
    assert validation["validation_status"] == "pass"
    assert loaded_manifest["base_only_var_codes"] == []
    assert loaded_manifest["joint_only_var_codes"] == ["JOINT1"]
    assert loaded_manifest["overlap_var_codes"] == ["BASE1"]


def test_loader_rejects_missing_complete(tmp_path: Path) -> None:
    frame = _canonical()
    paths = shared_substrate_paths(tmp_path, source="Synthetic", canonical_wave="R1", country_code="US")
    write_shared_respondent_substrate_atomic(
        frame,
        paths,
        manifest_fields=_manifest_fields(),
        base_var_codes=["BASE1"],
        joint_required_var_codes=["BASE1", "JOINT1"],
    )
    paths.complete_path.unlink()
    with pytest.raises(RuntimeError, match="COMPLETE marker missing"):
        load_shared_respondent_substrate(paths)


def test_loader_rejects_parquet_sha_mismatch(tmp_path: Path) -> None:
    frame = _canonical()
    paths = shared_substrate_paths(tmp_path, source="Synthetic", canonical_wave="R1", country_code="US")
    write_shared_respondent_substrate_atomic(
        frame,
        paths,
        manifest_fields=_manifest_fields(),
        base_var_codes=["BASE1"],
        joint_required_var_codes=["BASE1", "JOINT1"],
    )
    manifest = json.loads(paths.manifest_path.read_text())
    manifest["parquet_file_sha256"] = "0" * 64
    paths.manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(RuntimeError, match="parquet SHA mismatch"):
        load_shared_respondent_substrate(paths)


def test_validation_rejects_duplicate_scalar_response_keys() -> None:
    raw = pd.DataFrame(
        [
            {"respondent_id": 1, "var_code": "BASE1", "response_value_normalized": "1", "is_substantive": True},
            {"respondent_id": 1, "var_code": "BASE1", "response_value_normalized": "2", "is_substantive": True},
        ]
    )
    frame = _canonical(raw)
    validation = validate_shared_respondent_substrate(frame, _manifest_fields())
    assert validation["validation_status"] == "fail"
    assert "unauthorized_duplicate_scalar_response_keys" in validation["validation_message"]


def test_cache_signature_requires_governing_hashes(tmp_path: Path) -> None:
    frame = _canonical()
    paths = shared_substrate_paths(tmp_path, source="Synthetic", canonical_wave="R1", country_code="US")
    manifest = write_shared_respondent_substrate_atomic(
        frame,
        paths,
        manifest_fields=_manifest_fields(),
        base_var_codes=["BASE1"],
        joint_required_var_codes=["BASE1", "JOINT1"],
    )


def test_resolver_records_base_joint_union_overlap_and_joint_only() -> None:
    base_questions = pd.DataFrame(
        [
            {"source": "Synthetic", "wave": "R1", "canonical_wave": "R1", "country_code": "US", "var_code": "BASE1", "question_id": "q.base1"},
            {"source": "Synthetic", "wave": "R1", "canonical_wave": "R1", "country_code": "US", "var_code": "BASE2", "question_id": "q.base2"},
        ]
    )
    resolved = resolve_shared_substrate_requirements(
        base_questions,
        _registry_payload(),
        source="Synthetic",
        canonical_wave="R1",
    )
    assert resolved["base_var_codes"] == ["BASE1", "BASE2"]
    assert resolved["joint_required_var_codes"] == ["BASE1", "JOINT2"]
    assert resolved["overlap_var_codes"] == ["BASE1"]
    assert resolved["joint_only_var_codes"] == ["JOINT2"]
    assert resolved["union_var_codes"] == ["BASE1", "BASE2", "JOINT2"]
    assert len(resolved["union_question_rows"]) == 3
    assert resolved["joint_configuration_ids_by_var"]["JOINT2"] == ["JCFG-SYNTH-OVERLAP"]


def test_resolver_rejects_stale_authority_release() -> None:
    registry = _registry_payload()
    registry["p3_authority_release_id"] = "P3-AUTHORITY-OLD"
    with pytest.raises(RuntimeError, match="unexpected P3 authority release"):
        resolve_shared_substrate_requirements(
            pd.DataFrame([{"source": "Synthetic", "wave": "R1", "canonical_wave": "R1", "var_code": "BASE1"}]),
            registry,
            source="Synthetic",
            canonical_wave="R1",
        )


def test_resolver_accepts_all_section85_registries_with_synthetic_rows() -> None:
    registry_paths = sorted(SECTION85_AUTHORITY.glob("registry_*.yaml"))
    assert len(registry_paths) == 9
    for registry_path in registry_paths:
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        assert isinstance(registry, dict)
        source = str(registry["source_family"])
        wave = _registry_first_wave(registry)
        codes = _registry_var_codes(registry)
        base_questions = pd.DataFrame(
            [
                {
                    "source": source,
                    "wave": wave,
                    "canonical_wave": wave,
                    "country_code": "SYN",
                    "var_code": code,
                    "question_id": f"q.{code}",
                }
                for code in codes
            ]
        )
        resolved = resolve_shared_substrate_requirements(
            base_questions,
            registry,
            source=source,
            canonical_wave=wave,
        )
        assert set(resolved["joint_required_var_codes"]).issubset(set(resolved["union_var_codes"]))
        assert set(resolved["base_var_codes"]).issubset(set(resolved["union_var_codes"]))


def _run_v550j_gate(args: list[str], *, env_database_url: str | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("DATABASE_URL", None)
    if env_database_url is not None:
        env["DATABASE_URL"] = env_database_url
    return subprocess.run(
        [sys.executable, str(V550J_COMPILER), *args],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def test_v550j_forbid_database_access_rejects_db_url(tmp_path: Path) -> None:
    result = _run_v550j_gate(
        [
            "--v550-shard-dir",
            str(tmp_path),
            "--registry-path",
            str(tmp_path / "registry.yaml"),
            "--v550j-substrate-mode",
            "prepared_required",
            "--prepared-substrate-path",
            str(tmp_path / "substrate.parquet"),
            "--prepared-substrate-manifest-path",
            str(tmp_path / "manifest.json"),
            "--response-option-map",
            str(tmp_path / "response.parquet"),
            "--forbid-database-access",
            "--db-url",
            "postgres://user@localhost/db",
        ]
    )
    assert result.returncode != 0
    assert "V550J_DATABASE_ACCESS_FORBIDDEN" in result.stderr


def test_v550j_forbid_database_access_rejects_env_database_url(tmp_path: Path) -> None:
    result = _run_v550j_gate(
        [
            "--v550-shard-dir",
            str(tmp_path),
            "--registry-path",
            str(tmp_path / "registry.yaml"),
            "--v550j-substrate-mode",
            "prepared_required",
            "--prepared-substrate-path",
            str(tmp_path / "substrate.parquet"),
            "--prepared-substrate-manifest-path",
            str(tmp_path / "manifest.json"),
            "--response-option-map",
            str(tmp_path / "response.parquet"),
            "--forbid-database-access",
        ],
        env_database_url="postgres://user@localhost/db",
    )
    assert result.returncode != 0
    assert "V550J_DATABASE_ACCESS_FORBIDDEN" in result.stderr


def test_v550j_forbid_database_access_requires_prepared_required(tmp_path: Path) -> None:
    result = _run_v550j_gate(
        [
            "--v550-shard-dir",
            str(tmp_path),
            "--registry-path",
            str(tmp_path / "registry.yaml"),
            "--v550j-substrate-mode",
            "prepared_or_build",
            "--prepared-substrate-path",
            str(tmp_path / "substrate.parquet"),
            "--prepared-substrate-manifest-path",
            str(tmp_path / "manifest.json"),
            "--response-option-map",
            str(tmp_path / "response.parquet"),
            "--forbid-database-access",
        ]
    )
    assert result.returncode != 0
    assert "prepared_required is mandatory" in result.stderr


def test_v550j_forbid_database_access_requires_explicit_substrate(tmp_path: Path) -> None:
    result = _run_v550j_gate(
        [
            "--v550-shard-dir",
            str(tmp_path),
            "--registry-path",
            str(tmp_path / "registry.yaml"),
            "--v550j-substrate-mode",
            "prepared_required",
            "--response-option-map",
            str(tmp_path / "response.parquet"),
            "--forbid-database-access",
        ]
    )
    assert result.returncode != 0
    assert "explicit prepared substrate path and manifest are required" in result.stderr


def test_shard_plan_runner_forwards_shared_substrate_arguments() -> None:
    cmd = _build_command(
        {
            "run_id": "run",
            "shard_id": "Synthetic_R1",
            "source": "Synthetic",
            "wave": "R1",
            "canonical_wave": "R1",
            "countries": "",
        },
        response_option_map=None,
        max_depth=None,
        min_cell_n=None,
        min_branch_n=None,
        min_answer_n=None,
        full_readiness=False,
        readiness_only=False,
        readiness_artifact=None,
        readiness_output_root=None,
        stop_after_stage=0,
        shared_respondent_substrate_mode="write",
        joint_configuration_registry_path="/tmp/registry.yaml",
        joint_configuration_ids=["JCFG-SYNTH-OVERLAP"],
        resume=False,
        overwrite_shard=False,
        write_csv=False,
        write_parquet=True,
    )
    assert "--shared-respondent-substrate-mode" in cmd
    assert "write" in cmd
    assert "--v550-prepared-substrate-mode" in cmd
    assert "--joint-configuration-registry-path" in cmd
    assert "/tmp/registry.yaml" in cmd
    assert "--joint-configuration-id" in cmd
    assert "JCFG-SYNTH-OVERLAP" in cmd


def test_synthetic_v550j_prepared_required_no_db_execution(tmp_path: Path) -> None:
    shard = tmp_path / "v550/shard_runs/synthetic_run/Synthetic_R1_US"
    (shard / "core").mkdir(parents=True)
    pd.DataFrame(
        [{"source": "Synthetic", "source_family": "Synthetic", "wave": "R1", "canonical_wave": "R1", "country_code": "US"}]
    ).to_parquet(shard / "shard_scope.parquet", index=False)
    pd.DataFrame(
        [
            {"source": "Synthetic", "source_family": "Synthetic", "wave": "R1", "canonical_wave": "R1", "country_code": "US", "var_code": "BASE1", "question_id": "q.base1", "question_text": "Base one"},
            {"source": "Synthetic", "source_family": "Synthetic", "wave": "R1", "canonical_wave": "R1", "country_code": "US", "var_code": "JOINT2", "question_id": "q.joint2", "question_text": "Joint two"},
        ]
    ).to_parquet(shard / "core/question_use_contract.parquet", index=False)
    raw = pd.DataFrame(
        [
            {"respondent_id": "r1", "var_code": "BASE1", "question_id": "q.base1", "question_text": "Base one", "response_value_normalized": "1", "response_label": "Yes", "normalized_response_label": "yes", "is_substantive": True, "is_valid_substantive_response": True},
            {"respondent_id": "r1", "var_code": "JOINT2", "question_id": "q.joint2", "question_text": "Joint two", "response_value_normalized": "2", "response_label": "No", "normalized_response_label": "no", "is_substantive": True, "is_valid_substantive_response": True},
            {"respondent_id": "r2", "var_code": "BASE1", "question_id": "q.base1", "question_text": "Base one", "response_value_normalized": "2", "response_label": "No", "normalized_response_label": "no", "is_substantive": True, "is_valid_substantive_response": True},
            {"respondent_id": "r2", "var_code": "JOINT2", "question_id": "q.joint2", "question_text": "Joint two", "response_value_normalized": "1", "response_label": "Yes", "normalized_response_label": "yes", "is_substantive": True, "is_valid_substantive_response": True},
        ]
    )
    frame = canonicalize_shared_respondent_substrate(
        raw,
        run_id="synthetic_run",
        shard_id="Synthetic_R1_US",
        source="Synthetic",
        source_id="Synthetic",
        wave="R1",
        canonical_wave="R1",
        country_code="US",
        base_var_codes=["BASE1"],
        joint_required_var_codes=["BASE1", "JOINT2"],
        joint_configuration_ids_by_var={"BASE1": ["JCFG-SYNTH-OVERLAP"], "JOINT2": ["JCFG-SYNTH-OVERLAP"]},
    )
    paths = shared_substrate_paths(shard / "checkpoints/respondent_substrate", source="Synthetic", canonical_wave="R1", country_code="US")
    write_shared_respondent_substrate_atomic(
        frame,
        paths,
        manifest_fields={
            "run_id": "synthetic_run",
            "shard_id": "Synthetic_R1_US",
            "source": "Synthetic",
            "source_id": "Synthetic",
            "wave": "R1",
            "canonical_wave": "R1",
            "country_code": "US",
            "response_semantics_contract_hash": "synthetic_response",
            "question_family_registry_hash": "synthetic_registry",
            "joint_configuration_authority_release_id": "V550J-BOUNDED-AUTHORITY-2026-08-02-R1",
            "p3_authority_release_id": "P3-AUTHORITY-2026-08-02-R184",
            "respondent_relation_schema_hash": "synthetic_schema",
        },
        base_var_codes=["BASE1"],
        joint_required_var_codes=["BASE1", "JOINT2"],
    )
    registry_path = tmp_path / "registry.yaml"
    registry_path.write_text(
        yaml.safe_dump(
            {
                "status": "governed",
                "source_family": "Synthetic",
                "p3_authority_release_id": "P3-AUTHORITY-2026-08-02-R184",
                "joint_configuration_authority_release_id": "V550J-BOUNDED-AUTHORITY-2026-08-02-R1",
                "families": [
                    {
                        "family_id": "JCFG-SYNTH-OVERLAP",
                        "joint_configuration_id": "JCFG-SYNTH-OVERLAP",
                        "source_family": "Synthetic",
                        "family_label": "Synthetic overlap",
                        "family_type": "synthetic",
                        "eligible_waves": ["R1"],
                        "minimum_items_answered": 2,
                        "item_role_groups": {
                            "a": [{"var_code": "BASE1", "question_implementation_id": "q.base1", "condition_label": "A"}],
                            "b": [{"var_code": "JOINT2", "question_implementation_id": "q.joint2", "condition_label": "B"}],
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    response_path = tmp_path / "response_option_map.parquet"
    pd.DataFrame(
        [
            {"source": "Synthetic", "wave": "R1", "var_code": var_code, "var_name": var_code, "value_code_normalized": code, "value_label_clean": label, "semantic_response_role": "substantive"}
            for var_code in ["BASE1", "JOINT2"]
            for code, label in [("1", "Yes"), ("2", "No")]
        ]
    ).to_parquet(response_path, index=False)
    env = os.environ.copy()
    env.pop("DATABASE_URL", None)
    result = subprocess.run(
        [
            sys.executable,
            str(V550J_COMPILER),
            "--v550-shard-dir",
            str(shard),
            "--output-root",
            str(tmp_path / "v550j"),
            "--registry-path",
            str(registry_path),
            "--response-option-map",
            str(response_path),
            "--association-mode",
            "off",
            "--no-progress",
            "--no-write-csv",
            "--v550j-substrate-mode",
            "prepared_required",
            "--prepared-substrate-path",
            str(paths.parquet_path),
            "--prepared-substrate-manifest-path",
            str(paths.manifest_path),
            "--forbid-database-access",
        ],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    manifest_path = tmp_path / "v550j/runs/synthetic_run/Synthetic_R1_US/joint_patterns/v550j_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["success"] is True
    assert manifest["tables"]["joint_response_pattern_index"]["rows"] > 0
