# R01 SELF RED TEAM

This document attacks the R01 proposal rather than arguing for it.

## 1. The proposal can lie about bounded memory while still batching rows

A fixed Python row batch does not prove a fixed-memory compiler. Parquet/Arrow may retain dictionaries, page statistics, column builders, footer metadata, compression buffers, or allocator arenas whose live state grows with cardinality. External merge may also accidentally open every run at once or retain every inventory/member descriptor.

**Required defense:** fixed-size independently closed shards; fixed merge fan-in; explicit dictionary/cardinality policy; streamed inventories; memory measurement of the actual backend. If RSS or allocator-owned live bytes scale with N under fixed `Smax`, the design is falsified.

## 2. External sort can silently become semantic redesign

The current C11 package projection is order-invariant because it canonicalizes refs. It does not authorize R01 to reorder a source-native sequence whose order/rank is itself evidence.

**Required defense:** sort only canonical storage records. Every source-native order/rank/occurrence fact remains an identity-bearing field inside the row. Any family whose semantics depend on arrival order but lacks an explicit identity/tie field must fail closed and be adjudicated; R01 cannot invent a tie rule.

## 3. Duplicate handling is a trap

A merge implementation naturally wants to deduplicate adjacent equal keys. That would be unauthorized information destruction. Conversely, returning the “last” matching row from a lookup would create an unapproved override law.

**Required defense:** retain multiplicity. No last/first-write-wins. Do not collapse repeated refs/rows unless the frozen C11 validator itself authorizes that exact idempotence. Conflicting/ambiguous identity is a validation failure or remains distinct according to exact refs; physical arrival order is never authority.

## 4. A lazy reader can accidentally weaken validation

Current reopen materializes all relations and then reconstructs/validates a sealed `C11LogicalRelease`. A lazy handle that yields rows without proving the whole closure could expose partially corrupt data before discovering a bad shard later.

**Required defense:** distinguish `UNVERIFIED_STREAM`, `INTEGRITY_VERIFIED_SEALED_RELEASE`, and per-object read states. Before a release is admitted to I03/I05/I04, root/inventory/member integrity and semantic/replay closure checks required by the frozen contract must complete. Streaming verification may make multiple bounded passes. “Lazy” is a memory property, not permission to defer a required fail-closed gate until after downstream use.

If whole semantic validation fundamentally requires a corpus-sized set that cannot be externalized, R01 has not solved the problem and must be rejected rather than weaken validation.

## 5. Exact random reconstruction may be unusably slow

The conservative resolver is O(N) worst case. That satisfies exactness and bounded memory but can make operational use unacceptable.

**Required defense:** admit the cost. R01 is a correctness baseline, not the R04 endgame. Synthesis may add an immutable physical index, but cache/index miss must never become semantic absence and index corruption must fall back to verified scan or fail closed.

## 6. “Fixed-size root seal” can hide an unbounded inventory problem

Moving a million shard hashes from a Python dictionary into one inventory file solves RAM only if the inventory itself is streamed for write, hash, audit and reopen. A JSON parser that loads the whole inventory recreates the same fault.

**Required defense:** sequential framing such as NDJSON/length-prefixed records; incremental hashing; fixed one-record parser state; no `json.load()` over an unbounded member list.

## 7. Too many shards can destroy the filesystem and publication latency

Very small shard caps can produce huge inode counts and pathological open/stat costs. Very large caps can violate the memory proof.

**Required defense:** benchmark a bounded range of shard targets and set a minimum/maximum. The chosen target is physical configuration, not semantics. If safe shard sizes still produce operationally unacceptable file counts, R04/R05 synthesis needs a different bounded container hierarchy.

## 8. Atomic rename is not universally durable or atomic

The baseline assumes same-filesystem rename plus fsync. NFS/object stores/Windows edge cases or cross-device staging can break that assumption. `os.replace` alone is not a durability proof.

**Required defense:** target-specific publication tests and an R05-approved transactional adapter. Never stage on another filesystem. If atomic visibility cannot be guaranteed, no release is declared committed.

## 9. Directory garbage and canonical-copy ambiguity

Ignoring unreferenced files is safe only if sealed inventories are the sole membership authority and R05 agrees. A second plausible manifest/copy could create ambiguity.

**Required defense:** defer canonical-copy law to R05. The R01 publisher creates one immutable content-addressed destination and never mutates it. Any stronger R05 root/member/copy rule supersedes R01 physical details.

## 10. Cache contamination can become hidden authority

A bounded LRU keyed too weakly (e.g. release_id without semantic hash) can return an object from another semantic release. A cached “not found” before full verification can manufacture negative truth.

**Required defense:** keys include immutable content identity plus exact object/query key and carrier/schema version where relevant. Negative entries only after complete verified resolution. Cache corruption/deletion must not alter results.

## 11. Concurrency can reintroduce unbounded memory

Even with bounded worker queues, a coordinator that waits for sequence gaps may accumulate an unbounded reorder dictionary if one early task stalls while later tasks complete.

**Required defense:** baseline canonical external sort eliminates the need for an unbounded completion-order reorder map. Worker queues have fixed capacity and backpressure. Merge fan-in is fixed. Any deterministic sequence coordinator must itself have a fixed window and stop producers when the window is full.

## 12. The single-row problem is real

A source can contain a giant string/blob-like value. A “1,000 row” batch can still exceed memory dramatically, and exactness forbids truncation.

**Required defense:** resource bound includes `Smax`. Future implementation should support streaming field encoding where feasible or an explicit maximum-object policy approved by source law. It may not truncate, coerce or discard the value to satisfy a metric.

## 13. The compatibility decoder currently breaks end-to-end boundedness

`pre553_physical_decoder.py` has an exact-encoding compatibility path that performs a full read and retains `_frame`. R01 cannot truthfully call the entire decoder→C11 compiler bounded while that remains.

**Required defense:** keep the limitation explicit. The carrier design is bounded from a bounded incidence stream. Before production/end-to-end acceptance, prove an equivalent chunked compatibility reader for those exact SHA/config cases or reject the end-to-end boundedness claim. Do not weaken the frozen compatibility law.

## 14. External sort disk pressure can become the new catastrophic resource failure

Run generation and multi-pass merge can require substantial temporary disk, potentially several multiples of final payload. A crash may strand run files.

**Required defense:** preflight free-space policy; bounded generation; deterministic cleanup of noncanonical staging roots; telemetry for temp bytes; fail before publication if capacity falls below safe margin. Disk exhaustion cannot expose a sealed partial release.

## 15. Validation may require more than streaming hashes

Frozen C11 validates cross-record constraints: exact universes/respondents/questions, event occurrence distinctness, authority closure, replay closure, counts. Naively replacing in-memory maps with a streaming scan could miss cross-record contradictions.

**Required defense:** externalize validation state using bounded-memory sorted joins/merge passes or a correctness-neutral disk-backed index. R01’s contract is not “one pass”; it is “bounded live memory.” Multiple external passes are acceptable. Any validator whose proof is not reproduced exactly is a rejection.

## 16. Logical digest equivalence is more important than physical byte reproducibility

Parquet library versions/compression may produce different bytes from the same logical rows. Requiring byte-identical Parquet across environments could falsely make a physical encoder the semantic authority; ignoring all physical digests would weaken integrity.

**Required defense:** distinguish semantic/logical replay root from physical member integrity. Logical equivalence is judged by R03/frozen C11. Physical bytes are authenticated within a particular sealed carrier release. R05 decides the final canonical-copy/physical replay law.

## 17. Telemetry can perturb determinism

Callbacks, logging locks, sampling, or adaptive flush decisions based on RSS can alter timing and perhaps shard boundaries or worker completion.

**Required defense:** telemetry is non-authoritative and cannot influence row content/order or semantic decisions. Prefer deterministic event-count cadence. If adaptive physical flushing is used for safety, shard boundaries remain nonsemantic and logical digests must stay invariant.

## 18. The design may be too conservative

External sort + linear exact scan is heavier than a direct database/vectorized layout. If R04 proves a simpler bounded design with equivalent closure and stronger query performance, R01 should not become institutional inertia.

**Required defense:** treat R01 as baseline and rejection oracle for memory/transaction mechanics, not as the mandated endgame format.

## Red-team verdict

`SURVIVES_DESIGN_REVIEW_ONLY_WITH_HARD_GATES`

The mechanism is plausible because it attacks the actual corpus-scale retention surfaces without semantic compression. It is not yet production-proven. The highest-risk unresolved items are backend internal-memory bounds, streaming reproduction of full C11 validation, compatibility-decoder boundedness, and composition with R05 canonical integrity/publication law.
