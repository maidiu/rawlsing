# SOROK B05 AGENT B — one-debit rolling rent and batch/material integration

**Packet:** B05 `Prove multicycle material duration and later first-consumer parity`, CG-B.
**Grade:** `SOURCEFREE_S2_ONLY`; no native/science/actor/human/rights/merge authority.
**Composition start:** `2a47fb389b453c2f902b8c13ed52304fb40efd0d`.
**Branch:** `codex/sorok-duel-b04-b05-b-counter-20261112-r1`.
**Implementation SHA:** `4a3c45cda7d814df0c60ca4e245499fcfca62162`.
**Main relay handoff:** `WORKER_RETURNS/SOROK-DUEL-B04-R1/AGENT_B_HANDOFF.md`.
**B05 ABI revision:** `B05_B_ABI_REVISION.md`.
**Machine records:** `WORKER_RETURNS/SOROK-DUEL-B04-R1/PROGRAMMA_DELTA_B.json`, `impact_B.json`.

## 1. Exact artifact and preserved A work

A's B05 implementation is preserved: rent only on a `COMPLETE` B02 period, one rent per period, B01 fixed-A cash only, durable REFUSED receipt with no debit, one `_StoreWrite` over cash/checkpoint/receipt, no parent-cash debit for rent, no public event/P3 psychology, and historical rent reads after later activity.

This round adds:

- `rolling_reproduction._rent_lock` and a public `apply_household_rent` wrapper around the complete read/check/write unit.
- `test_b05_rollback.py`: injected checkpoint failure leaves no cash debit and no receipt; cold reopen and a later valid rent debit exactly once.
- `test_b05_batch_cycle.py`: actual three-event P3 `BatchEngine` after the B02 employment split, then B04 parent purchase, B05 materialization and rent; P3 head unchanged by B04/B05.

## 2. Governing requirement reconstruction

B05 requires ordinary life across dated intervals with recurring costs, changed constraints and a next actual consumer. It must not auto-generate psyche/traits/work from elapsed time; a source removal must refuse/change the read; cold replay must be exact. Rent is a material obligation, not a mother decision or public event. The two Library architecture sources remain NOT_INSPECTED locally.

## 3. A's valid findings and concessions

A's B05 receipt arithmetic, stable household/dwelling source checks, one-rent-per-period rule, refusal no-debit, cold subprocess and historical read are real. I preserved them. A's B02/B04 handoffs correctly identified the parent-history composition gap; B04's material bridge (see main handoff) is required for B05's parent-work read after purchase.

## 4. Defects and repairs

1. **Rent read/check/write was not serialized.** Two callers could both observe no rent for a period and append two debits/receipts. Fixed with a state-root file lock around the complete unit; not a scheduler/ledger.
2. **Crash rollback was not exercised at the checkpoint seam.** Added injected checkpoint failure; the existing `_StoreWrite` rolls back cash and receipt; cold state remains pre-rent.
3. **B05 depended on B04/C02 composition.** At frozen composition, B04 purchase made C02 parent history inconsistent and B05 parent reads failed. B04's material-state bridge fixes the current-material path; exact C02 purchase-history hook remains Pair3-owned.
4. **No actual multievent P3 batch in B05.** Added a real `BatchEngine` three-event run after a B02 employment split, then purchase/rent. It is actual batch execution, not a fixture; a batch with B02 materialize calls between events remains unproved.

## 5. Proof

- B05 rolling + rollback + batch: **3 passed in 72.10s** (`evidence/b05_b.log`).
- Combined B01+B03+B02+B04+B05: **37 passed in 332.40s** (`evidence/b01_b02_b03_b04_b05_b_combined.log`).
- P6 house/P2/actor: **15 passed in 216.57s** (`evidence/p6_adjacent_b.log`).
- P6 MII: **18 passed in 247.53s** (`evidence/p6_mii_b.log`).

The batch test verifies B02 split/currentness, three actual P3 records with `MISSING_RULE`, B04 stock/ownership/parent bridge, rent 55→43, B03 household affordability refusal, and unchanged P3 head after B04/B05. Rent crash recovery proves one debit after cold reopen.

## 6. Boundaries

No mother decision/utterance/uptake; no public event/Nadia perception; no parent cash for rent; no household cash for purchase; no variable rent/arrears/landlord ledger/currency conversion; no cold fork; no full P6 live turn; no native/science/rights/human/merge; P3 prior roots incompatible; Library sources NOT_INSPECTED. B05 receipt may report `period_uncovered` when P3 event ticks create gaps; no full scheduled coverage is claimed. A refused rent blocks a different operation for the same period; there is no arrears model.

## 7. Challenge to SAME A

Attack the rent lock with concurrent different operations for one period and an injected checkpoint failure; prove one debit and one receipt. Attack B05 after a later unrelated household cash change, severed/replaced dwelling or household source, and cold restart. Consume the actual B02/B04/P3 batch path without claiming full scheduled participation where `period_uncovered` is nonempty. Reconcile `PARENT_B02_HOLD` and the C02 purchase-history hook without editing live Pair3 files.
