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
OFFER="OFFER_PANTRY_CONTROL_TRANSFER"
ACCEPT="ACCEPT_PANTRY_CONTROL_TRANSFER"
TRANSFER_PRICE=1.0
TRANSFER_WINDOW=4
COST_INSTALL=1.0
COST_MAINTAIN=1.0
COST_SANCTION=2.0
INITIAL_FOOD_STAKE=2.0
MAINTAIN_TICKS=4
SANCTION_TICKS=3


def _amount(value,field):
    from .world import _cash_amount
    return _cash_amount(value,"R18_INVALID_"+field)




def _service(world,concession):
    ref=concession.get("enforcement_service_ref")
    provider=world.get("institutions",{}).get(ref)
    if (type(ref) is not str or type(provider) is not dict
            or provider.get("kind")!="DECLARED_FICTIONAL_ENFORCEMENT_SERVICE"
            or provider.get("site")!=concession.get("site")
            or provider.get("concession_ref")!=concession.get("id")):
        raise ValueError("R18_ENFORCEMENT_SERVICE_SOURCE_MISMATCH")
    return ref


def _paid_enforcement(world,concession,payer,cost,kind,intention):
    """Two-sided account transfer; no money minting or magical expenditure.

    The receiving entity is an explicitly fictional institutional service,
    NOT a secretly willing person. Particular human enforcement labor and
    consent remain unresolved scientific/developmental obligations.
    """
    service=_service(world,concession)
    from .world import _exact_material_delta
    money=_amount(world.get("accounts",{}).get(payer,0),
                  "ENFORCEMENT_PAYER_BALANCE")
    receiver=_amount(world.get("accounts",{}).get(service,0),
                     "ENFORCEMENT_SERVICE_BALANCE")
    if money<cost:
        raise ValueError("R18_UNFUNDED_ENFORCEMENT_TRANSFER")
    next_payer=_exact_material_delta(money,-cost,
                                    "R18_ENFORCEMENT_PAYMENT_DEBIT")
    next_provider=_exact_material_delta(receiver,cost,
                                       "R18_ENFORCEMENT_PAYMENT_CREDIT")
    identity=stable_id("enforcement_service_payment",{
        "payer":payer,"recipient":service,"kind":kind,
        "clock":world["clock"]+1,"amount":cost})
    world["accounts"][payer]=next_payer
    world["accounts"][service]=next_provider
    receipt={
        "id":identity,"clock":world["clock"]+1,
        "payer":payer,"recipient_institution":service,
        "amount":cost,"institutional_service_kind":kind,
        "actor_selection_source":intention,
        "money_conserved_between_two_accounts":True,
        "human_enforcer_consent_not_imputed":True,
        "grade":GRADE}
    world.setdefault("material_claims",[]).append({
        "clock":world["clock"]+1,"kind":"FINANCED_ENFORCEMENT_SERVICE",
        "payer":payer,"recipient":service,"amount":cost,
        "source_ref":concession["id"],
        "no_inferred_employee_or_ideology":True})
    world.setdefault("enforcement_payments",[]).append(receipt)
    return receipt

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
    q=spec.get("quorum",2)
    if type(q) is not int or not 2<=q<=len(petitioners):
        raise ValueError("R18_INVALID_QUORUM")
    provider_ref=stable_id("food_enforcement_provider",{
        "world":world["id"],"site":site,"concession":ref})
    if provider_ref in world.get("institutions",{}) or (
            provider_ref in world.get("accounts",{})):
        raise ValueError("R18_ENFORCEMENT_PROVIDER_COLLISION")
    world.setdefault("institutions",{})[provider_ref]={
        "kind":"DECLARED_FICTIONAL_ENFORCEMENT_SERVICE",
        "site":site,"concession_ref":ref,
        "separate_institution_not_a_coactor_or_person":True,
        "grade":GRADE}
    world.setdefault("accounts",{})[provider_ref]=0.0
    world.setdefault("food_control_concessions",{})[site]={
        "id":ref,"site":site,"controller":controller,
        "enforcement_service_ref":provider_ref,
        "eligible_petitioners":sorted(petitioners),
        "quorum":spec.get("quorum",2),
        "source_ref":spec["source_ref"],
        "public_notice_ref":notice,"status":"AVAILABLE_NOT_ENACTED",
        "preexisting_structural_permission_not_endogenous":True,
        "grade":GRADE}
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
    _service(world,concession)
    # All material source accounts qualified before the effective rule change.
    _amount(world["accounts"][
        concession["enforcement_service_ref"]],"INSTALL_SERVICE_BALANCE")
    created=configure_food_power(world,actors,{
        "grade":"EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO",
        "site":site,"controller_actor":who,
        "initially_permitted_givers":[who],
        "eligible_petitioners":concession["eligible_petitioners"],
        "quorum":concession["quorum"],
        "source_ref":concession["source_ref"]+":ENACTED:"+concession["id"],
        "pre_registered_concession_ref":concession["id"]})
    world.setdefault("holdings",{}).setdefault(who,{})["food"]=next_held
    world["sites"][site]["food"]=next_food
    install_payment=_paid_enforcement(
        world,concession,who,COST_INSTALL,
        "INITIAL_PANTRY_ENCLOSURE_SERVICE",intention)
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
        "payment_ref":install_payment["id"],
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
    concession=_concession(world,site)
    paid=_paid_enforcement(world,concession,who,COST_MAINTAIN,
                          "REPRODUCE_PANTRY_CONTROL",intention)
    board["r18_enforced_through"]=max(
        world["clock"],board["r18_enforced_through"])+MAINTAIN_TICKS
    receipt={"id":stable_id("paid_enforcement",{
            "board":board["id"],"clock":world["clock"]+1,
            "payer":who}),
        "clock":world["clock"]+1,"actor":who,
        "cost":COST_MAINTAIN,"kind":"MATERIAL_ENFORCEMENT_REPRODUCED",
        "payment_ref":paid["id"],
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
    concession=_concession(world,site)
    paid=_paid_enforcement(world,concession,who,COST_SANCTION,
                          "SELECTIVE_PANTRY_SANCTION",intention)
    until=world["clock"]+SANCTION_TICKS+1
    row={"id":stable_id("pantry_access_sanction",{
        "board":board["id"],"clock":world["clock"]+1,
        "target":other}),
        "controller":who,"subject":other,
        "start_clock":world["clock"]+1,"through_clock":until,
        "cost":COST_SANCTION,
        "payment_ref":paid["id"],
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



def offer_control_transfer(world,actors,who,recipient,site,intention):
    """Offer a *possible* transfer, not inherited control or recipient assent."""
    board=_owned_board(world,who,site)
    if (board is None or board.get("food_rights")!="CONTROLLED"
            or recipient not in actors or recipient==who
            or world["positions"].get(recipient)!=site):
        return {"status":"BLOCKED","outcome":"NO_SITUATED_PANTRY_TRANSFER_PARTIES"}
    previous=board.get("r18_transfer_offer")
    if previous and type(previous.get("through_clock")) is int and (
            previous["through_clock"]>=world["clock"]):
        return {"status":"BLOCKED","outcome":"ANOTHER_EFFECTIVE_TRANSFER_OFFER_EXISTS"}
    ident=stable_id("pantry_control_offer",{
        "board":board["id"],"from":who,"to":recipient,
        "clock":world["clock"]+1})
    notice=stable_id("posted_pantry_control_offer",{"offer":ident})
    record={
        "id":ident,"from_controller":who,"recipient":recipient,
        "clock":world["clock"]+1,
        "through_clock":world["clock"]+TRANSFER_WINDOW,
        "source_concession_ref":board["r18_origin_concession_ref"],
        "price":TRANSFER_PRICE,"notice_ref":notice,
        "actor_selection_source":intention,
        "recipient_has_not_yet_accepted":True,
        "grade":GRADE}
    board["r18_transfer_offer"]=record
    world.setdefault("public_notices",[]).append({
        "id":notice,"public":True,"location":site,
        "effective_from":world["clock"]+1,
        "effective_until":record["through_clock"],
        "public_terms":["food_control_offer","transmissible_property_claim"],
        "public_text":"The current controller offers to transfer pantry "+
                      "control by a separate actor-accepted material exchange.",
        "origin_rule_ref":ident,
        "acceptance_not_presumed_from_publication":True,
        "grade":GRADE})
    return {"status":"PERFORMED",
            "outcome":"PANTRY_CONTROL_TRANSFER_OFFERED_NOT_ACCEPTED",
            "offer_ref":ident,"notice_ref":notice}


def accept_control_transfer(world,actors,who,site,intention):
    """Separate independent action and paid exchange transfer real power."""
    from .food_access_struggle import _board
    board=_board(world,site)
    if (board is None or not board.get("r18_origin_concession_ref")
            or board.get("food_rights")!="CONTROLLED"):
        return {"status":"BLOCKED","outcome":"NO_TRANSFERRABLE_EFFECTIVE_PANTRY_CLAIM"}
    offer=board.get("r18_transfer_offer")
    if (not offer or offer.get("recipient")!=who or
            type(offer.get("clock")) is not int or
            type(offer.get("through_clock")) is not int or
            not offer["clock"]<=world["clock"]<=offer["through_clock"] or
            world["positions"].get(who)!=site or
            who not in actors or
            offer.get("from_controller")!=board["controller_actor"]):
        return {"status":"BLOCKED","outcome":"PANTRY_TRANSFER_OFFER_EXPIRED_OR_FOREIGN"}
    inspected=any(
        x.get("public_notice_ref")==offer["notice_ref"] and
        type(x.get("inspected_at_clock")) is int and
        offer["clock"]<=x["inspected_at_clock"]<=world["clock"]
        for x in actors[who].get("notice_exposures",[]))
    if not inspected:
        return {"status":"BLOCKED","outcome":"TRANSFER_NOTICE_NOT_PERSONALLY_INSPECTED"}
    seller=board["controller_actor"]
    buyer_cash=_amount(world.get("accounts",{}).get(who,0),
                       "PANTRY_TRANSFER_BUYER_BALANCE")
    seller_cash=_amount(world.get("accounts",{}).get(seller,0),
                        "PANTRY_TRANSFER_SELLER_BALANCE")
    price=_amount(offer["price"],"PANTRY_TRANSFER_PRICE")
    if buyer_cash<price:
        return {"status":"BLOCKED","outcome":"NO_MATERIAL_POWER_TO_ACQUIRE_CONTROL"}
    from .world import _exact_material_delta
    buyer_after=_exact_material_delta(buyer_cash,-price,
                                      "R18_TRANSFER_BUYER_CASH")
    seller_after=_exact_material_delta(seller_cash,price,
                                       "R18_TRANSFER_SELLER_CASH")
    # A paid change of controller must not retroactively rewrite the grant.
    world["accounts"][who]=buyer_after
    world["accounts"][seller]=seller_after
    board.setdefault("r18_original_controller_actor",seller)
    board["controller_actor"]=who
    board["initially_permitted_givers"]=[who]
    board["r18_transfer_offer"]=None
    receipt={
        "id":stable_id("pantry_control_transfer",{
            "board":board["id"],"offer":offer["id"],
            "new_controller":who,"clock":world["clock"]+1}),
        "clock":world["clock"]+1,"from_controller":seller,
        "to_controller":who,"offer_ref":offer["id"],
        "source_concession_ref":offer["source_concession_ref"],
        "price_paid":price,
        "enforcement_service_ability_inherited_not_ensured":True,
        "prior_controller_loses_exclusive_pantry_right":True,
        "actor_selection_source":intention,
        "recipient_motive_not_inferred":True,
        "grade":GRADE}
    board.setdefault("r18_transfer_history",[]).append(receipt)
    world.setdefault("material_claims",[]).append({
        "clock":world["clock"]+1,"kind":"PANTRY_CLAIM_PURCHASE",
        "payer":who,"recipient":seller,"amount":price,
        "source_ref":offer["id"],"paid_change_of_effective_control":True})
    return {"status":"PERFORMED",
            "outcome":"PANTRY_CONTROL_MATERIALLY_TRANSFERRED",
            "transfer_ref":receipt["id"]}


def food_power_opportunities(world,actor,site):
    """Specific existing means, not an attribution of desire or consciousness."""
    available=[];who=actor["id"]
    concession=_concession(world,site)
    if (concession and concession["controller"]==who
            and concession["status"]=="AVAILABLE_NOT_ENACTED"
            and world["positions"].get(who)==site
            and any(x.get("public_notice_ref")==concession["public_notice_ref"]
                and type(x.get("inspected_at_clock")) is int
                and x["inspected_at_clock"]<=world["clock"]
                for x in actor.get("notice_exposures",[]))
            and _amount(world.get("holdings",{}).get(
                who,{}).get("food",0),"AFFORDANCE_INSTALL_STAKE")>=2
            and _amount(world.get("accounts",{}).get(
                who,0),"AFFORDANCE_INSTALL_PAYMENT")>=COST_INSTALL):
        available.append(INSTALL)
    board=_owned_board(world,who,site)
    if board:
        old_offer=board.get("r18_transfer_offer")
        still_pending=(type(old_offer) is dict and
                       type(old_offer.get("through_clock")) is int and
                       old_offer["through_clock"]>=world["clock"])
        if (board.get("food_rights")=="CONTROLLED"
                and not still_pending):
            available.append(OFFER)
        balance=_amount(world.get("accounts",{}).get(
            who,0),"AFFORDANCE_ENFORCEMENT_CASH")
        if board["food_rights"]=="CONTROLLED" and balance>=COST_MAINTAIN:
            available.append(MAINTAIN)
        if (effective_enforcement(board,world["clock"])
                and balance>=COST_SANCTION
                and any(other!=who and location==site
                        for other,location in world["positions"].items())):
            available.append(SANCTION)
    from .food_access_struggle import _board
    existing=_board(world,site)
    if existing:
        proposed=existing.get("r18_transfer_offer")
        if (type(proposed) is dict and proposed.get("recipient")==who
                and type(proposed.get("clock")) is int
                and type(proposed.get("through_clock")) is int
                and proposed["clock"]<=world["clock"]<=proposed["through_clock"]
                and _amount(world.get("accounts",{}).get(
                    who,0),"AFFORDANCE_TRANSFER_FUNDS")>=TRANSFER_PRICE
                and any(x.get("public_notice_ref")==proposed.get("notice_ref")
                        and type(x.get("inspected_at_clock")) is int
                        and proposed["clock"]<=x["inspected_at_clock"]<=world["clock"]
                        for x in actor.get("notice_exposures",[]))):
            available.append(ACCEPT)
    if (_amount(world.get("holdings",{}).get(
            who,{}).get("food",0),"AFFORDANCE_HELD_FOOD")>=1
            and world["positions"].get(who)==site):
        available.append(COMMONS)
    return available
