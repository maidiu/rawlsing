import pathlib,subprocess,os,sys,json,time,signal,hashlib,shutil
R=pathlib.Path(__file__).resolve().parents[1];root=R/'runtime/handoff';E=R/'evidence/handoff';E.mkdir(parents=True,exist_ok=True)
assert not root.exists(),'EXISTING_HANDOFF_REFUSED';root.mkdir()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(R/'repro'))
cmd=[sys.executable,str(R/'repro/handoff_child.py'),str(root)];f=(E/'first.stdout').open('w');p=subprocess.Popen(cmd+['first'],env=env,stdout=f,stderr=subprocess.STDOUT);deadline=time.monotonic()+60
while not (root/'ready.json').exists() and p.poll() is None and time.monotonic()<deadline:time.sleep(.05)
if not (root/'ready.json').exists():
 if p.poll() is None:p.kill();p.wait()
 f.close();raise RuntimeError('HANDOFF_NOT_READY:'+str(p.returncode))
assert p.poll() is None;ready=json.loads((root/'ready.json').read_text());assert ready['pid']==p.pid and ready['six_receipts']==6
before={str(q.relative_to(root)):q.read_bytes() for q in (root/'ledger').rglob('*') if q.is_file()}
p.kill();p.wait(timeout=10);f.close();assert p.returncode==-signal.SIGKILL
processes=[dict(mode='first',pid=p.pid,exit=p.returncode,signal='SIGKILL')];(E/'first_terminal.json').write_text(json.dumps(processes[0],indent=2)+'\n')
for mode in ['replay','offline']:
 child=subprocess.run(cmd+[mode],env=env,capture_output=True,text=True);(E/(mode+'.stdout')).write_text(child.stdout+child.stderr);processes.append(dict(mode=mode,exit=child.returncode));assert child.returncode==0,child.stderr
replay=json.loads((root/'replay.json').read_text());assert replay['pid']!=p.pid
after={str(q.relative_to(root)):q.read_bytes() for q in (root/'ledger').rglob('*') if q.is_file()};assert before==after
for name in ['first.json','replay.json','offline.json','history_and_current.json','ready.json']:shutil.copyfile(root/name,E/name)
for name,b in after.items():
 q=E/'native_journals'/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
x=dict(processes=processes,first_pid=p.pid,replay_pid=replay['pid'],first_new_durable=[3,3],replay_new_durable=[0,0],recomputed_owner_calls=replay['trace']['call_counts'],byte_identical_journals=True,journal_sha256={k:hashlib.sha256(v).hexdigest() for k,v in after.items()},stable_method_receipt_hash=ready['method_hash'],grade='NEW_BOUNDED_HANDOFF_DEMONSTRATION_NOT_REPEATED_PV3N_COURT')
(E/'summary.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2))
