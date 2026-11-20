"""PYAT C6: real C5->PRE-V3/SEAM first-input bridge (SOURCEFREE ONLY).

The existing physical/I03/S04/DHIKR/FF01/C4/C5 pipeline owns all empirical
facts and sampling. C6 never recomputes a distribution, creates a respondent,
or manufactures the independent authority to admit a person, partner, world,
or psychological cause. It prepares bounded, replayable, source-coherent
entrance packets for the two actual Sorok historical entrances:
compressed adult backfill and a developing child's future contexts.

It *also* exercises the existing world-conditioned consumer's typed negative
path. This is a positive sourcefree interface and a negative actor/world
authority test, NOT a finished Sorok human.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import (
    ExactRef, canonical_json, canonicalize, semantic_hash,
)
from rawlsing_next.pre553_s04_field_forge_v3_bridge import (
    V3SeamEnvelope, V3SeamExternalPin,
)
from rawlsing_next.pre553_ff_prev3_possibility_navigation import (
    V3ContextPath, V3ContextNavigationError,
    plan_v3_sourcefree_context_branches,
    replay_v3_sourcefree_context_path,
)
from rawlsing_next.pre553_world_conditioned_progressive_service import (
    WorldConditionedPrefix,
)

CONTRACT = "PYAT_C6_SOURCEFREE_CONTEXTUAL_SEAM_ENTRANCE@1"
PAIR_CONTRACT = "PYAT_C6_TWO_INDEPENDENT_PARENT_ENTRANCES@1"
GRADE = "EXACT_SOURCEFREE_EMPIRICAL_POSSIBILITY__NOT_AN_ACTOR_OR_RELATIONSHIP"
ENTRY_PARENT = "PARENT_COMPRESSED_BACKFILL_INPUT"
ENTRY_NADIA = "NADIA_CONTINUING_DEVELOPMENTAL_CONTEXT_INPUT"
HELD_WORLD_STATE = "PYAT_SOURCEFREE_CANDIDATE_NOT_N10E_N10W_ISSUED"
UNISSUED = (
    "SOURCE_ORIGINAL_ANALYSIS_AND_DISCLOSURE",
    "PARTNER_SELECTION_OR_CO_RESIDENCE",
    "PERSON_OR_PSYCHOLOGICAL_STRUCTURE",
    "V3_SEAM_ACTOR_STATE_TRANSITION",
    "WORLD_CAUSAL_RELATION_OR_N10W",
    "POPULATION_INFERENCE_OR_SCIENTIFIC_DETERMINICITY",
    "SEAM_PARENTAL_OR_DEVELOPMENTAL_AUTHORITY",
)


class C6SeamError(ValueError):
    """Reject false source, historical-person, or world authority."""


def _seal(payload: dict[str, Any], cls):
    return cls(canonical_json(payload), semantic_hash(payload))


@dataclass(frozen=True)
class C6ContextualEntrance:
    payload_json: str
    content_hash: str

    def __post_init__(self) -> None:
        try:
            material = loads(self.payload_json)
            if (type(material) is not dict
                    or material.get("contract") != CONTRACT
                    or canonical_json(material) != self.payload_json
                    or semantic_hash(material) != self.content_hash
                    or material.get("grade") != GRADE
                    or material.get("not_issued") != list(UNISSUED)
                    or material.get("actor_state_transition") is not None):
                raise C6SeamError("C6 entrance must be exact and nonissuing")
        except (TypeError, ValueError) as exc:
            raise C6SeamError("invalid C6 entrance") from exc

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            CONTRACT,
            "urn:rawlsing:pyat:c6-entrance:sha256:" + self.content_hash,
            self.content_hash,
        )

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


@dataclass(frozen=True)
class C6IndependentParents:
    payload_json: str
    content_hash: str

    def __post_init__(self) -> None:
        try:
            m = loads(self.payload_json)
            if (type(m) is not dict or m.get("contract") != PAIR_CONTRACT
                    or canonical_json(m) != self.payload_json
                    or semantic_hash(m) != self.content_hash
                    or m.get("partner_selection_evidence") is not None
                    or m.get("inferred_parental_relationship") is not None
                    or m.get("actor_state_transition") is not None
                    or m.get("not_issued") != list(UNISSUED)):
                raise C6SeamError("pair cannot create partner-selection evidence")
        except (TypeError, ValueError) as exc:
            raise C6SeamError("invalid C6 independent parent packet") from exc

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            PAIR_CONTRACT,
            "urn:rawlsing:pyat:c6-two-parents:sha256:" + self.content_hash,
            self.content_hash,
        )

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


def assemble_c6_contextual_entrance(
    *,
    envelope: V3SeamEnvelope,
    external_pin: V3SeamExternalPin,
    path: V3ContextPath,
    entrance: str,
    slot: str,
    min_disclosure_cell_n: int = 2,
) -> C6ContextualEntrance:
    """Actual C5 replay -> conditioned C6 research packet, one source only.

    The minimum applies to disclosure of a *whole* joint cell, not merely
    the condition denominator. An XOR fixture has four respondents but
    singleton complete cells; it yields a real contextual research packet
    with its sampled configuration withheld.
    """
    if entrance not in (ENTRY_PARENT, ENTRY_NADIA):
        raise C6SeamError("unissued historical entrance kind")
    if type(slot) is not str or not slot.strip() or len(slot) > 96:
        raise C6SeamError("bounded scenario slot required, not actor identity")
    if (type(min_disclosure_cell_n) is not int
            or not 2 <= min_disclosure_cell_n <= 1000):
        raise C6SeamError("private cell support minimum must be integer >=2")
    if type(envelope) is not V3SeamEnvelope or type(external_pin) is not V3SeamExternalPin:
        raise C6SeamError("independently pinned C4 source required")
    if type(path) is not V3ContextPath:
        raise C6SeamError("actual C5 path required")
    # A valid content hash is insufficient: an attacker could self-rehash
    # a fabricated path. Recompute using separately held upstream roots.
    replay_v3_sourcefree_context_path(
        path=path, envelope=envelope, external_pin=external_pin,
    )
    p = path.material()
    context = {item["axis"]: item["exact_state"] for item in p["final_context"]}
    current = plan_v3_sourcefree_context_branches(
        envelope=envelope, external_pin=external_pin,
        conditions=context,
        min_context_n=p["min_context_n"],
    )
    c = current.material()
    if (c["source_handoff_ref"] != envelope.ref.as_dict()
            or c["state"] != p["status"].replace(
                "SOURCE_COHERENT_EXPLORATORY_CASE_OFFER",
                "CONTEXT_ELIGIBLE_FOR_SOURCEFREE_CASE_OFFER"
            ).replace(
                "LOW_CONTEXT_SUPPORT__ABSTAIN",
                "LOW_COMPLETE_CASE_N__NO_CANDIDATE_OFFER"
            ).replace(
                "ZERO_OBSERVED_CONTEXT__NOT_IMPOSSIBILITY",
                "OBSERVED_ZERO_IN_COMPLETE_CASE__NOT_IMPOSSIBLE"
            ).replace(
                "PRODUCER_TYPED_HELD__NO_CASE_OFFER",
                "UPSTREAM_TYPED_HELD__NO_INFERRED_ZERO"
            )):
        raise C6SeamError("C5/C6 conditioned source grade changed")
    o = p["final_case_offer_payload"]
    if o["source_handoff_ref"] != envelope.ref.as_dict():
        raise C6SeamError("C5 selected case source changed")
    cell_n = o["selected_cell_support_raw"]
    admit_cell = (
        p["status"] == "SOURCE_COHERENT_EXPLORATORY_CASE_OFFER"
        and type(cell_n) is int and cell_n >= min_disclosure_cell_n
    )
    if p["status"] != "SOURCE_COHERENT_EXPLORATORY_CASE_OFFER" and o["selected_complete_joint_cell"]:
        raise C6SeamError("held context contains disclosed whole case")
    if admit_cell and not o["selected_complete_joint_cell"]:
        raise C6SeamError("admissible source cell missing source dimensions")

    # This is a guarded scenario feature packet; no personal state, hidden
    # respondent identity, raw low-N cells, or relationship probabilities.
    # C4/C5 remain in independent restricted sourcefree custody for audit.
    branches = []
    for axis in c["source_observed_axes"]:
        options = []
        for b in axis["branches"]:
            n = b["raw_complete_case_n"]
            options.append({
                "source_state": b["exact_state"],
                "source_status": b["status"],
                "qualified_raw_n": n if type(n) is int and n >= min_disclosure_cell_n else None,
                "below_disclosure_threshold": type(n) is int and n < min_disclosure_cell_n,
                "population_probability": None,
                "person_trait_or_motive": None,
            })
        branches.append({
            "source_axis": axis["axis"],
            "source_target_ref": axis["target_ref"],
            "options": options,
        })
    payload = {
        "contract": CONTRACT,
        "grade": GRADE,
        "entrance": entrance,
        "scenario_slot_not_actor_id": slot.strip(),
        "source_c4_handoff_ref": envelope.ref.as_dict(),
        "source_c5_path_ref": path.ref.as_dict(),
        "source_case_offer_ref": p["final_case_offer_ref"],
        "source_context_plan_ref": current.ref.as_dict(),
        "source_ff01_ref": p["source_ff01_ref"],
        "source_dhikr_ref": p["source_dhikr_ref"],
        "source_states_conditioning": p["final_context"],
        "conditioned_sample_status": p["status"],
        "conditioned_raw_n_if_disclosable": (
            p["final_raw_complete_case_n"]
            if type(p["final_raw_complete_case_n"]) is int
            and p["final_raw_complete_case_n"] >= min_disclosure_cell_n
            else None
        ),
        "whole_case_state": (
            "SOURCEFREE_CELL_PROPOSAL_ONLY__NO_PERSON"
            if admit_cell else
            "WHOLE_CELL_WITHHELD_OR_NO_SUPPORTED_CONTEXT"
        ),
        "hypothetical_joint_configuration": (
            o["selected_complete_joint_cell"] if admit_cell else []
        ),
        "original_selected_cell_n_if_disclosable": cell_n if admit_cell else None,
        "source_observed_future_branches": branches,
        "min_disclosure_cell_n": min_disclosure_cell_n,
        "no_additional_i03_queries": True,
        "no_independent_marginal_sampling": True,
        "no_partner_coupling_inference": True,
        "original_data_usable": False,
        "world_or_actor_issuer": None,
        "actor_state_transition": None,
        "not_issued": list(UNISSUED),
    }
    return _seal(payload, C6ContextualEntrance)


def replay_c6_contextual_entrance(
    *,
    receipt: C6ContextualEntrance,
    envelope: V3SeamEnvelope,
    external_pin: V3SeamExternalPin,
    path: V3ContextPath,
) -> C6ContextualEntrance:
    """Authoritative recomputation is upstream-root-bound; hash alone fails."""
    if type(receipt) is not C6ContextualEntrance:
        raise C6SeamError("exact typed C6 receipt required")
    m = receipt.material()
    rebuilt = assemble_c6_contextual_entrance(
        envelope=envelope, external_pin=external_pin, path=path,
        entrance=m["entrance"], slot=m["scenario_slot_not_actor_id"],
        min_disclosure_cell_n=m["min_disclosure_cell_n"],
    )
    if rebuilt.ref != receipt.ref:
        raise C6SeamError("C6 cold source replay failed")
    return rebuilt


def assemble_two_sourcefree_parent_entrances(
    *,
    first: C6ContextualEntrance,
    second: C6ContextualEntrance,
    first_source: tuple[V3SeamEnvelope, V3SeamExternalPin, V3ContextPath],
    second_source: tuple[V3SeamEnvelope, V3SeamExternalPin, V3ContextPath],
    partner_selection_claim: Any = None,
) -> C6IndependentParents:
    """Two on-demand hypotheses, NEVER a simulated survey partner relation.

    Respondent-level within-person co-travel does not measure pair selection.
    Independently supplied partner-selection evidence must be separately
    owned and integrated by SEAM; this interface cannot admit it.
    """
    if partner_selection_claim is not None:
        raise C6SeamError("PARTNER_SELECTION_NOT_ESTABLISHED_BY_WITHIN_PERSON_SURVEY")
    if type(first) is not C6ContextualEntrance or type(second) is not C6ContextualEntrance:
        raise C6SeamError("two independently issued C6 proposal packets required")
    a = first.material()
    b = second.material()
    if a["entrance"] != ENTRY_PARENT or b["entrance"] != ENTRY_PARENT:
        raise C6SeamError("parent pair input requires two adult backfill entrances")
    if a["scenario_slot_not_actor_id"] == b["scenario_slot_not_actor_id"]:
        raise C6SeamError("independent parent scenario slots must differ")
    if len(first_source) != 3 or len(second_source) != 3:
        raise C6SeamError("both independent source triplets required")
    replay_c6_contextual_entrance(
        receipt=first, envelope=first_source[0], external_pin=first_source[1],
        path=first_source[2],
    )
    replay_c6_contextual_entrance(
        receipt=second, envelope=second_source[0], external_pin=second_source[1],
        path=second_source[2],
    )
    return _seal({
        "contract": PAIR_CONTRACT,
        "grade": GRADE,
        "first_parent_proposal_ref": first.ref.as_dict(),
        "second_parent_proposal_ref": second.ref.as_dict(),
        "first_source_ref": a["source_c4_handoff_ref"],
        "second_source_ref": b["source_c4_handoff_ref"],
        "first_scenario_slot": a["scenario_slot_not_actor_id"],
        "second_scenario_slot": b["scenario_slot_not_actor_id"],
        "partner_selection_evidence": None,
        "inferred_parental_relationship": None,
        "pairing_state": "TWO_INDEPENDENT_PERSON_HYPOTHESES__RELATIONSHIP_UNISSUED",
        "no_fabricated_cross_person_correlation": True,
        "actor_state_transition": None,
        "not_issued": list(UNISSUED),
    }, C6IndependentParents)


def as_nonissuing_world_conditioned_prefix(
    receipt: C6ContextualEntrance,
) -> WorldConditionedPrefix:
    """Real existing R112 first consumer receives a typed NONPOSITIVE step.

    Never falsify an N10E EXACT_SUPPORTED slice to activate a world/actor
    relation. A later competent owner may independently issue that slice.
    """
    if type(receipt) is not C6ContextualEntrance:
        raise C6SeamError("typed C6 entrance required for world first consumer")
    m = receipt.material()
    return WorldConditionedPrefix(
        prefix_id="PYAT_C6_" + receipt.content_hash[:24],
        target="SOURCE_MEASUREMENT_NOT_A_PERSON",
        conditioners=tuple(
            ("source_axis_" + str(x["axis"]), canonicalize(x["exact_state"]))
            for x in m["source_states_conditioning"]
        ),
        step={
            "state": HELD_WORLD_STATE,
            "content_hash": receipt.content_hash,
            "evidence_ref": receipt.ref.as_dict(),
            "denominator": None,
            "cells": [],
            "source_c4_handoff_ref": m["source_c4_handoff_ref"],
            "not_issued": list(UNISSUED),
        },
    )


__all__ = [
    "CONTRACT", "PAIR_CONTRACT", "GRADE", "ENTRY_PARENT", "ENTRY_NADIA",
    "HELD_WORLD_STATE", "UNISSUED", "C6SeamError", "C6ContextualEntrance",
    "C6IndependentParents", "assemble_c6_contextual_entrance",
    "replay_c6_contextual_entrance", "assemble_two_sourcefree_parent_entrances",
    "as_nonissuing_world_conditioned_prefix",
]
