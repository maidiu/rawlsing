# D1–D5/D9 reliable estimand, denominator and survey-weight decision court

**Grade:** independent S0–S1 methodological qualification; no original-source, current weight/design, model-use or scientific issuer authorization. Protected code cut `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`. Every equation below is a conditional *specification*, not an empirical measurement.

## 1. Decision keys and sampling objects

Let `s` be **one exact source edition**, restricted to a qualified country / survey wave / questionnaire form / administration route and analysis population. Let `r` index **unique eligible sampled persons**, not rows, household members accidentally multiplied, question occurrences, or joined identities from different waves. Let `D` be an original demographic/position field and `A,B,C` three lawfully coadministered, retained response fields.

Define:

- `U_s`: actual eligible respondent universe, with eligible sampling/consent/source use, and a stable respondent namespace.
- `R_Q(r)`: exact source-owned exposure/route/applicability law for each question `Q`, distinguishing asked/eligible from not asked, routing skips, DK, refusal and invalid responses.
- `E_T(r)`: intersection of the required target-item routing and unit eligibility for target set `T`; a *complete-case* condition is applied only under a predeclared missing policy.
- `G(r)`: an exact predicate on `D` or additional respondent attributes, not a proxy post-hoc synonym.
- `I_T(r,t)`: one if the source-declared tuple `T` resolves exactly to target cell `t`, else zero if unresolved; do not silently treat unresolved as any observed zero category.
- `w_r`: one permitted, nonnegative, exactly assigned design/analysis weight per respondent and relevant edition/population/risk set. Weight absence is **HELD**, not `w=1` for a population claim.

**Two competing denominators require an explicit issuer choice.** `R_G={r∈U_s:E_T(r),G(r)}` is the condition-selected *eligible* risk set; `R_G^{obs}={r∈R_G:T resolved}` is the response-complete set. A requested probability conditional on a response requires either a justified complete-case/missingness policy with denominator `|R_G^{obs}|`, or a stated eligible-exposure denominator `|R_G|` with retained missing mass. These are **different estimands**. Never present the latter's observed-cell mass, which may sum to less than one, as a normalized response distribution.

### Current implementation precision

In `rawlsing_next/_pre553_query_eval.py:371–450`, routing defines risk membership, the condition predicate selects `denominator_members`, and raw denominator equals their count at :452–455; full target resolution is only checked afterward. When any denominator member lacks a complete target cell, the state is `UNRESOLVED` (:472–474), not a false `SUPPORTED` subprobability. `SUPPORTED` requires `raw_resolved == raw_denominator`. This is a useful native safeguard **if** upstream source routing and response-state rules are competent.

## 2. D1–D3: which inferential units exist?

Before any estimate, the exact source issuer must distinguish:

1. dataset/release filename vs immutable content hash, original sample/wave and country subset, release/revision/fieldwork dates, physical host and retention/read purpose;
2. questionnaire wording and language, value labels/codes/polarity, administered occurrence, questionnaire form/ballot, mode, route/skip exposure, respondent comprehension/answer multiplicity, and whether two purported items were *ever* jointly asked;
3. person vs household vs proxy respondents; unique person key after household roster and duplicate/repeat rules; panel linkage only on certified longitudinal identifiers; all other wave IDs are source-local; D missing/unknown separate from target missing;
4. source-specific target population and inclusion probabilities, clusters/PSUs, strata, calibration, finite-population correction, and any officially required weight;
5. operation- and derivative-specific permission for exact original use, storage, derived counts, onward consumers, and release; *public availability does not constitute the recorded project's current grant*.

A variable appearing in an all-wave harmonized file does not prove that a local respondent saw it. Without direct original form, physical-occurrence and route proof, code must label coexposure **UNKNOWN**, not zero.

## 3. F1/F2/F4 raw, design-weighted, and two-way conditionals

For `T=(A,B,C)` with a source-approved complete-response risk set and demographic condition `D=d`:

\[
n(t,d)=\sum_{r∈U_s}1\{E_T(r),D(r)=d,T(r)=t\}, \qquad n(d)=\sum_t n(t,d).
\]

**F1 marginal:** `p_raw(A=a)=n(A=a)/n(A observed and eligible)`, with an explicit alternative eligible-exposure denominator only if separately named and its missing fraction published.

**F2 forward:** `p_raw(A=a | D=d)=n(A=a,D=d)/n(D=d)`; **F2 inverse:** `p_raw(D=d | A=a)=n(A=a,D=d)/n(A=a)`. They use the **same eligible and genuinely coexposed source cohort**, but different condition-selected denominators. For an illustrative (NOT source-observed) table with rows `D=0,1` and columns `A=0,1`, `[[2,1],[3,4]]`: forward `P(A=1|D=1)=4/7`; inverse `P(D=1|A=1)=4/5`. A swapped label cannot reproduce both.

**F4 joint:** `p_raw(A=a,B=b,C=c|D=d)=n(a,b,c,d)/n(d)`, where all three responses are **from the same respondent and same valid original route**. The declared domain contains every valid tuple, including `n=0` cells, and a joint zero cannot be inferred from missing or not asked. Pairwise `P(A,B)`, `P(A,C)`, `P(B,C)` do **not** identify the 3-way table.

For a source-authorized, strictly positive denominator and applicable design weight:

\[
\hat p_w(t|d)=\frac{\sum_{r∈U_s}w_r\,1\{E_T(r),D(r)=d,T(r)=t\}}
{\sum_{r∈U_s}w_r\,1\{E_T(r),D(r)=d\}}.
\]

If `Σw=0`, unknown weight basis, incompatible weights, missing design or violated source mandate, return an explicit weighted-estimand **UNAVAILABLE/HELD**, not raw fallback. Distinguish descriptive finite-sample `n/N`, weighted survey estimator of a **defined target population**, and a model-based prediction to another time/position/population.

**Current ABI limit:** `_pre553_query_eval.py:275–310,313–450,617–650` does carry governed `GOVERNED_WEIGHTED` supports through `EmpiricalFact`, but `pre553_analytical_composition.py:839–924` emits `weighted_probability_exact_fraction_if_authorized=None` and `weight_design_estimand_context=None`. Therefore the current N10E slice is an exact raw fraction (where fully resolved), **not** a verified weighted population probability. The weighted estimator and design context need a distinct source/science owner plus explicit current consumer implementation/review, not merely enabling a weight flag.

## 4. D4 statistical design, estimand, uncertainty and transport

| Choice | When legitimate | Output/refusal and material risk |
| --- | --- | --- |
| **RAW finite-sample descriptive** | Explicitly permitted and correct question/respondent/risk selection; named *sample*, not nationally representative population | Exact integer counts/fractions, complete domains, missing and sparse support; no population margin-of-error claim |
| **Survey-weighted descriptive population** | Competent design owner identifies the **correct** person/household/country/wave/pooled-scope weight, scale, calibration and target frame | Weight sums and ratio estimator; target meaning; effective n diagnostic; CI only with valid strata/PSU/replicate/FPC rules |
| **Design-based uncertainty** | Exact strata, cluster/PSU, weight design, lonely-PSU and variance method disclosed; sufficient support or appropriate replicate weights | Taylor linearization, replicate/bootstrap/jackknife/BRR per source protocol; report SE/CI/design df and small-cell caveat; otherwise `UNCERTAINTY_UNQUANTIFIED` |
| **Model-assisted/predictive** | Explicit selected model contract, calibration/validation and target-population/transport owner | Model estimate labeled PROXY/MODELLED, uncertainty interval and out-of-support/refusal; never observed frequency |
| **Cross-survey/year transport** | Independently justified harmonization, comparable administrations, distinct population accounting and permission | Separate source-indexed outputs by default; no pooling of file rows or same-number respondent IDs |

`rawlsing_next/pre553_effective_n.py::compute_effective_n:454` computes a scope-controlled Kish-like effective n for qualified weighted facts, not a surrogate for survey-cluster variance. The GSS official guidance, for example, recommends design weights and identifies edition-specific options; which one is correct for **these retained project files** is unissued. A public manual is guidance, not a signature for the current operation.

Uncertainty should accompany proportions and rare cells with explicit effective support and refusal, but *no arbitrarily selected confidence interval* counts as source-qualified proof. Small cells may be suppressed according to source privacy terms even where computation is permitted.

## 5. D5 finite K/J/D and minority/branch court

- **K:** maximum number of independently authorized conditioner atoms, not every potential demographic combination. Include named values, contradictions, rare groups and coverage anti-join.
- **J:** maximum number of jointly *administered* target item components (pilot requires J=3), not number of independently queryable marginals. I03 permits arbitrary declared arity structurally; source item rules and finite domain/budget impose the actual maximum.
- **D:** recursion depth/branch ancestry with a source-authorized stop law, explicitly distinguishing exhaustive finite I05 frontier from adaptive `UNKNOWN_UNVISITED`. Proposed pilot D≤1, no claim this is the system's owner-issued limit.
- **F3:** define minority by **observed joint/conditional support under a frozen rule**; preserve nonmodal cells and XOR counterpatterns. Ranking may prioritize analysis but cannot silently delete expected or negative candidate IDs. No significance or mechanism inference without a separate scientific rule.
- **Zero vs negative:** an admissible unobserved full-domain cell with positive risk denominator is observed zero. A zero selected denominator is `ZERO_SUPPORT`; absence of coexposure is `ZERO_OVERLAP` or an issuer-qualified `NOT_APPLICABLE` when known. Missing respondent records or unvisited branches remain `UNKNOWN`.

`rawlsing_next/pre553_discovery_exact.py:617–812` has actual K/J frontier enforcement and a `JOINT_DEPENDENCE`, `REVERSAL_GRID`, XOR exact plan. It is not a licence to enumerate arbitrarily large/all-original combinations. The independent source owner must state which finite candidates are truly in Epre and which are inapplicable/blocked/held.

## 6. D9 exact vs proxy, cross-position and later model use

Three incompatible products must be permanently distinguishable:

1. **Exact descriptive conditional:** observed respondent cooccurrence with exact release, risk, value, numerator, denominator, measure and negative states; no causal arrow.
2. **Proxy/partial-pooling prediction:** an explicitly selected statistical model extrapolating to sparse/unmeasured configurations, including priors, training/validation splits, transport domain, calibration, uncertainty and anti-leakage; never identical to original observed `EmpiricalFact`.
3. **Person/dyad/actor generation:** separate causal history and encounter/partner-selection mechanism, with position/time/availability/rights. `P(D|A)` from an independent cross-sectional survey is not evidence that an actor with attitude A has a particular mother/partner, or that two independent respondents meet.

No `D9` permission exists merely because the current N10E reader accepts a correct empirical `ConditionValueBindingWitness`. Exact source-supported neighboring subgroups are not a universal law for all positions/countries/times; high-dimensional empty combinations should abstain/model-qualify, not manufacture a social type.

## 7. Decision order and smallest falsifiers

1. **D1 rights before bytes:** exact recorded file/edition hash + licence + user/account/host/purpose/derived-output grant; absence ⇒ HELD.
2. **D2 item/coexposure:** original national form, wave, route, occurrences, response codes; absence ⇒ no F4 or F2 denominator claim.
3. **D3 respondent:** one true sample-unit key, duplicates/household/secondary respondents, complete-case/skip law; fail if joint tuples arise from Cartesian joins.
4. **D4 measure:** source owner decides raw sample vs authorized weighted target and SE; weighted support does not equal weighted N10E geometry at current cut.
5. **D5 frontier:** independently frozen expected candidates K/J/D and negative/unvisited ledger; compare expected↔executed by exact operation/ref.
6. **D9 consumer:** source/model/target-purpose owner explicitly permits each direct, inverse, generalized or actor-facing use; no implicit elevation.

**Methodology disposition:** RAW pilot is the lowest possible scientific complexity *only if RAW itself is permitted and explicitly labeled as sample-descriptive*. Weighted population statements require additional D4 issuance and currently a real N10E consumer gap. Any unissued required field leaves the operation **HELD**; it does not create authority to infer a favorable default.
