# VOZHD CHETIRI — COMPILER & PERSISTENCE ARCHITECTURE — MASTER CAMPAIGN CHARTER

Short tag: `VC4-COMPILER/PERSISTENCE`

Status: `EXPLORATORY__NON_DISPOSITIVE__NO_RUNTIME_WRITE_AUTHORITY`

## 0. PURPOSE

This campaign exists because the full source→compiled-structural-substrate pipeline-generator has not yet been built, while current PRE553 work is actively selecting/repairing a physical empirical carrier.

The timing creates one narrow architectural question that must be answered before the missing compiler-generator accidentally hard-codes a physical intermediate as an architectural requirement:

> What information must exist permanently, and what information only needs to be reproducibly computable during build time?

Chetiri does not reopen the closed semantic machine. It determines the correct **persistence and compiler lifecycle** under that machine.

## 1. FROZEN SEMANTIC/WHOLE-MACHINE BOUNDARIES

Chetiri SHALL preserve exactly:

- source truth and exact source bytes;
- decoder semantics and frozen compatibility execution distinctions;
- C11 M01–M18;
- respondent-grain lawful queryability;
- raw/canonical value separation;
- physical missingness/semantic response-state separation;
- topology/multiplicity/order/rank/component identity;
- routing/applicability/risk-set truth;
- weight/design/estimand authority;
- source relation/nonduplication provenance;
- ExactRef/content-hash semantics;
- I03 exact empirical truth;
- I05 exact-bounded/open-world discovery frontier;
- I04 structural-admission semantics and provenance;
- source evidence ≠ structural prior ≠ generated actor fact ≠ actor knowledge ≠ memory/presentation ≠ V2 expression;
- V553–V558, V3 and V2 jurisdiction;
- whole-machine closure.

No candidate earns performance by weakening any item above.

## 2. EXPLORATORY CANDIDATE FAMILIES

### A. Persistent canonical event carrier

```text
SOURCE
→ frozen decoder
→ persistent canonical event-grain carrier
→ carrier-neutral C11
→ I03/I05/I04
→ structural compiler-generator
→ compiled structural substrate
```

Current R5 LONG_SHARDED is the active implementation family under separate Trii authority.

### B. Source-backed virtual C11

```text
SOURCE
→ frozen decoder / source accessor
→ authority/semantic sidecars
→ virtual carrier-neutral C11
→ I03/I05/I04
→ structural compiler-generator
→ compiled structural substrate
```

No complete second empirical payload persists by default.

### C. Source-backed hybrid

```text
SOURCE
→ frozen decoder / source accessor
→ authority/semantic sidecars
→ virtual C11
→ transient or regenerable execution accelerators
   (Arrow / DuckDB / Parquet / bitmaps / indexes / vectors)
→ I03/I05/I04
→ structural compiler-generator
→ compiled structural substrate
```

Accelerators are nonauthoritative unless a separate proof establishes that some structure is logically required to prove completeness/absence and therefore belongs to canonical information.

## 3. CAMPAIGN PHASES

### PHASE P0 — ARCHITECTURAL NECESSITY

Cells: `C01`, `C02`, `C06`, `C07`.

Goal: determine whether source-backed compilation is semantically/replay-wise possible and identify the true permanent runtime product boundary.

No performance conclusion is allowed in P0.

P0 outputs must answer:

- what V3/runtime actually consumes;
- what C11 facts are derivable and from what determinants;
- what must persist for ExactRef/replay/integrity;
- what the compiled structural substrate must contain.

Gate: `G0_ARCHITECTURAL_FEASIBILITY`.

Possible dispositions:

- `G0_PASS__SOURCE_BACKED_REMAINS_LAWFUL_CANDIDATE`
- `G0_BLOCK__IRREDUCIBLE_EVENT_PERSISTENCE_REQUIRED`
- `G0_BLOCK__REPLAY_OR_INTEGRITY_CONTRADICTION`
- `G0_BLOCK__FROZEN_SEMANTIC_CONTRADICTION`
- `G0_RETURN__NAMED_EVIDENCE_REQUIRED`

### PHASE P1 — EXECUTION FEASIBILITY

Cells: `C03`, `C04`, `C05`, `C08`.

Launch only if `G0_PASS` or HQ explicitly authorizes a narrower probe.

Goal: determine how the compiler can actually execute against hostile SAV/DTA sources without turning source-backed authority into parser thrash or losing open-world capability.

Gate: `G1_EXECUTION_FEASIBILITY`.

Possible dispositions:

- `G1_PASS__SOURCE_BACKED_EXECUTION_FEASIBLE`
- `G1_PASS__HYBRID_ACCELERATION_REQUIRED`
- `G1_BLOCK__MANDATORY_FULL_MATERIALIZATION_REQUIRED`
- `G1_BLOCK__I03_CAPABILITY_STARVATION`
- `G1_BLOCK__I05_CAPABILITY_STARVATION`
- `G1_BLOCK__INCREMENTAL_BUILD_UNACCEPTABLE`
- `G1_RETURN__NAMED_EVIDENCE_REQUIRED`

### PHASE P2 — MEASURED CANDIDATE COURT

Cell: `C09`.

Launch only after P0/P1 define identical proof surfaces.

Goal: compare A/B/C on exact representative compiler primitives and resource costs.

Gate: `G2_MEASURED_BAKEOFF`.

No candidate may win on performance unless semantic/replay/integrity parity passes first.

### PHASE P3 — HOSTILE RED TEAM

Cell: `C10`.

Goal: attack the provisional synthesis and identify hidden assumptions, especially those induced by WVS/LiTS proving sources.

Gate: `G3_HOSTILE_SURVIVAL`.

### PHASE P4 — HQ SYNTHESIS

No worker owns P4. HQ only.

HQ may return exactly one of:

- `VC4_CLOSE__CURRENT_R5_PERSISTENT_CARRIER_REMAINS_ARCHITECTURALLY_JUSTIFIED`
- `VC4_CLOSE__SOURCE_BACKED_VIRTUAL_C11_PREFERRED__REOPENING_PETITION_REQUIRED`
- `VC4_CLOSE__HYBRID_SOURCE_AUTHORITY_PREFERRED__REOPENING_PETITION_REQUIRED`
- `VC4_CLOSE__INSUFFICIENT_EVIDENCE__NO_REOPENING`
- `VC4_CLOSE__FROZEN_CONTRACT_CONTRADICTION_ESCALATION_REQUIRED`

A preferred Chetiri architecture does not become implementation authority until an explicit later HQ reopening/adoption authority is checked in.

## 4. CORE EVIDENCE LAW

Evidence rank:

1. exact raw source bytes + source-native metadata;
2. frozen source/decoder authority;
3. accepted C11/I03/I05/I04 contracts and exact current implementation where it embodies them;
4. accepted whole-machine/V553–V558/V3/V2 authorities;
5. exact benchmark/court receipts generated under frozen workloads;
6. implementation convenience or intuition.

No prose preference may outrank measured or contractual evidence.

## 5. DERIVABILITY LAW

No field may be omitted from persistent state merely because it appears redundant.

Every proposed non-persistence claim must identify:

- logical fact/field;
- exact determinant set;
- authority establishing the functional dependency;
- scope of the dependency;
- deterministic reconstruction function;
- exhaustive exception domain;
- integrity binding of determinants and exceptions;
- hostile proof that reconstruction is exact.

Allowed classification vocabulary:

- `SOURCE_DERIVABLE`
- `SOURCE_PLUS_RELEASE_METADATA_DERIVABLE`
- `SOURCE_PLUS_VARIABLE_AUTHORITY_DERIVABLE`
- `SOURCE_PLUS_RESPONDENT_AUTHORITY_DERIVABLE`
- `SOURCE_PLUS_TOPOLOGY_AUTHORITY_DERIVABLE`
- `SOURCE_PLUS_MULTI_AUTHORITY_DERIVABLE`
- `SPARSE_EXCEPTION_MATERIAL_REQUIRED`
- `IRREDUCIBLE_EVENT_GRAIN_PERSISTENCE_REQUIRED`
- `UNRESOLVED`

## 6. PERSISTENCE CLASSIFICATION LAW

Every object in the prospective compiler lifecycle must receive exactly one primary disposition:

- `PERSIST_AUTHORITATIVE_SOURCE`
- `PERSIST_AUTHORITATIVE_SEMANTIC_OR_STRUCTURAL_PRODUCT`
- `PERSIST_PROVENANCE_OR_REPLAY_RECEIPT`
- `PERSIST_REGENERABLE_CACHE_OPTIONAL`
- `TRANSIENT_COMPILER_STATE`
- `DERIVE_ON_DEMAND`
- `UNRESOLVED_BLOCKING`

A cache may not become authoritative because downstream code happens to depend on it.

A transient representation may be large if bounded, safe and materially advantageous. Persistent system lightness and runtime effectiveness are judged separately from compiler scratch peak.

## 7. BUILD/RUNTIME NONCOLLAPSE

The campaign must distinguish:

`BUILD_TIME_CORRECTNESS`

from

`RUNTIME_LATENCY`

and

`PERSISTENT_SYSTEM_SIZE`

from

`TEMPORARY_COMPILER_SCRATCH_SIZE`.

A design may legitimately use a large temporary analytical image if:

- it is deterministically rebuildable from authoritative inputs;
- deletion causes zero information loss;
- it cannot silently acquire authority;
- scratch use is bounded and cleaned;
- the resulting permanent system is superior under the final objective.

## 8. FINAL OBJECTIVE ORDER

For the **compiled V3-facing structural substrate**:

1. flawless effectiveness / semantic completeness;
2. runtime speed;
3. persistent lightness;
4. operational simplicity and maintainability.

For **compiler intermediates**:

1. semantic/replay exactness;
2. boundedness and fail-closed behavior;
3. total build throughput;
4. scratch efficiency;
5. convenience.

The two objective functions must not be silently conflated.

## 9. DELETE-ALL-CACHES TERMINAL TEST

A source-backed/hybrid candidate is not architecturally valid unless the following experiment is conceptually and operationally sound:

> Delete every transformed empirical copy, query cache, bitmap, temporary Parquet/DuckDB/Arrow image and other compiler accelerator. Retain only immutable source artifacts, governed authority/semantic material, required provenance/replay receipts, and the compiled structural/runtime products. Rawlsing must still possess everything it claims to know and must be able to deterministically regenerate the deleted compiler state and reproduce the same governed products.

Failure of this test means the deleted object was not actually disposable and must be reclassified.

## 10. NO PREMATURE PIPELINE-GENERATOR CONCRETIZATION

Until Chetiri closes or HQ explicitly overrides this protection, new source→structural pipeline-generator design SHOULD target carrier-neutral logical interfaces rather than requiring a particular physical empirical carrier.

The desired dependency direction is:

```text
PIPELINE-GENERATOR
        ↓ depends on
C11 LOGICAL REPOSITORY / EMPIRICAL CONTRACT
        ↑ implemented by
PERSISTENT_R5 | SOURCE_BACKED | HYBRID | FIXTURE
```

The generator must not embed `load_parquet_event_table()`-style physical assumptions into semantic stages unless separately proven unavoidable.