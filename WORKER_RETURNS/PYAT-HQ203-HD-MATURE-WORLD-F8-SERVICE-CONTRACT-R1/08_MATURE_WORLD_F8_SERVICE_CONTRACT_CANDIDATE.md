# 08 — Mature-world F8 service contract candidate

**Status:** `CANDIDATE_REQUIRING_HQ_ADOPTION__DOCUMENTARY_ONLY__NOTHING_IMPLEMENTED`
**Commission:** PYAT-HQ203-HD-MATURE-WORLD-F8-SERVICE-CONTRACT-R1
**Control tip examined:** `3760ba31761cd6e27e978c31749161feced1a47a`

This contract is derived from HQD-125 §§3, 7, 8, 12 and from code actually present at the control tip. It does **not** adopt H10; H10 is unadopted worker evidence and is used only for corroboration, marked inline.

---

## 0. The load-bearing semantic finding

> **F8 does not transform possibility geometry. F8 selects among pre-materialized geometries.**

`MODEL_ALGORITHM_ID = EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION`

Geometry arrives on `PossibilitySliceEvidence.geometry` from an upstream producer and is chosen by exact `(source_universe_ref, release_ref, target_ref, retained_conditioner_ids)` match, or by a governed strictly-decreasing specificity walkback confined to the same source and release.

Therefore, for the commission's central question — *which world inputs may change possibility geometry/distribution* — the answer is:

**None of them, at F8.** Not "not yet" — at this grain there is no code path by which any world product could do so, even if a rule were written. A world product changes what F8 returns only by causing an upstream producer to materialize a *different evidence slice at a different retained-conditioner grain*. That is a producer-side act, under producer authority.

This is why the contract below separates **selection** from **transformation**, and why it is not reducible to transport.

---

## 1. Contract identity

| field | value |
|---|---|
| contract id | `MATURE_WORLD_F8_SERVICE_OPERATION_CONTRACT@1.0.0` (candidate) |
| consumes | `SOURCE_BACKED_POSITIONED_SUBJECT_POSSIBILITY@1.0.0` |
| query contract | `POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_QUERY@1` |
| field contract | `POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_FIELD@1` |
| consumer policy | `PREV3_OBJECTIVE_CONSUMER_BOUNDED_EVIDENCE@1.0.0` |
| structural gate | `P06` / `I04` structural admission |
| actor firewall owner | `rawlsing_next/m6_actor_safe_expression.py` |

---

## 2. Permitted operations, by world input family

Exactly one operation is available to F8: **selection among pre-materialized exact slices, plus governed specificity reduction.** Everything else in this table is a refusal or an upstream act.

| # | world input family | operation at F8 | required authority | state |
|---|---|---|---|---|
| 1 | exact source-local empirical fact | **CONDITIONER** | `ConditionerBinding`: subject_fact_ref + empirical_coordinate_ref + **positive** comparability_authority_ref + source_universe_ref + release_ref + effective_time_or_interval | form closed, instance per scope |
| 2 | conjunction / joint fact | **CONDITIONER** (multi-binding) | as (1), plus exact per-arity target authority | form closed, producer absent from lineage |
| 3 | branch / configuration incl. minority | **CONDITIONER** | as (1) + branch predicate + validation authority | form closed, instance per scope |
| 4 | structural position / role | **CONDITIONER** *only via exact comparator*; else CONTEXT_ONLY | comparator authority; OBL031 @1.1.3 adopted for exactly one field at `EXACT_FROZEN_D08GrammarBinding_TYPE_AND_VALUE_ONLY` | one field adopted; coverage unproved |
| 5 | opportunity / constraint | CONTEXT_ONLY | — | audit W06: F8 only "through lawful comparator/use" |
| 6 | mediation / route | NOT_ADMITTED as conditioner | route legitimacy lived in absent C1-03A | UNBOUND |
| 7 | higher-order topology | CONTEXT_ONLY | — | no comparator maps topology → conditioner |
| 8 | objective consequence (SDTF P1–P5) | NOT_ADMITTED | OC03 seam | `NOT_YET_APPLICABLE` — "P1-P5 remain CANDIDATE_NOT_CURRENT" |
| 9 | pressure / counterpressure | CONTEXT_ONLY | — | W08 UNKNOWN; no new object named |
| 10 | temporal products | NOT_ADMITTED | — | no current producer; W15 UNKNOWN |
| 11 | cross-source relations | **REFUSAL_ONLY** | — | `cross_source_proxy = FORBIDDEN_IN_V1` |
| 12 | uncertainty / noncomparability | ELIGIBILITY_FILTER (preserve, never floor) | typed states | form closed |
| 13 | current vs historical validity | ELIGIBILITY_FILTER (fail-closed) | lifecycle selection + validity states | form closed |
| 14 | service-source applicability | would be SOURCE_SELECTOR — **UNBOUND** | none adopted | validation-only today; H-C lane |
| 15 | whole-world container | NOT_ADMITTED; **OPTIONAL** by finding | OC05 seam | `NOT_YET_APPLICABLE` — "no universal terminal may be invented" |

---

## 3. Mandatory inputs to any mature-world F8 call

Derived from present code, not from proposal:

1. `subject_ref`, `target_ref` — exact `ExactRef`s. No latest/default/nearest/fuzzy/`*` resolution is lawful anywhere.
2. exactly one `source_universe_ref` and one `release_ref`, shared by every conditioner binding. No implicit bridge.
3. ≥1 `ConditionerBinding`, each carrying a **positive** `comparability_authority_ref`.
4. `purpose == "EMPIRICAL_POSSIBILITY_ONLY"`. Anything else raises.
5. a `PositionedSubjectPossibilityModelRule` carrying `model_authority_ref`, `walkback_authority_ref`, ≥1 `source_universe_refs`, and a `positive_proxy_authority_refs` list covering every walkback step.
6. replay determinants — `verify_positioned_subject_possibility_replay` must reproduce `result_hash` and `material()` exactly.

## 4. Conditional inputs

Present **only** where the corresponding authority exists, and marked as present:

- governed specificity walkback steps (`SpecificityWalkbackStep` with `proxy_authority_ref`) — same source/release only;
- `negative_authority_refs` on an F8-side rule;
- `target_use_permission_refs` + `time_geography_applicability` where the input came through P06 admission;
- `estimand_refs` / `measure_and_weight_authority_refs` where a measure/estimand-scoped admission applied.

Absent authority ⇒ typed absence, never a default.

## 5. Refused inputs (structurally unaccept-able)

| refused | enforced by |
|---|---|
| any realized actor state / biography / personality | `purpose != EMPIRICAL_POSSIBILITY_ONLY` raises; `actor_inference_allowed = False`; `FORBIDDEN_INTERPRETATION_MARKERS` reject actor semantics at rule construction |
| population or source-local statistic read as a positioned-subject attribute | `ClaimCeiling` lattice — `POPULATION_STATISTIC`/`SOURCE_LOCAL_STATISTIC` satisfy only themselves |
| any renormalization of coefficient/confidence/semantic scope | `RenormalizationForbidden` |
| merged cross-source respondent row; cross-source jointness claim | `cross_source_proxy = FORBIDDEN_IN_V1`; `SOURCE_RELATION_KINDS` handled only via independent universe states (C30) |
| unauthenticated averaged cross-source value | `SOURCE_CONFLICT != AVERAGE_BY_DEFAULT` (law); no averaging path exists in code |
| interpolated period presented as observation | no interpolation exists — algorithm forbids it; no temporal producer admitted |
| causal attribution of a temporal break | no causal authority at F8; `actor_inference_allowed = False` |
| individual-level change from a field trajectory | no temporal conditioner admitted; walkback is a *specificity* reduction within one source/release, never a cross-time move |
| proxy used to satisfy an exact request | `proxy_can_satisfy_exact_request = False`; result is `EXACT_UNRESOLVED_PROXY_AVAILABLE` with `exact_lane.disposition = UNRESOLVED` |
| current fact substituted for a historical ref | lifecycle `UNKNOWN_CURRENTNESS` / `CONFLICTING_CURRENT_SELECTION` are FAIL_CLOSED |

Rows 1–3, 5, 8, 9, 11 are enforced by **present code**. Rows 4, 6, 7, 10 are stated in H10 as **unadopted** worker evidence; each requires HQ adoption before it can bind, though 4, 6 and 10 are additionally made unreachable by the absences recorded in §2.

## 6. Typed outcomes the consumer must preserve

Never collapse these into confidence or zero:

- **result**: `EXACT_SUPPORTED` · `EXACT_UNRESOLVED_PROXY_AVAILABLE` · `UNRESOLVED` · `VALID_EMPTY` · `NONCOMPARABLE` · `FAIL_CLOSED`
- **evidence**: `SUPPORTED` · `UNDERPOWERED` · `VALID_EMPTY` · `UNRESOLVED` · `NONCOMPARABLE` · `UNAVAILABLE`
- **P06 decision**: 12-state precedence, 11 nonpositive; public states `ADMITTED_FOR_EXACT_STRUCTURAL_USE` · `MISSING_AUTHORITY` · `ADMISSION_DENIED` · `DEFERRED` · `NONCOMPARABLE` · `OUT_OF_SCOPE` · `INSUFFICIENT_EVIDENCE` · `UNRESOLVED` · `INTEGRITY_FAILURE`
- **objective-consumer**: `SUPPORTED_OBJECTIVE_RESULT` · `PARTIAL_OBJECTIVE_RESULT` · `REFUSED_REQUIRED_OBJECTIVE_EVIDENCE` · `ALL_UNAVAILABLE__NOT_POSITIVE_COMPLETION`

`ALL_UNAVAILABLE__NOT_POSITIVE_COMPLETION` exists specifically so an unimplemented gate cannot masquerade as a scoped success — HQD-125 §12's requirement.

## 7. Acceptance tests any adopted F8 contract must pass

Executable, not aspirational:

1. **Firewall.** No input yields actor state, biography or personality; refusal is structural.
2. **Population-fact.** A population field cannot be read as a positioned-subject attribute without a conditioning basis and positive comparability authority.
3. **Geometry-inertness.** No world input changes returned geometry except via a new upstream evidence slice at a new retained-conditioner grain.
4. **No-renormalization.** Any renormalization request raises.
5. **Ceiling monotonicity.** No ceiling upgrade path exists.
6. **Uncertainty preservation.** `UNRESOLVED`/`NONCOMPARABILITY` input cannot yield a confident output.
7. **Cross-source refusal.** Any conditioner or proxy crossing source universe or release yields `FAIL_CLOSED`.
8. **Walkback monotonicity.** A non-decreasing walkback ladder raises.
9. **Currentness fail-closed.** `UNKNOWN_CURRENTNESS` never defaults to current.
10. **Replay.** Every result reconstructs from its declared replay determinants.
11. **Adapter discipline.** No admitted adapter introduces a new semantic operation.

## 8. What this contract does not do

- It does not name a new authority **form**. Audit C17 and W16 both hold the forms closed while instances/proof remain; HQD-125 §15 forbids reopening on missing occupancy alone.
- It does not invent a pressure/hegemony/coupling object.
- It does not resolve H-A, H-B or H-C, and does not guess their answers.
- It does not import the C1 chain from side branches.
- It does not assert F8 completeness. HQD-125: `DDM_EMERGENT_FUNCTIONAL_REALIZATION_NOT_YET_PROVED_END_TO_END` remains true.