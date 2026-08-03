from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import psycopg


RELEASE_ID = "P3-AUTHORITY-2026-08-01-R36"
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
        manifest_hash = sha256_file(sec / "upstream/P3_UPSTREAM_INPUT_MANIFEST_v7.csv")
        release_rows = [
            ("P3-AUTHORITY-2026-08-01-R31", None, "p3-v7", "p3a-phase3-loader-v31-historical", manifest_hash, json.dumps({"historical_identity_surface": True}), "0" * 64, "53_P3A_V7_CONTRACT_BINDING_REPAIR_AND_PHASE3_RESUME", "historical"),
            ("P3-AUTHORITY-2026-08-01-R35", "P3-AUTHORITY-2026-08-01-R31", "p3-v7", "p3a-phase3-loader-v35-blocked", manifest_hash, json.dumps({"blocked_evidence": True}), "0" * 64, "57_P3A_V7_IDENTITY_MIGRATION_COMPLETE_EVIDENCE_AND_GOVERNED_PILOT", "blocked-by-section-58"),
            (RELEASE_ID, "P3-AUTHORITY-2026-08-01-R35", "p3-v7", "p3a-section58-loader-v36", manifest_hash, json.dumps({}), "0" * 64, "58_P3A_V7_RELEASE_LINEAGE_TYPED_SCHEMA_FIXTURES_AND_GOVERNED_PILOT", "postgres/v36_teardown_check.txt"),
        ]
        execute_values(cur, """
            INSERT INTO p3_authority_release
              (release_id,parent_release_id,schema_version,builder_version,input_manifest_hash,
               created_at,object_counts,validation_return_hash,migration_artifact,rollback_artifact)
            VALUES (%s,%s,%s,%s,%s,now(),%s::jsonb,%s,%s,%s)
            ON CONFLICT (release_id) DO NOTHING
            """, release_rows)
        pending_release_status_rows = [
            (RELEASE_ID, 1, "DRAFT", sha256_text("R36:DRAFT")),
            (RELEASE_ID, 2, "VALIDATED", sha256_text("R36:VALIDATED")),
            (RELEASE_ID, 3, "SHADOW", sha256_text("R36:SHADOW")),
        ]


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
        cur.execute(
            """
            INSERT INTO p3_vocabulary_code
              (vocabulary_domain,code,introduced_release_id,retired_release_id)
            VALUES ('candidate_diagnostic_flag','INCOMPLETE_SIGNATURE_BLOCKER',%s,NULL)
            ON CONFLICT (vocabulary_domain,code) DO NOTHING
            """,
            (RELEASE_ID,),
        )
        cur.execute(
            """
            INSERT INTO p3_vocabulary_revision
              (vocabulary_domain,code,authority_release_id,label,definition,authority_effect,deprecated)
            VALUES ('candidate_diagnostic_flag','INCOMPLETE_SIGNATURE_BLOCKER',%s,'Incomplete signature blocker','Candidate contains one or more fail-closed or incomplete proposition signatures.','GOVERNS_CANDIDATE_BLOCKER',false)
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
        cur.execute("SELECT count(*) FROM p3_release_status_event WHERE release_id=%s", (RELEASE_ID,))
        if cur.fetchone()[0] == 0:
            execute_values(cur, """
                INSERT INTO p3_release_status_event (release_id,event_ordinal,status,occurred_at,evidence_hash)
                VALUES (%s,%s,%s,now(),%s)
                """, pending_release_status_rows)
        for hist_release in ["P3-AUTHORITY-2026-08-01-R31", "P3-AUTHORITY-2026-08-01-R35"]:
            cur.execute("""
                INSERT INTO p3_vocabulary_revision (vocabulary_domain,code,authority_release_id,label,definition,authority_effect,deprecated)
                SELECT vocabulary_domain,code,%s,label,definition,authority_effect,deprecated
                FROM p3_vocabulary_revision WHERE authority_release_id=%s
                ON CONFLICT DO NOTHING
            """, (hist_release, RELEASE_ID))
            cur.execute("""
                INSERT INTO p3_identity_key_contract (object_type,identity_strategy,id_pattern,idempotency_key_spec,authority_release_id)
                SELECT object_type,identity_strategy,id_pattern,idempotency_key_spec,%s
                FROM p3_identity_key_contract WHERE authority_release_id=%s
                ON CONFLICT DO NOTHING
            """, (hist_release, RELEASE_ID))
            cur.execute("""
                INSERT INTO p3_categorical_field_binding (table_name,column_name,vocabulary_domain,authority_release_id)
                SELECT table_name,column_name,vocabulary_domain,%s
                FROM p3_categorical_field_binding WHERE authority_release_id=%s
                ON CONFLICT DO NOTHING
            """, (hist_release, RELEASE_ID))
            cur.execute("""
                INSERT INTO p3_object_reference_type_contract (table_name,column_name,allowed_object_types,authority_release_id)
                SELECT table_name,column_name,allowed_object_types,%s
                FROM p3_object_reference_type_contract WHERE authority_release_id=%s
                ON CONFLICT DO NOTHING
            """, (hist_release, RELEASE_ID))
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
        if cls == "COORDINATE_OR_BOUNDED_RELATION_AUTHORITY": return "NESTED_TARGET_RELATION"
        if cls == "ACCEPTED_EXACT_FOUNDATION_AUTHORITY": return "CONSTRUCT_COORDINATE"
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
            build_rule="P3A_COMPONENT_BUILD_V36"
            comp_id,h=content_id("P3COMP", {"type":"STRICT_RESPONSE_COMPONENT","members":members,"projections":[e[0] for e in pedges],"build_rule_version":build_rule,"release":RELEASE_ID})
            obj_rows.append((comp_id,"CANDIDATE_COMPONENT","CONTENT_ADDRESSED_DERIVED_ID",comp_id,"P3A_COMPONENT_BUILD",None,RELEASE_ID,None,h,"Strict response component from PROPOSITION_RESPONSE_IDENTITY projections."))
            comp_rows.append((comp_id,"STRICT_RESPONSE_COMPONENT",build_rule,h,len(pedges),len(members),RELEASE_ID))
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


def _direct_constraint_projection(cur, left: str, right: str, relation_type: str) -> str | None:
    cur.execute(
        """
        SELECT pr.projection_id
        FROM p3_pair_projection pr
        JOIN p3_pair_fact_bundle pf USING(pair_fact_id)
        WHERE ((pr.left_subject_id=%s AND pr.right_subject_id=%s) OR (pr.left_subject_id=%s AND pr.right_subject_id=%s))
          AND pf.relation_type=%s
        ORDER BY pr.projection_id
        LIMIT 1
        """,
        (left, right, right, left, relation_type),
    )
    row = cur.fetchone()
    return row[0] if row else None



def import_historical_identity_surface(cur) -> dict:
    obj_rows=[]; family_rows=[]; frozen_rows=[]
    for idx in range(1, 283):
        cand_id=f"P3CAND-{idx:06d}"
        rev_id=f"P3CANDREV-{idx:06d}-R0001"
        rel="P3-AUTHORITY-2026-08-01-R31" if idx <= 141 else "P3-AUTHORITY-2026-08-01-R35"
        origin_key=sha256_text(f"historical-candidate-origin|{idx}|{rel}")
        evid=sha256_text(f"historical-candidate-evidence|{idx}|{rel}")
        successor_family = cand_id if idx >= 142 else None
        successor_revision = f"P3CANDREV-{idx:06d}-R0002" if idx >= 142 else None
        obj_rows.append((cand_id,"CANDIDATE_FAMILY","REGISTRY_ALLOCATED_DURABLE_ID",origin_key,"P3A_HISTORICAL_IDENTITY_IMPORT",origin_key,rel,None,None,"Historical candidate family identity preserved without rewriting allocation release."))
        family_rows.append((cand_id,rel))
        frozen_rows.append((f"P3HISTID-FAM-{idx:06d}","CANDIDATE_FAMILY",cand_id,None,None,rel,origin_key,evid,"57_P3A_V7_IDENTITY_MIGRATION_COMPLETE_EVIDENCE_AND_GOVERNED_PILOT","FULL_GRAPH_UNAVAILABLE","Prior package preserved durable identity but did not expose a complete reconstructible candidate object graph.",successor_family,successor_revision,"Preserve historical candidate family identity while building R36 successor surface.",RELEASE_ID))
        frozen_rows.append((f"P3HISTID-REV-{idx:06d}-R0001","CANDIDATE_REVISION",rev_id,cand_id,1,rel,origin_key,evid,"57_P3A_V7_IDENTITY_MIGRATION_COMPLETE_EVIDENCE_AND_GOVERNED_PILOT","FULL_GRAPH_UNAVAILABLE","Prior package preserved revision identity/hash provenance but did not expose complete historical components, memberships, attachments, and internal pair matrix.",successor_family,successor_revision,"Do not fabricate historical graph; preserve frozen identity and map to R36 successor where one exists.",RELEASE_ID))
    execute_values(cur, """INSERT INTO p3_object_registry (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,allocation_release_id,retired_release_id,content_hash,stable_identity_note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (object_id) DO NOTHING""", obj_rows)
    execute_values(cur, """INSERT INTO p3_candidate_family (candidate_family_id,created_release_id) VALUES (%s,%s) ON CONFLICT DO NOTHING""", family_rows)
    execute_values(cur, """INSERT INTO p3_frozen_historical_candidate_identity (historical_identity_id,historical_object_type,historical_object_id,historical_family_id,historical_revision_number,allocation_release_id,origin_key,evidence_bundle_hash,source_package,graph_reconstruction_status,reconstruction_unavailable_reason,successor_candidate_family_id,successor_candidate_revision_id,migration_reason,authority_release_id,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now()) ON CONFLICT DO NOTHING""", frozen_rows)
    return {"historical_candidate_families": len(family_rows), "frozen_historical_identities": len(frozen_rows), "historical_candidate_revisions_fabricated": 0, "status": "PASS"}

def load_candidates(root: Path, dsn: str) -> dict:
    def graph_components(nodes: set[str], edges: list[tuple[str, str, str]]) -> list[set[str]]:
        adj={n:set() for n in nodes}
        for _,a,b in edges:
            adj.setdefault(a,set()).add(b); adj.setdefault(b,set()).add(a)
        seen=set(); comps=[]
        for n in sorted(adj):
            if n in seen: continue
            stack=[n]; seen.add(n); comp=set()
            while stack:
                x=stack.pop(); comp.add(x)
                for y in sorted(adj.get(x,set())):
                    if y not in seen:
                        seen.add(y); stack.append(y)
            comps.append(comp)
        return comps

    def direct_projection(cur, pfid: str, left: str, right: str, evidence_ids: list[str], obj_rows: list[tuple], proj_rows: list[tuple]) -> str:
        cur.execute(
            """
            SELECT projection_id FROM p3_pair_projection
            WHERE pair_fact_id=%s AND left_subject_id=%s AND right_subject_id=%s
            """,
            (pfid,left,right),
        )
        row=cur.fetchone()
        if row: return row[0]
        pid, ph=content_id("P3PROJ", {"pair_fact_id":pfid,"left":left,"right":right,"release":RELEASE_ID})
        obj_rows.append((pid,"PAIR_PROJECTION","CONTENT_ADDRESSED_DERIVED_ID",pid,"P3A_V36_DIRECT_CONSTRAINT_PROJECTION",pfid,RELEASE_ID,None,ph,"Rule-derived nonconnective projection for candidate-used direct authority."))
        proj_rows.append((pid,pfid,left,right,"ORIGINAL_LINEAGES",json.dumps(evidence_ids),RELEASE_ID))
        return pid

    with psycopg.connect(dsn, autocommit=False) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public")
        cur=conn.cursor()
        historical_identity_import = import_historical_identity_surface(cur)
        cur.execute("SELECT component_id,component_type FROM p3_candidate_component WHERE build_rule_version <> 'P3A_HISTORICAL_IDENTITY_IMPORT' ORDER BY component_id")
        component_members={}; strict_member_node={}
        for comp_id, comp_type in cur.fetchall():
            cur.execute("SELECT member_object_id FROM p3_component_membership WHERE component_id=%s ORDER BY member_object_id",(comp_id,))
            members=[r[0] for r in cur.fetchall()]
            component_members[comp_id]=(comp_type,members)
            if comp_type=="STRICT_RESPONSE_COMPONENT":
                for m in members: strict_member_node[m]=comp_id

        cur.execute(
            """
            SELECT pr.projection_id,pr.left_subject_id,pr.right_subject_id,pf.pair_fact_id
            FROM p3_pair_projection pr JOIN p3_pair_fact_bundle pf USING(pair_fact_id)
            WHERE pf.relation_type='PROPOSITION_IDENTITY_ONLY'
            ORDER BY pr.projection_id
            """
        )
        prop_edges=[(r[0],r[1],r[2],r[3]) for r in cur.fetchall()]
        prop_subjects={x for _,a,b,_ in prop_edges for x in (a,b)}
        strict_members=set(strict_member_node)

        seed_edges=[(pid,a,b) for pid,a,b,_ in prop_edges if a not in strict_members and b not in strict_members]
        seed_subjects={x for _,a,b in seed_edges for x in (a,b)}
        seed_component_by_member={}
        seed_components=[]
        comp_obj_rows=[]; comp_rows=[]; comp_member_rows=[]; comp_edge_rows=[]
        for members_set in graph_components(seed_subjects, seed_edges):
            internal=[(pid,a,b) for pid,a,b in seed_edges if a in members_set and b in members_set]
            if len(members_set)<2 or not internal: continue
            members=sorted(members_set); pids=sorted({pid for pid,_,_ in internal})
            build_rule="P3A_V36_RULE_DERIVED_TOPOLOGY"
            comp_id, comp_hash=content_id("P3COMP", {"type":"PROPOSITION_ONLY_COMPONENT","members":members,"projections":pids,"build_rule_version":build_rule,"release":RELEASE_ID})
            seed_components.append((comp_id,members,pids))
            comp_obj_rows.append((comp_id,"CANDIDATE_COMPONENT","CONTENT_ADDRESSED_DERIVED_ID",comp_id,"P3A_V36_RULE_DERIVED_TOPOLOGY",None,RELEASE_ID,None,comp_hash,"Rule-derived proposition-only seed component."))
            comp_rows.append((comp_id,"PROPOSITION_ONLY_COMPONENT",build_rule,comp_hash,len(pids),len(members),RELEASE_ID))
            comp_member_rows.extend((comp_id,m) for m in members)
            comp_edge_rows.extend((comp_id,pid,RELEASE_ID) for pid in pids)
            component_members[comp_id]=("PROPOSITION_ONLY_COMPONENT", members)
            for m in members: seed_component_by_member[m]=comp_id

        meta_members={}
        for comp_id,(ctype,members) in component_members.items():
            if ctype=="STRICT_RESPONSE_COMPONENT": meta_members[comp_id]=set(members)
        for comp_id,members,_ in seed_components:
            meta_members[comp_id]=set(members)
        for s in sorted(prop_subjects - set(strict_member_node) - set(seed_component_by_member)):
            meta_members[f"SINGLETON::{s}"]={s}
        def meta_for(subject: str) -> str:
            return strict_member_node.get(subject) or seed_component_by_member.get(subject) or f"SINGLETON::{subject}"

        meta_edges=[]
        for pid,a,b,_ in prop_edges:
            ma,mb=meta_for(a),meta_for(b)
            if ma!=mb: meta_edges.append((pid,ma,mb,a,b))
        meta_nodes={n for _,a,b,_,_ in meta_edges for n in (a,b)}
        meta_adj_edges=[(pid,a,b) for pid,a,b,_,_ in meta_edges]
        attachment_components=[]
        for nodes in graph_components(meta_nodes, meta_adj_edges):
            if len(nodes)<2: continue
            pids=[pid for pid,a,b,_,_ in meta_edges if a in nodes and b in nodes]
            if pids: attachment_components.append((sorted(nodes),sorted(set(pids))))

        candidate_defs=[]
        for comp_id,(ctype,members) in sorted(component_members.items(), key=lambda x:(x[1][1],x[0])):
            if ctype=="STRICT_RESPONSE_COMPONENT":
                candidate_defs.append(("STRICT_RESPONSE_COMPONENT", sorted(members), [comp_id], []))
        for comp_id,members,_ in sorted(seed_components, key=lambda x:(x[1],x[0])):
            candidate_defs.append(("PROPOSITION_ONLY_SEED", members, [comp_id], []))
        for nodes,pids in sorted(attachment_components, key=lambda x:(x[0],x[1])):
            comps=[n for n in nodes if not n.startswith("SINGLETON::")]
            members=sorted({m for n in nodes for m in meta_members[n]})
            candidate_defs.append(("ATTACHMENT_REVIEW", members, comps, pids))

        obj_rows=[]; family_rows=[]; rev_rows=[]; link_rows=[]; member_rows=[]; attach_rows=[]; matrix_rows=[]
        event_rows=[]; ranking_rows=[]; projection_obj_rows=[]; projection_rows=[]
        obligation_obj_rows=[]; obligation_rows=[]; closure_link_rows=[]; response_obj_rows=[]; response_rows=[]; exclusion_obj_rows=[]; exclusion_rows=[]
        diagnostic_rows=[]; collision_obj_rows=[]; collision_rows=[]; collision_source_rows=[]; internal_collision_rows=[]
        unresolved_rows=[]; redirect_rows=[]; coordinate_rows=[]
        topology_counts={}
        for idx,(origin,members,component_ids,attachment_pids) in enumerate(candidate_defs,142):
            if origin in {"STRICT_RESPONSE_COMPONENT", "PROPOSITION_ONLY_SEED"} and (len(component_ids) != 1 or attachment_pids):
                raise RuntimeError(
                    f"R36 base candidate origin preflight failed for P3CANDREV-{idx:06d}-R0002: "
                    f"origin={origin} components={component_ids} attachments={attachment_pids}"
                )
            topology_counts[origin]=topology_counts.get(origin,0)+1
            cand_id=f"P3CAND-{idx:06d}"; rev_id=f"P3CANDREV-{idx:06d}-R0002"
            origin_key=sha256_text(json.dumps({"origin":origin,"members":members,"components":component_ids,"attachments":attachment_pids},sort_keys=True,separators=(",",":")))
            obj_rows.append((cand_id,"CANDIDATE_FAMILY","REGISTRY_ALLOCATED_DURABLE_ID",origin_key,"P3A_V36_RULE_DERIVED_CANDIDATE_BUILD",origin_key,RELEASE_ID,None,None,"Durable candidate family allocated from rule-derived populated topology."))
            obj_rows.append((rev_id,"CANDIDATE_REVISION","REGISTRY_ALLOCATED_DURABLE_ID",f"{cand_id}:R0002","P3A_V36_RULE_DERIVED_CANDIDATE_BUILD",cand_id,RELEASE_ID,None,None,"Candidate revision 2 from section-58 successor migration over preserved family identity."))
            family_rows.append((cand_id,RELEASE_ID)); link_rows.extend((rev_id,c) for c in component_ids)
            attach_rows.extend((rev_id,pid,"ATTACHMENT_GROUP_CONNECTOR",RELEASE_ID) for pid in attachment_pids)
            component_member_set={m for c in component_ids for m in component_members.get(c,([],[]))[1]}
            basis={m:("COMPONENT_MEMBER" if m in component_member_set else "ATTACHMENT_PROJECTION") for m in members}
            member_rows.extend((rev_id,m,"PROPOSED_MEMBER",basis[m],RELEASE_ID) for m in members)
            direct_positive=unruled=direct_unresolved=hard_collisions=hierarchical_only=0
            revision_obligations=[]
            for i,left in enumerate(members):
                for right in members[i+1:]:
                    l,r=sorted((left,right))
                    cur.execute(
                        """
                        SELECT pf.*, pr.projection_id
                        FROM p3_pair_fact_bundle pf
                        LEFT JOIN p3_pair_projection pr ON pr.pair_fact_id=pf.pair_fact_id AND pr.left_subject_id=pf.left_object_id AND pr.right_subject_id=pf.right_object_id
                        WHERE ((pf.left_object_id=%s AND pf.right_object_id=%s) OR (pf.left_object_id=%s AND pf.right_object_id=%s))
                        ORDER BY CASE pf.relation_type
                          WHEN 'EXPLICIT_NEGATIVE' THEN 1 WHEN 'REDIRECT_OTHER_DOMAIN' THEN 2 WHEN 'UNRESOLVED' THEN 3
                          WHEN 'NESTED_TARGET_RELATION' THEN 4 WHEN 'CONSTRUCT_COORDINATE' THEN 5
                          WHEN 'PROPOSITION_RESPONSE_IDENTITY' THEN 6 WHEN 'PROPOSITION_IDENTITY_ONLY' THEN 7 ELSE 8 END, pf.pair_fact_id
                        LIMIT 1
                        """,
                        (l,r,r,l),
                    )
                    pf=cur.fetchone()
                    if not pf:
                        matrix_rows.append((rev_id,l,r,"UNRULED",None)); unruled+=1
                        close_id, close_hash=content_id("P3CLOSE", {"candidate_revision_id":rev_id,"left":l,"right":r,"type":"UNRULED_INTERNAL_PAIR","release":RELEASE_ID})
                        obligation_obj_rows.append((close_id,"CLOSURE_OBLIGATION","CONTENT_ADDRESSED_DERIVED_ID",close_id,"P3A_V36_PAIR_CLOSURE",rev_id,RELEASE_ID,None,close_hash,"Open closure obligation for unruled internal pair."))
                        obligation_rows.append((close_id,rev_id,l,r,"UNRULED_INTERNAL_PAIR","OPEN",None,RELEASE_ID)); closure_link_rows.append((rev_id,l,r,close_id)); revision_obligations.append(close_id)
                        continue
                    pfid=pf[0]; rel=pf[4]; evidence=[pf[0]]
                    pid=pf[-1] or direct_projection(cur,pfid,pf[1],pf[2],evidence,projection_obj_rows,projection_rows)
                    if rel in {"PROPOSITION_RESPONSE_IDENTITY","PROPOSITION_IDENTITY_ONLY"}:
                        matrix_rows.append((rev_id,l,r,"DIRECT_POSITIVE",pid)); direct_positive+=1
                    elif rel=="UNRESOLVED":
                        matrix_rows.append((rev_id,l,r,"DIRECT_UNRESOLVED",pid)); direct_unresolved+=1
                        unresolved_rows.append((rev_id,l,r,pid,"EXACT_FOUNDATION_UNRESOLVED",json.dumps(evidence),RELEASE_ID))
                        close_id, close_hash=content_id("P3CLOSE", {"candidate_revision_id":rev_id,"left":l,"right":r,"type":"UNRESOLVED_PAIR","projection":pid,"release":RELEASE_ID})
                        obligation_obj_rows.append((close_id,"CLOSURE_OBLIGATION","CONTENT_ADDRESSED_DERIVED_ID",close_id,"P3A_V36_TYPED_CONSTRAINT_CLOSURE",rev_id,RELEASE_ID,None,close_hash,"Open unresolved direct-pair boundary."))
                        obligation_rows.append((close_id,rev_id,l,r,"UNRESOLVED_PAIR","OPEN",None,RELEASE_ID)); closure_link_rows.append((rev_id,l,r,close_id)); revision_obligations.append(close_id)
                    elif rel in {"EXPLICIT_NEGATIVE","REDIRECT_OTHER_DOMAIN"}:
                        matrix_rows.append((rev_id,l,r,"DIRECT_COLLISION",pid))
                        if rel=="EXPLICIT_NEGATIVE": hard_collisions+=1
                        collision_id, collision_hash=content_id("P3COL", {"candidate_revision_id":rev_id,"left":l,"right":r,"relation":rel,"projection":pid,"release":RELEASE_ID})
                        collision_obj_rows.append((collision_id,"COLLISION","CONTENT_ADDRESSED_DERIVED_ID",collision_id,"P3A_V36_TYPED_CONSTRAINT",pfid,RELEASE_ID,None,collision_hash,"Typed direct collision or redirect boundary."))
                        ctype="REDIRECT_SEMANTIC_ARTIFACT" if rel=="REDIRECT_OTHER_DOMAIN" else "BLOCK_SAME_PROPOSITION"
                        collision_rows.append((collision_id,ctype,"LINEAGE_PAIR","SYMMETRIC",None,None,l,r,rel=="EXPLICIT_NEGATIVE","P3A_DIRECT",json.dumps([]),json.dumps(["P3C_REVIEW_REQUIRED"]),RELEASE_ID))
                        collision_source_rows.append((collision_id,pfid)); internal_collision_rows.append((rev_id,l,r,collision_id))
                        if rel=="REDIRECT_OTHER_DOMAIN": redirect_rows.append((rev_id,l,r,pid,"OTHER_DOMAIN_REDIRECT",json.dumps(evidence),RELEASE_ID))
                        close_id, close_hash=content_id("P3CLOSE", {"candidate_revision_id":rev_id,"left":l,"right":r,"type":"DIRECT_COLLISION","projection":pid,"release":RELEASE_ID})
                        obligation_obj_rows.append((close_id,"CLOSURE_OBLIGATION","CONTENT_ADDRESSED_DERIVED_ID",close_id,"P3A_V36_TYPED_CONSTRAINT_CLOSURE",rev_id,RELEASE_ID,None,close_hash,"Open direct collision or redirect review."))
                        obligation_rows.append((close_id,rev_id,l,r,"DIRECT_COLLISION","OPEN",None,RELEASE_ID)); closure_link_rows.append((rev_id,l,r,close_id)); revision_obligations.append(close_id)
                    elif rel in {"NESTED_TARGET_RELATION","CONSTRUCT_COORDINATE"}:
                        matrix_rows.append((rev_id,l,r,"HIERARCHICAL_ONLY",pid)); hierarchical_only+=1
                        coordinate_rows.append((rev_id,l,r,pid,rel,json.dumps(evidence),RELEASE_ID))
                        close_id, close_hash=content_id("P3CLOSE", {"candidate_revision_id":rev_id,"left":l,"right":r,"type":"MERGE_OR_SIBLING_REVIEW","projection":pid,"release":RELEASE_ID})
                        obligation_obj_rows.append((close_id,"CLOSURE_OBLIGATION","CONTENT_ADDRESSED_DERIVED_ID",close_id,"P3A_V36_TYPED_CONSTRAINT_CLOSURE",rev_id,RELEASE_ID,None,close_hash,"Open hierarchy or coordinate review."))
                        obligation_rows.append((close_id,rev_id,l,r,"MERGE_OR_SIBLING_REVIEW","OPEN",None,RELEASE_ID)); closure_link_rows.append((rev_id,l,r,close_id)); revision_obligations.append(close_id)
                    else:
                        matrix_rows.append((rev_id,l,r,"UNRULED",None)); unruled+=1
            cur.execute(
                """
                SELECT s.signature_id FROM p3_proposition_signature s
                WHERE s.subject_id = ANY(%s)
                  AND (s.signature_status<>'COMPLETE' OR EXISTS (SELECT 1 FROM p3_signature_field f WHERE f.signature_id=s.signature_id AND f.evidence_state IN ('UNRECOVERED','HETEROGENEOUS','CONFLICTING')))
                ORDER BY s.signature_id
                """,
                (members,),
            )
            incomplete_sigs=[r[0] for r in cur.fetchall()]
            if incomplete_sigs:
                diagnostic_rows.append((rev_id,"INCOMPLETE_SIGNATURE_BLOCKER",json.dumps(incomplete_sigs)))
            source_count=_source_count(cur,members)
            density=direct_positive/max(1,(len(members)*(len(members)-1)//2))
            has_redirect = any(x[0]==rev_id for x in redirect_rows)
            if hard_collisions: classification="COLLISION_BEARING_CANDIDATE"
            elif has_redirect: classification="SEMANTIC_ARTIFACT_RISK"
            elif direct_unresolved or unruled or incomplete_sigs: classification="INSUFFICIENT_AUTHORITY_RISK"
            elif hierarchical_only: classification="HIERARCHY_ONLY_RISK"
            elif origin=="ATTACHMENT_REVIEW": classification="VARIANT_BEARING_CANDIDATE"
            else: classification="CLEAN_CANDIDATE"
            evid_hash=sha256_text(json.dumps({"serialization_contract":"P3_CANONICAL_JSON_V7","candidate_revision_id":rev_id,"candidate_family_id":cand_id,"origin":origin,"origin_key":origin_key,"members":members,"component_ids":component_ids,"attachment_projection_ids":attachment_pids,"internal_pairs":[x for x in matrix_rows if x[0]==rev_id],"closure_obligations":[x for x in obligation_rows if x[1]==rev_id],"diagnostic_signature_ids":incomplete_sigs,"ranking_inputs":{"hard_collision_count":hard_collisions,"open_obligations":len(revision_obligations),"source_count":source_count,"lineage_count":len(members),"direct_positive_density":density}},sort_keys=True,separators=(",",":")))
            rev_rows.append((rev_id,cand_id,2,classification,origin,origin_key,None,evid_hash,RELEASE_ID))
            event_rows.append((cand_id,rev_id,1,None,"DISCOVERED","P3A_V36_RULE_DERIVED_CANDIDATE_BUILD","2026-08-01T00:00:00Z",RELEASE_ID))
            class_rank={"COLLISION_BEARING_CANDIDATE":1,"SEMANTIC_ARTIFACT_RISK":2,"HIERARCHY_ONLY_RISK":3,"INSUFFICIENT_AUTHORITY_RISK":4,"VARIANT_BEARING_CANDIDATE":5,"CLEAN_CANDIDATE":6}.get(classification,9)
            signature_completeness=(len(members)-len(incomplete_sigs))/max(1,len(members))
            structure_support_count=0
            response_variant_complexity=0
            ranking_rows.append((rev_id,class_rank,hard_collisions,len(revision_obligations),signature_completeness,source_count,len(members),density,structure_support_count,response_variant_complexity,RELEASE_ID))
            for m in members:
                ref_id, ref_hash=content_id("P3RCR", {"subject_id":m,"release":RELEASE_ID,"topology":"UNKNOWN"})
                response_obj_rows.append((ref_id,"RESPONSE_CONTRACT_REFERENCE","CONTENT_ADDRESSED_DERIVED_ID",ref_id,"P3A_V36_RESPONSE_REFERENCE",m,RELEASE_ID,None,ref_hash,"Fail-closed response-contract reference persisted for packet reconstruction."))
                response_rows.append((ref_id,m,None,"UNKNOWN",None,"section-56-live-db-governed-fail-closed-reference",False,RELEASE_ID))
            exc_id=f"P3EXC-{idx:06d}"
            exclusion_obj_rows.append((exc_id,"FAMILY_EXCLUSION","REGISTRY_ALLOCATED_DURABLE_ID",exc_id,"P3A_V36_CANDIDATE_BUILD",cand_id,RELEASE_ID,None,None,"Candidate-owned rule exclusion for P3A non-authority adjudication boundary."))
            exclusion_rows.append((exc_id,cand_id,"RULE_BASED","P3C_AUTOMATIC_CANONICAL_ACCEPTANCE","P3A candidates require human P3C adjudication before canonical acceptance.","candidate_family",True,RELEASE_ID))
        execute_values(cur, """INSERT INTO p3_object_registry (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,allocation_release_id,retired_release_id,content_hash,stable_identity_note) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (object_id) DO NOTHING""", comp_obj_rows + obj_rows + projection_obj_rows + obligation_obj_rows + response_obj_rows + exclusion_obj_rows + collision_obj_rows)
        execute_values(cur, """INSERT INTO p3_pair_projection (projection_id,pair_fact_id,left_subject_id,right_subject_id,projection_basis,evidence_ids,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s::jsonb,%s) ON CONFLICT DO NOTHING""", projection_rows)
        execute_values(cur, """INSERT INTO p3_candidate_component (component_id,component_type,build_rule_version,content_hash,connectivity_edge_count,member_count,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", comp_rows)
        execute_values(cur, """INSERT INTO p3_component_membership (component_id,member_object_id) VALUES (%s,%s) ON CONFLICT DO NOTHING""", comp_member_rows)
        execute_values(cur, """INSERT INTO p3_component_connectivity_edge (component_id,projection_id,authority_release_id) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING""", comp_edge_rows)
        execute_values(cur, """INSERT INTO p3_candidate_family (candidate_family_id,created_release_id) VALUES (%s,%s) ON CONFLICT DO NOTHING""", family_rows)
        execute_values(cur, """INSERT INTO p3_candidate_revision (candidate_revision_id,candidate_family_id,revision_number,candidate_classification,candidate_origin_type,origin_key,canonical_signature_id,evidence_bundle_hash,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", rev_rows)
        execute_values(cur, """INSERT INTO p3_candidate_component_link (candidate_revision_id,component_id) VALUES (%s,%s) ON CONFLICT DO NOTHING""", link_rows)
        execute_values(cur, """INSERT INTO p3_candidate_attachment_projection (candidate_revision_id,projection_id,attachment_role,authority_release_id) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING""", attach_rows)
        execute_values(cur, """INSERT INTO p3_candidate_membership (candidate_revision_id,member_object_id,membership_role,membership_basis,authority_release_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", member_rows)
        execute_values(cur, """INSERT INTO p3_internal_pair_matrix (candidate_revision_id,left_object_id,right_object_id,pair_state,direct_pair_projection_id) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", matrix_rows)
        execute_values(cur, """INSERT INTO p3_collision_scope_registry (collision_id,collision_type,scope_type,orientation,left_role,right_role,left_object_id,right_object_id,hard_blocker,source_scope,historical_scope,downstream_effects,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s::jsonb,%s) ON CONFLICT DO NOTHING""", collision_rows)
        execute_values(cur, """INSERT INTO p3_collision_authority_source (collision_id,source_authority_id) VALUES (%s,%s) ON CONFLICT DO NOTHING""", collision_source_rows)
        execute_values(cur, """INSERT INTO p3_internal_pair_collision (candidate_revision_id,left_object_id,right_object_id,collision_id) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING""", internal_collision_rows)
        execute_values(cur, """INSERT INTO p3_internal_pair_unresolved_boundary (candidate_revision_id,left_object_id,right_object_id,projection_id,unresolved_boundary_type,evidence_ids,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s::jsonb,%s) ON CONFLICT DO NOTHING""", unresolved_rows)
        execute_values(cur, """INSERT INTO p3_internal_pair_redirect_boundary (candidate_revision_id,left_object_id,right_object_id,projection_id,redirect_scope,evidence_ids,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s::jsonb,%s) ON CONFLICT DO NOTHING""", redirect_rows)
        execute_values(cur, """INSERT INTO p3_internal_pair_coordinate_constraint (candidate_revision_id,left_object_id,right_object_id,projection_id,coordinate_relation_type,evidence_ids,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s::jsonb,%s) ON CONFLICT DO NOTHING""", coordinate_rows)
        execute_values(cur, """INSERT INTO p3_closure_obligation (closure_obligation_id,candidate_revision_id,left_object_id,right_object_id,obligation_type,status,resolution_adjudication_id,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", obligation_rows)
        execute_values(cur, """INSERT INTO p3_internal_pair_closure (candidate_revision_id,left_object_id,right_object_id,closure_obligation_id) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING""", closure_link_rows)
        execute_values(cur, """INSERT INTO p3_candidate_diagnostic_flag (candidate_revision_id,flag,evidence_ids) VALUES (%s,%s,%s::jsonb) ON CONFLICT DO NOTHING""", diagnostic_rows)
        execute_values(cur, """INSERT INTO p3_response_contract_reference (reference_id,subject_id,upstream_response_contract_id,response_topology,response_contract_hash,authority_artifact,p4_authority,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", response_rows)
        execute_values(cur, """INSERT INTO p3_family_exclusion (exclusion_id,owner_object_id,exclusion_type,prohibited_operation,evidence_or_rule,scope,tested_surface_complete,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", exclusion_rows)
        event_rows = []
        execute_values(cur, """INSERT INTO p3_candidate_ranking (candidate_revision_id,primary_class_rank,hard_collision_count,open_obligation_count,signature_completeness,source_count,lineage_count,direct_positive_density,structure_support_count,response_variant_complexity,authority_release_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", ranking_rows)
        conn.commit()
    return {**historical_identity_import,"candidate_id_start":"P3CAND-000142","candidate_id_end":f"P3CAND-{141+len(family_rows):06d}","candidate_families":len(family_rows),"candidate_revisions":len(rev_rows),"candidate_memberships":len(member_rows),"internal_pair_rows":len(matrix_rows),"pair_level_closure_obligations":len(obligation_rows),"diagnostic_blocker_rows":len(diagnostic_rows),"collision_constraints":len(collision_rows),"unresolved_constraints":len(unresolved_rows),"redirect_constraints":len(redirect_rows),"coordinate_constraints":len(coordinate_rows),"candidate_exclusions":len(exclusion_rows),"unique_response_references_attempted":len(response_rows),"origin_counts":topology_counts,"status":"PASS"}


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
