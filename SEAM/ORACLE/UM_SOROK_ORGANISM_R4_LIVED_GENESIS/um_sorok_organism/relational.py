"""TCO R4 context-qualified psychic relations: operative and non-omnipotent.

PRE-A0's historically differentiated relational field is not a single
magnetism score. A form can function THROUGH another without being replaced;
inhibition can preserve an indirect causal possibility without claiming an
unseen conscious motive. The world never adopts an actor's moral re-description.
"""
from .types import copy,stable_id,GRADE

RELATIONAL_VERSION='TCO_R4_RELATIONAL_REFUNCTIONING@1'
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


class RelationalKernel:
    """Exchangeable functional read policy, separate from owner/world ledger."""
    version=RELATIONAL_VERSION
    def transduce(self,constitution,access,active_forms,inhibited_form_ids,candidates):
        return transduce(constitution,access,active_forms,inhibited_form_ids,candidates)
