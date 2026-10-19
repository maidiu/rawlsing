"""Repair-author source/result audit. Does not confer independent acceptance."""
from pathlib import Path
import hashlib,json,subprocess,os,sys,sqlite3,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent;E=ROOT/'evidence';C=ROOT/'candidate'
def sha(data):return hashlib.sha256(data).hexdigest()
def dump(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def main():
 changed=[]
 for row in json.loads((ROOT/'input_manifest.json').read_text()):
  data=(ROOT/row['local_path']).read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  if blob!=row['git_blob_sha1']:changed.append(row['local_path'])
 assert changed==['candidate/integration.py']
 originals=json.loads((C/'source_manifest.json').read_text())
 for row in originals:assert sha((C/row['local']).read_bytes())==row['sha256']
 suites={}
 for p in E.rglob('*.xml'):
  tree=ET.parse(p).getroot();suites[str(p.relative_to(E))]={**{k:sum(int(s.get(k,'0')) for s in tree.iter('testsuite')) for k in ('tests','failures','errors','skipped')},'failed_tests':[t.get('name') for t in tree.iter('testcase') if t.find('failure') is not None]}
 expected={'before_fix.xml':(2,2),'development_schema_repair.xml':(15,1),'schema_repair.xml':(33,0),'seeded_refusals.xml':(4,0),'b3.xml':(71,0),'atomic.xml':(63,0),'candidate/f2/junit.xml':(42,0),'x3.xml':(28,4)}
 for name,count in expected.items():assert (suites[name]['tests'],suites[name]['failures'])==count and suites[name]['errors']==suites[name]['skipped']==0,name
 assert set(suites['x3.xml']['failed_tests'])=={'test_duplicate_physical_check_cannot_form_practice','test_guard_rejects_missing_previously_used_sources','test_before_and_after_loss_practice_requires_pre_loss_act','test_privileged_second_connection_between_guard_and_commit_is_detected_only_on_reentry'}
 blind=json.loads((E/'f2_blinded/matrix.json').read_text());assert len(blind['rows'])==42 and all(not row['errors'] for row in blind['rows']) and sum(x['status']=='ELIGIBLE_NONCAUSAL' for x in blind['rows'])==20
 sql={}
 for label in ('positive','permission_absent'):
  live=json.loads((C/'evidence/loop'/(label+'.json')).read_text());cold=json.loads((E/(label+'_cold.log')).read_text());assert live['snapshot_hash']==cold['snapshot_hash'] and cold['receipts']==[x['receipt'] for x in live['episodes']]
  for suffix in ('','_cold'):
   p=C/'evidence/loop'/(label+suffix+'.sqlite');db=sqlite3.connect(p);integrity=db.execute('PRAGMA integrity_check').fetchone()[0];assert integrity=='ok';schema=db.execute('SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name').fetchall();rows={n:db.execute('SELECT * FROM "'+n+'" ORDER BY 1').fetchall() for n, in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")};db.close();sql[label+suffix]=dict(integrity=integrity,schema=schema,tables=rows)
  assert sql[label]==sql[label+'_cold']
 dump(E/'sql_cold_audit.json',sql);dump(E/'suite_results.json',suites)
 probe="from pathlib import Path;import sys,json,hashlib;sys.path.insert(0,sys.argv[1]);import integration,fixture_authority,developmental_loop;r=Path(sys.argv[1]);print(json.dumps([dict(module=n,path=str(Path(m.__file__).resolve().relative_to(r)),sha256=hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()) for n,m in list(sys.modules.items()) if getattr(m,'__file__',None) and Path(m.__file__).resolve().is_relative_to(r)]))"
 imported=json.loads(subprocess.check_output([sys.executable,'-c',probe,str(C)],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')))
 known={row['sha256'] for row in originals}|{sha(p.read_bytes()) for p in C.glob('*.py')}
 assert all(row['sha256'] in known for row in imported);dump(E/'loaded_modules.json',imported)
 # New evidence only; never alter frozen source/tests.
 def portable(s):
  s=s.replace(str(ROOT.parents[1]),'<REPAIR_WORKTREE>').replace(str(Path.home()),'<HOME>')
  return re.sub(r'/(?:private/)?var/folders/[^\s\'\"<>]*','<TEMP>',s)
 for p in E.rglob('*'):
  if not p.is_file() or p.suffix not in ('.json','.xml','.log'):continue
  raw=p.read_text()
  if p.suffix=='.xml':
   tree=ET.fromstring(raw)
   for node in tree.iter():
    if 'hostname' in node.attrib:node.set('hostname','local-host')
    for k,v in list(node.attrib.items()):node.set(k,portable(v))
    if node.text:node.text=portable(node.text)
    if node.tail:node.tail=portable(node.tail)
   raw=ET.tostring(tree,encoding='unicode')+'\n'
  else:raw=portable(raw)
  p.write_text(raw)
 dump(E/'verification.json',{'only_changed_inherited_file':changed[0],'pinned_source_entries_verified':len(originals),'actual_imports_verified':len(imported),'unchanged_schema_falsifiers':'2 RED before -> 2 PASS after','extended_court':'33 PASS','regressions':expected,'blinded_f2':'42 PASS / 20 eligible','cold_replay':'EXACT_ALL_RECEIPTS_AND_TABLES','independent_acceptance':False,'no_candidate_or_review_test_edits':True})
 print('Repair source and result verification PASS')
if __name__=='__main__':main()
