"""Versioned early-refusal transport of WG0L's three exact hostile stimuli.

The two old tests assumed a returned fact. The intended fixed edge refuses
before computation, so these assertions explicitly test the stronger behavior.
"""
from dataclasses import replace
import sys
import pytest


@pytest.mark.parametrize("field,forged",[("source_edition","FORGED_CALLER_EDITION"),
    ("native_item_ids",("FOREIGN_NATIVE_ITEM",)),("release_tag","REL-A-W2"),
    ("risk_name","R_ORD2"),("member_ids",("FOREIGN",)),("grant","CALLER_GRANT"),
    ("targets",(("FOREIGN",("yes","no")),)),("full_identity_hash","0"*64)])
def test_copied_descriptor_refused_before_native_execution(field,forged):
    from phase_b_support_v1 import w,plan,OP
    p=plan();specs=dict(p.op_specs);specs[OP]=replace(specs[OP],**{field:forged})
    altered=replace(p,op_specs=specs);calls=[];error=None
    assert altered.contract==p.contract
    def trace(frame,event,arg):
        if event=="call" and frame.f_code.co_name=="execute_empirical_query":
            calls.append(frame.f_code.co_filename)
    sys.setprofile(trace)
    try:w.make_executor(altered)(p.units_by_op[OP])
    except w.IdentityError as exc:error=exc
    finally:sys.setprofile(None)
    assert isinstance(error,w.IdentityError), "Issuer descriptor envelope was bypassed"
    assert not calls, "Forged descriptor reached native I03"


def test_caller_rehash_of_full_descriptor_is_not_new_issuance():
    from phase_b_support_v1 import w,plan,OP
    p=plan();contract=__import__("json").loads(p.contract)
    specs=dict(p.op_specs);specs[OP]=replace(specs[OP],source_edition="FORGED_CALLER_EDITION")
    contract["bindings"][OP]["descriptor"]=w._plain(vars(specs[OP]))
    altered=replace(p,op_specs=specs,contract=w.canonical(contract))
    with pytest.raises(w.IdentityError,match="NOT_REGISTERED"):
        w.make_executor(altered)(p.units_by_op[OP])
