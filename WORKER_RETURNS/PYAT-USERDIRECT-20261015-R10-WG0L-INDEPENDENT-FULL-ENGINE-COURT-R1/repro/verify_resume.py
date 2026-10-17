"""Revalidate the published independent court without reading candidate source."""
from pathlib import Path
from collections import Counter
import subprocess,hashlib,json,sys,os,datetime,importlib,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];WT=R.parents[1];RT=R/'runtime_root'
OUT=R/'observations/resume_20261016';OUT.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(WT),*args])
def read(path):return json.loads((R/path).read_text())
def main():
    sys.dont_write_bytecode=True
    head=git('rev-parse','HEAD').decode().strip()
    branch=git('branch','--show-current').decode().strip()
    assert branch=='agent/userdirect-pyat-20261015-r10-wg0l-precommitted-full-engine-court-r1'
    assert git('remote','get-url','origin').decode().strip()=='https://github.com/maidiu/rawlsing.git'
    sealed='1f198cb397d1602d0450f8bac60610ebfcaf5b3a'
    assert git('merge-base',sealed,head).decode().strip()==sealed
    frozen=[]
    for row in read('observations/PRECOMMITTED_TEST_ROOT.json')['files']:
        b=(R/row['path']).read_bytes();actual=sha(b);assert actual==row['sha256'],row['path']
        frozen.append(dict(**row,verified=True))
    oracle=read('01_FROZEN_EXPECTATIONS_BEFORE_WG0P4.json')
    groups={k:len(v) for k,v in oracle['hostiles'].items()}
    assert sum(groups.values())==65
    assert dict(Counter(o['disposition'] for o in oracle['operations']))=={'PRODUCED':3,'HELD':16,'INADMISSIBLE':6}
    staged=[]
    for row in read('source_selector_phase_a.json')['files']:
        p=RT/row['staged_path'];b=p.read_bytes()
        blob=git('hash-object',str(p)).decode().strip()
        assert blob==row['git_blob_sha1'] and sha(b)==row['sha256'],row['staged_path']
        assert git('rev-parse',row['commit']+':'+row['source_path']).decode().strip()==blob
        staged.append(dict(path=row['staged_path'],git_blob_sha1=blob,sha256=sha(b),commit=row['commit']))
    sys.path.insert(0,str(RT))
    imports=[]
    owner_pins={**oracle['required_owner_blobs'],'rawlsing_next/pre553_c11_integrity.py':'7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd'}
    for path,blob in owner_pins.items():
        module=importlib.import_module(path[:-3].replace('/','.'));p=Path(module.__file__)
        assert p==RT/path and git('hash-object',str(p)).decode().strip()==blob
        imports.append(dict(module=module.__name__,module_file='runtime_root/'+path,git_blob_sha1=blob,verified=True))
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',
             PYTHONPATH=os.pathsep.join(map(str,[RT,RT/'WG0P2/repro',RT/'WG0P3/repro',R/'repro'])))
    cmd=[sys.executable,'-m','pytest',str(R/'tests/test_precommitted_phase_b.py'),'--collect-only','-q','-p','no:cacheprovider']
    proc=subprocess.run(cmd,cwd=RT,env=env,capture_output=True,text=True)
    (OUT/'collection.stdout').write_text(proc.stdout+proc.stderr)
    assert proc.returncode==0 and '65 tests collected' in proc.stdout
    inherited=[]
    for label in ['author29','author36','phase_a','wg0k_full_historical']:
        suites=list(ET.parse(R/'observations'/f'{label}.xml').getroot().iter('testsuite'))
        inherited.append(dict(label=label,retained_not_rerun=True,
            tests=sum(int(s.attrib['tests']) for s in suites),failures=sum(int(s.attrib['failures']) for s in suites),
            errors=sum(int(s.attrib['errors']) for s in suites),skips=sum(int(s.attrib['skipped']) for s in suites),
            junit='observations/'+label+'.xml',sha256=sha((R/'observations'/f'{label}.xml').read_bytes())))
    # The old manifest is retained verbatim; record stale documentary hashes.
    stale=[]
    for row in read('ARTIFACT_MANIFEST.json')['files']:
        p=R/row['path']
        if not p.exists() or sha(p.read_bytes())!=row['sha256']:
            stale.append(dict(path=row['path'],manifest_sha256=row['sha256'],actual_sha256=sha(p.read_bytes()) if p.exists() else None))
    candidate_branch='refs/heads/agent/userdirect-pyat-20261015-r9-wg0p4-frontier-fact-receipt-repair-r1'
    raw=git('ls-remote','https://github.com/maidiu/rawlsing.git',candidate_branch).decode().strip()
    candidate_sha=raw.split()[0]
    state='WAIT_FOR_CANDIDATE_PUSH' if candidate_sha=='c1e88fb26f3ef757f13bad7cf901cd6529a368c8' else 'CANDIDATE_REF_MOVED_REQUIRES_GOVERNED_RETURN_INSPECTION'
    record=dict(schema='WG0L_RESUME_VERIFICATION@1',at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        sealed_resume=sealed,local_head_at_probe=head,branch=branch,
        prior_phase_a_checkpoint='aa4e361e9fbed79c395cb986c51798354bb3d6cd',
        phase_a_status='PHASE_A_ORACLE_READY_NOT_CANDIDATE_ADJUDICATED',
        state=state,candidate_branch=candidate_branch,candidate_remote_sha=candidate_sha,
        candidate_remote_ref_output=raw,candidate_source_read=False,candidate_imported=False,
        phase_b_executed=False,candidate_verdict=None,
        frozen_files=frozen,hostile_groups=groups,hostiles_collected=65,
        original_op_dispositions=dict(Counter(o['disposition'] for o in oracle['operations'])),
        verified_staged_sources=staged,actual_native_imports=imports,
        runtime_marker=read('observations/runtime_marker.json'),
        runtime_marker_sha256=sha((R/'observations/runtime_marker.json').read_bytes()),
        versions={'python':sys.version.split()[0],'pytest':subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),'git':git('--version').decode().strip()},
        collection_command=['python3','-m','pytest','tests/test_precommitted_phase_b.py','--collect-only','-q','-p','no:cacheprovider'],collection_exit=proc.returncode,
        collection_stdout='observations/resume_20261016/collection.stdout',
        inherited_junit=inherited,inherited_manifest_mismatches=stale,
        frozen_source_oracle_mutations=False,original_source_reads=0,owner_edits=False,
        preexisting_untracked_path_left_untouched='.DS_Store',
        live_worker_handle=None,no_worker_liveness_inferred_from_branch=True,
        goal_turn_classification='PROGRESS_LIVE_CUSTODY_AND_GATE_EVIDENCE',
        completion='NOT_COMPLETE_PHASE_B_GATE_UNSATISFIED')
    (OUT/'verification.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'state':state,'candidate_sha':candidate_sha,'frozen_files_verified':len(frozen),'staged_sources_verified':len(staged),'native_imports_verified':len(imports),'hostiles_collected':65,'legacy_manifest_mismatches':stale}))
if __name__=='__main__':main()
