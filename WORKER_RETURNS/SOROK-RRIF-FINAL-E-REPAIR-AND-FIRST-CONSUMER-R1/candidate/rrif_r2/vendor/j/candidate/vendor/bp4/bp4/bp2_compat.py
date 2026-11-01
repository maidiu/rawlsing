"""Versioned receiving contract for the future BP2 joined producer.

BP2 is a separate concurrent campaign. This contract is a typed consumer-side
requirement, not an emitted BP2 envelope and not a claim that BP2 has returned.
"""
from __future__ import annotations

from .c10 import C10State

SCHEMA = "BP2_JOINED_EVENT_HISTORY_TARGET_E2_ENVELOPE@1"
STATUS = "AWAITING_ACTUAL_BP2_PRODUCER__COMPAT_CONTRACT_NOT_EMITTED"
REQUIRED = (
    "schema", "producer", "actor_ids", "objective_event_refs",
    "actor_history_hashes", "c8_occurrence_refs", "c9_target_refs",
    "e2_receipt_refs", "world_refs", "effective_clocks", "authority_grades",
    "native_grants",
)


class BP2Refusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def validate_envelope(envelope: dict) -> dict:
    if not isinstance(envelope, dict):
        raise BP2Refusal("ENVELOPE_NOT_OBJECT")
    missing = [field for field in REQUIRED if field not in envelope]
    if missing:
        raise BP2Refusal("MISSING_REQUIRED_FIELD", ",".join(missing))
    if envelope.get("schema") != SCHEMA:
        raise BP2Refusal("SCHEMA_MISMATCH")
    actors = envelope.get("actor_ids")
    if not isinstance(actors, list) or len(actors) < 2 or len(set(actors)) != len(actors):
        raise BP2Refusal("TWO_DISTINCT_ACTORS_REQUIRED")
    for field in ("objective_event_refs", "c8_occurrence_refs", "c9_target_refs",
                  "e2_receipt_refs", "world_refs"):
        if not isinstance(envelope.get(field), list) or not envelope[field]:
            raise BP2Refusal("NONEMPTY_SOURCE_REFS_REQUIRED", field)
    native = envelope.get("native_grants")
    if not isinstance(native, dict):
        raise BP2Refusal("NATIVE_GRANTS_MUST_BE_TYPED")
    if any(value is True for value in native.values()):
        if not all(envelope.get("authority_grades", {}).get(key)
                   for key in native if native[key] is True):
            raise BP2Refusal("SELF_GRANTED_NATIVE_AUTHORITY_REFUSED")
    return {"ok": True, "schema": SCHEMA, "status": STATUS,
            "consumed_fields": list(REQUIRED)}


def receiving_requirements() -> dict:
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "required": list(REQUIRED),
        "join_rule": (
            "When BP2 returns, replace the BP1/BP3/C9R compatibility seed with the "
            "actual emitted BP2 envelope; verify producer provenance, two distinct "
            "actors, C8 occurrence refs, C9 target refs, E2 receipt refs, world refs "
            "and effective clocks before any C10/C12 read."
        ),
        "must_not": [
            "fabricate a BP2 envelope",
            "promote sourcefree BP1/BP3/C9R to native",
            "merge actor identities",
            "overwrite BP2 or its subtree",
        ],
    }


def from_c10(c10: C10State) -> dict:
    """A typed adapter from this C10 read, not a BP2 emission."""
    return {
        "schema": SCHEMA,
        "status": "SOURCEFREE_C10_ADAPTER_NOT_BP2",
        "producer": "BP4_C10_RECEIVER",
        "actor_ids": ["A", "B"],
        "objective_event_refs": [c10.c9_target.get("middle_state_id", "")],
        "actor_history_hashes": [c10.actor_snapshots["A"]["history_hash"],
                                 c10.actor_snapshots["B"]["history_hash"]],
        "c8_occurrence_refs": list(c10.c8_ingress.get("occurrence_ids", [])),
        "c9_target_refs": [c10.receipt["c9_target_id"]],
        "e2_receipt_refs": ["TEST_ONLY_BP4_E2_RECEIPT"],
        "world_refs": [c10.world.get("hash", "")],
        "effective_clocks": {
            "objective_world": c10.receipt["objective_world_clock"],
            "actor": c10.receipt["actor_as_of"],
            "c9_commit": c10.receipt["c9_target_commit_time"],
        },
        "authority_grades": {
            "actor": c10.receipt["actor_source_grade"],
            "world": c10.receipt["world_grade"],
            "c8": "TEST_ONLY_BP3_KEYED_C8_NOT_NATIVE",
            "c9": "C9R_TEST_ONLY_NOT_NATIVE",
        },
        "native_grants": {
            "actor": False, "rule": False, "c8_trust": False,
            "world": False, "c11": False, "c12": False,
        },
    }


def native_slot_template() -> dict:
    """Exact future owner slots; all UNISSUED in this sourcefree return."""
    return {
        "schema": SCHEMA,
        "status": "UNISSUED_NATIVE_SLOTS",
        "slots": {
            "pyat_world_receipt": {"owner": "Pyat N11/N12", "status": "UNISSUED"},
            "adp007_actor": {"owner": "V3 actor initialization owner", "status": "UNISSUED"},
            "adp010_encounter": {"owner": "ADP010 OEE owner", "status": "UNISSUED"},
            "adp019_event": {"owner": "External Admission Court", "status": "UNISSUED"},
            "adp016_memory": {"owner": "causal memory owner", "status": "UNISSUED"},
            "adp017_access": {"owner": "knowledge/perception owner", "status": "UNISSUED"},
            "can008_rule_a": {"owner": "competent CAN008 rule issuer", "status": "UNISSUED"},
            "can011_rule_t": {"owner": "separate CAN011 target owner", "status": "UNISSUED"},
            "performed_e2": {"owner": "independent actuator owner", "status": "UNISSUED"},
            "c8_d1_d2_d3": {"owner": "Journal/key/anchor/ADP019 owners", "status": "UNISSUED"},
            "c11_weld": {"owner": "separately authorized C11 owner", "status": "UNISSUED"},
        },
    }
