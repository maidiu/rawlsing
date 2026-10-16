"""Own cold executable: exact owner imports, original receipts, no surrogate IDs."""
from physical import *
import time
from rawlsing_next.pre553_empirical_objects import ExactRef
root=Path(sys.argv[1]);mode=sys.argv[2];root.mkdir(parents=True,exist_ok=True);policy=root/'selected_current_owner.json'
if mode=='offline':
 o=FixtureOwnerControl(policy_path=policy);api=RequestAPI(o.client(),o._attest);reg=o.installation.register;history=json.loads((root/'first.json').read_text())['report']
 try:api.read_current_consumer_material(reg,history)
 except ValueError as e:assert str(e)=='OFFLINE_FACT_RESTORATION_HOLD';claim=str(e)
 else:raise AssertionError('OFFLINE_FACT_SERVED_WITHOUT_LIVE_SOURCE')
 write(root/'offline.json',dict(pid=os.getpid(),claim=claim,source_calls=0,decisions={ns:o.client().resolve(ns).__dict__ for ns,_ in o.installation.source_editions},imports=imports()));raise SystemExit()
trace=Trace();fx=None
try:
 with Trace() as trace:
  owner,api,fx,installation=prepare(root/'ledger',policy=policy,provision=mode=='first')
  prior=None
  if mode!='first':
   first=json.loads((root/'first.json').read_text());prior={x['original_expected_work_key']:ExactRef(**x['consumer_ref']) for x in first['report']['links']}
  kw=args(fx)
  if prior:kw['prior_consumer_refs']=prior
  report=api.run_sourcefree_with_register(**kw)
  actual=receipts(fx);current=api.read_current_consumer_material(fx['register'],report)
  result=dict(pid=os.getpid(),mode=mode,installed_before_fixture=installation,reattested_native_files=reattest(),report=report,current=current,durable_calls=[len(c) for c in fx['calls']],actual_UnitExecutionReceipts=actual,trace=trace.data())
  if mode=='first':assert result['durable_calls']==[3,3]
  else:
   assert result['durable_calls']==[0,0] and all(x['run']['executed']==[] for x in report['owner_reports'])
   assert report['links']==first['report']['links'] and report['nonrunnable']==first['report']['nonrunnable']
   assert actual==first['actual_UnitExecutionReceipts']
except Exception as exc:
 write(root/(mode+'_failure.json'),dict(pid=os.getpid(),exception=type(exc).__name__,code=str(exc),durable_calls=[len(c) for c in fx['calls']] if fx else None,trace=trace.data()))
 raise
write(root/(mode+'.json'),result)
if mode=='first':
 write(root/'ready_to_kill.json',dict(pid=os.getpid(),durable_calls=result['durable_calls'],actual_receipts=sum(len(x['records']) for x in actual)))
 while True:time.sleep(0.2)
# Own current read uses still-live reattestation while an independent fixture control advances policy.
b=api.read_current_consumer_material(fx['register'],report,namespace='PV2-ADULT-B');past=deepcopy(report);o2=FixtureOwnerControl(policy_path=policy);o2.withdraw('PV2-ADULT-A','PV3N_SEPARATE_CONTROL_WITHDRAWAL')
a=api.read_current_consumer_material(fx['register'],report,namespace='PV2-ADULT-A');after=api.read_current_consumer_material(fx['register'],report,namespace='PV2-ADULT-B')
assert not a['servable'] and after==b and report==past
write(root/'selective_revocation.json',dict(A=a,B_before=b,B_after=after,historical_receipts_unchanged=True,policy=json.loads(policy.read_text())))
