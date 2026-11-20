"""SORACLE R19 — work, subsistence and employer power co-develop.

A sourcefree enterprise has an objectively situated controller and actual
wage capacity. A publicly inspected employment relation must be accepted by
the worker before a governed WORK can earn wages; an employer delegate can
fund a temporary exclusion, but cannot forge that worker's acceptance.
Actual wages can be transferred into a finite independently funded relief
pool. None of these states is an actor's entire psyche or a theory of class.
"""
from .types import GRADE,stable_id

ACCEPT="ACCEPT_WORK_TERMS"
SUSPEND="SUSPEND_WAGE_WORK"
RESIGN="WITHDRAW_FROM_WAGE_WORK"
CONTRIBUTE="CONTRIBUTE_WAGE_RELIEF"
DRAW="DRAW_WAGE_RELIEF"
SERVICE_COST=1.0
RELIEF_UNIT=.25
SUSPENSION_TICKS=4


def _money(value,what):
    from .world import _cash_amount
    return _cash_amount(value,"R19_INVALID_"+what)


def _transfer(world,payer,receiver,amount,kind,source,intention):
    from .world import _exact_material_delta
    frm=_money(world.get("accounts",{}).get(payer,0),"PAYER_ACCOUNT")
    to=_money(world.get("accounts",{}).get(receiver,0),"RECEIVER_ACCOUNT")
    if frm<amount:
        return None
    after_p=_exact_material_delta(frm,-amount,"R19_TRANSFER_PAYER")
    after_r=_exact_material_delta(to,amount,"R19_TRANSFER_RECEIVER")
    world["accounts"][payer]=after_p
    world["accounts"][receiver]=after_r
    ref=stable_id("sourcefree_labor_account_transfer",{
        "payer":payer,"receiver":receiver,"clock":world["clock"]+1,
        "amount":amount,"kind":kind})
    world.setdefault("material_claims",[]).append({
        "clock":world["clock"]+1,"kind":kind,
        "payer":payer,"recipient":receiver,
        "amount":amount,"source_ref":source,
        "actor_selection_source":intention,
        "no_unobserved_motive_or_other_consent":True})
    return ref


def register_work_regime(world,actors,spec):
    """Sourcefree institution is a precondition, not contracted employment."""
    if type(spec) is not dict or spec.get("grade")!=(
            "EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO"):
        raise ValueError("R19_WORK_REGIME_UNQUALIFIED")
    site=spec.get("site")
    if type(site) is not str or site not in world.get("sites",{}):
        raise ValueError("R19_WORK_UNKNOWN_SITE")
    from .world import _effective_material_controller
    controller,error=_effective_material_controller(
        world,site,world["sites"][site])
    if error or not controller or controller!=spec.get("controller"):
        raise ValueError("R19_WORK_UNQUALIFIED_EXISTING_CONTROLLER")
    workers=spec.get("eligible_workers")
    delegates=spec.get("delegates")
    if (type(workers) is not list or not workers or
            type(delegates) is not list or not delegates or
            len(workers)!=len(set(workers)) or
            len(delegates)!=len(set(delegates)) or
            any(type(a) is not str or a not in actors
                for a in workers+delegates)):
        raise ValueError("R19_WORK_INVALID_ACTOR_ROSTERS")
    if type(spec.get("source_ref")) is not str or not spec["source_ref"]:
        raise ValueError("R19_WORK_NO_SOURCE_REF")
    if site in world.get("work_regimes",{}):
        raise ValueError("R19_WORK_REGIME_DUPLICATE")
    # Sourcefree world controller must itself be an existing payer/producer
    # institution, not a selected actor's invented self-representation.
    _money(world["accounts"].get(controller,0),"ENTERPRISE_ACCOUNT")
    wage=_money(world["institutions"][controller].get("wage",0),
                "CONTRACTED_WAGE")
    if wage<=0:
        raise ValueError("R19_WORK_UNPAID_CONTRACT_CANNOT_PASS_AS_WAGE")
    ref=stable_id("fictional_work_regime",{
        "site":site,"controller":controller,"source":spec["source_ref"]})
    notice=stable_id("posted_wage_terms",{"regime":ref})
    enforcement=stable_id("labor_enforcement_service",{"regime":ref})
    relief=stable_id("independent_worker_relief_pool",{"regime":ref})
    for key in (enforcement,relief):
        if key in world.get("accounts",{}) or key in world.get("institutions",{}):
            raise ValueError("R19_ACCOUNT_IDENTITY_COLLISION")
    world.setdefault("institutions",{})[enforcement]={
        "kind":"DECLARED_LABOR_DISCIPLINE_SERVICE",
        "regime_ref":ref,
        "human_enforcement_labor_not_automatically_generated":True,
        "grade":GRADE}
    world["accounts"][enforcement]=0.0
    world["accounts"][relief]=0.0
    world.setdefault("work_regimes",{})[site]={
        "id":ref,"site":site,"controller":controller,
        "eligible_workers":sorted(workers),
        "authorized_delegates":sorted(delegates),
        "terms_notice_ref":notice,
        "wage":wage,
        "source_ref":spec["source_ref"],
        "contracts":{},
        "suspensions":[],
        "enforcement_service_ref":enforcement,
        "relief_pool_ref":relief,
        "relief_policy":"EXPLICIT_SOURCEFREE_TEMPORARY_SUSPENSION_SUPPORT",
        "employer_ownership_not_the_delegates_personality":True,
        "not_yet_any_worker_consented":True,
        "grade":GRADE}
    world.setdefault("public_notices",[]).append({
        "id":notice,"public":True,"location":site,
        "effective_from":world["clock"],"effective_until":None,
        "public_terms":["wage_work","contract_terms","employer_controls_output"],
        "public_text":"This worksite offers wage work under a specified "+
                      "controller. Actual employment requires a separate "+
                      "worker acceptance. Workers may be suspended.",
        "origin_rule_ref":ref,
        "posted_terms_not_signed_consent":True,"grade":GRADE})
    return {"regime_ref":ref,"terms_notice_ref":notice,
            "enforcement_service_ref":enforcement,
            "relief_pool_ref":relief}


def _regime(world,site):
    regime=world.get("work_regimes",{}).get(site)
    if regime is None:return None
    if (type(regime) is not dict or regime.get("site")!=site
            or regime.get("controller") not in world.get("institutions",{})):
        raise ValueError("R19_INCONSISTENT_WORK_RELATION")
    return regime


def _was_inspected(actor,ref,clock):
    return any(x.get("public_notice_ref")==ref
               and type(x.get("inspected_at_clock")) is int
               and x["inspected_at_clock"]<=clock
               for x in actor.get("notice_exposures",[]))


def work_permission(world,who,site):
    regime=_regime(world,site)
    if regime is None:return "NO_ADDITIONAL_CONTRACT_REGIME"
    contract=regime["contracts"].get(who)
    if (who not in regime["eligible_workers"] or
            not contract or contract.get("status")!="ACTIVE"):
        return "NO_ACCEPTED_WAGE_CONTRACT"
    now=world["clock"]
    if any(x.get("worker")==who and
           type(x.get("start_clock")) is int and
           type(x.get("through_clock")) is int and
           x["start_clock"]<=now<=x["through_clock"]
           for x in regime["suspensions"]):
        return "EMPLOYER_SANCTION_PREVENTS_PAID_WORK"
    return "QUALIFIED_WORK_CONTRACT_ACTIVE"


def accept_work_terms(world,actors,who,site,intention):
    regime=_regime(world,site)
    if (regime is None or who not in regime["eligible_workers"]
            or world["positions"].get(who)!=site or
            not _was_inspected(actors[who],
                               regime["terms_notice_ref"],world["clock"])):
        return {"status":"BLOCKED","outcome":"WAGE_TERMS_NOT_PERSONALLY_AVAILABLE"}
    old=regime["contracts"].get(who)
    if old and old.get("status")=="ACTIVE":
        return {"status":"BLOCKED","outcome":"WAGE_CONTRACT_ALREADY_ACTIVE"}
    ref=stable_id("accepted_wage_contract",{
        "actor":who,"site":site,"clock":world["clock"]+1,
        "source":regime["id"]})
    regime["contracts"][who]={
        "id":ref,"worker":who,"site":site,
        "controller":regime["controller"],"wage_at_acceptance":regime["wage"],
        "accepted_at_clock":world["clock"]+1,
        "source_notice_ref":regime["terms_notice_ref"],
        "actor_selection_source":intention,
        "status":"ACTIVE","not_consent_to_all_future_employer_conduct":True,
        "grade":GRADE}
    return {"status":"PERFORMED",
            "outcome":"WORKER_ACCEPTED_SPECIFIC_WORK_TERMS",
            "contract_ref":ref}


def suspend_worker(world,actors,delegate,worker,site,intention):
    regime=_regime(world,site)
    if (regime is None or delegate not in regime["authorized_delegates"]
            or worker not in regime["contracts"] or
            regime["contracts"][worker].get("status")!="ACTIVE"
            or world["positions"].get(delegate)!=site
            or delegate==worker):
        return {"status":"BLOCKED","outcome":"NO_AUTHORIZED_SITUATED_LABOR_SANCTION"}
    provider=regime["enforcement_service_ref"]
    funded=_transfer(world,regime["controller"],provider,SERVICE_COST,
                     "FINANCED_EMPLOYER_LABOR_SANCTION",
                     regime["id"],intention)
    if funded is None:
        return {"status":"BLOCKED","outcome":"EMPLOYER_CANNOT_FINANCE_SANCTION"}
    ref=stable_id("work_suspension",{
        "worker":worker,"regime":regime["id"],
        "clock":world["clock"]+1})
    receipt={"id":ref,"worker":worker,"delegate":delegate,
             "controller":regime["controller"],
             "clock":world["clock"]+1,
             "start_clock":world["clock"]+1,
             "through_clock":world["clock"]+SUSPENSION_TICKS,
             "service_payment_ref":funded,
             "actor_selection_source":intention,
             "worker_assent_not_assumed":True,
             "no_moral_justification_inferred":True,
             "grade":GRADE}
    regime["suspensions"].append(receipt)
    world.setdefault("public_notices",[]).append({
        "id":stable_id("work_suspension_notice",{"suspension":ref}),
        "public":True,"location":site,
        "effective_from":world["clock"]+1,
        "effective_until":receipt["through_clock"],
        "public_terms":["employment_suspension","income_access"],
        "public_text":"The employer has temporarily restricted access "+
                      "to paid work for a specified employee.",
        "origin_rule_ref":ref,"subject_identity_not_publicly_revealed":True,
        "grade":GRADE})
    return {"status":"PERFORMED",
            "outcome":"EMPLOYER_FINANCED_WAGE_WORK_SUSPENSION",
            "suspension_ref":ref}


def withdraw_labor(world,actors,who,site,intention):
    regime=_regime(world,site)
    if (regime is None or who not in regime["contracts"] or
            regime["contracts"][who].get("status")!="ACTIVE"
            or world["positions"].get(who)!=site):
        return {"status":"BLOCKED","outcome":"NO_SITUATED_ACTIVE_WORK_TO_WITHDRAW"}
    regime["contracts"][who]["status"]="WORKER_WITHDREW"
    regime["contracts"][who]["end_clock"]=world["clock"]+1
    regime["contracts"][who]["withdrawal_selection_source"]=intention
    return {"status":"PERFORMED","outcome":"WORKER_WITHDREW_FUTURE_LABOR"}


def _uncommitted_paid_wage(world,regime,who,site):
    """Actual wage receipts less previously funded transfers, never salary owed.

    Money is fungible. This identifies an upper bound on historically earned
    contributable claims, not which physical coins a worker happens to own.
    An initial cash balance or future unpaid wage cannot fabricate a wage-funded
    collective resource.
    """
    from decimal import Decimal
    paid=sum((Decimal(str(_money(x["wage"],"WAGE_PROVENANCE"))) for x in
        world.get("material_claims",[])
        if type(x) is dict and x.get("worker")==who
        and x.get("site")==site
        and x.get("controller")==regime["controller"]
        and type(x.get("clock")) is int and x["clock"]<=world["clock"]
        and type(x.get("wage")) in (int,float)),Decimal(0))
    assigned=sum((Decimal(str(_money(x["amount"],"PAST_RELIEF_TRANSFER")))
        for x in world.get("material_claims",[])
        if type(x) is dict and x.get("kind")=="ACTUAL_WAGE_FUNDED_RELIEF"
        and x.get("payer")==who and x.get("source_ref")==regime["id"]
        and type(x.get("amount")) in (int,float)),Decimal(0))
    if assigned>paid:
        raise ValueError("R19_RELIEF_EXCEEDS_PRIOR_ACTUAL_WAGES")
    return float(paid-assigned)


def fund_worker_relief(world,actors,who,site,intention):
    regime=_regime(world,site)
    if (regime is None or who not in regime["contracts"] or
            world["positions"].get(who)!=site):
        return {"status":"BLOCKED","outcome":"NO_SITUATED_WORKER_FOR_RELIEF"}
    if _uncommitted_paid_wage(world,regime,who,site)<RELIEF_UNIT:
        return {"status":"BLOCKED","outcome":"NO_UNCOMMITTED_PAID_WAGE_CLAIM"}
    receipt=_transfer(world,who,regime["relief_pool_ref"],RELIEF_UNIT,
                      "ACTUAL_WAGE_FUNDED_RELIEF",regime["id"],intention)
    if receipt is None:
        return {"status":"BLOCKED","outcome":"WORKER_HAS_NO_FUNDS_TO_SHARE"}
    return {"status":"PERFORMED","outcome":"WORKER_RELIEF_POOL_MATERIALLY_FUNDED",
            "relief_ref":receipt}


def draw_worker_relief(world,actors,who,site,intention):
    regime=_regime(world,site)
    if (regime is None or who not in regime["contracts"] or
            world["positions"].get(who)!=site):
        return {"status":"BLOCKED","outcome":"NO_SITUATED_WORK_RELATION_FOR_RELIEF"}
    if not any(x.get("worker")==who and
               x.get("start_clock",10**12)<=world["clock"]<=
               x.get("through_clock",-1) for x in regime["suspensions"]):
        return {"status":"BLOCKED","outcome":"NO_CURRENT_SOURCEQUALIFIED_WAGE_EXCLUSION"}
    receipt=_transfer(world,regime["relief_pool_ref"],who,RELIEF_UNIT,
                      "TEMPORARY_WORKER_RELIEF_DRAW",regime["id"],intention)
    if receipt is None:
        return {"status":"BLOCKED","outcome":"WORKER_RELIEF_POOL_EMPTY"}
    return {"status":"PERFORMED","outcome":"REAL_WAGE_RELIEF_TRANSFERRED",
            "relief_ref":receipt}


def actor_work_opportunities(world,actor,site):
    regime=_regime(world,site)
    if regime is None or world["positions"].get(actor["id"])!=site:
        return []
    who=actor["id"];out=[]
    if (who in regime["eligible_workers"]
            and work_permission(world,who,site)=="NO_ACCEPTED_WAGE_CONTRACT"
            and _was_inspected(actor,regime["terms_notice_ref"],world["clock"])):
        out.append(ACCEPT)
    if who in regime["authorized_delegates"]:
        if any(worker!=who and c.get("status")=="ACTIVE"
               for worker,c in regime["contracts"].items()):
            out.append(SUSPEND)
    if who in regime["contracts"]:
        if regime["contracts"][who].get("status")=="ACTIVE":
            out.append(RESIGN)
        if (_money(world.get("accounts",{}).get(who,0),
                   "ACTOR_RELIEF_BALANCE")>=RELIEF_UNIT
                and _uncommitted_paid_wage(
                    world,regime,who,site)>=RELIEF_UNIT):
            out.append(CONTRIBUTE)
        if (_money(world["accounts"].get(
                regime["relief_pool_ref"],0),"RELIEF_POOL_BALANCE")>=RELIEF_UNIT
                and any(x["worker"]==who and
                        x["start_clock"]<=world["clock"]<=x["through_clock"]
                        for x in regime["suspensions"])):
            out.append(DRAW)
    return out


def situated_suspension_targets(constitution,access,option):
    """Target *persons encountered*, not unseen payroll or private beliefs.

    A target-specific operation can be selected by a semantic actor policy.
    This is only a practical possibility; the independent world checks
    actual employment and sanction budgets at settlement time.
    """
    if option.get("action")!=SUSPEND:return []
    seen=sorted({c.get("source_actor") for c in access.cues
                if c.get("kind")=="coactor_present"
                and type(c.get("source_actor")) is str
                and c.get("source_actor")!=constitution.actor})
    return [{
        "option_id":stable_id("situated_labor_sanction_alternative",{
            "actor":constitution.actor,"clock":constitution.clock,
            "other":other,"action":SUSPEND}),
        "actor":constitution.actor,
        "as_of_clock":constitution.clock,
        "operation":SUSPEND,"project_id":None,
        "grounds_status":"PRESENT_PERSON_NOT_PROOF_OF_EMPLOYMENT",
        "world_request":{"operation":SUSPEND,
                         "addressed_party_ref":other,
                         "material_object_ref":None},
        "binding_status":"ACTUALLY_COPRESENT_TARGET",
        "other_motives_and_employment_status":"NOT_INFERRED",
        "world_will_requalify_authority_at_execution":True,
        "source_grade":GRADE}
        for other in seen]
