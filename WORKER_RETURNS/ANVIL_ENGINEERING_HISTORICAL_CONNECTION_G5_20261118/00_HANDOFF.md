# Historical → current shared computation — source-accuracy G5

**Decision:** `REVISE_EXACT_DOCUMENTARY_DEFECT`  
**Reviewer:** `ses_e30a442d8ffeYBbXi7rPUpPxoc`  
**Author correction:** `56eb6d084070e4a177809902909d636b0b215c6f`  
**Product:** `68aa7cac…` unchanged; no product/native execution

All six cited old-file SHA-256 values match the frozen local files; all four cited current-file SHA-256 values match the frozen 68aa snapshot. The issue is documentary accuracy, not the local hash match.

## Material corrections

1. **Old prepared substrate is LONG, not wide.**  
   `PREPARED_SUBSTRATE_REQUIRED_COLUMNS` contains `var_code`, `var_code_norm`, `question_id`, `response_value`, `response_value_normalized`, `response_label`, etc. There are **62 prepared + 5 additive = 67 required columns**, not 68. There are no one-row-per-respondent × question-name columns. The artifact `row_count=25067` is **long respondent×variable rows**, not respondent count. The repeated “wide respondent×variable” description and the causal claim “old wide / current long causes cost” are therefore unsupported. Both old and current preparation are long-form; the supported distinction is persisted preharmonized country substrate + DB-free load versus current canonical 13-family estate + per-query routing/object resolution.

2. **The frozen manifest lists 26 output paths, not 22.**  
   `shared_respondent_substrate_mode=write` and one shared substrate with row_count 25,067 prove the writer produced the substrate. The output list is writer-configured output evidence; it does **not by itself** prove each of those products consumed the substrate. Actual V550J load/cache code provides consumer-path evidence, but that is separate from the list. Correct the 22 count and label consumption honestly.

3. **babb256 is not a proven Git file identity.**  
   `babb256` is an artifact-bundle header/commit label. The local Rawlsing tree is not a live Git checkout for all cited files. Correct source grade: **LOCAL_SHA256_ONLY / BUNDLE_HEADER_IDENTIFIES_COMMIT**; no invented Git blob.

## Supported factual connection

- Old PostgreSQL extraction and one-time country harmonization are real; the resulting long prepared substrate is persisted with manifest/validation/COMPLETE and can be loaded without reharmonization/DB access.
- Current 68aa has a canonical long 13-family estate, temporary SQLite `members(family,respondent,ref,gid,off)` / `members_resp_idx`, one index build per prepared context, no query-independent routing selector, and only exact-core grouped reuse.
- A session-local query-independent routing/target selector over the existing members index is a supported **INFERENCE/candidate**, not a forced unique architecture. A persistent long prepared-country substrate is a broader representation decision; the old evidence does not establish a wide one-row-per-respondent frame or force that option.

I do not choose selector vs persistent substrate, authorize a production patch, or promote source/science/actor/CURRENT/protected authority. BrowserHQ/user must decide whether the narrow selector inference is sufficient or whether the broader persistent long prepared-country substrate is required.

No new history inventory, native query/build/benchmark, raw respondents, product edit or new architecture campaign. The correction needed is limited to the historical handoff/machine descriptions: long not wide; 67 not 68 columns; 26 not 22 output paths; writer-configured vs actual-consumption wording; local-hash source grade.

Evidence: `sourcecheck.json`, `REVIEW_RECEIPT.json`.
