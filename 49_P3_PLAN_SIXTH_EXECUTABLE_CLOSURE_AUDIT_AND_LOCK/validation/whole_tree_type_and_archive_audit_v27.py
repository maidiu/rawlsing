from __future__ import annotations
from pathlib import Path
import argparse, ast, csv, hashlib, io, json, zipfile
from collections import Counter
try:
 import yaml
except Exception: yaml=None

def audit(root:Path):
    csv.field_size_limit(2**31-1)
    errors=[];counts=Counter();archive_instances=0;unique_payloads=set();cache_paths=[]
    def walk_zip(data:bytes,label:str):
        nonlocal archive_instances
        h=hashlib.sha256(data).hexdigest()
        if h in unique_payloads:return
        unique_payloads.add(h)
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                bad=z.testzip()
                if bad:errors.append({'file':label,'error':'bad ZIP member '+bad});return
                for n in z.namelist():
                    if n.lower().endswith('.zip'):
                        archive_instances+=1;walk_zip(z.read(n),label+'!'+n)
        except Exception as e:errors.append({'file':label,'error':repr(e)})
    files=sorted(p for p in root.rglob('*') if p.is_file())
    for p in files:
        rel=p.relative_to(root).as_posix();ext=p.suffix.lower() or '[no_extension]';counts[ext]+=1
        if '__pycache__' in p.parts or '.pytest_cache' in p.parts or p.suffix=='.pyc':cache_paths.append(rel)
        try:
            if ext=='.json':json.loads(p.read_text(encoding='utf-8'))
            elif ext=='.csv':list(csv.reader(p.open(encoding='utf-8',newline='')))
            elif ext in {'.yaml','.yml'}:
                if yaml is None:raise RuntimeError('PyYAML unavailable')
                yaml.safe_load(p.read_text(encoding='utf-8'))
            elif ext=='.py':ast.parse(p.read_text(encoding='utf-8'))
            elif ext in {'.md','.txt','.sql'}:p.read_text(encoding='utf-8')
            elif ext=='.docx':
                with zipfile.ZipFile(p) as z:
                    bad=z.testzip()
                    if bad:raise ValueError('bad DOCX member '+bad)
                    if '[Content_Types].xml' not in z.namelist():raise ValueError('DOCX missing [Content_Types].xml')
            elif ext=='.zip':
                archive_instances+=1
                with zipfile.ZipFile(p) as z:
                    bad=z.testzip()
                    if bad:raise ValueError('bad ZIP member '+bad)
        except Exception as e:errors.append({'file':rel,'error':repr(e)})
    for p in sorted(root.rglob('*.zip')):walk_zip(p.read_bytes(),p.relative_to(root).as_posix())
    if cache_paths:errors.append({'file':'CACHE_DEBRIS','error':cache_paths[:20]})
    return {'status':'PASS' if not errors else 'FAIL','handoff_version':'v27','root_name':root.name,'files':len(files),
            'type_counts':dict(sorted(counts.items())),'recursive_archive_instances':archive_instances,
            'unique_archive_payloads':len(unique_payloads),'cache_or_bytecode_debris':len(cache_paths),'errors':errors}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--output');a=ap.parse_args();res=audit(Path(a.root).resolve())
    text=json.dumps(res,indent=2)+'\n';print(text,end='')
    if a.output:Path(a.output).write_text(text,encoding='utf-8')
    raise SystemExit(0 if res['status']=='PASS' else 1)
if __name__=='__main__':main()
