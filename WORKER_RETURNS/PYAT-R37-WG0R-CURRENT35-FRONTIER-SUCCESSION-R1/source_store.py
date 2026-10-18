"""Exact Git source custody inside the user-directed WG0R return only."""
import ast,hashlib,json,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parent
WT=ROOT.parent.parent
BASE='68873526efe5a39a0849aa401666ac997870f156'

def git(*args):return subprocess.check_output(['git','-C',str(WT),*args])
def tree(ref,prefix=''):
    args=['ls-tree','-r',ref]+(['--',prefix] if prefix else [])
    return {line.split(b'\t',1)[1].decode():line.split()[2].decode() for line in git(*args).splitlines()}
def prefetch(blobs):
    if blobs:
        subprocess.run(['git','-C',str(WT),'-c','gc.auto=0','fetch','--no-tags','--no-write-fetch-head','origin','--stdin'],input='\n'.join(sorted(set(blobs)))+'\n',text=True,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def save(ref,paths,label):
    allpaths=tree(ref);selected={p:allpaths[p] for p in paths}
    prefetch(selected.values());rows=[]
    for path,blob in selected.items():
        data=git('cat-file','blob',blob)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
        dest=ROOT/'sources'/label/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        rows.append(dict(commit=ref,path=path,blob_sha1=blob,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),local_path=str(dest.relative_to(ROOT))))
    evidence=ROOT/'evidence';evidence.mkdir(exist_ok=True)
    manifest=evidence/'source_manifest.json';old=json.loads(manifest.read_text()) if manifest.exists() else []
    combined={r['local_path']:r for r in old+rows};manifest.write_text(json.dumps(list(combined.values()),indent=2)+'\n')
    return rows

def closure(ref,seeds,label):
    files=tree(ref);pending=set(seeds);seen=set();rows=[]
    while pending:
        paths=sorted(pending-seen);pending=set()
        if not paths:break
        rows+=save(ref,paths,label);seen.update(paths)
        for path in paths:
            data=(ROOT/'sources'/label/path).read_text()
            for node in ast.walk(ast.parse(data)):
                mods=[]
                if isinstance(node,ast.Import):mods=[a.name for a in node.names]
                elif isinstance(node,ast.ImportFrom):
                    module=node.module or ''
                    if node.level:
                        parent=path.rsplit('/',1)[0].split('/')
                        module='.'.join(parent[:len(parent)-node.level+1]+([module] if module else []))
                    mods=[module]+[module+'.'+a.name for a in node.names]
                for mod in mods:
                    if not mod.startswith('rawlsing_next'):continue
                    base=mod.replace('.','/')
                    candidates=[base+'.py',base+'/__init__.py']
                    for candidate in candidates:
                        if candidate in files and candidate not in seen:pending.add(candidate)
        if 'rawlsing_next/__init__.py' in files and 'rawlsing_next/__init__.py' not in seen:pending.add('rawlsing_next/__init__.py')
    return rows
