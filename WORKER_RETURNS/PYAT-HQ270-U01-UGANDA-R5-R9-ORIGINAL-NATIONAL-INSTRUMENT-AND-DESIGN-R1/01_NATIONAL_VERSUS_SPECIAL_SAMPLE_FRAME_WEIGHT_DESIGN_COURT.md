# HQ270 U01 — Uganda R5/R9 national vs supplemental sample, frame and weight/design court

**Scope:** documentary survey design only; no respondent data, no national trend or inferred measurement.

## National target and independently repeated waves

Both documentary technical information forms name **Ugandan citizens aged at least 18, excluding institutionalized residents**. This is a *coverage-defined* target, not all people living in Uganda, not refugees/noncitizens and not a panel. Note the need to audit real coverage, exclusions, translations and substitutions before claiming equal implemented coverage.

| Dimension | R5 Uganda (field 2011-12-02 to 2012-02-27) | R9 Uganda (field 2022-01-07 to 2022-01-25) |
| --- | --- | --- |
| National **probability** target | **2,400** adult Ugandan citizens | **2,400** adult Ugandan citizens |
| Separate extra | **3,800** USAID Uganda mission focus-district targeted oversample; total fieldwork **6,200** | **992** in **10** new city administrations; total fieldwork **3,392** |
| Frame | UBOS **2002 Population and Housing Census**, 2011 projected population (R5 summary says 2010 projections; document-year reconciliation required) | **2014 Uganda National Population and Housing Census**, UBOS |
| Stratification | Five reported areas incl. Kampala as separate, by urban/rural; TIF labels **region × urban/rural** | **Sub-region × urban/rural** |
| PSU selection | Probability proportionate to population size | Probability proportionate to population size |
| Clustering | National **300 EAs × 8 interviews** (R5 summary); country TIF 8 per PSU | 8 households/respondents per PSU; national PSU roster and IDs must be explicitly confirmed |
| Household choice | Random walk; R5 Uganda TIF | Random start points + 5/10 walk interval (R9 TIF and field instrument) |
| Individual choice | Alternating male/female interview quota; selection from eligible persons via numbered card | Alternating gender quota; tablet randomly selects eligible within household |
| Interview mode | Face-to-face; Wilsken Agencies | Face-to-face; Hatchile Consult Ltd. |
| Translation | R5 official TIF lists **14 languages** (Luganda, Runyankole-Rukiga, Runyoro-Rutooro, Lugbara, Alur, Luo, Ateso, Ngakirimojong, Lumasaba, Madi, Lugwere, Kupsabiny, Lusoga, Japdhola) | R9 TIF lists **15 named survey-language options** when separations counted; questionnaire consent English, Alur, Lugbara, Langi/Acholi, Ngakarimojong, Ateso, Lumasaaba, Lusoga, Luganda, Runyankore/Rukiga, Runyoro/Rutooro, Japadhola; technical-form vs interview-script list differs in aggregation |
| Reported contact/cooperation/refusal/response | 89.9% / 96.2% / 3.69% / 86.5% | 96% / 86% / 3% / 82%; **EA substitution 2.4%, 10 EAs**, including limits from flooded, inaccessible/refugee/restricted areas |

**Evidence:** R5 country codebook June 2012 printed p. 2 and pp. 3,60: https://www.afrobarometer.org/wp-content/uploads/2022/02/uga_r5_codebook.pdf ; R5 official published national-only summary pp. 1–2: https://www.afrobarometer.org/wp-content/uploads/2022/02/uga_r5_sor.pdf ; R9 summary PDF index 1–4, technical form printed p. 4: https://www.afrobarometer.org/wp-content/uploads/2023/08/UGA_R9_Summary-of-results_Afrobarometer-9aug23.pdf ; R9 country questionnaire PDF indexes 1–4: https://www.afrobarometer.org/wp-content/uploads/2023/06/UGA_R9.Indigenized-questionnaire_29Dec21-Final.docx.pdf . **PDF screenshot verification failed** (index text only). Web-page Afrobarometer survey summaries independently confirm national/extra counts: https://www.afrobarometer.org/publication/uganda-round-5-summary-of-results/ and https://www.afrobarometer.org/publication/uganda-round-9-summary-of-results/ .

### Source-version conflict: respondent ID ranges are not sample flags

- R5 **country** June 2012 codebook `RESPNO = UGA0001–UGA6200`, national TIF `n=2400`, while R5 merged 2015 codebook enumerates irregular UGA respondent-ID ranges and the 2012 Uganda summary says only 2,400 used. **The ID range cannot be used to construct the national subset** absent exact approved selection metadata.
- R9 Uganda April 2023 country codebook `RESPNO = UGA0001–UGA3392`; R9 2023 summary TIF lists 3,392 but states substantive national tables derive from 2,400. World Bank's 2025-catalogued Uganda R9 file `UGA_R9.data_.final_.wtd_release.19Jun22_Updated.7Nov23.sav` is listed with **2,400 cases**, 394 variables; a separate 3,392 country codebook is **not** proof of the archive's exact 2,400 national selector nor of the Rawlsing R9 SAV version. Link https://microdata.worldbank.org/catalog/6756/data-dictionary/F1 .
- R9 summary printed p. 5 states reported Q1–Q97 frequency tables are **weighted** and uses national n=2,400, while its TIF lists sample 3,392; analysts must reconcile **which universe and version every published frequency table represents**.
- Neither codebook provides in the consulted text a certified variable that flags national vs supplemental origin, an explicit PSU/stratum design key guaranteed unique within each universe, or proof that a particular archived Rawlsing file already excludes the supplemental observations. **Do not infer sample selection from numeric identifier cut-offs, row order, “urban” flags, mere respondent counts or urban residency.**

### Weights: not fungible, not automatically validated

- **R5:** Uganda-specific codebook printed p. 60 defines `withinwt` as within-country selection-probability factor adjusting region, gender, urban/rural, household size and EA size. **But the R5 technical form printed p. 2 has an empty `Weighting:` field**, so actual final weight provenance/use needs adjudication. It must be shown applicable to the national-only observations and the retained archived dataset, not simply that a column exists.
- **R9:** Uganda country codebook last two PDF pages defines **`withinwt_ea` (“old AB withinwt”)** vs **`withinwt_hh` (“new AB withinwt”)**, with `withinwt_hh` additionally adjusting **ADULT_CT**, the count of adult citizens in the household. R9 TIF says weighted for individual selection probabilities. Source protocol must decide which is nationally appropriate at target release, and whether weights were calibrated/recomputed after extra-city sample separation. Choosing the older/newer by name alone is not authorized.
- **Cross-check risk:** R9 summary and R9 codebook's displayed unweighted/weighted demographic summaries should not be presumed to describe the same all-case fieldwork universe or exact release. R9 summary lists very different urban totals before vs after weighting; the codebook's final comparison differs. This is a positive reason to demand exact provenance, **not** to pick a convenient table.

Afrobarometer's official guidance says use within-country weights for national descriptive statistics and reserve merged `Combinwt` for standardized cross-country comparison: https://www.afrobarometer.org/surveys-and-methods/sampling/ . It does **not** answer the Uganda two-oversample case by itself.

### Variance and actual nationally defensible analysis

For **each independent wave separately**, owner must certify: national record inclusion identity; national adult-citizen universe; frame/version/date; PPS draw and PSU ID; stratum ID; household/respondent probability and quota practice; exclusions, substitutions, nonresponse; exact released analytic weight and calibration; response coding. No linear frequency-based / IID-binomial SE may be substituted for a complex-design estimator. Compute, under separately authorized respondent-backed execution, design-weighted `p_t = Pr(response=2 | response ∈ {1,2}, target nation_t)` and **survey-design SE and 95% CI** for `p_R9-p_R5` using independent wave designs; assess effective sample and design effect and pre-specify handling of DK/refusal/missing and associated bounds/sensitivity. Rescaled national weights must not turn the 3,800 or 992 extras into general national probability draws.

### Residual documentary requests to source custodian

Afrobarometer Data Management with Uganda country survey owners should supply **both waves**: (a) final national vs supplement inclusion flags/record manifest and national-release file identities, (b) stratum/PSU design variable names and uniqueness and geographic-crosswalk design, (c) final weight recipe (R5 `withinwt`, R9 `withinwt_ea` vs `withinwt_hh`) and intended population(s), (d) survey technical field implementation forms and substitution audit, (e) deployment translations, (f) full questionnaire revisions, (g) explicit accession/release identity and mapping to archived Rawlsing R5/R9 SAVs. Before those, national trend and design-based confidence assertions are held.
