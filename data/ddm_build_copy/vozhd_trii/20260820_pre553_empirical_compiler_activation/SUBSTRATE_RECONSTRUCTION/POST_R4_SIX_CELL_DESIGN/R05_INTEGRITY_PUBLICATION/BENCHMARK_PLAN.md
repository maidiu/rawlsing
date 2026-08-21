# R05 BENCHMARK / PROOF PLAN — INTEGRITY, REPLAY, PUBLICATION, CACHE

Status: `DESIGN_PROOF_PLAN_ONLY__NO_PERFORMANCE_CLAIM`

No benchmark result is asserted by this R05 return. This plan defines the courts a future implementation must pass before hierarchical/lazy verification can be accepted.

## 1. PURPOSE

Measure whether hierarchical root/member/chunk verification provides useful bounded reopen/query behavior **without** weakening current R4 integrity expectations.

Correctness gates are binary and precede latency/storage evaluation. A faster run that emits evidence from an unverified/incompletely closed dependency set is a failure, not a performance result.

## 2. FIXED PRECONDITIONS

Before benchmarking, freeze:

- semantic fixture/corpus and exact expected C11 reconstruction;
- root/member manifest schema and canonical serialization;
- hash algorithms/domain separation;
- chunking/row-group profile;
- cache schema and builder implementation identity;
- active-root authorization law;
- exact query-closure dependency law;
- publication substrate and its atomic/durability contract;
- whether the physical profile is `BYTE_REPRODUCIBLE`.

Use synthetic/checked-in bounded hostile fixtures first. Raw source is not required to validate R05 mechanics.

## 3. REQUIRED MEASUREMENTS

For every court record:

- exact semantic and physical root IDs;
- canonical bytes touched;
- canonical bytes cryptographically verified;
- number of root/member/chunk hashes evaluated;
- verification closure cardinality by member/chunk;
- cache bytes touched and whether cache was bypassable;
- wall time separately for verification, query/reconstruction, and total;
- peak RSS;
- scratch bytes;
- empirical result hash;
- verification state reached;
- expected versus actual failure classification;
- proof that no positive/negative output escaped on failed closure/integrity.

## 4. STORAGE ACCOUNTING

Report exactly the categories required by existing storage law:

1. `CANONICAL_STEADY_STATE_BYTES`
2. `ATOMIC_STAGING_PEAK_BYTES`
3. `SCRATCH_EXECUTION_PEAK_BYTES`
4. `NONAUTHORITATIVE_CACHE_BYTES`
5. `POST_SUCCESS_RETAINED_BYTES`

Additionally report:

- root-manifest bytes;
- member-manifest bytes;
- whole-member hash metadata bytes;
- chunk/Merkle metadata bytes;
- bytes per chunk descriptor;
- number of chunks/members;
- percentage integrity-metadata overhead versus canonical payload.

No staging/cache/scratch byte may be silently counted as or retained with canonical steady state.

## 5. BASELINE

### B00 — current full integrity path

On the same fixture, run the current-equivalent:

- root/member open;
- whole-member hash verification;
- streaming full audit;
- exact query/reconstruction.

This is the integrity baseline hierarchical verification must not weaken.

## 6. NORMAL-PATH COURTS

### B01 — cold root open

Fresh process, empty cache.

Measure root-manifest authorization and member-manifest verification only. Confirm no empirical query result is authorized merely by this open.

### B02 — narrow positive atomic query

Query one exact fact with a deliberately narrow dependency closure.

Pass only if:

- all fact/state/identity/provenance/default/exception dependencies are verified;
- untouched canonical regions are proven irrelevant by root-bound coverage law;
- result equals full-audit baseline exactly.

Measure potential savings in verified bytes versus full audit.

### B03 — exact negative query

Choose a query with no qualifying evidence whose governed search domain spans many partitions/chunks.

Pass only if:

- every refuting region is verified; or
- a verified root-bound canonical completeness structure proves a smaller exhaustive domain;
- a cache/index miss alone never completes closure;
- result equals full-audit baseline.

Expected outcome may legitimately approach full-release verification. That is evidence about the cost of exact negative truth, not a reason to weaken the gate.

### B04 — aggregate / denominator / weight / uncertainty

Exercise:

- physical missingness;
- semantic response state;
- routing/applicability/risk-set rules;
- weights/design/measure authority;
- sparse overrides.

Pass only if closure includes every canonical dependency capable of adding/removing/reweighting/reclassifying contributors and matches baseline exactly.

### B05 — arbitrary respondent conjunction

Use multiple variables whose relevant facts lie in distinct physical regions.

Verify exact incidence/intersection and negative respondent exclusions. Compare with full canonical result.

### B06 — I05 unforeseen combination

Construct a lawful bounded combination intentionally absent from any prebuilt speed index/cache.

Pass only if canonical fallback still discovers it. A faster false-negative discovery result is an integrity failure.

### B07 — repeated query in same process

Repeat B02-B06 without process restart.

Transient verified immutable buffers/query-closure state may reduce work only if they remain bound to the exact immutable root and cannot be invalidated by path mutation. Record reuse explicitly.

### B08 — repeated query in new process

Restart completely while leaving any persistent verification hint/cache present.

Pass only if prior-process `verified=true` or cache state does not substitute for current cryptographic authorization. Measure reopened verification work honestly.

### B09 — streaming full release audit

Verify every canonical member byte and reconstruct/audit full fixture by bounded streaming.

This path is mandatory even if B02-B08 are fast. It must detect every injected canonical corruption.

## 7. CACHE COURTS

### C01 — no-cache correctness

Delete all non-authoritative caches and rerun B02-B06.

Every exact result must be identical. Any correctness dependency on cache reclassifies that material as canonical or fails the design.

### C02 — cold cache build

Build each accelerator only from a verified canonical root. Record source root/member dependencies and builder/schema/config identities.

### C03 — root invalidation

Switch to a different authorized root with otherwise similar shape.

Old cache must not affect a result. It must be ignored/deleted/quarantined/rebuilt under the new key.

### C04 — builder/schema/config invalidation

Change each cache dependency independently. Prove old cache is not reused.

### C05 — cache corruption

Flip cache bytes. Canonical exact result must remain obtainable; corrupted cache is ignored/deleted. Cache corruption must not quarantine healthy canonical material.

### C06 — cache false positive

Inject extra candidate into cache. Canonical verification must reject it and invalidate/cache-correct behavior without changing canonical truth.

### C07 — cache false negative

Remove a real candidate. Canonical fallback must still find it unless the index is actually canonical completeness-proven material. This is a mandatory I05/I03 court.

### C08 — canonical corruption while cache is healthy

Corrupt canonical bytes while leaving cache intact.

Expected: canonical release quarantines; no empirical result. Cache fallback is forbidden.

## 8. INTEGRITY-CORRUPTION COURTS

Inject one at a time:

- root-manifest bit flip;
- source/authority/replay digest change;
- missing member;
- truncated member;
- swapped whole member;
- chunk byte flip;
- chunk transplant between members;
- chunk reorder/duplicate ordinal;
- chunk offset/length tamper;
- sparse exception member corruption;
- canonical completeness index corruption;
- state/dimension mapping corruption;
- cold provenance/topology member corruption.

For each, record earliest expected detection and prove no empirical output from the corrupted release after detection.

## 9. TOCTOU COURTS

### T01 — mutate path after chunk verification

Verify selected chunk, then mutate backing path before query backend opens it.

Pass only if the backend consumes the verified immutable bytes or the mutation is detected before interpretation.

### T02 — replace file preserving size

Swap bytes with same file size and, if possible, same timestamps. Pass requires cryptographic detection.

### T03 — stale mapped/open handle semantics

Exercise the actual intended storage/backend lifecycle. Prove documented immutable-byte semantics or force full-member verification before engine consumption.

### T04 — previous-process verification hint

Verify, exit, mutate, reopen. Persisted hint must not authorize modified bytes.

## 10. ATOMIC PUBLICATION / CRASH INJECTION

Use deterministic fault injection after every durable step:

1. first staging member write;
2. final staging member write;
3. member manifests complete;
4. root manifest generated;
5. staged full verification complete;
6. file fsync/durable object completion;
7. directory/metadata durability step;
8. content-address promotion;
9. sealed reopen verification;
10. immediately before selector CAS;
11. selector CAS failure;
12. selector CAS success before cleanup;
13. cleanup halfway complete.

After each simulated crash/restart prove:

- readers see only the old active root or the fully verified new root;
- staging never serves;
- mixed members from two roots are impossible;
- incomplete candidates cannot self-authorize;
- cleanup does not delete the active canonical root;
- orphan complete candidates remain explicitly inactive.

## 11. CONCURRENT PUBLICATION COURT

Run at least two publishers from the same expected previous root:

- same semantic release/same physical root;
- same semantic release/different non-byte-reproducible physical roots;
- different semantic releases/different roots.

Pass only if:

- identical root publication is idempotent;
- divergent roots cannot both win selector CAS;
- loser cannot overwrite winner;
- active selector always names one complete verified authorized root.

## 12. ROOT-AUTHORIZATION COURT

Populate storage with multiple internally valid roots including a stale or maliciously copied root having newer mtime/name.

Pass only if service follows explicit trusted authorization, never directory `latest` heuristics.

## 13. DETERMINISTIC REBUILD COURTS

### R01 — semantic deterministic replay

Build twice from identical governed inputs in independent scratch locations/processes.

Require exact equality of:

- `semantic_release_id`;
- logical member digests;
- reconstructed semantic objects;
- ExactRefs/object/content hashes;
- I03/I05/I04 results.

### R02 — incidental environment perturbation

Vary harmless:

- temp directory;
- wall clock;
- process ID;
- filesystem enumeration order;
- locale where governed encoding makes it irrelevant.

Semantic identity/results must remain unchanged.

### R03 — byte-reproducible physical profile

If claimed, rebuild twice and require exact `physical_root_id` equality.

### R04 — non-byte-reproducible profile

Permit physical-root difference only as an explicit condition. Require independent semantic equivalence proof before either root can replace the other.

## 14. SHADOW MIGRATION / ROLLBACK COURTS

### M01 — shadow isolation

Build fully valid candidate and prove production queries cannot route to it before admission.

### M02 — semantic divergence

Introduce one bounded semantic mismatch. Independent oracle rejects promotion; current active remains authoritative.

### M03 — atomic promotion

After full integrity/equivalence acceptance, switch active selector. Concurrent readers must observe complete old or complete new root, not both within one query.

### M04 — new-root runtime failure

Trigger an error after promotion. Automatic old/shadow/cache fallback must not occur. Expected behavior is fail closed until explicit recovery/rollback governance.

### M05 — rollback target integrity

Corrupt inactive rollback candidate before rollback request. Fresh verification must reject activation.

### M06 — strict one-copy mode

If HQ interprets one-copy law as forbidding retained complete rollback candidate, demonstrate deterministic rebuild/restore path instead and measure its recovery/storage cost without weakening authority.

## 15. C13 HOT/COLD COURTS

Exercise queries that require:

- hot facts only by proven closure;
- hot facts plus cold provenance;
- cold topology/weights/routing capable of changing result;
- negative result whose refuting domain spans hot and cold members.

Pass only if tiering affects I/O timing, never authority or truth.

## 16. C20 SOURCE-LOCAL COMPILER COURTS

With bounded synthetic source-family shapes:

- change source-local physical layout without changing logical semantics;
- change compiler configuration/version;
- prove compiler identity is replay/root-bound;
- prove I03/I05/I04 and downstream interfaces do not branch semantically on source family.

No raw-source survey execution is required for the R05 mechanics court.

## 17. C21 COLUMNAR / MATRIX / BITMAP COURTS

Reorder physical rows/columns/chunks while preserving exact logical identities and rebuild law. Confirm semantic results remain unchanged.

Delete/corrupt sparse-exception/topology/routing/weight members and prove closure fails rather than silently reconstructing defaults.

Use bitmap acceleration with an intentionally missing candidate and prove canonical fallback prevents false-negative evidence.

## 18. ACCEPTANCE CRITERIA

A future implementation may claim R05 integrity acceptance only if:

1. zero corruption injection yields an undetected emitted empirical result;
2. zero exact negative result is emitted with an unverified refuting region unless root-bound canonical completeness proves exclusion;
3. zero cache false negative suppresses an I03/I05 result;
4. cache deletion changes no exact result;
5. canonical corruption never falls back to cache/legacy/shadow;
6. TOCTOU courts prove verified bytes are consumed bytes;
7. full streaming audit remains and passes;
8. every crash point preserves old-or-new atomic serving;
9. concurrent publication leaves exactly one active root;
10. deterministic semantic rebuild passes;
11. `BYTE_REPRODUCIBLE` claims pass exact physical-root equality when made;
12. shadow/rollback never creates dual-serving canonical authority;
13. no hidden persistent database is required for correctness;
14. storage accounting separates canonical/staging/scratch/cache/post-success bytes exactly.

Only after all correctness gates pass may reopen/query latency and integrity-metadata overhead determine whether hierarchical/lazy verification is worth its complexity.

A null engineering result is acceptable: if safe query closure usually requires full-member/full-release verification, keep the simpler flat verification design. Integrity does not owe optimization a win.
