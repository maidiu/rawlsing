"""Read-only startup import/exec audit inherited by actual owner subprocesses."""
import atexit,hashlib,json,os,pathlib,sys
base=pathlib.Path(os.environ['PV_RUNTIME']).resolve()
ret=pathlib.Path(os.environ['PV_RETURN'])
pins={r['path']:r for r in json.loads((ret/'02_EXACT_COMPOSITE_SOURCE_SELECTOR.json').read_text())['files']}
executed={}
def check(path):
 p=pathlib.Path(path).resolve()
 if not p.is_relative_to(base):return None
 rel=p.relative_to(base).as_posix()
 if rel not in pins:return None
 ref=pins[rel];sha=hashlib.sha256(p.read_bytes()).hexdigest()
 if sha!=ref['sha256']:os._exit(91)
 return dict(path=rel,file=str(p),sha256=sha,git_blob=ref['git_blob'],commit=ref['commit'],match=True)
def hook(event,args):
 if event=='exec':
  f=args[0].co_filename
  if f.startswith(str(base)):
   row=check(f)
   if row:executed[row['path']]=row
sys.addaudithook(hook)
def finish():
 modules=[]
 for name,m in sorted(sys.modules.items()):
  f=getattr(m,'__file__',None)
  if not f:continue
  if name.startswith('rawlsing_next') and not pathlib.Path(f).resolve().is_relative_to(base):os._exit(91)
  row=check(f)
  if row:modules.append(dict(module=name,**row))
 out=ret/'repro/child_audits';out.mkdir(exist_ok=True)
 (out/(os.environ['PV_SUITE']+'_'+str(os.getpid())+'.json')).write_text(json.dumps(dict(pid=os.getpid(),argv=sys.argv,executed=list(executed.values()),imports=modules),indent=2))
atexit.register(finish)
