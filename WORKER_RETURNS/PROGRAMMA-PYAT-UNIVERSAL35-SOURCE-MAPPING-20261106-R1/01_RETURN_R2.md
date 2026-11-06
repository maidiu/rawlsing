# A — remaining source/config binding gaps — R2 return

**Job:** `PROGRAMMA-PYAT-UNIVERSAL35-SOURCE-MAPPING-20261106-R1`
**Branch:** `codex/pyat-universal35-source-mapping-20261106-r1`
**Continues:** `ef43bbbbb16ac8925056f7c5bed522d6b1200ea5`
**F review of frozen SRC31:** `df22997380d90d92a9dbf1100ae31e850ad6a0eb`
**Status:** `AUTHOR_TESTED__REMAINING7_BOUND__F_BINDING_CONTRACT_REPAIRED__INDEPENDENT_REVIEW_REQUESTED`

SRC31 correction remains byte-identical to `ef43bbbbb`; its frozen candidate is
preserved for F review. This R2 adds only the seven remaining observed
source/config binding gaps and the F-required base provenance enforcement.

## F binding-contract repair

`apply_source_config_corrections` now requires trusted loader/provider
`base_commit` and `base_config_path`, not registry self-assertion:

- no trusted provenance → no correction applied;
- exact R157 commit/path → correction applies;
- changed registry commit/path, alternate loaded path or wrong provider commit →
  `CORRECTION_BASE_PROVENANCE_MISMATCH`;
- exact restore → 31 SRC31 corrections apply.

`SourceConfigLibrary._artifact` passes the provider commit and exact indexed
relative path into the loader. `evidence_binding_contract.json` records the
wrong-commit, wrong-path and restore results. New tests cover both mismatch axes.

## Remaining seven — exact corrections

| Source | Changes | Old unbound cells | Corrected unbound | Wall | Peak RSS |
|---|---:|---:|---:|---:|---:|
| SRC32 | 86 | 28,877 | 0 | 11.2s | 110 MB |
| SRC04 | 733 | 49,868 | 0 | 18.5s | 157 MB |
| SRC16 | 2,538 | 58,697 | 0 | 6.4s | 194 MB |
| SRC24 | 999 | 274,638 | 0 | 33.6s | 203 MB |
| SRC25 | 1,086 | 819,124 | 0 | 127.6s | 320 MB |
| SRC33 | 274 | 208,850 | 0 | 32.6s | 320 MB |
| SRC26 | 378 | 305,578 | 0 | 80.6s | 320 MB |

The D prescan counts are bounded subsets; the old-unbound column here is a full
response-slot scan. SRC32/SRC04 match exactly; the others expose more cells when
all response slots are scanned. No count is silently normalized.

Correction policy per source:

- exact SAV-declared missing value/range → exact missing state, declaration and
  label-bound DK/NOT_ASKED/REFUSAL/SOURCE_SPECIFIC_SPECIAL state;
- observed code with a declared label → substantive **code-token identity** only;
- observed code without a declared label → `INVALID_UNRESOLVED`, never substantive;
- no administration, route, unit, weight, population or scientific meaning added.

All corrections remain source SHA + base canonical hash + base commit + base
config path bound. Immutable R157 configs and the SRC31 correction are unchanged.
All35 denominators remain 35 sources / 18,276 items / 18,413 slots / 18,250 joins
/ 26 unmatched; fixture identity is unchanged.

## Proof and limits

- `evidence_remaining7_boundary.json`: old config unbound > 0 for each source;
  corrected config unbound = 0 for all seven.
- `evidence_remaining7_summary.json`: per-source correction counts, old/corrected
  counts, wall and RSS.
- `evidence_binding_contract.json`: F provenance mismatch/restore proof.
- `evidence_pytest.txt`: **46 passed**.
- SRC31 selected-original-column facade proof remains at
  `evidence_src31_boundary.json`.
- Full C11 release/native facts are **NOT_RUN**; the next gate is the separate
  positive-authority `DEFER`. Coordinate binding gaps are not converted into
  response-mapping PASS.
- No respondent rows, native keys or raw source bytes were printed or committed.

## PROGRAMMA_DELTA

- **Identity:** correction registry now has SRC31 + SRC32/04/16/24/25/33/26;
  SRC31 frozen at `ef43bbbbb`.
- **Function:** source/hash/base-path-bound response-value/missingness binding.
- **Input → typed output:** exact source config + declared SAV metadata → corrected
  `SourceConfig` with `corrections_applied` → typed response states.
- **Root/schema/clock/permission:** no change; no source/native/science/actor grant.
- **Actual first consumer:** `SourceConfigLibrary.load_original` + current physical
  response projection.
- **Affected IDs:** the seven source response slots with observed gaps; no item,
  slot, join or fixture denominator change.
- **Conditional unlocks:** D can consume corrected selected columns for these
  seven; full release still awaits authority and C stream.
- **Next action:** independent review of new changes only; preserve SRC31 review.

## Independent review request

Review only the R2 delta from `ef43bbbbb`: trusted base commit/path enforcement,
the seven source/hash-bound correction entries, zero corrected unbound keys, and
the non-promotion of undeclared codes. SRC31 factual mapping is already under F
review and should not be re-litigated absent an actual F finding.
