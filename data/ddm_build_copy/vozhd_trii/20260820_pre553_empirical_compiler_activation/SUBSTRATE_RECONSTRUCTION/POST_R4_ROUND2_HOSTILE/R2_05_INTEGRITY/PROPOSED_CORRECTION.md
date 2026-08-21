# R2-05 PROPOSED CORRECTION — MINIMUM FAIL-CLOSED INTEGRITY / ACTIVE-ROOT / ONE-COPY CONTRACT

Status: `ROUND2_CORRECTION_ONLY__NO_RUNTIME_AUTHORIZATION`

This document narrows and hardens P0. It is not a production implementation. It deliberately removes mandatory chunk/Merkle integrity from the P0 core.

## 1. Normative objective

A future P0 carrier must make the following impossible:

- corrupt/incomplete canonical bytes becoming an ordinary empirical negative or positive;
- stale/cache/shadow/legacy material rescuing canonical corruption;
- a valid-but-unadmitted root serving;
- two publication transactions silently winning through selector ABA;
- one query consuming members from two roots;
- a query verifying bytes and interpreting different bytes;
- a cache/index miss proving absence;
- a retained rollback copy becoming a standing second canonical database.

The minimum solution is a flat authenticated member graph plus a trusted generation-stamped activation record.

## 2. Minimum identity graph

The canonical physical graph is:

```text
physical_root_id
  = H(ROOT_DOMAIN || canonical_root_manifest_preimage)

root manifest
  -> semantic_release_id
  -> source / decoder / compiler / authority / schema / replay identifiers
  -> member_inventory_digest
  -> logical_release_digest / logical member digest closure
  -> publication/integrity contract version

member inventory (streamed, canonical, exhaustive)
  -> record[0]
  -> record[1]
  -> ...

member record
  = {
      member_role,
      release_local_member_id,
      member_schema_version,
      byte_length,
      whole_member_byte_hash,
      logical_member_digest,
      canonical_coverage_scope
    }

canonical member bytes
  -> exact empirical / metadata / topology / routing / weight / provenance / replay material
```

There is no mandatory per-member Merkle manifest and no mandatory whole-release concatenated checksum.

### Root versus member hash job separation

- `physical_root_id` authenticates the expected composition and interpretation contract.
- `whole_member_byte_hash` authenticates actual bytes for one listed canonical member.

These jobs are non-redundant. Additional checksums need an independent named failure unit or remain diagnostics.

## 3. Semantic identity remains separate

`semantic_release_id` must remain deterministic under the frozen source/C11/replay law and independent of physical row-group/file/chunk/compression accidents.

The root manifest binds that semantic identity and the logical member digests, but the physical root does not self-certify semantic correctness. A newly built physical root enters serving authorization only after the independent semantic/equivalence/admission court accepts it.

A non-byte-reproducible rebuild may produce a different physical root for the same semantic release. That new root is still a new physical candidate and may not self-substitute.

## 4. Canonical member inventory law

The inventory is the sole physical membership authority.

Each record must be canonical and unambiguous and must bind enough logical coverage to answer:

> Can this member contain or alter evidence relevant to exact scope/query Q?

The coverage descriptor may name relation/family, source/release scope, question/block scope, respondent/source-row ranges where lawfully physical, exception/default scope, or another source-neutral deterministic partition descriptor. It may not encode semantic shortcuts unsupported by frozen C11/source law.

A reader may exclude a member from a query only when the verified root-bound coverage descriptor proves it outside the governed query/refuting domain. If exclusion is uncertain, verify/search the member or a broader set.

Unreferenced directory files are noncanonical garbage. Directory enumeration never creates membership.

## 5. Member-level verification closure

P0 minimum verification unit is the **whole canonical member**.

For exact query `Q`, define `C(Q)` as every root-listed member whose contents or absence can change:

- target incidence/value/state;
- respondent inclusion/exclusion;
- routing/applicability/risk set;
- weight/design/measure;
- topology/multiplicity/order/rank;
- sparse/default exception resolution;
- authority/provenance/source relation;
- exact identity/replay material;
- a negative/absence/completeness conclusion.

Before output:

1. verify root manifest;
2. verify complete member inventory;
3. derive `C(Q)` only from root-bound canonical coverage and frozen query authority;
4. verify full byte hash/length/schema of every member in `C(Q)`;
5. consume those exact immutable member generations;
6. construct the uniform validated C11 view and run exact semantics;
7. revalidate active-selector generation before empirical emission.

If `C(Q)` cannot be conservatively bounded, use a broader member set or full release. Never replace unknown closure with a cache miss.

### Negative/absence law

`no match`, `zero support`, `VALID_EMPTY`, or equivalent normal negative is permitted only after every canonical member capable of refuting that negative is inside the verified/exhausted closure or excluded by independently accepted root-bound completeness law.

`INCOMPLETE`, `CORRUPT`, selector failure, or TOCTOU failure precedes query semantics and cannot be converted into a normal negative state.

## 6. Consume-after-verify contract

Verification is valid only if the bytes interpreted are the bytes verified.

Required storage abstraction:

```text
ImmutableMemberHandle {
    physical_root_id
    member_id
    immutable_generation_or_snapshot_id
    length
    verified_whole_member_hash
    read_interface_used_by_query_backend
}
```

The query backend must consume the same immutable generation/handle that was hashed.

Forbidden:

- hash pathname, then backend reopens pathname;
- hash one object version, then unversioned object-store GET;
- use inode/mtime/size as identity;
- use a prior-process verified boolean as cryptographic proof;
- resolve members through a mutable `current` symlink/alias after query authorization.

If the selected backend cannot consume an immutable verified handle/snapshot, the backend integration fails. Merkle does not solve this problem.

## 7. Active-root authorization record

A valid root is not automatically authorized.

Minimum trusted record:

```text
ActiveRootRecord {
    serving_slot
    activation_generation
    semantic_release_id
    physical_root_id
    admission_receipt_id
}
```

Properties:

- `serving_slot` identifies the organizational publication channel;
- `activation_generation` is never reused for that slot;
- `semantic_release_id` must match root manifest and accepted target;
- `physical_root_id` names the exact immutable physical realization;
- `admission_receipt_id` names the exact independent equivalence/admission act authorizing that realization for that semantic target/slot.

The active-selector store must provide:

- linearizable/non-stale reads;
- durable atomic writes;
- compare-and-swap against the **complete expected prior record**;
- generation advance on every activation/rollback;
- no heuristic recovery from directory state.

A missing/corrupt/unavailable active record means no root is authorized to serve until control state is recovered explicitly.

## 8. ABA-safe activation

Unsafe:

```text
CAS(expected_root=A, new_root=C)
```

Safe shape:

```text
CAS(
  expected={slot=S, generation=41, semantic=X, root=A, receipt=RA},
  new={slot=S, generation=42, semantic=X, root=C, receipt=RC}
)
```

If another activation/rollback occurs, generation changes. Even if root `A` later becomes active again, a stale publisher expecting generation 41 cannot succeed.

Generation must not reset/wrap/reuse. Equivalent unique predecessor-linked activation tokens are acceptable if they provide the same ABA resistance under the trusted selector store.

## 9. Query root pin and authorization point

At query start:

1. read one authoritative `ActiveRootRecord`;
2. verify root/semantic/admission linkage;
3. pin that exact selector token and physical root;
4. never consult a mutable `current` alias for member reads.

At result emission:

1. reread authoritative selector;
2. if exact selector token/generation is unchanged, this check is the query's linearization/authorization point and the result may emit;
3. if changed, discard/retry against the new active root.

A selector CAS after the successful final check logically occurs after that query's authorization point. This provides a precise old-versus-new ordering without mixed-root reads.

## 10. Atomic publication state machine

Required states:

```text
ABSENT
 -> UNIQUE_STAGING_NON_SERVING
 -> COMPLETE_STAGING
 -> SEMANTICALLY_ACCEPTED_CANDIDATE
 -> INTEGRITY_SEALED_STAGING
 -> FULLY_VERIFIED_STAGING
 -> DURABLY_PROMOTED_INACTIVE_ROOT
 -> SEALED_REOPEN_VERIFIED_INACTIVE_ROOT
 -> ACTIVE_BY_ABA_SAFE_CAS
 -> OLD_ROOT_DRAINING_TRANSIENT
 -> OLD_ROOT_DELETED
 -> MIGRATION_SETTLED
```

Required order:

1. build all canonical members in unique staging;
2. finish frozen semantic reconstruction and independent oracle/admission checks;
3. write and close canonical streamed member inventory;
4. compute whole-member hashes/logical digests and inventory digest;
5. write immutable root manifest and compute physical root;
6. full staged verification;
7. durable flush under target-specific protocol;
8. atomic content-address promotion to immutable root namespace;
9. independently reopen and verify promoted root/members required by activation acceptance;
10. CAS exact active record with generation advance;
11. stop authorizing new reads against old root;
12. drain old pinned handles;
13. delete displaced complete root;
14. declare migration settled only after deletion/cleanup.

Crash/failure before step 10 leaves prior active root authoritative. A complete promoted candidate remains inactive. Failure after step 10 does not authorize automatic old-root fallback.

## 11. Concurrent publishers

Two publishers can produce candidates concurrently, but only one can activate from a given expected selector generation.

- same exact root: publication may be idempotent, but activation still follows selector transaction law;
- distinct roots, same semantic release: one CAS wins; loser remains inactive;
- different semantic releases: candidate must additionally match serving-slot semantic/admission policy; one generation wins.

A loser never overwrites the winner or infers authority from a newer filename/mtime.

## 12. Canonical corruption and quarantine

Any detected mismatch in root manifest, inventory, required canonical member hash/length/schema/logical replay closure, or consume-after-verify identity yields integrity failure before semantic result emission.

After a canonical mismatch is detected:

```text
ACTIVE_VALID -> CORRUPT_DETECTED -> QUARANTINED_NON_SERVING
```

No new empirical output from that physical root is permitted. No cache, old root, shadow root, legacy database, or historical result repairs or fills the canonical evidence.

Recovery paths:

- deterministic rebuild/restore from governed inputs, then full admission/publication; or
- explicit activation of a separately verified/admitted equivalent physical root under a new activation generation.

## 13. Cache law — minimum safe role

Default cache status:

`NONAUTHORITATIVE__REGENERABLE_HINT_OR_ACCELERATOR`

Required cache key dependencies include, as applicable:

- semantic release identity;
- physical root identity;
- exact predicate/index/query-plan definition;
- authority/risk/measure dependencies;
- cache schema/kind;
- builder implementation/version;
- relevant canonical configuration.

Minimum correctness restrictions:

1. cache deletion changes no empirical result/replay/discovery reachability;
2. cache hit can suggest candidate bytes/refs/read order but final evidence is canonically verified;
3. cache miss/nonmembership cannot exclude a canonical member/respondent/candidate or prove absence;
4. malformed/stale/corrupt cache is ignored/deleted and canonical path continues;
5. canonical corruption disables cache as evidence; no cache rescue;
6. no cache builds from another cache as its only empirical source;
7. persistent `verified=true` is only a hint.

If performance requires trusting an exact negative index to prune canonical search, that object is not a cache: it becomes canonical root-bound completeness material and faces the full semantic/integrity oracle.

Direct cached final empirical answers are outside the minimum P0 design.

## 14. One-copy shadow migration and rollback

### Build/shadow period

The current root is the sole serving canonical authority. The replacement is `SHADOW_CANDIDATE__NON_SERVING` and its bytes count as transient staging/migration peak, not steady-state canonical truth.

### Activation period

ABA-safe CAS makes new root the only root eligible for new/current empirical authorization. The displaced root becomes `OLD_ROOT_DRAINING_TRANSIENT__NONAUTHORITATIVE`.

### Settlement

After pinned readers drain, delete the displaced full root. Migration is not considered successful/settled until this deletion and staging cleanup complete. The post-success steady state contains one C11-equivalent canonical root plus tiny required control/audit metadata and optional disposable caches.

### Rollback before settlement

If old bytes still exist in the transient drain window, an operator may request rollback. The old root must be freshly integrity-verified and still semantically/admission-valid. Rollback is another ABA-safe activation with a new generation. The other root then drains/deletes.

### Rollback after settlement

No complete old C11 root is retained. Rollback requires deterministic rebuild/restore from governed source/authority/replay inputs, fresh semantic equivalence/admission, full integrity verification, and a new activation transaction.

There is never automatic error fallback.

## 15. Merkle/chunk ruling

### P0 core

`C14_MERKLE = REJECTED_FROM_CORE__NO_NAMED_NEED`

The minimum flat graph already detects:

- root tamper;
- missing/truncated/swapped member;
- cross-release composition;
- partial publication;
- stale active root;
- cache disagreement;
- negative completeness error when coverage is correctly root-bound;
- replay/config/schema mismatch;
- canonical corruption before a verified member contributes to output.

Whole-member hashing is bounded-memory and R01 permits bounded canonical shards/members.

### First escalation: flat chunks

Only after a measured court proves whole-member verification granularity is the remaining failed gate and smaller members are not acceptable. Add root-bound flat chunk records and immutable range handles. Query sufficiency remains separate.

### Second escalation: Merkle

Only after chunk verification itself is admitted and a flat chunk inventory/proof distribution is a named measured problem. Merkle may optimize inclusion proof size; it does not change semantic completeness law.

### Repair does not justify Merkle by itself

P0's recovery is deterministic rebuild/quarantine. No accepted requirement demands surgical canonical repair from untrusted cache ranges.

## 16. Full audit remains mandatory

Regardless of normal query closure, a bounded streaming full-release audit must:

- verify root and complete member inventory;
- hash every canonical member;
- reconstruct/audit the complete frozen logical C11/replay closure;
- detect all corruption injections;
- operate without corpus-scale Python retention.

No future lazy/chunk mechanism may remove this path.

## 17. Failure-state precedence

Integrity/control failures precede ordinary empirical semantics.

Examples:

```text
missing required member -> INCOMPLETE / INTEGRITY_FAILURE
member hash mismatch -> CORRUPT / INTEGRITY_FAILURE
selector unavailable/stale -> AUTHORIZATION_FAILURE
consume-after-verify mismatch -> INTEGRITY_FAILURE
coverage closure unproved -> CLOSURE_FAILURE / verify broader / no result
```

None may be normalized into:

```text
VALID_EMPTY
NO_MATCH
ZERO_SUPPORT
OBSERVED_ZERO
UNAVAILABLE_ROUTING
UNAVAILABLE_MEASURE
NONCOMPARABLE
```

unless the frozen semantic machinery reaches that state **after** integrity and authorization closure passes.

## 18. Acceptance conditions for Round-3 P0

Before implementation/prototype acceptance, synthesis should freeze and test:

- canonical root and member-inventory serialization/version;
- hash algorithm/version;
- member coverage descriptor law;
- trusted selector store semantics and ABA-safe CAS;
- active selector tuple/admission binding;
- root-pinned query authorization point;
- consume-after-verify storage adapter semantics;
- crash matrix for every publication boundary;
- cache deletion/stale/corrupt/false-negative courts;
- one-copy migration drain/delete behavior;
- rollback rebuild path;
- deterministic semantic replay;
- full streaming audit;
- explicit `NO_MERKLE_IN_P0_CORE` unless a new named court first admits C14.

Fail closed on any unclosed item.
