from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent
expected={'author_full':(90,0),'hostile':(37,26),'record_custody':(3,3),'positive_edges':(6,0)}
rows=[]
for name,(n,fail) in expected.items():
 cases=list(ET.parse(R/'evidence'/(name+'.xml')).iter('testcase'))
 results=[dict(name=c.get('name'),classname=c.get('classname'),status='ERROR' if c.find('error') is not None else 'RED' if c.find('failure') is not None else 'SKIP' if c.find('skipped') is not None else 'PASS') for c in cases]
 counts={s:sum(c['status']==s for c in results) for s in ['PASS','RED','ERROR','SKIP']}
 assert len(cases)==n and counts['RED']==fail and counts['ERROR']==counts['SKIP']==0,(name,counts)
 rows.append(dict(suite=name,junit='evidence/'+name+'.xml',counts=counts,cases=results))
faults=json.loads((R/'evidence/fault_trials.json').read_text());assert len(faults)==13
for f in faults:
 assert f['grade']=='SAME_ASSERTION_RED_RESTORED'
 assert f['before_sha256']==f['restored_sha256']
 assert f['negative']['failure'] and not f['negative']['error'] and not f['negative']['skipped']
 assert f['positive']['exit']==f['restored']['exit']==0
for name,n in [('author_severance',6),('author_consumer',2),('reviewer',5)]:
 receipt=json.loads((R/'evidence'/('shared_'+name+'.json')).read_text());assert len(receipt['claims'])==n
(R/'evidence/court_summary.json').write_text(json.dumps(dict(verdict='REVISE__NATIVE_HOLD',suites=rows,fault_triplets=13,original_shared_claims=8,reviewer_shared_claims=5,native_positive='NOT_PROVED',scientific_mechanism='NOT_PROVED',C12='NOT_RUN__LOCAL_ONLY_NO_TERMINAL_PERSON_DELTA'),indent=2)+'\n')
# This is a final custody manifest, not a claim that all test hashes were timestamped before first execution.
files=[p for p in sorted((R/'review').iterdir()) if p.is_file()]
(R/'custody/reviewer_final_preimages.json').write_text(json.dumps([dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files],indent=2)+'\n')
print('Court receipts checked: 90 original PASS; 11P/26R hostile; 3R record; 6P edges; 13 restored fault triplets; 13 shared witnesses')
