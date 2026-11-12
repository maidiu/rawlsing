> **Later same-pair semantic revision (B04/B05):** final tested code `4959596dd2e130a3856cc3b9d7ce24f8d0261400`. B's antecedent bridge is removed; after the first purchase C02 parent material/feasible/activity actually refuse `PARENT_MATERIAL_HISTORY_MISMATCH` until the typed `P2_PARENT_PURCHASE` hook, and read_purchase exposes that. A real 3-event BatchEngine now crosses the B02 split with materialize calls between events. Combined B01+B03+B02+B04+B05 is 39 passed; see `../SOROK-DUEL-B04-R1/AGENT_A_SEMANTIC_INTERLEAVE_HANDOFF.md`. The B02 period capability below is unchanged; its B04/B05 paragraphs/timings are historical and superseded.

# SOROK B02 AGENT A RELAY — incremental periods, P3 interleave, B04/B05

**Packet:** B02 counterstrike, then the same pair's B04 and B05 bounded constructions.
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, actor/human right, source right, Pyat rule, S14/A5 grant, or protected merge. Constructive author work, not independent terminal receiving.
**Composition start:** `046f0f3be85cf13d6cab5acc1a5cd3e90dce17c5` (B02 B + C02 A + D01/D02 A auto-composed by HQ; UNEXECUTED/UNACCEPTED as a combination).
**Opponent frozen return:** `4f78bf71d9674450f4b32811f0dbee84adf3ed14`; B implementation `509784c2850c499d1f640c9f43c569416081d76d`.
**Branch:** `codex/sorok-duel-b02-a-relay-b04-b05-20261112-r1`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

**Final tested code SHA:** `62292613aa9210a7d3e944314e36924349337439` (B02/B04/B05 feature commit `a3f74693b70cb09f0e8bac4a7ca094812173db3a`). Return/docs test HEAD is the branch tip after this handoff commit; `PROGRAMMA_DELTA_A_RELAY.json` carries the same exact values.

## 1. B's valid findings and improvements, explicitly acknowledged

1. **B02's dated plan/employment/as-of construction is real.** B wrote two source-qualified P2 facts through `write_material_fact`, mapped Gregorian dates explicitly to `S46_TEST_ONLY_LOGICAL_TICK_DAY_V1` at one tick/day, split the first period at the 2026-03-15 employment change, used the existing `session.produce_interval`, and proved no duplicate period on retry and cold replay. I ran B's suite independently (7 passed before my changes; 9 after the corrected span expectation).
2. **B's B03 same-root PsycheStore negative closes a real A evidence gap.** It writes a valid mediator through the actual root's `p3_psyche.sqlite3`, shows B03 production readers ignore it, severs the world dwelling and shows refusal while the store query remains, then restores. I preserved it and ran it in the combined suite.
3. **B's fork/provenance and prefix repairs remain sound.** B's C12 ancestor reads, `state_scope=C12_FORK_WITHOUT_S46_INTERVAL_STATE`, and the A `_copied_prefix_equal` actual-row check are preserved. B did not weaken P3 pins or P6 semantics.
4. **B correctly priced B02's limits.** It disclosed that B02 was not a full P3 cycle, that `SCHEDULED_ONLY` is not performed work, that materialization was all-periods-up-front, and that the P3 code-pin break is a real compatibility cost.

## 2. B's invalid or incomplete findings

### 2.1 Consequential: `materialize_periods` advanced every dated period before any P3/ordinary activity

`materialize_periods` built all period domains and called `produce_interval` for each up front. Once it ran, the session clock was at the end of the whole plan. There was no API to advance to a date inside a period, run a P3/owner cycle, and then continue; `read_material_period` only recognized a full-period domain hash. This made “interleaving” impossible in the actual clock, not merely untested.

**Repair:** `materialize_to(session, as_of_date)` advances only from the current clock to the target, period by period, splitting at employment changes inside the new range. `period_progress` exposes clock progress, B02 coverage, all S46 state coverage, gaps, remaining segments and remaining span. `materialize_periods` is retained as a legacy whole-plan wrapper over the incremental API.

### 2.2 Consequential: `p3_interval_span` returned the full period duration after time had already elapsed

After a period was materialized, `p3_interval_span` still returned its full 181/184-tick duration. A next P3 proposal would double-advance the period.

**Repair:** `p3_interval_span` now returns `max(0, period_end - max(current_clock, period_start))`, net of current progress, and accepts an optional target date. At a completed period it returns span 0; the caller must not propose a non-positive interval. B's old test encoded the full-duration-after-completion behavior; I corrected that assertion and added the remaining-span proof before materialization. This is a real behavior change, not a test-only accommodation.

### 2.3 Incomplete: no actual P3 DevelopmentOwner cycle was executed

B validated `P2Owner.validate_proposal` with the interval shape but did not run `P3Owner.realize`. I ran an actual `P3Owner.realize` cycle with the existing `vertical:event:2` plan and its exact `proposal_hash`, after a partial B02 advance. The cycle admitted an ACTUAL S46 interval, committed the P3 owner operation (`phase=COMPLETE`), wrote the owner receipt and response, advanced the clock from anchor+1 to anchor+4, and left `durable_psychological_transition=MISSING_RULE` (no fabricated psychology). The B02 period progress then showed the P3 interval as `ELAPSED_BY_OTHER_OWNER`, not as a B02 period state.

### 2.4 Incomplete: as-of currentness was not distinguished

B's reader could return a future employment term with `employment_status=EFFECTIVE` at a future as-of date, and a past as-of read after later materialization looked like a current snapshot. The reader now carries:

```text
as_of_relation                  PAST | CURRENT | FUTURE
employment_is_current           bool
employment_currentness          CURRENT_AS_OF | PAST_AS_OF | FUTURE_NOT_CURRENT
current_employment              employment effective at the current world clock
current_employment_status
interval_status_detail          MATERIALIZED_AT_AS_OF |
                                MATERIALIZED_RETROSPECTIVELY |
                                ELAPSED_BY_OTHER_OWNER |
                                FUTURE_NOT_MATERIALIZED |
                                NOT_MATERIALIZED_AT_AS_OF |
                                CURRENT_NOT_MATERIALIZED
state_admitted_clock
state_available_at_as_of
retrospective
period_progress
```

A future employment term is still available to a planning/read query under `employment`, but it is explicitly not current. A past as-of read of a state produced later is explicitly retrospective. `p3_interval_span` and all B02 readers remain material-only; no psyche or calendar native claim is made.

### 2.5 Incomplete: a state produced before its receipt was not recoverable

`produce_interval` commits the S46 state before B02 can append its own materialization receipt. A crash between those commits left a real state with no B02 receipt; `read_material_period`/progress would not count it and a retry at the same clock returned `ALREADY_CURRENT`.

**Repair:** `_recover_missing_receipts` scans states within the plan, requires `SCHEDULED_ONLY`, the exact plan/employment segment boundaries and an in-period range, appends a `RECOVERED` receipt, and returns `RECOVERED` exactly once. `test_crash_after_state_before_receipt_recovers_once` produces the state without a receipt, proves `RECOVERED`, proves progress `[[anchor, period_end]]`, and proves a retry adds no second receipt.

### 2.6 Not a defect: B's `SCHEDULED_ONLY` is not performed work

I preserved the explicit `NOT_PERFORMED`/`NOT_ATTEMPTED` semantics. The P3 interleave uses an ACTUAL interval for the owner cycle; B02's own period states remain `SCHEDULED_ONLY`. B04 purchase/refusal and B05 rent do not claim scheduled participation. No elapsed-time psychology or work participation is inferred.

### 2.7 Stale C02 qualification (Pair3-owned, disclosed not edited)

`parent_activity.py` still returns `period_qualification=HELD_B02_CALENDAR_ABSENT` and `historical_dates=NOT_AVAILABLE`. B02 now provides the dated plan, and the B04 purchase receipt includes the actual B02 period reference (`period_id`, `as_of_date`, `as_of_relation`, `interval_status`). The stale C02 literal is a Pair3/C02 composition obligation; I did not edit `parent_activity.py` or claim C02 dates are complete. Exact symbol/effect for HQ: `developmental_recursion.parent_activity.PARENT_B02_HOLD` (and the `period_qualification`/`historical_dates` fields in `_read_material`, `parent_feasible_actions`, `read_parent_activity`, `read_parent_history`) must be reconciled by the C02/C03 owner. B04/B05 use the actual B02 reader directly and do not treat the literal as authority.

### 2.8 Own mistake found in my first B02 implementation

My first `read_material_period` called `_all_states` before checking inherited fork provenance; on a child fork the S46 validator raised `S46_STATE_BRANCH_MISMATCH`, breaking B's fork test. I moved state reads behind the inherited check and the fork test passes. My first B05 receipt chain compared `household_material_hash` across clock advances; because the B01 material hash includes the current clock, the chain falsely went stale. I replaced the chain check with the durable receipt arithmetic plus stable household/dwelling source checks and historical cash; the final B05 test passes. These were my defects, repaired before return.

## 3. New defects discovered independently

1. B02 full-period up-front advancement and full-duration P3 span (2.1/2.2).
2. No actual P3 owner cycle (2.3).
3. Future/past as-of currentness missing (2.4).
4. State-without-receipt crash gap (2.5).
5. B's B02 tests did not exercise B04/B05; the B04/B05 construction below exposed the need for a source-qualified market inventory, explicit ownership, parent-local funding and household rent separation.
6. **B04 reconciliation defect risk:** a purchase funded from B01 fixed-A household cash would silently spend the focal household's money for the mother. The B04 implementation uses the registered parent's C02 cash/free-hours; the B01 household cash is proven untouched. B03's `REFUSED_AFFORDABILITY` is treated as a household-cash constraint, and the parent funding check is separate (no unit conversion; declared sourcefree currency basis).
7. **B05 double-rent risk:** a different operation ID could charge the same period twice. `B05_RENT_ALREADY_RECORDED` prevents that; a same-operation retry returns REPLAY/historical without a second debit.
8. **B05 rent/actor-A cash atomicity:** my first version checkpointed the household cash before appending the rent receipt. I moved the cash update, checkpoint and receipt into one `_StoreWrite` transaction; a failure rolls back both. The final test exercises cold and source severance.

## 4. Repairs implemented and demonstrated effects

### 4.1 B02 incremental dated API (`historical_period.py`)

- `materialize_to(session, as_of_date)`: incremental advance, target not in future beyond plan, no past target, no rewind, no duplicate interval, splits at employment changes only inside the new slice, appends a durable C12 `P2_B02_PERIOD_MATERIALIZATION` receipt per state.
- `period_progress(session, period_id)`: `BEFORE|PARTIAL|COMPLETE`, elapsed/remaining ticks, B02 coverage, all-S46 coverage, gaps, other-owner states, remaining segments and `next_p3_span`.
- `remaining_span(session, period_id, to_date=None)` and corrected `p3_interval_span`.
- `read_material_period` currentness/as-of/retrospective fields and interval coverage over partial states.
- `_recover_missing_receipts` for the state-before-receipt crash window.
- `materialize_periods` retained as a full-plan wrapper; old test expectations corrected only where they encoded the full-span bug.

### 4.2 B04 parent-funded stock purchase (`SOROK-DUEL-B04-R1/material_operations.py`)

- `p6_market_inventory` and `p6_owned_objects` are two new source-qualified P2 world facts; no second household database.
- `establish_market_inventory`/`read_market_inventory`: real stock must exist before transfer.
- `purchase_drum_kit(parent, owner_actor_id, request)`: registered-parent cash/free-hours are spent; B01 fixed-A cash/free-hours are proven untouched. The object must exist in market stock, price/currency must match, B03 material constraints must not refuse (household `REFUSED_AFFORDABILITY` is separated from parent funding), stock is decremented and ownership is added.
- Atomic `_StoreWrite`: C12 receipt + parent material + market stock + ownership + one checkpoint; a failure rolls back all. Refusal is a durable C12 receipt with no debit/stock/ownership change. Idempotent operation ID; immediate retry returns REPLAY; later-state retry is stale rather than re-debited.
- No world event/perception is emitted; `public_event=NOT_EMITTED_HELD_PAIR3_VOCABULARY`, `event_effect=NONE`. The actual later readers are `read_owned_objects`, `read_market_inventory`, `read_purchase`, `parent_feasible_actions`.
- The receipt includes the actual B02 period reference when the plan is established; otherwise `B02_NOT_AVAILABLE`.

### 4.3 B05 rolling material reproduction (`SOROK-DUEL-B05-R1/rolling_reproduction.py`)

- `apply_household_rent(period_id, operation_id)`: only a `COMPLETE` B02 period can be charged; one rent per period; household fixed-A cash is debited (not parent cash); atomic checkpoint + C12 `P2_HOUSEHOLD_RENT` receipt; no public event/psyche.
- `read_household_obligation`: verifies stable household/dwelling sources and rent arithmetic; returns current household cash and historical flag; source severance refuses.
- Combined with C02 `PAID_WORK`, B04 purchase and B02 `materialize_to`, the test shows: rent period 1 changes household cash 55→43 and flips B03 junior-kit availability from ADMISSIBLE to REFUSED_AFFORDABILITY; parent PAID_WORK changes parent cash/free-hours; parent-funded purchase succeeds despite household affordability because the parent pays; period 2 rent changes 43→31; second parent-funded purchase succeeds; third is refused on stock; P3 head unchanged; cold subprocess exact.

## 5. Regressions and negative controls tested

| Command | Result | Evidence |
|---|---|---|
| B02 period + incremental suite | **9 passed in 77.61s** | `WORKER_RETURNS/SOROK-DUEL-B02-R1/evidence/a_relay_b02.log` |
| B04 operations suite | **2 passed in 21.31s** | `WORKER_RETURNS/SOROK-DUEL-B04-R1/evidence/a_relay_b04.log` |
| B05 rolling suite | **1 passed in 14.25s** | `WORKER_RETURNS/SOROK-DUEL-B05-R1/evidence/a_relay_b05.log` |
| B01+B03+B03 same-root+B02+B04+B05 combined | **32 passed in 229.33s** | `WORKER_RETURNS/SOROK-DUEL-B05-R1/evidence/a_relay_b01_b02_b03_b04_b05.log` |
| P6 `test_house.py` | **8 passed in 162.31s** | `WORKER_RETURNS/SOROK-DUEL-B05-R1/evidence/p6_test_house.log` |
| P6 `test_mii.py` | **18 passed in 231.49s** | `WORKER_RETURNS/SOROK-DUEL-B05-R1/evidence/p6_test_mii.log` |
| P2 owner + actor scene + selected P3 reopen/config | **9 passed in 51.18s** | `WORKER_RETURNS/SOROK-DUEL-B05-R1/evidence/adjacent.log` |
| Pre-existing P6 chronology proof | **1 failed** on `mii_exposure_id`/`mii`, unchanged from baseline `6a5c12f` | `WORKER_RETURNS/SOROK-DUEL-B03-R1/evidence/p6_chronology_pre_existing.log` |

Negative controls exercised: past target refused; outside-plan target refused; future as-of not current; past as-of retrospective; no duplicate period on retry/cold; state-before-receipt recovery once; P3 event interval distinct from B02 period state; rent only on complete period; duplicate rent period blocked; insufficient household cash refused without debit; B04 wrong owner/currency/parent/price/market-branch/parent-branch refused; insufficient parent cash/time refused without debit; stock exhaustion refused; no possession on refusal; B03 material constraint refusal; no world event/perception; no P3 store change from B05; source severance/restore; cold subprocess.

## 6. Requirements still unfulfilled

- **C03/C04:** no actual parent decision, performed utterance, hidden-reason separation or Nadia-qualified uptake. `mother_material_input` remains `NONE_VERIFIED`; B04 purchase is an objective operation, not a mother decision.
- **B02 full P3 batch:** I ran a real single `P3Owner.realize` cycle, not a 3–5 event `BatchEngine` batch. A full batch and P3 source-closure decision remain.
- **C02 stale hold:** the exact Pair3-owned `PARENT_B02_HOLD` literal and C02 `historical_dates` fields still say B02 calendar is absent; B04/B05 use the real B02 reader, but the C02/C03 composition must reconcile that symbol. I did not edit `parent_activity.py`.
- **P3 code-pin migration:** the final `p2_owner.py` byte change invalidates P3 roots from `5bc29474e`, A's `993339851`, B's `362719b40`, and the composition start. Fresh final-code roots are used and tested; no migration or pin weakening. P3/Pair2 receiving owns migration.
- **Cold fork:** B02 fork reads remain material-only; new materialization on a fork is refused. No cold fork/full P6 experience on a fork is claimed.
- **Same-root PsycheStore:** B03's same-root negative is preserved; B04/B05 do not claim a new same-root psychology proof.
- **B04 public event:** no outward purchase event or Nadia perception is emitted. The event vocabulary/projection hook is Pair3-leased; the receipt explicitly holds it.
- **B05 economics:** rent uses the declared static `monthly_rent`, one charge per completed period; there is no landlord balance, arrears amortization, variable rent, or multi-currency conversion. The parent cash unit is declared sourcefree currency; no unit conversion is performed.
- **No external receiving:** this is executed author evidence at one cut, not independent nonauthor acceptance. The composition is unexecuted/unaccepted as a combination.
- **Native/science/rights/human/merge:** held. Two ChatGPT Library architecture records remain NOT_INSPECTED locally.
- **Cost:** UNKNOWN; no controller/provider token, latency, RSS or retry instrumentation was available or invented.

## 7. Exact artifact, provenance and execution receipts

- Branch/start/opponent: see header. Code commit: the commit containing
  `historical_period.py`, `test_b02_incremental.py`, `test_b02_period.py`,
  `p2_owner.py`, `material_operations.py`, `test_b04_operations.py`,
  `rolling_reproduction.py`, `test_b05_rolling.py`; exact SHA is in
  `PROGRAMMA_DELTA_A_RELAY.json` (`implementation_sha`).
- Changed code:
  - `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py`:
    added the `p6_market_inventory`/`p6_owned_objects` material-slot allowlist entries. No P2 constructor/validate/realize/participant edit.
  - `WORKER_RETURNS/SOROK-DUEL-B02-R1/historical_period.py`: incremental `materialize_to`, `period_progress`, `remaining_span`, corrected `p3_interval_span`, receipt/recovery, as-of currentness.
  - `WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py`: market inventory, ownership, parent-funded purchase/refusal, readers.
  - `WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py`: household rent/obligation reader.
- Untouched: `parent_activity.py`, `supporting_actor.py`, P3, `model_cycle`, `situated.py`, P6 `house.py`, B01/B03 production, guides/workflows/Pyat/config.
- Commands are in the B02/B04/B05 evidence logs above. The same qualified environment `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider ...` was used.

## 8. Strongest remaining attack surfaces for SAME B

1. **Full P3 3–5 event batch across two periods:** run `BatchEngine`/`RecursionCycle` with plans and intervals spanning the employment change; attack whether the B02 receipt/P3 state interleave remains exact, and whether a P3 interval can cross a B02 period boundary without double-advance.
2. **Crash windows:** crash after the B02 receipt but before the S46 checkpoint? The receipt is appended after the producer; the producer checkpoints. Crash after S46 state and before receipt is recovered. Attack the inverse and a crash after the B04 parent material update but before the C12 receipt (the `_StoreWrite` rollback should cover it), and a B05 rent crash.
3. **B04 funding/ownership:** make the parent material branch/source stale; make a child fork purchase; use a different owner actor slot; tamper market stock/ownership sources; retry a purchase after later parent activity. Verify no double debit, no conjured object, no B01 cash spend.
4. **B05 recurrence:** add a second rent for the same period with a different operation; change household cash by an unrelated P6 repair between rents; change the dwelling rent/tenure; sever/restore the market/owned/dwelling; test a later as-of read and cold reopen.
5. **As-of/currentness:** a leap-year custom plan, a term effective exactly at a period boundary, a date after the last period, a future as-of that would otherwise return a future term as current. The reader should distinguish planning/as-of from current.
6. **C02 stale hold:** reconcile `PARENT_B02_HOLD` and C02 `historical_dates` without editing Pair3 live files; prove the parent activity/decision sees the actual B02 period and not a fake date.
7. **P3 code-pin migration:** do not weaken pins or rewrite accepted state. Prove a lawful migration at the Pair2/shared-receiving boundary if old roots must survive.

**Hardest constructive challenge for SAME B:** run a full P3 `BatchEngine` 3–5 event cycle across the B02 midperiod employment change, with a P3 interval that ends exactly at a B02 period boundary and a B04 purchase between periods, then cold-crash every owner boundary and prove one period, one rent, one debit, one ownership record and one P3 record set. This is the next real integration, not another reader test.
