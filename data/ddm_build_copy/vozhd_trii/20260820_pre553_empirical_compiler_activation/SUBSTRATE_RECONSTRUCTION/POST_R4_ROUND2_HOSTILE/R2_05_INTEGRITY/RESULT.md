# POST-R4 ROUND-2 R2-05 — INTEGRITY / PUBLICATION / REPLAY / CACHE HOSTILE COURT

Status: `AUTHORIZED__ROUND2_HOSTILE__FAIL_CLOSED__NO_RUNTIME_MUTATION`

Repository: `maidiu/rawlsing`  
Branch: `agent/vozhd-trii-postr4-r2-r05-integrity`  
Exact starting HEAD: `d612b24cce9d53bdff90fc2d7ac2604d34da02ca`  
Cell: `R2-05 — Integrity / Publication / Replay / Cache Hostile Court`

Round-2 disposition: `ROUND2_PASS_WITH_REQUIRED_CORRECTIONS__P0_REPAIRABLE`

## 1. WHOLE_MACHINE_CONTAINMENT

This return changes no production runtime and no semantic authority. It writes only under the Round-2 R2-05 hostile-return directory. It does not modify `rawlsing_next/**`, the frozen C11 semantic contract, source-native law, I03, I05, I04, V553+, V3, or V2.

The empirical integrity boundary remains subordinate to the closed machine:

`source-native truth -> frozen C11 -> I03 -> I05 -> I04 -> downstream structural/developmental/actor/expression machine`.

Integrity can decide whether canonical bytes are admissible evidence. Integrity metadata cannot repair missing authority, reinterpret source meaning, convert corruption into a normal negative state, or authorize a stale/shadow/legacy copy to stand in for canonical truth.

The Round-2 target is P0 from Authority 54: `P0_BOUNDED_TYPED_CANONICAL_INCIDENCE_WITH_UNIFORM_C11_VIEW`. The court attacks only its physical integrity/publication/replay/cache laws and the one-copy migration seam.

## 2. ROUND1_EVIDENCE_USED

Authority 54 requires all six exact Round-1 returns. This court read them at the exact pinned commits, not branch tips:

| Cell | Exact Round-1 commit | R2-05 evidence used |
|---|---|---|
| R01 | `f3e1d198ca5b680adfe3330a7460d0b174f395e6` | Segmented bounded carrier; root-bound streamed inventories; whole-member hashes; exact negative only after complete verified search; staging/seal/promote law; cache deletion invariant; lazy reading must not weaken validation. |
| R02 | `6447d57a9818b5a427ad0367858f2030e127f8d8` | Hot/cold are one canonical root; missing cold is corruption/incompleteness, never degraded validity; locator/FD metadata must be sealed and exact; physical row position is not identity. |
| R03 | `220e017f34b2741fce80b7a6850a1679ea0ce0fe` | O6 corruption/partial-publication/cache court; integrity failure is not `VALID_EMPTY`/no-data; stale cache from another root must be rejected; candidate hashes are independently recomputed. |
| R04 | `bfc6b19c3bbdd43f1a04184d02515dc38dd82712` | Canonical member corruption fails closed; bitmaps/indexes default to removable cache; cache deletion/rebuild parity; exact canonical scan fallback; late materialization cannot erase negative truth. |
| R05 | `b2c74427b568ea9a9447fc2631e002830d700919` | Root/member/chunk proposal; active-root authorization distinct from hash validity; query verification closure; TOCTOU/consume-after-verify; atomic publication; global quarantine after detected canonical corruption; one-copy/rollback tension; explicit self-rejection of Merkle if no measured benefit. |
| R06 | `d573389eaf8df63c124d1439933bbe3cef4dda23` | Non-additive minimality gate; minimum likely integrity law is immutable root + exact member hashes + deterministic replay receipt + fail-closed missing/mismatch; C14 rejected unless a named chunk need exists; redundant integrity layers must be deleted. |

Cross-cell evidence converges on one key distinction: **cryptographic inclusion is not semantic completeness**. Hashing a selected member/chunk can authenticate bytes, but exact negative/aggregate/discovery truth additionally requires a root-bound proof that no omitted canonical region can change the result.

## 3. P0_SCOPE_ATTACKED

This cell attacked:

- immutable physical-root and semantic-release identity;
- exact canonical member identity and membership;
- member versus chunk verification granularity;
- active-root authorization and selector corruption/staleness;
- concurrent publication and selector CAS;
- selector ABA under rollback/re-activation;
- mixed-root and stale-root reads;
- partial/incomplete publication visibility;
- canonical corruption and failure-state laundering;
- negative/absence completeness;
- stale/corrupt/false-positive/false-negative cache/index behavior;
- consume-after-verify / TOCTOU identity;
- deterministic semantic and physical replay;
- shadow migration, old-root draining, rollback, and strict one-copy steady state;
- whether Merkle/chunk machinery has any named job that root + member hashes cannot serve.

## 4. DESTRUCTION_PATHS_FOUND

P0 is repairable, but its provisional wording leaves several paths by which a plausible wrong empirical answer could escape.

### D01 — Root-only CAS has an ABA activation bug

If the active selector CAS compares only the expected prior root ID:

1. root `A` is active;
2. publisher `P` reads `A` and prepares candidate `C` expecting `A`;
3. another publisher activates `B` (`A -> B`);
4. an explicit rollback later reactivates `A` (`B -> A`);
5. stale publisher `P` can now successfully CAS `A -> C` even though its activation transaction belongs to the earlier `A` epoch.

That is a real stale-publication path. The fact that `C` is internally valid does not prove it is authorized against the current authority/admission context.

**Required repair:** active selection MUST be ABA-resistant. CAS the complete selector token including a never-reused monotonic `activation_generation`, not merely `physical_root_id`.

### D02 — A valid root can still be the wrong authorized semantic release

A content hash proves what bytes exist, not whether those bytes are the root currently admitted for the semantic serving slot. A selector that stores only a physical root can accidentally activate a valid root for a different semantic release or an equivalence candidate whose admission receipt is not current.

**Required repair:** the active authorization record binds at least serving slot, activation generation, `semantic_release_id`, `physical_root_id`, and the exact accepted admission/equivalence receipt identity. Activation verifies the referenced root manifest matches the record before CAS.

### D03 — Stale selector replicas can resurrect old truth

A generation field does not help if readers are allowed to consult a stale local selector cache or non-linearizable replica. An old selector record is internally well formed and may name an intact old root.

**Required repair:** the active-selector store is a tiny trusted control-plane primitive with linearizable/non-stale reads, atomic CAS, durability, and no best-effort fallback. If this cannot be provided, serving is blocked. A cache of active authorization is not authority.

### D04 — Mixed/stale query authorization can survive a concurrent activation

A reader can resolve root `A`, publication can activate `B`, and the reader can later emit an `A` result while claiming current-root semantics. Worse, reopening member paths after the selector changes can mix `A` and `B`.

**Required repair:** every query pins one exact `(serving_slot, activation_generation, physical_root_id)` token for all reads. Before empirical emission it revalidates that token against the authoritative selector; if the generation changed, the result is discarded/retried. The successful final check is the query authorization/linearization point. No member path is re-resolved through a mutable `current` alias.

### D05 — Root/member hashes do not solve TOCTOU

A reader can hash member path `M`, then DuckDB/Parquet can reopen `M` after an in-place replacement or storage-generation change. The query consumes bytes that were never verified.

**Required repair:** the storage adapter MUST provide an immutable generation/snapshot/handle and the query engine MUST consume the exact verified handle/bytes. If the backend cannot prove this identity, that backend path is inadmissible until it uses a verified immutable snapshot/buffer. Path, inode, mtime, length, or prior-process `verified=true` is insufficient.

### D06 — Negative truth can be manufactured by member-selection metadata not bound to the root

Even with perfect whole-member hashes, a query can return no-match if a mutable/external partition map omits the member containing the match.

**Required repair:** the physical root MUST bind the exhaustive canonical member inventory and the exact logical scope/coverage descriptors used to decide which members can contain refuting evidence. If a smaller exhaustive domain cannot be proved from verified canonical coverage, the query expands to broader member scans or fails closed.

### D07 — A non-authoritative cache can suppress truth if it is allowed to prune

A stale bitmap with one false negative can remove a respondent/candidate before canonical evaluation. Because the surviving rows are valid, the final result can look completely plausible.

**Required repair:** a non-authoritative cache MAY suggest positive candidates/read order, but a cache miss/nonmembership MUST NOT exclude canonical search or prove absence. Any structure whose negative/completeness result is trusted to skip canonical regions is canonical completeness material and must be root-bound, not called cache.

### D08 — A retained rollback copy can become a hidden second canonical database

Keeping the complete displaced root indefinitely for fast rollback creates steady-state duplicate C11 truth, and availability pressure invites automatic fallback.

**Required repair:** shadow/new and old copies may coexist only inside the explicitly transient publication/migration window already permitted as staging peak. After activation and reader drain, the displaced full root is deleted before migration is declared settled. After settlement, rollback means deterministic rebuild/restore from governed inputs, full verification/admission, and a new activation generation. No standing full rollback database.

### D09 — “Verified at activation” can become stale authorization after later corruption

A persisted verification receipt/boolean can outlive byte integrity if canonical storage is mutable or externally corrupted.

**Required repair:** a fresh process/session does not treat a persisted boolean as cryptographic proof. It verifies the exact whole members required by the member-level query closure, or the storage substrate supplies a separately proved immutable-generation trust primitive. Current member-hash expectations are not weakened for reopen speed.

None of these requires a Merkle tree.

## 5. P0_MECHANISMS_CONFIRMED

The following P0/Round-1 mechanisms survive the hostile court and should remain synthesis law:

1. **Separate semantic and physical identity.** `semantic_release_id` names logical/replay equivalence; `physical_root_id` authenticates one exact physical realization.
2. **Immutable content-addressed root.** A root manifest with canonical serialization/version binds source/decoder/compiler/authority/replay identity and exact canonical member composition.
3. **Root-bound exact member inventory.** The inventory is canonical, streamed/bounded, exhaustive, and binds each member role/id/schema/length/whole-byte hash/logical digest/coverage descriptor.
4. **Whole-member cryptographic hashes.** These have a distinct job from the root hash: the root authenticates expected composition; member hashes authenticate actual member bytes.
5. **Canonical coverage metadata.** Any member-scope/pruning structure used to prove completeness or absence is canonical and root-bound.
6. **Member-level verification closure.** Every whole member capable of changing the exact result is verified before that result is emitted. If member-level scope cannot prove exclusion, verify more.
7. **Unique non-serving staging, full verify, durable promote, sealed reopen, explicit active authorization.** Staging/shadow never self-authorizes.
8. **Global quarantine after detected canonical corruption.** Once a canonical root/member mismatch is detected, that physical release stops serving. No cache/legacy/shadow rescue.
9. **Non-authoritative cache deletion law.** Deleting all caches cannot change correctness, replay identity, or empirical reachability.
10. **No automatic fallback/rollback.** Recovery is explicit and verified.
11. **Full streaming audit remains available.** Partial/lazy optimization never replaces it.
12. **Physical re-layout remains semantically invisible.** Row groups, shard boundaries, compression, and worker count do not alter semantic identity.

## 6. P0_MECHANISMS_REJECTED

### R06-1 — Mandatory Merkle/chunk tree as P0 core

`REJECT__NO_NAMED_REQUIREMENT`

Whole-member hashing is streaming and bounded. R01 already proposes bounded fixed-size shards, so member size itself is a controllable verification granularity. P0 is local-workstation-first and no accepted requirement demands remote inclusion proofs, partial remote fetch, or chunk repair. Corruption recovery is rebuild/quarantine, not surgical cache repair.

Therefore C14 does not enter the minimum P0 integrity stack.

### R06-2 — Separate per-member manifest when one authenticated inventory record suffices

A root-bound streamed inventory record can bind member role, schema, length, byte hash, logical digest, and coverage. A second per-member manifest layer is not mandatory unless a future member needs independently versioned metadata too large for the inventory record.

### R06-3 — Whole-release byte checksum in addition to root + member hashes

A monolithic release-byte checksum duplicates the composition proof already provided by `physical_root_id -> member inventory -> whole-member hashes`. It has no distinct required failure granularity and is rejected from the minimum stack.

### R06-4 — Format checksums as canonical integrity authority

Parquet/page checksums may remain implementation diagnostics/early error detectors, but they do not become an independent authority layer and do not alter failure precedence.

### R06-5 — Cache hashes as a reason to trust cache negatives

A cache checksum can detect accidental damage to a cache artifact, but it cannot grant empirical completeness authority. Cache nonmembership remains non-evidence.

### R06-6 — Standing rollback copy

A complete prior canonical carrier retained indefinitely for availability conflicts with strict one-copy steady state and creates fallback pressure. Reject it after migration settlement.

### R06-7 — Root-only active-selector CAS

Rejected because of the ABA path above.

## 7. P0_MECHANISMS_CONDITIONALLY_ADMISSIBLE

### C14-A — Flat root-bound chunk hashes

Conditional only if a later measured court proves whole-member verification granularity itself fails a named practical gate and reducing canonical shard/member size is insufficient or operationally worse. Chunk descriptors must be root-bound, and query completeness still comes from canonical coverage—not from chunk authentication.

### C14-B — Merkle tree

Conditional one step later. Merkle is justified only if all are true:

1. chunk-level independent verification/fetch is already proven necessary;
2. a flat root-bound chunk-hash inventory is itself a measured bottleneck or remote proof distribution requires logarithmic inclusion proofs;
3. the storage adapter provides immutable range-read identity;
4. negative/aggregate/discovery closure remains exact;
5. full whole-member/release audit remains.

No current accepted evidence establishes these conditions.

### Cache pruning

A derived accelerator may be allowed to prune only if it is promoted to **canonical root-bound completeness material** and independently equivalence-tested, or if every possible false negative is followed by canonical fallback. Otherwise cache is positive hint/read-order only.

### Byte-reproducible physical profile

Conditionally admissible as an explicit stronger profile. Absent that declaration, deterministic semantic identity/logical digests are mandatory while byte-different physical roots require independent equivalence/admission before activation.

## 8. INFORMATION_ACCOUNT

The minimum authoritative information classes are:

- **semantic release identity/replay receipt** — canonical logical authority binding;
- **physical root manifest** — exact physical realization identity and schema/algorithm version;
- **streamed member inventory** — exhaustive root-bound member composition and logical coverage;
- **whole-member byte hashes/lengths** — actual physical-byte integrity;
- **logical member digests** — deterministic reconstruction/equivalence bridge;
- **canonical coverage/scope descriptors** — member-level completeness for positive/negative query closure;
- **canonical member bytes** — unique empirical/replay/authority information;
- **accepted semantic/equivalence receipt identity** — binds authorization of the physical realization to the frozen semantic release.

The active selector is **authoritative control state but not empirical truth**. Its minimum tuple is:

`(serving_slot, activation_generation, semantic_release_id, physical_root_id, admission_receipt_id)`.

It MUST live in a trusted linearizable CAS/durability domain and MUST NOT be inferred from filesystem names/mtimes or cached as truth.

Caches, telemetry, scratch, staging runs, shadow candidate bytes, verification hints, and physical query plans remain noncanonical/transient. If deleting a purported cache prevents exact reconstruction or exact absence proof, it was misclassified and must move under the canonical root.

No source-native or C11 information is deleted by this R2-05 correction.

## 9. I03_I05_I04_EFFECT

### I03

Integrity is a prerequisite gate, not a semantic negative state. `INTEGRITY_FAILURE`, incomplete member closure, selector mismatch, stale authorization, and TOCTOU failure MUST NOT be mapped to `VALID_EMPTY`, no-match, observed-zero, zero-support, unavailable routing, or any other ordinary empirical fact state.

A positive I03 result requires verified whole-member closure for every member capable of changing the fact/support/risk/measure/provenance outcome. A negative I03 result additionally requires verified root-bound completeness for every possible refuting member in the governed domain.

### I05

A non-authoritative bitmap/index/cache cannot define candidate reachability. Cache misses cannot suppress an unforeseen candidate. Any pruning that can produce false negatives must either be canonical completeness-proven or be followed by canonical member fallback.

### I04

Only facts produced from the exact active, integrity-closed root are eligible for structural admission. Staging, shadow, old inactive roots, caches, legacy stores, and corrupt roots cannot contribute positive structural evidence.

## 10. INTEGRITY_REPLAY_EFFECT

The minimum P0 trust chain after Round-2 correction is:

`trusted active-selector record`
`-> exact semantic/admission binding`
`-> physical_root_id`
`-> verified immutable root manifest`
`-> verified streamed member inventory`
`-> whole-member hash verification for exact member-level query closure`
`-> consume those same immutable member generations/handles`
`-> validated uniform C11 view`
`-> I03/I05/I04 output`
`-> final selector-generation revalidation before emission`.

The minimum publication chain is:

`UNIQUE_STAGING`
`-> COMPLETE MEMBERS`
`-> SEMANTIC/ORACLE VALIDATION`
`-> WHOLE-MEMBER HASH + ROOT SEAL`
`-> FULL STAGED VERIFY`
`-> DURABLE CONTENT-ADDRESS PROMOTE`
`-> SEALED REOPEN VERIFY`
`-> ABA-SAFE ACTIVE-RECORD CAS`
`-> READER DRAIN`
`-> DELETE DISPLACED FULL ROOT`
`-> MIGRATION_SETTLED`.

Crash before CAS leaves the old selector authoritative. CAS failure leaves the candidate inactive. Crash after CAS cannot make the old root an automatic fallback. Recovery reopens the active authorization record and verifies exactly that root.

Semantic deterministic rebuild remains:

`exact source + governed decoder/extraction + compiler/schema/config/authority frontier -> identical semantic_release_id + logical member digests + logical C11/I03/I05/I04 results`.

Physical-root equality is required only for a profile explicitly admitted as byte-reproducible. A different physical root never self-substitutes merely because its producer claims equivalent semantics.

## 11. SOURCE_HETEROGENEITY_EFFECT

The integrity correction is representation- and source-family-neutral. It does not assume rectangularity, one missingness regime, one respondent ID, one topology, one weight, one encoding, or one physical layout.

R02/R04 source-shape distinctions matter only because every canonical determinant/member they require must be listed under the same root and included in member-level closure when it can change an answer. Hot/cold, dense/explicit, SAV/DTA, source-local compiler profiles, and columnar/long layout do not create different integrity semantics.

No raw-source probe was necessary. The Round-1 returns and Authorities 54/55 contain enough accepted evidence to decide this integrity/minimality question.

## 12. COMPLEXITY_MINIMALITY_EFFECT

Round-2 deletes more machinery than it adds.

### Minimum required integrity machinery

1. canonical root-manifest serialization + `physical_root_id`;
2. deterministic `semantic_release_id`/logical replay receipt;
3. one streamed root-bound exhaustive member inventory;
4. whole-member hashes/lengths/logical digests and coverage descriptors;
5. member-level exact verification closure;
6. immutable consume-after-verify storage handles/snapshots;
7. unique staging + durable content-address promotion + sealed reopen verification;
8. ABA-safe, linearizable active-selector record with semantic/admission binding;
9. root-pinned query authorization token and final generation check;
10. global quarantine after detected canonical corruption;
11. cache deletion/rebuild/bypass law;
12. transient one-copy migration settlement + deterministic rebuild rollback;
13. full streaming audit.

### Explicitly not required in P0 core

- Merkle tree;
- chunk tree;
- separate member manifest layer where inventory records suffice;
- monolithic whole-release byte checksum;
- format checksum as semantic authority;
- standing rollback database;
- cache-completeness authority;
- persistent verification booleans as read authorization.

This is consistent with R06's non-additive minimality law: every retained layer has a distinct named failure it closes.

## 13. RAW_SOURCE_PROBES_IF_ANY

`NONE__REPOSITORY_AND_PINNED_ROUND1_EVIDENCE_SUFFICIENT`

No source byte was required to answer an integrity/publication/control-plane question. The unresolved risks are storage/control semantics and query-closure proof, not source-physical ambiguity.

## 14. SELF_FALSIFICATION

This Round-2 ruling is falsified or must be reopened if a later bounded court demonstrates any of the following:

1. root + streamed member inventory + whole-member hashes cannot detect a canonical corruption before that corrupt member contributes to an emitted result;
2. canonical coverage cannot conservatively map exact query domains to whole members, and member-level closure can return false absence;
3. the storage backend cannot provide immutable consume-after-verify identity and no safe snapshot/buffer adapter is practical;
4. the active-selector store cannot provide linearizable non-stale reads, durable ABA-safe CAS, and explicit admission binding;
5. strict one-copy cleanup cannot be completed safely after activation without dual-serving or data loss;
6. deleting every non-authoritative cache changes an exact result or discovery reachability;
7. deterministic rebuild cannot reproduce semantic identity/logical digests under the frozen authority frontier;
8. a measured full-scale court shows whole-member verification is the remaining hard/practical failure while smaller canonical members/shards do not solve it;
9. a named remote partial-fetch/independent-repair requirement is later admitted that cannot be served at member granularity.

Items 8-9 may justify **flat chunk hashes first**. They do not automatically justify a Merkle tree. Merkle requires a second proof that a flat chunk inventory is itself insufficient.

If any integrity failure can still be converted into a normal empirical negative or rescued by cache/old/shadow truth, this disposition becomes `ROUND2_REJECT__P0_DESTRUCTIVE_OR_INCOMPLETE`.

## 15. REQUIRED_SYNTHESIS_CHANGES

P0 must be hardened by all of the following before Round-3 prototype law:

1. **Replace root-only selector CAS with ABA-safe activation CAS.** The selector token includes a never-reused monotonic generation.
2. **Bind active authorization to semantic and admission identity.** Active record includes serving slot, semantic release, physical root, and exact accepted equivalence/admission receipt.
3. **Require a linearizable trusted selector store.** Stale selector caches/replicas cannot authorize a root; missing/corrupt/unavailable selector authority fails closed.
4. **Pin one root per query and revalidate generation before emission.** No mixed-root query and no result from a root invalidated before its authorization point.
5. **Freeze a consume-after-verify storage contract.** Verify and interpret the exact same immutable generation/handle; mutable path reopen is forbidden.
6. **Make root-bound member coverage mandatory.** The canonical inventory includes exhaustive logical scope sufficient for conservative member-level closure; otherwise broaden scan.
7. **Narrow non-authoritative cache semantics.** Cache miss/nonmembership is never evidence and cannot suppress canonical fallback. Canonical corruption disables cache use entirely.
8. **Resolve strict one-copy migration.** Shadow/new duplicate is transient staging-like material only. After CAS and reader drain, delete displaced full root before declaring migration settled. No standing rollback copy.
9. **Define rollback after settlement as rebuild/restore + fresh verify/admission + new activation generation.** No automatic fallback.
10. **Reject C14 from P0 core.** Use whole-member hashes; admit flat chunks only after a measured member-granularity failure; admit Merkle only after an additional named flat-chunk insufficiency.
11. **Keep global quarantine and full streaming audit.** No local corruption exception or speed bargain.

These are corrections to P0's integrity/control contract, not a new storage architecture.

## 16. FINAL_ROUND2_DISPOSITION

`ROUND2_PASS_WITH_REQUIRED_CORRECTIONS__P0_REPAIRABLE`

P0 survives the assigned hostile integrity court **only after** the corrections above. The central architecture remains sound: bounded canonical incidence, one immutable root, uniform C11 view, one serving canonical truth, exact cache fallback to canonical, and transactional publication.

The court rejects mandatory Merkle/chunk machinery. No accepted Round-1 or Authority-54 requirement needs it for correctness, replay, atomic publication, negative truth, quarantine, one-copy migration, or cache deletion. Whole-member hashes at bounded shard/member granularity are the minimum sufficient cryptographic mechanism currently justified.

The most important newly named repair is ABA-resistant active-root authorization. A root hash authenticates bytes; only a generation-stamped, semantic/admission-bound, linearizable activation record authorizes **which** valid root may speak now.

`POST_R4_R2_R05_INTEGRITY_RETURNED`
