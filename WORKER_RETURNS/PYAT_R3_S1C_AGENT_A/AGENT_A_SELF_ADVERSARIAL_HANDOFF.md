# PYAT R3 S1-C — Agent A frozen adversarial handoff

**Status:** `AGENT_A_G1_G4_SOURCEFREE_PASS__READY_FOR_B_ATTACK__G5_NOT_RUN`. This is an author return, **not independent acceptance**, protected integration, or native original35 scientific/source issuance. Scope is #918 S1-C / P1-04, with #909 R3S no-optional-hardening rule and prospective MCR-lite.

## 1. Exact artifact and reproducibility

- Draft [PR #950](https://github.com/maidiu/rawlsing/pull/950), branch `agent/pyat-r3-s1c-adversarial-a-20261112-r1`, stacked on **unmerged** [PR #948](https://github.com/maidiu/rawlsing/pull/948) HEAD `7064daa14d93109211629e72d08f3a6e705a0d57`. Protected PRE-MAIN observed `6a5c12f04323d74001f9632063ec907f4fc4468e`. Do not imply #948 or #950 is protected.
- **Last implementation/test/source HEAD independently run by CI:** `9a539024f3d2a23f96e4e4fa50a0e749b0d6b56f`. The source/code/test blobs are:
  - `rawlsing_next/pre553_operation_fate_census.py` blob `1f68dc6ff60e68d72cee284cb8232f659100b8f6`
  - `rawlsing_next/tests/test_pyat_r3_s1c_source_operation_fates.py` blob `c1a0c4b757483454b641ddd501558bdf94df5acf`
  - `rawlsing_next/tests/pyat_r3_s1c_rss_runner.py` blob `63656522497dd6f7760872b692b46bf0e8b7580e`
  - `.github/workflows/pyat-r3-s1c-sourcefree.yml` blob `901e2e6ce54bf5fda7b016d39524aac32f2862a8`
- This handoff and the JSON receipt are added after the tested implementation commit; compare Git blobs and rerun on their final descendant, rather than treating documentation commit itself as an executed run.
- Actual commands, from repository root after installing `pytest pandas pyreadstat pyarrow duckdb psutil`:

```bash
PYTHONPATH=. python -B rawlsing_next/tests/pyat_r3_s1c_rss_runner.py rawlsing_next/tests/test_pyat_r3_s1c_source_operation_fates.py
PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider rawlsing_next/tests/test_universal_workload.py rawlsing_next/tests/test_universal_workload_custody.py
```

- Sourcefree hosted CI [S1-C test job](https://github.com/maidiu/rawlsing/actions/runs/43275142293/job/131381455682) at implementation SHA: **11/11 newly added PASS; 22/22 inherited PASS**. If the run URL differs due to reruns, the exact commit/check-run identity and log are controlling. The independent combined #948 integration CI is a separate check; it does not certify native science or G5.

## 2. Frozen governing obligations / capital preserved

The exact authority is [#918 S1-C G1–G5](https://github.com/maidiu/rawlsing/issues/918), [#909 R3S](https://github.com/maidiu/rawlsing/issues/909), the protected `PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md`, shared PRE-MAIN PROGRAMMA, and `CROSS_HQ_CONTROL_ROOM/MCR_LITE_EXECUTION_DISCIPLINE_R1.md`. Preserve existing `ScientificFrontier`, `compile_governed_frontier`, `execute_governed_frontier`, I05 and issued packet reader; source/scientific and CURRENT decisions are separately competent. Historic 18,467 preparatory fates are **not** 18,467 qualified native executable operations.

The adapter adds **no** second enumerator, scientific policy, authority issuer, parser, physical carrier, C11 engine, universal graph or new persistence system. It requires two caller-supplied complete typed lists, a content-addressed source census and independently supplied scientific fate census. It checks the cross-census and frontier exact operation IDs, op canonical hashes, edition/source SHA, instrument, universe, occurrence roles, declared source-authority reference, U_item/U_unit/U_app/E_pre roots, eligibility disposition, budget pending and nonoperation deferred-scope records **before** calling the incumbent compiler. After execution it anti-joins compiler rows, expected/actual I05 candidates, native facts and typed operation/execution fate rows; reused R03 checkpoint validation checks closure. All original code in #948 remains untouched.

## 3. Actual demonstrated outputs and falsifiers

The exact tested sourcefree fixture recorded:
- **309 declared / 309 compiled / 309 accounted operation rows**; **150 ELIGIBLE, 159 HELD**.
- **150 I05 candidate receipts**, **330 empirical facts**, **3 unsupported-runtime rows**, **6 deferred-scope records**.
- **1 source-factory call; 1 bounded I05 C11 repository build**. The test instrumentation targets actual `pre553_native_workload_binding.build_source_backed_c11_repository` rather than a guessed normal U43 path.
- Hosted 11-test process-tree sampled **peak RSS 260,079,616 bytes**; measured test wall 31.5029 seconds, with a separate representative packet runtime 3.229579 seconds. These are synthetic fixture costs, **not original35 100k/6GiB performance**.

Executed negative controls: omitted candidate, count-preserving duplicated frontier, source vs science census anti-joins including rehashed tamper, wrong edition/source SHA/occurrence/op hash, forged source authority reference, fake original science grade, altered eligibility, budget-pending no-false-positive, routing UNKNOWN no issuance or zero, proved inapplicable disjoint forms, unsupported runtime no fake receipt, source response-cell change with changed **actual** fact identity and exact restore, and changed eligible JOINT policy operation changing actual I05 issued candidate set with exact restored checkpoint. A valid scoped SAMPLE/RAW positive remains executable without optional population weights while population-weighted science stays held.

## 4. Hostile self-findings and repairs

1. **Reproduced author error:** initial test failed 7 cases: `ScientificOperation` has `op_id`, not `operation_id`. Repaired with an explicit typed ID adapter. The next run passed.
2. **Fake freeze concern:** original manifest refs were arbitrary labels. Replaced with `semantic_hash` of the complete frozen source list and separately the complete scientific list; tested omissions even when independently rehashed.
3. **False instrumentation:** first G4 probe patched unused `pre553_issued_workload`/Route B builders and failed. Directly read the actual test-only U43 envelope → bounded Batch/C11/I05 path, patched its real builder and obtained 1 measured build. **The normal/resume U43 path was not run by S1-C.**
4. **Silent residual fates:** conserved explicit nonoperation `frontier.deferred` policy records and U/E_pre roots, not merely status counts; added actual disjoint-forms and routing-unknown execution tests.
5. **Changing a physical response cell while retaining a synthetic source SHA** is a deliberate test seam counterfactual, not original-byte admission or source-attestation evidence.

## 5. Unresolved genuine challenges / proof boundaries

- **Input completeness requires competent independent sources.** The two lists in the tests are intentionally generated from the same synthetic initial frontier and then frozen before adversarial deletions/changes. Hashes bind content **after declaration**; a malicious/incompetent supplier can omit an item from both lists and recompute both hashes. No adapter can derive an authentic original35 all-operation census without the external source and scientific issuer.
- Synthetic `meaning_ref`, `source_decision_ref` and eligibility references are required and crosschecked where possible but do not prove external source entitlement or reviewer competence. Sourcefree grade is enforced, and original science/actor/host grants remain `HOLD_EXTERNAL`.
- The real first reader here is `execute_test_only_discovery_workload` backed by Batch/C11/I05, not S1-D's `execute_issued_workload` CURRENT normal/COMPLETED/PARTIAL/ABSENT. The S1-D accepted code in #948 remains separate; actual current resolver/revocation and original source read authority require independent qualified tests.
- Original35 empirical native product, immutable actual source documents/measurement meaning, production-scale memory, original data release, and N9/N10W are **not demonstrated**. The inherited compiler's sourcefree implementation is reused rather than certified as scientifically universal.
- #948 integration source is **unmerged**. A subsequent merge/rebase changes the graph and needs normal exact combined readback. No W03/W04 change or protected merge is authorized.

## 6. Best next hostile attacks

A. Give B a frozen 310th source candidate absent from the scientific frontier, then try submitting a 309-row synthetic pair with both hashes recomputed; ask whether a truly independent issuer's 310th root can be recovered. The answer **must not** be a false G1 original-source completeness claim.

B. In the same exact sourcefree packet, attack operation identity canonical-hash substitution, edition and occurrence source maps, operation disposition status, and deferred-scope record count-preserving swaps.

C. Replace one genuinely positive actual I05 native receipt/fact or confuse a typed routing UNKNOWN with `VALID_EMPTY`; validate candidate and fact anti-joins and the frozen restore checkpoint. Challenge an I05 output changing without a source/fate preimage.

D. Challenge normal/resume CURRENT revocation at S1-D's actual owner instead of attributing its authority to this adapter. Evaluate cross-ABI only where #948 exact accepted blobs are actually integrated.

E. Inspect sourcefree memory and `lower_frontier` computational scaling before generalizing to huge frontiers; the exact 309-operation fixture is not 18,467 native execution.

## 7. Significant alternatives rejected

Re-enumerating operations inside the compiler would make an omitted original operation invisible (same common-mode source); trusting only total counts allows equal-count substitutions; promoting 18,467 historic physical/preparatory records invents science; adding new authority or CURRENT resolvers would cross issuer ownership; rewriting normal Batch/Route B/C11 or W03/W04 would duplicate machinery; and a second approval layer contradicts #909 R3S.

## 8. Gate verdict and STOP

- **G1:** author-proved for the *full declared synthetic packet*, NOT independently issued original35.
- **G2:** actual sourcefree existing compiler → issued test-only Batch/C11/I05 → real candidate/fact identities; changed eligible operation and physical response facts restored.
- **G3:** author sourcefree anti-joins, negatives and fates verified; original35 issuer still external.
- **G4:** exact fixture counts/opens/builds/RSS measured; stateless adapter reuses R03's checkpoint validation and does not own new durable CAS.
- **G5:** `NOT_RUN` / requires an independent nonauthor, not A or B, to reproduce at the final shared descendant after Agent B's attack/repair.

**R3S STOP:** This author packet has no remaining reproduced in-scope severity defect at the tested sourcefree grade. Freeze code; B attacks, A counterattacks, then bounded independent G5. **Do not commission optional hardening** or repurpose an original35 external hold as an adapter code task.
