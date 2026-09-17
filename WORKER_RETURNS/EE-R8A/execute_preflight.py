import datetime,hashlib,json,os,pathlib,sys,uuid
root=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(root/'runtime_code'))
from rawlsing_next.ee_w4_harness_runtime import run_wait4,rusage_metrics
rows=[]
(root/'preflight').mkdir(exist_ok=True)
run_id='EE-R8A-PREFLIGHT-'+str(uuid.uuid4())
for universe in ['WVS7','LiTS-I']:
 out=root/'preflight'/f'{universe}.stdout.json';err=root/'preflight'/f'{universe}.stderr.txt'
 argv=[str(root/'venv/bin/python'),'-I',str(root/'decoder_preflight.py'),str(root),universe]
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 code,usage,wall=run_wait4(argv,out,err,os.environ.copy())
 metrics={'wall_ns':wall,**rusage_metrics(usage)}
 row={'run_id':run_id,'universe':universe,'argv':argv,'started_at_utc':started,'ended_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':code,'metrics':metrics,'child_stdout_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'child_stderr_sha256':hashlib.sha256(err.read_bytes()).hexdigest(),'child_stderr_bytes':err.stat().st_size,'child_receipt':json.loads(out.read_text()) if code==0 else None,'required_metric_gate':'FAIL_REQUIRED_PEAK_RSS_BYTES_NULL' if metrics['peak_rss_bytes'] is None else 'PASS','measurement_scope':'ACTUAL_DECODER_PREFLIGHT_ONLY__NOT_CANDIDATE_COMPARISON'}
 rows.append(row)
 print(universe,code,row['required_metric_gate'],flush=True)
 assert code==0,err.read_text()
(root/'preflight_receipt.json').write_text(json.dumps({'run_id':run_id,'parent_pid':os.getpid(),'runtime_freeze_sha256':hashlib.sha256((root/'runtime_freeze.json').read_bytes()).hexdigest(),'preflight_driver_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'decoder_child_driver_sha256':hashlib.sha256((root/'decoder_preflight.py').read_bytes()).hexdigest(),'executions':rows,'candidate_invocations':0,'status':'BLOCKED_REQUIRED_METRIC_NULL_ON_DARWIN'},indent=2)+'\n')
