import subprocess,pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
pins=[('e05i','a56f5c9c3d13081677586510a83351bcdeda2d3c','PYAT-USERDIRECT-20261015-R12-E05I-INDEPENDENT-WORLD-ADAPTER-R1'),('e04n','644a68b76042309be71f0eb65fabc4a6903f15b8','PYAT-USERDIRECT-20261015-R12-E04N-FULL-NATIVE-INDEPENDENT-R1'),('e05','257dfaf41be7d2a88c11741851e9dc89363b5386','PYAT-USERDIRECT-20261015-R11-E05-SELECTED-WORLD-INSTALLATION-R1')]
manifest=[]
for label,commit,name in pins:
 prefix='WORKER_RETURNS/'+name+'/'
 for p in subprocess.check_output(['git','ls-tree','--full-tree','-r','--name-only',commit,prefix],cwd=R).decode().splitlines():
  b=subprocess.check_output(['git','show',commit+':'+p],cwd=R);blob=subprocess.check_output(['git','rev-parse',commit+':'+p],cwd=R).decode().strip()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
  d=R/'inputs'/label/p[len(prefix):];d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(b)
  manifest.append(dict(commit=commit,path=p,local=str(d.relative_to(R)),git_blob=blob,sha256=hashlib.sha256(b).hexdigest()))
(R/'input_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Imported',len(manifest),'exact evidence objects')
