# HQ195-R1 Return — R9 Instrumented Runtime Feasibility

**Disposition:** `INSTRUMENTED_RUNTIME_FEASIBLE__SEMANTIC_EQUIVALENCE_NOT_YET_PROVED`
**Branch:** `agent/rabochii-pyat-hq195-r9-instrumented-runtime-feasibility-r1`
**Startup SHA (verified exact):** `f895b3dc2934a3d742722657ea43ba174d10043b`
**Commission implementation base:** `9dd3cac1fea3620f2ab7769cf4b90ab111f0ae01`
**Checkout mode:** sparse, non-cone, sufficient. No full-tree materialisation.

---

## Headline

The inherited working hypothesis — that literal O1-C07 file-open accounting cannot be
satisfied on this host without privilege or an architecture change — **is falsified.**

Literal O1-C07 accounting is achievable on the **accepted runtime**, with:

- no rebuild of pyreadstat or ReadStat
- no interposition, no `sitecustomize`, no monkeypatch of the compiled extension
- no privileged tracing
- no change to R7 runtime identity

The whole mechanism is a roughly 90-line application-side file broker plus a change to
the one call site that hands a file to the reader.

## Why it works

pyreadstat 1.3.6 **already contains the seam**. It was found by reading the installed
package source, not by guessing:

| Site | What it does |
|---|---|
| `_readstat_parser.pyx:1251-1254` | An object with `.read` and `.seek` is taken as a file object, and the filename is set to **empty** |
| `_readstat_parser.pyx:965-977` | With a file object, ReadStat gets four **Python-bridging handlers** |
| `_readstat_parser.pyx:865-869` | `pyobject_open_handler` and `pyobject_close_handler` are **no-ops returning 0** |
| `_readstat_parser.pyx:873-891` | `pyobject_read_handler` calls the Python object's `.read()`; a raised exception becomes a ReadStat read failure |
| `_readstat_parser.pyx:844-851, 1273-1276` | The path existence check runs **only** when no file object was supplied |
| `_readstat_parser.pyx:1383-1402` | `read_sav`/`read_dta` hard-set the format, so an empty path does not break format selection |

The consequence is the whole result: **hand the reader an already-open object and the
compiled reader performs no path-level open of its own and has no path available to
open.** Every byte it consumes crosses the application's own `read()`.

The commission asked for routes in order. Route 1 (source instrumentation / rebuild) was
**superseded, not blocked** — it is strictly larger than necessary. Route 2 (a named
callback surface) has **no public API**, but route 2's *effect* is reachable without a
build-time wrapper. Route 3 (application-owned broker) was selected.

## Measured on synthetic carriers only

Two synthetic files (one `.sav`, one `.dta`), 4 rows × 2 numeric variables, written by
pyreadstat's own writer and destroyed with the temp directory.

| Probe | Route | Result |
|---|---|---|
| P2 | metadata (SAV) | 1 app open, **0 compiled-reader opens**, 38 reads, 635 bytes, 7 seeks |
| P3 | full decode (DTA) | 1 app open, **0 compiled-reader opens**, 59 reads, 1906 bytes, 5 seeks |
| P4 | equivalence | columns, shape and values **identical** |
| P5 | read ceiling `max_reads=1` | 2nd read **refused, `executed=false`**; loud `ReadstatError` |
| P6 | byte ceiling `max_bytes=16` | 4th read **refused, `executed=false`**; 23 bytes delivered |
| P7 | `read_file_in_chunks` (SAV) | **brokered OK** — 118 reads, 4 rows |
| P7b | `read_file_in_chunks` (DTA) | **failed** — root cause isolated in P9 |
| P9 | app-driven chunk loop (DTA) | **OK** — 4 rows, 2 opens, 114 reads |

Measurement basis is exact and complete, not sampled: the reader has an empty path and an
inert open handler, so it cannot obtain a byte except through a counted `read()`.

**Incidental corroboration.** The first brokered metadata read requested **exactly 176
bytes** — the same header-prefix size HQ192 identified from the Python layer. This lane saw
it arriving from the compiled reader's own read pattern. Independent confirmation from the
opposite direction.

## Three caveats a reviewer must weigh

**D1 — chunked DTA needs a fresh broker per chunk.** Reusing one broker across successive
`row_offset` parses of a DTA carrier fails (`ReadstatError: This version of the file format
is not supported`). Root cause: ReadStat's DTA `row_offset` parse expects the file at
position 0. Opening a fresh broker per chunk works. Consequence: pyreadstat's
`read_file_in_chunks` helper **cannot be used as-is for DTA**, and the application must own
the chunk loop. This matters because **DTA is SRC27's format** and the chunked path is the
reader site earlier lanes flagged as unmeasured. The failure is loud, not silent.

**D2 — the seam is de facto, not an API.** There is no public handler-registration
surface and no `pyreadstat.FileLike`. The seam is reached by duck-typing on
`.read`/`.seek` and could change without notice. **Pin the pyreadstat version** and assert
the seam still behaves, so a change is *detected* rather than silently disabling
governance.

**D3 — byte ceilings are pre-read gates, not byte-exact cuts.** With a 16-byte ceiling,
23 bytes were delivered before the next read was refused. Overshoot is bounded by one
in-flight read. Byte-exact truncation would corrupt the stream, so it is not proposed.

## What this does not establish

- **Not survey-semantic equivalence.** Only a 4-row, 2-variable grain was compared. No
  real source was opened.
- **Not complete call-site coverage.** Any reader invocation still passed a raw path string
  would remain ungoverned. **No inventory of such call sites was produced**, and coverage
  is opt-in per call site, so it is only as complete as that inventory — which does not yet
  exist.
- **Not OS-level accounting.** This is accounting at the application-owned file object,
  which is where the reader's I/O actually occurs on this route. A reviewer demanding
  descriptor-level truth still needs privilege, which remains unavailable.
- Metadata comparison was limited to column names and row counts; a full metadata-field
  diff was not performed. Only `.sav` and `.dta` were exercised.

## Requalification burden — smaller than anticipated

The commission's burden section is conditional on *a modified pyreadstat/ReadStat binary
being required*. **It is not required.** Therefore:

| Court | Rerun? | Why |
|---|---|---|
| R7 runtime identity | **No** | Runtime identity is unchanged |
| C3 synthetic/enforcement | **Yes** | The enforcement surface moved |
| C4C3 environment | **Yes** | Same — environment unchanged, exercised path is not |

**The 55/55 source-free qualification cannot be reused as-is.** The corpus and expected
outputs remain valid inputs; the *comparison pass* must be repeated, because the reader now
receives a different argument. This is a re-execution and comparison pass over an existing
corpus — not a rebuild, not a re-authorisation, not a new corpus.

**Reviewer acceptance needed before any live use:** that the compiled reader truly performs
zero path opens on this route; that the de facto seam is acceptable with a version pin; that
D1 is a permanent design constraint rather than a deferred bug; that D3's overshoot is
acceptable; and a decision on call-site inventory.

## Holds

All holds respected. Zero real-source operations, locator discovery, warrants, live C4,
production mutation, C7 or actor/person work. `rawlsing_next/**` was **not** edited — it was
materialised read-only for analysis. The accepted R7 environment was **not** mutated; all
work ran against it read-only, and no disposable rebuild was needed because no rebuild was
required.

**No adoption is proposed.** This is a feasibility result and it is unreviewed.

## Artifacts

| File | Contents |
|---|---|
| `01_IO_OWNER_SOURCE_MAP.json` | Where opens/reads actually occur; the seam, with line-anchored evidence |
| `02_MINIMUM_INSTRUMENTATION_DESIGN.json` | Route analysis; why route 3 beats route 1 |
| `03_SYNTHETIC_PROOF.json` | Probes P1–P9 with exact figures and requirement coverage |
| `04_ENFORCEMENT_NEGATIVE_CASES.json` | N1–N5, including refusal-before-execution |
| `05_OUTPUT_EQUIVALENCE_AT_TEST_GRAIN.json` | The grain, what was shown, what was not |
| `06_R7_REQUALIFICATION_BURDEN.json` | Courts, 55/55 reuse, reviewer acceptance |
| `07_LIMITATIONS.json` | D1–D3 plus scope, coverage and non-claims |
| `08_FINAL_DISPOSITION.json` | Disposition, and why each alternative was rejected |

Reference implementation and raw observed run:
`PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/R9-INSTRUMENTED-RUNTIME-FEASIBILITY-R1/hq195_broker_proof.py`
and `observed_broker_run.json` alongside it.

## Recommended next step for HQ

Hostile independent review of three specific claims: that the compiled reader performs zero
path opens on the broker route; that the fresh-broker-per-chunk constraint is correctly
characterised for DTA; and that R7 runtime identity genuinely does not change. Then
commission a full-corpus path-versus-broker comparison over the existing 55/55 corpus to
close the equivalence gap — before any adoption question is opened.

`HQ195_R9_RUNTIME_FEASIBILITY_RETURNED__HQ_REVIEW_REQUIRED`
