import subprocess,sys,pathlib,os,json
R=pathlib.Path(__file__).resolve().parents[1];rows=[]
for mode in ['first','replay']:
 cmd=[sys.executable,str(R/'repro/cold.py'),mode];p=subprocess.run(cmd,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,cwd=R/'runtime');(R/'observations'/('independent_cold_'+mode+'.log')).write_text(p.stdout+'\n'+p.stderr);rows.append(dict(mode=mode,command=cmd,exit=p.returncode));print(mode,p.returncode,p.stdout[-250:],p.stderr[-500:],flush=True)
(R/'observations/cold_exits.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(int(any(x['exit'] for x in rows)))
