"""Actual SIGKILL then cold recovery; preserve the native checkpoint/journal bytes."""
from pathlib import Path
import subprocess,sys,os,json,time,hashlib,signal,shutil
R=Path(__file__).resolve().parents[1];root=R/'runtime/abrupt_court';E=R/'evidence/abrupt';E.mkdir(parents=True,exist_ok=True)
if root.exists():raise SystemExit('EXISTING_ABRUPT_COURT_REFUSED')
root.mkdir();C=R/'runtime/court';RT=C/'runtime_root'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=os.pathsep.join(map(str,[R/'repro',C/'repro',RT,RT/'candidate/repro',C/'frozen_pv2i/repro'])))
cmd=[sys.executable,str(R/'repro/abrupt_child.py'),str(root)]
f=(E/'first.stdout').open('w');first=subprocess.Popen(cmd+['first'],env=env,stdout=f,stderr=subprocess.STDOUT);deadline=time.monotonic()+60
while not (root/'ready_to_kill.json').exists() and first.poll() is None and time.monotonic()<deadline:time.sleep(0.05)
if not (root/'ready_to_kill.json').exists():
 if first.poll() is None:first.kill();first.wait()
 f.close();raise RuntimeError('FIRST_PROCESS_DID_NOT_REACH_COMMITTED_READY:'+str(first.returncode))
assert first.poll() is None
ready=json.loads((root/'ready_to_kill.json').read_text());assert ready['pid']==first.pid and ready['actual_receipts']==6
before={str(p.relative_to(root)):p.read_bytes() for p in (root/'ledger').rglob('*') if p.is_file()}
first.kill();first.wait(timeout=10);f.close();assert first.returncode==-signal.SIGKILL
rows=[dict(mode='first',pid=first.pid,exit=first.returncode,signal='SIGKILL',ready=ready,command=cmd+['first'])]
for mode in ['replay','offline']:
 p=subprocess.run(cmd+[mode],env=env,capture_output=True,text=True);(E/(mode+'.stdout')).write_text(p.stdout+p.stderr);rows.append(dict(mode=mode,exit=p.returncode,command=cmd+[mode]));assert p.returncode==0,p.stderr
replay=json.loads((root/'replay.json').read_text());assert replay['pid']!=first.pid
assert replay['durable_calls']==[0,0]
after={str(p.relative_to(root)):p.read_bytes() for p in (root/'ledger').rglob('*') if p.is_file()};assert before==after
for name in ['first.json','replay.json','offline.json','selective_revocation.json','ready_to_kill.json']:shutil.copyfile(root/name,E/name)
for path,b in after.items():
 d=E/'native_ledger_bytes'/path;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(b)
summary=dict(processes=rows,first_pid=first.pid,replay_pid=replay['pid'],actual_abrupt_death=True,first_durable=[3,3],replay_durable=[0,0],six_original_UnitExecutionReceipt_objects_restored=True,ledger_byte_identical=True,ledger={p:hashlib.sha256(b).hexdigest() for p,b in after.items()},source_calls_replay=replay['trace']['call_counts'],native_source_reattestation=replay['reattested_native_files'],selective_withdrawal='A denied B entire current value stable; historical receipts immutable',offline='OFFLINE_FACT_RESTORATION_HOLD; no live source reattestation')
(E/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
