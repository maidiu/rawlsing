#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import shlex
import subprocess
import sys
import time
import unicodedata
from pathlib import Path
from typing import Any

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from section85_typed_state import typed_stage_gate  # noqa: E402


def norm(value: str) -> str:
    return unicodedata.normalize("NFC", str(value)).casefold()


def resolve_child(root: Path, wanted: str) -> Path:
    exact = root / wanted
    if exact.exists():
        return exact
    candidates = [path for path in root.iterdir() if norm(path.name) == norm(wanted)] if root.exists() else []
    if len(candidates) != 1:
        raise RuntimeError(f"Cannot resolve {wanted!r} under {root}; candidates={candidates}")
    return candidates[0]


def find_script(repo_root: Path, name: str) -> Path:
    candidates = [
        repo_root / "data" / "ddm_build_copy" / name,
        repo_root / "02_CORE_REFERENCE" / "code" / name,
        repo_root / "35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE" / "runtime_reproducibility_code" / "data" / "ddm_build_copy" / name,
    ]
    for path in candidates:
        if path.exists():
            return path.resolve()
    raise FileNotFoundError(f"Missing compiler {name}; searched {candidates}")


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def invoke(command: list[str], *, cwd: Path, log_path: Path, timeout: int, env: dict[str, str]) -> dict[str, Any]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    completed = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, timeout=timeout)
    elapsed = round(time.time() - started, 3)
    log_path.write_text(
        "$ " + shlex.join(command) + "\n\n--- STDOUT ---\n" + completed.stdout + "\n--- STDERR ---\n" + completed.stderr,
        encoding="utf-8",
    )
    return {
        "exit_code": completed.returncode,
        "elapsed_seconds": elapsed,
        "command": command,
        "log_path": str(log_path),
        "stdout_tail": completed.stdout[-4000:],
        "stderr_tail": completed.stderr[-4000:],
    }


def optional_context_args(structural_dir: Path) -> list[str]:
    mapping = {
        "--v552-question-semantic-hierarchy-path": "question_semantic_hierarchy.parquet",
        "--v552-structural-channel-index-path": "structural_channel_index.parquet",
        "--v552-relation-axis-pressure-path": "relation_axis_pressure.parquet",
        "--v552-target-entity-pressure-path": "target_entity_pressure.parquet",
        "--v552-driver-facet-pressure-path": "driver_facet_pressure.parquet",
        "--v552-contradiction-surface-path": "contradiction_surface.parquet",
        "--v552-horizon-constraint-index-path": "horizon_constraint_index.parquet",
        "--v552-parent-prior-manifest-path": "parent_prior_manifest.parquet",
        "--v552-artifact-authority-index-path": "v552_artifact_authority_index.parquet",
        "--v552-known-absence-register-path": "v552_known_absence_register.parquet",
        "--v552-structural-fact-index-path": "v552_structural_fact_index.parquet",
        "--v552-temporal-key-source-index-path": "v552_temporal_key_source_index.parquet",
    }
    args: list[str] = []
    for flag, filename in mapping.items():
        path = structural_dir / filename
        if path.exists():
            args.extend([flag, str(path)])
    return args


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def build_plan(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    repo = args.repo_root.resolve()
    section = args.section.resolve()
    canary = args.canary_root.resolve()
    output = args.output_root.resolve()
    manifest_rows = read_manifest(section / "authority" / "bounded_nine_scope_manifest.csv")
    requested = {norm(value) for value in args.scope} if args.scope else set()
    if requested:
        manifest_rows = [row for row in manifest_rows if norm(row["scope_dir"]) in requested or norm(row["source_family"]) in requested]
        if not manifest_rows:
            raise RuntimeError(f"No scopes match --scope values {args.scope}")

    compilers = {
        "v550j": find_script(repo, "compile_v550j_joint_response_patterns.py"),
        "v551j": find_script(repo, "compile_v551j_joint_evidence_packets.py"),
        "v552j": find_script(repo, "compile_v552j_runtime_safe_structural_handoff.py"),
    }
    env_file = args.env_file.resolve() if args.env_file else repo / ".env"
    db_url = args.db_url or os.environ.get("DATABASE_URL", "")
    plan: list[dict[str, Any]] = []

    for row in manifest_rows:
        scope = row["scope_dir"]
        shard_matches = list(canary.glob(f"v550/shard_runs/*/{scope}"))
        if len(shard_matches) != 1:
            shard_matches = []
            for parent in (canary / "v550" / "shard_runs").iterdir():
                try:
                    shard_matches.append(resolve_child(parent, scope))
                except RuntimeError:
                    pass
        if len(shard_matches) != 1:
            raise RuntimeError(f"Expected one V550 shard for {scope}, found {shard_matches}")
        shard_dir = shard_matches[0].resolve()
        run_id = shard_dir.parent.name
        shard_id = shard_dir.name
        filter_path = (section / "inputs" / row["filter_file"]).resolve()
        registry = (section / "authority" / f"registry_{source_slug(row['source_family'])}.yaml").resolve()
        response_map = (shard_dir / "core" / "response_option_map.parquet").resolve()
        v551_scope = resolve_child(canary / "v551", scope)
        atoms = (v551_scope / "relation_evidence_atoms.parquet").resolve()
        v552_scope = resolve_child(canary / "v552", scope)
        structural_dir = v552_scope / "structural"

        v550j_output_root = output / "v550j"
        v550j_artifacts = v550j_output_root / "runs" / run_id / shard_id / "joint_patterns"
        v551j_output_root = output / "v551j"
        v551j_run_root = v551j_output_root / shard_id
        v552j_output_root = output / "v552j"

        v550j = [
            sys.executable, str(compilers["v550j"]),
            "--v550-shard-dir", str(shard_dir),
            "--output-root", str(v550j_output_root),
            "--registry-path", str(registry),
            "--response-option-map", str(response_map),
            "--question-filter-file", str(filter_path),
            "--env-file", str(env_file),
            "--association-mode", "off",
            "--v550j-substrate-mode", args.substrate_mode,
            "--no-progress", "--no-write-csv", "--write-parquet", "--with-diagnostics",
        ]
        if db_url:
            v550j.extend(["--db-url", db_url])

        # The V551J producer CLI is owned by W03-B. Its final G3B producer-bound
        # input hooks are intentionally not guessed here; this command remains the
        # current G2 invocation until that worker merges.
        v551j = [
            sys.executable, str(compilers["v551j"]),
            "--run-id", shard_id,
            "--v551-atoms-path", str(atoms),
            "--v550j-pattern-index-path", str(v550j_artifacts / "joint_response_pattern_index.parquet"),
            "--v550j-pattern-item-index-path", str(v550j_artifacts / "joint_response_pattern_item_index.parquet"),
            "--v550j-relation-signature-path", str(v550j_artifacts / "joint_pattern_relation_signature.parquet"),
            "--v550j-manifest-path", str(v550j_artifacts / "v550j_manifest.json"),
            "--v550j-readiness-report-path", str(v550j_artifacts / "v550j_source_wave_readiness_report.json"),
            "--v550j-meaning-summary-path", str(v550j_artifacts / "joint_pattern_meaning_summary.parquet"),
            "--registry-path", str(registry),
            "--output-root", str(v551j_output_root),
            "--emit-review-surface", "--emit-certified-index", "--no-write-csv", "--write-parquet", "--strict",
        ]
        for flag, filename in {
            "--v552-question-semantic-hierarchy-path": "question_semantic_hierarchy.parquet",
            "--v552-structural-channel-index-path": "structural_channel_index.parquet",
            "--v552-relation-axis-pressure-path": "relation_axis_pressure.parquet",
            "--v552-target-entity-pressure-path": "target_entity_pressure.parquet",
            "--v552-driver-facet-pressure-path": "driver_facet_pressure.parquet",
            "--v552-contradiction-surface-path": "contradiction_surface.parquet",
            "--v552-horizon-constraint-index-path": "horizon_constraint_index.parquet",
            "--v552-parent-prior-manifest-path": "parent_prior_manifest.parquet",
        }.items():
            path = structural_dir / filename
            if path.exists():
                v551j.extend([flag, str(path)])

        # W06-B owns the final V552J producer hook. Preserve the current command
        # until G4 rather than guessing its future manifest/CLI contract.
        v552j = [
            sys.executable, str(compilers["v552j"]),
            "--run-id", shard_id,
            "--v551j-run-root", str(v551j_run_root),
            "--output-root", str(v552j_output_root),
            "--write-parquet", "--no-write-csv", "--strict",
        ] + optional_context_args(structural_dir)

        plan.append({
            "source_family": row["source_family"],
            "wave": row["wave"],
            "country_code": row["country_code"],
            "scope_dir": scope,
            "run_id": run_id,
            "shard_id": shard_id,
            "joint_configuration_id": row["joint_configuration_id"],
            "v550_shard_dir": str(shard_dir),
            "filter_path": str(filter_path),
            "registry_path": str(registry),
            "response_option_map_path": str(response_map),
            "v551_atoms_path": str(atoms),
            "v552_structural_context_dir": str(structural_dir),
            "commands": {"v550j": v550j, "v551j": v551j, "v552j": v552j},
            "expected_outputs": {
                "v550j_manifest": str(v550j_artifacts / "v550j_manifest.json"),
                "v550j_readiness": str(v550j_artifacts / "v550j_source_wave_readiness_report.json"),
                "v551j_manifest": str(v551j_run_root / "manifest" / "manifest.json"),
                "v551j_readiness": str(v551j_run_root / "manifest" / "v551j_readiness_report.json"),
                "v552j_readiness": str(v552j_output_root / shard_id / "manifest" / "v552j_readiness_report.json"),
            },
        })

    preflight = {
        "status": "PASS_PLAN_READY" if plan else "FAIL_EMPTY_PLAN",
        "scope_count": len(plan),
        "database_url_supplied": bool(db_url),
        "database_required_for_execution": True,
        "python_executable": sys.executable,
        "required_modules": {name: importlib.util.find_spec(name) is not None for name in ("pandas", "yaml", "pyarrow")},
        "compilers": {key: str(value) for key, value in compilers.items()},
        "authority_scope": "BOUNDED_9_SOURCE_FAMILY_20_VARIABLE_CANARY",
        "production_completeness_claim": "NO_PRODUCTION_COMPLETENESS_CLAIM",
        "association_mode": "off",
        "section85_typed_state_contract": "rawlsing_pipeline_boundary_v1",
        "v551j_acceptance_hook": "AWAITING_G3B_PRODUCER_HOOK",
        "v552j_acceptance_hook": "AWAITING_G4_PRODUCER_HOOK",
    }
    return plan, preflight


def _typed_functional_gate(entry: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, bool]]:
    v550j_manifest = load_json(Path(entry["expected_outputs"]["v550j_manifest"]))
    v550j_ready = load_json(Path(entry["expected_outputs"]["v550j_readiness"]))
    v551j_manifest = load_json(Path(entry["expected_outputs"]["v551j_manifest"]))
    v552j_document = load_json(Path(entry["expected_outputs"]["v552j_readiness"]))

    v551j_state = typed_stage_gate(v551j_manifest, stage="v551j")
    v552j_state = typed_stage_gate(v552j_document, stage="v552j")
    checks = {
        "v550j_success": bool(v550j_manifest.get("success")),
        "v550j_validation_pass": str(v550j_manifest.get("validation_status", "")).lower() == "pass",
        "v550j_registry_applicable": v550j_ready.get("family_registry_status") == "applicable",
        "v550j_not_blocked": not v550j_ready.get("blocking_issues"),
        "v551j_typed_contract_valid": bool(v551j_state["typed_contract_valid"]),
        "v551j_run_integrity_pass": bool(v551j_state["integrity_pass"]),
        "v552j_typed_contract_valid": bool(v552j_state["typed_contract_valid"]),
        "v552j_run_integrity_pass": bool(v552j_state["integrity_pass"]),
    }
    return v551j_state, v552j_state, checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the exact bounded nine-source V550J -> V551J -> V552J canary on a live respondent database.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--section", type=Path, required=True)
    parser.add_argument("--canary-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--db-url", default="")
    parser.add_argument("--env-file", type=Path, default=None)
    parser.add_argument("--scope", action="append", default=[])
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--continue-on-failure", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=3600)
    parser.add_argument("--substrate-mode", choices=("prepared_required", "prepared_or_build", "prepared_or_forensic_fallback", "forensic_reharmonize"), default="prepared_or_build")
    args = parser.parse_args()

    args.output_root.mkdir(parents=True, exist_ok=True)
    plan, preflight = build_plan(args)
    reports = args.output_root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "bounded_nine_canary_execution_plan.json").write_text(json.dumps({"preflight": preflight, "plan": plan}, indent=2) + "\n", encoding="utf-8")

    if args.plan_only:
        print(json.dumps({"status": "PASS_PLAN_ONLY", "preflight": preflight, "scope_count": len(plan)}, indent=2))
        return 0
    if not preflight["database_url_supplied"] and not (args.env_file and args.env_file.exists()) and not os.environ.get("DATABASE_URL"):
        raise RuntimeError("LIVE_RESPONDENT_DATABASE_REQUIRED: supply --db-url, DATABASE_URL, or an --env-file containing DATABASE_URL")
    missing_modules = [name for name, present in preflight["required_modules"].items() if not present]
    if missing_modules:
        raise RuntimeError("MISSING_RUNTIME_MODULES: " + ",".join(missing_modules))

    environment = os.environ.copy()
    results: list[dict[str, Any]] = []
    for entry in plan:
        scope = entry["scope_dir"]
        result: dict[str, Any] = {key: entry[key] for key in ("source_family", "wave", "country_code", "scope_dir", "run_id", "shard_id", "joint_configuration_id")}
        result["stages"] = {}
        failed = False
        for stage in ("v550j", "v551j", "v552j"):
            run = invoke(entry["commands"][stage], cwd=args.repo_root, log_path=args.output_root / "logs" / scope / f"{stage}.log", timeout=args.timeout_seconds, env=environment)
            result["stages"][stage] = run
            if run["exit_code"] != 0:
                result.update({
                    "status": "FAIL",
                    "run_integrity_status": "FAIL",
                    "failure_stage": stage,
                    "failure_reason": run["stderr_tail"] or run["stdout_tail"],
                })
                failed = True
                break

        if not failed:
            v551j_state, v552j_state, checks = _typed_functional_gate(entry)
            result["typed_stage_states"] = {"v551j": v551j_state, "v552j": v552j_state}
            result["functional_checks"] = checks
            integrity_pass = all(checks.values())
            evidence_operation_permitted = bool(v551j_state["operation_permitted"] and v552j_state["operation_permitted"])
            result["run_integrity_status"] = "PASS" if integrity_pass else "FAIL"
            result["evidence_operation_status"] = "PERMITTED" if evidence_operation_permitted else "NOT_PERMITTED"

            if not integrity_pass:
                result["status"] = "FAIL"
                result["failure_stage"] = "typed_integrity_gate"
                result["failure_reason"] = ",".join(name for name, passed in checks.items() if not passed)
                failed = True
            elif not evidence_operation_permitted:
                result["status"] = "NO_EVIDENCE_PERMISSION"
                result["failure_stage"] = "typed_evidence_permission_gate"
                blocked = []
                if not v551j_state["operation_permitted"]:
                    blocked.append(
                        "v551j:"
                        + v551j_state["evidence_status"]
                        + "/"
                        + v551j_state["downstream_permission_status"]
                    )
                if not v552j_state["operation_permitted"]:
                    blocked.append(
                        "v552j:"
                        + v552j_state["evidence_status"]
                        + "/"
                        + v552j_state["downstream_permission_status"]
                    )
                result["failure_reason"] = ",".join(blocked)
                failed = True
            else:
                result["status"] = "PASS"

        results.append(result)
        (reports / "bounded_nine_canary_partial_return.json").write_text(json.dumps({"preflight": preflight, "results": results}, indent=2) + "\n", encoding="utf-8")
        if failed and not args.continue_on_failure:
            break

    status = "PASS_BOUNDED_NINE_J_CHAIN" if len(results) == len(plan) and all(row.get("status") == "PASS" for row in results) else "FAIL_BOUNDED_NINE_J_CHAIN"
    final = {
        "status": status,
        "preflight": preflight,
        "attempted_scope_count": len(results),
        "planned_scope_count": len(plan),
        "passed_scope_count": sum(row.get("status") == "PASS" for row in results),
        "integrity_pass_scope_count": sum(row.get("run_integrity_status") == "PASS" for row in results),
        "results": results,
    }
    (reports / "BOUNDED_NINE_J_CHAIN_RETURN.json").write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")
    with (reports / "bounded_nine_j_chain_summary.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["source_family", "wave", "country_code", "scope_dir", "joint_configuration_id", "status", "run_integrity_status", "evidence_operation_status", "failure_stage", "failure_reason"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in results:
            writer.writerow({field: row.get(field, "") for field in fields})
    print(json.dumps(final, indent=2))
    return 0 if status.startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
