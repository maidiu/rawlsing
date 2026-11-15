# SOROK #1037 B05 zero-status repair R3 — G5 handoff

**Candidate:** the commit containing this return on
`codex/sorok1037-b05-zero-status-repair-20261115-r3`
**Base / reviewed code:** `270eb29cd4487b6865b61adc9d671952554d425d`
**Adverse review:** `6dc921841a748ee7121887c0484068249a526b17` / PR #1069
**Author session:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Required receiver:** the same independent nonauthor
`ses_e21caf5dfffeSywXGrQ6qw65oe` in its separate checkout. The author cannot
self-G5.

## Frozen implementation cut

```text
WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py
  before R3  a193fb5bfb6a1955209bedf0e66be974dcfa8e1b
  R3 blob    9de3b5a295431fac2b0f9833ed520262df04b363
  sha256     bb67d3e03baf28943076cf5902e308c26ccbb7678672a297817a358a6296c774
B04 preserved blob 3c1d326bfa2f8a78c92a84e5cc5e039e04376441
```

The change is read-side only: `ADMITTED` requires `monthly_rent > 0`,
`household_cash_after < household_cash_before`, and exact debit
`before_cash - rent == after_cash`, on top of the accepted R2 adjacent durable
checkpoint transition. Zero/non-decreasing `ADMITTED` refuses
`B05_RENT_RECEIPT_INVALID`. Genuine `UNCHANGED` zero and `REFUSED` held rent
keep `before_cash == after_cash` and remain readable. No writer/schema/store/
lock/ledger/key/currency change.

## Exact receiving commands

Use your own scratch, `PYTHONDONTWRITEBYTECODE=1`, `pytest -p no:cacheprovider`,
and the authorized Python:

```text
PY=/private/tmp/rawlsing-oct28-p1r1/venv/bin/python
```

From the frozen checkout root:

1. Confirm pins:

```text
git rev-parse HEAD
git hash-object WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py
git hash-object WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py
git hash-object WORKER_RETURNS/SOROK1037_B05_ZERO_STATUS_REPAIR_R3/g5_r2_focused_probe.py
git hash-object WORKER_RETURNS/SOROK1037_B05_ZERO_STATUS_REPAIR_R3/g5_review_probe.py
git hash-object WORKER_RETURNS/SOROK1037_B05_ZERO_STATUS_REPAIR_R3/g5_probe_1027.py
git hash-object WORKER_RETURNS/SOROK1037_B05_ZERO_STATUS_REPAIR_R3/g5_cold_probe_1027.py
```

Expected: B05 `9de3b5a2...`, B04 `3c1d326b...`, focused probe `d5d41240...`,
positive/control probe `3e98929d...`, #1027 witness `7cd5a230...`, cold probe
`6fc86dc5...`.

2. Rerun the unchanged frozen zero probe:

```text
"$PY" WORKER_RETURNS/SOROK1037_B05_ZERO_STATUS_REPAIR_R3/g5_r2_focused_probe.py
```

Expected: literal exit `0`; 17/17; the forged `ADMITTED` zero-rent receipt is
refused `B05_RENT_RECEIPT_INVALID`. The author RED at the same probe blob is
`evidence/red_g5_r2_focused_probe_report.json` (exit `2`, 16/17, one failure).
No product mutation is needed to reproduce RED; the immutable reviewer report
is `evidence/reviewer_g5_r2_focused_probe_report.json`
(sha256 `f941df69...`).

3. Rerun the original positive-forgery/normal-hostile probe:

```text
"$PY" WORKER_RETURNS/SOROK1037_B05_ZERO_STATUS_REPAIR_R3/g5_review_probe.py
```

Expected: exit `0`; 34/34; sole positive rehash refuses
`B05_RENT_OPERATION_UNPROVEN`; B04 controls pass.

4. Rerun the exact #1027 63-control witness:

```text
"$PY" WORKER_RETURNS/SOROK1037_B05_ZERO_STATUS_REPAIR_R3/g5_probe_1027.py
```

Expected: literal exit `1` historical oracle quirk; 63/63 checks; both defect
rows `accepted=false`.

5. Rerun the exact #1027 cold probe:

```text
"$PY" WORKER_RETURNS/SOROK1037_B05_ZERO_STATUS_REPAIR_R3/g5_cold_probe_1027.py
```

Expected: exit `0`; `ok=true`, `warm_ok=true`, `child_exit=0`; two purchases +
one rent; head unchanged.

6. Rerun focused, regression, inherited and selected consumer tests:

```text
"$PY" -m pytest -p no:cacheprovider -q \
  WORKER_RETURNS/SOROK1037_B05_ZERO_STATUS_REPAIR_R3/tests/test_b05_zero_status_semantics.py
"$PY" -m pytest -p no:cacheprovider -q \
  WORKER_RETURNS/SOROK1037_B05_WRITER_PROOF_REPAIR_R2/tests/test_b05_actual_rent_transition.py
"$PY" -m pytest -p no:cacheprovider -q \
  WORKER_RETURNS/SOROK1037_B_RECEIPT_REPAIR_R1/tests/test_b04_b05_receipt_provenance.py
"$PY" -m pytest -p no:cacheprovider -q \
  WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/A_RETURN_R3/test_c03_c04_consumer.py
"$PY" -m pytest -p no:cacheprovider -q \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_fork_provenance.py \
  WORKER_RETURNS/SOROK-DUEL-B02-R1/test_b02_period.py \
  WORKER_RETURNS/SOROK-DUEL-B02-R1/test_b02_incremental.py \
  WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_dwelling.py \
  WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_same_root_psyche.py \
  WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_operations.py \
  WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_composition.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_rolling.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_rollback.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_batch_cycle.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_cross_batch.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_zero_and_held.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_interleave_retry.py
```

Expected: `4 passed`, `5 passed`, `6 passed`, `3 passed`, `43 passed`.

## Adversarial checks to inspect

- Public zero-rent dwelling + two public `session.product.say` no-cash
  checkpoints + sole appended `ADMITTED` rent 0 cash 55/55: must refuse.
- Positive forged receipt with same no-cash checkpoints: must remain
  `B05_RENT_OPERATION_UNPROVEN`.
- Genuine positive rent, genuine zero `UNCHANGED`, held `REFUSED`: all read.
- h1 historical after h2, replay/retry, changed/restored checkpoint pair,
  sibling transition copy, B04 purchase and cold reopen: preserved.
- #1027 foreign-root B04/B05 defects: refuse.

## Verdict options

- `ACCEPT_SCOPED@B05_SOURCEFREE_<frozen 40-hex SHA>` if the frozen zero probe is
  17/17, the positive probe 34/34, #1027 63/63 with both defects false, cold
  passes, and no new false accept is found.
- `REVISE_EXACT_DEFECT` only for a new exact reproducible in-scope defect.
- `HOLD_OWNER` if the existing durable evidence cannot be executed as described.

Return exact commands, exit codes, blob pins, logs, timings/RSS and a verdict.
Do not mutate the candidate, launch a new repair round, or claim native/science/
human/J1/protected acceptance.
