# DDM VOSKRES #1059 — Investigator A first pass (forward, documentary)

- Job: `voskres1059-forward-a-firstpass-20261115-r1`; session `ses_e22479ffdffesgfJ1bpwA8uqs1`
- Host `oldMac.lan`; checkout `/Users/matthewsmith/.codex/worktrees/voskres1059-forward-a/Rawlsing`
- Branch `codex/voskres1059-forward-a-20261115-r1`; frozen start / controlling spec `b9325f094b27d28c20006af9780a91b3254dcab8`
- Original source pin inspected: `25830fe7462bb9e29bc4087e6ae14f3f84cec377`
- Modern comparison inspected: `3e0ed0794498506520ae62c997a5c852ac672061` (#1006 R2 named locality)
- Grade vocabulary: SOURCE_ONLY (code read at pinned blob), OBSERVED_LOG (none in this pass), INFERENCE. No execution, tests, imports, raw respondent bytes, benchmarks, or other worktree/branch read.
- Status: finite tract inspected only; no global completeness, runtime, source-right, or native-equivalence claim.

## 1. Forward execution map (old source, SOURCE_ONLY)

1. **Source extraction.** `build_determinicity_repository_v550.py:722-798` `_prefetch_question_rows_by_country` issues **one Postgres query per country** for the shard's source/wave and all selected var aliases (`REGEXP_REPLACE(UPPER(var_code)...) = ANY(...)`, `ORDER BY var_code, respondent_id`), returning frames indexed by `var_code` (duplicate index). If the shard has more than one source it returns `{}` and the per-question path is used.
2. **Prepared question cache.** `build_determinicity_repository_v550.py:801-862` `_prepare_v550_question_row_cache` harmonizes the country frame **once per country** (`mode=country`) or in 100k chunks (`mode=chunked`), then reindexes by `var_code`. `mode=off` disables it. In-memory only; lifetime is one shard process.
3. **Question loop.** `build_determinicity_wave_shard_v550.py:1506-1661`: per question, `_question_rows_from_cache` (`repository:866-917`) slices the country frame by alias mapping; on empty it falls back to **one SQL query per question** (`repository:679-719`) and then harmonizes that fallback (`shard:1520-1549`). Checkpoints per question are written after each table; `--resume` skips existing checkpoints and `--resume-from-checkpoints-only` skips the loop entirely (`shard:1487-1512`, `repository:940-1000`).
4. **Per-question analytical families** (`shard:1591-1661`): distributions (pooled + country), 12-indicator position summaries, secondary-indicator joint gains, indicator matrix, outlier cohorts, recursive branch nodes, and optional cloud/co-signature tables. Each is checkpointed, accumulated, later concatenated and written as ~26 shard tables (`shard:1977-2014`).
5. **V549 respondent alignment.** `build_branch_co_signature_summary_v549.py:494-557` reads respondents and pivots the selected variables to a respondent×variable wide frame **once per source** in the scan; `:449-491` `build_branch_mask` recursively composes branch masks and memoizes by node id in a per-question-tree dict; `:712-747` builds masks and co-signatures per V548 node. `build_question_response_attitude_cloud_summary_v549b.py:322-376` repeats the same recursive mask idea per question with a per-question dict.
6. **V550J prepared substrate.** `build_v550j_prepared_substrate.py:316-522` loads a per source/wave/country parquet cache and validates a signature over authority compendium hash, question-family registry hash, response-semantics contract hash, view-schema hash, and compiler version; `prepared_required` raises if missing, other modes build or fall back. `compile_v550j_joint_response_patterns.py:1607-1828` loads/reuses a prepared country frame per `(source,wave,country)` in `country_prepared_state`, otherwise prefetches country rows; `:1942-1960` compiles family tables. `ddm_v550j_joint_patterns.py:4925-4979` summarizes respondents/patterns (answered-item counts and support), item/boundary/relation/position indexes and pattern membership per family.
7. **Handoffs/first consumers.** The V550 shard writes `v551_bridge_index` through `ddm_v550_bridge.build_bridge_*` (`shard` imports at `:61`); V551 atoms consume the bridge (`compile_v551_relation_evidence_atoms.py:176-187`); V552 consumes the V551 producer bundle and optional conditional determinicity parquet (`compile_v552_structural_ddm.py:291-309`); V551J consumes V550J pattern/item/relation indexes and manifest (`compile_v551j_joint_evidence_packets.py:140-167,277-282`). These are code-level consumers; no historical run witness was inspected.

## 2. Work shared / repeated / retained / recomputed

**Genuinely shared (old):**
- Country-level response fetch + harmonization across all questions in a shard (V550), with per-question SQL only as fallback.
- Respondent×variable wide pivot and recursive branch-mask memoization within a source/question tree (V549/V549b).
- Per-family/per-country prepared V550J substrate with a signed on-disk cache and country-level reuse across families.
- Output checkpointing per question, allowing resume to skip completed question work.

**Repeated or recomputed (old):**
- Baseline `H(Y)` and dominant response are recomputed independently in `indicator_summary_rows`, `secondary_indicator_summary_rows`, `branch_nodes_rows`, and `outlier_cohort_rows` on the same question frame (`ddm_v550_branching.py:143-200,203-325,372-465`).
- Conditional entropy over the same indicator/response pairs is recomputed in the indicator summary and again while selecting the primary/secondary indicators; no shared contingency/count table.
- Secondary joint gains are an O(k²) pass over indicators with joint masks recomputed per candidate (`branching:276-325`), not a single grouped joint count.
- V549 and V549b each re-derive recursive branch masks; the two cloud builders do not share a mask cache (source inspection; no import of one by the other).
- The V550 in-memory question cache is not the on-disk `ddm_v550_shared_cache`; that module is used by V550J country-slice caching (`compile_v550j_joint_response_patterns.py:33,1016+`). Cross-process reuse of the V550 question cache was not found in the inspected shard path.

## 3. Cache lifetime, invalidation, fallback

- **In-memory V550 question cache:** one shard run; keyed by country frame, sliced by alias; no TTL. Invalidation = new process/args. Fallback = per-question SQL when the slice is empty; empty SQL is counted as skipped and checkpointed (`shard:1519-1534`). This is a **routing/empty-cell** fallback, not proof of missing source questions.
- **On-disk shared cache:** `ddm_v550_shared_cache.py:65-125`; SHA-256 over `{cache_format_version:v2, payload}`, stored as `data.parquet` + `meta.json`; a signature mismatch or unreadable metadata returns `None` and the caller recomputes. No TTL. This is content-addressed invalidation.
- **V550J prepared substrate:** signature check at `build_v550j_prepared_substrate.py:298-370`; invalid/missing cache rebuilds when mode permits; `prepared_required` fails closed (`:373-374`). Per source/wave/country.
- **Checkpoints:** per-question parquet keyed by index + question key; resume trusts existence (`repository:953-1000`). No content hash on the cheap existence check; a corrupt/stale checkpoint is not detected by that path.

## 4. Substantive T/S/M and defect notes

See `TSM_FUNCTION_MAP.tsv`. Key scientific/statistical caution (SOURCE_ONLY): `indicator_summary_rows` computes `baseline_h = H(Y)` over **all question rows**, but `conditional_entropy` and `MI` over rows where the indicator is non-empty (`branching:145-161`). The clipped `ENTROPY_REDUCTION` and `MUTUAL_INFORMATION` fields therefore mix populations; `normalized_mutual_information` uses only the masked pair. Secondary gain has the same baseline/mask mismatch and compares a primary conditional entropy computed on the primary mask with a joint entropy on the intersection mask (`branching:269-289`). This is a **conditional-population / denominator defect**, not merely a naming issue. Pooled vs country distributions use different denominators by `groupby` (`ddm_v550_distributions.py:255-309`), and zero/special/DK values are separated by semantics flags rather than silently counted (`distributions.py:149-205,255-262`). Weights are classified once and positive-finite only (`ddm_v550_metrics.py:32-51`); unweighted/partial/invalid statuses are propagated. No historical output values were read, so the empirical magnitude of these defects is UNKNOWN.

## 5. FORGE comparison touched (SOURCE_ONLY, no equivalence claim)

At `3e0ed0794498506520ae62c997a5c852ac672061`:
- `rawlsing_next/pre553_empirical_query.py:490-538` defines `I03GroupedExecutionScope`: execution-local, nonauthoritative memo of measure-independent I03 cores with `max_groups=64`, `max_cached_members=500_000`, stats, and an explicit rule that weighted aggregation and all native facts/replay are recomputed per operation (`_pre553_query_eval.py:314-358,564-623`).
- Core sharing is **opt-in and gated**: `_evaluate_index_group_core` rejects sharing under an opt-in runtime successor binding and requires an unmodified sealed release index (`_pre553_query_eval.py:404-431`); `execute_empirical_query` rejects grouped reuse for the cold S2-C `DirectEstateI03Session` (`pre553_empirical_query.py:756-757`).
- `pre553_batch_runner.py:386-470` schedules units deterministically and treats cache/materialization presence as non-authority; no semantic batching of compatible groups is implemented in that scheduler.
- Therefore the modern grouped core is a real partial analogue of V549/V550 shared membership/denominator preparation, but it is not enabled on the cold direct estate and has no inspected production/batch first-consumer witness. `PRESENT_PARTIAL`, not `PRESENT_EQUIVALENT`.
- #1006 R2 at this commit remains sourcefree TEST_ONLY: 543.026 s → 294.087 s selected 100k, not production. No old runtime measurement exists in this pass, so **HISTORICAL_RUNTIME_UNKNOWN**; no “old was faster” claim.

## 6. Common-cause and counterexamples

See `FORGE_FATES_AND_COUNTEREXAMPLES.md`. Strongest counterexample to a simple common-cause story: the old source itself recomputes entropy/conditionals per family and contains a population-mixing MI defect, so “lost shared computation” is not identical to “lost scientific correctness.” Modern code has a genuine exact grouped core, so absence is not proven. Tags used: `RELATED_UNPROVED` for the V550 shared-prep ↔ modern grouped-core economics link; `FUNCTION_ONLY` for bridge lane/identity semantics; `PERFORMANCE_ONLY` for question-cache lifetime; `INDEPENDENT` where source-level reuse and statistical correctness are separable. No `SHARED_CAUSAL_LOSS_PROVED`.

## 7. Smallest evidence-backed recommendations (route only, do not implement)

1. **#960 / W05-P03:** document and measure `I03GroupedExecutionScope` at the already-specified 1k/10k/100k × 1/100/1000 batch. It already implements the old “prepare membership/denominator once, rematerialize measure per operation” pattern; the missing item is a first-consumer/witness and capacity behavior, not a new engine.
2. **#1006 owners:** before extending sharing, test whether the cold `DirectEstateI03Session` block (`pre553_empirical_query.py:756`) is a qualification gap or a semantic constraint; if qualification, add a bounded grouped-core parity test against the native path. No production switch.
3. **W05/P03:** if porting V550 entropy/information functions, consolidate baseline/conditional contingencies per `(question, condition set, weight regime)` and **fix the population denominator explicitly**; do not reproduce the old all-rows-vs-masked mismatch.
4. **V551/V552 owners:** test the bridge reduced-identity payload (`ddm_v550_bridge.py:804-860`) for noninjective collapse of distinct secondary/branch rows before relying on bridge counts; source-only suspicion, no observed drop.
5. **#960:** add checkpoint content identity (hash or semantic key) to resume validation; existence-only resume can trust a stale/foreign checkpoint (`repository:972-1000`). Documentary finding only.

## 8. Weak claims / missing pieces

- No historical execution logs, operation counts, wall/RSS/IO, or output row counts were inspected: historical runtime and actual reuse frequency are UNKNOWN.
- ZAK-02S `098ea6bea0ef37177fecb185a5c97dd8824216ba`, ZAK-03S `21bbe210a068001e99785ac954618a14be93b1bc`, ZAK-04S `69804f88abc8e84cf91ee256aa66fb607a49f5a7` and correction `89768120d391c385ec81f15f3f035281c7361cb4` are **absent locally** (`git cat-file` fatal). Recorded as NOT_INSPECTED; #1058 controller at `14b232b76eedffa005db4456eaacfc1ed0b4a7a4` was used only for intake orientation.
- The V550 `_question_rows_from_cache` alias/multiselect path and the prepared-substrate signature fields were read, not executed; semantic equality of fallback vs prepared is INFERENCE-limited.
- No V551/V552/V551J historical output file or first-reader invocation was read; consumer claims are code-import claims.
- `ddm_v550j_joint_patterns.py` is 5,286 lines; only the family-compilation entry, pattern/membership/denominator helpers, and association scaffolding were inspected. Other family-specific branches are UNINSPECTED.

## 9. Finite uninspected territory (explicit)

V551/V552/J runtime input files and actual historical runs; V549b full anchor loops beyond masks; V550 cloud emission thresholds; V550J family registry contents; all modern output/first-consumer paths beyond the named files; any old `_pre553_*` performance logs; ZAK 02S/03S/04S source objects (absent). NOT_INSPECTED ≠ NOT_FOUND.

## 10. Commit

Owned return committed at the exact 40-char SHA reported in the controller receipt; no push, no PR, no other path modified.
