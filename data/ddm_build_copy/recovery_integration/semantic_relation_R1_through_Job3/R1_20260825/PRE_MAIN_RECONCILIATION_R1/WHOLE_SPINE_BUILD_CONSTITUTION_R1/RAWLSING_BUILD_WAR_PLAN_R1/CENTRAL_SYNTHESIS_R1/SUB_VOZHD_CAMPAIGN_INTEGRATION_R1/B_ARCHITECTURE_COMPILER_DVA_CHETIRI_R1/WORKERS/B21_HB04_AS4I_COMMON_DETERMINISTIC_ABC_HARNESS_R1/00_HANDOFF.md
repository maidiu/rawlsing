# RABOCHII B21 — HB04 AS4I COMMON DETERMINISTIC A/B/C HARNESS IMPLEMENTATION R1

Repository:
`maidiu/rawlsing`

Branch:
`agent/rabochii-subv-b-as4i-common-deterministic-abc-harness-r1`

Exact starting HEAD:
`af9d863abba9579036885ee20486b0e27208792b`

Do NOT create a new branch.
Do NOT rebase.
Do NOT merge main/PRE-MAIN.
Do NOT execute C09.

Binding adjudication:
`49_B20Q3_ACCEPTANCE_ABC_INTAKE_FREEZE_AND_HB04_AUTHORIZATION_R1.md`

Frozen intake artifact:
`49A_HB04_QUALIFIED_ABC_INTAKE_FREEZE_R1.json`

Canonical intake JSON SHA-256:
`906973f78cd82678f678a9a803bb3c3c7f9e13b30e39a5f8dc3ea093d4390e88`

Authorized grain:
`B21_HB04_AS4I_COMMON_DETERMINISTIC_ABC_HARNESS_IMPLEMENTATION`

PASS terminal:
`AS4I_COMMON_DETERMINISTIC_ABC_HARNESS_IMPLEMENTATION_COMPLETE__READY_FOR_HB04_QUALIFICATION`

BLOCKER terminal:
`AS4I_COMMON_DETERMINISTIC_ABC_HARNESS_IMPLEMENTATION__EXACT_BLOCKER_PROVED`

This is implementation only. A PASS does not close HB04 and does not authorize C09.

## 1. Governing interface authority

Candidate definitions:
- HQ23 blob `bdf50129ac52a161dacd5859bc5b8bc60eaa65ac`

Common harness contract:
- HQ24 blob `7a6755f9e5c07329dca72619a29bc2e4dbc86a10`

Do not reinterpret either.

The smallest lawful implementation is a candidate-neutral common package, preferably under:

`rawlsing_next/as4/`

or the smallest equivalent namespace if repository import law proves another placement necessary.

## 2. Frozen candidate intake

### Route A
Definition:
`R5_LONG_COMPACT_V2__SERIAL_V4__AUDIT69__C05R2A_FACADE`

Qualification return:
`fa340c007f5f9d2835e6117daf1dc9545a173bc9`

Implementation blob:
`d4915e7e6755ba1850756aebff72f982f73a332b`

Qualification test blob:
`25e905868a21bb36035269065b7bc3640201b7d8`

Qualified execution tree:
`2dcabf4f67ac4f53433d66e13b946cef2e3ff6a0`

### Route B
Definition:
`SOURCE_BACKED_VIRTUAL_C11`

B16 production return:
`40a0a0529fa78765c7fc87f7e1f12260a2335f72`

Qualifying driver:
`f43c4be11d4f8fa98f538727337ec075d99d03bc`

Effective driver SHA-256:
`59ce6903776df5f5b17bc074b15d9ae06334a5a1c30fad91096fc3fb6a014a3f`

Final B16 production seal blob:
`0ebf319c0e6695b077b9ca70b9119007fecfcdcd`

B14 adapted driver:
- commit `de40c16dfb47fffca72bb095914957d0f6d30d0f`
- blob `ea1ec20e0e56a513b13388eeaf0a1c2e067dd9d9`
- SHA-256 `bbe732a1c07019e489900d36128c0e1d9b6d4dab5d81e3635ffc2f40dbc500f4`

B15 hostile return:
`d507e83058a20d087c3cdd64f6f6519a6524f6d1`

LiTS-I source identity pin:
`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

Do NOT open real LiTS-I in this implementation court.

### Route C
Definition:
`SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS`

Qualified intake identity:
`e8890b19ddcc9c1ee430fddcfd2cb47b8cccb2c3004975f03ec1f704e032ab10`

Driver:
- blob `9ed1a68300453bfcd4af4877bab397ed00b0e0e6`
- SHA-256 `497a9cb64fa4a1a57a3bf2ec6882aaf5fd996ea6408e7c7bbaf272fe534321ee`

Implementation:
- blob `abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889`
- SHA-256 `a07e73c514c6216c350ac7a69cb099256cf71680a49fe0796aac6729483b417d`

Exactly two accelerators only:
- CACC1
- CACC2

Do NOT add a third accelerator.

## 3. Frozen successor package

The common loader must consume the current successorized package:

- B13 seal `c041b7bbf17b9f494b4e3f59a6dd47ee078cb5b35c5c3593a404a2d6078903c3`
- runtime binding `8af38e94e1840b60461b1fead707332f250750295bb5902405836c77deb8ca5b`
- DiscoveryAuthority `2e153a153c59bd0b920f8db376478ad1b07000710e79a158471490c11b610cea`
- candidate grammar `7194b79298c97ff83575e43de472c0e0e1f1ba697d99c666dcba69266da51e06`
- official frontier `7aca4dbe1ccd36c48444d6858d378084e41aa30b3197662b6225753d5fc82e24`
- replay closure `45aeaba15ad003b0f734f7c54d68ec22de0e582840a8b239b4a58814e8ee4da1`
- predicate carrier blob `037ede5626fd0446328042db9aa8240ebcd24f26`
- query carrier blob `9a1a4886d148f94018023cd96ea99d684dbe2b15`
- 19 roles
- 18 distinct predicates
- 3 queries
- 21 distinct canonical objects
- sole alias `{A000,A1RAPP}`
- 82 candidates

Historical predecessor identities are negative fixtures only. They may not be treated as current.

## 4. Implement the common exact loader

Implement one exact loader that:
- reads only pinned/frozen identity material;
- validates the intake freeze before constructing sessions;
- reconstructs/validates DiscoveryAuthority and AuthorityRegistry material;
- reconstructs/validates all 19 role predicates / 18 distinct predicates;
- reconstructs/validates all 3 query templates;
- validates candidate grammar;
- validates official frontier;
- validates replay closure;
- validates common I03 manifest/target/measurement identities required by current authority;
- verifies exact content-addressed refs;
- fails closed on missing, stale, extra, malformed, or mismatched material;
- performs zero "latest" discovery;
- remints zero governed runtime objects.

Reuse banked constructors/carriers. Do not invent identity preimages.

## 5. Implement the candidate-neutral session protocol

Implement the HQ24 semantic surface:

`prepare(source, sealed_manifest, workdir) -> candidate_session`

Every A/B/C session must expose a common protocol equivalent to:
- `.repository` -> exact C11Repository surface;
- `.run_i03()`;
- `.run_i05()`;
- `.close()`;
- `.measurements`.

Route-specific wrappers may differ internally, but may not change semantic truth conditions or candidate definitions.

### A wrapper
Wrap the accepted Route-A source-backed adapter/runtime only.
Do not edit Route-A files.

### B wrapper
Wrap the accepted Route-B source-backed/RouteBSourceSession production seam and current successor package.
Do not redesign the source-backed architecture.
Do not open real LiTS-I in B21.

### C wrapper
Wrap the accepted Route-C accelerator implementation with exactly CACC1+CACC2.
Do not edit Route-C files.
Do not alter cacheless/accelerated identity law.

## 6. Implement deterministic runner surfaces

Required entry points:

`python -m rawlsing_next.as4.run_candidate --candidate A ...`

`python -m rawlsing_next.as4.run_candidate --candidate B ...`

`python -m rawlsing_next.as4.run_candidate --candidate C ...`

and:

`python -m rawlsing_next.as4.run_all ...`

Exact runner law:
- candidate identifiers are exactly A/B/C;
- source SHA must be verified before semantic execution;
- intake freeze and successor package are verified before candidate execution;
- each candidate execution occurs in a fresh subprocess;
- `run_all` executes sequentially in frozen order A -> B -> C;
- no overlapping candidate execution;
- each candidate gets a fresh workdir/scratch root;
- session `.close()` is guaranteed even on failure;
- cleanup state is receipted;
- machine-readable receipts are emitted;
- receipt surfaces bind exact candidate/intake/runtime refs;
- semantic results and replay identities are preserved exactly;
- resource observation fields must not alter semantic object identity or execution choice;
- no code path may rank, select, score, recommend, or stop based on comparative candidate performance.

## 7. Resource instrumentation

Implement only governed descriptive instrumentation needed by HQ24/C09 intake:
- wall/process timing where existing law requires;
- RSS/peak RSS where available under current repository law;
- scratch bytes;
- persistent bytes;
- file counts;
- relevant object/query/candidate counts.

If a metric is unavailable in a bounded fixture environment, represent it under existing NOT_APPLICABLE/BLOCKED law rather than inventing a value.

Instrumentation cannot:
- alter query/discovery semantics;
- change candidate order;
- skip a candidate;
- choose a candidate;
- enter semantic identity hashes where current receipt law excludes nondeterministic measurements.

## 8. Bounded implementation court

Do not use WVS7 or real LiTS-I.

Use bounded deterministic/synthetic fixtures and already-governed test material.

At minimum prove after committing implementation:

1. intake freeze verifies exactly;
2. each frozen Route A/B/C identity is bound;
3. current successor package reconstructs with zero remints;
4. all three adapters satisfy one protocol;
5. equivalent bounded semantic workload produces exact required parity across A/B/C where authority requires equality;
6. `run_candidate` runs in a child process and emits a valid receipt;
7. `run_all` launches exactly three fresh child processes sequentially A/B/C;
8. all three sessions close;
9. cleanup receipts are emitted;
10. resource instrumentation is descriptive only;
11. no ranking/selection fields or behavior exist;
12. no hidden transformed persistence or candidate-result cache is introduced.

Commit implementation BEFORE authoritative bounded execution.

## 9. Required hostile checks

At minimum fail closed on:
- wrong intake-freeze SHA;
- wrong Route-A implementation blob;
- wrong B16 Route-B production seal/driver pin;
- wrong Route-C qualified intake identity;
- historical predecessor runtime binding substituted for current;
- wrong DiscoveryAuthority;
- wrong grammar;
- wrong frontier;
- wrong replay closure;
- missing predicate carrier/object;
- missing query carrier/object;
- alias/cardinality violation;
- candidate other than A/B/C;
- source SHA mismatch;
- extra ungoverned accelerator request;
- attempt to supply a ranking/selection directive.

Do not weaken existing validators to make hostiles pass.

## 10. Allowed tracked write scope

Preferred:
- new files under `rawlsing_next/as4/`;
- new bounded tests under `rawlsing_next/tests/` specific to HB04;
- B21 receipts under this worker directory.

Existing Route A/B/C or shared engine files are read-only.

If an existing non-route common file must be changed, stop and prove why the new common package cannot lawfully own the behavior. Return a blocker rather than widening silently.

## 11. Hard stops

B21 must NOT:
- execute real C09;
- open/decode WVS7;
- open/decode real LiTS-I;
- benchmark A/B/C;
- rank/select/recommend candidates;
- alter A/B/C implementation semantics;
- alter shared I03/I05;
- alter candidate definitions;
- alter successor authority;
- add CACC3 or any third accelerator;
- launch HB05/HB06/HB07 as if already closed;
- launch OBL037;
- select OBL001/OBL002;
- enter positive V3;
- mutate central/PRE-MAIN/main.

## 12. Required outputs

Write under:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B21_HB04_AS4I_COMMON_DETERMINISTIC_ABC_HARNESS_R1/`

Required:
- `00_RETURN.md`
- `01_INPUT_FREEZE_IDENTITY_RECEIPT.json`
- `02_IMPLEMENTATION_IDENTITY_RECEIPT.json`
- `03_COMMON_LOADER_VALIDATION_RECEIPT.json`
- `04_CANDIDATE_INTERFACE_PARITY_RECEIPT.json`
- `05_RUNNER_FRESH_PROCESS_ORDER_AND_CLEANUP_RECEIPT.json`
- `06_HOSTILE_FAIL_CLOSED_RECEIPT.json`
- `07_HB04Q_OR_BLOCKER_HANDOFF.json`
- `CHANGED_FILES.txt`

If PASS, freeze:
- exact common harness implementation blob(s)/SHAs;
- exact bounded test blob(s)/SHAs;
- exact command(s);
- test counts;
- fresh-process evidence;
- no-real-source counts;
- no-ranking counts.

Then return only readiness for a separate qualification-only HB04Q court.

If blocked, identify the smallest exact layer and do not repair outside authorized common-package scope.

Return to SUB-VOZHD B.
