from pathlib import Path
import json,hashlib,subprocess,xml.etree.ElementTree as ET,datetime
R=Path(__file__).resolve().parents[1];O=R/'04_ORIGINAL_NEW_REAL_JUNIT_COLD';C=R/'runtime/candidate_checkout';W=C/'WORKER_RETURNS/PYAT-R32-WP2-NATIVE-WORLD-POSSIBILITY-R1'
selected=json.loads((O/'independent_suite_results.json').read_text());assert len(selected)==12 and all(x['exit']==0 for x in selected)
labels=['independent_'+x['label'] for x in selected]+['wp2_unchanged','independent_science','independent_f6n_frozen_n8','independent_f6n_diagnostics','independent_f6n_frozen_l26']
suites=[]
for label in labels:
 p=O/(label+'.xml');tree=ET.parse(p);cases=list(tree.getroot().iter('testcase'));fail=[c for c in cases if c.find('failure') is not None];err=[c for c in cases if c.find('error') is not None];skips=[c for c in cases if c.find('skipped') is not None];suites.append(dict(label=label,file=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),testcase_events=sum(int(v.attrib['tests']) for v in tree.getroot().iter('testsuite')),xml_testcase_nodes=len(cases),failures=len(fail),errors=len(err),skips=len(skips),failing_nodes=[c.attrib for c in fail]))
core=suites[:13];assert sum(s['testcase_events'] for s in core)==597;assert all(s['failures']==s['errors']==s['skips']==0 for s in core)
assert suites[13]['testcase_events']==32 and suites[13]['failures']==0
assert [(s['testcase_events'],s['failures']) for s in suites[14:]]==[(8,0),(7,0),(26,2)]
summary=dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),core=dict(testcase_events=597,top_level_cases=586,unittest_subtests=11,failures=0,errors=0,skips=0),new_scientific_cases=32,additional_f6n=dict(frozen_n8='8 PASS',diagnostics='7 PASS',unchanged_l26='24 PASS / 2 legacy failures'),all_final_selected=dict(testcase_events=sum(s['testcase_events'] for s in suites),pass_events=sum(s['testcase_events']-s['failures']-s['errors']-s['skips'] for s in suites),failures=sum(s['failures'] for s in suites),errors=sum(s['errors'] for s in suites),skips=sum(s['skips'] for s in suites)),suites=suites,excluded_initial_harness_attempt='independent_science_initial.xml: 27 PASS / 2 harness assertion-placement failures. Native registry rejected the forged grant at construction, earlier than the reviewer expected. Final test catches the same typed refusal at construction. No scientific expectation or owner code changed.')
(O/'final_independent_test_selection.json').write_text(json.dumps(summary,indent=2)+'\n')
identity=json.loads((R/'02_ACTUAL_FULL_OWNER_IMPORTS_AND_SHAS.json').read_text());probe=json.loads((O/'independent_owner_import_probe.json').read_text());assert all(x['status']=='IMPORTED_NATIVE' for x in probe['results'])
identity['independent_owner_probe']=probe;diff=subprocess.check_output(['git','-C',str(C),'diff','--name-only'],text=True).splitlines();identity['candidate_tracked_changes_after_execution']=diff;assert not any(p.endswith('.py') for p in diff)
identity['original_python_tests_and_owners_unchanged_after_execution']=True
(R/'02_ACTUAL_FULL_OWNER_IMPORTS_AND_SHAS.json').write_text(json.dumps(identity,indent=2)+'\n')
cold=json.loads((O/'independent_cold_replay.json').read_text());assert cold['byte_identical'] and cold['distinct_processes'] and cold['author_product_equal_after_checkout_path_normalization']
(R/'00_INDEPENDENT_NATIVE_OWNER_VERDICT.md').write_text(f'''# WP2I independent native owner court

**Verdict: PASS for the bounded native sourcefree owner-to-consumer read.** The complete scientific opportunity/route model remains **HOLD: NAMED_N10W_RULE_HOLD**. This is independent executable review, not HQ adoption, production acceptance, real-source qualification or permission to install a model.

Reviewed author: `f7824794bc6674c662734c9a8b110dd3df224be7`. Commission: `ac8a11654a4192bf16485399c3a0be3eac555697`. Independent Phase A freeze: `947da9aa64d83ca8cd18cccfd037f12b049d1946`, committed, pushed and directly read back before opening candidate source/outputs. The precommit fixed the owner universe, pinned accepted E05S/F6N scientific contracts, exact condition/readset expectations and fourteen falsifiers. The exhaustive physical transport inventory was independently checked in Phase B; its enumeration is not represented as a preinspection freeze.

## Independently reproduced progress

- Full separate Git checkout at exact author HEAD: {identity['tracked_files']} tracked files, zero missing files, zero sparse skip entries. The review branch is a separate checkout at the sealed commission plus reviewer-only returns. The repositories use local Git object alternates; this is a full working tree, not an independently packaged offline object store.
- {len(identity['closure_records'])} declared transport records independently compared to exact commit:path Git preimages. All Python source/test bytes match. The only two initial nonmatching records are the already declared E05R/S generated trace JSONs, not immutable code. Additional unchanged F6N exports are recorded separately. Cold imports: 36 exact inherited native Python modules plus the WP2 transport module; physical `__file__`, Git blobs and SHA256 retained for both processes. Separate owner probes verify J04/RouteB/I4/FieldForge/F7 imports.
- Two independent cold interpreters PIDs {cold['runs'][0]['pid']} and {cold['runs'][1]['pid']} exit 0. Full output bytes match within this checkout: SHA256 `{cold['sha256_a']}`. Both reproduce 79 C1 returns, 28 public N10E returns, 180 M4 resolutions and 60 M5 materializations. Author product equivalence is exact after checkout-path normalization; the author's literal byte hash is not claimed because absolute profile filenames differ.
- Direct recount of the native synthetic rows confirms 18/32 → 10/16 → 6/8; opposite 11/26 → 6/12 → 4/6; independently authorized reverse 18/29. The AT07 native source table independently gives 54/60 forward, 54/62 reverse, changed law 54/70. Empirical-only changes yield 19/32 → 11/16 → 7/8, changed source/release/evidence refs and actual new values in both clients with the structural rule fixed.
- The unchanged original `NONPARENT_OPTIONS` and finite proposal evaluator read actual empirical cells and structural producer payloads. At the same selection clock, a changed published TEST_ONLY structural rule changes training eligibility, modeled exit constraint and institutional proposal feasibility while empirical objects and the two native-field readsets remain identical. Actual proposal-label changes preserve modeled results. Publication/effective boundary combinations, forged rehashed snapshots, stale consumer replay after revocation and forged grants are independently exercised.
- Independent rational standardization of F6 native stratum tables gives complete joint 13/25, 1/10, 1/10, 7/25 and model conditional 26/31 formal versus 5/31 informal. World B retains uncovered mass 1/5 and source-disagreement bounds. The excluded-source world keeps unknown mass 1/2, cell lower 1/8 and upper 5/8, refusing a full-target point distribution. No pooled/common-respondent joint is introduced.

## Actual tests and exceptions

The author's selected regression claim is independently reproduced: **597 PASS testcase events = 586 top-level cases + 11 unittest subtests; zero failures, errors or skips**. This includes unchanged E05/E04/N9C/M4/M5/C1/N10E/progressive, RouteB/I4/FieldForge/temporal admission, E05R/E05S, PE2, F6M and original F6 suites, plus WP2's 25 tests. This is regression coverage, not 597 distinct scientific decisions.

The reviewer adds **32 PASS** scientific tests implementing frozen falsifiers. Additional unchanged F6N tests give **8 PASS** (six exercise the repaired producer; two preserve original-stage hash/relative-transport controls), F6N post-freeze diagnostics **7 PASS**, and inherited F6L **24 PASS / 2 FAIL**. The two failures are preserved, not waived into passes: (1) the unchanged old producer assertion expects `fc5e37...`, whereas the commissioned repaired producer is `2df811...`; (2) the original mixed-origin test looks up absent fixture alias `P5B_MIXED_ORIGIN_CONTAMINATION` and never executes the behavior. The unchanged F6N diagnostics separately execute mixed-origin behavior against the exact repaired blob and refuse real-use promotion. This matches the declared legacy-exception boundary inherited from F6N; it prevents any all-suites-green claim.

All final selected XMLs total **668 PASS / 2 legacy FAIL**, zero errors/skips. The reviewer initially placed the forged-grant assertion after registry construction; the registry correctly refused earlier. The initial 27-PASS/2-failure XML and log remain retained, and the final test expects the same typed refusal at the earlier boundary. No accepted test or owner code was modified. See `04_ORIGINAL_NEW_REAL_JUNIT_COLD/final_independent_test_selection.json` for the exact counted selection.

## Scientific and authority ceiling

These are sourcefree synthetic risk sets, TEST_ONLY structural producer objects and separately carried GSS/NCA fixture values, not fresh Ghana survey/census reads, authenticated publisher grants, a measured causal policy, or anyone's personal chance. The synthetic structural and empirical scopes and the distinct GSS/NCA native units are not established as one scientifically compatible joined target. F6 remains an inferred sidecar with stated transport/conditional-invariance assumptions and unidentified conditional uncertainty; 26/31 is not a validated real-world opportunity probability.

The actual clients preserve `route_probability=None / NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL` and `selection_weight=None / NO_SCENARIO_SELECTION_MODEL_OR_ISSUER`. Sorok's envelope remains `UNINSTALLED_TEST_ONLY_PORT`; actor knowledge is `NOT_REQUESTED_NO_ACTOR_OWNER`. No actor or model executes. F7 imports and returns typed missing-readiness errors for an empty carrier; no comparable-wave output is available for this product. Import success and temporal admission fixtures do not establish a wave, J04 real-item grant or source authorization.

GF1E/GF1H are not imported. No original35 processing, source/person/FieldForge issuance, N11/N12/OC05/CAN008/V3, installation or canonical adoption is authorized or inferred. The independent native read may pass with this explicit downstream HOLD intact.

Replay and evidence: `07_REPLAY_AND_PROOF_LIMITS.md`, physical identity manifest 02, independent recomputations 03, actual XML/cold outputs 04, exact owner motion 05/06. Final publication is verified by direct remote readback in the chat and the publication receipt; no self-referential final-commit claim is embedded in this file.
''')
(R/'05_EXACT_N10W_RULE_HOLD_OR_REVISED_OWNER_GAP.md').write_text('''# Exact N10W rule hold

**Retain NAMED_N10W_RULE_HOLD.** Upstream native sourcefree read passes. No candidate defect found in the tested native read warrants replacing the inherited owners. This does not establish an authorized joint empirical-structural route model, scientific model-use permission, scenario-selection law, F6 installed binding or Sorok accepted port.

Owner: N10W structural-route possibility/model-use owner under competent HQ. Receiver: unchanged NONPARENT_OPTIONS reader and finite proposal evaluator; Sorok-facing envelope remains uninstalled.

Finite next decision: identify and justify an existing structural-route rule/model, exact allowed target and use, bind it to exact selected M4/M5 publication/effective refs and native C1/N10E evidence, and separately decide whether F6 remains a sidecar. Reconcile the distinct synthetic and native-field scopes rather than treating carriage as scientific compatibility. Source/model rights and actor knowledge require their actual owners.

Positive test before any later acceptance: two permitted structural rule refs at fixed empirical input and fixed selection clock must change the intended structured route output; same-rule relabeling must not. Empirical-only changes must rebind evidence with structural rule fixed. Test publication/effective/request clocks, source-specific withdrawal, minority and unknown mass, native units, actual consumer dereference and refusal of unissued model use. Route/selection probabilities require separately justified model authority; a deterministic modeled eligibility rule supplies no causal or personal probability.

Dependencies: competent owner decision, qualified target/permission bindings, independent review of any installed F6 linkage, a genuinely comparable F7 carrier if used, separate Sorok port and actor-knowledge acceptance if later commissioned.

Rollback: retain upstream receipts, keep all installation/model/actor flags false and route_probability/selection_weight null. This court does not launch the next phase.
''')
(R/'06_ACCEPTANCE_MOTION_NON_GRANTS.md').write_text('''# Independent acceptance motion, not adoption

Recommend accepting the bounded native sourcefree owner-to-consumer read method demonstrated at WP2 f7824794bc6674c662734c9a8b110dd3df224be7, subject to the explicit scientific and legacy-test limits in verdict 00. Retain N10W rule HOLD, F6 sidecar status and Sorok UNINSTALLED. Competent HQ decides any adoption; this reviewer has no installation or issuer authority.

The motion covers actual native C1/N10E/F8 and M4/M5 values read by the two original consumers, clock/revocation binding, independent rational arithmetic and two fresh process replays. It does not certify every untested request or hostile mutation, production service persistence, original-estate coverage, provider/source authority, real personal prediction, a measured causal rule, structural-route model-use, selection weights, any new comparable wave or actor knowledge.

No grants: original35/SAV/DTA, signed source, person, Field Forge, N11/N12, operative N9/N10W/OC05, CAN008, V3, canonical adoption. GF1E/GF1H remain held. The immutable original legacy failures remain failures; diagnostic behavioral evidence is reported separately.
''')
(R/'07_REPLAY_AND_PROOF_LIMITS.md').write_text('''# Replay and proof limits

Use Python 3.11 with pytest and the inherited pytest-subtests dependency. The working tree is a full private checkout; Git object alternates refer to the existing local shared store. No original data or external publisher/actor service is required. Two fresh interpreters are process independence at the same checkout, not a second provisioned machine or production restart/persistence proof.

The ignored `runtime/candidate_checkout` is a separate full Git checkout, remote https://github.com/maidiu/rawlsing.git, detached exact f7824794bc6674c662734c9a8b110dd3df224be7. Reconstruct it with an authenticated full/filtered private clone and exact checkout. All 8,600 candidate tracked files and its complete declared source transport closure were present. Review source is pinned independently to immutable Git preimages, not only the author's hashes. `runtime/f6n` is an exact git-archive export of WORKER_RETURNS/PYAT-R29-F6N-INDEPENDENT-NATIVE-F6-COURT-R1 from 3ef97b0708e8ffd082ee4569b629554e5353fe27. Source inventories/hashes for both are retained in 02; outputs, logs, tests and reviewer scripts are committed under the owned return. Candidate owner code is not duplicated into this publication.

From the review repository root:

1. `python3 -B WORKER_RETURNS/PYAT-R33-WP2I-INDEPENDENT-NATIVE-WORLD-R1/repro/verify_and_run.py` verifies source closure, runs two cold interpreters, unchanged WP2 tests and all original selected owner suites, then the owner import probe.
2. `python3 -B -m pytest -q WORKER_RETURNS/PYAT-R33-WP2I-INDEPENDENT-NATIVE-WORLD-R1/tests/test_independent_science.py --import-mode=importlib -p no:cacheprovider --junitxml=WORKER_RETURNS/PYAT-R33-WP2I-INDEPENDENT-NATIVE-WORLD-R1/04_ORIGINAL_NEW_REAL_JUNIT_COLD/independent_science.xml` runs the independent scientific checks.
3. Run `repro/run_f6n.py diagnostics`, `repro/run_f6n.py frozen_n8` and `repro/run_f6n.py frozen_l26` with python3 -B and this return's path prefix. The last command deliberately returns failure for the two unchanged legacy assertions; do not patch or count them as passes. It preimports WP2's exact repaired producer before loading unchanged original tests.
4. `python3 -B WORKER_RETURNS/PYAT-R33-WP2I-INDEPENDENT-NATIVE-WORLD-R1/repro/finalize.py` validates the selected JUnit accounting, immutable Python bytes and sourcefree evidence before writing the verdicts.

Actual cold command argv/PID/cwd/exits are retained. Each owner's JUnit/log is fresh from this checkout; no author XML is copied as independent evidence. Candidate script run_suites.py writes its outputs within the ignored candidate checkout; fresh outputs are then copied into reviewer evidence. Generated native trace JSONs are separate from immutable test/code bytes. The initial reviewer assertion-placement failure is retained separately and excluded from the final selected summary. Every test grouping's XML is individually hashed.

The Phase A oracle was frozen before candidate inspection; executable tests were subsequently implemented against its fixed falsifiers. No phase boundary authorizes model issuance, installation or a subsequent build phase. This is bounded test evidence and a non-granting acceptance motion, not an exhaustive security proof.
''')
print(json.dumps(summary['all_final_selected']))
