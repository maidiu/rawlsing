"""Unlearned, actor-specific possible practical compositions.

A possible trial is neither an acquired composition method nor a motive nor
successful transfer. It uses presently available means and an *existing*
activity object, but remains untried and disposable. Objective world settlement
and later fictional formation are separate. Sourcefree, provisional.
"""
from .types import GRADE, stable_id
from .organism import ACTIONS

NON_TRIAL = {'WAIT', 'REST', 'ORIENT'}
MAX_PROSPECTIVE = 8


def candidate_trials(constitution, situated, limit=MAX_PROSPECTIVE):
    """Derive bounded candidate new combinations, never mutate actor state.

    A candidate requires two distinct historically acquired, currently
    recruited practices. One practical means participates in an existing
    current project, another is prospectively available from a different
    practice. That establishes an *actor-relevant trial* not learned skill.
    """
    if constitution.actor != situated.actor:
        raise ValueError('PROSPECTION_ACTOR_MISMATCH')
    if not 0 <= limit <= MAX_PROSPECTIVE:
        raise ValueError('UNBOUNDED_PROSPECTION')
    available={o['action'] for o in situated.candidate_actions}
    forms={f['id']:f for f in situated.recruited
           if f.get('kind')=='PRACTICE' and f.get('origin')
           and f.get('lifecycle','ACTIVE')=='ACTIVE'}
    sources={}
    for fid, form in forms.items():
        for action in form.get('enables',[]):
            if action in available and action in ACTIONS and action not in NON_TRIAL:
                sources.setdefault(action,set()).add(fid)
    current={c['ref'] for c in situated.currents
             if c.get('kind')=='ONGOING_ACTIVITY' and c.get('ref')}
    acquired={tuple(x['operations']) for x in situated.learned_compositions}
    trials=[]
    for project in constitution.projects:
        if project.get('status','active')!='active' or project['id'] not in current:
            continue
        for first in project.get('means',[]):
            for second in sorted(sources):
                if first == second or first not in sources:
                    continue
                if (first,second) in acquired:
                    continue
                for a in sorted(sources[first]):
                    for b in sorted(sources[second]):
                        if a==b:
                            continue
                        method_id=stable_id('prospect',{
                            'actor':constitution.actor,'project':project['id'],
                            'first':first,'second':second,'forms':[a,b]})
                        trials.append({
                            'id':method_id,'actor':constitution.actor,
                            'activity_ref':project['id'],
                            'existing_project_object':project.get('object'),
                            'operations':[first,second],
                            'source_forms':[a,b],
                            'state':'PROSPECTIVE_UNTRIED',
                            'actor_possible_not_acquired_method':True,
                            'new_motive_not_inferred':True,
                            'no_anticipated_world_success':True,
                            'evidence_basis':['project:'+project['id'],
                                              'form:'+a,'form:'+b],
                            'grade':GRADE})
                        if len(trials)>=limit:
                            return trials
    return trials
