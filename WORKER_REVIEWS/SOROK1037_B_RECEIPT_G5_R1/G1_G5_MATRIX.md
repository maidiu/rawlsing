# G1-G5 matrix — SOROK #1037 B04/B05 repair receiving

**Verdict:** `REVISE_EXACT_DEFECT`
**Probed code:** `c7018020f002bb7f509a83fba0bf2a6a5955cc00`
**Reviewer:** `ses_e21caf5dfffeSywXGrQ6qw65oe` (fresh nonauthor)

| Gate | Status | Evidence | Limiting condition |
|---|---|---|---|
| G1 source/owner/custody | PASS_SCOPED_SOURCEFREE | exact branch/parent/code; only B04/B05 product changed; before blobs equal #996 and `c724d1a8`; exact witness/cold assets byte-identical and unmodified; exclusive reviewer root; no hot imports; product read-only | before-state RED is author/#1027 evidence, not re-executed by mutating product |
| G2 build/first consumers | PASS_NORMAL_READERS_AND_COLD | genuine two purchases h1/h2 + one rent warm and fresh-process cold; no duplicate debit; head unchanged; 6 author tests; 43 inherited; 3 selected C03/C04 | no full P6/MII/J1 suite; timings under load |
| G3 falsification | FAIL_REVISE_EXACT_DEFECT | exact #1027 witness 63/63 raw checks, both foreign-root defects refused; own B04/B05 root/branch/actor/exchange/period/rent/second-receipt controls pass; B04 append-only chain forgery refused by C02 owner history | **B05 sole fully rehashed appended rent receipt for a completed period with no prior actual rent returns `READ` (historical=false), cash unchanged** |
| G4 boundaries/preservation | PARTIAL_PASS_PRESERVATION__SCOPED_OPERATION_BOUNDARY_FAILS | no writer/schema/lock/currency/P2/C03/C04/P6/D03 change; no new ledger; historical h1 `historical=true`; changed/restored exact; cold unchanged | required actual-rent operation authenticity not met; B04 privileged world-rewrite residual outside append-only threat model; B04 fail-closed availability loss noted |
| G5 independent receiving | REVISE_EXACT_DEFECT | one exact append-only in-scope B05 false accept reproduced with existing public reader | not `ACCEPT_SCOPED`; no protected merge |

## Exact RED witness

`g5_review_probe.py` / `b05_sole_rehash`:

- State: B02 plan materialized to `2026-07-01`; `period:2026-h1` `COMPLETE`; no rent episode.
- Append one `P2_HOUSEHOLD_RENT` episode with `session.product.store.append_episode` only.
- Receipt: `ADMITTED`, current root/branch/actor `A`, operation `g5review:b05:sole-rehashed`, period h1, rent 12, current household/dwelling sources, cash before 67 / after 55, coherent material hashes.
- Observed: `{"status":"READ","historical":false,"receipt_status":"ADMITTED","household_cash":55}`.
- Cash before append 55, after append 55; no debit, no prior actual rent.

This is false evidence/currentness acceptance, not a duplicate debit. It is in scope because #1037 requires proof that the receipt is the one actual period rent operation, not merely local hash consistency or uniqueness among appended receipts.

## Owner repair (one)

Bind `ADMITTED` B05 rents to the actual `apply_household_rent` debit in existing durable C12 checkpoint/state history (A cash before/after, after household material hash, clock and operation); refuse `B05_RENT_OPERATION_UNPROVEN` or equivalent if no actual debit transition exists. A sole appended receipt must refuse. Use existing checkpoint/store evidence; do not add a new ledger by default and do not weaken existing checks.

## Nonclaims

No native science, human/actor authority, J1/Nadia G2 acceptance, motive/volition result, protected merge, new ledger, or isolated performance/cost claim. Provider cost and checkpoint/org/quota `UNOBSERVED`.
