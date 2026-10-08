# PYAT HQ250 S02 — Scientific source binding for SRC02 Q86C — R1

**Status:** `SOURCE_DOCUMENTARY_PLAUSIBLE__TRIPLE_PRODUCT_AND_PERMISSION_UNVERIFIED`. **Role:** independently commissioned Browser/GitHub documentary investigation, not source execution, semantic adoption, measurement certification, or a new source warrant. **Frozen worker parent:** `1f70126ebdd62a44bc54f47e0ae32231a41b2a54`; later sealed HQ250 at control `f56bfa9afe3373126ceaef4fabf0ec81f09dbc59`. **Library:** NO. **Raw surveys opened:** NO.

## 1. Decision and precise scientific question

Consider SRC02 Afrobarometer Round 5 respondent attitudes:
- **Q86A, target Y:** whether a person **born in the respondent's country** to **one citizen/national and one non-citizen parent** has a right to citizenship.
- **Q86B, first conditioner A:** whether a person **born in the country** to **two non-citizen parents** has that right.
- **Q86C, proposed additional conditioner B:** whether the **wife of a citizen/national man**, despite being **born outside the country**, has that right.

The parent Q86 battery frames citizenship in terms of the right to a passport and to vote in national elections if at least 18. The questions are **respondents' opinions about hypothetical others**. Q86C is neither the respondent's sex, marital status or migrant status, nor a source/receiving structural position. Its gendered marriage criterion gives it a distinct proposition; it must not be treated as an interchangeable indicator of Q86A/Q86B or a unidimensional citizenship scale. A Q86B→Q86A co-occurrence is not causality, and neither relationship supplies V555 route-position credentials.

Source: official Afrobarometer **Merged Round 5 Codebook**, `Q86A/Q86B/Q86C`, PDF printed page 53 / PDF page index 52:
https://www.afrobarometer.org/wp-content/uploads/2022/02/merged_r5_codebook_2.pdf
Official resource: https://www.afrobarometer.org/survey-resource/merged-round-5-codebook-34-countries-2011-2013-last-update-july-2015/

## 2. Source-native states, exclusions, and distinct evidence ceilings

The merged codebook lists the Q86A/B/C substantive values **0 No** and **1 Yes**, with **9 Don't know**, **997 Not asked**, **998 Refused to answer**, and **-1 Missing** in its value-label/administrative declarations. Note the *presentation distinction*: `997` appears in the source value-label list even where the displayed “Values” listing does not separately enumerate it. Do not infer observed counts or absence from that typography. Preserve physical/raw value, typed response state and **independent exposure/routing** separately. Numeric codes identify response categories, not an ordinal/metric continuum. Missingness is not one homogeneous analytic null.

For Q86A, Q86B and Q86C the merged codebook identifies **ALG, EGY, MRC, SUD, TUN** as `Not asked`. This is official **general source documentation**, not a proof of each respondent's Q86C exposure, a full country-variant audit, or the accepted 11-country GT2 selection.

The existing adopted **A/B** R5 code at `rawlsing_next/wave1_r5_q86_c11_projection.py`, Git blob `d96933180d310b4078f23127bb5a97a3677728d1`, fixes:
- Frozen `Data/Afro Barometer Round 5.sav` SHA-256 `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`; source row count **51,587**.
- Existing A/B respondent key `country_native|respno`, source row ordinal and hashed respondent-local identity, distinct Q86A/B exposure events, and `COUNTRY_ALPHA3` routing coordinate.
- Existing **exact two-question common-coexposure** subset: **19,210**, risk `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`, member SHA-256 `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`.
- Existing *A/B* common-risk countries **BFO, BOT, CVE, KEN, LES, MAU, MLW, MOZ, NAM, SAF, UGA** — 11 countries, not “all countries except the five codebook exclusions.”
- Critically, the source module `Q86` mapping has **only Q86A and Q86B**; `question_ref()`, `domain_ref()` and related constructors reject other variables with `only Q86A/Q86B are frozen`; `R5Q86GovernedRow` carries A/B values and exposures but no Q86C. Its governed source/routing/target-use permissions are explicitly `Q86A_Q86B`-limited. Tests in `rawlsing_next/tests/test_wave1_r5_q86_c11_projection.py` enforce independent `EXPOSED__PROVED` even when a substantive response is present. This is positive evidence of a **current boundary**, not proof that source Q86C values are intrinsically unavailable.

Source references:
- https://github.com/maidiu/rawlsing/blob/1f70126ebdd62a44bc54f47e0ae32231a41b2a54/rawlsing_next/wave1_r5_q86_c11_projection.py
- https://github.com/maidiu/rawlsing/blob/1f70126ebdd62a44bc54f47e0ae32231a41b2a54/rawlsing_next/tests/test_wave1_r5_q86_c11_projection.py
- https://github.com/maidiu/rawlsing/blob/1f70126ebdd62a44bc54f47e0ae32231a41b2a54/WORKER_RETURNS/PYAT-HQ221-C5-GT2-STRUCTURAL-POSITIVE-REALIZATION-R1/01_RETAINED_EMPIRICAL_INPUT_BINDING.json
- [HQ250 sealed decision](https://github.com/maidiu/rawlsing/blob/f56bfa9afe3373126ceaef4fabf0ec81f09dbc59/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ250_ASTRA_FINAL_D1_D3_INTAKE_AND_SCOPED_SERVICE_FRONTIER_R1.md)

**The 19,210-person A/B cohort CANNOT be silently certified as the A/B/C cohort.** Any new operation must demonstrate same-person linkage and independent Q86C exposure across a **new exact triple risk-set member list and hash**. If HQ restricts the new operation to the accepted A/B cohort, its intersection count is at most 19,210, but may be lower; if HQ separately warrants a broader source universe, it becomes a differently scoped claim and must not inherit GT2 pair semantics.

## 3. Sampling, universes, design and weights

The Round 5 merged codebook documents **`withinwt`** (within-country unequal selection weighting) and **`combinwt`** (multi-country weighting that makes country samples contribute comparably to cross-country summaries). These are scientifically distinct estimands and require a chosen design/analysis policy. Neither codebook availability nor the variable name validates each weight or a particular variance estimator in the frozen Rawlsing release. The accepted GT2 product is `RAW`, `SINGLE_UNIVERSE` and explicitly **unweighted** (`weighted_support_authorized=false`). There is no authorization to silently change `q` into a population-weighted proportion or to produce pseudo-precision. Exact country/national sample frame, clustering/stratification, missingness and weight availability must be confirmed for any separately warranted weighted estimate; without that, only the selected properly authorized **raw count** geometry may be produced.

Scientific feasibility is **highly plausible** in questionnaire design: A/B/C share one Round 5 citizenship battery and a documented administrative state family. **Measured respondent compatibility, source-specific Q86C binding, coverage, distribution and triple exposure remain unverified.** Official public codebooks cannot certify that the frozen source SHA and its field/value variants match the cited public release.

## 4. Existing empirical positive and accepted consumer ceiling

The retained GT2 A/B pair has an actual `EmpiricalFact` SHA-256 `540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46`, `EmpiricalQuerySpec` `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0`, predicate `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3` and replay `c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f`. It is 36 exact joint cells from 19,210 common-risk respondents, with nonmodal states, denominators, missingness and lineages retained. It has a genuine actor-independent Field Forge bounded conditional support profile and adopted V554 SIG-004→V557/V558 **CONTEXT-only** publication (`RESOLUTION_COMPLETE`). Existing context is *not* an as-of N9/OC05 world, probability-pressure transformation or a Q86C triple product.

The adopted HQ225/HQ227 exact V555 terminal `NOT_APPLICABLE_TO_GT2_SIG004` is based on Q86A and Q86B being **attitude/disposition** questions and no lawful source/receiver structural positions; adding Q86C as a third attitude does not repeal this terminal or imply a new causal/mediating route.

Evidence: https://github.com/maidiu/rawlsing/blob/1f70126ebdd62a44bc54f47e0ae32231a41b2a54/WORKER_RETURNS/PYAT-HQ225-V555-GT2-POSITION-BINDING-AUTHORITY-R1/00_RETURN.md and https://github.com/maidiu/rawlsing/blob/1f70126ebdd62a44bc54f47e0ae32231a41b2a54/PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ227_GT2_TERMINALITY_ADOPTED_F7_N10E_REPAIR_N6_CONTEXT_WAVE_R1.md.

## 5. What a genuine ordered triple must demonstrate

Target `Y=Q86A`, conditioner `A=Q86B`, additional conditioner `B=Q86C`. The symbolic progression `q(Y|A)` to `q(Y|A,B)` is a *demand*, **not** newly authorized probability syntax or numerical forecast.

For a separately approved **same-respondent**, `RAW`, triple-co-exposure risk `R_ABC`:
1. An exact source-native `Q86C` question implementation reference, label/response-state domain authority, country/wording/skip/routing authority, per-respondent independent exposure evidence, source release/custody, and new source-native C11/empirical response product.
2. A respondent-key- and hash-aligned **three-component ordered joint** and operation/predicate authority. If official six-state domain and carrier semantics are truly certified for C too, full native topology is **6×6×6 = 216 explicitly typed cells**, including zeros and administrative states, not only the 2×2×2 substantive slice. This is a *candidate shape*, **not** actual observed cell claims.
3. Two genuinely distinct fact/query/predicate and consumer binding identities for `q(Q86A|Q86B)` and `q(Q86A|Q86B,Q86C)` **on the same defensible restricted universe** (or an explicit denominator-shift accounting). Marginalize triple cells over C and recover the *recomputed two-variable distribution on R_ABC*. It need NOT equal the originally accepted A/B table on 19,210 if R_ABC is a proper subset.
4. Preserve exact A/B/C component order, all positive/zero joint support, nonresponse, minority/counterpatterns, uncertain/underpowered/valid-empty cases, any discovery/recursive ancestry actually produced, source/admission/release/currentness identities and replay.
5. Independent falsification of synthetic overlap, independently multiplied marginals, missing Q86C lineage, mismatched country or exposure, hidden denominator changes, missing administrative states, and erroneous source-absence→`N/A`, `VALID_EMPTY` or empirical null.

**Current algorithmic route exists at a different grain.** `rawlsing_next/pre553_analytical_composition.py` `compose_positioned_subject_possibility` (blob `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`, lines 1008–1138) consumes `_all_bindings(consumer_query)`, accepted query/predicate/release, `ConditionValueBindingWitness`, exact I03 output and optionally discovery/recursive evidence; calls F8 only on genuinely `SUPPORTED` fact and verifies exact risk-set, measure, source universe and predicate identity. `rawlsing_next/pre553_empirical_possibility_provider.py` `_single_binding` (blob `23167aa25291fb148b1e3cf210ac33fe7769b783`, lines 479–487) rejects >1 binding; it must not be treated as the required path. `pre553_service_f8_source_scope_binding.py` (blob `4ba00b8ecf73f70ad0f6481e255fd0117744418a`, lines 894–961) *authenticates* source scope and passes supplied slices unchanged, not an independent producer. Code presence/earlier source-free tests are not Q86C triple runtime/consumer proof.

Refs:
- https://github.com/maidiu/rawlsing/blob/1f70126ebdd62a44bc54f47e0ae32231a41b2a54/rawlsing_next/pre553_analytical_composition.py
- https://github.com/maidiu/rawlsing/blob/1f70126ebdd62a44bc54f47e0ae32231a41b2a54/rawlsing_next/pre553_empirical_possibility_provider.py
- https://github.com/maidiu/rawlsing/blob/1f70126ebdd62a44bc54f47e0ae32231a41b2a54/rawlsing_next/pre553_service_f8_source_scope_binding.py

## 6. Negative and alternative interpretations

- The limited exact repository check found no **accepted respondent-backed Q86A/B/C triple**, Q86C source-specific authority, member hash, or exact current consumer use. GitHub default code search has archival Q86C mentions in historical source-code/structure files, but they are **not** an independently executed triple; these hits do not establish global nonexistence and are not warrants. An independently surfaced exact triple product with valid custody would **falsify** this bounded retrieval-negative.
- A published survey battery does not prove complete common exposure in the accepted 11-country A/B cohort; a source-native Q86C record could also be missing, unrouted or have country-specific wording. Without genuine source-level verification, **do not** declare it eligible or source-intrinsic not-applicable.
- The valid first response may be empirically weak, and the added conditioner may leave the numerical distribution unchanged; these are **acceptable produced measurements**, not excuses to omit a triple joint or authorize a causal interpretation.
- The complete-source question of weights must stay separate from source-native empirical response. A weighted/variance product needs an additional operation and design warrant, not an after-the-fact reinterpretation of integer counts.

## 7. Final scientific finding / independent disproof

**`Q86C_CANDIDATE_SCIENTIFICALLY_PLAUSIBLE__CURRENT_TRIPLE_EMPIRICAL_INPUT_UNVERIFIED`**.

The first falsifiable missing edge is **an authenticated SRC02 Q86C respondent response + independent exposure/routing + aligned triple risk-set source product and claim/operation authority**, not a new generic three-way mathematical engine. Owner: **future HQ scoped source/measurement/routing/operation authority** with source producer only after separately approved warrant; C1→F8 consumer selection remains an independent S01/HQ decision. Any inspected exact authorized Q86C responder, exposure and triple-production package would disprove the present bounded source-product gap. Any source document establishing Q86C never exists in the fixed source release, or lacks valid common exposure at the chosen grain, would defeat the chosen source candidate rather than prove an engine failure.

**STOP:** No source opened, no new warrant issued, no production/mapping/HQ/actor mutation. Return for independent review.
