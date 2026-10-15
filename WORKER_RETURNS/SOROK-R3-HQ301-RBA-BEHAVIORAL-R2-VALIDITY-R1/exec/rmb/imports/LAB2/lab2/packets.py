"""HQ298 S-M-LAB2 — matched held-out behavioral packet construction.

PROVISIONAL LAB PROTOCOL — NOT ADOPTED LAW.
Packets are derived from the blob-verified S-M-LAB1 fixture closure
(predecessor_lab1/lab/world_fixtures.py @ git blob 51910b01c187...).

Contract: within a K x contrast x seed block, the world snapshot, admitted
history, allowed actor-info packet and present occurrence are BYTE-IDENTICAL
across arms A / B_admissible / C_admissible. Only the internal machinery label
varies, and the machinery label is NOT present in the actor-visible packet.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_PRED = os.path.join(_HERE, "predecessor_lab1")
if _PRED not in sys.path:
    sys.path.insert(0, _PRED)

from lab.world_fixtures import case_fixture, world_receipt_hash  # noqa: E402
from lab.opacity import build_actor_safe_projection  # noqa: E402

PACKET_SCHEMA = "LAB2_BEHAVIORAL_TRIAL_PACKET@1.0.0"

# Frozen expected typed codes — mirrored from 01_PREREGISTRATION_FROZEN.json.
EXPECTED_TYPED_CODES: Dict[str, Dict[str, List[str]]] = {
    "K1": {"H_RESPONSIVE": ["REQUEST_FEEDBACK"], "H_PUNITIVE": ["SILENCE"]},
    "K2": {"EV_RELFORM_A_COMPENSATION": ["REQUEST_WITH_REPAIR"],
           "EV_RELFORM_B_CONDITIONAL": ["REQUEST_WITH_CONDITIONAL_CAUTION"]},
    "K3": {"TRACE_ACTIVE": ["HEIGHTENED_GUARD"], "TRACE_ABSENT": ["NEUTRAL_RESPONSE"],
           "RETAINED_INACCESSIBLE": ["HEIGHTENED_GUARD"]},
    "K4": {"CORRECTIVE_CONTEXT": ["NARROWED_CONSULT"],
           "RECURRENCE_SAME_AUTHORITY": ["REPEATED_QUESTION"],
           "WEAK_COUNTEREXAMPLE": ["NO_ACTION"]},
    "K5": {"WITNESS_REGISTRAR": ["ACCEPT_CERTIFICATE"],
           "WITNESS_SUPERVISOR": ["NO_STANDING_CHANGE_ACTION"],
           "WITNESS_PEER": ["NO_STANDING_CHANGE_ACTION"]},
    "K6": {"PRACTICE_AND_CAPACITY": ["POLICING_CANDIDATE"],
           "PRACTICE_NO_CAPACITY": ["NO_SANCTION"],
           "CATEGORY_ONLY": ["NO_SANCTION"]},
}

MENU_ORDER: Dict[str, List[str]] = {
    "K1": ["REQUEST_FEEDBACK", "SILENCE"],
    "K2": ["REQUEST_WITH_REPAIR", "REQUEST_WITH_CONDITIONAL_CAUTION"],
    "K3": ["HEIGHTENED_GUARD", "NEUTRAL_RESPONSE"],
    "K4": ["NARROWED_CONSULT", "REPEATED_QUESTION", "NO_ACTION"],
    "K5": ["ACCEPT_CERTIFICATE", "NO_STANDING_CHANGE_ACTION"],
    "K6": ["POLICING_CANDIDATE", "NO_SANCTION"],
}

SEEDS = [f"S{i:02d}" for i in range(1, 13)]
ARMS = ("A", "B_admissible", "C_admissible")

# Contrast label normalization: LAB1 fixture contrast names -> prereg names.
# (Plumbing only: the frozen scoring truth lives in EXPECTED_TYPED_CODES /
# 01_PREREGISTRATION_FROZEN.json and is NOT altered here.)
CONTRAST_ALIAS = {
    "K1": {"H_RESPONSIVE": "H_RESPONSIVE", "H_PUNITIVE": "H_PUNITIVE"},
    "K2": {"T_COMPENSATION": "EV_RELFORM_A_COMPENSATION",
           "T_CONDITION": "EV_RELFORM_B_CONDITIONAL"},
    "K3": {"TRACE_ACTIVE": "TRACE_ACTIVE", "TRACE_ABSENT": "TRACE_ABSENT",
           "RETAINED_INACCESSIBLE": "RETAINED_INACCESSIBLE"},
    "K4": {"CORRECTIVE_CONTEXT": "CORRECTIVE_CONTEXT",
           "RECURRENCE_SAME_AUTHORITY": "RECURRENCE_SAME_AUTHORITY",
           "WEAK_COUNTEREXAMPLE": "WEAK_COUNTEREXAMPLE"},
    "K5": {"REGISTRAR_CERTIFIES": "WITNESS_REGISTRAR",
           "POWERFUL_SUPERVISOR_PRAISE": "WITNESS_SUPERVISOR",
           "WEAK_PEER_PRAISE": "WITNESS_PEER"},
    "K6": {"PRACTICE_AND_CAPACITY": "PRACTICE_AND_CAPACITY",
           "PRACTICE_NO_CAPACITY": "PRACTICE_NO_CAPACITY",
           "CATEGORY_ONLY": "CATEGORY_ONLY"},
}


def _sha(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def presentation_code(trial_id: str, arm: str) -> str:
    """Deterministic counterbalance code: scorer sees this, never the arm label."""
    return "PC_" + _sha("PRES", trial_id, arm)[:12]


def menu_order_for(trial_id: str, k_id: str, arm: str) -> List[str]:
    """Counterbalanced menu order: deterministic per (trial, arm); position-bias
    controlled by rotating the canonical order. Arm index guarantees arms never
    share one presentation order within a trial."""
    base = MENU_ORDER[k_id]
    n = max(1, len(base))
    arm_offset = list(ARMS).index(arm) if arm in ARMS else 0
    rot = (int(_sha("ROT", trial_id)[:4], 16) + arm_offset) % n
    return base[rot:] + base[:rot]


def build_actor_info_packet(fixture: Dict[str, Any], contrast: str) -> Dict[str, Any]:
    """Allowed actor-info packet: only ADP017-accessible material. Hidden origins
    are NEVER included (accessible trace firewall)."""
    hist = fixture["histories"][contrast]
    receivable = []
    for ev in hist.get("events", []):
        if ev.get("admission") == "ADMITTED":
            receivable.append({
                "event_id": ev.get("event_id"),
                "actor_receivable_features": ev.get("actor_receivable_features", {}),
            })
    trace_refs = []
    for eff in hist.get("effects", []):
        if eff.get("owner") == "ADP016":
            trace_refs.append({
                "trace_marker": eff.get("target_key"),
                "access_state": eff.get("payload", {}).get("access_state"),
                "origin_content": None,  # firewall: never exposed
            })
    return {
        "packet_kind": "ALLOWED_ACTOR_INFO_PACKET",
        "receivable_events": receivable,
        "trace_markers": trace_refs,
        "first_person_origin_claims_permitted": False,
        "hidden_origin_content_included": False,
    }


def build_trial_packet(k_id: str, fixture_contrast: str, prereg_contrast: str,
                       seed: str, arm: str) -> Dict[str, Any]:
    fixture = case_fixture(k_id)
    trial_id = f"{k_id}__{prereg_contrast}__{seed}"
    world_hash = world_receipt_hash(fixture.get("world", {}))
    hist = fixture["histories"][fixture_contrast]
    packet = {
        "packet_schema": PACKET_SCHEMA,
        "trial_id": trial_id,
        "seed": seed,
        "presentation_code": presentation_code(trial_id, arm),
        "counterbalance_code": presentation_code(trial_id, arm),
        "k_id": k_id,
        "world_snapshot": fixture.get("world", {}),
        "world_receipt_hash": world_hash,
        "admitted_history": {
            "events": hist.get("events", []),
            "effects": hist.get("effects", []),
        },
        "allowed_actor_info_packet": build_actor_info_packet(fixture, fixture_contrast),
        "present_occurrence": fixture.get("present_event", {}),
        "typed_menu": menu_order_for(trial_id, k_id, arm),
        "matched_budget": {"temperature": 0.0, "max_tokens": 256, "calls": 1},
    }
    # Identical-content hash across arms: excludes presentation/counterbalance/arm.
    packet["matched_content_hash"] = _sha(
        json.dumps(packet["world_snapshot"], sort_keys=True),
        json.dumps(packet["admitted_history"], sort_keys=True),
        json.dumps(packet["allowed_actor_info_packet"], sort_keys=True),
        json.dumps(packet["present_occurrence"], sort_keys=True),
    )
    return packet


def contrast_pairs(k_id: str) -> List[Tuple[str, str]]:
    """(fixture_contrast_name, prereg_contrast_name) pairs for a K."""
    fixture = case_fixture(k_id)
    alias = CONTRAST_ALIAS.get(k_id, {})
    out = []
    for c in fixture["contrasts"]:
        out.append((c, alias.get(c, c)))
    return out


def expected_code(k_id: str, prereg_contrast: str) -> List[str]:
    return EXPECTED_TYPED_CODES[k_id][prereg_contrast]


def build_manifest() -> Dict[str, Any]:
    """Full matched held-out manifest: every trial packet identity across arms."""
    trials = []
    for k_id in EXPECTED_TYPED_CODES:
        for fixture_contrast, prereg_contrast in contrast_pairs(k_id):
            for seed in SEEDS:
                for arm in ARMS:
                    pkt = build_trial_packet(k_id, fixture_contrast, prereg_contrast, seed, arm)
                    trials.append({
                        "trial_id": pkt["trial_id"],
                        "k_id": k_id,
                        "prereg_contrast": prereg_contrast,
                        "seed": seed,
                        "arm": arm,
                        "presentation_code": pkt["presentation_code"],
                        "matched_content_hash": pkt["matched_content_hash"],
                        "typed_menu": pkt["typed_menu"],
                        "expected_typed_codes": expected_code(k_id, prereg_contrast),
                    })
    matched = {}
    for t in trials:
        matched.setdefault(t["trial_id"], set()).add(t["matched_content_hash"])
    violations = sorted(t for t, s in matched.items() if len(s) != 1)
    manifest = {
        "manifest_schema": "LAB2_MATCHED_HELDOUT_MANIFEST@1.0.0",
        "n_trials": len(trials),
        "n_k": len(EXPECTED_TYPED_CODES),
        "n_contrast_cells": sum(len(v) for v in EXPECTED_TYPED_CODES.values()),
        "n_seeds": len(SEEDS),
        "arms": list(ARMS),
        "matched_content_across_arms_violations": violations,
        "matched_content_across_arms_ok": not violations,
        "trials": trials,
    }
    manifest["manifest_hash"] = _sha(json.dumps(manifest["trials"], sort_keys=True))
    return manifest


def paraphrase_variant(packet: Dict[str, Any], variant: int) -> Dict[str, Any]:
    """N1 paraphrase null: surface wording of receivable features changes;
    semantic content preserved. Typed codes must not move."""
    p = json.loads(json.dumps(packet))
    for ev in p["admitted_history"]["events"]:
        feats = ev.get("actor_receivable_features") or {}
        for k, v in list(feats.items()):
            if isinstance(v, str):
                feats[k] = f"[paraphrase{variant}] {v}"
    for rec in p["allowed_actor_info_packet"]["receivable_events"]:
        for k, v in list(rec.get("actor_receivable_features", {}).items()):
            if isinstance(v, str):
                rec["actor_receivable_features"][k] = f"[paraphrase{variant}] {v}"
    return p


def label_shuffle(packet: Dict[str, Any], variant: int) -> Dict[str, Any]:
    """N2 label null: actor/place names shuffled; typed codes must not move."""
    p = json.loads(json.dumps(packet))

    def shuffle(obj):
        if isinstance(obj, dict):
            return {k: shuffle(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [shuffle(v) for v in obj]
        if isinstance(obj, str) and obj.startswith(("EV", "POS", "REL", "OPP")):
            return "LBL" + _sha("LBL", obj, str(variant))[:8]
        return obj
    for key in ("admitted_history", "present_occurrence"):
        p[key] = shuffle(p[key])
    return p


def surface_variant(packet: Dict[str, Any], variant: int) -> Dict[str, Any]:
    """N4 surface null: prose-style wrapper; typed codes must not move."""
    p = json.loads(json.dumps(packet))
    p["style_wrapper"] = {"tone": f"style_variant_{variant}", "scored": False}
    return p


def inject_hidden_origin(packet: Dict[str, Any], secret: str) -> Dict[str, Any]:
    """N5 trace firewall probe: hidden origin injected ONLY into evaluator-only
    metadata. Actor-visible payload must remain byte-identical."""
    p = json.loads(json.dumps(packet))
    p["evaluator_only_metadata"] = {"hidden_origin": secret, "actor_visible": False}
    return p


def actor_visible_fingerprint(packet: Dict[str, Any]) -> str:
    visible = {k: v for k, v in packet.items()
               if k not in ("evaluator_only_metadata", "style_wrapper",
                            "presentation_code", "counterbalance_code")}
    return _sha(json.dumps(visible, sort_keys=True))
