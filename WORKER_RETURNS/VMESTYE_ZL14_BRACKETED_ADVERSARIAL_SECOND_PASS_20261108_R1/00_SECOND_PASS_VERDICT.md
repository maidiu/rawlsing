# VMESTYE ZL-14 — bracketed adversarial second pass

**Disposition: REVISE #843 at exact head `c2090501619e5927696d032a33bff93485167b89`; NOT independent-agent acceptance.** This was deliberately separated into a review branch and source-first recourt, but it is **the same assistant/model context**, not a separately launched model/human reviewer. Consequently this return MUST NOT be represented as the commissioned independent I3+ acceptance for #847 or a VMESTYE ZL-15/16 receiving gate.

## Source read and exact identity result

- Protected starting state: `integration/pre-main-reconciliation-r1@9253064bc9423a0f0ccda4fbdea43c2f54f800c6`, candidate PR #843: `c2090501619e5927696d032a33bff93485167b89` (draft, unmerged at inspection).
- **Recovered and parsed the complete physical P0 census** via authenticated GitHub Git blob `65c1bbe4a602341c5caacca2d58dced31a23f382`: **6,125 data records, 25 columns, zero row-width deviations**; `P0_RETURN_AND_BRANCH_CENSUS.tsv` on protected at pinned cut. GitHub `fetch_file` returned 0 content for large file, but Git blob fetch delivered **5,371,334 UTF-8 characters**. This is not an absent-source or missing-permission case.
- **30/30 recent RM original P0 records:** `ZL01-000808`.. `ZL01-000837`, `estate_id=RECENT_CAMPAIGN30`, source `99384d8dc7bb4ec4b492f8cf8d409d3332e8e801`, blob `37c611aa3a2dc363603186f7144e5cdf88762011`, canonical `source_composite_id=[\"RMNN\"]`, `record_grain=record_id RM01..RM30`, `tsv:2..31`.
- **13/13 historical D06 source-package original records:** `ZL01-006003`.. `ZL01-006015`, `estate_id=D06_SOURCE_PACKAGE`, commit `93e84b084f14db2db410cbad5555e7820507d4d9`, blob `dd7639838cd8f54ff4b8925c0ddb015be423c560`, canonical `source_composite_id=[\"CURRENT_STRANDED_CAPITAL.csv\",\"SC-NNN\",physical_record_number]`, `record_grain=strand_id`, `csv-record:2..14`.
- **43 unique exact P0 census IDs located, 0 absent or ambiguous among these 43.** These are 43 *locator/source records*, NOT 43 distinct semantic operations or native-function successes. Table `01_...` gives every authoritative tuple and candidate mismatch.
- The candidate `COVERAGE.tsv` and `UNJOINS.tsv` label the 43 census joins unresolved, though exact P0 identities exist. Across 43, its bare composites and grain differ from the original. All 30 RM rows use protected `9253064bc9423a0f0ccda4fbdea43c2f54f800c6` instead of the P0 source commit for the five-key join. All 13 SC rows use synthetic estate/grain distinct from P0. Exact joins can be corrected **without** asserting any new first-consumer acceptance.

## P0 ↔ current distinct cut

Protected-current `CONTROL/RECENT_CAMPAIGN_INTAKE.tsv` has blob `989321a982c003615aa6cb3f9d21b59f10254f9d`, which is **not** the P0 census source blob `37c611aa3a2dc363603186f7144e5cdf88762011`. The 31-line current version differs on exactly **four data rows: RM09, RM23, RM24, RM30**. RM09 now references independently reviewed R5C D2 material REPAIR; RM23/24 show Pyat/Sorok SR01 source returns (not independent operational receiving); RM30 says protected documentary scaffold, not functional acceptance. Preserve older census identity and newer currentness, not one as surrogate for the other.

## Cross-table scope and substantive limits

PR #843 six TSVs contain 24 FINDINGS, 18 OPERATION_TRACES, 10 AUTHORITY_USE, 24 EVIDENCE, 43 COVERAGE, 53 UNJOINS. Visible local TSV widths and referenced finding/trace/evidence IDs are syntactically consistent: **0 local FK errors in this pass**. But their semantic dispositions are CANDIDATE, and the 10 `UJ_SEM` questions remain distinct from P0 lookup.

Direct source re-reads: R9 R5C independent source verdict `b8df0fa...` explicitly `REPAIR` because F14 response sign and usable/support fields are unbound to actual F13-producing membership (S2 not run); GF1 #691 exact candidate module declares `TEST_ONLY`; PR786 source layer itself states original execution `NOT_RUN` and PR is draft **base=main**; R8 #774 is frozen Q86B/Q86A source-identity code unmerged; PR770 remains open/unmerged. Current exact statuses of PR691, #770, #774, #786, #764, #692, #705, #709 checked at invocation; #709 merged documentary, #705 closed unmerged, neither entails unrestricted original35 semantic admission.

**No S2 tests were executed.** Authenticated GitHub source/metadata and deterministic in-tool TSV parsing only (S0–S1). No S3, no original respondent source, no science/human issuer, no protected edits, no current-source rights grant. Keep FIABC 144 PASS/3 FAIL, D05 F06/F11 holds and all paused campaigns unchanged.

## Bounded correction and receiving

PR #843 should be corrected by the original author for D1–D4 and scoped claim grades; the corrected head must then undergo **genuinely distinct** hostile re-review for the remaining operational/signed/permission cases. This second-pass return supplies independent-looking adversarial evidence **but not personnel/model independence**. Its output is a repair court, not an ACCEPT_SCOPED certification. #847 remains the commission if true independent receiving is required.
