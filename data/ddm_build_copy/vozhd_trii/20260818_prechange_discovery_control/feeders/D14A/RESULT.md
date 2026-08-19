# D14A — Current Compute & Materialization Geometry Baseline

**Status:** `NON_DISPOSITIVE_FEEDER_COMPLETE_WITH_STATIC_BASELINE_AND_BLOCKED_REAL_MEASUREMENT`  
**Repository:** `maidiu/rawlsing`  
**Exact base SHA:** `b92d3f3db9faaa962f59d55e61122701df9e53aa`  
**Branch:** `agent/vozhd-trii-d14a-current-cost-geometry`  
**Write scope:** `data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/feeders/D14A/`

## 1. Ruling

D14A establishes the **current implementation geometry** of the V550/V550J empirical machinery at the commanded base. It does not establish a replacement architecture, a savings estimate, a deletion entitlement, or semantic dispensability.

The static baseline is established. Production-equivalent wall-clock, CPU, peak RSS, live row counts, checkpoint/artifact bytes, and database I/O are not established because this feeder has no populated production-equivalent database execution surface.

The inherited law therefore remains literal:

`POPULATED_SUBSTRATE_EMPIRICAL_FACTS_UNKNOWN__NO_DB_ACCESS_EXPECTED`

No populated cardinality or database-I/O number below is fabricated.

## 2. Governing boundary

D07 is binding. In particular:

- cost is not semantic authority;
- `MATERIALIZE_ALL_PERMITTED` is not a universal workload command;
- semantic permission fields do not themselves command universal precomputation;
- bounded V550J configurations are a real authority-selected workload surface;
- reconstructibility, provenance, typed absence, weighting semantics and terminal necessity govern later decisions.

Accordingly, every cost fact in this feeder describes **what current code does**, not what future architecture may lawfully remove.

## 3. Measurement classification

`MEASURED` is used only for directly inspected repository/source facts, including exact branch/base identity before D14A writes. `STATICALLY_DERIVED` means a call/scan/join/cardinality formula follows from current source. `BLOCKED_REAL_MEASUREMENT` means the requested runtime magnitude requires a populated production-equivalent run not available here. `UNKNOWN` is reserved for facts, notably database I/O magnitude, for which this feeder has neither execution nor sufficient instrumentation evidence.

All `measured_wall_clock`, `measured_peak_rss`, and `measured_bytes` cells in `CURRENT_COST_GEOMETRY.csv` are intentionally blank.

## 4. Notation

Core requested variables are `Q` questions, `I` indicator fields, `R` respondents, `P` lawfully eligible ordered question pairs, `Cq` response categories, `D` recursion depth, `J` governed V550J configurations, `Kj` items in configuration `j`, `A` association candidates, and `B` recursive nodes.

Current source requires additional grain-safe notation: `C` countries; `N_c` response-long shared/prepared rows in country `c`; `I_q` present indicators for question `q`; `V` observed indicator-value cardinality; `F` support-eligible indicator-value groups; `E_q` position-signature candidate columns; `L_q` relation-co-signature candidate columns; `Q_cloud` questions passing the operational cloud resource gate; `P_state` actual stateful cloud pair attempts; and `R_jc`, `M_jc`, `MSHIP_jc` V550J eligible respondents, patterns, and membership rows.

`N_c` is necessary because the shared substrate is response-long. `R_c` alone cannot determine its row count.

## 5. Current family geometry

The exact 18-family matrix, including invocation scope, loop geometry, scan formulas, join formulas, output-cardinality formulas, checkpoint behavior, measurement status, cost drivers, and source symbols, is `CURRENT_COST_GEOMETRY.csv`.

The principal shapes are:

| computation family | principal current geometry | output cardinality |
|---|---|---:|
| `answer_distribution` | one response grouping per executed `q` | `Σq Cq` |
| `country_answer_distribution` | country grouping then response grouping within country | `ΣqΣc Cq,c` |
| `position_distribution` | post-loop country respondent sort/dedupe plus position-field groupings | `ΣcΣi Vc,i` |
| `position_indicator_summary` | `Σq Iq` indicator statistic passes | `Σq Iq` |
| `indicator_answer_matrix` | `Σq Iq` crosstabs, plus weighted pivots when applicable | `ΣqΣi Vq,i·Cq,i` |
| `outlier_cohort_summary` | `Σq Iq` indicator groupbys plus subgroup scans | `ΣqΣi Fq,i` |
| `secondary_indicator_summary` | `Iq` first-pass scores plus at most `Iq−1` primary-secondary checks per q | `Σq Sq`, `Sq≤Iq−1` |
| `recursive_branch_nodes` | binary recursion; every node tests all remaining indicators | `Bq≤2^(min(D,Iq)+1)−1` before pruning |
| `branch_position_signature` | score `E_q` position candidates, sort, top 5 | `≤5` per cloud-enabled q |
| `branch_relation_co_signature` | score `L_q` relation candidates, sort, top 5 | `≤5` per cloud-enabled q |
| `question_response_attitude_cloud` | stateful prior-question respondent joins and crosstabs | `≤P_state` |
| `shared V550/V550J extraction` | `Q+ΣjKj` requirement selection; response-long normalization/materialization | `Σc N_c` |
| `V550J joint-response patterns` | respondent grouping, `Kj` item filters, signature grouping | `M_jc≤R_jc` |
| `V550J respondent-membership materialization` | signature inner merge respondent summaries→patterns | normally `≤Σj,c R_jc` |
| `V550J association candidate generation` | membership×context respondent join, five aggregate groupings, four aggregate merges | `A` observed pattern×var×response groups |
| `association publication` | `O(A)` publication/lane gating | `PUB≤A` |
| `checkpoint/resume materialization` | `9Q_exec+3Q_cloud+Q_gap` table checkpoints | rows of checkpointed tables |
| `repeated scans between V550 and V550J` | repeated same-frame analysis, hash passes, pair joins, mode-dependent harmonization | no independent table |

## 6. Exact high-cost shapes

### 6.1 V550 repeated question-frame work

For every executed question, the shard builder independently calls distribution construction, indicator summary, secondary-indicator summary, indicator-answer matrix, outlier cohort, and recursive branch construction. When the cloud resource gate permits, it additionally calls position signature, relation co-signature, and attitude-cloud construction on the same prepared question frame.

This is not a claim that any family is unnecessary. It is a static fact that multiple analyses rescan the same question-row substrate.

### 6.2 Recursive branching

`branch_nodes_rows` is a binary recursive splitter. At depth `d`, each surviving node tests every remaining indicator, selects the highest positive entropy-gain indicator, and recurses into at most the two most frequent split values. If `d* = min(D, I_q)`, then before support/no-gain pruning:

- node upper bound: `B_q <= 2^(d*+1) - 1`;
- split-candidate evaluation upper bound: `Σ_{d=0}^{d*-1} 2^d (I_q-d)`.

Actual `B` is blocked by the no-DB law.

### 6.3 Stateful attitude-cloud pairs

The current cloud engine is processing-order dependent. It resets in-memory cloud state before the question loop. A current question allowed as an anchor iterates previously registered question frames only. Each attempted pair performs an inner merge on `respondent_id`, a response×response crosstab, normalized mutual information, and Cramér's V, then emits at most one highest-overlap cell.

Therefore:

`P_state = Σ_{anchor q} N_prev_registered(q)`

and, when every cloud-enabled question is both registered and anchor-enabled:

`P_state <= Q_cloud(Q_cloud-1)/2`.

This is not the Cartesian ordered-pair workload `Q(Q-1)`. D07 separately holds that eligibility does not itself authorize universal Cartesian materialization.

### 6.4 Shared V550/V550J substrate materialization

Current shared selection resolves the union of V550 base variables and governed V550J-required variables by scanning base question rows and `Σ_j K_j` registry items. Per country, canonicalization operates on the full response-long frame.

The atomic shared-substrate write then performs:

1. Parquet serialization;
2. schema materialization;
3. validation seed, including a full logical-content row hash;
4. manifest/file hashes;
5. a second validation, including a second full logical-content row hash;
6. Parquet reload;
7. a third full logical-content row hash before promotion;
8. manifest, validation, and `COMPLETE` promotion.

Those are current materialization costs only. They do not imply that any integrity step may be removed.

### 6.5 V550J joint patterns

For each governed configuration/country, `_summarize_respondents` groups family rows by respondent. Inside each respondent group it loops the `K_j` ordered family items and filters that respondent frame for each item. Eligible respondent summaries are then grouped by raw and semantic pattern signature.

Thus `M_jc <= R_jc`. For complete `K_j` signatures, a category bound is `M_jc <= min(R_jc, ∏_k C_jk)`. If the registry permits `minimum_items_answered=m_j<K_j`, a loose partial-signature bound is:

`M_jc <= min(R_jc, Σ_{S⊆K_j, |S|>=m_j} ∏_{k∈S} C_jk)`.

### 6.6 V550J respondent membership

`_pattern_membership_rows` primarily inner-merges respondent summaries to the pattern table on available raw/semantic signature columns, then emits one membership row per merged respondent assignment. A fallback builds a respondent lookup and iterates stored pattern member IDs. The live membership count is therefore data-dependent, while the normal signature path is bounded by eligible summarized respondents.

### 6.7 V550J association candidates

With materialized membership available, `_association_candidate_trace_rows` selects the fast path. It:

1. filters outside-family context to authorized rows with response values;
2. inner-merges pattern membership to eligible context on `respondent_id_norm`;
3. groups joined rows by `pattern_id`;
4. groups by `pattern_id × var_code`;
5. groups by `pattern_id × var_code × response_value`;
6. builds baseline `var_code × response_value` and `var_code` totals;
7. left-merges four aggregate tables into candidate counts;
8. computes gates, metrics, lane authority and publication status over candidate groups.

`A` is therefore the number of **observed overlapping** `(pattern, outside variable, outside response)` groups after eligibility—not a blind full Cartesian product. It is bounded by `M_jc × Σ_v C_v`, but the live count is blocked.

Publication then filters/classifies candidate rows. Final `PUB <= A`.

## 7. Checkpoint/resume geometry

For each executed V550 question the visible shard loop writes nine unconditional result checkpoints:

1. `question_universe`
2. `question_use_contract`
3. `answer_distribution`
4. `country_answer_distribution`
5. `position_indicator_summary`
6. `secondary_indicator_summary`
7. `indicator_answer_matrix`
8. `outlier_cohort_summary`
9. `recursive_branch_nodes`

A cloud-enabled question adds three: `question_response_attitude_cloud`, `branch_position_signature`, and `branch_relation_co_signature`. A non-empty mapping gap adds one more. Each handled question also receives a completion marker.

Static table-write formula:

`9 Q_exec + 3 Q_cloud + Q_gap`

plus `Q_handled` completion markers.

Finalization can re-read/combine checkpoint tables. `position_distribution` is computed after the question loop and is not per-question checkpointed in the visible current shard path.

Resume skipping is itself part of current geometry: an existing question checkpoint can bypass the entire question computation. In-memory attitude-cloud state is reset before the loop and is not reconstructed merely by skipping resumed questions; replayed cloud outputs use a separate replay path. This is a current cost/replay topology fact, not a D14A semantic ruling.

## 8. Repeated extraction and harmonization

Current code contains explicit instrumentation for V550 prepared/per-question/fallback harmonization call and row counts. V550J records stage timings and harmonization counters in `v550j_performance_profile.json`.

Static tracing establishes:

- V550 prefetches a country response cache once, then selects question frames from it;
- prepared V550 mode can harmonize at cache preparation, while non-prepared/fallback paths harmonize question frames;
- V550J caches prepared country state across applicable families on the normal prepared path;
- V550J forensic/fallback modes can reharmonize per question when prepared state is unavailable;
- each V550J family still filters prepared rows into family and outside-family context;
- association generation expands respondent membership against outside-family response-long context before aggregate collapse;
- shared-substrate atomic writing performs at least three full logical-content hash passes on each materialized country frame.

No live values for those counters were available to D14A.

## 9. Blocked real measurements

The following remain `BLOCKED_REAL_MEASUREMENT`: production wall-clock, CPU, peak RSS, rows read, intermediate rows, emitted rows, checkpoint bytes, output bytes, live `B`, live `P_state`, live `M_jc`, live `MSHIP_jc`, live `A`, and live `PUB`.

Database I/O magnitude is `UNKNOWN`: source code proves DB-capable extraction paths exist, but without a live instrumented execution D14A will not invent query counts, bytes, cache-hit ratios, or server work.

See `BASELINE_MEASUREMENTS.json` and `BLOCKED_MEASUREMENT_LEDGER.csv`.

## 10. Evidence spine

Primary current implementation evidence:

- `data/ddm_build_copy/build_determinicity_wave_shard_v550.py`
- `data/ddm_build_copy/ddm_v550_distributions.py`
- `data/ddm_build_copy/ddm_v550_position_distribution.py`
- `data/ddm_build_copy/ddm_v550_branching.py`
- `data/ddm_build_copy/ddm_v550_clouds.py`
- `data/ddm_build_copy/ddm_v550_shared_respondent_substrate.py`
- `data/ddm_build_copy/build_v550j_prepared_substrate.py`
- `data/ddm_build_copy/compile_v550j_joint_response_patterns.py`
- `data/ddm_build_copy/ddm_v550j_joint_patterns.py`

Binding governance:

- `data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/14_D07_D08_D10_D11_RETURN_ADJUDICATION.md`
- `data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/02_RESOURCE_INDEX.md`

## 11. Non-conclusions

D14A does **not** decide:

- which current artifacts are semantically necessary;
- which computations may be removed;
- whether a proposed sparse conditional architecture is equivalent;
- any replacement savings;
- any future materialization policy;
- any production cardinality, prevalence, completeness, overlap, loss rate, CPU, RAM, wall-clock, bytes, or DB I/O.

Those questions remain outside this non-dispositive feeder and, where specified by campaign law, blocked on D12/D13 semantic/replay closure.
