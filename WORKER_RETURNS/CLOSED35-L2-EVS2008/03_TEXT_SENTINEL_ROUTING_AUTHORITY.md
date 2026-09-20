# CLOSED35-L2-EVS2008 — Text / Sentinel / Routing Authority

## Scope and negative law

This return is documentary-only. It did **not** open `EVS 2008.sav`, execute a decoder, or run measured P2X. Exact physical claims are inherited from the accepted S35 / Authority71 estate for canonical source:

- file: `EVS 2008.sav`
- SHA-256: `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`
- accepted execution mechanism: `SAV_LATIN1_COMPAT_PHYSICAL_ONLY__SOURCE_DECLARES_UTF8`

The following distinction is binding:

```
latin1 compatibility decode
    = physical metadata/data extraction mechanism
    != intended source-text encoding
    != producer-authoritative label text
    != permission to repair malformed SAV strings
```

No malformed SAV label is promoted to semantics merely because a compatibility reader can render it.

## Producer documentary target

GESIS currently identifies the EVS fourth-wave Scientific Use File as **ZA4800 v5.0.0, released 2022-06-08, DOI 10.4232/1.13841**. Its current Variable Report documents **66,280 cases and 477 variables**, the same accepted source geometry recorded by the Rawlsing physical estate. GESIS also publishes the Master Questionnaire, method/technical reports, national questionnaires, bilingual variable documentation, translation-comparison material, version history, errata and patches.

Authority order for this worker is therefore:

1. accepted Rawlsing exact-source physical facts for byte identity / native topology;
2. current GESIS ZA4800 v5 Variable Report for integrated variable semantics, recodes, flags and country notes;
3. EVS 2008 Master Questionnaire for original English question wording, response design and routing;
4. method / national / translation documentation for country-specific implementation;
5. malformed compatibility-decoded SAV labels only as quarantined physical artifacts, never semantic authority.

A public GESIS SHA-256 for the downloadable SAV was not located. Therefore the current-release alignment is strong documentary alignment (study number, current release, 66,280 x 477 geometry, exact variable identities and question structure), not a producer-published cryptographic binding to Rawlsing's frozen SHA.

## Producer-authoritative text alignment rule

The old blocker asked for either a byte-by-byte text repair or a governed rule that leaves malformed strings non-semantic while sourcing semantics elsewhere. This worker establishes the latter.

For every field asserted semantically:

1. preserve the exact native variable/set identity from accepted physical evidence;
2. join to producer documentation by stable variable identity and question identity;
3. source human-readable question/label text from ZA4800 v5 Variable Report;
4. use the Master Questionnaire only where original wording/instruction/routing is required;
5. retain the malformed SAV text as an opaque/quarantined physical string;
6. if no producer document aligns a string by stable identity, emit `UNKNOWN_PRODUCER_TEXT`; do not reconstruct it from latin1 output.

This closes the **MR-label semantic** problem without pretending to repair the malformed metadata bytes themselves.

Official documentary anchors:

- EVS 2008 wave page: https://www.gesis.org/en/european-values-study/data-and-documentation/4th-wave-2008
- ZA4800 v5 Variable Report: https://access.gesis.org/dbk/17681
- searchable ZA4800 v5 variable catalogue: https://access.gesis.org/dbk/59828
- Master Questionnaire: https://access.gesis.org/dbk/17683
- data-access/documentation service: https://www.gesis.org/en/european-values-study/data-and-documentation/notes-on-data-access

## Native MR sets: semantic closure

All 13 native sets remain native MR sets. None may be flattened into a bag of unrelated variables merely because the integrated variables are dichotomized.

### Q5a family — `q5a`, `evs_q5a`, `vv25`

Producer question Q5a asks which voluntary organisations/activities the respondent belongs to and instructs interviewers to code all mentioned.

- `q5a` and `evs_q5a` are exact physical membership aliases: `v10..v25`.
- `vv25` is the overlapping body-only set `v10..v24`.
- `v25` is the explicit **None (spontaneous)** category.
- ZA4800 IDS recodes MR variables to `1=mentioned`, `0=not mentioned`; missing classes are `-5 other missing`, `-4 question not asked`, `-3 not applicable`, `-2 no answer`, `-1 don't know`.
- No response order is a rank.
- Producer `f25` logic explicitly contrasts any selection among `v10..v24` with `v25=None`. That provides documentary authority for the distinct structural role of `vv25`: substantive selection body excluding the None coordinate.
- Denmark has documented DK/NA handling; Sweden postal-mode data required not-mentioned recoding; Turkish source system-missings were integrated as `-5`.

The duplicate set names remain separate physical identities but have no producer evidence of distinct substantive meaning. They must not create duplicate analytic counts.

### Q5b family — `q5b`, `evs_q5b`, `vv43`

Producer Q5b asks which listed organisations the respondent currently does unpaid voluntary work for, again code-all-mentioned.

- `q5b` and `evs_q5b`: `v28..v43`.
- `vv43`: `v28..v42`.
- `v43`: explicit **None (spontaneous)**.
- `vv43` is the substantive-body-only overlap, supported by the producer's `f43` consistency relation between `v28..v42` and `v43=None`.
- Denmark did not implement Q5b and is `-4`; Sweden's postal questionnaire omitted the None category; Turkey's source system missings were recoded `-5`.
- Producer documentation warns that double negation may cause problems in `v43`; that warning is preserved, not “corrected” locally.

No rank semantics are authorized.

### Q6 — `evs_q6`

`v46..v60` are the listed groups the respondent would not like as neighbours.

- Multiple response, non-ranked.
- IDS semantics: `1=mentioned`, `0=not mentioned`, standard `-5..-1` missing classes.
- Austria, Belarus, Denmark, France, Italy, Norway and Slovenia did not implement the question; current report codes these as `-4 question not asked`.
- Finland's extra “no such groups” response was used to recode the battery to `0`; a “can't say” auxiliary was used to recode to `-1`.
- GESIS warns that countries differed in whether the battery was asked item-by-item or as a block and points to the current errata. That is a country-method caveat, not license to harmonize the answers by invention.

### Q14 family — `q14`, `evs_q14`

`v69..v86` represent job aspects personally considered important; the Master Questionnaire says code all mentioned.

- exact duplicate native aliases;
- non-ranked multiple response;
- `v86` is **None of these (spontaneous)**;
- `f86` is the producer consistency flag contrasting `v69..v85` against `v86`;
- current v5 documentation gives item/country-specific translation and implementation notes, which must remain local to the named variables/countries.

No duplicate semantic question is created by the two physical set names.

### Q52 family — `q52`, `evs_q52`

`v170..v181` represent qualities children should learn at home.

- respondent may select **up to five**;
- this is a selection cap, **not a ranking**;
- `v181` is **None (spontaneous)**;
- `f180` flags respondents who selected more than five among substantive qualities `v170..v180`;
- q52 and evs_q52 are exact physical aliases and must both be preserved without analytic double-counting.

### Q107 — `evs_q107`

Native members are:

`v323, v324a, v325a, v326a, v327a, v328a`.

They are yes/no presence indicators for partner/spouse, children, parents, grandparents, other relatives and other non-relatives in the household.

The Master Questionnaire separately records counts in `v324b..v328b`. Those **b variables have a different role and are not members of the native MR set**. The MR set therefore carries category-presence semantics, not household counts or ranks.

Routing:

- Q105 is asked to all;
- if Q105 reports zero children, Q106 is skipped and the questionnaire proceeds to Q107;
- Q107 itself is not filtered out by that route.
- Finland's field questionnaire had a “none of the above mentioned” auxiliary; the integrated a-variables were recoded to `0=no` accordingly.

### Q108 — `evs_q108`

Native members are:

`v329a, v330a, v331a, v332a, v333a, v334a`.

They are yes/no indicators of whether the respondent ever experienced six listed family events. Corresponding `b` variables record age at first experience and are **not** MR members.

- non-ranked;
- IDS a-variable semantics: `1=yes`, `0=no`, with standard `-5..-1` missing classes;
- Master Questionnaire b-side special values (`97 NAP`, `98 DK`, `99 NA`) are not MR-set sentinels and must not be generalized onto the a-variables;
- Finland's “none of the above” auxiliary maps the a-battery to `0`; its “can't say” auxiliary maps to `-1`.

## Flag authority

### `f201`: prior contradiction closed

The accepted physical estate exposed a misleading compatibility-rendered heading referring to respondent aims / Q55-Q56 while the neighboring variables are `v201/v202`.

Current producer documentation resolves the relation directly:

- `f201` indicates inconsistency for **`v201/v202`**;
- if `v201 = v202`, `f201=1`;
- `0=consistent`, `1=inconsistent`.

The semantic relation is therefore **v201/v202**. The stray heading/question-reference text must not override the producer's explicit rule. This is exactly the kind of case for which compatibility-rendered SAV text is quarantined.

### Other MR-related flags

- `f25`: Q5a substantive selections versus v25=None consistency.
- `f43`: Q5b substantive selections versus v43=None consistency.
- `f86`: Q14 substantive selections versus v86=None consistency.
- `f180`: Q52 five-selection limit for v170..v180.

These are flag variables around MR batteries, not extra MR members.

## Date sentinel authority: `v372`

Producer documentation establishes:

- `v372` = **date of interview**, Q137, day/month/year.
- Great Britain: invalid dates before/after the official survey period were converted to **system missing**.
- Netherlands: the question was not implemented in the field questionnaire; data are present as supplied by the country.
- Sweden: date data are unavailable because of postal mode.

Accepted Rawlsing physical evidence separately establishes that this frozen SAV declares a **typed date user-missing value rendered as `1582-10-13`**, affecting 1,917 records.

**What remains unknown:** no producer document located by this worker assigns a semantic reason/code meaning to that exact user-missing date sentinel. The Master Questionnaire gives no missing code for Q137, and the current v5 Variable Report documents the country exceptions above without naming `1582-10-13` or an equivalent producer code.

Therefore the only lawful rule is:

```
v372 == physical user-missing sentinel 1582-10-13
    => USER_MISSING__SEMANTIC_REASON_UNKNOWN
```

It is forbidden to infer that this means “don't know”, “no answer”, “not applicable”, “question not asked”, “other missing”, or any other standard EVS missing class merely from numeric/date formatting. It is also forbidden to generalize this date sentinel to any variable other than `v372`.

This unresolved semantic reason is sufficient to prevent the requested full PASS terminal.

## Country/filter/routing authority

Country applicability belongs to the exact question/variable documentation; it is not a global mask.

Binding examples recovered here:

- Q5b: Denmark not asked (`-4`); Sweden lacks the None item; Turkey had source system-missing recoded `-5`.
- Q6: AT/BY/DK/FR/IT/NO/SI not asked (`-4`); Finland has explicit auxiliary-driven recodes.
- Q14: country/item-specific translation exceptions must stay on the affected item/country; they do not invalidate the entire battery.
- Q107/Q108: Finland has documented auxiliary-category recodes.
- v372: Great Britain, Netherlands and Sweden have different producer-documented reasons/states and must remain distinct.

At source-specific realization, routing/applicability must be carried at variable × country/question scope; no single “EVS missing” or “EVS not asked” sentinel is authorized.

## Producer corrections / revised exports

The current producer estate establishes several corrections or release-level changes relevant to admission:

1. **ZA4800 v5.0.0 (2022-06-08)** is the current Scientific Use File.
2. ZA4800 and restricted ZA4799 now implement refined anonymization/access separation; the difference is concentrated in residence/occupation detail rather than the MR variables adjudicated here.
3. The current release explicitly excludes the Azerbaijan 2008 survey from the integrated file because of producer data-quality concerns.
4. National EVS 2008 datasets are documented as older replication/country-specific surfaces; the integrated current dataset is the producer target for current cross-country semantics.
5. Current variable documentation/errata, not stale malformed SAV label text, controls semantic corrections such as the `f201` relation and country-specific recodes.

These documentary corrections authorize interpretation of the current integrated semantics. They do **not** authorize rewriting Rawlsing's frozen source bytes before a source-specific realization layer explicitly maps the accepted physical source to the documentary semantics.

## Closure state

Closed:

- current producer release target and documentation estate;
- official Master Questionnaire;
- current v5 variable/data dictionary authority;
- semantics, ordering law, missing classes, routing/applicability and overlap roles for all 13 native MR sets;
- exact duplicate alias treatment;
- `vv25` / `vv43` body-only overlap roles;
- `f201` semantic relation;
- malformed-text quarantine + producer-text alignment rule;
- current producer correction/revised-export context.

Still open:

1. producer-published cryptographic hash binding Rawlsing's exact SAV SHA to ZA4800 v5.0.0 was not located (documentary alignment is strong but non-cryptographic);
2. producer semantic meaning of the exact `v372` user-missing sentinel rendered `1582-10-13`.

Terminal:

`CLOSED35_L2_EVS2008_DOCUMENTARY_AUTHORITY_PARTIAL__EXACT_TEXT_MR_OR_SENTINEL_UNKNOWN_SET_RETURNED`
