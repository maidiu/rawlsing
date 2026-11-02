#!/usr/bin/env python3
"""Initialize the clean R3 operating state and quarantine historical demo bytes.

This script is idempotent for the journal: it refuses to append a second
GENESIS.  It never rewrites the original historical receipt at the repository
root; an exact copy and SHA-256 are preserved under quarantine/.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import evidence_store
import living_reference as lr

ROOT = Path(__file__).resolve().parent
EXCLUDED = [
    {"history_id": "R2_DEMO_H0003", "kind": "TRANSITION_HOLD", "reason": "SYNTHETIC_DEMO source disqualification of S5; not operating evidence."},
    {"history_id": "R2_DEMO_H0004", "kind": "AUTHORIZED_TRANSITION", "reason": "Self-declared SOURCEFREE_REVIEW PASS; reviewer_role=INDEPENDENT_I3_ENGINEER written by the same worker. Not independent acceptance."},
    {"history_id": "R2_DEMO_H0005", "kind": "AUTHORIZED_TRANSITION", "reason": "Self-declared engineering INDEPENDENT_ACCEPT_SCOPED derived from the same synthetic review."},
    {"history_id": "R2_DEMO_H0006", "kind": "AUTHORIZED_TRANSITION", "reason": "Repair following the synthetic withdrawal; the source record is valid but the event chain is contaminated. Clean state takes S5 from frozen source-backed seeds."},
    {"history_id": "R2_DEMO_H0007", "kind": "INTAKE_RETURN_CANDIDATE", "reason": "Synthetic SOROK_R2_NEW_REQUIREMENT and repeated-a return SHA; not a real returned artifact."},
    {"history_id": "R2_DEMO_H0008", "kind": "TRANSITION_HOLD", "reason": "Unverified OWNER_GRANT preserved as a pending example only; clean state carries no owner adoption."},
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def quarantine() -> dict:
    target = lr.QUARANTINE
    target.mkdir(parents=True, exist_ok=True)
    files = []
    for source in (lr.STATE, lr.SNAPSHOT, ROOT / "r2_live_transaction.json"):
        destination = target / source.name
        if source.exists() and not destination.exists():
            shutil.copy2(source, destination)
        if destination.exists():
            files.append({
                "original_path": str(source.relative_to(ROOT)),
                "preserved_path": str(destination.relative_to(ROOT)),
                "sha256": sha256(destination),
                "size": destination.stat().st_size,
            })
    manifest = {
        "schema": "SOROK_PROGRAMMA_QUARANTINE_MANIFEST@1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "HISTORICAL_DEMONSTRATION_EVIDENCE__NOT_OPERATING_STATE",
        "preserved_files": files,
        "excluded_history": EXCLUDED,
        "explanation": "The R2 live transaction manufactured SOURCEFREE_REVIEW/PASS and a synthetic requirement, then wrote the resulting state and snapshot. Those bytes are preserved here exactly and are not replayed into the clean operating state. The root r2_live_transaction.json remains the original historical receipt; its exact copy is here and the demo now defaults to a temporary state.",
    }
    (target / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (target / "README.md").write_text(
        "# Quarantined historical demonstration evidence\n\n"
        "These files preserve the contaminated O-LIVE R2 demonstration bytes. They are not operating state, evidence of independent review, or scientific acceptance.\n\n"
        "Excluded history identities: " + ", ".join(x["history_id"] for x in EXCLUDED) + ".\n",
        encoding="utf-8")
    return manifest


def initialize() -> dict:
    manifest = quarantine()
    journal = lr.JOURNAL
    journal.parent.mkdir(parents=True, exist_ok=True)
    existing = evidence_store.read_journal(journal)
    if not existing:
        patch = lr._load(lr.OSCIENCE_PATCH)
        events = [
            lr._event("GENESIS", {
                "baseline_sha": lr.ENGINEERING_BASELINE,
                "olive_source_sha": lr.OLIVE_SOURCE_SHA,
                "seed_build_premain": lr.SEED_BUILD_PREMAIN,
                "seed_schema": lr.SCHEMA,
                "p1_seed_schema": "SOROK_PROGRAMMA_P1_SEED@1",
                "note": "Clean R3 operating state reconstructed from source-backed seeds and qualified nonfixture events.",
            }, created_at="2026-11-01T18:00:00+00:00"),
            lr._event("CANDIDATE_EVIDENCE", {
                "importer": "OSCIENCE",
                "patch_file": lr.OSCIENCE_PATCH.name,
                "patch_digest": lr._digest(patch),
                "source_commit": lr.OSCIENCE_CUT,
                "grade": "UNREVIEWED_CANDIDATE_EVIDENCE",
            }, created_at="2026-11-01T18:00:01+00:00"),
            lr._event("QUARANTINE", {
                "manifest": str((lr.QUARANTINE / "MANIFEST.json").relative_to(ROOT)),
                "excluded_history_ids": [x["history_id"] for x in EXCLUDED],
                "excluded_history": EXCLUDED,
                "retained_candidate_evidence": ["O-SCIENCE candidate import"],
                "policy": "Fixture-origin and self-review events are preserved, not replayed, not relabeled as acceptance.",
            }, created_at="2026-11-01T18:00:02+00:00"),
            lr._event("RETURN_INTAKE", {
                "id": "PROGRAMMA_SOROK_W1_A_VISION_ASTRA_R1",
                "branch": "research/programma-sorok-w1-a-vision-astra-20261101-r1",
                "sha": "e7787d7f22dfcc9dd1ad786d953755b4f4d410c7",
                "source": {
                    "commit": "e7787d7f22dfcc9dd1ad786d953755b4f4d410c7",
                    "path": "WORKER_RETURNS/PROGRAMMA_SOROK_W1_A_VISION_ASTRA_R1/00_FINDINGS_AND_RECOMMENDATIONS.md",
                    "blob": "b457bebf63d4ae12d01b8481481368bcd082e269",
                    "object_type": "blob",
                },
                "tests": {"passed": 0, "native": False, "note": "Documentary return; no execution claimed."},
                "gap": {
                    "id": "GAP-W1-A-WHOLE-SCOPE",
                    "parent_obligation": "Whole-estate source coverage required by the W1-A return",
                    "domain": "SOURCE_BREADTH",
                    "node": "W1_A_RETURN",
                    "status": "UNREVIEWED_CANDIDATE_EVIDENCE",
                    "missing_stages": ["T", "A", "E", "C", "V"],
                    "existing_evidence": ["W1-A return at e7787d7f"],
                    "locator": {
                        "path": "WORKER_RETURNS/PROGRAMMA_SOROK_W1_A_VISION_ASTRA_R1/00_FINDINGS_AND_RECOMMENDATIONS.md",
                        "quote": "No single technical milestone or personality description can certify it.",
                    },
                    "alternatives": ["treat selected reads as complete", "continue breadth ingest with visible limits"],
                    "dependencies": ["SOROK_HQ intake"],
                    "affected_consumer": "SOROK_HQ operator",
                    "owner": "W1_A_RESEARCHER / SOROK_HQ",
                    "smallest_useful_next_action": "Review the exact return scope and connect its unsupported estate families to explicit missing or unread nodes.",
                    "falsifier": "The return is treated as whole-estate proof or owner adoption.",
                    "blocked_by": [],
                    "independently_actionable": True,
                },
                "node_updates": [{
                    "id": "W1_A_RETURN",
                    "evidence": {"return_sha": "e7787d7f22dfcc9dd1ad786d953755b4f4d410c7", "grade": "CANDIDATE_NOT_PROMOTED"},
                    "locator": {
                        "path": "WORKER_RETURNS/PROGRAMMA_SOROK_W1_A_VISION_ASTRA_R1/00_FINDINGS_AND_RECOMMENDATIONS.md",
                        "quote": "No single technical milestone or personality description can certify it.",
                    },
                }],
            }, created_at="2026-11-01T18:00:03+00:00", source={
                "commit": "e7787d7f22dfcc9dd1ad786d953755b4f4d410c7",
                "path": "WORKER_RETURNS/PROGRAMMA_SOROK_W1_A_VISION_ASTRA_R1/00_FINDINGS_AND_RECOMMENDATIONS.md",
                "blob": "b457bebf63d4ae12d01b8481481368bcd082e269",
                "object_type": "blob",
            }),
        ]
        for body in events:
            evidence_store.append_event(journal, body)
    state = lr.rebuild_from_journal(journal, operating=True)
    lr._save(state, lr.STATE, revision=int(state.get("revision") or 0))
    return {
        "status": "INITIALIZED",
        "journal": str(journal.relative_to(ROOT)),
        "events": len(evidence_store.read_journal(journal)),
        "journal_head": state.get("journal_head"),
        "state_digest": state.get("state_digest"),
        "nodes": len(state["nodes"]),
        "edges": len(state["edges"]),
        "gaps": state.get("whole_program_gaps", {}).get("count", 0),
        "quarantine_manifest": str((lr.QUARANTINE / "MANIFEST.json").relative_to(ROOT)),
        "excluded_history_ids": [x["history_id"] for x in EXCLUDED],
        "preserved_sha256": manifest["preserved_files"],
    }


if __name__ == "__main__":
    print(json.dumps(initialize(), indent=2, sort_keys=True))
