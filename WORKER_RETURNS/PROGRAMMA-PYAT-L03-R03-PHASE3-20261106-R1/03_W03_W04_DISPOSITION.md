# 03 — W03/W04 disposition from the phase-3 compact evidence

## Short disposition

- **Current composed exact function:** present. The source-backed compact first
  reader composes the existing physical stream, governed candidate, complete I02
  validation, sealed release, compact view, exact I03 facts/replay, and the actual
  `CarrierNeutralResearchExecutor` first consumer. On the small N=200/1,000
  synthetic fixture, V0 native and V1/V2 compact full facts, source/projection/
  release identities, fact refs, and replay refs are equal.
- **Selected economical compact capability:** **not fulfilled.** The compact path
  has higher peak RSS than native and the warm persistent cache does not
  materially reduce total wall at N=1,000. This is a proven small-fixture physical
  economy deficit, not a missing exact API and not a wrong-fact defect.
- **Default persistent acceleration:** **competent-owner/policy boundary.** The
  optional authenticated Parquet/Zstd capability is present and works with an
  explicit env root. With the env root unset, `_cache_directory()` returns `None`;
  no persistent slot is written, while the in-memory compact view still exists.
  Whether default activation is required is a policy decision under the latest
  no-blanket-cache-default constraint, not a missing codec/engine.
- **Whole L03:** **not complete.** The exact function is present; the selected
  economical cold/memory/default capability is not fully delivered.

## Function-level disposition

| Requirement | Current exact function | Evidence at phase-3 | Disposition |
|---|---|---|---|
| W03/P01 — exact source-backed sealed realization/reconstruction and first read | `build_validated_source_backed_c11_release_from_stream`, `build_source_backed_c11_repository`, compact Arrow view, `C11Repository`, `CarrierNeutralResearchExecutor.execute_i03` | V0/V1/V2 full-fact/source/ref/replay equality N=200/1,000; V1/V2 use the actual source-backed facade and first consumer | **PRESENT / PASS** for exact function; no exact function gap found |
| W03/P01 — economical cold construction / peak memory | Same path; cold candidate currently materializes full native candidate/validation objects before compaction | N=1,000 peak RSS 263.4–272.3 MB compact vs 153.8 MB native; warm cache cuts conversion but total wall not materially improved | **NOT FULFILLED**; one proven first-reader physical deficit (below) |
| W04/P02 — exact optional compact/Parquet-Zstd capability | Default in-memory `_CompactPublicObjects`; optional authenticated `_read_bodies`/`_write_bodies` cache; `ParquetC11Carrier`, R4, R5 components | V2 cold miss/write and warm HIT; same cache slot; full fact parity; cache 318,780 bytes N=200 and 1,716,950 bytes N=1,000 | **PRESENT / PASS** as optional exact capability |
| W04/P02 — default persistent acceleration | Env-gated only; no persistent slot when root unset | V1/V0 runs have no persistent cache; V2 requires explicit root | **COMPETENT-OWNER BOUNDARY**; not a missing codec/engine, not a reviewer policy grant |

## The one precise remaining first-reader physical deficit

**Compact first-reader cold construction / peak-memory economy is worse than the
native first reader, and the warm cache does not recover a material total-wall
economy at the measured scale.**

Evidence (same sealed source, projection, release, and first consumer; fresh
process per variant; N=1,000):

- V0 native: 153.8 MB peak RSS, 21.29 s parent wall.
- V1 default compact: 263.4 MB, 21.76 s.
- V2 compact + cold persistent cache: 272.3 MB, 21.55 s; 1,716,950 cache bytes.
- V2 compact + warm persistent cache: 265.7 MB, 21.03 s; conversion 2.27→0.74 s.

The compact path peaks at roughly 1.7× native. The warm cache substantially
reduces compact-conversion time but total wall remains roughly flat versus V1/V0.
The cold path still materializes the full native candidate/validation object set
before producing the compact view; the persistent body cache accelerates reading
of event bodies, not the cold peak or the full object staging.

This is a **physical economy deficit** relative to the selected economical
compact/hybrid goal. It is **not** a source, authority, canonical-identity, or
fact/replay correctness defect. It is proven on the small synthetic fixture; it is
not proven at original35/production scale.

### What would close it (engineering candidate, not science)

If the competent owner requires the economy claim, the smallest next proof is a
bounded, same-sealed-release cold/warm compact-vs-native run at a representative
authorized scale with explicit peak-memory/cold-time budgets and exact
fact/replay parity. If that run fails the budget while still requiring exact facts,
the bounded engineering candidate is a lazy/streaming I02 candidate or compact
conversion path that avoids retaining the full native event/coordinate/weight
objects before compaction. That is a candidate requirement, not a scientific rule,
and this review does not authorize a source edit or a new engine. No streaming/
journal rewrite is justified by the current small-fixture evidence alone.

## Default persistent acceleration boundary

The selected W04 wording includes default regenerable compact acceleration or a
competent-owner-accepted equivalent. The current facts are:

- Default in-memory compact Arrow exists when pyarrow is installed.
- Persistent Parquet/Zstd body acceleration is optional and env-gated.
- With `RAWLSING_C11_ACCELERATOR_DIR` unset, no persistent slot exists; this is a
  configuration/default policy gap, not a missing codec or carrier.
- Turning it on by default would be a cache-policy/default decision. The latest
  no-blanket-cache-default constraint is binding; this reviewer does not invent or
  grant that policy.

Therefore W04 is **not a first-reader exact-function deficit**; it is either an
owner-accepted optional capability or a competent-owner default-policy decision.
It must not be silently erased, and it must not be declared complete without that
decision.

## Capacity guard repair

The concurrently assigned capacity-guard repair is **not returned**. This review
does not inspect imaginary code, wait for it, or extend scope. The phase-3
`max_groups=1` capacity probe (exact but +46.8% N=200 / +60.8% N=1,000) and the
earlier P41 capacity-pressure observation (82–92 fallbacks per discovery-bearing
scope) are measurement limits only. The future frozen repair review remains
outstanding.

## Non-claims

- No full functional-equivalence declaration from small-fixture speed.
- No original35, production, cross-machine, native-source, actor/human, Sorok, or
  scientific-owner claim.
- No new architecture court, default cache policy, or persistent truth engine.
- No source/test/guide/protected branch edit or merge.
- Accepted P2 scope, per-operation facts/replay, and prior negative evidence are
  preserved, not re-litigated or erased.
