# 00 — RETURN: HQ203 H-D mature-world F8 / service-operation contract audit R1

**Terminal:** `HQ203_HD_MATURE_WORLD_F8_SERVICE_RETURNED__HQ_ADJUDICATION_REQUIRED`

| field | value |
|---|---|
| branch | `agent/rabochii-pyat-hq203-hd-r1` |
| commission tip | `de129fea321981a8b47c3239f3858a0b6a535e46` |
| documentary base | `15018a303078cbcd867b08d39ed6b66e14d325fb` |
| control tip examined | `3760ba31761cd6e27e978c31749161feced1a47a` |
| primary audit | `b3ea471a3771113bf408a4e434a4b480b26d5856` |
| checkout mode | SPARSE (as prepared by HQ bootstrap) |
| disposition | **`MATURE_WORLD_F8_PARTIAL__NAMED_TRANSFORMATION_AUTHORITIES_UNBOUND`** |

---

## 1. Load-bearing finding

**F8 does not transform possibility geometry. It selects among pre-materialized geometries.**

```python
MODEL_ALGORITHM_ID = "EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION"
```

Geometry arrives on `PossibilitySliceEvidence.geometry` from an upstream producer and is chosen by exact `(source_universe_ref, release_ref, target_ref, retained_conditioner_ids)` match, or by a governed strictly-decreasing specificity walkback confined to the same source and release.

**Therefore: `GEOMETRY_TRANSFORMER` and `DISTRIBUTION_TRANSFORMER` are unavailable at F8 to every world input family.** Not deferred — at this grain no code path permits it. A world product changes what F8 returns only by causing an upstream producer to materialize a different evidence slice at a different retained-conditioner grain.

This is the answer to the commission's instruction not to reduce the question to transport. Transport asks how bytes move. The real question is which licensed semantic operation a world product may perform, and at F8 the licensed set is exactly:

> { select an exact pre-materialized slice · reduce specificity under a named positive proxy authority · refuse }

## 2. Classification summary

15 candidate input families classified across the 10-class taxonomy (`02_WORLD_INPUT_OPERATION_MATRIX.json`).

- **CONDITIONER** (4): exact source-local fact; joint fact; branch/configuration; structural position/role — the last *only* via exact comparator.
- **ELIGIBILITY_FILTER** (2): uncertainty/noncomparability; current-vs-historical validity.
- **CONTEXT_ONLY** (3): opportunity/constraint; higher-order topology; pressure/counterpressure.
- **REFUSAL_ONLY** (1): cross-source relations — `cross_source_proxy = FORBIDDEN_IN_V1`.
- **NOT_ADMITTED** (4): mediation/route; objective consequence; temporal products; whole-world container.
- **SOURCE_SELECTOR** (1): service-source applicability — **UNBOUND**, no adopted authority.
- **GEOMETRY_TRANSFORMER / DISTRIBUTION_TRANSFORMER** (0): unavailable at this grain.
- **CONTEXT_ONLY as sole residue** (1): cross-source coexistence in source-indexed mode.

## 3. Named unbound transformation authorities

Full list in `03_TRANSFORMATION_AUTHORITY_MATRIX.json`; summary:

| operation | state | debt class |
|---|---|---|
| SOURCE_SELECTION | no adopted authority; validation-only today | authority |
| SOURCE_COMPOSITION | forbidden in v1 (deliberate) | authority form |
| TEMPORAL products as conditioners | no current producer | authority instance |
| PRESSURE as conditioner | unresolved (H-B) | authority instance |
| CONDITIONING per scope | form closed, instances unbound | authority instance |
| Comparator instances | form closed, one field adopted | authority instance |
| Joint/multi-arity producer | absent from governed lineage | implementation |

**No missing authority FORM is proved.** Audit C17 and W16 both record forms closed while instances/proof remain.

## 4. Material inventory conflict — HQ adjudication required

The commission names three modules "at minimum inspect". **None exists** at the commission HEAD, the documentary base, the audit tip, or the control tip:

| module | last touched | in governed lineage? |
|---|---|---|
| `pre553_analytical_composition.py` | `bc661188b5` 2026-09-30 | no |
| `pre553_empirical_possibility_provider.py` | `e3bcbbb4fa` 2026-09-30 | no |
| `pre553_analytical_state_and_route.py` | `4f5555459e` 2026-10-01 | no |

Never deleted — every commit in their path history is `A` or `M`. They survive on ~20 non-ancestor side branches. `rawlsing_next` counts 307 files at both the control tip and the commission HEAD, ruling out a partial listing.

This puts pressure on audit claims such as MATRIX C18 ("C1 producer and consumer accepted; N10E scalar adapter narrower") and REPORT §236 ("accepted producer/consumer chain are sufficiently constituted at their declared grain") — none verifiable at the audit's own tip.

**Consequence:** the HQ168 grain premise H-D was told to respect could be neither confirmed nor refuted. The scalar source-local exact-lookup path is the only current F8 producer.

**No mutation was performed.** Absence was established read-only via `ls-tree` and `merge-base --is-ancestor`. Importing side-branch history is a re-commission decision.

## 5. Persistent container

`OPTIONAL__NOT_REQUIRED_AT_CURRENT_PROVEN_GRAIN`. F8 evaluates from evidence tuples and never reads a world aggregate; OC05 is `NOT_YET_APPLICABLE` with the reason "no universal terminal may be invented"; and the only two operations a container would enable — cross-source composition and renormalization — are forbidden by binding law, not merely unimplemented. Must be retested if H-A, H-C or an `AUTHORIZED_COMPOSITE` estimand is adopted.

## 6. Preserved distinctions — all six verified in current code

| distinction | enforcement |
|---|---|
| `POPULATION_FACT != POSITIONED_SUBJECT_POSSIBILITY` | `ClaimCeiling` has no positioned-subject member |
| `POSITIONED_SUBJECT_POSSIBILITY != INDIVIDUAL_PREDICTION` | `EPISTEMIC_CEILING` + mandatory `purpose == EMPIRICAL_POSSIBILITY_ONLY` |
| `OBJECTIVE_WORLD_TIME != ACTOR_MEMORY` | `ACTOR_MEMORY` is a forbidden interpretation marker; no temporal admission exists |
| `STRUCTURAL_PRESSURE != INDIVIDUAL_DESIRE` | actor markers rejected at rule construction |
| `FIELD_TRAJECTORY != PERSON_TRAJECTORY` | no temporal conditioner; walkback is specificity-only within one source/release |
| `CURRENT_FACT != HISTORICAL_FACT` | lifecycle selection/validity states orthogonal; fail-closed on unknown currentness |

## 7. Lanes not guessed

H-A, H-B and H-C are recorded as explicit dependencies with conditional rules under either resolution (`07_CONDITIONAL_DEPENDENCY_MAP.json`). Their answers are not pre-empted.

## 8. Outputs

| file | content |
|---|---|
| `00_RETURN.md` | this return |
| `01_CURRENT_F8_CHAIN_CENSUS.json` | current chain, present/absent components, C1 conflict |
| `02_WORLD_INPUT_OPERATION_MATRIX.json` | 15 families × 10-class taxonomy |
| `03_TRANSFORMATION_AUTHORITY_MATRIX.json` | 9 operations with exact required authority and refusal |
| `04_C1_CONSUMER_GRAIN_AND_ADAPTER_BOUNDARY.md` | HQ168 grain, adapter boundary rule |
| `05_NEGATIVE_AND_REFUSAL_LAW.json` | 25 refusal families, enforcement evidence |
| `06_PERSISTENT_CONTAINER_NECESSITY_TEST.json` | 6-part test → OPTIONAL |
| `07_CONDITIONAL_DEPENDENCY_MAP.json` | H-A/H-B/H-C + intrinsic C1 dependency |
| `08_MATURE_WORLD_F8_SERVICE_CONTRACT_CANDIDATE.md` | candidate contract, unadopted |
| `09_FINAL_DISPOSITION.json` | disposition + rejected alternatives |

## 9. Boundaries observed

No production mutation. No raw-source or survey access. No locator discovery, no warrant issuance. Sparse scope unchanged. All historical evidence read via exact git object operations against the shared canonical store. No network fetch performed by this worker.

## 10. Requested of HQ

1. **Adjudicate the C1 inventory conflict** — are the C1 modules current? If yes, the governing lineage is missing them; if no, several terminal-audit matrix rows overstate current capability.
2. **Note the disposition** is PARTIAL with named unbound authorities. The mature-world contract is not determinate (audit W17 remains `TERMINAL_CONSUMER_CONTRACT_UNDERDEFINED`), and architecture reopen is not warranted under HQD-125 §15.
3. **Cross-lane:** H-C owns `SOURCE_SELECTION`, the only operation here with no adopted authority at all.

`HQ203_HD_MATURE_WORLD_F8_SERVICE_RETURNED__HQ_ADJUDICATION_REQUIRED`