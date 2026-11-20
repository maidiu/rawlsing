"""SORACLE R17 — household food power is a material relation, not a trait.

A declared fictional household institution controls a physically existing
shared store. A caregiver can have food nearby and be unable to feed a child.
Real named actors can later use a publicly inspected procedure; only distinct
independently actor-selected contributions count toward changing the rule.
An absent child can benefit from the new right without knowing the process.

This is an explicit SOURCEFREE institutional scenario, NOT empirical property
law, a universal model of family, or proof of revolutionary consciousness.
"""
from .types import stable_id, GRADE

OPERATION="SIGN_FOOD_PETITION"
AUTHORITY="household_food_board"
RULE="DECLARED_SOURCEFREE_SHARED_FOOD_CONTROL_R1"


def configure_food_power(world,actors,spec):
    """Create one visible world-owned institution through a research fixture."""
    if type(spec) is not dict or spec.get("grade")!=(
            "EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO"):
        raise ValueError("FOOD_POWER_UNQUALIFIED_SCENARIO")
    site=spec.get("site")
    if (type(site) is not str or site not in world.get("sites",{})
            or world["sites"][site].get("shared_household_food") is not True
            or world["sites"][site].get("provisioning_rule")!=
               "PROPORTIONAL_DECLARED_CLAIMS_R1"):
        raise ValueError("FOOD_POWER_NO_OBJECTIVE_SHARED_STORE")
    if AUTHORITY in world.get("institutions",{}) or (
            "food_access_authority" in world["sites"][site]):
        raise ValueError("FOOD_POWER_ALREADY_REGISTERED")
    permitted=spec.get("initially_permitted_givers")
    signers=spec.get("eligible_petitioners")
    if (type(permitted) is not list or type(signers) is not list
            or len(permitted)<1 or len(signers)<2
            or len(set(permitted))!=len(permitted)
            or len(set(signers))!=len(signers)
            or any(type(x) is not str or not x or x not in actors
                   for x in permitted+signers)):
        raise ValueError("FOOD_POWER_INVALID_ACTOR_ROSTERS")
    quorum=spec.get("quorum")
    if type(quorum) is not int or not 2<=quorum<=len(signers):
        raise ValueError("FOOD_POWER_INVALID_QUORUM")
    if type(spec.get("source_ref")) is not str or not spec["source_ref"]:
        raise ValueError("FOOD_POWER_NO_SOURCEFREE_IDENTITY")
    if any(world.get("positions",{}).get(a)!=site for a in signers):
        raise ValueError("FOOD_POWER_SIGNER_NOT_PRESENT_AT_DECLARATION")
    ref=stable_id("fictional_food_access_order",{
        "world":world["id"],"clock":world["clock"],"site":site,
        "source":spec["source_ref"],"permitted":sorted(permitted),
        "petitioners":sorted(signers),"quorum":quorum})
    notice_ref=stable_id("public_food_rights_notice",{"authority_ref":ref})
    words=["household_food","public_petition","collective_food_access"]
    notice={
        "id":notice_ref,"public":True,"location":site,
        "effective_from":world["clock"],
        "effective_until":None,"public_terms":words,
        "public_text":"Household food is restricted. A public procedure "+
                      "accepts independent signatures for shared access.",
        "origin_rule_ref":ref,
        "public_notice_not_automatic_comprehension":True,
        "grade":GRADE}
    board={
        "id":ref,"controls":site,"food_rights":"CONTROLLED",
        "initially_permitted_givers":sorted(permitted),
        "eligible_petitioners":sorted(signers),
        "source_ref":spec["source_ref"],
        "declaration":"EXTERNAL_SOURCEFREE_WORLD_FIXTURE_NOT_ACTOR_ACTION",
        "public_notice_ref":notice_ref,
        "petition_quorum":quorum,
        "signatures":[],"rule_history":[],
        "not_derived_from_a_personality_label":True,
        "sourcefree_policy_not_universal_legal_law":True,
        "grade":GRADE}
    world["institutions"][AUTHORITY]=board
    world["sites"][site]["food_access_authority"]=AUTHORITY
    world.setdefault("public_notices",[]).append(notice)
    return {"authority_ref":ref,"public_notice_ref":notice_ref,
            "site":site,"grade":GRADE}


def _board(world,site):
    appointed=world.get("sites",{}).get(site,{}).get(
        "food_access_authority")
    board=world.get("institutions",{}).get(AUTHORITY)
    if appointed is None and board is None:
        return None
    if (appointed!=AUTHORITY or type(board) is not dict or
            board.get("controls")!=site or
            board.get("food_rights") not in (
                "CONTROLLED","SHARED_BY_COLLECTIVE_ACTS")):
        raise ValueError("FOOD_POWER_WORLD_AUTHORITY_INCONSISTENT")
    if type(board.get("initially_permitted_givers")) is not list:
        raise ValueError("FOOD_POWER_INVALID_RIGHTS_ROSTER")
    return board


def can_draw_shared_food(world,giver,site):
    """Actual institution, not actor willingness or inferred affection."""
    board=_board(world,site)
    if board is None:return True
    if type(giver) is not str or not giver:
        raise ValueError("FOOD_POWER_UNKNOWN_DRAWER")
    if board["food_rights"]=="SHARED_BY_COLLECTIVE_ACTS":
        return True
    return giver in board["initially_permitted_givers"]


def witnessed_public_procedure(actor,board):
    """Reading a public notice is not conscious assent or causal mastery."""
    return any(type(x) is dict and
               x.get("public_notice_ref")==board["public_notice_ref"]
               and "public_petition" in x.get(
                   "public_words_available",[])
               for x in actor.get("notice_exposures",[]))


def food_petition_available(world,actor,site):
    board=_board(world,site)
    if board is None or board["food_rights"]!="CONTROLLED":
        return False
    who=actor.get("id")
    if who not in board.get("eligible_petitioners",[]):
        return False
    if world.get("positions",{}).get(who)!=site:
        return False
    if not witnessed_public_procedure(actor,board):
        return False
    return not any(x.get("actor")==who for x in board["signatures"])


def live_food_petition_opportunity(world,actor,site):
    if not food_petition_available(world,actor,site):
        return []
    board=_board(world,site)
    return [{
        "operation":OPERATION,"institution":AUTHORITY,
        "source_public_notice_ref":board["public_notice_ref"],
        "site":site,"rule":"CONTINGENT_DISTINCT_ACTOR_QUORUM",
        "other_signatures_not_assumed":True,
        "historical_grounds_not_a_conscious_motive":True,
        "grade":GRADE}]


def contribute_food_petition(world,actors,who,site,intention):
    """One actor's present act; only independent decisions count for quorum."""
    actor=actors.get(who)
    if not actor or not food_petition_available(world,actor,site):
        return {"status":"BLOCKED",
                "outcome":"FOOD_PETITION_ACTOR_NOT_SITUATED",
                "institutional_rule_change":False}
    board=_board(world,site)
    autonomous=(intention=="ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE")
    signature_ref=stable_id("food_access_signature",{
        "actor":who,"clock":world["clock"]+1,
        "board":board["id"]})
    row={
        "id":signature_ref,"actor":who,"clock":world["clock"]+1,
        "notice_ref":board["public_notice_ref"],
        "actor_attempt_selection_source":intention,
        "independently_selected_in_research_runtime":autonomous,
        "witnessed_procedure_not_necessarily_agreed_ideology":True,
        "grade":GRADE}
    board["signatures"].append(row)
    independent={x["actor"] for x in board["signatures"]
                 if x["independently_selected_in_research_runtime"]}
    if len(independent)<board["petition_quorum"]:
        return {
            "status":"PERFORMED",
            "outcome":"FOOD_PETITION_RECORDED_NO_EFFECTIVE_QUORUM",
            "signature_ref":signature_ref,
            "independent_signatures":len(independent),
            "required_signatures":board["petition_quorum"],
            "institutional_rule_change":False}
    previous=board["food_rights"]
    board["food_rights"]="SHARED_BY_COLLECTIVE_ACTS"
    rule_ref=stable_id("changed_material_food_rights",{
        "board":board["id"],"clock":world["clock"]+1,
        "independent":sorted(independent)})
    receipt={
        "id":rule_ref,"effective_clock":world["clock"]+1,
        "prior":previous,"after":board["food_rights"],
        "site":site,"material_good":"SHARED_HOUSEHOLD_FOOD",
        "independent_signers":sorted(independent),
        "quorum":board["petition_quorum"],
        "source_procedure_ref":board["public_notice_ref"],
        "does_not_grant_later_private_psychic_knowledge":True,
        "applies_to_non_signers_and_children":True,
        "grade":GRADE}
    board["rule_history"].append(receipt)
    # The posted procedure remains an objective archived notice, but is not
    # itself a promise that all future actors will understand what happened.
    for notice in world.get("public_notices",[]):
        if notice.get("id")==board["public_notice_ref"]:
            notice["effective_until"]=world["clock"]
    world.setdefault("public_notices",[]).append({
        "id":stable_id("public_food_rights_change",{
            "institution_ref":rule_ref}),
        "public":True,"location":site,
        "effective_from":world["clock"]+1,
        "effective_until":None,
        "public_terms":["household_food","collective_change","shared_access"],
        "public_text":"Shared household food is now available under the "+
                      "changed institutional rule.",
        "origin_rule_ref":rule_ref,
        "objective_collective_rule_not_private_actor_knowledge":True,
        "grade":GRADE})
    return {
        "status":"PERFORMED",
        "outcome":"COLLECTIVE_FOOD_ACCESS_RIGHTS_CHANGED",
        "signature_ref":signature_ref,"policy_ref":rule_ref,
        "independent_signatures":len(independent),
        "required_signatures":board["petition_quorum"],
        "institutional_rule_change":True}


def offered_food_petition(constitution,access):
    """One situated route from historical care/frustration to public action.

    No automatic socialist belief or invented shared purpose: this is a
    proposal to act on a personally inspected public procedure that concerns
    materially practiced reproduction. The actor can still abstain.
    """
    if constitution.actor!=access.actor:
        raise ValueError("FOOD_POWER_WRONG_CONSTITUTION")
    if OPERATION not in access.affordances:return None
    noticed=[
        x for x in constitution.notice_exposures
        if "public_petition" in x.get("public_words_available",[])]
    if not noticed:return None
    practiced=[
        x for x in constitution.performed_feeding_events
        if x.get("site")==access.location and
        type(x.get("clock")) is int and
        x["clock"]<=constitution.clock]
    obstructed=[
        x for x in constitution.power_exercises
        if x.get("operation")=="FEED"
        and x.get("attempt_status_analyst_receipt") in ("BLOCKED","PARTIAL")
        and x.get("encounter_location")==access.location]
    if not practiced and not obstructed:return None
    return {
        "action":OPERATION,"score":.19,
        "basis":["ACTUAL_MATERIAL_CARE_OR_OBSTRUCTION",
                 "PERSONALLY_INSPECTED_COLLECTIVE_PROCEDURE"],
        "source_notice_exposure_ref":noticed[-1]["id"],
        "lived_care_refs":[x["id"] for x in practiced[-8:]],
        "attempted_obstruction_refs":[x["id"] for x in obstructed[-8:]],
        "public_procedure_not_an_ideological_conclusion":True,
        "quorum_not_actor's_unilateral_power":True,
        "grade":GRADE}


def choose_food_petition(options):
    """Sourcefree heuristic may nominate ONE noncontradicted qualified path."""
    offers=[
        x for x in options
        if x.get("action")==OPERATION
        and x.get("food_collective_ground",{}).get(
            "source_notice_exposure_ref")
        and x.get("psychodynamic_status")!="UNRESOLVED_CONTRADICTION"
        and x.get("preproject_recruitment",{}).get("status") not in (
            "ACQUIRED_NONPROJECT_WITHHOLD",
            "UNRESOLVED_PREPROJECT_CONTRADICTION")]
    if len(offers)!=1:return None
    if any(x.get("project_courses") for x in offers):
        return None
    return {
        "action":OPERATION,"project_id":None,
        "selection_grade":"SOURCEFREE_SITUATED_FOOD_RULE_CONTESTATION",
        "not_an_inferred_collective_identity_or_ideology":True}
