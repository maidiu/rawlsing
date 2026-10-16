"""Literal original frozen prediction; expected to FAIL, never xfailed or repaired."""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'staging/ms1/runtime'))
import ms1_serial as M
def test_original_P3b_C2_must_differ_from_C4():
    c2=M.run_cell('C2',M.MEMORY_CONTENT_UNCERTAIN,mediator='ACTIVE')
    c4=M.run_cell('C4',M.MEMORY_CONTENT_UNCERTAIN,mediator='WITHDRAWN')
    a=(c2['response_decision_state'],c2['response_effect_kind']);b=(c4['response_decision_state'],c4['response_effect_kind'])
    p=R/'evidence/literal_p3b/counterfactual.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(dict(C2=c2,C4=c4,original_prediction='C2 != C4',original_prediction_holds=a!=b,F_B_fired=a==b),indent=2)+'\n')
    assert a!=b,'Original prospective P3b is FALSIFIED: native UNKNOWN masks stance withdrawal'
