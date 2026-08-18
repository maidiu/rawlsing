# VOZHD TRII D02 — V526d / V548 → CURRENT RECURSIVE POSITIONAL BREAKAGE COURT

**Court:** D02 — Recursive Positional Breakage Lineage  
**Repository:** `maidiu/rawlsing`  
**Exact adjudicated base:** `bf9a0434eb2096d5c4725cf483ec757fd319b6af`  
**Authorized branch:** `agent/vozhd-trii-d02-v548-breakage`  
**Frozen VT3 comparison base:** `8c87f7725ba58202b5377c974548140420709fa9`  
**Production code modified:** `NO`  
**Architecture selected:** `NO`

## 1. Verdict

**VERDICT: `CAPABILITY_MUTATED__V548_DEVIATION_CHASER_BECAME_V550_GREEDY_TOP2_POSITION_TREE__CURRENT_TREE_IS_NOT_LOSSLESS_BRANCH_EVIDENCE__JOINT_RESPONDENT_INCIDENCE_IS_REQUIRED_TO_REGENERATE_THE_DISCOVERY_SPACE`.**

The historical and current objects share a family resemblance but do **not** implement the same empirical question.

Historical V526d explicitly aimed to discover **majority-position deviation, category failure, and deeper breakages**. Executable V548 operationalized that aim by:

1. finding a response majority at the current cohort;
2. choosing a positional predictor;
3. choosing the predictor category that **most strongly carried that majority response**;
4. partitioning the cohort into four `position relation × response relation` quadrants;
5. recursively following only `majority_position_deviation`: respondents in the selected majority-carrying positional category whose response broke from the node majority.

That is not a generic decision tree and not simply “which demographic predicts Y best?” It is a directed search for **where a socially located modal response fails, and whether a new positional channel becomes salient among the failures**.

Current V550 `branch_nodes_rows` does something materially different. At each node it greedily chooses the remaining indicator with the greatest positive reduction in response entropy, keeps only that indicator’s **two most frequent nonblank values**, follows both retained values, removes the selected indicator from the remainder of the path, and stops at default depth 3 or support/no-gain limits. It no longer defines or chases a response-deviation cohort. It no longer emits the historical four quadrants. It no longer stores a full node response distribution or node support. Its branch tree is therefore a **greedy, truncated positional partition search**, not a faithful continuation of V548 recursive positional breakage.

The mutation creates systematic discovery loss:

- balanced XOR and parity-style conjunctions with zero marginal signal stop at the root in current V550;
- third-and-lower-frequency categories disappear from the current tree even when strongly distinctive and sufficiently supported;
- rejected predictors and alternative split paths are never persisted;
- current nodes do not preserve general `P(Y | path)`, because they store only entropy plus the dominant response/share and no node `n`;
- no branch respondent IDs are persisted;
- current internal-node `split_indicator` is overwritten with the **outgoing** split while `split_value` remains the **incoming** path value, so those two fields cease to be a coherent pair on internal nodes;
- `entropy_gain_from_parent` is likewise the gain of the node’s **outgoing** split, not gain from its parent;
- `pure_or_near_pure` is written as a stop reason but does not actually stop recursion;
- tree splitting is unweighted;
- multi-select topology is not rejected inside the branch algorithm.

V548 was also lossy and selective. It did not exhaustively search all subgroup structure. It aggregated every nonselected predictor category into one “minority position” complement, recursively followed only one quadrant, allowed zero-MI predictors to seed arbitrary breakage scaffolds, did not consume V547’s `top_interaction_1`, did not persist respondent IDs, and its checked-in default entry point contains an `OUT_DUCKDB` name defect. The historical capability must therefore not be romanticized into a lossless interaction engine.

**Capability ruling:** socially structured minority departures, conditional reversals, and deeper subgroup forks are real discoverable empirical phenomena, but neither V548 nor current V550 exhausts that discovery space. The current tree loses some capability V548 explicitly represented (response-deviation quadrants and full emitted-node response distributions), gains other coverage (two recursive category branches and broader 12-field candidates), and introduces new truncations. The complete discovery space is reconstructible only from same-respondent response/position incidence plus exact scope, missingness, support, response topology, algorithm parameters and provenance. Whether that capability must be terminally retained is D12 jurisdiction; whether a tree must remain materialized is not decided here.

## 2. Historical purpose

### 2.1 Binding historical design evidence

The preserved historical design extract for `V526d_RECURSIVE_POSITIONAL_BREAKAGE_TREE` states:

- purpose: build recursive trees of **majority indicator, majority-position deviation, category failure, and deeper breakages**;
- required outputs:
  - `recursive_breakage_tree_nodes`
  - `majority_position_deviation_summary`
  - `branch_split_evidence`
- stop conditions:
  - low-N branch without exploratory flag
  - single-label tree used for a multi-select item
- forbidden:
  - no persona assignment.

This sits between historical V526c/V547 determinicity work and V526e/V549 branch co-signature work. V526e’s preserved purpose—discover what else “travels with each branch” and preserve covariance for profile generation—establishes that branch cohorts were intended to be usable **discovery anchors**, not merely a drawing.

The direct historical archive binaries are hash-addressed external evidence in the control surface and were not present as repository files at the adjudicated base. This court therefore does not invent pack details beyond the preserved extract. The executable V548 code is the controlling evidence for what was actually implemented.

### 2.2 The empirical question actually implied by V526d/V548

The closest exact statement is:

> **Within a question-response population, which social position most carries the current modal response; where do respondents inside that position break from the modal response; and, inside those breakages, which positional channel becomes salient next?**

This differs from the candidate interpretations as follows:

| Candidate meaning | Ruling |
|---|---|
| “What demographic variable best predicts response X?” | **PARTIAL ONLY.** Predictor MI is an internal selector, not the historical end object. |
| “Where does the modal response cease to hold?” | **YES, CENTRAL.** V548 explicitly constructs majority-position deviation. |
| “Which positions carry minority departures?” | **YES, BUT SELECTIVE.** It follows departures only inside the one category selected as most majority-conforming. |
| “Once inside a subgroup, which variable becomes salient next?” | **YES.** The deviation subgroup is rescored recursively when it still has multiple response values and enough N. |
| “Which conditional social configurations constitute distinct historical cohorts?” | **PARTIAL.** Emitted quadrants are cohort recipes, but the search is one-sided and complement-aggregating. |
| “Which branch cohorts should become anchors for cotravel analysis?” | **HISTORICALLY YES.** V526e follows V526d with explicit “travels with each branch” language. Current machinery no longer actually uses recursive membership for clouds/co-signatures; see §11. |

### 2.3 A crucial semantic point: V548 “majority position” is not the most prevalent position category

`choose_indicator_value()` does **not** choose the predictor’s modal category. It chooses, among predictor categories with `n >= 10`, the category maximizing:

1. share of the node’s current majority answer;
2. lift of that share over the predictor-complete node baseline;
3. category N.

Thus the V548 “majority position” is better described as the **category most carrying the majority response**, not the numerically largest demographic category.

### 2.4 V547 interaction evidence did not enter V548 recursion

V547 computed:

- `top_predictor_1`;
- `top_interaction_1`;
- `top_interaction_1_gain`;
- `shape_class`, including `interaction`.

V548 consults `top_predictor_1` at depth 0 but never reads `top_interaction_1` or `top_interaction_1_gain`. This is a real capability discontinuity. A pair interaction visible in V547 could fail to guide the V548 recursive search.

## 3. Executable V548 algorithm

Primary implementation evidence:

- `data/ddm_build_copy/build_recursive_breakage_tree_nodes_v548.py`
- blob at adjudicated base: `1fc72071a048cd5f7771a2164de1698e05423f88`

Relevant precursor:

- `data/ddm_build_copy/build_question_determinicity_summary_v547.py`
- blob: `3fc894501ce77c6519a2b32213f3f017465553e5`

### 3.1 Root cohort and scope

For each V547 summary row, V548 derives `var_code` from `question_id` and fetches rows from the live facet-ready view or response/respondent tables using only:

- `source = dataset_scope`;
- `var_code = question var`;
- `value_raw IS NOT NULL`.

The response SQL does **not** filter by `canonical_wave` or country. `canonical_wave` is copied into output metadata from the V547 row, but the V548 data fetch itself is source-wide for that variable.

This means the executable root cohort is:

`all fetched source-family respondents with that var_code`

not provably:

`the canonical_wave/country population named in output metadata`.

V547 exhibits the same scope hazard: it labels the mode `within_country`, but its response load is source/variable scoped and country is itself analyzed as a predictor. Exact historical wave isolation is therefore **not established by executable code**.

### 3.2 Target normalization

`value_raw` is numerically coerced. Codes `-1, -2, 8, 9, 98, 99, 101, 999` become missing.

If the remaining substantive values are a subset of `{0,1}`, the target becomes:

- nonzero → `present`;
- zero → `absent`.

However, in that presence branch, values already converted to `NaN` also map to `absent`. Thus coded missing values can be folded into the `absent` target for binary/presence-like questions. In non-presence mode they remain null and are dropped.

This is an implementation defect relative to typed missingness.

### 3.3 Predictor candidate set

Exactly seven fields:

1. `country_code`
2. `sex`
3. `age_group`
4. `education_level`
5. `income_level`
6. `urban_rural`
7. `religion_label`

`age_group` is generated from age with bins:

- 18–29
- 30–44
- 45–59
- 60+.

### 3.4 Split predictor criterion

`mi_score(feature, target)`:

- joins nonmissing feature/target rows;
- requires at least 50 joined rows;
- requires at least 2 feature values and 2 target values;
- computes unweighted discrete mutual information via `sklearn.feature_selection.mutual_info_classif(..., random_state=0)`.

At depth 0, V548 prefers V547 `top_predictor_1` if it is one of the seven fields and produces a finite MI on the V548 frame. Otherwise, and at every deeper level, all candidate fields are rescored and the greatest MI is selected, with field-name ordering breaking exact score ties.

**Previously used predictors are not removed.** The same predictor may be chosen again deeper if it remains variable in the recursive cohort.

**Zero MI is still finite.** V548 does not require positive signal before expansion. Therefore a variable with exactly zero MI can still become the split predictor and generate a tree.

### 3.5 Category selection

Given selected predictor `X` and node-majority response `M`, V548 considers each `X=value` with `n >= 10` and chooses the value maximizing:

`(P(Y=M | X=value), lift over predictor-complete P(Y=M), n)`.

It therefore picks the category most conforming to the node majority.

### 3.6 Four-way branch construction

Let selected category be `X=v` and node majority response be `M`.

V548 emits up to four nonempty child cohorts:

1. `majority_position_conformity`
   - `X=v AND Y=M`
2. `majority_position_deviation`
   - `X=v AND Y!=M`
3. `minority_position_convergence`
   - `X!=v AND Y=M`
4. `minority_position_divergence`
   - `X!=v AND Y!=M`

The “minority position” side is **the complement of one selected category**, not a list of named minority categories. Blank/string-missing categories may remain in that complement; numeric missing values stringify as nonmatching values in the branch mask.

### 3.7 Recursive continuation rule

Only `majority_position_deviation` is eligible for recursive expansion.

The recursive call occurs when:

- branch `n >= 50`;
- `depth + 1 < 5`.

At the recursive node, the response majority is recomputed inside the already-deviant cohort, predictors are rescored, and the procedure repeats.

This yields an important consequence:

**For a binary target, the first `Y != M` branch is single-target and cannot recurse meaningfully.** Deep recursion is primarily possible for questions with three or more response states, where deviation from the first mode can still contain multiple answers.

`removed_answers` is carried in metadata but is not itself used to filter rows; row filtering is accomplished by the nested branch subsets.

### 3.8 Maximum depth and support law

Constants:

- split threshold: `MIN_NODE_N_FOR_SPLIT = 50`;
- category inference threshold: `MIN_OPTION_N_FOR_CHANNEL_INFERENCE = 10`;
- report-only marker: `MIN_NODE_N_REPORT_ONLY = 25`;
- `MAX_DEPTH = 5`.

Nonempty child branch summaries are emitted even when below split support; they simply do not recurse. This is materially different from current V550 child omission.

### 3.9 Weighting

V548 is unweighted.

- `weighted_n` is literally `float(n)`;
- output limitations explicitly say `exploratory_unweighted`.

### 3.10 Node identity and persisted information

Each node stores:

- tree/node/parent ID;
- depth;
- canonical-wave metadata;
- `conditions_json`;
- complete `response_distribution_json` with response counts and shares;
- selected next predictor/category;
- branch type;
- `n`;
- `weighted_n`;
- stop reason;
- heuristic confidence.

`conditions_json` includes the node’s current majority response, chosen predictor, predictor MI, chosen category, category N/share/lift, branch type, and metadata.

But V548 node IDs use only branch-type path segments such as:

`question::majority_position_deviation/...`

They do **not** encode predictor/value predicates. An emitted cohort recipe can be reconstructed only by walking the parent chain and interpreting each parent’s chosen predictor/category/majority response together with the child branch type.

No respondent IDs are persisted.

### 3.11 Checked-in executable defect

At the adjudicated SHA, default `main()` contains:

`if OUT_DUCKDB.exists():`

but the file defines `DUCKDB_PATH`, not `OUT_DUCKDB`.

Therefore a clean non-`--append` invocation of the checked-in file would raise `NameError` before entering the question loop. The `--append` path does not execute that reference, and the core builder functions are otherwise callable.

No repository-local V548 run receipt was available to prove whether historical production output came from:

- an earlier revision without this defect;
- an append-mode launch;
- a direct function invocation;
- or another execution copy.

Accordingly:

- **algorithm semantics above = PROVEN from code**;
- **successful historical clean-run behavior of this exact checked-in file = NOT PROVEN**.

### 3.12 Multi-select stop law was not implemented

Historical V526d explicitly names “single-label tree used for multi-select item” as a stop condition.

V548 does not inspect question topology or multi-select status. It operates row-wise on one numeric `value_raw` per response row. If a multi-select question is represented by multiple rows per respondent, V548 does not protect against treating those rows as independent observations.

This is a direct implementation gap against historical design intent.

## 4. Current V550 algorithm

Primary implementation evidence:

- `data/ddm_build_copy/ddm_v550_branching.py`
- blob: `8f6d40e0d016d66e5a3b334b31747eaef752873f`

Support:

- `data/ddm_build_copy/ddm_v550_support.py`
- blob: `1b841139fee051b154dcccd52cd3d866b958dbb5`

Production shard orchestration:

- `data/ddm_build_copy/build_determinicity_wave_shard_v550.py`
- blob: `82ffc18df29a8e5ebd78cde97c89d463b3842df6`

Shared checkpoint helpers:

- `data/ddm_build_copy/build_determinicity_repository_v550.py`
- blob: `04f3a3646d8b468660385087d92541f03f860cb0`

### 4.1 Root scope

Current V550 question rows are built and prefetched at explicit:

- source;
- wave/canonical-wave aliases;
- country;
- question variable aliases.

`_question_rows()` filters source + canonical wave + country + variable. `_prefetch_question_rows_by_country()` likewise filters source + wave + country and selected variables, then `_question_rows_from_cache()` slices the question.

This is materially better scoped than executable V548’s source-wide question fetch.

### 4.2 Candidate predictor set

Current `INDICATOR_FIELDS` contains twelve fields:

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

### 4.3 Effective support threshold

`branch_nodes_rows(..., min_branch_n=DEFAULT_SUPPORT_CAP)` does not use `min_branch_n` as a fixed minimum. It passes it as the cap to:

`ceil(n_respondents * 0.005)`, bounded by:

- floor 2;
- cap 30 by default.

Examples under defaults:

- N=100 → threshold 2
- N=1,000 → 5
- N=10,000 → 30
- missing/invalid N → 30.

### 4.4 Literal recursive trace

At every node:

1. `Y = response_value_normalized` as string.
2. Compute unweighted:
   - dominant response;
   - dominant-response share;
   - response entropy.
3. Append a node row.
4. If depth/support/indicator availability permits, evaluate every remaining indicator:
   - convert indicator nulls to blank string;
   - exclude blanks from the candidate’s conditional-entropy calculation;
   - skip candidate if its nonblank support is below threshold;
   - compute `gain = H(Y on full node) - H(Y | X on X-nonblank rows)`.
5. Select only the candidate with strictly greatest positive gain.
   - ties remain with the earlier `INDICATOR_FIELDS` field because replacement is only on `gain > best_gain`.
6. Remove the chosen indicator from future candidates on that path.
7. Take only the two most frequent nonblank values of the chosen indicator.
8. For each retained value whose child support meets threshold:
   - recurse into `X=value`.
9. Stop by default at depth 3, under support, no remaining indicators, or no positive gain.

### 4.5 Current recursion is not historical deviation recursion

The path predicate is positional:

`X1=v1 AND X2=v2 ...`

The response is measured inside the node but does not define child membership.

There are no current equivalents of:

- majority-position conformity;
- majority-position deviation;
- minority-position convergence;
- minority-position divergence.

Current `branch_type` is merely:

- root: `conforms`;
- descendants: `split`.

The root label `conforms` is not tied to a conformity test.

### 4.6 Current child coverage

Only two values are followed, selected by **frequency**, not response distinctiveness.

Consequences:

- third-and-lower-frequency values vanish from the recursive tree;
- blank/missing selected-indicator rows remain in the parent calculation but belong to no child;
- a rare but highly distinctive category can drive the split’s entropy gain yet still be omitted from all children if it is not top-two by frequency.

### 4.7 Current node information

Branch-specific fields are:

- `node_id`
- `parent_node_id`
- `branch_depth`
- `split_indicator`
- `split_value`
- `node_entropy`
- `entropy_gain_from_parent`
- `stop_reason`
- `branch_type`
- `dominant_response`
- `dominant_response_pct`

plus repeated question metadata.

There is no node-level:

- `n_unweighted`;
- `n_weighted`;
- full response distribution;
- candidate predictor list;
- rejected score list;
- unexpanded category list;
- respondent-membership list;
- effective support threshold;
- explicit algorithm-parameter/version field.

### 4.8 Internal-node field inconsistency

A child node is initially appended with:

- `split_indicator = incoming path indicator`;
- `split_value = incoming path value`.

If that node itself finds a split, code overwrites:

- `split_indicator = outgoing best indicator`;
- `entropy_gain_from_parent = outgoing split gain`;

but does **not** replace `split_value`.

Thus an internal row can contain a nonsensical pair such as:

- `split_indicator = sex` (outgoing);
- `split_value = high` (incoming age-group value).

The accurate positional path is held in `node_id`, not reliably in the internal row’s `split_indicator/split_value` pair.

Similarly, `entropy_gain_from_parent` is misnamed: on a splitting node it is gain **from splitting that node**, not gain inherited from its parent.

### 4.9 `pure_or_near_pure` does not stop

A node with dominant-response share `>= 0.95` is initially labeled:

`stop_reason = pure_or_near_pure`

but the function does not return on that condition. If depth/support/available indicators permit and a positive gain is found, it continues recursion while retaining a “stop” reason.

The field is therefore not a reliable terminal-node indicator.

### 4.10 Missingness and entropy-universe mismatch

For each candidate predictor:

- node entropy is calculated over all node responses;
- conditional entropy is calculated only over rows where that predictor is nonblank.

These are different populations when predictor missingness exists.

The resulting `gain` is not, in that case, a standard same-universe `H(Y)-H(Y|X)` quantity and can partly reflect missingness/completeness composition.

Missing selected-indicator rows are not assigned a typed missing child.

### 4.11 Weighting

The recursive tree is wholly unweighted.

Current `outlier_cohort_rows` does compute `n_weighted` when `weight_value` exists, but:

- baseline dominant response is unweighted;
- subgroup dominant response is unweighted;
- branch classification is unweighted.

So weights do not change current tree topology or current outlier branch type.

### 4.12 Multi-select/non-simple response topology

`branch_nodes_rows` has no topology gate and no respondent deduplication.

Current `_question_rows_from_cache()` can explicitly combine multiple child variables for an `explicit_multiselect_children` mapping. If that produces multiple response rows for the same respondent, the branch tree counts those rows; it does not turn them into a respondent-level multi-select set.

Whether a particular governed question is prevented upstream from reaching this computation is D06 authority jurisdiction. The branch function itself is **not multi-select safe**.

### 4.13 Persistence

Production shard execution:

1. computes `branch_df = prepare_question_frame(df)`;
2. calls `branch_nodes_rows(...)`;
3. writes `recursive_branch_nodes` to a per-question Parquet checkpoint;
4. marks question completion separately;
5. finalizes wave tables from memory or checkpoint reload;
6. writes `recursive_branch_nodes` as a normal determinicity output;
7. serializes it into the V550→V551 bridge under empirical object type `recursive_branch` and evidence lane `derived_determinicity`.

The output has no dedicated static Arrow schema; it is written with dynamically inferred structure.

## 5. Lineage matrix

Classification vocabulary follows this court’s assignment: `PRESERVED`, `MUTATED`, `DROPPED`, `MORE_LOSSY`, `LESS_LOSSY`, `UNKNOWN`. Multiple labels are used when a behavior changes in more than one direction.

| Behavior | V548 | Current V550 | Classification |
|---|---|---|---|
| Core search target | majority-carrying position → response deviation → deeper breakage | greedy positive entropy-gain positional partition | **MUTATED** |
| Root scope | source + var_code fetch; wave only metadata | source + wave + country + question aliases | **LESS_LOSSY / MUTATED** |
| Position candidates | 7 fields | 12 fields | **MUTATED / LESS_LOSSY** for candidate breadth |
| V547 root predictor hint | consumed | no V547 dependency | **DROPPED** |
| V547 pair-interaction hint | not consumed | not consumed by tree | **PRESERVED** absence |
| Predictor score | unweighted sklearn discrete MI | unweighted entropy reduction | **MUTATED** |
| Positive-signal requirement | finite MI; zero MI can split | strictly positive gain required | **MUTATED** |
| Chosen category | max majority-response conformity/lift, n>=10 | top two categories by frequency after predictor selection | **MUTATED** |
| Response-defined branches | 4 explicit position×response quadrants | none | **DROPPED** |
| Recursive children | one: majority-position deviation | both retained top-two position values | **MUTATED / LESS_LOSSY** across the retained two values |
| Other category coverage | complement aggregated into two branch summaries | third+ categories omitted from tree | **MORE_LOSSY** for category existence/identity in tree |
| Same predictor may recur | yes | no, removed after split | **MUTATED / MORE_LOSSY** for repeated/nonstationary use |
| Max depth | 5 | default 3 | **MORE_LOSSY** |
| Split support | fixed 50 | wave-relative 2..30 default | **MUTATED / LESS_LOSSY** for many small retained top-two branches |
| Tiny nonempty branch summary | emitted after an expanded parent | child omitted if below current support | **MORE_LOSSY** in current tree |
| Weighting | unweighted | unweighted | **PRESERVED** |
| Full node response distribution | yes | no | **DROPPED / MORE_LOSSY** |
| Node support N | yes | no | **DROPPED / MORE_LOSSY** |
| Chosen split score | chosen MI in JSON | chosen entropy gain | **PRESERVED / MUTATED** |
| Rejected candidate scores | no | no | **PRESERVED** absence |
| Branch respondent IDs | no | no | **PRESERVED** absence |
| Cohort path ID | branch-type-only; predicate requires parent JSON | indicator/value path encoded in node ID | **LESS_LOSSY**, subject to delimiter ambiguity |
| Internal split field coherence | parent JSON defines split semantics | internal `split_indicator/split_value` can mismatch incoming/outgoing semantics | **MORE_LOSSY / MUTATED** |
| Missing position handling | blank may become category/complement; binary target missing can become absent | blank excluded from candidate and from child descent; node entropy still includes it | **MUTATED**, both lossy differently |
| Multi-select stop | design required; executable does not enforce | branch function does not enforce | **PRESERVED** implementation gap |
| Clean executable entry point | default path has undefined `OUT_DUCKDB` at adjudicated SHA | production shard path active | **LESS_LOSSY** operationally, historical run status **UNKNOWN** |
| Persistence | CSV + DuckDB + YAML/report intent | per-question Parquet checkpoints + final determinicity + bridge | **MUTATED** |
| Cloud/co-signature membership use | historical successor intent was “with each branch” | current cloud/signature builders receive full question frame, not recursive nodes | **DROPPED / MUTATED** relation; D03 owns full adjudication |

## 6. Branch information-content matrix

| Information/question | V548 emitted tree | Current V550 tree | Ruling |
|---|---|---|---|
| `P(Y | emitted node)` | **YES**: full response counts/shares in `response_distribution_json` | **NO in general**: entropy + dominant response/share only | Current is more lossy |
| Binary `P(Y | node)` | yes | proportions can be inferred from dominant label/share only if response topology is known to be exactly binary | Conditional special case; still no node N |
| Node support N | yes | no | Current cannot audit exact branch support from node row |
| Weighted `P(Y | node)` | no | no | Neither tree |
| Selected predictor | yes | yes | Current internal-row field is outgoing split; node ID needed for incoming path |
| Selected category | yes | yes for path, but internal row split fields can mismatch | Current path is clearer in node ID |
| All candidate predictors considered | no | no | Not reconstructible from trees |
| Rejected splits/scores | no | no | Not reconstructible |
| All categories of chosen predictor | no: one selected category + complement aggregation | no: top two only | Both lossy differently |
| Identity of every nonselected category | no | no | Requires deeper incidence/matrix |
| Full response topology of every branch | emitted V548 nodes only | no | Current loses |
| Exact branch respondent IDs | no | no | Requires source/respondent incidence |
| Alternative greedy paths | no | no | Requires recomputation under alternate choices |
| Three-way conjunction path | possible only along V548 deviation chain and includes response predicates | possible up to depth 3 if each greedy marginal gain is positive and categories survive top-two/support | Neither is exhaustive |
| Zero-marginal XOR/parity interaction | not identified as interaction; V548 may create arbitrary zero-MI first split and quadrant summaries | root `no_gain` | Not preserved as recursive discovery |
| Original same-respondent joint incidence | no | no | Cannot be reconstructed from node summaries |
| Cohort-definition recipe | yes, by parent-chain interpretation | yes for emitted positional path mainly via `node_id` | Neither equals persisted membership |
| Exact run algorithm parameters | constants implicit in historical code | max depth/support cap may be CLI-overridden and are not node fields | Node files alone insufficient for exact current replay |
| Typed missingness of predictors | no | no | Lost as branch semantics |
| Multi-select respondent set topology | no | no | Row-wise tree is insufficient |

### 6.1 What current tree nodes uniquely contain

Current nodes uniquely materialize a **greedy decision trace**: which split happened on this run and which two category paths were expanded.

They do **not** uniquely contain an empirical fact unavailable in respondent incidence. Given the exact scoped respondent frame, position fields, response normalization, algorithm version, candidate order, support rule and runtime parameters, the tree is recomputable.

But the inverse is false: the current node table cannot reconstruct the respondent frame or all alternative empirical subgroup facts.

## 7. Respondent-membership ruling

**RULING: `MEMBERSHIP_NOT_PERSISTED__EMITTED_COHORT_RECIPE_ONLY`.**

### 7.1 V548

No respondent IDs are stored.

Membership of an emitted child can be reconstructed from original respondent data only by composing parent decisions:

- parent predictor `X`;
- parent selected value `v`;
- parent majority response `M`;
- child `branch_type`.

For recursive descendants, all ancestor predicates must be composed.

Because V548 node IDs contain only branch-type names, a node ID alone is insufficient. The full parent chain plus `conditions_json` plus exact source data is required.

### 7.2 Current V550

No respondent IDs are stored.

For a normally encoded value, `node_id` contains the positional conjunction:

`question::indicator/value/indicator/value/...`

so emitted branch membership can be regenerated against the original scoped respondent frame.

Caveats:

- current path values are inserted into the slash-delimited ID without escaping; values containing `/` can make parsing ambiguous;
- internal `split_indicator/split_value` fields are not reliable as a pair once a node itself splits;
- rows with missing selected-indicator values belong to the parent but to no child;
- the recipe identifies only emitted paths, not unexpanded categories or alternate predictors.

Thus “branch membership” is a **regenerable recipe for emitted cohorts**, not a persisted empirical membership relation.

## 8. Hostile fixture results

The fixtures below were evaluated against the literal algorithms. Synthetic cases are discovery tests, not claims about any real survey population.

| Fixture | V548 result | Current V550 result | Court ruling |
|---|---|---|---|
| **A. Balanced XOR**: A and B individually independent of Y; A×B determines Y | V547 can detect the pair interaction, but V548 ignores `top_interaction_1`. V548 accepts a finite zero-MI predictor, chooses an arbitrary tied category, and emits four A×response quadrants. For binary Y the deviation branch is then single-target, so B never emerges recursively. | Every unary entropy gain is 0. Literal synthetic run produced one root node with `stop_reason=no_gain`. | **FAIL as interaction discovery in both trees.** V548 surfaces a response-deviation partition but not the XOR relation; current tree misses it entirely. |
| **B. Simpson reversal** | One selected majority-carrying category is explicit; all other predictor categories are complement-aggregated, and only one response-deviation quadrant recurses. It cannot systematically represent all strata needed to prove a reversal. | **Conditionally discoverable, not guaranteed.** In a 3-stratum synthetic reversal, current V550 selected the stratifier and expanded its two most frequent strata, then the second predictor; the third stratum was omitted. A two-stratum, well-supported case can be exposed, but general stratified reversal is not preserved. | **PARTIAL / NON-EXHAUSTIVE.** Greedy top-two branching cannot be relied on as a Simpson detector. |
| **C. Tiny stable minority / third category** | Rare/nonselected categories are merged into the `X!=v` complement. Their existence may influence a minority divergence summary, but category identity is not retained, and categories under n=10 cannot be chosen as the majority channel. | In a synthetic 1000-row case with category counts 450/450/100 and the 100-row category carrying the opposite response, threshold=5. The tree selected the predictor but emitted only the 450 and 450 children; the distinctive 100-row category vanished from the tree. `outlier_cohort_rows` would still emit a unary row for it because n=100>=5. | **CURRENT TREE FAIL.** Separate outlier output partially mitigates unary visibility, not recursive discovery. |
| **D. Three-way parity**: no unary or pair marginal signal; A×B×C determines Y | Zero-MI first split can occur, but response-defined binary deviation immediately becomes single-target; deeper B/C relationship is not discovered. | Literal synthetic run stopped at root with `no_gain`. | **FAIL both.** |
| **E. Nonmonotonic subgroup**: A matters overall; inside A=a B matters; inside B=b the A contrast reverses | V548 sees only the selected A category’s response-deviation lane recursively. Other A categories are complement summaries, so cross-A reversal under B is not generally represented. | With binary/top-two A and B, sufficient support, and positive gains, the tree can materialize the four positional cells through hierarchical paths, making a reversal inspectable by cross-branch comparison. It does not explicitly encode “reversal,” and it fails when a needed category is not top-two, a needed marginal gain is zero, or the conjunction exceeds depth. | **CONDITIONAL PASS ONLY for favorable low-cardinality cases; systematic capability absent.** |
| **F. Contradictory simultaneous positions** | One predictor/category is privileged as majority channel; all others are secondary recursion only inside one deviation lane. | Positions can coexist on a path if selected serially, but one greedy hierarchy decides which relations become visible. Weak-but-contradictory simultaneous coordinates can disappear if they do not add local entropy gain. | **FAIL as exhaustive simultaneous-position discovery.** Neither tree may be treated as actor identity. |
| **G. Multi-select / non-simple topology** | Historical design said stop; executable V548 does not. Multiple response rows per respondent are counted row-wise. | Branch function has no topology gate or respondent dedupe. `explicit_multiselect_children` can yield several rows per respondent, which the tree will count separately. | **FAIL/UNSAFE unless upstream authority guarantees a one-row-per-respondent scalar target.** |

### 8.1 Supplemental hostile findings

**Weighted reversal.** Both V548 and current V550 recursive trees follow unweighted response structure. A population in which 8/10 rows say Yes with small weights and 2/10 say No with large weights will be tree-majority Yes even if weighted mass is overwhelmingly No.

**Missingness.** Current V550 can compare full-node `H(Y)` with conditional entropy on a predictor-complete subset, so measured gain can partly reflect missingness composition. V548 can treat blank string positions as actual category candidates/complement members, while presence-target normalization can turn coded response missing into `absent`.

**One-person branch.** Once V548 has expanded a parent, a nonempty one-person quadrant is still emitted as report-only. Current V550’s support floor is 2, so an n=1 child is omitted from both recursive descent and current outlier cohort emission.

## 9. Rare/minority preservation ruling

**RULING: `V548_PRESERVES_RESPONSE_DEVIATION_EXISTENCE_BETTER_THAN_CATEGORY_IDENTITY__V550_PRESERVES_TWO_COMMON_CATEGORY_PATHS_BETTER_THAN_RARE_TREE_COVERAGE`.**

V548’s strength is that, once a parent qualifies for expansion, it emits every nonempty response-position quadrant, even underpowered ones. This makes the existence of a tiny response deviation visible.

Its weakness is positional identity:

- only one predictor category is named as the selected majority channel;
- all other categories collapse into `X!=v`;
- rare categories below n=10 cannot become the selected channel;
- only one deviation quadrant recurses.

Current V550’s strength is different:

- both top-two category values can recurse;
- the support threshold is often far below V548’s fixed 50.

Its weakness is categorical truncation:

- third-and-lower-frequency categories disappear from the tree;
- categories under the wave-relative threshold disappear;
- missing category is not represented as a child;
- no summary node records omitted categories.

`outlier_cohort_rows` partially recovers **unary** supported rare-category visibility because it loops all indicator values above the support threshold. It does not restore:

- recursive membership;
- full subgroup response distribution;
- conjunction paths;
- below-threshold category existence.

Therefore current rare/minority preservation cannot be adjudicated by the recursive tree alone; the tree systematically loses classes of socially meaningful minority structure.

## 10. Weight/support/missingness ruling

### 10.1 Weighting

- V548 recursion: unweighted.
- Current V550 recursion: unweighted.
- Current outlier cohort:
  - stores weighted N where available;
  - still chooses dominant response and branch type unweighted.

**Holding:** neither tree supports a claim that its branch topology is population-weighted structural truth.

### 10.2 Support

V548 has three fixed thresholds:

- n=50 split;
- n=10 category-channel inference;
- n=25 report-only label.

Current V550 uses one wave-relative branch threshold:

`min(30, max(2, ceil(0.005 * question_n)))`

under defaults.

The current policy is less suppressive for many small top-two branches, but support cannot rescue categories discarded by the top-two rule.

The CLI option `--min-branch-n` is semantically a **cap** in the call path, not a direct fixed minimum.

### 10.3 Missingness

Neither implementation has lawful typed branch missingness.

V548:
- numeric position nulls are dropped for predictor scoring/category selection;
- several string position fields convert null to blank string, which may be treated as an ordinary category;
- complement branch masks can absorb missing values;
- binary target normalization can convert coded missing response to `absent`.

Current V550:
- indicator blank is excluded from candidate conditional entropy;
- node entropy still includes its response;
- missing selected-indicator rows get no child;
- no `missing/unknown/not-asked/inapplicable` branch state is emitted.

**Holding:** exact replay and any future reconstruction of socially meaningful missingness require the underlying respondent-level typed state; tree nodes do not preserve it.

## 11. Relationship to downstream cloud/co-signature machinery

Current cloud/signature code:

- `data/ddm_build_copy/ddm_v550_clouds.py`
- blob: `dfc878e87d984a1a3d7000a0c726bdc444f9945f`

### 11.1 Current branch position signatures do not consume recursive branches

Production shard orchestration calls:

- `build_position_signature_rows(branch_df, question_meta)`
- `build_co_signature_rows(branch_df, question_meta)`
- `build_attitude_cloud_rows(branch_df, question_meta)`

using the **full prepared question frame**.

It does not pass `recursive_branch_nodes` or a recursive branch-member relation.

`build_position_signature_rows` sets:

- `branch_id = anchor_question_id`;
- `branch_key = source::wave::country::anchor_question`;

then ranks position-coordinate features against the question response across the full question frame.

Thus current “branch position signature” is **not a signature of a recursive branch cohort**.

### 11.2 Current relation co-signatures do not consume recursive branches

`build_co_signature_rows` uses the same question frame and the same question-level `branch_id`/`branch_key` pattern. It ranks eligible relation-evidence columns against the question response. No recursive node membership is used.

### 11.3 Current attitude cloud uses same-respondent cross-question incidence, not branch membership

`build_attitude_cloud_rows` prepares per-question frames keyed by `respondent_id`, deduplicates a respondent to one row per question frame, and joins anchor/candidate question frames by respondent ID.

This is genuine same-person cotravel computation, but it is question-response cotravel—not cotravel inside a recursive positional branch.

### 11.4 Bridge status

`ddm_v550_bridge.py` still maps:

`recursive_branch_nodes -> recursive_branch -> derived_determinicity`.

That proves current branch rows are indexed into the bridge, not that a terminal consumer needs their branch semantics.

### 11.5 D03 flag

Historical V526e/V549 intended “what else travels with each branch.” Current V550 cloud/co-signature functions use question-level/full-frame or cross-question respondent incidence rather than recursive branch membership.

This is a **material lineage discontinuity that D03 must adjudicate**:

- whether historical branch-level cotravel was intentionally superseded;
- whether current question-response cotravel preserves the intended capability;
- whether a branch-conditioned cloud exists anywhere else;
- whether “branch” survives only in artifact names.

D02 does not decide D03’s jurisdiction.

## 12. Reconstructibility statement

### 12.1 Exact underlying information needed

To regenerate current V550 branch discoveries, the empirical substrate must provide, at the exact question scope:

- respondent identity or losslessly equivalent same-row incidence;
- exact source;
- exact raw/canonical wave;
- country;
- question/variable identity and alias resolution;
- normalized response with response-topology/typed-state semantics;
- the available V550 position fields with exact values and missingness;
- question `n_respondents`;
- the precise population included in the branch frame.

Exact algorithmic replay additionally requires:

- `INDICATOR_FIELDS` order;
- current entropy/dominant-response implementations;
- support formula/version;
- actual `max_depth`;
- actual `min_branch_n`/support-cap parameter;
- missingness normalization behavior;
- software/tie behavior sufficient for deterministic ordering.

To regenerate V548 exactly, one additionally needs:

- V547 summary row, especially `top_predictor_1`;
- V548’s historical seven fields and age binning;
- original numeric `value_raw`;
- historical missing-code handling;
- source-wide question population actually fetched by V548;
- row/order behavior for ties;
- V548 constants and code version.

### 12.2 Do current branch nodes uniquely contain any required empirical information?

**No.**

They contain a materialized search decision trace, not irreducible empirical evidence.

Every current branch node can in principle be recomputed from richer same-respondent response/position incidence plus exact algorithm/provenance. Conversely, the node table cannot reconstruct:

- rejected predictors;
- unexpanded categories;
- all joint cells;
- respondent IDs;
- full response distributions;
- original missingness;
- arbitrary alternative branch paths.

### 12.3 Is current source/respondent incidence sufficient to regenerate branches?

**Information-theoretically yes, if retained at sufficient fidelity and paired with exact replay authority.**

Current V550’s shared respondent substrate deserves a precise caveat:

- `canonicalize_shared_respondent_substrate()` returns required columns **plus all original extra columns**, so position fields present in the prepared input frame can physically survive into the Parquet cache;
- however `SHARED_SUBSTRATE_REQUIRED_COLUMNS` does not require the 12 branch position coordinates;
- `LOGICAL_CONTENT_COLUMNS` equals only those required columns;
- the substrate logical content hash therefore does not protect the extra position-coordinate columns.

So the current shared substrate may physically carry enough information in a given run, but **its contract does not prove or hash-protect exact branch replay capability**.

The deeper facet/source database can regenerate the branch frame if its respondent incidence, positions, response semantics, scope and provenance remain reconstructible. D05 and D13 must prove that physical equivalence; D02 does not assume it.

### 12.4 Current persisted branch nodes are not enough for exact source reconstruction

Even with all current branch nodes, there are many distinct respondent-level datasets that produce the same tree. Therefore:

`TREE -> SOURCE INCIDENCE` is non-invertible.

But:

`SOURCE INCIDENCE + EXACT ALGORITHM/PARAMETERS -> TREE`

is reconstructible.

This is the core information-loss ruling.

## 13. Open questions

1. **Historical run receipt:** Did an earlier V548 revision or append-mode invocation successfully produce the historical V548 artifact? The checked-in default entry point at the adjudicated base has the undefined `OUT_DUCKDB` defect.
2. **Historical binary archive detail:** The original V526d pack is external hash-addressed evidence. This court used the preserved exact extract; any additional pack-specific semantics not in that extract remain unadjudicated.
3. **Historical scope intent versus executable scope:** Was source-wide mixing across canonical waves intentional, or a bug masked by source-variable naming? Current executable evidence does not prove wave isolation.
4. **Current delimiter safety:** Do any real current indicator values contain `/` or other path-delimiter content that makes `node_id` path parsing ambiguous?
5. **Current multi-select admission:** Does current R1 question-use authority prevent all multi-select/non-simple questions from reaching `branch_nodes_rows`, despite the function itself lacking a topology guard? D06 should answer.
6. **Current branch bridge consumption:** Which V551/V552/current downstream components materially read the `recursive_branch` / `derived_determinicity` bridge rows? D11 owns the full current consumer trace.
7. **Branch-conditioned cotravel:** Does any current code outside `ddm_v550_clouds.py` compute cotravel conditioned on actual recursive membership? D03 should search exhaustively.
8. **Exact replay parameters:** Are `max_depth` and `min_branch_n` persisted in a shard plan/launch receipt strongly enough to reproduce a historical tree when nondefaults are used?
9. **Actual source completeness:** Does the live/source-equivalent substrate preserve all 12 position coordinates, response topology, typed missingness and respondent joins for every governed wave? D05/D13 jurisdiction.
10. **Terminal necessity:** Which classes of breakage discovery actually starve V3/V2 if unavailable? D12 jurisdiction.

## 14. Exact implications for D08/D12/D13

### 14.1 D08 — conditional empirical evidence ↔ attitude-cloud separation/unification

D08 must not treat “branch” as one empirical primitive.

D02 establishes at least three distinct predicates/data operations:

1. positional condition:
   - `P(Y_response | position predicates, scope)`
2. response-conditioned positional breakage:
   - historical V548 cohorts such as `position=X AND Y!=modal_Y`
3. same-person response cotravel:
   - `P(Y_response | X_response, same respondent, scope)`

Current attitude clouds implement (3) through respondent joins. Current recursive V550 tree implements a selected/truncated search over (1). Historical V548 mixed position and response predicates as discovery cohorts.

Therefore D08 must test whether one deeper predicate algebra can represent all three **without erasing denominator, response-topology, same-respondent, and admission distinctions**. The fact that current cloud files use the word “branch” is no evidence of semantic identity.

### 14.2 D12 — terminal human-capability backward court

D12 must evaluate the **capability**, not the current tree artifact.

The candidate capability exposed by D02 is:

> discover supported conditional social configurations in which population response structure departs from its broader pattern, including minority departures, reversals and deeper intersections, without converting those associations into actor identity or destiny.

D12 must separately classify:

- unary conditioned distributions;
- conjunction-conditioned distributions;
- zero-marginal interactions;
- minority/rare configurations;
- response-conditioned breakage searches;
- branch-conditioned cotravel, if D03 proves it distinct.

A finding that `recursive_branch_nodes` is lossy/regenerable cannot by itself classify branch-discovery capability as terminally unnecessary. Conversely, historical V526d intent cannot prove terminal necessity.

Concrete starvation test required from D12:

- construct a terminal historical-life case whose lawful output changes when the relevant subgroup/joint evidence is unavailable;
- then determine whether the needed distinction is supplied by a tree, by a deeper conditional fact, by cotravel evidence, or by another accepted mechanism.

### 14.3 D13 — physical retention and exact replay proof

D13 must prove **same-respondent joint incidence**, not merely retain present tree files or unary marginals.

To replay the discovery classes exposed here, the physical substrate must preserve or exactly regenerate:

- respondent/question incidence;
- all governed position coordinates used by future searches;
- full response topology;
- typed missingness/routing states;
- source/wave/country identity;
- weights even though the current tree ignores them, because future lawful evidence may not;
- exact transformations/aliases;
- support/provenance;
- deterministic algorithm/version parameters.

D02 specifically warns D13 that the current shared respondent substrate’s logical hash does **not** include the branch position-coordinate extras, even though the Parquet writer may physically retain them. A retention proof that points only to that cache’s current physical columns is insufficient unless those columns become contractually required and hash-equivalent to source truth or the deeper source capsule can deterministically regenerate them.

The no-loss condition is therefore:

`RETAINED PHYSICAL AUTHORITY -> EXACT SAME-RESPONDENT RESPONSE/POSITION INCIDENCE -> REPLAYABLE LAWFUL BREAKAGE/CONJUNCTION DISCOVERY`

not:

`RETAIN CURRENT RECURSIVE TREE FILE`.

D13 must also preserve enough launch provenance to replay the **actual historical algorithm parameters** where byte/decision-trace reproducibility is required.

---

## Evidence ledger

### Current/base evidence directly inspected

- `data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/README.md`
- `00_FULL_MACHINE_VISION.md`
- `01_FINDINGS_LEDGER.md`
- `02_RESOURCE_INDEX.md`
- `03_ASSUMPTION_AND_UNKNOWN_REGISTER.md`
- `04_DISCOVERY_COURTS_REGISTER.md`
- `05_DECISION_PROTOCOL.md`
- `06_FIRST_WAVE_LAUNCH_REGISTER.md`
- `evidence/HISTORICAL_DESIGN_EXTRACTS.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md`
- `TERMINAL_DEMAND_ENVELOPE.md`
- `ARCHITECTURE_PASS_LAW.md`
- `data/ddm_build_copy/build_question_determinicity_summary_v547.py`
- `data/ddm_build_copy/build_recursive_breakage_tree_nodes_v548.py`
- `data/ddm_build_copy/ddm_v550_branching.py`
- `data/ddm_build_copy/ddm_v550_metrics.py`
- `data/ddm_build_copy/ddm_v550_support.py`
- `data/ddm_build_copy/build_determinicity_repository_v550.py`
- `data/ddm_build_copy/build_determinicity_wave_shard_v550.py`
- `data/ddm_build_copy/ddm_v550_clouds.py`
- `data/ddm_build_copy/ddm_v550_bridge.py`
- `data/ddm_build_copy/ddm_v550_schema.py`
- `data/ddm_build_copy/ddm_v550_shared_respondent_substrate.py`

### Frozen VT3 comparison evidence

Read as frozen comparison evidence, not current implementation authority:

- VT3-CM-R00 synthesis
- VT3-CM-R02 information-loss court
- VT3-CM-R05 compute/cardinality court
- VT3-CM-R07 hostile no-loss court

The frozen chamber’s claims that recursive trees are lossy analytical projections and that same-respondent joint incidence is required for arbitrary conjunction replay are **consistent with** this D02 reconstruction. D02 adds the historical V548 deviation semantics, current V550 literal implementation defects, rare-category/top-two loss, cloud-membership discontinuity, and the current shared-substrate hash caveat.
