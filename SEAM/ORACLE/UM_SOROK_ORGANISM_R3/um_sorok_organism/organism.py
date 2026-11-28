"""Bounded, functional, sourcefree organism model. No endocrine realism claims."""
from .types import copy
import math

ACTIONS = {
    'REST':{'motor':0.0,'language':0.0,'cost':0.0},
    'EAT':{'motor':0.10,'language':0.0,'cost':0.03},
    'BUY_FOOD':{'motor':0.18,'language':0.0,'cost':0.03},
    'SIGNAL':{'motor':0.10,'language':0.0,'cost':0.04},
    'ORIENT':{'motor':0.08,'language':0.0,'cost':0.02},
    'PRACTICE':{'motor':0.15,'language':0.0,'cost':0.08},
    'SING':{'motor':0.24,'language':0.0,'cost':0.07},
    'JOIN':{'motor':0.24,'language':0.0,'cost':0.07},
    'MAKE_SPACE':{'motor':0.24,'language':0.05,'cost':0.06},
    'CARE':{'motor':0.42,'language':0.0,'cost':0.10},
    'FEED':{'motor':0.42,'language':0.0,'cost':0.08},
    'WORK':{'motor':0.62,'language':0.0,'cost':0.22},
    'REPAIR':{'motor':0.55,'language':0.10,'cost':0.16},
    'MAKE_OBJECT':{'motor':0.52,'language':0.10,'cost':0.15},
    'ASK':{'motor':0.05,'language':0.4,'cost':0.04},
    'SPEAK':{'motor':0.02,'language':0.35,'cost':0.03},
    'REFUSE':{'motor':0.0,'language':0.0,'cost':0.01},
    'WAIT':{'motor':0.0,'language':0.0,'cost':0.0},
    'MOVE':{'motor':0.32,'language':0.0,'cost':0.06},
    'INSPECT':{'motor':0.10,'language':0.0,'cost':0.02},
    'OPEN_HALL':{'motor':0.35,'language':0.0,'cost':0.06},
    'DENY_HALL':{'motor':0.20,'language':0.0,'cost':0.01},
    'SIGN_HALL_PETITION':{'motor':0.22,'language':0.28,'cost':0.05},
    'SIGN_FOOD_PETITION':{'motor':0.22,'language':0.28,'cost':0.05},
    'INSTALL_PANTRY_GATE':{'motor':0.52,'language':0.28,'cost':0.17},
    'MAINTAIN_PANTRY_GATE':{'motor':0.42,'language':0.20,'cost':0.14},
    'SANCTION_PANTRY_ACCESS':{'motor':0.35,'language':0.20,'cost':0.12},
    'CONTRIBUTE_FOOD_COMMONS':{'motor':0.42,'language':0.0,'cost':0.09},
    'OFFER_PANTRY_CONTROL_TRANSFER':{'motor':0.24,'language':0.28,'cost':0.05},
    'ACCEPT_PANTRY_CONTROL_TRANSFER':{'motor':0.24,'language':0.28,'cost':0.05},
    'ACCEPT_WORK_TERMS':{'motor':0.20,'language':0.28,'cost':0.04},
    'SUSPEND_WAGE_WORK':{'motor':0.24,'language':0.32,'cost':0.08},
    'WITHDRAW_FROM_WAGE_WORK':{'motor':0.15,'language':0.28,'cost':0.04},
    'CONTRIBUTE_WAGE_RELIEF':{'motor':0.18,'language':0.20,'cost':0.04},
    'DRAW_WAGE_RELIEF':{'motor':0.14,'language':0.18,'cost':0.04},
    'PLEDGE_CARE':{'motor':0.18,'language':0.28,'cost':0.03},
    'IMPOSE':{'motor':0.50,'language':0.0,'cost':0.14},
}

def eligible(body, action):
    # Invalid embodied material must never acquire capacity by Python's NaN
    # comparison behavior or apply_body's clamps. Stop *before* objective action.
    for key in ('nutrition','rest','comfort','pain','arousal','motor',
                'sensor','language','illness','regulation'):
        v=body.get(key)
        if (isinstance(v,bool) or not isinstance(v,(int,float)) or
                not math.isfinite(v) or not 0<=v<=1):
            raise ValueError('INVALID_BODY_STATE:'+key)
    if action not in ACTIONS: return False, 'UNKNOWN_ACTION'
    needed=ACTIONS[action]
    if body['motor'] < needed['motor']:return False,'MOTOR_CAPABILITY'
    if body['language'] < needed['language']:return False,'LANGUAGE_CAPABILITY'
    if body['rest'] < needed['cost']*1.25: return False,'FATIGUE'
    if body['pain'] > .85 and action not in ('REST','WAIT','SIGNAL','REFUSE'):
        return False,'PAIN_LIMIT'
    if body['illness']>.85 and needed['cost']>.05:return False,'ILLNESS_LIMIT'
    return True,'ELIGIBLE'

def apply_body(actor, action, status, elapsed=1):
    b=actor['body']
    if status in ('PERFORMED','PARTIAL','IMPOSED'):
        b['rest']-=ACTIONS.get(action,{'cost':0})['cost']
        if action=='REST':
            b['rest']+=.23; b['comfort']+=.06
        elif action=='EAT':
            b['nutrition']+=.30; b['comfort']+=.10
        elif action=='CARE':
            b['comfort']+=.02
        elif action=='PRACTICE':
            b['motor']+=.008
        elif action=='IMPOSE':
            b['arousal']+=.07
    b['nutrition']-=.012*max(1,elapsed)
    b['rest']-=.006*max(1,elapsed)
    b['comfort']-=.004*max(1,elapsed)
    b['arousal']+=(0.5-b['arousal'])*.06
    for k in ('nutrition','rest','comfort','pain','arousal','motor','sensor','language','illness','regulation'):
        b[k]=round(max(0.0,min(1.0,b[k])),5)
    return actor

def conserved_motor_exercise(actor):
    """Bounded continuation of the EXISTING .008 performed PRACTICE effect.

    Actual actor-owned exercise and its distinct personal event path are
    required. Do not count a qualified aggregate day as a performed episode.
    This is a provisional motor readiness floor, not a skill, medical growth
    rate, recollection, project or proof of independent mastery.
    """
    paths={(x.get('event'),x.get('experience_ref'))
           for x in actor.get('evidence_paths',[])
           if x.get('own_action')=='PRACTICE'}
    seen=set()
    for row in reversed(actor.get('power_exercises',[])):
        pair=(row.get('event_ref'),row.get('experience_ref'))
        if (row.get('actor')==actor['id'] and row.get('operation')=='PRACTICE'
                and row.get('attempt_status_analyst_receipt')=='PERFORMED'
                and row.get('felt_attempt') is True
                and all(type(x) is str for x in pair) and pair in paths):
            seen.add(pair)
            if len(seen)>=5:break
    return round(.008*len(seen),5)


def mature(actor,days):
    """Explicit functional illustrative approximation, not science of human maturation."""
    if days<0:raise ValueError('negative passage of time')
    actor['age_days']+=days
    if actor['role']=='child':
        years=actor['age_days']/365.0
        b=actor['body']
        # Do not erase the bounded products of actually exercised bodily
        # activity when the age-only floor catches up to the old motor value.
        # max prevents charging the same exercise again on each period.
        # An already higher motor state remains intact, as before.
        baseline=min(.9,.17+.18*years)
        from .mediated_efficacy import preproject_motor_readiness
        b['motor']=max(b['motor'],round(min(.9,baseline+conserved_motor_exercise(actor)
                                         +preproject_motor_readiness(actor)),5))
        b['sensor']=max(b['sensor'],round(min(.9,.4+.12*years),5))
        # Language readiness != culturally acquired language competence: ceiling only.
        b['language_ceiling']=round(min(.95,.1+.22*years),5)
        b['regulation']=max(b['regulation'],round(min(.7,.28+.08*years),5))
    return actor
