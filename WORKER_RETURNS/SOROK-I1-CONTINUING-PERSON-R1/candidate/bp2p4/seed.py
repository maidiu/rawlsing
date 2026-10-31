"""BP4-compatible seed built only from verified BP2 joined artifacts.

The seed is the bridge between the two source-free domains. It is not a picture
of the BP2 receipt: every field is derived from a re-verified physical artifact
(keyed C8 journal, sealed C9 target row, CAN008 response row, separate CAN011
authorization row, target commit receipt and performed E2 admission).

Three things are deliberately explicit:

* the **practice materialization** - the committed BP2 ``V3MS_PRACTICE`` target
  plus its independently performed E2 act become real actor state
  (``projects``/``tools_remaining``) and a real world resource (the workshop tool
  the E2 act inspected). Without the performed E2 there is no practice and the
  later offscreen world outcome changes.
* the **clock bridge** - BP2's logical clock and BP4's world clock are separate
  domains. They are never compared numerically; the only declared relation is
  the same-process emission order, and a missing declaration is a typed
  ``TIME_COORDINATE_HOLD``.
* the **envelope** - the real BP2 -> BP4 envelope, re-derived from the artifacts
  before it is accepted.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402
from bp4.world import WorldState, initial_world  # noqa: E402

from .envelope import build_envelope, verify_producer_envelope  # noqa: E402
from .reunion import (  # noqa: E402
    BP2Artifacts,
    EXPECTED_DERIVED,
    ReunionRefusal,
    verify_artifacts,
    _verify_e2,
)

GRADE = "TEST_ONLY_SOURCEFREE_BP2P4J_SEED_NOT_NATIVE"
JOIN_SCHEMA = "BP2P4J_JOINED_SEED@1"
CLOCK_HOLD = "TIME_COORDINATE_HOLD"


class SeedRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class PracticeBinding:
    established: bool
    label: str
    target_ref: str
    performed_act: str
    e2_receipt_hash: str
    effective_from: int

    def as_dict(self) -> dict:
        return {
            "established": self.established,
            "practice_label": self.label,
            "source_target_ref": self.target_ref,
            "performed_act": self.performed_act,
            "e2_receipt_hash": self.e2_receipt_hash,
            "effective_from": self.effective_from,
            "native": False,
            "grade": "TEST_ONLY_SOURCEFREE_TECHNICAL",
        }


@dataclass(frozen=True)
class ClockBridge:
    bp2_domain: str
    bp4_domain: str
    bp2_event_time: int
    bp2_target_commit_time: int
    bp2_e2_action_time: int
    bp4_world_origin_clock: int
    process_order: tuple[str, ...]
    relation: str = "DECLARED_PROCESS_ORDER_NOT_NUMERIC_COMPARISON"
    numeric_ordering_used: bool = False

    def as_dict(self) -> dict:
        return {
            "relation": self.relation,
            "bp2_domain": self.bp2_domain,
            "bp4_domain": self.bp4_domain,
            "bp2_event_time": self.bp2_event_time,
            "bp2_target_commit_time": self.bp2_target_commit_time,
            "bp2_e2_action_time": self.bp2_e2_action_time,
            "bp4_world_origin_clock": self.bp4_world_origin_clock,
            "numeric_ordering_used": self.numeric_ordering_used,
            "process_order": list(self.process_order),
            "basis": (
                "The BP4 world root is created in the same process only after the "
                "BP2 C8 keyed commit, the C9 target commit and the independent E2 "
                "admission have been physically verified. The two logical clock "
                "domains are never compared numerically; no BP2 time is treated "
                "as a BP4 world time or vice versa."),
            "hold_code": "",
        }


def build_clock_bridge(artifacts: BP2Artifacts, *,
                       bp4_world_origin_clock: int = 10,
                       process_order: tuple[str, ...] | None = None) -> ClockBridge:
    e2 = artifacts.e2_receipt or {}
    return ClockBridge(
        bp2_domain="BP2_TEST_ONLY_LOGICAL_CLOCK",
        bp4_domain="BP4_TEST_ONLY_WORLD_CLOCK",
        bp2_event_time=artifacts.event_time,
        bp2_target_commit_time=int(e2.get("target_commit_time", artifacts.event_time)),
        bp2_e2_action_time=int(e2.get("action_time", artifacts.later_as_of)),
        bp4_world_origin_clock=int(bp4_world_origin_clock),
        process_order=process_order or (
            "BP2_C8_COMMIT", "BP2_C9_TARGET_COMMIT", "BP2_E2_ADMISSION",
            "BP4_SEED_BIND", "BP4_WORLD_ROOT_CREATE"),
    )


@dataclass
class JoinedSeed:
    """Duck-typed BP4 ``Seed`` plus the joined-source custody."""

    root: Path
    life: Any
    world: WorldState
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
    # joined custody
    artifacts: BP2Artifacts
    practice: PracticeBinding
    clock: ClockBridge
    envelope: dict
    envelope_validation: dict
    target: dict
    response: dict
    target_journal: dict
    commit_receipt: dict
    c8_ingress: dict
    join_receipt: dict = field(default_factory=dict)

    def public(self) -> dict:
        return {
            "schema": "BP4_SOURCEFREE_SEED@1",
            "actor_a": self.life.a_source.actor_id,
            "actor_b": self.life.b_source.actor_id,
            "source_refs": [self.life.a_source.source_ref, self.life.b_source.source_ref],
            "source_hashes": [self.life.a_source.source_hash,
                              self.life.b_source.source_hash],
            "snapshot_hashes": [self.life.a_snapshot["hash"],
                                self.life.b_snapshot["hash"]],
            "state_hashes": [self.life.a_snapshot["state_hash"],
                             self.life.b_snapshot["state_hash"]],
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
            "grade": GRADE,
            # joined extras
            "joined_mode": self.artifacts.mode,
            "practice": self.practice.as_dict(),
            "clock_bridge": self.clock.as_dict(),
            "envelope_hash": self.envelope.get("source_preimages", {}) and digest(
                self.envelope),
        }

    def custody(self) -> dict:
        return {
            "schema": JOIN_SCHEMA,
            "grade": GRADE,
            "native": False,
            "mode": self.artifacts.mode,
            "target_id": self.c9_target_id,
            "target_record_hash": self.artifacts.target_record_hash,
            "consumed_state_hash": self.c9_state_hash,
            "c8_occurrence_id": self.c8_occurrence_ids[0],
            "c8_state_digest": self.c8_state_digest,
            "c8_writer_version": self.c8_writer_version,
            "c8_commit_receipt_id": self.artifacts.c8_commit_receipt_id,
            "e1_event_id": self.artifacts.e1_event_id,
            "e1_event_hash": self.artifacts.e1_event_hash,
            "rule_a_content_hash": self.artifacts.rule_a_hash,
            "rule_t_content_hash": self.artifacts.rule_t_hash,
            "rule_t_dependency_hash": self.artifacts.rule_t_dependency,
            "response_hash": self.artifacts.response_hash,
            "grant_hash": self.artifacts.grant_hash,
            "e2_receipt_hash": self.artifacts.e2_receipt_hash,
            "e2_admitted": self.c9_e2_admitted,
            "c9_commit_receipt_hash": self.artifacts.receipt.get(
                "persisted", {}).get("c9_commit_receipt_hash", ""),
            "c9_authorization_hash": self.artifacts.receipt.get(
                "persisted", {}).get("c9_authorization_hash", ""),
            "practice": self.practice.as_dict(),
            "clock": self.clock.as_dict(),
            "envelope_validation": self.envelope_validation,
            "response_row_present": bool(self.response),
            "target_journal_present": bool(self.target_journal),
            "commit_receipt_present": bool(self.commit_receipt),
            "adp019_admission_receipt": "ADP019_ADMISSION_RECEIPT_ABSENT",
            "native_grants": {"actor": False, "rule": False, "c8_trust": False,
                              "e2": False, "world": False, "c11": False,
                              "c12": False, "adp019": False},
        }


def _materialize_practice(world: WorldState, artifacts: BP2Artifacts,
                          e2_admission: dict | None,
                          *, materialize: bool = True) -> PracticeBinding:
    # BP4's objective world keys actors by its own slot ids "A"/"B"; the BP2
    # joined actor A is that slot. The full BP1 actor id is recorded inside the
    # practice record for traceability.
    actor = "A"
    actor_id = artifacts.life.a_source.actor_id
    state = dict(world.actor_state.get(actor, {}))
    if e2_admission is None or not materialize:
        state["projects"] = []
        state["tools_remaining"] = 0
        world.actor_state[actor] = state
        world.resources["workshop"] = dict(world.resources.get("workshop", {}))
        world.resources["workshop"]["tool_available"] = False
        return PracticeBinding(
            established=False,
            label="",
            target_ref=artifacts.target_record_hash,
            performed_act="",
            e2_receipt_hash="",
            effective_from=artifacts.event_time,
        )
    label = str(artifacts.target["record_preimage"]["governed_payload"]["practice_label"])
    if label != EXPECTED_DERIVED["practice_label"]:
        raise SeedRefusal("BP2_PRACTICE_LABEL_UNEXPECTED", label)
    if e2_admission["act"] != EXPECTED_DERIVED["e2_act"]:
        raise SeedRefusal("BP2_E2_ACT_UNEXPECTED", e2_admission["act"])
    if e2_admission["consumed_state_hash"] != digest(dict(artifacts.target)):
        raise SeedRefusal("BP2_E2_CONSUMED_STATE_MISMATCH")
    practice = {
        "practice_label": label,
        "actor_id": actor_id,
        "source_target_ref": artifacts.target_record_hash,
        "performed_act": e2_admission["act"],
        "effective_from": artifacts.event_time,
        "e2_receipt_hash": artifacts.e2_receipt_hash,
        "native": False,
        "grade": "TEST_ONLY_SOURCEFREE_TECHNICAL",
    }
    state["projects"] = [practice]
    state["tools_remaining"] = 1
    world.actor_state[actor] = state
    world.resources["workshop"] = dict(world.resources.get("workshop", {}))
    world.resources["workshop"]["tool_available"] = True
    return PracticeBinding(
        established=True,
        label=label,
        target_ref=artifacts.target_record_hash,
        performed_act=e2_admission["act"],
        e2_receipt_hash=artifacts.e2_receipt_hash,
        effective_from=artifacts.event_time,
    )


def build_seed(artifacts: BP2Artifacts, *, e2: Any = "default",
               world: WorldState | None = None,
               clock_bridge: ClockBridge | None = None,
               materialize: bool = True) -> JoinedSeed:
    """Build the BP4-compatible seed from re-verified BP2 artifacts."""
    verified = verify_artifacts(artifacts)
    if e2 == "default":
        e2_receipt = verified.e2_receipt
    else:
        e2_receipt = e2
    e2_admission = None
    if e2_receipt is not None:
        e2_admission = _verify_e2(
            e2_receipt,
            expected={"actor_id": verified.life.a_source.actor_id,
                      "e2_act": EXPECTED_DERIVED["e2_act"]},
            target=verified.target,
        )
    world = initial_world(verified.life) if world is None else world
    practice = _materialize_practice(world, verified, e2_admission,
                                     materialize=materialize)
    bridge = clock_bridge or build_clock_bridge(verified)
    world_hash = world.snapshot()["hash"]
    envelope = build_envelope(verified, world_hash=world_hash,
                              clock_bridge=bridge.as_dict())
    validation = verify_producer_envelope(envelope, verified,
                                          world_hash=world_hash,
                                          clock_bridge=bridge.as_dict())
    ingress = {
        "state_digest": verified.c8_state_digest,
        "occurrence_ids": [verified.occurrence_id],
        "writer_version": verified.c8_writer_version,
        "commit_receipt_id": verified.c8_commit_receipt_id,
    }
    seed = JoinedSeed(
        root=verified.root,
        life=verified.life,
        world=world,
        c9_path=verified.c9_path,
        c9_target_id=verified.target_id,
        c9_state_hash=verified.consumed_state_hash,
        c9_commit_time=verified.event_time,
        c9_e2_admitted=bool(e2_admission and e2_admission["admitted"]),
        c8_journal=verified.journal_path,
        c8_key_path=verified.key_path,
        c8_anchor_log=verified.anchor_log,
        c8_anchor_watermark=verified.anchor_watermark,
        c8_key_id=verified.key_id,
        c8_occurrence_ids=[verified.occurrence_id],
        c8_state_digest=verified.c8_state_digest,
        c8_writer_version=verified.c8_writer_version,
        artifacts=verified,
        practice=practice,
        clock=bridge,
        envelope=envelope,
        envelope_validation=validation,
        target=verified.target,
        response={},
        target_journal={},
        commit_receipt={},
        c8_ingress=ingress,
    )
    seed.response = _response_row(verified)
    seed.target_journal = _journal_row(verified)
    seed.commit_receipt = _commit_row(verified)
    seed.join_receipt = seed.custody()
    return seed


def _response_row(artifacts: BP2Artifacts) -> dict:
    import json

    from candidate import CandidateStore

    with CandidateStore(artifacts.c9_path) as store:
        wanted = artifacts.target.get("response_hash")
        for (body,) in store.db.execute("SELECT body FROM response"):
            record = json.loads(body)
            if record.get("receipt_hash") == wanted:
                return record
    return {}


def _journal_row(artifacts: BP2Artifacts) -> dict:
    import json

    from candidate import CandidateStore

    with CandidateStore(artifacts.c9_path) as store:
        row = store.db.execute("SELECT body FROM target_journal WHERE id=?",
                               (artifacts.target_record_hash,)).fetchone()
    return json.loads(row[0]) if row else {}


def _commit_row(artifacts: BP2Artifacts) -> dict:
    import json

    from candidate import CandidateStore

    with CandidateStore(artifacts.c9_path) as store:
        for (body,) in store.db.execute("SELECT body FROM receipt"):
            record = json.loads(body)
            if record.get("target_id") == artifacts.target_id:
                return record
    return {}


__all__ = [
    "CLOCK_HOLD",
    "ClockBridge",
    "GRADE",
    "JOIN_SCHEMA",
    "JoinedSeed",
    "PracticeBinding",
    "SeedRefusal",
    "build_clock_bridge",
    "build_seed",
]
