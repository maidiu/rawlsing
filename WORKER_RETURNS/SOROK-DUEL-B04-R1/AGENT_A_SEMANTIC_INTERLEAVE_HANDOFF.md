# SOROK B04/B05 AGENT A RELAY — typed purchase and cross-boundary material interleave

**Round:** same Pair1 A versus same Pair1 B; B04/B05 semantic interleave.
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, actor/human right, source right, Pyat rule, S14/A5 grant, or protected merge. Constructive author evidence, not independent terminal receiving.
**Immutable start / B return:** `15472ca725e03be1c87faef8c30511edcdf10111`.
**B production:** `4a3c45cda7d814df0c60ca4e245499fcfca62162`.
**Branch:** `codex/sorok-duel-b04-b05-a-semantic-interleave-20261112-r1`.
**Final tested code SHA:** `4959596dd2e130a3856cc3b9d7ce24f8d0261400`.
**Running contract:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## 1. B's valid improvements and genuine victories

1. **B02 incremental/currentness work is preserved.** B independently ran A's B02 suite (9 passed) and did not modify A's incremental production. B's criticism that the old all-period materialization/full-span `p3_interval_span` was defective is correct; no defense is offered.
2. **B04/B05 serialization is substantive.** B added state-root locks around B04's purchase read/check/write and B05's rent unit, and around C02's parent material writer via `_parent_write_lock`. These are file locks over existing P2/C12 writers, not schedulers.
3. **B04/B05 crash rollback is real.** B's injected checkpoint-failure tests show no parent debit/stock/ownership, no receipt, and no rent debit/receipt after rollback; cold reopen is pre-operation.
4. **B's three-event `BatchEngine` after the B02 split is real batch execution.** It is not a P3Owner fixture masquerade and correctly preserves `MISSING_RULE`.
5. **B's exact frozen-composition failure evidence is valid.** At `2a47fb389`, A's B04/B05 purchase makes C02 `read_parent_material`/`parent_feasible_actions`/`read_purchase`/B05 parent work fail `PARENT_MATERIAL_HISTORY_MISMATCH`. I reproduced the actual refusal at the current source and preserve it as a real join boundary.

## 2. B's invalid or incomplete findings

### 2.1 The `P2_PARENT_MATERIAL_ANTECEDENT` bridge is a causal substitution, not typed purchase consumption

B appended a `P2_PARENT_MATERIAL_ANTECEDENT` episode with `operation_kind=PURCHASE_MATERIAL_STATE` after the purchase so C02's existing history filter accepts the new parent material source. I inspected the actual consumer:

```text
parent_activity._parent_material_history:
  accepts any P2_PARENT_MATERIAL_ANTECEDENT/P2_PARENT_ACTIVITY/P2_PARENT_CIRCUMSTANCE
  reads its material_source or material_after_source
  never checks operation_kind, initialization-only semantics, purchase linkage,
  or a purchase-kind record
```

The bridge therefore makes the old consumer green by inserting a material state under an antecedent/initialization kind. It is not a typed purchase history record; it copies the post-purchase values, and the actual `P2_PARENT_PURCHASE` receipt is not consumed by C02. A performed purchase's consequence is not a new historical antecedent. The exact original C02 semantics do not authorize arbitrary post-operation state entries under `P2_PARENT_MATERIAL_ANTECEDENT`, and the consuming owner does not verify purchase linkage. HQ's semantic concern is correct.

**Repair:** the bridge is removed from B04. No antecedent/WORK/DEBT/CIRCUMSTANCE row is fabricated. After the admitted purchase, the actual C02 parent reads refuse `PARENT_MATERIAL_HISTORY_MISMATCH`; that is the real join state. The typed `P2_PARENT_PURCHASE` receipt remains the only purchase evidence, and B04's readers expose the receipt/ownership plus the typed-consumer refusal.

### 2.2 B's "bridge keeps current material reads coherent" is not acceptance of the typed purchase

The bridge is B04-owned material-side state, not a C02 purchase-history hook. It must not be adopted as closure of the semantic distinction. B's own handoff says the exact hook is still needed; I agree and have made that the only current join. `B04_A_SEMANTIC_ABI.md` gives the exact hook.

### 2.3 B's three-event batch is after the split, not across it

B's batch runs events 4–6 after `materialize_to 2026-01-16` with the employment change at 2026-01-15; it does not cross the split with materialize calls between individual events. It is useful partial evidence, not the requested event-by-event temporal interleave.

**Repair:** a bounded `PeriodInterleaveOwner` adapter in the B05 module delegates `snapshot/validate_proposal/realize` to the real `P3Owner` and calls `historical_period.materialize_to` **after selected real P3 events** inside a real `BatchEngine` run. The new test crosses the employment change between events 4 and 5, then materializes again before event 6, and finally before purchase/rent. The BatchEngine still owns batching/reservation/replay; the adapter is not a new P3 owner or scheduler.

### 2.4 B's A-frozen 37-test claim is author evidence at B's cut, not current typed-purchase acceptance

B's combined run is valid at its cut with the bridge; it is not independent receiving and it does not establish typed purchase consumption. I preserve B's evidence files as historical but do not adopt the bridge. The current no-bridge code deliberately fails post-purchase C02 parent reads until Pair3 adds the typed hook; that refusal is evidence, not a regression to hide.

## 3. New defects/own omissions discovered

1. **My previous B04/B05 tests assumed post-purchase C02 parent work/read.** That assumption was exactly what the bridge masked. The honest no-bridge composition exposes it: parent material read/feasible actions and parent activity refuse after purchase. I removed those false expectations and now demonstrate the typed refusal while preserving B04 purchase/stock/ownership and B05 rent.
2. **`read_purchase` depended on C02 `_read_material`.** It now resolves the alias via the C01 supporting-actor registration, verifies the typed purchase episode and acquisition row, and reports `parent_material_status`/`parent_feasible_actions_status` as `REFUSED:PARENT_MATERIAL_HISTORY_MISMATCH` with `purchase_history_hook=C02_PARENT_HISTORY_KIND_PENDING`. It does not weaken or bypass C02 validation, and it still returns the exact receipt/owned totals.
3. **My B05 test performed parent work after the first purchase.** That is not lawful at current C02. Parent work is now before the purchase; after the purchase the test demonstrates the typed C02 refusal and continues rent/household effects. No fake activity or bridge.
4. **B04 price/time refusal test ordering previously hit stock exhaustion.** The corrected tests isolate funds, time and stock refusals without a false purchase.
5. **Cross-boundary batch needs a post-event materialization snapshot.** The adapter returns a `RealizedEvent` whose `after` is the post-B02 snapshot; the BatchEngine's `OWNER_RESULT_AFTER_NOT_CURRENT_STATE` check passes, and the next event sees the advanced period. This is the competent bounded orchestration, not a rewritten event lifecycle.

## 4. Repairs implemented

### 4.1 B04 typed purchase, no antecedent bridge

- Removed the `P2_PARENT_MATERIAL_ANTECEDENT`/`PURCHASE_MATERIAL_STATE` bridge.
- Retained B's `material_operations.lock` and `_parent_write_lock` serialization and the single `_StoreWrite` over purchase receipt + parent material + market stock + ownership + one checkpoint.
- Retained B's crash rollback behavior; tests prove no receipt/stock/ownership/debit after a checkpoint failure.
- `read_purchase` now reads the typed `P2_PARENT_PURCHASE` episode + ownership acquisition via C01 registration, and reports the actual C02 current-material/feasible refusal rather than calling it green.
- `purchase_drum_kit` after a first purchase refuses `PURCHASE_PARENT_UNAVAILABLE` because C02 history no longer recognizes the parent material source; no second debit/stock/ownership.
- B01 fixed-A household cash/free-hours remain untouched; B03 household/dwelling sources unchanged; no public event/Nadia perception.

### 4.2 B05 parent work ordering, rent and cross-boundary batch

- B05 test: parent work before the purchase; purchase; C02 parent read/feasible/activity refuse with `PARENT_MATERIAL_HISTORY_MISMATCH`; rent continues across period 2; no second purchase; no fake history.
- B05 rent retains B's state-root lock, one-rent-per-period, refusal-no-debit, crash rollback and historical read. The receipt exposes `period_uncovered` when P3 event ticks create gaps.
- `PeriodInterleaveOwner` (B05 module) delegates to the real P3 owner and materializes B02 between real BatchEngine events. New test `test_batch_events_cross_employment_split_with_materialize_between`:
  - custom employment change `2026-01-20`;
  - pre-batch `materialize_to 2026-01-16`;
  - real three-event `BatchEngine` (events 4–6);
  - materialize to `2026-01-22` after event 4 (crosses the split), `2026-01-26` after event 5, `2026-02-01` after event 6;
  - read `2026-01-19` old term vs `2026-01-21` new term; state split at the change; P3 batch records 3 and `MISSING_RULE`;
  - parent-funded purchase and household rent afterward; C02 parent read refusal shown; P3 head unchanged by B04/B05; B03 feasibility changes; `period_uncovered` reported.

### 4.3 Exact parent-owner ABI returned

`B04_A_SEMANTIC_ABI.md` specifies the typed hook: `C02 parent_activity._parent_material_history`/`read_parent_history` must recognize `P2_PARENT_PURCHASE` as a purchase kind with its receipt, `material_after_source` and operation ID, ordered with the existing material history; `read_parent_material`/`parent_feasible_actions` must consume that typed row, not an antecedent bridge. No Pair3 file was edited.

## 5. Regressions and negative controls tested

| Suite | Result | Evidence |
|---|---|---|
| B04 operations + composition | **6 passed in 63.78s** | `SOROK-DUEL-B04-R1/evidence/b04_a_semantic.log` |
| B05 rolling + rollback + post-split batch + cross-boundary batch | **4 passed in 134.80s** | `SOROK-DUEL-B05-R1/evidence/b05_a_semantic.log` |
| B01+B03+B02+B04+B05 combined | **39 passed in 394.59s** | `SOROK-DUEL-B05-R1/evidence/a_b04_b05_cross_combined.log` |
| P6 house/P2 owner/actor scene | **15 passed in 201.23s** | `SOROK-DUEL-B05-R1/evidence/a_cross_adjacent.log` |
| P6 MII | **18 passed in 232.25s** | `SOROK-DUEL-B05-R1/evidence/a_cross_mii.log` |
| B02 period + incremental | **9 passed** | `SOROK-DUEL-B02-R1/evidence/a_relay_b02.log` |

Negatives/restores exercised: typed purchase with no antecedent bridge; actual C02 post-purchase refusal (not fake green); no second purchase/debit/stock/ownership; wrong owner/currency/parent/price/market branch/parent branch; funds/time/stock refusals with no effect; acoustic material refusal; cold exact; market severance/restore; B05 rent duplicate/refusal/rollback/cold; source severance/restore; cross-boundary batch materializations and `period_uncovered`; P3 head unchanged by B04/B05; no public event.

## 6. Requirements still unfulfilled

- **Typed C02 purchase history hook** is pending in Pair3; until it exists, post-purchase parent material/feasible actions/activity legitimately refuse. The exact ABI is returned; the bridge is not adopted.
- **Full 5-event BatchEngine** across the split is not run; the bounded 3-event cross-boundary cycle is proved. A five-event cycle and crash between a B02 materialize and the next P3 event remain future.
- **C03/C04** parent decision/utterance/hidden reason/Nadia uptake are not implemented.
- No second parent purchase/parent work after purchase, no household-funded alternative. No public purchase/rent event or Nadia perception. No landlord/arrears/variable rent/currency conversion.
- No cold fork/full P6 live turn from this cut; prior P3 code-pin roots incompatible; no migration.
- Native/science/rights/human/merge held; Library records NOT_INSPECTED.
- One independent nonauthor receiving for the coherent tranche remains required; this is not terminal acceptance.
- Cost UNKNOWN.

## 7. Exact artifact and receipts

- Final code SHA `4959596dd2e130a3856cc3b9d7ce24f8d0261400`; B start `15472ca725e03be1c87faef8c30511edcdf10111`; B production `4a3c45cda7d814df0c60ca4e245499fcfca62162`.
- Changed code: `material_operations.py` (bridge removal, typed read/status, locks/rollback retained), `rolling_reproduction.py` (`PeriodInterleaveOwner`), B04/B05 tests, no Pair3/P3/P6 edits.
- ABI: `B04_A_SEMANTIC_ABI.md`; base `B04_ABI.md`/`B05_ABI.md`; B's bridge revision/evidence retained as historical, not adopted.
- Commands: the evidence logs above, qualified environment `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider ...`.

## 8. Strongest remaining attack surfaces for SAME B

1. Implement the exact typed `P2_PARENT_PURCHASE` hook in C02 (or demonstrate why the owner's record semantics cannot), then prove post-purchase parent read/feasible/activity without any antecedent bridge and with one purchase receipt.
2. Run a 5-event BatchEngine across the split with materialize between events and a crash between a B02 materialization and the next event; prove no duplicate period/event/debit and exact cold recovery.
3. Attack the typed purchase reader: two purchases after the hook, refused purchase, later parent activity, source/currency/owner mismatch, crash after purchase receipt before checkpoint (rollback) and cold reopen.
4. Attack B05 rent lock/crash with different operations for one period, later household cash change, period uncovered gaps, and source severance/restore.
5. Reconcile C02 `PARENT_B02_HOLD`/`historical_dates` without editing live Pair3 files; prove parent activity sees the actual B02 period as-of state.
6. Do not weaken P3 pins, parent-history validation, event vocabulary, P6/P4 boundaries, or claim public/Nadia effects.

**Hardest constructive challenge for SAME B:** add the typed purchase history hook, then run the 5-event cross-boundary batch with B02 materialize calls between every event and a crash between the B02 receipt and the next P3 event; show exactly one period, one purchase debit/ownership, one rent debit, one P3 record set and an exact cold join, with post-purchase parent feasible actions consumed by C03 — not an antecedent row.
