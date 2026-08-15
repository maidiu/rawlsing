#!/usr/bin/env python3
"""Append-only repair for R4 child-release signature subject ownership.

Default mode is rollback-only. The repair creates a child of the committed
R4 GSS child release and only revises the 12 candidate/canonical revisions
whose signatures are owned by the predecessor family revision.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import psycopg


DEFAULT_GRAPH = Path(
    "data/ddm_build_copy/manifests/p3c_r184_question_family_registry/"
    "_staging_gss_r4_v3/R4_V3_MERGED_CANONICAL_OBJECT_GRAPH_DRY_RUN.json"
)
DEFAULT_DSN = "postgresql://postgres@127.0.0.1:5432/rawlsing_p3c_gss_r184"
PARENT_RELEASE = "P3-AUTHORITY-2026-08-05-R4-GSS-CHILD"
REPAIR_RELEASE = "P3-AUTHORITY-2026-08-05-R4-GSS-CHILD-SIGREPAIR-R1"
BUILDER_VERSION = "r4-p3c-signature-subject-repair-v1"
SIGNATURE_SCHEMA_VERSION = "p3-proposition-signature-subject-owned-v1"

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
CONTENT_ADDRESSED_TYPES = {"PROPOSITION_SIGNATURE"}


def stable(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(stable(value).encode("utf-8")).hexdigest()


def signature_hash(semantic_signature_sha256: str, subject_type: str, subject_id: str) -> str:
    return hashlib.sha256(
        "\x1f".join(
            [
                SIGNATURE_SCHEMA_VERSION,
                semantic_signature_sha256,
                subject_type,
                subject_id,
            ]
        ).encode("utf-8")
    ).hexdigest()


def signature_id(content_hash: str) -> str:
    return f"P3SIG-{content_hash[:16]}"


def candidate_revision_id(candidate_family_id: str, revision_number: int) -> str:
    return f"P3CANDREV-{candidate_family_id.split('-', 1)[1]}-R{revision_number:04d}"


def canonical_revision_id(canonical_family_id: str, revision_number: int) -> str:
    return f"JFAMREV-{canonical_family_id.split('-', 1)[1]}-R{revision_number:04d}"


def adjudication_id(ordinal: int) -> str:
    return f"P3ADJ-{ordinal:06d}"


def object_row(object_id: str, object_type: str, origin: str, content_hash: str | None = None) -> tuple[Any, ...]:
    return (
        object_id,
        object_type,
        "CONTENT_ADDRESSED_DERIVED_ID" if object_type in CONTENT_ADDRESSED_TYPES else "REGISTRY_ALLOCATED_DURABLE_ID",
        object_id,
        "R4_GSS_P3C_SIGNATURE_SUBJECT_REPAIR",
        origin,
        REPAIR_RELEASE,
        None,
        content_hash,
        "Allocated by append-only R4 P3C signature subject repair.",
    )


def signature_fields(signature: str, identity: dict[str, Any]) -> list[tuple[Any, ...]]:
    mapped = {SIGNATURE_FIELD_MAP[k]: str(v) for k, v in identity.items() if k in SIGNATURE_FIELD_MAP}
    mapped.setdefault("derived_status", "R4_GSS_SEMANTIC_REVIEW_VERIFIED")
    rows = []
    for field in SIGNATURE_FIELDS:
        value = mapped.get(field)
        if value is None:
            rows.append((signature, field, None, None, "NOT_APPLICABLE", "NOT_APPLICABLE"))
        else:
            rows.append((signature, field, value, value, "KNOWN", "HIGH"))
    return rows


def load_graph(graph_path: Path) -> dict[str, dict[str, Any]]:
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    if graph.get("component_count") != 162 or graph.get("source_component_count") != 162:
        raise ValueError("graph is not 162/162")
    if graph.get("unresolved_components"):
        raise ValueError("graph still has unresolved components")
    return graph["components"]


def copy_release_contracts(cur: psycopg.Cursor) -> None:
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
        ORDER BY from_status NULLS FIRST,to_status,authority_release_id DESC
        ON CONFLICT DO NOTHING
        """,
        (REPAIR_RELEASE,),
    )


def validate_signature_insert(cur: psycopg.Cursor, signature: str, subject_id: str, content_hash: str) -> None:
    cur.execute(
        "SELECT subject_id, content_hash FROM p3_proposition_signature WHERE signature_id=%s",
        (signature,),
    )
    row = cur.fetchone()
    if row and (row[0] != subject_id or row[1] != content_hash):
        raise ValueError(
            f"signature id collision: {signature} existing_subject={row[0]} requested_subject={subject_id}"
        )


def promote(graph_path: Path, dsn: str, commit: bool) -> dict[str, Any]:
    graph_components = load_graph(graph_path)
    input_hash = digest({"parent_release": PARENT_RELEASE, "graph": graph_path.read_text(encoding="utf-8")})

    with psycopg.connect(dsn, autocommit=False) as conn:
        cur = conn.cursor()
        cur.execute("SET CONSTRAINTS ALL DEFERRED")

        cur.execute(
            """
            WITH cr AS (
              SELECT candidate_revision_id, candidate_family_id, revision_number,
                     candidate_classification, candidate_origin_type, origin_key,
                     canonical_signature_id, evidence_bundle_hash, authority_release_id
              FROM p3_candidate_revision
              WHERE authority_release_id=%s
            ), snap AS (
              SELECT candidate_revision_id,
                     canonical_payload->>'component_id' AS component_id,
                     canonical_payload->>'canonical_family_id' AS canonical_family_id,
                     canonical_payload->>'canonical_family_revision_id' AS canonical_family_revision_id,
                     canonical_payload->>'source_payload_revision_id' AS source_payload_revision_id,
                     canonical_payload->>'action' AS action,
                     canonical_payload
              FROM p3_candidate_evidence_snapshot
              WHERE authority_release_id=%s
            ), adj AS (
              SELECT DISTINCT ON (candidate_revision_id)
                     candidate_revision_id, adjudication_id, canonical_proposition,
                     response_portability_status, rationale, evidence_bundle_hash
              FROM p3_adjudication_decision
              WHERE authority_release_id=%s
              ORDER BY candidate_revision_id, decision_ordinal DESC
            )
            SELECT cr.candidate_revision_id, cr.candidate_family_id, cr.revision_number,
                   cr.candidate_classification, cr.candidate_origin_type, cr.origin_key,
                   cr.evidence_bundle_hash AS candidate_evidence_hash,
                   snap.component_id, snap.canonical_family_id,
                   snap.canonical_family_revision_id, snap.source_payload_revision_id,
                   snap.action, snap.canonical_payload,
                   cfr.revision_number AS canonical_revision_number,
                   cfr.canonical_proposition, cfr.evidence_bundle_hash AS canonical_evidence_hash,
                   adj.adjudication_id, adj.response_portability_status, adj.rationale,
                   s.signature_id, s.subject_id
            FROM cr
            JOIN p3_proposition_signature s ON s.signature_id=cr.canonical_signature_id
            JOIN snap USING(candidate_revision_id)
            JOIN p3_canonical_family_revision cfr
              ON cfr.family_revision_id=snap.canonical_family_revision_id
            JOIN adj USING(candidate_revision_id)
            WHERE s.subject_id <> cr.candidate_revision_id
            ORDER BY cr.candidate_revision_id
            """,
            (PARENT_RELEASE, PARENT_RELEASE, PARENT_RELEASE),
        )
        affected = cur.fetchall()
        if len(affected) != 12:
            raise ValueError(f"expected 12 affected signature subject rows, found {len(affected)}")

        object_counts = {
            "repair_scope": 12,
            "inherited_components": 150,
            "candidate_revisions": 12,
            "canonical_revisions": 12,
            "adjudications": 12,
            "proposition_signatures": 24,
        }
        cur.execute(
            """
            INSERT INTO p3_authority_release
              (release_id,parent_release_id,schema_version,builder_version,input_manifest_hash,
               created_at,object_counts,validation_return_hash,migration_artifact,rollback_artifact)
            VALUES (%s,%s,'p3-v7',%s,%s,now(),%s::jsonb,%s,%s,%s)
            ON CONFLICT (release_id) DO NOTHING
            """,
            (
                REPAIR_RELEASE,
                PARENT_RELEASE,
                BUILDER_VERSION,
                input_hash,
                stable(object_counts),
                "0" * 64,
                graph_path.as_posix(),
                "transaction rollback",
            ),
        )
        copy_release_contracts(cur)

        cur.execute("SELECT COALESCE(max(substring(adjudication_id from 'P3ADJ-([0-9]+)')::int),0) FROM p3_adjudication_decision")
        next_adjudication = cur.fetchone()[0] + 1

        object_rows: list[tuple[Any, ...]] = []
        signature_rows: list[tuple[Any, ...]] = []
        signature_field_rows: list[tuple[Any, ...]] = []
        candidate_revision_rows: list[tuple[Any, ...]] = []
        candidate_snapshot_rows: list[tuple[Any, ...]] = []
        candidate_genealogy_rows: list[tuple[Any, ...]] = []
        candidate_link_rows: list[tuple[Any, ...]] = []
        candidate_member_rows: list[tuple[Any, ...]] = []
        internal_pair_rows: list[tuple[Any, ...]] = []
        adjudication_rows: list[tuple[Any, ...]] = []
        adjudication_member_rows: list[tuple[Any, ...]] = []
        canonical_revision_rows: list[tuple[Any, ...]] = []
        canonical_member_rows: list[tuple[Any, ...]] = []
        predecessor_rows: list[tuple[Any, ...]] = []
        ledger_rows: list[tuple[Any, ...]] = []
        snapshot_rows: list[tuple[Any, ...]] = []

        for idx, row in enumerate(affected):
            (
                old_cand_rev,
                cand_family,
                old_cand_revision_number,
                candidate_classification,
                candidate_origin_type,
                _old_origin_key,
                _old_candidate_evidence_hash,
                component_id,
                canonical_family,
                old_family_revision,
                source_payload_revision,
                action,
                old_snapshot_payload,
                old_canonical_revision_number,
                canonical_proposition,
                old_canonical_evidence_hash,
                old_adjudication,
                response_portability_status,
                rationale,
                old_signature,
                old_signature_subject,
            ) = row
            if action != "ATTACH_EXISTING_FAMILY":
                raise ValueError(f"repair scope includes non-attachment action: {old_cand_rev} {action}")
            graph_row = graph_components[component_id]

            new_cand_rev_number = old_cand_revision_number + 1
            new_cand_rev = candidate_revision_id(cand_family, new_cand_rev_number)
            new_family_rev_number = old_canonical_revision_number + 1
            new_family_rev = canonical_revision_id(canonical_family, new_family_rev_number)
            new_adjudication = adjudication_id(next_adjudication + idx)

            candidate_sig_hash = signature_hash(graph_row["semantic_signature_sha256"], "CANDIDATE_REVISION", new_cand_rev)
            canonical_sig_hash = signature_hash(
                graph_row["semantic_signature_sha256"], "CANONICAL_FAMILY_REVISION", new_family_rev
            )
            candidate_sig = signature_id(candidate_sig_hash)
            canonical_sig = signature_id(canonical_sig_hash)
            validate_signature_insert(cur, candidate_sig, new_cand_rev, candidate_sig_hash)
            validate_signature_insert(cur, canonical_sig, new_family_rev, canonical_sig_hash)

            new_payload = dict(old_snapshot_payload)
            new_payload.update(
                {
                    "candidate_revision_id": new_cand_rev,
                    "canonical_family_revision_id": new_family_rev,
                    "source_defective_candidate_revision_id": old_cand_rev,
                    "source_defective_canonical_family_revision_id": old_family_revision,
                    "source_defective_signature_id": old_signature,
                    "signature_repair_reason": "subject_owned_signature_required",
                }
            )
            new_candidate_hash = digest(new_payload)
            new_origin_key = digest(
                {
                    "repair_release": REPAIR_RELEASE,
                    "source_candidate_revision_id": old_cand_rev,
                    "candidate_revision_id": new_cand_rev,
                }
            )
            new_canonical_hash = digest(
                {
                    "canonical_proposition": canonical_proposition,
                    "source_family_revision": old_family_revision,
                    "repaired_family_revision": new_family_rev,
                    "canonical_signature_id": canonical_sig,
                }
            )

            object_rows.extend(
                [
                    object_row(new_cand_rev, "CANDIDATE_REVISION", component_id, new_candidate_hash),
                    object_row(new_adjudication, "ADJUDICATION", component_id, old_canonical_evidence_hash),
                    object_row(new_family_rev, "CANONICAL_FAMILY_REVISION", component_id, new_canonical_hash),
                    object_row(candidate_sig, "PROPOSITION_SIGNATURE", component_id, candidate_sig_hash),
                    object_row(canonical_sig, "PROPOSITION_SIGNATURE", component_id, canonical_sig_hash),
                ]
            )
            signature_rows.append((candidate_sig, new_cand_rev, "COMPLETE", candidate_sig_hash, REPAIR_RELEASE))
            signature_rows.append((canonical_sig, new_family_rev, "COMPLETE", canonical_sig_hash, REPAIR_RELEASE))
            signature_field_rows.extend(signature_fields(candidate_sig, graph_row.get("canonical_identity") or {}))
            signature_field_rows.extend(signature_fields(canonical_sig, graph_row.get("canonical_identity") or {}))

            candidate_revision_rows.append(
                (
                    new_cand_rev,
                    cand_family,
                    new_cand_rev_number,
                    candidate_classification,
                    candidate_origin_type,
                    new_origin_key,
                    candidate_sig,
                    new_candidate_hash,
                    REPAIR_RELEASE,
                )
            )
            candidate_snapshot_rows.append(
                (new_cand_rev, "R4_P3C_SIGNATURE_SUBJECT_REPAIR_V1", stable(new_payload), new_candidate_hash, REPAIR_RELEASE)
            )
            candidate_genealogy_rows.append(
                (
                    new_cand_rev,
                    cand_family,
                    new_cand_rev_number,
                    cand_family,
                    old_cand_rev,
                    "LIVE_REVISION",
                    "UNCHANGED_FAMILY_APPEND_REVISION",
                    "SIGNATURE_SUBJECT_REPAIR",
                    REPAIR_RELEASE,
                )
            )

            cur.execute("SELECT component_id FROM p3_candidate_component_link WHERE candidate_revision_id=%s", (old_cand_rev,))
            candidate_link_rows.extend((new_cand_rev, linked_component) for (linked_component,) in cur.fetchall())
            cur.execute(
                "SELECT member_object_id,membership_role,membership_basis FROM p3_candidate_membership WHERE candidate_revision_id=%s",
                (old_cand_rev,),
            )
            candidate_member_rows.extend((new_cand_rev, member, role, basis, REPAIR_RELEASE) for member, role, basis in cur.fetchall())
            cur.execute(
                "SELECT left_object_id,right_object_id,pair_state,direct_pair_projection_id FROM p3_internal_pair_matrix WHERE candidate_revision_id=%s",
                (old_cand_rev,),
            )
            internal_pair_rows.extend((new_cand_rev, left, right, state, projection) for left, right, state, projection in cur.fetchall())

            adjudication_rows.append(
                (
                    new_adjudication,
                    new_cand_rev,
                    1,
                    "ACCEPTED_CANONICAL",
                    canonical_family,
                    stable(canonical_proposition),
                    response_portability_status,
                    f"Append-only repair of signature subject ownership for {old_cand_rev}; original rationale: {rationale}",
                    old_canonical_evidence_hash,
                    None,
                    REPAIR_RELEASE,
                )
            )
            cur.execute(
                "SELECT member_object_id,variant_revision_id FROM p3_canonical_family_membership WHERE family_revision_id=%s",
                (old_family_revision,),
            )
            old_members = cur.fetchall()
            adjudication_member_rows.extend((new_adjudication, member, "ALREADY_CANONICAL", variant) for member, variant in old_members)
            canonical_revision_rows.append(
                (
                    new_family_rev,
                    canonical_family,
                    new_family_rev_number,
                    canonical_sig,
                    stable(canonical_proposition),
                    new_canonical_hash,
                    new_adjudication,
                    REPAIR_RELEASE,
                )
            )
            canonical_member_rows.extend((new_family_rev, member, variant) for member, variant in old_members)
            predecessor_rows.append(
                (
                    new_family_rev,
                    old_family_revision,
                    digest({"predecessor": old_family_revision, "members": sorted(member for member, _ in old_members)}),
                    "EVIDENCE_ONLY_CONFIRMATION",
                    REPAIR_RELEASE,
                )
            )

            for oid, prior_hash, content_hash, change, reason in [
                (old_cand_rev, None, new_candidate_hash, "SUPERSEDED", "Signature subject repair supersedes defective candidate revision"),
                (old_family_revision, None, new_canonical_hash, "SUPERSEDED", "Signature subject repair supersedes defective canonical revision"),
                (new_cand_rev, None, new_candidate_hash, "ADDED", "Corrected candidate revision with subject-owned signature"),
                (new_adjudication, old_canonical_evidence_hash, old_canonical_evidence_hash, "ADDED", "Replacement adjudication for signature subject repair"),
                (new_family_rev, old_canonical_evidence_hash, new_canonical_hash, "REVISED", "Corrected canonical revision with subject-owned signature"),
                (candidate_sig, None, candidate_sig_hash, "ADDED", "Candidate-owned proposition signature"),
                (canonical_sig, None, canonical_sig_hash, "ADDED", "Canonical-revision-owned proposition signature"),
            ]:
                ledger_rows.append((REPAIR_RELEASE, oid, change, prior_hash, content_hash, reason))
                snapshot_rows.append((REPAIR_RELEASE, oid, content_hash))

        cur.executemany(
            """
            INSERT INTO p3_object_registry
              (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,
               allocation_release_id,retired_release_id,content_hash,stable_identity_note)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (object_id) DO NOTHING
            """,
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
            "INSERT INTO p3_candidate_revision (candidate_revision_id,candidate_family_id,revision_number,candidate_classification,candidate_origin_type,origin_key,canonical_signature_id,evidence_bundle_hash,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            candidate_revision_rows,
        )
        cur.executemany(
            "INSERT INTO p3_candidate_evidence_snapshot (candidate_revision_id,evidence_contract_version,canonical_payload,evidence_bundle_hash,authority_release_id,created_at) VALUES (%s,%s,%s::jsonb,%s,%s,now())",
            candidate_snapshot_rows,
        )
        cur.executemany(
            "INSERT INTO p3_candidate_revision_genealogy (candidate_revision_id,candidate_family_id,revision_number,predecessor_candidate_family_id,predecessor_candidate_revision_id,predecessor_source,genealogy_branch,migration_reason,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            candidate_genealogy_rows,
        )
        cur.executemany(
            "INSERT INTO p3_candidate_component_link (candidate_revision_id,component_id) VALUES (%s,%s)",
            candidate_link_rows,
        )
        cur.executemany(
            "INSERT INTO p3_candidate_membership (candidate_revision_id,member_object_id,membership_role,membership_basis,authority_release_id) VALUES (%s,%s,%s,%s,%s)",
            candidate_member_rows,
        )
        cur.executemany(
            "INSERT INTO p3_internal_pair_matrix (candidate_revision_id,left_object_id,right_object_id,pair_state,direct_pair_projection_id) VALUES (%s,%s,%s,%s,%s)",
            internal_pair_rows,
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
            SELECT %s, object_id, 'UNCHANGED_REFERENCE', content_hash, content_hash, 'Inherited unchanged from defective child release'
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
        checks: dict[str, Any] = {}
        for name, sql in {
            "repair_parent": "SELECT parent_release_id FROM p3_authority_release WHERE release_id=%s",
            "repair_candidate_revisions": "SELECT count(*) FROM p3_candidate_revision WHERE authority_release_id=%s",
            "repair_canonical_revisions": "SELECT count(*) FROM p3_canonical_family_revision WHERE authority_release_id=%s",
            "repair_adjudications": "SELECT count(*) FROM p3_adjudication_decision WHERE authority_release_id=%s",
            "repair_signatures": "SELECT count(*) FROM p3_proposition_signature WHERE authority_release_id=%s",
            "candidate_signature_mismatches": "SELECT count(*) FROM p3_candidate_revision cr JOIN p3_proposition_signature s ON s.signature_id=cr.canonical_signature_id WHERE cr.authority_release_id=%s AND s.subject_id<>cr.candidate_revision_id",
            "canonical_signature_mismatches": "SELECT count(*) FROM p3_canonical_family_revision r JOIN p3_proposition_signature s ON s.signature_id=r.canonical_signature_id WHERE r.authority_release_id=%s AND s.subject_id<>r.family_revision_id",
            "r184_release_rows": "SELECT count(*) FROM p3_authority_release WHERE release_id='P3-AUTHORITY-2026-08-02-R184'",
            "defective_child_rows": "SELECT count(*) FROM p3_authority_release WHERE release_id=%s",
        }.items():
            if "%s" in sql:
                cur.execute(sql, (REPAIR_RELEASE if name != "defective_child_rows" else PARENT_RELEASE,))
            else:
                cur.execute(sql)
            checks[name] = cur.fetchone()[0]
        expected = {
            "repair_parent": PARENT_RELEASE,
            "repair_candidate_revisions": 12,
            "repair_canonical_revisions": 12,
            "repair_adjudications": 12,
            "repair_signatures": 24,
            "candidate_signature_mismatches": 0,
            "canonical_signature_mismatches": 0,
            "r184_release_rows": 1,
            "defective_child_rows": 1,
        }
        if checks != expected:
            raise ValueError(f"repair verification mismatch: expected={expected} actual={checks}")

        if commit:
            conn.commit()
            mode = "committed"
        else:
            conn.rollback()
            mode = "rolled_back"
        return {"release_id": REPAIR_RELEASE, "mode": mode, **checks}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path, default=DEFAULT_GRAPH)
    parser.add_argument("--dsn", default=os.environ.get("RAWLSING_P3C_DSN", DEFAULT_DSN))
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    print(json.dumps(promote(args.graph, args.dsn, args.commit), indent=2))


if __name__ == "__main__":
    main()
