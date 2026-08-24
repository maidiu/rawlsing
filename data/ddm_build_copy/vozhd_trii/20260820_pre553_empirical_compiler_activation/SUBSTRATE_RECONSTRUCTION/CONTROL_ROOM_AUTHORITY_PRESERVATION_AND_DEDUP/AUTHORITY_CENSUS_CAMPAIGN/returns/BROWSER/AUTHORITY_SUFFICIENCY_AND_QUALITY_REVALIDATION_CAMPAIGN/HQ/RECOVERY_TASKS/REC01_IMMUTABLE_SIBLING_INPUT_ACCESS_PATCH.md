# REC-01 — Immutable Sibling Input Access Patch

Status: `BINDING_OVERRIDE__REC01_P1_INPUT_ACCESS`

This patch exists because the HQ control branch intentionally did not merge the R01-R08 sibling worker trees. The first REC-01 launch correctly stopped when it attempted to read R06 return files as current-tree paths.

That stop was an execution-protocol failure, not a TIR-014 evidence result.

## Governing override

For REC-01 section P1, **do not require the R06 sibling-return files to exist in the current worker tree**.

Read them from the exact immutable R06 return commit:

`R06_RETURN_SHA = 1d0918a907391ccddf3e6ff6ecbd8f754c549672`

The required files are:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/CONTROL_ROOM_AUTHORITY_PRESERVATION_AND_DEDUP/AUTHORITY_CENSUS_CAMPAIGN/returns/BROWSER/AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/R06/RETURN_ADJUDICATION_PROPOSAL.md`

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/CONTROL_ROOM_AUTHORITY_PRESERVATION_AND_DEDUP/AUTHORITY_CENSUS_CAMPAIGN/returns/BROWSER/AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/R06/OPEN_HQ_QUESTIONS.md`

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/CONTROL_ROOM_AUTHORITY_PRESERVATION_AND_DEDUP/AUTHORITY_CENSUS_CAMPAIGN/returns/BROWSER/AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/R06/FINDING_LEDGER.csv`

## Exact local procedure

From the Rawlsing repository, first test whether the immutable commit object is available:

```bash
git cat-file -e 1d0918a907391ccddf3e6ff6ecbd8f754c549672^{commit}
```

If it is not available locally, fetch **only that exact immutable object / assigned R06 branch** from the governed origin. Do not merge or rebase it into REC-01.

Permitted examples:

```bash
git fetch origin agent/vozhd-trii-authority-revalidation-r06-structure-relations
```

or, where the remote permits exact-SHA fetch:

```bash
git fetch origin 1d0918a907391ccddf3e6ff6ecbd8f754c549672
```

Then read each required file without changing the working tree:

```bash
git show '1d0918a907391ccddf3e6ff6ecbd8f754c549672:<EXACT_PATH>'
```

Optionally copy the rendered text into REC-01 scratch/output evidence notes, but do not cherry-pick or merge the R06 commits.

## Verification

Before relying on the inputs, record:

- immutable R06 commit SHA;
- successful `git cat-file -e` result;
- each exact path read;
- blob SHA where practical via `git rev-parse '1d0918a...:<path>'`.

## Failure rule

Only if the exact immutable commit cannot be obtained from the governed origin, or one of the three exact paths does not exist at that commit, may REC-01 stop with:

`STOP__PINNED_R06_INPUT_UNAVAILABLE`

Do **not** stop merely because the file is absent from the REC-01 current tree.

## Restart law

A prior REC-01 blocker produced solely by the old current-tree assumption has no substantive evidentiary weight. Restart REC-01 from the new launch HEAD supplied after this patch is committed.

Do not continue the old blocked branch as though it had executed P2-P7.
