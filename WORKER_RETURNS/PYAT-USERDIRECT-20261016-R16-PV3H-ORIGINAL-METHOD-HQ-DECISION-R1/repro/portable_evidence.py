"""Publish diagnostics with relative aliases, preserving scientific data/journals."""
import pathlib,hashlib,json,re
R=pathlib.Path(__file__).resolve().parents[1];rows=[]
for p in sorted((R/'evidence').rglob('*')):
 if not p.is_file() or 'native_journals' in p.parts:continue
 b=p.read_bytes()
 try:s=b.decode()
 except UnicodeDecodeError:continue
 t=s.replace(str(R),'<RETURN>').replace(str(pathlib.Path.home()),'<LOCAL_HOME>')
 if p.suffix=='.xml':t=re.sub(r' hostname="[^"]*"','',t)
 if t!=s:
  raw=R/'runtime/raw_portability'/p.relative_to(R);raw.parent.mkdir(parents=True,exist_ok=True);raw.write_bytes(b);p.write_text(t)
  rows.append(dict(path=str(p.relative_to(R)),raw_sha256=hashlib.sha256(b).hexdigest(),published_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(R/'portability_receipt.json').write_text(json.dumps(dict(scope='Only diagnostic own-return/home path aliases and JUnit hostname removal; native scientific refs/values and original journals unchanged; raw diagnostics retained under ignored runtime',files=rows),indent=2)+'\n')
print('Sanitized diagnostic artifacts',len(rows))
