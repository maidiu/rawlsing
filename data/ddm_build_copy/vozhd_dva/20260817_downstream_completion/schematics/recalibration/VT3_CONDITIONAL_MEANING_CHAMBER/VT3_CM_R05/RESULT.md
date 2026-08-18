# VT3-CM-R05 — Conditional Compute and Cardinality Court

**Cell:** `VT3-CM-R05`  
**Mission:** quantify the computational/materialization cost of the existing V550 determinicity architecture and determine how much work disappears under an authority-first sparse conditional-evidence model, without deleting required meaning.  
**Examined repository base:** `8c87f7725ba58202b5377c974548140420709fa9`  
**Working branch:** `agent/vozhd-trii-vt3-cm-r05`  
**Production code modified:** **NO**  
**Evidence mode:** static code audit at the exact launch base. No DB-backed wall-clock benchmark was run in this court.

## Verdict

**MAJOR_STATIC_COMPUTE_AND_MATERIALIZATION_REDUCTION_IS_AVAILABLE_IF_AND_ONLY_IF_THE_REPLACEMENT_PRESERVES_EXACT_AUTHORIZED_CONDITIONING_PREDICATES_PROVENANCE_UNCERTAINTY_AND_TYPED_ABSENCE.**

The current V550 architecture already resolves a `question_use_contract` before the expensive determinicity suite, but then computes the broad generic suite anyway: 12-field position summaries, secondary-indicator ranking, full indicator×response matrices, outlier cohorts, recursive branch trees, and optionally position-signature associations. The principal waste is therefore not respondent extraction itself; the shard builder already prefetches selected response rows by country and can harmonize them once. The principal waste is **post-authority broad analytical expansion and repeated metric work**.

At `P=12` generic position fields and recursive depth `D=3`, the current five determinicity families imply a conservative lower bound of **92 logical field/subset evaluation units per question** before counting the multiple internal passes performed by normalized mutual information, Cramér's V, crosstabs, weighted pivots, dominant-response calculations, sorting/grouping overhead, or optional branch-position signatures. If branch-position signatures emit, the lower bound rises to **104**. An authority-first compiler that needs only `K=1..4` exact conditioning predicates and conditional response counts has only `K` predicate-distribution accumulations in the corresponding core. On this deliberately conservative unit model, the removable field-evaluation surface is approximately **95.7%–99.0%** for `K=4..1` against 92 units, or **96.2%–99.0%** against 104 when position signatures emit. This is **not a wall-clock prediction**; it is a static operation-count ratio.

The matrix/materialization savings can be still larger when authority names exact predicates rather than whole dimensions. Current `indicator_answer_matrix` cardinality for question `q` is:

`M_q = Σ_p (V_qp × C_qp)`

where `V_qp` is the number of observed nonblank values for position field `p` and `C_qp` is the number of response categories observed among rows having that position field. The code emits the full crosstab rectangle, including zero-count cells. A sparse exact-predicate representation needs approximately:

`M_sparse,q = Σ_a C_qa`

for authorized predicates `a` such as `income_level=low`; if authority instead requires all values of a permitted dimension, the cost for that dimension remains `V×C` and cannot be claimed as removable.

The court therefore supports a large compute simplification, but **does not authorize semantic deletion**. In particular, the present `ddm_v551_conditional.py` compiler does not emit `position_field` or `position_value`. It cannot, by itself, establish semantic equivalence to an exact conditioned empirical distribution. Any redesign that drops V550 conditioned rows before a predicate-preserving replacement exists would violate the governing spirit.

---

## Governing law applied

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md`  
Blob SHA: `588cf3954c33417665c5f9bac04e8b27e75d7f7c`

Applied clauses:

- minimum sufficient machinery without duplicated semantic ownership or ornamental governance;
- never let downstream vividness exceed upstream authority;
- preserve uncertainty, lawful absence, provenance, replay, multiplicity, and structural constraint without turning statistics into psyche;
- convenience/compression is invalid if it flattens required distinctions.

This court treats compute savings as subordinate to exact semantic preservation.

---

# A. Current computational graph

## A1. Extraction and preparation

Primary implementation:
`data/ddm_build_copy/build_determinicity_wave_shard_v550.py`  
Blob SHA: `82ffc18df29a8e5ebd78cde97c89d463b3842df6`

Shared implementation:
`data/ddm_build_copy/build_determinicity_repository_v550.py`  
Blob SHA: `afd2a59e1cdff0024a57acaf1dab8ff30534e565`

Observed graph:

1. Resolve survey/wave scope and question mappings.
2. Build the selected question list.
3. Prefetch response rows **once per country** across selected question variable aliases via `_prefetch_question_rows_by_country`.
4. Optionally harmonize the prefetched country cache once via `_prepare_v550_question_row_cache` (`country` or `chunked` mode).
5. Slice question rows from that cache via `_question_rows_from_cache`.
6. Resolve per-question source-structure authority and build `question_use_contract`.
7. Build response distributions.
8. Only **after** response-distribution computation, zero them when `allowed_as_response_distribution` is false.
9. Unconditionally compute the five determinicity families.
10. Optionally compute cloud/signature families.
11. Write per-question checkpoints.
12. Combine checkpoint tables.
13. Build wave-level `position_distribution`.
14. Build V550→V551 bridge by serializing every row from mapped bridge tables.
15. Write bridge, read it back, validate, optionally build row-level bridge audits.
16. Write final tables (and CSV mirrors when enabled).

### Extraction finding

The current architecture has already solved much of the obvious repeated SQL problem. `_prefetch_question_rows_by_country` issues one selected-response query per country, and prepared-cache mode can harmonize each prefetched row once. An authority-first redesign should **retain this good shared-substrate behavior**, but shrink the selected question/predicate universe before extraction when higher authority permits.

---

## A2. Generic position universe

`data/ddm_build_copy/ddm_v550_branching.py`  
Blob SHA: `8f6d40e0d016d66e5a3b334b31747eaef752873f`

`INDICATOR_FIELDS` is hard-coded to exactly 12 generic fields:

1. `sex`
2. `age_group`
3. `education_level`
4. `income_level`
5. `religion_label`
6. `urban_rural`
7. `region`
8. `ethnicity`
9. `language`
10. `employment`
11. `marital`
12. `household_size`

The existence of question-level authority fields such as `allowed_as_demographic_predictor`, `allowed_as_branch_splitter`, and `position_conditioning` does **not** cause the five determinicity builders to restrict this universe before calculation.

---

## A3. Per-question response distributions

`data/ddm_build_copy/ddm_v550_distributions.py`  
Blob SHA: `43a62723b16f9c800ed7a6ef40a77e70a3f07377`

`build_distribution_tables`:

- classifies weights;
- groups all question rows by `response_value_normalized`;
- resolves response semantics per response value;
- emits `answer_distribution`;
- then groups again by `country_code` and response value for `country_answer_distribution`.

In the active shard builder, this work is performed before `allowed_as_response_distribution` is checked; disallowed outputs are computed and then replaced by empty frames.

**Removable when authority disallows response distributions:** almost all grouping/semantic-row construction for those questions, provided any required typed absence/audit receipt is preserved.

---

## A4. Position indicator summary

`indicator_summary_rows` computes:

- baseline entropy;
- baseline dominant response;
- for each of up to 12 indicators:
  - conditional entropy;
  - entropy reduction / MI-like delta;
  - normalized mutual information;
  - Cramér's V;
  - dominant-response calculations;
  - support and weighted counts.

Asymptotically, treating category counts as bounded relative to respondents:

`T_indicator(q) = Θ(P_q × R_q)`

but this hides several full or near-full passes per field.

---

## A5. Secondary indicator summary

`secondary_indicator_summary_rows` first **recomputes essentially the same full candidate score set** as `indicator_summary_rows`, including conditional entropy, normalized MI, Cramér's V, dominant response, and support. It then chooses one primary indicator and tests every other candidate jointly:

`joint_key = primary || secondary`

and recomputes conditional entropy for each qualifying secondary candidate.

Static lower-bound field evaluations:

`P_q + (P_q - 1) = 2P_q - 1`

plus the internal metric passes.

This is the clearest duplicated statistical work in the determinicity suite: the first `P` candidate evaluations duplicate the position-summary ranking inputs rather than reuse them.

---

## A6. Indicator answer matrix

`indicator_answer_matrix_rows` computes, for every available generic indicator:

- unweighted crosstab `indicator_value × response`;
- weighted pivot of the same rectangle when weights exist;
- one output row for **every crosstab cell**, including zero cells.

Cardinality:

`Rows_matrix(q) = Σ_p V_qp × C_qp`

The matrix therefore materializes the Cartesian rectangle of observed position values and observed response categories for each field, not merely observed nonzero pairs.

Compute:

`T_matrix(q) = Θ(P_q × R_q + Σ_p V_qp C_qp)`

with an additional weighted pivot when weights exist.

---

## A7. Outlier cohorts

`outlier_cohort_rows`:

- computes baseline dominant response;
- for every generic indicator, performs a groupby over indicator values;
- for every supported value, computes dominant response and branch classification.

Compute:

`T_outlier(q) = Θ(P_q × R_q)`

Materialization upper bound:

`Rows_outlier(q) ≤ Σ_p V_qp`

after support filtering.

This is another independent pass over the same position partitions already represented by the answer matrix.

---

## A8. Recursive branch nodes

`branch_nodes_rows` recursively:

1. computes node response entropy;
2. evaluates **every remaining indicator** using conditional entropy;
3. chooses the best gain;
4. follows only the two most frequent values of that best indicator;
5. repeats until depth, support, purity, or no-gain stop.

If child nodes partition respondents and `D` is maximum depth, respondent mass at each level is bounded by the root respondent mass. The dominant scan bound is therefore:

`T_recursive(q) = O(R_q × Σ_{d=0}^{D-1}(P_q-d))`

`= O(R_q × (D P_q - D(D-1)/2))`

rather than `R × number_of_nodes × P`.

For `P=12`, `D=3`:

`12 + 11 + 10 = 33`

field-equivalent respondent scans.

Because each split follows at most two values:

`Rows_recursive(q) ≤ 2^(D+1) - 1`

so at `D=3`, at most 15 node records before support/no-gain pruning.

This distinction matters: recursive branching is CPU-heavy through repeated candidate scans, while node-row cardinality itself is bounded.

---

## A9. Branch position signatures and repeated association metrics

`data/ddm_build_copy/ddm_v550_clouds.py`  
Blob SHA: `dfc878e87d984a1a3d7000a0c726bdc444f9945f`

When `should_emit_cloud_tables` permits emission and the question contract allows branch-position signatures, `build_position_signature_rows` loops position-coordinate fields and calls `_candidate_association_stats`, which **again** computes:

- normalized mutual information;
- Cramér's V;
- dominant feature and target responses.

It keeps at most five ranked features, but it can evaluate all 12 before truncation.

Thus the same NMI/Cramér's-V relation can be calculated in:

1. `indicator_summary_rows`;
2. `secondary_indicator_summary_rows` initial candidate scoring;
3. `build_position_signature_rows`.

The stored top-5 signature cardinality is small; the upstream computation can still scan all position fields.

---

## A10. Position distribution

`data/ddm_build_copy/ddm_v550_position_distribution.py`  
Blob SHA: `651329254244e9f42a8d88c2721ccae6bd768073`

`build_position_distribution_rows` operates at wave/country level over the shared prefetched cache:

- `_respondent_slice` sorts and deduplicates the long response substrate to one row per respondent/country;
- for every generic position field, groups respondent values and emits weighted/unweighted prevalence.

If `L_w` is the long prefetched row count for a wave and `R_w` unique respondents:

`T_position_distribution ≈ O(L_w log L_w + P R_w)`

Materialization:

`Rows_position_distribution = Σ_country Σ_p V_country,p`

This cost cannot be classified as disposable merely because it resembles other position summaries. It is a population-position prior, not a question-conditioned response distribution.

---

## A11. V550→V551 bridge

`data/ddm_build_copy/ddm_v550_bridge.py`  
Blob SHA: `29edd5e24f095334683035f2ce1ec95674fe274b`

`BRIDGE_TABLE_MAP` includes:

- `answer_distribution`
- `country_answer_distribution`
- `position_distribution`
- `position_indicator_summary`
- `indicator_answer_matrix`
- `outlier_cohort_summary`
- `secondary_indicator_summary`
- `recursive_branch_nodes`
- `branch_position_signature`
- `branch_relation_co_signature`
- `branch_co_signature`
- `question_response_attitude_cloud`
- `mapping_gap_report`
- `underpowered_quarantine`

`build_v551_bridge_index_for_table` iterates every source row through Python, constructs a large bridge dictionary, and then applies V551 eligibility.

Therefore:

`Rows_bridge = Σ_t Rows_t`

for nonempty bridge-mapped source tables, subject to no pre-serialization semantic pruning.

The bridge is written to parquet (and optionally CSV), read back for validation, and may then be scanned/grouped again for full bridge audits when its row count does not exceed `BRIDGE_AUDIT_MAX_ROWS = 250000`.

### Literal duplicate

The shard builder sets:

`wave_tables["branch_co_signature"] = wave_tables["branch_relation_co_signature"].copy()`

and the bridge map contains both names. When populated, this creates a compatibility duplicate that is independently serialized into the bridge.

---

# B. Cardinality equations

Define per question/country cell:

- `R` = respondent rows for the question;
- `P` = present generic position fields, `P ≤ 12`;
- `V_p` = nonblank unique values of position field `p`;
- `C_p` = response categories observed among rows where `p` is nonblank;
- `C` = overall response category count;
- `D` = recursive maximum depth;
- `B` = recursive node count;
- `K` = authority-permitted conditioning dimensions in the sparse model;
- `A` = authority-permitted **exact predicates** (dimension=value conditions);
- `S` = number of secondary candidates, at most `P-1`.

Current principal rows:

- answer distribution: `≈ C`
- country answer distribution: `≈ C` for a country-scoped question cell
- position indicator summary: `≤ P`
- secondary indicator summary: `≤ P-1`
- indicator answer matrix: `Σ_p V_p C_p`
- outlier cohorts: `≤ Σ_p V_p`
- recursive nodes: `B ≤ 2^(D+1)-1`
- branch position signature: `≤ 5` emitted rows, but up to `P` evaluated candidate fields
- bridge: sum of all mapped source-table rows, including compatibility duplication.

Current lower-bound logical field-evaluation units for the five determinicity families:

`E5(P,D) = P + (2P-1) + P + P + [D P - D(D-1)/2]`

`= 5P - 1 + D P - D(D-1)/2`

At `P=12,D=3`:

`E5 = 59 + 33 = 92`

If position-signature candidate scoring is emitted:

`E6 = E5 + P = 104`

These are intentionally conservative because one "unit" may itself perform multiple scans/groupings.

---

# C. Duplicated work

## C1. Direct statistical duplication

**Observed.**

`indicator_summary_rows` and the candidate-ranking phase of `secondary_indicator_summary_rows` independently compute the same family-level quantities for each indicator:

- conditional entropy;
- normalized mutual information;
- Cramér's V;
- dominant-response statistics;
- support counts.

No shared score cache is passed between them.

## C2. Repeated NMI/Cramér's V for position signatures

**Observed, conditional on signature emission.**

`build_position_signature_rows` recomputes association statistics against the same response target rather than reusing V550 determinicity scores.

## C3. Matrix vs outlier re-partitioning

**Observed.**

Both independently partition respondents by every generic position field. The matrix builds response counts per position value; outliers group the same partitions again to derive dominant-response labels.

If outlier semantics remain required, they are derivable from the same governed conditional count table without another respondent scan.

## C4. Recursive candidate rescanning

**Observed.**

At each recursive node, all remaining indicators are rescanned for conditional entropy even though root-level indicator conditional entropies were already calculated elsewhere. Child-node conditional statistics are genuinely new; root-level calculations are duplicated.

## C5. Response distributions computed before gating

**Observed.**

`build_distribution_tables` runs before `allowed_as_response_distribution` is checked. Disallowed frames are emptied only afterward.

## C6. Compatibility alias duplication

**Observed.**

`branch_co_signature` is a copy of `branch_relation_co_signature`; both are separately mapped into the bridge and final output surface.

## C7. Multi-stage materialization

**Observed.**

For each question the determinicity tables are written as checkpoint parquet files. Finalization reads/concatenates checkpoint data and writes final table files. Bridge construction then re-materializes mapped rows into a separate bridge table. Planned shard commands commonly enable both parquet and CSV, creating another mirror.

---

# D. Unnecessary materialization

The following is **compute/materialization-disposable only if parent authority establishes that the same required meaning is preserved elsewhere**:

1. **Generic all-12-field matrix rows outside authorized conditioning predicates.**
2. **Zero-count matrix cells** when exact sparse predicates are the governing representation and explicit absence can be represented without a Cartesian rectangle.
3. **Position indicator summary metric rows** if terminal authority requires conditional empirical distributions rather than predictor-ranking metrics.
4. **Secondary indicator summary** if no governing authority requires greedy primary/secondary predictor ranking.
5. **Outlier cohort rows** if their only required content is derivable from preserved conditional distributions with identical support/weight semantics.
6. **Recursive branch nodes** if no terminal authority requires greedy entropy-tree structure itself.
7. **Branch position signature ranking** if no terminal authority requires this diagnostic association surface.
8. **`branch_co_signature` compatibility duplicate** when its alias status has no independent consumer.
9. **Bridge rows sourced from disabled/diagnostic artifacts** when V551 and later stages have no lawful need for those rows.
10. **Row-level bridge audits** beyond the information needed for accountability; current code already recognizes this by switching to summary-only mode above 250,000 rows.

This court does **not** declare any item semantically deletable merely from cost.

---

# E. Sparse authority-first complexity

Hypothetical lawful flow:

`governed authority`
→ exact eligible question set
→ exact allowed conditioning dimensions
→ exact allowed position predicates
→ exact required empirical operation
→ selected respondent extraction
→ conditional distribution counts + weights + provenance + typed absence
→ downstream contract

Let:

- `Q` = current selected question count;
- `Q_a` = questions actually requiring conditional evidence;
- `K_q` = allowed conditioning dimensions for question `q`;
- `A_q` = exact authorized predicates for question `q`.

## Extraction

If authority can be resolved before respondent prefetch:

Current selected long-row substrate approximately scales with all selected questions.

Sparse extraction:

`T_extract_sparse ∝ Σ_{q∈Q_a} R_q`

plus any independently required direct-response/joint substrate.

This saving is proportional to `Q_a/Q` only where excluded questions are not needed by V550J/shared joint configurations.

## Conditional count core

Naive separate grouping:

`T_sparse(q) = O(R_q × |A_q|)`

A single streaming/vectorized accumulator can evaluate all authorized predicates during one respondent pass, making the dominant respondent read closer to:

`O(R_q + predicate_evaluation_cost)`

Materialization:

`Rows_sparse(q) = Σ_{a∈A_q} C_qa`

For authority that permits whole dimensions rather than exact values:

`Rows_sparse(q) = Σ_{p∈K_q} V_qp C_qp`

No saving may be claimed for an allowed dimension whose every value is semantically required.

## Removed metric families

If terminal authority requires conditional distributions and provenance but not predictor rankings, the following entire calculation classes disappear from the production path:

- entropy ranking;
- normalized MI;
- Cramér's V;
- primary-indicator selection;
- secondary-gain calculation;
- outlier classification scans;
- recursive best-split search;
- position-signature association ranking.

The conditional distribution itself does **not** require these metrics.

---

# F. Defensible savings ranges

## F1. Field-universe pruning only

Current generic `P=12`.

If lawful authority permits:

- `K=1`: 91.7% fewer position dimensions;
- `K=2`: 83.3% fewer;
- `K=3`: 75.0% fewer;
- `K=4`: 66.7% fewer.

This applies to dimension-proportional grouping work only.

## F2. Five-family analytical surface versus sparse conditional counts

Using the conservative `E5(12,3)=92` logical field/subset evaluations:

- sparse `K=1`: `(92-1)/92 = 98.9%` reduction;
- `K=2`: `97.8%`;
- `K=3`: `96.7%`;
- `K=4`: `95.7%`.

With optional position-signature scoring included (`E6=104`):

- `K=1`: `99.0%`;
- `K=2`: `98.1%`;
- `K=3`: `97.1%`;
- `K=4`: `96.2%`.

**Classification:** static operation-count estimate, not measured runtime.

## F3. Matrix row savings

Current:

`Σ_p V_p C_p`

Exact-predicate sparse:

`Σ_a C_a`

Therefore, for a single allowed predicate `p=v` compared with retaining all values of that field, the row multiplier falls from approximately `V_p×C` to `C`, i.e. a factor of approximately `V_p`.

Across the full 12-field suite the saving depends on actual field cardinalities; no numeric percentage is defensible without shard data.

## F4. Bridge serialization

Any source row removed upstream from the lawful production set also removes one bridge-row construction, eligibility pass, parquet row, validation row, and possible CSV row. Because the current bridge serializes diagnostic and disabled lanes as well as direct/derived evidence, bridge savings track eliminated source cardinality almost linearly.

No percentage is claimed without measured row counts.

---

# G. Costs that cannot be removed without semantic loss

1. **Exact conditioned response counts/distributions** for every terminally authorized predicate.
2. **Weighted and unweighted support** wherever survey weighting is valid or uncertainty/support law requires both.
3. **Response semantics identity**, including normalized response value/label and response-semantics contract hash.
4. **Typed missing/special states** where authority distinguishes missing, DK, refusal, not asked, inapplicable, etc.
5. **Support threshold/status and underpowered/zero-support semantics** where these affect admissibility.
6. **Question-use and source-structure provenance**, including authority hashes/receipts needed for replay.
7. **Wave/source/country/question identity** and exact conditioning predicate identity.
8. **Population position distribution** if terminal runtime requires a prior over generated structural positions; this is not equivalent to question-conditioned response evidence.
9. **Shared respondent substrate required by V550J joint configurations**; authority-first V550 pruning must not starve independently governed joint computations.
10. **Any all-values dimension distribution** where terminal authority explicitly requires heterogeneity across every value rather than one selected predicate.

---

# H. Benchmark plan

A redesign should not be accepted on static estimates. Validate it with paired runs over the exact same extracted source rows.

## H1. Representative cells

Select at least:

1. a low-response-cardinality question (binary/ternary);
2. a high-response-cardinality substantive question;
3. a large-respondent wave/country cell;
4. a small/underpowered cell;
5. a weighted cell with complete valid weights;
6. a partial/invalid-weight cell;
7. a question whose authority allows only one conditioning predicate;
8. a question allowing several conditioning dimensions;
9. a stress case with all 12 position fields present;
10. a V550J/shared-substrate case whose question union is broader than base V550.

Choose concrete waves from measured min/median/max quantiles of `R`, `P`, response cardinality, and country count; do not hand-pick only easy waves.

## H2. Run modes

For each benchmark cell:

- current V550 exact-base implementation;
- current V550 with prepared country cache;
- prototype authority-first sparse compiler using the **same prefetched input rows**;
- cold-cache and warm-cache runs separately.

## H3. Instrumentation

Record:

- wall time per stage;
- CPU time;
- peak RSS;
- prefetched long-row count;
- harmonization row/call count;
- per-family function call counts;
- conditional-entropy calls;
- NMI calls;
- Cramér's-V calls;
- crosstab/pivot calls;
- checkpoint bytes;
- final parquet bytes;
- CSV bytes when enabled;
- bridge rows and bytes;
- bridge-build and bridge-validation time;
- total rows by artifact;
- total filesystem writes.

## H4. Semantic equality gate

For every authorized predicate compare old and new outputs on:

- exact predicate field/value;
- response category identity;
- `n_unweighted`;
- `n_weighted`;
- `pct_unweighted`;
- `pct_weighted`;
- support status/threshold;
- typed special/missing state;
- response-semantics contract hash;
- source/question/wave/country identity;
- question-use/source-structure provenance;
- deterministic content hash under replay.

Any mismatch is a redesign failure until adjudicated.

Also assert that **unauthorized predicates are absent** from the sparse output.

## H5. Acceptance metrics

Report:

- speedup = `T_current / T_sparse`;
- CPU reduction;
- peak-memory reduction;
- checkpoint-byte reduction;
- final-artifact-byte reduction;
- bridge-row/byte reduction;
- semantic equality pass rate;
- number of authority predicates preserved;
- number of unauthorized predicates suppressed.

---

# Critical semantic-loss finding

`data/ddm_build_copy/ddm_v551_conditional.py`  
Blob SHA: `359665297677553a33556ce65c2e3d76b60b2cc1`

`build_conditional_determinicity_index` consumes `derived_determinicity` bridge rows, but `_conditional_row` does **not** emit `position_field` or `position_value`.

Separately, `ddm_v550_bridge._base_bridge_row` initially reads `position_field` and `position_value` fields by those exact names. V550 `indicator_answer_matrix_rows`, however, emits `indicator_name` and `indicator_value`. The inspected bridge helper section does not demonstrate a conversion of these names into exact `position_field`/`position_value` predicate fields.

Therefore this court cannot certify that the present V551 conditional index preserves the exact semantic object:

`P(response | position_field = position_value)`

even though its source lane is called `derived_determinicity`.

**Parent consequence:** do not delete V550 conditioned empirical rows on the theory that current V551 conditional determinicity already preserves equivalent predicate meaning. Predicate-preserving authority/schema must be established first.

---

# Counterevidence against an over-aggressive compute-deletion case

1. V550 already uses country-level prefetch and optional shared harmonization, so the architecture is not simply "N database scans per question."
2. `position_distribution` is a distinct population-position object and may be terminally necessary even if question-conditioned predictor summaries are not.
3. Recursive child-node statistics are not wholly duplicated by root-level summaries; child conditioning is genuinely different computation.
4. Full `V×C` matrices may be necessary if authority requires every value of an allowed dimension, not a sparse exact predicate.
5. Underpowered and zero-support states can be semantically meaningful; sparse representation must preserve them explicitly rather than merely omit cells.
6. V550J joint substrate requirements can force extraction of questions that V550 conditional evidence itself would not need.

---

# Unresolved questions

1. What exact predicate schema will R04/parent authority require at terminal runtime: one exact generated position, a set of allowed predicates, or full all-values conditional tables?
2. Is `position_distribution` independently required as a prior for V3 structural-position generation after W1 ADP-009 authority, and at what granularity?
3. Which V550 determinicity families have an accepted terminal semantic consumer versus diagnostic/history-only status? This court measured cost but did not adjudicate semantic ownership.
4. Does any downstream consumer rely on zero-count matrix rows as explicit lawful absence rather than deriving absence from a declared response/position domain?
5. Must weighted and unweighted conditional distributions both survive for every survey family, or can weight-status authority select one representation in some waves?
6. Can `branch_co_signature` be removed as a compatibility alias without breaking a current consumer?
7. What are real shard cardinalities (`Q,R,V,C`) and wall-clock stage shares at the exact base? No DB benchmark was available in this court.

---

# Recommended parent actions

1. **Require a predicate-preserving conditional-evidence authority/schema before implementation.** It must explicitly carry `position_field`, `position_value` (or a stricter predicate object), response distribution, support, weights, typed absence, and provenance.
2. **Use authority before compute.** Resolve exact eligible questions and conditioning predicates before distribution/determinicity builders and, where lawful, before respondent extraction.
3. **Collapse respondent scans, not meaning.** Compute authorized conditional counts once and derive any still-required summaries from that count object rather than rescanning microdata.
4. **Do not preserve MI/Cramér's-V/recursive ranking merely because current V550 computes them.** Require an explicit terminal consumer.
5. **Retain shared prefetch/prepared-substrate infrastructure** and extend it to the authority-pruned question union, including V550J-required union questions.
6. **Benchmark before acceptance** using the H-plan above and publish actual stage times, RSS, row counts, and byte counts.
7. **Treat current V551 conditional determinicity as insufficient evidence of semantic preservation** until exact conditioning predicate identity is proven.

---

## Evidence ledger

| Source | Blob SHA | High-value observed fact |
|---|---|---|
| `.../RAWLSING_GOVERNING_SPIRIT.md` | `588cf3954c33417665c5f9bac04e8b27e75d7f7c` | minimum sufficient machinery; no semantic flattening |
| `data/ddm_build_copy/build_determinicity_wave_shard_v550.py` | `82ffc18df29a8e5ebd78cde97c89d463b3842df6` | authority built before broad determinicity; five families computed unconditionally; checkpoints/final/bridge |
| `data/ddm_build_copy/build_determinicity_repository_v550.py` | `afd2a59e1cdff0024a57acaf1dab8ff30534e565` | country prefetch and prepared shared cache |
| `data/ddm_build_copy/ddm_v550_branching.py` | `8f6d40e0d016d66e5a3b334b31747eaef752873f` | 12 generic fields; duplicated metrics; matrix/outlier/recursive algorithms |
| `data/ddm_build_copy/ddm_v550_metrics.py` | `e7675f4080bb30e6526027a34db747b7be7f85c9` | entropy/NMI/Cramér's-V implementations |
| `data/ddm_build_copy/ddm_v550_distributions.py` | `43a62723b16f9c800ed7a6ef40a77e70a3f07377` | response/country distribution grouping |
| `data/ddm_build_copy/ddm_v550_position_distribution.py` | `651329254244e9f42a8d88c2721ccae6bd768073` | respondent-deduped population position distribution |
| `data/ddm_build_copy/ddm_v550_clouds.py` | `dfc878e87d984a1a3d7000a0c726bdc444f9945f` | position signatures recompute NMI/Cramér's V |
| `data/ddm_build_copy/ddm_v550_bridge.py` | `29edd5e24f095334683035f2ce1ec95674fe274b` | broad bridge map; direct/derived/context/disabled lanes; per-row serialization |
| `data/ddm_build_copy/ddm_v551_conditional.py` | `359665297677553a33556ce65c2e3d76b60b2cc1` | conditional index omits exact position predicate fields |
| `data/ddm_build_copy/ddm_v550_question_use.py` | `8d90a5116fd05b5db17e9b4645638a3aa6fc1131` | authority fields include position-conditioning and per-use allow flags |

---

## Court disposition

**Compute claim:** sustained. The current architecture performs a large amount of broad, repeated analytical work after authority is available.

**Compression claim:** qualified. Sparse authority-first conditional distributions can eliminate most of the measured analytical surface **only** where exact terminal authority permits that reduction.

**Semantic deletion claim:** not adjudicated here and specifically blocked where predicate identity/provenance would be lost.

**Benchmark status:** `NOT_RUN_STATIC_AUDIT`; H-plan is sufficient to validate the redesign empirically.
