# PYAT HQ199 — governed source-session / accounting owner — R1

Role: **SOURCE-FREE IMPLEMENTATION WORKER — SPACE BUNNY**
Branch: `agent/rabochii-pyat-hq199-r1`
Startup SHA: `f26b2ea632725596a9e94957ef1d6053c96c735c` — verified exactly.
Base `4b6335ca` — verified ancestor.

## Disposition

`GOVERNED_SOURCE_SESSION_CANDIDATE_READY_FOR_INDEPENDENT_REVIEW`

## The key correction, and why it mattered

The old decoder had this:

```python
elif encoding is not None:
    frame, metadata = broker.full_read(encoding=encoding)
```

So **a non-null encoding alone forced a full row-data read**. That conflated reader
configuration with row-data mode.

Now `encoding` is reader configuration and the plan alone decides the mode. Measured:

```
METADATA_ONLY + encoding="latin1"  ->  metadata 1, selected 0, full 0, chunk 0
```

That is the defect the commission named, fixed and measured rather than asserted.

## The owner

`rawlsing_next/pre553_source_session.py`. Created **once per caller-bound source entry**,
reused for every admitted operation in that scope:

```
3 plans in one session -> decoder_invocations=3, path_opens=1
```

One broker, one physical open, one aggregate receipt, one decoder-invocation account,
deterministic close. `RowDataMode` keeps the four modes independent, each driving exactly one
reader account:

| mode | account driven | measured |
|---|---|---|
| METADATA_ONLY | metadata_reads | meta 1, sel 0, full 0, chunk 0 |
| SELECTED | selected_reads | meta 1, **sel 1**, full 0 |
| FULL | full_reads | meta 1, full 1, **chunk 0** |
| CHUNKED_FULL | chunk_reads | meta 1, **chunk 4**, full 0 |

## Header-prefix is now explicit

`header_prefix_bytes=None` admits **no** prefix access — verified across all three non-chunked
modes (`header_prefix_reads=0`). `176` yields exactly one operation of 176 bytes.

## decoder_invocations ≠ reader_invocations

Added to `SourceAccessAccount`, `SourceAccessBudget`, the receipt basis and the pre-operation
checks, counted **once at the entry boundary** via `admit_decoder_entry()`. `reader_invocations`
was not renamed. Measured on a chunked decode: **decoder 1 vs reader 5**.

With the cap at 1, a second entry is refused with **all nine tracked accounts unmoving** —
`decoder_invocations`, `metadata_reads`, `selected_reads`, `full_reads`, `chunk_reads`,
`hash_passes`, `header_prefix_reads`, `path_opens`, `reader_invocations`. That is the
pre-operation property the commission asked for, asserted field by field rather than by count.

## Requalification

Production blobs changed, so the freeze's own invalidation condition (*"any `rawlsing_next/**`
production blob change"*) is triggered and a new qualification is required:

| step | result | exit | duration |
|---|---|---|---|
| collect-only | **55 collected** | 0 | 1.0s |
| run 1 | **55 passed**, 0 failed | 0 | 50.0s |
| run 2 | **55 passed**, 0 failed | 0 | 49.0s |

Session courts **15 passed**, broker courts **20 passed**, full suite **325 failed / 2523
passed / 58 errors** with **zero new failures**.

(The 10 fewer failures than the older baseline are fixture-dependent tests that now actually
run — this manifest materialises the FIABC/EE-P2R6S fixtures. Not attributable to my change.)

## Closure

Recomputed by AST from the five declared layer roots: freeze **21** → candidate **23**, delta
**+2** = the broker + the session module, both access/plan *mechanism*, not source policy.
**0 raw-path reader calls**, 1 reader call whose first argument is the governed view. The
positive control still finds the WVS7 file's 2 real `read_sav(str(path))` calls, so the zero is a
real negative.

## Two self-corrections, both in my courts
1. **c11** threw `AttributeError` on `.value` — I used a manual `try/except`, which binds the
   exception rather than a pytest `ExceptionInfo`. Fixed the court to `exc.code`.
2. **x3** reported "SRC02 hardcoded" — a substring scan flagged the module's *own docstring*,
   which names those sources precisely to record that it does **not** encode their plans. I
   replaced it with an AST scan of non-docstring literals and identifiers, so the check tests
   **code, not prose**.

Neither correction touched product code.

## What I deliberately did not decide
- **No SRCxx policy is bound.** Court x3 proves zero source constants exist in code.
- **SRC27's "multiple path-level opens" normativity is not adjudicated.** I supplied only the
  mechanism by which an admitted prefix size either is or isn't read.
- The selected route still does not physically suppress unselected-column bytes; disclosure
  unchanged.
- **R9 is not closed by this lane** — the architecture-warrant candidate and the authority
  questions remain HQ/Astra decisions. No adoption, warrant, locator work, live C4, C7 or actor
  work.

## Artifacts

`01_SESSION_OWNER.json` · `02_R7_REQUALIFICATION.json` · `03_CLOSURE_AND_HOLDS.json` ·
`04_FINAL_DISPOSITION.json` · `evidence/r7_six_file_court.txt` ·
`evidence/c4_closure_proof.json` (+ runner) ·
`rawlsing_next/tests/test_pre553_source_session_court.py` (15 courts)

Terminal: `HQ199_R9_GOVERNED_SOURCE_SESSION_RETURNED__HQ_REVIEW_REQUIRED`
