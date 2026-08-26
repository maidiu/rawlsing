#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sys
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import psycopg
from psycopg.types.json import Jsonb

csv.field_size_limit(sys.maxsize)

CONTRACT_RELEASE = "P3-AUTHORITY-2026-08-02-R41"
BASE_RELEASE = "P3-AUTHORITY-2026-08-01-R40"
SIGNATURE_FIELDS = [
    "subject_role", "operator", "target", "object_or_outcome", "modality", "timeframe",
    "condition", "population_scope", "geographic_scope", "polarity", "derived_status", "parent_context",
]
DIRECT_FAMILY = "JFAM-000203"
DERIVED_FAMILY = "JFAM-000425"
DIRECT_PRAYER = {
    "p2lineage_426d1a3925832d5372cd1f71",
    "p2lineage_54355f0f436fb8696b623ecc",
    "p2lineage_e6156ffbabedac638c4d1759",
}
DERIVED_PRAYER = {"p2lineage_f0f18e2e584bc04b1b301b41"}
BOUNDARY_FAMILY_PAIRS = [
    ("JFAM-000168", "JFAM-000225", "PRESENT_DEMOCRACY_PLACEMENT_VS_TEN_YEARS_AGO"),
    ("JFAM-000199", "JFAM-000242", "LAST_ELECTION_VS_GENERAL_ELECTION_CONDUCT"),
    ("JFAM-000210", "JFAM-000234", "FIRST_RANKED_AIM_VS_SECOND_RANKED_AIM"),
    ("JFAM-000260", "JFAM-000236", "CATEGORICAL_RELIGIOUS_IDENTITY_VS_GRADED_RELIGIOSITY"),
    (DIRECT_FAMILY, DERIVED_FAMILY, "DIRECT_PRAYER_FREQUENCY_VS_CONSTRUCTED_PRAYER_RECODE"),
]


def cjson(v: Any) -> str:
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(v: Any) -> str:
    if not isinstance(v, str):
        v = cjson(v)
    return hashlib.sha256(v.encode("utf-8")).hexdigest()


def num(value: str) -> int:
    m = re.search(r"-(\d{6})(?:-|$)", value)
    if not m:
        raise ValueError(value)
    return int(m.group(1))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def option_count(text: str) -> int:
    text = (text or "").strip()
    if not text:
        return 0
    return len([x for x in text.split(" | ") if x.strip()])


def build_lineage_profiles(node_registry: Path) -> tuple[dict[str, str], dict[str, dict[str, Any]]]:
    by_lineage: dict[str, list[dict[str, Any]]] = defaultdict(list)
    with node_registry.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            lid = r.get("lineage_id", "").strip()
            if not lid:
                continue
            form = {
                "response_topology": r.get("response_topology", "").strip(),
                "response_family_expectation": r.get("response_family_expectation", "").strip(),
                "substantive_response_signature": r.get("substantive_response_signature", "").strip(),
                "response_option_count": option_count(r.get("response_options_substantive", "")),
                "response_options_substantive": " ".join(r.get("response_options_substantive", "").split()),
                "position_conditioning": r.get("position_conditioning", "").strip(),
                "position_modifiers": r.get("position_modifiers", "").strip(),
            }
            by_lineage[lid].append(form)
    profile_id: dict[str, str] = {}
    profile_payload: dict[str, dict[str, Any]] = {}
    for lid, forms in by_lineage.items():
        unique = {cjson(x): x for x in forms}
        payload = {"material_response_forms": [unique[k] for k in sorted(unique)]}
        pid = sha(payload)[:16]
        profile_id[lid] = pid
        profile_payload[pid] = payload
    return profile_id, profile_payload


class Allocator:
    def __init__(self) -> None:
        self.variant = 0
        self.exclusion = 400000
        self.genealogy = 0

    def variant_id(self) -> str:
        self.variant += 1
        return f"P3VAR-{self.variant:06d}"

    def exclusion_id(self) -> str:
        self.exclusion += 1
        return f"P3EXC-{self.exclusion:06d}"

    def genealogy_id(self) -> str:
        self.genealogy += 1
        return f"P3GEN-{self.genealogy:06d}"


def register(cur: psycopg.Cursor, object_id: str, object_type: str, release: str, origin_phase: str,
             authority_id: str | None, content_hash: str | None, note: str) -> None:
    cur.execute(
        """INSERT INTO p3_object_registry
        (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,
         allocation_release_id,retired_release_id,content_hash,stable_identity_note)
        VALUES (%s,%s,'REGISTRY_ALLOCATED_DURABLE_ID',%s,%s,%s,%s,NULL,%s,%s)""",
        (object_id, object_type, object_id, origin_phase, authority_id, release, content_hash, note),
    )
    ledger_hash = content_hash or sha({
        "object_id": object_id, "object_type": object_type, "release": release,
        "origin_phase": origin_phase, "authority_id": authority_id, "note": note,
    })
    cur.execute(
        """INSERT INTO p3_release_change_ledger
        (release_id,object_id,change_type,prior_content_hash,content_hash,reason)
        VALUES (%s,%s,'ADDED',NULL,%s,%s)""",
        (release, object_id, ledger_hash, f"{origin_phase}: {note}"),
    )


def register_content(cur: psycopg.Cursor, object_id: str, object_type: str, release: str, origin_phase: str,
                     authority_id: str | None, content_hash: str, note: str) -> None:
    cur.execute(
        """INSERT INTO p3_object_registry
        (object_id,object_type,identity_strategy,idempotency_key,origin_phase,origin_authority_id,
         allocation_release_id,retired_release_id,content_hash,stable_identity_note)
        VALUES (%s,%s,'CONTENT_ADDRESSED_DERIVED_ID',%s,%s,%s,%s,NULL,%s,%s)""",
        (object_id, object_type, object_id, origin_phase, authority_id, release, content_hash, note),
    )
    cur.execute(
        """INSERT INTO p3_release_change_ledger
        (release_id,object_id,change_type,prior_content_hash,content_hash,reason)
        VALUES (%s,%s,'ADDED',NULL,%s,%s)""",
        (release, object_id, content_hash, f"{origin_phase}: {note}"),
    )


def insert_release(cur: psycopg.Cursor, release: str, parent: str, ordinal: int, manifest_hash: str) -> None:
    cur.execute(
        """INSERT INTO p3_authority_release
        (release_id,parent_release_id,schema_version,builder_version,input_manifest_hash,created_at,
         object_counts,validation_return_hash,migration_artifact,rollback_artifact)
        VALUES (%s,%s,'p3-v7-p3c-governed-replay-v1','p3c-governed-replay-v1',%s,%s,%s,%s,%s,%s)""",
        (
            release, parent, manifest_hash,
            datetime(2026, 8, 2, 12, 0, tzinfo=timezone.utc) + timedelta(seconds=ordinal),
            Jsonb({"decision_ordinal": ordinal}),
            sha({
                "release_id": release,
                "manifest_hash": manifest_hash,
                "validation_contract": "DEFERRED_COMMIT_GATES_PLUS_POSTCLOSE_MATRIX_V1",
            }),
            "84_P3C_GOVERNED_REPLAY_CONTRACT_AND_EXECUTION/code/p3c_governed_replay_v1.py",
            "restore Section 83 PostgreSQL dump",
        ),
    )
    for table, cols in [
        ("p3_identity_key_contract", "object_type,identity_strategy,id_pattern,idempotency_key_spec"),
        ("p3_candidate_lifecycle_transition", "from_stage,to_stage,guard_text"),
        ("p3_release_lifecycle_transition", "from_status,to_status,guard_text"),
    ]:
        cur.execute(
            f"INSERT INTO {table}({cols},authority_release_id) SELECT {cols},%s FROM {table} WHERE authority_release_id=%s",
            (release, CONTRACT_RELEASE),
        )
    base_time = datetime(2026, 8, 2, 12, 0, tzinfo=timezone.utc) + timedelta(seconds=ordinal)
    events = [(1, "DRAFT", "1"), (2, "VALIDATED", "2"), (3, "SHADOW", "3"), (4, "PROMOTED", "4")]
    for event_ordinal, status, tag in events:
        cur.execute(
            "INSERT INTO p3_release_status_event VALUES (%s,%s,%s,%s,%s)",
            (release, event_ordinal, status, base_time + timedelta(microseconds=event_ordinal), sha({"release": release, "status": status, "tag": tag})),
        )


def candidate_lifecycle_to_decided(cur: psycopg.Cursor, family_id: str, revision_id: str, release: str,
                                   guard: str, start_ordinal: int = 2, start_stage: str = "DISCOVERED") -> None:
    stages = ["GENERATED_CANDIDATE", "EVIDENCE_COMPLETE", "ADJUDICATION_REQUIRED", "DECIDED"]
    prior = start_stage
    base_time = datetime(2026, 8, 2, 13, 0, tzinfo=timezone.utc)
    for i, stage in enumerate(stages, start=start_ordinal):
        cur.execute(
            """INSERT INTO p3_candidate_status_event
            (candidate_family_id,candidate_revision_id,event_ordinal,from_stage,to_stage,guard_evidence_id,occurred_at,authority_release_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (family_id, revision_id, i, prior, stage, guard, base_time + timedelta(seconds=i), release),
        )
        prior = stage


def materialize_split_successor(cur: psycopg.Cursor, n: int, member: str, parent_revision: str,
                                source_family: str, representative_text: str) -> tuple[str, str]:
    family_id = f"P3CAND-{n:06d}"
    revision_id = f"P3CANDREV-{n:06d}-R0001"
    origin_payload = {
        "origin_type": "P3C_SPLIT_SUCCESSOR", "parent_candidate_revision_id": parent_revision,
        "members": [member], "split_dimension": "DIRECT_VS_CONSTRUCTED_PRAYER_FREQUENCY",
    }
    origin_key = sha(origin_payload)
    snapshot_payload = {
        "candidate_revision_id": revision_id,
        "candidate_family_id": family_id,
        "candidate_origin_type": "P3C_SPLIT_SUCCESSOR",
        "members": [member],
        "parent_candidate_revision_id": parent_revision,
        "source_family": source_family,
        "representative_text": representative_text,
        "authority_effect": "EXACT_SINGLETON_SPLIT_SUCCESSOR",
    }
    evidence_hash = sha(snapshot_payload)
    register(cur, family_id, "CANDIDATE_FAMILY", CONTRACT_RELEASE, "P3C_SPLIT_MATERIALIZATION", parent_revision, origin_key,
             "Durable candidate family materialized from exact governed split-result partition.")
    register(cur, revision_id, "CANDIDATE_REVISION", CONTRACT_RELEASE, "P3C_SPLIT_MATERIALIZATION", family_id, evidence_hash,
             "Immutable exact singleton successor revision.")
    cur.execute("INSERT INTO p3_candidate_family VALUES (%s,%s)", (family_id, CONTRACT_RELEASE))
    cur.execute(
        """INSERT INTO p3_candidate_revision
        (candidate_revision_id,candidate_family_id,revision_number,candidate_classification,candidate_origin_type,
         origin_key,canonical_signature_id,evidence_bundle_hash,authority_release_id)
        VALUES (%s,%s,1,'SPLIT_RISK','P3C_SPLIT_SUCCESSOR',%s,NULL,%s,%s)""",
        (revision_id, family_id, origin_key, evidence_hash, CONTRACT_RELEASE),
    )
    cur.execute(
        "INSERT INTO p3_candidate_membership VALUES (%s,%s,'PROPOSED_MEMBER','P3C_SPLIT_RESULT',%s)",
        (revision_id, member, CONTRACT_RELEASE),
    )
    cur.execute(
        """INSERT INTO p3_candidate_evidence_snapshot
        VALUES (%s,'P3C_SPLIT_SUCCESSOR_EVIDENCE_V1',%s,%s,%s,%s)""",
        (revision_id, Jsonb(snapshot_payload), evidence_hash, CONTRACT_RELEASE, datetime(2026, 8, 2, 12, 0, tzinfo=timezone.utc)),
    )
    cur.execute(
        """INSERT INTO p3_candidate_family_origin_ledger
        VALUES (%s,%s,%s,%s,%s)""",
        (family_id, origin_key, sha(origin_payload), revision_id, CONTRACT_RELEASE),
    )
    cur.execute(
        """INSERT INTO p3_candidate_family_semantic_origin
        VALUES (%s,%s,'P3C_SPLIT_SUCCESSOR',%s,%s,%s,%s,'p3c-split-successor-v1',%s)""",
        (family_id, revision_id, Jsonb([member]), Jsonb([]), Jsonb([]), origin_key, CONTRACT_RELEASE),
    )
    cur.execute(
        """INSERT INTO p3_candidate_revision_genealogy
        VALUES (%s,%s,1,NULL,NULL,'NONE_NEW_SUCCESSOR_FAMILY','UNCHANGED_FAMILY_APPEND_REVISION',%s,%s)""",
        (revision_id, family_id, f"Exact successor of {parent_revision} governed split partition.", CONTRACT_RELEASE),
    )
    cur.execute(
        """INSERT INTO p3_candidate_ranking
        VALUES (%s,1,0,0,1.0,1,1,0.0,0,1,%s)""",
        (revision_id, CONTRACT_RELEASE),
    )
    # Exact pre-adjudication lifecycle in the contract release.
    stages = [(1, None, "DISCOVERED"), (2, "DISCOVERED", "GENERATED_CANDIDATE"),
              (3, "GENERATED_CANDIDATE", "EVIDENCE_COMPLETE"),
              (4, "EVIDENCE_COMPLETE", "ADJUDICATION_REQUIRED")]
    for i, prior, stage in stages:
        cur.execute(
            "INSERT INTO p3_candidate_status_event VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (family_id, revision_id, i, prior, stage, "P3C_SPLIT_SUCCESSOR_CONTRACT",
             datetime(2026, 8, 2, 12, 30, tzinfo=timezone.utc) + timedelta(seconds=i), CONTRACT_RELEASE),
        )
    return family_id, revision_id


def add_signature(cur: psycopg.Cursor, release: str, family_revision_id: str, proposition: dict[str, Any],
                  member_sources: list[str], derived: bool) -> str:
    values = {
        "subject_role": "SURVEY_RESPONDENT",
        "operator": "QUESTION_PROPOSITION_AS_WORDED",
        "target": " | ".join(proposition.get("semantic_content_ids", [])) or "SOURCE_DEFINED_TARGET",
        "object_or_outcome": " || ".join(proposition.get("representative_texts", [])) or "SOURCE_DEFINED_OBJECT_OR_OUTCOME",
        "modality": "SOURCE_WORDING_GOVERNED",
        "timeframe": "SOURCE_SPECIFIED_OR_UNSPECIFIED",
        "condition": "SOURCE_SPECIFIED_OR_UNSPECIFIED",
        "population_scope": "SURVEY_RESPONDENT_UNIVERSE_PRESERVED_BY_SOURCE",
        "geographic_scope": " | ".join(sorted(member_sources)),
        "polarity": "SOURCE_CODED_NOT_HARMONIZED",
        "derived_status": "CONSTRUCTED_DERIVED_RECODE" if derived else "DIRECT_SOURCE_ITEM_SET",
        "parent_context": "SOURCE_BATTERY_AND_ROUTING_CONTEXT_PRESERVED",
    }
    payload = {k: {"field_value": values[k], "evidence_state": "KNOWN", "confidence": "HIGH"} for k in SIGNATURE_FIELDS}
    content_hash = sha({"subject_id": family_revision_id, "fields": payload, "schema": "p3-signature-v1"})
    signature_id = f"P3SIG-{content_hash[:16]}"
    register_content(cur, signature_id, "PROPOSITION_SIGNATURE", release, "P3C_CANONICAL_SIGNATURE", family_revision_id,
                     content_hash, "Content-addressed complete canonical proposition signature.")
    cur.execute("INSERT INTO p3_proposition_signature VALUES (%s,%s,'COMPLETE',%s,%s)",
                (signature_id, family_revision_id, content_hash, release))
    for field in SIGNATURE_FIELDS:
        cur.execute("INSERT INTO p3_signature_field VALUES (%s,%s,%s,NULL,'KNOWN','HIGH')",
                    (signature_id, field, values[field]))
    return signature_id


def add_exclusion(cur: psycopg.Cursor, alloc: Allocator, release: str, owner: str, exclusion_type: str,
                  prohibited: str, rule: str, scope: str, excluded: list[str]) -> str:
    eid = alloc.exclusion_id()
    payload = {"owner": owner, "type": exclusion_type, "prohibited": prohibited, "rule": rule,
               "scope": scope, "excluded": sorted(excluded)}
    register(cur, eid, "FAMILY_EXCLUSION", release, "P3C_EXCLUSION", owner, sha(payload),
             "Governed canonical-family exclusion.")
    cur.execute(
        "INSERT INTO p3_family_exclusion VALUES (%s,%s,%s,%s,%s,%s,true,%s)",
        (eid, owner, exclusion_type, prohibited, rule, scope, release),
    )
    for member in sorted(excluded):
        cur.execute("INSERT INTO p3_excluded_object VALUES (%s,%s)", (eid, member))
    return eid


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", required=True)
    ap.add_argument("--section", type=Path, required=True)
    ap.add_argument("--node-registry", type=Path, required=True)
    args = ap.parse_args()
    sec = args.section
    inputs = sec / "inputs"
    outputs = sec / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)

    candidate_rows = read_csv(inputs / "P3C_EVIDENCE_FIRST_CANDIDATE_INVENTORY.csv")
    member_rows = read_csv(inputs / "P3C_EVIDENCE_FIRST_MEMBER_MAP.csv")
    family_rows = read_csv(inputs / "P3C_FINAL_PROPOSITION_FAMILY_MAP.csv")
    candidate_by_revision = {r["candidate_revision_id"]: r for r in candidate_rows}
    members_by_candidate: dict[str, list[str]] = defaultdict(list)
    source_by_member: dict[str, str] = {}
    text_by_member: dict[str, str] = {}
    final_family_by_member: dict[str, str] = {}
    for r in member_rows:
        members_by_candidate[r["candidate_revision_id"]].append(r["member_object_id"])
        source_by_member[r["member_object_id"]] = r["source_family"]
        text_by_member[r["member_object_id"]] = r["representative_text"]
        final_family_by_member[r["member_object_id"]] = r["final_canonical_family_id"]
    family_meta = {r["canonical_family_id"]: r for r in family_rows}
    final_members_by_family: dict[str, set[str]] = defaultdict(set)
    for m, fam in final_family_by_member.items():
        final_members_by_family[fam].add(m)
    profile_by_member, profile_payloads = build_lineage_profiles(args.node_registry)
    missing_profiles = sorted(set(final_family_by_member) - set(profile_by_member))
    if missing_profiles:
        raise RuntimeError(f"node registry lacks material response profile for {len(missing_profiles)} lineages: {missing_profiles[:5]}")

    # Exact replay order: split parent followed immediately by its two exact successors.
    originals = sorted(candidate_by_revision, key=num)
    sequence: list[str] = []
    for rid in originals:
        sequence.append(rid)
        if num(rid) == 252:
            sequence.extend(["P3CANDREV-000424-R0001", "P3CANDREV-000425-R0001"])
    if len(sequence) != 143:
        raise RuntimeError(len(sequence))

    alloc = Allocator()
    family_state: dict[str, set[str]] = defaultdict(set)
    family_latest_revision: dict[str, str] = {}
    family_revision_count: dict[str, int] = defaultdict(int)
    canonical_variant_state: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    boundary_installed: set[tuple[str, str, str]] = set()
    decision_output: list[dict[str, Any]] = []
    variant_output: list[dict[str, Any]] = []
    exclusion_output: list[dict[str, Any]] = []
    release_output: list[dict[str, Any]] = []
    manifest_hash = sha({"candidate_inventory": candidate_rows, "family_map": family_rows,
                         "profile_payloads": profile_payloads})

    with psycopg.connect(args.dsn, autocommit=False) as conn:
        cur = conn.cursor()
        cur.execute("SET CONSTRAINTS ALL DEFERRED")
        # Baseline evidence surfaces.
        candidate_db = {r[0]: {"family": r[1], "hash": r[2]} for r in cur.execute(
            "SELECT candidate_revision_id,candidate_family_id,evidence_bundle_hash FROM p3_candidate_revision")}
        obligations: dict[str, list[dict[str, str]]] = defaultdict(list)
        for oid, rid, l, r, typ in cur.execute(
            "SELECT closure_obligation_id,candidate_revision_id,left_object_id,right_object_id,obligation_type FROM p3_replay_obligation_baseline ORDER BY closure_obligation_id"):
            obligations[rid].append({"id": oid, "left": l, "right": r, "type": typ})
        collisions: dict[str, list[tuple[str, str]]] = defaultdict(list)
        for rid, cid in cur.execute("SELECT candidate_revision_id,collision_id FROM p3_internal_pair_collision ORDER BY candidate_revision_id,collision_id"):
            collisions[rid].append((cid, rid))
        stronger: dict[str, list[dict[str, str]]] = defaultdict(list)
        for rid, l, r, key in cur.execute("SELECT candidate_revision_id,left_object_id,right_object_id,coalesce(direct_pair_projection_id,left_object_id||':'||right_object_id) FROM p3_internal_pair_matrix WHERE pair_state='HIERARCHICAL_ONLY'"):
            stronger[rid].append({"kind": "HIERARCHICAL_ONLY", "key": key, "left": l, "right": r})
        for table, kind in [("p3_internal_pair_unresolved_boundary", "UNRESOLVED_BOUNDARY"),
                            ("p3_internal_pair_redirect_boundary", "REDIRECT_BOUNDARY"),
                            ("p3_internal_pair_coordinate_constraint", "COORDINATE_CONSTRAINT")]:
            for rid, l, r, key in cur.execute(f"SELECT candidate_revision_id,left_object_id,right_object_id,projection_id FROM {table}"):
                stronger[rid].append({"kind": kind, "key": key, "left": l, "right": r})

        # Exact split successors are materialized before the parent split decision.
        direct_member = next(m for m in members_by_candidate["P3CANDREV-000252-R0002"] if m in DIRECT_PRAYER)
        derived_member = next(m for m in members_by_candidate["P3CANDREV-000252-R0002"] if m in DERIVED_PRAYER)
        fam424, rev424 = materialize_split_successor(cur, 424, direct_member, "P3CANDREV-000252-R0002",
                                                     source_by_member[direct_member], text_by_member[direct_member])
        fam425, rev425 = materialize_split_successor(cur, 425, derived_member, "P3CANDREV-000252-R0002",
                                                     source_by_member[derived_member], text_by_member[derived_member])
        members_by_candidate[rev424] = [direct_member]
        members_by_candidate[rev425] = [derived_member]
        candidate_db[rev424] = {"family": fam424, "hash": sha({"successor": rev424, "member": direct_member})}
        candidate_db[rev425] = {"family": fam425, "hash": sha({"successor": rev425, "member": derived_member})}
        # Use the actual immutable hashes inserted above.
        for rid, h in cur.execute("SELECT candidate_revision_id,evidence_bundle_hash FROM p3_candidate_revision WHERE candidate_revision_id IN (%s,%s)", (rev424, rev425)):
            candidate_db[rid]["hash"] = h

        parent_release = CONTRACT_RELEASE
        decision_ordinal = 0
        for rid in sequence:
            decision_ordinal += 1
            release_number = 41 + decision_ordinal
            release = f"P3-AUTHORITY-2026-08-02-R{release_number}"
            insert_release(cur, release, parent_release, decision_ordinal, manifest_hash)
            parent_release = release
            aid = f"P3ADJ-{decision_ordinal:06d}"
            register(cur, aid, "ADJUDICATION", release, "P3C_GOVERNED_REPLAY", rid,
                     sha({"adjudication": aid, "candidate": rid}), "Durable governed P3C adjudication.")
            n = num(rid)
            candidate_family = candidate_db[rid]["family"]
            candidate_members = sorted(members_by_candidate[rid])
            is_split = n == 252
            if rid == rev424:
                target_family = DIRECT_FAMILY
            elif rid == rev425:
                target_family = DERIVED_FAMILY
            else:
                target_family = candidate_by_revision[rid]["primary_family_id"]

            if is_split:
                decision_status = "SPLIT_REQUIRED"
                proposition = None
                rationale = ("The candidate combines a direct prayer-frequency item with a constructed WVS prayer recode. "
                             "The measures are proposition-near but identity-distinct and must be materialized as disjoint successors.")
                decision_hash = sha({"candidate": rid, "status": decision_status, "members": candidate_members,
                                     "split": [sorted(DIRECT_PRAYER & set(candidate_members)), sorted(DERIVED_PRAYER & set(candidate_members))]})
                cur.execute(
                    """INSERT INTO p3_adjudication_decision
                    VALUES (%s,%s,1,%s,NULL,NULL,'NOT_AUTHORIZED_BY_P3',%s,%s,NULL,%s,%s)""",
                    (aid, rid, decision_status, rationale, decision_hash, release,
                     datetime(2026, 8, 2, 14, 0, tzinfo=timezone.utc) + timedelta(seconds=decision_ordinal)),
                )
                for m in candidate_members:
                    cur.execute("INSERT INTO p3_adjudication_member VALUES (%s,%s,'SPLIT',NULL)", (aid, m))
                cur.execute("INSERT INTO p3_adjudication_split_point VALUES (%s,1,%s,%s)",
                            (aid, "DIRECT_VS_CONSTRUCTED_PRAYER_FREQUENCY", rationale))
                for m in candidate_members:
                    side = "LEFT" if m in DIRECT_PRAYER else "RIGHT"
                    cur.execute("INSERT INTO p3_adjudication_split_member VALUES (%s,1,%s,%s)", (aid, side, m))
                result_defs = [(1, fam424, [direct_member], "Direct prayer-frequency successor."),
                               (2, fam425, [derived_member], "Constructed prayer-recode successor.")]
                for result_ord, successor, result_members, rr in result_defs:
                    origin_key = sha({"parent": rid, "successor": successor, "members": sorted(result_members)})
                    cur.execute("INSERT INTO p3_adjudication_split_result VALUES (%s,%s,%s,%s,%s)",
                                (aid, result_ord, successor, origin_key, rr))
                    for m in result_members:
                        cur.execute("INSERT INTO p3_adjudication_split_result_member VALUES (%s,%s,%s)", (aid, result_ord, m))
                cur.execute("INSERT INTO p3_singleton_split_authority VALUES (%s,%s,%s,%s,%s,%s)",
                            (rev424, aid, rid, direct_member, sha({"parent": aid, "member": direct_member}), release))
                cur.execute("INSERT INTO p3_singleton_split_authority VALUES (%s,%s,%s,%s,%s,%s)",
                            (rev425, aid, rid, derived_member, sha({"parent": aid, "member": derived_member}), release))
            else:
                previous = set(family_state[target_family])
                excluded = set()
                if n == 264:
                    excluded = set(candidate_members) & DERIVED_PRAYER
                admitted = set(candidate_members) - excluded
                accepts = admitted - previous
                already = admitted & previous
                result_members = previous | accepts
                if not result_members:
                    raise RuntimeError((rid, target_family, "empty canonical result"))
                result_profiles = {profile_by_member[m] for m in result_members}
                decision_status = "ACCEPTED_WITH_VARIANTS" if len(result_profiles) > 1 else "ACCEPTED_CANONICAL"
                semantic_ids = [x.strip() for x in family_meta[target_family]["semantic_content_ids"].split(" | ") if x.strip()]
                representative_texts = [x.strip() for x in family_meta[target_family]["representative_texts"].split(" || ") if x.strip()]
                proposition = {
                    "canonical_family_id": target_family,
                    "semantic_content_ids": semantic_ids,
                    "representative_texts": representative_texts,
                    "member_lineages": sorted(result_members),
                    "authority_effect": "QUESTION_PROPOSITION_IDENTITY_ONLY",
                    "response_portability_status": "NOT_AUTHORIZED_BY_P3",
                    "source_context_preserved": True,
                }
                rationale = ("Complete source wording, parent context, candidate membership, P2 pair evidence, and the Section 83 "
                             "evidence-first family map support proposition identity. Response-value portability remains unauthorized.")
                if n in (179, 187):
                    rationale += " The inherited collision is explicitly disposed below and does not negate the restored proposition identity."
                if n == 188:
                    rationale += " The abortion item is governed by its justifiability-battery operator; the shorter label cannot erase that parent context."
                if n == 264:
                    rationale += " The constructed prayer recode is explicitly excluded from the direct prayer-frequency family."
                decision_hash = sha({"candidate": rid, "status": decision_status, "family": target_family,
                                     "accepts": sorted(accepts), "already": sorted(already), "excluded": sorted(excluded),
                                     "proposition": proposition})
                # The family registry object must exist before the decision's immediate object-registry FK.
                new_family = target_family not in family_latest_revision
                if new_family:
                    register(cur, target_family, "CANONICAL_FAMILY", release, "P3C_CANONICAL_PROMOTION", aid,
                             sha({"family": target_family, "seed_adjudication": aid}),
                             "Durable canonical proposition family.")
                cur.execute(
                    """INSERT INTO p3_adjudication_decision
                    VALUES (%s,%s,1,%s,%s,%s,'NOT_AUTHORIZED_BY_P3',%s,%s,NULL,%s,%s)""",
                    (aid, rid, decision_status, target_family, Jsonb(proposition), rationale, decision_hash, release,
                     datetime(2026, 8, 2, 14, 0, tzinfo=timezone.utc) + timedelta(seconds=decision_ordinal)),
                )
                if new_family:
                    cur.execute("INSERT INTO p3_canonical_family VALUES (%s,%s,%s,NULL)", (target_family, aid, release))

                # Candidate variants are created for every admitted profile when the resulting family is variant-bearing.
                candidate_variant_for_profile: dict[str, str] = {}
                canonical_variant_for_profile: dict[str, str] = {}
                if decision_status == "ACCEPTED_WITH_VARIANTS":
                    candidate_profiles = sorted({profile_by_member[m] for m in admitted})
                    for pid in candidate_profiles:
                        vid = alloc.variant_id()
                        vrev = f"P3VARREV-{num(vid):06d}-R0001"
                        payload = profile_payloads[pid]
                        register(cur, vid, "FAMILY_VARIANT", release, "P3C_CANDIDATE_VARIANT", candidate_family,
                                 sha({"owner": candidate_family, "profile": pid}), "Candidate response-form variant.")
                        register(cur, vrev, "FAMILY_VARIANT_REVISION", release, "P3C_CANDIDATE_VARIANT", vid,
                                 sha({"variant": vid, "revision": 1, "payload": payload}), "Candidate response-form variant revision.")
                        cur.execute("INSERT INTO p3_family_variant VALUES (%s,%s,%s)", (vid, candidate_family, release))
                        cur.execute("INSERT INTO p3_family_variant_revision VALUES (%s,%s,1,'SOURCE_RESPONSE_FORM',%s,'NOT_AUTHORIZED_BY_P3',%s)",
                                    (vrev, vid, cjson(payload), release))
                        for m in sorted(x for x in admitted if profile_by_member[x] == pid):
                            cur.execute("INSERT INTO p3_variant_membership VALUES (%s,%s)", (vrev, m))
                        candidate_variant_for_profile[pid] = vrev

                    for pid in sorted(result_profiles):
                        state = canonical_variant_state[target_family].get(pid)
                        current_profile_members = sorted(m for m in result_members if profile_by_member[m] == pid)
                        if pid in candidate_variant_for_profile:
                            if state is None:
                                cvid = alloc.variant_id()
                                state = {"variant_id": cvid, "revision": 0, "latest_revision": None, "members": set()}
                                canonical_variant_state[target_family][pid] = state
                                register(cur, cvid, "FAMILY_VARIANT", release, "P3C_CANONICAL_VARIANT", target_family,
                                         sha({"owner": target_family, "profile": pid}), "Canonical response-form variant.")
                                cur.execute("INSERT INTO p3_family_variant VALUES (%s,%s,%s)", (cvid, target_family, release))
                            state["revision"] += 1
                            crev = f"P3VARREV-{num(state['variant_id']):06d}-R{state['revision']:04d}"
                            register(cur, crev, "FAMILY_VARIANT_REVISION", release, "P3C_CANONICAL_VARIANT",
                                     state["variant_id"], sha({"variant": state["variant_id"], "revision": state["revision"], "members": current_profile_members}),
                                     "Append-only canonical response-form variant revision.")
                            cur.execute("INSERT INTO p3_family_variant_revision VALUES (%s,%s,%s,'SOURCE_RESPONSE_FORM',%s,'NOT_AUTHORIZED_BY_P3',%s)",
                                        (crev, state["variant_id"], state["revision"], cjson(profile_payloads[pid]), release))
                            for m in current_profile_members:
                                cur.execute("INSERT INTO p3_variant_membership VALUES (%s,%s)", (crev, m))
                            cur.execute("INSERT INTO p3_variant_promotion VALUES (%s,%s,%s)",
                                        (aid, candidate_variant_for_profile[pid], crev))
                            state["latest_revision"] = crev
                            state["members"] = set(current_profile_members)
                            variant_output.append({"adjudication_id": aid, "candidate_revision_id": rid,
                                                   "canonical_family_id": target_family, "profile_id": pid,
                                                   "candidate_variant_revision_id": candidate_variant_for_profile[pid],
                                                   "canonical_variant_revision_id": crev,
                                                   "canonical_profile_member_count": len(current_profile_members)})
                        if state is None or state["latest_revision"] is None:
                            raise RuntimeError((rid, target_family, pid, "missing canonical variant state"))
                        canonical_variant_for_profile[pid] = state["latest_revision"]

                for m in candidate_members:
                    if m in excluded:
                        disposition, vrev = "EXCLUDE", None
                    elif m in accepts:
                        disposition = "ACCEPT"
                        vrev = candidate_variant_for_profile.get(profile_by_member[m])
                    elif m in already:
                        disposition = "ALREADY_CANONICAL"
                        vrev = candidate_variant_for_profile.get(profile_by_member[m])
                    else:
                        raise RuntimeError((rid, m, previous, excluded))
                    cur.execute("INSERT INTO p3_adjudication_member VALUES (%s,%s,%s,%s)", (aid, m, disposition, vrev))

                family_revision_count[target_family] += 1
                revision_number = family_revision_count[target_family]
                frev = f"JFAMREV-{num(target_family):06d}-R{revision_number:04d}"
                revision_hash = sha({"family": target_family, "revision": revision_number,
                                     "members": sorted(result_members), "proposition": proposition,
                                     "adjudication": aid})
                register(cur, frev, "CANONICAL_FAMILY_REVISION", release, "P3C_CANONICAL_PROMOTION", target_family,
                         revision_hash, "Immutable append-only canonical family revision.")
                sources = sorted({source_by_member[m] for m in result_members})
                signature_id = add_signature(cur, release, frev, proposition, sources, target_family == DERIVED_FAMILY)
                cur.execute(
                    """INSERT INTO p3_canonical_family_revision
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (frev, target_family, revision_number, signature_id, Jsonb(proposition), revision_hash, aid, release),
                )
                predecessor = family_latest_revision.get(target_family)
                if predecessor is None:
                    extension_rule = "NEW_FAMILY"
                elif accepts:
                    extension_rule = "PREDECESSOR_UNION_NEW_ACCEPTS"
                else:
                    extension_rule = "EVIDENCE_ONLY_CONFIRMATION"
                cur.execute("INSERT INTO p3_family_revision_predecessor VALUES (%s,%s,%s,%s,%s)",
                            (frev, predecessor, sha(sorted(previous)), extension_rule, release))
                for m in sorted(result_members):
                    cv = canonical_variant_for_profile.get(profile_by_member[m]) if decision_status == "ACCEPTED_WITH_VARIANTS" else None
                    cur.execute("INSERT INTO p3_canonical_family_membership VALUES (%s,%s,%s)", (frev, m, cv))
                family_state[target_family] = set(result_members)
                family_latest_revision[target_family] = frev

                rule_id = add_exclusion(
                    cur, alloc, release, target_family, "RULE_BASED", "UNAUTHORIZED_PROPOSITION_OR_VALUE_COLLAPSE",
                    "Only exact governed proposition members are canonical; response values, scoring, and respondent joins remain downstream authority surfaces.",
                    f"canonical_family_revision={frev}", [],
                )
                exclusion_output.append({"adjudication_id": aid, "exclusion_id": rule_id, "owner": target_family,
                                         "type": "RULE_BASED", "excluded_member_count": 0})
                if excluded:
                    named_id = add_exclusion(cur, alloc, release, target_family, "NAMED_MEMBER",
                                             "DIRECT_CONSTRUCTED_PRAYER_IDENTITY_COLLAPSE",
                                             "A constructed prayer recode cannot be admitted as a direct prayer-frequency member.",
                                             f"candidate_revision={rid}", sorted(excluded))
                    exclusion_output.append({"adjudication_id": aid, "exclusion_id": named_id, "owner": target_family,
                                             "type": "NAMED_MEMBER", "excluded_member_count": len(excluded)})

                # Install reciprocal real near-neighbour boundaries once both canonical families exist.
                for left_fam, right_fam, code in BOUNDARY_FAMILY_PAIRS:
                    key = (left_fam, right_fam, code)
                    if key in boundary_installed:
                        continue
                    if left_fam in family_latest_revision and right_fam in family_latest_revision:
                        left_excluded = sorted(family_state[right_fam])
                        right_excluded = sorted(family_state[left_fam])
                        le = add_exclusion(cur, alloc, release, left_fam, "NAMED_MEMBER", code,
                                           f"Named semantic boundary: {code}.", "RECIPROCAL_NEAR_NEIGHBOUR_BOUNDARY", left_excluded)
                        re = add_exclusion(cur, alloc, release, right_fam, "NAMED_MEMBER", code,
                                           f"Named semantic boundary: {code}.", "RECIPROCAL_NEAR_NEIGHBOUR_BOUNDARY", right_excluded)
                        exclusion_output.extend([
                            {"adjudication_id": aid, "exclusion_id": le, "owner": left_fam, "type": "NAMED_MEMBER", "excluded_member_count": len(left_excluded)},
                            {"adjudication_id": aid, "exclusion_id": re, "owner": right_fam, "type": "NAMED_MEMBER", "excluded_member_count": len(right_excluded)},
                        ])
                        boundary_installed.add(key)

            # Collision dispositions and stronger-boundary resolutions are exact and mandatory for accepted decisions.
            for collision_id, _ in collisions.get(rid, []):
                disposition = "OUT_OF_SCOPE_REDIRECT_DOES_NOT_NEGATE_RESTORED_PROPOSITION_IDENTITY"
                rationale_collision = ("The collision is preserved as upstream history. Complete wording, battery context, and the governed family map "
                                       "show that its scope does not negate proposition identity; value portability remains denied.")
                cur.execute("INSERT INTO p3_adjudication_collision_disposition VALUES (%s,%s,%s,%s)",
                            (aid, collision_id, disposition, rationale_collision))
            for b in stronger.get(rid, []):
                if n == 188:
                    disposition = "CONTEXT_RESTORED_ACCEPT"
                    brationale = "The parent justifiability battery restores the operator omitted by the short source label."
                else:
                    disposition = "PROPOSITION_IDENTITY_ACCEPT_VALUE_PORTABILITY_DENIED"
                    brationale = "The stronger-boundary evidence is preserved; complete source context supports proposition identity only, not value portability."
                cur.execute(
                    """INSERT INTO p3_adjudication_stronger_boundary_resolution
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (aid, b["kind"], b["key"], b["left"], b["right"], disposition, brationale,
                     sha({"candidate": rid, "boundary": b, "disposition": disposition}), release),
                )

            # Resolve every original P3A pair obligation exactly once.
            for o in obligations.get(rid, []):
                lf = final_family_by_member[o["left"]]
                rf = final_family_by_member[o["right"]]
                if is_split or lf != rf:
                    resolution = "RESOLVED_SPLIT"
                    rrationale = "The pair crosses an explicitly governed proposition-identity boundary."
                elif n == 264 and (o["left"] in DERIVED_PRAYER or o["right"] in DERIVED_PRAYER):
                    resolution = "RESOLVED_EXCLUDE"
                    rrationale = "The constructed prayer recode is explicitly excluded from the direct prayer family."
                else:
                    resolution = "RESOLVED_ACCEPT"
                    rrationale = "Complete wording and context support proposition identity; response portability remains unauthorized."
                cur.execute("INSERT INTO p3_adjudication_pair_resolution VALUES (%s,%s,%s,%s,%s,%s)",
                            (aid, o["id"], resolution, rrationale,
                             sha({"obligation": o["id"], "adjudication": aid, "resolution": resolution}), release))
                cur.execute("UPDATE p3_closure_obligation SET status=%s,resolution_adjudication_id=%s WHERE closure_obligation_id=%s",
                            (resolution, aid, o["id"]))

            # Every candidate ends in DECIDED. Existing candidates begin with DISCOVERED; split successors already have four events.
            if rid in (rev424, rev425):
                cur.execute(
                    "INSERT INTO p3_candidate_status_event VALUES (%s,%s,5,'ADJUDICATION_REQUIRED','DECIDED',%s,%s,%s)",
                    (candidate_family, rid, aid,
                     datetime(2026, 8, 2, 15, 0, tzinfo=timezone.utc) + timedelta(seconds=decision_ordinal), release),
                )
            else:
                candidate_lifecycle_to_decided(cur, candidate_family, rid, release, aid)

            decision_output.append({
                "decision_ordinal": decision_ordinal, "adjudication_id": aid, "candidate_revision_id": rid,
                "decision_status": decision_status, "canonical_family_id": "" if is_split else target_family,
                "authority_release_id": release, "candidate_member_count": len(candidate_members),
                "open_obligations_resolved": len(obligations.get(rid, [])),
                "collision_dispositions": len(collisions.get(rid, [])),
                "stronger_boundary_resolutions": len(stronger.get(rid, [])),
            })
            release_output.append({"release_id": release, "parent_release_id": release if False else (CONTRACT_RELEASE if decision_ordinal == 1 else f"P3-AUTHORITY-2026-08-02-R{release_number-1}"),
                                   "decision_ordinal": decision_ordinal, "adjudication_id": aid})

        final_release = parent_release
        # Exact final lineage-disposition snapshot at the promoted replay release.
        canonical_owner = {m: fam for fam, members in family_state.items() for m in members}
        baseline_disposition = {r[0]: r[1] for r in cur.execute(
            "SELECT subject_id,disposition_status FROM p3_lineage_disposition WHERE authority_release_id=%s", (BASE_RELEASE,))}
        lineage_ids = [r[0] for r in cur.execute(
            "SELECT object_id FROM p3_object_registry WHERE object_type='IMPORTED_SOURCE_LOCAL_LINEAGE' ORDER BY object_id")]
        for lid in lineage_ids:
            if lid in canonical_owner:
                status = "CANONICAL_MEMBER"
                fam = canonical_owner[lid]
                reason = "Member of the final evidence-derived P3C canonical proposition-family surface."
                evidence = [family_latest_revision[fam]]
            elif baseline_disposition.get(lid) == "CONSTRAINT_ONLY_PRESERVED":
                status = "CONSTRAINT_ONLY_PRESERVED"
                fam = None
                reason = "Preserved as a noncanonical constraint-only lineage."
                evidence = ["P3A_V40_CONSTRAINT_ONLY_DISPOSITION"]
            else:
                status = "SOURCE_LOCAL_SINGLETON_PRESERVED"
                fam = None
                reason = "Not admitted to a canonical family; source-local identity is preserved."
                evidence = ["P3C_FINAL_NO_CANONICAL_ADMISSION"]
            cur.execute("INSERT INTO p3_lineage_disposition VALUES (%s,'IMPORTED_SOURCE_LOCAL_LINEAGE',%s,%s,%s,%s,%s)",
                        (lid, status, reason, fam, Jsonb(evidence), final_release))
        cur.execute("INSERT INTO p3_runtime_promotion_pointer VALUES (true,%s,%s,%s)",
                    (final_release, datetime(2026, 8, 2, 16, 0, tzinfo=timezone.utc),
                     sha({"final_release": final_release, "family_map_hash": manifest_hash})))

        # Commit-time deferred constraints are the decisive replay gate.
        conn.commit()

    summary = {
        "status": "PASS",
        "contract_release_id": CONTRACT_RELEASE,
        "final_authority_release_id": "P3-AUTHORITY-2026-08-02-R184",
        "adjudication_decisions": len(decision_output),
        "accepted_decisions": sum(r["decision_status"].startswith("ACCEPTED") for r in decision_output),
        "split_decisions": sum(r["decision_status"] == "SPLIT_REQUIRED" for r in decision_output),
        "canonical_families": len(family_state),
        "canonical_family_revisions": sum(family_revision_count.values()),
        "pair_obligations_resolved": sum(r["open_obligations_resolved"] for r in decision_output),
        "collision_dispositions": sum(r["collision_dispositions"] for r in decision_output),
        "stronger_boundary_resolutions": sum(r["stronger_boundary_resolutions"] for r in decision_output),
        "variant_promotions": len(variant_output),
        "family_exclusions": len(exclusion_output),
        "final_family_map_hash": sha({f: sorted(m) for f, m in sorted(family_state.items())}),
        "source_inventory_family_map_hash": sha({f: sorted(m) for f, m in sorted(final_members_by_family.items())}),
        "non_authoritative_recovery_records_used_as_decision_input": False,
    }
    if summary["adjudication_decisions"] != 143 or summary["accepted_decisions"] != 142 or summary["split_decisions"] != 1:
        raise RuntimeError(summary)
    if summary["canonical_families"] != 111 or summary["canonical_family_revisions"] != 142:
        raise RuntimeError(summary)
    if summary["pair_obligations_resolved"] != 345:
        raise RuntimeError(summary)
    if summary["final_family_map_hash"] != summary["source_inventory_family_map_hash"]:
        raise RuntimeError("final database family map diverges from Section 83 authority map")

    write_csv(outputs / "P3C_GOVERNED_REPLAY_DECISIONS.csv", decision_output)
    write_csv(outputs / "P3C_GOVERNED_REPLAY_VARIANT_PROMOTIONS.csv", variant_output)
    write_csv(outputs / "P3C_GOVERNED_REPLAY_EXCLUSIONS.csv", exclusion_output)
    write_csv(outputs / "P3C_GOVERNED_REPLAY_RELEASE_CHAIN.csv", release_output)
    (outputs / "P3C_GOVERNED_REPLAY_RETURN.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
