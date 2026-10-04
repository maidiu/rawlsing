# PYAT HQ201 — execution-binding independent review — R1

Repository: maidiu/rawlsing

Role: independent source-free reviewer
Preferred model: DeepSeek V4.1 Flash

Branch:
agent/reviewer-pyat-hq201-r1

Review target clean tip:
35ffa48204672e6c7180cd010a7c1adde9f18cd7

Code-bearing execution-binding candidate:
b8b4c99633c4aa849fd79614c5bffbd1321209b8

Accepted session mechanism below it:
90ccbd54c549f67358d0c02ad18ff90b843cf3ee

Unsigned warrant successor to cross-check:
89054b882c04cf0541b6f9f4abdb555c808ad94d

Checkout mode:
SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ201-R9-EXECUTION-BINDING-INDEPENDENT-REVIEW-R1/
- /WORKER_RETURNS/PYAT-HQ201-R9-EXECUTION-BINDING-INDEPENDENT-REVIEW-R1/
- /rawlsing_next/
- /WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/
- /WORKER_RETURNS/EE-P2R6S/
- /WORKER_RETURNS/FIABC-LM2/

Read HQ201 adjudication by exact Git object:
2dcc9a2ed7cf9e11ae91e01e9d8030c6ca4b85eb:
PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ201_R9_BINDING_HARDENING_AND_F6F7_ONTOLOGY_R1.md

Do not clone. Do not create a full checkout.
Do not inspect the parallel HQ201 hardening return before fixing your own conclusion.

## Mission

Independently attack the HQ200 execution-binding candidate and determine whether it can actually realize the seven-source warrant successor.

Do not reopen the already accepted GovernedSourceSession mechanism unless the binding layer exposes a concrete contradiction in it.

## Required attack A — route-pass applicability

The warrant successor freezes:
- SRC27: governed_full_route_passes expected/max 1.
- SRC02/SRC06/SRC08/SRC12/SRC14/SRC26: governed_full_route_passes exact 0.

The candidate currently increments its outer pass count after every successful execute().

Test whether a non-route selected or metadata-only bound execution can:
- execute its admitted source operation;
- return full_route_passes_observed = 0;
- satisfy an outer exact-zero constraint.

A route-pass maximum of zero must mean:
"this source plan admits no FULL ROUTE PASS"
and must NOT mean:
"this source entry may perform no operation whatsoever."

If the current candidate cannot express that, record a material defect.

## Required attack B — failed attempt / retry law

The frozen seven-source plans carry retries max 0.

Exercise the PUBLIC BoundSourceExecution.execute() path.

Cause the first execution attempt to fail before successful completion, then call execute() again on the same bound execution.

Determine:
- whether a second source operation occurs;
- whether any lower-layer account moves;
- whether retries are measured separately;
- whether the second attempt is refused pre-operation when retries max 0.

Do not accept the existing court as proof if it calls GovernedSourceSession.run() directly instead of the wrapper.

Keep distinct:
- route-pass attempts;
- retries;
- completed route passes.

## Required attack C — postcondition failure and completed-pass truth

Construct a run where the source operation itself returns but a caller-bound post-operation EXACT/FLOOR constraint fails.

Determine whether full_route_passes_observed may truthfully increment before the postcondition is satisfied.

Use governing semantics, not convenience.

Record the required completion rule:
- operation-return success only; or
- whole bound execution including required postconditions.

Attack whether the candidate's current ordering is correct.

## Required attack D — dependency injection

BoundSourceExecution.__init__ accepts pyreadstat_module.

Verify whether the supplied module reaches GovernedSourceSession.

If the constructor accepts a dependency and silently discards it, classify the defect and determine whether it is merely testability or can affect exact runtime identity enforcement.

## Warrant compatibility

Read the exact successor at 89054b882c04cf0541b6f9f4abdb555c808ad94d and check whether the runtime can represent its seven outer-pass plans without reinterpretation.

Also verify:
- expected/floor/maximum/observed remain distinct;
- policy maxima cannot appear as historical expected values;
- chunk_reads cannot satisfy full_reads floor;
- decoder/path-open policy ceilings remain lower-layer accounts;
- source-dependent byte ceilings remain uninvented.

## Exact qualification

Run:
- execution-binding court;
- session court;
- broker court.

Then the exact R7 six-file court with:
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python

Environment:
PYTHONHASHSEED=0
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
PYTHONPATH=<review worktree root>

pytest:
-p no:cacheprovider

Collect exactly 55 and run twice. Record all exit codes. Do not retry away failures.

## Allowed dispositions

Exactly one:
- EXECUTION_BINDING_ACCEPTABLE__WARRANT_SUCCESSOR_COMPATIBLE
- EXECUTION_BINDING_PARTIAL__ROUTE_APPLICABILITY_REPAIR_REQUIRED
- EXECUTION_BINDING_PARTIAL__RETRY_COMPLETION_REPAIR_REQUIRED
- EXECUTION_BINDING_MATERIAL_DEFECTS__BOUNDED_REPAIR_REQUIRED
- R7_REQUALIFICATION_FAILURE
- WARRANT_RUNTIME_CONTRACT_CONFLICT

## Return

At minimum:
- 00_REVIEW.md
- 01_ROUTE_PASS_APPLICABILITY.json
- 02_ATTEMPT_RETRY_REVIEW.json
- 03_COMPLETION_SEMANTICS.json
- 04_INJECTION_REVIEW.json
- 05_WARRANT_COMPATIBILITY.json
- 06_R7_AND_COURTS.json
- 07_FINAL_DISPOSITION.json

Commit, push, re-fetch, verify local == remote.

Terminal:
HQ201_R9_EXECUTION_BINDING_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED

No locator discovery, real-source access, warrant issuance, live C4, C7 or actor/person work.
