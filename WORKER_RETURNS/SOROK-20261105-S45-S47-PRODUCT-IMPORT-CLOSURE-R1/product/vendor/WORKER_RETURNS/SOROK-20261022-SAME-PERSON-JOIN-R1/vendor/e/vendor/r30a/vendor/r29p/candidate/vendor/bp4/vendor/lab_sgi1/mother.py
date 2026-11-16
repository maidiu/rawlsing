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
    owner_id: Optional[str] = None
    source_grade: str = "SOURCEFREE_RESEARCH_INPUT"

    def as_dict(self) -> Dict[str, Any]:
        return dict(self.__dict__)


def _evt(seq: int, kind: str, actors: List[str], payload: Dict[str, Any],
         parents: List[str]) -> LabEvent:
    eid = h_concat("EVT", str(seq), kind, ",".join(actors), h_obj(payload))
    return LabEvent(eid, seq, kind, actors, payload, parents)


def _build_history(actor_id: str, variant: str) -> List[LabEvent]:
    from .history import PersonHistoryBuilder
    # The maternal project is finishing/apprentice work, not a kin stereotype.
    events=PersonHistoryBuilder(actor_id,'MATERNAL_'+variant,role='finishing').build()
    return [LabEvent(**e) for e in events]


def _psyche_from_events(evs):
    from .history import derive_psyche
    return derive_psyche([e.as_dict() for e in evs])


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
        if hasattr(self,'archived_anchor'):
            from copy import deepcopy
            return deepcopy(self.archived_anchor)
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
            "older_child_source_grade": "FROZEN_M2_PRIOR_FIXTURE_REFERENCE_ONLY_NOT_NEW_CREATION",
            "lab_rule": "PROVISIONAL_LAB_RULE__NOT_ADOPTED",
        }

    def hash(self) -> str:
        return h_obj(self.anchor_dict())


def build_mother_checkpoint(fixture_id: str, variant: str) -> MotherCheckpoint:
    if variant in {'M2','MP'}:
        import json
        from pathlib import Path
        from copy import deepcopy
        packet=json.loads((Path(__file__).resolve().parents[1]/'data/frozen_maternal_archives.json').read_text())
        a=packet['archives'][variant]
        assert h_obj(a)==packet['expected_anchor_hashes'][variant]
        cp=MotherCheckpoint(fixture_id, a['actor_id'],variant,[LabEvent(**e) for e in a['history_events']],
            deepcopy(a['psyche']),a['t_preconception'],a['known_counterpart_identity_ref_or_null'],
            a['already_generated_child_refs'],a['admitted_partner_relationship_refs'],a['route_availability'],
            a['mobility_history_present'],a['prospective_opportunity_refs'],a['prohibited_future_input_hash'],a['history_prefix_commit_hash'])
        cp.archived_anchor=deepcopy(a)
        cp.archived_anchor['fixture_id']=fixture_id;cp.archived_anchor['anchor_id']='ANCHOR_'+fixture_id
        return cp
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
    from .history import validate_psyche
    errors=validate_psyche([e.as_dict() for e in cp.events],cp.psyche)
    return typed(S.INTEGRITY_FAILURE if errors else S.LAB_PASS,violations=errors,checked_domains=['attitudes','practices','strivings'])
