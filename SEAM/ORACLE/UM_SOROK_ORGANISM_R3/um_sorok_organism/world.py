"""Independent objective world with material effects and separately authored coactivity.
World consequences can be unilateral, imposed, cooperative, or refused.
"""
from .types import Attempt, Resolution, copy, stable_id, digest
from .organism import eligible
from dataclasses import asdict
import hmac, hashlib, os, json, math

COOPERATIVE={'SIGNAL':{'CARE','JOIN'},'SING':{'JOIN','SING','MAKE_SPACE'},'PRACTICE':{'CARE','JOIN','MAKE_SPACE'},
             'MAKE_SPACE':{'JOIN','SING'},'SHARE':{'JOIN','CARE'}}


def add_cue(world,kind,tags,location='all',modality='visual',description='',source_actor=None,
            private_to=None,threshold=.05,clock_offset=0,lasting_ticks=0):
    moment=world['clock']+clock_offset
    cue={'clock':moment,'last_access_clock':moment+lasting_ticks,'id':stable_id('cue',{'n':world['clock'],'tags':tags,'s':source_actor,'d':description,'index':len(world['cues'])}),
         'kind':kind,'tags':list(tags),'location':location,'modality':modality,
         'description':description or kind,'source_actor':source_actor,
         'private_to':private_to,'threshold':threshold}
    world['cues'].append(cue)
    return cue


def _field(world,a,b):
    ids=sorted((a,b));key='rel:'+':'.join(ids)
    return world['relations'].setdefault(key,{'id':key,'participants':ids,
       'history':[],'joint_capabilities':[],'observed_patterns':[], 'constraints':[],
       'continuity':'open','objective_grade':'SOURCEFREE_RESEARCH_PROVISIONAL'})


def _site(world,aid):return world['sites'].get(world['positions'].get(aid),{})

def _effective_material_controller(world, loc, site):
    """Resolve actual institutional control, including non-denormalized sites.

    A site may omit a controller label while an independent institution still
    controls it (e.g. the hall board). Missing/conflicting declarations must
    never turn controlled material into free stock.
    """
    controllers=[name for name,inst in world['institutions'].items()
                 if inst.get('controls')==loc]
    named=site.get('controller')
    if named is not None and (named not in controllers or len(controllers)!=1):
        return None,True
    if len(controllers)>1:
        return None,True
    return (named or (controllers[0] if controllers else None)),False


def _nonnegative_transfer_amount(raw, error):
    """Reject invalid fixture economics before world/actor mutations.

    Research accounts are money claims, not a market law or policy scheduler.
    An invalid negative or nonfinite amount cannot mint money, seize worker
    balances, or poison canonical ledger serialization.
    """
    # Bool is int in Python but not an objective quantity; accepting True as
    # a wage or price creates fictional monetary claims. Sourcefree world
    # receipts use explicit finite numeric inputs rather than coerced strings.
    if isinstance(raw,bool) or not isinstance(raw,(int,float)):
        raise ValueError(error)
    try:
        amount = float(raw)
    except (TypeError, ValueError, OverflowError):
        raise ValueError(error) from None
    if not math.isfinite(amount) or amount < 0:
        raise ValueError(error)
    return amount



def _cash_amount(raw,error):
    """A monetary claim must survive declared five-decimal storage exactly.

    A positive subtick price/wage must not round to zero and transfer goods or
    erase owed compensation. Nonrepresentable balances must not mint value on
    the next transfer. This rejects, rather than silently rounds, input. Not a
    claim that the sourcefree model has real-world currency-calibration rights.
    """
    amount=_nonnegative_transfer_amount(raw,error)
    if amount != round(amount,5):
        raise ValueError(error+'_PRECISION')
    return amount


def _resolve_untrusted_core(world,actors,attempt:Attempt,partner_attempt:Attempt|None=None):
    """Contributions must be independently supplied by a trusted runtime planner.
    The world never accepts a caller-provided consent boolean. Consent is not
    required for IMPOSITION; imposed consequences do not imply willing contribution.
    """
    aid=attempt.actor
    if aid not in actors or aid not in world['positions']:
        raise ValueError('UNREGISTERED_ACTOR')
    if partner_attempt and (partner_attempt.actor==aid or partner_attempt.actor not in actors):
        raise ValueError('FORGED_COACTOR_IDENTITY')
    loc=world['positions'][aid]
    actor=actors[aid]
    allowed,reason=eligible(actor['body'],attempt.action)
    performed=[];effects={aid:{'action':attempt.action,'bodily':True}}
    status='PERFORMED' if allowed else 'BLOCKED'
    output=''
    target=attempt.target
    partner_valid=False
    if partner_attempt:
        ok,why=eligible(actors[partner_attempt.actor]['body'],partner_attempt.action)
        partner_valid=(ok and world['positions'].get(partner_attempt.actor)==loc)
        performed.append({'actor':partner_attempt.actor,'action':partner_attempt.action,
                         'status':'PERFORMED' if partner_valid else 'BLOCKED',
                         'as_willing':'REFUSE' not in partner_attempt.action})
        effects[partner_attempt.actor]={'action':partner_attempt.action,'bodily':partner_valid}
    performed.insert(0,{'actor':aid,'action':attempt.action,'status':status,'as_willing':True})
    if not allowed:
        output='BODILY_'+reason
    elif attempt.action in ('EAT','BUY_FOOD','WORK','REPAIR') and loc not in world['sites']:
        # No phantom production on detached dict returned by _site().
        status='BLOCKED';output='UNKNOWN_MATERIAL_SITE'
    elif attempt.action=='MOVE':
        if attempt.object_ref in world['sites']:
            site=world['sites'][attempt.object_ref]
            if site['access']=='public' or aid in site.get('admitted',[]):
                world['positions'][aid]=attempt.object_ref;actor['location']=attempt.object_ref
                output='MOVED'
            else:status='BLOCKED';output='INSTITUTIONAL_ACCESS_DENIED'
        else:status='BLOCKED';output='UNKNOWN_DESTINATION'
    elif attempt.action=='EAT':
        site=_site(world,aid)
        inventory=world.setdefault('holdings',{}).setdefault(aid,{'food':0})
        owned=_nonnegative_transfer_amount(inventory.get('food',0),'INVALID_OWNED_FOOD')
        household=_nonnegative_transfer_amount(site.get('food',0),'INVALID_SITE_FOOD')
        if owned>=1:
            inventory['food']=owned-1;output='ATE_OWNED_FOOD'
        elif loc=='home' and household>=1:
            site['food']=household-1;output='ATE_SHARED_HOUSEHOLD_FOOD'
        else:status='BLOCKED';output='NO_ACCESSIBLE_FOOD'
    elif attempt.action=='BUY_FOOD':
        site=_site(world,aid)
        cost=_cash_amount(site.get('food_price',1.0), 'INVALID_MATERIAL_PRICE')
        available_food=_nonnegative_transfer_amount(site.get('food',0),'INVALID_SITE_FOOD')
        buyer_balance=_cash_amount(world['accounts'].get(aid,0),'INVALID_BUYER_BALANCE')
        owned_food=_nonnegative_transfer_amount(world.get('holdings',{}).get(aid,{}).get('food',0),
                                                'INVALID_OWNED_FOOD')
        # Ownership of offered goods and the monetary recipient must be
        # objective world relations. Charging the buyer without recording who
        # received the payment destroyed purchasing claims inside the modeled
        # economy. A room with food but no identifiable seller is NOT a shop.
        seller,controller_error=_effective_material_controller(world,loc,site)
        if available_food<1:status='BLOCKED';output='NO_FOOD_TO_PURCHASE'
        elif buyer_balance<cost:status='BLOCKED';output='INSUFFICIENT_CLAIM_ON_FOOD'
        elif controller_error:status='BLOCKED';output='MATERIAL_CONTROLLER_UNQUALIFIED'
        elif seller is None:status='BLOCKED';output='NO_OBJECTIVE_SELLER'
        else:
            seller_balance=_cash_amount(
                world['accounts'].get(seller,0),'INVALID_SELLER_BALANCE')
            paid=round(cost,5)
            if buyer_balance<paid:status='BLOCKED';output='INSUFFICIENT_CLAIM_ON_FOOD'
            else:
                site['food']=available_food-1
                if seller!=aid:
                    world['accounts'][aid]=round(buyer_balance-paid,5)
                    world['accounts'][seller]=round(seller_balance+paid,5)
                world.setdefault('holdings',{}).setdefault(aid,{'food':0})['food']=owned_food+1
                world.setdefault('material_claims',[]).append({
                    'clock':world['clock'],'kind':'FOOD_PURCHASE',
                    'buyer':aid,'site':loc,'seller':seller,'price_paid':paid,
                    'goods_transferred':1,'not_actor_psychic_motive':True})
                output='FOOD_PURCHASED'
    elif attempt.action=='WORK':
        site=_site(world,aid);controller,unqualified=_effective_material_controller(world,loc,site)
        stock=_nonnegative_transfer_amount(site.get('stock',0),'INVALID_SITE_STOCK')
        if unqualified:
            # Neither a missing issuer nor a mismatched owner converts an
            # institutionally controlled worksite into unowned production.
            status='BLOCKED';output='MATERIAL_CONTROLLER_UNQUALIFIED'
        elif controller is not None:
            institution=world['institutions'][controller]
            wage=_cash_amount(institution.get('wage',0), 'INVALID_WAGE')
            available=_cash_amount(world['accounts'].get(controller,0),
                                                      'INVALID_CONTROLLER_BALANCE')
            worker_balance=_cash_amount(world['accounts'].get(aid,0),
                                                      'INVALID_WORKER_BALANCE')
            # Precise within research account's declared five-decimal units.
            due=round(wage,5)
            paid=round(min(round(available,5),due),5)
            unpaid=round(max(0,due-paid),5)
            # Validation and controller relation precede every material write.
            site['stock']=stock+2
            world['accounts'][controller]=round(available-paid,5)
            world['accounts'][aid]=round(worker_balance+paid,5)
            claim={'clock':world['clock'],'worker':aid,'site':loc,'goods_produced':2,
                   'controller':controller,'wage':paid,'wage_due':due,
                   'wage_unpaid':unpaid,'worker_control_of_output':False}
            world.setdefault('material_claims',[]).append(claim)
            if unpaid>0:
                # A lack of cash does not erase an objectively configured wage
                # claim. This is an employer liability, not a worker's belief.
                world.setdefault('wage_arrears',[]).append({'clock':world['clock'],
                    'worker':aid,'controller':controller,'site':loc,
                    'amount':unpaid,'material_claim_index':len(world['material_claims'])})
            output='PRODUCED_GOODS_CONTROLLED_BY_OTHER'
        else:
            # No controller exists: this is not a wage relationship.
            site['stock']=stock+2
            output='MATERIAL_STOCK_PRODUCED'
    elif attempt.action=='REPAIR':
        site=_site(world,aid);controller,unqualified=_effective_material_controller(world,loc,site)
        stock=_nonnegative_transfer_amount(site.get('stock',0),'INVALID_SITE_STOCK')
        if unqualified:
            status='BLOCKED';output='MATERIAL_CONTROLLER_UNQUALIFIED'
        elif controller is not None and aid not in site.get('material_use_grants',[]):
            # Public entrance ≠ the right to appropriate a controller's goods.
            # Grant is an objective world/site relation, never actor assertion.
            status='BLOCKED';output='MATERIAL_USE_NOT_AUTHORIZED'
        elif stock<1:
            status='BLOCKED';output='MISSING_REPAIR_MATERIAL'
        else:
            site['stock']=stock-1;output='REPAIR_PERFORMED'
    elif attempt.action=='OPEN_HALL':
        members=world['institutions']['hall_board']['members']
        if aid not in members:status='BLOCKED';output='NO_INSTITUTIONAL_AUTHORITY'
        else:
            world['sites']['hall']['access']='public';output='HALL_OPENED'
    elif attempt.action=='DENY_HALL':
        members=world['institutions']['hall_board']['members']
        if aid not in members:status='BLOCKED';output='NO_INSTITUTIONAL_AUTHORITY'
        else:world['sites']['hall']['access']='controlled';output='HALL_ACCESS_RESTRICTED'
    elif attempt.action=='CARE':
        if target in actors and world['positions'].get(target)==loc:
            b=actors[target]['body'];b['comfort']=min(1,b['comfort']+.18)
            b['nutrition']=min(1,b['nutrition']+.06)
            effects[target]={'action':'RECEIVED_CARE','bodily':True}
            output='CARE_GIVEN'
        else:status='PARTIAL';output='CARE_TARGET_ABSENT'
    elif attempt.action=='IMPOSE':
        if target in actors and world['positions'].get(target)==loc:
            effects[target]={'action':'IMPOSED_ON','bodily':False}
            output='UNILATERAL_IMPOSITION_NOT_CONSENT'
        else:status='BLOCKED';output='TARGET_NOT_PRESENT'
    elif attempt.action in COOPERATIVE and target:
        if partner_attempt and partner_attempt.actor==target and partner_valid and partner_attempt.action in COOPERATIVE[attempt.action]:
            field=_field(world,aid,target)
            joint={'clock':world['clock'],'activity':attempt.action,
                    'contributions':[{'actor':aid,'act':attempt.action},
                                     {'actor':target,'act':partner_attempt.action}],
                    'material_effects':[]}
            if attempt.action=='SIGNAL' and partner_attempt.action=='CARE':
                # Distinct autonomous contributions jointly produce regulation.
                # No presumed praise/recognition/attachment or human-law claim.
                b=actors[aid]['body'];before=b['comfort']
                b['comfort']=min(1.0,b['comfort']+.12)
                b['arousal']=max(0.0,b['arousal']-.12)
                joint['material_effects'].append({'recipient':aid,
                    'kind':'CONTINGENT_CARE_REGULATION','comfort_before':before,
                    'comfort_after':b['comfort']})
                effects[aid]['received_assistance']=True
            field['history'].append(joint)
            # PFF noncollapse: two co-occurrences are evidence of repetition,
            # NOT proof of learned relational capability, love, recognition,
            # or a stable social attractor. Keep observed pattern distinct.
            if len(field['history'])>=2 and 'REPEATED_JOINT_ACT_OBSERVED' not in field['observed_patterns']:
                field['observed_patterns'].append('REPEATED_JOINT_ACT_OBSERVED')
            output='JOINT_ACTIVITY_PERFORMED'
        else:
            status='PARTIAL';output='INDEPENDENT_COACTOR_DID_NOT_JOIN'
    elif attempt.action in ('SING','PRACTICE','MAKE_SPACE'):
        output='SOLO_PRACTICE'
    elif attempt.action=='SIGNAL':
        output='NONVERBAL_SIGNAL'
    elif attempt.action=='SPEAK':
        output='SPEECH_PERFORMED'
    elif attempt.action=='ASK':
        output='REQUEST_EXPRESSED_NOT_AUTOMATICALLY_ACCEPTED'
    elif attempt.action=='REFUSE':output='ACTOR_REFUSED'
    elif attempt.action=='REST':output='BODY_RESTED'
    elif attempt.action=='ORIENT':output='ORIENTING_PERFORMED'
    elif attempt.action=='INSPECT':output='INSPECTION_PERFORMED'
    elif attempt.action=='WAIT':output='INACTION_OR_WAIT'
    else:output='ACT_COMPLETED'
    performed[0]['status']=status
    world['clock']+=1
    # A receipt may only identify a material claim if this action really
    # produced one; a blocked WORK attempt or a non-employer site does not.
    last_claim=world.get('material_claims',[])[-1] if world.get('material_claims') else None
    claim_ref=(len(world['material_claims']) if attempt.action=='WORK' and
               output=='PRODUCED_GOODS_CONTROLLED_BY_OTHER' and last_claim and
               last_claim['worker']==aid and last_claim['clock']==world['clock']-1
               else None)
    event_summary={'clock':world['clock'],'actor':aid,'action':attempt.action,
                   'target':target,'outcome':output,'status':status,
                   'coactor':partner_attempt.actor if partner_attempt else None,
                   'coactor_action':partner_attempt.action if partner_attempt else None,
                   'object_ref':attempt.object_ref,
                   'material_claim_ref':claim_ref,
                   'co_present_not_verified_witnessing':True}
    # Objective event audit contains the real resolution, but public history
    # must not publish the actor's private financial/material explanation.
    # A blocked act is observable as an unfinished attempt, not an accounting diagnosis.
    perceptible_outcome=(output if status=='PERFORMED' else 'ATTEMPT_NOT_COMPLETED')
    public_event={**event_summary,'outcome':perceptible_outcome}
    world['public_history'].append(public_event)
    # New cues are actual public world consequences, not actor introspection.
    # World effects persist even when no participant currently perceives them.
    # Public, witness-accessible sign is not a world-audit report. A refused
    # purchase, for example, does not reveal the purchaser's account deficit.
    add_cue(world,'performed_'+attempt.action.lower(),
            [attempt.action.lower(),perceptible_outcome.lower()],
            location=loc,modality='auditory' if attempt.action in ('SING','SPEAK','SIGNAL','ASK') else 'visual',
            description=perceptible_outcome,source_actor=aid)
    witnesses=[a for a in actors if world['positions'].get(a)==loc]
    return Resolution(status,performed,{'event':event_summary},effects,witnesses,output)


class IndependentWorldAuthority:
    """Research world entrypoint: independently plan any prospective coactor.

    A caller may request a joint activity by targeting another actor. It may NOT
    supply that actor's voluntary response, a consent Boolean, or a forged
    attempt receipt. The decision is issued by the owner's registered policy
    from the other actor's own committed state. This is an API trust boundary,
    not an OS/Python security sandbox against malicious in-process callers.
    """
    def __init__(self, coactor_planner):
        if not callable(coactor_planner):raise TypeError('QUALIFIED_COACTOR_PLANNER_REQUIRED')
        self.__planner=coactor_planner

    def resolve(self,world,actors,principal:Attempt):
        if principal.actor not in actors:raise ValueError('UNREGISTERED_ACTOR')
        partner=None;policy_receipt=None
        if (principal.action in COOPERATIVE and principal.target in actors
                and principal.target!=principal.actor and
                world['positions'].get(principal.actor)==world['positions'].get(principal.target)):
            candidate=self.__planner(principal,copy(world),copy(actors))
            if not isinstance(candidate,Attempt) or candidate.actor!=principal.target:
                raise ValueError('INDEPENDENT_COACTOR_POLICY_INVALID')
            if candidate.action not in COOPERATIVE[principal.action]|{'REFUSE'}:
                raise ValueError('INDEPENDENT_COACTOR_NOT_ELIGIBLE_TO_JOIN')
            ok,reason=eligible(actors[candidate.actor]['body'],candidate.action)
            if not ok:raise ValueError('COACTOR_BODILY_INELIGIBLE:'+reason)
            partner=candidate
            policy_receipt={'coactor':partner.actor,'action':partner.action,
                'actor_state_hash':digest(actors[partner.actor]),
                'world_state_hash':digest(world),'plan_basis':copy(partner.basis),
                'policy_grade':'SOURCEFREE_INDEPENDENT_ACTOR_PROSPECTIVE'}
        out=_resolve_untrusted_core(world,actors,principal,partner)
        return out,partner,policy_receipt


def resolve(*args,**kwargs):
    """Deprecated direct function: solo only. The trusted research runtime
    uses IndependentWorldAuthority with an installed other-actor policy.
    """
    if kwargs.get('partner_attempt') is not None or len(args)>=4 and args[3] is not None:
        raise ValueError('DIRECT_COACTOR_BYPASS_REFUSED')
    return _resolve_untrusted_core(*args,**kwargs)
