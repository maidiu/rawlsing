"""
v3/io/seed_frameworks.py

Seed real frameworks and cracks from identity signals before the first LLM band runs.

WHY: `backbone_state_from_identity()` initializes state.frameworks = [] and state.cracks = [].
The LLM filters out placeholder content (llm_contract.py:540-558), so if no real frameworks
or cracks exist, Pass 1 gets no ideological hooks → generic events → wound_vector stays at
defaults → ideology-level texture of the persona is never generated.

WHAT: Build 3-6 named frameworks and 2-4 named cracks from identity signals (religion,
class, minority_status, age, transmission_regime). These are initial conditions, not life
events — they represent the ideological/psychological starting point of this person's
background before the simulation runs.

Framework structure (v3/core/state.py):
    id: str                          # named strategy, e.g. "moderate_faith_practice"
    weight: float                    # initial influence 0–100
    acute_delta: dict[str, float]    # capacity field → delta (first N years)
    chronic_delta: dict[str, float]  # capacity field → delta (after half_life_years)
    half_life_years: int             # when acute benefits decay into chronic costs
    failure_mode: str                # what goes wrong: legalistic_hardening, nihilistic_drift, etc.
    enemy_requirement: float         # 0 = no enemy needed, 100 = strong in-group/out-group
    institutional_affinities: list[str]  # strata that reward this framework
    tenure_years: int                # starts at 0

Crack structure (v3/core/state.py):
    type: str           # named tension domain, e.g. "sacred_vs_reality"
    intensity: float    # structural tension strength 0–100
    latent_pressure: float  # psychological charge 0–100
    active: bool
    origin_year: int
"""

from __future__ import annotations

from typing import Any


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


# ---------------------------------------------------------------------------
# Framework recipes — each is a callable that returns a dict or None
# ---------------------------------------------------------------------------

def _faith_framework(religiosity: float, religion: str, age: int) -> list[dict]:
    """Faith frameworks: devout / moderate / post-religious / disenchanted."""
    rel = (religion or "").strip()
    if not rel or rel in ("—", "Unknown", "None", "none"):
        return []
    if religiosity >= 72:
        return [{
            "id": "devout_faith_frame",
            "weight": _clamp(religiosity * 0.9),
            "acute_delta": {"coherence": 6.0, "binding": 5.0, "aperture": -3.0},
            "chronic_delta": {"coherence": 2.0, "binding": 3.0, "aperture": -5.0},
            "half_life_years": 15,
            "failure_mode": "legalistic_hardening",
            "enemy_requirement": 20.0,
            "institutional_affinities": ["religion", "family", "community"],
            "tenure_years": max(0, age - 5),
        }]
    elif religiosity >= 38:
        return [{
            "id": "moderate_faith_practice",
            "weight": _clamp(religiosity * 0.75),
            "acute_delta": {"coherence": 3.0, "binding": 2.0},
            "chronic_delta": {"coherence": 0.5},
            "half_life_years": 20,
            "failure_mode": "gradual_secularization",
            "enemy_requirement": 5.0,
            "institutional_affinities": ["religion", "family"],
            "tenure_years": max(0, age - 6),
        }]
    else:
        # Low religiosity — drifting from or indifferent to faith
        return [{
            "id": "post_religious_drift",
            "weight": _clamp(60.0 - religiosity),
            "acute_delta": {"aperture": 4.0, "coherence": -2.0},
            "chronic_delta": {"coherence": -4.0, "binding": -2.0},
            "half_life_years": 12,
            "failure_mode": "nihilistic_drift",
            "enemy_requirement": 0.0,
            "institutional_affinities": ["education", "peer_group"],
            "tenure_years": max(0, age - 10),
        }]


def _class_framework(ses: str, age: int) -> list[dict]:
    """Class / economic frameworks: meritocracy, survival pragmatism, solidarity."""
    ses = (ses or "middle").replace(" ", "_").lower()
    if ses in ("elite", "upper_middle"):
        return [{
            "id": "legitimacy_entrenchment_frame",
            "weight": 60.0,
            "acute_delta": {"coherence": 4.0, "agency": 3.0},
            "chronic_delta": {"aperture": -3.0, "binding": -2.0},
            "half_life_years": 25,
            "failure_mode": "social_insulation_collapse",
            "enemy_requirement": 10.0,
            "institutional_affinities": ["work", "school", "government"],
            "tenure_years": max(0, age - 5),
        }]
    elif ses in ("middle", "lower_middle"):
        return [{
            "id": "meritocracy_achievement_frame",
            "weight": 58.0,
            "acute_delta": {"agency": 5.0, "skill": 2.0, "coherence": 2.0},
            "chronic_delta": {"agency": 1.0, "coherence": -1.0},
            "half_life_years": 20,
            "failure_mode": "self_blame_collapse",
            "enemy_requirement": 5.0,
            "institutional_affinities": ["school", "work"],
            "tenure_years": max(0, age - 6),
        }]
    else:
        # Working / underclass: survival pragmatism or solidarity, depending on tenure
        return [{
            "id": "survival_pragmatism_frame",
            "weight": 65.0,
            "acute_delta": {"agency": 3.0, "risk_tolerance": 4.0},
            "chronic_delta": {"coherence": -2.0, "binding": 1.0},
            "half_life_years": 15,
            "failure_mode": "chronic_exhaustion_retreat",
            "enemy_requirement": 15.0,
            "institutional_affinities": ["work", "family"],
            "tenure_years": max(0, age - 8),
        }]


def _identity_search_framework(age: int) -> list[dict]:
    """Young / fragmented identity: searching phase framework."""
    if age < 28:
        # Weight decays as persona integrates identity post-25
        weight = _clamp(75.0 - max(0.0, (age - 18) * 3.5))
        return [{
            "id": "identity_search_frame",
            "weight": weight,
            "acute_delta": {"aperture": 5.0, "coherence": -3.0, "agency": -1.0},
            "chronic_delta": {"coherence": -2.0},
            "half_life_years": 8,
            "failure_mode": "chronic_incoherence",
            "enemy_requirement": 0.0,
            "institutional_affinities": ["school", "peer_group"],
            "tenure_years": max(0, age - 14),
        }]
    return []


def _minority_framework(minority_status: str, age: int) -> list[dict]:
    """Group loyalty vs. institutional trust based on minority status."""
    status = (minority_status or "dominant").lower()
    if status in ("minoritized", "mixed"):
        return [{
            "id": "in_group_solidarity_frame",
            "weight": 62.0,
            "acute_delta": {"binding": 4.0, "coherence": 2.0, "agency": -1.0},
            "chronic_delta": {"binding": 2.0, "aperture": -2.0},
            "half_life_years": 30,
            "failure_mode": "sectarian_rigidity",
            "enemy_requirement": 35.0,
            "institutional_affinities": ["community", "family"],
            "tenure_years": max(0, age - 6),
        }]
    else:
        # Dominant group: institutional trust, may decay if disillusionment hits
        return [{
            "id": "institutional_trust_frame",
            "weight": 52.0,
            "acute_delta": {"coherence": 3.0, "agency": 2.0},
            "chronic_delta": {"coherence": -1.0},
            "half_life_years": 20,
            "failure_mode": "disillusionment_rupture",
            "enemy_requirement": 5.0,
            "institutional_affinities": ["school", "work", "government"],
            "tenure_years": max(0, age - 8),
        }]


# ---------------------------------------------------------------------------
# Crack recipes
# ---------------------------------------------------------------------------

def _sacred_crack(religiosity: float, religion: str, year: int, age: int) -> list[dict]:
    """Tension between sacred/moral framework and lived reality — seeds for any religious persona."""
    rel = (religion or "").strip()
    if not rel or rel in ("—", "Unknown", "None", "none") or religiosity < 20:
        return []
    # Higher religiosity → stronger initial investment → bigger crack potential when violated
    intensity = _clamp(15.0 + religiosity * 0.25)
    return [{
        "type": "sacred_vs_reality",
        "intensity": intensity,
        "latent_pressure": _clamp(intensity * 0.6),
        "active": True,
        "origin_year": max(year - age, year - age + 5),  # early childhood
    }]


def _family_stability_crack(ses: str, year: int, age: int) -> list[dict]:
    """Family-vs-stability tension: seeds for working/lower class or housing-insecure backgrounds."""
    ses = (ses or "middle").replace(" ", "_").lower()
    if ses in ("working", "lower_middle", "underclass"):
        intensity = {"underclass": 45.0, "working": 30.0, "lower_middle": 18.0}.get(ses, 18.0)
        return [{
            "type": "family_vs_stability",
            "intensity": intensity,
            "latent_pressure": intensity * 0.7,
            "active": True,
            "origin_year": max(year - age, year - age + 3),
        }]
    return []


def _identity_coherence_crack(age: int, year: int) -> list[dict]:
    """Identity coherence tension: universal for young personas, decays in adulthood."""
    if age < 30:
        intensity = _clamp(25.0 + max(0.0, (22 - age) * 2.0))
        return [{
            "type": "identity_coherence_vs_fragmentation",
            "intensity": intensity,
            "latent_pressure": intensity * 0.5,
            "active": True,
            "origin_year": max(year - age, year - age + 12),  # adolescence
        }]
    return []


def _class_aspiration_crack(ses: str, minority_status: str, year: int, age: int) -> list[dict]:
    """Status aspiration vs. origin: for upwardly-mobile or class-anxious personas."""
    ses = (ses or "middle").replace(" ", "_").lower()
    minority = (minority_status or "dominant").lower()
    if ses in ("working", "lower_middle") or minority == "minoritized":
        return [{
            "type": "aspiration_vs_origin",
            "intensity": 22.0,
            "latent_pressure": 15.0,
            "active": True,
            "origin_year": max(year - age, year - age + 10),
        }]
    return []


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def seed_frameworks_from_identity(
    identity: dict[str, Any] | Any,
    year: int,
    age: int,
) -> list[Any]:
    """
    Build initial Framework objects from identity signals.
    Returns a list of Framework instances (from v3.core.state).
    Safe to call before any yearly steps.
    """
    try:
        from v3.core.state import Framework
    except ImportError:
        return []

    religion = str(_get(identity, "religion") or _get(identity, "current_religion") or "").strip()
    religiosity = float(_get(identity, "religiosity_level") or 50.0)
    ses = str(_get(identity, "ses_band") or _get(identity, "class_origin") or "middle")
    minority = str(_get(identity, "minority_status") or "dominant")

    raw_frameworks: list[dict] = []
    raw_frameworks += _faith_framework(religiosity, religion, age)
    raw_frameworks += _class_framework(ses, age)
    raw_frameworks += _identity_search_framework(age)
    raw_frameworks += _minority_framework(minority, age)

    result = []
    for f in raw_frameworks:
        try:
            fw = Framework(
                id=f["id"],
                weight=float(f.get("weight", 50.0)),
                acute_delta=f.get("acute_delta") or {},
                chronic_delta=f.get("chronic_delta") or {},
                half_life_years=int(f.get("half_life_years", 15)),
                failure_mode=f.get("failure_mode", ""),
                enemy_requirement=float(f.get("enemy_requirement", 0.0)),
                institutional_affinities=list(f.get("institutional_affinities") or []),
                tenure_years=int(f.get("tenure_years", 0)),
            )
            result.append(fw)
        except Exception:
            continue
    return result


def seed_cracks_from_identity(
    identity: dict[str, Any] | Any,
    year: int,
    age: int,
) -> list[Any]:
    """
    Build initial Crack objects from identity signals.
    Returns a list of Crack instances (from v3.core.state).
    Safe to call before any yearly steps.
    """
    try:
        from v3.core.state import Crack
    except ImportError:
        return []

    religion = str(_get(identity, "religion") or _get(identity, "current_religion") or "").strip()
    religiosity = float(_get(identity, "religiosity_level") or 50.0)
    ses = str(_get(identity, "ses_band") or _get(identity, "class_origin") or "middle")
    minority = str(_get(identity, "minority_status") or "dominant")

    raw_cracks: list[dict] = []
    raw_cracks += _sacred_crack(religiosity, religion, year, age)
    raw_cracks += _family_stability_crack(ses, year, age)
    raw_cracks += _identity_coherence_crack(age, year)
    raw_cracks += _class_aspiration_crack(ses, minority, year, age)

    result = []
    for c in raw_cracks:
        try:
            crack = Crack(
                type=c["type"],
                intensity=float(c.get("intensity", 10.0)),
                latent_pressure=float(c.get("latent_pressure", 5.0)),
                active=bool(c.get("active", True)),
                origin_year=int(c.get("origin_year", year - age)),
            )
            result.append(crack)
        except Exception:
            continue

    # Cap active cracks at CRACKS_MAX_ACTIVE (3). All four recipes can fire simultaneously
    # (e.g. young + religious + working-class + minoritized). Deactivate lowest-intensity
    # active cracks past the limit; they remain in the list as latent.
    _MAX_ACTIVE = 3
    active_cracks = [c for c in result if getattr(c, "active", False)]
    if len(active_cracks) > _MAX_ACTIVE:
        active_cracks.sort(key=lambda c: getattr(c, "intensity", 0.0))
        for c in active_cracks[: len(active_cracks) - _MAX_ACTIVE]:
            c.active = False

    return result
