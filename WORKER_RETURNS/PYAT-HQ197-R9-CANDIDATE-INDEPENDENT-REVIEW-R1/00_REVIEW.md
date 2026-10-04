# PYAT HQ197 — R9 candidate independent review — R1

**Disposition:** `BROKER_CANDIDATE_PARTIAL__BYTE_CAP_REPAIR_REQUIRED`

**Terminal:** `HQ197_R9_CANDIDATE_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq197-r9-broker-candidate-hostile-r1`
Commissioned startup SHA: `b047e3258db80e753c23e5b5d70300e23b9bfafd` — **verified equal**
Candidate: `d5ce4ecff6acc25d199577a7859de7e98514e9fd`
Checkout mode: `SPARSE_REQUIRED` — honored. No clone, no full worktree, sparse checkout not widened.
Reviewer: DeepSeek Harness, **DeepSeek V4.1 Flash**.

---

## Bottom line

The candidate is **substantially sound**: the one-open broker route genuinely works, DTA reset
is genuinely correct, environment identity is unchanged, the 23-module closure is clean, and
the exact R7 court passes **55/55 twice**. It fails on **one load-bearing control**: the
`reader_bytes` ceiling is a **declared field that cannot fire**. The commission ordered me to
distinguish a declared field from an enforced limit — it resolves against the candidate.

## 1. Mission results

| # | Item | Result |
|---|---|---|
| 1 | one app-owned open, file-like objects not paths | **CONFIRMED** |
| 2 | stays on pyreadstat 1.3.6, identity unchanged | **CONFIRMED** |
| 3 | DTA position-zero view/reset over one physical open | **CONFIRMED** |
| 4 | `SourceAccessBudget.reader_bytes` enforced? | **NO — declared only** |
| 5 | raising from the read callback | **HANGS — not a safe limit; candidate correctly avoids it** |
| 6 | usecols vs underlying reads/bytes | **identical I/O; only returned columns differ** |
| 7 | modified pre-existing tests | change 1 preserved; **change 2 weakened coverage** |
| 8 | closure raw-path audit | **CLEAN** (23→24 modules; sole addition is the broker) |

## 2. The one-open route (confirmed)

`GovernedSourceOpen` opens the path **exactly once**, lazily; every logical parse gets a
`view()` that seeks the *same* handle to 0. Measured across metadata + selected + full reads:
**`path_opens=1`, `logical_views=3`**, one physical open.

No raw path reaches the reader: the sole reader call is
`pre553_source_access_broker.py:535 result = reader(arg, **kwargs)` where `arg` is a
`_GovernedView`, and line 522 raises `RawSourcePathEscape` if the argument is
`str`/`bytes`/`os.PathLike`. The broker additionally pins the pyreadstat seam itself (version,
genuine entry point, `usecols` presence, first parameter name) — defence in depth.

## 3. The blocking defect — `reader_bytes` cannot fire

`reader_bytes` is populated by `_sync_reader_totals()` as an **absolute snapshot taken after**
the reader returns. `SourceAccessBudget.check()` *does* project it, but **no call site ever
passes a `reader_bytes` delta** (`grep check( | grep -c reader_bytes` → **0**). Since
`current + 0 > cap` is only evaluated before operations that do not change bytes, the cap is
**dead configuration**.

Measured with `SourceAccessBudget(reader_bytes=10)` on a 12479-byte synthetic carrier:

| Operation | Bytes actually consumed | Violation raised |
|---|---|---|
| `metadata_read()` | **691** | **no** |
| `full_read()` | **12691** | **no** |
| `selected_read(['A'])` | **12691** | **no** |

Control caps still fire (`path_opens=0`, `metadata_reads=0`, `reader_invocations=0` all raise),
so **the gate machinery works — it is simply never wired for the byte account.**

**Why this is not a trivial oversight:** a mid-read byte ceiling requires the read callback to
interrupt the compiled reader. The only interrupt primitive the bridge exposes is the bare
`except: return -1` in `pyobject_read_handler` — and using it **hangs** (I re-confirmed on the
candidate's own view: no return within 15 s, killed). The candidate does **not** raise inside
its read path (verified by inspection), so it avoided the hang — and that is precisely why its
byte cap cannot fire. The safe alternative is a **premature EOF (`b""`)**, which produces a
prompt `ReadstatError` on SAV and DTA. I therefore require either genuine enforcement via EOF
with the in-flight residual documented, **or** re-typing `reader_bytes` as a measured account
so no consumer believes it bounds anything.

## 4. DTA reset (confirmed correct)

The candidate deliberately **avoids** `read_file_in_chunks` and uses an explicit
`row_offset`/`row_limit` loop with a fresh position-zero view per chunk over one physical open.
I reproduced the reason: over a broker view, `read_file_in_chunks` **fails for DTA**
(*"This version of the file format is not supported"*) but works for SAV. The candidate's
route gives correct chunks on both (500 rows, 1 open, 6 views, 5 chunk reads). `view()` returns
to position 0 on the same handle (`tell()==0`, `physical_opens` still 1), and chunk sizing is
honoured (1000-row carrier: `chunk_rows=7` → 143 chunks ≤7; `=100` → 10 chunks of 100). **No
fallback to a raw path string.**

## 5. usecols (measured, authority deferred)

| Carrier | Mode | Returned cols | read calls | bytes |
|---|---|---|---|---|
| SAV | `selected_read(['C0'])` | `['C0']` | 4054 | 192943 |
| SAV | `full_read()` | 6 cols | 4054 | 192943 |
| DTA | `selected_read(['C0'])` | `['C0']` | 4055 | 196393 |
| DTA | `full_read()` | 6 cols | 4055 | 196393 |

Identical I/O — matching HQ196 independently. The candidate **discloses** this honestly in
`selected_route_physical_column_suppression` (`NOT_ENFORCED_BY_READER__…measured_identical_bytes…`),
which I record as a strength. Per the commission I do **not** decide the authority meaning of
*PHYSICAL*.

## 6. Modified tests

**Change 1** (hash seam) **preserves** its guarantee — the seam was renamed because the hash
now runs over the broker's open. **Change 2 is weakened:** the freeze asserted
`chunk_calls[0]["chunksize"] == 2`, i.e. that the *requested chunk size was honoured*; the
rewrite asserts only `chunk_reads >= 1` on a 3-row carrier where everything fits in one read.
A chunk-size regression would no longer be caught. The behaviour itself is correct (verified
above), so this is a **test-coverage regression, advisory not blocking**.

## 7. R7 six-file court and closure audit

- Collect-only: **55 tests collected**, exit 0 (matches the required count).
- Run 1: **55 passed** (73.80 s, exit 0). Run 2: **55 passed** (68.09 s, exit 0). No failures
  hidden or retried.
- Closure: computed independently by AST traversal — **23 modules at the freeze** (matching the
  accepted closure) and **24 at the candidate**, the sole addition being the new broker. In the
  closure there is exactly **one** reader call site and it receives a file-like object. **No
  remaining raw-path pyreadstat call.** The WVS7 materializer is outside the closure and was
  not treated as a blocker.

**Environmental disclosure (full):** the first court attempts showed 6 then 5 failures, all
`FileNotFoundError` for **repository-committed fixtures outside the three commissioned sparse
patterns**. This is environmental, not a regression: the failing test file is **byte-identical
to the freeze**, all 9 of its tests pass in the canonical clone where fixtures exist, and every
failure was a missing-file error. I made the fixtures reachable via a **read-only symlink** and
verified `git sparse-checkout list` was **unchanged**. A recommended fix is recorded: the
manifest should name these fixtures, or the court should run where they are materialized.

## 8. Disposition rationale

- Not `…ACCEPTABLE_PENDING_SELECTED_AUTHORITY`: that would pass a candidate whose headline byte
  ceiling silently does nothing.
- Not `MATERIAL_COUNTEREXAMPLE__CANDIDATE_UNSOUND`: the candidate is not unsound; the defect is
  bounded and repairable.
- Not `R7_REQUALIFICATION_FAILURE…`: the court passes 55/55 twice.

**Required repairs:** `BYTE-CAP-01` (blocking), `TEST-COV-01` and `FIXTURE-MANIFEST-01`
(advisory).

## 9. Holds observed

Zero real survey/source access (synthetic carriers only); zero locator discovery; zero warrant
issuance; zero live C4; no production mutation; no C7/actor work. No adoption or self-adoption.
Nothing written outside the commissioned return directory.
