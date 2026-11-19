"""READ MODEL for the entire, possibly dormant and contradictory person; pure composition.
No psychology state is minted by materialization. This module is deliberately read-only.
"""
from .types import Constitution, Situated, AccessibleEncounter, copy
from .organism import eligible, ACTIONS


def materialize(actor,world):
    world_rels=[copy(v) for v in world['relations'].values() if actor['id'] in v.get('participants',[])]
    return Constitution(actor=actor['id'],clock=world['clock'],body=copy(actor['body']),
        forms=copy(actor['forms']),links=copy(actor['links']),projects=copy(actor['projects']),
        memories=copy(actor['memories']),traces=copy(actor['traces']),
        other_models=copy(actor['other_models']),self_model=copy(actor['self_model']),
        relations=world_rels,unknowns=list(actor['unknowns']),history_refs=list(actor.get('history_refs',[])))


def actor_access(actor,world):
    """Objective cues are never automatically the actor's concepts or memories."""
    location=world['positions'].get(actor['id'])
    cues=[]; counted=0;receipts=[]
    for x in world['cues']:
        if x.get('location') not in (location,'all'):
            counted+=1;continue
        sense=x.get('modality','visual')
        if sense in ('visual','auditory') and actor['body']['sensor']<x.get('threshold',.05):
            counted+=1;continue
        if x.get('private_to') not in (None,actor['id']):
            counted+=1;continue
        cues.append(copy(x));receipts.append(x['id'])
    env=[]
    site=world['sites'].get(location,{})
    if site.get('access')=='public' or actor['id'] in site.get('admitted',[]):env.append('SITE_ACCESS')
    env+=['REST','WAIT','ORIENT','SIGNAL']
    return AccessibleEncounter(actor['id'],world['clock'],location,cues,sorted(set(env)),receipts,counted)


def _tokens(cues):
    return set(v.lower() for c in cues for v in (c.get('tags',[])+[c.get('kind','')]))


def compose(constitution,access,limit=50):
    """Three streams: direct cue/ongoing project, acquired associative links, qualified traces.
    Does not select a motive, infer actor memory from objective facts, or claim transfer
    where the encoded form's scope prohibits it.
    """
    if constitution.actor!=access.actor:raise ValueError('ACTOR_IDENTITY_MISMATCH')
    forms=constitution.forms; cues=_tokens(access.cues)
    active={}; dormant=[]; inhibited=[]; currents=[]; disagreements=[]
    projects=constitution.projects
    project_tags=set(v.lower() for p in projects if p.get('status','active')=='active' for v in p.get('cue_terms',[]))
    for fid,f in forms.items():
        if f.get('lifecycle') in ('ENDED','DORMANT'):
            dormant.append(fid);continue
        if f.get('body_min',0)>constitution.body['motor']:inhibited.append(fid);continue
        scope=f.get('scope',{})
        if scope.get('locations') and access.location not in scope['locations']:
            dormant.append(fid);continue
        match=set(str(x).lower() for x in f.get('cues',[]))
        if match & (cues|project_tags) or f.get('always_recruitable'):
            active[fid]=copy(f)
    # Associations are admissible only if persisted as functional links.
    for _ in range(3):
        changed=False
        for link in constitution.links:
            src,dst=link.get('source'),link.get('target')
            if src not in active or dst not in forms:continue
            if link.get('contexts') and access.location not in link['contexts']:continue
            if link['relation'] in ('RECRUITS','SUPPORTS') and dst not in active:
                f=forms[dst]
                if f.get('lifecycle') not in ('ENDED','DORMANT') and f.get('body_min',0)<=constitution.body['motor']:
                    active[dst]=copy(f); changed=True
            elif link['relation']=='INHIBITS':
                inhibited.append(dst)
        if not changed:break
    for fid in set(inhibited):active.pop(fid,None)
    # Trace reads are only admitted trace references, not recovered episodic memory.
    traces=[t for t in constitution.traces if set(t.get('cue_terms',[]))&(cues|project_tags)]
    for t in traces[:limit]:currents.append({'kind':'NONDECLARATIVE_TRACE','ref':t['id'],'manifestation':t.get('manifestation','uninterpreted')})
    for p in projects:
        if p.get('status','active')=='active':currents.append({'kind':'ONGOING_ACTIVITY','ref':p['id'],'object':p['object'],'priority':p.get('priority',.5)})
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
    ordered=sorted(actions.values(),key=lambda x:(-x['score'],x['action']))[:limit]
    return Situated(actor=constitution.actor,clock=constitution.clock,recruited=list(active.values()),
       dormant=sorted(set(dormant)),inhibited=sorted(set(inhibited)),currents=currents,
       accessible_cues=access.cues,candidate_actions=ordered,disagreements=disagreements,
       readset=sorted(set(list(active)+[t['id'] for t in traces]+access.access_receipts)),
       unknowns=list(constitution.unknowns))
