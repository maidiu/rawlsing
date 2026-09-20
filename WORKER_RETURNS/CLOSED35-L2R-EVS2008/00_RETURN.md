# CLOSED35-L2R-EVS2008 — EVS 2008 V372 / Release-Binding Recovery

Status: `BOUNDED_PASS__DOCUMENTARY_REALIZATION_AUTHORITY_CLOSED__PUBLIC_PRODUCER_FILE_HASH_UNAVAILABLE`

Repository: `maidiu/rawlsing`  
Base: `agent/vozhd-closed35-l2-documentary-fanin-r1`  
Accepted base tip: `5c582e2325ecc2b37377cd518fe4c456331c81d8`  
Worker branch: `agent/rabochii-closed35-l2r-evs2008-v372-release-binding-r1`

Canonical Rawlsing source:

- `EVS 2008.sav`
- SHA-256 `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`

No raw SAV bytes were opened in this worker.

## Scope discipline

This worker reopened **only**:

1. `EVS2008_V372_SENTINEL_REASON`
2. `EVS2008_EXACT_RELEASE_HASH_BINDING`

The already-closed 13 MR sets, MR alias/overlap law, routing, malformed-text producer alignment, and `f201` relation remain inherited unchanged from `WORKER_RETURNS/CLOSED35-L2-EVS2008/`.

## 1. V372 residual — recovered at lawful realization grain

Inherited accepted physical evidence for `v372` is:

- variable: `v372`
- source ordinal: `466`
- producer question: Q137, date of interview
- rows: `66,280`
- ordinary-present: `64,363`
- user-missing: `1,917`
- accepted typed user-missing rendering: `1582-10-13`
- accepted system-missing count in the frozen physical census: `0`

### Producer missing-value authority

The current ZA4800 v5.0.0 Variable Report states that **for all variables** EVS uses a standardized negative missing-value set:

- `-1` = don't know
- `-2` = no answer
- `-3` = not applicable, including missingness caused by filter questions and missing values in administrative variables
- `-4` = question not asked / not included in the national field questionnaire / not provided
- `-5` = other missing, including system missing, wild codes, and illogical answer patterns

The same report identifies `v372` as Q137 **date of interview** and records v372-specific national notes:

- Great Britain: dates outside the official survey period were recoded into system missing;
- Netherlands: Q137 was not implemented in the field questionnaire, but date data were supplied by the country;
- Sweden: date data were unavailable because of postal mode.

The producer does **not** publish on the v372 documentation page a frequency table mapping the 1,917 missing records to individual negative subcodes.

### Why `1582-10-13` is not the producer semantic code

IBM SPSS date variables are numeric values stored as seconds relative to midnight 14 October 1582. The EVS negative missing codes therefore lie seconds immediately before that epoch. If converted to a date-only representation, negative values such as `-1`, `-2`, `-3`, `-4`, and `-5` all fall on the preceding calendar day and can render identically as:

`1582-10-13`

Accordingly, the inherited displayed date is a **representation collision**, not a unique EVS semantic category.

The lawful relation is:

```
accepted physical witness: 1582-10-13
        |
        v
EVS standardized negative missing domain {-1,-2,-3,-4,-5}
        |
        v
exact negative subcode / subreason UNKNOWN from this rendered witness
```

It is unlawful to infer from the displayed date alone that the records are specifically DK, no answer, NAP, question-not-asked, other-missing, or system-missing.

### V372 disposition

The exact realization state is:

`EVS_STANDARDIZED_MISSING__NEGATIVE_SUBCODE_NOT_RECOVERABLE_FROM_DATE_RENDERING`

with:

`missing_reason_detail = UNKNOWN_WITHIN_PRODUCER_NEGATIVE_MISSING_DOMAIN`.

That closes the former diffuse sentinel blocker at realization-authority grain: the 1,917 records are producer-domain **missing**, not ordinary historical dates, but the available lawful evidence does not identify a single producer subreason.

A future authorized exact numeric-storage realization may refine this state if it exposes the original `-1..-5` numeric code(s). This worker does not open raw bytes to do so.

## 2. Exact release binding

### Documentary release identity — closed

Current producer documentation establishes:

- study: **EVS 2008 Integrated Dataset**
- GESIS study number: **ZA4800**
- version: **5.0.0**
- release date: **2022-06-08**
- DOI: **10.4232/1.13841**
- documented cases: **66,280**
- documented release surface: **477 variables**

The current Variable Report is itself titled as documentation of the June 2022 release and identifies ZA4800 Version 5.0.0.

It also documents the administrative `version` variable as the GESIS archive version and shows `5.0.0 (2022-06-08)` for all 66,280 documented cases.

GESIS/DOI metadata further preserve the version lineage from earlier ZA4800 deposits into the current DOI.

This is a strong producer-side chain for:

`DOCUMENTARY_RELEASE_IDENTITY = ZA4800 v5.0.0`.

The Rawlsing source independently has exact internal byte identity:

`RAWLSING_CANONICAL_BYTE_IDENTITY = SHA256 5469e3...ac379`

and accepted exact geometry `66,280 × 477`.

### Byte-exact producer checksum binding — unavailable on searched public surfaces

Public research checked:

- the current GESIS EVS 4th-wave release page;
- the current ZA4800 v5.0.0 Variable Report/catalogue;
- GESIS EVS data-access documentation;
- GESIS version-history/errata references;
- DOI/B2FIND/DataCite-facing metadata and related-version lineage;
- public searches for ZA4800 v5.0.0 SHA-256, MD5, checksum, file digest, archive manifest, and versioned SAV filename-plus-digest surfaces.

No producer-published SHA-256, MD5, signed file manifest, or other public digest for the v5.0.0 SAV was located.

Therefore this worker does **not** assert:

`5469e3...ac379 == PRODUCER_PUBLISHED_ZA4800_V5_SAV_DIGEST`.

The strongest lawful chain is:

```
GESIS documentary release identity
  ZA4800 v5.0.0 / 2022-06-08 / DOI 10.4232/1.13841
        +
documented geometry and stable producer variable identities
        +
Rawlsing exact canonical SHA and accepted SR03 physical census
        =
STRONG_DOCUMENTARY_RELEASE_BINDING

not

BYTE_EXACT_PRODUCER_CHECKSUM_BINDING
```

The absence claim is bounded to searched **public** producer/DOI surfaces. It does not claim GESIS lacks a nonpublic internal checksum.

## 3. Admission consequence

EVS 2008 is now documentarily realizable without guessing:

- inherited MR/text/routing/F201 authority remains closed;
- v372 can be carried as missing with its subreason explicitly unresolved inside the producer-defined negative missing domain;
- ZA4800 v5.0.0 is the governing documentary release identity;
- Rawlsing's SHA remains the exact canonical byte identity;
- the two identities must not be collapsed into a producer-checksum claim.

The only residual is provenance strength at the **byte-exact producer checksum** layer. That does not block source-specific semantic realization, but it forbids claiming cryptographic producer equivalence.

## 4. Principal authorities

Producer:

- GESIS EVS 2008 fourth-wave documentation / current dataset page
- EVS 2008 Variable Report, ZA4800 v5.0.0, DOI `10.4232/1.13841`
- GESIS EVS data-access/version-history documentation
- DOI/B2FIND/DataCite-facing ZA4800 version metadata

Technical representation:

- IBM SPSS Statistics — Dates and Times in IBM SPSS Statistics
- IBM SPSS Statistics — Input versus display formats

Repository:

- `WORKER_RETURNS/CLOSED35-L2-EVS2008/`
- accepted Authority71 R04 EVS physical evidence
- accepted SR03 R3 physical-census adjudication

## Terminal

`CLOSED35_L2R_EVS2008_RELEASE_HASH_UNAVAILABLE__DOCUMENTARY_REALIZATION_AUTHORITY_OTHERWISE_CLOSED`
