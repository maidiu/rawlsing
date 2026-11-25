"""Independent objective world with material effects and separately authored coactivity.
World consequences can be unilateral, imposed, cooperative, or refused.
"""
from .types import Attempt, Resolution, copy, stable_id, digest
from .organism import eligible
from .institutional_reproduction import (
    contribute_to_hall_petition, retain_material_care)
from .material_conjunction import evaluate_material_conjunction
from .practical_inquiry import notices_present
from .material_objects import (
    produce_artifact, repair_artifact, material_objects_present)
from .mediated_efficacy import objective_arrangement
from .expectation_afterlife import realized_vocal_cadence, CADENCES
from .material_provisioning import perform_one_actual_feeding
from .food_access_struggle import (
    contribute_food_petition,can_draw_shared_food)
from .food_power_reproduction import (
    INSTALL,MAINTAIN,SANCTION,COMMONS,install_gate,
    maintain_gate,sanction_gate,contribute_food_commons,
    OFFER,ACCEPT,offer_control_transfer,accept_control_transfer)
from .labor_dependency import (
    ACCEPT as WORK_ACCEPT,SUSPEND as WORK_SUSPEND,RESIGN as WORK_RESIGN,
    CONTRIBUTE as WORK_POOL,DRAW as WORK_DRAW,
    accept_work_terms,suspend_worker,withdraw_labor,
    fund_worker_relief,draw_worker_relief,work_permission)
from dataclasses import asdict
import hmac, hashlib, os, json, math
from decimal import Decimal

COOPERATIVE={'SIGNAL':{'CARE','JOIN','FEED','SPEAK'},'SING':{'JOIN','SING','MAKE_SPACE'},'PRACTICE':{'CARE','JOIN','MAKE_SPACE'},
             'MAKE_SPACE':{'JOIN','SING'},'SHARE':{'JOIN','CARE'}}


def add_cue(world,kind,tags,location='all',modality='visual',description='',source_actor=None,
            private_to=None,threshold=.05,clock_offset=0,lasting_ticks=0):
    # Objective sensory records become actor-accessible, possibly influencing
    # future recruitment. Reject malformed observations before any world write:
    # list('care') is not the single cue 'care', and an untyped 'present'
    # modality must not bypass an organism's sensory threshold.
    if not isinstance(kind,str) or not kind:
        raise ValueError('INVALID_CUE_KIND')
    if (not isinstance(tags,list) or any(not isinstance(t,str) or not t for t in tags)):
        raise ValueError('INVALID_CUE_TAGS')
    if modality not in ('visual','auditory','tactile','olfactory'):
        raise ValueError('INVALID_CUE_MODALITY')
    if (isinstance(threshold,bool) or not isinstance(threshold,(int,float)) or
            not math.isfinite(threshold) or not 0<=threshold<=1):
        raise ValueError('INVALID_CUE_THRESHOLD')
    if (type(lasting_ticks) is not int or lasting_ticks<0 or
            type(clock_offset) is not int or clock_offset<0):
        raise ValueError('INVALID_CUE_TIME')
    if not isinstance(location,str) or not location:
        raise ValueError('INVALID_CUE_LOCATION')
    if private_to is not None and (not isinstance(private_to,str) or not private_to):
        raise ValueError('INVALID_CUE_PRIVATE_ACTOR')
    moment=world['clock']+clock_offset
    cue={'clock':moment,'last_access_clock':moment+lasting_ticks,'id':stable_id('cue',{'n':world['clock'],'tags':tags,'s':source_actor,'d':description,'index':len(world['cues'])}),
         'kind':kind,'tags':list(tags),'location':location,'modality':modality,
         'description':description or kind,'source_actor':source_actor,
         'private_to':private_to,'threshold':threshold}
    world['cues'].append(cue)
    return cue



# Source adaptation: NEIGHBOR R6 neighbor_runtime.sensory_evidence,
# exact donor 3dd615548bdce06de0ec1f173a3c5089e1345da7,
# blob 30192d5c927e52c3a8256f5a5ab8ebd0a17e0080 (P6/MIII-derived).
# Unlike visitor ingress, this reader concerns two constituted actors.
# Directional paths are explicitly fictional WORLD conditions, not inferred
# by a semantic proposal, a viewer's private gaze, or actor co-presence.

def register_recursive_encounter_paths(world, actors, spec):
    """Install finite, directed material paths in the existing world owner."""
    if (type(spec) is not dict or set(spec)!={'grade','source_ref','paths'}
            or spec['grade']!='SOURCEFREE_TEST_ONLY'
            or type(spec['source_ref']) is not str or not spec['source_ref']
            or type(spec['paths']) is not list or not 1<=len(spec['paths'])<=256):
        raise ValueError('ENCOUNTER_PATH_SOURCE_UNQUALIFIED')
    fields={'observer','source_actor','location','from_clock','through_clock',
            'hearing','sound_path','visual','light','sightline','facing'}
    history=world.get('recursive_encounter_paths',[])
    if type(history) is not list:
        raise ValueError('ENCOUNTER_PATH_HISTORY_INVALID')
    prepared=[]
    for row in spec['paths']:
        if type(row) is not dict or set(row)!=fields:
            raise ValueError('ENCOUNTER_PATH_INVALID_FIELDS')
        observer=row['observer']; source=row['source_actor']
        start=row['from_clock']; end=row['through_clock']
        if (type(observer) is not str or type(source) is not str
                or observer==source or observer not in actors or source not in actors
                or type(row['location']) is not str
                or row['location'] not in world['sites']
                or type(start) is not int or type(end) is not int
                or start<world['clock'] or not start<=end<=start+3650
                or type(row['hearing']) is not bool or type(row['visual']) is not bool
                or row['sound_path'] not in ('audible','blocked','unknown')
                or row['light'] not in ('lit','dark','unknown')
                or row['sightline'] not in ('unobstructed','partial','blocked','unknown')
                or row['facing'] not in ('source','away','unknown')):
            raise ValueError('ENCOUNTER_PATH_INVALID_CONDITION')
        for prior in history+prepared:
            if (all(prior.get(k)==row[k] for k in (
                    'observer','source_actor','location'))
                    and max(prior['from_clock'],start)<=min(prior['through_clock'],end)):
                raise ValueError('ENCOUNTER_PATH_OVERLAPPING_SOURCE')
        sealed=copy(row)
        sealed.update({'source_ref':spec['source_ref'],'grade':spec['grade'],
                       'id':stable_id('recursive_sensory_path',{
                           'world':world['id'],'source_ref':spec['source_ref'],'path':row})})
        prepared.append(sealed)
    world.setdefault('recursive_encounter_paths',[]).extend(prepared)
    return {'path_refs':[row['id'] for row in prepared],
            'source_ref':spec['source_ref'],
            'not_actor_exposure_or_attention':True,'grade':spec['grade']}


def recursive_encounter_channels(world, observer, source, location):
    """Pure directional channel read; None preserves the inherited coarse gate.

    A missing active path is UNKNOWN at the original approximation grade,
    not proof of sound or visibility. An explicit blocked/unknown channel
    does not qualify access. The read is anchored in current world time.
    """
    if source==observer or source is None:
        return None
    matches=[p for p in world.get('recursive_encounter_paths',[])
             if p.get('observer')==observer and p.get('source_actor')==source
             and p.get('location')==location
             and p['from_clock']<=world['clock']<=p['through_clock']]
    if not matches:return None
    if len(matches)!=1 or matches[0].get('grade')!='SOURCEFREE_TEST_ONLY':
        raise ValueError('ENCOUNTER_PATH_AMBIGUOUS_OR_UNQUALIFIED')
    p=matches[0]
    return {'path_ref':p['id'],
            'audible':p['hearing'] is True and p['sound_path']=='audible',
            'visible':p['visual'] is True and p['light']=='lit'
                and p['sightline']=='unobstructed' and p['facing']=='source'}


def project_recursive_actor_sign(world, actor, cue, location):
    """Adapt NEIGHBOR's auditory/visual distinction to CO's existing cue read.

    Never mutate the world cue. An anonymous auditory sign retains its exact
    objective cue ID for audit but omits source identity, target, outcome and
    referent. This is not proof of actor attention or speaker recognition.
    """
    source=cue.get('source_actor')
    if source==actor['id']:
        return copy(cue)
    channels=recursive_encounter_channels(world,actor['id'],source,location)
    if channels is None:return copy(cue)
    modality=cue.get('modality','visual')
    if modality=='visual' and not channels['visible']:return None
    if modality=='auditory' and not channels['audible']:return None
    # This source qualifies auditory/visual paths only; inherited tactile and
    # olfactory receipts continue under their own coarse access law.
    if modality not in ('visual','auditory'):return copy(cue)
    speech=cue.get('kind') in ('speech','performed_speak','visitor_speech')
    language=actor.get('body',{}).get('language',0)
    if type(language) not in (int,float) or not math.isfinite(language) or not 0<=language<=1:
        raise ValueError('ENCOUNTER_INVALID_LANGUAGE')
    if modality=='auditory' and (not channels['visible'] or (speech and language<.35)):
        # A child can have a real voice encounter without inheriting an adult
        # propositional description. Preserve source identity only when the
        # simultaneous visual channel is qualified, never by sound alone.
        result={k:copy(cue[k]) for k in (
            'id','clock','last_access_clock','location','modality','threshold')
            if k in cue}
        result.update({'kind':'heard_voice' if speech else 'heard_sound',
            'tags':['voice','speech_sound'] if speech else ['sound'],
            'description':'Speech sounds nearby.' if speech else 'A sound nearby.',
            'source_actor':source if channels['visible'] else None,
            'lexical_comprehension':'NOT_ESTABLISHED',
            'source_identity_visually_eligible_not_recognition':channels['visible'],
            'encounter_path_ref':channels['path_ref'],
            'not_actor_attention_or_understanding':True})
        if speech and cue.get('vocal_cadence') in CADENCES:
            result['vocal_cadence']=cue['vocal_cadence']
            result['description']=CADENCES[cue['vocal_cadence']]
        return result
    result=copy(cue)
    result['encounter_path_ref']=channels['path_ref']
    result['not_actor_attention_or_understanding']=True
    # A visible principal does not confer visibility of other participants.
    for field in ('actor_accessible_target_ref',
                  'actor_accessible_care_responder_ref',
                  'actor_accessible_speech_responder_ref'):
        other=result.get(field)
        other_path=recursive_encounter_channels(world,actor['id'],other,location)
        if other_path is not None and not other_path['visible']:
            result.pop(field,None)
    return result


def _field(world,a,b):
    ids=sorted((a,b));key='rel:'+':'.join(ids)
    return world['relations'].setdefault(key,{'id':key,'participants':ids,
       'history':[],'joint_capabilities':[],'observed_patterns':[], 'constraints':[],
       'continuity':'open','objective_grade':'SOURCEFREE_RESEARCH_PROVISIONAL'})


def _qualified_members(owner, field, error):
    """Return only an actual explicit actor-ID roster, never string substring rights.

    These are world-owner permissions; malformed external/fixture types fail
    closed before any site, material, or institutional write. No new powers are
    invented for an actor who merely resembles a listed principal's name.
    """
    members=owner.get(field, [])
    if (not isinstance(members,list) or
            any(not isinstance(member,str) or not member for member in members)):
        raise ValueError(error)
    return members


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


def _exact_material_delta(before, delta, error):
    """Refuse a material transfer that storage cannot actually represent.

    Current sourcefree accounts and inventories use JSON float numbers. Even
    individually finite/rounded balances can lose a real unit on addition or
    subtraction (e.g. 1e20 + 1 == 1e20). Validate the outcome in decimal space
    then require exact preservation through that existing representation.
    This is an integrity guard, NOT a new currency or labor law.
    """
    intended=Decimal(str(before))+Decimal(str(delta))
    if intended<0:
        raise ValueError(error)
    try:
        stored=float(intended)
    except (OverflowError,ValueError):
        raise ValueError(error) from None
    if not math.isfinite(stored) or Decimal(str(stored))!=intended:
        raise ValueError(error)
    return stored


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
    # Structural conditions bite where the world attempts an operation, not
    # as identity scores preloaded into a psychological selector.
    material_gate=evaluate_material_conjunction(world,aid,loc,attempt.action)
    if material_gate['readset']:
        world.setdefault('material_gate_audit',[]).append({
            'clock':world['clock']+1,'actor':aid,
            'operation':attempt.action,
            'objective_rule_evaluation':copy(material_gate),
            'not_actor_self_knowledge':True})
    partner_valid=False
    policy_receipt=None
    care_labor_receipt=None
    material_feeding_ref=None
    future_care_obligation_ref=None
    inspected_public_notice=None
    inspected_material_object=None
    worked_material_object=None
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
    elif material_gate['decision']=='BLOCKED':
        status='BLOCKED';output='STRUCTURAL_RULE_PREVENTED_OPERATION'
    elif material_gate['decision']=='UNRESOLVED':
        status='PARTIAL';output='INSTITUTIONAL_PERMISSION_UNRESOLVED'
    elif attempt.action in ('EAT','BUY_FOOD','WORK','REPAIR') and loc not in world['sites']:
        # No phantom production on detached dict returned by _site().
        status='BLOCKED';output='UNKNOWN_MATERIAL_SITE'
    elif attempt.action=='MOVE':
        if attempt.object_ref in world['sites']:
            site=world['sites'][attempt.object_ref]
            if (site['access']=='public' or aid in _qualified_members(site,'admitted','INVALID_SITE_ADMISSION')):
                world['positions'][aid]=attempt.object_ref;actor['location']=attempt.object_ref
                output='MOVED'
            else:status='BLOCKED';output='INSTITUTIONAL_ACCESS_DENIED'
        else:status='BLOCKED';output='UNKNOWN_DESTINATION'
    elif attempt.action=='EAT':
        site=_site(world,aid)
        inventory=world.get('holdings',{}).get(aid,{'food':0})
        owned=_nonnegative_transfer_amount(inventory.get('food',0),'INVALID_OWNED_FOOD')
        household=_nonnegative_transfer_amount(site.get('food',0),'INVALID_SITE_FOOD')
        if owned>=1:
            next_owned=_exact_material_delta(owned,-1,'INVALID_OWNED_FOOD_DELTA')
            world.setdefault('holdings',{}).setdefault(aid,{'food':0})['food']=next_owned
            output='ATE_OWNED_FOOD'
        elif _nonnegative_transfer_amount(
                site.get('mutual_aid_food',0),
                'INVALID_MUTUAL_AID_FOOD')>=1:
            site['mutual_aid_food']=_exact_material_delta(
                site['mutual_aid_food'],-1,
                'INVALID_COMMONS_FOOD_DELTA')
            output='ATE_INDEPENDENT_FOOD_COMMONS'
        elif loc=='home' and household>=1 and (
                can_draw_shared_food(world,aid,loc)):
            site['food']=_exact_material_delta(household,-1,'INVALID_SITE_FOOD_DELTA');output='ATE_SHARED_HOUSEHOLD_FOOD'
        elif loc=='home' and household>=1:
            status='BLOCKED';output='INSTITUTION_RESTRICTED_HOUSEHOLD_FOOD'
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
        elif seller!=aid and buyer_balance<cost:status='BLOCKED';output='INSUFFICIENT_CLAIM_ON_FOOD'
        elif controller_error:status='BLOCKED';output='MATERIAL_CONTROLLER_UNQUALIFIED'
        elif seller is None:status='BLOCKED';output='NO_OBJECTIVE_SELLER'
        else:
            seller_balance=_cash_amount(
                world['accounts'].get(seller,0),'INVALID_SELLER_BALANCE')
            paid=round(cost,5)
            if seller!=aid and buyer_balance<paid:status='BLOCKED';output='INSUFFICIENT_CLAIM_ON_FOOD'
            else:
                # Compute every transfer before mutating any ledger-owned fact.
                # Finite individually valid inputs may still overflow or lose
                # the requested five-decimal or physical-unit change.
                food_next=_exact_material_delta(available_food,-1,'INVALID_SITE_FOOD_DELTA')
                holdings_next=_exact_material_delta(owned_food,1,'INVALID_OWNED_FOOD_DELTA')
                # Existing sourcefree P049 treats self-collection of an owned
                # shop's food as a *performed* movement of material goods. It
                # is not a paid market transaction: the same account cannot
                # be both an outgoing and incoming external claim.
                if seller!=aid:
                    buyer_next=_exact_material_delta(buyer_balance,-paid,'INVALID_BUYER_TRANSFER_PRECISION')
                    seller_next=_exact_material_delta(seller_balance,paid,'INVALID_SELLER_TRANSFER_PRECISION')
                site['food']=food_next
                if seller!=aid:
                    world['accounts'][aid]=buyer_next
                    world['accounts'][seller]=seller_next
                world.setdefault('holdings',{}).setdefault(aid,{'food':0})['food']=holdings_next
                world.setdefault('material_claims',[]).append({
                    'clock':world['clock'],'kind':('FOOD_PURCHASE' if seller!=aid else 'SELF_STOCK_REALLOCATION'),
                    'buyer':aid,'site':loc,'seller':seller,'price_paid':(paid if seller!=aid else 0),
                    'goods_transferred':1,'not_actor_psychic_motive':True})
                output='FOOD_PURCHASED'
    elif attempt.action=='WORK' and work_permission(
            world,aid,loc) not in (
            'QUALIFIED_WORK_CONTRACT_ACTIVE',
            'NO_ADDITIONAL_CONTRACT_REGIME'):
        status='BLOCKED'
        output=work_permission(world,aid,loc)
    elif attempt.action=='WORK':
        site=_site(world,aid);controller,unqualified=_effective_material_controller(world,loc,site)
        stock=_nonnegative_transfer_amount(site.get('stock',0),'INVALID_SITE_STOCK')
        if unqualified:
            # Neither a missing issuer nor a mismatched owner converts an
            # institutionally controlled worksite into unowned production.
            status='BLOCKED';output='MATERIAL_CONTROLLER_UNQUALIFIED'
        elif controller==aid:
            # Self-controlled production is not a transfer of wages between
            # independent parties. Preserve the real performed activity and
            # stock change without minting a bogus employer-to-self salary.
            next_stock=_exact_material_delta(stock,2,'INVALID_SITE_STOCK_DELTA')
            site['stock']=next_stock
            world.setdefault('material_claims',[]).append({
                'clock':world['clock'],'worker':aid,'site':loc,'goods_produced':2,
                'controller':controller,'wage':0,'wage_due':0,'wage_unpaid':0,
                'worker_control_of_output':True,
                'economic_grade':'SOURCEFREE_SELF_CONTROL_NO_EXTERNAL_WAGE'})
            output='SELF_CONTROLLED_GOODS_PRODUCED'
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
            # Qualify material and monetary deltas BEFORE any persisted write.
            # Rounding separately validated operands does not guarantee a real
            # debit, credit or added stock at large magnitudes.
            stock_next=_exact_material_delta(stock,2,'INVALID_SITE_STOCK_DELTA')
            employer_next=_exact_material_delta(available,-paid,'INVALID_EMPLOYER_TRANSFER_PRECISION')
            worker_next=_exact_material_delta(worker_balance,paid,'INVALID_WORKER_TRANSFER_PRECISION')
            site['stock']=stock_next
            world['accounts'][controller]=employer_next
            world['accounts'][aid]=worker_next
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
            site['stock']=_exact_material_delta(stock,2,'INVALID_SITE_STOCK_DELTA')
            output='MATERIAL_STOCK_PRODUCED'
    elif attempt.action=='MAKE_OBJECT':
        worked_material_object=produce_artifact(world,aid,loc)
        status=worked_material_object['status']
        output=worked_material_object['outcome']
    elif attempt.action=='REPAIR':
        if attempt.object_ref is not None:
            worked_material_object=repair_artifact(
                world,aid,loc,attempt.object_ref,actor_state=actors[aid])
            status=worked_material_object['status']
            output=worked_material_object['outcome']
        else:
            site=_site(world,aid);controller,unqualified=_effective_material_controller(world,loc,site)
            stock=_nonnegative_transfer_amount(site.get('stock',0),'INVALID_SITE_STOCK')
            if unqualified:
                status='BLOCKED';output='MATERIAL_CONTROLLER_UNQUALIFIED'
            elif controller is not None and aid not in _qualified_members(site,'material_use_grants','INVALID_MATERIAL_GRANT'):
                # Public entrance ≠ the right to appropriate a controller's goods.
                # Grant is an objective world/site relation, never actor assertion.
                status='BLOCKED';output='MATERIAL_USE_NOT_AUTHORIZED'
            elif stock<1:
                status='BLOCKED';output='MISSING_REPAIR_MATERIAL'
            else:
                site['stock']=_exact_material_delta(stock,-1,'INVALID_SITE_STOCK_DELTA');output='REPAIR_PERFORMED'
    elif attempt.action=='OPEN_HALL':
        members=_qualified_members(world['institutions']['hall_board'],'members','INVALID_INSTITUTION_MEMBERSHIP')
        if aid not in members:status='BLOCKED';output='NO_INSTITUTIONAL_AUTHORITY'
        else:
            world['sites']['hall']['access']='public';output='HALL_OPENED'
    elif attempt.action=='DENY_HALL':
        members=_qualified_members(world['institutions']['hall_board'],'members','INVALID_INSTITUTION_MEMBERSHIP')
        if aid not in members:status='BLOCKED';output='NO_INSTITUTIONAL_AUTHORITY'
        else:world['sites']['hall']['access']='controlled';output='HALL_ACCESS_RESTRICTED'
    elif attempt.action=='PLEDGE_CARE':
        # The pledge is this actor's act, not the recipient's promise to
        # accept it, nor any claim that future care has already happened.
        if target in actors and target!=aid and world['positions'].get(target)==loc:
            future_care_obligation_ref=stable_id('care_obligation',{
                'actor':aid,'recipient':target,'at':world['clock']+1})
            world.setdefault('scheduled_obligations',[]).append({
                'id':future_care_obligation_ref,
                'kind':'ACTOR_PROMISED_FUTURE_CARE',
                'responsible_actor':aid,'recipient':target,
                'origin_clock':world['clock']+1,
                'due_clock':world['clock']+4,
                'status':'PENDING',
                'no_recipient_consent_to_future_action_assumed':True,
                'due_not_proof_of_breach_without_coverage':True,
                'grade':'SOURCEFREE_RESEARCH_PROVISIONAL'})
            output='FUTURE_CARE_PROMISED_NOT_FULFILLED'
        else:
            status='PARTIAL';output='PROMISE_ADDRESSEE_NOT_PRESENT'
    elif attempt.action=='SIGN_HALL_PETITION':
        institutional=contribute_to_hall_petition(world,aid,loc)
        status=institutional['status']
        output=institutional['outcome']
        policy_receipt=institutional.get('policy_receipt')
    elif attempt.action==WORK_ACCEPT:
        institutional=accept_work_terms(
            world,actors,aid,loc,attempt.intention)
        status=institutional['status']
        output=institutional['outcome']
        policy_receipt=institutional.get('contract_ref')
    elif attempt.action==WORK_SUSPEND:
        institutional=suspend_worker(
            world,actors,aid,target,loc,attempt.intention)
        status=institutional['status']
        output=institutional['outcome']
        policy_receipt=institutional.get('suspension_ref')
    elif attempt.action==WORK_RESIGN:
        institutional=withdraw_labor(
            world,actors,aid,loc,attempt.intention)
        status=institutional['status']
        output=institutional['outcome']
    elif attempt.action==WORK_POOL:
        institutional=fund_worker_relief(
            world,actors,aid,loc,attempt.intention)
        status=institutional['status']
        output=institutional['outcome']
        policy_receipt=institutional.get('relief_ref')
    elif attempt.action==WORK_DRAW:
        institutional=draw_worker_relief(
            world,actors,aid,loc,attempt.intention)
        status=institutional['status']
        output=institutional['outcome']
        policy_receipt=institutional.get('relief_ref')
    elif attempt.action==INSTALL:
        institutional=install_gate(world,actors,aid,loc,attempt.intention)
        status=institutional['status']
        output=institutional['outcome']
        policy_receipt=institutional.get('enclosure_event_ref')
    elif attempt.action==MAINTAIN:
        institutional=maintain_gate(world,actors,aid,loc,attempt.intention)
        status=institutional['status']
        output=institutional['outcome']
        policy_receipt=institutional.get('enforcement_ref')
    elif attempt.action==SANCTION:
        institutional=sanction_gate(
            world,actors,aid,target,loc,attempt.intention)
        status=institutional['status']
        output=institutional['outcome']
        policy_receipt=institutional.get('sanction_ref')
    elif attempt.action==OFFER:
        institutional=offer_control_transfer(
            world,actors,aid,target,loc,attempt.intention)
        status=institutional['status']
        output=institutional['outcome']
        policy_receipt=institutional.get('offer_ref')
    elif attempt.action==ACCEPT:
        institutional=accept_control_transfer(
            world,actors,aid,loc,attempt.intention)
        status=institutional['status']
        output=institutional['outcome']
        policy_receipt=institutional.get('transfer_ref')
    elif attempt.action==COMMONS:
        institutional=contribute_food_commons(
            world,actors,aid,loc,attempt.intention)
        status=institutional['status']
        output=institutional['outcome']
        policy_receipt=institutional.get('commons_ref')
    elif attempt.action=='SIGN_FOOD_PETITION':
        institutional=contribute_food_petition(
            world,actors,aid,loc,attempt.intention)
        status=institutional['status']
        output=institutional['outcome']
        policy_receipt=institutional.get('policy_ref')
    elif attempt.action=='FEED':
        resolved_food=perform_one_actual_feeding(
            world,actors,aid,target,loc,
            attempt.intention)
        status=resolved_food['status']
        output=resolved_food['outcome']
        material_feeding_ref=resolved_food['material_feeding_ref']
        if status=='PERFORMED':
            effects[target]={
                'action':'RECEIVED_FEEDING','bodily':True,
                'material_food_consumed_in_world':True}
    elif attempt.action=='CARE':
        if target in actors and world['positions'].get(target)==loc:
            b=actors[target]['body']
            # A recipient does not silently acquire valid physiology through a
            # giver's act; validate before the first objective bodily effect.
            eligible(b,'WAIT')
            b['comfort']=min(1,b['comfort']+.18)
            effects[target]={'action':'RECEIVED_CARE','bodily':True}
            care_labor_receipt=retain_material_care(
                world,aid,target,clock=world['clock']+1,
                location=loc,effect='RECEIVED_CARE')['id']
            # A later actually performed act can discharge an earlier pledge.
            # An elapsed deadline alone never invents fulfillment or breach.
            for due in world.get('scheduled_obligations',[]):
                if (due.get('status')=='PENDING'
                        and due.get('responsible_actor')==aid
                        and due.get('recipient')==target
                        and due.get('kind')=='ACTOR_PROMISED_FUTURE_CARE'):
                    due['status']='FULFILLED_BY_ACTUAL_CARE'
                    due['fulfilled_at_clock']=world['clock']+1
                    due['fulfillment_care_labor_ref']=care_labor_receipt
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
            if attempt.action=='SIGNAL' and partner_attempt.action=='FEED':
                # The responder's autonomous FEED is not merely consent to
                # a signal: objective food stock and bodily eligibility still
                # decide what material assistance actually happened.
                supported=perform_one_actual_feeding(
                    world,actors,partner_attempt.actor,aid,loc,
                    partner_attempt.intention)
                material_feeding_ref=supported['material_feeding_ref']
                if supported['status']=='PERFORMED':
                    effects[aid]['received_assistance']=True
                    joint['material_effects'].append({
                        'recipient':aid,
                        'kind':'SOURCE_QUALIFIED_ACTUAL_FEEDING',
                        'material_feeding_ref':material_feeding_ref})
                else:
                    status='PARTIAL'
                    output='COACTOR_ATTEMPTED_FEED_WITHOUT_AVAILABLE_STOCK'
                    for performed_action in performed:
                        if performed_action['actor']==partner_attempt.actor:
                            performed_action['status']='BLOCKED'
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
            if status=='PERFORMED':
                field['history'].append(joint)
            # PFF noncollapse: two co-occurrences are evidence of repetition,
            # NOT proof of learned relational capability, love, recognition,
            # or a stable social attractor. Keep observed pattern distinct.
            if status=='PERFORMED' and len(field['history'])>=2 and 'REPEATED_JOINT_ACT_OBSERVED' not in field['observed_patterns']:
                field['observed_patterns'].append('REPEATED_JOINT_ACT_OBSERVED')
            if status=='PERFORMED':
                output='JOINT_ACTIVITY_PERFORMED'
        else:
            status='PARTIAL';output='INDEPENDENT_COACTOR_DID_NOT_JOIN'
    elif attempt.action in ('SING','PRACTICE','MAKE_SPACE'):
        output='SOLO_PRACTICE'
    elif attempt.action=='SIGNAL':
        output='NONVERBAL_SIGNAL'
    elif attempt.action=='SPEAK':
        if attempt.object_ref is None:
            output='SPEECH_PERFORMED'
        else:
            # Publicly referring to a thing requires a thing that is
            # materially THERE. The simulation does not know the word said
            # or the speaker's inner intention, only the enacted conjunction.
            referred=[obj for obj in material_objects_present(world,loc)
                if obj.get('id')==attempt.object_ref]
            if len(referred)==1:
                output='SPEECH_WITH_PRESENT_MATERIAL_OBJECT'
            else:
                status='PARTIAL'
                output='ATTEMPTED_SPEECH_ABOUT_UNAVAILABLE_OBJECT'
    elif attempt.action=='ASK':
        output='REQUEST_EXPRESSED_NOT_AUTOMATICALLY_ACCEPTED'
    elif attempt.action=='REFUSE':output='ACTOR_REFUSED'
    elif attempt.action=='REST':output='BODY_RESTED'
    elif attempt.action=='ORIENT':output='ORIENTING_PERFORMED'
    elif attempt.action=='INSPECT':
        # An investigation has a real object. An arbitrary administrator's
        # private record is not what a posted notice says, and the actor must
        # identify a particular visible object rather than inspect 'society'.
        public=[notice for notice in notices_present(
                    world,loc,world['clock'])
                if notice['id']==attempt.object_ref]
        if len(public)==1:
            inspected_public_notice=public[0]
            output='PUBLIC_NOTICE_INSPECTED'
        else:
            objects=[obj for obj in material_objects_present(world,loc)
                     if obj['id']==attempt.object_ref]
            if len(objects)!=1:
                status='PARTIAL';output='NO_ACTOR_SELECTED_PUBLIC_OBJECT'
            else:
                inspected_material_object=objects[0]
                output='VISIBLE_MATERIAL_OBJECT_INSPECTED'
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
                   'institutional_policy_ref':policy_receipt,
                   'social_reproductive_labor_ref':care_labor_receipt,
                   'material_feeding_ref':material_feeding_ref,
                   'future_care_obligation_ref':future_care_obligation_ref,
                   'inspected_public_notice_ref':(
                        inspected_public_notice['id'] if inspected_public_notice else None),
                   'worked_material_object_ref':(
                        worked_material_object.get('object_ref')
                        if worked_material_object else None),
                   'inspected_material_object_ref':(
                        inspected_material_object['id']
                        if inspected_material_object else None),
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
    if inspected_public_notice is not None:
        # The personally received cue contains only what the institution
        # actually put on its public notice, not its private causal archive.
        # No separate second cue replaces the selected event cue in the
        # actor-specific experienced-event projection.
        terms=inspected_public_notice.get('public_terms',[])
        if type(terms) is not list or any(type(t) is not str for t in terms):
            raise ValueError('PUBLIC_NOTICE_INVALID_TERMS')
        sign=add_cue(world,'performed_inspect',
            ['inspect','public_notice']+terms,
            location=loc,modality='visual',private_to=aid,
            description=inspected_public_notice.get(
                'public_text','PUBLIC_NOTICE_WITHOUT_TEXT'),
            source_actor=aid)
        sign['public_notice_ref']=inspected_public_notice['id']
        sign['world_rule_truth_not_inferred_from_public_text']=True
    elif inspected_material_object is not None:
        # The actor sees apparent condition, not title, production class,
        # source labor, all past repairs or another person's private meaning.
        condition=inspected_material_object['condition']
        appearance=('visibly_worn' if condition<.65 else
                    'apparently_repaired' if condition<.95 else
                    'apparently_sound')
        sign=add_cue(world,'performed_inspect',
            ['inspect','material_object',appearance],
            location=loc,modality='visual',private_to=aid,
            description='visible material appearance: '+appearance,
            source_actor=aid)
        sign['material_object_ref']=inspected_material_object['id']
        sign['public_appearance_not_complete_object_history']=True
    else:
        sign=add_cue(world,'performed_'+attempt.action.lower(),
                [attempt.action.lower(),perceptible_outcome.lower()],
                location=loc,modality='auditory' if attempt.action in (
                    'SING','SPEAK','SIGNAL','ASK') else 'visual',
                description=perceptible_outcome,source_actor=aid)
        if worked_material_object and worked_material_object.get('object_ref'):
            sign['material_object_ref']=worked_material_object['object_ref']
            sign['actor_sensed_object_not_full_object_provenance']=True
        if (attempt.action=='SPEAK' and status=='PERFORMED'
                and output=='SPEECH_WITH_PRESENT_MATERIAL_OBJECT'):
            # In the objective world this speaker enacted speech in the
            # presence of a particular visible material thing. A listener
            # may hear the public sign; no actual lexical token, original
            # message, teaching motive or lexical competence is inferred.
            sign['material_object_ref']=attempt.object_ref
            sign['actual_spoken_object_demonstration']=True
            sign['spoke_about_material_object_without_encoded_word']=True
            sign['unobserved_semantic_content']='NOT_RECONSTRUCTED'
            sign['tags']+=['public_object_reference','object_present']
        if (attempt.action=='SIGNAL' and status=='PERFORMED'
                and partner_attempt is not None and partner_valid
                and partner_attempt.action in ('CARE','FEED')
                and output=='JOINT_ACTIVITY_PERFORMED'):
            # An actual particular-person coaction can be a publicly
            # perceptible part of this event without revealing the responder's
            # underlying motive, lasting disposition or private mind. This
            # sourcefree visibility approximation remains revisable.
            sign['actor_accessible_care_responder_ref']=partner_attempt.actor
            sign['actual_independent_care_response_not_a_motive']=True
            sign['not_automatic_actor_conscious_identification']=True
        if (attempt.action=='SIGNAL' and status=='PERFORMED'
                and partner_attempt is not None and partner_valid
                and partner_attempt.action=='SPEAK'
                and output=='JOINT_ACTIVITY_PERFORMED'):
            # The other person independently answered this particular
            # nonverbal call with speech. This supplies a real auditory
            # coordination occasion; it does NOT disclose a word, dictate
            # the listener's interpretation or teach a language instantly.
            sign['actor_accessible_speech_responder_ref']=partner_attempt.actor
            sign['actual_independent_speech_response']=True
            sign['spoken_content']='NOT_CAPTURED_OR_RECONSTRUCTED'
            sign['vocal_interchange_not_lexical_comprehension']=True
    if status=='PERFORMED' and attempt.action=='SPEAK':
        cadence=realized_vocal_cadence(actors[aid],attempt,loc)
        if cadence is not None:
            sign['vocal_cadence']=cadence
            sign['description']=CADENCES[cadence]
            sign['tags'].append('vocal_cadence:'+cadence.lower())
    # R26: world-owned, actually performed person-directed conduct has an
    # objective two-person history even when neither party interprets it alike.
    # Give *eligible* witnesses the target identity, not the target's mind,
    # relational meaning, consent, or a privileged explanation of this act.
    if (status=='PERFORMED' and attempt.action in ('CARE','FEED','IMPOSE')
            and type(target) is str and target in actors and target!=aid
            and world['positions'].get(target)==loc):
        field=_field(world,aid,target)
        field['history'].append({
            'clock':world['clock'],'actor':aid,'target':target,
            'operation':attempt.action,'performed_status':'PERFORMED',
            'not_consent_or_private_psychological_meaning':True,
            'grade':'SOURCEFREE_RESEARCH_PROVISIONAL'})
        sign['actor_accessible_target_ref']=target
        sign['public_person_directed_act_not_private_intention']=True
    witnesses=[a for a in actors if world['positions'].get(a)==loc]
    # World-level efficacy is NOT the actor's own explanatory model. Even an
    # independently authored coactor response does not make the principal's
    # body an owner of the jointly produced power. Preserve actual
    # participation and objective permissions as distinct analytic fields.
    genuinely_joined=(
        [partner_attempt.actor] if (
            partner_attempt and partner_valid and
            attempt.action in COOPERATIVE and
            partner_attempt.action in COOPERATIVE[attempt.action] and
            status=='PERFORMED') else [])
    arrangement=objective_arrangement(
        actors[aid],world,attempt.action,loc,
        actual_other_participants=genuinely_joined)
    return Resolution(status,performed,
        {'event':event_summary,
         'sourcefree_objective_efficacy_arrangement_analyst_only':arrangement},
        effects,witnesses,output)


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
                world['positions'].get(principal.actor)==world['positions'].get(principal.target)
                and eligible(actors[principal.actor]['body'],principal.action)[0]):
            candidate=self.__planner(principal,copy(world),copy(actors))
            if not isinstance(candidate,Attempt) or candidate.actor!=principal.target:
                raise ValueError('INDEPENDENT_COACTOR_POLICY_INVALID')
            if candidate.action not in COOPERATIVE[principal.action]|{'REFUSE'}:
                raise ValueError('INDEPENDENT_COACTOR_NOT_ELIGIBLE_TO_JOIN')
            if candidate.target!=principal.actor:
                raise ValueError('INDEPENDENT_COACTOR_TARGET_MISMATCH')
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
