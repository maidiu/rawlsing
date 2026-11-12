# SOROK B05 Agent A return

**Task:** B05 rolling material reproduction (CG-B), depends B02/B04.
**Code:** `62292613aa9210a7d3e944314e36924349337439` (feature `a3f74693b`), branch `codex/sorok-duel-b02-a-relay-b04-b05-20261112-r1`.
**Handoff:** `AGENT_A_HANDOFF.md`; **ABI:** `B05_ABI.md`; **delta/impact:** `PROGRAMMA_DELTA.json`, `impact.json`.

## FINDING

Across two completed B02 periods, household rent debits fixed-A cash only, C02 parent work changes parent cash/free-hours, and B04 parent-funded purchase changes stock/ownership without spending household cash. After rent 1 the B03 junior-kit availability flips from ADMISSIBLE to REFUSED_AFFORDABILITY; after rent 2 it remains refused; parent-funded purchases still succeed because the parent pays. Third purchase is refused on stock; duplicate rent is blocked; P3 head unchanged; cold replay exact.

## EVIDENCE

- B05 suite: 1 passed in 14.25s (`evidence/a_relay_b05.log`).
- Combined 32 passed in 229.33s (`evidence/a_relay_b01_b02_b03_b04_b05.log`).
- Cold subprocess exact rent/parent/owned/market/household/dwelling/feasibility/period/P3 head/counts; source severance/restore.

## LIMITS

No mother decision/utterance/uptake; static monthly rent, one charge per completed period, no arrears/landlord ledger/variable rent; C02 PARENT_B02_HOLD literal still stale (Pair3-owned); no full P3 3–5 batch; no cold fork; prior P3 code-pin roots incompatible; cost UNKNOWN; one independent nonauthor receiving still required.
