"""Portable exact environment for the non-pytest source/effect probes."""
import pathlib,os,sys,subprocess,json,time
RET=pathlib.Path(__file__).resolve().parents[1];RT=RET/'runtime_root';C=RT/'WORKER_RETURNS/SOROK-R3-HQ298-SC0-VALUE-BEARING-PORT-R1'
name=sys.argv[1]
if name not in ['connection_probe','facade_probe','probe_environment']:raise SystemExit('Unknown probe')
cmd=[sys.executable,str(RET/'repro'/(name+'.py'))];t=time.time()
env=dict(os.environ,PYTHONPATH=os.pathsep.join(map(str,[RT,C,C/'staging/ns',C/'staging/ns/rawlsing_next/tests',RT/'rawlsing_next/tests'])),RC0_RUNTIME=str(RT),RC0_RETURN=str(RET),RC0_SUITE=name,PYTHONDONTWRITEBYTECODE='1')
r=subprocess.run(cmd,cwd=RT,env=env,capture_output=True,text=True)
log=r.stdout+r.stderr
log=log.replace(str(RT),'$RC0_RUNTIME').replace(str(RET),'$RC0_RETURN')
(RET/'repro'/(name+'.log')).write_text(log)
(RET/'repro'/(name+'_execution.json')).write_text(json.dumps(dict(command=['python3','$RC0_RETURN/repro/'+name+'.py'],launcher=['python3','$RC0_RETURN/repro/run_probe.py',name],cwd='$RC0_RUNTIME',exit_code=r.returncode,seconds=time.time()-t),indent=2)+'\n')
print(log)
if r.returncode:raise SystemExit(r.returncode)
