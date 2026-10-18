"""Fresh exact-parent baseline and candidate courts. No historical evidence overwritten."""
from pathlib import Path
import hashlib, json, os, re, shutil, subprocess, sys, tempfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
B2='WORKER_RETURNS/SOROK-V2-HQ325-B2-FOUR_RETURN_INTEGRATION-R1'
BASE='950ecf0b3816ea7d0dd3ab48b62c92cedfe0e883'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def main(phase):
    out=ROOT/'evidence'/phase;out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='r1-court-') as temp:
        stage=Path(temp)/'B2';stage.mkdir()
        for path in git('ls-tree','-r','--name-only',BASE,B2).decode().splitlines():
            dest=stage/Path(path).relative_to(B2);dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(git('show',BASE+':'+path))
        if phase=='after':shutil.copyfile(REPO/B2/'bridge.py',stage/'bridge.py')
        env=dict(os.environ,GIT_DIR=git('rev-parse','--path-format=absolute','--git-common-dir').decode().strip(),B2_REVIEW_ROOT=str(stage))
        concurrent=out/'concurrency';concurrent.mkdir(exist_ok=True)
        env['R1_EVIDENCE']=str(concurrent)
        commands=[]
        def run(args,label,expected=0):
            p=subprocess.run(args,cwd=stage,env=env,capture_output=True,text=True)
            portable=lambda s:s.replace(str(stage),'<B2>').replace(str(ROOT),'<R1>').replace(str(Path.home()),'<HOME>')
            (out/(label+'.log')).write_text(portable(p.stdout+p.stderr))
            commands.append(dict(command=args,label=label,exit=p.returncode,expected=expected))
            if p.returncode!=expected:
                shutil.copytree(stage/'evidence',out/'failed_b2',dirs_exist_ok=True)
                raise AssertionError(commands[-1])
        run([sys.executable,'run_courts.py'],'all_courts')
        run([sys.executable,str(ROOT/'runtime_probe.py'),str(out/'runtime.json')],'runtime')
        run([sys.executable,'-m','pytest','-q',str(ROOT/'frozen/test_hostile_x2.py'),'--junitxml='+str(out/'x2.xml')],'x2',0 if phase=='before' else 1)
        run([sys.executable,str(ROOT/'probe.py'),str(out/'collision.json')],'collision')
        collision=json.loads((out/'collision.json').read_text())
        assert len(collision['raw_occurrence_rows'])==(2 if phase=='before' else 1)
        assert collision['checkpoint']==collision['initial']
        if phase=='after':assert collision['second']['reason']=='EVENT_IDENTITY_CONFLICT'
        x2=ET.parse(out/'x2.xml').find('testsuite')
        assert int(x2.get('tests'))==17 and int(x2.get('errors'))==0
        failed=[c.get('name') for c in x2.findall('testcase') if c.find('failure') is not None]
        assert failed==([] if phase=='before' else ['test_same_event_id_accepts_distinct_objective_payload_hashes'])
        if phase=='after':
            run([sys.executable,'-m','pytest','-q',str(ROOT/'test_identity.py'),'--junitxml='+str(out/'identity.xml')],'identity')
        if phase=='after':
            suite=ET.parse(out/'identity.xml').find('testsuite')
            assert int(suite.get('tests'))==45 and int(suite.get('failures'))==0 and int(suite.get('errors'))==0
        shutil.copytree(stage/'evidence',out/'b2',dirs_exist_ok=True)
        if (out/'failed_b2').exists():shutil.rmtree(out/'failed_b2')
        # Actual source/import identity for the exact bytes just executed.
        (out/'source_runtime.json').write_text(json.dumps(dict(
            bridge_sha256=hashlib.sha256((stage/'bridge.py').read_bytes()).hexdigest(),
            test_sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in ROOT.rglob('*.py') if '__pycache__' not in str(p)},
            b1_module='imports/B1/bfirst.py',p1_module='imports/P1/p1_contract.py'),indent=2)+'\n')
        shutil.copyfile(stage/'execution_receipt.json',out/'b2_execution_receipt.json')
        manifest=json.loads((stage/'imported_sources.json').read_text())
        for row in manifest:
            assert hashlib.sha256((stage/row['materialized_path']).read_bytes()).hexdigest()==row['sha256']
        (out/'imported_sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
        (out/'commands.json').write_text(json.dumps(commands,indent=2).replace(str(ROOT),'<R1>')+'\n')
    # Sanitize XML through its tree so placeholder angle brackets are escaped.
    def portable(s):
        s=s.replace(str(ROOT),'<R1>').replace(str(Path.home()),'<HOME>')
        s=re.sub(r"/private/var/folders/[^\s'\"<>]*",'<TEMP>',s)
        return re.sub(r"/var/folders/[^\s'\"<>]*",'<TEMP>',s)
    for p in out.rglob('*'):
        if not p.is_file() or p.suffix not in ('.json','.xml','.log'):continue
        if p.suffix=='.xml':
            tree=ET.parse(p)
            for node in tree.iter():
                node.attrib.pop('hostname',None)
                for k,v in node.attrib.items():node.set(k,portable(v))
                if node.text:node.text=portable(node.text)
                if node.tail:node.tail=portable(node.tail)
            tree.write(p,encoding='utf-8',xml_declaration=True)
        else:p.write_text(portable(p.read_text()))
    print(phase+' courts complete')
if __name__=='__main__':main(sys.argv[1])
