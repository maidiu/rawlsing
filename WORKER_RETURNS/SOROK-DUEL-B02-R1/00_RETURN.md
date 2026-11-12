# SOROK B02 Agent B return

**Task:** B02 `Map historical calendar/as-of to existing P3/S46 logical clock and split periods` (CG-B).
**Grade:** `SOURCEFREE_S2_ONLY`; no native/science/actor/human/rights/merge authority.
**Branch:** `codex/sorok-duel-b03-counter-b02-b-20261112-r1`.
**Implementation SHA:** `509784c2850c499d1f640c9f43c569416081d76d`.
**Start/frozen A result:** `5bc29474e769b928d9264f1607bab605e2b1c7e9`.
**B02 ABI:** `B02_ABI.md`; complete return: `AGENT_B_HANDOFF.md`; machine records: `PROGRAMMA_DELTA.json`, `impact.json`.
**Main relay handoff:** `WORKER_RETURNS/SOROK-DUEL-B03-R1/AGENT_B_HANDOFF.md`.

## FINDING

B02 was unbuilt and blocked C02/D02. One bounded historical period adapter now uses the existing S46 producer and P2 material writer: two dated periods, an explicit Gregorian-date → S46 tick mapping, a midperiod employment change split at the exact date, an employment-as-of reader, and the actual S46 interval state. A retry or cold replay reuses the exact interval state IDs and appends no duplicate period.

## ACTION

Added `p6_employment` and `p6_historical_period` to the P2 material-slot allowlist and the `historical_period` module. B01/B03 production behavior is unchanged. Added the same-root B03 PsycheStore negative test to close A's strongest B03 evidence gap; no B03 production change.

## EVIDENCE

- B02: **7 passed in 50.13s** (`evidence/b02_period.log`).
- B01 + B03 + B03 same-root + B02: **27 passed in 165.75s** (`evidence/b01_b02_b03_combined.log`).
- P6 house + adjacent: **17 passed in 217.45s** (`evidence/p6_adjacent.log`).
- P6 MII: **18 passed in 242.53s** (`evidence/p6_mii.log`).
- B03 same-root PsycheStore negative: **1 passed in 7.18s** (`SOROK-DUEL-B03-R1/evidence/b03_same_root_psyche.log`).

## LIMITS

P3 code-pin roots from all prior cuts are incompatible; fresh final-code roots only. B02 is a period/clock adapter, not a full P3 DevelopmentOwner cycle or daily work/care. S46 intervals are `SCHEDULED_ONLY/NOT_PERFORMED`. No purchase/debit/recurring cost, mother action/utterance, possession, trait, native science, or protected merge. Partial-crash atomicity remains B04/E03. Fork interval state is unavailable; materialization on a fork is refused. Plan/employment are one-shot at the anchor clock. The two Library architecture sources remain NOT_INSPECTED locally.
