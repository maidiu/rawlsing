# CLOSED35-L2-EVS2008 — Return

## Result

**PARTIAL.**

Terminal:

`CLOSED35_L2_EVS2008_DOCUMENTARY_AUTHORITY_PARTIAL__EXACT_TEXT_MR_OR_SENTINEL_UNKNOWN_SET_RETURNED`

This worker closed the EVS 2008 multiple-response and malformed-text documentary semantics far enough to make the remaining defect exact rather than diffuse. It did **not** open raw SAV bytes, execute source decoding, or run measured P2X.

Canonical physical source remains:

- `EVS 2008.sav`
- SHA-256 `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`
- compatibility mode `SAV_LATIN1_COMPAT_PHYSICAL_ONLY__SOURCE_DECLARES_UTF8`

Compatibility text remains non-semantic.

## Producer release/documentation recovered

Current GESIS authority identifies the EVS 2008 Scientific Use File as:

- GESIS study **ZA4800**
- version **5.0.0**
- release **2022-06-08**
- DOI **10.4232/1.13841**
- **66,280 cases / 477 variables**

Official documentary surfaces recovered and used:

- current EVS 2008 wave/release page;
- current ZA4800 v5 Variable Report / searchable variable catalogue;
- EVS 2008 final Master Questionnaire (7 March 2008);
- method-report authority;
- current data-access, national-documentation and errata framework.

The official geometry and exact variable/question identities strongly align with the accepted Rawlsing source. No public producer SHA-256 was located for the downloadable SAV, so this is not asserted as a producer-published cryptographic binding of Rawlsing's exact SHA to v5.0.0.

## Malformed text — semantic law closed

No attempt was made to “fix” malformed SAV UTF-8 metadata.

The source-specific semantic law is now:

```
accepted native variable / MR identity
  -> join to current producer documentation by stable variable/question identity
  -> take semantic text from ZA4800 v5 Variable Report
  -> take original wording/routing from Master Questionnaire when needed

compatibility-rendered malformed SAV text
  -> retain as opaque physical metadata
  -> never use as semantic authority
```

Unaligned producer text remains `UNKNOWN_PRODUCER_TEXT`.

This closes the prior MR-label blocker without inventing a byte-repair transform.

## All 13 native MR sets mapped

All 13 accepted native MR identities have producer-backed semantic mappings:

1. `q5a` — Q5a voluntary-organisation membership, `v10..v25`
2. `evs_q5a` — exact physical alias of q5a
3. `vv25` — Q5a substantive body `v10..v24`, excluding `v25=None`
4. `q5b` — Q5b unpaid voluntary work, `v28..v43`
5. `evs_q5b` — exact physical alias of q5b
6. `vv43` — Q5b substantive body `v28..v42`, excluding `v43=None`
7. `evs_q6` — Q6 groups not wanted as neighbours, `v46..v60`
8. `q14` — Q14 job aspects personally important, `v69..v86`
9. `evs_q14` — exact physical alias of q14
10. `q52` — Q52 child qualities, `v170..v181`
11. `evs_q52` — exact physical alias of q52
12. `evs_q107` — Q107 household-member presence, `v323,v324a..v328a`
13. `evs_q108` — Q108 family events experienced, `v329a..v334a`

All remain native MR topology. They are not to be flattened into unrelated independent variables.

### Ordering/rank

None of the 13 sets is rank-ordered.

Q52 has a **maximum-five selection constraint**, not rank significance.

For Q107 and Q108 the corresponding `b` variables have distinct non-MR roles:

- Q107 `v324b..v328b`: category counts;
- Q108 `v329b..v334b`: age at first experience.

They must not be absorbed into the MR sets.

### Alias/overlap law

Exact duplicates:

- `q5a == evs_q5a` by membership;
- `q5b == evs_q5b`;
- `q14 == evs_q14`;
- `q52 == evs_q52`.

These are distinct native set identities but one producer semantic battery each. Preserve both source identities; do not double-count them analytically.

Overlaps:

- `vv25 = q5a - v25`;
- `vv43 = q5b - v43`.

Current producer flag documentation (`f25` / `f43`) independently establishes the semantic distinction: the shortened sets are the substantive category bodies and the omitted coordinates are explicit **None** responses.

## MR missingness and routing

Current ZA4800 integrated MR variables generally use:

- `1` mentioned / yes;
- `0` not mentioned / no;
- `-1` don't know;
- `-2` no answer;
- `-3` not applicable;
- `-4` question not asked;
- `-5` other missing.

These codes are applied only where the producer documents them; they are not a universal license to reinterpret other physical sentinels.

Recovered local exceptions include:

- Q5b Denmark: not implemented -> `-4`;
- Q6 Austria, Belarus, Denmark, France, Italy, Norway, Slovenia: not implemented -> `-4`;
- Q6 Finland: producer auxiliary “no such groups” -> `0`, “can't say” -> `-1`;
- Q107 Finland: “none above” auxiliary -> `0`;
- Q108 Finland: “none above” -> `0`, “can't say” -> `-1`;
- Q107 routing: Q105=00 skips Q106 and proceeds to Q107; Q107 itself is not thereby inapplicable.

Country and filter authority must remain variable/question × country local.

## `f201` contradiction closed

The prior compatibility-rendered heading points to the wrong semantic neighborhood.

Current GESIS ZA4800 v5 documentation explicitly states:

- `f201` governs **`v201/v202`**;
- if `v201 == v202`, then `f201=1`;
- `0=consistent`;
- `1=inconsistent`.

Therefore the accepted semantic relation is `f201 -> v201/v202`. The stray Q55/Q56-style heading is not authority.

## Producer corrections / revised export context

Recovered current producer law includes:

- current release ZA4800 v5.0.0;
- refined Scientific Use File / Restricted Use File access and anonymization split;
- the Azerbaijan 2008 survey is **not integrated in the current file** because GESIS reports data-quality concerns;
- older national datasets are retained for replication and country-specific variables, while updated national data are integrated into the current cross-country file;
- current variable documentation and errata outrank stale/malformed label text for semantic corrections.

## Exact remaining blocker

Accepted physical evidence says `v372` has a typed user-missing date rendered as:

`1582-10-13`

with 1,917 affected records.

Producer documentation proves:

- `v372` is Q137 **date of interview**;
- Great Britain had invalid dates outside its official survey period converted to **system missing**;
- Netherlands did not implement Q137 in the field questionnaire but supplied date data;
- Sweden has no date data because of postal mode.

But no producer document located by this worker assigns an exact semantic meaning to the **`1582-10-13` user-missing sentinel itself**.

So it is currently lawful only as:

`USER_MISSING__SEMANTIC_REASON_UNKNOWN`

scoped to `v372` alone.

It is **not** lawful to relabel it as DK, NA, NAP, question-not-asked, other-missing, or any other conventional code by inference from date formatting.

That unresolved sentinel meaning prevents full L2 PASS.

A secondary provenance limitation also remains: no public producer SHA-256 was found that cryptographically binds the frozen Rawlsing SAV to ZA4800 v5.0.0, although documentary alignment is otherwise strong.

## Outputs

- `00_RETURN.md`
- `01_DOCUMENTARY_SOURCE_LEDGER.csv`
- `02_MR_SET_AUTHORITY_MAP.csv`
- `03_TEXT_SENTINEL_ROUTING_AUTHORITY.md`
- `04_SOURCE_ADMISSION_PACKET.json`
- `RETURN.json`

## Handoff

The next lawful move is **not** another generic decoder pass.

A source-specific realization may proceed for the 13 MR sets, producer-text substitution-by-identity, `f201`, and documented country routing while retaining malformed raw labels as non-semantic.

Full source admission remains gated only by the exact unresolved set recorded in `04_SOURCE_ADMISSION_PACKET.json`, chiefly the producer meaning of the `v372` typed user-missing sentinel.

