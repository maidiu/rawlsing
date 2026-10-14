import json,os,pathlib,sys
from pv_import_audit import Audit
audit=Audit()
audit.pytest_sessionstart(None)
from rawlsing_next.tests import test_postastra_pv_v2k_independent as court
root=pathlib.Path(sys.argv[1]);root.mkdir(exist_ok=True)
phase=sys.argv[2]
if phase=='replay':before=(root/'frozen_before_production.json').read_bytes()
records,expected,plans,calls=court.court(root)
if phase=='replay':assert before==(root/'frozen_before_production.json').read_bytes()
prior=None
if phase=='replay':
 first=json.loads((court.RETURN/'repro/cold_first.json').read_text())
 prior={l['original_expected_work_key']:court.ExactRef(**l['consumer_ref']) for l in first['report']['links']}
report=court.K.run_sourcefree(expected=expected,selected_scopes=plans,prior_consumer_refs=prior)
assert report['ok'] and len(report['links'])==6 and len(report['nonrunnable'])==2
assert [len(c) for c in calls]==([3,3] if phase=='first' else [0,0])
if phase=='replay':assert report['links']==first['report']['links']
result=dict(phase=phase,report=report,durable_calls=[len(c) for c in calls],setup_producer_reconstruction=True)
(court.RETURN/'repro'/('cold_'+phase+'.json')).write_text(json.dumps(result,indent=2))
audit.pytest_sessionfinish(None,0)
print(phase,'ok',report['ok'],'durable calls',result['durable_calls'])
