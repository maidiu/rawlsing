"""SORACLE R13 — material time, social reproduction, and compressed life.

A compressed period cannot silently grant one individual 25 hours of labor,
care and practice per day, invent a coactor's every consent, or convert an
ordinary project into thousands of eyewitness successes. Source-qualified
routine exposures are *aggregate fictional model assumptions*, not identified
real events, human developmental laws, or moral duties. The world owns time,
care benefit, work claim and the distribution of costs.

Existing ordinary_life.passage and existing actor-specific practice learning
remain the first writer/reader. No new canonical P2/P6/SDTF or native rights.
"""
import math
from .types import GRADE, copy, stable_id
from .routine_sources import (verify_qualified_period_envelope, live_routine_situational_reason,
                              LIVED_CLASS, lived_work_permission_boundaries,
                              realized_lived_process)
from .organism import eligible
from .mediated_efficacy import COMPONENTS
from .material_conjunction import qualify_aggregate_material_gate
from .co_regulation_history import conserve_received_period_care
from .material_provisioning import (
    PROVISION_KIND,qualify_feeding,settle_provisioning)

DAY_HOURS=24.0
PROVISIONAL_REST_RESERVE=8.0
ACTIVE_HOURS=DAY_HOURS-PROVISIONAL_REST_RESERVE
KINDS=frozenset({'QUALIFIED_ROUTINE_PRACTICE',
                 'QUALIFIED_REPRODUCTIVE_CARE',
                 'QUALIFIED_WAGE_LABOR',
                 'QUALIFIED_MATERIAL_FEEDING',
                 'QUALIFIED_OTHER_OBLIGATION'})


def _number(value, name, *, zero=True):
    if (type(value) not in (int,float) or
            not math.isfinite(value) or value<0 or
            (not zero and value==0)):
        raise ValueError('HISTORICAL_TIME_INVALID_'+name)
    return float(value)


def _typecheck(process):
    if type(process) is not dict or process.get('kind') not in KINDS:
        raise ValueError('HISTORICAL_TIME_UNSUPPORTED_PROCESS')
    if type(process.get('source_ref')) is not str or not process['source_ref']:
        raise ValueError('HISTORICAL_TIME_UNSOURCED_PROCESS')
    if type(process.get('actor')) is not str or not process['actor']:
        raise ValueError('HISTORICAL_TIME_MISSING_ACTOR')
    site=process.get('location')
    if type(site) is not str or not site:
        raise ValueError('HISTORICAL_TIME_MISSING_SITE')
    hours=_number(process.get('hours_per_active_day'),
                  'HOURS_PER_ACTIVE_DAY',zero=False)
    fraction=_number(process.get('provisional_exposure_fraction'),
                     'EXPOSURE_FRACTION')
    if hours>24 or fraction>1:
        raise ValueError('HISTORICAL_TIME_OVERSIZED_EXPOSURE')
    return hours,fraction


def _actor_at_site(world,actors,actor,site):
    return (actor in actors and world.get('positions',{}).get(actor)==site
            and actors[actor].get('location')==site)


def _support_history(world,a,b):
    for relation in world.get('relations',{}).values():
        if ({a,b}==set(relation.get('participants',[])) and
                any(type(h) is dict and h.get('contributions')
                    for h in relation.get('history',[]))):
            return True
    return False


def qualify_period_allocation(world,actors,processes,start_clock,days):
    """Validate whole-period feasibility BEFORE any developmental/world write.

    All named historical actors pay their own time. A caregiver's costs do
    not vanish into the recipient's comfort, nor can an employer time claim
    coexist for free with care or practice. Locational stability during the
    compressed interval is a *declared* fixture assumption; any modeled
    relocation should split the interval rather than be hidden.
    """
    if type(days) is not int or not 1<=days<=3650:
        raise ValueError('HISTORICAL_TIME_INVALID_DAYS')
    if type(start_clock) is not int or start_clock<0:
        raise ValueError('HISTORICAL_TIME_INVALID_CLOCK')
    if type(processes) is not list or len(processes)>512:
        raise ValueError('HISTORICAL_TIME_INVALID_PROCESS_BUDGET')
    normalized=[];fraction_by_actor={};support_downgrades=[];withheld=[];bodily_withheld=[];situationally_withheld=[]
    claims=[];seen_lived=set()
    for i,raw in enumerate(processes):
        hours,fraction=_typecheck(raw)
        source_confirmation=verify_qualified_period_envelope(
            world,raw,start_clock,days)
        raw={**raw,'source_registry_confirmation':source_confirmation}
        a=raw['actor'];site=raw['location']
        conditional=raw.get('routine_window_application')
        if conditional not in (None,'SITUATED_CONDITIONAL_ROUTINE'):
            raise ValueError('HISTORICAL_TIME_UNKNOWN_ROUTINE_APPLICATION')
        lived_source=source_confirmation['source_grade']==LIVED_CLASS
        if lived_source:
            if raw['source_ref'] in seen_lived:raise ValueError('LIVED_ROUTINE_DUPLICATE_ALLOCATION')
            seen_lived.add(raw['source_ref'])
        if lived_source and raw['kind']=='QUALIFIED_WAGE_LABOR' and lived_work_permission_boundaries(
                world,a,site,start_clock,start_clock+days-1):
            raise ValueError('LIVED_ROUTINE_SPLIT_AT_WORK_PERMISSION_CHANGE')
        if lived_source and conditional!='SITUATED_CONDITIONAL_ROUTINE':
            raise ValueError('LIVED_ROUTINE_REQUIRES_SITUATED_APPLICATION')
        if conditional:
            # The explicit aggregate premise is not unconditional conduct.
            # Withhold a known course that is now situationally unavailable.
            # Unregistered sources/participants remain hard failures.
            if a not in actors or site not in world.get('sites',{}):
                raise ValueError('HISTORICAL_TIME_UNKNOWN_ROUTINE_PARTICIPANT_OR_SITE')
            recipient=raw.get('recipient')
            care_kind=raw['kind'] in ('QUALIFIED_REPRODUCTIVE_CARE',PROVISION_KIND)
            if care_kind and (type(recipient) is not str or recipient==a or recipient not in actors):
                raise ValueError('HISTORICAL_TIME_UNKNOWN_ROUTINE_RECIPIENT')
            active_means={op for p in actors[a].get('projects',[])
                          if p.get('status','active')=='active' for op in p.get('means',[])}
            reason=('ACTOR_ELSEWHERE' if not _actor_at_site(world,actors,a,site) else
                    'RECIPIENT_ELSEWHERE' if care_kind and not _actor_at_site(world,actors,recipient,site) else
                    'NO_ACTIVE_CARE_COURSE' if care_kind and 'CARE' not in active_means else
                    'NO_ACTIVE_WORK_COURSE' if raw['kind']=='QUALIFIED_WAGE_LABOR' and 'WORK' not in active_means else None)
            if not reason and lived_source:
                reason=live_routine_situational_reason(world,actors,raw)
            if reason:
                situationally_withheld.append({'input_index':i,'source_ref':raw['source_ref'],
                    'actor':a,'location':site,'start_clock':start_clock,
                    'end_clock':start_clock+days,'reason':reason,'proposed_routine':copy(raw),
                    'unexecuted_premise_not_missed_duty_or_sensed_event':True})
                continue
        if lived_source:
            raw=realized_lived_process(world,raw)
            hours,fraction=_typecheck(raw)
        if not _actor_at_site(world,actors,a,site):
            raise ValueError('HISTORICAL_TIME_ACTOR_NOT_AT_RECORDED_SITE')
        if raw['kind']==PROVISION_KIND:
            # Feeding is an additional, materially specified routine, never
            # silently included in generic CARE or awarded by affection.
            qualify_feeding(world,actors,raw,start_clock,days)
        if raw['kind']=='QUALIFIED_REPRODUCTIVE_CARE':
            recipient=raw.get('recipient')
            if (type(recipient) is not str or recipient==a or
                    not _actor_at_site(world,actors,recipient,site)):
                raise ValueError('HISTORICAL_TIME_NO_CO_PRESENT_CARE_RECIPIENT')
            if not any('CARE' in p.get('means',[]) and
                       p.get('status','active')=='active'
                       for p in actors[a].get('projects',[])):
                raise ValueError('HISTORICAL_TIME_NO_PRACTICED_CARE_COURSE')
        if raw['kind']=='QUALIFIED_WAGE_LABOR':
            controller=world.get('sites',{}).get(site,{}).get('controller')
            institution=world.get('institutions',{}).get(controller,{})
            if (type(controller) is not str or not controller or
                    controller==a or
                    institution.get('controls')!=site):
                raise ValueError('HISTORICAL_TIME_NO_EMPLOYMENT_RELATION')
            if not any('WORK' in p.get('means',[]) and
                       p.get('status','active')=='active'
                       for p in actors[a].get('projects',[])):
                raise ValueError('HISTORICAL_TIME_NO_PRACTICED_WORK_COURSE')
        operation=({'QUALIFIED_REPRODUCTIVE_CARE':'CARE',
                    'QUALIFIED_WAGE_LABOR':'WORK',
                    PROVISION_KIND:'FEED'}.get(raw['kind']))
        if raw['kind']=='QUALIFIED_ROUTINE_PRACTICE':
            operation=raw.get('operation')
        gate=qualify_aggregate_material_gate(world,a,site,operation,start_clock,days)
        if gate is not None and gate['readset']:
            if gate['decision'] in ('BLOCKED','UNRESOLVED'):
                # The source qualifies a proposed modeled routine, not a
                # magical right to undertake it. Do not award practice dose,
                # wage, care, food or successful micro-scenes under denial.
                withheld.append({'input_index':i,'source_ref':raw['source_ref'],
                    'actor':a,'location':site,'operation':operation,
                    'start_clock':start_clock,'end_clock':start_clock+days,
                    'objective_rule_evaluation':copy(gate),
                    'proposed_routine':copy(raw),
                    'actual_time_lost_or_actor_experience':'NOT_INFERRED',
                    'not_a_performed_or_experienced_event':True})
                continue
            raw={**raw,'aggregate_objective_gate':copy(gate)}
        if lived_source and operation is not None:
            ok,why=eligible(actors[a]['body'],operation)
            if not ok:
                bodily_withheld.append({'input_index':i,'source_ref':raw['source_ref'],
                    'actor':a,'location':site,'operation':operation,
                    'start_clock':start_clock,'end_clock':start_clock+days,
                    'entry_body_reason':why,'proposed_routine':copy(raw),
                    'coverage':'UNRESOLVED_FROM_ENTRY_BODY_NOT_ELIGIBLE',
                    'not_proof_of_later_inability_or_actor_experience':True})
                continue
        if raw['kind']=='QUALIFIED_ROUTINE_PRACTICE':
            # A future age or future relief cannot retroactively establish
            # a child's bodily participation throughout the preceding period.
            # A start-boundary refusal is uncertainty about coverage, not a
            # claim that every day was physically impossible or that the
            # child experienced a refusal. Reconsider at a later checkpoint.
            if actors[a].get('role')=='child':
                # Withheld coverage must not disguise an invalid practice
                # contract that the existing learning owner would refuse.
                if type(operation) is not str or operation not in COMPONENTS:
                    raise ValueError('ROUTINE_UNKNOWN_COMPONENT_OR_SITE')
                if raw.get('mode','ARRANGEMENT_UNRESOLVED') not in (
                        'SOLO_COMPONENT_PRACTICE','ASSISTED_COMPONENT_PRACTICE',
                        'ARRANGEMENT_UNRESOLVED'):
                    raise ValueError('ROUTINE_UNQUALIFIED_SUPPORT')
                ok,why=eligible(actors[a]['body'],operation)
                if not ok:
                    bodily_withheld.append({'input_index':i,'source_ref':raw['source_ref'],
                        'actor':a,'location':site,'operation':operation,
                        'start_clock':start_clock,'end_clock':start_clock+days,
                        'entry_body_reason':why,'proposed_routine':copy(raw),
                        'coverage':'UNRESOLVED_FROM_ENTRY_BODY_NOT_ELIGIBLE',
                        'not_proof_of_later_inability_or_actor_experience':True})
                    continue
            mode=raw.get('mode','ARRANGEMENT_UNRESOLVED')
            if mode=='ASSISTED_COMPONENT_PRACTICE':
                supporter=raw.get('support_actor')
                if (type(supporter) is not str or
                        not _actor_at_site(world,actors,supporter,site) or
                        not _support_history(world,a,supporter)):
                    # No future cooperation is inferred. The actor may still
                    # have plausible generic practice, but the specific
                    # assistant cannot be assigned by a routine label.
                    mode='ARRANGEMENT_UNRESOLVED'
                    support_downgrades.append(i)
            raw={**raw,'mode':mode}
            if mode=='ASSISTED_COMPONENT_PRACTICE':
                # Do not silently treat the other person's modeled time as
                # free. Participation in a repeated shared arrangement uses
                # the supporter's own finite hours as well. The prior
                # coactivity trace is only a *warrant* for a provisional
                # aggregate, not proof of consent on every unrendered day.
                fraction_by_actor[supporter]=(
                    fraction_by_actor.get(supporter,0.)+hours*fraction)
        normalized.append(copy(raw))
        claims.append((i,raw,lived_source,hours*fraction))
        fraction_by_actor[a]=fraction_by_actor.get(a,0.)+hours*fraction
    over={a:round(x,6) for a,x in fraction_by_actor.items()
          if x>ACTIVE_HOURS+1e-9}
    if over:
        # Explicit historical scenario allocations remain strict. They are
        # fixed premises of this research cut, not a moral priority. If
        # those alone fit, do NOT silently choose among an actor's competing
        # contingent acquired routines. Conserve the unresolved whole set;
        # only later actor-local admission can revise its distribution.
        removed=set()
        for i,raw,lived,amount in claims:
            a=raw['actor']
            if a not in over or not lived:continue
            removed.add(i)
            situationally_withheld.append({'input_index':i,'source_ref':raw['source_ref'],
                'actor':a,'location':raw['location'],'start_clock':start_clock,
                'end_clock':start_clock+days,'reason':'UNRESOLVED_COMPETING_ROUTINE_TIME_CLAIMS',
                'total_modeled_actor_hours_claimed_per_day':over[a],
                'daily_active_hour_ceiling':ACTIVE_HOURS,'proposed_routine':copy(raw),
                'unexecuted_premise_not_missed_duty_or_sensed_event':True,
                'no_choice_between_routines_or_actor_knowledge_inferred':True})
            fraction_by_actor[a]-=amount
        still_over={a for a,x in fraction_by_actor.items() if x>ACTIVE_HOURS+1e-9}
        if still_over:
            raise ValueError('HISTORICAL_TIME_OVERBOOKED_ACTOR:'+','.join(sorted(still_over)))
        normalized=[copy(raw) for i,raw,_,_ in claims if i not in removed]
    return {
        'qualified':normalized,
        **({'structurally_withheld_processes':withheld} if withheld else {}),
        **({'bodily_withheld_processes':bodily_withheld} if bodily_withheld else {}),
        **({'situationally_withheld_processes':situationally_withheld} if situationally_withheld else {}),
        'actor_active_hour_claim_per_day':{
            a:round(h,5) for a,h in sorted(fraction_by_actor.items())},
        'unmodeled_free_hours_per_day':{
            a:round(max(0,ACTIVE_HOURS-h),5)
            for a,h in sorted(fraction_by_actor.items())},
        'support_downgraded_to_unresolved_indices':support_downgrades,
        'daily_time_cap_hours':DAY_HOURS,
        'provisional_rest_reserve_hours':PROVISIONAL_REST_RESERVE,
        'assumed_same_site_through_period':True,
        'no_unobserved_coactor_choices_invented':True,
        'not_empirical_time_use_validation':True,
        'start_clock':start_clock,'days':days,'grade':GRADE,
    }


def _care(world,actors,proc,start,days):
    a=proc['actor'];r=proc['recipient'];site=proc['location']
    hours=proc['hours_per_active_day']*proc[
        'provisional_exposure_fraction']*days
    # Routine work is not an explicit sequence of care actions; this is a
    # modeled resource/bodily consequence with distinct cost-bearers.
    giver=actors[a]['body'];recipient=actors[r]['body']
    fatigue=round(min(.12,hours*.00012),5)
    benefit=round(min(.10,hours*.00018),5)
    giver['rest']=max(.02,round(giver['rest']-fatigue,5))
    comfort_before=recipient['comfort']
    recipient['comfort']=min(1.,round(comfort_before+benefit,5))
    actual_bodily_effect=round(recipient['comfort']-comfort_before,5)
    ref=stable_id('aggregate_reproductive_care',{
        'world':world['id'],'giver':a,'recipient':r,
        'source':proc['source_ref'],'start':start,'days':days})
    row={
        'id':ref,'start_clock':start,'end_clock':start+days,
        'site':site,'giver':a,'recipient':r,
        'source_ref':proc['source_ref'],
        'modeled_labor_hours':round(hours,3),
        'giver_rest_expenditure_model':fatigue,
        'recipient_comfort_effect_model':actual_bodily_effect,
        'modeled_proposed_relief_before_bodily_saturation':benefit,
        'wage_opportunity_cost':'NOT_INFERRED_FROM_CARE_ALONE',
        'unprovided_other_care':'UNKNOWN',
        'actor_gratitude_or_love':'NOT_INFERRED',
        'no_individually_observed_care_events':True,
        'grade':'SOURCEFREE_QUALIFIED_AGGREGATE_CARE'}
    world.setdefault('reproductive_labor_periods',[]).append(row)
    # History must be available to the recipient's next psychic reader; the
    # caregiver's world labor cost is NOT automatically a child's conscious
    # attribution of where comfort came from.
    conserve_received_period_care(actors[r],row)
    return row


def _work(world,actors,proc,start,days):
    a=proc['actor'];site=proc['location']
    actual_site=world['sites'][site]
    controller=actual_site['controller']
    institution=world['institutions'][controller]
    wage=_number(institution.get('wage'),'WORKSITE_WAGE')
    hours=proc['hours_per_active_day']*proc[
        'provisional_exposure_fraction']*days
    # Explicitly provisional 8-hour-normalized period claim, not a verified
    # historical labor productivity/wage law. The world does not invent goods
    # it did not model. Actual creditor account and employer account differ.
    owed=round(hours/8*wage,5)
    cash=_number(world.get('accounts',{}).get(controller,0),
                 'EMPLOYER_BALANCE')
    paid=round(min(owed,cash),5)
    unpaid=round(max(0,owed-paid),5)
    # The source-qualified activity consumes bodily capacity even if the
    # controller cannot pay. Hours reserved outside modeled activity are
    # not actual rest. Use the existing care model's provisional hourly
    # coefficient, without its per-period cap (which would make wage
    # load depend on arbitrary partition). This is not a medical rate.
    body=actors[a]['body']
    from .organism import eligible
    eligible(body,'WAIT')  # validate; do not equate a period with a micro-act
    rest_before=body['rest']
    nominal_load=round(hours*.00012,5)
    rest_after=round(max(0.,rest_before-nominal_load),5)
    body['rest']=rest_after
    world['accounts'][controller]=round(cash-paid,5)
    world['accounts'][a]=round(_number(
        world['accounts'].get(a,0),'WORKER_BALANCE')+paid,5)
    ref=stable_id('aggregate_wage_work',{
        'world':world['id'],'worker':a,'controller':controller,
        'source':proc['source_ref'],'start':start,'days':days})
    row={
        'id':ref,'source_ref':proc['source_ref'],
        'start_clock':start,'end_clock':start+days,
        'worker':a,'controller':controller,'site':site,
        'modeled_labor_hours':round(hours,3),
        'worker_rest_before_modeled_work':rest_before,
        'worker_rest_after_modeled_work':rest_after,
        'worker_rest_expenditure_model':round(rest_before-rest_after,5),
        'nominal_bodily_load_model':nominal_load,
        'rest_recovery_in_unmodeled_hours':'NOT_INFERRED',
        'wage_due_sourcefree_model':owed,
        'actual_paid_model':paid,'wage_arrears':unpaid,
        'physical_goods_output':'NOT_INFERRED_WITHOUT_MATERIAL_PRODUCTION_MODEL',
        'worker_control_of_output':'NOT_CONFERRED_BY_WAGE',
        'no_observed_individual_work_events':True,
        'grade':'SOURCEFREE_QUALIFIED_AGGREGATE_WAGE'}
    world.setdefault('wage_labor_periods',[]).append(row)
    if unpaid>0:
        world.setdefault('wage_arrears',[]).append({
            'aggregate_labor_ref':ref,'worker':a,'controller':controller,
            'amount':unpaid,'period_end_clock':start+days})
    return row


def apply_period_allocation(world,actors,allocation):
    """Actual world/bodily result for one already-qualified history window.

    Caller uses copy-on-write ledger; call once per registered period.
    Results do NOT automatically become conscious autobiographical memories.
    """
    if allocation.get('grade')!=GRADE:
        raise ValueError('HISTORICAL_TIME_UNQUALIFIED_ALLOCATION')
    start=allocation['start_clock'];days=allocation['days']
    if world['clock']!=start:
        raise ValueError('HISTORICAL_TIME_WORLD_ADVANCED_BEFORE_SETTLEMENT')
    ref=stable_id('historical_time_allocation',{
        'world':world['id'],'start':start,'days':days,
        'processes':allocation['qualified'],
        **({'structurally_withheld_processes':allocation['structurally_withheld_processes']}
           if allocation.get('structurally_withheld_processes') else {}),
        **({'bodily_withheld_processes':allocation['bodily_withheld_processes']}
           if allocation.get('bodily_withheld_processes') else {}),
        **({'situationally_withheld_processes':allocation['situationally_withheld_processes']}
           if allocation.get('situationally_withheld_processes') else {})})
    if any(r.get('id')==ref for r in
           world.get('historical_time_allocations',[])):
        raise ValueError('HISTORICAL_TIME_DUPLICATE_SETTLEMENT')
    care=[];wages=[]
    # All qualification and per-person time budgets are checked before writes.
    for proc in allocation['qualified']:
        if proc['kind']=='QUALIFIED_REPRODUCTIVE_CARE':
            care.append(_care(world,actors,proc,start,days))
        elif proc['kind']=='QUALIFIED_WAGE_LABOR':
            wages.append(_work(world,actors,proc,start,days))
    provisioned=settle_provisioning(world,actors,allocation)
    receipt={
        'id':ref,'start_clock':start,'end_clock':start+days,
        'actor_hour_claims_per_day':copy(
            allocation['actor_active_hour_claim_per_day']),
        'free_hours_per_day_after_modeled_claims':copy(
            allocation['unmodeled_free_hours_per_day']),
        'care_period_refs':[x['id'] for x in care],
        'wage_period_refs':[x['id'] for x in wages],
        'material_feeding_period_refs':[x['id'] for x in provisioned],
        'material_feeding_shortfall_refs':[
            x['id'] for x in provisioned if x['uncovered_food_units']>0],
        'source_qualified_process_refs':[
            x['source_ref'] for x in allocation['qualified']],
        'support_downgraded_to_unresolved_indices':copy(
            allocation['support_downgraded_to_unresolved_indices']),
        **({'structurally_withheld_processes':copy(allocation['structurally_withheld_processes'])}
           if allocation.get('structurally_withheld_processes') else {}),
        **({'bodily_withheld_processes':copy(allocation['bodily_withheld_processes'])}
           if allocation.get('bodily_withheld_processes') else {}),
        **({'situationally_withheld_processes':copy(allocation['situationally_withheld_processes'])}
           if allocation.get('situationally_withheld_processes') else {}),
        'absent_high_resolution_scenes':'NOT_DEEMED_TO_HAVE_OCCURRED',
        'work_and_care_bearer_differentiation':True,
        'not_a_human_time_use_or_developmental_law':True,
        'grade':GRADE}
    world.setdefault('historical_time_allocations',[]).append(receipt)
    return receipt
