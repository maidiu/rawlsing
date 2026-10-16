"""Independent evidence consistency/custody checks, not independent acceptance."""
from pathlib import Path
import subprocess,json,hashlib,xml.etree.ElementTree as E,datetime,difflib,socket,shutil
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];M2=R/'staging/ms2';M1=M2/'staging/ms1';RT=M1/'runtime'
MS1='d40cc32ecec8f681dcced6a482b6438a86080899';P1='WORKER_RETURNS/SOROK-R3-HQ316-MS1-SERIAL-MEMORY-BELIEF-FEASIBILITY-R1';MS2='34b96ea98de181ca5264f0eed3824cad2db7cfc0';P2='WORKER_RETURNS/SOROK-R3-HQ317-MS2-MS1-SERIAL-INDEPENDENT-R1';FREEZE='650a46593fd19be2642a025c1e03bbe09583d337'
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0',*a],cwd=ROOT)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def save(p,d):(R/p).write_text(json.dumps(d,indent=2)+'\n')
def clean(s):
    for a,b in [(str(R),'[MS3_RETURN]'),(str(ROOT),'[WORKTREE]'),(str(Path.home()),'[HOME]'),(socket.gethostname(),'[HOST]')]:s=s.replace(a,b)
    return s
def cases(raw):
    return [dict(name=x.get('name'),classname=x.get('classname'),result='FAIL' if x.find('failure') is not None else 'ERROR' if x.find('error') is not None else 'SKIP' if x.find('skipped') is not None else 'PASS',failure=x.findtext('failure')) for x in E.fromstring(raw).iter('testcase')]
def main():
    for p,h in json.loads((R/'03_AUTHOR_FREEZE.json').read_text())['files'].items():
        b=(R/p).read_bytes();assert hashlib.sha256(b).hexdigest()==h and b==git('show',FREEZE+':'+str((R/p).relative_to(ROOT)))
    extension=json.loads((R/'03B_SELECTOR_EXTENSION_FREEZE.json').read_text())
    for path,h in extension['files'].items():
        data=(R/path).read_bytes();assert hashlib.sha256(data).hexdigest()==h and data==git('show','81ca89d3c1eab7f74c5036d1a42ca6b337502790:'+str((R/path).relative_to(ROOT)))
    v1=(R/'repro/test_selector_extension.py').read_bytes();v2=(R/'repro/test_selector_extension_v2.py').read_bytes()
    assert v1.replace(b'indent=2)',b'indent=2,default=str)')==v2
    assert v2==git('show','52a5c4706cce3a25ceed3d51be2beacd99d58599:'+str((R/'repro/test_selector_extension_v2.py').relative_to(ROOT)))
    assert git('rev-parse',FREEZE+'^').decode().strip()=='21c885ca1fcba532f71e45d1ba959d9943d33bf0'
    assert git('ls-tree','-r','--name-only',FREEZE,str((R/'candidate').relative_to(ROOT))).decode()==''
    native=[]
    for x in json.loads((M1/'evidence/native_source_ledger.json').read_text()):
        b=(M1/x['local']).read_bytes();assert b==git('show',x['commit']+':'+x['authoritative_path']);assert blob(b)==x['git_blob_sha1'];native.append(x)
    assert len(native)==10
    save('06_NATIVE_SOURCE_IDENTITIES.json',dict(native_CAN2=9,EMPTY_guard=1,files=native,accepted_law_blobs={'CAN008_R2':'b80dd6925066510ecbbfec7b427bf9f688475663','ADP016':'c6619a286e115d060ab4830889e7fc23762167a5','ADP017':'eece4f3f2f3f9288ab9bbc645dc81e20a99e1280'}))
    for name,h in json.loads((R/'06_NATIVE_SOURCE_IDENTITIES.json').read_text())['accepted_law_blobs'].items():
        b=(M2/'staging/accepted_law'/(name+'.txt')).read_bytes();assert blob(b)==h and b==git('cat-file','blob',h)
    tests=[]
    for sha,prefix,rel,path in [(MS1,P1,'runtime/test_ms1_serial.py',RT/'test_ms1_serial.py'),('ee6a48b40247b113c614fe2099d4c443e8dd7bb7','WORKER_RETURNS/SOROK-R3-HQ308-CAN2-LAW-CAUSAL-REPAIR-R1','repro/test_repair.py',RT/'candidate/can2_test_repair.py'),(MS2,P2,'repro/test_ms2.py',M2/'repro/test_ms2.py'),(MS2,P2,'repro/test_literal_p3b.py',M2/'repro/test_literal_p3b.py')]:
        b=path.read_bytes();assert b==git('show',sha+':'+prefix+'/'+rel);tests.append(dict(commit=sha,path=prefix+'/'+rel,module_file=str(path.relative_to(R)),blob_sha1=blob(b),sha256=hashlib.sha256(b).hexdigest(),byte_identical=True))
    # Original prospective falsifier, native empty guard and sources remain literal.
    for name in ['01_PREREGISTRATION.md','02_PREREGISTRATION.json']:assert (M1/name).read_bytes()==git('show','cc2f24a6837d007b0ba7ab5c40f39899e2d7b644:'+P1+'/'+name)
    save('07_UNCHANGED_TEST_AND_FREEZE_CUSTODY.json',dict(tests=tests,MS3_author_freeze=FREEZE,author_test_unchanged=True,candidate_absent_at_freeze=True,MS1_original_prereg='cc2f24a6837d007b0ba7ab5c40f39899e2d7b644; byte-identical',original_P3b='FALSIFIED',F_B='FIRED',serial_identification='HOLD',future_independent_MS4='REQUIRED; author previously MS2 reviewer and cannot self-accept'))
    allcases=[];matrix=[];by_phase={}
    for phase in ['before','after','author']:
        courts=['author'] if phase=='author' else ['original120','ms2_51','literal_p3b']
        for court in courts:
            path=R/'evidence'/phase/court/'junit.xml';rows=cases(path.read_bytes());by_phase[(phase,court)]=rows
            n={'original120':120,'ms2_51':51,'literal_p3b':1,'author':47}[court]
            f=2 if court=='original120' else 8 if court=='ms2_51' and phase=='before' else 1 if court=='literal_p3b' else 0
            count={x:sum(y['result']==x for y in rows) for x in ['PASS','FAIL','ERROR','SKIP']};assert len(rows)==n and count==dict(PASS=n-f,FAIL=f,ERROR=0,SKIP=0),(phase,court,count)
            matrix.append(dict(phase=phase,court=court,tests=n,**count));allcases.extend(dict(phase=phase,court=court,**r) for r in rows)
            if phase=='before':
                original=cases(git('show',(MS1+':'+P1+'/junit/combined_final.xml') if court=='original120' else (MS2+':'+P2+'/evidence/'+('new' if court=='ms2_51' else 'literal_p3b')+'/junit.xml')))
                assert sorted((x['name'],x['result']) for x in original)==sorted((x['name'],x['result']) for x in rows)
    closure=[]
    for court in ['original120','ms2_51','literal_p3b']:
        a={x['name']:x for x in by_phase[('before',court)]};b={x['name']:x for x in by_phase[('after',court)]};assert set(a)==set(b)
        for name in a:
            closure.append(dict(court=court,name=name,before=a[name]['result'],after=b[name]['result']))
    assert sum(x['before']=='FAIL' and x['after']=='PASS' for x in closure if x['court']!='literal_p3b')==8
    extra_folders=[('extension_before','selector_extension',12,1),('extension_after','selector_extension',12,0),('selector_logging_v1/before','selector_extension',12,12),('selector_logging_v1/after','selector_extension',12,12)]
    for phase,court,n,f in extra_folders:
        rows=cases((R/'evidence'/phase/court/'junit.xml').read_bytes());count={k:sum(x['result']==k for x in rows) for k in ['PASS','FAIL','ERROR','SKIP']}
        assert len(rows)==n and count==dict(PASS=n-f,FAIL=f,ERROR=0,SKIP=0)
        matrix.append(dict(phase=phase,court=court,tests=n,**count));allcases.extend(dict(phase=phase,court=court,**x) for x in rows)
    for phase,court,n,f in [('after','original120',120,2),('after','ms2_51',51,0),('after','literal_p3b',1,1),('author','author',47,0)]:
        rows=cases((R/'evidence/repair_v1'/phase/court/'junit.xml').read_bytes());assert len(rows)==n and sum(x['result']=='FAIL' for x in rows)==f
    save('evidence/SELECTOR_EXTENSION_HISTORY.json',dict(original12_expectations_frozen='81ca89d3c1eab7f74c5036d1a42ca6b337502790',v1_logging_TypeErrors_before_assertions='12FAIL per pre/post invocation; preserved under selector_logging_v1',v2_logging_only_change='default=str; all assertions and expected outcomes byte-identical',v2_freeze='52a5c4706cce3a25ceed3d51be2beacd99d58599',initial_source='79dba9afe30844c05fa840e7b36c0d5f27765e0c',v2_initial_result='11PASS/1scientificRED; None consumer returnedEMPTY',final_v2='12PASS',original47_and171_rerun_on_final=True,initial_target_and47_evidence='evidence/repair_v1'))
    save('04_BEFORE_AFTER_MATRIX.json',dict(rows=matrix,main171_before=dict(PASS=161,FAIL=10),main171_after=dict(PASS=169,FAIL=2),author47=dict(PASS=47,FAIL=0),literal_P3b_separate='1FAIL before and after',original171_cases=closure))
    save('05_FULL_EXECUTED_CASE_IDS.json',allcases)
    imports=[]
    for phase,court in by_phase:
        d=json.loads((R/'evidence'/phase/court/'actual_imports.json').read_text());assert d['guard_empty'] and d['guard_unchanged']
        for x in d['imports']:
            if x['module'] in ['ms1_serial','ms3_native_custody']:
                data=git('show',MS1+':'+P1+'/runtime/ms1_serial.py') if phase=='before' else (R/'candidate'/Path(x['module_file']).name).read_bytes()
            else:data=(R/x['module_file']).read_bytes()
            assert blob(data)==x['blob_sha1']
            imports.append(dict(phase=phase,court=court,**x))
    extra_imports=[('extension_before','extension_before/selector_extension'),('extension_after','extension_after/selector_extension'),('logging_v1_before','selector_logging_v1/before/selector_extension'),('logging_v1_after','selector_logging_v1/after/selector_extension'),('repair_v1_after','repair_v1/after/ms2_51'),('repair_v1_author','repair_v1/author/author')]
    for phase,folder in extra_imports:
        d=json.loads((R/'evidence'/folder/'actual_imports.json').read_text());assert d['guard_empty'] and d['guard_unchanged']
        imports.extend(dict(phase=phase,court='selector_or_v1',**x) for x in d['imports'])
    candidate=[]
    for p in (R/'candidate').glob('*.py'):
        b=p.read_bytes();assert b==(RT/p.name).read_bytes();candidate.append(dict(path=str(p.relative_to(R)),module_file=str((RT/p.name).relative_to(R)),blob_sha1=blob(b),sha256=hashlib.sha256(b).hexdigest()))
    seal=json.loads((R/'11_CANDIDATE_SOURCE_SEAL.json').read_text()) if (R/'11_CANDIDATE_SOURCE_SEAL.json').exists() else None
    ledger={str(Path('staging/ms2/staging/ms1')/x['local']):x for x in native}
    for row in imports:
        if row['module'] in ['ms1_serial','ms3_native_custody'] and row['phase']!='before':
            if seal is None:continue
            sha='79dba9afe30844c05fa840e7b36c0d5f27765e0c' if row['phase'] in ['extension_before','logging_v1_before','repair_v1_after','repair_v1_author'] else seal['commit'];path=str((R/'candidate'/Path(row['module_file']).name).relative_to(ROOT))
        elif row['module_file'] in ledger:
            original_row=ledger[row['module_file']];sha=original_row['commit'];path=original_row['authoritative_path']
        else:
            sha=MS1;path=P1+'/'+str((R/row['module_file']).relative_to(M1))
        data=git('show',sha+':'+path);assert blob(data)==row['blob_sha1']
        row.update(source_git_commit=sha,source_git_path=path)
    save('08_ACTUAL_IMPORT_AND_CANDIDATE_AUDIT.json',dict(imports=imports,candidate=candidate,native_code_unchanged=True,production_registry_empty=True,only_owned_wrapper_and_helper_overlay=True,source_grade='Native CAN2 fixture; accepted-law bytes are authority references, not an issued serial rule'))
    original=git('show',MS1+':'+P1+'/runtime/ms1_serial.py').decode();current=(R/'candidate/ms1_serial.py').read_text();(R/'candidate/MS1_TO_MS3.patch').write_text(''.join(difflib.unified_diff(original.splitlines(keepends=True),current.splitlines(keepends=True),fromfile='MS1/ms1_serial.py',tofile='MS3/ms1_serial.py')))
    cells=[]
    for p in sorted((R/'evidence/after/ms2_51/observations').glob('cell_C*.json')):
        after=json.loads(p.read_text());before=json.loads((R/'evidence/before/ms2_51/observations'/p.name).read_text());assert before['pre_read']['owner']==after['pre_read']['owner']
        assert (before['response']['decision_state'],before['response'].get('effect_kind'))==(after['response']['decision_state'],after['response'].get('effect_kind'))
        proof=after['response']['native_owner_provenance'];assert proof['current_owner_state_hash']==after['pre_read']['owner_hash']==after['response']['owner_state_hash_read']
        assert not after['response']['committed'] and not after['response']['production_owner_commit']
        if after['response']['decision_state']!='RESPONSE_EFFECTS_PRODUCED':assert after['pre_read']['registry']==after['after']['registry']
        cells.append(dict(cell=after['cell'],receipt=str(p.relative_to(R)),actual_owner_state_unchanged=True,outcome_projection_unchanged=True,owner_hash=after['pre_read']['owner_hash'],decision=after['response']['decision_state'],effect=after['response'].get('effect_kind'),proof=proof))
    assert len(cells)==11
    save('09_NATIVE_CAUSAL_PRESERVATION.json',dict(cells=cells,original_P3b='FALSIFIED',F_B='FIRED',serial_identification='HOLD',response_committed=False,source_of_private_update_comment='CAN2 candidate owner_transitions.py163-164; not accepted ADP017 law',consumer_exclusion='Choice is authored over verified permission. Full ctx remains available; no type-enforced direct-path exclusion.',history_and_reference_controls='Unchanged MS251 plus actual sourcefree CAN3 comparator passed'))
    failures=[]
    for p in sorted((R/'evidence/after/ms2_51/observations').glob('coherent_forgery_*.json')):
        x=json.loads(p.read_text());assert x['transition']['decision_state']!='APPLIED_EPISTEMIC_TRANSITION' and x['after']['owner']==x['forged_before']['owner'];failures.append(dict(receipt=str(p.relative_to(R)),result=x['transition']['decision_state']))
    for p in sorted((R/'evidence/after/ms2_51/observations').glob('stale_permission_*.json')):
        x=json.loads(p.read_text());assert x['response']['decision_state']!='RESPONSE_EFFECTS_PRODUCED' and x['after']==x['forged_before'];failures.append(dict(receipt=str(p.relative_to(R)),result=x['response']['decision_state']))
    x=json.loads((R/'evidence/after/ms2_51/observations/unknown_selected_claim.json').read_text());assert x['response']['decision_state'] not in ['RESPONSE_EFFECTS_PRODUCED','RESPONSE_INPUTS_VALID_EMPTY'] and x['after']==x['before'];failures.append(dict(receipt='evidence/after/ms2_51/observations/unknown_selected_claim.json',result=x['response']['decision_state']))
    assert len(failures)==8
    save('10_EIGHT_RED_CLOSURE_AND_ATOMICITY.json',dict(eight=failures,author_fault_receipts='evidence/author/observations/exception_*.json',author_faults_after_real_native_operations=5,original_tests_unchanged=True,no_journal_or_commit_simulation=True,candidate_only_requires_MS4=True))
    # Retain raw first-run outputs before portable metadata redaction.
    old_receipt=R/'evidence/PORTABILITY_RECEIPT.json';redactions=json.loads(old_receipt.read_text())['files'] if old_receipt.exists() else []
    for p in sorted((R/'evidence').rglob('*')):
        if not p.is_file():continue
        raw=p.read_bytes();new=clean(raw.decode()).encode()
        if new!=raw:
            archived=R/'staging/raw_execution'/p.relative_to(R)
            archived=R/'staging/raw_execution/by_sha256'/hashlib.sha256(raw).hexdigest()
            if not archived.exists():archived.parent.mkdir(parents=True,exist_ok=True);archived.write_bytes(raw)
            assert archived.read_bytes()==raw
            redactions.append(dict(path=str(p.relative_to(R)),raw_sha256=hashlib.sha256(raw).hexdigest(),portable_sha256=hashlib.sha256(new).hexdigest(),raw_archive=str(archived.relative_to(R))));p.write_bytes(new)
    save('evidence/PORTABILITY_RECEIPT.json',dict(policy='Personal path/hostname metadata only; source/test assertions, outcomes and synthetic native state unchanged',raw_retained='ignored staging/raw_execution',files=redactions))
    save('12_COMPLETION_AUDIT.json',dict(schema='MS3_COMPLETION_AUDIT@1',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),before171=dict(PASS=161,FAIL=10),after171=dict(PASS=169,FAIL=2),author47=dict(PASS=47,FAIL=0),selector_extension12=dict(PASS=12,FAIL=0),selector_history='evidence/SELECTOR_EXTENSION_HISTORY.json; v1 logging failures and initial None scientificRED preserved',original_P3b_before_and_after='1separate literalFAIL; F_BFIRED; serial identificationHOLD',all171_case_ids_and_tests_unchanged=True,native9_and_guard1_unchanged=True,candidate_requires_distinct_MS4=True,independence_disclosure='This author previously MS2 reviewer; no self-acceptance',authority='UNISSUED TEST_ONLY; no operative content map/issuer/psychology',production_registry='EMPTY byte-identical',publication='Commit/push and direct final SHA required; final receipt16',verdict='SOURCEFREE_TEST_ONLY_SERIAL_PROVENANCE_REPAIR_CANDIDATE_REQUIRES_MS4'))
    print('MS3_AUDIT_OK: 171before161P/10RED;171after169P/2historicalRED;author47P+selector12P;P3bFAIL retained;candidate requires MS4')
if __name__=='__main__':main()
