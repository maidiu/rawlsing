"""SORACLE R18 — institutional domination must be reproduced materially.

This is a bounded fictional world rule, not a sociology of lawful property.
A sourcefree concession is a historically external condition; installing a
monopoly requires an actor's subsequent material transfer and paid enforcement.
The legal pantry claim and effective capacity to enforce it differ. Even after
collective reform, residual enforcement funds can selectively obstruct access.
Independent held food can instead form a non-controller commons. Nothing here
entitles an analyst to infer an individual's consciousness or motive.
"""
from .types import stable_id, GRADE

CONCESSION="SOURCEFREE_FOOD_ENCLOSURE_CONCESSION_R18"
INSTALL="INSTALL_PANTRY_GATE"
MAINTAIN="MAINTAIN_PANTRY_GATE"
SANCTION="SANCTION_PANTRY_ACCESS"
COMMONS="CONTRIBUTE_FOOD_COMMONS"
COST_INSTALL=1.0
COST_MAINTAIN=1.0
COST_SANCTION=2.0
INITIAL_FOOD_STAKE=2.0
MAINTAIN_TICKS=4
SANCTION_TICKS=3


def _amount(value,field):
    from .world import _cash_amount
    return _cash_amount(value,"R18_INVALID_"+field)


def register_concession(world,actors,spec):
    """Fixture creates a *possibility of domination*, not a ruling board."""
    if type(spec) is not dict or spec.get("grade")!=(
            "EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO"):
        raise ValueError("R18_NO_QUALIFIED_SOURCEFREE_CONCESSION")
    site=spec.get("site");controller=spec.get("possible_controller")
    petitioners=spec.get("eligible_petitioners")
    if (type(site) is not str or site not in world.get("sites",{})
            or world["sites"][site].get("shared_household_food") is not True
            or type(controller) is not str or controller not in actors
            or world["positions"].get(controller)!=site
            or type(petitioners) is not list or len(petitioners)<2
            or len(set(petitioners))!=len(petitioners)
            or any(type(p) is not str or p not in actors or
                   world["positions"].get(p)!=site for p in petitioners)
            or type(spec.get("source_ref")) is not str or
            not spec["source_ref"]):
        raise ValueError("R18_INVALID_CONCESSION")
    if world["sites"][site].get("food_access_authority") is not None:
        raise ValueError("R18_PANTRY_ALREADY_CONTROLLED")
    if site in world.get("food_control_concessions",{}):
        raise ValueError("R18_DUPLICATE_CONCESSION")
    ref=stable_id("food_concession",{
        "world":world["id"],"clock":world["clock"],"site":site,
        "controller":controller,"source":spec["source_ref"]})
    notice=stable_id("posted_food_concession",{"concession":ref})
    world.setdefault("food_control_concessions",{})[site]={
        "id":ref,"site":site,"controller":controller,
        "eligible_petitioners":sorted(petitioners),
        "quorum":spec.get("quorum",2),
        "source_ref":spec["source_ref"],
        "public_notice_ref":notice,"status":"AVAILABLE_NOT_ENACTED",
        "preexisting_structural_permission_not_endogenous":True,
        "grade":GRADE}
    q=spec.get("quorum",2)
    if type(q) is not int or not 2<=q<=len(petitioners):
        raise ValueError("R18_INVALID_QUORUM")
    world.setdefault("public_notices",[]).append({
        "id":notice,"public":True,"location":site,
        "effective_from":world["clock"],"effective_until":None,
        "public_terms":["food_enclosure_concession","pantry_rights"],
        "public_text":"A registered concession may permit an eligible holder "+
                      "to create a controlled pantry by depositing food "+
                      "and financing enforcement.",
        "origin_rule_ref":ref,"not_actor_assent":True,"grade":GRADE})
    return {"concession_ref":ref,"notice_ref":notice}


def _concession(world,site):
    return world.get("food_control_concessions",{}).get(site)


def install_gate(world,actors,who,site,intention):
    """Transfers private food into institution; no right from labor alone.

    The concession is an explicit historical *world* grant and the actor's
    actual action is another event. Both are necessary to install the gate.
    """
    concession=_concession(world,site)
    if not concession or concession["status"]!="AVAILABLE_NOT_ENACTED":
        return {"status":"BLOCKED","outcome":"NO_UNEXERCISED_PANTRY_CONCESSION"}
    if (concession["controller"]!=who or who not in actors or
            world["positions"].get(who)!=site):
        return {"status":"BLOCKED","outcome":"NO_ACTOR_ENCLOSURE_PERMISSION"}
    from .food_access_struggle import witnessed_public_procedure
    # A concession can be an uninspected objective right: the actor must
    # actually inspect its separate notice before electing to use it.
    seen=any(x.get("public_notice_ref")==concession["public_notice_ref"]
             and type(x.get("inspected_at_clock")) is int
             and x["inspected_at_clock"]<=world["clock"]
             for x in actors[who].get("notice_exposures",[]))
    if not seen:
        return {"status":"BLOCKED","outcome":"CONCESSION_NOT_PERSONALLY_INSPECTED"}
    held=_amount(world.get("holdings",{}).get(
        who,{}).get("food",0),"CONCESSION_HELD_FOOD")
    cash=_amount(world.get("accounts",{}).get(who,0),"INSTALL_CASH")
    stock=_amount(world["sites"][site].get("food",0),"PANTRY_STOCK")
    if held<INITIAL_FOOD_STAKE or cash<COST_INSTALL:
        return {"status":"BLOCKED","outcome":"INSUFFICIENT_MATERIAL_ENCLOSURE_POWER"}
    # Only successful actor action changes world rights. A raw fixture alone
    # cannot become a completed institution.
    from .world import _exact_material_delta
    from .food_access_struggle import configure_food_power, AUTHORITY
    next_held=_exact_material_delta(held,-INITIAL_FOOD_STAKE,"R18_HELD_FOOD_DELTA")
    next_food=_exact_material_delta(stock,INITIAL_FOOD_STAKE,"R18_PANTRY_STOCK_DELTA")
    next_cash=_exact_material_delta(cash,-COST_INSTALL,"R18_INSTALL_CASH_DELTA")
    created=configure_food_power(world,actors,{
        "grade":"EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO",
        "site":site,"controller_actor":who,
        "initially_permitted_givers":[who],
        "eligible_petitioners":concession["eligible_petitioners"],
        "quorum":concession["quorum"],
        "source_ref":concession["source_ref"]+":ENACTED:"+concession["id"]})
    world.setdefault("holdings",{}).setdefault(who,{})["food"]=next_held
    world["sites"][site]["food"]=next_food
    world.setdefault("accounts",{})[who]=next_cash
    board=world["institutions"][AUTHORITY]
    board["r18_origin_concession_ref"]=concession["id"]
    board["r18_requires_material_enforcement"]=True
    board["r18_enforced_through"]=world["clock"]+MAINTAIN_TICKS
    board["r18_sanctions"]=[]
    board["r18_install_event_ref"]=stable_id("material_enclosure",{
        "concession":concession["id"],"clock":world["clock"]+1})
    board["r18_enforcement_history"]=[{
        "clock":world["clock"]+1,"actor":who,"cost":COST_INSTALL,
        "kind":"INITIAL_ENFORCEMENT_FINANCED",
        "actor_selection_source":intention,
        "independent_actor_choice_not_assumed":(
            intention=="INJECTED_NOT_NATIVE_ACTOR_CHOICE"),
        "grade":GRADE}]
    concession["status"]="ENACTED_BY_MATERIAL_TRANSFER"
    concession["installation_ref"]=board["r18_install_event_ref"]
    for notice in world["public_notices"]:
        if notice.get("id")==concession["public_notice_ref"]:
            notice["effective_until"]=world["clock"]
    return {"status":"PERFORMED","outcome":"PANTRY_ENCLOSURE_MATERIALLY_ENACTED",
            "authority_ref":created["authority_ref"],
            "enclosure_event_ref":board["r18_install_event_ref"]}


def _owned_board(world,who,site):
    from .food_access_struggle import _board
    board=_board(world,site)
    if (not board or board.get("controller_actor")!=who or
            not board.get("r18_origin_concession_ref")):
        return None
    if world["positions"].get(who)!=site:
        return None
    return board


def effective_enforcement(board,clock):
    if not board.get("r18_requires_material_enforcement"):
        return True  # historical R17 declaration, explicitly not R18 origin
    through=board.get("r18_enforced_through")
    if type(through) is not int:
        raise ValueError("R18_INVALID_ENFORCEMENT_CLOCK")
    return clock<=through


def maintain_gate(world,actors,who,site,intention):
    board=_owned_board(world,who,site)
    if board is None:
        return {"status":"BLOCKED","outcome":"NO_HISTORICALLY_ENACTED_CONTROLLER"}
    if board["food_rights"]!="CONTROLLED":
        return {"status":"BLOCKED","outcome":"COLLECTIVE_RULE_ALREADY_CHANGED"}
    money=_amount(world.get("accounts",{}).get(who,0),"MAINTENANCE_CASH")
    if money<COST_MAINTAIN:
        return {"status":"BLOCKED","outcome":"NO_RESOURCES_TO_ENFORCE_CONTROL"}
    from .world import _exact_material_delta
    next_balance=_exact_material_delta(money,-COST_MAINTAIN,
                                       "R18_ENFORCEMENT_TRANSFER")
    world["accounts"][who]=next_balance
    board["r18_enforced_through"]=max(
        world["clock"],board["r18_enforced_through"])+MAINTAIN_TICKS
    receipt={"id":stable_id("paid_enforcement",{
            "board":board["id"],"clock":world["clock"]+1,
            "payer":who}),
        "clock":world["clock"]+1,"actor":who,
        "cost":COST_MAINTAIN,"kind":"MATERIAL_ENFORCEMENT_REPRODUCED",
        "actor_selection_source":intention,"grade":GRADE}
    board["r18_enforcement_history"].append(receipt)
    return {"status":"PERFORMED","outcome":"PANTRY_CONTROL_REPRODUCED",
            "enforcement_ref":receipt["id"]}


def sanction_gate(world,actors,who,other,site,intention):
    board=_owned_board(world,who,site)
    if not board or other not in actors or other==who or (
            world["positions"].get(other)!=site):
        return {"status":"BLOCKED","outcome":"NO_SITUATED_ENFORCER_OR_ADDRESSEE"}
    # Even after changing the formal access rule, the concessionary controller
    # may still command some funded enforcement apparatus. Legal success and
    # a material ability to exclude do not necessarily change together.
    if not effective_enforcement(board,world["clock"]):
        return {"status":"BLOCKED","outcome":"CONTROLLER_HAS_NO_EFFECTIVE_ENFORCEMENT"}
    money=_amount(world.get("accounts",{}).get(who,0),"SANCTION_CASH")
    if money<COST_SANCTION:
        return {"status":"BLOCKED","outcome":"INSUFFICIENT_POWER_TO_SANCTION"}
    from .world import _exact_material_delta
    world["accounts"][who]=_exact_material_delta(
        money,-COST_SANCTION,"R18_SANCTION_PAYMENT")
    until=world["clock"]+SANCTION_TICKS+1
    row={"id":stable_id("pantry_access_sanction",{
        "board":board["id"],"clock":world["clock"]+1,
        "target":other}),
        "controller":who,"subject":other,
        "start_clock":world["clock"]+1,"through_clock":until,
        "cost":COST_SANCTION,
        "world_rule_after":board["food_rights"],
        "actor_selection_source":intention,
        "not_validated_moral_justification":True,"grade":GRADE}
    board["r18_sanctions"].append(row)
    world.setdefault("public_notices",[]).append({
        "id":stable_id("posted_food_sanction",{"sanction":row["id"]}),
        "public":True,"location":site,
        "effective_from":world["clock"]+1,
        "effective_until":until,
        "public_terms":["food_sanction","institutional_exclusion"],
        "public_text":"An individual is temporarily excluded from "+
                      "the institutionally controlled pantry.",
        "origin_rule_ref":row["id"],
        "subject_not_identifiable_from_public_notice":True,
        "grade":GRADE})
    return {"status":"PERFORMED","outcome":"MATERIAL_SANCTION_ON_PANTRY_ACCESS",
            "sanction_ref":row["id"]}


def contribute_food_commons(world,actors,who,site,intention):
    """Transfer actually owned food outside the enclosure's shared store.

    No assumption of recipient consent, equal mutual aid commitments or
    inherent revolutionary benevolence. A material alternative can be built.
    """
    if (who not in actors or world["positions"].get(who)!=site or
            site not in world["sites"]):
        return {"status":"BLOCKED","outcome":"NO_SITUATED_COMMONS_CONTRIBUTOR"}
    held=_amount(world.get("holdings",{}).get(
        who,{}).get("food",0),"COMMONS_HELD_FOOD")
    if held<1:
        return {"status":"BLOCKED","outcome":"NO_OWNED_FOOD_TO_POOL"}
    from .world import _exact_material_delta
    site_obj=world["sites"][site]
    current=_amount(site_obj.get("mutual_aid_food",0),"COMMONS_STOCK")
    held_after=_exact_material_delta(held,-1,"R18_COMMONS_GIVER_DELTA")
    stock_after=_exact_material_delta(current,1,"R18_COMMONS_STOCK_DELTA")
    world.setdefault("holdings",{}).setdefault(who,{})["food"]=held_after
    site_obj["mutual_aid_food"]=stock_after
    receipt={"id":stable_id("food_commons_contribution",{
                 "giver":who,"site":site,"clock":world["clock"]+1}),
        "clock":world["clock"]+1,"giver":who,"site":site,
        "food_debited_from_private_holdings":1,
        "food_credited_to_independent_commons":1,
        "actor_selection_source":intention,
        "motives_not_inferred":True,"grade":GRADE}
    world.setdefault("food_commons_history",[]).append(receipt)
    return {"status":"PERFORMED","outcome":"INDEPENDENT_FOOD_COMMONS_ENLARGED",
            "commons_ref":receipt["id"]}


def food_power_opportunities(world,actor,site):
    """Specific existing means, not an attribution of desire or consciousness."""
    available=[];who=actor["id"]
    concession=_concession(world,site)
    if (concession and concession["controller"]==who
            and concession["status"]=="AVAILABLE_NOT_ENACTED"
            and world["positions"].get(who)==site):
        available.append(INSTALL)
    board=_owned_board(world,who,site)
    if board:
        if board["food_rights"]=="CONTROLLED":
            available.append(MAINTAIN)
        if effective_enforcement(board,world["clock"]):
            available.append(SANCTION)
    if (_amount(world.get("holdings",{}).get(
            who,{}).get("food",0),"AFFORDANCE_HELD_FOOD")>=1
            and world["positions"].get(who)==site):
        available.append(COMMONS)
    return available
