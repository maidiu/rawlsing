#!/usr/bin/env python3
"""Append-only R2 repair for GSS P3C canonical signature subject ownership."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from typing import Any

import psycopg


DEFAULT_DSN = "postgresql://postgres@127.0.0.1:5432/rawlsing_p3c_gss_r184"
PARENT_RELEASE = "P3-AUTHORITY-2026-08-05-R4-GSS-CHILD-SIGREPAIR-R1"
BASE_CHILD_RELEASE = "P3-AUTHORITY-2026-08-05-R4-GSS-CHILD"
REPAIR_RELEASE = "P3-AUTHORITY-2026-08-05-R4-GSS-CHILD-SIGREPAIR-R2"
BUILDER_VERSION = "r4-p3c-canonical-signature-subject-repair-v2"
SIGNATURE_SCHEMA_VERSION = "p3-canonical-proposition-signature-subject-owned-v2"

SIGNATURE_FIELD_MAP = {
    "subject": "subject_role",
    "target": "target",
    "operator": "operator",
    "temporal_scope": "timeframe",
    "conditional_scope": "condition",
    "proposition_grain": "modality",
    "axis": "object_or_outcome",
}
SIGNATURE_FIELDS = [
    "subject_role",
    "target",
    "operator",
    "timeframe",
    "condition",
    "modality",
    "object_or_outcome",
    "parent_context",
    "polarity",
    "geographic_scope",
    "derived_status",
]


def stable(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(stable(value).encode("utf-8")).hexdigest()


def canonical_revision_id(canonical_family_id: str, revision_number: int) -> str:
    return f"JFAMREV-{canonical_family_id.split('-', 1)[1]}-R{revision_number:04d}"


def adjudication_id(ordinal: int) -> str:
    return f"P3ADJ-{ordinal:06d}"


def signature_hash(semantic_signature_sha256: str, subject_id: str) -> str:
    return hashlib.sha256(
        "\x1f".join([SIGNATURE_SCHEMA_VERSION, semantic_signature_sha256, "CANONICAL_FAMILY_REVISION", subject_id]).encode("utf-8")
    ).hexdigest()


def signature_fields(signature_id: str, proposition: dict[str, Any]) -> list[tuple[Any, ...]]:
    identity = proposition.get("semantic_identity") if isinstance(proposition.get("semantic_identity"), dict) else proposition
    mapped = {SIGNATURE_FIELD_MAP[k]: str(v) for k, v in identity.items() if k in SIGNATURE_FIELD_MAP}
    mapped.setdefault("derived_status", "R4_GSS_P3C_CANONICAL_SIGNATURE_SUBJECT_REPAIR_R2")
    rows = []
    for field in SIGNATURE_FIELDS:
        value = mapped.get(field)
        if value is None:
            rows.append((signature_id, field, None, None, "NOT_APPLICABLE", "NOT_APPLICABLE"))
        else:
            rows.append((signature_id, field, value, value, "KNOWN", "HIGH"))
    return rows


def object_row(object_id: str, object_type: str, content_hash: str | None = None) -> tuple[Any, ...]:
    return (
        object_id,
        object_type,
        "CONTENT_ADDRESSED_DERIVED_ID" if object_type == "PROPOSITION_SIGNATURE" else "REGISTRY_ALLOCATED_DURABLE_ID",
        object_id,
        "R4_GSS_P3C_CANONICAL_SIGNATURE_SUBJECT_REPAIR_R2",
        REPAIR_RELEASE,
        REPAIR_RELEASE,
        None,
        content_hash,
        "Allocated by append-only GSS P3C canonical signature subject repair R2.",
    )


def copy_release_contracts(cur: psycopg.Cursor[Any]) -> None:
    cur.execute(
        """
        INSERT INTO p3_identity_key_contract
          (object_type,identity_strategy,id_pattern,idempotency_key_spec,authority_release_id)
        SELECT DISTINCT ON (object_type,identity_strategy,id_pattern,idempotency_key_spec)
          object_type,identity_strategy,id_pattern,idempotency_key_spec,%s
        FROM p3_identity_key_contract
        ORDER BY object_type,identity_strategy,id_pattern,idempotency_key_spec,authority_release_id DESC
        ON CONFLICT DO NOTHING
        """,
        (REPAIR_RELEASE,),
    )
    cur.execute(
        """
        INSERT INTO p3_object_reference_type_contract
          (table_name,column_name,allowed_object_types,authority_release_id)
        SELECT DISTINCT ON (table_name,column_name)
          table_name,column_name,allowed_object_types,%s
        FROM p3_object_reference_type_contract
        ORDER BY table_name,column_name,authority_release_id DESC
        ON CONFLICT DO NOTHING
        """,
        (REPAIR_RELEASE,),
    )
    cur.execute(
        """
        INSERT INTO p3_vocabulary_code
          (vocabulary_domain,code,introduced_release_id,retired_release_id)
        SELECT vocabulary_domain,code,%s,NULL
        FROM p3_vocabulary_code
        ON CONFLICT DO NOTHING
        """,
        (REPAIR_RELEASE,),
    )
    cur.execute(
        """
        INSERT INTO p3_vocabulary_revision
          (vocabulary_domain,code,authority_release_id,label,definition,authority_effect,deprecated)
        SELECT DISTINCT ON (vocabulary_domain,code)
          vocabulary_domain,code,%s,label,definition,authority_effect,deprecated
        FROM p3_vocabulary_revision
        ORDER BY vocabulary_domain,code,authority_release_id DESC
        ON CONFLICT DO NOTHING
        """,
        (REPAIR_RELEASE,),
    )
    cur.execute(
        """
        INSERT INTO p3_release_lifecycle_transition
          (from_status,to_status,guard_text,authority_release_id)
        SELECT DISTINCT ON (from_status,to_status)
          from_status,to_status,guard_text,%s
        FROM p3_release_lifecycle_transition
        ORDER BY from_status,to_status,authority_release_id DESC
        ON CONFLICT DO NOTHING
        """,
        (REPAIR_RELEASE,),
    )


def active_mismatches(cur: psycopg.Cursor[Any]) -> list[dict[str, Any]]:
    cur.execute(
        """
        WITH latest_repair AS (
          SELECT canonical_family_id, family_revision_id
          FROM p3_canonical_family_revision
          WHERE authority_release_id=%s
        ), latest_parent AS (
          SELECT canonical_family_id, family_revision_id
          FROM p3_canonical_family_revision
          WHERE authority_release_id=%s
            AND canonical_family_id NOT IN (SELECT canonical_family_id FROM latest_repair)
        ), base_child AS (
          SELECT canonical_family_id, family_revision_id
          FROM p3_canonical_family_revision
          WHERE authority_release_id=%s
            AND canonical_family_id NOT IN (SELECT canonical_family_id FROM latest_repair)
            AND canonical_family_id NOT IN (SELECT canonical_family_id FROM latest_parent)
        ), active AS (
          SELECT * FROM latest_repair
          UNION ALL
          SELECT * FROM latest_parent
          UNION ALL
          SELECT * FROM base_child
        )
        SELECT cfr.canonical_family_id,
               cfr.family_revision_id,
               cfr.revision_number,
               cfr.canonical_signature_id,
               cfr.canonical_proposition,
               cfr.evidence_bundle_hash,
               cfr.created_by_adjudication_id,
               adj.candidate_revision_id,
               adj.response_portability_status,
               adj.rationale,
               ps.subject_id
        FROM active a
        JOIN p3_canonical_family_revision cfr USING(family_revision_id, canonical_family_id)
        JOIN p3_adjudication_decision adj ON adj.adjudication_id=cfr.created_by_adjudication_id
        JOIN p3_proposition_signature ps ON ps.signature_id=cfr.canonical_signature_id
        WHERE ps.subject_id<>cfr.family_revision_id
        ORDER BY cfr.canonical_family_id
        """,
        (REPAIR_RELEASE, PARENT_RELEASE, BASE_CHILD_RELEASE),
    )
    keys = [
        "canonical_family_id",
        "family_revision_id",
        "revision_number",
        "canonical_signature_id",
        "canonical_proposition",
        "evidence_bundle_hash",
        "created_by_adjudication_id",
        "candidate_revision_id",
        "response_portability_status",
        "rationale",
        "wrong_subject_id",
    ]
    return [dict(zip(keys, row)) for row in cur.fetchall()]


def promote(dsn: str, commit: bool) -> dict[str, Any]:
    with psycopg.connect(dsn, autocommit=False) as conn:
        cur = conn.cursor()
        cur.execute("SET CONSTRAINTS ALL DEFERRED")
        cur.execute("SELECT count(*) FROM p3_authority_release WHERE release_id=%s", (REPAIR_RELEASE,))
        if cur.fetchone()[0]:
            raise ValueError(f"{REPAIR_RELEASE} already exists")
        rows = active_mismatches(cur)
        if len(rows) != 150:
            raise ValueError(f"expected 150 active canonical signature mismatches, found {len(rows)}")

        object_counts = {"canonical_revisions": len(rows), "canonical_signatures": len(rows), "parent_release": PARENT_RELEASE}
        input_hash = digest({"repair_release": REPAIR_RELEASE, "mismatches": rows})
        validation_hash = digest(object_counts)
        cur.execute(
            "INSERT INTO p3_authority_release (release_id,parent_release_id,schema_version,builder_version,input_manifest_hash,created_at,object_counts,validation_return_hash) VALUES (%s,%s,%s,%s,%s,now(),%s::jsonb,%s)",
            (REPAIR_RELEASE, PARENT_RELEASE, "p3-v7", BUILDER_VERSION, input_hash, json.dumps(object_counts, sort_keys=True), validation_hash),
        )
        copy_release_contracts(cur)

        canonical_revision_rows = []
        canonical_member_rows = []
        predecessor_rows = []
        signature_rows = []
        signature_field_rows = []
        adjudication_rows = []
        adjudication_member_rows = []
        object_rows = []
        ledger_rows = []
        snapshot_rows = []
        cur.execute("SELECT coalesce(max(substring(adjudication_id from 'P3ADJ-([0-9]+)')::int), 0) FROM p3_adjudication_decision")
        next_adjudication_ordinal = int(cur.fetchone()[0]) + 1
        for row in rows:
            family_id = row["canonical_family_id"]
            new_revision_number = int(row["revision_number"]) + 1
            new_revision_id = canonical_revision_id(family_id, new_revision_number)
            proposition = row["canonical_proposition"] if isinstance(row["canonical_proposition"], dict) else {}
            semantic_hash = str(proposition.get("semantic_signature_sha256") or digest(proposition))
            sig_hash = signature_hash(semantic_hash, new_revision_id)
            sig_id = f"P3SIG-{sig_hash[:16]}"
            repair_adjudication_id = adjudication_id(next_adjudication_ordinal)
            next_adjudication_ordinal += 1
            cur.execute(
                "SELECT coalesce(max(decision_ordinal), 0) + 1 FROM p3_adjudication_decision WHERE candidate_revision_id=%s",
                (row["candidate_revision_id"],),
            )
            decision_ordinal = int(cur.fetchone()[0])
            adjudication_rows.append(
                (
                    repair_adjudication_id,
                    row["candidate_revision_id"],
                    decision_ordinal,
                    "ACCEPTED_CANONICAL",
                    family_id,
                    json.dumps(proposition, sort_keys=True),
                    row["response_portability_status"] or "NOT_AUTHORIZED_BY_P3",
                    f"Append-only canonical signature subject repair R2; preserves candidate evidence and canonical proposition. Prior adjudication: {row['created_by_adjudication_id']}.",
                    row["evidence_bundle_hash"],
                    row["created_by_adjudication_id"],
                    REPAIR_RELEASE,
                )
            )
            canonical_revision_rows.append(
                (
                    new_revision_id,
                    family_id,
                    new_revision_number,
                    sig_id,
                    json.dumps(proposition, sort_keys=True),
                    row["evidence_bundle_hash"],
                    repair_adjudication_id,
                    REPAIR_RELEASE,
                )
            )
            signature_rows.append((sig_id, new_revision_id, "COMPLETE", sig_hash, REPAIR_RELEASE))
            signature_field_rows.extend(signature_fields(sig_id, proposition))
            object_rows.append(object_row(new_revision_id, "CANONICAL_FAMILY_REVISION", digest({"family_revision_id": new_revision_id, "proposition": proposition})))
            object_rows.append(object_row(sig_id, "PROPOSITION_SIGNATURE", sig_hash))
            object_rows.append(object_row(repair_adjudication_id, "ADJUDICATION", digest({"adjudication_id": repair_adjudication_id, "candidate_revision_id": row["candidate_revision_id"], "canonical_family_id": family_id})))
            cur.execute(
                "SELECT member_object_id, variant_revision_id FROM p3_canonical_family_membership WHERE family_revision_id=%s ORDER BY member_object_id",
                (row["family_revision_id"],),
            )
            members = cur.fetchall()
            canonical_member_rows.extend((new_revision_id, member, variant) for member, variant in members)
            adjudication_member_rows.extend((repair_adjudication_id, member, "ALREADY_CANONICAL", variant) for member, variant in members)
            predecessor_hash = digest({"predecessor": row["family_revision_id"], "members": members})
            predecessor_rows.append((new_revision_id, row["family_revision_id"], predecessor_hash, "EVIDENCE_ONLY_CONFIRMATION", REPAIR_RELEASE))
            for object_id, object_hash in [(new_revision_id, object_rows[-3][8]), (sig_id, sig_hash), (repair_adjudication_id, object_rows[-1][8])]:
                ledger_rows.append((REPAIR_RELEASE, object_id, "REVISED", None, object_hash, "Subject-owned canonical proposition signature repair."))
                snapshot_rows.append((REPAIR_RELEASE, object_id, object_hash))

        cur.executemany(
            "INSERT INTO p3_object_registry (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,allocation_release_id,retired_release_id,content_hash,stable_identity_note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            object_rows,
        )
        cur.executemany(
            "INSERT INTO p3_proposition_signature (signature_id,subject_id,signature_status,content_hash,authority_release_id) VALUES (%s,%s,%s,%s,%s)",
            signature_rows,
        )
        cur.executemany(
            "INSERT INTO p3_signature_field (signature_id,field_name,field_value,normalized_value_code,evidence_state,confidence) VALUES (%s,%s,%s,%s,%s,%s)",
            signature_field_rows,
        )
        cur.executemany(
            "INSERT INTO p3_adjudication_decision (adjudication_id,candidate_revision_id,decision_ordinal,decision_status,canonical_family_id,canonical_proposition,response_portability_status,rationale,evidence_bundle_hash,supersedes_adjudication_id,authority_release_id,created_at) VALUES (%s,%s,%s,%s,%s,%s::jsonb,%s,%s,%s,%s,%s,now())",
            adjudication_rows,
        )
        cur.executemany(
            "INSERT INTO p3_adjudication_member (adjudication_id,member_object_id,member_disposition,variant_revision_id) VALUES (%s,%s,%s,%s)",
            adjudication_member_rows,
        )
        cur.executemany(
            "INSERT INTO p3_canonical_family_revision (family_revision_id,canonical_family_id,revision_number,canonical_signature_id,canonical_proposition,evidence_bundle_hash,created_by_adjudication_id,authority_release_id) VALUES (%s,%s,%s,%s,%s::jsonb,%s,%s,%s)",
            canonical_revision_rows,
        )
        cur.executemany(
            "INSERT INTO p3_canonical_family_membership (family_revision_id,member_object_id,variant_revision_id) VALUES (%s,%s,%s)",
            canonical_member_rows,
        )
        cur.executemany(
            "INSERT INTO p3_family_revision_predecessor (family_revision_id,predecessor_family_revision_id,predecessor_membership_hash,extension_rule,authority_release_id) VALUES (%s,%s,%s,%s,%s)",
            predecessor_rows,
        )
        cur.execute(
            """
            INSERT INTO p3_release_change_ledger (release_id,object_id,change_type,prior_content_hash,content_hash,reason)
            SELECT %s, object_id, 'UNCHANGED_REFERENCE', content_hash, content_hash, 'Inherited unchanged from parent repair release'
            FROM p3_release_object_snapshot
            WHERE release_id=%s
            ON CONFLICT DO NOTHING
            """,
            (REPAIR_RELEASE, PARENT_RELEASE),
        )
        cur.execute(
            """
            INSERT INTO p3_release_object_snapshot (release_id,object_id,content_hash)
            SELECT %s, object_id, content_hash
            FROM p3_release_object_snapshot
            WHERE release_id=%s
            ON CONFLICT DO NOTHING
            """,
            (REPAIR_RELEASE, PARENT_RELEASE),
        )
        cur.executemany(
            "INSERT INTO p3_release_change_ledger (release_id,object_id,change_type,prior_content_hash,content_hash,reason) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            ledger_rows,
        )
        cur.executemany(
            "INSERT INTO p3_release_object_snapshot (release_id,object_id,content_hash) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
            snapshot_rows,
        )
        cur.executemany(
            "INSERT INTO p3_release_status_event (release_id,event_ordinal,status,occurred_at,evidence_hash) VALUES (%s,%s,%s,now(),%s) ON CONFLICT DO NOTHING",
            [
                (REPAIR_RELEASE, 1, "DRAFT", input_hash),
                (REPAIR_RELEASE, 2, "VALIDATED", digest(object_counts)),
                (REPAIR_RELEASE, 3, "SHADOW", digest({"shadow": object_counts})),
                (REPAIR_RELEASE, 4, "PROMOTED", digest({"repair": object_counts, "parent": PARENT_RELEASE})),
            ],
        )
        cur.execute("SET CONSTRAINTS ALL IMMEDIATE")

        cur.execute("SELECT parent_release_id FROM p3_authority_release WHERE release_id=%s", (REPAIR_RELEASE,))
        repair_parent = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM p3_canonical_family_revision WHERE authority_release_id=%s", (REPAIR_RELEASE,))
        repair_canonical_revisions = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM p3_adjudication_decision WHERE authority_release_id=%s", (REPAIR_RELEASE,))
        repair_adjudications = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM p3_proposition_signature WHERE authority_release_id=%s", (REPAIR_RELEASE,))
        repair_signatures = cur.fetchone()[0]
        remaining = active_mismatches(cur)
        checks = {
            "repair_parent": repair_parent,
            "repair_canonical_revisions": repair_canonical_revisions,
            "repair_adjudications": repair_adjudications,
            "repair_signatures": repair_signatures,
            "active_canonical_signature_mismatches_after_repair": len(remaining),
        }
        expected = {
            "repair_parent": PARENT_RELEASE,
            "repair_canonical_revisions": 150,
            "repair_adjudications": 150,
            "repair_signatures": 150,
            "active_canonical_signature_mismatches_after_repair": 0,
        }
        if checks != expected:
            raise ValueError(f"R2 repair verification mismatch: expected={expected} actual={checks}")
        if commit:
            conn.commit()
            mode = "committed"
        else:
            conn.rollback()
            mode = "rolled_back"
        return {"release_id": REPAIR_RELEASE, "mode": mode, **checks}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dsn", default=os.environ.get("RAWLSING_P3C_DSN", DEFAULT_DSN))
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    print(json.dumps(promote(args.dsn, args.commit), indent=2))


if __name__ == "__main__":
    main()
