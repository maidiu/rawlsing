"""Bounded native import closure from direct-checked live canonical, no owner edits."""
from pathlib import Path
import subprocess,ast,json,hashlib
RET=Path(__file__).resolve().parents[1];ROOT=RET/'runtime_root/source';PIN='0d551d36ff19dc9806e0ad490ff33a1e4c25e381'
paths=set(subprocess.check_output(['git','ls-tree','-r','--name-only',PIN,'rawlsing_next']).decode().splitlines())
overrides={p:'0e0ed50dbce2dd1434d3a3c84b937b9a956adba9' for p in ['rawlsing_next/pre553_n9_n10w_progressive_candidate.py','rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py']}
# Newer N9C is an isolated test reader, not adopted/operative; retain exact source
# for clock/permission contract comparison and regression, never import its real
# documentary numeric fixtures into E04 sourcefree world production.
overrides.update({p:'9ab4a0192b7c951bb0b387637e6c74333246766c' for p in ['rawlsing_next/pre553_hq297_n9c_two_field_reader.py','tests/test_hq297_n9c_two_field_reader.py']})
paths|=set(overrides)
TESTS=['test_pre553_analytical_composition','test_pre553_analytical_composition_higher_order','test_pre553_empirical_possibility_provider','test_pre553_empirical_query','test_source_backed_positioned_subject_possibility','test_m4_v557_v558_publication_repository','test_m5_runtime_rsc_peer_prior']
queue=[*overrides,'rawlsing_next/objective_consumer_bounded_evidence.py',*['rawlsing_next/tests/'+n+'.py' for n in TESTS]];seen=set();manifest=[]
def add_module(name):
 p=name.replace('.','/')
 for candidate in [p+'.py',p+'/__init__.py']:
  if candidate in paths:queue.append(candidate)
while queue:
 path=queue.pop()
 if path in seen:continue
 seen.add(path);commit=overrides.get(path,PIN);raw=subprocess.check_output(['git','show',commit+':'+path]);dest=ROOT/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
 manifest.append(dict(commit=commit,path=path,local=str(dest.relative_to(RET)),blob_sha1=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),sha256=hashlib.sha256(raw).hexdigest()))
 tree=ast.parse(raw)
 for node in ast.walk(tree):
  if isinstance(node,ast.Import):
   for a in node.names:
    if a.name.startswith('rawlsing_next'):add_module(a.name)
  if isinstance(node,ast.ImportFrom):
   module=node.module or ''
   if node.level:
    parent=path.rsplit('/',1)[0].split('/');module='.'.join(parent[:len(parent)-node.level+1]+([module] if module else []))
   if module.startswith('rawlsing_next'):
    add_module(module)
    for a in node.names:add_module(module+'.'+a.name)
 for parent in dest.relative_to(ROOT).parents:
  init=str(parent/'__init__.py')
  if init in paths:queue.append(init)
(RET/'source_manifest.json').write_text(json.dumps(sorted(manifest,key=lambda r:r['path']),indent=2)+'\n')
print('Staged exact bounded native closure:',len(manifest),'files')
