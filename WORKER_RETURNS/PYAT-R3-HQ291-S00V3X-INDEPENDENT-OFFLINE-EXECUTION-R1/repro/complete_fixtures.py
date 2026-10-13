"""Add exact I01R fixture imports omitted by first assembly; no test executions."""
import ast,hashlib,json,pathlib,subprocess
OUT=pathlib.Path(__file__).resolve().parent;C=OUT/'composite';I='473b7997d1b446c54a2d8688f94053b6c8670881';rows=json.loads((OUT/'source_manifest.json').read_text());known={r['path'] for r in rows}
queue=['rawlsing_next/tests/c1_at08_at13_fixture.py','rawlsing_next/tests/test_pre553_empirical_query.py','rawlsing_next/tests/test_pre553_route_b_production.py']
while queue:
 p=queue.pop()
 if p in known:continue
 raw=subprocess.check_output(['git','show',I+':'+p]);target=C/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);known.add(p)
 rows.append(dict(path=p,origin_commit=I,origin_path=p,git_blob=subprocess.check_output(['git','rev-parse',I+':'+p]).decode().strip(),sha256=hashlib.sha256(raw).hexdigest()))
 for node in ast.walk(ast.parse(raw)):
  modules=[]
  if isinstance(node,ast.Import):modules=[a.name for a in node.names]
  if isinstance(node,ast.ImportFrom) and node.module:
   modules=[node.module] if node.module!='rawlsing_next.tests' else [node.module+'.'+a.name for a in node.names]
  for module in modules:
   if module.startswith('rawlsing_next.tests.'):queue.append(module.replace('.','/')+'.py')
(OUT/'source_manifest.json').write_text(json.dumps(rows,indent=2)+'\n');print('fixture closure complete',len(rows))
