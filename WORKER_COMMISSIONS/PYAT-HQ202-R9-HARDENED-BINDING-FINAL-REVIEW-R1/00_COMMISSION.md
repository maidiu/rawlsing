# PYAT HQ202 — R9 hardened execution-binding final independent review — R1

Repository: maidiu/rawlsing

Role: independent source-free reviewer
Preferred model: DeepSeek V4.1 Flash

Branch:
agent/reviewer-pyat-hq202-r1

Exact review target / commissioned base:
deea40541cda0627d129dcb7d30e06e0682e0fed

Pre-hardening candidate:
35ffa48204672e6c7180cd010a7c1adde9f18cd7

Accepted session mechanism:
90ccbd54c549f67358d0c02ad18ff90b843cf3ee

Accepted documentary warrant successor:
89054b882c04cf0541b6f9f4abdb555c808ad94d

Checkout mode: SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ202-R9-HARDENED-BINDING-FINAL-REVIEW-R1/
- /WORKER_RETURNS/PYAT-HQ202-R9-HARDENED-BINDING-FINAL-REVIEW-R1/
- /rawlsing_next/
- /WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/
- /WORKER_RETURNS/EE-P2R6S/
- /WORKER_RETURNS/FIABC-LM2/

Read HQ202 adjudication by exact Git object:
329a37455151f479886bd3cbb40d4d98d016fb13:
PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ202_R9_FINAL_REVIEW_AND_F6F7_CONSTITUTION_WAVE_R1.md

Do not clone. Do not create a full checkout.

## Mission

Independently review the HARDENED candidate, not the old HQ200 candidate.

Reproduce the four old defects first against the pre-hardening candidate if useful, then prove or falsify their repair at deea4054.

### A — route-pass applicability
Verify explicit caller-bound applicability is real and not inferred from source key or row-data mode.

Prove:
- a metadata-only non-route execution can run with outer EXACT 0 and observe 0;
- a selected non-route execution can run with outer EXACT 0 and observe 0;
- a FULL plan can still be NOT_APPLICABLE and observe outer 0;
- route max0 blocks an APPLICABLE route before session/source operation;
- non-route max0 does not block underlying source work;
- an incoherent NOT_APPLICABLE + exact1 spec fails before access.

### B — attempts/retries/completions
Use public BoundSourceExecution.execute() only.

Prove:
- first admitted attempt is not a retry;
- failed first attempt + retries0 => second execute refused pre-operation;
- refused attempt moves no source account;
- attempt, retry and completed-pass counters are distinct;
- retry count is the existing SourceAccessAccount.retries account;
- SourceAccessBudget.retries owns the ceiling;
- SourceOperationPlan.max_retries cannot silently disagree;
- retries >0, if supported, advance exactly and stop at the ceiling.

Attack failure before session creation as well as failure after session creation. A retry gate must not create unauthorized source activity merely to account the retry.

### C — completion semantics
Construct:
- source operation success + lower-layer postcondition failure;
- source operation success + outer exact failure.

Verify neither is reported as a completed route pass.

Completion must occur only after all required postconditions.

### D — dependency injection
Supply a controlled pyreadstat module/stub and prove the exact supplied object reaches the session/broker seam and is consulted. No silently ignored parameter.

### Seven-source warrant compatibility
Against 89054b88... prove:
- six non-route plan shapes can execute with full_route_passes exact0;
- SRC27-shaped route exact/max1 executes once;
- full_reads floor1 remains distinct;
- decoder/path-open maxima remain policy only;
- retries max0 works;
- no prefix on SRC27-shaped route;
- second route attempt refuses pre-op;
- source-dependent byte ceilings remain uninvented.

### Qualification
Run hardened binding court, session court, broker court.

Run exact R7 six-file court using:
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python

PYTHONHASHSEED=0
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
PYTHONPATH=<worktree root>
pytest -p no:cacheprovider

Collect exactly 55; run twice; target 55/55 twice. Record every exit code.

## Allowed dispositions
Exactly one:
- ACCEPT_HARDENED_EXECUTION_BINDING__SOURCE_FREE_R9_RUNTIME_COMPLETE_AT_BINDING_GRAIN
- HARDENED_BINDING_MATERIAL_DEFECT
- RETRY_MODEL_STILL_UNSOUND
- WARRANT_RUNTIME_CONTRACT_CONFLICT
- R7_REQUALIFICATION_FAILURE

Return at minimum:
00_REVIEW.md
01_ROUTE_APPLICABILITY.json
02_RETRY_ATTEMPT_COMPLETION.json
03_INJECTION.json
04_WARRANT_COMPATIBILITY.json
05_R7_AND_COURTS.json
06_FINAL_DISPOSITION.json

Commit, push, re-fetch, verify local == remote.

Terminal:
HQ202_R9_HARDENED_BINDING_FINAL_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED

No locator discovery, real-source access, warrant issuance, live C4, C7 or actor/person work.