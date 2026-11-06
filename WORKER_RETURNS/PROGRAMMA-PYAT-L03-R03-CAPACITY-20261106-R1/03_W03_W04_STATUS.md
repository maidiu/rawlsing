# 03 — W03/W04 and full-L03 status after the capacity guard

The capacity-miss guard is a bounded capacity-cost fix. It does not change the
W03/W04 or whole-L03 status established in the phase-3 compact assessment.

## Status

| Field | Status | Note |
|---|---|---|
| W03/P01 exact composed function | **PRESENT** | Source-backed compact first reader and exact I03 facts/replay unchanged; earlier small-fixture full-fact/source/ref/replay equality stands |
| W03/W04 economical compact / cold construction / peak memory | **NOT FULFILLED** | Compact peak RSS remained higher than native at N=1,000 and warm cache did not materially improve total wall in the phase-3 evidence; the capacity guard does not address cold construction or memory |
| W04 default persistent acceleration | **COMPETENT-OWNER / DEFAULT-POLICY BOUNDARY** | Optional env-gated authenticated Parquet/Zstd capability exists; default activation is a policy decision, not a missing codec/engine; no blanket cache default |
| Whole L03 | **NOT_COMPLETE** | Exact function and bounded capacity behavior exist, but the selected economical/default capabilities remain unresolved |
| Capacity guard | **FOCUSED ACCEPT** | Early MISS guard verified; HIT reuse, normal refusals, member-bound behavior, counters, cleanup unchanged |

## What the guard does and does not change

- It avoids a duplicate full core build when a MISS occurs after the cache is
  already at the group cap or cached denominator members are at the member cap.
- It preserves the HIT path at full capacity.
- It preserves the post-build prospective-member fallback for an unknown new
  denominator.
- It does not change `max_groups`, `max_cached_members`, eviction, persistence,
  cache defaults, source/authority/identity semantics, index attestation, or
  fact/replay construction.
- It does not fix compact cold construction, peak RSS, or default persistent
  activation. Those remain the phase-3 deficits.

## One precise remaining first-reader physical deficit (unchanged)

The compact source-backed first reader remains uneconomical in cold construction /
peak memory: N=1,000 compact variants peaked at approximately 263.4–272.3 MB vs
153.8 MB native, and the warm cache reduced compact conversion without materially
reducing total wall. The cold path still materializes full native
candidate/validation objects before compaction. This is proven on the small
synthetic fixture, not at original35/production scale.

If the selected requirement is only exact function plus optional caller-configured
cache, the exact function is present and the remaining item is the competent-owner
default-persistence policy decision. Neither outcome is a whole-L03 completion.

## Non-claims and boundaries

- No full functional-equivalence declaration from small-fixture speed.
- No original35, production, native-source, actor/human, Sorok, or scientific
  claim.
- No new architecture court, default policy, cache-policy grant, or new engine.
- No production/source/test/guide/protected merge.
- Earlier accepted `409be32` P2 scope, `e2f6c164` review, and `5dfef26d` phase-3
  assessment are preserved.
