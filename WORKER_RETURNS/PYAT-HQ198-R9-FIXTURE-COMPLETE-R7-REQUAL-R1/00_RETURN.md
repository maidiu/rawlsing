# PYAT HQ198 — fixture-complete R7 requalification proof — R1

Role: **SOURCE-FREE PROOF WORKER — SPACE BUNNY**
Branch: `agent/rabochii-pyat-hq198-r1`
Startup SHA: `2eccd7a4cec0e85af78cb68f6c078de2b68d5d90` — verified exactly.
Candidate `4b6335ca` / repair `a483cb66` — both verified ancestors of startup.
**No production code was modified in this lane.**

## Disposition

`R7_REQUALIFIED_55_OF_55_TWICE__BROKER_COURTS_PASS`

## The headline

The fixture-complete manifest closed the HQ197 blocker exactly as predicted:

| step | result | exit | duration |
|---|---|---|---|
| collect-only | **55 tests collected** (9+8+13+9+6+10) | 0 | 2.0s |
| **run 1** | **55 passed**, 0 failed | 0 | 74.0s |
| **run 2** | **55 passed**, 0 failed | 0 | 71.0s |

**55/55 twice.** There were no failures to retry.

A corroborating detail worth noting: runtime rose from ~2.7s (HQ197) to ~65s. That is the
expected signature of the previously-aborted file **actually executing its assertions**
instead of dying at `FileNotFoundError` — independent evidence the tests genuinely ran rather
than being silently skipped. Both fixtures were confirmed `PRESENT` on disk *before*
collection, so the 55/55 is not a collection artefact.

## Broker courts

Candidate court: **20 passed, 0 failed**, exit 0.
Independent exercises: **9/9**, exit 0.

I ran these separately from the candidate's own courts on purpose — a court that had drifted
or softened would still be caught.

| property | evidence |
|---|---|
| exactly-enough | cap 703 = bytes needed → completes, consumed 703, **not** a breach |
| one-byte-short | cap 702 → `READER_BYTES_LIMIT_EXCEEDED`, consumed exactly 702 |
| no bytes beyond ceiling | 8-ceiling sweep (1, 7, 64, 199, 702, 703, 704, 2109) — consumed ≤ cap every time, breach = none |
| **no callback exception as limiter** | driven directly under an armed allowance of 24: chunks served **`[24, 0]`** — exactly the allowance, then clean EOF. No exception crossed the bridge |
| DTA view/reset | naive single-view reuse **fails**; fresh position-zero views give correct disjoint chunks over **1** physical open |
| `chunk_rows` on a larger carrier | 200-row × 3-col at batch 30 → 20 chunk reads, all 200 rows, max batch 30, every `V00` value exact |
| selected/full counters | `selected_reads=1`, `full_reads=0`, `metadata_reads=1`, bound ordinals `[2]` |
| non-suppression disclosure | preserved verbatim |

One more result that *corroborates* the disclosure rather than contradicting it: on the same
carrier the **selected route moved 2846 physical bytes vs 703 for a full read**. It moves
*more*, because `usecols` subsets after a full stream read. Nothing anywhere claims byte
suppression.

## C4 closure proof — recomputed, not asserted

I derived the closure by AST walk from the five declared C4 layer roots, independently at the
freeze and at the candidate, rather than trusting any declared count.

- **freeze: 21** imported modules — exactly matching the accepted C4C3 declaration
- **candidate: 22** — delta **exactly +1 = the broker**, nothing else added or removed
- **0 raw-path reader calls** anywhere in the closure; **1** reader call total (the broker's,
  first argument is the governed view, not a path)
- **1 governed open per scope**, confirmed empirically: 100 decode+iterate cycles → exactly
  100 physical source opens, with the two dormant decoder fallbacks reached **0** times

**On the 23/24 figures:** the commission's 23 is the 21 imported modules **plus the two
declared producer/consumer references**, exactly as the accepted C4C3 artifact's own
completeness note states ("…these 21 module names **plus the two declared
producer/consumer references**"). On that basis freeze = 23 and candidate = 23 + broker = 24.
**Both bases agree on the load-bearing fact: the delta is exactly +1.** This resolves the
21-vs-23 discrepancy I flagged in HQ197. I did not independently re-derive *which* two modules
those are; I used the accepted artifact's own stated relationship.

**WVS7 materializer:** outside the closure, **not** treated as a C4 defect, **not** edited.

## Two self-corrections I want on the record

Both were bugs in my *measurement*, not in the candidate — and both are the kind that get
quietly suppressed if not written down:

1. **The DTA exercise first reported FAIL (8/9).** The candidate was right and my expectation
   was wrong: the exercise builds `V00 = float(i)`, so the correct chunks are `[0,1]`/`[2,3]`
   and I had asserted `[0,2]`/`[4,6]`. I corrected the **assertion**, not the code, and
   re-ran.
2. **The closure first derived 22 modules against the declared 21.** The auditor was expanding
   `from X import *` into phantom submodules, fabricating
   `rawlsing_next._pre553_query_common.*`. I removed the expansion; the derived freeze closure
   became exactly 21. An unexplained extra module is a bug in the measurement.

I also carried forward the falsifiability discipline from HQ197: **the closure auditor reported
a false zero three times** in that lane, so here the same auditor is run against the
out-of-closure WVS7 file as a **positive control** — where it correctly finds its **2** real
`read_sav(str(path))` calls. A static audit that cannot report non-zero proves nothing.

## Out of scope, recorded not hidden

`test_pre553_sr06_decoder_carrier.py` (not one of the six commissioned files) reports
**2 failed, 14 passed, 1 skipped** — `ModuleNotFoundError: No module named 'duckdb'`. duckdb is
absent from the R7 qualified venv. Identical to HQ196/HQ197, an environment package absence,
not a candidate defect. Not retried, not worked around.

## What this does *not* establish

Source-free only — qualifies no real source, and is not survey-semantic equivalence. The
selected route still does not physically suppress unselected-column bytes. Runtime identity is
unchanged (interpreter, pyreadstat, ReadStat, pandas, numpy all untouched). **R9 is not closed
by this lane** — the architecture-warrant candidate and the authority questions HQ195 recorded
remain HQ and Astra decisions. No adoption, warrant, locator work, live C4, C7 or actor work.

## Checkout law

`SPARSE_REQUIRED` honoured. No clone, no full checkout; **355 files materialised against 7097
tracked**; zero expansions beyond the six commissioned patterns; `sparse-checkout disable` never
run. Helper blob `22f3f624…` (sha256 `93e3fc97…`), byte-identical to the copy safety-reviewed
in HQ195, run from a temp copy because the canonical clone sits at the older freeze where it is
absent.

## Artifacts

`00_RETURN.md` · `01_R7_EXACT_COURT.json` · `02_BROKER_COURT.json` · `03_C4_CLOSURE_AUDIT.json` ·
`04_FINAL_DISPOSITION.json` · `evidence/c4_closure_proof.json` (+ runner) ·
`evidence/independent_broker_exercises.json` (+ runner)

Terminal: `HQ198_R9_FIXTURE_COMPLETE_REQUAL_RETURNED__HQ_REVIEW_REQUIRED`
