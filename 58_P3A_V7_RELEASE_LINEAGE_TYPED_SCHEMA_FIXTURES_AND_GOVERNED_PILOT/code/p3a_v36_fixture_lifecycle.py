from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import psycopg


SCHEMA = "p3a_v27_shadow"
FIXTURE_RELEASE = "P3-AUTHORITY-2026-08-01-R36-FIXTURE"


def members(cur, revision: str) -> list[str]:
    cur.execute(
        """
        SELECT member_object_id
        FROM p3_candidate_membership
        WHERE candidate_revision_id=%s AND membership_role='PROPOSED_MEMBER'
        ORDER BY member_object_id
        """,
        (revision,),
    )
    return [r[0] for r in cur.fetchall()]


def live_revision(cur, offset: int = 0, origin: str | None = None, min_members: int = 2) -> str:
    params = ["P3-AUTHORITY-2026-08-01-R36", min_members]
    origin_filter = ""
    if origin:
        origin_filter = "AND cr.candidate_origin_type=%s"
        params.append(origin)
    params.append(offset)
    cur.execute(
        f"""
        SELECT cr.candidate_revision_id
        FROM p3_candidate_revision cr
        JOIN (
          SELECT candidate_revision_id, count(*) member_count
          FROM p3_candidate_membership
          WHERE membership_role='PROPOSED_MEMBER'
          GROUP BY candidate_revision_id
        ) cm USING(candidate_revision_id)
        WHERE cr.authority_release_id=%s
          AND cm.member_count >= %s
          {origin_filter}
        ORDER BY cr.candidate_revision_id
        OFFSET %s
        LIMIT 1
        """,
        tuple(params),
    )
    row = cur.fetchone()
    if not row:
        raise RuntimeError("no live R36 candidate revision available for fixture")
    return row[0]


def ensure_release(cur) -> None:
    cur.execute(
        """
        INSERT INTO p3_authority_release
          (release_id,parent_release_id,schema_version,builder_version,input_manifest_hash,
           created_at,object_counts,validation_return_hash,migration_artifact,rollback_artifact)
        VALUES (%s,'P3-AUTHORITY-2026-08-01-R36','p3-v7','p3a-v33-isolated-test-fixture',
                %s,now(),'{}'::jsonb,%s,'NONAUTHORITY_TEST_FIXTURE','ROLLBACK_ONLY')
        ON CONFLICT (release_id) DO NOTHING
        """,
        (FIXTURE_RELEASE, "1" * 64, "2" * 64),
    )
    cur.execute(
        """
        INSERT INTO p3_identity_key_contract
          (object_type,identity_strategy,id_pattern,idempotency_key_spec,authority_release_id)
        SELECT object_type,identity_strategy,id_pattern,idempotency_key_spec,%s
        FROM p3_identity_key_contract
        WHERE authority_release_id='P3-AUTHORITY-2026-08-01-R36'
        ON CONFLICT (object_type,authority_release_id) DO NOTHING
        """,
        (FIXTURE_RELEASE,),
    )


def registry(cur, object_id: str, object_type: str, note: str) -> None:
    cur.execute(
        """
        INSERT INTO p3_object_registry
          (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,
           allocation_release_id,retired_release_id,content_hash,stable_identity_note)
        VALUES (%s,%s,'REGISTRY_ALLOCATED_DURABLE_ID',%s,'P3A_V32_TEST_FIXTURE',%s,%s,NULL,NULL,%s)
        ON CONFLICT (object_id) DO NOTHING
        """,
        (object_id, object_type, object_id, object_id, FIXTURE_RELEASE, note),
    )


def content_registry(cur, object_id: str, object_type: str, content_hash: str, note: str) -> None:
    cur.execute(
        """
        INSERT INTO p3_object_registry
          (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,
           allocation_release_id,retired_release_id,content_hash,stable_identity_note)
        VALUES (%s,%s,'CONTENT_ADDRESSED_DERIVED_ID',%s,'P3A_V32_TEST_FIXTURE',%s,%s,NULL,%s,%s)
        ON CONFLICT (object_id) DO NOTHING
        """,
        (object_id, object_type, content_hash, object_id, FIXTURE_RELEASE, content_hash, note),
    )


def insert_decision(cur, adjudication_id: str, revision: str, status: str, ordinal: int, canonical_family_id=None, canonical_proposition=None) -> None:
    registry(cur, adjudication_id, "ADJUDICATION", f"Non-authoritative {status} fixture decision.")
    cur.execute(
        """
        INSERT INTO p3_adjudication_decision
          (adjudication_id,candidate_revision_id,decision_ordinal,decision_status,canonical_family_id,
           canonical_proposition,response_portability_status,rationale,evidence_bundle_hash,
           supersedes_adjudication_id,authority_release_id,created_at)
        VALUES (%s,%s,%s,%s,%s,%s,'NOT_AUTHORIZED_BY_P3',%s,%s,NULL,%s,now())
        """,
        (
            adjudication_id,
            revision,
            ordinal,
            status,
            canonical_family_id,
            json.dumps(canonical_proposition) if canonical_proposition is not None else None,
            "NONAUTHORITY TEST FIXTURE ONLY",
            "3" * 64,
            FIXTURE_RELEASE,
        ),
    )


def accepted(cur) -> None:
    revision = live_revision(cur, 0, "STRICT_RESPONSE_COMPONENT")
    fam = "JFAM-910001"
    famrev = "JFAMREV-910001-R0001"
    adj = "P3ADJ-910001"
    ms = members(cur, revision)
    for oid, typ in [(fam, "CANONICAL_FAMILY"), (famrev, "CANONICAL_FAMILY_REVISION")]:
        registry(cur, oid, typ, "Non-authoritative accepted fixture object.")
    sig_content = hashlib.sha256(f"{famrev}|fixture-complete-signature|v32".encode("utf-8")).hexdigest()
    sig = f"P3SIG-{sig_content[:16]}"
    content_registry(cur, sig, "PROPOSITION_SIGNATURE", sig_content, "Non-authoritative complete fixture signature.")
    cur.execute(
        """
        INSERT INTO p3_proposition_signature
          (signature_id,subject_id,signature_status,content_hash,authority_release_id)
        VALUES (%s,%s,'COMPLETE',%s,%s)
        """,
        (sig, famrev, sig_content, FIXTURE_RELEASE),
    )
    for field in [
        "subject_role", "operator", "target", "object_or_outcome", "modality", "timeframe",
        "condition", "population_scope", "geographic_scope", "polarity", "derived_status", "parent_context",
    ]:
        cur.execute(
            """
            INSERT INTO p3_signature_field
              (signature_id,field_name,field_value,normalized_value_code,evidence_state,confidence)
            VALUES (%s,%s,%s,NULL,'KNOWN','HIGH')
            """,
            (sig, field, f"fixture_{field}"),
        )
    insert_decision(cur, adj, revision, "ACCEPTED_CANONICAL", 1, fam, {"fixture": "accepted"})
    cur.execute("INSERT INTO p3_canonical_family (canonical_family_id,created_by_adjudication_id,created_release_id) VALUES (%s,%s,%s)", (fam, adj, FIXTURE_RELEASE))
    cur.execute(
        """
        INSERT INTO p3_canonical_family_revision
          (family_revision_id,canonical_family_id,revision_number,canonical_signature_id,canonical_proposition,
           evidence_bundle_hash,created_by_adjudication_id,authority_release_id)
        VALUES (%s,%s,1,%s,%s,%s,%s,%s)
        """,
        (famrev, fam, sig, json.dumps({"fixture": "accepted"}), "5" * 64, adj, FIXTURE_RELEASE),
    )
    for m in ms:
        cur.execute("INSERT INTO p3_adjudication_member VALUES (%s,%s,'ACCEPT',NULL)", (adj, m))
        cur.execute("INSERT INTO p3_canonical_family_membership VALUES (%s,%s,NULL)", (famrev, m))
    exc = "P3EXC-910001"
    registry(cur, exc, "FAMILY_EXCLUSION", "Non-authoritative accepted fixture rule exclusion.")
    cur.execute(
        """
        INSERT INTO p3_family_exclusion
          (exclusion_id,owner_object_id,exclusion_type,prohibited_operation,evidence_or_rule,scope,tested_surface_complete,authority_release_id)
        VALUES (%s,%s,'RULE_BASED','AUTO_PROMOTION','NONAUTHORITY TEST FIXTURE ONLY','P3A_V32_FIXTURE',true,%s)
        """,
        (exc, fam, FIXTURE_RELEASE),
    )


def split(cur, omit_last: bool = False) -> None:
    revision = live_revision(cur, 1 if not omit_last else 2)
    adj = "P3ADJ-910002" if not omit_last else "P3ADJ-910012"
    insert_decision(cur, adj, revision, "SPLIT_REQUIRED", 1)
    cur.execute("INSERT INTO p3_adjudication_split_point VALUES (%s,1,'NONAUTHORITY_TEST_DIMENSION','fixture split point')", (adj,))
    ms = members(cur, revision)
    left, right = ms[: len(ms) // 2], ms[len(ms) // 2 :]
    if omit_last:
        right = right[:-1]
    for idx, group in [(1, left), (2, right)]:
        cf = f"P3CAND-91{idx:04d}" if not omit_last else f"P3CAND-92{idx:04d}"
        registry(cur, cf, "CANDIDATE_FAMILY", "Non-authoritative split successor fixture.")
        cur.execute("INSERT INTO p3_candidate_family (candidate_family_id,created_release_id) VALUES (%s,%s)", (cf, FIXTURE_RELEASE))
        cur.execute(
            "INSERT INTO p3_adjudication_split_result VALUES (%s,%s,%s,%s,%s)",
            (adj, idx, cf, f"{idx:064x}"[-64:].replace("0", "a", 1), "fixture split successor"),
        )
        for m in group:
            cur.execute(
                "INSERT INTO p3_adjudication_split_member VALUES (%s,1,%s,%s)",
                (adj, "LEFT" if idx == 1 else "RIGHT", m),
            )
            cur.execute("INSERT INTO p3_adjudication_split_result_member VALUES (%s,%s,%s)", (adj, idx, m))
    for m in ms:
        cur.execute("INSERT INTO p3_adjudication_member VALUES (%s,%s,'SPLIT',NULL)", (adj, m))


def hierarchy(cur, omit_member: bool = False) -> None:
    revision = live_revision(cur, 3 if not omit_member else 4)
    adj = "P3ADJ-910003" if not omit_member else "P3ADJ-910013"
    insert_decision(cur, adj, revision, "HIERARCHICAL_RELATION_ONLY", 1)
    ms = members(cur, revision)
    cur.execute("SELECT candidate_family_id FROM p3_candidate_revision WHERE candidate_revision_id=%s", (revision,))
    broader = cur.fetchone()[0]
    narrower = "P3CAND-910003" if not omit_member else "P3CAND-920003"
    registry(cur, narrower, "CANDIDATE_FAMILY", "Non-authoritative hierarchy successor fixture.")
    cur.execute("INSERT INTO p3_candidate_family (candidate_family_id,created_release_id) VALUES (%s,%s)", (narrower, FIXTURE_RELEASE))
    cur.execute("INSERT INTO p3_adjudication_hierarchy_relation VALUES (%s,%s,%s,'BROADER_NARROWER_TEST_ONLY')", (adj, broader, narrower))
    use = ms[:-1] if omit_member else ms
    for m in use:
        cur.execute("INSERT INTO p3_adjudication_member VALUES (%s,%s,'HIERARCHICAL',NULL)", (adj, m))


def duplicate_disposition(cur) -> None:
    revision = live_revision(cur, 5)
    adj = "P3ADJ-910014"
    insert_decision(cur, adj, revision, "HIERARCHICAL_RELATION_ONLY", 1)
    ms = members(cur, revision)
    cur.execute("SELECT candidate_family_id FROM p3_candidate_revision WHERE candidate_revision_id=%s", (revision,))
    broader = cur.fetchone()[0]
    narrower = "P3CAND-910014"
    registry(cur, narrower, "CANDIDATE_FAMILY", "Non-authoritative duplicate-disposition mutation fixture.")
    cur.execute("INSERT INTO p3_candidate_family (candidate_family_id,created_release_id) VALUES (%s,%s)", (narrower, FIXTURE_RELEASE))
    cur.execute("INSERT INTO p3_adjudication_hierarchy_relation VALUES (%s,%s,%s,'BROADER_NARROWER_TEST_ONLY')", (adj, broader, narrower))
    cur.execute("INSERT INTO p3_adjudication_member VALUES (%s,%s,'HIERARCHICAL',NULL)", (adj, ms[0]))
    cur.execute("INSERT INTO p3_adjudication_member VALUES (%s,%s,'HIERARCHICAL',NULL)", (adj, ms[0]))


def release_mismatch(cur) -> None:
    revision = live_revision(cur, 6)
    cur.execute("SELECT candidate_family_id FROM p3_candidate_revision WHERE candidate_revision_id=%s", (revision,))
    family = cur.fetchone()[0]
    cur.execute(
        """
        INSERT INTO p3_candidate_status_event
          (candidate_family_id,candidate_revision_id,event_ordinal,from_stage,to_stage,guard_evidence_id,occurred_at,authority_release_id)
        VALUES (%s,%s,99,'DISCOVERED','ADJUDICATION_REQUIRED','MUTATION_RELEASE_MISMATCH',now(),%s)
        """,
        (family, revision, FIXTURE_RELEASE),
    )


def incomplete_promotion_mapping(cur) -> None:
    revision = live_revision(cur, 7)
    adj = "P3ADJ-910015"
    family_id = "JFAM-910015"
    registry(cur, family_id, "CANONICAL_FAMILY", "Non-authoritative variant mapping mutation fixture.")
    insert_decision(cur, adj, revision, "ACCEPTED_WITH_VARIANTS", 1, family_id, {"fixture": "incomplete_promotion"})
    cur.execute(
        """
        INSERT INTO p3_canonical_family
          (canonical_family_id,created_by_adjudication_id,created_release_id,retired_release_id)
        VALUES (%s,%s,%s,NULL)
        """,
        (family_id, adj, FIXTURE_RELEASE),
    )
    ms = members(cur, revision)
    for m in ms:
        cur.execute("INSERT INTO p3_adjudication_member VALUES (%s,%s,'ACCEPT',NULL)", (adj, m))


def run_case(dsn: str, name: str, fn, expect_pass: bool) -> dict:
    try:
        with psycopg.connect(dsn, autocommit=False) as conn:
            conn.execute(f"SET search_path TO {SCHEMA}, public")
            cur = conn.cursor()
            ensure_release(cur)
            fn(cur)
            cur.execute("SET CONSTRAINTS ALL IMMEDIATE")
            if expect_pass:
                conn.commit()
            else:
                conn.rollback()
        return {"case": name, "status": "PASS" if expect_pass else "UNEXPECTED_PASS", "expect_pass": expect_pass}
    except Exception as exc:
        if expect_pass and "duplicate key value violates unique constraint" in str(exc):
            return {"case": name, "status": "PASS_ALREADY_COMMITTED", "expect_pass": expect_pass, "note": str(exc)}
        return {"case": name, "status": "EXPECTED_FAIL" if not expect_pass else "FAIL", "expect_pass": expect_pass, "error": str(exc)}


def stale_evidence_hash_case(section: Path) -> dict:
    fixture_dir = section / "test_only_fixtures"
    fixture_dir.mkdir(exist_ok=True)
    source = sorted((section / "candidate_packets").glob("*.json"))[0]
    mutated = fixture_dir / "MUTATION_STALE_EVIDENCE_HASH_PACKET.json"
    obj = json.loads(source.read_text())
    obj["evidence_bundle_hash"] = "0" * 64
    obj["candidate_family"]["evidence_bundle_hash"] = "0" * 64
    obj["decision_form"]["evidence_bundle_hash"] = "0" * 64
    mutated.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    proc = subprocess.run(
        [sys.executable, str(section / "validation/validate_p3_candidate_packet_v32.py"), str(mutated)],
        text=True,
        capture_output=True,
    )
    return {
        "case": "mutation_stale_evidence_hash",
        "status": "EXPECTED_FAIL" if proc.returncode != 0 else "UNEXPECTED_PASS",
        "expect_pass": False,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    cases = [
        ("valid_accepted_fixture", accepted, True),
        ("valid_split_fixture", lambda cur: split(cur, False), True),
        ("valid_hierarchy_fixture", lambda cur: hierarchy(cur, False), True),
        ("mutation_incomplete_split_union", lambda cur: split(cur, True), False),
        ("mutation_omitted_hierarchy_endpoint", lambda cur: hierarchy(cur, True), False),
        ("mutation_duplicate_dispositions", duplicate_disposition, False),
        ("mutation_release_mismatch", release_mismatch, False),
        ("mutation_incomplete_promotion_mapping", incomplete_promotion_mapping, False),
    ]
    results = [run_case(args.dsn, name, fn, expect) for name, fn, expect in cases]
    results.append(stale_evidence_hash_case(args.output.resolve().parents[1]))
    status = "PASS" if all(r["status"] in {"PASS", "PASS_ALREADY_COMMITTED", "EXPECTED_FAIL"} for r in results) else "FAIL"
    out = {"status": status, "release_id": FIXTURE_RELEASE, "results": results}
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
