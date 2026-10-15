"""SC0 two-contract port — contract core (sourcefree, TEST_FIXTURE_ONLY).

Contract 1: GENERIC_WORLD_SELECTION@1.0.0  (N9 selected-world value receipt)
Contract 2: GENERIC_ORDERED_POSSIBILITY@1.0.0 (N10E/N10W ordered possibility receipt)

Normative conservation laws transcribed independently from the SC0 frozen
envelope (blob 610ac870fde6cfe63796592b3c6b1e1bf1e37150) and oracles
(K9 9ccb66f9..., K10 e78b3ee9...).  No historical V558 stage name appears in
the public vocabulary.  Nothing here is adopted semantic law.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

WORLD_CONTRACT_ID = "GENERIC_WORLD_SELECTION@1.0.0"
POSSIBILITY_CONTRACT_ID = "GENERIC_ORDERED_POSSIBILITY@1.0.0"
FACADE_CONTRACT_ID = "GENERIC_WORLD_POSSIBILITY_DISPATCH_FACADE@1.0.0"
GRADE = "TEST_FIXTURE_ONLY__SOURCEFREE__NOT_OPERATIVE_N9__NOT_MODEL_USE"

# fields a physical provider may legitimately vary (K9 normalization policy)
ALLOWED_PROVIDER_VARIANT_PATHS = (
    "physical_provider_id",
    "physical_storage_locator",
    "physical_serialization",
    "physical_lineage_blob",
    "nonsemantic_cache_ids",
)

NOT_ALLOWED_TO_NORMALIZE = (
    "source_object_semantic_id",
    "native_response_value",
    "native_unit",
    "absolute_horizon",
    "roles_order",
    "nary_participants",
    "f2_requirement_ref",
    "time_axes",
    "permission_ceiling",
    "query_conditioner_order",
    "universe",
    "denominator",
    "support",
    "negative_state",
    "consumer_effect",
    "replay_semantic_digest",
)

CLOCK_AXES = (
    "observation_effective",
    "publication",
    "knowledge_as_of",
    "actor_event",
    "request",
)

NEGATIVE_STATES = (
    "OBSERVED_ZERO",
    "VALID_EMPTY",
    "MISSING",
    "UNDERPOWERED",
    "NOT_ASKED",
    "NONCOMPARABLE",
    "HELD_AUTHORITY",
    "DENIED",
)

PSYCHIC_TOKENS = (
    "EXPERIENCE", "PSYCH", "DESIRE", "GUILT", "RECOGNITION_FELT", "ATTITUDE_AS_PERSON",
    "PERSONAL_MEMORY", "ENNEAGRAM", "PERSONALITY", "TRAUMA", "FEELS_", "WANTS_",
)

CONSUMERS = (
    "CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY",
    "NONPARENT_APPRENTICESHIP_ENTRY",
)


class PortContractError(ValueError):
    code = "PORT_CONTRACT_ERROR"

    def __init__(self, code: str, reason: str):
        self.code = code
        self.reason = reason
        super().__init__(f"{code}: {reason}")


class SemanticLossError(PortContractError):
    code = "REJECT_SEMANTIC_LOSS"


class GradePromotionError(PortContractError):
    code = "REJECT_EPISTEMIC_PROMOTION"


class ActorFirewallError(PortContractError):
    code = "REJECT_ACTOR_FIREWALL"


class ReversalHeld(PortContractError):
    code = "HELD_AUTHORITY"


class PermissionDenied(PortContractError):
    code = "DENIED_USE"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def semantic_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# semantic projection (the conserved meaning layer)
# ---------------------------------------------------------------------------

def semantic_world_projection(selection: Mapping[str, Any]) -> dict[str, Any]:
    """Exact conserved semantic projection: everything except physical lineage."""

    world = selection["world"]
    out = {
        "semantic_world_id": world["semantic_world_id"],
        "source_ref": world["source_ref"],
        "source_release_ref": world["source_release_ref"],
        "epistemic_grade": world["epistemic_grade"],
        "native_unit": world["native_unit"],
        "native_strata": list(world["native_strata"]),
        "absolute_horizon": world["absolute_horizon"],
        "nary": canonical_json(world["nary"]),
        "f2": canonical_json(world["f2"]),
        "public_categories": list(world["public_categories"]),
        "public_sanctions": list(world["public_sanctions"]),
        "authority_ref": world["authority_ref"],
        "time_axes": dict(world["time_axes"]),
        "clock_mode": world["clock_mode"],
        "contradictory_alternatives": canonical_json(world["contradictory_alternatives"]),
        "support": dict(world["support"]),
        "negative_states": canonical_json(world["negative_states"]),
        "routes": canonical_json(world["routes"]),
        "permission_ceiling": dict(world["permission_ceiling"]),
        "values": canonical_json(world["values"]),
        "generated_binding_echo": canonical_json(world["generated_binding_echo"]),
        "f1_refs": list(world["f1_refs"]),
        "f2_requirement_ref": world["f2_requirement_ref"],
    }
    return out


def ordered_possibility_projection(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Conserved ordered-possibility projection (no physical lineage)."""

    return {
        "contract": receipt["contract"],
        "universe": receipt["universe"],
        "sampling_unit": receipt["sampling_unit"],
        "release": receipt["release"],
        "target": receipt["target"],
        "direction": receipt["direction"],
        "ordered_condition_chain": canonical_json(receipt["ordered_condition_chain"]),
        "support": dict(receipt["support"]),
        "minority": receipt["minority"],
        "routing": receipt["routing"],
        "risk_set": receipt["risk_set"],
        "weight": receipt["weight"],
        "uncertainty": receipt["uncertainty"],
        "model_use": receipt["model_use"],
        "permission_ceiling": dict(receipt["permission_ceiling"]),
        "walkback": canonical_json(receipt["walkback"]),
        "values_read": canonical_json(receipt["values_read"]),
    }


def consumer_effect_projection(receipt: Mapping[str, Any], consumer_id: str) -> dict[str, Any]:
    effect = receipt["consumer_effects"][consumer_id]
    values_read = dict(effect["values_read"])
    values_read.pop("provider_id", None)  # declared physical lineage, may vary
    return {
        "consumer_id": consumer_id,
        "output": canonical_json(effect["output"]),
        "values_read": canonical_json(values_read),
        "minority_alternatives": canonical_json(effect["minority_alternatives"]),
        "restrictions": canonical_json(effect["restrictions"]),
        "person_generation": effect["person_generation"],
    }


def compare_projections(a: Mapping[str, Any], b: Mapping[str, Any]) -> list[str]:
    """Return the list of unequal conserved fields (must be empty for equivalence)."""

    diffs = []
    for key in sorted(set(a) | set(b)):
        if a.get(key) != b.get(key):
            diffs.append(key)
    return diffs
