"""Exact original3 negative sources; explicit early typed-refusal transport.
No KeyError is accepted as refusal. Third original test body runs unchanged.
"""
import importlib.util,sys,pytest
from phase_b_support_v1 import R,w,dump,profile_calls
sp=importlib.util.spec_from_file_location('_unchanged_original_three',R/'tests/phase_b/test_additional_descriptor_binding_red.py')
original=importlib.util.module_from_spec(sp);sp.loader.exec_module(original)
@pytest.mark.parametrize('field,value',[('source_edition','FORGED_CALLER_EDITION'),('native_item_ids',('FOREIGN_NATIVE_ITEM',))])
def test_original_counterexample_no_supported_forged_provenance(field,value):
 calls=[];exception=None
 sys.setprofile(profile_calls(calls))
 try:original.test_bound_descriptor_cannot_change_served_provenance(field,value)
 except w.IdentityError as e:
  exception=type(e).__name__
  assert str(e)=='COMPLETE_BOUND_SOURCE_DESCRIPTOR_CHANGED'
 finally:sys.setprofile(None)
 dump(R/('observations/p5_original_three_'+field+'.json'),{'field':field,'exception_type':exception,'calls':calls,'transport':'Original body unchanged; early typed IdentityError before native query satisfies no forged publication. Untyped escapes still fail.'})
 assert not any(c['name']=='execute_empirical_query' for c in calls)
 assert exception=='IdentityError'

def test_original_release_tag_counterexample_body_unchanged():
 original.test_copied_release_descriptor_refused_before_native_query()
