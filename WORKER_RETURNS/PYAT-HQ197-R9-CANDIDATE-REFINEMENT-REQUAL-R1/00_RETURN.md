# PYAT HQ197 — R9 candidate refinement and exact requalification — R1

Role: **SOURCE-FREE IMPLEMENTATION WORKER — SPACE BUNNY**
Branch: `agent/rabochii-pyat-hq197-r1`
Startup SHA: `5b98343561e5bf225442d9ab59032d36e98693ba` — verified exactly.
Candidate ancestor `d5ce4ecf` — verified, exactly 1 commit apart.

## Disposition

`CHECKOUT_MODE_INSUFFICIENT__HQ_RECOMMISSION_REQUIRED`

**The primary repair is complete. The mandated 55/55 court target is unreachable under the
commissioned sparse manifest, and the gap is checkout-caused, not candidate-caused.**

## The headline: I could not reach 55/55, and here is exactly why

Collect-only gives **exactly 55** (9+8+13+9+6+10), as required. But the court runs
**49 passed / 6 failed**, twice, before *and* after my refinement:

| | run 1 | run 2 |
|---|---|---|
| pre-refinement (inherited candidate) | exit 1, 3.0s — 6 failed / 49 | exit 1, 3.0s — 6 failed / 49 |
| post-refinement (this lane) | exit 1, 3.0s — 6 failed / 49 | exit 1, 3.0s — 6 failed / 49 |

All six are in one file and all six are `FileNotFoundError`, not assertion failures:

```
WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/01_PHYSICAL_KEY_INVENTORY.json
WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py
```

Both **exist in git at HEAD**; neither is covered by the commissioned sparse manifest.

**I proved they are candidate-independent** rather than asserting it: I reverted the
candidate's production files to pre-candidate state (`55f75664`) in this same worktree and
re-ran the court — **the identical 6 failed, 6/49**. Then I restored the candidate.

I did not retry them away, did not expand the sparse checkout beyond the commissioned
manifest, and did not edit anything to make them pass.

### The fix HQ needs to apply

Add two sparse patterns. That is the entire gap:

```
/WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/
/WORKER_RETURNS/EE-P2R6S/
```

No clone, no full checkout, no other path.

## Primary repair — `reader_bytes` is now a real ceiling

It was a declared limit consulted nowhere. Now the limiter is armed per compiled-reader
invocation with the remaining allowance, and it **never raises through the read callback** —
because an exception inside a file-like object that a C extension is calling from arbitrary
internal state can be swallowed, become a short read, or hang.

- a request larger than the allowance is **shortened** to exactly the allowance
- at zero allowance it returns `b""` so the reader sees clean EOF and stops on its own
- the breach is raised as a typed `READER_BYTES_LIMIT_EXCEEDED` at the **outer decode
  boundary**, with exact accounting

On a truncated stream pyreadstat raises its own `ReadstatError`. I capture that, account it,
and re-raise it as a typed byte-limit breach chained from the original — so the refusal is
attributable to the ceiling rather than looking like a generic reader fault. If the limiter
did *not* trip, the original error propagates unchanged.

Measured (3 cols × 60 rows, 611 bytes needed):

| cap | outcome | consumed | within cap |
|---|---|---|---|
| unlimited / 100000 / **611** | OK | 611 | yes |
| **610** (one short) | REFUSED | 610 | yes |
| 200 | REFUSED | 200 | yes |
| 10 | REFUSED | 10 | yes |

Six new negative courts (C11–C11f) sweep eight ceilings, assert promptness (~0.2 ms against
a 10 s hang threshold), prove bridge safety, and distinguish an **allowed partial final read**
(exactly-enough cap → reader completes, no refusal) from an excess read.

**An extra defect surfaced and was fixed:** `reader_bytes` was inflated by the application's
own hash and header-prefix reads, because it was read as an absolute of the whole open. It is
now attributed by *delta* across each reader invocation, so the account matches its name.

## §2 — selected-route disclosure preserved

`selected_route_physical_column_suppression` still reads
`NOT_ENFORCED_BY_READER__pyreadstat_1_3_6_reads_full_stream_then_subsets…`. Counters stay
separate (`selected_reads=1`, `full_reads=0`, `metadata_reads=1`, `reader_bytes` independent).
**No physical suppression is claimed, and `PHYSICAL_SELECTED_VARIABLE_READ` was not
reinterpreted** — as commissioned.

## §5 — C4 closure audit, and it is falsifiable

Verdict: **`NO_RAW_PATH_READER_CALLS_IN_C4_CLOSURE`** — 22 modules, **0** raw-path reader
calls, **1** reader call, **1** source-path open.

That "0" is only meaningful because the auditor earned it. **It reported a false zero three
times** before detecting the reader at all:

1. it scanned only `pyreadstat.<reader>(...)` and missed the local-variable alias,
2. then missed the `self.pyreadstat.<reader>` form,
3. then missed the **ternary** that actually binds the alias (`ast.IfExp`, not `ast.Attribute`).

A static audit that reports zero is worthless unless it can report non-zero. So I ran a
**positive control** against the out-of-closure WVS7 file: the same auditor detects its **2**
real `read_sav(str(path))` calls. The zero is a real negative.

**Count discrepancy reported, not reconciled:** the commission said **23** modules; the accepted
C4C3 artifact *and* the freeze both say **21** (`c4_import_closure_modules: 21`). I used the
accepted list and reported the gap rather than inventing two modules. My broker is audited as
a genuine closure addition → 22 audited.

**WVS7 materializer:** outside the closure, **not edited**, still has its 2 raw-path calls.

## Full regression

**335 failed / 2498 passed / 1 skipped / 58 errors** — identical failure set to the HQ196
candidate run (335/2492/58). **Zero new failures**, +6 passes from the new byte-limit courts.
The 335/58 are pre-existing sparse artefacts.

## Freeze-law note worth HQ's attention

The freeze's own `validity_and_invalidation` lists **"any `rawlsing_next/**` production blob
change"** as an invalidating condition, with *"STOP… a new qualification is required."* This
lane changes a production blob by construction — which is precisely why a requalification was
commissioned and why I inherit no earlier pass. No dependency or interpreter changed, so no
version-based invalidating condition is triggered.

Also: the freeze declares the import closure as **21** modules, and the candidate adds one,
so the closure is now **22**. If the closure count is itself bound anywhere, that is a
requalification fact.

## Holds

Zero real survey-source access, locator work, warrant, live C4, C7/actor work. pyreadstat and
the R7 environment unmutated. WVS7 materializer not edited. No production file touched outside
terrain — `pre553_physical_decoder.py` did **not** require modification, because the seam
already exposed `source_access_budget`, so the refinement stayed inside the broker. No sparse
expansion beyond the manifest; no clone; no self-adoption; no failure retried away.

## Artifacts

`01_BYTE_LIMIT_REPAIR.json` · `02_C4_CLOSURE_AUDIT.json` · `03_FINAL_DISPOSITION.json` ·
`evidence/r7_six_file_court.txt` · `evidence/c4_closure_audit.json` (+ runner) ·
`rawlsing_next/tests/test_pre553_source_access_broker_court.py` (20 courts)

Terminal: `HQ197_R9_CANDIDATE_REFINEMENT_RETURNED__HQ_REVIEW_REQUIRED`
