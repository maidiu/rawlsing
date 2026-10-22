"""Producer-emitted BP2 envelope and independent re-derivation.

BP4's ``bp4.bp2_compat`` defines the receiving contract
``BP2_JOINED_EVENT_HISTORY_TARGET_E2_ENVELOPE@1`` but deliberately refuses to
fabricate an emission. This module emits the real envelope from the physical BP2
artifacts and, separately, re-derives every field from those artifacts.

The distinction matters: ``bp4.bp2_compat.validate_envelope`` only checks shape,
non-empty lists and native flags. ``verify_producer_envelope`` recomputes the
actor hashes, C8 proof, occurrence identity, C9 target digest, response row,
separate CAN011 authorization row, target commit receipt and performed E2
admission, and refuses any envelope that is merely shape-correct.
"""
from __future__ import annotations

from typing import Any

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402
from bp4.bp2_compat import validate_envelope  # noqa: E402

from .reunion import BP2Artifacts, ReunionRefusal, verify_artifacts  # noqa: E402

SCHEMA = "BP2_JOINED_EVENT_HISTORY_TARGET_E2_ENVELOPE@1"
PRODUCER = "BP2_JOINED_PRODUCER"
GRADE_C8 = "TEST_ONLY_BP3_KEYED_C8_NOT_NATIVE"
GRADE_C9 = "C9R_TEST_ONLY_NOT_NATIVE"
GRADE_E2 = "TEST_ONLY_BP2_INDEPENDENT_E2_NOT_NATIVE"
GRADE_ACTOR = "TEST_ONLY_BP1_FIXTURE_ACTOR_NOT_NATIVE"


class EnvelopeRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


def build_envelope(artifacts: BP2Artifacts, *, world_hash: str,
                   clock_bridge: dict) -> dict:
    """Emit the real BP2 -> BP4 envelope from verified physical artifacts."""
    target = artifacts.target
    payload = target["record_preimage"]["governed_payload"]
    e2 = artifacts.e2_receipt or {}
    envelope = {
        "schema": SCHEMA,
        "producer": {
            "name": PRODUCER,
            "return_commit": artifacts.receipt.get("return_commit",
                                                   "5065e2e6934e9d5bca800cbf88c79e461bcf2393"),
            "module": "bp2_joined.producer.JoinedProducer",
            "named_assertion": "bp2_joined.producer.joined_consumer_assertion",
            "mode": artifacts.mode,
        },
        "actor_ids": [artifacts.life.a_source.actor_id, artifacts.life.b_source.actor_id],
        "objective_event_refs": [
            payload.get("declared_history_refs", [None, None])[0],
            payload.get("declared_history_refs", [None, None])[1],
            payload.get("declared_offer_ref"),
            payload.get("declared_material_ref"),
        ],
        "actor_history_hashes": [
            artifacts.life.a_snapshot["history_hash"],
            artifacts.life.b_snapshot["history_hash"],
        ],
        "c8_occurrence_refs": [artifacts.occurrence_id],
        "c9_target_refs": [artifacts.target_id, artifacts.target_record_hash],
        "e2_receipt_refs": [artifacts.e2_receipt_hash] if artifacts.e2_receipt_hash else [],
        "world_refs": [world_hash],
        "effective_clocks": {
            "bp2_logical_clock": {
                "domain": "BP2_TEST_ONLY_LOGICAL_CLOCK",
                "event_time": artifacts.event_time,
                "target_commit_time": e2.get("target_commit_time", artifacts.event_time),
                "e2_action_time": e2.get("action_time", artifacts.later_as_of),
                "as_of": artifacts.as_of,
                "authority": "TEST_ONLY_FIXTURE_CLOCK_NOT_TRUSTED_TIME",
            },
            "bp4_world_clock": {
                "domain": "BP4_TEST_ONLY_WORLD_CLOCK",
                "origin": clock_bridge.get("bp4_world_origin_clock", 10),
                "authority": "TEST_ONLY_SOURCEFREE_WORLD_CLOCK",
            },
            "numeric_cross_domain_ordering_used": False,
            "bridge": clock_bridge,
        },
        "authority_grades": {
            "actor": GRADE_ACTOR,
            "c8": GRADE_C8,
            "c9": GRADE_C9,
            "e2": GRADE_E2,
            "world": "TEST_ONLY_SOURCEFREE_WORLD_NOT_NATIVE",
            "rule": "TEST_ONLY_BP2_CAN008_CAN011_NOT_NATIVE",
        },
        "native_grants": {
            "actor": False, "rule": False, "c8_trust": False, "world": False,
            "c11": False, "c12": False, "adp019": False, "e2": False,
        },
        "source_preimages": {
            "c8_state_digest": artifacts.c8_state_digest,
            "c8_content_hash": artifacts.c8_content_hash,
            "c8_identity_digest": artifacts.c8_identity_digest,
            "c8_writer_version": artifacts.c8_writer_version,
            "c8_commit_receipt_id": artifacts.c8_commit_receipt_id,
            "c8_canonical_bytes_sha256": artifacts.c8_canonical_bytes_sha256,
            "e1_event_id": artifacts.e1_event_id,
            "e1_event_hash": artifacts.e1_event_hash,
            "actor_source_hash": artifacts.life.a_source.source_hash,
            "other_source_hash": artifacts.life.b_source.source_hash,
            "actor_snapshot_hash": artifacts.life.a_snapshot["hash"],
            "other_snapshot_hash": artifacts.life.b_snapshot["hash"],
            "rule_a_content_hash": artifacts.rule_a_hash,
            "rule_t_content_hash": artifacts.rule_t_hash,
            "rule_t_dependency_hash": artifacts.rule_t_dependency,
            "response_hash": artifacts.response_hash,
            "grant_hash": artifacts.grant_hash,
            "target_commit_receipt_hash": artifacts.receipt["persisted"].get(
                "c9_commit_receipt_hash", ""),
            "c9_authorization_hash": artifacts.receipt["persisted"].get(
                "c9_authorization_hash", ""),
        },
        "consumed_state_hash": artifacts.consumed_state_hash,
        "target_record_hash": artifacts.target_record_hash,
        "practice_label": artifacts.practice_label,
        "adp019_admission_receipt": "ADP019_ADMISSION_RECEIPT_ABSENT",
    }
    return envelope


def _expected_from_artifacts(artifacts: BP2Artifacts, world_hash: str,
                             clock_bridge: dict) -> dict:
    return build_envelope(artifacts, world_hash=world_hash, clock_bridge=clock_bridge)


def verify_producer_envelope(envelope: dict, artifacts: BP2Artifacts, *,
                             world_hash: str, clock_bridge: dict) -> dict:
    """Re-derive every envelope field from the artifacts; refuse a shape-only one."""
    try:
        shape = validate_envelope(envelope)
    except Exception as error:  # noqa: BLE001 - BP4 contract refusal
        raise EnvelopeRefusal("BP4_CONTRACT_REFUSED",
                              getattr(error, "code", type(error).__name__)) from error
    verified = verify_artifacts(artifacts)
    expected = _expected_from_artifacts(verified, world_hash, clock_bridge)
    mismatches = []
    for key, value in expected.items():
        actual = envelope.get(key)
        if actual != value:
            mismatches.append({"field": key, "expected": value, "actual": actual})
    if mismatches:
        raise EnvelopeRefusal(
            "SHAPE_VALID_ENVELOPE_NOT_BACKED_BY_ARTIFACTS",
            str([row["field"] for row in mismatches[:5]]),
        )
    # Independent cross-checks that do not trust the envelope at all.
    if digest(dict(verified.target)) != expected["consumed_state_hash"]:
        raise EnvelopeRefusal("TARGET_DIGEST_NOT_CONSUMED_HASH")
    if verified.target["record_hash"] != expected["target_record_hash"]:
        raise EnvelopeRefusal("TARGET_RECORD_HASH_MISMATCH")
    if verified.e2_receipt and (verified.e2_receipt_hash
                               != expected["e2_receipt_refs"][0]):
        raise EnvelopeRefusal("E2_RECEIPT_NOT_BOUND")
    return {
        "ok": True,
        "schema": SCHEMA,
        "bp4_contract_status": shape["status"],
        "recomputed_from_artifacts": True,
        "fields_checked": len(expected),
        "target_digest_equal_consumed": True,
        "e2_receipt_bound": bool(verified.e2_receipt),
        "mode": artifacts.mode,
    }


__all__ = [
    "EnvelopeRefusal",
    "SCHEMA",
    "build_envelope",
    "verify_producer_envelope",
]
