# PYAT HQ201 — execution-binding bounded hardening — R1

Repository: maidiu/rawlsing

Role: source-free implementation worker — Space Bunny

Branch:
agent/rabochii-pyat-hq201-r1

Implementation base / HQ200 candidate:
35ffa48204672e6c7180cd010a7c1adde9f18cd7

Code-bearing candidate:
b8b4c99633c4aa849fd79614c5bffbd1321209b8

Accepted session mechanism:
90ccbd54c549f67358d0c02ad18ff90b843cf3ee

Checkout mode:
SPARSE_REQUIRED

Materialize only:
- /WORKER_COMMISSIONS/PYAT-HQ201-R9-EXECUTION-BINDING-HARDENING-R1/
- /WORKER_RETURNS/PYAT-HQ201-R9-EXECUTION-BINDING-HARDENING-R1/
- /rawlsing_next/
- /WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/
- /WORKER_RETURNS/EE-P2R6S/
- /WORKER_RETURNS/FIABC-LM2/

Read:
- HQ201 adjudication at 2dcc9a2ed7cf9e11ae91e01e9d8030c6ca4b85eb
- unsigned warrant successor at 89054b882c04cf0541b6f9f4abdb555c808ad94d

Do not clone. Do not create a full checkout.
Do not inspect the parallel reviewer return before completing your own repair.

## Mission

Repair only the bounded execution-binding defects identified by HQ201.

Do not change the accepted seven-source authority.
Do not hard-code SRCxx policy into production.
Do not touch real sources.

## Repair 1 — outer route-pass applicability

Current execute() treats every successful source execution as one full_route_pass.

That is wrong for the warrant successor:
- six plans have full_route_passes EXACT 0 but must still execute metadata/selected work;
- SRC27-shaped FULL Route-B plan has full_route_passes EXACT/MAX 1.

Make route-pass applicability explicit in the immutable bound spec.

Required semantics:

### non-route execution
A caller must be able to bind:
- route-pass not admitted/applicable;
- expected outer count 0 where authority supplies zero.

The source plan must still execute normally.

On success:
- full_route_passes_observed = 0;
- full_route_passes_completed_successfully = false or another truthful typed non-applicable representation;
- lower-layer accounts reflect the actual metadata/selected/etc work.

A route-pass maximum of 0 MUST NOT mean "no source operation".

### route execution
When route-pass is explicitly admitted:
- the full Route-B outer account is active;
- expected/max are enforced separately from lower layers;
- completion increments only under the completion law below.

Do not infer applicability from source key.
If you infer it from plan mode, prove the mapping is generic and does not make every FULL operation a Route-B pass.
Prefer explicit caller-bound applicability.

## Repair 2 — attempts, retries, completed passes

Keep these separate:

- route_pass_attempts
- retries
- completed_route_passes

For a route-applicable bound execution:

First attempt:
- attempt count begins;
- retry count remains 0.

If it fails before full bound-execution completion:
- completed passes remains 0.

If retries max 0:
- a second execute() attempt must be refused PRE-OPERATION;
- no identity/hash/metadata/row account may move.

If retries >0 is generically supported:
- each additional admitted attempt must increment the separate retries account under its own budget before source work;
- retry ceiling is checked pre-operation.

Do not silently use completed-pass count as an attempt counter.

The existing SourceAccessAccount.retries field is the lower-layer retry account. Use it truthfully or state/implement a single exact owner; do not create two incompatible retry counts.

SourceOperationPlan.max_retries and SourceAccessBudget.retries must not become divergent silent knobs. Establish one binding law or fail closed on mismatch.

## Repair 3 — completion ordering

A route pass counts as completed only after the WHOLE bound execution succeeds, including all caller-supplied required exact/floor postconditions.

Therefore:
- run source operation;
- evaluate bound lower-layer postconditions;
- evaluate outer expected rule;
- only then report/increment completed route pass.

If a postcondition fails:
- route_pass_attempts reflects the attempt;
- completed route passes stays 0 for that attempt;
- retry law controls whether another attempt is possible.

Do not report a postcondition-failed execution as a completed governed pass.

## Repair 4 — pyreadstat_module wiring

BoundSourceExecution currently accepts pyreadstat_module but discards it.

Either:
- store and pass the exact supplied module into GovernedSourceSession; OR
- remove the public parameter completely and update courts/API honestly.

Prefer preserving deliberate dependency injection if it is useful for exact seam/identity courts.

No silent ignored argument.

## Required courts

Add focused courts proving at minimum:

1. metadata-only non-route execution succeeds with outer EXACT 0 and observed 0;
2. selected non-route execution succeeds with outer EXACT 0 and observed 0;
3. route-applicable FULL execution gives outer EXACT/MAX 1;
4. non-route max0 does not block source work;
5. route max0 blocks before creating a session;
6. failed first wrapper execute + retries0 => second wrapper execute refused with all source accounts unchanged;
7. attempt/retry/completed counts are distinguishable;
8. postcondition failure leaves completed route passes unchanged;
9. second attempt after postcondition failure obeys retry0;
10. retry account cannot exceed its ceiling;
11. plan/budget retry knobs cannot silently disagree;
12. pyreadstat_module injection is actually observed, or parameter is absent;
13. chunk_reads cannot satisfy full_reads floor;
14. lower-layer expected/floor/max/observed law remains intact;
15. no source-specific production constants.

Use synthetic carriers only.

## Seven-plan compatibility court

Instantiate the seven DOCUMENTARY PLAN SHAPES in tests.

For six non-route shapes:
- execute successfully;
- outer pass observed = 0;
- exact-zero satisfied.

For the SRC27-shaped route:
- outer expected/max1;
- full_reads floor1;
- decoder max1 policy;
- retries max0;
- no header prefix;
- second route attempt refused pre-operation.

Production remains source-agnostic.

## Exact requalification

Run:
- hardening execution-binding court;
- source-session court;
- broker court.

Then exact R7 court using:
/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv/bin/python

Environment:
PYTHONHASHSEED=0
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
PYTHONPATH=<worktree root>

pytest:
-p no:cacheprovider

Collect exactly 55; run twice; target 55/55 twice.
Do not retry away failures.

## Write terrain

Only:
- rawlsing_next/pre553_execution_binding.py
- rawlsing_next/tests/test_pre553_execution_binding_court.py
- rawlsing_next/pre553_source_access_broker.py if strictly required for truthful retry accounting
- rawlsing_next/pre553_source_session.py if strictly required for retry binding law
- directly corresponding tests if either accepted module must change
- WORKER_RETURNS/PYAT-HQ201-R9-EXECUTION-BINDING-HARDENING-R1/**

No unrelated production files.

## Allowed dispositions

Exactly one:
- EXECUTION_BINDING_HARDENED__READY_FOR_FINAL_INDEPENDENT_ACCEPTANCE
- EXECUTION_BINDING_PARTIAL__SPECIFIC_DEFECT_REMAINS
- RETRY_ACCOUNT_MODEL_CONFLICT__HQ_ADJUDICATION_REQUIRED
- R7_REQUALIFICATION_FAILURE
- MATERIAL_NEW_COUNTEREXAMPLE

No self-adoption.

Commit, push, re-fetch, verify.

Terminal:
HQ201_R9_EXECUTION_BINDING_HARDENING_RETURNED__HQ_REVIEW_REQUIRED

No locator discovery, real-source access, warrant issuance, live C4, C7 or actor/person work.
