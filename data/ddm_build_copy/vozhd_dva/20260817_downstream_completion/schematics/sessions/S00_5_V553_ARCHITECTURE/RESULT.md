# S00.5 — V553 Architecture Build-Out

**Worker:** Rabochii S00.5  
**Stage:** V553  
**Status:** `ARCHITECTURE_COMPLETE`  
**Production implementation performed:** no  
**Current `V553_COMPLETE_FOR_V554`:** `FAIL` — architecture is specified, but the required repairs and completion tests are not yet implemented.

## Executive architecture

V553 should converge on the **sparse exact-key temporal compiler already present inside `ddm_v553_temporal_pressure.py`**, fronted by the strong canonical V552J publication verifier and hardened by two missing gates: exact V552J↔V552 fact coherence and explicitly certified cross-wave comparability authority. The parallel harmonization/readiness/aggregate lane should be subordinated rather than allowed to compete for semantic authority. It remains useful for discovery, preflight, diagnostics, and a reversible secondary country-year projection; it must not authorize temporal keys, provide structural pressure values, interpolate missing years, or reconstruct exact identity. The completed stage should publish four primary semantic/negative tables, one secondary reversible projection, one exact V554 handoff, and manifest/readiness metadata. V554 must be able to resolve exact V553 key/observation/relation/limit objects and their V552/V552J lineage without synthesizing country:year identities or requiring aggregate files.

The architecture preserves the strongest current work rather than starting over: `ddm_v553_canonical_harmonization.py` is a strong fail-closed ingress adapter; `ddm_v553_temporal_identity.py` is a strong identity validator; the sparse builders in `ddm_v553_temporal_pressure.py` already encode the right primary object grains. The repair is therefore a **promotion-and-consolidation operation**, not a replacement system.

## Binding S00 reconciliation

| S00 excavation finding | Forward evidence | Backward evidence | Vozhd ruling | Concrete V553 architecture consequence |
|---|---|---|---|---|
| V552 fact and V552J authorization are complementary co-inputs | Current V553 can reopen direct V552 material after V552J admission | V554 needs structural provenance plus V553 temporal meaning | Direct V552 reuse is lawful only when coherent with the V552J-authorized fact/scope; mismatch fails closed | Add a V553-owned strict coherence gate; never rematch an authorized V552J row to a substitute fact |
| Exact sparse temporal objects are primary authority | Sparse key/observation/delta/gap objects already exist beside aggregate harmonization | Current V554 ignores them and consumes aggregate country-year pressure | Sparse exact identity outranks aggregate projection | Promote sparse compiler as the sole semantic path; aggregate becomes secondary and reversible |
| Earlier certified semantic/directionality/position authority governs comparability | Legacy harmonization can count high-confidence or untyped overlay rows as certified | Shared-column/aggregate identity is weaker than exact object-level authority | Heuristic/review/file-presence signals do not create authority | Require explicit governed/certified status at the authority input; remove fallback certification |
| V552 temporal-key-source is lineage, not comparability authority | Sparse path already carries temporal-key-source IDs | V554 loses them when it synthesizes country:year IDs | Wave-local factual eligibility/source lineage cannot be promoted into cross-wave authority | Carry temporal-key-source IDs on observations/handoff, but never use them alone to authorize a comparative key |
| Readiness/probe scores are execution context, not pressure | Legacy pressure intensity uses coverage, differences, missing overlays and thin/readiness | V554 currently uses aggregate/readiness material in seed construction | V553 may not derive pressure from readiness/probe state | Canonical observation values come only from direct V552 facts; readiness stays metadata |
| Measured zero and absence/gap are distinct | Sparse observations can preserve direct structural zero while gap artifacts exist separately | Downstream needs temporal state without imputed zero | Measured zero, valid empty, temporal gap and blocked/noncomparable are distinct | Zero remains an observed value; gaps/limits have null semantic value and typed reason |
| Noncomparability must survive | Harmonization can call wave pairs comparable from shared column surfaces | V554 needs exact relation objects or explicit inability to relate them | No delta for noncomparable anchors | Numeric relation only for authorized comparable pairs; otherwise emit a typed limit |
| Interpolation is not default evidence | Legacy compiler still publishes interpolation/year-expanded surfaces | Aggregate-first V554 can consume interpolated pressure as if primary | Missing years may not be interpolated merely because they are missing | Remove interpolation from canonical semantics; retain code only as non-authoritative compatibility/diagnostic if needed |
| Structural rupture candidate is not a causal event | Current rupture logic has status mismatch and mislabels large signed moves as reversal | No external event-authority source exists at the seam | Candidate requires a deterministic/versioned rule; causal event claim requires separate authority | Candidate metadata is optional relation annotation under approved rule; otherwise disabled, never causal |
| V554 may compose earlier objects directly with V553 | Sparse V553 already carries many upstream IDs | Current V554 synthesizes weaker country/year pressure IDs | V552 fact + V552J authorization remain the normative structural pair under V553 temporal meaning | Repair `v553_v554_handoff_index` to carry exact V553 and upstream IDs; aggregate is optional convenience |

### Worker suggestions narrowed or rejected by the ruling/current code

- Aggregate/shared-column harmonization cannot be promoted to primary comparability. S00 makes exact sparse identity primary and requires certified authority.
- V553 must not “repair” an authorized V552J association by searching for a better V552 fact. The current reusable resolver is useful diagnostically, but once V552J names an admitted fact, disagreement is an integrity failure and must fail closed.
- Cohort/person-development requirement outputs in current V553 publication are outside frozen V553 jurisdiction and should disappear from the canonical artifact set.
- A rupture-event slot has no lawful positive semantics without separate event authority. The only V553-owned concept allowed here is a bounded structural candidate under a versioned deterministic rule.

## 1. Current implementation topology

| Current module/surface | What it actually does | Semantic authority it currently claims | Disposition | Why |
|---|---|---|---|---|
| `ddm_v553_canonical_harmonization.py` | Verifies the canonical V552J manifest/readiness/handoff/join/input boundary; validates declared paths, hashes, row counts, schema and scope; distinguishes valid-present, valid-empty, missing, unreadable, schema-invalid and integrity-invalid | Upstream publication/integrity admission | **KEEP / PROMOTE** | Strongest current ingress code and already substantially matches S00 fail-closed law |
| `ddm_v553_temporal_identity.py` | Normalizes one source-family/country scope, requires real calendar anchors, rejects duplicate years, orders waves | Canonical source/country/wave/year identity validation | **KEEP / PROMOTE** | Clean pure validator; no need to redesign |
| `ddm_v553_harmonization.py` | Builds wave bundles, overlay inventory, shared-column surfaces, pair evidence and readiness/harmonization scores | Currently can imply certification/comparability from explicit status, confidence, or raw row presence | **REPAIR / DEMOTE** | Useful preflight, but fallback certification and shared-column comparability are too weak for semantic authority |
| `ddm_v553_repo_discovery.py` | Discovers family-aware wave roots and overlay locations | Intended nonsemantic discovery; directory scoring currently rewards overlay presence | **KEEP / REPAIR** | Discovery may locate candidates, but must remain authority-neutral or explicitly certification-aware |
| `ddm_v553_temporal_pressure.py` — sparse path | Forms stable key profiles, direct-V552 observations, cross-wave deltas, gaps, rupture candidates and a sparse V554 handoff | Closest implementation of accepted V553 families | **PROMOTE / REPAIR** | Correct production nucleus; needs exact fact coherence, per-key authority, relation/negative cleanup, ruled rupture semantics and exact handoff |
| `ddm_v553_temporal_pressure.py` — legacy aggregate/interpolation path | Computes pressure from overlay coverage/differences/missingness/readiness; publishes country-year/year-indexed/interpolated surfaces and many audits/ledgers | Currently looks primary and is actually consumed downstream | **DEMOTE / DEPRECATE** | Semantically unlawful as pressure authority; retain only a projection derived from canonical sparse objects |
| `ddm_v553_schema.py` | Defines both sparse exact contracts and a large legacy/diagnostic artifact family | Multiple parallel primary-looking contracts | **MERGE / REPAIR** | Collapse primary publication to the finite target; compatibility schemas may remain temporarily but role-labeled |
| `compile_v553_temporal_pressure_field.py` | Direct entrypoint into the temporal compiler plus readiness validation | Production V553 build | **KEEP / PROMOTE** | Make this the one canonical semantic CLI |
| `compile_v553_wave_harmonization.py` + `_from_repo.py` | Explicit/repository preflight, discovery and harmonization reports/evidence | Parallel readiness/harmonization entrypoints | **MERGE / DEMOTE** | Keep as preflight adapters feeding the canonical build; their outputs are diagnostic |
| `compile_v553_thin_layer.py` + V553 in `ddm_v5_thin_end_to_end.py` | Thin scaffold based on obsolete `v552j_structural_handoff_packet.json` and aggregate/interpolated expectations | Explicitly boundary/readiness only | **COMPATIBILITY-ONLY / REPAIR** | Never semantic; update paths after canonical contract freezes |
| Readiness/run-manifest logic | Publishes readiness from counts, harmonization scores and a very large artifact list | `ready_for_v554` can become true from a small count condition | **MERGE / REPAIR** | Replace count/readiness-score semantics with a finite invariant gate |
| `v553_v554_handoff_index` + legacy downstream handoff | New sparse handoff exists beside a blocked legacy shadow | Competing handoff surfaces | **PROMOTE ONE / RETIRE ONE** | Repair exact refs in `v553_v554_handoff_index`; remove legacy shadow from authority |
| `ddm_v554_seed_contract.py` V553 intake | Reads V553 readiness/harmonization and country-year/year-indexed aggregate pressure; synthesizes `country:year` pressure IDs | Actual downstream consumer boundary | **CONSUMER-PROOF TARGET** | Do not redesign V554 here; V553 must make exact composed intake possible |
| `test_postg5_v552j_v553_consumer_contract.py` + Wave-0 harness | Strong V552J publication hostile cases plus reference-model vertical continuity with strict downstream XFAILs | Partial proof only | **KEEP / EXTEND** | Add V553 semantic and exact-handoff court; do not falsely un-XFAIL downstream slices |

### What is already strong enough to preserve

1. **Canonical V552J verifier.** It already treats path presence as insufficient, validates the declared publication boundary, and makes valid-empty distinct from corrupt/missing.
2. **Temporal identity normalizer.** It enforces the right source/country/anchor invariants.
3. **Sparse key/observation object shape.** The newer path already carries exact V552 fact IDs, V552 temporal-key-source IDs, structural dimensions, temporal anchors, authorization status and direct structural values.
4. **Sparse delta shape.** The code already separates an authorized structural delta from a probe delta and carries ordered wave/year references. The authoritative branch should be promoted while the probe numeric branch leaves the primary relation surface.
5. **Gap-preserving instinct.** The newer interpolation-segment code already chooses “no interpolation / gap preserved unknown”; that principle becomes canonical.
6. **Forbidden-inference audit.** Keep it as a guard, while removing production artifacts that themselves wander into cohort/person-development semantics.

### The central current contradiction

V553 currently contains two production conceptions:

- **Exact sparse V553:** exact structural keys → direct V552-backed observations → cross-wave relations → typed gaps/limits.
- **Aggregate/readiness V553:** shared column overlap + overlay counts + readiness/coverage → wave/country-year pressure → interpolation and aggregate handoff.

They cannot remain co-primary. The first is S00 V553. The second can survive only as preflight, diagnostics, or a projection whose inputs are the first.

## 2. Target V553 internal architecture

Seven components are enough; no new ontology is needed.

| Component | Responsibility | Inputs / authority owners | Outputs | Role | S00 family | Existing code after repair |
|---|---|---|---|---|---|---|
| **C1 CanonicalUpstreamAdmission** | Verify V552J publication integrity, valid-empty vs failure, scope identity and calendar anchors | V552J publication/permission; canonical identity | Verified wave bundles; typed admission failure/readiness | Validate | LIMIT/NEGATIVE metadata | `ddm_v553_canonical_harmonization.py`, `ddm_v553_temporal_identity.py` |
| **C2 ExactFactCoherenceResolver** | Verify every V552J-authorized row against the exact direct V552 fact/scope and attach temporal-key-source lineage without substitution | V552 fact; V552J association/permission; V552 temporal-key-source | Coherent admitted fact records or hard mismatch | Validate + lineage | KEY, OBSERVATION, LIMIT | sparse part of `ddm_v553_temporal_pressure.py`; reuse V552J field conventions, not permissive rematching |
| **C3 CertifiedComparabilityResolver** | Require explicit governed semantic/directionality/position authority at the exact structural grain | Earlier certified authority | Authorized comparable-key basis or typed insufficiency | Validate | KEY, LIMIT | repaired harmonization helpers + exact key authorization |
| **C4 SparseTemporalCompiler** | Create keys, direct observations, authorized relations/deltas and merged limits | C2 + C3 + temporal anchors | Four canonical semantic/negative tables | Semantic creation | KEY, OBSERVATION, RELATION, LIMIT | sparse builders in `ddm_v553_temporal_pressure.py`, schemas |
| **C5 GovernedTemporalRuleAnnotator** | Optionally annotate relation rows with persistence/drift/rupture-candidate metadata under versioned deterministic rules | Authorized relations + approved rule config | Relation annotations or explicit disabled state | Bounded semantic annotation | RELATION/LIMIT | repair current rupture builder; do not create event ontology |
| **C6 SecondaryProjectionBuilder** | Produce reversible country-year convenience aggregates from sparse objects only | C4 primary objects | Secondary country-year projection | Project | secondary aggregate | repair existing aggregate builder |
| **C7 V554HandoffAndCompletionGate** | Package exact refs, artifact integrity, blockers and finite readiness | C1–C6 | exact V554 handoff, run manifest, readiness report | Package + validate | all | repaired handoff/manifest/readiness in temporal compiler |

### Canonical entrypoint

`compile_v553_temporal_pressure_field.py` should be the **only semantic production entrypoint**.

The two harmonization CLIs remain preflight/discovery adapters. The thin-layer CLI remains compatibility/readiness scaffolding. Neither may publish an artifact that the canonical readiness report identifies as semantic authority.

## 3. Canonical production dataflow

1. **Normalize scope and anchors.** Require exactly one source family/country and unique real temporal anchors. Duplicate or ambiguous anchor fails before semantic construction.
2. **Verify canonical V552J publication.** Validate manifest/readiness/handoff/join/input declarations, hashes, row counts, schema and scope. `VALID_EMPTY` is lawful emptiness; missing/corrupt/schema-invalid/integrity-invalid stops the semantic build.
3. **Check exact V552 coherence.** For each V552J row that claims temporal-field permission, require the exact referenced V552 structural fact in the same run/source/wave/country-or-shard scope. If V552J says fact A and direct V552 material says fact B, fail closed. Do **not** search for a “better” replacement.
4. **Attach V552 temporal-key-source lineage.** Resolve the key-source row tied to that exact fact where available/required. Carry its ID as factual lineage only.
5. **Resolve certified comparability authority.** At the exact structural grain, require the governed semantic/directionality/position authority applicable to the key. Explicit certified/governed status is required. High confidence, reviewability, file presence, shared column names and thin readiness do not count.
6. **Form the comparable temporal key.** Stable key basis is source family + country + allowed structural grain + resolved semantic dimensions. It is wave-independent so observations across waves can share it, but it is never a `shared_*` label or country:year aggregate identity.
7. **Admit observations.** One authoritative observation = one exact comparable key × temporal anchor × exact V552 structural fact. Semantic pressure value is copied from V552; `0` is an observed zero. Readiness/probe values may be diagnostic fields only.
8. **Derive temporal relations.** Order authoritative observations within one comparable key. Numeric delta/direction is created only for an authorized comparable pair. A gap between observed anchors may be recorded as span metadata, but a missing anchor is never interpolated.
9. **Emit negative authority.** Successful semantic runs may emit typed `TEMPORAL_GAP`, `NONCOMPARABLE`, `BLOCKED_OR_PROBE_ONLY`, `INSUFFICIENT_CERTIFIED_AUTHORITY`, and bounded uncertainty states. Transport/integrity failure is a run failure in readiness, not a fabricated semantic row. Valid-empty remains its own run/admission state.
10. **Apply optional governed temporal rules.** Persistence/drift/rupture-candidate annotations are absent unless a deterministic `rule_id` + `rule_version` is approved. A structural candidate never becomes an external event or causal claim.
11. **Project secondary aggregate.** Country-year projection is computed only from canonical sparse object IDs, records all contributors/coverage, and is marked `SECONDARY_REVERSIBLE`.
12. **Build exact V554 handoff.** Each handoff scope references exact key, observations, relations, limits, V552 fact IDs, V552J authorization/association lineage, and certified authority refs. Secondary aggregate refs are optional convenience only.
13. **Run the completion court.** Manifest verifies publication integrity; readiness evaluates the finite gate below. Any ambiguity about primary vs compatibility authority is a failure.

## 4. Canonical artifact contract

Eight physical artifacts are sufficient.

| Artifact | Family / row grain | Required identity and lineage | Epistemic / permission fields | Status | V554 use |
|---|---|---|---|---|---|
| `packets/v553_harmonized_pressure_key_index.parquet` | `TEMPORAL_KEY`; one wave-independent exact comparable structural key | stable key ID; source family/country; exact structural dimensions; semantic signature; certified authority refs | authorization/comparability status, authority status, blocker reason | **PRIMARY** | Exact temporal structural identity |
| `packets/v553_temporal_pressure_observation_index.parquet` | `TEMPORAL_OBSERVATION`; one key × observed anchor × exact V552 fact | observation ID; key ID; year/wave; exact V552 fact; V552J authorization; V552 temporal-key-source lineage | observation status, direct pressure value, `observed_zero`, measurement evidence, bounded uncertainty | **PRIMARY** | Exact observed anchors |
| `packets/v553_cross_wave_delta_index.parquet` | `TEMPORAL_RELATION`; one key × authorized ordered observation pair | relation/delta ID; key ID; from/to observation IDs and upstream lineage | comparability status; delta/direction; span; optional governed rule annotations | **PRIMARY** | Governed temporal change |
| `packets/v553_temporal_limit_index.parquet` | `TEMPORAL_LIMIT / NEGATIVE AUTHORITY`; one key/scope/anchor-or-pair × typed limit | stable limit ID; key/scope refs; relevant upstream refs | limit type/reason, null semantic value, downstream permission, uncertainty context | **PRIMARY** | Preserve inability/absence without invented value |
| `packets/v553_country_year_pressure_field.parquet` | secondary aggregate; country × year × declared slice | projection ID + aggregation-rule version + all contributing sparse IDs | `projection_status=SECONDARY_REVERSIBLE`, coverage/contributor count | **SECONDARY** | Optional convenience only |
| `packets/v553_v554_handoff_index.parquet` | packaging; one downstream-ready exact key scope | key + observation/relation/limit IDs; V552 fact IDs; V552J authorization IDs; certified authority refs | `ready_for_v554`, blocker codes, primary object counts | **PRIMARY HANDOFF** | Normative V553 consumer boundary |
| `manifest/v553_run_manifest.parquet` | one artifact declaration per run artifact | run ID; path; schema/compiler version; upstream hashes; artifact hash/row count | role = PRIMARY/SECONDARY/DIAGNOSTIC/COMPATIBILITY; integrity status | **PRIMARY METADATA** | Verify exact publication |
| `manifest/v553_temporal_readiness_report.json` | one run | run ID + manifest reference | `V553_COMPLETE_FOR_V554`, failed gate codes, optional-rule state, legacy containment | **PRIMARY GATE** | Gate only; never structural pressure |

### Artifacts that should no longer be primary

**Diagnostic only**
- wave harmonization table/report/evidence/difference ledger;
- key-candidate/blocker and structural-dimension-resolution audits after their authoritative states are represented in key/limit rows;
- pressure-basis/confidence-penalty ledgers if retained;
- source-wave/temporal-anchor discovery manifests;
- duplicate comparability/rupture-block audits after canonical fields exist.

**Compatibility only, then retire after consumer migration**
- `v553_year_indexed_pressure_over_time`;
- year-expanded `v553_temporal_pressure_field` / thin temporal-pressure packet;
- legacy `downstream_v554_handoff_index`;
- thin-layer V553 packet;
- contradiction/absence-over-time legacy projections.

**Remove from canonical publication**
- interpolated pressure-over-time;
- interpolation segment/policy/manifest as semantic outputs;
- readiness-derived pressure-component breakdown;
- rupture-event-slot ledger without event authority;
- cohort-window/person-development requirement index;
- duplicate temporal-authority and absence/noncomparability registers once merged.

## 5. Identity / authority / precedence rules

1. **V552 fact > any V553 reconstruction.** V552 owns the measured structural value and factual provenance. V553 copies it or lacks it.
2. **V552J authorization controls admission.** V553 may verify the producer-bound association but may not substitute a different V552 fact.
3. **V552 temporal-key-source is lineage only.** It can explain why a wave/fact is eligible; it cannot by itself make two waves comparable.
4. **Certified earlier authority > heuristic/review presence.** Only explicit governed/certified semantic/directionality/position authority can authorize cross-wave comparability.
5. **Exact sparse V553 identity > aggregate projection.** Aggregate/shared labels are never a source of canonical key identity.
6. **Structural pressure value > readiness/probe score.** Readiness, harmonization, coverage and confidence may describe execution/epistemic state but cannot alter or replace the V552 value.
7. **Observed zero > absence inference.** Zero is a measured value. Missing anchor/gap has null semantic value.
8. **Comparability is permission, not confidence.** Missing authority or incompatible identity is not a low-confidence relation; there is no semantic delta.
9. **Thin/readiness is nonsemantic.** It can stop execution or report blockers, never generate temporal meaning.
10. **Structural rupture candidate ≠ event/causal rupture.** Candidate only under a deterministic versioned relation rule; external event claim requires separate governed authority.

### Current violations/ambiguities that implementation must remove

- `_certified_overlay_row_count` can count high-confidence rows—or all rows when status/confidence columns are absent—as certified.
- Harmonization wave-pair comparability is largely shared-column/readiness logic rather than exact key-level certified authority.
- Repository discovery scoring rewards overlay presence and therefore risks biasing input selection toward unauthoritative material.
- V553 uses the V552J structural-dimension resolver in a way that can reopen matching instead of treating a disagreement with the producer-bound authorized fact as failure.
- Legacy pressure intensity is computed from overlay coverage, difference coverage, missingness and thin/readiness.
- Interpolation/year-expanded paths create value-bearing surfaces for missing years.
- Primary-looking relation output still has probe numeric deltas; probe numerics belong in diagnostics, not the authoritative relation.
- Rupture code checks `"comparable"` while authorized deltas emit `"authorized_comparable"` and calls any sufficiently large signed move a `direction_reversal`.
- Cohort/person-development requirements are emitted by V553 despite being outside its jurisdiction.
- Readiness can claim V554 readiness from object counts while still naming aggregate/interpolated expectations.
- Current V554 consumption synthesizes `country:year` pressure IDs from aggregate surfaces rather than resolving sparse objects.
- Negative/readiness/authority/handoff state is duplicated across many overlapping artifacts.

## 6. Completion gap matrix

| Capability | Current classification | Required completion action |
|---|---|---|
| Canonical V552J admission verification | `ALREADY_STRONG` | Promote canonical adapter as sole ingress; retain hostile boundary tests |
| Source/country/wave/year temporal identity | `ALREADY_STRONG` | Retain temporal identity normalizer |
| Exact V552J↔V552 fact coherence | `PARTIAL_NEEDS_REPAIR` | Require exact authorized fact ID/scope; ban rematching/substitution |
| Certified cross-wave authority | `PARTIAL_NEEDS_REPAIR` | Remove confidence/presence fallbacks and shared-column authorization |
| Exact temporal key | `PRESENT_BUT_NEEDS_PROMOTION` | Promote stable sparse key; forbid shared/aggregate fallback identity |
| Temporal observation | `PRESENT_BUT_NEEDS_PROMOTION` | One exact fact per observation; direct V552 value only; measured zero preserved |
| Temporal relation/delta | `PARTIAL_NEEDS_REPAIR` | Semantic delta only on authorized comparable pairs; remove probe delta from primary relation |
| Typed negative/limit states | `DUPLICATE_OR_CONFLICTING` | Merge semantic negatives into one limit artifact; transport/integrity failure stays in readiness |
| Uncertainty/confidence | `DUPLICATE_OR_CONFLICTING` | Carry uncertainty as epistemic metadata; prevent scores from becoming facts/authority |
| Persistence/drift | `MISSING` | Optional: enable only under a versioned rule; not required for minimum V554 handoff |
| Structural rupture candidate | `PARTIAL_NEEDS_REPAIR` | Fix comparability/semantics; require approved rule or explicit disablement |
| Lineage/provenance | `PARTIAL_NEEDS_REPAIR` | Enforce exact one-fact lineage and propagate exact refs through handoff |
| Readiness/integrity | `DUPLICATE_OR_CONFLICTING` | Reduce to run manifest + finite readiness gate |
| Secondary aggregation | `WRONG_PRIMARY_SURFACE` | Rebuild only from canonical sparse objects with contributor refs |
| V554 consumption/handoff | `WRONG_PRIMARY_SURFACE` | Promote exact handoff and prove aggregate-independent resolution |
| Forbidden persona/biography/cohort semantics | `PARTIAL_NEEDS_REPAIR` | Keep guard audit; remove cohort/person-development publication |

## 7. Dependency-ordered implementation strategy

### V553-P1 — Admission and authority hardening

**Goal:** make it impossible for unauthoritative overlay material or a substitute V552 fact to enter semantic compilation.

**Likely production files**
- `ddm_v553_canonical_harmonization.py`
- `ddm_v553_harmonization.py`
- `ddm_v553_repo_discovery.py`
- `ddm_v553_temporal_identity.py`
- `tests/test_postg5_v552j_v553_consumer_contract.py`

**Invariants**
- all existing V552J missing/corrupt/schema/integrity distinctions survive;
- `VALID_EMPTY` remains lawful emptiness;
- only explicit certified/governed authority counts;
- discovery/preflight is nonsemantic.

**Proof**
- untyped overlay does not certify;
- high-confidence/review-only overlay does not certify;
- valid-empty ≠ missing/corrupt;
- multi-family/country/duplicate-anchor cases fail.

**Dependencies:** none.  
**Parallelism:** test-fixture scaffolding may proceed separately; semantic packets must wait for this contract.

### V553-P2 — Exact sparse key and observation core

**Goal:** promote exact key/observation compilation and enforce strict V552J↔V552 coherence.

**Likely production files**
- `ddm_v553_temporal_pressure.py`
- `ddm_v553_schema.py`
- `compile_v553_temporal_pressure_field.py`
- new focused `tests/test_v553_sparse_temporal_contract.py`

**Invariants**
- V552 value is never recomputed;
- an authorized V552J row cannot be rematched to another V552 fact;
- temporal-key-source remains lineage only;
- measured zero is preserved;
- readiness/probe numerics never populate semantic pressure.

**Proof**
- fact A authorized / fact B presented → hard fail;
- key is stable across waves for the same exact structural semantics;
- every observation resolves one authoritative V552 fact;
- zero-versus-gap hostile case.

**Depends on:** P1.  
**Parallelism:** key/observation tests can be split from implementation after P1 freezes the ingress contract.

### V553-P3 — Relations, negative authority, governed temporal rules

**Goal:** complete authorized temporal relations and collapse negative states into one primary limit surface.

**Likely production files**
- `ddm_v553_temporal_pressure.py`
- `ddm_v553_schema.py`
- `tests/test_v553_sparse_temporal_contract.py`

**Invariants**
- numeric semantic delta only on authorized comparable observations;
- gaps/noncomparability/blockers cannot become zero;
- no semantic interpolation;
- rupture candidate has rule ID/version and never asserts causal event.

**Proof**
- comparable pair gets correct delta/direction;
- noncomparable pair gets no semantic delta;
- gap and insufficient authority are typed separately;
- rupture candidate/event boundary.

**Depends on:** P2.  
**Parallelism:** tests can be split by relation vs negative cases, but production edits share compiler/schema and should merge serially.

### V553-P4 — Publication consolidation and secondary projection

**Goal:** enforce the eight-artifact publication contract, make aggregate strictly secondary/reversible, and contain old harmonization/thin paths.

**Likely production files**
- `ddm_v553_temporal_pressure.py`
- `ddm_v553_schema.py`
- `compile_v553_wave_harmonization.py`
- `compile_v553_wave_harmonization_from_repo.py`
- `compile_v553_thin_layer.py`
- `ddm_v5_thin_end_to_end.py`

**Invariants**
- exactly one semantic compiler entrypoint;
- sparse semantics survive deletion of all aggregate/diagnostic files;
- aggregate contains contributing exact object IDs;
- cohort/person-development and event-slot artifacts disappear from canonical publication;
- readiness cannot source pressure.

**Proof**
- canonical artifact allowlist;
- aggregate-cannot-replace-sparse;
- old artifacts role-labeled diagnostic/compatibility;
- no persona/cohort outputs.

**Depends on:** P3.  
**Parallelism:** wrapper/thin compatibility edits can run separately after artifact schemas freeze.

### V553-P5 — Exact V554 handoff and completion court

**Goal:** make the consumer boundary resolvable from exact V553 objects and run the finite completion gate.

**Likely files**
- `ddm_v553_temporal_pressure.py`
- `ddm_v553_schema.py`
- `ddm_v554_seed_contract.py` **only if a minimal read adapter is required to prove exact consumption; do not redesign seed semantics**
- new `tests/test_v553_v554_handoff_contract.py`
- Wave-0 `test_vertical_continuity.py` / `vertical_continuity.py` for V553-local production hooks

**Invariants**
- handoff resolves exact key/observation/relation/limit IDs plus V552/V552J lineage;
- consumer proof does not synthesize country:year identity as a substitute;
- aggregate files are optional to the proof;
- downstream Wave-0 XFAILs remain XFAIL where the first unsatisfied stage is V554+.

**Proof**
- exact-reference composed-consumption test;
- delete aggregate files and handoff still resolves;
- manifest/hash/readiness gate;
- V553-local production hook matches reference-fixture temporal invariants.

**Depends on:** P4.  
**Parallelism:** the consumer-proof fixture can be prepared while P4 lands, but final assertions wait for frozen handoff schema.

**Proposed packet count: 5.**

## 8. Minimum completion test court

### Fast required tests

1. **Canonical V552J admission contract** — keep/extend `test_postg5_v552j_v553_consumer_contract.py`:
   - valid-present;
   - valid-empty;
   - missing;
   - unreadable/corrupt;
   - schema-invalid;
   - integrity/hash/row-count invalid;
   - path-existence alone never grants authority.
2. **Sparse temporal contract** — focused new test file:
   - exact fact coherence;
   - exact stable key identity;
   - explicit certified authority;
   - direct observations and measured zero;
   - comparable relation/delta;
   - typed gap/noncomparability/blocker/uncertainty;
   - no semantic interpolation/probe pressure;
   - optional rule boundary.
3. **V553→V554 handoff contract**:
   - every handoff exact ref resolves;
   - direct V552/V552J lineage resolves;
   - aggregate files can be removed without breaking the exact handoff;
   - synthetic country:year identity cannot substitute for missing sparse objects.
4. **V553-local Wave-0 hook**:
   - actual V553 producer output is checked against the vertical fixture’s key/observation/relation/negative invariants.

### Hostile cases that must exist

- V552J authorizes fact A but V553 is offered/re-resolves fact B → **hard fail**.
- Overlay file exists but has no explicit certified/governed status → **no semantic authority**.
- High confidence/review-required overlay → **no certification**.
- Same-looking columns but distinct exact authority/semantic basis → **noncomparable**.
- Measured `0` between positive observations → **observed zero**, never gap.
- Missing year → **typed temporal gap with null value**, never interpolation.
- Valid-empty V552J publication → **valid empty**, never missing/corrupt.
- Noncomparable observations → **no semantic delta**.
- Aggregate files present but sparse exact refs missing → **completion FAIL**.
- Rupture rule absent → **no rupture candidate**; causal/event field remains absent.

### Wave-0 XFAIL rule

**No existing full-chain strict XFAIL should flip solely because V553 is repaired if its recorded first live gap is V554 or later.** V553 completion should add/promote a V553-local production hook to PASS. Full vertical slices flip only when the downstream stage that actually constitutes their first gap is also satisfied. This avoids turning the reference harness into false evidence of downstream completion.

### Later horizontal qualification

The 35-wave empirical/horizontal qualification is **not** part of this architecture completion and is not claimed here. After the fast gate passes, broader corpus qualification should test deterministic IDs, coverage, source-family diversity and diagnostic behavior without relaxing any semantic gate.

## 9. Finite `V553_COMPLETE_FOR_V554` gate

The gate operator is **ALL REQUIRED CHECKS TRUE**.

- [ ] **G01 Upstream admission:** canonical V552J publication passes integrity/schema/scope or is explicitly `VALID_EMPTY`; bad transport/integrity cannot emit semantics.
- [ ] **G02 Exact fact coherence:** every authoritative observation resolves exactly the V552 fact authorized by V552J in the same scope; zero substitute/rematch cases.
- [ ] **G03 Certified authority:** every authoritative comparable key has explicit certified/governed semantic/directionality/position authority required by its grain; no presence/confidence/review fallback.
- [ ] **G04 Exact key identity:** primary key IDs are sparse, wave-independent structural identities; no `shared_*` or country:year fallback is authoritative.
- [ ] **G05 Observation value:** every authoritative observation value is direct V552 structural value; measured zero preserved; readiness/probe/interpolation never supplies it.
- [ ] **G06 Relation validity:** semantic delta exists only for authorized comparable observation pairs.
- [ ] **G07 Negative authority:** temporal gap, blocked/probe-only, noncomparability, insufficient authority and bounded uncertainty are typed and cannot collapse into zero/default.
- [ ] **G08 Optional temporal rules:** persistence/drift/rupture is either `DISABLED_NO_GOVERNED_RULE` or carries deterministic `rule_id`/`rule_version`; no external event/causal claim without separate authority.
- [ ] **G09 Publication containment:** primary publication is limited to the declared sparse semantic/negative artifacts, exact handoff and manifest/readiness; compatibility/diagnostic artifacts cannot be selected as primary.
- [ ] **G10 Aggregate subordination:** country-year aggregate derives only from sparse IDs, is `SECONDARY_REVERSIBLE`, and can be deleted without breaking handoff.
- [ ] **G11 Exact V554 handoff:** `v553_v554_handoff_index` resolves exact key/observation/relation/limit IDs and relevant V552/V552J/certified-authority lineage.
- [ ] **G12 Integrity/readiness:** run manifest verifies schema/compiler versions, upstream hashes and canonical artifact hashes/row counts; readiness reports failed gate codes deterministically.
- [ ] **G13 Jurisdiction:** no canonical V553 output asserts persona, biography, psyche, household, cohort-development, Enneagram or runtime actor semantics.
- [ ] **G14 Fast completion court:** all focused and hostile-negative V553 tests pass, including aggregate-cannot-replace-sparse and V552J↔V552 mismatch fail-closed.
- [ ] **G15 Consumer proof:** V554 composed-consumption proof resolves exact V553 objects with aggregate files absent.
- [ ] **G16 Wave-0 honesty:** V553-local production hook passes; no downstream strict XFAIL is removed unless its actual first gap is satisfied.

**Current evaluation:** `FAIL_NOT_YET_IMPLEMENTED`.

### Explicitly deferrable without starving V554

- 35-wave horizontal qualification;
- persistence/drift labels when explicitly disabled;
- structural rupture candidates when no deterministic governed rule has been approved;
- external historical event/causal rupture authority;
- physical deletion of compatibility artifacts after downstream migration, provided they are role-labeled non-authoritative and cannot satisfy the completion gate.

## Unresolved Vozhd decision

`VD-V553-01` — **non-blocking:** decide whether the first V553 completion tranche should include an approved deterministic/versioned persistence-drift/structural-rupture candidate rule, or ship those optional annotations as `DISABLED_NO_GOVERNED_RULE`. Recommended default: **ship the minimum completion with optional annotations disabled unless a rule is separately approved**. Numeric authorized temporal relations remain canonical and V554 is not starved.

## Files inspected

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/sessions/S00_5_V553_ARCHITECTURE/ASSIGNMENT.md`
- both forward S00 excavation results (`RESULT.md`, `RESULT.json`)
- both backward S00 excavation results (`RESULT.md`, `RESULT.json`)
- `schematics/synthesis/S00_V552J_TO_V553_RULING.md`
- `schematics/CUMULATIVE_UPSTREAM_MAP.md`
- `schematics/TRANSFORMATION_METHOD.md`
- `data/ddm_build_copy/ddm_v553_canonical_harmonization.py`
- `data/ddm_build_copy/ddm_v553_harmonization.py`
- `data/ddm_build_copy/ddm_v553_temporal_identity.py`
- `data/ddm_build_copy/ddm_v553_schema.py`
- `data/ddm_build_copy/ddm_v553_temporal_pressure.py`
- `data/ddm_build_copy/ddm_v553_repo_discovery.py`
- `data/ddm_build_copy/compile_v553_wave_harmonization.py`
- `data/ddm_build_copy/compile_v553_wave_harmonization_from_repo.py`
- `data/ddm_build_copy/compile_v553_temporal_pressure_field.py`
- `data/ddm_build_copy/compile_v553_thin_layer.py`
- `data/ddm_build_copy/ddm_v5_thin_end_to_end.py`
- `data/ddm_build_copy/ddm_v552j_handoff.py`
- `data/ddm_build_copy/ddm_v554_seed_contract.py`
- `data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py`
- `data/ddm_build_copy/tests/vozhd_dva_wave0/test_vertical_continuity.py`
- `data/ddm_build_copy/tests/vozhd_dva_wave0/vertical_continuity.py`

## Scope explicitly not claimed

No production implementation was performed. This result does not redesign V550–V552J, does not redesign V554 seed semantics beyond the V553 handoff/consumer-proof requirement, does not enter V555+, V3/V2 or runtime implementation, and does not claim 35-wave empirical qualification.
