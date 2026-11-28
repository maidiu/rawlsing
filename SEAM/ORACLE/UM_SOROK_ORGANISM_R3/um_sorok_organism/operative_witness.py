"""R9 third MULCH: freeze situated policy grounds BEFORE world settlement.

A person can really act without being able to explain why. This records only
which historically acquired pressures were causally IN THE SOURCEFREE POLICY
path, not an ontological truth about drive, consent, reflective intention, or
unconscious motive. The world/Other/experience remain distinct owners.
"""

GRADE='SOURCEFREE_RESEARCH_OPERATIVE_SELECTION_WITNESS'
NONPROJECT_APPROACH='FICTIONAL_PREPROJECT_ORIENTATION_NOT_CONSCIOUS_INTENTION'
NONPROJECT_DEFERRAL='HEURISTIC_DEFERRAL_UNDER_NONPROJECT_WITHHOLD_OR_CONTRADICTION'


def _preproject(option):
    p=option.get('preproject_recruitment')
    if p is None:
        return None
    if not isinstance(p,dict) or not isinstance(p.get('ground_refs'),list):
        raise ValueError('OPERATIVE_MALFORMED_CURRENT')
    if any(not isinstance(s,str) or not s for s in p['ground_refs']):
        raise ValueError('OPERATIVE_MALFORMED_GROUND')
    if len(set(p['ground_refs']))!=len(p['ground_refs']):
        raise ValueError('OPERATIVE_DUPLICATED_GROUND')
    return p


def freeze_operative_witness(actor_id,clock,options,chosen_action,proposal,provider_grade,
                             selected_projects=None):
    """State which SOURCEFREE policy rule used which currently recruited grounds.

    Do not infer that all eligible currents were effective motives. A semantic
    provider's authored action is an attribution to an operation, not proof of
    conscious initiation. Offline heuristic paths get stronger but still
    purely computational policy-identity receipts.
    """
    if not isinstance(actor_id,str) or not actor_id or type(clock) is not int or clock<0:
        raise ValueError('OPERATIVE_INVALID_ACTOR_CLOCK')
    if not isinstance(options,list) or not isinstance(proposal,dict):
        raise ValueError('OPERATIVE_INVALID_INPUT')
    if not isinstance(chosen_action,str):
        raise ValueError('OPERATIVE_INVALID_ACTION')
    if not isinstance(selected_projects,list) or any(type(v) is not str for v in selected_projects):
        raise ValueError('OPERATIVE_INVALID_PROJECTS')
    chosen=[o for o in options if o.get('action')==chosen_action]
    if len(chosen)!=1:
        raise ValueError('OPERATIVE_ACTION_NOT_SINGULARLY_ISSUED')
    for opt in options:_preproject(opt)
    recorded={
        'actor':actor_id,'as_of_clock':clock,'chosen_operation':chosen_action,
        'selected_project_refs':list(selected_projects),
        'policy_path':'INDETERMINATE_SEMANTIC_CHOICE',
        'recruited_ground_refs_at_choice':[],
        'affected_option_refs':[],
        'other_coexisting_currents_not_overwritten':True,
        'not_actor_self_knowledge':True,
        'not_objective_world_cause':True,
        'not_a_clinical_claim_about_motive':True,
        'grade':GRADE,
    }
    # The exact issued destination is part of the computational choice,
    # not an explanation of why the actor wished to go there.
    if chosen_action=='MOVE' and proposal.get('practical_option_id') is not None:
        matches=[p for p in chosen[0].get('practical_alternatives',[])
                 if p['option_id']==proposal['practical_option_id']
                 and p.get('grounds_status')=='HISTORICALLY_FAMILIAR_DESTINATION']
        if matches:
            if len(matches)!=1:
                raise ValueError('OPERATIVE_AMBIGUOUS_FAMILIAR_DESTINATION')
            from .types import copy
            m=matches[0];source=m['familiar_destination_basis']
            if (m['actor']!=actor_id or m['as_of_clock']!=clock
                    or m['world_request']['material_object_ref']!=source['site']
                    or source['experienced_clock']>=clock or selected_projects):
                raise ValueError('OPERATIVE_UNQUALIFIED_FAMILIAR_DESTINATION')
            recorded['familiar_destination_choice']={
                'option_ref':m['option_id'],'source':copy(source),
                'not_current_permission_or_conscious_reason':True}
    # Never grant an external model the internal offline-policy witness simply
    # because it submitted an identically worded selection_grade string.
    if provider_grade!='SOURCEFREE_RULE_BASED_PLACEHOLDER_NO_LLM':
        return recorded
    marker=proposal.get('purpose_selection_grade')
    if marker==NONPROJECT_APPROACH:
        p=_preproject(chosen[0]);refs=p['ground_refs'] if p else []
        if (not p or p.get('status')!='ACQUIRED_NONPROJECT_APPROACH'
                or chosen_action not in ('ORIENT','SIGNAL') or selected_projects):
            raise ValueError('OPERATIVE_FALSE_PREPROJECT_ATTRIBUTION')
        recorded.update({'policy_path':'OFFLINE_HISTORICALLY_RECRUITED_ORIENTATION',
                         'recruited_ground_refs_at_choice':sorted(refs),
                         'affected_option_refs':[chosen_action],
                         'recruitment_is_not_conscious_reason':True})
    elif marker==NONPROJECT_DEFERRAL:
        if chosen_action!='WAIT' or selected_projects:
            raise ValueError('OPERATIVE_FALSE_DEFERRAL')
        pressing=[o for o in options if (_preproject(o) or {}).get('status') in
                  ('ACQUIRED_NONPROJECT_WITHHOLD','UNRESOLVED_PREPROJECT_CONTRADICTION')]
        approaching=[o for o in options if (_preproject(o) or {}).get('status')==
                     'ACQUIRED_NONPROJECT_APPROACH']
        if not pressing or approaching:
            raise ValueError('OPERATIVE_UNGROUNDED_DEFERRAL')
        refs=sorted({ref for o in pressing for ref in o['preproject_recruitment']['ground_refs']})
        recorded.update({'policy_path':'OFFLINE_DEFERRAL_FROM_RECRUITED_INHIBITION',
                         'recruited_ground_refs_at_choice':refs,
                         'affected_option_refs':sorted(o['action'] for o in pressing),
                         'deferral_is_not_universal_response_to_conflict':True})
    return recorded