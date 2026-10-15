"""Actual marker, imported modules, original blob preimages and R3 frozen source."""
import datetime,hashlib,importlib,importlib.metadata,json,os,pathlib,platform,subprocess
from r3.data import verify_freeze
ROOT=pathlib.Path(os.environ['BL3_RETURN']);RT=ROOT/'runtime_root';sel=json.loads((ROOT/'source_selector.json').read_text())
for r in sel['files']:
 b=(RT/r['staging_path']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==r['git_blob_sha1'];assert hashlib.sha256(b).hexdigest()==r['sha256']
modules={}
for n in ['assay.architecture','assay.mock_policy','assay.scoring','assay.transport','r3.data','r3.policies','r3.transport','r3.analysis','r3.audit']:
 m=importlib.import_module(n);p=pathlib.Path(m.__file__).resolve();b=p.read_bytes();modules[n]=dict(file='$BL3_RETURN/'+str(p.relative_to(ROOT)),sha256=hashlib.sha256(b).hexdigest(),git_blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest())
raw=(RT/'runtime_marker.json').read_bytes();marker=json.loads(raw)
obj=dict(schema='BL3_LIVE_ENVIRONMENT_PROBE@1',at=datetime.datetime.now(datetime.timezone.utc).isoformat(),marker=marker,marker_sha256=hashlib.sha256(raw).hexdigest(),python=platform.python_version(),pytest=importlib.metadata.version('pytest'),git=subprocess.check_output(['git','--version'],text=True).strip(),branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),original_files_verified=len(sel['files']),actual_imports=modules,R3_freeze=verify_freeze(),model='gpt-6.1-sol',effort='high',model_evidence='Own current-session turn_context verified before tests; no personal session path exported',external_experimental_model_calls=0)
(ROOT/'repro/live_environment_probe.json').write_text(json.dumps(obj,indent=2)+'\n');print('LIVE_VERIFIED',len(sel['files']),'ORIGINAL_FILES',len(modules),'IMPORTS','R3_FROZEN',obj['R3_freeze'])
