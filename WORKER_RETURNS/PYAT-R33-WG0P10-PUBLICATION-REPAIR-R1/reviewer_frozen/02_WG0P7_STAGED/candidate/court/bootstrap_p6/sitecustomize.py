"""P6 identity/path/call-trace transport; no frozen assertions or outputs changed.

Every inherited input except the disclosed productive module remains byte exact.
Actual imported project Python files are checked before execution, including
pytest's rewritten tests. A bootstrap error terminates instead of being ignored
by Python's normal sitecustomize error handler.
"""
import atexit,hashlib,importlib,json,os,pathlib,sys
C=pathlib.Path(__file__).resolve().parents[1]
R=C.parent
P=C/'runtime_phase_b/p5_return/review/runtime_phase_b/candidate'
AUDIT=[]
def clean(value):
 if isinstance(value,str):return value.replace(str(R.parents[1]),'<WORKTREE>').replace(str(pathlib.Path.home()),'<HOME>')
 if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
 if isinstance(value,list):return [clean(v) for v in value]
 return value
try:
 pin=json.loads((R/'CANDIDATE_CODE_PIN.json').read_text())
 original=json.loads((R/'SOURCE_INPUTS.json').read_text())['files']
 expected={(R/r['staged_path']).resolve():r for r in original}
 for row in pin['files']:expected[(R/row['staged_path']).resolve()]=row
 def verify(path):
  path=pathlib.Path(path).resolve();row=expected.get(path)
  if row is None:raise ImportError('UNPINNED_PROJECT_SOURCE:'+str(path))
  data=path.read_bytes();sha=hashlib.sha256(data).hexdigest()
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  if sha!=row['sha256'] or blob!=row['git_blob_sha1']:raise ImportError('SOURCE_PREIMAGE_CHANGED:'+str(path))
  return dict(file=str(path),sha256=sha,git_blob_sha1=blob)
 for path in expected:verify(path)
 def before_exec(event,args):
  if event=='exec':
   p=pathlib.Path(args[0].co_filename)
   if p.is_absolute() and p.resolve().is_relative_to(R):AUDIT.append(verify(p))
 sys.addaudithook(before_exec)
 sys.path[:0]=[str(P/'repro'),str(P/'pinned'),str(C/'repro')]
 import wg0p4_workload as w
 import phase_b_support_v1 as support
 support.C=P
 def physical_modules():
  result={}
  for name in ('pre553_c11_repository','pre553_c11_ingest','pre553_empirical_query','pre553_batch_runner','pre553_empirical_objects','pre553_c11_integrity'):
   module=importlib.import_module('rawlsing_next.'+name);path=pathlib.Path(module.__file__).resolve()
   if not path.is_relative_to(P/'pinned/rawlsing_next'):raise ImportError('WRONG_NATIVE_OWNER_ROOT:'+str(path))
   result[name]=verify(path)
  return result
 support.verified_modules=physical_modules
 def profile_calls(calls):
  def trace(frame,event,arg):
   if event=='call' and str(P) in frame.f_code.co_filename and frame.f_code.co_name in ('__init__','enumerate','build_executable_plan','make_executor','run_plan','run','execute_empirical_query','consumer_effects','execute_positive_conditional','build_positive_conditional_frontier'):
    calls.append(dict(name=frame.f_code.co_name,file=frame.f_code.co_filename,line=frame.f_code.co_firstlineno))
  return trace
 support.profile_calls=profile_calls
 import phase_b_adapter_v1 as adapter
 adapter.profile_calls=profile_calls
 adapter.Adapter.candidate_sha=pin['code_snapshot_commit']
 def register_committed(self):
  import subprocess
  path=C/'observations/phase_b/reviewer_second_frontier_register.json'
  source='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R10-WG0L-INDEPENDENT-FULL-ENGINE-COURT-R1/observations/phase_b/reviewer_second_frontier_register.json'
  actual=path.read_bytes();verify(path)
  original_bytes=subprocess.check_output(['git','show','bec9a128922e4e431ce2ed862aa7802c902813ed:'+source],cwd=C)
  return actual==original_bytes
 adapter.Adapter.register_committed=register_committed
 def receipt():
  modules=[]
  for name,module in sorted(sys.modules.items()):
   file=getattr(module,'__file__',None)
   if file and pathlib.Path(file).resolve().is_relative_to(R) and file.endswith('.py'):
    # Bootstrap itself is identified by the pin, though it began before hook installation.
    modules.append(dict(module=name,**verify(file)))
  record=clean(dict(pid=os.getpid(),argv=sys.argv,python=sys.version,executable=sys.executable,
                    preexecution_project_file_checks=AUDIT,actually_loaded_modules=modules,
                    candidate_pin=pin['files'][0],native_modules=physical_modules(),
                    transport_only=['candidate identity/source root','physical call tracing','byte-exact original committed register path']))
  folder=R/'observations/imports';folder.mkdir(exist_ok=True)
  (folder/('process-'+str(os.getpid())+'.json')).write_text(json.dumps(record,indent=2)+'\n')
 atexit.register(receipt)
except BaseException as exc:
 print('WG0P6_BOOTSTRAP_REFUSE:'+type(exc).__name__+':'+str(exc),file=sys.stderr,flush=True)
 os._exit(86)
