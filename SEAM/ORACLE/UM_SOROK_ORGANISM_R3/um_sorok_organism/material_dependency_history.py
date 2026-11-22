"""SORACLE R18 — an unfinished material activity can change later possibility.

The actor does not automatically know why care failed. Record an actual
actor-sensed attempted operation and event sign, not the analyst's power
diagnosis. A later self-owned alternative material source can recruit action.
The difference between actor experience and objective institutional cause
is essential: this is not a fabricated class-consciousness module.
"""
from .types import stable_id,GRADE


def conserve_sensed_material_nonperformance(actor,experience,event_ref):
    if actor.get("id")!=experience.get("actor"):
        raise ValueError("R18_MATERIAL_EXPERIENCE_FOREIGN_ACTOR")
    if (experience.get("own_action")!="FEED" or
            experience.get("status") not in ("BLOCKED","PARTIAL")
            or not experience.get("participated")
            or (experience.get("felt_enactment") or {}).get(
                "attempted_operation")!="FEED"):
        return None
    clock=experience.get("clock")
    if type(clock) is not int:
        raise ValueError("R18_MATERIAL_EXPERIENCE_UNCLOCKED")
    signs=[x for x in experience.get("perceived_cues",[])
           if type(x) is dict and
           x.get("kind")=="performed_feed"
           and x.get("source_actor")==actor["id"]
           and x.get("description")=="ATTEMPT_NOT_COMPLETED"
           and type(x.get("id")) is str]
    if len(signs)!=1:return None
    identity=stable_id("experienced_unfinished_feeding",{
        "actor":actor["id"],"clock":clock,
        "event_ref":event_ref,"received":signs[0]["id"]})
    if any(x.get("id")==identity for x in actor.get(
            "material_dependency_encounters",[])):
        raise ValueError("R18_MATERIAL_EXPERIENCE_DUPLICATE")
    row={
        "id":identity,"actor":actor["id"],
        "experience_ref":experience["ref"],
        "event_ref":event_ref,
        "clock":clock,"location":experience.get("location"),
        "own_operation_attempted":"FEED",
        "received_nonperformance_sign_ref":signs[0]["id"],
        "felt_material_constraint":"SOMETHING_PREVENTED_THIS_FEEDING",
        "actual_hidden_reason":"NOT_KNOWN_TO_ACTOR",
        "cause_does_not_have_to_be_institutional":"UNRESOLVED",
        "possible_future_material_alternative":"NOT_AUTOMATICALLY_PURSUED",
        "grade":GRADE}
    actor.setdefault("material_dependency_encounters",[]).append(row)
    return row


def choose_lived_material_counterpath(options):
    """One bounded *possible* response, not emancipation or moral virtue."""
    matches=[]
    for op in options:
        if op.get("action")!="CONTRIBUTE_FOOD_COMMONS":
            continue
        ground=op.get("material_counterpower_ground")
        if not ground or type(ground.get(
                "personally_sensed_incomplete_feeding_ref")) is not str:
            continue
        if (op.get("psychodynamic_status")=="UNRESOLVED_CONTRADICTION"
                or op.get("preproject_recruitment",{}).get("status") in (
                    "ACQUIRED_NONPROJECT_WITHHOLD",
                    "UNRESOLVED_PREPROJECT_CONTRADICTION")
                or op.get("project_courses")):
            continue
        matches.append(op)
    if len(matches)!=1:return None
    return {
        "action":"CONTRIBUTE_FOOD_COMMONS",
        "project_id":None,
        "selection_grade":"SOURCEFREE_LIVED_MATERIAL_ALTERNATIVE",
        "own_earlier_experience_ref":matches[0][
            "material_counterpower_ground"][
            "personally_sensed_incomplete_feeding_ref"],
        "actor_conscious_institutional_diagnosis":"NOT_INFERRED",
        "other_people_contributions":"NOT_ASSUMED"}
