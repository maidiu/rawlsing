# PYAT R3 — S2-E Agent A3, bounded final conservation repair over B2

**Disposition:** \`A3_SOURCEFREE_EXACT_CLOSURE_PATCH_COMMITTED__NO_NATIVE_RUNNER__NOT_G5_ACCEPTED\`.

## Immutable artifact and actual successor lineage

- Original obligation: **P2-06**, governing [#919 S2-E G1–G5](https://github.com/maidiu/rawlsing/issues/919) and [#909 R3C/R3S](https://github.com/maidiu/rawlsing/issues/909); PYAT PROGRAMMA and MCR-lite. No broader commission.
- A initial tested code: \`d7af5b8df922caa86bcd36a7baa0bbb55b43742d\`, [Actions 43275018294](https://github.com/maidiu/rawlsing/actions/runs/43275018294): **78 sourcefree native/regression and 19 S2-F preservation tests passed**, ***only at the older A code SHA***.
- B1 correction: \`56ce7299508d2d28d2eefb6a6a7f6fbe93360103\` — false \`valid_empty\` and false top-level I05 replay.
- A2 correction: \`75d4a24bddcfdc5bd1553bd48f130d64f5d5b1e3\` — complete native candidate identity, inner replay and grammar-declared roster.
- **B2 actual received frozen head:** \`2132932b920e3572068cd8d4fcf8fae5cc2957f9\`, [PR #970](https://github.com/maidiu/rawlsing/pull/970). B2 corrected scientific fate mismatches using the native I05 validators and shared one per-discovery fact reference index.
- **A3 frozen code/test/workflow SHA:** \`81a764cc7eac960f0fd607d9c3fe62428905daa4\`, branch \`agent/pyat-r3-s2e-a-final-conservation-20261112-r3\`, [draft PR #973](https://github.com/maidiu/rawlsing/pull/973), **base B2's own isolated branch**. Later commits on this branch only add receiving documentation.
- Code/test/workflow changes relative to B2: \`rawlsing_next/pre553_s2e_exact_conservation.py\`, **new** \`rawlsing_next/tests/test_pyat919_s2e_a3_native_closure.py\`, \`.github/workflows/pyat-r3-s2e-a.yml\`. The existing I03/F1–F4 sourcefree native evaluator, I05 producer, Batch runner, grouped computation, S2-F closure, source rights and protected PRE-MAIN are untouched.

## Hostile reception of B2: genuine strengths retained

**B2 was right**: A2's candidate identity/fate type checks could accept a coherent \`VALID_EMPTY\` scientific claim inconsistent with the actual referenced I03 cell distributions. B2's \`_verify_i05_scientific_fate_against_facts\` computes the native I05 validation from retained exact facts using the existing \`_terminal_fact_class\`, \`_distribution_differs\`, \`_joint_dependence\`, \`_conditional_reversal\` and \`_target_cell_supported\` functions, with the exact native support rule. That is a material correction and is retained unchanged. B2's shared \`facts_by_key\` index instead of one full map per candidate is also retained. The prior B1 and A2 provenance checks are likewise intact. No B2 finding was shown false; I do not claim otherwise. B2 correctly did not claim an unexecuted CI test as PASS.

## New first-consumer omissions A3 repaired

Read the pinned native source, \`rawlsing_next/pre553_discovery_exact.py\` \`execute_exact_bounded_discovery()\`, against the auditor \`census_native_batch()\` and \`DiscoveryResultReceipt\` constructor. The native producer not only computes candidate science and replay: it emits specific authority and dependency *sets*, an exact I03 contract ID, three false nonpromotion flags, and exactly the predicate/query preimages used by its compiled candidate roles. A self-hashed public receipt can change these without changing the actual empirical facts or replay.

**A3-01 — no illicit actor/structural/diagnostic promotion.** The auditor now requires \`diagnostic_score_is_empirical_fact\`, \`structural_truth_effect\`, and \`actor_v3_effect\` to be **literally False**, as emitted by native I05, and the exact \`QUERY_EXECUTION_CONTRACT_ID\`. Test \`test_a3_rehashed_structural_or_actor_promotion_is_not_native_discovery\` loops all three flags, constructs a new canonical valid receipt, and rebuilds the outer replay and completed Batch references; \`test_a3_rehashed_wrong_query_contract_is_not_native_i05\` tests the incorrect I03 contract. Expected refusal: \`S2E_I05_NONPROMOTION_FLAGS_MISMATCH\` or \`S2E_I05_QUERY_EXECUTION_CONTRACT_MISMATCH\`.

**A3-02 — exact native receipt dependency/issuer closure.** B2 verifies numerical fact-derived outcomes but did not verify that \`receipt.dependency_refs\` exactly conserves the issued discovery authority, candidate grammar, frontier, winning predicate and all fact references; nor that \`receipt.authority_snapshot_refs\` contains the complete union of source issuer and retained fact authority snapshots. A3 compares those sets against actual pinned native producer formula, not against a self-asserted receipt. Test \`test_a3_rehashed_native_dependency_and_authority_loss_is_refused\` forges independently rehashed objects with missing dependencies and then missing authority snapshots, preserving the scientific evidence. Expected refusal: \`S2E_I05_DEPENDENCY_CLOSURE_MISMATCH\` or \`S2E_I05_AUTHORITY_SNAPSHOT_CLOSURE_MISMATCH\`.

**A3-03 — exactly the executed object inventory, with no imported extra.** A2/B2 recompiled the entire authority-declared candidate roster and checked receipt roles but did not check that \`ExactBoundedDiscoveryResult.executed_queries\` and \`executed_predicates\` are **exactly** the union of executed role objects constructed by that roster. The native I05 producer does this. A3 refuses extra or missing public objects. \`test_a3_extra_self_consistent_executed_query_outside_issued_frontier_refused\` appends a *legitimate but unused* F2 query object to the result; all I05 frontier replay and Batch refs still agree, but the added exact object is not scientifically executed by any issued I05 candidate. Expected refusal: \`S2E_I05_EXECUTED_OBJECT_CLOSURE_MISMATCH\`.

These are **new producer-conservation checks**, not a rewrite of B2's scientific arithmetic or original35 permission. Any comparison to the producer is conditional on the original exact \`RuntimeObjectCatalog\`; absent issuer catalog the audit must remain at its weaker advertised scope.

## Execution commands and honest proof ledger

At A3 frozen code SHA, from the repository root, Python 3.11 and \`pytest pandas pyreadstat pyarrow duckdb\`:

\`\`\`sh
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
PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pyat940_s2f_a_counter_provenance.py \
  rawlsing_next/tests/test_pyat940_s2f_b_negative_and_multisource.py \
  rawlsing_next/tests/test_pyat940_s2f_durable_closure.py \
  rawlsing_next/tests/test_pyat940_s2f_fresh_process.py
\`\`\`

**CI explicitly not green.** [A3 exact-head workflow 43298785954](https://github.com/maidiu/rawlsing/actions/runs/43298785954) ended FAILURE *with no recorded job steps*. A single focused retry reported successful API submission, but likewise failed before any job steps. The separately triggered scoped integration workflow also failed pre-runner. The runtime could not reach private GitHub for a local clone. Python syntax of selected new starred-set expressions was checked in isolation; **that is not a full file compile, native execution, test pass or RED→GREEN witness**. Do not assert B2's or A3's new science/provenance checks have passed tests. Original A's earlier 78 + 19 green tests belong solely to A's older code SHA.

## Current G1–G5 and independent receiving

| Gate | Disposition |
|---|---|
| G1 — exact scientific and full output obligations | PARTIAL: sourcefree producer closure strengthened, but actual original35 issuance and exhaustive operation universe not proved |
| G2 — full native graph equivalence | A old scoped PASS, **NOT_RUN at B2 or A3 code cut** |
| G3 — hostile native falsification | A3 four adversarial functions, plus inherited B2/B1/A2 regressions, **COMMITTED BUT NOT_RUN** |
| G4 — shared resource economics | PARTIAL; A's 12-row Batch had one cache hit and no speedup; no current process-tree/cold-repeat/100k output cap or S2-D saved store |
| G5 — independent third-party receiving | NOT_RUN, cannot self-issue acceptance |

Engineering grade: \`SOURCEFREE_REPAIR_COMMITTED__RUNNER_EVIDENCE_MISSING\`. Scientific grade: **no original35 native or causal-science promotion**. Source/actor grade: **no new source use, structural admission, actor V3/persona or human consent**. Integration: **draft PR only, protected branch untouched**. \`HOLD_DEPENDENCY:S2-D\` continues solely for actual saved-store integration.

**Strongest bounded next attack:** execute exactly this SHA against all inherited sourcefree and S2-F tests and the new four hostile functions, then confirm genuine I05 SUPPORTED/VALID_EMPTY/INSUFFICIENT_SUPPORT/NONCOMPARABLE/weighted and multi-universe outputs do not false-reject. Independently trace actual declared compiled frontier and every executed public object; challenge the new closure equalities and support snapshots. Repair only a reproduced consequential defect, then independent **third-party G5**. No more general A/B escalation; no hall-monitor acceptance theater.

**STOP:** \`A3_BOUNDED_CONSERVATION_REPAIR_FROZEN__EXECUTION_AND_G5_PENDING\`.
