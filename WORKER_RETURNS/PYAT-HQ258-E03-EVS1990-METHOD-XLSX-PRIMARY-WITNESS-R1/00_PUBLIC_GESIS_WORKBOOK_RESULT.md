# HQ258 E03 — public GESIS methodology XLSX retrieval result

**TERMINAL:** `HQ258_E03_RETURNED__NO_SELF_ADOPTION`
**Agent:** existing DeepSeek-Harness/OpenCode independent documentary verifier
**Branch:** `agent/deepseek-harness-pyat-hq258-evs1990-method-workbook-independent-r1`
**HEAD at run:** `f3b4877554930141f447668eab9025ecc062d5a1` (commission tip; clean worktree)
**Live control:** `integration/pre-main-reconciliation-r1 @ f57be2d9e221eb089e3475b5f5be40ca41544510`
**Sealed HQ258 row:** `HQ258_E03_EVS_GESIS_PUBLIC_XLSX` in checkpoint
`20261008-PYAT-HQ258-G2-INDEPENDENT-REVIEW-ACCEPTED-I01-E03-ISSUED-R1 @ 08219a5f…` — branch and
`commission_tip f3b48775…` match exactly.
**Scope honoured:** public documentation only; no `.sav`/`.dta`, no Library, no raw respondents, no
actor/V3, no native F7, no AT07 issuer, no code or HQ/semantic change, no model-use grant.

## 1. Retrieval — SUCCESS, and the two catalogue entries are the same file

`web_fetch` refuses the workbook (`unsupported content type
"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"`), reproducing the Browser
failure E02 recorded. A governed local `curl` retrieval succeeded for both catalogue URLs:

| URL | HTTP | Content-Type | Content-Length | Content-Disposition filename |
|---|---|---|---|---|
| `https://access.gesis.org/dbk/70780` | 200 | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | 92628 | `ZA7503_Method_Information.xlsx` |
| `https://access.gesis.org/dbk/70775` | 200 | same | 92628 | `ZA7503_Method_Information.xlsx` |

Both downloads are **byte-identical**:
`sha256 401048862995440764950a3fa3ec9ec5349bff674a58de7725db848de6655734`, `file` = Microsoft Excel
2007+, no HTML interstitial, no login wall.

**Binding consequence:** the "1981–2008 Method Overview" entry (70780) and the "1981–2017 Method
Overview" entry (70775) currently resolve to the **same physical workbook**, `ZA7503_Method_Information.xlsx`.
The workbook's own metadata explains this: `docProps/core.xml` title is
"European Values Study 1981-2008 - Method Information (v1)" (`dcterms:created` 2013-06-12,
`dcterms:modified` 2022-12-15, creator Brislinger, Evelyn, last modified by Solanes, Ivet), while
`Contents!C4` reads "(Version 6, December 2022)" and the data sheet is named
`EVS Surveys 1981-2017`. The 1981–2008 workbook was updated in place through the 2017 wave and is
served for both catalogue rows. This is **not** an access failure; it is an identity finding.

## 2. Workbook structure

- `Contents` (sheet 1): 32 populated cells, C3:D23 — title/version, related datasets (including
  `Contents!C13` = "EVS 1990 Integrated Dataset. ZA4460, Version 3.0.0" ↔ `Contents!D13` =
  `doi:10.4232/1.10790`), and access notes.
- `EVS Surveys 1981-2017` (sheet 2): 2 352 populated cells, A1:N169 — one row per country × wave.
- Columns (row 1 headers): `A1` EVS Survey · `B1` Country/Region · `C1` ISO 3166-1 (embedded
  newline) · `D1` ISO 3166-1-alpha-2 code · `E1` ZANo in GESIS Data Collection · `F1` DOI in GESIS
  Data Collection · `G1` Principal Investigator · `H1` Data Collector · `I1` Fieldwork period ·
  `J1` Mode of data collection · `K1` Sample size · `L1` Weight · `M1` Datasets available as ·
  `N1` Languages fielded.

## 3. The exact Austria 1990 witness (reproducible primary cell provenance)

Austria appears four times: rows 6 (2017), 7 (2008), 8 (1999) and **9 (1990)**.

`EVS Surveys 1981-2017!A9:N9`:

| cell | header | value |
|---|---|---|
| A9 | EVS Survey | `EVS 1990` |
| B9 | Country/Region | `Austria` |
| C9 | ISO 3166-1 | `40` |
| D9 | ISO 3166-1-alpha-2 code | `AT` |
| E9 | ZANo in GESIS Data Collection | `4479` |
| F9 | DOI in GESIS Data Collection | `doi:10.4232/1.10790` |
| G9 | Principal Investigator | `Zulehner, Paul M. - University of Vienna, Austria` |
| H9 | Data Collector | `Fessel - GIK Institut (Vienna)` |
| I9 | Fieldwork period | `1990-04-09 to 1990-06-01` |
| J9 | Mode of data collection | `Face-to-face interviews with standardized questionnaire` |
| K9 | Sample size | `1460` |
| L9 | Weight | `yes` |
| M9 | Datasets available as | `Integration / Cumulation` |
| N9 | Languages fielded | `German` |

This is an exact, quotable public primary witness that the official GESIS method overview assigns
the **national Austrian 1990 study number ZA4479** and gives PI, data collector, fieldwork window,
mode, sample size and weight availability.

## 4. What the workbook does NOT contain — bounded negative

A whole-workbook term census over every populated cell of both sheets found:

| concept | occurrences |
|---|---|
| "frame", "design", "population", "citizen", "selection", "strat(ification)" as method text, "cluster", "respondent" | **0** |
| "weight" | only the header `L1` "Weight" and the `Contents!C6` field list; **no** weight construction, variable name or design |
| "sampl" | only the header `K1` "Sample size" and country labels such as "Germany - subsample East" |

The workbook therefore carries **no sampling frame, no sampling design, no target-population
definition (age/citizenship), no selection procedure, no stratification/cluster description, and no
weight-variable construction**. Column `K` is a bare sample-size count and column `L` is a yes/no
availability flag. The Austria 1990 design question is **not resolved by this workbook**, and no
methodology was inferred to fill the gap.

## 5. E02 contradiction clarified at documentary level

- `ZA4460` = **EVS 1990 Integrated Dataset** (`Contents!C13`, version 3.0.0, `doi:10.4232/1.10790`).
- `ZA4479` = the **Austrian national 1990 study**, appearing only at `E9` in the whole workbook.
- Column `E` is not uniform: Austria `4479`, Belgium `4461`, Bulgaria `4462`, Canada `4473`, while
  the other 1990 countries carry `4460` (the integrated dataset number). Column `F` carries the
  **integrated** DOI `doi:10.4232/1.10790` for **every** 1990 row.
- `ZA4754` occurs **nowhere** in the workbook.

So the "ZA4460 vs ZA4479" tension is a column-semantics mix, not a conflict: the national Austrian
study `ZA4479` and the integrated `ZA4460` are different objects, and this workbook cites the
national study number while citing the integrated DOI. That corroborates E02's national-catalogue
finding at primary level; it says nothing about ZA4754.

## 6. Evidence grade and limits

- **Primary/reproducible:** exact public URL, HTTP status, content type/length, workbook filename,
  sha256, sheet name, row/column/cell references, header text and cell values — all quoted above.
- **Not evidence:** the workbook's own metadata does not authenticate any `.sav` SRC12/SRC14
  SHA-256; it provides no variance calculation and no design fields, so no design-based inference
  is possible from it; and "Weight: yes" is an availability flag, not a weight specification.
- **Deliberately not done:** no raw survey, no `.dta`/`.sav`, no Library, no temporal calculation,
  no pair authority, no code change, no self-adoption, no re-download of the E02 PDFs, no
  reopening of the A048 question texts.
- **Terrain:** governed Mac, isolated sparse shared-store worktree, `HEAD f3b48775…`, clean worktree,
  public HTTPS retrieval only.

**Terminal:** `HQ258_E03_RETURNED__NO_SELF_ADOPTION`.
