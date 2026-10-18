"""Replay frozen E2 at exact R1 and at the bounded candidate; keep all oracle failures."""
from pathlib import Path
import hashlib, json, os, re, shutil, subprocess, sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
R1='358fd1086eac0a4aa7791ca14abc25c45b935ddd'
E2='8983315b3aee130e9446d43bd983c4a91c6f0437'
B2_PATH='WORKER_RETURNS/SOROK-V2-HQ325-B2-FOUR_RETURN_INTEGRATION-R1'
R1_PATH='WORKER_RETURNS/SOROK-V2-HQ327-R1-EVENT-IDENTITY-REPAIR-R1'
E2_PATH='WORKER_RETURNS/SOROK-V2-HQ328-E2-R1-INDEPENDENT-CUSTODY-R1'

def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')

def main(phase):
    assert phase in ('before','after')
    stage=ROOT/'.runtime'/phase;stage.mkdir(parents=True,exist_ok=True)
    out=ROOT/'evidence'/phase;out.mkdir(parents=True,exist_ok=True)
    for path in git('ls-tree','-r','--name-only',R1,B2_PATH).decode().splitlines():
        target=stage/Path(path).relative_to(B2_PATH);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(git('show',R1+':'+path))
    if phase=='after':shutil.copyfile(REPO/B2_PATH/'bridge.py',stage/'bridge.py')
    tests=ROOT/'.runtime'/('tests_'+phase);tests.mkdir(exist_ok=True)
    test_sources=[]
    for commit,prefix,label in [(E2,E2_PATH,'E2'),(R1,R1_PATH,'R1')]:
        dest=tests/label;dest.mkdir(exist_ok=True)
        for path in git('ls-tree','-r','--name-only',commit,prefix).decode().splitlines():
            if not path.endswith('.py'):continue
            target=dest/Path(path).relative_to(prefix);target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(git('show',commit+':'+path))
            test_sources.append(dict(commit=commit,path=path,git_blob_sha1=git('rev-parse',commit+':'+path).decode().strip(),sha256=digest(target)))
    env=dict(os.environ,GIT_DIR=git('rev-parse','--path-format=absolute','--git-common-dir').decode().strip(),B2_REVIEW_ROOT=str(stage),E2_EVIDENCE=str(out/'e2_sql'),R1_EVIDENCE=str(out/'r1_sql'),REPAIR_EVIDENCE=str(out/'regression_sql'),PYTHONDONTWRITEBYTECODE='1')
    for label in ('e2_sql','r1_sql','regression_sql'):(out/label).mkdir(exist_ok=True)
    commands=[]
    def portable(s):
        s=s.replace(str(ROOT),'<REPAIR_RETURN>').replace(str(Path.home()),'<HOME>')
        return re.sub(r'/(?:private/)?var/folders/[^\s\'\"<>]*','<TEMP>',s)
    def run(args,name,expected=0):
        p=subprocess.run(args,cwd=stage,env=env,text=True,capture_output=True)
        (out/(name+'.log')).write_text(portable(p.stdout+p.stderr))
        commands.append(dict(command=[portable(str(a)) for a in args],cwd='<B2_STAGE>',environment=dict(B2_REVIEW_ROOT='<B2_STAGE>',GIT_DIR='<SHARED_OBJECT_STORE>'),exit=p.returncode,expected_exit=expected))
        dump(out/'commands.json',commands)
        assert p.returncode==expected,(name,p.returncode,p.stdout[-1000:],p.stderr[-1000:])
    def pytest(source,name,expected=0,extra=()):
        run([sys.executable,'-m','pytest','-q',str(source),*extra,'--junitxml='+str(out/(name+'.xml'))],name,expected)
    run([sys.executable,'materialize.py'],'materialize')
    pytest(tests/'E2/test_e2.py','e2_strict',1 if phase=='before' else 0,('-k','legacy_after_mapping_must_fail_closed_at_b2_reentry'))
    if phase=='after':
        run([sys.executable,'run_courts.py'],'inherited')
        shutil.copytree(stage/'evidence',out/'inherited',dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.sqlite','*.sqlite-*'))
        shutil.copyfile(stage/'execution_receipt.json',out/'execution_receipt.json')
        pytest(tests/'R1/test_identity.py','r1')
        pytest(tests/'E2/test_e2.py','e2_full',1)
        suite=ET.parse(out/'e2_full.xml').find('testsuite')
        failures=[c.get('name') for c in suite.findall('testcase') if c.find('failure') is not None]
        assert failures==['test_direct_b1_after_wrapper_limit_is_measured[False]','test_direct_b1_after_wrapper_limit_is_measured[True]']
        pytest(tests/'R1/frozen/test_hostile_x2.py','x2',1)
        suite=ET.parse(out/'x2.xml').find('testsuite')
        assert [c.get('name') for c in suite.findall('testcase') if c.find('failure') is not None]==['test_same_event_id_accepts_distinct_objective_payload_hashes']
        pytest(ROOT/'test_regression.py','regression')
        run([sys.executable,str(tests/'E2/runtime_probe.py'),str(out/'runtime.json')],'runtime')
    imports=json.loads((stage/'imported_sources.json').read_text());assert len(imports)==69
    for row in imports:
        assert digest(stage/row['materialized_path'])==row['sha256']
        if 'git_blob_sha1' in row:
            assert git('cat-file','blob',row['git_blob_sha1'])==(stage/row['materialized_path']).read_bytes()
    dump(out/'source_provenance.json',dict(bridge_sha256=digest(stage/'bridge.py'),frozen_tests=test_sources,inherited=imports,regression_source_sha256=digest(ROOT/'test_regression.py')))
    # Portable evidence copies only: frozen/source code is never transformed.
    for p in out.rglob('*'):
        if not p.is_file():continue
        if p.suffix=='.xml':
            tree=ET.parse(p)
            for node in tree.iter():
                node.attrib.pop('hostname',None)
                for k,v in node.attrib.items():node.set(k,portable(v))
                if node.text:node.text=portable(node.text)
                if node.tail:node.tail=portable(node.tail)
            tree.write(p,encoding='utf-8',xml_declaration=True)
        elif p.suffix in ('.json','.log'):p.write_text(portable(p.read_text()))
    print(phase+' verification complete',flush=True)

if __name__=='__main__':main(sys.argv[1])
