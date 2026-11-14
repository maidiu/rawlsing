# PYAT #1006 follow-through r2 — corrected baseline + measured locality candidate + writer profile

## Verdict

**`REVISE_EXACT_DEFECT_RECONCILED`.**  The independent G5 at
`0169fac9f3840800796c664eee462bbb8984bb42` (draft PR #1034) is the controlling
disposition.  Its three exact report defects are corrected, and this bounded
follow-through supplies:

- one executable TEST_ONLY matched before/after locality comparison on the same
  reviewer-retained accepted estates;
- a per-shape exact fact/projection/replay/release parity receipt;
- a 2k call-boundary writer profile with honest scale limits;
- one measured candidate for a later conditional S2-C/D handoff.

No production file was edited.  No optimized engine, owner acceptance,
independent G5, source bridge, #999 native repair, #998 integration, #1001
full court or #1007 rights is claimed.

## Identity and permissions

- Author session: `ses_e2969dd1affeEwT1XKJtlWJeI4` (same #1006 author).
- Follow-through branch: `codex/pyat1006-locality-writer-profile-20261113-r1`,
  descendant of `51aabffef90399359008e00890f551a1e56c0da9`.
- Tested production head: `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`.
- Independent review: `0169fac9f3840800796c664eee462bbb8984bb42`.
- Write scope: only new/changed harness/report/evidence under
  `WORKER_RETURNS/PYAT1006_PHYSICAL_ECONOMICS_R1/` and its
  `followthrough_r2/` subtree.
- Permission grade: **SOURCEFREE TEST_ONLY**; original35/source/native science/
  CURRENT/issuer/rights/protected merge not used or claimed.
- `rawlsing_next` production and accepted tests: READONLY.

## Reviewer data reused read-only

Reviewer data root:
`/Users/matthewsmith/.codex/worktrees/pyat1007-dual-series-prep/Rawlsing/WORKER_REVIEWS/PYAT1006_PHYSICAL_ECONOMICS_G5_R1/data/`.
Capsules and actual estate opens were verified by `SavedC11Admission`; exact
capsule SHA-256s are recorded in
`evidence/locality_candidate_matrix.json`.  No reviewer file was edited,
deleted or committed as this author's work.

## Locality candidate

`locality_probe.py` is labeled **`EXPERIMENT_NOT_IMPLEMENTED`**.  It changes
only the module-global `sorted` lookup in `_pre553_query_eval` so respondent
traversal follows the session's physical insertion order.  It skips no roots,
current check, selector coverage, row-group read, body/locator validation,
predicate/risk/denominator logic, fact issuance or replay construction.

Matched same-release results (full table and per-family read counts in
`evidence/locality_candidate_summary.md` and
`evidence/locality_candidate_matrix.json`):

| case | query | baseline | candidate | factor | exact |
|---|---|---:|---:|---:|---|
| 100k selected | selected | 580.548 s / 204,125 reads / 103.1M rows | 265.680 s / 5,784 reads / 3.0M rows | 2.19x | yes |
| 10k selected | selected | 49.066 s / 20,157 | 21.812 s / 588 | 2.25x | yes |
| 10k reverse F2 | f2_reverse | 51.790 s / 20,153 | 21.116 s / 614 | 2.45x | yes |
| 10k 3-way F4 | f4_three | 56.624 s / 20,161 | 24.665 s / 588 | 2.30x | yes |
| 1k selected | selected | 4.390 s / 1,784 | 2.046 s / 61 | 2.15x | yes |
| 1k reverse F2 | f2_reverse | 4.545 s / 1,785 | 1.993 s / 63 | 2.28x | yes |
| 1k 3-way F4 | f4_three | 5.002 s / 1,784 | 2.468 s / 61 | 2.03x | yes |

Exact means fact ref, full semantic projection SHA-256, replay ref and release
refs all equal baseline and native-oracle behavior.  Candidate 100k selected
tree RSS is 2.81 GiB versus 2.95 GiB baseline; temp SQLite is 1.301 GB in both.
The remaining 100k candidate time is native object/predicate evaluation
(about 247.8 CPU s) plus session build, not read churn.

Semantic/change/restore/hostile tests: **2 passed**
(`evidence/locality_candidate_tests.txt`).  This is a candidate for a narrow
S2-C/D handoff only after the qualified S2-A native body-truth descendant; it
is not production, owner acceptance or G5.

## Writer profile

`writer_profile.py` profiles the unchanged accepted writer on the existing
sourcefree fixture: 2,000 respondents / 6,490 events / weights / chunk 512.
Absolute unprofiled writer wall: 38.277 s; cProfile wall 108.106 s is used only
for relative shares.  Full diagnosis and proposal:
`WRITER_PROFILE.md`, compact receipt:
`evidence/writer_profile_summary.json`.

Key correction: the 100k direct-I02 inclusive 2,249.700 s (author) / 2,218.465 s
(review) contains first-pass `_Sink`/`_row` body construction and Parquet
flush, `_insert_object`, public-object validation, relation checks, projection/
replay hashing and SQLite work.  At 2k absolute the first pass/sink is 6.507 s,
insert 4.494 s, validate 3.413 s, logical root 0.968 s and candidate/replay
hash 1.010 s; the reread/re-encode pass is 12.691 s.  cProfile shows canonical
projection/identity/object validation and JSON/body reconstruction dominate;
SQLite execute is about 4.2% of the inflated profile wall.

One smallest owner-consistent writer proposal (not implemented): a bounded
per-build memo of the already-computed immutable semantic projection/hash used
by both validation and insertion, retaining one full verification per object
and every source/root/omission/body/locator/current check.  Removing the
second reread/re-encode proof is a separate versioned proof/identity policy
change and is not proposed here.

## Corrected report facts

- RUNBOOK five-file S2-D group: **29** passed, not 36; separate partial-binding
  suite **2** passed; focused **31**; own fixture **6**; follow-through **2**.
- 1k/10k RSS rows are whole-worker peaks; writer-only 1k
  `194,072,576 B`, writer-only 10k `214,261,760 B` (review); 50k/100k are
  writer-only.
- Actual query cause: native respondent ref-key traversal across physically
  ordered row groups plus a separate event cache; not per-respondent
  `ORDER BY ref`.
- Full reconciliation: `CORRECTION_RECONCILIATION.md`.

## Explicit REDs / NOT_RUN / holds

- 100k reverse F2 and 3-way F4 for the locality candidate: `NOT_RUN`.
- Candidate I05/grouped execution and all-seven readers: `NOT_RUN`.
- 100k all-seven native readers and 10/10 same/fresh experiments: `NOT_RUN`.
- #997 source bridge, #998 joined vertical, #1001 full 100k/6 GiB,
  #1007 source rights: external owner holds.
- #999 coherent native body-poison RED: preserved; no blanket native
  correctness is claimed.
- No original35, source permission, native psychology/science, production
  CURRENT/issuer, protected merge or provider credential change.

## Reuse ABI

The accepted ABI is unchanged: `SourcefreeDirectI02Sections`,
`write_direct_estate`, `VerifiedDirectEstate`, `DirectEstateI03Session`,
`SavedC11Admission.execute_i03/execute_i05`, `execute_saved_batch`,
`execute_issued_workload`/`resume_joined_workloads`.  See
`../READER_ABI.md`.  The locality candidate would require an owner-approved
traversal-order hook or equivalent production change on a new descendant; the
runtime monkeypatch here is not that ABI.

## Commands

See `../RUNBOOK.md` and the exact commands in
`evidence/locality_candidate_matrix.json` / `evidence/writer_profile_summary.json`.

## Stop

No production change, no self-G5, no downstream dispatch.  Await HQ decision on
the measured candidate and the conditional S2-C/D owner handoff.
