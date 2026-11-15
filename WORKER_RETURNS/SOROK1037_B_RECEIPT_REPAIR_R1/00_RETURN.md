# SOROK #1037 B04/B05 receipt-proof repair — author return

**Verdict:** `AUTHOR_CANDIDATE_FOR_G5` (not self-G5)
**Issue:** #1037
**Session:** `ses_e22146cc1ffeLXXJyO5aDi0REe`
**Start:** `fb061dec16c8386b9caa1b5ea75ec7645aff88a7`
**Branch:** `codex/sorok1037-b-receipt-repair-20261115-r1`
**Grade:** `SOURCEFREE_S2_ONLY`
**Terminal:** STOP; no next job launched.

## Scope

Repaired only the two established #1023 public-reader false accepts:

- B04 `read_purchase` accepted a forged appended `ADMITTED`
  `P2_PARENT_PURCHASE` receipt with foreign nested `root`/`branch` and a
  coherent ownership row.
- B05 `read_household_obligation` accepted a forged appended `ADMITTED`
  `P2_HOUSEHOLD_RENT` receipt with foreign nested `root`/`branch`, coherent
  cash arithmetic and no second debit.

No writer, ledger, schema, lock, currency conversion, C03/C04/P6/D03, or
protected PRE-MAIN file was changed.

## Exact changed source

```text
WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py
  7901b4fe80248c8ecb731440464454c799fa73b8 -> 3c1d326bfa2f8a78c92a84e5cc5e039e04376441
  sha256 114f38e5303815d890188809309de56f2ff001d8fc8adb02243a6b1fc83d241a
WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py
  9500d80e85fba969f8e5fb8f3d233fc11f39c9d0 -> b944b8f0b6e0d700e85141256df01cdaef8d59e2
  sha256 c22e1b3dd7de69d5bf7afa4b1309c0be6c9e72598b18a4a9f2e15c2260709778
```

The before blobs equal #996 `fb061dec` and composed cut `c724d1a8`.

## Repair

**B04** now requires the episode/body/receipt `schema`, `grade`, `root`,
`branch`, `parent_id`/`actor_id`, `parent_alias`, `operation_id`, buyer,
status and clock to bind to the current session, requested parent and exact
operation; recomputes `purchase_source`; binds owner to holder-or-parent; and
for `ADMITTED` reads requires the existing C02 parent-material history owner
chain to validate the receipt.

**B05** now requires episode actor `A` and body/receipt root, branch,
operation, status and clock binding; preserves all source/hash/cash checks;
requires the receipt rent to equal the current dwelling rent and the period to
be a text B02 period currently `COMPLETE`; and requires the receipt to be the
unique rent receipt for that period. A second same-period receipt refuses
`B05_RENT_OPERATION_NOT_UNIQUE`.

## Evidence

- Exact #1027 witness: RED 63 checks / 2 failed / both forged receipts
  `accepted:true`; GREEN 63/63 PASS / both `accepted:false` with typed
  refusals. The unmodified witness always appends its historical defect rows
  and exits 1, so GREEN is the per-check pass plus `accepted:false`, not the
  terminal exit or verdict field.
- Author provenance tests: 6 passed.
- Normal two purchases (2026-h1, 2026-h2) + one rent, warm first readers and
  fresh-process cold: exit 0, no duplicate debit, P3 head unchanged.
- Original 43 B01–B05 tests: 43 passed before repair and 43 passed after
  repair.
- Selected read-only C03/C04 normal consumer regression: 3 passed, no product
  edit.
- Full commands, raw logs, time/RSS, blob and log hashes: `EVIDENCE.json`,
  `evidence/`, `G5_HANDOFF.md`.

## Limits / known weaknesses

- B05 cannot detect a fully rehashed *sole* rent receipt for an already
  completed period with no prior actual rent without a writer-side
  authenticated operation registry/cash ledger; adding one is outside this
  narrow repair.
- B04 operation authenticity relies on the existing C02 parent-history chain;
  a forged sibling episode fails closed and can temporarily make genuine
  parent reads refuse.
- Historical genuine receipts remain readable with `historical=true`.
- Host was under concurrent independent load; timings/RSS are observations.
- Provider token/USD cost and checkpoint/quota are `UNOBSERVED`.

## Holds

- RULE_A: no native/human authority.
- T: no motive/volition inference.
- NO_CHANGE: P2 writers, C03/C04, P6, D03, protected PRE-MAIN untouched; no new
  engine/ledger/currency conversion.
- No protected merge. Distinct nonauthor G5 still required.

## STOP

One narrow repair complete. HQ may publish the frozen author candidate; a
separate nonauthor reviewer must run the exact reproduction in
`G5_HANDOFF.md` before any `ACCEPT_SCOPED` claim.
