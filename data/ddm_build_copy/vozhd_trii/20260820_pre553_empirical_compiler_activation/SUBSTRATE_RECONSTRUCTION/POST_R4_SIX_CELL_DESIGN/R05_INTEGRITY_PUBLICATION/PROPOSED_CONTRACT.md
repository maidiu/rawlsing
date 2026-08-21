# R05 PROPOSED CONTRACT — FAIL-CLOSED CANONICAL PUBLICATION AND VERIFICATION

Status: `DESIGN_ONLY__NON_DISPOSITIVE`

This contract is a synthesis candidate for any future replacement C11 carrier. It does not authorize production implementation.

## 1. SCOPE

The contract governs:

- canonical release/root identity;
- member and sub-member integrity;
- empirical-read authorization;
- atomic publication and crash behavior;
- corruption quarantine/recovery;
- deterministic replay/rebuild;
- non-authoritative cache lifecycle;
- shadow migration and rollback;
- one-authoritative-copy discipline.

It is carrier-neutral. Long-form Parquet, normalized relations, source-local compiled relations, columnar/matrix/bitmap layouts, and late-materialized virtual long projections may comply only if all requirements below are met.

## 2. TERMS

### `semantic_release_id`

Deterministic identity of the complete logical empirical release under frozen source/extraction/decoder/compiler/authority/coverage/reconstruction law.

### `physical_root_id`

Cryptographic identity of one exact immutable physical realization of that semantic release.

### `canonical member`

An immutable root-listed member containing unique empirical information, unique replay/authority information, or canonical completeness information required for exact results.

### `cache`

`NONAUTHORITATIVE__REGENERABLE_CACHE`: material whose total deletion cannot change correctness and which contains no unique empirical truth.

### `verification closure`

The exact root-bound set of canonical dependencies whose integrity and coverage have been proven sufficient for one exact query/result.

### `active selector`

Tiny trusted control state naming the one physical root authorized to serve. It does not contain empirical truth.

## 3. ROOT TRUST AND IDENTITIES

1. A release MUST have a deterministic `semantic_release_id`.
2. A physical realization MUST have a cryptographic `physical_root_id`.
3. The semantic identity MUST bind immutable source/extraction/decoder/compiler/authority/coverage/logical-member identity sufficient to reproduce all frozen C11 behavior.
4. The physical identity MUST bind exact root/member manifests, byte hashes, chunking profile, and hierarchical roots.
5. Incidental path names, wall-clock timestamps, process IDs, mutable aliases, and directory enumeration order MUST NOT enter semantic identity.
6. A physical profile MAY require byte reproducibility only if explicitly frozen as `BYTE_REPRODUCIBLE`.
7. Byte-different roots for a non-byte-reproducible profile MUST NOT be treated as interchangeable solely because a producer claims identical inputs. Independent semantic equivalence/admission remains required.
8. The root-digest preimage MUST be unambiguous and MUST NOT recursively depend on its own final digest value.
9. A valid `physical_root_id` authenticates content; it DOES NOT by itself authorize that root to serve. The active selector/trust authority MUST be explicit.

## 4. IMMUTABLE ROOT MANIFEST

The root manifest MUST bind at least:

- root schema/version;
- canonical serialization/version;
- hash algorithms and domain-separation version;
- `semantic_release_id`;
- physical/chunking profile;
- exact source snapshot and accepted extraction/decoder receipt identities;
- decoder/compiler/configuration/authority digests required by replay law;
- canonical release coverage declaration;
- ordered canonical member roles/identifiers and member-manifest digests;
- logical member digests;
- any canonical completeness/index member identities;
- replay/publication contract version.

The root manifest MUST be immutable after sealing.

Caches, scratch, staging, verification hints, access timestamps, and active-selector state MUST NOT be included as empirical canonical material.

## 5. MEMBER AND CHUNK MANIFESTS

Every canonical member MUST bind:

- exact release-local member identity and role;
- byte length;
- whole-member cryptographic hash;
- logical member digest;
- exact chunk/row-group profile;
- ordered chunk descriptors;
- hierarchical/Merkle root.

Every chunk descriptor MUST bind:

- member identity;
- chunk ordinal;
- byte offset;
- byte length;
- leaf digest.

Leaf and internal-node hash domains MUST be distinct. A leaf digest MUST bind member identity, ordinal, offset, length, and bytes so relocation/substitution cannot preserve meaning accidentally.

Whole-member hashing MUST remain available and mandatory for full audit. Hierarchical hashing is additive and MUST NOT replace the current whole-member/release verification path.

## 6. VERIFICATION STATE MACHINE

Permitted success states:

`UNSEEN -> ROOT_VERIFIED -> MEMBER_MANIFEST_VERIFIED -> CHUNK_VERIFIED / MEMBER_VERIFIED_FULL -> QUERY_CLOSED / RELEASE_VERIFIED_FULL`

Failure/containment states:

`INCOMPLETE`, `CORRUPT`, `QUARANTINED`.

Rules:

1. `ROOT_VERIFIED` proves only root-manifest integrity/authorization linkage.
2. `MEMBER_MANIFEST_VERIFIED` proves only member metadata belongs to the root.
3. `CHUNK_VERIFIED` proves only selected bytes belong to the sealed member/root.
4. `CHUNK_VERIFIED` MUST NOT authorize empirical output.
5. Empirical output requires `QUERY_CLOSED` for that exact result, or the stronger `RELEASE_VERIFIED_FULL`.
6. A persisted verification boolean from a prior process/session MUST NOT substitute for current cryptographic authorization.
7. Verification hints MAY schedule work but MUST NOT change correctness.

## 7. QUERY VERIFICATION CLOSURE

Before emitting an empirical result, the implementation MUST identify and integrity-close every canonical dependency whose content **or absence** can change that result.

### 7.1 Positive atomic claim

MUST verify:

- exact canonical bytes carrying the fact/incidence;
- exact state/type/value interpretation dependencies;
- exact identity/provenance/authority dependencies required by the claim;
- sparse/default exception coverage capable of changing the fact.

### 7.2 Aggregate/support/denominator/uncertainty

MUST verify every canonical region capable of:

- adding/removing a contributor;
- changing physical/semantic missingness classification;
- changing routing/applicability/risk-set membership;
- changing weight/design/measure authority;
- changing duplicate/nonduplication treatment;
- changing state or sparse overrides.

### 7.3 Negative/absence claim

MUST verify every canonical region in the governed domain capable of containing refuting evidence, unless a separately verified root-bound canonical completeness structure proves a smaller region exhaustive.

A cache miss, Bloom-filter miss, stale bitmap, previous query result, or unverified partition directory MUST NOT prove absence.

### 7.4 I05/discovery

Candidate-pruning acceleration MUST satisfy one of:

- canonical root-bound completeness proof; or
- non-authoritative over-approximation with mandatory canonical fallback such that false negatives cannot suppress lawful candidates.

Pre-indexed designer expectations MUST NOT define the discovery frontier.

### 7.5 Closure failure

If the implementation cannot prove a conservative verification closure, it MUST verify a broader member/release or fail closed. It MUST NOT emit a best-effort empirical result.

## 8. TOCTOU / CONSUME-AFTER-VERIFY

The bytes verified MUST be the bytes interpreted.

Preferred implementation contract:

`read immutable bytes -> hash/verify -> decode/query the same immutable bytes`.

If a backend reopens a mutable path or cannot prove byte identity between verification and interpretation, partial verification MUST be disabled and the whole member MUST be verified before backend access.

File size, mtime, inode, path, memory-map identity, OS page cache, and ungovened ETags MUST NOT count as cryptographic authorization.

## 9. ATOMIC PUBLICATION STATE MACHINE

A publisher MUST use a unique non-serving staging area in a storage/durability domain with proved commit semantics.

Required sequence:

1. `BUILD_STAGING` — write all canonical members/manifests.
2. `SEMANTIC_VALIDATE` — complete required logical reconstruction/equivalence checks.
3. `INTEGRITY_SEAL` — compute/verify whole-member hashes, chunk roots, root manifest, and physical root.
4. `FULL_STAGED_VERIFY` — prove the staged release is internally complete and consistent.
5. `DURABLE_FLUSH` — durably persist bytes/manifests/directories under the substrate-specific protocol.
6. `CONTENT_ADDRESS_PROMOTE` — atomically promote to immutable `releases/<physical_root_id>` or an equivalently strong primitive.
7. `SEALED_REOPEN_VERIFY` — independently reopen/verify the promoted root.
8. `ACTIVE_SELECTOR_CAS` — atomically compare-and-swap active selector from the expected old root to the newly verified root.
9. `CLEANUP` — remove staging/scratch/cache material under explicit lifecycle law.

No empirical reader may discover or serve staging.

## 10. CRASH / INCOMPLETE RELEASE LAW

| Crash point | Required post-crash state | Serving authority |
|---|---|---|
| before integrity seal | incomplete staging only; disposable | old active root |
| after seal before durable promotion | non-serving staged/sealed candidate | old active root |
| after content-address promotion before selector CAS | complete inactive root may remain | old active root |
| during failed selector CAS | no partial selector state; candidate inactive | whichever root CAS law leaves active |
| after successful selector CAS | new root active; old no longer serving | new active root |

Readers MUST observe one root identity for an entire query/transaction. Mixed-root reads are forbidden.

Publication of the exact same root SHOULD be idempotent. An existing root identifier with divergent content MUST trigger catastrophic integrity/collision handling, not overwrite.

Concurrent publishers MUST use content-addressed roots plus selector compare-and-swap. A losing publisher MUST NOT overwrite a winning root or selector.

## 11. CORRUPTION LAW

Any canonical root/member/chunk integrity mismatch MUST:

1. classify the physical release `CORRUPT`;
2. block new empirical output from that physical release;
3. transition it to `QUARANTINED` for serving;
4. preserve diagnostic evidence according to operational law;
5. recover only via deterministic rebuild or explicit activation of a separately verified/admitted equivalent release.

The implementation MUST NOT:

- serve supposedly unaffected partitions by default after discovered canonical corruption;
- repair canonical bytes from cache;
- fill missing/corrupt canonical evidence from legacy PostgreSQL/SQLite/DuckDB;
- auto-fallback to a shadow/rollback carrier.

## 12. CACHE CONTRACT

Every cache MUST be marked `NONAUTHORITATIVE__REGENERABLE_CACHE` and MUST satisfy all:

1. no unique empirical information;
2. correctness unchanged after total cache deletion;
3. correct canonical bypass path exists;
4. cache namespace/key binds all relevant immutable dependencies: release/root/member identity, schema/kind, builder implementation digest, relevant canonical config/parameters;
5. stale/corrupt behavior is `ignore -> delete/quarantine -> deterministic rebuild from verified canonical`;
6. canonical disagreement invalidates cache; canonical is never rewritten to match cache;
7. canonical corruption blocks evidence; cache cannot rescue;
8. a completeness structure required to prove exact absence is canonical material and MUST NOT be mislabeled cache;
9. verification-state caches are hints only and MUST NOT authorize later-process reads.

Persistent analytical stores are permitted only as accelerators if they satisfy this cache contract. A persistent DuckDB/PostgreSQL/SQLite/Arrow store containing unique or required truth is forbidden.

## 13. CACHE INVALIDATION / DELETE / REBUILD

A cache MUST invalidate when any bound dependency changes or fails verification, including:

- semantic or physical release root;
- relevant member/chunk root;
- cache schema/kind;
- builder implementation;
- relevant canonical configuration/parameters;
- cache integrity.

Invalidation MUST NOT patch stale entries into apparent freshness. Rebuild MUST originate from a currently verified canonical release, not from another stale cache.

Deleting every cache MUST be an explicit acceptance court.

## 14. DETERMINISTIC REPLAY / REBUILD

The replay receipt MUST bind:

`immutable source snapshot + accepted extraction/decoder receipt + frozen compiler/authority contract + build profile -> semantic_release_id + logical member digests + physical_root_id + publication verification receipt`.

For identical governed inputs, rebuild MUST reproduce:

- semantic release identity;
- logical member digests;
- reconstructed semantic objects;
- ExactRefs/content hashes/object IDs;
- I03/I05/I04 observable behavior;
- exact query results.

If the profile is `BYTE_REPRODUCIBLE`, physical root MUST also match. Otherwise physical-root difference requires explicit equivalence/admission before substitution.

## 15. SHADOW MIGRATION

A replacement carrier MUST begin as:

`SHADOW_CANDIDATE__NON_SERVING__NONAUTHORITATIVE`.

It MAY be built, fully verified, benchmarked, and queried for equivalence proof. It MUST NOT supply production empirical evidence before admission.

Promotion requires:

- complete integrity verification;
- independent semantic equivalence/admission;
- atomic change of the one serving root role.

Old and new carriers MUST NOT both serve and runtime MUST NOT choose between them opportunistically.

## 16. ROLLBACK

A prior carrier/root MAY exist only under explicitly synthesized retention law as:

`ROLLBACK_CANDIDATE__NON_SERVING__NONAUTHORITATIVE`.

Rollback MUST:

- be explicit/operator-governed;
- freshly verify the rollback target;
- atomically promote it through the same active-root mechanism;
- never happen as automatic error fallback.

If retaining a full rollback candidate conflicts with the one-copy steady-state law, the system MUST rebuild/restore deterministically rather than preserve duplicate canonical bytes. R05 does not weaken the one-copy rule.

## 17. C13 / C20 / C21 INTEGRITY BINDINGS

### C13 — hot/cold

Hot and cold canonical material MUST remain under the same root. Cold material MAY be fetched later but MUST NOT be treated as weaker, optional, or non-authoritative when query closure depends on it.

### C20 — source-local compilation

Source-local physical compiler identity/configuration MUST be replay/root-bound. Below the C11 boundary, I03/I05/I04 and downstream stages MUST NOT branch on source family or physical carrier choice.

### C21 — columnar/matrix/bitmap

The root MUST bind sufficient canonical material to reconstruct exact respondent/variable incidence, typed state/value, routing/applicability, weights/design, topology, provenance, sparse exceptions, and frozen identities. Physical row/column/bitmap position MUST remain execution-only unless separately source-authorized.

## 18. FORBIDDEN DESIGNS

The following are contract violations:

- `verified chunk == safe answer` without closure proof;
- cache/index miss as negative evidence;
- footer-only verification represented as full-member integrity;
- consume-after-verify from mutable reopened bytes;
- hot-only authority while cold canonical dependencies remain unverified;
- persistent `verified=true` as later-process authorization;
- automatic cache/legacy/shadow fallback on canonical corruption;
- selecting `latest` root by filesystem incidental state;
- mixed-root queries;
- dual-serving old/new carriers;
- retained hidden persistent empirical database required for correctness;
- removal of current streaming full audit to gain reopen speed.

## 19. ADMISSION CHECKLIST

A future implementation is not admissible until all are true:

- [ ] immutable root/member/chunk schema frozen;
- [ ] trusted active-root authorization law frozen;
- [ ] canonical manifest serialization and domain separation frozen;
- [ ] full member/release audit retained;
- [ ] query closure conservatively proven for positive/negative/aggregate/discovery courts;
- [ ] exact consume-after-verify guarantee proven;
- [ ] cache deletion leaves correctness unchanged;
- [ ] no hidden persistent second canonical database;
- [ ] publication crash injection proves old-or-new never mixed;
- [ ] concurrent publication CAS proved;
- [ ] corruption quarantines and never cache-falls-back;
- [ ] deterministic semantic rebuild proved;
- [ ] byte-reproducible physical profiles separately proved if claimed;
- [ ] shadow promotion requires independent semantic equivalence;
- [ ] rollback is explicit and freshly verified;
- [ ] C13/C20/C21 physical designs preserve complete root-bound reconstruction/coverage;
- [ ] no performance target has weakened any integrity invariant.

Until then, fail closed.
