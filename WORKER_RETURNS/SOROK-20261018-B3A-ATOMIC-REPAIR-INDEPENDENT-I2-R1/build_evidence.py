"""Derive review tables from actual outputs; sanitize only new execution receipts."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET,sqlite3,re,subprocess
ROOT=Path(__file__).resolve().parent;E=ROOT/'evidence';RUN=ROOT/'.scratch/b3a'
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def suite(p):
 t=ET.parse(p).getroot()
 return {**{k:sum(int(x.get(k,'0')) for x in t.iter('testsuite')) for k in ('tests','failures','errors','skipped')},'failed_tests':[x.get('name') for x in t.iter('testcase') if x.find('failure') is not None],'claim':'EXECUTED_BY_THIS_REVIEWER'}
def main():
 summary={str(p.relative_to(E)):suite(p) for p in E.rglob('*.xml')}
 dump(E/'suite_results.json',summary)
 fixed=set(summary['original_x3.xml']['failed_tests'])-set(summary['candidate_x3.xml']['failed_tests'])
 new=set(summary['candidate_x3.xml']['failed_tests'])-set(summary['original_x3.xml']['failed_tests'])
 assert len(fixed)==5 and len(new)==1
 matrix={}
 for family in ('original_x3_sql','candidate_x3_sql'):
  matrix[family]={}
  for p in (E/family).glob('*.json'):
   x=json.loads(p.read_text());matrix[family][p.stem]={'result_status':x['result'].get('status'),'result_code':x['result'].get('code'),'no_mutation':x['result'].get('no_mutation'),'tables':{n:{'before':len(rows),'after':len(x['after'][n]),'unchanged':rows==x['after'][n]} for n,rows in x['before'].items()}}
 for family in ('original_seeded_sql','candidate_seeded_sql','reviewer_sql'):
  matrix[family]={}
  for p in (E/family).glob('*.json'):
   x=json.loads(p.read_text());before=x['before'];after=x['after'];matrix[family][p.stem]={'schema_unchanged':before['schema']==after['schema'],'tables':{n:{'before':len(rows),'after':len(after['tables'][n]),'unchanged':rows==after['tables'][n]} for n,rows in before['tables'].items()},'result_status':x.get('result',{}).get('status'),'result_code':x.get('result',{}).get('code'),'no_mutation':x.get('result',{}).get('no_mutation')}
 dump(E/'table_case_matrix.json',matrix);dump(E/'x3_adjudication.json',{'fixed_five_test_identities':sorted(fixed),'persistent_three':sorted(set(summary['original_x3.xml']['failed_tests'])&set(summary['candidate_x3.xml']['failed_tests'])),'new_obsolete_expectation':sorted(new)})
 sql={}
 for version,base in [('original',RUN/'frozen_b3'),('candidate',RUN/'candidate')]:
  for label in ('positive','permission_absent'):
   for suffix in ('','_cold'):
    p=base/'evidence/loop'/(label+suffix+'.sqlite');db=sqlite3.connect(p);assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    tables={n:db.execute('SELECT * FROM "'+n+'" ORDER BY 1').fetchall() for n, in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")};db.close()
    sql[version+'/'+label+suffix]={'integrity':'ok','tables':tables,'snapshot_sha256':sha(json.dumps(tables,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())}
   assert sql[version+'/'+label]['snapshot_sha256']==sql[version+'/'+label+'_cold']['snapshot_sha256']
 dump(E/'sql_cold_audit.json',sql)
 kills=[]
 for p in sorted((E/'reviewer_sql').glob('kill_*.json')):
  x=json.loads(p.read_text());assert x['exit']==-9 and x['ready']['pid']!=x['after']['pid'];kills.append({'case':p.stem,'ready_pid':x['ready']['pid'],'inspector_pid':x['after']['pid'],'exit':x['exit'],'stage':x['ready']['stage'],'tables_unchanged':x['before']['tables']==x['after']['tables'],'schema_unchanged':x['before']['schema']==x['after']['schema']})
 assert len(kills)==10
 dump(E/'process_death_summary.json',{'new_reviewer_process_kills':kills,'power_loss_durability_tested':False,'author_atomic_kills_are_separate':12})
 # Source/input trees remain byte-identical; portability transformation is new receipt-only.
 repo=ROOT.parents[1]
 def portable(s):
  s=s.replace(str(repo),'<REVIEW_WORKTREE>').replace(str(Path.home()),'<HOME>')
  s=re.sub(r'/(?:private/)?var/folders/[^\s\'\"<>]*','<TEMP>',s)
  s=re.sub(r'/tmp/b3-atomic-[^/\s\'\"<>]+','<B3_SCRATCH>',s)
  return s
 for p in list(E.rglob('*'))+[ROOT/'first_hostile.log']:
  if not p.is_file() or p.suffix not in ('.log','.json','.xml'):continue
  raw=p.read_text()
  if p.suffix=='.xml':
   t=ET.fromstring(raw)
   for node in t.iter():
    if 'hostname' in node.attrib:node.set('hostname','local-host')
    for k,v in list(node.attrib.items()):node.set(k,portable(v))
    if node.text:node.text=portable(node.text)
    if node.tail:node.tail=portable(node.tail)
   p.write_text(ET.tostring(t,encoding='unicode')+'\n')
  else:p.write_text(portable(raw))
 print('Derived and sanitized evidence; fixed X3 identities:',len(fixed),'new kills:',len(kills))
if __name__=='__main__':main()
