"""Typed durable owner state: CAN010 / CAN011 / ADP015 / ADP016 / ADP017 lab semantics.

These are SYNTHETIC bounded owner models for the laboratory only.  Each durable
change must name its destination owner, carry exact admitted parent event refs,
and pass its own owner's effect gate.  Cross-owner mutation is refused.  Owner
states are never rewritten in place: history is monotonic and effects are
appended with parent provenance.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from lab.hashutil import canonicalize, semantic_hash

OWNERS = ("CAN010", "CAN011", "ADP015", "ADP016", "ADP017", "WORLD_PUBLIC_RECORD")

OWNER_BOUNDARY_ERROR = "OWNER_BOUNDARY_SEIZURE"
MISSING_PARENT_ERROR = "EFFECT_WITHOUT_ADMITTED_PARENT"
UNKNOWN_OWNER_ERROR = "UNKNOWN_DESTINATION_OWNER"
REWRITE_ERROR = "PRIOR_STATE_REWRITE_ATTEMPT"


class OwnerEffectError(ValueError):
    def __init__(self, code: str, reason: str):
        self.code = code
        self.reason = reason
        super().__init__(f"{code}: {reason}")


@dataclass
class OwnerState:
    """Durable person organization formed by admitted actor<->world history."""

    CAN010: dict[str, Any] = field(default_factory=dict)  # expectations + strivings
    CAN011: dict[str, Any] = field(default_factory=dict)  # tensions + practices
    ADP015: dict[str, Any] = field(default_factory=dict)  # perceived relationships
    ADP016: dict[str, Any] = field(default_factory=dict)  # traces + episodic access
    ADP017: dict[str, Any] = field(default_factory=dict)  # claims + beliefs + permissions
    WORLD_PUBLIC_RECORD: dict[str, Any] = field(default_factory=dict)

    def material(self) -> dict[str, Any]:
        return {
            "CAN010": canonicalize(self.CAN010),
            "CAN011": canonicalize(self.CAN011),
            "ADP015": canonicalize(self.ADP015),
            "ADP016": canonicalize(self.ADP016),
            "ADP017": canonicalize(self.ADP017),
            "WORLD_PUBLIC_RECORD": canonicalize(self.WORLD_PUBLIC_RECORD),
        }

    def state_hash(self) -> str:
        return semantic_hash(self.material())

    def clone(self) -> "OwnerState":
        return state_from_material(self.material())


def state_from_material(material: Mapping[str, Any]) -> OwnerState:
    return OwnerState(
        CAN010=dict(material.get("CAN010", {})),
        CAN011=dict(material.get("CAN011", {})),
        ADP015=dict(material.get("ADP015", {})),
        ADP016=dict(material.get("ADP016", {})),
        ADP017=dict(material.get("ADP017", {})),
        WORLD_PUBLIC_RECORD=dict(material.get("WORLD_PUBLIC_RECORD", {})),
    )


def empty_state() -> OwnerState:
    return OwnerState(
        CAN010={"expectations": {}, "strivings": {}},
        CAN011={"tensions": {}, "practices": {}},
        ADP015={"relationships": {}},
        ADP016={"traces": {}, "episodic_access": {}},
        ADP017={"claim_permissions": {}, "beliefs": {}},
        WORLD_PUBLIC_RECORD={"standing": {}, "certifications": {}},
    )


def apply_effect(
    state: OwnerState,
    *,
    owner: str,
    effect_kind: str,
    target_key: str,
    payload: Mapping[str, Any],
    parent_event_refs: tuple[str, ...],
    effect_id: str,
) -> dict[str, Any]:
    """Apply one authorized durable effect to exactly one destination owner."""

    if owner not in OWNERS:
        raise OwnerEffectError(UNKNOWN_OWNER_ERROR, f"no such destination owner: {owner!r}")
    if not parent_event_refs:
        raise OwnerEffectError(MISSING_PARENT_ERROR, f"effect {effect_id} has no admitted parent event")
    bucket = getattr(state, owner)
    record = {
        "effect_id": effect_id,
        "effect_kind": effect_kind,
        "target_key": target_key,
        "payload": canonicalize(payload),
        "parent_event_refs": list(parent_event_refs),
        "owner": owner,
    }
    shelf = bucket.setdefault("effects", {})
    if effect_id in shelf:
        raise OwnerEffectError(REWRITE_ERROR, f"effect {effect_id} already committed; history is monotonic")
    shelf[effect_id] = record
    # materialize the typed view used by recruitment
    view = bucket.setdefault("view", {})
    entry = dict(payload)
    entry["parent_event_refs"] = list(parent_event_refs)
    entry["effect_id"] = effect_id
    view[target_key] = entry
    return record


def effect_receipt(record: Mapping[str, Any], pre_hash: str, post_hash: str) -> dict[str, Any]:
    return {
        "effect_id": record["effect_id"],
        "owner": record["owner"],
        "effect_kind": record["effect_kind"],
        "target_key": record["target_key"],
        "parent_event_refs": list(record["parent_event_refs"]),
        "owner_state_before_hash": pre_hash,
        "owner_state_after_hash": post_hash,
    }


def committed_effects(state: OwnerState) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for owner in OWNERS:
        for effect in getattr(state, owner).get("effects", {}).values():
            out.append(dict(effect))
    return sorted(out, key=lambda e: e["effect_id"])
