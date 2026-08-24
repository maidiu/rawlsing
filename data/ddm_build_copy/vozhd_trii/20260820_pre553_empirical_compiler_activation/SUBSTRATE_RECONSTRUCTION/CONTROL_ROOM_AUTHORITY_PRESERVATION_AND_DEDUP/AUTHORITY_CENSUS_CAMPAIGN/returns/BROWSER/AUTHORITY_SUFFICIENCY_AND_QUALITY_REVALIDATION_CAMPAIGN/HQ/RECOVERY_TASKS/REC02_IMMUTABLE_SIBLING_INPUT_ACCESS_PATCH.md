# REC-02 — Immutable Sibling Input Access Patch

Status: `BINDING_OVERRIDE__REC02_P1_INPUT_ACCESS`

HQ intentionally reconciled R01-R08 as sibling evidence branches without merging those worker trees into the control branch. REC-02 must therefore read R08 and R03 inputs by immutable commit, not by assuming their return directories are present in the current tree.

## Pinned worker inputs

### R08 provenance/succession inputs

`R08_RETURN_SHA = 742fa99500f2f8ff82d65b4e0eb1339e7a56accb`

Required files:

- `.../returns/R08/README.md`
- `.../returns/R08/UNPROVED_SUCCESSION_AND_COEXISTENCE_LEDGER.csv`
- `.../returns/R08/OPEN_HQ_QUESTIONS.md`

Expanded exact prefix:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/CONTROL_ROOM_AUTHORITY_PRESERVATION_AND_DEDUP/AUTHORITY_CENSUS_CAMPAIGN/returns/BROWSER/AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/R08/`

### R03 evidence-access inputs

`R03_RETURN_SHA = 6d8cc6b4c918516c475e3c0bea1b8c9e50f60374`

Required files:

- `.../returns/R03/FINDING_LEDGER.csv`
- `.../returns/R03/OPEN_HQ_QUESTIONS.md`

Expanded exact prefix:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/CONTROL_ROOM_AUTHORITY_PRESERVATION_AND_DEDUP/AUTHORITY_CENSUS_CAMPAIGN/returns/BROWSER/AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/R03/`

## Exact local procedure

Check object availability:

```bash
git cat-file -e 742fa99500f2f8ff82d65b4e0eb1339e7a56accb^{commit}
git cat-file -e 6d8cc6b4c918516c475e3c0bea1b8c9e50f60374^{commit}
```

If either object is unavailable locally, fetch only the exact governed sibling branch/object needed:

```bash
git fetch origin agent/vozhd-trii-authority-revalidation-r08-provenance-supersession
git fetch origin agent/vozhd-trii-authority-revalidation-r03-driver-facet-quality
```

Exact-SHA fetch is also permitted where supported.

Do not merge, rebase, or cherry-pick either sibling into REC-02.

Read each file using:

```bash
git show '<PINNED_SHA>:<EXACT_PATH>'
```

Record the commit and blob identity for every pinned governing input used.

## Failure rule

Only if the pinned commit cannot be obtained from the governed origin, or a required file is absent at its pinned commit, may REC-02 classify the governing input itself as blocked.

Absence from the current REC-02 tree is NOT a blocker.

## Warrant construction

`WARRANT_REGISTER.csv` must be constructed from the exact R08 U003-U014 rows read from the pinned R08 commit, not from memory or a chat summary.

The V525b and d62-92 warrants must be constructed from the exact pinned R03 findings/questions.

All remaining REC-02 rules remain unchanged.
