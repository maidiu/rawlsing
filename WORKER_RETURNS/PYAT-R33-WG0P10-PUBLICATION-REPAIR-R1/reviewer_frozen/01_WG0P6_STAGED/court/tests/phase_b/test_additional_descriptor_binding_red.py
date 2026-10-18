"""Post-precommit counterexamples. No original or Phase A expectation is edited.
These are additional adversarial tests discovered by independent full-source execution.
"""
from dataclasses import replace
import pytest
from phase_b_support_v1 import *

@pytest.mark.parametrize('field,forged',[('source_edition','FORGED_CALLER_EDITION'),('native_item_ids',('FOREIGN_NATIVE_ITEM',))])
def test_bound_descriptor_cannot_change_served_provenance(field,forged):
 p=plan();specs=dict(p.op_specs);specs[OP]=replace(specs[OP],**{field:forged});altered=replace(p,op_specs=specs)
 assert altered.contract==p.contract
 runner,receipts,effects=execute(altered)
 entry=effects[OP][0];expected=getattr(p.op_specs[OP],field)
 actual=entry[field];expected=list(expected) if isinstance(expected,tuple) else expected
 dump(R/('observations/phase_b/descriptor_'+field+'_counterexample.json'),{'mutated_field':field,'forged_value':forged,'expected':expected,'served':actual,'native_release_edition':p.releases['REL-A-W1'].source_edition,'contract_unchanged':p.contract==altered.contract,'summary':str(runner.summary()),'consumer':effects,'receipts':[w.receipt_to_json(r) for r in receipts]})
 assert actual==expected, 'Caller copied a plan with unbound descriptor metadata; native issued result carries forged provenance'

def test_copied_release_descriptor_refused_before_native_query():
 p=plan();specs=dict(p.op_specs);specs[OP]=replace(specs[OP],release_tag='REL-A-W2');altered=replace(p,op_specs=specs)
 calls=[];error=None
 import sys
 sys.setprofile(profile_calls(calls))
 try:w.make_executor(altered)(p.units_by_op[OP])
 except (KeyError,w.IdentityError) as e:error=e
 finally:sys.setprofile(None)
 dump(R/'observations/phase_b/descriptor_release_tag_counterexample.json',{'exception':type(error).__name__ if error else None,'reason':str(error),'calls':calls,'contract_unchanged':p.contract==altered.contract})
 assert isinstance(error,w.IdentityError) and not any(c['name']=='execute_empirical_query' for c in calls), 'Unbound release tag reaches native query and fails later with a topology KeyError'
