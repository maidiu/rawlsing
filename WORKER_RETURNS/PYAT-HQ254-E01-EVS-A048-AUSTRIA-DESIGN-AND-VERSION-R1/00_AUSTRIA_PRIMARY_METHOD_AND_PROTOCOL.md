# PYAT HQ254 E01 — Austria A048 primary method, design and administration court — R1

**DISPOSITION:** `DOCUMENTARY_QUALIFICATION_PARTIAL__PAIR_NOT_READY`  
**TERMINAL:** `HQ254_E01_RETURNED_FOR_HQ_REVIEW__NOT_ADOPTED`  
**COMMISSION:** `a264c028a7921bb92e5ab56b4d79399f4149a09f`  
**BRANCH:** `agent/rabochii-pyat-hq254-evs-a048-design-version-r1`  
**SEALED HQ254:** `20261008-PYAT-HQ254-T01-T0-POSITIVE-FIVE-PARALLEL-ISSUED-R1 @ 6072a6891f47e713df0f70f0dec8770fc0abac32`  
**RAW SURVEY ACCESS:** NONE. No SAV/DTA opened, no wave value calculated, no pair authority issued.

## 1. Authority and frozen repo witnesses

The commission authorizes documentary qualification only and explicitly forbids re-retrieving the already recovered Austrian A048 wording, raw survey access, wave-value production and self-granted comparability. Witness: `WORKER_COMMISSIONS/PYAT-HQ254-E01-EVS-A048-AUSTRIA-DESIGN-AND-VERSION-R1/00_COMMISSION.md @ a264c028a7921bb92e5ab56b4d79399f4149a09f`, blob `e1532068fd37387c796764dd77af11643e436ed2`, lines 15–35.

Sealed HQ254 names this exact E01 row at `a264c028a7921bb92e5ab56b4d79399f4149a09f` and keeps the EVS 1990/2008 pair pending national sampling/weight, exact frozen versions and pair relation. Witness: `HQ_HANDOFF/checkpoints/20261008-PYAT-HQ254-T01-T0-POSITIVE-FIVE-PARALLEL-ISSUED-R1/CURRENT.md @ 6072a6891f47e713df0f70f0dec8770fc0abac32`, blob `e64ffa47922cd7361b87fc8d780600532cb04259`, lines 20 and 28.

HQ253 is the only instrument-text witness used here. It records the 1990 national field-questionnaire identity `ZA4479`, the 2008 national identity `ZA4754`, the same target clause/substantive direction, and a protocol difference: the visible 1990 national block is read aloud with no visible independent card instruction while 2008 explicitly uses Liste 53 plus oral reading. It also leaves national 1990 design/weight and byte→release identity unresolved. Witness: `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ253_R01_R02_INDEPENDENT_INTAKE_AUSTRIA_PRIMARY_SCAN_AND_T0_FIRST_TEST_R1.md @ 85f2835dc5b26735ed9ed36a6cb52ee11fc5abea`, blob `db045dff5d4340faa9abe604ef6e0cc8fe1f2c9e`, lines 26–38. **No questionnaire was re-retrieved in E01.**

Retained physical identities remain exactly:
- SRC12 `EVS 1990.sav`, 24,341,244 bytes, SHA-256 `66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec`.
- SRC14 `EVS 2008.sav`, 63,832,833 bytes, SHA-256 `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`.

Witness: `data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SOURCE_BYTE_INVENTORY.csv @ a3d44f554e4e4fa01223679035599019ae2de527`, blob `2a87ed920606be95003684e3775227ff8e94639c`, lines 13 and 15.

## 2. 1990 Austria sampling/design: what is actually proved

### Primary/current GESIS evidence

GESIS's current EVS 1990 wave page identifies the released source as **ZA4460 v3.0.0 (November 2011), DOI 10.4232/1.10790**, gives Austria fieldwork 1990-04-09 through 1990-06-01 with **n=1460**, and characterizes the wave as using representative multistage random samples **respectively quota samples** of adults 18+. That wording is wave-wide; it does **not identify which design Austria used**. Source: https://www.gesis.org/en/european-values-study/data-and-documentation/2nd-wave-1990 (retrieved 2026-10-08).

The official ZA4460 variable report proves a usable Austria calibration weight but not Austria's selection mechanics. It says `weight_g` adjusts national samples for **gender and age**; Austria is absent from the enumerated countries for which no weights are available. Source: https://access.gesis.org/dbk/50678, PDF p.24, extracted lines 763–770. Therefore:
- `1990_AT_WEIGHT_G_EXISTS = PRIMARY_DOC_PASS`.
- `1990_AT_WEIGHT_G_KIND = AGE_GENDER_CALIBRATION`.
- `1990_AT_PROBABILITY_INCLUSION_WEIGHT = NOT_PROVED`.
- A calibration weight must **not** be re-labelled an inverse-probability/design weight.

The same variable report documents administrative identifiers including national-study and version fields and warns that dataset code values can differ from questionnaire specifications because of standardization/harmonization (PDF pp.22, 27; extracted lines 639–658 and 859–883). This supports keeping source-native, integrated and trend layers distinct.

### Austria-specific corroboration, but not primary design closure

A later University of Vienna/AUSSDA Austria longitudinal product (`European Values Study 1990-2018 Austria Longitudinal Data`, DOI `10.11587/C4YBOT`) describes its universe as eligible Austrian citizens older than 18 with registered residence in a private household, its time method as repeated cross-section, and its overall sampling procedure as **mixed probability and non-probability**. Source: https://data.aussda.at/dataset.xhtml?persistentId=doi:10.11587/C4YBOT, metadata lines 285–290. Because this metadata describes the **combined 1990–2018 product**, its “mixed” label cannot be projected backward as proof that the 1990 wave itself contained a non-probability component.

A University of Vienna master's thesis independently reports Austria 1990 as PAPI face-to-face, **multi-stage random sampling**, target Austrian population 18+, n=1460, fielded by Fessel-GfK. Source: https://services.phaidra.univie.ac.at/api/object/o:1350433/download, p.41. This is useful corroboration but is a **secondary source**, not the missing country-specific primary sample certificate.

**1990 design disposition:**  
`PROVISIONAL_MULTISTAGE_RANDOM__SECONDARY_CORROBORATED__PRIMARY_COUNTRY_DESIGN_NOT_RECOVERED`.

Still missing before design-based national inference:
1. primary Austria-1990 frame definition and coverage exclusions;
2. exact stages/strata and PSU definition/count;
3. household and within-household/person selection rule;
4. inclusion probabilities or enough inputs to reconstruct them;
5. nonresponse handling and any design/nonresponse weight provenance;
6. exact analysis variables that carry PSU/stratum information, if any.

A wave-wide “random or quota” statement cannot choose between the two. Conversely, the secondary “multistage random” report cannot be promoted into primary design authority.

## 3. 2008 Austria design: primary country documentation is materially stronger

The official Austria national method report `ZA4754` defines the universe as persons 18+ resident in private households regardless of nationality, citizenship or language (PDF p.13, extracted lines 341–345). It documents a **multistage, stratified, clustered random-address design**: 463 region × political-district × community-size cells; election units as PSUs; Statistik Austria source frame; **375 sample points**; PAC address sampling; random target household; and last-birthday target-person selection (PDF p.18, lines 558–575). It also documents response/nonresponse accounting and 1,510 valid interviews (pp.18–19, lines 577–614).

Weighting is not unitary. The report states that EVS computed `weight` from gender×age categories and explicitly cautions its use; Austria is also among countries supplied with an **additional country-specific original weight** (PDF p.21, lines 629–656). The same report identifies the national dataset as **ZA4754 v1.1.0 (2010-11-30), DOI 10.4232/1.10152** (PDF p.22, lines 676–678). Source: https://access.gesis.org/dbk/17933.

**Consequence:** neither the EVS age×sex calibration weight nor the Austria-original weight may be selected automatically, and they must not be multiplied together absent source documentation saying to do so. The estimand must choose the weight whose construction matches the target population and analysis.

## 4. National study catalogue identity discrepancy

Observed facts:
1. HQ253's primary 1990 national questionnaire cover identifies **ZA4479**.
2. The official ZA4460 v3.0.0 variable report's national-study table prints **“Austria ZA4754”** (PDF p.11, extracted line 258).
3. The same ZA4460 report says that for 1981 and 1990 **only integrated datasets are provided**, whereas national datasets are additionally accessible for 1999/2008 (p.11, lines 277–279).
4. Current GESIS catalogue architecture lists 1990 as integrated **ZA4460**, while 2008 has integrated **ZA4800** plus national datasets **ZA4751–ZA4797**. Source: https://www.gesis.org/en/european-values-study/data-and-documentation.
5. Current GESIS 2008 documentation identifies Austria unambiguously as **ZA4754**, and the Austria national method report cites ZA4754 v1.1.0 / DOI 10.4232/1.10152.

**Inference, high confidence:** `ZA4754` in the old ZA4460 1990 national-study table is a metadata/table defect or contamination by the later Austria-2008 identifier. It cannot coherently denote both the 1990 Austrian field archive and the independently versioned 2008 national dataset.

**Do not overcorrect:** `ZA4479` is presently qualified as the archive-study identity printed on the 1990 Austrian field questionnaire. E01 does **not** prove that a separately distributable ZA4479 national data release/version corresponds byte-for-byte to SRC12. The authoritative 1990 integrated release remains ZA4460 v3.0.0.

## 5. Administration/protocol relation, without re-reading the item

From HQ253 only:
- substantive target clause and approve/disapprove direction match across 1990 and 2008;
- 1990 national field block was visibly framed as interviewer-read scenarios, with no independent show-card instruction visible in that block;
- the 1990 English integrated/master representation references Card Z;
- 2008 Austrian national fielding explicitly used Liste 53, read aloud, one response per row.

This is **not** a broad interview-mode change—both are face-to-face standardized survey administrations—but it is a real **stimulus/display/context difference**. A harmonized A048 variable does not prove that display differences are behaviorally null.

**Measurement disposition:**  
`SEMANTIC_TARGET_MATCH__ADMINISTRATION_EQUIVALENCE_UNPROVED__NOT_FATAL_BY_ITSELF`.

The pair is scientifically disqualified only if competent evidence shows that the differing display/order/instruction creates a construct-meaning or response-process break material to the requested estimand. In the absence of such evidence, the correct state is uncertainty/qualification debt, not “equivalent” and not “noncomparable.”

## 6. Exact unresolved edge and one lawful next action

**First unresolved documentary edge:** an authoritative Austria-1990 technical-method record that specifies the country sample type, population/frame, stages/PSUs/strata, household/person selection, nonresponse treatment and weight construction. The linked GESIS `EVS 1981-2008 Method Overview` exists but was served as XLSX and was not inspectable through this worker's browser content interface; no value from it is guessed.

**Owner:** GESIS/EVS archival methodology custodian, with AUSSDA/University of Vienna Austria-series custodian as an independent national-source witness; later statistical qualification belongs to a survey-method reviewer, not this documentary worker.

**Disconfirming test:** if the primary country method shows quota/non-probability selection, a frame materially different from the proposed common target, or unavailable/reconstructively invalid inclusion/cluster information, then probability-design inference and/or direct common-population comparison fails at that exact grain.

**One next lawful owner action:** obtain and bank the public, non-raw Austria-1990 country method row/report (including any weight-design notes) plus any public archive/version checksum or release manifest capable of connecting the retained SRC12/SRC14 bytes to official release identities; then send that fixed documentary packet to an independent survey-statistical/source-authority reviewer. Do **not** open the SAVs merely to compensate for missing documentary authority.

**STOP:** no pair grant, no temporal sign, no source operation, no consumer emission.

`HQ254_E01_RETURNED_FOR_HQ_REVIEW__NOT_ADOPTED`
