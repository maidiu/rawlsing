import json, os, subprocess, sys, time
from pathlib import Path
root=Path(os.environ['FAKE_ROOT']); repo=Path(os.environ['REPO']); cfg=root/'repo/config.json'; run=root/'repo/controller-state/fake-attest'; work=root/'work'; run.mkdir(parents=True,exist_ok=True); work.mkdir(exist_ok=True)
# supervisor process creates its own child and reports PIDs
sup_code="import os,subprocess,sys,time; c=subprocess.Popen([sys.executable,'-c','import time;time.sleep(120)']); open(os.environ['SUP_FILE'],'w').write(str(os.getpid())+'\\n'+str(c.pid)); time.sleep(120)"
sup_file=root/'sup.pid'; sup_file.unlink(missing_ok=True)
sup=subprocess.Popen([sys.executable,'-c',sup_code],env={**os.environ,'SUP_FILE':str(sup_file)})
obs=subprocess.Popen([sys.executable,'-c','import time;time.sleep(120)'])
for _ in range(100):
    if sup_file.is_file(): break
    time.sleep(0.05)
s,c=map(int,sup_file.read_text().split())
job={'job_id':'fake-attest','session':'ses_e2186e745ffecK1Ilg4cw26pVu','grant_id':'fake-grant','argv':['/usr/bin/true']}
binding={'session':job['session'],'worktree':str(work),'recipient_thread':'00000000-0000-4000-8000-000000000000','grant':{'id':'fake-grant','argv_sha256':__import__('hashlib').sha256(json.dumps(job['argv'],separators=(',',':')).encode()).hexdigest()},'sorok_currentness':{'role':'REVIEWER','task_id':'AUTOMATIC_CURRENTNESS_R1','expected_session':'ses_e2186e745ffecK1Ilg4cw26pVu','expected_source_commit':'ea5e48cf3240e72e39cd19be3120ad727902eee2','return_filename':'return/REVIEW_RECEIPT.json'}}
for name,value in [('job.json',job),('binding.json',binding),('launch.json',{'job_id':'fake-attest','child_pid':c,'supervisor_pid':s,'observer_pid':obs.pid,'run_dir':str(run)}),('process.json',{'job_id':'fake-attest','session':job['session'],'grant_id':job['grant_id'],'pid':c,'started_utc':'2026-11-16T06:50:00+00:00'}),('completion.json',{'job_id':'fake-attest','session':job['session'],'grant_id':job['grant_id'],'pid':c,'exit_code':0})]:
    (run/name).write_text(json.dumps(value,indent=2)+'\n')
proc=subprocess.run([sys.executable,'-B',str(repo/'SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py'),'--config',str(cfg),'attest-launch','--run-dir',str(run)],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
(root/'attest.out').write_text(proc.stdout); (root/'attest.err').write_text(proc.stderr); (root/'attest.exit').write_text(str(proc.returncode)+'\n')
print('exit',proc.returncode); print(proc.stdout); print(proc.stderr,file=sys.stderr)
for p in (sup,obs):
    try: p.terminate()
    except Exception: pass
