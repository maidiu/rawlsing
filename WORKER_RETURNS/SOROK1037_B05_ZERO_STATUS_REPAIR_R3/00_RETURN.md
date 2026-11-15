# SOROK #1037 B05 zero-status repair R3 — author return

**Engineering verdict:** `AUTHOR_CANDIDATE_FOR_SAME_NONAUTHOR_FOCUSED_RERECEIVING`
**Scientific verdict:** `HELD`
**Authority verdict:** `HELD`
**Issue:** #1037 (fresh authorization comment `6901893989`)
**Author session:** `ses_e21a481bfffefyvpxaeFaAOFvQ` (same R2 author)
**Base / reviewed code:** `270eb29cd4487b6865b61adc9d671952554d425d`
**Branch:** `codex/sorok1037-b05-zero-status-repair-20261115-r3`
**Adverse review:** `6dc921841a748ee7121887c0484068249a526b17` / PR #1069, `REVISE_EXACT_DEFECT`
**Grade:** `SOURCEFREE_S2_ONLY`
**Terminal:** STOP. No R4 launched.

## Exact received defect

The R2 checkpoint proof authenticated any adjacent same-clock checkpoint pair.
With legitimate zero-rent dwelling conditions, two ordinary public
`session.product.say` actions create same-clock no-cash checkpoints. A sole
appended `ADMITTED` `monthly_rent=0` receipt, cash `55 -> 55`, matching those
public hashes, was returned `READ historical=false`; the actual zero-rent writer
returns `UNCHANGED`. This is false operation evidence, not a second debit.

## Single correction

Only `WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py` changed:

```text
before R3  a193fb5bfb6a1955209bedf0e66be974dcfa8e1b
after R3   9de3b5a295431fac2b0f9833ed520262df04b363
sha256     bb67d3e03baf28943076cf5902e308c26ccbb7678672a297817a358a6296c774
diff       10 insertions, 6 deletions; read-side status validation only
```

For `ADMITTED`, the reader now requires `monthly_rent > 0`,
`household_cash_after < household_cash_before`, and the exact debit
`before_cash - rent == after_cash`, in addition to the accepted R2 adjacent
durable-checkpoint proof. A zero or non-decreasing `ADMITTED` receipt refuses
`B05_RENT_RECEIPT_INVALID`. `UNCHANGED` and `REFUSED` keep their existing
`before_cash == after_cash` semantics and remain readable without a debit
checkpoint. The same status rule is used by the existing `_rent_chain` replay
validator; no writer, schema, store, lock, ledger, key or currency changed.
B04 is byte-identical at `3c1d326bfa2f8a78c92a84e5cc5e039e04376441`.

## Exact RED -> GREEN

The frozen reviewer probe was extracted byte-identically
(`blob d5d41240d32170ab0f2bed292afa747662283287`, sha256 `0300e8dd...`).
No harness adapter was needed: the own return is two path levels deep, matching
the reviewer root's `HERE.parents[1]` checkout resolution.

| Run | Source | Exit | Checks | Result |
|---|---|---|---|---|
| RED | unchanged `270eb29`/`a193fb5b` | `2` | 16/17 | forged ADMITTED zero rent accepted `READ` |
| GREEN | R3 `9de3b5a2` | `0` | 17/17 | zero forgery refused `B05_RENT_RECEIPT_INVALID` |

The immutable reviewer report is preserved byte-identically at
`evidence/reviewer_g5_r2_focused_probe_report.json`
(sha256 `f941df69...`).

## Final-source runs (each once; not summed)

| Consumer / control | Result |
|---|---|
| Frozen focused zero probe | RED 16/17 exit 2 -> GREEN 17/17 exit 0 |
| Original positive forgery `g5_review_probe.py` | 34/34, exit 0; positive rehash remains `B05_RENT_OPERATION_UNPROVEN` |
| Exact #1027 63-control witness | 63/63, literal exit `1` historical quirk preserved; both defects `accepted=false` |
| Exact #1027 cold probe | exit 0; `ok=true`, `warm_ok=true`, `child_exit=0`; two purchases + one rent; head unchanged |
| New R3 focused tests | 4 passed |
| Prior R2 focused tests | 5 passed |
| Author legacy B04/B05 tests | 6 passed |
| Selected read-only C03/C04 consumer | 3 passed |
| Inherited original B01-B05 43 | 43 passed once on final source |

Observed elapsed/RSS: RED 85.36 s / 60,424,192 B; GREEN 72.75 s / 56,250,368 B;
positive forgery 60.06 s / 60,702,720 B; #1027 22.98 s / 62,283,776 B; cold
23.41 s / 58,707,968 B; R3 focused 42.71 s / 62,877,696 B; R2 focused 46.70 s /
66,887,680 B; author legacy 65.31 s / 67,239,936 B; selected consumer 71.46 s /
71,438,336 B; inherited 43 528.82 s / 72,462,336 B.

## Actual first consumer and downstream material reader

- First consumer: `WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py:read_household_obligation`.
- Downstream material readers: `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py:read_household` and `read_dwelling`, plus `WORKER_RETURNS/SOROK-DUEL-B02-R1/historical_period.py:period_progress`.

## Preserved behavior

- Genuine positive rent remains `ADMITTED` and readable warm/cold.
- Genuine zero rent remains `UNCHANGED` and readable.
- Insufficient-resource rent remains `REFUSED` and readable.
- h1 remains `historical=true` after h2; h2 remains `historical=false`; exactly
  two debits.
- Replay is `REPLAY`; late same-period operation remains
  `B05_RENT_ALREADY_RECORDED`; no second debit.
- Changed/restored checkpoint, dwelling and B04 ownership cases pass.
- B04 foreign-root, operation exchange, ownership stale/restore and C02 chain
  forgeries still refuse; genuine B04 purchase still reads.
- No new writer, receipt schema, store, lock, ledger, registry, key, currency,
  C03/C04, P6 or D03 change.

## Boundaries

Only the leased B05 file and this own return were written. B04 and all other
product files are read-only. No protected write/merge, Browser/PYAT/SEAM
operation, new agent/server/controller, model/provider/account change, global
permission, installation or CI dispatch. The hard-money composite remains
invisible per the settled product choice; no portal work was done.

## Limits

Sourcefree engineering only. No native science, actor knowledge, human
authority or motive/volition inference is claimed. Fully privileged checkpoint
fabrication remains outside the observed public-action/`append_episode` threat
model. Provider checkpoint/org/quota and token/USD cost are `UNOBSERVED`.

## STOP

The author cannot self-G5. The separate nonauthor `ses_e21caf5dfffeSywXGrQ6qw65oe`
should receive this frozen cut in its separate checkout. No automatic R4.

Evidence, pins and commands: `EVIDENCE.json`, `evidence/`, `G5_HANDOFF.md`,
`PROGRAMMA_DELTA.json`.
