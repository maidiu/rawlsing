"""Fresh interpreter production/inspection/reconstruction of TEST_ONLY SQLite state."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parent;ROOT=R/'runs/runtime';P=ROOT/'WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1'
def child(mode,path):
 sys.path[:0]=[str(ROOT/'review'),str(ROOT),str(P)]
 from support import CandidateStore,LaterActionConsumer,digest,run
 from candidate.later_action import read_target_for_later_action
 with CandidateStore(path) as s:
  if mode=='build':
   r=run(s);assert r.receipt.committed and r.decision.branch.value=='CREATE'
  ids=s.committed_target_ids();assert len(ids)==1;key=next(iter(ids))
  read=read_target_for_later_action(s,consumer=LaterActionConsumer('TEST_ONLY_COLD_PROCESS','target'),middle_state_id=key,as_of=30,commit_time=15)
  assert read.status.value=='ACTION_ADMISSION_HELD'
  assert read.state_hash==digest(s.read_target_state(key))
  return dict(snapshot=s.snapshot(),snapshot_hash=digest(s.snapshot()),target_hash=s.target_state_hash(),read_hash=read.read_receipt_hash,readset=list(read.readset_refs),integrity=s.db.execute('PRAGMA integrity_check').fetchone()[0],pid=os.getpid(),mode=mode)
def main():
 if len(sys.argv)>1:
  print(json.dumps(child(sys.argv[1],Path(sys.argv[2]))));return
 out=R/'runs/cold';out.mkdir(parents=True,exist_ok=True)
 rows=[]
 for filename,mode in [('a.sqlite','build'),('a.sqlite','inspect'),('b.sqlite','build'),('b.sqlite','inspect')]:
  p=out/filename
  if mode=='build' and p.exists():p.unlink()
  r=subprocess.run([sys.executable,'-B',str(Path(__file__).resolve()),mode,str(p)],cwd=ROOT,text=True,capture_output=True,check=True)
  rows.append(json.loads(r.stdout))
 assert len({x['pid'] for x in rows})==4
 for field in ['snapshot_hash','snapshot','target_hash','read_hash','readset','integrity']:
  assert all(x[field]==rows[0][field] for x in rows),field
 assert rows[0]['integrity']=='ok'
 (R/'evidence/cold_replay.json').write_text(json.dumps(dict(grade='TEST_ONLY_FRESH_PROCESS_LOGICAL_REPLAY_PASS',runs=rows),indent=2)+'\n')
 print('Four distinct processes; exact logical snapshots/read receipts; two reconstructed databases')
if __name__=='__main__':main()
