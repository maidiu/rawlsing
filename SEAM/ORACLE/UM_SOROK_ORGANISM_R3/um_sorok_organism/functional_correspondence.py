"""SORACLE R11 / Astra 1,3,4,7,16: actor-grounded functional correspondences.

A new end cannot be recognized elsewhere by an omniscient 'solidarity' label.
A sourcefree semantic proposal must cite the *actor's* earlier real trial and
a different *personally perceived* later sign. The accepted correspondence
is initially valid for at most one prospective trial, not an acquired doctrine.
It may be wrong; its use does not prove its anticipated consequence.
"""
from .types import copy, stable_id, GRADE


def signature(actor, cue):
    if type(cue) is not dict:
        return []
    body=actor.get('body',{})
    language=body.get('language',0)
    if type(language) not in (int,float):
        raise ValueError('FUNCTIONAL_INVALID_LANGUAGE')
    modality=cue.get('modality')
    if language < .25:
        return ['sensory:'+modality] if modality in (
            'auditory','visual','tactile','olfactory','present') else []
    terms=cue.get('tags',[])
    if not isinstance(terms,list):
        return []
    return sorted(set(x.casefold() for x in terms
                      if type(x) is str and x.strip()))[:16]


def _dissimilar_means_basis(actor, experience, event_ref, end, trial, sign):
    """Two actual lived operations and a shared bodily difference.

    This licenses a fallible new means hypothesis, not sameness of ends.
    Object-specific and Other-addressed ends retain their original boundary.
    """
    op=(experience.get('felt_enactment') or {}).get('attempted_operation')
    if (not experience.get('participated') or op==trial.get('operation')
            or op in end.get('possible_means',[])
            or end.get('origin_material_object_ref') is not None
            or end.get('addressed_party_ref') is not None
            or sign.get('source_actor')!=actor['id']
            or sign.get('kind')!='performed_'+str(op).lower()):
        return None
    rows=actor.get('lived_genesis_episodes',[])
    earlier=[x for x in rows if x.get('actor')==actor['id']
             and x.get('event_ref')==trial.get('event_ref')
             and x.get('experience_ref')==trial.get('experience_ref')
             and x.get('actor_felt_attempt')==trial.get('operation')]
    later=[x for x in rows if x.get('actor')==actor['id']
           and x.get('event_ref')==event_ref
           and x.get('experience_ref')==experience.get('ref')
           and x.get('actor_felt_attempt')==op
           and sign['id'] in x.get('received_sign_refs',[])]
    if len(earlier)!=1 or len(later)!=1:return None
    a,b=earlier[0],later[0]
    if (type(a.get('clock')) is not int or type(b.get('clock')) is not int
            or a['clock']>=b['clock'] or b['clock']!=experience.get('clock')
            or a.get('location')==b.get('location')
            or b.get('location')!=experience.get('location')
            or a.get('unfinished_own_activity') or b.get('unfinished_own_activity')):
        return None
    shared=sorted(set(a.get('received_relief',{}))&set(b.get('received_relief',{})))
    if not shared:return None
    return {'earlier_episode_ref':a['id'],'later_episode_ref':b['id'],
            'earlier_operation':trial['operation'],'later_operation':op,
            'earlier_location':a['location'],'later_location':b['location'],
            'shared_lived_relief_axes':shared,
            'not_proof_of_same_good_or_cause':True}


def propose_actor_lived_correspondences(actor, experience, event_ref):
    """Evidence-limited candidate for the EXISTING semantic development owner.

    Its evidence is a prior attempted end-trial and this actor's later
    independently experienced performance. Does not infer motive, beneficiary
    or sameness of goods. Produces a candidate for optional model nomination.
    """
    if actor.get('id')!=experience.get('actor'):
        raise ValueError('FUNCTIONAL_FOREIGN_EXPERIENCE')
    if not experience.get('participated') or not experience.get('felt_enactment'):
        return []
    operation=experience['felt_enactment'].get('attempted_operation')
    if type(operation) is not str:
        return []
    signs=[c for c in experience.get('perceived_cues',[])
           if type(c) is dict and type(c.get('id')) is str]
    if not signs:return []
    candidates=[]
    for end in actor.get('possible_ends',[])[-64:]:
        if end.get('status')!='POSSIBLE_NOT_ACQUIRED_MOTIVE':
            continue
        trials=[t for t in end.get('trial_history',[])
                if type(t) is dict and t.get('event_ref')!=event_ref
                and t.get('experience_ref')]
        if not trials:
            continue
        novel=operation not in end.get('possible_means',[])
        original_terms={x.casefold() for x in end.get('cue_terms',[])
                        if type(x) is str}
        for sign in signs:
            sig=signature(actor,sign)
            # Only a new personally available distinction warrants a new
            # proposed correspondence, not re-labelling the same cue.
            if not sig or (original_terms and set(sig)&original_terms):
                continue
            if any(b.get('possible_end_ref')==end['id']
                   and b.get('origin_received_cue_ref')==sign['id']
                   for b in actor.get('functional_bindings',[])):
                continue
            basis=None
            if novel:
                basis=_dissimilar_means_basis(actor,experience,event_ref,end,trials[-1],sign)
                if basis is None:continue
            candidate={
                'kind':'ACQUIRE_FUNCTIONAL_CORRESPONDENCE',
                'possible_end_ref':end['id'],
                'prior_trial_ref':trials[-1]['id'],
                'perceived_cue_ref':sign['id'],
                'different_historical_event_ref':trials[-1]['event_ref'],
                'candidate_operation':operation,
                'hypothesis':'SAME_POSSIBLE_DIFFERENCE_MIGHT_BE_RELEVANT_HERE',
                'use_scope':'ONE_QUALIFIED_PROSPECTIVE_TRIAL',
                'not_established_causal_function':True,
                'not_necessarily_conscious_analogy':True,
                'source_grade':'SOURCEFREE_CONTRAST_NOT_EMPIRICAL_ANALOGY',
            }
            if basis is not None:
                candidate['dissimilar_means_basis']=basis
                candidate['hypothesis']='DIFFERENT_OPERATION_MIGHT_MEDIATE_THIS_POSSIBLE_END'
            candidates.append(candidate)
            break
    return candidates[:3]


def admit_functional_correspondence(actor, experience, event_ref, candidate):
    if actor.get('id')!=experience.get('actor') or not event_ref:
        raise ValueError('FUNCTIONAL_ACTOR_MISMATCH')
    end_ref=candidate.get('possible_end_ref')
    ends=[x for x in actor.get('possible_ends',[])
          if x.get('id')==end_ref and x.get('status')==
             'POSSIBLE_NOT_ACQUIRED_MOTIVE']
    if len(ends)!=1:
        raise ValueError('FUNCTIONAL_UNQUALIFIED_END')
    end=ends[0]
    prior=[t for t in end.get('trial_history',[])
           if t.get('id')==candidate.get('prior_trial_ref')
           and t.get('event_ref')!=event_ref]
    if len(prior)!=1:
        raise ValueError('FUNCTIONAL_NO_EARLIER_REAL_TRIAL')
    received=[x for x in experience.get('perceived_cues',[])
              if type(x) is dict and
              x.get('id')==candidate.get('perceived_cue_ref')]
    if len(received)!=1:
        raise ValueError('FUNCTIONAL_CUE_NOT_ACTOR_PERCEIVED')
    operation=candidate.get('candidate_operation')
    novel=operation not in end.get('possible_means',[])
    if ((experience.get('felt_enactment') or {}).get('attempted_operation')
            !=operation):
        raise ValueError('FUNCTIONAL_NO_CURRENT_ENACTMENT')
    basis=None
    if novel:
        matches=[p for p in propose_actor_lived_correspondences(actor,experience,event_ref)
                 if p.get('dissimilar_means_basis') and
                 p['possible_end_ref']==end_ref and
                 p['prior_trial_ref']==candidate.get('prior_trial_ref') and
                 p['perceived_cue_ref']==candidate.get('perceived_cue_ref') and
                 p['candidate_operation']==operation]
        if len(matches)!=1 or matches[0]['dissimilar_means_basis']!=candidate.get('dissimilar_means_basis'):
            raise ValueError('FUNCTIONAL_NO_QUALIFIED_DISSIMILAR_MEANS')
        basis=copy(matches[0]['dissimilar_means_basis'])
    elif 'dissimilar_means_basis' in candidate:
        raise ValueError('FUNCTIONAL_FALSE_NOVEL_MEANS')
    if candidate.get('use_scope')!='ONE_QUALIFIED_PROSPECTIVE_TRIAL':
        raise ValueError('FUNCTIONAL_UNBOUNDED_GENERALIZATION')
    sig=signature(actor,received[0])
    if not sig:raise ValueError('FUNCTIONAL_UNDIFFERENTIATED_SIGN')
    ref=stable_id('functional_bridge',{
        'actor':actor['id'],'end':end_ref,'event':event_ref,
        'sign':received[0]['id'],'prior':prior[0]['id']})
    if any(b.get('id')==ref for b in actor.get('functional_bindings',[])):
        raise ValueError('FUNCTIONAL_DUPLICATE_BINDING')
    record={
        'id':ref,'actor':actor['id'],'possible_end_ref':end_ref,
        'origin_event':event_ref,'origin_experience_ref':experience.get('ref'),
        'origin_received_cue_ref':received[0]['id'],
        'prior_trial_history_ref':prior[0]['id'],
        'signature':sig,'scope':'ONE_QUALIFIED_PROSPECTIVE_TRIAL',
        'status':'POSSIBLE_FUNCTIONAL_SIMILARITY_NOT_BELIEF',
        'actor_explicit_concept':'NOT_INFERRED',
        'beneficiary_identity':'NOT_INFERRED',
        'objective_success':'UNKNOWN_NOT_A_CAUSAL_COMPARISON',
        'empirical_learning_law':'NOT_ESTABLISHED','grade':GRADE,
    }
    if basis is not None:
        record['dissimilar_means_basis']=basis
        record['candidate_operation']=operation
    actor.setdefault('functional_bindings',[]).append(record)
    return {'kind':'ACQUIRE_FUNCTIONAL_CORRESPONDENCE',
            'binding_ref':ref,'possible_end_ref':end_ref,
            'status':'ONE_TRIAL_POSSIBILITY_NOT_DURABLE_TRANSFER',
            'grade':GRADE}


def possible_functional_revisions(actor, experience, event_ref):
    """Historically earned local consolidation or inhibition of a lived means.

    The first exploratory trial is not its own consolidation. An independent
    later relevant episode must be lived, and the semantic owner may abstain.
    The old possibility and its attempted courses are never deleted.
    """
    aid=actor.get('id')
    operation=experience.get('own_action')
    clock=experience.get('clock')
    if (experience.get('actor')!=aid or type(clock) is not int
            or type(operation) is not str or not experience.get('participated')
            or (experience.get('felt_enactment') or {}).get('attempted_operation')!=operation):
        return []
    signs=[c for c in experience.get('perceived_cues',[])
           if type(c) is dict and c.get('source_actor')==aid
           and c.get('kind')=='performed_'+operation.lower()
           and type(c.get('id')) is str]
    if len(signs)!=1:return []
    rows=actor.get('lived_genesis_episodes',[])
    current=[e for e in rows if e.get('actor')==aid
             and e.get('event_ref')==event_ref
             and e.get('experience_ref')==experience.get('ref')
             and e.get('clock')==clock
             and e.get('location')==experience.get('location')
             and e.get('actor_felt_attempt')==operation
             and signs[0]['id'] in e.get('received_sign_refs',[])]
    if len(current)!=1:return []
    current=current[0]
    ends={e['id']:e for e in actor.get('possible_ends',[])
          if e.get('status')=='POSSIBLE_NOT_ACQUIRED_MOTIVE'}
    by_id={e['id']:e for e in rows if e.get('actor')==aid}
    by_event={(e.get('event_ref'),e.get('experience_ref')):e
              for e in rows if e.get('actor')==aid}
    candidates=[]
    for bridge in actor.get('functional_bindings',[])[-128:]:
        status=bridge.get('status')
        if status not in ('POSSIBLE_FUNCTIONAL_SIMILARITY_NOT_BELIEF',
                          'ACQUIRED_CONDITIONAL_FUNCTIONAL_MEANS'):
            continue
        basis=bridge.get('dissimilar_means_basis')
        end=ends.get(bridge.get('possible_end_ref'))
        if (type(basis) is not dict or not end or bridge.get('actor')!=aid
                or bridge.get('candidate_operation')!=operation
                or basis.get('later_location')!=current['location']
                or end.get('origin_material_object_ref') is not None
                or end.get('addressed_party_ref') is not None):
            continue
        history=bridge.get('revision_history',[])
        if any(h.get('event_ref')==event_ref for h in history):continue
        seed=by_id.get(basis.get('later_episode_ref'))
        if not seed or seed.get('event_ref')!=bridge.get('origin_event'):continue
        trials=[t for t in end.get('trial_history',[])
                if t.get('functional_bridge_ref')==bridge['id']
                and t.get('operation')==operation
                and t.get('event_ref')!=event_ref]
        if not trials:continue
        first=trials[0]
        tested=by_event.get((first.get('event_ref'),first.get('experience_ref')))
        if (not tested or tested.get('actor_felt_attempt')!=operation
                or tested.get('location')!=current['location']
                or not seed['clock']<tested['clock']<clock):
            continue
        shared=set(basis.get('shared_lived_relief_axes',[]))
        reproduced=sorted(shared & set(seed.get('received_relief',{}))
                          & set(tested.get('received_relief',{}))
                          & set(current.get('received_relief',{})))
        adverse=bool(current.get('unfinished_own_activity')
                     or current.get('personally_lived_adverse_course'))
        if status=='POSSIBLE_FUNCTIONAL_SIMILARITY_NOT_BELIEF':
            if (history or adverse or not reproduced
                    or first.get('actor_experienced_status')!='PERFORMED'
                    or experience.get('status')!='PERFORMED'
                    or (experience.get('own_practical_selection') or {}).get('possible_end_trial')):
                continue
            mode='CONSOLIDATE'
        else:
            if (not history or history[-1].get('mode')!='CONSOLIDATE'
                    or history[-1].get('clock',clock)>=clock or not adverse):
                continue
            mode='SUSPEND'
        candidates.append({
            'kind':'REVISE_FUNCTIONAL_CORRESPONDENCE',
            'binding_ref':bridge['id'],'mode':mode,
            'revision_basis':{
                'possible_end_ref':end['id'],
                'initial_episode_ref':seed['id'],
                'first_bridge_trial_ref':first['id'],
                'first_bridge_trial_episode_ref':tested['id'],
                'later_episode_ref':current['id'],
                'later_event_ref':event_ref,'later_experience_ref':experience['ref'],
                'later_received_sign_ref':signs[0]['id'],
                'operation':operation,'location':current['location'],
                'reproduced_relief_axes':reproduced,
                'later_incomplete':bool(current.get('unfinished_own_activity')),
                'later_adverse_axes':sorted(current.get('personally_lived_adverse_course',{})),
                'prior_status':status,
                'previous_revision_ref':history[-1]['id'] if history else None,
            },
        })
        if len(candidates)>=3:break
    return candidates


def admit_functional_revision(actor, experience, event_ref, candidate):
    """Same actor, same bridge identity, recomputed historical occasion."""
    if set(candidate)!={'kind','binding_ref','mode','revision_basis'}:
        raise ValueError('FUNCTIONAL_REVISION_UNQUALIFIED_FIELDS')
    matches=[c for c in possible_functional_revisions(actor,experience,event_ref)
             if c==candidate]
    if len(matches)!=1:raise ValueError('FUNCTIONAL_REVISION_NO_LIVED_BASIS')
    bridge=next(b for b in actor['functional_bindings'] if b['id']==candidate['binding_ref'])
    mode=candidate['mode']
    previous=bridge['status']
    status=('ACQUIRED_CONDITIONAL_FUNCTIONAL_MEANS' if mode=='CONSOLIDATE'
            else 'SUSPENDED_CONDITIONAL_FUNCTIONAL_MEANS')
    revision={'id':stable_id('functional_revision',{'binding':bridge['id'],
                  'event':event_ref,'mode':mode}),
              'event_ref':event_ref,'clock':experience['clock'],'mode':mode,
              'previous_status':previous,'new_status':status,
              'basis':copy(candidate['revision_basis']),'grade':GRADE}
    bridge.setdefault('revision_history',[]).append(revision)
    bridge['status']=status
    return {'kind':candidate['kind'],'binding_ref':bridge['id'],
            'revision_ref':revision['id'],'status':status,'grade':GRADE}


def project_functional_correspondences(constitution, access):
    if constitution.actor!=access.actor:
        raise ValueError('FUNCTIONAL_COMPOSITION_ACTOR_MISMATCH')
    active=[];readset=[]
    already_used={
        trial.get('functional_bridge_ref')
        for end in constitution.possible_ends
        for trial in end.get('trial_history',[])
        if type(trial) is dict and trial.get('functional_bridge_ref')
    }
    body={'body':constitution.body}
    for bridge in getattr(constitution,'functional_bindings',[]):
        reusable=bridge.get('status')=='ACQUIRED_CONDITIONAL_FUNCTIONAL_MEANS'
        if not reusable and (bridge.get('status')!='POSSIBLE_FUNCTIONAL_SIMILARITY_NOT_BELIEF'
                or bridge.get('id') in already_used):
            continue
        end=next((x for x in constitution.possible_ends
                  if x.get('id')==bridge.get('possible_end_ref')
                  and x.get('status')=='POSSIBLE_NOT_ACQUIRED_MOTIVE'),None)
        if not end:
            continue
        matches=[cue for cue in access.cues
                 if set(signature(body,cue))&set(bridge.get('signature',[]))]
        if not matches:
            continue
        projected={
            'binding_ref':bridge['id'],'possible_end_ref':end['id'],
            'current_perceived_candidate_refs':[
                c['id'] for c in matches if type(c.get('id')) is str],
            'prior_trial_history_ref':bridge['prior_trial_history_ref'],
            'would_require_qualified_trial':True,
            'not_sameness_proof':True,
            'not_actor_conscious_reason':True,
            'grade':GRADE,
        }
        if bridge.get('dissimilar_means_basis'):
            if access.location!=bridge['dissimilar_means_basis']['later_location']:
                continue
            projected['candidate_operation']=bridge['candidate_operation']
            projected['dissimilar_means_basis']=copy(bridge['dissimilar_means_basis'])
            if reusable:
                projected['conditional_means_revision_ref']=bridge['revision_history'][-1]['id']
                projected['reusable_contextual_means_not_motive']=True
        active.append(projected)
        readset.append(bridge['id'])
    return {'active':active,'readset':sorted(set(readset)),
            'identity_to_means_not_proved':True,'grade':GRADE}
