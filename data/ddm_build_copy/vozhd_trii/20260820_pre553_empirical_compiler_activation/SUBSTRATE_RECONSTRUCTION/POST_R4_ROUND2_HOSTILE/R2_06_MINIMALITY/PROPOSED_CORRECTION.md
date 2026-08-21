# R2-06 PROPOSED CORRECTION TO P0

Status: `ROUND2_REQUIRED_SYNTHESIS_CORRECTION__NO_IMPLEMENTATION_AUTHORITY`

This document does not replace Authority 54. It states the exact corrections R2-06 requires HQ to apply when synthesizing P0 after the Round-2 hostile court.

## C1 — Change “canonical member classes” into an information-ownership contract

P0 §5.3 currently lists twelve kinds of canonical material. Preserve every information obligation but remove any implication that each category is a distinct table/file/relation.

Corrected law:

> Every frozen source/C11 obligation must have exactly one canonical physical owner, exact derivation, or exact exception path. Physical co-location is preferred when it preserves grain/key/type distinctions and reduces joins/failure surfaces. Separate members are introduced only for exact grain, boundedness, access, or integrity reasons that survive the final deletion court.

This preserves R02's grain law without converting normalization into architecture.

## C2 — Freeze the baseline as cacheless serial bounded LONG_SHARDED

The first shadow implementation candidate is:

```text
LONG_SHARDED
persistent caches = 0
worker_count = 1
flat root/member integrity
standard exact typed lanes
standard physical encoding/compression tuning only
one C11 materializer
```

Simple exact question/release metadata ownership is allowed where R02 certificates are already clear; direct event storage remains fallback.

No QBL/HYBRID/vector/Merkle/adaptive/parallel mechanism is required merely to begin the court.

## C3 — Remove C04 cache from the provisional core

C04 is not a correctness mechanism. Baseline cache count is zero.

C04 may return only if repeated exact identity/derivation computation misses a pre-frozen runtime boundary and the cache key binds every source/release/schema/compiler/config/authority determinant. Total deletion must preserve correctness and reachability.

## C4 — Reframe C03 and C07

C03 is primarily a **proof law**:

```text
field omission requires determinant + scope + grain + authority + exception/fallback + reconstruction + fail-closed behavior
```

It does not require normalization of every provably repeated field.

C07 is an **encoding option** against an accepted C03/R02 certificate. If direct storage is simpler or the exception path approaches direct cost, delete C07 for that field.

## C5 — Preserve state separations without mandatory state sidecars

Physical missing state, semantic response state, and routing/applicability stay logically and typologically distinct.

For LONG baseline they may occupy distinct typed lanes/fields in the same bounded event shard. No inference is allowed between lanes without exact authority.

Separate physical relations are admitted only if their true grain/resource behavior earns separation.

## C6 — Keep a small question metadata owner; do not over-normalize respondent/event fields

Native variable/question declarations, labels, type/storage/display metadata, and zero-incidence missing declarations naturally live at question/release grain and should have one exact owner.

A respondent dimension is optional unless respondent-grain material or repeated event-row references justify it.

Unproved event-specific authority/topology/order/state stays direct.

## C7 — Make vectorization orthogonal to organization

C08 means:

`bounded decoder batches -> exact typed vectors -> complete invariant validation -> canonical writer`

It does **not** mean:

`vector compiler -> question matrix canonical storage`.

A validated vector compiler may write LONG_SHARDED. It enters only if the object-heavy compiler path misses a frozen RSS/CPU boundary. The slow validated/reference lane remains court tooling, not a second production truth path.

## C8 — Use flat integrity as the minimum baseline

Baseline integrity/publication:

1. deterministic semantic release identity;
2. immutable physical root manifest;
3. exact authoritative member inventory;
4. whole-member byte length/hash;
5. full bounded audit;
6. fail-closed missing/mismatch behavior;
7. unique non-serving staging;
8. content-addressed promote;
9. sealed reopen verification;
10. explicit trusted active-root CAS.

Do not include Merkle/chunk trees or query-scoped lazy verification in baseline P0.

Add them only when a named pre-frozen partial verification/fetch/repair/reopen boundary fails and the query-closure sufficiency proof is independently closed.

## C9 — Baseline completeness is root inventory + exhaustive canonical scan

Do not add a separate canonical completeness index merely because negative queries exist.

If the authoritative member/shard inventory plus exact source-to-shard traversal proves exhaustive coverage, scan it.

A separate completeness structure is admitted only when that proof is impossible or a pre-frozen practical boundary requires smaller closed regions. Once required for correctness, it is canonical root-bound—not cache.

## C10 — Delete source-family physical architecture

Frozen decoder paths already handle governed source-format/reader differences.

The replacement compiler may inspect exact physical capability/type/grain certificates, but it must not select semantic behavior from family names. Prefer one organization across the accepted scope.

If later source-local specialization is unavoidable, it is a compiler implementation detail that terminates at the identical C11 boundary and must pass the same oracle. No downstream repair branch.

## C11 — Replace relative benchmark thresholds

Delete the R04 suggested relative rule from synthesis.

Corrected selection law:

1. freeze absolute hard/preferred resource and practical-runtime boundaries before candidate results;
2. court candidates in escalation order;
3. semantic/integrity/open-world failure rejects;
4. boundary failure marks candidate insufficient;
5. first candidate passing every boundary is sufficient;
6. apply final deletion pass;
7. select and stop.

A 2x or 35% improvement can diagnose value only after a candidate is otherwise required; it does not authorize architecture by itself.

## C12 — Exact organization escalation

### LONG_SHARDED

First candidate. Select and stop if all boundaries pass.

### QUESTION_BLOCKED_LONG

Only after LONG fails a frozen projection/read-amplification/reopen-locality boundary and the failure is mechanically attributable to irrelevant question bytes/fanout. QBL retains the same logical event schema, no persistent bitmap truth, no source-family semantics, and no materialized LONG duplicate.

### HYBRID_DENSE_PLUS_EXPLICIT

Only after lower-risk organizations/remedies fail a remaining boundary attributable to event-row/coordinate/storage/materialization overhead and exact R02 geometry/grain certificates are already available. Explicit escape is total and canonical. Dense selection never uses family identity or observed regularity alone.

## C13 — Make no-cache blind I05 dispositive

Organization selection runs after deleting every optional accelerator.

The blind frontier is compiled after candidate/tuning disclosure freeze and must include high-cardinality/string, k-way, NOT/routing, reversal, recursive/branch-conditioned, co-signature/cloud-like, and multi-block/mixed-profile cases.

Every candidate is evaluated. `candidate_count == covered_candidate_count` is mandatory for a complete claim.

## C14 — Split canonical feasibility from optional serving acceleration

A canonical organization must be correct, bounded, open-world and complete without caches within the frozen fallback/acceptance envelope.

After organization selection, at most one disposable cache type may be added for a separately frozen serving-latency objective. It does not change canonical identity or reachability and may be deleted/corrupted/rebuilt without semantic effect.

This prevents “optional” cache from secretly choosing the architecture.

## C15 — Resolve one-copy migration minimally

Permit:

- one active serving root;
- one non-serving shadow during a bounded implementation/equivalence court;
- staging/scratch counted separately.

Promotion atomically moves serving authority to the admitted candidate. The old root immediately becomes non-serving. No automatic fallback.

After promotion/cleanup, retain no full steady-state rollback duplicate absent higher authority. Explicit rollback otherwise rebuilds/restores from governed inputs and freshly verifies before CAS.

## C16 — Freeze one common runner

Every organization uses the contract in `MINIMUM_ONE_RUNNER_CONTRACT.md`.

Candidate-specific accepted tests, semantic adapters, cache-warmed courts, or downgraded hostile suites are forbidden.

The independent evaluator remains deliberately small to avoid becoming a second production engine.

## C17 — Count total burden

Every candidate reports:

- canonical steady-state bytes;
- staging peak;
- scratch peak;
- cache bytes;
- post-success retained bytes;
- phase-specific peak RSS/runtime;
- member count;
- profile count;
- cache/invalidation types;
- reconstruction dependency count;
- vector invariant implementations;
- source-family semantic branches;
- recovery/publication states.

Do not compare matrix payload bytes to long total bytes or warm-cache query time to cacheless correctness time.

## C18 — Final deletion court

Before implementation authority, for every retained mechanism ask:

> Which exact pre-frozen boundary fails when this mechanism is removed?

If the answer is none, delete it and rerun only the bounded court needed to verify the deletion.

This applies even to mechanisms that are correct, elegant, or individually beneficial.

## Corrected P0 minimum skeleton

```text
exact source + frozen decoder batches
-> bounded serial canonical builder
-> cacheless LONG_SHARDED first
   + exact question/release metadata owner where proven
   + direct event-varying typed incidence
   + no mandatory sidecar for each logical dimension
-> immutable semantic/physical root + member hashes
-> full bounded audit
-> one C11 materialization boundary
-> cacheless I03/I05/I04
-> independent R03 oracle + blind I05
-> replay/integrity/determinism/resource receipts
-> first-sufficient organization decision
-> final mechanism deletion pass
-> HQ only may authorize runtime implementation/adoption
```

Escalation adds exactly one mechanism for exactly one failed boundary.

## Required disposition after correction

`ROUND2_PASS_WITH_REQUIRED_CORRECTIONS__P0_REPAIRABLE`

P0's core is preserved. Its architectural default is made subtractive rather than additive.
