"""Research-only counterfactual court: independent workplace → encounter → enacted practices.

This is an explicitly UNCALIBRATED source-free demonstrator of a material encounter
chain; it does NOT generate human personalities or adopt CAN008/CAN011/ADP semantics.
No choices are keyed on a desired child psychology or expected counterfactual result.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, replace
from hashlib import sha256
from typing import Literal
import json
import random

GRADE = 'SOURCEFREE_UNCALIBRATED_EVENT_INTERSECTION_EXPERIMENT_R1'
WORK_OUTCOMES = ('HOURS_CUT', 'RAISE_WITH_OVERTIME', 'ROUTINE')


def digest(x):
    return sha256(json.dumps(x,sort_keys=True,separators=(',', ':'),ensure_ascii=True).encode()).hexdigest()


@dataclass(frozen=True)
class FatherHistory:
    worker_id: str = 'father'
    cash_buffer: int = 125
    available_after_work_min: int = 35
    joint_repair_episodes: int = 4
    protected_care_min: int = 0
    repair_skill: int = 3
    # Practices/constraints acquired before work shock, not temperament tags.


@dataclass(frozen=True)
class ChildHistory:
    child_id: str = 'child'
    practical_bicycle_episodes: int = 1
    school_transport_required: bool = True
    bus_route_accessible: bool = True
    weekday_practice_slots: int = 2


@dataclass(frozen=True)
class NeighborHistory:
    neighbor_id: str = 'neighbor'
    independently_scheduled_shift_day4: bool = True
    independent_project: str = 'library_inventory'
    tool_lending_available: bool = False


@dataclass(frozen=True)
class WorldParameters:
    father: FatherHistory = FatherHistory()
    child: ChildHistory = ChildHistory()
    neighbor: NeighborHistory = NeighborHistory()
    replacement_cost: int = 175
    repair_material_cost: int = 18


@dataclass(frozen=True)
class Occurrence:
    id: str
    day: int
    minute: int
    actor: str
    kind: str
    facts: tuple[tuple[str, str|int|bool], ...]
    parents: tuple[str,...]
    issuer: str
    hash: str

    def fact(self,key):
        return dict(self.facts)[key]


@dataclass(frozen=True)
class Trace:
    events: tuple[Occurrence,...]
    actor_actions: tuple[str,...]
    child_practice_count: int
    child_project_after: str
    degree_of_psychological_change: None = None
    evidence_grade: str = GRADE

    def get(self,event_id):
        return next(e for e in self.events if e.id==event_id)

    def content_digest(self):
        return digest([asdict(e) for e in self.events])

    def validate(self):
        seen={}
        for e in self.events:
            body=asdict(e);body.pop('hash')
            assert digest(body)==e.hash, ('CONTENT_CHANGED',e.id)
            assert e.id not in seen, ('ID_COLLISION',e.id)
            for parent_id in e.parents:
                assert parent_id in seen, ('MISSING_PARENT_OR_TIME_TRAVEL',e.id,parent_id)
                parent=seen[parent_id]
                assert (parent.day,parent.minute)<(e.day,e.minute), ('NONCAUSAL_TIME',e.id)
            seen[e.id]=e
        assert self.get('workplace').actor=='employer'
        assert 'theft' not in self.get('workplace').parents
        assert self.degree_of_psychological_change is None
        return True


class Journal:
    def __init__(self): self.events=[]
    def add(self,event_id,day,minute,actor,kind,facts,parents=(),issuer='TEST_ONLY_WORLD_FIXTURE'):
        known={e.id:e for e in self.events}
        if event_id in known: raise ValueError('EVENT_ID_COLLISION')
        for parent_id in parents:
            if parent_id not in known:raise ValueError('UNWITNESSED_PARENT')
            parent=known[parent_id]
            if (parent.day,parent.minute)>=(day,minute):raise ValueError('TEMPORAL_LEAKAGE')
        facts=tuple(sorted(facts.items()))
        args=dict(id=event_id,day=day,minute=minute,actor=actor,kind=kind,
                  facts=facts,parents=tuple(parents),issuer=issuer)
        e=Occurrence(**args,hash=digest(args))
        self.events.append(e)
        return e


def sample_independent_workplace(seed:int):
    """Exogenous lottery used solely for experiment; distribution NOT empirical."""
    return random.Random(seed).choice(WORK_OUTCOMES)


def work_facts(outcome):
    # These are materially distinguishable shift/pay conditions, NOT mood or psyche.
    if outcome=='HOURS_CUT':
        return dict(kind=outcome,wage_delta=-175,required_overtime_min=0,job_security_warning=True)
    if outcome=='RAISE_WITH_OVERTIME':
        return dict(kind=outcome,wage_delta=210,required_overtime_min=32,job_security_warning=False)
    if outcome=='ROUTINE':
        return dict(kind=outcome,wage_delta=0,required_overtime_min=0,job_security_warning=False)
    raise ValueError('UNKNOWN_WORKPLACE_OUTCOME')


def father_action(work, history:FatherHistory, replacement_cost:int, repair_cost:int):
    """Explicit uncalibrated action/feasibility rule, not a stress → mood lookup.

    Competing material projects: keep household solvent, respond to child, maintain
    own practiced repair activity, and discharge assigned work obligations.
    """
    cash_after=history.cash_buffer + work['wage_delta']
    assigned_overtime=work['required_overtime_min']
    # A prior care commitment can cause a worker to DECLINE some assigned overtime;
    # it cannot conjure time out of nowhere. Record the material work tradeoff.
    minimum_declined=max(0,history.protected_care_min -
                         max(0,history.available_after_work_min-assigned_overtime))
    declined=min(assigned_overtime,minimum_declined)
    worked_overtime=assigned_overtime-declined
    care_budget=max(0,history.available_after_work_min-worked_overtime)
    repair_possible=(history.joint_repair_episodes>=2 and history.repair_skill>=2
                     and care_budget>=15 and cash_after>=repair_cost)
    if repair_possible:
        action='OFFER_JOINT_REPAIR'
    elif care_budget<10:
        action='DEFER_CONVERSATION'
    elif cash_after>=replacement_cost:
        action='OFFER_REPLACEMENT'
    else:
        action='DISCUSS_NONPURCHASE_OPTIONS'
    return dict(action=action,available_minutes=care_budget,assigned_overtime_min=assigned_overtime,
                overtime_declined_min=declined, overtime_worked_min=worked_overtime,
                cash_after_work=cash_after,
                replacement_feasible=cash_after>=replacement_cost,
                material_repair_feasible=cash_after>=repair_cost)


def child_next_activity(father_response, history:ChildHistory, neighbor:NeighborHistory):
    """Observable project/action rules; NOT a belief, attachment or trait classifier."""
    action=father_response['action']
    if action=='OFFER_JOINT_REPAIR' and history.weekday_practice_slots>0:
        return 'PARTICIPATE_JOINT_REPAIR'
    if action=='OFFER_REPLACEMENT' and history.school_transport_required:
        return 'ARRANGE_TEMPORARY_TRANSPORT'
    if history.bus_route_accessible:
        return 'TAKE_BUS'
    if not neighbor.independently_scheduled_shift_day4 and neighbor.tool_lending_available:
        return 'ASK_NEIGHBOR_FOR_TOOL'
    return 'MISS_TRIP_AND_SEEK_ALTERNATIVE'


def simulate(outcome:Literal['HOURS_CUT','RAISE_WITH_OVERTIME','ROUTINE'],
             params:WorldParameters=WorldParameters()):
    """The theft and all biographies are fixed; only employer exogenous event varies."""
    j=Journal()
    f=params.father;c=params.child;n=params.neighbor
    j.add('father_history',0,60,'father','PREEXISTING_ACTIVITY',asdict(f))
    j.add('child_history',0,61,'child','PREEXISTING_ACTIVITY',asdict(c))
    j.add('neighbor_history',0,62,'neighbor','PREEXISTING_PROJECT',asdict(n))
    w=work_facts(outcome)
    j.add('workplace',3,540,'employer','WORKPLACE_OCCURRENCE',w,
          issuer='TEST_ONLY_INDEPENDENT_EMPLOYER_FIXTURE')
    j.add('theft',3,900,'world','MISSING_BICYCLE',dict(object='bicycle',location='garage',
          culprit='UNKNOWN'),issuer='TEST_ONLY_OBJECTIVE_EVENT_FIXTURE')
    j.add('father_receives_work_news',3,960,'father','WORK_NOTIFICATION',
          dict(workplace_ref='workplace'),parents=('workplace','father_history'))
    j.add('child_reports_theft',3,1080,'child','LOSS_REPORT',
          dict(bicycle_missing=True),parents=('theft','child_history'))
    response=father_action(w,f,params.replacement_cost,params.repair_material_cost)
    j.add('father_response',3,1081,'father','ACTUAL_FATHER_ACTION',response,
          parents=('father_receives_work_news','child_reports_theft','father_history'))
    # Neighbor has an independently scheduled life, irrespective of child's theft.
    j.add('neighbor_independent_shift',4,420,'neighbor','OTHER_PROJECT_ACTION',
          dict(working_library_shift=n.independently_scheduled_shift_day4,project=n.independent_project),
          parents=('neighbor_history',))
    day4=child_next_activity(response,c,n)
    readset=['father_response','child_history']
    if day4=='ASK_NEIGHBOR_FOR_TOOL':
        j.add('neighbor_tool_response',4,450,'neighbor','OTHER_ACTOR_RESPONSE',
              dict(action='OFFER_TOOL',project=n.independent_project),
              parents=('neighbor_independent_shift',))
        readset.append('neighbor_tool_response')
    j.add('child_activity_day4',4,480,'child','OBSERVABLE_ACTIVITY',dict(action=day4),
          parents=tuple(readset))
    actions=[day4]
    if day4=='PARTICIPATE_JOINT_REPAIR':
        follow='REHEARSE_BICYCLE_REPAIR' if c.weekday_practice_slots>1 else 'INSPECT_BICYCLE'
    elif day4=='TAKE_BUS':
        follow='TAKE_BUS'
    elif day4=='ARRANGE_TEMPORARY_TRANSPORT':
        follow='USE_BORROWED_BICYCLE'
    else:
        follow='PLAN_NEXT_TRANSPORT'
    j.add('child_activity_day5',5,480,'child','OBSERVABLE_ACTIVITY',dict(action=follow),
          parents=('child_activity_day4',))
    actions.append(follow)
    # The only candidate retained practical effect is COUNTING ENACTED practice.
    # It does not infer a stable preference, belief, motive, or psychic organization.
    count=c.practical_bicycle_episodes+sum(a in ('PARTICIPATE_JOINT_REPAIR',
          'REHEARSE_BICYCLE_REPAIR') for a in actions)
    if count>=3:
        later='TRY_INDEPENDENT_REPAIR'
    else:
        later='ASK_FOR_ASSISTANCE'
    j.add('later_practical_opportunity',8,540,'world','SEPARATE_MAINTENANCE_NEED',
          dict(bike_chain_slips=True),issuer='TEST_ONLY_OBJECTIVE_EVENT_FIXTURE')
    j.add('child_later_enacted_response',8,545,'child','OBSERVABLE_ACTIVITY',
          dict(action=later),parents=('later_practical_opportunity','child_activity_day5',
                                      'child_history'))
    actions.append(later)
    t=Trace(tuple(j.events),tuple(actions),count,later)
    t.validate()
    return t


def paired_counterfactual(outcomes=('HOURS_CUT','RAISE_WITH_OVERTIME','ROUTINE'),
                          params:WorldParameters=WorldParameters()):
    traces={o:simulate(o,params) for o in outcomes}
    fixed=['father_history','child_history','neighbor_history','theft']
    for id in fixed:
        assert len({t.get(id).hash for t in traces.values()})==1, ('NOT_HELD_FIXED',id)
    assert len({t.get('workplace').hash for t in traces.values()})==len(traces)
    return traces


def output_table(outcomes=('HOURS_CUT','RAISE_WITH_OVERTIME','ROUTINE'),
                 params:WorldParameters=WorldParameters()):
    ts=paired_counterfactual(outcomes,params)
    return [{'workplace':w,
             'parent_time_available':t.get('father_response').fact('available_minutes'),
             'parent_cash_after_work':t.get('father_response').fact('cash_after_work'),
             'parent_action':t.get('father_response').fact('action'),
             'child_day4_action':t.get('child_activity_day4').fact('action'),
             'child_day5_action':t.get('child_activity_day5').fact('action'),
             'later_observable_action':t.child_project_after,
             'practical_episodes_enacted':t.child_practice_count,
             'inferred_psychological_disposition':None,
             'trace_sha256':t.content_digest()} for w,t in ts.items()]


if __name__=='__main__':
    print(json.dumps({'grade':GRADE,'counterfactual':output_table()},indent=2))
