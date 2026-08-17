from __future__ import annotations

import argparse
import json
from pathlib import Path

import data.ddm_build_copy.compile_v5_paired_wave_preflight as preflight
import data.ddm_build_copy.resolve_pipeline_lineage as lineage
import data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke as smoke
import data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke_impl as smoke_impl
from data.ddm_build_copy.ddm_source_wave_identity import resolve_source_wave_identity


class _Artifact:
    def __init__(self, *, exists=True, readable=True, row_count=1, error=""):
        self.exists = exists
        self.readable = readable
        self.row_count = row_count
        self.error = error


def _stage(name: str, uid_source: str, uid_wave: str, *, usable: bool = True) -> lineage.StageResolution:
    return lineage.StageResolution(
        name,
        f"/repo/{name}/run",
        usable,
        "PASS/PRESENT/ALLOW" if usable else "BLOCKED_OR_MISSING",
        "" if usable else "blocked",
        {"identity": {"source_family_uid": uid_source, "wave_uid": uid_wave}},
    )


def test_supported_smoke_scope_is_exact_closed35_uid_catalog():
    pairs = []
    for source, wave, country in smoke.ALL_WAVES:
        identity, resolved_country = smoke.resolve_smoke_identity(source, wave, country)
        pairs.append((identity.source_family_uid, identity.wave_uid))
        assert resolved_country == country
        assert identity.closed_35_member is True
    assert len(smoke.ALL_WAVES) == 35
    assert len(set(pairs)) == 35
    assert ("Asian Barometer", "W6", "ID") not in smoke.ALL_WAVES


def test_smoke_aliases_share_uid_native_run_namespace():
    a = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    b = resolve_source_wave_identity("European Values Study", "W1", require_closed_35=True)
    assert (a.source_family_uid, a.wave_uid) == (b.source_family_uid, b.wave_uid)
    assert smoke.run_id_for_identity(a, "20260817T120000Z") == smoke.run_id_for_identity(
        b, "20260817T120000Z"
    )


def test_smoke_scope_duplicate_alias_is_rejected_by_uid_not_spelling():
    issues = smoke.validate_explicit_scope(
        [
            ("EVS", "1981", "BE"),
            ("European Values Study", "W1", "BE"),
        ]
    )
    assert issues == ["duplicate_source_wave_uid:sf_evs_v1|wv_evs_1981_v1"]


def test_smoke_runtime_compilers_are_exact_current_v550_to_v552j_paths():
    paths = {stage: path.name for stage, path in smoke.runtime_compiler_paths().items()}
    assert paths == {
        "v550": "build_determinicity_wave_shard_v550.py",
        "v550j": "compile_v550j_joint_response_patterns.py",
        "v551": "compile_v551_relation_evidence_atoms.py",
        "v551j": "compile_v551j_joint_evidence_packets.py",
        "v552": "compile_v552_structural_ddm.py",
        "v552j": "compile_v552j_structural_handoff.py",
    }
    assert all("v553" not in value.lower() for value in paths.values())


def test_impl_module_has_no_independent_alias_namespace():
    assert not hasattr(smoke_impl, "_source_aliases")
    assert not hasattr(smoke_impl, "_wave_aliases")
    assert smoke_impl.resolve_smoke_identity is smoke.resolve_smoke_identity
    assert smoke_impl.main is smoke.main


def test_lineage_v550_discovery_uses_manifest_uid_not_directory_spelling(tmp_path, monkeypatch):
    identity = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    root = tmp_path / "data/ddm_repository_copy/v550/shard_runs" / "opaque-run" / "not__a__wave_token"
    root.mkdir(parents=True)
    payload = {
        "run_id": "manifest-run-id",
        "shard_id": "legacy-shard-id",
        "source": "European Values Study",
        "source_family": "EVS",
        "wave": "W1",
        "canonical_wave": "1981",
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
        "success": True,
    }
    (root / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")
    (root / "bridge").mkdir()
    (root / "core").mkdir()
    (root / "bridge/v551_bridge_index.parquet").write_bytes(b"x")
    (root / "core/question_use_contract.parquet").write_bytes(b"x")
    monkeypatch.setattr(lineage, "inspect_artifact", lambda path: _Artifact())
    resolved = lineage._resolve_v550(tmp_path, identity)
    assert resolved.usable is True
    assert resolved.root == str(root)
    assert resolved.metrics["run_id"] == "manifest-run-id"
    assert resolved.metrics["shard_id"] == "legacy-shard-id"
    assert resolved.metrics["identity"]["wave_uid"] == "wv_evs_1981_v1"


def test_lineage_requested_uid_contradiction_fails_closed(tmp_path):
    identity = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    root = tmp_path / "data/ddm_repository_copy/v550/shard_runs" / "x" / "y"
    root.mkdir(parents=True)
    payload = {
        "run_id": "r",
        "shard_id": "s",
        "source": "Arab Barometer",
        "wave": "I",
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
        "success": True,
    }
    (root / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")
    resolved = lineage._resolve_v550(tmp_path, identity)
    assert resolved.usable is False
    assert "contradictory_requested_uid_manifest" in resolved.reason


def test_lineage_catalog_discovery_accepts_alias_filter_and_returns_values():
    rows = lineage._discover_wave_specs(Path("/unused"), "European Values Study")
    assert ("EVS", "1981") in rows
    assert ("EVS", "1999") in rows
    assert all(source == "EVS" for source, _ in rows)
    assert len(rows) == 5


def test_preflight_reports_base_spine_and_actual_j_traversal_separately(tmp_path, monkeypatch):
    a = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    b = resolve_source_wave_identity("EVS", "1990", require_closed_35=True)

    def fake_resolve(_repo, _source, wave):
        identity = a if str(wave) in {"1981", "W1"} else b
        stages = {
            name: _stage(name, identity.source_family_uid, identity.wave_uid)
            for name in ("v550", "v550j", "v551", "v551j", "v552", "v552j")
        }
        stages["v550"] = lineage.StageResolution(
            "v550",
            "/repo/v550",
            True,
            "PASS",
            metrics={
                "run_id": f"run-{identity.wave_uid}",
                "shard_id": f"shard-{identity.wave_uid}",
                "identity": {
                    "source_family_uid": identity.source_family_uid,
                    "wave_uid": identity.wave_uid,
                },
            },
        )
        return stages

    monkeypatch.setattr(preflight, "resolve_stage_roots", fake_resolve)
    compiler_dir = tmp_path / "compilers"
    compiler_dir.mkdir()
    compiler_paths = {}
    for stage, rel in smoke.COMPILER_SPECS.items():
        path = compiler_dir / Path(rel).name
        path.write_text("# compiler\n", encoding="utf-8")
        compiler_paths[stage] = path
    monkeypatch.setattr(preflight, "runtime_compiler_paths", lambda config: compiler_paths)

    report = preflight.build_paired_wave_preflight(tmp_path, "EVS", "BE", "W1", "W2")
    assert report["base_spine_ready"] is True
    assert report["j_branch_traversed"] is True
    assert report["comparison_ready"] is True
    assert report["wave_reports"][0]["wave_uid"] == a.wave_uid
    assert report["wave_reports"][1]["wave_uid"] == b.wave_uid
    assert report["v553_plus_checked"] is False


def test_preflight_uid_value_mismatch_blocks_even_when_stage_flags_are_usable(tmp_path, monkeypatch):
    expected = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    wrong = resolve_source_wave_identity("EVS", "1990", require_closed_35=True)

    def fake_resolve(_repo, _source, _wave):
        return {
            name: _stage(name, wrong.source_family_uid, wrong.wave_uid)
            for name in ("v550", "v550j", "v551", "v551j", "v552", "v552j")
        }

    monkeypatch.setattr(preflight, "resolve_stage_roots", fake_resolve)
    compiler = tmp_path / "compiler.py"
    compiler.write_text("# compiler\n", encoding="utf-8")
    monkeypatch.setattr(
        preflight,
        "runtime_compiler_paths",
        lambda config: {stage: compiler for stage in smoke.COMPILER_SPECS},
    )
    row = preflight._wave_report(tmp_path, "EVS", "1981", "BE")
    assert row["base_spine_ready"] is True
    assert row["j_branch_traversed"] is True
    assert row["full_v550_to_v552j_ready"] is False
    assert row["uid_mismatch_stages"] == ["v550", "v550j", "v551", "v551j", "v552", "v552j"]
    assert row["wave_uid"] == expected.wave_uid


def test_smoke_summary_distinguishes_base_from_untraversed_j_branch(tmp_path):
    rows = [
        {
            "survey_family": "EVS",
            "wave_id": "1981",
            "source_family_uid": "sf_evs_v1",
            "wave_uid": "wv_evs_1981_v1",
            "country": "BE",
            "base_spine_passed": True,
            "joint_branch": {"traversed": False, "status": "not_traversed"},
            "full_chain_passed": False,
            "acceptance_boundary": "typed_base_spine",
            "passed": True,
        }
    ]
    smoke.write_summaries(rows, str(tmp_path), "fixed", False, {"passed": True})
    payload = json.loads((tmp_path / "reports/smoke_summary.json").read_text(encoding="utf-8"))
    assert payload["results"][0]["base_spine_passed"] is True
    assert payload["results"][0]["joint_branch"]["traversed"] is False
    assert payload["results"][0]["full_chain_passed"] is False
    text = (tmp_path / "reports/smoke_report.md").read_text(encoding="utf-8")
    assert "Base V550→V552 spines passed: 1" in text
    assert "J branches actually traversed: 0" in text


def test_parse_args_compatibility_does_not_overwrite_explicit_joint_mode(monkeypatch):
    monkeypatch.setattr(smoke, "_ORIGINAL_PARSE_ARGS", lambda: argparse.Namespace(joint_mode="required"))
    monkeypatch.setattr("sys.argv", ["prog", "--joint-mode=required"])
    assert smoke.parse_args().joint_mode == "required"
