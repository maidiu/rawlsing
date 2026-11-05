"""P1R2: poison every exported authority/event/question ref through the actual selector seam."""
from unittest.mock import patch
from rawlsing_next.tests.test_pre553_route_b_production import _fixture, _execute
from rawlsing_next._pre553_query_predicate import _select_respondent_events, _SELECTOR_CONTRACT_VERSION
from rawlsing_next._pre553_c11_execution_view import _EventLane
from rawlsing_next.pre553_empirical_objects import ExactRef
import json,os
os.environ.pop('RAWLSING_C11_ACCELERATOR_DIR',None)
fx=_fixture();route=_execute(fx);executor=route.repository_binding.executor;repo=executor.repository
index=next(iter(repo._i03_release_indices.values()));request=fx['requests'][0]
def facts():
 return [f.as_dict() for f in executor.execute_i03(query_ref=request.query_ref,predicate_ref=request.predicate_ref).facts]
before=facts()
selectors=tuple(e for key in index.respondents for target in fx['qrefs'].values() for e in _select_respondent_events(index,key,target,native_only=True))
assert _SELECTOR_CONTRACT_VERSION==1 and len(index.respondents)>1
assert len(selectors)>len(index.respondents)*len(fx['qrefs'])
sealed={e.ref.key:repo.resolve_object_exact(e.ref).as_dict() for e in selectors}
mutations=0
with patch.object(_EventLane,'materialize',side_effect=AssertionError('native realization on hot mutation court')):
 for event in selectors:
  for field in ('ref','native_question_ref','canonical_question_ref_if_authorized','component_or_subitem_ref','authority_snapshot_refs'):
   exported=getattr(event,field)
   children=exported if isinstance(exported,tuple) else (() if exported is None else (exported,))
   expected=[ref.as_dict() for ref in children]
   for ref in children:
    original=ref.as_dict()
    for key in original:ref.__dict__[key]='f'*64 if 'hash' in key else 'urn:review:forged'
    assert facts()==before
    fresh=getattr(event,field);fresh_children=fresh if isinstance(fresh,tuple) else (fresh,)
    assert [ref.as_dict() for ref in fresh_children]==expected
    ref.__dict__.update(original)
    assert facts()==before
    mutations+=1
for event in selectors:assert repo.resolve_object_exact(event.ref).as_dict()==sealed[event.ref.key]
print(json.dumps({'contract_version':1,'respondents':len(index.respondents),'events_with_occurrences':len(selectors),'poisoned_reference_exports':mutations,'all_facts_exact':True,'sealed_native_lookup_exact':True,'hot_native_realizations':0},sort_keys=True))
