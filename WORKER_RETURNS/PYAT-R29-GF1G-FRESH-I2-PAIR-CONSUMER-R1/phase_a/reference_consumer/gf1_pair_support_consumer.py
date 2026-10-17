"""GF1G Phase A — INDEPENDENT reference consumer (NOT the GF1E candidate).

Authored from the pre-GF1E contract only:
  * PYAT R17 01_PRECOMMITTED_GENERIC_NATIVE_PAIR_ORACLE.json
  * PYAT R23 GF1C recovered contract GF1_PAIR_SUPPORT_SIGNATURE_CONSUMER_TEST_ONLY@1.0.0
  * the frozen original 44 (court/repro/test_gf1_generic_pair.py)
  * the pre-GF1E generic producer (court/runtime_root/generic_native_pair_relation.py)

Purpose: independently derive the expected classifications, vectors and hashes and
freeze them BEFORE the GF1E consumer is inspected or executed. This module is a
REFERENCE, not a claim about the GF1E candidate.
"""
from __future__ import annotations

import hashlib
import json

from generic_native_pair_relation import (
    GENERIC_CONSUMER_ID,
    GENERIC_RELATION_OWNER,
    GENERIC_RESULT_FAMILY,
    ZERO_CELL_STATES,
    canonical_json,
    semantic_hash,
)

REFERENCE_ID = "GF1G_PHASE_A_INDEPENDENT_REFERENCE_CONSUMER"

EXACT = "EXACT_PAIR_SEPARATION"
NO = "NO_PAIR_SEPARATION"
NO_RISK = "UNDETERMINED_NO_ELIGIBLE_RISK"
ZERO = "UNDETERMINED_ZERO_SUPPORT_RISK"

COMPUTED = "PAIR_SUPPORT_SIGNATURE_COMPUTED"
INVALID = "CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION"
EMPTY = "RESPONSE_INPUTS_VALID_EMPTY"
INCONSISTENT = "CONSUMER_INPUT_INCONSISTENT_DENOMINATOR"
INVALID_CELL = "CONSUMER_INPUT_INVALID_CELL_STATE"
BLOCKING = "PRODUCER_TYPED_STATE_BLOCKING"
BLOCKING_ZERO = "PRODUCER_TYPED_STATE_ZERO_SUPPORT"
SUPPORT_EXCEEDS_RISK = "CONSUMER_INPUT_SUPPORT_EXCEEDS_ELIGIBLE_RISK"

ZERO_TYPED_STATES = frozenset({
    "ZERO_SUPPORT", "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"})


def _is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _read(relation):
    """Return a structural read of the relation or a typed refusal."""
    proj_getter = getattr(relation, "semantic_projection", None)
    if not callable(proj_getter):
        return None, "not a generic pair relation"
    try:
        proj = proj_getter()
    except Exception as exc:  # noqa: BLE001
        return None, f"projection unavailable: {exc}"
    if not isinstance(proj, dict):
        return None, "projection is not a mapping"
    if proj.get("semantic_owner") != GENERIC_RELATION_OWNER:
        return None, "semantic owner is not the generic pair owner"
    if proj.get("relation_family") != "GF1_GENERIC_NATIVE_PAIR_RELATION_TEST_ONLY@1.0.0":
        return None, "relation family is not the generic pair family"
    digest = semantic_hash(proj)
    if getattr(relation, "content_hash", None) != digest:
        return None, "content hash does not bind the projection"
    if getattr(relation, "object_id", None) != (
            f"urn:rawlsing:gf1:generic-pair-relation:sha256:{digest}"):
        return None, "object id does not bind the projection"
    return relation, None


def _typed_profile(relation):
    """Validate and normalise the conditional profile. Returns (profile, error)."""
    rows = list(getattr(relation, "conditional_count_profile", ()) or ())
    seen_states = set()
    profile = []
    for row in rows:
        if not isinstance(row, dict):
            return None, "profile row is not a mapping"
        state = row.get("condition_state")
        key = json.dumps(state, sort_keys=True)
        if key in seen_states:
            return None, "duplicate condition state"
        seen_states.add(key)
        denominator = row.get("condition_denominator_support")
        if not _is_int(denominator) or denominator < 0:
            return None, "condition denominator is not a nonnegative exact integer"
        targets = list(row.get("target_counts") or ())
        if not targets:
            return None, "condition has no target counts"
        seen_targets = set()
        counts = {}
        for cell in targets:
            if not isinstance(cell, dict):
                return None, "target count is not a mapping"
            target = cell.get("target_state")
            tkey = json.dumps(target, sort_keys=True)
            if tkey in seen_targets:
                return None, "duplicate target state"
            seen_targets.add(tkey)
            count = cell.get("joint_support_count")
            if not _is_int(count) or count < 0:
                return None, "joint support is not a nonnegative exact integer"
            cell_state = cell.get("joint_cell_state")
            if count == 0 and cell_state not in ZERO_CELL_STATES:
                return None, "zero joint count has an inconsistent cell state"
            if count > 0 and cell_state != "OBSERVED_POSITIVE":
                return None, "positive joint count has an inconsistent cell state"
            counts[tkey] = (target, count, cell_state)
        if sum(v[1] for v in counts.values()) != denominator:
            return None, "condition denominator does not equal the target-count sum"
        profile.append({
            "condition_state": state,
            "denominator": denominator,
            "targets": sorted(counts.values(), key=lambda v: json.dumps(v[0], sort_keys=True)),
        })
    return profile, None


def compute_pair_support_signature(relation) -> dict:
    read, why = _read(relation)
    if read is None:
        return {
            "consumer_id": GENERIC_CONSUMER_ID,
            "reference_implementation": REFERENCE_ID,
            "decision_state": INVALID,
            "separation_class": None,
            "downstream_value_produced": False,
            "generic_native_semantics_hold": "RETAINED",
            "refusal_reason": why,
            "is_population_evidence_not_actor_fact": True,
            "makes_no_causal_or_psychological_claim": True,
            "production_owner_commit": False,
        }
    typed_state = getattr(read, "typed_state", None)
    profile, why = _typed_profile(read)
    base = {
        "consumer_id": GENERIC_CONSUMER_ID,
        "consumer_output_family": GENERIC_RESULT_FAMILY,
        "reference_implementation": REFERENCE_ID,
        "read_relation_object_id": getattr(read, "object_id", None),
        "read_relation_content_hash": getattr(read, "content_hash", None),
        "read_relation_owner": GENERIC_RELATION_OWNER,
        "read_relation_typed_state": typed_state,
        "eligible_joint_risk_total": getattr(read, "eligible_joint_risk_total", None),
        "generic_native_semantics_hold": "RETAINED",
        "is_population_evidence_not_actor_fact": True,
        "makes_no_causal_or_psychological_claim": True,
        "production_owner_commit": False,
    }
    if why is not None:
        base.update({
            "decision_state": INCONSISTENT if "denominator" in why else INVALID_CELL,
            "separation_class": None,
            "downstream_value_produced": False,
            "refusal_reason": why,
            "support_vectors": [],
            "zero_cell_semantics": {},
            "joint_support_total": None,
            "condition_states_with_positive_denominator": [],
            "separation_signature": None,
        })
    elif typed_state != "SUPPORTED":
        zero_typed = typed_state in ZERO_TYPED_STATES
        base.update({
            "decision_state": BLOCKING_ZERO if zero_typed else BLOCKING,
            "separation_class": ZERO if zero_typed else None,
            "downstream_value_produced": False,
            "support_vectors": [],
            "zero_cell_semantics": {},
            "joint_support_total": 0,
            "condition_states_with_positive_denominator": [],
            "separation_signature": f"BLOCKING::{typed_state}",
        })
    elif not profile:
        base.update({
            "decision_state": EMPTY,
            "separation_class": ZERO,
            "downstream_value_produced": False,
            "support_vectors": [],
            "zero_cell_semantics": {},
            "joint_support_total": 0,
            "condition_states_with_positive_denominator": [],
            "separation_signature": "EMPTY_PROFILE",
        })
    else:
        vectors = []
        zero_sem = {}
        total = 0
        positive_states = []
        for row in profile:
            state = row["condition_state"]
            state_key = json.dumps(state, sort_keys=True)
            counts = []
            for target, count, cell_state in row["targets"]:
                counts.append({
                    "target_state": target,
                    "joint_support_count": count,
                    "joint_cell_state": cell_state,
                })
                total += count
                if count == 0:
                    zero_sem[f"{state_key}:{json.dumps(target, sort_keys=True)}"] = cell_state
            if row["denominator"] > 0:
                positive_states.append(state)
            vectors.append({
                "condition_state": state,
                "condition_denominator_support": row["denominator"],
                "target_counts": counts,
            })
        signature = "|".join(
            "%s:%s@%d" % (
                json.dumps(v["condition_state"], sort_keys=True),
                ",".join(str(c["joint_support_count"]) for c in v["target_counts"]),
                v["condition_denominator_support"],
            )
            for v in vectors
        )
        eligible = getattr(read, "eligible_joint_risk_total", None)
        if typed_state != "SUPPORTED":
            decision = BLOCKING_ZERO if typed_state in ZERO_TYPED_STATES else BLOCKING
            separation = ZERO if typed_state in ZERO_TYPED_STATES else None
            downstream = False
        elif not _is_int(eligible) or eligible < 0:
            decision = INCONSISTENT
            separation = None
            downstream = False
        elif total > eligible:
            decision = SUPPORT_EXCEEDS_RISK
            separation = None
            downstream = False
        elif total == 0:
            decision = COMPUTED
            separation = ZERO if eligible > 0 else NO_RISK
            downstream = True
        elif any(v["condition_denominator_support"] == 0 for v in vectors):
            decision = COMPUTED
            separation = NO_RISK
            downstream = True
        else:
            modes = []
            degenerate = True
            for v in vectors:
                positive = [c for c in v["target_counts"] if c["joint_support_count"] > 0]
                if len(positive) != 1 or positive[0]["joint_support_count"] != \
                        v["condition_denominator_support"]:
                    degenerate = False
                    break
                modes.append(json.dumps(positive[0]["target_state"], sort_keys=True))
            if degenerate and len(set(modes)) == len(modes):
                separation = EXACT
            else:
                separation = NO
            decision = COMPUTED
            downstream = True
        base.update({
            "decision_state": decision,
            "separation_class": separation,
            "separation_signature": signature,
            "support_vectors": vectors,
            "zero_cell_semantics": zero_sem,
            "joint_support_total": total,
            "condition_states_with_positive_denominator": positive_states,
            "downstream_value_produced": downstream,
        })
    payload = {k: v for k, v in base.items() if k != "result_hash"}
    base["result_hash"] = hashlib.sha256(
        canonical_json(payload).encode()).hexdigest()
    return base
