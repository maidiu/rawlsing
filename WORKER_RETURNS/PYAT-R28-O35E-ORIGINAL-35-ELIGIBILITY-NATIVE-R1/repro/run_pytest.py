"""Fresh-process, source-free, byte-verified actual native pytest worker."""
import hashlib,json,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
PIN=HERE/'runtime/pinned'
os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
spec=json.loads((HERE/'SOURCE_INPUTS.json').read_text())
court_pin=HERE/'COURT_CODE_PIN.json'
if court_pin.exists():
 for path,record in json.loads(court_pin.read_text())['files'].items():
  assert hashlib.sha256((HERE/path).read_bytes()).hexdigest()==record['sha256'],path
for path,record in spec['files'].items():
 data=(PIN/path).read_bytes()
 assert hashlib.sha256(data).hexdigest()==record['sha256'],path
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==record['git_blob'],path
def guard(event,args):
 if event in ('socket.connect','socket.getaddrinfo'):
  raise PermissionError('O35E sourcefree court forbids network')
 if event=='open' and isinstance(args[0],(str,bytes)):
  name=os.fsdecode(args[0]).lower()
  if name.endswith(('.sav','.dta','.zsav','.por')):
   raise PermissionError('O35E original source file access not granted')
sys.addaudithook(guard)
# No current checkout import fallback. Exact staged package wins; dependencies
# remain the established Python/pytest installation.
sys.path[:]=[str(PIN),str(HERE/'repro')]+[p for p in sys.path if p and 'Rawlsing' not in p]
import pytest
label=sys.argv[1]
tests=sys.argv[2:]
obs=HERE/'observations';obs.mkdir(exist_ok=True)
code=pytest.main(['-q','-c','/dev/null','--rootdir',str(HERE),
 '--import-mode=importlib','-p','no:cacheprovider',f'--junitxml={obs/label}.xml',*tests])
imports=[]
for name,module in sorted(sys.modules.items()):
 if not name.startswith('rawlsing_next'):continue
 file=getattr(module,'__file__',None)
 if file is None:continue
 path=Path(file).resolve();rel=path.relative_to(PIN).as_posix()
 assert rel in spec['files'],(name,rel)
 data=path.read_bytes();record=spec['files'][rel]
 assert hashlib.sha256(data).hexdigest()==record['sha256']
 imports.append({'module':name,'__file__':'$RETURN/runtime/pinned/'+rel,
  'actual_path_under_verified_pin':True,'git_blob':record['git_blob'],'sha256':record['sha256']})
(obs/f'{label}_imports.json').write_text(json.dumps({'python':sys.version,'executable':sys.executable,
 'pinned_commit':spec['pin'],'all_project_modules_verified':True,'modules':imports,
 'pytest_version':pytest.__version__,'exit_code':int(code)},indent=2)+'\n')
sys.exit(code)
