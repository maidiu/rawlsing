"""Supplement to V1 candidate extra-field probe: mutate an actual endpoint."""
from copy import deepcopy
import json
from g12_assays import ROOT,adp020_select,h_obj

def test_changed_actual_endpoint_payload_invalidates_selection_identity():
    record=json.loads((ROOT/'sources/sgi1/08_LLM_PROPOSAL_RECORDS/proposal_M0_GENERAL.json').read_text())['record']
    classes=record['dedup']['classes'];changed=deepcopy(classes)
    changed[0]['candidate']['endpoint_constraints']['required_state_predicates']=[{'field':'place','equals':'G12_FORGED_UNREACHABLE_PLACE'}]
    a=adp020_select('SIM_UNIFORM_CLASSES',classes,'G12_SEED','G12_SCOPE')
    b=adp020_select('SIM_UNIFORM_CLASSES',changed,'G12_SEED','G12_SCOPE')
    evidence=dict(original_candidate_payload_hash=h_obj(classes[0]['candidate']),mutated_candidate_payload_hash=h_obj(changed[0]['candidate']),before=a,after=b,
                  scope='Direct selector trust boundary with stale canonical class identity; not a claim that a fresh dedup preserves the key')
    (ROOT/'evidence/actual_endpoint_payload_mutation.json').write_text(json.dumps(evidence,indent=2)+'\n')
    assert a['candidate_set_hash']!=b['candidate_set_hash']
