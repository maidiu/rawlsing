"""Independent objective world with material effects and separately authored coactivity.
World consequences can be unilateral, imposed, cooperative, or refused.
"""
from .types import Attempt, Resolution, copy, stable_id, digest
from .organism import eligible
from dataclasses import asdict
import hmac, hashlib, os, json

COOPERATIVE={'SING':{'JOIN','SING','MAKE_SPACE'},'PRACTICE':{'CARE','JOIN','MAKE_SPACE'},
             'MAKE_SPACE':{'JOIN','SING'},'SHARE':{'JOIN','CARE'}}


def add_cue(world,kind,tags,location='all',modality='visual',description='',source_actor=None,
            private_to=None,threshold=.05):
    cue={'id':stable_id('cue',{'n':world['clock'],'tags':tags,'s':source_actor,'d':description,'index':len(world['cues'])}),
         'kind':kind,'tags':list(tags),'location':location,'modality':modality,
         'description':description or kind,'source_actor':source_actor,
         'private_to':private_to,'threshold':threshold}
    world['cues'].append(cue)
    return cue


def _field(world,a,b):
    ids=sorted((a,b));key='rel:'+':'.join(ids)
    return world['relations'].setdefault(key,{'id':key,'participants':ids,
       'history':[],'joint_capabilities':[],'constraints':[],
       'continuity':'open','objective_grade':'SOURCEFREE_RESEARCH_PROVISIONAL'})


def _site(world,aid):return world['sites'].get(world['positions'].get(aid),{})


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
        if site.get('food',0)<1:status='BLOCKED';output='NO_FOOD_AVAILABLE'
        else:site['food']-=1;output='ATE_FOOD'
    elif attempt.action=='WORK':
        site=_site(world,aid);site['stock']=site.get('stock',0)+2;output='MATERIAL_STOCK_PRODUCED'
    elif attempt.action=='REPAIR':
        site=_site(world,aid)
        if site.get('stock',0)<1:status='BLOCKED';output='MISSING_REPAIR_MATERIAL'
        else:site['stock']-=1;output='REPAIR_PERFORMED'
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
            field['history'].append({'clock':world['clock'],'activity':attempt.action,
                    'contributions':[attempt.action,partner_attempt.action]})
            if len(field['history'])>=2 and 'RECURRENT_COORDINATION' not in field['joint_capabilities']:
                field['joint_capabilities'].append('RECURRENT_COORDINATION')
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
    event_summary={'clock':world['clock'],'actor':aid,'action':attempt.action,
                   'target':target,'outcome':output,'status':status,
                   'coactor':partner_attempt.actor if partner_attempt else None,
                   'coactor_action':partner_attempt.action if partner_attempt else None,
                   'object_ref':attempt.object_ref}
    world['public_history'].append(event_summary)
    # New cues are actual public world consequences, not actor introspection.
    # World effects persist even when no participant currently perceives them.
    add_cue(world,'performed_'+attempt.action.lower(),[attempt.action.lower(),output.lower()],
            location=loc,modality='auditory' if attempt.action in ('SING','SPEAK','SIGNAL','ASK') else 'visual',
            description=output,source_actor=aid)
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
