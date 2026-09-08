"""OBL059 R1 candidate: direct positive-applicability source authority.

This module is deliberately pure and side-effect free.  In this candidate wave it
will evaluate only NONCURRENT_SYNTHETIC fixtures.  Project-current issuance is
hard-blocked until later SUB-VOZHD/HQ adoption and runtime installation.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Dict, Iterable, List, Mapping, Tuple

AUTHORITY_ID = "OBL059_FIRST_POSITIVE_OEE_DIRECT_POSITIVE_APPLICABILITY_SOURCE_AUTHORITY@R1"
RECEIPT_VERSION = "OBL059_DIRECT_POSITIVE_APPLICABILITY_RECEIPT@R1"

FIRST_CANARY_SUBJECT_ID = (
    "urn:rawlsing:v3:subject:sha256:"
    "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
)
SUBJECT_CLASSIFICATION_PREDICATE = "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL"

ADP007_OWNER = "V3_ACTOR_INITIALIZATION_RULE@1.0.0"
ADP008_OWNER = "V3_DEVELOPMENTAL_PHASE_RULE@1.1.0"
ADP010_CONSUMER = "V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0"

SYNTHETIC_SCOPE = "NONCURRENT_SYNTHETIC"
POSITIVE_DECISION = "DIRECT_POSITIVE_APPLICABILITY"
NEGATIVE_DECISION = "NOT_DIRECTLY_APPLICABLE"

# These are explicitly not source-authority delegations for this lane.
FORBIDDEN_ALIAS_AUTHORITIES = frozenset(
    {
        "V554",
        "CAN-001",
        "CAN-003",
        "ROUTING",
        ADP010_CONSUMER,
    }
)

_REQUIRED_BINDINGS = (
    "actor_id",
    "subject_id",
    "world_id",
    "time_id",
    "adp010_opportunity_id",
)


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _valid_id(value: Any) -> bool:
    """Conservative opaque-ID validity without inventing a project-wide grammar."""
    if not isinstance(value, str):
        return False
    if not value or len(value) > 512 or value != value.strip():
        return False
    return not any(ch.isspace() or ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value)


def _base_receipt(packet: Mapping[str, Any], decision: str, reason: str) -> Dict[str, Any]:
    bindings = {
        key: packet.get(key)
        for key in _REQUIRED_BINDINGS
    }
    return {
        "receipt_version": RECEIPT_VERSION,
        "authority_id": AUTHORITY_ID,
        "execution_scope": packet.get("execution_scope"),
        "decision": decision,
        "reason": reason,
        "bindings": bindings,
        "consumer_rule": ADP010_CONSUMER,
        "proof_sha256": _sha256(packet),
        "evidence_ownership": [],
        # Negative capability / no-effect attestation is part of every result.
        "project_current_state_created": False,
        "actor_created_or_activated": False,
        "adp008_phase_transition_executed": False,
        "adp019_occurrence_admitted": False,
        "causal_use_permission_owned": False,
        "contact_witness_independence_owned": False,
        "encounter_created": False,
        "oee_realized": False,
        "obl055_executed": False,
        "current_positive_obl056_installed": False,
    }


def _deny(packet: Mapping[str, Any], reason: str) -> Dict[str, Any]:
    return _base_receipt(packet, NEGATIVE_DECISION, reason)


def _require_evidence_mapping(packet: Mapping[str, Any]) -> Tuple[Mapping[str, Any] | None, str | None]:
    evidence = packet.get("evidence")
    if not isinstance(evidence, Mapping):
        return None, "EVIDENCE_MISSING_OR_MALFORMED"
    return evidence, None


def _check_exact_scope(packet: Mapping[str, Any]) -> str | None:
    if packet.get("execution_scope") != SYNTHETIC_SCOPE:
        return "PROJECT_CURRENT_ISSUANCE_FORBIDDEN_IN_R1"

    for key in _REQUIRED_BINDINGS:
        if key not in packet:
            return f"MISSING_BINDING:{key}"
        if not _valid_id(packet.get(key)):
            return f"MALFORMED_BINDING:{key}"

    if packet["subject_id"] != FIRST_CANARY_SUBJECT_ID:
        return "WRONG_FIRST_CANARY_SUBJECT"

    opportunity = packet.get("opportunity")
    if not isinstance(opportunity, Mapping):
        return "OPPORTUNITY_BINDING_MISSING_OR_MALFORMED"

    expected = {
        "actor_id": packet["actor_id"],
        "subject_id": packet["subject_id"],
        "world_id": packet["world_id"],
        "time_id": packet["time_id"],
        "opportunity_id": packet["adp010_opportunity_id"],
        "consumer_rule": ADP010_CONSUMER,
    }
    for key, value in expected.items():
        if opportunity.get(key) != value:
            return f"OPPORTUNITY_SCOPE_MISMATCH:{key}"

    # Caller attempts to derive/alias this source authority fail closed.
    claim = packet.get("claimed_positive_applicability_source")
    if claim is not None:
        if claim in FORBIDDEN_ALIAS_AUTHORITIES:
            return f"FORBIDDEN_SOURCE_AUTHORITY_ALIAS:{claim}"
        if claim != AUTHORITY_ID:
            return "UNRECOGNIZED_SOURCE_AUTHORITY_CLAIM"

    return None


def _check_fresh(receipt: Mapping[str, Any], packet: Mapping[str, Any], label: str) -> str | None:
    if receipt.get("stale") is not False:
        return f"STALE_OR_UNDECLARED_FRESHNESS:{label}"
    if receipt.get("fresh_for_time_id") != packet["time_id"]:
        return f"WRONG_TIME_FRESHNESS:{label}"
    return None


def _check_evidence(packet: Mapping[str, Any], evidence: Mapping[str, Any]) -> Tuple[str | None, List[Dict[str, str]]]:
    ownership: List[Dict[str, str]] = []

    classification = evidence.get("subject_classification")
    if not isinstance(classification, Mapping):
        return "STRUCTURAL_CLASSIFICATION_EVIDENCE_MISSING", ownership
    if classification.get("subject_id") != packet["subject_id"]:
        return "SUBJECT_CLASSIFICATION_SCOPE_MISMATCH", ownership
    if classification.get("predicate") != SUBJECT_CLASSIFICATION_PREDICATE:
        return "SUBJECT_CLASSIFICATION_PREDICATE_MISMATCH", ownership
    if classification.get("jurisdiction") != "OBL048_SUBJECT_CLASSIFICATION":
        return "SUBJECT_CLASSIFICATION_JURISDICTION_MISMATCH", ownership
    classification_owner = classification.get("semantic_owner")
    if not _valid_id(classification_owner):
        return "SUBJECT_CLASSIFICATION_OWNER_MISSING_OR_MALFORMED", ownership
    if classification_owner == AUTHORITY_ID or classification_owner in FORBIDDEN_ALIAS_AUTHORITIES:
        return "SUBJECT_CLASSIFICATION_OWNER_ALIAS_FORBIDDEN", ownership
    freshness_error = _check_fresh(classification, packet, "subject_classification")
    if freshness_error:
        return freshness_error, ownership
    ownership.append(
        {
            "kind": "subject_classification",
            "semantic_owner": classification_owner,
            "jurisdiction": "OBL048_SUBJECT_CLASSIFICATION",
        }
    )

    actor = evidence.get("actor_activation")
    if not isinstance(actor, Mapping):
        return "ACTOR_ACTIVATION_EVIDENCE_MISSING", ownership
    if actor.get("semantic_owner") != ADP007_OWNER:
        return "ACTOR_ACTIVATION_WRONG_AUTHORITY", ownership
    if actor.get("actor_id") != packet["actor_id"]:
        return "ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id", ownership
    if actor.get("world_id") != packet["world_id"]:
        return "ACTOR_ACTIVATION_SCOPE_MISMATCH:world_id", ownership
    if actor.get("time_id") != packet["time_id"]:
        return "ACTOR_ACTIVATION_SCOPE_MISMATCH:time_id", ownership
    if actor.get("state") != "ACTIVE":
        return "ACTOR_NOT_ACTIVE", ownership
    freshness_error = _check_fresh(actor, packet, "actor_activation")
    if freshness_error:
        return freshness_error, ownership
    ownership.append(
        {
            "kind": "actor_activation",
            "semantic_owner": ADP007_OWNER,
            "jurisdiction": "ADP-007_ACTOR_CREATION_ACTIVATION",
        }
    )

    phase = evidence.get("developmental_phase")
    if not isinstance(phase, Mapping):
        return "DEVELOPMENTAL_PHASE_EVIDENCE_MISSING", ownership
    if phase.get("semantic_owner") != ADP008_OWNER:
        return "DEVELOPMENTAL_PHASE_WRONG_AUTHORITY", ownership
    if phase.get("actor_id") != packet["actor_id"]:
        return "DEVELOPMENTAL_PHASE_SCOPE_MISMATCH:actor_id", ownership
    if phase.get("world_id") != packet["world_id"]:
        return "DEVELOPMENTAL_PHASE_SCOPE_MISMATCH:world_id", ownership
    if phase.get("time_id") != packet["time_id"]:
        return "DEVELOPMENTAL_PHASE_SCOPE_MISMATCH:time_id", ownership
    if phase.get("phase") != "V3DP_DEVELOPMENT_ACTIVE":
        return "DEVELOPMENTAL_PHASE_NOT_ACTIVE", ownership
    freshness_error = _check_fresh(phase, packet, "developmental_phase")
    if freshness_error:
        return freshness_error, ownership
    ownership.append(
        {
            "kind": "developmental_phase",
            "semantic_owner": ADP008_OWNER,
            "jurisdiction": "ADP-008_DEVELOPMENTAL_PHASE_TRANSITION",
        }
    )

    return None, ownership


def evaluate_direct_positive_applicability(packet: Mapping[str, Any]) -> Dict[str, Any]:
    """Evaluate the OBL059 R1 candidate without mutating any project state.

    The positive semantic grain is intentionally narrow:
      exact first-canary subject + exact actor/world/time/ADP-010 opportunity
      + competent exact-scope actor/phase/structural receipts
      => source-owned DIRECT_POSITIVE_APPLICABILITY receipt.

    In R1, only NONCURRENT_SYNTHETIC execution is permitted.  This function
    never creates actor state, phase state, occurrences, permission,
    independence, encounter, OEE, OBL056 entries, or project-current facts.
    """
    if not isinstance(packet, Mapping):
        packet = {}
        return _deny(packet, "PACKET_MALFORMED")

    packet = deepcopy(dict(packet))

    scope_error = _check_exact_scope(packet)
    if scope_error:
        return _deny(packet, scope_error)

    evidence, evidence_error = _require_evidence_mapping(packet)
    if evidence_error:
        return _deny(packet, evidence_error)

    proof_error, ownership = _check_evidence(packet, evidence)
    if proof_error:
        receipt = _deny(packet, proof_error)
        receipt["evidence_ownership"] = ownership
        return receipt

    receipt = _base_receipt(packet, POSITIVE_DECISION, "EXACT_SCOPE_AND_REQUIRED_EVIDENCE_PROVED")
    receipt["evidence_ownership"] = ownership
    return receipt
