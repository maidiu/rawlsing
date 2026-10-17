"""Reviewer cold-process court with a separately persisted trusted fixture ledger.

Pickle is only our own retained fixture-state harness, never an untrusted input or
candidate persistence API. Ledger digest is an integrity pin, not issuer signing.
"""
import pathlib,sys,os,json,pickle,hashlib,subprocess,copy
R=pathlib.Path(__file__).resolve().parents[1];RT=R/'runtime';O=R/'observations'
sys.path[:0]=list(map(str,[RT,RT/'rawlsing_next/tests',RT/'rawlsing_next',R/'repro']))
from court_support import *
import copyreg, types
def restore_mappingproxy(value):return types.MappingProxyType(value)
copyreg.pickle(types.MappingProxyType, lambda value:(restore_mappingproxy,(dict(value),)))
mode=sys.argv[1]
if mode=='prepare':
 a,q,s,acc,r=run();p=O/'trusted_fixture_state.pickle';p.write_bytes(pickle.dumps((a,q,s,acc,r)))
 native_records=rows()
 for row in native_records:
  if row['role']==NCA:row['status']='REVOKED_TEST_ONLY'
 ledger=dict(native_records=native_records,schema='R14_TRUSTED_FIXTURE_GRANTS@1',epoch=2,accepted_epoch=1,denied_native=[NCA],original_refs=a.registry.refs_by_role(),fixture_only=True,issuer_attestation=False)
 l=O/'trusted_fixture_grants.json';l.write_text(json.dumps(ledger,sort_keys=True)+'\n')
 save('r14_cold_preparation',dict(pid=os.getpid(),state_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),ledger_sha256=hashlib.sha256(l.read_bytes()).hexdigest(),accepted_request=q.binding(),accepted=acc.binding(),receipt_hash=r['receipt_hash']))
 print('prepared',os.getpid())
elif mode=='restart':
 prior=json.loads((O/'r14_cold_preparation.json').read_text());assert prior['pid']!=os.getpid()
 p=O/'trusted_fixture_state.pickle';l=O/'trusted_fixture_grants.json'
 assert hashlib.sha256(p.read_bytes()).hexdigest()==prior['state_sha256'];assert hashlib.sha256(l.read_bytes()).hexdigest()==prior['ledger_sha256']
 a,q,s,acc,old=pickle.loads(p.read_bytes());ledger=json.loads(l.read_text())
 # Apply the independently persisted current grant ledger after acceptance,
 # across process death; do not recreate a permissive field fixture.
 a.registry=TestOnlyRegistry(ledger['native_records'])
 for role in ledger['denied_native']:a.invalidate(role,'R14_PERSISTED_FIXTURE_WITHDRAWAL_EPOCH_2')
 r=a.serve(q,acc,s,consumers=clients(a,s));assert NCA not in native(r);assert GSS in native(r)
 assert r['state']=='TYPED_PARTIAL_SELECTED_WORLD';assert a.receipts[old['receipt_hash']]==old
 for key in ['structural_values','empirical_steps','consumers']:assert r[key]==old[key]
 archive=a.historical_receipt(old['receipt_hash']);assert not archive['fresh_use_authorized']
 # A genuinely fresh adapter refuses the old acceptance, then receives its own
 # acceptance after loading the same deny ledger. No grant resurrection.
 fresh=adapter(ledger['native_records'])
 for role in ledger['denied_native']:fresh.invalidate(role,'R14_PERSISTED_FIXTURE_WITHDRAWAL_EPOCH_2')
 fs=fresh.build_snapshot(q)
 try:fresh.serve(q,acc,fs)
 except E.N9SelectedWorldRefusal:old_acceptance_refused=True
 else:raise AssertionError('OLD_ACCEPTANCE_IMPORTED_AS_FRESH_AUTHORIZATION')
 fa=fresh.accept(q,fs);fr=fresh.serve(q,fa,fs,consumers=clients(fresh,fs));assert NCA not in native(fr);assert GSS in native(fr)
 # Bare reconstruction is intentionally different and is never called renewal.
 _,_,_,_,bare=run();assert NCA in native(bare)
 save('r14_cold_restart',dict(pid=os.getpid(),preparation_pid=prior['pid'],ledger=ledger,retained_receipt=old,late_withdrawal_receipt=r,fresh_ledger_loaded_receipt=fr,archival=archive,old_acceptance_refused=old_acceptance_refused,bare_reconstruction_restores_fixture_only=True,candidate_native_durable_store=False,trust_limit='Harness persisted grants and adapter state. No candidate durable-store API, publisher licence or issuer attestation established.'))
 print('restart passed',os.getpid())
else:raise ValueError(mode)
