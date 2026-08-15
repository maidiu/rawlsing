#!/usr/bin/env python3
"""Compile executable GSS P3C registry YAML from the repaired child release."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import psycopg
import yaml


DEFAULT_DSN = "postgresql://postgres@127.0.0.1:5432/rawlsing_p3c_gss_r184"
DEFAULT_OUTPUT = Path(
    "data/ddm_build_copy/manifests/p3c_r184_question_family_registry/"
    "gss_p3c_repair_r1_question_family_registry.yaml"
)
DEFAULT_AUDIT_OUTPUT = Path(
    "data/ddm_build_copy/manifests/p3c_r184_question_family_registry/"
    "gss_p3c_repair_r1_question_family_registry_audit.csv"
)
DEFAULT_LINEAGE_AUTHORITY = Path(
    "Rawlsing_GSS_P3C_Joint_Authority_Codex_Ready_Cumulative_R4/"
    "Rawlsing_GSS_P3C_Joint_Authority_WORKING_HANDOFF_R4/"
    "10_GSS_P3C_FULL_SEMANTIC_AUTHORITY/GSS_FULL_LINEAGE_SEMANTIC_AUTHORITY_R1.csv"
)
REPAIR_RELEASE = "P3-AUTHORITY-2026-08-05-R4-GSS-CHILD-SIGREPAIR-R2"
PARENT_REPAIR_RELEASE = "P3-AUTHORITY-2026-08-05-R4-GSS-CHILD-SIGREPAIR-R1"
DEFECTIVE_CHILD = "P3-AUTHORITY-2026-08-05-R4-GSS-CHILD"


def load_lineage_authority(path: Path) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    with path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            lineage_id = str(row.get("lineage_id") or "").strip()
            if not lineage_id:
                continue
            variables: list[str] = []
            try:
                variables = [str(value).strip() for value in json.loads(row.get("variables") or "[]") if str(value).strip()]
            except json.JSONDecodeError:
                variables = []
            try:
                waves = [str(value).strip() for value in json.loads(row.get("waves") or "[]") if str(value).strip()]
            except json.JSONDecodeError:
                waves = []
            primary = str(row.get("primary_variable") or "").strip()
            if primary and primary not in variables:
                variables.insert(0, primary)
            lookup[lineage_id] = {
                "primary_variable": primary,
                "variables": variables,
                "representative_text": str(row.get("text") or row.get("normalized_proposition_text") or "").strip(),
                "waves": waves,
                "classification_confidence": str(row.get("classification_confidence") or "").strip(),
                "classification_method": str(row.get("classification_method") or "").strip(),
                "classification_basis": str(row.get("classification_basis") or "").strip(),
            }
    return lookup


def resolve_var_codes(lineage_lookup: dict[str, dict[str, Any]], members: list[str]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    audit_rows: list[dict[str, str]] = []
    for member in members:
        authority = lineage_lookup.get(member, {})
        variables = authority.get("variables") or []
        for var_code in variables:
            rows.append(
                {
                    "var_code": str(var_code),
                    "condition_label": member,
                    "p3_member_object_id": member,
                    "representative_text": str(authority.get("representative_text") or ""),
                }
            )
            audit_rows.append(
                {
                    "lineage_id": member,
                    "var_code": str(var_code),
                    "representative_text": str(authority.get("representative_text") or ""),
                    "var_code_resolution_basis": "GSS_FULL_LINEAGE_SEMANTIC_AUTHORITY_R1.variables",
                    "classification_confidence": str(authority.get("classification_confidence") or ""),
                    "classification_method": str(authority.get("classification_method") or ""),
                    "classification_basis": str(authority.get("classification_basis") or ""),
                    "waves": "|".join(authority.get("waves") or []),
                }
            )
    return rows, audit_rows


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def compile_registry(dsn: str, output_path: Path, lineage_authority_path: Path, audit_output_path: Path) -> dict[str, Any]:
    lineage_lookup = load_lineage_authority(lineage_authority_path)
    with psycopg.connect(dsn) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            WITH latest_repair AS (
              SELECT canonical_family_id, family_revision_id
              FROM p3_canonical_family_revision
              WHERE authority_release_id=%s
            ), parent_repair AS (
              SELECT canonical_family_id, family_revision_id
              FROM p3_canonical_family_revision
              WHERE authority_release_id=%s
                AND canonical_family_id NOT IN (SELECT canonical_family_id FROM latest_repair)
            ), base_child AS (
              SELECT canonical_family_id, family_revision_id
              FROM p3_canonical_family_revision
              WHERE authority_release_id=%s
                AND canonical_family_id NOT IN (SELECT canonical_family_id FROM latest_repair)
                AND canonical_family_id NOT IN (SELECT canonical_family_id FROM parent_repair)
            ), active_revisions AS (
              SELECT * FROM latest_repair
              UNION ALL
              SELECT * FROM parent_repair
              UNION ALL
              SELECT * FROM base_child
            )
            SELECT ar.canonical_family_id,
                   ar.family_revision_id,
                   r.canonical_signature_id,
                   r.canonical_proposition,
                   s.content_hash,
                   coalesce(ces.canonical_payload->>'component_id', es.canonical_payload->>'component_id', r.canonical_proposition->>'component_id') as component_id,
                   array_agg(m.member_object_id order by m.member_object_id) as members
            FROM active_revisions ar
            JOIN p3_canonical_family_revision r USING(family_revision_id, canonical_family_id)
            JOIN p3_proposition_signature s ON s.signature_id=r.canonical_signature_id
            JOIN p3_canonical_family_membership m USING(family_revision_id)
            LEFT JOIN p3_adjudication_decision adj
              ON adj.adjudication_id=r.created_by_adjudication_id
            LEFT JOIN p3_candidate_evidence_snapshot ces
              ON ces.candidate_revision_id=adj.candidate_revision_id
            LEFT JOIN p3_candidate_evidence_snapshot es
              ON es.canonical_payload->>'canonical_family_revision_id'=ar.family_revision_id
            GROUP BY ar.canonical_family_id, ar.family_revision_id, r.canonical_signature_id,
                     r.canonical_proposition, s.content_hash, component_id
            ORDER BY ar.canonical_family_id, ar.family_revision_id
            """,
            (REPAIR_RELEASE, PARENT_REPAIR_RELEASE, DEFECTIVE_CHILD),
        )
        rows = cur.fetchall()
        if len(rows) != 162:
            raise ValueError(f"expected 162 active GSS families, found {len(rows)}")

        families = []
        audit_rows: list[dict[str, str]] = []
        for family_id, revision_id, signature_id, proposition, signature_hash, component_id, members in rows:
            identity = proposition if isinstance(proposition, dict) else {}
            genealogy = identity.get("genealogy") if isinstance(identity.get("genealogy"), dict) else {}
            family_label = (
                identity.get("canonical_label")
                or identity.get("family_label")
                or identity.get("target")
                or component_id
                or family_id
            )
            member_rows, family_audit_rows = resolve_var_codes(lineage_lookup, list(members or []))
            for audit_row in family_audit_rows:
                audit_row.update(
                    {
                        "family_id": str(family_id),
                        "family_revision_id": str(revision_id),
                        "p3_signature_id": str(signature_id),
                        "r4_component_id": str(component_id or genealogy.get("source_component_id") or ""),
                    }
                )
            audit_rows.extend(family_audit_rows)
            families.append(
                {
                    "family_id": family_id,
                    "family_revision_id": revision_id,
                    "family_label": str(family_label),
                    "family_type": "p3c_canonical_question_family",
                    "family_structure_type": "SOURCE_NATIVE_PROPOSITION",
                    "eligible_waves": [],
                    "item_role_groups": {"canonical_member": member_rows},
                    "response_role_rules": {
                        "operator": identity.get("operator"),
                        "response_portability_status": "NOT_AUTHORIZED_BY_P3",
                    },
                    "target_resolution_rules": {
                        "subject": identity.get("subject"),
                        "target": identity.get("target"),
                    },
                    "boundary_rules": {
                        "axis": identity.get("axis"),
                        "conditional_scope": identity.get("conditional_scope"),
                        "temporal_scope": identity.get("temporal_scope"),
                    },
                    "p3_signature_id": signature_id,
                    "p3_signature_content_hash": signature_hash,
                    "r4_component_id": component_id or genealogy.get("source_component_id"),
                    "r4_semantic_signature_sha256": identity.get("semantic_signature_sha256"),
                }
            )

    payload = {
        "registry_version": "gss_p3c_repair_r1_executable",
        "source_family": "GSS",
        "status": "governed",
        "authority_release": REPAIR_RELEASE,
        "authority_release_id": REPAIR_RELEASE,
        "parent_release": DEFECTIVE_CHILD,
        "repair_parent_release": PARENT_REPAIR_RELEASE,
        "authority_source": "P3C append-only signature-subject repair release",
        "lineage_authority_source": lineage_authority_path.as_posix(),
        "runtime_source_constraint": "installed_registry_only_no_r4_source_runtime_dependency",
        "family_count": len(families),
        "families": families,
    }
    payload["registry_sha256"] = digest(payload)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")
    audit_output_path.parent.mkdir(parents=True, exist_ok=True)
    audit_fields = [
        "family_id",
        "family_revision_id",
        "p3_signature_id",
        "r4_component_id",
        "lineage_id",
        "var_code",
        "representative_text",
        "var_code_resolution_basis",
        "classification_confidence",
        "classification_method",
        "classification_basis",
        "waves",
    ]
    with audit_output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=audit_fields)
        writer.writeheader()
        writer.writerows(audit_rows)
    return {
        "output_path": output_path.as_posix(),
        "audit_output_path": audit_output_path.as_posix(),
        "family_count": len(families),
        "registry_sha256": payload["registry_sha256"],
        "audit_rows": len(audit_rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dsn", default=os.environ.get("RAWLSING_P3C_DSN", DEFAULT_DSN))
    parser.add_argument("--lineage-authority", type=Path, default=DEFAULT_LINEAGE_AUTHORITY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--audit-output", type=Path, default=DEFAULT_AUDIT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(compile_registry(args.dsn, args.output, args.lineage_authority, args.audit_output), indent=2))


if __name__ == "__main__":
    main()
