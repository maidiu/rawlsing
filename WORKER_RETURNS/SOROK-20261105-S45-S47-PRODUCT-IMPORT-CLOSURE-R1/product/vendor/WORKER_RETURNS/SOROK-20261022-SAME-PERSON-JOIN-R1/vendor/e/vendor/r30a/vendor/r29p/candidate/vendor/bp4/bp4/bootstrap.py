"""Sourcefree seed construction: BP1 two-actor life, C9R target/E2, BP3 C8.

All inputs are explicitly TEST_ONLY. The C8 occurrence is written through the
BP3 keyed exclusive journal and verified with its external anchor; the C9 target
and later E2 are produced by the pinned C9R sourcefree candidate over BP1's
historical actor snapshot.
"""
from __future__ import annotations

import base64
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from bp1.c9_bridge import run_bp1_c9
from bp1.composer import build_two_actor_life

from .canon import digest
from .world import initial_world

from candidate import CandidateStore  # noqa: E402  (vendor/c9r on sys.path)
import c8_exclusive_writer as bp3  # noqa: E402  (vendor/bp3 on sys.path)
import c9_event_ingress as bp3_ingress  # noqa: E402


@dataclass
class Seed:
    root: Path
    life: object
    world: object
    c9_path: Path
    c9_target_id: str
    c9_state_hash: str
    c9_commit_time: int
    c9_e2_admitted: bool
    c8_journal: Path
    c8_key_path: Path
    c8_anchor_log: Path
    c8_anchor_watermark: Path
    c8_key_id: str
    c8_occurrence_ids: list
    c8_state_digest: str
    c8_writer_version: int

    def public(self) -> dict:
        return {
            "schema": "BP4_SOURCEFREE_SEED@1",
            "actor_a": self.life.a_source.actor_id,
            "actor_b": self.life.b_source.actor_id,
            "source_refs": [self.life.a_source.source_ref, self.life.b_source.source_ref],
            "source_hashes": [self.life.a_source.source_hash, self.life.b_source.source_hash],
            "snapshot_hashes": [self.life.a_snapshot["hash"], self.life.b_snapshot["hash"]],
            "state_hashes": [self.life.a_snapshot["state_hash"], self.life.b_snapshot["state_hash"]],
            "c9_target_id": self.c9_target_id,
            "c9_state_hash": self.c9_state_hash,
            "c9_commit_time": self.c9_commit_time,
            "c9_e2_admitted": self.c9_e2_admitted,
            "c8_occurrence_ids": list(self.c8_occurrence_ids),
            "c8_state_digest": self.c8_state_digest,
            "c8_writer_version": self.c8_writer_version,
            "native_actor": False,
            "native_rule": False,
            "native_c8": False,
            "grade": "TEST_ONLY_SOURCEFREE_BP4_SEED_NOT_NATIVE",
        }


def _write_key(path: Path, key_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    key = os.urandom(32)
    path.write_text(json.dumps({"key_id": key_id,
                                "key_b64": base64.b64encode(key).decode()}), encoding="utf8")
    os.chmod(path, 0o600)


def build_c8(root: Path, life, c9_state_hash: str):
    journal_dir = root / "c8"
    journal_dir.mkdir(parents=True, exist_ok=True)
    key_path = root / "keys" / "bp4_writer_key.json"
    key_id = "TEST_ONLY_BP4_WRITER_KEY"
    _write_key(key_path, key_id)
    store = bp3.WriterKeyStore.load(key_path, key_id)
    anchor = bp3.KeyedMonotonicAnchor(
        log_path=root / "anchor" / "log.json",
        watermark_path=root / "anchor" / "watermark.json",
        store=store,
    )
    journal = bp3.ExclusiveJournal(journal_dir / "journal.json", store=store, anchor=anchor)
    capability = bp3.KeyedCapability.issue(store, journal.journal_id, "TEST_ONLY_BP4_WRITER")
    candidate = {
        "candidate_id": "TEST_ONLY_BP4_C8_OCC_1",
        "payload": {
            "fact": "verified_sourcefree_occurrence",
            "joint_task": "coordinated_material_inspection",
            "c9_state_hash": c9_state_hash,
            "grade": "TEST_ONLY_SOURCEFREE_C8",
        },
    }
    event, refusal, receipt = journal.append_occurrence(candidate, capability=capability)
    if event is None or receipt is None:
        raise RuntimeError(f"BP4_C8_APPEND_REFUSED:{refusal}")
    proof = journal.verify_journal()
    ingress = bp3_ingress.receive_event(journal.path, proof_verifier=journal.verify_journal)
    return {
        "journal": journal.path,
        "key_path": key_path,
        "key_id": key_id,
        "anchor_log": anchor.log_path,
        "anchor_watermark": anchor.watermark_path,
        "occurrence_ids": ingress["occurrence_ids"],
        "state_digest": ingress["state_digest"],
        "writer_version": ingress["writer_version"],
        "proof": proof,
        "ingress": ingress,
    }


def build_seed(root: str | Path) -> Seed:
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    for name in ("c9.sqlite", "seed.json"):
        path = root / name
        if path.exists():
            path.unlink()
    for name in ("c8", "keys", "anchor"):
        path = root / name
        if path.exists():
            import shutil
            shutil.rmtree(path)
    life = build_two_actor_life()
    world = initial_world(life)
    c9_path = root / "c9.sqlite"
    with CandidateStore(c9_path) as store:
        c9 = run_bp1_c9(life, store, actor="A")
    if not c9.committed or not c9.e2 or not getattr(c9.e2, "admitted", False):
        raise RuntimeError("BP4_C9_POSITIVE_NOT_ESTABLISHED")
    c8 = build_c8(root, life, c9.state_hash)
    seed = Seed(
        root=root,
        life=life,
        world=world,
        c9_path=c9_path,
        c9_target_id=c9.target_id,
        c9_state_hash=c9.state_hash,
        c9_commit_time=c9.commit_time,
        c9_e2_admitted=True,
        c8_journal=c8["journal"],
        c8_key_path=c8["key_path"],
        c8_anchor_log=c8["anchor_log"],
        c8_anchor_watermark=c8["anchor_watermark"],
        c8_key_id=c8["key_id"],
        c8_occurrence_ids=c8["occurrence_ids"],
        c8_state_digest=c8["state_digest"],
        c8_writer_version=c8["writer_version"],
    )
    (root / "seed.json").write_text(json.dumps(seed.public(), indent=2, sort_keys=True) + "\n",
                                    encoding="utf8")
    return seed
