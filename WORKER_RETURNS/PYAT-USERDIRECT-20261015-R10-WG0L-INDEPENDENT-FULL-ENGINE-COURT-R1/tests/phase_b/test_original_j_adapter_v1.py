"""WG0L mapping for all44 original WG0J tests, never editing original source.
Admission may refuse earlier; detached immutable exports preserve the same science.
All original baseline, actual-owner numerics and cold/shard assertions remain.
"""
import copy,functools,importlib.util,sys
from dataclasses import FrozenInstanceError,replace
import pytest
import reviewer_common_v1 as common
from phase_b_support_v1 import C,AdmissionRefused
from reviewer_common_v1 import w,plan,execute
sys.modules['common']=common
sp=importlib.util.spec_from_file_location('_wg0l_original_j_tests',C/'pinned/predecessors/j/tests/test_independent.py')
original=importlib.util.module_from_spec(sp);sp.loader.exec_module(original)
baseline=original.baseline
EARLY={'test_native_options_must_affect_computation_or_hold','test_native_metadata_must_bind_release_or_hold','test_unknown_withdrawn_grants_hold'}
for name,fn in vars(original).copy().items():
 if not name.startswith('test_'):continue
 if name in EARLY:
  def mapped(fn):
   @functools.wraps(fn)
   def call(*args,**kwargs):
    try:return fn(*args,**kwargs)
    except (w.IdentityError,w.FrontierError) as e:
     assert str(e).startswith(('NATIVE_ITEM_METADATA_NOT_QUALIFIED','EXACT_EXTERNAL_FRONTIER_MISMATCH'))
    except AdmissionRefused as e:assert e.value=='CONFLICTING_NATIVE_ITEM_IDENTITY'
   return call
  globals()[name]=mapped(fn)
 else:globals()[name]=fn

def test_fact_payload_is_bound_at_read():
 p=plan();_,rs,e=execute(p);op='OP-WG0P-ORD-01-MARGINAL';before=copy.deepcopy(common.values(e))
 e[op][0]['denominator']=999;e[op][0]['cells'][0]['n']=999
 assert common.values(w.consumer_effects(p,rs))==before

def test_wrong_release_bound_to_unit_is_rejected():
 p=plan();op='OP-WG0P-ORD-01-MARGINAL';spec=p.op_specs[op]
 with pytest.raises(FrozenInstanceError):spec.release_tag='REL-A-W2'
 altered=dict(p.op_specs);altered[op]=replace(spec,release_tag='REL-A-W2')
 with pytest.raises(TypeError):p.op_specs[op]=altered[op]
 with pytest.raises(w.IdentityError):w.make_executor(p)(replace(p.units_by_op[op],release_refs=(p.releases['REL-A-W2'].release_ref,)))
