# PYAT P0 — prepared cold saved C11 session (TEST_ONLY candidate)

**Status:** `IMPLEMENTATION_MEASURED__SOURCEFREE_TEST_ONLY__OWNER_GRANT_PENDING`.
No protected merge, no production reader/evaluator edit, no original-source or
scientific permission, no self-G5.

**Base:** `b830458c3ebfe0a3f0e2d18e516e68b90324c88a` (#997 R03/W05 corrective,
which already contains accepted #999 native body-truth and W05 physical-order
traversal). **Branch:** `implementation/pyat-p0-c11-operable-20261115-r1`.

## What now executes that previously did not

The cold saved reader opened a new `DirectEstateI03Session` for every operation,
rebuilding the complete SQLite posting index from all event-locator/event-body
and side-family row groups each time (J5 measured 100 session builds for 100
distinct operations; cold grouped execution was explicitly refused).

The new additive `rawlsing_next/pre553_prepared_saved_i03.py` exposes
`PreparedSavedC11Admission.prepared_i03()`: one exact authenticated S2-C
session/index is reused across many I03 operations and I05 discoveries. It
retains the existing native evaluator, catalog resolution, query/predicate
scope, exact condition check, release binding, current/revocation checks,
body-truth checks, fact/replay construction and typed negative states. No
existing production file was edited.

## Changed files

- NEW `rawlsing_next/pre553_prepared_saved_i03.py`
- NEW `rawlsing_next/tests/test_pre553_prepared_saved_i03.py`
- NEW `WORKER_RETURNS/PYAT_P0_C11_OPERABLE_20261115_R1/` (return, probes,
  evidence)

## Actual results

### A. J5 128-respondent / 5-question estate, 100 distinct operations

Same estate, catalog, operations, evaluator and host; only session lifetime
differs. Each mode ran in a separate fresh process.

| | baseline | prepared |
|---|---:|---:|
| wall | 213.456 s | **126.424 s (1.69×)** |
| session builds | 100 | **1** |
| session build seconds | 63.004 | **0.412** |
| row-group reads | 28,076 | **17,384** |
| process-tree RSS peak | 97,558,528 B | **89,079,808 B** |
| temp SQLite peak | 1,703,936 B | 1,703,936 B |
| exact fact parity | 100/100 vs prepared | 100/100 vs baseline |

The baseline facts equal the accepted J5 `cold_100ops` receipts exactly
(100/100), whose independent review reproduced 100/100 native-oracle parity.
The prepared run equals the baseline on fact ref, full fact SHA-256, typed
state, raw/weighted support, replay ref and release refs.

### B. Realistic-width synthetic estate, 64 respondents × 30 questions

1,638 events (25.6/respondent), 1,920 routing facts, 64 valid weights, sparse
responses and a conditional cohort predicate; 20 distinct operations include
raw and governed-weighted 1/2/3-target queries. Writer construction:
**29.954 s** plus 3.196 s fixture, **39,609,311 B retained**. Cold admission:
0.423 s; prepared session build: 2.403 s; first query: 1.587 s.

| | baseline | prepared |
|---|---:|---:|
| wall (20 ops) | 142.996 s | **83.873 s (1.70×)** |
| session builds | 20 | **1** |
| session build seconds | 60.804 | **2.763** |
| row-group reads | 121,882 | **71,304** |
| process-tree RSS peak | 263,856,128 B | **162,922,496 B** |
| temp SQLite peak | 4,706,304 B | 4,706,304 B |
| exact parity | 20/20 vs prepared | 20/20 vs baseline and native oracle |

All 20 facts are `SUPPORTED`; both RAW and GOVERNED_WEIGHTED are present. The
in-memory native oracle comparison is 20/20 exact on fact ref, full fact
SHA-256, state, support and replay.

### C. Prepared I05

A prepared session executed the accepted S1-E discovery authority with the same
session; 8/8 discovery receipt refs and the evaluated-frontier ref equal the
baseline. See `test_prepared_i05_reuses_session_with_exact_discovery_parity`.

## Tests

- NEW prepared-session tests: **3 passed** (index reuse/parity, revocation and
  condition refusal, prepared I05 parity).
- Focused regression: **80 passed** across prepared, R03 v2, W05, S1-E saved
  native/source/body, direct-estate, grouped-I03 and saved-admission suites.
- No failures. No C11Repository or whole-table tripwires in either benchmark.
- No source reopen; the sourcefree estate was reopened in a fresh process.

## #1097 / #960 status

The #1097 register text is not present in this checkout or remote refs; no new
register was created. The measured status change is limited to the C11
physical-substrate/repeated-operation capability class:

- Prepared cold saved execution: `UNMEASURED_HYPOTHESIS` (J5 Option B) →
  `SOURCEFREE_MEASURED_CANDIDATE`.
- Repeated distinct operations over one authenticated estate: now one index
  build per process instead of one per operation; exact parity.
- Cold reopening: one admission open plus one session build per process,
  measured; persistent cross-process index remains unimplemented.
- Conditional populations, raw/weighted measures and 1/2/3-target operations:
  exercised at the wide synthetic scope; not a new scientific issuance.
- Country-level shared preparation, persistent index, and 100k/6 GiB
  qualification remain unchanged gaps. No other #1097 area is reclassified.

## Remaining defects / owner dependencies

1. Reader/index is execution-local: a fresh process still rebuilds the posting
   index; no persistent cross-process index contract or crash-interruption
   recovery has been implemented or measured.
2. The new prepared API is additive candidate code; S2-C/S2-D reader owner and
   semantic evaluator owner grants are not on record. This is not a protected
   or production reader.
3. Wide and narrow estates are synthetic TEST_ONLY, not SAV/DTA original source
   or original wave/country data. No source/science/CURRENT/N11 promotion.
4. Writer construction remains expensive (29.954 s for 39.6 MB; prior 100k
   writer 3,033.723 s). No writer repair was made in this pass.
5. 100k / 6 GiB was not rerun; the prior #1006/#1036 measurements remain
   observations at their exact cuts, not this candidate's production speedup.
6. Only session-level close/reopen and revocation/restore were tested; process
   kill and durable interrupted-operation recovery are not demonstrated.

## Review readiness

The new module, its tests, probes and exact evidence are ready for independent
adversarial review at sourcefree TEST_ONLY scope. They are not ready for
protected adoption, original-source/science use or a production performance
claim.
