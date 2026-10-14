import pathlib,json,hashlib,xml.etree.ElementTree as ET
R=pathlib.Path(__file__).resolve().parents[1]
selector=json.loads((R/'02_EXACT_COMPOSITE_SOURCE_SELECTOR.json').read_text())
rows=[]
for p in sorted((R/'repro').glob('*.xml')):
 suites=list(ET.parse(p).getroot().iter('testsuite'))
 counts={k:sum(int(s.attrib.get(k,0)) for s in suites) for k in ['tests','failures','errors','skipped']}
 rows.append(dict(file=str(p.relative_to(R)),**counts))
for name,n in [('independent',21),('candidate',24),('owners',111)]:
 row=next(x for x in rows if x['file']=='repro/'+name+'.xml')
 assert row['tests']==n and all(row[k]==0 for k in ['failures','errors','skipped'])
for p in (R/'repro').glob('*imports.json'):
 assert all(r['match'] for r in json.loads(p.read_text()))
for p in [R/'repro'/f'{name}_executed_sources.json' for name in ['independent','candidate','owners','cold_first','cold_replay']]:
 sources=json.loads(p.read_text());assert sources and all(r['match'] for r in sources)
owner_executed=json.loads((R/'repro/owners_executed_sources.json').read_text())
child_audits=[json.loads(p.read_text()) for p in (R/'repro/child_audits').glob('*.json')]
child_executed=[r for a in child_audits for r in a['executed']]
assert any('a04t_join_worker' in r['path'] for r in child_executed)
assert all(r['match'] for a in child_audits for r in a['imports']+a['executed'])
first=json.loads((R/'repro/cold_first.json').read_text());replay=json.loads((R/'repro/cold_replay.json').read_text())
assert first['durable_calls']==[3,3] and replay['durable_calls']==[0,0] and first['report']['links']==replay['report']['links']
assert hashlib.sha256((R/'01_FROZEN_ORIGINAL_IDENTITY_ORACLES.json').read_bytes()).hexdigest()=='1d551e0776e01e32a9c180f55ed2913a527f9e91a6c76278c8e923497304c5eb'
summary=dict(junit=rows,actual_executed_source_counts={n:len(json.loads((R/'repro'/f'{n}_executed_sources.json').read_text())) for n in ['independent','candidate','owners','cold_first','cold_replay']},all_imported_and_executed_pinned_sources_match=True,child_process_audit_count=len(child_audits),actual_helper_executed=list({r['path']:r for r in child_executed if 'WORKER_RETURNS/' in r['path']}.values()),candidate_source=next(r for r in selector['files'] if r['path']=='rawlsing_next/pre553_original_identity_v2k_successor_candidate.py'),cold=dict(first_calls=first['durable_calls'],replay_calls=replay['durable_calls'],identical_links=True,producer_setup_reconstructed=True))
(R/'repro/verification_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
table='\n'.join('| '+x['file']+' | '+' | '.join(str(x[k]) for k in ['tests','failures','errors','skipped'])+' |' for x in rows)
commands=[]
for f in ['execution.json','profile_execution.json','final_execution.json','cold_execution.json','child_execution.json']:
 raw=json.loads((R/'repro'/f).read_text());runs=raw if isinstance(raw,list) else raw['suites']
 commands.append('### '+f+'\n\n```json\n'+json.dumps(runs,indent=2)+'\n```\n')
report='''# Actual execution, commands, JUnit and failures

**EXECUTED:** fixed-composite local Python tests and independent cold replay. **NOT_EXECUTED:** raw original surveys, competent real original U/E/custody issuance, science/source-use admission, semantic adoption, canonical merge, full historical/full-estate suites beyond the five named selected owner suites, N9/N10E/N10W operative service, N11/N12 wake, V3 actor/model or V2/persona production.

## Runtime and selector

Bootstrap: `bash /Users/matthewsmith/.cache/rawlsing/prepare_sparse_worktree.sh /Users/matthewsmith/Desktop/as2b-lits1-DiSDJn/repository /Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent agent/reviewer-pyat-r3-postastra-pv-v2k-independent-r1 ce760f231cb5ae0678e39f9d12798997f8b6da27 /WORKER_COMMISSIONS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/ /WORKER_RETURNS/PYAT-R3-HQ295-V2K-ORIGINAL-IDENTITY-SUCCESSOR-R1/ /WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/ /rawlsing_next/ /AGENTS.md`. It fetched and matched the remote, created only the isolated assigned branch, and checked clean exact HEAD. No tracked AGENTS.md existed at the start tree. Read-only Git blob reads, source hashes and live branch comparisons are indexed in `documentary_sources_and_remote_cut.json`; resource telemetry is in `resource_preflight.json`.

`repro/run_court.py` reconstructs exact owner archive + candidate blobs, checks every materialized selected source against Git and SHA256, copies only the new independent test, and runs all three named suites in fresh subprocesses. Actual `PYTHONPATH` and cwd point exclusively to that isolated composite. A pytest plugin rejects foreign rawlsing_next module paths and records imported source paths/blob/SHA256; a Python profile hook separately records executed source files, and a read-only startup audit verifies actual helper execution/imports in child processes (`child_audits/`), including `a04t_join_worker.py`. All final imported/executed source bytes match the selector. Instrumentation adds overhead and is not a production latency measurement. No installed library source is upgraded into a project owner.

Reproduce from an exact checkout containing this return: `python3 WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/run_court.py`, then `python3 WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/run_cold.py`. Use a fresh copy of the return to preserve this run's evidence. The runtime locations in manifests are actual temporary execution terrain, not persistent production services. `repro/retry_independent.py` documents reviewer development reruns against the original isolated archive; final reproduction does not depend on those development retries.

## Every retained JUnit result

| Artifact | Tests | Failures | Errors | Skips |
|---|---:|---:|---:|---:|
'''+table+'''

The final 21 independent passes include affirmative observation of candidate limitations. They are not 21 semantic-adoption approvals. The 24 candidate and 111 owner tests are original unmodified suite files, checked against exact fixed Git blobs. Repeated runs are repeat verification, never extra independent proof. Full failure bodies and tracebacks remain in corresponding `.log` and `.xml`; no failure was hidden by a skipped/xfail marker. There are no skips/xfails in final named suites.

## Development and instrumentation diagnoses

- First independent run: 7 failed /14 passed. Reviewer constructed documentary discovery rows from the full dataclass serializer, preserving `query_ref:null`. The existing P01 adapter selects `raw.get('query_ref', raw.get('discovery_authority_ref'))`, so discovery became a foreign manifest unit. Changed only reviewer input serialization to omit optional None fields, consistent with owner input convention. Frozen roster/arithmetic/case hypotheses unchanged; no owner repair.
- Second independent run: 1 failed /20 passed. Reviewer assertion assumed flat `conditioner_ref`/`target_ref` export fields; actual material uses `roles.CONDITIONER.ref`/`roles.TARGET.ref`. Corrected assertion path, with the same exact refs and arithmetic. Both failed-run artifacts retained.
- Third independent run: 21 passed. Strengthened independent original key reconstruction before production; reran reviewer tests, still 21 passed.
- Added executed-file audit because dynamically loaded helper execution deserved evidence beyond normal sys.modules imports. First instrumentation pass missed path aliases (`/var` versus `/private/var`), yielding empty executed-source lists, even though imported-source hashes and all tests passed. These empty audit artifacts are retained as `pre_trace_*`; they are not claimed as executed-source proof. Resolved runtime path before instrumentation and reran all named suites. Final nonempty parent source audits cover in-process owners. The helper runs in child processes; parent profiling does not cover them. A further startup exec/import audit inherited by real child processes verifies the actual helper and every imported selected project source against the same selector. Its full 111-owner rerun and per-process receipts are retained; no owner code or verifier import blocker was changed.
- Original candidate and owner suites passed on every executed attempt here. The HQ295 worker's older failure history is distinct and is not counted as this reviewer's runs.

## Cold terminal

Two fresh independent processes, identical complete independently frozen preimages before producer reconstruction. First calls [3,3], replay [0,0], six exact same original/result/consumer links, two held rows. Actual logs/JSON/source audits in `cold_first*` and `cold_replay*`. No durable-call suppression monkeypatch and no worker positive emitter/fixture import. The synthetic producer reconstruction in both processes is explicitly retained; no claim of zero total computation.

## Exact commands and exit statuses

The following are the actual subprocess commands, working directories, elapsed times and terminal exit statuses. Shell entrypoints and the data-source reconstruction are saved as runnable scripts; output is actual stdout/stderr and pytest JUnit.

'''+ '\n'.join(commands)+'''
## Write and proof boundary

All new tracked files are under this own return and the one new independent test path. Candidate, published V2, owner code, frozen original tests and production CURRENT were not edited. `02_EXACT_COMPOSITE_SOURCE_SELECTOR.json` includes every materialized original source/test/helper Git blob and SHA256. `verification_summary.json` summarizes exact final terminals. The manifest binds saved evidence without a self-hash. Commit/push use only the assigned reviewer branch, and exact direct remote readback is reported outside the commit's own bytes.
'''
(R/'03_EXECUTION_COMMANDS_JUNIT_AND_FAILURES.md').write_text(report)
files={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(R.rglob('*')) if p.is_file() and p.name!='05_EVIDENCE_MANIFEST.json'}
(R/'05_EVIDENCE_MANIFEST.json').write_text(json.dumps(dict(schema='POSTASTRA_PV_RETURN_ARTIFACT_SHA256@1',files=files,independent_test_sha256=hashlib.sha256((R.parents[1]/'rawlsing_next/tests/test_postastra_pv_v2k_independent.py').read_bytes()).hexdigest(),self_excluded=True),indent=2)+'\n')
print(json.dumps(summary,indent=2)[:3500])
