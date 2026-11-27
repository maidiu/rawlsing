"""SORACLE R16 — materially constrained reproduction, not care without food.

A historically qualified caregiver may devote real time and available food to
a recipient. Their labor, the objective stock and the dependent body are three
separate things. Requested nourishment never silently becomes delivered
nourishment; shortage never silently becomes evidence of bad motives.

A provider/source authorizes *only a fictional compressed fixture*, not the
unobserved consent, skill, intent or knowledge of every day. The explicit
sourcefree world provisioning policy divides simultaneous scarce claims
proportionally; it is not a universal culture, rationing justice law or
human-care priority. It is replaced by qualified material institutions later.
"""
from decimal import Decimal, ROUND_DOWN
from math import isfinite
from .types import stable_id, copy, GRADE
from .food_access_struggle import can_draw_shared_food

UNIT = Decimal("0.00001")
PROVISION_KIND="QUALIFIED_MATERIAL_FEEDING"
ORIGINS=frozenset(("SHARED_SITE_FOOD","GIVER_HELD_FOOD","MUTUAL_AID_FOOD"))
CAP=Decimal("1000000")


def _quantity(value, label, *, positive=False):
    if (type(value) not in (int,float) or not isfinite(value)
            or value<0 or (positive and value==0)):
        raise ValueError("PROVISION_INVALID_"+label)
    d=Decimal(str(value))
    if d>CAP or d!=d.quantize(UNIT):
        raise ValueError("PROVISION_INVALID_"+label)
    return d


def _available(world, origin, giver, location):
    if origin=="GIVER_HELD_FOOD":
        return _quantity(world.get("holdings",{}).get(
            giver,{}).get("food",0),"HELD_FOOD")
    site=world["sites"][location]
    if origin=="MUTUAL_AID_FOOD":
        return _quantity(site.get("mutual_aid_food",0),"MUTUAL_AID_FOOD")
    if not site.get("shared_household_food",False):
        raise ValueError("PROVISION_SITE_HAS_NO_SHARED_FOOD_GRANT")
    if site.get("provisioning_rule")!="PROPORTIONAL_DECLARED_CLAIMS_R1":
        raise ValueError("PROVISION_UNKNOWN_MATERIAL_ALLOCATION_RULE")
    return _quantity(site.get("food",0),"SHARED_FOOD")


def qualify_feeding(world,actors,process,start,days):
    """Qualify source-verified, site-local child provisioning BEFORE any write."""
    if process.get("kind")!=PROVISION_KIND:
        raise ValueError("PROVISION_INVALID_KIND")
    giver=process.get("actor");recipient=process.get("recipient")
    loc=process.get("location");origin=process.get("supply_origin")
    if (type(giver) is not str or type(recipient) is not str or
            giver==recipient or giver not in actors or
            recipient not in actors):
        raise ValueError("PROVISION_UNREGISTERED_GIVER_OR_RECIPIENT")
    if (loc not in world.get("sites",{}) or
            world.get("positions",{}).get(giver)!=loc or
            world.get("positions",{}).get(recipient)!=loc or
            actors[giver].get("location")!=loc or
            actors[recipient].get("location")!=loc):
        raise ValueError("PROVISION_NOT_COLOCATED")
    if not any(p.get("status","active")=="active" and
               "CARE" in p.get("means",[])
               for p in actors[giver].get("projects",[])):
        raise ValueError("PROVISION_NO_HISTORICAL_CARE_COURSE")
    if origin not in ORIGINS:
        raise ValueError("PROVISION_NO_OWNED_OR_SHARED_FOOD_ORIGIN")
    daily=_quantity(process.get("food_units_per_active_day"),
                    "DAILY_FOOD_REQUEST",positive=True)
    exposure=process.get("provisional_exposure_fraction")
    if (type(exposure) not in (float,int) or not isfinite(exposure)
            or not 0<=exposure<=1):
        raise ValueError("PROVISION_BAD_EXPOSURE_FRACTION")
    requested=(daily*Decimal(str(exposure))*Decimal(days)).quantize(UNIT)
    if requested<=0:
        raise ValueError("PROVISION_ZERO_REQUEST")
    _available(world,origin,giver,loc)
    key=stable_id("provisioning_claim",{
        "giver":giver,"recipient":recipient,
        "source":process["source_ref"],"location":loc,
        "origin":origin,"start":start,"days":days})
    return {
        "id":key,"giver":giver,"recipient":recipient,"location":loc,
        "origin":origin,"source_ref":process["source_ref"],
        "requested_units":str(requested),
        "time_claimed_from":"R13_FINITE_ACTOR_TIME",
        "not_witnessed_day_by_day":True,
        "caregiver_willingness_each_day":"NOT_ESTABLISHED",
        "grade":GRADE}


def _allocate(pool, claims):
    """A declared objective fixture rule, invariant under input order.

    At five decimal places, residual goes to the lowest stable claim ID.
    The residual rule is transparent, not human merit or caregiving priority.
    """
    claims=sorted(claims,key=lambda c:c["id"])
    requests=[Decimal(c["requested_units"]) for c in claims]
    total=sum(requests,Decimal(0))
    actual=min(pool,total)
    if not claims or total<=0:return []
    amounts=[(actual*r/total).quantize(UNIT,rounding=ROUND_DOWN)
             for r in requests]
    remaining=int((actual-sum(amounts,Decimal(0)))/UNIT)
    if remaining<0 or remaining>len(claims):
        raise ValueError("PROVISION_ROUNDING_ERROR")
    for i in range(remaining):
        if amounts[i]+UNIT>requests[i]:
            raise ValueError("PROVISION_RESIDUAL_EXCEEDS_REQUEST")
        amounts[i]+=UNIT
    if sum(amounts,Decimal(0))!=actual:
        raise ValueError("PROVISION_NONCONSERVATION")
    return list(zip(claims,amounts))


def settle_provisioning(world, actors, allocation):
    """World-owned scarce stocks settle before actor developmental inference.

    All pools and IDs validated before mutation. The caller uses its existing
    transactional ledger, so any subsequent failure cannot commit half a day.
    """
    start=allocation["start_clock"];days=allocation["days"]
    procs=[p for p in allocation["qualified"]
           if p.get("kind")==PROVISION_KIND]
    claims=[qualify_feeding(world,actors,p,start,days) for p in procs]
    if len({c["id"] for c in claims})!=len(claims):
        raise ValueError("PROVISION_DUPLICATE_SOURCE_CLAIM")
    pools={}
    for claim in claims:
        key=(claim["origin"],
             claim["giver"] if claim["origin"]=="GIVER_HELD_FOOD"
             else claim["location"])
        pools.setdefault(key,[]).append(claim)
    outcomes=[];changes=[]
    # Plan nutrition across *all* competing sources before any mutation.
    # Two carers cannot each independently raise the same child's body
    # toward one and then sum their isolated gains beyond physiology.
    projected_nutrition={
        aid:_quantity(actor["body"]["nutrition"],"RECIPIENT_NUTRITION")
        for aid,actor in actors.items()}
    for key,items in sorted(pools.items()):
        origin,holder=key
        loc=items[0]["location"]
        pool=_available(world,origin,items[0]["giver"],loc)
        if pool>CAP:
            raise ValueError("PROVISION_POOL_EXCEEDS_CAP")
        # A pantry controller can withhold *accessible* stock without
        # deleting its physical existence. Distinct eligible and restricted
        # claims may coexist against the same site. Only entitled requests
        # compete for the accessible portion; denied claims consume nothing.
        eligible_claims=[
            claim for claim in items if
            origin in ("GIVER_HELD_FOOD","MUTUAL_AID_FOOD") or
            can_draw_shared_food(world,claim["giver"],loc)]
        alloc=_allocate(pool,eligible_claims)
        allowed_amounts={claim["id"]:amount for claim,amount in alloc}
        delivered=sum(allowed_amounts.values(),Decimal(0))
        changes.append((key,pool-delivered))
        for claim in sorted(items,key=lambda x:x["id"]):
            amount=allowed_amounts.get(claim["id"],Decimal(0))
            denied=(origin=="SHARED_SITE_FOOD" and
                    not can_draw_shared_food(world,claim["giver"],loc))
            requested=Decimal(claim["requested_units"])
            shortage=requested-amount
            # Provisional physiology: max 0.02 body nutrition per unit. It
            # does NOT certify a diet or infer hunger satisfaction from hours.
            recipient=claim["recipient"]
            old=projected_nutrition[recipient]
            nominal=min(Decimal("0.50"),amount*Decimal("0.02"))
            after=min(Decimal("1"),old+nominal).quantize(UNIT)
            gained=after-old
            projected_nutrition[recipient]=after
            outcomes.append({
                "id":stable_id("material_feeding_period",{
                    "claim":claim["id"],"delivery":str(amount),
                    "start":start,"days":days}),
                "claim_ref":claim["id"],
                "source_ref":claim["source_ref"],
                "giver":claim["giver"],"recipient":claim["recipient"],
                "location":claim["location"],"origin":origin,
                "start_clock":start,"end_clock":start+days,
                "requested_food_units":float(requested),
                "consumed_food_units":float(amount),
                "uncovered_food_units":float(shortage),
                "uncovered_due_to_institutional_rights_units":(
                    float(requested) if denied else 0.0),
                "uncovered_due_to_material_shortage_units":(
                    0.0 if denied else float(shortage)),
                "physical_stock_was_present_but_inaccessible":(
                    bool(denied and pool>0)),
                "actual_recipient_nutrition_gain":float(gained),
                "material_status":(
                    "INSTITUTIONAL_RIGHTS_DENIED" if denied else
                    "FULLY_PROVISIONED" if shortage==0 else
                    "PARTIALLY_PROVISIONED" if amount>0 else
                    "UNPROVISIONED_NO_AVAILABLE_FOOD"),
                "caregiver_effort":"ACCOUNTED_IN_FINITE_TIME",
                "no_individually_witnessed_meals":True,
                "failure_is_not_evidence_of_caregiver_unwillingness":True,
                "no_actor_causal_comprehension_inferred":True,
                "policy":"PROPORTIONAL_DECLARED_CLAIMS_R1",
                "grade":"SOURCEFREE_QUALIFIED_MATERIAL_PROVISIONING"})
    # Validate the entire settlement first, then apply exact material
    # conservation and nutrition as one transaction.
    for key,nextstock in changes:
        origin,holder=key
        if origin=="GIVER_HELD_FOOD":
            old=world.setdefault("holdings",{}).setdefault(
                holder,{}).get("food",0)
        elif origin=="MUTUAL_AID_FOOD":
            old=world["sites"][holder].get("mutual_aid_food",0)
        else:
            old=world["sites"][holder]["food"]
        _quantity(old,"FOOD_BEFORE_SETTLEMENT")
        _quantity(float(nextstock),"FOOD_AFTER_SETTLEMENT")
    for recipient,final in projected_nutrition.items():
        _quantity(float(final),"RECIPIENT_AFTER_SETTLEMENT")
    for key,nextstock in changes:
        origin,holder=key
        if origin=="GIVER_HELD_FOOD":
            world["holdings"][holder]["food"]=float(nextstock)
        elif origin=="MUTUAL_AID_FOOD":
            world["sites"][holder]["mutual_aid_food"]=float(nextstock)
        else:
            world["sites"][holder]["food"]=float(nextstock)
    for recipient,final in projected_nutrition.items():
        actors[recipient]["body"]["nutrition"]=float(final)
    world.setdefault("material_provisioning_periods",[]).extend(outcomes)
    return outcomes


def visitor_held_food_available(world, giver, location):
    """A human may offer only existing held stock, not another's pantry."""
    person=world.get("neighbor_users",{}).get(giver,{})
    return (person.get("present") is True
            and person.get("location")==location
            and giver not in world.get("positions",{})
            and _quantity(world.get("holdings",{}).get(giver,{}).get(
                "food",0),"VISITOR_HELD_FOOD")>=1)


def current_feeding_sources(world,giver,location):
    """Existing eligible sources, not another person's private stock or a promise.

    A sourcefree local practical power is not a claim of subjective
    recognition of the controller, entitlement under native law, or future
    availability. No stock amount is returned to semantic policy.
    """
    if world.get("positions",{}).get(giver)!=location:
        return []
    site=world.get("sites",{}).get(location)
    if site is None:return []
    out=[]
    if _quantity(world.get("holdings",{}).get(giver,{}).get("food",0),
                 "GIVER_HELD_FOOD")>=1:
        out.append("GIVER_HELD_FOOD")
    if _quantity(site.get("mutual_aid_food",0),"INDEPENDENT_COMMONS_FOOD")>=1:
        out.append("MUTUAL_AID_FOOD")
    if (site.get("shared_household_food") is True
            and site.get("provisioning_rule")=="PROPORTIONAL_DECLARED_CLAIMS_R1"
            and can_draw_shared_food(world,giver,location)
            and _quantity(site.get("food",0),"HOUSEHOLD_FOOD")>=1):
        out.append("SHARED_SITE_FOOD")
    return out


def offer_feeding_source_alternatives(world,access,option):
    """Refine existing addressed FEED alternatives, never create a new end.

    Keep legacy action-only and previously issued option IDs unchanged. A
    selected source is a different materially consequential means, even when
    the same FEED operation and recipient are held fixed.
    """
    if option.get("action")!="FEED" or "FEED" not in access.affordances:
        return []
    sources=current_feeding_sources(world,access.actor,access.location)
    if len(sources)<2:return []
    peers={c.get("source_actor") for c in access.cues
           if c.get("kind")=="coactor_present"}
    out=[]
    for base in option.get("practical_alternatives",[]):
        target=base.get("world_request",{}).get("addressed_party_ref")
        if target not in peers or target==access.actor:continue
        for source in sources:
            row=copy(base)
            row.update(option_id=stable_id("feeding_source_option",{
                "base":base["option_id"],"actor":access.actor,
                "clock":access.world_clock,"recipient":target,"source":source}),
                grounds_status="PRESENT_FEEDING_SOURCE_ALTERNATIVE",
                source_base_option_ref=base["option_id"],
                source_base_grounds_status=base.get("grounds_status"),
                selected_feeding_source=source,
                no_future_availability_or_recipient_appraisal_inferred=True)
            out.append(row)
    return out


def perform_one_actual_feeding(world,actors,giver,recipient,location,
                               actor_selection_source='UNKNOWN_NOT_ISSUED',
                               *, qualified_human_offer_ref=None, selected_food_source=None):
    """One independently authored, actual FEED transfers a full food unit.

    No infant duty or assumed caregiver motive. This operation belongs to
    the world action resolver, not to the simulated child's self-understanding.
    """
    human_offer=(qualified_human_offer_ref is not None)
    if human_offer and (type(qualified_human_offer_ref) is not str
            or not qualified_human_offer_ref or giver in actors
            or not visitor_held_food_available(world,giver,location)):
        return {"status":"BLOCKED","outcome":"NO_QUALIFIED_HUMAN_HELD_FOOD",
                "material_feeding_ref":None}
    if (recipient not in actors or giver==recipient
            or location not in world.get("sites",{})
            or (not human_offer and (giver not in actors
                or world.get("positions",{}).get(giver)!=location
                or actors[giver].get("location")!=location))
            or world.get("positions",{}).get(recipient)!=location
            or actors[recipient].get("location")!=location):
        return {"status":"BLOCKED","outcome":"RECIPIENT_NOT_PRESENT",
                "material_feeding_ref":None}
    held=_quantity(world.get("holdings",{}).get(
        giver,{}).get("food",0),"GIVER_HELD_FOOD")
    if selected_food_source is not None:
        if (human_offer or actor_selection_source!=
                "ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE"
                or selected_food_source not in ORIGINS
                or selected_food_source not in current_feeding_sources(world,giver,location)):
            return {"status":"BLOCKED","outcome":"SELECTED_FEEDING_SOURCE_UNAVAILABLE",
                    "material_feeding_ref":None}
        origin=selected_food_source
        next_food=_available(world,origin,giver,location)-Decimal(1)
    elif held>=1:
        origin="GIVER_HELD_FOOD"
        next_food=held-Decimal(1)
    elif human_offer:
        return {"status":"BLOCKED","outcome":"NO_QUALIFIED_HUMAN_HELD_FOOD",
                "material_feeding_ref":None}
    else:
        # A collectively built store is not the controller's original pantry
        # and does not inherit that pantry's unilateral title.
        commons=_quantity(world["sites"][location].get(
            "mutual_aid_food",0),"INDEPENDENT_COMMONS_FOOD")
        if commons>=1:
            origin="MUTUAL_AID_FOOD"
            next_food=commons-Decimal(1)
        else:
            if not world["sites"][location].get("shared_household_food",False):
                return {"status":"BLOCKED",
                        "outcome":"NO_AUTHORIZED_FEEDING_STOCK",
                        "material_feeding_ref":None}
            if not can_draw_shared_food(world,giver,location):
                return {"status":"BLOCKED",
                        "outcome":"HOUSEHOLD_FOOD_ACCESS_RESTRICTED",
                        "material_feeding_ref":None}
            site_food=_quantity(world["sites"][location].get("food",0),
                                "HOUSEHOLD_FOOD")
            if site_food<1:
                return {"status":"BLOCKED",
                        "outcome":"NO_MATERIAL_FOOD_TO_GIVE",
                        "material_feeding_ref":None}
            if world["sites"][location].get("provisioning_rule")!=(
                    "PROPORTIONAL_DECLARED_CLAIMS_R1"):
                raise ValueError("FEED_UNQUALIFIED_SHARED_MATERIAL_RULE")
            origin="SHARED_SITE_FOOD"
            next_food=site_food-Decimal(1)
    body=actors[recipient]["body"]
    nutrition=_quantity(body.get("nutrition"),"RECIPIENT_NUTRITION")
    proposed=min(Decimal(1),nutrition+Decimal("0.12"))
    after=proposed.quantize(UNIT)
    identity=stable_id("independently_performed_feeding",{
        "world":world["id"],"clock":world["clock"]+1,
        "giver":giver,"recipient":recipient,"origin":origin})
    # Material effect and bodily result computed before either source changes.
    if origin=="GIVER_HELD_FOOD":
        world.setdefault("holdings",{}).setdefault(giver,{})[
            "food"]=float(next_food)
    elif origin=="MUTUAL_AID_FOOD":
        world["sites"][location]["mutual_aid_food"]=float(next_food)
    else:
        world["sites"][location]["food"]=float(next_food)
    body["nutrition"]=float(after)
    receipt={
        "id":identity,"clock":world["clock"]+1,
        "giver":giver,"recipient":recipient,"site":location,
        "food_source":origin,"food_consumed":1,
        "nutrition_before":float(nutrition),
        "nutrition_after":float(after),
        "nutrition_effect":float(after-nutrition),
        "actor_selection_source":actor_selection_source,
        "actor_independently_selected_this_attempt":(
            actor_selection_source==
            "ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE"),
        "external_action_not_actor_motive":(
            actor_selection_source=="INJECTED_NOT_NATIVE_ACTOR_CHOICE"),
        "co_presence_not_future_consent":True,
        "caregiver_intent_or_love":"NOT_INFERRED",
        "not_compressed_fiction":True,
        "grade":GRADE}
    if selected_food_source is not None:
        receipt.update(explicit_actor_selected_food_source=selected_food_source,
                       food_pool_holder=(giver if origin=="GIVER_HELD_FOOD" else location),
                       food_pool_before=float(next_food+Decimal(1)),
                       food_pool_after=float(next_food),
                       no_counterfactual_lost_wage_or_motive_inferred=True)
    if human_offer:
        receipt.update(human_authored_offer_ref=qualified_human_offer_ref,
                       actor_independently_selected_this_attempt=False,
                       human_authored_offer_not_actor_selection=True,
                       recipient_independently_accepted=True)
    world.setdefault("material_feeding_events",[]).append(receipt)
    world.setdefault("social_reproductive_labor",[]).append({
        "id":identity+":labor","giver":giver,"recipient":recipient,
        "site":location,"clock":world["clock"]+1,
        "work_kind":"DIRECT_MATERIAL_FEEDING",
        "material_feed_ref":identity,
        "caregiver_bodily_cost":("HUMAN_BODILY_COST_NOT_MODELED"
                              if human_offer else "PHYSICAL_ACTION_FEED"),
        "grade":GRADE})
    return {"status":"PERFORMED","outcome":"MATERIAL_FOOD_GIVEN",
            "material_feeding_ref":identity}
