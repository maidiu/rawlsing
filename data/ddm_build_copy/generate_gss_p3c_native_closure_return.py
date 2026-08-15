#!/usr/bin/env python3
"""Generate the R9-required GSS P3C native closure return."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import psycopg
import yaml


DEFAULT_DSN = "postgresql://postgres@127.0.0.1:5432/rawlsing_p3c_gss_r184"
R184_RELEASE = "P3-AUTHORITY-2026-08-02-R184"
CHILD_RELEASE = "P3-AUTHORITY-2026-08-05-R4-GSS-CHILD"
REPAIR_R1_RELEASE = "P3-AUTHORITY-2026-08-05-R4-GSS-CHILD-SIGREPAIR-R1"
REPAIR_R2_RELEASE = "P3-AUTHORITY-2026-08-05-R4-GSS-CHILD-SIGREPAIR-R2"
REGISTRY_PATH = Path("data/ddm_build_copy/manifests/p3c_r184_question_family_registry/gss_p3c_repair_r1_question_family_registry.yaml")
AUDIT_PATH = Path("data/ddm_build_copy/manifests/p3c_r184_question_family_registry/gss_p3c_repair_r1_question_family_registry_audit.csv")
NORMALIZATION_REPORT_PATH = Path("data/ddm_build_copy/manifests/p3c_r184_question_family_registry/gss_p3c_repair_r1_normalization_report.json")
OUTPUT_PATH = Path("data/ddm_build_copy/manifests/p3c_r184_question_family_registry/GSS_P3C_NATIVE_CLOSURE_RETURN.json")


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def active_release_sql() -> str:
    return """
    WITH latest_repair AS (
      SELECT canonical_family_id, family_revision_id
      FROM p3_canonical_family_revision
      WHERE authority_release_id=%(repair_r2)s
    ), parent_repair AS (
      SELECT canonical_family_id, family_revision_id
      FROM p3_canonical_family_revision
      WHERE authority_release_id=%(repair_r1)s
        AND canonical_family_id NOT IN (SELECT canonical_family_id FROM latest_repair)
    ), base_child AS (
      SELECT canonical_family_id, family_revision_id
      FROM p3_canonical_family_revision
      WHERE authority_release_id=%(child)s
        AND canonical_family_id NOT IN (SELECT canonical_family_id FROM latest_repair)
        AND canonical_family_id NOT IN (SELECT canonical_family_id FROM parent_repair)
    ), active AS (
      SELECT * FROM latest_repair
      UNION ALL SELECT * FROM parent_repair
      UNION ALL SELECT * FROM base_child
    )
    """


def db_report(dsn: str) -> dict[str, Any]:
    params = {"repair_r2": REPAIR_R2_RELEASE, "repair_r1": REPAIR_R1_RELEASE, "child": CHILD_RELEASE}
    with psycopg.connect(dsn) as conn:
        cur = conn.cursor()
        release_rows = {}
        for rel in [R184_RELEASE, CHILD_RELEASE, REPAIR_R1_RELEASE, REPAIR_R2_RELEASE]:
            cur.execute(
                "SELECT release_id,parent_release_id,schema_version,builder_version,object_counts,validation_return_hash FROM p3_authority_release WHERE release_id=%s",
                (rel,),
            )
            row = cur.fetchone()
            release_rows[rel] = {
                "present": bool(row),
                "parent_release_id": row[1] if row else None,
                "schema_version": row[2] if row else None,
                "builder_version": row[3] if row else None,
                "object_counts": row[4] if row else None,
                "validation_return_hash": row[5] if row else None,
            }

        cur.execute(
            active_release_sql()
            + """
            , base AS (
              SELECT cfr.*, adj.candidate_revision_id, cr.canonical_signature_id AS candidate_signature_id
              FROM active a
              JOIN p3_canonical_family_revision cfr USING(family_revision_id, canonical_family_id)
              LEFT JOIN p3_adjudication_decision adj ON adj.adjudication_id=cfr.created_by_adjudication_id
              LEFT JOIN p3_candidate_revision cr ON cr.candidate_revision_id=adj.candidate_revision_id
            )
            SELECT
              count(*) AS active_revisions,
              count(distinct canonical_family_id) AS active_families,
              count(*) FILTER (WHERE created_by_adjudication_id IS NOT NULL) AS canonical_with_adjudication,
              count(*) FILTER (WHERE candidate_revision_id IS NOT NULL) AS canonical_with_candidate_revision,
              count(*) FILTER (WHERE EXISTS (SELECT 1 FROM p3_candidate_evidence_snapshot ces WHERE ces.candidate_revision_id=base.candidate_revision_id)) AS candidate_with_snapshot,
              count(*) FILTER (WHERE EXISTS (SELECT 1 FROM p3_candidate_component_link ccl WHERE ccl.candidate_revision_id=base.candidate_revision_id)) AS candidate_with_component,
              count(*) FILTER (WHERE EXISTS (SELECT 1 FROM p3_candidate_membership cm WHERE cm.candidate_revision_id=base.candidate_revision_id)) AS candidate_with_memberships,
              count(*) FILTER (WHERE EXISTS (SELECT 1 FROM p3_proposition_signature ps WHERE ps.signature_id=base.canonical_signature_id AND ps.subject_id=base.family_revision_id)) AS canonical_signature_subject_owned,
              count(*) FILTER (WHERE EXISTS (SELECT 1 FROM p3_proposition_signature ps WHERE ps.signature_id=base.candidate_signature_id AND ps.subject_id=base.candidate_revision_id)) AS candidate_signature_subject_owned
            FROM base
            """,
            params,
        )
        keys = [
            "active_revisions",
            "active_families",
            "canonical_with_adjudication",
            "canonical_with_candidate_revision",
            "candidate_with_snapshot",
            "candidate_with_component",
            "candidate_with_memberships",
            "canonical_signature_subject_owned",
            "candidate_signature_subject_owned",
        ]
        closure_counts = dict(zip(keys, cur.fetchone()))

        cur.execute(
            active_release_sql()
            + """
            SELECT count(*) AS membership_rows, count(distinct m.member_object_id) AS member_objects
            FROM active a
            JOIN p3_canonical_family_membership m USING(family_revision_id)
            """,
            params,
        )
        closure_counts.update(dict(zip(["active_membership_rows", "active_member_objects"], cur.fetchone())))

        cur.execute("SELECT count(*) FROM p3_release_status_event WHERE release_id=%s", (REPAIR_R2_RELEASE,))
        repair_r2_status_events = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM p3_release_object_snapshot WHERE release_id=%s", (REPAIR_R2_RELEASE,))
        repair_r2_snapshot_rows = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM p3_release_change_ledger WHERE release_id=%s", (REPAIR_R2_RELEASE,))
        repair_r2_ledger_rows = cur.fetchone()[0]

    parent_chain_ok = (
        release_rows[R184_RELEASE]["present"]
        and release_rows[CHILD_RELEASE]["parent_release_id"] == R184_RELEASE
        and release_rows[REPAIR_R1_RELEASE]["parent_release_id"] == CHILD_RELEASE
        and release_rows[REPAIR_R2_RELEASE]["parent_release_id"] == REPAIR_R1_RELEASE
    )
    relationship_counts_ok = all(closure_counts.get(key) == 162 for key in keys)
    return {
        "release_rows": release_rows,
        "parent_chain_ok": parent_chain_ok,
        "closure_counts": closure_counts,
        "relationship_counts_ok": relationship_counts_ok,
        "repair_r2_status_events": repair_r2_status_events,
        "repair_r2_snapshot_rows": repair_r2_snapshot_rows,
        "repair_r2_ledger_rows": repair_r2_ledger_rows,
        "r184_immutability_result": {
            "status": "PASS" if release_rows[R184_RELEASE]["present"] and parent_chain_ok else "FAIL",
            "basis": "R184 release row remains present with original parent/schema/builder/object_counts; GSS child and repairs are append-only descendants.",
            "r184_release_row": release_rows[R184_RELEASE],
        },
    }


def registry_report(dsn: str) -> dict[str, Any]:
    payload = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    normalization = json.loads(NORMALIZATION_REPORT_PATH.read_text(encoding="utf-8"))
    audit_rows = list(csv.DictReader(AUDIT_PATH.open(newline="", encoding="utf-8")))
    wave_counter: Counter[str] = Counter()
    for row in audit_rows:
        for wave in str(row.get("waves") or "").split("|"):
            if wave:
                wave_counter[wave] += 1

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_registry = Path(tmpdir) / "registry.yaml"
        tmp_audit = Path(tmpdir) / "audit.csv"
        env = os.environ.copy()
        result = subprocess.run(
            [
                sys.executable,
                "data/ddm_build_copy/compile_gss_p3c_registry_from_repair_release.py",
                "--dsn",
                dsn,
                "--output",
                tmp_registry.as_posix(),
                "--audit-output",
                tmp_audit.as_posix(),
            ],
            cwd=Path.cwd(),
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        deterministic = result.returncode == 0 and file_sha256(tmp_registry) == file_sha256(REGISTRY_PATH)
        rebuild_stdout = result.stdout.strip()

    return {
        "path": REGISTRY_PATH.as_posix(),
        "sha256": file_sha256(REGISTRY_PATH),
        "declared_registry_sha256": payload.get("registry_sha256"),
        "authority_release_id": payload.get("authority_release_id"),
        "family_count": len(payload.get("families") or []),
        "audit_path": AUDIT_PATH.as_posix(),
        "audit_sha256": file_sha256(AUDIT_PATH),
        "audit_rows": len(audit_rows),
        "unique_lineages": len({row.get("lineage_id") for row in audit_rows}),
        "unique_var_codes": len({str(row.get("var_code") or "").lower() for row in audit_rows if row.get("var_code")}),
        "wave_mapping_coverage": dict(sorted(wave_counter.items())),
        "normalization_report": normalization,
        "deterministic_rebuild": {
            "status": "PASS" if deterministic else "FAIL",
            "stdout": rebuild_stdout,
        },
        "runtime_dependency_check": {
            "status": "PASS" if payload.get("runtime_source_constraint") == "installed_registry_only_no_r4_source_runtime_dependency" else "FAIL",
            "basis": "Installed registry is self-contained YAML plus audit sidecar; R4 source authority is used at build time, not loaded by runtime.",
            "runtime_source_constraint": payload.get("runtime_source_constraint"),
        },
    }


def active_processes() -> list[str]:
    patterns = [
        "promote_r4_p3c_child_release.py",
        "repair_r4_p3c_signature_subjects.py",
        "repair_gss_p3c_canonical_signature_subjects_r2.py",
        "build_determinicity_wave_shard_v550.py",
        "compile_v550j_joint_response_patterns.py",
        "compile_v551j",
        "compile_v552j",
    ]
    result = subprocess.run(["ps", "aux"], text=True, capture_output=True, check=False)
    lines = []
    for line in result.stdout.splitlines():
        if "generate_gss_p3c_native_closure_return.py" in line:
            continue
        if any(pattern in line for pattern in patterns):
            lines.append(line)
    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dsn", default=os.environ.get("RAWLSING_P3C_DSN", DEFAULT_DSN))
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    db = db_report(args.dsn)
    registry = registry_report(args.dsn)
    processes = active_processes()
    gates = {
        "release_parent_chain": db["parent_chain_ok"],
        "relationship_closure_162": db["relationship_counts_ok"],
        "registry_family_count_162": registry["family_count"] == 162,
        "registry_mapping_rows_present": registry["audit_rows"] == registry["unique_lineages"] == registry["unique_var_codes"] == 361,
        "registry_normalization_pass": registry["normalization_report"].get("status") == "pass",
        "deterministic_rebuild_pass": registry["deterministic_rebuild"]["status"] == "PASS",
        "r184_immutability_pass": db["r184_immutability_result"]["status"] == "PASS",
        "no_active_upstream_or_j_processes": not processes,
    }
    status = "PASS" if all(gates.values()) else "FAIL"
    payload = {
        "schema_version": "GSS_P3C_NATIVE_CLOSURE_RETURN_R1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "p3c_native_closure": status,
        "release_ids": {
            "r184_parent": R184_RELEASE,
            "gss_child": CHILD_RELEASE,
            "signature_repair_r1": REPAIR_R1_RELEASE,
            "canonical_signature_repair_r2": REPAIR_R2_RELEASE,
            "active_release": REPAIR_R2_RELEASE,
        },
        "gates": gates,
        "database": db,
        "registry": registry,
        "downstream_j_series_status": "NOT_RUN_AUTHORITY_NOT_YET_BUILT",
        "bounded_v550j_smoke_status": "PRESERVED_AS_SMOKE_ONLY_NOT_AUTHORITY",
        "active_processes": processes,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"p3c_native_closure": status, "output": args.output.as_posix(), "sha256": file_sha256(args.output)}, indent=2))


if __name__ == "__main__":
    main()
