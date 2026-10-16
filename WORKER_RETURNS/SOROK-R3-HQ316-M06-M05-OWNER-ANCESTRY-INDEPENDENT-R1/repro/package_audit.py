"""Independent custody audit and portable presentation of actual execution."""
from pathlib import Path
import subprocess, json, hashlib, shutil, xml.etree.ElementTree as ET, sys, socket, datetime, platform
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];M=R/'runtime/m05';M1=M/'runtime/m02/runtime/m01'
M05='8b7f3ed2ad095eee060fd040dcab88e59d4ca255';P05='WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1'
FREEZE='8f6d11c54f313665e9320d4d58af7b6d1825796e'
def git(*args):return subprocess.check_output(['git','-c','gc.auto=0',*args],cwd=ROOT)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def save(name,value):(R/name).write_text(json.dumps(value,indent=2)+'\n')
def clean(s):
    for source,target in [(str(R),'[M06_RETURN]'),(str(ROOT),'[WORKTREE]'),(str(Path.home()),'[HOME]'),(socket.gethostname(),'[HOST]')]:s=s.replace(source,target)
    return s
def cases(path):
    root=ET.fromstring(path if isinstance(path,bytes) else path.read_bytes())
    return [dict(name=t.get('name'),classname=t.get('classname'),outcome='FAIL' if t.find('failure') is not None else 'ERROR' if t.find('error') is not None else 'SKIP' if t.find('skipped') is not None else 'PASS') for t in root.iter('testcase')]
def main():
    assert git('rev-parse',FREEZE+'^').decode().strip()=='3c685eb4734856b61f2d601e082eb325e3f6f1d1'
    assert git('rev-parse','3c685eb4734856b61f2d601e082eb325e3f6f1d1^').decode().strip()=='8af50c539bd249d6aab76bea7cf81f61579906fa'
    for source,dest in [('after','baseline638'),('m05_author','m05_author48'),('historical_nine','historical_nine')]:
        shutil.copytree(M/'evidence'/source,R/'evidence'/dest,dirs_exist_ok=True)
    # Preserve source bytes and assertions: sanitize only presentation paths/host metadata.
    redactions=json.loads((R/'evidence/PORTABILITY_RECEIPT.json').read_text())['files'] if (R/'evidence/PORTABILITY_RECEIPT.json').exists() else []
    for path in sorted((R/'evidence').rglob('*')):
        if not path.is_file():continue
        data=path.read_bytes();text=data.decode();new=clean(text).encode()
        if new!=data:
            redactions.append(dict(path=str(path.relative_to(R)),raw_sha256=hashlib.sha256(data).hexdigest(),portable_sha256=hashlib.sha256(new).hexdigest()))
            path.write_bytes(new)
    save('evidence/PORTABILITY_RECEIPT.json',dict(policy='Literal assertions, case outcomes, source bytes and synthetic causal data unchanged; paths and hostname presentation only',files=redactions,raw_evidence_preserved='runtime/m05/evidence; new original raw metadata represented by digests'))
    matrix=[];all_cases=[]
    for folder,n,f in [('baseline638',638,0),('m05_author48',48,0),('historical_nine',9,9),('new',114,0)]:
        found=[]
        for path in sorted((R/'evidence'/folder).rglob('junit.xml')):
            observed=cases(path);found+=observed
            all_cases.extend(dict(court=folder,junit=str(path.relative_to(R)),**c) for c in observed)
            if folder!='new':
                rel=str(path.relative_to(R/'evidence'/folder));source='after/'+rel if folder=='baseline638' else ('m05_author/' if folder=='m05_author48' else 'historical_nine/')+rel
                original=cases(git('show',M05+':'+P05+'/evidence/'+source))
                assert sorted((c['name'],c['outcome']) for c in original)==sorted((c['name'],c['outcome']) for c in observed),(folder,rel)
        counts={k:sum(c['outcome']==k for c in found) for k in ['PASS','FAIL','ERROR','SKIP']}
        assert len(found)==n and counts==dict(PASS=n-f,FAIL=f,ERROR=0,SKIP=0),(folder,counts)
        matrix.append(dict(court=folder,tests=n,**counts,source_case_names_match_pinned_M05=folder!='new'))
    save('04_EXECUTED_MATRIX.json',matrix);save('05_FULL_CASE_IDS.json',all_cases)
    # Validate actual unchanged executable tests against original Git bytes, not author counts.
    refs=[]
    for row in json.loads((M/'07_LITERAL_EXECUTED_TEST_PREIMAGES.json').read_text()):
        if row['phase']!='after':continue
        refs.append((row['source_commit'],row['source_path'],M/row['actual_file']))
    refs.extend([
        ('0216d9036a87e2f60f42fd5b2870556027808419','WORKER_RETURNS/SOROK-R3-HQ312-M02-MEMORY-MEDIATION-INDEPENDENT-R1/repro/test_independent.py',M/'runtime/m02/repro/test_independent.py'),
        ('e1f7a74e51201b9614bcc578348b4e9db7be7bd3','WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1/repro/test_author.py',M/'repro/test_author.py'),
        ('3a993abcc0a9f6bd3a1bb003d298d293be199ea6','WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/review/test_falsifiers.py',M/'review/test_falsifiers.py'),
        (M05,P05+'/review/test_m05_author.py',M/'review/test_m05_author.py'),
        ('ef12349defe22a50e053a7a8080a67ab45673417','WORKER_RETURNS/SOROK-R3-HQ309-CAN3-CAN008-INDEPENDENT-R1/repro/test_can3.py',M1/'runtime/can3/repro/test_can3.py'),
    ])
    # Historical nine execute the inherited candidate and independent test files unchanged.
    source=M1/'runtime/can3/runtime/author/runtime_root/court_repaired/runtime_root/source'
    historical=[('189da3b54307d8731132c9a7f7baf578fee8bc96','WORKER_RETURNS/SOROK-R3-HQ300-CAN008-FIRST-POSITIVE-SOURCEFREE-R1/candidate/test_hq300_court.py',source/'WORKER_RETURNS/SOROK-R3-HQ300-CAN008-FIRST-POSITIVE-SOURCEFREE-R1/candidate/test_hq300_court.py')]
    # The inherited independent path is anchored by CAN2's exact retained input tree.
    historical.append(('ee6a48b40247b113c614fe2099d4c443e8dd7bb7','WORKER_RETURNS/SOROK-R3-HQ308-CAN2-LAW-CAUSAL-REPAIR-R1/inherited/repro/test_independent.py',M1/'runtime/can3/runtime/author/runtime_root/court_repaired/repro/test_independent.py'))
    refs+=historical
    verified=[]
    for sha,path,actual in refs:
        data=git('show',sha+':'+path);assert actual.read_bytes()==data,(sha,path)
        verified.append(dict(commit=sha,path=path,actual_file=str(actual.relative_to(R)),blob_sha1=blob(data),sha256=hashlib.sha256(data).hexdigest(),byte_identical=True))
    save('06_UNCHANGED_TEST_SOURCE_IDENTITIES.json',verified)
    # All original frozen expectation files remain source-identical to their sealed commits.
    freeze_refs=[('845edf5d7c9c48b192b631dacf295afa6f587137','WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1/01_PREREGISTRATION.md',M1/'01_PREREGISTRATION.md'),('0c875790fd7341402d7eeee4a515ca67dc43ee65','WORKER_RETURNS/SOROK-R3-HQ312-M02-MEMORY-MEDIATION-INDEPENDENT-R1/01_INDEPENDENT_EXPECTATIONS.json',M/'runtime/m02/01_INDEPENDENT_EXPECTATIONS.json'),('3b529996ddd05c3c84225d2054428ff943091aef','WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/review/test_falsifiers.py',M/'review/test_falsifiers.py'),(FREEZE,str((R/'repro/test_m06.py').relative_to(ROOT)),R/'repro/test_m06.py')]
    freeze_rows=[]
    for sha,path,actual in freeze_refs:
        data=git('show',sha+':'+path);assert actual.read_bytes()==data
        freeze_rows.append(dict(commit=sha,path=path,blob_sha1=blob(data),sha256=hashlib.sha256(data).hexdigest()))
    save('07_FREEZE_CUSTODY.json',dict(reviewer_freeze_commit=FREEZE,before_new_execution=True,unchanged=freeze_rows,no_oracle_repair=True,original_M05_freeze='Local prospective freeze15a25d19; published redacted counterpart later. Independently verified delivered tests against03 digest; do not promote later counterpart to prospective Git custody.'))
    # Actual imports were captured after pytest in the same Python process.
    imported=json.loads((R/'evidence/new/actual_imports.json').read_text());index={}
    for sha,prefix in [(M05,P05),('ee6a48b40247b113c614fe2099d4c443e8dd7bb7','WORKER_RETURNS/SOROK-R3-HQ308-CAN2-LAW-CAUSAL-REPAIR-R1'),('189da3b54307d8731132c9a7f7baf578fee8bc96','rawlsing_next'),('02187a14e75ff30dd953d3c7185d689b80e62304','WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1')]:
        for line in git('ls-tree','-r','--full-tree',sha,prefix).decode().splitlines():
            metadata,path=line.split('\t');mode,kind,h=metadata.split()
            if kind=='blob':index.setdefault(h,[]).append(dict(commit=sha,path=path))
    for row in imported['imports']:
        data=(R/row['module_file']).read_bytes();assert blob(data)==row['blob_sha1']
        assert git('cat-file','blob',row['blob_sha1'])==data
        row['verified_git_sources']=index.get(row['blob_sha1'],[])
        assert row['verified_git_sources'],row
    laws=[]
    for name,h in [('CAN008_R2','b80dd6925066510ecbbfec7b427bf9f688475663'),('ADP016','c6619a286e115d060ab4830889e7fc23762167a5'),('ADP017','eece4f3f2f3f9288ab9bbc645dc81e20a99e1280')]:
        path=M1/'runtime/can3/runtime/law'/(name+'.txt');data=path.read_bytes();assert blob(data)==h and data==git('cat-file','blob',h)
        laws.append(dict(name=name,blob_sha1=h,actual_file=str(path.relative_to(R))))
    for name,h in [('cell','7655867608c21eb7e40d6f51434491db380b7e4e'),('claim_provenance','c1e126fd2080ef78e5e77ed96861450a75355276')]:
        assert next(x for x in imported['imports'] if x['module']==name)['blob_sha1']==h
    imported.update(accepted_law_bytes=laws,source_root='M05 fixture candidate; not accepted production owner',actual_absolute_module_file_probe='Observed in process; published relative to this return to remove personal home path')
    save('08_ACTUAL_IMPORT_AND_LAW_AUDIT.json',imported)
    arms=[]
    for path in sorted((R/'evidence/new/observations').glob('factorial_*.json')):
        data=json.loads(path.read_text());before=data['before'];out=data['result'];after=data['after'];state=out['read']['actual_state']
        assert before['owner_state']==state==after['owner_state'];proof=out['read']['claim_selection_provenance']['native_owner_ancestry']
        assert proof['current_owner_state_hash']==out['state_hash']==out['read']['state_hash']
        arms.append(dict(arm=path.stem,source_receipt=str(path.relative_to(R)),actor=out['read']['actor'],events=list(after['events']),first_entry_hash=proof['first_event_entry_hash'],root_state_hash=proof['root_state_hash'],first_owner_hash=proof['first_owner_state_hash'],current_owner_hash=proof['current_owner_state_hash'],streams=out['streams'],actual_state_equal=True,native_first_steps=proof['first_steps'],terminal_transition_refs=proof['terminal_transition_refs']))
    assert len(arms)==36
    save('09_CAUSAL_NATIVE_EVIDENCE.json',dict(arms=arms,paired_counterfactuals='evidence/new/observations/independent_causal_contrasts.json',parallel='DEMONSTRATED_CONSTRUCTED_FINITE',serial_ADP016_to_ADP017='UNPROVED',human_psychological_calibration='UNPROVED'))
    # Final privacy check applies to the portable packet, never scientific source rewrites.
    for p in R.rglob('*'):
        if not p.is_file() or 'runtime' in p.relative_to(R).parts:continue
        text=p.read_text();assert str(Path.home()) not in text and socket.gethostname() not in text,p
    save('10_COMPLETION_AUDIT.json',dict(schema='M06_COMPLETION@1',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),matrix=matrix,independence='ONE_FRESH_REVIEWER; no conversation retrieval, helpers or model switches',reviewer_oracle_unchanged=True,all_original_686_case_names_and_test_sources_verified=True,historical_nine_separate=True,full_CAN3_585_rerun=False,production_registry_empty_unchanged=imported['guard_empty'] and imported['guard_unchanged'],verdict='REVIEW_PASS_SOURCEFREE_FINITE_NATIVE_ANCESTRY',adoption='NO_ADOPTION',remote='Verify after content commit/push; final receipt cannot contain its own commit hash'))
    print('M06_AUDIT_OK: 686 original PASS; 114 independent PASS; 9 historical FAIL; 36 native arms')
if __name__=='__main__':main()
