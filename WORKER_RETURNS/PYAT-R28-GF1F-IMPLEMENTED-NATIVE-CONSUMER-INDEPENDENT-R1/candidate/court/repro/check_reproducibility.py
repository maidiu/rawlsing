"""Verify clean bootstrap without any ignored runtime/frozen input directories."""
from pathlib import Path
import shutil,subprocess,sys,json,os
R=Path(__file__).resolve().parents[1]
check=R/'runtime_root/staging_check3/WORKER_RETURNS'/R.name
check.mkdir(parents=True,exist_ok=False)
for name in ('repro','tests','authority'):shutil.copytree(R/name,check/name,ignore=shutil.ignore_patterns('__pycache__'))
commands=[]
for command in ([sys.executable,str(check/'repro/stage.py')],[sys.executable,str(check/'repro/run.py'),'pv3']):
 p=subprocess.run(command,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 commands.append({'argv':command,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 if p.returncode:break
(R/'observations/clean_bootstrap_check.json').write_text(json.dumps({'commands':commands,'no_existing_runtime_or_frozen_inputs':True},indent=2)+'\n')
assert len(commands)==2 and all(c['exit']==0 for c in commands),commands[-1]
print('CLEAN_GIT_BLOB_BOOTSTRAP_AND_28_REPAIR_GUARDS_PASS')
