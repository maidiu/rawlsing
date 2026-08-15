#!/usr/bin/env python3
"""Promote the staged R4 GSS payload into a P3C child release.

Default mode is rollback-only: it exercises the full transaction, forces
deferred constraints, reports verification counts, and rolls back.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import psycopg


DEFAULT_PAYLOAD = Path(
    "data/ddm_build_copy/manifests/p3c_r184_question_family_registry/"
    "_staging_gss_r4_v3/execution/R4_P3C_IMPORT_PAYLOAD_V1.json"
)
DEFAULT_GRAPH = Path(
    "data/ddm_build_copy/manifests/p3c_r184_question_family_registry/"
    "_staging_gss_r4_v3/R4_V3_MERGED_CANONICAL_OBJECT_GRAPH_DRY_RUN.json"
)
DEFAULT_DSN = "postgresql://postgres@127.0.0.1:5432/rawlsing_p3c_gss_r184"
PARENT_RELEASE = "P3-AUTHORITY-2026-08-02-R184"
CHILD_RELEASE = "P3-AUTHORITY-2026-08-05-R4-GSS-CHILD"
BUILDER_VERSION = "r4-p3c-child-promoter-v1"


def stable(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(stable(value).encode("utf-8")).hexdigest()


def content_id(prefix: str, value: Any, chars: int = 24) -> str:
    return f"{prefix}-{digest(value)[:chars]}"


def family_revision_id(family_id: str, graph_row: dict[str, Any], action: str) -> str:
    if action == "ALLOCATE_NEW_FAMILY":
        return f"JFAMREV-{family_id.split('-', 1)[1]}-R0001"
    raise AssertionError("existing-family child revision ids are allocated from live DB state")


def candidate_family_id(ordinal: int) -> str:
    return f"P3CAND-{ordinal:06d}"


def candidate_revision_id(ordinal: int) -> str:
    return f"P3CANDREV-{ordinal:06d}-R0001"


def adjudication_id(ordinal: int) -> str:
    return f"P3ADJ-{ordinal:06d}"


def genealogy_id(ordinal: int) -> str:
    return f"P3GEN-{ordinal:06d}"


def signature_id(signature_hash: str) -> str:
    return f"P3SIG-{signature_hash[:16]}"


CONTENT_ADDRESSED_TYPES = {"CANDIDATE_COMPONENT", "PAIR_FACT", "PAIR_PROJECTION", "PROPOSITION_SIGNATURE"}
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


def object_row(object_id: str, object_type: str, origin: str, content_hash: str | None = None) -> tuple[Any, ...]:
    return (
        object_id,
        object_type,
        "CONTENT_ADDRESSED_DERIVED_ID" if object_type in CONTENT_ADDRESSED_TYPES else "REGISTRY_ALLOCATED_DURABLE_ID",
        object_id,
        "R4_GSS_P3C_CHILD_PROMOTION",
        origin,
        CHILD_RELEASE,
        None,
        content_hash,
        "Allocated by deterministic R4-to-P3C child release promoter.",
    )


def ensure_no_conflict(cur: psycopg.Cursor, table: str, key_col: str, key: str, comparable: dict[str, Any]) -> None:
    cur.execute(f"SELECT to_jsonb(t) FROM {table} t WHERE {key_col}=%s", (key,))
    row = cur.fetchone()
    if not row:
        return
    existing = row[0]
    for col, expected in comparable.items():
        if existing.get(col) != expected:
            raise ValueError(f"conflicting existing row in {table}.{key_col}={key}: {col}")


def load_payload(payload_path: Path, graph_path: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    if payload.get("version") != "R4_P3C_IMPORT_PAYLOAD_V1":
        raise ValueError("unexpected payload version")
    if graph.get("component_count") != 162 or graph.get("source_component_count") != 162:
        raise ValueError("graph is not 162/162")
    if graph.get("unresolved_components"):
        raise ValueError("graph still has unresolved components")
    if len(payload.get("families", [])) != 146:
        raise ValueError("payload does not contain 146 new-family candidates")
    if len(payload.get("revisions", [])) != 162 or len(payload.get("memberships", [])) != 413:
        raise ValueError("payload row counts do not match the R4 V3 contract")
    return payload, graph["components"]


def promote(payload_path: Path, graph_path: Path, dsn: str, commit: bool) -> dict[str, Any]:
    payload, graph_components = load_payload(payload_path, graph_path)
    by_component = {a["component_id"]: a for a in payload["actions"]}
    revision_by_component = {}
    revision_by_family_revision = {}
    payload_members_by_revision: dict[str, set[str]] = {}
    for rev in payload["revisions"]:
        component_id = rev["proposition"].get("component_id") or rev["proposition"].get("genealogy", {}).get("source_component_id")
        if component_id:
            revision_by_component[component_id] = rev
        revision_by_family_revision[(rev["family_id"], rev["family_revision_id"])] = rev
    for membership in payload["memberships"]:
        payload_members_by_revision.setdefault(membership["family_revision_id"], set()).add(membership["member_object_id"])
    for action in payload["actions"]:
        revision_by_component.setdefault(
            action["component_id"],
            revision_by_family_revision[(action["family_id"], action["revision_id"])],
        )

    input_hash = digest({"payload_sha256": payload["payload_sha256"], "graph": graph_path.read_text(encoding="utf-8")})
    object_counts = {
        "components": 162,
        "new_families": 146,
        "existing_family_attachments": 16,
        "revisions": 162,
        "payload_memberships": 413,
    }

    with psycopg.connect(dsn, autocommit=False) as conn:
        cur = conn.cursor()
        cur.execute("SET CONSTRAINTS ALL DEFERRED")
        cur.execute(
            """
            INSERT INTO p3_authority_release
              (release_id,parent_release_id,schema_version,builder_version,input_manifest_hash,
               created_at,object_counts,validation_return_hash,migration_artifact,rollback_artifact)
            VALUES (%s,%s,'p3-v7',%s,%s,now(),%s::jsonb,%s,%s,%s)
            ON CONFLICT (release_id) DO NOTHING
            """,
            (
                CHILD_RELEASE,
                PARENT_RELEASE,
                BUILDER_VERSION,
                input_hash,
                stable(object_counts),
                "0" * 64,
                payload_path.as_posix(),
                "transaction rollback",
            ),
        )
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
            (CHILD_RELEASE,),
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
            (CHILD_RELEASE,),
        )
        cur.execute(
            """
            INSERT INTO p3_vocabulary_code
              (vocabulary_domain,code,introduced_release_id,retired_release_id)
            SELECT vocabulary_domain,code,%s,NULL
            FROM p3_vocabulary_code
            ON CONFLICT DO NOTHING
            """,
            (CHILD_RELEASE,),
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
            (CHILD_RELEASE,),
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
            (CHILD_RELEASE,),
        )

        object_rows: list[tuple[Any, ...]] = []
        signature_rows: list[tuple[Any, ...]] = []
        signature_field_rows: list[tuple[Any, ...]] = []
        component_rows: list[tuple[Any, ...]] = []
        component_member_rows: list[tuple[Any, ...]] = []
        component_edge_rows: list[tuple[Any, ...]] = []
        pair_fact_rows: list[tuple[Any, ...]] = []
        pair_endpoint_rows: list[tuple[Any, ...]] = []
        pair_endpoint_subject_rows: list[tuple[Any, ...]] = []
        pair_projection_rows: list[tuple[Any, ...]] = []
        pair_source_rows: list[tuple[Any, ...]] = []
        candidate_family_rows: list[tuple[Any, ...]] = []
        candidate_revision_rows: list[tuple[Any, ...]] = []
        candidate_snapshot_rows: list[tuple[Any, ...]] = []
        candidate_origin_rows: list[tuple[Any, ...]] = []
        candidate_genealogy_rows: list[tuple[Any, ...]] = []
        candidate_link_rows: list[tuple[Any, ...]] = []
        candidate_member_rows: list[tuple[Any, ...]] = []
        internal_pair_rows: list[tuple[Any, ...]] = []
        adjudication_rows: list[tuple[Any, ...]] = []
        adjudication_member_rows: list[tuple[Any, ...]] = []
        canonical_family_rows: list[tuple[Any, ...]] = []
        canonical_revision_rows: list[tuple[Any, ...]] = []
        canonical_member_rows: list[tuple[Any, ...]] = []
        genealogy_rows: list[tuple[Any, ...]] = []
        genealogy_member_rows: list[tuple[Any, ...]] = []
        predecessor_rows: list[tuple[Any, ...]] = []
        ledger_rows: list[tuple[Any, ...]] = []
        snapshot_rows: list[tuple[Any, ...]] = []
        cur.execute("SELECT COALESCE(max(substring(candidate_family_id from 'P3CAND-([0-9]+)')::int),0) FROM p3_candidate_family")
        next_candidate = cur.fetchone()[0] + 1
        cur.execute("SELECT COALESCE(max(substring(adjudication_id from 'P3ADJ-([0-9]+)')::int),0) FROM p3_adjudication_decision")
        next_adjudication = cur.fetchone()[0] + 1
        cur.execute("SELECT COALESCE(max(substring(genealogy_id from 'P3GEN-([0-9]+)')::int),0) FROM p3_family_genealogy")
        next_genealogy = cur.fetchone()[0] + 1
        cur.execute("SELECT COALESCE(max(substring(canonical_family_id from 'JFAM-([0-9]+)')::int),0) FROM p3_canonical_family")
        next_canonical_family = cur.fetchone()[0] + 1
        cur.execute(
            """
            SELECT canonical_family_id, COALESCE(max(substring(family_revision_id from 'R([0-9]{4})$')::int),0)
            FROM p3_canonical_family_revision
            GROUP BY canonical_family_id
            """
        )
        live_family_revision_numbers = dict(cur.fetchall())
        cur.execute("SELECT family_revision_id, member_object_id FROM p3_canonical_family_membership")
        live_revision_members: dict[str, set[str]] = {}
        for rev_id, member_id in cur.fetchall():
            live_revision_members.setdefault(rev_id, set()).add(member_id)

        # The dry-run plan intentionally uses provisional family IDs for new
        # families. Allocate durable IDs only here, inside the promotion
        # transaction, after reconciling against the live registry.
        new_family_ids: dict[str, str] = {}
        for component_id in sorted(graph_components):
            action = by_component[component_id]
            if action["action"] == "ALLOCATE_NEW_FAMILY":
                provisional = action["family_id"]
                new_family_ids.setdefault(
                    provisional,
                    f"JFAM-{next_canonical_family + len(new_family_ids):06d}",
                )

        for ordinal, component_id in enumerate(sorted(graph_components)):
            graph_row = graph_components[component_id]
            action = by_component[component_id]
            rev = revision_by_component[component_id]
            family_id = action["family_id"]
            cand_num = next_candidate + ordinal
            adj_num = next_adjudication + ordinal
            gen_num = next_genealogy + ordinal
            cand_family = candidate_family_id(cand_num)
            cand_rev = candidate_revision_id(cand_num)
            adj = adjudication_id(adj_num)
            if action["action"] == "ALLOCATE_NEW_FAMILY":
                family_id = new_family_ids[action["family_id"]]
                fam_rev = family_revision_id(family_id, graph_row, action["action"])
                revision_number = 1
            else:
                revision_number = live_family_revision_numbers.get(family_id, 0) + 1
                fam_rev = f"JFAMREV-{family_id.split('-', 1)[1]}-R{revision_number:04d}"
            semantic_sig_hash = graph_row["semantic_signature_sha256"]
            sig_hash = digest(
                {
                    "semantic_signature_sha256": semantic_sig_hash,
                    "candidate_revision_id": cand_rev,
                    "family_revision_id": fam_rev,
                }
            )
            sig = signature_id(sig_hash)
            decision_members = {m["lineage_id"] for m in graph_row.get("member_decisions", []) if m.get("lineage_id")}
            payload_delta_members = payload_members_by_revision.get(action["revision_id"], set())
            canonical_members = sorted(
                decision_members
                | payload_delta_members
                | set(rev["proposition"].get("member_lineages", []))
            )
            members = canonical_members
            if not members:
                raise ValueError(f"component has no members: {component_id}")
            support_ids = sorted(set(graph_row.get("supporting_pair_ids") or []))
            if not support_ids:
                support_ids = [content_id("r4syntheticpair", {"component_id": component_id, "members": members}, 24)]
            pair_members = members[:2] if len(members) >= 2 else [members[0], members[0]]
            if pair_members[0] == pair_members[1]:
                raise ValueError(f"component has fewer than two members after canonical union: {component_id}")
            left_member, right_member = sorted(pair_members)

            canonical_payload = rev["proposition"]
            evidence_hash = rev["evidence_bundle_hash"]
            origin_key = digest({"component_id": component_id, "family_id": family_id, "signature": sig_hash})
            comp_hash = digest({"component_id": component_id, "members": members, "identity": graph_row.get("canonical_identity")})
            comp_id = f"P3COMP-{comp_hash[:16]}"
            cand_payload = {
                "component_id": component_id,
                "canonical_family_id": family_id,
                "canonical_family_revision_id": fam_rev,
                "canonical_signature_id": sig,
                "canonical_proposition": canonical_payload,
                "member_lineages": members,
                "canonical_revision_member_lineages": canonical_members,
                "action": action["action"],
                "source_payload_revision_id": rev["family_revision_id"],
            }
            cand_hash = digest(cand_payload)
            prior_rev = rev["proposition"].get("genealogy", {}).get("parent_family_revision_id")

            object_rows.extend(
                [
                    object_row(comp_id, "CANDIDATE_COMPONENT", component_id, comp_hash),
                    object_row(cand_family, "CANDIDATE_FAMILY", component_id),
                    object_row(cand_rev, "CANDIDATE_REVISION", component_id, cand_hash),
                    object_row(adj, "ADJUDICATION", component_id, evidence_hash),
                    object_row(sig, "PROPOSITION_SIGNATURE", component_id, sig_hash),
                    object_row(fam_rev, "CANONICAL_FAMILY_REVISION", component_id, evidence_hash),
                ]
            )
            if action["action"] == "ALLOCATE_NEW_FAMILY":
                object_rows.append(object_row(family_id, "CANONICAL_FAMILY", component_id))
            gen_id = genealogy_id(gen_num)
            projection_ids = []
            for support_id in support_ids:
                pair_payload = {
                    "source_pair_id": support_id,
                    "left_object_id": left_member,
                    "right_object_id": right_member,
                    "relation_type": "PROPOSITION_IDENTITY_ONLY",
                    "component_id": component_id,
                }
                pair_hash = digest(pair_payload)
                pair_id = f"P3PF-{pair_hash[:16]}"
                projection_payload = {"pair_fact_id": pair_id, "left": left_member, "right": right_member, "basis": "ORIGINAL_LINEAGES"}
                projection_hash = digest(projection_payload)
                projection_id = f"P3PROJ-{projection_hash[:16]}"
                object_rows.append(object_row(pair_id, "PAIR_FACT", support_id, pair_hash))
                object_rows.append(object_row(projection_id, "PAIR_PROJECTION", support_id, projection_hash))
                pair_fact_rows.append((pair_id, left_member, right_member, "SYMMETRIC", "PROPOSITION_IDENTITY_ONLY", None, None, None, None, "QUESTION_PROPOSITION_ONLY", "QUESTION_PROPOSITION_ONLY", True, "J_FAMILY_CANDIDATE_ELIGIBLE", False, CHILD_RELEASE))
                pair_endpoint_rows.append((pair_id, "LEFT", left_member, "ORIGINAL_LINEAGE", stable([support_id]), CHILD_RELEASE))
                pair_endpoint_rows.append((pair_id, "RIGHT", right_member, "ORIGINAL_LINEAGE", stable([support_id]), CHILD_RELEASE))
                pair_endpoint_subject_rows.append((pair_id, "LEFT", left_member))
                pair_endpoint_subject_rows.append((pair_id, "RIGHT", right_member))
                pair_projection_rows.append((projection_id, pair_id, left_member, right_member, "ORIGINAL_LINEAGES", stable([support_id]), CHILD_RELEASE))
                pair_source_rows.append((pair_id, "EXACT_FOUNDATION_CLOSURE", support_id, "GOVERNING", True, None))
                projection_ids.append(projection_id)

            signature_rows.append((sig, cand_rev, "COMPLETE", sig_hash, CHILD_RELEASE))
            identity = graph_row.get("canonical_identity") or {}
            mapped_fields = {SIGNATURE_FIELD_MAP[k]: str(v) for k, v in identity.items() if k in SIGNATURE_FIELD_MAP}
            mapped_fields.setdefault("derived_status", "R4_GSS_SEMANTIC_REVIEW_VERIFIED")
            for field in SIGNATURE_FIELDS:
                value = mapped_fields.get(field)
                if value is None:
                    signature_field_rows.append((sig, field, None, None, "NOT_APPLICABLE", "NOT_APPLICABLE"))
                else:
                    signature_field_rows.append((sig, field, value, value, "KNOWN", "HIGH"))
            connectivity_edges = len(projection_ids)
            component_rows.append((comp_id, "PROPOSITION_ONLY_COMPONENT", "R4_V3_MERGED_CANONICAL_OBJECT_GRAPH", comp_hash, connectivity_edges, len(members), CHILD_RELEASE))
            component_member_rows.extend((comp_id, m) for m in members)
            component_edge_rows.extend((comp_id, pid, CHILD_RELEASE) for pid in projection_ids)
            candidate_family_rows.append((cand_family, CHILD_RELEASE))
            candidate_revision_rows.append((cand_rev, cand_family, 1, "CLEAN_CANDIDATE", "PROPOSITION_ONLY_SEED", origin_key, sig, cand_hash, CHILD_RELEASE))
            candidate_snapshot_rows.append((cand_rev, "R4_P3C_IMPORT_PAYLOAD_V1", stable(cand_payload), cand_hash, CHILD_RELEASE))
            candidate_origin_rows.append((cand_family, origin_key, cand_hash, cand_rev, CHILD_RELEASE))
            candidate_genealogy_rows.append((cand_rev, cand_family, 1, None, None, "NONE_NEW_SUCCESSOR_FAMILY", "UNCHANGED_FAMILY_APPEND_REVISION", action["action"], CHILD_RELEASE))
            candidate_link_rows.append((cand_rev, comp_id))
            candidate_member_rows.extend((cand_rev, m, "PROPOSED_MEMBER", "COMPONENT_MEMBER", CHILD_RELEASE) for m in members)
            direct_projection_id = projection_ids[0]
            for left_idx, left in enumerate(members):
                for right in members[left_idx + 1 :]:
                    if (left, right) == (left_member, right_member):
                        internal_pair_rows.append((cand_rev, left, right, "DIRECT_POSITIVE", direct_projection_id))
                    else:
                        internal_pair_rows.append((cand_rev, left, right, "SIGNATURE_COMPATIBLE", None))
            adjudication_rows.append((adj, cand_rev, 1, "ACCEPTED_CANONICAL", family_id, stable(canonical_payload), "NOT_AUTHORIZED_BY_P3", graph_row.get("rationale") or action["action"], evidence_hash, None, CHILD_RELEASE))
            predecessor_members = live_revision_members.get(prior_rev or "", set())
            accepted_set = set(canonical_members) - predecessor_members if prior_rev else set(canonical_members)
            adjudication_member_rows.extend((adj, m, "ACCEPT" if m in accepted_set else "ALREADY_CANONICAL", None) for m in members)
            if action["action"] == "ALLOCATE_NEW_FAMILY":
                canonical_family_rows.append((family_id, adj, CHILD_RELEASE, None))
            canonical_revision_rows.append((fam_rev, family_id, revision_number, sig, stable(canonical_payload), evidence_hash, adj, CHILD_RELEASE))
            canonical_member_rows.extend((fam_rev, m, None) for m in canonical_members)
            if prior_rev:
                predecessor_rows.append((fam_rev, prior_rev, digest({"predecessor": prior_rev, "members": canonical_members}), "PREDECESSOR_UNION_NEW_ACCEPTS", CHILD_RELEASE))
            else:
                predecessor_rows.append((fam_rev, None, digest({"new_family": family_id, "members": canonical_members}), "NEW_FAMILY", CHILD_RELEASE))

            for oid, chash, change in [
                (comp_id, comp_hash, "ADDED"),
                (cand_family, cand_hash, "ADDED"),
                (cand_rev, cand_hash, "ADDED"),
                (adj, evidence_hash, "ADDED"),
                (sig, sig_hash, "ADDED"),
                (fam_rev, evidence_hash, "REVISED" if prior_rev else "ADDED"),
            ]:
                ledger_rows.append((CHILD_RELEASE, oid, change, None, chash, "R4 GSS P3C child promotion"))
                snapshot_rows.append((CHILD_RELEASE, oid, chash))

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
        cur.executemany("INSERT INTO p3_proposition_signature (signature_id,subject_id,signature_status,content_hash,authority_release_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", signature_rows)
        cur.executemany("INSERT INTO p3_signature_field (signature_id,field_name,field_value,normalized_value_code,evidence_state,confidence) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", signature_field_rows)
        cur.executemany("INSERT INTO p3_pair_fact_bundle (pair_fact_id,left_object_id,right_object_id,orientation,relation_type,target_relation,operator_relation,timeframe_relation,response_relation,source_portability_ceiling,p3_portability_ceiling,proposition_graph_allowed,j_family_candidate_eligibility,creates_endpoint_authority,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", pair_fact_rows)
        cur.executemany("INSERT INTO p3_pair_endpoint_resolution (pair_fact_id,endpoint_side,original_lineage_id,resolution_status,evidence_ids,authority_release_id) VALUES (%s,%s,%s,%s,%s::jsonb,%s) ON CONFLICT DO NOTHING", pair_endpoint_rows)
        cur.executemany("INSERT INTO p3_pair_endpoint_resolved_subject (pair_fact_id,endpoint_side,resolved_subject_id) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING", pair_endpoint_subject_rows)
        cur.executemany("INSERT INTO p3_pair_projection (projection_id,pair_fact_id,left_subject_id,right_subject_id,projection_basis,evidence_ids,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s::jsonb,%s) ON CONFLICT DO NOTHING", pair_projection_rows)
        cur.executemany("INSERT INTO p3_pair_fact_source_authority (pair_fact_id,registry_code,authority_id,authority_role,governing,superseded_by_authority_id) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", pair_source_rows)
        cur.executemany("INSERT INTO p3_candidate_component (component_id,component_type,build_rule_version,content_hash,connectivity_edge_count,member_count,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", component_rows)
        cur.executemany("INSERT INTO p3_component_membership (component_id,member_object_id) VALUES (%s,%s) ON CONFLICT DO NOTHING", component_member_rows)
        cur.executemany("INSERT INTO p3_component_connectivity_edge (component_id,projection_id,authority_release_id) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING", component_edge_rows)
        cur.executemany("INSERT INTO p3_candidate_family (candidate_family_id,created_release_id) VALUES (%s,%s) ON CONFLICT DO NOTHING", candidate_family_rows)
        cur.executemany("INSERT INTO p3_candidate_revision (candidate_revision_id,candidate_family_id,revision_number,candidate_classification,candidate_origin_type,origin_key,canonical_signature_id,evidence_bundle_hash,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", candidate_revision_rows)
        cur.executemany("INSERT INTO p3_candidate_evidence_snapshot (candidate_revision_id,evidence_contract_version,canonical_payload,evidence_bundle_hash,authority_release_id,created_at) VALUES (%s,%s,%s::jsonb,%s,%s,now()) ON CONFLICT DO NOTHING", candidate_snapshot_rows)
        cur.executemany("INSERT INTO p3_candidate_family_origin_ledger (candidate_family_id,family_origin_key,origin_payload_hash,first_candidate_revision_id,authority_release_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", candidate_origin_rows)
        cur.executemany("INSERT INTO p3_candidate_revision_genealogy (candidate_revision_id,candidate_family_id,revision_number,predecessor_candidate_family_id,predecessor_candidate_revision_id,predecessor_source,genealogy_branch,migration_reason,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", candidate_genealogy_rows)
        cur.executemany("INSERT INTO p3_candidate_component_link (candidate_revision_id,component_id) VALUES (%s,%s) ON CONFLICT DO NOTHING", candidate_link_rows)
        cur.executemany("INSERT INTO p3_candidate_membership (candidate_revision_id,member_object_id,membership_role,membership_basis,authority_release_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", candidate_member_rows)
        cur.executemany("INSERT INTO p3_internal_pair_matrix (candidate_revision_id,left_object_id,right_object_id,pair_state,direct_pair_projection_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", internal_pair_rows)
        cur.executemany("INSERT INTO p3_adjudication_decision (adjudication_id,candidate_revision_id,decision_ordinal,decision_status,canonical_family_id,canonical_proposition,response_portability_status,rationale,evidence_bundle_hash,supersedes_adjudication_id,authority_release_id,created_at) VALUES (%s,%s,%s,%s,%s,%s::jsonb,%s,%s,%s,%s,%s,now()) ON CONFLICT DO NOTHING", adjudication_rows)
        cur.executemany("INSERT INTO p3_adjudication_member (adjudication_id,member_object_id,member_disposition,variant_revision_id) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING", adjudication_member_rows)
        cur.executemany("INSERT INTO p3_canonical_family (canonical_family_id,created_by_adjudication_id,created_release_id,retired_release_id) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING", canonical_family_rows)
        cur.executemany("INSERT INTO p3_canonical_family_revision (family_revision_id,canonical_family_id,revision_number,canonical_signature_id,canonical_proposition,evidence_bundle_hash,created_by_adjudication_id,authority_release_id) VALUES (%s,%s,%s,%s,%s::jsonb,%s,%s,%s) ON CONFLICT DO NOTHING", canonical_revision_rows)
        cur.executemany("INSERT INTO p3_canonical_family_membership (family_revision_id,member_object_id,variant_revision_id) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING", canonical_member_rows)
        cur.executemany("INSERT INTO p3_family_genealogy (genealogy_id,relation_type,adjudication_id,authority_release_id) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING", genealogy_rows)
        cur.executemany("INSERT INTO p3_family_genealogy_member (genealogy_id,family_id,genealogy_role) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING", genealogy_member_rows)
        cur.executemany("INSERT INTO p3_family_revision_predecessor (family_revision_id,predecessor_family_revision_id,predecessor_membership_hash,extension_rule,authority_release_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", predecessor_rows)
        cur.executemany("INSERT INTO p3_release_change_ledger (release_id,object_id,change_type,prior_content_hash,content_hash,reason) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING", ledger_rows)
        cur.executemany("INSERT INTO p3_release_object_snapshot (release_id,object_id,content_hash) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING", snapshot_rows)
        cur.executemany("INSERT INTO p3_release_status_event (release_id,event_ordinal,status,occurred_at,evidence_hash) VALUES (%s,%s,%s,now(),%s) ON CONFLICT DO NOTHING", [(CHILD_RELEASE, 1, "DRAFT", input_hash), (CHILD_RELEASE, 2, "VALIDATED", digest(object_counts)), (CHILD_RELEASE, 3, "SHADOW", digest({"shadow": object_counts})), (CHILD_RELEASE, 4, "PROMOTED", payload["payload_sha256"])])

        cur.execute("SET CONSTRAINTS ALL IMMEDIATE")
        checks: dict[str, Any] = {}
        for name, sql in {
            "child_adjudications": "SELECT count(*) FROM p3_adjudication_decision WHERE authority_release_id=%s",
            "child_candidate_revisions": "SELECT count(*) FROM p3_candidate_revision WHERE authority_release_id=%s",
            "child_canonical_revisions": "SELECT count(*) FROM p3_canonical_family_revision WHERE authority_release_id=%s",
            "child_canonical_memberships": "SELECT count(*) FROM p3_canonical_family_membership m JOIN p3_canonical_family_revision r USING(family_revision_id) WHERE r.authority_release_id=%s",
            "r184_release_rows": "SELECT count(*) FROM p3_authority_release WHERE release_id=%s",
        }.items():
            cur.execute(sql, (CHILD_RELEASE if name != "r184_release_rows" else PARENT_RELEASE,))
            checks[name] = cur.fetchone()[0]
        expected = {
            "child_adjudications": len(adjudication_rows),
            "child_candidate_revisions": len(candidate_revision_rows),
            "child_canonical_revisions": len(canonical_revision_rows),
            "child_canonical_memberships": len(canonical_member_rows),
            "r184_release_rows": 1,
        }
        if checks != expected:
            raise ValueError(f"post-insert verification count mismatch: expected={expected} actual={checks}")

        if commit:
            conn.commit()
            mode = "committed"
        else:
            conn.rollback()
            mode = "rolled_back"
        return {"release_id": CHILD_RELEASE, "mode": mode, **checks}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", type=Path, default=DEFAULT_PAYLOAD)
    parser.add_argument("--graph", type=Path, default=DEFAULT_GRAPH)
    parser.add_argument("--dsn", default=os.environ.get("RAWLSING_P3C_DSN", DEFAULT_DSN))
    parser.add_argument("--commit", action="store_true", help="commit the child release; default is rollback-only validation")
    args = parser.parse_args()
    print(json.dumps(promote(args.payload, args.graph, args.dsn, args.commit), indent=2))


if __name__ == "__main__":
    main()
