# C1 reporting corrections

**Review source:** independent cut `753ff5dc95fb218f84ebf1697a91a2d392367f2c` (content `6bb88792a74c96645df4fa83948ee9de3272be54`).
**Review verdict:** `ACCEPT_WITH_REPORTING_CORRECTIONS`.
**Author cut corrected:** `a98299e7c9cd05aa3eabe2c22d20ea6b746ea667` (historical cut retained).
**Core verdict retained:** `FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED`.

This file maps the review corrections to reporting edits. No new investigation, no repeat of the 97/8 suites, no production/C11/runtime/test change, and no new authority gate or forced restoration was made.

## Correction map

| Review ID | Correction applied | Files/fields changed | Proof limit retained |
|---|---|---|---|
| C1R-08 | Q86 is described as a **sourcefree canary/candidate** operation, not an actual present/current non-test operation. No non-test first consumer is proved. `B5:O17` is a register entry, not demand evidence. | `00_RETURN.md` FINDING/ACTION/interpretation; `01_CASES.jsonl` and `02_CASES.tsv` `CASE_SCOPE`, `B`, `F`, `H`, `CURRENT_EFFECT`, `STAGE`, `PROOF`; `03_TEST_RECEIPTS.md` §2/§4; `05_REGISTER_ANTIJOIN.tsv` O17/A12/A13/P04 match roles and notes | `wave1_gt12_a2_real_gt1.execute_and_replay_a2_gt1` and Q86 plan calls are test-imported only; no non-test caller proved. Preserve `UNPROVED`. |
| C1R-09 | FF wording changed to **FF producer candidate; no demonstrated non-test Q86 joint caller**. | `00_RETURN.md`; case `CASE_SCOPE`, `B`, `D`, `REVERSE...`; `03_TEST_RECEIPTS.md`; `05_REGISTER_ANTIJOIN.tsv` A12/A13/P04 roles | `produce_exact_conditional_support_profile` exists; no non-test Q86 joint fact caller. Do not call it an existing consumer. |
| C1R-10 | Removed the mandatory “bind AR-0033 hashes or retire” remedy. AR-0033 is `HISTORICAL_ONLY__CURRENT_PROTECTED_PATH_ABSENT`, `ISSUER-HOLD-AR-0033`, `RESTORABLE_AS_HISTORICAL_PRODUCER_INPUT`; it cannot be reinstated as per-query runtime authority. | `00_RETURN.md` ACTION/J; case `A`, `J`, `OWNER_ACTION`, `REVERSE...`; `04_MINIMAL_OWNER_ACTIONS.tsv`; `03_TEST_RECEIPTS.md` NOT_RUN | First establish non-test demand; if none, canary/historical-only. If demand exists, source owner decides; only then bind/no-build/retire at true owner. No forced restoration. |
| C1R-11 | Added the real code-created candidate substitute `GT12-A-R5-Q86-SOURCE-SEMANTICS` at `wave1_r5_q86_c11_projection.py:334`, operation `R5_Q86A_Q86B_NATIVE_RESPONSE_SEMANTICS`; competence/provenance UNPROVED, not disproved. | `00_RETURN.md`; case `B`, `C`, `D`, `E`, `G`, `REVERSE...`; `03_TEST_RECEIPTS.md` §4; `probes/q86_source_semantics_probe.json`; `04` | Literal AR-0033 hash absence alone is not severance; candidate substitute not assessed. No equivalence/adoption claim. |
| C1R-12 | Qualified `context_only` / `recommended_computation=none`: it does **not** by itself demonstrate a raw-count ban. Raw counts may be consistent with source-native context; source-owner decision remains. | `00_RETURN.md`; case `A`, `D`, `G`, `J`; `03_TEST_RECEIPTS.md` §4; probe JSON `context_only_does_not_ban_raw_counts`; `04` | No response-option structural computation is inferred as mandatory; no historical packet reinstatement required. |
| C1R-02 | Added the precise status split: substantive 0/1 rows are `curated_packet`; special -1/9/997/998 rows are `curated_special`. | Case `A`; probe JSON per-variable `response_semantics_status_counts`, `substantive_rows_status`, `special_rows_status`, `special_codes`; `03` §4 | Raw CSV bytes/rows unchanged; status summary corrected only. |
| C1R-13 | Core verdict retained exactly. | `00`, `01/02` `VERDICT`, `04`, `05` | `FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED`; not upgraded to severance/equivalence. |
| C1R-14 | Next operation corrected to demand-first / candidate-substitute assessment / owner decision. | `00` ACTION; `04` ACTION; case `J`; `03` NOT_RUN | Preserve 212-row anti-join and all unmatched IDs; no whole-estate completeness claim. |

## Preserved supported findings

- C1R-01: AR-0033 CSV identity/bytes/SHA exact.
- C1R-03: current Q86 source anchors and 8/8 direct sourcefree tests pass; 97/97 inherited suite separate.
- C1R-04: no literal AR-0033 Q86 contract hashes in current `rawlsing_next`; absence alone is not severance.
- C1R-05: selected-row version/shadow/withdrawal/cold-restore `NOT_RUN`.
- C1R-06: generic T01 remains a distinct held owner control; no C11 repair/requalification.
- C1R-07: 212 register rows preserved = 17 matched + 195 unmatched; no whole-register completeness claim.

## Historical evidence handling

- The prior raw logs under `logs/` are retained unchanged. The old `logs/q86_source_semantics_probe.log` contains the pre-correction wording and is explicitly treated as raw history.
- The historical probe JSON is retained at `probes/historic/q86_source_semantics_probe.a98299e7.json`.
- The current `probes/q86_source_semantics_probe.json` keeps the raw observed CSV bytes/row fields, adds the status split, candidate-substitute status, literal-absence caveat, and a `historical_overclaim_superseded` block with the original finding. Raw bytes were not rewritten.
- The `a98299e7` Git cut remains the historical author cut; this correction is a reporting-only successor.

## Mechanical validation

- `01_CASES.jsonl`: one valid JSON object; 30 fields; `VERDICT` preserved.
- `02_CASES.tsv`: header + one row; 30 columns; A–J fields present; all rows same width.
- `04_MINIMAL_OWNER_ACTIONS.tsv`: header + one row; 11 columns; no mandatory AR-0033 runtime-binding/retirement command.
- `05_REGISTER_ANTIJOIN.tsv`: 212 data rows + header; 10 columns; register counts `B5=27`, `F1=29`, `748=30`, `FF26`, `FFdep16`, `postFF15`, `postFF11`, `AR58`; matched 17, unmatched 195.
- Probe JSON parses; selected CSV SHA still `305cb...`; Q86 row hashes still `e3750a...`/`d16ff20...`; contract hashes unchanged; status counts add 2 substantive `curated_packet` + 4 special `curated_special` per variable.
- Mechanical validation log: `logs/reporting_validation.log`, SHA-256 `5bc14225a76fb4209b612aef39ffde31388881793b22467f461cfadf7a621eed`; result `REPORTING_VALIDATION_PASS`.
- No production/C11/runtime/test/HQ/peer/protected write; no respondent/SAV/DTA/DB read; no native/science/actor effect.
