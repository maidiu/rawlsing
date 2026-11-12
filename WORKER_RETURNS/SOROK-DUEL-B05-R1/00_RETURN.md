# SOROK B05 Agent A return — cross-boundary material interleave

**Task:** B05 rolling material reproduction (CG-B), depends B02/B04.
**Code:** `d2a0a4eadab4ba99ae830c8e47013e60295a4632` on `codex/sorok-duel-b04-b05-a-semantic-interleave-20261112-r1`; B locks/rollback retained from `4a3c45c`; B start `15472ca`.
**Full relay handoff:** `../SOROK-DUEL-B04-R1/AGENT_A_SEMANTIC_INTERLEAVE_HANDOFF.md`; **B05 addendum:** `B05_A_SEMANTIC_ADDENDUM.md`; delta/impact: `PROGRAMMA_DELTA.json`, `impact.json`.

## FINDING

A real three-event P3 `BatchEngine` now crosses the B02 employment split with B02 `materialize_to` calls **between** events via the thin `PeriodInterleaveOwner` adapter: pre-batch to 2026-01-16; after event 4 to 2026-01-22 (crosses 2026-01-20); after event 5 to 2026-01-26; after event 6 to 2026-02-01. The reader shows the old term at 2026-01-19 and `civic-works` at 2026-01-21, with the split state. Then a typed parent purchase and household rent run; rent changes household cash 55→43 and flips B03 junior-kit feasibility to REFUSED_AFFORDABILITY; purchase stock/ownership changes; C02 parent work/read after purchase refuses `PARENT_MATERIAL_HISTORY_MISMATCH` (typed hook pending, no bridge); P3 head is unchanged by B04/B05. Period gaps are reported in `period_uncovered`; no elapsed psyche/work.

## EVIDENCE

- B05 rolling + rollback + post-split batch + cross-boundary + zero/held: 6 passed in 141.03s (`evidence/b05_a_semantic.log`).
- Combined 42 passed in 399.43s (`evidence/a_b04_b05_cross_combined.log`).
- P6 house/P2/actor 15 passed; P6 MII 18 passed.
- Cold, rent rollback, source severance/restore, duplicate rent, one-debit, cross-boundary materialization statuses.

## LIMITS

Three-event bounded batch, not five; no crash between a B02 materialize and the next P3 event; C02 typed purchase hook pending, so post-purchase parent work/read and second purchase refuse; no mother decision/utterance/uptake, public event/Nadia perception, arrears/landlord/variable rent/currency conversion, cold fork, full P6 live turn, native/science/rights/human/merge, or old P3 root compatibility. One independent nonauthor receiving remains required. Cost UNKNOWN.
