from bootstrap import ROOT,A,RT
# E05A observer uses its own ROOT; load that exact bootstrap in an alias-free
# subprocess environment by adapting only observer globals, not owner methods.
import importlib.util,json,sys,hashlib,platform,datetime
from copy import deepcopy
import e05_n9_selected_world_adapter as E
from handoff import fixture_handoff
from preview import read_preview,PreviewDisabled
from rawlsing_next.pre553_hq297_n9c_two_field_reader import TestOnlyRegistry,GSS,NCA
from rawlsing_next.objective_consumer_bounded_evidence import installation_manifest,OC05,evaluate_current_consumer,NotYetApplicableConsumer
spec=importlib.util.spec_from_file_location('exact_e05a_observer',A/'repro/observe.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
mod.ROOT=A;mod.RT=RT
obs=mod.Observer();obs.start()
rows=json.loads((RT/'WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json').read_text())['fields']
def binding(label='CURRENT_TEST_CLOCK',**kw):return E.standard_request(label=label,**kw).binding()
packets={}
for label in ['CURRENT_TEST_CLOCK','HISTORICAL_AS_OF','TYPED_PARTIAL_PRE_NCA_PUBLICATION']:
 packets[label]=read_preview(fixture_handoff(rows),binding(label),enabled=True)
packets['EMPIRICAL_Y_CHANGED']=read_preview(fixture_handoff(rows,empirical_changed=True),binding(),enabled=True)
packets['ZERO_SUPPORT']=read_preview(fixture_handoff(rows,support_loss=True),binding(),enabled=True)
# New actual reads of selective present registry changes, same acceptance.
changes={}
for role in [GSS,NCA]:
 for change in ['revoke','rekey']:
  h=fixture_handoff(rows);q=binding();p=h.prepare(q);before=read_preview(h,q,enabled=True,prepared=p)
  altered=deepcopy(rows);row=next(x for x in altered if x['role']==role)
  if change=='revoke':row['status']='REVOKED_TEST_ONLY'
  else:row['release_nonce']='E05H_FRESH_SEPARATE_GRANT_REQUIRED'
  h.adapter.registry=TestOnlyRegistry(altered)
  after=read_preview(h,q,enabled=True,prepared=p)
  changes[role+'_'+change]=dict(before=before,after=after,archival=h.archive(before['packet']))
reverse_h=fixture_handoff(rows)
reverse=reverse_h.execute(binding(target='A',conditions=(('Y',1),)),consumer_mode='SCALAR_ONLY')
# Null/weak/minority fixture branches remain measured outputs, not refusal.
branches={}
for conditions in [(('A',0),('B',0),('C',0)),(('A',1),('B',0),('C',1))]:
 h=fixture_handoff(rows);q=binding(conditions=conditions);p=h.prepare(q)
 branches[str(conditions)]=h.adapter.serve(p.request,p.acceptance,p.snapshot)
try:read_preview(fixture_handoff(rows),binding())
except PreviewDisabled as exc:off=dict(type=type(exc).__name__,reason=str(exc))
else:raise AssertionError('default on')
try:evaluate_current_consumer(policy_id=OC05,operation_id='E05H_PREVIEW_ONLY',inputs=(),requested_claim_ceiling='OBJECTIVE_FACT',partial_allowed=False)
except NotYetApplicableConsumer as exc:oc05=dict(type=type(exc).__name__,reason=str(exc))
else:raise AssertionError('unexpected installed OC05')
obs.stop();trace=obs.result()
out=dict(schema='E05H_ACTUAL_OPT_IN_SOURCEFREE_CONSUMER_PREVIEW@1',observed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),packets=packets,selective_current_grant_changes=changes,reverse_separate_grant=reverse,weak_null_branches=branches,off_default=off,actual_oc05=dict(manifest=installation_manifest(),direct_refusal=oc05),native_trace=trace,court403_rerun=False,source_rights='TEST_ONLY_NO_EXTERNAL_USE_GRANT',installation=False)
(ROOT/'02_ACTUAL_OPT_IN_SOURCEFREE_CONSUMER_PREVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
(ROOT/'observations').mkdir(exist_ok=True)
(ROOT/'observations/native_imports_and_calls.json').write_text(json.dumps(trace,indent=2)+'\n')
print('Fresh preview: both real clients; current/historical, Y change, ZERO_SUPPORT, four selective grant changes; imports',len(trace['imports']))
