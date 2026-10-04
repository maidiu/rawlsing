# Corrected current F6/F7 constitution (after HQ203 reconciliation)

This replaces the HQ201 F6/F7 constitution at the points listed. HQ201 remains an **unadopted
worker return** (audit: *"no HQ adoption located at control freeze"*).

## F6 — cross-source constitution

### What is current binding law / implemented now

| Meaning | Owner | Status |
|---|---|---|
| cross-source **coexistence** in one result | `pre553_empirical_query.py` `SOURCE_INDEXED_MULTI_UNIVERSE` | **OWNED AND IMPLEMENTED** — one fact per universe |
| **no implicit pooling** / no synthetic respondent table | `AUTHORIZED_COMPOSITE` gate requiring `SOURCE_COMPOSITION_POOLING` + `SOURCE_UNIVERSE_RELATION` + `WEIGHT_DESIGN_ESTIMAND` | **OWNED AND IMPLEMENTED** — fail-closed bundle |
| typed noncomparability | `pre553_structural_admission.py` `EMPIRICAL_FACT_NONCOMPARABLE` + typed negative states | **OWNED AND IMPLEMENTED** |
| source plurality relations | `pre553_source_relations.py` eight relation kinds, each with its own required material, positive authority kind and explicit `does_not_grant` tuple | **OWNED AND IMPLEMENTED** |
| operation-scoped comparability authority | `allowed_effective_time_or_interval_refs` slot + M1 `rule_relevant_source_relation_comparability_authority_fingerprint` | **SLOT EXISTS, PRODUCER/INSTANCE MISSING** |

### The binding distinction (the headline correction)

> **`SOURCE_INDEXED_MULTI_UNIVERSE` != `AUTHORIZED_COMPOSITE`.**

- **`SOURCE_INDEXED_MULTI_UNIVERSE`** evaluates each universe separately and emits **one fact per
  universe**. Required authority: source-local. **It does not pool and requires no pooling
  authority.** OBL063: *"Executor returns one fact per universe; it does not pool sources."*
- **`AUTHORIZED_COMPOSITE`** pools/combines universes into **one** fact and therefore requires an
  exact operation-specific authority bundle binding **pooling, nonduplication and estimand
  composition**. OBL063: *"Blanket source-local pooling is not allowed."*

**Therefore:** lawful cross-source coexistence without row pooling does **not** inherit a pooling
requirement merely because `AUTHORIZED_COMPOSITE` has one.

### What is NOT settled in F6

- typed cross-source relation kinds (corroboration / contradiction / complementarity) beyond the
  existing relation machinery — **no new object family required**; at most a typed annotation
  bound to a relation authority ref (see `07`).
- composed-world relation mapping pending adjudication of H06/H09 (audit W15/W14 = UNKNOWN).

## F7 — temporal constitution

### What M1 actually is

`m1_temporal_v554_admission_dedup.py` is a **fail-closed fingerprinted ingress/dedup seam**, not a
temporal producer. It defines three signatures (NONTEMPORAL-EXACT, TEMPORAL-POINT-EXACT,
TEMPORAL-RELATIONAL-EXACT) and on any temporal signature it requires
`REQUIRES_V553_OWNED_TEMPORAL_MEANING`.

**M1 proves** a lawful transport/admission/dedup home and exact fingerprint equality.
**M1 does not prove** persisting temporal-object identity, positive relation meaning, time grain,
directionality authority, or rupture semantics. It carries
`rule_relevant_effective_time_semantics_fingerprint` — a fingerprint *of* a semantics that must
already exist.

### Binding noncollapse that survives

> **`DIFFERENCE != TRAJECTORY`** — two observations differing across time does not by itself
> constitute an ordered trajectory and does not by itself confer directionality authority.

**Not law:** *"trajectory requires at least three anchors"* is **UNSUPPORTED_STRENGTHENING**
(no adopted authority; audit REPORT line 103).

### Time grain

Not a universal point-year-versus-fieldwork-interval binary. See `05`. Current time fields are
polymorphic (`allowed_effective_time_or_interval_refs`), and the V3 executor's `time_granularity`
uses **INSTANT**/**INTERVAL**, not point-year/fieldwork. The grain question is
operation/source-specific and remains **UNKNOWN_PENDING_EXACT_EVIDENCE** rather than a decidable
binary.

### Genuinely unresolved F7 meanings

After corrections: **one** affirmatively unconstituted meaning (authority for temporal
**directionality**), **seven** UNKNOWN pending the missing semantic test, **three** owned and
implemented, **three** needing only typing or a concrete instance. See `04`.

## Residual class boundary

`MultiSourceTemporalWorld` remains **EXPLORATORY / OPTIONAL**, not a terminal requirement. Adopted
law declines a universal geometry/world carrier; optional local carriers are not terminal
necessities.

## F8 — not decided here

The mature-world F8/service-operation contract belongs to residual node **H-D**. The recalibration
warns: *"Do not classify this as mere transport until the semantic operation is proven."* This
reconciliation makes no F8 claim.
