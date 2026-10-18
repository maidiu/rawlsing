import hashlib,json,subprocess,sys,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parent;REPO=R.parents[1]
OUT=R/'03_REAL_FROZEN_ALL_COURTS_AND_COLD_JUNIT'
C=R/'stage/WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1/court'
sel=json.loads((C/'source_selector.json').read_text())
verified=[]
for row in sel['files']:
    b=(C/'runtime_root'/row['staged_path']).read_bytes()
    sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    assert sha1==row['git_blob_sha1']
    assert hashlib.sha256(b).hexdigest()==row['sha256'] and len(b)==row['bytes']
    p=subprocess.run(['git','show',row['commit']+':'+row['source_path']],cwd=REPO,capture_output=True)
    assert p.returncode==0, (row,p.stderr)
    assert p.stdout==b,row
    verified.append(dict(row,verified_against_original_git_bytes=True))
cold=[json.loads((OUT/f'gf1h_cold_{i}.log').read_text()) for i in (0,1)]
a,b=[dict(v) for v in cold]
assert a.pop('pid')!=b.pop('pid')
assert a==b
for receipt in cold:
    for row in receipt['custody']['imports']:
        path=C.parent/row['file'];src=path.read_bytes()
        assert hashlib.sha256(src).hexdigest()==row['sha256']
        assert hashlib.sha1(b'blob '+str(len(src)).encode()+b'\0'+src).hexdigest()==row['blob_sha1']
obj=dict(stage='GF1H predecessor full native independent replay; GF1K not returned',native_files=verified,native_file_count=len(verified),python_file_count=sum(v['staged_path'].endswith('.py') for v in verified),cold_processes=cold,distinct_pid=True,identical_non_pid_receipts=True,scope='SOURCEFREE TEST_ONLY; structural self-rehash does not authenticate original issuer; no adoption',GF1G_original_phase_a_full_sha='ecd975ad5b424f952ac248dfcf1b7a83aa867a6a')
(R/'02_EXACT_NATIVE_SOURCE_IMPORTS_AND_ISSUER_SCOPE.json').write_text(json.dumps(obj,indent=2)+'\n')
summary=[]
for xml in sorted(OUT.glob('*.xml')):
    root=ET.parse(xml).getroot(); suites=[root] if root.tag=='testsuite' else list(root.findall('testsuite'))
    counts={k:sum(int(s.attrib.get(k,0)) for s in suites) for k in ('tests','failures','errors','skipped')}
    failures=[dict(node=t.attrib.get('name'),class_name=t.attrib.get('classname'),kind='failure' if t.find('failure') is not None else 'error') for t in root.iter('testcase') if t.find('failure') is not None or t.find('error') is not None]
    summary.append(dict(court=xml.stem,**counts,failures_by_node=failures,sha256=hashlib.sha256(xml.read_bytes()).hexdigest()))
(R/'court_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(dict(native_files=len(verified),python_files=obj['python_file_count'],cold_pids=[c['pid'] for c in cold],courts=[{k:v for k,v in s.items() if k not in ('failures_by_node','sha256')} for s in summary]),indent=2))
