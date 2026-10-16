from bootstrap import ROOT,RT
from observe import Observer
from handoff import fixture_handoff,render_markdown,PROPOSALS
import e05_n9_selected_world_adapter as E
from rawlsing_next.pre553_hq297_n9c_two_field_reader import TestOnlyRegistry,GSS,NCA
from rawlsing_next.objective_consumer_bounded_evidence import installation_manifest,OC05,evaluate_current_consumer,NotYetApplicableConsumer
from copy import deepcopy
import json,datetime,platform,sys,hashlib
OBS=ROOT/'observations';OBS.mkdir(exist_ok=True);EX=ROOT/'examples';EX.mkdir(exist_ok=True)
FIX=RT/'WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json'
rows=json.loads(FIX.read_text())['fields'];obs=Observer();obs.start();packets={}
def request(label):return E.standard_request(label=label).binding()
for label in ['CURRENT_TEST_CLOCK','HISTORICAL_AS_OF','TYPED_PARTIAL_PRE_NCA_PUBLICATION']:
 binding=request(label);(EX/('request_'+label.lower()+'.json')).write_text(json.dumps(binding,indent=2)+'\n')
 packets[label]=fixture_handoff(rows).execute(binding)
packets['EMPIRICAL_Y_CHANGED']=fixture_handoff(rows,empirical_changed=True).execute(request('CURRENT_TEST_CLOCK'))
packets['ZERO_SUPPORT']=fixture_handoff(rows,support_loss=True).execute(request('CURRENT_TEST_CLOCK'))
reverse=E.standard_request(label='CURRENT_TEST_CLOCK',target='A',conditions=(('Y',1),)).binding()
(EX/'request_reverse.json').write_text(json.dumps(reverse,indent=2)+'\n')
packets['AUTHORIZED_REVERSE']=fixture_handoff(rows).execute(reverse,consumer_mode='SCALAR_ONLY')
# Retain the old complete result, then fresh-serve the SAME accepted world
# against the CURRENT attached registry whose NCA arm was withdrawn.
h=fixture_handoff(rows);prepared=h.prepare(request('CURRENT_TEST_CLOCK'));before=h.serve(prepared)
withdrawn=deepcopy(rows);next(x for x in withdrawn if x['role']==NCA)['status']='REVOKED_TEST_ONLY';h.adapter.registry=TestOnlyRegistry(withdrawn)
packets['LATE_NCA_WITHDRAWAL']=h.serve(prepared);archive=h.archive(before)
assert before['selected_world_receipt']['receipt_hash'] in h.adapter.receipts
assert archive['retained']['fresh_use_authorized'] is False
# Explicit new separately accepted fixture after a late publication/grant cut.
late=fixture_handoff(rows);pre=late.execute(request('TYPED_PARTIAL_PRE_NCA_PUBLICATION'))
after=late.execute(request('CURRENT_TEST_CLOCK'));late_grant=dict(before=pre,after=after,new_acceptance=pre['acceptance']!=after['acceptance'],interpretation='Separately accepted fixture request/publication cut; not an issued real publisher grant')
manifest={x['policy_id']:x for x in installation_manifest()}
try:evaluate_current_consumer(policy_id=OC05,operation_id='E05A_METHOD_HANDOFF',inputs=(),requested_claim_ceiling='OBJECTIVE_FACT',partial_allowed=False)
except NotYetApplicableConsumer as exc:refusal=dict(type=type(exc).__name__,message=str(exc))
else:raise AssertionError('OC05 unexpectedly installed')
obs.stop();trace=obs.result()
for name,packet in packets.items():
 (EX/(name.lower()+'.json')).write_text(json.dumps(packet,indent=2)+'\n')
 (EX/(name.lower()+'.md')).write_text(render_markdown(packet))
result=dict(schema='E05A_TWO_CONSUMER_EXECUTED_HANDOFF@1',packets=packets,native_withdrawal_before=before,archival_receipt=archive,late_publication_and_separate_acceptance=late_grant,actual_OC05=dict(manifest=manifest,direct_refusal=refusal),native_trace=trace,rights='TEST_ONLY_NO_EXTERNAL_USE_GRANT',independent_acceptance_reused='f524f60781e2e7e72278d04d6377fb1da877698a',completed_court_rerun=False)
(ROOT/'02_EXECUTED_TWO_CONSUMER_SERVICE_HANDOFF.json').write_text(json.dumps(result,indent=2)+'\n')
marker=json.loads((RT/'live_epoch.json').read_text());marker.update(status='LIVE_VERIFIED_IN_THIS_PYTHON_PROCESS',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat());(RT/'live_epoch.json').write_text(json.dumps(marker,indent=2)+'\n')
(OBS/'native_imports_and_calls.json').write_text(json.dumps(trace,indent=2)+'\n')
print('E05A real request -> acceptance -> receipt -> BOTH original consumers executed')
print('Examples',len(packets),'native imports',len(trace['imports']),'actual owner entries',sum(x['count'] for x in trace['actual_entries']))
