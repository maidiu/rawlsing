#!/usr/bin/env python3
"""Run the bounded Section 85 nine-family diagnostic smoke matrix."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


SECTION = Path("section85")
BASE_MODULE_DIR = Path("data/ddm_build_copy")
BINDING_AUTHORITY_RELATIVE = SECTION / "authority/section85_binding_authority.json"
DEFAULT_QSM_RELATION = "question_structural_mapping"
DEFAULT_CANONICAL_REGISTRY_RELATION = "rawlsing_authority_reconcile_ar_20260719t213835z.canonical_question_registry"

PRIVACY_PATH_RE = re.compile(
    r"(respondent_substrate|respondent_membership|raw_response|raw_responses|\.env$|DATABASE_URL|data\.parquet$)",
    re.IGNORECASE,
)
PRIVACY_COLUMN_RE = re.compile(
    r"(^respondent_id$|^respondent_ids$|respondent_membership|caseid|person_id|raw_response|DATABASE_URL|password|secret|token)",
    re.IGNORECASE,
)
SECRET_RE = re.compile(r"postgres(?:ql)?://[^@\s]+@", re.IGNORECASE)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_env_database_url(path: Path) -> str:
    if not path.exists():
        return os.environ.get("DATABASE_URL", "")
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("DATABASE_URL="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("DATABASE_URL", "")


def redacted(value: str) -> str:
    return SECRET_RE.sub("postgresql://<redacted>@", value or "")


def source_slug(source: str) -> str:
    return {
        "Afrobarometer": "afrobarometer",
        "Arab Barometer": "arab_barometer",
        "Asian Barometer": "asian_barometer",
        "EVS": "evs",
        "GSS": "gss",
        "Latinobarómetro": "latinobarometro",
        "LiTS": "lits",
        "South Asia": "south_asia",
        "WVS": "wvs",
    }[source]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def load_binding_authority(repo_root: Path) -> dict[str, Any]:
    payload = load_json(repo_root / BINDING_AUTHORITY_RELATIVE)
    return payload if payload else {
        "database_bindings": {
            "qsm_relation": {"canonical": DEFAULT_QSM_RELATION},
            "canonical_registry_relation": {"canonical": DEFAULT_CANONICAL_REGISTRY_RELATION},
            "response_long_relation": {"preferred": "public.v_ddm_response_long_facet_ready_authority"},
        }
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({field: row.get(field, "") for field in fields})


def load_base(repo_root: Path):
    sys.path.insert(0, str((repo_root / BASE_MODULE_DIR).resolve()))
    import run_20var_allwaves_v550_552j_smoke as base

    return base


def section85_inventory(repo_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    authority = pd.read_csv(repo_root / SECTION / "authority/bounded_joint_configuration_authority.csv")
    items = pd.read_csv(repo_root / SECTION / "authority/bounded_joint_configuration_item_crosswalk.csv")
    inventory: list[dict[str, Any]] = []
    surfaces: list[dict[str, Any]] = []
    for _, cfg in authority.iterrows():
        cfg_id = str(cfg["joint_configuration_id"])
        cfg_items = items[items["joint_configuration_id"].astype(str).eq(cfg_id)].sort_values("item_order")
        registry = repo_root / SECTION / "authority" / f"registry_{source_slug(str(cfg['source_family']))}.yaml"
        member_vars = [str(v) for v in cfg_items["var_code"].tolist()]
        item_roles = [str(v) for v in cfg_items["item_role"].tolist()]
        inventory.append({
            "configuration_id": cfg_id,
            "survey_family": cfg["source_family"],
            "intended_wave": cfg["wave"],
            "country_code": cfg["country_code"],
            "member_variables": json.dumps(member_vars, ensure_ascii=False),
            "item_roles": json.dumps(item_roles, ensure_ascii=False),
            "family_type": cfg["family_type"],
            "minimum_items_answered": cfg["minimum_items_answered"],
            "response_role_rules": json.dumps(_registry_response_role_rules(registry, cfg_id), ensure_ascii=False, sort_keys=True),
            "status": cfg["configuration_authority_status"],
            "authority_id": cfg["joint_configuration_authority_release_id"],
            "registry_path": str(registry),
            "registry_sha256": sha256_file(registry),
        })
        filter_path = repo_root / SECTION / "inputs" / f"{source_slug(str(cfg['source_family'])).replace('arab_barometer', 'arabbarometer').replace('asian_barometer', 'asianbarometer').replace('latinobarometro', 'latinobarometro')}_{str(cfg['wave']).lower()}.json"
        manifest = pd.read_csv(repo_root / SECTION / "authority/bounded_nine_scope_manifest.csv")
        row = manifest[manifest["joint_configuration_id"].astype(str).eq(cfg_id)].iloc[0]
        filter_payload = load_json(repo_root / SECTION / "inputs" / str(row["filter_file"]))
        base_vars = list(dict.fromkeys([str(v) for v in filter_payload.get("var_codes", [])]))
        union = list(dict.fromkeys(base_vars + member_vars))
        for var in union:
            surfaces.append({
                "configuration_id": cfg_id,
                "survey_family": cfg["source_family"],
                "scope": row["scope_dir"],
                "variable": var,
                "in_base_smoke_variables": var in base_vars,
                "in_joint_configuration_closure_variables": var in member_vars,
                "in_union": True,
                "include_reason": "section85_closure_member" if var in member_vars else "section85_bounded_smoke_context",
            })
    return inventory, surfaces


def _registry_response_role_rules(registry: Path, cfg_id: str) -> list[dict[str, Any]]:
    payload = yaml.safe_load(registry.read_text(encoding="utf-8"))
    for family in payload.get("families", []):
        if family.get("joint_configuration_id") == cfg_id or family.get("family_id") == cfg_id:
            return family.get("response_role_rules", [])
    return []


def summarize_rows(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        if path.suffix == ".parquet":
            import pyarrow.parquet as pq

            return int(pq.ParquetFile(path).metadata.num_rows)
        if path.suffix == ".csv":
            return max(0, sum(1 for _ in path.open(encoding="utf-8", errors="ignore")) - 1)
        if path.suffix == ".json":
            payload = load_json(path)
            for key in ("row_count", "rows", "candidate_packet_count", "component_row_count", "certified_packet_count"):
                if key in payload:
                    return int(payload[key] or 0)
    except Exception:
        return 0
    return 0


def current_v551j_gate(v551j_root: Path) -> dict[str, Any]:
    manifest = load_json(v551j_root / "manifest/manifest.json")
    readiness = load_json(v551j_root / "manifest/v551j_readiness_report.json")
    validation = load_json(v551j_root / "manifest/v551j_packet_contract_validation_report.json")
    return {
        "final_status": readiness.get("final_status") or manifest.get("final_status", ""),
        "candidate_packet_count": readiness.get("candidate_packet_count", manifest.get("row_counts", {}).get("candidate", 0)),
        "component_row_count": readiness.get("component_row_count", manifest.get("row_counts", {}).get("component", 0)),
        "certified_packet_count": readiness.get("certified_packet_count", manifest.get("row_counts", {}).get("certified", 0)),
        "review_required_packet_count": readiness.get("review_required_packet_count", 0),
        "blocked_packet_count": readiness.get("blocked_packet_count", 0),
        "ready_for_review": readiness.get("ready_for_review", False),
        "ready_for_v552j_joint_evidence": readiness.get("ready_for_v552j_joint_evidence", False),
        "candidate_contract_valid": readiness.get("candidate_contract_valid", validation.get("candidate_contract_valid", False)),
        "component_contract_valid": readiness.get("component_contract_valid", validation.get("component_contract_valid", False)),
        "issues_json": validation.get("issues_json", "[]"),
    }


def field_inventory(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or PRIVACY_PATH_RE.search(path.as_posix()):
            continue
        rel = path.relative_to(root).as_posix()
        stage = next((part for part in path.parts if part.lower() in {"v550", "v551", "v552", "v550j", "v551j", "v552j"}), "")
        try:
            if path.suffix == ".parquet":
                import pyarrow.parquet as pq

                pf = pq.ParquetFile(path)
                table = pf.read()
                df = table.to_pandas()
                for name in df.columns:
                    rows.append({
                        "artifact": rel,
                        "source_stage": stage,
                        "column_name": name,
                        "type": str(df[name].dtype),
                        "row_grain": infer_grain(rel),
                        "null_count": int(df[name].isna().sum()),
                        "destination_stage_where_mapped": infer_destination(name),
                    })
            elif path.suffix == ".csv":
                df = pd.read_csv(path, nrows=10000)
                for name in df.columns:
                    rows.append({
                        "artifact": rel,
                        "source_stage": stage,
                        "column_name": name,
                        "type": str(df[name].dtype),
                        "row_grain": infer_grain(rel),
                        "null_count": int(df[name].isna().sum()),
                        "destination_stage_where_mapped": infer_destination(name),
                    })
        except Exception as exc:
            rows.append({"artifact": rel, "source_stage": stage, "column_name": "", "type": "ERROR", "row_grain": "", "null_count": "", "destination_stage_where_mapped": str(exc)})
    return rows


def infer_grain(rel: str) -> str:
    text = rel.lower()
    for token, grain in [
        ("pattern_item", "joint pattern item/component"),
        ("component", "component"),
        ("candidate", "candidate packet"),
        ("atom", "relation atom"),
        ("pressure_observation", "pressure observation"),
        ("question_use_contract", "question"),
        ("bridge", "bridge row"),
        ("pattern", "joint pattern"),
    ]:
        if token in text:
            return grain
    return "artifact row"


def infer_destination(name: str) -> str:
    n = name.lower()
    if "pattern_id" in n or "family" in n or "component" in n:
        return "v550j,v551j,v552j"
    if "atom_id" in n or "empirical_distribution" in n or "measurement" in n or "denominator" in n:
        return "v551,v551j,v552"
    if "pressure" in n or "structural" in n or "target" in n or "horizon" in n:
        return "v552,v552j"
    if "certification" in n or "review" in n:
        return "v551j,v552j"
    return ""


def copy_nonrespondent(src: Path, dst: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    manifest: list[dict[str, Any]] = []
    privacy: list[dict[str, Any]] = []
    for path in sorted(src.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(src)
        rel_text = rel.as_posix()
        if PRIVACY_PATH_RE.search(rel_text):
            privacy.append({"path": rel_text, "action": "excluded", "reason": "privacy_path_rule"})
            continue
        if path.suffix == ".parquet":
            try:
                import pyarrow.parquet as pq

                columns = pq.ParquetFile(path).schema.names
            except Exception as exc:
                privacy.append({"path": rel_text, "action": "excluded", "reason": f"schema_unreadable:{exc}"})
                continue
            bad = [c for c in columns if PRIVACY_COLUMN_RE.search(c)]
            if bad:
                privacy.append({"path": rel_text, "action": "excluded", "reason": "privacy_columns:" + ",".join(bad[:10])})
                continue
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix.lower() in {".json", ".csv", ".txt", ".log", ".md", ".yaml", ".yml"} and path.stat().st_size < 32 * 1024 * 1024:
            target.write_text(redacted(path.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
        else:
            shutil.copy2(path, target)
        manifest.append({"relative_path": rel_text, "size_bytes": target.stat().st_size, "sha256": sha256_file(target)})
    return manifest, privacy


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--env-file", type=Path, required=True)
    parser.add_argument("--response-option-map", type=Path, required=True)
    parser.add_argument("--question-structure-register", type=Path, required=True)
    parser.add_argument(
        "--qsm-relation",
        default=os.environ.get("DDM_QSM_RELATION"),
        help="Question structural mapping relation. Defaults to the same public relation proven by Section 85 preflight.",
    )
    parser.add_argument(
        "--canonical-registry-relation",
        default=os.environ.get("DDM_CANONICAL_REGISTRY_RELATION"),
        help="Canonical question registry relation.",
    )
    parser.add_argument("--only-scope", action="append", default=[])
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    os.chdir(repo)
    binding_authority = load_binding_authority(repo)
    db_bindings = binding_authority.get("database_bindings", {}) if isinstance(binding_authority.get("database_bindings"), dict) else {}
    if not args.qsm_relation:
        args.qsm_relation = (db_bindings.get("qsm_relation") or {}).get("canonical") or DEFAULT_QSM_RELATION
    if not args.canonical_registry_relation:
        args.canonical_registry_relation = (
            (db_bindings.get("canonical_registry_relation") or {}).get("canonical")
            or DEFAULT_CANONICAL_REGISTRY_RELATION
        )
    output = args.output_root.resolve()
    reports = output / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    write_json(reports / "SECTION85_BINDING_AUTHORITY_USED.json", binding_authority)

    base = load_base(repo)
    db_url = read_env_database_url(args.env_file)
    runtime = repo
    config = base.RuntimeConfig(
        repo_root=runtime,
        env_file=args.env_file.resolve(),
        db_url=db_url,
        qsm_relation=args.qsm_relation,
        canonical_registry_relation=args.canonical_registry_relation,
        response_option_map=args.response_option_map.resolve(),
        joint_registry_paths=tuple((repo / SECTION / "authority" / f"registry_{source_slug(row['source_family'])}.yaml").resolve() for row in csv.DictReader((repo / SECTION / "authority/bounded_nine_scope_manifest.csv").open())),
        association_lane_registry=repo / "data/ddm_registries/association_lane_registry.yaml",
        association_threshold_profiles=repo / "data/ddm_registries/association_threshold_profiles.yaml",
        first_pass_authority_dir=repo / "data/ddm_build_copy/reports",
        semantic_authority_dir=repo / "data/ddm_build_copy/reports",
        position_conditioning_authority_dir=repo / "data/ddm_build_copy/reports",
        directionality_authority_dir=repo / "data/ddm_build_copy/directionality_authority",
        association_mode="off",
        joint_mode="required",
        readiness_mode="full",
        diagnostic_continue=True,
    )
    os.environ["DDM_QUESTION_STRUCTURE_REGISTER"] = str(args.question_structure_register.resolve())

    database_contract = base.inspect_database_contract(config, db_url)
    write_json(reports / "DATABASE_RELATION_BINDING.json", database_contract)
    if not database_contract.get("checked") or not database_contract.get("passed"):
        raise RuntimeError(
            "database_relation_preflight_failed:"
            + json.dumps(database_contract, sort_keys=True, default=str)
        )

    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    status = subprocess.check_output(["git", "status", "--short"], cwd=repo, text=True)
    write_json(reports / "CURRENT_STATE_CAPTURE.json", {
        "git_commit": commit,
        "git_status_short": status,
        "database_url_redacted": redacted(db_url),
        "env_file": str(args.env_file),
        "response_option_map": str(args.response_option_map),
        "question_structure_register": str(args.question_structure_register),
        "runtime_repo_root": str(runtime),
        "binding_authority_path": str((repo / BINDING_AUTHORITY_RELATIVE).resolve()),
        "binding_authority_id": binding_authority.get("authority_id", ""),
        "qsm_relation_requested": args.qsm_relation,
        "qsm_relation_resolved": database_contract.get("relations", {}).get("qsm_relation", {}).get("resolved", ""),
        "canonical_registry_relation_requested": args.canonical_registry_relation,
        "canonical_registry_relation_resolved": database_contract.get("relations", {}).get("canonical_registry_relation", {}).get("resolved", ""),
        "response_long_relation_resolved": database_contract.get("relations", {}).get("response_long_relation", {}).get("resolved", ""),
    })
    inventory, surfaces = section85_inventory(repo)
    write_csv(reports / "SECTION85_CONFIGURATION_INVENTORY.csv", inventory, list(inventory[0]))
    write_csv(reports / "SMOKE_VARIABLE_SURFACE.csv", surfaces, list(surfaces[0]))

    manifest_rows = list(csv.DictReader((repo / SECTION / "authority/bounded_nine_scope_manifest.csv").open()))
    if args.only_scope:
        wanted = set(args.only_scope)
        manifest_rows = [row for row in manifest_rows if row["scope_dir"] in wanted or row["source_family"] in wanted or row["joint_configuration_id"] in wanted]

    results: list[dict[str, Any]] = []
    run_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for row in manifest_rows:
        source, wave, country = row["source_family"], row["wave"], row["country_code"]
        filter_path = repo / SECTION / "inputs" / row["filter_file"]
        filter_payload = load_json(filter_path)
        selected = list(dict.fromkeys([str(v) for v in filter_payload.get("var_codes", [])]))
        registry = repo / SECTION / "authority" / f"registry_{source_slug(source)}.yaml"
        scoped_config = config._replace(joint_registry_paths=(registry.resolve(),))
        result = base.run_wave(source, str(wave), country, run_ts, str(output / "live_outputs"), str(filter_path), selected, scoped_config)
        result["configuration_id"] = row["joint_configuration_id"]
        result["scope_dir"] = row["scope_dir"]
        result["section85_filter_path"] = str(filter_path)
        result["section85_registry_path"] = str(registry)
        v551j_root = output / "live_outputs/v551j" / f"{source}_{wave}_{country}"
        result["current_v551j_gate"] = current_v551j_gate(v551j_root)
        results.append(result)
        write_json(reports / "SECTION85_DIAGNOSTIC_PARTIAL_RETURN.json", {"results": results})

    base.write_summaries(results, str(output / "live_outputs"), run_ts, False, {"section85": True})

    matrix_rows: list[dict[str, Any]] = []
    for result in results:
        fc = result.get("functional_checks", {})
        gate = result.get("current_v551j_gate", {})
        matrix_rows.append({
            "configuration_id": result.get("configuration_id", ""),
            "scope": result.get("scope_dir", ""),
            "selected_variable_count": result.get("selected_variable_count", ""),
            "closure_variable_count": len(json.loads(next((x["member_variables"] for x in inventory if x["configuration_id"] == result.get("configuration_id")), "[]"))),
            "v550_status": result.get("stages", {}).get("v550", {}).get("exit_code", ""),
            "quc_relation_evidence_count": fc.get("v550_quc", {}).get("relation_rows", ""),
            "v551_atom_count": fc.get("v551", {}).get("atom_rows", ""),
            "v552_pressure_observation_count": fc.get("v552", {}).get("pressure_observation_rows", fc.get("v552", {}).get("atoms_row_count", "")),
            "v550j_pattern_count": fc.get("v550j", {}).get("pattern_rows", ""),
            "v550j_component_count": summarize_rows(output / "live_outputs/v550j/runs" / result.get("run_id", "") / f"{result.get('survey_family')}_{result.get('wave_id')}_{result.get('country')}" / "joint_patterns/joint_response_pattern_item_index.parquet"),
            "v551j_candidate_count": gate.get("candidate_packet_count", ""),
            "v551j_certified_count": gate.get("certified_packet_count", ""),
            "v551j_review_count": gate.get("review_required_packet_count", ""),
            "v551j_blocked_count": gate.get("blocked_packet_count", ""),
            "v552j_status": fc.get("v552j", {}).get("status", ""),
            "first_failing_stage": result.get("failure_stage", ""),
            "exact_error_or_validation_issue": result.get("functional_failure_reason", "") or gate.get("issues_json", ""),
        })
    write_csv(reports / "CROSS_SOURCE_RESULT_MATRIX.csv", matrix_rows, list(matrix_rows[0]) if matrix_rows else [])
    write_json(reports / "SECTION85_DIAGNOSTIC_RETURN.json", {"status": "COMPLETE_DIAGNOSTIC_MATRIX", "results": results})

    fields = field_inventory(output / "live_outputs")
    if fields:
        write_csv(reports / "FIELD_PRESERVATION_INVENTORY.csv", fields, list(fields[0]))

    package_root = output / "package_work"
    if package_root.exists():
        shutil.rmtree(package_root)
    package_root.mkdir(parents=True)
    (package_root / "README_FIRST.md").write_text(
        "# Section 85 nine-family diagnostic smoke package\n\n"
        "This package contains diagnostic nonrespondent outputs only. It does not claim production completeness and does not include respondent substrate, respondent membership, raw responses, .env, or credentials.\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "bundle", "create", str(package_root / "section85_diagnostic_harness.bundle"), "4191b517dbc34aa61a6584bbd4d6a3005057629f..HEAD"], cwd=repo, check=True)
    shutil.copytree(repo / SECTION / "authority", package_root / "authority")
    shutil.copytree(reports, package_root / "reports")
    manifest, privacy = copy_nonrespondent(output / "live_outputs", package_root / "nonrespondent_outputs")
    write_csv(package_root / "NONRESPONDENT_OUTPUT_MANIFEST.csv", manifest, ["relative_path", "size_bytes", "sha256"])
    write_csv(package_root / "PRIVACY_RETURN.csv", privacy, ["path", "action", "reason"])
    all_files = [{"relative_path": p.relative_to(package_root).as_posix(), "size_bytes": p.stat().st_size, "sha256": sha256_file(p)} for p in sorted(package_root.rglob("*")) if p.is_file()]
    write_csv(package_root / "SHA256_MANIFEST.csv", all_files, ["relative_path", "size_bytes", "sha256"])
    zip_path = output / "Rawlsing_Section85_Nine_Family_Diagnostic_Smoke_6ba0d67.zip"
    if zip_path.exists():
        zip_path.unlink()
    shutil.make_archive(str(zip_path.with_suffix("")), "zip", package_root)
    print(json.dumps({"status": "COMPLETE_DIAGNOSTIC_MATRIX", "zip": str(zip_path), "sha256": sha256_file(zip_path), "size_bytes": zip_path.stat().st_size}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
