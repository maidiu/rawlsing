"""K35 unissued, no-actor, source-free causal-rule prototype.

NEVER an implementation of accepted CAN008 / ADP016 / ADP017. It models
proposed SM LAB_R_K3/LAB_R_K5 outputs for falsifiable mechanics only.
No actor, model, original survey, memory ledger, event admission, durable mutation.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import json
from typing import Literal

GRAIN = "ISOLATED_RULE_PROTOTYPE_ONLY__NOT_REAL_CAN008_RUNTIME"
Rule = Literal["K3", "K5"]
Variant = Literal["B0", "B1"]


def stable_hash(x: object) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()).hexdigest()


@dataclass(frozen=True)
class Fixture:
    rule: Rule
    event_id: str
    admitted: bool = True
    public_event_features: tuple[str, ...] = ("comment",)
    world_role: str = "NONE"
    world_owner_grant: bool = False
    history: str = "UNSAFE"
    trace_formed: bool = False
    trace_use_rule: bool = False
    child_feature_state: str = "UNAVAILABLE"
    analyst_only_childhood_origin: str = "sealed_origin_alpha"
    biography_annotation: str = "DO_NOT_USE"


class AccessLeakBlocked(ValueError):
    pass


def request_hidden_origin_claim(f: Fixture) -> None:
    # This is an intentional negative test, not a successful actor recall.
    if f.child_feature_state == "UNAVAILABLE":
        raise AccessLeakBlocked("BLOCK_UNAVAILABLE_CHILDHOOD_FEATURE_TO_FIRST_PERSON")
    raise AccessLeakBlocked("BLOCK_UNISSUED_ACTOR_CLAIM")


def evaluate(f: Fixture, variant: Variant = "B0") -> dict:
    if variant not in {"B0", "B1"} or f.rule not in {"K3", "K5"}:
        raise ValueError("unsupported sourcefree rule / comparator")
    # Immutable public occurrence contents are separated from analyst-only
    # history and unadmitted narrative; neither is an actor memory.
    event_hash = stable_hash((f.event_id, f.public_event_features))
    receipt = {
        "grain": GRAIN,
        "rule": f.rule,
        "variant": variant,
        "event_hash": event_hash,
        "status": None,
        "effect": "RESPONSE_EFFECTS_VALID_EMPTY",
        "trace_recruitment": "NONE",
        "claim": "DENY_FIRST_PERSON_CLAIM",
        "institutional_permission": "ABSENT",
        "world_effect": "NO_INSTITUTIONAL_CHANGE",
        "world_effect_is_committed": False,
        "actor_safe_view": {"event_features": f.public_event_features, "childhood_origin_claim": None},
    }
    # B1 has extra *hypothesized* latent state, derived from exactly the same
    # permitted input. It receives no privileged analyst origin or hidden data.
    latent = {"recognition_sensitivity": int(f.history == "UNSAFE"),
              "trace_pressure": int(f.trace_formed and f.trace_use_rule)} if variant == "B1" else None
    if not f.admitted:
        receipt["status"] = "BLOCK_UNADMITTED_EVENT"
    elif f.rule == "K3":
        if f.trace_formed and f.trace_use_rule:
            receipt["status"] = "PROTOTYPE_CAUSAL_EFFECT"
            receipt["trace_recruitment"] = "ADP016_TRACE_T7"
            receipt["effect"] = "BUFFER"
        else:
            receipt["status"] = "RESPONSE_EFFECTS_VALID_EMPTY"
    else:
        # Objective world authority and actor history are orthogonal axes.
        recognized = f.world_role == "OFFICIAL"
        receipt["institutional_permission"] = "PRESENT" if recognized else "ABSENT"
        if recognized and f.world_owner_grant:
            receipt["world_effect"] = "OFFICIAL_RECOGNITION"
        # This is a *would-request* label, not an operative world mutation.
        receipt["effect"] = "DEFLECT" if f.history == "UNSAFE" else ("REROUTE" if recognized else "AMPLIFY")
        receipt["status"] = "PROTOTYPE_CAUSAL_EFFECT"
    # B1 is not allowed to introduce a new result unless a held-out independent
    # typed discriminant is separately registered. It currently has none.
    if latent is not None:
        receipt["B1_extra_computation_not_semantic_authority"] = latent
    return receipt


def typed_projection(r: dict) -> dict:
    return {k: v for k, v in r.items() if k not in ("variant", "B1_extra_computation_not_semantic_authority")}


def visible_projection(r: dict) -> dict:
    return r["actor_safe_view"] | {"claim_permission": r["claim"]}


def all_predeclared_arms() -> dict[str, Fixture]:
    k3 = {"K3_A_TRACE": Fixture("K3", "E_ADULT", trace_formed=True, trace_use_rule=True),
          "K3_B_NO_TRACE": Fixture("K3", "E_ADULT"),
          "K3_C_UNAVAILABLE_NO_TRACE": Fixture("K3", "E_ADULT", child_feature_state="UNAVAILABLE")}
    k5 = {"K5_A_OFFICIAL_UNSAFE": Fixture("K5", "E_OFFICIAL_SAME_TEXT", world_role="OFFICIAL", world_owner_grant=True, history="UNSAFE"),
          "K5_B_PEER_TRUSTED": Fixture("K5", "E_OFFICIAL_SAME_TEXT", world_role="PEER", world_owner_grant=True, history="TRUSTED"),
          "K5_C_OFFICIAL_TRUSTED": Fixture("K5", "E_OFFICIAL_SAME_TEXT", world_role="OFFICIAL", world_owner_grant=True, history="TRUSTED"),
          "K5_D_PEER_UNSAFE": Fixture("K5", "E_OFFICIAL_SAME_TEXT", world_role="PEER", world_owner_grant=True, history="UNSAFE")}
    return k3 | k5
