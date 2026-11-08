# C15 — commands and evidence

**Review worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-c5-source35-independent-review`
**Review branch:** `agent/pyat777-c5-source35-independent-review-20261107-r1`
**Target content snapshot:** `f42b73abf2532f9a4ea589e7f80841e15585d8e1`
**Provenance metadata:** `ea7e878a82e2343591724433fcd6b13910602c84`
**C8 accepted historical content:** `55fca441d1c674c256473c264cabda48f2df0e52`
**Verdict:** `REVISE`

All HQ/fan-in/source reads were read-only. The only writes were under `C15_HQ_FANIN_C14_REREVIEW/`. No source, respondent/SAV/DTA/DB, source-byte, native, science, actor, test, environment install, CI/merge or protected write occurred.

## 1. Worktree/branch and target identity

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-c5-source35-independent-review
git branch --show-current
git rev-parse HEAD
git status --short
```

Result:

```text
agent/pyat777-c5-source35-independent-review-20261107-r1
ea9ff9e54e2bc7c9a56a1398d172e87a8f109f03
(only the C15 lease is untracked before commit)
```

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq cat-file -t f42b73abf2532f9a4ea589e7f80841e15585d8e1
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq cat-file -t ea7e878a82e2343591724433fcd6b13910602c84
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq cat-file -t 55fca441d1c674c256473c264cabda48f2df0e52
```

Result: all three are commits. `f42b73ab` parent `23a3454b8`; `ea7e878a` parent `f42b73ab`; C8 `55fca441` is an ancestor of C14 intake base `46104b8d`.

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq diff --stat f42b73abf2532f9a4ea589e7f80841e15585d8e1..ea7e878a82e2343591724433fcd6b13910602c84
```

Result: provenance touches only `09`, `C14/00_RETURN.md`, `GOAL_AUDIT.json`, `EVIDENCE_INDEX.json` (metadata references). The C14 content is immutable at `f42b73ab`.

## 2. Canonical/alias and count/schema verification

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq show f42b73abf2532f9a4ea589e7f80841e15585d8e1:WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl | shasum -a 256
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq show f42b73abf2532f9a4ea589e7f80841e15585d8e1:WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl | shasum -a 256
cmp <(git -C ... show f42b73abf2532f9a4ea589e7f80841e15585d8e1:...03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl) \
    <(git -C ... show f42b73abf2532f9a4ea589e7f80841e15585d8e1:...03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl)
```

Result:

```text
canonical f21823f83e6aed6a64695150bf4ed43df2e7fd88b3310ab26752476acc61a778
alias    f21823f83e6aed6a64695150bf4ed43df2e7fd88b3310ab26752476acc61a778
cmp exit 0 (byte-equal)
```

The Python probe `probes/verify_c14.py` parsed the exact 55 records:

```text
cases=55 unique=55
families={'C1': 1, 'C2': 2, 'C3': 10, 'C4': 2, 'C5': 7, 'C6': 29, 'C9': 4}
taxonomy={'FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED': 25, 'NOT_RUN': 30}
A_J_schema_all_55=True
02_rows=153 02_cases=55 05_rows=55 01_rows=94 08_rows=60
```

Per-record verification:

- all 55 `A`–`J`, `forward_walk`, `reverse_walk`, `exact_hold`, `frozen_taxonomy_verdict` nonempty;
- `02` 153 rows = 55 CASE + 26 FF_REGISTER + 16 FF_DEPENDENCY + 15 POST_FF_REGISTER + 11 POST_FF_SEAM + 30 748_CURRENT_OWNER;
- `02`/`05` case IDs equal the 55-case `03`;
- 17 A01–A17 agenda gates present.

## 3. C8 51-case preservation split

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-authority-severance-hq show 55fca441d1c674c256473c264cabda48f2df0e52:.../03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl | shasum -a 256
```

Result:

```text
C8 51-case 03 SHA-256 = cc4275628286f31ba3695d92910f52d639a3f2d54ca7d43852bbd9d12b614251
C14 55-case 03 SHA-256 = f21823f83e6aed6a64695150bf4ed43df2e7fd88b3310ab26752476acc61a778
C8 rows=51; all 51 historical IDs/taxonomy/A-J preserved in C14 55-case return
Only q3_supplemental/q3_supplemental_source added on C6-F03_QREL and C6-F08_Q_USE
```

C8 lineage evidence:

- C8 review `356124ee452d8cababaae7f2f57d05e8f0d17deb` (`C8_HQ_FANIN_REREVIEW/00_REVIEW.md`);
- C8 focused check `77a8798223998cf56535424794bc3bcb6ce80c9f` (C8-001/002 closed; C8-003 residual);
- C8 reference residual closure `0e0997213` (`13_C8_REFERENCE_RESIDUAL_CLOSURE.md`);
- C8 accepted content `55fca441d1c674c256473c264cabda48f2df0e52`.

The C14 `00` line 115 claim that the C8 rereview “has not been performed” is therefore stale/contradictory and is reported as `C14-F01-C8-LINEAGE`.

## 4. Derived-table and evidence-pin checks

`02` case rows (55) have the expected taxonomy after C8/C14 correction:

```text
EVIDENCE_GRADE: 30 NOT_RUN + 25 FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED
C3-FF-04: NOT_RUN (no implementation-inadequate label)
```

`05` 55 rows, IDs equal `03`. `01` 94 rows (29+58+6+1 crossref). `08` 60 rows. `07` 17 A01–A17 rows.

C9–C13 evidence pins independently hashed at the content snapshot:

```text
C9 01_CASES.jsonl                 e05ed0876aaba76c9085784b654c4c10b2d3d72771ed2449d5d9247438e41400
C9 P1 04_BOUNDARY_LEDGER.jsonl    09964387b58fa94be6783fc6a789a9f5445253eeb28f198d9d865dc57c8b5e49
C9 independent REVIEW.json        d56b499e672c7d8094fc955e8035deb90167fc979a8e8c484cef10f1f4ff3b35
C10 TRACE.jsonl                   53c2b4ed0ae775682f4ae7b7cd477868d6dc9dadd4d70bf802ce45670cb97184
C11 TRACE.jsonl                   6a23bf6a1e99c5fbbe9e0ddeca6ae8c5c52d823e793701ee46e4e85aeed0d22b
C12 RESPONSIBILITY_MAP.jsonl      5067649bbd16a2c95426ae88e112c56da2667029071b53cfc0a48bb8991675a1
C13 RESPONSIBILITY_MAP.jsonl      66e7ee95f2d6d02a27d08b238319d0a9ba460129cf8b65bae7cfb34ef4db9ed2
```

C9 substantive effects verified from the C9 return/P1 boundary: 4/4 API ops/facts/receipts; wrong SHA 0/4; typed wrong host/purpose; restore exact; 840 candidate admitted; PDEV01 210/210 COMPLETED/SUPPORTED; 630 typed refusals; I05 16/30/16; empty C11 expected negative. C9 review `05a750ad` was `REVISE_SCOPED` on author return `d540cfcc`; C9R correction is `02a13a5e`; no independent re-review of `02a13a5e` is recorded. This is reported as `C14-F04-C9-LINEAGE`, not a rejection of the substantive C9 effects.

C10/C11 effects verified from their returns/reviews: C10 18,518 rows/35 waves/9 witnesses, original run `NOT_OBSERVED`, current F03 `UNPROVED`; C11 one GSS/1973/`uswar` row, positive `1c78a386…`, original run `NOT_RUN`, current QUC `UNPROVED`. C12/C13 are limited maps; no QUC/F03-equivalent producer→selector→consumer and no selected current operation.

## 5. Probe output and failed checks

```sh
python3 WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C15_HQ_FANIN_C14_REREVIEW/probes/verify_c14.py
```

Result:

```text
C14_CONTENT_SNAPSHOT_VERIFICATION
content=f42b73abf2532f9a4ea589e7f80841e15585d8e1
provenance=ea7e878a82e2343591724433fcd6b13910602c84
c8=55fca441d1c674c256473c264cabda48f2df0e52 c8_03_sha=cc4275628286f31ba3695d92910f52d639a3f2d54ca7d43852bbd9d12b614251 c14_03_sha=f21823f83e6aed6a64695150bf4ed43df2e7fd88b3310ab26752476acc61a778
cases=55 unique=55 families={'C1': 1, 'C2': 2, 'C3': 10, 'C4': 2, 'C5': 7, 'C6': 29, 'C9': 4}
taxonomy={'FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED': 25, 'NOT_RUN': 30}
c8_rows=51 02_rows=153 02_cases=55 05_rows=55 01_rows=94 08_rows=60
terminal={'T1': 'SATISFIED_AT_BOUNDED_DECLARED_SCOPE__NOT_GLOBAL_MACHINE_COMPLETENESS', 'T2': 'NOT_SATISFIED__TYPED_HOLD', 'T3': 'SATISFIED_AT_ZERO_FULL_EQUIVALENCE_CLAIMS__NO_EQUIVALENCE_ACCEPTED', 'T4': 'SATISFIED_AT_ZERO_PROVED_SEVERANCES__NO_PRE_FORGE_FF_DUPLICATION', 'T5': 'SATISFIED_AT_PRESERVATION__RESIDUALS_REMAIN_OPEN', 'T6': 'TYPED_HOLD__PARENT ISSUE-BY-ISSUE DISPOSITION NOT RE-ADJUDICATED HERE__17 GATES PRESERVED__NO FALSE GREEN'}
failed_check_count=11
FAILED_CHECK c9_review_cut_reviews_source_cut
FAILED_CHECK c9_acceptance_label_qualified
FAILED_CHECK c6_f08_exact_hold_no_quc_reader
FAILED_CHECK 04_no_unqualified_no_quc_reader
FAILED_CHECK 00_c9_non_test_wording_qualified
FAILED_CHECK 00_c8_stale_line_absent
FAILED_CHECK 00_base_46104b8d
FAILED_CHECK 09_no_all_prior_reviewer_gate
FAILED_CHECK T6_not_blanket_hold
FAILED_CHECK T3_limit_not_positive
FAILED_CHECK T4_limit_not_positive
REVISE_REQUIRED
```

The failed checks are the findings in `01_FINDINGS.jsonl` and the correction list in `00_REVIEW.md`; they are not a rejection of the verified 55-case counts/schema.

## 6. Findings output validation

```sh
python3 WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C15_HQ_FANIN_C14_REREVIEW/probes/build_findings.py
```

Result:

```text
wrote 14 records to .../C15_HQ_FANIN_C14_REREVIEW/01_FINDINGS.jsonl
13 FINDING + 1 VERIFICATION
verdict REVISE
failed checks 11
```

## 7. Evidence/hashes logs

- `logs/verify_c14.json` — structured counts, hashes, checks and failed checks.
- `logs/verify_c14.log` — human-readable verification and failure list.
- `logs/c15_file_hashes.log` — SHA-256 of the C15 review artifacts and C14/C8 evidence references.

## 8. Limits

No source/respondent/SAV/DTA/DB/source-byte read, no source configuration execution, no native/S3/science/actor effect, no new test/full matrix, no environment install, no CI/merge, no HQ/fan-in/protected/peer write, no goal-status change. The C14 content snapshot and provenance are immutable; this review only writes the C15 lease. Quota `UNKNOWN`.
