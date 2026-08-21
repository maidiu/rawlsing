# R04 BENCHMARK PLAN — CLASS-C COLUMNAR CHALLENGER COURT

Status: `PROPOSED__NON_DISPOSITIVE`

## 1. Court rule

Benchmark CCIV only after semantic equivalence is independently established. The mandatory comparator is the simplest R01 streaming-long representation that survives the same oracle. R4 may remain a historical/reference datapoint but is not the preferred complexity baseline.

Compression alone cannot win. Measure end-to-end resources, exact query/discovery behavior, replay/integrity, and operational complexity.

## 2. Freeze before measurement

Freeze and record:

- exact code commits for each candidate;
- exact source bytes/hashes;
- exact decoder/configuration;
- exact source/C11/I03/I05/I04 authority set;
- exact compiler settings;
- exact hardware/runtime/dependency versions;
- exact benchmark query/discovery corpus;
- cache state for each run;
- whether the workload was known before physical design.

At least one I05 workload must be frozen only **after** physical/index design is fixed so it cannot be tuned to the storage vocabulary.

## 3. Candidates

A. `STREAMING_LONG_BASELINE` — R01 lower-risk design.

B. `CCIV_NO_CACHE` — CCIV with all optional bitmaps/indexes deleted. This is the semantic/open-world baseline for CCIV.

C. `CCIV_WARM_CACHE` — same canonical release plus optional exact caches built from a declared policy.

D. Optional `R4_REFERENCE` — only if existing bounded evidence is cheap to reuse; do not rerun a dead full-source court solely for diagnosis.

CCIV must pass as B. C can demonstrate acceleration but cannot repair semantic or feasibility failure in B.

## 4. Sources / hostile physical strata

Minimum real/source-backed strata:

1. WVS7: 97,220 x 613; SPSS user-missing hostile variables; D_INTERVIEW; weight distinction; exact multi-question joints.
2. LiTS I: 29,002 x 1,198; DTA ordinary semantic-sentinel values; three weights; system missing; compatibility-reader law.
3. At least one declared-MR source from Asian Barometer Wave 5 / EVS 2008 / EVS 2017.
4. Cross-corpus fixture set from accepted SR09-PRE covering overlapping/alias MR identity, all-row typed-missing columns, ordinary blank strings, longitudinal/cardinality/type drift, and source-specific reader/text hazards.
5. Generated logical hostile fixtures from R03 that create rare event-level exceptions, repeated/ranked/componentized topology, high-cardinality strings, nonrectangular incidence, unresolved routing, and authority/dependency exceptions.

Do not infer semantics from raw probes. Use exact accepted source authority/oracle fixtures.

## 5. Compilation workloads

For each candidate/source measure:

- source cells/events processed;
- wall time;
- physical cells/sec and logical events/sec where comparable;
- peak RSS;
- peak scratch bytes;
- final authoritative bytes;
- optional cache bytes separately;
- authoritative bytes/cell and bytes/logical-event where meaningful;
- Python object-count/high-water telemetry if available;
- number/size distribution of persistent canonical members;
- number/size distribution of optional cache members;
- deterministic repeat hashes.

CCIV-specific telemetry:

- decoder batches -> Arrow batches count;
- dense versus explicit-event block counts;
- explicit-event/exception incidence rate;
- vector fast-path versus validated fallback rate;
- bitmap/index build cost;
- tiny-file/member metadata overhead.

## 6. Reopen / integrity workloads

Measure cold and warm:

- release seal verification;
- authoritative member hash verification;
- metadata open without full event materialization;
- random exact event reconstruction at N fixed sampled locators/refs;
- full streaming semantic audit;
- cache manifest verification;
- delete-all-cache reopen;
- stale-cache dependency mismatch;
- corrupted cache fallback;
- corrupted authoritative member fail-closed behavior.

Record wall time, peak RSS, bytes read, and exact semantic receipt parity.

## 7. I03 workload matrix

Every query runs on A and B; selected repeat workloads also on C.

### Q1 univariate scalar
One target, raw measure, common exact risk set.

### Q2 restrictive single predicate
One target conditioned by one low-cardinality response predicate.

### Q3 uncached high-cardinality/string predicate
Must be absent from cache policy; proves scan fallback.

### Q4 pair joint
Two target questions; exact joint distribution.

### Q5 five-way joint
Use WVS7 hostile Q177-Q181 or equivalently governed exact fixture.

### Q6 k-way conditioned joint
Multiple target questions plus 2-4 condition leaves.

### Q7 AND conjunction
Multiple response/coordinate leaves at respondent grain.

### Q8 OR conjunction
Multiple leaves.

### Q9 NOT predicate
Complement inside exact risk set; include inapplicable/nonmember respondents outside the governed denominator.

### Q10 routing hostile
NOT_ASKED, INAPPLICABLE, eligible, and unresolved cases. Negative/failure state parity is mandatory.

### Q11 typed-response-state predicate
DK/refusal/missing/source-specific state with physical-missing counterexamples.

### Q12 weighted query
Governed weight/design/estimand authority; include missing/invalid weight cases.

### Q13 coordinate predicate
Exact coordinate value/time authority.

### Q14 repeated/ranked target
Preserve semantic order/rank/multiplicity.

### Q15 componentized/multiselect target
Preserve component/set topology.

### Q16 multi-universe query
Requires exact source-relation/composition authority; prove physical co-location does not widen pooling.

### Q17 valid empty / observed zero / zero support / zero overlap / low support
Freeze separate fixtures and compare exact public result state/ref/receipt.

For each: wall time, peak RSS, bytes read, temporary selector bytes, target materialization bytes, cache hit/miss, final semantic projection/hash parity.

## 8. I05 workloads

### D1 pair response cotravel
Multiple pair candidates, no ingest-time pair tables.

### D2 bounded k-way response configuration
At least k=3 and one higher bounded arity allowed by authority.

### D3 conditional reversal / Simpson grid
Conditioning predicates not all cached.

### D4 recursive subgroup fork
At least two recursion levels within exact authority.

### D5 branch-conditioned distribution
Exact branch membership plus uncached target/condition scan.

### D6 branch-conditioned cotravel
Pair target within a branch selector.

### D7 cloud-like diagnostic workload
Diagnostics remain reporting/ranking only; candidate coverage unchanged.

### D8 storage-untuned unforeseen frontier
Freeze after CCIV block/index policy is fixed. Must include at least:

- one uncached string/high-cardinality atom;
- one 3+ way conjunction;
- one NOT/routing-sensitive atom;
- one reversal or branch-conditioned candidate;
- questions spread across multiple physical blocks.

For every discovery run record candidate_count, covered_candidate_count, receipt refs/hashes, empirical fact refs/hashes, valid-empty/coverage states, wall time, peak RSS, bytes read, cache hits, and candidate evaluation order if governed.

Any candidate count/coverage mismatch is semantic failure, not performance noise.

## 9. Cache ablation court

Run an identical I03/I05 suite in this order:

1. B: no caches;
2. C: build caches and rerun;
3. delete every cache byte and rerun B;
4. rebuild caches in a different permitted physical grouping and rerun C.

Required: identical logical outputs/refs/hashes/coverage in all four runs. Only performance may differ.

## 10. Profile-equivalence court

For generated fixtures representable by both geometry profiles, compile once as `AXIS_DENSE` and once as `EXPLICIT_EVENT`.

Required:

- identical virtual C11 semantic projections/refs/hashes;
- identical I03/I05/I04 outputs;
- identical replay semantics;
- different physical bytes/layout allowed.

This catches semantic leakage from physical specialization.

## 11. Re-layout metamorphic court

Recompile identical logical material with varied:

- question block width;
- Parquet row-group size;
- compression level/codec where permitted;
- cache policy;
- physical member grouping.

Logical semantic refs/hashes and I03/I05/I04 outputs must remain exact. Canonical physical release hashes may differ if the physical compilation descriptor changes; semantic object identity may not.

## 12. Vector-validation court

On every hostile fixture compare:

`frozen semantic constructor/integrity projection`

against

`CCIV vector compile -> virtual reconstruction projection`.

Compare exact canonical JSON/semantic hash for all public and internal C11 objects plus release/replay closure. Inject invalid fixtures for every invariant class and require both paths to reject/fail with equivalent semantic disposition. Do not require identical exception text.

## 13. Operational complexity measures

Record:

- runtime source files/modules touched by a production implementation candidate;
- number of physical schemas/profile variants;
- number of invariant implementations duplicated vectorially;
- number of cache types/invalidation keys;
- number of source-family conditionals in common consumers (required: zero for meaning);
- total hostile test count;
- total persistent authoritative member count;
- recovery procedure complexity for cache versus canonical corruption.

Complexity is part of the decision, not an afterthought.

## 14. Proposed acceptance comparison rule

This is a proposal for HQ, not frozen law.

First, both candidates must pass exact semantic/oracle gates. Then:

- If streaming-long fails a hard resource/operational gate and CCIV passes, CCIV may advance despite complexity.
- If streaming-long passes comfortably, CCIV should advance only for clearly material benefit: suggested threshold is either >=2x on a currently blocking end-to-end metric, or approximately >=35% improvement on two primary metrics with no required hostile workload regression greater than approximately 25%.
- Disk compression alone does not satisfy the rule.
- A warm-cache win does not excuse a no-cache feasibility/parity failure.
- Any semantic, replay, integrity, open-world, or fail-closed failure rejects CCIV regardless of performance.

## 15. Decision outputs

Allowed R04 court recommendations:

- `REJECT_CCIV__SIMPLER_STREAMING_LONG_SUFFICIENT`
- `ADVANCE_CCIV__SIMPLER_DESIGN_HARD_GATE_FAILURE`
- `ADVANCE_CCIV__MATERIAL_END_TO_END_BENEFIT_PROVEN`
- `REJECT_CCIV__SEMANTIC_OR_OPEN_WORLD_FAILURE`
- `REJECT_CCIV__COMPLEXITY_NOT_JUSTIFIED_BY_MEASURED_BENEFIT`

No benchmark run under this design-only return itself constitutes adoption authority.
