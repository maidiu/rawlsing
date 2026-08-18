# D04 — Current V550 Attitude-Cloud Correctness & Completeness Court

**Court:** VOZHD TRII D04  
**Repository:** `maidiu/rawlsing`  
**Accepted parent discovery-control base:** `7ea5962f644ad796064e30ffafb46f2c077404b9`  
**Work branch:** `agent/vozhd-trii-d04-cloud-correctness`  
**Binding predecessor:** D03 `RESULT.md` + `RESULT.json` at the same accepted base  
**Disposition:** `FAIL_WITH_MATERIAL_IMPLEMENTATION_DEFECTS_AND_AUTHORITY_GAPS`  
**Production code modified:** no

## 1. Finite verdict

Current V550 does **not** faithfully compute the full same-respondent cotravel object defined by D03's D04 test oracle for every lawfully supported question order and eligibility configuration.

The court found five material implementation failures:

1. **ordered-pair coverage is incomplete and processing-order dependent**;
2. **response-level DK/refusal/IAP/not-asked/inapplicable/special states can be converted into cotravel content** because cloud preparation ignores the harmonized missingness/substantiveness flags;
3. **`normalized_mutual_information` has a logarithm-base unit mismatch** (`mutual_info_score` in nats divided by entropy in bits);
4. **checkpoint resume is not semantically equivalent to fresh computation** because attitude-cloud state is reset and completed/skipped questions are not rehydrated into the cross-question state;
5. **cloud cardinality/mode gating occurs before state registration**, so a gated question disappears not only from its own computation but from later lawful pair formation, while the final status surface does not type that omission.

Other challenged behaviors are not implementation defects under the binding D03 oracle:

- the current partial-overlap denominator formula is reproduced exactly;
- requested scope isolation by `run_id`, `source`, `wave`, `canonical_wave`, and `country_code` is present in the in-memory state key;
- support tiers mark low support but do not suppress an otherwise emitted pair;
- current cloud computation is wholly unweighted, but D03 explicitly leaves the normative weighting law unresolved;
- current question-use authority intentionally restricts the live directional-atom lane to `scalar` and `binary_contrast`; nominal, multiselect, ranked/routed, derived/reference, administrative, and most matrix-child structures are not silently supported cloud topologies.

The result therefore separates **bugs in the implementation of the present mathematical object** from **limitations of that object** and from **questions for which governing authority is still missing**.

## 2. Base-law gate and audit scope

D04 did not start from the old discovery-control base. D03 closed on branch `agent/vozhd-trii-d03-v549-cloud-lineage` at:

`7ea5962f644ad796064e30ffafb46f2c077404b9`.

That D03 tip was a clean two-commit fast-forward over the previous discovery-control base and added only:

- `courts/D03/RESULT.md`;
- `courts/D03/RESULT.json`.

The parent branch `agent/vozhd-trii-prechange-discovery-control` was fast-forwarded to that accepted D03 tip, and D04 was created from exactly that SHA. No production file was changed by D04.

The court read D03 first, especially its section **D04 TEST ORACLE**, then the complete discovery-control surface and governing whole-machine law, including:

- `README.md`;
- `00_FULL_MACHINE_VISION.md`;
- `01_FINDINGS_LEDGER.md`;
- `02_RESOURCE_INDEX.md`;
- `03_ASSUMPTION_AND_UNKNOWN_REGISTER.md`;
- `04_DISCOVERY_COURTS_REGISTER.md`;
- `05_DECISION_PROTOCOL.md`;
- `06_FIRST_WAVE_LAUNCH_REGISTER.md`;
- `DISCOVERY_REGISTER.json`;
- `RAWLSING_GOVERNING_SPIRIT.md`;
- `TERMINAL_DEMAND_ENVELOPE.md`;
- `ARCHITECTURE_PASS_LAW.md`.

Primary executable surfaces inspected:

- `data/ddm_build_copy/ddm_v550_clouds.py`;
- `data/ddm_build_copy/ddm_v550_metrics.py`;
- `data/ddm_build_copy/ddm_v550_support.py`;
- `data/ddm_build_copy/ddm_v550_question_use.py`;
- `data/ddm_build_copy/ddm_v550_validation.py`;
- `data/ddm_build_copy/ddm_v550_branching.py`;
- `data/ddm_build_copy/build_determinicity_wave_shard_v550.py`;
- `data/ddm_build_copy/build_determinicity_repository_v550.py`.

Empirical micro-fixtures and exact outputs are preserved under:

`courts/D04/evidence/EMPIRICAL_PROBES.json`.

The connector does not expose a local checkout runtime. The empirical probes therefore reproduce the exact inspected pandas/state/metric operations in an isolated Python harness; code inspection remains authoritative for orchestration, eligibility, gating, checkpoint, and replay behavior.

## 3. Classification ledger

| ID | Classification | Finding |
|---|---|---|
| D04-F01 | **IMPLEMENTATION_DEFECT** | Lawful ordered-pair coverage depends on processing order. A current anchor is compared only with candidates already stored. |
| D04-F02 | **IMPLEMENTATION_DEFECT** | Perfect deterministic binary association reports NMI `0.693147...`, not `1.0`, because MI is in nats while entropy denominator is in bits. |
| D04-F03 | **IMPLEMENTATION_DEFECT** | Cloud preparation ignores row-level `is_substantive`, `is_missing`, `is_special`, `is_dk`, `is_refusal`, `is_iap`, `is_not_asked`, and `is_inapplicable`; any nonblank special code can become the selected cotravel category. |
| D04-F04 | **IMPLEMENTATION_DEFECT** | Resume resets attitude state, skips completed questions, and does not restore their frames; cross-boundary pairs disappear relative to fresh compute. |
| D04-F05 | **IMPLEMENTATION_DEFECT** | Cardinality/mode gating prevents `build_attitude_cloud_rows` from running at all, so gated questions are not registered as later candidates; omission propagates into the pair graph. |
| D04-F06 | **SEMANTIC_AMBIGUITY** | Empty cloud output is surfaced as `disabled_until_cross_question_engine` regardless of whether emptiness came from mode, cardinality, eligibility, no overlap, order loss, or resume loss. |
| D04-F07 | **SEMANTIC_AMBIGUITY** | Output column `mutual_information` contains normalized mutual information, not raw mutual information. D03 fixes this as current executable meaning but the field name remains hazardous. |
| D04-F08 | **MISSING_AUTHORITY** | Normative survey-weight requirement for the diagnostic cloud lane is not established. Current execution is unweighted. |
| D04-F09 | **MISSING_AUTHORITY** | Conflicting duplicate/repeated-response semantics and lawful multiselect set/order semantics are unresolved. First-row collapse is executable fact, not authority. |
| D04-F10 | **MISSING_AUTHORITY** | Modal-cell tie-breaking has no governing law. Reverse-pair modal selection need not transpose under a tie. |
| D04-F11 | **MISSING_AUTHORITY** | Whether routed eligibility requires a common risk-set denominator rather than D03's current asymmetric denominator is unresolved. |
| D04-F12 | **TOPOLOGY_UNSUPPORTED** | `nominal_choice`, `multiselect`, `ranked_choice`, `routed_followup`, derived/reference, administrative, missingness-control, and structurally classified matrix-child/factual-context forms are outside the current directional-atom cloud lane. |
| D04-F13 | **NO_DEFECT** | Current denominator arithmetic matches D03's exact oracle. |
| D04-F14 | **NO_DEFECT** | Requested state-scope isolation is exact across `run_id/source/wave/canonical_wave/country_code`. |
| D04-F15 | **EXPECTED_BEHAVIOR** | Low selected-cell support changes `support_status`/`confidence_tier`; it does not suppress an otherwise valid emitted row. |
| D04-F16 | **EXPECTED_BEHAVIOR** | The persistent object retains one modal joint cell plus pairwise summary statistics, not every rare/category-specific joint cell. |

## 4. Pair coverage theorem and counterexample

D03 defines the lawful semantic ordered-pair set within a scope as:

`L = {(A,B) | A != B AND anchor_eligible(A) AND feature_eligible(B)}`.

Current `build_attitude_cloud_rows` implements a strictly narrower stateful relation. Let the processing order be `Q1 ... Qn`. A current question is compared only against entries already in `_ATTITUDE_CLOUD_STATE`, and the current question is inserted into state only **after** its emission loop.

Ignoring other gates for the moment, the fresh-run executable pair set is therefore:

`E = {(Qi,Qj) | j < i AND anchor_eligible(Qi) AND feature_eligible(Qj)}`.

Hence `E ⊆ L`, but in general `E != L`.

The strongest counterexample is unavoidable whenever two questions are both dual-eligible:

- order `A,B` emits `B→A` only;
- order `B,A` emits `A→B` only;
- D03 requires **both** `A→B` and `B→A`.

No single linear processing order can make both directions appear under the current one-pass algorithm. Therefore any scope containing two distinct dual-eligible questions is provably incomplete independent of the response values.

The required asymmetric eligibility fixtures also fail exactly where the state order predicts:

| Eligibility | Order A,B | Order B,A | Lawful expected |
|---|---|---|---|
| A anchor+feature, B anchor+feature | `B→A` | `A→B` | both directions |
| A anchor only, B feature only | none | `A→B` | `A→B` |
| A feature only, B anchor only | `B→A` | none | `B→A` |
| both anchor only | none | none | none |
| both feature only | none | none | none |

A blocked/ineligible question is not stored and does not create a lawful pair; that exclusion is expected.

### Ruling

**Pair coverage theorem/counterexample:** `IMPLEMENTATION_DEFECT`.

The current algorithm computes a lower-triangular projection of the lawful ordered-pair graph determined by processing order, not the complete lawful graph.

## 5. Question-order invariance

D03 requires permutation of otherwise identical question inputs not to alter the lawful ordered-pair set or fixed-pair metrics.

The pair-set invariant fails immediately under the dual-eligible and anchor-only/feature-only fixtures above.

For a fixed A→B pair that is actually emitted in both executions, the pair arithmetic itself is order-independent because `_emit_attitude_cloud_pair` receives the same prepared A and B frames and recomputes the join/crosstab from those frames. The defect lies in **whether the pair exists at all**.

The practical production order is therefore semantically consequential even though it is operationally incidental.

### Ruling

**Order-invariance:** `FAIL — IMPLEMENTATION_DEFECT`.

## 6. Directional semantics

The current cloud is not a symmetric association-only product.

For an emitted A→B row:

- `p_cotravelling_given_anchor = N_ab / N_a`;
- `p_cotravelling_baseline = N_b / N_B`;
- `difference_from_baseline` and `lift` inherit that anchor/candidate asymmetry.

NMI and Cramér's V are symmetric pairwise association summaries, but they do not erase the directional probability fields.

A no-tie fixture gives:

**A→B**
- selected cell `(a,b)`;
- `N_ab=2`, `N_a=3`, `N_b=2`, `N_B=4`;
- `P(B=b|A=a as currently defined)=2/3`;
- baseline `=1/2`.

**B→A**
- selected cell `(b,a)`;
- `N_ab=2`, `N_b-as-anchor=2`, A baseline count `=3`, A denominator `=4`;
- conditional `=1`;
- baseline `=3/4`.

Thus `P(B|A)` and `P(A|B)` are not interchangeable even when the selected cell transposes and symmetric association statistics agree.

Under a modal tie, current stable sorting can select a different tied maximum after transposition. The empirical tie fixture selects A→B `(a1,b2)` but B→A `(b1,a2)`, not the transpose `(b2,a1)`. D03 explicitly leaves tie law unresolved, so this is **MISSING_AUTHORITY**, not a proven implementation defect.

### Ruling

**Directional semantics:** the lawful product requires an ordered A→B row whenever A is anchor-eligible and B is feature-eligible; if both sides are dual-eligible, both directions are required. Symmetric NMI/Cramér's V do not substitute for the reverse conditional. Current implementation fails this requirement through D04-F01.

## 7. Respondent overlap and denominator law

For a fixed emitted pair the core respondent mechanics match D03.

`_prepare_attitude_cloud_frame` first reduces each question to nonblank respondent IDs and nonblank normalized responses, then keeps one row per respondent. `_emit_attitude_cloud_pair` performs an inner join by `respondent_id` to form the complete-case cross-tab.

Important naming fact:

`n_overlap` is **not total complete-case overlapping respondents**. It is the count of the selected modal joint cell `(a*,b*)`.

Partial-overlap fixture:

Anchor A:
- r1=a
- r2=a
- r3=a
- r4=x

Candidate B:
- r2=b
- r3=b
- r4=y
- r5=b
- r6=b

There are 3 complete-case overlapping respondents, but the modal cell `(a,b)` has count 2. Current/D03 result:

- `n_overlap = 2`;
- `n_anchor = 3` (r1 remains in the A=a denominator even though B is absent);
- `n_candidate_baseline = 4`;
- candidate denominator `len(B)=5`;
- conditional `2/3`;
- baseline `4/5`;
- lift `5/6`.

This exactly matches D03's oracle.

### Population comparability caveat

The two probability denominators are deliberately not a common complete-case risk set:

- conditional denominator: all prepared A respondents in `a*`;
- baseline denominator: all prepared B responders.

Therefore, if B is observed only for a routed or otherwise selected population, the lift can mix response cotravel with response availability/routing. D03 explicitly commands D04 not to replace these denominators silently. The arithmetic is therefore **NO_DEFECT** relative to the current object, while the normative question of a common routed-eligibility denominator remains **MISSING_AUTHORITY**.

### Ruling

**Denominator:** `NO_DEFECT` against the binding current-code oracle; routed-risk-set interpretation remains unresolved.

## 8. Weighting

The attitude-cloud path is wholly unweighted.

No survey weight is supplied to:

- respondent deduplication;
- cross-tab construction;
- modal-cell selection;
- `n_anchor`;
- `n_candidate_baseline`;
- `n_overlap`;
- conditional probability;
- baseline probability;
- lift;
- NMI;
- Cramér's V.

The row exposes `n_unweighted = n_overlap`, but the probability/lift field names do not carry an equally explicit unweighted qualifier.

This is not partial weighting: it is an unweighted computation end-to-end.

D03 explicitly leaves the normative cloud weighting law unresolved. The repository contains weighting helpers elsewhere, but their existence does not create authority to apply them here.

### Ruling

**Weighting:** executable behavior = unweighted. Normative law = `MISSING_AUTHORITY`. Generic probability naming = `SEMANTIC_AMBIGUITY`, because a consumer could mistake these quantities for survey-weighted population estimates.

## 9. Metric correctness: normalized mutual information

`ddm_v550_metrics.normalized_mutual_information` combines:

- `sklearn.metrics.mutual_info_score`, whose natural-log result is in **nats**;
- `distribution_entropy`, whose `entropy_from_counts` uses `log(p, 2)`, yielding **bits**.

The implementation then divides the former by the latter.

Perfect deterministic binary fixture:

`x=[0,0,1,1]`, `y=[0,0,1,1]`.

Observed:

- MI in nats = `0.6931471805599453`;
- entropy in bits = `1.0`;
- current NMI = `0.6931471805599453`;
- unit-consistent normalized MI = `1.0`;
- Cramér's V = `1.0`.

Thus the NMI field is systematically scaled by the log-base mismatch rather than normalized on the intended common unit basis.

This defect affects the persisted `mutual_information` value and any place where that value participates in `association_strength=max(nmi,c_v)`. Even when Cramér's V happens to dominate, the NMI field itself remains wrong.

### Ruling

**Metric correctness:** `IMPLEMENTATION_DEFECT`.

Separate naming issue: the output column is called `mutual_information` although it receives the normalized value. D03 establishes that as current executable meaning, so D04 records the name as `SEMANTIC_AMBIGUITY` rather than silently redefining it.

## 10. Duplicate responses, repeated modules, and multi-select

Current preparation executes:

`drop_duplicates(subset=["respondent_id"], keep="first")`.

There is no row-order authority in this helper.

### Exact duplicates

When duplicate rows are truly identical at the respondent/question normalized-response level, first-row retention prevents duplicated source rows from inflating counts. For that narrow case the court found `NO_DEFECT`.

### Conflicting duplicates / legitimate repeated responses

When one respondent has more than one different response row for the same question frame, reversing only those duplicate row positions changes the prepared response and can change cloud counts.

Fixture result:

- first ordering: selected `(yes,b1)`, `n_overlap=3`, `n_anchor=3`;
- reversed duplicate rows: selected `(yes,b1)`, `n_overlap=2`, `n_anchor=2`.

A stronger fixture can also change the selected modal cell; the important theorem is already established: the result is a function of input row order whenever duplicate respondent rows disagree.

### Multi-select

The helper itself has no set semantics. If a long-form multiselect were forced into it, all but the first selected value for a respondent would be discarded.

However, current question-use authority normally prevents that from becoming a live cloud defect: `multiselect` is outside `CURRENT_DIRECTIONAL_ATOM_TOPOLOGIES`, and non-current directional atoms have attitude-cloud anchor/feature permissions forced false.

Likewise, question types/handling rules containing `battery`, `multi_select`, `check_all`, or equivalent language are classified as `multiselect` before current directional eligibility.

### Repeated modules / source duplication

- distinct module items with distinct question IDs remain distinct questions;
- repeated rows under the same respondent/question ID are first-row collapsed;
- exact source duplication is deduplicated at the cloud preparation layer;
- conflicting source duplication silently first-wins.

D03 explicitly withholds governing authority over legitimate duplicate/repeated/multiselect semantics.

### Ruling

**Duplicate/multi-select:** executable first-row sensitivity is proven. For true exact duplication: `NO_DEFECT`. For conflicting legitimate repeats: `MISSING_AUTHORITY` plus `SEMANTIC_AMBIGUITY`; no normative ordering can be invented. Multiselect as a live cloud topology: `TOPOLOGY_UNSUPPORTED`.

## 11. Routing and missingness

This is a material implementation failure, but it must be separated into question-level topology and response-level special states.

### 11.1 Question-level routed topology

`ddm_v550_question_use._response_topology_for_row` classifies explicit follow-up/conditional/skip-logic questions as `routed_followup`. That topology is not in the current directional-atom set, so it is not currently lawful as an attitude-cloud anchor/feature.

That exclusion is `TOPOLOGY_UNSUPPORTED`, not a cloud arithmetic defect.

### 11.2 Response-level special states inside an otherwise eligible question

Upstream harmonization explicitly materializes:

- `is_substantive`;
- `is_missing`;
- `is_special`;
- `is_dk`;
- `is_refusal`;
- `is_iap`;
- `is_not_asked`;
- `is_inapplicable`.

Cloud preparation does not inspect any of them. It checks only that `response_value_normalized` is nonblank.

Therefore a nonblank code such as `DK`, `REFUSED`, `IAP`, or a labeled not-asked/inapplicable code survives preparation and is treated exactly like substantive relation content.

Hostile fixture:

- r1/r2: A=`IAP`, explicitly `is_iap=true`, non-substantive;
- r1/r2: B=`DK`, explicitly `is_dk=true`, non-substantive;
- r3/r4: substantive yes/no values.

Current modal cell becomes `(IAP,DK)` with:

- `n_overlap=2`;
- conditional `1.0`;
- candidate baseline `0.5`;
- lift `2.0`.

The machine has therefore converted a shared absence/routing pattern into the headline cotravel category.

That violates the governing requirement that typed ignorance/absence/control flow not silently become content.

### Exact routing/missingness matrix

| Input state | Current preparation | Ruling |
|---|---|---|
| blank normalized response | filtered out | **EXPECTED_BEHAVIOR** |
| valid substantive zero `"0"` | retained | **NO_DEFECT** |
| DK, nonblank and flagged special/non-substantive | retained as category | **IMPLEMENTATION_DEFECT** |
| refusal, nonblank and flagged special/non-substantive | retained as category | **IMPLEMENTATION_DEFECT** |
| IAP/inapplicable, nonblank and flagged special | retained as category | **IMPLEMENTATION_DEFECT** |
| explicit not-asked code, nonblank and flagged | retained as category | **IMPLEMENTATION_DEFECT** |
| structurally impossible special response, nonblank | retained as category | **IMPLEMENTATION_DEFECT** |
| candidate row physically absent | cannot enter join; anchor may remain in conditional denominator | **EXPECTED_BEHAVIOR** under D03 denominator law |

### Ruling

**Routing/missingness:** `FAIL — IMPLEMENTATION_DEFECT` for explicit special/non-substantive response rows. Question-level routed follow-ups remain `TOPOLOGY_UNSUPPORTED` under current authority.

## 12. Response-topology admissibility

Current question-use law is conservative. `CURRENT_DIRECTIONAL_ATOM_TOPOLOGIES` contains only:

- `scalar`;
- `binary_contrast`.

Even these require certified directionality/authority and `RELATION_EVIDENCE` role before attitude-cloud use remains enabled.

| Requested topology | Current classification/admissibility | Ruling |
|---|---|---|
| binary | `binary_contrast`; potentially current directional atom when certified | **EXPECTED_BEHAVIOR / supported** |
| scale | normally `scalar`; potentially current directional atom when certified | **EXPECTED_BEHAVIOR / supported** |
| ordinal | `question_type=ordinal` falls to `scalar`; still requires directional certification | **EXPECTED_BEHAVIOR / supported conditionally** |
| nominal | `nominal_choice` where detected; outside current directional atom set | **TOPOLOGY_UNSUPPORTED** |
| multi-select | `multiselect`; outside current directional atom set | **TOPOLOGY_UNSUPPORTED** |
| ranked choice | `ranked_choice`; outside current directional atom set | **TOPOLOGY_UNSUPPORTED** |
| routed follow-up | `routed_followup`; outside current directional atom set | **TOPOLOGY_UNSUPPORTED** |
| matrix/battery | `battery`/multiresponse forms classify as multiselect; `matrix_child` source structure becomes factual/structural context; a relation-evidence matrix item represented as a scalar item can be supported | **TOPOLOGY_UNSUPPORTED unless reduced by existing authority to a certified scalar item** |
| derived/reference | `valid_cloud_feature` rejects `question_type=derived_reference` | **TOPOLOGY_UNSUPPORTED / expected exclusion** |
| administrative/non-substantive question | administrative/missingness/factual-context roles are blocked | **TOPOLOGY_UNSUPPORTED / expected exclusion** |

The arithmetic helper could technically crosstab arbitrary categories. That implementation permissiveness does not create lawful topology support.

### Ruling

**Topology:** current cloud is a certified scalar/binary directional-atom product only. Unsupported topologies must not be judged as if the present helper had lawful semantics for them.

## 13. Support and rare categories

For an emitted pair, support is based on the **selected modal cell count** `n_overlap`.

The threshold helper is wave-relative:

`ceil(total * 0.005)`, clipped to floor `2` and cap `30`.

For attitude-cloud rows, the `total` supplied to support labeling is `min(anchor_meta.n_respondents, candidate_meta.n_respondents)` when both are positive, not the actual complete-case join size.

Behavior:

- positive low-N rows are still emitted;
- low support becomes `underpowered` and lowers confidence;
- support status does not alter the probability, lift, NMI, or Cramér's-V computation;
- support is not a significance test.

A rare but stable category-specific association may never be named in the persistent row if it is not the globally modal joint cell. NMI/Cramér's V still see the full complete-case contingency table, but the category-specific rare joint cell itself is discarded from persistent output.

That is a limitation of the current **one-modal-cell mathematical object**, not support gating.

No governing rule located by D04 specifies whether support tiers should use actual complete-case overlap rather than the current `min(question totals)` proxy. D04 therefore does not invent a replacement denominator.

### Ruling

**Support / rare categories:** support marking = `EXPECTED_BEHAVIOR`; no suppression defect. Nonmodal rare-cell loss = `EXPECTED_BEHAVIOR` of the current persistent object. Choice of total for support labeling = `SEMANTIC_AMBIGUITY / MISSING_AUTHORITY`, not a proven computation defect.

## 14. Scope isolation

`_ATTITUDE_CLOUD_STATE` is keyed by the exact tuple:

`(run_id, source, wave, canonical_wave, country_code)`.

Candidate frames are only compared inside that state entry. Therefore identical respondent IDs in different requested scopes cannot meet in the pairwise respondent join.

Hostile collisions across each requested dimension are isolated by construction:

- different `run_id` → different state;
- different `source` → different state;
- different `wave` → different state;
- different `canonical_wave` → different state;
- different `country_code` → different state.

Within one state, candidate frames are keyed only by `question_id`. If the same question ID can lawfully identify multiple distinct physical question frames inside one exact state, later storage overwrites earlier storage. D03 leaves global question/frame uniqueness unresolved, and D04 found no authority permitting a stronger claim. That within-state collision therefore remains `MISSING_AUTHORITY`, not a requested scope failure.

### Ruling

**Scope isolation:** `NO_DEFECT` for all five requested scope dimensions and respondent-ID collisions across them.

## 15. Cloud gating completeness

`should_emit_cloud_tables` has four modes/behaviors:

- `full`: always true;
- `off`: always false;
- `auto`: emit only when `branch_rows <= cloud_max_branch_rows`;
- `share`: effective threshold is `max(cloud_max_branch_rows, round(wave_respondents * cloud_max_branch_share))`.

The `share` argument therefore does not act as an independent maximum-share ceiling; it can enlarge the absolute row threshold. The naming is semantically non-obvious, but no governing rule found by D04 establishes an alternative formula.

The material defect is where the gate sits in orchestration.

In `build_determinicity_wave_shard_v550.py`, when the gate is false:

- `build_attitude_cloud_rows` is not called;
- the question frame is not inserted into `_ATTITUDE_CLOUD_STATE`;
- no attitude-cloud checkpoint for that question is written;
- the question can nevertheless be marked complete.

Consequently a gated feature question cannot participate as candidate for a later anchor. The gate is therefore not merely “do not emit this question's expensive row”; it removes a node from later pair formation.

Example:

- B is a lawful feature but exceeds the auto threshold and is skipped;
- later A is a small lawful anchor and passes the gate;
- A→B cannot be emitted because B was never registered.

That pair loss is not represented in `cloud_exclusion_audit`, whose validators operate only on rows that already exist.

### Typed absence failure

At finalization, an empty attitude-cloud table receives the global status:

`disabled_until_cross_question_engine`.

The same status can therefore represent:

- explicit `cloud_mode=off`;
- all questions exceeding threshold;
- no eligible pairs;
- no overlap;
- order-dependent pair loss;
- resume pair loss;
- or other empty-output causes.

It does not identify which questions/pairs were gated and does not preserve a typed reason for nonexecution. The accompanying warning is also stale in substance: the current implementation **does** contain a cross-question respondent-join engine.

### Ruling

**Cloud-gating completeness:**

- explicit `off` and threshold policy as control choices: `EXPECTED_BEHAVIOR` at the mode level;
- pre-state gating that removes later lawful pair candidates: `IMPLEMENTATION_DEFECT` against D03 pair completeness;
- absence/status surface: `SEMANTIC_AMBIGUITY` and observability failure;
- `share` formula semantics: executable fact established; normative meaning of “max share” remains `MISSING_AUTHORITY`.

## 16. Checkpoint and replay equivalence

### 16.1 Per-question resume: definite non-equivalence

At shard start, V550 calls:

`reset_attitude_cloud_state()`.

The resume loop then skips a question when `_question_checkpoint_exists(...)` returns true. Skipped questions are not passed back through `build_attitude_cloud_rows`, and their prepared frames are not rehydrated into `_ATTITUDE_CLOUD_STATE`.

Counterexample using the current flawed fresh semantics themselves:

- A and B are both anchor+feature eligible;
- fresh order A,B emits `B→A`;
- A's checkpoint is complete;
- resume starts, state is reset;
- A is skipped;
- B is recomputed;
- B sees no stored A;
- resumed output for B contains no `B→A` row.

Thus resume is not merely incomplete relative to D03's ideal graph; it is **not equivalent even to a fresh execution of the current implementation**.

This is a direct `IMPLEMENTATION_DEFECT`.

### 16.2 Resume invalidation surface

Question checkpoint reuse is guarded by the saved/current `question_use_contract_hash`. The complete marker itself is just `complete`.

The skip check does not establish equivalence for:

- cloud mode;
- `cloud_max_branch_rows`;
- `cloud_max_branch_share`;
- cloud engine version;
- actual response-row content.

Therefore changing cloud execution configuration can leave a question “complete” and skipped even though a fresh run under the new configuration would make a different cloud decision. The missing attitude-state rehydration already proves failure with unchanged configuration; this weaker invalidation surface compounds it.

### 16.3 Whole-cloud replay shortcut

`_load_replayed_cloud_tables` requires:

- `cloud_refresh_manifest.json` and the persisted attitude-cloud parquet;
- explicit `cloud_replay_allowed=true`;
- exact `cloud_engine_version` match;
- current question-use contract hash match;
- replayed row validation;
- consistency between a disabled manifest status and nonempty replay.

This is stronger than the per-question checkpoint guard.

However, the acceptance function does not itself compare a hash/fingerprint of the current harmonized response substrate or the exact expected lawful ordered-pair universe. `validate_attitude_cloud_rows` validates existing row shape/provenance/self-pair constraints but does not prove pair-set completeness.

D04 did not locate governing authority that defines `cloud_replay_allowed=true` as an external proof of response-data identity. Therefore whole-cloud replay equivalence is **not proven** for changed-but-authority-identical substrates.

This is classified `MISSING_AUTHORITY` / replay-proof insufficiency rather than inventing a stale-replay event that was not observed in a materialized run.

### Ruling

**Replay equivalence:** `FAIL` overall.

- per-question checkpoint/resume: **IMPLEMENTATION_DEFECT**, proven non-equivalent;
- full-cloud replay under identical data/config: row-level checks exist, but full semantic pair completeness is not validated;
- replay under changed response substrate with unchanged authority hash: equivalence not established; `MISSING_AUTHORITY` / insufficient proof.

## 17. Validator completeness

`validate_attitude_cloud_rows` checks existing row schema, required provenance fields, diagnostic status, cloud flags, and self-question exclusion.

It returns no issue for an empty table and contains no reconstruction of the expected D03 pair set.

Therefore the validator cannot detect:

- a missing A→B pair;
- order-dependent half-graphs;
- pairs lost at cardinality gating;
- pairs lost across a resume boundary;
- an empty table whose computation was never attempted;
- the NMI log-base mismatch;
- special response categories that survived as content if their provenance fields otherwise look valid.

`cloud_exclusion_audit` is downstream of this row validator, so it likewise cannot report omitted rows that never existed.

This is an implementation-observability gap. D04 does not prescribe a replacement validator.

## 18. Required final rulings

### Pair coverage theorem/counterexample

**FAIL — IMPLEMENTATION_DEFECT.** Current fresh output is the processing-order lower triangle of the lawful anchor×feature graph. Two dual-eligible questions are a universal counterexample: exactly one direction appears per order although both are required.

### Order-invariance ruling

**FAIL — IMPLEMENTATION_DEFECT.** Permuting question order changes the emitted ordered-pair set.

### Directional-semantics ruling

**A→B and B→A are distinct lawful semantic products when each side is respectively anchor/feature eligible.** Conditional/baseline quantities are directional. NMI and Cramér's V are symmetric and cannot substitute for the missing reverse conditional. Modal ties remain `MISSING_AUTHORITY`.

### Denominator ruling

**NO_DEFECT** against D03's executable oracle. `n_overlap` is modal-cell count, `n_anchor` is selected anchor-category count over the full prepared anchor frame, and candidate baseline uses the full prepared candidate frame. Routed common-risk-set comparability remains `MISSING_AUTHORITY`.

### Weighting ruling

**Current cloud is entirely unweighted.** Normative weighting requirement = `MISSING_AUTHORITY`; generic probability names are semantically ambiguous about survey representativeness.

### Duplicate/multi-select ruling

**First-row collapse is executable fact and row-order sensitive for conflicting duplicates.** Exact duplication can be harmlessly collapsed. Lawful repeat semantics = `MISSING_AUTHORITY`. Multiselect = `TOPOLOGY_UNSUPPORTED` by current question-use law and would be lossy if forced through the helper.

### Routing/missingness ruling

**FAIL — IMPLEMENTATION_DEFECT.** Explicit nonblank DK/refusal/IAP/not-asked/inapplicable/special response rows can become cotravel content because cloud preparation ignores row-level epistemic/routing flags. Blank rows are filtered and valid substantive zero is retained correctly.

### Scope-isolation ruling

**PASS — NO_DEFECT** for `run_id`, `source`, `wave`, `canonical_wave`, `country_code`. Cross-scope respondent-ID collisions cannot join through cloud state.

### Cloud-gating completeness ruling

**FAIL — IMPLEMENTATION_DEFECT + SEMANTIC_AMBIGUITY.** Mode/cardinality policy can prevent a question from entering cloud state at all, deleting later lawful pairs; the final empty-cloud status does not type the reason for nonexecution.

### Replay-equivalence ruling

**FAIL.** Per-question resume is provably non-equivalent to fresh compute because skipped questions do not rehydrate cross-question state. Whole-cloud replay has engine/authority/row checks but does not itself prove response-substrate identity or lawful pair-set completeness.

## 19. Boundary for the later architect

The later architect should not collapse these findings into one generic claim that “attitude clouds are bad.” D04 establishes three different categories of limitation.

### A. Bugs/omissions in implementation of the present object

These can change the answer while holding the intended present object fixed:

- missing half or all lawful ordered pairs due processing order;
- special/missing response states becoming substantive cloud categories;
- NMI base-unit error;
- resume state loss;
- pre-state cloud gating deleting later pairs;
- untyped/stale empty-output status;
- row validators unable to detect pair-set incompleteness.

### B. Mathematical-object limitations that are currently expected

These are properties of the current D03-defined object, not implementation bugs:

- one selected modal joint cell rather than a full pairwise joint distribution;
- directional event probability with an asymmetric non-complete-case denominator;
- full-table NMI/Cramér's V as lossy summaries;
- rare nonmodal joint cells not persisted individually;
- support tiers mark rather than suppress;
- no inference from population cotravel to actor psyche/belief/identity.

### C. Authority gaps / unsupported domains

These cannot lawfully be solved by guessing inside D04:

- survey-weight requirement for the diagnostic lane;
- common routed-risk-set denominator law;
- legitimate repeated-response ordering/set semantics;
- multiselect set semantics;
- modal-cell tie law;
- within-scope question-ID uniqueness guarantee;
- the semantic proof required for `cloud_replay_allowed` across changed response substrates;
- future topology laws for nominal, multiselect, ranked/routed, and other non-current directional atoms.

That separation is the court's success condition: a later architecture decision can now distinguish what the current cloud **means**, where its implementation fails to compute that meaning, and where the machine still lacks authority to say what the meaning should be.
