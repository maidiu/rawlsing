# SOROK #1037 B05 writer-proof repair R2 — G5 handoff

**Candidate:** the commit containing this return on
`codex/sorok1037-b05-writer-proof-repair-20261115-r2`
**Base:** `c7018020f002bb7f509a83fba0bf2a6a5955cc00`
**Grade:** `SOURCEFREE_S2_ONLY`
**Author session:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Required receiver:** the same independent nonauthor (`ses_e21caf5dfffeSywXGrQ6qw65oe`)
or an equally independent fresh nonauthor. The author cannot self-G5.

## What is being received

One minimal read-side correction in
`WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py`:

```text
reviewed blob  b944b8f0b6e0d700e85141256df01cdaef8d59e2
candidate blob a193fb5bfb6a1955209bedf0e66be974dcfa8e1b
sha256         5ac75cb66c61fb120f56900e976a8cdcd4e153fd4b0d37d9a93a0c95ab578331
```

`B04` is byte-identical to the reviewed candidate:
`3c1d326bfa2f8a78c92a84e5cc5e039e04376441`.

`ADMITTED` rent reads now require the actual existing
`apply_household_rent` `_StoreWrite` + `_checkpoint` A-household-cash/material
transition at the receipt/episode clock. Missing or ambiguous proof refuses
`B05_RENT_OPERATION_UNPROVEN`. `UNCHANGED`/`REFUSED` zero/held rents remain
readable without a debit checkpoint. No writer/ABI/store/lock/schema change.

## Exact receiving commands

Use the existing Python and scratch discipline:

```text
TMPDIR=<your own scratch>/tmp
PYTHONDONTWRITEBYTECODE=1
PY=/private/tmp/rawlsing-oct28-p1r1/venv/bin/python
pytest -p no:cacheprovider
```

From the frozen checkout root:

1. Confirm the frozen source pins:

```text
git rev-parse HEAD
git hash-object WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py
git hash-object WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py
git hash-object WORKER_RETURNS/SOROK1037_B05_WRITER_PROOF_REPAIR_R2/g5_review_probe.py
git hash-object WORKER_RETURNS/SOROK1037_B05_WRITER_PROOF_REPAIR_R2/g5_probe_1027.py
git hash-object WORKER_RETURNS/SOROK1037_B05_WRITER_PROOF_REPAIR_R2/g5_cold_probe_1027.py
```

Expected: B05 `a193fb5...`, B04 `3c1d326...`, review probe `3e98929...`,
#1027 witness `7cd5a23...`, cold probe `6fc86dc...`.

2. Rerun the unchanged frozen reviewer probe:

```text
"$PY" WORKER_RETURNS/SOROK1037_B05_WRITER_PROOF_REPAIR_R2/g5_review_probe.py
```

Expected: literal exit `0`; `34/34` checks pass; no residual; the sole
rehashed receipt is refused `B05_RENT_OPERATION_UNPROVEN`. The author's RED
report at the same probe blob is `evidence/red_g5_review_probe_report.json`
(exit `2`, 33/34, one failure). No product mutation is needed to reproduce RED:
the frozen probe and its RED report are the unchanged reviewer witness.

3. Rerun the exact #1027 hostile witness:

```text
"$PY" WORKER_RETURNS/SOROK1037_B05_WRITER_PROOF_REPAIR_R2/g5_probe_1027.py
```

Expected: literal exit `1` (historical oracle quirk); `63/63` checks pass; both
defects `accepted=false` with `PURCHASE_READ_PROVENANCE_MISMATCH` and
`B05_RENT_PROVENANCE_MISMATCH`.

4. Rerun the exact #1027 cold probe:

```text
"$PY" WORKER_RETURNS/SOROK1037_B05_WRITER_PROOF_REPAIR_R2/g5_cold_probe_1027.py
```

Expected: exit `0`; `ok=true`; `warm_ok=true`; two purchases + one rent; head
unchanged.

5. Rerun focused and inherited tests:

```text
"$PY" -m pytest -p no:cacheprovider -q \
  WORKER_RETURNS/SOROK1037_B05_WRITER_PROOF_REPAIR_R2/tests/test_b05_actual_rent_transition.py
"$PY" -m pytest -p no:cacheprovider -q \
  WORKER_RETURNS/SOROK1037_B_RECEIPT_REPAIR_R1/tests/test_b04_b05_receipt_provenance.py
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
"$PY" -m pytest -p no:cacheprovider -q \
  WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/A_RETURN_R3/test_c03_c04_consumer.py
```

Expected: `5 passed`, `6 passed`, `43 passed`, `3 passed`.

## Focused adversarial checks to inspect

The new tests and probe cover:

- sole caller-rehashed `ADMITTED` receipt with correct current root/branch,
  actor `A`, operation, period, rent, before/after cash and self-consistent
  material hashes, appended with **no** checkpoint transition: refuse;
- actual transition hidden (severed) then exactly restored: refuse then exact
  baseline READ;
- forged sibling copying a real transition for another completed period:
  both ambiguous receipts refuse (fail-closed, not a false accept);
- genuine zero (`UNCHANGED`) and held (`REFUSED`): READ without a debit
  checkpoint;
- genuine h1/h2 historical flags, replay, and once-per-period retry.

## Verdict options

- `ACCEPT_SCOPED@B01_B05_SOURCEFREE_<frozen 40-hex SHA>` if the frozen probe is
  34/34, both #1027 defects refuse, all suites pass, and no new false accept is
  found.
- `REVISE_EXACT_DEFECT` only for a new exact reproducible in-scope defect.
- `HOLD_SOURCE_OWNER` if the existing durable evidence cannot be executed as
  described.

Return the exact commands, exit codes, blob pins, logs, timings/RSS, and a
verdict. Do not mutate the candidate, do not open a new repair round, and do
not treat this handoff as native/science/human/J1/protected acceptance.
