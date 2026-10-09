# HQ258 E03 — Austria 1990 method qualification

Scope: what the official public GESIS method workbook does and does not establish for the Austrian
1990 EVS survey, separated into **explicit workbook cells** and **inference** (none used).

Primary witness: `ZA7503_Method_Information.xlsx`, `sha256 401048862995440764950a3fa3ec9ec5349bff674a58de7725db848de6655734`,
retrieved from both `https://access.gesis.org/dbk/70780` and `https://access.gesis.org/dbk/70775`
(byte-identical), sheet `EVS Surveys 1981-2017`, row 9 (`A9:N9`), headers row 1 (`A1:N1`).

## 1. Explicitly established by cell values (primary, quotable)

| field | cell | value |
|---|---|---|
| wave | `A9` | `EVS 1990` |
| country | `B9` | `Austria` |
| ISO numeric / alpha-2 | `C9` / `D9` | `40` / `AT` |
| **national GESIS study number** | `E9` | **`4479`** |
| DOI cited by the row | `F9` | `doi:10.4232/1.10790` (the EVS 1990 **Integrated** dataset DOI) |
| principal investigator | `G9` | Zulehner, Paul M. — University of Vienna, Austria |
| data collector | `H9` | Fessel - GIK Institut (Vienna) |
| fieldwork period | `I9` | 1990-04-09 to 1990-06-01 |
| mode of data collection | `J9` | Face-to-face interviews with standardized questionnaire |
| sample size | `K9` | 1460 |
| weight | `L9` | `yes` (availability flag only) |
| datasets available as | `M9` | Integration / Cumulation |
| languages fielded | `N9` | German |

At documentary level this **corroborates E02**: the official 1990 Austrian national study number is
`ZA4479`, distinct from the integrated 1990 dataset `ZA4460` cited in `Contents!C13`
("EVS 1990 Integrated Dataset. ZA4460, Version 3.0.0" ↔ `doi:10.4232/1.10790`). The workbook's
`E` column is not uniform across the 1990 cohort (30 rows): Austria `4479`, Belgium `4461`,
Bulgaria `4462`, Canada `4473`, and 26 countries `4460`; the `F` column cites the integrated DOI for
every 1990 row. `ZA4754` occurs nowhere in the workbook.

## 2. NOT established by this workbook (the bounded gap)

The workbook contains **no** sampling frame, sampling design, target-population definition
(age/citizenship), selection procedure, stratification or cluster description, primary sampling
unit structure, or weight-construction description. Whole-workbook census: 0 cells containing
"frame", "design", "population", "citizen", "selection", "cluster" or "respondent"; "weight" occurs
only as the `L1` header and the `Contents!C6` field list; "sampl" occurs only as the `K1` header and
country labels such as "Germany - subsample East".

Consequences that must not be papered over:

- `K9 = 1460` is a **count**, not a design. It does not tell us the sampling frame, the stages, the
  selection probabilities or the target population.
- `L9 = yes` is an **availability flag**, not a weight specification. It does not name a weight
  variable, state whether it is design or post-stratification, or permit any variance calculation.
- The fieldwork window and mode are descriptive metadata; they do not characterise the sample design.
- The workbook's own metadata (title "1981-2008 - Method Information (v1)", modified 2022-12-15,
  `Contents!C4` "(Version 6, December 2022)") does not authenticate any collected data file hash.

## 3. Separating explicit cells from inference

- **Explicit**: everything in §1, quoted directly from named cells of a checksummed public workbook.
- **Inference**: none was used to fill the design gap. In particular, the wave-general EVS 1990
  cross-national design (whatever it may be) was **not** projected onto the Austrian national
  survey, because the workbook provides no national design statement to project from or to test
  against. Any such projection would be invention.

## 4. What this does and does not authorise

- It **does** give HQ an exact reproducible primary witness (URL, HTTP receipt, sha256, sheet, row,
  cells, header text) that a methods reviewer can verify directly from the public catalogue.
- It **does not** grant any pair authority, temporal sign, reported probability, EE14 model use, F8
  producer custody, or raw/Library access; it is public documentation only.
- It **does not** resolve the Austria 1990 sampling/design/weight question; see
  `03_NEXT_SCIENTIFIC_EDGE_OR_CUSTODIAN_REQUEST.md` for the precise next official request.

## 5. Evidence ceiling

This qualification is documentary. The decisive design fields are not in the public workbook, so no
statement about the Austrian 1990 sampling design, weighting or target population is made here at
all — positive or negative beyond "absent from this document".
