# #1023 runnable defect witness — forged receipt provenance at B04/B05 readers

**Verdict:** `REVISE_EXACT_DEFECT`
**Reviewer:** `ses_e28ef72f9ffelBx7qet6BAina3`
**Tested cut:** B `1161e5f74081888bd813825b3df4afab3e2f5ca7`, composed code
`c724d1a89626f3e177acd004c0be20029dc7ade4`, documentary
`fb061dec16c8386b9caa1b5ea75ec7645aff88a7`.
**Product code was not edited.**

## Run

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  WORKER_REVIEWS/SOROK1023_MATERIAL_WORLD_G5_R1/g5_probe.py
```

Observed: `TRUE_EXIT=1`; 63 checks; two failures; report at
`evidence/hostile_report.json` and `evidence/g5_probe_run.log`.

## Defect 1 — B04 `read_purchase` accepts a foreign-root receipt

**First reader:** `WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py:646`
(`read_purchase`). The acquisition checks are at lines 661–672. The reader
never compares the nested `receipt["root"]`, `receipt["branch"]`, or
`receipt["parent_id"]` with the current session.

**Actual input:** the witness builds a real parent/market/dwelling state, makes
one real admitted purchase, then appends a second `P2_PARENT_PURCHASE` episode
through the existing C12 store API
(`session.product.store.append_episode`) with:

- a coherent `p6_owned_objects` row and recomputed `purchase_source`;
- nested receipt `root = "f"*64`, `branch = "foreign-branch"`;
- no corresponding B04 material operation.

**Expected:** typed refusal (the same root/branch mismatch that C02
`parent_activity.py:363-364` already refuses as
`PARENT_MATERIAL_HISTORY_MISMATCH`).

**Actual:** `read_purchase` returns `status = READ`, accepting the forged
`ADMITTED` receipt.

**Smallest suggested owner fix (not applied):** in B04 `read_purchase`, require
`receipt["root"] == session.read_root()["root_hash"]`,
`receipt["branch"] == session.branch_id`, and
`receipt["parent_id"] == parent_id` before returning a read.

## Defect 2 — B05 `read_household_obligation` accepts a foreign-root rent receipt

**First reader:** `WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py:376`
(`read_household_obligation`). Lines 386–406 check the stable household/dwelling
sources and rent arithmetic, but not the receipt's root/branch, and do not
require the receipt to be the unique actual rent operation for its period.

**Actual input:** a real admitted rent exists; the witness appends a second
`P2_HOUSEHOLD_RENT` episode through the existing C12 store API with:

- nested receipt `root = "e"*64`, `branch = "foreign-branch"`;
- `monthly_rent = 12`;
- `household_cash_before = current_cash + 12`,
  `household_cash_after = current_cash`.

**Expected:** typed refusal binding the receipt to the current session and the
actual rent operation.

**Actual:** `read_household_obligation` returns `status = READ` for the forged
`ADMITTED` rent receipt. Household cash itself is unchanged, so this is false
evidence acceptance, not a second debit.

**Smallest suggested owner fix (not applied):** in B05
`read_household_obligation`, require the receipt root/branch to equal the
current root/branch and bind the operation to the single actual rent receipt
for that period.

## Why this is not a duplicate of the passing cases

The original 43 tests and this witness's other 61 checks cover the normal
purchase/rent path, refusals, duplicate replay, partial ownership removal,
wrong currency, unknown acoustics, tenancy, root/actor material tampering,
period boundaries, changed/restored feasibility, and cold-after-failure. Those
all pass. The two failures are specifically nested receipt provenance at the
two public read APIs, which the original B suite does not exercise.
