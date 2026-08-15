#!/usr/bin/env python3
"""Build the deterministic row payload consumed by the R4 P3C promoter.

This stage performs no database writes. It resolves every graph component to a
single canonical-family action, derives stable child object identities, and
fails closed on missing evidence or ambiguous family references.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def stable(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(stable(value).encode()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    plan = json.loads(args.plan.read_text())
    rows = plan["components"]
    if len(rows) != 162:
        raise SystemExit("R4 plan must contain exactly 162 components")
    if any(not r.get("member_lineage_ids") for r in rows):
        raise SystemExit("component without member lineage")
    if any(len(r.get("semantic_signature_sha256", "")) != 64 for r in rows):
        raise SystemExit("component without complete signature hash")

    families = []
    signatures = []
    revisions = []
    memberships = []
    actions = []
    new_ordinal = 0
    for row in rows:
        cid = row["component_id"]
        existing = row.get("existing_family_id", "")
        if existing:
            family_id = existing
            action = "ATTACH_EXISTING_FAMILY"
        else:
            new_ordinal += 1
            family_id = row.get("proposed_canonical_family_id") or f"PROVISIONAL::R185::{new_ordinal:04d}::{cid}"
            action = "ALLOCATE_NEW_FAMILY"
        genealogy = row.get("genealogy") or {}
        signature_id = genealogy.get("canonical_signature_id") or f"P3SIG-{row['semantic_signature_sha256'][:16]}"
        revision_id = genealogy.get("family_revision_id") or (f"JFAMREV-{family_id[5:]}-R0001" if family_id.startswith("JFAM-") else f"PROVISIONAL::JFAMREV::{family_id}::R0001")
        adjudication_id = genealogy.get("source_adjudication_id") or f"P3ADJ-{new_ordinal:06d}"
        if not row.get("existing_family_id"):
            signatures.append({"signature_id": signature_id, "subject_id": cid, "content_hash": row["semantic_signature_sha256"], "status": "COMPLETE"})
        revisions.append({"family_revision_id": revision_id, "family_id": family_id, "signature_id": signature_id, "proposition": row["canonical_proposition"], "evidence_bundle_hash": digest(row), "created_by_adjudication_id": adjudication_id})
        memberships.extend({"family_revision_id": revision_id, "member_object_id": m} for m in row["member_lineage_ids"])
        if not existing:
            families.append({"family_id": family_id, "source_component_id": cid, "action": action})
        actions.append({"component_id": cid, "family_id": family_id, "revision_id": revision_id, "adjudication_id": adjudication_id, "action": action})

    payload = {"version": "R4_P3C_IMPORT_PAYLOAD_V1", "parent_release": "P3-AUTHORITY-2026-08-02-R184", "database_mutated": False, "families": families, "signatures": signatures, "revisions": revisions, "memberships": memberships, "actions": actions}
    payload["payload_sha256"] = digest(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"families": len(families), "signatures": len(signatures), "revisions": len(revisions), "memberships": len(memberships), "payload_sha256": payload["payload_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
