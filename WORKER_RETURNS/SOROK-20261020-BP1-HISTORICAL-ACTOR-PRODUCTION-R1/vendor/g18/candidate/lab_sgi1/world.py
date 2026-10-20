"""Synthetic world fixture: institutions, routes, opportunities, synthetic possibility base.

PROVISIONAL_LAB_RULE__NOT_ADOPTED. Source-free: no survey originals, no real persons.
The generic possibility layer answers only within this synthetic world's declared
universe and always returns a use ceiling label.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .core import h_obj, typed, S

WORLD_PREMISE_VERSION = "SYNTH_WORLD@1.0.0"


@dataclass(frozen=True)
class Institution:
    inst_id: str
    kind: str  # WORKPLACE | EVENING_CLASS | MARKET | COMMUNITY_GROUP | TRANSIT_HUB | FRIEND_NETWORK
    name: str
    location_id: str
    open_hours: str
    membership_rule: str


@dataclass(frozen=True)
class Route:
    route_id: str
    route_kind: str  # LOCAL_CLOSED | INSTITUTIONAL | MOBILITY | UNCONVENTIONAL
    via_institution: str
    requires_mobility: bool
    reachable_from_mother: bool
    lawful_for_mother: bool
    premise_note: str


@dataclass(frozen=True)
class WorldSnapshot:
    world_id: str
    premise_version: str
    calendar: str
    institutions: List[Institution]
    routes: List[Route]
    synthetic_possibility_base: Dict[str, Any]
    joint_bridge_available: bool
    coverage_note: str

    def ref(self) -> str:
        return h_obj(
            {
                "world_id": self.world_id,
                "premise_version": self.premise_version,
                "institutions": [i.__dict__ for i in self.institutions],
                "routes": [r.__dict__ for r in self.routes],
                "synthetic_possibility_base": self.synthetic_possibility_base,
                "joint_bridge_available": self.joint_bridge_available,
            }
        )


def build_world(mother_mobility_history: bool) -> WorldSnapshot:
    """World premise is fixed; only route reachability facts vary with lawful mother facts.

    The MOBILITY route is present in the world either way; whether it is *reachable*
    is decided against the mother checkpoint (no backdating of her history).
    """
    institutions = [
        Institution("INST_WORKSHOP_A", "WORKPLACE", "Riverside Fabrication Workshop", "LOC_RIVERSIDE", "day", "employment"),
        Institution("INST_EVENING_CLASS_B", "EVENING_CLASS", "Municipal Evening Technical Class", "LOC_CENTER", "evening", "enrollment"),
        Institution("INST_MARKET_C", "MARKET", "Old Quarter Market", "LOC_OLDQUARTER", "day", "open"),
        Institution("INST_COMMUNITY_D", "COMMUNITY_GROUP", "Neighborhood Water Committee", "LOC_RIVERSIDE", "evening", "residency"),
        Institution("INST_TRANSIT_E", "TRANSIT_HUB", "Regional Bus Interchange", "LOC_INTERCHANGE", "all", "ticket"),
        Institution("INST_FRIEND_NET_F", "FRIEND_NETWORK", "Two mutual-friend network", "LOC_VARIOUS", "social", "introduction"),
    ]
    routes = [
        Route("ROUTE_LOCAL_CLOSED", "LOCAL_CLOSED", "INST_WORKSHOP_A", False, True, True,
              "closed local contact route through workplace adjacency"),
        Route("ROUTE_INSTITUTIONAL", "INSTITUTIONAL", "INST_EVENING_CLASS_B", False, True, True,
              "lawful local contact route through evening class enrollment"),
        Route("ROUTE_MOBILITY", "MOBILITY", "INST_TRANSIT_E", True, mother_mobility_history, True,
              "route expansion via regional interchange; reachable only if checkpoint "
              "contains past mobility or a lawfully reachable opportunity"),
        Route("ROUTE_UNCONVENTIONAL", "UNCONVENTIONAL", "INST_COMMUNITY_D", False, True, True,
              "unconventional encounter via water-committee emergency repair meeting; "
              "admitted mother route and world permit it; no typicality mandate"),
    ]
    # Synthetic single-person marginals only. Joint two-person encounter propensity
    # is NOT in this base: no dyad law, no population coupling.
    possibility = {
        "universe": "SYNTHETIC_LAB_WORLD_ONLY",
        "single_person_marginals": {
            "evening_class_enrollment_rate": 0.18,
            "committee_participation_rate": 0.09,
            "regional_transit_use_rate": 0.22,
            "workplace_adjacency_contact_rate": 0.31,
        },
        "joint_two_person_encounter_propensity": None,
        "denominator_note": "single-person marginals only; joint dyad law NOT_ESTIMABLE in this synthetic base",
        "design": "synthetic_labeled_fixture_not_population_estimate",
    }
    return WorldSnapshot(
        world_id="WORLD_SYNTHTIC_LAB_001",
        premise_version=WORLD_PREMISE_VERSION,
        calendar="LAB_CAL_DAY",
        institutions=institutions,
        routes=routes,
        synthetic_possibility_base=possibility,
        joint_bridge_available=False,
        coverage_note="source-free synthetic world; generic queries answer inside this universe only",
    )


def generic_possibility_query(world: WorldSnapshot, request: Dict[str, Any]) -> Dict[str, Any]:
    """Generic PRE-V3 positioned possibility envelope (source-free synthetic implementation).

    Never returns a generated person fact. Joint/dyad requests have no bridge in this
    world -> NOT_ESTIMABLE with ceiling label, never zero plausibility.
    """
    joint = request.get("joint_topology") == "MULTI_UNIT_WITH_QUALIFIED_BRIDGE"
    unit = request.get("subject_universe_and_observation_unit")
    key = request.get("target_variable")
    base = world.synthetic_possibility_base
    if joint or not world.joint_bridge_available and request.get("requires_joint") :
        return typed(
            S.GENERIC_QUERY_NONCOMPARABLE
            if joint and not world.joint_bridge_available
            else "NOT_ESTIMABLE",
            request_hash=h_obj(request),
            result_state="NOT_ESTIMABLE",
            reason="no qualified joint/dyad bridge in synthetic world base",
            empirical_use_ceiling="SYNTHETIC_SINGLE_PERSON_MARGINAL_ONLY",
            no_generated_person_fact=True,
            source_release="SYNTHETIC_LAB_WORLD@1.0.0",
            observation_unit=unit,
        )
    marginals = base.get("single_person_marginals", {})
    if key in marginals:
        return typed(
            "SUPPORTED",
            request_hash=h_obj(request),
            result_state="SUPPORTED",
            native_value=marginals[key],
            native_unit="synthetic_rate_within_declared_universe",
            empirical_use_ceiling="SYNTHETIC_LAB_WORLD_ONLY__NOT_POPULATION_ESTIMATE",
            no_generated_person_fact=True,
            source_release="SYNTHETIC_LAB_WORLD@1.0.0",
            observation_unit=unit,
            uncertainty="synthetic_fixture_no_interval_claim",
        )
    return typed(
        "UNKNOWN",
        request_hash=h_obj(request),
        result_state="UNKNOWN",
        reason="target variable outside synthetic base coverage",
        empirical_use_ceiling="SYNTHETIC_LAB_WORLD_ONLY__NOT_POPULATION_ESTIMATE",
        no_generated_person_fact=True,
        source_release="SYNTHETIC_LAB_WORLD@1.0.0",
    )
