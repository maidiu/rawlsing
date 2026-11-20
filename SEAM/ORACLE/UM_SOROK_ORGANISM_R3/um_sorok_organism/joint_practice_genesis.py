"""SORACLE P006/P015 — historically developed conditional joint practice.

A child may learn a way of coordinating an operation with a particular
person after an unfinished personal attempt and a distinct independently
reciprocated joint attempt. This is a practiced relation, NOT an inherent
property of the pair, automatic affection, unconditional consent, or proof
of durable objective joint mastery. Its first consumer is the EXISTING
conditional-invitation machinery in distributed_power.
"""
from .types import copy, stable_id, GRADE


def possible_joint_practice(actor,experience,event_ref):
    if experience.get("actor")!=actor.get("id"):
        return []
    history=actor.get("participation_history",[])
    current=[h for h in history
             if h.get("event_ref")==event_ref
             and h.get("experience_ref")==experience.get("ref")]
    if len(current)!=1:return []
    now=current[0]
    operation=now.get("own_attempted_operation")
    partner=now.get("reciprocated_partner_actor_visible")
    if (not now.get("joint_participation_perceived")
            or now.get("own_status")!="PERFORMED"
            or type(operation) is not str
            or type(partner) is not str or partner==actor["id"]
            or not now.get("received_cue_refs")):
        return []
    # Stronger than repeat counting: first an actual *unfinished* activity
    # with no successful coactor participation, then a different real
    # encounter in which the Other independently participated.
    prior=[h for h in history if h.get("event_ref")!=event_ref
           and h.get("own_attempted_operation")==operation
           and h.get("own_status") in ("PARTIAL","BLOCKED")
           and not h.get("joint_participation_perceived")
           and type(h.get("event_ref")) is str
           and type(h.get("experience_ref")) is str]
    if not prior:return []
    before=prior[-1]
    ident=stable_id("historically_acquired_joint_practice",{
        "actor":actor["id"],"failed":before["id"],"joint":now["id"],
        "partner":partner,"operation":operation})
    if any(x.get("id")==ident for x in actor.get("joint_practices",[])):
        return []
    return [{
        "kind":"ACQUIRE_CONDITIONAL_JOINT_PRACTICE",
        "practice_ref":ident,
        "prior_unfinished_participation_ref":before["id"],
        "later_joint_participation_ref":now["id"],
        "coactor_ref":partner,
        "operation":operation,
        "sourcefree_learning_hypothesis_not_a_law":True,
        "partner_future_consent":"MUST_REMAIN_INDEPENDENT",
        "grade":GRADE}]


def admit_joint_practice(actor,experience,event_ref,proposal):
    qualified=possible_joint_practice(actor,experience,event_ref)
    if len(qualified)!=1:
        raise ValueError("JOINT_PRACTICE_NO_DISTINCT_QUALIFIED_HISTORY")
    expected=qualified[0]
    for k in ("practice_ref","prior_unfinished_participation_ref",
              "later_joint_participation_ref","coactor_ref","operation"):
        if proposal.get(k)!=expected[k]:
            raise ValueError("JOINT_PRACTICE_FORGED_SOURCE_"+k)
    history=actor.get("participation_history",[])
    older=next(x for x in history
               if x.get("id")==expected["prior_unfinished_participation_ref"])
    later=next(x for x in history
               if x.get("id")==expected["later_joint_participation_ref"])
    if older["event_ref"]==later["event_ref"]:
        raise ValueError("JOINT_PRACTICE_ONE_EVENT_CANNOT_BE_TWO")
    record={
        "id":expected["practice_ref"],"actor":actor["id"],
        "operation":expected["operation"],
        "coactor_ref":expected["coactor_ref"],
        "origin_event_refs":[older["event_ref"],later["event_ref"]],
        "origin_experience_refs":[
            older["experience_ref"],later["experience_ref"]],
        "source_participation_refs":[older["id"],later["id"]],
        "location":experience.get("location"),
        "status":"ACQUIRED_CONDITIONAL_COORDINATION_NOT_DYAD_MASTERY",
        "inhibition_and_other_future_refusal_still_possible":True,
        "other_private_motives_not_known":True,
        "no_automatic_affective_investment":True,
        "not_an_inherent_trait_or_empirical_law":True,
        "grade":GRADE}
    actor.setdefault("joint_practices",[]).append(record)
    return {"kind":proposal["kind"],"practice_ref":record["id"],
            "status":"ADMITTED_CONDITIONAL_PRACTICE_NOT_FORCED_JOINT_SUCCESS",
            "grade":GRADE}
