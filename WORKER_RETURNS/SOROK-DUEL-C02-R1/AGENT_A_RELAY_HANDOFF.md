> **Superseded B02 status (A relay R3):** B02's actual incremental owner is now available (`period_progress`, `materialize_to`, `read_material_period`) and B proves two chronological parent periods plus source severance on the prepared composition. The `PARENT_B02_FULL_PROOF_HOLD`/current-period-only statements below are historical for this earlier cut; the current A consumer evidence is under `WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/A_RETURN_R3/`.

# SOROK C02 AGENT A RELAY — live-root composition and B02 ingress

**Role:** Pair3 Agent A relay, permanent session `ses_e31295836ffeW9bYwX9iiMMcXS`; only opponent SAME Pair3 B `ses_e31295826ffe6kteacpU7p3nQW`.
**Branch:** `codex/sorok-duel-c02-a-period-live-20261112-r1`.
**Implementation SHA:** `9ac1ac71cdbc8dd2c832b2980b501b4031e163e8`.
**Composition start:** `ea1f8d75b894c28d8a7bdb2d667761af2b67e310`.
**B frozen return:** `4d93685df4c5abdfbd09f44510a24a41c850b6a8`; B implementation `3f9d1079bc3b1f09a318afc80bd5aa63d7ccdecf`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.
**Grade:** `SOURCEFREE_S2_ONLY`; no native/science/rights/actor/human/protected authority.

## 1. B's return received — genuine strengths conceded

B's C02 kernel and relay are real and are preserved:

- **Truthful `MATERIAL_ACTIVITY` vocabulary.** A's `OFFSCREEN_REPAIR` carrier falsely attested a repair at `make_event`, the owner receipt and the projection/consumer chain. B's single `MATERIAL_ACTIVITY` event kind + matching receipt act is correct. I accept B's refutation of my “carrier kind” defense.
- **History-bound parent material.** Current material must equal the latest parent C12 history source; a recomputed/tampered document or severed activity episode fails closed. B's repair is correct.
- **Actual activity evidence validation.** `read_parent_activity` now validates author, activity/parameters, before/after sources, owner receipt, and parent `own_action` perception. B's D3 is genuine.
- **Explicit parent currency.** Parent cash/wage/debt carry `parent_sourcefree_currency_unit`, distinct from B03 household `sourcefree_currency_unit`, with no conversion. B's D4 is genuine.
- **Serialized parent writes.** A per-state-root lock around parent read-modify-write prevents lost/duplicated effects. B's D5 is genuine.
- **Live-root gap (D6).** B correctly established that direct C12/P2 parent writes after C01/C02 cause ordinary `run_p6.experience(state, "view")` to refuse `P4_COLD_STATE_MISMATCH`. Static house/parent reads are not a live-turn proof. This was A's most consequential remaining defect, and it is now repaired.

I found **no false accusation** in B's D1–D6. The only B statement now superseded is its global “B02 is absent/held” status: the actual B02 source exists at this composition and is now composed.

## 2. My own mistakes / false claims, conceded

- My prior C02 ABI's global `HELD_B02_CALENDAR_ABSENT` framing was false once B02 existed. The current code reads the actual B02 plan/current period; `PARENT_B02_HOLD` now means only “no B02 plan on this root.”
- My prior P6/B01/B03 “composition” test was static reader coexistence, not a live P6 consumer. B was right to reject reading it as a live-turn proof.
- My prior test expected `OFFSCREEN_REPAIR` and omitted parent currency; those were stale against B's correct repairs. I updated the A test to `MATERIAL_ACTIVITY` and `parent_sourcefree_currency_unit`.
- My first B02 ingress treated a one-sided B02 material state as “plan absent”; I tightened it so a partial B02 state fails closed for parent writes.
- I did not attempt a two-period proof with `materialize_periods`; that would use the full-plan interleaver the B02 owner is still counterstriking. The exact incremental/current-period API remains a finite required hook.

## 3. Repairs implemented

### A. Normal live-root parent background entry

```text
run_p4.run_parent_operation(state, *, operation, request)
run_p6.parent_background_operation(state, *, operation, request)
```

Closed operations:

```text
period-establish, parent-register, parent-establish,
parent-circumstance, parent-activity
```

The entry:

1. acquires the existing P4 `foreground_lock`;
2. loads `p4_receipts.json` and refuses if `pending`;
3. opens `state/actual-p2` through the normal `open_owner`;
4. calls `check_source` and the unchanged `check_boundary` **before any write**;
5. records a durable pending marker;
6. executes the existing B02/supporting/parent owner API;
7. clears pending and records the actual after snapshot/receipt through the existing `record_activity` (`ledger.activity_turns`, `last_boundary`, `foreground_witness`);
8. skips a new activity turn for a no-op/replay;
9. leaves pending set if a mutation was followed by failure (fail-stop, no re-bless).

No second ledger, scheduler, owner, callback, or direct snapshot-anchor rewrite. No user inspection prerequisite. Existing user-turn semantics are unchanged.

### B. B02 current-period ingress

`parent_activity` now loads the actual B02 module and uses:

```text
historical_period.read_period_plan(session)
historical_period.read_material_period(session, current_date)
```

The current date is derived from the committed plan anchor/clock/ticks and the actual current S46 clock. Qualified parent reads/options/activity/history carry the current period, tick, calendar/clock basis, plan source and interval status. A qualified activity event binds the period plan/period ID into its receipt and event body. B02 employment holder `A` is explicitly **not** applied to the parent; parent wage/currency remain parent-local, and household cash/conversion/spend permission remain `NOT_READ`/`C03_B04_HELD`/`NOT_APPLIED`.

B02 period-source severance makes current parent options `HELD` with `B02_PERIOD_UNAVAILABLE` while committed activity receipts retain their historical period context; restoring the exact plan restores current qualification. No `materialize_periods` full-plan advance and no fake dates.

## 4. Demonstrated live-root result

Fresh final-code P6 root:

```text
new
  -> normal background period-establish (actual B02 plan)
  -> normal background parent-register
  -> normal background parent-establish
  -> normal background parent-activity (PAID_WORK, MATERIAL_ACTIVITY)
  -> ordinary P6 view: succeeds
  -> ordinary P6 say("hello"): succeeds
  -> cold reopen/parent reads: period, material, options and activity receipt persist
```

Evidence:

| Check | Result | Log |
|---|---|---|
| Live-root parent/B02 packet | 5 passed in 78.14 s | `A_RETURN_R2/evidence/live_root_b02.log` |
| B + A C02 kernels | 11 passed in 30.29 s | `A_RETURN_R2/evidence/c02_ab.log` |
| C01 B/A + P2 owner + P3 owner | 28 passed, 1 skipped in 79.89 s | `A_RETURN_R2/evidence/c01_p2_p3.log` |
| B01 + B03 current cut | 15 passed in 92.82 s | `A_RETURN_R2/evidence/b01_b03.log` |
| B02 current cut | 7 passed in 47.37 s | `A_RETURN_R2/evidence/b02_period.log` |
| P4 response/speech + P5 gaze/experience | 7 passed in 67.92 s | `A_RETURN_R2/evidence/p4_p5.log` |

Negative/consumer discriminators:

- Direct unrecorded C01 registration on a fresh P6 root still makes `run_p6.experience(view)` and the background entry refuse `P4_COLD_STATE_MISMATCH`.
- A pending ledger refuses both view and background entry.
- An injected post-mutation failure leaves `pending` set; the next view/background entry refuses reconciliation.
- Repeating the parent activity operation through the P4 entry returns owner `REPLAY`, adds no activity turn, and leaves cash/world/episode counts unchanged.
- A fresh Python subprocess after parent activity runs ordinary P6 `view` and `say`; both succeed, with no parent secret/activity summary on the surface.
- Parent activity private secret and activity summary are absent from P6 view/say; focal access is `NOT_PERCEIVED`; P3 psychology head is unchanged.
- B02 qualified context has `logical_tick == activity clock`, period `period:2026-h1`, `b02_employment_applied_to_parent=False`, `interval_status=NOT_MATERIALIZED`; removing the plan source makes options held, restoring it requalifies, and past activity receipt is not retconned.

## 5. Unresolved requirements

- **Full C02 dated proof is held.** No two dated periods, split-period cold replay, or incremental interval materialization. Required B02 hook: `historical_period.current_material_period(session)` returning exact current period/tick/employment/interval without `materialize_periods` advancing the whole plan.
- **C03/C04 remain future.** No parent decision, performed utterance, hidden-reason vs speech split, or Nadia-qualified uptake.
- **E03 crash reconciliation remains future.** This return proves only pending fail-stop and no duplicate effect on retry; it does not claim SIGKILL recovery or composite event+participation atomicity.
- **Fork/cold parent lineage** remains unsupported by the C01 origin-branch registration refusal.
- **Shared household currency/spending** remains a B04/C03 boundary; no conversion, double count or spend permission is invented.
- **P3 source closure.** `parent_activity.py` is still unpinned by P3; the P3 integration owner must deliberately add it if required. No P3 edit.
- **MI/P5/P6 projection** of `MATERIAL_ACTIVITY` is deliberately not extended while the parent event is not a Nadia/user percept.
- **No full-estate run.**

## 6. Exact artifact / provenance

- Branch: `codex/sorok-duel-c02-a-period-live-20261112-r1`
- Implementation commit: `9ac1ac71cdbc8dd2c832b2980b501b4031e163e8`
- Start: `ea1f8d75b894c28d8a7bdb2d667761af2b67e310`
- B return: `4d93685df4c5abdfbd09f44510a24a41c850b6a8` / `3f9d1079bc3b1f09a318afc80bd5aa63d7ccdecf`
- Changed this turn:
  - `WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/run_p4.py` — normal background entry
  - `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py` — internal dispatch seam
  - `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_activity.py` — B02 current-period ingress
  - `WORKER_RETURNS/SOROK-DUEL-C01-R1/C02/test_c02_parent_activity.py` — accept B's truthful kind/currency
  - `WORKER_RETURNS/SOROK-DUEL-C02-R1/A_RETURN_R2/test_c02_live_root_b02.py` — live-root/B02 proof
- Return artifacts: `A_RETURN_R2/C02_LIVE_ROOT_ABI.md`, `C02_B02_INGRESS_ABI.md`, `PROGRAMMA_DELTA_LIVE_ROOT.json`, `PROGRAMMA_DELTA_B02_INGRESS.json`, `impact.json`, `evidence/*.log`.

## 7. Strongest remaining attack surfaces for SAME B

1. Implement the exact incremental B02 current-period API and prove two dated parent periods with cold reopen/source severance; do not use full-plan `materialize_periods` and do not rename years.
2. Attack the live-root entry's pending/fail-stop boundary with a real subprocess SIGKILL between world commit and ledger activity, and prove exactly-once or explicit reconciliation without duplicate effects.
3. Build C03's parent decision/utterance from the current parent material/options, then C04 hidden reason vs outward speech vs Nadia-qualified uptake; preserve no Nadia private leak.
4. Reconcile parent/household currency and spending without double count or fabricated wealth.
5. Prove fork/cold parent identity/material/activity under verified C12 ancestry without weakening C01 registration provenance.
6. Extend MI/P5/P6 `MATERIAL_ACTIVITY` exposure only through a lawful perceived/source path.

**Hardest concrete challenge for SAME B:** on one fresh final-code root, implement the exact incremental B02 current-period/two-period transition and a real C03 parent decision/utterance after a parent activity, with cold reopen and source severance, while preserving the live P4/P6 user-turn boundary, Nadia's focal root, parent-only self reads, no private leak, and no duplicate effects. A reader-only or static-house improvement will not surpass this cut.

## 8. Measured cost and limits

Test wall times are in the logs above. Controller/provider token, latency, process RSS and retry cost are `UNKNOWN`; no instrumentation was available or invented. The two full ChatGPT Library architecture records remain **NOT_INSPECTED locally**; no contents are claimed. This is a sourcefree engineering candidate, not independent terminal acceptance, native actor/science, source rights, human validation, or protected adoption.
