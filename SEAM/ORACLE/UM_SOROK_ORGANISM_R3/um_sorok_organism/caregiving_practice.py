"""SORACLE R16 — a material feeding act can become future practical means.

The historical actor's own actually performed FEED, not the investigator's
belief that someone should be caring, is the provenance of a possible future
feeding response. Another person remains free to refuse at each invitation.
No innate mother-role function or infant knowledge of hidden household stock.
"""
from .types import stable_id, copy, GRADE


def retain_performed_material_feeding(actor,experience,event_ref,world):
    if actor.get("id")!=experience.get("actor"):
        raise ValueError("FEEDING_PRACTICE_FOREIGN_ACTOR")
    if (experience.get("own_action")!="FEED" or
            experience.get("status")!="PERFORMED" or
            (experience.get("felt_enactment") or {}).get(
                "attempted_operation")!="FEED"):
        return None
    signs=[x for x in experience.get("perceived_cues",[])
           if type(x) is dict and x.get("kind")=="performed_feed"
           and x.get("source_actor")==actor["id"]]
    # A responsive caregiver may have a proprioceptively received FEED act
    # while the single public world sign belongs to the person signaling.
    # Actual world food settlement plus their OWN enactment is necessary;
    # absence of a public FEED sign alone is not absence of that act.
    if len(signs)>1:return None
    refs=[r for r in world.get("material_feeding_events",[])
          if r.get("clock")==experience.get("clock")
          and r.get("giver")==actor["id"]]
    # The objective world identity is inspected by the ANALYST, but neither
    # a cause nor a social role is installed as this actor's conscious reason.
    if len(refs)!=1:return None
    ref=refs[0]
    ident=stable_id("experienced_material_feeding",{
        "actor":actor["id"],"event":event_ref,"receipt":ref["id"]})
    if any(x.get("id")==ident for x in
           actor.get("performed_feeding_events",[])):
        raise ValueError("FEEDING_PRACTICE_DUPLICATE_EVENT")
    row={
        "id":ident,"world_feeding_ref":ref["id"],
        "event_ref":event_ref,"giver":actor["id"],
        "recipient":ref["recipient"],"clock":experience["clock"],
        "site":ref["site"],"material_food_source":ref["food_source"],
        "applied_nutrition_change":ref["nutrition_effect"],
        "actual_action_selection_source":ref.get(
            "actor_selection_source","UNKNOWN_NOT_ISSUED"),
        "original_action_was_actor_selected":ref.get(
            "actor_independently_selected_this_attempt",False),
        "observed_practice_not_automatic_endorsement":True,
        "received_action_sign_ref":(signs[0]["id"] if signs else None),
        "own_somatic_enactment_qualified":True,
        "operative_possible_means":"FEED",
        "skill_or_future_repetition":"NOT_ESTABLISHED",
        "conscious_reason_or_gender_duty":"NOT_ESTABLISHED",
        "grade":GRADE}
    actor.setdefault("performed_feeding_events",[]).append(row)
    return row


def project_repeat_feeding(constitution,access,option):
    if option.get("action")!="FEED" or (
            "FEED" not in access.affordances):
        return []
    peers={c.get("source_actor") for c in access.cues
           if type(c) is dict and c.get("kind")=="coactor_present"}
    out=[]
    for peer in sorted(peers):
        source=[x for x in constitution.performed_feeding_events
                if x.get("recipient")==peer
                and type(x.get("clock")) is int
                and x["clock"]<=constitution.clock]
        if not source:continue
        newest=max(source,key=lambda x:x["clock"])
        out.append({
            "option_id":stable_id("repeat_material_feeding",{
                "actor":constitution.actor,"clock":constitution.clock,
                "recipient":peer,"source":newest["id"]}),
            "actor":constitution.actor,
            "as_of_clock":constitution.clock,
            "operation":"FEED","project_id":None,
            "grounds_status":"HISTORICALLY_PERFORMED_MATERIAL_FEEDING",
            "anticipated_difference":None,
            "binding_status":"RECIPIENT_PRESENT_AND_MATERIAL_STOCK_AVAILABLE",
            "world_request":{"operation":"FEED",
                             "addressed_party_ref":peer,
                             "material_object_ref":None},
            "performed_feeding_origin_ref":newest["id"],
            "prior_practical_exercise_does_not_prove_original_willingness":True,
            "not_a_duty_or_permanent_consent":True,
            "may_choose_refusal":True,
            "grade":GRADE})
    return out


def choose_independent_repeat_feeding(options,requesting_actor,
                                      requesting_action):
    """Optional actor-specific coactor response, never caller consent injection.

    Other's independent policy may abstain. Material access, bodily ability
    and this actor's own history must all be qualified at the same moment.
    """
    if requesting_action!="SIGNAL" or type(requesting_actor) is not str:
        return None
    found=[]
    for o in options:
        if o.get("action")!="FEED" or (
                o.get("psychodynamic_status")=="UNRESOLVED_CONTRADICTION"):
            continue
        if o.get("preproject_recruitment",{}).get("status") in (
                "ACQUIRED_NONPROJECT_WITHHOLD",
                "UNRESOLVED_PREPROJECT_CONTRADICTION"):
            continue
        for alt in o.get("practical_alternatives",[]):
            if alt.get("grounds_status")!=(
                    "HISTORICALLY_PERFORMED_MATERIAL_FEEDING"):
                continue
            if alt.get("world_request",{}).get(
                    "addressed_party_ref")!=requesting_actor:
                continue
            found.append(alt)
    if len(found)!=1:return None
    return {
        "action":"FEED",
        "practical_option_id":found[0]["option_id"],
        "project_id":None,
        "selection_grade":"SOURCEFREE_INDEPENDENT_ACTOR_REPEATED_PRACTICE",
        "caregiver_future_willingness":"ACTOR_POLICY_NEW_DECISION_NOT_PROMISE",
        "not_the_requester_authoring_the_reply":True}
