# PYAT R3 S1-C — Agent A reciprocal counterattack on B

**Role and disposition:** A counterauthor; not G5 and not protected integration. `COUNTER_REPAIR_COMMITTED__UNVERIFIED_RUNNER_INFRASTRUCTURE__G5_NOT_RUN`. This return distinguishes a source-code-derived counterexample from an executed defect reproducer. No full MCR-C superstructure, no original35 source/scientific/host permission.

## 1. Actual opponent received, protected baseline, preserved valid work

- B immutable documentary HEAD: `5b1db9b5a687184615a199da8a39c55d5a30ed61`, B executed code `e15ccaedaa54155fc3855f821565e2794c946a68`, [B PR #955](https://github.com/maidiu/rawlsing/pull/955).
- Independently read B's complete self-adversarial handoff, machine receipt, actual census adapter, B's three tests, #918 S1-C and #909 R3/R3S, PYAT frontdoor, and adopted MCR-lite.
- B's **valid victory**: A did not bind independent `frontier.unknown`, `frontier.excluded`, or `frontier.inventory_ledger` negative axes. B correctly froze and compared these before source opening. Preserve B's new input fields, literal negative records, hashes, three tests, and 14/14 focused + 22/22 R03/R61 CI green at B tested SHA. Do not replace B's sourcefree scientific-fate census, its real R03 → Batch/C11/I05 first consumer, or the external original35 grant boundary.
- B's refuted alternative remains refuted: historical 18,467 preparation rows do not themselves constitute issued scientific operations; a second compiler/issuer is not justified.
- B's *incomplete* victory: comparison of a frozen negative axis to the frontier copy is not a source-to-fate consistency proof if both copies are coordinatedly altered. This is separate from the known unissued original35 upstream completeness HOLD.

## 2. Concrete defect and material consequences

B's `verify_frozen_inputs` checks:
`semantic_hash(census.inventory_ledger_records) == semantic_hash(frontier.inventory_ledger.material)`,
likewise for `unknown` and `excluded`. It does **not** recompute the per-occurrence status from the separately supplied `SourceInventory` and `GrammarPolicy`, or cross-check the operation-linked UNKNOWN/EXCLUDED records to the actual `frontier.operations`.

Thus:
- An actual `SourceInventory` occurrence with administration UNKNOWN can be misreported as `ADMINISTERED / ELIGIBLE` in **both** `FrozenInputCensus.inventory_ledger_records` and `frontier.inventory_ledger`, with source hash, eligible operation count and B's cross-copy hash comparisons unchanged. This is a false source-fate report even if the correctly derived operations continue to withhold native execution.
- A real UNKNOWN operation can be dropped from **both** `FrozenInputCensus.unknown_scope_records` and `frontier.unknown` while keeping `frontier.operations`, frozen source/science operation lists and hashes unchanged. Same for operation-linked excluded/inapplicable rows. B's current frozen-vs-frontier comparison accepts a jointly truncated list, although every declared negative operation has a fate obligation.

These are concrete *static control-flow* holes in existing G1/G3 source-qualified fate truth; sourcefree CI execution of the counterexamples is **not** represented as achieved.

## 3. Implemented narrow causal repair

Draft [A counter PR #962](https://github.com/maidiu/rawlsing/pull/962), branch `agent/pyat-r3-s1c-adversarial-a-counter-20261112-r1`. Isolated descendant of B's full verified code (B's PR unchanged); PR targets A's branch for readable shared evolution, and the actual git ancestry retains all B commits.

No new enumerator/scientific/authority engine was created:
1. Recompute expected `InventoryLedgerEntry.material()` from the **existing** `rawlsing_next.universal_grammar.enumerate.inventory_ledger(inventory, policy)` implementation, compare against `frontier.inventory_ledger` before compilation/source open; refuse `INVENTORY_LEDGER_INVENTORY_MISMATCH`.
2. For `frontier.unknown`, compare every operation-linked `op.material()` to operations with disposition `UNKNOWN`; refuse `UNKNOWN_OPERATION_NEGATIVE_LOSS`. For `frontier.excluded`, compare `op_id`, class, disposition and reasons against `PROHIBITED / INAPPLICABLE_PROVED` operations; refuse `EXCLUDED_OPERATION_NEGATIVE_LOSS`.
3. Continue preserving separately declared **non-operation** negative/source-held records with no `op_id` exactly as B supplied them. These records are not fabricated as authorized operations; correct RAW operations must still run.

No `pre553_universal_workload.py`, `pre553_issued_workload.py`, `pre553_native_workload_binding.py`, source carrier, W03/W04, PR #948 or protected branch edits.

## 4. Countertests, self-adversarial challenge and evidence limit

New tests appended to the existing B suite:
- `test_s1c_a_counter_rehashed_occurrence_false_admin_fails_before_source_open`: create genuine UNKNOWN administration; jointly forge both ledger copies as ELIGIBLE/ADMINISTERED; source/scientific operation manifests unchanged; expect typed refusal before source factory and exact restored I05 downstream conservation.
- `test_s1c_a_counter_joint_forged_unknown_and_excluded_drops_refuse`: create genuine disjoint-form `INAPPLICABLE_PROVED` rows, jointly remove one operation-linked excluded row from both copies; separately create genuine UNKNOWN operation and jointly remove its UNKNOWN row; expect exact respective typed refusals.
- `test_s1c_a_counter_independent_nonoperation_negatives_preserved`: add independently declared non-operation source UNKNOWN and source EXCLUSION with no scientific `op_id`, execute the unchanged real sourcefree I05 reader and check retained original candidate/fact identity and no valid RAW loss.

Own test correction: the basic 309-operation baseline contains 150 ELIGIBLE + 159 HELD but no operation-linked EXCLUDED, so the excluded-severance test initially assumed non-existing fixture data. Repaired by deriving a genuine disjoint-forms inapplicable frontier before removing its excluded evidence.

**Execution status: CI blocked before test steps.** Three pushes and a rerun produced near-instant workflow FAILURE (2–6 seconds), **zero GitHub Actions job steps** and 404/no stored job logs; both focused S1-C and combined sourcefree jobs exhibit this. These are not pytest/implementation diagnostics and they are **not** evidence of a code PASS or FAIL. Source-code examination and committed hostile tests support a plausible causal repair, but there is **no successful full S1-C run at the A counter code SHA**. B's earlier successful two workflows remain the last verified execution baseline.

Exact commands to run once execution is available:

```bash
PYTHONPATH=. python -B rawlsing_next/tests/pyat_r3_s1c_rss_runner.py rawlsing_next/tests/test_pyat_r3_s1c_source_operation_fates.py
PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider rawlsing_next/tests/test_universal_workload.py rawlsing_next/tests/test_universal_workload_custody.py
```

Also rerun the stacked S1-B/S1-D/S2-F sourcefree integration workflow. The checked CI errors presently preclude an honest `PASS` designation for new code.

## 5. Best next attacks and grades

- **Attack A**: source authority/meaning/decision `source_decision_ref` still external; changing both source+science census and independent inventory in coordinated fashion cannot be rejected using local synthetic authority. This is held rather than modeled as original35 permission.
- **Attack B**: `frontier.unknown/excluded` may include foreign source-document evidence without operation links; preserve it, don't reject all records without `op_id`. Distinguish false no-drop from true external scope.
- **Attack C**: independent test run must demonstrate that the cross-owner operation-negative comparison does not alter the incumbent Batch/C11/I05 candidate and fact identities, especially qualified RAW and routing UNKNOWN. A successful static source review alone is insufficient.
- **Attack D**: sourcefree memory cost is O(declared frontier and inventory evidence), but original35 scale and native_CURRENT/resume remain unrun here.
- **Rejected alternatives**: resurrecting R01 scientific compiler, inventing a new hash owner, forcing all external negatives into native operations, adding a new review court or treating logless CI FAIL as pytest diagnostics.

### Court/STOP (honest grade)

- G1: B's proved scoped negative-axis freeze preserved, extra *source consistency* repair **COMMITTED / TEST_NOT_RUN**.
- G2: B's prior real I05 sourcefree positive/changed/restoration **PASS inherited**, new repair same consumer **NOT_RETESTED**.
- G3: A's new coordinated-mutation negatives **COMMITTED / TEST_NOT_RUN**, B's previously demonstrated three negatives PASS inherited.
- G4: B's prior sourcefree 309/150/330, 1 open/1 build and ~260MB RSS PASS inherited; new incremental resource result **NOT_RUN**.
- G5: **NOT_RUN**; independent receiver distinct from A and B.
- Authority/science: original35 scientific and source permissions HOLD_EXTERNAL; protected merge prohibited.
- STOP: No new speculative hardening. Resume only the three new tests and inherited CI when a genuine runner exists; repair concrete failures, then freeze the shared descendant for single nonauthor G5. Do not mark this counterattack ACCEPTED before executable proof.
