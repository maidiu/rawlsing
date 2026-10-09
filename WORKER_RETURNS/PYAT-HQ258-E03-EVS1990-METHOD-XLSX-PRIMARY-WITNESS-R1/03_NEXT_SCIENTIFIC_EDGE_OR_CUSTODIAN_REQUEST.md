# HQ258 E03 — next scientific edge and custodian request

## 1. Where the evidence stops

The E03 primary witness (see `00_…` and `01_…`) fixes the Austrian 1990 **identity and administrative
metadata** exactly: national study `ZA4479`, PI Zulehner, data collector "Fessel - GIK Institut
(Vienna)", fieldwork 1990-04-09 → 1990-06-01, face-to-face standardised questionnaire, sample size
1460, weight *available*, German. The public method workbook contains **no sampling frame, no design,
no target-population definition, no selection procedure and no weight construction**, so the
Austria-specific method question remains open and is **not** answerable from this document.

## 2. Precise official custodian request (bounded, public-documentation only)

Request from GESIS – Leibniz-Institut für Sozialwissenschaften (Data Catalogue / EVS archive) the
**study-level documentation for the Austrian 1990 national survey `ZA4479`**, and separately the
**EVS 1990 integrated study description**:

1. **ZA4479 study description / technical report (Austria 1990)** — specifically:
   - sampling frame (register, register type and coverage);
   - sample design (stages, primary sampling units, stratification variables, cluster structure);
   - target population definition (minimum age, citizenship/nationality, institutionalised
     population treatment, regional coverage);
   - selection procedure at each stage and any substitution rules;
   - achieved vs issued sample (the 1460 figure's status: interviews, respondents or net sample);
   - weighting: exact weight variable name(s), design vs post-stratification, calibration
     variables, and whether a design weight is separately provided.
2. **ZA4460 EVS 1990 integrated dataset study description / codebook front matter** — the
   cross-national design and harmonisation statement, so the Austrian national design can be read
   against the integrated one rather than projected from it.
3. **Any EVS 1990 national methodology annex for Austria** held by the archive (e.g. the national
   fieldwork report) if it exists as public documentation.

Requested format: public PDF/HTML documentation from the GESIS Data Catalogue record for `ZA4479`
and `ZA4460`, cited by DOI `doi:10.4232/1.10790` (integrated 1990) and by the `ZA4479` catalogue
record. The already-verified XLSX (`ZA7503_Method_Information.xlsx`,
`sha256 401048862995440764950a3fa3ec9ec5349bff674a58de7725db848de6655734`, from
`https://access.gesis.org/dbk/70780` and `/70775`) can be cited to the custodian as the document
that names `ZA4479` but not the design.

**Access note for the custodian:** the two catalogue URLs return the same workbook; the entry
labelled "1981–2008 Method Overview" is served the updated Version 6 (December 2022) file whose data
sheet is `EVS Surveys 1981-2017`. If an earlier 1981–2008-only edition exists, it would be useful to
know whether it carried any column this version lacks.

## 3. Why this is the correct next edge, and what it is not

- It is the **smallest** step that can resolve the open Austria-1990 design question: the design
  fields are simply not in the public overview workbook that E02 identified as decisive, so the
  next artefact must be study-level documentation.
- It is **not** a raw-data request: no `.sav`/`.dta`, no respondent microdata, no Library access,
  no re-analysis. The request is for public methodology text only.
- It is **not** an inference: no EVS wave-general design is projected onto Austria, and no design
  is invented to fill the gap.
- It does **not** carry pair authority, a temporal sign, a reported probability, EE14/T1 model use,
  F8 producer custody, native F7 or any AT07 issuer authority.

## 4. Decision options for HQ

1. **Forward the exact primary witness** (URL receipt + sha256 + `EVS Surveys 1981-2017!A9:N9`) to an
   independent scientific methods reviewer as the reproducible public provenance for the
   `ZA4479` identity — it needs no further local work.
2. **Issue the bounded custodian request** in §2 for the `ZA4479`/`ZA4460` study descriptions if HQ
   needs the actual sampling/weighting design.
3. **Hold** the Austria-1990 design question open; do not represent the workbook's `Weight: yes`
   flag or `Sample size 1460` as a design statement in any downstream return.

**Terminal:** `HQ258_E03_RETURNED__NO_SELF_ADOPTION`.
