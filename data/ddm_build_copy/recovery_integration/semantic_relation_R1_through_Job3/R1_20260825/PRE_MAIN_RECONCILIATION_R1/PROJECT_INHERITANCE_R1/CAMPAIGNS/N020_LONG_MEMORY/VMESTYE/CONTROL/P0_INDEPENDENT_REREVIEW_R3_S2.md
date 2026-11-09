# VMESTYE ZL-P0R — R3 independent receiving of local S2 return PR #826
Date: 2026-11-08 America/New_York / source return timestamp 2026-11-09 UTC.
Formal receiving result: **REVISE — independently confirmed five lost D05 source keys; executable baseline FAIL; P0 not accepted, P1 ZL-02–ZL-14 CLOSED.**
R1 review REVISE and R2 review HOLD remain immutable earlier events. This R3 is a new event and does not rewrite prior findings.

## Exact subjects and custody
- Protected PRE-MAIN HEAD `2162d85db5e6822707e5cdff7aac2656ebef4761` (unchanged and unmerged).
- ZL-00 PR #819 corrected `11047708a6e4b4050da351f4b6cc35f03cb8269b` (draft).
- ZL-01 PR #820 corrected `3590b223c1c04df10d78b0c1df3fc2dfa2e32618` (draft).
- R2 reviewer PR #821 HEAD before R3 `a71fa746a733e9f33e220516c2a530893be8a088`.
- S2 worker draft PR #826 `8438959c4eeb4b7c8637790afe03fab1bd139c29`, branch `test/vmestye-p0-s2-qualified-validator-r1`; 29 changed files, 1982 additions, zero deletions; worker return under `WORKER_RETURNS/PROGRAMMA-VMESTYE-P0-S2-QUALIFIED-VALIDATOR-20261109-R1/`. No merge. All four PR heads and protected HEAD rechecked during receiving.
- Historical source: `b7dd1bce667651c88ddd71c17c065f2b33ec38ec::data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/LONG_MEMORY_CURRENT_ZERO_LOSS_DELTA_R1/D05_MAINTENANCE_LIFECYCLE/AUTHORITY_MAINTENANCE_FUNCTION_LEDGER.csv#blob=bf77b70f1858697ce663f2eeec2e91e25aa6ac94`; blob content and exact commit-path fetch match.
- S2 worker reports mainMac.lan / macOS 13.2.1 / Python 3.11.3 / OpenCode `opencode-go/deepseek-v4.1-flash`, effort unexposed. User dispatch of local structural S2 recorded. Independent runner credential attestation is **not claimed**. This reviewer has authenticated GitHub S0–S1 read access, not execution on mainMac; review of logs is not independent S2 re-execution.

## Independent D05 source falsifier
From the immutable source blob, independently inspected physical CSV source-key lines and original first-column `function_id` fields:
`D05-F01` through `D05-F11` each occurs once, source record ordinals 2–12. The corrected ZL-01 census blob `ace431dde03fde7aa124c351d2549b6e9b2b587b` (6,120×25) contains only the six `D05-F01`–`D05-F06` records for that exact `source_path`. Missing exact file-grain IDs:
- `D05-F07`: row 8.
- `D05-F08`: row 9.
- `D05-F09`: row 10.
- `D05-F10`: row 11.
- `D05-F11`: row 12.

This independently supports the S2 failure's source key differences: source 11 vs candidate 6 in the named file; D05 grouped candidate 24 vs source 29; 23 D02–D07 per-file candidate 364 vs source 369. At unchanged overall sourcecut the expected aggregate census increases by five from 6,120 to 6,125 once repaired, subject to re-derivation of all other rows. **A claimed no-drop source-key PASS at PR #820's reviewed head is false.**

Independent source-format qualification: the historical file itself contains irregular CSV quoting in `D05-F06` and `D05-F11`. A lenient Python CSV parser read 11 keyed records but field widths 5 rather than the declared eight on these two rows; strict CSV parsing raised `Error: ',' expected after '"'`. This was a **read-only S0–S1 source-format diagnostic**, not execution of the project S2 validator. Preserve exact historical raw bytes. Do not invent eight-field semantics/negative/status fields from malformed rows. ZL-01 needs a documented source-key/raw-row extraction rule and explicit field-semantic HOLD/owner where parse is not qualified. A repair that only changes aggregate counts without documenting this source-format anomaly is inadequate.

Machine-readable independent falsifier: `P0_S2_D05_SOURCE_FALSIFIER_R3.tsv` (11 keyed records; source SHA/blob/path/ordinal; candidate presence/absence; irregular-quote marker). It proves source identity omission, not semantic reconciliation.

## S2 report/log receiving
PR #826's complete returned files were fetched at exact immutable HEAD. Evidence includes stage/assembly/environment manifests, full baseline and bootstrap logs, execution TSV, negative fixture logs, test source and validator script.

- Historical bootstrap: worker receipt exit 0 with `BOOTSTRAP_SOURCE_PIN_AND_SHAPE_OK__FUNCTIONAL_ZERO_LOSS_UNPROVED`, frozen 18 NOT_DISPATCHED and nine NOT_RUN. The reviewer observed log and exact script source; did not rerun on host.
- Stage-aware baseline: worker receipt exit 1, `P0_S2_BASELINE_RESULT.json` enumerates **46 checks: 43 PASS, 3 FAIL**, exactly `A_SOURCE_KEYS:D05_SOURCE_PACKAGE`, `C_D02_D07_SOURCE:AJ-D05_SOURCE_PACKAGE__AUTHORITY_MAINTENANCE_FUNCTION_LEDGER.csv`, `C_D02_D07_ROWS`. All three have the independently confirmed five-key cause.
- Eight mutants: each submitted log contains its advertised **distinct expected error ID** in addition to the persistent baseline D05 errors; all eight returned nonzero exit. The test harness marks PASS if nonzero exit and expected error ID present. This is useful targeted fail-closed detection but **not a clean-baseline negative-control court**, because every mutant inherited the already-failing D05 baseline. All eight must be rerun after ZL-01 and validator count corrections on a green baseline.
- Five unit tests: worker log `5 passed in 0.03s`. This is received worker evidence, not independently re-executed.
- The assembly manifest enumerates 17 candidate files and no path overlaps; reported SHA256 `e28a1aa8f0751e8d1832b3e678498a4bf0db423ef78725a0f710578b3cdc720a`; exact local assembly reconstruction has not been performed by this S0–S1 reviewer.
- Worker reported canonical-tree CI PASS and three inherited governed-court failures; not independently reproduced here and irrelevant to the D05 source-key mismatch.

**Separate S2 implementation correction:** the newly committed `validation/validate_vmestye_p0_s2.py` at PR #826 hardcodes `len(census) == 6120` and `source_total == total == 364` (source lines around 296 and 583–585). These are now disproved denominators at the same pinned sourcecut. Once ZL-01 adds five exact rows, the validator would fail its own old-count assertions even if the no-drop comparison is fixed. The S2 owner must version/update or source-derive the denominators to 6,125 and 369 respectively, preserve exact original-source comparisons and rerun baseline/negatives. Do not weaken source-key equality to make the test pass.

## Required repairs, owners, and independent follow-up
1. **ZL-01 author (#798 / PR #820):** append exact five D05 file-grain rows with immutable commit, source path, blob, row ordinal, keyed identity, typed negative/status and explicit source-format qualification where needed; reconcile per-file anti-join expected/observed counts, grouped D05 29, D02–D07 369, aggregate census expected 6,125, receipt digests/coverage, crossrefs and narrative, without claiming five new functions. Do not change historic source bytes. Return a **new exact immutable candidate HEAD**.
2. **Local S2 validator owner (#826):** follow-up implementation on own isolated branch, replace stale 6,120 and 364 aggregate pins with independently source-derived/versioned sourcecut totals; preserve original historical bootstrap; establish a clean corrected baseline and rerun all eight mutants, capturing expected target error IDs **relative to a green baseline**. Return a new immutable validator HEAD, logs and SHA manifest.
3. **Historical D05 source-format steward:** explicitly adjudicate malformed F06/F11 eight-column field parsing (strict CSV fails); no silent authority/semantic promotion. Source-key identity may still be conserved with documented physical-row rule and negative qualification. If unresolved, retain typed HOLD.
4. **Same independent ZL-P0R reviewer:** re-read the new candidate and S2 heads, independently compare all five returned source keys/raw anomalies and revised receipt sums; receive complete clean-run evidence before any `ACCEPT_P0_SCHEMA_AND_ESTATE` decision.

## Release decision
**REVISE, NOT ACCEPT.** R2 D06 is no longer merely `NOT_RUN`: a local structural S2 return was made and documented **FAIL**, with independent source-key confirmation. The 8/8 negative results remain qualified by a failed baseline. P1 ZL-02–ZL-14 remains CLOSED. No merge to PRE-MAIN, no #777/#784/#786/#787–#790 resumption, no original35, native/S3, original respondent, scientific, authority-applied, first-consumer or current functional zero-loss claims. Independent reviewer does not self-promote.
