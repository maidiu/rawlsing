"""HQ298 S-M-LAB2 — model-call authorization gate.

PROVISIONAL LAB PROTOCOL — NOT ADOPTED LAW.
ZERO paid/actor/external model calls may pass this gate without a complete,
competently-issued grant. Prior authoring-environment use does NOT license
model-actor trials. Do not submit calls by inference.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional

GATE_ID = "LAB2_MODEL_CALL_AUTHORIZATION_GATE"
GATE_VERSION = "1.0.0"

REQUIRED_FIELDS = (
    "named_provider_exact_endpoint",
    "exact_model_and_version_pin",
    "privacy_permission_for_synthetic_lab_packets",
    "experiment_use_grant_behavioral_actor_trials",
    "explicit_monetary_cap",
    "price_class_and_quota_observed",
    "raw_request_response_retention_permission",
    "per_trial_call_budget",
)

HOLD_ID = "MODEL_BEHAVIORAL_HOLD"


class ModelCallDenied(Exception):
    """Raised on any attempt to issue a model call without a complete grant."""


@dataclass
class Grant:
    named_provider_exact_endpoint: Optional[str] = None
    exact_model_and_version_pin: Optional[str] = None
    privacy_permission_for_synthetic_lab_packets: Optional[str] = None
    experiment_use_grant_behavioral_actor_trials: Optional[str] = None
    explicit_monetary_cap: Optional[str] = None
    price_class_and_quota_observed: Optional[str] = None
    raw_request_response_retention_permission: Optional[str] = None
    per_trial_call_budget: Optional[int] = None

    def missing_fields(self) -> list[str]:
        out = []
        for f in REQUIRED_FIELDS:
            v = getattr(self, f)
            if v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, int) and v <= 0):
                out.append(f)
        return out

    def is_complete(self) -> bool:
        return not self.missing_fields()


@dataclass
class GateDecision:
    gate_id: str
    gate_version: str
    allowed: bool
    hold_id: Optional[str]
    missing_fields: list[str]
    missing_authority_class: str
    model_calls_permitted: int
    reason: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


def evaluate_gate(grant: Optional[Grant]) -> GateDecision:
    """No grant or incomplete grant => MODEL_BEHAVIORAL_HOLD, zero calls permitted."""
    g = grant if grant is not None else Grant()
    missing = g.missing_fields()
    if missing:
        return GateDecision(
            gate_id=GATE_ID, gate_version=GATE_VERSION, allowed=False,
            hold_id=HOLD_ID, missing_fields=missing,
            missing_authority_class="MISSING_ACTOR_OR_MODEL_USE_AUTHORITY",
            model_calls_permitted=0,
            reason=(
                "grant incomplete: named provider, exact model/version pin, privacy "
                "permission, experiment-use grant, explicit monetary cap and call budget "
                "must ALL be present before any paid/actor/external model call; "
                "prior authoring-environment use does not license model-actor trials"
            ),
        )
    return GateDecision(
        gate_id=GATE_ID, gate_version=GATE_VERSION, allowed=True,
        hold_id=None, missing_fields=[],
        missing_authority_class="NONE",
        model_calls_permitted=g.per_trial_call_budget or 0,
        reason="complete grant; re-verify immediately before first call",
    )


def require_call_permission(grant: Optional[Grant]) -> GateDecision:
    """Callable by the behavioral runner before every single call."""
    d = evaluate_gate(grant)
    if not d.allowed:
        raise ModelCallDenied(
            f"{HOLD_ID}: missing grant fields {d.missing_fields}")
    return d
