"""R3 provisional, history-qualified and *non-unitary* psychodynamic currents.

Not universal clinical affect science. No one scalar sums together desire, care,
prohibition, bodily need, or activity. Only acquired actor-scoped tendencies can
alter voluntary action eligibility. Opposed tendencies are conserved rather than
silently sorted into one rational preference. The current is a *situated read*,
not a new source-of-truth for the psyche and not a mind-reading public tip.
"""
from .types import copy, GRADE
from .organism import ACTIONS
import math

POLARITIES = {'APPROACH', 'WITHHOLD'}


def validate_tendencies(form):
    # Existing form-strength and motor threshold are executable quantities,
    # not unconstrained strings supplied by a construction model.
    if not isinstance(form,dict):raise ValueError('INVALID_ACQUIRED_FORM_PARAMETERS')
    for key,default in (('strength',.5),('body_min',0)):
        v=form.get(key,default)
        if (isinstance(v,bool) or not isinstance(v,(int,float)) or
                not math.isfinite(v) or not 0<=v<=1):
            raise ValueError('INVALID_ACQUIRED_FORM_PARAMETERS')
    scope=form.get('scope',{})
    if (not isinstance(scope,dict) or
            not isinstance(scope.get('locations',[]),list) or
            any(not isinstance(x,str) for x in scope.get('locations',[])) or
            ('counterpart' in scope and scope['counterpart'] is not None and
             (not isinstance(scope['counterpart'],str) or not scope['counterpart'])) or
            not isinstance(form.get('cues',[]),list) or
            any(not isinstance(x,str) for x in form.get('cues',[]))):
        raise ValueError('INVALID_ACQUIRED_FORM_PARAMETERS')
    ts=form.get('tendencies', [])
    if not isinstance(ts, list) or len(ts)>12:
        raise ValueError('INVALID_ACQUIRED_TENDENCIES')
    for t in ts:
        if (not isinstance(t, dict) or t.get('polarity') not in POLARITIES or
                not isinstance(t.get('action'),str) or t['action'] not in ACTIONS or
                not isinstance(t.get('cue_terms',[]),list) or
                not all(isinstance(x,str) for x in t.get('cue_terms',[]))):
            raise ValueError('INVALID_ACQUIRED_TENDENCIES')


def enact_currents(constitution, access, active_forms, candidates, relational=None, historical=None):
    """Composes differentiated pressures without universal numerical conversion.

    A learned WITHHOLD does not vanish from the iceberg when thwarted by a
    learned APPROACH; it becomes an unresolved antagonism. Without counterforce,
    it suspends an action from the actor-originated candidate set. An externally
    injected action remains disclosed as injection and may transgress the form.
    """
    cues={str(x).lower() for c in access.cues for x in c.get('tags',[])+[c.get('kind','')]}
    forces={};currents=[]
    b=constitution.body
    for metric,flag,threshold in (('nutrition','HUNGER',.42),('rest','EXHAUSTION',.4),('comfort','DISTRESS',.35)):
        if b.get(metric,1.0)<threshold:
            currents.append({'kind':'ORGANISMIC_CONDITION','state':flag,
                'source':'CURRENT_BODY','objective_body_state':metric,
                'not_a_conscious_motive':True})
    for form in active_forms.values():
        validate_tendencies(form)
        for t in form.get('tendencies',[]):
            if t.get('cue_terms') and not (set(v.lower() for v in t['cue_terms']) & cues):
                continue
            a=t['action'];pol=t['polarity'];ident=form['id']
            forces.setdefault(a,{}).setdefault(pol,[]).append(ident)
            currents.append({'kind':'ACQUIRED_ACTION_CURRENT','action':a,'polarity':pol,
                'form_ref':ident,'grade':GRADE,'no_universal_motive_strength':True})
    # An acquired relation-of-relations may produce an action current without
    # restoring an inhibited source form to direct ability. No universal
    # psychological force coefficient is inferred from the motif.
    for mediated in (relational or {}).get('action_currents', []):
        action=mediated['action']; polarity=mediated['polarity']
        ref='motif:'+mediated['motif_ref']
        forces.setdefault(action,{}).setdefault(polarity,[]).append(ref)
        current={'kind':'RELATIONALLY_MEDIATED_ACTION_CURRENT',
            'action':action,'polarity':polarity,'motif_ref':mediated['motif_ref'],
            'source_form_refs':copy(mediated['source_form_refs']),
            'has_inhibited_source':mediated['has_inhibited_source'],
            'grade':GRADE,'not_actor_self_knowledge':True}
        # Exact historical compatibility: the earlier explicit ACTION_CURRENT
        # still has its old record shape. Only the newly operative relational
        # transduction carries extra source-causal metadata.
        if mediated.get('mode') is not None:
            current.update({
                'mediation_mode':mediated['mode'],
                'relation_transduced':mediated['mediation_relation'],
                'relation_source_ref':mediated['mediation_source_ref'],
                'relation_target_ref':mediated['mediation_target_ref'],
                'not_objective_justification_of_conduct':True})
        currents.append(current)
    for h in (historical or {}).get('currents', []):
        action=h['action'];polarity=h['polarity'];ref='history:'+h['ref']
        forces.setdefault(action,{}).setdefault(polarity,[]).append(ref)
    updated=[];antagonisms=[];suspended=[]
    for option in candidates:
        o=copy(option);action=o['action'];polarities=forces.get(action,{})
        approach=sorted(set(polarities.get('APPROACH',[])))
        withhold=sorted(set(polarities.get('WITHHOLD',[])))
        if approach and withhold:
            o['psychodynamic_status']='UNRESOLVED_CONTRADICTION'
            o['opposed_currents']={'approach':approach,'withhold':withhold}
            antagonisms.append({'action':action,'approach':approach,'withhold':withhold,
               'resolution':'UNDETERMINED; NO FORCED HARMONY', 'actor':constitution.actor})
            updated.append(o)
        elif withhold:
            suspended.append({'action':action,'by_form_refs':withhold,
              'status':'SITUATED_ACQUIRED_INHIBITION','still_bodily_possible':True})
        else:
            if approach:
                o['psychodynamic_status']='ACQUIRED_APPROACH_WITHOUT_RECORDED_COUNTERCURRENT'
                o['support_currents']=approach
                if any(ref.startswith('history:') for ref in approach):
                    o['score'] += .16
                    o['historical_pre_cue_rank_effect']='BOUNDED_SOURCEFREE_POLICY'
            updated.append(o)
    return {'candidate_actions':updated,'currents':currents,'antagonisms':antagonisms,
            'suspended':suspended,'grade':GRADE}
