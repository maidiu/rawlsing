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
        if (bridge.get('status')!='POSSIBLE_FUNCTIONAL_SIMILARITY_NOT_BELIEF'
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
        active.append(projected)
        readset.append(bridge['id'])
    return {'active':active,'readset':sorted(set(readset)),
            'identity_to_means_not_proved':True,'grade':GRADE}
