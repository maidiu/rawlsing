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
from decimal import Decimal, ROUND_DOWN, ROUND_UP
from math import isfinite
from .types import stable_id, copy, GRADE
from .food_access_struggle import can_draw_shared_food,shared_food_permission_boundaries

UNIT = Decimal("0.00001")
PROVISION_KIND="QUALIFIED_MATERIAL_FEEDING"
SELF_MEAL_KIND="QUALIFIED_SELF_MEAL"
PURCHASE_KIND="QUALIFIED_FOOD_PURCHASE"
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
    self_meal=process.get("kind")==SELF_MEAL_KIND
    if process.get("kind") not in (PROVISION_KIND,SELF_MEAL_KIND):
        raise ValueError("PROVISION_INVALID_KIND")
    giver=process.get("actor");recipient=giver if self_meal else process.get("recipient")
    if self_meal and (process.get("recipient") is not None or
            (process.get("source_registry_confirmation") or {}).get("source_grade")!="SOURCEFREE_ACTOR_LIVED_ROUTINE_PROPOSAL"):
        raise ValueError("SELF_MEAL_REQUIRES_ACTOR_LOCAL_SOURCE")
    loc=process.get("location");origin=process.get("supply_origin")
    if (type(giver) is not str or type(recipient) is not str or
            (giver==recipient)!=self_meal or giver not in actors or
            recipient not in actors):
        raise ValueError("PROVISION_UNREGISTERED_GIVER_OR_RECIPIENT")
    if (loc not in world.get("sites",{}) or
            world.get("positions",{}).get(giver)!=loc or
            world.get("positions",{}).get(recipient)!=loc or
            actors[giver].get("location")!=loc or
            actors[recipient].get("location")!=loc):
        raise ValueError("PROVISION_NOT_COLOCATED")
    if not any(p.get("status","active")=="active" and
               ("EAT" if self_meal else "CARE") in p.get("means",[])
               for p in actors[giver].get("projects",[])):
        raise ValueError("PROVISION_NO_HISTORICAL_SELF_MEAL_COURSE" if self_meal else "PROVISION_NO_HISTORICAL_CARE_COURSE")
    if self_meal and origin=="SHARED_SITE_FOOD" and loc!="home":
        raise ValueError("SELF_MEAL_SHARED_SITE_NOT_AUTHORIZED")
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
    if origin=="SHARED_SITE_FOOD" and shared_food_permission_boundaries(world,giver,loc,start,start+days-1):
        raise ValueError("PROVISION_SPLIT_AT_EFFECTIVE_FOOD_PERMISSION_CHANGE")
    key=stable_id("provisioning_claim",{
        "giver":giver,"recipient":recipient,
        "source":process["source_ref"],"location":loc,
        "origin":origin,"start":start,"days":days})
    return {
        "id":key,"giver":giver,"recipient":recipient,"location":loc,
        "origin":origin,"source_ref":process["source_ref"],
        "requested_units":str(requested),
        "modeled_labor_hours":round(process["hours_per_active_day"]*exposure*days,5),
        "time_claimed_from":"R13_FINITE_ACTOR_TIME",
        "not_witnessed_day_by_day":True,
        **({"self_meal":True,"individual_meal_choices_not_established":True}
           if self_meal else {"caregiver_willingness_each_day":"NOT_ESTABLISHED"}),
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
    # Zero and already satisfied claims cannot take the rounding residue.
    for i in range(len(claims)):
        if not remaining:break
        if amounts[i]+UNIT<=requests[i]:
            amounts[i]+=UNIT
            remaining-=1
    if remaining:raise ValueError("PROVISION_RESIDUAL_EXCEEDS_REQUEST")
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
           if p.get("kind") in (PROVISION_KIND,SELF_MEAL_KIND)]
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
            nominal=min(Decimal("0.50"),amount*Decimal("0.02")).quantize(UNIT)
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
                "modeled_labor_hours":claim["modeled_labor_hours"],
                "nominal_recipient_nutrition_gain_model":float(nominal),
                "actual_recipient_nutrition_gain":0.0,
                "nutrition_allocation_policy":"PROPORTIONAL_SIMULTANEOUS_BODILY_CAPACITY_R1",
                "material_status":(
                    "INSTITUTIONAL_RIGHTS_DENIED" if denied else
                    "FULLY_PROVISIONED" if shortage==0 else
                    "PARTIALLY_PROVISIONED" if amount>0 else
                    "UNPROVISIONED_NO_AVAILABLE_FOOD"),
                **({"self_meal":True,"own_reproduction_time":"ACCOUNTED_IN_FINITE_TIME"}
                   if claim.get("self_meal") else
                   {"caregiver_effort":"ACCOUNTED_IN_FINITE_TIME",
                    "failure_is_not_evidence_of_caregiver_unwillingness":True}),
                "no_individually_witnessed_meals":True,
                "no_actor_causal_comprehension_inferred":True,
                "policy":"PROPORTIONAL_DECLARED_CLAIMS_R1",
                "grade":"SOURCEFREE_QUALIFIED_MATERIAL_PROVISIONING"})
    # An unordered aggregate period provides no evidence that the first
    # iterated source fed first. Allocate limited bodily headroom among
    # simultaneous modeled effects, separately from physical food delivery.
    by_recipient={}
    for row in outcomes:
        by_recipient.setdefault(row["recipient"],[]).append(row)
    for recipient,rows in by_recipient.items():
        claims=[{"id":x["id"],"requested_units":str(x["nominal_recipient_nutrition_gain_model"])}
                for x in rows]
        gains={q["id"]:v for q,v in _allocate(Decimal(1)-projected_nutrition[recipient],claims)}
        for row in rows:
            row["actual_recipient_nutrition_gain"]=float(gains.get(row["id"],Decimal(0)))
        projected_nutrition[recipient]+=sum(gains.values(),Decimal(0))
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
    # Same stock competition and nutrition capacity, distinct historical
    # meaning: self-reproduction must never fabricate a caregiver relation.
    world.setdefault("material_provisioning_periods",[]).extend(
        row for row in outcomes if not row.get("self_meal"))
    from .co_regulation_history import conserve_received_period_provision
    for row in outcomes:
        if row.get("self_meal"):
            world.setdefault("material_self_meal_periods",[]).append(row)
        else:
            conserve_received_period_provision(actors[row["recipient"]],row)
    return outcomes


def qualify_period_purchase(world,actors,process,start,days):
    """Exact actor-local market course; never an invented seller."""
    from .world import _effective_material_controller,_cash_amount
    a=process.get("actor");loc=process.get("location")
    if (process.get("kind")!=PURCHASE_KIND
            or (process.get("source_registry_confirmation") or {}).get("source_grade")!="SOURCEFREE_ACTOR_LIVED_ROUTINE_PROPOSAL"
            or a not in actors or world.get("positions",{}).get(a)!=loc
            or actors[a].get("location")!=loc or loc not in world["sites"]
            or process.get("supply_origin")!="SITE_MARKET_PURCHASE"):
        raise ValueError("PURCHASE_PERIOD_UNQUALIFIED_COURSE")
    site=world["sites"][loc]
    seller,error=_effective_material_controller(world,loc,site)
    if error or seller is None or seller==a or seller!=process.get("market_seller"):
        raise ValueError("PURCHASE_PERIOD_UNQUALIFIED_SELLER")
    if not any(p.get("id")==process.get("routine_project_ref") and
               p.get("status","active")=="active" and "BUY_FOOD" in p.get("means",[])
               for p in actors[a].get("projects",[])):
        raise ValueError("PURCHASE_PERIOD_NO_OWN_PROJECT")
    price=Decimal(str(_cash_amount(site.get("food_price",1.),"PURCHASE_PERIOD_PRICE")))
    _cash_amount(world["accounts"].get(a,0),"PURCHASE_PERIOD_BUYER_CASH")
    _cash_amount(world["accounts"].get(seller,0),"PURCHASE_PERIOD_SELLER_CASH")
    _quantity(site.get("food",0),"PURCHASE_PERIOD_STOCK")
    _quantity(world.get("holdings",{}).get(a,{}).get("food",0),"PURCHASE_PERIOD_HOLDINGS")
    daily=_quantity(process.get("food_units_per_active_day"),"PURCHASE_DAILY_FOOD",positive=True)
    qty=(daily*Decimal(str(process["provisional_exposure_fraction"]))*Decimal(days)).quantize(UNIT)
    if qty<=0:raise ValueError("PURCHASE_PERIOD_ZERO_REQUEST")
    return {"id":stable_id("aggregate_purchase_claim",{"source":process["source_ref"],"start":start,"days":days}),
            "source_ref":process["source_ref"],"buyer":a,"seller":seller,"location":loc,
            "price":price,"requested":qty,"modeled_hours":round(process["hours_per_active_day"]*
                process["provisional_exposure_fraction"]*days,5)}


def settle_period_purchases(world,actors,allocation,opening_cash):
    """End-of-interval replenishment, not a fictional daily economy.

    Prior wage/provisioning settlements cannot finance retroactive purchases:
    use at most opening cash AND cash still held, and remaining physical stock.
    New food cannot retroactively provision this interval. Simultaneous
    affordable demand uses the existing proportional stock allocator.
    """
    from .world import _cash_amount,_exact_material_delta
    start=allocation["start_clock"];days=allocation["days"]
    claims=[qualify_period_purchase(world,actors,p,start,days)
            for p in allocation["qualified"] if p["kind"]==PURCHASE_KIND]
    if not claims:return []
    if len({q["buyer"] for q in claims})!=len(claims):
        raise ValueError("PURCHASE_PERIOD_COMPETING_BUYER_COURSES")
    pools={};affordable={}
    for q in claims:
        a=q["buyer"];cash=Decimal(str(min(
            _cash_amount(opening_cash.get(a,0),"PURCHASE_OPENING_CASH"),
            _cash_amount(world["accounts"].get(a,0),"PURCHASE_SETTLEMENT_CASH"))))
        cap=q["requested"] if not q["price"] else min(q["requested"],(cash/q["price"]).quantize(UNIT,rounding=ROUND_DOWN))
        affordable[q["id"]]=cap
        pools.setdefault(q["location"],[]).append({"id":q["id"],"requested_units":str(cap)})
    transfers={};stocks={};holdings={};out=[]
    for loc,requests in sorted(pools.items()):
        pool=_quantity(world["sites"][loc].get("food",0),"PURCHASE_PERIOD_STOCK")
        amounts={q["id"]:v for q,v in _allocate(pool,requests)}
        stocks[loc]=pool-sum(amounts.values(),Decimal(0))
        for q in sorted((x for x in claims if x["location"]==loc),key=lambda x:x["id"]):
            amount=amounts.get(q["id"],Decimal(0))
            paid=(amount*q["price"]).quantize(UNIT,rounding=ROUND_UP)
            buyer=q["buyer"];seller=q["seller"]
            transfers[buyer]=transfers.get(buyer,Decimal(0))-paid
            transfers[seller]=transfers.get(seller,Decimal(0))+paid
            holdings[buyer]=_quantity(world.get("holdings",{}).get(buyer,{}).get("food",0),"PURCHASE_HOLDINGS")+amount
            out.append({"id":q["id"],"source_ref":q["source_ref"],"buyer":buyer,"seller":seller,
                "location":loc,"start_clock":start,"end_clock":start+days,
                "requested_food_units":float(q["requested"]),"affordable_food_units":float(affordable[q["id"]]),
                "purchased_food_units":float(amount),"actual_paid_model":float(paid),
                "uncovered_due_to_cash_units":float(q["requested"]-affordable[q["id"]]),
                "uncovered_due_to_stock_units":float(affordable[q["id"]]-amount),
                "unit_price_model":float(q["price"]),"modeled_hours":q["modeled_hours"],
                "policy":"OPENING_CASH_REMAINING_STOCK_END_BOUNDARY_R1",
                "not_available_for_same_period_provisioning":True,
                "not_individually_witnessed_purchase_events":True,"grade":GRADE})
    cash_after={a:_exact_material_delta(_cash_amount(world["accounts"].get(a,0),"PURCHASE_ACCOUNT"),float(v),"PURCHASE_ACCOUNT_DELTA")
                for a,v in transfers.items()}
    for v in stocks.values():_quantity(float(v),"PURCHASE_FINAL_STOCK")
    for v in holdings.values():_quantity(float(v),"PURCHASE_FINAL_HOLDINGS")
    if sum(transfers.values(),Decimal(0))!=0:raise ValueError("PURCHASE_CASH_NONCONSERVATION")
    for a,v in cash_after.items():world["accounts"][a]=v
    for loc,v in stocks.items():world["sites"][loc]["food"]=float(v)
    for a,v in holdings.items():world.setdefault("holdings",{}).setdefault(a,{})["food"]=float(v)
    for row in out:
        body=actors[row["buyer"]]["body"];before=body["rest"]
        body["rest"]=min(before,round(max(0.,before-row["modeled_hours"]*.00012),5))
        row["own_rest_expenditure_model"]=round(before-body["rest"],5)
    world.setdefault("material_purchase_periods",[]).extend(out)
    return out


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


def offer_self_meal_source_alternatives(world,access,option):
    """Self-reproduction can compete with other lives for the same food.

    Refine the existing unaddressed EAT choice; no new appetite, consent,
    project or assumption of ownership. Reuse R37's qualified stock reader.
    Only multiple real sources warrant a new alternative, preserving legacy
    default IDs and avoiding unnecessary semantic expansion.
    """
    if option.get("action")!="EAT":return []
    sources=[s for s in current_feeding_sources(world,access.actor,access.location)
             if s!="SHARED_SITE_FOOD" or access.location=="home"]
    if len(sources)<2:return []
    out=[]
    for base in option.get("practical_alternatives",[]):
        request=base.get("world_request",{})
        if (request.get("operation")!="EAT" or request.get("addressed_party_ref") is not None
                or request.get("material_object_ref") is not None):continue
        for source in sources:
            row=copy(base)
            row.update(option_id=stable_id("self_meal_source",{
                "base":base["option_id"],"actor":access.actor,"clock":access.world_clock,
                "source":source}),
                grounds_status="PRESENT_SELF_MEAL_SOURCE_ALTERNATIVE",
                source_base_option_ref=base["option_id"],
                source_base_grounds_status=base.get("grounds_status"),
                selected_self_meal_source=source,
                no_other_person_stock_or_future_availability_inferred=True)
            out.append(row)
    return out


def settle_selected_self_meal(world,actor,location,source,selection_source):
    """Debit precisely the chosen source, never fall through to another.

    The existing EAT body owner applies nourishment only on actual success.
    Return an objective audit receipt; no spectator is entitled to the
    source's balance or the actor's motive. No separate material store.
    """
    if (selection_source!="ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE"
            or type(source) is not str or source not in ORIGINS
            or (source=="SHARED_SITE_FOOD" and location!="home")
            or source not in current_feeding_sources(world,actor,location)):
        return "BLOCKED","SELECTED_SELF_MEAL_SOURCE_UNAVAILABLE",None
    before=_available(world,source,actor,location)
    after=before-Decimal(1)
    if source=="GIVER_HELD_FOOD":
        world["holdings"][actor]["food"]=float(after)
        outcome="ATE_OWNED_FOOD"
    elif source=="MUTUAL_AID_FOOD":
        world["sites"][location]["mutual_aid_food"]=float(after)
        outcome="ATE_INDEPENDENT_FOOD_COMMONS"
    else:
        world["sites"][location]["food"]=float(after)
        outcome="ATE_SHARED_HOUSEHOLD_FOOD"
    receipt={"id":stable_id("selected_self_meal",{"world":world["id"],
        "actor":actor,"clock":world["clock"]+1,"location":location,"source":source}),
        "actor":actor,"clock":world["clock"]+1,"location":location,
        "food_source":source,"pool_holder":actor if source=="GIVER_HELD_FOOD" else location,
        "pool_before":float(before),"pool_after":float(after),"consumed_units":1,
        "other_person_need_or_actor_intention_not_inferred":True,"grade":GRADE}
    return "PERFORMED",outcome,receipt


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
                or type(selected_food_source) is not str
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
