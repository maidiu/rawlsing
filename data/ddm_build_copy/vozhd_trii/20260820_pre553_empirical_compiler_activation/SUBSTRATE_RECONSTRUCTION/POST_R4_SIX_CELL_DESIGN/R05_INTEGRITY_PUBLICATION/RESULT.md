# POST-R4 R05 — INTEGRITY / REPLAY / PUBLICATION / CANONICAL-COPY RECONNAISSANCE

Status: `AUTHORIZED__NON_DISPOSITIVE__FAIL_CLOSED_INTEGRITY_DESIGN`

Cell: `R05 — INTEGRITY / REPLAY / CACHE / PUBLICATION / CANONICAL-COPY LAW`

Starting HEAD: `bc2d022d49b1a860a33b29ce171a89c91956c35e`

Return posture: design/proof only; no production runtime implementation; no raw-source probe.

## 1. WHOLE_MACHINE_CONTAINMENT

This proposal changes only the physical integrity, publication, replay, cache, and canonical-copy discipline around a future C11-equivalent empirical carrier. It does not reopen source-native semantics, C11 semantic families, M01-M18, ExactRef/object identity, I03 exact-query truth conditions, I05 exact-bounded discovery, I04 structural admission, or V553/V554/V555/V556/V557/V558/V3/V2 jurisdiction.

The governing whole-machine separation remains intact: source evidence establishes empirical reality; later structural/developmental/actor/expression stages may consume governed evidence but may not manufacture, relabel, or repair empirical truth. R05 therefore treats integrity failure as an evidence-availability failure, not as permission to substitute cache state, an old database, a shadow carrier, or a downstream inference.

The proposal is intentionally carrier-neutral. It can bind a future long, normalized, columnar, matrix, bitmap, late-materialized, or source-local compiled carrier provided that carrier exposes exact immutable canonical members and an exact reconstruction/coverage contract. C13 hot/cold partitioning, C20 source-local compilation, and C21 vector/matrix layout remain physical choices under the same root; none may create downstream semantic branching.

## 2. PROBLEM_OWNED

R05 owns the failure boundary between `bytes exist` and `empirical evidence is admissible`.

The replacement carrier must answer all of the following without weakening current R4 expectations:

- What immutable object names one complete release?
- How are exact canonical members and sub-member chunks authenticated?
- What verification states exist, and which state actually authorizes empirical output?
- How can partial/lazy verification be safe for positive, negative, aggregate, weighted, routed, and discovery queries?
- How is a release published atomically so crashes cannot expose mixed or incomplete truth?
- What happens when corruption is detected after publication?
- Which bytes are canonical and which are regenerable non-authoritative cache?
- How are caches invalidated, deleted, and rebuilt without becoming a second truth store?
- What deterministic replay identity survives physical encoder variation?
- How can shadow migration and rollback occur without two simultaneously serving canonical databases?

The hostile target is especially `lazy verification`: it is easy to verify the bytes that produced a hit while silently allowing unverified bytes to determine who was not seen, which denominators were used, which respondents were excluded, or which candidate combinations were never discovered. That design is rejected here.

## 3. PROPOSED_MECHANISM

Propose a two-level immutable release identity plus hierarchical integrity and a query-scoped verification-closure gate.

### 3.1 Two identities, not one overloaded hash

Define:

1. `semantic_release_id`
   - deterministic identity of the complete logical empirical release;
   - binds source snapshot identities, accepted extraction/decoder receipts, frozen authority/compiler contract, canonical coverage law, and deterministic logical member digests;
   - excludes incidental paths, wall-clock timestamps, temporary names, and physical encoder accidents;
   - same lawful rebuild must reproduce this identity and the same logical query/reconstruction results.

2. `physical_root_id`
   - cryptographic identity of one exact immutable physical realization;
   - binds the immutable root manifest, member manifests, exact member byte hashes, chunking profile, and hierarchical chunk roots;
   - distinguishes byte-different physical realizations even when they are separately proven semantically equivalent.

This separation is required because current R4 law makes semantic/logical determinism dispositive while Parquet byte identity is not automatically semantic authority. A future physical profile may additionally declare `BYTE_REPRODUCIBLE`; only then does a same-input physical-root mismatch become a deterministic-rebuild failure.

The root digest payload must exclude the field that stores its own outer digest or use an explicitly defined canonical preimage form. No recursive self-hash ambiguity is permitted.

### 3.2 Immutable root manifest

The sealed root manifest must bind at minimum:

- manifest schema/version and domain-separation version;
- cryptographic algorithms;
- `semantic_release_id`;
- physical profile/chunking profile;
- exact source snapshot identifiers/hashes or immutable references to the accepted source/extraction receipt set;
- decoder/extractor/compiler implementation and configuration digests required by governing replay law;
- frozen C11/M01-M18/authority contract digests sufficient to prevent replay under silently different semantics;
- canonical coverage inventory;
- ordered canonical member roles and member-manifest digests;
- exact logical member digests;
- any canonical completeness/index structures required to prove query-domain coverage;
- publication/replay contract version.

Caches, transient verification state, filesystem mtimes, process IDs, wall-clock publication time, and active-pointer state are excluded from semantic identity.

### 3.3 Member and chunk integrity

Every canonical member has an immutable member manifest binding:

- member role/type and exact release-local identifier;
- byte length;
- whole-member cryptographic hash;
- logical member digest;
- chunk/row-group partition profile;
- ordered chunk descriptors: ordinal, byte offset, byte length, leaf digest;
- Merkle/hierarchical root over those chunk leaves.

Chunk leaves are domain-separated and bind member identity, chunk ordinal, offset, length, and bytes. Internal nodes are separately domain-separated. Swapping equal-looking chunks, duplicating ordinals, changing boundaries, or reinterpreting a leaf under another member must fail.

The current whole-member verification path remains mandatory. Hierarchical verification is additive: it enables exact bounded verification for query-scoped access; it never removes the streaming full member/release audit.

### 3.4 Verification state machine

Canonical release/member state is modeled as monotonic evidence within a process/session, with terminal failure states:

- `UNSEEN`
- `ROOT_VERIFIED`
- `MEMBER_MANIFEST_VERIFIED`
- `CHUNK_VERIFIED`
- `MEMBER_VERIFIED_FULL`
- `QUERY_CLOSED`
- `RELEASE_VERIFIED_FULL`

Failure states:

- `INCOMPLETE`
- `CORRUPT`
- `QUARANTINED`

`CHUNK_VERIFIED` is not an output authorization state. Only a `QUERY_CLOSED` proof for the exact query/evidence plan may authorize empirical output, or `RELEASE_VERIFIED_FULL` as the stronger case.

A query closure records the exact immutable root, dependency/member/chunk coverage set, completeness predicates, and verification results used. It is process-local/transient unless separately sealed as an audit receipt; a persisted boolean such as `verified=true` never authorizes a later process to skip cryptographic verification.

### 3.5 Verification closure law

Before any empirical result is emitted, the verifier must close every canonical dependency whose content **or absence** can change that result.

For a positive atomic fact, the exact canonical bytes containing the fact and all canonical identity/state/provenance dependencies required to interpret it must be verified.

For an aggregate, support count, denominator, weighted estimate, routing/applicability/risk set, uncertainty calculation, respondent conjunction, or discovery frontier, closure includes every canonical member/chunk whose contents can add, remove, reweight, reroute, or reclassify a contributor.

For a negative/absence claim, closure is stricter: every canonical region in the governed coverage domain capable of containing refuting evidence must be verified, unless a root-bound canonical completeness structure proves that a smaller region is exhaustive. A non-authoritative cache/index miss never proves absence.

A speed index may narrow reads only if it is either:

- canonical, root-bound, completeness-proven material under the root; or
- a non-authoritative over-approximation whose false negatives cannot suppress canonical fallback/closure.

If the system cannot prove a query-scoped dependency closure, it must escalate to whole-member or whole-release verification, or fail closed. Latency is not permission to guess.

### 3.6 TOCTOU closure

The bytes authenticated must be the bytes interpreted. The preferred mechanism hashes an immutable read buffer and decodes/query-consumes that exact buffer. If a storage/query backend cannot guarantee use-after-verify identity for sub-member reads, partial verification is unsafe and the member must be fully hashed/verified before the backend is allowed to interpret it.

File size, inode, mtime, mmap identity, page-cache residency, object-store ETag without a governed algorithm contract, or a previous process's verification marker are not cryptographic proof.

### 3.7 Atomic publication

Publication uses a unique, non-serving staging tree on the same atomicity/durability domain as the release store.

Required order:

1. build all canonical members and manifests in staging;
2. complete required semantic reconstruction/parity checks;
3. compute and verify whole-member hashes plus hierarchical roots;
4. build canonical root manifest and `physical_root_id`;
5. perform a full release integrity pass sufficient to prove the staged release self-consistent;
6. durably flush files/manifests and staging directory according to the verified filesystem/object-store publication protocol;
7. atomically rename/promote staging to content-addressed `releases/<physical_root_id>` or use an equally strong object-store commit primitive;
8. independently reopen/verify the sealed root;
9. atomically compare-and-swap the non-authoritative active selector from the expected previous root to the new verified root.

If the storage substrate cannot provide a proved atomic/durable publication primitive with these semantics, this mechanism is rejected for that substrate.

Crash behavior:

- crash before sealing/promote: staging is invisible and disposable;
- crash after seal but before promote: sealed staging remains non-serving and disposable/recoverable;
- crash after content-addressed promote but before selector swap: complete inactive release may remain, old active release still serves;
- selector swap: readers observe old or new root, never a mixed tree;
- duplicate publication of the exact same root is idempotent;
- an existing `physical_root_id` with divergent bytes is a catastrophic integrity/collision alarm, not overwrite permission.

Concurrent publishers use content-addressed roots plus selector compare-and-swap. A losing publisher leaves only an inactive complete candidate and cannot overwrite a concurrently promoted release.

### 3.8 Corruption and quarantine

Any root/member/chunk integrity failure marks the physical release `CORRUPT` and then `QUARANTINED` for empirical serving. Once canonical corruption is detected, the release must not continue serving supposedly unaffected queries: the integrity boundary of that physical release is broken and the corruption's scope is not entitled to self-limit.

Recovery is deterministic rebuild from accepted immutable authority/source inputs or activation of a separately verified equivalent release under explicit operator action. Cache, shadow state, a legacy database, or an older carrier may not silently repair or fill corrupt canonical evidence.

### 3.9 Canonical versus cache

Every accelerator that is not required for exact reconstruction/coverage is labeled:

`NONAUTHORITATIVE__REGENERABLE_CACHE`

A cache:

- contains no unique empirical information;
- is outside `physical_root_id` and `semantic_release_id`;
- can be deleted at any time without changing correctness;
- can be bypassed by every correct query path;
- is keyed by immutable dependencies, including at least semantic/root identity, cache schema/kind, builder implementation digest, and relevant canonical config/parameters;
- never supplies evidence when canonical integrity fails.

Canonical disagreement always wins against cache. Cache disagreement causes cache invalidation/quarantine/rebuild, not canonical rewriting.

A structure needed to prove complete absence or exhaustive candidate coverage is not a mere cache; it is canonical, root-bound material and must be integrity-verified as part of query closure.

### 3.10 Cache invalidation/deletion/rebuild

Invalidate a cache exactly when any bound dependency changes or fails verification: root/semantic release, canonical member root, cache schema, builder implementation, relevant config/parameters, or the cache's own integrity.

Stale/corrupt cache behavior is `ignore -> delete/quarantine -> deterministic rebuild from verified canonical release`. Never patch stale entries in place into apparent freshness; never fall back to a stale cache because canonical reads are slow.

Verification-status caches are hints only. They may schedule work, but they cannot substitute for the verification gate in a new process/session.

### 3.11 Deterministic replay/rebuild

Replay receipt must map:

`immutable source snapshot + accepted extraction/decoder receipt + frozen compiler/authority contract + build profile -> semantic_release_id + logical member digests + physical_root_id + publication verification receipt`.

Same governed inputs must reproduce the same semantic identity, logical member digests, reconstructed objects, ExactRefs/content hashes, I03/I05/I04 behavior, and query results. If the physical profile declares byte reproducibility, the physical root must also match. Otherwise byte-different roots may be admitted only after independent semantic equivalence proof; byte difference is never silently treated as irrelevant.

Randomness, wall-clock time, temporary paths, directory enumeration order, process IDs, locale, and unspecified encoder defaults may not enter identity-producing logic.

### 3.12 No hidden second canonical database

Persistent DuckDB/PostgreSQL/SQLite/Arrow/materialized-long/index stores are forbidden as a hidden second empirical authority. In-memory/transient execution remains lawful. A persistent accelerator is permitted only if it is explicitly non-authoritative, disposable, root-keyed, correctness-bypassable, and contains no unique information.

Raw source snapshots remain separate source evidence under existing law; legacy database material remains historical/compatibility evidence under its own governance and does not become fallback C11 truth.

### 3.13 Shadow migration and rollback

A future carrier begins as `SHADOW_CANDIDATE__NON_SERVING__NONAUTHORITATIVE`. It may be built and queried for equivalence proof, but only the current admitted root supplies empirical evidence to production consumers.

Promotion requires full integrity verification plus the independent semantic equivalence/admission court; then the serving role changes atomically. Dual-serving canonicals are forbidden.

The displaced carrier may temporarily exist only as `ROLLBACK_CANDIDATE__NON_SERVING__NONAUTHORITATIVE`, excluded from query and cache-builder paths. There is no automatic fallback to it when the new carrier errors; automatic fallback would recreate a hidden second authority. Explicit rollback requires fresh integrity verification of the rollback target and an atomic operator-governed promotion.

If the one-authoritative-copy storage law is interpreted to forbid retaining a complete rollback candidate that duplicates C11 bytes even while non-serving, synthesis must choose deterministic rebuild-from-source rather than weakening the one-copy law. R05 does not unilaterally settle that cross-cell storage-policy question.

## 4. WHAT_CHANGES_PHYSICALLY

A future replacement adds immutable root/member manifests, whole-member hashes, domain-separated chunk/row-group integrity roots, explicit canonical coverage metadata, an atomic publication staging/seal/promote protocol, and root-keyed disposable cache namespaces.

It may physically split hot/cold canonical material, source-local compiled members, columnar/matrix/bitmap members, sparse exception members, and completeness metadata, but every such canonical member remains under one sealed root. Cold is a latency property, not a weaker authority class.

No current production code is modified by this return.

## 5. WHAT_MUST_NOT_CHANGE_LOGICALLY

The replacement must preserve exactly:

- source identity and all source-native physical distinctions admitted by C11;
- complete respondent incidence and arbitrary lawful respondent conjunction;
- M01-M18;
- ExactRef, object/content-hash, provenance, replay, and authority identities;
- raw versus authorized canonical value separation;
- physical missingness versus semantic response/absence;
- routing/applicability/risk-set distinctions;
- repeated/multiple/ordered/ranked topology;
- weights/design/measure authority;
- source relation/nonduplication provenance;
- I03 positive **and negative** truth conditions;
- I05 bounded discovery over unforeseen lawful combinations;
- I04 structural admission;
- downstream carrier ignorance.

Integrity metadata may prove that bytes are the sealed bytes. It may not create semantic meaning, repair unknowns, reinterpret missingness, or turn absence of verified evidence into negative evidence.

## 6. INFORMATION_ACCOUNT

The canonical root contains every unique empirical fact, every unique authority/provenance fact required for exact replay, and every completeness structure required to establish the scope of positive/negative queries. Redundant material may be physically omitted only under an allowed derivability disposition documented in `INFORMATION_PRESERVATION_LEDGER.csv`.

No semantic information is assigned to physical row order. Dense ordinals, chunk ordinals, local matrix coordinates, bitmap positions, and partition paths are execution locators only unless separately frozen source-native authority says otherwise.

Caches are outside the information-preservation proof because correctness survives total cache deletion. If deletion changes an answer or makes an exact negative answer impossible except by trusting the deleted structure, that structure was canonical and was misclassified as cache.

## 7. ASSUMPTIONS_AND_AUTHORITY

Primary authority is the complete closed machine plus Authorities 52/53, source-native constitution, decoder contract, R4 acceptance/scale law, and existing transient/canonical-copy law. R4 implementation details are treated only as current expectations to preserve, not as semantic authority.

Material assumptions are enumerated in `ASSUMPTION_LEDGER.csv`. The most dangerous assumptions are:

- the release selector has an external trusted authorization path; a valid hash alone cannot say which root is authorized;
- the storage substrate's atomic rename/commit and durability semantics are real and tested;
- exact verified bytes are the exact bytes interpreted;
- any canonical completeness index is actually complete and root-bound;
- the chosen hash algorithms remain cryptographically acceptable and are versioned for migration.

Failure of any of these converts the design from optimization to integrity theater.

## 8. HOSTILE_COUNTEREXAMPLES

`HOSTILE_CASES.csv` and `SELF_RED_TEAM.md` enumerate the attack surface. The highest-risk cases are:

1. verify only a hit chunk, then claim a global negative/denominator from unverified chunks;
2. use a stale bitmap/index miss as proof that no respondent qualifies;
3. mark a whole file verified after verifying only its footer/metadata;
4. hash a file, then let a query engine reopen a mutable path and consume different bytes;
5. treat hot members as verified authority while silently ignoring corrupt cold provenance/topology;
6. let cache rescue a corrupt canonical member;
7. crash between member publication steps and expose a mixed release;
8. serve from both old and new carriers during migration and resolve disagreement opportunistically;
9. use `latest` directory/mtime as root authorization;
10. assume a same semantic release must have byte-identical Parquet despite no byte-reproducibility contract.

Every one is rejected by the proposed contract.

## 9. I03_I05_I04_EFFECT

I03: exact positive answers require verified evidence closure; exact negative answers require verified coverage closure. This is stronger than hit-only lazy verification and preserves the distinction between `no qualifying evidence` and `unverified region not read`.

I05: discovery candidate generation may use cache/bitmap pruning only as an over-approximation or through canonical completeness-proven indexes. Unforeseen combinations cannot disappear because a designer failed to pre-index them. Any candidate suppression capable of a false negative must be followed by canonical fallback or is forbidden.

I04: structural admission receives only evidence derived from a query-closed or fully verified canonical release. Cache/shadow/legacy material cannot become positive structural evidence. Integrity failure therefore propagates as unavailable/blocked evidence according to existing admission law, never as a substitute semantic claim.

## 10. INTEGRITY_REPLAY_EFFECT

Integrity strengthens from flat member hashes to a hierarchy while retaining full flat verification. Replay gains a clear separation between semantic/logical identity and exact physical realization.

The expected steady-state trust chain is:

`authorized physical_root_id -> verified root manifest -> verified member manifest -> verified whole member or exact verified chunks -> query verification closure -> empirical result`.

A semantic replay court separately proves:

`source/extraction/decoder/authority/compiler inputs -> same semantic_release_id + logical member digests + same observable semantics`.

Neither chain substitutes for the other: cryptographically intact wrong semantics can still be wrong, and semantically intended bytes that fail integrity are still inadmissible.

## 11. RESOURCE_EXPECTATION

No performance improvement is claimed in this reconnaissance.

Hierarchical verification should permit bounded first-query reads when query closure is narrow, while keeping an O(release-bytes) streaming full audit. Root/member manifests add fixed metadata; chunk hashes add approximately one digest plus descriptor per chunk/row group. Smaller chunks improve verification selectivity but increase manifest/hash overhead; larger chunks do the reverse.

Atomic staging can temporarily require near one additional release-sized physical footprint and must be accounted separately as `ATOMIC_STAGING_PEAK_BYTES`, never retained as steady-state canonical duplication. Cache bytes remain separately reported and deletable.

`BENCHMARK_PLAN.md` requires measurement before any speed/storage claim is admissible.

## 12. COMPLEXITY_COST

The proposal introduces real complexity:

- two release identities rather than one overloaded checksum;
- immutable root/member schema versioning;
- chunk tree generation and verification;
- query dependency/coverage closure planning;
- TOCTOU-safe read plumbing;
- atomic publication and selector CAS;
- corruption quarantine and explicit rollback workflow;
- root-keyed cache invalidation.

This complexity is justified only if partial verification materially improves reopen/query cost without weakening evidence. If dependency closure routinely expands to whole-release verification, the Merkle machinery may not earn its operational cost; retain flat full-member verification instead.

## 13. RAW_SOURCE_PROBES_IF_ANY

None.

No named integrity/replay question required raw source. Checked-in whole-machine, C11/R4, source constitution, decoder, and storage authorities were sufficient.

## 14. REASONS_TO_REJECT_OWN_PROPOSAL

Reject the proposal if any of the following holds:

- the query engine cannot prove that verified bytes are the bytes consumed;
- negative/aggregate/discovery dependency closure cannot be computed conservatively without hidden semantic assumptions;
- a proposed speed index can create false-negative candidate suppression and canonical fallback is not guaranteed;
- the storage substrate lacks proved atomic/durable publication semantics;
- root authorization depends on mutable directory ordering/mtime rather than explicit trusted control state;
- caches contain unique information or are required for correctness;
- shadow/rollback operation requires two simultaneously serving authorities;
- chunk-hash overhead/complexity gives no measured advantage over current member hashing;
- the design would weaken the existing streaming full-audit path;
- the semantic/physical identity split cannot be reconciled with the independent equivalence oracle.

The strongest self-rejection is simple: if lazy verification cannot prove closure, do not ship lazy verification.

## 15. FALSIFICATION_CONDITIONS

The proposed architecture is falsified by any bounded hostile court demonstrating one of:

- a corrupt/unverified canonical byte changes an emitted result without detection;
- an exact negative result is emitted while a refuting canonical region remains unverified;
- a cache false negative suppresses a lawful I05/I03 result;
- a cache survives dependency-root change and affects an answer;
- a canonical integrity failure is masked by cache/legacy/shadow fallback;
- a crash exposes a release containing members from two roots;
- a post-verification mutation can be consumed without a failed verification;
- a rebuild from identical governed inputs changes semantic identity/logical member digests/results;
- an explicitly `BYTE_REPRODUCIBLE` profile changes physical root under identical inputs;
- rollback activates a target without fresh verification;
- deletion of all non-authoritative caches changes correctness;
- a persistent database becomes necessary to recover empirical truth not present under the canonical root.

## 16. SYNTHESIS_REQUIREMENTS

HQ/cross-cell synthesis must resolve these interfaces before any production implementation:

1. R02 must provide the exact canonical grain/functional-dependency and reconstruction inventory that R05 root/member coverage must bind.
2. R03 must define the independent semantic equivalence oracle and acceptance receipt that authorizes a new physical root as representing the same semantic release.
3. R04 must expose exact vector/matrix/bitmap member and row-group/chunk dependency surfaces so query verification closure is computable without semantic leakage.
4. R01 must align staging, bounded-memory writes, flush/commit semantics, and crash cleanup with R05 atomic publication.
5. R06 must test zero-destruction migration, concurrency, operational recovery, and any one-copy-versus-rollback-retention conflict.
6. HQ must designate the trusted root-authorization/active-selector authority and lifecycle. A content hash authenticates content, not organizational authorization.
7. Hash algorithms, canonical serialization of manifests, domain-separation strings, chunking profile, and algorithm-migration law must be frozen before implementation.
8. The full current member/release audit must remain available and must be part of acceptance even if lazy verification is introduced.
9. Any canonical completeness index used to prove absence must be included under the root and in the information-preservation ledger; it cannot be called cache.

## 17. RECOMMENDATION

`ADMIT_FOR_SYNTHESIS__WITH_HARD_FAIL_CLOSED_PRECONDITIONS`

R05 recommends hierarchical root/member/chunk integrity, atomic content-addressed publication, deterministic semantic/physical replay identities, and aggressively disposable root-keyed caches **only** under the verification-closure law above.

Do not authorize production lazy verification merely because Merkle proofs exist. Merkle proofs authenticate selected bytes; they do not prove that the selected bytes are sufficient for the query. Sufficiency is the hard problem, and it must fail closed.

Required return token:

`POST_R4_R05_INTEGRITY_PUBLICATION_RETURNED`
