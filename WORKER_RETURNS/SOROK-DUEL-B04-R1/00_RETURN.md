# SOROK B04 Agent A return

**Task:** B04 parent-funded stock purchase/refusal (CG-B), depends B02/B03.
**Code:** `62292613aa9210a7d3e944314e36924349337439` (feature `a3f74693b`), branch `codex/sorok-duel-b02-a-relay-b04-b05-20261112-r1`.
**Handoff:** `AGENT_A_HANDOFF.md`; **ABI:** `B04_ABI.md`; **delta/impact:** `PROGRAMMA_DELTA.json`, `impact.json`.

## FINDING

A registered C02 parent can buy one source-qualified object from the actual P2 market stock with her own cash/free-hours. The object must exist before transfer; refusal does not debit or create ownership; B01 fixed-A household cash stays untouched; admission atomically writes parent material, market stock, ownership, a C12 receipt and one checkpoint. The later readers expose the changed stock/ownership and parent feasible actions.

## EVIDENCE

- B04 suite: 2 passed in 21.31s (`evidence/a_relay_b04.log`).
- Combined B01+B03+B02+B04+B05: 32 passed in 229.33s (`../SOROK-DUEL-B05-R1/evidence/a_relay_b01_b02_b03_b04_b05.log`).
- P6 test_house 8/8, P6 MII 18/18, adjacent 9/9.
- Negatives: wrong owner/currency/parent/price/market branch/parent branch; stock/funds/time/material refusals; no possession; no public event; cold/severance.

## LIMITS

No mother decision/utterance/uptake; no household-funded purchase; no public event/Nadia perception; no fork/cold-fork purchase; no general economy/landlord balance; parent_activity is Pair3-owned (new P2_PARENT_PURCHASE operation and stale PARENT_B02_HOLD need HQ reconciliation); prior P3 code-pin roots incompatible; cost UNKNOWN; one independent nonauthor receiving still required.
