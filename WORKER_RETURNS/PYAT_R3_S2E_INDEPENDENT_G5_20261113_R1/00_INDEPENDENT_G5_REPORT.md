# PYAT R3 S2-E — Independent Nonauthor Native Execution and G5

**Disposition:** `ACCEPT_SCOPED@S2_SOURCEFREE_NATIVE_F1_F4_I05`

- Original obligation: P2-06, [#919 S2-E](https://github.com/maidiu/rawlsing/issues/919), [#909 R3C/R3S](https://github.com/maidiu/rawlsing/issues/909), Codex HQ [#960](https://github.com/maidiu/rawlsing/issues/960), PYAT PROGRAMMA / MCR-lite.
- Frozen production code/test/workflow SHA: `81a764cc7eac960f0fd607d9c3fe62428905daa4`.
- Documentary/author delivery HEAD: `1f787305f2f712f8a45e937cde7ee4b7a3be741e`.
- Previous accepted B2 repair ancestor: `2132932b920e3572068cd8d4fcf8fae5cc2957f9`.
- PR: [#973](https://github.com/maidiu/rawlsing/pull/973) (draft; no protected merge).
- Independent review branch: `review/pyat-r3-s2e-independent-g5-20261113-r1`.
- Return directory: `WORKER_RETURNS/PYAT_R3_S2E_INDEPENDENT_G5_20261113_R1/`.

This is an independent receiving result, not an A/B author round. No author branch, protected PRE-MAIN, original science issuer, or paused W03/W04 path was modified.

## 1. Prior independent G5 search

All 3668 remote branch tips were fetched and searched. No independent S2-E G5 receipt exists at the frozen delivery HEAD. The only S2-E refs are author A/A2/A3/B/B2 branches plus a post-freeze author **test-only** repair (`7b19a242...`). The #980 combined receiving covers S1-B, S1-D, S2-F and S2-G only; S2-E is absent. Issue API reads returned HTTP 403 for the available token, so contract reconstruction used the commission, the frozen author returns and the frozen code/tests. Details: `evidence/10_PRIOR_G5_SEARCH.txt`.

## 2. Lineage and custody (G1)

- `git merge-base --is-ancestor 2132932... 81a764cc...` → **YES**.
- `git merge-base --is-ancestor 75d4a24... 2132932...` → **YES**.
- A3 changes relative to B2 are exactly three files: `rawlsing_next/pre553_s2e_exact_conservation.py`, `rawlsing_next/tests/test_pyat919_s2e_a3_native_closure.py`, `.github/workflows/pyat-r3-s2e-a.yml`.
- B2 code changes relative to A2 touch only the conservation verifier, its B2 test and the workflow. The native I03 evaluator, I05 producer, Batch runner, issued-workload consumer and object contracts are **unchanged**.
- The post-freeze test repair `7b19a242ebc9edf85bf8303be33338f860eabf65` is a child of `81a764cc`; its diff is only the B2 falsifier's ref normalization. The production-tree diff against `81a764cc` is **empty**.
- Hashes and exact diff: `evidence/12_GIT_IDENTITY.txt`.

## 3. Execution at the frozen SHA (G2–G4)

Environment: macOS 13.7.8, Intel i9-9880H, Python 3.11.3, pytest 9.2.0, pandas 3.1.1, pyreadstat 1.3.7, pyarrow 26.0.1, duckdb 2.0.0 (`evidence/09_ENVIRONMENT.txt`). A dedicated temp venv was used; the frozen code worktree was sparse (`rawlsing_next` + `.github`, 13 MB) at `81a764cc`.

### 3.1 Frozen native/hostile/regression suite

```sh
PYTHONPATH=. python -B -m pytest -q -s -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat919_s2e_a3_native_closure.py \
  rawlsing_next/tests/test_pyat919_s2e_b2_fate_counterexample.py \
  rawlsing_next/tests/test_pyat919_s2e_a_whole_native_batch.py \
  rawlsing_next/tests/test_pyat919_s2e_a_counterattack.py \
  rawlsing_next/tests/test_pyat919_s2e_a_conservation.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_universal_workload_custody.py
```

- Collected **90**, passed **89**, failed **1**, skipped **0**; 122.31 s.
- The single failure is **test-only**: the frozen B2 falsifier calls `.as_dict()` on a frozen mapping ref (`AttributeError: 'mappingproxy' object has no attribute 'as_dict'`) while constructing its own replay material, before submitting anything to the native first consumer. It is not an implementation assertion failure.
- Exact log: `evidence/00_FROZEN_90_SUITE_RED.log`; timing/memory: `evidence/15_FROZEN_90_SUITE_TIME.log`.
- The 22-test S2-E core subset (A3/B2/B1/A2/A1 files) ran **21 passed, 1 failed** in 21.48 s with a sampled process-tree peak of **132.5 MiB**. Log: `evidence/02_FROZEN_CORE_22_SUITE_MONITORED.log`.

### 3.2 Test-harness correction execution

The existing author repair `7b19a242...` changes only the B2 falsifier's frozen-ref handling. A separate sparse worktree at that SHA, with production files byte-identical to `81a764cc`, executed the same nine files:

- **90 passed, 0 failed, 0 skipped**; 115.88 s.
- Process-tree peak RSS **312.7 MiB** (max single process 244.7 MiB, 2 live processes, 1430 samples).
- Full-output graph SHA256 remains `befb766af812995cdf06989d1afd83d3f250859df30a1f01968e6f808eef63d0`.
- Exact log: `evidence/03_TEST_REPAIRED_90_SUITE_GREEN.log`; details: `evidence/13_TEST_REPAIR_EXECUTION.txt`.

The independent equivalent B2 falsifier at the frozen code (`attacks/test_independent_b2_fate.py`) also passes: a fully rehashed `SUPPORTED → VALID_EMPTY` substitution is refused with `S2E_I05_CANDIDATE_SCIENTIFIC_FATE_MISMATCH`, then exact restoration passes. Log: `evidence/06_INDEPENDENT_B2_GREEN.log`.

### 3.3 Accepted S2-F preservation

```sh
PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat940_s2f_a_counter_provenance.py \
  rawlsing_next/tests/test_pyat940_s2f_b_negative_and_multisource.py \
  rawlsing_next/tests/test_pyat940_s2f_durable_closure.py \
  rawlsing_next/tests/test_pyat940_s2f_fresh_process.py
```

**19 passed, 0 failed, 0 skipped**; 10.00 s. Monitored tree peak **142.3 MiB** with 2 live processes (fresh-process case). Logs: `evidence/04_S2F_19_GREEN.log`, `evidence/05_S2F_19_GREEN_MONITORED.log`.

### 3.4 Native five-unit positive witness

`probes/s2e_positive_witness.py` executes the real five-unit native sourcefree Batch (`execute_i03` × 4, `execute_i05` × 1) and prints the full witness (`evidence/14_POSITIVE_WITNESS.log`):

- 12 synthetic respondents; 5 Batch units; calls `{query: 4, discovery: 1}`.
- I03 facts **4**; I05 facts **2**; I05 receipts **1**; candidate count **1**.
- F1 marginal `Y`: denominator 12, cells `0:10, 1:2` (complete two-value domain; exact rates `10/12`, `2/12`).
- F2 `Y|X=1`: independent denominator **6**, cells `0:5, 1:1` (exact `5/6`, `1/6`).
- F2 reversed `X|Y=1`: independent denominator **2**, cells `0:1, 1:1` (exact `1/2`, `1/2`); distinct member-ref set from the forward conditioner.
- F3 minority branch `G=C`: denominator **2**, `Y=1` count **2** vs all-baseline denominator **12**, `Y=1` count **2**; exact contrast `2/2 = 1` vs `2/12 = 1/6`; candidate `DISCOVERED_RESULT_SUPPORTED` / `EVALUATED_SUPPORTED`.
- F4 same-respondent `X×Y×Z`: arity 3; complete **8-cell** domain; supports `(0,0,0):5, (0,0,1):0, (0,1,0):0, (0,1,1):1, (1,0,0):0, (1,0,1):5, (1,1,0):1, (1,1,1):0`; total 12; zero cells are `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET`, not omitted. This is a genuine joint, not pairwise arithmetic.
- I05 receipt: `exact_query_contract_id = PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0`; `dependency_refs=6`; `authority_snapshot_refs=5`; `empirical_fact_refs=2`; executed predicates/queries 2/2; all three nonpromotion flags `False`.
- Provenance closure: F1 27 refs, F2 33/29 refs, F4 75 refs; denominator members are exact unique refs contained in risk members; `actual_source_file_opens_during_all_runs = []` (Python audit hook).
- Process max RSS (witness process) 31,657,984 bytes ≈ 30.2 MiB; Batch elapsed 0.0608 s.

The F3 recursive and counterpattern families were additionally executed from the inherited native tests:

- `test_recursive_subgroup_fork_preserves_exact_parent_ancestry` passed; targeted five-test F3/valid-empty bundle **5 passed** (`evidence/17_F3_MINORITY_RECURSIVE_SIMPSON_VALID_EMPTY.log`).
- Native I05 has no literal `COUNTERPATTERN` family; the exact counterpattern-family analogue `CONDITIONAL_REVERSAL_OR_SIMPSON` passed (`test_simpson_reversal_is_detected_from_exact_pooled_and_stratified_facts`), and the AT10 minority/counterpattern fixture passed with modal/minority/counterpattern groups 10/8/2 (`evidence/18_AT10_COUNTERPATTERN.log`).
- AT14 state-distinction tests **11 passed**: observed zero vs zero support vs valid empty vs underpowered/insufficient support vs unresolved/unknown vs unvisited vs noncomparable vs authority-blocked vs integrity failure (`evidence/19_AT14_STATE_DISTINCTIONS.log`).

### 3.5 Changed legitimate input and exact restoration

The positive witness reruns the same five-unit Batch on a changed legitimate sourcefree input (all respondents `Y=1`):

- The discovery fate changes from `DISCOVERED_RESULT_SUPPORTED` / `EVALUATED_SUPPORTED` / `valid_empty=False` to **`VALID_EMPTY` / `EVALUATED_VALID_EMPTY` / `valid_empty=True`**.
- The frontier and replay identities change to new exact refs; F1/F2/F4 facts also re-identify.
- Re-running the original input restores the complete native output graph exactly: `restore_identical=true`; full-output SHA256 before and after = `befb766af812995cdf06989d1afd83d3f250859df30a1f01968e6f808eef63d0`.
- This is an actual scientific fate change, not a receipt relabel.

### 3.6 Resource and scope facts

- Zero actual `.sav/.dta/.parquet/.csv/.rdata/.rds/.xpt` source opens during all witness runs; the synthetic C11 release was already constructed in memory. The native Batch test also reports `source_opens_during_batch: 0`.
- Full frozen 90-test process high-water from `/usr/bin/time -l`: 258,904,064 bytes ≈ **246.9 MiB**. Test-repaired 90-test process-tree peak: **312.7 MiB**.
- Temporary disk: sparse code worktree **13 MB**, test venv **399 MB**, evidence **< 1 MB**; 10 GiB free before/after. No persisted saved-store/scratch artifact was produced.
- **Not run / not claimed:** full S2-D compact cold saved-release consumer, 100,000-respondent / 6 GiB integrated workload, original35 native operation universe, production issuer currentness/revocation. This fixture is 12 respondents and a 5-unit sourcefree Batch; it is not a scale or economy claim.

## 4. Hostile repairs and negative controls (G3)

The four new A3 native-closure tests execute and pass:

1. `test_a3_rehashed_structural_or_actor_promotion_is_not_native_discovery` — self-rehashed `structural_truth_effect`, `actor_v3_effect`, or `diagnostic_score_is_empirical_fact` promotion is refused with `S2E_I05_NONPROMOTION_FLAGS_MISMATCH`; exact restoration passes.
2. `test_a3_rehashed_wrong_query_contract_is_not_native_i05` — wrong I03 query-execution contract is refused with `S2E_I05_QUERY_EXECUTION_CONTRACT_MISMATCH`.
3. `test_a3_rehashed_native_dependency_and_authority_loss_is_refused` — removed dependencies or authority snapshots are refused with `S2E_I05_DEPENDENCY_CLOSURE_MISMATCH` / `S2E_I05_AUTHORITY_SNAPSHOT_CLOSURE_MISMATCH`.
4. `test_a3_extra_self_consistent_executed_query_outside_issued_frontier_refused` — an authentic but unissued extra query object is refused with `S2E_I05_EXECUTED_OBJECT_CLOSURE_MISMATCH`.

Independent additional hostile variations (not speculative hardening; targeted at the remaining additive risk not covered by the published removal tests):

- Append a legitimate but non-native dependency ref and, separately, a non-native authority snapshot; both are refused with the same exact closure codes and exact restoration passes (`attacks/test_independent_a3_additive.py`, `evidence/07_INDEPENDENT_A3_ADDITIVE_GREEN.log`).
- Append a legitimate but unissued extra executed predicate outside the I05 role set; refused with `S2E_I05_EXECUTED_OBJECT_CLOSURE_MISMATCH` (`attacks/test_independent_a3_predicate.py`, `evidence/08_INDEPENDENT_A3_PREDICATE_GREEN.log`).

Retained earlier repairs and defenses (all executed in the 90-test suite): B2's fact-derived scientific fate (independently reproduced), B1's valid-empty/frontier replay refusal, A2's candidate identity/replay/ancestry/whole-roster refusals, A1's full-output/declared-domain/Batch result-graph refusals.

**Strongest negative:** a fully rehashed, structurally valid receipt and outer frontier that changes a genuinely `SUPPORTED` minority discovery into `VALID_EMPTY` is refused by the native fact-derived validator; the exact original graph restores. No native first-consumer counterexample survived.

**Disclosed evidence defect:** the frozen B2 falsifier itself is red for the test-only `.as_dict()` reason above. The implementation check it targets is valid and independently reproduced. The author test-only repair `7b19a242...` makes the suite green with an empty production diff. No production repair is requested and no new A/B round is opened.

## 5. G1–G5 evaluation

| Gate | Evaluation |
|---|---|
| G1 — original operation/science preservation | **PASS_SCOPED**. Verified ancestry; A3/B2 touch only the conservation verifier/tests/workflow; native I03/I05/Batch objects unchanged; genuine F1–F4/I05 facts and discovered-claim identity retained; exact source/authority/dependency/role closure; valid-empty/support/negative fates retained; no structural/causal/actor/diagnostic promotion. Original35 issuance is not proved. |
| G2 — real native positive | **PASS_SCOPED**. Actual five-unit native Batch and I05 first consumer executed; F1 complete marginal, F2 both independent denominators, F3 minority/recursive/Simpson-counterpattern, F4 genuine 3-way same-respondent joint; zero/unknown/not-applicable/unsupported/underpowered/valid-empty distinctions; exact denominator/risk/provenance/Fraction closure; changed input produces a real discovery-fate change and exact restore. |
| G3 — attack latest repairs | **PASS_SCOPED**. Four A3 controls pass; additive dependency/authority and extra-predicate variations pass; B2/B1/A2 defenses pass; strongest false scientific fate refused. Frozen test-harness defect disclosed and independently proven test-only. |
| G4 — execute, measure, distinguish | **PASS_SCOPED**. Exact commands, 89/90 frozen + 90/90 test-repaired, 19/19 S2-F, process-tree RSS, zero source opens, hashes and restore recorded. S2-D saved reader and 100k/6 GiB workload explicitly NOT_RUN. |
| G5 — independent disposition | **ACCEPT_SCOPED@S2_SOURCEFREE_NATIVE_F1_F4_I05**. |

## 6. Disposition and holds

**Accepted:** the sourcefree native S2-E production code at `81a764cc...`, with the existing test-only harness correction `7b19a242...` adopted for a green suite (production tree byte-identical). The demonstrated grade is sourcefree engineering: synthetic 12-respondent native F1–F4/I05 closure, not original35 source science.

**Explicitly not accepted / preserved holds:**

- No original35 native operation universe, source issuance, production issuer currentness, revocation, causal/structural effect, actor V3/persona or human-consent authority.
- No full S2-D compact cold saved-release consumer; no 100,000-respondent/6 GiB integrated workload or economy claim.
- No protected PRE-MAIN merge, author-branch rewrite, or W03/W04 activation.
- Issue comments could not be posted because the available token returned HTTP 403; the committed branch/return is the durable notification (`evidence/11_ISSUE_NOTIFICATION.md`).

**Integration unlock:** S2-E is terminal at the demonstrated sourcefree engineering grade. This acceptance explicitly unlocks the full upstream native **S2-E → durable S2-F → learned S2-G** integration, subject to the still-unbuilt actual saved-reader **S2-D** and independent combined receiving. It does not itself perform or accept that combined integration.

**STOP:** no new A/B round, no optional hardening, no invented source/causal/actor authority. Execute, receive, close.
