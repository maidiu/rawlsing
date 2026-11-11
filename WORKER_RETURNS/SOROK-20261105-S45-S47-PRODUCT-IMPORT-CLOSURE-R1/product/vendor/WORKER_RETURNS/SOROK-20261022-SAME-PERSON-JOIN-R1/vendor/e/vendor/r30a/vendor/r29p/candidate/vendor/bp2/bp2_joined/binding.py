"""BP1 actor/world occurrence -> BP3 committed C8 occurrence -> OUT9 read binding.

The BP1 two-actor life is the actor/history source. Its shared objective, two
independently performed G18 actions and both sealed actor snapshots are bound
into ONE C8 occurrence candidate, committed through BP3's keyed exclusive
writer, and read back through the accepted OUT9 read-only consumer.

Nothing here re-implements BP1, BP3, C8O or OUT9. The candidate payload is a
declared TEST_ONLY source-free occurrence; the C8 admission grade it receives is
``SOURCEFREE_LEGACY_FIXTURE_NO_OWNER_AUTHORITY``, which is exactly not an ADP019
admission. A payload key that could pose as an executable owner directive, a
future-child field or a psychological claim is refused before any commit.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402
from bp1.composer import future_child_findings  # noqa: E402
from bp1.source import (  # noqa: E402
    BP1_ACTOR_SOURCE_GRADE,
    BP1_NATIVE_GRANT,
    PSYCHOLOGY_KEYS,
    TEST_ONLY_PREFIX,
)

WORLD_OCCURRENCE_SCHEMA = "BP2_WORLD_OCCURRENCE@1"
E1_CONTENT_SCHEMA = "BP2_E1_CONTENT@1"
OWNER_DIRECTIVE_KEYS = frozenset({
    "admit", "admitted", "admitted_event_id", "occurrence_id", "event_id",
    "event_cursor", "cursor_after", "cursor_before", "admitted_cursor",
    "state_delta", "final_state", "effect_result", "effect_state", "effect_delta",
    "memory_delta", "memory_update", "actor_memory_update", "world_owner",
    "material_effect", "physical_transition", "client_perceived",
    "human_perceived", "perception_receipt",
})
SCENE = "workshop"


class BindingRefusal(ValueError):
    """A source-free occurrence binding is not admissible."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class WorldOccurrence:
    """The deterministic source-free occurrence built from one BP1 life."""

    actor_key: str
    actor_id: str
    other_id: str
    event_time: int
    candidate: dict
    payload: dict
    causal_parent_event_ids: tuple[str, ...]
    actor_snapshot: dict
    other_snapshot: dict
    performed_act_ref: str
    other_act_ref: str
    objective_ref: str
    objective_hash: str
    material_ref: str
    material_receipt_id: str
    witness_ref: str
    actor_source_ref: str
    actor_source_hash: str
    other_source_ref: str
    other_source_hash: str
    actor_performed_receipt_id: str
    other_performed_receipt_id: str
    life: Any

    @property
    def candidate_id(self) -> str:
        return self.candidate["candidate_id"]

    def summary(self) -> dict:
        return {
            "schema": WORLD_OCCURRENCE_SCHEMA,
            "candidate_id": self.candidate_id,
            "payload_hash": digest(self.payload),
            "actor_id": self.actor_id,
            "other_actor_id": self.other_id,
            "actor_source_ref": self.actor_source_ref,
            "actor_source_hash": self.actor_source_hash,
            "other_source_ref": self.other_source_ref,
            "other_source_hash": self.other_source_hash,
            "actor_snapshot_hash": self.actor_snapshot["hash"],
            "other_snapshot_hash": self.other_snapshot["hash"],
            "actor_state_hash": self.actor_snapshot["state_hash"],
            "other_state_hash": self.other_snapshot["state_hash"],
            "bp1_objective_ref": self.objective_ref,
            "bp1_objective_hash": self.objective_hash,
            "material_ref": self.material_ref,
            "material_receipt_id": self.material_receipt_id,
            "performed_act_ref": self.performed_act_ref,
            "performed_act_receipt_id": self.actor_performed_receipt_id,
            "other_act_ref": self.other_act_ref,
            "other_act_receipt_id": self.other_performed_receipt_id,
            "witness_ref": self.witness_ref,
            "event_time": self.event_time,
            "causal_parent_event_ids": list(self.causal_parent_event_ids),
            "source_grade": BP1_ACTOR_SOURCE_GRADE,
            "native_grant": BP1_NATIVE_GRANT,
            "psychology_claim": False,
            "native_actor_claim": False,
            "adp019_status": "ADP019_ADMISSION_RECEIPT_ABSENT",
        }


def _forbidden_owner_directive(value: Any) -> str | None:
    """Recursively find a key that could pose as an executable owner directive."""
    if isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str):
                compact = "".join(ch for ch in key.lower() if ch.isalnum())
                if key.lower() in OWNER_DIRECTIVE_KEYS or compact in {
                    "".join(c for c in k.lower() if c.isalnum())
                    for k in OWNER_DIRECTIVE_KEYS
                }:
                    return key
                if compact.startswith("objective"):
                    return key
            found = _forbidden_owner_directive(item)
            if found:
                return found
    elif isinstance(value, (list, tuple)):
        for item in value:
            found = _forbidden_owner_directive(item)
            if found:
                return found
    return None


def _forbidden_psychology(value: Any) -> str | None:
    """Recursively find a psychological-claim key in the occurrence payload."""
    if isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str) and key.lower() in PSYCHOLOGY_KEYS:
                return key
            found = _forbidden_psychology(item)
            if found:
                return found
    elif isinstance(value, (list, tuple)):
        for item in value:
            found = _forbidden_psychology(item)
            if found:
                return found
    return None


def validate_occurrence_payload(payload: Mapping[str, Any]) -> None:
    """Refuse a payload carrying future-child, psychology or owner directives."""
    if not isinstance(payload, Mapping) or not payload:
        raise BindingRefusal("OCCURRENCE_PAYLOAD_MISSING")
    findings = future_child_findings(dict(payload))
    if findings:
        raise BindingRefusal("FUTURE_CHILD_INFORMATION_LEAK")
    psychology = _forbidden_psychology(dict(payload))
    if psychology:
        raise BindingRefusal("PSYCHOLOGY_CLAIM_IN_OCCURRENCE", psychology)
    directive = _forbidden_owner_directive(dict(payload))
    if directive:
        raise BindingRefusal("UNLICENSED_OWNER_DIRECTIVE_IN_OCCURRENCE", directive)


def _actor_block(life, key: str) -> dict:
    snapshot = life.a_snapshot if key == "A" else life.b_snapshot
    source = life.a_source if key == "A" else life.b_source
    ledger = life.a_ledger if key == "A" else life.b_ledger
    performed = ledger.performed_action_events
    return {
        "actor_id": source.actor_id,
        "source_ref": source.source_ref,
        "source_hash": source.source_hash,
        "role": source.role,
        "seed": source.seed,
        "history_hash": snapshot["history_hash"],
        "snapshot_hash": snapshot["hash"],
        "state_hash": snapshot["state_hash"],
        "event_head": snapshot["event_head"],
        "clock": int(snapshot["last_clock"]),
        "performed_act_ref": performed[0].event_id if performed else "",
        "relation_view": [
            {
                "perceiver": event.payload.get("perceiver"),
                "target": event.payload.get("target"),
                "perceived_state": event.payload.get("perceived_state"),
                "causal_basis": event.payload.get("causal_basis"),
            }
            for event in ledger.events
            if event.kind == "RELATION_VIEW"
        ],
    }


def build_world_occurrence(life, *, actor: str = "A") -> WorldOccurrence:
    """Build the deterministic C8 occurrence candidate from one BP1 life."""
    if actor not in {"A", "B"}:
        raise BindingRefusal("ACTOR_NOT_IN_LIFE")
    actor_key = actor
    other_key = "B" if actor == "A" else "A"
    snapshot = life.a_snapshot if actor == "A" else life.b_snapshot
    other_snapshot = life.b_snapshot if actor == "A" else life.a_snapshot
    source = life.a_source if actor == "A" else life.b_source
    other_source = life.b_source if actor == "A" else life.a_source
    ledger = life.a_ledger if actor == "A" else life.b_ledger
    other_ledger = life.b_ledger if actor == "A" else life.a_ledger
    performed = ledger.performed_action_events
    other_performed = other_ledger.performed_action_events
    if not performed or not other_performed:
        raise BindingRefusal("PERFORMED_ACTION_MISSING")
    actor_receipt_id = digest(performed[0].payload["g18_action"]["source_receipt"])
    other_receipt_id = digest(other_performed[0].payload["g18_action"]["source_receipt"])
    prior = ledger.prior_history_event_id
    objective_event = ledger.objective_events[0]
    event_time = int(snapshot["last_clock"]) + 1
    causal_parents = (prior, objective_event.event_id)
    payload = {
        "schema": WORLD_OCCURRENCE_SCHEMA,
        "occurrence_kind": "BP1_TWO_ACTOR_SHARED_MATERIAL_TASK",
        "actor": _actor_block(life, actor_key),
        "other_actor": _actor_block(life, other_key),
        "world": {
            "bp1_objective_ref": life.objective["objective_event_id"],
            "bp1_objective_hash": life.objective["objective_hash"],
            "material_ref": life.material["event_id"],
            "material_receipt_id": digest(life.material["source_receipt"]),
            "witness_ref": life.witness["event_id"],
            "performed_act_ref": performed[0].event_id,
            "performed_act_receipt_id": actor_receipt_id,
            "other_act_ref": other_performed[0].event_id,
            "other_act_receipt_id": other_receipt_id,
            "scene": SCENE,
            "practice_label": "coordinated_material_inspection",
        },
        "causal_parent_event_ids": list(causal_parents),
        "clock": event_time,
        "source_grade": BP1_ACTOR_SOURCE_GRADE,
        "native_grant": BP1_NATIVE_GRANT,
        "adp010_stage": "AVAILABLE_ONLY",
        "adp019_status": "ADP019_ADMISSION_RECEIPT_ABSENT",
        "psychology_claim": False,
        "native_actor_claim": False,
    }
    validate_occurrence_payload(payload)
    candidate = {
        "candidate_id": "BP2-OCC-" + digest(payload)[:24].upper(),
        "payload": payload,
        "source_refs": [source.source_ref, other_source.source_ref],
        "causal_time": event_time,
    }
    return WorldOccurrence(
        actor_key=actor_key,
        actor_id=source.actor_id,
        other_id=other_source.actor_id,
        event_time=event_time,
        candidate=candidate,
        payload=payload,
        causal_parent_event_ids=causal_parents,
        actor_snapshot=snapshot,
        other_snapshot=other_snapshot,
        performed_act_ref=performed[0].event_id,
        other_act_ref=other_performed[0].event_id,
        objective_ref=life.objective["objective_event_id"],
        objective_hash=life.objective["objective_hash"],
        material_ref=life.material["event_id"],
        material_receipt_id=digest(life.material["source_receipt"]),
        witness_ref=life.witness["event_id"],
        actor_source_ref=source.source_ref,
        actor_source_hash=source.source_hash,
        other_source_ref=other_source.source_ref,
        other_source_hash=other_source.source_hash,
        actor_performed_receipt_id=digest(performed[0].payload["g18_action"]["source_receipt"])
        if performed[0].payload.get("g18_action") else "",
        other_performed_receipt_id=digest(
            other_performed[0].payload["g18_action"]["source_receipt"])
        if other_performed[0].payload.get("g18_action") else "",
        life=life,
    )


@dataclass
class C8Commit:
    """The actual committed C8 occurrence plus its keyed proof receipt."""

    occurrence_id: str
    event: dict
    receipt: Any
    journal_id: str
    state_digest: str
    version_state_digest: str
    ledger_prefix_digest: str
    commit_receipt_id: str
    writer_version: int
    anchor_seq: int
    proof: dict
    commit_receipt: dict
    candidate_id: str
    payload_hash: str

    def summary(self) -> dict:
        return {
            "occurrence_id": self.occurrence_id,
            "candidate_id": self.candidate_id,
            "journal_id": self.journal_id,
            "state_digest": self.state_digest,
            "version_state_digest": self.version_state_digest,
            "ledger_prefix_digest": self.ledger_prefix_digest,
            "commit_receipt_id": self.commit_receipt_id,
            "writer_version": self.writer_version,
            "anchor_seq": self.anchor_seq,
            "payload_hash": self.payload_hash,
            "admission_grade": self.event.get("admission_grade"),
            "source_refs": self.event.get("source_refs"),
            "causal_time": self.event.get("causal_time"),
            "psychology_claimed": False,
            "adp019_issued": False,
        }


def commit_world_occurrence(journal, capability, occurrence: WorldOccurrence) -> C8Commit:
    """Commit one occurrence through BP3's keyed exclusive writer."""
    import c8_exclusive_writer as writer

    try:
        event, refusal, receipt = journal.append_occurrence(
            occurrence.candidate, capability=capability)
    except writer.ExclusiveWriteRefused:
        raise
    if event is None or receipt is None:
        raise BindingRefusal("C8_OCCURRENCE_NOT_ADMITTED", str(refusal))
    journal.verify_journal()
    if event.get("content_hash") != digest(occurrence.payload):
        raise BindingRefusal("C8_CONTENT_HASH_DIVERGES_FROM_SOURCE")
    if event.get("candidate_id") != occurrence.candidate_id:
        raise BindingRefusal("C8_CANDIDATE_ID_DIVERGES_FROM_SOURCE")
    return C8Commit(
        occurrence_id=event["occurrence_id"],
        event=event,
        receipt=receipt,
        journal_id=receipt.journal_id,
        state_digest=receipt.c8o["state_digest"],
        version_state_digest=receipt.c8o["version_state_digest"],
        ledger_prefix_digest=receipt.c8o["ledger_prefix_digest"],
        commit_receipt_id=receipt.c8o["receipt_id"],
        writer_version=int(receipt.c8o["writer_version"]),
        anchor_seq=int(receipt.anchor_seq),
        proof=receipt.proof,
        commit_receipt=receipt.c8o,
        candidate_id=event["candidate_id"],
        payload_hash=digest(occurrence.payload),
    )


@dataclass
class Out9Binding:
    """The actual OUT9 read: readset plus the committed occurrence payload."""

    occurrence_id: str
    event: dict
    readset: dict
    ingress: dict
    grade: str
    verified_proof: bool
    canonical_bytes_sha256: str

    def summary(self) -> dict:
        return {
            "occurrence_id": self.occurrence_id,
            "occurrence_ids": list(self.readset["occurrence_ids"]),
            "state_digest": self.readset["state_digest"],
            "version_state_digest": self.readset["version_state_digest"],
            "ledger_prefix_digest": self.readset["ledger_prefix_digest"],
            "writer_version": self.readset["writer_version"],
            "writer_id": self.readset["writer_id"],
            "commit_receipt_id": self.readset["commit_receipt_id"],
            "canonical_bytes_sha256": self.canonical_bytes_sha256,
            "admission_grade": self.grade,
            "proof_verified": self.verified_proof,
            "adp019_admission_receipt": self.ingress.get("adp019_admission_receipt"),
            "e2_performed": self.ingress.get("e2_performed"),
            "native_actor_admitted": self.ingress.get("native_actor_admitted"),
            "route_probability": self.ingress.get("route_probability"),
            "selection_weight": self.ingress.get("selection_weight"),
        }


def read_out9(
    *,
    journal_path,
    expected_state_digest: str,
    expected_occurrence_id: str,
    proof_verifier=None,
) -> Out9Binding:
    """Read the committed occurrence through the accepted OUT9 consumer path."""
    from c8_readonly_consumer import C8ReadOnlyConsumer
    from c9_event_ingress import receive_event

    ingress = receive_event(
        journal_path,
        expected_state_digest=expected_state_digest,
        proof_verifier=proof_verifier,
    )
    consumer = C8ReadOnlyConsumer(journal_path)
    view = consumer.load()
    readset = view.readset.to_json()
    if readset["state_digest"] != expected_state_digest:
        raise BindingRefusal("OUT9_STATE_DIGEST_DIVERGES")
    if list(readset["occurrence_ids"]) != [expected_occurrence_id]:
        raise BindingRefusal("OUT9_OCCURRENCE_SET_DIVERGES")
    event = view.get(expected_occurrence_id)
    if event is None:
        raise BindingRefusal("OUT9_OCCURRENCE_ABSENT")
    consumer.assert_read_only_against(journal_path.read_bytes())
    return Out9Binding(
        occurrence_id=expected_occurrence_id,
        event=dict(event),
        readset=readset,
        ingress=ingress,
        grade=str(event.get("admission_grade")),
        verified_proof=proof_verifier is not None,
        canonical_bytes_sha256=readset["canonical_bytes_sha256"],
    )


def verify_out9_against_source(binding: Out9Binding, commit: C8Commit,
                               occurrence: WorldOccurrence) -> None:
    """Cross-check that OUT9 returned exactly the source occurrence."""
    event = binding.event
    if event.get("content_hash") != digest(occurrence.payload):
        raise BindingRefusal("OUT9_CONTENT_HASH_DIVERGES_FROM_SOURCE")
    identity = event.get("identity_preimage")
    if not isinstance(identity, Mapping):
        raise BindingRefusal("OUT9_IDENTITY_PREIMAGE_MISSING")
    if event.get("identity_digest") != digest(dict(identity)):
        raise BindingRefusal("OUT9_IDENTITY_DIGEST_INVALID")
    if dict(identity.get("payload", {})) != dict(occurrence.payload):
        raise BindingRefusal("OUT9_PAYLOAD_DIVERGES_FROM_SOURCE")
    if identity.get("candidate_id") != occurrence.candidate_id:
        raise BindingRefusal("OUT9_CANDIDATE_ID_DIVERGES_FROM_SOURCE")
    if binding.readset["state_digest"] != commit.state_digest:
        raise BindingRefusal("OUT9_STATE_DIGEST_DIVERGES_FROM_COMMIT")
    if binding.readset["commit_receipt_id"] != commit.commit_receipt_id:
        raise BindingRefusal("OUT9_RECEIPT_ID_DIVERGES_FROM_COMMIT")
    if binding.readset["writer_version"] != commit.writer_version:
        raise BindingRefusal("OUT9_WRITER_VERSION_DIVERGES_FROM_COMMIT")
    if binding.readset["ledger_prefix_digest"] != commit.ledger_prefix_digest:
        raise BindingRefusal("OUT9_LEDGER_PREFIX_DIVERGES_FROM_COMMIT")
    if binding.grade != "SOURCEFREE_LEGACY_FIXTURE_NO_OWNER_AUTHORITY":
        raise BindingRefusal("OUT9_ADMISSION_GRADE_UNEXPECTED", binding.grade)
    if binding.ingress.get("e2_performed") is not False:
        raise BindingRefusal("OUT9_CLAIMED_PERFORMED_E2")
    if binding.ingress.get("native_actor_admitted") is not False:
        raise BindingRefusal("OUT9_CLAIMED_NATIVE_ACTOR")


def e1_content(occurrence: WorldOccurrence, binding: Out9Binding,
               e1) -> dict:
    """Build the C9R event-witness content bound to the actual OUT9 read."""
    return {
        "schema": E1_CONTENT_SCHEMA,
        "fact": "joint_material_task",
        "scene": SCENE,
        "participants": [occurrence.actor_id, occurrence.other_id],
        "bp1_objective_ref": occurrence.objective_ref,
        "bp1_objective_hash": occurrence.objective_hash,
        "material_ref": occurrence.material_ref,
        "performed_act_ref": occurrence.performed_act_ref,
        "other_act_ref": occurrence.other_act_ref,
        "bp1_causal_parent_event_ids": list(occurrence.causal_parent_event_ids),
        "c8_occurrence_id": binding.occurrence_id,
        "c8_identity_digest": binding.event.get("identity_digest"),
        "c8_content_hash": binding.event.get("content_hash"),
        "c8_state_digest": binding.readset["state_digest"],
        "c8_ledger_prefix_digest": binding.readset["ledger_prefix_digest"],
        "c8_commit_receipt_id": binding.readset["commit_receipt_id"],
        "c8_writer_version": binding.readset["writer_version"],
        "source_grade": BP1_ACTOR_SOURCE_GRADE,
        "native_grant": BP1_NATIVE_GRANT,
        "adp019_admission_receipt": e1.adp019_admission_receipt,
        "native_actor_claim": False,
        "psychology_claim": False,
    }


__all__ = [
    "BindingRefusal",
    "C8Commit",
    "E1_CONTENT_SCHEMA",
    "Out9Binding",
    "SCENE",
    "WORLD_OCCURRENCE_SCHEMA",
    "WorldOccurrence",
    "build_world_occurrence",
    "commit_world_occurrence",
    "e1_content",
    "read_out9",
    "validate_occurrence_payload",
    "verify_out9_against_source",
]
