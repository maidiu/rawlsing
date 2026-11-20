"""READ MODEL for the entire, possibly dormant and contradictory person; pure composition.
No psychology state is minted by materialization. This module is deliberately read-only.
"""
from .types import Constitution, Situated, AccessibleEncounter, copy
from .organism import eligible, ACTIONS
from .activity import eligible_activities
from .psychodynamics import enact_currents
from .relational_metabolism import derive_relational_metabolism
from .plans import qualified_learned_compositions


def materialize(actor,world):
    world_rels=[copy(v) for v in world['relations'].values() if actor['id'] in v.get('participants',[])]
    return Constitution(actor=actor['id'],clock=world['clock'],body=copy(actor['body']),
        forms=copy(actor['forms']),links=copy(actor['links']),projects=copy(actor['projects']),
        activity_links=copy(actor.get('activity_links',[])),
        composition_methods=copy(actor.get('composition_methods',[])),
        relational_motifs=copy(actor.get('relational_motifs',[])),
        memories=copy(actor['memories']),traces=copy(actor['traces']),
        other_models=copy(actor['other_models']),self_model=copy(actor['self_model']),
        relations=world_rels,unknowns=list(actor['unknowns']),history_refs=list(actor.get('history_refs',[])))


def actor_access(actor,world):
    """Objective cues are never automatically the actor's concepts or memories."""
    location=world['positions'].get(actor['id'])
    cues=[]; counted=0;receipts=[]
    for x in world['cues']:
        # An event in history is not a permanently present sensory object.
        # Materially persistent signs require an explicit, bounded lifetime.
        if not (x.get('clock', -1) <= world['clock'] <= x.get('last_access_clock', -1)):
            counted+=1;continue
        if x.get('location') not in (location,'all'):
            counted+=1;continue
        sense=x.get('modality','visual')
        if sense in ('visual','auditory') and actor['body']['sensor']<x.get('threshold',.05):
            counted+=1;continue
        if x.get('private_to') not in (None,actor['id']):
            counted+=1;continue
        cues.append(copy(x));receipts.append(x['id'])
    # Co-presence is an objective present opportunity, not an assertion about
    # the other's intentions, consent, feelings, or accessible psychology.
    if actor['body']['sensor'] >= .05:
        for other,where in sorted(world['positions'].items()):
            if other!=actor['id'] and where==location:
                cues.append({'id':'presence:'+other+':'+str(world['clock']),
                    'clock':world['clock'],'kind':'coactor_present',
                    'tags':['coactor',other],'source_actor':other,'location':location,
                    'modality':'present','description':'co-present other actor'})
    env=[]
    site=world['sites'].get(location,{})
    if site.get('access')=='public' or actor['id'] in site.get('admitted',[]):env.append('SITE_ACCESS')
    env+=['REST','WAIT','ORIENT','SIGNAL']
    return AccessibleEncounter(actor['id'],world['clock'],location,cues,sorted(set(env)),receipts,counted)


def _tokens(cues):
    return set(v.lower() for c in cues for v in (c.get('tags',[])+[c.get('kind','')]))


def _form_in_scope(form,access):
    scope=form.get('scope',{})
    if scope.get('locations') and access.location not in scope['locations']:
        return False
    counterpart=scope.get('counterpart')
    if counterpart and not any(c.get('source_actor')==counterpart for c in access.cues):
        return False
    return True

def compose(constitution,access,limit=50):
    """Three streams: direct cue/ongoing project, acquired associative links, qualified traces.
    Does not select a motive, infer actor memory from objective facts, or claim transfer
    where the encoded form's scope prohibits it.
    """
    if constitution.actor!=access.actor:raise ValueError('ACTOR_IDENTITY_MISMATCH')
    forms=constitution.forms; cues=_tokens(access.cues)
    active={}; dormant=[]; inhibited=[]; currents=[]; disagreements=[]
    # A contextual project that is not presently recruited must NOT prime its
    # own cues. Otherwise an unseen future project bootstraps a form into the
    # present, and the form is then misrepresented as the project's cause.
    seed_projects=eligible_activities(constitution,(),access)
    project_tags=set(v.lower() for p in seed_projects for v in p.get('cue_terms',[]))
    for fid,f in forms.items():
        if f.get('lifecycle') in ('ENDED','DORMANT'):
            dormant.append(fid);continue
        if f.get('body_min',0)>constitution.body['motor']:inhibited.append(fid);continue
        if not _form_in_scope(f,access):
            dormant.append(fid);continue
        match=set(str(x).lower() for x in f.get('cues',[]))
        if match & (cues|project_tags) or f.get('always_recruitable'):
            active[fid]=copy(f)
    # P012: evidence-bounded reachability to a real fixed point, independently
    # of arbitrary link order or a three-pass depth limit. A qualifying
    # inhibitor blocks its target's ability to become a recruitment conduit;
    # it cannot first recruit a descendant and then disappear at the end.
    #
    # We use a conservative two-stage lattice: positive possible reachability,
    # then inhibitor veto by all potential qualified active sources, followed
    # by positive reachability without vetoed conduits. This may over-suppress
    # under opposing cycles; it never fabricates the affected form's action.
    seed=set(active)
    qualified={fid for fid,f in forms.items()
        if f.get('lifecycle') not in ('ENDED','DORMANT')
        and f.get('body_min',0)<=constitution.body['motor']
        and _form_in_scope(f,access)}
    valid_links=[link for link in constitution.links
        if link.get('source') in forms and link.get('target') in forms
        and (not link.get('contexts') or access.location in link['contexts'])]
    # PRE-A0's explicitly admitted relation functions must do work; not
    # merely appear in a relation-history report. Activation and suppression
    # still respect the form's own scope and bodily eligibility.
    positive=[link for link in valid_links if link.get('relation') in
              ('RECRUITS','SUPPORTS','ACTIVATES','REINFORCES')]
    negative=[link for link in valid_links if link.get('relation') in
              ('INHIBITS','SUPPRESSES')]

    def closure(start, blocked=frozenset()):
        reached=set(start)&qualified-set(blocked)
        # Monotonic form set grows at most len(qualified) times, cycles stop.
        while True:
            added={l['target'] for l in positive
                   if l['source'] in reached and l['target'] in qualified
                   and l['target'] not in blocked}
            newer=reached|added
            if len(newer)==len(reached):return reached
            reached=newer

    potentially_active=closure(seed)
    vetoed={l['target'] for l in negative if l['source'] in potentially_active}
    inhibited.extend(sorted(vetoed))
    active={fid:copy(forms[fid]) for fid in closure(seed,vetoed)}
    # History-made links to activities can recruit an ongoing project under
    # a new cue. Its object/motive remains separate from its possible means.
    projects=eligible_activities(constitution,active.keys(),access)
    # Trace reads are only admitted trace references, not recovered episodic memory.
    traces=[t for t in constitution.traces if set(t.get('cue_terms',[]))&(cues|project_tags)]
    for t in traces[:limit]:currents.append({'kind':'NONDECLARATIVE_TRACE','ref':t['id'],'manifestation':t.get('manifestation','uninterpreted')})
    for field in constitution.relations:
        if 'REPEATED_JOINT_ACT_OBSERVED' in field.get('observed_patterns',[]):
            counterpart=[x for x in field['participants'] if x!=constitution.actor]
            if any(c.get('source_actor') in counterpart for c in access.cues):
                currents.append({'kind':'WORLD_RELATIONAL_FIELD_OBSERVATION', 'ref':field['id'],
                                 'objective_pattern':'REPEATED_JOINT_ACT_OBSERVED',
                                 'joint_capability_unproved':True,
                                 'not_personal_investment':True})
    for p in projects:
        if p.get('status','active')=='active':currents.append({'kind':'ONGOING_ACTIVITY','ref':p['id'],'object':p['object'],'motive':p.get('motive','UNSPECIFIED_ACQUIRED_MOTIVE'),
            'priority':p.get('priority',.5),'recruitment_basis':p.get('recruitment_basis',[]),
            'means':copy(p.get('means',[])),
            'latest_lived_attempt':copy(p.get('latest_lived_attempt'))})
    for fid,f in active.items():
        currents.append({'kind':f['kind'],'ref':fid,'object':f.get('object'),'actor_access':f.get('access','tacit')})
    for a in constitution.links:
        if a['relation']=='COMPETES' and a['source'] in active and a['target'] in active:
            disagreements.append({'a':a['source'],'b':a['target'],'reason':'ADMITTED_COMPETITION'})
    actions={}
    for fid,f in active.items():
        for a in f.get('enables',[]):
            status,why=eligible(constitution.body,a)
            if status:
                q=actions.setdefault(a,{'action':a,'score':.1,'basis':[],'opportunity':'ACQUIRED'})
                q['score']+=.24*f.get('strength',.5);q['basis'].append(fid)
    for p in projects:
        if p.get('status','active')!='active':continue
        for a in p.get('means',[]):
            status,why=eligible(constitution.body,a)
            if status:
                q=actions.setdefault(a,{'action':a,'score':.1,'basis':[],'opportunity':'PROJECT'})
                q['score']+=.4*p.get('priority',.5);q['basis'].append('project:'+p['id'])
                q.setdefault('practical_objects',[]).append(p['object'])
                q.setdefault('motive_hypotheses',[]).append(p.get('motive','UNKNOWN'))
    # Developmentally rudimentary orienting and self-preserving actions remain possible
    # even with no acquired conceptual operations.
    for a in ('WAIT','REST','ORIENT','SIGNAL'):
        status,why=eligible(constitution.body,a)
        if status:actions.setdefault(a,{'action':a,'score':.06,'basis':['organism'],'opportunity':'ORGANISM'})
    for a,q in actions.items():
        if a in ('WORK','REPAIR','SING','JOIN','MAKE_SPACE','OPEN_HALL') and access.location not in ('workshop','home','hall'):
            q['score']*=.45
        if a=='REST' and constitution.body['rest']<.45:q['score']+=1.0
        if a=='EAT' and constitution.body['nutrition']<.5:q['score']+=1.0
        if a=='SIGNAL' and constitution.body['comfort']<.4:q['score']+=.6
    # An inhibited form can still have an indirect, historically admitted
    # effect on another form or action. Never reinstate its direct capabilities.
    relational=derive_relational_metabolism(constitution,access,active,vetoed)
    currents+=relational['currents']
    dynamics=enact_currents(constitution,access,active,actions.values(),
                             relational=relational)
    currents+=dynamics['currents']
    # These effects are *derived* from present bodily state and historically
    # acquired forms, never silently committed as an event or a new mind state.
    inhibited+=['action:'+x['action'] for x in dynamics['suspended']]
    learned=qualified_learned_compositions(constitution,access,active,projects,
                                          dynamics['candidate_actions'])
    ordered=sorted(dynamics['candidate_actions'],key=lambda x:(-x['score'],x['action']))[:limit]
    return Situated(actor=constitution.actor,clock=constitution.clock,recruited=list(active.values()),
       dormant=sorted(set(dormant)),inhibited=sorted(set(inhibited)),currents=currents,
       accessible_cues=access.cues,candidate_actions=ordered,disagreements=disagreements,
       readset=sorted(set(list(active)+list(vetoed)+relational['readset']+
                           [t['id'] for t in traces]+access.access_receipts)),
       unknowns=list(constitution.unknowns),antagonisms=dynamics['antagonisms'],
       suspended_actions=dynamics['suspended'],learned_compositions=learned)
