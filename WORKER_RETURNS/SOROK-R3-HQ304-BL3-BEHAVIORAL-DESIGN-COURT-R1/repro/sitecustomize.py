"""Network denial and actual imported-source custody for every Python child."""
import atexit,hashlib,json,os,pathlib,site,sys
RET=pathlib.Path(os.environ['BL3_RETURN']);RT=RET/'runtime_root'
pins={r['staging_path']:r for r in json.loads((RET/'source_selector.json').read_text())['files']}
blocked=[]
def hook(event,args):
 if event in ('socket.connect','socket.getaddrinfo','socket.gethostbyname','socket.gethostbyaddr'):
  blocked.append(event);raise RuntimeError('BL3_ZERO_EXTERNAL_EXPERIMENTAL_CALLS_NETWORK_DENIED')
sys.addaudithook(hook)
def clean(s):
 return str(s).replace(str(RT),'$BL3_RUNTIME').replace(str(RET),'$BL3_RETURN').replace(site.getusersitepackages(),'$LOCAL_PYTHON_USER_SITE')
def finish():
 rows=[]
 for name,m in sorted(sys.modules.items()):
  f=getattr(m,'__file__',None)
  if not f:continue
  p=pathlib.Path(f).resolve()
  if name.startswith(('assay.','lab.','lab2.')) and not p.is_relative_to(RT):os._exit(91)
  if not p.is_relative_to(RET):continue
  raw=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()
  rel=p.relative_to(RT).as_posix() if p.is_relative_to(RT) else None
  if rel in pins and blob!=pins[rel]['git_blob_sha1']:os._exit(91)
  rows.append(dict(module=name,file=clean(p),git_blob_sha1=blob,sha256=hashlib.sha256(raw).hexdigest(),pinned_original=rel in pins))
 out=RET/'repro/import_audits';out.mkdir(exist_ok=True)
 (out/(os.environ['BL3_SUITE']+'_'+str(os.getpid())+'.json')).write_text(json.dumps(dict(argv=[clean(a) for a in sys.argv],modules=rows,blocked_network_events=blocked,external_dispatches=0),indent=2)+'\n')
atexit.register(finish)
