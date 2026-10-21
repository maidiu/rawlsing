"""One joined source-free run. No person, child, biological or native event issued."""
from copy import deepcopy
from .proposal import frozen_fallback_record,freeze_proposal_record,PROPOSAL_SYSTEM_PROMPT
from .joint import material_joint_opportunity
from .pipeline import run_pipeline
import json


def inputs():
 c=deepcopy(frozen_fallback_record('M0','ROUTE_LOCAL_CLOSED').parsed_candidates[0])
 c['endpoint_constraints']['required_state_predicates']=[dict(field='place',equals='INST_WORKSHOP_A'),dict(field='availability_status',equals='available_for_encounter')]
 b=deepcopy(c);b['candidate_local_id']='G15_SECOND_ENDPOINT_CLASS'
 b['endpoint_constraints']['required_state_predicates'].append(dict(field='material_position',equals='waged_repair'))
 rec=freeze_proposal_record('M0','ROUTE_LOCAL_CLOSED','{}',PROPOSAL_SYSTEM_PROMPT,dict(raw_output=json.dumps([c,b])),4)
 return dict(fixture_variant='M0',causal_run_id='G15_JOINED_RESEARCH_RUN',root_seed='13'*32,
    policy_name='SIM_UNIFORM_CLASSES',proposal_record=rec,model_enabled=False,
    joint_material_opportunity=material_joint_opportunity(),continued_joint_material=material_joint_opportunity(effective_index=1100))


def run(inputs_override=None):
 return run_pipeline(**(inputs() if inputs_override is None else inputs_override))
