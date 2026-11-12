# SOROK B04/B05 AGENT B — material throughline, composition repair, crash boundary

**Round:** Pair1 same persistent Agent B versus same Pair1 Agent A.
**Frozen composition start:** `2a47fb389b453c2f902b8c13ed52304fb40efd0d` (A result `8de517bd3`, A production `62292613`, returned Pair3 C02 `4d93685`; clean automatic merge, not executed/accepted as a combination).
**Branch:** `codex/sorok-duel-b04-b05-b-counter-20261112-r1`.
**This round's implementation SHA:** `4a3c45cda7d814df0c60ca4e245499fcfca62162`.
**A production inspected:** `62292613aa9210a7d3e944314e36924349337439`; A result `8de517bd3c0d2a8afb29509c7917d62cac4dc59a`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, actor/human right, source right, Pyat rule, S14/A5 grant, or protected merge. No terminal acceptance.

## 1. Reconstruction before trusting A

I re-read the frozen B02/B04/B05 packets, programme owner reconciliation and user material/duration requirement before reading A's relay/B04/B05 handoffs. The required result is one real material throughline:

- B02 maps historical dates to the existing S46 logical clock with actual date arithmetic, incremental progress, split periods at a real employment change, currentness/as-of semantics, cold replay and no duplicate period.
- B04 makes a paid obligation/purchase/refusal change actual stock/ownership/resources and later feasibility, with one debit, one receipt, no negative balance, no conjured object, no public event vocabulary edit, and atomic retry/crash behavior.
- B05 proves repeated ordinary material cost across dated cycles, one rent per completed period, nonnegative cash/refusal, exact historical receipts under later activity, and no elapsed-time automatic psyche/work.
- No second scheduler, universal world/psychology engine, landlord economy, or rival parent owner. The two ChatGPT Library architecture records remain **NOT_INSPECTED locally**; no contents are claimed.

## 2. Exact artifact

Code at `4a3c45cda7d814df0c60ca4e245499fcfca62162`:

| Path | Change |
|---|---|
| `WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py` | State-root material-operation lock; C02-compatible parent material-state bridge in the admitted purchase transaction; parent-write serialization; crash-safe same-transaction purchase receipt/stock/ownership/parent update. |
| `WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py` | State-root rent lock around the complete read/check/write unit; wrapped rent API; crash rollback proof remains one `_StoreWrite`. |
| `WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_composition.py` | C02 history consistency, no-fake-activity, later-activity stale retry, and checkpoint-crash rollback. |
| `WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_rollback.py` | Rent checkpoint crash rollback then exact one-debit recovery. |
| `WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_batch_cycle.py` | Actual three-event P3 `BatchEngine` after B02 employment split, then B04 purchase and B05 rent. |

B02 production was not changed by this round; A's `materialize_to`/currentness/receipt implementation at `62292613` is preserved. B01/B03 production is untouched. `parent_activity.py`, `supporting_actor.py`, P3, `model_cycle`, P6 `house.py`/`situated.py`, bp4 event vocabulary, guides, workflows, Pyat/config/protected files were not edited.

ABI revisions: `B04_B_ABI_REVISION.md`, `B05_B_ABI_REVISION.md`; B02 verification/integration: `SOROK-DUEL-B02-R1/AGENT_B_RELAY_HANDOFF.md`. Machine records: `PROGRAMMA_DELTA_B.json`, `impact_B.json`. A's records are preserved.

## 3. A's valid improvements and concessions

A's work is real and preserved:

1. **B02 incremental API and currentness are substantive.** `materialize_to` advances only the unelapsed range, refuses past/outside targets, splits employment changes inside the slice, records durable `P2_B02_PERIOD_MATERIALIZATION` receipts, and recovers state-before-receipt once. `period_progress` exposes B02/S46 coverage/gaps. `p3_interval_span` is net of progress; the old full-span double-advance behavior was a real B defect and A fixed it.
2. **B02 currentness is correct in the tested cases.** Future employment is labeled `FUTURE_NOT_CURRENT`; past as-of states are `MATERIALIZED_RETROSPECTIVELY`; P3 ACTUAL intervals are `ELAPSED_BY_OTHER_OWNER`, not B02 period states.
3. **A ran a real `P3Owner.realize` cycle.** That is an actual P3 owner cycle, not a fixture. A correctly retained `SCHEDULED_ONLY/NOT_PERFORMED` for B02's own intervals and `MISSING_RULE` for durable psychology.
4. **B04/B05 material construction is real at A's cut.** Parent-funded stock purchase, market stock/ownership, refusal with no debit, B05 rent on completed B02 periods, historical receipts, P3 head unchanged, and no public event/psychology are genuine. A's B04/B05 tests pass **before** the frozen C02 composition merge.
5. **A's P3 code-pin disclosure is correct.** No migration or pin weakening was invented.

## 4. Established defect at the frozen composition

### 4.1 A's B04/B05 do not compose with returned C02 at the frozen cut

At `2a47fb389`, A's B04 tests and B05 test fail. The purchase updates the parent material document but appends only `P2_PARENT_PURCHASE`; Pair3 C02 `_parent_material_history` recognizes only `P2_PARENT_MATERIAL_ANTECEDENT`, `P2_PARENT_ACTIVITY`, and `P2_PARENT_CIRCUMSTANCE`. After one admitted purchase:

```text
read_parent_material    -> PARENT_MATERIAL_HISTORY_MISMATCH
parent_feasible_actions -> PARENT_MATERIAL_HISTORY_MISMATCH
read_purchase           -> PARENT_MATERIAL_HISTORY_MISMATCH
B05 parent read/work    -> PARENT_MATERIAL_HISTORY_MISMATCH
```

This is the exact parent-source composition gap. A's claim of 32 combined green tests is author evidence at a different cut, not a passed frozen composition. I did not weaken C02 history validation, forge a work/debt/circumstance record, or call the failed composition green.

### 4.2 A's B04/B05 read-modify-write units were not serialized

B04 checked parent cash/stock/ownership and only then opened `_StoreWrite`; a concurrent C02 parent activity or second purchase could read the same source and lose/duplicate a debit. B05 checked period/operation rent state before its transaction; two callers could each append a rent. A's tests were sequential and did not cover this.

### 4.3 A's crash tests did not cross the existing episode/checkpoint seam

A's B04/B05 tests covered cold/severance, but not a checkpoint failure after episode/stock/ownership writes. The user requires meaningful crash rollback/recovery, not only a successful cold read.

### 4.4 B02 full P3 batch not proved by A

A ran one real `P3Owner.realize` cycle. The priority asks for an actual multievent cycle across the employment split and material operation where competent APIs permit. I added a three-event `BatchEngine` run after the B02 split, followed by B04 purchase and B05 rent. It is a real batch, not a fixture; full cross-boundary materialize-between-events remains a challenge, not a green claim.

### 4.5 Concessions and refuted/withdrawn claims

A's B02 criticisms of my previous all-upfront materialization and full-duration `p3_interval_span` were correct; I withdraw any defense. A's B04/B05 material tests pass at A's pre-merge `62292613` cut, so I do not call A's B04/B05 construction false. What is false is the claim that the 32-test combination is green at frozen merge `2a47fb389`; the frozen B04 tests fail `PARENT_MATERIAL_HISTORY_MISMATCH` (`evidence/a_frozen_b04_failure.log`). I found no other false A criticism to refute in this round; the C02 stale hold and purchase-history hook are real Pair3 reconciliation obligations, not fabricated attacks.

## 5. Repairs implemented

### 5.1 B04 C02 material-history bridge

On admitted purchase, in the same `_StoreWrite` as the purchase receipt, market/ownership/parent updates and checkpoint, B04 appends a C02-recognized `P2_PARENT_MATERIAL_ANTECEDENT` **material-state** record containing the exact post-purchase material source/content and `operation_kind=PURCHASE_MATERIAL_STATE`. It is not a WORK/DEBT/CIRCUMSTANCE activity claim and does not edit Pair3. The separate `P2_PARENT_PURCHASE` receipt remains purchase evidence.

This makes current material history consistent, so `read_parent_material`, `parent_feasible_actions`, `read_purchase` and later B05 parent work/read work at the frozen composition. On rollback, the bridge is rolled back with the purchase.

**Exact Pair3 hook still needed for full history exposure:** `parent_activity._parent_material_history` and `read_parent_history` must also recognize `P2_PARENT_PURCHASE` with its `material_after_source` and operation receipt. The bridge is the B04-owned material-side contract; it is not a substitute for exposing the purchase kind in C02 history. If Pair3 adds that hook, the bridge must be reviewed to avoid duplicate history rows. `PARENT_B02_HOLD`/`historical_dates=NOT_AVAILABLE` are also stale Pair3 literals; B04/B05 use actual B02 and do not treat them as authority.

### 5.2 B04 serialization

- `purchase_drum_kit` now takes a state-root `material_operations.lock` plus C02's existing `parent_activity.lock` around the complete read/check/write unit.
- `establish_market_inventory` takes the material-operation lock.
- The admitted write remains one `_StoreWrite` over purchase receipt, material bridge, parent material, market stock, ownership and one checkpoint.

### 5.3 B05 serialization and rollback

- `apply_household_rent` takes a state-root `rolling_reproduction.lock` around the complete read/check/write unit. Two callers cannot both observe no rent and append a second debit.
- The one-rent-per-period, duplicate-operation, replay and refusal semantics are unchanged; no landlord ledger/arrears model is invented.
- An injected checkpoint failure leaves household cash and rent receipt rolled back; cold reopen returns pre-rent cash and `B05_RENT_NOT_FOUND`.

### 5.4 Actual batch/material integration

`test_b05_batch_cycle.py` establishes a custom B02 employment change at `2026-01-15`, advances to `2026-01-16`, runs a real three-event `BatchEngine` with exact existing plan hashes, then performs B04 purchase, B05 materialization to `2026-07-01`, and B05 rent. It verifies the B02 split/read, purchase stock/ownership, rent cash change, B03 feasibility refusal, and unchanged P3 head.

## 6. Proof

| Suite | Result | Evidence |
|---|---|---|
| B02 period + incremental | **9 passed in 83.88s** | `SOROK-DUEL-B02-R1/evidence/b02_b_verified.log` |
| B04 operations + composition | **5 passed in 45.20s** | `SOROK-DUEL-B04-R1/evidence/b04_b.log` |
| A frozen-cut B04 failure | **2 failed** `PARENT_MATERIAL_HISTORY_MISMATCH` | `SOROK-DUEL-B04-R1/evidence/a_frozen_b04_failure.log` |
| B05 rolling + rollback + batch | **3 passed in 72.10s** | `SOROK-DUEL-B05-R1/evidence/b05_b.log` |
| B01+B03+B02+B04+B05 combined | **37 passed in 332.40s** | `SOROK-DUEL-B05-R1/evidence/b01_b02_b03_b04_b05_b_combined.log` |
| P6 house + P2 owner + actor scene | **15 passed in 216.57s** | `SOROK-DUEL-B05-R1/evidence/p6_adjacent_b.log` |
| P6 MII | **18 passed in 247.53s** | `SOROK-DUEL-B05-R1/evidence/p6_mii_b.log` |

Discriminating proof:

- C02 material read/options/read_purchase/B05 parent work now pass after purchase; history `material_consistent=True`; the bridge row is material, not activity.
- Later parent activity makes a stale purchase replay refuse with no second debit; `read_purchase` is historical.
- Forced B04 checkpoint failure leaves no parent debit, stock, ownership, receipt or bridge; cold reopen pre-purchase.
- Forced B05 checkpoint failure leaves no household debit/receipt; retry admits exactly one rent.
- B05 batch integration: actual three P3 records, one B02 employment split, one parent purchase/ownership, one rent 55→43, P3 head unchanged by B04/B05.
- A's B04 tests now pass with the bridge; B05 A test passes; B02 A tests pass.

## 7. Preserved functionality and boundaries

- B01/B03 household/dwelling/feasibility, P6 house/MII, P2 owner snapshots and existing C02 vocabulary remain green.
- No bp4 event vocabulary or P3 file was edited by this round; C02 B's `MATERIAL_ACTIVITY` is preserved.
- No public purchase/rent event, Nadia perception, psyche record, mother decision/utterance, or possession-by-narrative.
- No B01 fixed-A cash spent for the parent's purchase; no parent C02 cash spent for household rent.
- No new scheduler/clock/database/ledger; locks are file serialization over existing state roots.
- P3 code-pin roots from prior p2_owner cuts remain incompatible; no migration.
- No fork/cold-fork purchase/rent; no full P6 user-turn proof from this cut; no native/science/rights/human/merge.
- The two Library architecture records remain NOT_INSPECTED locally.

## 8. Surviving questions / exact blockers

1. **C02 purchase history exposure.** The B04 bridge keeps current material reads coherent, but `read_parent_history` does not list `P2_PARENT_PURCHASE` as purchase history until Pair3 adds the exact hook. Do not mistake the bridge for that hook.
2. **C02 `PARENT_B02_HOLD`/`historical_dates`.** Pair3-owned stale literals remain; B04/B05 use actual B02. Reconcile under Pair3, not by editing live files here.
3. **B02 cross-boundary batch.** The added BatchEngine batch is after the B02 split; a batch with B02 materialize calls between individual events is not proved. B02 `period_progress` reports event-tick gaps; B05 receipt carries `period_uncovered`; no full scheduled coverage claim.
4. **B05 no arrears.** A refused rent blocks a different operation for that period; no arrears settlement/late payment model. Variable rent/landlord balance/currency conversion remain out.
5. **B04 bridge duplicate-history risk.** If Pair3 later recognizes purchase directly, the material bridge may need removal/reconciliation.
6. **Concurrency** is serialized by file locks but no multi-process/SIGKILL stress test was run.
7. **P3 pin migration** remains Pair2/shared-receiving scope; no weakening.

## 9. Challenge to SAME A

1. Rebase on B04's material-history bridge and prove C02 `read_parent_material`/`parent_feasible_actions`/`read_purchase` and B05 parent work all pass after purchase; then implement the exact `P2_PARENT_PURCHASE` history hook without duplicate rows or fake activity.
2. Attack the bridge with parent activity before/after purchase, two purchases, a refused purchase, a crash after bridge append, and cold reopen. Prove one debit/one ownership and no work/debt/circumstance forgery.
3. Attack B05 rent with concurrent different operations for one period, injected checkpoint failure, later household cash change, duplicate rent and cold restart. Prove one debit/one receipt.
4. Build a full P3 `BatchEngine` 3–5 event cycle **across** a B02 employment split with B02 materialize calls between events, not only after the split; show no double-advance or unexplained gap compression.
5. Reconcile `PARENT_B02_HOLD`/`historical_dates` without editing Pair3 live files; prove parent activity sees actual B02 as-of state.
6. Do not weaken event vocabulary, parent history validation, P3 pins, P6/P4 boundaries, or claim public perception/Nadia uptake.

**Returned for same rival; no terminal acceptance.**
