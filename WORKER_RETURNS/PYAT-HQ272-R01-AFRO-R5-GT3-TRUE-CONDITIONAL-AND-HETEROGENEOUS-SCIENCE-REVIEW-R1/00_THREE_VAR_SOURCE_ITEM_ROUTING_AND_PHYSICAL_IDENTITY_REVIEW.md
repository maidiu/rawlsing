# HQ272 R01 — Adversarial R5 Q86ABC source-item, routing, and physical-identity court

**Decision:** INDEPENDENT_SOURCE_ITEM_CANDIDATE_CONFIRMED__Q86C_EXACT_EXPOSURE_UNPROVED.
**Status:** Independent documentary/scientific hostile review, NOT source read/permission/adoption.
**Commission:** 063afdaf0934ae5aaa5f4e40f25f3689c24c219f; HQ272 frozen base e3a2e7c5ae77ae2f085339a84340007762588bd3; sealed HQ272 `HQ_HANDOFF/checkpoints/20261009-PYAT-HQ272-M01-F01-TRUE-TRIPLE-CANDIDATE-AND-FF02-SEMANTIC-HOLD-R1/CURRENT.md @ ff964c463fbe6674aa8112d4e00fbeb1f920751b`. Semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390`, unchanged.
**Actual model:** GPT-6; Sol High UI/intelligence tier not independently attestable. Browser/GitHub only; no local Mac, no source SAV read/decode, no row execution, statistics, CI tests, or custody rehash.

## Source original verified independently

**External original authority checked:** Afrobarometer *Data codebook for a Round 5 survey in 34 African countries*, July 2015, `https://afrobarometer.org/wp-content/uploads/migrated/files/data/round-5/merged_r5_codebook.pdf`. Original PDF **pageno 52 / printed p. 53 visually inspected** in independent browser screenshot; Q86A/B/C share the actual citizenship-rights stem (citizenship understood as passport and national-election vote rights at age >=18). Items:

| Variable | Actual intended respondent opinion | Native states and source wording |
|--|--|--|
| Q86A | citizenship of person born in country with one national and one non-national parent | 0 No; 1 Yes; 9 Don't know; 997 Not asked; 998 Refused to answer; -1 Missing |
| Q86B | citizenship of person born in country with two non-national parents | same code-state names |
| Q86C | citizenship of foreign-born wife of a national man | same code-state names |

All **three** entries individually state not asked in **ALG, EGY, MRC, SUD, TUN**. The printed `Values` shorthand for each reads `0,1,9,998,-1` but the adjacent *Value Labels* explicitly include `997=Not asked`; treat this source-internal discrepancy as a required reconciliation, not permission to drop 997. Q86C asks about a **woman's marital tie to a male national**; it is not an undifferentiated migration attitude or an observed legal citizenship rule. The adjacent Q86D is the distinct reverse-gender husband case; no symmetry may be presumed. Original source conveys common block administration, not exact unique 19,210 Q86C exposure facts. World Bank merged R5 source dictionary separately lists Q86A/B/C plus Q8A and Q97 under the same released merged dataset (catalogue `AFR_2011_AFB-MR5_v01_M`: https://microdata.worldbank.org/catalog/2924/data-dictionary/F1), but this online index is not an original respondent-level exposure certificate.

**Alternative items from same original July 2015 codebook, independent PDF-index checks:** pageno 11 printed p.12 Q8A asks if respondent or family went without enough food to eat during past year; its named response states 0 Never; 1 Just once or twice; 2 Several times; 3 Many times; 4 Always; 9 DK; 998 Refused; -1 Missing. No 997 on this item. Pageno 60 printed p.61 Q97 asks highest completed education, 0–9 graded education, 99 DK, 998 Refused, -1 Missing. Neither is the same construct as Q86A. Q8A/Q97 page screenshots were not retrievable in this browser session; their content is indexed by the authoritative original PDF and secondarily by M01. Distinguish index-backed from visually confirmed evidence.

## Independent hostile check on M01 original and physical claims

M01's four-source returns read fully at `e115b81a0833a8f8983fe0ece62ef66b31654ff5`, including physical-dictionary `01_FILE_SHA_DICTIONARY_AND_NATIONAL_SAMPLE_METADATA.json`; HQ272 intake read. M01 *reports* actual local physical SHA-256 checks at a different Mac: R5 `Afro Barometer Round 5.sav` SHA `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`, 51,587 rows/348 columns; R9 SHA `3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8`; governed merged-R5 codebook SHA `7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`. R01 **did not independently rehash physical bytes**. Public July-2015 PDF URL is independently inspected, but byte-identity with M01's locally retained PDF is *not* freshly verified by R01.

Original merged R5 physical M01 metadata gives Q86A/B/C and `RESPNO` present, with matching code-state numeric labels; 998 physical label **`Refused`** versus codebook/frozen authority **`Refused to answer`**. This is an exact label-to-state translation obligation, not authority to rewrite the original carrier. Frozen semantic COUNTRY_ALPHA3 coordinate is **derived**; physical R5 SAV contains COUNTRY and COUNTRY_ALPHA, not a literal COUNTRY_ALPHA3 variable. Reconcile derived country crosswalk, exact source-native country codes, original (COUNTRY, RESPNO) respondent identity, and scope per country; do not assert native alpha-3 direct column provenance.

Current C11 `rawlsing_next/wave1_r5_q86_c11_projection.py` blob `d96933180d310b4078f23127bb5a97a3677728d1`: 
- `R5Q86GovernedRow` at 206–236 carries **only** Q86A and Q86B raw/response/exposure slots; `R5Q86ProjectionPackage` at 275–289 returns **only** those Q86 question/domain/replay references.
- `_validate_rows` at 383–394 proves independent `EXPOSED__PROVED` **Q86A and Q86B**, not Q86C.
- `_authorities` at 332–366 scopes routing, native semantics, carrier reexpression, replay and exact target-use permissions to **Q86A/Q86B**.
- `_build` at 437–529 creates two `QuestionVariableBinding`, two response slots and two `RoutingEligibilityFact` per respondent; its frozen country list is BFO, BOT, CVE, KEN, LES, MAU, MLW, MOZ, NAM, SAF, UGA. R5 Q86C has **NO projected RespondentEvent or RoutingEligibilityFact** in this owner.
- current producer `wave1_gt12_i03_positive_facts.py` frozen `R5Q86I03ExecutionBinding` at 138–151 has **only q86a/q86b**; `_validate_release_member_scope_linear` at 342–466 independently validates only those two.

**Decisive negative:** identical printed country-level exclusions do not prove per-respondent Q86C eligibility, exposure, answered/not-asked mapping, or equivalence with all **19,210** Q86A/B eligible members. The 19,210 scope is `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`, member hash `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`, frozen for **Q86A/B**. It is a *candidate* Q86C scope only, not a proved Q86ABC common exposure set. Q86C requires own exact qimpl, original domain and target replay identities, per-item routing/exposure producer, authenticated member-set parity or new hash, and country-native reconciliations.

**Absence classifications:** Q86C original field meaning = DOCUMENTED; Q86C physical dictionary = M01 DOCUMENTED/NOT R01 REHASHED; exact same source respondent *capacity* = PLAUSIBLE; Q86C actor-independent 19,210 respondent-level exposure = UNPROVED; Q86C C11 `RespondentEvent` / `RoutingEligibilityFact` = NOT PRODUCED; Q86C GT3 target-use = UNISSUED; any temporal, weighted, actor or causal claim = NOT AUTHORIZED.

Sources: M01 `00`–`03` four returns @ e115b81a; original codebook URL above, printed p.53 screenshot; `rawlsing_next/wave1_r5_q86_c11_projection.py` @ semantic PRE-MAIN `1f47063...`; HQ272 sealed CURRENT and decision. No source rows were used.
