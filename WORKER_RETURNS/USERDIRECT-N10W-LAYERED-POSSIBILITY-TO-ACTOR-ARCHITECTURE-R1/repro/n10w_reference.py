"""Independent source-free falsifier probe; not a Pyat/Sorok production implementation.
Deliberately tests negative ownership/identification boundaries, not actual V3 actor science.
"""
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json

UNKNOWN = 'UNKNOWN'
NOT_REACHED = 'NOT_REACHED_UNISSUED_ACTOR_RULE'

class BoundaryRefusal(ValueError):
    pass

def strict_field(v, *, current=True, published=True, authorized=True):
    if not (current and published and authorized): return UNKNOWN
    if v is None: return UNKNOWN
    if type(v) not in (int,bool): raise BoundaryRefusal('BAD_FIELD_TYPE')
    return v

def structural(rule, budget):
    if type(budget) is not int or budget < 0: raise BoundaryRefusal('BAD_BUDGET')
    a, fee, exit_, civil, sanction=(rule.get(k,UNKNOWN) for k in ('training_access','training_fee','exit_cost','civil_open','civil_sanction'))
    known=lambda x:x!=UNKNOWN
    permitted=UNKNOWN if not known(a) else bool(a)
    affordable=UNKNOWN if not known(fee) else fee<=budget
    practical=UNKNOWN if not known(permitted) or not known(affordable) else permitted and affordable
    exit_aff=UNKNOWN if not known(exit_) else exit_<=budget
    civil_ok=UNKNOWN if not known(civil) or not known(sanction) else bool(civil) and not bool(sanction)
    return dict(institutional_access=permitted,budget_affordability=affordable,training_practicable=practical,exit_affordable=exit_aff,civil_practicable=civil_ok)

def perspective(*, institutional, practical, witnessed_channel=None, actor_rule_issued=False, actor_history=None):
    # No permission to manufacture actor knowledge, even when formal possibility is true.
    if witnessed_channel is None:
        exposure=UNKNOWN
    else:
        exposure=bool(witnessed_channel)
    return dict(institutional_access=institutional,material_practicability=practical,
                exposure=exposure,actor_knowledge=NOT_REACHED if not actor_rule_issued else UNKNOWN,
                actor_meaning=NOT_REACHED if not actor_rule_issued else UNKNOWN,
                proposed_action=NOT_REACHED if not actor_rule_issued else UNKNOWN,
                empirical_route_propensity=None,simulation_policy=None)

def audit_joint_probability(*,joint_attempted=None,eligible_denominator=None,exposed_denominator=None,
                            provenance_granted=False,model_policy=None):
    if not provenance_granted or joint_attempted is None or eligible_denominator is None:
        empirical=None
    else:
        if not (isinstance(joint_attempted,int) and isinstance(eligible_denominator,int)) or eligible_denominator<=0 or not 0<=joint_attempted<=eligible_denominator:
            raise BoundaryRefusal('UNQUALIFIED_RISK_SET')
        empirical=Fraction(joint_attempted,eligible_denominator)
    return dict(empirical=empirical,empirical_identification='UNIDENTIFIED' if empirical is None else 'JOINT_SAMPLE_DESCRIPTIVE_ONLY',
                simulation_policy=None if model_policy is None else {'candidate':'UNISSUED_TEST_ONLY','value':model_policy})

def partial_bounds(covered_cell, unknown_mass):
    a,u=Fraction(covered_cell),Fraction(unknown_mass)
    if not (0<=a<=1 and 0<=u<=1 and a+u<=1): raise BoundaryRefusal('INVALID_MASS')
    return a,a+u

def select_world(*, effective, published, requested, known_at=None, revoked=False):
    if revoked:return UNKNOWN
    if requested<effective or requested<published:return UNKNOWN
    return {'world_selected':True,'actor_knows':UNKNOWN if known_at is None else known_at<=requested}

def candidate_actor_transition(*, rule_issued=False, owner_receipt=None, history_replayed=False, actor_ref=None):
    if not rule_issued or not owner_receipt or not history_replayed or not actor_ref:
        return NOT_REACHED
    return 'RULED_ACTOR_CANDIDATE_ONLY_NO_ADMISSION'

def admitted_consequence(*, event_receipt=None, counterpart_receipt=None, world_owner_permission=False):
    if not event_receipt or not counterpart_receipt or not world_owner_permission:return NOT_REACHED
    return 'EXTERNAL_OWNER_REVALIDATION_REQUIRED'

def canonical_hash(payload):
    return sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
