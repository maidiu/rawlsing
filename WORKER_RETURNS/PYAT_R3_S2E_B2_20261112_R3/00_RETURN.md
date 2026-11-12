# PYAT R3 / S2-E — Agent B2 bounded response to A2 counterattack

**Disposition:** \`B2_EXACT_IN_SCOPE_FATE_DEFECT_REPAIRED_IN_SOURCE__NATIVE_EXECUTION_UNVERIFIED__G5_NOT_RUN\`.
**Applicable mission:** ONLY P2-06 / [#919 S2-E G1–G5](https://github.com/maidiu/rawlsing/issues/919) under [#909 R3C/R3S](https://github.com/maidiu/rawlsing/issues/909). MCR-lite no-drop, real first-consumer proof and bounded repair. Do not re-open any other packet. Code is isolated SOURCEFREE engineering, no original35/source-science grant or protected merge.

## 1. Exact lineage and frozen evidence

| Cut | Immutable Git commit | Status |
| --- | --- | --- |
| Original A tested science/evaluator reuse | \`d7af5b8df922caa86bcd36a7baa0bbb55b43742d\` | [Original A native 78 + S2-F 19 PASS](https://github.com/maidiu/rawlsing/actions/runs/43275018294) |
| Agent B's two correct provenance repairs | \`56ce7299508d2d28d2eefb6a6a7f6fbe93360103\` | Source-derived, runtime not executed |
| A2 tested-code cut | \`75d4a24bddcfdc5bd1553bd48f130d64f5d5b1e3\` | A2 candidate+frontier repairs committed, not executed |
| A2 complete handoff (B2's actual ancestor) | \`d6f9f1a75ed96d2d8dccb41cd5be3e386d83ce04\` | [PR #966](https://github.com/maidiu/rawlsing/pull/966) draft/unmerged |
| B2 test-only RED candidate | \`e31d520cc836723e1a36f0be51f8dac1696a937f\` | Native runnable test committed; runner did not execute |
| B2 first semantic-fate repair | \`c0f8df0b874bae9fe057c3340516eb04c28ae08c\` | Source patch |
| **B2 final code/test/workflow cut** | **\`b48d0a9287968012a9c97a9602ec31dc1099f183\`** | Source-verified, native run pre-runner failure |

- Writer branch: \`agent/pyat-r3-s2e-b-fate-counterexample-20261112-r2\` — direct descendant of A2 complete handoff, not a parallel replacement.
- [Draft PR #970](https://github.com/maidiu/rawlsing/pull/970) based on A2's isolated branch, not protected PRE-MAIN.
- Changed relative to A2 **only three paths**: \`rawlsing_next/pre553_s2e_exact_conservation.py\`; \`rawlsing_next/tests/test_pyat919_s2e_b2_fate_counterexample.py\`; \`.github/workflows/pyat-r3-s2e-a.yml\`.
- B2 final auditor blob: \`2c28d4ab250d2fcc8b1752a09b60e160f2718423\`; A2 antecedent blob \`2fbcf1d7ecdfb9b205a5122f5e6f7965cd7a0e91\`. Pinned native I05 producer \`pre553_discovery_exact.py\` blob \`1b82b6df993bf14afa5e78782d988cba6e76b668\`.
- No edit to original F1–F4/I05 science evaluator, group-core implementation, Batch engine, source/issuer, admitted S2-F, S2-D, W03/W04 or PRE-MAIN.

## 2. The A2 improvements I concede and retain

**A2's counterattack was substantively right about B:** Source-derived top-level replay and \`valid_empty\` do **not** independently authenticate a candidate receipt. A2 preserved B's correct two repairs while adding candidate inner replay and producer-root rederivation; winner, roles, fact and ancestry integrity; actual declared grammar compilation rather than claimed count; and coverage-state↔typed-state pairing. I inspected those against native \`_candidate\`, \`_compile_frontier\`, \`_evaluate_candidate\`, and \`execute_exact_bounded_discovery\`. The formulas and layering are appropriate. Both B and A2 correctly declined to claim unrun CI as a PASS; original A's true F4 three-way and both directional F2 denominators survive. **No failed accusation of A2's identity or replay correction is sustained.**

## 3. Shared error neither A2 nor B caught: reported scientific fate is a self-consistent lie

**B2-01 \`SEV-1_IF_NATIVE_REPRODUCED\` — S2-E G1/G2/G3, exact native I05 first consumer.**

At A2 frozen code, \`_verify_i05_candidate_receipt\` independently verifies *who the candidate is*, whose facts it cites, and what it claims its typed/coverage fate to be, but it **does not verify that actual fact values satisfy the claimed scientific discovery validation**. \`_verify_i05_declared_frontier\` runs the *pre-search* grammar compiler, but the scientific outcome is decided only *after* execution by \`_terminal_fact_class\`, support thresholds, \`_distribution_differs\`, \`_joint_dependence\`, \`_conditional_reversal\`, or \`_target_cell_supported\`. Neither prior author checks the actual return values of these functions against its discovery receipt.

**Concrete adversarial construction:** Take A's actual 12-respondent first-reader fixture: 10 respondents in A with \`Y=0\`, two in minority C with \`Y=1\`. Baseline \`Y=1\`: **2/12 = 1/6**; conditioned C \`Y=1\`: **2/2 = 1**. Native issued minority discovery should be \`EVALUATED_SUPPORTED / DISCOVERED_RESULT_SUPPORTED\`. Keep all I03 empirical facts, their risk/member/denominator and domain closure, original winning predicate, candidate hash/ID, role refs, declared grammar/frontier and authority unchanged. Forge only \`typed_state="VALID_EMPTY"\` and \`coverage_state="EVALUATED_VALID_EMPTY"\`, then rebuild canonical public \`DiscoveryResultReceipt\` with **correct new candidate replay and producer root**, recalculate outer frontier replay and \`valid_empty=True\`, and replace completed Batch \`result_refs\` with the forged receipt ref.

The forged negative satisfies **both previous B checks**, A2's **typed-state/coverage-state mapping**, exact role/fact/ancestry/candidate identity and declared grammar. Its inconsistency is the unchanging actual I03 support evidence. A2's audit has no post-evaluation fate check; hash closure alone cannot detect the false scientific decision. The attack is committed as \`test_b2_rehashed_false_valid_empty_from_actually_supported_minority_is_red\`, but **the native test has not run**, so do not claim an observed pre-repair RED. A separate local Python \`fractions.Fraction\` independent arithmetic check confirmed 2/2 vs 2/12; this is **not** the native Batch execution.

The public \`DiscoveryResultReceipt\` constructor at the pinned source itself does not enforce scientific coverage correctness (it only forbids \`UNEVALUATED\` with facts). The exact first reader \`census_native_batch\` is therefore the appropriate in-scope audit edge.

## 4. Concrete bounded correction

B2 added \`_verify_i05_scientific_fate_against_facts\` and calls it only when an issued \`RuntimeObjectCatalog\` is present **after** A2's declared-frontier validation.

- Build exact role-specific \`QueryExecutionResult\` views from **existing stored I03 fact objects** and exact per-role query/ref closure; no source open, new C11 build or I03 reevaluation.
- Compare the original \`_support_summary\` values, including risk/source/weight support and \`query_role_fact_refs\`, to the receipt's \`support_uncertainty_state\`; do not trust the latter merely because it was hashed.
- Reapply **the same native I05** \`_terminal_fact_class\`, exact source-authorized minimum denominator, and one of the four original scientific validation functions **on the retained facts**. Assert exact pair \`(coverage_state, typed_state)\` equals the computed native decision. No parallel estimator or new scientific issuer.
- If runtime catalog is absent, retain the existing \`declared_frontier_verified=False\` weaker grade: no invented issuance or claim of independent complete census.
- **B2 self-attack:** first repair constructed a full \`facts_by_key\` map inside every candidate verifier, augmenting an existing per-candidate map in A2. Instead, the final code now builds **one O(F) shared fact map per discovery unit**, reused by both A2's and B2's checks, avoiding another O(C×F) construction. This is a source-level complexity reduction; no measured speedup is claimed. It also preserves specific \`S2EOutputConservationError\` errors instead of swallowing them into a generic ValueError handler.

The B2 production patch is narrow: 115 additions / 3 deletions relative to A2, including the original shared-index correction. It keeps *all* predecessor tests and source science unchanged.

## 5. Executions, preservation and hard proof ceiling

**Native replay and regression command at B2 exact code cut:**

\`\`\`sh
PYTHONPATH=. python -B -m pytest -q -s -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat919_s2e_b2_fate_counterexample.py \
  rawlsing_next/tests/test_pyat919_s2e_a_whole_native_batch.py \
  rawlsing_next/tests/test_pyat919_s2e_a_counterattack.py \
  rawlsing_next/tests/test_pyat919_s2e_a_conservation.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_universal_workload_custody.py

PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat940_s2f_a_counter_provenance.py \
  rawlsing_next/tests/test_pyat940_s2f_b_negative_and_multisource.py \
  rawlsing_next/tests/test_pyat940_s2f_durable_closure.py \
  rawlsing_next/tests/test_pyat940_s2f_fresh_process.py
\`\`\`

B2's test is in the existing S2-E Actions workflow; all A/B/A2 sourcefree controls and accepted S2-F preservation suites remain included. The B2 positive restores untouched original receipts, catalog, output graph, replay and full census identity after the forgery test.

**Actual GitHub CI:** [B2 run 43293037049](https://github.com/maidiu/rawlsing/actions/runs/43293037049) failed **before runner execution**, as did the existing scoped integration workflow. GitHub exposed a failed workflow job but **no executed steps**. Earlier A2 [43287533659](https://github.com/maidiu/rawlsing/actions/runs/43287533659) and B [43282556270](https://github.com/maidiu/rawlsing/actions/runs/43282556270) did not run native tests either. Local environment has no reachable GitHub host/clone and does not contain the private repository. Thus **B2 native test PASS = NOT_RUN, RED→GREEN = NOT_PROVED, inherited regression PASS at B2 SHA = NOT_RUN**. Do not infer any Python regression from pre-runner CI status.

**Independently executed limited oracle:** \`Fraction(2,2) != Fraction(2,12)\` evaluated in local Python and produced \`minority 1, baseline 1/6, rates_differ=True\`. This is an independent numerically discriminating observation, NOT source-native execution or G2/G3 completion.

## 6. G1–G5, risks, next attack and STOP

| Gate | Exact grade |
| --- | --- |
| G1 | **PARTIAL** — Sourcefree candidate and fact fate conservation strengthened; no all35 source/issuer proof or native B2 test |
| G2 | **NOT_RUN on B2** — A's five-unit F1–F4/I03/I05 native test passed **at the original A SHA only** |
| G3 | **NOT_RUN on B2** — New fully rehashed semantic-fate hostile committed, plus inherited seven B/A2 hostile tests; no executable RED→GREEN |
| G4 | **PARTIAL** — Shared sourcefree core exists, 12-row A run had one hit but no speedup; exact B2 process-tree RSS/cap/scratch/output unmeasured |
| G5 | **NOT_RUN** — Distinct nonauthor reviewer needed after genuine applicable G1–G4 |

**New attack surfaces from B2:** imports native private scientific validator functions and reconstructs query views from retained fact preimages; verify against exact pinned I05 source and all negative, weighted Fraction, multiple universes and repeated-occurrence cases at runtime. The extra validation may cost CPU/memory; exact large-scale resource measurement remains missing. This verifier does NOT independently certify the native I03 facts against original respondent sources, external CURRENT permission or original35 scientific design. S2-D admitted saved-store interface remains an honest separate HOLD, not an excuse to block lawful sourcefree code.

**Strongest challenge to Agent A:** Run the single B2 counterexample on the test-only commit and on \`b48d0a9287968012a9c97a9602ec31dc1099f183\`, with the exact issued native five-unit Batch; show the red is **only** scientific-fate contradiction despite all source-provenance/candidate/replay hashes being valid. Then test that legitimate \`VALID_EMPTY\`, \`INSUFFICIENT_SUPPORT\`, \`NONCOMPARABLE\`, \`COVERAGE_LIMITED\` and supported F3 branches remain admissible and unchanged under the same native evaluator. Also challenge the source-specific native validation import stability and measured consumption. **If all frozen obligations pass without reproduced material defect, STOP and request distinct independent G5 immediately. No more generalized A/B hardening.**

**Final decision by this author:** No independent acceptance, protected merge, source/actor/science promotion, W03/W04 change or administrative side commission. \`ONE_BOUNDED_REPAIR_RETURNED__CI_NATIVE_NOT_EXECUTED__NO_FURTHER_GENERAL_DUEL\`.
