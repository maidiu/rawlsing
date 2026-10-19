"""Source-free whole-person mother checkpoint fixtures (M0, MP, M2).

PROVISIONAL_LAB_RULE__NOT_ADOPTED. Synthetic generated actor fixtures only.
Mothers are built as forward causal event histories, then checkpointed at
t_preconception. Every psyche fact carries its causal event ancestry — no
demographic->psyche direct mutation exists in this builder.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .core import h_obj, h_concat, typed, S, Ledger

EMBARGOED_PARTITION_MANIFEST = [
    "future_child_outcome_label",
    "future_child_personality",
    "future_child_desired_adversity_tag",
    "future_child_health_outcome",
    "future_child_education_outcome",
    "any_field_derived_from_future_child",
]


@dataclass
class LabEvent:
    event_id: str
    effective_index: int  # governed effective order (chronological)
    kind: str
    actors: List[str]
    payload: Dict[str, Any]
    causal_parent_event_ids: List[str]

    def as_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)


def _evt(seq: int, kind: str, actors: List[str], payload: Dict[str, Any],
         parents: List[str]) -> LabEvent:
    eid = h_concat("EVT", str(seq), kind, ",".join(actors), h_obj(payload))
    return LabEvent(eid, seq, kind, actors, payload, parents)


def _build_history(actor_id: str, variant: str) -> List[LabEvent]:
    """Deterministic forward causal history. variant selects lawful content."""
    evs: List[LabEvent] = []
    a = actor_id

    def add(kind, payload, parents):
        e = _evt(len(evs), kind, [a] + payload.get("other_actors", []), payload, parents)
        evs.append(e)
        return e

    # Roots (sparse, explicit unknowns permitted)
    e_root = add("ORIGIN_FAMILY", {
        "region": "RIVERSIDE_DISTRICT",
        "household_occupation": "mixed_fabrication_and_market_trade",
        "known_siblings": 2,
        "root_status": "LAB_ROOT_ADMITTED",
    }, [])
    e_school = add("SCHOOLING", {
        "level": "secondary_complete_plus_one_year_vocational",
        "site": "MUNICIPAL_VOCATIONAL_ANNEX",
    }, [e_root.event_id])
    e_firstjob = add("WORK_POSITION", {
        "workplace": "RIVERSIDE_FABRICATION_WORKSHOP",
        "role": "junior_finisher",
        "material_position": "waged_artisan",
    }, [e_school.event_id])
    e_practice_form = add("PRACTICE_FORMATION", {
        "practice": "measure_twice_cut_once_workshop_discipline",
        "causal_basis": "repeated supervised finishing work with rework costs",
    }, [e_firstjob.event_id])
    e_att_form = add("ATTITUDE_FORMATION", {
        "attitude": "self_reliance_under_deadline",
        "causal_basis": "piece_rate pressure and rework experience",
    }, [e_firstjob.event_id, e_practice_form.event_id])
    e_project_apprentice = add("PROJECT", {
        "project": "mentor_two_apprentices_through_journeyman_exam",
        "third_party": ["APPRENTICE_ONE", "APPRENTICE_TWO"],
        "duration_index_span": [40, 88],
        "consequential": True,
        "nonmother": True,
    }, [e_firstjob.event_id, e_practice_form.event_id])
    e_rel_sibling = add("NONMOTHER_RELATIONSHIP", {
        "counterpart": "SIBLING_R",
        "relation_kind": "sibling_care_obligation",
        "consequential": True,
        "nonmother": True,
    }, [e_root.event_id])
    e_mem1 = add("MEMORY_TRACE", {
        "trace": "remembered_rework_loss_from_measurement_error",
        "experienced_basis_event": e_firstjob.event_id,
    }, [e_firstjob.event_id])
    e_mem2 = add("MEMORY_TRACE", {
        "trace": "remembered_apprentice_exam_failure_then_recovery",
        "experienced_basis_event": e_project_apprentice.event_id,
    }, [e_project_apprentice.event_id])
    e_striving = add("STRIVING", {
        "striving": "complete_evening_technical_certificate",
        "causal_basis": "blocked promotion without certificate",
    }, [e_firstjob.event_id, e_att_form.event_id])
    e_enroll = add("ENROLLMENT", {
        "institution": "MUNICIPAL_EVENING_TECHNICAL_CLASS",
        "course": "structural_mechanics_ii",
    }, [e_striving.event_id])
    e_workpos2 = add("WORK_POSITION", {
        "workplace": "RIVERSIDE_FABRICATION_WORKSHOP",
        "role": "finisher_specialist",
        "material_position": "waged_artisan_senior",
    }, [e_firstjob.event_id, e_project_apprentice.event_id])
    e_household = add("HOUSEHOLD_STATE", {
        "residence": "RIVERSIDE_RENTED_ROOM_SHARED_KITCHEN",
        "membership": [a],
    }, [e_workpos2.event_id])

    if variant == "M2":
        e_prior_rel = add("RELATIONSHIP_ADMISSION", {
            "counterpart": "PRIOR_PARTNER_P",
            "relation_kind": "partner_relationship",
            "objective_relation": True,
        }, [e_workpos2.event_id])
        e_older_child = add("CHILD_GENERATED", {
            "child_actor": "LAB_OLDER_CHILD_O1",
            "generation_boundary": "PRIOR_ADMITTED_GENERATION",
            "note": "prior admitted child; stable actor stream",
        }, [e_prior_rel.event_id])
        e_prior_split = add("RELATIONSHIP_CHANGE", {
            "counterpart": "PRIOR_PARTNER_P",
            "change": "separation",
        }, [e_older_child.event_id])
        e_household = add("HOUSEHOLD_STATE", {
            "residence": "RIVERSIDE_RENTED_FLAT_TWO_ROOM",
            "membership": [a, "LAB_OLDER_CHILD_O1"],
        }, [e_older_child.event_id, e_prior_split.event_id])
        e_olderchild_care = add("CARE_ROUTINE", {
            "subject": "LAB_OLDER_CHILD_O1",
            "routine": "school_run_and_evening_supervision",
        }, [e_older_child.event_id])
    elif variant == "MP":
        e_existing = add("NONMOTHER_RELATIONSHIP", {
            "counterpart": "F_EXISTING",
            "relation_kind": "acknowledged_partner",
            "objective_relation": True,
            "identity_evidence": "mutual_household_registration_and_witnessed_introduction",
            "known_counterpart_identity": True,
        }, [e_workpos2.event_id])
        e_shared_event = add("SHARED_ENCOUNTER", {
            "counterpart": "F_EXISTING",
            "witnesses": ["W1", "W2"],
            "place": "WATER_COMMITTEE_MEETING",
            "note": "existing admitted shared event E_pre",
        }, [e_existing.event_id])
        e_relstate = add("RELATIONSHIP_STATE", {
            "counterpart": "F_EXISTING",
            "state": "ongoing_partner_relationship",
        }, [e_shared_event.event_id])

    e_route_local = add("ROUTE_AVAILABILITY", {
        "route": "ROUTE_LOCAL_CLOSED",
        "via": "INST_WORKSHOP_A",
        "basis": "employment adjacency",
    }, [e_workpos2.event_id])
    e_route_inst = add("ROUTE_AVAILABILITY", {
        "route": "ROUTE_INSTITUTIONAL",
        "via": "INST_EVENING_CLASS_B",
        "basis": "evening enrollment",
    }, [e_enroll.event_id])
    e_route_unconv = add("ROUTE_AVAILABILITY", {
        "route": "ROUTE_UNCONVENTIONAL",
        "via": "INST_COMMUNITY_D",
        "basis": "residency in riverside district water committee catchment",
    }, [e_household.event_id])

    if variant == "M0":
        # M0 has NO admitted mobility history. A prospective reachable opportunity
        # IS part of the immutable checkpoint: the regional interchange one-day
        # commission she is lawfully invited to. This permits ROUTE_MOBILITY
        # expansion WITHOUT backdating any past mobility into her history.
        e_prosp = add("PROSPECTIVE_OPPORTUNITY", {
            "opportunity": "REGIONAL_INTERCHANGE_ONE_DAY_COMMISSION_OPEN_TO_HER",
            "route_basis": "ROUTE_MOBILITY",
            "lawful_reachable": True,
            "is_past_mobility": False,
            "note": "prospective reachable opportunity in immutable checkpoint; "
                    "not a mobility history fact",
        }, [e_workpos2.event_id])
    elif variant in ("MP", "M2"):
        e_mob = add("MOBILITY_HISTORY", {
            "kind": "seasonal_relocation_for_commissioned_work",
            "detail": "one 3-month commissioned installation at regional interchange town",
            "route_basis": "ROUTE_MOBILITY",
        }, [e_workpos2.event_id])

    e_neg = add("NEGATIVE_OR_UNKNOWN_FACTS", {
        "unknowns": ["no admitted prior encounter with unknown counterpart",
                     "no admitted family wealth"],
    }, [e_household.event_id])
    return evs


def _psyche_from_events(evs: List[LabEvent]) -> Dict[str, Any]:
    """Derive psyche fields strictly from event ancestry (no demographic mutation)."""
    attitudes, practices, strivings = [], [], []
    for e in evs:
        if e.kind == "ATTITUDE_FORMATION":
            attitudes.append({
                "attitude": e.payload["attitude"],
                "causal_event_refs": [e.event_id] + e.causal_parent_event_ids,
            })
        elif e.kind == "PRACTICE_FORMATION":
            practices.append({
                "practice": e.payload["practice"],
                "causal_event_refs": [e.event_id] + e.causal_parent_event_ids,
            })
        elif e.kind == "STRIVING":
            strivings.append({
                "striving": e.payload["striving"],
                "causal_event_refs": [e.event_id] + e.causal_parent_event_ids,
            })
    return {"attitudes": attitudes, "practices": practices, "strivings": strivings}


@dataclass
class MotherCheckpoint:
    fixture_id: str
    actor_id: str
    variant: str
    events: List[LabEvent]
    psyche: Dict[str, Any]
    t_preconception: str
    known_counterpart_identity_ref_or_null: Optional[str]
    already_generated_child_refs: List[str]
    admitted_partner_relationship_refs: List[str]
    route_availability: List[str]
    mobility_history_present: bool
    prospective_opportunity_refs: List[Dict[str, Any]]
    prohibited_future_input_hash: str
    history_prefix_commit_hash: str

    def anchor_dict(self) -> Dict[str, Any]:
        return {
            "anchor_id": "ANCHOR_" + self.fixture_id,
            "fixture_id": self.fixture_id,
            "actor_id": self.actor_id,
            "variant": self.variant,
            "t_preconception": self.t_preconception,
            "read_cut": "BEFORE_TARGET_OCCURRENCE",
            "history_events": [e.as_dict() for e in self.events],
            "psyche": self.psyche,
            "known_counterpart_identity_ref_or_null": self.known_counterpart_identity_ref_or_null,
            "already_generated_child_refs": self.already_generated_child_refs,
            "admitted_partner_relationship_refs": self.admitted_partner_relationship_refs,
            "route_availability": self.route_availability,
            "mobility_history_present": self.mobility_history_present,
            "prospective_opportunity_refs": self.prospective_opportunity_refs,
            "prohibited_future_input_hash": self.prohibited_future_input_hash,
            "history_prefix_commit_hash": self.history_prefix_commit_hash,
            "schema": "MotherPreconceptionAnchor@1-LAB",
            "lab_rule": "PROVISIONAL_LAB_RULE__NOT_ADOPTED",
        }

    def hash(self) -> str:
        return h_obj(self.anchor_dict())


def build_mother_checkpoint(fixture_id: str, variant: str) -> MotherCheckpoint:
    actor_id = f"LAB_MOTHER_{variant}"
    evs = _build_history(actor_id, variant)
    psyche = _psyche_from_events(evs)

    known_counterpart = None
    children: List[str] = []
    partners: List[str] = []
    if variant == "MP":
        known_counterpart = "F_EXISTING"
        partners = ["REL_ADMITTED_F_EXISTING"]
    elif variant == "M2":
        children = ["LAB_OLDER_CHILD_O1"]

    mobility = any(e.kind == "MOBILITY_HISTORY" for e in evs)
    prospective = [e.payload for e in evs if e.kind == "PROSPECTIVE_OPPORTUNITY"]
    routes = set(e.payload["route"] for e in evs if e.kind == "ROUTE_AVAILABILITY")
    for e in evs:
        if e.kind in ("PROSPECTIVE_OPPORTUNITY", "MOBILITY_HISTORY"):
            rb = e.payload.get("route_basis")
            if rb:
                routes.add(rb)
    routes_sorted = sorted(x for x in routes if x)
    prefix_hash = h_obj([e.as_dict() for e in evs])
    embargo_manifest_hash = h_obj(EMBARGOED_PARTITION_MANIFEST)

    return MotherCheckpoint(
        fixture_id=fixture_id,
        actor_id=actor_id,
        variant=variant,
        events=evs,
        psyche=psyche,
        t_preconception="T_PRECONCEPTION_LAB_BOUNDARY",
        known_counterpart_identity_ref_or_null=known_counterpart,
        already_generated_child_refs=children,
        admitted_partner_relationship_refs=partners,
        route_availability=routes_sorted,
        mobility_history_present=mobility,
        prospective_opportunity_refs=prospective,
        prohibited_future_input_hash=embargo_manifest_hash,
        history_prefix_commit_hash=prefix_hash,
    )


def validate_no_demographic_psyche(cp: MotherCheckpoint) -> Dict[str, Any]:
    """Every psyche fact must reference causal events; otherwise INTEGRITY_FAILURE."""
    violations = []
    for domain in ("attitudes", "practices", "strivings"):
        for item in cp.psyche.get(domain, []):
            if not item.get("causal_event_refs"):
                violations.append({"domain": domain, "item": item})
    return typed(
        S.INTEGRITY_FAILURE if violations else S.LAB_PASS,
        violations=violations,
        checked_domains=["attitudes", "practices", "strivings"],
    )
