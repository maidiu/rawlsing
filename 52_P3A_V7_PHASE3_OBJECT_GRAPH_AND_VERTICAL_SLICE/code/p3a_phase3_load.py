from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import psycopg


RELEASE_ID = "P3-AUTHORITY-2026-08-01-R30-P3A-TEST"
SCHEMA = "p3a_v27_shadow"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def split_pipe(value: str) -> list[str]:
    return [part for part in value.split("|") if part and part != "UNBOUNDED"]


def boolish(value: str) -> bool:
    return value.strip().upper() in {"YES", "TRUE", "1"}


def execute_values(cur: psycopg.Cursor, sql: str, values: list[tuple]) -> None:
    for value in values:
        cur.execute(sql, value)


def load_contracts(root: Path, dsn: str) -> dict:
    sec = root / "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK"
    with psycopg.connect(dsn, autocommit=False) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public")
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO p3_authority_release
              (release_id,parent_release_id,schema_version,builder_version,input_manifest_hash,
               created_at,object_counts,validation_return_hash,migration_artifact,rollback_artifact)
            VALUES (%s,NULL,'p3-v7','p3a-phase3-loader-v30',%s,now(),%s,%s,%s,%s)
            ON CONFLICT (release_id) DO NOTHING
            """,
            (
                RELEASE_ID,
                sha256_file(sec / "upstream/P3_UPSTREAM_INPUT_MANIFEST_v7.csv"),
                json.dumps({}),
                "0" * 64,
                "52_P3A_V7_PHASE3_OBJECT_GRAPH_AND_VERTICAL_SLICE",
                "postgres/teardown_postgres_55432.sh",
            ),
        )

        vocab = rows(sec / "P3_CONTROLLED_VOCABULARIES_v7.csv")
        execute_values(
            cur,
            """
            INSERT INTO p3_vocabulary_code (vocabulary_domain,code,introduced_release_id,retired_release_id)
            VALUES (%s,%s,%s,NULL)
            ON CONFLICT (vocabulary_domain,code) DO NOTHING
            """,
            [(r["vocabulary_domain"], r["code"], RELEASE_ID) for r in vocab],
        )
        execute_values(
            cur,
            """
            INSERT INTO p3_vocabulary_revision
              (vocabulary_domain,code,authority_release_id,label,definition,authority_effect,deprecated)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (vocabulary_domain,code,authority_release_id) DO NOTHING
            """,
            [
                (
                    r["vocabulary_domain"],
                    r["code"],
                    RELEASE_ID,
                    r["label"] or r["code"],
                    r["definition"] or r["label"] or r["code"],
                    r.get("authority_effect") or None,
                    boolish(r.get("deprecated", "")),
                )
                for r in vocab
            ],
        )

        cat = rows(sec / "P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v7.csv")
        execute_values(
            cur,
            """
            INSERT INTO p3_categorical_field_binding
              (table_name,column_name,vocabulary_domain,authority_release_id)
            VALUES (%s,%s,%s,%s)
            ON CONFLICT DO NOTHING
            """,
            [(r["table_name"], r["column_name"], r["vocabulary_domain"], RELEASE_ID) for r in cat],
        )

        ident = rows(sec / "P3_IDENTITY_KEY_SPEC_v7.csv")
        execute_values(
            cur,
            """
            INSERT INTO p3_identity_key_contract
              (object_type,identity_strategy,id_pattern,idempotency_key_spec,authority_release_id)
            VALUES (%s,%s,%s,%s,%s)
            ON CONFLICT DO NOTHING
            """,
            [
                (
                    r["object_type"],
                    r["identity_strategy"],
                    r["id_pattern"],
                    r["idempotency_key"],
                    RELEASE_ID,
                )
                for r in ident
            ],
        )

        objref = rows(sec / "P3_OBJECT_REFERENCE_TYPE_CONTRACT_v7.csv")
        execute_values(
            cur,
            """
            INSERT INTO p3_object_reference_type_contract
              (table_name,column_name,allowed_object_types,authority_release_id)
            VALUES (%s,%s,%s,%s)
            ON CONFLICT DO NOTHING
            """,
            [
                (r["table_name"], r["column_name"], split_pipe(r["allowed_object_types"]), RELEASE_ID)
                for r in objref
            ],
        )

        hyper = rows(sec / "P3_HYPEREDGE_ROLE_TYPE_CONTRACT_v7.csv")
        execute_values(
            cur,
            """
            INSERT INTO p3_hyperedge_role_type_contract
              (hyperedge_type,participant_role,allowed_object_types,minimum_count,maximum_count,authority_effect_ceiling,authority_release_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT DO NOTHING
            """,
            [
                (
                    r["hyperedge_type"],
                    r["participant_role"],
                    split_pipe(r["allowed_object_types"]),
                    int(r["minimum_count"]),
                    None if r["maximum_count"] == "UNBOUNDED" else int(r["maximum_count"]),
                    r["authority_effect_ceiling"],
                    RELEASE_ID,
                )
                for r in hyper
            ],
        )

        cand_life = [r for r in rows(sec / "P3_LIFECYCLE_STATE_MACHINE_v7.csv") if boolish(r["allowed"])]
        execute_values(
            cur,
            """
            INSERT INTO p3_candidate_lifecycle_transition
              (from_stage,to_stage,guard_text,authority_release_id)
            VALUES (%s,%s,%s,%s)
            ON CONFLICT DO NOTHING
            """,
            [(r["from_stage"] or None, r["to_stage"], r["guard"], RELEASE_ID) for r in cand_life],
        )

        rel_life = [r for r in rows(sec / "P3_RELEASE_LIFECYCLE_STATE_MACHINE_v7.csv") if boolish(r["allowed"])]
        execute_values(
            cur,
            """
            INSERT INTO p3_release_lifecycle_transition
              (from_status,to_status,guard_text,authority_release_id)
            VALUES (%s,%s,%s,%s)
            ON CONFLICT DO NOTHING
            """,
            [(r["from_status"] or None, r["to_status"], r["guard"], RELEASE_ID) for r in rel_life],
        )
        conn.commit()

    return {
        "release_id": RELEASE_ID,
        "vocabulary_rows": len(vocab),
        "categorical_bindings": len(cat),
        "identity_contracts": len(ident),
        "object_reference_contracts": len(objref),
        "hyperedge_role_contracts": len(hyper),
        "candidate_lifecycle_transitions": len(cand_life),
        "release_lifecycle_transitions": len(rel_life),
    }


def load_imported_membership(root: Path, dsn: str) -> dict:
    lineage_path = root / "32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv"
    baseline_path = root / "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK/upstream/P3_LINEAGE_PARTICIPATION_BASELINE_v7.csv"
    lineages = rows(lineage_path)
    baseline = {r["lineage_id"]: r for r in rows(baseline_path)}
    object_rows = []
    upstream_rows = []
    membership_rows = []
    participation_rows = []
    disposition_rows = []
    seen_impl = set()
    for row in lineages:
        lineage_id = row["lineage_id"]
        source_family = row.get("source_family") or row.get("source") or ""
        object_rows.append((lineage_id, "IMPORTED_SOURCE_LOCAL_LINEAGE", "INHERITED_UPSTREAM_ID", f"lineage:{lineage_id}", "P2_GLOBAL", lineage_id, RELEASE_ID, None, None, "Inherited exact P2 source-local lineage ID."))
        upstream_rows.append((lineage_id, "P2_GLOBAL", source_family, "DELIVERED_HANDOFF", "SOURCE_LOCAL_LINEAGE", lineage_id, lineage_path.relative_to(root).as_posix(), sha256_file(lineage_path), "P2_SOURCE_LOCAL_LINEAGE_REGISTRY"))
        members = json.loads(row["member_question_implementation_ids_json"])
        for ordinal, impl_id in enumerate(members):
            if impl_id not in seen_impl:
                seen_impl.add(impl_id)
                object_rows.append((impl_id, "IMPORTED_IMPLEMENTATION", "INHERITED_UPSTREAM_ID", f"implementation:{impl_id}", "P2_GLOBAL", impl_id, RELEASE_ID, None, None, "Inherited exact P2 question implementation ID."))
                upstream_rows.append((impl_id, "P2_GLOBAL", source_family, "DELIVERED_HANDOFF", "QUESTION_IMPLEMENTATION", impl_id, lineage_path.relative_to(root).as_posix(), sha256_file(lineage_path), "P2_SOURCE_LOCAL_LINEAGE_REGISTRY"))
            membership_rows.append((lineage_id, impl_id, ordinal, lineage_id, RELEASE_ID))
        b = baseline[lineage_id]
        participation_rows.append((lineage_id, b["participation_status"], int(b["effective_pair_incident_count"]), int(b["proposition_pair_incident_count"]), b["signature_requirement"], b["authority_note"] or None, RELEASE_ID))
        status = "CONSTRAINT_ONLY_PRESERVED" if b["participation_status"] == "CONSTRAINT_ONLY_INCIDENT" else "UNADJUDICATED"
        reason = "Initial P3A lineage state from corrected participation baseline."
        disposition_rows.append((lineage_id, status, reason, None, json.dumps([lineage_id]), RELEASE_ID))

    with psycopg.connect(dsn, autocommit=False) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public")
        cur = conn.cursor()
        execute_values(cur, """INSERT INTO p3_object_registry (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,allocation_release_id,retired_release_id,content_hash,stable_identity_note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (object_id) DO NOTHING""", object_rows)
        execute_values(cur, """INSERT INTO p3_upstream_object_reference (object_id,upstream_phase,source_family,license_provenance_state,upstream_object_type,upstream_object_id,authority_artifact,authority_hash,license_provenance_ref) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", upstream_rows)
        execute_values(cur, """INSERT INTO p3_imported_lineage_membership (lineage_id,implementation_id,ordinal_position,source_authority_id,authority_release_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", membership_rows)
        execute_values(cur, """INSERT INTO p3_lineage_participation (lineage_id,participation_status,effective_pair_incident_count,proposition_pair_incident_count,signature_requirement,authority_note,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", participation_rows)
        execute_values(cur, """INSERT INTO p3_lineage_disposition (subject_id,disposition_status,reason,canonical_family_id,evidence_ids,authority_release_id) VALUES (%s,%s,%s,%s,%s::jsonb,%s) ON CONFLICT DO NOTHING""", disposition_rows)
        conn.commit()
    return {
        "lineage_objects": len(lineages),
        "implementation_objects": len(seen_impl),
        "membership_rows": len(membership_rows),
        "participation_rows": len(participation_rows),
        "disposition_rows": len(disposition_rows),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--dsn", required=True)
    ap.add_argument("--phase", required=True, choices=["contracts", "membership"])
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    if args.phase == "contracts":
        result = load_contracts(root, args.dsn)
    else:
        result = load_imported_membership(root, args.dsn)
    result["status"] = "PASS"
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
