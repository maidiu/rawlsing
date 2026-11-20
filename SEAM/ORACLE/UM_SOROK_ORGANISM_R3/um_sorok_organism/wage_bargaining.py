"""SORACLE R20 — contested wage relations with genuinely independent decisions.

An external sourcefree wage proposal is only a posted possibility. Workers
can separately inspect and endorse it. Even a qualified worker quorum does
not change the wage. Distinct actual workers must independently forgo shifts:
no output or wages are fabricated for those acts. An identified employer
delegate then separately receives the public demand and may ACCEPT or REJECT.
Every operation is a historically situated act inside the inherited WORLD,
not a generated class trait, morality index or claim of actual union science.
"""
from .types import GRADE,stable_id

AUTHOR="ENDORSE_WAGE_DEMAND"
WITHHOLD="WITHHOLD_WORK_SHIFT"
EMPLOYER_ACCEPT="EMPLOYER_ACCEPT_WAGE_DEMAND"
EMPLOYER_REJECT="EMPLOYER_REJECT_WAGE_DEMAND"
POLICY="SOURCEFREE_COLLECTIVE_WAGE_BARGAINING_R20"


def _amount(value,what):
    from .world import _cash_amount
    return _cash_amount(value,"R20_INVALID_"+what)


def _regime(world,site):
    from .labor_dependency import _regime
    return _regime(world,site)


def register_wage_dispute(world,actors,spec):
    """Posted hypothetical wage condition without an assumed shared motive."""
    if type(spec) is not dict or spec.get("grade")!=(
            "EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO"):
        raise ValueError("R20_UNQUALIFIED_SOURCEFREE_WAGE_CONDITIONS")
    site=spec.get("site")
    if type(site) is not str or site not in world.get("sites",{}):
        raise ValueError("R20_WAGE_DISPUTE_SITE_UNKNOWN")
    regime=_regime(world,site)
    if regime is None:
        raise ValueError("R20_WAGE_DISPUTE_REQUIRES_EXISTING_WORK_RELATION")
    if site in world.get("wage_disputes",{}):
        raise ValueError("R20_WAGE_DISPUTE_ALREADY_REGISTERED")
    if type(spec.get("source_ref")) is not str or not spec["source_ref"]:
        raise ValueError("R20_UNSOURCED_WAGE_DISPUTE")
    workers=spec.get("eligible_workers")
    if (type(workers) is not list or len(workers)<2
            or len(workers)!=len(set(workers))
            or any(type(who) is not str
                   or who not in regime["eligible_workers"]
                   or who not in actors for who in workers)):
        raise ValueError("R20_WORKERS_NOT_REGISTERED_IN_SOURCE")
    quorum=spec.get("quorum")
    if type(quorum) is not int or not 2<=quorum<=len(workers):
        raise ValueError("R20_INVALID_BARGAINING_QUORUM")
    proposal=_amount(spec.get("requested_wage"),"REQUESTED_WAGE")
    old=_amount(regime["wage"],"CURRENT_WAGE")
    if proposal<=old:
        raise ValueError("R20_NOT_AN_ACTUAL_DISTINCT_WAGE_PROPOSAL")
    ref=stable_id("wage_bargaining_procedure",{
        "site":site,"source":spec["source_ref"],
        "workers":sorted(workers),"wage":proposal,
        "clock":world["clock"]})
    posting=stable_id("posted_wage_proposal",{"procedure":ref})
    record={
        "id":ref,"site":site,"regime_ref":regime["id"],
        "controller":regime["controller"],
        "eligible_workers":sorted(workers),
        "quorum":quorum,"initial_wage":old,
        "proposed_wage":proposal,
        "public_proposal_ref":posting,
        "source_ref":spec["source_ref"],
        "endorsements":[],"stoppages":[],
        "decision":None,"decision_history":[],
        "stage":"POSTED_ONLY_NOT_A_COLLECTIVE_DEMAND",
        "proposal_exists_without_any_actor_endorsement":True,
        "grade":GRADE}
    world.setdefault("wage_disputes",{})[site]=record
    world.setdefault("public_notices",[]).append({
        "id":posting,"public":True,"location":site,
        "effective_from":world["clock"],"effective_until":None,
        "public_terms":["wage_proposal","material_work","collective_bargaining"],
        "public_text":"A proposed higher wage may be endorsed by workers "+
                      "who personally inspect this notice. Endorsements alone "+
                      "do not change the actual wage.",
        "origin_rule_ref":ref,
        "no_automatic_worker_assent":True,
        "grade":GRADE})
    return {"procedure_ref":ref,"proposal_notice_ref":posting}


def _current(world,site):
    item=world.get("wage_disputes",{}).get(site)
    if item is None:return None
    regime=_regime(world,site)
    if (not regime or type(item) is not dict
            or item.get("site")!=site
            or item.get("regime_ref")!=regime.get("id")
            or item.get("controller")!=regime.get("controller")):
        raise ValueError("R20_CONTRADICTORY_WAGE_DISPUTE_WORLD")
    return item


def _inspected(actor,ref,clock):
    return any(x.get("public_notice_ref")==ref and
               type(x.get("inspected_at_clock")) is int
               and x["inspected_at_clock"]<=clock
               for x in actor.get("notice_exposures",[]))


def _active_worker(world,who,site):
    from .labor_dependency import work_permission
    return work_permission(world,who,site) in (
        "QUALIFIED_WORK_CONTRACT_ACTIVE",
        "EMPLOYER_SANCTION_PREVENTS_PAID_WORK")


def endorse_wage_demand(world,actors,who,site,intention):
    dispute=_current(world,site)
    if not dispute or dispute["stage"]!="POSTED_ONLY_NOT_A_COLLECTIVE_DEMAND":
        return {"status":"BLOCKED","outcome":"NO_CURRENT_UNENDORSED_WAGE_PROPOSAL"}
    if (who not in dispute["eligible_workers"]
            or world["positions"].get(who)!=site
            or not _active_worker(world,who,site)
            or not _inspected(actors[who],
                              dispute["public_proposal_ref"],world["clock"])
            or any(e["actor"]==who for e in dispute["endorsements"])):
        return {"status":"BLOCKED","outcome":"WORKER_NOT_QUALIFIED_TO_ENDORSE"}
    actor_selected=(intention=="ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE")
    ref=stable_id("actual_wage_demand_endorsement",{
        "dispute":dispute["id"],"worker":who,"clock":world["clock"]+1})
    dispute["endorsements"].append({
        "id":ref,"actor":who,"clock":world["clock"]+1,
        "inspected_notice_ref":dispute["public_proposal_ref"],
        "source_of_actor_selection":intention,
        "independently_actor_selected":actor_selected,
        "not_a_proxy_for_other_workers":True,"grade":GRADE})
    independent={e["actor"] for e in dispute["endorsements"]
                 if e["independently_actor_selected"]}
    if len(independent)<dispute["quorum"]:
        return {"status":"PERFORMED",
                "outcome":"WAGE_DEMAND_ENDORSED_WITHOUT_QUALIFIED_QUORUM",
                "endorsement_ref":ref,"independent_count":len(independent),
                "wage_changed":False}
    dispute["stage"]="QUALIFIED_COLLECTIVE_DEMAND_NO_CONCESSION"
    demand_notice=stable_id("posted_actual_worker_wage_demand",{
        "dispute":dispute["id"],"clock":world["clock"]+1})
    dispute["actual_demand_notice_ref"]=demand_notice
    world.setdefault("public_notices",[]).append({
        "id":demand_notice,"public":True,"location":site,
        "effective_from":world["clock"]+1,"effective_until":None,
        "public_terms":["worker_wage_demand","employer_response_not_yet_given"],
        "public_text":"Distinct workers have made a collective demand "+
                      "for higher wages. The employer has not agreed.",
        "origin_rule_ref":dispute["id"],
        "employer_response_not_assumed":True,"grade":GRADE})
    return {"status":"PERFORMED",
            "outcome":"ACTUAL_COLLECTIVE_WAGE_DEMAND_WITHOUT_PAY_CHANGE",
            "endorsement_ref":ref,"independent_count":len(independent),
            "demand_notice_ref":demand_notice,"wage_changed":False}


def withhold_paid_shift(world,actors,who,site,intention):
    dispute=_current(world,site)
    if not dispute or dispute["stage"] not in (
            "QUALIFIED_COLLECTIVE_DEMAND_NO_CONCESSION",
            "ACTIVE_WAGE_WITHHOLDING"):
        return {"status":"BLOCKED","outcome":"NO_CURRENT_COLLECTIVE_WAGE_DISPUTE"}
    if (who not in dispute["eligible_workers"]
            or not _active_worker(world,who,site)
            or world["positions"].get(who)!=site
            or not any(e.get("actor")==who and
                       e.get("independently_actor_selected") is True
                       for e in dispute["endorsements"])):
        return {"status":"BLOCKED","outcome":"NO_OWN_QUALIFIED_PRIOR_WAGE_DEMAND"}
    ref=stable_id("materially_withheld_paid_shift",{
        "dispute":dispute["id"],"worker":who,
        "clock":world["clock"]+1})
    row={
        "id":ref,"worker":who,"clock":world["clock"]+1,
        "site":site,"dispute_ref":dispute["id"],
        "actual_worker_action":"WITHHOLD_WORK_SHIFT",
        "goods_produced_this_action":0,
        "wage_paid_this_action":0,
        "old_wage_entitlement_not_lost_for_past_work":True,
        "counterfactual_output_not_invented":True,
        "source_of_actor_selection":intention,"grade":GRADE}
    dispute["stoppages"].append(row)
    # Consequential pressure is *observed nonproduction*, not a numeric
    # diagnosis of future capital losses. The employer can still reject.
    independent={s["worker"] for s in dispute["stoppages"]
                 if s.get("source_of_actor_selection")==(
                     "ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE")}
    if len(independent)>=dispute["quorum"]:
        dispute["stage"]="ACTIVE_WAGE_WITHHOLDING"
    return {"status":"PERFORMED",
            "outcome":"ACTUAL_WORK_SHIFT_WITHHELD_NO_GOODS_OR_WAGES",
            "stoppage_ref":ref,
            "distinct_independent_withholding_workers":len(independent),
            "wage_changed":False}


def employer_respond(world,actors,delegate,site,intention,accept):
    dispute=_current(world,site)
    regime=_regime(world,site)
    if not dispute or dispute["stage"] not in (
            "QUALIFIED_COLLECTIVE_DEMAND_NO_CONCESSION",
            "ACTIVE_WAGE_WITHHOLDING"):
        return {"status":"BLOCKED","outcome":"NO_ACTIVE_WAGE_DEMAND"}
    if (delegate not in regime["authorized_delegates"]
            or world["positions"].get(delegate)!=site
            or not _inspected(actors[delegate],
                dispute.get("actual_demand_notice_ref"),world["clock"])):
        return {"status":"BLOCKED","outcome":"EMPLOYER_DELEGATE_HAS_NOT_ENCOUNTERED_DEMAND"}
    if dispute["decision"] is not None:
        return {"status":"BLOCKED","outcome":"DEMAND_ALREADY_SETTLED"}
    new_rate=dispute["proposed_wage"]
    current=_amount(regime["wage"],"CURRENT_WAGE")
    if accept:
        employer_balance=_amount(
            world.get("accounts",{}).get(regime["controller"],0),
            "EMPLOYER_BARGAINING_BALANCE")
        if employer_balance<new_rate:
            return {"status":"BLOCKED","outcome":"EMPLOYER_CANNOT_FINANCE_NEXT_WAGE"}
        # Critical: merely endorsing and withholding cannot mint a pay
        # increase. A distinctly embodied delegate must choose acceptance,
        # and the existing WORK world will pay the new price on later acts.
        regime["wage"]=new_rate
        world["institutions"][regime["controller"]]["wage"]=new_rate
        for contract in regime["contracts"].values():
            if contract.get("status")=="ACTIVE":
                contract.setdefault("wage_changes",[]).append({
                    "clock":world["clock"]+1,"old":current,
                    "new":new_rate,"source_dispute_ref":dispute["id"],
                    "worker_has_not_separately_assented_to_every_future_condition":True})
        dispute["decision"]="EMPLOYER_ACCEPTED_CHANGED_WAGE"
        dispute["stage"]="NEGOTIATED_WAGE_CHANGE_EFFECTIVE"
        outcome="EMPLOYER_ACCEPTED_COLLECTIVE_WAGE_DEMAND"
    else:
        dispute["decision"]="EMPLOYER_REJECTED_WAGE_DEMAND"
        dispute["stage"]="PUBLIC_EMPLOYER_REFUSAL"
        outcome="EMPLOYER_REJECTED_COLLECTIVE_WAGE_DEMAND"
    event_ref=stable_id("actually_decided_wage_dispute",{
        "dispute":dispute["id"],"accepted":accept,
        "delegate":delegate,"clock":world["clock"]+1})
    receipt={
        "id":event_ref,"delegate":delegate,
        "decision":dispute["decision"],
        "clock":world["clock"]+1,
        "prior_wage":current,
        "after_wage":regime["wage"],
        "distinct_worker_endorsements":sorted({
            e["actor"] for e in dispute["endorsements"]
            if e["independently_actor_selected"]}),
        "different_human_delegate_actually_selected_action":True,
        "actor_selection_source":intention,
        "not_all_worker_motives_known":True,"grade":GRADE}
    dispute["decision_history"].append(receipt)
    notice_ref=stable_id("posted_wage_dispute_outcome",{"event":event_ref})
    world.setdefault("public_notices",[]).append({
        "id":notice_ref,"public":True,"location":site,
        "effective_from":world["clock"]+1,"effective_until":None,
        "public_terms":["wage_dispute","wage_outcome",
                        "acceptance" if accept else "refusal"],
        "public_text":("A negotiated wage increase is now operative." if accept
                       else "The employer refused the workers' wage demand."),
        "origin_rule_ref":event_ref,
        "public_statement_not_universal_actor_understanding":True,
        "grade":GRADE})
    return {"status":"PERFORMED","outcome":outcome,
            "decision_ref":event_ref,
            "public_result_notice_ref":notice_ref,
            "wage_changed":accept}


def actor_bargaining_opportunities(world,actor,site):
    dispute=_current(world,site)
    if not dispute or world["positions"].get(actor["id"])!=site:
        return []
    who=actor["id"];out=[]
    if (dispute["stage"]=="POSTED_ONLY_NOT_A_COLLECTIVE_DEMAND"
            and who in dispute["eligible_workers"]
            and _active_worker(world,who,site)
            and _inspected(actor,dispute["public_proposal_ref"],
                           world["clock"])
            and not any(e["actor"]==who for e in dispute["endorsements"])):
        out.append(AUTHOR)
    if (dispute["stage"] in (
            "QUALIFIED_COLLECTIVE_DEMAND_NO_CONCESSION",
            "ACTIVE_WAGE_WITHHOLDING")
            and who in dispute["eligible_workers"]
            and _active_worker(world,who,site)
            and any(e["actor"]==who and e["independently_actor_selected"]
                    for e in dispute["endorsements"])):
        out.append(WITHHOLD)
    regime=_regime(world,site)
    if (dispute["stage"] in (
            "QUALIFIED_COLLECTIVE_DEMAND_NO_CONCESSION",
            "ACTIVE_WAGE_WITHHOLDING")
            and who in regime["authorized_delegates"]
            and _inspected(actor,dispute.get("actual_demand_notice_ref"),
                           world["clock"])):
        out +=[EMPLOYER_ACCEPT,EMPLOYER_REJECT]
    return out
