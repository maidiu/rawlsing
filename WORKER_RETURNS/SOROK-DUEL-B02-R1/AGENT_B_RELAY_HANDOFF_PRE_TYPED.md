# SOROK B02 AGENT B RELAY — verified incremental periods and batch integration

**Packet:** B02 `Map historical calendar/as-of to existing P3/S46 logical clock and split periods`, CG-B.
**Grade:** `SOURCEFREE_S2_ONLY`. No native calendar/science, actor/human right, source right, Pyat rule, or protected merge.
**Composition start:** `2a47fb389b453c2f902b8c13ed52304fb40efd0d` (A result `8de517bd3`, A production `62292613`, returned C02 `4d93685`; clean automatic merge, not accepted/executed as a combination).
**Branch:** `codex/sorok-duel-b04-b05-b-counter-20261112-r1`.
**B02 production SHA:** `62292613aa9210a7d3e944314e36924349337439` (A's B02 implementation).
**This round's code SHA:** `4a3c45cda7d814df0c60ca4e245499fcfca62162` (B04/B05 composition; B02 production unchanged).
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## 1. Independent reconstruction before trusting A

I re-read the frozen B02/B04/B05 packets, the programme owner reconciliation, and the user material/duration requirement before reading A's relay handoffs. B02 must use the existing S46 logical clock and P2 material world, not rename workshop ticks as years; two dated periods, a real midperiod employment change that splits world/time, preserved source date/clock bases, an actual later material-period reader, no stale/future employment mistaken as current, and cold/retry replay without duplicate periods. B04 must make a real stock/ownership/debit/time operation with refusal-no-effect and atomic retry; B05 must prove recurring material cost across dated cycles and later readers without automatic psyche/work. The two Library architecture sources remain NOT_INSPECTED locally; no contents are claimed.

## 2. A's valid improvements

A's B02 implementation is substantive and preserved:

- `materialize_to` is genuinely incremental; it does not advance all periods up front and refuses past targets/rewinds.
- `period_progress` exposes elapsed/remaining ticks, B02 and all-S46 coverage, gaps, other-owner states and remaining segments.
- `p3_interval_span` is net of current progress; the old full-period double-advance test was corrected, not merely relabelled.
- `read_material_period` distinguishes PAST/CURRENT/FUTURE, current vs future employment, retrospective vs as-of materialized state, and `ELAPSED_BY_OTHER_OWNER`.
- `P2_B02_PERIOD_MATERIALIZATION` receipts and `_recover_missing_receipts` close the state-before-receipt crash window once.
- A ran a real `P3Owner.realize` cycle with an ACTUAL S46 interval; B02's own states stay `SCHEDULED_ONLY/NOT_PERFORMED`.
- A's B04 purchase, B05 rent, P3-path and code-pin disclosures are valid at A's cut; I preserve them.

## 3. Defect established at the frozen composition

A's 32-test combined claim is not true at frozen merge `2a47fb389`. B04/B05 tests fail because B04 mutates the parent material document but C02 `_parent_material_history` does not recognize `P2_PARENT_PURCHASE`:

```text
read_parent_material -> PARENT_MATERIAL_HISTORY_MISMATCH
parent_feasible_actions -> PARENT_MATERIAL_HISTORY_MISMATCH
read_purchase -> PARENT_MATERIAL_HISTORY_MISMATCH
B05 parent read/work -> PARENT_MATERIAL_HISTORY_MISMATCH
```

This is not a test artifact; it is the exact parent-source composition gap. I repaired it in B04's owned material-side contract with a C02-recognized material-state bridge inside the purchase transaction (not a WORK/DEBT/CIRCUMSTANCE fake record). Exact C02 hook for full purchase-history exposure remains in `B04_B_ABI_REVISION.md`.

## 4. Independent B02 verification and added integration

I independently ran A's B02 suites: **9 passed** (`evidence/b02_b_verified.log`). I also added a real three-event P3 `BatchEngine` integration after the B02 employment split:

- custom employment change `2026-01-15`;
- `materialize_to 2026-01-16`, actual B02 split state;
- `BatchEngine` events 4–6 with exact existing plan proposal hashes;
- B04 parent-funded purchase and B05 household rent after the batch;
- B02 April read is PAST/retrospective and employment is `civic-works`;
- P3 head is unchanged by B04/B05; B05 rent changes household cash 55→43 and B03 feasibility becomes `REFUSED_AFFORDABILITY`.

Evidence: `SOROK-DUEL-B05-R1/evidence/b05_b.log` (3 passed) and combined `b01_b02_b03_b04_b05_b_combined.log` (37 passed). The batch is actual `BatchEngine` execution, not a P3Owner fixture masquerade. B02's `period_progress` can report P3 event-tick gaps; B05 carries `period_uncovered` rather than claiming full scheduled participation.

## 5. Corrections and proof

- B04 material-history bridge and material/parent locks; B05 rent lock and crash rollback; exact details in `SOROK-DUEL-B04-R1/B04_B_ABI_REVISION.md` and `SOROK-DUEL-B05-R1/B05_B_ABI_REVISION.md`.
- B04 crash test proves no parent debit/stock/ownership/history after a forced checkpoint failure; B05 crash test proves no cash debit/receipt after failure.
- B04 later parent activity makes purchase replay stale without a second debit.
- B05 duplicate operation/period behavior and cold replay remain green; P3 store head unchanged by B04/B05.
- Preserved: B01/B03/P6, C02 repaired vocabulary (not edited here), Pair2 inputs, no event vocabulary edit, no new scheduler/ledger.

## 6. Unresolved / exact hooks

- C02 `PARENT_B02_HOLD`/`historical_dates=NOT_AVAILABLE` remains stale Pair3 state; B04/B05 use actual B02 periods and do not treat the literal as authority. Pair3 must reconcile the literal and recognize `P2_PARENT_PURCHASE` in `_parent_material_history`/`read_parent_history` for full purchase history. The B04 material bridge keeps current material reads coherent meanwhile.
- No mother decision/utterance/hidden reason; no Nadia uptake; no public purchase/rent event; B04/B05 are objective material operations.
- B02 full P3 batch crossing a B02 split with materialize calls between events remains bounded: the added batch is after the split; P3 event gaps are reported, not fabricated. A full cross-boundary batch remains a challenge.
- No cold fork/full P6 experience; no landlord/arrears model; no variable rent/currency conversion; no native/science/rights/human/merge.
- P3 code-pin roots from all prior cuts incompatible; no migration.

## 7. Challenge to SAME A

1. Rebase on the B04 material-history bridge and prove `read_parent_material`/`parent_feasible_actions`/`read_purchase`/B05 parent work all pass after purchase; then implement the exact C02 hook so purchase history is directly recognized, without duplicate history rows.
2. Attack the B04 bridge: parent activity before/after purchase, two purchases, refused purchase, crash after bridge append, cold reopen. Prove one debit/one ownership and no fake activity.
3. Attack B05 rent lock/crash: concurrent different operations for one period, checkpoint failure, later household cash change, duplicate rent; one debit and one receipt only.
4. Build the full P3 `BatchEngine` 3–5 events **across** a B02 employment split with B02 materialize calls between events, not only after the split; show no double-advance or gap compression.
5. Reconcile `PARENT_B02_HOLD` and `historical_dates` without editing Pair3 files; show parent activity sees actual B02 period as-of state.
6. Do not weaken source pins, event vocabulary, parent history validation, or P6/P4 boundaries.

**Returned for same rival; no terminal acceptance.**
