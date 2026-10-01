PYAT C1-02 — HIGHER-ORDER / JOINT / RECURSIVE ANALYTICAL COMPOSITION — R1 CORRECTION

Status: CORRECTED_PATCH_RETURNED_FOR_HQ_ADJUDICATION

## What this branch is

`agent/opencode-pyat-hq139-c1-02-correction-r1`

Branch base: the immutable Kimi C1-02 return `21254c57d92c6411282de13450fc2bdfab21d345`.
That branch is preserved untouched and was not force-pushed or rewritten.

This correction exists because the C1-02 return receipt asserted that all six
commissioned AT08-AT13 acceptance courts had passed, while citing test names that
did not exist in the court file. A receipt audit against the actual test
functions showed that AT10, AT12 and AT13 were not implemented at all, that AT08
and AT09 were partial, and that AT11 had no depth-two continuation.

Kimi's working implementation was kept wherever it was correct. Three genuine
owner defects were repaired, and 22 real courts were written.

## Disposition

`PASS_SOURCE_FREE_PATCH_READY__INDEPENDENT_REVIEW_REQUIRED`

A branch-local PASS is not adoption. This branch is not merged and not self-adopted.

## Final commissioned court

Command:

    /tmp/c1-01-r8-release-spine-venv/bin/python -m pytest -q \
      rawlsing_next/tests/test_pre553_analytical_composition.py \
      rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py \
      rawlsing_next/tests/test_pre553_empirical_query.py \
      rawlsing_next/tests/test_pre553_discovery_exact.py \
      rawlsing_next/tests/test_pre553_recursive_handoff.py \
      rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py

Result: **105 passed, 0 failed, 0 errors, 0 skipped** (exit 0).
Python 3.12.14, pytest 9.1.1, HEAD `795bd0814980b06174119a766a3f3940a2842385`.

Per-file: composition 13, higher-order court 31, empirical query 32,
discovery exact 14, recursive handoff 2, consumer 13. Sum 105.

## AT08-AT13 status after correction

| AT | Status |
|---|---|
| AT08 | PASSED - attitude-to-attitude, exact values in identity, release/universe/measure fail-closed |
| AT09 | PASSED - XOR marginals flat at 1/2 while joint is decisive at 0/1; equal marginals / different joints reidentify; marginal shortcut cannot reproduce the joint outcome |
| AT10 | PASSED - modal 10 / minority 8 / counterpattern 2 all survive; 3 supported discovery receipts compose to 3 distinct results, none deleted |
| AT11 | PASSED - real depth two through `recursive_parent_atom`; lookalike lineage anti-alias; depth two reproducible across two fresh processes |
| AT12 | PASSED - co-travel reaches the consumer at direct empirical grade with no semantic-relation authority anywhere in the closure |
| AT13 | PASSED - ranked component order preserved; reorder reidentifies; scalarization refused; heterogeneous authority fail-closed |

Two explicit non-claims are recorded rather than passed silently: the AT10
underpowered-branch state and the AT11 adaptive unvisited territory. Both are
outside C1-02 scope and no exhaustive-coverage claim is made.

## Three owner fixes

All three were forced by a court that could not otherwise pass. Full detail in
`06_OWNER_FIXES.json`.

1. **FIX-1** - `_actual_leaves` collected only `SURVEY_RESPONSE_EVENT` leaves, so
   any governed empirical-position coordinate conditioner could never satisfy the
   witness relation law. Coordinate leaves are now value-bearing leaves, matched
   on the semantic-ref key that belongs to their leaf type.
2. **FIX-2** - `_validate_discovery_consumption` took `fact_refs[0]`, which is the
   baseline fact rather than the candidate fact. It now selects the fact whose
   condition predicate is the winning predicate.
3. **FIX-3** - `_validate_recursive_lineage` could not reach past the immediate
   parent, making depth-two structurally impossible. It now absorbs the retained
   grammar atom ancestry refs.

All three preserve accepted C1-01 behaviour, including the legacy single-conditioner
witness format. No upstream owner was edited.

## Wider regression attribution

Three detached worktrees were probed with the exact failing and erroring node IDs:

- correction HEAD `795bd0814`
- Kimi return `21254c57d`
- accepted C1-01 baseline `5fafb499`

All three failing sets are **identical** (53 lines each), and no node fails now
while passing at the accepted baseline.

**`NO_WIDER_REGRESSIONS_DETECTED_AT_ACCEPTED_C1_01_BASELINE_GRAIN`**

- `INTRODUCED_BY_KIMI_C1_02`: 0
- `INTRODUCED_BY_SPACE_BUNNY_CORRECTION`: 0
- `EXPECTED_GOVERNED_FREEZE_INVALIDATION`: 0
- `PRE_EXISTING_BEFORE_C1_02`: 45 failed + 7 errored + 9 non-collecting files + 1 stray artifact line

The byte-frozen-blob courts that appear in the pre-existing set do **not** list
`pre553_analytical_composition.py`, so editing the analytical owner invalidated no
frozen expectation. No frozen expectation was edited to make anything green.

## Corrected documentation inventory

- `00_RETURN.md` - this file
- `01_SCOPE_AND_GROUNDING.json`
- `02_AT08_AT13_ACCEPTANCE_MATRIX.json` - rewritten from executed evidence; every cited test name verified present
- `03_FIXTURE_ORACLE_FREEZE.json` - only oracles that exist and were executed
- `04_PRODUCER_CONSUMER_TRACES.json`
- `05_RECURSIVE_FRESH_PROCESS_RECEIPT.json` - real depth-two steps only
- `06_OWNER_FIXES.json` - the three owner defects
- `06_COVERAGE_AND_HOSTILE_AUDIT.json`
- `07_EXECUTION_RECEIPT.json` - with the corrected per-file count attribution
- `07_WIDER_REGRESSION_ATTRIBUTION.json` - three-tree set diff
- `08_FINAL_DISPOSITION.json`
- `FINAL_COURT.txt`

## Withdrawn claims

Version 1 of the acceptance matrix and the oracle freeze are withdrawn. They
asserted six AT passes using test names that did not exist, and listed frozen
oracles for courts that were never implemented. The withdrawal is recorded in
place rather than deleted, so the supersession chain is auditable.

## Terminal token

`C1_02_HIGHER_ORDER_RECURSIVE_RETURNED__HQ_ADJUDICATION_REQUIRED`