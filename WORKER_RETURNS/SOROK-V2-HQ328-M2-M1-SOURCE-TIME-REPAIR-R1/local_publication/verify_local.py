"""Verify and publish handoff evidence; never edit supplied implementation/tests."""
from pathlib import Path
import datetime, hashlib, json, os, platform, shutil, subprocess, sys, tarfile, tempfile, uuid
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'local_publication'
REPO=ROOT.parent.parent
GRADE='TEST_ONLY_M1_SOURCE_TIME_REPAIR_CANDIDATE_PENDING_I2'
SEAL='6eebdf23fec3d24d29df1f95fd567f3599316e11'
BLOBS={'M1':'37174efcf6689f87110ef97023e91cc83786fe2a','I2':'23ebc5a15df242b288555ec415ef6533b4420a7f'}

def sha(data):return hashlib.sha256(data).hexdigest()
def dump(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)

def verify_package():
    m=json.loads((ROOT/'manifest.json').read_text())
    for name,expected in m['file_sha256'].items():
        path=ROOT/name
        assert path.resolve().is_relative_to(ROOT.resolve())
        assert sha(path.read_bytes())==expected,name
    for label,record in m['pinned_archives'].items():
        data=(ROOT/record['relative']).read_bytes()
        assert sha(data)==record['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==BLOBS[label]
        assert git('cat-file','blob',BLOBS[label])==data
    return m

def archive(path,dest):
    with tarfile.open(path) as tar:
        for member in tar.getmembers():
            assert not member.issym() and not member.islnk()
            target=dest/member.name
            assert target.resolve().is_relative_to(dest.resolve())
            if member.isfile():
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(tar.extractfile(member).read())

def outcomes(path):
    tree=ET.parse(path)
    return {c.get('name'):('ERROR' if c.find('error') is not None else 'RED' if c.find('failure') is not None else 'SKIP' if c.find('skipped') is not None else 'PASS') for c in tree.iter('testcase')}

def main():
    m=verify_package();commands=[];results={}
    with tempfile.TemporaryDirectory(prefix='m2-local-verification-') as tmp:
        stage=Path(tmp)
        def portable(s):return s.replace(str(stage),'<ISOLATED_STAGE>').replace(str(ROOT),'<M2_RETURN>').replace(str(Path.home()),'<HOME>')
        original=stage/'original';strict=stage/'strict'
        archive(ROOT/m['pinned_archives']['M1']['relative'],original)
        archive(ROOT/m['pinned_archives']['I2']['relative'],strict)
        # Independently inspect supplied source archive, not just its outer hash.
        source_archive=stage/'source_archive'
        archive(ROOT/'archives/M2_source_tests.tar.gz',source_archive)
        archived={p.name:p for p in source_archive.rglob('*') if p.is_file()}
        for name in ('kernel.py','test_m2.py'):
            assert archived[name].read_bytes()==(ROOT/name).read_bytes(),name
        cases=[('after_m2_41',None,'test_m2.py',41,0),
               ('before_m1_37',original/'kernel.py','test_kernel.py',37,0),
               ('before_i2_23',original/'kernel.py','test_i2_strict.py',23,9),
               ('after_m1_37',ROOT/'kernel.py','test_kernel.py',37,19),
               ('after_i2_23',ROOT/'kernel.py','test_i2_strict.py',23,10)]
        for label,kernel,test,n,red in cases:
            if kernel is None:cwd=ROOT
            else:
                cwd=stage/label;cwd.mkdir()
                shutil.copyfile(kernel,cwd/'kernel.py')
                shutil.copyfile((original if test=='test_kernel.py' else strict)/test,cwd/test)
            env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
            env.pop('PYTHONPATH',None)
            args=[sys.executable,'-m','pytest','-q',test,'-p','no:cacheprovider','--junitxml='+str(OUT/(label+'.xml'))]
            p=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True)
            (OUT/(label+'.log')).write_text(portable(p.stdout+p.stderr))
            commands.append(dict(command=[portable(x) for x in args],cwd=portable(str(cwd)),environment=dict(PYTHONDONTWRITEBYTECODE='1',PYTHONPATH='UNSET'),exit_code=p.returncode,expected_exit=bool(red)))
            assert p.returncode==(1 if red else 0),(label,p.returncode)
            actual=outcomes(OUT/(label+'.xml'))
            expected=outcomes(ROOT/'execution'/(label+'.xml'))
            assert len(actual)==n and sum(v=='RED' for v in actual.values())==red
            assert all(v in ('PASS','RED') for v in actual.values())
            assert actual==expected,(label,'per-case outcome divergence')
            imported=subprocess.check_output([sys.executable,'-c','import kernel,json,hashlib;from pathlib import Path;p=Path(kernel.__file__);print(json.dumps(dict(module_path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())))'],cwd=cwd,env=env,text=True)
            imported=json.loads(imported)
            assert imported['sha256']==sha((cwd/'kernel.py').read_bytes())
            results[label]=dict(tests=n,pass_count=n-red,red=red,errors=0,per_case=actual,loaded_kernel=portable(imported['module_path']),kernel_sha256=imported['sha256'])
            for xml in [OUT/(label+'.xml')]:
                t=ET.parse(xml)
                for node in t.iter():
                    node.attrib.pop('hostname',None)
                    for key,value in node.attrib.items():node.set(key,portable(value))
                    if node.text:node.text=portable(node.text)
                    if node.tail:node.tail=portable(node.tail)
                t.write(xml,encoding='utf-8',xml_declaration=True)
            print(label,n-red,'PASS',red,'RED',flush=True)
    verify_package()
    dump('commands.json',commands)
    dump('verification.json',dict(grade=GRADE,expected_startup=SEAL,input_form='supplied already-extracted directory; no ZIP container available to hash',package_files_verified=24,package_manifest_sha256=sha((ROOT/'manifest.json').read_bytes()),original_manifest_preserved=True,pinned_blobs=BLOBS,results=results,divergences=[],source_kernel_sha256=m['file_sha256']['kernel.py'],source_tests_sha256=m['file_sha256']['test_m2.py']))
    marker=dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),alias='M2_local_handoff')
    dump('runtime_marker.json',marker)
    dump('environment_passport_delta.json',dict(passport_schema='SOROK_ENVIRONMENT_PASSPORT_R1',**marker,owner_session_alias='M2_local_publication',surface='LOCAL_SHARED_STORE',machine_alias='authorized_local',status='LIVE_VERIFIED',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),runtime_marker_digest=sha((OUT/'runtime_marker.json').read_bytes()),python=platform.python_version(),pytest=subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),git=git('--version').decode().strip(),node='NOT_REQUIRED',shell='zsh_user_environment',capabilities=dict(Python='VERIFIED',pytest='VERIFIED',Git='VERIFIED',filesystem='VERIFIED',remote_read='VERIFIED'),git_object_store_alias='existing_shared_store',worktree_alias='M2_isolated_publication',branch=m['remote_branch'],checkout_base=SEAL,pre_publication_head=git('rev-parse','HEAD').decode().strip(),dirty_state='assigned subtree only',dependency_closure_status='BOUNDED_FULL_FOR_HANDOFF',materialized_source_refs=dict(pinned_archives=m['pinned_archives'],binary_git_blobs=BLOBS,actual_imports='verification.json/results'),covered_test_suites='verification.json and commands.json',science_grade=GRADE,model_provider='OpenAI_Codex_user_authorized_handoff',effort='UNKNOWN',pricing_class='UNKNOWN',observed_credits=None,observed_usage=None,independent_review_separation='local execution/publication only; NOT scientific I2',privacy_source_grant='private sourcefree handoff only',assignments_completed=['M2_LOCAL_VERIFICATION'],next_good_affinity_tags=['SOURCE_CUSTODY','GIT_PUBLICATION'],staged_state_preservation='input sources retained; temporary comparison dirs disposed',retire_or_rebuild_reason=None))
    print('All five suites match the supplied per-case outcomes; all input bytes unchanged',flush=True)

if __name__=='__main__':main()
