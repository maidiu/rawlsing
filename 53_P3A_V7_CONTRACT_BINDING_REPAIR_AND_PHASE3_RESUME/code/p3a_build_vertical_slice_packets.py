from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import psycopg


RELEASE_ID = "P3-AUTHORITY-2026-08-01-R31"
SCHEMA = "p3a_v27_shadow"
FIELDS = [
    "subject_role",
    "operator",
    "target",
    "object_or_outcome",
    "modality",
    "timeframe",
    "condition",
    "population_scope",
    "geographic_scope",
    "polarity",
    "derived_status",
    "parent_context",
]


def stable(prefix: str, *parts: str, width: int = 16) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:width]
    return f"{prefix}-{digest}"


def canonical_sha256(value):
    from p3_canonical_json_v7 import canonical_sha256 as _sha

    return _sha(value)


def fetch_all(cur, sql: str, params=()):
    cur.execute(sql, params)
    return [dict(row) for row in cur.fetchall()]


def evidence_surface(packet):
    candidate = dict(packet["candidate_family"])
    candidate.pop("evidence_bundle_hash", None)
    candidate.pop("ranking", None)

    def sort_objects(values):
        return sorted(values, key=canonical_sha256)

    return {
        "serialization_contract": "P3_CANONICAL_JSON_V7",
        "candidate_family": candidate,
        "origin_components": sort_objects(packet["origin_components"]),
        "members_by_source": packet["members_by_source"],
        "proposition_signature_matrix": sort_objects(packet["proposition_signature_matrix"]),
        "response_contract_matrix": sort_objects(packet["response_contract_matrix"]),
        "pair_projections": sort_objects(packet["pair_projections"]),
        "internal_pair_matrix": sort_objects(packet["internal_pair_matrix"]),
        "hard_collisions": sort_objects(packet["hard_collisions"]),
        "unresolved_pairs": sort_objects(packet["unresolved_pairs"]),
        "unruled_pairs": sort_objects(packet["unruled_pairs"]),
        "closure_obligations": sort_objects(packet["closure_obligations"]),
        "likely_split_points": sort_objects(packet["likely_split_points"]),
        "proposed_variants": sort_objects(packet["proposed_variants"]),
        "explicit_exclusions": sort_objects(packet["explicit_exclusions"]),
        "hyperedge_context": sort_objects(packet["hyperedge_context"]),
        "strata_horizon_context": sort_objects(packet["strata_horizon_context"]),
        "exact_evidence_links": packet["exact_evidence_links"],
    }


def build_packet(cur, row: dict, ordinal: int) -> tuple[dict, dict]:
    cand_rev = row["candidate_revision_id"]
    cand_family = row["candidate_family_id"]
    members = [r["member_object_id"] for r in fetch_all(
        cur,
        """
        SELECT member_object_id
        FROM p3_candidate_membership
        WHERE candidate_revision_id=%s
        ORDER BY member_object_id
        """,
        (cand_rev,),
    )]
    source_rows = fetch_all(
        cur,
        """
        SELECT u.source_family AS source_authority_id, cm.member_object_id
        FROM p3_candidate_membership cm
        JOIN p3_upstream_object_reference u ON u.object_id=cm.member_object_id
        WHERE cm.candidate_revision_id=%s
        ORDER BY u.source_family, cm.member_object_id
        """,
        (cand_rev,),
    )
    members_by_source = {}
    for source_row in source_rows:
        members_by_source.setdefault(source_row["source_authority_id"], []).append(source_row["member_object_id"])

    component_rows = fetch_all(
        cur,
        """
        SELECT ccl.component_id, cc.component_type, cc.build_rule_version, cc.content_hash, cce.projection_id
        FROM p3_candidate_component_link ccl
        JOIN p3_candidate_component cc ON cc.component_id=ccl.component_id
        JOIN p3_component_connectivity_edge cce ON cce.component_id=ccl.component_id
        WHERE ccl.candidate_revision_id=%s
        ORDER BY ccl.component_id, cce.projection_id
        """,
        (cand_rev,),
    )
    comp_id = component_rows[0]["component_id"]
    comp_meta = component_rows[0]
    connectivity_projection_ids = sorted({r["projection_id"] for r in component_rows})

    projections = fetch_all(
        cur,
        """
        SELECT projection_id,pair_fact_id,left_subject_id,right_subject_id,projection_basis,evidence_ids,authority_release_id
        FROM p3_pair_projection
        WHERE projection_id = ANY(%s)
        ORDER BY projection_id
        """,
        (connectivity_projection_ids,),
    )
    projection_by_pair = {
        tuple(sorted((p["left_subject_id"], p["right_subject_id"]))): p for p in projections
    }

    signatures = []
    for member in members:
        sig = fetch_all(
            cur,
            """
            SELECT s.signature_id, s.subject_id, sf.field_name, sf.field_value,
                   sf.normalized_value_code, sf.evidence_state, sf.confidence,
                   s.signature_status, s.content_hash
            FROM p3_proposition_signature s
            JOIN p3_signature_field sf ON sf.signature_id=s.signature_id
            WHERE s.subject_id=%s
            ORDER BY sf.field_name
            """,
            (member,),
        )
        fields = {}
        for field in FIELDS:
            field_row = next(r for r in sig if r["field_name"] == field)
            fields[field] = {
                "field_value": field_row["field_value"],
                "normalized_value_code": field_row["normalized_value_code"],
                "evidence_state": field_row["evidence_state"],
                "confidence": field_row["confidence"],
                "evidence_ids": [],
            }
        signatures.append(
            {
                "signature_id": sig[0]["signature_id"],
                "subject_id": member,
                "subject_type": "IMPORTED_SOURCE_LOCAL_LINEAGE",
                "fields": fields,
                "response_topologies": ["UNKNOWN"],
                "signature_status": sig[0]["signature_status"],
                "content_hash": sig[0]["content_hash"],
                "authority_release_id": RELEASE_ID,
            }
        )

    response_contracts = [
        {
            "reference_id": stable("P3RCR", member),
            "subject_id": member,
            "upstream_response_contract_id": None,
            "response_topology": "UNKNOWN",
            "response_contract_hash": None,
            "authority_artifact": "section-53-live-db-derived-fail-closed-reference",
            "p4_authority": False,
            "authority_release_id": RELEASE_ID,
        }
        for member in members
    ]

    internal_pairs = []
    for i, left in enumerate(members):
        for right in members[i + 1 :]:
            proj = projection_by_pair.get(tuple(sorted((left, right))))
            if proj:
                internal_pairs.append(
                    {
                        "left_id": left,
                        "right_id": right,
                        "pair_state": "DIRECT_POSITIVE",
                        "pair_fact_id": proj["pair_fact_id"],
                        "pair_projection_id": proj["projection_id"],
                        "collision_ids": [],
                        "closure_obligation_ids": [],
                    }
                )
            else:
                internal_pairs.append(
                    {
                        "left_id": left,
                        "right_id": right,
                        "pair_state": "UNRULED",
                        "pair_fact_id": None,
                        "pair_projection_id": None,
                        "collision_ids": [],
                        "closure_obligation_ids": [],
                    }
                )

    expected_pairs = len(internal_pairs)
    direct_positive = sum(1 for pair in internal_pairs if pair["pair_state"] == "DIRECT_POSITIVE")
    unruled = sum(1 for pair in internal_pairs if pair["pair_state"] == "UNRULED")
    ranking = {
        "candidate_revision_id": cand_rev,
        "primary_class_rank": ordinal,
        "hard_collision_count": 0,
        "open_obligation_count": 0,
        "signature_completeness": 0,
        "source_count": len(members_by_source),
        "lineage_count": len(members),
        "direct_positive_density": direct_positive / expected_pairs,
        "structure_support_count": direct_positive,
        "response_variant_complexity": 0,
        "authority_release_id": RELEASE_ID,
    }
    exclusion_id = f"P3EXC-{ordinal:06d}"
    candidate = {
        "candidate_family_id": cand_family,
        "revision_id": cand_rev,
        "revision_number": row["revision_number"],
        "component_ids": [comp_id],
        "member_ids": members,
        "canonical_signature_id": row["canonical_signature_id"],
        "candidate_classification": row["candidate_classification"],
        "candidate_origin_type": row["candidate_origin_type"],
        "diagnostic_flags": ["SPARSE"],
        "internal_pair_counts": {
            "expected_pairs": expected_pairs,
            "direct_positive": direct_positive,
            "direct_collision": 0,
            "direct_unresolved": 0,
            "hierarchical_only": 0,
            "unruled": unruled,
            "signature_conflict": 0,
            "signature_compatible": 0,
        },
        "closure_obligation_ids": [],
        "variant_ids": [],
        "exclusion_ids": [exclusion_id],
        "ranking": ranking,
        "evidence_bundle_hash": "0" * 64,
        "authority_release_id": RELEASE_ID,
        "origin_key": row["origin_key"],
        "attachment_projection_ids": [],
    }
    origin_component = {
        "component_id": comp_id,
        "component_type": comp_meta["component_type"],
        "member_ids": members,
        "connectivity_projection_ids": connectivity_projection_ids,
        "build_rule_version": comp_meta["build_rule_version"],
        "content_hash": comp_meta["content_hash"],
        "authority_release_id": RELEASE_ID,
    }
    packet = {
        "packet_id": stable("P3PKT", cand_rev),
        "candidate_family": candidate,
        "origin_components": [origin_component],
        "members_by_source": members_by_source,
        "proposition_signature_matrix": signatures,
        "response_contract_matrix": response_contracts,
        "pair_projections": projections,
        "internal_pair_matrix": internal_pairs,
        "hard_collisions": [],
        "unresolved_pairs": [],
        "unruled_pairs": [pair for pair in internal_pairs if pair["pair_state"] == "UNRULED"],
        "closure_obligations": [],
        "likely_split_points": [],
        "proposed_variants": [],
        "explicit_exclusions": [
            {
                "exclusion_id": exclusion_id,
                "owner_object_id": cand_rev,
                "exclusion_type": "RULE_BASED",
                "prohibited_operation": "P3C_AUTOMATIC_CANONICAL_ACCEPTANCE",
                "evidence_or_rule": "P3A signatures are fail-closed and require P3C adjudication before canonical acceptance.",
                "scope": "candidate_revision",
                "tested_surface_complete": True,
                "excluded_object_ids": [],
                "authority_release_id": RELEASE_ID,
            }
        ],
        "hyperedge_context": [],
        "strata_horizon_context": [],
        "exact_evidence_links": [cand_rev, comp_id],
        "evidence_bundle_hash": "0" * 64,
        "decision_form": {},
        "fixture_status": "AUTHORITY_PACKET",
    }
    evidence_hash = canonical_sha256(evidence_surface(packet))
    packet["evidence_bundle_hash"] = evidence_hash
    packet["candidate_family"]["evidence_bundle_hash"] = evidence_hash
    decision = {
        "adjudication_id": f"P3ADJ-{ordinal:06d}",
        "candidate_family_id": cand_family,
        "candidate_revision_id": cand_rev,
        "decision_ordinal": 1,
        "decision_status": None,
        "canonical_family_id": None,
        "canonical_proposition": None,
        "accepted_members": [],
        "excluded_members": [],
        "variant_assignments": [],
        "split_points": [],
        "hierarchical_relations": [],
        "collision_dispositions": [],
        "unresolved_boundaries": [],
        "response_portability_status": "NOT_AUTHORIZED_BY_P3",
        "rationale": "Draft only: P3A generated live object graph evidence, but P3C adjudication is not authorized in this phase.",
        "evidence_bundle_hash": evidence_hash,
        "supersedes_adjudication_id": None,
        "authority_release_id": RELEASE_ID,
        "split_results": [],
        "variant_promotions": [],
        "exclusion_promotions": [],
    }
    packet["decision_form"] = decision
    return packet, decision


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", required=True)
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--limit", type=int, default=3)
    args = ap.parse_args()

    section = args.root / "53_P3A_V7_CONTRACT_BINDING_REPAIR_AND_PHASE3_RESUME"
    packet_dir = section / "candidate_packets"
    decision_dir = section / "draft_decisions"
    packet_dir.mkdir(parents=True, exist_ok=True)
    decision_dir.mkdir(parents=True, exist_ok=True)
    validation = []
    with psycopg.connect(args.dsn, row_factory=psycopg.rows.dict_row) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public")
        cur = conn.cursor()
        candidates = fetch_all(
            cur,
            """
            SELECT cr.*
            FROM p3_candidate_revision cr
            JOIN p3_candidate_membership cm ON cm.candidate_revision_id=cr.candidate_revision_id
            GROUP BY cr.candidate_revision_id, cr.candidate_family_id, cr.revision_number,
                     cr.candidate_classification, cr.candidate_origin_type, cr.origin_key,
                     cr.canonical_signature_id, cr.evidence_bundle_hash, cr.authority_release_id
            HAVING count(*) >= 2
            ORDER BY count(*) DESC, cr.candidate_revision_id
            LIMIT %s
            """,
            (args.limit,),
        )
        for ordinal, candidate in enumerate(candidates, 1):
            packet, decision = build_packet(cur, candidate, ordinal)
            packet_path = packet_dir / f"{packet['packet_id']}_{candidate['candidate_family_id']}.json"
            decision_path = decision_dir / f"{decision['adjudication_id']}_{candidate['candidate_family_id']}_DRAFT.json"
            packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            decision_path.write_text(json.dumps(decision, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(args.root / "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK/validation/validate_p3_candidate_packet_v7.py"), str(packet_path), str(decision_path)],
                text=True,
                capture_output=True,
                check=False,
            )
            validation.append(
                {
                    "packet_path": str(packet_path.relative_to(args.root)),
                    "decision_path": str(decision_path.relative_to(args.root)),
                    "returncode": proc.returncode,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                }
            )
    out = {"status": "PASS" if all(v["returncode"] == 0 for v in validation) and len(validation) == args.limit else "FAIL", "packets": validation}
    (section / "outputs/p3a_vertical_slice_packet_build_return.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))
    return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
