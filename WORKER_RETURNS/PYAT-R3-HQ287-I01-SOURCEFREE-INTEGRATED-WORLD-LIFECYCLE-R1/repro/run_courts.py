import datetime,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[3];OUT=pathlib.Path(__file__).resolve().parent
P01=['rawlsing_next/tests/'+n for n in ('test_pre553_v2_durable_consumer_integration_candidate.py','test_pre553_batch_durable_checkpoint_candidate.py','test_pre553_governed_batch_checkpoint_integration_candidate.py','test_pre553_original_workload_v2_verifier_candidate.py','test_pre553_original_workload_v2_mutation_hostiles_candidate.py')]
def run(label,paths,extra=()):
 cmd=[sys.executable,'-m','pytest',*paths,'-q','-p','no:cacheprovider',f'--junitxml={OUT/(label+".xml")}',*extra]
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(OUT)+os.pathsep+str(ROOT)}
 p=subprocess.run(cmd,cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (OUT/(label+'.log')).write_text(p.stdout)
 manifest=OUT/'executions.json';records=json.loads(manifest.read_text()) if manifest.exists() else []
 records.append(dict(label=label,argv=cmd,cwd=str(ROOT),env={'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':env['PYTHONPATH']},exit=p.returncode,timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()));manifest.write_text(json.dumps(records,indent=2)+'\n')
 print(label,p.returncode,p.stdout.splitlines()[-1],flush=True)
if __name__=='__main__':run('p01_complete',P01,('-p','p01_paths'))
