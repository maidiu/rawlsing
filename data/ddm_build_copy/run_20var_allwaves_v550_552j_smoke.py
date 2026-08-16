#!/usr/bin/env python3
"""Governed orchestration shim for the preserved all-wave smoke implementation.

The implementation module is the integration-baseline smoke byte-for-byte.
This shim changes only W05-owned orchestration policy:
* all-wave scope is derived from CLOSED_35_WAVES authority;
* joint execution defaults to applicability-scoped ``auto``;
* absent joint authority is reported as NOT_APPLICABLE or coverage debt.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Iterable

from data.ddm_build_copy import run_20var_allwaves_v550_552j_smoke_impl as _impl
from data.ddm_build_copy.ddm_pipeline_boundary_contract import load_closed_35_waves
from data.ddm_build_copy.ddm_v550_question_relation_authority import DEFAULT_AUTHORITY_PATH

for _name in dir(_impl):
    if _name.startswith("__"):
        continue
    globals()[_name] = getattr(_impl, _name)

_ORIGINAL_RESOLVE_JOINT = _impl.resolve_joint_authority
_ORIGINAL_SUMMARIZE_JOINT = _impl.summarize_joint_authority_coverage
_ORIGINAL_PARSE_ARGS = _impl.parse_args
_ORIGINAL_RUN_WAVE = _impl.run_wave
_ORIGINAL_WRITE_SUMMARIES = _impl.write_summaries

ALL_WAVES: list[tuple[str, str, str]] = list(load_closed_35_waves(DEFAULT_AUTHORITY_PATH))
_impl.ALL_WAVES = ALL_WAVES
RuntimeConfig = _impl.RuntimeConfig
DEFAULT_CONFIG = RuntimeConfig(joint_mode="auto")
_impl.DEFAULT_CONFIG = DEFAULT_CONFIG


def validate_explicit_scope(waves: Iterable[tuple[str, str, str]] = ALL_WAVES) -> list[str]:
    rows = list(waves)
    governed = list(load_closed_35_waves(DEFAULT_AUTHORITY_PATH))
    governed_pairs = {(family, wave) for family, wave, _ in governed}
    pairs = [(family, wave) for family, wave, _ in rows]
    issues: list[str] = []
    if len(set(pairs)) != len(pairs):
        issues.append("duplicate_family_wave_in_governed_scope")
    outside = sorted(set(pairs) - governed_pairs)
    if outside:
        issues.append("scope_outside_CLOSED_35_WAVES:" + ",".join(f"{f}|{w}" for f, w in outside))
    if len(rows) == len(governed) and set(pairs) != governed_pairs:
        missing = sorted(governed_pairs - set(pairs))
        issues.append("governed_scope_mismatch:" + ",".join(f"{f}|{w}" for f, w in missing))
    if len(rows) > len(governed):
        issues.append(f"governed_scope_count_exceeds_35:{len(rows)}")
    if ("Asian Barometer", "W6") in set(pairs):
        issues.append("asian_barometer_w6_present_in_CLOSED_35_WAVES")
    return issues


def _joint_coverage_state(authority: dict[str, Any]) -> str:
    if authority.get("applicable"):
        return "PRESENT"
    reason = str(authority.get("reason") or "")
    if reason in {"no_explicit_joint_registry_for_family_wave", "joint_registry_exists_but_selected_slice_has_no_family_items"}:
        return "NOT_APPLICABLE"
    return "APPLICABLE_UNRESOLVED"


def resolve_joint_authority(config: RuntimeConfig, family: str, wave: str, selected_vars: Iterable[str] | None = None) -> dict[str, Any]:
    authority = dict(_ORIGINAL_RESOLVE_JOINT(config, family, wave, selected_vars))
    authority["coverage_state"] = _joint_coverage_state(authority)
    authority["downstream_permission_status"] = "ALLOW" if authority.get("applicable") else "NOT_APPLICABLE" if authority["coverage_state"] == "NOT_APPLICABLE" else "DENY"
    return authority


def summarize_joint_authority_coverage(config: RuntimeConfig, waves: Iterable[tuple[str, str, str]] = ALL_WAVES) -> dict[str, Any]:
    rows = list(waves)
    report = dict(_ORIGINAL_SUMMARIZE_JOINT(config, rows))
    typed_rows: list[dict[str, Any]] = []
    not_applicable: list[dict[str, Any]] = []
    coverage_debt: list[dict[str, Any]] = []
    applicable: list[dict[str, Any]] = []
    for family, wave, country in rows:
        authority = resolve_joint_authority(config, family, wave)
        row = {"source": family, "wave": wave, "country_code": country, "coverage_state": authority["coverage_state"], "downstream_permission_status": authority["downstream_permission_status"], "reason": authority.get("reason", ""), "registry_path": authority.get("registry_path", "")}
        typed_rows.append(row)
        if authority.get("applicable"):
            applicable.append(row)
        elif authority["coverage_state"] == "NOT_APPLICABLE":
            not_applicable.append(row)
        else:
            coverage_debt.append(row)
    report.update(typed_scopes=typed_rows, applicable_scopes=applicable, not_applicable_scopes=not_applicable, coverage_debt_scopes=coverage_debt, applicable_scope_count=len(applicable), not_applicable_scope_count=len(not_applicable), coverage_debt_scope_count=len(coverage_debt))
    return report


def parse_args():
    args = _ORIGINAL_PARSE_ARGS()
    if "--joint-mode" not in sys.argv:
        args.joint_mode = "auto"
    return args


def run_wave(family: str, wave: str, country: str, run_ts: str, output_root: str, filter_path: str, selected_vars: list[str], config: RuntimeConfig | None = None) -> dict[str, Any]:
    result = _ORIGINAL_RUN_WAVE(family, wave, country, run_ts, output_root, filter_path, selected_vars, DEFAULT_CONFIG if config is None else config)
    branch = result.setdefault("joint_branch", {})
    authority = branch.get("authority")
    if isinstance(authority, dict):
        authority = dict(authority)
        authority["coverage_state"] = _joint_coverage_state(authority)
        authority["downstream_permission_status"] = "ALLOW" if authority.get("applicable") else "NOT_APPLICABLE" if authority["coverage_state"] == "NOT_APPLICABLE" else "DENY"
        branch["authority"] = authority
    return result


def write_summaries(results: list[dict[str, Any]], output_root: str, run_ts: str, canary_only: bool, preflight: dict[str, Any] | None = None) -> None:
    _ORIGINAL_WRITE_SUMMARIES(results, output_root, run_ts, canary_only, preflight)
    report_dir = Path(output_root) / "reports"
    total = len(results)
    passed = sum(bool(row.get("passed")) for row in results)
    base_passed = sum(bool(row.get("base_spine_passed")) for row in results)
    applicable = sum(bool((row.get("joint_branch") or {}).get("authority", {}).get("applicable")) for row in results)
    joint_passed = sum((row.get("joint_branch") or {}).get("status") == "passed" for row in results)
    lines = ["# Universality Functional Smoke Report", "", f"**Run:** {run_ts}", f"**Scope:** {'canary only' if canary_only else 'authority-derived CLOSED_35_WAVES'}", "**Base spine:** V550 → V551 → V552", "**Joint branch:** V550J → V551J → V552J only where executable governed family authority applies", "", "## Summary", "", f"- Waves attempted: {total}", f"- Base spines passed: {base_passed}", f"- Joint-applicable scopes: {applicable}", f"- Joint-applicable chains passed: {joint_passed}", f"- Waves passed at the applicability-scoped acceptance boundary: {passed}", "", "| Source | Wave | Country | Base | Joint coverage | Joint status | Passed | Failure |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for row in results:
        branch = row.get("joint_branch") or {}
        authority = branch.get("authority") or {}
        lines.append("| {source} | {wave} | {country} | {base} | {coverage} | {joint} | {passed} | {failure} |".format(source=row.get("survey_family", ""), wave=row.get("wave_id", ""), country=row.get("country", ""), base="PASS" if row.get("base_spine_passed") else "FAIL", coverage=authority.get("coverage_state", "UNKNOWN"), joint=branch.get("status", "not-run"), passed="PASS" if row.get("passed") else "FAIL", failure=row.get("functional_failure_reason", "")))
    lines.extend(["", "## Readiness", ""])
    if total and passed == total and joint_passed == applicable:
        lines.append("**READY at the applicability-scoped boundary.** Every attempted base scope passed, and every joint-applicable scope passed its J-chain.")
    else:
        lines.append(f"**NOT READY.** {passed}/{total} scopes passed; {joint_passed}/{applicable} applicable J-chains passed.")
    (report_dir / "smoke_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


_impl.validate_explicit_scope = validate_explicit_scope
_impl.resolve_joint_authority = resolve_joint_authority
_impl.summarize_joint_authority_coverage = summarize_joint_authority_coverage
_impl.parse_args = parse_args
_impl.run_wave = run_wave
_impl.write_summaries = write_summaries

globals().update(ALL_WAVES=ALL_WAVES, RuntimeConfig=RuntimeConfig, DEFAULT_CONFIG=DEFAULT_CONFIG, validate_explicit_scope=validate_explicit_scope, resolve_joint_authority=resolve_joint_authority, summarize_joint_authority_coverage=summarize_joint_authority_coverage, parse_args=parse_args, run_wave=run_wave, write_summaries=write_summaries)


def main() -> int:
    return _impl.main()


if __name__ == "__main__":
    raise SystemExit(main())
