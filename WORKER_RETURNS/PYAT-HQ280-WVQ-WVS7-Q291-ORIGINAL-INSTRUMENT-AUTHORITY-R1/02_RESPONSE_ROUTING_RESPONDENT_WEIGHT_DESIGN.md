# HQ280 WVQ — source-native response, eligibility, respondent and design qualification

**Evidence grade:** WVSA-authored Wave 7 English master instrument and WVSA-authored historical Variables Report recovered in public third-party accessible reproductions, **not** proved byte-identical to the retained 613-field WVS7.sav or to each country-specific fielded form. The official WVS public portal identifies separate Wave 7 and country documentation and national technical reports. No microdata read or actual Q291 asked-risk computation.

## The original distinction: Q291 is 18 items and a SELECTED-COUNTRY module

The WVS Wave 7 master, heading *Regional and Thematic Modules — 1. Political Trust Module*, labels **Q291** as the stem for 18 responses: parliament (`Q291P1` through `Q291P6`), government (`Q291G1` through `Q291G6`), United Nations (`Q291UN1` through `Q291UN6`). Exact subitem statements and codes are in `01`. This is not a single source-native Q291 response field, not a household attribute, not a 5x5 question, and not proof that two unknown derived I05 query refs use the battery. One interviewing **person** answers separate Likert-choice statements, if exposed.

Each Q291 subitem: 1 agree strongly, 2 agree, 3 neither, 4 disagree, 5 disagree strongly. The WVSA *Variables Report* Q291 section gives -1 don't know; -2 no answer; -4 not asked; -5 missing/not available. The earlier English master instead prints a **generic -3 not applicable (filter)** and generic -5 missing/not applicable for other reasons. These are distinct documentation layers; **do not silently turn codebook -4 into -3, or treat -3 as observed Q291 subitem value without a version/country dataset warrant.** WVS Wave 7 Q292's orientation is reversed (5 agree strongly, 1 disagree strongly) in this report; so any automatic Q291/Q292 pooled 5-point coding or directional interpretation is explicitly unwarranted. The five source responses are ordered agreement categories for *each statement*; shared category counts do not establish matching empirical meaning across subitems.

The Q291 module's description names a TrustGov (University of Southampton) pilot in Ethiopia, Iran, Kyrgyzstan, Myanmar, Nicaragua, Philippines, Tajikistan, Vietnam, Zimbabwe, with additional surveys proposed. This is a nonexhaustive historical list, not a retained-v6 66-country routing table. **Master inclusion does not prove source-native presence or exposure in the retained cross-national SAV**, and the early Variables Report says the pilot was in national datasets. Need each participating country's actual instrument, country/year/language, module installation, asked flags, filter application, and source-code dictionary across the retained release. `NOT_ASKED`, `NOT_APPLICABLE_FILTER`, `NO_ANSWER`, `DK`, `MISSING` must remain separate.

## Risk and sampling design

WVS surveys adults through national sampled interviews; the reporting unit of Q291 is the **individual respondent**. The master has an interview number, interviewer-recorded primary sampling unit (`I`), mode/language and geographic variables; a household-based selection method is not a household outcome unit. A two-variable `Q291Px × Q291Gy` operation requires verified **same respondent, both exact administered items** and a demonstrable denominator of eligible cases. The 97,220 global raw records are a file census, not the Q291 pilot asked-risk and not a denominator.

The retrieved historical WVS Wave 7 variables report names `W_WEIGHT` (weight), `S018` (country equilibrated to 1000) and `S019` (to 1500); the general WVSA weight documentation also discusses older `S017` country original weights and alternate S017A etc. **Never import the older general naming automatically into the specific 613-field retained release.** Publication-grade estimation requires identified release-native original country weight, country/year selection, PSU and stratum/cluster design, sample coverage, nonresponse and country-specific technical reports. `S018/S019` equal-sample normalization is not a country population weight, and mixed-country raw pooling has no self-evident estimand. The I05 R08 rule receipts refer to `RawUnweightedExactCountMeasureBasis@1.0.0`: that is a *historical RAW computational basis*, not representative weighting authorization or variance-method certification.

The original standard describes sample selection and country technical documentation, but **we did not retrieve/examine all national selection/weight protocols**. Therefore:
- source-native substantive item semantics: **DOCUMENTARY IDENTIFIED at English master/codebook-family level**;
- respondent unit: **DOCUMENTARY PERSON-level**;
- particular country/year/language/form asked-risk: **HELD**;
- actual two-component same-respondent overlap/denominator: **HELD**;
- country-justified weighted national estimator, pooled estimator, PSU/strata variance: **HELD**;
- any new original query or I05/46 eligibility: **NOT ISSUED**.

## Exact source URLs (public, source-authored content, delivery copies not checksum-verified)

- WVSA WVS7 documentation: https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp
- WVSA documentation structure: https://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=Documentation
- Master English, F00010738, Q291 page 23/27: https://www.scribd.com/document/477319701/F00010738-WVS-7-Master-Questionnaire-2017-2020-English-pdf
- WVSA-authored original variables report, Q291 page 101–105 (PDF indices 100–104): https://www.statsclass.org/dsci310/Tasks/WorldValuesData_Codebook.pdf
- WVSA latest joint page reporting Wave 7 v6 2024-05-01, 97,220 cases and 606 variables: https://www.worldvaluessurvey.org/WVSEVSjoint2017.jsp
- General WVSA weighting rationale: https://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=WEIGHT

**Custody note:** direct PDF screenshot requests for indices 100 and 102 were attempted and returned cache miss. PDF page-indexed text and independent questionnaire transcription were readable; page-image certification and an exact locally retained PDF SHA256 were not obtained. Do not claim visual or PDF-byte custody.
