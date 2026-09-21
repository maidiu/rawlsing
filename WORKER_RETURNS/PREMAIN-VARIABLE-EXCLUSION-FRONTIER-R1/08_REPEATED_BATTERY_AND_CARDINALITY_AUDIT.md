# PREMAIN VARIABLE EXCLUSION FRONTIER R1 — REPEATED BATTERY / CARDINALITY AUDIT

Status: **PASS — family × physical-instance court completed; no cardinality exclusion promoted without proof**

## Governing distinction

`SEMANTIC FAMILY RELEVANT != EVERY PHYSICAL INSTANCE REQUIRED`.

This audit therefore tested repeated source expansions at their actual candidate consumption grain. It did **not** preserve repeated columns merely because their question family is interesting. It also did **not** prune repeated columns merely because they are wide.

The controlling PRE-V3/V3 seam is the clean-room world/context resolution architecture at `127dd9c921f376fde8f34d238b2cb1ff16f9d48c`, not the quarantined OBL063 fixed 22-driver / 22×9 driver→type architecture. Long Memory additionally preserves household/relationship history, age-indexed relational graphs, and path-bearing whole-history information. Those current requirements make member/job/year identity a live consumption grain.

## Largest width multipliers

| source | family | physical instances | semantic content | required grain | does index identity matter? | R1 disposition |
|---|---|---:|---|---|---|---|
| LiTS | LITS_HH_ROSTER_CORE | 132 | household/family roster: member identity, sex, relation-to-head, DOB/age views | member-level + relationship graph | member identity/order YES; physical-layout redundancy unresolved | KEEP; 0 proved exclusions |
| LiTS | LITS_HH_ROSTER_DOB_DUAL_LAYOUT | 72 | two 36-column physical layouts for 12 members × day/month/year | member-level age-indexed relationship history | member identity YES; layout identity not proven necessary, but no supersession/equality authority | UNRESOLVED FOR DEDUP; 0 proved exclusions |
| LiTS | LITS_HH_ROSTER_AGE_DIRECT_DERIVED_PAIR | 24 | q105 member age plus derived age1..age12 | member-level age-indexed relationship history | member identity YES; direct-vs-derived audit/reconstruction role not retired | KEEP; 0 proved exclusions |
| LiTS | LITS_CURRENT_JOB_MONTH_TRAJECTORY | 60 | jobs A-E repeated across 12 monthly positions | job × time trajectory | job and month identity YES | KEEP; 0 proved exclusions |
| LiTS | LITS_CURRENT_JOB_A_E_ATTRIBUTES | 65 | occupation/industry/status/ownership/contract/size/supervision/employees across jobs A-E | job-level position/trajectory | job identity YES; q414 main-job selector does not erase secondary-job history | KEEP; 0 proved exclusions |
| LiTS | LITS_ANNUAL_LIFE_EVENT_HISTORY_Q601 | 114 | six event families across 1989-2006 plus NA slots | time-indexed life history | year identity YES | KEEP; 0 proved exclusions |
| LiTS | LITS_JOB_BY_YEAR_LIFE_HISTORY_Q602 | 252 | jobs A-N × 1989-2006 wage-work history | job × time trajectory | job and year identity YES under whole-history envelope | KEEP; 0 proved exclusions |
| LiTS | LITS_LIFE_HISTORY_JOB_A_N_ATTRIBUTES | 112 | five attribute families across jobs A-N, ownership expanded to four components | job-level trajectory | ordered job identity YES/plausible | KEEP; 0 proved exclusions |
| LiTS | LITS_LIFE_HISTORY_JOB_A_N_EXIT | 14 | job-leaving type across jobs A-N | job-level trajectory | ordered job identity YES/plausible | KEEP; 0 proved exclusions |
| LiTS | LITS_ANNUAL_SELF_EMPLOYMENT_HISTORY_Q604 | 18 | self-employment by year 1989-2006 | time-indexed trajectory | year identity YES | KEEP; 0 proved exclusions |
| LiTS | LITS_ANNUAL_COPING_TRANSITION_HISTORY_Q605 | 209 | 11 coping/transition families × 18 years plus NA slots where present | time-indexed deprivation/trajectory history | year identity YES | KEEP; 0 proved exclusions |
| WVS7 | WVS7_ORGANIZATION_MEMBERSHIP_RAW_RECODE_PAIRS | 24 | Q94-Q105 source items paired with R recodes | respondent × organization type | organization target identity YES; raw/recode supersession not proved | KEEP; 0 proved exclusions |
| WVS7 | WVS7_PARALLEL_COUNTRY_ENCODINGS | 5 | ISO numeric/alpha, CoW alpha/numeric, country-year | context/geography/provenance | coding-system identity may matter for join/replay | KEEP; 0 proved exclusions |
| WVS7 | WVS7_PARALLEL_GEOGRAPHY_ENCODINGS | 11 | town size, settlement type, urban/rural, region encodings, town, coordinates | geography/context at multiple grains | not duplicate: grains differ | KEEP; 0 proved exclusions |

## What the physical-instance court actually found

### 1. LiTS household roster: semantically relevant, member identity remains live

The accepted 1,198-slot bridge explicitly preserves member-specific topology for members 1–12. Long Memory says a generated person should arise through household/relationship history and that age-indexed caregiver/peer/institution relations are part of the explanatory substrate. Therefore the 12-member expansion cannot be collapsed to household size or a generic family flag under the current envelope.

This blocks `REPEATED_TEMPLATE_CARDINALITY_EXCESS` for q101/q102/q103/q105 and derived age slots **today**.

### 2. LiTS q104 DOB dual-layout surface: strongest dedup candidate, but not yet proved

There are 72 q104 DOB physical variables: 36 component-prefix slots (`q104_d1`, `q104_m1`, `q104_y1`, …) and 36 member-prefix slots (`q104_1d`, `q104_1m`, `q104_1y`, …). The accepted LiTS ledger binds both layouts to the same member topology and questionnaire authority.

That is strong evidence of a duplicate-looking physical surface, but the current documentary estate does **not** provide a competent supersession/equality law proving that one layout can be removed while preserving transformation provenance, discrepancy detection, replay and audit. Raw value equality was forbidden and was not inspected.

Disposition: `UNRESOLVED__DO_NOT_PRUNE` at the duplicate-view question, while the individual variables remain in the conservative KEEP envelope.

A future source-authority court could potentially unlock up to **36 columns** here if it proves one layout is a deterministic/superseded view of the other and preserves all audit/replay obligations.

### 3. LiTS direct q105 age vs derived age1..age12

The ledger distinguishes q105 member-age slots from `age1..age12` as derived roster context. That does not automatically make the derived view disposable: current information-conservation law preserves derivation/provenance and exact downstream meaning, and no competent authority retires either view.

Disposition: no `SUPERSEDED_DERIVED_OR_ADMIN_VIEW` proof yet.

### 4. LiTS job and year expansions are not mere maximum-cardinality padding under current law

The 252 q602 job×year cells, 112 A-N job-attribute cells, 209 q605 annual coping/transition cells, 114 q601 annual event cells, and current-job A-E expansions are physically expensive. But Long Memory explicitly rejects final-state substitution for the path that generated a person, and Field Forge preserves origin/trajectory indicators, employment/occupation position and migration/mobility.

Distinct job and year identity is therefore plausibly consumable. No bounded subset (for example jobs A-E only, or latest year only) is currently authorized as lossless.

### 5. WVS7 paired recodes and parallel geographic encodings

WVS7 contains source-item/R-recode membership pairs and multiple country/region representations. These may later admit deterministic projection or canonical-substitution pruning, but current provenance, portability, exact-join and geography-grain functions prevent a class-A ruling without a specific reconstruction/supersession authority.

## Cardinality verdict

- Proven `REPEATED_TEMPLATE_CARDINALITY_EXCESS`: **0**
- Proven `DUPLICATE_PHYSICAL_INSTANCE`: **0**
- Proven `SOURCE_PLACEHOLDER_OUTSIDE_REQUIRED_GRAIN`: **0**
- Proven `SUPERSEDED_DERIVED_OR_ADMIN_VIEW`: **0**
- Proven `SEMANTICALLY_OUTSIDE_ENVELOPE`: **0**

This is not a claim that no such columns exist. It is the narrower claim required by the commission: **none is affirmatively proved disposable under the current foreseeable envelope with the evidence presently frozen**.

## Highest-value successor proof courts

1. q104 dual-layout equivalence/supersession court.
2. q105 vs derived-age lineage/reconstruction court.
3. LiTS job-slot maximum-cardinality semantics: whether A-N are true ordered trajectory records or source placeholders beyond an instrument-defined maximum actually used by Rawlsing.
4. WVS source-item/R-recode deterministic reconstruction and provenance-retention court.
5. Administrative presentation aliases (country names/codes, derived display fields) only after exact replay/audit substitution law is frozen.

Terminal: `REPEATED_BATTERY_CARDINALITY_AUDIT_COMPLETE__NO_UNPROVED_PRUNE`
