# R01 PROPOSED CONTRACT

Non-dispositive physical contract for synthesis. This does not authorize implementation or alter frozen source/C11 semantics.

## 1. Boundary

Input is an exact authority-governed logical C11 stream (or bounded source-incidence stream feeding frozen C11 construction). Output is one immutable exact-addressed sealed carrier release logically equivalent to frozen C11.

The carrier MUST NOT infer semantic fields from storage position, omit fields through unproved functional dependency, turn arrival/completion order into semantic order, deduplicate occurrences without frozen authority, make cache/index presence part of truth, expose an unsealed release, or weaken validation to achieve streaming.

## 2. Logical rows

Every frozen logical family remains reconstructible: public objects, internal records, replay manifest, release identity, M01–M18, authority/dependency refs, topology, routing/risk-set, weights/design, typed absence, and source-native distinctions conserved into C11.

Storage order is nonsemantic. Source-native order/rank/multiplicity stays in identity-bearing logical fields.

## 3. Bounded run formation

Finite configuration MUST bound `B_rows`, canonical payload bytes `B_payload_bytes`, workers `W`, queue capacities `Q`, merge fan-in `F`, final shard size/row groups, cache `C`, and backend dictionary/page/footer state `E`.

When a run reaches a bound, sort only that bounded run by canonical C11 storage key, write/close/hash it, append one streamed run receipt, and release live rows. A single row larger than the ordinary payload cap is preserved exactly as a singleton/streamed oversize row; it is never truncated. Memory reporting includes `Smax`.

## 4. External merge and duplicate law

Final canonical order MUST use fixed-fan-in external merge; run count > F requires deterministic multi-pass merge. Do not open all runs or retain all run heads.

Tie law:

1. exact frozen identity is primary;
2. authority-defined deterministic tie rule applies where one exists;
3. logical multiplicity is retained;
4. unresolved equal-key conflicting material FAILS CLOSED.

There is no physical first-write-wins, last-write-wins, dictionary overwrite, or unproved deduplication.

## 5. Final shards and streamed inventories

Each relation emits independently closed deterministic shards with bounded row groups/pages/footer state. Each inventory record contains at least relation/schema identity, shard ordinal/name, row count, encoded bytes, physical content hash, canonical lower/upper key bound where applicable, and physical encoding version.

Inventory framing MUST be incrementally writable/readable/hashable (e.g. NDJSON or length-prefixed records). No unbounded JSON member array/dictionary may be required.

## 6. Proposed root seal

Subject to R05 final authority, the root seal holds fixed-count descriptors per frozen relation rather than one field per shard and binds:

- carrier/schema version;
- exact source and release identity;
- semantic release/replay root;
- required M01–M18 identity/coverage digest;
- each relation inventory filename/hash, shard count, logical row count and relation digest;
- deterministic sort/tie authority identity;
- publication protocol version;
- seal hash.

Seal is written only after all final shards/inventories and frozen semantic validation are complete.

## 7. Transactional publication

Allowed state machine:

`ABSENT -> STAGING -> SEALED_STAGING -> COMMITTED_IMMUTABLE`

Procedure:

1. unique staging directory on same filesystem as target;
2. construct/merge only in staging;
3. close and stream-hash final shards;
4. close/fsync/hash relation inventories;
5. complete frozen semantic/replay validation;
6. write root seal last;
7. fsync seal and directory chain;
8. atomic rename sealed payload to exact immutable destination;
9. fsync destination parent;
10. optional convenience pointer only after commit and never as semantic authority.

Crash before step 8 leaves noncanonical staging only. Platform semantics that cannot prove this require an R05-approved transactional/CAS adapter.

## 8. Reader/reopen contract

Canonical reopen MUST NOT materialize complete relations. It MUST require exact selectors, verify root seal, stream/verify inventories and members, reproduce required semantic/replay validation with bounded passes/sorted joins, and only then expose an `INTEGRITY_VERIFIED_SEALED_RELEASE` handle.

The handle supports streaming relation iteration, exact object/ref reconstruction, exact counts/identity, replay/release-root access and bounded audit.

An eager compatibility materializer may exist only behind an explicit caller-supplied bound and must refuse to exceed it.

## 9. Exact lookup

Cache miss means only “not cached.” Inventory key bounds may skip shards only if verified and correctness-preserving. Candidate rows are exact-ref/content-hash checked. Absence is returned only after the complete authorized search domain is verified and exhausted. Conflicting candidates fail closed unless frozen law explicitly governs them.

O(N) worst-case scan is acceptable for this conservative correctness baseline; R04 may add independently proven acceleration.

## 10. Cache

C04 cache is finite, immutable-release-keyed, correctness-independent and deletable. Keys include complete semantic release identity plus exact lookup/query identity and any physical schema version needed for safe decoding. Negative entries require a complete verified negative resolution.

Eviction/deletion/rebuild MUST NOT change semantic result, failure state, replay identity or release validity.

## 11. Validation observability

Streaming replacement MUST preserve observable equivalents of frozen R4/C11 checks, including declared universe/authority/count checks; respondent namespace integrity; question/topology binding; distinct event occurrence; routing/risk set; weight/design typed absence; source-universe relation/default; authority resolution and unauthorized-promotion rejection; replay projection/closure/tie authority; semantic release-root reconstruction; exact selectors/content-addressed paths; and corrupt/missing member rejection.

Multiple bounded passes, external sorted joins or correctness-neutral disk-backed temporary indexes are permitted. Skipping a check is not.

## 12. Concurrency/backpressure

Every queue, worker pool, merge fan-in and reorder window is finite. Completion order cannot affect canonical rows, logical/semantic digest, duplicate treatment or failure disposition. A deterministic single-worker oracle path remains available.

## 13. Telemetry

Physical telemetry SHOULD cover phase/relation, rows/cells, logical/encoded bytes, run/shard counts, temp disk, current/peak RSS, queue depths/backpressure, open files/fan-in, cache size, throughput and crash-injection stage.

Telemetry is noncanonical and cannot influence semantic decisions or canonical content/order.

## 14. Memory acceptance

With `Smax` and configured bounds held fixed, writer and reader/audit peak live memory MUST asymptotically plateau as corpus N grows. Library/internal allocations count. Caller-side batching alone is not proof.

## 15. Upstream decoder dependency

The normal accepted decoder path supplies bounded batches, but the exact-encoding compatibility path currently retains a full frame. R01 forbids an **end-to-end bounded-memory** claim until equivalent bounded behavior is proven for that exact compatibility law. R01 does not authorize changing encoding/source authority.

## 16. I03/I05/I04

I03/I05/I04 receive the same file-neutral evidence and authority, never shard/cache details. I03 positive/negative truth is identical; I05 retains complete typed incidence for unforeseen combinations; I04 receives identical evidence/replay/authority roots.

## 17. Rejection rule

If any invariant cannot be reproduced with bounded live memory, return a named contradiction/blocker. Never weaken the invariant to make a resource metric pass.
