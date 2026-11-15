# DDM VOSKRES #1059 — bounded A/B reconciliation (lane B)

Status: final bounded correction. First-pass artifacts in this directory are preserved verbatim.
This file and appended `SOURCE_LEDGER.tsv` correction rows are the only new evidence.

- A frozen return: `f36276f33ab88992460235a60ca3f9ca71068557:WORKER_RETURNS/DDM_VOSKRES1059_A_R1/`
- B frozen return: `1291880f7d04fc3e752c440fa86a63b94d7142ec`
- Original source: `25830fe7462bb9e29bc4087e6ae14f3f84cec377`; A modern source: `3e0ed0794498506520ae62c997a5c852ac672061`; B spec-head modern source: `b9325f094b27d28c20006af9780a91b3254dcab8`
- Method: read opponent committed files via `git show`; exact old/new code lines; ZAK objects via `git show`/`git grep`. No execution, tests, raw respondents, other worktree, or branch writes.
- Historical runtime remains `HISTORICAL_RUNTIME_UNKNOWN`. Source-only findings are not historical runtime faults or live regressions.

## 1. Checkpoint discrepancy — exact resolution

| Claim | Exact source | Verdict | Corrected outcome |
|---|---|---|---|
| A: per-question checkpoint resume "trusts existence"; "no content hash on the cheap existence check"; "corrupt/stale checkpoint is not detected by that path" (A `00_RETURN` §3; A ledger row 5; A TSM M-A-005) | `build_determinicity_repository_v550.py:972-992` | **REJECTED as blanket; QUALIFIED** | The function checks the complete marker, the `question_use_contract` parquet exists and is readable, has a nonempty saved `question_use_contract_hash`, and that value equals the current recomputed hash (`:963-969`). A's existence-only statement is false for the contract table and for the skip decision that calls it (`build_determinicity_wave_shard_v550.py:1509`, `:1489-1499`). |
| B: "resume verifies question-use-contract hash" (B `00_RETURN` finding 8; B-08) | same lines | **CONFIRMED; QUALIFIED** | Only the contract table and its recomputed hash are guarded. Other per-question body parquets (distributions, indicator/secondary/branch/cloud tables) have no per-body hash; `_question_checkpoint_complete_path` is a text existence marker (`:953-960,995-1002`). Source/version changes are caught only insofar as they change the current question-use-contract hash. |
| A recommendation: add checkpoint content identity/hash to resume validation | A `00_RETURN` §7.5 | **INVALIDATED / do not implement** | A redundant contract-hash guard is not justified; it already exists. A body-level guard would need an observed stale/corrupt body failure first, not a documentary suspicion. No new checkpoint infrastructure recommended. |

## 2. Priority challenges

| Issue | A position | B first-pass position | Exact source read now | Verdict and correction |
|---|---|---|---|---|
| V552 conditional determinicity | A ledger row 23: "V552 consumes the V551 producer bundle plus optional conditional determinicity parquet." | B: accepted and unused beyond signature/provenance/empty audit. | `compile_v552_structural_ddm.py:299-309` reads parquet and passes it; `ddm_v552_structural.py:253-259` uses it only in the signature and an empty `conditional_determinicity_status_audit`; `ddm_v550_schema.py:1617-1631` requires path/hash/row count in the V552 input-provenance manifest; V551J packet builder has no conditional-index input and derives `conditional_support_packet` from V550J association (`ddm_v551j_packets.py:244-253,625-635`); V552J joins only V551J packets to V552 structural facts (`ddm_v552j_handoff.py:131-140`). | **A REJECTED as "consumes"; B CONFIRMED and strengthened.** ZAK03 R2 already banked this exact dead socket (blob `0df56d70...`, lines 253-259) as "historical local dead socket, not established absence of every successor." B's provenance-manifest and V551J/V552J bounded successor checks are additional detail, not a new capability discovery. Do not claim universal absence. Tag `FUNCTION_ONLY`. |
| V549 branch-mask predictors | A ledger rows 9-10: wide pivot and recursive mask reuse; no demographic-availability warning. | B: `load_source_frame` blanks demographic columns, then passes `respondents` as the position frame. | `build_branch_co_signature_summary_v549.py:518-524` sets sex/age/education/income/religion/urban_rural/age_group blank; `:681` loads respondents+wide; `:725` calls `build_branch_mask(..., respondents, cache)`; `:449-491` compares parent predictor against `position_df`. V549b loads six of the fields at `:201-231` and repeats the mask builder at `:322-375`. | **B CONFIRMED at code-path level; A INCOMPLETE, not contradicted.** Effect on actual V548 trees is INFERENCE because the predictor inventory/outputs were not inspected. This is the strongest genuinely new B item versus A; no ZAK02/ZAK03 term-search hit for these blanking lines was found in the portions read. Do not call every historical branch empty, and do not call it a runtime fault. |
| V550J "MI" | A does not claim it; A's V550J row is pattern/denominator compilation. | B: field named `mutual_information` is a scaled log-ratio. | `ddm_v550j_joint_patterns.py:4278-4285`: `mi = log2(p_given_pattern / baseline_share) * pattern_count_unweighted / family_count`; denominator fields at `:4384-4405` include pattern member, answered-var-within-pattern, response overlap, baseline answered, eligible rows. | **B CONFIRMED for the inspected association branch.** It is not 2×2/joint MI and not a signed MI; it is a weighted log-lift scaled by pattern prevalence. Other association lanes are `NOT_INSPECTED`. ZAK03 T0014 co-travel is related but was not matched to this formula in the portions read; novelty is bounded. |
| Modern grouped scope | A at `3e0ed...`: `I03GroupedExecutionScope` is execution-local, nonauthoritative, max 64 groups/500k members; core sharing opt-in and sealed-index only; cold `DirectEstateI03Session` grouping rejected; batch runner treats cache as non-authority. | B at spec HEAD `b9325f...`: exact diagnostics and grouped core exist; modern comparison incomplete. | `3e0ed...:rawlsing_next/pre553_empirical_query.py:490-538` (scope docstring, limits); `:756-757` (cold direct estate rejection); `3e0ed...:rawlsing_next/_pre553_query_eval.py:404-431` (runtime-binding/sealed-index rejection); `3e0ed...:rawlsing_next/pre553_batch_runner.py:386-391` (no cache-hit authority). | **A CONFIRMED; B modern scope was narrower and is corrected.** A's `3e0ed...` evidence supersedes B's spec-head-only modern claim for grouped execution. Still source-only: no production first-consumer witness, no native/cold grouped positive, no runtime measurement. `PRESENT_PARTIAL`, not equivalent. |
| Masked MI population vs weighting | A: baseline all rows vs conditional indicator-observed; secondary primary vs intersection masks. | B: same population defect; NMI/diagnostic fields also mix regimes. | `ddm_v550_branching.py:145-161,203-325`; `ddm_v550_metrics.py:32-51,67-97,123-140`. | **BOTH CONFIRMED, with distinct additional caveats.** (i) Population: H(Y) baseline all rows vs H(Y\|X) indicator-observed. (ii) Weights: MI uses optional weights in both entropy terms; `normalized_mutual_information` calls unweighted `distribution_entropy` on the masked pair, so MI and NMI can disagree by weight regime, not only population. (iii) `classify_weight_status` keeps only positive finite weights and `conditional_entropy` fills invalid weights with 0 without per-subgroup renormalization. (iv) `dominant_response_pct_unweighted` and `_weighted` are both assigned the same baseline dominant percentage (`branching.py:194-195,257-258`). (v) Secondary `secondary_gain` compares primary-mask conditional H with intersection-mask joint H, while the emitted baseline/conditional columns are the candidate's own. These are separate caveats; do not reduce them to one "masked MI" story. |
| Pooled vs country distributions | A: separate groupbys/denominators; pooled scope label may be narrower for multi-country input; caller must be established. | B: inspected wave-shard path is country-keyed, so pooled equals country there; function-level risk only. | `ddm_v550_distributions.py:252-312`; `build_determinicity_repository_v550.py:866-897` selects the cache by question-row `country_code`; `_prefetch_question_rows_by_country` at `:722-798` returns `{}` for multiple sources and prefetches one frame per country. | **BOTH CONFIRMED at their scopes; B's "pooled equals country" must not be generalized.** It holds for the inspected wave-shard path. Legacy/other callers were `NOT_INSPECTED`; the function-level multi-country risk remains. A's caution is retained. |
| Common cause / absence | A: no `SHARED_CAUSAL_LOSS_PROVED`; modern grouped core is real but opt-in and cold-blocked; old MI defect separable. | B: same conservative tags. | A and B ledgers; `3e0ed...` grouped guards; old per-question recomputation. | **AGREEMENT.** No shared-causal-loss proof. Modern code absence is not established: exact diagnostics and a guarded grouped core exist. No old-product first consumer was proved by either pass. Tags remain `RELATED_UNPROVED` (shared-prep/economics), `PERFORMANCE_ONLY` (cache/prefetch), `FUNCTION_ONLY` (conditional lane), `INDEPENDENT` (MI correctness). |

## 3. ZAK objects newly read in this correction — differential only

| Object | Portion actually read | Differential finding |
|---|---|---|
| ZAK02S `098ea6bea0ef37177fecb185a5c97dd8824216ba` | `UNIFIED_LOG_R1/ZAK02_AGENTB_RECON_20261114/R10_V550_MISSING_DISTRIBUTIONS_AND_METRIC_SEMANTICS.md` (full R10 narrative) | T0026 already banked the all-rows vs indicator-observed MI defect, weighted/unweighted indicator selection, and duplicated dominant pct fields; T0027/T0028 already banked pooled/country denominators and the `allowed_as_response_distribution` veto. B's B-09/B-13 are reconfirmations, not new discoveries. |
| ZAK03S `21bbe210a068001e99785ac954618a14be93b1bc` | `UNIFIED_LOG_R1/ZAK03_SOURCE_AUTHORITY_RECON_R3/00_RETURN.md` (opening through R2 terminal); `R2_SOURCE_COUNTERSEARCH_AND_DEFECTS.md` items 1-8 | ZAK03 R2 item 7 already recorded the V552 conditional dead socket at the same blob/lines and explicitly refused "absence of every successor." B's V552 finding is confirmation plus bounded V551J/V552J successor detail. R3 also records 14 provisional T and zero newly proved same-grain current QSM first readers; not recreated here. |
| ZAK04S correction `89768120d391c385ec81f15f3f035281c7361cb4` | `UNIFIED_LOG_R1/ZAK04S_CODEX_CAMPAIGN_R1/00_RETURN.md` sections 1-2.6 | Reinforces two cautions used here: a static importing reader is not selected numeric consumption (F6M/F6P), and a false-negative path glob was corrected to preserve `NOT_INSPECTED != NOT_FOUND`. No direct V551/V552 conditional evidence; no branch acceptance inferred from file existence. |

No ZAK inventory was recreated. Prior first-pass `NOT_INSPECTED` items remain historical; the above is the exact newly read portion.

## 4. What is genuinely new vs already banked

**New or strengthened in bounded B scope (documentary, no T minted):**
1. V549 blank-demographic predictor code path (`:518-524,725`) as a concrete mechanism defect omitted by A and not located by ZAK02/ZAK03 term search.
2. V550J association field named `mutual_information` is a scaled log-lift, not MI (`:4278-4285`), with the multi-denominator ledger already visible beside it.
3. V552 conditional determinicity is provenance-recorded and V551J/V552J do not supply an alternate consumer, beyond ZAK03's already-banked local dead socket.
4. Checkpoint scope correction: contract-hash guard proven; body tables unguarded; redundant hash guard rejected.

**Already banked / reconfirmed, not new:**
- V550 indicator MI population defect (ZAK02 T0026).
- Pooled vs country distribution denominators and permission veto (ZAK02 T0027/T0028).
- V552 conditional dead socket (ZAK03 R2).
- Recursive top-two tree, secondary gain, minority classification (ZAK02 provisional T0023-T0025).

**Not claimed:** no new T identity, no historical runtime, no observed output magnitude, no modern absence, no live regression.

## 5. Finite old → successor → FORGE dispositions (inspected region only)

| Old capability | ZAK status | FORGE inspected | Disposition | Evidence/falsifier |
|---|---|---|---|---|
| V550 indicator entropy/MI/NMI/Cramér V (T01) | ZAK02 T0026 banked | `rawlsing_next/pre553_diagnostics.py:243-365,622-752` exact arity-2 joint diagnostics | `PRESENT_PARTIAL_DIFFERENT_GRAIN`; old estimator defect must not be ported | Falsifier: a modern indicator-conditioned product with same population/weight semantics at a real consumer; not found in inspected files. |
| V550 secondary joint gain (T02) | ZAK02 provisional T0023 | none located | `COMPARE_UNKNOWN`/`NOT_INSPECTED` | Need a current consumer of secondary-gain rows; none inspected. |
| V550 recursive branches / minority (T03/T04) | ZAK02 provisional T0024/T0025 | none located; I05/Authority37 outside files | `COMPARE_UNKNOWN`/`NOT_INSPECTED` | Do not infer absence from I03 alone. |
| V550 distributions (T05) | ZAK02 T0027/T0028 | V551 direct atoms; modern I03 exact facts related | `PRESENT_PARTIAL`; signed handoff not proved | Need selected V553 consumer of signed distribution atoms; not inspected. |
| V551 conditional determinicity (T12) | ZAK03 R2 dead socket | V552 builder ignores; V551J/V552J no alternate consumer in inspected files | `FUNCTION_ONLY_GAP` / unresolved disposition | Need a real successor consumer or owner retirement; no hash guard. |
| V549/V549b recursive branch masks | no ZAK identity located in read portions; A generic | no exact modern successor inspected | `NOT_INSPECTED`/`COMPARE_UNKNOWN`; do not port until predictor inventory proved | Falsifier: V548 tree predictor list plus nonblank position columns; outputs not read. |
| V550J same-person patterns/denominators (T09) | ZAK03 T0014 related; formula not located in read portions | I03 exact joints related, not same-grain | `RELATED_UNPROVED`; old MI field must not be cited as MI | Need family/pattern-level parity and first consumer; not inspected. |
| Checkpoint/resume (M03) | A/B source | exact contract guard verified; body unguarded | `PRESENT` with scope correction | No new guard; body failure would need observed evidence. |

## 6. Highest 3 actionable recommendations for existing owners

1. **#960 / W05 / P03, plus existing I03/C11 owners.** Qualify or explicitly retain the cold `DirectEstateI03Session` guard on `I03GroupedExecutionScope` at the already-specified batch sizes; measure the guarded grouped core with a real first consumer. Source/falsifier: `3e0ed...:pre553_empirical_query.py:756-757` and `_pre553_query_eval.py:404-431`; if enabling grouping on cold direct estate raises or yields no measured batch benefit, no extension is justified. No new engine.
2. **Existing V551/V552 owners.** Close conditional determinicity as an explicit retired/handoff decision, or name a real successor consumer; do not leave an accepted-and-provenance-recorded input that the builder ignores. Source/falsifier: `ddm_v552_structural.py:253-259`, `compile_v552_structural_ddm.py:299-309`, `ddm_v551j_packets.py:244-253`; a real consumer importing the index and changing output would refute retirement. No redundant checkpoint hash guard (invalidated above).
3. **Existing diagnostics/entropy owners.** Require one common respondent population and one weight regime for any field called MI/NMI/entropy reduction; reject the old V550 estimator and the V550J scaled log-ratio label. Source/falsifier: `ddm_v550_branching.py:145-161`, `ddm_v550_metrics.py:67-140`, `ddm_v550j_joint_patterns.py:4278-4285`; algebraic constant-indicator and weight-regime counterexamples already show the defect without runtime data.

## 7. Would another archaeology tract add new information?

Yes, but bounded and not authorized here: (i) full V551J certification / V552J / real V553 successor chain for conditional determinicity; (ii) V548 predictor inventory plus one authorized synthetic check of V549 masks; (iii) V550J all association lanes and any genuine joint-MI consumer; (iv) historical run logs if any exist. These would add information; no global completion or conservation claim follows. This correction does not execute any of them.

## 8. Weak claims and residual uncertainty

- V549 mask effect is code-path inference; actual V548 trees/outputs were not read.
- V550J MI finding is bounded to the inspected association branch.
- V552 "dead end" is bounded to inspected producer/caller; ZAK03 already says not every successor is excluded.
- Modern grouped-core evidence is `3e0ed...` source-only; no production/native grouped run, no first-consumer witness.
- #1006 543.026→294.087 s remains a documentary intake figure, not independently verified here.
- Historical runtime and output magnitudes remain unknown; no old/fast or modern/slow claim is made.
