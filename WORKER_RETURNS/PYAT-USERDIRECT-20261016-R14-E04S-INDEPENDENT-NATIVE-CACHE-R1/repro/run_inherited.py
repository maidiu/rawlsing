import subprocess,sys,pathlib,json
R=pathlib.Path(__file__).resolve().parents[1];rows=[]
for mode in ['independent51','author37','native231','author_hostiles37']:
 p=subprocess.run([sys.executable,str(R/'repro/run.py'),mode],cwd=R,capture_output=True,text=True)
 print(p.stdout,p.stderr,flush=True);rows.append(dict(mode=mode,exit=p.returncode))
(R/'observations/inherited_exits.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(int(any(x['exit'] for x in rows)))
