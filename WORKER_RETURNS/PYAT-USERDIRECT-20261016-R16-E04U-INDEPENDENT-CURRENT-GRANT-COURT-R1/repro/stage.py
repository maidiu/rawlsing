"""Exact original 94-file/native closure plus six immutable E04R baseline files."""
import pathlib,json,subprocess,hashlib
R=pathlib.Path(__file__).resolve().parents[1];RT=R/'runtime_root'
if RT.exists():raise SystemExit('Refusing to overwrite existing runtime_root')
# Primary inputs are ignored runtime artifacts, recoverable from exact Git objects.
for item in json.loads((R/'primary_input_manifest.json').read_text()):
 b=subprocess.check_output(['git','-c','gc.auto=0','show',item['commit']+':'+item['path']],cwd=R)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==item['git_blob']
 assert hashlib.sha256(b).hexdigest()==item['sha256']
 out=R/item['local'];out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():assert out.read_bytes()==b
 else:out.write_bytes(b)
RT.mkdir();rows=[]
def put(c,p,local,expected=None):
 b=subprocess.check_output(['git','-c','gc.auto=0','show',c+':'+p],cwd=R);oid=subprocess.check_output(['git','rev-parse',c+':'+p],cwd=R,text=True).strip();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
 if expected:assert oid==expected
 out=RT/local;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b);rows.append(dict(commit=c,path=p,local=str(out.relative_to(R)),git_blob=oid,sha256=hashlib.sha256(b).hexdigest()))
selector=json.loads((R/'primary/e04n/source_selector.json').read_text());assert len(selector['files'])==94
for row in selector['files']:put(row['commit'],row['source_path'],row['staged_path'],row['git_blob_sha1'])
c='97254d0b215b5dd45580dd94608a8ec95ff8b76f';prefix='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R13-E04R-NATIVE-CACHE-INTEGRITY-REPAIR-R1/'
for p in subprocess.check_output(['git','ls-tree','--full-tree','-r','--name-only',c,prefix+'product'],cwd=R,text=True).splitlines():put(c,p,'repaired/'+p[len(prefix):])
(R/'source_manifest.json').write_text(json.dumps(rows,indent=2)+'\n');print('Exact original files staged:',len(rows))
