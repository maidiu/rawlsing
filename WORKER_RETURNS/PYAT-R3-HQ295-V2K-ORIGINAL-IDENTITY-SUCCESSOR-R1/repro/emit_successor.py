"""Separate-process exact source-free successor, actual owners, retained ledger."""
import importlib.util, json, sys
from pathlib import Path
from rawlsing_next import pre553_original_identity_v2k_successor_candidate as K
from rawlsing_next.pre553_empirical_objects import ExactRef
repo,ledger,output,mode=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),sys.argv[4]
spec=importlib.util.spec_from_file_location('v2k_fixture',repo/'rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py')
fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)
inputs=[fixture.sourcefree_original_inputs(ns) for ns in ('V2K-NAMESPACE-A','V2K-NAMESPACE-B')]
per_scope=[fixture.freeze_original_before_production(data)[0] for data in inputs]
records=tuple(record for group in per_scope for record in group)
expected=K.FrozenOriginalExpected.from_records(records,input_origin=K.ORIGIN)
# Persist/verify original expected preimages BEFORE any Route B/I03/I05 call.
if mode=='first':
    (output/'expected_before_production.json').write_text(expected.payload_json+'\n')
else:
    assert (output/'expected_before_production.json').read_text()==expected.payload_json+'\n'
prepared=[fixture.prepare_owner_scope(ledger/str(i),data,group)
    for i,(data,group) in enumerate(zip(inputs,per_scope))]
plans=tuple(plan for plan,calls in prepared)
calls=[calls for plan,calls in prepared]
prior=None
if mode=='replay':
    first=json.loads((output/'first.json').read_text())
    assert (output/'expected_before_production.json').read_text()==expected.payload_json+'\n'
    prior={l['original_expected_work_key']:ExactRef(**l['consumer_ref']) for l in first['links']}
report=K.run_sourcefree(expected=expected,selected_scopes=plans,prior_consumer_refs=prior)
assert report['ok'] and len(report['links'])==6 and len(report['nonrunnable'])==2
if mode=='replay':
    assert report['links']==first['links'] and calls==[[],[]]
    assert all(r['run']['executed']==[] for r in report['owner_reports'])
else:
    assert [len(c) for c in calls]==[3,3]
(output/(mode+'.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'mode':mode,'ok':report['ok'],'original_keys':len(report['links']),
    'distinct_legacy_keys':len({l['legacy_expected_work_key'] for l in report['links']}),
    'durable_executor_calls':[len(c) for c in calls],'held_original_records':len(report['nonrunnable']),
    'source_grade':'SOURCEFREE_NOT_ISSUED','schema':K.SCHEMA}))
