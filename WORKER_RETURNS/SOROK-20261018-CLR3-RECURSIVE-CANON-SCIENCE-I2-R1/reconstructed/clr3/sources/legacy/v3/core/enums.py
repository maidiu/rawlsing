# v3/core/enums.py
# Canonical enums for backbone state. Aligned with v3config.yaml enums.

from typing import Literal

LoopTopology = Literal["reciprocal", "extractive", "self_contained"]
SolidarityBoundary = Literal["none", "transactional", "in_group", "expanding", "universal"]
TheoryOfChangeStyle = Literal[
    "witness_exposure",
    "mass_nonviolent_disruption",
    "armed_deterrence",
    "armed_insurrection",
    "institution_building",
]

CrackType = Literal[
    "shame_core",
    "rage_core",
    "dissociation",
    "nihilism",
    "intimacy_avoidance",
    "authority_fixation",
    "performance_compulsion",
    "moral_alibi",
]

BufferType = Literal[
    "piety",
    "ideology",
    "craft",
    "intimacy",
    "work",
    "intoxication",
    "status",
    "family_role",
    "health_regimen",
    "escapism",
]

# Domain names used for SL baseline (v3config)
DOMAIN_NAMES = ("empire_occupation", "nation_state", "sect_class_ethnicity", "family_household", "body_self")

# A/S/V as structured (new_version: domain_awareness_viscerality)
AwarenessLevel = Literal["unknown", "distorted", "partial", "structural"]
SolidarityLevel = Literal["aligned", "partial", "none"]  # + buffer type
VisceralityLevel = Literal["target", "proximate", "distant", "identified"]


def domain_axis_to_label(axis: str, value: float) -> str:
    """Map A/S/V 0-100 to structured label for state summary. Heuristic bands."""
    v = max(0, min(100, value))
    if axis == "A":
        if v < 25:
            return "unknown"
        if v < 50:
            return "distorted"
        if v < 75:
            return "partial"
        return "structural"
    if axis == "S":
        if v < 33:
            return "none"
        if v < 66:
            return "partial"
        return "aligned"
    if axis == "V":
        if v < 25:
            return "identified"
        if v < 50:
            return "distant"
        if v < 75:
            return "proximate"
        return "target"
    return ""


# Default scale for numeric fields
DEFAULT_MIN = 0
DEFAULT_MAX = 100
