# D15 — BLOCKED RUNTIME AND EMPIRICAL UNKNOWNS

## 1. Status

D15 architecture is **not blocked** by the items in this document.

Binding inherited state:

`POPULATED_SUBSTRATE_EMPIRICAL_FACTS_UNKNOWN__NO_DB_ACCESS_EXPECTED`

D13 closes information sufficiency at specification level. D14 closes symbolic cost geometry. The following are implementation/runtime/populated-evidence unknowns and must not be converted into architectural facts.

## 2. Source→C11 populated equivalence

**State:** `BLOCKED_SOURCE_EQUIVALENCE` / no current populated C11 implementation certified.

Unknown:

- exact current source-native snapshot set/identity for every production source;
- actual source→current-ingest row/event loss or multiplication;
- multiselect/repeated/ranked preservation rates;
- routing/applicability preservation;
- native special-state preservation;
- weight completeness/design basis;
- future-coordinate completeness;
- current shared-substrate populated parity/JOINT_ONLY parity.

**Architecture consequence:** retain source snapshots and current migration surfaces until per-source positive equivalence. No architecture reopening required.

## 3. Actual empirical content

Unknown and not claimed:

- population prevalence;
- conditional support rates;
- minority configuration frequency;
- respondent overlap among questions;
- branch sizes;
- k-way sparsity/occupied-cell distributions;
- source disagreement prevalence;
- source overlap/double-counting incidence;
- actual comparator match/no-match/ambiguity rates.

**Architecture consequence:** exact sparse/support-bearing representation is required, but no tuned thresholds/cardinalities are selected from nonexistent measurements.

## 4. Current production performance

`BLOCKED_LIVE_PRODUCTION_MEASUREMENT`:

- wall-clock by current V550/V550J family;
- CPU;
- peak RSS;
- database I/O/network;
- rows/intermediate expansion;
- checkpoint/artifact bytes;
- live recursive branch count/support;
- cloud pair overlap/join expansion;
- V550J pattern/membership/association/publication cardinalities.

Static loop/write geometry remains useful implementation evidence but is not a measured production budget.

## 5. Target C11 physical sizing

Unknown until I02 produces a concrete implementation:

- bytes per response event;
- bytes per coordinate fact;
- routing/eligibility bytes;
- authority-manifest overhead;
- indexes/partition metadata;
- compression ratio;
- read/write amplification;
- peak ingest/query memory;
- source/C11 duplication ratio.

**Architecture parameter left open:** storage engine, codec, compression and physical index family. D15 selects semantic physical strategy (append-only universe-scoped normalized incidence + immutable manifests), not a database vendor/format.

## 6. Target query cost

Unknown until concrete implementation + source-equivalent populated corpus:

- W01–W17 wall/CPU/RSS/I/O;
- real predicate selectivity;
- topology multiplicity distribution;
- condition arity frequency;
- joint arity frequency;
- exact query latency/SLA under concurrency.

**Architecture consequence:** exact query semantics are fixed; access plan/indexing remain implementation-time optimizations.

## 7. Autonomous discovery runtime frontier

Unknown:

- real authority-declared frontier sizes `F/P/H`;
- actual feasible support pruning under future authorities;
- cost of EXACT_BOUNDED for representative source scopes;
- useful beam/screen parameters for ADAPTIVE_EXPLORATORY;
- safe-pruning theorems, if any, beyond deliberately proven cases;
- production cadence/concurrency for discovery.

**Architecture consequence:** two truthful coverage modes are selected; operational default between them for a given discovery authority remains workload/sizing policy.

No cost fact may weaken a declared completeness claim after the fact.

## 8. Reverse positioned-subject workload

Unknown:

- actor objective fact count available at query time;
- typical comparator rule/crosswalk size;
- `K` conditioner arity distribution;
- `J` target arity distribution;
- number of source universes admitted per query;
- comparator no-match/ambiguity rates;
- zero/low-support rates;
- field reuse/cacheability.

**Architecture consequence:** exact field production and typed fail-closed paths are fixed; cache thresholds and performance policy remain tunable.

## 9. Cache/materialization economics

Unknown:

- query reuse distributions;
- cache hit rates;
- invalidation frequency;
- authority/source update cadence;
- E1/E2/branch/field cache byte cost;
- cold vs warm latency delta.

**Architecture consequence:** caches are optional and nonauthoritative. I11 measures them before tuning.

## 10. Production savings

Still unknown and prohibited as a D15 claim:

- percentage compute savings;
- percentage storage savings;
- required production hardware;
- production concurrency budget;
- operational cost savings.

A lawful comparison requires both current and target systems measured on semantically equivalent W01–W17 workloads after C11 equivalence.

## 11. Cross-universe composition models

D12 left a generic pooling/backfill statistical model `UNPROVEN`.

D15 does not create one. Source-indexed plurality is sufficient. A future specific pooling/composition authority may be created only for a named estimand/source relation with design/nonduplication evidence.

## 12. Universal uncertainty estimator

D12 left one universal numeric estimator `UNPROVEN`.

D15 creates an uncertainty **authority registry**, not a universal formula. Where no governed estimator applies, `UNCERTAINTY_UNQUANTIFIED` is the lawful state.

## 13. Downstream V553+ implementation details

Semantic revalidation is closed, but concrete changes remain implementation questions:

- exact new V553 intake schema/adapter shape;
- whether V554/V555/V556 require only provenance field pass-through or no code change;
- exact V557 adapter version changes;
- exact V3 module/interface location for V3EmpiricalPossibilityInput;
- exact V3 metabolism rule family behavior after authority design.

These do not reopen jurisdiction. `V553_PLUS_REVALIDATION_MATRIX.csv` fixes the semantic requirements.

## 14. Source retirement

Even after technical C11 equivalence, legal, audit, reproducibility or operational source-retention obligations may remain unknown.

D15 therefore does not authorize source deletion and I13 is audit-only.

## 15. Unknowns that WOULD require architecture review if discovered

A later implementation must return to architecture governance, rather than silently patch, if evidence shows:

- a source semantic distinction cannot be injectively represented by the selected C11 object families;
- a terminal D12 query requires information outside M01–M18;
- the selected V3 possibility-field boundary necessarily forces direct actor-state assignment to function;
- a required structural use cannot be represented as an explicit StructuralEmpiricalAdmission without changing downstream structural jurisdiction;
- an accepted V554–V558 contract actually depends on a superseded survey/persona semantic not captured in current revalidation.

No such blocker is presently established.

## 16. Closure

All known remaining blockers are empirical/runtime/implementation measurements or concrete authority content to be authored under the selected architecture.

They do not satisfy the D15 failure condition `ARCHITECTURE_SYNTHESIS_BLOCKED__DISCOVERY_REOPEN_REQUIRED`.
