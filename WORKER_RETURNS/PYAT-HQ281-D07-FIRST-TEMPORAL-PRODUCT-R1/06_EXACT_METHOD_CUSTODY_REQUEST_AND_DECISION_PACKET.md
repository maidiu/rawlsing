# D07 — single issuer-ready Ghana Q43/Q31 source-release and design-qualification request

**Delivery grade:** DECISION-READY DOCUMENTARY REQUEST, **NOT A GRANT**. This file is a bounded follow-on court to D07; it is not proof an outside source custodian has responded or a permission to open retained SAVs. Parent delivery: `e0b81aa2fc3520dfd0a645ac3db624e3235ef364`. The governing HQ decision remains `HQD-2026-10-10-280`.

## Selected original claim — frozen before result inspection

Two **independent Ghana national adult-citizen** Afrobarometer repeated cross-sections: `SRC02:R5:GH:Q43` (field May 8–27 2012) vs `SRC03:R9:GH:Q31` (field April 4–20 2022). The exact preselected question is **change in the weighted proportion self-reporting fairly or very satisfied with how democracy works**, relative to five substantive answers `{0,1,2,3,4}`. Category `0` ("Ghana is not a democracy") is a **substantive reported judgment** retained in its own cell, **not investigator objective assessment, missingness or dissatisfaction**. Separate DK, refusal, not-asked and unascertained; R5 refusal `998` and R9 refusal `8` in merged codebooks must not be merged by numeric value. No numerical change or sign has been inspected or approved.

**Official country-English questionnaire evidence already located:** `https://www.afrobarometer.org/wp-content/uploads/2022/02/gha_r5_questionnaire.pdf` (finalized April 19 2012, Q43 PDF index 8), `https://www.afrobarometer.org/wp-content/uploads/2023/06/GHA_R9.Indigenized-Questionnaire-_30mar22-FINAL.docx.pdf` (revised March 30 2022, Q31 PDF index 12). Both contain the relevant 0–4 + DK9 topology, immediately follow the prior democracy-classification question and instruct the interviewer to say "democracy" in English, translating into the local language if not understood. Original PDF index text confirmed; visual PDF screenshot retrieval unavailable, no full translation/deployment logs certified. **Do not spend another owner cycle re-searching the 2012 Ghana country English questionnaire.**

## One consolidated missing bridge, three separate authorities (cannot be silently conflated)

**Docket key:** `GHANA_Q43_Q31_EXACT_RETAINED_RELEASE_NATIONAL_DESIGN_ESTIMAND_BRIDGE_R1`.

| Competent party | Exact question/request | Required return, pass/refusal |
|---|---|---|
| **Afrobarometer Data Management + original Ghana round survey owner (CDD-Ghana)** | For 2012 R5 and 2022 R9, identify exact original official **merged-round release/accession and version**, published Ghana Q43/Q31 country-domain variable names and data dictionary; whether original official merged samples include every eligible Ghana record, any supplements, filtering; official design strata/EA/PSU fields, intended Ghana within-country weight and calibration; fielded English version, local-language deployment/protocol revisions, routing, DK/refusal and missing coding; field response and substitution. | Primary official release manifest/revision and country method/field protocol. If fields withheld from public microdata, explicitly state which are withheld, which public-use variance/inference statements remain authorized and where restricted design metadata may be obtained. Archive URLs alone or citations of a country-only file with a merged file's name are **not** sufficient. |
| **Rawlsing retained-source/forensic custody owner, under separately issued source-read warrant** | Authenticate retained physical merged files `SRC02` **SHA256 `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`** and `SRC03` **SHA256 `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8`** against the *custodian-provided official merged release identity*, with lawful non-row file/provenance metadata first. Precisely bind frozen source version, actual Ghana-only selection, Q43/Q31 field, routing and weight/design columns; check that the retained file is **not silently replaced**. | Exact hash, provenance/accession/version and column/record inclusion mapping, signed source-read decision. A public Ghana-only `.sav` (even with n=2400) **does not prove** identical bytes to Rawlsing's retained merged-round SAV. External custodians cannot cryptographically certify private Rawlsing byte roots they have not received; they certify *their* release evidence, while the internal owner certifies the bridge. This worker **has no independent authorization to inspect rows or bytes**. |
| **Independent authorized survey-statistics and measurement-comparability reviewer** | Given both official method records, determine whether adult Ghanaian citizens 18+ valid-item satisfaction shares are population-interpretable under the actual PPS / cluster / strata designs and changing 2010 vs 2021 census frame; whether person selection (numbered card vs tablet), 2012 72.9% vs 2022 94.23% response, wording/presentation/translation, sample inclusion, original response process and weight methodology support a **single positive crosswave estimand**. State design-based variance/uncertainty procedure, including unavailability of released PSU/strata or calibration metadata. | Exact affirmative qualified measurement+design estimand decision **or** named necessary missing witness / source-proven incompatibility at the specified estimand. If only point-description is defensible, mark quantified uncertainty unavailable, **not** a confidence interval or "no change." This is scientific recommendation, *not itself a source-execution or EE12/C7 permission*. |

**Distinct competent EE12/C7 issuer after the bridge:** The HQ-authorized source-semantic/comparison decision owner (not D07, not the questionnaire publisher alone and not an implementation test) must issue a scoped, authentic positive `SOURCE_SEMANTIC_EQUIVALENCE` or equivalent explicit comparison/estimand/source-universe target-use relation on the verified exact two per-wave products, with justified method transformations. A retained `PROVENANCE_ORIGIN` or `HARMONIZATION_ALIAS` is **nonauthorizing**; a comparability relation is not automatically a linkage/pooling claim. Source-read permission and intended N9 context-only consumer permission remain separate.

## The minimum acceptable decision-return schema

```json
{
  "docket": "GHANA_Q43_Q31_EXACT_RETAINED_RELEASE_NATIONAL_DESIGN_ESTIMAND_BRIDGE_R1",
  "source_a": {
    "physical_root_SHA256": "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651",
    "official_merged_release_ref": null, "release_date_or_version": null,
    "release_to_SHA_custody_receipt": null,
    "GHA_inclusion_selector": null, "Q43_native_column": null,
    "eligible_asked_rule": null, "weight_column_and_authority": null,
    "stratum_PSU_sampling_unit_refs": null
  },
  "source_b": {
    "physical_root_SHA256": "3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8",
    "official_merged_release_ref": null, "release_date_or_version": null,
    "release_to_SHA_custody_receipt": null,
    "GHA_inclusion_selector": null, "Q31_native_column": null,
    "eligible_asked_rule": null, "weight_column_and_authority": null,
    "stratum_PSU_sampling_unit_refs": null
  },
  "instrument_language_and_response_equivalence_decision": null,
  "target_population_and_design_compatible_decision": null,
  "variance_or_typed_unquantified_state": null,
  "statistician_signed_estimand_decision": null,
  "custodial_source_read_authorization": null,
  "positive_EE12_claim_target_use": null,
  "decision": "HELD_MISSING_EVIDENCE_NOT_SCIENTIFIC_NONCOMPARABLE"
}
```

**Receipt requirements:** signed named issuer/principal; source identity/date/version/hash where permitted; actual original question-language/form/response/risk; denominator, weighting/variance and eligibility decision; exact uncertainty or **typed withholding**; positive/negative permission distinct from missing evidence; decision date/as-of; target-use and limits; provenance and replay locator. Unknown stays null with reason; never replace it with `0`, `NONCOMPARABLE` or assertion of source-proven no change.

## On acceptance: one bounded product-producing commission, still separate

Commission the existing source execution owner (only with authorized source-read) to publish separately `GHA_R5_Q43_WEIGHTED_FIVE_CATEGORY_FACT` and `GHA_R9_Q31_WEIGHTED_FIVE_CATEGORY_FACT`, with native categorical cells, asked/valid/invalid denominators and weight/design variance records; an independently issued **EE12/C7** positive pair decision; an actually current/adopted **N8E** operation calculating `p2022-p2012` with warranted uncertainty; a real **N9** consumer limited to reported-attitude historical context with selected source-dependency as-of/replay and no N8S objective causal promotion. Test a changed release to verify selective invalidation. No work on private rows, no sign and no downstream actor use until warrants exist.

## Exact refusal ordering

1. If official original merged-release identity or Rawlsing SHA bridge is not authenticated: **HOLD_SOURCE_CUSTODY**; do not open records or claim comparison.
2. If original weights, sample inclusions, strata/PSUs and inference cannot be resolved: **HOLD_DESIGN_AND_ESTIMAND** or separately signed qualified limited descriptive estimand, not invented confidence.
3. If wording/translation/form/target population is found scientifically incompatible by a competent issuer: **EXACT_ISSUED_NEGATIVE_FOR_DECLARED_ESTIMAND**, with necessary-condition proof; otherwise **HOLD_MISSING_METHOD**.
4. Even with all methods qualified, absent a separate positive EE12/C7 operation-specific authorization: **HOLD_EE12_ISSUER**.
5. Even with EE12, absent two actual per-wave products/current N8E code/actual N9 receipt: **HOLD_PRODUCT_OR_CONSUMER**, not success.

**Source references:** D07 `00`/`01`/`02`/`03`, inherited D03 `05_ALL63_SCOPE_AND_PREREQUISITES.json`, selected Afrobarometer Ghana country-original PDF links above. Not a replacement for private data-release custody.
