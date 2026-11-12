> **Later same-pair semantic revision:** the current code adds `PeriodInterleaveOwner` for B02 materialize calls between real BatchEngine events, removes the B04 antecedent bridge, and demonstrates post-purchase C02 parent refusal rather than bridge success. See `../SOROK-DUEL-B04-R1/AGENT_A_SEMANTIC_INTERLEAVE_HANDOFF.md` and `B05_A_SEMANTIC_ADDENDUM.md`; this file is retained as historical.

# SOROK B05 AGENT A — rolling material reproduction handoff

**Packet:** B05 `Prove multicycle material duration and later first-consumer parity` (CG-B), depends B02/B04.
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, actor/human right, source right, Pyat rule, or protected merge. Constructive author evidence, not independent receiving.
**Composition start:** `046f0f3be85cf13d6cab5acc1a5cd3e90dce17c5`.
**Branch:** `codex/sorok-duel-b02-a-relay-b04-b05-20261112-r1`.
**Code:** final SHA `62292613aa9210a7d3e944314e36924349337439`; feature commit `a3f74693b70cb09f0e8bac4a7ca094812173db3a`.
**Running contract:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Module:** `WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py`.
**ABI:** `B05_ABI.md`. **Delta/impact:** `PROGRAMMA_DELTA.json`, `impact.json`.

## 1. Exact artifact

| Path | Change |
|---|---|
| `WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py` | Household rent obligation on fixed-A cash, one charge per completed B02 period, atomic receipt/checkpoint, source-chain reader. |
| `WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_rolling.py` | Two dated cycles, rent, C02 parent work, B04 purchase, later B03 feasibility, duplicate-rent, source severance/restore and cold subprocess. |

Untouched: `parent_activity.py`, `supporting_actor.py`, P3, `situated.py`, P6 `house.py`, B01/B03 production, B04 module, guides/workflows/Pyat/config.

Commands and evidence:

```text
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_rolling.py
```
1 passed in 14.25s (`evidence/a_relay_b05.log`). Combined B01+B03+B02+B04+B05 32 passed in 229.33s (`evidence/a_relay_b01_b02_b03_b04_b05.log`). P6 house 8/8, P6 MII 18/18, adjacent 9/9.

## 2. Governing contract

B05 requires ordinary life to progress across dated intervals with recurring costs, changed constraints and a next actual consumer; the negative is all elapsed time auto-generating psyche, an old source surviving revocation, or period time compressing away causally important change. Restoration must cold-replay exactly. B05 depends on actual B02 dated periods and actual B04 material operations; no second scheduler/ledger. `SCHEDULED_ONLY` periods are `NOT_PERFORMED`, not performed work. C03/C04 parent decision/utterance remain future; native/science/rights/human/merge held. The two Library architecture records remain NOT_INSPECTED locally.

## 3. Strongest achieved result

`apply_household_rent(session, operation_id, period_id)` charges the actual B03 dwelling `monthly_rent` against the **B01 fixed-A household cash** only after the B02 period is `COMPLETE`. It:
- refuses a non-complete period before any effect;
- refuses/records one rent per period (`B05_RENT_ALREADY_RECORDED` for a different operation on the same period);
- debits actor-A household cash only if cash >= rent; insufficient cash is a durable REFUSED receipt with no debit and no negative balance;
- records a C12 `P2_HOUSEHOLD_RENT` receipt and one checkpoint in the same `_StoreWrite` transaction;
- does not debit the registered parent's C02 cash, emit a public event/perception, or write P3 psychology;
- carries stable household document source, dwelling source, current household cash, period status and `scheduled_participation=NOT_PERFORMED`.

`read_household_obligation` verifies the stable household/dwelling sources and rent arithmetic; it returns the durable receipt, current household cash and a `historical` flag when later rent/parent activity has moved the current state. A severed dwelling/household source refuses; restore returns the exact read.

The test runs two complete dated cycles:
1. `materialize_to 2026-07-01`; rent period 1 (household cash 55→43); C02 `PAID_WORK` (parent cash 60→70, free 8→6); B03 junior-kit availability flips from ADMISSIBLE to REFUSED_AFFORDABILITY (household cash 43, rent due 12, price 40); B04 parent-funded purchase succeeds despite household affordability (parent cash 70→30, free 6→5, ownership 1, stock 1); household cash/dwelling unchanged by the purchase.
2. `materialize_to 2027-01-01`; rent period 2 (household 43→31); C02 `PAID_WORK` (parent 30→40, free 5→3); B04 purchase (parent 40→0, free 3→2, ownership 2, stock 0); third purchase REFUSED stock with no debit; parent feasible PAY_DEBT becomes REFUSED_INSUFFICIENT_CASH; P3 store head unchanged.
3. `read_material_period` at 2026-04-01 and 2026-08-01 shows the midperiod employment change (`civic-works`) as a past, retrospective materialized read, not a future/current claim.
4. Duplicate rent, same-op replay, source severance/restore and cold subprocess exact.

## 4. Own hostile findings

1. **Rent vs parent cash.** I deliberately debit fixed-A household cash for the household rent and keep parent C02 cash for parent work/purchase. This avoids silently spending either actor's money for the other. A parent-funded rent variant is not built.
2. **One rent per period, but no arrears model.** A REFUSED insufficient-cash rent is recorded and blocks a different operation for the same period; there is no later arrears settlement. This is a bounded recurrence, not a complete rent economy.
3. **Static rent.** The B03 `monthly_rent` is static; no variable rent, landlord balance, or currency conversion. `rent_due_now` is context, not the recurring rule.
4. **Household cash can change via other P6 actions.** The rent reader uses receipt arithmetic plus stable household/dwelling sources and reports `historical`; it does not require the current cash to equal the historical after. A later unrelated cash change does not invalidate the historical receipt, but the next rent's before/after arithmetic is its own.
5. **No P3 psychology.** The test asserts P3 store head unchanged; the P3 cycle is a separate B02 test. Rent/parent/purchase do not generate traits or memory.
6. **My first B05 implementation checkpointed cash before the rent receipt.** I moved both into one transaction. My first chain check compared clock-dependent household material hashes; I replaced it with receipt arithmetic plus stable source checks. Both were my defects, repaired.
7. **C02 stale B02 hold.** `parent_activity.py` still reports `HELD_B02_CALENDAR_ABSENT`; B05 uses B02 directly and does not treat that literal as authority. The C02/C03 owner must reconcile it.
8. **No public event.** Rent is a household material obligation; `public_event=NOT_EMITTED`, `event_effect=NONE`; no Nadia perception.

## 5. Unresolved challenges

- C03/C04 parent decision/utterance/uptake; B05 supplies material inputs and recurring constraints, not a mother decision.
- Variable rent, arrears settlement, landlord/institution balance, multiple currencies.
- C02 stale `PARENT_B02_HOLD` literal and `historical_dates`; exact Pair3-owned symbols must be reconciled.
- Full P3 `BatchEngine` 3–5 cycle across periods (B02 proves one real `P3Owner.realize`).
- Cold fork/full P6 experience on a fork; B02/B04/B05 fork purchases/rent are not claimed.
- P3 code-pin migration: final `p2_owner` slots invalidate prior roots; fresh final-code roots used; no migration.
- Native/science/rights/human/merge held; two Library records NOT_INSPECTED.
- Cost UNKNOWN.

## 6. Likely attack surfaces for SAME B

1. Change household cash via a non-rent P6 action between rents; re-read historical rent and next rent. The receipt arithmetic/stable sources should remain clear.
2. Charge two rents for one period with different operation IDs; require `B05_RENT_ALREADY_RECORDED` and no second debit.
3. Make rent > household cash; require REFUSED, no debit, no negative balance, and no stale source claim.
4. Remove/change the dwelling/household source; require read/rent refusal; restore exact.
5. Run a full P3 batch across the employment change and a B04 purchase between periods; verify no double-advance/period compression.
6. Reconcile the C02 `PARENT_B02_HOLD` literal without editing Pair3 live files.
7. Test a child fork and a cold restart after a rent/purchase; no phantom owner/period.

**Hardest constructive challenge for SAME B:** run a full P3 `BatchEngine` 3–5 event cycle across the B02 midperiod change with B04 purchase and B05 rent between periods, inject a crash after the rent receipt before the checkpoint (and after the S46 state before the B02 receipt), and prove cold-recovery preserves one rent, one debit, one ownership record, one period and the exact employment as-of. This is the next real integration.

## 7. Rejected alternatives

- **Debit parent cash for household rent.** Rejected: the household rent is a fixed-A household obligation; the parent's independent cash must not be silently used. Parent cash changes only via C02 work/purchase.
- **Debit B01 cash for the parent's purchase.** Rejected by B04; B05 keeps the two funding sources separate.
- **Charge rent at period start or before completion.** Rejected: a scheduled-only period is not a completed material period; rent is charged only after `COMPLETE`.
- **Allow a second rent with a new operation ID.** Rejected: one recurring cost per period; duplicate operation blocked.
- **Auto-apply all periods in one rent call.** Rejected: B02 incremental periods and one receipt per completed period; no time compression.
- **Use elapsed time to generate psyche or work.** Rejected: rent/parent/purchase are material; scheduled participation is NOT_PERFORMED; P3 head unchanged.
- **Emit a public rent event.** Rejected: no event vocabulary edit; actual household cash receipt is the consumer.
- **Model a landlord ledger.** Rejected: out of B05 scope; no second ledger.

## 8. Proof boundaries

Do not claim: a mother decision/utterance/uptake; a landlord/institution balance; variable rent/arrears; a completed household economy; a full P3 batch; cold fork; native actor/world science, rights, human validation, or protected merge; old P3 root compatibility; full-estate coverage. B05 is executed author evidence at the code cut above; one independent nonauthor receiving remains required. Cost UNKNOWN.
