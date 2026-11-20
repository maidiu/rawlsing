"""TCO R4 context-qualified psychic relations: operative and non-omnipotent.

PRE-A0's historically differentiated relational field is not a single
magnetism score. A form can function THROUGH another without being replaced;
inhibition can preserve an indirect causal possibility without claiming an
unseen conscious motive. The world never adopts an actor's moral re-description.
"""
from .types import copy,stable_id,GRADE

RELATIONAL_VERSION='TCO_R5_RELATIONAL_REFUNCTIONING@2'
REFUNCTION={'SUBORDINATES','INSTRUMENTALIZES','JUSTIFIES','LICENSES',
            'RATIONALIZES','INTERPRETS_THROUGH','REVALUES','COMPENSATES_FOR'}
LATENT={'INHIBITS','SUPPRESSES','QUARANTINES_FROM'}


def transduce(constitution,access,active_forms,inhibited_form_ids,candidates):
    """Return private actor-conditional interpretation and cause provenance.

    No new action is minted; each implicated action must already be eligible.
    Neither coercive practice nor objective injury is excused by a frame.
    A suppressed form remains available as *historical indirect lineage*, not
    as a public action, self-report, or forced affect discharge.
    """
    currents=[];qualified=copy(candidates)
    suppressed=set(inhibited_form_ids);observed=set()
    for link in constitution.links:
        src,dst=link.get('source'),link.get('target')
        relation=link.get('relation')
        if src not in constitution.forms or dst not in constitution.forms:continue
        if link.get('contexts') and access.location not in link['contexts']:continue
        if src not in active_forms and src not in suppressed:continue
        if relation not in REFUNCTION|LATENT:continue
        key=stable_id('relation',{'actor':constitution.actor,'source':src,
                 'target':dst,'relation':relation,'origin':link.get('origin',[])})
        src_in_current=src in active_forms;dst_in_current=dst in active_forms
        latent=not src_in_current or (dst in suppressed and not dst_in_current)
        # Existing historical relation can condition the psychological meaning
        # of something without being directly expressed in this scene.
        current={'kind':'LATENT_RELATIONAL_CONDITION' if latent else
                 'HISTORICALLY_REFUNCTIONED_MEANING',
                 'ref':key,'relation':relation,'source':src,'target':dst,
                 'origin':copy(link.get('origin',[])),
                 'source_currently_recruited':src_in_current,
                 'target_currently_recruited':dst_in_current,
                 'not_world_moral_verdict':True,
                 'not_actor_conscious_self_account':True,
                 'version':RELATIONAL_VERSION,'grade':GRADE}
        currents.append(current)
        # Only a currently available target's OWN existing means can receive
        # interpretive provenance; dormant/inhibited targets mint no action.
        if relation in REFUNCTION and src_in_current and dst_in_current:
            for option in qualified:
                if option['action'] in constitution.forms[dst].get('enables',[]) and (
                        src in option.get('basis',[]) or dst in option.get('basis',[])):
                    option.setdefault('relational_frames',[]).append({'ref':key,
                        'relation':relation,'source':src,'target':dst,
                        'meaning':'ACTOR_SITUATED_HYPOTHESIS_NOT_OBJECTIVE_JUSTIFICATION'})
                    if 'relation:'+key not in option['basis']:
                        option['basis'].append('relation:'+key)
                    observed.add(key)
    return {'currents':currents,'candidate_actions':qualified,
            'operative_relations':sorted(observed),'version':RELATIONAL_VERSION}


def recruit_functional_possibility(constitution,access,active_forms,inhibited_form_ids):
    """TCO: an already active organization can give another an operative function.

    An actor-*acquired* directed relation can make a previously irrelevant
    practice prospectively available. This is not a new ability, action opcode,
    motive, or moral license: the target must already be acquired, embodied,
    currently scoped, and not inhibited. Neither speaker ideology nor a pretty
    social account can create a new world permission or coactor agreement.

    Deliberately one-hop: no recursive contagion or global taxonomy. Theory
    revisions can replace this function via RelationalKernel without rewriting
    historic events or retroactively manufacturing acquired practices.
    """
    from .organism import eligible
    from .constitution import _form_in_scope
    allowed={'SUBORDINATES','INSTRUMENTALIZES','INTERPRETS_THROUGH',
             'REVALUES','JUSTIFIES','LICENSES'}
    active=copy(active_forms);blocked=set(inhibited_form_ids)
    currents=[]
    for link in constitution.links:
        source,target=link.get('source'),link.get('target')
        if source not in active_forms or target not in constitution.forms:
            continue
        if target in blocked or target in active:
            continue
        relation=link.get('relation')
        if relation not in allowed:
            continue
        # Do not reintroduce REMONT R7's string-membership permission bug through
        # a new relation operator. This bounds R5 only; it does NOT receive or
        # replace the wider independent REMONT R7 source-owner repair.
        contexts=link.get('contexts',[])
        if (not isinstance(contexts,list) or
              any(not isinstance(x,str) for x in contexts)):
            continue
        if contexts and access.location not in contexts:
            continue
        form=constitution.forms[target]
        scope=form.get('scope',{})
        if not isinstance(scope,dict):continue
        locs=scope.get('locations',[])
        if (not isinstance(locs,list) or any(not isinstance(x,str) for x in locs)):
            continue
        counterpart=scope.get('counterpart')
        if counterpart is not None and not isinstance(counterpart,str):continue
        if form.get('lifecycle') in ('ENDED','DORMANT'):
            continue
        if form.get('body_min',0)>constitution.body['motor']:
            continue
        if not _form_in_scope(form,access):
            continue
        # Historical linkage never creates a bodily-unavailable action. The
        # form can still operate noninstrumentally when it enables no action.
        active[target]=copy(form)
        ref=stable_id('relation',{'actor':constitution.actor,
             'source':source,'target':target,'relation':relation,
             'origin':link.get('origin',[])})
        currents.append({'kind':'ACQUIRED_RELATION_ENABLED_PRACTICE',
              'ref':ref,'source':source,'target':target,'relation':relation,
              'origin':copy(link.get('origin',[])),
              'no_new_ability_minted':True,'not_world_moral_verdict':True,
              'not_actor_self_explanation':True,'version':RELATIONAL_VERSION})
    return {'active':active,'currents':currents,'version':RELATIONAL_VERSION}


class RelationalKernel:
    """Exchangeable functional read policy, separate from owner/world ledger."""
    version=RELATIONAL_VERSION
    def recruit(self,constitution,access,active_forms,inhibited_form_ids):
        return recruit_functional_possibility(constitution,access,active_forms,inhibited_form_ids)
    def transduce(self,constitution,access,active_forms,inhibited_form_ids,candidates):
        return transduce(constitution,access,active_forms,inhibited_form_ids,candidates)
