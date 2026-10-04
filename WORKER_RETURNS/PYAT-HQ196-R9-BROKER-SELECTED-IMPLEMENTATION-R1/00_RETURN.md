# PYAT HQ196 — R9 brokered source access + selected-reader implementation — R1

Role: **RABOCHII / SOURCE-FREE IMPLEMENTER — SPACE BUNNY**
Branch: `agent/rabochii-pyat-hq196-r9-broker-selected-implementation-freeze-r1`
Commissioned startup SHA: `55f75664949b4a92431b54351e7244ff1fa4a652` — verified exactly.
Lineage: exactly **1 commit over the executable freeze `8ff40d37`**, as commissioned.

## Disposition

`BROKER_SELECTED_CANDIDATE_READY_FOR_HOSTILE_REVIEW`

A **candidate**, not an adoption. No self-adoption, no warrant, no authority exercised, no
live C4, zero real-source access.

## The census expectation was wrong — verified, not assumed

The commission expected the repository-wide pyreadstat census to be confined to
`pre553_physical_decoder.py` and directed me to verify that. **It is not confined.**
`rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py` lines 986 and 1015 make
production `pyreadstat.read_sav(str(path), …)` calls — and line 1015 already does
`usecols=["B_COUNTRY"]`, so a selected read already exists outside the decoder.

Those sites are **outside my write terrain**. I did not broker or modify them, and I did not
determine whether they sit inside the C4 governed closure — that is an authority question,
and it is LIM-5.

## What the census found in the decoder (before any edit)

| Site | Operation | Account created | Owner |
|---|---|---|---|
| `_decode:481` | `source.is_file()` | existence check | application |
| `_sha:211` | `path.open("rb")` | hash pass **+ a physical open** | application |
| `_raw_layout_declarations:407` | `source.open("rb")` | header read **+ a 3rd physical open** | application |
| `_decode:496` | `reader(str(source), metadataonly=True)` | metadata read **+ OS open inside the compiled reader** | **compiled, unowned** |
| `_decode:499` | `reader(str(source), …)` | full read **+ another OS open** | **compiled, unowned** |
| `iter_batches:155` | `read_file_in_chunks(reader, self._source_path, …)` | chunk reads **+ OS opens** | **compiled, unowned** |

So the path-open account was **both** incomplete (three separate application opens for one
scope) **and** partly unobservable (the compiled reader's opens were outside application
control). Selected reads: **zero occurrences**.

## Seam 1 — the broker

`rawlsing_next/pre553_source_access_broker.py`. The application performs **exactly one**
physical open and lends it to the compiled reader through a position-zero view exposing
`fileno()`.

| | before | after |
|---|---|---|
| application-owned physical opens | **3** | **1** |
| compiled-reader path opens | unbounded, unobservable | **0** |
| raw path strings reaching the reader | yes | **0** |

I did **not** force the count. One open is what serving the whole scope actually requires.
`logical_views` is reported separately from `path_opens` precisely so a rewind is never
presented as a fresh open — and the tests assert `account.path_opens == physical_opens` and
`account.logical_views == views_issued`.

All six seam facts were **measured before implementation**, not assumed. The two that shaped
the design:

- **DTA needs a real fd.** ReadStat maps its input: a pure `BytesIO` works for SAV but is
  *rejected* for DTA. Hence `fileno()` over the application's own open.
- **Reuse across row-offset parses fails** — ReadStat wants position zero. Calling `view()`
  again succeeds because it rewinds the same open. That is the whole fix.

## Seam 2 — the selected route

`usecols`, with names and ordinals bound against the real column inventory **before** any
row-data read. Every carrier: `selected_reads=1`, `full_reads=0`. Missing selection →
`DecoderError` before any row read. A reader injecting an unselected column →
`UNEXPECTED_SELECTED_COLUMN`. The route pins `full_reads=0`, so a full read is refused
before it executes.

## The honest limitation (LIM-1)

**pyreadstat 1.3.6 does not physically suppress reads of unselected columns.** Measured on a
12-column / 200-row SAV (20,159 bytes on disk): a full read and `usecols=["c00"]` issued an
**identical 278 read calls and 20,659 bytes**.

So the selected route is a genuine **logical** selected-read account. It is **not** evidence
that unselected columns went unread, and the candidate does not claim it. The receipt carries
`selected_route_physical_column_suppression: NOT_ENFORCED_BY_READER…`, and court C9c asserts
that disclosure is present so it cannot be quietly dropped.

## DTA chunk constraint — proven, not asserted

Court **C5b** proves the naive form *still fails*: reusing one **view object** across two
`row_offset` parses raises. So the reset is load-bearing, not decorative. The governed loop
issues a fresh view per chunk over the **same single open** — 5 logical views over 1 physical
open on a 10-row carrier. `read_file_in_chunks` is not used at all (it fails for DTA).

## Courts

Nine mandatory courts, **14 passed / 0 failed**. Budget refusals are proven to fire *before*
the operation: after a refusal `reader_bytes` is unchanged and `header_prefix_reads` is still
`0`.

Run twice: `2 failed, 28 passed, 1 skipped` both times — deterministic. Both failures are
`ModuleNotFoundError` for **duckdb** and were verified failing at the pristine freeze.

## Equivalence at declared grain — and an unlocated prior

- **A full route: 55/55 equivalent**
- **B selected route: 55/55 equivalent**
- **distinct path opens observed: `[1]`**

**The prior named 55-carrier court could not be located** — no runner, corpus or expected-result
artifact at the commissioned freeze, in the R7 qualification environment, or in reachable
history. The figure appears only as prose in the HQ195 feasibility return. So this corpus is
**constructed here**, is **not** a re-run of the prior court, and inherits **no** pass from it.
Matching the count makes the denominator comparable, not the corpus identical.

I also corrected an 8-carrier "missingness difference" that was a **harness artefact**: raw
pyreadstat yields `NaN` where the decoder contract yields `None`. Normalising **both** sides
through the canonical `_physical_value` made them agree exactly — asymmetric normalisation
would have manufactured a fake semantic regression.

## Regression: measured, not assumed

A single run cannot distinguish my regression from pre-existing sparse failures, so I
captured a **real pristine baseline** by setting the candidate aside and restoring the freeze:

| | failed | passed | skipped | errors |
|---|---|---|---|---|
| pristine freeze | 335 | 2478 | 1 | 58 |
| candidate | 335 | **2492** | 1 | 58 |

**Regressions introduced: 0.** Net +14 passes = my new courts. The 335/58 are sparse
artifacts (fixtures outside the manifest); the identical 5 collection errors reproduce at the
pristine freeze.

### Six defects I introduced and caught

Worth stating plainly, since most were real:

1. **Selected route attributed values to the wrong variable names** — the inventory stayed
   full-length while the frame held one column, so `emit()` mis-zipped. A genuine correctness bug.
2. **`_bump` used `replace`, which *sets* fields** — zeroed delta entries wiped accumulated
   counters; the account reported last-operation values instead of totals.
3. **kwarg filtering against the reader signature** silently dropped `metadataonly`/`usecols`
   for a `(*args, **kwargs)` test double, **downgrading a metadata read into a full read**.
4. **The receipt was snapshotted at decode**, hiding later chunk reads from the account meant
   to record them.
5. **The default budget capped `full_reads` globally**, wrongly forbidding the ordinary
   compatibility decode; that cap belongs to the selected route only.
6. **The governed hash seam was unobservable**, so identity-gate-before-reader-access could no
   longer be audited.

## Two tests changed — and why that is disclosed

Both encoded mechanisms the commission told me to replace. Neither assertion was weakened:
each now tests the **governed property** instead of the removed helper.

- `…is_hashed_once_before_reader_decode` → instruments `_governed_source_sha` instead of
  `_sha` (the hash now runs over the broker's open). Still fails if a reader is reached before
  the hash.
- `…uses_chunk_path_and_compatibility_uses_full_read` → asserted `read_file_in_chunks` was
  called. That helper fails for DTA. Now asserts: chunk reads occurred, exactly one physical
  open, correct cells and ordinals, and compatibility still metadata-then-full-read.

Also: `iter_batches` now **raises** `RawSourcePathEscape` when no broker is attached, instead
of silently reverting to a raw path. Verified **zero regressions**, so nothing depended on the
removed fallback.

## Holds

Zero real-source access, locator discovery, warrant issuance, live C4, C7, actor/person work.
pyreadstat/ReadStat **unmutated**; the R7 environment **unmutated**; interpreter and package
identity **unchanged** (`11d6f541…`, anchor `C4C3-DARWIN-X86_64-ANCHOR/CPYTHON-3.11.3/
PYREADSTAT-1.3.6/…`). Zero production files touched outside terrain. Every carrier was
synthetic, written by pyreadstat's own writer into a temp dir and deleted with it.

**R9 is not closed by this lane.** It closes two implementation seams. The architecture-warrant
candidate and the authority questions HQ195 recorded remain HQ/Astra decisions.

## Checkout law

`SPARSE_REQUIRED` honoured. No clone; **331 files materialised against 7078 tracked**; **zero**
sparse expansions; `sparse-checkout disable` never run; no full checkout.

One disclosure: the commissioned helper exists only on the documentary-control lineage
(`aad3fc2a8`) because this branch is deliberately rooted on the freeze. I read it by git
object, verified blob `22f3f624…` (sha256 `93e3fc97…`, byte-identical to the copy
safety-reviewed in HQ195), reviewed it, and ran it from a temp copy. Using the helper as a tool
imports no lineage — it creates the worktree **at the passed SHA**.

## Artifacts

`01_PHASE0_CENSUS.json` · `02_CANDIDATE_RESULT.json` · `03_FINAL_DISPOSITION.json` ·
`evidence/declared_grain_comparison.json` (+ its runner) · `evidence/court_runs.txt` ·
`evidence/full_suite_vs_baseline.txt` ·
`rawlsing_next/tests/test_pre553_source_access_broker_court.py` (the 14 courts)

Terminal: `HQ196_R9_BROKER_SELECTED_IMPLEMENTATION_RETURNED__HQ_REVIEW_REQUIRED`
