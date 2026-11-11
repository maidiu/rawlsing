"""C10 coupled actor/world receiver over actual pinned sourcefree carriers.

The receiver re-verifies every source edge at read time:
  - BP1 actor-owned historical snapshots (exact hash/source grade)
  - BP3 keyed C8 journal proof + external anchor + C9 event ingress
  - C9R durable target record and later E2 admission
  - source-owned objective world events and owner receipts

Objective world truth and actor-visible V2 claims stay separate. This is a
TEST_ONLY C10 technical receiver, not native C10/C11.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bp1.ledger import verify_snapshot

from candidate import CandidateStore
import c8_exclusive_writer as bp3
import c9_event_ingress as bp3_ingress

from .canon import digest, valid
from .perception import render_perceived_claims
from .world import WorldState, validate_owner_receipt

C10_SCHEMA = "BP4_C10_COUPLED_RECEIVER@1"
GRADE = "TEST_ONLY_SOURCEFREE_C10_NOT_NATIVE"


class C10Refusal(Exception):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


@dataclass
class C10State:
    branch_id: str
    actor_id: str
    clock: int
    actor_snapshots: dict
    c9_target: dict
    c9_e2_admitted: bool
    c8_ingress: dict
    world: dict
    runtime_state: dict
    actor_v2: dict
    receipt: dict


def _read_c9(seed, path: Path | None = None) -> dict:
    path = seed.c9_path if path is None else Path(path)
    with CandidateStore(path) as store:
        target = store.read_target_state(seed.c9_target_id)
    if target is None:
        raise C10Refusal("C9_TARGET_MISSING", seed.c9_target_id)
    preimage = target.get("record_preimage")
    if not isinstance(preimage, dict) or not valid(preimage):
        raise C10Refusal("C9_TARGET_PREIMAGE_UNSEALED")
    if preimage.get("hash") != target.get("record_hash"):
        raise C10Refusal("C9_TARGET_PREIMAGE_HASH_MISMATCH")
    if digest({k: v for k, v in preimage.items() if k != "hash"}) != target.get("record_hash"):
        raise C10Refusal("C9_TARGET_PREIMAGE_DIGEST_MISMATCH")
    if digest(dict(target)) != seed.c9_state_hash:
        raise C10Refusal("C9_TARGET_STATE_MISMATCH")
    return dict(target)


def _read_c8(seed, proof_verifier=None) -> dict:
    store = bp3.WriterKeyStore.load(seed.c8_key_path, seed.c8_key_id)
    anchor = bp3.KeyedMonotonicAnchor(
        log_path=seed.c8_anchor_log,
        watermark_path=seed.c8_anchor_watermark,
        store=store,
    )
    journal = bp3.ExclusiveJournal(seed.c8_journal, store=store, anchor=anchor)
    verifier = proof_verifier or journal.verify_journal
    try:
        verifier()
    except Exception as exc:  # noqa: BLE001 - typed source failure
        raise C10Refusal("BP3_PROOF_INVALID", type(exc).__name__ + ":" + str(exc))
    try:
        ingress = bp3_ingress.receive_event(seed.c8_journal, proof_verifier=verifier)
    except Exception as exc:  # noqa: BLE001
        raise C10Refusal("BP3_INGRESS_REFUSED", type(exc).__name__ + ":" + str(exc))
    if ingress["state_digest"] != seed.c8_state_digest:
        raise C10Refusal("BP3_STATE_DIGEST_MISMATCH")
    return ingress


def _verify_world(state: dict) -> WorldState:
    world = WorldState.restore(state["world"])
    for event in world.events:
        body = {k: v for k, v in event.items() if k != "hash"}
        if digest(body) != event.get("hash"):
            raise C10Refusal("WORLD_EVENT_INTEGRITY_FAILURE", event.get("event_id", ""))
        if event["kind"] in {"REPAIR", "OFFSCREEN_REPAIR", "OFFSCREEN_NO_CHANGE"}:
            if event.get("owner_receipt") is None:
                raise C10Refusal("WORLD_ACTION_OWNER_RECEIPT_MISSING", event["event_id"])
            try:
                validate_owner_receipt(
                    event["owner_receipt"], actor_id=event["actor_id"],
                    act=event["kind"], clock=event["clock"],
                )
            except Exception as exc:  # noqa: BLE001
                raise C10Refusal("WORLD_OWNER_RECEIPT_INVALID", type(exc).__name__)
    return world


def receive(seed, store, branch_id: str, *, actor_id: str = "A",
            expected_a_hash: str | None = None,
            expected_b_hash: str | None = None,
            proof_verifier=None,
            c9_path: Path | None = None) -> C10State:
    store.branch(branch_id)
    state = store.latest_state(branch_id)
    expected_a = expected_a_hash or seed.life.a_snapshot["hash"]
    expected_b = expected_b_hash or seed.life.b_snapshot["hash"]
    ok_a, reason_a = verify_snapshot(seed.life.a_snapshot, expected_hash=expected_a)
    if not ok_a:
        raise C10Refusal("BP1_ACTOR_SOURCE_NOT_AUTHENTICATED", "A:" + str(reason_a))
    ok_b, reason_b = verify_snapshot(seed.life.b_snapshot, expected_hash=expected_b)
    if not ok_b:
        raise C10Refusal("BP1_ACTOR_SOURCE_NOT_AUTHENTICATED", "B:" + str(reason_b))
    c9_target = _read_c9(seed, c9_path)
    c8_ingress = _read_c8(seed, proof_verifier=proof_verifier)
    world = _verify_world(state)
    runtime_state = dict(state)
    runtime_state["episodes"] = store.episodes(branch_id)
    runtime_state["perceptions"] = {
        actor: store.perceptions(branch_id, actor)
        for actor in store.branch(branch_id)["actor_ids"]
    }
    runtime_state["knowledge"] = {
        actor: [p["event_id"] for p in runtime_state["perceptions"][actor]]
        for actor in runtime_state["perceptions"]
    }
    actor_v2 = render_perceived_claims(actor_id, world.clock, runtime_state, world.events)
    receipt = {
        "schema": C10_SCHEMA,
        "branch_id": branch_id,
        "actor_id": actor_id,
        "grade": GRADE,
        "native": False,
        "objective_world_clock": world.clock,
        "actor_as_of": int(seed.life.a_snapshot["last_clock"] if actor_id == seed.life.a_source.actor_id
                           else seed.life.b_snapshot["last_clock"]),
        "c9_target_id": seed.c9_target_id,
        "c9_target_commit_time": seed.c9_commit_time,
        "c9_e2_admitted": seed.c9_e2_admitted,
        "c8_writer_version": c8_ingress["writer_version"],
        "c8_state_digest": c8_ingress["state_digest"],
        "c8_occurrence_count": c8_ingress["occurrence_count"],
        "actor_source_grade": seed.life.a_source.source_grade,
        "world_grade": world.grade,
        "v2_claim_count": len(actor_v2.get("claims", [])),
    }
    receipt["receipt_hash"] = digest(receipt)
    return C10State(
        branch_id=branch_id,
        actor_id=actor_id,
        clock=world.clock,
        actor_snapshots={"A": seed.life.a_snapshot, "B": seed.life.b_snapshot},
        c9_target=c9_target,
        c9_e2_admitted=seed.c9_e2_admitted,
        c8_ingress=c8_ingress,
        world=world.snapshot(),
        runtime_state=runtime_state,
        actor_v2=actor_v2,
        receipt=receipt,
    )
