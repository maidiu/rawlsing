# GT12 E2B R3 — REAL CURRENT NO-LIBRARY EXECUTION R1

## Terminal

`PASS__GT12_FINAL_E2B_REAL_INTEGRATED_GT2_TO_V558__V3_DENY_ZERO_EFFECT`

## Working ancestry

Exact required start:

`62202de75aa8bbd73a0895730d19dba4c06658e2`

Branch:

`agent/rabochii-gt12-e2b-real-current-no-library-r3`

No empirical GT2 rerun, Library access, source-data access, authority rediscovery, authority redesign, or R4 reopening occurred.

## Write-ahead checkpoints

Checkpoint 1 — actual current input loaded and verified before downstream execution:

`e8c52bb5fb237338a7f0d0b420ef3932b9311627`

Checkpoint 2 — actual E2B runtime result banked before hostile/regression court:

`f18dae23e60c1ba761a6fa0bb82c44ece71a1a23`

Checkpoint 2 atomically replaced the one-shot execution court spec with the post-execution regression spec, preventing later CI synchronization from re-entering the real E2B chain.

## Actual accepted input

Loaded only through:

`load_current_gt2_query_fact()`

Exact current identities:

- predicate: `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3`
- query: `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0`
- fact: `540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46`
- replay: `c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f`
- state: `SUPPORTED`
- denominator: `19,210`
- semantic order: `Q86B -> Q86A`

## Actual production execution

Called the real current entry with query/fact only:

`run_current_r1c_e2b_actual_objects(query, fact)`

The entry internally consumed the adopted current publication/governance bundle:

`GT12_E2B_R3_CURRENT_V554_V557_PUBLICATION_GOVERNANCE_BINDING@1.0.0`

hash:

`f7d4d2313bcc70faf104cff205b0eb7aaa7d88556c895c8ea123a3725105cf14`

No caller-selected governed use, V554 rule, publication authority, or V557 authority was supplied.

## Runtime identity ledger

FIELD FORGE exact relation:

`1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19`

PRE-V3 admission:

`a445e43da99405e0f8181f7ab6c428d9b0dd14fefc7fc5091f21f2d21f00b08d`

Decision:

`ADMITTED`

Target-use permissions:

`("STRUCTURAL_MEDIATION_INPUT",)`

M1/V554 evaluation evidence hash:

`2d0acb74c8a1722ce339c7b014fb3e5eb630d4a88bee4e2560653d0efc13a036`

M1 state:

`ELIGIBLE`

Direct route:

`V554_TO_V557_DIRECT`

Direct publication object family:

`("F1",)`

Exact F1 root:

`a008553dc94af138de44e73ade8ddbcc1e2bb3a5c40cec575aad694aae104cbb`

V557 governance record:

`845522a7101f2632ac37d4fa1bbe15515ad29a0551a31570e4138796eaab48b6`

V557 state / uses:

`ALLOW_CONTEXT_ONLY / ("CONTEXT",)`

V557 publication bundle:

`2c7fb3f81343179ad75c6441fadcd09201aa47b9dc0e032383071e83cc4e022a`

V558 repository:

`47594be9aaf284122f76e3f2e3d74af29054ae3e1d6228134e4eccfdacfa46d1`

V558 query:

`73a47dcb4ab5497aadb16c1f3d074ef0e0203995e9d175b7fe5ee02b19cf2b54`

Requested uses:

`("CONTEXT",)`

V558 resolution receipt:

`730dbe577966b34587c5cb9ef3931ae83219cb62b945fdea6675a0cd53520b34`

Resolution:

`RESOLUTION_COMPLETE`

Resolved producer:

`V554`

Resolved uses:

`("CONTEXT",)`

Adopted permission binding hash:

`35381ce38e9cb6254c5f0c7608efcdc4a3f77c58313d433c6af74ff1ade5ab3d`

## V3 zero-effect proof

V3 decision evidence hash:

`216f8db74b89a7c168b0db0da91404e0fffb69d8b704710e59ec63a53d42d988`

Outcome:

`DENY_ZERO_EFFECT`

Reason:

`ZERO_POSITIVE_REGISTRY`

Pre/post state fingerprint is identical:

`5845b7d3e0be9c50accbc89ba56263fdd33b3b9832550857417efda962011723`

Exact deltas:

- actor state effect: `ZERO`
- causal-ledger appends: `0`
- causal cursor: `0 -> 0`
- RNG mutations: `0`
- scheduler mutations: `0`

No positive mutation occurred.

## Real execution evidence

Governed run:

`33987208384`

Job:

`101362897852`

Evidence execution SHA:

`cfec9665f2266f30f5f6b5435de9051fedae0310`

PR synthetic merge:

`c46bf8aa9eb39241005b3280a364d82fcf09f0a5`

Protocol:

`20 passed in 0.06s`

Real execution probe:

`1 passed, 1 evidence warning in 13.55s`

Receipt artifact:

`9975527389`

The warning is the intentional canonical runtime-evidence emission from the passing one-shot probe.

### Probe correction record

An earlier evidence probe run `33987156948` executed the real chain successfully but then failed on a test-only assertion that internal M1 `B1` must be absent.

That assertion was wrong: the adoption forbids **B1 publication**, not internal B1 existence. No production code changed. The corrected probe proves the direct V557 handoff contains exactly one `F1` root.

## Mandatory post-execution hostile/regression court

Governed run:

`33987310081`

Job:

`101363167802`

Evidence execution SHA:

`f18dae23e60c1ba761a6fa0bb82c44ece71a1a23`

PR synthetic merge:

`0d1f29070c375a32b34e7b02ec80a85f91a746ee`

Semantic candidate:

`62202de75aa8bbd73a0895730d19dba4c06658e2`

Protocol:

`20 passed in 0.08s`

Bounded hostile/regression court:

`221 passed in 20.86s`

Receipt:

- result: `PASS`
- exit code: `0`
- Python: `3.12.14`
- determinism: `EXACT`
- elapsed: `21.108262s`
- spec SHA-256: `f484b55e7eea49dbfbfc7f70da3c542f5409ed16aa67fe7ffbd1916549affab0`
- artifact ID: `9975557906`

The regression spec excludes the real execution probe, so this court does not re-execute E2B.

## Explicit non-actions

- empirical GT2 rerun: NO
- Library: NO
- source data: NO
- historical A3 substitution: NO
- synthetic authority substitution: NO
- authority rediscovery/redesign: NO
- final integrated hostile audit: NO
- GT1/GT2 adoption: NO
- PRE-MAIN movement: NO
- main movement: NO

## Final

`PASS__GT12_FINAL_E2B_REAL_INTEGRATED_GT2_TO_V558__V3_DENY_ZERO_EFFECT`
