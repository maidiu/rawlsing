# VMESTYE ZAK-Z1 — independent historical-contract receiving, R1

**Decision: REVISE_EXACT_DEFECT / HOLD T1 historical acceptance.** Source artifact: [PR #871](https://github.com/maidiu/rawlsing/pull/871), frozen author T1 R5 head `5827cdb74f6820c338b79db0c423e9e0dc88a992`. This is an independent *analytical* historical S0–S1 review, NOT a GitHub-account-distinct approving review, scientific issuance, native replay, ZL-15 adoption, or protected merger.

## Preflight and version custody

| Surface | Exact observed state |
|---|---|
| Frozen source PR #871 | open / draft / not merged; HEAD `5827cdb74f6820c338b79db0c423e9e0dc88a992` |
| T1 R4 parent | `886d8926bedbeb7bf57737aaab04cdd98ed2ba2d`; R5 is exactly one commit ahead |
| R5 differential | five modified T1 return files, no new source identities or atlas census |
| T1 PR base | `research/vmestye-zl15-master-function-join-r1@31d2642ce7667d72efc08c3f6d42a2674b10d5ea` |
| Protected PRE-MAIN observed | `integration/pre-main-reconciliation-r1@256d46bf425cc37e114465cddbe3c60e535766ab`; no protected writes |
| Independent review branch | `review/vmestye-zak-z1-historical-contract-receiving-r1`, created exclusively from frozen R5 SHA after no same-name branch was found |
| Account provenance | GitHub connection `maidiu` is also #871's PR author account; no verified separately credentialed reviewer. Review authorship is analytically separate, not externally attested. |
| Prior PR reviews | zero in live review list at preflight |
| Evidence grade | S0–S1 original code and exact TSV readbacks only; original Python/DB/survey, node self-tests, source-cut Git-clone replay, S2/S3 and native pipeline tests **NOT_RUN** |

The reviewer did not modify the author branch. Its historical source anchor is original PRE-MAIN `9253064bc9423a0f0ccda4fbdea43c2f54f800c6`, with pinned original file blob SHAs as below.

## Exact material defect ZAK-Z1-D01 — V549b normal-reporting path fails

**Original file** `data/ddm_build_copy/build_question_response_attitude_cloud_summary_v549b.py` at original commit `9253064bc9423a0f0ccda4fbdea43c2f54f800c6`, blob `bf874a95ea5172817b0d1bdf21b43600aac5cbfe`.

At lines **604–611**, inside `build_answer_presence_anchors`, when `reporter is not None` and `other_index % PROGRESS_ITEM_STEP == 0`, the message f-string evaluates `answer_type` (line 607). **There is no assignment of `answer_type` in this function or module-level binding of that name.** The candidate item variable `cand_item_id` is read at line 608 before the current iteration assigns it at line 611. `PROGRESS_ITEM_STEP=50` (line 56). Thus whenever an eligible literal presence/absence anchor enters the inner candidate scan of 50 or more candidates with a reporter, iteration 50 raises `NameError` before a score/output row can be completed for that anchor. Earlier accepted rows in memory do not make the function return.

At lines **565–570**, the outer progress message likewise reads `item_id` and `answer_code` before assigning the current `item_id`; it can display stale values or, on certain prior-iteration paths, encounter an unbound name. The inner `answer_type` bug alone establishes the hard failure path.

`main()` creates `reporter = ProgressReporter()` and invokes `build_answer_presence_anchors(..., reporter=reporter)` around original lines 845–950. `get_candidate_registry` returns the eligible filtered merge without a top-49 cap (lines 378–406). This exception is therefore reachable under source-grain preconditions, although **no original survey fixture or actual source run has been executed here**. It is not a claim that all historical V549b runs failed.

**R5 contract impacted:** `T1R2-V549B-PRESENCE` currently reports appropriate literal anchor/complement semantics, but its `output_guarantee` and `negative_refusal` omit this reachability-dependent hard exception. The `D23_V549B_TEXT_ABSENCE_NOT_ANCHORED` finite delta describes comparator/falsification but not the progress-error path. A bounded exception is materially different from a low-support omission, ordinary scoring suppression or typed refusal. Therefore T1 cannot be received as a complete historical transformation contract at the source cut.

**Required author correction:** preserve the existing R5 comparator fields; add a separately typed progress-exception branch and its conditions to the same V549b transformation contract, with a faithful output guarantee, failure/refusal semantics and original-run uncertainty. Extend the finite delta (existing D23 or one additional exact bounded row) to name the source, owner, earliest falsifier and stop. Do not mutate original code or issue source/scientific authority in T1.

**Earliest falsifier:** at the pinned code, a sourcefree in-memory fixture with at least one `multi_select` or `split_block` literal `1`/ `0` anchor meeting `MIN_ANCHOR_N=50`, `len(candidate_items)>=50`, nonempty `source_wide` and a non-null reporter; enter the 50th inner candidate iteration and record the specific exception. A `None` reporter is a control and need not fail. This fixture was not executed by ZAK-Z1. Stop when corrected contract and actual bounded reporter/no-reporter witness are reviewed or register a clearly typed `NOT_RUN` limitation.

## Independently corroborated source semantics (bounded, not complete 52-row adjudication)

| Family | Pinned code evidence | Receiving finding |
|---|---|---|
| V549b answer/comparator | `build_question_response_attitude_cloud_summary_v549b.py@bf874a95` L257–284 and L565–645 | Only literal `1`/`0` give anchors. Cramer's V joins Boolean anchor mask with candidate variable and `dropna()` discards candidate nulls; anchor nulls are in False comparison when candidate is present. R5 comparator correction **CONFIRMED**. |
| V552 pressure / overcount | `ddm_v552_structural.py@0df56d70` L130–185 | `_surface` emits `BLOCKED_RESPONSE_CATEGORY_COUNT_EXCEEDS_DENOMINATOR` for category sum over shared respondent denominator; score and `ALLOW` branch does **not** gate on `sel`. `_class` falls to `selected_response_surface_pressure` for overcount. R5 static correction **CONFIRMED**, policy still unissued. |
| F08 manual override conflict | `ddm_v550_question_use.py@8d90a511` L1106–1186 | Multirow on one selector basis or conflicting rows across bases raises `RuntimeError`; it does **not** itself write a review row. R4 correction **CONFIRMED**, caller persistence unproved. |
| V551 neutral and adjudication | `ddm_v551_atoms.py@d07e9a0c` L89–166 | For certified direction neutral, `_signed_projection` returns neutral/0 before directional geometry. This is **after** registry loading; eligibility prefilter excludes missing/special/inapplicable rows, while eligible candidates are adjudicated separately. R4 correction **CONFIRMED** at static code-path grain. |
| V551J target gate | `ddm_v551j_packets.py@740bae4c` L1410–1465 | Target status can certify through all-resolved components OR qualifying relation signature OR positive `registry_resolved_share`; it does not mean all component mappings resolved. R4 correction **CONFIRMED**. |
| V552J join | `ddm_v552j_handoff.py@476e6173` L55–142 | Scope equality is not full structural equality; score >=5 can resolve a partial match, >=8 an exact match; sorted first match has no explicit tied-score ambiguity refusal. R4 correction **CONFIRMED**. |

A source-body `ALLOW`, `CERTIFIED`, or historical selected release is **not** accepted native source authority or safe current consumer permission. In particular, whether a successor should reproduce V552's overcount+ALLOW inconsistency is **issuer/T2-owned and HELD**.

## Inventory preservation and anti-omission challenge

Independently read back T1 R5 TSVs at the frozen head:

- `HISTORICAL_TRANSFORM_CONTRACTS.tsv`: **52 records** / 38 columns, no ragged records.
- `R1_CANDIDATE_FATES.tsv`: **235 unique candidate rows** / 23 columns. **148** retain `NONE__NOT_PROMOTED` rather than pretending to have an inverse transformation; **87** carry some candidate references, of which **seven** have strict same-static-branch alignment. Candidate reference does not imply proven equivalence.
- `C6_SELECTED_AUTHORITY_EVIDENCE.tsv`: **94 records** / 31 columns. These are historical selected-release evidence, not observed original invocation.
- `SOURCE_RECORD_TO_TRANSFORM.tsv`: **10,348 unique source_record_key identities** / 14-column header. A full GitHub contents read was required because the line-limited file action returned no body for this large TSV. The last row has trailing empty fields; do not misdiagnose it as source-record loss.
- `INHERITED_OBLIGATION_FATES.tsv`: **44 LMX + 30 LMQ = 74** independently named obligations/resources, not 74 executed transformation functions.
- `FINITE_ESTATE_DELTA.tsv`: **27** previous finite delta rows, D01–D27. ZAK-Z1-D01 is a *review-only requested delta*, not an unauthorized edit to the frozen T1 file.

High-impact anti-alias challenges are enumerated in `02_FATE_CHALLENGE.tsv`: J conditional input handed to V552 but unused; reduced V553 temporal/field authority; F16 joint-component scalarization; F17 respondent risk set and cache parity; Chetiri risk-set NOT and same-respondent joins; cache-delete replay; adaptive discovery tie/stop; old F22/F23/F24/F28 identities. **All remain typed source/issuer/first-consumer holds**, not inferred lost capabilities or unproblematic replacement functions.

The frozen 74 obligations remain individually tracked in `03_LMX_LMQ_NO_DROP.tsv`. Special high-impact `LMX-043` remains a required atomic stage→promotion / failure→rollback / restart→idempotent replay transition, **not** a proven native function. LMQ-001 whole-system re-court, LMQ-002 V550J production authority, LMQ-003 exact routing predicates stay open.

## Receiving disposition and stop

**REVISE_EXACT_DEFECT** for frozen T1 R5 historical contract acceptance; **no retrospective rewriting** of R4/R5 author history. R5's two corrected central source semantics are preserved as independently corroborated *static* facts. The exception path means it is premature to accept V549b's complete output/refusal contract. This is a narrow, repairable defect, not a mandate to recensus 10,348 records or invent another engine.

Required follow-up: author adds the conditional source-exception semantics at T1 and repairs its finite delta; independent nonauthor reviewer checks the corrected exact HEAD. VMC-T2, scientific issuer, original authority selection, native respondent runtime, Pyat/Sorok first reader and ZL-15 receiving remain separate gates. Do **not** merge protected PRE-MAIN or promote S0–S1 to S2/S3/native proof.

**Reviewer boundary:** exact GitHub author account equals the connected credential (`maidiu`), so this report is not evidence of a credential-independent GitHub reviewer. If organizationally distinct review is mandatory, a different credential/authorized reviewer must perform that gate.
