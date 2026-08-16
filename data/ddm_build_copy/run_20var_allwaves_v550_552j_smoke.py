#!/usr/bin/env python3
"""Governed orchestration shim for the preserved all-wave smoke implementation.

W05-A fixed the governed 35-wave scope and joint applicability policy. W05-B
adds the merged V551 v3.0 consumer boundary while deliberately stopping before
unmerged V551J/V552/V552J producer contracts.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from data.ddm_build_copy import run_20var_allwaves_v550_552j_smoke_impl as _impl
from data.ddm_build_copy.ddm_pipeline_boundary_consumer import verify_v551_v3_producer_manifest
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError, load_closed_35_waves
from data.ddm_build_copy.ddm_v550_question_relation_authority import DEFAULT_AUTHORITY_PATH

for _name in dir(_impl):
    if _name.startswith("__"):
        continue
    globals()[_name] = getattr(_impl, _name)

_ORIGINAL_RESOLVE_JOINT = _impl.resolve_joint_authority
_ORIGINAL_SUMMARIZE_JOINT = _impl.summarize_joint_authority_coverage
_ORIGINAL_PARSE_ARGS = _impl.parse_args
_ORIGINAL_WRITE_SUMMARIES = _impl.write_summaries

ALL_WAVES: list[tuple[str, str, str]] = list(load_closed_35_waves(DEFAULT_AUTHORITY_PATH))
_impl.ALL_WAVES = ALL_WAVES
RuntimeConfig = _impl.RuntimeConfig
DEFAULT_CONFIG = RuntimeConfig(joint_mode="auto")
_impl.DEFAULT_CONFIG = DEFAULT_CONFIG


def validate_explicit_scope(
    waves: Iterable[tuple[str, str, str]] = ALL_WAVES,
) -> list[str]:
    rows = list(waves)
    governed = list(load_closed_35_waves(DEFAULT_AUTHORITY_PATH))
    governed_pairs = {(family, wave) for family, wave, _ in governed}
    pairs = [(family, wave) for family, wave, _ in rows]
    issues: list[str] = []
    if len(set(pairs)) != len(pairs):
        issues.append("duplicate_family_wave_in_governed_scope")
    outside = sorted(set(pairs) - governed_pairs)
    if outside:
        issues.append(
            "scope_outside_CLOSED_35_WAVES:" + ",".join(f"{family}|{wave}" for family, wave in outside)
        )
    if len(rows) == len(governed) and set(pairs) != governed_pairs:
        missing = sorted(governed_pairs - set(pairs))
        issues.append(
            "governed_scope_mismatch:" + ",".join(f"{family}|{wave}" for family, wave in missing)
        )
    if len(rows) > len(governed):
        issues.append(f"governed_scope_count_exceeds_35:{len(rows)}")
    if ("Asian Barometer", "W6") in set(pairs):
        issues.append("asian_barometer_w6_present_in_CLOSED_35_WAVES")
    return issues


def _joint_coverage_state(authority: dict[str, Any]) -> str:
    if authority.get("applicable"):
        return "PRESENT"
    reason = str(authority.get("reason") or "")
    if reason in {
        "no_explicit_joint_registry_for_family_wave",
        "joint_registry_exists_but_selected_slice_has_no_family_items",
    }:
        return "NOT_APPLICABLE"
    return "APPLICABLE_UNRESOLVED"


def resolve_joint_authority(
    config: RuntimeConfig,
    family: str,
    wave: str,
    selected_vars: Iterable[str] | None = None,
) -> dict[str, Any]:
    authority = dict(_ORIGINAL_RESOLVE_JOINT(config, family, wave, selected_vars))
    authority["coverage_state"] = _joint_coverage_state(authority)
    authority["downstream_permission_status"] = (
        "ALLOW"
        if authority.get("applicable")
        else "NOT_APPLICABLE"
        if authority["coverage_state"] == "NOT_APPLICABLE"
        else "DENY"
    )
    return authority


def summarize_joint_authority_coverage(
    config: RuntimeConfig,
    waves: Iterable[tuple[str, str, str]] = ALL_WAVES,
) -> dict[str, Any]:
    rows = list(waves)
    report = dict(_ORIGINAL_SUMMARIZE_JOINT(config, rows))
    typed_rows: list[dict[str, Any]] = []
    not_applicable: list[dict[str, Any]] = []
    coverage_debt: list[dict[str, Any]] = []
    applicable: list[dict[str, Any]] = []
    for family, wave, country in rows:
        authority = resolve_joint_authority(config, family, wave)
        row = {
            "source": family,
            "wave": wave,
            "country_code": country,
            "coverage_state": authority["coverage_state"],
            "downstream_permission_status": authority["downstream_permission_status"],
            "reason": authority.get("reason", ""),
            "registry_path": authority.get("registry_path", ""),
        }
        typed_rows.append(row)
        if authority.get("applicable"):
            applicable.append(row)
        elif authority["coverage_state"] == "NOT_APPLICABLE":
            not_applicable.append(row)
        else:
            coverage_debt.append(row)
    report.update(
        typed_scopes=typed_rows,
        applicable_scopes=applicable,
        not_applicable_scopes=not_applicable,
        coverage_debt_scopes=coverage_debt,
        applicable_scope_count=len(applicable),
        not_applicable_scope_count=len(not_applicable),
        coverage_debt_scope_count=len(coverage_debt),
    )
    return report


def parse_args():
    args = _ORIGINAL_PARSE_ARGS()
    if "--joint-mode" not in sys.argv:
        args.joint_mode = "auto"
    return args


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "null"} else text


def _bridge_run_id(bridge_path: str | Path) -> str:
    bridge = pd.read_parquet(bridge_path)
    if "run_id" not in bridge.columns:
        raise BoundaryContractError("V551_BRIDGE_RUN_ID_MISSING")
    run_ids = sorted({_clean(value) for value in bridge["run_id"].tolist() if _clean(value)})
    if len(run_ids) != 1:
        raise BoundaryContractError(f"V551_BRIDGE_RUN_ID_NOT_SINGULAR:{run_ids}")
    return run_ids[0]


def run_v551(
    shard_id: str,
    bridge_path: str,
    quc_path: str,
    response_map_path: str,
    output_root: str,
    config: RuntimeConfig = DEFAULT_CONFIG,
) -> dict[str, Any]:
    """Invoke the merged V551 v3 CLI while preserving the legacy wrapper ABI."""
    del shard_id, quc_path, response_map_path
    producer_run_id = _bridge_run_id(bridge_path)
    cmd = [
        sys.executable,
        _impl._abs("data/ddm_build_copy/compile_v551_relation_evidence_atoms.py", config),
        "--run-id",
        producer_run_id,
        "--bridge-path",
        bridge_path,
        "--output-root",
        output_root,
        "--v551-compile-mode",
        "canonical",
    ]
    result = _impl._invoke_run(cmd, timeout_sec=1800, config=config)
    result["producer_run_id"] = producer_run_id
    return result


def summarize_v551_functional_gate(
    path: str | Path,
    *,
    run_id: str,
    source: str,
    wave: str,
    country_code: str = "",
    shard_id: str = "",
) -> dict[str, Any]:
    manifest_path = Path(path)
    try:
        verified = verify_v551_v3_producer_manifest(
            manifest_path,
            run_id=run_id,
            source=source,
            wave=wave,
            country_code=country_code,
            shard_id=shard_id,
        )
    except BoundaryContractError as exc:
        return {
            "manifest_path": str(manifest_path),
            "manifest_exists": manifest_path.exists(),
            "passed": False,
            "integrity_passed": False,
            "downstream_permitted": False,
            "terminal_not_applicable": False,
            "failure_reason": f"v551_boundary_invalid:{exc}",
        }
    state = verified.state
    payload = verified.manifest_payload
    artifacts = {
        Path(item.path).name: {
            "row_count": item.row_count,
            "artifact_file_sha256": item.artifact_file_sha256,
            "valid_empty": item.valid_empty,
        }
        for item in verified.verified_artifacts
    }
    atom_rows = int(payload.get("atom_count") or 0)
    return {
        "manifest_path": str(manifest_path),
        "manifest_exists": True,
        "contract_version": state.contract_version,
        "schema_version": str(payload.get("schema_version") or ""),
        "compiler_version": str(payload.get("compiler_version") or ""),
        "run_integrity_status": state.run_integrity_status,
        "evidence_status": state.evidence_status,
        "downstream_permission_status": state.downstream_permission_status,
        "v551_evidence_detail": str(payload.get("v551_evidence_detail") or ""),
        "candidate_count": int(payload.get("candidate_count") or 0),
        "promotable_candidate_count": int(payload.get("promotable_candidate_count") or 0),
        "nonpromotable_candidate_count": int(payload.get("nonpromotable_candidate_count") or 0),
        "atom_rows": atom_rows,
        "distribution_coverage_rows": int(payload.get("distribution_coverage_rows") or 0),
        "artifacts": artifacts,
        # 'passed' is producer-integrity smoke, not downstream sufficiency.
        "passed": True,
        "integrity_passed": True,
        "downstream_permitted": state.downstream_permission_status == "ALLOW",
        "terminal_not_applicable": state.downstream_permission_status == "NOT_APPLICABLE",
        "failure_reason": "",
    }


def _pending_downstream(result: dict[str, Any], *, v551_gate: dict[str, Any]) -> dict[str, Any]:
    result["cross_stage_status"] = "PARTIAL_AWAITING_CROSS_HOOK"
    result["functional_checks"]["v552"] = {
        "status": "PARTIAL_AWAITING_CROSS_HOOK",
        "reason": "W02-B typed V552 producer/consumer hook is not merged at the G2 base",
        "v551_evidence_status": v551_gate.get("evidence_status", ""),
        "v551_downstream_permission_status": v551_gate.get("downstream_permission_status", ""),
    }
    result["acceptance_boundary"] = "v551_v3_verified_pending_v552_hook"
    result["passed"] = False
    return result


def run_wave(
    family: str,
    wave: str,
    country: str,
    run_ts: str,
    output_root: str,
    filter_path: str,
    selected_vars: list[str],
    config: RuntimeConfig = DEFAULT_CONFIG,
) -> dict[str, Any]:
    """Run through the real V551 v3 boundary; stop before unmerged V552 hooks."""
    run_id = f"{_impl._family_wave_id(family, wave)}_{run_ts}"
    shard_id = f"{family}_{wave}" + (f"_{country}" if country else "")
    result: dict[str, Any] = {
        "survey_family": family,
        "wave_id": wave,
        "country": country,
        "run_id": run_id,
        "selected_variable_count": len(selected_vars),
        "selected_variables": selected_vars,
        "stages": {},
        "functional_checks": {},
        "joint_branch": {},
        "base_spine_passed": False,
        "full_chain_passed": False,
        "acceptance_boundary": "none",
        "passed": False,
    }

    _impl._log(f"WAVE {family} {wave} ({country}) — {len(selected_vars)} variables")
    shard_dir = Path(output_root) / "v550" / "shard_runs" / run_id / shard_id
    authority = resolve_joint_authority(config, family, wave, selected_vars)
    result["joint_branch"]["authority"] = authority

    registry_path_for_v550 = (
        authority["registry_path"]
        if authority.get("applicable") and config.joint_mode != "off"
        else None
    )
    raw = _impl.run_v550_shard(
        run_id,
        shard_id,
        family,
        wave,
        country,
        filter_path,
        str(Path(output_root) / "v550"),
        registry_path_for_v550,
        config,
    )
    if raw["exit_code"] != 0:
        result["stages"]["v550"] = _impl._stage_result(raw)
        return _impl._fail(result, "v550_process", raw.get("stderr_tail") or "v550_nonzero_exit")
    v550_gate = _impl.summarize_v550_manifest_gate(shard_dir / "manifest.json")
    result["stages"]["v550"] = _impl._stage_result(raw, v550_gate)
    result["functional_checks"]["v550_manifest"] = v550_gate
    if not v550_gate["passed"]:
        return _impl._fail(result, "v550_manifest_gate", v550_gate["failure_reason"])

    quc_gate = _impl.summarize_quc_functional_gate(shard_dir / "core/question_use_contract.parquet")
    result["functional_checks"]["v550_quc"] = quc_gate
    if not quc_gate["passed"]:
        return _impl._fail(result, "v550_quc_gate", quc_gate["failure_reason"])

    response_map_path = shard_dir / "core/response_option_map.parquet"
    if not response_map_path.exists():
        return _impl._fail(
            result,
            "v550_response_semantics_contract",
            "missing_scoped_response_option_map_artifact",
        )

    bridge_path = shard_dir / "bridge/v551_bridge_index.parquet"
    quc_path = shard_dir / "core/question_use_contract.parquet"
    v551_root = Path(output_root) / "v551"
    try:
        producer_run_id = _bridge_run_id(bridge_path)
    except Exception as exc:
        return _impl._fail(result, "v551_bridge_identity", f"{type(exc).__name__}:{exc}")
    if producer_run_id != run_id:
        return _impl._fail(
            result,
            "v551_bridge_identity",
            f"v551_bridge_run_id_mismatch:expected={run_id}:actual={producer_run_id}",
        )

    raw = run_v551(
        shard_id,
        str(bridge_path),
        str(quc_path),
        str(response_map_path),
        str(v551_root),
        config,
    )
    if raw["exit_code"] != 0:
        result["stages"]["v551"] = _impl._stage_result(raw)
        return _impl._fail(result, "v551_process", raw.get("stderr_tail") or "v551_nonzero_exit")
    v551_run_root = v551_root / producer_run_id
    v551_gate = summarize_v551_functional_gate(
        v551_run_root / "manifest.json",
        run_id=producer_run_id,
        source=family,
        wave=wave,
        country_code=country,
        shard_id=shard_id,
    )
    result["stages"]["v551"] = _impl._stage_result(raw, v551_gate)
    result["functional_checks"]["v551"] = v551_gate
    if not v551_gate["passed"]:
        return _impl._fail(result, "v551_gate", v551_gate["failure_reason"])

    if v551_gate["downstream_permission_status"] == "DENY":
        return _impl._fail(
            result,
            "v551_downstream_permission_gate",
            "v551_downstream_denied:" + str(v551_gate.get("evidence_status") or "UNKNOWN"),
        )

    # At G2 the V552 producer hook is still owned by W02-B.  Passing old V552
    # path/row-count gates would reintroduce exactly the stale contract this
    # repair is removing, so stop explicitly rather than guessing its manifest.
    result["joint_branch"]["status"] = "pending_downstream_cross_hook"
    result["joint_branch"]["reason"] = "V552/V551J/V552J typed producer hooks not yet merged"
    return _pending_downstream(result, v551_gate=v551_gate)


def write_summaries(
    results: list[dict[str, Any]],
    output_root: str,
    run_ts: str,
    canary_only: bool,
    preflight: dict[str, Any] | None = None,
) -> None:
    _ORIGINAL_WRITE_SUMMARIES(results, output_root, run_ts, canary_only, preflight)
    report_dir = Path(output_root) / "reports"
    total = len(results)
    completed = sum(bool(row.get("passed")) for row in results)
    partial = sum(row.get("cross_stage_status") == "PARTIAL_AWAITING_CROSS_HOOK" for row in results)
    v551_integrity = sum(bool((row.get("functional_checks") or {}).get("v551", {}).get("integrity_passed")) for row in results)
    lines = [
        "# Universality Functional Smoke Report",
        "",
        f"**Run:** {run_ts}",
        f"**Scope:** {'canary only' if canary_only else 'authority-derived CLOSED_35_WAVES'}",
        "**Current verified boundary:** V550 → V551 v3.0",
        "**Later stages:** explicitly pending merged V552/V551J/V552J typed producer hooks",
        "",
        "## Summary",
        "",
        f"- Waves attempted: {total}",
        f"- V551 producer-integrity boundaries passed: {v551_integrity}",
        f"- Partial awaiting cross-stage producer hooks: {partial}",
        f"- Full acceptance passes: {completed}",
        "",
        "| Source | Wave | Country | V551 integrity | V551 evidence | V551 permission | Cross-stage | Passed | Failure |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in results:
        v551 = (row.get("functional_checks") or {}).get("v551", {})
        lines.append(
            "| {source} | {wave} | {country} | {integrity} | {evidence} | {permission} | {cross} | {passed} | {failure} |".format(
                source=row.get("survey_family", ""),
                wave=row.get("wave_id", ""),
                country=row.get("country", ""),
                integrity=v551.get("run_integrity_status", "not-run"),
                evidence=v551.get("evidence_status", "not-run"),
                permission=v551.get("downstream_permission_status", "not-run"),
                cross=row.get("cross_stage_status", ""),
                passed="PASS" if row.get("passed") else "NO",
                failure=row.get("functional_failure_reason", ""),
            )
        )
    lines.extend(["", "## Readiness", ""])
    if partial:
        lines.append(
            "**PARTIAL_AWAITING_CROSS_HOOK.** V551 v3.0 is verified without atom-count readiness shortcuts; full smoke closure waits for the actual V552/V551J/V552J producer contracts."
        )
    elif total and completed == total:
        lines.append("**READY.** Every attempted scope passed the currently installed typed contracts.")
    else:
        lines.append(f"**NOT READY.** {completed}/{total} attempted scopes passed.")
    (report_dir / "smoke_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


_impl.validate_explicit_scope = validate_explicit_scope
_impl.resolve_joint_authority = resolve_joint_authority
_impl.summarize_joint_authority_coverage = summarize_joint_authority_coverage
_impl.parse_args = parse_args
_impl.run_v551 = run_v551
_impl.summarize_v551_functional_gate = summarize_v551_functional_gate
_impl.run_wave = run_wave
_impl.write_summaries = write_summaries

globals().update(
    ALL_WAVES=ALL_WAVES,
    RuntimeConfig=RuntimeConfig,
    DEFAULT_CONFIG=DEFAULT_CONFIG,
    validate_explicit_scope=validate_explicit_scope,
    resolve_joint_authority=resolve_joint_authority,
    summarize_joint_authority_coverage=summarize_joint_authority_coverage,
    parse_args=parse_args,
    run_v551=run_v551,
    summarize_v551_functional_gate=summarize_v551_functional_gate,
    run_wave=run_wave,
    write_summaries=write_summaries,
)


def main() -> int:
    return _impl.main()


if __name__ == "__main__":
    raise SystemExit(main())
