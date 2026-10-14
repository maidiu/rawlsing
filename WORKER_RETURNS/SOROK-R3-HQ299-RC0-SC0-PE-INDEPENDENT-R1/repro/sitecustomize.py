"""Read-only exact source audit inherited by child Python processes."""
import atexit,hashlib,json,os,pathlib,sys
base=pathlib.Path(os.environ['RC0_RUNTIME']).resolve();ret=pathlib.Path(os.environ['RC0_RETURN'])
pins={r['staging_path']:r for r in json.loads((ret/'source_selector.json').read_text())['files']};executed={}
def checked(filename):
 p=pathlib.Path(filename).resolve()
 if not p.is_relative_to(base):return None
 rel=p.relative_to(base).as_posix()
 if rel not in pins:return None
 raw=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest();row=pins[rel]
 if blob!=row['git_blob_sha1']:os._exit(91)
 return dict(staging_path=rel,imported_file='$RC0_RUNTIME/'+rel,git_blob_sha1=blob,sha256=hashlib.sha256(raw).hexdigest(),source_commit=row['commit'],source_path=row['source_path'],match=True)
def hook(event,args):
 if event=='exec' and args[0].co_filename.startswith(str(base)):
  row=checked(args[0].co_filename)
  if row:executed[row['staging_path']]=row
sys.addaudithook(hook)
def finish():
 imports=[]
 for name,m in sorted(sys.modules.items()):
  f=getattr(m,'__file__',None)
  if not f:continue
  if name.startswith(('rawlsing_next','port.')) and not pathlib.Path(f).resolve().is_relative_to(base):os._exit(91)
  row=checked(f)
  if row:imports.append(dict(module=name,**row))
 out=ret/'repro/import_audits';out.mkdir(exist_ok=True)
 argv=[str(v).replace(str(base),'$RC0_RUNTIME').replace(str(ret),'$RC0_RETURN') for v in sys.argv]
 (out/(os.environ['RC0_SUITE']+'_'+str(os.getpid())+'.json')).write_text(json.dumps(dict(pid=os.getpid(),argv=argv,executed=list(executed.values()),imports=imports),indent=2)+'\n')
atexit.register(finish)
