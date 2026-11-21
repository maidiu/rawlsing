"""SORACLE R19 — personally experienced income obstruction, not assumed ideology.

An actor may sense that its own WORK attempt was unfinished and later use
actually existing worker relief, while the causal employment decision remains
in the independent world. No automatic belief about an employer's motives.
"""
from .types import stable_id,GRADE


def conserve_incomplete_work(actor,experience,event_ref):
    if actor.get("id")!=experience.get("actor"):
        raise ValueError("R19_WORK_EXPERIENCE_FOREIGN_ACTOR")
    if (experience.get("own_action")!="WORK"
            or experience.get("status") not in ("PARTIAL","BLOCKED")
            or not experience.get("participated")
            or (experience.get("felt_enactment") or {}).get(
                "attempted_operation")!="WORK"):
        return None
    seen=[x for x in experience.get("perceived_cues",[])
          if type(x) is dict and
          x.get("kind")=="performed_work"
          and x.get("source_actor")==actor["id"]
          and x.get("description")=="ATTEMPT_NOT_COMPLETED"
          and type(x.get("id")) is str]
    if len(seen)!=1:return None
    if type(experience.get("clock")) is not int:
        raise ValueError("R19_WORK_EXPERIENCE_NO_CLOCK")
    ident=stable_id("lived_unfinished_wage_activity",{
        "actor":actor["id"],"event":event_ref,
        "cue":seen[0]["id"]})
    if any(x.get("id")==ident for x in actor.get(
            "labor_dependency_encounters",[])):
        raise ValueError("R19_WORK_EXPERIENCE_DUPLICATE")
    row={
        "id":ident,"actor":actor["id"],
        "clock":experience["clock"],"location":experience.get("location"),
        "experience_ref":experience["ref"],"world_event_ref":event_ref,
        "own_attempted_work":"WORK",
        "received_unfinished_sign_ref":seen[0]["id"],
        "reason_employer_or_body_or_structural":"NOT_INFERRED",
        "future_income_absent_or_lost":"NOT_YET_MEASURED_BY_TIP",
        "not_developed_political_consciousness":True,
        "grade":GRADE}
    actor.setdefault("labor_dependency_encounters",[]).append(row)
    return row


def sourcefree_relief_recruitment(options):
    """The fallible next action remains the actor's option, not relief owed."""
    candidates=[]
    for option in options:
        if option.get("action")!="DRAW_WAGE_RELIEF":
            continue
        ground=option.get("labor_relief_ground")
        if not ground or type(ground.get("personal_failed_work_ref")) is not str:
            continue
        if option.get("psychodynamic_status")=="UNRESOLVED_CONTRADICTION":
            continue
        if option.get("preproject_recruitment",{}).get("status") in (
                "ACQUIRED_NONPROJECT_WITHHOLD",
                "UNRESOLVED_PREPROJECT_CONTRADICTION"):
            continue
        if option.get("project_courses"):
            continue
        candidates.append(option)
    if len(candidates)!=1:return None
    return {
        "action":"DRAW_WAGE_RELIEF",
        "project_id":None,
        "selection_grade":"SOURCEFREE_LIVED_UNFINISHED_WORK_RELIEF_POSSIBILITY",
        "lived_source_ref":candidates[0]["labor_relief_ground"][
            "personal_failed_work_ref"],
        "employer_motive_not_known":True,
        "collective_entitlement_not_inferred":True}
