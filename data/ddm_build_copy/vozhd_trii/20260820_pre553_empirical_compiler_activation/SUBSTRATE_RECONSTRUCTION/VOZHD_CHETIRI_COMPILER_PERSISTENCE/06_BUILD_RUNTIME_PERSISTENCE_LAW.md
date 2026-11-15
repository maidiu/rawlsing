# VOZHD CHETIRI — BUILD/RUNTIME PERSISTENCE LAW

Short tag: `VC4-COMPILER/PERSISTENCE`

Status: `EXPLORATORY_BINDING_LAW_WITHIN_CHETIRI__NON_DISPOSITIVE_EXTERNALLY`

## 0. PURPOSE

This law prevents Rawlsing from confusing:

- source authority with transformed convenience;
- logical C11 semantics with a particular storage layout;
- compiler scratch with permanent product;
- build-time throughput with runtime latency;
- a regenerable cache with canonical empirical truth.

## 1. SIX PERSISTENCE CLASSES

Every object in the prospective source→compiled-substrate lifecycle SHALL receive exactly one primary class.

### P1 — `PERSIST_AUTHORITATIVE_SOURCE`

Examples may include exact `.sav` / `.dta` bytes and separately governed documentary/source authorities.

Properties:

- highest physical empirical evidence within its jurisdiction;
- immutable/content-addressed;
- deletion is information loss unless an exactly certified equivalent authority exists under separate law;
- never reconstructed from a lower-ranked derivative merely because the derivative is convenient.

### P2 — `PERSIST_AUTHORITATIVE_SEMANTIC_OR_STRUCTURAL_PRODUCT`

Examples may include accepted semantic authority packs, admitted structural products, immutable StructuralPriorRepository material and V3-facing runtime substrate.

Properties:

- contains Rawlsing-added governed information not reducible to raw source bytes alone;
- must be versioned, provenance-bound and integrity-protected;
- may be rebuildable in principle, but remains a first-class governed product rather than disposable scratch.

### P3 — `PERSIST_PROVENANCE_OR_REPLAY_RECEIPT`

Examples may include source/compiler/authority roots, admission receipts, exact operation definitions, semantic release roots and product provenance sufficient for deterministic replay/audit.

Properties:

- persists because audit/replay/provenance is a product requirement;
- must not duplicate full empirical payload without necessity proof;
- must identify exact determinants needed to reconstruct any omitted material.

### P4 — `PERSIST_REGENERABLE_CACHE_OPTIONAL`

Examples may include local optimized Parquet, indexes, predicate bitmaps or decoded column caches retained solely to accelerate repeated builds.

Properties:

- nonauthoritative;
- exact immutable cache key must bind source + decoder + authority + compiler identity as applicable;
- stale/partial/corrupt cache fails closed;
- cache absence cannot change semantic result;
- cache deletion causes zero information loss;
- system must retain a lawful no-cache regeneration path.

### P5 — `TRANSIENT_COMPILER_STATE`

Examples may include Arrow batches, DuckDB temporary relations, external-sort runs, respondent masks, transient Parquet, scratch indexes or in-memory dictionaries.

Properties:

- exists only during a build/query/discovery/audit session;
- may be large if bounded and beneficial;
- must be cleaned on success and safely recoverable after failure;
- may not be cited as empirical authority;
- no downstream product may require the exact transient physical arrangement for meaning.

### P6 — `DERIVE_ON_DEMAND`

Examples may include deterministic object IDs, content hashes, virtual event rows or semantic projections whose determinant sets are exactly proved.

Properties:

- no persistent bytes required for the derived value itself;
- derivation function/version and determinants must be governed;
- exact inverse/reconstruction/parity proof required where the derived value participates in semantic identity;
- exceptions must be exhaustively represented elsewhere.

`UNRESOLVED_BLOCKING` is permitted only as a temporary campaign state and must be owned before gate closure.

## 2. AUTHORITY NON-PROMOTION LAW

The following implication is forbidden:

`USED_FREQUENTLY -> AUTHORITATIVE`

The following implication is also forbidden:

`EXPENSIVE_TO_REBUILD -> AUTHORITATIVE`

Frequency/cost may justify P4 cache retention. They do not elevate a P4/P5 object into P1/P2/P3.

## 3. BUILD/RUNTIME BOUNDARY

The campaign must determine the exact accepted boundary, but its target abstraction is:

```text
BUILD SIDE

P1 source
 + P2 semantic authority
 + P3 required replay roots
      ↓
virtual/materialized C11 execution
      ↓
I03 / I05 / I04
      ↓
source→structural pipeline-generator
      ↓
P2/P3 compiled structural/runtime products

================ BUILD/RUNTIME BOUNDARY ================

RUNTIME SIDE

compiled structural/runtime products
      ↓
V553–V558 / ContextResolver / V3
      ↓
V2 / application
```

If C01 finds a legitimate runtime path back to empirical incidence, the boundary must be amended by exact evidence rather than assumed away.

## 4. OBJECTIVE FUNCTIONS

### Permanent runtime-facing products

Optimize lexicographically:

1. `FLAWLESS_EFFECTIVENESS`
2. `RUNTIME_SPEED`
3. `PERSISTENT_LIGHTNESS`
4. `OPERATIONAL_SIMPLICITY`

### Compiler intermediates

Optimize lexicographically:

1. `SEMANTIC_AND_REPLAY_EXACTNESS`
2. `BOUNDED_FAIL_CLOSED_EXECUTION`
3. `TOTAL_COMPILATION_THROUGHPUT`
4. `SCRATCH_EFFICIENCY`
5. `IMPLEMENTATION_SIMPLICITY`

A temporary 10 GiB compiler image may beat a permanent 2 GiB canonical empirical copy if the former is bounded/regenerable and materially improves total compilation while the permanent system remains smaller and equally exact.

This is not automatically preferred; it is merely a lawful comparison.

## 5. INFORMATION-LIFECYCLE TABLE REQUIRED OF C07

C07 SHALL produce, for every major object:

- object name;
- semantic owner;
- producer;
- consumer(s);
- grain;
- determinant set;
- persistence class;
- rebuildability;
- invalidation key;
- integrity mechanism;
- runtime latency sensitivity;
- audit/replay necessity;
- physical-size expectation if known;
- whether deletion causes information loss;
- whether deletion prevents runtime;
- whether deletion merely increases rebuild cost.

## 6. SOURCE-BACKED DELETION TEST

For B/C to remain lawful, after compiling accepted permanent products:

1. delete every P4 cache;
2. delete every P5 compiler intermediate;
3. retain P1/P2/P3 only;
4. verify ordinary runtime remains correct if runtime is contractually independent of empirical substrate;
5. verify a fresh compiler process can regenerate required C11 logical observations and rebuild the compiled product from exact authoritative determinants;
6. verify regenerated product semantic identity/replay receipts equal the governed expectation.

Any deleted object whose absence destroys information rather than performance is misclassified.

## 7. PERSISTENT EMPIRICAL COPY TEST

For candidate A, Chetiri must ask:

- What governed information exists in the persistent canonical event carrier that is not recoverable from P1 source + P2 authority + P3 receipts?
- If none, is the carrier nevertheless justified as a mandatory operational product rather than P4 cache?
- What consumer contract requires its persistence?
- Could the same requirement be met by a smaller sidecar/index/cache without making the cache authoritative?

A persistent carrier may still win. It must win by proof rather than inherited assumption.

## 8. PIPELINE-GENERATOR INTERFACE LAW

Until HQ selects otherwise, the still-unbuilt generator SHOULD depend on a logical empirical repository contract, not a storage product.

Forbidden architectural dependency pattern:

```text
I05/PIPELINE_GENERATOR -> PARQUET_FILE_LAYOUT
```

Preferred dependency pattern:

```text
I05/PIPELINE_GENERATOR -> C11_LOGICAL_REPOSITORY
C11_LOGICAL_REPOSITORY <- R5_PERSISTENT_BACKEND | SOURCE_BACKED_BACKEND | HYBRID_BACKEND
```

This does not require implementation of multiple production backends. It requires avoiding an unnecessary semantic dependency on one physical layout.