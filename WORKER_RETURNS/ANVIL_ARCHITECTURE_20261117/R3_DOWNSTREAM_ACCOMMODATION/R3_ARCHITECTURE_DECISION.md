# R3 ARCHITECTURE DECISION — downstream accommodation

**Status:** `AUTHOR_CONDITIONAL_ACCOMMODATION_CANDIDATE_PENDING_FOCUSED_C`.
**Branch:** `agent/anvil-r3-downstream-accommodation-20261117-r1`.
**Starting HEAD:** `f95e6eecc476ac09400a583503828bdee5571a24`.
**Inherited candidate:** `06e88a5ac7e4c14362a97a046f44e25d8eec4162` (R2 tag
`anvil-architecture-candidate-20261117-r1`/`r2` untouched).
**Product cut:** `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`.
**Prior C:** `d109ffa9fa8d88f60b6d8c11f3885428555c7bcd`, scoped acceptance of
the conditional direction only — not whole downstream accommodation.
**Protected currentness observed:** `5d387a9a8c72c68e6ef87a671d6d486bfd1fc43e`,
paired PYAT revision 11, read-only; prior `31291` snapshot is not live.
**No** new product code, native run, source right, science/actor authorization,
protected adoption or H1.

## 1. Decision in one paragraph

**Retain the accepted conditional physical direction** — prepared-session-first
for within-process reuse, conditional one-journal/source-derived Q2 construction
with full physical proof and second-certificate fallback, selected no-clobber
recovery repair, and the durable locator index **held** — and **amend the access
architecture** with an explicit, versioned, derived-access contract over the
unchanged 13-family canonical C11. The contract defines respondent-major event
access, question-major selector/denominator access, and content-addressed
derived products (F1–F4, F6/F7 owner products, FF01, FF02/ N9/N10E/N10W/
PRE-V3/SEAM/SOROK boundaries). It creates no new canonical body family, no new
database, no new science engine and no psychological C11 columns. The physical
storage stays; the access/derivation architecture becomes explicit and
testable. Savings remain conditional on measurement: prepared sessions remove
repeated `S` only, not fresh-open `S`, full-population `Q` or evidence-output
`O`.

## 2. What is actually preserved versus accommodated

| Grade | Meaning in R3 |
|---|---|
| `PRESERVED_BYTES` | exact source/body/ref/state bytes remain in C11 or an immutable source |
| `NOT_PRECLUDED` | no current field/contract logically forbids a future authorized computation |
| `CONCEPTUALLY_ACCOMMODATED` | a concrete information→C11→access→derived-product→consumer route is specified, with owner and falsifier |
| `IMPLEMENTED_FIRST_CONSUMER` | actual code executes that route at the stated scope |
| `SCIENTIFICALLY_OR_ACTOR_AUTHORIZED` | the science/actor/source owner has issued the claim; never inferred here |

The R3 claim is **conceptual accommodation at known downstream maturity**, not
native performance, scientific truth or actor authorization. Existing R2
prepared-path tests are sourcefree implementation evidence; they do not
authorize downstream science.

## 3. Currentness, authority and inherited limits

- Protected `5d387a9a…` and paired revision 11 were read; the prior local
  `31291` snapshot is historical, not live. No protected write.
- R2 C accepted the corrected documentary **direction** only. Its source-lineage
  inspection was sampled, not exhaustive; this R3 package does not claim a
  141-row recensus or a new 118/20 guard.
- The 26 PYAT-PC `NOT_ADOPTED`, 14 P4R `HELD`, F26 exact caller/invalidation
  (`K1-CAP-24` / `P4R-R02` / `PYAT-PC-R11-21`) and separate 52/24/21 estate
  remain exactly as before. No historical status is promoted.
- The 13-family body remains `EmpiricalUniverse`, `RespondentIdentity`,
  `QuestionVariableBinding`, `RespondentEvent`, `RoutingEligibilityFact`,
  `EmpiricalCoordinateFact`, `WeightMeasureFact`, `AuthoritySnapshot`,
  `SourceUniverseRelation`, `EmpiricalPredicateReplayBinding`,
  `ComparatorReplayBinding`, `DiscoveryBranchReplayBinding`,
  `StructuralAdmissionReplayBinding`.

## 4. The selected access architecture — R3-DERIVED-ACCESS

The canonical body is unchanged. Add a **read-only derived-access contract**,
not a new canonical C11 family:

### 4.1 Respondent-major event view

A typed view over `RespondentEvent` + `RoutingEligibilityFact` +
`EmpiricalCoordinateFact` + `WeightMeasureFact`, keyed by exact
`(universe, respondent, question/native, occurrence/rank/repeat)`:

- exact raw/canonical value and typed state;
- native/canonical/component role refs;
- occurrence group/id/topology;
- risk/eligibility/routing status;
- weight/design refs where issued;
- source/instrument/time/authority refs.

This is the physical view needed for true same-person k≥3, repeated/ranked
events, F2/F3/F4 and FF01. It may be implemented as bounded in-memory typed
selection first; a persisted compact form is a later option, not a new body.

### 4.2 Question-major selector/denominator view

A typed view over `QuestionVariableBinding` + native/canonical/component refs +
`RoutingEligibilityFact` + weight/design and predicate/risk refs:

- native option/form/routing/version;
- eligible / asked / observed / refused / inapplicable / routing-unknown;
- forward and reverse condition/target roles;
- weight/estimand/design scope;
- exact risk-set and predicate refs.

This is the view needed for demand-driven selection without a full respondent
scan for every operation. It is a selector/denominator view, not a new
scientific evaluator.

### 4.3 Derived-product contract

Every downstream product is an immutable manifest with exact:
`input C11 release + universe + fact/ref set + method/authority + typed state +
negative/refusal + replay + owner + validity/invalidation + claim grade`.
Examples:

- `F1-F4` product: native `execute_empirical_query` / `AnalyticalCompositionResult`
  output, exact risk/denominator refs, true same-person joint.
- `F6` numeric product: separate owner-held partial-identification interval and
  uncovered mass; no C11 canonical F6 family.
- `F7` comparability product: separate owner-held wave/source comparison; C11
  supplies separate universes/time/instrument refs, never a fake longitudinal
  row.
- `FF01` conditional support: existing `ExactConditionalSupportProfile` /
  `produce_exact_conditional_support_profile` over native facts.
- `FF02` structural/material product: independent external authority, not a
  relabel of FF01; may reference C11 positions but must carry its own
  provenance/population/time/rule.
- `N9/N10E/N10W/PRE-V3` world possibility: `run_progressive_chain` /
  `provide_empirical_possibility_slice` over C11 facts plus separately issued
  world/structural material.
- `SEAM` encounter/access and `SOROK` actor history: separate owners; C11
  provides source/position/time/occurrence refs, not actor private knowledge.

The v1 fact/ref/replay ABI remains intact. Any versioned compression/sharing is
owner-qualified and must preserve exact fact identity; no permanent per-query
precomputation.

### 4.4 Physical implementation choice

| Choice | Disposition | Reason |
|---|---|---|
| Prepared-session-first within process | **RETAIN** | actual code, exact facts, removes repeated `S`; no new retained artifact |
| Conditional one-journal/source-derived Q2 | **RETAIN CONDITIONAL** | removes duplicate representation only if full physical proof against Q2 survives; second-certificate fallback mandatory |
| Recovery no-clobber claim/lease/typed orphan | **RETAIN CONDITIONAL** | actual target-before-manifest defect; crash-injection proof still required |
| Durable locator index | **HELD** | only route to remove fresh-open `S`, but 1.30 GB cited retained cost and invalidation/rebuild economics unproven; must earn place |
| New primary DB / bitmap / DuckDB / Stone | **NOT SELECTED** | no evidence it beats the derived views on exactness/retention; avoid fashion |
| Batch prepared variable | **PROPOSED_NOT_WIRED** | exact-type guards reject prepared subclass; owner-approved adapter required |

**Key distinction:** unchanged 13-family storage does **not** mean unchanged
access architecture. R3 changes the access/derivation contract, not the
canonical body.

## 5. Strongest-alternative court

### Alternative A — prepared-session-first only

**Verdict: insufficient as the whole destination, retained as the first query
step.** It removes repeated `S` within one process. It does not remove
fresh-open `S`, full-universe `Q` or evidence-output `O`. It also has no
explicit contract for question-major selection, derived products or downstream
owner handoffs. It is a valid optimization, not a complete accommodation.

### Alternative B — demand-driven typed selection / respondent-major + question-major + reusable derived intermediates

**Verdict: selected access architecture.** It directly addresses the known
information/access needs without a new body corpus. It can be implemented in
bounded typed views first, with exact C11 refs and native evaluators. It
accommodates K1-CAP-08/17/23/27 and FF/SEAM/SOROK boundaries at the right
owner grade. It preserves the v1 fact/output ABI.

### Alternative C — compact durable/secondary access

**Verdict: genuinely competitive, held.** It is the only route that can remove
fresh-open `S` and make 1/10/100 fresh processes cheap. But the cited SQLite
index is 1.30 GB (≈4.19× the 310.16 MB estate); invalidation/rebuild frequency
and compact exact encoding are unmeasured. It must pass `#1006` H/S/Q/O and a
retained-size/binding gate. It is not rejected forever and not selected now.

### Alternative D — new canonical body database / full object graph / per-query precompute

**Verdict: rejected.** New authority/body surface, duplicate evidence, RSS/cost,
or stale output. No evidence it is needed for the known capabilities.

## 6. Six capability envelopes — summary

### 6.1 Source observability and native meaning

C11 preserves native item/option/form/routing/version, raw/canonical values,
respondent/household namespace, occurrence/rank/repeat, typed absent/unknown,
weights/design and source/time/authority. The derived observability profile
classifies `OBSERVED_RESPONDENT`, `SAMPLE_DESIGN_ONLY`,
`COLLECTED_BUT_NOT_RELEASED`, `EXTERNAL_GROUP_CONTEXT`, `PROXY_OBSERVED`,
`MEASUREMENT_NONCOMPARABLE`, `RIGHTS_HELD`. A design stratum is never an
individual sect/ancestry. The route is conceptually accommodated; source
rights and wave availability remain owner/source holds.

### 6.2 Respondent-coherent DDM and F1–F4/I03/I05

The respondent-major view carries exact events/occurrences; the question-major
view carries risk/denominator roles; native `execute_empirical_query`,
`execute_exact_bounded_discovery` and `AnalyticalCompositionResult` compute
F1–F4. True same-person k≥3, F2 forward/reverse, F3 minority/recursive and
signed/neutral distinctions are preserved in the native evaluator and exact
refs. Historical V549/V550/V550J semantics are conserved functionally, not as
old carriers. F26 remains held. Pairwise substitution is refused.

### 6.3 F6/F7 numerical and historical comparison

C11 preserves separate releases, universes, waves, instruments, time, design
and source relations. F6 numeric partial-ID/uncovered mass is a separate
owner-held derived product; the I07 structural guard is not numeric proof. F7
cross-wave comparability is a separate owner-held product; same-name variables
are not a measured trajectory, and cross-sections are not an individual
longitudinal join. No pooling without authority. This is a genuine external
science hold, not an architectural omission: the information needed to ask the
question is preserved.

### 6.4 FF01 and Field Forge

`ExactConditionalSupportProfile` already models conditional support with
producer/relation permissions, typed states and replay. The R3 contract extends
the route to `P(Y1..Yk|D,U,W)` and reverse `P(D|Y,U,W)` over exact F1–F4
facts, with ordinary/minority alternatives, role/position contrasts,
branch/recursive conditionals, uncertainty/coverage. FF01 is a derived product;
it is not a canonical C11 psychological field. FF01 measured association is
not FF02 structural power.

### 6.5 FF02/material power, N9/N10E/N10W, PRE-V3, SEAM and SOROK

C11 can supply positions, resources actually measured, time, occurrence,
universe relations and exact fact refs. FF02 must add independently measured
institutional/legal/economic power with its own population/time/rule. N9/N10E/
N10W world possibility uses `run_progressive_chain` / possibility provider plus
separate world material. SEAM needs an encounter/access relation; C11 does not
invent contact probabilities. SOROK `HistoricalWorld` owns actor-specific
access, interpretation, identification and action. Availability ≠ access ≠
comprehension ≠ identification ≠ action. No respondent psyche, sect/ancestry,
longitudinal person, contact probability, hegemony or causal antagonism is
minted.

### 6.6 Construction, query and evidence economics

The selected access architecture separates source decode/Q2 proof, canonical
body, cold `H`, session `S`, per-operation `Q` and evidence `O`. Prepared-first
removes repeated `S` in one process. Demand-driven typed views can reduce
selector/denominator work without a second evaluator. Fresh-open `S` remains
until a compact durable index earns its retained cost. Evidence output is
30–50 MB/fact at 100k before provenance (100 facts 3–5 GB), so exact set-ref
sharing under identical population/condition/routing/measure/wave is required;
replay re-executes; cached facts are never authoritative.

## 7. K1-CAP-08/17/23/27 — specific findings

The generic crosswalk fate is **not sufficient**. Actual adjacent code/contracts
support concrete routes, with different grades:

- **K1-CAP-08 signed neutral/nonneutral structural atom:** source projection
  carries native value/role/authority; `evaluate_structural_empirical_admission`
  provides exact admission/refusal and support/uncertainty material; FF02
  structural owner issues signed/nonneutral meaning. **Partially accommodated;
  signed/neutral is not a standalone canonical field and must not be collapsed
  to absence or causal power.** Owner-held at FF02.
- **K1-CAP-17 F6 numerical partial-ID:** no dedicated F6 numeric C11 family or
  complete numeric method exists. `compute_effective_n` is F018 effective-N,
  not F6; I07/I04 structural admission is not numeric partial identification.
  C11 preserves the source/frame/design/weight/uncertainty material; F6 interval
  and uncovered mass are a separate owner-held derived product. **Owner-held
  science, not architectural loss.**
- **K1-CAP-23 objective N9 world vs SOROK person:** `run_progressive_chain`
  and `provide_empirical_possibility_slice` produce world/possibility material;
  `sorok_history.owner.HistoricalWorld` is a separate actor reader. **Route
  conceptually accommodated; actual N9/SOROK first reader owner-held.**
- **K1-CAP-27 J-to-FF handoff:** `j_component_certification_validator` +
  `JFamilyRoleAssignment`/`JComponentCertificationPremise` +
  `build_m1_bundle_from_m01`/`adapt_m1_disposition_to_m2` provide the exact J/
  FF manifest path. **Route exists at code-contract grade; selected J→FF
  first reader and science remain owner-held.**

## 8. Explicit dispositions

- **RETAIN** prepared-session-first within-process.
- **RETAIN CONDITIONAL** one-journal/source-derived Q2 and recovery repair.
- **HOLD** durable locator index pending H/S/Q/O and compact exact
  encoding/binding/invalidation/retained-size evidence.
- **MODIFY** access/derivation architecture: add R3-DERIVED-ACCESS contract;
  canonical 13-family body unchanged.
- **PROPOSED_NOT_WIRED** prepared Batch/wrapper path.
- **OWNER_HELD** FF02 material power, F6 numeric, F7 comparability, N9/N10W/
  PRE-V3, SEAM encounter/access, SOROK actor, F26, original35/source/science/
  actor rights, 100k/6 GiB/1–10/100.
- **NO NEW** C11 family, primary DB, body corpus, science engine or protected
  status.

## 9. Terminal statement

To the best of what is presently conceptualized downstream, the chosen C11 and
surrounding derived-access/derivation architecture **conceptually accommodate**
the six capability envelopes at the stated grades, with exact routes, preserved
information, falsifiers and owner boundaries. They do **not** yet implement all
first consumers, authorize the science/actor/source claims, or prove native
100k/6 GiB/1–10–100 economics. The remaining gaps are named, bounded and
owner-routed, not hidden under a generic `OWNER_HOLD` or a false claim of
universal future proof.
