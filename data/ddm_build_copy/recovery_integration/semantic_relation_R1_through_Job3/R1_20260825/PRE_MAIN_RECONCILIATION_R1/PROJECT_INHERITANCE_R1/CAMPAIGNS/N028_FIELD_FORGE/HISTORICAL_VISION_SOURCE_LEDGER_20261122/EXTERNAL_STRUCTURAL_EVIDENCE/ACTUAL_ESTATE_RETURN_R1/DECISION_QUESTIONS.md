# DECISION QUESTIONS — exact source references
No implementation choice is made here. These are the remaining source-to-function questions that require owner/receiving decision after the actual-file evidence.

## ES01 — EPR Core
1. Which release is admitted for group-conditioned disposition evidence: `EPR_DATASET_FAMILY/2021/core/EPR-2021.csv` or `.../2023_beta/core/EPR-2023.csv`? The 2023 beta adds 2022–2023 and has no official 2023 codebook in custody (`EPR_2023_Codebook_EPR.pdf` 404).
2. Which fields are used for a group-power interval profile: `size`, `status`, `umbrella`, `reg_aut`, with `from`/`to` as inclusive years, and `gwgroupid` as the stable key? The 2021 and 2023 beta coding must be compared before choosing, not silently merged.
3. Destination: existing S06.2/S06.4/PYAT group-conditioned disposition owner or independent context retrieval; no new EmpiricalFact is implied by the table alone.

## ES02 — GeoEPR
4. Is region-level settlement geometry (`GeoEPR-2021.geojson`, `GeoEPR-2023.geojson`, properties `gwgroupid`, `type`, `sqkm`, geometry) sufficient for the intended locality-qualified context, or is the absence of a geometry engine/overlay a blocker? Geometry validity and overlaps are unchecked.
5. How should no-geometry and Statewide/Regional categories be typed? `type` value codes and null geometry counts are in `VALUE_CODES.tsv` and `COVERAGE.tsv`; they are not population or local dominance.
6. Destination: ES01 spatial context or world-owner reader; not a density or local-dominance generator.

## ES03 — EPR-ED
7. Which ED dimension is admissible for a group crosswalk: `religion1–3`/`rel*_size`, `language1–3`/`lang*_size`, or `phenotype1–3`/`pheno*_size`? The dimensions are not interchangeable and ED group identity is not individual identity.
8. What exact EPR/TEK group-key correspondence is permitted beyond `gwgroupid`? No name-only crosswalk or imputation to omitted groups is evidenced.
9. Destination: S06.2/PP26-15/16 group semantic and crosswalk owner; not a respondent identity join.

## ES04 — EPR-TEK
10. Which `tekid`/`gwgroupid` links are used, and at what scope? The link is nominal kin, not migration, money flow, alliance, contact, solidarity, or causal pressure. The 2023 Atlas/codebook are 404.
11. Destination: cross-border formation/relation owner (S06.2/PP26-16/18), with the link type and scope explicit.

## ES05 — RAS3
12. Which state-religion dimensions are admitted: `SAX{y}` official religion, `SBX{y}` official support, `NX01X{y}`/`MX01X{y}` restrictions, `LX01X{y}` religious marriage/divorce, `VFUNDINGX{y}` funding, `VOFFICE01X{y}` office oaths? These are expert codes, not law text or private belief.
13. Which years are selected (1990/2000/2010/2014 and/or X endpoints)? Coverage and missingness are in `COVERAGE.tsv` ES05; no interpolation is authorized.
14. Rights: no explicit RAS license found. Is written provider clarification required before any external publication/reuse beyond local evidence?

## ES06 — RASM3
15. Which minority-level discrimination series are admitted (`MMX01X`, `MMX02X`, `WZSOCDIS01X`, `WZMIN2MAJ01X`, `WZGENERALX`), and how is the 771-minority universe compared with EPR/ED without name-only matching?
16. Which country-minority key is stable enough for group-differentiated institutional context? No imputation to omitted groups is evidenced.

## ES07 — RAS Constitutions
17. Which constitutional provisions are admitted (`coff`, `coffestab`, `csras01x`, `creldis01x`, `cfree01x`, `claws01x`) and at which years? Provision alone is not operative sanction, enforcement, or practical access.
18. Enactment vs effective dates are not separate fields in this array. Is a separate date source required before any temporal panel use?

## ES08 — WBL
19. Which WBL version and pillar set is admitted: WBL 1.0 historical `WBL_index`/`GR1–GR8`, WBL 2024 legal/supportive/EO, or WBL 2026 `LF_econ_index`/`SF_econ_index`/`EP_econ_index` and topic scores? Versions/methodologies must not be silently combined.
20. Are legal question variables (`*_qs`, `*_is`) or composite indices the evidence unit? A composite is not a provision; legal scope/exceptions and actual enforcement are separate.
21. Which WBL 2024 expert-respondent records, if any, are admitted? They are reserve and cannot be converted into population facts.
22. Rights: confirm WBL dataset/report reuse terms and any third-party restrictions before publication.

## ES09 — ILOSTAT
23. For each selected indicator, is the file observed, 19th-ICLS, or modelled? The indicator ID and `obs_status` (present in 83/93 files) must be checked; files without `obs_status` need an explicit typed absence.
24. Which reference areas are admissible: ISO-3 countries only or also `X…` regional/aggregate codes? `ref_area` is in `COVERAGE.tsv`; no automatic country/aggregate merge.
25. Maternity protection: `EES_XPLV_SEX_RT_A` is parental leave, not maternity protection. Is a different source required for the maternity-protection requirement?
26. Destination: ES09/10 contextual labour-position qualification to FF01 or independent context retrieval; no individual control/employment-relation inference.

## ES10 — JOIN
27. Which JOIN indicators are comparable to ES09 estimands? Same label does not mean same survey instrument, denominator, or year. `Survey Data Source`, `Survey Type`, `Subsample`, and quality flags must be carried.
28. Are `Subsample` margins usable as published, or is a country-year `All` row required? No averaging or duplicate evidence is authorized.

## ES11 — WID
29. Which series/percentiles are admitted: `sptinc992j` p90p100/p99p100, `shweal992j` p90p100/p99p100, `aptinc992j`/`ahweal992j` p0p100, `spllin992j`/`spkkin992j` p90p100, `tptinc992j` p99p100? Units, age, population unit and PPP basis come from per-country metadata and must not be mixed.
30. Which geography set is admitted: current ISO-3 countries, historical units, subnational regions, or regional aggregates? WID includes all four.
31. Rights: WID public pages are ambiguous (third-party CC BY-NC-SA vs CC BY). Is written confirmation required?

## ES12 — Findex
32. Which published subgroup axes are admitted (`group`/`group2`: gender, age, education, labour force, income, urbanicity)? Only published margins exist; no joint distribution may be reconstructed.
33. Which waves are used: 2011, 2014, 2017, 2021, 2024? The 2022 observations belong to the 2021 round; no silent re-labeling.
34. Destination: contextual financial-access/resource-capacity profile to FF01 or world owner; no actor-level savings/credit assignment.

## ES13 — Enterprise
35. Which universe is admitted: global-methodology, historical non-global, or informal-city indicator database? They are distinct and not nation-representative where city-only.
36. Which variables are enterprise-context (size, ownership, exporter, sector, finance, infrastructure, constraints) versus worker outcomes? The firm is not the worker.
37. Are any raw firm records needed? They remain unprofiled/unextracted; the selected aggregate indicator DBs are sufficient only for employer-context distributions.
38. Rights: capture Enterprise-specific terms before publication; the general World Bank license page is retained but survey-specific terms were not found.

## ES14 — V-Dem
39. Which indicators are admitted for civil-society/labor/assembly/expression/media/religion/repression context: `v2csreprss`, `v2cseeorgs`, `v2cscnsult`, `v2csprtcpt`, `v2x_cspart`, `v2xcs_ccsi`, `v2x_frassoc_thick`, `v2caassemb`, `v2x_freexp_altinf`, `v2meslfcen`, `v2clrelig`, `v2csrlgrep`, `v3cllabrig`, `v2cltort`, `v2clkill`, `v2edteunion`, `v2edteunionindp`?
40. Are uncertainty fields (`_codelow`, `_codehigh`, `_sd`) carried into any reader? They must not be collapsed into a point fact without a decision.
41. Destination: S06.2/PP26-16/18/19 independent institutional context, not a generic democracy score or automatic repression rule.

## Cross-source
42. Does the same country-year in ES09 and ES10 refer to the same survey instrument? Evidence does not establish a same-survey crosswalk; source/quality fields differ.
43. Which ES01–ES07/ES14 group or institutional relation needs a real crosswalk, and which is only contextual association? No name-only or respondent-identity crosswalk is evidenced.
44. Which facts route directly to the world owner rather than through FF comparison? The source map's existing owner destinations remain controlling; this return does not choose.
