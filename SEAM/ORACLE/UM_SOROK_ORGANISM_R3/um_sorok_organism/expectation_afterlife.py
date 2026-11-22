"""SORACLE R13 — world consequences and psychic expectations run on two clocks.

An objective allocation can close now; an actor's anticipation may remain
uninterpreted through other events, be revised years later, and reshape a
situated future attempt. We compare only signs the actor could receive, never
counterfactual non-encounters. A sign produced by their own previous choice
is not independent confirmation of their theory.

First writer: existing development.admit(APPRAISE_EXPECTED_DIFFERENCE).
First reader: existing constitution practical alternatives and semantic choice.
This is a sourcefree fictional policy, not a universal preference for truth,
a measured updating law, or an imported theory of conscious reflection.
"""
from .types import GRADE, copy


def source_qualified_appraisal_candidates(actor, experience, event_ref):
    if actor.get('id')!=experience.get('actor') or not event_ref:
        raise ValueError('APPRAISAL_FOREIGN_ACTOR_OR_EVENT')
    cues=[c for c in experience.get('perceived_cues',[])
          if type(c) is dict and type(c.get('id')) is str]
    if not cues:return []
    candidates=[]
    for exp in actor.get('expectations',[])[-128:]:
        if (type(exp) is not dict or exp.get('origin_event')==event_ref
                or not exp.get('id')):
            continue
        if exp.get('state') not in (
            'STILL_PENDING','MEANING_UNRESOLVED',
            'MATERIAL_OBSTACLE_SUSPECTED',
            'ACTOR_INTERPRETS_DISAPPOINTED',
            'ACTOR_INTERPRETS_SUPPORTED'):
            continue
        signs=exp.get('anticipated_difference',{}).get('sign_tags',[])
        if type(signs) is not list or not signs:
            continue
        wished={s.casefold() for s in signs if type(s) is str}
        matching=[c for c in cues
                  if wished & {str(t).casefold() for t in c.get('tags',[])
                               if type(t) is str}]
        for cue in matching:
            if any(x.get('perceived_cue_ref')==cue['id']
                   for x in exp.get('appraisal_history',[])):
                continue
            source_actor=cue.get('source_actor')
            # Sources of signals are not necessarily their causes; the
            # actual world and actor's inquiry must qualify every inference.
            origin=('SELF_POSITIONED_SOURCED_SIGN'
                    if source_actor==actor['id'] else
                    'OTHER_OR_WORLD_SOURCED_SIGN'
                    if type(source_actor) is str else
                    'SIGN_SOURCE_NOT_ACTOR_IDENTIFIED')
            candidates.append({
                'expectation_ref':exp['id'],
                'prior_event_ref':exp['origin_event'],
                'later_event_ref':event_ref,
                'source_perceived_cue_ref':cue['id'],
                'cue_origin_class_analyst_only':origin,
                'recognized_signal_feature_set':sorted(
                    wished & set(x.casefold() for x in cue.get('tags',[])
                                 if type(x) is str)),
                'current_interpretation':exp.get('state'),
                'possible_actor_appraisals':[
                    'MEANING_UNRESOLVED','STILL_PENDING',
                    'ACTOR_INTERPRETS_SUPPORTED',
                    'ACTOR_INTERPRETS_DISAPPOINTED',
                    'MATERIAL_OBSTACLE_SUSPECTED'],
                'self_selected_evidence_not_external_proof':True,
                'sign_is_not_causal_warrant_for_outcome':True,
                'other_unselected_paths':'UNKNOWN_NOT_OBSERVED',
                'source_grade':GRADE,
            })
    return candidates[:8]


def conservative_appraisal_proposal(candidates):
    """Fallback refuses a causal verdict while allowing actual reappraisal.

    A live semantic constructor can instead propose a fallible interpretation
    from actor-specific history, with the existing typed owner verifying that
    the claimed sign was actually received.
    """
    if len(candidates)!=1:
        return []
    row=candidates[0]
    if row['current_interpretation'] not in (
        'STILL_PENDING','MATERIAL_OBSTACLE_SUSPECTED'):
        return []
    return [{
        'kind':'APPRAISE_EXPECTED_DIFFERENCE',
        'expectation_ref':row['expectation_ref'],
        'perceived_cue_ref':row['source_perceived_cue_ref'],
        'appraisal':'MEANING_UNRESOLVED',
        'no_retroactive_objective_cause':True,
        'not_a_final_interpretation':True,
        'grade':GRADE,
    }]


def annotate_practical_expectations(constitution,options):
    """A personally revised expectation modifies the *particular* course.

    No disappointment changes another project's score just because the
    projects happen to share an action name. The LLM can use this actor's
    prior appraisal to propose different attempts; fallback may choose
    another existing means but cannot assert certainty or project defeat.
    """
    known={}
    for exp in constitution.expectations[-256:]:
        if (type(exp) is dict and exp.get('project_id')
                and exp.get('state') not in (None,'STILL_PENDING')):
            known.setdefault(exp['project_id'],[]).append(exp)
    annotations=0
    for opt in options:
        for alt in opt.get('practical_alternatives',[]):
            pid=alt.get('project_id')
            records=known.get(pid,[])
            if not records:continue
            # Keep competing appraisals and evidence grades; later appraisals
            # do not rewrite older attempts into intentional prophecy.
            alt['prior_actor_appraisals']=[{
                'expectation_ref':x['id'],
                'state':x['state'],
                'appraisal_event_refs':[e.get('event') for e in
                                        x.get('appraisal_history',[])],
                'objective_success':'NOT_INFERRED',
                'not_actor_conscious_report':True,
            } for x in records[-12:]]
            alt['sourcefree_revised_future_approach']=[
                'REPEAT_OR_SUSTAIN','VARY_MEANS','WITHHOLD','SEEK_OTHER_EVIDENCE']
            alt['no_global_preference_for_novelty_or_confirmation']=True
            annotations+=1
    return {'annotated_alternative_count':annotations,
            'readset':sorted(set(
                x['id'] for group in known.values() for x in group)),
            'actor_interpretation_not_objective_event':True,'grade':GRADE}
