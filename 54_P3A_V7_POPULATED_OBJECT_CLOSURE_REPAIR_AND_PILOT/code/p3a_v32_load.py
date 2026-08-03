from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import psycopg


RELEASE_ID = "P3-AUTHORITY-2026-08-01-R31"
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
        cur.execute(
            """
            INSERT INTO p3_vocabulary_code
              (vocabulary_domain,code,introduced_release_id,retired_release_id)
            VALUES ('adjudication_member_disposition','SPLIT',%s,NULL)
            ON CONFLICT (vocabulary_domain,code) DO NOTHING
            """,
            (RELEASE_ID,),
        )
        cur.execute(
            """
            INSERT INTO p3_vocabulary_revision
              (vocabulary_domain,code,authority_release_id,label,definition,authority_effect,deprecated)
            VALUES ('adjudication_member_disposition','SPLIT',%s,'SPLIT','Member is assigned to a split successor in a split-required adjudication.','GOVERNS_ADJUDICATION_MEMBER_DISPOSITION',false)
            ON CONFLICT (vocabulary_domain,code,authority_release_id) DO NOTHING
            """,
            (RELEASE_ID,),
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
            [(r["from_status"], r["to_status"], r["guard"], RELEASE_ID) for r in rel_life if r["from_status"]],
        )
        for r in rel_life:
            if not r["from_status"]:
                cur.execute(
                    """
                    INSERT INTO p3_release_lifecycle_transition
                      (from_status,to_status,guard_text,authority_release_id)
                    SELECT NULL,%s,%s,%s
                    WHERE NOT EXISTS (
                      SELECT 1 FROM p3_release_lifecycle_transition
                      WHERE from_status IS NULL AND to_status=%s AND authority_release_id=%s
                    )
                    """,
                    (r["to_status"], r["guard"], RELEASE_ID, r["to_status"], RELEASE_ID),
                )
        cur.execute("CALL p3_install_contract_triggers(%s)", (RELEASE_ID,))
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
    lineage_rel = lineage_path.relative_to(root).as_posix()
    lineage_hash = sha256_file(lineage_path)
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
        object_rows.append((lineage_id, "IMPORTED_SOURCE_LOCAL_LINEAGE", "INHERITED_UPSTREAM_ID", lineage_id, "P2_GLOBAL", lineage_id, RELEASE_ID, None, None, "Inherited exact P2 source-local lineage ID."))
        upstream_rows.append((lineage_id, "P2_GLOBAL", source_family, "KNOWN", "SOURCE_LOCAL_LINEAGE", lineage_id, lineage_rel, lineage_hash, "P2_SOURCE_LOCAL_LINEAGE_REGISTRY"))
        members = json.loads(row["member_question_implementation_ids_json"])
        for ordinal, impl_id in enumerate(members):
            if impl_id not in seen_impl:
                seen_impl.add(impl_id)
                object_rows.append((impl_id, "IMPORTED_IMPLEMENTATION", "INHERITED_UPSTREAM_ID", impl_id, "P2_GLOBAL", impl_id, RELEASE_ID, None, None, "Inherited exact P2 question implementation ID."))
                upstream_rows.append((impl_id, "P2_GLOBAL", source_family, "KNOWN", "QUESTION_IMPLEMENTATION", impl_id, lineage_rel, lineage_hash, "P2_SOURCE_LOCAL_LINEAGE_REGISTRY"))
            membership_rows.append((lineage_id, impl_id, ordinal, lineage_id, RELEASE_ID))
        b = baseline[lineage_id]
        participation_rows.append((lineage_id, b["participation_status"], int(b["effective_pair_incident_count"]), int(b["proposition_pair_incident_count"]), b["signature_requirement"], b["authority_note"] or None, RELEASE_ID))
        status = "CONSTRAINT_ONLY_PRESERVED" if b["participation_status"] == "CONSTRAINT_ONLY_INCIDENT" else "UNADJUDICATED"
        reason = "Initial P3A lineage state from corrected participation baseline."
        disposition_rows.append((lineage_id, "IMPORTED_SOURCE_LOCAL_LINEAGE", status, reason, None, json.dumps([lineage_id]), RELEASE_ID))

    with psycopg.connect(dsn, autocommit=False) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public")
        cur = conn.cursor()
        execute_values(cur, """INSERT INTO p3_object_registry (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,allocation_release_id,retired_release_id,content_hash,stable_identity_note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (object_id) DO NOTHING""", object_rows)
        execute_values(cur, """INSERT INTO p3_upstream_object_reference (object_id,upstream_phase,source_family,license_provenance_state,upstream_object_type,upstream_object_id,authority_artifact,authority_hash,license_provenance_ref) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", upstream_rows)
        execute_values(cur, """INSERT INTO p3_imported_lineage_membership (lineage_id,implementation_id,ordinal_position,source_authority_id,authority_release_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", membership_rows)
        execute_values(cur, """INSERT INTO p3_lineage_participation (lineage_id,participation_status,effective_pair_incident_count,proposition_pair_incident_count,signature_requirement,authority_note,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", participation_rows)
        execute_values(cur, """INSERT INTO p3_lineage_disposition (subject_id,subject_type,disposition_status,reason,canonical_family_id,evidence_ids,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s::jsonb,%s) ON CONFLICT DO NOTHING""", disposition_rows)
        conn.commit()
    return {
        "lineage_objects": len(lineages),
        "implementation_objects": len(seen_impl),
        "membership_rows": len(membership_rows),
        "participation_rows": len(participation_rows),
        "disposition_rows": len(disposition_rows),
    }


def content_id(prefix: str, obj: dict) -> tuple[str, str]:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    h = sha256_text(payload)
    return f"{prefix}-{h[:16]}", h


def load_pair_facts(root: Path, dsn: str) -> dict:
    sec = root / "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK"
    eff = rows(sec / "upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE_v7.csv")
    src_rows = rows(sec / "upstream/P3_EFFECTIVE_PAIR_SOURCE_AUTHORITY_SURFACE_v7.csv")
    prop = {r["pair_key"]: r for r in rows(sec / "upstream/P3_PROPOSITION_RELATION_ELIGIBILITY_PREFLIGHT_v7.csv")}
    pair_by_key = {}
    obj_rows = []
    bundle_rows = []
    endpoint_rows = []
    endpoint_subject_rows = []
    projection_obj_rows = []
    projection_rows = []
    source_rows = []
    def relation_type(r):
        if r["pair_key"] in prop:
            return prop[r["pair_key"]]["p3_relation_type"]
        cls = r["normalized_authority_class"]
        if cls == "NEGATIVE_AUTHORITY": return "EXPLICIT_NEGATIVE"
        if cls == "REDIRECTED_OTHER_DOMAIN_AUTHORITY": return "REDIRECT_OTHER_DOMAIN"
        if cls == "UNRESOLVED_FAIL_CLOSED_AUTHORITY" or cls == "UNRESOLVED_EXACT_FOUNDATION_AUTHORITY": return "UNRESOLVED"
        if cls == "COORDINATE_OR_BOUNDED_RELATION_AUTHORITY" or cls == "ACCEPTED_EXACT_FOUNDATION_AUTHORITY": return "CONSTRUCT_COORDINATE"
        if cls == "REJECTED_EXACT_FOUNDATION_AUTHORITY": return "EXPLICIT_NEGATIVE"
        return "CONSTRUCT_COORDINATE"
    def p3_ceiling(r, rel):
        if rel == "PROPOSITION_RESPONSE_IDENTITY": return "QUESTION_PROPOSITION_AND_RESPONSE_CONTRACT"
        if rel == "PROPOSITION_IDENTITY_ONLY": return "QUESTION_PROPOSITION_ONLY"
        c=r["source_portability_ceiling"]
        if c in {"QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY","QUESTION_PROPOSITION_ONLY","DOMAIN_COORDINATE_ONLY","NO_POSITIVE_AUTHORITY"}: return c
        if c in {"CONSTRUCT_TARGET_ONLY","CONSTRUCT_OR_CONTEXT_COORDINATE_ONLY","CONSTRUCT_TARGET_COORDINATE_ONLY","CONTEXT_OR_POSITION_COORDINATE_ONLY","TARGET_AND_RELATION_COORDINATE_ONLY","DERIVED_INDEX_CONSTRUCT_ONLY","TARGET_AND_TRUST_DOMAIN_COORDINATE_ONLY"}: return "CONSTRUCT_TARGET_COORDINATE_ONLY"
        if c in {"TARGET_RELATION_AXIS_ONLY_NO_VALUE_PORTABILITY","TARGET_AND_CONTEXT_FUNCTION_ONLY","METADATA_FUNCTION_ONLY"}: return "HIERARCHICAL_ONLY"
        return "NO_POSITIVE_AUTHORITY"
    for r in eff:
        rel=relation_type(r)
        pfid,h=content_id("P3PF", {"pair_key":r["pair_key"],"authority":r["governing_authority_id"],"left":r["left_lineage_id"],"right":r["right_lineage_id"],"relation":rel})
        pair_by_key[r["pair_key"]]=pfid
        obj_rows.append((pfid,"PAIR_FACT","CONTENT_ADDRESSED_DERIVED_ID",pfid,"P3A_PAIR_NORMALIZATION",r["governing_authority_id"],RELEASE_ID,None,h,"Content-addressed P3 pair fact from effective P2 authority."))
        allowed = r["pair_key"] in prop and prop[r["pair_key"]]["proposition_graph_allowed"] == "YES"
        elig = prop[r["pair_key"]]["provisional_j_family_eligibility"] if r["pair_key"] in prop else "NONCONNECTIVE"
        bundle_rows.append((pfid,r["left_lineage_id"],r["right_lineage_id"],"DIRECTIONAL",rel,None,None,None,None,r["source_portability_ceiling"],p3_ceiling(r,rel),allowed,elig,False,RELEASE_ID))
        for side, lid in [("LEFT", r["left_lineage_id"]),("RIGHT", r["right_lineage_id"] )]:
            endpoint_rows.append((pfid,side,lid,"ORIGINAL_LINEAGE",json.dumps([r["governing_authority_id"]]),RELEASE_ID))
            endpoint_subject_rows.append((pfid,side,lid))
        if allowed and elig == "J_FAMILY_CANDIDATE_ELIGIBLE":
            proj_id,ph=content_id("P3PROJ", {"pair_fact_id":pfid,"left":r["left_lineage_id"],"right":r["right_lineage_id"],"release":RELEASE_ID})
            projection_obj_rows.append((proj_id,"PAIR_PROJECTION","CONTENT_ADDRESSED_DERIVED_ID",proj_id,"P3A_PAIR_PROJECTION",pfid,RELEASE_ID,None,ph,"Projection over original lineage endpoints."))
            projection_rows.append((proj_id,pfid,r["left_lineage_id"],r["right_lineage_id"],"ORIGINAL_LINEAGES",json.dumps([r["governing_authority_id"]]),RELEASE_ID))
    for r in src_rows:
        pfid=pair_by_key[r["pair_key"]]
        gov = r["authority_role"] == "GOVERNING"
        source_rows.append((pfid,r["registry_code"],r["authority_id"],r["authority_role"],gov,r["superseded_by_authority_id"] or None))
    with psycopg.connect(dsn, autocommit=False) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public")
        cur=conn.cursor()
        execute_values(cur, """INSERT INTO p3_object_registry (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,allocation_release_id,retired_release_id,content_hash,stable_identity_note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (object_id) DO NOTHING""", obj_rows + projection_obj_rows)
        execute_values(cur, """INSERT INTO p3_pair_fact_bundle (pair_fact_id,left_object_id,right_object_id,orientation,relation_type,target_relation,operator_relation,timeframe_relation,response_relation,source_portability_ceiling,p3_portability_ceiling,proposition_graph_allowed,j_family_candidate_eligibility,creates_endpoint_authority,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", bundle_rows)
        execute_values(cur, """INSERT INTO p3_pair_fact_source_authority (pair_fact_id,registry_code,authority_id,authority_role,governing,superseded_by_authority_id) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", source_rows)
        execute_values(cur, """INSERT INTO p3_pair_endpoint_resolution (pair_fact_id,endpoint_side,original_lineage_id,resolution_status,evidence_ids,authority_release_id) VALUES (%s,%s,%s,%s,%s::jsonb,%s) ON CONFLICT DO NOTHING""", endpoint_rows)
        execute_values(cur, """INSERT INTO p3_pair_endpoint_resolved_subject (pair_fact_id,endpoint_side,resolved_subject_id) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING""", endpoint_subject_rows)
        execute_values(cur, """INSERT INTO p3_pair_projection (projection_id,pair_fact_id,left_subject_id,right_subject_id,projection_basis,evidence_ids,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s::jsonb,%s) ON CONFLICT DO NOTHING""", projection_rows)
        conn.commit()
    return {"pair_facts":len(bundle_rows),"pair_source_authority_rows":len(source_rows),"endpoint_resolution_rows":len(endpoint_rows),"endpoint_subject_rows":len(endpoint_subject_rows),"pair_projections":len(projection_rows)}


SIGNATURE_FIELDS = [
    "subject_role", "operator", "target", "object_or_outcome", "modality", "timeframe",
    "condition", "population_scope", "geographic_scope", "polarity", "derived_status", "parent_context",
]


def load_signatures(root: Path, dsn: str) -> dict:
    sec = root / "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK"
    work = [r for r in rows(sec / "upstream/P3_SIGNATURE_WORKSET_v7.csv") if r["signature_requirement"] == "FULL_P3A_SIGNATURE"]
    obj_rows=[]; sig_rows=[]; field_rows=[]
    for r in work:
        subject=r["lineage_id"]
        fields={name:{"evidence_state":"UNRECOVERED","field_value":None} for name in SIGNATURE_FIELDS}
        sig_id,h=content_id("P3SIG", {"subject_id":subject,"fields":fields,"release":RELEASE_ID})
        obj_rows.append((sig_id,"PROPOSITION_SIGNATURE","CONTENT_ADDRESSED_DERIVED_ID",sig_id,"P3A_SIGNATURE_RECOVERY",subject,RELEASE_ID,None,h,"P3A initial fail-closed proposition signature record."))
        sig_rows.append((sig_id,subject,"PARTIAL_FAIL_CLOSED",h,RELEASE_ID))
        for name in SIGNATURE_FIELDS:
            field_rows.append((sig_id,name,None,None,"UNRECOVERED","NOT_APPLICABLE"))
    with psycopg.connect(dsn, autocommit=False) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public")
        cur=conn.cursor()
        execute_values(cur, """INSERT INTO p3_object_registry (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,allocation_release_id,retired_release_id,content_hash,stable_identity_note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (object_id) DO NOTHING""", obj_rows)
        execute_values(cur, """INSERT INTO p3_proposition_signature (signature_id,subject_id,signature_status,content_hash,authority_release_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", sig_rows)
        execute_values(cur, """INSERT INTO p3_signature_field (signature_id,field_name,field_value,normalized_value_code,evidence_state,confidence) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", field_rows)
        conn.commit()
    return {"signature_subjects":len(work),"signature_rows":len(sig_rows),"signature_field_rows":len(field_rows)}


def load_components(root: Path, dsn: str) -> dict:
    with psycopg.connect(dsn, autocommit=False) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public")
        cur=conn.cursor()
        cur.execute("""
            SELECT pr.projection_id, pr.left_subject_id, pr.right_subject_id
            FROM p3_pair_projection pr JOIN p3_pair_fact_bundle pf USING(pair_fact_id)
            WHERE pf.relation_type='PROPOSITION_RESPONSE_IDENTITY'
            ORDER BY pr.projection_id
        """)
        edges=cur.fetchall()
        adj={}
        for proj,l,r in edges:
            adj.setdefault(l,set()).add(r); adj.setdefault(r,set()).add(l)
        seen=set(); comps=[]
        for n in sorted(adj):
            if n in seen: continue
            stack=[n]; seen.add(n); members=[]
            while stack:
                x=stack.pop(); members.append(x)
                for y in sorted(adj[x]):
                    if y not in seen:
                        seen.add(y); stack.append(y)
            members=sorted(members)
            pedges=[e for e in edges if e[1] in members and e[2] in members]
            comps.append((members,pedges))
        obj_rows=[]; comp_rows=[]; member_rows=[]; edge_rows=[]
        for members,pedges in comps:
            comp_id,h=content_id("P3COMP", {"type":"STRICT_RESPONSE_COMPONENT","members":members,"projections":[e[0] for e in pedges],"release":RELEASE_ID})
            obj_rows.append((comp_id,"CANDIDATE_COMPONENT","CONTENT_ADDRESSED_DERIVED_ID",comp_id,"P3A_COMPONENT_BUILD",None,RELEASE_ID,None,h,"Strict response component from PROPOSITION_RESPONSE_IDENTITY projections."))
            comp_rows.append((comp_id,"STRICT_RESPONSE_COMPONENT","P3A_COMPONENT_BUILD_V31",h,len(pedges),len(members),RELEASE_ID))
            member_rows.extend((comp_id,m) for m in members)
            edge_rows.extend((comp_id,e[0],RELEASE_ID) for e in pedges)
        execute_values(cur, """INSERT INTO p3_object_registry (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,allocation_release_id,retired_release_id,content_hash,stable_identity_note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (object_id) DO NOTHING""", obj_rows)
        execute_values(cur, """INSERT INTO p3_candidate_component (component_id,component_type,build_rule_version,content_hash,connectivity_edge_count,member_count,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", comp_rows)
        execute_values(cur, """INSERT INTO p3_component_membership (component_id,member_object_id) VALUES (%s,%s) ON CONFLICT DO NOTHING""", member_rows)
        execute_values(cur, """INSERT INTO p3_component_connectivity_edge (component_id,projection_id,authority_release_id) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING""", edge_rows)
        conn.commit()
    return {"strict_components":len(comps),"component_membership_rows":len(member_rows),"component_connectivity_edges":len(edge_rows)}



def _member_list(value: str) -> list[str]:
    return sorted(json.loads(value))


def _source_count(cur, members: list[str]) -> int:
    cur.execute("SELECT count(DISTINCT source_family) FROM p3_upstream_object_reference WHERE object_id = ANY(%s)", (members,))
    return int(cur.fetchone()[0])


def _all_projections_between(cur, members: list[str]) -> dict[tuple[str, str], tuple[str, str]]:
    cur.execute(
        """
        SELECT projection_id,left_subject_id,right_subject_id
        FROM p3_pair_projection
        WHERE left_subject_id = ANY(%s) AND right_subject_id = ANY(%s)
        ORDER BY projection_id
        """,
        (members, members),
    )
    return {tuple(sorted((l, r))): (pid, pid) for pid, l, r in cur.fetchall()}


def _proposition_projection_ids(root: Path) -> dict[tuple[str, str], str]:
    sec = root / "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK"
    out = {}
    for r in rows(sec / "upstream/P3_PROPOSITION_ONLY_TOPOLOGY_CLASSIFICATION_v7.csv"):
        key = tuple(sorted((r["left_lineage_id"], r["right_lineage_id"])))
        pid, _ = content_id("P3PROJ", {"pair_fact_id": content_id("P3PF", {"pair_key":r["pair_key"],"authority":r["governing_authority_id"],"left":r["left_lineage_id"],"right":r["right_lineage_id"],"relation":"PROPOSITION_IDENTITY_ONLY"})[0], "left":r["left_lineage_id"], "right":r["right_lineage_id"], "release":RELEASE_ID})
        out[key] = pid
    return out


def load_candidates(root: Path, dsn: str) -> dict:
    sec = root / "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK"
    inventory = rows(sec / "upstream/P3_PREFLIGHT_CANDIDATE_INVENTORY_v7.csv")
    prop_projection_by_pair = _proposition_projection_ids(root)
    with psycopg.connect(dsn, autocommit=False) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public")
        cur=conn.cursor()
        cur.execute("SELECT component_id, component_type FROM p3_candidate_component ORDER BY component_id")
        existing_components=cur.fetchall()
        component_members={}
        for comp_id, comp_type in existing_components:
            cur.execute("SELECT member_object_id FROM p3_component_membership WHERE component_id=%s ORDER BY member_object_id", (comp_id,))
            component_members[comp_id]=(comp_type, [r[0] for r in cur.fetchall()])
        strict_by_members={tuple(v[1]): k for k,v in component_members.items() if v[0]=='STRICT_RESPONSE_COMPONENT'}
        next_component_index=len(component_members)+1
        obj_rows=[]; family_rows=[]; rev_rows=[]; link_rows=[]; member_rows=[]; matrix_rows=[]; event_rows=[]; ranking_rows=[]
        comp_obj_rows=[]; comp_rows=[]; comp_member_rows=[]; comp_edge_rows=[]
        attach_rows=[]; obligation_obj_rows=[]; obligation_rows=[]; closure_link_rows=[]; response_obj_rows=[]; response_rows=[]; exclusion_obj_rows=[]; exclusion_rows=[]
        topology_counts={}
        for idx,r in enumerate(inventory, start=1):
            origin=r["candidate_origin_type"]
            topology_counts[origin]=topology_counts.get(origin,0)+1
            members=_member_list(r["member_ids_json"])
            cand_id=f"P3CAND-{idx:06d}"
            rev_id=f"P3CANDREV-{idx:06d}-R0001"
            origin_key=r["origin_key"]
            candidate_component_ids=[]
            candidate_attachment_projection_ids=[]
            basis_by_member={m:"COMPONENT_MEMBER" for m in members}
            if origin == "STRICT_RESPONSE_COMPONENT":
                comp_id=strict_by_members[tuple(members)]
                candidate_component_ids.append(comp_id)
            elif origin == "PROPOSITION_ONLY_SEED":
                projection_ids=[]
                for i,l in enumerate(members):
                    for rr in members[i+1:]:
                        pid=prop_projection_by_pair.get(tuple(sorted((l,rr))))
                        if pid:
                            projection_ids.append(pid)
                if not projection_ids:
                    raise RuntimeError(f"no proposition-only projections for {r['preflight_candidate_key']}")
                comp_id, comp_hash = content_id("P3COMP", {"type":"PROPOSITION_ONLY_COMPONENT","members":members,"projections":sorted(projection_ids),"release":RELEASE_ID})
                candidate_component_ids.append(comp_id)
                comp_obj_rows.append((comp_id,"CANDIDATE_COMPONENT","CONTENT_ADDRESSED_DERIVED_ID",comp_id,"P3A_V32_TOPOLOGY_BUILD",None,RELEASE_ID,None,comp_hash,"Proposition-only component from full preflight topology."))
                comp_rows.append((comp_id,"PROPOSITION_ONLY_COMPONENT","P3A_V32_PROPOSITION_ONLY_TOPOLOGY",comp_hash,len(set(projection_ids)),len(members),RELEASE_ID))
                comp_member_rows.extend((comp_id,m) for m in members)
                comp_edge_rows.extend((comp_id,pid,RELEASE_ID) for pid in sorted(set(projection_ids)))
            elif origin == "ATTACHMENT_REVIEW":
                linked=[]
                for comp_id,(comp_type,cmembers) in component_members.items():
                    if comp_type == 'STRICT_RESPONSE_COMPONENT' and set(cmembers).issubset(set(members)):
                        linked.append((comp_id,cmembers))
                if not linked:
                    # Attach-only singleton meta-node represented as diagnostic origin member set with attachments.
                    linked=[]
                candidate_component_ids.extend(comp_id for comp_id,_ in linked)
                covered=set().union(*(set(x[1]) for x in linked)) if linked else set()
                projection_ids=[]
                for i,l in enumerate(members):
                    for rr in members[i+1:]:
                        pid=prop_projection_by_pair.get(tuple(sorted((l,rr))))
                        if pid and ({l,rr} - covered or l not in covered or rr not in covered):
                            projection_ids.append(pid)
                if not projection_ids:
                    for i,l in enumerate(members):
                        for rr in members[i+1:]:
                            pid=prop_projection_by_pair.get(tuple(sorted((l,rr))))
                            if pid:
                                projection_ids.append(pid)
                if not projection_ids:
                    raise RuntimeError(f"no attachment projections for {r['preflight_candidate_key']}")
                candidate_attachment_projection_ids=sorted(set(projection_ids))
                for m in members:
                    if m not in covered:
                        basis_by_member[m]="ATTACHMENT_PROJECTION"
                attach_rows.extend((rev_id,pid,"ORPHAN_ATTACHMENT",RELEASE_ID) for pid in candidate_attachment_projection_ids)
            else:
                raise RuntimeError(f"unsupported candidate origin {origin}")
            obj_rows.append((cand_id,"CANDIDATE_FAMILY","REGISTRY_ALLOCATED_DURABLE_ID",origin_key,"P3A_V32_CANDIDATE_BUILD",r["preflight_candidate_key"],RELEASE_ID,None,None,"Durable candidate family allocated from full preflight topology."))
            obj_rows.append((rev_id,"CANDIDATE_REVISION","REGISTRY_ALLOCATED_DURABLE_ID",f"{cand_id}:R0001","P3A_V32_CANDIDATE_BUILD",cand_id,RELEASE_ID,None,None,"Candidate revision 1 from full preflight topology."))
            family_rows.append((cand_id,RELEASE_ID))
            link_rows.extend((rev_id,comp_id) for comp_id in candidate_component_ids)
            member_rows.extend((rev_id,m,"PROPOSED_MEMBER",basis_by_member[m],RELEASE_ID) for m in members)
            projections=_all_projections_between(cur, members)
            direct_positive=0; unruled=0
            revision_obligations=[]
            for i,l in enumerate(members):
                for rr in members[i+1:]:
                    key=tuple(sorted((l,rr)))
                    pid_tuple=projections.get(key)
                    if pid_tuple and key in prop_projection_by_pair and prop_projection_by_pair[key] == pid_tuple[0] and origin != "STRICT_RESPONSE_COMPONENT":
                        # Proposition-only evidence can create attachment/review support but does not merge strict response candidates.
                        matrix_rows.append((rev_id,key[0],key[1],"DIRECT_POSITIVE",pid_tuple[0]))
                        direct_positive+=1
                    elif pid_tuple and key not in prop_projection_by_pair:
                        matrix_rows.append((rev_id,key[0],key[1],"DIRECT_POSITIVE",pid_tuple[0]))
                        direct_positive+=1
                    else:
                        matrix_rows.append((rev_id,key[0],key[1],"UNRULED",None))
                        unruled+=1
                        close_id, close_hash=content_id("P3CLOSE", {"candidate_revision_id":rev_id,"left":key[0],"right":key[1],"type":"UNRULED_INTERNAL_PAIR","release":RELEASE_ID})
                        obligation_obj_rows.append((close_id,"CLOSURE_OBLIGATION","CONTENT_ADDRESSED_DERIVED_ID",close_id,"P3A_V32_CLOSURE_REPAIR",rev_id,RELEASE_ID,None,close_hash,"Open closure obligation for unruled internal pair."))
                        obligation_rows.append((close_id,rev_id,key[0],key[1],"UNRULED_INTERNAL_PAIR","OPEN",None,RELEASE_ID))
                        closure_link_rows.append((rev_id,key[0],key[1],close_id))
                        revision_obligations.append(close_id)
            source_count=_source_count(cur,members)
            density=direct_positive/max(1,(len(members)*(len(members)-1)//2))
            classification="INSUFFICIENT_AUTHORITY_RISK" if unruled else "CLEAN_CANDIDATE"
            if origin == "ATTACHMENT_REVIEW": classification="SPLIT_RISK" if unruled else "VARIANT_BEARING_CANDIDATE"
            evid_hash=sha256_text(f"v32-candidate-evidence-placeholder|{rev_id}|{origin_key}|{unruled}|{direct_positive}")
            rev_rows.append((rev_id,cand_id,1,classification,origin,origin_key,None,evid_hash,RELEASE_ID))
            event_rows.append((cand_id,rev_id,1,None,"DISCOVERED","P3A_V32_CANDIDATE_BUILD", "2026-08-01T00:00:00Z", RELEASE_ID))
            ranking_rows.append((rev_id,idx,0,unruled,0,source_count,len(members),density,direct_positive,0,RELEASE_ID))
            for m in members:
                ref_id, ref_hash=content_id("P3RCR", {"subject_id":m,"release":RELEASE_ID,"topology":"UNKNOWN"})
                response_obj_rows.append((ref_id,"RESPONSE_CONTRACT_REFERENCE","CONTENT_ADDRESSED_DERIVED_ID",ref_id,"P3A_V32_RESPONSE_REFERENCE",m,RELEASE_ID,None,ref_hash,"Fail-closed response-contract reference persisted for packet reconstruction."))
                response_rows.append((ref_id,m,None,"UNKNOWN",None,"section-54-live-db-governed-fail-closed-reference",False,RELEASE_ID))
            exc_id=f"P3EXC-{idx:06d}"
            exclusion_obj_rows.append((exc_id,"FAMILY_EXCLUSION","REGISTRY_ALLOCATED_DURABLE_ID",exc_id,"P3A_V32_CANDIDATE_BUILD",rev_id,RELEASE_ID,None,None,"Candidate-owned rule exclusion for P3A non-authority adjudication boundary."))
            exclusion_rows.append((exc_id,cand_id,"RULE_BASED","P3C_AUTOMATIC_CANONICAL_ACCEPTANCE","P3A candidates require human P3C adjudication before canonical acceptance.","candidate_family",True,RELEASE_ID))
        execute_values(cur, """INSERT INTO p3_object_registry (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,allocation_release_id,retired_release_id,content_hash,stable_identity_note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (object_id) DO NOTHING""", comp_obj_rows + obj_rows + obligation_obj_rows + response_obj_rows + exclusion_obj_rows)
        execute_values(cur, """INSERT INTO p3_candidate_component (component_id,component_type,build_rule_version,content_hash,connectivity_edge_count,member_count,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", comp_rows)
        execute_values(cur, """INSERT INTO p3_component_membership (component_id,member_object_id) VALUES (%s,%s) ON CONFLICT DO NOTHING""", comp_member_rows)
        execute_values(cur, """INSERT INTO p3_component_connectivity_edge (component_id,projection_id,authority_release_id) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING""", comp_edge_rows)
        execute_values(cur, """INSERT INTO p3_candidate_family (candidate_family_id,created_release_id) VALUES (%s,%s) ON CONFLICT DO NOTHING""", family_rows)
        execute_values(cur, """INSERT INTO p3_candidate_revision (candidate_revision_id,candidate_family_id,revision_number,candidate_classification,candidate_origin_type,origin_key,canonical_signature_id,evidence_bundle_hash,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", rev_rows)
        execute_values(cur, """INSERT INTO p3_candidate_component_link (candidate_revision_id,component_id) VALUES (%s,%s) ON CONFLICT DO NOTHING""", link_rows)
        execute_values(cur, """INSERT INTO p3_candidate_attachment_projection (candidate_revision_id,projection_id,attachment_role,authority_release_id) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING""", attach_rows)
        execute_values(cur, """INSERT INTO p3_candidate_membership (candidate_revision_id,member_object_id,membership_role,membership_basis,authority_release_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", member_rows)
        execute_values(cur, """INSERT INTO p3_internal_pair_matrix (candidate_revision_id,left_object_id,right_object_id,pair_state,direct_pair_projection_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", matrix_rows)
        execute_values(cur, """INSERT INTO p3_closure_obligation (closure_obligation_id,candidate_revision_id,left_object_id,right_object_id,obligation_type,status,resolution_adjudication_id,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", obligation_rows)
        execute_values(cur, """INSERT INTO p3_internal_pair_closure (candidate_revision_id,left_object_id,right_object_id,closure_obligation_id) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING""", closure_link_rows)
        execute_values(cur, """INSERT INTO p3_response_contract_reference (reference_id,subject_id,upstream_response_contract_id,response_topology,response_contract_hash,authority_artifact,p4_authority,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", response_rows)
        execute_values(cur, """INSERT INTO p3_family_exclusion (exclusion_id,owner_object_id,exclusion_type,prohibited_operation,evidence_or_rule,scope,tested_surface_complete,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", exclusion_rows)
        execute_values(cur, """INSERT INTO p3_candidate_status_event (candidate_family_id,candidate_revision_id,event_ordinal,from_stage,to_stage,guard_evidence_id,occurred_at,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", event_rows)
        execute_values(cur, """INSERT INTO p3_candidate_ranking (candidate_revision_id,primary_class_rank,hard_collision_count,open_obligation_count,signature_completeness,source_count,lineage_count,direct_positive_density,structure_support_count,response_variant_complexity,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", ranking_rows)
        conn.commit()
    return {"candidate_families":len(family_rows),"candidate_revisions":len(rev_rows),"candidate_memberships":len(member_rows),"internal_pair_rows":len(matrix_rows),"unruled_internal_pairs":len(obligation_rows),"closure_obligations":len(obligation_rows),"closure_links":len(closure_link_rows),"response_references":len(response_rows),"candidate_exclusions":len(exclusion_rows),"origin_counts":topology_counts,"status":"PASS"}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--dsn", required=True)
    ap.add_argument("--phase", required=True, choices=["contracts", "membership", "pairs", "signatures", "components", "candidates"])
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    root = Path(args.root)
    if args.phase == "contracts":
        result = load_contracts(root, args.dsn)
    elif args.phase == "membership":
        result = load_imported_membership(root, args.dsn)
    elif args.phase == "pairs":
        result = load_pair_facts(root, args.dsn)
    elif args.phase == "signatures":
        result = load_signatures(root, args.dsn)
    elif args.phase == "components":
        result = load_components(root, args.dsn)
    else:
        result = load_candidates(root, args.dsn)
    result["status"] = "PASS"
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
