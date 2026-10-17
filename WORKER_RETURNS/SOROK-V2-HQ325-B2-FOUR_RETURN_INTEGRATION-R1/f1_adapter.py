"""Honest optional adapter for the unmodified F1 run_native_b1.py contract.

Compatible *negative/deferral envelope* cases execute B2+P1 with zero B1 response.
Unimplemented native positive meanings return NOT_APPLICABLE, not PASS.
"""
from pathlib import Path
import json,tempfile
from bridge import Bridge,b1,input_pair,ROOT,verify_import
from f1_boundary import unsupported_reason,digest


def run_case(case):
    with tempfile.TemporaryDirectory() as directory:
        bridge=Bridge(Path(directory)/'state.sqlite',b1.initialize(b1.prehistory()))
        packet,context,policy=input_pair(bridge.store.state())
        before=b1.digest(bridge.store.state());world=digest(case['world'])
        # F1 envelope is quarantined at ingress, not cast to an occurred B1 event.
        result=bridge.advance(packet,context,policy,None,None,frozen_envelope=case)
        after=b1.digest(bridge.store.state())
        proposal=case['proposal'];gate=result.get('frozen_boundary_gate')
        receipt=dict(status=gate['status'] if gate else 'NOT_APPLICABLE_TO_THIS_LAB',
            reasons=gate['reasons'] if gate else [unsupported_reason(case)],
            actor_id=proposal['actor_id'],event_ref=case['world']['event']['id'],
            recruited_source_refs=proposal['recruited_refs'],observed_source_refs=proposal['observed_refs'],
            rule_ref=proposal['rule_ref'],rng_stream=proposal['rng_stream'],calibration=proposal['probability_grade'],
            world_before=world,world_after=digest(case['world']),actor_state_before=before,actor_state_after=after,
            committed_effect_count=0,selected_action=None,b2_receipt=result,
            applicability='B2_BOUNDARY_NEGATIVE_OR_DEFERRAL' if gate else 'NOT_APPLICABLE_TO_THIS_LAB',
            p1_invoked=True,b1_response_invoked=False,
            provenance_scope='F1_ENVELOPE_AUDIT_REFS__NOT_B1_RECRUITED_FACTS')
        bridge.close();return receipt


def court():
    cases=json.loads((ROOT/'imports/F1/court/f1_frozen_court/frozen_cases.json').read_text())['cases']
    # Only the independent frozen *validator* checks outputs; its response simulator is unused.
    import importlib.util
    verify_import(ROOT/'imports/F1/court/f1_frozen_court/reference_oracle.py')
    spec=importlib.util.spec_from_file_location('f1_frozen_validator',ROOT/'imports/F1/court/f1_frozen_court/reference_oracle.py')
    oracle=importlib.util.module_from_spec(spec);spec.loader.exec_module(oracle)
    rows=[]
    for case in cases:
        result=run_case(case);errors=oracle.validate_native_receipt(case,result)
        na=result['applicability']=='NOT_APPLICABLE_TO_THIS_LAB'
        rows.append(dict(case_id=case['case_id'],family=case['family'],expected_gate=case['expected_gate'],
            applicability=result['applicability'],result='NOT_APPLICABLE_TO_THIS_LAB' if na else 'RED' if errors else 'PASS_BOUNDARY_ONLY',
            reason=result['reasons'],frozen_validator_errors=errors,receipt=result))
    return rows


if __name__=='__main__':
    rows=court();(ROOT/'evidence/f1_applicability.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps({label:sum(r['result']==label for r in rows) for label in ['PASS_BOUNDARY_ONLY','RED','NOT_APPLICABLE_TO_THIS_LAB']},sort_keys=True))
