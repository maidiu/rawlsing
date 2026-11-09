# VMESTYE ZL-10R — R2 adversarial re-review of author repair

**Disposition: REVISE (schema/provenance), then HELD for full functional acceptance.** This R2 report supplements and does not overwrite R1 \`00_HOSTILE_REVIEW.md\` or \`01_DEFECTS.tsv\`.

**Re-examined exact author PR:** [#844](https://github.com/maidiu/rawlsing/pull/844), new immutable head \`a477372aec091b4a8741f415a7f0252ce015680a\`; prior reviewed head \`8ae360672633a3bb67eeb6d1af8b0751b4f6fd46\`; protected source/base \`integration/pre-main-reconciliation-r1@9253064bc9423a0f0ccda4fbdea43c2f54f800c6\`. GitHub compare verified the author repair is **exactly one descendant commit with eight modified files**; PR still draft/open, original nine-file subtree only, and protected base unchanged at inspection. This report is written **only to the pre-existing side-lane review branch**. No author branch or protected changes.

**Execution surface:** authenticated GitHub read/cross-file audit. Source bodies fetched at exact pinned commits; no S2 runner, no Actions, no Copilot review, no S3 original native source/grants; no separately instantiated reviewer. As before, **separate branch is not a genuinely different agent** and must not supply constitutionally required different-agent receiving status.

## R2 method and reproducible receipts

- Read all six repaired candidate TSVs, exact headers and row widths; totals: \`FINDINGS=20, OPERATION_TRACES=20, AUTHORITY_USE=20, EVIDENCE=73, COVERAGE=20, UNJOINS=67\`. **Zero width violations.** Local same-prong foreign-key/cross-finding checks: **zero dangling references** for material non-sentinel finding, trace, evidence and consumer links; all 12 \`COVERAGE.first_consumer_presence=PRESENT\` links now resolve to a **\`FIRST_CONSUMER\`** evidence record. Of 20 coverage records, 12 are \`PRESENT\` (static source evidence only), eight \`NOT_ASSESSED\`.
- Validated all **19 distinct \`(source_commit_sha, source_path)\` pairs** named by \`EVIDENCE\` against exact Git blob SHA: **19/19 match**, covering 17 current/historical code files and two historical roster files. Presence of a blob is evidence of file identity, not execution or source-native issuer.
- Independently loaded original 44-row D01 \`INHERITED_44_OBLIGATION_BASELINE.csv\` at commit \`bb0814fa39de335558a11fec2b9d085e68216c9a\`, blob \`f1252e901677203f7b54ded855a18a7738f28df7\`; **all 23** candidate \`EHLMX*\` obligation IDs are actual unique rows of that source.
- Independently loaded C6 94-row (29 FUNCTION + 58 RELEASE + 6 DENOMINATOR + 1 CROSSREF) \`01_LEGACY_SELECTED_AUTHORITY_USE_AND_INCOMPLETE_CALLEE_COVERAGE.tsv\` at commit \`aed1a0ae13c58f11f4dabd07c818b62f72adf989\`, blob \`ba39d8f9c9f06440df5d068bdd9f0b857c06ce58\`; **all 18** candidate \`EHC6*\` \`ROW_TYPE=FUNCTION;ID=...\` identities match unique original FUNCTION source rows. These **41 real historical row identities** are source-graded *overlap candidates*, not proof of same-grain successors or exact accepted P0 census IDs.
- The large accepted \`CONTROL/P0_RETURN_AND_BRANCH_CENSUS.tsv\` remains unavailable to bounded GitHub connector source reads (returned empty body), consistent with author caveat. **No 6,125-row replay**, no P0 ID allocation, no cross-estate completeness. 67 UNJOINS = 22 retained prior symbol attempts + 4 new code-symbol/census attempts + 41 historical/census attempts. Of those 67, 22 are \`OTHER_TYPED\`, 45 \`SOURCE_UNAVAILABLE\`. Zero \`QUALIFIED_SAME_GRAIN_SUCCESSOR\` claims, as appropriate.
- New current code called out by the author is real and blob-verified: \`rawlsing_next/pre553_universal_workload.py\` \`8e7fe00a3ed008361d9f3c501e7782b2de3a636e\`; \`rawlsing_next/pre553_batch_runner.py\` \`2d291600b9a10c56d9c6f6de7f7d619f6c52e829\`; \`rawlsing_next/pre553_effective_n.py\` \`76bbddb0fddc91d64c83f5d6164a63cb4e2a3ff5\`.

## Six R1 findings: disposition at R2

| Original | R2 adjudication | Exact observed basis | Residual qualification |
|---|---|---|---|
| **D01: census and no-drop** | **PARTIAL REPAIR; HELD** | 23 LMX + 18 C6 source identities independently source-validated; 67 explicit unjoins; all \`census_id=UNRESOLVED\` | No accepted P0 exact five-tuple join, scoped source-minus-coverage, 6,125 census readback, or whole-prong no-drop |
| **D02: four first-consumer mislinks** | **CLOSED AT S1-TABLE GRAIN** | F02→EC02, F03→EC03, F11→EC11 correctly typed; F15 downgraded to NOT_ASSESSED; 12 PRESENT links have FIRST_CONSUMER records | Callsite citation is static, not observed test/native first-reader execution |
| **D03: source rule availability** | **CLOSED AT ACCURACY GRAIN** | All 20 rows \`rule_available=UNKNOWN\`; selected/applied/refusal all UNKNOWN; no source-specific issuer claim | Source rules, selection, application and negative enforcement still unknown by design |
| **D04: R01/R03/Batch/F018 omissions** | **CLOSED AT S1-LOCATOR GRAIN** | New F17–F20 operations and exact code, first-consumer candidate EC17/18/19; F20 explicitly UNRESOLVED | No source/native execution or issued operation receipt, not a substantive proof of whole chain |
| **D05: inverse/higher-order falsification** | **SPECIFIED, NOT EXECUTED; HELD** | Constructed denominator and XOR/XNOR controls described; report explicitly \`NOT_RUN\` | No sourcefree or original35 executed directional conditional receipt; no regression pass awarded |
| **D06: historical Dva/Trii/Chetiri** | **PARTIAL REPAIR; HELD** | Historical 23/18 exact source IDs established; inherited Trii/Chetiri owner obligations now traceable | Dva native execution and whole historic-to-current same-grain consumer equivalence remain unproved |

**Conserved architectural positives:** exact I03 respondent-bound F4 joint cells and typed negatives, directional query architecture, C1 computed N10E evidence, existing sourcefree k-way first-consumer receipts from accepted earlier owner work, I05 bounded/adaptive/recursive distinctions, E41 learned sourcefree seam, existing source-indexed separation, retired V550 lossy cloud **format** without erasure of respondent-level meaning, and narrow owner lifecycle inability for no-lawful-replacement dependents. No rebuilding or physical architecture reopening.

## NEW R2 defects (do not silently absorb into earlier six)

### R2-D07 — BLOCKER / P0 frozen enum violation across 41 historical evidence rows

\`EVIDENCE.tsv\` **lines 34–74 inclusive** contain **41** \`claim_kind=HISTORICAL_SOURCE_OBLIGATION\`. The frozen \`CONTROL/P0_SCHEMA_AND_LEASES.md\` §3B allows \`SOURCE_IDENTITY | OPERATION | AUTHORITY_SELECTION | AUTHORITY_APPLICATION | REFUSAL | PRODUCER | FIRST_CONSUMER | HISTORICAL_DISPOSITION | SOURCE_PERMISSION | OTHER_TYPED\`; **\`HISTORICAL_SOURCE_OBLIGATION\` is not a permitted value**. The same file prescribes versioned \`VMESTYE_P1_PRONG_TABLES_V2\` migration and P0R approval before adding a new enum. This is a literal blocking schema defect **even though the 41 historical source records are real**. The repair author checked tabular widths and FK targets but appears not to have enforced frozen field-level enum values.

**Bounded remedy:** without any schema migration, retype all 41 records as \`claim_kind=SOURCE_IDENTITY\` (the claims explicitly say a source row identity exists, *not* an accepted historical disposition). Keep \`claim_supported\`, exact source IDs/cuts, all 41 matching UNJOINS and negative status intact. Alternatively formally approve a v2 schema through its lawful owner before publication; no ad hoc enum extension. Audit all 73 rows against every frozen enum, not only columns and foreign keys.

### R2-D08 — MEDIUM / reviewer-history pointer lodged in independent-review acceptance field

The **51 newly added EVIDENCE rows** (lines 24–74) populate \`independent_review_ref\` with \`PR853:D02\`, \`PR853:D04\` or \`PR853:D01/D06\`. Those are **the earlier hostile self-side-lane defect references at old author head**, not genuinely independent acceptance of the 51 new or changed rows at \`a477372a...\`. In particular historical rows 34–74 were not present at the original PR #853 review. Existing 22 rows retained \`NOT_INDEPENDENTLY_REVIEWED\`. The row-level field semantics are acceptance-sensitive, and naming a prior review is not an independent review receipt for a newly written row.

**Bounded remedy:** set the 51 \`independent_review_ref=NOT_INDEPENDENTLY_REVIEWED\` until a genuinely separate reviewer verifies *that exact row at its actual author SHA*. Preserve PR #853 D01/D02/D04 as **repair lineage or previous defect** in narrative/claim-supported text, not the independent acceptance pointer. The fact that current \`00_RETURN.md\` says “independent review pending” is correct, but does not cure misleading field data.

## Verdict and gates

**REVISE on exact \`a477372aec091b4a8741f415a7f0252ce015680a\`** because R2-D07 is an actual frozen schema break and D08 muddies reviewer provenance. Both are documentary, mechanically bounded; fix on **existing author PR #844** without another compiler, campaign, or uncontrolled architecture change. Preserve all 41 verified historical source identities and all open UNJOINS.

**Even after D07/D08 repair:** the authoritative full VMESTYE qualified functional succession remains **HELD**, not “PASS”: D01 accepted P0 census exact anti-join, D05 directional/higher-order actual falsifier execution, D06 Dva/native source-to-current equivalence, selected original35 source/science grants, real non-test learned/FF world/actor first consumer, and a constitutionally separate independent re-review are still absent. These missing external/source-law proofs must not be reported as a software/compiler defect.

**Post-repair receiving protocol:** compare exact corrected author head to \`a477...\`; verify exactly 41 retyped source-identity rows and 51 independent-review pointer corrections, no lost/duplicated/unjoined historical identities; validate all six P0 schema enums and local keys; confirm S1-only status unchanged. Release for proper separate-agent adjudication, **not** protected merge or self-acceptance.

**Review branch custody:** prior R1 files preserved; author branch, original issue, selected source/native issuers, protected PRE-MAIN unmodified. No credit-consuming reviewers or Actions invoked.
