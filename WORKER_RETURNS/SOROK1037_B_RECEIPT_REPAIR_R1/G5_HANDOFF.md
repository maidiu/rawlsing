# SOROK B04/B05 receipt-provenance repair — nonauthor G5 handoff

**Verdict for this author return:** `AUTHOR_CANDIDATE_FOR_G5`
**Scope:** the two established #1023 first-reader false accepts only.
**Start:** `fb061dec16c8386b9caa1b5ea75ec7645aff88a7`
**Branch:** `codex/sorok1037-b-receipt-repair-20261115-r1`
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, motive/volition, human acceptance, protected merge, or G5 claim.

A distinct nonauthor session must receive the exact implementation and test blobs below on identical code. Do not accept this author run as G5.

## Exact changed product source

```text
WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py
  before blob 7901b4fe80248c8ecb731440464454c799fa73b8
  after  blob 3c1d326bfa2f8a78c92a84e5cc5e039e04376441
  sha256 114f38e5303815d890188809309de56f2ff001d8fc8adb02243a6b1fc83d241a
WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py
  before blob 9500d80e85fba969f8e5fb8f3d233fc11f39c9d0
  after  blob b944b8f0b6e0d700e85141256df01cdaef8d59e2
  sha256 c22e1b3dd7de69d5bf7afa4b1309c0be6c9e72598b18a4a9f2e15c2260709778
```

The before blobs equal both #996 head `fb061dec` and composed code cut
`c724d1a89626f3e177acd004c0be20029dc7ade4`. No other product file is modified.

## Exact hostile asset custody

```text
#1027 g5_probe.py
  git blob 7cd5a23044426961d6f33e13b1ccf44f54916f81
  sha256   da1d4389fdae9d092f3bb777777e5f5ea76a71fea943730ff6cf029e3414fa5a
#1027 g5_cold_probe.py
  git blob 6fc86dc5ca7ca8cc52baa8ad71ad33349d846cab
  sha256   f9cc6e56cf6899bea1b09c820b4b3dc0ad52a97b5864bc9121a34229dc1820aa
```

Both files were extracted byte-identically from
`dfd09434ebbdb99971ac22a02533399c303ebbec` into this return root so their
`HERE.parents[1]` resolves to the repository root. They are unmodified.

## Reproduction commands

Run sequentially from the checkout root. Use the actual host Python.

```text
export TMPDIR="$PWD/.local-logs/sorok1037-b-receipt-repair/tmp"
export PYTHONDONTWRITEBYTECODE=1
PY=/private/tmp/rawlsing-oct28-p1r1/venv/bin/python
```

### 1. Exact #1027 witness (RED at start, GREEN after repair)

```text
/usr/bin/time -l "$PY" WORKER_RETURNS/SOROK1037_B_RECEIPT_REPAIR_R1/g5_probe.py
```

At the frozen start: 63 checks, 61 PASS, two FAIL, both forged receipts
`accepted:true` (`READ`). After repair: 63 checks, 63 PASS, both forged
receipts `accepted:false` with `PURCHASE_READ_PROVENANCE_MISMATCH` and
`B05_RENT_PROVENANCE_MISMATCH`.

**Oracle caveat:** this witness always appends the two historical defect rows
to `REPORT["defects"]` and returns exit 1, even when both attacks are refused.
Grade GREEN from `checks[].pass == true` and `defects[].accepted == false`,
not from its terminal exit code or `verdict` field.

### 2. Author provenance tests

```text
"$PY" -m pytest -p no:cacheprovider -q \
  WORKER_RETURNS/SOROK1037_B_RECEIPT_REPAIR_R1/tests/test_b04_b05_receipt_provenance.py
```

### 3. Normal two purchases + one rent, fresh-process cold

```text
/usr/bin/time -l "$PY" WORKER_RETURNS/SOROK1037_B_RECEIPT_REPAIR_R1/g5_cold_probe.py
```

### 4. Inherited original B01–B05 43 tests

```text
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

### 5. Selected read-only C03/C04 normal consumer regression

```text
"$PY" -m pytest -p no:cacheprovider -q \
  WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/A_RETURN_R3/test_c03_c04_consumer.py
```

This is a regression only; no C03/C04/parent-decision product file was edited.

## Repair semantics

**B04 `read_purchase`**
- Requires exactly one matching purchase episode for `(parent alias, operation_id)`.
- Requires episode/body and nested receipt `schema`, `grade`, `root`, `branch`,
  `actor_id`/`parent_id`, `parent_alias`, `operation_id`, `buyer`, `status`, and
  `clock` to bind to the current session and requested parent/operation.
- Recomputes the `purchase_source` digest and requires equality with the
  receipt and the ownership acquisition row.
- Requires `owner_actor_id` to be the fixed-A holder or the registered parent.
- For `ADMITTED` receipts, requires the actual C02 parent-material/history read
  to succeed, so the receipt must be the purchase operation accepted by the
  existing C02 owner chain; otherwise refuses
  `PURCHASE_READ_PARENT_MISMATCH`.

**B05 `read_household_obligation`**
- Requires episode actor `A` and body/receipt `schema`, `grade`, `root`,
  `branch`, `operation_id`, `status`, and `clock` to bind to the current
  session and requested operation.
- Preserves the existing household/dwelling source, material-hash, cash
  arithmetic, and current-cash checks.
- Requires the receipt period to be a text B02 period whose current progress is
  `COMPLETE`, and requires the receipt to be the unique rent receipt for that
  period in the branch; a second same-period receipt refuses
  `B05_RENT_OPERATION_NOT_UNIQUE`.
- Requires the receipt rent to equal the current dwelling monthly rent.

No writer, ledger, currency conversion, lock, P2 fact, P3/P6 state, C03/C04,
parent-decision, or D03 path was changed.

## Known weaknesses / receiving notes

1. **B05 sole-receipt rehash for a completed period.** A fully rehashed rent
   receipt with correct current root/branch/actor/operation/sources/cash
   arithmetic, for a completed period that has no prior actual rent receipt,
   can still be presented as the unique period receipt. Read-side checks cannot
   prove a debit happened without a writer-side authenticated operation
   registry or cash ledger; adding one is outside this repair and would violate
   the no-new-ledger constraint. The established #1023 defect (a second rent
   receipt for an already-recorded period) is refused.
2. **B04 depends on the C02 parent-history owner chain.** A fully rewritten,
   internally consistent parent material history plus market/owned state could
   in principle be made consistent. Appending a forged sibling purchase episode
   fails closed and also makes genuine parent-material reads refuse until the
   forged episode is removed; this is availability loss, not false acceptance.
3. **Historical reads remain readable.** A genuine earlier purchase/rent whose
   after-sources are superseded still returns `READ` with `historical=true`.
   The repair binds provenance/operation identity, not currentness.
4. **Scoped grade only.** Sourcefree engineering; no native/human/scientific
   acceptance, no motive/volition inference, no protected PRE-MAIN merge, no
   J1/Nadia G2 claim.
5. **Host contention.** Other independent jobs were active on `oldMac.lan`;
   elapsed/RSS are observations, not isolated benchmarks. Provider token/USD
   cost is `UNOBSERVED`.

## Reviewer acceptance target

`ACCEPT_SCOPED@B01_B05_SOURCEFREE_<40-hex>` only if the distinct nonauthor
reproduces both forged refusals, normal two-purchase/one-rent first reader +
cold, the original 43, and the selected read-only C03/C04 consumer regression
on exactly these blobs.
