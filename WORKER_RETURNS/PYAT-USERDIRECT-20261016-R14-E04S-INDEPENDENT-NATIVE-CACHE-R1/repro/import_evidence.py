import pathlib,subprocess,hashlib,json
R=pathlib.Path(__file__).resolve().parents[1];REPO=R.parents[1]
pins=[('E04R','97254d0b215b5dd45580dd94608a8ec95ff8b76f','PYAT-USERDIRECT-20261015-R13-E04R-NATIVE-CACHE-INTEGRITY-REPAIR-R1'),('E04N','644a68b76042309be71f0eb65fabc4a6903f15b8','PYAT-USERDIRECT-20261015-R12-E04N-FULL-NATIVE-INDEPENDENT-R1'),('E04','9c96f201f3530d2dae321201e9a913bb7a61800f','PYAT-USERDIRECT-20261015-R10-E04-GENERIC-WORLD-POSSIBILITY-SERVICE-R1'),('E04I','54013488a181f25db7b10ef5220afc48d320fa37','PYAT-USERDIRECT-20261015-R11-E04I-INDEPENDENT-GENERIC-WORLD-SERVICE-R1')]
m=[]
for label,commit,name in pins:
 prefix='WORKER_RETURNS/'+name+'/'
 paths=subprocess.check_output(['git','-c','gc.auto=0','ls-tree','-r','--name-only',commit,prefix],cwd=REPO).decode().splitlines()
 if not paths:
  # Discover exact immutable return name if historical capitalization differs.
  candidates=subprocess.check_output(['git','-c','gc.auto=0','ls-tree','--name-only',commit+':WORKER_RETURNS'],cwd=REPO).decode().splitlines()
  names=[x for x in candidates if '-E04I-' in x]
  assert label=='E04I' and len(names)==1,names
  prefix='WORKER_RETURNS/'+names[0]+'/'
  paths=subprocess.check_output(['git','-c','gc.auto=0','ls-tree','-r','--name-only',commit,prefix],cwd=REPO).decode().splitlines()
 for p in paths:
  b=subprocess.check_output(['git','-c','gc.auto=0','show',commit+':'+p],cwd=REPO);blob=subprocess.check_output(['git','-c','gc.auto=0','rev-parse',commit+':'+p],cwd=REPO).decode().strip()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
  d=R/'inputs'/label/p[len(prefix):];d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(b)
  m.append(dict(commit=commit,path=p,local=str(d.relative_to(R)),git_blob=blob,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)))
(R/'input_manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('Exact imported evidence objects',len(m))
