#!/usr/bin/env python3
"""Verify the repaired GSS P3C registry matches governed non-GSS registry form."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import yaml


REQUIRED_ITEM_KEYS = {"var_code", "condition_label", "p3_member_object_id", "representative_text"}
DEFAULT_REGISTRY_DIR = Path("data/ddm_build_copy/manifests/p3c_r184_question_family_registry")
DEFAULT_GSS_REGISTRY = DEFAULT_REGISTRY_DIR / "gss_p3c_repair_r1_question_family_registry.yaml"
DEFAULT_GSS_AUDIT = DEFAULT_REGISTRY_DIR / "gss_p3c_repair_r1_question_family_registry_audit.csv"
DEFAULT_REPORT = DEFAULT_REGISTRY_DIR / "gss_p3c_repair_r1_normalization_report.json"


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def registry_shape(path: Path) -> dict[str, Any]:
    payload = load_yaml(path)
    families = payload.get("families") or []
    roles = set()
    item_keys = set()
    missing_required: list[dict[str, str]] = []
    families_missing_items: list[str] = []
    item_count = 0
    for family in families:
        groups = family.get("item_role_groups") or {}
        if not groups.get("canonical_member"):
            families_missing_items.append(str(family.get("family_id")))
        for role, rows in groups.items():
            roles.add(str(role))
            for row in rows or []:
                item_count += 1
                item_keys.update(row.keys())
                for key in REQUIRED_ITEM_KEYS:
                    if not str(row.get(key) or "").strip():
                        missing_required.append(
                            {
                                "family_id": str(family.get("family_id")),
                                "p3_member_object_id": str(row.get("p3_member_object_id") or ""),
                                "missing_key": key,
                            }
                        )
    return {
        "path": path.as_posix(),
        "registry_version": payload.get("registry_version"),
        "source_family": payload.get("source_family"),
        "status": payload.get("status"),
        "authority_release_id": payload.get("authority_release_id"),
        "family_count": len(families),
        "declared_family_count": payload.get("family_count"),
        "item_count": item_count,
        "roles": sorted(roles),
        "item_keys": sorted(item_keys),
        "families_missing_items": families_missing_items,
        "items_missing_required_fields": missing_required,
    }


def audit_summary(path: Path) -> dict[str, Any]:
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    missing = []
    for row in rows:
        for key in ["family_id", "family_revision_id", "p3_signature_id", "r4_component_id", "lineage_id", "var_code", "var_code_resolution_basis"]:
            if not str(row.get(key) or "").strip():
                missing.append({"lineage_id": row.get("lineage_id", ""), "missing_key": key})
    return {
        "path": path.as_posix(),
        "rows": len(rows),
        "unique_families": len({row.get("family_id") for row in rows}),
        "unique_lineages": len({row.get("lineage_id") for row in rows}),
        "unique_var_codes": len({str(row.get("var_code") or "").lower() for row in rows if row.get("var_code")}),
        "missing_required_fields": missing,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry-dir", type=Path, default=DEFAULT_REGISTRY_DIR)
    parser.add_argument("--gss-registry", type=Path, default=DEFAULT_GSS_REGISTRY)
    parser.add_argument("--gss-audit", type=Path, default=DEFAULT_GSS_AUDIT)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    gss_shape = registry_shape(args.gss_registry)
    non_gss_paths = sorted(
        path for path in args.registry_dir.glob("*_p3c_r184_question_family_registry.yaml")
        if path.name != args.gss_registry.name
    )
    non_gss_shapes = [registry_shape(path) for path in non_gss_paths]
    non_gss_roles = sorted({tuple(shape["roles"]) for shape in non_gss_shapes})
    non_gss_item_keys = sorted({tuple(shape["item_keys"]) for shape in non_gss_shapes})
    gss_audit = audit_summary(args.gss_audit)

    report = {
        "status": "pass",
        "gss": gss_shape,
        "gss_audit": gss_audit,
        "non_gss": non_gss_shapes,
        "parity": {
            "non_gss_registry_count": len(non_gss_shapes),
            "gss_roles_match_non_gss": tuple(gss_shape["roles"]) in non_gss_roles,
            "gss_item_keys_match_non_gss": tuple(gss_shape["item_keys"]) in non_gss_item_keys,
            "expected_role": "canonical_member",
            "expected_item_keys": sorted(REQUIRED_ITEM_KEYS),
        },
    }
    failures = []
    if gss_shape["family_count"] != 162 or gss_shape["declared_family_count"] != 162:
        failures.append("gss_family_count_not_162")
    if gss_shape["status"] != "governed":
        failures.append("gss_registry_not_governed")
    if gss_shape["roles"] != ["canonical_member"]:
        failures.append("gss_role_contract_mismatch")
    if set(gss_shape["item_keys"]) != REQUIRED_ITEM_KEYS:
        failures.append("gss_item_key_contract_mismatch")
    if gss_shape["families_missing_items"]:
        failures.append("gss_families_missing_items")
    if gss_shape["items_missing_required_fields"]:
        failures.append("gss_items_missing_required_fields")
    if gss_audit["rows"] != gss_shape["item_count"]:
        failures.append("gss_audit_row_count_mismatch")
    if gss_audit["missing_required_fields"]:
        failures.append("gss_audit_missing_required_fields")
    if not report["parity"]["gss_roles_match_non_gss"] or not report["parity"]["gss_item_keys_match_non_gss"]:
        failures.append("gss_non_gss_shape_parity_failed")
    if failures:
        report["status"] = "fail"
        report["failures"] = failures

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"status": report["status"], "output": args.output.as_posix(), "failures": failures}, indent=2))


if __name__ == "__main__":
    main()
