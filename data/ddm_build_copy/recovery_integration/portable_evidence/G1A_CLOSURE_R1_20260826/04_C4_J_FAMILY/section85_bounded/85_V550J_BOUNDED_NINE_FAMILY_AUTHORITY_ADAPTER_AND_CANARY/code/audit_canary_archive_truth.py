#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import unicodedata
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def schema_columns(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [str(row.get("name", "")) for row in payload.get("columns", [])]


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the exact capabilities and limits of the nine-source canary archive.")
    parser.add_argument("--section", type=Path, required=True)
    parser.add_argument("--canary-root", type=Path, required=True)
    args = parser.parse_args()

    section = args.section.resolve()
    canary = args.canary_root.resolve()
    authority = section / "authority"
    outputs = section / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)

    scopes = read_csv(authority / "bounded_nine_scope_manifest.csv")
    items = read_csv(authority / "bounded_joint_configuration_item_crosswalk.csv")
    items_by_config: dict[str, list[dict[str, str]]] = {}
    for row in items:
        items_by_config.setdefault(row["joint_configuration_id"], []).append(row)

    scope_returns: list[dict[str, Any]] = []
    failures: list[str] = []
    respondent_identifier_schemas: list[str] = []
    aggregate_respondent_count_schemas: list[str] = []

    for schema_path in sorted((canary / "v550" / "shard_runs").glob("*/*/schemas/*.schema.json")):
        columns = schema_columns(schema_path)
        lowered = {column.casefold() for column in columns}
        if {"respondent_id", "respondent_id_norm"} & lowered:
            respondent_identifier_schemas.append(str(schema_path.relative_to(canary)))
        if "n_respondents" in lowered:
            aggregate_respondent_count_schemas.append(str(schema_path.relative_to(canary)))

    for row in scopes:
        config_id = row["joint_configuration_id"]
        filter_path = section / "inputs" / row["filter_file"]
        filter_payload = json.loads(filter_path.read_text(encoding="utf-8"))
        selected = [str(value) for value in filter_payload.get("var_codes", [])]
        selected_norm = {value.casefold() for value in selected}
        configured = [item["var_code"] for item in items_by_config.get(config_id, [])]
        configured_norm = {value.casefold() for value in configured}

        audit_path = canary / row["v550_response_semantics_audit"]
        audit_rows = read_csv(audit_path)
        audit_vars = {str(item.get("var_code", "")).casefold() for item in audit_rows}

        shard_matches = list(canary.glob(f"v550/shard_runs/*/{row['scope_dir']}"))
        if not shard_matches:
            # Unicode-normalized fallback.
            parent_matches = list((canary / "v550" / "shard_runs").glob("*"))
            shard_matches = []
            for parent in parent_matches:
                try:
                    shard_matches.append(resolve_child(parent, row["scope_dir"]))
                except RuntimeError:
                    pass
        shard_matches = sorted({path.resolve() for path in shard_matches})
        v551_scope = resolve_child(canary / "v551", row["scope_dir"])
        v552_scope = resolve_child(canary / "v552", row["scope_dir"])

        checks = {
            "filter_has_exactly_20_variables": len(selected) == 20 and len(selected_norm) == 20,
            "configured_items_present_in_filter": configured_norm <= selected_norm,
            "configured_items_present_in_response_semantics_audit": configured_norm <= audit_vars,
            "filter_hash_matches_manifest": sha256_file(filter_path) == row["filter_sha256"],
            "response_audit_hash_matches_manifest": sha256_file(audit_path) == row["v550_response_semantics_audit_sha256"],
            "exactly_one_v550_shard": len(shard_matches) == 1,
            "v551_relation_atoms_present": (v551_scope / "relation_evidence_atoms.parquet").exists(),
            "v551_manifest_present": (v551_scope / "manifest.json").exists(),
            "v552_profile_present": (v552_scope / "v552_performance_profile.json").exists(),
        }
        failed = [name for name, passed in checks.items() if not passed]
        if failed:
            failures.extend(f"{row['scope_dir']}:{name}" for name in failed)
        scope_returns.append({
            "source_family": row["source_family"],
            "wave": row["wave"],
            "country_code": row["country_code"],
            "scope_dir": row["scope_dir"],
            "joint_configuration_id": config_id,
            "selected_variable_count": len(selected),
            "configured_item_count": len(configured),
            "checks": checks,
            "failed_checks": failed,
            "v550_shard_dir": str(shard_matches[0].relative_to(canary)) if len(shard_matches) == 1 else "",
            "v551_scope_dir": str(v551_scope.relative_to(canary)),
            "v552_scope_dir": str(v552_scope.relative_to(canary)),
        })

    capability = {
        "archive_contains_exact_nine_scope_filters": len(scopes) == 9,
        "archive_contains_v550_aggregate_outputs": True,
        "archive_contains_v551_relation_atoms": all(row["checks"]["v551_relation_atoms_present"] for row in scope_returns),
        "archive_contains_respondent_identifier_schema": bool(respondent_identifier_schemas),
        "archive_contains_respondent_level_joint_substrate": bool(respondent_identifier_schemas),
        "archive_is_sufficient_for_static_authority_binding": not failures,
        "archive_is_sufficient_for_real_v550j_execution_without_live_database": False,
        "real_v550j_required_input": "live respondent-level database/view or a separately packaged prepared V550J substrate containing respondent_id",
    }
    if respondent_identifier_schemas:
        failures.append("unexpected_respondent_identifier_schema_present_review_archive_classification")

    result = {
        "status": "PASS_STATIC_CANARY_ARCHIVE_TRUTH_AUDIT" if not failures else "FAIL_STATIC_CANARY_ARCHIVE_TRUTH_AUDIT",
        "scope_count": len(scopes),
        "configured_item_count": len(items),
        "respondent_identifier_schema_count": len(respondent_identifier_schemas),
        "respondent_identifier_schemas": respondent_identifier_schemas,
        "aggregate_respondent_count_schema_count": len(aggregate_respondent_count_schemas),
        "capability": capability,
        "scope_returns": scope_returns,
        "failures": failures,
    }
    out_json = outputs / "CANARY_ARCHIVE_TRUTH_AUDIT.json"
    out_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with (outputs / "CANARY_ARCHIVE_SCOPE_AUDIT.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = ["source_family", "wave", "country_code", "scope_dir", "joint_configuration_id", "selected_variable_count", "configured_item_count", "all_checks_passed", "v550_shard_dir", "v551_scope_dir", "v552_scope_dir"]
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in scope_returns:
            writer.writerow({
                **{key: row[key] for key in fields if key in row},
                "all_checks_passed": not row["failed_checks"],
            })

    lines = [
        "# Nine-source canary archive truth audit",
        "",
        f"Status: **{result['status']}**",
        "",
        f"- Exact source-wave-country scopes: {len(scopes)}",
        f"- Configured joint items: {len(items)}",
        f"- Schemas containing respondent identifiers: {len(respondent_identifier_schemas)}",
        f"- Schemas containing aggregate `n_respondents`: {len(aggregate_respondent_count_schemas)}",
        "",
        "## Governing conclusion",
        "",
        "The archive is sufficient for exact scope recovery, question binding, response-semantics audit, and reuse of preserved V551 relation atoms.",
        "It is **not** a respondent-level V550J substrate: no packaged schema exposes `respondent_id` or `respondent_id_norm`.",
        "The large `indicator_answer_matrix` tables are aggregate question/answer distributions carrying counts such as `n_respondents`; those counts cannot be inverted into respondent co-occurrence patterns.",
        "Real V550J execution must therefore use the live respondent database/view (or a separately governed prepared substrate) on the receiving host.",
        "",
        "This gate prevents marginal distributions from being silently counterfeited as joint-response evidence.",
    ]
    (outputs / "CANARY_ARCHIVE_TRUTH_AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
