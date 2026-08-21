# R2-05 BENCHMARK / PROOF PLAN — FLAT INTEGRITY FIRST, C14 ONLY BY NECESSITY

Status: `ROUND2_HOSTILE_PROOF_PLAN_ONLY__NO_RUNTIME_IMPLEMENTATION`

## 1. Purpose

This plan decides whether the corrected minimum P0 integrity stack is sufficient and whether C14 chunk/Merkle machinery has any measured job.

Correctness gates run before performance. One corruption that becomes `VALID_EMPTY`, no-match, zero-support, a plausible aggregate, or cache/old-root fallback rejects the candidate.

No raw survey source is required for these mechanics courts. Use bounded synthetic/checked-in logical fixtures until HQ authorizes implementation-scale execution.

## 2. Candidate integrity variants

Test in this order. Do not skip ahead.

### V0 — minimum flat member integrity

- immutable root manifest;
- streamed exhaustive member inventory;
- whole-member hashes/lengths/logical digests;
- root-bound coverage descriptors;
- full streaming audit;
- ABA-safe active selector;
- immutable consume-after-verify member handles;
- no chunk hashes;
- no Merkle.

### V1 — smaller canonical members/shards

Same as V0, with smaller deterministic member target to test whether verification granularity can be improved without another integrity layer.

### V2 — flat root-bound chunk hashes

Only run as an admission candidate if V0/V1 fail a named practical verification/fetch gate. No Merkle internal tree; root/member inventory binds the chunk-hash inventory.

### V3 — Merkle tree over chunks

Run only if V2 is already necessary and V2's flat chunk inventory/proof transfer is itself a named measured bottleneck or remote inclusion-proof requirement.

If V0 or V1 closes the whole court, stop and reject V2/V3 as overengineering.

## 3. Fixed acceptance identities

Freeze before each run:

- fixture semantic expected truth;
- exact source/replay identities represented by fixture;
- frozen C11/I03/I05/I04 law/version;
- candidate root-manifest schema/canonical serialization;
- member inventory schema;
- hash algorithm/version;
- member sizing/shard policy;
- coverage descriptor law;
- active-selector store semantics;
- cache key schema if cache is present;
- storage adapter immutable-generation/handle semantics;
- whether the physical profile claims byte reproducibility.

## 4. Mandatory measurements

Record separately:

- root manifest bytes/read/hash time;
- member inventory bytes/read/hash time;
- member count and size distribution;
- canonical bytes read;
- canonical bytes cryptographically verified;
- full-member hash time;
- query/reconstruction time;
- cold open total time;
- warm repeated-query time;
- full streaming audit time;
- peak RSS by phase;
- open file count;
- filesystem metadata/stat operations;
- scratch bytes;
- staging peak bytes;
- post-success retained bytes;
- cache bytes separately;
- selector read/CAS latency;
- result/replay identities;
- exact failure state for every injected fault.

For V2/V3 additionally record:

- chunk count/size;
- flat chunk inventory bytes;
- Merkle node bytes;
- chunk-hash generation time;
- inclusion-proof bytes/verification time;
- verified-byte savings relative V0/V1;
- whether exact query closure actually became narrower.

## 5. Gate A — flat integrity correctness

### A01 — root tamper

Flip root manifest byte. V0 must fail before canonical member selection.

### A02 — member missing

Delete a root-listed member. Exact lookup/aggregate must return integrity/incomplete failure, never empty/no-match.

### A03 — member truncate

Truncate while preserving a parseable prefix. Whole-member length/hash must fail before output.

### A04 — cross-root swap

Replace one member with a valid member from another root. Expected member hash/record rejects.

### A05 — unreferenced file

Add plausible extra member file. It must not enter truth because verified inventory is sole membership authority.

### A06 — semantic-wrong but hash-valid fixture

Generate internally hashed candidate with one known semantic mismatch. Independent R03-style oracle rejects; integrity must not self-certify semantics.

V0 fails the entire Round-2 correction if any A01-A06 emits plausible empirical truth from invalid state.

## 6. Gate B — negative/absence completeness

Construct a release with at least four members where matches/refuting evidence are deliberately placed in late members and sparse-exception/route/weight metadata is separate.

Run:

- exact no-match;
- exact zero-support candidate;
- `VALID_EMPTY`-capable semantic fixture;
- NOT predicate;
- weighted support;
- routing/applicability negative;
- sparse default plus late override;
- I05 unforeseen combination.

For each:

1. corrupt or omit one member capable of refuting/changing the result;
2. leave early members and cache/index plausible;
3. require integrity/closure failure before ordinary semantic negative;
4. then restore member and require exact baseline result.

A root-bound coverage descriptor may exclude a member only when the independent fixture oracle proves that exclusion sound.

## 7. Gate C — cache deletion/staleness/corruption

Run every exact query under:

- no cache;
- warm cache;
- cache deleted immediately before query;
- cache rebuilt twice;
- stale cache from different physical root;
- stale cache from different semantic release;
- stale routing/authority dependency;
- one false-positive cache entry;
- one false-negative cache entry;
- malformed/truncated cache;
- healthy cache while canonical member is corrupt.

Pass conditions:

- cache deletion changes no truth/replay/discovery reachability;
- false-positive hits are rejected by canonical verification;
- false-negative/miss cannot suppress canonical match/candidate;
- malformed/stale cache is discardable;
- canonical corruption yields no result even when cache is healthy.

## 8. Gate D — active selector ABA and stale authorization

Use deterministic state machine tests.

### D01 — simple CAS

`A/g1 -> B/g2`; require exact selector record advance.

### D02 — ABA

1. publisher C records expected `A/g1`;
2. activate `B/g2`;
3. explicit rollback activates `A/g3`;
4. stale C attempts CAS using `A/g1`.

Required: fail. A root-only CAS implementation is rejected.

### D03 — wrong semantic root

Candidate physical root is valid but semantic id differs from serving slot. Required: reject before CAS.

### D04 — wrong admission receipt

Root/semantic id valid, receipt not accepted for candidate/slot. Required: reject.

### D05 — stale selector read

Inject stale replica/cache returning older complete record. Required: it cannot authorize. The test platform must either provide linearizable authoritative read or fail closed.

### D06 — torn/corrupt selector

Required: no directory scan/latest heuristic; serving authorization unavailable.

## 9. Gate E — query activation linearization

### E01 — activation before final check

Query pins `A/g10`, computes result, `B/g11` activates, then query final-checks. Required: discard/retry.

### E02 — activation after successful final check

Query final check succeeds on `A/g10`; then `B/g11` activates. Treat query authorization point as before activation; output may complete with A result without claiming mixed/current B semantics.

### E03 — member resolution after selector change

Force backend to request another member after selector changed. It must continue only on the pinned immutable A root token; final generation check then prevents stale emission. It may never resolve through `current` and open B.

## 10. Gate F — TOCTOU consume-after-verify

### F01 — pathname replacement

Hash member; replace path with same-length alternate bytes before query backend accesses it. Required: backend consumes old verified immutable handle/generation or aborts.

### F02 — object generation drift

Verify object version/generation G1; unversioned read is manipulated to G2. Required: reject unsafe read path.

### F03 — previous-process marker

Verify; terminate process; alter member; reopen with persisted hint. Required: fresh member closure detects change.

### F04 — same inode/mtime/size

Where test platform permits, mutate bytes while preserving convenient metadata. Cryptographic/immutable-handle law must still detect/prevent consumption.

Failure of F01-F04 is not repaired by adding Merkle unless the same immutable range identity is also proven.

## 11. Gate G — publication crash/concurrency

Inject crash after each step:

1. first staging member;
2. final staging member;
3. inventory close;
4. semantic/oracle acceptance;
5. member hash completion;
6. root seal;
7. full staged verify;
8. durable flush;
9. content-address promote;
10. sealed reopen verification;
11. immediately before selector CAS;
12. selector CAS success;
13. reader drain start;
14. old-root deletion halfway;
15. cleanup complete.

After restart require:

- one exact active selector record or explicit authorization failure;
- no staging/shadow discovery as truth;
- no mixed-root member set;
- no automatic old/cache fallback;
- candidate promoted-but-inactive remains inactive;
- migration not marked settled while displaced full root remains after drain/cleanup expectation.

Concurrency court runs two publishers with same expected generation and distinct roots; exactly one activation generation may win.

## 12. Gate H — one-copy migration/rollback

### H01 — shadow isolation

While candidate builds, only old active root can authorize results.

### H02 — activation

After CAS, no new query can authorize old root. Old root is `DRAINING_TRANSIENT` only.

### H03 — reader drain/delete

Old root may remain physically only until pinned handles drain. Migration is not settled until full old root and staging duplicate are removed.

### H04 — transient rollback

Before old deletion, explicit rollback requires fresh old-root integrity verification and new-generation CAS. No automatic fallback.

### H05 — settled rollback

After old deletion, request rollback. Required path: deterministic rebuild/restore -> semantic/oracle acceptance -> full integrity verify -> content-address promote -> ABA-safe activation. No secret backup C11 store may be read directly as truth.

Storage accounting must show one post-success canonical root.

## 13. Gate I — deterministic replay

Rebuild same governed semantic inputs while varying harmless:

- temp path;
- filesystem enumeration order;
- process ID;
- hash seed;
- worker count where deterministic build permits;
- row-group/member grouping where semantic identity is layout-independent;
- cache absent/present.

Require identical:

- `semantic_release_id`;
- logical member digests at the contracted logical partitioning law;
- reconstructed C11 identities/ExactRefs;
- I03/I05/I04 outputs and replay receipts.

If `BYTE_REPRODUCIBLE`, additionally require exact physical root. Otherwise physical-root difference is visible and requires independent equivalence before activation.

## 14. Gate J — full streaming audit

On every variant, run bounded full release audit:

- verify root;
- verify complete inventory;
- whole-hash every canonical member;
- reconstruct/audit semantic/replay closure;
- detect each injected canonical fault;
- prove no corpus-scale Python retention.

V2/V3 may not delete or weaken J.

## 15. C14 admission court

### Step C14-0 — V0/V1 first

Measure later Round-3 practical targets under the same representative fixture/workload. Authority 54 suggests preliminary `cold open < 5s` and `warm repeated query < 1s` subject to adjustment before launch.

If V0/V1 satisfy exactness, fail-closed law, resource bounds, and practical verification/open behavior, disposition is:

`REJECT_C14__WHOLE_MEMBER_INTEGRITY_SUFFICIENT`.

### Step C14-1 — flat chunks only after named failure

If whole-member hashing is specifically the remaining failed gate and smaller members/shards are not acceptable due file-count/metadata/other measured cost, pilot V2.

V2 must prove:

- exact immutable range handles;
- root-bound chunk map;
- no false-negative query closure;
- negative queries verify every refuting chunk/member or canonical completeness proof;
- full audit retained;
- material improvement on the failed gate.

If V2 fails to materially solve the named gate, reject C14.

### Step C14-2 — Merkle only after flat chunks are insufficient

Pilot V3 only if V2 is necessary **and** flat chunk inventory/proof distribution is itself the measured problem.

Examples of potentially admissible named jobs:

- remote client needs compact independent inclusion proofs without fetching flat chunk inventory;
- flat chunk manifest is too large for the accepted open/fetch envelope;
- authenticated chunk proof must be transported independently through an untrusted distribution layer.

Corruption localization by itself is not enough because P0 quarantines/rebuilds rather than trusts surgical cache repair.

### C14 acceptance rule

Merkle passes only if:

`V0/V1 fail named gate`
`AND V2 is necessary`
`AND V2 itself fails named flat-proof gate`
`AND V3 materially cures that gate`
`AND all correctness/closure/audit/TOCTOU/one-copy courts remain exact`.

Anything weaker is ornamental integrity machinery.

## 16. Automatic rejection conditions

Reject P0 implementation if any occurs:

- corruption becomes `VALID_EMPTY`, no-match, zero-support, observed-zero, or plausible positive;
- cache false negative suppresses a lawful result/candidate;
- canonical corruption falls back to cache/old/shadow/legacy;
- selector root-only ABA succeeds;
- selector reads can be stale while still authorizing;
- valid root for wrong semantic/admission target activates;
- query mixes roots;
- query verifies bytes but backend consumes another generation;
- standing old full root remains after migration settlement;
- rollback happens automatically;
- full audit is removed;
- Merkle is added before the C14 admission sequence establishes necessity.
