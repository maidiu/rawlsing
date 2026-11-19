"""R2: historically situated activity-object-motive-means relations.

Leontiev/Sève distinction: technical success != fulfillment of the motive; a
single performed operation can belong to multiple contradictory activities.
This is a derived and then actor-owned *research* process, not native V3.
"""
from .types import copy, stable_id, GRADE


def eligible_activities(constitution, recruited_form_ids, encounter):
    """A project can have its own cues or be recruited through an acquired form.

    Contextual-only projects stay dormant absent real cues or a qualified
    FORM->ACTIVITY link. Noncontextual ordinary projects remain available.
    """
    actual_tags={str(t).lower() for c in encounter.cues for t in c.get('tags',[])}
    sources=set(recruited_form_ids)
    result=[]
    for p in constitution.projects:
        if p.get('status','active')!='active': continue
        cue_match=bool(set(t.lower() for t in p.get('cue_terms',[])) & actual_tags)
        recruiting=[link for link in constitution.activity_links
            if link.get('relation')=='RECRUITS_ACTIVITY'
            and link.get('source') in sources and link.get('target')==p['id']
            and (not link.get('contexts') or encounter.location in link['contexts'])]
        if p.get('contextual_only') and not (cue_match or recruiting): continue
        x=copy(p)
        x['recruitment_basis']=['ACTIVITY_CUE'] if cue_match else []
        x['recruitment_basis'] += ['FORM_LINK:'+r['source'] for r in recruiting]
        x['motive']=p.get('motive','UNSPECIFIED_ACQUIRED_MOTIVE')
        x['object']=p['object']
        result.append(x)
    return result


def record_activity_afterlife(actor, own_action, status, outcome, basis, event_ref, object_delta=None):
    """Register actual means and the actor's possible relation to their object.

    The external act never proves satisfaction of the purpose; provenance must
    indicate *which* ongoing activity, if any, was recruited. An injected action
    does not retroactively invent the actor's purpose.
    """
    project_ids={r.removeprefix('project:') for r in basis if r.startswith('project:')}
    histories=[]
    for project in actor.get('projects',[]):
        if project['id'] not in project_ids: continue
        if own_action not in project.get('means',[]):continue
        entry={'event':event_ref,'project':project['id'],
            'operation':own_action,'objective_outcome':outcome,'performed_status':status,
            'practical_object':project['object'],'motive_hypothesis':project.get('motive'),
            'object_transformation':copy(object_delta or {}),
            'motive_realized':'UNDETERMINED_BY_TECHNICAL_OUTCOME','grade':GRADE}
        histories.append(entry)
        project.setdefault('operational_history',[]).append(entry)
    actor.setdefault('activity_history',[]).extend(histories)
    return histories
