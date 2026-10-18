"""Version1 port of all44 frozen WG0J cases. Original source is never edited.

Changed interface cases are explicit: unqualified metadata/grants now refuse at
plan admission; bound specs are immutable; fact reads are detached rather than
corrupting an archive then erroring. Baseline/cold evidence comes from fresh
native WG0P4 execution. No historical RED is erased by these adapter passes.
"""
import functools,importlib.util,sys
from dataclasses import FrozenInstanceError,replace
import pytest
import common_v1 as common
from common_v1 import w,R,plan,execute
sys.modules['common']=common
sp=importlib.util.spec_from_file_location('_frozen_wg0j',R/'pinned/predecessors/j/tests/test_independent.py')
original=importlib.util.module_from_spec(sp);sp.loader.exec_module(original)
baseline=original.baseline
ADMISSION_REFUSAL={'test_native_options_must_affect_computation_or_hold','test_native_metadata_must_bind_release_or_hold','test_unknown_withdrawn_grants_hold'}
for name,function in vars(original).copy().items():
    if not name.startswith('test_'):continue
    if name in ADMISSION_REFUSAL:
        def adapt(fn):
            @functools.wraps(fn)
            def wrapped(*args,**kwargs):
                try:return fn(*args,**kwargs)
                except (w.IdentityError,w.FrontierError) as e:
                    assert 'NATIVE_ITEM_METADATA_NOT_QUALIFIED' in str(e) or 'EXACT_EXTERNAL_FRONTIER_MISMATCH' in str(e)
            return wrapped
        globals()[name]=adapt(function)
    else:globals()[name]=function

def test_fact_payload_is_bound_at_read():
    p=plan();_,rs,e=execute(p);op='OP-WG0P-ORD-01-MARGINAL'
    e[op][0]['denominator']=999;e[op][0]['cells'][0]['n']=999
    fresh=w.consumer_effects(p,rs)
    assert fresh[op][0]['denominator']==6 and fresh[op][0]['cells'][0]['n']==1

def test_wrong_release_bound_to_unit_is_rejected():
    p=plan();spec=p.op_specs['OP-WG0P-ORD-01-MARGINAL']
    with pytest.raises(FrozenInstanceError):spec.release_tag='REL-A-W2'
    with pytest.raises(TypeError):p.op_specs[spec.op_id]=replace(spec,release_tag='REL-A-W2')
    wrong=replace(p.units_by_op[spec.op_id],release_refs=(p.releases['REL-A-W2'].release_ref,))
    with pytest.raises(w.IdentityError):w.make_executor(p)(wrong)
