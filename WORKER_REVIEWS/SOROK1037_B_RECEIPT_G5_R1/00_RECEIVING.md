# SOROK #1037 B04/B05 receipt-proof repair — independent nonauthor G5 receiving

**Verdict:** `REVISE_EXACT_DEFECT` (not `ACCEPT_SCOPED`)
**Issue:** #1037
**Reviewer session:** `ses_e21caf5dfffeSywXGrQ6qw65oe`
**Independence:** fresh nonauthor session; neither original material author nor repair author `ses_e22146cc1ffeLXXJyO5aDi0REe`; no author conversation reused.
**Probed code:** `c7018020f002bb7f509a83fba0bf2a6a5955cc00`
**Branch:** `codex/sorok1037-b-receipt-g5-20261115-r1`
**Parent:** `fb061dec16c8386b9caa1b5ea75ec7645aff88a7`
**Grade:** `SOURCEFREE_S2_ONLY`
**Terminal:** STOP. No product fix, no protected merge, no native/science/human/J1 acceptance.

## 1. What was received

The frozen author candidate at `c7018020f002bb7f509a83fba0bf2a6a5955cc00` changes only the two established public readers plus the author's own return/tests/evidence:

| Path | Before (fb061dec and c724d1a8) | Probed after | Result |
|---|---|---|---|
| `WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py` | `7901b4fe80248c8ecb731440464454c799fa73b8` | `3c1d326bfa2f8a78c92a84e5cc5e039e04376441` | changed |
| `WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py` | `9500d80e85fba969f8e5fb8f3d233fc11f39c9d0` | `b944b8f0b6e0d700e85141256df01cdaef8d59e2` | changed |
| author test `SOROK1037_B_RECEIPT_REPAIR_R1/tests/test_b04_b05_receipt_provenance.py` | absent | `a28db531306b3ad4dcebc76915d079f14ac0ea0f` | 6 tests |
| `#1027` witness `g5_probe.py` | original `7cd5a23044426961d6f33e13b1ccf44f54916f81` | byte-identical copy | unmodified |
| `#1027` witness `g5_cold_probe.py` | original `6fc86dc5ca7ca8cc52baa8ad71ad33349d846cab` | byte-identical copy | unmodified |

The before product blobs equal both #996 head `fb061dec16c8386b9caa1b5ea75ec7645aff88a7` and composed cut `c724d1a89626f3e177acd004c0be20029dc7ade4`. No other product file changed. Full pins: `evidence/BLOB_PINS.json`; source delta: `evidence/source_delta_name_status.txt`.

The #1027 witness was copied byte-identically into this reviewer root so its `HERE.parents[1]` resolves to the repository root, then executed unmodified. Its git blob and sha256 were unchanged before and after execution:

```text
g5_probe_1027.py       blob 7cd5a23044426961d6f33e13b1ccf44f54916f81
                       sha256 da1d4389fdae9d092f3bb777777e5f5ea76a71fea943730ff6cf029e3414fa5a
g5_cold_probe_1027.py  blob 6fc86dc5ca7ca8cc52baa8ad71ad33349d846cab
                       sha256 f9cc6e56cf6899bea1b09c820b4b3dc0ad52a97b5864bc9121a34229dc1820aa
```

## 2. Environment and exact commands

Host: `oldMac.lan`, Darwin 22.6.0 x86_64, macOS 13.7.8, 16 GiB RAM; load average about 4.3 at receipt time. Actual Python `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python` 3.11.3; pytest 9.1.1. Every command used:

```text
TMPDIR="$PWD/.local-logs/sorok1037-b-receipt-g5/tmp"
PYTHONDONTWRITEBYTECODE=1
pytest -p no:cacheprovider
```

No provider, model, account, authentication, global-permission or server setting was changed. No hosted CI was used. Model checkpoint/organization/quota and provider token/USD cost are `UNOBSERVED`.

| # | Command (from checkout root) | Exit | Result | Real / max RSS |
|---|---|---|---|---|
| 1 | `python WORKER_REVIEWS/SOROK1037_B_RECEIPT_G5_R1/g5_probe_1027.py` | `1` literal | 63/63 raw checks pass; both `defects[].accepted=false`; typed refusals `PURCHASE_READ_PROVENANCE_MISMATCH`, `B05_RENT_PROVENANCE_MISMATCH` | 23.69 s / 62,550,016 B |
| 2 | `python WORKER_REVIEWS/SOROK1037_B_RECEIPT_G5_R1/g5_cold_probe_1027.py` | `0` | `ok=true`, `warm_ok=true`, `child_exit=0`; 2 purchases + 1 rent, fresh-process cold | 20.58 s / 59,281,408 B |
| 3 | `python -m pytest ... WORKER_RETURNS/SOROK1037_B_RECEIPT_REPAIR_R1/tests/test_b04_b05_receipt_provenance.py` | `0` | 6 passed | 86.27 s / 66,297,856 B |
| 4 | `python -m pytest ... <14 inherited B01-B05 test files>` | `0` | 43 passed | 580.65 s / 69,885,952 B |
| 5 | `python -m pytest ... WORKER_RETURNS/SOROK-DUEL-C02-C03-R2/A_RETURN_R3/test_c03_c04_consumer.py` | `0` | 3 passed; product read-only | 61.11 s / 72,028,160 B |
| 6 | `python WORKER_REVIEWS/SOROK1037_B_RECEIPT_G5_R1/g5_review_probe.py` | `2` own oracle | 33/34 checks pass; one failed check is the reproduced B05 sole-receipt false accept | 66.85 s / 50,266,112 B |

Raw stdout, stderr/time and reports are under `evidence/`. Module resolution was verified to this checkout only (`evidence/module_paths.txt`); no hot imports from another checkout.

### #1027 witness oracle caveat

The unmodified witness always appends the two historical defect rows to `REPORT["defects"]` and returns exit `1`, even when both attacks are refused. Its literal exit and its `verdict` field are therefore not the repaired result. I inspected `checks[].pass` and `defects[].accepted` directly:

- own run: `63` checks, `63` pass, `0` fail; `G5-B04-RECEIPT-FOREIGN-ROOT accepted=false`; `G5-B05-RENT-RECEIPT-FOREIGN-ROOT accepted=false`.
- the embedded historical `source_cause` text in those rows is also from the pre-repair oracle and is not a live finding for these two cases.

The original RED is author/#1027 evidence, not independently re-executed here by mutating product: the committed #1027 report at `dfd09434...` and the author's `red_hostile_report_1027.json` each show 61/63 with both defect rows `accepted=true`. This receiving did not alter product to recreate the before state.

## 3. G1-G5 result

| Gate | Status | Basis |
|---|---|---|
| G1 source/owner/custody | `PASS_SCOPED_SOURCEFREE` | exact HEAD/branch/parent; only B04/B05 product changed; before blobs match #996 and `c724d1a8`; exact witness/cold assets byte-identical; exclusive reviewer root; product read-only |
| G2 build/actual first consumers | `PASS_NORMAL_READERS_AND_COLD` | genuine two purchases (h1/h2) + one rent; warm readers and fresh-process cold; 6 author tests; 43 inherited; 3 selected C03/C04; unchanged writers/locks |
| G3 falsification | `FAIL_REVISE_EXACT_DEFECT` | both established #1023 foreign-root false accepts now refuse; own foreign root/branch/actor/exchange/period/rent/same-period second receipt controls refuse; B04 append-only chain forgery refused by C02 owner history; **B05 sole rehashed append-only rent receipt still returns `READ`** |
| G4 boundaries/preservation | `PARTIAL_PASS_PRESERVATION__SCOPED_OPERATION_BOUNDARY_FAILS` | no writer/schema/lock/currency/P2/C03/C04/P6/D03 change; no new ledger; historical genuine h1 still `historical=true`; changed/restored exact; but the required actual-rent operation authenticity boundary is not met |
| G5 independent receiving | `REVISE_EXACT_DEFECT` | one exact reproducible in-scope defect; not `ACCEPT_SCOPED` |

## 4. Mandatory residual adjudication — in-scope B05 failure

### Exact append-only witness

`g5_review_probe.py`, scenario `b05_sole_rehash`, on a fresh state:

1. Establish the B02 plan and materialize to `2026-07-01`; `period:2026-h1` is `COMPLETE`; no rent episode exists.
2. Read current B01 household/dwelling. Household cash is `55`; current monthly rent is `12`.
3. Build a fully shaped `SOROK_HOUSEHOLD_RENT_RECEIPT@1` `ADMITTED` receipt for the current root/branch, actor `A`, operation `g5review:b05:sole-rehashed`, period `period:2026-h1`, `period_status=COMPLETE`, `monthly_rent=12`, `household_cash_before=67`, `household_cash_after=55`, current household/dwelling sources, and material hashes consistent with the claimed before/after cash.
4. Append exactly one `P2_HOUSEHOLD_RENT` episode through the public `session.product.store.append_episode` API. No world rewrite, no checkpoint write, no privileged state edit.
5. Append changed no cash (`55 -> 55`). There was no prior actual rent operation and no debit.
6. `rolling_reproduction.read_household_obligation(session, op)` returned:

```json
{"status": "READ", "historical": false, "receipt_status": "ADMITTED",
 "household_cash": 55}
```

This is a false evidence/currentness acceptance: the reader asserts an admitted rent for a completed period and treats the current household state as its after-state, although no actual rent operation occurred. It is **not** a second debit.

### Why this is in scope

The #1037 B05 defect was not only “a second receipt must be rejected.” The contract says the reader must not accept a receipt “without proof that it is the one actual period rent operation” and requires “exact source/root/branch/actor/household/period/operation/receipt identity and uniqueness as applicable,” explicitly warning not to “merely check that hashes are self-consistent.” The repair adds root/branch/actor/period/source/rent checks and uniqueness among appended receipts. A sole forged receipt is trivially unique, so uniqueness does not establish the actual writer operation. The failure is reproducible with append-only evidence under the same public-store threat model as #1023, not only by a fully privileged world rewrite. It therefore cannot be waived as out of scope.

### B04 contrast

A chain-extending appended purchase with the correct session root/branch/actor/alias, recomputed self-consistent `purchase_source`, and a coherent ownership row but no actual parent debit is refused:

```text
PURCHASE_READ_PARENT_MISMATCH
```

The actual C02 parent-material owner history is the binding, not local hash consistency; stored parent cash and market source are unchanged. The author-disclosed fully privileged rewrite of parent material plus world/material facts is outside the observed append-only threat model and is not used here to condemn B04. A forged purchase sibling does cause fail-closed availability loss for genuine parent reads; that is not a false accept.

## 5. Historical, changed/restored, and cold status

- Genuine h1 rent remains readable with `historical=true` after a later h2 rent; h2 remains `historical=false`; household cash debits exactly twice.
- A genuine h1 rent after a lawful dwelling change is refused `B05_RENT_SOURCE_STALE`. This is the pre-existing dwelling-source binding, not a new false accept and not caused by the added current-rent check; exact stored-document restore returns the identical baseline. The contract does not require a superseded dwelling source to remain a current READ.
- B04 ownership row removed then exactly restored: `PURCHASE_READ_STALE`, then READ with the same owned source.
- #1027 witness independently re-ran market branch/root restore, household root/actor restore, dwelling change/restore, period replay and partial-ownership restore; all passed.
- Fresh-process cold: exact #1027 cold probe reopened two purchases and one rent, replayed/stale-refused/duplicate-refused without a second debit, and left the store head unchanged.

## 6. One precise owner repair instruction

**B05 owner (`rolling_reproduction.read_household_obligation`):** for an `ADMITTED` rent receipt, require proof of the actual `apply_household_rent` writer debit from the existing durable C12 state history, not merely uniqueness among appended receipts. Concretely, verify that the receipt’s `household_cash_before`/`household_cash_after`, `household_material_hash_after` (and clock/operation) correspond to the actual A-household-cash checkpoint transition written by the existing `_StoreWrite` + `_checkpoint` path for this branch, and refuse a typed `B05_RENT_OPERATION_UNPROVEN` (or existing equivalent) when no actual debit transition exists. A sole appended receipt for a completed period with no prior rent must refuse. Use the existing checkpoint/store evidence; do not add a new ledger or registry by default, and do not weaken any existing root/branch/actor/period/source/rent/uniqueness check. If the existing evidence is demonstrably insufficient, return a narrow owner ABI note rather than widening the receipt oracle.

## 7. Limitations and nonclaims

- The original before-repair RED was not independently re-executed by mutating product; it is author/#1027 evidence and was inspected in the committed reports.
- The B05 failure is false evidence/currentness acceptance, not a duplicate debit. No motive, desire, volition or psychological fact is inferred.
- No native science, actor/human authority, J1/Nadia G2 acceptance, protected PRE-MAIN merge, or new ledger/currency conversion is claimed.
- The B04 fully privileged rewrite residual is outside the observed append-only threat model; the B04 fail-closed availability loss is recorded, not accepted as a false read.
- Timings/RSS are observations under concurrent host load, not isolated benchmarks. Provider cost and checkpoint/org/quota are `UNOBSERVED`.
- The full P6/MII/J1 suites and unrelated 27-packet campaign were not run.

## 8. STOP

The candidate does not earn `ACCEPT_SCOPED@B01_B05_SOURCEFREE_c7018020f002bb7f509a83fba0bf2a6a5955cc00`. One exact in-scope B05 defect remains. Product is unchanged; this receiving stops here.
