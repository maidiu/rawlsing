# D2C — native measurement, denominator, publication-as-of and cross-source court

**Evidence grade: OFFICIAL_PUBLISHER_WEB_PDF_TABLE_AND_DEFINITIONS_VERIFIED; original PDF bytes and revision chain NOT in custody.** This is a documentary source evaluation, not an issued N5/N6 source product or an empirical two-source join.

## Source packet GSS — 2021 PHC Volume 3K, Table 5.10

Official original publisher [GSS Volume 3K: Housing Characteristics PDF](https://census2021.statsghana.gov.gh/gssmain/fileUpload/reportthemesub/Volume%203K_Housing%20Characteristics_240222.pdf). Cover image inspected on PDF zero page 0: **Ghana 2021 Population and Housing Census, General Report Volume 3K, Housing Characteristics, February 2022**. Official GSS [news release](https://census2021.statsghana.gov.gh/newspage.php?GSS-completes-release-of-2021-PHC-General-Reports=&readmorenews=MjM0ODgzNjQxMy41MDg1), posted **26 February 2022**, explicitly says GSS released Volume 3K with the last five general volumes on **24 February 2022**. Census reference night is 27 June 2021; the data collection and release clocks are not interchangeable.

Read directly from **Table 5.10, printed page 62 / zero-based PDF page 75**, independently visually inspected and cross-checked with official extracted table:

| Native rural occupied-dwelling lighting category | Original count | Published % |
|---|---:|---:|
| Total rural occupied dwelling units, the denominator | **3,288,063** | 100.0 |
| Electricity (all five electric categories) | **2,388,192** | **72.6** |
| Electricity (mains) | 2,288,193 | 69.6 |
| Electricity (community-based Grid) | 74,490 | 2.3 |
| Electricity (private generator) | 3,640 | 0.1 |
| Electricity (solar panel/invertor) | 21,512 | 0.7 |
| Electricity (wind energy) | 357 | 0.0 |
| Solar lamp (separate NON-electricity category in table) | 123,903 | 3.8 |

**Independent integrity computation:** 2,288,193 + 74,490 + 3,640 + 21,512 + 357 = **2,388,192** exactly; 2,388,192 / 3,288,063 = **72.6321849673%**, one decimal **72.6%**. Mains only = **69.5909%**, rounded 69.6%; it is not the claimed all-electric numerator. A free-standing `Solar lamp` is listed as separate from `Electricity (solar panel/invertor)` and cannot be included by similarity of name alone.

**Denominator law:** Volume 3K §3.5 defines a dwelling unit as one or more rooms within a housing unit occupied by a household; §3.6 distinguishes occupied, secondary housing and vacant dwellings. The note **at the end of Table 5.10** explicitly excludes **secondary housing and vacant dwelling units**; the report §2 states it is based on responses from households and excludes homeless households. These are native **rural occupied dwelling units**, not people, not all rural houses, not vacant structures, not individual electric connection accounts. The table records **main source of lighting**; it does not measure hours of service, stability of supply, ownership of appliances, indoor electrification quality or a particular future person's use. `Lighting` in §3.15 includes main and secondary source concepts, but Table 5.10 is restricted to *main*.

**Design/uncertainty:** a population and housing **census** aggregate from household enumeration, not a probability sample whose sampling margin may be fabricated. Classification and enumeration non-sampling error, age of observations within 2021 field operations, and corrected source editions are **not quantified for this precise cell** in the inspected table. Do not create spurious confidence intervals or retroactive prepublication knowledge.

## Source packet NCA — Volume 6 Issue 4, Q4 2021, Table 10

Official [NCA 2021 Q4 statistical bulletin PDF](https://nca.org.gh/wp-content/uploads/2022/07/Q4-2021-statistical-Bulletin.pdf), PDF cover and title pages zero 0–1: **Quarterly Statistical Bulletin on Communications in Ghana, Volume 6 Issue 4, Fourth Quarter October–December 2021**. Direct official [NCA July 8, 2022 bulletin announcement](https://nca.org.gh/2022/07/08/quarterly-statistical-bulletin-on-communications-2022-q4/) explicitly calls the issue **2021 Q4** and links to this exact 2021 Q4 PDF. Its path's **2022-q4** slug is a *web slug ambiguity*, NOT evidence for a Q4 2022 issue.

Read from **Table 10, printed page 17 / zero-based PDF page 29**, official parsed PDF text:

| Native category | Ghana Q4 2021 subscriptions |
|---|---:|
| Mobile data **prepaid subscriptions** | 23,237,338 |
| Mobile data **postpaid subscriptions** | 177,189 |
| Total mobile data subscriptions | **23,414,527** |

The sum 23,237,338 + 177,189 = **23,414,527** exactly. PDF printed-page **x**, PDF zero page **10**, defines Mobile Data in terms of active subscriptions to GPRS, EDGE, HSPA, UMTS, EV-DO, 3G and LTE **that generated internet traffic (upload and/or download) within the preceding ninety (90) days**. NCA introduction states source is licensees' monthly and quarterly reports and some in-house regulatory collection; this is **administrative subscription accounting**, not a census of unique individuals. Native unit is an **active mobile data subscription**, and the table's geographic scope is national Ghana. A person can have several subscriptions, a shared subscription can serve multiple people, and a subscription cannot establish human access at household, rural, or person grain. No Ghana-rural/subnational breakout or de-duplicated person denominator is issued in Table 10.

**Time law:** reporting/reference Q4 October–December **2021** and active-within-90-days test; official publication notice **8 July 2022**. The 90-day activity window is a validity rule on a subscription count, NOT 90 days of continuous service, stable ownership, use by one person, daily activity, or rural household internet penetration. Licensee report revisions, backfills, errors and coverage uncertainty are not specified for this count in the inspected table; no sampling CI is licensed.

**Method/version quality note:** the NCA PDF table of contents contains stale quarter language for certain broadcasting entries (references to Q3 2021). That editorial irregularity deserves original-publisher revision verification but **does not override** the explicit cover/issue identity or Q4 2021 column in Table 10. NCA screenshot of PDF p29 failed web cache miss, although the official PDF HTML reader returns the exact Table 10 rows. Do not misreport a successful visual NCA check.

## Explicit scientific contrast and historical-as-of gate

| Dimension | GSS | NCA |
|---|---|---|
| Statistical object | Rural **occupied dwelling-unit main lighting** | National active **mobile-data subscriptions** |
| Collection / design | 2021 national population/housing census | Telecom service licensees' administrative aggregates |
| Native geography | Ghana **rural** | Ghana **national** |
| Units | Dwelling units counted once in their main-lighting category | Subscription accounts/records, may be multiple per human |
| Observation/reference | Census 2021, reference night June 27 | 2021 Q4; trailing 90-day active rule |
| First supported public availability | **2022-02-24** | **2022-07-08** |
| Original immutable PDF file SHA | **NULL — binary unobtained** | **NULL — binary unobtained** |
| Field product | N5/N6 **UNISSUED** | N5/N6 **UNISSUED** |

- Historical query on **2021-12-31**: neither *published report/table* can be presented as contemporary-known material, even though the historical events/conditions existed. Distinguish present-day historical reconstruction with later evidence from knowledge available to 2021 actors.
- **2022-02-24 through 2022-07-07**: GSS source is officially released; NCA's present bulletin remains **NOT_YET_PUBLISHED**. An all-two-sources demand must be held or explicitly partial/nonpositive.
- **2022-07-08 onward**: minimum *documentary publication-available* two-source date, conditional on independently certified editions/rights and source-specific revisions for production. Neither source becomes a real N9 WORLD serving object merely through page visibility.
- Joining 2,388,192/3,288,063 to 23,414,527 creates neither a common statistical universe nor a legitimate probability, correlation, connectedness rate, rural smartphone rate or two-dimensional empirical respondent cell. At most, with separate N7/EE13 authority, the two facts can coexist as **NONPOOLED_CONTEXTUAL_CO_PRESENCE_ONLY**, each retaining its native publisher, unit, geography, observation and knowledge clocks.

**Generated-person relevance:** one field represents documented 2021 rural material lighting conditions, while the other describes a contemporary *national subscription market*. They can constrain objective historical possibility only in their correct scope. Neither establishes that a generated Ghanaian mother, father, rural learner, child or nonparent held a SIM, had light, accessed networks, learned something from either institution, or experienced any emotional/psychological consequence.

See the two separate UNISSUED candidate documentary packets `05_GSS_DOCUMENTARY_PACKET.json` and `06_NCA_DOCUMENTARY_PACKET.json`. Their source-root SHA-256 and current/original edition comparison deliberately remain NULL.
