# C15 — independent hostile whole-record review of C14

**Review:** issue #777 P7 independent nonauthor whole-record review of the C14 combined fan-in.
**Reviewer:** existing qualified C5 independent reviewer reused; not an author of C14, the HQ fan-in, C1–C13 author returns, or any implementation. Read-only over the fan-in/HQ/source evidence; only `C15_HQ_FANIN_C14_REREVIEW/` written on the existing review branch.
**Verdict:** `REVISE` — scoped accept of the immutable content counts/schema/lineage; terminal criterion 6 is a blanket hold and is not satisfied; reporting/lineage corrections required; no native/product acceptance.
**Target content snapshot:** `f42b73abf2532f9a4ea589e7f80841e15585d8e1`.
**Provenance metadata:** `ea7e878a82e2343591724433fcd6b13910602c84`.
**C8 accepted historical content:** `55fca441d1c674c256473c264cabda48f2df0e52`.
**Goal complete:** `false`. Whole #777 remains incomplete.

## 1. Reviewer independence, recorded transparently

**Actual relationship:** this reviewer authored the C5 independent review at `ea9ff9e54e2bc7c9a56a1398d172e87a8f109f03` (C5 author was a distinct session). This reviewer did not author C14, the C14 fan-in, C7/C8, any C1–C4/C6–C13 author return, or any implementation under review. C14 incorporates the C5 evidence and cites the C5 review; that prior review relationship is disclosed here and is not treated as independent re-verification of C5 by this review.

The C14 `09` request says the reviewer must be “a different session from every C1–C13 author/reviewer, the HQ fan-in author, and the C7/C8 reviewers.” That is an unsupported procedural expansion, not the user’s P7 requirement. The user requires **nonauthor independence**, not absence of all prior review experience. This review does **not** apply the “different from every prior reviewer” clause as a gate. It applies the actual requirement: nonauthor of C14/fanin/implementations, no write authority in the fan-in lease, prior relationships disclosed, and independent verification of the exact content snapshot. The 09 clause should be corrected to that formulation.

## 2. Exact content/provenance and preservation split

| Item | Value | Verification |
|---|---|---|
| C14 content snapshot | `f42b73abf2532f9a4ea589e7f80841e15585d8e1` | commit exists; parent `23a3454b8dc3a6f2824899f6d6ee3bb3a6316521` |
| C14 provenance commit | `ea7e878a82e2343591724433fcd6b13910602c84` | metadata-only child of `f42b73ab`; updates 09/00_RETURN/GOAL_AUDIT/EVIDENCE_INDEX references |
| C8 accepted historical content | `55fca441d1c674c256473c264cabda48f2df0e52` | ancestor of C14 intake base `46104b8ddf44db4d5a32e603ca9332cebbbb1f94` |
| C8 51-case canonical `03` | SHA-256 `cc4275628286f31ba3695d92910f52d639a3f2d54ca7d43852bbd9d12b614251` | preserved separately from the 55-case return |
| C14 55-case canonical/alias `03` | SHA-256 `f21823f83e6aed6a64695150bf4ed43df2e7fd88b3310ab26752476acc61a778` | byte-equal canonical/alias |
| C14 09 at content snapshot | `__C14_CONTENT_SNAPSHOT__` / `__C14_PROVENANCE_COMMIT__` placeholders | provenance commit resolves the content-snapshot reference; its own hash remains externally recorded in `C14_COMBINED_RETURN_INTAKE.json` |
| No self-hash cycle | yes | content snapshot does not hash itself; provenance is separate; the provenance commit does not embed its own hash |

The C8 51-case historical snapshot and the C14 55-case current return are preserved **separately**. The C8 51-case `03` is `cc427562…`; the C14 55-case `03` is `f21823…`. The provenance commit is metadata-only; it does not change the C14 case content. The `SEE_BRANCH_HEAD__VERIFY_GIT_REV_PARSE_HEAD` text in the provenance commit is a lineage ambiguity (branch HEAD later moves), not a self-hash cycle; it should point to the external intake record instead.

## 3. Whole-record verification actually performed

Read-only checks over `f42b73ab` (content) and `ea7e878a` (provenance), plus the C8/C9–C13 evidence:

| Claim | Verified |
|---|---|
| Case identity | **55 unique** cases; C1 1/C2 2/C3 10/C4 2/C5 7/C6 29/C9 4; no extra/drop |
| Taxonomy | **25** `FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED` + **30** `NOT_RUN`; 0 historical-only; 0 implementation-inadequate; 0 original-wired; 0 qualified-equivalent; 0 proved-severance |
| Canonical/alias | byte-equal; both SHA-256 `f21823f83e6aed6a64695150bf4ed43df2e7fd88b3310ab26752476acc61a778` |
| A–J schema | all 55 records have nonempty `A`–`J`, `forward_walk`, `reverse_walk`, `exact_hold`, `frozen_taxonomy_verdict` |
| C8 51-case preservation | all 51 historical IDs, taxonomy and A–J payloads unchanged; only `q3_supplemental`/`q3_supplemental_source` added to `C6-F03_QREL` and `C6-F08_Q_USE`; C8 `03` SHA `cc427562…` |
| Derived tables | `02` 153 rows = 55 CASE + 26 FF + 16 deps + 15 post-FF + 11 seams + 30 #748; `05` 55 rows; `01` 94; `08` 60; all `02`/`05` case IDs equal the 55-case `03` |
| Agenda | 17 A01–A17 gates present/open; 42 selected-state/16 unresolved; 50 C6 gaps; 154/1608 overlap distinct |
| C9 evidence | 4 C9 cases; C9 cases SHA `e05ed087…`; P1 boundary ledger `09964387…`; review `d56b499e…`; 4/4 API ops/facts/receipts; wrong SHA 0/4; typed wrong host/purpose; restore exact; 840 candidate admitted; PDEV01 210/210 COMPLETED/SUPPORTED; 630 typed refusals; I05 16/30/16; empty C11 expected negative |
| C10 evidence | 18,518 rows/35 active waves/9 family witnesses; trace SHA `53c2b4ed…`; original historical run `NOT_OBSERVED`; current F03 selection `UNPROVED` |
| C11 evidence | one GSS/1973/`uswar` row; trace SHA `6a23bf6a…`; positive `1c78a386…`; contract `6c94c7a8…`; original run `NOT_RUN`; current QUC succession `UNPROVED` |
| C12/C13 | maps `5067649b…` / `66e7ee95…`; 6/5 rows; limited responsibility comparisons; no QUC/F03-equivalent producer→selector→consumer; no selected current operation |
| C8 provenance | C8 review `356124ee…`, focused check `77a879822…`, C8 reference residual closure `0e0997213…`; C8 accepted content `55fca441…` |

The detailed machine-readable report is `logs/verify_c14.json`; the human log is `logs/verify_c14.log`.

## 4. Terminal criteria — judgment

| # | C14 audit status | C15 judgment |
|---:|---|---|
| 1 | `SATISFIED_AT_BOUNDED_DECLARED_SCOPE__NOT_GLOBAL_MACHINE_COMPLETENESS` | **PASS_SCOPED.** 55 cases, bounded registers, A–J complete, C8 51-case preservation, C9 append, no global machine claim. |
| 2 | `NOT_SATISFIED__TYPED_HOLD` | **NOT_SATISFIED__TYPED_HOLD__CORRECT.** The C9 API, PDEV01 210-DIST and C2 joint are sourcefree/test-only/fixture evidence, not a genuinely demanded non-canary selected operation; the exact blockers are real. This is not a new science gate, not a retirement, and not authority to halt eligible existing-owner tests. |
| 3 | `SATISFIED_AT_ZERO_FULL_EQUIVALENCE_CLAIMS__NO_EQUIVALENCE_ACCEPTED` | **LIMIT_ONLY.** Zero equivalence claims are a limit, not product positive proof. Relabel as a limit. |
| 4 | `SATISFIED_AT_ZERO_PROVED_SEVERANCES__NO_PRE_FORGE_FF_DUPLICATION` | **LIMIT_ONLY.** Zero proved severances are a limit, not product positive proof. Relabel as a limit. |
| 5 | `SATISFIED_AT_PRESERVATION__RESIDUALS_REMAIN_OPEN` | **PASS_AT_PRESERVATION.** 17 gates, 42/16, 50 gaps, issuer/provenance holds and 154/1608 overlap preserved. |
| 6 | `TYPED_HOLD__PARENT ISSUE-BY-ISSUE DISPOSITION NOT RE-ADJUDICATED HERE__17 GATES PRESERVED__NO FALSE GREEN` | **NOT_SATISFIED__BLANKET_HOLD.** The blanket “not re-adjudicated here” is not the required issue-by-issue disposition or precise unfinished action. |

The overall records correctly say `goal_complete=false`. The review does not accept the C14 record as a terminal pass; it accepts the verified content counts/schema/lineage at scoped source-preparation grade and requires the corrections below.

## 5. Main judgment — demand, sourcefree demonstration, and exact blocker

**No genuinely demanded non-canary current operation is proved to have a legal sourcefree authority-to-output demonstration in the C14 record.**

- **C9 O08/O12/O13** is a real sourcefree API path, but its authority is `TEST_ONLY_SOURCEFREE` / `B49-TEST-ONLY-QUERY-AUTH`, `target_use_permission_ids=[]`; it is not a production/non-test selected operation.
- **C9 P1/PDEV01 210-DIST** is existing test-only/sourcefree capital: 210 DIST bound to 210 current I03 queries/predicates and 210 Batch units, 210/210 COMPLETED/SUPPORTED, 630 typed refusals; it is not original35/native selection and does not prove a selected shared35 operation.
- **C2 O11** is an exact sourcefree same-person joint composition over a 58-row synthetic nonrespondent fixture; it has no selected original J issuer and is not historical J equivalence.
- **C10/C11** are test-time historical replays; C10 original run `NOT_OBSERVED`, C11 original run `NOT_RUN`; one row/9-family witnesses are not all35 or current selection.

The exact remaining blockers are the selected shared35 source/wave + current C11 release + I03 query/predicate, a selected current F03 operation with current authority/permission, a selected current QUC operation with successor contract, and the original/current source-science issuer record. These are precise missing inputs, not a new authority gate. **No original scope or scientific authority is minted by this review.** The C9 empty-repository refusal is an expected as-built negative; the 630 non-DIST operations are typed refusals, not missing engines. No rebuild/new engine is justified.

Conversely, the C14’s typed hold must not be used to retire a function or to stop eligible existing-owner tests. The sourcefree C9/PDEV/C2 evidence remains useful at its declared sourcefree scope; it simply does not satisfy the “genuinely demanded non-canary selected operation” criterion.

## 6. Findings requiring correction

| ID | Severity | Gate | Required correction |
|---|---|---|---|
| **C14-G6-T6** | P1 | T6 | Replace the blanket “PARENT ISSUE-BY-ISSUE DISPOSITION NOT RE-ADJUDICATED HERE” with an issue-by-issue table for #716/#748/#753 and all post-#765 issues, each backed by an actual qualified record or an exact missing record/owner/next action. |
| **C14-F01-C8-LINEAGE** | P2 | C8 lineage | Remove the stale `00` line 115 claim that the C8 rereview “has not been performed.” Record C8 review `356124ee`, focused check `77a879822`, residual closure `0e0997213`, C8 accepted content `55fca441`, C8 51-case `03` SHA `cc427562…`, and C14 55-case `03` SHA `f21823…` separately. |
| **C14-F03-REVIEWER-INDEPENDENCE** | P2 | Independence | Replace the 09 “different session from every C1–C13 author/reviewer” clause with nonauthor-of-C14/fanin/implementations, disclosed prior review relationships, no fan-in write authority, verified model/effort. Do not make absence of prior review experience a gate. |
| **C14-F04-C9-LINEAGE** | P2 | C9 lineage | Cite the reviewed C9 cut `d540cfcc` and the C9R correction `02a13a5e` separately; label the HQ disposition as scoped acceptance after correction with no independent re-review, or perform a focused independent re-review. Do not present `05a750ad` as the review of `02a13a5e`. |
| **C14-F05-C6F08-QUC** | P2 | C6-F08 | Replace the unqualified `__NO_QUC_READER__` / “F08 no QUC reader” wording in `03` line 30 and `04` line 40 with “current QUC owner/first consumer UNKNOWN_NOT_PROVED; no selected current operation; no absence proof.” Preserve the q3 supplemental and C12/C13 limited-map limits. |
| **C14-G3-T3 / C14-G4-T4** | P2 | T3/T4 | Relabel zero-equivalence/zero-severance statuses as limits (`SATISFIED_AS_LIMIT...__NO_PRODUCT_POSITIVE_PROOF`), not product positive proof. |
| **C14-F02-BASE-LINEAGE** | P3 | Base lineage | Distinguish original prepared base `e2fdd975` from C14 intake base `46104b8d` in `00` line 5 vs `09` line 16. |
| **C14-F06-C9-WORDING** | P3 | C9 wording | Replace “real sourcefree non-test API path” with “real API path exercised in the sourcefree test-only harness; not a production/non-test selected operation.” |
| **C14-F07-PROVENANCE-PLACEHOLDER** | P3 | Provenance | Point the provenance field to the external C14 intake record rather than the ambiguous branch-head placeholder; keep content/provenance hashes separate; no self-hash. |

The C14 content also passes the substantive checks not listed above: 55 unique IDs, families, 25/30 taxonomy, canonical/alias equality, A–J schema, C8 51-case preservation, 02/05/01/08 counts, C9–C13 evidence pins, and no false native/S3/science/actor green.

## 7. Scoped acceptance

**Accept at scoped source-preparation/documentary grade:** the immutable C14 content snapshot `f42b73ab` counts, case IDs, families, taxonomy, A–J schema, canonical/alias equality, C8 51-case preservation, derived-table counts and C9–C13 evidence pins. **Do not accept** the blanket T6 hold, the “SATISFIED_AT_ZERO” product-positive reading of T3/T4, the C8 stale line, the C9 review-cut/acceptance lineage, or the unqualified QUC absence wording. This is not native/S3/science/actor acceptance, not a protected merge, not a CI waiver, and not a whole-#777 completion.

## 8. Next executable authorized action

1. **Immediate documentary correction** by the existing HQ/fan-in owner (no new worker): apply C14-G6-T6, C14-F01, C14-F03, C14-F04, C14-F05, C14-G3/G4, C14-F02, C14-F06 and C14-F07. For T6, produce the issue-by-issue disposition table from existing qualified records; if a record is absent, name the exact missing record, owner and next action. Do not write the fan-in from this review lease.
2. **Next product action where evidence exists:** reuse the existing PDEV01-GAP007 210-DIST sourcefree path with one actual selected shared35 source/wave + current C11 release + I03 query/predicate, if a competent source owner names it. If no selected input exists, record the exact `NOT_RUN__UNPROVED_SELECTION` blocker; do not add an `EpreOperation→I03` resolver, a new Batch/C11/I03 engine, or a 630-missing-capability inference.
3. **C10/C13 F03 and C11/C12 F08:** if a real selected current F03 or QUC operation exists, name its exact current authority/permission/contract and route at the existing owner. Otherwise retain `F03=UNPROVED_CURRENT_SELECTION` and F08 `UNPROVED`; no new QUC/F03 reader or engine.
4. **No new broad archaeology, rebuild, environment install, CI/merge, source/respondent read, or new tests/full matrix** from this review. The smallest real competent decision is a source/science/C11 owner naming the selected operation and exact authority; absent that, the typed hold remains.

## 9. Limits

This review read immutable Git objects and C14/C8/C9–C13 text/TSV/JSONL evidence only. It did not execute source, tests, source configuration, native/original data, or any S3/science/actor operation; it did not read respondent/SAV/DTA/DB/source bytes; it did not install, merge, waive CI, or write HQ/fan-in/protected/peer state. Only `C15_HQ_FANIN_C14_REREVIEW/` was written. Quota `UNKNOWN`. This is the required P7 whole-record court, not final native/product acceptance.

**Final:** `REVISE` — scoped acceptance of the verified C14 counts/schema/lineage; T6 blanket hold rejected; reporting/lineage corrections required; no whole-#777 or native/product acceptance.
