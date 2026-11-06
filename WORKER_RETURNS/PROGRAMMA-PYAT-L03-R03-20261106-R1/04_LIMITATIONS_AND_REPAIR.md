# 04 — Limits, W03/W04 status, and narrow follow-up guidance

## No blocking correctness defect found

The bounded P2 diff is numerically exact in the reviewed synthetic scope and
reachable first-consumer paths. The items below are honest limits and one
non-blocking performance/robustness follow-up. They do not justify a source
repair before scoped receiving, but they must remain visible to HQ.

## W03 / W04: capability present, whole L03 not complete

The current code supplies the selected physical capability in two parts:

1. **Default compact realization.** When pyarrow is installed,
   `_compact_public_objects` derives `_CompactPublicObjects` for the sealed
   release; the source-backed builder uses it without an environment switch.
   This is the existing default in-memory Arrow compact view, not new in this
   diff. My probe confirmed `_CompactPublicObjects` with 160 exact selectors for
   the small fixture.
2. **Optional persistent acceleration.** `RAWLSING_C11_ACCELERATOR_DIR` is a
   caller-configured, absolute-path, owner-only cache root. The event-body
   Parquet/Zstd slot is keyed by source/decoder/projection/release/replay/member
   root, authenticated against exact event content hashes, and regenerable. My
   probe wrote one 19,333-byte slot and reused it; the existing 8-test compact
   view suite (HIT/DELETE/CORRUPT/STALE/REVOKED) passed in the focused run.

What remains unresolved is **economical cold construction and peak memory**, not
a missing semantic API. The author’s Phase-1 evidence reports N=1,000 compact
peak RSS of 352–384 MB versus native 287.7 MB, with source reacquisition/fixture
construction dominating cold runs. This review did not rerun compact N=1,000
memory, and the grouped N=200 benchmark used a native tuple release
(`release_public_objects_class: "tuple"`), not the compact source-backed release.
Therefore:

- the selected W03/P01 sealed execution and default compact realization are
  **retained**;
- the selected W04/P02 caller-configured persistent capability is **retained**;
- `WHOLE_L03_NOT_COMPLETE` because economical cold construction/lower memory and
  compact grouped timing are not established;
- no new persistent engine, cache-policy grant, or scientific owner is created
  or implied.

### Smallest needed engineering/functional-equivalence proof

If HQ requires the remaining W03/W04 physical claim, the smallest proof is one
paired cold/warm, compact-vs-native run of the actual first consumer:

- build from the same sealed source through
  `build_source_backed_c11_repository` and execute the same operation mix through
  `CarrierNeutralResearchExecutor.execute_i03`, with
  `RAWLSING_C11_ACCELERATOR_DIR` cold and then warm;
- report CPU/wall, Darwin peak RSS bytes, cache bytes, number of index builds,
  core builds/hits, and exact fact/replay parity against the native run;
- state the cold-build and peak-memory budget being met. If the requirement is
  only functional equivalence, the existing compact + optional Parquet path
  already supplies it and the budget question remains a W04 follow-up.

No new architecture bakeoff is needed.

## Capacity fallback: measured performance limitation (not a wrong-fact defect)

The P41/issued path uses one owned scope per workload. Discovery-heavy scopes
reached the default `max_groups=64`. `p41_scope_probe.py` recorded, across two
probe runs, three owned scopes with 129 total builds, about 350–368 hits, and
about 82–92 `capacity_fallbacks` per discovery-bearing scope. All outputs remained
exact and the P41 grouped-vs-unshared hashes matched.

The issue is placement: `I03GroupedExecutionScope.evaluate` computes the full core
first, then checks `len(self._cache) >= max_groups` (or the denominator-member
budget). On a capacity miss it discards that computation and `_evaluate_index_group`
falls through to the full unshared evaluation. Under capacity pressure this is
double work, and the warm-compatible 13-op speedup does not establish an economy
for discovery-heavy workloads. The member budget also counts only denominator
members, not risk members or retained used objects, so a zero-condition group can
retain more than the nominal member cap.

**Narrow, nonblocking follow-up (if HQ wants it):**

- check capacity before the expensive core build, or evict the least-recently
  used group, instead of building-then-discarding;
- include risk-member/used-object retention in the bound or document it;
- pair-measure a discovery-heavy issued workload (the existing P41 fixture is a
  suitable sourcefree reproducer) before claiming a broader economy.

This is a performance/robustness improvement, not a correctness repair. The
reviewer made no source change.

## Identity-memo review

The reviewer specifically checked the `id()`-keyed `_index_identity` /
`_registry_identity` memos:

- the memo stores a strong reference to the object and requires `entry[0] is
  object`, so Python id reuse cannot silently map a new object to an old entry;
- `_ReleaseIndex` is frozen and its payload maps are `MappingProxyType`;
  `AuthorityRegistry` is immutable (`MappingProxyType`), so no reachable accepted
  API mutates a cached index/registry in place;
- repository index cut/rebuild creates a new index object and was verified to
  build new cores; exact restore reused only the restored object’s cores;
- no reachable changed map/authority/revocation masked the memo in the review
  checks.

If a future API ever permits in-place mutation of an index payload or authority
registry, these memos would need explicit invalidation. That is a future-contract
note, not a current defect.

## Measurement and evidence gaps

- N=1,000 and N=3,000 were audited in retained artifacts but not independently
  rerun. Their 3.07–3.25× warm speedups remain author claims; the N=200 direction
  and magnitude reproduced. The retained phase-2 commands show 3 warm rounds at
  N=1,000 and 2 warm rounds at N=3,000; the repeat summary also contains
  per-operation warm min/median/max with visible spread (for example
  `all_ABCK_raw` at N=1,000 ranged about 1.43–1.89 s across retained passes), so
  the small single-op/incompatible percentages should be read as noise-sensitive.
- The grouped benchmark used a native tuple release
  (`release_public_objects_class: "tuple"`), not the compact source-backed
  release. Compact grouping timing/peak memory is not established.
- The author’s raw untracked `.local-logs/pyat-l03-c4` JSON was absent from the
  assigned checkout. The tracked JSONL/summary artifacts and independent reruns
  were used; the full N=200 raw JSON remains local at
  `.local-logs/pyat-l03-r03/evidence/review-grouped-n200.json` and is not
  committed (disk cap). No author measurement process was run or observed during
  this review; all timed runs were the reviewer’s single runner.
- Small single-op/incompatible deltas are noise-sensitive; my N=200 signs differed
  from the author’s final rerun for those two micro-cases, while the warm economy
  and exactness were stable.
- The poison result is an accidental/stale-corruption check, not an adversarial
  recomputed-fingerprint defense.

## Preserved positives

Nothing above erases the earlier verified positives: the six-file scope is
bounded; the core is measure-independent; every operation builds its own fact,
provenance, dependency refs, and replay; incompatible scopes do not cross-share;
authority/index/rebuild paths fail closed; issued Batch/I05/P41 parity holds; and
the existing compact/Parquet physical capability is retained and regenerable.
