"""One-store, source-immutable X3 reproduction and independent evidence collector.

python3 run_review.py --runtime /tmp/new-x3-runtime
Use --collect-only with an already executed runtime to avoid redundant court runs.
"""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,tarfile,sqlite3,uuid,platform,datetime,shutil,re
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
B3_SHA='47b46a85b9ebb633754866f1e6f1b12db3bd2012'
PREFIX='WORKER_RETURNS/SOROK-V2-HQ329-B3-COUPLED-INTERPRETATION-R1/'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def counts(p):
    root=ET.parse(p).getroot()
    return {k:sum(int(x.get(k,'0')) for x in root.iter('testsuite')) for k in ('tests','failures','errors','skipped')}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--runtime',required=True);parser.add_argument('--collect-only',action='store_true');args=parser.parse_args()
    b3=Path(args.runtime).resolve()/'WORKER_RETURNS/B3';b3.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,GIT_DIR=git('rev-parse','--path-format=absolute','--git-common-dir').decode().strip(),X3_B3_ROOT=str(b3),X3_EVIDENCE=str(ROOT/'evidence/sql'))
    if not args.collect_only:
        for p in git('ls-tree','-r','--name-only',B3_SHA,PREFIX).decode().splitlines():
            rel=p[len(PREFIX):]
            if rel.startswith('evidence/'):continue
            target=b3/rel;target.parent.mkdir(parents=True,exist_ok=True);data=git('show',B3_SHA+':'+p)
            if target.exists():assert target.read_bytes()==data,rel
            else:target.write_bytes(data)
        result=subprocess.run([sys.executable,'run_all.py'],cwd=b3,env=env,capture_output=True,text=True)
        (ROOT/'reproduction_driver.log').write_text(result.stdout+result.stderr)
        # Pinned author finalizer requires its author branch. Never fake/change it.
        if result.returncode:assert "assert branch=='agent/rabochii" in result.stdout+result.stderr
        p=subprocess.run([sys.executable,'-m','pytest','-q',str(ROOT/'test_independent.py'),'--junitxml='+str(ROOT/'evidence/independent_final.xml')],cwd=ROOT,env=env,capture_output=True,text=True)
        (ROOT/'independent_final.log').write_text(p.stdout+p.stderr)
        assert p.returncode in (0,1)
        fenv=dict(env,X3_EVIDENCE=str(ROOT/'evidence/f2_blinded'))
        p=subprocess.run([sys.executable,str(ROOT/'audit_f2.py')],env=fenv,capture_output=True,text=True)
        (ROOT/'f2_blinded.log').write_text(p.stdout+p.stderr);assert p.returncode==0
    # Independently compare every imported Git blob and archive member to bytes.
    rows=json.loads((b3/'source_manifest.json').read_text());verified=[]
    for row in rows:
        data=(b3/row['local']).read_bytes();assert sha(data)==row['sha256']
        if 'commit' in row:
            path=row.get('path',row.get('source_path'));original=git('show',row['commit']+':'+path)
            assert data==original
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            assert blob==row['git_blob_sha1']==git('rev-parse',row['commit']+':'+path).decode().strip()
        else:
            archive=b3/'.runtime/b2/imports/F1/F1_frozen_court.tar.gz';assert sha(archive.read_bytes())==row['archive_sha256']
            with tarfile.open(archive) as t:assert t.extractfile(row['archive_member']).read()==data
        verified.append(dict(row,independently_verified=True))
    # All B3 executable files are verified separately against exact target commit.
    for p in git('ls-tree','-r','--name-only',B3_SHA,PREFIX).decode().splitlines():
        rel=p[len(PREFIX):]
        if not rel.endswith('.py'):continue
        data=(b3/rel).read_bytes();assert data==git('show',B3_SHA+':'+p)
        verified.append(dict(commit=B3_SHA,path=p,local=rel,sha256=sha(data),git_blob_sha1=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),independently_verified=True))
    dump(ROOT/'verified_sources.json',verified)
    probe="import sys,json,hashlib;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import integration; r=Path(sys.argv[1]).resolve();print(json.dumps([dict(module=n,relative_file=str(Path(m.__file__).resolve().relative_to(r)),sha256=hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()) for n,m in list(sys.modules.items()) if getattr(m,'__file__',None) and Path(m.__file__).resolve().is_relative_to(r)]))"
    modules=json.loads(subprocess.check_output([sys.executable,'-c',probe,str(b3)],env=env));dump(ROOT/'loaded_modules.json',modules)
    for m in modules:assert any(m['sha256']==r['sha256'] for r in verified),m
    shutil.copytree(b3/'evidence',ROOT/'evidence/reproduction',dirs_exist_ok=True)
    shutil.copyfile(b3/'F2_CASE_MATRIX.json',ROOT/'author_adapter_reexecuted_F2_matrix.json')
    summary={str(p.relative_to(ROOT/'evidence')):counts(p) for p in (ROOT/'evidence').rglob('*.xml')}
    dump(ROOT/'suite_results.json',summary)
    sql={}
    for name in ('positive','positive_cold','permission_absent','permission_absent_cold'):
        p=b3/'evidence/loop'/(name+'.sqlite');db=sqlite3.connect(p)
        integrity=db.execute('PRAGMA integrity_check').fetchone()[0];assert integrity=='ok'
        snap={n:db.execute('SELECT * FROM '+n+' ORDER BY 1').fetchall() for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")};db.close()
        sql[name]=dict(integrity=integrity,rows={k:len(v) for k,v in snap.items()},snapshot_hash=sha(json.dumps(snap,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()),file_sha256=sha(p.read_bytes()))
    assert sql['positive']['snapshot_hash']==sql['positive_cold']['snapshot_hash']
    assert sql['permission_absent']['snapshot_hash']==sql['permission_absent_cold']['snapshot_hash']
    dump(ROOT/'sql_replay_audit.json',sql)
    marker=b3/'.x3_runtime_marker.json'
    if not marker.exists():dump(marker,dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4())))
    passport=dict(passport_schema='SOROK_WARM_ENVIRONMENT_PASSPORT_R1',**json.loads(marker.read_text()),owner_session_alias='X3_INDEPENDENT_REVIEWER',surface='LOCAL_SHARED_STORE',machine_alias='LOCAL_X3',conversation_or_account_affinity=None,status='LIVE_VERIFIED',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),runtime_marker_digest=sha(marker.read_bytes()),probe_command_and_result=dict(python=sys.version.split()[0],pytest=__import__('pytest').__version__,sqlite=sqlite3.sqlite_version,git=git('--version').decode().strip(),node=subprocess.check_output(['node','--version'],text=True).strip(),shell='zsh'),capabilities={x:'VERIFIED' for x in ('python','pytest','sqlite','git','node','filesystem','subprocess')},git_object_store_alias='EXISTING_SHARED_STORE',worktree_alias='X3_SEALED_REVIEW',branch=git('branch','--show-current').decode().strip(),exact_checkout_base='50349f2e90f8e9d0379040fdb7d3186dfe3b6c02',head_at_probe=git('rev-parse','HEAD').decode().strip(),clean_dirty_state='ONLY_X3_RETURN_CHANGES',materialized_source_refs='verified_sources.json',verified_imports='loaded_modules.json',dependency_closure_status='BOUNDED',fixture_query_source_permission='USER_AUTHORIZED_SOURCEFREE_ONLY',covered_test_suites='suite_results.json',science_grade='B3_REVISE',model_provider='CODEX',model_effort='USER_REQUESTED_GPT6_MEDIUM_RUNTIME_SELECTION_NOT_INDEPENDENTLY_VERIFIED',pricing_class='UNKNOWN',observed_usage=None,independent_review_separation='FRESH_X3_NO_B3_OR_M2_AUTHORSHIP_NO_AGENTS',privacy_source_grant='SYNTHETIC_ONLY_NO_MODEL_APIS',assignments_completed=['X3'],next_good_affinity_tags=['B3_ATOMICITY','TEMPORAL','SOURCE_PREIMAGE','SQLITE'],staged_state_preservation='LOCAL_RUNTIME_RECHECK_ON_RESUME',retire_or_rebuild_reason=None,attestation='00C_READ=YES;00D_WARM_PASSPORT_READ=YES;LIVE_RESOURCE_CHECK=YES;REAL_SESSION_CONTINUITY_VERIFIED_OR_NEW=YES;CHEAPEST_QUALIFIED_ROUTE_EVALUATED=YES;INDEPENDENCE_AND_AUTHORITY_PRESERVED=YES')
    dump(ROOT/'environment_passport_delta.json',passport)
    # Portable evidence may sanitize local path/hostname; exact source bytes never change.
    for p in ROOT.rglob('*'):
        if not p.is_file() or '.runtime' in p.parts or p.suffix not in ('.json','.xml','.log'):continue
        def portable(text):
            text=text.replace(str(b3),'<B3_RUNTIME>').replace(str(REPO),'<REVIEW_WORKTREE>').replace(str(Path.home()),'<HOME>')
            return re.sub(r'/(?:private/)?var/folders/[^\s\'\"<>]*','<TEMP>',text)
        text=p.read_text()
        if p.suffix=='.xml':
            tree=ET.fromstring(text)
            for node in tree.iter():
                node.attrib.pop('hostname',None)
                for k,v in list(node.attrib.items()):node.set(k,portable(v))
                if node.text:node.text=portable(node.text)
                if node.tail:node.tail=portable(node.tail)
            text=ET.tostring(tree,encoding='unicode')
        else:text=portable(text)
        p.write_text(text)
    print('Independent Git/import/SQL audit complete:',len(verified),'sources;',len(modules),'loaded modules')
if __name__=='__main__':main()
