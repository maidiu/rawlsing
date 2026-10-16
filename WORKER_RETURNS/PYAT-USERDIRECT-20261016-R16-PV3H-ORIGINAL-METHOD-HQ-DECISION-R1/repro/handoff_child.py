"""One positive six-consumer handoff; real abrupt/cold/current/history behavior."""
from physical import *
from method_receipt import build,verify
import time
from rawlsing_next.pre553_empirical_objects import ExactRef
root=Path(sys.argv[1]);mode=sys.argv[2];root.mkdir(parents=True,exist_ok=True);policy=root/'fixture_current_owner.json'
if mode=='offline':
 owner=FixtureOwnerControl(policy_path=policy);api=RequestAPI(owner.client(),owner._attest);history=json.loads((root/'first.json').read_text())['report']
 try:api.read_current_consumer_material(owner.installation.register,history)
 except ValueError as e:assert str(e)=='OFFLINE_FACT_RESTORATION_HOLD';reason=str(e)
 else:raise AssertionError('SOURCELESS_CURRENT_USE')
 write(root/'offline.json',dict(pid=os.getpid(),claim=reason));raise SystemExit()
with Trace() as trace:
 owner,api,fx,installation=prepare(root/'ledger',policy=policy,provision=mode=='first')
 prior=None
 if mode=='replay':
  old=json.loads((root/'first.json').read_text());prior={x['original_expected_work_key']:ExactRef(**x['consumer_ref']) for x in old['report']['links']}
 kwargs=args(fx)
 if prior:kwargs['prior_consumer_refs']=prior
 report=api.run_sourcefree_with_register(**kwargs);current=api.read_current_consumer_material(fx['register'],report);original_receipts=receipts(fx)
 receipt=build(owner,report,current,original_receipts);verify(receipt)
 result=dict(pid=os.getpid(),report=report,current=current,method_receipt=receipt,original_receipts=original_receipts,new_durable_jobs=[len(x) for x in fx['calls']],trace=trace.data(),native_reattestation=reattest())
assert result['new_durable_jobs']==([3,3] if mode=='first' else [0,0])
if mode=='replay':
 assert receipt==old['method_receipt'];assert original_receipts==old['original_receipts'];assert report['links']==old['report']['links'];assert report['nonrunnable']==old['report']['nonrunnable']
 expected=json.loads((R/'handoff_oracle.json').read_text())['cold']['actual_replay_recomputation']
 assert all(result['trace']['call_counts'][k]==v for k,v in expected.items()),result['trace']['call_counts']
write(root/(mode+'.json'),result)
if mode=='first':
 write(root/'ready.json',dict(pid=os.getpid(),method_hash=receipt['method_receipt_hash'],new_durable_jobs=result['new_durable_jobs'],six_receipts=sum(len(x['records']) for x in original_receipts)))
 while True:time.sleep(.2)
# Real retained owner history is verified after source withdrawal, never regranted.
old_report=deepcopy(report);old_receipt=deepcopy(receipt);before_B=api.read_current_consumer_material(fx['register'],report,namespace='PV2-ADULT-B')
control=FixtureOwnerControl(policy_path=policy);control.withdraw('PV2-ADULT-A','PV3A_HANDOFF_SOURCE_A_WITHDRAWAL')
A=api.read_current_consumer_material(fx['register'],report,namespace='PV2-ADULT-A');B=api.read_current_consumer_material(fx['register'],report,namespace='PV2-ADULT-B');owner.client().verify_history(report)
assert not A['servable'] and A['links']==[] and B==before_B and report==old_report and receipt==old_receipt
write(root/'history_and_current.json',dict(A_current=A,B_current=B,B_before=before_B,archival_A=[x for x in report['links'] if x['original_identity']['original']['respondent_namespace']=='PV2-ADULT-A'],original_history_verified=True,history_unchanged=True,method_receipt_unchanged=True,historical_use_only=True,generic_current=api.read_current_consumer_material(fx['register'],report,semantics='GENERIC_NATIVE')))
