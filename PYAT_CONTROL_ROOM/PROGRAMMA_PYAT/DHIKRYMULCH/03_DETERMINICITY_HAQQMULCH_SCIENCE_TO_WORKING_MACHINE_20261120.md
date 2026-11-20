# DETERMINICITY — HAQQMULCH of one scientific and computational problem
## From a misleading historical “most deterministic variable” to a workable country-conditioned empirical inquiry

**20 November 2026 · subject-specific analysis/design candidate · beside [DHIKRYMULCH](00_DHIKRYMULCH.md), [what PYAT actually is](01_WHAT_PYAT_PRESENTLY_IS.md), and [smallest build-first delta](02_TARGET_TO_PRESENT_DELTA.md).**

**THIS IS NOT THE GENERAL HAQQMULCH PRIMER.** The general resource and historical-function discipline belongs to [CROSS-PROGRAMMA/05 HAQQMULCH](https://github.com/maidiu/rawlsing/pull/1202), the general primer stacked on [PR #1195](https://github.com/maidiu/rawlsing/pull/1195), and is intentionally **not tied to this statistical problem**. This document owns the actual *question of determinicity* at the present PYAT stage, with real historical source code, an affordable proposed estimator/inquiry and the next existing-owner implementation. Do not reissue its rules to unrelated workers.

**Controlling outcome:** commitments 1, 2 and 3 are to **build PYAT**. Preserve scientific truth and the real powers needed by DHIKRYMULCH and SOROK while accepting that finite time, available computer power, wall time, RAM, staging bytes and durable storage force **selective, adaptive resolution**. A production system using honest lower-resolution conditional knowledge is preferable to a permanently unfinished high-dimensional omniscient model. A false empirical fact is not a permissible cost saving.

**Evidence class:** GitHub-inspected historical and modern code; scientific methods publicly researched; worked arithmetic **synthetic**; prospective design and decision; **10/10 sourcefree local Python unittest PASS** on two byte-identical-to-GitHub committed candidate files (details below). **No source-backed PYAT production execution, independent G5 or protected receiving.** All code refs must be refreshed by the owner before implementation.

---

## 1. The question we are *actually* trying to answer

For a source-qualified historical population configuration **D**, a governed measured response **Y**, and a finite set of genuinely measured candidate predictors **X**, determine:

**Which X most usefully, reliably and *incrementally* differentiates the observed distribution of Y *inside D*; what answering alternatives remain after the split; how does the answer change in a narrower legitimate configuration; and how many computer resources are justified to know more?**

This is not “which demography determines a human being.” It is not a global table of socioeconomic traits ordered by importance. And it is **not** simply “the variable with the highest mutual information in a pooled survey.” It is a conditional empirical question at an explicit source/world grain, whose value is to make grounded demographic configurations and minority/repertoire possibilities available to later selection.

At the root, estimate `P(Y | S, wave, country, eligible population)` at the **right evidence grade**. Then for supported source-measured X, estimate `P(Y | D, X=x)` and the change from the baseline, preserving the full response distribution. After selecting one useful refinement, ask whether another X adds new information **conditional on the first**. Where the same respondent answered several items, preserve higher-order co-travel. This is what makes PYAT more than a dashboard and more truthful than independently sampling unrelated percentages.

**The word “prior” needs discipline.** In a conditional probabilistic sampling-law sense, an observed demographic condition can be informative about a questionnaire response. That does **not** mean it temporally precedes, causes or psychologically generates that answer. An attitude used to predict another answer is a different association/response-co-travel operation from a source-observed social position predicting a response. No learned psychological force may be inferred from MI alone.

The relevant scientific target is an **empirically bounded conditional response surface**, not an individual or a 100%-resolution theoretical universe.

## 2. What history already discovered—and where it betrayed its own objective

### V547: an intended country bracket that was not actually computed

Source: `data/ddm_build_copy/build_question_determinicity_summary_v547.py`, inspected protected blob `3fc894501ce77c6519a2b32213f3f017465553e5`. It explicitly records `analysis_mode="within_country"` and `country_code_policy="baseline_zero_predictor"`. The author recognized that country can absorb the country's institutional, cultural, demographic and even instrument differences, then trivially overwhelm other predictors.

**But** its `compute_rows` constructs a pooled respondent frame for the question, computes `country_code_score` over all its countries, then computes MI for other predictors over that same pooled frame while merely excluding `country_code` from the winners. It **does not subset, stratify or model the MI by country**. Its claimed `within_country` is a **label**, not an implemented statistical condition.

The trap is neither that country is a meaningless variable nor that country somehow causes everything: country can be a high-information **proxy for national answer baselines, populations, survey wording, fieldwork and real material histories simultaneously**. Excluding it from a ranking does not purge those effects from other predictors correlated with it.

**Concrete falsifier (synthetic):** In country A, X=1 is 90% prevalent and Y=1 is 90% prevalent; X and Y are *independent*. Among 100 respondents the 2×2 X,Y cell counts are 81/9/9/1. In country B, both are 10% prevalent and independent; counts 1/9/9/81. Pool both countries: X,Y counts 82/18/18/82, and sample mutual information is **approximately 0.319923 bits**, although **within each country it is exactly 0 bits**. That alone can create an enormous apparent “determinicity” ranking. The solution is **actual country-conditioned source population**, not naming a pooled result “within-country.”

**Correct default:** where a governed survey is comparable and has genuine country populations, query each country within the actual source/wave/question/eligibility/weight design. Report country-specific results. Country remains meaningful for legitimate cross-country **F6/F7 comparability and explanatory world inquiries**, not a forbidden concept. A national estimate remains a separate target with its own survey design/weights; a deliberately cross-national question requires explicitly permitted populations and measurement comparability, not a fake unit respondent.

**Survey-design caveat:** Bracket a country in the *estimand and point-estimate query* without necessarily discarding survey-design data required for correct domain variance estimation. CDC's NHANES guidance warns that physically dropping records before defining a complex survey design can produce wrong standard errors. Preserve source-specific strata/PSU/repeated-weight information and conduct domain estimation correctly when claiming population inference.

### V550: raw entropy from one population, conditional entropy from another

Source: `data/ddm_build_copy/ddm_v550_branching.py`, protected blob `8f6d40e0d016d66e5a3b334b31747eaef752873f`. `indicator_summary_rows` computes `baseline_h = distribution_entropy(y, weights)` over every target-observed row, then masks X-missing respondents before calculating `conditional_entropy(yx,x,wx)`. `branch_nodes_rows` repeats the pattern at each node. The naive subtraction is not an estimate of `I(Y;X)` on one population.

**Concrete falsifier (synthetic):** 50 respondents have observed X all at one value and observed Y=A; another 50 have X missing and Y=B. Overall Y entropy = **1 bit**; observed-X conditional Y entropy = **0 bits**; the historical subtraction says X gave **1 bit** of value discrimination. But observed X has **only one value**: among people for whom X is observed, **X-values provide 0 bits**. The missingness *itself* supplies the information. That is a potentially important measurement or social-selection pattern, but it must not be labeled the substantive variable's differentiating power.

V550 separately returns MI/NMI/Cramér's V on differing weight treatments in parts of its old implementation and defaults to depth 3, support cap 30 and top-two branch values. None of those numbers or formula mixes is binding current science. **Recover the functional question and the respondent-coherent source, not these mechanical shortcuts.**

### V547 interaction inflation from unmatched complete-case populations

V547 `pair_mi_score` uses complete cases for (X1,X2,Y), but `mi_score` for each X uses its *own* (X,Y) complete cases. Subtracting their scores to claim a pair's incremental “interaction gain” compares different populations. The correct `I(Y;X2 | X1,D,R*)` (and alternative conditional direction) must use one shared eligible respondent population `R*` with an exact joint. Don't infer conjunction from separate survey marginals.

### Modern PYAT already contains the numerical core

Protected `rawlsing_next/pre553_diagnostics.py` blob `32a2d063f3b69fc983b352e69e032dd214a3e8d7` is **not** V550 lifted intact. `produce_governed_diagnostics` consumes exactly sourced, authority-checked I03 `EmpiricalFact/EmpiricalQuerySpec`. It calculates entropy, MI, NMI, Cramér's V and cell uplift from a **single exact arity-2 contingency** in `_association_metrics`, with exact source refs, replay, typed low-support/negative and diagnostic-only provenance. Its source states explicitly say diagnostic ranking **cannot mint empirical truth or control I05's authorized frontier**.

**This is the crucial architectural fact: do not build another entropy calculator.** The missing *whole* is the country/source/domain query issuance, comparable-cohort and missingness semantics, systematic candidate comparison, affordable next-query selection and first actual downstream consumer. Do not falsely claim that the modern diagnostics' correct within-table arithmetic itself solves those **between-table** compatibility and real-source issuance problems.

Existing `pre553_empirical_query.py::execute_empirical_query` and `I03GroupedExecutionScope` already contain source/authority and execution-local shared-core machinery; `pre553_discovery_exact.py` and `pre553_discovery_adaptive.py` separate exact issued frontiers from partial cost-driven exploration; `pre553_analytical_composition.py` and N10E consume conditioned facts. Direct saved-estate I03 reuse under current unmerged S2-D remains **unproved at realistic source width**, not assumed from protected in-memory code.

## 3. The scientifically useful reconstruction

### A. Fix the legitimate population before doing arithmetic

Let `S` be a source-specific edition and wave; `C` the permitted country/domain; `D` the currently established demographic/source-condition configuration; `Y` the exact response target; `X` a candidate measured splitter; `R_0` the source-qualified eligible/asked/target-observed/respondent-linked analytical population for **this declared estimand**. Record the difference between eligible, administered, response received, don't know, refused, not applicable, structurally missing and truly absent source fact.

Do **not** assume all participants answered all questions. A source-specific design weight/PSU/stratum may be authorized for population inference; if not, the result is a **sample descriptive/exploratory** estimate, not an unexplained nationally representative prior.

For each candidate X, track its observation/availability state **separately** from its actual values. This is how the machine can learn from nonresponse without accidentally inventing X values.

### B. Decompose missingness rather than corrupting predictor value gain

Define `M_X` = whether X was genuinely observed (with further typed administrative nonanswer reasons available); define `X_obs` only when observed. Under one common `R_0`:

`I(Y ; [M_X, X_obs] | D) = I(Y ; M_X | D) + P(M_X=observed | D) I(Y ; X_obs | D,M_X=observed)`.

This is an **exact chain-rule identity** for the joint variable that stores both the observation state and the observed value (with a missing sentinel); its probabilities must use the same selected valid measure/estimand. The terms are different kinds of information:

- **Observation-pattern information**, `I(Y;M_X|D)`: which Y answer patterns co-occur with X being recorded/asked/missing.
- **Substantive observed-X value information**, `I(Y;X_obs|D,M_X=observed)`: how actual distinct X values differentiate Y among respondents for whom X was observed.
- **Coverage-adjusted observed-value contribution**, `q_X × I(Y;X_obs|D,M_X=observed)` where `q_X=P(M_X=observed|D)`: the value-information contribution per member of the original domain, sensitive to a predictor's actual availability.

**Why this matters:** It turns V550's defect into a productive distinction: did the “predictor” matter because its *values* differ, or because the *survey/people who could answer it* differ? This can be computed from **sparse, compact counts**, without imputation or new respondent data. It preserves the whole target domain, distinguishes nonavailability from observed value, and retains an inexpensive path to honest coarse analysis. It does **not** assert that missingness is a psychological trait, nor infer the unobserved X–Y relationship.

For multiple missingness categories, compute the observation-status term over a properly typed state variable; keep actual X values nested only within observed cases. If Y itself is missing, its participation depends on the issued Y estimand and cannot be silently recoded as a valid attitude. The decomposition describes the measured sample (or design-qualified domain), **not** the latent truth about unobserved opinions.

### C. What ranking can actually mean

Do **not** force one undifferentiated score with mysterious weights. Retain a **small vector of comparable evidence**, at least:

1. **Value discrimination** within legitimately observed X: within-X conditional MI/entropy reduction, cell-level conditional answer distributions and uplift;
2. **Domain reach/coverage**: the observed X share, and the separate observation-pattern/selection information;
3. **Credibility**: raw sample and effective design precision where available, source response topology, support per branch, uncertainty, potential overfit and source/model grade;
4. **Incremental gain**: information gained **after already known D**, and, for a second variable, after the exact chosen X1, all on an agreed shared cohort;
5. **Downstream usefulness and cost**: which previously unknown demographic variation/minority repertoire would it make usable for SOROK, and what are additional I/O/compute/retention costs?

**Different X's observed-only MI values may refer to different subpopulations.** They cannot automatically be ranked as a coherent universal hierarchy. Coverage-adjusted contribution is calculable on the common original domain, but it measures information made available through each survey measurement—not a pure causal or psychological importance ranking. To make a stronger **between-X observed-value** comparison, require exact shared qualified respondent overlap, an explicit model for missingness or a common held-out predictive task with correct abstentions/availability. If these are infeasible or incomparable, report **partial order / comparable subsets / no single winner**. This is a useful answer, not a failure.

### D. Penalize spurious detail and uncertainty *selectively*

A variable with many possible categories has more opportunities to win a raw split, especially in small cells. A many-level education/region/income coding can outrank a lower-level variable by chance. Use a **cheap initial information screen** but demand more evidence before acting on narrow cells or high-cardinality findings. Options, ordered by practical cost/fit:

- *Default inexpensive:* source-correct contingency + within-domain effect magnitude + support per cell, stable/clear uncertainty reporting; no claim of population precision without design. Prefer finite, meaningful source-authorized categories, not post hoc answer-seeking recodes.
- *When a splitting decision materially matters:* compare improvement against a simple baseline using an honest separated sample or design-aware replication; avoid target leakage, repeated respondents across folds and unsupported random i.i.d. inference. A small, lawful validation may overturn a naive MI winner.
- *When sample/position support is sparse and downstream needs are important:* consider **separately graded hierarchical partial pooling or shrinkage** only under admitted source/measurement and model assumptions; publish model dependence, and do not silently replace observed minority frequencies with smoothed national majority. Independent surveys require transport and valid population linkage, not invented respondent joins.
- *When none of the above is feasible:* return a coarser source-supported distribution, a tied/uncertain ordering or next-query HOLD. The output remains productive.

**Not selected by default:** heavyweight random forests, an exhaustive permutation search over every country/wave/target/candidate, universal bootstrap for every branch, universal high-dimensional Bayesian fitting, massive precomputed interaction cubes, or a new database. These may be appropriate for a *particular* high-value unresolved problem, but are not a universal price of “scientific rigor.”

**Survey-inference distinction:** For a source with known complex design, weighted cell proportions are not sufficient to infer uncertainty or generalize to the population. Design-based domain variance can require full PSU/stratum context even when the target point estimate concerns a country/subpopulation. Kish effective N is at most a scoped approximation, never a substitute for correct design variance; if variance cannot be quantified, mark it **UNCERTAINTY_UNQUANTIFIED** instead of printing fake standard errors.

### E. Follow the branch, not an exhaustive cube

After a source-eligible, informative candidate X emerges, keep **all legitimate response alternatives** and the corresponding branch-specific source support; then, when useful, issue the next condition Y / X2 within a selected D+x. A response-to-response co-travel inquiry may require an exact joint of 3+ variables and corresponding source permissions; it is not satisfied by combining two marginal contingency tables.

Choose further work by **expected new information and practical cost** while reserving explicit exploratory room for minority/counterpattern hypotheses and an exact record of **searched, unsearched, low-power, unsupported** alternatives. Exact I05 complete-frontier claims must evaluate **their whole declared finite issued frontier**; adaptive ranking may arrange a partial search but cannot rewrite that fact or the underlying respondent observations.

Coarser intervals, partial branch ordering or a broader admissible D are always preferable to an unsupported answer presented at 8k precision. If the next condition adds too little scientifically relevant information or exceeds the resource budget, **stop** and deliver the current honest conditional response surface. A later consumer can legitimately request more detail.

## 4. The material implementation, not another engine

**Hard architectural choice:** reuse existing C11 → source-issued I03 → governed quantitative diagnostics → existing S04/DHIKR/N10E. Do **not** port V547/V550 wholesale, rewrite the existing exact diagnostic mathematics, replace accepted 13-family C11/Parquet, or force SOROK to consume a gigantic individual/personality tensor.

**The missing operation is a small *country-scoped comparative inquiry/selection wrapper*** coordinated by the existing S02/S04/diagnostics owners, not an independently self-issued scientific producer. It must request authenticated source-country-domain Y+X contingencies from I03, attach a **common risk-set/observation-status/estimand certificate**, consume existing replayable diagnostic outputs, calculate/express the observation-value decomposition where legal, and expose budget-labeled next-question offers and explicit abort/walkback.

### A. The intended *logical* product (not a new mandatory ABI)

An eligible logical response could expose:

`ConditionedResponseInquiry:
  source_release_ref, authority_refs, country_domain_ref, target_ref,
  domain_eligibility_and_design_ref, current_configuration_D,
  target_response_distribution + full morphology + missingness,
  candidate_Xs: [
    exact_comparison_cohort_ref,
    observation_status_distribution,
    actual_X_value_contingency_ref,
    MI_value, MI_observation_status, observed_share, contribution_value,
    within_condition_answer_cells + minority_support,
    design_uncertainty_or_qualified_UNKNOWN,
    diagnostic_grade, bias_risk, cost_accounting, next_query_refs
  ],
  ranking_state: COMPARABLE | PARTIAL_ORDER | INCOMPARABLE | HELD,
  searched_frontier_ref, unsearched/underpowered_holds,
  consumer_first_read_ref, replay_and_currentness_ref`

These are **desired logical fields**, not a command to invent this Python class, store one object per possible person, make all fields mandatory for every source, or claim the current I03 ABI already emits them. Reuse and extend **only** current owners' actual types where the first genuine consumer needs a missing field.

### B. Reuse, physical complexity, concrete stopping decisions

**One independent source read / durable existing C11** preserves respondent occurrence and survey semantics; indexed queries reduce repeated source scans where already supported. In a source-qualified domain with N relevant respondents, a k-category X and a-category Y, the **retained** sparse diagnostic table scales with the **actually represented (X,Y) cells** (up to k×a), not with all possible respondent-shaped persons. The **working query time** additionally depends on source/event selection, stored physical layout, row-group and session-index rebuild costs, and cannot be claimed O(1) or “cheap” without actual measurement.

Use the available I03GroupedExecutionScope cache where its live source/authority/cold saved reader actually support it, and record real hit/miss/capacity. The current documented S2-D direct estate may still rehash members and rebuild a temporary SQLite posting index on fresh opens. **Profile that accepted path** before proposing another cache or physical ABI. Cache exactly reusable components only when its retained size, invalidation proof and meaningful repeat-query cost earn it.

**Avoid Cartesian materialization:** with m eligible predictors and average k values, a naïve depth-d branching enumeration can grow roughly as `O((m k)^d)` before response-question combinations; merely “allow arbitrary depth” does not require eager computation of that tree. Instead an *anytime* bounded frontier returns the current honest resolution, may refine relevant branches next, and retains an unsearched scope record. No fixed depth, category limit or query-count ritual is adopted.

**Four resource decisions must be recorded:** human/engineering effort, available compute/quota, wall-clock first/repeated work, and peak RAM/temporary+retained storage on the actual host. A historical 6 GiB/100k stress test may inform the court but is **not** a presently reauthorized binding universal threshold. The agent-invented **1/10/100** query-count ritual is explicitly NOT BINDING. Choose only enough workload variation to reveal whether the next engineering choice changes. **Scientific sophistication cannot bankrupt the implementation.**

### C. The real first reader and the minimal completion sequence

1. **Source permit and first I03:** latest MainMac #1185 reported both SRC04/SRC16 original saved wave estates cold-admitted, but **QUERY_NOT_ISSUED**. An actual source-science owner must issue a lawful country/response/risk-set request or typed HOLD; do **not** rebuild or silently compute over privately held source files to force a positive. Independently, the #997 owner already owns the generic 13-family one-pass persisted first-consumer bridge.
2. **One meaningful direct conditioning:** on the earliest lawful source or explicitly sourcefree fixture, ask *one qualified response and its observed country-specific baseline*, *two measured candidate predictors*, and compute their valid I03 arity-2 contingencies with current `pre553_diagnostics.py`. Verify the same risk/population law and missingness distinction. If current code already does it, **reuse—no new score engine**.
3. **One truthful compared result:** produce matched-population **ranking or explicit incomparable state**, report observation status, branch support, full response alternatives and estimated value information. Use the chain-rule decomposition as a small additional **diagnostic projection** if the currently emitted contingencies actually carry its required missingness cells; if not, the smallest existing-owner extension is source-authoritative observation-status/I03 query inclusion, *not* a second statistician database.
4. **One narrower re-query or justified stop:** inspect a meaningful minority/contrary conditional or one true 3+ respondent joint if affordable and source-issued; if underpowered, broaden scope and state the cost/uncertainty. Do not create millions of empty cells to satisfy theory.
5. **One downstream altered observation:** have the actual S04/DHIKR or N10E receiving owner consume the result and show changed conditional possibility or rightful refusal when the eligible source cell changes. The consumer, **not a ranking CSV**, is the finished capability.
6. **Only then** profile the actual realistic ingest/cold/index/queries/retention; apply a narrow proven economics repair if performance is unacceptable. Expand to authorized two-series and a different survey family; later original35 F1–F8 no-loss receiving and SOROK sampling remain distinct work.

Do not turn steps 1–6 into new independent 20-worker commissions. They are **one bounded integration path through existing owners**.

## 5. A compact hostile scientific test suite (not a ritual count)

| Test | Attacker input | A defensible outcome |
|---|---|---|
| **Country confounding** | Two individually independent country populations whose pooling yields 0.319923 MI bits | Within-country predictor MI 0; country contrast retained as separate world/source fact |
| **Missingness impersonates X** | X observed in half with one constant value, Y fully tracked | Observed-X value MI 0, observation-pattern MI positive; no “X predicts Y 1 bit” claim |
| **Different candidate cohorts** | X1/X2 have different source/routing/missing overlaps | Explicit comparability certificate or PARTIAL_ORDER/INCOMPARABLE; no false universal winner |
| **False interaction** | Pair X1/X2/Y overlap differs from each single-predictor overlap | Pair incremental claim recalculated on *one exact* matched joint population |
| **High-cardinality false victory** | Many-level noise compared with low-cardinality meaningful X at low N | Rank provisional; compact bias/reliability validation before treating candidate as strong |
| **Survey design and morphology** | Weighted clustered sample, routed target, observed zero versus not asked | Accurate domain point/uncertainty grade and exact selected source states |
| **Minority and budget** | Rare, observed contradictory branch with insufficient resources for full tree | Retain observable alternative and query/ref, limit expansion, report unsearched rather than absent |
| **Consumer proof** | A legitimate source cell changes without changing schema/authority | Actual downstream conditioned product changes or legal refusal; no “standalone diagnostics = completed PYAT” |

**Proof discipline:** These wider first-reader tests remain future work at precise engineering owner cuts. A scoped source-neutral **observation/value decomposition** and ten sourcefree falsifiers **were run locally** at exact committed source blob identities. They do **not** execute current source-driven I03, model validation, joined survey design or end-to-end native/consumer tests. Do not claim the sourcefree 10/10 result certifies native science.

### Executed reference candidate — deliberately smaller than another PYAT engine

The smallest new calculation that existing `pre553_diagnostics.py` does not yet explicitly supply is separating the information in **the availability/status of X** from the information in **its observed values**. The added [reference operation](https://github.com/maidiu/rawlsing/blob/7dde3ed398a91805b953ca63d6a711291c1df7c7/WORKER_RETURNS/PYAT_HAQQMULCH_DETERMINICITY_20261120/reference_observation_value_information.py) (Git blob `490992899fc7ff10b7e79ef6420e0c0936ba599c`) is a **pure aggregate-count diagnostic-only** function. It uses only Python standard library and exact `Fraction` cell weights. It makes no source reads or truth/permission claims and *cannot* invent a missing X value. Its explicit requirement is an **already source-qualified I03 common-domain observed/missing contingency**—which is not yet shown to be emitted in production.

[Sourcefree regression tests](https://github.com/maidiu/rawlsing/blob/7dde3ed398a91805b953ca63d6a711291c1df7c7/WORKER_RETURNS/PYAT_HAQQMULCH_DETERMINICITY_20261120/test_reference_observation_value_information.py), Git blob `197499195dff6c9c64a225dd58d04cab3512c73f`, test country pooling, an observed constant-X/missingness impostor, true X-value gain, typed nonanswers, rare alternatives, exact fractional counts/scale invariance, and hard rejection of invented nonobserved X, missing observed values, floats masquerading as exact weights and empty/negative cells.

**Actual execution:** Python **3.13.5** in the present sandbox, command `python -m unittest discover -s /mnt/data/haqqmulch_check -p 'test_*.py' -v`; **10 tests PASS, 0 FAIL**, 0.002 seconds reported by unittest. Independently checked local `git hash-object` values against both committed GitHub source blobs, **byte-for-byte identical**, so the local execution is the exact candidate code/test identity, not a vaguely similar reconstruction. This is a **small scientific-math witness only**. No PYAT imports, original respondent data, I03 provenance/authority, full survey design, current native source or first downstream consumer were exercised. It is an existing-owner **adoption/proposal**, not production implementation or G5 acceptance.

**Next owned adapter**, if useful after a legal I03 result: obtain the observation-status × observed-X-value × Y aggregate via the governed source-risk pipeline, then feed those exact count cells into the diagnostic projection. **Do not create a parallel source decoder, duplicate estimator, new C11 store or universal ranking engine.** If the current I03/diagnostic product already contains an equally adequate typed observation-status decomposition on the latest actual HEAD, **reuse it and retire this reference**.

## 6. Alternatives rejected for now, alternatives left legitimately open

**Reject for now:** all-person sampling precompute; one global transnational importance ranking; V547's pooled “within_country” label; V550's mixed-denominator gain; unqualified universal causal/deterministic interpretation; importing random forests solely to have feature importance; a large precomputed census of all multidimensional contexts; a universal expensive hierarchical model; a new primary C11 storage design; demanding a fixed 100-query test; an all35 population grant inferred from sourcefree scaffolding.

**Retain as specialized later tools:** per-source design-aware sampling/uncertainty; a finite conditional-inference tree with bias controls; conditional/permutation predictive checks when an actually selected comparison warrants them; partial pooling for truly sparse source-qualified subgroup estimands **as a model with honest assumptions**; sensitivity analyses for nonignorable missingness; source-correct F6/F7 country/time comparison; explicit respondent-coherent multi-response attitude clouds; structural interpretation under independent Field Forge evidence.

**The default is neither a decision-tree religion nor a mutual-information religion.** It is the smallest source-correct conditional query whose statistics and within-group alternatives are actually consumed by the continuing empirical-social machine. The solver can choose alternative methods at the appropriate owned target when they earn their extra cost.

## 7. Outside data-science research and exact relevance

Primary-methodological sources consulted 2026-11-20; their published claims are not evidence that PYAT has run those methods:

- **Hothorn, Hornik & Zeileis (2006), “Unbiased Recursive Partitioning: A Conditional Inference Framework.”** Separates selection of informative splitting variable from split point selection, controlling systematic variable-selection bias of tree algorithms. *Use in PYAT*: finite informed branching and avoiding a high-cardinality variable “winning” by having more split candidates; **not** a mandate to install a full forest. [Author-hosted paper](https://www.zeileis.org/papers/Hothorn+Hornik+Zeileis-2006.pdf).
- **Strobl, Boulesteix, Zeileis & Hothorn (2007), “Bias in random forest variable importance measures.”** Shows misleading variable importance and selection frequencies when predictors differ in scale or number of categories. *Use*: a raw high-MI/high-cardinality winning X is **hypothesis-generating**, not automatic confidence or causal power. [Journal text](https://pmc.ncbi.nlm.nih.gov/articles/PMC1796903/).
- **Paninski (2003), “Estimation of Entropy and Mutual Information.”** Establishes important finite-sample/bias issues of plug-in information estimates. *Use*: small cells and repeated search can create spurious apparent fine-grain determinicity. [Author PDF](https://www.cns.nyu.edu/pub/eero/paninski-infoEst-2003.pdf).
- **Lumley (2004), “Analysis of complex survey samples.”** Clarifies design-based/replicate methods for complex sampling. *Use*: unweighted sample descriptions, authorized population estimates and variance are **different evidence products**. [Paper](https://citeseerx.ist.psu.edu/document?doi=fef23a2efb06a23723ddb42dbc8abae3ce581c5b&repid=rep1&type=pdf).
- **CDC NHANES Tutorial, “Variance Estimation” / “Software Tips.”** Domain estimation and retention of PSU/strata context rather than physically dropping design records before variance calculation. *Use*: avoid a naive “filter country rows and compute population confidence” error. [Variance estimation](https://wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx); [Software tips](https://wwwn.cdc.gov/nchs/nhanes/tutorials/softwaretips.aspx).
- **Carpenter, Smuk and colleagues, “Missing data: a statistical framework for practice” (2021).** Missingness mechanisms and their implications for complete-case/inference; model assumptions cannot be inferred just by seeing a blank response. *Use*: the value-vs-observation information decomposition measures *what is observed*, not unobserved survey answers. [Open paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7615108/).
- **Journal of Survey Statistics and Methodology (2023), “A Comprehensive Overview of Unit-Level Modeling of Survey Data for Small Area Estimation Under Informative Sampling.”** Reviews model-based small-domain estimation and limited sampling. *Use*: partial pooling when direct within-configuration cells become too thin, **only as separately model-qualified estimate**, not an observed within-survey joint. [Review](https://academic.oup.com/jssam/article/11/4/829/7198195).
- **Statistics Canada / PracTools design-effect technical material.** Effective sample size and design effects depend on weighting, strata, clustering and the estimand; simple weight-only N_eff is conditional and insufficient as a universal inference guarantee. *Use*: don't let a numeric arbitrary small-n cutoff masquerade as actual effective precision. [PracTools vignette](https://cran.wustl.edu/web/packages/PracTools/vignettes/Design-effects.html).

## 8. HAQQMULCH verdict and actual next development

**SAVAGE:** The original “within-country determinicity” could be pooled country correlation in disguise; V550's information gain can conflate response differentiating power with predictor observation status; V547's pair comparison can mix populations; high-cardinality and thin samples can produce statistical illusions. The beautiful full DHIKRYMULCH could easily become a physically impossible Cartesian product if its demands were read as eager materialization obligations.

**RECOVER:** Original question-level MI, subgroup discovery and respondent-joint ambitions; modern exact I03/F1–F4/diagnostic mathematics and replay; already accepted compact C11/Parquet; source-condition and survey-design semantics; minority and rare-supported response morphologies; DHIKRYMULCH's conditional reverse query and later N10E/SOROK entrance.

**RECONSTITUTE:** *Country-true, source-qualified, observation-aware, matched-population conditional information* as a bounded, progressively refined inquiry with honest unsearched state. Where useful, split observation-pattern information from substantive value information. Apply explicit comparability/precision/cost tests before claiming a winner.

**BUILD NEXT:** do NOT invent another numeric engine. Have the **existing issuer/analytical owner** produce the first truly authorized I03 country-response-target facts, then extend the **existing diagnostic consumer** only for missing common-cohort/observation-status comparison and a real next-query/first-reader. Prove the first use and actual cost, then advance to the next valid consumer and broader source coverage. No preserved historical 8k-resolution demand can delay that.

**Hold:** `HQ_CURRENTNESS_HOLD` for no live accredited HQ/owner lease, no evidence this specific new comparative operator is independently reviewed or native-issued, no 35-wave saturation, no protected receiving. This document is an actionable **research-to-engineering owner candidate**, not a claim of a newly built determinicity runtime.