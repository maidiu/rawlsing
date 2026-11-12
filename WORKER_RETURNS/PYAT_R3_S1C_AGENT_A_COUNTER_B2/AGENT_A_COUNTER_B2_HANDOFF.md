# PYAT R3 S1-C — Agent A bounded counterattack on B2

**Role:** original Agent A reciprocal counterauthor, not independent G5, issuer, HQ, or protected integrator.
**Scope:** P1-04 / #918 and R3/R3S #909; TEST_ONLY_SOURCEFREE. **Draft PR:** https://github.com/maidiu/rawlsing/pull/975.
**Exclusive branch:** `agent/pyat-r3-s1c-a-counter-b2-pending-20261112-r1`, created from immutable B2 runner HEAD `f011a7639c89ec07829521cff3824dcaf95b6e6e`. No alteration to B2, B1, #950/#955/#959/#967, W03/W04 or protected PRE-MAIN (`6a5c12f04323d74001f9632063ec907f4fc4468e` at readback).

## Received B2 achievement — conserved, not re-litigated

B2's actual local macOS 13.2.1/Python 3.11.3 sourcefree test runs are preserved as **author evidence**, not new A evidence: 17/17 focused (post test-fixture repair `19ab029c2c5076ec6bc12d0287af60c00a41f576`), 22/22 R03/R61, plus 46 S1-B, 59 S1-D, 19 S2-F, 58 shared (182 per combined group, some suite overlap), all reported zero failures/skips. Sourcefree real issued path retained 309 accounted operations, 150 candidate receipts, 330 empirical facts, one source-factory open, one bounded C11 build; changed-value native facts and exact checkpoint restoration tested. B2 corrected an actual fixture error: a risk-set-UNKNOWN mutation did not generate an excluded operation until the B/Y risk sets were made disjoint. Accepted at its **reported executed sourcefree scope**, without claiming G5 or original35.

The B2 role-fate repair is source-grounded: `role_disposition(inventory,policy,...)` is checked for every operation, including HELD rows that the native lowerer deliberately does not revalidate. B2's jointly rehashed false HELD demonstration proves an actual lost positive in unguarded existing R03, and B2's `SOURCEFREE_ROLE_FATE_DRIFT` guard is retained without modification. B1's additional frozen UNKNOWN, EXCLUDED and occurrence records and #959's authentic R61 projection/inventory/histogram checks are all retained.

## One newly identified in-scope vulnerability

**Source path:** `rawlsing_next/pre553_operation_fate_census.py`, original B2 `verify_frozen_inputs`; downstream `rawlsing_next/pre553_universal_workload.py::compile_governed_frontier`, and `rawlsing_next/universal_grammar/native_map.py::lower_operation/lower_frontier`.

R61 `enumerate_frontier(inventory, policy, budget=5)` marks every eligible beyond budget `ScientificOperation.execution_state="PENDING"` and places its ID in `ScientificFrontier.pending_operation_ids`; `budget_state="PARTIAL"`. B2 verified that every ID *listed* pending was eligible and checked counts of per-operation execution states, but **never joined the PENDING operation IDs back to the pending list**. B2's frozen source/science manifestations contain operation ID, source/hash and eligibility disposition but not pending-list membership. The unknown/excluded/ledger rows also do not carry this relation.

The current R03 compiler creates `active_frontier` by **removing solely IDs from `frontier.pending_operation_ids`**, not by checking `operation.execution_state`. A coordinated edit that simply replaces `frontier.pending_operation_ids=()` leaves all operation objects, two census refs, inventory/negative axes, histogram totals and role fates unchanged. At B2's former preflight it passed; R03 now lowers all eligible operations. Its post-native anti-joins are relative to the **forged plan**, so they need not reject additional issued candidate receipts. This is an actual original G1/G3 bounded-execution conservation obligation, not a new science/authority condition.

**Causal distinction:** Source-level control flow and the missing conditional are independently verified from the pinned tree. The newly committed native reproducer has **not been executed**, so an actual overissued receipt count on this specific B2 code cut is a test expectation, NOT a claimed observation. The B2 genuine positive test and existing 182 author-executed checks remain accepted as evidence for unchanged code only.

## Repair — allowlisted in existing adapter

Product commit: `0fc55cb5d6c2199bea44000447e0784d127b9ea6`; test commit: `dae66cdf9f3846d237e0b1c3069cc17eb05b7746`.

At the existing pre-compilation validator after verifying operation/fate identity, reconcile the exact set of `operation.execution_state=="PENDING"` to the actual `frontier.pending_operation_ids`. Refuse via `PENDING_FATE_CENSUS_DRIFT` on missing/extra IDs. Additionally refuse via `BUDGET_STATE_FATE_DRIFT` unless `PARTIAL` has nonempty pending IDs and `COMPLETE` has none. Both checks happen before the source factory and before compiling. No compiler, enumeration engine, source policy, existing negative verifier, scientific issuer, persistence or authorization interface is changed.

One new test `test_s1c_a_counter_pending_severance_cannot_overissue_bounded_work`:
1. Obtain a genuine partial R61 budget=5 frontier and run the actual R03→I05 first reader; assert pending rows have no candidate IDs.
2. Remove only the pending ID list; separately freeze content-consistent census, verify source/science/negative ledgers have identical hashes.
3. Directly invoke the existing R03 compiler and actual I05 issued reader on the poisoned frontier, assert candidate receipts exceed the honest budget-limited baseline while native anti-joins report success.
4. Call the patched adapter with the poisoned frontier: expect `PENDING_FATE_CENSUS_DRIFT` **before any source-factory call**.
5. Forge only the `budget_state="COMPLETE"` metadata: expect `BUDGET_STATE_FATE_DRIFT`.
6. Restore honest inputs, rerun native first reader, require exact checkpoint/frozen census/operation-fate identities.

**Regression status: NOT EXECUTED at new A code SHA.** This session has GitHub connector code-read/write privileges but no clone-capable network or authorized local project runner. GitHub Actions hosted runs were confirmed billing/spending-limit-blocked in B2; do not falsely turn an unstarted CI job into a code PASS/FAIL.

## One-run completion instruction (no further author duel)

On the same authorized isolated local runner used for B2, checkout this A PR code commit (or its unchanged-code documentary descendant) and execute:

```bash
PYTHONPATH=. python -B rawlsing_next/tests/pyat_r3_s1c_rss_runner.py rawlsing_next/tests/test_pyat_r3_s1c_source_operation_fates.py
PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider rawlsing_next/tests/test_universal_workload.py rawlsing_next/tests/test_universal_workload_custody.py
```

Expect **18 focused tests** (17 B2 + this one) and **22 inherited**, if all are green; combined S1-B/S1-D/S2-F/shared suite should be rerun if receiving demands code-cut integration evidence. If the new test fails, diagnose the actual native evidence and correct **that exact cause**, rather than assuming this static hypothesis has already been proved. Once G1–G4 execute cleanly, R3S STOP: independent nonauthor G5 on the final exact code cut.

## Court / authority boundaries

- **Engineering G1–G4:** B2 17+22+182 reported local test evidence applies to the unchanged ancestor. A's source-based counter and committed regression are **NOT YET EXECUTION-QUALIFIED**.
- **Scientific:** test-only sourcefree grammar and native receipt behavior; no original35 source, U_item/U_unit/U_app/E_pre issuer or source-complete entitlement.
- **Authority:** original35, actual native-host CURRENT, source permission, W03/W04 and protected merge remain outside this branch. This is a draft unmerged PR. G5 nonauthor was not run.
- **Strongest remaining attack:** whether a co-mutated pending ID list *plus* individual PENDING row states/budget state can still misrepresent the externally intended budget (not independently frozen by the S1-C manifest). Sourcefree input consistency can catch one-sided severance; it cannot certify an omitted issuer-held budget absent independently fixed authority. Also run the new actual native test: no runtime outcome is claimed yet.

**Disposition:** `A_COUNTER_B2_SOURCE_GROUNDED_PENDING_DRIFT_REPAIR_COMMITTED__NEW_TEST_NOT_RUN__G5_PENDING`. Do not merge or mark accepted merely on this report.
