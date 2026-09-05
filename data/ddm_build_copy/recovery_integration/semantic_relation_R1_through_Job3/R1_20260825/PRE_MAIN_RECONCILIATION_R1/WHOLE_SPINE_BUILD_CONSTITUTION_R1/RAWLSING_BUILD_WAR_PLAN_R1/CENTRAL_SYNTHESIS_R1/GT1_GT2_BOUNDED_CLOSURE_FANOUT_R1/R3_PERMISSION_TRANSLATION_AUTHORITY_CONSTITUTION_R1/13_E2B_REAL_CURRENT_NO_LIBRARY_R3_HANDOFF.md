# GT12 E2B R3 — REAL CURRENT NO-LIBRARY EXECUTION R1

Repository:

`maidiu/rawlsing`

Worker branch:

`agent/rabochii-gt12-e2b-real-current-no-library-r3`

Exact working-ancestry start:

`62202de75aa8bbd73a0895730d19dba4c06658e2`

This instruction commit is evidence only. Working ancestry begins exactly at the SHA above.

Profile:

`REAL_EXECUTION -> VERIFY_REGRESSION -> CLOSURE_ONLY`

## Purpose

Execute the actual current GT2 object through the now-implemented and independently-audited production E2B path.

Do not rediscover authority.
Do not redesign.
Do not rerun empirical GT2.
Do not use Library/source data.
Do not reopen R4.
Do not run a broad final audit in this worker.

The only purpose of this worker is:

`real current query/fact -> actual E2B path -> exact V558 CONTEXT resolution -> V3 DENY_ZERO_EFFECT`

## Frozen accepted input

Load via:

`load_current_gt2_query_fact()`

Required exact identities:

- predicate:
  `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3`
- query:
  `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0`
- fact:
  `540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46`
- replay:
  `c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f`
- state:
  `SUPPORTED`
- denominator:
  `19,210`
- semantic order:
  `Q86B -> Q86A`

## Frozen accepted current publication/governance bundle

Real production provider:

`load_current_gt12_e2b_publication_governance_binding()`

Exact bundle:

`GT12_E2B_R3_CURRENT_V554_V557_PUBLICATION_GOVERNANCE_BINDING@1.0.0`

hash:

`f7d4d2313bcc70faf104cff205b0eb7aaa7d88556c895c8ea123a3725105cf14`

Exact publication family:

`("F1",)`

Exact V557 state:

`ALLOW_CONTEXT_ONLY`

Exact V557/V558 uses:

`("CONTEXT",)`

The real current entry is:

`run_current_r1c_e2b_actual_objects(query, fact)`

and accepts only query/fact. Caller-selected publication/governance inputs are forbidden.

## First action

1. verify branch HEAD exactly;
2. read only this handoff;
3. inspect only:
   - current repo-native query/fact loader;
   - real E2B entry;
   - adopted publication/governance provider;
   - directly invoked FIELD FORGE / PRE-V3 / M1-V554 / V557-V558 / V3 guard surfaces;
4. load the actual current objects;
5. verify exact identities;
6. immediately persist a nonterminal current-input checkpoint before executing the downstream chain.

Do not perform broad historical orientation.

## Exact chain

Execute only:

`load_current_gt2_query_fact()`

-> ordinary current `EmpiricalQuerySpec` + `EmpiricalFact`

-> `run_current_r1c_e2b_actual_objects(query, fact)`

which must internally traverse:

FIELD FORGE exact conditional-support relation
-> PRE-V3 relation admission
-> relation M1 / V554
-> adopted publication/governance bundle
-> adopted PRE-V3->M4 permission descent
-> V557
-> V558
-> V3 zero-positive guard

## Required terminal semantics

FIELD FORGE:
- exact count-only relation;
- Q86B conditions Q86A;
- exact 19,210 risk set;
- actor-independent;
- no causal meaning.

PRE-V3:
- `ADMITTED`;
- target use `STRUCTURAL_MEDIATION_INPUT`.

M1/V554:
- exact relation-specific SIG-004 route;
- publication root family exactly `F1`;
- direct route `V554_TO_V557_DIRECT`.

Permission descent:
- `STRUCTURAL_MEDIATION_INPUT -> CONTEXT`;
- producer uses exactly `("CONTEXT",)`.

V557:
- exact current adopted V557 AuthorityRef;
- decision `ALLOW_CONTEXT_ONLY`;
- allowed uses exactly `("CONTEXT",)`.

V558:
- requested uses exactly `("CONTEXT",)`;
- result `RESOLUTION_COMPLETE`;
- resolved producer family exactly `V554`.

V3:
- exact outcome `DENY_ZERO_EFFECT`;
- `zero_effect == true`.

## Write-ahead checkpoint law

Persist two checkpoints.

### Checkpoint 1 — actual current input loaded

Immediately after exact current query/fact/replay/predicate verification, persist a bounded checkpoint recording those identities.

Do not proceed to E2B execution before this checkpoint is durable.

### Checkpoint 2 — actual E2B runtime result

Immediately after the real downstream chain returns successfully, persist exact identity-bearing runtime evidence BEFORE running broad regressions or writing the final return.

At minimum record exact refs/hashes for:

- FIELD FORGE relation;
- PRE-V3 admission;
- M1 evaluation;
- F1 publication root(s);
- V557 governance record(s);
- V557 publication bundle;
- V558 repository;
- V558 query;
- V558 resolution receipt;
- V3 decision.

Also record the exact adopted publication/governance bundle hash used.

A tool/process loss after this point must not require re-running the actual E2B chain.

## Zero-effect proof

Record exact pre/post state fingerprints for:

- actor state;
- causal ledger;
- causal cursor;
- RNG state;
- scheduler state.

Prove no positive mutation.

The exact expected terminal is:

`V3 DENY_ZERO_EFFECT`

No actor mutation.
No causal-ledger append.
No cursor change.
No RNG change.
No scheduler change.

## Mandatory hostile/regression court after checkpoint 2

After the real runtime checkpoint is durable, run one governed bounded court containing the smallest relevant set proving:

1. exact current repo-native query/fact load;
2. exact current-object boundary;
3. adopted publication/governance binding;
4. real E2B actual-object harness;
5. FIELD FORGE conditional support;
6. PRE-V3 admission;
7. C->D relation bridge;
8. relation M1/V554;
9. permission translation/descent;
10. V557/V558 repository/resolution;
11. typed-negative conservation;
12. V3 zero-positive guard.

Also prove hostile rejection of:

- historical A3;
- wrong query/fact/replay;
- reversed Q86 target order;
- wrong risk set;
- non-SUPPORTED / OBSERVED_ZERO promotion;
- F2/B1 publication;
- V553/V555/V556 substitution;
- REVIEW;
- ACTIVE_CAUSAL;
- widened V557/V558 uses;
- wrong publication/governance bundle;
- actor/V3/V2 reverse material.

Do not run unrelated tests for count inflation.

## Required return

Commit:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/E2B_REAL_CURRENT_NO_LIBRARY_R3/00_RETURN.md`

and bounded machine-readable execution evidence sufficient for the final independent audit delta.

## PASS terminal

Only if the actual current ordinary objects traverse the real production chain successfully and V3 returns exact zero effect:

`PASS__GT12_FINAL_E2B_REAL_INTEGRATED_GT2_TO_V558__V3_DENY_ZERO_EFFECT`

Otherwise return the smallest exact blocker.

## Explicit non-actions

- no empirical GT2 rerun;
- no Library;
- no source data;
- no new authority;
- no authority redesign;
- no synthetic authority substitution;
- no final integrated hostile audit;
- no final GT1/GT2 adoption;
- no PRE-MAIN movement;
- no main movement.

After this worker returns, HQ will combine its runtime evidence with the already-completed final hostile-audit preflight and commission only the tiny remaining E2B audit delta.
