"""Package actual MS2 results; REDs remain REDs. No scientific test rerun."""
from pathlib import Path
import subprocess,json,hashlib,xml.etree.ElementTree as E,datetime,socket,shutil
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];S=R/'staging/ms1';SRC='d40cc32ecec8f681dcced6a482b6438a86080899';PREFIX='WORKER_RETURNS/SOROK-R3-HQ316-MS1-SERIAL-MEMORY-BELIEF-FEASIBILITY-R1';F='6a1e733cd92113b10ba85db4e93f13e9ef9861b5'
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0',*a],cwd=ROOT)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def save(n,d):(R/n).write_text(json.dumps(d,indent=2)+'\n')
def clean(s):
    for a,b in [(str(R),'[MS2_RETURN]'),(str(ROOT),'[WORKTREE]'),(str(Path.home()),'[HOME]'),(socket.gethostname(),'[HOST]')]:s=s.replace(a,b)
    return s
def cases(b):
    return [dict(name=x.get('name'),classname=x.get('classname'),result='FAIL' if x.find('failure') is not None else 'ERROR' if x.find('error') is not None else 'SKIP' if x.find('skipped') is not None else 'PASS',failure=x.findtext('failure')) for x in E.fromstring(b).iter('testcase')]
def main():
    fs=json.loads((R/'03_REVIEWER_FREEZE.json').read_text())
    for p,h in fs['files'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h and (R/p).read_bytes()==git('show',F+':'+str((R/p).relative_to(ROOT)))
    assert git('rev-parse',F+'^').decode().strip()=='f0362f849819583564bf42d40002d246657ad887'
    assert git('rev-parse','f0362f849819583564bf42d40002d246657ad887^').decode().strip()=='c0d8d84d1c095720dfc570bf4e751a6854f7ccec'
    # Original prospective material is copied verbatim, never rewritten for this court.
    old=R/'evidence/ms1_original_prereg';old.mkdir(exist_ok=True)
    chrono=[]
    for name in ['01_PREREGISTRATION.md','02_PREREGISTRATION.json']:
        raw=git('show','cc2f24a6837d007b0ba7ab5c40f39899e2d7b644:'+PREFIX+'/'+name)
        assert raw==(S/name).read_bytes()==git('show',SRC+':'+PREFIX+'/'+name);(old/name).write_bytes(raw)
        chrono.append(dict(path=PREFIX+'/'+name,freeze_commit='cc2f24a6837d007b0ba7ab5c40f39899e2d7b644',blob_sha1=blob(raw),sha256=hashlib.sha256(raw).hexdigest(),unchanged=True))
    freeze_tree=git('ls-tree','-r','--name-only','cc2f24a6837d007b0ba7ab5c40f39899e2d7b644',PREFIX).decode().splitlines()
    assert not any(x.endswith(('/runtime/ms1_serial.py','/runtime/test_ms1_serial.py')) for x in freeze_tree)
    times={}
    for name in ['can2_repair_control.xml','ms1_serial.xml','combined_final.xml']:
        times[name]=[x.get('timestamp') for x in E.parse(S/'junit'/name).getroot().iter('testsuite')]
    freeze_time=datetime.datetime.fromisoformat(git('show','-s','--format=%cI','cc2f24a6837d007b0ba7ab5c40f39899e2d7b644').decode().strip())
    assert all(datetime.datetime.fromisoformat(x)>freeze_time for name in ['ms1_serial.xml','combined_final.xml'] for x in times[name])
    history=git('log','--reverse','--format=%H %P %aI %cI %s','8bb23745ef0e650cfaea241754e3bf73600ac738..'+SRC,'--',PREFIX).decode().splitlines()
    save('07_ORIGINAL_AND_REVIEWER_FREEZE_CUSTODY.json',dict(original_prereg=chrono,original_git_history=history,original_junit_reported_timestamps=times,new_mediator_and_test_absent_at_original_freeze=True,new_mediator_first_published_commit='67e14f129674af667025c87b06a878c365ff8d6a',chronology_scope='Git ancestry and reported JUnit timestamps support prereg before published implementation/results; no independently attested host first-execution clock',reviewer_freeze_commit=F,reviewer_before_collection_import_execution=True,reviewer_files_unchanged=True,original_P3b='FALSIFIED; original inequality and F_B gate retained',original_top_gate=False))
    # Verify all actual source imports and original executable test preimages.
    source_rows=[]
    for row in json.loads((R/'01_SOURCE_PACKET_IDENTITIES.json').read_text()):
        if not row['path'].endswith('.py'):continue
        data=(R/row['local']).read_bytes();assert data==git('show',SRC+':'+row['path']);assert blob(data)==row['blob_sha1'];source_rows.append(row)
    imported=[];lookup={x['local']:x for x in source_rows}
    for court in ['original','new','literal_p3b']:
        d=json.loads((R/'evidence'/court/'actual_imports.json').read_text());assert d['guard_empty'] and d['guard_unchanged']
        for x in d['imports']:
            assert x['module_file'] in lookup,x
            source=lookup[x['module_file']];assert source['blob_sha1']==x['blob_sha1']
            imported.append(dict(court=court,**x,source_commit=SRC,source_path=source['path']))
    native=json.loads((R/'evidence/NATIVE_BLOB_VERIFICATION.json').read_text())
    for row in native['files']:
        data=(S/row['local']).read_bytes();assert data==git('show',row['commit']+':'+row['authoritative_path']);assert blob(data)==row['git_blob_sha1']
    save('08_ACTUAL_IMPORT_AND_SOURCE_AUDIT.json',dict(native_CAN2_verified=9,guard_verified=1,total_verified=10,imports=imported,source_preimages=source_rows,production_guard_empty_and_unchanged=True,absolute_module_file_observed_in_python=True,portable_paths='Relative to this return; personal home path removed only in presentation'))
    # Keep the original literal120, independent51, and literal original prediction separate.
    allcases=[];matrix=[]
    for court,n,f in [('original',120,2),('new',51,8),('literal_p3b',1,1)]:
        rows=cases((R/'evidence'/court/'junit.xml').read_bytes());assert len(rows)==n
        counts={k:sum(x['result']==k for x in rows) for k in ['PASS','FAIL','ERROR','SKIP']};assert counts==dict(PASS=n-f,FAIL=f,ERROR=0,SKIP=0)
        matrix.append(dict(court=court,tests=n,**counts));allcases.extend(dict(court=court,**x) for x in rows)
        if court=='original':
            original=cases(git('show',SRC+':'+PREFIX+'/junit/combined_final.xml'))
            assert sorted((x['name'],x['result']) for x in original)==sorted((x['name'],x['result']) for x in rows)
    save('04_EXECUTED_MATRIX.json',matrix);save('05_FULL_CASE_IDS.json',allcases)
    # Real independently reconstructed state hashes and events match original per-cell observations.
    original_cells={x['cell']:x for x in json.loads((S/'evidence/intervention_receipts.json').read_text())}
    cells=[]
    for path in sorted((R/'evidence/new/observations').glob('cell_C*.json')):
        d=json.loads(path.read_text());old=original_cells[d['cell']];state=d['pre_read']['owner']['state'];memory=d['before']['memory'];response=d['response']
        assert memory['memory_id']==old['memory_id'] and memory['current_state_hash']==old['memory_state_hash']
        assert d['pre_read']['owner_hash']==old['owner_state_hash_after_mediation']==response['owner_state_hash_read']
        assert d['before']['events'][0]['event_hash']==old['e1_event_hash'] and d['before']['events'][1]['event_hash']==old['e2_event_hash']
        assert response['decision_state']==old['response_decision_state'] and response.get('effect_kind')==old['response_effect_kind']
        assert d['after']['owner']==d['pre_read']['owner']
        cells.append(dict(cell=d['cell'],receipt=str(path.relative_to(R)),actor=state['actor_id'],claim=d['before']['claim'],memory_id=memory['memory_id'],memory_hash=memory['current_state_hash'],uncertainty=memory['uncertainty_state'],owner_hash_read=response['owner_state_hash_read'],source_events=d['before']['events'],epistemic_transition_ids=[x['transition_id'] for x in state['epistemic_transitions']],permission=state['permissions'].get(d['before']['claim']),decision=response['decision_state'],effect=response.get('effect_kind'),native_owner_after_equals_read=True,original_published_state_matches=True,committed=response['committed']))
    assert len(cells)==11
    save('09_CAUSAL_COUNTERFACTUAL_LEDGER.json',dict(cells=cells,independent_paired_adjudication='evidence/new/observations/causal_adjudication.json',full_channel_clamps='evidence/new/observations/clamp_*.json',native_sequence_evidence='evidence/new/observations/sequence_*.json',prior_history_comparator='evidence/new/observations/history_and_CAN3.json',estimand='Decision/effect projection only; full provenance hashes vary with memory',accessible_arm='Observed constructible memory-content -> stipulated access -> native permission -> authored response choice',unknown_arm='Fixed UNKNOWN active and withdrawn both DEFER; absent changes typed refusal only; access interventions can change outcome but do not satisfy original P3b',original_P3b='FALSIFIED',F_B='FIRED',general_serial_identification=False,operative_accepted_serial_rule=False,rules='UNISSUED'))
    # Source-attribution and finite-law analysis, without substituting candidate comments for law.
    quote='Trace refs may condition a private update but never establish conscious'
    native_text=(S/'runtime/candidate/owner_transitions.py').read_text();assert quote in native_text
    auth=(R/'staging/accepted_law/ADP017.txt').read_text();auth_md=(S/'runtime/runtime_root/law/ADP017_AUTHORITY_MD_RAW.txt').read_text();assert 'may condition a private update' not in auth and 'may condition a private update' not in auth_md
    adp=json.loads(auth)
    save('10_AUTHORITY_AND_DAG_LIMITS.json',dict(verdict='REVIEW_REVISE',authority_quote_correction=dict(author_F7_attribution='Accepted ADP017 blobeece4f3f; alleged quote may condition a private update',actual_source='CAN2 candidate/owner_transitions.py lines163-164; blobac943d07459f68ba2e27baf05b442d9ecbddefd5',exact_sentence_absent_from_pinned_accepted_ADP017_JSON_and_MD=True,accepted_belief_gate=adp['belief_gate'],accepted_memory_interaction=adp['memory_interaction']),consumer_exclusion='Full ctx contains memory; choice map authored to read permission. No explicit memory argument is not capability isolation. Hash/provenance may directly depend on memory.',history_control='MS1 prior_history is a tuple whose length enters prestate, not an independently verified prior-response journal; native CAN3 comparator remains separate',journal_limit='MS1 consume constructs receipt; committed=False. No verified response journal commit in this construct, despite prereg wording.',unknown_access_limit='A flat active/withdrawal contrast at UNKNOWN does not prove the structural graph has no mediated edge. Original F_B nevertheless fires by the frozen gate.',production='NO_ADOPTION; hypothetical mediator/consumer UNISSUED; issuer/destination authority and empirical psychology unproved'))
    # Comparative sources are documentary references, not falsely claimed reruns.
    refs=[('ee6a48b40247b113c614fe2099d4c443e8dd7bb7','CAN2 native source'),('ef12349defe22a50e053a7a8080a67ab45673417','CAN3 original independent history court'),('02187a14e75ff30dd953d3c7185d689b80e62304','M01 constructed parallel paths'),('0216d9036a87e2f60f42fd5b2870556027808419','M02 finite independent review'),('10a116f273c76095fca7255d4b6422a9ff3497a2','M06 finite ancestry review; no serial grant')]
    for sha,meaning in refs:assert git('cat-file','-t',sha).decode().strip()=='commit'
    save('11_COMPARATIVE_SOURCE_PINS.json',dict(refs=[dict(commit=s,meaning=m) for s,m in refs],scope='No new complete M01/M02/M06 suite rerun; independent native CAN3 comparator executed in MS2',no_MS1_author_conversation_access=True,no_helpers=True,no_model_switch=True))
    # Portable evidence redacts only host metadata. Preserve outcome/test/source preimages.
    receipts=json.loads((R/'evidence/PORTABILITY_RECEIPT.json').read_text())['files'] if (R/'evidence/PORTABILITY_RECEIPT.json').exists() else []
    for path in sorted((R/'evidence').rglob('*')):
        if not path.is_file():continue
        raw=path.read_bytes();out=clean(raw.decode()).encode()
        if out!=raw:
            receipts.append(dict(path=str(path.relative_to(R)),raw_sha256=hashlib.sha256(raw).hexdigest(),portable_sha256=hashlib.sha256(out).hexdigest()));path.write_bytes(out)
    save('evidence/PORTABILITY_RECEIPT.json',dict(policy='Personal paths/hostname presentation only; source, assertions, scientific data and outcomes unchanged',files=receipts))
    save('12_COMPLETION_AUDIT.json',dict(schema='MS2_REQUIREMENT_COMPLETION@1',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),matrix=matrix,reviewer_freeze=F,reviewer_scientific_RED_count=8,REDs_preserved_no_repair=True,original_case_names_and_outcomes_verified=True,native9_and_guard1_verified=True,actual_import_paths_verified=True,original_prereg_unchanged=True,original_P3b='FALSIFIED',F_B='FIRED',original_top_verdict_withheld=True,eleven_cells_actual_native_state_matches=True,source_and_authority_HOLDs_explicit=True,independence='Single reviewer previously M06; no MS1 implementation/conversation involvement',verdict='REVIEW_REVISE',adoption='NO_ADOPTION',publication='Commit, push and direct final remote SHA verification required after this content audit'))
    print('MS2_AUDIT_OK: original118P/2RED; new43P/8RED; literal P3b1RED; 11 cells match; REVIEW_REVISE')
if __name__=='__main__':main()
